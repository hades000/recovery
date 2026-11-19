<!-- source: 05 Technical architecture/Recovery Workbench Batch and Scheduling Design v2.xlsx -->
<!-- converted: 2026-11-04 from XLSX -->

> **Source:** `05 Technical architecture/Recovery Workbench Batch and Scheduling Design v2.xlsx`  
> **Converted from:** XLSX

## Jobs

| Every scheduled job |  |  |  |  |  |  |
|---|---|---|---|---|---|---|
| 19 jobs on Quartz and Spring Batch in the ACE service. Times are Asia/Bangkok. |  |  |  |  |  |  |
| ID | Job | What it does | When | Depends on | If it fails or runs late | Owner |
| JOB-01 | COLLINS load check and intake | Reads the COLLINS daily load into the recovery tables; runs the load checks | Daily 05:00, retried hourly to 09:00 | COLLINS end of day | Previous load kept; products marked stale; data steward alerted | Data steward |
| JOB-02 | Case creation | Creates cases for accounts that reached 90 days past due; attaches history | Daily after JOB-01 | JOB-01 passed | No cases from stale data; runs after the next good load | Data steward |
| JOB-03 | Morning allocation | Places new cases in queues and gives owners by rule | Daily after JOB-02, by 07:00 | JOB-02 | Cases stay New; rerun from the monitor | Team managers |
| JOB-04 | Daily reconciliation | Accounts at 90 days past due against open cases; balances against the core bank | Daily after JOB-02 | JOB-01 | Breaks listed for the data steward | Data steward |
| JOB-05 | Timer check | Finds due and warning timers; raises warnings, escalations and timer events | Every 5 minutes | None | Next run picks up missed timers | Platform administrator |
| JOB-06 | Daily rebalancing | Moves cases from owners above the cap or absent | Daily 06:30 | JOB-03 | Rerun; managers rebalance by hand | Team managers |
| JOB-07 | Payment matching | Matches payments to plans and settlements; raises missed payments | Daily after JOB-01 | JOB-01 | Exception list | Credit Administration |
| JOB-08 | Booking confirmation | Matches approved treatments to bookings in the ALS load | Daily after JOB-01 | JOB-01 | Task to the officer for missing bookings | Credit Administration |
| JOB-09 | File loads | CCMS, SVAF, RPS and WIN weekly; AMIS and GL monthly | Weekly Monday 04:00; monthly 2nd working day | File arrival | Previous load kept; alert | Data steward |
| JOB-10 | WIN outbound notices | Writes the daily notice file for registered mail | Daily 16:00 | Approved notices | Retry; exception queue | Platform administrator |
| JOB-11 | Outbox sender | Sends outbound work with retry | Every minute | None | Exception queue after the retry limit | Platform administrator |
| JOB-12 | Document intake | Picks up scanner folders, SFTP and mailboxes into OCR | Every 15 minutes in business hours | None | Next run; alert after two failures | Platform administrator |
| JOB-13 | Decision log copy | Copies the decision log to the data lake | Nightly 01:00 | None | Rerun the next night | Data steward |
| JOB-14 | Hash chain check | Checks the decision log chain | Nightly 02:00 | JOB-13 | Break reported to Compliance | Compliance |
| JOB-15 | Reporting extract | Case, queue, decision and outcome data to the data lake for Power BI | Nightly 01:30 | None | Reports show the previous day | Reporting and BI analyst |
| JOB-16 | Write-off scan | Tests open cases against write-off eligibility | Monthly, 3rd working day | ALS load; tax criteria version | Hold until the load or version arrives (R-WO-02, R-WO-03) | Write-off team |
| JOB-17 | Retention job | Lists records past retention for review | Monthly, 1st Sunday | None | Next month | Compliance |
| JOB-18 | Access review list | Produces role holder lists for recertification | Every six months | None | Rerun | Security administrator |
| JOB-19 | Re-appraisal cycle | Raises re-appraisal orders for assets due | Monthly | Asset holding age | Next month | Head of NPA |

## Daily timeline

| The working day |  |
|---|---|
| The order the daily jobs run in. |  |
| Time | Jobs |
| 05:00 | JOB-01 COLLINS load check |
| after JOB-01 | JOB-02 case creation; JOB-04 reconciliation; JOB-07 payment matching; JOB-08 booking confirmation |
| 06:30 | JOB-06 rebalancing |
| by 07:00 | JOB-03 morning allocation complete |
| 16:00 | JOB-10 WIN notices |
| 01:00 to 02:00 | JOB-13, JOB-15, JOB-14 |
