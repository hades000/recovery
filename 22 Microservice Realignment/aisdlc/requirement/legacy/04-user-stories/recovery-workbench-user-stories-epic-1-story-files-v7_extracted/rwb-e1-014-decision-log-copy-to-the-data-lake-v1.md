<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7.zip!RWB E1 014 Decision log copy to the data lake v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7.zip!RWB E1 014 Decision log copy to the data lake v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-014 Decision log copy to the data lake

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-014 |
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | FEAT-RDF-20 Copy the decision log to the lake; FEAT-DRI-06 Stream the decision log to the data lake; FEAT-RPT-04 Publish operations reporting from the decision log |
| Requirement IDs | REQ-DRI-009, REQ-RDF-013 |
| BRD section | Business Requirements Epic 1, section 3.1 (story) and section 4 (REQ-DRI-009, REQ-RDF-013) |
| L3 process | 17 Run the decision center; 15 Manage performance, data and AI |
| Decision | None |
| Priority | Should |
| Depends on | RWB-E1-056, RWB-E1-017 |
| Status | Ready for build |

## 1. Story

As a **center of excellence analyst (RW-COE)**, I want **the decision log copied to the data lake each night, with a retention rule applied to the copy**, so that **reporting reads the log without touching the live log and nothing in the copy is kept longer than its rule**.

## 2. Business rationale

Reporting, audit sampling and model feedback need the full decision history, and queries against the live log slow the write path that every action depends on (ADR-009). A nightly copy that matches the live log on row count and last hash gives Power BI and audit one checked source (REC-08). The copy carries its own retention rule, so the lake does not keep decisions longer than the bank schedule allows. Serves REQ-DRI-009 and REQ-RDF-013; measure: copy matched on count and last hash on 99 percent of days (FSD P1 A2.20.1).

## 3. Preconditions

- RWB-E1-008 (decision log store) and RWB-E1-027 (decision log writer) are done, and P7 publishes the DecisionLogExport interface in section 12.
- RWB-E1-056 is done: JOB-13 has a run book, and its runs show in the job monitor.
- RWB-E1-017 is done: the retention rule table holds a row for product DP12, table decision_log_entry, record class LAKE_COPY (assumed 120 months; DL26).
- The data lake intake container for INT-19 exists in each environment and the job's service identity SY-DATALOAD can write to it.
- Quartz holds the JOB-13 trigger at 01:00 Asia/Bangkok.

## 4. Flow

1. Quartz: starts JOB-13 Decision log copy at 01:00 for business date D (the previous calendar day).
2. DecisionLogLakeCopyService: reads the watermark (last copied entry hash and cumulative count) from lake_copy_watermark.
3. DecisionLogLakeCopyService: calls DecisionLogExport.head() and fixes the cut-off: the live count and last entry hash at start.
4. DecisionLogLakeCopyService: calls DecisionLogExport.entriesAfter(watermarkHash, 5000) in chain order until it reaches the cut-off hash.
5. LakeFileWriter: writes the entries to `decision-log/business_date=D/` as Parquet files and writes `_manifest.json` with the row count, first hash, last hash and cumulative count.
6. LakeCopyReconciler: reads the manifest back from the lake and compares the cumulative count and last hash with the cut-off (REC-08, tolerance zero).
7. LakeCopyReconciler: on a match, marks the partition complete, moves the watermark forward and records the checks on the job run.
8. LakeRetentionService: reads the retention rule for DP12 LAKE_COPY and moves each partition older than the rule to the archive tier, recording the partition list, the count and the rule version on the job run.
9. Data steward: reads the run result in GET /admin/jobs and the break, if any, in the morning.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The lake count or last hash differs from the cut-off | Partition not marked complete; watermark not moved; break recorded; data steward alerted; JOB-13 runs again the next night | MSG-P1-019 | AC3 |
| X2 | JOB-13 runs again for a business date already copied | The same chain range is written to the same partition; no duplicate rows | None | AC4 |
| X3 | DecisionLogExport is unavailable or the lake write fails | Job ends Failed; previous copy and watermark kept; alert raised; rerun from the job monitor | MSG-GEN-006 | AC5 |
| X4 | No decision was written since the last copy | Empty partition with a manifest of zero rows and the unchanged last hash; checks pass | None | AC6 |
| X5 | A second start of JOB-13 while one is running | Second start refused; 409 on a manual rerun | MSG-P2-006 | AC7 |
| X6 | A partition is exactly at its retention age | The partition is kept; only partitions older than the rule move | None | AC8 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the decision log store and writer (RWB-E1-008, RWB-E1-027), the job monitoring (RWB-E1-056) and the retention rule table (RWB-E1-017), all earlier in Epic 1 |
| Negotiable | File size, lake path and retention period are configuration and data; the story fixes the copy, the match and the archive behavior |
| Valuable | Reporting and audit read the log without load on the live store |
| Estimable | One job, one watermark table, one published interface call, no screen |
| Small | Finished inside two weeks with its tests |
| Testable | Each criterion below is one automated test against a test lake container |

