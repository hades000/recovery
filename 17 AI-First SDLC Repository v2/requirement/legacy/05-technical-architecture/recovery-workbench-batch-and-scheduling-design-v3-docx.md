<!-- source: 05 Technical architecture/Recovery Workbench Batch and Scheduling Design v3.docx -->
<!-- converted: 2026-11-16 from DOCX -->

> **Source:** `05 Technical architecture/Recovery Workbench Batch and Scheduling Design v3.docx`  
> **Converted from:** DOCX

Recovery Workbench

Batch and scheduling design

SCB Collections and Recovery. Henka Group, 15 November 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench batch and scheduling design |
| Version | 3 |
| Date | 15 November 2026 |
| Prepared by | Henka Group |
| Structure | arc42 runtime view |

# 1. How scheduled work runs

- Quartz in the ACE service holds the schedules in ACE's existing qrtz_* tables, shared with ACE; one run per job across service instances. The Workbench creates no new qrtz_ table.

- Spring Batch runs the Workbench jobs and the outbound files in chunks with restart from the last chunk. It runs no inbound load. Its step records go to ACE's existing Spring Batch batch_* tables, shared with ACE; no new batch_ table is created (ACE Data Tier Map rows 23 and 24).

- Every job writes its run to the job monitor with business date, rows, checks and result.

- Schedules and thresholds are configuration; changing them needs no release.

- The data jobs start on the ACE batch-complete record, read through recovery.v_ace_batch_status (EV-26 AceDataReady). No job waits on a file, and no data job starts on a fixed clock time.

# 2. The jobs

19 jobs are listed. JOB-01 and JOB-09 are retired under D-RCV-35 and keep their rows; the other 17 run on Quartz and Spring Batch. The data jobs start on the ACE batch-complete record, not on a load.

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

# 3. Dependencies

The data jobs start from the ACE batch record, not from a fixed time. ACE ingests each source and writes a completion record; the Workbench reads recovery.v_ace_batch_status and starts the chain when the record for the business date shows COMPLETED: JOB-02 case creation, then JOB-04 reconciliation, JOB-07 payment matching and JOB-08 booking confirmation, then JOB-03 allocation by 07:00. JOB-16 write-off scan runs on the same record on its scheduled day. If a source is not complete at the Workbench cut-off, the data products show their last complete business date, AceDataLate goes to the data steward, and the chain starts when the record arrives. No job reads a file, and no job retries a load.

# 4. Late and failed runs

- A missed run is processed when the service starts.

- A failed job alerts its owner within 15 minutes.

- A rerun from the job monitor is logged with who ran it.

- No job processes the same business date twice; repeats are ignored.

- An ACE batch that is late raises AceDataLate; the data jobs start when its record arrives and use the business date it carries.

# 5. Calendar

Working days come from the bank holiday calendar held as reference data. Monthly jobs on a holiday run the next working day.
