# RWB-P1-E1015-OPS Freshness stamp per data product

Version 3. 27 November 2026.
SCB Collections and Recovery. Henka Group.
(C) Siam Commercial Bank and Henka Pte Ltd

### Version 3 changes

- Applied RD-P1-003, RD-P1-040 and RD-P1-044: three retry topics and .dlt, outbox, one business-date workflow, late event at 05:30, one Schedule, task-queue scaling, topics verified and not created; fixed findings #1, #3, #4, #7, #10, #11 and #14.
- Applied RD-P1-045 (rollback with forward-only migrations) and RD-P1-043 (flag-off behaviour, alerts not armed); fixed findings #2, #19 and, with RD-P1-021 and RD-P1-028, #8, #12 and #13.
- Fixed findings #5, #9, #15, #17, #18, #21, #22 and #24: alert table with message ID or none, PROD, acceptance criteria with concrete checks. Finding #16 is fixed by removing the reused test case rows; new rows are a delivery step (#17).
- Findings #6 and #20 are fixed except for values no source gives (alert thresholds, workload identity), pending under NEW-GAP-S3-9 and NEW-GAP-S3-6; finding #23 is a design document correction requested in the edit log.
- Finishing pass (requests W2-tests-1062, W5-runtime-0064; test case backfill): Test Cases v9 IDs are cited in section 16 and the traceability table.

| Item | Value |
|---|---|
| Story key | RWB-P1-E1015-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-015 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP05, DP07, DP09, DP10, DP11, DP15, DP19 |
| Parallel lane | L-P1-I |
| Ready to start | After RWB-P1-E1015-CON and RWB-PLT-N002-INF; checks that need the application image wait for RWB-P1-E1015-APP; switching the feature on in SIT, UAT and PROD waits for the RWB-ACE-001 dependency gate |
| Size | Not specified; set by the squad at refinement (DOR-RWB-P1-E1015-OPS-16) |
| Depends on (build) | RWB-P1-E1015-CON, RWB-PLT-N002-INF, RWB-PLT-E1044-CON, RWB-PLT-E1071-CON, RWB-PLT-TE006-CON; RWB-P1-E1015-APP for the application image |
| Contract dependencies | RWB-P1-E1015-CON, RWB-PLT-N002-INF, RWB-PLT-E1044-CON, RWB-PLT-E1071-CON, RWB-PLT-TE006-CON |
| Contract version | rwb-source-data.yaml and AsyncAPI 5.1.0 (API Specification v7) |
| Integration dependencies | None |
| External dependencies | RWB-ACE-001 Section B (feature activation gate) |
| Integration with other stories | Later rwb-source-data OPS stories name this story as their base release (RD-P1-044) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-014, FR-P1-015, FR-P1-016, FR-P1-017) |
| Readiness decisions | RD-P1-001, RD-P1-003, RD-P1-005, RD-P1-021, RD-P1-022, RD-P1-028, RD-P1-040, RD-P1-041, RD-P1-043, RD-P1-044, RD-P1-045 |
| Epic design sign-off | Pending |
| CON Done | Pending |
| Fake published | Pending |
| DEV test data | Pending |
| Status | Draft (RD-P1 decisions applied; delivery pending) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-015 for rwb-source-data. The freshness capability is deployed as the api and worker of the service with its own login, its listener and KEDA scaling on `v_ace_batch_status`, its topic with retry and `.dlt`, one cut-off Schedule per data product, the configuration rows behind `expected_by`, `refresh_cycle` and the product-to-source map, the feature flag until RWB-ACE-001 lands, the dashboards and alerts of the legacy story and its runbook (DP-02, DP-09, DP-10, DP-15). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1015-OPS). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 19 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: applied the binding readiness decisions and story review fixes. Agent: S3-stories.

### 1. Story

As a platform engineer, I want the rwb-source-data release to deploy its API and worker, run its forward-only migration, register the 05:30 Schedule, scale on the Temporal task-queue backlog, verify platform-owned event topics and ACLs, configure its flag, and expose operational alerts, so that the freshness workflow and its business-date gate can be operated safely across environments.

RWB-P1-E1015-OPS owns the chart skeleton, API and worker deployments, probes, migration job, AceIngestCheck worker registration, 05:30 Schedule, readiness/status routes, and P1 Load late, Load failed and stale alert instances (RD-P1-044). RWB-PLT-N002-INF owns the topics; this story verifies their settings and producer ACL and creates no topic or consumer group.

