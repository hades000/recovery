# RWB-P5-E2025-OPS Extraction for the stage 2 and 3 document types

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E2025-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-025 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP19 |
| Parallel lane | L-P5-X |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-013, FR-P5-015, FR-P5-016, FR-P5-017, FR-P5-018, FR-P5-027, FR-P5-028, FR-P5-029) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-025 for rwb-document. The legacy story prepared a classifier version, a type table version and a reader and expected an operator to run the extraction job from a shared scheduler. This story deploys the stage 2 and 3 extension of `rwb-document`: one chart and its values, the migration step of the extraction sequence with its reader index, the one intake Schedule on queue `rwb-document` in namespace `rwb-recovery` verified and never duplicated, the model route endpoint and the credential references of the service identity, the OCR provider endpoint verified and not replaced, the dashboards and alerts for extraction outcomes and field accuracy, the flag that turns the new types on and off, and the runbook with its rollback. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform engineer**, I want **the stage 2 and 3 extension of `rwb-document` deployed as one Helm release with its values files, its migration gate over the extraction sequence and the reader index, the one intake Schedule on queue `rwb-document` in namespace `rwb-recovery` verified with no second timer, the endpoint and credential references the extraction needs for the model route and the OCR provider, the feature flag that turns the new types on and off, the dashboards that show extraction outcomes and field accuracy, the alerts on a failed extraction and on an accuracy below the pass mark, and a runbook with its rollback**, so that **an operator can see an item that failed to extract, a field set that fell below the accuracy pass mark, a model route that stopped answering and a Schedule that stopped moving, recover from the run book alone, and prove that the six Epic 1 types were untouched and that no document was altered when the flag was switched or the release was rolled back**.

The legacy story ran the extension inside a shared scheduler and a shared schema: the type table version and the classifier version were prepared by hand, `ExtractStep` ran as a job step of JOB-12, and the reader was a Java interface nobody could see the health of. In the target that picture splits in four. JOB-12 stays one Temporal Schedule in the service that owns it, so the release verifies the Schedule rather than registering a second one (DP-10). The extraction writes tables of `rwb_document` only, so the migration gate carries the Epic 1 sequence and the reader index (DP-01). The new types are data rows of the type table, so the release ships a flag and no code per type. The reader is a published operation of this service, so the release publishes its latency and error series and the S4 and S2 callers build against the contract (DP-11, DP-13). What is left for this story is a chart, a migration gate, a Schedule check, two provider bindings, six dashboard series, five alert rules, five runbook entries and a rollback.

Deployment is also where the extension is kept reversible. The flag removes the five new types without a schema change and without a redeployment of a type table; the type table version is a data load owned by the reference data administrator and the release only reports which version each environment holds; and no release ever replaces the OCR provider or the model provider, because both are owned elsewhere and this story carries their endpoints and credential references only. The observability follows ADR-023 per service: six series, five alerts and five runbook entries, each alert carrying a message identifier and one runbook entry.

### 2. Business rationale

The business measure of this legacy key is fields extracted without review, and the operational measure behind it is the one no unit test sees: a new type whose accuracy fell below the pass mark must be visible before an officer trusts its values in a litigation pack. A field set that fails, a model route that has expired its credential, a Schedule that stopped after a release and a type table version that was never loaded are all silent unless the release emits them and the run book says what to do.

The split changes what an operator does. In the legacy story the operator re-ran a job and checked a type table by hand. In the target the operator reads the Schedule's run history, the extraction-outcome counters of each type, the accuracy series against the 0.90 pass mark and the review backlog of the new types, and then takes one of five actions: re-run the Schedule for the business date, hold the flag, reload the type table through the reference data administrator, clear the model route credential, or roll back the chart. The runbook is written for that sequence, because the difference between a busy release week and an incident is whether the operator has to guess which of the five failed.

The story also carries the retirement explicitly. No Quartz job, no scheduler table and no second timer is deployed; the intake Schedule is the only timer and the release refuses a second one (BR3). The five new types are data, so their rollback is a flag and never a rebuild, and the six Epic 1 types keep their behaviour under every value of the flag (BR4, BR9).

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The Kafka event platform provides `rwb.document.events.v1` with its three retry topics and its `.dlt` topic, and the ACLs of this service's principals (RWB-PLT-EVT, RWB-PLT-TE006-CON; DP-09).
- The Temporal workflow kit and the namespace `rwb-recovery` exist, with worker versioning, the build ID provider and the payload codec (RWB-PLT-WF, RWB-PLT-E1071-CON; DP-10).
- The per-service Flyway sequence and the migration conventions of `rwb_document` are published (RWB-PLT-E1044-CON), and the sequence of the Epic 1 extraction is in place (RWB-P5-E1053-CON).
- The platform error envelope and the message catalogue are in force, so an alert can carry a message identifier.
- The three environments DEV, SIT and UAT exist and the production namespace exists for the release date; the feature flag library is available.
- The worker compute, the storage, the containers, the topic binding, the ACLs and the service identity exist in each environment, and the private route to the model provider is open (the infrastructure stories of this service).
- The gateway-bff composite route for SCR-30 and SCR-31 is published (RWB-PLT-N001-CON; DP-19).
- The extraction operations and the checked-fields read are declared (RWB-P5-E1053-CON, RWB-P5-E2025-CON), so the release deploys a capability that exists and not a shell.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7). The baseline it deploys is RWB-P5-E2025-APP's, the contract it gates is RWB-P5-E2025-CON's and the endpoints it injects are the platform's; none of them blocks the chart work.
- The release date 31 December 2026 is the legacy one and is tentative (ASM-1912), and the story carries Status Draft (realignment v1) because no approval of the realigned story is recorded (ASM-1913).

