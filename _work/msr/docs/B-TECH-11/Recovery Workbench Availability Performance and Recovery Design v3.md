SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Recovery Workbench

Availability, performance and recovery design

| Item | Detail |
|---|---|
| Document | Recovery Workbench availability, performance and recovery design |
| Version | 3 |
| Date | 22 November 2026 |
| Change | 3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Prepared by | Henka Group |
| Structure | ISO/IEC 25010 |
| Status | Draft. No approval is recorded for this version (ASM-B-TECH-11-13) |
| Source version | 2 as the file name and 1 as the version in the source table, 28 October 2026 (CG-B-TECH-11-1; ASM-B-TECH-11-1) |
| Tool | T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60 |

# Change log

| Version | Date | Change |
|---|---|---|
| 3 | 22 November 2026 | 3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash. Targets per service and per call type, the recovery point and the recovery time left open per store, the shape and the scaling of one of the 19 services, backup per store, degraded modes per service, and tests per service. Sections 1 to 6; the change table is at the end of the document |
| 2 | 28 October 2026 | Source version. The source carries no change log and records no change: one recovery module inside ACE, with its service levels, the load it carries, scaling, backup and restore, degraded modes and tests |

# 1. Service levels

Version 2 wrote these eight levels for one recovery module. Architecture v5 sets the same targets per service (slide 48, "Service targets (NFR v3)") and cuts the module into 19 services (ADR-013; Rules v1 §R4), so every level keeps its value and its status and gains the owner that makes it testable (DL45, DL46). No level is relaxed and no number is changed.

| Item | Target | Status |
|---|---|---|
| Availability in business hours | 99.9 percent | Proposed, DL11 |
| Availability outside business hours | 99.5 percent, excluding the change window | Proposed, DL11 |
| Screen response | Under 2 seconds at the 95th percentile | Proposed, DL11 |
| Rule evaluation | Under 300 milliseconds | Proposed, DL11 |
| Agent response | 60 seconds, then the rule result | Proposed, DL11 |
| COLLINS load complete | By 07:00 | Proposed |
| Recovery point objective | The ACE value | Open, DL11 |
| Recovery time objective | The ACE value | Open, DL11 |

## 1.1 Who owns each service level

Every owner below is a service code or a platform epic of the Microservice Ownership Map v1 and the plan ownership file, not a team and not a person (ASM-B-TECH-11-11).

| Service level | Owner | Basis |
|---|---|---|
| Availability in business hours | The 19 services, RWB-SVC-P1 to RWB-SVC-S9, each for its own API and worker deployment; RWB-PLT-DB for the instance | Architecture v5 slide 48 sets the target per service; ADR-013, ADR-014 |
| Availability outside business hours | The same 19 services, with RWB-PLT-WF and RWB-PLT-EVT for the platform the window depends on | Architecture v5 slide 48; ADR-015, ADR-016 |
| Screen response | gateway-bff composes the screen (RWB-PLT-EDGE); each owning service answers inside the one-hop budget | Architecture v5 slide 10; ADR-020 |
| Rule evaluation | The owning service with its embedded engine (ADR-017); the registry and the versions are P7 rwb-decision (RWB-SVC-P7) | Temporal and Drools design slides 15 and 16; DP-04 |
| Agent response | P10 rwb-agent (RWB-SVC-P10) | Architecture v5 slide 41; DP-20 |
| COLLINS load complete | P1 rwb-source-data, with P3 rwb-case and P8 rwb-payment in the same 05:00 to 07:00 chain | Architecture v5 slide 33; JOB-04 owner P1 (CG-B-TECH-11-9) |
| Recovery point objective | RWB-PLT-DB with SCB IT infrastructure, which operates the store | Section 4; CG-B-TECH-11-2 |
| Recovery time objective | RWB-PLT-DB with SCB IT infrastructure, which operates the store | Section 4; CG-B-TECH-11-2 |

## 1.2 Availability per service

All 19 services carry the same two targets, because the target of slide 48 is a service target and the module has no tiering rule of any kind in the source (CG-B-TECH-11-5; ASM-B-TECH-11-5). "Outside business hours" carries the same exclusion as the table above: the change window does not count.

