# RWB-ITG-E1070-ITG Temporal platform on the ACE AKS clusters — integration

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1070-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-070 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP04, DP05, DP06, DP07, DP13, DP14, DP15, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-E1070-ITG-16); the squad sizes it at refinement |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | Temporal activity contract jar version Not specified in the source documents (DOR-RWB-ITG-E1070-ITG-23) |
| Integration dependencies | RWB-P4-E1022-APP, RWB-PLT-E1070-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-009, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-016, FR-PLT-017, FR-PLT-018, FR-PLT-021, FR-PLT-022, FR-PLT-023, FR-PLT-024, FR-PLT-025, FR-PLT-026, FR-PLT-028, FR-PLT-029) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: RWB-E1-070 is split and reworked. The cluster, the two Temporal databases, the namespace bootstrap, the mTLS certificates, the Entra ID configuration, the dashboard and the run book become the wave-0 platform deliverable RWB-PLT-E1070-APP, and the Workbench roles the Web UI maps come from RWB-P4-E1022-APP; the legacy criteria AC1 to AC7 stay at component level there. This wave-1 integration story keeps only what no component story can prove: one namespace `rwb-recovery` per environment, one task queue `rwb-<short>` and one worker identity per service on the real wave-1 services, a step in another service executed as a Temporal call on that service's queue and not as a REST chain, the two Temporal databases refused to every `rwb_*` login and back, a smoke run that survives a frontend pod restart with the same workflow ID and run ID, no personal data in payloads or search attributes, and 30-day retention with no Quartz table behind a workflow timer. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (11 resolved, 18 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer**, I want **the shared Temporal platform of the programme proved on the real wave-1 services — one namespace `rwb-recovery` per environment, one task queue `rwb-<short>` and one worker identity per service, each worker presenting its own certificate, the two Temporal databases refused to every `rwb_*` login and back, a step in another service executed as a Temporal call on that service's queue with no REST hop, the smoke workflow `platform-smoke-20261116` still RUNNING with the same workflow ID and run ID after a frontend pod restart, no personal data in workflow payloads or search attributes, and 720 hours of retention with no Quartz table or shared job table behind a workflow timer**, so that **the engine every case workflow of Epic 3 depends on is proved on the services that will run it, before wave 1 exits**.

### 2. Business rationale

The legacy story installs one Temporal cluster per environment on the ACE AKS clusters as a single-module platform enabler: the databases `temporal` and `temporal_visibility` owned by `temporal_svc`, the namespace `rwb-recovery` with 30-day retention and four Keyword search attributes, mTLS from the ACE internal CA, the Web UI behind Entra ID OIDC, metrics and a run book. That work does not disappear, but it is no longer Epic 1 module work: Arch v5 slides 23 and 24 keep the cluster, the namespaces and the workflow kit owned once by the platform team and reused by every workbench (DP, platform epic RWB-PLT-WF), so the release, the schema jobs, the namespace bootstrap, the certificates, the OIDC application, the dashboard and the run book become RWB-PLT-E1070-APP in wave 0, and the Workbench roles the Web UI maps come from rwb-access in RWB-P4-E1022-APP. The seven legacy criteria stay where they are built.

What no component story can prove is the shape the platform has to hold once 19 services use it. In the target every service has its own task queue `rwb-<short>` in the one namespace (Arch v5 slide 41), its own login and its own schema `rwb_<name>` with its own Flyway sequence (DP-02, DP-01, DP-15), its own topic `rwb.<short>.events.v1` through the naming library (DP-14), its own embedded Drools kit taking rule packages from rwb-decision (DP-04), parameters and reference data through the contracts of rwb-case (DP-06, DP-07), ACE data only through rwb-source-data (DP-05), REST only at `/api/recovery/<short>/v1` (DP-13) and only behind gateway-bff (DP-19). On that shape four properties are load-bearing and none of them is visible from one module:

- A service that polls another service's queue takes work it may not execute; two registrations of one service quietly double the pollers of a queue. Both break the release boundary that makes a service reusable.
- A shared or foreign certificate makes the frontend log useless and lets one service signal another service's workflows.
- A REST chain between two services inside a business step puts a synchronous dependency inside a durable process, which is exactly what Arch v5 slide 11 forbids; the step has to be a Temporal call on the owner's queue with the workflow ID as the idempotency key.
- One grant between `temporal_svc` and a `rwb_*` schema puts case data in the workflow store or workflow history in the case schema, and a workflow timer parked in a Quartz table puts the durability of a case on the scheduler that Arch v5 slide 44 retires.

This story builds the harness that proves those properties together, on the nine wave-1 services, against the deployed platform of RWB-PLT-E1070-APP and the roles of RWB-P4-E1022-APP. It meets REQ-DRI-007 (a named owner and a tested way back for every failure) and REQ-DRI-010 (environment values come from configuration, not code): the namespace, the retention, the four search attributes, the queue list, the probe queue and the endpoints are configuration, and the harness edits no platform value to make a test pass.

The legacy measure — DEV and SIT pass every check, and operations restart a stopped frontend in SIT from the run book alone — stays with RWB-PLT-E1070-APP, which owns the run book. The measure of this story is the platform-wide one: the seven checks of section 16 pass on the deployed wave-1 services in SIT, each of the nine services shows exactly one poller on its own queue, the smoke run keeps its workflow ID and run ID across a frontend pod delete and completes once, the cross-service step is a Temporal call with no REST hop, and both grant directions are refused with SQLSTATE 42501.

The worker registration, the per-service certificate and the smoke-queue element of the platform contract, and the exact way the suite selects the cross-service step and the access review evidence, are not named in the sources: Not specified in the source documents (GAP-0378; ASM-0544). The suite asserts the properties that are named and records the three defaults it reads from configuration, so a change of registration path or probe queue is one configuration edit and one test edit.

### 3. Preconditions

