<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB E1 020 Allocation and assignment engine v1 v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB E1 020 Allocation and assignment engine v1 v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-020 Allocation and assignment engine v1

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-020 |
| Epic | E1, release 30 November 2026 |
| Module | P3 Case and workflow |
| Feature | FEAT-CWC-07 Run the allocation rule table; FEAT-CWC-08 Run the assignment engine by load and continuity; FEAT-CWC-09 Send a case to the overflow queue when no rule matches |
| Requirement IDs | REQ-CWC-007, REQ-CWC-008, REQ-CWC-009, REQ-CWC-016 |
| BRD section | Business Requirements Epic 1, section 3.3; Business Requirements Program, section 5.3 |
| L3 process | 18.3.2 Allocate work to teams, people and partners by rule; 6.1 Take over the case at 90 days past due |
| Decision | D6 entry, take over and own the case |
| Priority | Must |
| Depends on | RWB-E1-018, RWB-E1-019, RWB-E1-027, RWB-E1-056 |
| Status | Ready for build |

## 1. Story

As a **team manager (RW-TEAMMGR)**, I want **every new recovery case placed in a queue and given an owner by the allocation and assignment rule tables on the morning it arrives**, so that **each case at 90 days past due has one owner from its first day and nobody allocates cases by hand**.

## 2. Business rationale

Cases are allocated today from team spreadsheets, and ownership is agreed by email, so a case can wait days with no owner. This story places every new case in a queue and gives it an owner by rule before 07:00 on the morning after case creation, with the rule row and version on a decision log entry. It meets REQ-CWC-007, REQ-CWC-008, REQ-CWC-009 and REQ-CWC-016, and serves the business measure "cases inside the service level" (target set with DL22) and control CTL-03.

## 3. Preconditions

- RWB-E1-018 is done: new cases exist with status NEW, product group, region and exposure band.
- RWB-E1-019 is done: queues, queue members and caseload caps are loaded; queue "MTG-BKK-CO" belongs to team "MTG-BKK" and role RW-CASEOWN.
- RWB-E1-027 is done: the decision log writer is available through its published interface.
- RWB-E1-056 is done: JOB-03 has a run book and appears in the job monitor.
- The allocation table version "ALLOC-2026.11" is loaded and approved (rule rows with rule table ALLOCATION; DL24). Every row holds row ID, product group, region, exposure band, target queue, valid from, valid to, approver and test case ID.
- Parameters loaded through RWB-E1-042: `allocation.exception.queue.code` = "RWB-EXC" and `allocation.deviation.queue.code` = "DEV-HANDLER" (assumed values; DL23).
- JOB-02 case creation has completed for today's business date after v_ace_batch_status showed the ALS batch COMPLETED.
- The job runs as service identity SY-CASEWF; rules are evaluated as SY-RULES.

## 4. Flow

