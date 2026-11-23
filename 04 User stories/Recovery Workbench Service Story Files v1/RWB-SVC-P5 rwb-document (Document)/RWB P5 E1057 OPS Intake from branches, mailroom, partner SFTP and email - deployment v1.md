# RWB-P5-E1057-OPS Intake from branches, mailroom, partner SFTP and email

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1057-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-057 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P5-Q |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-020, FR-P5-022, FR-P5-023) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-057 for rwb-document. The legacy story ran JOB-12 on a shared Quartz scheduler behind a shared schema, held the four channel paths as Spring properties of one monolith node, and expected an operator to read the job record in the database. This story deploys the channel-intake capability of `rwb-document`: one chart and its values, the `rwb_document` migration step, the 15-minute intake Schedule registered in Temporal on queue `rwb-document` in namespace `rwb-recovery`, the channel configuration and its four flags, the dashboards for the channels and the run states, the four alerts with their message identifiers, the runbook and the rollback. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform engineer**, I want **the channel-intake capability of `rwb-document` deployed as one Helm release with its values files, its per-service Flyway step in `rwb_document`, the channel configuration of each environment behind the flag `rwb.document.intake` and its four sub-flags, the 15-minute intake Schedule registered in Temporal on queue `rwb-document` in namespace `rwb-recovery`, the dashboards that show a channel that was read, a channel that failed and a folder that is filling, the four alerts with their message identifiers, and a runbook with its rollback**, so that **an operator can see a channel that stopped reading, a run that failed on one channel, a branch folder whose processed folder is filling and a mailbox whose grant was withdrawn, take the channel out of service with one flag without a redeploy, and prove that no file was taken in twice and none was lost when the flag was switched or the release was rolled back**.

The legacy story ran the pickup behind a shared Quartz scheduler, a shared schema and a property file: JOB-12 fired on the scheduler table, `IntakeStep` wrote the recovery schema, and the four channel paths were entries in a monolith's properties. In the target that picture splits in four. JOB-12 is a Temporal Schedule in the service that owns it, so the release registers the Schedule and the worker that serves it (DP-10). The migration is one step of the service's own Flyway sequence in `rwb_document` (DP-15). The channel configuration is one value block per environment, injected as configuration and never built into the image (BR6). The four channels have one feature switch each, so a branch, the mailroom, the SFTP root or the mailboxes can be taken out of service without a redeploy. What is left for this story is a chart, a migration gate, a Schedule, a configuration block, four switches, six dashboard series, four alert rules, five runbook entries and a rollback.

Deployment is also where the split is enforced operationally. The release carries the rwb-document login only, migrates `rwb_document` only, publishes on its own topic and on the shared decision-record topic only, polls `rwb-document` only, and reads only the channels of its own environment. It provisions no ACE grant, no view and no data-lake route (DP-01, DP-05, DP-17), and no inbound consumer of this path, because the trigger is the Schedule. The observability follows ADR-023 per service: six series, four alerts and five runbook entries, each alert carrying a message identifier and one runbook entry.

### 2. Business rationale

The business measure of this legacy key is documents on the case the same day (FSD P5 AC-BG-P5-013-01), and the operational measure behind it is simple: a channel that stops reading must be visible before the case owner asks where a scan went. Neither is a unit test. A branch folder whose grant was withdrawn, a partner key that expired, a mailbox whose permission was removed, a run that failed at 10:15 and a processed folder that is filling the branch file share are all silent unless the release emits them and the run book says what to do.

The split changes what an operator does. In the legacy story the operator restarted a Quartz job and read the job record in the same database. In the target the operator reads the Schedule's run history and the run record of the app story, restarts through the Schedule, takes one channel out of service through its own switch, and confirms three things: that the worker polled `rwb-document`, that the channel that failed is named, and that the files it did not take in are still at the channel so the next run reads them. The runbook is written for that sequence, because the difference between a busy morning and an incident is whether the operator has to guess which of the four channels stopped.

The story also carries the retirement explicitly. No Quartz job, no scheduler table and no shared schema is deployed; the Schedule is the only timer, and a release that registers a second one or a job on a foreign queue fails its own checks (BR1, BR2, BR3). The switches keep a channel reversible without a schema change, and the rollback keeps the previous build serving open runs.

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The Kafka event platform provides `rwb.document.events.v1` with its three retry topics and its `.dlt` topic and the shared `rwb.decision-record.v1`, and the ACLs of this service's principals (RWB-PLT-EVT, RWB-PLT-TE006-CON; DP-09).
- The Temporal workflow kit and the namespace `rwb-recovery` exist, with worker versioning, the build ID provider and the payload codec (RWB-PLT-WF, RWB-PLT-E1071-CON; DP-10).
- The per-service Flyway sequence and the migration conventions of `rwb_document` are published (RWB-PLT-E1044-CON; DP-15).
- The platform error envelope, the message catalogue and the feature-flag library are in force, so an alert can carry a message identifier and a channel can be switched in one environment.
- The three environments DEV, SIT and UAT exist and the production namespace exists for the release date.
- The four channels, the worker compute, the hold container, the topic binding, the ACLs, the identity and the private routes exist in each environment (RWB-P5-E1057-INF).
- The gateway-bff composite route for the run record is published (RWB-PLT-N001-CON; DP-19).
- The pickup activity and the run record are declared (RWB-P5-E1057-APP), so the release deploys a capability that exists and not a shell.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7). The baseline it deploys is RWB-P5-E1057-APP's and the values it injects are RWB-P5-E1057-INF's; both are declared before the release and neither blocks the chart work.
- The release date 30 November 2026 is the legacy one and is tentative (ASM-1826), and the story carries Status Draft (realignment v1) because no approval of the realigned story is recorded (ASM-1850).