- RWB-PLT-E1070-APP is done in wave 0: the release, TemporalSchemaJob, NamespaceBootstrapJob, the OIDC configuration, the certificate binding, the dashboard and the run book are in place (Template and Rules §R5.6: platform is wave 0).
- The namespace `rwb-recovery` exists once in SIT with retention 720 hours and the Keyword search attributes CaseId, Stage, ProductGroup and QueueCode.
- RWB-P4-E1022-APP is done: rwb-access holds the Workbench roles RW-PLATADM, RW-AUDIT and RW-CASEOWN with their letters, and the synthetic SIT sign-in identities U-70, U-53 and U-62 are mapped to them.
- The nine wave-1 services are deployed in SIT with their own worker deployment, login and schema: rwb-source-data (P1), rwb-integration (P2), rwb-case (P3), rwb-access (P4), rwb-document (P5), rwb-comms (P6), rwb-decision (P7), rwb-reporting (P9) and rwb-agent (P10), each on its own task queue `rwb-<short>`.
- Each of the nine worker deployments runs in the ACE namespace of SIT with a workload identity and a client certificate issued by the ACE internal CA that names the namespace; the certificate and key are readable through the CSI driver binding of RWB-PLT-E1070-APP.
- The published activity contract jar of each service is in the artefact repository, so the smoke run can call a step on another service's queue without importing that service's code.
- The ACE AKS SIT cluster runs the ACE namespace, the zone-redundant PostgreSQL flexible server, Key Vault, the ACE monitoring namespace and the internal ingress of the Web UI; the frontend gRPC port 7233 is reachable only from the cluster network and the worker subnets.
- The access review report of the platform is produced in SIT and lists the grants of `temporal_svc` and of every `rwb_*` login.
- The harness reads the namespace, the retention, the four search attributes, the nine queues, the probe queue, the workflow ID `platform-smoke-20261116`, the endpoints and the three test identities from configuration, and refuses a UAT or production target.
- The worker registration, the per-service certificate and the smoke-queue element of the platform contract, and the selection of the cross-service step, are Not specified in the source documents (GAP-0378; ASM-0544).
- The run is SIT only, on synthetic data; no run of this harness points at UAT or production, and no production connection is opened.
- The release date 30 November 2026 is tentative; a date is not a condition of this story.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7). The harness is written on Day 1 against the platform contract and is run when the wave-1 services are in SIT; a fake worker is never used in place of a service worker.

### 4. Flow

1. Harness: loads the configuration — the namespace, the retention, the four search attributes, the nine queues, the probe queue, the workflow ID `platform-smoke-20261116`, the endpoints, the three test identities — and runs the preflight; a missing namespace, deployment, queue, role or certificate, or a UAT or production target, stops the run before any test.
2. Harness: describes the namespace of the environment and asserts that it is the single namespace `rwb-recovery` in which a wave-1 service runs (AC1, AC7).
3. Harness: describes the nine task queues and records the poller identity of each, then compares it with the workload identity of the owning service and with the queue declaration of that service's worker deployment (AC1).
4. Harness: connects to the frontend with no certificate, with an expired certificate and with a certificate issued for another namespace, and attempts to start a workflow each time; then connects each of the nine service certificates and records the result (AC2).
5. Harness: runs the grant probes — a session as `temporal_svc` against a table of each `rwb_*` schema, and a session as each `rwb_*` login against `temporal` and `temporal_visibility` — and records SQLSTATE 42501 each time, then reads the access review report (AC3).
6. Harness: starts the smoke workflow `platform-smoke-20261116` on the queue of the service named in configuration, with the workflow ID `platform-smoke-20261116` as the idempotency key, and waits until it is RUNNING on its timer (AC4, AC5).
7. Harness: asserts the two steps the run executes — the read step through the published activity contract on task queue `rwb-decision` and the write step on task queue `rwb-case` — and asserts that the call chain of the run holds no REST call between two services (AC4).
8. Harness: starts the same workflow ID a second time and asserts that the running execution is returned with no second run and no second write (AC4).
9. Harness: deletes the frontend pod, waits for the replacement pod to be ready, and re-reads the workflow — same workflow ID, same run ID, still RUNNING; the timer then fires and the smoke activity completes the run (AC5).
10. Harness: reads the search attributes of the namespace and of the run and the payload of the run and of its two activity calls, and asserts the four Keyword attributes only and no personal data field (AC6).
11. Harness: reads the timer of the run from the workflow history of the database `temporal` and asserts that no Quartz table and no ACE shared job table holds it (AC7).
12. Harness: reconciles the counts — one namespace, nine queues, nine pollers, one smoke run, zero grants across the boundary, zero REST calls in the chain — and writes the run report.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A client connects to the frontend with no certificate, an expired certificate or a certificate for another namespace | The TLS handshake fails or the call is refused with PERMISSION_DENIED; no workflow is started or signalled, and the frontend log records the client identity only | None (TLS) | AC2 |
| X2 | A service registers two workers, a worker declares two queues, or a queue lists a poller of another service | The run fails and the report names the service, the queue and the identity; no test after it runs | None | AC1 |
| X3 | A grant exists between `temporal_svc` and a `rwb_*` schema, or between a `rwb_*` login and the Temporal databases, in either direction | The run fails, the access review check fails and the grant is removed before the next environment | None (access review) | AC3 |
| X4 | A step in another service is executed as a REST call, or a workflow of the run calls a service base | The run fails and the report names the step, the workflow ID and the path called | None | AC4 |
| X5 | The frontend pod delete loses, restarts or duplicates the smoke run | The run fails and names the workflow ID, the run ID and the status observed after the restart | None | AC5 |
| X6 | A search attribute, a workflow input or a payload carries a name, a national ID or another personal data field | The run fails and the field is named in the report; the platform value is corrected in RWB-PLT-E1070-APP, never in the harness | None | AC6 |
| X7 | Retention differs from 720 hours, or a workflow timer is found in a Quartz table or a shared job table | The run fails and names the store that holds the timer | None | AC7 |
| X8 | The configuration points at UAT or production, a service has no worker deployment, or a fake worker or fake frontend is configured | The preflight stops the run with the offending element named; no test data is written anywhere | None | AC1 |

