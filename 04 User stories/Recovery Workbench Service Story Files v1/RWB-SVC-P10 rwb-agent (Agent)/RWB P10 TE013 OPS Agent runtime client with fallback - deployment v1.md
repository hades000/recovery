# RWB-P10-TE013-OPS Agent runtime client with fallback

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-TE013-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 1 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP07, DP09, DP10, DP11, DP13, DP15, DP19, DP20 |
| Parallel lane | L-P10-M |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (FR-P10-001, FR-P10-002, FR-P10-003, FR-P10-004, FR-P10-008, FR-P10-009, FR-P10-010, FR-P10-011, FR-P10-015, FR-P10-018, FR-P10-024, FR-P10-025, FR-P10-026) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: deployment slice of RWB-TE-013 for rwb-agent. This story deploys the client capability of the key: the rwb-agent api and worker deployments from the service template, the pre-deploy migration job of `V10_002__agent_run_decision_link.sql` on the per-service Flyway sequence (**DP-15**), the worker on queue `rwb-agent` in namespace `rwb-recovery` with AgentRunWorkflow and the three client activities (**DP-10**, **DP-20**), the boundary wiring of the rwb-case reference lists (**DP-07**), the decision-record library with the publish right on `rwb.decision-record.v1` and its retry and `.dlt` topics (**DP-03**, **DP-09**), the approved autonomy policies and the legacy `rwb.agent.client` switch, the probes, dashboards, alerts carrying MSG-P7-003 and the fallback rate, the publication of the run read through gateway-bff (**DP-19**), the runbook, the rollback and the capacity plan. It deploys no lake artefact, no extract and no Quartz job table: the legacy dependence on RWB-TE-007 is retired under §R6. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform engineer**, I want **rwb-agent deployed from the service template with its api and worker deployments, its `V10_002__agent_run_decision_link.sql` migration job, its probes, its Temporal worker and KEDA scaling on the `rwb-agent` task queue, the wiring of the rwb-case reference lists and of the decision-record library with the publish right on `rwb.decision-record.v1` and its retry and `.dlt` topics, the approved autonomy policies and the legacy `rwb.agent.client` switch, the dashboards and alerts that watch a fallback rate, a record write failure and a refused link, the publication of the run read through the gateway-bff route, the runbook, the rollback and the capacity plan**, so that **a calling step can reach the agent client from day one in every environment, the fallback rate and every failed decision record are visible and actionable, and an operator can restart a stuck step, a refused link or a worker backlog without reading code and without a Quartz job table that no longer exists**.

### 2. Business rationale

The legacy story depends on a Quartz chain of RWB-TE-007 with its run books and its shared job table, an in-process orchestrator and a decision log writer of P7 inside the same deployment. In the target a service is a Helm release built by one pipeline with its own schema, login, topic rights, queue and Schedules (DP-02, DP-10, DP-15), the record is written by the calling step through a shared library into the ledger topic (DP-03), and the orchestrator is a workflow on the rwb-agent queue (DP-20). Deployment is therefore part of the capability:

- Without the worker on queue `rwb-agent` with AgentRunWorkflow and the three client activities, a submitted step would hang until its policy timeout and every step would fall back.
- Without the migration job, `agent_run.decision_log_id` is absent or unindexed and the link of a record to its run cannot be stored, so no step may act.
- Without the publish right on `rwb.decision-record.v1` and the relay, the ledger of rwb-decision falls behind the steps and an audit read of a case finds no record.
- Without the alert on a record write failure, a step that refuses to act looks like a quiet case rather than a decision that could not be recorded, and MSG-P7-003 is never seen.
- Without the route publication, the run read and its fallback column are unreachable from a screen and the fallback measure has no reader.