The model name and the model version behind the agent route, the alert thresholds, the evaluation cadence and the exact business-hours window are Not specified in the source documents (ASM-1916). The OCR provider product and its endpoint are the ones the Epic 1 intake release provisions and are verified here, not replaced (ASM-1918).

### 4. Flow

1. The pipeline builds the service image and the contract jar, runs the unit, component and contract tests, scans the image and the dependencies, and publishes one chart version.
2. The chart deploys the API deployment and the worker deployment with the rwb-document login, the namespace `rwb-recovery`, the task queue `rwb-document`, the codec, the build ID of the release and the values of the platform.
3. The worker scaling step enables KEDA on the queue backlog of `rwb-document`, so the pool grows with the 15-minute run and the front stays at its fixed replica count.
4. The migration step applies the `rwb_document` sequence of the release and refuses to run when the target schema is not `rwb_document`; the index `ix_document_type_case` of the checked-fields read is one step of it, and this story adds no table and no column.
5. The type table step reports the version in force per environment (`DOCTYPE-2026.11` or `DOCTYPE-2026.12`) and fails the smoke run when the version the environment is meant to hold is not in force; the load itself stays with the reference data administrator and the type table of RWB-P5-E1025-APP (ASM-1914).
6. The Schedule step verifies the intake Schedule: workflow `DocumentIntakeWorkflow`, queue `rwb-document`, namespace `rwb-recovery`, every 15 minutes in business hours, overlap policy skip and a catch-up window of one run; it creates nothing and fails the release when the Schedule is missing, duplicated or pointed at a foreign workflow, because the Schedule belongs to RWB-P5-E1049-OPS.
7. The provider step binds the model route endpoint and the OCR provider endpoint from the values of the environment, the client credential of the service identity from the platform secret store, and fails the release when an endpoint is missing, points outside the private network or carries a literal secret (ASM-1916, ASM-1918).
8. The flag step sets `rwb.document.extract-stage23` from the values of the environment; the legacy name `rwb.dochub.extraction-stage23` is recorded as retired and is not deployed (ASM-1915).
9. The dashboards are published with the six series and the environment, release, build ID and document type as dimensions.
10. The five alerts are wired to their message identifiers and to their runbook entries: MSG-P2-004 for a failed extraction run, MSG-P5-003 for a review backlog of the new types, MSG-GEN-006 for an unavailable dependency or an expired credential, and the accuracy and read alerts whose identifiers are Not specified in the source documents (ASM-1917).
11. A smoke step in SIT loads the 60-document sample with the flag on, waits for one Schedule run, confirms fields of the five new types with one `DocumentFieldsExtracted` event, turns the flag off and confirms that the new types are no longer offered and that the six Epic 1 types still extract, then restores the environment.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The chart render or the migration job fails | The deployment stays unready and the pipeline stops; no traffic, no offset and no migration is left half applied | None | AC1 |
| X2 | The migration step is pointed at a schema other than `rwb_document` | The step refuses and the release stops | None | AC1 |
| X3 | A run of the intake Schedule fails, or runs past its threshold | The run-failure alert fires with MSG-P2-004 naming the run, the time and the runbook path; the Schedule retries on its next interval | MSG-P2-004 | AC4 |
| X4 | The model route does not answer, or its credential has expired | The extraction of the item fails on every attempt, the item stays unreviewed with `extract_status` FAILED, and the dependency alert fires with MSG-GEN-006 naming the system and the runbook entry names the rotation | MSG-GEN-006 | AC3, AC4, AC5 |
| X5 | A Schedule is missing, registered twice, or points at a foreign workflow | The Schedule check fails the release: one Schedule ID, one workflow, one queue | None | AC2 |
| X6 | The type table version the environment should hold is not in force | The type table step fails the smoke run and the release is not promoted | None | AC1, AC6 |
| X7 | Field accuracy on the sample falls below the pass mark | The accuracy alert fires with the per-field series and the runbook entry names the review-only proposal route through RWB-P5-E1025-APP | Not specified in the source documents (ASM-1917) | AC4, AC5 |
| X8 | A dashboard series is missing, or an alert carries no message identifier or no runbook link | The observability check fails the release | None | AC4 |
| X9 | The feature flag is off in an environment | The five new types are not offered to classification and the checked-fields read returns nothing for them; the six Epic 1 types are unaffected; the flag is not a way to stop a run in progress | None | AC6 |
| X10 | A new build is promoted while runs are open | The open runs replay on the new build from their history; the dashboards show both build IDs | None | AC1, AC4 |
| X11 | The reader latency or error rate of the checked-fields read passes its threshold | The read alert fires and the runbook entry names the caller, the route and the partition of the case | Not specified in the source documents (ASM-1917) | AC4, AC5 |
| X12 | A reviewer or a caller reads a document outside their scope after the release | The 404 shape of MSG-P4-003 is unchanged and no field value is returned | MSG-P4-003 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the workflow kit, the topic provisioning, the migration conventions, the flag library and the provider endpoints; no application code is built here |
| Negotiable | Replica counts, resource sizes, lag and error thresholds, the evaluation cadence and quotas are environment values |
| Valuable | Makes the new types observable, reversible and provable before the release date, and keeps the six Epic 1 types untouched |
| Estimable | One chart, one migration gate, one Schedule check, two provider bindings, one flag, six series, five alerts and five runbook entries |
| Small | Fits one sprint with the runbook |
| Testable | Every criterion tests an artefact: the chart renders, the migration refuses a foreign schema, one Schedule exists, an alert fires on a synthetic metric, the smoke run passes |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the stage 2 and 3 extraction extension for rwb-document

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the namespace is rwb-recovery and the task queue of rwb-document is rwb-document
    Given the target environment is SIT

  Scenario: AC1 One chart, one login, one schema and one queue are deployed (new, D-RCV-60)
    Given the rwb-document chart and its values files
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the API and the worker deployments carry the rwb-document login and no other service's credential
    Then the worker polls only the task queue rwb-document in namespace rwb-recovery and KEDA scales it on the queue backlog
    Then the migration step applies the rwb_document sequence, creates the index ix_document_type_case and refuses a target schema other than rwb_document
    Then the release adds no table and no column, because the extension writes the tables of the Epic 1 extraction
    Then worker versioning is enabled and a new run goes to the new build while the old build drains
    Then the deployment registers no Quartz job and no scheduler table
    Then the type table step reports the version in force per environment and fails the smoke run when the expected version is not in force

  Scenario: AC2 The one intake Schedule on queue rwb-document is verified and no second timer exists (new, D-RCV-60)
    Given the deployed release and the namespace rwb-recovery
    When the Schedule step runs and is applied a second time
    Then one Schedule exists with the ID fixed by the intake release, the workflow DocumentIntakeWorkflow and the queue rwb-document
    Then its interval is every 15 minutes in business hours and its overlap policy is skip with a catch-up window of one run
    Then the second apply creates no second Schedule and changes nothing
    Then a release that finds the Schedule missing, duplicated or pointed at a foreign workflow fails its own check
    Then no Quartz job, no scheduler table and no cron entry exists in the release
    Then the extraction and evaluation activities registered by this worker are the ones of queue rwb-document and no other queue
    Then the exact business-hours window and the evaluation cadence are Not specified in the source documents (ASM-1914)

  Scenario: AC3 The model route and the OCR provider endpoints and credentials are bound (new, D-RCV-60)
    Given the values files of DEV, SIT and UAT and the platform secret store
    When the provider step runs
    Then the model route endpoint of the extraction is the private route the agent service publishes, and its client credential is a secret reference of the rwb-document service identity
    Then the OCR provider endpoint and its secret are the ones the intake release provisions and are verified as present and unchanged, not replaced
    Then no provider key, no model name and no endpoint credential is written into a values file, a chart template, a dashboard or the runbook
    Then a missing endpoint, an endpoint outside the private network or a literal secret fails the release
    Then the model name, the model version and the provider product behind the route are Not specified in the source documents (ASM-1916)

  Scenario: AC4 The dashboards and the five alerts are published with their identifiers (new, D-RCV-60)
    Given the published dashboards and alert rules of the deployment
    When a synthetic run produces extracted items of the five new types, one failed item, one field set below the pass mark and one handler failure on the reader
    Then the dashboards show extraction outcomes per type and status, fields in review per type, the extractor version in use, the field accuracy of the sample against the 0.90 pass mark, the checked-fields read latency and error rate, and the queue backlog and age of the task queue
    Then each series carries the environment, the release, the build ID and the document type as dimensions
    Then the run-failure alert fires with MSG-P2-004, the review-backlog alert with MSG-P5-003 and the dependency alert with MSG-GEN-006
    Then the accuracy alert and the read alert carry their identifiers, which are Not specified in the source documents (ASM-1917)
    Then each alert names the Schedule ID, the build ID, the environment and one runbook link
    Then no panel and no alert payload carries a field value, a party name, an account number or a document text

  Scenario: AC5 The runbook and the rollback are exercised (new, D-RCV-60)
    Given the published runbook and the rollback of the release
    When a failed extraction run, a review backlog of a new type, an unavailable model route, an accuracy below the pass mark and a failing reader are simulated
    Then each condition maps to one runbook entry with the check, the owner role and the recovery step
    Then the model route entry names the credential rotation and the dependency owner, and no entry asks an operator to edit a type row by hand
    Then the rollback redeploys the previous chart with its own build ID and the open runs finish on the old build
    Then a rollback leaves the type table version and the field rows in place, because the release writes no business row and the migration is additive
    Then the smoke run ends with the fields of the five new types, one DocumentFieldsExtracted event per extraction and no altered file, and the environment restored

  Scenario: AC6 The feature flag turns the new types on and off (new, D-RCV-60)
    Given the published runbook, the flag and the SIT type table holding DOCTYPE-2026.12
    When the flag rwb.document.extract-stage23 is turned off in SIT and one Schedule run is waited for
    Then the five new types are not offered to classification and the checked-fields read returns no field for them
    Then the six Epic 1 types still extract and still answer their fields with the flag off
    Then the legacy flag rwb.dochub.extraction-stage23 appears in no values file, chart or runbook
    Then turning the flag on again restores the new types on the next run with no redeployment of the type table
    Then the flag is a value of the environment and never a literal in a template
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One login, one task queue and one schema per service: the release carries the rwb-document login, polls `rwb-document` only and migrates `rwb_document` only | Arch v5 slide 41; DP-02; DP-01 |
| BR2 | The release publishes on `rwb.document.events.v1` only and subscribes to no topic of this service; the decision-record topic is not used by this path | Arch v5 slides 16 and 42; DP-09 |
| BR3 | One Schedule and one scheduler: the intake Schedule is the only timer for JOB-12, registered in Temporal on queue `rwb-document` in namespace `rwb-recovery`; the release verifies it and registers no second one, and no Quartz job, scheduler table or cron entry exists | Arch v5 slide 44; DP-10; `ASM-1914` |
| BR4 | The five new types are reversible by one flag, `rwb.document.extract-stage23`, which replaces the legacy `rwb.dochub.extraction-stage23`, and the six Epic 1 types keep their behaviour under every value of the flag | legacy section 13; DP-07; `ASM-1915` |
| BR5 | Every alert carries a message identifier or its recorded placeholder and links one runbook entry | Template and Rules §R7.2 s14 |
| BR6 | No environment value is hard-coded: replicas, resources, thresholds, intervals, quotas, endpoints and the flag come from values files and parameters | Template and Rules §R7.2 s17 |
| BR7 | Dashboard series, alert payloads and the runbook carry counts, identifiers, statuses, business dates, type codes and build IDs only, never a field value, a party name or a document text | ADR-023; CTL-11; DL26 |
| BR8 | The release exposes the checked-fields read and the extraction operations through the chart and its ingress and declares no path of its own; SCR-30 and SCR-31 are reached through the gateway-bff composite route | DP-19; RWB-P5-E2025-CON 12.1 |
| BR9 | The type table version is data: the release reports it and never loads it, and a version is applied only by the approved load of RWB-P5-E1025-APP | DL19; `ASM-1914` |
| BR10 | A failing release never replaces a working one: the previous build stays in force until the new build passes its tests and its smoke run | DP-10 |
| BR11 | The release provisions no ACE grant, no view and no lake route, and carries no provider key in a value, a template or a runbook | DP-01; DP-05; D-RCV-35 U1; NFR-052 |
| BR12 | A field set below the pass mark is never promoted to a confident one by the release: the accuracy series and its alert route the proposal through the review-only load of the type table | CTL-08; `ASM-1917` |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the contract tests pass | Deploying |
| Deploying | Migration applied and worker registered | The `rwb_document` sequence applied and the worker polls `rwb-document` | Ready |
| Ready | Schedule and type table verified | One Schedule with the intake release ID, and the expected type version in force | Scheduled |
| Scheduled | First run completes | The run finishes and its counters reach the dashboards | In use |
| In use | Release superseded | A new chart version passes its tests | Rolling |
| Rolling | All workers on the new build | The old build drains its open runs | In use |
| In use | Flag off | `rwb.document.extract-stage23` is turned off in the environment | Restricted |
| Restricted | Flag on | The flag is turned on again and the next run extracts the new types | In use |
| In use | Smoke run failed | The Schedule check, the provider check, the type table check or the smoke step fails | Blocked |
| Blocked | Previous build restored | The previous chart is redeployed or a later build passes the smoke run | In use |

