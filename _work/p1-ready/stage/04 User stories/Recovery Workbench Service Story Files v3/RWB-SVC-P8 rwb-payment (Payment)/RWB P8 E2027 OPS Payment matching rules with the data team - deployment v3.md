# RWB-P8-E2027-OPS Payment matching rules with the data team - deployment

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- RD-P1-066: Apply the shared topic groups and the JOB-08 ownership amendment.
- The matching run starts only on `AceDataReady` with `sourceSystem` ALS and `status` COMPLETED; events for other source systems start nothing (RD-P1-003, RD-P1-040).

| Item | Value |
|---|---|
| Story key | RWB-P8-E2027-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-payment |
| Service epic | RWB-SVC-P8 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-027 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P8-E |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P8-E2027-OPS-16) |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P8 rwb-payment v1.md (FR-P8-001, FR-P8-002, FR-P8-004, FR-P8-006, FR-P8-007, FR-P8-010, FR-P8-011, FR-P8-012, FR-P8-013, FR-P8-015, FR-P8-016, FR-P8-017, FR-P8-027, FR-P8-028, FR-P8-032) |
| Readiness decisions | RD-P1-003, RD-P1-040, RD-P1-066 |
| FSD trace | FEAT-PAY-01 to FEAT-PAY-11; acceptance criteria AC-P8-xxx, AC-ALT-P8-xxx, AC-EXC-P8-xxx (FSD P8 v3 has no REQ ID; see GAP-1624) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (27 resolved, 37 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **platform engineer**, I want **rwb-payment deployed for the payment-matching key with a `RulePackageInForce` consumer group on `rwb.decision.events.v1` that refreshes the evaluated copy of PAYMENT_MATCH and falls back to the version in force — never to a default match — a provisioned `rwb.payment.events.v1` with its `.retry` and `.dlt` topics and their ACLs, the consumer groups of the six consumed events, a Temporal worker pool on task queue `rwb-payment` that registers the JOB-07 workflow and its activities and no Schedule, a Flyway migration job that touches `rwb_payment` only, secrets taken from the key store by reference, four alerts on outbox lag, dead-letter depth, workflow failures and rule-cache staleness, a canary gate and a rehearsed rollback**, so that **an operator can see whether the matching run is deciding on the approved version, catch a stuck run or a lost event before a payment is affected, and return to the previous version or the previous release without a code change**.

This story deploys and operates the capability of RWB-P8-E2027-APP. It writes no business code, no rule row, no threshold and no event schema; it fixes how the service is provisioned, observed, gated and rolled back.

### 2. Business rationale

A rule package is data and a matching run is a workflow, so almost nothing that can go wrong in this key looks like "the service is down". The evaluated copy can be a version behind, a `RulePackageInForce` event can be lost, a run can sit on a retry, an event can pile up in the `.dlt` topic, or the outbox relay can fall behind while every probe answers healthy. In the monolith the matching rules were a table read in process and the run was a Quartz trigger on a shared job table; a stale table and a stuck job were the same class of incident and the same person looked at them. In the target the model is fetched from another service, the run is a workflow on another platform and the events cross a broker, so each of those failures has its own signal and its own recovery path.

Deployment is therefore part of the capability. The rule-cache refresh is an operational behaviour, not a library detail: the event must arrive, the model must be verified, and when it cannot be, the service must keep the version in force and say so — because the alternative, a default match or an empty cache, silently breaks BR9 and every decision taken under it. The topics need their retry and dead-letter paths and their ACLs, because a mis-scoped ACL and a missing `.dlt` topic both look like "the consumer is quiet". The worker pool needs its own build ID and its own visibility, because JOB-07 is started by `AceDataReady` (EV-26) and a worker that is not polling is invisible until the morning cut-off. The migration job must be pinned to `rwb_payment`, because the registry tables are rwb-decision's and a migration that touches them would cross the boundary DP-01 draws.

The values that operators need are not specified by any source: the alert thresholds, the cache-staleness window, the outbox-lag and dead-letter limits, the worker pool size, the canary percentage and the probe timings (DL11 covers the non-functional target values; its recommended resolution is accepted, see section 18, and the sources give no number for these values). This story therefore fixes their names and the rule that they are values of the chart, and carries the numbers as placeholders (GAP-2508; ASM-4156).

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The Kafka event platform provisions a topic with a `.retry` topic and a `.dlt` topic and applies topic ACLs (RWB-PLT-EVT, RWB-PLT-TE006-CON, RWB-PLT-N002-INF).
- The Temporal workflow kit and the `rwb-recovery` namespace are available (RWB-PLT-WF, RWB-PLT-E1071-CON), because the matching run is an event-started workflow on task queue `rwb-payment` (DP-10).
- The per-service Flyway sequence and the migration conventions are in force (RWB-PLT-E1044-CON), and the `rwb_payment` schema and login exist with their grants (RWB-PLT-DB).
- rwb-decision publishes `rwb.decision.RulePackageInForce.v1` on `rwb.decision.events.v1` (EV-30) and owns the 00:01 promotion (JOB-20; Arch v5 slide 44).
- The platform secret store, the workload identity and the mTLS material are available; their names are Not specified in the source documents (GAP-2508; ASM-4157) and the chart references them by role only.
- The registry answers the version list and the model fetch (RWB-P7-E2027-APP, RWB-P7-E1073-CON), and the model carries its SHA-256.
- The message catalogue and the platform error envelope are in force, so an alert can carry a message ID where a message exists.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The pipeline builds the service image from the template, runs the unit, component and contract tests of the app story, scans the image and the dependencies, publishes the chart, and promotes the same image digest and chart version through DEV, SIT and UAT without a rebuild.
2. The chart deploys the service with its own login, its migration job, its probes, the consumer configuration and the values of section 11: the rule-cache bound and warm-up list, the worker pool size, the consumer concurrency, the outbox-lag and dead-letter limits, the canary percentage and the alert windows.
3. The provisioning step creates `rwb.payment.events.v1` with its `.retry` and `.dlt` topics and the producer ACL for this service, and the consumer groups of the six consumed events with their own `.retry` and `.dlt` paths.
4. The migration job runs the per-service Flyway sequence against `rwb_payment` only, and the deployment is not marked ready before it succeeds.
5. The worker pool registers task queue `rwb-payment` in namespace `rwb-recovery` with the JOB-07 workflow and the `matchPayments`, `confirmBookings` and `postProceeds` activities under the build ID of the release; no Schedule is registered.
6. The warm-up step asks the registry for the version in force of PAYMENT_MATCH, fetches the model, verifies its checksum and loads it, so the first business date of the morning does not pay the fetch.
7. The read-only smoke step publishes a synthetic `AceDataReady` with `sourceSystem` ALS and `status` COMPLETED for a test business date, asserts that the run starts on `rwb-payment`, that a synthetic match writes one record and one `proceeds` row in the test schema, and that one synthetic `RulePackageInForce` swaps the model.
8. The dashboards are published: version in force and its load time, run outcomes, retry and dead-letter depth, outbox lag, workflow failures and rule-cache staleness.
9. The four alerts and the canary gate are wired to the runbook entries; the canary gate holds the promotion until the canary slice is green.
10. The rollback path is rehearsed: a release rollback by chart version, and a rule rollback by the one call in rwb-decision followed by the swap on the event, with no release of this service.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A `RulePackageInForce` event fails the fetch or the checksum | The refresh handler retries on the kit policy; after the last attempt the event goes to the `.retry` topic and then to the `.dlt` with an alert, and the version in force stays loaded | None | AC1, AC2 |
| X2 | No model can be loaded at start-up | Readiness reports the rule cache as not warm; the "rule-cache stale" alert fires after the warm-up window; no match is taken and no default version is substituted | MSG-P3-027 | AC1, AC5 |
| X3 | A topic ACL is missing or too narrow | The consumer or the producer fails to start or to write, the dead-letter depth stays at zero and the run does not appear; the provisioning test fails and the release is blocked | None | AC2 |
| X4 | The worker pool is not polling, or the workflow build ID has no compatible worker | No run starts from `AceDataReady`; the "workflow failures" and "no run started" signals fire; the previous build stays serving | None | AC3, AC5 |
| X5 | The migration job targets another schema or a registry table | The migration test fails on the schema assertion and the release is blocked; the schema of rwb-decision is never touched | None | AC4 |
| X6 | A secret is read from a values file or an environment literal instead of the key store | The pipeline secret scan fails the build and the release is blocked | None | AC5 |
| X7 | The outbox relay falls behind | The outbox-lag alert fires with the age of the oldest unsent event; events are not lost and the relay catches up | None | AC5 |
| X8 | The canary slice is red | The promotion stops and the previous chart version stays in service; a rollback of the release is one command | None | AC6 |
| X9 | A run is stuck on a retry | The workflow-failure alert names the workflow ID and the activity; the run is retried on the kit policy and then left for the runbook entry | MSG-P8-001 | AC3, AC5 |

No alert of this story raises a business message except the ones that carry MSG-P3-027 and MSG-P8-001, whose texts are the app story's.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the platform topic provisioning, the workflow kit, the secret store and the pipeline; builds no business code |
| Negotiable | The alert thresholds, the cache bound, the pool sizes, the resource sizes, the canary percentage and the probe timings are environment values, not story decisions |
| Valuable | Makes the version in force, the runs, the retry paths, the outbox and the secret hygiene visible and operable, and makes a rollback a command rather than a release |
| Estimable | One chart with its values, one provisioning step, one migration job, one worker pool, four alerts, four runbook entries, one canary gate and one rollback |
| Small | Fits one sprint with the runbook |
| Testable | Every criterion tests an artefact: a rendered chart, a provisioned topic, a registered queue, a migration result, a secret reference, a synthetic metric and a gate result |

### 7. Acceptance criteria

```gherkin
Feature: Deployment and operations of the payment matching rules in rwb-payment

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the target environment is SIT
    Given the package code is PAYMENT_MATCH and the version in force is "PM-2026.12" from 2026-12-01

  Scenario: AC1 The rule cache refreshes on RulePackageInForce and falls back to the version in force (new, D-RCV-60)
    Given a running rwb-payment pod with version "PM-2026.12" of PAYMENT_MATCH loaded and verified
    When rwb.decision.RulePackageInForce.v1 arrives for a newer version with its checksum
    Then the service fetches the model of that version, verifies the checksum and swaps it in one step, so a run sees either the old or the new version and never a half-loaded one
    When a later event names a version whose model fails its checksum
    Then no swap happens, the version in force stays loaded, the mismatch is counted with the package code, the version label and both checksums
    When the registry answers NoPackageInForce for a business date
    Then the run stops with MSG-P3-027 and no match is taken, and no default version and no empty model is ever substituted
    Then the warm-up list and the cache bound of 20 come from the values files and are never hard-coded

  Scenario: AC2 The topic, its retry and dead-letter topics and the ACLs are provisioned (new, D-RCV-60)
    Given the provisioning step for rwb-payment
    When it runs against the environment
    Then rwb.payment.events.v1 exists with its .retry topic and its .dlt topic
    Then the producer ACL permits this service to write the topic, its retry topic and its dead-letter topic, and permits no other service to write them
    Then the consumer groups of AceDataReady, TreatmentApproved, RulePackageInForce, DecisionRecorded, LotAwarded and AssetSold exist with their retry and dead-letter paths
    Then a failed swap or a failed activity reaches the retry topic and then the .dlt topic, and the message is never acknowledged as processed
    Then the consumer dedupes through the inbox, so a repeated event starts no second run and no second swap
    Then the provisioning test fails the release when a topic, a retry path, a dead-letter path or an ACL is missing

  Scenario: AC3 The Temporal worker pool registers the payment matching workflow and no Schedule (new, D-RCV-60)
    Given the deployment of this release
    When the worker pool starts on namespace rwb-recovery
    Then task queue rwb-payment is registered with the payment matching workflow and the matchPayments, confirmBookings and postProceeds activities under the build ID of the release
    Then a synthetic AceDataReady with sourceSystem ALS and status COMPLETED starts one run of the payment matching workflow on the queue
    Then the worker pool size and the maximum concurrent activities come from the values files
    Then no Schedule is registered, and the 00:01 rule promote Schedule remains rwb-decision's and is not retimed, duplicated or disabled here
    Then a worker that is not polling is visible as a workflow-failure and no-run signal and does not silently drop the business date

  Scenario: AC4 The migration job touches rwb_payment only (new, D-RCV-60)
    Given the migration job of the chart
    When it runs against the environment
    Then it applies the per-service Flyway sequence of this release to schema rwb_payment and to no other schema
    Then it creates or updates proceeds, decision_record, outbox_event, processed_event and idempotency_key, and creates no registry table and no payment_match_rule
    Then the deployment is not marked ready before the migration reports success
    Then the schema assertion test fails the release when the job names another schema, another service's login or a registry table

  Scenario: AC5 Every secret and identity is a reference to the key store (new, D-RCV-60)
    Given the rendered chart and the running workload
    When the configuration is inspected
    Then the rwb-payment login, the Kafka client credential, the Temporal mTLS material, the registry certificate and the key-store reference are mounted from the platform secret store and appear in no values file, no config map and no image layer
    Then the workload runs under its own identity and holds no other service's credential
    Then the pipeline secret scan fails the build on a secret in code, a values file, a test or a log
    Then a rotation of a secret is picked up without a rebuild of the image

  Scenario: AC6 Four alerts, the canary gate and the rollback are in place (new, D-RCV-60)
    Given the published alerts, the canary gate and the runbook
    When the four conditions are replayed with synthetic metrics
    Then an outbox lag above its value raises its alert with the age of the oldest unsent event
    Then a dead-letter depth above its value raises its alert with the topic, the consumer group and the event type
    Then a workflow failure or a run that did not start for the business date raises its alert with the workflow ID and the activity
    Then a rule cache that is not warm or is a version behind raises its alert with the package code and the version in force
    Then each alert links exactly one runbook entry with the check, the owner role and the recovery step
    Then the canary gate holds the promotion until the canary slice is green, and a red slice stops it
    Then the release rollback returns the previous chart version and the rule rollback is one call in rwb-decision followed by the swap on the event, with no release of this service

  Scenario: AC7 Every business rule of section 8 has a criterion and a test (new, D-RCV-60)
    Given the business rules table of section 8 and the test cases of section 16
    When the traceability check runs
    Then every rule BR1 to BR12 names at least one criterion of section 7 and one test case of section 16 in its Covered by cell
    Then a rule with no criterion or no test fails the release, and an architecture constraint may be proved by a guardrail or boundary test instead

  Scenario: AC8 A consumed call that fails or does not answer is retried, parked and alerted (new, D-RCV-60)
    Given a running rwb-payment pod with its consumed services reachable
    When a consumed call fails or does not answer (timeout value: Not specified in the source documents (NEWAC-RWB-P8-E2027-OPS-AC12))
    Then the call is retried on the kit policy and the event is never acknowledged as processed
    Then the event reaches the retry topic and then the .dlt topic, and no outbox event is written for it
    Then the dead-letter depth alert fires with the topic, the consumer group and the event type

  Scenario: AC9 A status change the model does not allow is refused (new, D-RCV-60)
    Given a running rwb-payment pod with the status model of this release loaded
    When a status change the model does not allow is received
    Then the change is refused
    Then no outbox event is written and the event is never acknowledged as processed
```

The nine criteria are new under D-RCV-60 and they test deployment and operations only: no legacy criterion of RWB-E2-027 is restated, no business rule is re-evaluated, and every business assertion they touch — the version in force and the stopped run — is the app story's and is named, not proved, here.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The evaluated copy of PAYMENT_MATCH is refreshed on `RulePackageInForce`: fetch, verify the checksum, swap atomically; on any failure the version in force stays loaded | DP-04; Temporal and Drools slide 15 notes; ADR-017 | AC1; TC-P8-E2027-OPS-01 |
| BR2 | No version in force is a stopped run with MSG-P3-027; no default version, no empty model and no last-known-anything is substituted | legacy BR9; D-RCV-36 T3; R-UNI-41 | AC1; TC-P8-E2027-OPS-01 |
| BR3 | Every topic has a `.retry` topic and a `.dlt` topic, and a consumer never acknowledges an event it could not process | DP-09 as the platform pattern; Arch v5 slide 22 notes; RWB-PLT-TE006-CON | AC2; TC-P8-E2027-OPS-02 |
| BR4 | JOB-07 is event-started on `rwb-payment` and JOB-08 on `rwb-integration`; this release registers no Schedule and never touches JOB-20 | DP-10; Arch v5 slide 44 | AC3; TC-P8-E2027-OPS-03 |
| BR5 | The migration job writes schema `rwb_payment` only, and creates no registry table and no retired table | DP-01, DP-15; D-RCV-36 T10 | AC4; TC-P8-E2027-OPS-04 |
| BR6 | Readiness answers healthy only when the migration is at the expected schema version, the worker polls, the outbox relay is up and the version in force of PAYMENT_MATCH is loaded and verified | Arch v5 slide 27; Temporal and Drools slide 28 | AC1, AC3; TC-P8-E2027-OPS-01, TC-P8-E2027-OPS-03 |
| BR7 | Every secret and identity is a reference to the platform secret store; no secret is written into a values file, a chart template, a dashboard or a runbook | NFR-052; DP-02 | AC5; TC-P8-E2027-OPS-05 |
| BR8 | Every alert carries the package code, the version label, the topic, the consumer group or the workflow ID it needs, and links exactly one runbook entry with the owner role | Template and Rules §R7.2 s14 | AC6; TC-P8-E2027-OPS-06 |
| BR9 | A rule rollback is one call in rwb-decision and the swap back happens on the event; the service is never redeployed to change a rule | Arch v5 slide 27; Temporal and Drools slide 15 | AC6; TC-P8-E2027-OPS-06 |
| BR10 | One image digest and one chart version are promoted through the environments without a rebuild, and the canary gate holds the promotion until its slice is green | Template and Rules §R5.7 rule 6; RWB-PLT-N004-OPS | AC6; TC-P8-E2027-OPS-06 |
| BR11 | Nothing on a dashboard, an alert or a runbook carries a case fact or a personal datum | Template and Rules §R7.2 s17 | AC6; TC-P8-E2027-OPS-09 |
| BR12 | The alert thresholds, the cache-staleness window, the outbox-lag and dead-letter limits, the pool sizes, the canary percentage and the probe timings are values of the chart and never constants of a template or of code | GAP-2508; ASM-4156 | AC6; TC-P8-E2027-OPS-06, TC-P8-E2027-OPS-09 |

### 9. State transitions

The deployment, and not a payment, moves through these states.

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart, the tests and the scans pass | Deploying |
| Deploying | Migration complete and probes healthy | The schema is at the expected version and both probes answer | Ready |
| Ready | Warm-up complete | The version in force of PAYMENT_MATCH is loaded and verified | Warm |
| Warm | `RulePackageInForce` arrives | The checksum verifies and the swap succeeds | Warm (new version) |
| Warm | Checksum mismatch or fetch failure | The version in force stays and the alert fires | Warm (unchanged; alerting) |
| Warm | Rollback called in rwb-decision | The earlier version is announced and swapped back | Warm (earlier version) |
| Warm | Release superseded | The canary slice is green and the promotion proceeds | Rolling |
| Rolling | All pods on the new version | The old ReplicaSet drains and each pod is Warm | Warm |
| Any | A red canary slice or a failed gate | The promotion stops and the previous chart version stays in service | Previous release in service |

No state of this table is a `proceeds` row state; the row states MATCHED and UNMATCHED are the app story's.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the provisioning step, the migration job, the worker pool, the dashboards, the alerts and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the topic provisioning, the ACLs and the consumer group rights |
| ACE database administrator | Owns the `rwb_payment` schema, the login and its grants, and approves the migration job |
| Release manager | Approves the promotion of one artefact through the environments and holds the canary gate |
| RW-COE, center of excellence analyst | Owns the rule content and the runbook entry for a version not in force |
| RW-RISK, risk and model risk officer | Calls the rollback in rwb-decision, which is one call |
| On-call operator | Runs the runbook entries and opens an incident when an alert persists |
| Identity and access team | Owns the key-store references, the rotation of the secrets and the workload identity |

Separation of duty stays where it is: the person who promotes a release is not the person who approves a rule version, and a rule rollback is RW-RISK's call in rwb-decision. No person is named anywhere; the actors are roles and service identities.

### 11. Data

| Item | Content |
|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, feature switches, the rule-cache bound and warm-up list, the warm-up timeout, the worker pool size, the consumer concurrency, the outbox-lag limit, the dead-letter depth limit, the alert windows and the canary percentage |
| Schema | `rwb_payment`, migrated by the per-service Flyway sequence; `proceeds` and the four library objects; no registry table and no `payment_match_rule` |
| Topics provisioned | `rwb.payment.events.v1` with its `.retry` and `.dlt` topics and the producer ACL; the consumer groups of the six consumed events with their own retry and dead-letter paths |
| Queue | Temporal task queue `rwb-payment` in namespace `rwb-recovery`, with the JOB-07 workflow and three activities |
| Dashboard series | Version in force and its load time, run outcomes per business date, retry and dead-letter depth, outbox lag, workflow failures, rule-cache staleness, swap duration |
| Alerts | Outbox lag, dead-letter depth, workflow failure or no run, rule-cache stale |
| Runbook entries | Rule-cache refresh and fallback, dead-letter replay, stuck or missing run, release and rule rollback |
| Secrets | The rwb-payment login, the Kafka client credential, the Temporal mTLS material and the registry certificate, all as references to the platform secret store |

The numeric values of the alert thresholds, the cache-staleness window, the outbox-lag and dead-letter limits, the pool sizes, the canary percentage and the probe timings are Not specified in the source documents (GAP-2508; ASM-4156); the chart exposes them as values and this story fixes only their names and the rule that they are never hard-coded. The names of the secrets and of the identity are Not specified in the source documents (GAP-2508; ASM-4157) and are referenced by role only.

The eight rows of the table above are deployment and platform items. Their BR Field IDs are Not specified in the source documents (DOR-RWB-P8-E2027-OPS-7). `decision_record` is a PLT library table created in `rwb_payment`, one of the library objects of the Schema row.

The PAYMENT_MATCH rows live only in the rule package, and no service schema holds a match rule table. The package tries its rows in the order EXACT, then PARTIAL, then WINDOW, and its scenario set tests that one order. This story holds version PM-2026.12, in force from 2026-12-01. RWB-E2-042 records PMT-2026.12, valid from 2026-12-15, for the same package. The two are reconciled into one label and one valid-from date before the package is promoted in SIT, so that the registry holds one row per package version.

### 12. Contract

Contract version built against: v1, the `/v1` paths and the `.v1` event types and topics of this section.

#### 12.1 REST operations provided

None provided by this story. The deployment exposes the two operations of the service through gateway-bff, and they are declared in RWB-P8-E2027-CON. The readiness and liveness probes are cluster-internal and are not part of the API surface.

#### 12.2 REST operations consumed

| Method | Path | Owner | Deployment need |
|---|---|---|---|
| GET | `/api/recovery/decision/v1/admin/rule-packages/PAYMENT_MATCH/versions` | P7 rwb-decision | The warm-up and the refresh resolve the version in force and its checksum; one hop, 2 s client budget (DP-11) |
| GET | `/api/recovery/decision/v1/rule-models/{packageCode}/{version}` | P7 rwb-decision | The model fetch of the warm-up and of the swap, verified by its checksum |

The two rows are the only calls the deployment path makes; the business calls of the app story are not repeated here.

#### 12.3 Events published

None. This story publishes no event of its own; the topics and their ACLs are provisioned so that RWB-P8-E2027-APP can publish `TreatmentBooked`, `PaymentMissed`, `ProceedsMatched` and the local record.

#### 12.4 Events consumed

| Event | Topic | Provisioning | Consuming service |
|---|---|---|---|
| `AceDataReady` (EV-26) | `rwb.source-data.events.v1` | Consumer group with inbox, `.retry` and `.dlt`; on `sourceSystem` ALS and `status` COMPLETED only, starts the JOB-07 run | rwb-payment |
| `rwb.treatment.TreatmentApproved.v1` (EV-10) | `rwb.treatment.events.v1` | Consumer group with its retry and dead-letter paths | rwb-payment |
| `rwb.decision.RulePackageInForce.v1` (EV-30) | `rwb.decision.events.v1` | Consumer group with its retry and dead-letter paths; one swap per package code and version label | rwb-payment |
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` (shared) | Read-only consumer group for the ledger acknowledgement of a local record | rwb-payment |
| `rwb.debtsale.LotAwarded.v1` (EV-23) | `rwb.debtsale.events.v1` | Consumer group with its retry and dead-letter paths | rwb-payment |
| `rwb.asset.AssetSold.v1` | `rwb.asset.events.v1` | Consumer group with its retry and dead-letter paths | rwb-payment |

Each consumer group is the service-wide group of its topic, named `rwb-payment.<topic>` and shared with the other rwb-payment stories; this release registers no per-story group (RD-P1-066). The ACLs give this service read on the six topics and their retry and dead-letter topics, and write on `rwb.payment.events.v1` and its retry and dead-letter topics only. No other service is given write on this service's topic.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| JOB-07 payment matching | Event-started workflow, started by `AceDataReady` (`sourceSystem` ALS, `status` COMPLETED) | `rwb-payment` | Registered by the worker pool under the build ID of the release; no Schedule |
| `matchPayments` | Activity | `rwb-payment` | Registered by the same worker; mTLS to the Temporal front end |
| `confirmBookings` | Activity | `rwb-payment` | Registered by the same worker |
| `postProceeds` | Activity | `rwb-payment` | Registered by the same worker; the saga step of the settlement and sale flows |
| Rule-cache refresh handler | Event handler of `RulePackageInForce` (section 12.4); not a Temporal workflow or activity, and Temporal Catalog v1 lists no workflow for it | Not applicable (Kafka consumer group) | Deployed with the service; fetch, verify and swap |

The worker pool size, the maximum concurrent activities and the build ID policy are values of the chart. No worker of this release may poll another service's task queue. Every numeric operations value of this release (alert thresholds, rule-cache staleness window and warm-up timeout, outbox-lag and dead-letter limits, consumer concurrency, canary percentage and probe timings) is a chart value; each is Not specified in the source documents (GAP-2508) until the values are set by the DL11 route recorded in section 18. Each secret, the Kafka client credential, the Temporal mTLS material, the registry certificate and the workload identity is referenced by role and recorded in the platform secret-store catalogue; the rwb-payment login (DP-02) is one of them.

#### 12.6 Schedules

None. JOB-07 and JOB-08 are event-started workflows and this release registers no Schedule. The 00:01 rule promote Schedule JOB-20 is rwb-decision's and is neither registered, retimed, duplicated nor disabled here (Arch v5 slide 44).

#### 12.7 Tables owned

| Table | Owner | Deployment element |
|---|---|---|
| `proceeds` | P8 (`rwb_payment`) | Created or migrated by the per-service Flyway sequence; the unique key and the indexes of the matching read |
| `decision_record` | PLT library, created in `rwb_payment` | Created by the same migration job; used by every match |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_payment` | Created by the same migration job; used by the producer, the six consumers and the manual match |

No registry table, no `payment_match_rule` and no other service's table is created, migrated or read by this story (DP-01, DP-15).

#### 12.8 Contract fakes

| Fake | Deployment use |
|---|---|
| rwb-decision WireMock | Runs in the pipeline and in the SIT smoke profile so the release can warm, verify and swap the model without the real service |
| rwb-case WireMock | The same, for the parameters, the reference lists and the session of the business path |
| rwb-treatment WireMock | The same, for the installment-paid call of the smoke match |

The fakes are test-only workloads and are not deployed into UAT or production.

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | None provided, 2 consumed in the deployment path | The version list and the model fetch of the warm-up and the swap; one hop, 2 s |
| Kafka | None published here, 6 consumed and 1 provisioned topic | `rwb.payment.events.v1` with its `.retry` and `.dlt` topics and the ACLs; the six consumer groups of 12.4 |
| Temporal | 1 workflow, 3 activities, no Schedule | The JOB-07 workflow with `matchPayments`, `confirmBookings` and `postProceeds`; the worker pool on `rwb-payment`. The rule-cache refresh is an event handler, not a Temporal element |
| File | None | The release reads no runtime file; the values files are build inputs |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The DP rows that change a deployment artefact are DP-04 (the warm-up, the cache bound and the swap), DP-10 (the worker pool and the absence of a Schedule), DP-14 (the topic, its retry and dead-letter topics and their ACLs), DP-15 (the migration job pinned to one schema) and DP-19 (the route the probes and the smoke step do not use). DP-03 and DP-01 fix what the migration job may create. The advisory H rows are not build dependencies of an OPS story and are carried with the app story.

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-payment/` | Chart with deployment, service, migration job, config map, secret references, probes, the worker pool configuration and the rule-cache warm-up hook |
| `helm/rwb-payment/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, feature switches, the rule-cache bound and warm-up list, the pool sizes, the outbox-lag and dead-letter limits, the alert windows and the canary percentage. Each numeric operations value that has no source is carried as a placeholder in all three files and is closed before UAT by the DL11 route of section 18 |
| Pipeline stage | Build, unit, component and contract tests, image and dependency scan, secret scan, chart publish, canary gate, promote the same artefact |
| Provisioning step | `rwb.payment.events.v1` with its `.retry` and `.dlt` topics and the producer ACL; the six consumer groups; task queue `rwb-payment` in namespace `rwb-recovery` |
| Migration job | The per-service Flyway sequence against `rwb_payment`, with the schema assertion of AC4 |
| Warm-up hook | One version-list read and one model fetch with its checksum, with the timeout from the values |
| Dashboards | Version in force and load time, run outcomes, retry and dead-letter depth, outbox lag, workflow failures, rule-cache staleness |
| Alerts | Four rules, each with its entity, its value and one runbook entry |
| Runbook | Four entries: rule-cache refresh and fallback, dead-letter replay, stuck or missing run, release and rule rollback |

**Probes.** Readiness answers healthy only when the migration is at the expected schema version, the outbox relay is running, the Temporal worker has polled and the version in force of PAYMENT_MATCH is loaded and verified. A registry that answers `NoPackageInForce` is a degraded dependency with its count and does not fail the pod, because a failed pod would hide the business signal. Liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database and neither calls rwb-decision on every check; the warm-up is a start-up step and the refresh is the event.

**Alert mapping.**

| Condition | Alert | Payload | Route |
|---|---|---|---|
| Outbox lag above its value | Outbox lag, with the age of the oldest unsent event and the topic | Topic, age, count | Platform on-call, ticket |
| Dead-letter depth above its value | Dead-letter depth, with the topic, the consumer group and the event type | Topic, consumer group, count, first and last occurrence | Platform on-call, page |
| A workflow failure, or no run started for the business date | Workflow failure, with the workflow ID, the activity and the attempt count | Workflow ID, activity, business date | Platform on-call, page |
| The rule cache is not warm, or is a version behind after its window | Rule-cache stale, with the package code and the version in force | Package code, version in force, loaded version, warm-up duration | Business on-call (RW-COE) and platform on-call, page |

**Rollback runbook.** Two rollbacks, and neither is a code change to a rule. The release rollback returns the previous chart version and keeps the same image digest repository. The rule rollback is one call in rwb-decision (`POST /admin/rule-package-versions/{versionId}/rollback`, owned there); rwb-decision announces the earlier version in force and this service swaps back on the event, so no release is needed and no cache is edited by hand. The cache-purge entry exists only to rebuild the cache from scratch: it empties the cache, the warm-up runs, and the version in force is fetched and verified before readiness reports Warm.

**Canary gate.** The promotion runs a canary slice of the traffic with the previous release still serving; the gate reads the four alert conditions and the run outcome of the canary business date and holds the promotion until the slice is green. The canary percentage and the window are values, not constants (GAP-2508; ASM-4156).

**Done when.** The chart renders in the three environments with every value in its values file, the topic with its retry and dead-letter topics and the ACLs is verified by a test, the six consumer groups exist, the worker pool registers the JOB-07 workflow and no Schedule, the migration job is proven to touch `rwb_payment` only, the secret scan is green and no secret is in a values file, the four panels and the four alerts fire on synthetic metrics, the canary gate blocks a red slice, and the rollback entries are rehearsed by the on-call rota.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-027 | No version is in force for PAYMENT_MATCH, or the run stops on the package-in-force check | The {table} load was refused: {check}. The version in force is unchanged. |
| MSG-P8-001 | A run summary holds unmatched payments and the run is reported on the dashboard | {count} payments for {date} matched no plan and are on the exception list. |
| MSG-P7-003 | The local decision record cannot be written during a run | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A role without the Write-off and posting right calls the read operation of the service | You cannot {action} here. Your role does not include it. |

The texts are copied unchanged from the legacy story and the message catalogue; the deployment adds the alert routing and the runbook link, never a new wording. The checksum mismatch, the cache-staleness, the outbox lag and the dead-letter conditions carry identifiers, counts and durations to the alert and produce no business message. Thai text follows DL10.

### 15. Screens and states

The operator-facing surfaces of this story are the pipeline run view, the release and canary view, the dashboards and the runbook. No business screen is built or changed: SCR-28 Proceeds matching is composed by the gateway-bff route (DP-19) and belongs to the app story, and the version list a person reads to see LOADED, APPROVED, IN_FORCE, SUPERSEDED and REFUSED is rwb-decision's, shown by SCR-39 Rules and parameters in Epic 8. The deployment serves no new screen.

| Where | State | What the operator sees |
|---|---|---|
| The release view | Deploying | The migration job, the probes and the warm-up steps with their result |
| The release view | Ready and Warm | The version in force loaded per package and the build ID of the release |
| The dashboard | Alerting | The condition, the entity and its value, and the runbook link |
| The canary view | Held or green | The canary slice result and the promotion decision |
| The run view | No run for the business date | The workflow-failure signal with the business date and no silent gap |
| SCR-28 Proceeds matching (app story) | Loading | The receipts of the business date are being read; a skeleton, no partial totals |
| SCR-28 Proceeds matching (app story) | Empty | Not specified in the source documents (DOR-RWB-P8-E2027-OPS-10) |
| SCR-28 Proceeds matching (app story) | Error | Not specified in the source documents (DOR-RWB-P8-E2027-OPS-10) |
| SCR-28 Proceeds matching (app story) | No access | A role without the Write-off and posting right is refused with MSG-P4-002 |
| SCR-39 Rules and parameters (Epic 8) | Empty | No version is listed for the package yet: an empty list with a total of 0 and no error |
| SCR-39 Rules and parameters (Epic 8) | Loading | Not specified in the source documents (DOR-RWB-P8-E2027-OPS-10) |
| SCR-39 Rules and parameters (Epic 8) | Error | Not specified in the source documents (DOR-RWB-P8-E2027-OPS-10) |
| SCR-39 Rules and parameters (Epic 8) | No access | Not specified in the source documents (DOR-RWB-P8-E2027-OPS-10) |

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-P8-E2027-OPS-01 | AC1 | NFR | The warm-up loads "PM-2026.12" and verifies its checksum; a synthetic RulePackageInForce swaps a newer version; a bad checksum keeps the version in force; NoPackageInForce stops the run with MSG-P3-027 and substitutes nothing |
| TC-P8-E2027-OPS-02 | AC2 | NFR | `rwb.payment.events.v1` with its `.retry` and `.dlt` topics and the ACLs; the six consumer groups; a failed swap reaches the `.dlt`; a repeated event starts no second run |
| TC-P8-E2027-OPS-03 | AC3 | NFR | Task queue `rwb-payment` registered with the payment matching workflow and three activities under the release build ID; a synthetic `AceDataReady` starts one run; no Schedule is registered; a non-polling worker is visible |
| TC-P8-E2027-OPS-04 | AC4 | NFR | The migration job applies the sequence to `rwb_payment` only; `proceeds` and the four library objects exist; no registry table and no `payment_match_rule`; the schema assertion fails a job that names another schema |
| TC-P8-E2027-OPS-05 | AC5 | NFR | The rendered chart and the running workload hold only secret references; the secret scan fails a secret in code, a values file, a test or a log; a rotation is picked up without a rebuild |
| TC-P8-E2027-OPS-06 | AC6 | NFR | The four alerts fire on synthetic metrics and link one runbook entry each; the canary gate holds a red slice and promotes a green one; the release rollback and the one-call rule rollback are rehearsed |
| TC-P8-E2027-OPS-07 | AC2, AC3 | NFR | Contract test: every operation, event and activity of section 12 (the paths, the event types and topics of section 12.4, and the activities) matches the published contracts; a missing or renamed one fails the build |
| TC-P8-E2027-OPS-08 | AC4 | NFR | Boundary test of each table in section 12.7 (ASM-3438): proceeds and the four library objects are created in rwb_payment only and no other table is touched at the boundary; a job that crosses it fails |
| TC-P8-E2027-OPS-09 | AC5, AC6 | NFR | Dashboards, alerts and runbooks hold no case fact or personal datum; the alert thresholds, cache-staleness window, outbox-lag and dead-letter limits, pool sizes, canary percentage and probe timings are read from chart values, and a template or code constant fails the check |
| TC-P8-E2027-OPS-10 | AC7 | NFR | The traceability check reads section 8 and section 16; a rule with no criterion or no test fails it; a guardrail or boundary test stands in for an architecture constraint |
| TC-P8-E2027-OPS-11 | AC8 | NFR | A synthetic consumed call that fails and one that does not answer each reach the `.retry` topic and then the `.dlt` topic, are not acknowledged as processed, and raise the dead-letter depth alert |
| TC-P8-E2027-OPS-12 | AC9 | NFR | A synthetic status change the model does not allow is refused, writes no outbox event and is not acknowledged as processed |

Legacy test cases TC-E2-027-01 to TC-E2-027-13 are owned by RWB-P8-E2027-APP; this story adds the twelve deployment and operations cases above, all at Level NFR, and renumbers none of them.

### 17. Guardrails

- No business value in a values file: the match type, the row order (the target name of the ordering column; priority is its legacy and TSD name), the amount tolerance, the window, the grace and the partial floor are rows of the PAYMENT_MATCH package and rows of the registry. The cache bound, the warm-up list and the alert windows are configuration, not rule content.
- No personal data in logs, dashboard series, alert payloads, workflow history or the runbook: payment codes, case references, package codes, version labels, checksums, counts and durations only.
- One topic and one consumer group set per service; the 00:01 promotion Schedule JOB-20 is never registered, retimed, duplicated or disabled in this release (DP-10, DP-14).
- The service writes only schema `rwb_payment` and the registry is reached only through its two operations; the migration job creates no registry table (DP-01, DP-04, DP-15).
- Every topic has a retry topic and a `.dlt` topic and the consumer dedupes through the inbox (DP-09 as the platform pattern; RWB-PLT-TE006-CON).
- The release pins the image digest and the chart version; a rebuild between environments is not allowed and no rule version is ever shipped in the image (BR10).
- No secret is written into a values file, a chart template, a dashboard or the runbook; every one is a key-store reference under the workload's own identity (BR7).
- A red canary slice or a red gate blocks the promotion, and no gate is waived for a release (BR10).
- No ACE data is copied into a dashboard, a log or a topic; the freshness signal of the source is P1's (DP-05).

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-CHO-009 | Payments matched to the plan by the approved and dated rule version; unmatched to an exception list | The rule-cache refresh and fallback, the run visibility and the stopped-run signal | TC-P8-E2027-OPS-01, TC-P8-E2027-OPS-03 |
| ADR-017 | Embedded Drools per service; rule registry in rwb-decision | The warm-up, the cache bound and the swap on `RulePackageInForce` | TC-P8-E2027-OPS-01 |
| ADR-023 | Observability per service | The four panels, the four alerts and the four runbook entries | TC-P8-E2027-OPS-06 |
| ADR-021 | Per-service Flyway and migration ownership | The migration job pinned to `rwb_payment` and its schema assertion | TC-P8-E2027-OPS-04 |
| DP-10 | Schedules and event-started workflows | The worker pool and the JOB-07 workflow with no Schedule of this release | TC-P8-E2027-OPS-03 |
| D-RCV-36 T10 | `payment_match_rule` is retired | The migration assertion that the retired table is never created | TC-P8-E2027-OPS-04 |
| NFR-052 | Secrets held in the key store and never in code or configuration | The secret references and the pipeline secret scan | TC-P8-E2027-OPS-05 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E2-027, disposition Split (rework) |
| Legacy criteria | AC6, AC7 and AC10 owned by RWB-P8-E2027-APP; AC1, AC2, AC4, AC5, AC8 and AC9 by RWB-P8-E2008-APP; AC3 by RWB-P7-E2027-APP; this story copies none |
| Test cases | The six new deployment cases `TC-P8-E2027-OPS-01` to `-06`; the legacy thirteen are owned by RWB-P8-E2027-APP |
| Feature and screen | FEAT-OCC-10, FEAT-PAY-01; SCR-28 served, not built here |
| Decoupling patterns | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Architecture decisions | ADR-014 (schema and login per service), ADR-015 (Kafka with outbox), ADR-016 (Temporal replaces Quartz), ADR-017 (embedded Drools, registry in rwb-decision), ADR-021 (per-service Flyway), ADR-023 (observability per service) |
| Decision DL10 (Thai names of fields, labels and messages) | Recommended resolution accepted by the programme directive: the business lead drafts per module one epic ahead; Legal and Compliance approve. Assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 are confirmed |
| Decision DL11 (non-functional target values) | Recommended resolution accepted by the programme directive: use the ACE values where ACE has them; the solution architect proposes the rest; Risk agrees. Assumptions ASM-0553, ASM-0703, ASM-1051 and ASM-1104 are confirmed |

### 19. Out of scope

- The matching code, the facts builder, the version resolver, the decision writer and the event writer (RWB-P8-E2027-APP).
- The contract document, its schemas, its `Idempotency-Key` rule, its error envelope and its fakes (RWB-P8-E2027-CON).
- The registry and the governance of a package version, the load checks, the four-eyes approval, the 00:01 promotion Schedule JOB-20 and the one-call rule rollback operation (RWB-P7-E2027-APP).
- The PAYMENT_MATCH workbook, its Rows and Tests tabs and the authoring pipeline (RWB-P3-E2042-APP, RWB-P3-E1073-APP).
- The platform topic provisioning implementation, the schema registry and the Temporal cluster itself (RWB-PLT-EVT, RWB-PLT-N002-INF, RWB-PLT-N008-INF, RWB-PLT-WF).
- The database schema, login and grants of `rwb_payment` (RWB-PLT-DB and the per-service DB story).
- The gateway-bff composite route and the SCR-28 screen (RWB-PLT-N001-CON and the app story).
- The numeric alert thresholds, cache-staleness window, outbox-lag and dead-letter limits, pool sizes, canary percentage and probe timings, which are reviewed values and Not specified in the source documents (GAP-2508; ASM-4156).
- The names of the secrets, of the workload identity and of the certificate, which are Not specified in the source documents (GAP-2508; ASM-4157).
- The real cross-service proof of the refresh, the run and the rollback across rwb-payment and rwb-decision: the wave 2 harness. Its ALS payment fixture, JOB-07 window control (opened by publishing `AceDataReady`), seed pack, evidence format and pass or fail gate belong to the wave 2 integration story of RWB-E2-027; the rule version is loaded through `POST /api/recovery/decision/v1/admin/rule-packages/PAYMENT_MATCH/versions`.

Change log: D-RCV-60 (realignment v1), 22 November 2026. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
