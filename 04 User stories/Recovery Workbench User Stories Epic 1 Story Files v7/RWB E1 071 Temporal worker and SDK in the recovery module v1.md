# RWB-E1-071 Temporal worker and SDK in the recovery module

SCB Collections and Recovery. Henka Group, 16 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-071 |
| Epic | E1, release 30 November 2026 |
| Module | P3 Case and workflow |
| Feature | None (platform enabler) |
| Requirement IDs | REQ-DRI-005, REQ-DRI-007, REQ-DRI-010 |
| BRD section | Business Requirements Epic 1, section 3.2; Business Requirements Program, sections 5.1 and 5.2 |
| L3 process | All recovery processes |
| Decision | D-RCV-36 (T1, T2, T7); ADR-011 |
| Priority | Must |
| Depends on | RWB-E1-070, RWB-E1-042, RWB-E1-047, RWB-TE-001 |
| Status | Ready for build |

## 1. Story

As a **platform administrator (RW-PLATADM)**, I want **the recovery module to run a Temporal worker through the Spring Boot starter, with fixed task-queue and workflow-ID conventions, a PDPA payload codec and a smoke workflow**, so that **Epic 3 workflows plug into a worker that is already secure and observable**.

## 2. Business rationale

The Temporal cluster of RWB-E1-070 is only useful when a worker connects to it from the recovery module. Without one worker pattern, each Epic 3 squad would choose its own task queue, workflow ID, payload handling and start-up checks, and the first clear personal data in a workflow history would be found in production. This story gives the module one worker, one codec, one gateway and one smoke workflow, and it proves the path end to end before the first case workflow exists.

It meets REQ-DRI-005 (an action does not proceed when its decision record cannot be written), REQ-DRI-007 (a failed start reaches a named owner) and REQ-DRI-010 (the target, namespace and task queue are parameters, not code). It follows D-RCV-36 T1 (hybrid, case data stays in the ACE DB), T2 (Quartz stays for Epic 1 and 2 jobs; the smoke job is Quartz) and T7 (workflow code is deterministic and calls Drools only inside an activity). The measure is a daily smoke workflow that completes with one decision log entry and a history that holds no clear personal data.

## 3. Preconditions

- RWB-E1-070 is done: the Temporal cluster, the rwb-recovery namespace, mTLS and the Web UI exist in DEV and SIT.
- RWB-E1-042 is done: ParameterService serves temporal.target, temporal.namespace, temporal.taskqueue.platform and temporal.retention.days = 30; the values are in the catalog as at 16 November 2026.
- RWB-E1-047 is done: the feature flag service serves rwb.p3.temporal, and a flag change is a logged data change.
- RWB-TE-001 is done: the module boundaries and the architecture tests run in the pipeline.
- The Temporal Java SDK version is pinned with the server version approved for RWB-E1-070; the build reads the version from the dependency lock and not from a property.
- A Key Vault key for the payload codec exists, and the SY-CASEWF managed identity has wrap and unwrap rights on that key only.
- LOV-DECISION carries PLATFORM_SMOKE as a system event code with no case, loaded by RW-DATASTEW through the versioned reference load (RWB-E1-043). The decision log writer accepts it under the system event exception, as it accepts the access event codes.
- The clustered ACE Quartz scheduler is available for the daily smoke job (T2); no Temporal Schedule is created.

## 4. Flow

