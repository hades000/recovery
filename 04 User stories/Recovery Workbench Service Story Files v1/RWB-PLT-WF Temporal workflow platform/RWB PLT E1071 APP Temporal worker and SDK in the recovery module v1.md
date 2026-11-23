# RWB-PLT-E1071-APP Temporal worker and SDK in the recovery module

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-E1071-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-WF |
| Wave | 0 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-071 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-PLT-WF-E |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1071-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-PLT-E1070-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | RWB-PLT-TE001-APP |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-009, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-014, FR-PLT-015, FR-PLT-016, FR-PLT-017, FR-PLT-018, FR-PLT-021, FR-PLT-022, FR-PLT-023, FR-PLT-024, FR-PLT-025, FR-PLT-026, FR-PLT-028, FR-PLT-029) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-071 for the workflow platform epic; the smoke job is now the JOB-22 Temporal Schedule on `rwb-platform` and the smoke operation is the PLT-owned `POST /admin/workflows/smoke`, while the worker, the codec, the gateway and every value are kept. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform administrator**, I want **the recovery module to run one Temporal worker through the Spring Boot starter with fixed task-queue and workflow-ID conventions, the payload codec, the published WorkflowGateway and a smoke workflow on a Temporal Schedule**, so that **Epic 3 workflows plug into a worker that is already secure and observable**.

This is the app story of legacy key RWB-E1-071, split from the monolith Epic 1 story of the same name for epic RWB-PLT-WF. The platform is shared platform and not one of the 19 services: it has no `rwb_*` schema, no `rwb.<short>.events.v1` topic and no `/api/recovery/<short>/v1` REST base of its own, and its namespace is the specified `rwb-recovery`. The story delivers one worker pattern, one codec, one published gateway and one smoke workflow, and it proves the whole path before the first case workflow exists.

### 2. Business rationale

The cluster of RWB-PLT-E1070-APP is only useful when a worker connects to it from the recovery module. Without one worker pattern, each Epic 3 squad would choose its own task queue, workflow ID, payload handling and start-up checks, and the first clear personal data in a workflow history would be found in production. This story gives the module one worker, one codec, one gateway and one smoke workflow, and it proves the path end to end before the first case workflow exists.

It meets REQ-DRI-005 (an action does not proceed when its decision record cannot be written), REQ-DRI-007 (a failed start reaches a named owner) and REQ-DRI-010 (the target, namespace and task queue are parameters, not code). It keeps the codec rule of NFR-045: every payload is a ciphertext with codec metadata, and the history, the worker log and the test data hold no clear personal data. The measure is a daily smoke workflow that completes with one decision-record entry and a history that holds no clear personal data.

**Two realignment deltas.** First, the smoke job is **JOB-22**: a Temporal Schedule at 06:00 on the platform task queue (Architecture v5 slide 44; Temporal and Drools design slide 32 item 6; ADR-016, DP-10). The legacy story relied on the clustered ACE Quartz scheduler under exception T2 and on the retired RWB-TE-007 Quartz scheduler; both no longer apply, this story creates no Quartz job and no job-catalog row, and the Schedule is owned by the platform. Second, the monolith API base is retired (DP-13): the smoke operation is published as `POST /admin/workflows/smoke`, whose owner is PLT in the Ownership Map, so it no longer sits in a service base and does not repeat the monolith path.

### 3. Preconditions

