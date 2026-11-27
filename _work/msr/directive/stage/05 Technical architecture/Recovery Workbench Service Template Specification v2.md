SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench Service Template Specification v1

**Change log.** D-RCV-60, 26 November 2026: cross-document changes under the programme directive. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Document | Recovery Workbench Service Template Specification |
| Version | 1 |
| Date | 22 November 2026 |
| Decision | D-RCV-60 microservice realignment |
| Tool | T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Status | Draft |
| Owner role | Solution architect, with the platform team |
| Applies to | The 19 Recovery services P1 to P10 and S1 to S9, and gateway-bff |
| Source of record | Recovery Workbench Architecture v5 Text Extract v1 (slides 11, 20, 23 to 30, 33, 38); Recovery Workbench Temporal and Drools Design Text Extract v1 (slides 13 to 15); Recovery Workbench Microservice Ownership Map v1; Recovery Workbench Non Functional Specification v3 |
| Companion | Recovery Workbench Service Catalog v1 |
| Change log | below |

| Version | Date | Change | Detail |
|---|---|---|---|
| 1 | 22 November 2026 | D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash | First Service Template Specification. Fixes the one template from which all 19 services are built: the repository layout, the naming, the data, REST, event, Temporal, rules, decision record, access, observability, resilience, security and test parts, the delivery shape, the Definition of Done and the instantiation checklist. |

# 1. Purpose and scope

Architecture v5 says that every Recovery service is built from one template: Spring Boot, outbox relay, inbox, Temporal worker, codec, OpenTelemetry and contract tests (slide 20), and that Wave 0 builds the template once with one Helm chart, the golden pipeline, the contract libraries, the workflow kit, the 19 schemas and logins, the Kafka topics and ACLs, and Temporal 1.30 or later (slide 38).

This specification writes down what that template contains, so that 19 teams do not each invent it. It is the build contract between the platform team, which owns the template, and each service team, which instantiates it.

It does not repeat the per-service facts. The code, the schema, the REST base, the topic, the task queue, the Java package, the resources and the service's own contract are in the Service Catalog v1. This document describes the parts that are identical in all 19 services, the parts that are parameterised per service, and the tests that prove a service was built from the template.

# 2. What the template is

## 2.1 The twelve parts

| # | Part | What it gives the service | Basis |
|---|---|---|---|
| 1 | Service skeleton | Spring Boot application with the health, metrics, configuration, error handling and logging wiring already in place | Arch v5 slide 20 |
| 2 | Data access and migrations | Own schema, one login, Flyway sequence, standard record columns, capped connection pool | Arch v5 slide 29; TSD T3.0 |
| 3 | REST adapter | OpenAPI-first controller, RFC 9457 problem details, Idempotency-Key, timeout, breaker and bulkhead | Arch v5 slides 10 and 11 |
| 4 | Event adapter and outbox relay | CloudEvents binary producer, outbox and inbox, retry topics and dead-letter handling | Arch v5 slides 11 and 22 |
| 5 | Temporal worker | Worker on queue `rwb-<svc>`, activity and workflow registration, payload codec, Continue-As-New helper | Arch v5 slides 23 and 24 |
| 6 | Workflow kit client | The versioned L3 templates: Approval, Notify, Document intake, Agent run with fallback, Human task with SLA, Saga runner, Scheduled job, Partner instruction | Arch v5 slide 23 |
| 7 | Rules kit | Embedded Drools, the EvaluateRules activity, rule package fetch with checksum, fallback to the last in-force package | Arch v5 slides 27 and 28; Temporal and Drools slides 13 to 15 |
| 8 | Decision record library | Local hash-linked record in the service schema, DecisionRecorded through the outbox, strict mode for points of no return | Arch v5 slides 20 and 28 |
| 9 | Access guard | Authorise call to rwb-access, cached permissions, object-level authorisation, masking policy | Arch v5 slides 10 and 30; DP-08 |
| 10 | Observability kit | OpenTelemetry traces, metrics and logs, the standard dashboards and the standard alerts | Arch v5 slide 20; NFR-064 and NFR-068 |
| 11 | Contract kit | OpenAPI 3.1, AsyncAPI 3.0 and activity contract jar, published before the code, with the fake for each | Arch v5 slide 11 |
| 12 | Delivery kit | One Helm chart, the golden pipeline, two deployments (API and worker), KEDA scaling on the queue | Arch v5 slides 33 and 38 |

## 2.2 What the template does not decide

- The service's own tables, beyond the standard columns and the library tables. They come from the Physical Schema and the Ownership Map.
- The service's own REST resources and event names. They come from the API Specification v5 and the Kafka Topic and Event Catalog v1.
- The service's own workflow steps. They come from the Temporal Workflow and Activity Catalog v1.
- The release date of the service. It comes from the Release Plan and is tentative (Decision U7 and DL48).
- The stack versions the bank has not yet pinned (GAP-0134; ASM-0212).

# 3. Repository and module layout

