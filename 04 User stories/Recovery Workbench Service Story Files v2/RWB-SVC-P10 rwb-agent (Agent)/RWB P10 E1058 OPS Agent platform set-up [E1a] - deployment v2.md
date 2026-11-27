# RWB-P10-E1058-OPS Agent platform set-up [E1a]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E1058-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-058 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP08, DP09, DP11, DP13, DP15, DP19, DP20 |
| Parallel lane | L-P10-C |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P10-E1058-OPS-16); the squad sizes it at refinement |
| Contract version | v1 (the /v1 path version of every operation in section 12.2) |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-N001-CON (delivery prerequisites of the service template, not per-story blockers); wave 0 release date Not specified in the source documents (GAP-1525); no capability of this story starts before these platform enablers exist |
| Contract dependencies | RWB-P10-E2032-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON, and the published contract of the P4 authorise call (ID Not specified in the source documents (GAP-2404)); RWB-P5-E1053-CON is added to this row in a later version when it is published (GAP-0610) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (FR-P10-001, FR-P10-002, FR-P10-003, FR-P10-024, FR-P10-025) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-058 for rwb-agent. The legacy platform was deployed as part of the monolith: one release, one migration set and one schema for every module. This story deploys the agent platform as its own Helm release of `rwb-agent`: the pipeline and the three environments, the api and worker deployments, the pre-deploy Flyway migration job in the order the service's own sequence fixes, the configuration and secret injection with no value in code, the feature flags taken from the platform library, the health and readiness signals, the dashboards and alerts of a run and an evaluation, the runbook and the rollback, and the blue-green path of the admin operations so a version load is never interrupted. It deploys no lake artefact and no business value. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 14 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform engineer**, I want **rwb-agent deployed from the service template with its api deployment, its worker deployment for queue `rwb-agent`, its pre-deploy Flyway migration job applying the service's own sequence to schema `rwb_agent`, its configuration and secret injection from the platform secret store and from Key Vault with no value in code, its feature flags from the platform library, its health, readiness and start-up signals, its dashboards and alerts for a run, a fallback and an evaluation, its runbook and rollback, and the blue-green path of the admin operations**, so that **the agent platform is released, observed and rolled back predictably in DEV, SIT and UAT, and an operator can see and act on a failed migration, an unready worker, a rise in fallbacks, a growing dead-letter count or a failed version load without reading code or a chart**.

### 2. Business rationale

The legacy story shipped with the monolith: the Flyway baseline `V0001` created the recovery schema, the agent tables arrived in the same migration set as every other module's, the application and the scheduler were one deployment, and a failed release was rolled back by redeploying the previous monolith build. In the target a service is one Helm release built by one pipeline with its own schema, login, topic and queue (DP-02, DP-09, DP-15), and the platform it hosts is what four later agent keys and the calling services of wave 1 stand on. Deployment is therefore part of the capability:

- A migration job that does not run before the rollout, or runs out of order, leaves a service that answers on a schema without its tables, and the app story has no way to know.
- A worker that is not on queue `rwb-agent` accepts no run, so every calling step falls back for the wrong reason and the fallback measure becomes meaningless.
- A configuration value written into a values file - a timeout, a floor, a price, a list value - breaks the no-business-value rule of the key and makes a version change a rebuild.
- An alert that fires only on an exception misses the condition this key cares about most: a rising fallback rate at a normal error rate, and a dead-letter count that grows while the topic looks healthy.
- The admin path loads and approves a version: a release that interrupts a load in flight leaves a half-written version and an officer without a prompt. The blue-green path of the admin operations is what prevents it.

This story makes the release repeatable and observable so the app story can be proved in SIT and the on-call rota can operate the service.

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB), and the Temporal workflow kit with namespace `rwb-recovery` is in place (RWB-PLT-WF, RWB-PLT-E1071-CON).
- The Kafka event platform provisions topics with a retry topic and a `.dlt` topic, and the schema registry validates a payload before the relay (RWB-PLT-EVT, RWB-PLT-TE006-CON).
- RWB-P10-E1058-INF is done or in flight: schema `rwb_agent` and its login exist, the Key Vault entries are wired to the workload identity, the topic and the queue are provisioned. The exact login name and the Key Vault entry names are Not specified in the source documents (GAP-0606; ASM-0848); the chart references them by name and never by value.
- RWB-P10-E1058-CON is baselined: the eleven operations, the schema keys, the EV-28 payload, the record payload and the fakes are published, so the pipeline can run the contract tests against them.
- The platform error envelope, the message catalogue and the alert routing are in force, so an alert can carry a message ID.
- The feature-flag library of the platform is available, because the flag of this service is a data row of that library and not a value in a chart (§R3 default ruling).
- The three environments DEV, SIT and UAT exist with the parameter scope of LOV-ENVIRONMENT.
- No build dependency: this story is Day 1 by rule (§R5.7) and sits in lane L-P10-C.

### 4. Flow