1. Application start: TemporalConfig reads temporal.target, temporal.namespace and temporal.taskqueue.platform through ParameterService; a missing value stops start-up with MSG-P3-032.
2. Application start: TemporalWorkerLifecycle reads rwb.p3.temporal; when it is on, it creates one worker on rwb-platform with the workflow and activity classes and the build ID from the pipeline.
3. Worker: connects to the frontend with its mTLS certificate and polls rwb-platform; when the flag is off, no worker and no poller are created.
4. PdpaPayloadCodec: registers as the data converter on the client and the worker; it encrypts every payload with AES-GCM and the Key Vault key, and it decrypts only inside the worker.
5. WorkflowGateway: starts and signals workflows by workflow ID; a start with an existing workflow ID returns the running execution and does not start a second run.
6. SmokeScheduleJob: Quartz runs daily at 06:00 and calls WorkflowGateway.start("PlatformSmokeWorkflow", "platform-smoke-{yyyymmdd}", input).
7. PlatformSmokeWorkflow: runs one activity; PlatformSmokeActivity writes a decision log entry with decision code PLATFORM_SMOKE through DecisionLogWriter, then returns the worker build ID.
8. Workflow: completes when the activity commits; a failed decision log write fails the activity and the workflow, and the incident reaches RW-PLATADM.
9. Platform administrator: may call POST /admin/workflows/smoke to run the same workflow on demand; the response gives the workflow ID, run ID and status.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The Temporal frontend is unreachable or refuses the connection | WorkflowGateway.start fails; the endpoint returns 503; no workflow, no history and no decision log entry are written | MSG-P3-036 | AC3 |
| X2 | A start uses a workflow ID that is already RUNNING | The running execution is returned; no second run and no second activity | None | AC4 |
| X3 | rwb.p3.temporal is off | No worker is registered and the admin smoke endpoint is not registered; the call returns 404 | None | AC5 |
| X4 | temporal.target has no value for the environment at start-up | The service does not start; the missing parameter and environment are named | MSG-P3-032 | AC6 |
| X5 | A workflow class is placed outside recovery.casewf.workflow | The build fails naming the class and the package rule; the merge is blocked | Build log | AC7 |
| X6 | A role without Platform administration U calls the smoke endpoint | The call is refused with 403; nothing starts | MSG-P4-002 | TC-E1-071-08 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the cluster of RWB-E1-070, the parameters of RWB-E1-042, the flag of RWB-E1-047 and the module rules of RWB-TE-001; the smoke workflow is self-contained |
| Negotiable | The smoke schedule, build ID format and retry policy are configuration; the codec, the package boundary and the ID conventions are fixed |
| Valuable | Epic 3 starts from a worker that already encrypts payloads, records a decision and survives a restart |
| Estimable | One worker, one codec, one gateway, one smoke workflow and one endpoint |
| Small | Fits two weeks with its tests |
| Testable | Each criterion in section 7 is one test in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Temporal worker and SDK in the recovery module

  Background:
    Given the worker is built with the Temporal Java SDK version pinned for RWB-E1-070
    Given rwb.p3.temporal is on and the parameters temporal.target, temporal.namespace and temporal.taskqueue.platform have values for SIT

  Scenario: AC1 Smoke workflow completes
    Given the Quartz smoke job runs at 06:00 on 16 November 2026
    When PlatformSmokeWorkflow "platform-smoke-20261116" starts on task queue rwb-platform
    Then the workflow runs one activity and ends COMPLETED within 60 seconds
    Then one decision_log_entry exists with decision code PLATFORM_SMOKE, actor SY-CASEWF and inputsRef "platform-smoke-20261116"
    Then no recovery_case row is created or changed

  Scenario: AC2 History holds encrypted payloads only
    Given the smoke activity input carries the synthetic national ID "1101700203456"
    When the workflow completes
    Then the raw history from the Temporal CLI shows the payload as binary ciphertext with codec metadata
    Then the string "1101700203456" appears nowhere in the history or the worker log
    Then decoding through PdpaPayloadCodec with the Key Vault key returns the input
    Then the worker log holds the workflow ID and no payload

  Scenario: AC3 Temporal unreachable
    Given the Temporal frontend is unreachable on port 7233
    When U-70 calls POST /api/recovery/v1/admin/workflows/smoke
    Then the response is 503 with MSG-P3-036
    Then no workflow execution exists and no decision_log_entry is written
    Then the metric workflow_start_failures_total increases by one

  Scenario: AC4 Duplicate workflow ID
    Given platform-smoke-20261116 is RUNNING
    When U-70 calls the smoke endpoint again with workflow ID platform-smoke-20261116
    Then the response is 200 with the same run ID and status RUNNING
    Then the history holds one WorkflowExecutionStarted event
    Then the activity runs once

  Scenario: AC5 Flag off
    Given rwb.p3.temporal is off in DEV
    When the application starts
    Then no worker is registered on rwb-platform and no poller connection is opened
    When U-70 calls POST /api/recovery/v1/admin/workflows/smoke
    Then the response is 404 and no workflow starts

  Scenario: AC6 Missing parameter at start-up
    Given temporal.target has no value for SIT
    When the application starts in SIT
    Then start-up fails with MSG-P3-032 naming temporal.target and SIT
    Then no worker polls and the health endpoint stays 503

  Scenario: AC7 Workflow class outside the package
    Given a branch adds the class recovery.casewf.smoke.SmokeWorkflowImpl outside recovery.casewf.workflow
    When the build runs WorkflowBoundaryTest
    Then the build fails naming the class and the package rule
    Then the merge is blocked
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Workflow code lives only in recovery.casewf.workflow; activities, gateways and I/O live in recovery.casewf.activities or the owning module, and the boundary test enforces it | D-RCV-36 T7; ADR-011 |
| BR2 | Workflow code is deterministic: no clock, random, I/O, parameter read or direct Drools call; time comes from Workflow.currentTimeMillis or a timer, and all I/O is an activity | D-RCV-36 T7 |
| BR3 | Every payload passes through PdpaPayloadCodec (AES-GCM, key in Azure Key Vault); no clear personal data in history, logs, tests or prompts | D-RCV-36 T1; NFR-045 |
| BR4 | Task queues are rwb-platform for smoke and health in Epic 1; rwb-case and rwb-integration are reserved for Epic 3 and no Epic 1 workflow uses them | D-RCV-36 T1 |
| BR5 | Workflow IDs are platform-smoke-{yyyymmdd} and, from Epic 3, case-{caseId}; a repeated start with the same ID returns the running execution and never starts a second run | D-RCV-36 T1; R-UNI-40 |
| BR6 | Every worker carries the build ID from the pipeline; a worker with an unknown build ID takes no new workflow | D-RCV-36 T1 |
| BR7 | With rwb.p3.temporal off, no worker is registered, no poller is opened and the smoke endpoint returns 404; nothing else changes | D-RCV-36 T1; RWB-E1-047 |
| BR8 | A required parameter with no value stops start-up with MSG-P3-032; the service never substitutes a default for temporal.target, temporal.namespace or temporal.taskqueue.platform | REQ-DRI-010; MSG-P3-032 |
| BR9 | The smoke activity writes its decision log entry through DecisionLogWriter before the workflow completes; a failed write fails the workflow | REQ-DRI-005; RWB-E1-027 |
| BR10 | The smoke workflow reads no case, no ACE view and no business table | D-RCV-35 U1; RWB-TE-001 |
| BR11 | A start that cannot reach the frontend fails with MSG-P3-036 and writes no workflow, no history and no decision log entry | D-RCV-36 T1; REQ-DRI-007 |