## 3.1 One repository per service

Each service has one repository and one deployable, built twice into an API deployment and a worker deployment (the TSDs state one service, one repository; Architecture v5 slide 33 states the two deployments). The repository name and its location are not fixed by any source read for this work package. Not specified in the source documents (GAP-0135; ASM-0213).

The layout below is proposed by this specification (D-RCV-60) and is the same in every service. Only the package segment and the version-specific resources change.

| Path | Content | Basis |
|---|---|---|
| `src/main/java/th/co/scb/ace/workbench/recovery/<short>/api` | REST controllers generated from the OpenAPI contract, request validation, problem details | Arch v5 slide 11 |
| `.../domain` | Business logic and the state machine of the service; no framework types | Proposed |
| `.../adapter/rest` | Clients for the REST operations the service consumes, with timeout, breaker and bulkhead | Arch v5 slides 10 and 11 |
| `.../adapter/kafka` | Consumers with inbox dedupe and the producer used by the outbox relay | Arch v5 slide 22 |
| `.../adapter/db` | Repositories over the service's own schema only | Arch v5 slide 29 |
| `.../workflow` | Domain workflows (L5) and the child workflow calls; deterministic code only | Arch v5 slides 23 and 25 |
| `.../activity` | Activities: every I/O call, the rules call and the decision record call | Arch v5 slide 24 |
| `.../rules` | The EvaluateRules activity, the rule package loader and the checksum check | Temporal and Drools slide 14 |
| `.../config` | Configuration binding, secret references, feature flags | Arch v5 slide 20 |
| `src/main/resources/db/migration` | Flyway sequence V0001 to Vnnnn, owned by the service | Arch v5 slide 29 |
| `src/main/resources/openapi` | `<short>-v1.yaml`, OpenAPI 3.1, the REST contract | Arch v5 slide 11 |
| `src/main/resources/asyncapi` | `<short>-events-v1.yaml`, AsyncAPI 3.0, the event contract | Arch v5 slide 11 |
| `contract` | The activity and workflow interfaces published as a contract jar for callers | Arch v5 slide 23 |
| `helm` | Values per service and per environment for the one shared chart | Arch v5 slide 38 |
| `pipeline` | The include of the golden pipeline | Arch v5 slide 38 |
| `docs` | The service's run book; every scheduled job has one (NFR-067) | NFR-067 |

## 3.2 Shared libraries and contract artefacts

A service depends on the shared libraries and never copies them. The versions are pinned per service and upgraded deliberately (Arch v5 slide 23: kit versioned; workers pinned).

The repository and pipeline model that applies to these artefacts is in section 3.3.

| Artefact | Owner | What the service uses it for |
|---|---|---|
| Service template (this specification) | Platform team | The skeleton and every part in section 2.1 |
| Shared libraries: outbox, inbox, idempotency, codec, observability, access guard | Platform team (PLT) | The parts that must behave identically in all 19 services |
| Workflow kit L3 | Platform team | Approval, Notify, Document intake, Agent run with fallback, Human task with SLA, Saga runner, Scheduled job, Partner instruction |
| Activity contract jars L4 | Each service team | The typed interface another service calls on queue `rwb-<svc>` |
| Contract fakes | Each service team | The stand-in that lets a caller build before the callee exists (dependency class C) |
| Rule package registry client | P7 rwb-decision | Fetch and verify a rule package version |
| Decision record library | Platform team (PLT) | The local hash-linked record and DecisionRecorded |

Activity contract jar (GAP-0101). The artefact is one activity contract jar per service, named by the service's task queue `rwb-<short>`, with the Java package root `th.co.scb.ace.workbench.recovery.<short without hyphen>` (section 4). A change to an activity signature is a new major version of the jar and a new worker deployment (Service Contract Catalog v1). The groupId and artifactId are allocated with the repositories in the service template work; their values and the rest of the versioning scheme are Not specified in the source documents (GAP-0101).

## 3.3 Repository and pipeline model

The model is one repository per service, 19 repositories for the 19 services, not one repository with 19 modules and not a mixed model. It applies the constraint "one service, one repository" to each of the 19 services (story RWB-PLT-NF01-OPS).

| Item | Rule | Basis |
|---|---|---|
| Repository | Each service repository is created from the template, records the pinned template version and holds one service's code, migrations and values only | RWB-PLT-NF01-OPS |
| Pipeline | One pipeline definition in the template, referenced by every repository and not copied. The gates are build, unit, contract, boundary, migration lint, image scan, secret scan and personal-data scan; a repository cannot disable, reorder or re-threshold a gate | RWB-PLT-NF01-OPS |
| Code owners | Code owner validation runs in the pull request build of every service repository; the main branch of each requires a pull request with one approval from code owners, stale approvals are dismissed and the author's own approval does not count. Owners are team handles, never individuals; `@scb-ace/techx-recovery-tech-leads` is assumed for the recovery paths until DL37 and DL36 are answered. One code owners file per repository or one shared file: Not specified in the source documents (GAP-3192; ASM-5584) | RWB-TE-002 (Build Notes Technical Enablers v3) |
| Boundary test | Runs in every service repository against that service's own schema: it fails the build on a statement, datasource, grant or join that names another service's schema, on a reference to another service's table, and on a migration file or fixture that carries another service's objects or rows (see also section 6.5) | RWB-PLT-NF01-OPS; Arch v5 slide 29 |