- RWB-PLT-E1071-CON is published: the WorkflowGateway interface, the workflow-ID and task-queue conventions, the payload-codec metadata contract, the smoke workflow contract and the admin operation, with its fake.
- RWB-PLT-E1070-CON is published: the cluster contract of namespace `rwb-recovery` with the frontend endpoint, the mTLS certificates, the Web UI and the codec server, at server version 1.30 or later.
- RWB-PLT-E1027-CON is published: the DecisionLogApi of the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03). RWB-P7-E1027-CON publishes the central ledger contract behind it.
- RWB-PLT-E1072-CON is published: the embedded Drools kit (DP-04). The worker registers the kit activity classes so that Epic 3 workflows find them; the smoke workflow evaluates no rule package.
- RWB-PLT-E1042-CON and RWB-PLT-E1043-CON are published: the parameters contract and the reference-data contract with the client library (DP-06, DP-07), with RWB-P3-E1042-CON and RWB-P3-E1043-CON behind them as the C dependencies that never block this build.
- RWB-PLT-E1047-CON is published: the topic and event naming library (DP-14). RWB-PLT-E1044-CON is published: the per-service Flyway conventions (DP-15); this story adds no migration.
- RWB-PLT-N001-CON is published: the gateway-bff route contract (DP-19). This story exposes no screen, and the contract is cited because the platform administration surface reaches its operations through the edge.
- The Temporal Java SDK version is pinned with the server version approved for RWB-PLT-E1070-APP, and the build reads the version from the dependency lock and not from a property. The release is the SCB IT approved release recorded in Environment and Deployment Design v4, Temporal 1.30 or later (ASM-2537).
- A Key Vault key for the payload codec exists, and the SY-CASEWF managed identity has wrap and unwrap rights on that key only. The key is one AES-GCM key per environment and is never in a values file or a test (ASM-2537); the key name is Not specified in the source documents (GAP-1442; ASM-2537).
- LOV-DECISION carries PLATFORM_SMOKE as a system event code with no case, loaded by the data steward through the versioned reference load of the rwb-case reference-data contract. The decision-record library accepts it under the system event exception, as it accepts the access event codes.
- No Quartz scheduler is needed and none is a dependency: the smoke job is the JOB-22 Temporal Schedule with overlap policy SKIP and a catch-up window, and the retired RWB-TE-007 Quartz scheduler is not referenced.
- The platform login, the queue row in the Ownership Map and the admin base of the platform are Not specified in the source documents (GAP-1442; ASM-2537). The story uses the working read of ASM-2537 until the Wave 0 Service Catalog fixes them.

### 4. Flow

1. Application start: TemporalConfig reads temporal.target, temporal.namespace and temporal.taskqueue.platform through the parameters contract; a missing value stops start-up with MSG-P3-032.
2. Application start: TemporalWorkerLifecycle reads the flag `rwb.p3.temporal`; when it is on, it creates one worker on `rwb-platform` with the workflow and activity classes and the build ID from the pipeline.
3. Worker: connects to the frontend with its mTLS certificate and polls `rwb-platform`; when the flag is off, no worker and no poller are created.
4. PdpaPayloadCodec: registers as the data converter on the client and the worker; it encrypts every payload with AES-GCM and the Key Vault key, and it decrypts only inside the worker.
5. WorkflowGateway: starts and signals workflows by workflow ID; a start with an existing workflow ID returns the running execution and does not start a second run.
6. The platform smoke Schedule (JOB-22) fires daily at 06:00, with overlap policy SKIP and a catch-up window, and calls WorkflowGateway.start("PlatformSmokeWorkflow", "platform-smoke-{yyyymmdd}", input) through the worker.
7. PlatformSmokeWorkflow: runs one activity; PlatformSmokeActivity writes the decision record with decision code PLATFORM_SMOKE through the DecisionLogApi, then returns the worker build ID.
8. Workflow: completes when the activity commits; a failed decision-record write fails the activity and the workflow, and the incident reaches RW-PLATADM.
9. Platform administrator: may call `POST /admin/workflows/smoke` to run the same workflow on demand; the response gives the workflow ID, run ID and status.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The Temporal frontend is unreachable or refuses the connection | WorkflowGateway.start fails; `POST /admin/workflows/smoke` returns 503; no workflow, no history and no decision record are written | MSG-P3-036 | AC3 |
| X2 | A start uses a workflow ID that is already RUNNING | The running execution is returned; no second run and no second activity | None | AC4 |
| X3 | The flag `rwb.p3.temporal` is off | No worker is registered and the admin smoke operation is not registered; the call returns 404 | None | AC5 |
| X4 | A required parameter has no value for the environment at start-up (temporal.target, temporal.namespace or temporal.taskqueue.platform) | The service does not start; the missing parameter and environment are named | MSG-P3-032 | AC6 |
| X5 | A workflow class is placed outside recovery.casewf.workflow | The build fails naming the class and the package rule; the merge is blocked | Build log | AC7 |
| X6 | A role without Platform administration U calls `POST /admin/workflows/smoke` | The call is refused with 403; nothing starts | MSG-P4-002 | TC-E1-071-08 |