### 4. Flow

1. The pipeline builds the service image and the contract jar, runs the unit, component and contract tests, scans the image and the dependencies, and publishes one chart version.
2. The chart deploys the API deployment and the worker deployment with the rwb-document login, the namespace `rwb-recovery`, the task queue `rwb-document`, the codec, the build ID of the release and the values of RWB-P5-E1057-INF.
3. The worker scaling step enables KEDA on the queue backlog of `rwb-document`, so the pool grows with the 15-minute run and the front stays at its fixed replica count.
4. The migration step applies the `rwb_document` sequence of the release and refuses to run when the target schema is not `rwb_document`; the intake migration `V1057_1__intake_channels.sql` is one step of it.
5. The channel step renders the four channel blocks of the environment — the branch folders by branch code, the mailroom folder, the SFTP root and the mailboxes with their processed, rejected and archive folder names — as configuration, and the Deployment states that no path, no branch code and no mailbox address is in the image.
6. The topic step verifies `rwb.document.events.v1` with its partitions, its replication factor, its retention, the three retry topics at 1 minute, 10 minutes and 1 hour and its `.dlt` topic, and records the ACL of the producer and of the consumer groups.
7. The Schedule step registers the intake Schedule: workflow `DocumentIntakeWorkflow`, queue `rwb-document`, namespace `rwb-recovery`, every 15 minutes in business hours, overlap policy skip and a catch-up window of one run, its ID fixed by the release so a second apply changes nothing.
8. The flag step sets `rwb.document.intake` and its four sub-flags `rwb.document.intake.branch`, `.mailroom`, `.sftp` and `.email` from the values of the environment; the legacy name `rwb.dochub.intake` and its four sub-flags are recorded as retired and are not deployed (ASM-1856).
9. The dashboards are published with the six series and the environment, release and build ID as dimensions.
10. The four alerts are wired to their message identifiers and to their runbook entries: MSG-P5-E1057-OPS-01 for a channel that is not ready, MSG-P5-008 for two failed runs in a row, MSG-P2-004 for a failed run, and MSG-P5-E1057-OPS-02 for a folder or a held file past its age rule.
11. A smoke step in DEV drops one synthetic file in a SIT branch folder and one in the mailroom folder, waits for one Schedule run, confirms one intake row per file, one move to each processed folder and one refused file in a rejected folder, switches the branch flag off to see the channel skipped, and confirms that the environment is restored.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The chart render or the migration job fails | The deployment stays unready and the pipeline stops; no traffic, no offset and no migration is left half applied | None | AC1 |
| X2 | The migration step is pointed at a schema other than `rwb_document` | The step refuses and the release stops | None | AC1 |
| X3 | A channel block is missing from the values of an environment, or a branch code has no folder | The render fails with the missing key named; a channel with no configuration is not deployed | MSG-P5-E1057-OPS-01 | AC1, AC3 |
| X4 | A channel path, a branch code or a mailbox address appears in the image or in a chart template | The configuration check fails the release | None | AC1, AC3 |
| X5 | A run of the intake Schedule fails, or runs past its threshold | The run-failure alert fires with MSG-P2-004 naming the run, the time and the runbook path; the Schedule retries on its next interval | MSG-P2-004 | AC2, AC4 |
| X6 | Two runs in a row fail on one channel | The channel alert fires with MSG-P5-008 naming the channel code and the runbook entry | MSG-P5-008 | AC4, AC6 |
| X7 | A dependency is not available, or its credential has expired | The run fails closed, the file stays at its channel, the channel alert fires with MSG-P5-E1057-OPS-01 and the runbook entry names the rotation | MSG-P5-E1057-OPS-01 | AC4, AC6 |
| X8 | The Schedule is registered twice, or a foreign job is registered on the queue | The Schedule check fails the release: one Schedule ID, one workflow, one queue | None | AC2 |
| X9 | A dashboard series is missing, or an alert carries no message identifier or no runbook link | The observability check fails the release | None | AC4 |
| X10 | A new build is promoted while runs are open | The open runs replay on the new build from their history; the dashboards show both build IDs | None | AC1, AC4 |
| X11 | A channel is switched off in an environment | The channel is skipped and the run completes with zero on it; a switched-off channel is not an error and is not counted as failed | None | AC6 |
| X12 | The lag of the attach-event consumer group passes its threshold | The lag alert fires; the runbook entry names the group, the topic and the partition | Not specified in the source documents (GAP-1015; ASM-1854) | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the workflow kit, the topic provisioning, the migration conventions, the flag library and the channel values; no application code is built here |
| Negotiable | Replica counts, resource sizes, lag and age thresholds, intervals and quotas are environment values |
| Valuable | Makes the four channels observable, restartable and reversible before the release date, and keeps a channel switchable without a redeploy |
| Estimable | One chart, one migration gate, one Schedule, one channel block with four switches, six series, four alerts and five runbook entries |
| Small | Fits one sprint with the runbook |
| Testable | Every criterion tests an artefact: the chart renders, the migration refuses a foreign schema, the Schedule exists once, an alert fires on a synthetic metric, a switch skips a channel, the smoke run passes |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the channel-intake capability for rwb-document

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the namespace is rwb-recovery and the task queue of rwb-document is rwb-document
    Given the target environment is SIT

  Scenario: AC1 One chart, one login, one schema and one queue are deployed with the channel configuration injected (new, D-RCV-60)
    Given the rwb-document chart and its values files
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the API and the worker deployments carry the rwb-document login and no other service's credential
    Then the worker polls only the task queue rwb-document in namespace rwb-recovery and KEDA scales it on the queue backlog
    Then the migration step applies the rwb_document sequence with V1057_1__intake_channels.sql and refuses a target schema other than rwb_document
    Then the four channel blocks are injected as configuration for the environment and no folder path, branch code, partner code or mailbox address appears in the image or in a chart template
    Then worker versioning is enabled and a new run goes to the new build while the old build drains
    Then the deployment registers no Quartz job and no scheduler table
    Then the chart key names and the channel block layout are Not specified in the source documents (GAP-1015; ASM-1852)

  Scenario: AC2 The 15-minute intake Schedule is registered in Temporal and in no other scheduler (new, D-RCV-60)
    Given the deployed release and the namespace rwb-recovery
    When the Schedule step runs and is applied a second time
    Then one Schedule exists with the ID fixed by the release, the workflow DocumentIntakeWorkflow and the queue rwb-document
    Then its interval is every 15 minutes in business hours and its overlap policy is skip with a catch-up window of one run
    Then the second apply creates no second Schedule and changes nothing
    Then no Quartz job, no scheduler table and no cron entry exists in the release
    Then a run that fails is retried on its next interval and the files it did not take in are still at their channels
    Then the Schedule ID and the run slot are the identity the run record and the rerun use
    Then the exact business-hours window and the catch-up policy are Not specified in the source documents (GAP-1015; ASM-1851)

  Scenario: AC3 The four pickup channels and their switches are deployed per environment (new, D-RCV-60)
    Given the channel blocks of the environment and the feature-flag library
    When the release is deployed in DEV, SIT and UAT
    Then the branch block carries one entry per branch code with its scanner, processed and rejected folder names, and the mailroom block carries its folder names
    Then the partner SFTP block carries the inbound root and the processed and rejected subfolder names, and no partner key is written in a values file
    Then the mailbox block carries the declared mailbox codes and their archive folder names, and no mailbox address is written in a values file beyond the reference the environment supplies
    Then the four switches rwb.document.intake.branch, .mailroom, .sftp and .email are deployed with their environment values
    Then a switch that is off makes the run skip that channel and complete with zero on it
    Then a missing channel block fails the render with the missing key named
    Then the branch codes, the folder names, the mailbox codes and the channel values are Not specified in the source documents (GAP-1015; ASM-1851)

  Scenario: AC4 The dashboards and the four alerts fire with their identifiers (new, D-RCV-60)
    Given the published dashboards and alert rules of the deployment
    When a synthetic run reads every channel, fails one channel twice, and leaves one held file and one processed folder past their age rules
    Then the dashboards show runs by state, files taken in per channel, refusals per reason code, duplicates per channel, the age of the oldest held file, and the queue backlog and age of the task queue
    Then each series carries the environment, the release and the build ID as dimensions
    Then the run-failure alert fires with MSG-P2-004 naming the run, the time, the business date and the runbook path
    Then the channel alert fires with MSG-P5-008 naming the channel code of the second failure in a row
    Then the channel-not-ready alert fires with MSG-P5-E1057-OPS-01 naming the channel and its credential or grant
    Then the age alert fires with MSG-P5-E1057-OPS-02 naming the folder or the held file
    Then each alert carries a message identifier or its placeholder and one runbook link, and no alert payload carries a file name, a sender address, an account number or a customer identifier

  Scenario: AC5 The runbook and the rollback are exercised (new, D-RCV-60)
    Given the published runbook and the rollback of the release
    When a failed run, a channel that is not ready, an expired partner key, a mailbox whose grant was withdrawn and a filling processed folder are simulated
    Then each condition maps to one runbook entry with the check, the owner role and the recovery step
    Then the runbook states that a file the run did not take in is still at its channel and is read by the next run, and that no operator deletes a file at a channel
    Then the rollback redeploys the previous chart with its own build ID and the open runs finish on the old build
    Then the Schedule keeps its ID across the rollback and points at the same workflow, so only the build under it changes
    Then the smoke run ends with one intake row per synthetic file, one move to each processed folder, one refused file in a rejected folder and the environment restored
    Then the runbook entries, the smoke run and the thresholds are this story's construction and are Not specified in the source documents (GAP-1015; ASM-1855)

  Scenario: AC6 The feature switches take one channel out of service without a redeploy (new, D-RCV-60)
    Given the feature-flag library and the deployed release
    When the switch rwb.document.intake.branch is turned off in SIT and one Schedule run is waited for
    Then the run skips the branch channel, completes with zero on it and takes in the mailroom, partner and mailbox files of the same window
    Then the switched-off channel is reported as skipped and never as failed, and no alert fires for it
    When the switch rwb.document.intake is turned off and one Schedule run is waited for
    Then no channel is read and the run completes with zero on every channel
    Then the legacy flag rwb.dochub.intake and its four sub-flags appear in no values file, chart or runbook
    Then a switch change needs no rebuild, no migration and no restart of the worker
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One login, one task queue and one schema per service: the release carries the rwb-document login, polls `rwb-document` only and migrates `rwb_document` only | Arch v5 slide 41; DP-02; DP-15 |
| BR2 | The release publishes on `rwb.document.events.v1` and `rwb.decision-record.v1` only and subscribes to no topic of this service | Arch v5 slides 16, 42 and 43; DP-09; DP-14 |
| BR3 | One Schedule and one scheduler: the intake Schedule is the only timer for JOB-12, registered in Temporal on queue `rwb-document` in namespace `rwb-recovery`; no Quartz job, no scheduler table and no cron entry exists | Arch v5 slide 44; DP-10; `ASM-1851` |
| BR4 | Each of the four channels is switchable by its own flag, and the whole path by `rwb.document.intake`, which replaces the legacy `rwb.dochub.intake` | legacy section 13; DP-14; `ASM-1856` |
| BR5 | A channel is configuration and never code: the branch folders, the mailroom folder, the SFTP root and the mailboxes come from the values of the environment and never from the image | RWB-E1-057 section 8 BR8; Template and Rules §R7.2 s17 |
| BR6 | No partner key, no mailbox credential and no connection string is written in a values file, a chart template, a dashboard or the runbook; all of them come from the platform secret store | NFR-052 |
| BR7 | Every alert carries a message identifier and the agreed text and links one runbook entry | Template and Rules §R7.2 s14 |
| BR8 | No environment value is hard-coded: replicas, resources, thresholds, intervals, quotas, channel blocks and flags come from values files and parameters | Template and Rules §R7.2 s17 |
| BR9 | Dashboard series, alert payloads and the runbook carry counts, channel codes, statuses, business dates and build IDs only, never a file name, a sender address or a customer identifier | ADR-023; CTL-11 |
| BR10 | A failing release never replaces a working one: the previous build stays in force until the new build passes its tests and its smoke run, and the Schedule keeps its ID across a rollback | DP-10 |
| BR11 | A file the run did not take in is never deleted and never moved by an operator: it stays at its channel for the next run, and a switched-off channel is skipped and never failed | R-UNI-40; legacy X4, X10, X11 |
| BR12 | The release provisions no ACE grant, no view, no data-lake route and no inbound consumer of this path | D-RCV-35 U1; ADR-010; DP-05; DP-17 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the contract tests pass | Deploying |
| Deploying | Migration applied and worker registered | The `rwb_document` sequence applied and the worker polls `rwb-document` | Ready |
| Ready | Channel blocks rendered | Every channel block of the environment is present and no path is in the image | Configured |
| Configured | Schedule registered | One Schedule with the release ID, the workflow and the queue | Scheduled |
| Scheduled | First run completes | The run finishes and its counts reach the dashboards | In use |
| In use | Release superseded | A new chart version passes its tests | Rolling |
| Rolling | All workers on the new build | The old build drains its open runs | In use |
| In use | A channel switch is turned off | `rwb.document.intake.<channel>` is off in the environment | Partly in use |
| Partly in use | The switch is turned on again | The next run reads the channel | In use |
| In use | Smoke run failed | The Schedule check, the alert check or the smoke step fails | Blocked |
| Blocked | Previous build restored | The previous chart is redeployed or a later build passes the smoke run | In use |