# 4. Naming and identifiers

The template generates every identifier from two inputs: the service code and the short name. Nothing is typed by hand, so a service cannot drift from the rules in Template and Rules §R4.

| Element | Template expression | Example (S2) |
|---|---|---|
| Service | `rwb-<short>` | rwb-treatment |
| Schema | `rwb_<short with _>` | rwb_treatment |
| Login | the schema name | rwb_treatment |
| REST base | `/api/recovery/<short>/v1` | /api/recovery/treatment/v1 |
| Kafka topic | `rwb.<short>.events.v1` | rwb.treatment.events.v1 |
| Retry topics | `<topic>.retry.1m`, `.retry.10m`, `.retry.1h` | rwb.treatment.events.v1.retry.1m |
| Dead-letter topic | `<topic>.dlt` | rwb.treatment.events.v1.dlt |
| Event type | `rwb.<short>.<Event>.v1` | rwb.treatment.TreatmentApproved.v1 |
| Task queue | `rwb-<short>` | rwb-treatment |
| Workflow type | `<Stage>Workflow` | TreatmentWorkflow |
| Java package | `th.co.scb.ace.workbench.recovery.<short without hyphen>` | th.co.scb.ace.workbench.recovery.treatment |
| Service epic | `RWB-SVC-<code>` | RWB-SVC-S2 |
| Consumer group | the service name | rwb-treatment |
| Helm release | Not specified in the source documents (GAP-0136; ASM-0214) | Not specified in the source documents (GAP-0136; ASM-0214) |
| Container image | `<registry>/<short>:<tag>` (the registry is not fixed by a source read for this work package) | Not specified in the source documents (GAP-0136; ASM-0214) |

The database object prefix inside the schema is the short name with underscores, for example `rwb_treatment.treatment`. Cross-service references are held as IDs with a `CROSS_REF` field type and are never foreign keys (TSD T3.0 and T3.1; Arch v5 slide 29).

# 5. Configuration and secrets

| Item | Rule | Basis |
|---|---|---|
| Configuration | One configuration file per service; every value that differs by environment comes from the environment, never from code | Arch v5 slide 20 |
| Secrets | No secret in code or in a values file; secrets are read from Key Vault at run time (the codec key, the database credential, the client credential) | Arch v5 slides 23 and 29; NFR security target |
| Business values | No business value in code: parameters, reference data and rules are data (DP-06, DP-07, DP-04) | Template and Rules §R5.5 |
| Feature flags | Read from the platform library; the administration API is served by P2 | Ownership Map ruling feature flags |
| Identity | Workload identity per service for mTLS and Kafka OAUTHBEARER; a user JWT from gateway-bff for staff calls | Arch v5 slide 11 |
| Environment set | The same configuration keys in every environment; values differ only | Arch v5 slide 29 |

# 6. Data layer

## 6.1 Schema, login and grants

- One schema `rwb_<short>` and one login of the same name per service, on the ACE PostgreSQL server (Arch v5 slide 29; ADR-014).
- The login owns its schema and has no grant on any other schema. Only `rwb_source_data` has SELECT on the 30 `recovery.v_ace_*` views.
- Each login goes through its own PgBouncer pool with a connection cap and a statement timeout, so one service cannot starve ACE.
- No cross-schema joins, views or foreign keys. Services hold each other's IDs and use contracts for everything else.

## 6.2 Tables the template creates in every schema

| Table | Purpose | Owner | Basis |
|---|---|---|---|
| outbox_event | The event to publish, written in the same transaction as the state change | PLT (library object created in every schema) | Arch v5 slide 22; Ownership Map ruling library tables |
| outbox_delivery | The relay's send attempt and result for each outbox row | PLT (library object) | Ownership Map ruling library tables |
| processed_event | Inbox: the ce_id of every consumed event, written in the same transaction as the change | PLT (library object) | Arch v5 slide 22 |
| idempotency_key | The Idempotency-Key of every accepted POST, with its stored response | PLT (library object) | Arch v5 slide 11 |
| decision_record | The local, hash-linked decision record of the service | PLT (library object); the central ledger is P7 | Arch v5 slide 20; the Ownership Map v1 has no row for it |
| feature_flag, feature_flag_change | Flags read by the service and their change history | PLT | Ownership Map ruling feature flags |

The Ownership Map v1 holds six library tables as PLT objects created in every service schema: `outbox_event`, `outbox_delivery`, `processed_event`, `idempotency_key`, `feature_flag` and `feature_flag_change`. Architecture v5 slide 20 also names `decision_record` in the same sentence; the map has no row for it, so the table carries the placeholder Not specified in the source documents (GAP-0138; ASM-0216) until the map adds it.

