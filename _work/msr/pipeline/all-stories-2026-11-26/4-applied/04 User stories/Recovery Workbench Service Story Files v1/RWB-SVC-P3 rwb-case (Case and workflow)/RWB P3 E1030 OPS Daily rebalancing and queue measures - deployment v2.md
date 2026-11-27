# RWB-P3-E1030-OPS Daily rebalancing and queue measures - deployment

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1030-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-030 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP17, DP19 |
| Parallel lane | L-P3-L |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-017, FR-P3-018) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-030 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P3-E1030-OPS). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **DevOps engineer**, I want **the daily rebalance and measure capability of `rwb-case` deployed as a chart with its migration, its Temporal Schedule, its topic subscriptions, its metrics, its alerts, its runbook and its feature flag**, so that **the 06:30 run and the measure snapshot land in SIT and UAT with evidence, and can be switched off or rolled back without a data change**.

The capability to deploy:

- Service `rwb-case`: schema `rwb_case`, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1` with `rwb.case.<Event>.v1`, topic `rwb.decision-record.v1` for the decision record, Temporal task queue `rwb-case` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.case`.
- Workloads: the worker deployment (`DailyCaseRun` with the `rebalance`, `takeQueueMeasures` and `publishBreachAlert` activities) and the api deployment (`GET /queues`).
- The Temporal Schedule `rwb-case-rebalance-daily` at 06:30, replacing the Quartz job JOB-06.
- One migration creating `queue_measure` and the `timer` index of the breach count.

### 2. Business rationale

The morning rebalance is the run that decides who works which case on the day: if the worker does not start, or the Schedule does not fire, cases stay in the overflow queue and the case list shows an owner nobody assigned. If the snapshot is served before it reconciles, two team managers read two depths for the same queue, which is the failure the legacy spreadsheets had.

This story keeps the operational envelope in one place: one chart, one values file per environment, the Schedule with its own guard and catch-up rule, the topic and dead-letter provisioning, the migration, the six metrics an operator needs, the alerts on the four failures that matter (run did not start, snapshot held, dead-letter growth, decision-record write rate), a runbook and the feature flag `rwb.p3.rebalance` so the moves can be taken out without touching the schema.

It is Day 1 work with no build dependency: the chart is authored against the platform charts of the workflow kit, the outbox library and the naming library, and it is exercised as soon as the build story reaches SIT.

### 3. Preconditions

- The platform charts the chart consumes — the workflow kit (RWB-PLT-E1071-CON), the outbox and inbox library (RWB-PLT-TE006-CON), the decision-record library (RWB-PLT-E1027-CON) and the naming library (RWB-PLT-E1047-CON) — are published in the chart repository at version 1. This is a consumption of a published chart, not a build dependency.
- The namespace `rwb-recovery` and the Temporal namespace `rwb-recovery` exist, with the task queue `rwb-case` registered.
- The Kafka cluster serves the business-event topics with the retry and dead-letter naming of the platform event library.
- The per-service database login exists and its secret is in the vault; the chart takes it by reference only, never by value.
- The read contract of RWB-P3-E1030-CON version 1 is published, so the api deployment can serve `GET /queues`.
- The deployment topology and the operating values — cluster, node pool, replica counts, resource limits, ingress host, the business time zone, the catch-up window of the Schedule and the alert thresholds — are Not specified in the source documents (GAP-2207; ASM-3623). The chart exposes every one as a value and this story ships no environment-specific default.

### 4. Flow

