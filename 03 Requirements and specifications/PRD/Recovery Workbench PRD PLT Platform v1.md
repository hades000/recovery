SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

---
title: Recovery Workbench PRD PLT Platform
description: Product requirements for the Recovery Workbench platform (PLT) under D-RCV-60 - the service template and repositories, the shared libraries, the Temporal workflow platform, the ACE database schemas and logins, the Kafka event platform, the edge and gateway, and the observability baseline that the 19 services are built on in wave 0.
status: Draft
brd: 03 Requirements and specifications/Recovery Workbench Business Requirements Program v5.docx
version: 1
date: 22 November 2026
decision: D-RCV-60
service: PLT platform
service_epic: RWB-PLT-TPL, RWB-PLT-LIB, RWB-PLT-WF, RWB-PLT-DB, RWB-PLT-EVT, RWB-PLT-EDGE, RWB-PLT-OBS
wave: 0
---

# Recovery Workbench PRD PLT Platform

## 1. Document control and change log

### 1.1 Document control

| Attribute | Value |
|---|---|
| Document title | Recovery Workbench PRD PLT Platform |
| Document ID | PLT-RWB-PRD-v1 |
| Version | 1 |
| Status | Draft |
| Classification | Confidential |
| Date | 22 November 2026 |
| Service | The shared platform of the Recovery Workbench: seven platform epics, wave 0, outside the 19 services |
| Service epics | RWB-PLT-TPL, RWB-PLT-LIB, RWB-PLT-WF, RWB-PLT-DB, RWB-PLT-EVT, RWB-PLT-EDGE, RWB-PLT-OBS |
| Realignment decision | D-RCV-60 |
| Business baseline | Recovery Workbench Business Requirements Program v5 (22 November 2026), sections 6.1 to 6.12 (the 78 non-functional requirements), 7 (constraints), 8 (release plan) and 10 (delivery model) |
| Business baseline, business requirements served | Program v5 section 5, read through the Ownership Map: REQ-DRI-001 to REQ-DRI-008, REQ-DRI-010, REQ-DRI-011, REQ-ACA-003, REQ-ACA-005, REQ-ACA-006, REQ-ACA-007, REQ-ACA-009, REQ-ACA-012, REQ-CWC-006, REQ-CWC-011, REQ-CWC-013, REQ-CWC-014, REQ-CWC-016, REQ-RDF-001, REQ-RDF-010, REQ-DCM-002, REQ-DCM-003, REQ-OCC-007 |
| Functional baseline | No functional specification module exists for the platform; the FSD v6 set carries 19 module files and none for PLT (GAP-1664; ASM-2809). The platform behaviour is specified from Architecture v5, the Temporal and Drools Design v1 and the platform story set |
| Architecture baseline | Recovery Workbench Architecture v5 Text Extract v1 (slides 4, 7 to 11, 13, 20, 22 to 24, 29 to 36, 38 to 44, 49); Temporal and Drools Design Text Extract v1 (slides 11 to 13, 26 to 28); Ownership Map v1; Story Template and Rules v1; Non Functional Specification v3 |
| Structure | ISO/IEC/IEEE 29148, until the SCB X requirement template is adopted (DL13) |
| Tool and model | T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Prepared by | PRD Builder, AI-SDLC playbook |

### 1.2 Trace metadata

| Item | Value |
|---|---|
| Run | D-RCV-60 microservice realignment, folder 22 |
| Work package | B-REQ-PRD-PLT |
| Upstream artifacts | BRD Program v5; BRD Epic 1 v5; BRD Epic 2 v3; BRD Epics 3 to 8 v1; Arch v5 Text Extract v1; Temporal and Drools Design Text Extract v1; Non Functional Specification v3; Ownership Map v1 (ASM-2810) |
| Upstream ID sets | NFR-001 to NFR-078 (the 78 non-functional requirements of Program v5 section 6, delivered as non-functional work by the platform epics under ASM-2616); REQ-DRI-001 to REQ-DRI-008, REQ-DRI-010, REQ-DRI-011; REQ-ACA-003, REQ-ACA-005, REQ-ACA-006, REQ-ACA-007, REQ-ACA-009, REQ-ACA-012; REQ-CWC-006, REQ-CWC-011, REQ-CWC-013, REQ-CWC-014, REQ-CWC-016; REQ-RDF-001, REQ-RDF-010; REQ-DCM-002, REQ-DCM-003; REQ-OCC-007 |
| Legacy keys covered | RWB-E1-027, RWB-E1-037, RWB-E1-042, RWB-E1-043, RWB-E1-044, RWB-E1-047, RWB-E1-056, RWB-E1-070, RWB-E1-071, RWB-E1-072, RWB-TE-001 to RWB-TE-012, RWB-E2-037, RWB-E2-038, RWB-E2-039, RWB-E2-040, NF-01 to NF-08, N001 to N012 |
| Generated ID sets | CAP-PLT-001 to CAP-PLT-015; FR-PLT-001 to FR-PLT-034; NFR-PLT-001 to NFR-PLT-018; AC-PLT-001 to AC-PLT-025; Q-PLT-01 to Q-PLT-11 |
| Source artifact | 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; 22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md; Recovery Workbench Microservice Ownership Map v1.xlsx (ASM-2811) |
| Status | Draft; approval gate open |

### 1.3 Change log

| Version | Date | Change | Decision | Tool |
|---|---|---|---|---|
| 1 | 22 November 2026 | First version. The platform PRD is derived from BRD Program v5 sections 6, 7, 8 and 10, the business requirements the platform mechanisms serve, Architecture v5 slides 4 to 44 and 49, the Temporal and Drools Design slides 11 to 13 and 26 to 28, and the Ownership Map, under D-RCV-60 microservice realignment. Seven platform epics deliver, in wave 0, the service template and repositories, the shared libraries, the Temporal workflow platform, the 19 ACE schemas and logins, the Kafka event platform, the edge and gateway, and the observability baseline; the 19 services then arrive in waves 1 to 4 on that platform. The requirements are stated as product behaviour: what every service, every operator and every auditor can rely on, with no design beyond the constraints Architecture v5 confirms. | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |

### 1.4 Requirement ID conventions

| Prefix | Meaning | Example |
|---|---|---|
| CAP-PLT-nnn | Product capability of the platform | CAP-PLT-001 |
| FR-PLT-nnn | Functional requirement; mapped to the FSD requirement it serves where one exists, and to the business requirement or non-functional requirement it serves | FR-PLT-001 |
| NFR-PLT-nnn | Non-functional requirement; mapped to the BRD NFR IDs | NFR-PLT-001 |
| AC-PLT-nnn | Acceptance criterion in Gherkin, mapped to FR and NFR | AC-PLT-001 |
| Q-PLT-nn | Open question | Q-PLT-01 |
| BR IDs | Business requirement IDs of the BRD, copied unchanged | REQ-DRI-007 |
| NFR IDs | Non-functional requirement IDs of BRD Program v5 section 6, copied unchanged | NFR-068 |
| CG and ASM | Candidate gap and assumption rows of this work package, numbered later as GAP-nnnn and ASM-nnnn | GAP-1664 |

Four conventions govern the identifiers of this file.

- No BRD requirement is renumbered, and no BRD NFR is renumbered (ASM-2807).
- There is no predecessor PRD in the PLT family, so this file is version 1 (GAP-1665; ASM-2808).
- The FSD v6 set has no module for the platform, so a platform capability has no FSD requirement ID of its own; its functional requirements name the FSD requirement of the module the platform mechanism serves where that requirement states the behaviour, and the BRD non-functional requirement that sets its target (GAP-1664; ASM-2809).
- The BRD carries no platform business requirement: BRD Program v5 section 11 states that the 78 non-functional requirements are not business requirements and are delivered as non-functional work by RWB-ITG-NFR and by the platform epics (ASM-2616). The BR column of section 6 therefore names the business requirement the mechanism serves and the non-functional requirement it meets, and Appendix A.2 reports coverage against both.

## 2. Product overview and relationship to ACE

### 2.1 What the platform is

The Recovery Workbench platform is the shared layer that the 19 services are built and run on. It is not a service: it owns no business data, serves no business screen and decides nothing. It provides seven things, once, in wave 0:

- a service template and a set of repositories, so that a new service starts complete and compliant instead of being assembled by hand;
- a set of shared libraries, so that the outbox, the inbox, the idempotency key, the problem envelope, the decision record, the feature flag, the parameter and reference-data clients and the authorisation guard are written once and behave the same in 19 services;
- a Temporal workflow platform, so that a case, a stage, an approval and a job run as durable workflows on one cluster, in one namespace, with one versioned workflow kit;
- 19 schemas and 19 logins in the ACE database, so that each service owns its data and no service can read another's;
- the Kafka event platform, so that a fact published by one service reaches every consumer once, in order per case, with a retry path and a dead-letter path;
- the edge, so that a person reaches the Workbench through one App Gateway and one gateway-bff, partners reach only the partner gateway, and the bank's Airflow reaches the platform at its edges and nowhere else;
- the observability baseline, so that one trace, one dashboard set and one alert route exist before the first service is deployed.

The product value is stated by the business requirements the platform makes achievable and by nothing else: a screen under two seconds, an alert inside fifteen minutes, a decision that cannot be written and therefore does not happen, an event that is never lost, a case that survives a worker restart, and an audit that can reproduce any decision from the versions recorded with it. Architecture v5 puts the case for the shape in one line: build the platform pieces once, then every epic adds only its own services, so nothing is built twice (slide 38).

### 2.2 What is new under D-RCV-60

| New | Detail |
|---|---|
| Seven platform epics, as a wave of their own | RWB-PLT-TPL, RWB-PLT-LIB, RWB-PLT-WF, RWB-PLT-DB, RWB-PLT-EVT, RWB-PLT-EDGE and RWB-PLT-OBS deliver in wave 0, before EP01, and the 19 service epics arrive on top of them in waves 1 to 4 (Arch v5 slide 38; BRD Program v5 section 10.3; Story Template and Rules R5.1) |
| The platform is outside the 19 services | The shared pieces are not counted in the 19: gateway-bff with Redis session, the shared Temporal layer, the Kafka business-event topics, the bank's Airflow scheduler and the observability stack (Arch v5 slide 4) |
| One template, one chart, one pipeline | Every service is generated from one template (Spring Boot, outbox relay, inbox, Temporal worker, codec, OpenTelemetry, contract tests), deployed by one Helm chart and built by one golden pipeline (Arch v5 slides 20, 33 and 38) |
| One schema and one login per service | 19 schemas and 19 logins on the ACE PostgreSQL server, each with grants on its own schema only, a capped connection pool per service, a migrator role and a grant check (Arch v5 slides 29, 34 and 39; ADR-014; DP-01, DP-02, DP-15) |
| One event platform | A topic `rwb.<short>.events.v1` per service, CloudEvents 1.0 in binary mode, a JSON Schema registry with BACKWARD compatibility, retry topics and a dead-letter topic, transactional outbox in the producer and an inbox in every consumer (Arch v5 slides 11 and 22; ADR-015; DP-09, DP-14) |
| One workflow platform with a versioned kit | One Temporal cluster per environment, namespace `rwb-recovery` with its own retention, quotas, certificates and codec keys, and the L3 workflow kit of generic templates that carries no business term in its interface (Arch v5 slides 23 and 24; ADR-016; DP-10) |
| One edge and two doors | gateway-bff composes the staff screens one hop from the owner service, and partners reach the Workbench only through the partner gateway in the DMZ under FAPI 2.0 (Arch v5 slides 8, 10, 20 and 35; ADR-019; DP-19) |
| One observability baseline | OpenTelemetry with W3C Trace Context across REST, Kafka and Temporal, one dashboard set and one alert route inherited by every service, with the stuck-workflow scan and the smoke workflow owned by the platform (Arch v5 slides 8, 44 and 49; ADR-023) |
| No shared scheduler table and no data lake | No ACE Quartz table is used: a job is a Temporal Schedule or an event-started workflow in its owning service, and the bank's Airflow runs only the cross-system edges; INT-19 and INT-20 are removed (Arch v5 slides 31, 32, 37 and 44; ADR-016, ADR-018; DP-17) |

### 2.3 What is reused from ACE and from the platform