## 6.3 Standard record columns and field types

Every business table carries the standard record columns of the TSDs (T3.0): `is_active`, `state`, `version` (optimistic lock), `created_at`, `created_by`, `updated_at`, `updated_by`. Identifiers are UUID. A reference to another service's object is a `CROSS_REF` held as a UUID, never a foreign key. A list value is an `LOV` code resolved through the reference-data contract of P3 (DP-07).

## 6.4 Migrations

- Flyway, one sequence per service, in the service's own pipeline (Arch v5 slide 29; DP-15).
- `V0001` is the service's baseline: the library tables of section 6.2 and the service's own tables.
- A migration is forward-only. A corrective change is a new version, never an edit of an applied one.
- The pipeline runs the migrations against a throw-away PostgreSQL instance and against the shared schema in order, before the deployment.

## 6.5 Boundary test

Every build runs a boundary test that fails on any reference to another schema, on any cross-schema join or view, and on any grant outside the service's own schema (Arch v5 slide 29). The test is part of the template, not of each service.

# 7. REST layer

| Item | Rule | Basis |
|---|---|---|
| Contract first | The OpenAPI 3.1 document is committed before the controller and is the source of the generated interface | Arch v5 slide 11 |
| Base path | `/api/recovery/<short>/v1`; the version is in the path | Template and Rules §R4; DP-13 |
| Depth | One hop only: browser, gateway-bff, owner. A service never calls a service that calls another for the same screen | Arch v5 slides 10 to 12 |
| Timeout | 2 s per call | Arch v5 slide 11 |
| Retry | GET retried once with jitter; a POST is never retried automatically | Arch v5 slide 11 |
| Breaker and bulkhead | Resilience4j circuit breaker and bulkhead per downstream | Arch v5 slide 11 |
| Idempotency | Idempotency-Key on every POST, stored in idempotency_key with the response | Arch v5 slide 11 |
| Errors | RFC 9457 problem details, one error model in every service | Arch v5 slide 11 |
| Authorisation | The service authorises the object itself (OWASP API1), using cached permissions from rwb-access | Arch v5 slide 10; DP-08 |
| Validation | Request validation at the edge of the controller; domain rules in the domain layer | Proposed |
| Screens | A composite screen is composed by gateway-bff in parallel; the service returns its own resource only | Arch v5 slide 10 |

# 8. Event layer

| Item | Rule | Basis |
|---|---|---|
| Transport | Kafka over TLS; CloudEvents 1.0, Kafka binding in binary mode (ce_* headers) | Arch v5 slide 11 |
| Topic | `rwb.<short>.events.v1`, 12 partitions, replication factor 3, 7-day retention, key caseId | Arch v5 slides 9 and 21 |
| Contract | AsyncAPI 3.0 per topic; JSON Schema registry with BACKWARD compatibility | Arch v5 slide 11 |
| Payload | IDs and facts only; never personal data; never the data itself (claim-check instead) | Arch v5 slide 11 |
| Producer | Transactional outbox in the service schema, published by the relay every minute (JOB-11) with an idempotent producer (acks=all, min.insync.replicas=2) | Arch v5 slides 11, 22 and 44 |
| Consumer | One consumer group per service; ce_id recorded in processed_event in the same transaction as the change | Arch v5 slide 22 |
| Retry | Retry topics at 1 min, 10 min and 1 h, then the `.dlt` topic with an alert and the replay tool | Arch v5 slide 22 |
| Ordering | Order per case, from the key caseId; no ordering assumed across cases | Arch v5 slide 21 |
| Decision record | Every service publishes DecisionRecorded to the shared topic rwb.decision-record.v1 | Arch v5 slides 20 and 28 |
| Naming | Event type `rwb.<short>.<Event>.v1`, past tense, one fact per event | Template and Rules §R4 |

# 9. Temporal layer

| Item | Rule | Basis |
|---|---|---|
| Cluster and namespace | The shared cluster, namespace rwb-recovery, Temporal 1.30 or later | Arch v5 slides 23 and 38 |
| Task queue | `rwb-<short>`; the service polls only its own queue | Arch v5 slide 24 |
| Worker | In the worker deployment of the service; KEDA Temporal scaler 2.17 or later, down to zero for bursty work | Arch v5 slides 24 and 33 |
| Deterministic code | Workflow code is deterministic; all I/O is in activities | Arch v5 slide 23 |
| Workflow ID | The business key: the case ID (written case-{caseId}) for CaseWorkflow; the stage's own key otherwise | Arch v5 slides 23 and 25 |
| Parent and children | CaseWorkflow starts one child per stage on the owner's queue; parent close policy ABANDON | Arch v5 slides 23 and 25 |
| History | Continue-As-New at every stage end and at least every 28 days (limit 51,200 events or 50 MB) | Arch v5 slide 25 |
| Codec | AES-GCM payload codec, keys in Key Vault per namespace; a codec server for the UI | Arch v5 slides 23 and 24 |
| Activity contract | Typed interfaces published as a contract jar; callers import the interface only | Arch v5 slide 23 |
| Nexus | Cross-namespace calls only, for example the restructure calculator in ACE | Arch v5 slide 24 |
| Search attributes | CaseId, Stage, ProductGroup, QueueCode | Temporal and Drools slide 13 |
| Versioning | Worker Versioning for safe upgrades; the kit is versioned and workers are pinned | Arch v5 slide 23 |
| Retry policy | 1 s initial interval, back-off 2, 10 attempts; NoPackageInForce is non-retryable | Temporal and Drools slide 14 |