### 2. Business rationale

The P1 release must run one AceIngestCheck workflow per business date and expose whether freshness is late or stale. The primary start is the readiness POST; the 05:30 Schedule and Control-M poll are fallback starts of the same workflow. A completed ALS stamp starts downstream child workflows; the service does not consume its own event topic (RD-P1-040).

Operations must see the 05:30 late event, stale status at expected_by, failed sources, gate holds and duplicate restatements. Rollback is flag off, redeploy the previous tag and repair the schema forward under RD-P1-045.

### 3. Preconditions

- The service chart and pipeline are available. The API Deployment has 2 replicas; worker replica and scaling thresholds are deployment values.
- RWB-P1-E1015-CON version 5.1.0 is baselined; its published fake and DEV test data are pending.
- RWB-PLT-N002-INF provisions the topics and ACLs and shares the settings and ACL evidence.
- The workflow kit, the Temporal namespace rwb-recovery and the observability platform are available.
- DEV and the pipeline test database create the Section B views over the synthetic fixture of RWB-P1-E1065-CON; synthetic ace_batch_run rows for the checks come from that fixture. In SIT, UAT and PROD the Section B migration is not applied until RWB-ACE-001 has landed there (RD-P1-043).
- data_product.expected_by, refresh_cycle and data_product_source are P1-owned rows, changed by reference loads (RD-P1-021); no value is copied into a chart template. Confirm the source_system seed against the ace_batch_run.source_system code list (NEW-ASM-B3).
- Settings (RD-P1-028): `ingest.poll.interval.minutes` = 5 and `rwb.dataengine.freshness.alert-channel` and the alert thresholds are per-environment values-file entries; the flags rwb.dataengine.freshness-stamp and rwb.source-data.ingest-poll-fallback are in the platform flag library. None is a parameter catalog row.
- The checks of AC5, AC10, AC18 and AC19 need the application image of RWB-P1-E1015-APP.

### 4. Flow

