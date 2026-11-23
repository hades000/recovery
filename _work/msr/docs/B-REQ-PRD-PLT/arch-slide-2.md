
At a glance: 19 Recovery services, still part of ACE

Read clockwise from the top left

Recovery Workbench
19 services in ACE

Stays part of ACE

Same AKS cluster and App Gateway as ACE

Uses ACE Common shared services

ACE database; no data lake connection

19 services, one per module

recovery-core split along module lines

Each one reusable or replaceable alone

Own schema, topic and task queue each

Clear contracts between them

REST for screens, one hop only

Kafka events for facts

Temporal for steps and long processes

What we need from you

Kafka topics on the ACE platform

19 schemas and logins in the ACE DB

Owner for the shared Temporal layer

Recovery stays part of ACE: 19 small services on ACE's cluster, ACE's shared services and ACE's database.

2

Notes: Stays inside ACE: same AKS cluster and Azure App Gateway as ACE (path routing /recovery/* and /api/recovery/*), the ACE Common shared services (sign-in and access checks, audit and PII logging, shared case view, shared entities, restructure calculator, notification path), and the ACE PostgreSQL database. Recovery has no connection to the data lake; INT-19/INT-20 are removed.

19 services: recovery-core from the six-service proposal is split along its module lines, one service per BA module P1-P10 and S1-S9. Each has an api and a worker deployment, its own schema and login in the ACE database, its own Kafka topic and its own Temporal task queue.

How they connect: REST for screens (one hop from the BFF), Kafka events for facts, Temporal for steps in another service and long processes, files for outside parties, SQL views only for rwb-source-data reading ACE.

Decisions needed: last slide.

