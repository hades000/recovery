# RWB-P3-E1021-OPS Transfer rules and engine v1 - deployment

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1021-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-021 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P3-J |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-007, FR-P3-012, FR-P3-013, FR-P3-030, FR-P3-031) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-021 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **DevOps engineer**, I want **the transfer capability of `rwb-case` deployed as a chart with its two deployments, its migration, its topic subscriptions, its Temporal retry policy, its metrics, its alerts, its runbook and its feature flag**, so that **a rule transfer and a manual transfer run in SIT and UAT with evidence, and can be switched off or rolled back without a data change**.

The capability to deploy:

- Service `rwb-case`: schema `rwb_case`, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1` with `rwb.case.<Event>.v1`, topic `rwb.decision-record.v1` for the decision record, Temporal task queue `rwb-case` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.case`.
- Workloads: the api deployment (the gateway's `POST /cases/{caseId}/transfer` and `POST /cases/{caseId}/legal-hold`) and the worker deployment (`CaseWorkflow`, `DailyCaseRun`, the `EvaluateRules` and `transfer` activities).
- Database login: the per-service login of DP-02. Its name and its credential reference are Not specified in the source documents (GAP-0688; ASM-1235); the chart refers to "the rwb-case login (DP-02)" and takes the secret by reference only, never by value.

### 2. Business rationale

The transfer of a case between teams is the busiest write path of the case service in wave 1: eight trigger events, the morning allocation step and the manual call all move a case through it. If the worker, the topic subscriptions or the retry policy are wrong, cases stop moving and the case record shows a queue and an owner that nobody is working, which is the exact failure the legacy process had with email hand-offs.

This story keeps the operational envelope of the capability in one place: one chart, one values file per environment, the retry policy the Temporal and Drools design fixes, the topic and dead-letter provisioning of DP-09 and DP-14, the four metrics an operator needs, the alerts on the two failures that matter (no package in force, and a growing dead-letter topic), a runbook and the feature flag `rwb.p3.transfer` so the capability can be taken out without touching the schema.

It is Day 1 work with no build dependency: the chart is authored against the platform charts of the workflow kit, the outbox library and the naming library, and it is exercised as soon as the build story reaches SIT.

### 3. Preconditions

- The platform charts the chart consumes — the workflow kit (RWB-PLT-E1071-CON), the outbox and inbox library (RWB-PLT-TE006-CON), the decision-record library (RWB-PLT-E1027-CON), the Drools kit (RWB-PLT-E1072-CON) and the naming library (RWB-PLT-E1047-CON) — are published in the chart repository at their version 1. This is a consumption of a published chart, not a build dependency; the story has no build dependency.
- The namespace `rwb-recovery` and the Temporal namespace `rwb-recovery` exist, with the task queue `rwb-case` registered.
- The Kafka cluster serves the business-event topics, with the retry and dead-letter naming of the platform event library.
- The per-service login of DP-02 exists and its secret is in the vault; the name is Not specified in the source documents (GAP-0688; ASM-1235).
- The transfer contract of RWB-P3-E1021-CON version 1 is published, so the api deployment can serve the two operations.
- The deployment topology of the capability — cluster, node pool, replica counts per environment, ingress host and the resource limits — is Not specified in the source documents (GAP-0691; ASM-1238); the chart takes every one of them as a value and the story does not choose defaults for an environment.

### 4. Flow

1. Chart authoring: one Helm chart for the service, one values file per environment, one overlay per wave. The transfer capability adds a values block (`transfer:`) for its activity, its subscriptions and its alerts.
2. Deployment: the api deployment (2 replicas as a starting value) and the worker deployment (2 replicas as a starting value), both reading the same config map and the same secret reference.
3. Migration: a pre-install and pre-upgrade job runs the per-service Flyway sequence of DP-15 and applies `V1021_1__transfer.sql` before the new pods are ready; the job is idempotent and holds a lock.
4. Topic provisioning: the release creates the topic `rwb.case.events.v1` if it does not exist, with its retry topic and its dead-letter topic, the same for `rwb.decision-record.v1` (owned by the platform library), and the consumer groups of the worker for the seven inbound events of the capability.
5. Temporal: the worker is registered on task queue `rwb-case` with the retry policy of the Temporal and Drools design (1 s initial interval, back-off 2, 10 attempts) and `NoPackageInForce` listed as non-retryable; the worker build ID is stamped so the replay gate can hold a rollout.
6. Flag: `rwb.p3.transfer` starts off in SIT and UAT. Off: the worker does not register the `transfer` activity and the api answers 404 on the two operations.
7. Smoke: a platform smoke call reads `GET /cases/{caseId}` through the gateway, the worker reports its pollers on `rwb-case`, and the topic lag on the seven inbound topics is zero.
8. Enable: the flag is switched on in SIT with a change record; one rule transfer and one manual transfer on a test case are observed in the metrics and the decision record is read back from the topic.
9. Rollback: flag off returns the capability to inert without a schema change; a chart rollback re-points the deployments at the previous image and the previous values, and the migration job is forward-only.

### 5. Exception paths

| ID | Situation | What the deployment does |
|---|---|---|
| D1 | The migration job fails | The release stops before the new pods; the old pods keep serving; the job log names the failing script |
| D2 | The worker crash-loops on the task queue | The rollout is held by the readiness gate; the previous worker keeps polling; an alert fires on the restart count |
| D3 | A package version is not in force in SIT | `NoPackageInForce` is non-retryable; the alert counts it; the event stays on the inbound topic for redelivery once a version is in force (MSG-P3-027) |
| D4 | The dead-letter topic grows | An alert fires on the rate and the depth; the runbook gives the drain and replay steps |
| D5 | The topic does not exist at release time | The release creates it; if creation is refused by policy, the release fails before the worker starts, and the operator raises it to the platform team |
| D6 | A rollout changes the workflow code | The replay gate compares the build ID; a non-deterministic change is refused and the previous build ID keeps polling |
| D7 | The flag is switched on before the migration | The release order puts the migration before the flag; the flag is a release step, not a chart value, so it cannot precede the migration |
| D8 | The decision-record topic is unavailable | The record write and the state change fail together (R-UNI-39) and the activity is retried; the alert on the outbox backlog covers it |

Legacy messages kept where they still apply: MSG-P7-003 for a decision record that cannot be written, MSG-P3-027 for a package version not in force, MSG-GEN-004 for a version conflict on the case, MSG-P4-002 for a caller without the right. The deployment does not reword them.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Day 1; consumes published platform charts; no service code and no build dependency |
| Negotiable | Replica counts, resource limits, alert thresholds and host names are values |
| Valuable | The capability can be deployed, observed, switched off and rolled back by one team with one chart |
| Estimable | One chart, one values block, two jobs, four alerts, one runbook |
| Small | One sprint-week for one pair |
| Testable | Every artifact has a test in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Transfer rules and engine v1 - deployment

  Background:
    Given the chart of rwb-case version 1 in the chart repository
    Given the namespace rwb-recovery and the Temporal namespace rwb-recovery

  Scenario: AC1 Helm chart and values for the capability (new, D-RCV-60)
    Given the chart and its values file for an environment
    When the release is rendered without a cluster
    Then the api deployment and the worker deployment both render with the image, the config map and the secret reference of the rwb-case login (DP-02)
    Then the transfer block renders the activity name, its task queue rwb-case and its feature flag rwb.p3.transfer
    Then no business value, no credential and no host name is typed in the template, and a lint of the chart reports no error

  Scenario: AC2 Temporal retry policy and worker registration (new, D-RCV-60)
    Given the rendered worker configuration
    When the activity options of the transfer activity are read
    Then the retry policy states 1 s initial interval, back-off 2 and 10 attempts
    Then NoPackageInForce is listed as non-retryable
    Then the task queue is rwb-case in the namespace rwb-recovery and the worker build ID is stamped for the replay gate
    Then no Schedule is created by this story and DailyCaseRun keeps the one it has

  Scenario: AC3 Topic, retry topic and dead-letter topic (new, D-RCV-60)
    Given the release values for the event platform
    When the topic declarations are rendered
    Then rwb.case.events.v1 is declared with its retry topic and its dead-letter topic
    Then the consumer groups of the seven inbound events of the capability are declared
    Then the decision record uses rwb.decision-record.v1 as published by the platform library
    Then every topic name comes from the naming library and none is typed in a template

  Scenario: AC4 Metrics and alerts (new, D-RCV-60)
    Given the observability configuration of the release
    When the dashboards and the alert rules are read
    Then the dashboard shows transfers by trigger, manual transfers, refusals by message ID and the decision-record write latency
    Then an alert fires on a NoPackageInForce rate above zero in SIT and UAT
    Then an alert fires on the dead-letter topic depth and rate, and on the outbox backlog
    Then every alert names its runbook section

  Scenario: AC5 Runbook and feature-flag rollout (new, D-RCV-60)
    Given the runbook of the capability
    When the rollout and rollback sections are read
    Then the order is migration, worker, api, smoke, flag on
    Then the rollback section gives flag off, chart rollback and the dead-letter drain and replay steps
    Then the section on a refused transfer states that it changes nothing and that no override exists (GAP-0689; ASM-1236)
    Then a dry run of the runbook in SIT is signed off with the case numbers it used
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The transfer activity retries with 1 s initial interval, back-off 2 and 10 attempts; `NoPackageInForce` is non-retryable | Temporal and Drools design, slide 14 |
| BR2 | The rule package version is fetched and checksum-verified by the kit; the deployment never ships a rule table | DP-04; D-RCV-36 T5 |
| BR3 | The record and the state change commit in one transaction; a failure leaves the case unchanged | R-UNI-39 |
| BR4 | Topic and event names follow the naming rule; retry and dead-letter topics are created with the topic | DP-09; DP-14 |
| BR5 | The capability is switched by `rwb.p3.transfer`; off means no rule transfer and 404 on the two operations | RWB-E1-021, section 13 |
| BR6 | The migration is forward-only and runs before the new pods | DP-15 |
| BR7 | No credential, host name or business value is in a template | BR-P3-010; security baseline |
| BR8 | The Temporal timer replaces the legacy timer job inside the workflow; no new Schedule is created for the transfer | The timer ruling in the Ownership Map; RWB-P3-E1028-CON |
| BR9 | A repeated POST is answered from the stored response of its `Idempotency-Key`; the platform library provides the store | Architecture v5 slide 11; TSD P3 API-P3-006 |

The deployment topology — cluster, node pool, replica counts, ingress host and resource limits — is Not specified in the source documents (GAP-0691; ASM-1238); the chart exposes every value and this story ships no environment-specific default.

### 9. State transitions

| From | Event | To |
|---|---|---|
| Chart authored | lint and template render pass | Chart in the repository, version 1 |
| Chart version 1 | migration job succeeds | Schema at `V1021_1__transfer.sql` |
| Schema migrated | worker and api pods ready | Capability deployed, flag off |
| Flag off | flag on with a change record | Capability live in the environment |
| Capability live | flag off | Capability inert; data and schema unchanged |
| Capability live | chart rollback | Previous image and values; schema stays forward-only |
| Worker running | a non-deterministic change is deployed | Replay gate refuses the new build ID; the previous build ID keeps polling |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Authors the chart, the values, the jobs, the alerts and the runbook; runs the release |
| Release manager | Approves the release and the flag change in each environment |
| Platform team (event platform) | Owns the topic policy, the retry and dead-letter naming, and the cluster policy that can refuse a topic creation |
| ACE DB team | Owns the per-service login and the migration grant |
| Security | Approves the secret reference and the network policy of the two deployments |
| TechX build team | Consumes the runbook; does not change the chart in this story |

### 11. Data

The deployment writes no business data of its own.

| Item | Value | Source |
|---|---|---|
| Schema | `rwb_case` | Template and Rules §R4 |
| Migration applied | `V1021_1__transfer.sql` | RWB-E1-021 section 13, adapted to the per-service sequence |
| Tables touched by the migration | `recovery_case` (status_before_hold), `assignment` (transfer_reason_code, the partial unique index), `processed_event` | RWB-E1-021 section 13 |
| Topic owned | `rwb.case.events.v1` with retry and dead-letter | DP-09, DP-14 |
| Topic consumed | `rwb.decision-record.v1` | DP-03 |
| Temporal | Namespace `rwb-recovery`, task queue `rwb-case` | Template and Rules §R4 |
| Secret | The credential of the rwb-case login (DP-02), by reference only; its name is Not specified in the source documents (GAP-0688; ASM-1235) | DP-02 |
| Configuration keys | `transfer.enabled`, `transfer.taskQueue`, `transfer.retry.initialInterval`, `transfer.retry.backoff`, `transfer.retry.maxAttempts`, `transfer.retry.nonRetryable`, `outbox.relay.interval`, `alert.noPackageInForce.threshold` | This story |
| Feature flag | `rwb.p3.transfer` | RWB-E1-021 section 13 |

No personal data is copied into a config map, a values file, a log or an alert annotation.

### 12. Contract

#### 12.1 REST operations provided

None. The operations are served by the api deployment of RWB-P3-E1021-APP and defined by RWB-P3-E1021-CON; this story only routes them.

#### 12.2 REST operations consumed

None.

#### 12.3 Events published

| Event | Topic | Owner | Provisioned by this story |
|---|---|---|---|
| `rwb.case.CaseTransferred.v1` | `rwb.case.events.v1` | P3 | The topic, its retry topic and its dead-letter topic |
| `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | P3 | The same topic |
| decision record | `rwb.decision-record.v1` | PLT library, consumed by P7 | The consumer group and the dead-letter policy of the shared topic |

#### 12.4 Events consumed

| Event | Topic | Owner | Consumer group provisioned |
|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | P3 | Yes |
| `rwb.deviation.DeviationRaised.v1` | `rwb.deviation.events.v1` | S8 | Yes |
| `rwb.deviation.DeviationCleared.v1` | `rwb.deviation.events.v1` | S8 | Yes |
| `rwb.decision.ApprovalRequested.v1` | `rwb.decision.events.v1` | P7 | Yes |
| `rwb.payment.PaymentMissed.v1` | `rwb.payment.events.v1` | P8 | Yes |
| `rwb.document.DocumentStored.v1` | `rwb.document.events.v1` | P5 | Yes |
| `rwb.valuation.RouteDecided.v1` | `rwb.valuation.events.v1` | S1 | Yes |

#### 12.5 Workflows and activities

| Name | Kind | Queue | Deployment note |
|---|---|---|---|
| `CaseWorkflow` | Parent workflow | `rwb-case` | Registered by the worker; build ID stamped; Continue-As-New at stage end and at least every 28 days |
| `DailyCaseRun` | Workflow | `rwb-case` | Unchanged; keeps the Schedule it already has |
| `transfer` | Activity | `rwb-case` | Registered only while `rwb.p3.transfer` is on |
| `EvaluateRules` | Activity, from the kit | `rwb-case` | Registered by the kit; no Drools call in workflow code |

#### 12.6 Schedules

None. The transfer has no Schedule; `DailyCaseRun` keeps the Schedule it already has, and the timer expiry is a durable timer inside `CaseWorkflow`.

#### 12.7 Tables owned

| Table | Owner | Deployment note |
|---|---|---|
| `recovery_case` | P3 | Migration adds `status_before_hold` |
| `assignment` | P3 | Migration adds `transfer_reason_code` and the partial unique index `ux_assignment_open_case` |
| `queue` | P3 | Read; no change |
| `queue_member` | P3 | Read; no change |
| `task` | P3 | Read; no change |
| `timer` | P3 | Read; no change |
| `processed_event` | PLT library, created in `rwb_case` | Migration creates it |

#### 12.8 Contract fakes

None. The capability is exercised against the real contract server of RWB-P3-E1021-CON in SIT.

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 0, consumed 0 | Routes the two operations of the api deployment |
| Kafka | 2 owned topics published, 7 subscriptions provisioned | `rwb.case.events.v1`, `rwb.decision-record.v1` |
| Temporal | 2 workflows, 2 activities registered; 0 Schedules created | `CaseWorkflow`, `DailyCaseRun`, `transfer`, `EvaluateRules` |
| File | None | None |

### 13. Solution plan

**Artifacts**

| Artifact | Path | Contents |
|---|---|---|
| Chart | `deploy/rwb-case/` | `Chart.yaml`, templates for api, worker, migration job, config map, service, network policy |
| Values | `deploy/rwb-case/values-<env>.yaml` | Image, replicas, resources, topology, the `transfer` block, the alert thresholds, the secret reference |
| Migration job | `deploy/rwb-case/templates/migration-job.yaml` | Pre-install and pre-upgrade hook running the Flyway sequence |
| Topic declarations | `deploy/rwb-case/templates/topics.yaml` | The owned topic with retry and dead-letter, and the seven consumer groups |
| Observability | `deploy/rwb-case/templates/observability.yaml` | The four dashboard panels and the four alert rules |
| Runbook | `docs/runbooks/rwb-case-transfer.md` | Rollout, enable, rollback, drain and replay, refused transfer |

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The dependencies above are the platform charts this chart consumes at authoring time; the story itself carries no build dependency, as a Day-1 deployment story.

**Build steps**

1. Chart skeleton from the service template, with the api and worker deployments and the config map.
2. The `transfer` values block and the flag key.
3. The migration job with the Flyway sequence and the hook weights.
4. The topic, retry, dead-letter and consumer-group declarations through the naming library.
5. The activity registration, the retry policy and the worker build ID.
6. The four dashboard panels and the four alert rules with runbook links.
7. The runbook, including the refused-transfer statement and the drain and replay steps.
8. The dry run in SIT: render, install, migrate, smoke, flag on, one rule transfer, one manual transfer, flag off, rollback.

**Done when.** The chart renders and lints clean, the migration job applies `V1021_1__transfer.sql` in SIT and UAT, the two operations answer through the gateway, the four alerts fire on a forced failure and clear, one rule transfer and one manual transfer are visible in the dashboard with their decision records, and the runbook dry run is signed off.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-001 | Manual transfer without a reason | Choose a reason for the transfer. |
| MSG-P3-002 | Target owner at the cap | {owner} is at the caseload cap. Choose another owner or the team queue. |
| MSG-P3-005 | Move not allowed from the status | This case cannot move to {state} from {current}. |
| MSG-P3-011 | Target queue full, case in overflow | {count} new cases are waiting in the overflow queue for {team}. Every owner is at the caseload cap. |
| MSG-P3-027 | No TRANSFER version is in force for a rule trigger | The rule version was refused at the {check} check: {detail}. |
| MSG-GEN-004 | Second transfer on a changed record | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

The deployment adds no message of its own to a caller. Its own failures are release errors with an exit code and a job log line naming the template and the value that failed; they are never shown to a case user. The alert on MSG-P3-027 carries the package code only, as the message itself does.

### 15. Screens and states

No screen. The operator surfaces are:

- The release pipeline view: render, lint, dry run, install, migrate, smoke, flag.
- The capability dashboard: transfers by trigger, manual transfers, refusals by message ID, decision-record write latency, outbox backlog, dead-letter depth.
- The alert list: the four rules of AC4, each with a runbook link.
- The Temporal view: `CaseWorkflow` runs by queue, the replay gate status and the worker build ID per deployment.

The case record view keeps the states of RWB-P3-E1021-APP: the new queue and owner after a transfer, the hold banner and the overflow marker.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E1021-OPS-01 | AC1 | NFR | Chart lint and a template render of the api and worker deployments, the config map and the secret reference in all environments |
| TC-P3-E1021-OPS-02 | AC2 | NFR | The rendered activity options: 1 s, back-off 2, 10 attempts, NoPackageInForce non-retryable, queue rwb-case, build ID stamped |
| TC-P3-E1021-OPS-03 | AC3 | NFR | The topic, retry, dead-letter and consumer-group declarations rendered against the naming library |
| TC-P3-E1021-OPS-04 | AC4 | NFR | A forced NoPackageInForce, a forced dead-letter write and a stopped record topic, each alert firing and clearing with its runbook link |
| TC-P3-E1021-OPS-05 | AC5 | NFR | The runbook dry run: migration, worker, api, smoke, flag on, one rule transfer, one manual transfer, flag off, rollback |

### 17. Guardrails

- No business value in a template or a values file: the trigger rows, the queues, the reason list and the cap are data of the service, not of the chart (BR-P3-010).
- No credential, host name or personal data in a values file, a config map, a log or an alert annotation; the login of DP-02 is a reference to a vault secret and its name is Not specified in the source documents (GAP-0688; ASM-1235).
- No read of another service's tables from a job, a probe or a dashboard query (DP-01).
- No Drools call in workflow code: the kit runs only inside the `EvaluateRules` activity, and the deployment must not register a rule evaluation bean in a workflow bean (BR2).
- The migration is forward-only; a rollback never re-runs a destructive script.
- Topic and event names come from the naming library; a template that types a topic name fails lint (DP-14).
- The capability is switchable by `rwb.p3.transfer` without a data change and without deleting a message.
- A dead-letter message is drained and replayed, never discarded, and every drain is recorded in the runbook log.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-010 | Transfer by rule on eight triggers and manual request with a reason | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-10 | All recovery processes | R-UNI-20, R-UNI-21, R-UNI-40 | TC-P3-E1021-OPS-02, TC-P3-E1021-OPS-03, TC-P3-E1021-OPS-05 |
| REQ-CWC-016 | Every transfer logged with rule ID and version | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-10 | All recovery processes | R-UNI-39 | TC-P3-E1021-OPS-04 |
| REQ-WKM-003 | A case is transferred or reassigned manually only with a reason code from the agreed list | Epic 2, work management | FEAT-CWC-10 | All recovery processes | VR-P3-010-1; DL23 | TC-P3-E1021-OPS-01, TC-P3-E1021-OPS-05 |
| REQ-CWC-005 | A case is in one queue with one open assignment | Epic 1, 3.3 | FEAT-CWC-10 | All recovery processes | R-UNI-20 | TC-P3-E1021-OPS-01 |

| Legacy reference | Where it is kept |
|---|---|
| Package code TRANSFER, version "TRF-2026.11" | Sections 3, 5, 8, 14 |
| Event CaseTransferred (EV-04) | Sections 12.3, 16 |
| MSG-P3-001, MSG-P3-002, MSG-P3-005, MSG-P3-011, MSG-P3-027, MSG-GEN-004, MSG-P7-003, MSG-P4-002 | Section 14 |
| Feature flag `rwb.p3.transfer` | Sections 4, 8, 11, 17 |
| JOB-03 and JOB-05 as legacy references | Sections 8, 12.5, 12.6 |
| Legacy key RWB-E1-021, story RWB-P3-E1021-APP, contract RWB-P3-E1021-CON, deployment RWB-P3-E1021-OPS | Metadata, section 12 |

### 19. Out of scope

- The transfer capability code, its tests and its business rules (RWB-P3-E1021-APP).
- The OpenAPI and AsyncAPI documents and the contract fake (RWB-P3-E1021-CON).
- The platform charts themselves and the Kafka cluster policy (RWB-PLT-E1071, RWB-PLT-TE006, RWB-PLT-E1047, RWB-PLT-E1044).
- The rule package authoring, approval and promotion (RWB-P3-E1073-APP).
- The central decision ledger in rwb-decision and its own deployment.
- The gateway-bff route and the Epic 2 transfer screen (RWB-E2-012).
- Cluster sizing, node pools and the ingress host, which the platform team owns and this story only consumes as values.