1. Build the image and chart, run unit and contract checks and the view conformance test over the views that exist, scan the image, and promote the same digest.
2. Deploy the API and worker workloads with the rwb_source_data secret reference and the forward-only Flyway migration job; the migration completes before the new deployment is ready.
3. Register the AceIngestCheck worker and its four activities on task queue rwb-source-data, and the one Schedule rwb-source-data-ace-late-check at 05:30 Asia/Bangkok, overlap SKIP, catch-up window 1 h.
4. Verify rwb.source-data.events.v1 as provisioned by RWB-PLT-N002-INF: 12 partitions, replication factor 3, 7-day retention, .retry.1m, .retry.10m, .retry.1h, .dlt and the producer ACL. Create no topic and no consumer group on this topic.
5. Configure the KEDA scaler on the Temporal task-queue backlog; do not scale on Kafka consumer lag. The api keeps 2 replicas.
6. Set ingest.poll.interval.minutes = 5 (NEW-ASM-C1) in the values file. expected_by checks are durable timers inside AceIngestCheck and the run closes when every due source is stamped or 24 h after its start (NEW-ASM-C2); register no per-product Schedule.
7. Keep rwb.dataengine.freshness-stamp off in SIT, UAT and PROD until the Section B migration is applied and the ACE dependency gate passes. While it is off the alert rules of the feature are not armed, the health check reports the flag state and the release note names the services waiting on RWB-ACE-001.
8. Publish the dashboards, the alert rules of section 13 and one runbook entry per condition.
9. Run the smoke profile against the readiness and status routes and the contract fake. Keep rwb.source-data.ingest-poll-fallback off whenever Airflow is live; until NEW-GAP-C1 gives its start time the poll is deployed and tested in DEV only and stays off in SIT, UAT and PROD.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Migration fails | The rollout stops; existing pods keep serving; a forward fix is applied | None | AC1, AC13 |
| X2 | Readiness or liveness probe fails | New pods receive no traffic and the release fails | None | AC1, AC14 |
| X3 | The task queue stops draining | The backlog panel and the dependency alert identify the worker | MSG-GEN-006 | AC2, AC6 |
| X4 | A platform-owned topic, retry topic or ACL is missing | Verification fails and deployment is blocked; the service creates no topic | None | AC3 |
| X5 | 05:30 Schedule registration is rejected | The release fails and names rwb-source-data-ace-late-check | None | AC4 |
| X6 | A start arrives while the run of the date is open | USE_EXISTING joins it and the duplicate-start metric rises; Schedule overlap SKIP is a separate rule | None | AC4 |
| X7 | A source is late or failed, or a product is stale, or the gate holds | The alert of section 13 fires within 15 minutes | MSG-P1-001 for stale and hold; none assigned for late and failed | AC6 |
| X8 | A restated batch changes completed_at | duplicate_count rises; the duplicate alert names product, source and business date | None | AC6 |
| X9 | Feature flag is off | No stamp, event or child; readiness LATE; freshness STALE with null businessDate; alerts not armed | None | AC5 |
| X10 | ACE view is unavailable | No stamp is guessed or changed; activity retry, then the dependency alert | MSG-GEN-006 | AC10 |
| X11 | The 05:30 occurrence is missed | It runs once if the outage ends within 1 h; after that it is not run | None | AC17 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the platform topic provisioning, the workflow kit and the observability platform; no application code is built here |
| Negotiable | API replicas are two and the Schedule catch-up one hour; worker resources, KEDA and alert thresholds are environment values |
| Valuable | Makes the freshness pipeline deployable, observable and repeatable, and makes a silent gate hold impossible |
| Estimable | One chart with two workloads, one pipeline stage, one migration job, two probes, one verification step, one registration step, two dashboards and seven alert rules |
| Small | Fits one sprint with the runbook |
| Testable | Every criterion tests an artefact: the chart renders, probes answer, the worker scales, topics are verified, the Schedule is registered and alerts fire on a synthetic metric |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the rwb-source-data freshness capability

  Background:
    Given the service chart is versioned and the contract baseline is rwb-source-data 5.1.0

  Scenario: AC1 Chart deploys in each environment
    Given values files for DEV, SIT, UAT and PROD
    When the chart is rendered and promoted
    Then image digest and chart version are pinned, the API has 2 replicas, API and worker declare readiness and liveness probes and the migration completes before the new pods are ready
    And only the rwb_source_data secret reference is declared, the migration is forward-only and no secret literal appears in values

  Scenario: AC2 Worker scales on the Temporal task queue
    Given AceIngestCheck tasks are queued on rwb-source-data above the values-file backlog threshold
    When the backlog rises and later drains
    Then KEDA adds worker replicas and returns to the values-file minimum
    And no Kafka consumer lag or view-listener lag is a scaler trigger

  Scenario: AC3 Platform topics and ACLs are verified
    Given RWB-PLT-N002-INF has provisioned rwb.source-data.events.v1
    When the deployment verification runs
    Then the topic has 12 partitions, replication factor 3, 7-day retention and the topics .retry.1m, .retry.10m, .retry.1h and .dlt exist
    And the rwb-source-data principal may write the topic and has no consumer group on it
    And this story creates no topic and no consumer group

  Scenario: AC4 One Schedule and durable timers
    Given the rwb-source-data worker is deployed
    When Schedule registration runs twice
    Then exactly one rwb-source-data-ace-late-check Schedule exists at 05:30 Asia/Bangkok with overlap SKIP and a catch-up window of 1 h
    And no per-product Schedule exists
    And a second start for an open business date joins the run and rwb_source_data_duplicate_start_total rises by 1

  Scenario: AC5 Flag-off behaviour follows the ACE dependency gate
    Given rwb.dataengine.freshness-stamp is off
    When a business date is started, and freshness and readiness are read
    Then no stamp, event or child workflow is created, readiness is LATE and freshness is STALE with businessDate null
    And the Load late, Load failed, stale and gate-hold alert rules are not armed
    And the health check reports the flag state and the release note names the services waiting on RWB-ACE-001

  Scenario: AC6 Alerts reach their route
    Given the flag is on and the alert rules of section 13 are configured from the values file
    When a synthetic run produces each of the seven conditions
    Then each alert is raised within 15 minutes with the message ID or none of the table, product or source and business date, its route and one runbook link
    And the stale alert carries MSG-P1-001 with productName and the business date of the stamp in use
    And the Load late alert fires with AceDataLate at 05:30

  Scenario: AC10 ACE view failure does not change stamps
    Given v_ace_batch_status is unavailable or times out
    When readBatchStatus is retried with 1 s initial interval, back-off 2 and 10 attempts
    Then no data_product_load row is written or changed
    And after the last attempt the dependency alert fires with MSG-GEN-006, the object name and the trace ID

  Scenario: AC12 Rollback uses the flag, then the previous tag
    Given a release is ready with its migration applied and a previous tag exists
    When the release owner switches the flag off and, only if that does not cover the fault, redeploys the previous tag and chart
    Then the previous pods pass the smoke test on the newer schema and no undo script runs
    And the release note names every rwb-source-data capability the redeploy reverts, and no running workflow is terminated

  Scenario: AC13 Failed migration blocks the rollout
    Given a migration fails
    When the deployment pipeline runs
    Then old pods keep serving, new pods receive no traffic and the release is marked failed

  Scenario: AC14 Readiness failure removes the pod from service
    Given the Temporal worker cannot connect during its start-up window
    When the readiness probe fails
    Then the pod receives no traffic and the probe-failure runbook entry is linked

  Scenario: AC15 Secrets and least privilege are checked
    Given the deployed chart, config maps and service login
    When secret scanning runs and the login selects a public schema table
    Then no secret literal is found and the select is refused

  Scenario: AC16 Telemetry contains no personal data
    Given a synthetic run raises every configured alert
    When logs, series labels, alert payloads and workflow inputs are inspected
    Then they contain only product codes, source codes, dates, counts, durations and trace IDs

  Scenario: AC17 Catch-up after an outage
    Given the namespace is unavailable over the 05:30 occurrence
    When it returns less than 1 h after 05:30
    Then the missed occurrence runs once
    And when it returns more than 1 h after 05:30 that occurrence is not run

  Scenario: AC18 Smoke check uses the versioned fake
    Given the 5.1.0 provider fake and the synthetic Section B fixture in DEV
    When the smoke profile posts the readiness signal twice for one business date with the same Idempotency-Key
    Then both calls answer 202 with the same body and one open AceIngestCheck run exists

  Scenario: AC19 Worker restart does not duplicate work
    Given a business-date run is open and has stamped ALS
    When a worker pod restarts
    Then the run resumes from its history, no second run starts, no second AceDataReady is written and duplicate_count is unchanged

  Scenario: AC20 Publish failure stays recoverable
    Given the outbox relay cannot deliver an AceDataReady row to Kafka
    When delivery keeps failing
    Then the row stays unpublished in outbox_event, the stamp stays and the dependency alert links the runbook
    And after Kafka recovers the row is published once, and a consumer's .dlt record is recovered with the platform replay tool

  Scenario: AC21 Rollback of the first release
    Given there is no previous tag
    When the release owner rolls back
    Then the flag is off, the worker is scaled to zero, the Schedule of the release is paused and the flagged API operations answer 404
