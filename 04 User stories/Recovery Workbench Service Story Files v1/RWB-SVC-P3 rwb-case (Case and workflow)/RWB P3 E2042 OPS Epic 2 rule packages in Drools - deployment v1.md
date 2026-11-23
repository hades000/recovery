# RWB-P3-E2042-OPS Epic 2 rule packages in Drools

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2042-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-042 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P3-AO |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-027, FR-P3-028, FR-P3-029) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-042 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform engineer**, I want **rwb-case deployed with Helm values for the model cache bound and the model warm-up, a RulePackageInForce consumer group on `rwb.decision.events.v1` with its retry and `.dlt` topics, a readiness signal that reports whether the model in force is loaded, four dashboards and three alerts on the package state and the evaluation latency, a runbook whose rollback is one call in rwb-decision followed by the swap back in this service, and a pipeline step that runs `RuleScenarioBuildGate` and `PaymentMatchRuleAbsentCheck` on every build**, so that **an operator can see which package version is deciding, catch a cold cache or a checksum mismatch before a case is affected, and return to the previous version without a release**.

### 2. Business rationale

A rule package is data, so the only thing that can go wrong at run time is the state of the copy this service holds: it can be cold, it can be a version behind, it can fail its checksum, or no version can be in force at all — and each of those looks from the outside like "the service is up". The legacy story relied on a build gate and a manual check of the version list; the target adds an event that announces a new version and a local cache that must be warm for the service to decide (Arch v5 slide 27; Temporal and Drools slides 15, 16 and 28).

Deployment is therefore part of the capability. The cache bound and the warm-up must be values, not constants, because the same image runs in three environments. The consumer group needs a retry path and a `.dlt`, because a lost RulePackageInForce is a service that silently decides on yesterday's rules. Readiness must tell an operator whether the model in force is loaded, and the dashboards must show the version in force per package, the load failures, the checksum mismatches, the `NoPackageInForce` count and the evaluation latency against the 300 ms target. Only then can the on-call rota act before a decision is taken on the wrong table.

