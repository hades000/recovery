<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB TE 008 Decision log hash chain check v1.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB TE 008 Decision log hash chain check v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-TE-008 Decision log hash chain check

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-TE-008 |
| Epic | E1, release 30 November 2026 |
| Module | P7 Decision center and log |
| Feature | None |
| Requirement IDs | REQ-DRI-003 |
| BRD section | Business Requirements Epic 1, section 3.7; Business Requirements Program, sections 5.7 and 6.6 |
| L3 process | 17 Run the decision center |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-008, RWB-TE-007 |
| Status | Ready for build |

## 1. Story

As an **internal auditor (RW-AUDIT)**, I want **a nightly job that recomputes the whole decision log hash chain, records the result with the last hash, and reports a break to Compliance the same day**, so that **a changed entry is found the day it happens and the log can be relied on in audit**.

## 2. Business rationale

The decision log is evidence only while nobody can change an entry unseen. The database refuses updates and deletes (RWB-E1-008), but a change made outside the service, for example by a database administrator, is found only by recomputing the chain. This story runs that check as JOB-14 every night after the decision log copy, records each run with its last hash, and tells Compliance of a break, an incomplete run or an intact chain. It meets REQ-DRI-003 and NFR-035 and supports control CTL-06. The measure is a daily check with a same-day report: target 100 percent of nights.

## 3. Preconditions

- RWB-E1-008 is done: HashChainVerifier, CanonicalEntryForm and ChainBreakNotifier exist.
- RWB-TE-007 is done: jobs run on Quartz in the ACE service with job run records shown by GET /admin/jobs.
- JOB-13 Decision log copy is scheduled nightly at 01:00 (RWB-E1-014).
- Parameters in the catalog: rwb.decision.chaincheck.start=02:00, rwb.decision.chaincheck.latest-start=04:00, rwb.decision.chaincheck.batch-size=1000, all Asia/Bangkok (assumed; owner RW-COMPLY).
- The Compliance and PDPA officer group and the platform administrator group are set in the ACE notification path.

## 4. Flow