The four steps inside every stage workflow are the same (Temporal and Drools slide 13): receive the event, ask the rules (EvaluateRules), record and apply in one transaction (RecordAndApply), wait on a durable timer or the next signal.

# 10. Rules layer

- Governance is central: authoring, tests, four-eyes approval, effective dating and version audit in P7 rwb-decision (Arch v5 slide 27; ADR-017).
- Evaluation is local: each service embeds the Drools kit and evaluates inside an activity, under 300 ms at the 95th percentile (NFR-011). There is no shared rule server on the hot path.
- The service loads a package with `GET /rule-models/{n}/{v}` on rwb-decision, verifies the checksum and swaps it in when RulePackageInForce arrives (Arch v5 slides 15 and 27).
- `RuleEvaluator.evaluate(packageCode, facts, onDate)` returns `RuleResult(packageCode, packageVersion, ruleId, outputs)`. The answer and the version are written to the decision record.
- The target is OMG DMN 1.6, table by table, on the same Drools runtime (Arch v5 slide 32).
- A package version moves through LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED; the promotion at 00:01 is JOB-20 and it publishes RulePackageInForce (Temporal and Drools slide 15).

# 11. Decision record layer

- Every service writes a decision record in its own schema, hash-linked to the previous record, in the same transaction as the state change, and publishes DecisionRecorded through its outbox (Arch v5 slide 28).
- P7 collects the records into the central ledger within 5 minutes, raises a gap alert and checks the chain every day (JOB-14).
- Strict mode applies at points of no return, where the step waits for the ledger acknowledgement: debt transfer, write-off, auction sale and title transfer. Every other step carries on at full speed.
- What the record carries: the rule or DMN model version and id, the inputs, the answer, the approver where an approval was needed, and the hash link.
- The daily ledger seal is anchored in WORM storage by P7 (Arch v5 slide 28; ADR-022).

# 12. Access and authority

- Sign-in is ACE Common; gateway-bff holds the session in Redis and passes a short-lived user JWT (Arch v5 slides 10 and 20).
- Authorisation is a call to `POST /authorise` on rwb-access with role, scope and DoA, and the answer is cached (DP-08, guard library).
- Roles and DoA limits are data in rwb_access, not code (Ownership Map ruling delegation_limit).
- Each service enforces object-level authorisation on the object it returns, and applies the masking policy for the caller's role (Arch v5 slide 10).
- Partner access goes through the partner gateway with FAPI 2.0, MFA and partner identities separate from bank identities; each partner user sees only their own firm's instructions (Arch v5 slides 17 and 30; NFR section 4).

# 13. Observability

| Item | Rule | Basis |
|---|---|---|
| Traces | OpenTelemetry, propagated across REST, Kafka headers and Temporal; one trace shows the hop chain | Arch v5 slide 20 |
| Metrics | The service exposes /metrics; the platform scrapes it; the queue backlog and consumer lag are standard panels | Arch v5 slides 24 and 33 |
| Logs | Structured, correlated by trace ID and case ID; audit and PII logging goes to ACE Common | Arch v5 slides 20 and 30 |
| Health | /health for the platform; readiness covers the database, Kafka and Temporal connections | Arch v5 slide 20 |
| Dashboards | One standard service dashboard from the template: requests, errors, latency, queue backlog, consumer lag, outbox age, DLT count | Proposed |
| Alerts | An alert reaches the named owner within 15 minutes (NFR-068); every scheduled job has a run book and an alert (NFR-067) | NFR-067, NFR-068 |
| SLOs | Screen under 2 s at the 95th percentile (NFR-008); rule evaluation under 300 ms (NFR-011); 99.9 per cent in business hours (NFR-020) | NFR-008, NFR-011, NFR-020 |

# 14. Error handling and resilience