## 7. Acceptance criteria

```gherkin
Feature: Decision log copy to the data lake

  Background:
    Given the live decision log holds 12,480 entries with last entry hash "a3f1...09c2"
    Given the watermark shows 12,100 entries copied with last hash "77be...41d0"
    Given the retention rule for DP12 record class LAKE_COPY is 24 months, rule version "RET-2026.11"

  Scenario: AC1 Daily copy
    Given 380 entries were written on business date 2026-11-30
    When JOB-13 runs at 01:00 on 2026-12-01
    Then the partition "business_date=2026-11-30" holds 380 rows
    Then the manifest shows cumulative count 12,480 and last hash "a3f1...09c2"
    Then the data lake copy has the same row count and the same last hash as the live log
    Then the watermark moves to 12,480 and "a3f1...09c2"

  Scenario: AC2 Retention rule
    Given lake partitions for business dates 2024-11-29 and 2024-11-30 exist
    When the retention step of JOB-13 runs on 2026-12-01
    Then the partitions "business_date=2024-11-29" and "business_date=2024-11-30" move to the archive tier
    Then the job run records 2 partitions archived under rule version "RET-2026.11"

  Scenario: AC3 A copy that does not match is not published
    Given the lake write for 2026-11-30 stops after 379 of 380 rows
    When the reconciliation step compares the copy with the live log
    Then the system does not mark the partition complete
    Then the watermark stays at 12,100 and "77be...41d0"
    Then the job run shows check "REC-08" failed with MSG-P1-019

  Scenario: AC4 A repeat run for the same date writes no duplicates
    Given JOB-13 completed for 2026-11-30 with 380 rows
    When JOB-13 is rerun for 2026-11-30
    Then the partition "business_date=2026-11-30" still holds 380 rows
    Then the cumulative count stays 12,480

  Scenario: AC5 The decision log interface is unavailable
    Given DecisionLogExport returns an error for every call
    When JOB-13 runs for 2026-11-30
    Then the job run ends with status "FAILED" and MSG-GEN-006 for system "Decision log"
    Then the watermark and the previous partitions are unchanged

  Scenario: AC6 A day with no new decisions
    Given no entry was written after "77be...41d0"
    When JOB-13 runs for 2026-11-30
    Then the partition holds 0 rows and the manifest shows cumulative count 12,100
    Then check "REC-08" passes

  Scenario: AC7 Two runs at the same time
    Given JOB-13 is running for 2026-11-30
    When a platform administrator posts a rerun of JOB-13
    Then the system refuses the rerun with status 409 and MSG-P2-006
    Then one run continues

  Scenario: AC8 A partition exactly at its retention age is kept
    Given a lake partition for business date 2024-12-01
    When the retention step runs on 2026-12-01
    Then the partition "business_date=2024-12-01" stays in the copy
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The copy matches the live log on count and last hash with zero tolerance, or it is not published | REC-08; DL25 |
| BR2 | The copy reads the decision log only through the P7 published interface | ADR-002; DT08 |
| BR3 | Analysis reads the lake copy, not the live log | ADR-009 |
| BR4 | A lake partition older than the retention rule for DP12 LAKE_COPY moves to the archive tier | retention_rule (RWB-E1-017); DL26 |
| BR5 | The retention period is a data row with a version, never a code value | Principle 1; DT02 |
| BR6 | A failed copy is rerun the next night; the previous copy stays in use | JOB-13, batch.txt |

## 9. State transitions

None. This story does not change a case status. It changes the JOB-13 run status (Running, Complete, Failed) on the job run record, the lake partition state (Written, Complete, Archived) and the watermark.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-DATALOAD, data load | Runs JOB-13, reads through DecisionLogExport, writes the lake files and the watermark |
| SY-DECLOG, decision log writer | Owns the live log; not called for writes in this story |
| RW-PLATADM, platform administrator | Reruns JOB-13 (Platform administration U) |
| RW-DATASTEW, data steward | Reads the job result and the break (Platform administration R) |
| RW-COE, RW-AUDIT, RW-COMPLY | Read the job monitor (Platform administration R); read the lake copy in Power BI |
| RW-BIANAL, reporting and BI analyst | Reads the lake copy for reporting |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 | decision_log_entry | id | Read |
| DF-DEC-002 | decision_log_entry | case_id | Read |
| DF-DEC-003 | decision_log_entry | decision_code | Read |
| DF-DEC-004 | decision_log_entry | rule_id | Read |
| DF-DEC-005 | decision_log_entry | rule_version | Read |
| DF-DEC-006 | decision_log_entry | model_version | Read |
| DF-DEC-007 | decision_log_entry | agent_version | Read |
| DF-DEC-008 | decision_log_entry | inputs_ref | Read |
| DF-DEC-009 | decision_log_entry | recommendation | Read |
| DF-DEC-010 | decision_log_entry | approver_user_id | Read |
| DF-DEC-011 | decision_log_entry | approval_level | Read |
| DF-DEC-012 | decision_log_entry | final_call | Read |
| DF-DEC-013 | decision_log_entry | override_reason | Read |
| DF-DEC-014 | decision_log_entry | actions | Read |
| DF-DEC-015 | decision_log_entry | outcome | Read |
| DF-DEC-016 | decision_log_entry | decided_at | Read |
| DF-DEC-017 | decision_log_entry | prev_hash | Read |
| DF-DEC-018 | decision_log_entry | entry_hash | Read |
| DF-OPS-131 | lake_copy_watermark | copy_name | Write |
| DF-OPS-132 | lake_copy_watermark | last_entry_hash | Write |
| DF-OPS-133 | lake_copy_watermark | last_decided_at | Write |
| DF-OPS-134 | lake_copy_watermark | rows_copied_total | Write |
| DF-OPS-135 | lake_copy_watermark | business_date | Write |
| DF-REF-117 | retention_rule | product_code | Read |
| DF-REF-119 | retention_rule | record_class | Read |
| DF-REF-120 | retention_rule | retention_months | Read |
| DF-REF-123 | retention_rule | rule_version | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Job**

| Item | Value |
|---|---|
| Trigger | Quartz cron `0 0 1 * * ?`, Asia/Bangkok |
| Job name | JOB-13 Decision log copy |
| Schedule | Nightly 01:00; before JOB-15 at 01:30 and JOB-14 at 02:00 |
| Input | Decision log entries after the watermark hash, up to the head at job start, through DecisionLogExport |
| Output | Parquet files and `_manifest.json` under `decision-log/business_date=YYYY-MM-DD/` in the INT-19 intake container; the watermark row; checks on the job run (rows, REC-08 result, partitions archived, rule version) |
| Events published | None. JOB-13 publishes no event in events.txt |
| Idempotency key | Business date. A rerun for a date rewrites the same partition from the same chain range |
| Restart behavior | A failed run leaves the watermark unchanged; the next run or a manual rerun starts from the watermark. Quartz `@DisallowConcurrentExecution` |

**Published interface (P7 to P1)**

```java
package recovery.decisionlog.api;