The 00:01 promotion Schedule is rwb-decision's: this story consumes its event and never registers, retimes or duplicates it.

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The Temporal workflow kit and the `rwb-recovery` namespace are available (RWB-PLT-WF, RWB-PLT-E1071-CON), because the model swap is an event-started workflow on task queue `rwb-case` (DP-10).
- The Kafka event platform provisions topics with a retry topic and a `.dlt` topic and applies topic ACLs (RWB-PLT-EVT, RWB-PLT-TE006-CON).
- The container `rule-packages`, the workload identity and the rwb-decision certificate exist (RWB-P3-E2042-INF).
- The rwb-decision service publishes `rwb.decision.RulePackageInForce.v1` on `rwb.decision.events.v1` (EV-30) and owns the 00:01 promotion (JOB-20; Arch v5 slide 44).
- The three package codes and version labels are agreed: RESTRUCTURE "RES-2026.12", PAYMENT_MATCH "PMT-2026.12", BOOKING_MATCH "BKG-2026.12".
- The platform error envelope and the message catalogue are in force, so an alert can carry a message ID where a message exists.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The pipeline builds the service image, runs the unit, component and contract tests, and runs the two rule gates before it publishes the chart.
2. `RuleScenarioBuildGate` runs the 174 scenarios of the three in-force versions from the release manifest; `PaymentMatchRuleAbsentCheck` runs on a Testcontainers database and asserts 93 tables, no `payment_match_rule` and no column of DF-REF-261 to DF-REF-273.
3. The chart deploys the service with its own login, its migration job, its probes and the three rule-package values: the cache bound of 20, the warm-up list and the warm-up timeout.
4. The warm-up step asks the version list once at start-up and fetches the model in force of each package in the warm-up list, so the first case of the morning does not pay the fetch.
5. The provisioning step creates the consumer group of rwb-case on `rwb.decision.events.v1` with the retry topic and the `.dlt` topic, and registers task queue `rwb-case` in namespace `rwb-recovery`.
6. The readiness signal reports the schema version, the worker polling state and the model state of each package in the warm-up list.
7. The dashboards are published: version in force per package, model load failures, checksum mismatches, `NoPackageInForce` count and evaluation latency against the 300 ms target.
8. The three alerts are wired to the runbook entries: cache cold, checksum mismatch and package not in force.
9. A smoke step asserts in a test namespace that a synthetic RulePackageInForce event swaps the model and that readiness and the dashboards reflect it.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The model in force is not loaded when the pod starts | Readiness reports the package as not warmed; the alert "cache cold" fires after the warm-up window | None | AC3, AC5 |
| X2 | A RulePackageInForce event fails the swap | The activity retries on the kit policy; after the last attempt the event goes to the retry topic and then to `.dlt` with an alert, and the model in force stays | None | AC2, AC5 |
| X3 | A fetched model fails its checksum | No swap; the mismatch is counted with the package code and both checksums, and the "checksum mismatch" alert fires | None | AC4, AC5 |
| X4 | No version is in force for a package | `NoPackageInForce` is counted per package and the "package not in force" alert fires once per package per window; the message text is MSG-P3-027 | MSG-P3-027 | AC4, AC5 |
| X5 | The build gate fails on a scenario or on a table | The pipeline stops before the chart is published; nothing is deployed | None | AC6 |
| X6 | The 00:01 promotion does not run in rwb-decision | No event arrives; the version in force on the dashboard does not change and the "package not in force" path is the visible symptom, owned with rwb-decision | MSG-P3-027 | AC2, AC5 |
| X7 | A rollback is called in rwb-decision | rwb-decision announces the earlier version and the consumer swaps back to it; no release of this service is needed | None | AC5 |
| X8 | The evaluation latency exceeds the 300 ms target | The latency panel shows the breach and the package code; the card is reviewed with the rule owner, and nothing is restarted | None | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the platform topic provisioning, the workflow kit and the two gates; no application code is built here |
| Negotiable | Replica counts, the warm-up list, the alert windows and the resource sizes are environment values, not story decisions |
| Valuable | Makes the package state, the swap and the evaluation latency visible and operable, and makes a rollback a call rather than a release |
| Estimable | One chart with three values, one warm-up step, one consumer group with retry and `.dlt`, four dashboards panels, three alerts, four runbook entries and one pipeline step |
| Small | Fits one sprint with the runbook |
| Testable | Every criterion tests an artefact: a rendered chart, a provisioned group, a readiness answer, a synthetic metric and a gate result |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the Epic 2 rule packages in rwb-case

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the target environment is SIT
    Given the three package codes are RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH

  Scenario: AC1 The chart carries the cache bound and the warm-up as values (new, D-RCV-60)
    Given the rwb-case Helm chart and its values files
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the model cache bound, the warm-up list and the warm-up timeout come from the values files
    Then no cache bound, no warm-up entry and no evaluation timeout is hard-coded in a chart template or in code
    Then the warm-up list names the three package codes and their versions in force and nothing else
    Then the migration job runs the per-service Flyway sequence in schema rwb_case before the deployment is marked ready

  Scenario: AC2 The RulePackageInForce consumer group has a retry path and a dead-letter topic (new, D-RCV-60)
    Given the provisioning step for rwb-case
    When it runs against the environment
    Then the consumer group of rwb-case exists on rwb.decision.events.v1
    Then the retry topic and the .dlt topic exist and are configured on the consumer
    Then a failed swap is retried on the kit policy and then routed to the retry topic and the .dlt topic with an alert
    Then the consumer dedupes through the inbox, so a repeated event starts no second swap
    Then the 00:01 promotion Schedule is not registered, retimed or duplicated in this release

  Scenario: AC3 Readiness reports whether the model in force is loaded (new, D-RCV-60)
    Given a running rwb-case pod
    When readiness is called before the migration job, the start-up window and the warm-up complete
    Then the pod is not marked ready
    When the warm-up has loaded the model in force of each package in the warm-up list
    Then readiness answers healthy and names the version loaded per package
    Then a package with no version in force is reported as a degraded dependency with the NoPackageInForce count, not as a live-and-broken pod
    Then neither probe writes to a database and no probe calls rwb-decision on every check

  Scenario: AC4 Four dashboard panels report the package state and the latency (new, D-RCV-60)
    Given the published dashboard of rwb-case
    When its panels are reviewed
    Then one panel shows the version in force per package and the time it was loaded
    Then one panel shows model load failures and checksum mismatches with the package code and the version label
    Then one panel shows the NoPackageInForce count per package
    Then one panel shows the evaluation latency with the 300 ms target marked and the breach counted
    Then no panel carries a case fact, a person or a personal datum

  Scenario: AC5 Three alerts and four runbook entries cover the package state (new, D-RCV-60)
    Given the published alerts and the runbook
    When a synthetic state is replayed for a cold cache, a checksum mismatch and a package not in force
    Then each condition raises its alert with the package code and the version label
    Then the package-not-in-force alert carries the message text of MSG-P3-027 and links the runbook entry of its owner role
    Then the rollback runbook entry is one call in rwb-decision, followed by the swap back in this service, with no release
    Then the cache-purge entry empties the model cache and warms the versions in force again
    Then every alert links exactly one runbook entry with the check, the owner role and the recovery step

  Scenario: AC6 The pipeline runs the two rule gates on every build (new, D-RCV-60)
    Given a commit on the main line
    When the pipeline runs
    Then it runs RuleScenarioBuildGate over the three versions in the release manifest and fails on a failing scenario
    Then it runs PaymentMatchRuleAbsentCheck on a Testcontainers database and fails when payment_match_rule or any column of DF-REF-261 to DF-REF-273 exists
    Then it promotes the same image and chart artefact through DEV, SIT and UAT without a rebuild
    Then a red gate blocks the merge and the promotion
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The cache bound, the warm-up list and the warm-up timeout are values per environment; no template or code constant carries them | DP-04; Template and Rules §R7.2 s17 |
| BR2 | Every topic has a retry topic and a `.dlt` topic, and a consumer never acknowledges an event it could not process | DP-09; Arch v5 slide 22 notes |
| BR3 | The model swap is an event-started workflow on task queue `rwb-case`; the 00:01 promotion Schedule belongs to rwb-decision and is not registered here | DP-10; Arch v5 slide 44 |
| BR4 | Readiness answers healthy only when the schema is at the expected version, the worker polls and the model in force of the warm-up list is loaded; a package with no version in force is a degraded signal, not a failed pod | Arch v5 slide 27; Temporal and Drools slide 28 |
| BR5 | Every alert carries the package code and the version label, and links one runbook entry with the owner role; where a message exists its text is the agreed text | Template and Rules §R7.2 s14 |
| BR6 | A rollback is one call in rwb-decision; this service swaps back on the event and is never redeployed to change a rule | Arch v5 slide 27; Temporal and Drools slide 15 |
| BR7 | The two rule gates run in every build and a red gate blocks the merge and the promotion | REQ-CWC-014; D-RCV-36 T4, T10 |
| BR8 | Nothing on a dashboard, an alert or a runbook carries a case fact or a personal datum | Template and Rules §R7.2 s17 |
| BR9 | No secret is written into a values file, a chart template, a dashboard or a runbook; all come from the platform secret store | RWB-P3-E2042-INF |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart, the two rule gates and the migration job pass | Deploying |
| Deploying | Migration complete and probes healthy | The schema is at the expected version and both probes answer | Ready |
| Ready | Warm-up complete | The model in force of each package in the warm-up list is cached | Warm |
| Warm | RulePackageInForce arrives | The checksum verifies and the swap succeeds | Warm (new version) |
| Warm | Checksum mismatch or swap failure | The last good model stays and the alert fires | Warm (unchanged; alerting) |
| Warm | Rollback called in rwb-decision | The earlier version is announced and swapped back | Warm (earlier version) |
| Warm | Release superseded | A new chart version is promoted | Rolling |
| Rolling | All pods on the new version | The old ReplicaSet drains and each pod is Warm | Warm |
| Any | The gate is red | A scenario fails or the schema assertion fails | Failed; nothing is published |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the provisioning step, the dashboards, the alerts and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the topic provisioning and the consumer group rights |
| ACE database administrator | Owns the `rwb_case` schema, the login and its grants, and approves the migration job |
| Release manager | Approves the promotion of one artefact through the environments |
| RW-COE, center of excellence analyst | Owns the rule content and the runbook entry for a package not in force |
| RW-RISK, risk and model risk officer | Calls the rollback in rwb-decision, which is one call |
| On-call operator | Runs the runbook entries and opens an incident when an alert persists |