1. Chart authoring: one Helm chart for the service, one values file per environment, one overlay per wave. The capability adds a values block (`rebalance:`) for its activities, its Schedule, its subscriptions and its alerts.
2. Migration: a pre-install and pre-upgrade job runs the per-service Flyway sequence of DP-15 and applies `V1030_1__queue_measure.sql` before the new pods are ready; the job is idempotent and holds a lock.
3. Schedule: the release creates the Temporal Schedule `rwb-case-rebalance-daily` on task queue `rwb-case` with the cron and the business time zone of the values file, an overlap policy of skip, and a catch-up window as a value. A Schedule already present is updated in place by its own ID, never duplicated.
4. Deployment: the worker deployment (2 replicas as a starting value) and the api deployment (2 replicas as a starting value), both reading the same config map and the same secret reference.
5. Topic provisioning: the release creates the topic `rwb.case.events.v1` if it does not exist, with its retry topic and its dead-letter topic, the same for `rwb.decision-record.v1` as published by the platform library, and the consumer group of `rwb.case.TimerBreached.v1` for the breach alert.
6. Temporal: the worker is registered on task queue `rwb-case` with the kit's retry policy for the two activities, and the worker build ID is stamped so the replay gate can hold a rollout. No activity of this capability is non-retryable.
7. Flag: `rwb.p3.rebalance` starts off in SIT and UAT. Off: the rebalance step registers no activity and moves no case; the measure step still runs and still writes the snapshot, because the snapshot is read-only reporting work.
8. Smoke: the worker reports its pollers on `rwb-case`, the Schedule shows its next firing time, `GET /queues` answers through the gateway with an empty page before the first run, and the topic lag on the inbound subscription is zero.
9. Enable: the flag is switched on in SIT with a change record; the Schedule is triggered once by hand, the run moves the test cases, one `CaseTransferred` per move is on the topic, and the snapshot is read back as `PUBLISHED` or `HELD` with its reason.
10. Rollback: flag off returns the moves to inert without a schema change; a chart rollback re-points the deployments at the previous image and values and the migration job is forward-only; pausing the Schedule stops the next firing without losing it.

### 5. Exception paths

| ID | Situation | What the deployment does |
|---|---|---|
| D1 | The migration job fails | The release stops before the new pods; the old pods keep serving; the job log names the failing script |
| D2 | The worker crash-loops on the task queue | The rollout is held by the readiness gate; the previous worker keeps polling; an alert fires on the restart count |
| D3 | The Schedule does not fire at 06:30 | An alert fires on the missing firing for the business date; the runbook gives the manual trigger and the effect on the business date |
| D4 | A snapshot stays `HELD` | An alert fires on the held count; the runbook gives the reconciliation and re-run steps and names the data steward as the owner of the break |
| D5 | The dead-letter topic grows | An alert fires on rate and depth; the runbook gives the drain and replay steps |
| D6 | Two releases create the Schedule twice | The Schedule is addressed by its ID; a second creation is refused by the kit and the release reports it as a value error |
| D7 | The flag is switched on before the migration | The release order puts the migration before the flag; the flag is a release step, not a chart value, so it cannot precede the migration |
| D8 | The decision-record topic is unavailable | The move's transaction fails and the case is not moved (R-UNI-39); the activity is retried; the alert on the outbox backlog covers it |