1. Quartz: starts JOB-03 Morning allocation after JOB-02 completes for business date 2026-12-01.
2. AllocationJob: selects every case with status NEW whose last allocation date is before the business date.
3. AllocationService: locks the case row and reads deviation_open; a case with an open deviation goes to the deviation handler queue (R-DEV-01).
4. AllocationRuleEvaluator (SY-RULES): reads the allocation rows in force on the business date and returns the first row, in row order, whose product group, region and exposure band match the case.
5. AssignmentEngine: reads the target queue's method (DF-WRK-006) and cap (DF-WRK-007), counts the open cases of each queue member and picks the owner below the cap by the method.
6. AllocationService: in one transaction sets queue, team, owner, status ASSIGNED, stage clock start and rule version, writes the assignment with reason ALLOCATION, sets the last allocation date and writes CaseAllocated (EV-02) to the outbox.
7. AllocationService: as the last step before commit, calls DecisionLogWriter.write with the row ID, table version, queue, owner and inputs; a failed write rolls the allocation back.
8. AllocationJob: after the last case, builds the allocation summary per team (MSG-P3-011, MSG-P3-012) and sends it to the team manager through the ACE notification path.
9. AllocationJob: records the run result (cases read, assigned, overflow, exception, failed) on the job record for the monitor.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Every owner in the target queue is at or above the cap | Case goes to the overflow queue of the target queue; status stays NEW; counted in the summary | MSG-P3-011 | AC4 |
| X2 | No allocation row matches the case | Case goes to the exception queue; status stays NEW; rule gap logged; CaseAllocationFailed (EV-03) published | MSG-P3-012 | AC5 |
| X3 | Decision log write fails | Allocation rolled back; case stays NEW with no queue change; retried in the next run | MSG-P3-013 | AC6 |
| X4 | Case has deviation_open = true | Case goes to the deviation handler queue; no case owner is chosen | None | AC7 |
| X5 | The run is repeated for the same business date | Cases already allocated for that date are skipped; no second assignment or log entry | None | AC8 |
| X6 | No case has status NEW | Run completes with zero counts; summary says 0 | MSG-P3-011, MSG-P3-012 with count 0 | AC9 |
| X7 | JOB-02 has not completed for the business date | JOB-03 does not start; job monitor shows it waiting; cases stay NEW | MSG-P1-001 | AC10 |
| X8 | A rerun starts while the first run still holds a case | The case row lock stops the second worker; each case is allocated once | None | AC11 |
| X9 | The overflow queue is not set on a queue whose owners are all at the cap | Case goes to the exception queue with the reason "no overflow queue" | MSG-P3-012 | AC13 |
| X10 | A user without the right reruns JOB-03 | Refused with 403; nothing runs | MSG-P4-002 | Access test TC-E1-020-14 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the case record (RWB-E1-018), the roles, teams and queues table (RWB-E1-019), the decision log writer (RWB-E1-027) and the job monitoring (RWB-E1-056), all earlier in Epic 1 |
| Negotiable | The allocation method per queue, the cap and the queue codes are data values. The story fixes the behavior, not the values |
| Valuable | Ends allocation from spreadsheets for every new case, about 3,110 a month (DL15) |
| Estimable | One rule table, one service, one batch step, no screen |
| Small | Can be finished in two weeks or less with its tests |
| Testable | Every criterion has a test case in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Allocate a new recovery case to a queue and an owner

  Background:
    Given the allocation table version "ALLOC-2026.11" is in force from 2026-11-30
    Given the queue "MTG-BKK-CO" belongs to team "MTG-BKK" and role RW-CASEOWN
    Given the queue uses the method "ROUND_ROBIN" with a caseload cap of 150
    Given the queue "MTG-BKK-CO" has the overflow queue "MTG-BKK-OVF"
    Given the business date is 2026-12-01

  Scenario: AC1 A new case is placed in the queue its row names
    Given a new case RW-2026-000201 with status "NEW", product group "MORTGAGE", region "BKK" and exposure band "B2"
    Given allocation row "ALLOC-014" matches product group "MORTGAGE", region "BKK" and any exposure band, with target queue "MTG-BKK-CO"
    When the morning allocation run starts
    Then the system places the case in queue "MTG-BKK-CO"
    Then the case team is "MTG-BKK" and the region is "BKK"

  Scenario: AC2 The owner is chosen by the queue's method
    Given queue "MTG-BKK-CO" holds three case owners U-01, U-02 and U-03 with 120, 95 and 140 open cases
    Given the last owner given a case in the queue was U-02
    When case RW-2026-000201 is placed in the queue
    Then the system gives the case to U-03
    Then the case status becomes "ASSIGNED"
    Then the system writes an assignment record with reason "ALLOCATION" and rule ID "ALLOC-014"

  Scenario: AC3 An owner at the caseload cap is skipped
    Given the last owner given a case was U-02
    Given U-03, the next owner in turn, holds 150 open cases
    Given U-01 holds 120 open cases
    When case RW-2026-000202 is placed in the queue
    Then the system gives the case to U-01, the following owner below the cap

  Scenario: AC4 Every owner is at the cap
    Given U-01, U-02 and U-03 each hold 150 open cases
    When case RW-2026-000203 is placed in queue "MTG-BKK-CO"
    Then the system places the case in the overflow queue "MTG-BKK-OVF"
    Then the case status stays "NEW" and no owner is set
    Then the team manager of "MTG-BKK" receives the allocation summary with MSG-P3-011 and count 1

  Scenario: AC5 No allocation row matches
    Given a new case RW-2026-000204 with product group "SSME" and region "NE3" that matches no allocation row
    When the morning allocation run starts
    Then the system places the case in the exception queue "RWB-EXC"
    Then the case status stays "NEW"
    Then the system writes a decision log entry with final call "RULE_GAP", product group "SSME" and region "NE3"
    Then the system publishes caseAllocationFailed with reason "NO_ROW_MATCHED"
    Then the allocation summary carries MSG-P3-012 with count 1

  Scenario: AC6 Every allocation is logged
    Given case RW-2026-000205 matches row "ALLOC-014" and owner U-02 is below the cap
    When the case is placed in the queue and given an owner
    Then the system writes one decision log entry with rule ID "ALLOC-014", rule version "ALLOC-2026.11", queue "MTG-BKK-CO", owner U-02 and the inputs used
    Then if the decision log write fails, the allocation is not made, the case stays "NEW" with no queue and the job record carries MSG-P3-013 for the case

  Scenario: AC7 A case with an open deviation is not allocated to a case owner
    Given a new case RW-2026-000206 with deviation_open = true
    When the morning allocation run starts
    Then the system places the case in the deviation handler queue "DEV-HANDLER" named by rule R-DEV-01
    Then the system sets no case owner and the status stays "NEW"

  Scenario: AC8 A repeated run for the same date has no further effect
    Given the morning allocation run for 2026-12-01 has assigned case RW-2026-000201 to U-03
    When the run for 2026-12-01 is started again from the job monitor
    Then case RW-2026-000201 keeps owner U-03 and its one assignment record
    Then the system writes no second decision log entry for the case
    Then the job record shows 1 case skipped as already allocated

  Scenario: AC9 A run with no new cases
    Given no case has status "NEW" on 2026-12-01
    When the morning allocation run starts
    Then the run completes with 0 cases read
    Then the allocation summary for each team shows 0 in overflow and 0 in the exception queue

  Scenario: AC10 The run waits for case creation
    Given JOB-02 has not completed for 2026-12-01 because v_ace_batch_status holds no COMPLETED ALS row for that date
    When 07:00 passes
    Then JOB-03 has not started for 2026-12-01
    Then the job monitor shows JOB-03 waiting on JOB-02 with MSG-P1-001
    Then every NEW case keeps no queue and no owner

  Scenario: AC11 Two runs at the same time allocate each case once
    Given a first run is allocating case RW-2026-000207
    When a rerun for 2026-12-01 reaches the same case at the same time
    Then the rerun skips the locked case
    Then the case has exactly one assignment record and one decision log entry for 2026-12-01

  Scenario: AC12 An owner one case below the cap gets the case
    Given U-03 is next in turn and holds 149 open cases
    When case RW-2026-000208 is placed in queue "MTG-BKK-CO"
    Then the system gives the case to U-03
    Then U-03 now holds 150 open cases

  Scenario: AC13 A queue with no overflow queue sends the case to the exception queue
    Given queue "HP-CEN-CO" has no overflow queue
    Given every owner in queue "HP-CEN-CO" holds 150 open cases
    When case RW-2026-000209 is placed in queue "HP-CEN-CO"
    Then the system places the case in the exception queue "RWB-EXC" with reason "NO_OVERFLOW_QUEUE"
    Then the case status stays "NEW"
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A case is allocated by the first row of the allocation table, in row order, whose product group, region and exposure band match the case. "Any" in a column matches every value | Allocation table (rule_row, rule table ALLOCATION), DL24; REQ-CWC-008 |
| BR2 | The owner is chosen by the method held on the queue: ROUND_ROBIN, LOWEST_LOAD, NAMED_OWNER or SKILL | queue.assignment_method (DF-WRK-006), LOV-ASSIGN |
| BR3 | An owner at or above the queue's caseload cap is skipped. Open cases are cases in the queue owned by the person with status other than CLOSED | queue.capacity_cap (DF-WRK-007); values DL23 |
| BR4 | A case that cannot be given an owner goes to the overflow queue of its queue | queue.overflow_queue_id (DF-WRK-008) |
| BR5 | A case that matches no row goes to the exception queue, and the gap is logged. R-UNI-41 handles the case once a person decides | R-UNI-41; FEAT-CWC-09 |
| BR6 | A case with an open deviation goes to the deviation handler queue | R-DEV-01 |
| BR7 | A decision that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39; CTL-06 |
| BR8 | A case is allocated at most once per business date | R-UNI-40; events.txt rule "Duplicates" |
| BR9 | Each allocation records the rule row and the table version | REQ-CWC-016; CTL-03 |