| Service | Owner | Wave | Availability in business hours | Availability outside business hours |
|---|---|---|---|---|
| rwb-source-data | RWB-SVC-P1 | 1 | 99.9 percent | 99.5 percent |
| rwb-integration | RWB-SVC-P2 | 1 | 99.9 percent | 99.5 percent |
| rwb-case | RWB-SVC-P3 | 1 | 99.9 percent | 99.5 percent |
| rwb-access | RWB-SVC-P4 | 1 | 99.9 percent | 99.5 percent |
| rwb-document | RWB-SVC-P5 | 1 | 99.9 percent | 99.5 percent |
| rwb-comms | RWB-SVC-P6 | 1 | 99.9 percent | 99.5 percent |
| rwb-decision | RWB-SVC-P7 | 1 | 99.9 percent | 99.5 percent |
| rwb-payment | RWB-SVC-P8 | 2 | 99.9 percent | 99.5 percent |
| rwb-reporting | RWB-SVC-P9 | 1 | 99.9 percent | 99.5 percent |
| rwb-agent | RWB-SVC-P10 | 1 | 99.9 percent | 99.5 percent |
| rwb-valuation | RWB-SVC-S1 | 3 | 99.9 percent | 99.5 percent |
| rwb-treatment | RWB-SVC-S2 | 2 | 99.9 percent | 99.5 percent |
| rwb-guarantee | RWB-SVC-S3 | 3 | 99.9 percent | 99.5 percent |
| rwb-litigation | RWB-SVC-S4 | 3 | 99.9 percent | 99.5 percent |
| rwb-asset | RWB-SVC-S5 | 2 | 99.9 percent | 99.5 percent |
| rwb-debtsale | RWB-SVC-S6 | 3 | 99.9 percent | 99.5 percent |
| rwb-writeoff | RWB-SVC-S7 | 4 | 99.9 percent | 99.5 percent |
| rwb-deviation | RWB-SVC-S8 | 2 | 99.9 percent | 99.5 percent |
| rwb-partner | RWB-SVC-S9 | 4 | 99.9 percent | 99.5 percent |

The target is a target per service, not per screen. A screen that composes two answers through gateway-bff sees the product of the two, 99.8 percent, and the call budget of section 1.3 is what keeps that screen inside the 2 second target (ASM-B-TECH-11-6). A service is measured on its own API deployment and on its own task queue, and the 19 measurements together are the Workbench number.

## 1.3 Performance per call type

The response levels of section 1 are stated per call, not per service: the owning service answers one call inside its budget, and the composed screen is the sum of the one-hop budgets of Architecture v5 slide 10 (gateway and session 0.15 s, the slowest of the parallel calls 0.6 s, composition and transfer 0.3 s, about 1.2 s against the 2 second target). The targets below are the ones the source gives for each call type and each engine.

| Call type | Target | Owner | Basis |
|---|---|---|---|
| REST | 2 second timeout per call, one hop, GET retried once with jitter, circuit breaker and bulkhead per downstream; screen under 2 seconds at the 95th percentile | The calling service; the composition gateway-bff (RWB-PLT-EDGE) | Architecture v5 slides 10 and 11; ADR-020 |
| Event (Kafka) | Retry topics 1 minute, 10 minutes and 1 hour, then the dead-letter topic with an alert; 12 partitions, replication factor 3, 7 days retention; key caseId for order per case | The producing service; RWB-PLT-EVT for the platform | Architecture v5 slide 22; ADR-015 |
| Temporal | Activity start-to-close with back-off: 1 second initial interval, back-off 2, 10 attempts; a missing rule package is not retried; durable timers wait days or years across releases and restarts | The owning service and its task queue; RWB-PLT-WF for the cluster | Temporal and Drools design slides 26, 27 and 28; ADR-016 |
| File | Claim-check: a SAS link per file, valid 15 minutes, and a manifest with the checksum; the checksum is verified on receipt and the workflow retries the file | P2 rwb-integration for outbound files, P5 rwb-document for documents | Architecture v5 slide 11 |
| SQL view | 5 second statement timeout; read-only login; 30 recovery.v_ace_* views; no other service reads them | P1 rwb-source-data only | Architecture v5 slide 11; ADR-014; DP-05 |
| Rule evaluation | Under 300 milliseconds | The owning service, with the version and the checksum from P7 rwb-decision | Section 1; ADR-017; DP-04 |
| Agent | 60 seconds, then the rule result; the officer is never blocked | P10 rwb-agent | Section 1; R-UNI-32; DP-20 |