The identity the chart uses for the container and the certificate is Not specified in the source documents (GAP-0722; ASM-1269); the chart references "the rwb-case workload identity (DP-02)" through a secret reference and never a literal name.

### 11. Data

| Item | Content |
|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, feature switches, the model cache bound, the warm-up list, the warm-up timeout |
| Schema | rwb_case, migrated by the per-service Flyway sequence; no table is added for the packages |
| Consumer group | rwb-case on `rwb.decision.events.v1`, with the retry topic and the `.dlt` topic |
| Queue | Temporal task queue `rwb-case` in namespace `rwb-recovery` |
| Dashboard series | Version in force per package and the time loaded, model load failures, checksum mismatches, NoPackageInForce count, evaluation latency, swap duration, cache size |
| Alerts | Cache cold, checksum mismatch, package not in force |
| Runbook entries | Cache cold and warm-up, checksum mismatch, package not in force with the rollback call, cache purge |
| Secrets | The rwb-case login secret, the Kafka client credential, the Temporal mTLS material and the rwb-decision certificate reference, all from the platform secret store |

The alert windows, the replica counts, the resource sizes and the exact probe timings are Not specified in the source documents (GAP-0723; ASM-1270); the chart exposes them as values and this story fixes only their names and the rule that they are not hard-coded.

