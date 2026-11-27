# RWB-P5-E1032-OPS Automatic attach from the OCR intake

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1032-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-032 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Base document baseline | FSD P6 Communications v3 and TSD P6 Communications v2 are In review; the wave 1 build uses these reviewed versions, and any change in the approved text is a change request |
| Size | Not specified in the source documents (DOR-RWB-P5-E1032-OPS-16) |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP15, DP19 |
| Platform baseline (wave 0, not H) | RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON are the shared baseline of wave 0 and are not in H (RWB-PLT-N001-CON stays H per DP-19); revisit only if a platform contract is not published before the wave 1 entry check |
| Parallel lane | L-P5-H |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P5-E1032-CON (build status Not started; contract not yet published); contract version Not specified in the source documents (DOR-RWB-P5-E1032-OPS-23); contract fake library version Not specified in the source documents (DOR-RWB-P5-E1032-OPS-22) |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-P5-E1032-OPS-14) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-015, FR-P5-017, FR-P5-018, FR-P5-019, FR-P5-032) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-032 for rwb-document. The legacy story ran JOB-12 on a shared Quartz scheduler behind a shared schema and expected an operator to read the review queue in the database. This story deploys the intake-match capability of `rwb-document`: one chart and its values, the `rwb_document` migration step, the topic and the queue, the 15-minute intake Schedule registered in Temporal on queue `rwb-document` in namespace `rwb-recovery`, the flag that replaces `rwb.dochub.autoattach`, the dashboards for match outcomes and held items, the alerts on a failed run and on a decision-record failure, the runbook and the rollback. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (26 resolved, 33 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **DevOps engineer**, I want **the intake-match capability of `rwb-document` deployed as one Helm release with its values files, its per-service Flyway step in `rwb_document`, its topic and its task queue with retry and `.dlt`, the intake trigger on the DocumentStored event with KEDA-scaled workers on queue `rwb-document` in namespace `rwb-recovery`, the feature flag that turns the automatic attach on and off, the dashboards that show match outcomes and held items, the alerts on a failed run and on a decision-record failure, and a runbook with its rollback**, so that **an operator can see a run that failed, an item that was held, a decision record that could not be written and a queue that stopped moving, restart it from the run book alone, and prove that no document was filed twice or lost when the flag was switched or the release was rolled back**.

The legacy story ran the intake behind a shared Quartz scheduler and a shared schema: JOB-12 fired on the scheduler table, `matchStep` wrote the recovery schema, and the Unmatched list was a query somebody ran. In the target that picture splits in four. JOB-12 is an event-started DocumentIntakeWorkflow in the service that owns it, started from the DocumentStored event with KEDA-scaled workers, so the release registers the worker that serves it (DP-10). The migration is one step of the service's own Flyway sequence in `rwb_document` (DP-15). The topic is `rwb.document.events.v1` with its retry and `.dlt` topics and its ACLs (DP-09, DP-14). The review queue is SCR-31 served through the gateway-bff composite route by the app story (DP-19). What is left for this story is a chart, a migration gate, a trigger, a flag, six dashboard series, four alert rules, five runbook entries and a rollback.

Deployment is also where the split is enforced operationally. The release carries the rwb-document login only, migrates `rwb_document` only, publishes on its own topic and on the shared decision-record topic only, and polls `rwb-document` only. It provisions no ACE grant, no view and no data-lake route (DP-01, DP-05, DP-17), and no inbound consumer on this path, because the trigger is the Schedule. The observability follows ADR-023 per service: six series, four alerts and five runbook entries, each alert carrying a message identifier and one runbook entry.

### 2. Business rationale

The business measure of this legacy key is fields extracted without review (FSD P5 A2.12.1), and the operational measure behind it is simple: an item that is held must be visible to the reviewer, and an item that failed must be visible to the operator. Neither is a unit test. A run that fails at 10:15, a decision record that refuses every write for ten minutes, a queue that stops moving because the worker lost its identity, and a set of held items that nobody counted are all silent unless the release emits them and the run book says what to do.

The split changes what an operator does. In the legacy story the operator restarted a Quartz job and opened the review queue in the same database. In the target the operator reads the Schedule's run history, the match-outcome counters and the held-item panel, restarts through the Schedule itself, and confirms three things: that the worker polled `rwb-document`, that the hole in the decision records is closed by the retry of the run, and that the items the failed run touched are back in PENDING so the next run selects them. The runbook is written for that sequence, because the difference between a busy morning and an incident is whether the operator has to guess which of the three failed.

The story also carries the retirement explicitly. No Quartz job, no scheduler table and no shared schema is deployed; the Schedule is the only timer, and a release that registers a second one or a job on a foreign queue fails its own checks (BR1, BR2, BR3). The flag keeps the automatic attach reversible without a schema change, and the rollback keeps the previous build serving open runs.

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The Kafka event platform provides `rwb.document.events.v1` with its three retry topics and its `.dlt` topic and the shared `rwb.decision-record.v1`, and the ACLs of this service's principals (RWB-PLT-EVT, RWB-PLT-TE006-CON; DP-09).
- The Temporal workflow kit and the namespace `rwb-recovery` exist, with worker versioning, the build ID provider and the payload codec (RWB-PLT-WF, RWB-PLT-E1071-CON; DP-10).
- The per-service Flyway sequence and the migration conventions of `rwb_document` are published (RWB-PLT-E1044-CON; DP-15). The migration file takes the next number of the V0001 to Vnnnn sequence of Service Template Specification v1 §3.
- The platform error envelope and the message catalogue are in force, so an alert can carry a message identifier.
- The intake run window is Not specified in the source documents (GAP-0994); the overlap policy and catch-up are Not specified in the source documents (CG-ALL-5846). The run-failure, held-item-age, KEDA and consumer-lag thresholds are environment values, and the consumer-lag alert carries a placeholder message identifier until the Error and Message Standard names it.
- The three environments DEV, SIT and UAT exist and the production namespace exists for the release date; the feature flag library is available.
- The worker compute, the storage, the hold container, the topic binding, the ACLs, the identity and the route exist in each environment (RWB-P5-E1032-INF).
- The gateway-bff composite route for SCR-31 is published (RWB-PLT-N001-CON; DP-19).
- The store and the intake workflow are declared (RWB-P5-E1024-APP, RWB-P5-E1049-APP), so the release deploys a capability that exists and not a shell.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7). The baseline it deploys is RWB-P5-E1032-APP's and the values it injects are RWB-P5-E1032-INF's; both are declared before the release and neither blocks the chart work.
- The release date 30 November 2026 is the legacy one and is tentative (ASM-1764), and the story carries Status Draft (realignment v1) because no approval of the realigned story is recorded (ASM-1765).

