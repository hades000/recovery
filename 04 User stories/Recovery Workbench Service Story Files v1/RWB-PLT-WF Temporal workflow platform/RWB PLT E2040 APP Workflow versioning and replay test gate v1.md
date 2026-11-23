# RWB-PLT-E2040-APP Workflow versioning and replay test gate

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-E2040-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-WF |
| Wave | 0 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-040 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-PLT-WF-I |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E2040-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-014, FR-PLT-015) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-040 for the workflow platform epic; the replay test gate becomes the platform's single gate for every worker and every service task queue, the nightly export becomes a Temporal Schedule at 01:00 on task queue `rwb-platform`, build rollout follows Worker Versioning on Temporal 1.30+, and the eight legacy criteria are carried whole. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **developer**, I want **every workflow change replayed against recorded histories in the pipeline, and workers rolled out by build ID**, so that **a change never breaks a case already in flight**.

This is the split (rework) slice of legacy key RWB-E2-040 under epic RWB-PLT-WF (Template and Rules §R6). No legacy section is copied without change and no delta copy of an as-built story is made: section 7 carries the eight legacy criteria with every value kept, and the microservice change for the legacy key is described here. The change from the legacy story:

- **One gate, not one gate per module.** The gate moves out of the monolith's case-workflow module and becomes the platform's gate: one `ReplayTestGate` pipeline step, one export, one set of test bases and one rollout script for every worker and every service task queue (`rwb-case`, `rwb-treatment`, `rwb-litigation` and the rest), owned once by the platform team and inherited by every service (Architecture v5 slide 23; Temporal and Drools Design slide 27 notes). The Workbench API Specification carries none of its paths.
- **Contract first.** The export manifest and index shape, the replay report shape, the gate result values, the build-registry commands, the error vocabulary and the fakes are published on Day 1 by RWB-PLT-E2040-CON, before any code (ADR-020). This story builds against that contract and its fake.
- **The nightly export.** The 01:00 export stops being a Quartz job — Quartz is retired with RWB-TE-007 (Template and Rules §R6) — and becomes a Temporal Schedule on task queue `rwb-platform` that starts `HistoryExportJob` in namespace `rwb-recovery` (DP-10 pattern, through RWB-PLT-E1071-CON).
- **Worker Versioning.** A build is no longer a row in a monolith job table: the worker registers a build ID of the form `<git-sha>-<build-number>` against its task queue through the Temporal build ID API on Temporal 1.30 or later, which is the release floor for Worker Versioning (Architecture v5 slide 23; Temporal and Drools Design slide 27 notes); a running workflow stays on the build it started on and a new one starts on the newest default.
- **The histories.** The replay store is a separate Blob container `rwb-temporal-replay` with a 90-day retention, written by the export workflow and read by the gate; it holds codec-encrypted SIT histories only (NFR-045).
- **No service shape.** The platform is **not one of the 19 services**: Template and Rules §R4 has no platform row, so this story owns no `rwb_*` schema, publishes no `rwb.<short>.events.v1` topic and owns no `/api/recovery/<short>/v1` base. What it does own is the gate step, the export Schedule on task queue `rwb-platform` and the rollout script.
- **The message.** A failure reports MSG-P3-038 unchanged, with `{detail}` naming the workflow type, the history ID, the event ID and the first mismatch, and never a payload.

### 2. Business rationale

Temporal workflow code must replay: a worker that picks up a running workflow re-executes its code against the recorded history, and any change in the order of commands makes the replay fail with a non-determinism error. The workflow then stops, the case waits, and the failure appears in production rather than in the pipeline. Epic 3 will change case workflows release after release while cases are open, so the gate that catches this must exist before the first case workflow is written, not after the first incident.

This story adds gate 10 to the pipeline: a nightly export of SIT histories, a replay of every affected history against the branch build, time-skipping tests for timers, and a build ID rollout that lets running workflows finish on the build they started on. It meets REQ-DRI-005: a replay that reaches the same decisions proves that the recorded decision path still matches the code, and a change that would make a recorded decision unreproducible is refused before it reaches a case. The measure is that no workflow change merges without a gate 10 result and that no build is retired with a running workflow.

After the split the gate is the platform's, and that is the point of moving it into this epic. Nineteen services will each own workers on their own task queue, and a per-module gate would give the bank nineteen places where a non-deterministic change can slip past a merge; one gate on the shared platform is written once, upgraded once and applies to every queue the platform runs (Architecture v5 slide 23; Temporal and Drools Design slide 27 notes). The export schedule moves with it, from a Quartz trigger to a Temporal Schedule, so the only timer involved lives where every other Recovery timer lives. Everything else keeps its legacy value: the 200 histories per type, the 24-hour freshness limit, the 10-minute budget, the 60-second timer target, the 90-day retention, the two build IDs and MSG-P3-038.

### 3. Preconditions