1. The pipeline builds one image and one chart version from one commit, runs the unit, component and contract tests against the fakes of RWB-P10-E1058-CON, scans the image and the dependencies, and publishes the chart.
2. The chart deploys the api deployment, the worker deployment and the service, with the login reference, the pre-deploy migration job, the probes and the platform secret references; no value of section 11 is written in the template.
3. The migration job runs the per-service Flyway sequence against `rwb_agent` in the order the sequence fixes, starting with the baseline of this service, and the rollout is not marked ready until the job succeeds.
4. The provisioning check confirms the topic `rwb.agent.events.v1` with its retry and `.dlt` topics and its producer ACL, the queue `rwb-agent` in namespace `rwb-recovery`, and the two registry subjects.
5. The configuration step injects the environment values - the service base URL, the INT-23 endpoint reference, the topic and queue names, the 2 second client budget, the evaluation poll interval and the log level - and reads the feature flags from the platform library; no business value is injected.
6. The dashboards are published: runs started and finished by agent and status, fallback rate, latency at the median and the 95th percentile, tokens and cost, evaluation runs and their duration, guardrail failures by check code, queue backlog, consumer lag and the `.dlt` count.
7. The alerts are wired to MSG-P10-001, MSG-P10-002 and MSG-P10-003 through the message catalogue, and to the conditions that have no message ID: a fallback-rate rise, a `.dlt` count above its reviewed value, a migration failure, an unready worker, a refused read and a failed version load.
8. The blue-green path of the admin operations is configured: the new version receives the admin traffic first on a second colour, a synthetic load and approve is exercised against it, and the old colour is retired only after the check passes.
9. A smoke step loads, approves, runs and evaluates a synthetic agent in a test namespace against the fakes and checks the run row, the event, the evaluation status and the probes.
10. The runbook entries are published with the check, the owner role and the recovery step, and the release records what it deployed and what it rolled back.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The migration job fails | The deployment stays unready and the pipeline stops; no traffic to the new version, and the sequence is not partially applied | None | AC2 |
| X2 | The readiness probe fails after the start-up window | The pod is removed from the service and the pipeline marks the release failed | None | AC4 |
| X3 | The worker does not poll queue `rwb-agent` | The readiness check fails, the release stops, and no run is accepted | None | AC4, AC5 |
| X4 | A feature flag of the service cannot be read from the platform library | The service starts with the documented fallback of the last known value and the flag alert fires; no flag value is written into a chart as a workaround | None | AC6 |
| X5 | A prompt or policy file fails a load check during the release check | The check reports 422 with MSG-P10-001 and the release continues, because the version in force is unchanged | MSG-P10-001 | AC7 |
| X6 | An evaluation is started on an empty sample during the smoke step | The check reports 422 with MSG-P10-002 and the release records it as expected | MSG-P10-002 | AC7 |
| X7 | A second evaluation of the same agent and sample is started | The check reports 409 with MSG-P10-003 and the release records it as expected | MSG-P10-003 | AC7 |
| X8 | The fallback rate rises above its reviewed value at a normal error rate | The fallback alert fires with the agent, the status and the window, and links the runbook entry | None | AC8 |
| X9 | The `.dlt` count grows while the topic looks healthy | The dead-letter alert fires with the subject and the count and pages the on-call rota | None | AC8 |
| X10 | The admin path fails the blue-green check | The new colour is not promoted, the old colour keeps serving the admin operations, and the release is marked failed | None | AC9 |
| X11 | A role without the right calls an admin operation | The refused-read count is visible on the dashboard only and never pages the on-call rota | MSG-P4-002 | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the platform topic and queue provisioning and the workflow kit; no application code is built here |
| Negotiable | Replica counts, resource sizes, probe timings, alert thresholds and the rollout window are environment values, not story decisions |
| Valuable | Makes the platform deployable, observable and repeatable in every environment, and keeps a version load from being interrupted by a release |
| Estimable | One chart, one pipeline stage, one migration job, two deployments, three probes, one provisioning check, nine dashboard panels, nine alert rules, six runbook entries and one blue-green step |
| Small | Fits one sprint with the runbook and the capacity note |
| Testable | Every criterion tests an artefact: the chart renders, the migration applies in order, the probes answer, the flags resolve, the alerts fire on a synthetic metric, and the blue-green check passes or blocks |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the rwb-agent platform

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the target environment is SIT
    Given the release date 30 November 2026 is tentative

  Scenario: AC1 The chart deploys the api and the worker with no business value and no lake artefact (new, D-RCV-60)
    Given the rwb-agent Helm chart and its values files
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the release declares the api deployment, the worker deployment, the pre-deploy migration job and the platform secret references, and no other workload
    Then no replica count, resource size, probe timing, alert threshold, topic name, queue name or business value is hard-coded in the template
    Then the release declares no lake credential, no file adapter, no outbound mount and no data-set job

  Scenario: AC2 The migration job applies the service's own sequence in order (new, D-RCV-60)
    Given an empty schema rwb_agent with its Flyway history table
    When the pre-deploy migration job runs
    Then the baseline of this service applies first and every later migration of rwb_agent follows in the order of the sequence, with the version recorded in the history table
    Then the rollout is not marked ready until the job reports success, and a failed job leaves the deployment unready and the pipeline stopped
    Then no migration touches another schema and no mixed-version schema is ever served
    Then the migration numbers beyond the baseline named by the source are Not specified in the source documents (GAP-0609; ASM-0856)

  Scenario: AC3 Configuration and secrets are injected and no value sits in code (new, D-RCV-60)
    Given the platform secret store, Key Vault and the environment values of the release
    When the pods start
    Then the login secret, the client certificate, its key and the INT-23 endpoint reference are read from Key Vault by the workload identity
    Then the topic name, the queue name, the base path and the 2 second client budget are environment values, and the model timeout, the confidence floor, the tool list, the price and the cap come from the approved policy row at run time
    Then no secret, no business value and no list value appears in a values file, a chart template, a config map, a log or a dashboard, and the pipeline scan fails the release when one does
    Then a rotation of a secret or of the endpoint reference needs no rebuild and no chart change

  Scenario: AC4 Health, readiness and start-up signals answer (new, D-RCV-60)
    Given a running pod of the api and of the worker
    When the readiness probe is called before the migration job and the start-up window complete
    Then the pod is not marked ready
    When the readiness and liveness endpoints are called after start-up
    Then both answer healthy without a database write
    Then a failing dependency - the schema, the topic, the queue or an owner contract - is reported as not ready and never as live-and-broken
    Then the worker reports ready only when it has polled queue rwb-agent

  Scenario: AC5 The worker, the queue and the consumer of the topic are in place (new, D-RCV-60)
    Given the worker deployment and the provisioning check
    When a synthetic backlog is queued on rwb-agent in namespace rwb-recovery
    Then the worker polls only its own queue with the release build ID on the version set and scales on backlog through KEDA, returning to the minimum when the backlog clears
    Then AgentRunWorkflow and its six activities are registered by the same worker
    Then the outbox relay of the service is configured with the producer ACL on rwb.agent.events.v1, its retry topic and its .dlt topic, and the inbox dedupe is enabled
    Then no consumer group outside the service's own is created by the release

  Scenario: AC6 The feature flags come from the platform library (new, D-RCV-60)
    Given the feature-flag library of the platform
    When the release resolves the flags of the service
    Then rwb.agent.platform is read as a data row of the library with its scope and its removal date, and is not a value of the chart
    Then with the flag off the orchestrator returns a fallback result with reason DISABLED and makes no model call, and the alert on the flag state is visible
    Then a flag value that cannot be read leaves the service on its last known value and fires the flag alert, and no flag is written into a values file as a workaround

  Scenario: AC7 The dashboards and alerts cover the run, the evaluation and the legacy messages (new, D-RCV-60)
    Given the published dashboard, the alert rules and the runbook
    When a synthetic run is replayed with a fallback, a guardrail failure, a failed version load, an empty sample and a second evaluation
    Then the dashboard shows runs by agent and status, fallback rate, median and 95th percentile latency, tokens and cost, evaluation runs and duration, guardrail failures by check code, queue backlog, consumer lag and the .dlt count
    Then the alerts carry MSG-P10-001 for a failed load, MSG-P10-002 for an empty sample, MSG-P10-003 for a second evaluation, and MSG-P4-002 for a refused read, with the legacy text
    Then the conditions without a message ID - a fallback-rate rise, a .dlt count above its value, a migration failure, an unready worker and a failed version load - carry the resource or the run and open no business message
    Then every alert links one runbook entry with the check, the owner role and the recovery step

  Scenario: AC8 The runbook, the rollback and the capacity note are in place (new, D-RCV-60)
    Given the runbook and the release record
    When a release is rolled back after a failed migration and after a failed admin check
    Then the previous chart version is redeployed with its image digest pinned, the schema is left at the version the pre-deploy migration job applied, and the release record names both versions
    Then the six runbook entries - migration failure, unready worker, fallback-rate rise, .dlt growth, failed version load and refused read - are accepted by the on-call rota
    Then the capacity note states the runs of a peak day, the evaluations of a peak day, the worker minimum and maximum, the connection cap of the login and the run duration at maximum
    Then the note records no lake throughput and no file window, because neither exists in this service

  Scenario: AC9 The admin operations are released blue-green (new, D-RCV-60)
    Given the two colours of the admin path in front of the gateway-bff route
    When a release is promoted
    Then the new colour serves the eleven operations of the contract baseline and answers the synthetic load, approve and listing check before any traffic is moved
    Then a load in flight on the old colour completes and is readable on the new colour, and no version is left half-written
    Then the admin traffic moves only after the check passes, the old colour keeps serving until it does, and a failed check leaves the old colour in place and marks the release failed

  Scenario: AC10 The release keeps one schema, one login and contract-only reads (new, D-RCV-60)
    Given the rwb-agent login (DP-02) reference, the rendered chart and the grants of schema `rwb_agent`
    When the release is deployed to SIT and the boundary scan runs
    Then the api, the worker and the pre-deploy migration job use the rwb-agent login (DP-02) reference and no other service's credential appears in the chart, the values or the rendered manifests
    Then the migration job and the service write only schema `rwb_agent`, and the scan fails the release when a grant of `rwb_agent` on the recovery schema or on another service schema, or a foreign key across schemas, is added
    Then case facts are read only through the rwb-source-data tool contract and extracted document fields only through the rwb-document tool contract, one hop with the 2 second client budget
    Then every neighbour of the service is reached only through its published contract
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One service, one schema, one login: the release uses the rwb-agent login (DP-02) reference and no other service's credential | DP-02; Arch v5 slide 41 |
| BR2 | The migration is a per-service Flyway sequence in schema `rwb_agent`, applied by a pre-deploy job before the rollout is ready, in the order of the sequence | DP-15; RWB-PLT-E1044-CON |
| BR3 | Every topic has a retry topic and a `.dlt` topic, and the consumer dedupes through the inbox | DP-09; Arch v5 slide 11 |
| BR4 | The worker polls only `rwb-agent` in namespace `rwb-recovery` and scales on backlog | §R4; Temporal and Drools design slide 11 |
| BR5 | No environment value and no business value is hard-coded: replicas, resources, thresholds, cadences and the policy values come from values files, the platform library and the approved row at run time; feature flags are read from the platform library and held in no chart | DP-06; DP-07; Template and Rules §R7.2 s17 |
| BR6 | An alert carries a message ID where one exists, the agreed text, and links one runbook entry | Template and Rules §R7.2 s14 |
| BR7 | A refused read is counted on the dashboard and never pages the on-call rota | MSG-P4-002 |
| BR8 | The service writes only schema `rwb_agent` and reads its neighbours only through their contracts; case facts only through the rwb-source-data tool contract and extracted document fields only through the rwb-document tool contract, one hop with a 2 s budget; no grant of rwb_agent on the recovery schema or on another service schema | DP-01; DP-11; Arch v5 slides 9 and 16 |
| BR9 | The release pins the image digest and the chart version and promotes the same artefact through the environments; a rebuild between environments is not allowed | ADR-021; Template and Rules §R8.2 |
| BR10 | A release never interrupts a version load: the admin operations move to the new colour only after the synthetic load, approve and listing check passes | Legacy section 4 and AC8; DP-19 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the contract tests pass the pipeline | Deploying |
| Deploying | Migration job complete and probes healthy | The schema is at the expected version, the worker has polled and both probes answer | Ready |
| Deploying | Migration job failed | The schema is not at the expected version | Failed; the previous release keeps serving |
| Ready | Release superseded | A new chart version is promoted | Rolling |
| Rolling | All pods on the new version and the admin check passed | The old ReplicaSet drains, the worker build ID is on the version set and the admin path answers on the new colour | Ready |
| Rolling | The admin check fails | A load, an approve or a listing check fails on the new colour | Failed; the old colour keeps serving the admin operations |
| Failed | Rollback | The previous chart version is redeployed with its digest | Ready (previous) |
| Ready | Feature flag off | rwb.agent.platform is off in the platform library | Ready (disabled); the orchestrator returns DISABLED and makes no model call |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the migration job, the provisioning check, the dashboards, the alerts, the runbook and the blue-green step |
| Platform administrator | Owns the `rwb-recovery` namespace, the topic provisioning, the queue and the flag rows of the platform library |
| ACE database administrator | Owns schema `rwb_agent`, the login, its grants and the migration job approval |
| Release manager | Approves the promotion of one artefact through the environments and the rollback |
| On-call operator | Runs the runbook entries and opens an incident when a fallback-rate or `.dlt` alert persists |
| RW-PLATADM | Reads and operates the agent runs and the versions in the running service, not in the cluster |
| RW-SECADM | Holds the break-glass right on the secret material and approves a rotation record |