This story makes the capability observable and repeatable. It deploys and watches; it changes no business behaviour and holds no business value.

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB), and the Temporal workflow kit with namespace `rwb-recovery` is in place (RWB-PLT-WF, RWB-PLT-E1071-CON).
- The Kafka event platform provisions topics with a retry topic and a `.dlt` topic (RWB-PLT-EVT, RWB-PLT-TE006-CON), and the shared topic `rwb.decision-record.v1` exists with its rights (RWB-PLT-E1027-CON).
- The ACE database administrator has created schema `rwb_agent` and the login, with rights on `rwb_agent` only (DP-02). That login is Not specified in the source documents (GAP-0621; ASM-0913).
- The platform error envelope, the message catalogue and the alert routing are in force, so an alert can carry a message ID.
- The contract baseline of RWB-P10-TE013-CON is published: the two operations, their members, their refusals, the record payload and the three fakes.
- The baseline release of RWB-P10-E1058-OPS is known and deployed, because it owns the schema baseline, the topic `rwb.agent.events.v1` and the worker that runs the six baseline activities of AgentRunWorkflow.
- RWB-P3-E1043-CON (reference lists) and RWB-P7-E1027-CON (record read) are published for the boundary wiring.
- The three environments DEV, SIT and UAT exist with the parameter scope of LOV-ENVIRONMENT.
- The chart values, replica counts, probe paths and timings, resource sizes, topic partitions, worker concurrency, alert thresholds and deployment topology are Not specified in the source documents (GAP-0621; ASM-0912, ASM-0914).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The pipeline builds one image and one chart version from one commit, runs the unit, component and contract tests, scans the image and the dependencies, and publishes the chart.
2. The chart deploys the api and worker deployments with the `rwb_agent` login reference, the pre-deploy migration job of `V10_002__agent_run_decision_link.sql` after `V10_001__agent_runtime.sql`, and the probes; the job runs before the rollout is marked ready (AC1; DP-15).
3. The provisioning step checks the task queue `rwb-agent` in namespace `rwb-recovery` and the publish right of rwb-agent on the shared `rwb.decision-record.v1`, and confirms that the retry topic and the `.dlt` topic of the decision-record family are the platform's and bound to this producer; the release creates no topic and no consumer group (AC2; DP-03, DP-09).
4. The worker registers AgentRunWorkflow with its six baseline activities and the three client activities ResolveAutonomyMode, ApplyAutonomyMode and LinkDecisionRecord on queue `rwb-agent`, with the release build ID on the version set (AC2).
5. The configuration step wires LOV-AUTONOMY, LOV-AGENT and LOV-PRODUCT through the rwb-case reference-data contract, the record read through the rwb-decision contract, and the approved `agent_policy` rows with their modes, timeouts and prompt versions; no mode, timeout, agent code or check code is written into a values file (AC3; DP-07).
6. The legacy flag `rwb.agent.client` is registered with the platform flag library, off by default in DEV and on in SIT and UAT only after the smoke step answers (AC3).
7. The dashboards are published: step submissions by outcome, fallback rate per agent and policy version against the 10 percent target, runs by status, record writes and failures, refused links, worker backlog and refused reads (AC4).
8. The alerts are wired to MSG-P7-003 for a record write failure, to the fallback rate above target, to a refused link, to a `.dlt` message on the decision-record topic and to a failed migration, each linked to one runbook entry (AC4).
9. The route publication step registers the run read `GET /api/recovery/agent/v1/admin/agent-runs` behind the gateway-bff pass-through route, one hop, and checks the health of the route target (AC5; DP-19).
10. A smoke step submits a synthetic step for case "RW-2026-000201" against the three fakes, reads the outcome and the run through the route, and checks the record write, the link, the probes and the alerts (AC5, AC6).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The migration job of `V10_002__agent_run_decision_link.sql` fails | The deployment stays unready and the pipeline stops; no traffic to the new version and no step is linked | None | AC1 |
| X2 | The readiness probe fails after the start-up window | The pod is removed from the service and the pipeline marks the release failed | None | AC1 |
| X3 | The task queue is not registered, or the worker build ID is not on the version set | The release fails; a submitted step would otherwise wait until its policy timeout and fall back | None | AC2 |
| X4 | The publish right on `rwb.decision-record.v1` is missing, or a record lands in `.dlt` | The release fails on the missing right; a refused record is alerted with its reference and registry subject and a runbook entry is opened | None | AC2 |
| X5 | A record write fails at run time | The step does not act; the alert carries MSG-P7-003 with the step key, the agent and the business date and opens a ticket | MSG-P7-003 | AC4 |
| X6 | A link is refused with 409 because the run holds another record | The refused-link alert carries the run ID and both references and opens a ticket for the data steward; neither record is deleted | None | AC4 |
| X7 | The reference-data contract or the record read is unavailable during start-up | The readiness probe answers unready and the release is not marked ready; no step is served with a guessed mode | None | AC3 |
| X8 | The worker backlog passes its threshold on queue `rwb-agent` | KEDA scales the worker on the backlog and, if it persists, the on-call rota opens the backlog runbook entry | None | AC2 |
| X9 | The route publication fails or the route target is not healthy | The release fails and the run read stays unreachable; no partial route is left | None | AC5 |
| X10 | A role without the right reads agent runs | The refused-read count rises on the dashboard with MSG-P4-002 and never pages the on-call rota | MSG-P4-002 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the platform topic provisioning, the workflow kit and the published contracts; no application code is built here |
| Negotiable | Replica counts, resource sizes, partitions, concurrency, alert thresholds and cluster topology are environment values, not story decisions |
| Valuable | Makes the client reachable and observable from day one, keeps every step's record and link deployable, and keeps the retired Quartz chain out of the release |
| Estimable | One chart, one pipeline stage, one migration job, two deployments, two probes, one provisioning check, a Schedule-free worker registration, six dashboard panels, five alert rules and six runbook entries |
| Small | Fits one sprint with the runbook and the capacity plan |
| Testable | Every criterion tests an artefact: the chart renders, the probes answer, the queue is registered, the wiring comes from contracts, the alerts fire on a synthetic condition, the route answers within 2 s |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the rwb-agent agent runtime client capability

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the target environment is SIT

  Scenario: AC1 The chart deploys the api and worker with the decision-link migration (new, D-RCV-60)
    Given the rwb-agent Helm chart and its values files
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the release declares the api deployment and the worker deployment, the pre-deploy migration job of V10_002__agent_run_decision_link.sql and the platform secret references
    Then the migration job runs the per-service Flyway sequence in schema rwb_agent after V10_001__agent_runtime.sql and before the rollout is marked ready, and it creates no table
    Then agent_run holds decision_log_id and its index, and the step key index exists for the repeat lookup
    Then the release declares no Quartz job table, no job admin read and no lake artefact
    Then no replica count, resource size, timeout or mode is hard-coded in the template

  Scenario: AC2 The worker, the queue and the record topic are in place (new, D-RCV-60)
    Given the provisioning step and the worker deployment
    When a synthetic backlog is queued on rwb-agent in namespace rwb-recovery
    Then the worker polls only its own task queue with the release build ID on the version set and KEDA scales it on backlog
    Then AgentRunWorkflow, ResolveAutonomyMode, ApplyAutonomyMode and LinkDecisionRecord are registered by the same worker
    Then the release holds the publish right on rwb.decision-record.v1 and the retry topic and the .dlt topic of the decision-record family are bound to it, with the relay interval of the outbox
    Then the release creates no topic of its own and no consumer group, and no consumer group reads a topic of another service
    Then the legacy job table and its admin read are used by nothing in the release

  Scenario: AC3 The reference lists, the record read, the policies and the feature switch are wired by contract (new, D-RCV-60)
    Given the values files and the configuration step
    When the release is rendered and started
    Then LOV-AUTONOMY, LOV-AGENT and LOV-PRODUCT are read through the rwb-case reference-data contract and the record read through the rwb-decision contract
    Then the approved agent_policy rows carry the modes OFF, SHADOW and L1, timeout_seconds 60 and the prompt version, and no mode, timeout, agent code or check code appears in a values file or in the chart template
    Then the rwb.agent.client switch is off in DEV and on in SIT and UAT only after the smoke step answers, and off starts no run and writes the record with agent version null
    Then every secret is a reference to the platform secret store, and no secret value is in the chart, the dashboards or the runbook

  Scenario: AC4 Alerts and the runbook cover the fallback rate, the record failure and the refused link (new, D-RCV-60)
    Given the published dashboards and the runbook
    When a synthetic step is replayed with a fallback, a failed record write and a refused link
    Then the fallback-rate panel carries the rate per agent and policy version against the 10 percent target
    Then the record-failure alert carries MSG-P7-003 with the step key, the agent and the business date
    Then the refused-link alert carries the run ID and both record references and opens a ticket for the data steward
    Then the .dlt alert fires on a refused record with its record reference and its registry subject
    Then the refused-read count carries MSG-P4-002 and does not page the on-call rota
    Then every alert links one runbook entry with the check, the owner role and the recovery step

  Scenario: AC5 The probes and the smoke step answer through the route (new, D-RCV-60)
    Given a running pod of the api and of the worker
    When the readiness probe is called before the migration job and the start-up window complete
    Then the pod is not marked ready
    When the readiness and liveness endpoints are called after start-up
    Then both answer healthy without a database write
    Then the smoke step submits agent "INTAKE" for case "RW-2026-000201" with step key "CASEWF:RW-2026-000201:ENTRY:2026-11-30" against the three fakes and answers the outcome within the 60 second policy budget
    Then the run is read through the gateway-bff route within the 2 s budget
    Then the route path is Not specified in the source documents (GAP-0621; ASM-0915)

  Scenario: AC6 The runbook, the rollback and the capacity plan are accepted (new, D-RCV-60)
    Given the runbook, the rollback plan and the capacity plan
    When the on-call rota walks the six entries and the rollback is rehearsed in SIT
    Then the rollback redeploys the previous chart version, re-registers no Schedule, leaves the schema at its forward-only version and leaves the publish right in place
    Then the capacity plan states the step throughput of a peak business date, the worker minimum and maximum, the queue backlog trigger and the database connection cap of the login
    Then the plan records no Quartz job window and no lake window, because both are retired or removed
    Then the deployment topology detail, the host, the SKU and the budget are Not specified in the source documents (GAP-0621; ASM-0912)