Legacy messages kept where they still apply: MSG-P7-003 for a move whose record cannot be written, MSG-P3-011 for cases left without an owner, MSG-P3-029 for a held snapshot, MSG-P4-002 for a caller without the right. The deployment does not reword them.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Day 1; consumes published platform charts; no service code and no build dependency |
| Negotiable | Replica counts, resource limits, the time zone, the catch-up window, the thresholds and the host names are values |
| Valuable | The run and the snapshot can be deployed, observed, switched off and rolled back by one team with one chart |
| Estimable | One chart, one values block, one migration job, one Schedule, six alerts, one runbook |
| Small | One sprint-week for one pair |
| Testable | Every artifact has a test in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Daily rebalancing and queue measures - deployment

  Background:
    Given the chart of rwb-case version 1 in the chart repository
    Given the namespace rwb-recovery and the Temporal namespace rwb-recovery

  Scenario: AC1 Helm chart and values for the capability (new, D-RCV-60)
    Given the chart and its values file for an environment
    When the release is rendered without a cluster
    Then the worker deployment and the api deployment both render with the image, the config map and the secret reference of the per-service login
    Then the rebalance block renders the two activity names, the task queue rwb-case and the feature flag rwb.p3.rebalance
    Then no business value, no credential and no host name is typed in the template, and a lint of the chart reports no error

  Scenario: AC2 The Schedule, the retry policy and the worker registration (new, D-RCV-60)
    Given the rendered worker and Schedule configuration
    When the Schedule and the activity options are read
    Then the Schedule ID is rwb-case-rebalance-daily on task queue rwb-case with the cron, the business time zone and the catch-up window taken from the values file
    Then the overlap policy is skip and a second firing for the same business date does not start a second run
    Then the retry policy of the rebalance and measure activities is the kit's policy and no activity is listed as non-retryable
    Then the worker build ID is stamped for the replay gate

  Scenario: AC3 The migration, the topics and the decision record (new, D-RCV-60)
    Given the release values for the event platform
    When the migration job and the topic declarations are rendered
    Then the migration job applies V1030_1__queue_measure.sql before the new pods are ready
    Then the migration creates queue_measure with the unique key on queue and as-of time, and the expired-timer index
    Then rwb.case.events.v1 is declared with its retry topic and its dead-letter topic, and the consumer group of TimerBreached is declared
    Then the decision record uses rwb.decision-record.v1 as published by the platform library
    Then every topic name comes from the naming library and none is typed in a template

  Scenario: AC4 Metrics and alerts (new, D-RCV-60)
    Given the observability configuration of the release
    When the dashboards and the alert rules are read
    Then the dashboard shows the run duration, the moves per run, the cases left without an owner, the snapshot status per queue, the decision-record write latency and the outbox backlog
    Then an alert fires on a missing run for a business date and on a snapshot held beyond its threshold
    Then an alert fires on the dead-letter topic depth and rate, and on the restart count of the worker
    Then every alert names its runbook section

  Scenario: AC5 Runbook and feature-flag rollout (new, D-RCV-60)
    Given the runbook of the capability
    When the rollout and rollback sections are read
    Then the order is migration, worker, api, Schedule, smoke, flag on
    Then the rollback section gives flag off, Schedule pause, chart rollback and the dead-letter drain and replay steps
    Then the section on a held snapshot names the data steward, the message and the reconciliation step
    Then a dry run of the runbook in SIT is signed off with the case numbers and the business date it used
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The run fires daily at 06:30 after the allocation step of the same workflow run; a missed firing is an alert, never a silent skip | Batch and Scheduling Design v5, JOB-06; RWB-E1-030 section 4 |
| BR2 | The Schedule addresses one run per business date; a repeat finds balanced queues and moves nothing | RWB-E1-030 AC7; DP-10 |
| BR3 | The record and the move commit in one transaction; a failure leaves the case where it was | R-UNI-39; principle 5 |
| BR4 | Only a reconciled snapshot is served; a held snapshot is an alert and a break for the data steward | RWB-E1-030 BR6; MSG-P3-029 |
| BR5 | Topic and event names follow the naming rule; retry and dead-letter topics are created with the topic | DP-09; DP-14 |
| BR6 | The moves are switched by `rwb.p3.rebalance`; the snapshot runs whether the flag is on or off | RWB-E1-030 section 13 |
| BR7 | The migration is forward-only and runs before the new pods | DP-15 |
| BR8 | No credential, host name or business value is in a template | BR-P3-017; security baseline |
| BR9 | No file and no data-lake copy is deployed, because the lake path is removed | DP-17 |

The operating values — the business time zone, the catch-up window, the replica counts, the resource limits, the threshold of a held snapshot and the alert rates — are Not specified in the source documents (GAP-2207; ASM-3623). The chart exposes every value and this story ships no environment-specific default.

### 9. State transitions

| From | Event | To |
|---|---|---|
| Chart authored | lint and template render pass | Chart in the repository, version 1 |
| Chart version 1 | migration job succeeds | Schema at `V1030_1__queue_measure.sql` |
| Schema migrated | worker and api pods ready | Capability deployed, flag off, Schedule created and paused |
| Flag off, Schedule paused | flag on and Schedule resumed with a change record | Run live in the environment |
| Run live | flag off | Moves inert; the snapshot still runs; data and schema unchanged |
| Run live | chart rollback | Previous image and values; schema stays forward-only |
| Schedule live | a firing is missed | Alert; the runbook manual trigger runs the same workflow for the business date |
| Worker running | a non-deterministic change is deployed | The replay gate refuses the new build ID; the previous build ID keeps polling |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Authors the chart, the values, the jobs, the Schedule, the alerts and the runbook; runs the release |
| Release manager | Approves the release, the Schedule resume and the flag change in each environment |
| Platform team (workflow platform) | Owns the Temporal namespace, the Schedule policy and the cluster policy |
| Platform team (event platform) | Owns the topic policy and the retry and dead-letter naming |
| ACE DB team | Owns the per-service login and the migration grant |
| Security | Approves the secret reference and the network policy of the two deployments |
| RW-PLATADM | Triggers the Schedule by hand under Platform administration U |
| TechX build team | Consumes the runbook; does not change the chart in this story |