The run states running, failed and complete and the intake item states of the app story are its runtime and are not states of this deployment.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the migration gate, the channel block, the Schedule step, the dashboards and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the Schedule, the topic ACLs, the consumer quotas, the flag library and the restart of a run |
| Platform event owner | Owns `rwb.document.events.v1`, its retry and `.dlt` topics, its schema subject and its retention |
| Network and security | Own the partner key material, the mailbox grant and the public-access scan; approve any relaxation |
| Release manager | Approves the promotion of one artefact and may block it on a failing smoke run |
| On-call operator | Runs the five runbook entries and opens an incident when a failed run, a channel that is not ready or a filling folder persists |
| rwb-document owner | Owns the pickup, the run record and the migration the release applies |
| Data steward | Confirms that no dashboard, alert or runbook carries a file name, a sender address or a customer identifier |
| RW-AUDIT | Reads the run history, the alert trail and the runbook |

The worker runs as the rwb-document service identity (DP-02), carried by the chart as a secret reference and never as a literal. The login name is Not specified in the source documents (GAP-1015; ASM-1852). The partner keys and the mailbox credential are secret references, and the values file carries the reference name and never the value.

### 11. Data

| Item | Content |
|---|---|
| Deployment values | Image digest, chart version, replica counts for the API and the worker, resource requests and limits, probe paths and timings, log level, namespace, task queue, build ID, feature switches, KEDA backlog threshold, Schedule ID and interval (ASM-1852) |
| Channel block | The branch entries with their scanner, processed and rejected folder names; the mailroom entry with its folder names; the SFTP root with its processed and rejected subfolder names; the mailbox entries with their codes and archive folder names; and the secret reference names of the partner keys and the mailbox credential. The values are the environment's and are Not specified in the source documents (GAP-1015; ASM-1851) |
| Task queue | `rwb-document` in namespace `rwb-recovery`, polled by the worker of this service only |
| Topic | `rwb.document.events.v1` with its partitions, replication factor, retention and key, its three retry topics and its `.dlt` topic; `rwb.decision-record.v1` published by the library; no subscription of this service |
| Schema | `rwb_document`, migrated by its own per-service Flyway sequence; the intake migration `V1057_1__intake_channels.sql` is one step of it |
| Schedule | The intake Schedule: `DocumentIntakeWorkflow`, queue `rwb-document`, namespace `rwb-recovery`, every 15 minutes in business hours (JOB-12), overlap policy skip, catch-up window one run, ID fixed by the release |
| Flags | `rwb.document.intake` and `rwb.document.intake.branch`, `.mailroom`, `.sftp` and `.email`, on in DEV and SIT for the tests, from the values of each environment; the legacy `rwb.dochub.intake` and its four sub-flags are retired |
| Dashboard series | Runs by state, files taken in per channel, refusals per reason code, duplicates per channel, age of the oldest held file, queue backlog and age; dimensions environment, release, build ID |
| Runbook entries | Failed run, channel not ready, expired partner key or withdrawn mailbox grant, filling processed folder or held file past its age rule, lagging consumer group; each with the check, the owner role and the recovery step |
| Alerts | Four rules and one runbook entry each: MSG-P5-E1057-OPS-01 for a channel not ready, MSG-P5-008 for two failed runs in a row on a channel, MSG-P2-004 for a failed run, MSG-P5-E1057-OPS-02 for a folder or held file past its age rule; the lag alert carries the identifier placeholder of GAP-1015 |
| Secrets | The rwb-document login secret, the Kafka client credential, the Temporal mTLS material, the storage identity reference, the partner SFTP keys and the mailbox credential, all from the platform secret store |
| Test data | One synthetic file in a branch folder, one in the mailroom folder, one refused file and one flag-off run; synthetic identifiers only |