The login name and the Key Vault entry names used by the chart are Not specified in the source documents (GAP-0606; ASM-0848); the chart references them through a name and never a literal password. The service login is agreed with the ACE database team, and this story refers to it as the rwb-agent login (DP-02) until a name is recorded (GAP-0610).

### 11. Data

| Item | Content | BR Field ID |
|---|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, environment name, rollout window and the blue-green check profile | Not specified in the source documents (DOR-RWB-P10-E1058-OPS-7) |
| Schema | `rwb_agent`, migrated by the pre-deploy job on the service's own Flyway sequence; the agent tables and the library objects of the contract baseline; the first migration is V10_001__agent_runtime.sql for the six agent tables and later migrations take the next numbers of the sequence | Not specified in the source documents (DOR-RWB-P10-E1058-OPS-7) |
| Topics | `rwb.agent.events.v1` produced with the retry topic and the `.dlt` topic; no consumer group of another service is created | Not specified in the source documents (DOR-RWB-P10-E1058-OPS-7) |
| Queue | Temporal task queue `rwb-agent` in namespace `rwb-recovery`, scaled on backlog | Not specified in the source documents (DOR-RWB-P10-E1058-OPS-7) |
| Feature flags | `rwb.agent.platform` and any later flag of the service, as rows of the platform feature-flag library with scope and removal date | Not specified in the source documents (DOR-RWB-P10-E1058-OPS-7) |
| Configuration | The service base path, the INT-23 endpoint reference, the topic and queue names, the 2 second client budget, the evaluation poll interval and the contract endpoint names of the owner services | Not specified in the source documents (DOR-RWB-P10-E1058-OPS-7) |
| Dashboard series | runs by agent and status, fallback rate, median and 95th percentile latency, tokens and cost, evaluation runs and duration, guardrail failures by check code, queue backlog, consumer lag, `.dlt` count, refused reads | Not specified in the source documents (DOR-RWB-P10-E1058-OPS-7) |
| Runbook entries | migration failure, unready worker, fallback-rate rise, `.dlt` growth, failed version load, refused read | Not specified in the source documents (DOR-RWB-P10-E1058-OPS-7) |
| Secrets | The `rwb_agent` login secret, the model-gateway client certificate and key, the endpoint reference and the Kafka client credential, all from the platform secret store and Key Vault | Not specified in the source documents (DOR-RWB-P10-E1058-OPS-7) |