- RWB-PLT-E2040-CON is published: the export manifest and index shape, the replay report shape, the gate result values PASSED and FAILED, the build-registry commands (register, describe, retire), the workflow-type watch list rule, the error vocabulary and the fakes.
- The six platform contracts of the build set are published: RWB-PLT-E1027-CON (the local decision-record library and the DecisionLogApi), RWB-PLT-E1043-CON (the reference-data client the platform loads its configuration vocabulary through, DP-07), RWB-PLT-E1071-CON (the worker and SDK contract, the build ID provider, the platform worker on task queue `rwb-platform` and the Schedule template, DP-10), RWB-PLT-E1047-CON (the naming library, DP-14), RWB-PLT-E1044-CON (the per-service Flyway baseline this story deliberately does not use, DP-15) and RWB-PLT-N001-CON (the gateway-bff route surface; the gate report is not a Workbench route, DP-19).
- The owner contract RWB-P3-E1043-CON (reference data of rwb-case) is consumed as a C row through its fake; this story builds against it and does not wait for rwb-case.
- Legacy RWB-PLT-E1071-APP is done: the worker, WorkflowGateway, WorkerBuildIdProvider, the smoke workflow and the build ID format `<git-sha>-<build-number>` exist, and the worker polls task queue `rwb-platform`.
- The Temporal Java SDK test kit, `WorkflowReplayer` and `TestWorkflowEnvironment`, is on the test classpath in test scope only. The release the gate is pinned to is Not specified in the source documents (GAP-1449; ASM-2544); the design puts the floor at Temporal 1.30 or later because Worker Versioning needs it (Temporal and Drools Design slide 27 notes).
- The SIT namespace `rwb-recovery` holds histories for the workflow types under test: PlatformSmokeWorkflow and the test-only CaseHoldWorkflow, and from Epic 3 CaseWorkflow.
- The Blob container `rwb-temporal-replay` exists with a 90-day retention, and the nightly export runs in SIT only. The role that owns the container's retention policy is Not specified in the source documents (GAP-1449; ASM-2544).
- The pipeline runs the nine checks of Recovery Workbench Engineering Practices, and the merge checklist and the pull request template are held in the repository.
- No production history is exported and no production data is used in a test or a prompt (NFR-045).
- The feature flag `rwb.p3.temporal` is on in SIT, read through the parameters contract rather than from a code constant; the gate itself has no flag.
- The platform login that runs the export and the pipeline identity that runs the gate are Not specified in the source documents (GAP-1449; ASM-2544); the working read is the platform workload identity of RWB-PLT-E1071 and a build-agent identity scoped to the SIT namespace.
- No approval is required to start: the story is Draft (realignment v1) and builds against the published contracts and their fakes.

### 4. Flow

1. HistoryExportJob: on the 01:00 Temporal Schedule on task queue `rwb-platform`, in SIT only, exports the last 200 closed histories per workflow type through the Temporal frontend API, passes each payload through ReplayPayloadCheck, writes the file and the index row to the Blob container `rwb-temporal-replay`, and records the export time and its last successful run. In the legacy story this was the Quartz job of the same name; Quartz is retired with RWB-TE-007, so the job is a Schedule-started workflow (DP-10).
2. Developer: changes a workflow class, an activity signature or the order of commands, and raises a pull request.
3. Pipeline gate 10 (ReplayTestGate): reads the index for the affected workflow types and replays every history against the branch build with WorkflowReplayer at the pinned SDK release.
4. ReplayTestGate: on a non-determinism error, reports the workflow type, history ID, event ID and the first mismatch, and fails the gate with MSG-P3-038.
5. ReplayTestGate: runs the time-skipping tests in TestWorkflowEnvironment, including a workflow that waits on a 30-day timer, and holds the whole run to its 10-minute budget.
6. Developer: on a failure, restores the old path or guards the change with `Workflow.getVersion`, then runs the gate again.
7. Reviewer: merges only with a passing gate 10 result on the pull request; a workflow change with no result cannot merge.
8. Deploy: the pipeline registers the new build ID as the default for the task queue through the Temporal build ID API (Worker Versioning, Temporal 1.30+); new workflows start on it and running workflows stay on their build.
9. Rollout report: counts running workflows per build; the script refuses to retire a build with a running workflow and retires it when the count reaches zero, moving REGISTERED to DRAINING and DRAINING to RETIRED.
10. GateReportPublisher: attaches the gate result and the replay report to the pull request; RW-AUDIT reads the same result, and no result is editable after the merge.