The field states OK, REVIEW, CONFIRMED and CORRECTED and the `extract_status` values are the app story's runtime and are not states of this deployment.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the migration gate, the Schedule check, the provider bindings, the dashboards and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the Schedule, the topic ACLs, the consumer quotas, the flag library and the restart of a run |
| Platform event owner | Owns `rwb.document.events.v1`, its retry and `.dlt` topics, its schema subject and its retention |
| RW-REFADM, reference data administrator | Loads and reports the type table version the release checks; never the DevOps engineer |
| Release manager | Approves the promotion of one artefact and may block it on a failing smoke run |
| On-call operator | Runs the five runbook entries and opens an incident when a failed extraction, an accuracy drop or a reader failure persists |
| rwb-document owner | Owns the extraction extension, the checked-fields read and the migration the release applies |
| Agent service owner | Owns the model route, the model, the prompt and the provider credential behind it |
| Data steward | Confirms that no dashboard, alert or runbook carries a field value or a personal value |

The worker runs as the rwb-document service identity (DP-02), carried by the chart as a secret reference and never as a literal. The login name is Not specified in the source documents (ASM-1916).

### 11. Data

| Item | Content |
|---|---|
| Deployment values | Image digest, chart version, replica counts for the API and the worker, resource requests and limits, probe paths and timings, log level, namespace, task queue, build ID, feature switch, KEDA backlog threshold, Schedule ID, model route endpoint, OCR provider endpoint reference, alert thresholds |
| Task queue | `rwb-document` in namespace `rwb-recovery`, polled by the worker of this service only |
| Topic | `rwb.document.events.v1` with its partitions, replication factor, retention and key, its three retry topics and its `.dlt` topic; no subscription of this service |
| Schema | `rwb_document`, migrated by its own per-service Flyway sequence; the reader index `ix_document_type_case` is one step of it and the release adds no table and no column |
| Schedule | The intake Schedule: `DocumentIntakeWorkflow`, queue `rwb-document`, namespace `rwb-recovery`, every 15 minutes in business hours (JOB-12), overlap policy skip, catch-up window one run; verified by this release and registered by RWB-P5-E1049-OPS |
| Type table | The version in force per environment, reported and never loaded; `DOCTYPE-2026.11` before the release date and `DOCTYPE-2026.12` from 2026-12-31 |
| Flag | `rwb.document.extract-stage23`, on in DEV and SIT for the tests, from the values of each environment; the legacy `rwb.dochub.extraction-stage23` is retired |
| Provider bindings | The model route endpoint published by the agent service with the client credential of the service identity, and the OCR provider endpoint of the intake release with its secret; both as secret references |
| Dashboard series | Extraction outcomes per type and status, fields in review per type, extractor version in use, field accuracy of the sample against the pass mark, checked-fields read latency and error rate, queue backlog and age; dimensions environment, release, build ID, document type |
| Runbook entries | Failed extraction run, review backlog of a new type, unavailable model route, accuracy below the pass mark, failing checked-fields read; each with the check, the owner role and the recovery step |
| Alerts | Five rules and one runbook entry each: MSG-P2-004 for a failed run, MSG-P5-003 for the review backlog, MSG-GEN-006 for an unavailable dependency, and the accuracy and read alerts with the placeholder of ASM-1917 |
| Secrets | The rwb-document login secret, the Kafka client credential, the Temporal mTLS material, the model route client credential and the storage identity reference, all from the platform secret store |
| Test data | The 60-document sample of the app story, masked, one forced extraction failure, one field set below the pass mark and one flag-off run; synthetic identifiers only |