The deployment topology detail - cluster names, node pools, replica counts, resource sizes, zone spread, ingress class and exact probe timings - is Not specified in the source documents (GAP-0609; ASM-0860); the chart exposes them as values and this story fixes only their names and the rule that they are not hard-coded. There is no lake path, no extract file and no data-set refresh time to document. The INT-23 host, port, certificate subject and certificate authority, the Key Vault entry names of the gateway call and of the login, the login name, the partition count, replication factor and retention of `rwb.agent.events.v1` and of its retry and `.dlt` topics, the worker concurrency, the budget measurement points and the alarm thresholds are Not specified in the source documents (GAP-0608); the release records each of them as a reviewed value per environment and never as a template constant, and their provisioning belongs to RWB-P10-E1058-INF.

### 12. Contract

#### 12.1 REST operations provided

The deployment exposes the eleven operations of the contract baseline behind the gateway-bff route, all relative to the base `/api/recovery/agent/v1`: `GET` and `POST /admin/agent-configs`, `POST /admin/agent-configs/{versionId}/approve`, `GET /admin/agent-runs`, `POST /admin/agent-samples`, `POST` and `GET /admin/agent-evaluations`, `GET /admin/agent-evaluations/{evaluationId}/report`, `GET /admin/agent-metrics`, `GET /cases/{caseId}/agent-outputs` and `POST /agent-runs/{runId}/feedback`. Owner rwb-agent (P10). The probes are cluster-internal and are not part of the API surface. The base `/api/recovery/agent/v1` follows DP-13, and the exact path names of the eleven operations belong to the service contract carried by the API Specification v4 and the Ownership Map, so the paths named in the FSD stay the behavioural reference (GAP-1520). The route path of the gateway-bff in front of these operations is agreed with the edge owner and is Not specified in the source documents (GAP-0613; GAP-0610).

