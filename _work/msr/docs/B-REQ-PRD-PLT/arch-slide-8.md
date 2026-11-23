
System architecture: every runtime part and how it connects

C4 level 2 for Recovery inside the shared ACE cluster; line style shows the call type

Staff
browser

Azure App Gateway + WAF (shared)   /  and  /api/*  → ACE        /recovery/*  and  /api/recovery/*  → Recovery gateway-bff

ACE AKS CLUSTER · SHARED

ACE

ACE frontend + backend

ACE COMMON (SHARED)

Sign-in & access checks

Audit & PII logging

Shared case view

Restructure calculator

Notification path

Shared entities

gateway-bff
Redis session · JWT

Key Vault · codec server
payload keys (AES-GCM)

Partner gateway
FAPI 2.0 → S9

RECOVERY · 19 SERVICES · namespace rwb-recovery

Case &
control

P3
Case

P7
Decision

P4
Access

S8
Deviation

Routes

S1
Valuation

S2
Treatment

S3
Guarantee

S4
Litigation

S5
Asset

S6
Debt sale

S7
Write-off

Shared

P5
Document

P6
Comms

P8
Payment

S9
Partner

P2
Integration

Data & AI

P1
Source data

P9
Reporting

P10
Agent

Kafka
events

Airflow
bank, to discuss

Observability
OpenTelemetry

Temporal (shared)
task queue per service

ACE PostgreSQL · ACE schemas + 30 recovery.v_ace_* views · 19 rwb_* schemas, one login each

Blob (WORM) · documents

Temporal persistence (own DB)

OUTSIDE THE CLUSTER

Partners
law firms, agencies, buyers

Entra ID
sign-in via ACE Common

NSS SMS · LINE OA
via ACE notification path

WIN
daily letters file (INT-14)

Debt buyers
encrypted files (INT-25)

Enterprise AI
private endpoint (INT-23)

SOC / SIEM
via ACE PII logging

Data lake / Power BI
not connected (INT-19/20 removed)

Calls

REST (sync, one hop)

Kafka event

Temporal activity / child / Nexus

SQL view (read-only)

File (claim-check)

8

Notes: Edge: staff reach the shared Azure App Gateway (WAF); / and /api/* go to ACE, /recovery/* and /api/recovery/* go to the Recovery gateway-bff (Spring Cloud Gateway, session in Redis, sign-in through ACE Common). Partners use the partner gateway (FAPI 2.0) that fronts rwb-partner.

Recovery: 19 services in the rwb-recovery namespace, each an api and a worker deployment. Calls: REST from the BFF (one hop); Kafka business-event topics (outbox and relay in each service); Temporal task queue rwb-<service> in namespace rwb-recovery; Nexus to ACE for the restructure calculator.

Data: one ACE PostgreSQL server. ACE schemas and the 30 recovery.v_ace_* views (read only by rwb-source-data); 19 Recovery schemas, one login and connection pool each; Temporal persistence in its own database; documents in Blob with WORM.

Outside: Enterprise AI (INT-23) from rwb-agent; WIN file (INT-14) and debt-buyer files (INT-25) from rwb-integration via MFT/SFTP; SMS and LINE through the ACE notification path; logs to SOC through ACE PII logging. No data lake.

Airflow in the platform row is the bank's enterprise scheduler, replacing Control-M (for discussion). It runs the overnight chain, file windows and report extracts and calls Recovery APIs only; per-case work stays in Temporal.