### 12. Contract

#### 12.1 REST operations provided

None provided by this story. The deployment exposes the case read operations of the service through gateway-bff, and they are declared in their own contract story. The probes are cluster-internal and are not part of the API surface.

#### 12.2 REST operations consumed

| Method | Path | Owner | Deployment need |
|---|---|---|---|
| GET | `/api/recovery/decision/v1/rule-models/{packageCode}/{version}` | P7 rwb-decision | The warm-up fetch and the swap; one hop, 2 s client budget (DP-11) |
| GET | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | P7 rwb-decision | The warm-up resolves the version in force per package |

#### 12.3 Events published

None. This story publishes no event; the model swap records nothing on a topic.

#### 12.4 Events consumed

| Event | Topic | Provisioning |
|---|---|---|
| `rwb.decision.RulePackageInForce.v1` | `rwb.decision.events.v1` | Consumer group for rwb-case with the inbox, the retry topic and the `.dlt` topic; one swap per package code and version label |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| RuleModelSwap | Workflow started by RulePackageInForce | `rwb-case` | Worker deployment with the build ID of the release; no Schedule registration |
| swapRuleModel | Activity | `rwb-case` | Registered by the same worker; mTLS to the Temporal front end |
| EvaluateRules, RecordAndApply | Activities (workflow kit) | `rwb-case` | Registered by the same worker |

#### 12.6 Schedules

None. The 00:01 promotion is the Temporal Schedule JOB-20 in rwb-decision and is out of scope; this release registers no Schedule for a rule package (Arch v5 slide 44).

#### 12.7 Tables owned

| Table | Owner | Deployment element |
|---|---|---|
| recovery_case, timer, queue | P3 (rwb_case) | Created by the per-service Flyway sequence; no column is added for the packages |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | Created by the same migration job; used by the inbox of the RulePackageInForce consumer |

#### 12.8 Contract fakes

| Fake | Deployment use |
|---|---|
| rwb-decision WireMock | Runs in the pipeline and in the SIT smoke profile so the release can warm and swap the three models without the real service |
| rwb-access WireMock | Same, for the admin read right |