The export is a Schedule-started workflow run, not a Quartz job and not a daemon: each 01:00 run is one short workflow on task queue `rwb-platform` with overlap policy SKIP, so a slow export never stacks behind itself (DP-10). The replay rule, the time-skipping rule and the build ID rule are the legacy behaviour unchanged.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The nightly export failed, a workflow type has no history, or the newest history is more than 24 hours old | The gate fails closed with no replay; the merge is blocked and the failure names the export job and its last successful run | MSG-P3-038 | AC6 |
| X2 | The rollout script is asked to retire a build that still has a running workflow | The script refuses and names the workflow IDs; the build stays REGISTERED and its workers stay up | None (script refusal) | AC7 |
| X3 | A replay history holds a clear personal data pattern, because a test wrote it without the codec | The file is not written to the replay store, the index row is FAILED, an incident is raised, and the gate fails closed for that workflow type | None (incident only) | AC8 |
| X4 | A value the story needs is named by no source: the platform login, the gate's pipeline identity, the owner of the replay container's retention and the pinned SDK release the gate runs at | The value is published as the working read of the assumption, the placeholder is written where the value is still open, and the gap stays open; no code constant is written for it | Not specified in the source documents (GAP-1449; ASM-2544) | Section 13 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the worker, build ID and gateway of RWB-PLT-E1071-APP; it adds the export, the gate, the time-skipping tests and the rollout script, and builds against RWB-PLT-E2040-CON and six platform contracts and their fakes |
| Negotiable | The history count, the freshness limit, the time budget and the retention are configuration; the replay rule and the build ID rule are fixed |
| Valuable | A workflow change that would strand a live case is stopped in the pipeline, not in production, once for every queue the platform runs |
| Estimable | One export workflow, one gate, two test bases, one rollout script and one report publisher |
| Small | Fits two weeks with its tests |
| Testable | Each criterion in section 7 is one test in section 16 on fixed histories and build IDs |

### 7. Acceptance criteria

```gherkin
Feature: Workflow versioning and replay test gate

  Background:
    Given the replay store holds 200 histories exported from SIT on 16 November 2026, including 40 of workflow type PlatformSmokeWorkflow
    Given the export timestamp is 01:00 on 16 November 2026 and the gate runs at 09:00 on 16 November 2026
    Given rwb.p3.temporal is on in SIT

  Scenario: AC1 A non-deterministic change fails the gate (legacy RWB-E2-040 AC1)
    Given build ID "9f3c2a1-418" produced the 40 PlatformSmokeWorkflow histories
    Given a branch removes the activity call from PlatformSmokeWorkflow and completes at once
    When pipeline gate 10 replays the 40 histories against the branch build
    Then the replay fails with a non-determinism error at the first mismatched event "ActivityTaskScheduled", event ID 4
    Then the gate fails and the merge is blocked with MSG-P3-038 naming the workflow type, history ID and event ID
    Then no build ID is registered for the branch and no worker takes a workflow with that code

  Scenario: AC2 A change guarded by Workflow.getVersion passes (legacy RWB-E2-040 AC2)
    Given the same 40 PlatformSmokeWorkflow histories
    Given the branch adds a second activity and guards it with Workflow.getVersion("smoke-step-2", Workflow.DEFAULT_VERSION, 2)
    When gate 10 replays the 40 histories
    Then every history takes the pre-version path and replays to the end without error
    Then a new execution takes version 2 and runs the second activity
    Then a history recorded under version 2 replays on the branch build with version 2
    Then the gate passes and the pull request may merge

  Scenario: AC3 Time skipping runs a 30-day timer in under a minute (legacy RWB-E2-040 AC3)
    Given a test workflow waits on a 30-day timer and then calls one activity
    When the time-skipping test runs in TestWorkflowEnvironment
    Then the timer fires and the workflow completes in under 60 seconds of wall-clock time
    Then the test reports the simulated elapsed time of 30 days
    Then the gate's total run stays inside its 10-minute budget
    Then a run over the budget is reported as failed and never as passed

  Scenario: AC4 A new build ID takes new workflows and old ones drain (legacy RWB-E2-040 AC4)
    Given build ID "9f3c2a1-418" is the default for `rwb-platform` and 12 workflows are RUNNING on it
    When the pipeline deploys build ID "7b1d4e0-419" and registers it as the new default
    Then a workflow started after the deploy runs on "7b1d4e0-419"
    Then the 12 running workflows finish on "9f3c2a1-418"
    Then the rollout report shows 12 draining on the old build and 1 running on the new build
    Then the old build is retired only when its running count is zero

  Scenario: AC5 The gate is pipeline gate 10 (legacy RWB-E2-040 AC5)
    Given Recovery Workbench Engineering Practices lists the nine pipeline checks
    When this story is merged
    Then gate 10, "Workflow replay and time-skipping tests", is listed with its owner, its pass rule, its budget and its failure message MSG-P3-038
    Then the merge checklist and the pull request template name gate 10
    Then a pull request that changes a class under recovery.casewf.workflow without a gate 10 result cannot merge

  Scenario: AC6 A stale or missing history export fails the gate closed (legacy RWB-E2-040 AC6)
    Given the nightly history export failed and the newest history in the replay store is 36 hours old
    When gate 10 runs for a branch that changes PlatformSmokeWorkflow
    Then the gate fails closed with "history export stale" and runs no replay
    Then the merge is blocked and the failure names the export job and its last successful run
    Then no result is reported as a pass
    Then the gate passes only after a fresh export exists

  Scenario: AC7 A build with a running workflow is not retired (legacy RWB-E2-040 AC7)
    Given build ID "9f3c2a1-418" still has 2 RUNNING workflows
    When the rollout script is asked to retire it
    Then the script refuses and names the 2 workflow IDs
    Then the build stays REGISTERED, its workers stay up and new workflows do not start on it
    Then the retire command succeeds only after both workflows close

  Scenario: AC8 A replay history with a clear payload is refused (legacy RWB-E2-040 AC8)
    Given a replay history file holds a salary slip payload with the national ID "1101700203456" in clear text, because a SIT test wrote it with the codec off
    When the export job validates the file
    Then the file is not written to the replay store and the index row is FAILED
    Then an incident reaches RW-SECADM and RW-PLATADM
    Then gate 10 fails closed for that workflow type until a clean export exists
    Then the test profile is corrected and the history is deleted at the source
```