```

**Target reading.** The six criteria are new (D-RCV-60) and test only this deliverable: the chart, the migration job, the queue and topic rights, the wiring, the alerts, the probes, the route and the operations artefacts. The legacy values used in the fixtures - agent "INTAKE", the policy with timeout 60 seconds, case "RW-2026-000201", the step key "CASEWF:RW-2026-000201:ENTRY:2026-11-30", the modes OFF, SHADOW and L1, the 10 percent fallback target and the message IDs MSG-P7-003 and MSG-P4-002 - are copied from RWB-TE-013 and from the app story, character for character. No criterion asserts a business outcome, which is RWB-P10-TE013-APP's.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One service, one schema, one login: the release uses the `rwb_agent` login reference and no other service's credential | DP-02; Arch v5 slide 41 |
| BR2 | The decision link arrives as a per-service Flyway sequence in schema `rwb_agent` and runs before the rollout is ready, and it creates no table | DP-15; RWB-PLT-E1044-CON |
| BR3 | The release holds the publish right on `rwb.decision-record.v1` and never creates the topic, the retry topic or the `.dlt` topic, which are the platform's and the record library's | DP-03; DP-09; RWB-PLT-E1027-CON |
| BR4 | Every topic a producer writes has a retry topic and a `.dlt` topic, and the outbox relay publishes within its interval | DP-09; Arch v5 slide 11 |
| BR5 | The worker registers AgentRunWorkflow and the three client activities on queue `rwb-agent` in namespace `rwb-recovery` and holds no Schedule of its own | DP-10; Arch v5 slides 16 and 44 |
| BR6 | No environment value is hard-coded: replica counts, resource sizes, alert thresholds, partitions, concurrency, the modes and the timeout come from values files and contracts | DP-07; Template and Rules §R7.2 s17 |
| BR7 | An alert carries a message ID where one exists, the agreed text, and links one runbook entry | Template and Rules §R7.2 s14 |
| BR8 | The release writes only schema `rwb_agent` and reads other services only through their contracts | DP-01 |
| BR9 | A refused read is counted on the dashboard and never pages the on-call rota | MSG-P4-002 |
| BR10 | The release carries no Quartz job table, no job admin read and no lake artefact; the legacy dependence on RWB-TE-007 is retired and points to the workflow kit | §R6; DP-10; DP-17; ASM-0912 |
| BR11 | The run read is published behind the gateway-bff pass-through route, one hop, and a screen never calls rwb-agent directly | DP-19; ADR-019 |
| BR12 | A record write failure is an alert with MSG-P7-003 and a ticket, so a step that correctly refused to act is never mistaken for a quiet case | R-UNI-39; legacy X4 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the migration job pass the pipeline | Deploying |
| Deploying | Migration job complete and probes healthy | The schema is at the expected version, the worker has polled, the relay runs and both probes answer | Ready |
| Ready | Boundary check passed | The lists and the record read answer, and a synthetic step answers its outcome | Ready with the client live |
| Ready | Release superseded | A new chart version is promoted | Rolling |
| Rolling | All pods on the new version | The old ReplicaSet drains and the worker build ID is on the version set | Ready |
| Ready | Migration job failed, probes failed or a required right missing | The schema is not at the expected version, a probe is unready or the publish right is absent | Failed |
| Failed | Rollback | The previous chart version is redeployed and the forward-only schema stays | Ready |

The states of a step, a run and its record - RUNNING, ANSWERED, TIMED_OUT, GUARDRAIL_FAILED, NO_POLICY and the link - are the app story's and are only watched here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the provisioning and route publication steps, the dashboards, the alerts and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the task queue, the shared topic's rights and the flag registration |
| ACE database administrator | Owns the `rwb_agent` schema, the login, its grants and the migration job approval |
| Release manager | Approves the promotion of one artefact through the environments |
| On-call operator | Runs the six runbook entries and opens an incident when a fallback rate, a record failure, a refused link or a backlog persists |
| RW-PLATADM | Re-presents a step of a business date in the running service, not in the cluster |

The per-service login name used by the chart is Not specified in the source documents (GAP-0621; ASM-0913); the chart references it through a secret reference and never a literal password.

### 11. Data

| Item | Content |
|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, feature switches, environment name |
| Schema | `rwb_agent`, migrated by the per-service Flyway sequence; the decision link and its indexes from this release and the library objects |
| Topic rights | The publish right of rwb-agent on `rwb.decision-record.v1`, with the retry topic and the `.dlt` topic of the platform and the relay interval of the outbox |
| Queue | Temporal task queue `rwb-agent` in namespace `rwb-recovery`; no Schedule |
| Policies | The approved `agent_policy` rows with autonomy_mode OFF, SHADOW and L1, timeout_seconds 60 and the prompt version, read at run time and never held as deployment values |
| Reference data | LOV-AUTONOMY, LOV-AGENT and LOV-PRODUCT through the rwb-case reference-data contract |
| Dashboard series | Step submissions by outcome, fallback rate per agent and policy version, runs by status, record writes and failures, refused links, worker backlog, refused reads |
| Runbook entries | Record write failure, refused link, fallback rate breach, `.dlt` message, worker backlog, migration failure or route unavailable |
| Secrets | The `rwb_agent` login secret, the Kafka client credential and the Temporal mTLS material, all from the platform secret store |

The deployment topology detail (cluster names, node pools, replica counts, resource sizes, zone spread, ingress class, probe timings), the host, the SKU and the budget are Not specified in the source documents (GAP-0621; ASM-0912); the chart exposes them as values and this story fixes only their names and the rule that they are not hard-coded. The alert thresholds and the runbook wording are Not specified in the source documents (GAP-0621; ASM-0914). There is no lake path, no extract and no Quartz job window to document.

### 12. Contract

#### 12.1 REST operations provided

The deployment exposes the two client operations on `/api/recovery/agent/v1`, owner rwb-agent (P10), as fixed by RWB-P10-TE013-CON: `POST /agent-steps` and `PUT /agent-runs/{runId}/decision-record`. The run read `GET /api/recovery/agent/v1/admin/agent-runs` and the other ten platform operations are served by the same release under the baseline of RWB-P10-E1058-CON and are registered on the route with this story's operations. The probes are cluster-internal and not part of the API surface.

#### 12.2 REST operations consumed

| Method | Path | Owner | Deployment need |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-AUTONOMY, LOV-AGENT and LOV-PRODUCT with their version, checked by the readiness probe and the smoke step; 2 s client budget (DP-07, DP-11) |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | P7 rwb-decision | The record read-back before a link is stored, checked by the smoke step |

No operation of rwb-integration is deployed here, and the model endpoint INT-23 is called inside AgentRunWorkflow by the baseline release of RWB-P10-E1058-OPS and is not wired by this story.

#### 12.3 Events published

| Event | Topic | Provisioning |
|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | The release takes or verifies the publish right of rwb-agent and the binding of the retry topic and the `.dlt` topic of the platform; it creates no topic and no consumer group. The record is written by the calling step through the library in its own transaction, so the producer credential this release holds is the one the library uses |

No agent event is provisioned by this story: `rwb.agent.AgentRunCompleted.v1` (EV-28) on `rwb.agent.events.v1` belongs to RWB-P10-E1058-OPS and is unchanged. No lake copy and no extract event exists.

#### 12.4 Events consumed

None by this release. It creates no consumer group: the consumers of EV-08 are rwb-decision and rwb-reporting, and their groups belong to their own releases.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| AgentRunWorkflow | Workflow of the baseline, one execution per step key with the key as workflow ID | `rwb-agent` | Registered by the release worker with the release build ID on the version set |
| ResolveAutonomyMode | Activity | `rwb-agent` | Registered by the same worker; reads `agent_policy` and the P3 lists |
| ApplyAutonomyMode | Activity | `rwb-agent` | Registered by the same worker |
| LinkDecisionRecord | Activity | `rwb-agent` | Registered by the same worker; writes `decision_log_id` |
| KEDA scaling | Worker scaler | `rwb-agent` | Scales on the task-queue backlog with a minimum and a maximum from the values file |

No Schedule is registered, updated or watched by this release: a step is started by its caller.

#### 12.6 Schedules

None. The key starts no Schedule, and the legacy dependence on the Quartz entry of RWB-TE-007 is retired under §R6: the release deploys no job table, no job admin read and no cron entry, and a job step that called the client is a Temporal step of the calling service through the workflow kit of RWB-PLT-E1071-CON (DP-10).

#### 12.7 Tables owned

| Table | Owner | Deployment element |
|---|---|---|
| agent_run | P10 (`rwb_agent`) | The decision link column DF-AGT-058 and its index arrive from `V10_002__agent_run_decision_link.sql`; the table itself is the baseline's |
| agent_policy, agent_prompt | P10 (`rwb_agent`) | Created by the earlier P10 migrations; read by the mode resolution |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_agent` | Created by the same migration job and used by the idempotency of the step key |