The fakes are test-only workloads and are not deployed into UAT or production.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None provided, 2 consumed in the deployment path | The model fetch and the version list for the warm-up; one hop, 2 s |
| Kafka | None published, 1 consumed | `rwb.decision.events.v1` with the retry topic and the `.dlt` topic |
| Temporal | 1 workflow, 5 activities, no Schedule | RuleModelSwap; swapRuleModel, EvaluateRules, RecordAndApply and the warm-up activity |
| File | None | The release reads no file; the values files are build inputs, not runtime data |

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
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-case/` | Chart with deployment, service, migration job, config map, secret references, probes and the warm-up hook |
| `helm/rwb-case/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, feature switches, the model cache bound, the warm-up list, the warm-up timeout |
| Pipeline stage | Build, unit, component and contract tests, the two rule gates, image and dependency scan, chart publish, promote the same artefact |
| Provisioning step | Consumer group of rwb-case on `rwb.decision.events.v1` with the retry topic and the `.dlt` topic; task queue `rwb-case` in namespace `rwb-recovery` |
| Warm-up hook | One version list read and one model fetch per package in the warm-up list, with the timeout from the values |
| Dashboards | Four panels: version in force, load failures and checksum mismatches, NoPackageInForce count, evaluation latency against 300 ms |
| Alerts | Three rules, each with the package code, the version label and one runbook entry |
| Runbook | Four entries: cache cold and warm-up, checksum mismatch, package not in force with the rollback call, cache purge |

**Probes.** Readiness answers healthy only when the migration is at the expected schema version, the outbox relay is running, the Temporal worker has polled, and the model in force of each package in the warm-up list is cached. A package with no version in force is reported as a degraded dependency with its `NoPackageInForce` count and does not fail the pod. Liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database, and neither calls rwb-decision on every check; the warm-up is a start-up step and the refresh is the event.

**Alert mapping.**

| Condition | Alert | Payload | Route |
|---|---|---|---|
| The model in force is not cached after the warm-up window | Cache cold, with the package code and the version label | Package code, version label, warm-up duration | Platform on-call, ticket |
| A fetched model fails its SHA-256 check | Checksum mismatch, with the package code, the version label and both checksums | Package code, version label, expected and computed checksum | Platform on-call and the rwb-decision owner, page |
| No version is in force for a package | Package not in force, with the package code and the text of MSG-P3-027 | Package code, first and last occurrence in the window | Business on-call (RW-COE), page |
| Evaluation latency above 300 ms | Latency breach on the latency panel and the dashboard card | Package code, version label, p95 and p99 | Dashboard, no page |

**Rollback runbook.** The rollback is one call in rwb-decision (`POST /admin/rule-package-versions/{versionId}/rollback`, owned there). rwb-decision announces the earlier version in force, and the consumer of this service swaps back on that event; no release of rwb-case is needed and no cache is edited by hand. The cache-purge entry exists only for the case where an operator must rebuild the cache from scratch: it empties the model cache, the warm-up runs again, and the versions in force are fetched and verified before readiness reports Warm.

**Done when.** The chart renders in all three environments with the cache bound and the warm-up as values, the consumer group and its retry and `.dlt` topics are verified by a test, readiness reports the version loaded per package, the four panels and the three alerts fire on synthetic metrics, the rollback and cache-purge entries are rehearsed by the on-call rota, and the two gates run in the pipeline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-027 | No version is in force for a package | The rule version was refused at the {check} check: {detail}. |
| MSG-P7-002 | The approver is the author | You prepared this decision, so you cannot approve it. |
| MSG-GEN-004 | The version label is already loaded | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-001 | An empty workbook | Enter {field}. |
| MSG-GEN-003 | Valid from before today | {field} cannot be before {other}. |
| MSG-P4-002 | A role without Rules and parameters calls a package operation | You cannot {action} here. Your role does not include it. |

The texts are copied unchanged from the legacy story and the message catalogue; the deployment adds the alert routing and the runbook link, never a new wording. The checksum mismatch and the cache-cold condition carry the package code, the version label and the two checksums or the warm-up duration to the alert, and produce no business message.

### 15. Screens and states