The missing-parameter row is X4: the legacy exception covered temporal.target only, and the platform binds the namespace and the task queue under the same start-up rule because all three are parameters and none may take a default (REQ-DRI-010).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the cluster contract, the parameters, the reference data, the decision-record library, the Drools kit, the naming library, the Flyway conventions, the edge contract and the module rules; the smoke workflow is self-contained |
| Negotiable | The Schedule cadence, the build-ID format, the retry policy and the actor identity are configuration or platform values; the codec, the package boundary, the queue and the ID conventions are fixed by the contract |
| Valuable | Epic 3 starts from a worker that already encrypts payloads, records a decision and survives a restart |
| Estimable | One worker, one codec, one gateway, one smoke workflow, one Schedule and one admin operation |
| Small | Fits two weeks with its tests |
| Testable | Each criterion in section 7 is one test in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Temporal worker and SDK in the recovery module

  Background:
    Given the worker is built with the Temporal Java SDK version pinned for RWB-PLT-E1070-APP
    Given rwb.p3.temporal is on and the parameters temporal.target, temporal.namespace and temporal.taskqueue.platform have values for SIT

  Scenario: AC1 Smoke workflow completes (legacy RWB-E1-071 AC1)
    Given the platform smoke Schedule (JOB-22) runs at 06:00 on 16 November 2026
    When PlatformSmokeWorkflow "platform-smoke-20261116" starts on task queue `rwb-platform`
    Then the workflow runs one activity and ends COMPLETED within 60 seconds
    Then one decision_log_entry exists with decision code PLATFORM_SMOKE, actor SY-CASEWF and inputsRef "platform-smoke-20261116"
    Then no recovery_case row is created or changed

  Scenario: AC2 History holds encrypted payloads only (legacy RWB-E1-071 AC2)
    Given the smoke activity input carries the synthetic national ID "1101700203456"
    When the workflow completes
    Then the raw history from the Temporal CLI shows the payload as binary ciphertext with codec metadata
    Then the string "1101700203456" appears nowhere in the history or the worker log
    Then decoding through PdpaPayloadCodec with the Key Vault key returns the input
    Then the worker log holds the workflow ID and no payload

  Scenario: AC3 Temporal unreachable (legacy RWB-E1-071 AC3)
    Given the Temporal frontend is unreachable on port 7233
    When U-70 calls POST /admin/workflows/smoke
    Then the response is 503 with MSG-P3-036
    Then no workflow execution exists and no decision_log_entry is written
    Then the metric workflow_start_failures_total increases by one

  Scenario: AC4 Duplicate workflow ID (legacy RWB-E1-071 AC4)
    Given platform-smoke-20261116 is RUNNING
    When U-70 calls the smoke endpoint again with workflow ID platform-smoke-20261116
    Then the response is 200 with the same run ID and status RUNNING
    Then the history holds one WorkflowExecutionStarted event
    Then the activity runs once

  Scenario: AC5 Flag off (legacy RWB-E1-071 AC5)
    Given rwb.p3.temporal is off in DEV
    When the application starts
    Then no worker is registered on `rwb-platform` and no poller connection is opened
    When U-70 calls POST /admin/workflows/smoke
    Then the response is 404 and no workflow starts

  Scenario: AC6 Missing parameter at start-up (legacy RWB-E1-071 AC6)
    Given temporal.target has no value for SIT
    When the application starts in SIT
    Then start-up fails with MSG-P3-032 naming temporal.target and SIT
    Then no worker polls and the health endpoint stays 503

  Scenario: AC7 Workflow class outside the package (legacy RWB-E1-071 AC7)
    Given a branch adds the class recovery.casewf.smoke.SmokeWorkflowImpl outside recovery.casewf.workflow
    When the build runs WorkflowBoundaryTest
    Then the build fails naming the class and the package rule
    Then the merge is blocked