No table is created by this story and no grant crosses a schema (DP-01, DP-15). `decision_log_entry` is written by the calling step in its own schema and is never created here.

#### 12.8 Contract fakes

| Fake | Deployment use |
|---|---|
| Decision-record library and record-read fake (RWB-PLT-E1027-CON, RWB-P7-E1027-CON) | Runs in the pipeline and in the SIT smoke profile so the release can start without rwb-decision, with a written record, its reference and a 503 path |
| rwb-case reference-data fake (RWB-P3-E1043-CON) | Same, answering LOV-AUTONOMY, LOV-AGENT and LOV-PRODUCT |
| gateway-bff route stub (RWB-PLT-N001-CON) | Same, a pass-through of one hop in front of the run read |

The fakes are test-only workloads; they are not deployed into UAT or production.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided by this release and 11 by the baseline, 2 consumed | The step and link operations on `/api/recovery/agent/v1`; the lists and the record read consumed, one hop and 2 s each |
| Kafka | 1 published by the calling step through the library, 0 consumed | EV-08 on `rwb.decision-record.v1` with the retry and `.dlt` topics; the release holds the publish right and creates no topic |
| Temporal | 1 workflow of the baseline, 3 activities of this story, 0 Schedules | AgentRunWorkflow with ResolveAutonomyMode, ApplyAutonomyMode and LinkDecisionRecord on queue `rwb-agent`, with KEDA on backlog |
| File | None | The release carries no file, no extract and no lake credential |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON; C RWB-P7-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; the rule result is a request member |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |
| DP-20 | Agent client | rwb-agent contract | C RWB-P10-TE013-CON as the legacy dependency of the pattern |

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-agent/` | Chart with the api deployment, the worker deployment, the service, the migration job, the config map, the secret references and the probes; no Schedule registration hook |
| `helm/rwb-agent/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, feature switches, environment name |
| Pipeline stage | Build, unit and contract tests, image and dependency scan, chart publish, promote the same artefact |
| Provisioning step | Task queue `rwb-agent` in namespace `rwb-recovery`; the publish right on `rwb.decision-record.v1` and its retry and `.dlt` bindings; no topic and no consumer group created |
| Route publication | The two client operations and the run read registered behind the gateway-bff pass-through route, one hop |
| KEDA scaling | Worker scaled on the task-queue backlog with a minimum and a maximum from the values file |
| Dashboards | Six panels: step submissions by outcome, fallback rate per agent and version, runs by status, record writes and failures, refused links, worker backlog and refused reads |
| Alerts | Five rules: MSG-P7-003 on a record failure, a fallback-rate breach, a refused link, a `.dlt` record, a failed migration or an unhealthy route |
| Runbook | Six entries: record write failure, refused link, fallback rate breach, `.dlt` message, worker backlog, migration failure or route unavailable |

