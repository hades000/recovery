# RWB-PLT-N004-OPS Service pipeline template and Helm chart

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-N004-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-TPL |
| Wave | 0 |
| Size | Not specified in the source documents (DOR-RWB-PLT-N004-OPS-16) |
| Business epic | NEW |
| Release | None (new story) |
| Legacy key | N004 |
| Legacy disposition | New |
| Build status | Not started |
| Patterns applied | None |
| Parallel lane | L-PLT-TPL-A |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | Contract story named in DOR-RWB-PLT-N004-OPS-21 (not a story of this set) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: new platform story (N004, service template and repositories — one service pipeline template and one Helm chart for all 19 services, built once in wave 0). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (5 resolved, 7 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **DevOps engineer**, I want **one service pipeline template and one Helm chart, versioned and pinned, that render all 19 services from one values file per service**, so that **every service of wave 1 to wave 4 is built, tested and deployed the same way, the api tier stays at 2 fixed pods while the worker tier follows its own Temporal task queue, and no service team forks the chart or the pipeline**.

### 2. Business rationale

The split into 19 services is only affordable if the delivery machinery is built once. Arch v5 slide 38 makes this the first item of wave 0: the platform is built once as "service template + Helm", contract libraries, workflow kit, 19 schemas and logins, Kafka topics and ACLs and Temporal 1.30+, and slide 38's note names "service template (Spring Boot, outbox, inbox, Temporal worker, codec, OpenTelemetry), one Helm chart, golden pipeline". Every later wave then adds only its own services. Without that, wave 1 alone would put nine services in front of nine teams who each invent a chart, a stage list and a promotion habit, and the same defect would be fixed nine times in nine dialects.

The shape the chart has to render is fixed by the architecture. Slide 33 gives every one of the 19 services the same shape — a front of 2 fixed api copies and a back of workers that grow with the queue, with KEDA watching the service's own task queue, so a bursty service can shrink to zero workers and a busy one can grow — and slide 48 repeats that the screens are light ("2 small pods per service are enough") and that scaling is by worker pools (KEDA) on the few hot paths. Slide 20 gives every service `/health` and `/metrics` for the platform, its own task queue `rwb-<svc>`, its own schema with outbox, inbox and decision record, and its own Temporal worker. Slide 29 and R4 fix one schema and one login per service and no cross-schema grant. R4 fixes the derived names the values file must carry: schema `rwb_<short with _>`, topic `rwb.<short>.events.v1`, task queue `rwb-<short>`, REST base `/api/recovery/<short>/v1`.

Two requirements sit directly on the pipeline. NFR-052 (section 6.9, Proposed) says secrets are held in the key store and never in code, configuration files or prompts — so a chart that carries a password is a defect, not a convenience. NFR-054 (section 6.9, Proposed) says the build pipeline blocks a change that carries a secret, personal data in code, tests or logs, or an unapproved dependency — so the blocking checks are part of the template and cannot be left to a service team's goodwill. ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop) and ADR-021 (per-service Flyway and migration ownership) all reach the cluster and the pipeline through this chart and this template, and the migration lint and the drift gate they imply are the RWB-PLT-E1044-CON gate that this story calls as a stage rather than reimplements.

This is Day-1 wave 0 work with no build dependency. The nine services of wave 1 cannot start their OPS stories before it exists, and every service OPS story from wave 1 onwards inherits it and adds nothing but its own values file.

### 3. Preconditions

- The 19-service list and the short names of Template and Rules §R4 and Arch v5 slide 41 are fixed (`source-data`, `integration`, `case`, `access`, `document`, `comms`, `decision`, `payment`, `reporting`, `agent`, `valuation`, `treatment`, `guarantee`, `litigation`, `asset`, `debtsale`, `writeoff`, `deviation`, `partner`), because every derived name in a values file is computed from the short name.
- The platform chart repository and the pipeline template repository exist as platform-owned repositories, and both are read by the service repositories at the version each service pins.
- The Kafka event platform epic (RWB-PLT-EVT) has fixed the topic naming and the retry and `.dlt` naming the chart does not create, and the ACE DB epic (RWB-PLT-DB) has fixed the per-service login so that the connection reference in a values file has a target.
- The Temporal namespace `rwb-recovery` exists and each service's worker polls its own task queue `rwb-<short>` (Arch v5 slides 20 and 41).
- The key store, the container registry and the bank's CI service exist as platform resources, and the key store is reachable from the deploying pipeline and from the pods at run time.
- The RWB-PLT-E1044-CON contract publishes the migration lint and the drift gate as callable pipeline stages with a published result, because this story runs that gate as a stage and does not write it.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).
- The chart name, the chart repository name, the registry and image naming, the resource sizes, the KEDA thresholds, the toolchain, the promotion gates and the chart version scheme are Not specified in the source documents (GAP-1424; ASM-2492).