#### 12.2 REST operations consumed

| Method | Path | Owner | Deployment need |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The tool read of a run; 2 s client budget (DP-11) |
| GET | `/api/recovery/case/v1/parameters/{key}` | P3 rwb-case | The parameter keys of the policy in force |
| GET | `/api/recovery/case/v1/reference-data/{lovCode}` | P3 rwb-case | LOV-AGENT, LOV-AUTONOMY, LOV-CONFIG-STATUS, LOV-EVAL-STATUS and LOV-SUBJECT-TYPE |
| GET | `/api/recovery/document/v1/documents/{documentId}` | P5 rwb-document | The tool read of the document and its extracted fields |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The right and the masking decision before each operation |
| GET | `/api/recovery/access/v1/masking-policies` | P4 rwb-access | The masking policy in force for the agent identity |

Every call is one hop with the 2 second client budget. The 60 second model call is not a REST call of the release: it happens inside the workflow and is provisioned by RWB-P10-E1058-INF.

#### 12.3 Events published

None by this story as code. The release wires the outbox relay to `rwb.agent.events.v1` with its retry topic and its `.dlt` topic, and the payload `rwb.agent.AgentRunCompleted.v1` is declared in RWB-P10-E1058-CON and written by RWB-P10-E1058-APP.

#### 12.4 Events consumed

None. The service consumes no topic in this key: CaseCreated and DocumentStored belong to the intake and screening keys of the service, and this release only enables the inbox dedupe for the consumers those keys add. No consumer group is created here.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| AgentRunWorkflow | Workflow, one execution per idempotency key; workflow ID form and duplicate-start policy Not specified in the source documents (CG-ALL-2538) | `rwb-agent` | Worker deployment with the release build ID on the version set |
| ResolveAgentConfig, GatherInputs, MaskInputs, CallModelGateway, CheckGuardrail, RecordAgentRun | Activities | `rwb-agent` | Registered by the same worker; mTLS to the Temporal frontend; activity timeouts as values |

#### 12.6 Schedules

None. The release registers no Schedule: the Arch v5 job map names no job for the agent platform (slide 44), a run is started by a calling step and an evaluation by a user request.

#### 12.7 Tables owned