```

Two substitutions are made and no other change: the Quartz smoke job becomes the platform smoke Schedule (JOB-22), which is DP-10 and ADR-016, and the monolith admin path becomes the PLT-owned `POST /admin/workflows/smoke`, which is DP-13. Every value of the seven legacy criteria is kept character for character — the workflow ID "platform-smoke-20261116", the namespace `rwb-recovery`, the 60-second completion, the decision code PLATFORM_SMOKE, the actor SY-CASEWF, the synthetic national ID "1101700203456", the message identifiers MSG-P3-036, MSG-P3-032 and MSG-P4-002, the metric workflow_start_failures_total, the flag `rwb.p3.temporal`, the package `recovery.casewf.workflow` and the port 7233 — and the scenario titles stay as the legacy titles with their origin tag.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Workflow code lives only in recovery.casewf.workflow; activities, gateways and I/O live in recovery.casewf.activities or the owning module, and WorkflowBoundaryTest enforces the boundary in every build | D-RCV-36 T7; ADR-011; DP-01 |
| BR2 | Workflow code is deterministic: no clock, random, I/O, parameter read or direct Drools call; time comes from Workflow.currentTimeMillis or a timer, and all I/O is an activity | D-RCV-36 T7; DP-10 |
| BR3 | Every payload passes through PdpaPayloadCodec (AES-GCM, one key per environment in Key Vault); no clear personal data in history, logs, tests or prompts | D-RCV-36 T1; NFR-045 |
| BR4 | Task queues are `rwb-platform` for the platform smoke and health, and `rwb-<short>` per service from Epic 3; no Epic 1 workflow uses a service queue | D-RCV-36 T1; Architecture v5 slide 24; JOB-22 |
| BR5 | Workflow IDs are platform-smoke-{yyyymmdd} and, from Epic 3, case-{caseId}; a repeated start with the same ID returns the running execution and never starts a second run | D-RCV-36 T1; R-UNI-40 |
| BR6 | Every worker carries the build ID from the pipeline manifest; a worker with no build ID or an unknown build ID starts no new workflow | D-RCV-36 T1; Architecture v5 slide 23 (Worker Versioning) |
| BR7 | With `rwb.p3.temporal` off, no worker is registered, no poller is opened and `POST /admin/workflows/smoke` returns 404; nothing else changes | D-RCV-36 T1; RWB-E1-047 |
| BR8 | A required parameter with no value stops start-up with MSG-P3-032; the service never substitutes a default for temporal.target, temporal.namespace or temporal.taskqueue.platform | REQ-DRI-010; MSG-P3-032; DP-06 |
| BR9 | The smoke activity writes its decision record through the DecisionLogApi before the workflow completes; a failed write fails the workflow | REQ-DRI-005; DP-03 |
| BR10 | The smoke workflow reads no case row, no ACE view and no business table | D-RCV-35 U1; Architecture v5 slide 20; DP-01, DP-05 |
| BR11 | A start that cannot reach the frontend fails with MSG-P3-036 and writes no workflow, no history and no decision record | D-RCV-36 T1; REQ-DRI-007; DP-11 |

The task queue name is the working read of ASM-2537: Template and Rules §R4 has no platform row, and JOB-22 on Architecture v5 slide 44 puts PlatformSmokeWorkflow on the platform queue, so `rwb-platform` is published as the platform queue until the Wave 0 Service Catalog and the Ownership Map name it (GAP-1442).

### 9. State transitions

None for a case. This story changes the status of the platform smoke workflow only.

| From | Event | Condition | To |
|---|---|---|---|
| None | Start (Schedule or admin operation) | Workflow ID not known | RUNNING |
| RUNNING | Activity completes | The decision record is committed | COMPLETED |
| RUNNING | Activity fails after its retry policy | No decision record is written | FAILED |
| COMPLETED or FAILED | Retention 30 days (parameter temporal.retention.days) | The workflow is closed | Removed from visibility; archive is RWB-PLT-E2039-APP |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM | Runs the smoke workflow on demand, reads the worker health and the history (Platform administration, U) |
| RW-AUDIT | Reads the history and the decision record (Platform administration and Decision log, R) |
| RW-SECADM | Reads the codec configuration; decode through the codec server is RWB-PLT-E2038-APP, not this story |
| SY-CASEWF | The worker identity; connects with mTLS, polls `rwb-platform` and writes the PLATFORM_SMOKE entry (Decision log C) |
| RW-COE | Reads the smoke result as a platform check (Platform administration, R) |
| RW-TRIBE | Builds and deploys the worker through the pipeline; has no PROD endpoint right |
| No delegation of authority level applies | A smoke run is not a credit decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write | Owner |
|---|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write | P7 (rwb_decision) |
| DF-DEC-030 | decision_log_entry | actor_user_id | Write | P7 (rwb_decision) |
| DF-DEC-031 | decision_log_entry | idempotency_key | Write, read | P7 (rwb_decision) |
| DF-REF-028 | lov_value | lov_code | Read | P3 (rwb_case) |
| DF-REF-029 | lov_value | value_code | Read | P3 (rwb_case) |

The PLATFORM_SMOKE entry has no case, no rule ID and no version group; it is a system event under the same exception that the access event codes use. Its idempotency key is the workflow ID, so a repeated run of the same day cannot write a second entry. The decision record is written through the DecisionLogApi into the rwb-decision schema and this story writes no table of its own; the level of detail (lov_code, value_code) is read through the reference-data contract of rwb-case. The parameters temporal.target, temporal.namespace, temporal.taskqueue.platform and temporal.retention.days are read through the parameters contract and add no field. No field is added by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner PLT. The operation is published on the platform, not inside a service base.

| Method | Path | Purpose | Access | Errors | Idempotency |
|---|---|---|---|---|---|
| POST | `/admin/workflows/smoke` | Run PlatformSmokeWorkflow on demand and return its run | Platform administration, right U | 401 (MSG-P4-001); 403 no Platform administration U (MSG-P4-002); 404 flag off; 409 the workflow ID already completed (MSG-GEN-004); 503 Temporal unreachable (MSG-P3-036) | Workflow ID: a repeat while RUNNING returns the running execution; a repeat after COMPLETED returns 409 with no second run |

Request body optional: { workflowId: string }, default platform-smoke-{yyyymmdd} in the server time zone. Response 200 WorkflowRun: workflowId, runId, workflowType, status, taskQueue, startedAt. The host, the admin base and the platform login of the operation are Not specified in the source documents (GAP-1442; ASM-2537); the path is taken from the Ownership Map row, whose owner is PLT, and is kept character for character.

#### 12.2 REST operations consumed

| Method | Path | Provider | Used for | Transport |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/parameters` | rwb-case (P3) | temporal.target, temporal.namespace, temporal.taskqueue.platform and temporal.retention.days, with the flags | One hop, 2 s, GET retried once with jitter (DP-06, DP-11) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | rwb-case (P3) | LOV-DECISION, to confirm PLATFORM_SMOKE is a loaded system event code | One hop, 2 s, GET retried once with jitter (DP-07, DP-11) |
| POST (library call, not REST) | DecisionLogApi.record | RWB-PLT-E1027-CON library | The PLATFORM_SMOKE decision record in the activity's transaction | In-process library call; the library writes the row and the outbox row |

