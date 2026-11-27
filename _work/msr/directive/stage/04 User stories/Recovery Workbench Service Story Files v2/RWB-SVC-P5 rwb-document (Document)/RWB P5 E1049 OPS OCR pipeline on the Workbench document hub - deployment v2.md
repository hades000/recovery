# RWB-P5-E1049-OPS OCR pipeline on the Workbench document hub

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1049-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-049 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P5-L |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement (DOR-RWB-P5-E1049-OPS-16) |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | v1 (the /v1 API path) |
| Integration dependencies | None |
| External dependencies | RWB-P5-E1049-INF (OCR engine, external dependency) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-013, FR-P5-016, FR-P5-020, FR-P5-022, FR-P5-023, FR-P5-027) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-049 for the deployment of the OCR pipeline of `rwb-document`; the Quartz job of legacy JOB-12 becomes a Temporal Schedule registered from configuration, and the job-monitor counts become dashboards, alerts and a runbook. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (13 resolved, 17 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform administrator**, I want **the OCR pipeline of `rwb-document` deployed from the service template with its chart, its values files and its own login, the `DocumentIntakeWorkflow` and its five activities on queue `rwb-document` in namespace `rwb-recovery`, the 15-minute business-hours Schedule registered from configuration, the feature flag `rwb.document.ocr`, dashboards for intake volume, OCR failure rate and held items, alerts that name the platform administrator, a runbook for a failed run, a held item and a re-run of a business date, and a rehearsed rollback**, so that **an operator can see within minutes that OCR has stopped, that items are being held for rescan or that the engine is failing, and repair it inside the business day without reading code or waiting for a business report**.

This story deploys an existing capability. It adds no table, builds no endpoint and writes no text: the run is `DocumentIntakeWorkflow` on queue `rwb-document`, the engine is the external provider that RWB-P5-E1049-INF provisions, the status and the text rows are RWB-P5-E1049-APP's, and the Schedule only starts the work.

### 2. Business rationale

The legacy capability leaned on a Quartz job whose only failure signal was a job exception, so a run that stopped on a refused engine and a run that read nothing looked the same as a quiet quarter-hour. In the target the run is a Temporal Schedule and a workflow (DP-10), the engine is an external provider behind a private route, and the status is a set of values on the intake item (DP-09 carries the completion event). There is no scheduler row to be late and no job record to inspect, so the operational signal moves from "did the job run" to "did the items move, is the engine answering, and how long has an item been held".

Two properties make deployment part of the capability. First, the failure is silent for the case owner: an item that stays PENDING looks like a document nobody read, and an item held in RESCAN looks like a rescan nobody was told about, so the failure-rate and held-item alerts have to be built here or nobody raises them. Second, the legacy promise is time-bound: every scan becomes text the same day and an unreadable page is sent back for rescan the same day, with the 60-minute throughput of legacy AC2 and the 500-pages-an-hour target of Arch v5 slide 46. A pipeline that has quietly throttled to nothing breaks that promise without breaking a single request.

Deployment is otherwise the standard shape: the chart carries the rwb-document login and no other credential (DP-02), the migration job runs the per-service Flyway sequence in schema `rwb_document` (DP-15), `rwb.document.events.v1` is reused with its retry and `.dlt` topics as RWB-PLT-N002-INF provisions them (DP-09), the outbox relay runs every minute (JOB-11), and the runbook names the four failures an operator will actually see.

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The Temporal workflow kit and the `rwb-recovery` namespace are available (RWB-PLT-WF, RWB-PLT-E1071-CON), so the worker polls `rwb-document` and the Schedule runs in every environment.
- The Kafka event platform provisions topics with a retry topic and a `.dlt` topic (RWB-PLT-EVT, RWB-PLT-TE006-CON), and `rwb.document.events.v1` is provisioned by RWB-PLT-N002-INF.
- The observability stack of the platform is available (RWB-PLT-OBS, ADR-023): metrics, traces and logs with one trace across REST, Kafka, Temporal and the file step.
- The three environments DEV, SIT and UAT exist with their parameter scope and their Kafka, Temporal and object-store endpoints.
- RWB-P5-E1049-CON is published, so the smoke profile runs against the four operations and the four fakes of that baseline.
- RWB-P5-E1049-INF has provisioned the engine capacity and its queue, the worker pool sizing, the intake and text containers, the secret, the identity and the private route.
- The engine endpoint, the deployment slot, the exact business-hours window and the alert thresholds are Not specified in the source documents (GAP-1001; ASM-1783).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The pipeline builds one image and one chart version from the same commit, runs the unit, component and contract tests, scans the image and the dependencies, and publishes the chart.
2. The chart deploys `rwb-document` with the rwb-document login, the pre-deploy migration job for schema `rwb_document`, the readiness and liveness probes, the api deployment and the worker deployment that polls `rwb-document`.
3. The worker carries the build ID of the release and registers `DocumentIntakeWorkflow` with its five activities `ingest`, `ocr`, `classify`, `extract` and `matchStep`; the three activities of other stories must resolve on the same queue and a missing registration fails readiness.
4. The Schedule registration step registers exactly one Schedule for legacy JOB-12 from the environment values: every 15 minutes in business hours, Asia/Bangkok, overlap SKIP, with the catch-up window of the workflow kit, and asserts that it starts `DocumentIntakeWorkflow`.
5. The same step records the retirement: no Quartz row, no shared job table entry and no Control-M job is registered for document intake.
6. The provisioning step reuses `rwb.document.events.v1` and `rwb.decision-record.v1` as their owners provision them, declares the consumer group that reads `rwb.document.events.v1`, and confirms that no topic is created by this release.
7. The outbox relay is deployed as the platform standard of JOB-11: every minute, one relay per service, with its lag and its dead-letter count exposed.
8. The dashboards are published: intake volume by run and by source, the OCR failure rate, the held items by reason and by age, the queue depth, the outbox lag and the workflow open, stuck and failed count.
9. The alerts are wired: a run failed twice, an engine error rate above its value, held items older than their value, a queue with no poller and a stuck workflow; each links exactly one runbook entry and each carries its message ID where one maps.
10. The feature flag `rwb.document.ocr` is set per environment and a smoke step runs the loop against the four fakes in SIT: 180 items into text, one item held for rescan, one item unreadable and one engine failure that raises the alert.
11. The runbook is published and reviewed with the on-call rota: a failed run, a held item, a re-run of a business date, a stuck workflow and an outbox relay that stopped.
12. The rollback path is rehearsed once in UAT and recorded in the runbook, together with the flag state of each environment.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The migration job fails | The deployment stays unready and the pipeline stops; no traffic reaches the new version | None | AC1 |
| X2 | The worker is deployed with the wrong build ID, or an activity of another story is not registered | The workflow run fails on the missing activity; the readiness check fails the release and the rollback restores the previous build | None | AC2 |
| X3 | The Schedule is registered twice, with overlap ALLOW, or outside business hours | The registration check fails the release; the duplicate is removed before promotion | None | AC3 |
| X4 | A run fails twice on the engine | The failed-run alert fires with MSG-GEN-006 naming the OCR service, and the engine runbook entry opens | MSG-GEN-006 | AC5, AC6 |
| X5 | The held items pass their age value, or their count rises while the run completes | The held-item alert fires with the reason and the oldest item, and the held-item runbook entry opens | None | AC5, AC6 |
| X6 | No worker polls `rwb-document`, or the queue depth rises while the runs complete | The no-poller alert fires and the queue runbook entry checks the scaler and the replica ceiling | None | AC2, AC5 |
| X7 | A workflow stops on a non-retryable failure | The stuck-workflow scan of JOB-21 raises the case and the stuck-workflow runbook entry starts from the history | None | AC5, AC6 |
| X8 | A read without the Documents right is refused | The refusal is counted on the dashboard and no page is raised | MSG-P4-002 | AC5 |
| X9 | The flag is off in an environment | The `ocr` activity is skipped, items stay PENDING and the reads still answer; the held-item panel shows the growth without an alert storm | None | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the Schedule registration, the topic set and the observability stack; builds no application code |
| Negotiable | Replica counts, resource sizes, thresholds, the business-hours window and the deployment slot are environment values, not story decisions |
| Valuable | Makes a pipeline with no job record observable: the run, the engine, the held items and the queue each have a signal, an owner and a runbook entry |
| Estimable | One chart, one Schedule registration, one provisioning step, one relay, six panels, five alerts, five runbook entries and one smoke profile |
| Small | Fits one sprint with the runbook and the smoke profile |
| Testable | Every criterion tests an artefact: the chart renders, the Schedule exists once, an alert fires on a synthetic metric, a runbook entry resolves, the smoke profile passes |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the OCR pipeline of rwb-document

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the target environment is SIT

  Scenario: AC1 The chart deploys rwb-document with the api and the worker that polls rwb-document (new, D-RCV-60)
    Given the rwb-document Helm chart and its values-dev.yaml, values-sit.yaml and values-uat.yaml
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the release declares the rwb-document login reference and no other service's credential
    Then the migration job runs the per-service Flyway sequence in schema rwb_document before the deployment is marked ready
    Then the worker deployment polls task queue rwb-document in namespace rwb-recovery with the build ID of the release, and the api deployment serves the four intake operations
    Then readiness answers healthy only when the migration is at the expected version, the outbox relay is running and the worker has polled
    Then no replica count, resource size, timeout, threshold or cadence is hard-coded in the template

  Scenario: AC2 DocumentIntakeWorkflow and its five activities are deployed and resolve on the queue (new, D-RCV-60)
    Given the deployed worker of this release
    When the queue rwb-document is inspected
    Then DocumentIntakeWorkflow is registered with the build ID of the release
    Then the activities ingest, ocr, classify, extract and matchStep resolve on the same queue
    Then a release that leaves one of the five activities unregistered fails the readiness check
    Then the workflow runs one business date with the input of RWB-P5-E1049-CON and writes the counts read, done, rescan and failed
    Then a run started by a hand-registered workflow is refused by the registration check

  Scenario: AC3 The 15-minute Schedule is registered from configuration and no Quartz row exists (new, D-RCV-60)
    Given the Schedule registration step of the release
    When it runs against the environment
    Then exactly one Schedule starts DocumentIntakeWorkflow every 15 minutes in business hours, Asia/Bangkok, with overlap SKIP and the catch-up window of the workflow kit
    Then the cadence and the window come from the environment values and are not written in a class or a script
    Then no Quartz row, no shared job table entry and no Control-M job is registered for document intake
    Then a release that registers a second Schedule, an overlap of ALLOW or a cadence other than the configured one fails the registration check
    Then the exact business-hours window is Not specified in the source documents (GAP-1001; ASM-1783)

  Scenario: AC4 The feature flag is set per environment and its off state is safe (new, D-RCV-60)
    Given the flag rwb.document.ocr and the Schedule state per environment
    When the flag is off in an environment
    Then the ocr activity is skipped, the items stay PENDING and the intake reads still answer
    Then the Schedule still ticks and starts the workflow, and the workflow completes with no item read
    Then the flag and the Schedule state are values-file entries, never code, and are recorded per environment
    Then turning the flag on in a fresh environment reads the pending items on the next tick without a second text row for any item

  Scenario: AC5 The dashboards and alerts cover intake volume, OCR failure rate and held items (new, D-RCV-60)
    Given the published dashboard and the five alert rules
    When a synthetic day is replayed with 180 items read, one item held for rescan, one unreadable item, one engine failure and a drained queue
    Then the panels show the intake volume by run and by source, the OCR failure rate, the held items by reason and by age, the queue depth, the outbox lag and the workflow open, stuck and failed count
    Then a run that fails twice raises its alert with MSG-GEN-006 naming the OCR service, and held items past their age raise their alert with the reason and the oldest item
    Then a queue with no poller raises its alert and a refused read is counted and never pages the on-call rota
    Then no panel or alert payload carries a page text, a file name with a customer value or a personal value
    Then the alert thresholds and the held-item age value are Not specified in the source documents (GAP-1001; ASM-1783)

  Scenario: AC6 The runbook covers a failed run, a held item and a re-run, and the rollback is rehearsed (new, D-RCV-60)
    Given the published runbook, the five alert conditions and the rollback rehearsal of UAT
    When an operator opens the entry a fired alert links
    Then the runbook holds one entry each for a failed run, a held item, a re-run of a business date, a stuck workflow and an outbox relay that stopped
    Then the re-run entry states how the run of a business date is started again without reading a DONE item a second time and without a second text row
    Then the held-item entry states how a RESCAN item reaches the review queue and how a case owner is notified again without a duplicate notice
    Then every entry names its check, the owner role, the recovery step and the escalation path when the step fails, and every alert links exactly one entry
    Then a rollback to the previous chart version restores the previous flag state and leaves the intake items, the text rows and the published events unchanged
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One service, one schema, one login: the release uses the rwb-document login and no other service's credential | DP-02; Architecture v5 slide 29 |
| BR2 | The migration is a per-service Flyway sequence in schema `rwb_document` and runs before the deployment is ready | DP-15; RWB-PLT-E1044-CON |
| BR3 | Every subscription has a retry topic and a `.dlt` topic, and a consumer never acknowledges an event it could not process | DP-09; Architecture v5 slide 22 notes |
| BR4 | The outbox relay runs every minute and is the platform standard of JOB-11; it is not rebuilt per story | Architecture v5 slide 44; DP-09 |
| BR5 | JOB-12 is a Temporal Schedule of this service; no Quartz row, no shared job table entry and no Control-M job is registered | DP-10; Architecture v5 slide 44 |
| BR6 | No environment value is hard-coded: replica counts, resource sizes, the business-hours window, thresholds and the flag state come from values files; the business-hours window, the alert thresholds and the deployment slot are set at the wave 1 entry check with the DevOps team | Template and Rules §R7.2 s17 |
| BR7 | An alert carries a message ID and the agreed text where one maps, and links exactly one runbook entry | Template and Rules §R7.2 s14 |
| BR8 | A refused read is counted and never pages the on-call rota | MSG-P4-002 |
| BR9 | A re-run of a business date never reads a DONE item twice and never writes a second text row for a page | legacy AC8, AC9; R-UNI-40 |
| BR10 | No dashboard series, log line or alert payload carries page text or personal data; intake IDs, document IDs, statuses, counts and durations only | Template and Rules §R7.2 s17 |
| BR11 | The pipeline's time promise is operational: every scan becomes text the same day and an unreadable page is sent back for rescan the same day | RWB-E1-049 story intent; FSD P5 A2.7.1 |

### 9. State transitions

The release and the Schedule move through these states; no business object moves.

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the migration job pass the pipeline | Deploying |
| Deploying | Migration complete and probes healthy | The schema is at the expected version, the relay runs and the worker polls `rwb-document` | Ready |
| Ready | Schedule registered | Exactly one Schedule exists and the retirement of the Quartz job is recorded | Armed |
| Armed | Release superseded | A new chart version is promoted | Rolling |
| Rolling | All pods on the new version | The old ReplicaSet drains and the worker build ID is the new one | Armed |
| Armed | Alert on a failed run, held items or a queue with no poller | The condition passes its value | Alerted; the runbook entry opens |
| Alerted | Re-run of the business date, or the owner's repair | The items move and the status is what the run wrote | Armed |
| Armed | Flag turned off | The `ocr` activity is skipped and the reads still answer | Armed, capability off |
| Armed | Rollback | The previous chart version and the previous flag state are restored | Armed on the previous version |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the Schedule registration, the dashboards, the alerts and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the topic set, the visibility queries behind JOB-21 and the re-run of a job on SCR-44 |
| ACE database administrator | Owns schema `rwb_document`, the login and its grants, and approves the migration job |
| OCR provider owner | Owns the engine endpoint, its quota and its availability window; is paged by the engine alert and owns the repair beyond the pipeline's client |
| Release manager | Approves the promotion of one artefact through the environments and the rollback |
| On-call operator | Runs the runbook entries and opens an incident when a failed run or a held-item spike persists |
| RW-PLATADM, platform administrator | Sees the run counts and the alerts on SCR-44 in the running service, not in the cluster |
| RW-CASEOWN, case owner | Receives the rescan notice of MSG-P5-018 for a held item of their case, through the running service |

The per-service login used by the chart is a secret reference resolved at deploy time; the chart references "the rwb-document login (DP-02)" and never a literal name. The deployment slot and the exact business-hours window are Not specified in the source documents (GAP-1001; ASM-1783).

### 11. Data

| Item | Content | BR Field ID |
|---|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, the flag `rwb.document.ocr`, the Schedule state and its business-hours window, the client timeouts, the alert thresholds | Not specified in the source documents (DOR-RWB-P5-E1049-OPS-7) |
| Schema | `rwb_document`, migrated by the per-service Flyway sequence; the tables `document_intake` and `document_text` with the library objects | Not specified in the source documents (DOR-RWB-P5-E1049-OPS-7) |
| Topic | `rwb.document.events.v1` with its three retry topics and its `.dlt` topic, reused as RWB-PLT-N002-INF provisions them; `rwb.decision-record.v1` reused as its owner provisions it | Not specified in the source documents (DOR-RWB-P5-E1049-OPS-7) |
| Queue | Temporal task queue `rwb-document` in namespace `rwb-recovery`, served by the worker of this release | Not specified in the source documents (DOR-RWB-P5-E1049-OPS-7) |
| Schedule | One document-intake Schedule, every 15 minutes in business hours, Asia/Bangkok, overlap SKIP, with the catch-up window of the kit | Not specified in the source documents (DOR-RWB-P5-E1049-OPS-7) |
| Dashboard series | Intake volume by run and by source, OCR failure rate, held items by reason and by age, queue depth, worker scale events, outbox lag, workflow open, stuck and failed, refusal rate | Not specified in the source documents (DOR-RWB-P5-E1049-OPS-7) |
| Runbook entries | Failed run, held item, re-run of a business date, stuck workflow, outbox relay stopped | Not specified in the source documents (DOR-RWB-P5-E1049-OPS-7) |
| Secrets | The rwb-document login secret, the engine credential reference, the storage identity, the Kafka client credential and the Temporal mTLS material, all from the platform key store | Not specified in the source documents (DOR-RWB-P5-E1049-OPS-7) |

The alert thresholds and the held-item age value are deployment values; their provisional values are carried by the gap and the assumption of section 14 (GAP-1001; ASM-1783). The exact cluster topology, node pools, replica counts and probe timings are deployment values of the platform chart and are not fixed here.

The four OCR parameters (OCR_MIN_QUALITY, OCR_WORKERS, OCR_TIMEOUT_SECONDS, OCR_MAX_ATTEMPTS) are held as data rows in the document hub parameter table, document_hub_parameter, and are read as data at run time. OCR_WORKERS is the worker concurrency cap; the platform scales workers on queue depth. The 60-minute target is kept.

The OCR engine capacity ceiling, the admission queue depth, the bytes per page and the container quota: Not specified in the source documents (GAP-1000). They are set at the capacity review with the OCR provider owner.

The eight rescan notice values (template code, version, language and body; the operational rescan notice type; the Notice answer properties of API-P6-002; the request and result of the ACE notification path; the recipient reference; the retry values; the state list): Not specified in the source documents (GAP-1204). Each placeholder stays until the row that publishes it closes at the baseline review.

Screen SCR-44 empty, loading, error and no access states: Not specified in the source documents (DOR-RWB-P5-E1049-OPS-10).

### 12. Contract

#### 12.1 REST operations provided

None. The deployment exposes the four operations of RWB-P5-E1049-CON behind gateway-bff: the intake submit, the intake item read, the text read and the OCR status read. The probes are cluster-internal and are not part of the API surface, and this story adds no path.

#### 12.2 REST operations consumed

None. The deployment configures the client timeouts and the breakers of the consumed rows declared in RWB-P5-E1049-CON and adds no call of its own.

#### 12.3 Events published

None. `rwb.document.OcrCompleted.v1` is RWB-P5-E1049-APP's; the deployment reuses `rwb.document.events.v1` with its retry and `.dlt` topics as provisioned by its owner and creates no topic.

#### 12.4 Events consumed

None declared. The subscription of the `ingest` activity to `rwb.document.events.v1` is provisioned in the step of section 13 and described in AC1 and AC2, and its shape belongs to RWB-P5-E1049-CON.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| `DocumentIntakeWorkflow` | Workflow, one run per Schedule tick and business date | `rwb-document` | Worker deployment with the build ID of the release; holds the five activities in order |
| `ingest` | Activity, P5 | `rwb-document` | Registered by the same worker; creates the intake item from `DocumentStored` |
| `ocr` | Activity, P5 | `rwb-document` | Registered by the same worker; selects and locks the pending items, calls the engine and writes the status and the text |
| `classify` | Activity, P5 | `rwb-document` | Registered by the same worker; owned by RWB-P5-E1050-APP |
| `extract` | Activity, P5 | `rwb-document` | Registered by the same worker; owned by RWB-P5-E1053-APP |
| `matchStep` | Activity, P5 | `rwb-document` | Registered by the same worker; owned by RWB-P5-E1032-APP |

Exactly one worker build serves the workflow and all five activities; a release that leaves one of them unregistered fails the readiness check of AC2.

Workflow ID: Not specified in the source documents (CG-ALL-5933). Start rule: the catalog names the starters as an event from the scanner folder, SFTP or mailbox pickup (JOB-12), or a child start from a stage workflow; the duplicate-start policy is Not specified in the source documents (CG-ALL-5933).

#### 12.6 Schedules

| Schedule | Cron | Overlap | What it starts |
|---|---|---|---|
| Document intake (legacy JOB-12) | Every 15 minutes in business hours, Asia/Bangkok, from the environment values | SKIP, with the catch-up window of the kit | `DocumentIntakeWorkflow` on `rwb-document` |

Exactly one Schedule is registered per environment, and no Quartz row, shared job table entry or Control-M job is created. The exact business-hours window is Not specified in the source documents (GAP-1001; ASM-1783).

#### 12.7 Tables owned

None. The migration job creates and migrates the tables of RWB-P5-E1049-APP in schema `rwb_document`; this story owns no table and adds no column. `document`, `document_type` and `document_hub_parameter` belong to their P5 stories and the migration job touches schema `rwb_document` only (DP-01).

#### 12.8 Contract fakes

None. The fakes are test-only workloads of RWB-P5-E1049-CON; the SIT smoke profile of section 13 runs against them and they are not deployed into UAT or production.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None | No operation is provided or consumed by the deployment itself |
| Kafka | None | No topic is created; the event and the consumed event ride `rwb.document.events.v1` with retry and `.dlt` |
| Temporal | 1 workflow, 5 activities, 1 Schedule | `DocumentIntakeWorkflow` with `ingest`, `ocr`, `classify`, `extract` and `matchStep` on `rwb-document`, and the 15-minute business-hours Schedule registered once per environment |
| File | 1 dotted grey path | The intake file read and the OCR JSON written at `ocr/{intakeId}.json`, through the storage product; the smoke profile asserts the path against the stub |

### 13. Solution plan

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-document/` | Chart with api and worker deployments, service, migration job, config map, secret references, probes and the Schedule registration hook |
| `helm/rwb-document/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, `rwb.document.ocr`, the Schedule state and its business-hours window, the client timeouts, the alert thresholds |
| Pipeline stage | Build, unit, component and contract tests, the retired-element check, image and dependency scan, chart publish, one artefact promoted through the environments |
| Schedule registration step | Exactly one document-intake Schedule, its cadence, its window, its overlap and its catch-up, plus the recorded retirement of the Quartz job |
| Provisioning step | The consumer subscription on `rwb.document.events.v1` with retry and `.dlt`; reuse of `rwb.document.events.v1` and `rwb.decision-record.v1`; task queue `rwb-document` in namespace `rwb-recovery` with all five activities registered |
| Outbox relay | The platform standard of JOB-11, one relay per service, with lag and dead-letter series |
| Dashboards | Six panels: intake volume, OCR failure rate, held items, queue depth and scale events, outbox lag, workflow health |
| Alerts | Five rules, each with a message ID where one maps, and one runbook entry |
| Runbook | Five entries: failed run, held item, re-run of a business date, stuck workflow, outbox relay stopped |
| Smoke profile | The SIT run of section 13's step 10 against the four fakes |

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H rows are delivered by the platform waves and are not repeated in the metadata H field, which stays empty. DP-10 is the pattern this story serves: the Schedule registration and the worker deployment are the operational form of "no shared Quartz", and the retired-element check proves that no Quartz row survives the release. DP-09 is the failure path of the event, DP-15 the migration the release runs, and DP-19 the route the four operations are read through. DP-01, DP-06, DP-07, DP-11 and DP-13 add no work here: they are the shapes the deployment carries.

**Probes.** Readiness answers healthy only when the migration is at the expected schema version, the outbox relay is running, the Temporal worker on `rwb-document` has polled and all five activities are registered; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database and neither calls another service or the OCR engine.

**Alert mapping**

| Message ID | Condition | Alert | Route |
|---|---|---|---|
| MSG-GEN-006 | A run fails twice on the engine, or the engine error rate passes its value | Failed-run alert with the run, the business date, the failed count and the engine endpoint reference | Platform on-call, page; ticket to the OCR provider owner and the rwb-document owner |
| MSG-P4-002 | A read without the Documents right is refused | Refusal count on the dashboard | No page |
| None | Held items past their age value, or their count rising while the runs complete | Held-item alert with the reason, the count and the oldest item | Platform on-call, page; the held-item runbook entry |
| None | No worker polls `rwb-document`, or the queue depth rises while the runs complete | No-poller or queue-depth alert with the backlog and the scale events | Platform on-call, page |
| None | The outbox lag passes its value, or the dead-letter count rises | Relay alert with the lag and the oldest row | Platform on-call, page |
| None | The stuck-workflow scan of JOB-21 raises a `rwb-document` workflow | Stuck-workflow alert with the workflow ID, the business date and the last event | Platform on-call, page |

Every alert carries its message ID where the condition maps to one, and the conditions without one carry the series or the workflow name instead. The thresholds and the held-item age are deployment values with provisional defaults; the missing source is carried by the gap and the assumption of section 14 (GAP-1001; ASM-1783).

**Done when.** The chart renders for the three environments and the migration job runs before the pods are ready; the worker serves `DocumentIntakeWorkflow` with all five activities; exactly one Schedule exists and no Quartz row survives; the flag is off and on in the expected environments and the off state is safe; the six panels and five alerts answer a synthetic day, including a failed run with MSG-GEN-006 and a held-item spike; the five runbook entries resolve and each alert links exactly one; the smoke profile passes against the four fakes; the rollback has been rehearsed once in UAT after a business-hours run that read 180 items and held one for rescan.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-006 | The engine did not answer, a run failed twice, or a consumed call failed | {system} is not available. Your request is queued and will be retried. |
| MSG-P5-018 | A held item of a known case is notified again after a re-run | Page {page} of {document} on case {case} could not be read. Scan it again and send it to the document hub. |
| MSG-P4-002 | A role without the Documents right reads an item | You cannot {action} here. Your role does not include it. |

MSG-P5-018 and MSG-P4-002 are the legacy messages copied unchanged; MSG-GEN-006 is the unavailability shape the alert of a failed run uses, naming "OCR service". Thai text for each message follows decision DL10.

Delivery shape: the alert payload carries the message ID where one maps, the environment, the business date, the run identifier, the counts and the runbook path; it never carries a page text, a file name with a customer value or a personal value.

### 15. Screens and states

No Workbench screen in this story. The operator surfaces are the workbook "Document intake" (six panels and the alert list) and SCR-44 Interface and job monitor, which shows the same run counts in the running service. The four states the operator reads are Running, Complete, Failed and Waiting, as defined by the app story; the deployment adds the flag state and the Schedule state per environment, which are configuration and not a screen state. Empty, loading, error and no access states of SCR-44: Not specified in the source documents (CG-ALL-5940).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P5-E1049-OPS-01 | AC1 | Component | The chart rendered for DEV, SIT and UAT with the login reference, the migration job and the api and worker probes |
| TC-P5-E1049-OPS-02 | AC2 | Integration | One business date run with all five activities registered; one release with `extract` unregistered, which fails readiness |
| TC-P5-E1049-OPS-03 | AC3 | Component | The Schedule registration in SIT; one Schedule, overlap SKIP, the configured cadence, and the retirement check finding no Quartz row |
| TC-P5-E1049-OPS-04 | AC4 | Component | The flag off and on in SIT; items PENDING while off, read on the next tick while on, no second text row |
| TC-P5-E1049-OPS-05 | AC5 | End to end | A synthetic day: 180 items read, one held for rescan, one unreadable, one engine failure, one drained queue |
| TC-P5-E1049-OPS-06 | AC6 | NFR | The five runbook entries resolving from their alerts, and a rollback rehearsal in UAT after a business-hours run |
| TC-P5-E1049-OPS-07 | AC2 | Contract | The operations, events and activities of section 12 checked against Temporal Catalog v1 and the topic set, including the start rule of DocumentIntakeWorkflow |

### 17. Guardrails

- No business value in code: thresholds, the held-item age, the business-hours window, the replica counts and the flag state are values-file entries.
- No personal data in logs, metrics, alerts, tests or prompts; the run record and the dashboards hold intake IDs, document IDs, statuses, counts, durations and role names only, and never a page text.
- No read of another service's tables and no read of a table in schema `public`; the case owner comes through the owner's contract and no ACE view is read by this service.
- A runbook names roles and service identities, never a person.
- No runbook describes a hand-registered Schedule, a Quartz row or a Control-M job; the Schedule is registered from configuration only.
- No secret, credential or connection string appears in a runbook, a dashboard panel or an alert payload; each is a secret reference.
- The re-run path never reads a DONE item twice and never writes a second text row for a page; the guard is the status predicate and the unique page index of the app story.
- The flag removes the capability without a rollback of the schema, and the rollback restores the previous flag state with the previous chart version.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| NFR-067 | Every scheduled job has a run book, monitoring and an alert to the operations channel | The five runbook entries and the five alert rules | TC-P5-E1049-OPS-05, TC-P5-E1049-OPS-06 |
| NFR-068 | A failing interface, job or agent raises an alert to a named owner within its target | The alert mapping of section 13 and the failed-run alert with MSG-GEN-006 | TC-P5-E1049-OPS-05 |
| RWB-E1-049 AC2 | 500 pages in 125 items reach DONE or RESCAN within 60 minutes with 4 workers | The worker build, the five activities and the Schedule that starts the run | TC-P5-E1049-OPS-02, TC-P5-E1049-OPS-05 |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz | The Schedule registration and the retirement check | TC-P5-E1049-OPS-03 |
| ADR-023 | Observability per service | The six panels, the five alerts and the runbook entries | TC-P5-E1049-OPS-05, TC-P5-E1049-OPS-06 |
| DP-15 | Per-service Flyway and migration ownership | The pre-deploy migration job in schema `rwb_document` | TC-P5-E1049-OPS-01 |

The legacy key is RWB-E1-049; its AC1 to AC9 are owned by RWB-P5-E1049-APP, its contract by RWB-P5-E1049-CON and its capacity by RWB-P5-E1049-INF. This story proves that the same pipeline runs, is watched and is repairable in an environment.

### 19. Out of scope

- The pipeline, its activities and the engine client: RWB-P5-E1049-APP.
- The contract baseline and its fakes: RWB-P5-E1049-CON.
- The engine capacity, the containers, the secret and the private route: RWB-P5-E1049-INF.
- The Kafka topic set and its ACL model: RWB-PLT-N002-INF.
- The SCR-44 screen and incident handling after a job failure: Epic 2 and Epic 8.
- The other Epic 1 job run books and the platform workbook: RWB-PLT-E1056-OPS.
- The OCR engine's own availability and quota management, which belong to the OCR provider owner.
