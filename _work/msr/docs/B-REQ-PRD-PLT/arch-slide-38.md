
Getting there: services arrive with the epics that need them

Wave 0 builds the template once; then each epic adds its services

Wave 0 · now
Platform once

Service template + Helm

Contract libraries

Workflow kit (L3)

19 schemas + logins

Kafka topics + ACLs

Temporal 1.30+

Wave 1 · Epic 1
9 services

P1 · Source data

P2 · Integration

P3 · Case

P4 · Access

P5 · Document

P6 · Comms

P7 · Decision

P9 · Reporting

P10 · Agent

Wave 2 · Epics 2-3
+4 services

P8 · Payment

S2 · Treatment

S5 · Asset

S8 · Deviation

Wave 3 · Epics 4-5
+4 services

S1 · Valuation

S3 · Guarantee

S4 · Litigation

S6 · Debt sale

Wave 4 · Epics 6-7
+2 services

S7 · Write-off

S9 · Partner

BOT approval before Wave 1 go-live, if required (FPG 19/2560 cl. 5.5; up to 30 business days)

Build the platform pieces once; then every epic adds only its own services, so nothing is built twice.

38

Notes: Wave 0 is the enabler: service template (Spring Boot, outbox, inbox, Temporal worker, codec, OpenTelemetry), one Helm chart, golden pipeline, contract libraries, the workflow kit, the 19 schemas and logins, Kafka topics and ACLs, Temporal 1.30+.

Waves follow the first epic of each module: Epic 1: P1, P2, P3, P4, P5, P6, P7, P9, P10 (9 services). Epics 2-3: P8, S2, S5, S8 (+4). Epics 4-5: S1, S3, S4, S6 (+4). Epics 6-7: S7, S9 (+2). A service is created when its epic starts, so nothing is built twice.

BOT: if the change is significant under FPG 19/2560 cl. 5.5, BOT approval is needed before Wave 1 go-live (up to 30 business days).