1. Quartz: fires JOB-14 at 02:00 Asia/Bangkok for the business date of the previous day.
2. Job (HashChainCheckJob): checks that JOB-13 for the same business date has ended; if not, waits and checks again every 5 minutes until 04:00, then runs and records that JOB-13 had not ended.
3. Job: reads the highest chain_seq at the start and fixes it as the end of the run; entries appended later are checked the next night.
4. Job: calls HashChainVerifier over chain_seq 1 to the end in batches of 1,000, recomputing each entry_hash and checking each prev_hash.
5. Job: counts every entry that fails and keeps the first.
6. Job: writes the job run record with type JOB-14, business date, status and checks: entries checked, last chain_seq, last entry_hash, result, first break chain_seq and entry ID, failing count.
7. Job: sends MSG-P7-007 to Compliance when the chain is intact, or MSG-P7-008 with an incident when it is broken.
8. Job: on an error that stops the run, records status FAILED, alerts the platform administrator and sends MSG-P7-013 to Compliance.
9. Platform administrator: can rerun the job for the business date from the job monitor; a rerun is a new run record.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | An entry does not match its hash or its prev_hash | Run result BROKEN; first break and failing count recorded; incident; Compliance told | MSG-P7-008 | AC2, AC7 |
| X2 | The run stops on an error, for example a lost database connection | Status FAILED; platform administrator alerted; Compliance told the check did not complete | MSG-P7-013 | AC3 |
| X3 | The job is rerun for the same business date | A new run record with the same checks; the report says it is a rerun; no second scheduled run starts | MSG-P7-007 or MSG-P7-008 | AC4 |
| X4 | The log is empty | Result INTACT with count 0 and the genesis hash | MSG-P7-007 | AC5 |
| X5 | JOB-13 has not ended at 02:00 | The job waits up to 04:00, then runs and records the late copy | MSG-P7-007 or MSG-P7-008 | AC6 |
| X6 | Entries are appended while the job runs | They are outside this run and are checked the next night | None | AC8 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the verifier from RWB-E1-008 and the scheduler from RWB-TE-007 |
| Negotiable | Start times and batch size are parameters |
| Valuable | A changed entry is found by the morning after it is changed |
| Estimable | One Quartz job, one report, no screen |
| Small | Fits in one week with its tests |
| Testable | Each criterion below is one test in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Decision log hash chain check

  Background:
    Given the environment is SIT with the synthetic decision log
    Given JOB-13 for business date 2 December 2026 ended at 01:40 on 3 December 2026

  Scenario: AC1 Chain intact
    Given the decision log holds 48,210 entries and none has been changed
    When JOB-14 runs at 02:00 on 3 December 2026
    Then the job run record shows type "JOB-14", business date 2 December 2026, status "COMPLETED" and result "INTACT"
    Then its checks hold entries checked 48,210, last chain_seq 48,210 and that entry's entry_hash
    Then MSG-P7-007 with the count and the last hash is sent to the Compliance group

  Scenario: AC2 Break
    Given the actions of the entry with chain_seq 30,005 were changed in the SIT database with the trigger disabled
    When JOB-14 runs
    Then the run result is "BROKEN" with first break chain_seq 30,005 and its entry ID
    Then the system raises an incident and MSG-P7-008 with the entry ID is sent to the Compliance group before 08:00 on 3 December 2026

  Scenario: AC3 A run that stops is reported
    Given the database connection is closed in the test double after 20,000 entries
    When JOB-14 runs
    Then the run status is "FAILED" with entries checked 20,000
    Then the system alerts the platform administrator group
    Then the system sends MSG-P7-013 to the Compliance group with the date of the last complete check, 2 December 2026

  Scenario: AC4 A rerun gives a new record and no second scheduled run
    Given JOB-14 for business date 2 December 2026 failed at 02:20
    When test user "U-9301" holding RW-PLATADM reruns it from the job monitor at 08:30
    Then a second run record for business date 2 December 2026 is written with rerun true
    Then the system marks the report to Compliance as a rerun
    Then while the rerun is running a second start of JOB-14 is refused by the scheduler

  Scenario: AC5 An empty log is intact
    Given the decision log holds no entry
    When JOB-14 runs
    Then the result is "INTACT" with entries checked 0 and last hash of 64 zeros

  Scenario: AC6 The job waits for the decision log copy
    Given JOB-13 for business date 2 December 2026 is still running at 02:00 and ends at 02:25
    When JOB-14 fires at 02:00
    Then it starts the check at 02:25 and records the JOB-13 end time
    Then if JOB-13 has not ended by 04:00 the check starts at 04:00 with the note "JOB-13 not ended"

  Scenario: AC7 Several changed entries
    Given the entries with chain_seq 12,001 and 40,350 were changed in the SIT database
    When JOB-14 runs
    Then the first break is chain_seq 12,001 and the failing count is 2
    Then one incident and one MSG-P7-008 report name both entry IDs

  Scenario: AC8 Entries written during the run
    Given the log holds 48,210 entries when JOB-14 starts
    Given 37 entries are appended while it runs
    When the run ends
    Then entries checked is 48,210 and last chain_seq is 48,210
    Then the next night's run checks 48,247 entries
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The whole chain is recomputed every night and a break is reported to Compliance the same day | REQ-DRI-003; NFR-035; JOB-14 |
| BR2 | Each entry's entry_hash is recomputed from the canonical form and its prev_hash compared with the entry before | RWB-E1-008, BR3 and BR4 |
| BR3 | A run covers chain_seq 1 to the highest chain_seq at its start | This story |
| BR4 | JOB-14 runs after JOB-13 for the same business date, starting no later than 04:00 | batch.txt, daily timeline; parameters rwb.decision.chaincheck.* |
| BR5 | A run that does not complete is reported to Compliance with the date of the last complete check | NFR-035 |
| BR6 | Only one run of JOB-14 is active at a time; a rerun is a new run record | RWB-TE-007; job run record |
| BR7 | Start times and batch size are parameters, not code | Principle 1 |

## 9. State transitions

None. This story does not change a case status. A JOB-14 run moves from Waiting (for JOB-13) to Running, then to Completed with result INTACT or BROKEN, or to Failed.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-DECLOG Decision log writer | The job runs under this service identity and reads the log (Decision log C and read through the store) |
| RW-COMPLY Compliance and PDPA officer | Receives every report; owns the job (batch.txt) and its parameters |
| RW-AUDIT Internal audit | Reads the run records (Platform administration R); may not rerun |
| RW-PLATADM Platform administrator | Receives failure alerts; reruns the job (Platform administration U) |
| RW-SECADM Security administrator | Receives the break incident with Compliance |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Read |
| DF-DEC-028 | decision_log_entry | chain_seq | Read |
| DF-DEC-030 | decision_log_entry | actor_user_id | Read |
| DF-DEC-029 | decision_log_entry | corrects_entry_id | Read |

Field IDs are those in the Logical Data Model and Data Dictionary. The run result is written to the ACE job run record (Job schema), not to a recovery table.

## 12. Contract

| Item | Value |
|---|---|
| Trigger | Quartz cron 0 0 2 * * ? in Asia/Bangkok, after JOB-13 for the same business date |
| Job name | JOB-14 Hash chain check |
| Schedule | Nightly 02:00; latest start 04:00 |
| Input | decision_log_entry in chain_seq order, chain_seq 1 to the highest at start |
| Output | Job run record: type JOB-14, businessDate, status, startedAt, endedAt, checks (entriesChecked, lastSeq, lastHash, result, breakSeq, breakEntryId, failingCount, rerun, copyJobEndedAt); reports MSG-P7-007, MSG-P7-008 or MSG-P7-013 to the Compliance group; incident on a break |
| Events published | None from events.txt; the report goes through the ACE notification path |
| Idempotency key | Business date plus run number; a rerun adds a record and changes nothing else |
| Restart | A failed run is not resumed; a rerun starts again from chain_seq 1 |