### 4. Flow

1. Lay down the one chart with its `Chart.yaml`, its default `values.yaml` and its values schema, and with no template that hard-codes a service name, a schema, a topic, a queue, a port or a resource size.
2. Declare the values-file contract: `name`, `short`, `schema`, `topic`, `queue` and `image` are required, every other key has a documented default, and the schema rejects an unknown key and a missing required one.
3. Render the front tier: an api deployment fixed at 2 pods (Arch v5 slides 33 and 48) with liveness and readiness on `/health`, a scrape annotation for `/metrics`, the service and its port, and the config map and secret reference mounts — and no horizontal autoscaler on it.
4. Render the back tier: a worker deployment of the same image with the Temporal worker role, its own container, its own resources, and a KEDA scaled object on that service's own task queue `rwb-<short>` with a floor of 0 and a ceiling and a backlog threshold held as values (Arch v5 slide 33: "Workers: 0 to many").
5. Render the configuration and the secret references: one config map per service from the values, and one list of key-store references per service (database login, Kafka credentials, Temporal client credentials, object storage for claim-check files) that the deployment resolves at deploy time and never stores as a value.
6. Write the one pipeline template with the same stage list for every service: build, unit and contract tests, the boundary test, the image scan, `helm lint` and `helm template`, the migration lint and the drift gate of RWB-PLT-E1044-CON, then deploy DEV, SIT, UAT and PROD in that order with a gate per environment.
7. Add the blocking checks of NFR-052 and NFR-054: a secret scan over the diff and over the rendered chart, a personal-data scan over code, tests and logs, an approved-dependency check, and a rendered-chart check that fails on any literal secret in `values.yaml`, in a template or in a pipeline log.
8. Version both artefacts, publish the version, and make every service repository pin the chart version and the pipeline template version it builds with; then prove the pair on the canary service.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A values file names another service's schema, topic or queue | The values schema and the derived-name check fail the render and name the key, the value found and the value the short name implies; nothing is deployed | None | AC2 |
| X2 | A template hard-codes a service value, or a values file omits `schema`, `topic` or `queue` | `helm template` fails on the missing required key, and the template lint rule rejects the hard-coded literal; the pipeline stops before the image is pushed | None | AC1, AC2 |
| X3 | A commit or a rendered chart carries a secret | The secret scan blocks the stage, names the file and the line and never prints the value (NFR-052); the build does not reach the image push | None | AC4 |
| X4 | A commit carries personal data in code, tests or logs, or an unapproved dependency | The personal-data scan or the dependency check blocks the stage and names the file and the rule (NFR-054); no exception is granted inside the template | None | AC4 |
| X5 | The migration lint or the drift gate of RWB-PLT-E1044-CON fails | The deploy stage stops after the image scan and before the first environment; the gate's own result is attached to the run and the environment is unchanged | None | AC3 |
| X6 | The worker queue is empty, or the backlog crosses the threshold | KEDA scales the worker to its floor of 0 on an empty queue and adds worker pods as the backlog grows, up to the ceiling; the api deployment stays at its 2 fixed pods throughout | None | AC5 |
| X7 | A service pins a chart version or a pipeline template version that does not exist, or a version with a breaking change is published | A pin to an unknown version fails at render with the version named; a breaking change is published as a new version and the pinned services keep the old one until they move | None | AC6 |
| X8 | A stage is skipped or reordered in a service's copy of the pipeline | The stage-list check compares the service pipeline against the template and fails, naming the missing or moved stage; a service cannot remove the scan, the lint or the gate | None | AC3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the 19-service list, the §R4 naming, the key store, the registry and the RWB-PLT-E1044-CON gate only |
| Negotiable | The chart name, the chart version scheme, the toolchain, the resource sizes, the KEDA thresholds and the promotion approvers are agreed with the solution architect and the platform administrator; the api fixed at 2 pods, the values-file key set, the stage list and the two NFR checks are fixed |
| Valuable | Gives the nine wave 1 services and every later service one chart and one stage list on Day 1, and keeps the secret and personal-data blocks of NFR-052 and NFR-054 out of each team's hands |
| Estimable | One chart with six template groups and one values file per service, one pipeline template with nine stages, one canary; six acceptance criteria |
| Small | Fits one sprint with the chart, the schema, the stage list and the canary; the per-service resource sizes and thresholds are values that the service OPS stories fill in |
| Testable | Every criterion is tested by `helm template` over the 19 values files, by the values schema, by a pipeline run on the canary service and by a scaling test in a cluster |

