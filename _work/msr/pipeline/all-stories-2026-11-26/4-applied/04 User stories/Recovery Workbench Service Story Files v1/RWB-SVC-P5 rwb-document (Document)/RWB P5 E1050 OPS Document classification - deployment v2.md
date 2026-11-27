# RWB-P5-E1050-OPS Document classification

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1050-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-050 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP10, DP11, DP15, DP19 |
| Parallel lane | L-P5-N |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-015, FR-P5-017, FR-P5-018) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-050 for `rwb-document`; the classification capability is deployed as the api and worker of the service with its own login and migration job, a pinned and promoted classifier artefact, the configuration and parameter reads, the feature flag, its participation in the 15-minute intake Schedule, the confidence and review-reason dashboards, the alerts of the legacy story and the runbook with the model rollback. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P5-E1050-OPS). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **DevOps engineer**, I want **rwb-document's classification capability deployed from the service template with its own login and migration job, the classifier and its model artefact pinned, promoted and rollback-able by version, the three parameters and the type table read from data, a feature flag that can switch the capability off, its participation in the 15-minute intake Schedule, dashboards for the confidence distribution and the review reasons, the alerts of the legacy story and a runbook that names each entry**, so that **every environment classifies on the same artefact version, an operator can see a model that has drifted or stopped answering before a reviewer drowns in the queue, and one person can roll the model or the release back without a build**.

### 2. Business rationale

In the legacy story classification is a Quartz step and an in-process adapter inside one deployable: the model version is a string in a column, the threshold is a row an administrator edits, and the only signal that the model has drifted is a review queue that grows. In the target the step runs in the `rwb-document` worker on the Temporal queue, the model is one artefact among the release's artefacts, and the 15-minute intake Schedule that starts it belongs to RWB-P5-E1049-APP (DP-10). Deployment is therefore part of the capability: an unpinned model means two environments classify differently on the same document, a missing parameter read means the step either guesses a threshold or stops the whole intake, and a dashboard without the confidence distribution means nobody sees a model that has started answering the same low score to everything until the review queue is the size of the day's scans.

The story also carries the guard that has to be visible in operations. BR5 of the app story makes 162 of 180 the release gate of the model, and BR6 keeps the PII masking in front of every call; both are only real if the pipeline refuses a promotion without an evaluation report and the runbook says what to do when the masking service, the parameters contract or the model does not answer. This story makes those two guards deployable and observable, so the app story can be proven in SIT and the on-call rota can operate it.

### 3. Preconditions

- The service template, chart skeleton and pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB, RWB-PLT-N004-OPS).
- The Temporal workflow kit and the `rwb-recovery` namespace are available (RWB-PLT-WF, RWB-PLT-E1071-CON), and the intake workflow and its 15-minute Schedule are registered by RWB-P5-E1049-APP.
- The Kafka event platform provisions topics with a retry topic and a `.dlt` topic (RWB-PLT-EVT, RWB-PLT-TE006-CON), and `rwb.document.events.v1` already exists for the store and extraction events.
- The observability platform provides the dashboard, the alert rules and the runbook link convention (RWB-PLT-OBS, RWB-PLT-N005-OPS, ADR-023).
- The storage product behind the evaluation report is available through the service's configured storage client (the platform storage product, reached by managed identity); the container and account are Not specified in the source documents (GAP-1004; ASM-1791).
- RWB-P5-E1050-CON and RWB-P5-E1050-APP are baselined and buildable, so the chart, the values and the dashboards render from published names rather than from a local choice.
- The three parameters `CLASSIFY_THRESHOLD` 0.80, `CLASSIFY_MAX_PAGES` 3 and `CLASSIFY_TIMEOUT_SECONDS` 60 are reference rows of the environment, loaded through the rwb-case parameters contract (DP-06).
- The type table version DOCTYPE-2026.11 is loaded and approved through RWB-P5-E1025-APP.
- The classifier provider and its model version, and the way a model artefact is produced, are Not specified in the source documents (GAP-1002; ASM-1795).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).
- No approval of this deployment story was available in this run, so it is carried as Status Draft (realignment v1) with the release 30 November 2026 unchanged and marked tentative (ASM-1788).

### 4. Flow