### 4. Flow

1. The pipeline builds the service image and the contract jar, runs the unit, component and contract tests, scans the image and the dependencies, and publishes one chart version.
2. The chart deploys the API deployment and the worker deployment with the rwb-document login, the namespace `rwb-recovery`, the task queue `rwb-document`, the codec, the build ID of the release and the values of RWB-P5-E1032-INF.
3. The worker scaling step enables KEDA on the queue backlog of `rwb-document`, so the pool grows with the 15-minute run and the front stays at its fixed replica count.
4. The migration step applies the `rwb_document` sequence of the release and refuses to run when the target schema is not `rwb_document`; the intake migration `V1032_1__intake_match.sql` is one step of it.
5. The topic step creates or verifies `rwb.document.events.v1` with its partitions, its replication factor, its retention, the three retry topics at 1 minute, 10 minutes and 1 hour and its `.dlt` topic, and records the ACL of the producer and of the consumer groups.
6. The Schedule step registers the intake Schedule: workflow `DocumentIntakeWorkflow`, queue `rwb-document`, namespace `rwb-recovery`, every 15 minutes in business hours, overlap policy skip and a catch-up window of one run, its ID fixed by the release so a second apply changes nothing.
7. The flag step sets `rwb.document.intake-autoattach` from the values of the environment; the legacy name `rwb.dochub.autoattach` is recorded as retired and is not deployed (ASM-1766).
8. The dashboards are published with the six series and the environment, release and build ID as dimensions.
9. The four alerts are wired to their message identifiers and to their runbook entries: MSG-P2-004 for a failed run, MSG-P7-003 for failed decision records, MSG-P5-003 for held items and MSG-GEN-006 for a dependency that is not available.
10. A smoke step in DEV drops one synthetic notice in the hold container with the case ID "RW-2026-000123", waits for one Schedule run, confirms one document, one DOCATT record and one attach event, forces one decision-record failure to see the alert, and confirms that the item returned to PENDING and the environment is restored.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The chart render or the migration job fails | The deployment stays unready and the pipeline stops; no traffic, no offset and no migration is left half applied | None | AC1 |
| X2 | The migration step is pointed at a schema other than `rwb_document` | The step refuses and the release stops | None | AC1 |
| X3 | A run of the intake Schedule fails, or runs past its threshold | The run-failure alert fires with MSG-P2-004 naming the run, the time and the runbook path; the Schedule retries on its next interval | MSG-P2-004 | AC4 |
| X4 | The decision-record write fails during a run | The run stops at the failing item, MSG-P7-003 is raised, the item stays PENDING and the decision-record alert fires with the count of failed records | MSG-P7-003 | AC4, AC6 |
| X5 | The feature flag is off in an environment | No automatic attach runs: `matchStep` sets every classified item to NO_MATCH and the items reach the reviewer; the flag is not a way to stop a run in progress | None | AC1, AC6 |
| X6 | A dependency is not available, or its credential has expired | The run fails closed, the item stays PENDING, the dependency alert fires with MSG-GEN-006 naming the system and the runbook entry names the rotation | MSG-GEN-006 | AC4, AC6 |
| X7 | The Schedule is registered twice, or a foreign job is registered on the queue | The Schedule check fails the release: one Schedule ID, one workflow, one queue | None | AC3 |
| X8 | A dashboard series is missing, or an alert carries no message identifier or no runbook link | The observability check fails the release | None | AC5, AC6 |
| X9 | A new build is promoted while runs are open | The open runs replay on the new build from their history; the dashboards show both build IDs | None | AC1, AC5 |
| X10 | The lag of the attach-event consumer group passes its threshold | The lag alert fires; the runbook entry names the group, the topic and the partition | Not specified in the source documents (GAP-0994; ASM-1768) | AC5, AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the workflow kit, the topic provisioning, the migration conventions and the flag library; no application code is built here |
| Negotiable | Replica counts, resource sizes, lag and age thresholds, intervals and quotas are environment values |
| Valuable | Makes the intake path observable, restartable and provable before the release date, and keeps the automatic attach reversible |
| Estimable | One chart, one migration gate, one Schedule, one flag, six series, four alerts and five runbook entries |
| Small | Fits one sprint with the runbook |
| Testable | Every criterion tests an artefact: the chart renders, the migration refuses a foreign schema, the Schedule exists once, an alert fires on a synthetic metric, the smoke run passes |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the intake-match capability for rwb-document

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
    Then the migration step applies the rwb_document sequence and refuses a target schema other than rwb_document
    Then worker versioning is enabled and a new run goes to the new build while the old build drains
    Then the deployment registers no Quartz job and no scheduler table

  Scenario: AC2 The topic and its retry and dead-letter topics are provisioned with their ACLs (new, D-RCV-60)
    Given the release of this story and the platform event epic
    When the topic step runs
    Then rwb.document.events.v1 exists with its partitions, its replication factor and its retention
    Then the retry topics at 1 minute, 10 minutes and 1 hour and the .dlt topic exist for it
    Then the producer ACL is granted to the rwb-document principal only
    Then the consumer ACLs of rwb-case and rwb-agent are granted on the topic
    Then a topic outside rwb.document.events.v1 and rwb.decision-record.v1 is refused by the release
    Then the deployment subscribes to no topic of this service, because the path is started by the Schedule

  Scenario: AC3 The 15-minute intake Schedule is registered in Temporal and in no other scheduler (new, D-RCV-60)
    Given the deployed release and the namespace rwb-recovery
    When the Schedule step runs and is applied a second time
    Then one Schedule exists with the ID fixed by the release, the workflow DocumentIntakeWorkflow and the queue rwb-document
    Then its interval is every 15 minutes in business hours and its overlap policy is skip with a catch-up window of one run
    Then the second apply creates no second Schedule and changes nothing
    Then no Quartz job, no scheduler table and no cron entry exists in the release
    Then a run that fails is retried on the next interval and the items it touched are back in PENDING
    Then the exact business-hours window and the catch-up policy are Not specified in the source documents (GAP-0994; ASM-1767)

  Scenario: AC4 The failed-run and decision-record alerts fire with their identifiers (new, D-RCV-60)
    Given the published alert rules of the deployment
    When a synthetic run fails and a synthetic decision-record write is forced to fail
    Then the run-failure alert fires with MSG-P2-004 naming the run, the time, the business date and the runbook path
    Then the decision-record alert fires with MSG-P7-003 and the count of failed records of the run (message text: Not specified in the source documents (GAP-2449))
    Then each alert names the Schedule ID, the build ID and the environment
    Then each alert carries a message identifier and one runbook link
    Then no alert payload carries OCR text, a file name, an account number or a customer identifier

  Scenario: AC5 The dashboards show the six series for match outcomes and held items (new, D-RCV-60)
    Given the published dashboards of the deployment
    When a synthetic run produces matched items, held items of each status and one failure
    Then the dashboards show items by match status, the age of the oldest held item, documents attached per run, the count of files stored for review, decision-record failures per run, and the queue backlog and age of the task queue
    Then each series carries the environment, the release and the build ID as dimensions
    Then a held item, a failed run and a decision-record failure are visible on the dashboards before any alert is read
    Then no panel shows OCR text or a customer identifier

  Scenario: AC6 The flag, the runbook and the rollback are exercised (new, D-RCV-60)
    Given the published runbook, the flag and the rollback of the release
    When the flag rwb.document.intake-autoattach is turned off in SIT and one Schedule run is waited for
    Then every classified item of that run is held with match_status NO_MATCH and no document is stored
    Then the legacy flag rwb.dochub.autoattach appears in no values file, chart or runbook
    When a failed run, a held item, a stuck retry, an unavailable dependency and a lagging group are simulated
    Then each condition maps to one runbook entry with the check, the owner role and the recovery step
    Then the rollback redeploys the previous chart with its own build ID and the open runs finish on the old build
    Then the smoke run ends with one document, one DOCATT record and one attach event, no duplicate, and the environment restored

  Scenario: AC7 No environment value is hard-coded and the release exposes only the four intake operations (new, D-RCV-60)
    Given the chart, the values files and the ingress of the deployed release
    When the chart is rendered and the ingress is inspected
    Then a hard-coded replica count, threshold, interval, quota or flag is refused and each value comes from the values file of its environment
    Then the four intake operations are the only operations exposed through the chart and its ingress
    Then the release declares no path of its own and SCR-31 is reached through the gateway-bff composite route

  Scenario: AC8 The four intake operations answer 401, 403 and 404 (new, D-RCV-60)
    Given the ingress of the deployed release
    When a request reaches an intake operation without a credential, with a credential of another service, or to an unknown path
    Then the answer is 401 for a request without a credential, 403 for a credential of another service and 404 for an unknown path
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One login, one task queue and one schema per service: the release carries the rwb-document login, polls `rwb-document` only and migrates `rwb_document` only | Arch v5 slide 41; DP-02; DP-15 |
| BR2 | The release publishes on `rwb.document.events.v1` and `rwb.decision-record.v1` only and subscribes to no topic of this service | Arch v5 slides 16, 42 and 43; DP-09; DP-14 |
| BR3 | One trigger and one scheduler: the intake starts on the `DocumentStored` event on queue `rwb-document` in namespace `rwb-recovery` with KEDA-scaled workers; no Quartz job, no scheduler table and no cron entry exists; the ledger completeness check runs on the ledger ingest window of DP-06 with no Temporal Schedule and no cron entry of this service | Arch v5 slide 44; DP-10; `ASM-1767` |
| BR4 | The automatic attach is reversible by one flag, `rwb.document.intake-autoattach`, which replaces the legacy `rwb.dochub.autoattach` | legacy section 13; DP-14; `ASM-1766` |
| BR5 | Every alert carries a message identifier and the agreed text and links one runbook entry | Template and Rules §R7.2 s14 |
| BR6 | No environment value is hard-coded: replicas, resources, thresholds, intervals, quotas and the flag come from values files and parameters; the communications module declares no business-owned value, so no notice parameter is named here and DP-06 applies to it as a path without a value | Template and Rules §R7.2 s17 |
| BR7 | Dashboard series, alert payloads and the runbook carry counts, identifiers, statuses, business dates and build IDs only, never OCR text, a file name or a customer identifier | ADR-023; CTL-11 |
| BR8 | The release exposes the four intake operations through the chart and its ingress and declares no path of its own; SCR-31 is reached through the gateway-bff composite route | DP-19; RWB-P5-E1032-CON 12.1 |
| BR9 | A failing release never replaces a working one: the previous build stays in force until the new build passes its tests and its smoke run | DP-10 |
| BR10 | An item a failed run touched is never deleted and never left matched on a guess: it stays PENDING for the next run, and a decision-record failure leaves nothing stored; whether a held item or a refused attach leaves a DOCATT entry is Not specified in the source documents (GAP-2446) | R-UNI-39; legacy X13 |
| BR11 | The release provisions no ACE grant, no view, no data-lake route and no inbound consumer of this path | D-RCV-35 U1; ADR-010; DP-05; DP-17 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the contract tests pass | Deploying |
| Deploying | Migration applied and worker registered | The `rwb_document` sequence applied and the worker polls `rwb-document` | Ready |
| Ready | Schedule registered | One Schedule with the release ID, the workflow and the queue | Scheduled |
| Scheduled | First run completes | The run finishes and its counters reach the dashboards | In use |
| In use | Release superseded | A new chart version passes its tests | Rolling |
| Rolling | All workers on the new build | The old build drains its open runs | In use |
| In use | Flag off | `rwb.document.intake-autoattach` is turned off in the environment | Held |
| Held | Flag on | The flag is turned on again and the next run matches | In use |
| In use | Smoke run failed | The Schedule check, the alert check or the smoke step fails | Blocked |
| Blocked | Previous build restored | The previous chart is redeployed or a later build passes the smoke run | In use |