| Table | Owner | Deployment element |
|---|---|---|
| agent_policy, agent_prompt, agent_run, agent_sample, agent_evaluation_run, agent_evaluation | P10 (rwb_agent) | Created by the per-service Flyway sequence in the pre-deploy migration job |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_agent | Created by the same migration job; used by the outbox relay and the idempotency of the loads |
| agent_feedback, agent_alert | P10 (rwb_agent) | Declared in the contract baseline and created by RWB-P10-E2032-APP and RWB-P10-E1063-APP; the release applies them when their migration is in the same sequence |

The pre-deploy job applies the sequence and touches no other schema (DP-15).

#### 12.8 Contract fakes

| Fake | Deployment use |
|---|---|
| rwb-case fake (RWB-P3-E1042-CON, RWB-P3-E1043-CON and the case read) | Runs in the pipeline and in the SIT smoke profile, so the release can start and the contract tests can run without rwb-case |
| rwb-document fake | Same, with a document and its extracted fields |
| rwb-access fake (RWB-P4-E1037-CON) | Same, with the rights, the masking decision and the masking policy |
| gateway-bff route stub and model gateway fake (INT-23) | Same, with the pass-through route and the five answer variants |

The fakes are test-only workloads; they are not deployed into UAT or production.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 11 provided, 6 consumed in the run path | The eleven operations of the contract baseline, and the case, parameter, reference-data, document, authorise and masking-policy calls; one hop, 2 s |
| Kafka | 1 published, 0 consumed | `rwb.agent.events.v1` with its retry topic and its `.dlt` topic through the outbox relay |
| Temporal | 1 workflow, 6 activities, 0 Schedules | AgentRunWorkflow and its six activities on queue `rwb-agent`, scaled on backlog through KEDA |
| File | None | The release carries no file, no lake credential and no data-set job; a policy, prompt or sample file arrives in a multipart body at run time |

**Contract baseline open points.** EV-28 `rwb.agent.AgentRunCompleted.v1` is the only member of the `rwb.agent.<Event>.v1` family the sources name; no source names a run-started or a run-failed member, so the contract declares EV-28 only and any further member is a new version of the topic's contract agreed with its consumers (GAP-0607). No source names an event for the completion of an evaluation run: an evaluation completes as a row state, the contract declares no event for it, and a name invented for it would be an unowned event type (GAP-0613). The element names of `AgentEvaluationReport` and `AgentMetric[]` are fixed and their types, the internal member names and types of `promotion_conditions` and `watch_measures` beyond the three legacy texts, and the type detail of the report members are left to the review with their owners and are Not specified in the source documents (GAP-0607; GAP-0613). The type and length of the inputs reference of the decision record are given by no source, and the record shape belongs to the decision-record library (GAP-0607). The legacy sample key is kept and `agent_run_daily` is left to the monitor story that names it (GAP-0607).

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | none here; the release wires the relay |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON for the app story; the endpoint is configured here |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON for the app story; the endpoint is configured here |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON for the app story; the route is opened here |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON for the app story; the relay is deployed here |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none here; the budget is configured here |
| DP-13 | the monolith API base | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON for the app story; the job is deployed here |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON for the app story; the route target is registered here |
| DP-20 | Agent client | rwb-agent contract | none here; the worker that carries the run is deployed here |

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-agent/` | Chart with the api deployment, the worker deployment, the service, the migration job, the config map, the secret references, the probes and the flag resolution |
| `helm/rwb-agent/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, rollout window, environment name and the flag library scope |
| Pipeline stage | Build, unit and contract tests, image and dependency scan, chart publish, promote the same artefact |
| Provisioning check | Topic with retry and `.dlt` and the producer ACL, queue `rwb-agent` in namespace `rwb-recovery`, the two registry subjects, the relay and the inbox dedupe |
| Migration job | The service's own Flyway sequence against `rwb_agent` as a pre-deploy job with a backoff limit; a failed job blocks the rollout |
| KEDA scaling | Worker scaled on the task-queue backlog with a minimum and a maximum from the values file |
| Dashboards | Nine series: runs by agent and status, fallback rate, latency at the median and the 95th percentile, tokens and cost, evaluation runs and duration, guardrail failures by check code, queue backlog, consumer lag, `.dlt` count and refused reads |
| Alerts | Rules for MSG-P10-001, MSG-P10-002, MSG-P10-003, MSG-P4-002, the fallback-rate rise, the `.dlt` count, the migration failure, the unready worker and the failed version load |
| Runbook | Six entries: migration failure, unready worker, fallback-rate rise, `.dlt` growth, failed version load, refused read |
| Blue-green step | The two colours of the admin path, the synthetic load, approve and listing check, and the traffic move |

**Probes.** Readiness answers healthy only when the migration is at the expected schema version, the worker has polled queue `rwb-agent`, the topic is reachable and the last owner-contract read answered; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database. Exact paths and timings are values.

**Migration job.** Runs the per-service Flyway sequence for schema `rwb_agent` with the `rwb_agent` login as a pre-deploy job with a backoff limit; a failed job blocks the rollout and the release, and the schema is never left at a version the running release does not expect. The baseline of the service is named by the source; the later numbers come from the sequence (ASM-0856).