Both REST reads are built against the RWB-P3-E1042-CON and RWB-P3-E1043-CON contracts and their fakes, so the C dependencies never block this build. The decision record does not travel over REST: the DecisionLogApi of the platform library is the only path, and it is not a second writer of the schema.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 | workflow ID | decision code PLATFORM_SMOKE, actor SY-CASEWF, workflow ID, build ID, recorded at |

The event is written to the outbox by the library in the same transaction as the decision record, and relayed with the CloudEvents envelope (DP-03). The platform publishes no topic of its own and no platform event name.

#### 12.4 Events consumed

None. The smoke workflow waits on its activity and on no event, and the worker consumes no topic of its own.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| PlatformSmokeWorkflow | Workflow | `rwb-platform` | Runs one activity and completes; deterministic and free of I/O (JOB-22) |
| PlatformSmokeActivity | Activity | `rwb-platform` | Writes the PLATFORM_SMOKE decision record through the DecisionLogApi and returns the build ID |
| WorkflowGateway | Published interface | `rwb-platform` | start(workflowType, workflowId, input) and signal(workflowId, signal, payload), implemented by WorkflowGatewayImpl; the only way a module starts or signals a workflow |

#### 12.6 Schedules

| Schedule | Cadence | Task queue | Overlap | Legacy reference |
|---|---|---|---|---|
| Platform smoke (JOB-22) | Daily at 06:00 | `rwb-platform` | SKIP, with a catch-up window | JOB-22 Smoke workflow; Architecture v5 slide 44; Temporal and Drools design slide 32 item 6; ADR-016; DP-10 |

#### 12.7 Tables owned

None. The platform owns no `rwb_*` schema of its own: the decision record is written through the library into the rwb-decision schema (P7), the reference data is read through the rwb-case contract (P3), and the smoke writes no table of its own and no migration.

#### 12.8 Contract fakes