The eight criteria above are copied from RWB-E2-040 with every value kept: 200 histories, 40 PlatformSmokeWorkflow histories, 01:00 and 09:00 on 16 November 2026, build IDs "9f3c2a1-418" and "7b1d4e0-419", event ID 4 and "ActivityTaskScheduled", `Workflow.getVersion("smoke-step-2", Workflow.DEFAULT_VERSION, 2)`, the 30-day timer in under 60 seconds, the 10-minute budget, 12 running workflows, 2 running workflows, 36 hours stale, the national ID "1101700203456", gate 10, `recovery.casewf.workflow`, `rwb.p3.temporal` and MSG-P3-038. The realignment mechanics are the ones named in section 1: the export is a Temporal Schedule at 01:00 on task queue `rwb-platform` instead of the retired Quartz job (DP-10), the histories live in the Blob container `rwb-temporal-replay`, rollout follows Worker Versioning on Temporal 1.30 or later, and the gate stays unfakeable and cannot be switched off — the flag `rwb.p3.temporal` governs the worker, never the gate.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Workflow code is deterministic, and every change is replayed against the recorded histories of the affected workflow types before merge | D-RCV-36 T7; ADR-011 |
| BR2 | A non-deterministic change fails gate 10 with MSG-P3-038 and blocks the merge; no label, flag or reviewer waives the gate | RWB-PLT-E2040-CON; AC1 |
| BR3 | A behaviour change is guarded with `Workflow.getVersion`; an old history takes the old path and a new execution takes the new one | ADR-011; AC2 |
| BR4 | Time-skipping tests run every timer in the changed workflow; a 30-day timer completes in under a minute, and a gate run over its 10-minute budget fails | AC3 |
| BR5 | Gate 10 is listed in Recovery Workbench Engineering Practices with its owner, pass rule, budget and failure message, and is part of the merge checklist | Recovery Workbench Engineering Practices; AC5 |
| BR6 | Replay histories come from SIT only, are codec-encrypted by the codec server of RWB-PLT-E2038-CON, are kept 90 days in the Blob container `rwb-temporal-replay` and hold no clear personal data; a history that fails the check is not used | NFR-045; AC8 |
| BR7 | The gate fails closed when the export is missing, stale by more than 24 hours, or refused; it never passes on an empty set | MSG-P3-038; AC6 |
| BR8 | Workers register a build ID of the form `<git-sha>-<build-number>`; a new workflow goes to the newest default build and a running workflow stays on the build it started on | Temporal 1.30+; RWB-PLT-E1071-CON; AC4 |
| BR9 | A build is retired only when it has no running or open workflow, and the rollout script refuses otherwise | AC7 |
| BR10 | The histories per type, the freshness limit, the time budget, the history retention and the build ID format are configuration, never code | REQ-DRI-005 |

### 9. State transitions

None for a case. A build ID and a gate run change state.

| From | Event | Condition | To |
|---|---|---|---|
| None | Deploy and register | The gate passed | REGISTERED |
| REGISTERED | Register as the default for the task queue | It is the newest build | CURRENT; the previous build becomes DRAINING |
| DRAINING | The last running workflow closes | Running count is zero | RETIRED |
| DRAINING | Retire requested | A workflow is still running | DRAINING, refused with the workflow IDs |
| None | Gate run | A history mismatches or the export is stale | FAILED; the merge is blocked |
| None | Gate run | Every history replays and the tests pass | PASSED; the merge may proceed |

