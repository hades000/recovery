
Service contracts 2/7 · Deviation, source data, reporting

IN = what the service accepts; OUT = what it writes and sends; the tag is the call type

IN

OUT

REST  GET/POST /deviations · POST /deviations/{id}/clear
EVT  CaseCreated (screening) · AceDataReady (deceased, bankrupt flags) · AgentRunCompleted
TMP  DeviationWorkflow (child of case)

DB  writes schema rwb_deviation: X1-X7 screening, pause, handling, return
EVT  rwb.deviation.events.v1: DeviationRaised, DeviationCleared
TMP  Agent: child: screening agent run
REST  Source data: party flags

S8 · rwb-deviation
Deviation handling
queue rwb-deviation
rwb.deviation.events.v1

IN

OUT

REST  GET /customers/{id}, /accounts/{id} · GET /collateral/{id}, /payments?accountId= · GET /freshness (business date) · POST /business-days/{date}/ready (Airflow)
EVT  (none: Airflow call; fallback polls ACE batch record)
TMP  Act: listEligibleAccounts, snapshot(page) · Workflow: AceIngestCheck, reconciliation

DB  writes schema rwb_source_data: ACE view contract, extension tables, freshness, reconciliation
EVT  rwb.source-data.events.v1: AceDataReady, AceDataLate (05:30)
SQL  ACE DB views: SELECT recovery.v_ace_* (30 views)

P1 · rwb-source-data
Source data
queue rwb-source-data
rwb.source-data.events.v1

IN

OUT

REST  GET /dashboards/{id} · GET /reports/{id} · POST /reports/{id}/run (Airflow)
EVT  All business events (projections) · DecisionRecorded
TMP  Schedule: measures 01:30 · Act: buildRegulatoryExtract

DB  writes schema rwb_reporting: measures, snapshots, steering dashboard, regulatory reports
EVT  rwb.reporting.events.v1: ReportPublished
TMP  Source data: snapshot(page) for measures · Integration: deliverFile (regulatory extract)

P9 · rwb-reporting
Reporting
queue rwb-reporting
rwb.reporting.events.v1

15

Notes: Contracts in full (also in the service catalogue in the appendix):

rwb-deviation (S8, Deviation handling)
IN: REST GET/POST /deviations; POST /deviations/{id}/clear | events CaseCreated (screening); AceDataReady (deceased, bankrupt flags); AgentRunCompleted | Temporal DeviationWorkflow (child of case)
OUT: schema rwb_deviation (X1-X7 screening, pause, handling, return) | topic rwb.deviation.events.v1: DeviationRaised, DeviationCleared | TMP Agent: child: screening agent run | REST Source data: party flags

rwb-source-data (P1, Source data)
IN: REST GET /customers/{id}, /accounts/{id}; GET /collateral/{id}, /payments?accountId=; GET /freshness (business date); POST /business-days/{date}/ready (Airflow) | events (none: Airflow call; fallback polls ACE batch record) | Temporal Act: listEligibleAccounts, snapshot(page); Workflow: AceIngestCheck, reconciliation
OUT: schema rwb_source_data (ACE view contract, extension tables, freshness, reconciliation) | topic rwb.source-data.events.v1: AceDataReady, AceDataLate (05:30) | SQL ACE DB views: SELECT recovery.v_ace_* (30 views)

rwb-reporting (P9, Reporting)
IN: REST GET /dashboards/{id}; GET /reports/{id} · POST /reports/{id}/run (Airflow) | events All business events (projections); DecisionRecorded | Temporal Schedule: measures 01:30; Act: buildRegulatoryExtract
OUT: schema rwb_reporting (measures, snapshots, steering dashboard, regulatory reports) | topic rwb.reporting.events.v1: ReportPublished | TMP Source data: snapshot(page) for measures · Integration: deliverFile (regulatory extract)

Tags: REST = synchronous HTTPS (OpenAPI 3.1); EVT = Kafka topic (CloudEvents, AsyncAPI); TMP = Temporal activity or child workflow on the owner's task queue; NEXUS = Temporal Nexus operation into another namespace; SQL = read-only view; FILE = claim-check file; DB = the service's own schema in the ACE database.