## 9. State transitions

None for a case. This story changes the status of the platform smoke workflow only.

| From | Event | Condition | To |
|---|---|---|---|
| None | Start | Workflow ID not known | RUNNING |
| RUNNING | Activity completes | The decision log entry is committed | COMPLETED |
| RUNNING | Activity fails after its retry policy | No decision log entry is written | FAILED |
| COMPLETED or FAILED | Retention 30 days | The workflow is closed | Removed from visibility; archive is RWB-E2-039 |

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM | Runs the smoke workflow on demand, reads the worker health and the history (Platform administration, U) |
| RW-AUDIT | Reads the history and the decision log entry (Platform administration and Decision log, R) |
| RW-SECADM | Reads the codec configuration; decode through the codec server is RWB-E2-038, not this story |
| SY-CASEWF | The worker identity; connects with mTLS and writes the PLATFORM_SMOKE entry (Decision log C) |
| RW-COE | Reads the smoke result as a platform check (Platform administration, R) |
| RW-TRIBE | Builds and deploys the worker through the pipeline; has no PROD endpoint right |
| No delegation of authority level applies | A smoke run is not a credit decision |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |
| DF-DEC-030 | decision_log_entry | actor_user_id | Write |
| DF-DEC-031 | decision_log_entry | idempotency_key | Write, read |
| DF-REF-028 | lov_value | lov_code | Read |
| DF-REF-029 | lov_value | value_code | Read |