| Reused capability | Owner | Effect on this PRD |
|---|---|---|
| AKS cluster, Azure App Gateway with WAF, path routing `/recovery/*` and `/api/recovery/*` | ACE platform team | The edge is a route on a shared gateway, not a new front door; no platform requirement creates a second cluster or a second App Gateway (Arch v5 slides 7 and 8) |
| ACE Common sign-in (Entra ID, MFA) and the shared gateway-bff entry | ACE team | The edge obtains the short-lived user JWT per request and never exposes it to the browser; no platform requirement builds a sign-in (Arch v5 slides 20 and 30) |
| ACE Common audit and PII logging to SOC over the PII Kafka path | ACE team | Every service writes audit and personal-data access logs through that path; the platform supplies the instrumentation, not the path (Arch v5 slides 8, 30 and 35) |
| ACE PostgreSQL server, its backup, its recovery point and recovery time | ACE team and DBA | The platform creates 19 schemas and 19 logins in the existing server; the platform inherits the ACE recovery objectives (NFR-022, NFR-023; Arch v5 slide 29) |
| Azure Key Vault, Blob storage with WORM, MFT/SFTP with PGP | Platform and SCB IT infrastructure | The platform provisions the standard resources once; no service creates its own vault, container or transfer path (Arch v5 slides 8, 22 and 35; NFR-052, NFR-053) |
| The bank's Kafka platform (fallback: Azure Event Hubs Kafka endpoint) | Enterprise Architecture and ACE platform team | Recovery's business-event topics are hosted with separate topics and ACLs from the PII path; the hosting decision is open (Arch v5 slide 39; Q-PLT-06) |
| The bank's Airflow scheduler, replacing Control-M | Bank platform team | Airflow runs the overnight chain, the file windows and the extracts and calls service APIs only; per-case work stays in Temporal (Arch v5 slides 31, 32 and 44; NF-07) |
| Parameters and reference data | P3 rwb-case | The platform publishes the client libraries; the parameter rows and reference tables stay P3's (DP-06, DP-07; Ownership Map, Parameters sheet) |
| Role, scope, masking and DoA data | P4 rwb-access | The platform publishes the guard library; the policy rows and the access log stay P4's (DP-08; REQ-ACA-003) |
| Rule registry, approvals and the central decision ledger | P7 rwb-decision | The platform publishes the decision-record library and the embedded rules kit; the registry, the ledger and the approval engine stay P7's (DP-03, DP-04; ADR-017, ADR-022) |
| Rule packages, prompts and model versions | P7 rwb-decision, P10 rwb-agent | The kit loads a versioned rule package from P7; the agent runtime stays P10's (DP-04; Arch v5 slide 16) |

### 2.4 Confirmed constraints from Architecture v5

| Constraint | Source |
|---|---|
| 19 services inside one ACE platform, one ACE database and one front end; the shared platform pieces are not counted in the 19 | Arch v5 slides 2 and 4; ADR-013; D-RCV-60 |
| Schema `rwb_<name>` and login per service, grants on the own schema only, no cross-schema access, capped pools | Arch v5 slides 29, 34, 39 and 41; ADR-014; DP-01, DP-02 |
| REST: OpenAPI 3.1, `/api/recovery/<short>/v1` behind gateway-bff, one hop, 2 s timeout, breaker per downstream, `Idempotency-Key` on every POST, RFC 9457 problem details | Arch v5 slides 11 and 20; ADR-020; DP-11, DP-13 |
| Kafka: CloudEvents 1.0 binary mode, JSON Schema registry with BACKWARD compatibility, retry topics 1 min / 10 min / 1 h then `.dlt`, topic ACLs per service, outbox and inbox | Arch v5 slides 11, 22 and 35; ADR-015; DP-09, DP-14 |
| Temporal: one cluster per environment on ACE AKS, version 1.30 or later, namespace per workbench with own retention, quotas, certificates and codec keys, task queue `rwb-<short>`, payload codec AES-GCM with keys in Key Vault, 30-day retention of closed histories, search attributes CaseId, Stage, ProductGroup and QueueCode | Arch v5 slides 23, 24, 33 and 44; Temporal and Drools Design slides 11, 12 and 27; ADR-016 |
| Schedules replace Quartz; the platform owns the stuck-workflow scan (JOB-21, every 5 minutes) and the smoke workflow (JOB-22, 06:00) on task queue `rwb-platform` | Arch v5 slide 44; Ownership Map, Jobs sheet; DP-10 |
| Edge: shared App Gateway with WAF, gateway-bff with Redis session and a 15-minute idle timeout, partner gateway in the DMZ under FAPI 2.0, no business data at the edge | Arch v5 slides 8, 10, 20 and 35; ADR-019; DP-19 |
| Airflow runs the cross-system chain, the file windows and the extracts, calls service APIs only and never reads or writes an `rwb_*` schema | Arch v5 slides 31, 32 and 44; NF-07 |
| No data lake, no Power BI connection; INT-19 and INT-20 removed | Arch v5 slides 7, 8, 13, 37 and 51; ADR-018; DP-17 |
| OpenTelemetry with W3C Trace Context, one trace across services, events and workflows; ADR-023 | Arch v5 slides 8, 35 and 49; NFR-064 |
| Standards applied: BIAN v14, microservices.io patterns, NIST SP 800-204 to 204D, OWASP API Security Top 10 (2023), FAPI 2.0, OpenAPI 3.1, AsyncAPI 3.x, CloudEvents 1.0, OpenTelemetry, DMN 1.6 | Arch v5 slide 49 |

### 2.5 Exclusions of this PRD

| Excluded | Reason and later home |
|---|---|
| Any business capability: a case, a queue, a task, a document, a notice, a payment, a route decision, a deviation, a treatment, a write-off, an agent answer | Owned by the 19 services; the platform supplies the mechanism and owns no business object (DP-01; Ownership Map, Services sheet) |
| The parameter catalog, the reference tables, the rule registry, the central decision ledger, the approval engine and the DoA table | P3 rwb-case, P7 rwb-decision and P4 rwb-access; the platform publishes the client libraries only (BRD Program v5 section 10.5) |
| The business screens and their layout | The ACE front end; the edge composes the screen model and renders nothing (ASM-2822) |
| Environment names, sizing, tenancy and the per-environment subscription layout | Not in the source set; the Environment and Deployment Design v5 carries it (GAP-1668; Q-PLT-01) |
| Solution design: class names, table columns, endpoint signatures beyond the confirmed contract, module layout, deployment topology | Out of scope of a PRD; the technical specification and the story set carry it |
| The brand, colour and accessibility of the user interface | The front-end workbench; the platform carries the shell, the session and the internationalised message rule (NFR-PLT-017) |

## 3. Personas and roles

Roles only; no person is named anywhere.

| Role | Who | What they need from the platform |
|---|---|---|
| Platform administrator (RW-PLATADM) | Operations and platform team | Create a service, deploy it, switch a feature flag, run the smoke workflow, read the platform dashboards, open the run book of a job |
| Platform engineer | Platform team | Own the template, the libraries, the workflow kit, the cluster, the topics and the dashboards baseline, and change them once for every service |
| DevOps engineer | DevOps team | One chart, one pipeline, one release path, a rollback by tag, a secret that is never in a file, a masked SIT and UAT |
| ACE database administrator | ACE team and DBA | 19 schemas and 19 logins, a migrator role, a capped pool per service, a grant check that fails a violation |
| Infrastructure engineer | SCB IT infrastructure | The Temporal namespace, the codec key, the Kafka topics and ACLs, the registry, Blob, Key Vault and the transfer paths, provisioned once |
| Service team member (TechX) | Any team picking up a service story | A template that starts complete, a contract with a fake, a boundary test, a library that already solves the outbox, the inbox and the decision record |
| Security administrator (RW-SECADM) | Second line | Deny by default, mTLS between services, topic ACLs, one login per schema, no secret in code, a signed evidence pack for the namespace |
| Audit and compliance reader (RW-AUDIT) | Second and third line | A decision record that cannot be written silently dropped, a hash chain checked daily, an access log, reproducible versions |
| Partner user | Agency, law firm, auction vendor, buyer | Reach only the partner gateway, only their own cases, with multi-factor authentication |
| Reporting and BI analyst | Data office | Events that carry the facts a projection needs, with no personal data, and a trace that shows where a measure came from |
| Business analyst | Business and delivery | The BOT approval position, the release the platform lands in, and the business release it unblocks |

## 4. User journeys

### 4.1 A new service, today and in the target

| Step | Today (monolith) | Target (platform) |
|---|---|---|
| 1 | A new module is a package inside one deployable, built with the same release as every other module | A team generates a service from the template and gets a repository, a chart, a pipeline, a contract skeleton and a green build on the first commit |
| 2 | The schema, the login and the grants are requested by hand and differ per module | The schema and login already exist from wave 0 with grants on that schema only, and the grant check proves it |
| 3 | The event path, the idempotency key and the error envelope are re-implemented or copied | The library supplies them, and the pipeline refuses a service that bypasses them |
| 4 | A breaking call is found in integration testing | The contract is published before the build, every consumer builds against its fake, and a breaking change raises a new version |

### 4.2 One event, from a state change to a consumer

| Step | What happens |
|---|---|
| 1 | A service writes its state change and its event in one transaction, so a failure leaves neither behind |
| 2 | The outbox relay publishes once a minute to the service topic as a CloudEvents 1.0 message, keyed by the case identifier |
| 3 | Each consumer records the event identifier in its inbox and applies the event once; a repeat is counted and dropped |
| 4 | A consumer that keeps failing moves the message through the retry topics to the dead-letter topic, and an alert reaches the owner of the consuming service |

### 4.3 A case action across the edge

| Step | What happens |
|---|---|
| 1 | The browser presents an opaque session cookie; the gateway resolves the session in Redis with a 15-minute idle timeout and obtains a short-lived user JWT through ACE Common |
| 2 | The gateway checks a coarse permission and calls the owner services in parallel, one hop each, with a 2 s timeout and a breaker per downstream |
| 3 | The gateway merges the answers into one screen model; object-level authorisation remains the owner's |
| 4 | One owner that fails to answer turns one tab into "temporarily unavailable" with 503 problem details, and the rest of the screen still loads |

### 4.4 A rule change, from the load to every service

| Step | What happens |
|---|---|
| 1 | The centre of excellence loads a rule package version in rwb-decision; the load checks refuse a package that fails a check, and the version in force keeps running |
| 2 | The package is promoted at 00:01 by the decision service's own Schedule and the promotion is published as `RulePackageInForce` |
| 3 | The embedded rules kit in each service refreshes its cached package and the next evaluation uses the new version, with no deployment |
| 4 | Every decision record names the rule ID and the rule version that produced it, and a faulty package rolls back to the previous version by one call |

### 4.5 A workflow that survives a worker stop, and a platform that does not lose a case

| Step | What happens |
|---|---|
| 1 | A worker stops mid-activity: the task stays on the task queue, the worker returns and the workflow resumes from its history |
| 2 | A call to ACE, to a partner or to the database fails: the activity retries on its policy with a 1 s initial interval and doubling, and a non-retryable failure stops at once |
| 3 | Temporal itself is down: running journeys pause and resume where they stopped, and the screens keep working |
| 4 | A workflow makes no progress for five minutes: the platform's stuck-workflow scan raises it to the owner role, and the smoke workflow proves the platform at 06:00 before the working day |

### 4.6 A flag that must be removed and a schema that must not be crossed

| Step | What happens |
|---|---|
| 1 | A feature ships switched off as a versioned flag row with an owner and a removal date |
| 2 | The platform administrator switches it on for one environment with a reason; the change is a row with old value, new value, user and time, and the audit path is written |
| 3 | A weekly report lists every flag past its removal date with its owner, so the old code path is removed rather than kept forever |
| 4 | A statement that reads another service's schema, or the recovery schema, fails the build, so the boundary is a check and not a habit |

## 5. Capabilities and features

A capability carries the highest priority among the requirements it traces to. Every platform capability is Must: each one is the mechanism a BRD non-functional requirement or a business requirement of the BRD needs in wave 0, and none of them is optional for the first service that is deployed. There is no Should, Could or Will-not capability in this PRD: a platform capability that is not built in wave 0 is a gap in the wave, not a later increment (ASM-2812).

