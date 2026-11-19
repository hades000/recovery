<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5.zip!RWB E2 040 Workflow versioning and replay test gate v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5.zip!RWB E2 040 Workflow versioning and replay test gate v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-040 Workflow versioning and replay test gate

SCB Collections and Recovery. Henka Group, 16 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-040 |
| Epic | E2, release 31 December 2026 |
| Module | P2 Integration |
| Feature | None (platform enabler) |
| Requirement IDs | REQ-DRI-005 |
| BRD section | Business Requirements Epic 2, section 3.2; Business Requirements Program, section 5.7 |
| L3 process | All recovery processes |
| Decision | D-RCV-36 (T1, T7); ADR-011 |
| Priority | Must |
| Depends on | RWB-E1-071 |
| Status | Ready for build |

## 1. Story

As a **developer**, I want **every workflow change replayed against recorded histories in the pipeline, and workers rolled out by build ID**, so that **a change never breaks a case already in flight**.

## 2. Business rationale

Temporal workflow code must replay: a worker that picks up a running workflow re-executes its code against the recorded history, and any change in the order of commands makes the replay fail with a non-determinism error. The workflow then stops, the case waits, and the failure appears in production rather than in the pipeline. Epic 3 will change case workflows release after release while cases are open, so the gate that catches this must exist before the first case workflow is written, not after the first incident.

This story adds gate 10 to the pipeline: a nightly export of SIT histories, a replay of every affected history against the branch build, time-skipping tests for timers, and a build ID rollout that lets running workflows finish on the build they started on. It meets REQ-DRI-005: a replay that reaches the same decisions proves that the recorded decision path still matches the code, and a change that would make a recorded decision unreproducible is refused before it reaches a case. The measure is that no workflow change merges without a gate 10 result and that no build is retired with a running workflow.

## 3. Preconditions

- RWB-E1-071 is done: the worker, WorkflowGateway, WorkerBuildIdProvider, the smoke workflow and the build ID format `<git-sha>-<build-number>` exist, and the worker polls rwb-platform.
- The Temporal Java SDK test kit, WorkflowReplayer and TestWorkflowEnvironment, is on the test classpath at the pinned SDK version and in test scope only.
- The SIT namespace rwb-recovery holds histories for the workflow types under test: PlatformSmokeWorkflow and the test-only CaseHoldWorkflow, and from Epic 3 CaseWorkflow.
- The Blob container rwb-temporal-replay exists with a 90-day retention, and the nightly export job runs in SIT only.
- The pipeline runs the nine checks of Recovery Workbench Engineering Practices, and the merge checklist and pull request template are held in the repository.
- No production history is exported and no production data is used in a test or a prompt (NFR-045).
- Feature flag rwb.p3.temporal is on in SIT; the gate itself has no flag.

## 4. Flow

1. HistoryExportJob (Quartz, nightly at 01:00, SIT only): exports the last 200 closed histories per workflow type through the Temporal API, checks each payload, writes the file and the index row to Blob, and records the export time.
2. Developer: changes a workflow class, an activity signature or the order of commands, and raises a pull request.
3. Pipeline gate 10 (ReplayTestGate): reads the index for the affected workflow types and replays every history against the branch build with WorkflowReplayer.
4. ReplayTestGate: on a non-determinism error, reports the workflow type, history ID, event ID and the first mismatch, and fails the gate with MSG-P3-038.
5. ReplayTestGate: runs the time-skipping tests in TestWorkflowEnvironment, including a workflow that waits on a 30-day timer.
6. Developer: on a failure, restores the old path or guards the change with Workflow.getVersion, then runs the gate again.
7. Reviewer: merges only with a passing gate 10 result on the pull request; a workflow change with no result cannot merge.
8. Deploy: the pipeline registers the new build ID as the default for the task queue; new workflows start on it and running workflows stay on their build.
9. Rollout report: counts running workflows per build; the script refuses to retire a build with a running workflow and retires it when the count reaches zero.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The nightly export failed, a workflow type has no history, or the newest history is more than 24 hours old | The gate fails closed with no replay; the merge is blocked and the failure names the export job and its last successful run | MSG-P3-038 | AC6 |
| X2 | The rollout script is asked to retire a build that still has a running workflow | The script refuses and names the workflow IDs; the build stays REGISTERED and its workers stay up | None (script refusal) | AC7 |
| X3 | A replay history holds a clear personal data pattern, because a test wrote it without the codec | The file is not written to the replay store, the index row is FAILED, an incident is raised, and the gate fails closed for that workflow type | None (incident only) | AC8 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the worker, build ID and gateway of RWB-E1-071; it adds the export, the gate, the time-skipping tests and the rollout script |
| Negotiable | The history count, the freshness limit, the time budget and the retention are configuration; the replay rule and the build ID rule are fixed |
| Valuable | A workflow change that would strand a live case is stopped in the pipeline, not in production |
| Estimable | One export job, one gate, two test bases, one rollout script and one document update |
| Small | Fits two weeks with its tests |
| Testable | Each criterion in section 7 is one test in section 16 on fixed histories and build IDs |