The PLATFORM_SMOKE entry has no case, no rule ID and no version group; it is a system event under the same exception that RWB-E1-027 applies to access events. Its idempotency key is the workflow ID. The parameters temporal.target, temporal.namespace and temporal.taskqueue.platform are read through ParameterService (RWB-E1-042) and add no field. Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**POST /api/recovery/v1/admin/workflows/smoke** (P3 endpoint)

| Item | Value |
|---|---|
| Request | Body optional: { workflowId: string }. Default platform-smoke-{yyyymmdd} in the server time zone |
| Response | 200 WorkflowRun: workflowId, runId, workflowType, status, taskQueue, startedAt |
| Errors | 401 (MSG-P4-001); 403 no Platform administration U (MSG-P4-002); 404 flag off; 409 the workflow ID already completed for the day (MSG-GEN-004); 503 Temporal unreachable (MSG-P3-036) |
| Authorization | Platform administration, right U |
| Idempotency | Workflow ID; a repeat while RUNNING returns the running execution, and a repeat after COMPLETED returns 409 with no second run |

**Published interface WorkflowGateway** (package recovery.casewf.workflow, Epic 1):

```java
public interface WorkflowGateway {
    String start(String workflowType, String workflowId, Object input); // returns the run ID; throws WorkflowUnavailableException (MSG-P3-036)
    void signal(String workflowId, String signal, Object payload);
}

public record WorkflowRun(String workflowId, String runId, String workflowType, String status,
                          String taskQueue, Instant startedAt) {}
```

The gateway is the only way a Workbench module starts or signals a workflow. It applies the PdpaPayloadCodec and the workflow ID convention, and it never exposes a Temporal type to a caller.

## 13. Solution plan

**Package.** Worker, codec and gateway in `recovery/casewf/workflow` and `recovery/casewf/activities` (Java packages `recovery.casewf.workflow` and `recovery.casewf.activities`); the endpoint in `recovery/casewf/admin`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TemporalConfig | Configuration | Reads temporal.target, temporal.namespace and temporal.taskqueue.platform through ParameterService; fails start-up with MSG-P3-032 on a missing value |
| TemporalWorkerLifecycle | Service | Starts and stops the worker with rwb.p3.temporal; registers the workflow and activity classes and the build ID |
| PdpaPayloadCodec | Service | AES-GCM payload encryption with the Key Vault key; the only data converter on the client and the worker |
| WorkflowGatewayImpl | Service | Implements the published gateway: start and signal by workflow ID; maps an unreachable frontend to MSG-P3-036 |
| PlatformSmokeWorkflow | Workflow | One activity, then complete; deterministic and free of I/O |
| PlatformSmokeActivity | Activity | Writes the PLATFORM_SMOKE decision log entry and returns the build ID |
| SmokeScheduleJob | Job | Quartz, daily at 06:00, calls WorkflowGateway.start with platform-smoke-{yyyymmdd} |
| WorkerBuildIdProvider | Service | Reads the build ID from the pipeline manifest and refuses to start without it |
| WorkflowAdminController | Controller | POST /admin/workflows/smoke with the access check |
| WorkflowBoundaryTest | Test | Fails the build when a workflow class is outside recovery.casewf.workflow |

**Database.** No new table and no migration. The smoke activity writes decision_log_entry through DecisionLogWriter (RWB-E1-027), in the activity's transaction.

**Configuration and reference data**

- Parameters through RWB-E1-042: temporal.target (host and port), temporal.namespace = rwb-recovery, temporal.taskqueue.platform = rwb-platform, temporal.retention.days = 30.
- Feature flag rwb.p3.temporal through RWB-E1-047.
- Key Vault key name for the codec, one per environment; the key is never in a values file or a test.
- Build ID format `<git-sha>-<build-number>` from the pipeline manifest.

**Build steps**

1. Add the Temporal SDK at the pinned version and the Spring Boot starter; prove the dependency lock holds the version.
2. Build TemporalConfig with the parameter reads and the missing-value failure; test AC6.
3. Build PdpaPayloadCodec and register it on the client and the worker; test AC2 with a synthetic national ID.
4. Build WorkflowGatewayImpl with the ID convention and the unreachable mapping; tests AC3 and AC4.
5. Build PlatformSmokeWorkflow, PlatformSmokeActivity and the decision log write; test AC1.
6. Build SmokeScheduleJob on Quartz and add its job_catalog row through RWB-E1-056.
7. Build the worker lifecycle and the flag check; test AC5.
8. Build the endpoint with the access check; access test.
9. Build WorkflowBoundaryTest and prove it fails on a class outside the package; test AC7.