The item states PENDING, MATCHED, NO_MATCH, MULTIPLE, CONFLICT, CASE_CLOSED and NO_TYPE are the app story's runtime and are not states of this deployment.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the migration gate, the Schedule step, the dashboards and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the Schedule, the topic ACLs, the consumer quotas, the flag library and the restart of a run |
| Platform event owner | Owns `rwb.document.events.v1`, its retry and `.dlt` topics, its schema subject and its retention |
| Release manager | Approves the promotion of one artefact and may block it on a failing smoke run |
| On-call operator | Runs the five runbook entries and opens an incident when a failed run, a held item or a lag persists |
| rwb-document owner | Owns the matcher, the store and the migration the release applies |
| Data steward | Confirms that no dashboard, alert or runbook carries OCR text or a customer identifier |
| RW-AUDIT | Reads the run history, the alert trail and the runbook |

The worker runs as the rwb-document service identity (DP-02), carried by the chart as a secret reference and never as a literal. The login name is Not specified in the source documents (GAP-0994; ASM-1768).

Each of the four intake operations checks the caller with an rwb-access authorise call (DP-08) before it acts; the check's role mapping is Not specified in the source documents (DOR-RWB-P5-E1032-OPS-6).

### 11. Data

| Item | Content | BR Field ID |
|---|---|---|
| Deployment values | Image digest, chart version, replica counts for the API and the worker, resource requests and limits, probe paths and timings, log level, namespace, task queue, build ID, feature switch, KEDA backlog threshold, trigger name | Not specified in the source documents (DOR-RWB-P5-E1032-OPS-7) |
| Task queue | `rwb-document` in namespace `rwb-recovery`, polled by the worker of this service only | Not specified in the source documents (DOR-RWB-P5-E1032-OPS-7) |
| Topic | `rwb.document.events.v1` with its partitions, replication factor, retention and key, its three retry topics and its `.dlt` topic; `rwb.decision-record.v1` published by the library; no subscription of this service | Not specified in the source documents (DOR-RWB-P5-E1032-OPS-7) |
| Schema | `rwb_document`, migrated by its own per-service Flyway sequence; the intake migration `V1032_1__intake_match.sql` is one step of it | Not specified in the source documents (DOR-RWB-P5-E1032-OPS-7) |
| Trigger | `DocumentIntakeWorkflow` started by the `DocumentStored` event, queue `rwb-document`, namespace `rwb-recovery`, workers scaled by KEDA on the backlog threshold; overlap policy and duplicate-start rule Not specified in the source documents (CG-ALL-5846) | Not specified in the source documents (DOR-RWB-P5-E1032-OPS-7) |
| Flag | `rwb.document.intake-autoattach`, on in DEV and SIT for the tests, from the values of each environment; the legacy `rwb.dochub.autoattach` is retired | Not specified in the source documents (DOR-RWB-P5-E1032-OPS-7) |
| Dashboard series | Items by match status, age of the oldest held item, documents attached per run, files stored for review, decision-record failures per run, queue backlog and age; dimensions environment, release, build ID | Not specified in the source documents (DOR-RWB-P5-E1032-OPS-7) |
| Runbook entries | Failed run, held item, stuck retry, unavailable dependency, lagging group; each with the check, the owner role and the recovery step | Not specified in the source documents (DOR-RWB-P5-E1032-OPS-7) |
| Alerts | Four rules and one runbook entry each: MSG-P2-004 for a failed run, MSG-P7-003 for failed decision records, MSG-P5-003 for held items, MSG-GEN-006 for an unavailable dependency; the lag alert carries the identifier placeholder of GAP-0994 | Not specified in the source documents (DOR-RWB-P5-E1032-OPS-7) |
| Secrets | The rwb-document login secret, the Kafka client credential, the Temporal mTLS material and the storage identity reference, all from the platform secret store | Not specified in the source documents (DOR-RWB-P5-E1032-OPS-7) |
| Test data | One synthetic notice for case "RW-2026-000123", one forced decision-record failure and one flag-off run; synthetic identifiers only | Not specified in the source documents (DOR-RWB-P5-E1032-OPS-7) |
| Case document link | The case-side document link table and its field IDs are Not specified in the source documents (GAP-0742) | Not specified in the source documents (DOR-RWB-P5-E1032-OPS-7) |
| Decision record entry (DOCATT attach) | `decision_record` entry of the DOCATT attach: document reference, intake item and match method in `actions`; classifier version in `model_version`; confidence and type candidates in `recommendation`; message id of a refusal in `outcome`; `final_call` value Not specified in the source documents (GAP-2445); the columns are proposed in rwb_decision and their schema is Not specified in the source documents (GAP-2444) | Not specified in the source documents (DOR-RWB-P5-E1032-OPS-7) |