| CAP | Capability | BR IDs | MoSCoW | Wave | FRs | Platform epic |
|---|---|---|---|---|---|---|
| CAP-PLT-001 | The service template and the module boundary: one generated service with the API and worker deployment, the outbox relay, the inbox, the Temporal worker, the payload codec, OpenTelemetry, the health and metrics endpoints, the contract-test harness and the boundary test | REQ-DRI-006; NFR-054, NFR-064 | Must | 0 | FR-PLT-001, FR-PLT-002 | RWB-PLT-TPL |
| CAP-PLT-002 | One golden pipeline, one Helm chart and one release path for every service, with code ownership and a rollback by previous tag | NFR-027, NFR-054 | Must | 0 | FR-PLT-003, FR-PLT-004 | RWB-PLT-TPL |
| CAP-PLT-003 | The migration, environment and secret baseline: one migration sequence per service with a parameterised schema name, the environment set, and secrets that never sit in code or a file | REQ-RDF-001; NFR-052 | Must | 0 | FR-PLT-005, FR-PLT-006, FR-PLT-007 | RWB-PLT-TPL |
| CAP-PLT-004 | Masked data in SIT and UAT, and the pipeline gate that refuses a secret, personal data in code, tests or logs, or an unapproved dependency | REQ-RDF-010, REQ-ACA-005; NFR-045, NFR-054 | Must | 0 | FR-PLT-008 | RWB-PLT-TPL |
| CAP-PLT-005 | Contract-first publication: OpenAPI 3.1 for REST, AsyncAPI 3.0 for events, an activity contract jar for Temporal, a fake per contract and a contract test in every build | REQ-DRI-007; NFR-054 | Must | 0 | FR-PLT-009 | RWB-PLT-TPL |
| CAP-PLT-006 | The messaging library: the transactional outbox, the inbox dedupe with the retry ladder and the dead-letter path, the idempotency key and the RFC 9457 problem envelope | REQ-DRI-006, REQ-DRI-007; NFR-025, NFR-059 | Must | 0 | FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013 | RWB-PLT-LIB |
| CAP-PLT-007 | The decision-record and audit kit: a local record in the same transaction as the state change, sealed on the shared decision-record topic, and the daily hash-chain check | REQ-DRI-001, REQ-DRI-002, REQ-DRI-003, REQ-DRI-004, REQ-DRI-005; NFR-033, NFR-034, NFR-035 | Must | 0 | FR-PLT-014, FR-PLT-015 | RWB-PLT-LIB |
| CAP-PLT-008 | Feature flags with an owner and a removal date, the parameter and configuration client, and the reference-data client, all read in process and changed without a release | REQ-DRI-010, REQ-DRI-011, REQ-CWC-006 | Must | 0 | FR-PLT-016, FR-PLT-017, FR-PLT-018 | RWB-PLT-LIB |
| CAP-PLT-009 | The authorisation guard: every action checked against the rwb-access contract, deny by default, with the permission cache refreshed by the access events | REQ-ACA-003, REQ-ACA-005, REQ-ACA-006, REQ-ACA-007, REQ-ACA-009 | Must | 0 | FR-PLT-019 | RWB-PLT-LIB |
| CAP-PLT-010 | The embedded rules kit: a versioned rule package loaded from the owner's registry, evaluated inside the owning service's activity, with the load checks and the one-call rollback | REQ-CWC-011, REQ-CWC-013, REQ-CWC-014, REQ-CWC-016 | Must | 0 | FR-PLT-020 | RWB-PLT-LIB |
| CAP-PLT-011 | The Temporal platform: one cluster per environment, the namespace with its retention, quotas, certificates and codec key, the versioned workflow kit, durable timers and Schedules, the resilience rules, the workflow health jobs and the admin audit | REQ-DRI-007; NFR-025, NFR-027, NFR-053, NFR-068 | Must | 0 | FR-PLT-021, FR-PLT-022, FR-PLT-023, FR-PLT-024, FR-PLT-025, FR-PLT-026 | RWB-PLT-WF |
| CAP-PLT-012 | The ACE database baseline: 19 schemas and 19 logins, grants on the own schema only, a capped connection pool per service, a migrator role and a grant check that fails a violation | REQ-DRI-006; NFR-001, NFR-020 | Must | 0 | FR-PLT-027 | RWB-PLT-DB |
| CAP-PLT-013 | The Kafka event platform: a topic per service with retry and dead-letter topics and per-service ACLs, a registry with BACKWARD compatibility, and the standard Blob, Key Vault and transfer resources | REQ-DRI-007, REQ-DCM-002, REQ-DCM-003; NFR-025, NFR-029, NFR-053 | Must | 0 | FR-PLT-028, FR-PLT-029 | RWB-PLT-EVT |
| CAP-PLT-014 | The edge: gateway-bff with its public route surface, the Redis session and the composite screens, the partner gateway in the DMZ under FAPI 2.0, and the Airflow edge contract | REQ-OCC-007, REQ-ACA-012, REQ-DRI-008; NFR-008, NFR-009, NFR-050 | Must | 0 | FR-PLT-030, FR-PLT-031, FR-PLT-032 | RWB-PLT-EDGE |
| CAP-PLT-015 | The observability baseline: OpenTelemetry with W3C Trace Context across REST, Kafka and Temporal, the golden-signal dashboards, the alert rules with a named owner, and a run book for every job | NFR-064, NFR-067, NFR-068 | Must | 0 | FR-PLT-033, FR-PLT-034 | RWB-PLT-OBS |

### 5.1 Capabilities carried out of scope, with their source

| Removed or non-capability | Source and disposition |
|---|---|
| A `rwb_*` schema, a topic and a task queue for the platform itself | The platform is outside the 19: no row in the Ownership Map Services sheet, no `rwb.<short>.events.v1` topic and no `/api/recovery/<short>/v1` base; the library objects exist inside the service schemas (Arch v5 slides 4 and 41; ASM-2813) |
| A second App Gateway, a second cluster, or a cluster per workbench | The edge rides the shared App Gateway; a new workbench takes a namespace on the same Temporal cluster, not a second cluster (Arch v5 slides 7, 23 and 46) |
| The ACE Quartz scheduler and its shared job tables | Retired: a job is a Temporal Schedule or an event-started workflow in the owning service, and Airflow runs only the cross-system edges (Arch v5 slide 44; DP-10) |
| A data lake copy, the daily lake copy of the decision log and the Power BI connection | Removed by Architecture v5 (ADR-018; DP-17); the read model is built from events into rwb-reporting |
| The parameter rows, the reference tables, the rule registry, the ledger and the DoA table | They stay P3's, P7's and P4's; the platform publishes the client libraries only (BRD Program v5 section 10.5; Ownership Map, Parameters and Rulings sheets) |
| A model host, a model gateway or an agent runtime | P10 rwb-agent; the platform supplies the workflow kit template for an agent run with rule fallback (DP-04, DP-20) |
| An event-tracking or issue-register function inside the platform | No issue-tracker access in this run; the tracker impact sits in one separate file (Story Template and Rules U6) |
| The archive of closed workflow histories as a product feature | RWB-PLT-E2039 owns backup, archive and upgrade of the Temporal layer; this PRD requires the outcome (a closed history is archived before its retention removes it), not the mechanism (FR-PLT-024) |

## 6. Functional requirements

Every requirement is specific and testable. The BR column names the business requirement or the non-functional requirement of the BRD it serves; the FSD column names the FSD requirement of the module whose behaviour depends on the platform mechanism, and states where no FSD requirement exists.