### 11. Data

The deployment writes no business data of its own.

| Item | Value | Source |
|---|---|---|
| Schema | `rwb_case` | Template and Rules §R4 |
| Migration applied | `V1030_1__queue_measure.sql` | RWB-E1-030 section 13, adapted to the per-service sequence |
| Tables touched by the migration | `queue_measure` created; a partial index on `timer` for the expired breach count | RWB-E1-030 section 13 |
| Topic owned | `rwb.case.events.v1` with retry and dead-letter | DP-09, DP-14 |
| Topic consumed | `rwb.decision-record.v1` (publish path of the library) | DP-03 |
| Temporal | Namespace `rwb-recovery`, task queue `rwb-case`, Schedule `rwb-case-rebalance-daily` | Template and Rules §R4 |
| Secret | The credential of the per-service login, by reference only; its name is Not specified in the source documents (GAP-2207; ASM-3623) | DP-02 |
| Configuration keys | `rebalance.enabled`, `rebalance.taskQueue`, `rebalance.schedule.id`, `rebalance.schedule.cron`, `rebalance.schedule.zone`, `rebalance.schedule.catchUpWindow`, `rebalance.schedule.overlapPolicy`, `outbox.relay.interval`, `alert.missingRun.threshold`, `alert.heldSnapshot.threshold` | This story |
| Feature flag | `rwb.p3.rebalance` | RWB-E1-030 section 13 |

No personal data is copied into a config map, a values file, a log or an alert annotation.

### 12. Contract

#### 12.1 REST operations provided

None. `GET /queues` is served by the api deployment of RWB-P3-E1030-APP and defined by RWB-P3-E1030-CON; this story only routes it.

#### 12.2 REST operations consumed

None.

#### 12.3 Events published

| Event | Topic | Owner | Provisioned by this story |
|---|---|---|---|
| `rwb.case.CaseTransferred.v1` | `rwb.case.events.v1` | P3 | The topic, its retry topic and its dead-letter topic |
| decision record | `rwb.decision-record.v1` | PLT library, consumed by P7 | The dead-letter policy of the shared topic |

#### 12.4 Events consumed

| Event | Topic | Owner | Consumer group provisioned |
|---|---|---|---|
| `rwb.case.TimerBreached.v1` | `rwb.case.events.v1` | P3 | Yes, for the breach alert |

#### 12.5 Workflows and activities

| Name | Kind | Queue | Deployment note |
|---|---|---|---|
| `DailyCaseRun` | Workflow | `rwb-case` | Registered by the worker; build ID stamped |
| `rebalance` | Activity | `rwb-case` | Registered only while `rwb.p3.rebalance` is on |
| `takeQueueMeasures` | Activity | `rwb-case` | Always registered; the snapshot runs whether the flag is on or off |
| `publishBreachAlert` | Activity | `rwb-case` | Registered with the breach listener |

#### 12.6 Schedules

| Schedule | Workflow | Cron and zone | Deployment note |
|---|---|---|---|
| `rwb-case-rebalance-daily` | `DailyCaseRun` | 06:30 daily in the business time zone of the values file, Not specified in the source documents (GAP-2207; ASM-3623) | Created by its own ID, overlap policy skip, catch-up window as a value, paused until the flag is on |

#### 12.7 Tables owned