The deployment topology (cluster names, node pools, replica counts, resource sizes, zone spread, ingress class and probe timings) belongs to each environment and is set by the platform team in its values file; the chart exposes every one of them as a value and this story fixes only their names and the rule that they are never hard-coded.

Capacity values of the intake-match path (GAP-0993): the worker replica count, the request and limit set, the KEDA ceiling, the growth figure of `document_text` and its index budget, the clearing age of `rwb-quarantine`, the hold container capacity and the scan rate per hour are Not specified in the source documents (GAP-0993). Each is set in the environment values files of its environment. The four-worker figure and the 500-page sample of the OCR module are test values, not sizing targets.

**Probes.** Readiness answers healthy only after the worker has polled `rwb-document` once and the API has answered its health path; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database or commits an offset, and a failing dependency is reported as not ready, never as live-and-broken.

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Owner | Notes |
|---|---|---|---|
| None | — | — | The four intake operations — `GET /api/recovery/document/v1/intake-items`, `GET /api/recovery/document/v1/intake-items/{intakeItemId}`, `GET /api/recovery/document/v1/intake-items/{intakeItemId}/content` and `POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve` — are declared by RWB-P5-E1032-CON and implemented by RWB-P5-E1032-APP; this deployment exposes them through the chart and its ingress and declares no path of its own. The probes are cluster-internal and are not part of the API surface |