| ID | Requirement | CAP | BR (BRD) | FSD source | Priority |
|---|---|---|---|---|---|
| FR-PLT-001 | The platform SHALL generate a new service from one template that contains, with no hand-written infrastructure, the API deployment and the worker deployment, the outbox relay, the inbox, the Temporal worker on its own task queue, the payload codec, the OpenTelemetry instrumentation, the health and metrics endpoints, the OpenAPI 3.1, AsyncAPI 3.0 and activity contract skeletons, the contract-test harness and the module boundary test; a generated service SHALL pass the boundary test and the pipeline on its first commit. | CAP-PLT-001 | NFR-054, NFR-064 | FSD P2 v3 A1.1 (REQ-DRI-006, REQ-DRI-007) | Must |
| FR-PLT-002 | The build SHALL fail a service whose code reads an ACE table or view directly, reads or writes another service's schema, carries a foreign key out of its own schema, or calls a second service from inside a request the gateway started; only rwb-source-data SHALL hold SELECT on the `recovery.v_ace_*` views, and the failure SHALL name the statement and the schema. | CAP-PLT-001 | REQ-DRI-006 | FSD P2 v3 A1.1 REQ-DRI-006; Arch v5 slide 29; DP-01, DP-05 | Must |
| FR-PLT-003 | The platform SHALL build and deploy every service from one golden pipeline and one versioned Helm chart, with two deployments per service (the API at two copies for availability and the worker scaled on its task-queue backlog or its consumer lag), SHALL apply a chart or pipeline change to every service by one release, and SHALL roll a release back by redeploying the previous tag. | CAP-PLT-002 | NFR-027, NFR-054 | No FSD requirement states the pipeline (GAP-1664; ASM-2809); Arch v5 slides 33 and 38 | Must |
| FR-PLT-004 | The platform SHALL hold the code owners of each service folder as data, SHALL refuse a change that no owner rule covers, and SHALL refuse a build that carries a secret, personal data in code, tests or logs, or a dependency that is not on the approved list. | CAP-PLT-002 | NFR-052, NFR-054 | FSD P2 v3 A1.1; Arch v5 slide 39; RWB-TE-002, RWB-TE-011 | Must |
| FR-PLT-005 | The platform SHALL run one migration sequence per service against the service's own schema, SHALL take the schema name as a parameter rather than as a literal, SHALL refuse a migration that names another schema, and SHALL leave the previous version in place when a migration fails; the built baseline of the monolith SHALL be kept as the first version of the sequence. | CAP-PLT-003 | REQ-RDF-001 | FSD P1 v3 A1.1 REQ-RDF-001; ADR-021; DP-15; RWB-E1-044 | Must |
| FR-PLT-006 | The platform SHALL provide the environment set that the services are deployed into, with the same chart parameters in every environment and the environment code as data, and SHALL refuse a deployment whose environment code is not on the list. | CAP-PLT-003 | NFR-045 | No FSD requirement states the environments (GAP-1668; ASM-2823) | Must |
| FR-PLT-007 | The platform SHALL hold every credential, certificate and key in the key store, SHALL deliver it to a workload through its managed identity, SHALL refuse a build or a manifest that carries a secret, and SHALL record the key version in force with the release evidence. | CAP-PLT-003 | NFR-052, NFR-053 | Arch v5 slides 8 and 35; NFR-052 | Must |
| FR-PLT-008 | The development environment SHALL hold synthetic data only and the user acceptance environment SHALL hold masked copies, and the pipeline SHALL run a personal-data scan over code, tests, fixtures and logs that fails the build on a party identifier, a name in clear or an account number in clear. | CAP-PLT-004 | REQ-RDF-010, REQ-ACA-005, NFR-045 | FSD P1 v3 REQ-RDF-010; FSD P4 v3 REQ-ACA-005; RWB-TE-004, RWB-TE-011 | Must |
| FR-PLT-009 | Every service SHALL publish, before its build starts, an OpenAPI 3.1 document for its REST resources under `/api/recovery/<short>/v1`, an AsyncAPI 3.0 document for its topic `rwb.<short>.events.v1`, an activity contract jar for its task queue `rwb-<short>` and a fake per contract, and the build SHALL run a contract test against each fake so that a consumer builds without the owner being finished; a name that departs from the naming rule SHALL fail the build. | CAP-PLT-005 | NFR-054 | FSD P2 v3 A1.1; Arch v5 slides 11 and 36; ADR-020; DP-11, DP-13, DP-14; RWB-TE-003 | Must |
| FR-PLT-010 | The library SHALL write a state change and its event in one transaction in the service's own schema, SHALL publish from the outbox at least once a minute on the service topic as a CloudEvents 1.0 message keyed by the case identifier, SHALL retry a failed publish, and SHALL leave no event unsent and no state change without its event. | CAP-PLT-006 | REQ-DRI-007, NFR-025 | FSD P2 v3 A1.1 REQ-DRI-007; Arch v5 slides 11, 20 and 44 (JOB-11); ADR-015; DP-09; RWB-TE-006 | Must |
| FR-PLT-011 | The library SHALL record each consumed event in the inbox of the consumer schema and SHALL apply an event once; a repeat SHALL be counted and dropped; a consumer that keeps failing SHALL move the message through the retry topics at 1 minute, 10 minutes and 1 hour to the dead-letter topic, and SHALL raise an alert to the owner role of the consuming service. | CAP-PLT-006 | REQ-DRI-006, NFR-025, NFR-068 | FSD P2 v3 A1.1 (duplicate handling); Arch v5 slides 11 and 22; ADR-015; DP-09 | Must |
| FR-PLT-012 | The library SHALL require an `Idempotency-Key` on every POST, SHALL return the stored answer to a repeated request with the same key and make no second state change, and SHALL reject a request that reuses a key with a different request body; the storage period of the stored answer SHALL be a configuration value and not a constant. | CAP-PLT-006 | REQ-DRI-007, NFR-025 | FSD P2 v3 A1.1; Arch v5 slide 11; RWB-PLT-N009 | Must |
| FR-PLT-013 | The library SHALL answer every REST error with one RFC 9457 problem envelope carrying type, title, status, detail and instance, SHALL pass the owner's message identifier and detail through the gateway unchanged, SHALL carry no business value and no personal data in the detail, and SHALL offer the title and the detail in Thai and in English. | CAP-PLT-006 | NFR-059, NFR-068 | Arch v5 slide 11; NFR-059; RWB-PLT-N009 | Must |
| FR-PLT-014 | The library SHALL write one local decision record in the same transaction as the action it records, SHALL carry the decision code, the subject reference, the rule, model, agent and prompt versions in force, the freshness of the data used and the action taken, SHALL seal the record on `rwb.decision-record.v1`, and SHALL refuse the action when the record cannot be written. | CAP-PLT-007 | REQ-DRI-001, REQ-DRI-002, REQ-DRI-004, REQ-DRI-005 | FSD P7 v3 REQ-DRI-001 to REQ-DRI-005; ADR-022; DP-03; RWB-E1-027 | Must |
| FR-PLT-015 | The kit SHALL provide the daily hash-chain check that reads the chain, reports a break to the Compliance role on the same business day, and records the result of the check with its business date and the count of records verified. | CAP-PLT-007 | REQ-DRI-003, NFR-035 | FSD P7 v3 REQ-DRI-003; NFR-035; RWB-TE-008; JOB-14 | Must |
| FR-PLT-016 | The platform SHALL hold every feature flag as a versioned row with its key, its description, its owner, its default value, its value per environment and a removal date; a flag SHALL be off when it has no value, SHALL be switchable without a deployment, SHALL write a change row with the old value, the new value, the user identifier and the time, and SHALL be listed in a removal report with its owner when its removal date has passed. | CAP-PLT-008 | REQ-DRI-010 | FSD P7 v3 REQ-DRI-010; Arch v5 slide 20; RWB-E1-047; Ownership Map ruling ASM-0073 | Must |
| FR-PLT-017 | The platform SHALL provide a parameter and configuration client that reads every threshold, limit, name and timer as a versioned row with valid-from and valid-to dates, the loader and the approver, SHALL use the version in force for the business date, SHALL answer from a local cache, and SHALL let a caller change a value through a validated load with no code release; no business value SHALL exist in code. | CAP-PLT-008 | REQ-DRI-010 | FSD P7 v3 REQ-DRI-010; DP-06; RWB-E1-042 | Must |
| FR-PLT-018 | The platform SHALL provide a reference-data client that reads every versioned list with its valid-from and valid-to dates, its author and its approver, SHALL answer from a local cache, SHALL refresh when a list version changes, and SHALL refuse a value that is not in force on the business date. | CAP-PLT-008 | REQ-DRI-011, REQ-CWC-006 | FSD P7 v3 REQ-DRI-011; FSD P3 v4 REQ-CWC-006; DP-07; RWB-E1-043 | Must |
| FR-PLT-019 | The guard SHALL check every action against the rwb-access contract for the acting role, its scope and its delegation limit, SHALL refuse and record a refusal when the policy does not allow the action, SHALL deny by default when no policy is cached, SHALL run a service identity under the same checks as a person, and SHALL refresh its permission cache on `AccessPolicyChanged`, `DoaLimitChanged` and `RulePackageInForce`. | CAP-PLT-009 | REQ-ACA-003, REQ-ACA-005, REQ-ACA-006, REQ-ACA-007, REQ-ACA-009 | FSD P4 v3 REQ-ACA-003 to REQ-ACA-009; Arch v5 slides 20 and 35; DP-08; RWB-E1-037 | Must |
| FR-PLT-020 | The rules kit SHALL evaluate a decision inside the owning service's activity from the rule package version in force, SHALL hold no rule in code, SHALL refuse a package that fails a load check (schema, overlapping rows, unreachable rows, a missing default row, the stated test scenarios and a dry run), SHALL keep the version in force running when a new load is refused, and SHALL record the rule ID and the rule version on every decision it produces. | CAP-PLT-010 | REQ-CWC-011, REQ-CWC-013, REQ-CWC-014, REQ-CWC-016 | FSD P3 v4 REQ-CWC-013, REQ-CWC-014, REQ-CWC-016; ADR-017; DP-04; RWB-E1-072 | Must |
| FR-PLT-021 | The platform SHALL run one Temporal cluster per environment on the ACE AKS cluster at version 1.30 or later, SHALL hold the namespace `rwb-recovery` with its own retention, rate limits, certificates and encryption key, SHALL keep 30 days of closed history, SHALL expose the four search attributes CaseId, Stage, ProductGroup and QueueCode, and SHALL refuse a namespace call made with a certificate of another namespace. | CAP-PLT-011 | NFR-020, NFR-021, NFR-053 | No FSD requirement states the cluster (GAP-1664); Arch v5 slides 23, 24 and 39; Temporal and Drools Design slides 11, 12 and 27; RWB-E1-070, RWB-PLT-N003 | Must |
| FR-PLT-022 | The platform SHALL provide one versioned workflow kit of generic templates with no business term in their interfaces, covering approval with the delegation lookup as a parameter, notification, document intake, agent run with rule fallback, human task with service-level timers, saga runner, scheduled job and partner instruction, SHALL version the kit with semantic versioning, and SHALL pin a worker version per deployment so that an upgrade cannot change a running journey. | CAP-PLT-011 | REQ-CWC-011, NFR-025 | FSD P3 v4 REQ-CWC-011; Arch v5 slides 23, 24 and 36; ADR-016; DP-12 | Must |
| FR-PLT-023 | The platform SHALL replace the shared scheduler table: a scheduled job SHALL be a Temporal Schedule with an overlap policy and a catch-up window in the owning service, a journey SHALL use durable timers inside its workflow, and the platform SHALL provide no shared job table and no five-minute timer check. | CAP-PLT-011 | REQ-CWC-011, NFR-067 | FSD P3 v4 REQ-CWC-011; Arch v5 slide 44 (JOB-05, JOB-06, JOB-16, JOB-20, JOB-22); ADR-016; DP-10 | Must |
| FR-PLT-024 | The platform SHALL retry an activity on its stated policy with a 1 s initial interval and doubling up to 10 attempts, SHALL stop at once on a non-retryable failure such as no rule version in force, SHALL back up the Temporal persistence, SHALL support a failover and an upgrade without losing a running journey, SHALL archive a closed history before its retention removes it, and SHALL run a replay test gate before a workflow change reaches production. | CAP-PLT-011 | NFR-025, NFR-027 | Arch v5 slide 34; Temporal and Drools Design slide 28; ADR-016; RWB-E2-039, RWB-E2-040 | Must |
| FR-PLT-025 | The platform SHALL run the stuck-workflow scan every five minutes on task queue `rwb-platform` and raise an alert with the workflow identifier, the type and the last event time when a workflow makes no progress, SHALL run the smoke workflow at 06:00 and report one trace across the edge and the workflow, and SHALL encrypt every payload through the codec with AES-GCM and a key held in the key store. | CAP-PLT-011 | NFR-053, NFR-068 | Arch v5 slides 24, 44 (JOB-21, JOB-22); NFR-068; RWB-PLT-N005 | Must |
| FR-PLT-026 | The platform SHALL authenticate every Temporal client and worker with mutual TLS and a workload identity per service, SHALL record every administrative action on the namespace with the actor, the action and the time, and SHALL grant decode rights on a history to the audit role only under a recorded break-glass approval. | CAP-PLT-011 | REQ-ACA-006, NFR-042, NFR-051 | FSD P4 v3 REQ-ACA-006; Arch v5 slide 35; RWB-E2-038 | Must |
| FR-PLT-027 | The platform SHALL create 19 schemas and 19 logins in the ACE database, one per service, SHALL grant each login on its own schema only, SHALL cap the connection pool of each service so that Recovery cannot starve ACE, SHALL provide a migrator role separate from the runtime login, and SHALL run a grant check that fails and reports when any login can reach a schema that is not its own. | CAP-PLT-012 | REQ-DRI-006, NFR-001, NFR-020 | FSD P2 v3 A1.1 REQ-DRI-006; Arch v5 slides 29, 34, 39 and 41; ADR-014; DP-01, DP-02; NF-06, RWB-PLT-N011 | Must |
| FR-PLT-028 | The platform SHALL create for every service a topic `rwb.<short>.events.v1` with its retry topics and its dead-letter topic, with per-service ACLs, a registry that accepts only a BACKWARD-compatible schema change, and a producer configured for idempotence with all replicas acknowledged; the PII logging path SHALL be a separate topic with separate ACLs. | CAP-PLT-013 | REQ-DRI-007, NFR-025 | FSD P2 v3 A1.1 REQ-DRI-007; Arch v5 slides 11, 22 and 39; ADR-015; DP-09, DP-14; RWB-PLT-N002, RWB-PLT-N008 | Must |
| FR-PLT-029 | The platform SHALL provide the standard resources once for every service: a Blob container with a write-once policy for the legal document types, a key store for credentials and keys, and the managed file transfer path with encryption for an outside party, with a manifest carrying the file identifier, the batch identifier, the checksum and the record count, and never the data in the message. | CAP-PLT-013 | REQ-DCM-002, REQ-DCM-003, NFR-029, NFR-053 | FSD P5 v3 REQ-DCM-002, REQ-DCM-003; Arch v5 slides 11 and 22; RWB-PLT-N012 | Must |
| FR-PLT-030 | The edge SHALL serve the staff screens from one gateway behind the shared App Gateway, SHALL resolve an opaque session cookie in Redis with a 15-minute idle timeout, SHALL obtain a short-lived user JWT per request through ACE Common sign-in and never expose it to the browser, SHALL call each owner service once and in parallel with a 2 s timeout and a breaker per downstream, SHALL merge the answers into one screen model, SHALL check a coarse permission only and leave object-level authorisation with the owner, and SHALL answer 401, 403, 404 and 503 with the problem envelope so that one failing owner degrades one tab and no other. | CAP-PLT-014 | REQ-OCC-007, NFR-008, NFR-009 | FSD P6 v3 REQ-OCC-007; Arch v5 slides 8, 10 and 20; ADR-019, ADR-020; DP-19; RWB-PLT-N001 | Must |
| FR-PLT-031 | The platform SHALL route every partner user through the partner gateway in the DMZ and never through the staff gateway, SHALL authenticate the partner with multi-factor authentication and a sender-constrained token under FAPI 2.0, SHALL scope the partner to its own cases, and SHALL refuse a partner request that reaches a staff route. | CAP-PLT-014 | REQ-ACA-012, NFR-050 | FSD P4 v3 REQ-ACA-012; Arch v5 slides 8, 20 and 35; ADR-019; RWB-PLT-N007 | Must |
| FR-PLT-032 | The platform SHALL publish the Airflow edge contract: the ingestion DAG's last task calls the source-data business-date endpoint once per business date and receives an accepted answer, a sensor reads the status of that date, the file windows and the report extract are triggered by Airflow, and Airflow SHALL call service APIs only and never read or write an `rwb_*` schema. | CAP-PLT-014 | REQ-DRI-008, NFR-013, NFR-019 | FSD P2 v3 REQ-DRI-008; Arch v5 slides 31, 32 and 44; RWB-PLT-NF07 | Must |
| FR-PLT-033 | The platform SHALL produce one trace per user action across the edge, the owner service, the event and the workflow, using W3C Trace Context propagated through REST, the Kafka headers and the Temporal context, SHALL produce metrics and logs for every service with the service as a resource attribute, and SHALL scrub personal data before export so that no trace, metric label or log line carries a party identifier, a name or a document value. | CAP-PLT-015 | NFR-064, NFR-039, NFR-042 | FSD P4 v3 REQ-ACA-006; Arch v5 slides 8, 35 and 49; ADR-023; NFR-064 | Must |
| FR-PLT-034 | The platform SHALL provide the dashboard set, the alert rules and the run book catalogue before the first service reaches SIT, SHALL route every alert to the owner role of the failing piece with its message identifier, SHALL raise the alert inside 15 minutes of the failure, and SHALL fail a deployment of a service that carries no run book entry for each of its jobs. | CAP-PLT-015 | NFR-067, NFR-068 | Arch v5 slides 8, 44 and 49; NFR-067, NFR-068; RWB-E1-056, RWB-PLT-N005 | Must |

### 6.1 Business rules that qualify the requirements

| BR ID | Rule | Source |
|---|---|---|
| BR-PLT-001 | No value a business person may change is written in code: every threshold, limit, timer, name, flag, rule package and queue value is a versioned row changed through a validated load, with no release | BRD Program v5 section 7 (Principle 1); REQ-DRI-010; ADR-017 |
| BR-PLT-002 | One owner per object: the platform owns the mechanism and the library, and the service owns its data, its decisions and its business rows; no platform component reads a service's data to answer a business question | DP-01; Arch v5 slides 4 and 41; Ownership Map, Services sheet |
| BR-PLT-003 | The platform decides nothing: the authorisation guard returns the owner's answer, the rules kit evaluates the owner's package, the workflow kit runs the owner's workflow and the edge merges the owner's answers | Arch v5 slides 20 and 23; REQ-ACA-003; ADR-017 |
| BR-PLT-004 | Nothing is lost and nothing happens twice: a state change and its event are one transaction, a consumed event is applied once, a repeated request returns the first answer, and a failed decision record stops the action | Arch v5 slides 11 and 34; REQ-DRI-005; ADR-015, ADR-022; R-UNI-39 |
| BR-PLT-005 | No personal data leaves its owning service: events, workflow payloads, telemetry and logs carry identifiers and facts only, the codec encrypts a workflow payload, and the masking rule is applied before a value is used | Arch v5 slide 35; NFR-039, NFR-040, NFR-053; DP-09 |
| BR-PLT-006 | One naming rule for every artefact: schema `rwb_<name>`, base `/api/recovery/<short>/v1`, topic `rwb.<short>.events.v1`, event `rwb.<short>.<Event>.v1`, task queue `rwb-<short>` and package `th.co.scb.ace.workbench.recovery.<short>`, with `rwb-platform` as the one platform queue | Story Template and Rules R4; Arch v5 slide 41; Ownership Map, Jobs sheet |
| BR-PLT-007 | A platform change is versioned and reversible: the chart, the pipeline, the workflow kit and a rule package all carry a version, and each rolls back to the previous version by one action | NFR-027; ADR-016, ADR-017; Story Template and Rules R7.2 |
| BR-PLT-008 | The edge and the platform hold no business data: Redis holds sessions only, the key store holds keys only, and no customer, account, case or document row is cached at the platform | Arch v5 slides 10, 20 and 35; RWB-PLT-N001, RWB-PLT-N006 |