## 7. Acceptance criteria

```gherkin
Feature: Workflow versioning and replay test gate

  Background:
    Given the replay store holds 200 histories exported from SIT on 16 November 2026, including 40 of workflow type PlatformSmokeWorkflow
    Given the export timestamp is 01:00 on 16 November 2026 and the gate runs at 09:00 on 16 November 2026
    Given rwb.p3.temporal is on in SIT

  Scenario: AC1 A non-deterministic change fails the gate
    Given build ID "9f3c2a1-418" produced the 40 PlatformSmokeWorkflow histories
    Given a branch removes the activity call from PlatformSmokeWorkflow and completes at once
    When pipeline gate 10 replays the 40 histories against the branch build
    Then the replay fails with a non-determinism error at the first mismatched event "ActivityTaskScheduled", event ID 4
    Then the gate fails and the merge is blocked with MSG-P3-038 naming the workflow type, history ID and event ID
    Then no build ID is registered for the branch and no worker takes a workflow with that code

  Scenario: AC2 A change guarded by Workflow.getVersion passes
    Given the same 40 PlatformSmokeWorkflow histories
    Given the branch adds a second activity and guards it with Workflow.getVersion("smoke-step-2", Workflow.DEFAULT_VERSION, 2)
    When gate 10 replays the 40 histories
    Then every history takes the pre-version path and replays to the end without error
    Then a new execution takes version 2 and runs the second activity
    Then a history recorded under version 2 replays on the branch build with version 2
    Then the gate passes and the pull request may merge

  Scenario: AC3 Time skipping runs a 30-day timer in under a minute
    Given a test workflow waits on a 30-day timer and then calls one activity
    When the time-skipping test runs in TestWorkflowEnvironment
    Then the timer fires and the workflow completes in under 60 seconds of wall-clock time
    Then the test reports the simulated elapsed time of 30 days
    Then the gate's total run stays inside its 10-minute budget
    Then a run over the budget is reported as failed and never as passed

  Scenario: AC4 A new build ID takes new workflows and old ones drain
    Given build ID "9f3c2a1-418" is the default for rwb-platform and 12 workflows are RUNNING on it
    When the pipeline deploys build ID "7b1d4e0-419" and registers it as the new default
    Then a workflow started after the deploy runs on "7b1d4e0-419"
    Then the 12 running workflows finish on "9f3c2a1-418"
    Then the rollout report shows 12 draining on the old build and 1 running on the new build
    Then the old build is retired only when its running count is zero

  Scenario: AC5 The gate is pipeline gate 10
    Given Recovery Workbench Engineering Practices lists the nine pipeline checks
    When this story is merged
    Then gate 10, "Workflow replay and time-skipping tests", is listed with its owner, its pass rule, its budget and its failure message MSG-P3-038
    Then the merge checklist and the pull request template name gate 10
    Then a pull request that changes a class under recovery.casewf.workflow without a gate 10 result cannot merge

  Scenario: AC6 A stale or missing history export fails the gate closed
    Given the nightly history export failed and the newest history in the replay store is 36 hours old
    When gate 10 runs for a branch that changes PlatformSmokeWorkflow
    Then the gate fails closed with "history export stale" and runs no replay
    Then the merge is blocked and the failure names the export job and its last successful run
    Then no result is reported as a pass
    Then the gate passes only after a fresh export exists

  Scenario: AC7 A build with a running workflow is not retired
    Given build ID "9f3c2a1-418" still has 2 RUNNING workflows
    When the rollout script is asked to retire it
    Then the script refuses and names the 2 workflow IDs
    Then the build stays REGISTERED, its workers stay up and new workflows do not start on it
    Then the retire command succeeds only after both workflows close

  Scenario: AC8 A replay history with a clear payload is refused
    Given a replay history file holds a salary slip payload with the national ID "1101700203456" in clear text, because a SIT test wrote it with the codec off
    When the export job validates the file
    Then the file is not written to the replay store and the index row is FAILED
    Then an incident reaches RW-SECADM and RW-PLATADM
    Then gate 10 fails closed for that workflow type until a clean export exists
    Then the test profile is corrected and the history is deleted at the source
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Workflow code is deterministic, and every change is replayed against the recorded histories of the affected workflow types before merge | D-RCV-36 T7; ADR-011 |
| BR2 | A non-deterministic change fails gate 10 with MSG-P3-038 and blocks the merge; no label, flag or reviewer waives the gate | AC1 |
| BR3 | A behaviour change is guarded with Workflow.getVersion; an old history takes the old path and a new execution takes the new one | AC2 |
| BR4 | Time-skipping tests run every timer in the changed workflow; a 30-day timer completes in under a minute, and a gate run over its 10-minute budget fails | AC3 |
| BR5 | Gate 10 is listed in Recovery Workbench Engineering Practices with its owner, pass rule, budget and failure message, and is part of the merge checklist | AC5 |
| BR6 | Replay histories come from SIT only, are codec-encrypted, are kept 90 days and hold no clear personal data; a history that fails the check is not used | NFR-045; AC8 |
| BR7 | The gate fails closed when the export is missing, stale by more than 24 hours, or refused; it never passes on an empty set | AC6 |
| BR8 | Workers register a build ID; a new workflow goes to the newest default build and a running workflow stays on the build it started on | AC4 |
| BR9 | A build is retired only when it has no running or open workflow, and the rollout script refuses otherwise | AC7 |
| BR10 | The histories per type, the freshness limit, the time budget, the history retention and the build ID format are configuration, never code | REQ-DRI-005 |

## 9. State transitions

None for a case. A build ID and a gate run change state.

| From | Event | Condition | To |
|---|---|---|---|
| None | Deploy and register | The gate passed | REGISTERED |
| REGISTERED | Register as the default for the task queue | It is the newest build | CURRENT; the previous build becomes DRAINING |
| DRAINING | The last running workflow closes | Running count is zero | RETIRED |
| DRAINING | Retire requested | A workflow is still running | DRAINING, refused with the workflow IDs |
| None | Gate run | A history mismatches or the export is stale | FAILED; the merge is blocked |
| None | Gate run | Every history replays and the tests pass | PASSED; the merge may proceed |

## 10. Authority

| Who | What they may do in this story |
|---|---|
| Developer, squad member (RW-TRIBE) | Changes workflow code, runs gate 10, reads the replay report (Platform administration, R) |
| Reviewer | Approves the merge only with a passing gate 10 result |
| RW-PLATADM | Runs the rollout, registers a build as the default, retires a build when its count is zero (Platform administration, U) |
| RW-AUDIT | Reads the gate result, the export manifest and the build registry (Platform administration, R) |
| RW-COE | Reads the gate result for a workflow that evaluates a rule package; may not change the gate |
| RW-SECADM | Receives a clear-payload incident from the export; decode stays with RWB-E2-038 |
| No delegation of authority level applies | A pipeline gate is not a credit decision |

Separation of duty: the developer who changes the workflow does not approve the merge.

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| None (platform enabler) | None in the recovery schema | None | None |

Replay histories and their index live in Blob storage, container rwb-temporal-replay; the build registry lives in Temporal; the gate result lives in the pipeline and on the pull request; the export job's schedule, owner and run book path live in job_catalog through RWB-E1-056. No DF-REF, DF-CAS or DF-DEC field is added or changed, and the Physical Schema v6 is unchanged.

## 12. Contract

No Workbench endpoint. This story adds no path under /api/recovery/v1. The interfaces are the SDK test kit, Blob storage, the Temporal build ID API and the pipeline.

| Interface | Method | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|
| WorkflowReplayer | In-process Java call at the pinned SDK version | Workflow class, workflow type, a recorded history | Replay result, or a NonDeterministicException with the event ID | Non-determinism; unknown workflow type | Build and test process only | Read only; replaying the same history twice gives the same result |
| TestWorkflowEnvironment | In-process time-skipping test | Test workflow, timer, activities | Result and the elapsed wall-clock time | Assertion failure; budget exceeded | Build and test process only | Each test run is independent |
| Blob storage (replay) | HTTPS GET and LIST on container rwb-temporal-replay | Index prefix, workflow type, history ID | Index rows and history files | 403 role; 404 no such history; 409 immutability | SY-CASEWF writes in SIT; the build reads | The workflow ID and run ID path is the key |
| Temporal build ID API | gRPC over mTLS, port 7233: UpdateWorkerBuildIdCompatibility, DescribeNamespace | Task queue rwb-platform, build ID set, default build ID | The compatibility set and the default | PERMISSION_DENIED; FAILED_PRECONDITION | Client certificate of SY-CASEWF from the pipeline | Registering the same build ID twice changes nothing |
| Pipeline gate 10 | Pipeline step on the pull request | Branch build, affected workflow types, replay index | PASSED or FAILED, with the report and MSG-P3-038 | A failed replay; a stale export; a budget overrun | The pipeline identity; the result is visible to the reviewer | A re-run on the same commit gives the same result |

The export job never reads a Workbench table or the ACE database. No production history is exported, and the replay store holds SIT data only.

## 13. Solution plan

**Package.** The gate and the test bases in `src/test/java/recovery/casewf/replay`; the export job in `recovery/integration/ops/temporal`; the pipeline step in `.github/workflows/`; the rollout script in `deploy/temporal/rollout/`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ReplayTestGate | Test and pipeline step | Selects the affected types, replays every history, reports the first mismatch and fails with MSG-P3-038 (BR1, BR2, BR7) |
| HistoryExportJob | Job | Quartz, nightly in SIT: exports 200 closed histories per type, validates and writes the file and the index (BR6) |
| ReplayPayloadCheck | Service | Refuses a history whose payload is not codec-encrypted or holds a clear personal data pattern (BR6) |
| ReplayHistoryStore | Repository | Writes and lists the replay files and the index rows in Blob |
| TestWorkflowEnvironmentBase | Test base | Starts the SDK test environment at the pinned version and applies the shared timeouts |
| TimeSkippingTimerTest | Test | The 30-day timer test and the gate budget check (BR4) |
| BuildIdRolloutScript | Script | Registers a build, reports the running count per build and refuses a premature retirement (BR8, BR9) |
| GateReportPublisher | Service | Attaches the gate result and the replay report to the pull request |

**Database.** No migration and no new table. The export job gets one job_catalog row through RWB-E1-056 as a data change. The replay files and the index live in Blob storage.

**Configuration and reference data**

- 200 histories per workflow type, a 24-hour freshness limit, a 10-minute gate budget and a 90-day replay retention.
- The build ID format `<git-sha>-<build-number>` from RWB-E1-071.
- The list of workflow packages the gate watches: `recovery.casewf.workflow`, from the boundary test of RWB-E1-071.
- Feature flag rwb.p3.temporal for the worker only; the gate has no flag and cannot be switched off.

**Build steps**

1. Build HistoryExportJob and ReplayPayloadCheck; test AC8 and the index with 200 synthetic histories.
2. Build ReplayTestGate over WorkflowReplayer and prove it fails on a deliberate non-deterministic change; test AC1.
3. Add a getVersion guard to the test workflow and prove the old histories pass; test AC2.
4. Build TestWorkflowEnvironmentBase and TimeSkippingTimerTest; test AC3 and the budget.
5. Build BuildIdRolloutScript with the running count and the refusal; test AC4 and AC7.
6. Add the pipeline step, the report and the merge rule; test AC5 and AC6.
7. Add the gate to Engineering Practices, the merge checklist and the pull request template; run the gate on a real pull request in SIT.

**Feature flag.** None on the gate. With rwb.p3.temporal off, no workflow runs, the export finds no history and the gate fails closed; the gate is on in every environment where a workflow class can change.

**Done when.** A deliberate non-deterministic change fails gate 10 in SIT, a getVersion change passes, the 30-day timer test completes in under a minute, a build drains and retires with no lost workflow, and gate 10 is listed in Engineering Practices.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-038 | A workflow change fails the replay test against the recorded histories | The workflow change fails the replay test against recorded histories: {detail}. |

MSG-P3-038 is new and is added to Error and Message Standard v4. {detail} names the workflow type, the history ID, the event ID and the first mismatch, and never a payload. The same message is used for a stale export, with {detail} naming the export job and its last successful run. The gate report carries the same text; no other message ID is added.

## 15. Screens and states

No Workbench screen in this story. The views are the pipeline gate report on the pull request, with the states PASSED, FAILED and Running, and the build registry in the rollout report, with the states REGISTERED, CURRENT, DRAINING and RETIRED. The reviewer sees the gate result on the pull request and in the merge checklist. The platform screens of Epic 8 do not repeat this data.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-040-01 | AC1, BR1, BR2 | System | 40 PlatformSmokeWorkflow histories; branch removes the activity call |
| TC-E2-040-02 | AC2, BR3 | System | The same 40 histories; getVersion "smoke-step-2" version 2 |
| TC-E2-040-03 | AC3, BR4 | System | Test workflow with a 30-day timer; 60-second and 10-minute budgets |
| TC-E2-040-04 | AC4, BR8 | Operational | Build IDs 9f3c2a1-418 and 7b1d4e0-419; 12 running workflows |
| TC-E2-040-05 | AC5, BR5 | Operational | Engineering Practices, merge checklist and pull request template |
| TC-E2-040-06 | AC6, BR7 | System | Replay index 36 hours old; branch changes PlatformSmokeWorkflow |
| TC-E2-040-07 | AC7, BR9 | System | Build 9f3c2a1-418 with 2 running workflows; retire requested |
| TC-E2-040-08 | AC8, BR6 | System | History written with the codec off; clear national ID 1101700203456 |
| TC-E2-040-09 | Operational | Operational | Nightly export in SIT writes 200 encrypted histories per type and the index |
| TC-E2-040-10 | Operational | Operational | Full rollout in SIT: new build takes new workflows, old build drains and retires |

The checks are run by the developer, the reviewer and the platform administrator in SIT and recorded on the pull request and in the release evidence; there is no Workbench endpoint and no Access test in this story. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the history count, the freshness limit, the time budget, the retention and the build ID format are configuration.
- No personal data in logs, tests, workflow history or prompts: the replay store holds codec-encrypted SIT histories only, and a clear payload is refused.
- No read of another module's tables; ACE data only through recovery.v_ace_* views: this story reads no case and no ACE table.
- No production history is exported, and no production data is used in a test or a prompt.
- No workflow change merges without a passing gate 10 result, and no label or flag waives the gate.
- A stale, missing or refused export fails the gate closed; an empty replay set is never a pass.
- No build is retired while it has a running workflow, and no new workflow starts on a draining build.
- No change to the pinned SDK version without the gate run at the new version.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | Epic 2, 3.2; Program, 5.7 | None (platform enabler) | All recovery processes | R-UNI-39 | TC-E2-040-01, TC-E2-040-02, TC-E2-040-03, TC-E2-040-04, TC-E2-040-06, TC-E2-040-08 |

## 19. Out of scope

- The Temporal cluster, namespace and Web UI (RWB-E1-070).
- The worker, codec, gateway and smoke workflow (RWB-E1-071).
- Case workflow code and the reference skeleton (Epic 3, RWB-E2-043).
- Alerts, the stuck scanner and the dashboard (RWB-E2-037).
- The codec server, decode and the administrative audit (RWB-E2-038).
- Backup, failover, upgrade and archive (RWB-E2-039).
- The other nine pipeline checks and the release gates (Recovery Workbench Engineering Practices).
- Load, performance and soak testing of workflow executions (RWB-E1-056, Epic 3).
- Production history export and replay against production data.