X1 is the legacy exception path X1 of RWB-E1-070 carried onto the real services; X3 is the legacy X3 carried onto the 19 schemas; X2 and X4 are the registration and call-shape regressions that Arch v5 slides 11, 24 and 41 need; X5 to X7 are the durability, boundary and retention guardrails in testable form.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | A harness of its own that owns no schema, no migration and no workflow; it needs the platform contract of RWB-PLT-E1070-APP, the roles of RWB-P4-E1022-APP and the nine wave-1 workers |
| Negotiable | Probe queue, wait intervals, retry counts, the certificate names and the report layout are configuration; the namespace, the retention, the four search attributes, the queue list and the two message IDs are fixed |
| Valuable | Proves across services what no single story proves: nine registrations on nine queues, no cross-polling, one certificate per service, a step in another service as a Temporal call, a restart that loses nothing, a boundary with no grant and no timer in a scheduler table |
| Estimable | One harness module, six probes, one restart window and one report |
| Small | Fits one sprint with the report |
| Testable | Every criterion is asserted on an observable: a namespace describe, a queue describe, a poller identity, a TLS result, an activity call, a workflow ID and run ID, SQLSTATE 42501, a search attribute, a retention value and a history event count |

### 7. Acceptance criteria

```gherkin
Feature: Temporal platform on the ACE AKS clusters, proved on the real wave-1 services

  Background:
    Given the environment is SIT with synthetic data
    Given the platform release of RWB-PLT-E1070-APP runs in the ACE namespace of SIT with the namespace rwb-recovery
    Given the nine wave-1 services rwb-source-data, rwb-integration, rwb-case, rwb-access, rwb-document, rwb-comms, rwb-decision, rwb-reporting and rwb-agent each run their own worker deployment behind their own login and schema
    Given no contract fake stands in for a service in this suite

  Scenario: AC1 One namespace per environment, one queue per service and each worker polls only its own queue (new, D-RCV-60)
    Given the task queue of a service is rwb-<short> in the namespace rwb-recovery, as on Arch v5 slides 23, 24 and 41
    When the harness describes the namespaces of SIT
    Then rwb-recovery exists once and no second namespace holds a run of a wave-1 service
    When the harness describes every task queue of the namespace
    Then the nine queues rwb-source-data, rwb-integration, rwb-case, rwb-access, rwb-document, rwb-comms, rwb-decision, rwb-reporting and rwb-agent are registered
    Then each of the nine queues lists exactly one poller and that poller is the workload identity of the service that owns the queue
    Then no queue lists a poller of another service and no worker identity appears on two queues
    Then the worker deployment of each service declares that one queue and no other

  Scenario: AC2 Each worker presents its own certificate and a missing, expired or foreign certificate is refused (new, D-RCV-60)
    Given the frontend on port 7233 requires a client certificate issued by the ACE internal CA that names the namespace rwb-recovery
    When a client connects with no certificate and tries to start the smoke workflow
    Then the TLS handshake fails, no workflow call is served and no run is started
    When a client connects with an expired certificate
    Then the TLS handshake fails with certificate expired and no run is started
    When a client connects with a certificate issued for another namespace
    Then the call is refused with PERMISSION_DENIED and no run is started
    Then each refusal is in the frontend log and the TLS alert with the client identity only
    When each of the nine service workers connects with the certificate bound to its own service
    Then every connection is accepted and no two services present the same certificate

  Scenario: AC3 The Temporal databases and the rwb_* schemas are separated in both directions (new, D-RCV-60)
    Given temporal_svc owns the databases temporal and temporal_visibility
    Given each wave-1 service reads and writes the ACE database through its own rwb_* login
    When a session as temporal_svc runs SELECT on a table of each rwb_* schema of the nine services
    Then PostgreSQL refuses every statement with SQLSTATE 42501 and returns no row
    When a session as each of the nine rwb_* logins runs SELECT on temporal.executions and on a table of temporal_visibility
    Then PostgreSQL refuses every statement with SQLSTATE 42501 and returns no row
    Then the access review report shows no grant between temporal_svc and any rwb_* schema and no grant from a rwb_* login to the two Temporal databases

  Scenario: AC4 A step in another service is a Temporal call on that service's queue and the chain makes no REST call (new, D-RCV-60)
    Given the platform workflow kit of RWB-PLT-WF and the published activity contract of each wave-1 service are deployed
    Given the smoke workflow platform-smoke-20261116 is started on the queue of the service named in configuration, with the workflow ID platform-smoke-20261116 as the idempotency key
    When the run reaches the decision step that belongs to rwb-decision
    Then the step is executed as the activity EvaluateRules on task queue rwb-decision and never as a call to the rwb-decision service base
    When the run reaches the write step that belongs to rwb-case
    Then the step is executed as the activity RecordAndApply on task queue rwb-case
    Then the call chain of the run records no REST call between two services and no call to the base /api/recovery/<short>/v1 by the harness or by the workflow
    When the same workflow ID platform-smoke-20261116 is started a second time
    Then the running execution is returned with no second run and no second write

  Scenario: AC5 A frontend pod restart keeps the smoke run RUNNING with the same workflow ID and run ID (new, D-RCV-60)
    Given the smoke workflow platform-smoke-20261116 is RUNNING and waits on its timer
    When the frontend pod is deleted and the replacement pod becomes ready
    Then the workflow is still RUNNING with workflow ID platform-smoke-20261116 and the same run ID
    When the timer fires and the activity completes
    Then the workflow status is COMPLETED
    Then the history holds every event once, with no gap and no duplicate start
    Then the visibility record of the run still carries the four search attributes of the run

  Scenario: AC6 No personal data in a workflow payload or a search attribute (new, D-RCV-60)
    Given the smoke run carries a synthetic payload written by the platform workflow kit
    When the harness reads the search attributes of the namespace and of the smoke run
    Then the only attributes are CaseId, Stage, ProductGroup and QueueCode, each of type Keyword
    Then no attribute holds a name, a national ID, an address, a phone number or another personal data field
    When the harness reads the payload of the run and of its two activity calls
    Then each payload carries CaseId, Stage, ProductGroup and QueueCode only
    Then no workflow input, no payload and no log line of the run holds a personal data field

  Scenario: AC7 Retention is 30 days and no Quartz table or shared job table holds a workflow timer (new, D-RCV-60)
    When the harness describes the namespace rwb-recovery in SIT
    Then the retention is 720 hours, 30 days
    Given the smoke run waits on its timer
    When the harness reads the timer of the run
    Then the timer is in the workflow history of the database temporal and in no other store
    Then no row of a Quartz table and no row of the ACE shared job table holds the timer of the run
    Then the Temporal Schedule that runs the same workflow type at 06:00 belongs to RWB-PLT-E1070-APP and is neither created nor changed by this story

  Scenario: AC8 The namespace, retention, queues, endpoints and workflow ID are read from run configuration and the harness never reaches UAT or production (new, D-RCV-60)
    Given the namespace, the retention, the search attributes, the queue list, the endpoints, the probe queue and the workflow ID are set in the run configuration and not in code
    When the harness starts the smoke run in SIT
    Then the run uses the namespace rwb-recovery, the retention of the run configuration and the workflow ID platform-smoke-20261116
    When the harness is pointed at a UAT or production endpoint
    Then the harness refuses the endpoint and starts nothing

  Scenario: AC9 A retried or timed-out activity keeps the workflow ID as its key and writes once (new, D-RCV-60)
    Given the smoke run has started the activity EvaluateRules on task queue rwb-decision under the workflow ID platform-smoke-20261116
    When an attempt of the activity EvaluateRules times out
    Then the run does not write while EvaluateRules has not completed and the workflow ID stays the key of the run
    When EvaluateRules has completed and the first attempt of the activity RecordAndApply on task queue rwb-case times out
    Then the activity is retried on the same task queue rwb-case under the same workflow ID and no second run is started
    When the retried attempt completes
    Then the write is recorded once and the history holds one completed activity for the step
```