The build states are the platform's and live in the Temporal build registry, not in a `rwb_*` schema. A gate run's PASSED or FAILED lives on the pull request and in the pipeline; a running gate run is displayed as Running and is never a result.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Developer, squad member (RW-TRIBE) | Changes workflow code, runs gate 10, reads the replay report (Platform administration, R) |
| Reviewer | Approves the merge only with a passing gate 10 result |
| RW-PLATADM | Runs the rollout, registers a build as the default, retires a build when its count is zero (Platform administration, U) |
| RW-AUDIT | Reads the gate result, the export manifest and the build registry (Platform administration, R) |
| RW-COE | Reads the gate result for a workflow that evaluates a rule package; may not change the gate |
| RW-SECADM | Receives a clear-payload incident from the export; decode stays with RWB-PLT-E2038-APP |
| The platform identity that runs the export Schedule and the pipeline identity that runs the gate | Not specified in the source documents (GAP-1449; ASM-2544) |
| No delegation of authority level applies | A pipeline gate is not a credit decision |

Separation of duty: the developer who changes the workflow does not approve the merge.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| None (platform enabler) | None in a `rwb_*` schema | None | None |

Replay histories and their index live in Blob storage, container `rwb-temporal-replay`, which this story writes through ReplayHistoryStore and reads through the gate; the build registry lives in Temporal persistence and the build ID API; the gate result lives in the pipeline and on the pull request; the export workflow's schedule, owner and run book path are declared by the Schedule itself in the Temporal and Drools design and carry no `job_catalog` row of their own, because the target has no shared job table for per-service Schedules (Ownership Map: job_catalog). No DF-REF, DF-CAS or DF-DEC field is added or changed, this story creates no table and runs no migration, and the Physical Schema is unchanged. The replay files hold codec-encrypted SIT histories only: no payload is read by the gate, no payload is written to a log line and no personal data is held by this story.

### 12. Contract

#### 12.1 REST operations provided

None. The platform has no service short (Template and Rules §R4 has no platform row), so it publishes no path under `/api/recovery/<short>/v1` and no Workbench endpoint. The gate's surfaces are the pipeline step on the pull request, the pull request report and the Blob prefix of the replay store, none of which is a Workbench route (DP-13, DP-19).

#### 12.2 REST operations consumed

None. The gate makes no Workbench REST call at run time: it reads the replay index from Blob, the build registry from the Temporal build ID API and the branch build from the pipeline. The C row RWB-P3-E1043-CON is the owner contract behind the platform reference-data client RWB-PLT-E1043-CON, which the platform loads its configuration vocabulary through at build and test time, and it is reached through its published fake and not through a table read (DP-07, DP-11).

#### 12.3 Events published

None. The platform publishes no `rwb.<short>.events.v1` topic and no event schema (DP-14). A gate result, an export run and a build registration are pipeline and registry state, never a business event, and the v5 event catalogue carries no replay event.

#### 12.4 Events consumed

None. The export reads the Temporal visibility and history API, not a Kafka topic, and the gate reads the Blob index; no other service's event reaches this story.

#### 12.5 Workflows and activities

| Name | Type | Runs on | Purpose |
|---|---|---|---|
| HistoryExportJob | Workflow started by the 01:00 Schedule, one short run per export | `rwb-platform` | Exports the last 200 closed histories per workflow type through the frontend API, checks each payload, writes the file and the index row to Blob and records the export time and last successful run (BR6, BR7) |
| ReplayTestGate | Pipeline step and test base | The pipeline build agent, at the pinned SDK release | Selects the affected types, replays every history with WorkflowReplayer, reports the first mismatch and fails with MSG-P3-038; runs the time-skipping tests against the same branch build (BR1, BR2, BR4, BR7) |
| BuildIdRolloutScript | Script, run from the pipeline and by RW-PLATADM | The `rwb-platform` task queue and the Temporal build ID API | Registers a build as the default, reports the running count per build and refuses a premature retirement (BR8, BR9) |
| exportHistories, validatePayload, writeReplayIndex, recordExportRun | Activities | `rwb-platform` | The four steps of the export: the frontend history read, the payload check, the Blob write and the run record |
| ReplayPayloadCheck | Service called by the export activity | `rwb-platform` | Refuses a history whose payload is not codec-encrypted or holds a clear personal data pattern (BR6) |

No other workflow is started by this story, and no activity of the gate runs on a service task queue: the gate is a pipeline step and an in-process test, and the only `rwb-platform` work is the 01:00 export.

#### 12.6 Schedules

| Schedule | Cadence | Task queue | Legacy reference |
|---|---|---|---|
| HistoryExportJob nightly export | Daily at 01:00, overlap policy SKIP, SIT only | `rwb-platform` | The legacy nightly 01:00 export job, carried by a Temporal Schedule instead of Quartz (DP-10; RWB-TE-007 retired) |

The Schedule is created from the workflow kit template of RWB-PLT-E1071-CON, in namespace `rwb-recovery`, with the tenant and retention of the platform namespace. It is declared in SIT only; UAT and production run no export and hold no replay store. Its catch-up window and overlap policy are configuration, and a missed run is reported as a stale export by the gate, not retried into the next day.