```

AC7, AC8, AC9 and AC11 are not used: version 2 AC9 is removed and AC11 is covered by RWB-P1-E1015-APP AC26. For every criterion above, the Test Cases v9 row is listed in section 16.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Use only the rwb_source_data service login and its secret reference; the login and grants are those of RWB-P1-E1069-DB | DP-02 |
| BR2 | Run the forward-only Flyway sequence before readiness; no migration is reversed and no undo script exists; each migration works with the previous tag | DP-15; RD-P1-045 |
| BR3 | The event topic has .retry.1m, .retry.10m, .retry.1h and .dlt; a consumer never acknowledges an event it could not process | DP-09; RD-P1-003 |
| BR4 | One 05:30 Schedule; expected_by checks are durable timers, not per-product Schedules | RD-P1-040, RD-P1-041 |
| BR5 | API replicas 2 and Schedule catch-up 1 h; worker resources, KEDA and alert thresholds are values-file entries | NFR-067, NFR-068; RD-P1-028, RD-P1-040 |
| BR6 | Every alert reaches a named route within 15 minutes, links one runbook entry and carries its message ID where one is assigned | NFR-068; Template and Rules §R7.2 s14 |
| BR7 | Section B features stay off until the ACE dependency gate passes; while off, their alerts are not armed | RD-P1-043 |
| BR8 | P1 writes only rwb_source_data and reads ACE through recovery.v_ace_* | DP-01, DP-05 |
| BR9 | Logs, dashboard labels, alert payloads and runbook data contain no personal data | CTL-11; ADR-023 |
| BR10 | RWB-PLT-N002-INF provisions topics; this story verifies settings and producer ACL and creates no topic or consumer group | RD-P1-044 |
| BR11 | Roll back with the flag first. The release owner rolls back when a post-deploy check fails (smoke, view conformance, contract or replay gate), the platform smoke workflow JOB-22 reports no result for the day, or an incident is attributed to the release. A FAILED P1 run is re-run after the fix through the admin rerun (NEW-ASM-X4) | RD-P1-045 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart promoted | Image and chart digest are pinned | Deploying |
| Deploying | Migration and probes succeed | Forward migration applied and health checks pass | Ready |
| Ready | Feature flag off | ACE Section B dependency gate not passed | Ready, capability dark |
| Ready, capability dark | Feature flag on | RWB-ACE-001 landed and gate passed in the environment | Ready, capability live |
| Ready | New release | Same artefact promoted | Rolling |
| Rolling | New pods healthy | Previous pods drain; schema stays compatible | Ready |
| Deploying | Migration fails | Pipeline blocks release; old pods remain | Failed |
| Failed or Ready | Rollback | Flag off; if needed the previous tag on the newer schema; first release: worker to zero, Schedule paused | Ready on the previous release, or capability dark |
| Any | Schema fault found | A new forward migration is applied | Ready after fix |

### 10. Authority

| Who | What they may do |
|---|---|
| rwb-source-data DevOps engineer | Own chart, values, pipeline, worker registration, 05:30 Schedule, dashboards and runbook |
| Platform administrator | Own the namespace, Schedule registration rights and flags; approve environment promotion |
| RWB-PLT-N002-INF owner | Provision topics, retry topics, .dlt and ACLs |
| ACE database administrator | Own the schema, login and grants; approve the migration job |
| Release owner and ACE team lead | Pass the Section B dependency gate, switch flags on, decide a rollback |
| Data steward (RW-DATASTEW) | Receive stale and gate-hold alerts; confirm the source map and expected-by rows |
| On-call operator | Follow the runbook and raise an incident |

The service uses only the rwb_source_data secret reference; credential values are held by the platform secret store. The Airflow caller of the readiness route needs a workload identity with Platform administration U; its identifier, network route and secret are pending (NEW-GAP-S3-6).

### 11. Data

| Item | Content | Rule |
|---|---|---|
| Deployment values | Image digest, chart version, replica and resource settings, probe values, KEDA task-queue thresholds, alert thresholds, alert channel, ingest.poll.interval.minutes = 5 | API replicas 2; threshold names and values pending (NEW-GAP-S3-9) |
| Schema | rwb_source_data with the P1 freshness tables and library objects | Forward-only migration |
| ACE views | recovery.v_ace_batch_status, recovery.v_ace_holiday and the other granted views | Read only through rwb_source_data |
| Event topics | rwb.source-data.events.v1, .retry.1m, .retry.10m, .retry.1h, .dlt | Provisioned by RWB-PLT-N002-INF; verified here |
| Producer ACL | rwb-source-data principal may write the topic | Verified, not created |
| Schedule | rwb-source-data-ace-late-check, 05:30 Asia/Bangkok | Overlap SKIP, catch-up 1 h |
| Feature flags | rwb.dataengine.freshness-stamp; rwb.source-data.ingest-poll-fallback | Platform flag library; off by default |
| Operations | Readiness POST, status GET and GET /data-products/freshness | Contract version 5.1.0 |
| Test fixtures | Synthetic Section B fixture of RWB-P1-E1065-CON and the 5.1.0 provider fake | DEV and pipeline; publication pending |

### 12. Contract

#### 12.1 REST operations

The deployment exposes the version 5.1.0 routes GET /data-products/freshness, POST /business-days/{date}/ready and GET /business-days/{date}/status behind gateway-bff. The API runs two replicas. The account-page read is deployed by RWB-P1-E1002-OPS once its path exists (NEW-GAP-B3). Probes are cluster-internal and not API routes.

#### 12.2 Consumed calls

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | /api/recovery/access/v1/authorise | rwb-access | Read authorisation; path not yet published (NEW-GAP-S3-15) |

Reference changes arrive through the apply handler of RWB-P3-E1043-CON; the release adds no run-time reference call.

#### 12.3 Events published and platform-owned topics

P1 publishes AceDataReady and AceDataLate to rwb.source-data.events.v1 through its transactional outbox, key {sourceSystem}:{businessDate}, ce_subject = sourceSystem, data {sourceSystem, businessDate, status, completedAt}; the status value when no batch row exists is pending (NEW-GAP-S3-2). RWB-PLT-N002-INF provisions the topic (12 partitions, replication factor 3, 7-day retention), .retry.1m, .retry.10m, .retry.1h and .dlt. This story verifies them and creates no topic or consumer group.

#### 12.4 Events consumed

None from rwb.source-data.events.v1. Each consuming service's OPS story declares its own consumer group. Ledger-intake groups are declared by RWB-P1-E1066-OPS.

#### 12.5 Worker and workflow registration

| Name | Type | Deployment element |
|---|---|---|
| AceIngestCheck | Workflow, one run per businessDate | Worker on task queue rwb-source-data, ID ace-ingest-check-{businessDate}, Worker Versioning |
| readBatchStatus, stampProducts, markStale, checkDailyCompleteness | Activities | Same worker |
| rwb-source-data-ace-late-check | Schedule | One, at 05:30 Asia/Bangkok |
| Product expected_by checks | Durable timers | Inside AceIngestCheck |

No publishAceDataReady or publishAceDataLate activity is deployed; the outbox relay of the platform library publishes the rows. ReconciliationWorkflow is registered by RWB-P1-E1011-OPS and Stage2ProductWorkflow by RWB-P1-E2010-OPS.

#### 12.6 Registration and values

The chart registers the 05:30 Schedule (catch-up window 1 h) and reads ingest.poll.interval.minutes = 5, KEDA thresholds, alert thresholds and the alert channel from the values file. The fallback poll flag is off whenever Airflow is live; until NEW-GAP-C1 is closed it stays off outside DEV.

#### 12.7 Deployed data objects

| Object | Owner | Deployment element |
|---|---|---|
| data_product, data_product_source, data_product_load | P1 | Existing P1 migration sequence |
| outbox_event | Platform library in rwb_source_data | Same migration job |
| decision_log_entry | P7 | Not created or granted here |
| recovery.v_ace_* | ACE | Read-only grant |

#### 12.8 Fakes

Provider fake fakes/rwb-source-data/5.1.0/ (working value, NEW-ASM-A1) and the rwb-access and reference-load apply fakes run in the pipeline and the DEV smoke profile; publication is pending. No fake is deployed to UAT or PROD.

#### 12.9 Call-type summary

| Call type | Deployment |
|---|---|
| REST | Freshness and readiness routes; rwb-access authorise |
| Kafka | Two P1 events through the outbox; no own-topic consumer |
| Temporal | One workflow, four activities, one 05:30 Schedule and durable timers |
| File | None |

### 13. Solution plan

**Deployment artefacts.** The rwb-source-data Helm chart: two-replica API Deployment, worker Deployment, service, forward-only migration job, config map, probes, secret references, KEDA scaler and Schedule registration hook. Values files for DEV, SIT, UAT and PROD pin the same image digest across promotion.

**Probes.** Readiness answers healthy only when the migration is at the expected schema version, the outbox relay is running and the Temporal worker has polled; liveness answers healthy when the process is up and its internal loop responds. Neither probe writes to the database. Paths and timings are values.

**Migration job.** The per-service Flyway sequence for schema rwb_source_data, run before the rollout with a backoff limit; a failed job blocks the release.

**Provisioning ownership.** RWB-PLT-N002-INF creates the topics, retry topics, .dlt and ACLs; this story verifies them.

**Workflow deployment.** Register AceIngestCheck and the 05:30 Schedule; expected_by checks are durable timers. DEF-020: JOB-01 and JOB-09 are retired and AceIngestCheck is the one business-date freshness workflow.

**Alert rules** (armed only while the flag is on)

| Alert | Condition | Message ID | Route | Runbook entry |
|---|---|---|---|---|
| Load late | AceDataLate at 05:30 for a source and business date | None assigned (NEW-GAP-S3-4) | Pending (NEW-GAP-S3-4) | Source late |
| Load failed | A source reads FAILED | None assigned (NEW-GAP-S3-4) | Pending (NEW-GAP-S3-4) | Batch failed |
| Stale product | A stamp turns STALE | MSG-P1-001 with productName and stamp business date | Data steward queue, ticket | Product stale |
| Gate hold | DailyCompletenessGate returns HOLD | MSG-P1-001 with product and date | Data steward queue, ticket | Gate hold |
| Duplicate restatement | duplicate_count above its threshold for a product and business date | None | Platform on-call, ticket | Restated batch |
| Long stale | A product stays STALE past the threshold with no later LOADED row | None | Data steward and platform on-call, page | Long stale |
| Dependency | Store or ACE view unavailable, outbox not delivering or task queue not draining | MSG-GEN-006 with object and trace ID | Platform on-call, page | Dependency down |

Alert payloads carry product or source codes and business dates. The alert channel is the values-file entry rwb.dataengine.freshness.alert-channel. Alerts are delivered within 15 minutes (NFR-068).

**Dashboards.** Freshness: stamps written, stale products and stale duration, duplicate count, event lag. Gate and workflow: gate results, task-queue backlog, Schedule fires and skips, duplicate starts, workflow failures, flag state and ACE dependency gate status.

**Runbook entries.** Source late, batch failed, product stale, gate hold, restated batch, long stale, dependency down, migration failure, probe failure, flag left off. Each gives the check, the owner role and the recovery step.

**Capacity.** One AceIngestCheck run per business date; replica counts, resources, KEDA thresholds and maximum concurrent activities are values entries.

**Rollback** (RD-P1-045). Flag off first. Only if the flag does not cover the fault, redeploy the previous image tag and chart against the newer schema; Schedules return to the previous definition and a Schedule added by the faulty release is paused. Kafka offsets are not reset and no workflow is terminated. Never run an undo script; repair the schema with a new forward migration. First release: flag off, worker scaled to zero, Schedule paused, flagged operations answer 404.

**Done when.** Deployments, probes, topic verification, Schedule registration, alert rules, smoke profile and runbook satisfy section 7; delivery items are in section 20.

### 14. Validation and messages

| ID | Condition | Message |
|---|---|---|
| MSG-P1-001 | A product is STALE or the gate returns HOLD | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-006 | Store, view or dependency unavailable | {system} is not available. Try again in a few minutes. |
| MSG-GEN-001 | Malformed date or required value missing on a read | Enter {field}. |
| MSG-GEN-007 | product value outside its list | {value} is not a valid value for {field}. Choose a value from the list. |
| MSG-P4-001 | No valid session or no Workbench role (401) | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | Caller lacks the right (403) | You cannot {action} here. Your role does not include it. |

Texts are those of Error and Message Standard v6. No message ID is assigned to the Load late and Load failed alerts (NEW-GAP-S3-4).

### 15. Screens and states

Operations uses the pipeline release view, the two dashboards of section 13, the alert routes and the runbook. The deployment does not define the SCR-03 panel fields or its states; they are in RWB-P1-E1015-APP section 15. The release dashboard reports the Section B flag state and the ACE dependency gate status.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P1-E1015-OPS-16 | AC1 | NFR | Chart deploys in each environment |
| TC-P1-E1015-OPS-17 | AC2 | NFR | Worker scales on the Temporal task queue |
| TC-P1-E1015-OPS-01 | AC3 | NFR | Platform topics and ACLs are verified |
| TC-P1-E1015-OPS-18 | AC4 | NFR | One Schedule and durable timers |
| TC-P1-E1015-OPS-19 | AC5 | NFR | Flag-off behaviour follows the ACE dependency gate |
| TC-P1-E1015-OPS-20 | AC6 | NFR | Alerts reach their route |
| TC-P1-E1015-OPS-02 | §12 operations, events and activities | Contract | §12 operations, events and activities |
| TC-P1-E1015-OPS-03 | §12.7 tables | Boundary | §12.7 tables |
| TC-P1-E1015-OPS-04 | BR1 | NFR | As the covered item |
| TC-P1-E1015-OPS-05 | BR2 | NFR | As the covered item |
| TC-P1-E1015-OPS-06 | BR3 | NFR | As the covered item |
| TC-P1-E1015-OPS-07 | BR4 | NFR | As the covered item |
| TC-P1-E1015-OPS-08 | BR5 | NFR | As the covered item |
| TC-P1-E1015-OPS-09 | BR6 | NFR | As the covered item |
| TC-P1-E1015-OPS-10 | BR7 | NFR | As the covered item |
| TC-P1-E1015-OPS-11 | BR8 | NFR | As the covered item |
| TC-P1-E1015-OPS-12 | BR9 | NFR | As the covered item |
| TC-P1-E1015-OPS-14 | AC10 | NFR | ACE view failure does not change stamps |
| TC-P1-E1015-OPS-24 | AC12 | Component | Rollback uses the flag, then the previous tag |
| TC-P1-E1015-OPS-25 | AC13 | Component | Failed migration blocks the rollout |
| TC-P1-E1015-OPS-26 | AC14 | Component | Readiness failure removes the pod from service |
| TC-P1-E1015-OPS-27 | AC15 | Component | Secrets and least privilege are checked |
| TC-P1-E1015-OPS-28 | AC16 | Component | Telemetry contains no personal data |
| TC-P1-E1015-OPS-29 | AC17 | Component | Catch-up after an outage |
| TC-P1-E1015-OPS-30 | AC18 | Component | Smoke check uses the versioned fake |
| TC-P1-E1015-OPS-31 | AC19 | Component | Worker restart does not duplicate work |
| TC-P1-E1015-OPS-32 | AC20 | Component | Publish failure stays recoverable |
| TC-P1-E1015-OPS-33 | AC21 | Component | Rollback of the first release |

The version 2 rows that reused the application test case IDs TC-E1-015-01 to -08 for infrastructure checks are removed; those IDs do not belong to this story.

### 17. Guardrails

- Only the rwb_source_data secret reference is deployed; no secret literal is stored in values or chart templates.
- Migrations are forward-only; rollback switches the flag off first and redeploys the previous tag on the newer schema only if the flag does not cover the fault.
- RWB-PLT-N002-INF provisions event topics and ACLs; E1015-OPS verifies them and does not create them.
- No consumer group is declared on rwb.source-data.events.v1 for rwb-source-data.
- KEDA scales on Temporal task-queue backlog, not Kafka consumer lag.
- One 05:30 Schedule is registered; product expected_by checks use durable workflow timers.
- With Section B flag off, no stamp, event or child workflow is produced and no freshness value is guessed.
- Telemetry contains no personal data.

### 18. Traceability

| Requirement | Deployment element | Test |
|---|---|---|
| REQ-RDF-009 | Worker, Schedule, stamp series and alerts | TC-P1-E1015-OPS-16, TC-P1-E1015-OPS-18, TC-P1-E1015-OPS-20 |
| BR-P1-014-4 | Gate-hold alert and runbook entry | TC-P1-E1015-OPS-20 |
| NFR-014 | Two-replica API deployment and freshness routes | TC-P1-E1015-OPS-16 |
| NFR-067 | Schedule, monitors, alerts and runbook | TC-P1-E1015-OPS-18, TC-P1-E1015-OPS-20 |
| NFR-068 | Named route and 15-minute target | TC-P1-E1015-OPS-20 |
| RD-P1-040, RD-P1-043 | One workflow and Schedule; flag-off behaviour | TC-P1-E1015-OPS-18, TC-P1-E1015-OPS-19 |
| RD-P1-044, RD-P1-045 | Shared chart, topic ownership, forward-only rollback | TC-P1-E1015-OPS-01, TC-P1-E1015-OPS-24, TC-P1-E1015-OPS-25 |

### 19. Out of scope

- P1 application code, freshness rows, gate behavior and API or event schemas (RWB-P1-E1015-APP and RWB-P1-E1015-CON).
- Platform topic creation, retry topics, .dlt and platform ACL implementation (RWB-PLT-N002-INF).
- ACE view definitions and source ingestion (RWB-ACE-001 and RWB-P1-E1069-APP).
- Decision snapshots and case-list ownership (rwb-decision and rwb-case).

### 20. Remaining delivery steps

- Set story size at refinement; owner: squad.
- Record epic design sign-off; owner: solution architect.
- Complete and baseline RWB-P1-E1015-CON 5.1.0 and publish its provider fake; owner: rwb-source-data tech lead.
- Create and publish synthetic Section B data in DEV; owner: data engineering and QA.
- Add OPS test case rows in Test Cases v9; owner: QA lead.
- Pass the RWB-ACE-001 dependency gate before switching the feature on in SIT, UAT or PROD; owner: release owner and ACE team lead.
- Set the Control-M fallback poll start time (NEW-GAP-C1); owner: bank platform team with solution architect.
- Name and set the alert and KEDA threshold values for each environment (NEW-GAP-S3-9); owner: platform administrator and service owner.
- Assign Load late and Load failed message IDs and routes and the repeat rule of the stale alert (NEW-GAP-S3-4); owner: solution architect with the data steward and the Error and Message Standard owner.
- Give the Airflow caller identity, route, secret and grant (NEW-GAP-S3-6); owner: solution architect with the security owner.
- Publish the authorise path in rwb-access.yaml (NEW-GAP-S3-15); owner: rwb-access service owner.
- AceDataLate status when no batch row exists (NEW-GAP-S3-2); owner: solution architect.
- Confirm the data_product_source seed against the ACE code list (NEW-ASM-B3) and that every source-fed product has refresh_cycle and expected_by rows before the flag is switched on; owner: ACE team lead and data owner.
- Approve production promotion; owner: release owner.

