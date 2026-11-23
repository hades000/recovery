<!-- source: 05 Technical architecture/Recovery Workbench Batch and Scheduling Design v4.xlsx -->
<!-- converted: 2026-11-16 from XLSX -->

> **Source:** `05 Technical architecture/Recovery Workbench Batch and Scheduling Design v4.xlsx`  
> **Converted from:** XLSX

## Jobs

| Every scheduled job |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|
| 22 jobs are listed; JOB-01 and JOB-09 are retired under D-RCV-35 and the other 20 run on Quartz and Spring Batch in the ACE service, using ACE's existing qrtz_* and batch_* tables shared with ACE (no new qrtz_ or batch_ table). Times are Asia/Bangkok. The data jobs start on the ACE batch-complete record; JOB-20 to JOB-22 are added under D-RCV-36. The TimerScheduler column marks the job that implements the port. |  |  |  |  |  |  |  |
| Version 4, 16 November 2026. D-RCV-36. |  |  |  |  |  |  |  |
| ID | Job | What it does | When | Depends on | If it fails or runs late | Owner | TimerScheduler |
| JOB-01 | COLLINS load check and intake | ACE ingests the COLLINS feed; the Workbench loads nothing and reads the result through v_ace_account and v_ace_payment | Retired - D-RCV-35 | None | Not run; ACE ingestion reports its own status through v_ace_batch_status | ACE team | - |
| JOB-02 | Case creation | Creates cases for accounts that reached 90 days past due; attaches history | On the ACE batch-complete record for ALS | ACE batch (v_ace_batch_status) | No cases from a stale business date; runs on the next complete ACE batch | Data steward | - |
| JOB-03 | Morning allocation | Places new cases in queues and gives owners by rule | Daily after JOB-02, by 07:00 | JOB-02 | Cases stay New; rerun from the monitor | Team managers | - |
| JOB-04 | Daily reconciliation | Accounts at 90 days past due against open cases; balances against the core bank | On the ACE batch-complete record, after JOB-02 | JOB-02; ACE batch (v_ace_batch_status) | Breaks listed for the data steward | Data steward | - |
| JOB-05 | Timer check | Finds due and warning timers; raises warnings, escalations and timer events. Implements TimerScheduler (schedule, cancel, pause, resume) for every caller | Every 5 minutes | None | Next run picks up missed timers | Platform administrator | Yes: schedule, cancel, pause, resume |
| JOB-06 | Daily rebalancing | Moves cases from owners above the cap or absent | Daily 06:30 | JOB-03 | Rerun; managers rebalance by hand | Team managers | - |
| JOB-07 | Payment matching | Matches payments to plans and settlements; raises missed payments | On the ACE batch-complete record for ALS, after JOB-02 | JOB-02; ACE batch (v_ace_batch_status) | Exception list | Credit Administration | - |
| JOB-08 | Booking confirmation | Matches approved treatments to bookings in the ACE account view | On the ACE batch-complete record for ALS, after JOB-02 | JOB-02; ACE batch (v_ace_batch_status) | Task to the officer for missing bookings | Credit Administration | - |
| JOB-09 | File loads | ACE ingests the CCMS, SVAF, RPS, WIN, AMIS and GL files; the Workbench reads them through the v_ace_* views | Retired - D-RCV-35 | None | Not run; ACE ingestion reports its own status through v_ace_batch_status | ACE team | - |
| JOB-10 | WIN outbound notices | Writes the daily notice file for registered mail | Daily 16:00 | Approved notices | Retry; exception queue | Platform administrator | - |
| JOB-11 | Outbox sender | Sends outbound work with retry | Every minute | None | Exception queue after the retry limit | Platform administrator | - |
| JOB-12 | Document intake | Picks up scanner folders, SFTP and mailboxes into OCR | Every 15 minutes in business hours | None | Next run; alert after two failures | Platform administrator | - |
| JOB-13 | Decision log copy | Copies the decision log to the data lake | Nightly 01:00 | None | Rerun the next night | Data steward | - |
| JOB-14 | Hash chain check | Checks the decision log chain | Nightly 02:00 | JOB-13 | Break reported to Compliance | Compliance | - |
| JOB-15 | Reporting extract | Case, queue, decision and outcome data to the data lake for Power BI | Nightly 01:30 | None | Reports show the previous day | Reporting and BI analyst | - |
| JOB-16 | Write-off scan | Tests open cases against write-off eligibility | Monthly, 3rd working day, on the ACE batch-complete record for ALS | ACE batch (v_ace_batch_status); tax criteria version | Hold until the ACE batch or the version arrives (R-WO-02, R-WO-03) | Write-off team | - |
| JOB-17 | Retention job | Lists records past retention for review | Monthly, 1st Sunday | None | Next month | Compliance | - |
| JOB-18 | Access review list | Produces role holder lists for recertification | Every six months | None | Rerun | Security administrator | - |
| JOB-19 | Re-appraisal cycle | Raises re-appraisal orders for assets due | Monthly | Asset holding age | Next month | Head of NPA | - |
| JOB-20 | RulePackageEffectiveDateJob | Sets APPROVED rule package versions with today's valid-from date to IN_FORCE; moves the previous version to SUPERSEDED | Daily 00:01 | rule_package_version | Approved versions stay APPROVED; the next run sets them IN_FORCE | Center of excellence analyst | - |
| JOB-21 | StuckWorkflowScanner | Uses Temporal visibility queries to find RUNNING workflows with no progress for temporal.stuck.hours | Every 5 minutes | Temporal visibility (rwb-recovery) | Stuck panel marked stale; incident raised; no zero is published | Platform administrator | - |
| JOB-22 | PlatformSmokeWorkflow trigger (SmokeScheduleJob) | Starts PlatformSmokeWorkflow as platform-smoke-{yyyymmdd} on task queue rwb-platform through WorkflowGateway | Daily 06:00 | RWB-E1-071 worker | No smoke result for the day; alert to the platform administrator | Platform administrator | - |

## Daily timeline

| The working day |  |
|---|---|
| The order the daily jobs run in. The data jobs start when the ACE batch-complete record arrives. Times are Asia/Bangkok. |  |
| Time | Jobs |
| On the ACE batch-complete record for ALS | JOB-02 case creation, then JOB-04 reconciliation, JOB-07 payment matching and JOB-08 booking confirmation |
| 00:01 | JOB-20 rule package effective date |
| Every 5 minutes | JOB-21 stuck workflow scan |
| 06:00 | JOB-22 platform smoke trigger, platform-smoke-{yyyymmdd} on rwb-platform |
| 06:30 | JOB-06 rebalancing |
| by 07:00 | JOB-03 morning allocation complete |
| 16:00 | JOB-10 WIN notices |
| 01:00 to 02:00 | JOB-13, JOB-15, JOB-14 |