The deployment topology (cluster names, node pools, replica counts, resource sizes, zone spread, ingress class and probe timings) belongs to each environment and is set by the platform team in its values file; the chart exposes every one of them as a value and this story fixes only their names and the rule that they are never hard-coded.

**Probes.** Readiness answers healthy only after the worker has polled `rwb-document` once and the API has answered its health path; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database or commits an offset, and an unreachable model route is reported as not ready for extraction, never as live-and-broken.

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Owner | Notes |
|---|---|---|---|
| None | — | — | The checked-fields read of `GET /api/recovery/document/v1/cases/{caseId}/checked-fields` is declared by RWB-P5-E2025-CON and the extraction operations of `POST /api/recovery/document/v1/intake-items/{intakeItemId}/extract`, `GET /api/recovery/document/v1/intake-items/{intakeItemId}/extraction` and `GET /api/recovery/document/v1/documents/{documentId}/fields` are declared by RWB-P5-E1053-CON; this deployment exposes them through the chart and its ingress and declares no path of its own. The probes are cluster-internal and are not part of the API surface |

#### 12.2 REST operations consumed

| Method | Path | Owner | Story | Note |
|---|---|---|---|---|
| None | — | — | — | The deployment carries no REST client of its own. At run time the extract activity reaches `rwb-case` for its parameters and lists, the checked-fields read reaches `rwb-case` for the case, and the model route is the agent service's; the chart's only start-up calls are the Temporal frontend, the Kafka brokers and the health paths of its own dependencies |

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| None | — | — | — | `rwb.document.DocumentFieldsExtracted.v1` on `rwb.document.events.v1` is published by the extraction of the app story through the outbox relay (DP-09); the deployment publishes nothing of its own and writes no decision record for this path |

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| None | — | — | This path consumes no event: the trigger is the intake Schedule. The consumer groups of `rwb-case` on `rwb.document.events.v1` are theirs and are not deployed here |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| `DocumentIntakeWorkflow` | Workflow, from the L3 "Document intake" template | `rwb-document` | Registered by the worker of this release with the build ID and worker versioning; owned by RWB-P5-E1049-APP |
| `extract` | Activity | `rwb-document` | Registered by the same worker with the kit's retry policy; extended by RWB-P5-E2025-APP for the new types |
| `evaluateExtraction` | Activity | `rwb-document` | Registered by the same worker; extended by RWB-P5-E2025-APP with the accuracy and confusion-matrix report; started on demand and never by a Schedule of its own |
| Outbox relay | Platform relay | not a worker | Deployed with the library; publishes `rwb.document.events.v1` on its one-minute interval (JOB-11) |

