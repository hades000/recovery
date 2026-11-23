
Six decisions we need from the architecture team

Each has a clear owner; the first three are needed before Wave 0 starts

1

Kafka for business events

Host Recovery's business-event topics on the bank Kafka platform ACE already uses (separate topics and ACLs from PII logging); fallback: Azure Event Hubs Kafka endpoint

Owner: Enterprise Architecture, ACE platform team

2

A schema per service in the ACE database

19 schemas and 19 logins on the ACE PostgreSQL server; connection budget per service; no cross-schema access

Owner: ACE team, DBA

3

Shared Temporal layer

Platform team owns the cluster and the workflow kit; upgrade to 1.30+ for Nexus; namespaces per workbench

Owner: Platform team, ACE team

4

ACE Common contracts

Sign-in, notification path, shared case view adapter, restructure calculator (Nexus), audit and PII logging

Owner: ACE team

5

Decision ledger model

Local record + central ledger in rwb-decision; strict mode for irreversible steps; changes ADR-009

Owner: Risk, Internal Audit

6

BOT approval route

Is this a significant change under FPG 19/2560 cl. 5.5? Lead time up to 30 business days

Owner: Compliance, IT Risk

39

Notes: Decisions (owners in brackets):
1 Kafka for business events: Host Recovery's business-event topics on the bank Kafka platform ACE already uses (separate topics and ACLs from PII logging); fallback: Azure Event Hubs Kafka endpoint (Enterprise Architecture, ACE platform team)
2 A schema per service in the ACE database: 19 schemas and 19 logins on the ACE PostgreSQL server; connection budget per service; no cross-schema access (ACE team, DBA)
3 Shared Temporal layer: Platform team owns the cluster and the workflow kit; upgrade to 1.30+ for Nexus; namespaces per workbench (Platform team, ACE team)
4 ACE Common contracts: Sign-in, notification path, shared case view adapter, restructure calculator (Nexus), audit and PII logging (ACE team)
5 Decision ledger model: Local record + central ledger in rwb-decision; strict mode for irreversible steps; changes ADR-009 (Risk, Internal Audit)
6 BOT approval route: Is this a significant change under FPG 19/2560 cl. 5.5? Lead time up to 30 business days (Compliance, IT Risk)