**Probes.** Readiness answers healthy only when the migration is at the expected schema version, the worker has polled, the relay is running and the last read of the reference lists and of the record read answered; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database.

**Migration job.** Runs the per-service Flyway sequence for schema `rwb_agent` with the service login as a pre-deploy job with a backoff limit; `V10_002__agent_run_decision_link.sql` applies after `V10_001__agent_runtime.sql`, a failed job blocks the rollout and the release, and the sequence is forward only (DP-15).

**Alert mapping carried over from the legacy story.**

| Message ID or check | Condition | Alert | Route |
|---|---|---|---|
| MSG-P7-003 | A record write fails and a step does not act | Record-failure alert with the step key, the agent and the business date | Platform on-call and RW-PLATADM, ticket |
| None (fallback rate) | The fallback rate of an agent and policy version is above the 10 percent target | Fallback-rate alert with the agent, the version and the rate | RW-RISK and RW-COE, no page |
| None (refused link) | A link is refused because the run holds another record | Refused-link alert with the run ID and both references | Data steward, ticket |
| None (record) | A record lands in `.dlt` | `.dlt` alert with the record reference and its registry subject | Platform on-call, page |
| None (backlog) | The worker backlog passes its threshold | Backlog alert on queue `rwb-agent` | Platform on-call, page |
| MSG-P4-002 | A read without the Platform administration right | Refused-read count on the dashboard | No page |