#### 12.7 Tables owned

None. This story owns no `rwb_*` schema, no table and no migration (DP-01, DP-15); the replay files and the index are Blob objects in `rwb-temporal-replay`, the build registry belongs to the Temporal namespace of RWB-PLT-E1070-CON, and the gate result belongs to the pipeline. No table of another service is read.

#### 12.8 Contract fakes

| Fake | Serves | Used by |
|---|---|---|
| Export manifest and index fake (RWB-PLT-E2040-CON) | The index rows, the manifest fields, the export timestamp, the last successful run and the STALE, MISSING and FAILED variants | The export tests of AC8 and the closed-gate tests of AC6 |
| Replay report and gate result fake (RWB-PLT-E2040-CON) | The report shape, the first-mismatch fields, the PASSED and FAILED results and the MSG-P3-038 text | The gate tests of AC1, AC2 and AC5 |
| Build registry fake (RWB-PLT-E2040-CON) | Register, describe and retire with the REGISTERED, CURRENT, DRAINING and RETIRED states and the running count per build | The rollout tests of AC4 and AC7 |
| Reference-data fake (RWB-PLT-E1043-CON with RWB-P3-E1043-CON behind it) | The configuration vocabulary the gate and the export read, with the versioned rows and the C-row contract behind it | Every test that reads a configured value (DP-07, DP-11) |
| Decision-record fake (RWB-PLT-E1027-CON) | The DecisionLogApi write and its failure, so the platform worker template is wired without a live P7 | The export and deprovision tests, and the platform worker start |

The fakes are test-only; they are not deployed into SIT, UAT or production, and no environment value points at one.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 0 | No Workbench operation is provided or consumed; the reference-data contract is reached through the platform client and its fake (DP-07, DP-11) |
| Kafka | 0 | 0 | The platform owns no topic and consumes none; a gate result is not an event (DP-14) |
| Temporal | 1 workflow on a Schedule, 4 activities, and the build ID API for register, describe and retire | 0 | `HistoryExportJob` at 01:00 on `rwb-platform`, namespace `rwb-recovery`; Worker Versioning on Temporal 1.30+ |
| File | 0 read at run time | 0 written | The replay files and the index are Blob objects written by the export and read by the gate; the pipeline step and the rollout script are repository content and read no file at runtime |

### 13. Solution plan

**Package.** The gate, the export workflow, the payload check, the replay store and the report publisher in the platform workflow module, Java package `th.co.scb.ace.workbench.recovery.workflow.replay`; the two test bases in `src/test/java/th/co/scb/ace/workbench/recovery/workflow/replay`; the pipeline step in `.github/workflows/`; the rollout script in `deploy/temporal/rollout/`. The final artifact names and the deployment names of the pipeline identity are Not specified in the source documents (GAP-1449; ASM-2544) and follow the platform template of RWB-PLT-TPL rather than this story.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ReplayTestGate | Test and pipeline step | Selects the affected types, replays every history, reports the first mismatch and fails with MSG-P3-038 (BR1, BR2, BR7) |
| HistoryExportJob | Workflow started by the 01:00 Schedule | SIT only: exports 200 closed histories per type, validates and writes the file and the index (BR6) |
| ReplayPayloadCheck | Service | Refuses a history whose payload is not codec-encrypted or holds a clear personal data pattern (BR6) |
| ReplayHistoryStore | Repository | Writes and lists the replay files and the index rows in the Blob container `rwb-temporal-replay` |
| TestWorkflowEnvironmentBase | Test base | Starts the SDK test environment at the pinned release and applies the shared timeouts and the 10-minute budget |
| TimeSkippingTimerTest | Test | The 30-day timer test and the gate budget check (BR4) |
| BuildIdRolloutScript | Script | Registers a build, reports the running count per build and refuses a premature retirement (BR8, BR9) |
| GateReportPublisher | Service | Attaches the gate result and the replay report to the pull request |

**Database.** No migration and no new table. The replay files and the index live in Blob storage, the build registry lives in Temporal, and the gate result lives in the pipeline, so this story owns no `rwb_*` schema and adds no Flyway sequence (DP-01, DP-15). The export writes no catalogue row: a per-service or per-platform Schedule is declared, not registered in the shared job table (Ownership Map: job_catalog).

**Configuration and reference data**

- 200 histories per workflow type, a 24-hour freshness limit, a 10-minute gate budget and a 90-day replay retention.
- The build ID format `<git-sha>-<build-number>` from RWB-PLT-E1071.
- The list of workflow packages the gate watches: `recovery.casewf.workflow` and every service workflow package published after it, resolved through the naming library of RWB-PLT-E1047-CON rather than from a hard-coded list (DP-14).
- The configuration vocabulary is read through the reference-data client of RWB-PLT-E1043-CON and is never a Java literal (DP-07).
- Feature flag `rwb.p3.temporal` for the worker only; the gate has no flag and cannot be switched off.
- The pinned SDK release, the platform login and the owner of the replay container's retention policy are Not specified in the source documents (GAP-1449; ASM-2544).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