| Table | Owner | Deployment note |
|---|---|---|
| `queue_measure` | P3 | Migration creates it with the unique key on queue and as-of time |
| `timer` | P3 | Migration adds the partial index on the expired breach count |
| `recovery_case`, `assignment`, `queue`, `queue_member` | P3 | Read and write by the capability; no change in this story |
| decision-record, outbox and inbox tables | PLT library, created in `rwb_case` | Provided by the platform charts |

#### 12.8 Contract fakes

None. The capability is exercised against the real contract server of RWB-P3-E1030-CON in SIT.

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 0, consumed 0 | Routes `GET /queues` of the api deployment |
| Kafka | 1 owned topic published, 1 subscription provisioned | `rwb.case.events.v1`, `rwb.decision-record.v1` |
| Temporal | 1 workflow, 3 activities registered, 1 Schedule created | `DailyCaseRun`, `rebalance`, `takeQueueMeasures`, `publishBreachAlert` |
| File | None | No file is deployed; the legacy lake extract is removed (DP-17) |

### 13. Solution plan

**Artifacts**

| Artifact | Path | Contents |
|---|---|---|
| Chart | `deploy/rwb-case/` | `Chart.yaml`, templates for api, worker, migration job, config map, service, network policy |
| Values | `deploy/rwb-case/values-<env>.yaml` | Image, replicas, resources, topology, the `rebalance` block, the alert thresholds, the secret reference |
| Migration job | `deploy/rwb-case/templates/migration-job.yaml` | Pre-install and pre-upgrade hook running the Flyway sequence |
| Schedule | `deploy/rwb-case/templates/schedule.yaml` | The Schedule by ID, its cron, zone, overlap policy and catch-up window |
| Topic declarations | `deploy/rwb-case/templates/topics.yaml` | The owned topic with retry and dead-letter, and the TimerBreached consumer group |
| Observability | `deploy/rwb-case/templates/observability.yaml` | The six dashboard panels and the four alert rules |
| Runbook | `docs/runbooks/rwb-case-rebalance.md` | Rollout, enable, manual trigger, held snapshot, rollback, drain and replay |

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; nothing is deployed for the lake |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The dependencies above are the platform charts this chart consumes at authoring time; the story itself carries no build dependency, as a Day-1 deployment story.

**Build steps**

1. Chart skeleton from the service template, with the worker and api deployments and the config map.
2. The `rebalance` values block, the flag key and the Schedule values.
3. The migration job with the Flyway sequence and the hook weights.
4. The Schedule by ID with its overlap policy, catch-up window and paused state.
5. The topic, retry, dead-letter and consumer-group declarations through the naming library.
6. The activity registration, the retry policy and the worker build ID.
7. The six dashboard panels and the four alert rules with runbook links.
8. The runbook, including the manual trigger, the held-snapshot step and the drain and replay steps.
9. The dry run in SIT: render, install, migrate, Schedule created, smoke, flag on, manual trigger, snapshot read back, flag off, rollback.

**Done when.** The chart renders and lints clean, the migration job applies `V1030_1__queue_measure.sql` in SIT and UAT, the Schedule fires at 06:30 and is visible with its next firing time, a manual trigger moves the test cases and one `CaseTransferred` per move is on the topic, one snapshot is `PUBLISHED` and one is `HELD` with MSG-P3-029, the four alerts fire on a forced failure and clear, and the runbook dry run is signed off.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-011 | Cases left without an owner | {count} new cases are waiting in the overflow queue for {team}. Every owner is at the caseload cap. |
| MSG-P3-028 | Service level breach alert | {count} cases in {queue} are past their service level. |
| MSG-P3-029 | Snapshot does not reconcile | The queue measures for {date} were not published: {check}. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

The deployment adds no message of its own to a caller. Its own failures are release errors with an exit code and a job log line naming the template and the value that failed; they are never shown to a case user. The alert on a held snapshot carries the check name only, as MSG-P3-029 does.

### 15. Screens and states

No screen. The operator surfaces are:

- The release pipeline view: render, lint, dry run, install, migrate, smoke, flag.
- The capability dashboard: run duration, moves per run, cases left without an owner, snapshot status per queue, decision-record write latency, outbox backlog.
- The Schedule view: `rwb-case-rebalance-daily` with its next firing time, its last result and its paused state.
- The alert list: the four rules of AC4, each with a runbook link.