## 7. Non-functional requirements

Each requirement traces to a BRD non-functional requirement. A target the source does not state is held open and never invented (GAP-1670; ASM-2819).

| ID | Requirement | Traces to | Target | Status |
|---|---|---|---|---|
| NFR-PLT-001 | A screen served through the edge answers inside its target under normal load, including the case record view of a case with 50 documents | NFR-008, NFR-009 | Under 2 seconds | Proposed |
| NFR-PLT-002 | The platform is available while cases are worked and while batch, dispatch and partner exchange run | NFR-020, NFR-021 | 99.9 percent in business hours; 99.5 percent outside, excluding the change window | Proposed, DL11 |
| NFR-PLT-003 | A platform failure loses no committed data and restores service inside the target the bank sets | NFR-022, NFR-023 | The ACE recovery point and recovery time objective | Open, DL11 |
| NFR-PLT-004 | A failure in one part is contained: Kafka down leaves events in the outbox, Temporal down pauses and resumes a journey while screens keep working, a busy ACE database is held off by capped pools, and an agent that is slow falls back to the rule result | NFR-025, NFR-024 | Containment always on | Proposed |
| NFR-PLT-005 | A failed call retries on its stated policy and anything that still fails reaches an exception path with a task for a named owner, never a silent loss | NFR-026, NFR-068 | Three retries per outbound item, then the exception queue; retry topics at 1 minute, 10 minutes and 1 hour, then the dead-letter topic with an alert (GAP-1666; ASM-2815) | Proposed, DL11 |
| NFR-PLT-006 | A release rolls back by redeploying the previous tag, and a chart, kit, flag, parameter or rule package change rolls back to its previous version by one action | NFR-027 | Rollback by previous tag and by one action | Proposed |
| NFR-PLT-007 | Every action that matters carries a decision record written in the same transaction, and every service writes audit and personal-data access logs on the ACE PII path to SOC | NFR-033, NFR-034, NFR-042 | Every action; every read of personal data | Proposed |
| NFR-PLT-008 | No personal data appears in an event, a workflow payload, a workflow history, a telemetry signal or a log; the codec encrypts a payload with AES-GCM, the key lives in the key store, and masking is applied before a value is used | NFR-039, NFR-040, NFR-053 | No personal data outside the owning service; encrypted payloads; masked in use | Proposed |
| NFR-PLT-009 | Platform data and telemetry stay in the bank's own tenancy in the agreed region, and every platform object carries a classification | NFR-046, NFR-047 | SCB Azure, Southeast Asia; classification per object | Proposed, DL26 |
| NFR-PLT-010 | Identity is checked at every layer: staff single sign-on with multi-factor at the edge, partner multi-factor with a sender-constrained token, mutual TLS between services with a workload identity per service, topic ACLs per service, one database login per schema, and deny by default | NFR-049, NFR-050, NFR-051, NFR-053 | Every call authenticated both ways; deny by default | Proposed |
| NFR-PLT-011 | Secrets, certificates and keys are held in the key store, delivered through a managed identity, and never in code, a manifest, a repository, a configuration file or a log | NFR-052 | No secret outside the key store | Proposed |
| NFR-PLT-012 | The pipeline blocks a change that carries a secret, personal data in code, tests or logs, an unapproved dependency, a boundary violation or a contract break | NFR-054 | Every build | Proposed |
| NFR-PLT-013 | A penetration test and a security review are completed before the first production release, and a further test is completed before the partner gateway opens to users outside the bank | NFR-056 | Before the first production release; before the partner portal opens | Proposed, DL11 |
| NFR-PLT-014 | Logs, traces and metrics exist for every service, every event and every workflow, and one trace follows a case action from the edge to the workflow | NFR-064 | One trace across services, events and workflows | Proposed |
| NFR-PLT-015 | Every scheduled job and every platform component has a run book, monitoring and an alert to a named owner role, and the alert is raised inside its target | NFR-067, NFR-068 | Alert within 15 minutes to the named owner | Proposed, DL11 |
| NFR-PLT-016 | The platform carries the program's volume with room to grow: about 23,600 open cases at go-live and 47,389 by 2031, about 420 concurrent users and about 21 requests a second at peak, with a capped database pool per service and workers that scale to zero | NFR-001, NFR-002 | About 23,600 open cases at go-live; 420 concurrent users; 21 requests a second | Proposed |
| NFR-PLT-017 | Every message the edge or a shared library returns to a person is available in Thai and in English, and the platform shell does not break the accessibility and browser targets of the screens it carries | NFR-059, NFR-060, NFR-061 | Thai and English; WCAG 2.1 level AA; current and previous major versions of Edge and Chrome | Proposed, DL10, DL11 |
| NFR-PLT-018 | A failed write to the outbox, the decision record or the audit path raises an incident, and no entry is discarded silently | NFR-077, NFR-025 | No silent gap | Proposed |

## 8. Data requirements

The platform holds the mechanism and the evidence of what it did. It holds no case, no customer, no account, no document, no notice, no payment and no ACE row. The four library objects that every service schema carries are one definition created 19 times; the two flag tables are one platform store, which is the pair the Ownership Map gives owner PLT with a platform schema; the rest is operator evidence, not business data.

| Entity | Key fields | Classification | Source | Retention |
|---|---|---|---|---|
| Outbox event (`outbox_event`) | event identifier, event type and version, case identifier, message key, payload, occurred at, published at, attempt count | [CONFIDENTIAL] | Library, written in the same transaction as the state change | Open (GAP-1674; ASM-2819) |
| Outbox delivery (`outbox_delivery`) | delivery identifier, event identifier, topic, partition, offset, error code, next attempt at | [CONFIDENTIAL] | Library, on every publish attempt | Open (GAP-1674) |
| Processed event (`processed_event`) | consumer, event identifier, message key, first seen at, hit count | [CONFIDENTIAL] | Library, on every consumed event | Open (GAP-1674) |
| Idempotency record (`idempotency_key`) | key, operation, request hash, stored answer, created at | [CONFIDENTIAL] | Library, on every POST that carries a key | Not specified in the source documents (GAP-1674; ASM-2819); the period is a configuration value |
| Feature flag (`feature_flag`) | flag key, description, owner role, default value, value per environment, removal date, version | [CONFIDENTIAL] | Loaded by the platform administrator; served through the library | Versioned; a superseded row is kept with its validity |
| Feature flag change (`feature_flag_change`) | flag key, environment, old value, new value, reason, user identifier, changed at, version | [CONFIDENTIAL] | Written on every flag change; the change is also written to the ACE audit path | Open (GAP-1674) |
| Local decision record (library object) | decision code, subject reference, rule, model, agent and prompt version, freshness, action, outcome, record identifier | [CONFIDENTIAL] | Library, in the same transaction as the action | Per the decision log retention (DL26) |
| Rule package cache (embedded kit) | package identifier, version, model, hash, loaded at, in force from | [CONFIDENTIAL] | Read from rwb-decision on promotion | The last two versions are kept for rollback |
| Parameter and reference cache (client library) | list or parameter code, version, value, valid from and to, author, approver | [CONFIDENTIAL] | Read from rwb-case on load and on version change | Versioned; the cache is disposable |
| Session record (Redis, edge) | session identifier, user identifier, role codes, issued at, last seen, idle expiry | [PII] | Written at sign-in; refreshed on every request | The session lifetime only; no business data |
| Telemetry signal (traces, metrics, logs) | trace and span identifiers, service, operation, duration, status, scrubbed attributes, correlation identifier | [CONFIDENTIAL] with no personal data | OpenTelemetry collector | Open (GAP-1674; Q-PLT-08) |
| Workflow record (Temporal, not a table) | workflow identifier (the business key), type, status, history (encrypted), search attributes CaseId, Stage, ProductGroup, QueueCode | [CONFIDENTIAL]; the payload is encrypted | The owning service's worker through the codec | 30 days of closed history, archived before expiry |
| Namespace register and evidence pack (platform record) | namespace name, retention, search attributes, quotas, entitlements, key name and enabled version | [CONFIDENTIAL] | Written by the platform on provisioning and on rotation | For the life of the namespace and the release evidence |

Rules that apply to the data:

- No platform object holds a customer, account, case or document row; a reference is an identifier only (DP-01; BR-PLT-002).
- An event, a workflow payload, a telemetry signal and a log carry identifiers and facts, never a name, an address, an identity number or document content (BR-PLT-005; DP-09).
- A workflow payload is encrypted by the codec before it is written to history, and the key is unwrapped by the platform identity alone (FR-PLT-025; Arch v5 slides 24 and 35).
- The session record holds identifiers and role codes only; the edge holds no business data (BR-PLT-008).
- The physical names, lengths and required flags of the library tables are the technical specification's; this PRD fixes the product content only.

## 9. Integration points

| System or service | Direction | Protocol | Owner | Notes and unknowns |
|---|---|---|---|---|
| Browser through the shared App Gateway | In | HTTPS, `/recovery/*` and `/api/recovery/*` routed to gateway-bff | ACE platform team with RWB-PLT-EDGE | WAF at the shared gateway; the staff door; no second gateway (Arch v5 slides 7 and 8) |
| ACE Common sign-in (Entra ID, MFA) | Out | OIDC and REST | ACE team | A short-lived user JWT per request; the browser never sees it (Arch v5 slides 20 and 30) |
| ACE Common audit and PII logging | Out | Kafka, the ACE PII path | ACE team | Audit and personal-data access logs to SOC; the platform supplies the instrumentation only |
| ACE PostgreSQL server | Out | PostgreSQL over TLS; one login per service | ACE team and DBA | 19 schemas, 19 logins, capped pools, a migrator role and a grant check (FR-PLT-027) |
| Kafka platform (business events) | Out and in | Kafka over TLS; CloudEvents 1.0 binary mode | Enterprise Architecture and ACE platform team | Hosting decision open: the bank's Kafka platform or the Event Hubs Kafka endpoint (Q-PLT-06; GAP-1672) |
| Schema registry | Out | Registry API, BACKWARD compatibility | Platform team | One registry for the business-event schemas (FR-PLT-028) |
| Shared Temporal layer | Out and in | Temporal gRPC over mutual TLS; namespace `rwb-recovery` | Platform team | Cluster owner of record is open (Q-PLT-05; GAP-1672) |
| Temporal Web UI and codec server | In | HTTPS behind Entra ID | Platform team | Decode only under a recorded break-glass approval (FR-PLT-026) |
| Azure Key Vault | Out | Managed identity | Platform and SCB IT infrastructure | Codec keys, credentials and certificates; key versions in the release evidence (FR-PLT-007) |
| Blob storage | Out | HTTPS with a write-once policy for legal types | Platform and SCB IT infrastructure | Standard containers created once (FR-PLT-029) |
| Managed file transfer (MFT/SFTP) | Out | SFTP or MFT with encryption for an outside party | Platform and SCB IT infrastructure | A manifest per file; the data never in the message (FR-PLT-029) |
| Bank Airflow | In and out | REST calls to service APIs; status polls | Bank platform team | Placement, DAG ownership and the Control-M migration date are open (Q-PLT-07; GAP-1673) |
| Partner gateway in the DMZ | In | HTTPS, FAPI 2.0 | Platform with SCB IT security | Partners only; provision and penetration scope open (Q-PLT-10; GAP-1676) |
| rwb-access | Out | REST and Kafka events | P4 rwb-access | The authorise contract and the three cache-refresh events (FR-PLT-019) |
| rwb-decision | Out and in | Kafka on `rwb.decision-record.v1` and the rule-package contract | P7 rwb-decision | The local record is sealed in the central ledger; the rule package is read on promotion (FR-PLT-014, FR-PLT-020) |
| rwb-case | Out | REST | P3 rwb-case | Parameters and reference data through the client libraries (FR-PLT-017, FR-PLT-018) |
| OpenTelemetry collector and the log workspace | Out | OTLP | Platform team | One collector and one workspace for every service (FR-PLT-033) |
| Source and pipeline repository | Out | Git over HTTPS; the golden pipeline | Platform team | The repository product and the pipeline tool are not named in the source set (Q-PLT-11) |
| Notification path (NSS, LINE OA) | Out | ACE REST path | ACE team with P6 rwb-comms | The removal report and the platform alerts reach a role through the shared path |