All nine criteria are new: the legacy criteria AC1 to AC7 of RWB-E1-070 assert the cluster, the two databases, mTLS, the Web UI roles, the namespace settings, the frontend restart and the run book at component level, and they are owned by RWB-PLT-E1070-APP (with the roles of AC4 taken from RWB-P4-E1022-APP). Nothing of that is re-copied here; this story asserts the same platform across services, on the queues, the identities, the call shape, the retention and the boundary that only exist once more than one service uses it.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One Temporal cluster per environment on the ACE AKS clusters and one namespace per workbench; the platform is owned once by the platform team and each service only runs a worker in it | Arch v5 slides 23 and 24; RWB-PLT-E1070-APP |
| BR2 | The namespace is `rwb-recovery` in every environment; retention is 30 days (720 hours) and the only search attributes are CaseId, Stage, ProductGroup and QueueCode as Keyword, holding case codes and queue codes only | RWB-E1-070 BR5; Arch v5 slide 23; Temporal design slide 27 |
| BR3 | Each service registers exactly one worker on the task queue `rwb-<short>` of its own service in namespace `rwb-recovery`, and no worker polls another service's queue | Arch v5 slides 23, 24 and 41; Temporal design slide 11 |
| BR4 | Every worker connects to the frontend over mTLS with its own certificate from the ACE internal CA naming the namespace; a missing, expired or foreign-namespace certificate starts and signals nothing | RWB-E1-070 BR3; Arch v5 slide 11 |
| BR5 | Temporal persistence is separate from the ACE database: `temporal_svc` has no grant on any `rwb_*` schema and no `rwb_*` login has a grant on `temporal` or `temporal_visibility` | RWB-E1-070 BR2; Arch v5 slide 11 |
| BR6 | A step in another service is a Temporal call on the owner's task queue; the workflow ID is the business key and therefore the idempotency key, and a REST call between two services inside a business step is not allowed | Arch v5 slide 11 (never: call chains, depth greater than one); Temporal design slide 12 |
| BR7 | A frontend pod restart loses no workflow: the run keeps its workflow ID and run ID, completes on its timer, and its history holds every event once | RWB-E1-070 BR6 |
| BR8 | No personal data in a search attribute, a workflow payload, a workflow input, a workflow history or a log; the smoke payload is synthetic and the codec is out of scope here | RWB-E1-070 §17; Arch v5 slide 11 (never: PII in workflow code or payloads); Temporal design slide 27 |
| BR9 | A workflow timer lives in the Temporal history and never in a Quartz table or a shared job table; every scheduled job is a Temporal Schedule in its owning service | Arch v5 slide 44; Template and Rules §R5.5 DP-10 |
| BR10 | Namespace, retention, search attributes, queue list, endpoints, probe queue and workflow ID are configuration read at run time, never code (REQ-DRI-010); the harness never points at UAT or production | RWB-E1-070 BR8; REQ-DRI-010 |

### 9. State transitions

None for a case status. This story changes no case status and starts no business workflow; it observes the platform states below.