## 1.4 Recovery point and recovery time

The two rows of section 1 are kept exactly as version 2 wrote them: the value is the ACE value and the status is open (DL11). Architecture v5 records the same position and calls it an NFR gap ("RPO/RTO: not yet set. Proposed tiers."), and no proposed tier appears in any source of this run. The value is therefore Not specified in the source documents (CG-B-TECH-11-2; ASM-B-TECH-11-2) for every store, and version 3 does not invent a tier, a number of minutes or a number of hours for any service (DL48, DL49).

| Store | Scope | Recovery point objective | Recovery time objective |
|---|---|---|---|
| ACE database | The 19 schemas in one zone-redundant PostgreSQL flexible server | Not specified in the source documents (CG-B-TECH-11-2; ASM-B-TECH-11-2) | Not specified in the source documents (CG-B-TECH-11-2; ASM-B-TECH-11-2) |
| Temporal persistence | The rwb-recovery namespace, in its own database with no grant on the ACE database | Not specified in the source documents (CG-B-TECH-11-2; ASM-B-TECH-11-2) | Not specified in the source documents (CG-B-TECH-11-2; ASM-B-TECH-11-2) |
| Kafka topics | The 19 topics rwb.<short>.events.v1 and rwb.decision-record.v1 | Not specified in the source documents (CG-B-TECH-11-2; ASM-B-TECH-11-2) | Not specified in the source documents (CG-B-TECH-11-2; ASM-B-TECH-11-2) |

Three consequences are worth writing down while the value is open. First, an RPO belongs to the store and not to the service: the 19 schemas sit in one instance, so one restore point covers all 19, and no service can promise a tighter target than the database it sits in. Second, the 7 days retention and the replication factor 3 of a Kafka topic are a replay window, not an RPO. Third, the 30 days retention of a closed Temporal workflow, archived to Blob, is a retention rule and not an RTO. Until the ACE value is confirmed, a restore test measures the time and records it; it cannot pass or fail against a target.

# 2. Load the design carries

The seven measures of version 2 are kept as written. They describe the Workbench and not one service, and with 19 services they are split by the owner of the work, not multiplied (section 2.1).

| Measure | Value |
|---|---|
| Open cases at go-live | About 23,600 |
| Open cases at the end of 2027 | About 26,500 |
| Named users | 1,234 |
| Online in the busiest hour | About 410 |
| Requests a second in the busiest hour | About 21 |
| Documents by the end of 2031 | About 5.8 million, 2.8 TB |
| Decision log and ledger by the end of 2031 | About 36 GB |

## 2.1 Where the load lands, service by service

Architecture v5 slide 33 names the services the load concentrates on, and the numbers agree with the table above to within a fraction of a percent (CG-B-TECH-11-4; ASM-B-TECH-11-4):

- The 05:00 to 07:00 chain: case creation and allocation in rwb-case (P3), payment matching in rwb-payment (P8), and the deviation screening that runs after the data is ready in rwb-deviation (S8).
- Document intake and text reading: bursts of uploads in rwb-document (P5) and the runs in rwb-agent (P10), against the 500 pages an hour target of slide 48.
- Letters and notices at 16:00, and court-date timers: rwb-comms (P6) with rwb-integration (P2).
- Agent runs: rwb-agent (P10), 60 seconds then the rule result.
- Rule evaluation: 283 to 318 thousand evaluations a month, in the owning service, so the load lands on all 19 embedded engines in proportion to their rules and not on one central engine.