**Capacity.** The plan states, per environment, the step submissions of a peak business date, the share that falls back, the queue backlog trigger, the worker minimum and maximum, the connection cap of the login and the relay interval. The target is the legacy measure: an answer inside the 60 second policy budget with the rule result used on expiry, and a fallback rate below 10 percent per month (FSD P10 Agent runtime v3 A2.11.1). No Quartz job window and no lake window appear in the plan.

**Rollback.** The previous chart version is redeployed; the Flyway sequence is forward only, so the link column and its index stay and no down-migration is run; the publish right on `rwb.decision-record.v1` is left in place, because removing it would stop the record of every step of a calling service; the route is republished from the previous release; and no Schedule has to be re-registered, because this release holds none. A rollback is rehearsed in SIT before UAT.

**Done when.** The chart renders in all three environments, the pipeline promotes one artefact, the probes answer, the queue, the topic right and the bindings are verified by a test, KEDA scales on backlog, the four workflows and activities are registered, the five alerts fire on synthetic conditions including the record failure with MSG-P7-003, the route answers within 2 s, the capacity plan is reviewed, the rollback is rehearsed and the six runbook entries are accepted by the on-call rota.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | A record write fails and the step does not act | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A read without the Platform administration right | You cannot {action} here. Your role does not include it. |

