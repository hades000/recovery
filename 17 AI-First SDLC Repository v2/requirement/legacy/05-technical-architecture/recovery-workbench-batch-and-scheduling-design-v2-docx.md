<!-- source: 05 Technical architecture/Recovery Workbench Batch and Scheduling Design v2.docx -->
<!-- converted: 2026-11-16 from DOCX -->

> **Source:** `05 Technical architecture/Recovery Workbench Batch and Scheduling Design v2.docx`  
> **Converted from:** DOCX

Recovery Workbench

Batch and scheduling design

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench batch and scheduling design |
| Version | 1 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Structure | arc42 runtime view |

# 1. How scheduled work runs

- Quartz in the ACE service holds the schedules; one run per job across service instances.

- Spring Batch runs loads and outbound files in chunks with restart from the last chunk.

- Every job writes its run to the job monitor with business date, rows, checks and result.

- Schedules and thresholds are configuration; changing them needs no release.

# 2. The jobs

| ID | Job | When | If it fails or runs late | Owner |
|---|---|---|---|---|
| JOB-01 | COLLINS load check and intake | Daily 05:00, retried hourly to 09:00 | Previous load kept; products marked stale; data steward alerted | Data steward |
| JOB-02 | Case creation | Daily after JOB-01 | No cases from stale data; runs after the next good load | Data steward |
| JOB-03 | Morning allocation | Daily after JOB-02, by 07:00 | Cases stay New; rerun from the monitor | Team managers |
| JOB-04 | Daily reconciliation | Daily after JOB-02 | Breaks listed for the data steward | Data steward |
| JOB-05 | Timer check | Every 5 minutes | Next run picks up missed timers | Platform administrator |
| JOB-06 | Daily rebalancing | Daily 06:30 | Rerun; managers rebalance by hand | Team managers |
| JOB-07 | Payment matching | Daily after JOB-01 | Exception list | Credit Administration |
| JOB-08 | Booking confirmation | Daily after JOB-01 | Task to the officer for missing bookings | Credit Administration |
| JOB-09 | File loads | Weekly Monday 04:00; monthly 2nd working day | Previous load kept; alert | Data steward |
| JOB-10 | WIN outbound notices | Daily 16:00 | Retry; exception queue | Platform administrator |
| JOB-11 | Outbox sender | Every minute | Exception queue after the retry limit | Platform administrator |
| JOB-12 | Document intake | Every 15 minutes in business hours | Next run; alert after two failures | Platform administrator |
| JOB-13 | Decision log copy | Nightly 01:00 | Rerun the next night | Data steward |
| JOB-14 | Hash chain check | Nightly 02:00 | Break reported to Compliance | Compliance |
| JOB-15 | Reporting extract | Nightly 01:30 | Reports show the previous day | Reporting and BI analyst |
| JOB-16 | Write-off scan | Monthly, 3rd working day | Hold until the load or version arrives (R-WO-02, R-WO-03) | Write-off team |
| JOB-17 | Retention job | Monthly, 1st Sunday | Next month | Compliance |
| JOB-18 | Access review list | Every six months | Rerun | Security administrator |
| JOB-19 | Re-appraisal cycle | Monthly | Next month | Head of NPA |

# 3. Dependencies

The morning chain depends on the COLLINS load: JOB-01, then case creation, reconciliation, payment matching and booking confirmation, then allocation by 07:00. If the load is late, the chain waits; at 09:00 the day runs on the previous load and the data products show their date.

# 4. Late and failed runs

- A missed run is processed when the service starts.

- A failed job alerts its owner within 15 minutes.

- A rerun from the job monitor is logged with who ran it.

- No job processes the same business date twice; repeats are ignored.

# 5. Calendar

Working days come from the bank holiday calendar held as reference data. Monthly jobs on a holiday run the next working day.