The remaining capacity figure is the 2031 horizon, which version 2 stops short of: about 47,389 open cases by 2031 (Architecture v5 slide 33). The screens themselves stay light - two small pods per service are enough (slide 48) - so the load is a reason to scale workers, not a reason to add a service.

# 3. Scaling

- The 19 Recovery services run inside ACE on the shared AKS clusters, each as an API deployment of two pods for availability, scaled on CPU or request rate, and a worker deployment scaled by KEDA on the Temporal task-queue backlog or on Kafka consumer lag, down to zero for bursty work (Architecture v5 slide 33; ADR-013, ADR-016). Recovery adds no separate platform: the cluster, Kafka, Temporal and the database are already the ACE platforms (ASM-B-TECH-11-9).
- PostgreSQL flexible server, zone redundant, with one schema per service; read queries for reports go to the rwb-reporting read model built from the events, not to the 19 live schemas and not to a data lake, which the target architecture removes (ADR-014, ADR-018; DP-17; CG-B-TECH-11-3, ASM-B-TECH-11-3).
- Large tables (decision log, ledger, documents index) are partitioned by month.
- Documents are in Blob storage; the database holds only the index and extracted fields.
- Batch work runs outside business hours where it can: loads before 07:00, reconciliation after the load, retention at night.

The three bullets above name an object and no owner. In version 3 each object is owned once: the decision log and the ledger are in rwb_decision (P7) and the documents index in rwb_document (P5), and each is partitioned in its own schema, with no partition and no index crossing a schema (ADR-014). The Blob container and the custody and retention rows are P5 rwb-document, whose JOB-17 retention run is the record of where a document is. The load check and the reconciliation are JOB-04 in rwb-source-data (P1), the retention run is JOB-17 in rwb-document (P5), and no shared Quartz table remains (ADR-016; DP-10).

## 3.1 The shape of one of the 19 services

All 19 services have the same shape, so capacity is a per-service question with one answer that repeats (Architecture v5 slide 33; ADR-013).

| Part | Copies | Scaling signal | Owner |
|---|---|---|---|
| API deployment | 2 pods fixed for availability, more on CPU or request rate if ever needed | CPU or request rate | Each service, RWB-SVC-P1 to RWB-SVC-S9 |
| Worker deployment | 0 to many, down to zero for bursty work such as OCR or agent runs | KEDA on the Temporal task-queue backlog, or on Kafka consumer lag | Each service, with RWB-PLT-WF for the scaler and the queues |
| Database access | One pool per service login, capped | Connections per login | RWB-PLT-DB with the ACE DBA; ADR-014, ADR-021 |
| Event path | One topic rwb.<short>.events.v1 per service, 12 partitions, replication factor 3 | Consumer lag | RWB-PLT-EVT; ADR-015 (CG-B-TECH-11-6; ASM-B-TECH-11-7) |
| Workflow path | One task queue rwb-<short> per service | Task-queue backlog | Each service, with RWB-PLT-WF |

## 3.2 What is scaled and what is not

- Scaled: the morning chain (rwb-case, rwb-payment, rwb-deviation), document intake and reading (rwb-document, rwb-agent), notice generation and timers (rwb-comms, rwb-integration) and the agent runs (rwb-agent).
- Not scaled for throughput: the API tier. Two pods per service carry the 21 requests a second of the busiest hour, and the case for 19 services is ownership, release independence and failure isolation, not raw throughput (Architecture v5 slide 48).
- Never one hop deeper: a screen calls each owner directly and in parallel, so a slow service slows its own tab and not the screen (ADR-020).

# 4. Backup and restore

| Store | Backup | Restore test |
|---|---|---|
| ACE database | Point-in-time restore on the ACE pattern | Before the first production release, then each quarter |
| Document storage | Bank backup service on the bank schedule (DL27) | Before the first production release and at each release (NFR-071) |
| Configuration and reference data | Versioned in the database and in the load files | With the database restore |

## 4.1 The owner of each store

Version 2 named three stores for one module. Version 3 keeps the three and adds the two stores the target architecture introduces, with an owner each, so a restore drill has one call to make per store.