| Item | States |
|---|---|
| Namespace | REGISTERED (the only state of a namespace in this story); a missing namespace or a second namespace holding a wave-1 run stops the run |
| Worker registration | Registered on its own queue `rwb-<short>` and polling it, or unregistered; a second registration, a second queue or a foreign poller fails the run |
| Certificate | Valid and accepted, or absent, expired or issued for another namespace and refused |
| Workflow run | RUNNING on its timer, then COMPLETED; a lost, restarted or duplicated run fails the run |
| Activity step | Executed on the owner's queue, or refused; a REST hop in its place fails the run |
| Grant | Absent across the boundary (`temporal_svc` against `rwb_*`, `rwb_*` against the Temporal databases) and refused with SQLSTATE 42501; present fails the run |
| Timer | Held in the workflow history of the database `temporal`; held in a Quartz table or a shared job table fails the run |
| Harness run | Not started, running, passed, or failed with the criterion, the service and the observable named |

The suite reads these states through the platform interfaces and the access review report; it changes none of them directly.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Owns the harness, the fixtures, the restart window and the report; runs the suite in SIT |
| RW-PLATADM Platform administrator | Reads the namespace, the queues and the deployments; owns the platform values the suite only reads |
| RW-AUDIT Internal audit | Reads the namespace and the workflow history in the Web UI; changes nothing |
| RW-SECADM Security administrator | Reads the certificate and OIDC configuration; decode through the codec server is RWB-E2-038, not this story |
| RW-CASEOWN and every other Workbench role | No Web UI access on the platform surface; the role mapping is RWB-P4-E1022-APP |
| The nine service worker identities | Connect with their own certificate and poll only their own queue `rwb-<short>`; no Web UI account |
| RWB-PLT-E1070-APP owner | Owns the cluster, the namespace, the registration contract, the certificates, the Schedule and the run book that this story exercises |
| RWB-P4-E1022-APP owner | Owns the Workbench roles and their letters that the Web UI maps |
| No role | May register a second worker, poll another service's queue, share a certificate between services or hold a grant across the database boundary |

No delegation of authority level applies: a platform proof is not a credit decision.

### 11. Data

Temporal persistence is outside the recovery schema. This story reads and writes no table in the recovery schema, adds no DF-REF, DF-CAS or DF-DEC field, and owns no schema of its own.

| Store | What it holds | Owner | In the Physical Schema | BR Field ID |
|---|---|---|---|---|
| `temporal` | Workflow histories, mutable state, timers, tasks | `temporal_svc` | No | Not specified in the source documents (DOR-RWB-ITG-E1070-ITG-7) |
| `temporal_visibility` | Workflow visibility records and search attributes | `temporal_svc` | No | Not specified in the source documents (DOR-RWB-ITG-E1070-ITG-7) |
| ACE database, the `rwb_*` schemas | Case and module data, the system of record | each service login | Yes, unchanged by this story | Not specified in the source documents (DOR-RWB-ITG-E1070-ITG-7) |

The Physical Schema counts 93 tables and does not include the Temporal tables. The two Temporal databases are created by TemporalSchemaJob of RWB-PLT-E1070-APP; no Flyway migration of any service touches them. The only data the suite handles is the synthetic smoke payload, which carries CaseId, Stage, ProductGroup and QueueCode and no personal data; every other observable is a namespace describe, a queue describe, a Web UI page, a gRPC start or signal, a SQL SELECT that must be refused, or a read of the access review report. The SIT evidence is recorded beside the run report, and the grant evidence is taken from the access review of rwb-access (GAP-0378; ASM-0546).

### 12. Contract

The platform is reached over Temporal gRPC on port 7233 with mTLS, and over the Temporal Web UI on its internal ingress behind Entra ID OIDC. It is not reached through a Workbench REST operation: this story adds no path under `/api/recovery/<short>/v1`, no service base and no service route, and no service proxies a workflow call.

#### 12.1 REST operations provided

None. The harness is a test project and provides no REST operation. No path is added under `/api/recovery/<short>/v1` for any service, and the names of P2 rwb-integration are not used: no `/api/recovery/integration/v1` operation, no `rwb.integration.events.v1` topic and no `rwb_integration` table is written by this story.

#### 12.2 REST operations consumed

None. The platform interfaces are Temporal gRPC (start, signal, describe) and the Web UI; neither is a Workbench REST operation. No service base is called by the harness and none is called by a workflow of the run, because a step in another service is a Temporal call on that service's queue (AC4). The Workbench roles the Web UI maps are held in rwb-access and reach the Web UI as Entra ID app-role claims (RWB-P4-E1022-APP), so the harness makes no authorise call.

#### 12.3 Events published

None. The harness publishes no business event, and no workflow payload is published to Kafka.

#### 12.4 Events consumed

None. This story consumes no Kafka topic: the smoke run is started by the harness on a task queue, not by an event, and no consumer group is created for the suite.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Owner | Use in the suite |
|---|---|---|---|---|
| `PlatformSmokeWorkflow` with workflow ID `platform-smoke-20261116` | Workflow, one of the templates of the platform workflow kit | the queue of the one wave-1 service named in configuration | RWB-PLT-E1070-APP (platform workflow kit) | Started once with the workflow ID as the idempotency key, survives a frontend pod delete and completes on its timer (AC4, AC5) |
| `EvaluateRules` | Activity of the published activity contract | `rwb-decision` | P7 rwb-decision | The decision step that belongs to another service, executed as a Temporal call on the owner's queue and not as a REST call (AC4) |
| `RecordAndApply` | Activity of the published activity contract | `rwb-case` | P3 rwb-case | The write step executed on the owner's queue; repeated under the same workflow ID to prove no second write (AC4) |
| the remaining templates of the platform workflow kit (`Approval`, `Human task with SLA`, `Saga runner`, `Scheduled job`, `Notify`, `Partner instruction`) | Versioned workflow and activity library | the queue of the service that uses the template | RWB-PLT-WF | Not started by this story; named so the suite asserts that the smoke run uses a kit template and starts no business workflow |