1. The pipeline builds the service image, runs the unit and contract tests, scans the image and the dependencies, and publishes one Helm chart version and one classifier artefact version from the same commit.
2. The chart deploys an api workload and a worker workload with the `rwb_document` login, the migration job on the service's own Flyway sequence and the probes; the migration job runs before the deployment is marked ready.
3. The release pins the classifier artefact by digest and records the pair (chart version, classifier artefact version) in the release record; the artefact identifier is what the step writes into `classifier_version`.
4. The evaluation gate reads the report of `evaluation/classification/{runDate}.json`; a report below 162 of the 180 labeled documents, or a report whose model version differs from the pinned artefact, blocks the promotion.
5. The configuration step confirms the three parameter rows, the type table version in force, the property `classify.model-route` and the feature flag `rwb.document.classify`.
6. The worker joins the intake Schedule: it polls queue `rwb-document`, and its `classifyStep` runs as one step of `DocumentIntakeWorkflow` started by the 15-minute Schedule that RWB-P5-E1049-APP registers; this story registers no Schedule of its own.
7. KEDA scales the worker on the depth of the intake queue and on the running workflow count, so a morning scan burst does not age the review queue.
8. The dashboards are published: classified items, the confidence distribution, the review reasons, the fallback count, the masking failures, the evaluation accuracy and the artefact version in force.
9. The alerts are wired to the message IDs of section 14 and to the runbook entries, and the threshold values behind them are values entries, not code.
10. The runbook is published with its entries: a model that stops answering, a review queue that grows, a masking failure, a parameter read failure, a migration failure, a probe failure and a rollback to the previous model version.
11. A smoke step classifies one synthetic intake item in SIT, checks the answer against the classifier stub, and confirms that the artefact version of the answer equals the version the release pinned.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The migration job fails | The deployment stays unready and the pipeline stops; no traffic to the new version | None | AC1 |
| X2 | The readiness probe fails after the start-up window | The pod leaves the service and the pipeline marks the release failed | None | AC1 |
| X3 | The chart is rendered without a pinned classifier artefact or image digest | The pipeline fails the release before the deployment step | None | AC1, AC2 |
| X4 | The evaluation report is missing, below 162 of 180, or names another model version | The promotion is blocked and the previous artefact stays in force | None | AC2 |
| X5 | The parameters contract does not answer, or a parameter row is absent | The step writes no classification; the item stays unclassified for the next run and the alert fires | MSG-GEN-006 | AC3, AC5 |
| X6 | The feature flag is off | `classifyStep` is skipped, no classification is written and every scanned item goes to review at attach | MSG-P5-003 | AC3, AC5 |
| X7 | The intake Schedule fires while the previous run is still open | The run is skipped by the overlap policy; the skip is counted on the dashboard and never alerted | None | AC4 |
| X8 | The review share or the unknown-type share crosses its threshold | The drift alert fires with the window, the share and the artefact version, and the runbook entry is opened | MSG-P5-003 | AC5 |
| X9 | The masking service fails before a model call | No call is made, the item stays with `ocr_status` DONE, and the masking-failure alert fires | MSG-GEN-006 | AC5, AC6 |
| X10 | A rollback is requested | The previous (chart, classifier artefact) pair is redeployed, the flag stays on and the version in force is shown on the dashboard | None | AC2, AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the platform topic provisioned for the service, the workflow kit and the observability platform; the step itself is the app story's |
| Negotiable | Replica counts, resource sizes, KEDA thresholds, alert shares and windows are environment values, not story decisions |
| Valuable | Makes the classification capability deployable, observable and repeatable, and makes a drifted or silent model impossible to miss |
| Estimable | One chart with two workloads, one pipeline stage, one migration job, two probes, one artefact pinning and promotion step, one configuration step, two dashboards, five alert rules and one runbook set |
| Small | Fits one sprint with the runbook |
| Testable | Every criterion tests an artefact: the chart renders, the probes answer, the artefact pair is pinned, the parameters are read, the flag is proven off and on, the worker joins the Schedule, the alerts fire on a synthetic series |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the rwb-document classification capability

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the target environment is SIT and the namespace is rwb-recovery
    Given the document type table version "DOCTYPE-2026.11" is in force in rwb_document

  Scenario: AC1 The chart deploys the api and the worker, the migration job and the pinned classifier artefact (new, D-RCV-60)
    Given the rwb-document Helm chart and its values files
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version, the image digest and the classifier artefact digest pinned
    Then it declares one api workload and one worker workload, each with a readiness and a liveness probe
    Then it declares the rwb_document login and no other service's credential
    Then the migration job runs the per-service Flyway sequence in schema rwb_document before the deployment is marked ready
    Then the worker polls the queue rwb-document in namespace rwb-recovery and registers the classifyStep and evaluateClassifier activities
    Then no replica count, resource size, KEDA threshold, alert share or evaluation path is hard-coded in the template

  Scenario: AC2 The classifier artefact is versioned, promoted and rollback-able and the evaluation gate blocks a bad model (new, D-RCV-60)
    Given the release record of a build
    When the promotion runs from SIT to UAT and from UAT to production
    Then each promotion carries the same (chart version, classifier artefact version) pair and rebuilds neither
    Then the classifierVersion written on a classified intake item equals the artefact version the release pinned
    Then a promotion with a missing evaluation report, a report below 162 of the 180 labeled documents, or a report naming another model version is refused and the previous artefact stays in force
    Then a rollback redeploys the previous pair, leaves the feature flag on, and the dashboard shows the artefact version in force after the rollback
    Then the rollback takes no schema change and no data migration

  Scenario: AC3 The configuration, the parameter reads and the feature flag are in force (new, D-RCV-60)
    Given the parameter rows, the type table version in force, the property classify.model-route and the feature flag rwb.document.classify
    When the environment is provisioned
    Then CLASSIFY_THRESHOLD 0.80, CLASSIFY_MAX_PAGES 3 and CLASSIFY_TIMEOUT_SECONDS 60 are read through the rwb-case parameters contract and no value appears in a values file, a class or a test
    Then the type codes come from document_type in the version in force and no code list appears in a values file
    Then with the feature flag on a synthetic item is classified
    Then with the feature flag off no classification is written, the item is left unclassified, and the review guard of the app story routes it to review with review_reason LOW_CONFIDENCE
    Then the flag state is visible on the classification dashboard and no restart is needed to change it

  Scenario: AC4 The worker joins the 15-minute intake Schedule and scales without a second Schedule (new, D-RCV-60)
    Given the intake Schedule registered by RWB-P5-E1049-APP and the worker deployment of this release
    When the Schedule fires every 15 minutes in business hours
    Then the worker runs the classifyStep of DocumentIntakeWorkflow for the selected items and this release registers no Schedule of its own
    Then a second run for the same business date and the same open workflow is skipped by the overlap policy and the skip is counted
    Then KEDA scales the worker out on the intake queue depth and back in when the queue is empty
    Then a run that ends with unclassified items leaves them for the next run and the queue age is on the dashboard

  Scenario: AC5 The dashboards and the alerts cover the confidence distribution and the review reasons (new, D-RCV-60)
    Given the published dashboards and alert rules
    When a synthetic window is replayed with a low-confidence share, an unknown-type share, a fallback, a masking failure and a low evaluation result
    Then the confidence distribution series shows the buckets of the answered scores and the artefact version in force for the same window
    Then the review-reason series shows LOW_CONFIDENCE, MODEL_UNAVAILABLE and UNKNOWN_TYPE separately, and the fallback count matches classify_fallback true
    Then the review-share and unknown-type-share alerts fire above their values with the window, the share and the artefact version, and carry MSG-P5-003
    Then the model-unavailable and masking-failure alerts fire with MSG-GEN-006 naming the dependency
    Then the evaluation series shows the accuracy of the last run against the 162 of 180 gate and names the model version it measured
    Then every alert links one runbook entry and no alert payload carries OCR text, a candidate list or a personal value

  Scenario: AC6 The runbook and the rollback cover the legacy signals (new, D-RCV-60)
    Given the published runbook for the classification capability
    When an operator follows it for a model that stops answering, a review queue that grows, a masking failure, a parameter read failure, a migration failure and a probe failure
    Then each entry names the check, the role, the recovery step and the message ID the screen shows
    Then the model-unavailable entry ends in the rollback to the previous classifier artefact version, and the rollback is proven in SIT
    Then the queue-growth entry names the confidence distribution and the review-reason series as its evidence and the artefact version as its comparison
    Then no entry names a person, a secret, a credential or an OCR text sample
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One service, one schema, one login: the release uses the `rwb_document` login and no other service's credential | DP-02; Architecture v5 slide 29 |
| BR2 | The migration is a per-service Flyway sequence in schema `rwb_document` and runs before the deployment is ready | DP-15; RWB-PLT-E1044-CON |
| BR3 | The topic `rwb.document.events.v1` carries a retry topic and a `.dlt` topic, and the release never recreates the topic the store and extraction events already use | DP-09; Architecture v5 slide 11 |
| BR4 | The classify step is a step of the intake Schedule that RWB-P5-E1049-APP registers: this release adds no Schedule, no cron entry and no job name | DP-10; Architecture v5 slide 44 JOB-12 |
| BR5 | No environment value is hard-coded: replica counts, resource sizes, KEDA thresholds, alert shares and windows come from values files and parameters | DP-06; Template and Rules §R7.2 s17 |
| BR6 | The classifier artefact is pinned by digest, promoted as one (chart, artefact) pair and rolled back as one pair; a rebuild between environments is not allowed | Architecture v5 slide 11 notes; Template and Rules §R5.7 |
| BR7 | A promotion requires an evaluation report of at least 162 of 180 correct that names the pinned model version | Legacy BR5; FEAT-AGT-04 |
| BR8 | The three parameters and the type table are data: the threshold 0.80, the page bound 3, the timeout 60 and the six type codes are rows, never values | DP-06, DP-07; legacy BR3 and AC9 |
| BR9 | The feature flag `rwb.document.classify` removes the capability without a schema rollback; with the flag off every scanned item routes to review | Legacy section 13; ASM-1790 |
| BR10 | No personal data in a log, a dashboard series, an alert payload or the runbook: type codes, reasons, scores, counts, versions and durations only | CTL-11; DL26; ADR-023 |
| BR11 | An alert carries a message ID and the agreed text, and links one runbook entry | Template and Rules §R7.2 s14 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart and artefact published | The image, the chart, the classifier artefact and the migration job pass the pipeline | Deploying |
| Deploying | Migration job complete and probes healthy | The schema is at the expected version and both probes answer | Ready |
| Ready | Evaluation gate passed and promotion approved | The report is at least 162 of 180 and names the pinned version | Promoting |
| Promoting | Previous ReplicaSet drained | The new pair serves and the Schedules are unchanged | Ready, pair in force |
| Ready | Flag off | An operator takes the capability out of service | Ready, capability dark |
| Ready, capability dark | Flag on | The cause is cleared and the smoke item classifies | Ready, capability live |
| Ready | Model drift or model unavailable | The review share or the fallback alert fires | Degraded |
| Degraded | Rollback | The previous (chart, artefact) pair is redeployed and the smoke item classifies on it | Ready, previous pair in force |
| Ready or Degraded | Migration job failed | The schema is not at the expected version | Failed |
| Failed | Rollback | The previous chart version is redeployed and the migration is reversed by its own script | Ready |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the artefact pinning and promotion step, the configuration step, the dashboards, the alerts and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the topic provisioning, the Schedule registration rights that RWB-P5-E1049-APP uses, and the feature flag |
| ACE database administrator | Owns the `rwb_document` schema, the login and its grants, and approves the migration job |
| Release manager | Approves the promotion of one (chart, artefact) pair through the environments |
| Data steward (RW-DATASTEW) | Receives the drift alert; confirms the parameter rows behind the threshold, the page bound and the timeout |
| RW-COE, center of excellence analyst | Runs the evaluation and confirms the report the gate reads |
| RW-RISK, risk and model risk officer | Approves a model change before the production promotion |
| On-call operator | Runs the runbook entries and opens an incident when a drift, a fallback or a masking failure persists |