public interface DecisionLogExport {
    /** Live count and last entry hash at the moment of the call. */
    ChainHead head();

    /** Entries after the given hash in chain order, at most limit entries. Genesis hash is 64 zeros. */
    List<DecisionLogEntryView> entriesAfter(String afterEntryHash, int limit);
}

public record ChainHead(long count, String lastEntryHash, OffsetDateTime lastDecidedAt) {}
```

DecisionLogEntryView carries the 18 fields of DecisionLogEntry in api.yaml, with the same names.

**Endpoints used**

| Method and path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|
| GET /api/recovery/v1/admin/jobs | Query: type=JOB-13, status, from, to | Job[]: id, type, businessDate, status, startedAt, endedAt, checks | 401 no session (MSG-P4-001); 403 role lacks the right (MSG-P4-002); 503 store down | Platform administration, R | Not applicable |
| POST /api/recovery/v1/admin/jobs/{jobId}/rerun | Path: jobId; header Idempotency-Key | Job | 401; 403; 404 unknown job (MSG-P4-003); 409 job running (MSG-P2-006); 503 | Platform administration, U | Idempotency-Key header; a repeat key returns the first result |

## 13. Solution plan

- Package: folder `recovery/dataengine/lake`, Java package `recovery.dataengine.lake`.

| Component | Type | Responsibility |
|---|---|---|
| DecisionLogLakeCopyJob | Job | Quartz job for JOB-13; one run per business date; no concurrent run |
| DecisionLogLakeCopyService | Service | Reads the watermark, fixes the cut-off, pages entries through DecisionLogExport |
| LakeFileWriter | Service | Writes Parquet files and the manifest to the intake container |
| LakeCopyReconciler | Service | Reads the manifest back and checks REC-08; records the result on the job run |
| LakeRetentionService | Service | Applies the DP12 LAKE_COPY retention rule to lake partitions |
| LakeCopyWatermarkRepository | Repository | Reads and writes lake_copy_watermark |
| LakeCopyWatermark | Entity | One row per copy name |
| DecisionLogExport | Published interface | P7 interface used to read the log; built in P7 if not present |

- Database: table lake_copy_watermark (new, Flyway migration in this story): copy_name varchar(40) primary key, last_entry_hash char(64) not null, last_decided_at timestamptz, rows_copied_total bigint not null, business_date date not null, plus the standard columns. No read of decision_log_entry in P1 code. Reads retention_rule (RWB-E1-017).
- Configuration and reference data: properties `rwb.dataengine.lake.container`, `rwb.dataengine.lake.path-prefix=decision-log`, `rwb.dataengine.lake.page-size=5000`, `rwb.dataengine.lake.rows-per-file=50000` (platform administrator, per environment); retention rule row DP12 LAKE_COPY loaded by the reference data administrator and approved by Compliance (RWB-E1-017).
- Build steps:
  1. Flyway migration for lake_copy_watermark; seed row copy_name `DECISION_LOG`, last_entry_hash 64 zeros, rows_copied_total 0.
  2. DecisionLogExport in P7 with head() and entriesAfter(); unit tests on chain order.
  3. DecisionLogLakeCopyService paging from the watermark to the cut-off; test with 12,480 synthetic entries.
  4. LakeFileWriter with Parquet output and manifest; test against an Azurite or local file system container.
  5. LakeCopyReconciler with REC-08 checks and MSG-P1-019 on a mismatch; watermark moves only on a match.
  6. LakeRetentionService reading the rule row; partitions older than retention_months move to the archive tier.
  7. DecisionLogLakeCopyJob on Quartz with `@DisallowConcurrentExecution`, run record and checks through the RWB-E1-056 job monitoring.
  8. Integration tests for AC1 to AC8 and the access test.
- Feature flag: `rwb.dataengine.lake-copy`.
- Done when: the tests in section 16 pass, JOB-13 shows in GET /admin/jobs with its checks, and the run book from RWB-E1-056 covers the rerun.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-019 | Lake copy does not match the live log (new, see additions) | The decision log copy for {date} does not match the live log: {check}. The copy was not published. |
| MSG-GEN-006 | DecisionLogExport or the lake is unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P2-006 | Rerun while JOB-13 is running (new, see additions) | {job} is already running. Wait for it to finish before you rerun it. |
| MSG-P4-002 | Role without Platform administration R or U | You cannot {action} here. Your role does not include it. |

Thai text for each message follows decision DL10.

## 15. Screens and states

No screen in this story. The platform administrator and the data steward see the JOB-13 run, its status and its checks through GET /admin/jobs; SCR-44 Interface and job monitor shows them from Epic 2 (states Running, Failed, Complete). The data steward receives the operations alert on a failed run.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-014-01 | AC1, BR1, BR2 | System | 12,480 synthetic entries; watermark at 12,100 |
| TC-E1-014-02 | AC2, BR4, BR5 | System | Partitions 2024-11-29 and 2024-11-30; rule 24 months |
| TC-E1-014-03 | AC3, BR1 | System | Lake write stopped after 379 of 380 rows |
| TC-E1-014-04 | AC4 | System | JOB-13 run twice for 2026-11-30 |
| TC-E1-014-05 | AC5, BR6 | System | DecisionLogExport stub returning errors |
| TC-E1-014-06 | AC6 | System | No entry after the watermark |
| TC-E1-014-07 | AC7 | System | Rerun posted during a running JOB-13 |
| TC-E1-014-08 | AC8, BR4 | System | Partition 2024-12-01 on run date 2026-12-01 |
| TC-E1-014-09 | Access | Access | RW-CASEOWN calls GET /admin/jobs; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the retention period, page size, file size and lake path are data rows or properties.
- No personal data in logs, tests or prompts. Test entries use synthetic case IDs and synthetic hashes; inputs_ref holds references only.
- No read of another module's tables: decision_log_entry is read only through DecisionLogExport.
- The job never writes, updates or deletes a live decision log entry.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-009 | Decision log copied to the lake daily with row counts matched | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-20, FEAT-DRI-06 | 17 Run the decision center | REC-08 | TC-E1-014-01, TC-E1-014-03, TC-E1-014-04, TC-E1-014-05, TC-E1-014-06, TC-E1-014-07 |
| REQ-RDF-013 | Retention and archive rule by record class | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-20 | 15 Manage performance, data and AI | DL26 | TC-E1-014-02, TC-E1-014-08 |

## 19. Out of scope

- Retention of the live decision log (NFR-030, DL26) and the hash chain check (JOB-14, RWB-TE-008).
- Operations reports built on the copy (FEAT-RPT-04, Epic 2).
- Logging each read of the lake copy to the access log (REQ-ACA-006, RWB-E1-039).
- The retention rule table and the data store retention job (RWB-E1-017).