The two texts are copied unchanged from RWB-TE-013; the deployment adds the alert routing and the runbook link, never a new wording. The fallback-rate, refused-link, `.dlt` and backlog conditions have no message ID in the legacy story and keep none.

### 15. Screens and states

The deployment serves the run read and the two client operations of RWB-P10-TE013-APP through the gateway-bff pass-through route (DP-19). The operator-facing surfaces of this story are the pipeline run view, the release view, the dashboards and the runbook. The agent monitor screen SCR-46 belongs to RWB-E2-031 and the autonomy-level screen to Epic 3, and neither is changed here. The exact path of the route is Not specified in the source documents (GAP-0621; ASM-0915).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P10-TE013-OPS-01 | AC1, BR2 | NFR | Chart renders for DEV, SIT and UAT with a pinned digest, the login reference and the migration job of `V10_002__agent_run_decision_link.sql` after `V10_001__agent_runtime.sql`, creating no table |
| TC-P10-TE013-OPS-02 | AC2, BR3, BR4, BR5 | NFR | Backlog scales the worker, the build ID is on the version set, the four workflows and activities are registered, the publish right and the retry and `.dlt` bindings exist, and no topic or consumer group is created |
| TC-P10-TE013-OPS-03 | AC3, BR6 | NFR | The three lists and the record read come from the contracts, the policies carry OFF, SHADOW, L1 and timeout 60, the switch off starts no run, and every secret is a reference |
| TC-P10-TE013-OPS-04 | AC4, BR7, BR12 | NFR | Five synthetic conditions raise the mapped alerts, MSG-P7-003 on the record failure, the refused link with both references, the `.dlt` record, and one runbook entry each |
| TC-P10-TE013-OPS-05 | AC5, BR11 | End to end | Probes false before the migration, true after; the smoke step for case "RW-2026-000201" answers its outcome against the three fakes and the run is read through the route within 2 s |
| TC-P10-TE013-OPS-06 | AC6, BR1, BR10 | NFR | The six runbook entries walked, the rollback rehearsed with the schema forward only and the publish right kept, and the capacity plan figures stated |

The six test cases are this story's own (D-RCV-60) and test the deployment artefacts of the legacy criteria rather than the business outcomes, which are the app story's: the legacy ids TC-TE-013-01 to TC-TE-013-10 stay with RWB-P10-TE013-APP and are not copied here. The legacy Level "System" maps to NFR for a deployment check and to End to end where the smoke step and the route answer are proved.

### 17. Guardrails