## 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| New | Allocation rule matched | Row matched and an owner below the cap | Assigned |
| New | Allocation rule matched | Row matched and every owner at the cap | New, in the overflow queue |
| New | Allocation rule matched | No row matched | New, in the exception queue |
| New | DEVIATION_FLAGGED (R-DEV-01) | deviation_open = true | New, in the deviation handler queue |

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-RULES, rules component | Evaluates the allocation table (Rules and parameters R) |
| SY-CASEWF, case workflow module | Updates the case and writes the assignment (Case record CRU; Queue and allocation CRU) |
| SY-DECLOG, decision log writer | Writes the entry (Decision log C) |
| RW-TEAMMGR, team manager | Reads the queue and the allocation summary for their team (Queue and allocation R) |
| RW-CASEOWN, case owner | Reads the cases given to them (Case record R, scope Own) |
| RW-PLATADM, platform administrator | Reruns JOB-03 from the job monitor (Platform administration U) |
| RW-REFADM, reference data administrator | Prepares the allocation table load file; the load is RWB-E1-029 |
| Process owner for L1 18, Shared operations | Approves each allocation table version (reference data change process, step 4). No delegation of authority level applies |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
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
| DF-CAS-021 | recovery_case | rule_version | Write |
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
| DF-REF-002 | rule_row | rule_id | Read |
| DF-REF-003 | rule_row | rule_version | Read |
| DF-REF-007 | rule_row | condition_expr | Read |
| DF-REF-012 | rule_row | valid_from | Read |
| DF-REF-013 | rule_row | valid_to | Read |
| DF-REF-052 | rule_row | rule_table | Read |
| DF-REF-053 | rule_row | row_order | Read |
| DF-REF-054 | rule_row | target_queue_code | Read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Job**