### 7. Acceptance criteria

```gherkin
Feature: One service pipeline template and one Helm chart for the 19 services

  Background:
    Given the 19-service list and the short names of Template and Rules section R4
    Given one Helm chart, one pipeline template and one values file per service
    Given the key store, the container registry and the CI service of the platform

  Scenario: AC1 One chart renders all 19 services from one values file per service (new, D-RCV-60)
    Given the one chart and the 19 values files, one per short name of section R4
    When helm template renders the chart once per values file
    Then 19 releases render and each one has an api deployment of 2 fixed pods and a worker deployment that KEDA scales on its own Temporal task queue rwb-<short>
    And each release exposes liveness and readiness on /health and a scrape target on /metrics
    And each release carries the schema rwb_<short with _>, the topic rwb.<short>.events.v1 and the task queue rwb-<short> of section R4
    And no per-service chart and no second chart exist

  Scenario: AC2 The chart and values schema reject a values file that names another service's schema, topic or queue (new, D-RCV-60)
    Given a copy of one values file in which schema, topic or queue is changed to another service's value
    When the values schema and the derived-name check run against it
    Then the render fails and names the key, the value found and the value the short name implies
    And a values file with a missing schema, topic or queue fails, because no template supplies a default
    And a template that hard-codes a service name, schema, topic or queue fails the template lint

  Scenario: AC3 The pipeline template runs the same stages for every service (new, D-RCV-60)
    Given the one pipeline template
    When any service repository runs it
    Then the stages run in the same order: build, unit and contract tests, boundary test, image scan, helm lint and helm template, migration lint and drift gate, deploy DEV, deploy SIT, deploy UAT, deploy PROD
    And the migration lint and the drift gate are the stages published by RWB-PLT-E1044-CON and are not optional
    And a service pipeline that skips or reorders a stage fails the stage-list check and names the stage
    And no stage is reachable by a service-specific exception in the template

  Scenario: AC4 Secrets are key-store references and the pipeline blocks a secret or personal data (new, D-RCV-60)
    Given a values file and the chart rendered from it
    When the values file, every template and the pipeline log of the run are inspected
    Then no password, token, key or credential-bearing connection string appears in any of them
    And every credential is a key-store reference that the deployment resolves at deploy time (NFR-052)
    When a commit carries a secret, personal data in code, tests or logs, or an unapproved dependency
    Then the pipeline blocks the stage, names the file and the rule, and prints no secret value (NFR-054)
    And a rendered chart carrying a literal secret fails before the image is pushed

  Scenario: AC5 The api and the worker scale independently (new, D-RCV-60)
    Given a deployed service from the chart
    When the api tier is observed under screen load
    Then it stays at 2 pods and has no horizontal autoscaler of its own
    When the task queue rwb-<short> is empty
    Then the worker scales down to 0 pods
    When the backlog on rwb-<short> grows past the configured threshold
    Then the worker adds pods up to its configured ceiling and the api pod count is unchanged
    And the api and the worker are two deployments that never share a pod

  Scenario: AC6 The chart and the pipeline template are versioned and pinned, and a breaking change is a new version (new, D-RCV-60)
    Given a published chart version and a published pipeline template version
    When a service repository builds and deploys
    Then it uses the exact versions it pins and not the head of either repository
    When a breaking change to the chart or the template is needed
    Then it is published as a new version and the pinned services keep rendering and deploying on their pinned version
    And a pin to a version that does not exist fails at render and names the version

  Scenario: AC7 The section 8 business rules BR1 to BR9 hold for every release the template renders (new, D-RCV-60)
    Given the rules BR1 to BR9 of section 8 and the 19 releases that the chart renders
    When the chart, the template and the pipeline are checked against each rule
    Then one chart and one template serve all 19 services with derived names, no cross-schema value or default, an api of 2 fixed pods, the /health and /metrics paths only, key-store references only, the secret and personal-data block, pinned versions, and the RWB-PLT-E1044-CON migration lint and drift gate run and are not reimplemented per service
    And a values file, a template or a pipeline that breaks one of these rules fails the check and names the rule
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One chart and one pipeline template for all 19 services; a service is a values file, never a fork and never a copy | Arch v5 slide 38 (service template, one Helm chart, golden pipeline); this story |
| BR2 | Every rendered name is derived from the short name: schema `rwb_<short with _>`, topic `rwb.<short>.events.v1`, task queue `rwb-<short>`, REST base `/api/recovery/<short>/v1` | Template and Rules §R4; Arch v5 slide 41 |
| BR3 | A values file may not name another service's schema, topic or queue, and no template defaults one, because a default would let a service write in the wrong schema | Arch v5 slide 29 (one schema and one login per service, no cross-schema grant); ADR-014 |
| BR4 | The api tier is fixed at 2 pods and is never autoscaled; the worker tier is scaled by KEDA on the service's own Temporal task queue, from 0 up | Arch v5 slides 33 and 48 |
| BR5 | Every service exposes `/health` and `/metrics` for the platform, and the chart's probes and scrape target read only those paths | Arch v5 slide 20 |
| BR6 | A secret is a key-store reference and never a value in a values file, a template or a log | NFR-052 |
| BR7 | The pipeline blocks a change that carries a secret, personal data in code, tests or logs, or an unapproved dependency, and the block is part of the template | NFR-054 |
| BR8 | The chart and the template are versioned; a service pins both, and a breaking change raises a new version instead of changing a pinned one | This story; Arch v5 slide 38 (built once, then reused by every wave) |
| BR9 | The migration lint and the drift gate are the RWB-PLT-E1044-CON stages, run by the template and never reimplemented per service | Template and Rules §R5.5 DP-15; ADR-021 |

### 9. State transitions

None. This story changes no business state. The chart and the pipeline template move Draft, Published and Superseded as versions in their repositories, and that is a release state of an artefact and not a state of a case. A service release moves through the four environments as a deployment record, which is the pipeline's own state and not the Workbench case lifecycle.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns this story, the chart repository and the pipeline template repository; publishes a chart version and a template version, and changes neither a pinned version nor a service's values file |
| Platform administrator | Approves the chart name and version scheme, the registry and image naming, the key-store reference convention and the resource defaults |
| Solution architect | Approves the rendered shape against Arch v5 slides 20, 33, 38 and the §R4 naming, and the values-file key set |
| Release role | Approves the promotion gate of each environment from DEV to SIT to UAT to PROD; holds no write right on the chart or the template |
| RW-PLATADM | Reads the deployed releases, the chart versions and the pipeline runs for operations and break-glass support; holds no write right on the versioned artefacts |
| RW-SECADM | Reads the secret-scan, personal-data-scan and dependency-scan results of every run; writes nothing in the chart or the template |

The platform stories carry no service short name, schema, topic or task queue of their own, because the §R4 table has 19 service rows and no platform row: this story renders the 19 services and owns none of their names. Where a chart name, a registry name, an image name or a release name would sit, it is Not specified in the source documents (GAP-1424; ASM-2492).

### 11. Data

**The values-file contract.** One values file per service, held in the chart repository and named after the service short name.

| Key | What it sets | Where the value comes from | BR Field ID |
|---|---|---|---|
| `name` | The release and deployment name of the service | The service name `rwb-<short>` of §R4 and Arch v5 slide 41 | BR2 |
| `short` | The short name every other name is derived from | Template and Rules §R4 | BR2 |
| `schema` | The service's own schema, `rwb_<short with _>` | Template and Rules §R4; Arch v5 slides 29 and 41 | BR3 |
| `topic` | The service's own topic, `rwb.<short>.events.v1` | Template and Rules §R4; Arch v5 slide 41 | BR2 |
| `queue` | The service's own Temporal task queue, `rwb-<short>` | Template and Rules §R4; Arch v5 slide 41 | BR2 |
| `image` | Repository, tag and digest of the service image | Not specified in the source documents (GAP-1424; ASM-2492) | Not specified in the source documents (DOR-RWB-PLT-N004-OPS-7) |
| `api.replicas` | The fixed api pod count, 2 | Arch v5 slides 33 and 48 | BR4 |
| `api.resources`, `worker.resources` | Requests and limits of each tier | Not specified in the source documents (GAP-1424; ASM-2492) | Not specified in the source documents (DOR-RWB-PLT-N004-OPS-7) |
| `keda.min`, `keda.max`, `keda.threshold` | The worker floor (0), the ceiling and the backlog threshold on `rwb-<short>` | Floor 0 from Arch v5 slide 33; ceiling and threshold Not specified in the source documents (GAP-1424; ASM-2492) | BR4 |
| `probes.path`, `probes.port` | Liveness and readiness on `/health`, scrape on `/metrics` | Paths from Arch v5 slide 20; ports Not specified in the source documents (GAP-1424; ASM-2492) | BR5 |
| `secretRefs` | The key-store references the deployment resolves | NFR-052; the reference convention Not specified in the source documents (GAP-1424; ASM-2493) | BR6 |

**What a values file never carries**

| Not in a values file | Why | Where it lives instead | BR Field ID |
|---|---|---|---|
| A password, token, key or credential-bearing connection string | NFR-052: secrets are held in the key store and never in code or configuration files | A key-store reference resolved at deploy time | BR6 |
| Another service's schema, topic or queue | A cross-service name would let one service write in another's schema, which the grants refuse (Arch v5 slide 29) | The check of AC2 fails the render | BR3 |
| A business parameter, a reference-data row or a decision value | Template and Rules §R7.2 s17: no business value in code or configuration | The owning service's parameter and reference-data contract | Not specified in the source documents (DOR-RWB-PLT-N004-OPS-7) |

**Secret references the chart declares.** Names only; no value is ever held in the chart.

| Reference | What it is for | BR Field ID |
|---|---|---|
| Database login of the service | Connects only to the service's own login in the ACE database (Arch v5 slide 29) | BR6 |
| Kafka client credentials | Publishes to `rwb.<short>.events.v1` and reads only the topics the service subscribes to | BR6 |
| Temporal client credentials | Polls `rwb-<short>` in the namespace `rwb-recovery` | BR6 |
| Object storage credential | Reads and writes claim-check files for large payloads (Arch v5 slide 20 tags) | BR6 |
| Key-store access reference | Lets the pod resolve the other references at run time | BR6 |

The chart and the values files hold names, references, counts and sizes only. They hold no business value and no personal data, in line with the guardrail of §R7.2 s17 and NFR-052.

### 12. Contract

This story provides no REST operation, publishes and consumes no business event, runs no workflow and no Schedule, and owns no table and no schema. Its deliverable is one Helm chart and one pipeline template, both held as code and both versioned.

#### 12.1 REST operations provided

None. The chart renders the `/health` and `/metrics` endpoints that every service already owes the platform (Arch v5 slide 20); those endpoints belong to each service and are not a contract of this story.

#### 12.2 REST operations consumed

None. The pipeline calls the platform services it deploys with, and it consumes the migration lint and drift gate stages of RWB-PLT-E1044-CON; neither is a REST contract of this story.

#### 12.3 Events published

None. The chart creates no topic and publishes no event; the topics it names in a values file are owned by RWB-PLT-EVT (RWB-PLT-N002-INF) and by each service.

#### 12.4 Events consumed

None. The pipeline subscribes to no business event.

#### 12.5 Workflows and activities

None. The chart deploys the Temporal worker container that each service's own workflows need, on the service's own task queue `rwb-<short>`; it defines no workflow and no activity.

#### 12.6 Schedules

None. The pipeline template runs on a commit and on a promotion, not on a Temporal Schedule.

#### 12.7 Tables owned

None. The chart creates no table, no schema and no login; the 19 schemas and logins belong to RWB-PLT-DB and to each service's DB story (ADR-014, ADR-021).

#### 12.8 Contract fakes

None. This story publishes no service contract and therefore needs no contract fake, and it adds no fake for another service's contract. The values schema, the derived-name check and `helm template` are tested against the chart itself.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None | The chart renders each service's own api tier and its `/health` and `/metrics` endpoints; this story provides no REST operation of its own |
| Kafka | None | The chart names each service's topic and creates no topic and no ACL |
| Temporal | None | The chart deploys each service's worker on its own queue `rwb-<short>`; it defines no workflow, activity or Schedule |
| File | One | One Helm chart and one pipeline template, both held as code and versioned; the chart has no schema, topic, queue or REST surface of its own |

### 13. Solution plan

**Artefacts.** Paths are relative to the platform chart repository, and the section markers are the design of this story.

| Path | Artefact | What it holds |
|---|---|---|
| `chart/Chart.yaml` | The one chart | The chart name (Not specified in the source documents (GAP-1424; ASM-2492)), the version and the app version |
| `chart/values.schema.json` | The values schema | The required keys of section 11, the types, the closed key set and the derived-name rule of AC2 |
| `chart/values.yaml` | The documented defaults | Every default except the six required keys, so that no default can name a service |
| `chart/values/<short>.yaml` | One values file per service | The 19 files, one per short name of §R4 |
| `chart/templates/api-deployment.yaml` | The front tier | 2 fixed pods, `/health` liveness and readiness, `/metrics` scrape, the service port, no autoscaler |
| `chart/templates/worker-deployment.yaml` | The back tier | The same image in the worker role, its own resources, its own container |
| `chart/templates/keda-scaledobject.yaml` | The worker scaler | KEDA on the queue `rwb-<short>`, the floor, the ceiling and the threshold as values |
| `chart/templates/service.yaml` | The service | The cluster service and its port of the api tier |
| `chart/templates/configmap.yaml` | The configuration | The non-secret configuration of the service, rendered from the values |
| `chart/templates/secretrefs.yaml` | The secret references | The key-store references of section 11, resolved at deploy time and never carrying a value |
| `pipeline/template.yml` | The one pipeline template | The nine stages of AC3 in order, the scans of AC4, the gate per environment, and the version pin |
| `pipeline/checks/derived-names.yml` | The derived-name check | Compares `schema`, `topic` and `queue` against the short name and fails the render |
| `pipeline/checks/stage-list.yml` | The stage-list check | Compares a service pipeline against the template and names a missing or moved stage |
| `pipeline/checks/secrets.yml` | The secret and personal-data scans | The NFR-052 and NFR-054 blocks over the diff, the rendered chart and the log |
| `canary/` | The canary service | The one service used to prove the pair end to end before wave 1 starts |

**Pattern application**

| DP | Pattern | Where it shows in this story |
|---|---|---|
| None | None of the DP table applies: this story introduces no legacy table, no legacy login, no legacy topic and no legacy call (`patterns` is empty) | — |

The chart renders the names that the DP-15 stories migrate into (`rwb_<name>` per service), it carries the outbox and inbox of DP-09 as library tables that each service's own schema story creates, and it calls the RWB-PLT-E1044-CON gate of DP-15 as a stage; the patterns themselves stay with the service and platform CON stories and none is applied here.

**Build steps**

1. Create the chart skeleton with `Chart.yaml`, the closed `values.schema.json` and a `values.yaml` that names no service.
2. Write the api deployment: 2 fixed pods, `/health` liveness and readiness, `/metrics` scrape, the service port, and no autoscaler on the front tier.
3. Write the worker deployment and the KEDA scaled object on the service's own queue `rwb-<short>`, with the floor at 0 and the ceiling and threshold as values.
4. Write the config map and the secret references, so that every credential in a rendered release is a key-store reference.
5. Write the derived-name check and the template lint rule, and make the render fail on a missing or foreign schema, topic or queue.
6. Write the pipeline template: build, unit and contract tests, boundary test, image scan, `helm lint` and `helm template`, the migration lint and drift gate of RWB-PLT-E1044-CON, then DEV, SIT, UAT and PROD with a gate per environment.
7. Add the secret scan, the personal-data scan and the approved-dependency check, and prove that a seeded secret and a seeded personal-data field each block a run without printing the value.
8. Publish the chart version and the template version, add the pin to a service repository, and prove the pair on the canary through all four environments.

**Done when.** The one chart renders all 19 services from the 19 values files, with the api fixed at 2 pods and the worker scaled by KEDA on its own queue, `/health` and `/metrics` reachable, and the §R4 schema, topic and queue in every release; the values schema rejects a foreign or missing schema, topic or queue; the one pipeline template passes on the canary through DEV, SIT, UAT and PROD with the same stage list and with the RWB-PLT-E1044-CON migration lint and drift gate in place; the secret and personal-data checks block a seeded change; the worker scales from 0 while the api stays at 2; and the chart and the template are pinned by version.

The chart name, the chart repository and the registry and image naming, the resource sizes of both tiers, the KEDA ceiling and threshold per service, the toolchain of the pipeline, the promotion gates and their approvers, and the chart version scheme are Not specified in the source documents (GAP-1424; ASM-2492 and ASM-2493).

### 14. Validation and messages

| Message ID | When | Message |
|---|---|---|
| MSG-P4-002 | A role without the right tries to publish a chart version, change a pinned version or approve a promotion gate | You cannot {action} here. Your role does not include it. |

The template invents no message ID and shows no message to a user. A failed stage reports its own rule and file in the pipeline result, and a deployment refusal to a person carries MSG-P4-002, whose wording already exists in the message catalogue and is quoted and not rewritten here. No pipeline log carries a secret value or a personal data field (NFR-052, NFR-054).

### 15. Screens and states

None. This story adds no Workbench screen and no screen state. The operator surfaces are the pipeline run result and the deployment view of the four environments, which are read-only for a service team and are changed only by a new version of the chart or the template.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-N004-OPS-01 | AC1 | Component | `helm template` renders the chart 19 times, once per values file of §R4: every release has an api deployment of 2 pods, a worker deployment with a KEDA scaled object on `rwb-<short>`, `/health` and `/metrics`, and the schema, topic and queue of §R4; no second chart exists |
| TC-PLT-N004-OPS-02 | AC2 | Unit | A values file with a foreign `schema`, `topic` or `queue` fails the render naming key, found value and implied value; a values file with a missing key fails; a template with a hard-coded name fails the lint |
| TC-PLT-N004-OPS-03 | AC3 | Component | The template run on the canary shows the same ten stages in order, including the RWB-PLT-E1044-CON migration lint and drift gate; a service pipeline with a skipped, moved or removed stage fails the stage-list check |
| TC-PLT-N004-OPS-04 | AC4 | NFR | A seeded secret in a values file, in a template and in a commit each block the stage without printing the value; a seeded personal data field in code, a test and a log blocks the stage; an unapproved dependency blocks the stage; a rendered release carries key-store references only |
| TC-PLT-N004-OPS-05 | AC5 | Integration | In a cluster, the api stays at 2 pods under screen load with no autoscaler, the worker falls to 0 on an empty `rwb-<short>` queue and grows to its ceiling as the backlog rises, and the api pod count does not change |
| TC-PLT-N004-OPS-06 | AC6 | End to end | A service pinned to a chart version and a template version renders and deploys on those versions and not on the head; a published breaking version leaves the pinned service unchanged; a pin to an unknown version fails naming the version |
| TC-PLT-N004-OPS-07 | AC7 | Component | `helm template` and the template lint run over the 19 rendered releases and the one pipeline template, and check each rule BR1 to BR9 of section 8: one chart and no fork, names derived from the short name, no foreign or default schema, topic or queue, api fixed at 2 pods with no autoscaler, /health and /metrics only, key-store references only, the secret and personal-data block, pinned versions, and the RWB-PLT-E1044-CON stages present and not reimplemented; a breach of any rule fails the check and names the rule |

### 17. Guardrails

- No business value in code or configuration: a values file holds names, references, counts and sizes only, and every business parameter stays with its owning service's contract (Template and Rules §R7.2 s17).
- No secret in a values file, a template or a pipeline log: every credential is a key-store reference resolved at deploy time (NFR-052).
- No personal data in a values file, in a test fixture or in a pipeline log, and the pipeline blocks a change that carries one (NFR-054).
- No cross-service name: a values file may not name another service's schema, topic or queue, and no template supplies such a name as a default (Arch v5 slide 29).
- No personal data in events, workflow inputs or logs: the chart only mounts configuration, and the event payloads stay the owning service's.
- ACE data only through the owner's contract or the `v_ace_*` views: the chart creates no view and no grant, and the service login of each values file is the one RWB-PLT-DB creates.
- No unapproved dependency: a new library or image dependency is a reviewed change, and the pipeline blocks an unapproved one (NFR-054).
- One chart and one template: a fork, a per-service chart or a per-service stage list is refused by the checks and not by convention (Arch v5 slide 38).

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| NFR-052 | Secrets are held in the key store and never in code, configuration files or prompts | The secret references of `chart/templates/secretrefs.yaml`, the closed values schema and the secret scan of the template | TC-PLT-N004-OPS-04 |
| NFR-054 | The build pipeline blocks a change carrying a secret, personal data in code, tests or logs, or an unapproved dependency | The secret scan, the personal-data scan and the approved-dependency check as blocking stages | TC-PLT-N004-OPS-04 |
| Arch v5 slides 20 and 41 | Every service exposes `/health` and `/metrics`, keeps its own schema, topic and task queue, and carries outbox, inbox and a Temporal worker | The api and worker deployments, the derived names of the values file and the §R4 names in every release | TC-PLT-N004-OPS-01 |
| Arch v5 slides 33 and 48 | The api tier is 2 fixed pods and the worker tier scales 0 to many by KEDA on its own queue | The fixed api deployment and the KEDA scaled object on `rwb-<short>` | TC-PLT-N004-OPS-05 |
| Arch v5 slide 38 | Wave 0 builds the service template, one Helm chart and the golden pipeline once | The one chart, the one pipeline template and the version pin | TC-PLT-N004-OPS-01, TC-PLT-N004-OPS-06 |
| RWB-PLT-E1044-CON | The migration lint and the drift gate of per-service Flyway migrations | The two gate stages of the pipeline template | TC-PLT-N004-OPS-03 |

### 19. Out of scope

- The service code, the Spring Boot skeleton, the outbox relay, the inbox, the codec and the OpenTelemetry agent: RWB-PLT-TPL's template stories and RWB-PLT-LIB own them; this story only deploys what they produce.
- The outbox, inbox, idempotency and decision-record tables themselves: RWB-PLT-TE006-CON and each service's DB story create them, and the chart creates no table (ownership.json tables `outbox_event`, `processed_event`, `idempotency_key`).
- The 19 schemas and logins: RWB-PLT-DB and the per-service DB stories (ADR-014, ADR-021).
- The Kafka topics, the retry and `.dlt` topics and the ACLs: RWB-PLT-N002-INF; the chart names the topic and creates none.
- The migration lint and the drift gate they run: RWB-PLT-E1044-CON owns both as stages; this story calls them.
- The repository layout, the branch rules and the review route of a service repository: RWB-PLT-NF01-OPS owns the repository and pipeline baseline, and this story only supplies the template it applies.
- The environments themselves, the cluster and its quota: RWB-PLT-NF03-OPS; the key store and the configuration convention: RWB-PLT-NF04-OPS.
- The dashboards, alerts and SLOs of a deployed service: RWB-PLT-N005-OPS and each service's own OPS story.
- The per-service resource sizes, KEDA ceilings and thresholds: values that each service OPS story fills in, and the defaults are the gap GAP-1424 for the solution architect to close before the chart is Published.