The deployment topology (cluster names, node pools, replica counts, resource sizes, zone spread, ingress class and probe timings) belongs to each environment and is set by the platform team in its values file; the chart exposes every one of them as a value and this story fixes only their names and the rule that they are never hard-coded.

**Probes.** Readiness answers healthy only after the worker has polled `rwb-document` once and the API has answered its health path; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe reads a channel, writes to the database or commits an offset, and a failing dependency is reported as not ready, never as live-and-broken.

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Owner | Notes |
|---|---|---|---|
| None | — | — | The three admin operations — `GET /api/recovery/document/v1/admin/jobs`, `GET /api/recovery/document/v1/admin/jobs/{jobId}` and `POST /api/recovery/document/v1/admin/jobs/{jobId}/rerun` — are declared by RWB-P5-E1057-CON and implemented by RWB-P5-E1057-APP; this deployment exposes them through the chart and its ingress and declares no path of its own. The probes are cluster-internal and are not part of the API surface |

#### 12.2 REST operations consumed

| Method | Path | Owner | Story | Note |
|---|---|---|---|---|
| None | — | — | — | The deployment carries no REST client of its own. At run time the app story's client reaches `rwb-partner` and the shared clients reach `rwb-case` over the private routes of RWB-P5-E1057-INF; the chart's only start-up calls are the Temporal frontend, the Kafka brokers and the health paths of its own dependencies |

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| None | — | — | — | This path publishes no event. `rwb.document.events.v1` and `rwb.decision-record.v1` are bound by the release and written by the store and by the local decision-record library through the relay (DP-03, DP-09); the deployment publishes nothing of its own |

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| None | — | — | This path consumes no event: the trigger is the intake Schedule. The consumer groups of `rwb-case` and `rwb-agent` on `rwb.document.events.v1` are theirs and not deployed here |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| `DocumentIntakeWorkflow` | Workflow, from the L3 "Document intake" template | `rwb-document` | Registered by the worker of this release with the build ID and worker versioning; owned by RWB-P5-E1049-APP |
| `pickup` | Activity | `rwb-document` | Registered by the same worker with the kit's retry policy; owned by RWB-P5-E1057-APP |