The workflow ID is the business key of the run and therefore the idempotency key: a second start with `platform-smoke-20261116` returns the running execution and starts nothing. No case workflow, no stage workflow and no child workflow of any service is started by this story.

The worker registration contract is: one worker per service on its queue `rwb-<short>` in namespace `rwb-recovery`, with its own workload identity and a client certificate whose subject names the service; the queues are created at platform install from the service catalogue and a worker that polls another queue is refused; each service has its own codec key under the namespace key; the smoke workflow starts through RWB-PLT-E1070-APP on one named service queue (GAP-0378; ASM-0544); ASM-0545 fixes the call shape the suite asserts: one activity call on the owner's queue per cross-service step, under the workflow ID of the run.

#### 12.6 Schedules

None. No Temporal Schedule belongs to this story: the smoke run is started once by the harness, and the Schedule JOB-22 of Arch v5 slide 44 — the same workflow type at 06:00 — is owned and registered by RWB-PLT-E1070-APP. The suite reads that JOB-22 exists and changes nothing about it.

#### 12.7 Tables owned

None. Temporal persistence is outside the recovery schema and the harness owns no table in the ACE database, in `temporal` or in `temporal_visibility`. The stores it touches are listed in section 11 with their owners, and every statement the harness runs is a SELECT that must be refused.

#### 12.8 Contract fakes

None, and no service contract is faked: this is the integration level, so the real platform, the real nine service workers, the real certificates and the real access review replace the fakes of the app stories. A run configured with a fake worker or a fake frontend fails the preflight. The payload codec of the platform is out of scope and is neither exercised nor faked here. Definition of Ready item 22 (Fake published) is not applicable: the story has no contract dependency and uses no contract fake library, so there is no fake library version to publish.

#### 12.9 Call-type summary

| Call type | Provided by the suite | Consumed by the suite |
|---|---|---|
| REST | 0 | 0 |
| Kafka | 0 | 0 |
| Temporal | 0 | 14 calls: one namespace describe, nine queue describes, two starts of the same workflow ID, the `EvaluateRules` call on `rwb-decision` and the `RecordAndApply` call on `rwb-case` |
| File | 0 | 0 |

### 13. Solution plan

**Package.** `integration/recovery/wave1/temporal` in the ACE repository, package `<ACE base package>.recovery.itg.wave1.temporal`. Not part of a deployed service.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| HarnessRunner | Runner | Preflight against the platform contract and the nine worker deployments, run order, report and exit code |
| ConfigLoader | Service | Reads the namespace, the retention, the four search attributes, the nine queues, the probe queue, the workflow ID, the endpoints and the three test identities, and refuses a UAT or production target |
| QueuePollerProbe | Service | Describes the namespace and the nine queues, records the poller identity of each, and fails on a second namespace, a second registration of one service, a worker identity on two queues or a poller of another service (AC1) |
| TlsProbe | Service | Connects with no certificate, an expired certificate, a certificate for another namespace and each of the nine service certificates; starts a workflow on each attempt and records the TLS result and the frontend log line (AC2) |
| GrantProbe | Service | Runs the SELECT set as `temporal_svc` against each `rwb_*` schema and as each `rwb_*` login against the two Temporal databases, records SQLSTATE 42501 and reads the access review report (AC3) |
| CallShapeProbe | Service | Starts the smoke run, asserts the `EvaluateRules` call on `rwb-decision` and the `RecordAndApply` call on `rwb-case`, asserts no REST call in the chain, and repeats the start under the same workflow ID (AC4) |
| RestartProbe | Service | Deletes the frontend pod, waits for the replacement pod, re-reads the workflow ID, the run ID, the status and the history event count, and lets the timer complete the run (AC5) |
| PayloadProbe | Service | Reads the search attributes of the namespace and of the run and the payload of the run and of its two activity calls, and asserts the four Keyword attributes and no personal data field (AC6) |
| TimerProbe | Service | Reads the retention of the namespace, the timer of the run from the history of `temporal`, and the absence of the timer in a Quartz table and in the ACE shared job table (AC7) |
| ReportWriter | Service | One row per test case with the observable, the evidence and the elapsed time |

**Real-service topology.** The nine wave-1 services are reached as the real SIT services behind their own logins (DP-02): rwb-source-data (P1, schema `rwb_source_data`, queue `rwb-source-data`), rwb-integration (P2, schema `rwb_integration`, queue `rwb-integration`), rwb-case (P3, schema `rwb_case`, queue `rwb-case`), rwb-access (P4, schema `rwb_access`, queue `rwb-access`), rwb-document (P5, schema `rwb_document`, queue `rwb-document`), rwb-comms (P6, schema `rwb_comms`, queue `rwb-comms`), rwb-decision (P7, schema `rwb_decision`, queue `rwb-decision`), rwb-reporting (P9, schema `rwb_reporting`, queue `rwb-reporting`) and rwb-agent (P10, schema `rwb_agent`, queue `rwb-agent`). Each service keeps its own base `/api/recovery/<short>/v1` (DP-13) behind gateway-bff (DP-19) and its own topic `rwb.<short>.events.v1` (DP-14); none of those bases is called by this suite. Each schema named in this section is owned by the service named beside it; this suite owns no `rwb_*` schema and only attempts SELECT statements that must be refused (section 11).

**Fixtures**

| Fixture | Content | Used by |
|---|---|---|
| Queue set | The nine wave-1 queues with the expected workload identity of each service | AC1 |
| Certificate set | The nine service certificates, one expired certificate and one certificate issued for another namespace | AC2 |
| Grant set | The SELECT statements of `temporal_svc` against each `rwb_*` schema and of each `rwb_*` login against `temporal` and `temporal_visibility` | AC3 |
| Smoke run | The synthetic workflow `platform-smoke-20261116` on the probe queue, RUNNING on its timer, carrying CaseId, Stage, ProductGroup and QueueCode only | AC4, AC5, AC6 |
| Timer set | The timer of the run, the Quartz table names and the ACE shared job table name to search | AC7 |
| Namespace baseline | The namespace describe, retention 720 hours, the four Keyword search attributes and the Schedule JOB-22 | AC1, AC6, AC7 |