#### 12.2 REST operations consumed

| Method | Path | Owner | Story | Note |
|---|---|---|---|---|
| None | — | — | — | The deployment carries no REST client of its own. At run time the app story's clients reach `rwb-case` and `rwb-decision` over the private routes of RWB-P5-E1032-INF; the chart's only start-up calls are the Temporal frontend, the Kafka brokers and the health paths of its own dependencies |

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| None | — | — | — | `rwb.document.DocumentAttached.v1` on `rwb.document.events.v1` is published by the app story, and `DecisionRecorded` on `rwb.decision-record.v1` by the local decision-record library through the relay (DP-03, DP-09); the deployment publishes nothing of its own |

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| None | — | — | This path consumes no event: the trigger is the intake Schedule. The consumer groups of `rwb-case` and `rwb-agent` on `rwb.document.events.v1` are theirs and not deployed here |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| `DocumentIntakeWorkflow` | Workflow, from the L3 "Document intake" template | `rwb-document` | Registered by the worker of this release with the build ID and worker versioning; owned by RWB-P5-E1049-APP |
| `matchStep` | Activity | `rwb-document` | Registered by the same worker with the kit's retry policy; owned by RWB-P5-E1032-APP |
| Outbox relay | Platform relay | not a worker | Deployed with the library; publishes `rwb.document.events.v1` and `rwb.decision-record.v1` on its one-minute interval (JOB-11) |

**Build ID and versioning.** The build ID is the one supplied by the workflow kit for the release commit; worker versioning is enabled and a new build takes new runs while the old build drains. The build ID format and the versioning policy are Not specified in the source documents (GAP-0994; ASM-1768).

**Workflow ID and start.** The start trigger is the `DocumentStored` event from the scanner folder, SFTP or mailbox pickup (JOB-12), or a child start from a stage workflow. The workflow ID form and the start rule (start or signalWithStart, duplicate-start policy) are Not specified in the source documents (CG-ALL-5846).

#### 12.6 Schedules

| Schedule | Workflow | Queue | Interval | Note |
|---|---|---|---|---|
| The intake Schedule (JOB-12 Document intake) | `DocumentIntakeWorkflow` | `rwb-document` | Every 15 minutes in business hours | Registered by this release from its values, with the ID fixed by the release, overlap policy skip and a catch-up window of one run; a run that fails is retried on the next interval and the items it touched stay PENDING. The exact business-hours window and the catch-up policy are Not specified in the source documents (GAP-0994; ASM-1767) |

