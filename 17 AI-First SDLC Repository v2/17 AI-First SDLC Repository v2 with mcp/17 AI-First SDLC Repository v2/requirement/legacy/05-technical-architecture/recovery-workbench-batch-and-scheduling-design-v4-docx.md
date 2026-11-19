<!-- source: 05 Technical architecture/Recovery Workbench Batch and Scheduling Design v4.docx -->
<!-- converted: 2026-11-16 from DOCX -->

> **Source:** `05 Technical architecture/Recovery Workbench Batch and Scheduling Design v4.docx`  
> **Converted from:** DOCX

Recovery Workbench

Batch and scheduling design

SCB Collections and Recovery. Henka Group, 16 November 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench batch and scheduling design |
| Version | 4 |
| Date | 16 November 2026 |
| Change | v4, 16 November 2026, D-RCV-36: Quartz and Spring Batch stay for every Epic 1 and Epic 2 job, JOB-05 runs behind the TimerScheduler port, RulePackageEffectiveDateJob, StuckWorkflowScanner and the daily smoke trigger are added, and case waits move to Temporal only from Epic 3 (ADR-011) |
| Prepared by | Henka Group |
| Structure | arc42 runtime view |

# 1. How scheduled work runs

Quartz and Spring Batch stay for every Epic 1 and Epic 2 scheduled job: JOB-03 allocation, JOB-04 reconciliation, JOB-05 timer check, JOB-06 rebalance, JOB-07, JOB-08 and the rest. Temporal Schedules are not used in Epics 1 and 2. Temporal is present for the daily smoke workflow and for visibility queries, and case workflows with durable timers start in Epic 3 (ADR-011).

- Quartz in the ACE service holds the schedules in ACE's existing qrtz_* tables, shared with ACE; one run per job across service instances. The Workbench creates no new qrtz_ table.

- Spring Batch runs the Workbench jobs and the outbound files in chunks with restart from the last chunk. It runs no inbound load. Its step records go to ACE's existing Spring Batch batch_* tables, shared with ACE; no new batch_ table is created (ACE Data Tier Map rows 23 and 24).

- Every job writes its run to the job monitor with business date, rows, checks and result.

- Schedules and thresholds are configuration; changing them needs no release.

- The data jobs start on the ACE batch-complete record, read through recovery.v_ace_batch_status (EV-26 AceDataReady). No job waits on a file, and no data job starts on a fixed clock time.

- Timer scheduling goes through the TimerScheduler port. JOB-05 is its Quartz implementation, and every caller uses the port (section 3).

# 2. The jobs

22 jobs are listed. JOB-01 and JOB-09 are retired under D-RCV-35 and keep their rows; the other 20 run on Quartz and Spring Batch. JOB-20 to JOB-22 are added under D-RCV-36. The data jobs start on the ACE batch-complete record, not on a load.

| ID | Job | When | If it fails or runs late | Owner |
|---|---|---|---|---|
| JOB-01 | COLLINS load check and intake | Retired - D-RCV-35 | Not run; ACE ingestion replaces it and reports its own status through v_ace_batch_status | ACE team |
| JOB-02 | Case creation | On the ACE batch-complete record for ALS | No cases from a stale business date; runs on the next complete ACE batch | Data steward |
| JOB-03 | Morning allocation | Daily after JOB-02, by 07:00 | Cases stay New; rerun from the monitor | Team managers |
| JOB-04 | Daily reconciliation | On the ACE batch-complete record, after JOB-02 | Breaks listed for the data steward | Data steward |
| JOB-05 | Timer check | Every 5 minutes | Next run picks up missed timers | Platform administrator |
| JOB-06 | Daily rebalancing | Daily 06:30 | Rerun; managers rebalance by hand | Team managers |
| JOB-07 | Payment matching | On the ACE batch-complete record for ALS, after JOB-02 | Exception list | Credit Administration |
| JOB-08 | Booking confirmation | On the ACE batch-complete record for ALS, after JOB-02 | Task to the officer for missing bookings | Credit Administration |
| JOB-09 | File loads | Retired - D-RCV-35 | Not run; ACE ingestion replaces it and reports its own status through v_ace_batch_status | ACE team |
| JOB-10 | WIN outbound notices | Daily 16:00 | Retry; exception queue | Platform administrator |
| JOB-11 | Outbox sender | Every minute | Exception queue after the retry limit | Platform administrator |
| JOB-12 | Document intake | Every 15 minutes in business hours | Next run; alert after two failures | Platform administrator |
| JOB-13 | Decision log copy | Nightly 01:00 | Rerun the next night | Data steward |
| JOB-14 | Hash chain check | Nightly 02:00 | Break reported to Compliance | Compliance |
| JOB-15 | Reporting extract | Nightly 01:30 | Reports show the previous day | Reporting and BI analyst |
| JOB-16 | Write-off scan | Monthly, 3rd working day, on the ACE batch-complete record for ALS | Hold until the ACE batch or the version arrives (R-WO-02, R-WO-03) | Write-off team |
| JOB-17 | Retention job | Monthly, 1st Sunday | Next month | Compliance |
| JOB-18 | Access review list | Every six months | Rerun | Security administrator |
| JOB-19 | Re-appraisal cycle | Monthly | Next month | Head of NPA |
| JOB-20 | RulePackageEffectiveDateJob | Daily 00:01 | Approved versions due today stay APPROVED; the next run sets them IN_FORCE | Center of excellence analyst |
| JOB-21 | StuckWorkflowScanner | Every 5 minutes | Stuck panel marked stale; incident raised; no zero is published | Platform administrator |
| JOB-22 | PlatformSmokeWorkflow trigger (SmokeScheduleJob) | Daily 06:00 | No smoke result for the day; alert to the platform administrator | Platform administrator |