| Item | Value |
|---|---|
| Trigger | Quartz, after JOB-02 completes for the business date |
| Job name | JOB-03 Morning allocation |
| Schedule | Daily after JOB-02, complete by 07:00 Asia/Bangkok |
| Input | Cases with status NEW and last_allocation_date before the business date; allocation rows in force on the business date; queues and queue members |
| Output | Case queue, team, owner, status and rule version; assignment rows; decision log entries; allocation summary per team; job record with counts |
| Events published | CaseAllocated (EV-02: caseId, queueId, ownerId, ruleId, ruleVersion); CaseAllocationFailed (EV-03: caseId, reason, ruleGap) |
| Idempotency key | caseId and businessDate. A case with last_allocation_date equal to the business date is skipped |
| Restart | Rerun from the job monitor (POST /api/recovery/v1/admin/jobs/{jobId}/rerun). A rerun processes only cases not yet allocated for the date. Chunk commit per case, so a failure in one case does not undo the others |

**Endpoint used to read the result**

| Item | Value |
|---|---|
| Method and path | GET /api/recovery/v1/cases/{caseId} |
| Request | Path caseId (uuid) |
| Response | Case: queueId, teamCode, ownerUserId, status, ruleVersion |
| Errors | 401 no session (MSG-P4-001); 403 role lacks Case record R (MSG-P4-002); 404 not found or outside scope (MSG-P4-003); 503 store unavailable |
| Authorization | Case record, right R, scope applied |
| Idempotency | Not applicable |

**Endpoint used to rerun the job (P1)**

| Item | Value |
|---|---|
| Method and path | POST /api/recovery/v1/admin/jobs/{jobId}/rerun |
| Response | Job: id, type, businessDate, status, checks |
| Errors | 401; 403 role lacks Platform administration U (MSG-P4-002); 404 job not found; 409 job already running (MSG-GEN-004) |
| Authorization | Platform administration, right U |
| Idempotency | The rerun follows the job's idempotency key above |

**Published interfaces**

