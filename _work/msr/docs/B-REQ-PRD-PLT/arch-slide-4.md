
19 business modules become 19 services, in four groups

One service per module from the functional specifications; each can be reused or replaced on its own

Case & control  (4)

Case & workflow
P3 · rwb-case

Decision center & log
P7 · rwb-decision

Access & administration
P4 · rwb-access

Deviation handling
S8 · rwb-deviation

Recovery routes  (7)

Valuation & route
S1 · rwb-valuation

TDR, settlement, DIL
S2 · rwb-treatment

Guarantees
S3 · rwb-guarantee

Litigation & enforcement
S4 · rwb-litigation

Assets & auction
S5 · rwb-asset

Debt sale
S6 · rwb-debtsale

Write-off & recovery
S7 · rwb-writeoff

Shared capabilities  (5)

Document hub
P5 · rwb-document

Communications
P6 · rwb-comms

Payments & posting
P8 · rwb-payment

Partner management
S9 · rwb-partner

Integration & files
P2 · rwb-integration

Data & AI  (3)

Source data
P1 · rwb-source-data

Reporting
P9 · rwb-reporting

Agent runtime
P10 · rwb-agent

Every service has
api + worker deployment
schema rwb_<name> + DB login
topic rwb.<name>.events.v1
task queue rwb-<name>

Shared platform (not in the 19)
gateway-bff + Redis session
Temporal, shared with ACE
Kafka business-event topics
Airflow, bank scheduler (to discuss)
observability (OpenTelemetry)

19 modules = 19 services: each can be released, scaled, reused or replaced on its own.

4

Notes: Rule: one deployable service per BA module, so that each capability has its own code, release, owner, contract, schema, topic and task queue. This is what makes later reuse possible: another workbench can call or deploy rwb-document, rwb-comms or rwb-decision without taking the rest of Recovery.

Groups are for reading only; they are not deployment units. Shared platform pieces (gateway-bff with Redis, Temporal, Kafka, the bank's Airflow scheduler, observability) are not counted in the 19.

First epic per service: Epic 1: P1, P2, P3, P4, P5, P6, P7, P9, P10. Epics 2-3: P8, S2, S5, S8. Epics 4-5: S1, S3, S4, S6. Epics 6-7: S7, S9.