**GET /api/recovery/v1/admin/jobs** (owned by P1): lists JOB-14 runs; Platform administration R. **POST /api/recovery/v1/admin/jobs/{jobId}/rerun** (owned by P1): reruns; Platform administration U; errors 401, 403 (MSG-P4-002), 404, 409 when a run is active (MSG-GEN-004).

## 13. Solution plan

- Package: folder `recovery/decision/log` in the recovery module; Java package `recovery.decision.log`.
- Components:

| Component | Type | Responsibility |
|---|---|---|
| HashChainCheckJob | Job | Quartz job with DisallowConcurrentExecution; waits for JOB-13; fixes the end chain_seq; runs the verifier; writes the run record |
| HashChainVerifier | Service | From RWB-E1-008; extended to count every failing entry and continue after the first |
| ChainCheckReporter | Service | Sends MSG-P7-007, MSG-P7-008 or MSG-P7-013 to the Compliance group; raises the incident on a break |
| JobRunRecorder | Service | Writes the ACE job run record through the scheduler interface of RWB-TE-007 |

- Database: reads decision_log_entry by chain_seq using its unique index; no table of its own.
- Configuration and reference data: parameters rwb.decision.chaincheck.start, latest-start and batch-size (RW-COMPLY); Compliance and platform administrator groups in the ACE notification path; job entry JOB-14 in the job catalog and its run book (RWB-E1-056).
- Build steps:
  1. Add JOB-14 to Quartz with the cron, time zone and no concurrent execution.
  2. Build the wait for JOB-13 with the 04:00 latest start; test AC6 with a fixed clock.
  3. Extend HashChainVerifier to count all failing entries; tests for AC2 and AC7.
  4. Build the run record and the fixed end chain_seq; tests for AC1, AC5 and AC8.
  5. Build ChainCheckReporter with the three messages; tests for AC1, AC2 and AC3.
  6. Test the rerun path and the concurrency guard for AC4.
  7. Run the timing check on 10 million synthetic entries against a 60 minute budget (assumed; DL11).
- Feature flag: `rwb.decision.hash-check`.
- Done when: the tests in section 16 pass and the run book for JOB-14 is in the job monitoring (RWB-E1-056).

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-007 | The chain is intact (new) | The decision log check for {date} passed: {count} entries checked. The last hash is {hash}. |
| MSG-P7-008 | The chain is broken | The decision log check for {date} found a break at entry {entryId}. Entries from that entry on cannot be relied on until Compliance reviews them. |
| MSG-P7-013 | The run did not complete (new) | The decision log check for {date} did not complete. The chain was last confirmed on {lastDate}. |
| MSG-P4-002 | Rerun without Platform administration U | You cannot {action} here. Your role does not include it. |

Thai text for each message follows DL10; proposed Thai for the new messages is in the additions file.

## 15. Screens and states

No screen in this story. Run records show on the job monitor through GET /admin/jobs (SCR-44 Interface and job monitor from Epic 2); Compliance receives each report by the ACE notification path.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-008-01 | AC1, BR1, BR2 | System | 48,210 synthetic entries, none changed |
| TC-TE-008-02 | AC2, BR1 | System | One entry changed in SIT with the trigger disabled |
| TC-TE-008-03 | AC3, BR5 | System | Connection closed after 20,000 entries |
| TC-TE-008-04 | AC4, BR6 | System | Failed run, then a rerun at 08:30 |
| TC-TE-008-05 | AC5 | System | Empty log |
| TC-TE-008-06 | AC6, BR4 | System | JOB-13 ending at 02:25; JOB-13 not ended by 04:00 |
| TC-TE-008-07 | AC7, BR2 | System | Two entries changed |
| TC-TE-008-08 | AC8, BR3 | System | 37 entries appended during the run |
| TC-TE-008-09 | Access | Access | A role without the right is refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: times and batch size are parameters.
- No personal data in logs, tests or prompts; reports name entry IDs and chain_seq only.
- No read of another module's tables; the job reads only decision_log_entry.
- The job never writes to decision_log_entry and never repairs an entry.
- One canonical form implementation, shared with the store.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-003 | Hash chain checked every day, break reported to Compliance the same day | Epic 1, 3.7 | FEAT-DRI-01 (store this job checks) | 17 Run the decision center | BR1 to BR7 | TC-TE-008-01 to TC-TE-008-09 |

## 19. Out of scope

- The store, the hash computation and the on-demand verifier (RWB-E1-008).
- The check of each entry returned by an audit query (RWB-E2-005).
- The decision log copy to the data lake (RWB-E1-014, JOB-13).
- Detecting a broken chain as a control breach through the administration screens (Epic 8, FEAT-ADM-10).