```java
// P3, package recovery.casewf.allocation (published)
public interface AllocationService {
    AllocationOutcome allocate(UUID caseId, LocalDate businessDate);
}
public record AllocationOutcome(UUID caseId, OutcomeType type, UUID queueId,
        UUID ownerUserId, String ruleId, String ruleVersion, String reason) {}
public enum OutcomeType { ASSIGNED, OVERFLOW, EXCEPTION, DEVIATION_QUEUE, SKIPPED, FAILED_LOG }

// P7, used by this story (RWB-E1-027)
// package recovery.decision.writer; called inside the caller's transaction as the last step before commit
public interface DecisionLogWriter {
    DecisionLogEntryRef write(DecisionLogRecord record)
        throws DecisionLogRecordInvalidException, DecisionLogUnavailableException;
}

// P4, used by this story: rule rows are P4 tables
public interface RuleTableReader {
    RuleTableVersion rowsInForce(String ruleTable, LocalDate onDate);
}
```

## 13. Solution plan

**Package.** `src/main/java/.../recovery/casewf/allocation`, Java package `recovery.casewf.allocation`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AllocationJob | Job | Quartz job for JOB-03; selects NEW cases, calls AllocationService per case, builds the summary, writes job counts |
| AllocationService | Published interface | Implementation AllocationServiceImpl: lock, deviation check, rule match, owner choice, decision log write, case update, outbox event |
| AllocationRuleEvaluator | Service | Evaluates the allocation rows returned by RuleTableReader in row order; first match wins |
| AssignmentEngine | Service | Applies ROUND_ROBIN, LOWEST_LOAD, NAMED_OWNER or SKILL with the cap |
| OwnerLoadRepository | Repository | Counts open cases per owner in a queue (ix_case_owner_status) |
| CaseAndWorkflowRepository | Repository | Reads and updates recovery_case, queue, queue_member, assignment |
| AllocationSummaryBuilder | Service | Counts overflow and exception cases per team; fills MSG-P3-011 and MSG-P3-012 |
| AllocationRuleTable | Rule table | Rule rows with rule table ALLOCATION, read through RuleTableReader |

**Database**

- Reads: recovery_case (id, case_no, product_group, region_code, exposure_band, deviation_open, status, last_allocation_date), queue (id, queue_code, team_code, role_code, assignment_method, capacity_cap, overflow_queue_id), queue_member (user_id, capacity).
- Writes: recovery_case (status, owner_user_id, queue_id, team_code, stage_clock_start, rule_version, last_allocation_date, version), queue (rr_cursor_user_id), assignment (all columns), outbox.
- Lock: `SELECT ... FROM recovery_case WHERE id = ? AND status = 'NEW' FOR UPDATE SKIP LOCKED`; optimistic version column on update.
- Migration in this story: `V020_1__allocation_columns.sql` adds recovery_case.last_allocation_date (date) and queue.rr_cursor_user_id (uuid). queue_member is created by RWB-E1-019.

**Configuration and reference data**

- Allocation table version "ALLOC-2026.11" (rule_row, rule table ALLOCATION), prepared by RW-REFADM, loaded by RW-COE through RWB-E1-029, approved by the Shared operations process owner.
- Queues and members from RWB-E1-019; caps DL23.
- Parameters from RWB-E1-042: `allocation.exception.queue.code`, `allocation.deviation.queue.code`.
- Lists LOV-ASSIGN, LOV-ASSIGN-REASON, LOV-CASE-STATUS (P4 lov_value).

**Build steps**

1. AllocationRuleEvaluator: given a case snapshot and the rows of a version, return the first matching row or none. Unit tests per BR1 with "any" values.
2. AssignmentEngine: implement the four methods with cap skipping and the round robin cursor. Unit tests for AC2, AC3, AC12 boundary.
3. OwnerLoadRepository: open case count per owner and queue; integration test on PostgreSQL with Testcontainers.
4. AllocationServiceImpl: lock, deviation branch, rule match, overflow and exception branches, then case update, assignment and outbox row in one transaction with the decision log write as its last step.
5. Idempotency: skip when last_allocation_date equals the business date; return SKIPPED.
6. AllocationJob: Quartz job with `@DisallowConcurrentExecution`, dependency on JOB-02 completion, per-case transaction, job counts.
7. AllocationSummaryBuilder and the call to the ACE notification path for each team manager.
8. System tests TC-E1-020-01 to TC-E1-020-15 on the synthetic case set.

**Feature flag.** `rwb.p3.allocation`. Off: JOB-03 does not run and cases stay NEW.