These are the Template and Rules §R5.5 rows the legacy markers call for, in the metadata order, and each of them adds nothing this story does not already depend on. **DP-10** is the substantive row: the legacy `HistoryExportJob` was a Quartz job at 01:00, Quartz is retired with RWB-TE-007, and the export is now a Temporal Schedule on task queue `rwb-platform` whose run is one short workflow with overlap policy SKIP, so the gate needs no scheduler table, no cluster-wide cron and no second job store. **DP-11** is the one hop this story declares: RWB-PLT-E1043-CON is the platform client and RWB-P3-E1043-CON is the owner contract behind it, reached through its fake with a 2 s budget and a breaker, and it is why the C row is a contract and not a table read; no other cross-service call is made, which is why 12.2 lists no runtime operation. **DP-14** keeps the watched package names and every queue name in the naming library, so `recovery.casewf.workflow` today and each service package later are resolved, not typed. **DP-05** applies negatively — the export reads no ACE view and no extension table — and **DP-01** and **DP-15** apply as absences: no `rwb_*` schema is created or read and no migration runs. **DP-03** is declared because the platform worker template wires the local decision-record library, which this story never calls on the gate path; **DP-07** supplies the configured vocabulary; **DP-13** and **DP-19** are why the gate publishes no base and adds no gateway route, because the pull request report is not a Workbench screen.

**Build steps**

1. Build HistoryExportJob on the 01:00 Schedule and ReplayPayloadCheck; test AC8 and the index with 200 synthetic histories.
2. Build ReplayTestGate over WorkflowReplayer and prove it fails on a deliberate non-deterministic change; test AC1.
3. Add a getVersion guard to the test workflow and prove the old histories pass; test AC2.
4. Build TestWorkflowEnvironmentBase and TimeSkippingTimerTest; test AC3 and the 10-minute budget.
5. Build BuildIdRolloutScript with the running count and the refusal, and register it against the build ID API on Temporal 1.30+; test AC4 and AC7.
6. Add the pipeline step, the report and the merge rule; test AC5 and AC6.
7. Add the gate to Engineering Practices, the merge checklist and the pull request template; run the gate on a real pull request in SIT and confirm the Schedule history shows the 01:00 run.

**Done when.** A deliberate non-deterministic change fails gate 10 in SIT, a getVersion change passes, the 30-day timer test completes in under a minute, a build drains and retires with no lost workflow, the Schedule history shows the 01:00 export on task queue `rwb-platform`, and gate 10 is listed in Engineering Practices.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-038 | A workflow change fails the replay test against the recorded histories | The workflow change fails the replay test against recorded histories: {detail}. |

MSG-P3-038 exists in Error and Message Standard v4 and is reused unchanged. `{detail}` names the workflow type, the history ID, the event ID and the first mismatch, and never a payload. The same message is used for a stale export, with `{detail}` naming the export job and its last successful run. The gate report carries the same text; no other message ID is added, and the platform publishes no message of its own because it is not on the Workbench API.

### 15. Screens and states

No Workbench screen in this story, and no gateway-bff route (DP-19). The views are the pipeline gate report on the pull request, with the states PASSED, FAILED and Running, and the build registry in the rollout report, with the states REGISTERED, CURRENT, DRAINING and RETIRED. The reviewer sees the gate result on the pull request and in the merge checklist; RW-AUDIT reads the same result and the export manifest. Running is never a pass: only PASSED unblocks the merge. The platform screens of Epic 8 do not repeat this data.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-040-01 | AC1, BR1, BR2 | Integration | 40 PlatformSmokeWorkflow histories; branch removes the activity call |
| TC-E2-040-02 | AC2, BR3 | Integration | The same 40 histories; getVersion "smoke-step-2" version 2 |
| TC-E2-040-03 | AC3, BR4 | Component | Test workflow with a 30-day timer; 60-second and 10-minute budgets |
| TC-E2-040-04 | AC4, BR8 | Component | Build IDs 9f3c2a1-418 and 7b1d4e0-419; 12 running workflows |
| TC-E2-040-05 | AC5, BR5 | Component | Engineering Practices, merge checklist and pull request template |
| TC-E2-040-06 | AC6, BR7 | Integration | Replay index 36 hours old; branch changes PlatformSmokeWorkflow |
| TC-E2-040-07 | AC7, BR9 | Integration | Build 9f3c2a1-418 with 2 running workflows; retire requested |
| TC-E2-040-08 | AC8, BR6 | Integration | History written with the codec off; clear national ID 1101700203456 |
| TC-E2-040-09 | BR6, section 12.6 nightly export | NFR | Nightly export in SIT writes 200 encrypted histories per type and the index, 90-day retention |
| TC-E2-040-10 | AC4, AC7, BR8, BR9 | Component | Full rollout in SIT: new build takes new workflows, old build drains and retires |