| Store | Owner | Note |
|---|---|---|
| ACE database, the 19 schemas | Each service for its own schema; RWB-PLT-DB for the instance, the logins and the point-in-time restore; the ACE DBA runs it | RWB-PLT-NF06-DB creates the 19 schemas and logins; ADR-014, ADR-021 |
| Document storage | P5 rwb-document (RWB-SVC-P5) for the container and the index; the bank backup service for the copies | The index and the extracted fields are in rwb_document, the content is in Blob |
| Configuration and reference data | P3 rwb-case for parameters and reference data (DP-06, DP-07); the platform library for feature flags | R-PREC default rulings; both are versioned rows, not files |
| Temporal persistence | RWB-PLT-WF, in the rwb-recovery namespace and its own database | It has no grant on the ACE database (Temporal and Drools design L1) |
| Kafka topics | RWB-PLT-EVT, with replication factor 3 and 7 days retention | The replay window is not a backup |

## 4.2 What a restore of one service looks like

- The schema is restored to a point in time, and the other 18 schemas come with it, because the 19 sit in one instance (section 1.4; CG-B-TECH-11-2).
- Nothing published is lost: the outbox row is written in the same transaction as the change, so a restored schema replays what it had not yet published (DP-09; ADR-015).
- Nothing is applied twice: the inbox table processed_event of each consumer drops a redelivered event (DP-09).
- The journeys of that service resume from the last recorded step, because Temporal replays its history; tasks that were on its queue are still on its queue (Temporal and Drools design slide 27).
- Nothing is stuck without a signal: the stuck-workflow scan JOB-21, a visibility query every five minutes, reports a workflow that has not moved (JOB-21 owner PLT; RWB-PLT-WF).
- A service restored alone is consistent with the other 18 through its events, because no service reads another service's tables and no view or foreign key crosses a schema (DP-01; ADR-014).

# 5. Degraded modes

| Failure | What still works |
|---|---|
| COLLINS load late | Every screen with the last loaded data and its date; no new cases from stale data |
| Agent platform down | Every decision on rules |
| Outbound system down | Everything; outbound work waits in the outbox |
| Partner gateway down | Bank staff record partner results |
| Document storage down | Case work without opening documents; uploads wait |

## 5.1 One of the 19 services down

A failure now has a smaller blast radius than in version 2, and the cost is that there are 19 ways to lose one part. When a service is down, its own tabs show that it is temporarily unavailable, its work waits on its own task queue and on its own consumer offset, and the other 18 services keep running (Architecture v5 slide 34). With rwb-litigation (S4) as the example: the litigation tabs say temporarily unavailable, LitigationWorkflow tasks wait on queue rwb-litigation, the consumer offset of rwb.litigation.events.v1 holds, and the case list, the payments and every other route carry on; when the service is back, the tasks resume in order. The failure is seen by RWB-PLT-OBS, per service, and the alerting target belongs to that epic (CG-B-TECH-11-8; ASM-B-TECH-11-10). The partner gateway of the table above is the one row of section 5 that has no service code of its own: it is the edge of RWB-PLT-EDGE with S9 rwb-partner behind it, and the map has no row for the component itself (CG-B-TECH-11-7; ASM-B-TECH-11-8).

## 5.2 Inside one service

The failures that happen inside a service are the ones the source details, and each one now has an owner in the map (Temporal and Drools design slide 28).

| Failure | What still works | Owner |
|---|---|---|
| Worker stops | Work waits on its queue; it resumes from history | The service that owns the queue |
| A call fails (ACE, partner, database) | Retried: 1 second, doubling, up to 10 tries | The calling service |
| No rule version in force | Stops at once, no retry; the stuck-case alert is raised | P7 rwb-decision with the owning service |
| A new rule version is faulty | Refused at load; the version in force keeps running | P7 rwb-decision |
| The decision record write fails | Same transaction: nothing moves (R-UNI-39) | The owning service, with the ledger in P7 |
| The AI assistant is slow | After 60 seconds the rule answer is used (R-UNI-32) | P10 rwb-agent |
| Kafka is down | Events wait in the outbox; none lost | RWB-PLT-EVT with every producer |
| The central ledger is late | Work carries on; points of no return wait for the confirmation | P7 rwb-decision |