**Done when.** The tests in section 16 pass; TC-E1-020-01 and TC-E1-020-08 are in the regression suite; JOB-03 finishes 3,110 synthetic cases inside 15 minutes in SIT (assumed target; DL11).

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-011 | Allocation summary, case in overflow | {count} new cases are waiting in the overflow queue for {team}. Every owner is at the caseload cap. |
| MSG-P3-012 | Allocation summary, no row matched | {count} new cases matched no allocation row and are in the exception queue. |
| MSG-P3-013 | Decision log write failed for a case | The case was not allocated because the decision could not be recorded. It will be tried again in the next run. |
| MSG-P1-001 | JOB-03 waiting because the ACE batch has not completed | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | A role without the right reruns the job | You cannot {action} here. Your role does not include it. |

Thai text for each message follows decision DL10.

## 15. Screens and states

No new screen in Epic 1. SCR-02 Case list (states Loading; list) shows the queue, the owner and the status of each case after the run. SCR-09 Exception queue (states Loading; list) shows cases placed in "RWB-EXC". The team manager receives the allocation summary after each run. Queue screens come in Epic 2 (SCR-07).

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-020-01 | AC1, BR1 | System | One case per product group and region in the synthetic set |
| TC-E1-020-02 | AC2, BR2 | System | Three owners with 120, 95 and 140 open cases, round robin |
| TC-E1-020-03 | AC3, BR3 | System | Next owner at 150 open cases |
| TC-E1-020-04 | AC4, BR4 | System | Every owner at 150 open cases |
| TC-E1-020-05 | AC5, BR5 | System | Product group SSME and region NE3 with no row |
| TC-E1-020-06 | AC6, BR9 | System | Allocation run over the synthetic set; one log entry checked per case; log write forced to fail for one case |
| TC-E1-020-07 | AC7, BR6 | System | Case with deviation_open = true |
| TC-E1-020-08 | AC8, BR8 | System | The same run repeated for 2026-12-01 |
| TC-E1-020-09 | AC9 | System | No NEW cases |
| TC-E1-020-10 | AC10 | System | JOB-02 not complete for the business date |
| TC-E1-020-11 | AC11, BR8 | System | Two workers on the same case |
| TC-E1-020-12 | AC12, BR3 | System | Next owner at 149 open cases |
| TC-E1-020-13 | AC13, BR4 | System | Queue HP-CEN-CO with no overflow queue and every owner at 150 |
| TC-E1-020-14 | Access | Access | RW-CASEOWN reruns JOB-03 and is refused with MSG-P4-002 |
| TC-E1-020-15 | Principle 5 | Resilience | Decision log write forced to fail for every case in the run |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No allocation value is written in code. Product groups, regions, bands, queues, methods, caps and queue codes are read from tables and parameters.
- No personal data in the allocation summary, the logs, the events or the test data. Cases are named by case number only.
- The service never reads tables owned by another module. Rule rows come through RuleTableReader (P4); the decision log through DecisionLogWriter (P7).
- The decision log entry is written in the same transaction as the case change; a failed write leaves the case unchanged.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-007 | Every new case placed in a queue and assigned by rule | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-07 | 18.3.2 | R-DEV-01 | TC-E1-020-01, TC-E1-020-02, TC-E1-020-09 |
| REQ-CWC-008 | Allocation rules apply first match and always have a default | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-07, FEAT-CWC-09 | 18.3.2 | R-UNI-41 | TC-E1-020-01, TC-E1-020-05, TC-E1-020-07 |
| REQ-CWC-009 | Round robin, lowest load, named owner, cap and overflow | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-08 | 18.3.2 | R-UNI-19 | TC-E1-020-02, TC-E1-020-03, TC-E1-020-04, TC-E1-020-12, TC-E1-020-13 |
| REQ-CWC-016 | Every allocation logged with rule ID and version | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-07 | 6.1 | R-UNI-39, R-UNI-40 | TC-E1-020-06, TC-E1-020-08, TC-E1-020-11, TC-E1-020-15 |

## 19. Out of scope

- Manual transfer and reassignment screens (RWB-E2-011, RWB-E2-012).
- Reallocation when an owner leaves or passes the cap (R-UNI-18 and R-UNI-19, Epic 2; daily rebalancing in RWB-E1-030).
- The values of the caseload caps and the service levels (DL22, DL23).
- Loading and validating the allocation table (RWB-E1-029).
- Placement on a queue by a model or an agent (RWB-E2-036).