The checks are run by the developer, the reviewer and the platform administrator in SIT and recorded on the pull request and in the release evidence; there is no Workbench endpoint and no Access test in this story. Legacy levels map System to Integration or Component and Operational to Component or NFR as above: the replay and export checks stay Integration because they run against the SIT frontend and the Blob store, the time-skipping, template and rollout checks are Component because they exercise one build artefact, and the nightly export check keeps the NFR level because it measures volume and retention. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the history count, the freshness limit, the time budget, the retention and the build ID format are configuration.
- No personal data in logs, tests, workflow history or prompts: the replay store holds codec-encrypted SIT histories only, and a clear payload is refused (BR6).
- No read of another service's tables and no ACE view: this story reads no case table, no ACE table and no `rwb_*` schema (DP-01, DP-05).
- No production history is exported, and no production data is used in a test or a prompt (NFR-045).
- No workflow change merges without a passing gate 10 result, and no label or flag waives the gate.
- A stale, missing or refused export fails the gate closed; an empty replay set is never a pass.
- No build is retired while it has a running workflow, and no new workflow starts on a draining build.
- No change to the pinned SDK release without the gate run at the new release.
- No Quartz, no scheduler table and no second job store: the export is a Temporal Schedule on task queue `rwb-platform` at 01:00 (DP-10).
- No platform topic, no platform `/api/recovery` base and no `rwb_*` schema: the platform is not one of the 19 services (DP-13, DP-14).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | Epic 2, 3.2; Program, 5.7 | None (platform enabler) | All recovery processes | R-UNI-39 | TC-E2-040-01, TC-E2-040-02, TC-E2-040-03, TC-E2-040-04, TC-E2-040-06, TC-E2-040-08 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E2040-CON | Contract | H: publishes the export manifest and index shape, the replay report shape, the gate result values, the build-registry commands, the error vocabulary and the fakes this story builds against |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library the platform worker template wires; the gate path writes no decision record (DP-03) |
| RWB-PLT-E1043-CON | Contract | H: the platform reference-data client that supplies the configuration vocabulary (DP-07) |
| RWB-PLT-E1071-CON | Contract | H: the worker, the build ID provider, the `<git-sha>-<build-number>` format, the platform worker on task queue `rwb-platform` and the Schedule template the 01:00 export uses (DP-10) |
| RWB-PLT-E1047-CON | Contract | H: the naming library that resolves the watched workflow packages and the queue names (DP-14) |
| RWB-PLT-E1044-CON | Contract | H: the Flyway convention this story deliberately does not use (DP-15) |
| RWB-PLT-N001-CON | Contract | H: gateway-bff; the gate report is not a Workbench route (DP-19) |
| RWB-P3-E1043-CON | Contract | C: the owner contract behind the reference-data read, built against its published fake (DP-07, DP-11) |
| RWB-PLT-E2039-APP, RWB-PLT-E2039-CON | App development, Contract | Siblings of RWB-E2-039: backup, point-in-time restore, zone failover, upgrade and archive; out of scope here, and the archive period is what the replay retention sits under |
| RWB-PLT-N003-INF | Infrastructure | Sibling: the namespace `rwb-recovery` and the codec key this story's SIT histories depend on |
| RWB-PLT-NF08-INF | Infrastructure | Sibling: the platform baseline (cluster, ingress, monitoring) the export and the gate run on |

### 19. Out of scope

- The Temporal cluster, namespace, mTLS, Web UI and platform dashboard (legacy RWB-E1-070; RWB-PLT-E1070-APP).
- The worker, the codec, the gateway and the smoke workflow (legacy RWB-E1-071; RWB-PLT-E1071-APP), and the JOB-22 smoke Schedule.
- The codec server, decode and the administrative audit (legacy RWB-E2-038; RWB-PLT-E2038-APP, RWB-PLT-E2038-CON).
- Alerts, the stuck scanner and the workflow dashboard (legacy RWB-E2-037; RWB-PLT-E2037-APP, RWB-PLT-E2037-CON).
- Backup, point-in-time restore, zone failover, upgrade and archive (legacy RWB-E2-039; RWB-PLT-E2039-APP, RWB-PLT-E2039-CON).
- The namespace `rwb-recovery` and the codec key (RWB-PLT-N003-INF), and the platform baseline (RWB-PLT-NF08-INF).
- Case workflow code and the reference skeleton (Epic 3, legacy RWB-E2-043).
- The other nine pipeline checks and the release gates (Recovery Workbench Engineering Practices).
- Load, performance and soak testing of workflow executions (legacy RWB-E1-056, Epic 3).
- Production history export and replay against production data.
- The contract documents and the fakes themselves: RWB-PLT-E2040-CON.