The per-service login name used by the chart is Not specified in the source documents (GAP-1004; ASM-1795); the chart references "the `rwb_document` login (DP-02)" through a secret reference and never a literal name.

### 11. Data

| Item | Content |
|---|---|
| Deployment values | Image digest, chart version, classifier artefact version and digest, replica counts of the api and the worker, KEDA thresholds, resource requests and limits, probe paths and timings, log level, alert shares and windows, feature switches |
| Schema | `rwb_document`, migrated by the per-service Flyway sequence; `document_intake`, `document_text`, `document_type`, `document_hub_parameter` and the library objects |
| Parameters | `CLASSIFY_THRESHOLD` 0.80, `CLASSIFY_MAX_PAGES` 3, `CLASSIFY_TIMEOUT_SECONDS` 60, read through the rwb-case parameters contract (DP-06) |
| Reference data | LOV-INTAKE-REVIEW and LOV-DOC-TYPE through the reference-data contract (DP-07); the type table version DOCTYPE-2026.11 read from `document_type` |
| Topic | `rwb.document.events.v1` with its retry and `.dlt` topics; `rwb.decision-record.v1` is not used by this capability |
| Queue | Temporal task queue `rwb-document` in namespace `rwb-recovery` |
| Schedules | None registered here; the 15-minute intake Schedule is RWB-P5-E1049-APP's |
| Dashboard series | classified items, confidence distribution, review reasons by value, fallback count, masking failures, queue age, evaluation accuracy, artefact version in force, flag state, skipped runs, workflow failures |
| Runbook entries | model unavailable, model drift, review queue growth, masking failure, parameter read failure, migration failure, probe failure, flag left off, rollback to the previous model version |
| Secrets | The `rwb_document` login secret, the Kafka client credential, the Temporal mTLS material and the model endpoint credential, all from the platform secret store |