- No business value in a values file: the modes, the timeout, the agent codes, the check codes and the lists are contract and policy values, never deployment values (DP-07).
- No personal data in logs, dashboard series, alert payloads or the runbook: run counts, IDs, dates, codes and durations only.
- No other service's table is read and no grant crosses a schema: the login holds rights on `rwb_agent` only (DP-01, DP-02).
- The release takes the publish right on the shared decision-record topic and never creates a topic, a retry topic, a `.dlt` topic or a consumer group (DP-03, DP-09).
- The release pins the image digest and the chart version; a rebuild between environments is not allowed.
- No secret is written into a values file, a chart template, a dashboard or the runbook; all secrets come from the platform secret store.
- The release deploys no Quartz job table, no job admin read and no lake artefact, and the legacy dependence on RWB-TE-007 points to the workflow kit (§R6; DP-10).
- The run read is published only through the gateway-bff route, one hop, and a screen never reaches the service (DP-19).
- A record write failure is alerted with MSG-P7-003 and never repaired by writing a record from an agent run, because the record belongs to the step (DP-03).

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-DRI-001 | Every decision records rule, model, agent and prompt versions | The record write and its publish right, and the record-failure alert | TC-P10-TE013-OPS-02, TC-P10-TE013-OPS-04 |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | The MSG-P7-003 alert, its runbook entry and the ticket | TC-P10-TE013-OPS-04 |
| REQ-ACA-010 | Agents run under service identities with the same role checks | The `rwb_agent` login reference and the refused-read count | TC-P10-TE013-OPS-03, TC-P10-TE013-OPS-04 |
| D-RCV-60 DP-03 | Local decision record plus central ledger | The publish right on `rwb.decision-record.v1` and the boundary wiring of the record read | TC-P10-TE013-OPS-02, TC-P10-TE013-OPS-03 |
| D-RCV-60 DP-09 | Kafka with outbox, inbox and CloudEvents | The retry and `.dlt` bindings, the relay interval and the `.dlt` alert | TC-P10-TE013-OPS-02, TC-P10-TE013-OPS-04 |
| D-RCV-60 DP-10 | Temporal replaces Quartz | The worker registration on queue `rwb-agent`, KEDA and the absent Schedule and job table | TC-P10-TE013-OPS-02, TC-P10-TE013-OPS-06 |
| D-RCV-60 DP-15 | Per-service Flyway and migration ownership | The migration job and the forward-only rollback | TC-P10-TE013-OPS-01, TC-P10-TE013-OPS-06 |
| D-RCV-60 DP-19 | gateway-bff composite route | The route publication and the one-hop smoke read | TC-P10-TE013-OPS-05 |
| D-RCV-60 DP-20 | Agent client through the rwb-agent contract | The two client operations and the workflow the worker registers | TC-P10-TE013-OPS-02, TC-P10-TE013-OPS-05 |
| ADR-021 | Per-service Flyway and migration ownership | The migration job and the forward-only rollback | TC-P10-TE013-OPS-01, TC-P10-TE013-OPS-06 |
| ADR-023 | Observability per service | Six dashboard panels, five alerts and six runbook entries | TC-P10-TE013-OPS-04 |
| NFR-010 | An agent returns an answer inside its target, after which the rule result is used | The 60 second policy budget of the smoke step and the fallback-rate panel | TC-P10-TE013-OPS-05 |

The gap GAP-0621 records what the sources leave open for this release - the topology and sizing, the login and secret name, the alert thresholds and runbook wording, and the route path - and each default it raises is settled by ASM-0912 to ASM-0915.

### 19. Out of scope

- The application code of the mode resolution, the timed run, the fallback, the record write and the link (RWB-P10-TE013-APP).
- The contract documents and the fakes as published artefacts (RWB-P10-TE013-CON); this story deploys the test copies only.
- The agent platform release, its schema baseline, its topic, its model gateway wiring and its own worker activities (RWB-P10-E1058-OPS and RWB-P10-E1058-APP).
- The platform topic provisioning, the Temporal cluster, the KEDA operator and the gateway-bff implementation (RWB-PLT-EVT, RWB-PLT-WF, RWB-PLT-EDGE and RWB-PLT-OBS).
- The record library, the record type, the central ledger and the record read (RWB-PLT-E1027-CON, RWB-P7-E1027-CON).
- The reference lists of rwb-case (RWB-P3-E1043-CON) and the embedded Drools kit (RWB-PLT-E1072-CON).
- The case steps that call the client, the screen field list of the agent monitor and the autonomy-level screen (RWB-E2-028, RWB-E2-029, RWB-E2-031, Epic 3).
- The exact deployment topology, the host, the SKU, the budget, the replica counts, the resource sizes, the topic partitions, the worker concurrency, the alert thresholds and the probe timings (GAP-0621).
- Any lake artefact, extract or Quartz job table, which DP-17 and §R6 remove (GAP-0621).
- The end-to-end run of the legacy criteria AC1 to AC8 across services (RWB-ITG-TE013-ITG).