# 3. TimerScheduler

JOB-05 Timer check is the Quartz implementation of the TimerScheduler port. The port has four methods: schedule(TimerSpec), cancel(UUID timerId), pause(UUID timerId) and resume(UUID timerId). The job finds due and warning timers and raises warnings, escalations and timer events as it does today.

All callers go through TimerScheduler, whether they are a job, a case action or an API call. No caller writes the timer table directly and no caller knows that Quartz is underneath. The Epic 3 case workflow gets the same four methods with Temporal durable timers behind them, and no caller changes.

No new Quartz job may hold a case wait. A case wait is a durable timer on the case workflow; it moves to Temporal in Epic 3. JOB-05 keeps the timers that are still rows in the timer table.

# 4. Temporal in Epics 1 and 2

Temporal is used in Epics 1 and 2 for the platform smoke workflow and for visibility. SmokeScheduleJob is a Quartz job, daily at 06:00 that starts PlatformSmokeWorkflow as platform-smoke-{yyyymmdd} on task queue rwb-platform (RWB-E1-071). StuckWorkflowScanner is a Quartz job every 5 minutes that runs Temporal visibility queries to find workflows with no progress (RWB-E2-037). Neither job uses a Temporal Schedule.

RulePackageEffectiveDateJob is a Quartz job, daily at 00:01. It sets each APPROVED rule package version whose valid-from date is today to IN_FORCE, and moves the previous IN_FORCE version of the same package to SUPERSEDED in the same transaction. A run with no version due changes nothing, and a second run on the same day is a no-op.

Roadmap: from Epic 3 the case lifecycle runs as one Temporal workflow per case on task queue rwb-case. Case waits and durable timers move to Temporal, and JOB-05 keeps serving any timer that has not moved. The scheduled jobs stay on Quartz, including JOB-03 allocation, JOB-04 reconciliation, JOB-06 rebalance, JOB-07, JOB-08 and the rest. A future move of a scheduled job to a Temporal Schedule needs a new decision. ADR-011 records the hybrid design.

Timers do not all move to Temporal now. Only case waits move, and only from Epic 3; nothing in Epics 1 and 2 depends on Temporal being available.

# 5. Dependencies

The data jobs start from the ACE batch record, not from a fixed time. ACE ingests each source and writes a completion record; the Workbench reads recovery.v_ace_batch_status and starts the chain when the record for the business date shows COMPLETED: JOB-02 case creation, then JOB-04 reconciliation, JOB-07 payment matching and JOB-08 booking confirmation, then JOB-03 allocation by 07:00. JOB-16 write-off scan runs on the same record on its scheduled day. If a source is not complete at the Workbench cut-off, the data products show their last complete business date, AceDataLate goes to the data steward, and the chain starts when the record arrives. No job reads a file, and no job retries a load.

# 6. Late and failed runs

- A missed run is processed when the service starts.

- A failed job alerts its owner within 15 minutes.

- A rerun from the job monitor is logged with who ran it.

- No job processes the same business date twice; repeats are ignored.

- An ACE batch that is late raises AceDataLate; the data jobs start when its record arrives and use the business date it carries.

- A failed StuckWorkflowScanner marks the stuck panel stale and raises an incident; it never publishes a zero.

- A failed RulePackageEffectiveDateJob leaves the approved version APPROVED; the next run with the same valid-from date sets it IN_FORCE.

# 7. Calendar

Working days come from the bank holiday calendar held as reference data. Monthly jobs on a holiday run the next working day.