| Failure | Behaviour | Basis |
|---|---|---|
| REST downstream slow or down | 2 s timeout, circuit breaker opens, bulkhead caps concurrent calls, the screen shows the partial answer | Arch v5 slides 10 and 11 |
| Kafka down | Events wait in the outbox; nothing is lost; the relay resumes | Arch v5 slides 22 and 34 |
| Consumer failure | Retry topics at 1 min, 10 min and 1 h, then the dead-letter topic with an alert and the replay tool | Arch v5 slide 22 |
| Temporal down | Journeys pause and resume; screens still work from the read model | Arch v5 slide 34 |
| ACE database busy | Capped pools and statement timeouts keep Recovery from starving ACE | Arch v5 slide 29 |
| AI slow | The rule result is used after 60 s and the case still routes | Arch v5 slides 16 and 33; NFR-010 |
| Interface failure after retries | The item moves to the exception queue with a task for the owner (three retries per item) | NFR-026 |
| Release failure | Roll back by redeploying the previous tag | NFR-027 |
| Saga step failure before the pivot | Compensating activity undoes the completed steps | Arch v5 slide 26 |
| Saga step failure after the pivot | The step is retried until it succeeds; strict mode holds the pivot until the ledger confirms | Arch v5 slides 26 and 28 |

# 15. Security and supply chain

- Zero trust between services: mutual TLS with workload identity, authorisation by policy, deny by default (NIST SP 800-204 and 800-204A; Arch v5 slide 30).
- No personal data in events, workflow payloads or logs; the codec encrypts workflow payloads (Arch v5 slides 11 and 23).
- Secrets in Key Vault only; the pipeline scans for secrets and dependencies; the image is signed and its bill of materials is kept (NIST SP 800-204C and 204D; Arch v5 slide 30).
- Every service has its own login and its own schema, which is the data boundary (ADR-014).
- Partner traffic terminates in the DMZ partner gateway; the partner portal is FAPI 2.0 with MFA (Arch v5 slides 17 and 30).

# 16. Testing

| Level | What it proves | Runs |
|---|---|---|
| Unit | Domain logic and rule outputs against fixed facts | Every build |
| Component | The service against Testcontainers Kafka and PostgreSQL, the outbox and inbox included | Every build |
| Contract | OpenAPI, AsyncAPI and the activity contract jar against the published contract and its fake | Every build |
| Architecture | The boundary test: no cross-schema reference, no call chain, no PII in an event | Every build |
| Temporal replay | A recorded history replays without a non-determinism error | Every build |
| Integration | The real behaviour across two services against their contracts | Wave gate |
| End to end | A case journey through the services on the real topics and queues | Wave gate |
| NFR | Response time, rule latency, availability and volume at the stated load (NFR-008 to NFR-011, NFR-020) | Before each release |
| Smoke | The daily journey smoke workflow PlatformSmokeWorkflow at 06:00 (JOB-22) | Daily, production |

Contract tests run in every build (Arch v5 slide 11), and the daily smoke workflow is the standing check that the 19 services still work together (Arch v5 slide 45).

# 17. Delivery and runtime shape

| Item | Rule | Basis |
|---|---|---|
| Deployments | Two per service: an API deployment with 2 pods for availability, and a worker deployment | Arch v5 slide 33 |
| Scaling | The API scales on CPU or requests if ever needed; the worker scales by KEDA on the Temporal queue backlog or Kafka consumer lag, down to zero for bursty work | Arch v5 slides 24 and 33 |
| Chart | One Helm chart for all 19 services, with one values file per service and per environment. Chart name and release naming: Not specified in the source documents (GAP-0136; ASM-0214) | Arch v5 slide 38 |
| Pipeline | One golden pipeline template that every service includes: build, test, scan, migrate, deploy, smoke. Pipeline tool and stage names: Not specified in the source documents (GAP-0139; ASM-0217) | Arch v5 slide 38 |
| Environments | The same chart and the same pipeline in every environment; only values differ | Arch v5 slide 29 |
| Rollback | Redeploy the previous tag | NFR-027 |
| Footprint | About 38 small deployments at rest for the 19 services, most workers idle at minimum | Arch v5 slide 33 |

# 18. Definition of Done for a service

A service is done when every line below is true. Items 1 to 12 follow the template; items 13 to 15 are the service-specific facts.

| # | Done when |
|---|---|
| 1 | The service is generated from the template at a pinned version and differs only in its package segment, its contracts and its own tables |
| 2 | The OpenAPI 3.1, AsyncAPI 3.0 and activity contract jar are published, with a fake for each |
| 3 | The schema, the login and the Flyway baseline exist; the boundary test passes |
| 4 | The outbox relay and the inbox dedupe are wired and tested |
| 5 | The Temporal worker polls only `rwb-<short>` and the workflows replay without error |
| 6 | The rules are evaluated in an activity, under 300 ms, with the package version recorded |
| 7 | Every decision writes a hash-linked record and publishes DecisionRecorded |
| 8 | Authorisation is enforced per object through the guard, and masking follows the policy |
| 9 | Traces, metrics, logs, /health and /metrics are live; the standard dashboard and alerts exist |
| 10 | The run book exists for every scheduled job |
| 11 | The Helm values and the pipeline include exist for every environment |
| 12 | The service appears in the Service Catalog v1 with its code, schema, base, topic, queue and package |
| 13 | The CON contract story of the service epic is done before any build story starts |
| 14 | No business value is in code; parameters, reference data and rules are data |
| 15 | No personal data is in an event, a workflow payload or a log |