Unknowns carried as questions: the environment set and its sizing (Q-PLT-01), the per-namespace quotas, retention and key rotation (Q-PLT-02), the flag store host and the service that serves the flag paths (Q-PLT-03), the target values of the non-functional requirements (Q-PLT-04), the owner of record for Temporal and Kafka (Q-PLT-05), the Kafka hosting (Q-PLT-06), the Airflow ownership and date (Q-PLT-07), the retention of the platform rows and telemetry (Q-PLT-08), the masking and scrubbing list (Q-PLT-09), the partner gateway provision (Q-PLT-10) and the repository and pipeline product (Q-PLT-11).

## 10. Release slicing proposal

Waves follow Architecture v5 slide 38, the wave map of the Story Template and Rules section R5.6 and BRD Program v5 section 10.3. Dates are copied unchanged from BRD Program v5 section 8 and section 10.3 and are tentative. The platform is one slice in wave 0, with a second wave-0 increment at the end of December 2026 for the four Temporal governance capabilities the Epic 2 platform stories carry; no service capability of this PRD exists, so every later increment is the arrival of services on a platform that does not change.

| Slice | Wave | Release (tentative) | Capabilities | Rationale |
|---|---|---|---|---|
| Wave 0, first increment | 0 | Before EP01, November 2026 (tentative) | CAP-PLT-001, CAP-PLT-002, CAP-PLT-003, CAP-PLT-004, CAP-PLT-005, CAP-PLT-006, CAP-PLT-007, CAP-PLT-008, CAP-PLT-009, CAP-PLT-010, CAP-PLT-011 (except the four governance items below), CAP-PLT-012, CAP-PLT-013, CAP-PLT-014, CAP-PLT-015 (baseline) | Nothing of the 19 services is buildable before the template, the libraries, the schemas, the topics, the namespace, the edge and the dashboards exist; Architecture v5 slide 38 makes wave 0 the enabler of wave 1 and the platform epics deliver it before the first business release |
| Wave 0, second increment | 0 | 31 December 2026 (tentative) | CAP-PLT-011 (Temporal observability and run books, security and admin audit, backup, failover, upgrade and archive, workflow versioning and the replay gate), CAP-PLT-015 (full alert and run book coverage) | The four Epic 2 platform stories carry the governance of the Temporal layer: its dashboards, its admin audit, its resilience and its versioning gate. They land one month after the first services so that the first real histories exist to test the archive and the replay (RWB-E2-037 to RWB-E2-040) |
| Wave 1 | 1 | 30 November 2026 (tentative) | No new platform capability; nine services onboard (P1, P2, P3, P4, P5, P6, P7, P9, P10) | The wave-1 services are created on the platform as it stands; the platform slice is unchanged and any platform defect is fixed in the platform release, never in a service |
| Wave 2 | 2 | 31 December 2026 (tentative) and 31 January 2027 (tentative) | No new platform capability; four services onboard (P8, S2, S5, S8) | A new service starts from the template and needs no new platform capability; the second wave-0 increment lands in the same window |
| Wave 3 | 3 | 28 February 2027 (tentative) and 31 March 2027 (tentative) | No new platform capability; four services onboard (S1, S3, S4, S6) | As wave 2 |
| Wave 4 | 4 | 30 April 2027 (tentative), 31 May 2027 (tentative) and 30 June 2027 (tentative) | No new platform capability; two services onboard (S7, S9) | As wave 2; the platform carries 19 services, about 38 deployments at rest and one chart and pipeline (Arch v5 slide 33) |

Slicing rules:

- The platform ships whole in wave 0: a service is never deployed on a partial platform, because a template without the boundary test, a topic without its dead-letter path or a schema without its grant check is a defect found 19 times.
- A capability is not postponed into a service wave: if a wave-0 capability is late, the wave it unblocks is late, and the delay is reported rather than absorbed by a service team (ASM-2814).
- The second wave-0 increment is additive and reversible: it changes no contract a wave-1 service consumes, and a service keeps running if the increment slips.
- A platform change that breaks a contract raises a new version of the contract and deprecates the old one; no platform release edits a published version in place.

## 11. Acceptance criteria and validation evidence

```gherkin
Feature: PLT platform product behaviour

  Background:
    Given the seven platform epics deliver in wave 0 and the 19 services are created on them in waves 1 to 4
    Given the namespace rwb-recovery, the platform task queue rwb-platform and the 19 service schemas exist
    Given every consumed contract is the published contract of its owner and every downstream answer is the fake of that contract
    Given the business date is 2026-11-30

  Scenario: AC-PLT-001 A service is generated from the template and passes on its first commit
    Given a team generates a service from the template
    When the repository is created and the pipeline runs for the first time
    Then the service has an API deployment, a worker deployment, an outbox relay, an inbox, a Temporal worker on its own task queue, a payload codec, OpenTelemetry instrumentation, health and metrics endpoints, and an OpenAPI 3.1, an AsyncAPI 3.0 and an activity contract skeleton
    And the boundary test and the contract tests pass with no hand-written infrastructure
    And the service holds no schema of its own until its database story creates it in its own schema

  Scenario: AC-PLT-002 A statement that crosses the boundary fails the build
    Given a service whose code contains a SELECT on a recovery.v_ace_* view, a write to another service's schema, or a foreign key that leaves its own schema
    When the boundary test runs
    Then the build fails and names the statement and the schema it touches
    And the same statement is accepted in rwb-source-data when it reads only the 30 read-only views

  Scenario: AC-PLT-003 One pipeline deploys a service and a rollback restores the previous tag
    Given one versioned Helm chart and one golden pipeline
    When a service is released and the next release fails its checks
    Then the previous tag is redeployed and the service answers as it did before the failed release
    And the chart and the pipeline are versioned, and a change to either reaches every service by one release

  Scenario: AC-PLT-004 A migration runs in the service's own schema only
    Given a migration sequence for a service whose schema name is a parameter
    When the migration runs in DEV and again in SIT
    Then every object is created in that service's schema and in no other
    And a migration that names another schema is refused and the previous version stays in place
    And the built baseline of the monolith is the first version of the sequence and is not edited

  Scenario: AC-PLT-005 The environment set is closed and no secret sits in a file
    Given the environment list held as reference data
    When a deployment names an environment code that is not on the list
    Then the deployment is refused and no pod is created
    When a manifest, an image or a repository contains a credential, a certificate or a key
    Then the build and the deployment fail, and the credential is delivered to the workload through its managed identity instead

  Scenario: AC-PLT-006 Development is synthetic, acceptance is masked, and the personal-data scan fails the build
    Given the development and user acceptance environments
    Then development holds synthetic data only and user acceptance holds masked copies
    When the personal-data scan runs over code, tests, fixtures and logs
    Then it fails the build on a name in clear, an identity number, an account number or a document value
    And a test fixture that uses a party identifier and no personal value passes

  Scenario: AC-PLT-007 A contract is published before the build and every consumer builds against its fake
    Given a service whose contract stories are Day 1 and whose build has not started
    When the OpenAPI 3.1 document, the AsyncAPI 3.0 document, the activity contract jar and the fakes are published
    Then the service builds and its tests pass against the fakes of every contract it consumes, with the owner service unfinished
    And a name that departs from the naming rule fails the build

  Scenario: AC-PLT-008 A state change and its event are one transaction
    Given a service that changes its state and publishes an event
    When the transaction commits
    Then the state row and the outbox row are committed together and the relay publishes the event within one minute as a CloudEvents 1.0 message keyed by the case identifier
    When the transaction fails
    Then neither the state row nor the outbox row exists
    When the broker is unavailable
    Then the event waits in the outbox and is published when the broker returns, and no event is lost

  Scenario: AC-PLT-009 A duplicate event is applied once
    Given a consumer that applied an event with a given event identifier
    When the same event arrives again
    Then the inbox records the hit, the consumer applies nothing and the duplicate is counted
    When a consumer keeps failing
    Then the message passes the retry topics at 1 minute, 10 minutes and 1 hour, reaches the dead-letter topic, and an alert reaches the owner role of that consumer

  Scenario: AC-PLT-010 A repeated POST returns the first answer and makes no second change
    Given a POST that carried the Idempotency-Key "REQ-2026-11-30-0001" and was answered
    When the same request arrives again with the same key and the same body
    Then the stored answer is returned and no second state change exists
    When the same key arrives with a different body
    Then the request is refused and no state change exists

  Scenario: AC-PLT-011 One problem envelope, and the owner's message passes through
    Given a REST answer that fails at the owner, at the gateway or at the library
    Then the body is RFC 9457 problem details with type, title, status, detail and instance
    And the owner's message identifier and detail appear unchanged
    And the title and the detail are available in Thai and in English
    And the body carries no business value and no personal data

  Scenario: AC-PLT-012 A decision record that cannot be written stops the action
    Given a decision record writer that fails
    When the action is attempted
    Then the action does not happen, the state does not change and the outbox holds no event for it
    And the caller receives the failure with the owner's message identifier
    When the writer succeeds
    Then the local record and the state change commit in one transaction and the record is sealed on rwb.decision-record.v1

  Scenario: AC-PLT-013 The hash chain is checked daily and a break reaches Compliance the same day
    Given a decision log with a hash chain
    When the daily check at 02:00 runs
    Then the result is recorded with the business date and the count of records verified
    When the chain is broken at one record
    Then the check reports the break to the Compliance role on the same business day and names the record it found first

  Scenario: AC-PLT-014 A flag past its removal date is reported to its owner
    Given a flag with owner role "P3 squad" and removal date 2027-01-31
    When the weekly removal report runs on 2027-02-07
    Then the flag is listed with its owner and its removal date
    And the report reaches the owner role and the platform administrator role through the shared notification path
    When the flag has no removal date or a removal date in the past at creation
    Then the creation is refused and no flag row exists

  Scenario: AC-PLT-015 A parameter and a reference list take effect on their date
    Given parameter version "P7" in force from 2026-11-30 and reference list version "L3" in force from 2026-12-01
    When a service evaluates a decision on 2026-11-30 and again on 2026-12-01
    Then the first evaluation uses "P7" and "L3" as in force on its date, and the second uses the versions in force on 2026-12-01
    And the value is answered from the local cache with no call to the owner on every use
    And a value that is not in force on the business date is refused

  Scenario: AC-PLT-016 The guard denies by default and records the refusal
    Given a role whose policy does not include the action
    When the action is attempted
    Then it is refused and the refusal is recorded with the role, the action and the time
    When no policy is cached
    Then the action is refused and not allowed
    When a service identity acts
    Then it passes the same checks as a person and the actor is the service identity

  Scenario: AC-PLT-017 A faulty rule package is refused and the version in force keeps running
    Given rule package version "R12" in force
    When version "R13" is loaded with an unreachable row and no default row
    Then the load is refused with the failed check named, the version "R12" stays in force, and a decision taken after the refusal still returns the "R12" answer with the rule ID and the rule version recorded
    When a valid version "R14" is promoted at 00:01
    Then the next evaluation uses "R14" with no deployment, and a rollback to "R13" is refused while "R13" is invalid

  Scenario: AC-PLT-018 A workflow survives a worker stop and a Temporal outage
    Given a journey running on its task queue
    When its worker stops mid-activity and returns
    Then the journey resumes from its history and no step runs twice
    When the Temporal cluster is unavailable
    Then the running journey pauses and the screens keep working, and the journey resumes where it stopped
    And a call that fails is retried with a 1 s interval and doubling up to 10 attempts, and a non-retryable failure stops at once

  Scenario: AC-PLT-019 The stuck scan and the smoke workflow do their job
    Given the platform task queue rwb-platform
    When a workflow makes no progress for five minutes
    Then the stuck-workflow scan raises an alert with the workflow identifier, its type and its last event time to the owner role
    When the smoke workflow runs at 06:00
    Then it proves one trace across the edge and the workflow and reports success to the platform administrator
    And every payload in the namespace history is encrypted and a scan finds no clear personal value

  Scenario: AC-PLT-020 Nineteen schemas, nineteen logins and a grant check
    Given the ACE PostgreSQL server
    When the database baseline is applied
    Then 19 schemas and 19 logins exist, one per service, and each login holds grants on its own schema only and no grant on recovery or on another service schema
    And each service has a capped connection pool and a migrator role separate from its runtime login
    And the grant check fails and reports when any login can reach a schema that is not its own

  Scenario: AC-PLT-021 Topics, the retry ladder and the dead-letter path
    Given the event platform for a service
    Then the topic rwb.<short>.events.v1 exists with its retry topics and its dead-letter topic, and only the owner and its consumers hold ACLs on it
    When a message is consumed and fails three retries
    Then it reaches the dead-letter topic with an alert to the owner role of the consumer
    When a schema change is not BACKWARD compatible
    Then the registry refuses it and no consumer sees a broken schema

  Scenario: AC-PLT-022 The case screen is composed in parallel inside 2 s and one tab degrades
    Given the case screen of case "RW-2026-000101"
    When the gateway composes the screen
    Then the case read and the customer and account reads run in parallel with a 2 s timeout each, and the merged model answers inside the 2 s target
    When the payments owner exceeds 2 s
    Then the payments tab answers 503 with the problem envelope and the case, customer, documents, notices and legal areas still load
    And the session expires after 15 minutes idle and the browser is sent to sign-in with 401

  Scenario: AC-PLT-023 A partner reaches only the partner gateway and only its own cases
    Given a partner user of an agency
    When the user calls a staff route on gateway-bff
    Then the request is refused
    When the user calls the partner gateway with a valid sender-constrained token after multi-factor authentication
    Then only that partner's own cases are returned and no other case is visible

  Scenario: AC-PLT-024 Airflow reaches the platform at its edges only
    Given the bank's ingestion DAG for a business date
    When its last task calls the source-data business-date endpoint
    Then the call is accepted once for that business date and a repeated call for the same date changes nothing
    And the sensor reads the status of that date until it completes
    And the file windows and the report extract are triggered by Airflow
    And no Airflow task reads or writes an rwb_* schema

  Scenario: AC-PLT-025 One trace, no personal data, and an alert inside 15 minutes
    Given a case action from the browser through the gateway to the owner service and its event and workflow
    When the action completes
    Then one trace holds the gateway span, the owner span, the event and the workflow span with the W3C context propagated across REST, the Kafka headers and the Temporal context
    And no trace attribute, metric label or log line carries a name, an address, an identity number or document content
    When an interface, a job or a workflow fails
    Then an alert reaches the named owner role with its message identifier inside 15 minutes, and the run book of the failing piece exists
```