**Feature flag.** `rwb.p3.temporal`. Off: no worker, no poller, the smoke endpoint returns 404, and no other behaviour changes.

**Done when.** The tests in section 16 pass, the smoke workflow completes daily in SIT with one decision log entry, and the raw history holds no clear personal data.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-036 | The workflow service is unreachable or refuses a start | The workflow service is not available. Try again in a few minutes. |
| MSG-P3-032 | A required parameter has no value at start-up | Parameter {name} has no value for {environment}. The service did not start. |
| MSG-P4-002 | A role without Platform administration U calls the smoke endpoint | You cannot {action} here. Your role does not include it. |

MSG-P3-036 is new and is added to Error and Message Standard v4. MSG-P3-032 exists and is reused unchanged.

## 15. Screens and states

No Workbench screen in this story. The platform administrator calls the smoke endpoint and reads the Temporal Web UI; the job monitor of RWB-E1-056 shows the daily smoke job with its last run, status and duration. The smoke run has the states Not run, Running, Completed and Failed. SCR-44 Interface and job monitor shows the same data from Epic 2.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-071-01 | AC1, BR9 | System | PlatformSmokeWorkflow platform-smoke-20261116 on rwb-platform |
| TC-E1-071-02 | AC2, BR3 | System | Synthetic national ID 1101700203456 in the activity input |
| TC-E1-071-03 | AC3, BR11 | System | Frontend stopped; smoke endpoint called |
| TC-E1-071-04 | AC4, BR5 | System | The same workflow ID started twice while RUNNING |
| TC-E1-071-05 | AC5, BR7 | System | rwb.p3.temporal off in DEV |
| TC-E1-071-06 | AC6, BR8 | System | temporal.target missing for SIT |
| TC-E1-071-07 | AC7, BR1 | System | Workflow class in recovery.casewf.smoke |
| TC-E1-071-08 | Access | Access | RW-CASEOWN calls POST /admin/workflows/smoke and is refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the target, namespace, task queue, retention and flag are parameters.
- No personal data in logs, tests, workflow history or prompts: every payload is encrypted; the test national ID is synthetic.
- No read of another module's tables; ACE data only through recovery.v_ace_* views: the smoke workflow reads no case and no ACE row.
- Workflow code is deterministic: no clock, random, I/O or Drools call in workflow code; all I/O is an activity.
- The codec is the only payload path; no clear personal data is written to history, even in DEV.
- No worker without a build ID and no start with a missing parameter.
- No Temporal Schedule and no case wait on Quartz; the smoke job is the only Epic 1 workflow and it has no business wait.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-005 | No action proceeds if its decision entry cannot be written | Epic 1, 3.7 | None (platform enabler) | All recovery processes | R-UNI-39 | TC-E1-071-01, TC-E1-071-02, TC-E1-071-03 |
| REQ-DRI-007 | A failed start reaches a named owner; a retry is safe | Epic 1, 3.2; Program, 5.2 | None (platform enabler) | All recovery processes | R-UNI-40 | TC-E1-071-03, TC-E1-071-04, TC-E1-071-05, TC-E1-071-07 |
| REQ-DRI-010 | Every threshold, limit and name is a versioned parameter | Epic 1, 3.2; Program, 5.1 and 5.7 | None (platform enabler) | All recovery processes | R-UNI-38 | TC-E1-071-06 |

## 19. Out of scope

- Case workflows, case signals and the case task queue (Epic 3).
- The replay test gate, history export and build ID rollout (RWB-E2-040).
- Workflow alerts, the stuck workflow scanner and the workflow dashboard (RWB-E2-037).
- The codec server, decode and the Temporal admin audit (RWB-E2-038).
- Backup, failover, upgrade and archive (RWB-E2-039).
- The reference case workflow skeleton (RWB-E2-043).
- The Temporal cluster, namespace, mTLS and Web UI (RWB-E1-070).