No other Schedule, cron entry or Quartz job is registered by this release, and the outbox relay runs on the platform's one-minute interval (BR3).

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `document_intake` | P5 (`rwb_document`) | Created or altered by the `rwb_document` sequence of the release; written by the app story, never by the deployment |
| `document_text` | P5 (`rwb_document`) | Created by the intake path's own migration step; read by the app story |
| `document` | P5 (`rwb_document`) | Created by the store's migration in the same sequence; written by the store |
| `document_hub_parameter` | P5 (`rwb_document`) | Created by the store's migration; the three parameter rows are loaded as data by the reference data administrator, never as a chart value |
| `outbox_event`, `outbox_delivery`, `processed_event`, `idempotency_key`, `decision_record` | PLT library, created in `rwb_document` | Created by the library migrations in the same schema; written by the app story and the relay |

The release applies the `rwb_document` sequence of this key and no other: no ACE view, no other service's table and no lake object is created, altered or read (DP-01, DP-05, DP-15, DP-17).

#### 12.8 Contract fakes

| Fake | Story | Used for |
|---|---|---|
| None | — | No fake is deployed. The contract fakes of RWB-P5-E1032-CON and the dependency stubs of RWB-P5-E1032-INF are test-only workloads and are not promoted into SIT, UAT or production |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 0 consumed by the deployment | The four intake operations are the app story's; the probes are cluster-internal |
| Kafka | 0 published, 0 consumed here; 1 topic configured with retry and `.dlt` | `rwb.document.events.v1` with its ACLs and `rwb.decision-record.v1` published by the library; no subscription |
| Temporal | 1 workflow, 1 activity, 1 Schedule | Worker on `rwb-document` with a pinned build ID, worker versioning and KEDA scaling; the intake Schedule every 15 minutes in business hours |
| File | 3 containers | The values point at `rwb-docs`, `rwb-docs-legal` and `rwb-quarantine` of RWB-P5-E1032-INF; no file is built or moved by the deployment |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | The release migrates `rwb_document` only and reads no other schema | none |
| DP-03 | DecisionLogWriter, decision log | The local record library is deployed with the relay and publishes to `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | No ACE grant, no view and no route in this release | none |
| DP-06 | Parameters, casewf.config | The three parameters stay rows read through the client library; no chart value carries them | H RWB-PLT-E1042-CON |
| DP-07 | Reference data, LOV | The five lists stay reference rows; no chart value carries them | H RWB-PLT-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | The topic with its retry and `.dlt` topics, the inbox and the relay | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | The worker, the task queue, worker versioning and the intake Schedule from the kit; no Quartz job | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | The release declares no REST path and no client of its own; the private routes are RWB-P5-E1032-INF's | none |
| DP-15 | V0001 baseline, migration | The `rwb_document` sequence with its intake step and a foreign-schema refusal | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | The ingress registers the service base for the gateway-bff edge; no screen is deployed | H RWB-PLT-N001-CON |

**Dependencies from the DP table.** The DP table also adds the contracts C RWB-P3-E1042-CON and C RWB-P3-E1043-CON and the authorise contract RWB-P4-E1037-CON. The header metadata rows keep the contract dependencies as the work package fixes them.

DP-10 is the substantive row of this story: JOB-12 stops being a Quartz job on a shared scheduler and becomes a Temporal Schedule on the service's own queue, so the release registers the Schedule, the worker and the build ID, and the operator restarts a run through the Schedule rather than a scheduler table. DP-01 and DP-15 keep the migration inside `rwb_document` and make the step refuse a foreign schema. DP-02 is not in the pattern list of the key and is applied by the chart anyway: one login, carried as a secret reference. DP-03 and DP-09 deploy the library, the relay, the topic and the retry and `.dlt` topics the attach event needs. DP-06 and DP-07 keep the parameters and the five lists out of the values files. DP-11 and DP-05 are applied by absence: the release declares no REST path of its own, no client and no ACE grant. DP-19 registers the ingress path the edge calls and deploys no screen.

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-document/` overlay | API deployment, worker deployment, config map, secret references, probes, task queue, namespace, build ID, KEDA rule, Schedule definition and flag |
| `helm/rwb-document/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, flag value, build ID, Schedule ID and interval, KEDA threshold, container references (ASM-1768) |
| Pipeline stage | Build, unit and contract tests, image and dependency scan, chart publish, migration gate, topic step, Schedule step, smoke run, promotion |
| Migration step | The `rwb_document` sequence with `V1032_1__intake_match.sql`; a target schema other than `rwb_document` is refused |
| Topic step | `rwb.document.events.v1` with its three retry topics and its `.dlt`, the producer ACL and the consumer ACLs of rwb-case and rwb-agent |
| Schedule step | The intake Schedule with its release ID, the workflow, the queue, the interval, the overlap policy and the catch-up window, idempotent on the ID |
| Dashboards | The six series of section 11 with the three dimensions |
| Alerts | Four rules, each with a message identifier or its placeholder and one runbook entry |
| Runbook | Five entries: failed run, held item, stuck retry, unavailable dependency, lagging group |

**Alert mapping**

| Message ID | Condition | Alert | Route |
|---|---|---|---|
| MSG-P2-004 | A run of the intake Schedule failed or ran past its threshold | Run-failure alert naming the Schedule ID, the run, the time, the business date and the runbook path | Platform on-call, page in business hours, else ticket |
| MSG-P7-003 | The decision-record write failed during a run | Decision-record alert naming the run, the count of failed records and the retry state of the items | Platform on-call and the rwb-decision owner, page |
| MSG-P5-003 | Items are held for a person, or a document is stored for review | Held-items alert on the age of the oldest held item and the count per status | Reviewer lead and the data steward, ticket |
| MSG-GEN-006 | A dependency is not available or its credential has expired | Dependency alert naming the system and the health state | Platform on-call, page |
| Not specified in the source documents (GAP-0994; ASM-1768) | The attach-event consumer group lags past its threshold | Lag alert naming the group, the topic, the partition and the lag | Platform on-call, ticket |

**Retry and offsets.** The Schedule retries a failed run on its next interval and never runs two runs at once, because the overlap policy is skip. The activity retry is the kit's three attempts with back-off; the deployment adds no retry of its own. The relay commits its offset after the outbox row is marked sent, so a restart republishes nothing twice, and the consumer inbox of rwb-case makes a replay harmless (DP-09).

**Rollback.** A release that fails the smoke run is not promoted. A release already promoted is rolled back by redeploying the previous chart version with its own build ID, which keeps the old build serving its open runs until they finish; the Schedule keeps its ID and points at the workflow, so a rollback changes the build under it and not the timer. Items a failed run touched are PENDING and are selected again; no data repair is needed, because the release writes no business row of its own and the migration is additive.

**Feature switch.** `rwb.document.intake-autoattach`. On: `matchStep` matches, stores or holds. Off: every classified item is set to NO_MATCH and reaches the reviewer, and the flag is not a way to stop a run in progress, which is what the Schedule and the runbook are for. The legacy name `rwb.dochub.autoattach` appears in no value, chart or runbook (ASM-1766).

**Done when.** The chart renders for DEV, SIT and UAT with a pinned digest and the build ID, the migration step refuses a foreign schema, the topic and its retry and `.dlt` topics exist with their ACLs, one Schedule exists with the release ID and the queue `rwb-document` and a second apply changes nothing, the flag-off run holds every classified item, the six series and the four alerts are published with their identifiers or placeholders and their runbook links, the smoke run produces one document, one record and one event with no duplicate, and the five runbook entries are reviewed by the on-call rota. The alert thresholds, the intervals and the catch-up window are Not specified in the source documents (GAP-0994; ASM-1768).

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-004 | A run of the intake Schedule failed or ran past its threshold | {job} failed at {time} for business date {date}. Follow run book {runbook}. |
| MSG-P7-003 | The decision-record write failed during a run | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P5-003 | Items held for a person, or a document stored for review | Some fields need checking. The document is in the review queue. |
| MSG-GEN-006 | A dependency is not available or its credential has expired | {system} is not available. Your request is queued and will be retried. |
| Identifier pending | The attach-event consumer group lags past its threshold | Not specified in the source documents (GAP-0994; ASM-1768) |

MSG-P5-003 and MSG-P7-003 are the legacy texts of section 14 of RWB-E1-032 and are unchanged. MSG-P2-004 is the job-failure text of the observability epic and MSG-GEN-006 the platform text for an unavailable system; both are used here with their agreed wording. The lag alert has no identifier in the source set, so it carries the placeholder until the Error and Message Standard names it. An alert payload names counts, statuses, business dates, the Schedule ID, the build ID and group names only, never OCR text, a file name, an account number or a customer identifier.

### 15. Screens and states

The deployment has no screen of its own. Its operator-facing surfaces are the pipeline run view, the release view, the Temporal Web UI, the dashboards, SCR-31 Document review queue through the gateway-bff composite route, and the runbook. SCR-31 is served by the app story and the route of RWB-PLT-N001-CON; the deployment only registers the ingress path. States of SCR-31: loading as in Screen Specifications v1; empty, error and no access: Not specified in the source documents (CG-ALL-5850). The Temporal Web UI stays behind Entra ID: RW-PLATADM operates and RW-AUDIT reads, and payloads are decoded only through the codec server under break-glass. SCR-44 Interface and job monitor belongs to Epic 2 and shows the same run data from there; this release publishes the run records the monitor reads. States of SCR-44: empty, loading, error and no access are Not specified in the source documents (CG-ALL-5851).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P5-E1032-OPS-01 | AC1, BR1, BR11 | NFR | The chart renders for three environments with a pinned digest, the build ID, the login reference and worker versioning; a foreign migration target is refused; the worker polls only `rwb-document` |
| TC-P5-E1032-OPS-02 | AC2, BR2 | NFR | The topic with its three retry topics and its `.dlt`; the producer and consumer ACLs; a fourth topic refused; no subscription of this service |
| TC-P5-E1032-OPS-03 | AC3, BR3 | NFR | One Schedule with the release ID, the queue and the interval; a second apply changes nothing; a failed run is retried on the next interval and its items are PENDING; no Quartz job and no scheduler table |
| TC-P5-E1032-OPS-04 | AC4, BR5, BR10 | NFR | A forced failed run and a forced decision-record failure raise the two alerts with MSG-P2-004 and MSG-P7-003, one runbook link each, and no personal data |
| TC-P5-E1032-OPS-05 | AC5, BR7 | NFR | The six series with the three dimensions; a held item, a failed run and a decision-record failure visible before the alerts |
| TC-P5-E1032-OPS-06 | AC6, BR4, BR9 | NFR | The flag off holds every classified item; the legacy flag name appears nowhere; five synthetic conditions map to five runbook entries; the rollback redeploys the previous build; the smoke run leaves no duplicate |
| TC-P5-E1032-OPS-07 | BR2, BR8 | NFR | Contract test: the four intake operations, the events and the activities of section 12 match their declared shapes and paths; a shape outside the declared set is refused; the activity `matchStep` is registered on `rwb-document` |
| TC-P5-E1032-OPS-08 | BR1, BR11 | NFR | Boundary test: each table of section 12.7 is written only by its owner; a write to a table outside the owner list is refused; no ACE view, other service table or lake object is touched |
| TC-P5-E1032-OPS-09 | AC7, BR6 | NFR | A chart with a hard-coded replica count, threshold, interval, quota or flag is refused; the same values come from the values files of each environment |
| TC-P5-E1032-OPS-10 | AC7, BR8 | NFR | The four intake operations are reached only through the chart and its ingress; a path declared by the release is refused; SCR-31 is reached through the gateway-bff composite route |
| TC-P5-E1032-OPS-11 | AC3, BR3 | NFR | A DocumentStored event starts one run per document with KEDA-scaled workers; a duplicate event starts no second run |
| TC-P5-E1032-OPS-12 | AC8 | NFR | Requests to the four intake operations without a credential, with a credential of another service and to an unknown path; the answers are 401, 403 and 404 respectively |

### 17. Guardrails

- No business value in a values file: the patterns, the threshold, the type list, the owner role and the alert role are parameters and reference rows, never a deployment value.
- No personal data in logs, dashboard series, alert payloads, the runbook or the workflow history: counts, statuses, identifiers, business dates and build IDs only, and payloads stay encrypted.
- One login, one task queue and one schema per service: the release carries the rwb-document login, polls `rwb-document` and migrates `rwb_document` only (DP-02, DP-15).
- The release deploys no ACE grant, no view, no data-lake route and no inbound consumer of this path (DP-05, DP-17, BR11).
- One Schedule and one scheduler: no Quartz job, no scheduler table and no cron entry besides the intake Schedule (BR3).
- The topic and its retry and `.dlt` topics exist with their ACLs before the worker starts (DP-09, BR2).
- An item a failed run touched is never deleted and never left matched on a guess; a decision-record failure leaves nothing stored (BR10, R-UNI-39).
- The release pins the image digest, the chart version and the build ID; a rebuild between environments is not allowed, and a failing smoke run never replaces a working build.
- No secret is written into a values file, a chart template, a dashboard or the runbook; all secrets come from the platform secret store (NFR-052).

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| Arch v5 slide 44 | JOB-12 Document intake runs every 15 minutes, owned by rwb-document, as a schedule in the owning service | The intake Schedule, the worker and the build ID | TC-P5-E1032-OPS-01, TC-P5-E1032-OPS-03 |
| Arch v5 slide 41 | One schema, one API base, one topic and one task queue per service | The migration gate, the topic step and the queue binding | TC-P5-E1032-OPS-01, TC-P5-E1032-OPS-02 |
| Arch v5 slide 42 | rwb-document publishes on `rwb.document.events.v1`; DocumentStored is consumed by rwb-case and rwb-agent | The topic, its ACLs and the absence of a subscription of this service | TC-P5-E1032-OPS-02 |
| Arch v5 slides 38 and 20 | The platform provides the template, the schemas and logins, the topic set and Temporal before the wave 1 services | The bindings this release verifies and the pieces it deploys | TC-P5-E1032-OPS-01, TC-P5-E1032-OPS-03 |
| ADR-023 | Observability per service | The six series, the four alerts and the five runbook entries | TC-P5-E1032-OPS-04, TC-P5-E1032-OPS-05 |
| NFR-068 | A failing interface, job or agent raises an alert to a named owner within its target | The run-failure, decision-record and dependency alerts with their routes | TC-P5-E1032-OPS-04 |
| NFR-052 | Secrets in the key store and never in code or configuration | Secret references only, and the secret scan of the release | TC-P5-E1032-OPS-01 |
| REQ-DCM-007, REQ-DCM-005, REQ-DRI-004 | The attach path this release runs: one clear case attaches, an uncertain one is held, every decision is recorded | The Schedule, the flag, the flag-off behaviour and the decision-record alert | TC-P5-E1032-OPS-03, TC-P5-E1032-OPS-04, TC-P5-E1032-OPS-06 |

### 19. Out of scope

- The build of the matcher, the activity, the two attach services, the four operations and the Unmatched tab (RWB-P5-E1032-APP).
- The contract documents, the shapes, the event schema and the fakes (RWB-P5-E1032-CON); this story only deploys and gates them.
- The worker compute, the storage, the hold container, the topic binding, the ACLs, the identity and the route (RWB-P5-E1032-INF).
- The Temporal cluster, the namespace, worker versioning and the codec server as platform components (RWB-PLT-WF, RWB-PLT-E1071-CON).
- The topic provisioning, the schema registry and the `.dlt` retention as platform components (RWB-PLT-EVT, RWB-PLT-TE006-CON); this story configures the ACLs and the group it needs.
- The ingestion, OCR and classification jobs of the same workflow (RWB-P5-E1049-APP, RWB-P5-E1050-APP, RWB-P5-E1053-APP).
- The SCR-44 screen and the full interface and job monitor (Epic 2, Epic 8).
- The real cross-service journey of the path with all services live (RWB-ITG-E1032-ITG).
- The exact cluster topology, node pools, replica counts, alert thresholds, the business-hours window and the catch-up policy, which are set per environment by the platform team (GAP-0994).
