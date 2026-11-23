
The overnight chain: everything ready before officers start at 07:00

Bank Airflow runs the cross-system chain; inside Recovery each job is a Temporal Schedule or an event

00:00

02:00

04:00

07:00

08:00

10:00

12:00

14:00

16:00

ACE ingestion
ACE · bank Airflow DAG

Rules, ledger, measures
rwb-decision · rwb-reporting

Create & allocate cases
rwb-case

Match payments
rwb-payment

Health check, rebalance
platform · rwb-case

Officers working

Customer letters
rwb-comms → rwb-integration

◆ Airflow: ACE ready (~04:30) → AceDataReady starts the run   ◆ AceDataLate alarm at 05:30   ◆ WIN letters file at 16:00

Temporal Schedules
in the service that owns the job

Started by events
AceDataReady triggers the morning run

Bank Airflow (to discuss)
says 'date ready'; SLA alerts 05:30, 07:00

Officers start at 07:00 with today's cases allocated; if ACE is late, the alarm goes off at 05:30.

31

Notes: ACE ingests the source systems into the ACE database overnight. The bank's Airflow (replacing Control-M; for discussion) runs the ACE ingestion DAG. Its last task calls rwb-source-data (POST /v1/business-days/{date}/ready, idempotent), which checks freshness and publishes AceDataReady; a sensor waits for DailyCaseRun and Airflow raises SLA alerts at 05:30 and 07:00. rwb-source-data still publishes AceDataLate at 05:30 with an alarm and a banner. Fallback if ACE ingestion is still on Control-M at go-live: rwb-source-data polls ACE's batch record, as today.

AceDataReady starts DailyCaseRun in rwb-case (case creation JOB-02, allocation JOB-03 by 07:00), payment matching and booking confirmation in rwb-payment (JOB-07, JOB-08), reconciliation in rwb-source-data (JOB-04) and deviation screening in rwb-deviation.

Temporal Schedules: rule promotion 00:01 (rwb-decision, JOB-20), measures 01:30 (rwb-reporting, JOB-15, from its own projections: no data lake), hash-chain check 02:00 (JOB-14), smoke workflow 06:00 (JOB-22), rebalancing 06:30 (JOB-06), WIN letters 16:00 (rwb-comms with rwb-integration, JOB-10). The ACE shared Quartz tables are no longer used. Full job map in the appendix.

