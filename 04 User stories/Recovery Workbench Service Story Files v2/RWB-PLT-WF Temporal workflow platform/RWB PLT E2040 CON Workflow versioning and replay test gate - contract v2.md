# RWB-PLT-E2040-CON Workflow versioning and replay test gate - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-E2040-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-WF |
| Wave | 0 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-040 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Set by the squad at refinement |
| Patterns applied | DP01, DP03, DP05, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | CG-W0 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | v1, pinned (AC8) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-014, FR-PLT-015) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-040 for the workflow platform epic; the replay history index, the gate report, the build-ID registry, the time-skipping test rule, the fail-closed rule and the error vocabulary are published on Day 1 with three fakes. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (7 resolved, 13 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **consumer of the versioning and replay-gate contract** (the pipeline, the platform administrators, the developers of the workflow types under test and the release manager), I want **the replay history index, the gate report, the build-ID registry, the time-skipping test rule, the fail-closed rule and the error vocabulary published on Day 1 with fakes**, so that **the gate, the replay store and the rollout are built and tested against one frozen set instead of three private readings**.

This is the contract story of legacy key RWB-E2-040 under epic RWB-PLT-WF. It publishes, on Day 1 with fakes, the contract of the gate that stops a workflow change which would strand a case already in flight:

- The replay history index contract: workflow type, history ID, workflow ID, run ID, export time, build ID, path, payload-check status and retention.
- The gate report contract: PASSED or FAILED, the replay set size, the first mismatch as workflow type, history ID, event ID and event type, the gate budget and the MSG-P3-038 text with its {detail} fields — never a payload.
- The build-ID registry contract: REGISTERED, CURRENT, DRAINING and RETIRED, the default per task queue, the running count and the refusal rule.
- The time-skipping test contract: the timer under test, the simulated elapsed time and the wall-clock budget.
- The fail-closed rule: a missing, stale, refused or empty replay set never passes.
- The error vocabulary of section 14.
- Three fakes — a replay history store and index, a build registry and a gate report — plus a contract test, so the pipeline, the replay store and the rollout are built with no SIT namespace and no long wait for a real history.

The workflow platform is **shared platform**, not one of the 19 services: Template and Rules §R4 has no platform row, so this document declares no `rwb_*` schema, no `rwb.<short>.events.v1` topic and no `/api/recovery/<short>/v1` base (DP-01, DP-13, DP-14). What it publishes is a document set, a fake set and one vocabulary. The namespace `rwb-recovery` and the task queue `rwb-platform` are fixed by RWB-PLT-E1070-CON and RWB-PLT-E1071-CON and are recorded here, not redefined.

Four values the contract depends on are named by no read source: the pipeline identity that runs the gate, the replay container retention, the pinned SDK version the contract is fixed at, and the owner of the build registry — Not specified in the source documents (GAP-1450; ASM-2545). They are published as the working read of that assumption and stay open.

The contract is published at status Draft (realignment v1) and is frozen when RWB-PLT-E2040-APP and the pipeline integration pass their contract tests.

### 2. Business rationale

Temporal replays workflow code from history after any restart, so workflow code has to be deterministic: no database call, no system clock, no random, no Drools and no network — all of that goes into activities, whose results are recorded (Temporal and Drools design slide 27). A change in the order of commands therefore does not fail a unit test; it fails a worker picking up a running case, in production, hours after the release. Epic 3 changes case workflows release after release while cases are open, so the gate that catches this has to exist before the first case workflow is written, and it has to exist as a contract, because three parties write against it at once: the pipeline that runs the gate, the platform team that owns the replay store, and every developer whose change is replayed.

In the monolith the three parties were one team and one build, so the export format, the report and the rollout were conventions nobody had to write down. In the target the gate is a pipeline step, the histories come from a SIT namespace owned by the platform team, the registry is the cluster's own build-ID API, and the consumers are developers of services in four waves (Architecture v5 slides 11, 20 and 23). Nothing in that chain forces the three artefacts to agree unless a contract does.

The contract fixes four things before any code. First, the replay history index: one row per exported history with its build ID, export time and payload-check status, so freshness and provenance are decidable and a stale export can be refused rather than quietly replayed. Second, the gate report: PASSED or FAILED, the replay set size and the first mismatch, so a failure names the workflow type, the history ID, the event ID and the event type instead of reporting a stack trace, and so MSG-P3-038 carries {detail} and never a payload. Third, the build-ID registry: four states, the default per task queue and the running count, so a rollout drains and retires a build without losing a workflow, and the retire request is refused while a workflow still runs. Fourth, the fail-closed rule: a missing, stale, refused or empty replay set never passes, because an empty set is exactly what a broken export produces and exactly what a pass would hide.

This meets REQ-DRI-005 (a replay that reaches the same decisions proves the recorded decision path still matches the code, and a change that would make a recorded decision unreproducible is refused before it reaches a case), ADR-011 (workflow kit plus stage children, which is what makes versioning necessary at all) and ADR-020 (the contract and its fake come before code). The measure is that no workflow change merges without a gate result, that no build is retired with a running workflow, and that every contract test answers from the three fakes on Day 1.

### 3. Preconditions

- RWB-PLT-E1070-CON is published: the namespace `rwb-recovery`, one cluster per environment at version 1.30 or later for Worker Versioning, its persistence database and its mTLS identities.
- RWB-PLT-E1071-CON is published: the platform worker on the task queue `rwb-platform`, the WorkflowGateway interface, the smoke workflow and the build ID format `<git-sha>-<build-number>` this document quotes unchanged.
- RWB-PLT-N010-CON is published: the workflow kit interface and the rule that a kit change is a version change, so a replayed history of a kit template can be attributed to a kit version.
- The reference-data contract of RWB-PLT-E1043-CON exists, so the state and outcome codes of sections 9 and 12.5 are versioned values and never literals in a document or a rule (DP-07).
- The legacy values are carried from RWB-E2-040: the SIT namespace holds histories for the workflow types under test, 200 closed histories per workflow type, a 24-hour freshness limit, a 10-minute gate budget, a 90-day replay retention, the 30-day timer and the 60-second wall-clock bound of the time-skipping test.
- No production history is exported and no production data is used in a test or a prompt (NFR-045); the replay store holds codec-encrypted SIT histories only.
- Recovery Workbench Engineering Practices lists the pipeline checks; this story adds gate 10 to that list as a contract obligation of RWB-PLT-E2040-APP (legacy RWB-E2-040 AC5, BR5).
- The gate carries no feature flag and cannot be switched off; with no workflow running, the export finds no history and the gate fails closed (legacy RWB-E2-040 section 13).
- The pipeline identity, the replay container retention, the pinned SDK version and the owner of the build registry are named by no read source: Not specified in the source documents (GAP-1450; ASM-2545). The contract publishes the working read of the assumption: namespace `rwb-recovery`, task queue `rwb-platform`, SIT-only histories, 200 per type, 24-hour freshness, 10-minute budget, 90-day retention, gate 10 and MSG-P3-038 unchanged.
- The contract is Draft (realignment v1) until RWB-PLT-E2040-APP and the pipeline integration pass; no approval is required to publish a Draft contract.

### 4. Flow

1. The contract author writes `replay-gate.yaml`: the replay history index with its nine fields, the replay set selection (the newest 200 rows per workflow type, the 24-hour freshness rule and the payload-check rule), the time-skipping test contract and the fail-closed rule.
2. The author writes `build-registry.yaml`: the four states, the rule that exactly one build is CURRENT per task queue, the running count per build and the refusal rule of a retire request.
3. The author writes `gate-report.yaml`: the outcome PASSED or FAILED, the replay set size, the first mismatch as workflow type, history ID, event ID and event type, the gate budget, the wall-clock time and the MSG-P3-038 text with its {detail} fields.
4. The author writes the field list of an index row and the rule that a row holds no payload, no workflow input and no personal data field, and that a row whose payload check is FAILED leaves no history file in the store.
5. The author writes the error vocabulary of section 14: MSG-P3-038 reused unchanged, and the reserved PLT-REPLAY identifiers for the refusal, the payload check, the unavailable store and the budget overrun.
6. The three fakes are generated from the documents: the fake replay history store and index, the fake build registry and the fake gate report, each answering every example the documents publish.
7. The lint rules run over the three documents: no schema name, no topic name and no service base in any field or path; every index row field typed; every state and every outcome from the reference-data code set; the MSG-P3-038 text present once and only once.
8. The contract test runs the fakes against the documents on every change: a field, a state, a status or a placeholder that drifts fails the build.
9. The documents and the fakes are published as v1 to the contract registry; RWB-PLT-E2040-APP and the pipeline integration pin v1, and the contract is frozen when both pass.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A document declares an `rwb_*` schema, a topic or a `/api/recovery/<short>/v1` base, or a field carries a payload or a personal data field | The lint step fails the build and the version is not published | Lint finding, no message id | AC1 |
| X2 | An index row has no build ID, no export time or no payload-check status, or its export time is not the newest of its type | The contract test fails naming the field and the row; freshness is never inferred from a file | Lint finding, no message id | AC2 |
| X3 | A document lets an empty, missing, stale or refused replay set be reported as PASSED | The fail-closed rule is a single declaration in `replay-gate.yaml`; the contract test fails if any example or fake reports PASSED for such a set | Lint finding, no message id | AC6 |
| X4 | A retire request on a build with a running count above zero is reported as accepted anywhere in the documents or a fake | The contract test fails; the registry answers the refusal and names the workflow IDs, and the build stays DRAINING | PLT-REPLAY-409 placeholder of section 14 | AC4 |
| X5 | A change breaks a consumer: a renamed field, a removed state, a changed outcome value or a changed {detail} field set | v1 is not edited; the change raises v2, v1 is deprecated, and no consumer sees an edited v1 | Lint finding, no message id | AC8 |
| X6 | A value the consumers need is named by no read source: the pipeline identity, the replay container retention, the pinned SDK version and the owner of the build registry | The value is published as the working read of the assumption, with the placeholder where it is still open, and the gap stays open | Not specified in the source documents (GAP-1450; ASM-2545) | None; GAP-1450 and ASM-2545 stay open |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes three documents and three fakes; builds no gate and no job, reads no business data and depends on nothing after Day 1 |
| Negotiable | Field order inside a model, example timestamps, the fake's transport and the internal file layout are open until the version is frozen; the nine index fields, the four build states, PASSED and FAILED, the fail-closed rule and the MSG-P3-038 placeholder set are fixed |
| Valuable | The pipeline step, the replay store, the export job and the rollout start on Day 1 against one frozen set and three fakes, so a developer never has to read another team's code to know what a gate result looks like |
| Estimable | Three documents, three fakes, one contract test and one lint set |
| Small | One sprint for the documents, the fakes and the lint rules |
| Testable | Each criterion in section 7 is a schema, lint or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Workflow versioning and replay test gate - contract

  Background:
    Given the platform is shared platform and publishes no schema, no topic and no Workbench REST base
    Given the replay gate serves the workflows of namespace rwb-recovery on the task queue `rwb-platform`

  Scenario: AC1 The three contract documents are published, validated and linted (new, D-RCV-60)
    Given the replay gate contract tree holding replay-gate.yaml, build-registry.yaml and gate-report.yaml
    When each document is validated against its schema and linted
    Then replay-gate.yaml declares the replay history index, the replay set selection, the time-skipping test contract and the fail-closed rule
    Then build-registry.yaml declares the four build states, the default per task queue and the running count
    Then gate-report.yaml declares PASSED and FAILED, the replay set size, the first mismatch fields, the gate budget and the MSG-P3-038 text
    Then no document declares an rwb_* schema, a rwb.<short>.events.v1 topic or a /api/recovery/<short>/v1 base, and the lint step fails the build if one appears

  Scenario: AC2 The replay history index contract declares one row per exported history (new, D-RCV-60)
    Given the replay history index of replay-gate.yaml
    When an index row is validated
    Then the row declares the workflow type, history ID, workflow ID, run ID, export time, build ID, path, payload-check status and retention
    Then the payload-check status has the values PASSED and FAILED, and a FAILED row leaves no history file in the store
    Then the build ID has the format <git-sha>-<build-number>
    Then the export time of the newest row of a type decides freshness, and the retention is 90 days
    Then no row, example or file name holds a payload, a workflow input or a personal data field

  Scenario: AC3 The gate report contract declares the outcome, the replay set size and the first mismatch (new, D-RCV-60)
    Given the gate report of gate-report.yaml
    When a report is validated
    Then it declares PASSED or FAILED, the replay set size, the gate budget and the wall-clock time of the run
    Then a FAILED report declares the first mismatch as the workflow type, the history ID, the event ID and the event type
    Then a FAILED report carries MSG-P3-038 with the {detail} fields set to the workflow type, the history ID, the event ID and the first mismatch
    Then no report, example or log carries a payload, a workflow input or a clear personal data value
    Then the same text is produced for a stale export, with {detail} naming the export job and its last successful run

  Scenario: AC4 The build-ID registry contract declares the four states, the default per task queue and the running count (new, D-RCV-60)
    Given the build-ID registry contract
    When a build is registered, made current, drained and retired
    Then the states are REGISTERED, CURRENT, DRAINING and RETIRED, and exactly one build is CURRENT per task queue
    Then a workflow started after the deploy runs on the CURRENT build and a running workflow stays on the build it started on
    Then the registry answers the running count per build, and a build with a running workflow stays DRAINING
    Then a retire request on a build whose running count is above zero is refused and names the workflow IDs, and the same request succeeds at zero
    Then registering the same build ID twice changes nothing

  Scenario: AC5 The time-skipping test contract declares the timer, the simulated elapsed time and the wall-clock budget (new, D-RCV-60)
    Given the time-skipping test contract of replay-gate.yaml
    When the test workflow that waits on a 30-day timer runs
    Then the contract declares the timer under test, the simulated elapsed time the test reports and the wall-clock budget of 60 seconds
    Then a test over its wall-clock budget is reported as failed and never as passed
    Then the gate run stays inside its 10-minute budget and an overrun is reported as FAILED
    Then the test runs in the SDK test environment only and reads no SIT history

  Scenario: AC6 A missing, stale, refused or empty replay set never passes (new, D-RCV-60)
    Given a replay set for a workflow type
    When the newest export is missing, more than 24 hours old, carries a FAILED payload-check status, or the set is empty
    Then the contract declares that the gate reports FAILED and runs no replay
    Then the report names the export job and its last successful run in the {detail} of MSG-P3-038
    Then no such run is ever reported as PASSED, and a re-run after a fresh export (at most 24 hours old, payload-check status PASSED) is reported as PASSED
    Then the gate has no flag and no switch that turns this rule off

  Scenario: AC7 The three fakes answer every example of the contract (new, D-RCV-60)
    Given the fake replay history store and index, the fake build registry and the fake gate report, generated from the documents
    When the contract test runs on every change
    Then the fake store answers an index row for every declared field, a FAILED payload-check row and an empty set
    Then the fake registry answers all four states, the default per task queue, the running count and the refused retirement with the workflow IDs
    Then the fake gate report answers PASSED, FAILED with the first mismatch, the budget overrun and the stale-export text
    Then a field, a state, a status or a placeholder that drifts between a document and a fake fails the build

  Scenario: AC8 A breaking change raises v2 and v1 is never edited (new, D-RCV-60)
    Given v1 of the three documents, pinned by RWB-PLT-E2040-APP and the pipeline integration
    When a field, a state, an outcome value or the MSG-P3-038 placeholder set is changed
    Then the change is published as v2 and v1 is marked deprecated and stays pinnable
    Then an additive field with a default raises the minor number and no consumer sees an edited v1
    Then the contract test fails against v1 for the breaking change and passes against v2

  Scenario: AC9 Each business rule of section 8 is covered by a criterion and a test case (new, D-RCV-60)
    Given the business rules BR1 to BR8 of section 8
    When the criteria of this story are checked against section 8
    Then BR1 and BR2 are met by the gate report of AC3, which fails the merge on a non-deterministic change
    Then BR3 and BR8 are met by the build-ID registry of AC4
    Then BR4 is met by the time-skipping test contract of AC5
    Then BR5 is met by the gate 10 entry that carries the MSG-P3-038 text declared in AC1
    Then BR6 and BR7 are met by the replay history index of AC2 and the fail-closed rule of AC6

  Scenario: AC10 A retried or timed-out activity whose event does not match the history is never reported as PASSED (new, D-RCV-60)
    Given a replayed workflow whose activity is retried or times out in the recorded history
    When the gate replays the history of that workflow
    Then an activity event that does not match the recorded history is reported as the first mismatch of AC3 with outcome FAILED
    Then the gate budget of AC5 still applies, and an overrun is reported as FAILED
```

The ten criteria are new and test only the published contract and its fakes: no legacy acceptance criterion is repeated here, and every value in an example comes from RWB-E2-040 character for character or is left out.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Workflow code is deterministic, and every change is replayed against the recorded histories of the affected workflow types before merge; a replay that reaches the same decisions proves the recorded decision path still matches the code | Legacy RWB-E2-040 section 8 BR1; ADR-011; Temporal and Drools design slide 27 |
| BR2 | A non-deterministic change fails gate 10 with MSG-P3-038 and blocks the merge; no label, flag, role or review waives the gate | Legacy RWB-E2-040 section 8 BR2; ADR-020 |
| BR3 | A behaviour change is guarded with Workflow.getVersion: an old history takes the old path and a new execution takes the new one, and the guarded version is part of the replay result | Legacy RWB-E2-040 section 8 BR3; Temporal and Drools design slide 27 |
| BR4 | Time-skipping tests run every timer in the changed workflow; a 30-day timer completes inside the 60-second wall-clock budget, and a gate run over its 10-minute budget is reported as FAILED | Legacy RWB-E2-040 section 8 BR4 |
| BR5 | Gate 10, "Workflow replay and time-skipping tests", is listed in Recovery Workbench Engineering Practices with its owner, its pass rule, its budget and its failure message MSG-P3-038, and is part of the merge checklist and the pull request template | Legacy RWB-E2-040 section 8 BR5 |
| BR6 | Replay histories come from SIT only, are codec-encrypted, are kept 90 days and hold no clear personal data; a history that fails the payload check is not used and is not written to the store | NFR-045; Legacy RWB-E2-040 section 8 BR6 |
| BR7 | The gate fails closed when the export is missing, stale by more than 24 hours, refused or empty; it never passes on an empty set, and no configuration turns the rule off | Legacy RWB-E2-040 section 8 BR7 |
| BR8 | Workers register a build ID; a new workflow starts on the CURRENT build of its task queue, a running workflow stays on the build it started on, and a build is retired only when its running count is zero | Legacy RWB-E2-040 sections 8 BR8 and BR9; RWB-PLT-E1071-CON |

### 9. State transitions

The contract has its own lifecycle; the objects it describes have the states of the registry and of the gate report. This story changes no case status.

| Object | State | Meaning in this contract |
|---|---|---|
| Contract document | Draft | Published (realignment v1) and open to comment |
| Contract document | Published | v1 in the contract registry, the three fakes generated from it, consumers pinning it |
| Contract document | Frozen | RWB-PLT-E2040-APP and the pipeline integration have passed; a change now raises v2 |
| Contract document | Deprecated | A v2 exists; v1 is read-only and still answered by its fake |
| Build in the registry | REGISTERED | The build ID is known to the task queue and takes no new workflow |
| Build in the registry | CURRENT | The newest default of its task queue; new workflows start here |
| Build in the registry | DRAINING | A newer build is CURRENT; the running workflows finish here and no new one starts |
| Build in the registry | RETIRED | The running count is zero; the workers are down and the build is not started again |
| Gate report | PASSED | Every history replayed and every time-skipping test passed inside the budget; the merge may proceed |
| Gate report | FAILED | A mismatch, a stale export, a refused set or a budget overrun; the merge is blocked |

| Object | From | Event | To |
|---|---|---|---|
| Build | None | Deploy and register after a passed gate | REGISTERED |
| Build | REGISTERED | Register as the default of the task queue as the newest build | CURRENT; the previous build becomes DRAINING |
| Build | DRAINING | The last running workflow closes | RETIRED |
| Build | DRAINING | Retire requested while a workflow runs | DRAINING, refused with the workflow IDs |
| Gate report | None | A history mismatches, the export is stale or refused, or the set is empty | FAILED; the merge is blocked |
| Gate report | None | Every history replays and every test passes inside the budget | PASSED; the merge may proceed |

The build states and the gate outcomes are values of the reference-data code set (DP-07) and the fake answers them; this contract owns the document states and the vocabulary only.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the three documents, the error vocabulary, the fakes and the contract test |
| The platform owner of the workflow layer | Owns the version rule, approves a breaking change and a freeze, and owns the build registry |
| The pipeline owner | Confirms the gate budget, the report fields and the merge rule the contract states |
| Security architecture | Confirms that the replay store holds SIT histories only, codec-encrypted, with no clear personal data |
| The rwb-case owner (P3) | Confirms the state and outcome codes as reference data and the LOV entries they come from |
| RW-PLATADM, RW-AUDIT, RW-COE | Read the contract and the gate result; raise a change request rather than a private variant |
| RW-SECADM | Receives the payload-check refusal of a history; decode stays with RWB-PLT-E2038-CON |
| No delegation of authority level applies | A replay-gate contract is a technical artefact, not a credit decision |

No personal name, no email address and no credential appears in a document, an index row, a report or a fake. Where a caller must be named, the example uses a role code, a workflow identifier or a service identity only, and the store names the export job rather than the person who ran it.

### 11. Data

| Item | Value | BR Field ID |
|---|---|---|
| Business data published | None. The documents publish field names, state names, outcome values, thresholds and message placeholders; no customer, account, case or document value appears | Not specified in the source documents (DOR-RWB-PLT-E2040-CON-7) |
| Identifiers in the examples | Synthetic only: the workflow type PlatformSmokeWorkflow and the test-only workflow type of the replay corpus, the synthetic build IDs and the synthetic export timestamps of the examples | Not specified in the source documents (DOR-RWB-PLT-E2040-CON-7) |
| Personal data | None, and none is admitted: a replay history is codec-encrypted and never republished by this contract, and no index row, report, example or fake holds a person field, a national identifier or an account number | Not specified in the source documents (DOR-RWB-PLT-E2040-CON-7) |
| Payload content | None published. A report names the history ID and the event ID of a mismatch and never the event payload | Not specified in the source documents (DOR-RWB-PLT-E2040-CON-7) |
| Tables published | None. This document declares no table, no column and no migration; the index lives in Blob storage and the registry is the Temporal build-ID API | Not specified in the source documents (DOR-RWB-PLT-E2040-CON-7) |
| Retention | None at the contract: a document keeps no data and the fakes hold only the examples they publish. The replay store's own retention is 90 days and its owner is named by no read source (GAP-1450; ASM-2545) | Not specified in the source documents (DOR-RWB-PLT-E2040-CON-7) |

### 12. Contract

#### 12.1 REST operations provided

None. The platform has no service short (Template and Rules §R4 has no platform row), so the contract publishes no path under `/api/recovery/<short>/v1` and no Workbench endpoint (DP-13). What it publishes is a document set, a fake set and one error vocabulary. The gate report reaches a reviewer as a pipeline artefact of RWB-PLT-E2040-APP and the registry answers over the Temporal API, not over HTTP of the Workbench.

#### 12.2 REST operations consumed

None. The contract consumes no Workbench operation. The reference-data read behind the state and outcome codes is a C row of its consumer (RWB-P3-E1043-CON, one hop, 2 s budget, DP-11) and is recorded in the app story, not here.

#### 12.3 Events published

None. The platform publishes no `rwb.<short>.events.v1` topic and no event schema (DP-14); a gate result is a pipeline artefact and a build state is a cluster state, and neither becomes an event of a service.

#### 12.4 Events consumed

None. The gate consumes no Kafka topic: it reads the replay history store and the build registry, and it is started by the pipeline rather than by an event.

#### 12.5 Workflows and activities

None owned. The contract declares four interfaces and no workflow, no activity and no queue entry of its own:

| Model | Fields |
|---|---|
| Replay history index row | workflowType, historyId, workflowId, runId, exportTime, buildId, path, payloadCheck (PASSED or FAILED), retentionDays; the row holds no payload and no workflow input |
| Replay set selection | workflowType, the newest 200 index rows of the type, the freshness rule of 24 hours against the newest exportTime, and the rule that only a PASSED payload check is selected |
| Gate report | outcome (PASSED or FAILED), replaySetSize, firstMismatch { workflowType, historyId, eventId, eventType }, gateBudget, wallClock, messageId with message text; on FAILED the firstMismatch and the MSG-P3-038 text with its {detail} fields |
| Build registry answers | taskQueue, buildId, state (REGISTERED, CURRENT, DRAINING or RETIRED), runningCount, and the refusal answer naming the workflow IDs; at most one CURRENT build per task queue |
| Time-skipping test result | test name, timer under test, simulatedElapsed, wallClock, budget; a result over the budget is failed |

The read side of the model is the history read of the Temporal frontend on namespace `rwb-recovery` and the write side is the build-ID compatibility call on the task queue `rwb-platform`, both over mTLS; the contract fixes the fields and the answers, and the transports are RWB-PLT-E1070-CON's and RWB-PLT-E1071-CON's (DP-11, DP-10). The pipeline identity that runs the gate and the pinned SDK version the corpus is replayed at are named by no read source (GAP-1450; ASM-2545) and are published as the working read of the assumption.

#### 12.6 Schedules

None owned by this contract. The 01:00 export of the day's histories is the app story's Schedule (RWB-PLT-E2040-APP section 12.6) on the task queue `rwb-platform` with overlap policy SKIP; this contract fixes the freshness rule, the row it writes and the fail-closed answer, and registers no Schedule and owns no batch window (DP-10).

#### 12.7 Tables owned

None. The contract owns no `rwb_*` schema and no table (DP-01, DP-15): the index and the history files live in Blob storage, the registry is the Temporal build-ID API, and neither a migration nor a Flyway sequence of this story runs.

#### 12.8 Contract fakes

| Fake | Serves | Used by |
|---|---|---|
| Fake replay history store and index (this story) | An index row for every declared field, a PASSED and a FAILED payload-check row, an empty set, a set older than 24 hours and a history file path per row | RWB-PLT-E2040-APP, the pipeline integration, TC-PLT-E2040-CON-02 and TC-PLT-E2040-CON-06 |
| Fake build registry (this story) | The four states, the default per task queue, the running count per build, the refused retirement with the workflow IDs and the duplicate registration | RWB-PLT-E2040-APP, the rollout of the app story, TC-PLT-E2040-CON-04 |
| Fake gate report (this story) | PASSED, FAILED with the first mismatch, the budget overrun and the stale-export text with the MSG-P3-038 {detail} fields | RWB-PLT-E2040-APP, the pipeline integration, TC-PLT-E2040-CON-03, TC-PLT-E2040-CON-05 and TC-PLT-E2040-CON-08 |
| Workflow-kit fake (RWB-PLT-N010-CON) | The eight template interfaces with deterministic replay, so a replayed history of a kit template is answered without the kit library | The replay examples of TC-PLT-E2040-CON-07 |
| Fake worker and gateway (RWB-PLT-E1071-CON) | The WorkflowGateway start and signal, PlatformSmokeWorkflow and the build ID it returns | The history selection and the build ID examples of TC-PLT-E2040-CON-02 and TC-PLT-E2040-CON-04 |
| Reference-data fake (RWB-P3-E1043-CON) | The state codes REGISTERED, CURRENT, DRAINING and RETIRED and the outcome codes PASSED and FAILED as versioned values | The state and outcome assertions of TC-PLT-E2040-CON-04 and TC-PLT-E2040-CON-07 |

The three own fakes answer from the documents of this section and of sections 7 and 13, and read the state and outcome codes from the reference-data fake rather than from copied literals, so a change to a code or to a field shows up as a contract-test failure. They are test-only and are never deployed to SIT, UAT or PROD.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 0 | The contract is a document set and a fake set; the platform publishes no Workbench base |
| Kafka | 0 | 0 | No topic and no event schema; a gate result is not an event |
| Temporal | 2 contracts: the history read on namespace `rwb-recovery` and the build-ID registry on the task queue `rwb-platform` | 0 | mTLS only; the contract fixes the fields and the answers, and RWB-PLT-E1070-CON and RWB-PLT-E1071-CON own the transports |
| File | 2 contracts: the replay history store and index in Blob storage, and the gate report artefact of the pipeline | 0 | No service reads either at runtime; no file is committed with a payload |

### 13. Solution plan

**Deliverables.**

| Deliverable | Form | Content |
|---|---|---|
| `replay-gate.yaml` | Versioned document plus schema | The replay history index with its nine fields, the replay set selection, the 24-hour freshness rule, the payload-check rule, the time-skipping test contract and the fail-closed rule |
| `build-registry.yaml` | Versioned document plus schema | The four states, the one-CURRENT rule per task queue, the running count, the refusal answer and the duplicate registration rule |
| `gate-report.yaml` | Versioned document plus schema | PASSED and FAILED, the replay set size, the first mismatch fields, the gate budget, the wall-clock time and the MSG-P3-038 text with its {detail} fields |
| Fake generation | Test-only runnable set | The fake replay history store and index, the fake build registry and the fake gate report, generated from the three documents |
| Lint rules | Rules in the build | No schema, topic or service base in a field or a path; every index field typed; every state and outcome from the reference-data code set; the MSG-P3-038 text once and only once; a payload scan over every example |
| Contract test | Test suite in the build | Every field, state, outcome, refusal and message asserted against the fakes on every change |

**Pattern application**

| DP code | legacy marker | microservice pattern | dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none: the index is a Blob object and the registry is cluster state, so the contract reads no table of any service |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON for the app story: the gate records no decision of its own and the replayed workflow writes its records through the library |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none: the contract reads no ACE data and no `v_ace_*` view |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON: the four build states and the two outcomes are versioned codes |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON for the app story: the legacy nightly Quartz export becomes a Schedule on the task queue `rwb-platform` and the contract declares its cadence and freshness rule |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none added by this story: the legacy in-process call into the SDK test kit and the replay classes becomes a typed contract with a fake and a budget |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none: the platform has no base and this document declares none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON for the app story; the contract publishes no topic of its own |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON for the app story; this story runs no migration |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON for the app story; this contract adds no screen and no route |

These are the Template and Rules §R5.5 rows that bear on this contract. DP-11 and DP-10 are the two rows the document is about: DP-11 because the legacy gate called the replay classes in process, so the same classes in a shared build could drift with the pipeline that used them, and the contract replaces that with a typed index row and report answered by a fake; DP-10 because the legacy export was a Quartz job in the monolith and becomes a Schedule on the task queue `rwb-platform`, with the freshness rule in the contract and the Schedule itself in the app story. DP-07 keeps the four build states and the two outcomes as reference-data codes, so a new state is a value and not a document version. DP-01, DP-03, DP-05, DP-13, DP-14, DP-15 and DP-19 are declared as absences with the dependency each would carry for a consumer: the gate reads no `rwb_*` table and no ACE view, writes no decision record, publishes no service base and no topic, runs no migration and composes no Workbench screen. This story adds no dependency of its own: it is a CON story, starts on Day 1 and is frozen when its consumers pass.

**Build steps**

1. Write `replay-gate.yaml` with the nine index fields, the replay set selection, the 24-hour freshness rule, the payload-check rule, the time-skipping test contract and the fail-closed rule.
2. Write `build-registry.yaml` with the four states, the one-CURRENT rule per task queue, the running count and the refusal rule with the workflow IDs.
3. Write `gate-report.yaml` with PASSED and FAILED, the replay set size, the first mismatch fields, the 10-minute gate budget, the wall-clock time and the MSG-P3-038 text with its {detail} fields.
4. Write the error and idempotency sections: MSG-P3-038 reused unchanged, the four reserved PLT-REPLAY identifiers, and the rules that a repeated registration changes nothing and a re-run on the same commit gives the same result.
5. Add the lint rules: no schema name, no topic name, no service base, every field typed, every state and outcome from the reference-data code set, the no-payload scan and the single MSG-P3-038 text.
6. Generate the three fakes over the kit fake, the worker fake and the reference-data fake, write the contract test, and publish v1 to the contract registry with the version the consumers pin.

**Done when.** The three documents validate, every lint rule passes, the three fakes answer every example of sections 7, 12 and 14 including the FAILED payload check, the empty set, the refused retirement and the budget overrun, and the contract test is green on the build of this story.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-P3-038 | A workflow change fails the replay test against the recorded histories, or the export is missing, stale or refused | The workflow change fails the replay test against recorded histories: {detail}. | Gate report, reused unchanged; {detail} names the workflow type, the history ID, the event ID and the first mismatch, or the export job and its last successful run, and never a payload |
| PLT-REPLAY-409 | A retire request names a build whose running count is above zero | Not specified in the source documents (GAP-1450; ASM-2545) | Build registry refusal, reserved; the answer names the workflow IDs and the build stays DRAINING |
| PLT-REPLAY-422 | An index row or an exported history fails the schema, or its payload check is FAILED | Not specified in the source documents (GAP-1450; ASM-2545) | Replay store refusal, reserved; no file is written for that row |
| PLT-REPLAY-503 | The replay history store or the build registry does not answer, so the gate cannot run | Not specified in the source documents (GAP-1450; ASM-2545) | Gate report, reserved; the run is FAILED and no replay is claimed |
| PLT-REPLAY-504 | A gate run passes its 10-minute budget | Not specified in the source documents (GAP-1450; ASM-2545) | Gate report, reserved; the run is FAILED and the wall-clock time is reported |

MSG-P3-038 is the only business message this contract publishes, and it publishes it unchanged from RWB-E2-040 and the message catalogue: the text is quoted as it stands, its {detail} names the workflow type, the history ID, the event ID and the first mismatch, the same text serves a stale export with {detail} naming the export job and its last successful run, and no payload and no personal data enters it. The four PLT-REPLAY identifiers are reserved for this contract and carry no business value; where the message catalogue has no entry their text is the placeholder above, and when the catalogue gains platform replay entries they replace the placeholder and no other value changes.

### 15. Screens and states

No screen in this story, and the contract declares none: the gate report is a pipeline artefact on the pull request and the build registry is read in the rollout report, and both belong to RWB-PLT-E2040-APP. No route is added to the gateway (DP-19). What this contract fixes is the vocabulary a person reads there — PASSED and FAILED with the first mismatch, and REGISTERED, CURRENT, DRAINING and RETIRED with the running count — together with the four document states of section 9, so the pipeline, the rollout and the review share one set of words. The platform screens of Epic 8 and the admin console do not repeat this data.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-E2040-CON-01 | AC1 | Contract | The three documents validated and linted: no schema, topic or service base; every section declared; the MSG-P3-038 text once |
| TC-PLT-E2040-CON-02 | AC2 | Contract | The index row with its nine fields; a PASSED and a FAILED payload-check row; the build ID format `<git-sha>-<build-number>`; 200 rows per type; 24-hour freshness; 90-day retention |
| TC-PLT-E2040-CON-03 | AC3 | Contract | The report fields; PASSED and FAILED; the first mismatch at event ID 4 of event type ActivityTaskScheduled; MSG-P3-038 with its {detail} fields; the no-payload scan |
| TC-PLT-E2040-CON-04 | AC4 | Component | Build IDs 9f3c2a1-418 and 7b1d4e0-419; 12 running workflows draining; 2 running workflows refused; retirement at zero; a duplicate registration |
| TC-PLT-E2040-CON-05 | AC5 | Contract | The 30-day timer; the simulated elapsed time of 30 days; the 60-second wall-clock budget; the 10-minute gate budget and the overrun |
| TC-PLT-E2040-CON-06 | AC6 | Contract | A missing export; an export 36 hours old; a FAILED payload check; an empty set; the same run never reported as PASSED |
| TC-PLT-E2040-CON-07 | AC7 | Component | The three fakes over the kit fake, the worker fake and the reference-data fake; every example answered; a drifting field, state or status failing the build |
| TC-PLT-E2040-CON-08 | AC8 | Contract | v1 pinned; a field, a state, an outcome and the placeholder set changed; v2 published and v1 deprecated; an additive field raising the minor number |
| TC-PLT-E2040-CON-09 | AC9 | Contract | Each rule BR1 to BR8 traced to its criterion and test case; no rule without a criterion |
| TC-PLT-E2040-CON-10 | AC10 | Component | A retried activity and a timed-out activity replayed; a matching event passes; a non-matching event reported as the first mismatch with FAILED |

### 17. Guardrails

- No business value in a document, an example or a fake: the history count, the freshness limit, the time budgets, the retention and the build ID format are configuration values supplied by the pipeline and the reference-data contract.
- No personal data in an index row, a report, an example, a fake or a log: the replay store holds codec-encrypted SIT histories only, a report names a history ID and an event ID, and a payload scan fails the build otherwise.
- No production history is exported and no production data is used in a test or a prompt (NFR-045).
- No payload, no workflow input and no clear field in a report: MSG-P3-038 carries {detail} only, and the first mismatch is named by event ID and event type.
- No service short, no schema name, no topic name and no Workbench REST base in the document set: the platform owns none of them (DP-01, DP-13, DP-14).
- An empty, missing, stale or refused replay set is never a PASSED: the rule is one declaration in `replay-gate.yaml`, and no example or fake contradicts it.
- No build is retired while its running count is above zero, and no fake answers an accepted retirement of such a build.
- The contract is versioned: a breaking change raises v2 and deprecates v1 in place of editing v1, and the state and outcome codes come from the reference-data contract rather than from literals.

### 18. Traceability

| Requirement ID | Requirement (short) | Source | Test cases |
|---|---|---|---|
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written: a replay that reaches the same decisions proves the recorded path still matches the code | RWB-E2-040 section 18 (Epic 2, 3.2; Program, 5.7); R-UNI-39 | TC-PLT-E2040-CON-03, TC-PLT-E2040-CON-06 |
| ADR-011 | Workflow kit plus stage children plus Continue-As-New, which is why a workflow change must replay | Architecture v5 slide 24; Decision Log | TC-PLT-E2040-CON-03 |
| ADR-020 | Contract-first: the contract and its fakes are published before any code | Architecture Decision Records, ADR-020; Architecture v5 slide 11 | TC-PLT-E2040-CON-01, TC-PLT-E2040-CON-07, TC-PLT-E2040-CON-08 |
| DP-01 | No `rwb_*` table is read or owned; the index lives in Blob storage and the registry in the cluster | Template and Rules §R5.5 DP-01 | TC-PLT-E2040-CON-01 |
| DP-03 | The gate writes no decision record; the replayed workflow writes through the local library (RWB-PLT-E1027-CON) | Template and Rules §R5.5 DP-03 | TC-PLT-E2040-CON-01 |
| DP-05 | No ACE view and no `v_ace_*` read on the replay path | Template and Rules §R5.5 DP-05 | TC-PLT-E2040-CON-01 |
| DP-07 | The four build states and the two outcomes are reference-data codes of rwb-case (RWB-PLT-E1043-CON; C RWB-P3-E1043-CON) | Template and Rules §R5.5 DP-07 | TC-PLT-E2040-CON-04, TC-PLT-E2040-CON-07 |
| DP-10 | The nightly export becomes a Schedule on the task queue `rwb-platform`; the contract fixes the cadence and the freshness rule (RWB-PLT-E1071-CON) | Template and Rules §R5.5 DP-10 | TC-PLT-E2040-CON-02, TC-PLT-E2040-CON-06 |
| DP-11 | The legacy in-process replay call becomes a typed contract with a fake, one hop and a budget | Template and Rules §R5.5 DP-11 | TC-PLT-E2040-CON-07 |
| DP-13 | No `/api/recovery/<short>/v1` base, because the platform has no service short | Template and Rules §R5.5 DP-13 | TC-PLT-E2040-CON-01 |
| DP-14 | No topic and no event schema on the replay path (RWB-PLT-E1047-CON) | Template and Rules §R5.5 DP-14 | TC-PLT-E2040-CON-01 |
| DP-15 | No migration and no Flyway sequence of this story (RWB-PLT-E1044-CON) | Template and Rules §R5.5 DP-15 | TC-PLT-E2040-CON-01 |
| DP-19 | No screen and no gateway route; the report and the rollout view belong to the app story (RWB-PLT-N001-CON) | Template and Rules §R5.5 DP-19 | TC-PLT-E2040-CON-01 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E2040-APP | App development | H consumer: builds the export Schedule, the gate, the replay store writer and the rollout against this contract and its fakes |
| RWB-PLT-E1071-CON | Contract | The platform worker, the WorkflowGateway, the smoke workflow and the build ID format this document quotes |
| RWB-PLT-E1027-CON | Contract | The local decision-record library the replayed workflow calls; the gate writes no record of its own (DP-03) |
| RWB-PLT-E1043-CON | Contract | The reference data that supplies the four build states and the two gate outcomes (DP-07) |
| RWB-PLT-E1044-CON | Contract | The Flyway convention this story does not run (DP-15) |
| RWB-PLT-E1047-CON | Contract | The naming library the platform does not use for a topic of its own (DP-14) |
| RWB-PLT-N001-CON | Contract | gateway-bff; the gate report is not a Workbench screen and no route is added (DP-19) |
| RWB-P3-E1043-CON | Contract | C: the owner contract of the reference data behind the state and outcome codes, read one hop with a 2 s budget |
| RWB-PLT-E2039-CON | Contract | Sibling of the same legacy wave: backup, failover, upgrade and archive; the upgrade rule is what makes a pinned SDK version matter here |
| RWB-PLT-N003-INF | Infrastructure | Sibling: the namespace `rwb-recovery` with its retention, quotas and certificates the replay store depends on |
| RWB-PLT-NF08-INF | Infrastructure | Sibling: the platform baseline, the cluster version 1.30 or later and the Worker Versioning capability this contract assumes |

### 19. Out of scope

- The export job, the gate step, the replay store writer, the rollout script and the report publisher: RWB-PLT-E2040-APP.
- The cluster, the namespace, the persistence stores and the mTLS identities: RWB-PLT-E1070-CON and RWB-PLT-E1070-APP.
- The worker, the WorkflowGateway, the smoke workflow and the SDK wiring: RWB-PLT-E1071-CON and RWB-PLT-E1071-APP.
- The workflow kit templates and their own version rule: RWB-PLT-N010-CON and RWB-PLT-N010-APP.
- The case workflow code, the stage workflows and their getVersion calls: Epic 3, RWB-P3-E2043-CON and the service app stories.
- The codec server, decode and the administrative audit the payload check depends on: RWB-PLT-E2038-CON and RWB-PLT-E2038-APP.
- Backup, failover, upgrade and archive, including the SDK upgrade itself: RWB-PLT-E2039-CON and RWB-PLT-E2039-APP.
- The other nine pipeline checks, the merge checklist and the release gates: Recovery Workbench Engineering Practices; this story states gate 10's contract only.
- Alerts, the stuck scanner and the workflow dashboard: RWB-PLT-E2037-CON and RWB-PLT-E2037-APP.
- A Workbench screen for a gate result or for the build registry (Epic 8); both are pipeline and operational views.
- Production history export and any replay against production data.