**Build ID and versioning.** The build ID is the one supplied by the workflow kit for the release commit; worker versioning is enabled and a new build takes new runs while the old build drains. The build ID format and the versioning policy are Not specified in the source documents (GAP-1015; ASM-1853).

#### 12.6 Schedules

| Schedule | Workflow | Queue | Interval | Note |
|---|---|---|---|---|
| The intake Schedule (JOB-12 Document intake) | `DocumentIntakeWorkflow` | `rwb-document` | Every 15 minutes in business hours | Registered by this release from its values, with the ID fixed by the release, overlap policy skip and a catch-up window of one run; a run that fails is retried on its next interval and the files it did not take in stay at their channels. The exact business-hours window and the catch-up policy are Not specified in the source documents (GAP-1015; ASM-1851) |

No other Schedule, cron entry or Quartz job is registered by this release (BR3).

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `document_intake` | P5 (`rwb_document`) | Created or altered by the `rwb_document` sequence of the release; written by the app story, never by the deployment |
| `document_hub_parameter` | P5 (`rwb_document`) | Created by the store's migration; the five parameter rows are loaded as data by the reference data administrator, never as a chart value |
| idempotency library table | PLT library, created in `rwb_document` | Created by the library migrations in the same schema; written by the app story |
| outbox, inbox library tables | PLT library, created in `rwb_document` | Created by the library migrations in the same schema; this path writes no outbox row of its own |

The release applies the `rwb_document` sequence of this key and no other: no ACE view, no other service's table and no lake object is created, altered or read (DP-01, DP-05, DP-15, DP-17).

#### 12.8 Contract fakes