# 19. Instantiating a service from the template

## 19.1 Steps

1. Take the service code and short name from the Service Catalog v1; generate every identifier from section 4.
2. Create the repository from the template at the pinned version; set the package segment.
3. Ask ACE DB for the schema and the login, and the PgBouncer pool with its cap.
4. Write `V0001`: the library tables of section 6.2 and the service's own tables from the Physical Schema.
5. Write the OpenAPI, AsyncAPI and activity contracts; publish the fakes.
6. Register the task queue `rwb-<short>` and the topic `rwb.<short>.events.v1` with its retry and dead-letter topics and ACLs.
7. Implement the domain, the workflows, the activities and the rules; keep every I/O in an activity.
8. Add the Helm values for each environment and include the golden pipeline.
9. Run the contract tests, the boundary test, the replay test and the smoke workflow.
10. Add the service to the conformance register in section 20.

## 19.2 The values for the 19 services

| Code | Service | Schema and login | REST base | Kafka topic | Task queue | Java package | Service epic |
|---|---|---|---|---|---|---|---|
| P1 | rwb-source-data | rwb_source_data | /api/recovery/source-data/v1 | rwb.source-data.events.v1 | rwb-source-data | th.co.scb.ace.workbench.recovery.sourcedata | RWB-SVC-P1 |
| P2 | rwb-integration | rwb_integration | /api/recovery/integration/v1 | rwb.integration.events.v1 | rwb-integration | th.co.scb.ace.workbench.recovery.integration | RWB-SVC-P2 |
| P3 | rwb-case | rwb_case | /api/recovery/case/v1 | rwb.case.events.v1 | rwb-case | th.co.scb.ace.workbench.recovery.case | RWB-SVC-P3 |
| P4 | rwb-access | rwb_access | /api/recovery/access/v1 | rwb.access.events.v1 | rwb-access | th.co.scb.ace.workbench.recovery.access | RWB-SVC-P4 |
| P5 | rwb-document | rwb_document | /api/recovery/document/v1 | rwb.document.events.v1 | rwb-document | th.co.scb.ace.workbench.recovery.document | RWB-SVC-P5 |
| P6 | rwb-comms | rwb_comms | /api/recovery/comms/v1 | rwb.comms.events.v1 | rwb-comms | th.co.scb.ace.workbench.recovery.comms | RWB-SVC-P6 |
| P7 | rwb-decision | rwb_decision | /api/recovery/decision/v1 | rwb.decision.events.v1 | rwb-decision | th.co.scb.ace.workbench.recovery.decision | RWB-SVC-P7 |
| P8 | rwb-payment | rwb_payment | /api/recovery/payment/v1 | rwb.payment.events.v1 | rwb-payment | th.co.scb.ace.workbench.recovery.payment | RWB-SVC-P8 |
| P9 | rwb-reporting | rwb_reporting | /api/recovery/reporting/v1 | rwb.reporting.events.v1 | rwb-reporting | th.co.scb.ace.workbench.recovery.reporting | RWB-SVC-P9 |
| P10 | rwb-agent | rwb_agent | /api/recovery/agent/v1 | rwb.agent.events.v1 | rwb-agent | th.co.scb.ace.workbench.recovery.agent | RWB-SVC-P10 |
| S1 | rwb-valuation | rwb_valuation | /api/recovery/valuation/v1 | rwb.valuation.events.v1 | rwb-valuation | th.co.scb.ace.workbench.recovery.valuation | RWB-SVC-S1 |
| S2 | rwb-treatment | rwb_treatment | /api/recovery/treatment/v1 | rwb.treatment.events.v1 | rwb-treatment | th.co.scb.ace.workbench.recovery.treatment | RWB-SVC-S2 |
| S3 | rwb-guarantee | rwb_guarantee | /api/recovery/guarantee/v1 | rwb.guarantee.events.v1 | rwb-guarantee | th.co.scb.ace.workbench.recovery.guarantee | RWB-SVC-S3 |
| S4 | rwb-litigation | rwb_litigation | /api/recovery/litigation/v1 | rwb.litigation.events.v1 | rwb-litigation | th.co.scb.ace.workbench.recovery.litigation | RWB-SVC-S4 |
| S5 | rwb-asset | rwb_asset | /api/recovery/asset/v1 | rwb.asset.events.v1 | rwb-asset | th.co.scb.ace.workbench.recovery.asset | RWB-SVC-S5 |
| S6 | rwb-debtsale | rwb_debtsale | /api/recovery/debtsale/v1 | rwb.debtsale.events.v1 | rwb-debtsale | th.co.scb.ace.workbench.recovery.debtsale | RWB-SVC-S6 |
| S7 | rwb-writeoff | rwb_writeoff | /api/recovery/writeoff/v1 | rwb.writeoff.events.v1 | rwb-writeoff | th.co.scb.ace.workbench.recovery.writeoff | RWB-SVC-S7 |
| S8 | rwb-deviation | rwb_deviation | /api/recovery/deviation/v1 | rwb.deviation.events.v1 | rwb-deviation | th.co.scb.ace.workbench.recovery.deviation | RWB-SVC-S8 |
| S9 | rwb-partner | rwb_partner | /api/recovery/partner/v1 | rwb.partner.events.v1 | rwb-partner | th.co.scb.ace.workbench.recovery.partner | RWB-SVC-S9 |