# 6. Tests

- Load test at the busiest-hour volume before each release (RWB-TE-009).
- Failover test of the database before the first production release.
- Restore test of documents and the database before the first production release.
- Agent outage test: the case routes on the rule result.

## 6.1 The tests per service and across services

Version 2 named four tests and one story, RWB-TE-009. The split plan carries that story as RWB-ITG-TE009-ITG, and the platform and service stories carry the rest, so every test below has one owner and one level (Rules v1 §R7.2 s16). The failover and the restore test have no story of their own in the split plan and are owned by the database story (CG-B-TECH-11-10; ASM-B-TECH-11-12).

| Test | Scope | Owner | Level |
|---|---|---|---|
| Load test at the busiest-hour volume before each release | The composed screens and the 19 services | RWB-ITG-TE009-ITG | NFR |
| Failover test of the database before the first production release | The zone-redundant instance and all 19 schemas | RWB-PLT-NF06-DB with the ACE DBA | NFR |
| Restore test of documents and the database before the first production release | Blob and the 19 schemas; the time is recorded while the target is open | P5 rwb-document with RWB-PLT-DB | NFR |
| Agent outage test: the case routes on the rule result | P10 and every caller of the agent contract | RWB-SVC-P10 | Integration |
| Replay gate: every build replays recorded histories (E2-040) | Each service's workflows | Each service, with RWB-PLT-WF | Component |
| Contract tests of the 19 contracts, run in every build | OpenAPI, AsyncAPI and the activity jars | The CON story of each service | Contract |
| Boundary test: the build fails on any cross-schema reference | Each service's own schema | Each service, with the ACE DBA | Component |
| Stuck-workflow scan JOB-21 | The rwb-recovery namespace | RWB-PLT-WF | NFR |

# Realignment changes in version 3 (D-RCV-60)

| Section | Version 2 | Version 3 | Decision |
|---|---|---|---|
| 1, 1.1 | Eight service levels for one module, no owner | The same eight, with an owner for each from the Ownership Map | ADR-013; DL45, DL46 |
| 1.2 | No target per service | Availability per service, 19 rows, the same two targets | ADR-013; ASM-B-TECH-11-5 |
| 1.3 | Screen, rule and agent levels only | The same levels per call type, with the 2 second timeout, the retry topics and the activity retry policy | ADR-015, ADR-016, ADR-020 |
| 1.4 | RPO and RTO "The ACE value", open | Kept as written; the store table states that no value exists (CG-B-TECH-11-2) | DL11, DL48, DL49 |
| 2, 2.1 | Load for one module, to 2027 | The same rows, plus where the load lands service by service and the 2031 horizon | ADR-013 |
| 3 | "The recovery module adds no separate service"; reports read the data lake copy | 19 services, each with an API and a worker deployment scaled by KEDA; reports read the rwb-reporting read model, no data lake | ADR-013, ADR-016, ADR-018; DP-17 |
| 3.1, 3.2 | No deployment shape | One shape repeated 19 times, and what is scaled and what is not | ADR-013, ADR-016 |
| 4, 4.1 | Three stores, no owner | The three, with an owner each, plus the Temporal persistence and the Kafka topics | ADR-014, ADR-015, ADR-016 |
| 4.2 | A restore test, quarterly | What a restore of one service looks like: outbox replay, inbox dedupe, history replay | DP-09, ADR-016 |
| 5, 5.1, 5.2 | Five failures, no owner | The five kept, plus one service down and the eight failures inside one service, each with an owner | ADR-023 |
| 6, 6.1 | Four tests and RWB-TE-009 | The four kept, plus contract, replay gate and boundary tests, each with the story that owns it | RWB-ITG-TE009-ITG; E2-040 |
| all | DL11 the only decision reference | DL11 kept; DL44 to DL49 and ADR-013 to ADR-023 cited where the realignment needs them; every date of the source is unchanged and read as tentative (ASM-B-TECH-11-14) | ids.json; Rules v1 §R8.4; DL48 |