| Fake | Story | Used for |
|---|---|---|
| None | — | No fake is deployed. The contract fakes of RWB-P5-E1057-CON and the channel and storage fixtures of RWB-P5-E1057-INF are test-only workloads and are not promoted into SIT, UAT or production |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 0 consumed by the deployment | The three admin operations are the app story's; the probes are cluster-internal |
| Kafka | 0 published, 0 consumed here; 1 topic verified with retry and `.dlt` | `rwb.document.events.v1` with its ACLs and `rwb.decision-record.v1` bound by the release; no subscription |
| Temporal | 1 workflow, 1 activity, 1 Schedule | Worker on `rwb-document` with a pinned build ID, worker versioning and KEDA scaling; the intake Schedule every 15 minutes in business hours |
| File | 4 channels configured, 3 containers referenced | The branch, mailroom, SFTP and mailbox blocks of the environment; the values point at `rwb-docs`, `rwb-docs-legal` and `rwb-quarantine` of RWB-P5-E1057-INF; no file is built or moved by the deployment |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | The release migrates `rwb_document` only and reads no other schema | none |
| DP-06 | Parameters, casewf.config | The five parameters stay rows read through the client library; no chart value carries them | H RWB-PLT-E1042-CON |
| DP-07 | Reference data, LOV | The three lists stay reference rows; no chart value carries them | H RWB-PLT-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | The topic with its retry and `.dlt` topics and the ACLs; the path binds no consumer group | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | The worker, the task queue, worker versioning and the intake Schedule from the kit; no Quartz job | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | The release declares no REST path and no client of its own; the private routes are RWB-P5-E1057-INF's | none |
| DP-13 | `/api/recovery/v1` | The ingress registers the service base `/api/recovery/document/v1` and declares no path of its own | none |
| DP-15 | V0001 baseline, migration | The `rwb_document` sequence with its intake step and a foreign-schema refusal | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | The ingress registers the service base for the gateway-bff edge; no screen is deployed | H RWB-PLT-N001-CON |

DP-10 is the substantive row of this story: JOB-12 stops being a Quartz job on a shared scheduler and becomes a Temporal Schedule on the service's own queue, so the release registers the Schedule, the worker and the build ID, and the operator restarts a run through the Schedule rather than a scheduler table. DP-01 and DP-15 keep the migration inside `rwb_document` and make the step refuse a foreign schema. DP-02 is not in the pattern list of the key and is applied by the chart anyway: one login, carried as a secret reference. DP-06 and DP-07 keep the parameters and the three lists out of the values files. DP-09 binds the topic and its four derived topics and subscribes to nothing. DP-11 and DP-13 are applied by absence: the release declares no REST path of its own and no client. DP-19 registers the ingress path the edge calls and deploys no screen.

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-document/` overlay | API deployment, worker deployment, config map, secret references, probes, task queue, namespace, build ID, KEDA rule, Schedule definition, channel block and the five switches |
| `helm/rwb-document/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, flag values, build ID, Schedule ID and interval, KEDA threshold, container references, the four channel blocks and the secret reference names (ASM-1852) |
| Pipeline stage | Build, unit and contract tests, image and dependency scan, chart publish, migration gate, channel configuration check, topic step, Schedule step, smoke run, promotion |
| Migration step | The `rwb_document` sequence with `V1057_1__intake_channels.sql`; a target schema other than `rwb_document` is refused |
| Channel step | The four channel blocks as configuration per environment and the check that no path, no branch code and no mailbox address is in the image or a template |
| Topic step | `rwb.document.events.v1` with its three retry topics and its `.dlt`, the producer ACL and the consumer ACLs of rwb-case and rwb-agent |
| Schedule step | The intake Schedule with its release ID, the workflow, the queue, the interval, the overlap policy and the catch-up window, idempotent on the ID |
| Dashboards | The six series of section 11 with the three dimensions |
| Alerts | Four rules, each with a message identifier or its placeholder and one runbook entry |
| Runbook | Five entries: failed run, channel not ready, expired partner key or withdrawn mailbox grant, filling processed folder or held file past its age rule, lagging consumer group |

**Alert mapping**

| Message ID | Condition | Alert | Route |
|---|---|---|---|
| MSG-P5-E1057-OPS-01 | A channel is not reachable, its grant is missing or its key does not match | Channel-not-ready alert naming the channel code, the run and the grant or key class | Platform on-call and network security, page |
| MSG-P5-008 | Two runs in a row failed on one channel | Channel alert naming the channel code, the two runs and the runbook path | Platform on-call, page in business hours, else ticket |
| MSG-P2-004 | A run of the intake Schedule failed or ran past its threshold | Run-failure alert naming the Schedule ID, the run, the time, the business date and the runbook path | Platform on-call, page in business hours, else ticket |
| MSG-P5-E1057-OPS-02 | A processed or rejected folder, or a held file, is past its age rule | Age alert naming the folder or the item count per channel | Branch operations, the mailroom and the data steward, ticket |
| Not specified in the source documents (GAP-1015; ASM-1854) | The attach-event consumer group lags past its threshold | Lag alert naming the group, the topic, the partition and the lag | Platform on-call, ticket |

**Retry and offsets.** The Schedule retries a failed run on its next interval and never runs two runs at once, because the overlap policy is skip. The activity retry is the kit's three attempts with back-off; the deployment adds no retry of its own. A file the failed run did not take in is still at its channel and is read by the next run, so no replay tool and no offset reset is part of this runbook.