**Alert mapping carried over from the legacy story.**

| Message ID or condition | Condition | Alert | Route |
|---|---|---|---|
| MSG-P10-001 | A prompt, policy or sample file fails a load check | Load-refused alert with the kind, the agent and the check text | Platform on-call, ticket |
| MSG-P10-002 | An evaluation is started on an empty sample | Evaluation-refused alert with the agent and the sample | Counted on the dashboard, no page |
| MSG-P10-003 | A second evaluation of the same agent and sample | Counted on the dashboard and in the run log | No page |
| MSG-P4-002 | A role without the right calls an admin operation | Refused-read count on the dashboard | No page |
| None (fallback rise) | The fallback rate rises above its reviewed value at a normal error rate | Fallback alert with the agent, the status and the window | Platform on-call, page |
| None (`.dlt` growth) | The `.dlt` count grows while the topic looks healthy | Dead-letter alert with the subject and the count | Platform on-call, page |
| None (migration failure) | The pre-deploy job fails | Release alert with the sequence version and the schema | Platform on-call, page |
| None (unready worker) | The worker does not poll the queue after the start-up window | Readiness alert with the queue and the build ID | Platform on-call, page |
| None (failed version load) | The blue-green check fails on a load, an approve or a listing | Release alert with the operation and the colour | Platform on-call, ticket |

**Blue-green.** The admin operations run on two colours behind the gateway-bff route. A release deploys the new colour, runs the synthetic load, approve and listing check against it, and moves the admin traffic only when the check passes; the old colour keeps serving until then, and a load in flight on the old colour completes and stays readable on the new one. The read operations follow the admin traffic, so a listing never shows a version the store does not hold.

**Capacity.** The plan states, per environment, the runs of a peak day, the evaluations of a peak day, the worker minimum and maximum, the connection cap of the login and the run duration at maximum. The target is the legacy measure: an agent answer or a recorded fallback inside its budget on the runs of a normal day. No lake throughput and no file window appear in the plan, because neither exists in this service.

**Done when.** The chart renders in all three environments, the pipeline promotes one artefact, the migration job applies the sequence in order on an empty schema, the probes answer, the queue and the relay are verified by a test, the flags resolve from the platform library, the nine alerts fire on synthetic metrics, the blue-green check blocks a bad release, the capacity note is reviewed and the six runbook entries are accepted by the on-call rota.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-001 | A prompt, policy or sample file fails a load check | The {kind} file for {agent} was refused: {check}. The version in force is unchanged. |
| MSG-P10-002 | Evaluation started on a sample with no labeled rows | Sample {sample} has no labeled rows for {agent}. Load the labels before you run the evaluation. |
| MSG-P10-003 | Evaluation started while the same one is running | An evaluation of {agent} on sample {sample} is already running. Wait for it to finish. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

The four texts are copied unchanged from the legacy story and this story adds no message ID. The deployment adds the alert routing and the runbook link, never a new wording. The conditions without a message ID - a fallback rise, a `.dlt` growth, a migration failure, an unready worker and a failed version load - keep none.

### 15. Screens and states

The deployment serves no screen of its own. The admin reads it exposes stand behind the gateway-bff route and will feed the agent monitor screen SCR-46 of RWB-P10-E1063-APP, whose states empty, loading, error and no access are Not specified in the source documents (CG-ALL-2542); this story registers the route target and the health check of the eleven operations only, and the screen field list and the composite route specification belong to the edge and monitor stories. The operator-facing surfaces of this story are the pipeline run view, the release view, the dashboard, the alert page and the runbook.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P10-E1058-OPS-01 | AC1, BR5, BR9 | NFR | The chart rendered for DEV, SIT and UAT with a pinned digest; a scan of the rendered manifests for a hard-coded value, a lake artefact and a second workload |
| TC-P10-E1058-OPS-02 | AC2, BR2 | NFR | An empty `rwb_agent` schema; the sequence applied in order; a failed migration that blocks the rollout; a migration that names another schema |
| TC-P10-E1058-OPS-03 | AC3, BR3 | NFR | The Key Vault read by the workload identity; the environment values injected; the scan for a secret or a business value in the values, the config map and the log; a rotation without a rebuild |
| TC-P10-E1058-OPS-04 | AC4, BR4 | NFR | Readiness false before the migration and the start-up window, then true; liveness true throughout; a failing dependency reported as not ready; neither probe writes |
| TC-P10-E1058-OPS-05 | AC5, BR4 | NFR | A backlog on queue `rwb-agent` scales the worker; the build ID is on the version set; the workflow and six activities are registered; the relay and the `.dlt` route are configured |
| TC-P10-E1058-OPS-06 | AC6, BR5 | Contract | The flag read from the platform library; the flag off returning DISABLED with no model call; an unreadable flag leaving the last known value and firing the flag alert |
| TC-P10-E1058-OPS-07 | AC7, BR6, BR7 | NFR | A synthetic replay of a fallback, a guardrail failure, a failed load, an empty sample and a second evaluation; the nine alerts with the four legacy texts and one runbook entry each |
| TC-P10-E1058-OPS-08 | AC8 | End to end | A rollback after a failed migration and after a failed admin check; the previous digest redeployed; the six runbook entries; the capacity note |
| TC-P10-E1058-OPS-09 | AC9, BR10 | End to end | Two colours of the admin path; a synthetic load, approve and listing on the new colour; a load in flight during the move; a failed check that leaves the old colour serving |
| TC-P10-E1058-OPS-10 | ASM-3438, BR1, BR8 | NFR | The pre-deploy job run on an empty `rwb_agent` schema; each table of section 12.7 checked for its owner and schema; a table of another schema in the sequence refused; the rwb-agent login used and no other credential |
| TC-P10-E1058-OPS-11 | AC10, BR1, BR8 | NFR | The chart and the values scanned for a second service credential; the api, the worker and the migration job checked against the rwb-agent login (DP-02); a grant of `rwb_agent` on the recovery schema, a grant on another service schema and a cross-schema foreign key refused; the case and document reads through the rwb-source-data and rwb-document tool contracts, one hop with the 2 second client budget |