### 11.1 Criterion to requirement mapping

| AC | FR and NFR | Origin in the source |
|---|---|---|
| AC-PLT-001 | FR-PLT-001; NFR-PLT-014 | Arch v5 slides 20, 33 and 38; RWB-PLT-TPL, RWB-PLT-NF01 |
| AC-PLT-002 | FR-PLT-002; NFR-PLT-012 | Arch v5 slide 29; REQ-DRI-006; DP-01, DP-05; RWB-TE-001 |
| AC-PLT-003 | FR-PLT-003, FR-PLT-004; NFR-PLT-006 | Arch v5 slides 33 and 38; NFR-027; RWB-PLT-N004 |
| AC-PLT-004 | FR-PLT-005 | REQ-RDF-001; ADR-021; DP-15; RWB-E1-044 |
| AC-PLT-005 | FR-PLT-006, FR-PLT-007; NFR-PLT-011 | Arch v5 slides 8 and 35; NFR-052; RWB-PLT-NF03, RWB-PLT-NF04 |
| AC-PLT-006 | FR-PLT-008; NFR-PLT-008 | REQ-RDF-010, REQ-ACA-005; NFR-045; RWB-TE-004, RWB-TE-011 |
| AC-PLT-007 | FR-PLT-009 | Arch v5 slides 11 and 36; ADR-020; RWB-TE-003, RWB-PLT-N009 |
| AC-PLT-008 | FR-PLT-010; NFR-PLT-004 | REQ-DRI-007; Arch v5 slides 11 and 44 (JOB-11); ADR-015; RWB-TE-006 |
| AC-PLT-009 | FR-PLT-011; NFR-PLT-005 | Arch v5 slides 11 and 22; ADR-015; RWB-PLT-N002 |
| AC-PLT-010 | FR-PLT-012; NFR-PLT-004 | Arch v5 slide 11; RWB-PLT-N009 |
| AC-PLT-011 | FR-PLT-013; NFR-PLT-017 | Arch v5 slide 11; NFR-059; RWB-PLT-N009 |
| AC-PLT-012 | FR-PLT-014; NFR-PLT-007 | REQ-DRI-001 to REQ-DRI-005; ADR-022; RWB-E1-027 |
| AC-PLT-013 | FR-PLT-015; NFR-PLT-007 | REQ-DRI-003; NFR-035; JOB-14; RWB-TE-008 |
| AC-PLT-014 | FR-PLT-016 | REQ-DRI-010; RWB-E1-047; Ownership Map ruling ASM-0073 |
| AC-PLT-015 | FR-PLT-017, FR-PLT-018 | REQ-DRI-010, REQ-DRI-011, REQ-CWC-006; DP-06, DP-07; RWB-E1-042, RWB-E1-043 |
| AC-PLT-016 | FR-PLT-019; NFR-PLT-010 | REQ-ACA-003 to REQ-ACA-009; Arch v5 slides 20 and 35; DP-08; RWB-E1-037 |
| AC-PLT-017 | FR-PLT-020; NFR-PLT-006 | REQ-CWC-013, REQ-CWC-014, REQ-CWC-016; ADR-017; DP-04; RWB-E1-072 |
| AC-PLT-018 | FR-PLT-021, FR-PLT-022, FR-PLT-024; NFR-PLT-004 | Arch v5 slides 23, 24 and 34; Temporal and Drools Design slide 28; ADR-016 |
| AC-PLT-019 | FR-PLT-023, FR-PLT-025, FR-PLT-026; NFR-PLT-008 | Arch v5 slides 24 and 44 (JOB-21, JOB-22); NFR-068; RWB-PLT-N003, RWB-PLT-N005 |
| AC-PLT-020 | FR-PLT-027; NFR-PLT-016 | Arch v5 slides 29, 34, 39 and 41; ADR-014; DP-01, DP-02; NF-06, RWB-PLT-N011 |
| AC-PLT-021 | FR-PLT-028, FR-PLT-029; NFR-PLT-005 | Arch v5 slides 11, 22 and 39; ADR-015; RWB-PLT-N002, RWB-PLT-N008, RWB-PLT-N012 |
| AC-PLT-022 | FR-PLT-030; NFR-PLT-001 | REQ-OCC-007; NFR-008, NFR-009; Arch v5 slides 8, 10 and 20; DP-19; RWB-PLT-N001 |
| AC-PLT-023 | FR-PLT-031; NFR-PLT-010 | REQ-ACA-012; NFR-050; Arch v5 slides 8 and 35; RWB-PLT-N007 |
| AC-PLT-024 | FR-PLT-032 | REQ-DRI-008; NFR-013, NFR-019; Arch v5 slides 31, 32 and 44; RWB-PLT-NF07 |
| AC-PLT-025 | FR-PLT-033, FR-PLT-034; NFR-PLT-014, NFR-PLT-015 | NFR-064, NFR-067, NFR-068; Arch v5 slides 8, 35, 44 and 49; ADR-023; RWB-E1-056, RWB-PLT-N005 |

### 11.2 Validation evidence required before a capability is called done

| Evidence | What it shows |
|---|---|
| A generated service that passes on its first commit | The template is complete: two deployments, the outbox, the inbox, the worker, the codec, the instrumentation, the contracts and the boundary test |
| The boundary test run against a deliberate violation of each kind | No ACE view read, no cross-schema statement, no foreign key out of the schema, no second hop |
| A release and a rollback of one service | The chart, the pipeline and the previous tag restore the service as it was |
| A migration in DEV and in SIT | The schema name is a parameter, no other schema is touched, and the monolith baseline is the first version |
| A secret-scan and a personal-data scan failure, and a clean run | The pipeline blocks a secret and a clear personal value and passes a clean change |
| A contract published before the build and consumed through its fake | A consumer builds and is tested with the owner unfinished, and a naming departure fails the build |
| An outbox, inbox, idempotency and problem-envelope test | One transaction, one application of an event, one answer to a repeated POST, one problem envelope, the owner's message passed through |
| A decision-record failure and a hash-chain break | The action stops when the record cannot be written, and a break reaches Compliance the same day |
| A flag, a parameter and a reference-list test | Off by default, removal report with the owner, version in force on the business date, cache answer, no release |
| A guard test and a rule-package test | Deny by default, refusal recorded, service identity checked, a faulty package refused with the version in force still running |
| A worker-stop, a Temporal outage and a stuck-workflow test | The journey resumes, a pause is not a loss, the stuck scan alerts, the smoke workflow proves one trace |
| A schema and grant check run | 19 schemas, 19 logins, own-schema grants only, capped pools, a migrator role |
| A topic, retry and registry test | Retry topics and the dead-letter path, per-service ACLs, a non-BACKWARD change refused |
| A gateway test and a partner test | Parallel composition inside 2 s, one degraded tab, a session timeout, partners only through the partner gateway and only their own cases |
| An Airflow edge test | A repeated business-date call changes nothing, the sensor reads the status, no `rwb_*` access |
| A trace and alert run | One trace across the edge, the service, the event and the workflow, no personal data in telemetry, an alert inside 15 minutes with its run book |

## 12. Open questions

Questions carried forward from the BRD and the Architecture v5 decision list, plus product-level questions this PRD raises. No answer is invented.

| ID | Question | Owner | Needed by | Impact if unanswered |
|---|---|---|---|---|
| Q-PLT-01 | Which environments exist, with which names, and what size does each carry? The Environment and Deployment Design v5 records the names as a gap and Architecture v5 names DEV, SIT, UAT and production without sizing them (GAP-1668) | Solution architect with SCB IT infrastructure | Before wave 0 starts | The template cannot be parameterised, and the platform is built in an environment count that no one has agreed |
| Q-PLT-02 | What are the per-namespace quotas and rate limits, the retention beyond the 30 days of the closed-workflow rule, and the codec key rotation period? No source names them (GAP-1670) | Platform team with ACE team | Before wave 0 starts | The namespace is provisioned with invented values or with none, and a quota or a rotation is discovered in production |
| Q-PLT-03 | Where are the feature flags held, and which component serves the four flag paths? The Ownership Map gives owner PLT with schema "platform" and has no platform row in the Services sheet, while the rwb-integration API specification carries the paths (GAP-1667) | Solution architect with the platform team | Before the wave-1 release | Two flag stores or none, and a flag read that differs between services |
| Q-PLT-04 | What target value applies to each non-functional requirement that is still open: the recovery point and recovery time, the alert target, the retention periods and the masking rules? DL11 and DL26 are open (GAP-1670) | Solution architect with Risk and Compliance | Before the wave-1 release | The platform is built against a proposal that no owner has confirmed, and an audit finding lands on the platform |
| Q-PLT-05 | Who is the owner of record for the shared Temporal cluster and for the Kafka hosting? Architecture v5 slide 39 records the decision with two owners and no named team (GAP-1672) | Enterprise Architecture with the platform team | Before wave 0 starts | No one is accountable for an outage that stops every running journey |
| Q-PLT-06 | Are Recovery's business-event topics hosted on the bank's Kafka platform, or on the Azure Event Hubs Kafka endpoint as the fallback? Architecture v5 slide 39 leaves the fallback open (GAP-1672) | Enterprise Architecture with the ACE platform team | Before wave 0 starts | The topic provisioning, the ACL model and the registry placement are built twice or rebuilt |
| Q-PLT-07 | Who owns the Airflow DAGs, where does Airflow run, and when does Control-M move? Architecture v5 slide 32 lists all three as "to agree" (GAP-1673) | Bank platform team with the delivery lead | Before the wave-1 release | The overnight chain has no owner and the business-date trigger is manual |
| Q-PLT-08 | How long are the outbox, inbox, idempotency and flag rows and the telemetry signals kept? DL26 is open (GAP-1674) | Compliance with the platform team | Before the wave-1 release | A purge deletes the evidence of an event or of a flag change before an audit asks for it |
| Q-PLT-09 | Which fields are masked or scrubbed before a value reaches a prompt, a telemetry signal or an export? DL26 and Q-012 are open (GAP-1675) | Compliance with the data office | Before the wave-1 release | A personal value in a trace is a reportable breach with no rule to test against |
| Q-PLT-10 | Is the partner gateway in the DMZ provided by the bank platform or built by the programme, and what is the penetration-test scope before it opens? Partner access is open under DL03 (GAP-1676) | SCB IT security with the partner and agency manager | Before the first partner release | Partners cannot be given a door, or a door is built twice |
| Q-PLT-11 | Which repository and pipeline product carries the code, the chart and the golden pipeline? No source names it (GAP-1669) | DevOps team with the platform team | Before wave 0 starts | The template and the pipeline cannot be built, and the "one pipeline" promise has no product behind it |

## 13. Approval

| Role | Name | Decision | Date | Signature |
|---|---|---|---|---|
| Product Owner | | | | |
| FDA | | | | |

Approval is open. The BRD carries no approval record and no status field, so this PRD is issued as Draft and the requirements approval gate is not evidenced (GAP-1671; ASM-2824).

## Appendix A. Traceability summary

The master matrix `requirement/Traceability_Matrix.md` in the AI-SDLC workspace is assembler-owned; the rows this PRD contributes are below.

### A.1 Business and non-functional requirement coverage