**Rollback.** A release that fails the smoke run is not promoted. A release already promoted is rolled back by redeploying the previous chart version with its own build ID, which keeps the old build serving its open runs until they finish; the Schedule keeps its ID and points at the workflow, so a rollback changes the build under it and not the timer. Files a failed run did not take in are still at their channels and are read again; no data repair is needed, because the release writes no business row of its own and the migration is additive.

**Feature switch.** `rwb.document.intake` and its four sub-flags. On: the pickup reads the channels. Off: the channel is skipped and the run completes with zero on it. A switch change is a configuration change in the flag library, needs no rebuild, no migration and no restart, and is not a way to stop a run in progress, which is what the Schedule and the runbook are for. The legacy name `rwb.dochub.intake` and its four sub-flags appear in no value, chart or runbook (ASM-1856).

**Done when.** The chart renders for DEV, SIT and UAT with a pinned digest and the build ID, the migration step refuses a foreign schema, the four channel blocks render as configuration with no path in the image, one Schedule exists with the release ID and the queue `rwb-document` and a second apply changes nothing, a switched-off channel is skipped and never failed, the six series and the four alerts are published with their identifiers or placeholders and their runbook links, the smoke run produces one row per synthetic file, one move per processed folder, one refusal and no duplicate, and the five runbook entries are reviewed by the on-call rota. The alert thresholds, the intervals, the catch-up window and the channel values are Not specified in the source documents (GAP-1015; ASM-1851).

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-E1057-OPS-01 | A channel is not ready, its grant is missing or its key does not match | Channel {channel} of document intake is not ready. Follow run book {runbook}. |
| MSG-P5-E1057-OPS-02 | A folder or a held file is past its age rule | {resource} of document intake is past its age rule. Follow run book {runbook}. |
| MSG-P2-004 | A run of the intake Schedule failed or ran past its threshold | {job} failed at {time} for business date {date}. Follow run book {runbook}. |
| MSG-P5-008 | Two runs in a row failed on one channel | Document intake failed twice in a row for {channel}. Check the interface and job monitor. |
| Identifier pending | The attach-event consumer group lags past its threshold | Not specified in the source documents (GAP-1015; ASM-1854) |

MSG-P5-008 is the legacy alert text of section 14 of RWB-E1-057 and is unchanged. MSG-P2-004 is the job-failure text of the observability epic and is used here with its agreed wording. MSG-P5-E1057-OPS-01 and MSG-P5-E1057-OPS-02 are the deployment's own two texts and are new; no legacy business message is renumbered or reworded by them. The lag alert has no identifier in the source set, so it carries the placeholder until the Error and Message Standard names it. An alert payload names counts, channel codes, statuses, business dates, the Schedule ID, the build ID and group names only, never a file name, a sender address, an account number or a customer identifier.

### 15. Screens and states

The deployment has no screen of its own. Its operator-facing surfaces are the pipeline run view, the release view, the Temporal Web UI, the dashboards, the folder and mailbox inventories of the file service and the mail service, the run record of RWB-P5-E1057-APP through the gateway-bff composite route, and the runbook. The run record is served by the app story and the route of RWB-PLT-N001-CON; the deployment only registers the ingress path. The Temporal Web UI stays behind Entra ID: RW-PLATADM operates and RW-AUDIT reads, and payloads are decoded only through the codec server under break-glass. SCR-44 Interface and job monitor belongs to Epic 2 and shows the same run data from there; this release publishes the records the monitor reads.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P5-E1057-OPS-01 | AC1, BR1, BR5, BR12 | NFR | The chart renders for three environments with a pinned digest, the build ID, the login reference and worker versioning; the four channel blocks render as configuration and a path in a template fails the check; a foreign migration target is refused; the worker polls only `rwb-document` |
| TC-P5-E1057-OPS-02 | AC2, BR3 | NFR | One Schedule with the release ID, the workflow and the interval; a second apply changes nothing; a failed run is retried on its next interval and its files stay at their channels; no Quartz job and no scheduler table |
| TC-P5-E1057-OPS-03 | AC3, BR5, BR6 | NFR | The four channel blocks of SIT with the branch, mailroom, SFTP and mailbox entries; a missing block fails the render; a partner key or a mailbox credential in a values file fails the secret scan; a switch that is off skips the channel |
| TC-P5-E1057-OPS-04 | AC4, BR7, BR9 | NFR | A synthetic run over all channels, one channel failing twice, one held file and one processed folder past their age rules; the four alerts fire with their identifiers or placeholder, one runbook link each, and no personal data |
| TC-P5-E1057-OPS-05 | AC5, BR10, BR11 | NFR | Five synthetic conditions map to five runbook entries; the rollback redeploys the previous build; the Schedule keeps its ID; the smoke run leaves one row per file, one move per processed folder, one refusal and no duplicate |
| TC-P5-E1057-OPS-06 | AC6, BR4 | NFR | The branch switch off skips the branch channel and reads the other three; the whole path off completes with zero on every channel; the legacy flag name appears nowhere; a switch change needs no rebuild, no migration and no restart |

The legacy test cases this path serves are owned by the app story RWB-P5-E1057-APP and are not copied here: TC-E1-057-01 branch scan, TC-E1-057-02 partner SFTP, TC-E1-057-03 mailbox, TC-E1-057-04 mailroom scan, TC-E1-057-05 file type refused, TC-E1-057-06 size refused, TC-E1-057-07 unknown or suspended partner, TC-E1-057-08 duplicate, TC-E1-057-09 empty run, TC-E1-057-10 container refuses writes, TC-E1-057-11 two failed runs, TC-E1-057-12 one run across two instances, TC-E1-057-13 email with no usable attachment, TC-E1-057-14 file seen again after a failed move, TC-E1-057-15 outside business hours, TC-E1-057-16 scanned before OCR and TC-E1-057-17 rerun without the right. The contract-level copies of the same seventeen sit in RWB-P5-E1057-CON.

