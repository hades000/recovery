
System context: Recovery lives inside the ACE platform

C4 level 1: people above, ACE platform in the middle, outside systems at the sides

Recovery officers & approvers
Work cases, approve routes

Managers, Risk & Audit
Monitor, review, audit

External partners
Law firms, agencies, valuers, buyers

ACE PLATFORM · SAME AKS CLUSTER, APP GATEWAY AND DATABASE

ACE Collection
collections workbench

Recovery Workbench
19 services + gateway-bff

Temporal · Kafka
shared with ACE

ACE Common
sign-in, logging, case view, calculator, notices

ACE PostgreSQL · ACE schemas + v_ace_* views + 19 Recovery schemas

/recovery/* via App Gateway

partner gateway

case view

own schemas

Recovery → ACE Common: sign-in, logging, notices, restructure calculator

Source systems
COLLINS, ALS, CCMS, GL …

ACE ingestion (overnight)

Data lake / Power BI
not connected

Entra ID
via ACE Common sign-in

Enterprise AI
private endpoint · rwb-agent

NSS SMS · LINE OA
via ACE notification path

WIN · debt buyers
files · rwb-integration

SOC / SIEM
via ACE PII logging (Kafka)

Recovery adds services inside ACE's platform; it reads ACE data through views and never connects to the data lake.

7

Notes: Recovery Workbench runs in the same AKS cluster and behind the same Azure App Gateway as ACE Collection. The App Gateway routes / and /api/* to ACE and /recovery/* and /api/recovery/* to the Recovery gateway-bff.

ACE ingests all source systems (COLLINS, ALS, CCMS, SVAF, AMIS, RPS, LIT, WIN POD, GL, SCBPDM, NLEADS, EasyApp) into the ACE database overnight. Recovery loads no source data itself: rwb-source-data reads ACE data through the 30 read-only recovery.v_ace_* views (ADR-010).

ACE Common (owned by the ACE team, INT-34) gives Recovery: sign-in and access checks (Entra ID), audit and PII logging (PII Kafka to SOC), the shared case view, shared entities, the restructure calculator and the notification path (NSS SMS, LINE OA).

Outside: Enterprise AI private endpoint (INT-23) for rwb-agent; WIN outbound file (INT-14) and debt-buyer files (INT-25) through rwb-integration. No data lake or Power BI connection (INT-19/20 removed).