The case list keeps the states of RWB-P3-E1030-APP: the new owner after a rebalance, the overflow marker and the queue measures of the latest published snapshot.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E1030-OPS-01 | AC1 | NFR | Chart lint and a template render of the worker and api deployments, the config map and the secret reference in all environments |
| TC-P3-E1030-OPS-02 | AC2 | NFR | The rendered Schedule: ID, cron, zone, catch-up window, overlap policy; the activity retry policy and the build ID |
| TC-P3-E1030-OPS-03 | AC3 | NFR | The migration job order and the created table and index; the topic, retry, dead-letter and consumer-group declarations against the naming library |
| TC-P3-E1030-OPS-04 | AC4 | NFR | A skipped firing, a held snapshot, a forced dead-letter write and a worker restart, each alert firing and clearing with its runbook link |
| TC-P3-E1030-OPS-05 | AC5 | NFR | The runbook dry run: migration, worker, api, Schedule, smoke, flag on, manual trigger, snapshot read back, flag off, rollback |

### 17. Guardrails

- No business value in a template or a values file: the cap, the method, the member capacity and the measure definitions are data of the service, not of the chart.
- No credential, host name or personal data in a values file, a config map, a log or an alert annotation; the login is a reference to a vault secret and its name is Not specified in the source documents (GAP-2207; ASM-3623).
- No read of another service's table from a job, a probe or a dashboard query (DP-01).
- Nothing is deployed for the data lake: no file export, no extract job and no lake credential (DP-17).
- The migration is forward-only; a rollback never re-runs a destructive script.
- Topic and event names come from the naming library; a template that types a topic name fails lint (DP-14).
- The Schedule is created by ID and paused until the flag is on; a second creation is refused, never duplicated.
- The moves are switchable by `rwb.p3.rebalance` without a data change; the snapshot is not switchable, because it is reporting work.
- A dead-letter message is drained and replayed, never discarded, and every drain is recorded in the runbook log.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-015 | Daily rebalancing; queue counts, ageing and breaches reported | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-17, FEAT-CWC-18, FEAT-WKM-11 | All recovery processes | R-UNI-19, R-UNI-30 | TC-P3-E1030-OPS-02, TC-P3-E1030-OPS-03, TC-P3-E1030-OPS-05 |
| REQ-RDF-012 | Baseline measures for cases by queue and age published | Epic 1, 3.3; Program, 5.1 | FEAT-RPT-02 | 15 Manage performance, data and AI | None | TC-P3-E1030-OPS-03, TC-P3-E1030-OPS-04 |

| Legacy reference | Where it is kept |
|---|---|
| JOB-06 Daily 06:30, rerun from the job monitor | Sections 4, 8, 9, 12.6, 17 |
| Event CaseTransferred (EV-04) | Sections 12.3, 16 |
| MSG-P3-011, MSG-P3-028, MSG-P3-029, MSG-P7-003, MSG-P4-002 | Section 14 |
| Feature flag `rwb.p3.rebalance` | Sections 4, 8, 11, 17 |
| `queue_measure` snapshot status | Sections 8, 12.7, 15 |
| Legacy key RWB-E1-030, story RWB-P3-E1030-APP, contract RWB-P3-E1030-CON, deployment RWB-P3-E1030-OPS | Metadata, section 12 |

### 19. Out of scope

- The rebalancing and measure code, its tests and its business rules (RWB-P3-E1030-APP).
- The OpenAPI and AsyncAPI documents and the contract fake (RWB-P3-E1030-CON).
- The platform charts themselves, the Kafka cluster policy and the Temporal namespace policy (RWB-PLT-E1071, RWB-PLT-TE006, RWB-PLT-E1047, RWB-PLT-E1044).
- The central decision ledger in rwb-decision and its own deployment.
- The gateway-bff route and the Epic 2 team queues screen (RWB-E2-011).
- The reporting projection and the Power BI report (rwb-reporting).
- Cluster sizing, node pools and the ingress host, which the platform team owns and this story consumes as values.