### 17. Guardrails

- No business value in a values file: the type list, the size limit, the duplicate window, the alert threshold and the channel values are parameters and reference rows, never a deployment value.
- No personal data in logs, dashboard series, alert payloads, the runbook or the workflow history: counts, channel codes, statuses, identifiers, business dates and build IDs only, and payloads stay encrypted.
- No partner key, no mailbox credential and no connection string in a values file, a chart template, a dashboard or the runbook; all of them come from the platform secret store (BR6, NFR-052).
- One login, one task queue and one schema per service: the release carries the rwb-document login, polls `rwb-document` and migrates `rwb_document` only (DP-02, DP-15).
- A channel is configuration and never code: the branch folders, the mailroom folder, the SFTP root and the mailboxes come from the values of the environment and never from the image (BR5).
- The release deploys no ACE grant, no view, no data-lake route and no inbound consumer of this path (DP-05, DP-17, BR12).
- One Schedule and one scheduler: no Quartz job, no scheduler table and no cron entry besides the intake Schedule (BR3).
- An operator never deletes a file at a channel and never resets a cursor to make a file reappear; the next run reads it (BR11).
- The release pins the image digest, the chart version and the build ID; a rebuild between environments is not allowed, and a failing smoke run never replaces a working build.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-DCM-009 | Documents arrive from branches, the mailroom, partner file transfer and email through the same intake | The four channel blocks, the five switches and the one worker and Schedule that read them | TC-P5-E1057-OPS-01, TC-P5-E1057-OPS-03, TC-P5-E1057-OPS-06 |
| REQ-DCM-010 | Every document carries a retention class, and intake runs a virus scan before the document is stored | The order the Schedule-started workflow runs and the runbook entry that the next run reads what a failed run left | TC-P5-E1057-OPS-02, TC-P5-E1057-OPS-05 |
| Arch v5 slide 44 | JOB-12 Document intake runs every 15 minutes, owned by rwb-document, as a schedule in the owning service | The intake Schedule, the worker and the build ID | TC-P5-E1057-OPS-01, TC-P5-E1057-OPS-02 |
| Arch v5 slide 41 | One schema, one API base, one topic and one task queue per service | The migration gate, the topic step and the queue binding | TC-P5-E1057-OPS-01 |
| Arch v5 slide 42 | rwb-document publishes on `rwb.document.events.v1`; DocumentStored is consumed by rwb-case and rwb-agent | The topic, its ACLs and the absence of a subscription of this service | TC-P5-E1057-OPS-01 |
| Arch v5 slide 38 | The platform provides the template, the schemas and logins, the topic set and Temporal before the wave 1 services | The bindings this release verifies and the pieces it deploys | TC-P5-E1057-OPS-01, TC-P5-E1057-OPS-02 |
| Arch v5 slide 35 | Partners only through the partner gateway in a separate DMZ, and keys in the key store | The secret reference names of the partner keys and the mailbox credential in the channel block | TC-P5-E1057-OPS-03, TC-P5-E1057-OPS-04 |
| ADR-023 | Observability per service | The six series, the four alerts and the five runbook entries | TC-P5-E1057-OPS-04, TC-P5-E1057-OPS-05 |
| NFR-068 | A failing interface, job or agent raises an alert to a named owner within its target | The channel, run, age and dependency alerts with their routes | TC-P5-E1057-OPS-04 |
| NFR-052 | Secrets in the key store and never in code or configuration | Secret references only, and the secret scan of the release | TC-P5-E1057-OPS-01, TC-P5-E1057-OPS-03 |

### 19. Out of scope

- The build of the pickup activity, the channel readers, the intake service, the alert service and the run record (RWB-P5-E1057-APP).
- The contract documents, the shapes, the enumerations and the fakes (RWB-P5-E1057-CON); this story only deploys and gates them.
- The four channels, the folders, the mailbox grants, the worker compute, the hold container, the topic binding, the ACLs, the identity and the route (RWB-P5-E1057-INF).
- The Temporal cluster, the namespace, worker versioning and the codec server as platform components (RWB-PLT-WF, RWB-PLT-E1071-CON).
- The topic provisioning, the schema registry and the `.dlt` retention as platform components (RWB-PLT-EVT, RWB-PLT-TE006-CON); this story verifies them and deploys no consumer group.
- The branch scanners, the mailroom equipment and the mailbox tenant configuration beyond the four declared mailboxes (branch operations, the mailroom and the mail team).
- The partner gateway itself and its penetration test (the edge epic, RWB-PLT-EDGE).
- The ingestion, OCR, classification and extraction activities of the same workflow (RWB-P5-E1049-APP, RWB-P5-E1050-APP, RWB-P5-E1053-APP).
- The SCR-44 screen and the full interface and job monitor (Epic 2, Epic 8).
- The real cross-service journey of the path with all services live (RWB-ITG-E1057-ITG).
- The exact cluster topology, node pools, replica counts, alert thresholds, the business-hours window, the catch-up policy and the channel values, which are set per environment by the platform team (GAP-1015).