| Fake | Serves | Used by this story |
|---|---|---|
| WorkflowGateway fake and platform worker fake (RWB-PLT-E1071-CON) | The gateway interface, the ID and queue conventions, the codec metadata and the smoke workflow contract | The unit and component tests of the gateway, the worker lifecycle and the boundary test |
| Decision-log fake (RWB-PLT-E1027-CON) | DecisionLogApi.record | AC1 and the failed-write path of BR9 |
| rwb-case parameter fake (RWB-P3-E1042-CON) | `GET /api/recovery/case/v1/admin/parameters` | AC6, and the temporal.retention.days read |
| rwb-case reference-data fake (RWB-P3-E1043-CON) | `GET /api/recovery/case/v1/admin/lists/{listCode}` | The LOV-DECISION check that PLATFORM_SMOKE is loaded |
| Temporal frontend fake (RWB-PLT-E1070-CON) | The frontend endpoint, the namespace and the mTLS identity | AC3, AC4 and AC5 without a cluster |

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 1 operation (`POST /admin/workflows/smoke`, owner PLT) | 3 consumption rows: 2 REST reads on rwb-case and 1 library call (DecisionLogApi) | OpenAPI 3.1, one hop, 2 s timeout, GET retried once with jitter, `Idempotency-Key` carried as the workflow ID |
| Kafka | 1 published (`rwb.decision-record.DecisionRecorded.v1`) | 0 | CloudEvents 1.0 through the outbox of the decision-record library; the platform publishes no topic of its own |
| Temporal | 1 workflow and 1 activity, on `rwb-platform`, plus 1 Schedule (JOB-22) | 0 | Namespace `rwb-recovery`; overlap SKIP with a catch-up window |
| File | 0 | 0 | No file is read or written |

### 13. Solution plan

**Package.** Worker, codec and gateway in `recovery/casewf/workflow` and `recovery/casewf/activities` (Java packages `recovery.casewf.workflow` and `recovery.casewf.activities`); the admin operation in `recovery/casewf/admin`. The platform is shared platform and owns no service schema, no service topic and no service base.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TemporalConfig | Configuration | Reads temporal.target, temporal.namespace, temporal.taskqueue.platform and temporal.retention.days through the parameters contract; fails start-up with MSG-P3-032 on a missing value |
| TemporalWorkerLifecycle | Service | Starts and stops the worker with `rwb.p3.temporal`; registers the workflow and activity classes, the Drools kit activities and the build ID |
| PdpaPayloadCodec | Service | AES-GCM payload encryption with the Key Vault key and the key version in the metadata; the only data converter on the client and the worker |
| WorkflowGatewayImpl | Service | Implements the published gateway: start and signal by workflow ID, applies the codec and the ID convention, maps an unreachable frontend to MSG-P3-036 |
| PlatformSmokeWorkflow | Workflow | One activity, then complete; deterministic and free of I/O |
| PlatformSmokeActivity | Activity | Writes the PLATFORM_SMOKE decision record through the DecisionLogApi and returns the build ID |
| SmokeSchedule | Schedule definition | Declares JOB-22: daily at 06:00 on `rwb-platform`, overlap SKIP, catch-up window, workflow ID platform-smoke-{yyyymmdd} |
| WorkerBuildIdProvider | Service | Reads the build ID from the pipeline manifest and refuses to start without it |
| WorkflowAdminController | Controller | `POST /admin/workflows/smoke` with the Platform administration U check |
| WorkflowBoundaryTest | Test | Fails the build when a workflow class is outside recovery.casewf.workflow |

**Parameters, flag and configuration**