The classification columns the dashboards count are the ones the app story writes: `predicted_type`, `classification_confidence` numeric(5,4), `type_candidates`, `classifier_version` varchar(40), `classify_fallback` boolean and `review_reason` varchar(20) (GAP-1004; ASM-1796), so a series never counts a value the step does not write. The deployment topology detail (cluster names, node pools, replica counts, resource sizes, zone spread, ingress class, probe timings, KEDA thresholds, alert shares and windows) is Not specified in the source documents (GAP-1004; ASM-1796); the chart exposes them as values and this story fixes only their names and the rule that they are not hard-coded.

### 12. Contract

#### 12.1 REST operations provided

The deployment exposes the two operations of RWB-P5-E1050-CON behind gateway-bff: `POST /api/recovery/document/v1/intake-items/{intakeItemId}/classify` and `GET /api/recovery/document/v1/intake-items/{intakeItemId}/classification`, owner rwb-document (P5). It also serves the review list of API-P5-010 and the document read of API-P5-003, which RWB-P5-E1049-APP and RWB-P5-E1024-APP declare. The probes are cluster-internal and are not part of the API surface.

#### 12.2 REST operations consumed

| Method | Path | Owner | Deployment need |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/parameters/{paramCode}` | P3 rwb-case | The three classification parameters; 2 s client budget (DP-06, DP-11) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-INTAKE-REVIEW and LOV-DOC-TYPE (DP-07, DP-11) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The access decision behind the classification-state read; 2 s client budget (DP-11) |

#### 12.3 Events published

| Event | Topic | Provisioning |
|---|---|---|
| `rwb.document.DocumentClassified.v1` | `rwb.document.events.v1` | The topic, its retry topic and its `.dlt` topic already exist for the store and extraction events; this release adds the class, the schema subject and the outbox relay configuration |

#### 12.4 Events consumed

| Event | Topic | Provisioning |
|---|---|---|
| None | None | The capability is a workflow step; it creates no consumer group and subscribes to no topic |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| `DocumentIntakeWorkflow` | Workflow, owned by RWB-P5-E1049-APP | `rwb-document` | The worker deployment registers the build ID of the release; this story changes no workflow definition |
| `classifyStep` | Activity | `rwb-document` | Registered by the worker; the step this story deploys |
| `evaluateClassifier` | Activity | `rwb-document` | Registered by the worker; started on demand for the gate report |

#### 12.6 Schedules

| Schedule | Cadence | Registration | Legacy reference |
|---|---|---|---|
| The document-intake Schedule, which carries the classify step | Every 15 minutes in business hours, overlap policy SKIP | Registered by RWB-P5-E1049-APP and observed by this release; this story registers nothing | The legacy JOB-12 step classifyStep |

#### 12.7 Tables owned

| Table | Owner | Deployment element |
|---|---|---|
| `document_intake`, `document_text`, `document_type`, `document_hub_parameter` | P5 (`rwb_document`) | Created by the per-service Flyway sequence in the migration job; this release adds the five classification columns to `document_intake` |
| outbox_event, processed_event and the idempotency table | PLT library, created in `rwb_document` | Created by the same migration job; used by the relay and the step |
| `document`, `document_field` | P5 (`rwb_document`) | Not migrated here; the classification columns of the stored document are written by the store and attach |

No table of another service is created, read or granted (DP-01).

#### 12.8 Contract fakes

| Fake | Deployment use |
|---|---|
| rwb-case parameters WireMock | Runs in the pipeline and the SIT smoke profile so the release can start without `rwb-case`, carrying 0.80, 3 and 60 |
| rwb-case reference-data WireMock | Same, carrying LOV-INTAKE-REVIEW and the six type codes |
| classifier stub | Same, answering the fixed scores so the smoke step proves the artefact pair before the real model is reachable |
| PII masking stub | Same, so the masking path is exercised without the ACE common module in a developer environment |

The fakes are test-only workloads; they are not deployed into UAT or production.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided and 2 referenced, 3 consumed in the deployment path | The classify command and the read; the review list and the document read belong to the neighbouring stories; the parameters, list and authorise reads; one hop, 2 s |
| Kafka | 1 published, 0 consumed | `rwb.document.events.v1` with retry and `.dlt`; no decision-record topic for this capability |
| Temporal | 1 workflow observed, 2 activities registered, 0 Schedules | `DocumentIntakeWorkflow` observed on `rwb-document`; the Schedule is RWB-P5-E1049-APP's |
| File | 1 report | `evaluation/classification/{runDate}.json` through the service's storage client; container and account Not specified (GAP-1004; ASM-1791) |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The seven rows are the patterns the legacy RWB-E1-050 carries. DP-10 is the substantive one for a deployment: the legacy Quartz step is now a step of a workflow that another story's Schedule starts, so this release must deploy a worker that polls the same queue and registers the two activities, and must register no Schedule of its own or the intake would run twice. DP-06 and DP-07 keep the threshold, the page bound, the timeout and the reason set out of the values files: the environment provisions rows, and AC3 proves that a value change needs no release. DP-01 and DP-15 keep the release inside `rwb_document` and its own sequence, so the migration job needs no grant elsewhere. DP-11 fixes the three consumed reads to one hop with a 2 s client budget and a fake, and DP-19 is the route the classification-state read answers through. The platform H dependencies are wave 0 contracts published before this story starts under the Day-1 rule (§R5.7) and are therefore not repeated in the metadata row, which stays None.

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-document/` | Chart with the api and worker deployments, service, migration job, config map, secret references, probes, KEDA scaler and the artefact-pinning values |
| `helm/rwb-document/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, classifier artefact version and digest, replicas, resources, KEDA thresholds, probe timings, log level, alert shares and windows, feature switches, environment name |
| Pipeline stage | Build, unit and contract tests, image and dependency scan, chart publish, classifier artefact publish, evaluation gate, promote the same pair |
| Evaluation gate | Reads `evaluation/classification/{runDate}.json`, refuses below 162 of 180 or a report naming another version, and records the pair in the release record |
| Provisioning step | The schema subject and the outbox relay configuration for `rwb.document.DocumentClassified.v1` on the existing topic with its retry and `.dlt` topics; the queue `rwb-document` is asserted, not created |
| Configuration step | The three parameter rows, the type table version in force, the property `classify.model-route` and the flag `rwb.document.classify` |
| Dashboards | Classified items, confidence distribution, review reasons, fallback count, masking failures, queue age, evaluation accuracy, artefact version, flag state, skips, workflow failures |
| Alerts | Five rules, each with a message ID and one runbook entry |
| Runbook | Nine entries: model unavailable, model drift, review queue growth, masking failure, parameter read failure, migration failure, probe failure, flag left off, rollback to the previous model version |

**Probes.** Readiness answers healthy only when the migration is at the expected schema version, the outbox relay is running and the Temporal worker has polled; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database and neither calls the model. Exact paths and timings are values.

**Migration job.** Runs the per-service Flyway sequence for schema `rwb_document` with the `rwb_document` login, as a pre-deploy job with a backoff limit; a failed job blocks the rollout and the release. The classification step is `V1050_1__intake_classification.sql`, one step of that sequence; the job replays no legacy monolith script.

**Model artefact policy.** The classifier artefact is versioned with the release, pinned by digest in the values, and promoted as one (chart, artefact) pair; the version string it reports is what the step writes into `classifier_version`, so the column, the dashboard and the release record agree. A rollback redeploys the previous pair and needs no schema change, because the six classification columns are unchanged between model versions. How the artefact is produced, and who produces it, is Not specified in the source documents (GAP-1002; ASM-1795).

**Alert mapping carried over from the legacy story.**

| Message ID | Condition | Alert | Route |
|---|---|---|---|
| MSG-P5-003 | The review share crosses its value, or the unknown-type share crosses its value | Drift alert with the window, the share, the reason and the artefact version | Data steward queue, ticket |
| MSG-GEN-006 | The model does not answer, or the masking service or the parameters read fails | Dependency alert naming the failing system and the trace identifier | Platform on-call, page |
| None (evaluation gate) | The evaluation report is below 162 of 180 or names another model version | Gate alert in the pipeline and in the dashboard | Release manager, ticket |
| None (fallback count) | The fallback count rises above its value in one window | Fallback alert with the artefact version | Platform on-call, ticket |

The legacy message texts are copied unchanged; the deployment adds the routing and the runbook link, never a new wording. The legacy story's own signal to the reviewer is carried by SCR-31 and MSG-P5-003, not by a second alert.

**Capacity.** The worker is sized on the intake volume and the page bound, not on the case volume: one `classifyStep` per selected intake item, one model call per item and one evaluation run on demand, with the extraction and attach steps of the neighbouring stories sharing the same queue. The per-environment capacity (replica counts, KEDA thresholds, resource requests and limits, alert shares and windows) is a values entry, and its numbers are Not specified in the source documents (GAP-1004; ASM-1796).

**Done when.** The chart renders in all three environments, the pipeline promotes one (chart, artefact) pair, the probes answer, the topic and its dead-letter path are verified by a test, the worker joins the 15-minute Schedule with no Schedule of its own, the flag is proven off and on, the five alerts fire on synthetic series, the model rollback is proven in SIT, and the runbook entries are reviewed by the on-call rota.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-003 | Items are held for type review, or the review share alert fires | Some fields need checking. The document is in the review queue. |
| MSG-GEN-006 | The model, the masking service or the parameters read does not answer | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | The classification-state read is called without the Documents right | You cannot {action} here. Your role does not include it. |

The texts are copied unchanged from the legacy story; the deployment adds the alert routing and the runbook link, never a new wording. Thai text for each follows decision DL10. For MSG-GEN-006 the {system} value is "Classification model", "PII masking" or "Classification parameters", fixed by the dependency that failed.

### 15. Screens and states

The deployment serves SCR-31 Document review queue through the gateway-bff composite route (DP-19), in its states Loading, list and reviewed, with the two candidates and MSG-P5-003; the screen itself is RWB-P5-E1054-APP's. The operator-facing surfaces of this story are the pipeline run view, the release view, the two dashboards, the alert list and the runbook. The composite route specification and the panel field list are Not specified in the source documents (GAP-1004; ASM-1796); the deployment registers the route target and the health check of the two classification operations only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-050-11 | AC1; regression evidence for legacy Access | Component | The chart renders with the login reference and the migration job; a read without the Documents right is refused with MSG-P4-002 |
| TC-E1-050-01 | AC2, AC5 | NFR | Labeled sample of 180 synthetic documents; the evaluation gate at 162 and the accuracy series |
| TC-E1-050-02 | AC3, AC5 | NFR | Threshold 0.80 and a synthetic item at 0.62; the review-share series and the drift alert |
| TC-E1-050-03 | AC3, AC4 | NFR | Top score 0.80 and a parameter change to 0.90; the flag off and on |
| TC-E1-050-04 | AC5, AC6 | NFR | Model stub silent for 60 seconds; the model-unavailable alert and the runbook entry |
| TC-E1-050-05 | AC5 | NFR | Stub returns LOAN_CONTRACT 0.91; the unknown-type share and its alert |
| TC-E1-050-06 | AC4 | NFR | Upload of type TITLE_DEED and an item in RESCAN; no classify call and no queue growth |
| TC-E1-050-07 | AC4 | NFR | A second intake run while the first workflow is open; the overlap skip is counted |
| TC-E1-050-08 | AC2, AC4 | NFR | A repeat run over 20 classified items; no second model call and no artefact change |
| TC-E1-050-09 | AC3 | NFR | Parameter CLASSIFY_THRESHOLD 0.90 with no release; the values files unchanged |
| TC-E1-050-10 | AC5 | NFR | Synthetic page with a national ID number and an account number; the masking series and no text on a dashboard |

This story owns no legacy acceptance criterion, so the eleven rows are the legacy test cases of RWB-E1-050 with their IDs kept in legacy order; the Covers column names this story's own criteria, because the deployment is what each case now exercises: the chart and the artefact pair, the evaluation gate, the parameters and the flag, the Schedule participation and the scaling, the dashboards and the alerts, and the runbook with the rollback. The legacy level System maps to NFR and Access to Component; the criteria themselves are proven in RWB-P5-E1050-APP and are listed as regression evidence here. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in a values file: the threshold, the page bound, the timeout, the type codes and the reason set are reference rows and parameters, never a deployment value.
- No personal data in logs, dashboard series, alert payloads, workflow inputs or the runbook: type codes, reasons, scores, counts, versions, dates and durations only.
- No OCR text and no candidate list on a dashboard, in an alert or in a runbook: the evidence is a count, a share and a version.
- ACE data only through the owner's contract or the `v_ace_*` views; this capability reads no ACE view.
- No cross-schema read and no cross-schema key: the release writes only `rwb_document`, holds no grant elsewhere and creates no constraint into another schema (DP-01, DP-02).
- One login per service; the chart carries the `rwb_document` login reference and no other service's credential.
- The topic keeps its retry topic and its `.dlt` topic, and the release never recreates a topic that other keys' events already use (DP-09).
- The release pins the image digest, the chart version and the classifier artefact digest; a rebuild between environments is not allowed.
- No secret is written into a values file, a chart template, a dashboard or the runbook; all secrets come from the platform secret store, including the model endpoint credential.
- The flag is the first step of every recovery, and a rollback changes no schema: the release is designed so the previous model version can run against the same columns.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-DCM-005 | Classified into an agreed type with a confidence; below the threshold to review | The worker and the classify activity, the parameter reads, the flag, the confidence and review-reason dashboards | TC-E1-050-01, TC-E1-050-02, TC-E1-050-03 |
| FEAT-DCM-08 | Classify a document into one of the six types | The type table read in force, the artefact version in the answer, the unknown-type alert | TC-E1-050-05, TC-E1-050-09 |
| FEAT-AGT-04 | The agent and model capability behind the step | The artefact pinning, promotion and rollback, and the evaluation gate | TC-E1-050-01, TC-E1-050-04 |
| NFR-067 | Every scheduled job has a run book, monitoring and an alert | The nine runbook entries and the five alert rules | TC-E1-050-04, TC-E1-050-11 |
| NFR-068 | A failing job or interface raises an alert to a named owner within its target | The model, masking and parameter alerts and their routes | TC-E1-050-04, TC-E1-050-05 |
| ADR-023 | Observability per service | Two dashboards, five alerts and the runbook | TC-E1-050-02, TC-E1-050-10 |
| ADR-021 | Per-service Flyway and migration ownership | The migration job and its one step | TC-E1-050-11 |

### 19. Out of scope

- The application code of the classify step, the masking client, the classifier and the evaluation runner (RWB-P5-E1050-APP).
- The contract documents, the contract jar and the fakes as published artefacts (RWB-P5-E1050-CON); this story only deploys the test copies.
- The intake workflow, its 15-minute Schedule and the OCR step (RWB-P5-E1049-APP).
- The platform topic provisioning, the Temporal cluster and the observability platform (the platform epics RWB-PLT-EVT, RWB-PLT-WF and RWB-PLT-OBS).
- The model provider, the training and production of the model artefact, and the `rwb-agent` satellite (GAP-1002; ASM-1795).
- The exact cluster topology, node pools, replica counts, KEDA thresholds, probe timings and alert shares (GAP-1004).
- The evaluation report content and the risk sign-off of the model (RWB-P5-E1050-APP and the risk and model risk officer).
- The review queue screen and its actions (RWB-P5-E1054-APP).