### 17. Guardrails

- No business value in a values file: the model, the timeout, the floor, the tool list, the price and the cap are read from the approved policy row, and the parameter keys and lists from the rwb-case contracts (DP-06, DP-07, BR5).
- No personal data in logs, dashboard series, alert payloads or the runbook: run counts, agent codes, statuses, versions, check codes, dates and durations only.
- No cross-schema write and no cross-schema key: the migration job writes `rwb_agent` only and the boundary scan fails a change that adds a foreign key across schemas (DP-01, BR8).
- Every topic has a retry topic and a `.dlt` topic, and the consumer dedupes through the inbox (DP-09, BR3).
- The release pins the image digest and the chart version; a rebuild between environments is not allowed (BR9).
- No secret is written into a values file, a chart template, a dashboard or the runbook; all secrets come from the platform secret store and Key Vault (BR3).
- Every flag comes from the platform library and none is written into a chart, so a flag change is a data change and not a release (BR5).
- A release never interrupts a version load: the admin operations move colour only after the synthetic check passes (BR10).
- The tool gateway is read-only, and the allowed tool list on the policy row is an allow list that can only narrow what a run may read; a tool that writes is an open question and not a requirement (GAP-1528).

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-ACA-010 | Agents run under service identities with the same role checks as people | The login reference, the worker identity and the refused-read alert | TC-P10-E1058-OPS-03, TC-P10-E1058-OPS-07 |
| REQ-ACA-005 | Personal data masked by role in every agent call | The masking-policy endpoint configured for the run and the log scan of the release | TC-P10-E1058-OPS-03 |
| REQ-DRI-010 | Every threshold, limit and name is versioned and changed without a code release | The policy values read at run time and the flags read from the platform library | TC-P10-E1058-OPS-06 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The six consumed contracts configured with the 2 s budget and the route target of the eleven operations | TC-P10-E1058-OPS-01, TC-P10-E1058-OPS-05 |
| ADR-021 | Per-service Flyway and migration ownership | The pre-deploy migration job and the order of the sequence | TC-P10-E1058-OPS-02, TC-P10-E1058-OPS-10 |
| ADR-023 | Observability per service | The nine dashboard series, the nine alerts and the six runbook entries | TC-P10-E1058-OPS-07 |
| D-RCV-60 DP-19 | A screen reaches the service only through the gateway-bff route | The route target registration and the blue-green path of the admin operations | TC-P10-E1058-OPS-09 |
| ASM-0860 | Replica counts, resource sizes, probe timings, rollout window and alert thresholds are reviewed values per environment | The values files, the probes and the alert rules | TC-P10-E1058-OPS-01, TC-P10-E1058-OPS-04, TC-P10-E1058-OPS-07 |

### 19. Out of scope

- The application code of the operations, the gateway client, the store, the guardrail, the harness and the workflow (RWB-P10-E1058-APP).
- The contract documents, the schema keys, the payloads and the fakes as published artefacts (RWB-P10-E1058-CON); this story deploys the test copies only.
- The network path, the login, the Key Vault entries, the topic provisioning, the queue, the sizing figures and the platform budgets (RWB-P10-E1058-INF).
- The platform topic provisioning implementation, the Temporal cluster and the KEDA operator (RWB-PLT-EVT, RWB-PLT-WF and RWB-PLT-OBS).
- The exact cluster topology, node pools, replica counts, resource sizes and probe timings (GAP-0609).
- The agent monitor screen SCR-46, its dashboard and its measures (RWB-P10-E1063-APP), and the four other agent keys of the service.
- The end-to-end run of the legacy criteria (RWB-ITG-E1058-ITG) and the harness (RWB-ITG-W1J01-ITG).
- The legacy criterion AC5 of the intake key (a stale input flagged from a COMPLETED ALS row) and its test case TC-E1-059-05, which the split places with RWB-ITG-E1059-ITG (wave 1) and which this story does not reconstruct; which story of the epic serves the sample and the evaluation operations is agreed with the evaluation story (GAP-0610).
