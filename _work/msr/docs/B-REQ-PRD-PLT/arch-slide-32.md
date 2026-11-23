
Where the bank's Airflow fits: at Recovery's edges, not inside it

For discussion: the bank is moving from Control-M to Airflow; this is the use we recommend

AIRFLOW DOES (BANK SCHEDULER)

RECOVERY ENTRY POINT

1

Overnight chain (main use)
ACE ingestion DAG ends with 'business date X ready'; a sensor waits for DailyCaseRun; SLA alerts 05:30 and 07:00

P1 rwb-source-data
publishes AceDataReady

2

Fixed-window file transfers
WIN letters 16:00 (INT-14), debt-buyer encrypted files (INT-25) over MFT; Recovery still builds the files

P2 rwb-integration
file + manifest ready

3

Report and regulatory extracts
JOB-15 at 01:30; rerun any business date; backfills on demand

P9 rwb-reporting
POST /reports/{id}/run

4

One-off bulk work
Cutover loads (tracker inventory), backfills, data-quality and GL reconciliation

P1 · P8 APIs
never their schemas

Interface contract: Airflow → Recovery
POST /v1/business-days/{date}/ready → 202, idempotent on the date  ·  GET /v1/business-days/{date}/status → RUNNING | DONE | LATE
Service APIs only, mTLS with client credentials; Airflow never reads or writes rwb_* schemas

Stays in Temporal and Kafka
Per-case workflows and approvals
Multi-day timers, sagas, deadlines
Reactions to business events
Anything a user waits for
Outbox every minute; timer and stuck checks every 5 min

To agree (for discussion)
Who owns the DAGs: bank platform team or Recovery
When Control-M moves to Airflow
Where Airflow runs: bank platform or ACE cluster
Fallback: poll ACE's batch record while ACE is on Control-M
New ADR replacing the BRD's ADF / Control-M

Airflow says when the bank's data and files are ready; Temporal decides what happens to each case.

32

Notes: Context: the bank's batch scheduling is moving from Control-M to Airflow. The BRD still names ADF and Control-M jobs, and the reference proposal (recovery-architecture.pptx) already puts Airflow on scheduled work and Temporal on multi-step work. This slide is a recommendation to discuss, not a decision.

1 Overnight chain (main use). Airflow runs the ACE ingestion DAG. Its last task calls rwb-source-data: POST /v1/business-days/{date}/ready, idempotent on the business date, answered 202. rwb-source-data checks freshness against the 30 views and publishes AceDataReady, which starts DailyCaseRun in rwb-case and the matching and reconciliation workflows. An Airflow sensor polls GET /v1/business-days/{date}/status until DONE, and Airflow raises SLA alerts at 05:30 and 07:00. This replaces rwb-source-data polling ACE's batch record; the poll stays as the fallback if ACE ingestion is still on Control-M at go-live.

2 Fixed-window file transfers: WIN letters at 16:00 (INT-14) and debt-buyer encrypted files (INT-25) over MFT or SFTP. rwb-integration still builds the files and manifests; Airflow owns the window, the transfer and the retry.

3 Report and regulatory extracts: JOB-15 at 01:30 through POST /v1/reports/{id}/run on rwb-reporting, with a rerun for any business date and backfills.

4 One-off bulk work: cutover loads such as the tracker inventory, backfills, data-quality and GL reconciliation runs, all through service APIs.

Not Airflow: per-case workflows, approvals, multi-day timers, sagas, reactions to business events, anything a user waits for, and high-frequency jobs (outbox every minute, timer and stuck-workflow checks every 5 minutes). These stay in Temporal and Kafka. Airflow never reads or writes rwb_* schemas.

To agree: who owns the DAGs (bank platform team or Recovery), when Control-M moves to Airflow, where Airflow runs, and a new ADR replacing the BRD's ADF/Control-M wording.