**Build ID and versioning.** The build ID is the one supplied by the workflow kit for the release commit; worker versioning is enabled and a new build takes new runs while the old build drains. The build ID format and the versioning policy are the platform kit's and are not set by this story (ASM-1919).

#### 12.6 Schedules

| Schedule | Workflow | Queue | Interval | Note |
|---|---|---|---|---|
| The intake Schedule (JOB-12 Document intake), verified by this release | `DocumentIntakeWorkflow` | `rwb-document` | Every 15 minutes in business hours | One Schedule with the ID fixed by the intake release, overlap policy skip and a catch-up window of one run; this release creates nothing and fails when the Schedule is missing, duplicated or pointed at a foreign workflow. The exact business-hours window and the catch-up policy are the intake release's and are Not specified in the source documents (ASM-1914) |

No other Schedule, cron entry or Quartz job is registered by this release, the evaluation activity registers no Schedule of its own, and the outbox relay runs on the platform's one-minute interval (BR3).

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `document_field` | P5 (`rwb_document`) | Created by the Epic 1 extraction sequence the release applies; written by the app story, never by the deployment |
| `document_intake` | P5 (`rwb_document`) | Created by the intake sequence; read and written by the app story |
| `document_text` | P5 (`rwb_document`) | Created by the intake sequence; read by the app story |
| `document_type` | P5 (`rwb_document`) | Created by the type table migration; the version rows are loaded as data by the reference data administrator, never as a chart value |
| `document_hub_parameter` | P5 (`rwb_document`) | Created by the store migration; the seven extraction rows are loaded as data, never as a chart value |
| `document` | P5 (`rwb_document`) | Created by the store migration; this release adds the index `ix_document_type_case` only |
| `outbox_event`, `outbox_delivery`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_document` | Created by the library migrations in the same schema; written by the app story and the relay |

The release applies the `rwb_document` sequence of this key and no other: no ACE view, no other service's table and no lake object is created, altered or read (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Story | Used for |
|---|---|---|
| None | — | No fake is deployed. The contract fakes of RWB-P5-E2025-CON, RWB-P5-E1053-CON and the dependency stubs of the platform are test-only workloads and are not promoted into SIT, UAT or production |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 0 consumed by the deployment | The checked-fields read and the three extraction operations are the app story's and the two baselines'; the probes are cluster-internal |
| Kafka | 0 published, 0 consumed here; 1 topic configured with retry and `.dlt` | `rwb.document.events.v1` with its ACLs; no subscription and no decision-record topic on this path |
| Temporal | 1 workflow, 2 activities, 1 Schedule verified | Worker on `rwb-document` with a pinned build ID, worker versioning and KEDA scaling; the intake Schedule every 15 minutes in business hours, verified and never duplicated |
| File | 0 built or moved | The extraction reads `document_text` rows and touches no blob; the containers of the intake and store releases are unchanged by this release |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | The release migrates `rwb_document` only and reads no other schema | none |
| DP-06 | Parameters, casewf.config | The seven parameters stay rows read through the client library; no chart value carries them | H RWB-PLT-E1042-CON |
| DP-07 | Reference data, LOV | The three lists stay reference rows and the type codes stay type table rows; no chart value carries them | H RWB-PLT-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | The topic with its retry and `.dlt` topics, the inbox of the readers and the relay | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | The worker, the task queue, worker versioning and the one intake Schedule from the kit; the release verifies the Schedule and registers no Quartz job | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | The release declares no REST path and no client of its own; the private routes are the platform's | none |
| DP-13 | `/api/recovery/v1` | The ingress registers the service base `/api/recovery/document/v1` for the edge | none |
| DP-19 | Screen, ace-web | The ingress serves the gateway-bff edge; no screen is deployed | H RWB-PLT-N001-CON |

DP-10 is the substantive row of this story: JOB-12 stops being a Quartz job on a shared scheduler and is one Temporal Schedule on the service's own queue, so the release verifies the Schedule, the worker and the build ID and the operator restarts a run through the Schedule rather than a scheduler table. DP-01 keeps the migration inside `rwb_document` and makes the step refuse a foreign schema. DP-06 and DP-07 keep the pass mark, the threshold and the three lists out of the values files, so the only thing an environment sets is where the data lives, not what it says. DP-09 keeps the topic and the retry and `.dlt` topics under the platform owner while this release verifies the ACLs it needs. DP-11 and the two provider bindings are what the release does not own: the endpoints and the credential references are injected and checked, and no client, no model and no provider key is deployed here. DP-13 and DP-19 register the service base and the edge route and deploy no screen.

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-document/` overlay | API deployment, worker deployment, config map, secret references, probes, task queue, namespace, build ID, KEDA rule, provider bindings and flag |
| `helm/rwb-document/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, flag value, build ID, Schedule ID, KEDA threshold, model route endpoint, OCR provider reference, alert thresholds |
| Pipeline stage | Build, unit and contract tests, image and dependency scan, chart publish, migration gate, type table step, Schedule check, provider step, smoke run, promotion |
| Migration step | The `rwb_document` sequence with `ix_document_type_case`; a target schema other than `rwb_document` is refused |
| Type table step | Reports the version in force and fails the smoke run when the expected version is not in force; loads nothing |
| Schedule check | One Schedule with the intake release ID, the workflow, the queue, the interval, the overlap policy and the catch-up window; a missing, duplicated or foreign Schedule fails the release |
| Provider bindings | The model route endpoint with the client credential reference, and the OCR provider endpoint reference verified as the intake release's |
| Dashboards | The six series of section 11 with the four dimensions |
| Alerts | Five rules, each with a message identifier or its placeholder and one runbook entry |
| Runbook | Five entries: failed extraction run, review backlog of a new type, unavailable model route, accuracy below the pass mark, failing checked-fields read |

**Alert mapping**

| Message ID | Condition | Alert | Route |
|---|---|---|---|
| MSG-P2-004 | A run of the intake Schedule failed or ran past its threshold | Run-failure alert naming the Schedule ID, the run, the time, the business date and the runbook path | Platform on-call, page in business hours, else ticket |
| MSG-P5-003 | Fields of a new type are held for a person and the backlog passes its age | Review-backlog alert naming the type, the count per state and the age of the oldest item | Reviewer lead and the data steward, ticket |
| MSG-GEN-006 | The model route, a case read or a list read is unavailable, or a credential has expired | Dependency alert naming the system and the health state | Platform on-call and the agent service owner, page |
| Not specified in the source documents (ASM-1917) | The field accuracy of the sample falls below the 0.90 pass mark | Accuracy alert naming the field, the type, the measured value, the pass mark and the evaluator version | Data steward and the rwb-document owner, page |
| Not specified in the source documents (ASM-1917) | The latency or the error rate of the checked-fields read passes its threshold | Read alert naming the operation, the caller service and the partition of the case | Platform on-call, ticket |

**Retry and offsets.** The Schedule retries a failed run on its next interval and never runs two runs at once, because the overlap policy is skip. The activity retry is the kit's policy; the release adds no retry of its own, and the agent route keeps the 60-second budget per attempt and the three attempts of the extraction baseline. The relay commits its offset after the outbox row is marked sent, so a restart republishes nothing twice.

**Rollback.** A release that fails the smoke run is not promoted. A release already promoted is rolled back by redeploying the previous chart version with its own build ID, which keeps the old build serving its open runs until they finish; the Schedule keeps its ID and points at the workflow, so a rollback changes the build under it and not the timer. A rollback leaves the type table version and the field rows in place, because the release writes no business row of its own and the migration is additive; reverting the new types is the flag and not the chart.

**Feature switch.** `rwb.document.extract-stage23`. On: the five new types are classified, extracted and read. Off: the new types are not offered to classification and the checked-fields read returns nothing for them, while the six Epic 1 types keep their behaviour. The legacy name `rwb.dochub.extraction-stage23` appears in no value, chart or runbook (ASM-1915).

**Done when.** The chart renders for DEV, SIT and UAT with a pinned digest and the build ID, the migration step refuses a foreign schema and creates the reader index, the type table step reports the expected version, the Schedule check passes with one Schedule and a second apply changes nothing, the provider bindings resolve the model route and the OCR provider without a literal secret, the flag-off run restricts the new types and leaves the six Epic 1 types extracting, the six series and the five alerts are published with their identifiers or placeholders and their runbook links, the smoke run produces fields of the five new types with one event per extraction and no altered file, and the five runbook entries are reviewed by the on-call rota.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-004 | A run of the intake Schedule failed or ran past its threshold | {job} failed at {time} for business date {date}. Follow run book {runbook}. |
| MSG-P5-003 | Fields of a new type are held for a person | Some fields need checking. The document is in the review queue. |
| MSG-GEN-006 | The model route, the case read or the list read is unavailable, or a credential has expired | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-003 | A caller reads a document outside its scope after the release | This case is not in your scope. |
| Identifier pending | The field accuracy of the sample falls below the pass mark | Not specified in the source documents (ASM-1917) |
| Identifier pending | The checked-fields read passes its latency or error threshold | Not specified in the source documents (ASM-1917) |

MSG-P5-003 is the legacy text of RWB-E2-025 section 14 and is unchanged; MSG-P4-003 is the legacy scope text of the same section. MSG-P2-004 is the job-failure text of the observability epic and MSG-GEN-006 the platform text for an unavailable system, both used with their agreed wording. The accuracy and read alerts have no identifier in the source set, so they carry the placeholder until the Error and Message Standard names them. An alert payload names counts, statuses, business dates, type codes, the Schedule ID, the build ID and group names only, never a field value, a party name or a document text.

### 15. Screens and states

The deployment has no screen of its own. Its operator-facing surfaces are the pipeline run view, the release view, the Temporal Web UI, the dashboards, SCR-30 Case documents and SCR-31 Document review queue through the gateway-bff composite route, and the runbook. The two screens are served by the app stories and the route of RWB-PLT-N001-CON; the deployment only registers the ingress path. The Temporal Web UI stays behind Entra ID: RW-PLATADM operates and RW-AUDIT reads, and payloads are decoded only through the codec server under break-glass. The job monitor of Epic 2 shows the same run data; this release publishes the run records the monitor reads.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P5-E2025-OPS-01 | AC1, BR1, BR11 | NFR | The chart renders for three environments with a pinned digest, the build ID, the login reference and worker versioning; the reader index is created; a foreign migration target is refused; the type table step fails on a wrong version |
| TC-P5-E2025-OPS-02 | AC2, BR3 | NFR | One Schedule with the intake release ID, the queue and the interval; a second apply changes nothing; a missing, duplicated or foreign Schedule fails the release; no Quartz job and no scheduler table |
| TC-P5-E2025-OPS-03 | AC3, BR6, BR11 | NFR | The model route endpoint and the client credential reference resolve; the OCR provider endpoint is verified unchanged; a literal secret or a non-private endpoint fails the release |
| TC-P5-E2025-OPS-04 | AC4, BR5, BR7, BR12 | NFR | The six series with the four dimensions; the five alerts with their identifiers or placeholders, one runbook link each, and no field value or personal value |
| TC-P5-E2025-OPS-05 | AC5, BR9, BR10 | NFR | Five synthetic conditions map to five runbook entries; the rollback redeploys the previous build and leaves the type table and the field rows in place; the smoke run leaves no altered file |
| TC-P5-E2025-OPS-06 | AC6, BR4 | NFR | The flag off restricts the five new types and leaves the six Epic 1 types extracting; the legacy flag name appears nowhere; the flag on restores the new types with no reload |

The legacy test cases of this key are answered by the app story: TC-E2-025-12 at Component and TC-E2-025-01, TC-E2-025-02, TC-E2-025-03, TC-E2-025-04, TC-E2-025-05, TC-E2-025-06, TC-E2-025-07, TC-E2-025-08, TC-E2-025-09, TC-E2-025-10 and TC-E2-025-11 at End to end, and the same twelve at contract level by RWB-P5-E2025-CON. This deployment proves the operating conditions those tests assume and adds no business outcome of its own.

### 17. Guardrails

- No business value in a values file: the types, the field codes, the patterns, the threshold, the pass mark and the review-only flags are type table rows and parameters, never a deployment value.
- No personal data in logs, dashboard series, alert payloads, the runbook or the workflow history: counts, statuses, type codes, identifiers, business dates and build IDs only, and payloads stay encrypted.
- One login, one task queue and one schema per service: the release carries the rwb-document login, polls `rwb-document` and migrates `rwb_document` only (DP-02, DP-01).
- The release deploys no ACE grant, no view and no lake route (DP-05, BR11).
- One Schedule and one scheduler: the intake Schedule is verified once and no second timer, Quartz job or cron entry exists (BR3).
- The model route and the OCR provider are injected as endpoint and secret references; no provider key, model name or credential is written into a value, a template, a dashboard or the runbook (BR11, NFR-052).
- The type table version is reported and never loaded by the release; a version is applied only by the approved load of RWB-P5-E1025-APP (BR9).
- The flag restricts the five new types and never touches the six Epic 1 types, and it is never a way to stop a run in progress (BR4).
- The release pins the image digest, the chart version and the build ID; a rebuild between environments is not allowed, and a failing smoke run never replaces a working build.
- No secret is written into a values file, a chart template, a dashboard or the runbook; all secrets come from the platform secret store.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| Arch v5 slide 44 | JOB-12 Document intake runs every 15 minutes, owned by rwb-document, as a schedule in the owning service | The one intake Schedule verified by the release, the worker and the build ID | TC-P5-E2025-OPS-01, TC-P5-E2025-OPS-02 |
| Arch v5 slides 16 and 41 | One schema, one API base, one topic and one task queue per service; the extraction writes OCR text and fields in `rwb_document` | The migration gate with the reader index, the topic ACLs and the queue binding | TC-P5-E2025-OPS-01, TC-P5-E2025-OPS-03 |
| Arch v5 slide 42 | rwb-document publishes DocumentFieldsExtracted on `rwb.document.events.v1` | The topic, its retry and `.dlt` topics and the absence of a subscription of this service | TC-P5-E2025-OPS-04 |
| Arch v5 slide 38 | The platform provides the template, the schemas and logins, the topic set and Temporal before the wave 2 services | The bindings this release verifies and the pieces it deploys | TC-P5-E2025-OPS-01, TC-P5-E2025-OPS-02 |
| ADR-023 | Observability per service | The six series, the five alerts and the five runbook entries | TC-P5-E2025-OPS-04, TC-P5-E2025-OPS-05 |
| NFR-068 | A failing interface, job or agent raises an alert to a named owner within its target | The run-failure, dependency, accuracy and read alerts with their routes | TC-P5-E2025-OPS-04 |
| NFR-052 | Secrets in the key store and never in code or configuration | Secret references only, and the secret scan of the release | TC-P5-E2025-OPS-01, TC-P5-E2025-OPS-03 |
| REQ-DCM-006, REQ-DCM-005 | The extraction path this release runs: the agreed types are extracted with a confidence and the uncertain ones go to review | The type table step, the flag, the accuracy series and the review-backlog alert | TC-P5-E2025-OPS-04, TC-P5-E2025-OPS-05, TC-P5-E2025-OPS-06 |

### 19. Out of scope

- The build of the extension, the checked-fields read and the evaluation runner (RWB-P5-E2025-APP).
- The contract documents, the shapes, the fixture, the event schema and the fakes (RWB-P5-E2025-CON and RWB-P5-E1053-CON); this story only deploys and gates them.
- The worker compute, the storage, the containers, the topic binding, the ACLs, the identity and the private routes (the platform and infrastructure stories of this service).
- The Temporal cluster, the namespace, worker versioning and the codec server as platform components (RWB-PLT-WF, RWB-PLT-E1071-CON).
- The registration of the intake Schedule and its run book (RWB-P5-E1049-OPS); this story verifies the Schedule and registers nothing.
- The type table itself, the DOCTYPE-2026.12 load and its Legal and NPA sign-off (RWB-P5-E1025-APP and the reference data administrator).
- The model route, the model, the prompt and the provider credential (P10 `rwb-agent` and RWB-P10-TE013-CON).
- The OCR engine, its provider and its capacity (RWB-P5-E1049-APP and the intake infrastructure story).
- The classification model and its contract (RWB-P5-E1050-APP, RWB-P5-E1050-CON).
- The review queue screen and the correction of a field (RWB-P5-E1054-APP).
- The cross-service journey of the checked-fields read with S4 and S2 live (RWB-ITG-E2025-ITG).
- The exact cluster topology, node pools, replica counts, alert thresholds, the evaluation cadence and the business-hours window, which are set per environment by the platform team.