Decoupling patterns applied (Template and Rules v1 §R5.5):

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The dependency-added column records the build dependency of the owning story: DP-04, DP-06, DP-07, DP-14, DP-15 and DP-19 resolve to platform contract stories and stay with the service and platform builds that apply them; DP-01, DP-02, DP-05 and DP-13 add none. The H, C, I and X lists of this story are exactly those of the metadata table: no H, no C, no X, and the two I dependencies RWB-P4-E1022-APP and RWB-PLT-E1070-APP. An ITG story waits on no build of its own (§R5.4, §R5.7).

**Build steps**

1. Create the harness module next to the wave-1 harness RWB-ITG-W1J01-ITG and wire it to the SIT gRPC endpoint, the Web UI ingress and the platform contract of RWB-PLT-E1070-APP.
2. Build the ConfigLoader with the namespace, the retention, the four search attributes, the nine queues, the probe queue, the workflow ID and the three test identities; prove that a UAT or production target stops the run.
3. Implement AC1 with the namespace describe and the nine queue describes, and fail on a second namespace, a second registration or a foreign poller.
4. Implement AC2 with the three refusal certificates and the nine accepted service certificates, and record the frontend log line of each refusal.
5. Implement AC3 with the two grant directions and the access review report read.
6. Implement AC4: start the smoke run with the workflow ID `platform-smoke-20261116`, assert the `EvaluateRules` call on `rwb-decision` and the `RecordAndApply` call on `rwb-case`, assert no REST call in the chain, and repeat the start.
7. Implement AC5 with the frontend pod delete, the readiness wait, the workflow ID, the run ID, the status and the history event count, and implement AC6 and AC7 on the payload, the search attributes, the retention and the timer store.
8. Run the suite in SIT against the wave-1 release candidate, write the report and attach it to the wave-1 integration record.

**Configuration.** The namespace, the retention, the four search attributes, the nine queues, the probe queue, the workflow ID, the endpoints, the certificate names and the three test identities sit in configuration files; no platform value and no business value is coded in a test method.

**Done when.** The ten test cases of section 16 pass in SIT on the nine deployed wave-1 services, each of the nine shows exactly one poller on its own queue, the cross-service step is a Temporal call on the owner's queue with no REST hop, the smoke run keeps its workflow ID and run ID across the frontend delete and completes once, both grant directions are refused with SQLSTATE 42501, the retention is 720 hours with no timer in a Quartz or shared job table, no payload or search attribute holds personal data, and the report names every criterion with its observable.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | A user with no Workbench role opens the platform surface | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | A Workbench role other than RW-PLATADM or RW-AUDIT opens the platform surface | You cannot {action} here. Your role does not include it. |

A certificate failure shows in the frontend log and the TLS alert only, with the client identity and no personal data; no Workbench message is shown because no Workbench screen is involved. The same holds for a missing namespace, a foreign poller, a REST hop in the chain, a lost run, a grant across the boundary and a timer in a scheduler table: each is a harness report line and an alert for the platform owner, with the service, the queue and the observable, and none of them is user-facing text. The two message IDs and their texts are copied unchanged from RWB-E1-070 and the platform surface; this story adds no message ID.

### 15. Screens and states

Screens built by this story: none. No Workbench screen is built in this story and the harness renders nothing of its own. The operational view is the Temporal Web UI behind Entra ID with two states — operate for RW-PLATADM and read-only for RW-AUDIT — and a refused sign-in showing MSG-P4-001 or MSG-P4-002 with no namespace listed; those states and the role mapping belong to RWB-PLT-E1070-APP and RWB-P4-E1022-APP. The Grafana dashboard "Temporal platform" of the platform story shows the five services, request rate, errors and persistence latency and is referenced, not built, here. The Workbench admin screens for platform settings come in Epic 8.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-070-01-ITG | AC1, BR1, BR3 | Integration | The nine wave-1 queues and their pollers; the namespace describe; one namespace per environment; synthetic |
| TC-E1-070-02-ITG | AC3, BR5 | Integration | Roles `temporal_svc` and the nine `rwb_*` logins; cross-database SELECT in both directions; synthetic |
| TC-E1-070-03-ITG | AC2, BR4 | Integration | A worker with no certificate, an expired certificate and a certificate for another namespace; the nine service certificates; synthetic |
| TC-E1-070-04-ITG | AC6, BR8 | Integration | The search attributes of the namespace and of the run and the payloads of the run and its two activity calls; synthetic |
| TC-E1-070-05-ITG | AC7, BR2, BR9 | NFR | Namespace describe with retention 720 hours; the timer of the run read from `temporal` and searched in the Quartz and shared job tables; synthetic |
| TC-E1-070-06-ITG | AC5, BR7 | Integration | The smoke workflow `platform-smoke-20261116` and a frontend pod delete; workflow ID, run ID, status and history event count; synthetic |
| TC-E1-070-07-ITG | AC4, BR6 | Integration | The smoke run's `EvaluateRules` call on `rwb-decision` and `RecordAndApply` call on `rwb-case`, the repeated start and the absence of a REST call in the chain; synthetic |
| TC-E1-070-08-ITG | §12 contract | Contract | Temporal gRPC on port 7233 with mTLS, the Temporal Web UI ingress behind Entra ID OIDC, and the absence of any path under `/api/recovery/<short>/v1` in the chain; synthetic |
| TC-E1-070-09-ITG | AC8, BR10 | Integration | The run configuration of SIT and a UAT or production endpoint set as the harness target; synthetic |
| TC-E1-070-10-ITG | AC9, BR6 | Integration | The smoke run's `RecordAndApply` call on `rwb-case` and `EvaluateRules` call on `rwb-decision` with a timed-out first attempt; synthetic |