The operator-facing surfaces of this story are the pipeline run view, the release view, the dashboard and the runbook. The version list a person reads to see the states LOADED, APPROVED, IN_FORCE, SUPERSEDED and REFUSED is rwb-decision's, shown by SCR-39 Rules and parameters in Epic 8; this story only carries the version in force per package onto its own dashboard. The deployment serves no new screen.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E2042-OPS-01 | AC1 | NFR | The chart renders for DEV, SIT and UAT with the cache bound, the warm-up list and the timeout from values only |
| TC-P3-E2042-OPS-02 | AC2 | NFR | The consumer group, the retry topic and the `.dlt` topic exist; a failed swap reaches the `.dlt` with an alert; no promotion Schedule is registered |
| TC-P3-E2042-OPS-03 | AC3 | NFR | Readiness false before the migration and the warm-up, then healthy with the version per package; a package with no version in force is degraded only |
| TC-P3-E2042-OPS-04 | AC4 | NFR | The four panels show a synthetic version in force, a load failure, a checksum mismatch, a NoPackageInForce count and a 300 ms latency breach |
| TC-P3-E2042-OPS-05 | AC5 | NFR | The three alerts fire on synthetic state and link one runbook entry each; the rollback and the cache purge are rehearsed |
| TC-P3-E2042-OPS-06 | AC6 | Integration | The pipeline runs both gates, fails on a failing scenario and on a created payment_match_rule, and blocks the promotion |

### 17. Guardrails

- No business value in a values file: rows, tolerances, windows, action text, owner roles and timers stay in the workbooks and the registry; the cache bound and the warm-up are configuration, not rule content.
- No personal data in logs, dashboard series, alert payloads or the runbook: package codes, version labels, checksums, counts and durations only.
- One topic and one consumer group per service; the 00:01 promotion Schedule is never registered, retimed or duplicated in this release (DP-10, DP-14).
- The service writes only schema rwb_case and reads no registry table; the packages come over the rwb-decision operations (DP-01, DP-04).
- Every topic has a retry topic and a `.dlt` topic, and the consumer dedupes through the inbox (DP-09).
- The release pins the image digest and the chart version; a rebuild between environments is not allowed, and no rule version is ever shipped in the image.
- No secret is written into a values file, a chart template, a dashboard or the runbook; all come from the platform secret store.
- A red gate blocks the merge and the promotion; `PaymentMatchRuleAbsentCheck` is never waived for a release.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-CWC-013 | Rule change by validated load with a version and rollback by one call | The rollback runbook entry, the RulePackageInForce consumer group and the swap-back path | TC-P3-E2042-OPS-02, TC-P3-E2042-OPS-05 |
| REQ-CWC-014 | Schema, overlap, unreachable, default and scenario checks before a rule takes effect | The pipeline step that runs RuleScenarioBuildGate and PaymentMatchRuleAbsentCheck | TC-P3-E2042-OPS-06 |
| ADR-017 | Embedded Drools per service; rule registry in rwb-decision | The cache bound and warm-up values, the readiness signal and the version-in-force panel | TC-P3-E2042-OPS-01, TC-P3-E2042-OPS-03, TC-P3-E2042-OPS-04 |
| ADR-023 | Observability per service | The four panels, the three alerts and the four runbook entries | TC-P3-E2042-OPS-04, TC-P3-E2042-OPS-05 |
| DP-10 | Schedules and event-started workflows | The swap as an event-started workflow; no Schedule registered here | TC-P3-E2042-OPS-02 |
| D-RCV-36 T10 | `payment_match_rule` is retired | The gate that fails a release that creates the table | TC-P3-E2042-OPS-06 |

### 19. Out of scope

- The cache, the swap, the catalog client and the model verification code (RWB-P3-E2042-APP).
- The authoring, consumption and activity contract as a document (RWB-P3-E2042-CON).
- The container, the identity, the certificate, the sizing and the isolated gate database (RWB-P3-E2042-INF).
- The registry, the three seed rows, the admin operations, the four-eyes approval, the one-call rollback and the 00:01 promotion Schedule JOB-20 (RWB-P7-E2042-APP; ASM-0069).
- The platform topic provisioning implementation, the Temporal cluster and the schema registry (RWB-PLT-EVT, RWB-PLT-WF, RWB-PLT-N008-INF).
- The case screens and the composite route specification (platform edge story and RWB-P3-E1023-APP).
- The exact alert windows, replica counts, resource sizes and probe timings, which are reviewed values and Not specified in the source documents (GAP-0723; ASM-1270).