# 20. Conformance register

The register tracks each service against the template. Deviations are the parts a service does not use because its own contract needs something else; they are listed, not hidden. All entries are Draft in this version.

| Code | Service | Wave | Template parts | Deviations | Status |
|---|---|---|---|---|---|
| P1 | rwb-source-data | 1 | 12 of 12 | SQL view access to the 30 recovery.v_ace_* views as the only reader (ADR-010) | Draft |
| P2 | rwb-integration | 1 | 12 of 12 | File gateway: the only service that moves bulk files and manifests | Draft |
| P3 | rwb-case | 1 | 12 of 12 | Parent workflow host, case router and the case list read model | Draft |
| P4 | rwb-access | 1 | 12 of 12 | Reference-data owner for access; no events consumed | Draft |
| P5 | rwb-document | 1 | 12 of 12 | Blob WORM storage for documents; OCR pipeline | Draft |
| P6 | rwb-comms | 1 | 12 of 12 | ACE Common notification path (SMS, LINE); WIN letters through P2 | Draft |
| P7 | rwb-decision | 1 | 12 of 12 | Central decision ledger, rule package registry and WORM daily seal | Draft |
| P8 | rwb-payment | 2 | 12 of 12 | Posting file through P2; saga steps for the route services | Draft |
| P9 | rwb-reporting | 1 | 12 of 12 | Event projections and regulatory extracts; no data lake | Draft |
| P10 | rwb-agent | 1 | 12 of 12 | Tool gateway to P1 and P5, and the private enterprise AI endpoint | Draft |
| S1 | rwb-valuation | 3 | 12 of 12 | Route decision under D6; rule package version in the record | Draft |
| S2 | rwb-treatment | 2 | 12 of 12 | Nexus call to the ACE restructure calculator | Draft |
| S3 | rwb-guarantee | 3 | 12 of 12 | None | Draft |
| S4 | rwb-litigation | 3 | 12 of 12 | Long-running workflow with Continue-As-New over years | Draft |
| S5 | rwb-asset | 2 | 12 of 12 | Re-appraisal schedule and the LED auction ladder | Draft |
| S6 | rwb-debtsale | 3 | 12 of 12 | Saga with the transfer as the pivot; buyer file through P2 | Draft |
| S7 | rwb-writeoff | 4 | 12 of 12 | Committee approval through P7; monthly scan schedule | Draft |
| S8 | rwb-deviation | 2 | 12 of 12 | Stage clock pause while the deviation is open | Draft |
| S9 | rwb-partner | 4 | 12 of 12 | Partner gateway and FAPI 2.0 partner portal | Draft |

# 21. Open points

| ID | Point | Effect in this specification | Owner role |
|---|---|---|---|
| GAP-0134 | The stack versions are not pinned in any source read for this work package: Spring Boot, the Java runtime, the base image, the PostgreSQL driver and the Drools runtime | Section 2 and section 17 carry the placeholder Not specified in the source documents (GAP-0134; ASM-0212) | Platform team |
| GAP-0135 | The repository name and its location are not fixed; the sources state one repository per service and nothing more | Section 3.1 carries the placeholder Not specified in the source documents (GAP-0135; ASM-0213) | Platform team |
| GAP-0136 | The Helm chart name, the release naming and the container registry are not fixed | Section 4 and section 17 carry the placeholder Not specified in the source documents (GAP-0136; ASM-0214) | Platform team |
| GAP-0138 | Architecture v5 slide 20 names a decision_record table in every service schema; the Ownership Map v1 has no row for it | Section 6.2 carries the placeholder Not specified in the source documents (GAP-0138; ASM-0216) | Solution architect |
| GAP-0139 | The pipeline tool and its stage names are not fixed; the sources state one golden pipeline template and nothing more | Section 17 carries the placeholder Not specified in the source documents (GAP-0139; ASM-0217) | DevOps team |
| GAP-0140 | No earlier Service Template Specification exists, so v1 carries no inherited IDs, numbers or dates | Version 1, status Draft | Delivery lead |

The full text of every gap and assumption is in the Gap Register and the Assumptions Register (folder 23).

# 22. Change log

| Version | Date | Change | Detail |
|---|---|---|---|
| 1 | 22 November 2026 | D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash | First Service Template Specification: the twelve template parts, the repository layout, naming, data, REST, event, Temporal, rules, decision record, access, observability, resilience, security, testing, delivery, the Definition of Done and the instantiation checklist for the 19 services. |