The seven legacy test cases are kept as ITG copies with the `-ITG` suffix and re-scoped to the platform-wide proof: the cluster and namespace checks of TC-E1-070-01 and TC-E1-070-05 and the Web UI role check of TC-E1-070-04 are owned at component level by RWB-PLT-E1070-APP and RWB-P4-E1022-APP, so their ITG copies assert the registered queues (AC1), the retention and the timer store (AC7) and what the platform exposes to an operator and an auditor (AC6); the run book of TC-E1-070-07 stays with RWB-PLT-E1070-APP, so its ITG copy asserts the call path the run book documents (AC4). No legacy test is re-run against the monolith and no new business value is added; the full test, with its Given, When and Then, is in Recovery Workbench Test Cases, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the namespace, the retention, the search attributes, the queue list, the probe queue, the workflow ID, the endpoints and the wait intervals are configuration (REQ-DRI-010).
- No personal data in search attributes, workflow payloads, workflow inputs, workflow history, fixtures, logs or the report: CaseId, Stage, ProductGroup and QueueCode only; the smoke payload is synthetic and the codec is out of scope here.
- One namespace and one worker per service on its own queue (BR2, BR3): a second namespace, a second registration, a worker on two queues or a poller of another service fails the run rather than being reported as a warning.
- One certificate per service (BR4): a shared certificate, a certificate for another namespace or an mTLS bypass fails the run; there is no bypass in SIT.
- A step in another service is a Temporal call on the owner's queue (BR6): a REST hop between two services, or a workflow calling a service base, fails the run.
- Temporal persistence never sits in the ACE database and no `rwb_*` schema is granted to `temporal_svc` (BR5); both directions are asserted, not only the one the platform story checks.
- No workflow timer in a Quartz table or a shared job table (BR9); the timer is read from the history of `temporal`.
- The harness owns no schema, no migration and no workflow of its own: every write is made by a service or by the platform, every statement the harness runs is a SELECT that must be refused, and its only workflow is the synthetic smoke run.
- The suite never starts a case workflow, never signals a case workflow, never edits a platform value and never uses production data or a production namespace.
- Synthetic data only, and the SIT data set is restored after the run.

### 18. Traceability

| Requirement or decision | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-007 | Every failure reaches a named owner; a tested way back | The platform release of RWB-PLT-E1070-APP, its namespace, its two databases, the smoke run with its workflow ID and run ID, and the report line that names the owner of each failure | TC-E1-070-01-ITG, TC-E1-070-03-ITG, TC-E1-070-06-ITG, TC-E1-070-07-ITG |
| REQ-DRI-010 | Environment values are versioned and changed without a code release | The namespace, the retention, the search attributes, the nine queues, the probe queue and the workflow ID, all read from configuration | TC-E1-070-05-ITG, TC-E1-070-01-ITG |
| DP-01, DP-02, DP-15 | Owner's schema and login per service, own Flyway sequence | The nine service logins and schemas of section 13 and the grant probes of AC3 | TC-E1-070-02-ITG |
| DP-13, DP-14, DP-19 | Per-service base, per-service topic, gateway-bff edge | The bases `/api/recovery/<short>/v1`, the topics `rwb.<short>.events.v1` and the absence of a REST call in the chain | TC-E1-070-07-ITG |
| DP-04, DP-05, DP-06, DP-07 | Embedded Drools kit, rwb-source-data for ACE data, parameters and reference data from rwb-case | The nine services keep their own kit and their own reads; the suite asserts that no service reads another service's schema or ACE view | TC-E1-070-02-ITG, TC-E1-070-01-ITG |
| ASM-0544 | One registration per service on its own queue, one identity and one certificate per service | The queue describes and the poller identities of AC1 and the certificate probes of AC2 | TC-E1-070-01-ITG, TC-E1-070-03-ITG |
| ASM-0545 | A cross-service step is one activity call on the owner's queue under the workflow ID of the run | The two activity calls and the repeated start of AC4 | TC-E1-070-07-ITG |
| ASM-0546 | The access review report and the SIT evidence location | The access review read of AC3 and the report of section 13 | TC-E1-070-02-ITG |
| GAP-0378 | The registration, certificate, smoke-queue and evidence elements are not specified in the sources | The configuration of section 13 and the probe defaults of section 12.5 | All |

The legacy AC1 to AC7 of RWB-E1-070 are owned at component level by RWB-PLT-E1070-APP, with the roles of AC4 taken from RWB-P4-E1022-APP; they are not re-stated here. This story adds no dependency and changes no schema.

### 19. Out of scope

- The platform contract, the release, TemporalSchemaJob, NamespaceBootstrapJob, the certificates, the OIDC configuration, the dashboard and the run book (RWB-PLT-E1070-CON, RWB-PLT-E1070-APP), and the workflow kit itself (RWB-PLT-WF).
- The Workbench roles, their letters and the DoA table (RWB-P4-E1022-APP) and the Web UI role mapping of the platform story.
- The payload codec, its AES-GCM keys in Key Vault, the decode server, the Temporal admin audit and the break-glass decode (RWB-E2-038).
- Case workflows, stage workflows, the case router and the child workflows of Epic 3, and the workflow and activity code of each service.
- Workflow-level alerts, the stuck workflow scanner and the workflow dashboard (RWB-E2-037).
- Backup, point-in-time restore, zone failover, the upgrade procedure and archive (RWB-E2-039).
- The `ace-collection` namespace, the Nexus operations into it and the ACE team's own Temporal use.
- The Temporal Schedules of the services, including JOB-22, which are owned and registered by RWB-PLT-E1070-APP and by each service.
- Workbench screens and the admin console (Epic 8).
- NFR load, performance and soak testing of the platform.