| BR or NFR ID | CAP | FR and NFR | AC |
|---|---|---|---|
| REQ-DRI-001 | CAP-PLT-007 | FR-PLT-014; NFR-PLT-007 | AC-PLT-012 |
| REQ-DRI-002 | CAP-PLT-007 | FR-PLT-014 | AC-PLT-012 |
| REQ-DRI-003 | CAP-PLT-007 | FR-PLT-015 | AC-PLT-013 |
| REQ-DRI-004 | CAP-PLT-007 | FR-PLT-014 | AC-PLT-012 |
| REQ-DRI-005 | CAP-PLT-007 | FR-PLT-014; NFR-PLT-007 | AC-PLT-012 |
| REQ-DRI-006 | CAP-PLT-001, CAP-PLT-012 | FR-PLT-002, FR-PLT-011, FR-PLT-027; NFR-PLT-012 | AC-PLT-002, AC-PLT-009, AC-PLT-020 |
| REQ-DRI-007 | CAP-PLT-005, CAP-PLT-006, CAP-PLT-013 | FR-PLT-009, FR-PLT-010, FR-PLT-012, FR-PLT-028; NFR-PLT-004 | AC-PLT-007, AC-PLT-008, AC-PLT-010, AC-PLT-021 |
| REQ-DRI-008 | CAP-PLT-014 | FR-PLT-032 | AC-PLT-024 |
| REQ-DRI-010 | CAP-PLT-008 | FR-PLT-016, FR-PLT-017 | AC-PLT-014, AC-PLT-015 |
| REQ-DRI-011 | CAP-PLT-008 | FR-PLT-018 | AC-PLT-015 |
| REQ-ACA-003 | CAP-PLT-009 | FR-PLT-019; NFR-PLT-010 | AC-PLT-016 |
| REQ-ACA-005 | CAP-PLT-004, CAP-PLT-009 | FR-PLT-008, FR-PLT-019; NFR-PLT-008 | AC-PLT-006, AC-PLT-016 |
| REQ-ACA-006 | CAP-PLT-009, CAP-PLT-011 | FR-PLT-019, FR-PLT-026, FR-PLT-033; NFR-PLT-007 | AC-PLT-016, AC-PLT-025 |
| REQ-ACA-007 | CAP-PLT-009 | FR-PLT-019 | AC-PLT-016 |
| REQ-ACA-009 | CAP-PLT-009 | FR-PLT-019 | AC-PLT-016 |
| REQ-ACA-012 | CAP-PLT-014 | FR-PLT-031; NFR-PLT-010 | AC-PLT-023 |
| REQ-CWC-006 | CAP-PLT-008 | FR-PLT-018 | AC-PLT-015 |
| REQ-CWC-011 | CAP-PLT-010, CAP-PLT-011 | FR-PLT-020, FR-PLT-022, FR-PLT-023 | AC-PLT-017, AC-PLT-018 |
| REQ-CWC-013 | CAP-PLT-010 | FR-PLT-020 | AC-PLT-017 |
| REQ-CWC-014 | CAP-PLT-010 | FR-PLT-020 | AC-PLT-017 |
| REQ-CWC-016 | CAP-PLT-010 | FR-PLT-020 | AC-PLT-017 |
| REQ-RDF-001 | CAP-PLT-003 | FR-PLT-005 | AC-PLT-004 |
| REQ-RDF-010 | CAP-PLT-004 | FR-PLT-008; NFR-PLT-008 | AC-PLT-006 |
| REQ-DCM-002 | CAP-PLT-013 | FR-PLT-029 | AC-PLT-021 |
| REQ-DCM-003 | CAP-PLT-013 | FR-PLT-029 | AC-PLT-021 |
| REQ-OCC-007 | CAP-PLT-014 | FR-PLT-030; NFR-PLT-001 | AC-PLT-022 |
| NFR-001, NFR-002 | CAP-PLT-012 | FR-PLT-027; NFR-PLT-016 | AC-PLT-020 |
| NFR-008, NFR-009 | CAP-PLT-014 | FR-PLT-030; NFR-PLT-001 | AC-PLT-022 |
| NFR-013, NFR-019 | CAP-PLT-014 | FR-PLT-032 | AC-PLT-024 |
| NFR-020, NFR-021 | CAP-PLT-011, CAP-PLT-012 | FR-PLT-021, FR-PLT-027; NFR-PLT-002 | AC-PLT-018, AC-PLT-020 |
| NFR-022, NFR-023 | CAP-PLT-011 | NFR-PLT-003 | AC-PLT-018 |
| NFR-024, NFR-025, NFR-026 | CAP-PLT-006, CAP-PLT-011, CAP-PLT-013 | FR-PLT-010, FR-PLT-011, FR-PLT-022, FR-PLT-024, FR-PLT-028; NFR-PLT-004, NFR-PLT-005, NFR-PLT-018 | AC-PLT-008, AC-PLT-009, AC-PLT-018, AC-PLT-021 |
| NFR-027 | CAP-PLT-002, CAP-PLT-011 | FR-PLT-003, FR-PLT-024; NFR-PLT-006 | AC-PLT-003, AC-PLT-018 |
| NFR-029 | CAP-PLT-013 | FR-PLT-029 | AC-PLT-021 |
| NFR-033, NFR-034, NFR-035 | CAP-PLT-007 | FR-PLT-014, FR-PLT-015; NFR-PLT-007 | AC-PLT-012, AC-PLT-013 |
| NFR-039, NFR-040 | CAP-PLT-004, CAP-PLT-015 | FR-PLT-008, FR-PLT-033; NFR-PLT-008 | AC-PLT-006, AC-PLT-025 |
| NFR-042 | CAP-PLT-009, CAP-PLT-011, CAP-PLT-015 | FR-PLT-019, FR-PLT-026, FR-PLT-033; NFR-PLT-007 | AC-PLT-016, AC-PLT-025 |
| NFR-045 | CAP-PLT-003, CAP-PLT-004 | FR-PLT-006, FR-PLT-008; NFR-PLT-008 | AC-PLT-005, AC-PLT-006 |
| NFR-046, NFR-047 | All | NFR-PLT-009 | AC-PLT-025 |
| NFR-049, NFR-050, NFR-051 | CAP-PLT-009, CAP-PLT-011, CAP-PLT-014 | FR-PLT-019, FR-PLT-026, FR-PLT-031; NFR-PLT-010 | AC-PLT-016, AC-PLT-023 |
| NFR-052 | CAP-PLT-002, CAP-PLT-003 | FR-PLT-004, FR-PLT-007; NFR-PLT-011 | AC-PLT-005 |
| NFR-053 | CAP-PLT-011, CAP-PLT-013 | FR-PLT-025, FR-PLT-029; NFR-PLT-008 | AC-PLT-019, AC-PLT-021 |
| NFR-054 | CAP-PLT-001, CAP-PLT-002, CAP-PLT-004, CAP-PLT-005 | FR-PLT-001, FR-PLT-003, FR-PLT-004, FR-PLT-009; NFR-PLT-012 | AC-PLT-001, AC-PLT-003, AC-PLT-007 |
| NFR-056 | CAP-PLT-014 | NFR-PLT-013 | AC-PLT-023 |
| NFR-059 | CAP-PLT-006 | FR-PLT-013; NFR-PLT-017 | AC-PLT-011 |
| NFR-060, NFR-061 | All | NFR-PLT-017 | AC-PLT-022 |
| NFR-064 | CAP-PLT-001, CAP-PLT-015 | FR-PLT-001, FR-PLT-033; NFR-PLT-014 | AC-PLT-001, AC-PLT-025 |
| NFR-067, NFR-068 | CAP-PLT-011, CAP-PLT-013, CAP-PLT-015 | FR-PLT-011, FR-PLT-013, FR-PLT-023, FR-PLT-025, FR-PLT-034; NFR-PLT-015 | AC-PLT-009, AC-PLT-011, AC-PLT-019, AC-PLT-025 |
| NFR-077 | CAP-PLT-006, CAP-PLT-007 | FR-PLT-010, FR-PLT-014; NFR-PLT-018 | AC-PLT-008, AC-PLT-012 |

### A.2 Platform requirement coverage

| ID | Requirement | CAP | FR count | Status |
|---|---|---|---|---|
| FR-PLT-001 | Service template completeness | CAP-PLT-001 | 1 | Covered |
| FR-PLT-002 | Module boundary test | CAP-PLT-001 | 1 | Covered |
| FR-PLT-003 | One pipeline, one chart, two deployments, rollback by tag | CAP-PLT-002 | 1 | Covered |
| FR-PLT-004 | Code ownership and the pipeline gates | CAP-PLT-002 | 1 | Covered |
| FR-PLT-005 | Migration per service with a parameterised schema | CAP-PLT-003 | 1 | Covered |
| FR-PLT-006 | The environment set | CAP-PLT-003 | 1 | Covered |
| FR-PLT-007 | Secrets and keys in the key store | CAP-PLT-003 | 1 | Covered |
| FR-PLT-008 | Synthetic development, masked acceptance, personal-data scan | CAP-PLT-004 | 1 | Covered |
| FR-PLT-009 | Contract-first publication with fakes and contract tests | CAP-PLT-005 | 1 | Covered |
| FR-PLT-010 | Transactional outbox | CAP-PLT-006 | 1 | Covered |
| FR-PLT-011 | Inbox dedupe, retry ladder and dead-letter path | CAP-PLT-006 | 1 | Covered |
| FR-PLT-012 | Idempotency key | CAP-PLT-006 | 1 | Covered |
| FR-PLT-013 | RFC 9457 problem envelope | CAP-PLT-006 | 1 | Covered |
| FR-PLT-014 | Local decision record in the transaction, sealed on the shared topic | CAP-PLT-007 | 1 | Covered |
| FR-PLT-015 | Daily hash-chain check | CAP-PLT-007 | 1 | Covered |
| FR-PLT-016 | Feature flags with a removal date | CAP-PLT-008 | 1 | Covered |
| FR-PLT-017 | Parameter and configuration client | CAP-PLT-008 | 1 | Covered |
| FR-PLT-018 | Reference-data client | CAP-PLT-008 | 1 | Covered |
| FR-PLT-019 | Authorisation guard, deny by default | CAP-PLT-009 | 1 | Covered |
| FR-PLT-020 | Embedded rules kit with the load checks and the rollback | CAP-PLT-010 | 1 | Covered |
| FR-PLT-021 | Cluster, namespace, retention, search attributes | CAP-PLT-011 | 1 | Covered |
| FR-PLT-022 | The versioned workflow kit | CAP-PLT-011 | 1 | Covered |
| FR-PLT-023 | Schedules and durable timers replace Quartz | CAP-PLT-011 | 1 | Covered |
| FR-PLT-024 | Retry policy, backup, failover, archive, replay gate | CAP-PLT-011 | 1 | Covered |
| FR-PLT-025 | Stuck-workflow scan, smoke workflow, codec | CAP-PLT-011 | 1 | Covered |
| FR-PLT-026 | Mutual TLS, admin audit, break-glass decode | CAP-PLT-011 | 1 | Covered |
| FR-PLT-027 | 19 schemas, 19 logins, capped pools, grant check | CAP-PLT-012 | 1 | Covered |
| FR-PLT-028 | Topics, retry and dead-letter topics, ACLs, registry | CAP-PLT-013 | 1 | Covered |
| FR-PLT-029 | Blob, key store and transfer resources | CAP-PLT-013 | 1 | Covered |
| FR-PLT-030 | gateway-bff, session, composite screens, error mapping | CAP-PLT-014 | 1 | Covered |
| FR-PLT-031 | Partner gateway under FAPI 2.0 | CAP-PLT-014 | 1 | Covered |
| FR-PLT-032 | The Airflow edge contract | CAP-PLT-014 | 1 | Covered |
| FR-PLT-033 | One trace, metrics, logs and scrubbing | CAP-PLT-015 | 1 | Covered |
| FR-PLT-034 | Dashboards, alert rules and run books | CAP-PLT-015 | 1 | Covered |

Coverage statement. The BRD carries no platform business requirement (BRD Program v5 section 11 and ASM-2616), so there is no BR of the platform without a functional requirement and no FR without a BR: every FR names at least one business requirement of the BRD that the mechanism serves or one BRD non-functional requirement that sets its target. Eleven of the 34 requirements name an FSD requirement of the module whose behaviour depends on the mechanism; the remaining 23 name the BRD non-functional requirement and the confirmed Architecture v5 constraint, because the FSD v6 set has no module for the platform (GAP-1664; ASM-2809).

Four obligations are carried without a requirement of their own and are named here so the gap is not read as an omission:

- REQ-DRI-009 (the daily copy of the decision log to the data lake) is removed with the data lake (ADR-018; DP-17). The platform requires the local record and the shared topic (FR-PLT-014) and no lake copy.
- The queue write interface of REQ-CWC-017 to REQ-CWC-020 is P3 rwb-case's; the platform requires only that the flag that ships it is a versioned row with a removal date (FR-PLT-016) and that the call runs under a service identity through the guard (FR-PLT-019).
- NFR-065 and NFR-066 (business measures per decision, and agent acceptance, override, latency and cost) are delivered by the read model of rwb-reporting and by rwb-agent; the platform supplies the events, the trace and the dashboard baseline they are measured from (FR-PLT-033, FR-PLT-034).
- NFR-028, NFR-030, NFR-031, NFR-072 to NFR-075 (retention classes, legal hold, discovery and disposal) are the document hub's and the decision log's; the platform keeps no business record and states only the retention of its own rows and telemetry, which is open under Q-PLT-08.