- Through RWB-PLT-E1042-CON and RWB-P3-E1042-CON: temporal.target (host and port), temporal.namespace = `rwb-recovery`, temporal.taskqueue.platform = `rwb-platform`, temporal.retention.days = 30.
- Flag `rwb.p3.temporal`, read through the parameters contract: off means no worker, no poller, the admin operation returns 404, and no other behaviour changes.
- Build ID format `<git-sha>-<build-number>` from the pipeline manifest (ASM-2537); the format is Not specified in the source documents (GAP-1442; ASM-2537).
- Codec key: one AES-GCM key per environment in Key Vault, referenced by name in the payload metadata and never in a values file or a test (ASM-2537); the key name is Not specified in the source documents (GAP-1442; ASM-2537).
- No Quartz configuration, no job-catalog row and no new table: JOB-22 is a Temporal Schedule and the decision record is written through the library.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; the platform writes no table and reads no other service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views; the smoke reads no ACE row | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` for the services; the platform operation sits on its own path with no service base | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema; the platform adds none | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is applied as the library, not as a second writer: the activity calls the DecisionLogApi, the library writes the decision record and its outbox row in the activity's transaction, and the platform therefore seals nothing locally and owns no decision table. DP-10 is applied as one Schedule declared by the platform worker instead of a Quartz job and a job-catalog row: JOB-22 fires at 06:00 on `rwb-platform` with overlap SKIP and a catch-up window, and the retired RWB-TE-007 Quartz scheduler disappears from the dependency set. DP-11 is applied to the admin operation and to the two parameter reads: one hop each, a 2 s timeout, a breaker per downstream and a GET retried once with jitter, with the published WorkflowGateway as the one interface a module may call and no Temporal type in its signature.

**Build steps**

1. Add the Temporal SDK at the pinned version and the Spring Boot starter; prove the dependency lock holds the version.
2. Build TemporalConfig with the parameter reads and the missing-value failure; test AC6.
3. Build PdpaPayloadCodec with the key reference and the key version in the metadata, and register it on the client and the worker; test AC2 with the synthetic national ID.
4. Build WorkflowGatewayImpl with the ID convention, the codec application and the unreachable mapping; tests AC3 and AC4.
5. Build PlatformSmokeWorkflow, PlatformSmokeActivity and the decision-record write through the DecisionLogApi; test AC1.
6. Declare the JOB-22 Schedule on `rwb-platform` with overlap SKIP and the catch-up window; verify it starts the same workflow the admin operation starts.
7. Build the worker lifecycle and the flag check; test AC5.
8. Build the admin operation with the Platform administration U check; test the 403 of TC-E1-071-08.
9. Build WorkflowBoundaryTest and prove it fails on a class outside recovery.casewf.workflow; test AC7.

**Done when.** The tests in section 16 pass, the smoke workflow completes daily in SIT through JOB-22 with one decision record, the raw history holds no clear personal data, and the WorkflowGateway, the ID and queue conventions and the codec metadata of RWB-PLT-E1071-CON answer every test unchanged.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-036 | The workflow service is unreachable or refuses a start | The workflow service is not available. Try again in a few minutes. |
| MSG-P3-032 | A required parameter has no value at start-up | Parameter {name} has no value for {environment}. The service did not start. |
| MSG-P4-002 | A role without Platform administration U calls the smoke operation | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | No session, or the session has expired | Existing message catalogue entry, cited by the operation; its text is not restated in the source documents |
| MSG-GEN-004 | The same workflow ID has already completed | Existing message catalogue entry, cited by the operation; its text is not restated in the source documents |

MSG-P3-036 and MSG-P3-032 are the legacy identifiers, kept unchanged, and MSG-P4-002 and MSG-P4-001 are reused. No identifier is renumbered by the realignment, and no new message is introduced by the platform move.

### 15. Screens and states

No Workbench screen in this story. The platform administrator calls the admin operation and reads the Temporal Web UI, and the platform job monitor shows the daily smoke run with its last run, status and duration. The smoke run has the states Not run, Running, Completed and Failed, and the run is visible per business date through the workflow ID platform-smoke-{yyyymmdd}. SCR-44 Interface and job monitor shows the same data from Epic 2, and the observability and run books of the platform are RWB-PLT-E2037-APP.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-071-01 | AC1, BR9 | Integration | PlatformSmokeWorkflow platform-smoke-20261116 on `rwb-platform`, started by JOB-22 |
| TC-E1-071-02 | AC2, BR3 | Integration | Synthetic national ID 1101700203456 in the activity input; the raw history of the run |
| TC-E1-071-03 | AC3, BR11 | Integration | Frontend refused by the fake; `POST /admin/workflows/smoke` called; workflow_start_failures_total |
| TC-E1-071-04 | AC4, BR5 | Integration | The same workflow ID started twice while RUNNING |
| TC-E1-071-05 | AC5, BR7 | Component | `rwb.p3.temporal` off in DEV; the admin operation returns 404 |
| TC-E1-071-06 | AC6, BR8 | Component | temporal.target missing for SIT; start-up fails with MSG-P3-032 |
| TC-E1-071-07 | AC7, BR1 | Component | Workflow class in recovery.casewf.smoke; WorkflowBoundaryTest fails the build |
| TC-E1-071-08 | §5 X6, BR7; the 403 answer of §12.1 with MSG-P4-002 (the Access exception of legacy TC-E1-071-08) | Component | RW-CASEOWN calls `POST /admin/workflows/smoke` and is refused with MSG-P4-002 |

Legacy levels map System to Integration and Access to Component, as the level vocabulary of this template requires. The full test, with its Given, When and Then, is in the Recovery Workbench Test Cases master, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the target, the namespace, the task queue, the retention, the workflow-ID patterns and the flag are parameters or convention values.
- No personal data in logs, tests, workflow history or prompts: every payload is a ciphertext with codec metadata, and the test national ID is synthetic.
- No read of another service's tables and no ACE view: the smoke workflow reads no case row and no ACE row, and the reference data is read through the rwb-case contract.
- Workflow code is deterministic: no clock, random, I/O or Drools call in workflow code; all I/O is an activity.
- The codec is the only payload path; no clear personal data is written to history, even in DEV, and the codec key is never in a values file or a test.
- No worker without a build ID and no start with a missing parameter.
- No Quartz job and no job-catalog row: the smoke job is the JOB-22 Temporal Schedule with overlap SKIP, and it has no business wait.
- The platform keeps no schema, no topic and no service base of its own; the decision record is written through the P7 library and the parameters and reference data are read through the P3 contract.
- The admin operation is idempotent by workflow ID: a repeat while RUNNING returns the running execution and a repeat after COMPLETED returns 409 with no second run.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-005 | No action proceeds if its decision entry cannot be written | Epic 1, 3.7 | None (platform enabler) | All recovery processes | R-UNI-39 | TC-E1-071-01, TC-E1-071-02, TC-E1-071-03 |
| REQ-DRI-007 | A failed start reaches a named owner; a retry is safe | Epic 1, 3.2; Program, 5.2 | None (platform enabler) | All recovery processes | R-UNI-40 | TC-E1-071-03, TC-E1-071-04, TC-E1-071-05, TC-E1-071-07 |
| REQ-DRI-010 | Every threshold, limit and name is a versioned parameter | Epic 1, 3.2; Program, 5.1 and 5.7 | None (platform enabler) | All recovery processes | R-UNI-38 | TC-E1-071-06 |

The BRD sections are the legacy sections of RWB-E1-071, kept unchanged; the requirement identifiers and their text do not move with the epic change.

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1071-CON | Contract | H: the gateway interface, the ID and queue conventions, the codec metadata, the smoke workflow contract and the admin operation, with the fake this story builds against |
| RWB-PLT-E1070-CON | Contract | H: the cluster contract of namespace `rwb-recovery`, the frontend endpoint, the mTLS certificate and the codec server |
| RWB-PLT-E1027-CON | Contract | H: the DecisionLogApi and the shared topic `rwb.decision-record.v1` (DP-03) |
| RWB-PLT-E1072-CON | Contract | H: the embedded Drools kit whose activities the worker registers (DP-04) |
| RWB-PLT-E1042-CON, RWB-PLT-E1043-CON | Contract | H: the parameters and reference-data contracts with the client library (DP-06, DP-07) |
| RWB-PLT-E1047-CON, RWB-PLT-E1044-CON | Contract | H: the topic and event naming library and the Flyway conventions (DP-14, DP-15) |
| RWB-PLT-N001-CON | Contract | H: the edge route contract (DP-19) |
| RWB-P3-E1042-CON, RWB-P3-E1043-CON | Contract | C: the rwb-case parameter and reference-data contracts whose fakes this story builds against; they never block |
| RWB-PLT-TE001-APP | App development | X: the module boundary tests and the architecture tests that run in the same pipeline |
| RWB-PLT-E2037-APP | App development | Successor: workflow alerts, the stuck workflow scanner (JOB-21), the dashboard and the run books |
| RWB-PLT-E2038-APP | App development | Successor: the codec server, decode and the Temporal admin audit |
| RWB-PLT-E2039-APP | App development | Successor: backup, failover, upgrade and archive of the workflow histories |
| RWB-PLT-E2040-APP | App development | Successor: the replay test gate, the history export and the build-ID rollout |
| RWB-E2-037, RWB-E2-038, RWB-E2-039, RWB-E2-040 | Legacy Epic 2 keys | Successors of the legacy scope that this story leaves out; each is realigned by its own platform story |

### 19. Out of scope

- Case workflows, case signals and the case task queues of Epic 3, including the workflow ID case-{caseId}.
- The cluster, the namespace, the mTLS certificates and the Web UI (RWB-PLT-E1070-APP).
- The workflow kit templates and the codec server (RWB-PLT-N010-APP), and the codec server and admin audit (RWB-PLT-E2038-APP).
- Workflow alerts, the stuck workflow scanner JOB-21 and the workflow dashboard (RWB-PLT-E2037-APP).
- The replay test gate, history export and build-ID rollout (RWB-PLT-E2040-APP).
- Backup, failover, upgrade and archive (RWB-PLT-E2039-APP).
- The reference case workflow skeleton.
- The Quartz scheduler, its job catalog and the retired RWB-TE-007 scope.
