# RWB-PLT-N005-OPS Platform dashboards and alerts baseline

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-N005-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-OBS |
| Wave | 0 |
| Business epic | NEW |
| Release | None (new story) |
| Legacy key | N005 |
| Legacy disposition | New |
| Build status | Not started |
| Patterns applied | None |
| Parallel lane | L-PLT-OBS-A |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: new platform story (N005, platform observability). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-PLT-N005-OPS). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform engineer**, I want **one versioned observability baseline — the golden-signal dashboard set, the alert rules, the SLOs, the trace and metric conventions and the retention values — deployed once and inherited by every service and platform epic**, so that **no wave 0 or wave 1 capability reaches SIT without the panels and alerts an operator needs, and no service team invents its own**.

### 2. Business rationale

Observability is a platform piece, not a service feature. Arch v5 slide 8 places OpenTelemetry in the shared platform row of the C4 diagram, next to Kafka, Temporal and the database; slide 35 puts one trace across services in the audit and monitoring layer, with PII logging to SOC through ACE Common; slide 49 records OpenTelemetry and W3C Trace Context as the standard that gives one trace across services, events and workflows (baseline Req 10); slide 22 gives every event topic a retry ladder and a `.dlt` with an alert; slide 44 gives the platform the stuck-workflow scan JOB-21 (a visibility query plus an alert) and the smoke workflow JOB-22, and requires run visibility for the event-started workflows and the Schedules. ADR-023 records observability per service. NFR-064 asks for logs, traces and metrics across the workflow, the decision service and the agents; NFR-065 asks for measures per decision from the decision log; NFR-066 asks for agent acceptance, override rate, latency and cost; NFR-067 asks for a run book, monitoring and an alert to the operations channel for every scheduled job; NFR-068 asks that a failing interface, job or agent raise an alert to a named owner within its target, and its target is 15 minutes (status Proposed, DL11).

Without a shared baseline the same work is repeated 76 times. There are 19 services and 4 environments (DEV, SIT, UAT and production), so a per-service, per-environment dashboard habit produces 76 bespoke dashboards, 76 rule sets and 76 private opinions about what "healthy" means. The panels then differ between services, the alerts route to whoever wrote them, and the first SIT of wave 0 or wave 1 opens with an operator who cannot see whether a case actually moved. One baseline deployed from one repository gives every service the same four golden signals, the same trace convention across REST, Kafka and Temporal, the same alert route to the owner role and the same retention values, and leaves the service teams free to add only the business panels that are theirs.

The baseline is also the only place where the cross-cutting signals exist. Consumer lag and `.dlt` depth, Temporal Schedule and workflow health, outbox relay lag and per-schema connection pool use are not one service's business; they are the shared failure modes of the platform. No service story can see them alone, and the 15-minute target of NFR-068 cannot be met by a route that each story invents. This story is a Wave 0 Day-1 enabler: it has no build dependency and every service and platform story from wave 0 onwards inherits it.

### 3. Preconditions

- The platform epics RWB-PLT-TPL (service template and repositories), RWB-PLT-LIB (shared libraries), RWB-PLT-EVT (Kafka event platform) and RWB-PLT-WF (Temporal workflow platform) exist in wave 0, because the baseline instruments what they provide: the template's OpenTelemetry agent, the outbox relay, the event topics with retry and `.dlt`, and the Temporal namespace with its Schedules.
- The shared OpenTelemetry collector, the shared Log Analytics workspace and the secret store are provisioned as platform resources, and the collector is reachable from every service pod.
- The 19-service list and the short names of Template and Rules §R4 are fixed, so that `service` identity, the per-service panel set and the per-schema connection pool panel have a stable list to render from.
- The message catalogue exists with its MSG IDs, because every alert rule names the message ID it carries and this story invents none.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).
- The names, targets and values of the baseline are Not specified in the source documents (GAP-1418; ASM-2481).

### 4. Flow

1. Publish the baseline repository: dashboards, alert rules and SLOs as code, one versioned commit per change, deployed by the pipeline and never edited in the workspace.
2. Fix the resource attributes and the collector configuration once: receivers, processors (batch, scrubbing, sampling), exporters, the workspace connection and the retention values, so that every service exports the same shape.
3. Fix the trace propagation through the three call types: REST carries `traceparent` (W3C Trace Context), Kafka carries the CloudEvents headers plus `traceparent` (Arch v5 slide 22), and Temporal carries the context propagator so that an activity stays in the parent trace.
4. Render the golden-signal panels per service from one template: request rate, error rate, duration and saturation for each of the 19 services, driven by the resource attribute of the service and not by a hand-made copy.
5. Add the platform panels: consumer lag and `.dlt` depth per topic, Temporal Schedule and workflow health (including a stuck workflow, the JOB-21 visibility query), outbox relay lag per service, and connection pool use per schema.
6. Write the alert rules: one rule set as code, each rule routed to the owner role of the failing piece, each rule carrying an existing message ID, and the route tested against the 15-minute target of NFR-068.
7. Set the sampling and the scrubbing: error-biased sampling so that no error span is lost, and a scrubbing processor that removes personal data before export, with the PII path to SOC left to ACE Common (Arch v5 slides 8 and 35).
8. Prove the baseline with the SIT canary, which calls the platform smoke endpoint `POST /admin/workflows/smoke` and checks one trace across REST and Temporal, a populated panel set and a routed alert; then hand the baseline to each service OPS story, which adds only its own business panels.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The collector does not answer | The exporters keep their buffer, the panels show a gap and the platform canary fails; the alert rule fires to the platform owner role and the operator restores the collector | MSG-P2-004 | AC7 |
| X2 | The sampling policy hides a failure | Error-biased sampling keeps every error span and every error log, so a failing call stays visible in the trace and on the panel; the sampling rate is a value and is raised for the failure window | None | AC6 |
| X3 | A service ships without the baseline | The pipeline baseline check fails the build and names the service and the missing artefact, so the deployment does not reach SIT | None | AC2 |
| X4 | A personal data field reaches telemetry | The scrubbing processor drops the field before export, the pipeline test fails on the known test field and the incident goes through the ACE Common PII path to SOC | None | AC6 |
| X5 | The workspace quota or the ingestion cap is reached | The sampling tightens to the value fixed for the cap, a quota alert fires to the platform owner role, and no signal is dropped without that alert | None | AC6 |
| X6 | An alert rule drifts or falls silent | The pipeline compares the live rules against the baseline and restores them; a hand edit in the workspace is refused, and the difference is reported with the rule name | MSG-P4-002 | AC4 |
| X7 | The SIT canary fails | The baseline is not accepted for SIT and the hand-over to the service OPS stories is blocked; the canary failure is alerted with the canary job name and the run book | MSG-P2-004 | AC7 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the 19-service list, the message catalogue and the platform resources only |
| Negotiable | The dashboard names, the panel set per service, the metric and span names, the thresholds, the sampling and the retention values are agreed with the solution architect and the platform administrator; the three call types, the trace convention and the 15-minute target are fixed |
| Valuable | Gives every service and platform story from wave 0 onwards the panels, the alerts and the SLOs an operator needs on Day 1, and removes 76 bespoke dashboards |
| Estimable | One baseline repository with six artefact groups, one collector configuration and one SIT canary; seven acceptance criteria |
| Small | Fits one sprint with the rendering, the routing and the canary; the per-service business panels stay with the service OPS stories |
| Testable | Every criterion is tested against the deployed dashboards, rules and traces in DEV, SIT and UAT, and against the canary in SIT |

### 7. Acceptance criteria

```gherkin
Feature: Platform observability baseline inherited by the 19 services and the platform epics

  Background:
    Given the shared OpenTelemetry collector, the shared Log Analytics workspace and the secret store of the platform
    Given the 19-service list and the short names of Template and Rules §R4
    Given the message catalogue that gives every alert its message ID

  Scenario: AC1 The baseline is versioned as code and deploys to DEV, SIT and UAT (new, D-RCV-60)
    Given the baseline repository with its dashboards, alert rules and SLOs as code
    When the baseline pipeline runs against DEV, SIT and UAT
    Then the same dashboards, alert rules and SLOs are deployed to each of the three environments
    And no dashboard, rule or SLO is created by hand in any workspace
    When the pipeline runs a second time with no change
    Then no artefact is created, changed or deleted

  Scenario: AC2 Every service of the 19-service list gets the golden-signal dashboard set (new, D-RCV-60)
    Given the dashboard template of the baseline
    When the template is rendered for each service of the 19-service list
    Then every service has the same four golden-signal panel groups
    And each panel reads that service's own telemetry through its resource attribute
    When one rendered dashboard is missing a panel
    Then the baseline check fails, names the service and the panel, and stops the deployment

  Scenario: AC3 One trace crosses REST, Kafka and Temporal (new, D-RCV-60)
    Given a case action that is one REST call, one Kafka event and one workflow activity
    When the action is executed in SIT
    Then one trace carries all three hops under the same trace identifier
    And the REST hop carries traceparent and the Kafka hop carries the CloudEvents headers plus traceparent
    And the spans show the call depth of each hop, so that a call depth above one is visible
    And no REST hop exceeds the 2 s budget of one hop

  Scenario: AC4 Alert rules route to owner roles, carry a message ID and meet the 15-minute target (new, D-RCV-60)
    Given a failing interface, job or agent in SIT
    When its alert rule fires
    Then the alert reaches the owner role of the failing piece within 15 minutes
    And the alert carries an existing message ID from the message catalogue
    And no alert is addressed to a named person
    When a rule names a role with no route
    Then the baseline check fails and names the rule

  Scenario: AC5 The platform panels cover consumer lag and .dlt, Temporal health, the outbox relay and the connection pools (new, D-RCV-60)
    Given the platform panels of the baseline
    When they are reviewed against the platform pieces
    Then consumer lag and .dlt depth are shown per topic
    Then Temporal Schedule and workflow health is shown per Schedule and per workflow type
    Then outbox relay lag is shown per service
    Then connection pool use is shown per schema
    And a platform piece with no panel fails the baseline check

  Scenario: AC6 Telemetry carries no personal data and sampling, retention and thresholds are values (new, D-RCV-60)
    Given a telemetry stream from a service in SIT
    When spans, metrics, logs and alert payloads are inspected
    Then none carries a personal data field, a token or a secret
    And the scrubbing processor removes a known test field before export
    When the sampling rate, a retention period or an alert threshold is changed
    Then the change is a value in the baseline repository and not a code change
    And error-biased sampling keeps every error span

  Scenario: AC7 The baseline is proven in SIT by the canary and inherited by the service OPS stories (new, D-RCV-60)
    Given the SIT canary of the baseline
    When it runs and calls the platform smoke endpoint POST /admin/workflows/smoke
    Then it sees one trace across REST and Temporal, the golden-signal panels with data and the alert route of the owner role
    And a canary that sees no trace or an empty panel fails the SIT acceptance
    When a service OPS story starts
    Then it inherits this baseline and adds only its own business panels
    And it creates no dashboard, rule or SLO of its own
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Observability per service: every service emits its own traces, metrics and logs, and the platform provides the conventions and the shared pieces, not one central agent inside a service | ADR-023; Arch v5 slide 20 |
| BR2 | One trace across the three call types: REST carries `traceparent`, Kafka carries the CloudEvents headers plus `traceparent`, and Temporal propagates the context, so a case action is one trace | Arch v5 slides 22, 35, 46 and 49 |
| BR3 | No personal data in logs, metrics, spans or alert payloads; the scrubbing processor runs before export and the PII path to SOC stays with ACE Common | Arch v5 slides 8 and 35; Template and Rules §R7.2 s17 |
| BR4 | Alerts are addressed to owner roles and never to a person, and each alert carries an existing message ID | NFR-068; Template and Rules §R1 U3 |
| BR5 | Every event topic has a retry ladder and a `.dlt` with an alert, and the `.dlt` depth is visible on a platform panel | Arch v5 slides 11 and 22 |
| BR6 | A Temporal Schedule exposes its overlap policy and its catch-up window, and a workflow that is stuck or silent raises an alert through the JOB-21 visibility query | Arch v5 slide 44; Batch and Scheduling Design v5 JOB-21 |
| BR7 | Retention, sampling and alert thresholds are values held in the baseline repository and are changed without a code release | Business Requirements Program v5 §7 principle 1; NFR-068 |
| BR8 | Dashboards, alert rules and SLOs are code, reviewed and versioned; the workspace is never edited by hand and the next pipeline run corrects any manual change | NFR-067; this story |

### 9. State transitions

None. This story changes no business state; the baseline itself moves Draft, In review, Published and Superseded as code in its repository, and that is a review state of an artefact, not a state of a case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns this story, the baseline repository, the pipeline and the SIT canary; changes the dashboards, the rules, the SLOs and the collector configuration through the repository only |
| Platform administrator | Approves the collector configuration, the workspace layout, the retention values and every alert route; owns the 15-minute target of NFR-068 |
| Solution architect | Approves the trace convention, the golden-signal panel set, the SLO set and the metric and span names |
| On-call operator | Reads the dashboards, the alert list and the SLO view; acknowledges an alert and follows the run book, and never edits a rule |
| RW-PLATADM | Reads the platform dashboards, the alert list and the SLO view for operations and break-glass support; holds no write right on the baseline |
| RW-AUDIT | Reads the audit-relevant panels and the retention values; writes nothing |
| RW-SECADM | Reads the scrubbing, sampling and access panels and the alert routes; writes nothing in the baseline |

The platform observability stories carry no service short name, schema, topic or task queue in the §R4 service table, because that table has 19 service rows and no platform row. Where a service identity, a schema, a topic or a task queue would be named for this story, it is Not specified in the source documents (GAP-1418; ASM-2481); the baseline runs in the `rwb-recovery` namespace with the platform identity.

### 11. Data

**Telemetry series**

| Signal | What the baseline carries | Source |
|---|---|---|
| Traces | One trace across REST, Kafka and Temporal, one span per hop, the call depth of each hop, and the canary trace that proves the whole path | Arch v5 slides 35, 46 and 49; NFR-064 |
| Metrics | Request rate, error rate, duration and saturation per service API (the four golden signals); consumer lag and `.dlt` depth per topic; Temporal Schedule and workflow health; outbox relay lag per service; connection pool use per schema | Arch v5 slides 20, 22 and 44; NFR-064 |
| Logs | Structured logs with the same resource attributes, scrubbed before export, into the shared Log Analytics workspace | Arch v5 slides 8 and 35 |
| SLOs | One objective, one window and one error budget per service API and per platform piece, held as values | NFR-068; ADR-023 |

**Dashboard and rule inventory**

| Artefact | Scope | Count |
|---|---|---|
| Golden-signal dashboard set | One template rendered for each service of the 19-service list | 19 services × 4 environments = 76 deployments from one template |
| Platform panel group · events | Consumer lag and `.dlt` depth per topic, with the retry ladder visible | The topic inventory of RWB-PLT-N002-INF |
| Platform panel group · workflow | Temporal Schedule and workflow health, including the stuck workflow of JOB-21 | Arch v5 slide 44 |
| Platform panel group · outbox | Outbox relay lag and age per service, which is JOB-11 | Arch v5 slides 20 and 44 |
| Platform panel group · database | Connection pool use and wait per schema | Arch v5 slide 8 |
| Alert rules | One rule set as code, routed to the owner role of the piece and carrying a message ID | Every rule of the baseline |
| SLO set | One SLO per service API and per platform piece | 19 service APIs and the platform pieces |

**Resource attributes**

| Attribute | Value | Source |
|---|---|---|
| Service name | The service's own short name from the 19-service list | Template and Rules §R4 |
| Namespace | `rwb-recovery` | Arch v5 slide 8 |
| Environment | DEV, SIT, UAT and production (4 environments) | This story |
| Service version | The deployed build version, so that a panel can be split by release | Arch v5 slide 20 |
| The attribute keys beyond these four | Not specified in the source documents (GAP-1418; ASM-2481) | — |

**Retention values**

| Signal | Retention | Where the value is held |
|---|---|---|
| Traces | Not specified in the source documents (GAP-1418; ASM-2481) | A value in the baseline repository, applied by the collector |
| Metrics | Not specified in the source documents (GAP-1418; ASM-2481) | A value in the baseline repository, applied to the workspace |
| Logs | Not specified in the source documents (GAP-1418; ASM-2481) | A value in the baseline repository, applied to the workspace |

The baseline holds series and artefact definitions, SLO targets, resource attributes and retention values only. It holds no business value and no personal data: business data stays in the owning service's schema, and personal data stays in the owning service, masked, with the PII path to SOC through ACE Common (Arch v5 slide 35). The sampling rate, the alert thresholds and the alert windows are values of the same kind and are Not specified in the source documents (GAP-1418; ASM-2481).

### 12. Contract

This story provides no REST operation, publishes and consumes no business event, runs no workflow and no Schedule, and owns no table and no schema. It is a platform baseline only.

#### 12.1 REST operations provided

None. The baseline exposes no REST surface of its own; the operator reads the dashboards, the alert list and the SLO view of the platform.

#### 12.2 REST operations consumed

None provided or consumed by the baseline as a service contract. The SIT canary calls the platform smoke endpoint `POST /admin/workflows/smoke`, whose owner is PLT; its path prefix and its payload are Not specified in the source documents (GAP-1418; ASM-2481).

#### 12.3 Events published

None. The baseline publishes no business event; the alerts leave the platform through the alert route and not through a Kafka topic.

#### 12.4 Events consumed

None. The baseline receives telemetry by OTLP push from the services and does not subscribe to a business event.

#### 12.5 Workflows and activities

None. The stuck-workflow scan JOB-21 and the smoke workflow JOB-22 belong to the platform workflow epic; this story only consumes their health signals on a panel.

#### 12.6 Schedules

None. No Temporal Schedule is created by this story; the canary is a pipeline step and not a Schedule.

#### 12.7 Tables owned

None. The baseline owns no table and no schema; the dashboards, the rules and the SLOs live as code in the baseline repository, and the telemetry lives in the shared Log Analytics workspace.

#### 12.8 Contract fakes

Two fakes in the pipeline: a synthetic telemetry generator that emits traces, metrics and logs with the resource attributes of every one of the 19 services, and a stub collector that accepts the OTLP push and records what it received. They let the dashboard rendering, the scrubbing test and the alert route be tested with no live service.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None | The baseline provides no REST operation; the SIT canary calls the platform smoke endpoint `POST /admin/workflows/smoke` owned by PLT |
| Kafka | None | The baseline consumes no business event and publishes none; the event panels read the topic metrics and the `.dlt` depth |
| Temporal | None | The baseline runs no workflow, no activity and no Schedule; it reads the health signals of the platform Schedules |
| File | None | No file is read or written by the baseline |

The baseline receives an OTLP push from the services, which is a telemetry export and not a service contract: it has no API version, no OpenAPI document and no consumer outside the platform. The push endpoint, its authentication and its payload shape are Not specified in the source documents (GAP-1418; ASM-2481).

### 13. Solution plan

**Artefacts.** All paths are relative to the baseline repository.

| Path | Artefact | What it holds |
|---|---|---|
| `observability/baseline/` | The baseline root | The version, the environment list and the include list of the artefact groups below |
| `observability/baseline/dashboards/` | Dashboards as code | The golden-signal template for the 19 services and the four platform panel groups |
| `observability/baseline/alerts/` | Alert rules as code | The rule set, its windows and thresholds as values, the owner role of each rule and the message ID it carries |
| `observability/baseline/slos/` | SLOs as code | The objective, the window and the error budget per service API and per platform piece |
| `observability/baseline/otel-collector/` | Collector configuration | Receivers, the batch and scrubbing and sampling processors, the exporters, the resource attributes and the retention values |
| `observability/baseline/runbooks/README` | Run book index | One line per alert: what it means, the owner role, the first checks and the run book it points to |
| `observability/baseline/canary/` | The SIT canary | The pipeline step that emits a known trace, calls `POST /admin/workflows/smoke` and asserts the trace, the panels and the alert route |

**Pattern application.** None of the DP table applies to this story (`patterns` is empty): it introduces no legacy table, no legacy login, no legacy topic name and no legacy call. The trace and event conventions it fixes are used by the stories that do apply DP-09 (outbox and inbox with CloudEvents) and DP-11 (one REST hop with a 2 s timeout), and the retry and `.dlt` alert it renders is the one the DP-09 stories produce.

**Build steps**

1. Create the baseline root and the environment list, and wire the pipeline that applies it to DEV, SIT and UAT from the same files.
2. Write the resource attributes and the collector configuration: receivers, batch, scrubbing, error-biased sampling, exporters, the workspace connection and the retention values.
3. Fix the trace propagation for the three call types: `traceparent` on REST, the CloudEvents headers plus `traceparent` on Kafka, and the Temporal context propagator.
4. Render the golden-signal template for the 19 services and add the four platform panel groups.
5. Write the alert rules with their owner roles and message IDs, and test the route against the 15-minute target.
6. Add the pipeline baseline check: a service with no dashboard, a dashboard with no panel, a rule with no route or a hand-edited artefact fails the build.
7. Build the synthetic telemetry generator and the stub collector, and run the scrubbing, sampling and rendering tests against them.
8. Run the SIT canary, then publish the baseline and the run book index and hand it to each service OPS story.

**Done when.** The same dashboards, alert rules and SLOs are deployed to DEV, SIT and UAT from one repository; every one of the 19 services has the four golden-signal panel groups; one trace crosses REST, Kafka and Temporal in SIT with the call depth visible; every alert reaches an owner role within 15 minutes with a message ID; the four platform panel groups are populated; the scrubbing test passes; and the SIT canary has proved the baseline once and the service OPS stories have inherited it.

The dashboard names and the panel set per service, the metric and span names, the SLO targets, the alert thresholds and windows, the sampling policy, the retention of logs, metrics and traces, the workspace layout, the alert delivery channel and the on-call rota, the collector deployment and its owner, and the repository that hosts the dashboards and rules as code are Not specified in the source documents (GAP-1418; ASM-2481).

### 14. Validation and messages

| Message ID | When | Message |
|---|---|---|
| MSG-P1-001 | A panel or an alert depends on a data product and the ACE batch for that source is late or failed | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P2-004 | A scheduled job, a job step or the canary fails, or a job runs past its alert threshold | {job} failed at {time} for business date {date}. Follow run book {runbook}. |
| MSG-P4-002 | A role without the right tries an operator action on the baseline | You cannot {action} here. Your role does not include it. |

The baseline invents no message ID. The three IDs above already exist in the message catalogue: MSG-P1-001 for a data product stale after a late or failed ACE batch, MSG-P2-004 for a feed or scheduled job that failed or runs past its threshold, and MSG-P4-002 for an action the role does not include. Their wording is quoted from the catalogue and is not rewritten here; an alert that needs a new ID waits for the catalogue to give it one, and the rule carries no free text of its own.

### 15. Screens and states

None. This story adds no Workbench screen and no screen state. The operator surfaces are the dashboards, the alert list and the SLO view of the observability platform, which are read-only for an operator and are changed only through the baseline repository. The states of section 9 are review states of the baseline artefact and not screen states.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-N005-OPS-01 | AC1 | Component | The baseline pipeline applies to DEV, SIT and UAT from one repository; a second apply reports no change; a hand-created dashboard in a workspace is reported and removed by the next apply |
| TC-PLT-N005-OPS-02 | AC2 | Contract | The template renders 19 golden-signal dashboards from the 19-service list of §R4; a rendered dashboard with a missing panel fails the baseline check and names the service and the panel |
| TC-PLT-N005-OPS-03 | AC3 | Integration | A synthetic case action is one REST call with `traceparent`, one Kafka event with the CloudEvents headers plus `traceparent` and one Temporal activity; all three hops share one trace and the call depth is visible; no REST hop exceeds the 2 s budget |
| TC-PLT-N005-OPS-04 | AC4 | NFR | A failing interface, job and agent each alert to the owner role within 15 minutes; each alert carries an existing message ID; a rule with no route fails the baseline check; no alert is addressed to a person |
| TC-PLT-N005-OPS-05 | AC5 | Component | The four platform panel groups render with the synthetic telemetry: consumer lag and `.dlt` per topic, Temporal Schedule and workflow health, outbox relay lag per service, connection pool use per schema |
| TC-PLT-N005-OPS-06 | AC6, AC7 | End to end | The scrubbing test removes the known personal-data test field before export; a sampling, retention or threshold change is a value and not code; the SIT canary calls `POST /admin/workflows/smoke`, sees one trace, the populated panels and the routed alert, and a service OPS story inherits the baseline without adding a dashboard of its own |

### 17. Guardrails

- No business value in code: the sampling rate, the retention values, the thresholds, the windows and the SLO targets are values, and a rule change is a value change without a code release.
- No personal data in logs, metrics, spans or alert payloads: the scrubbing processor runs before export, and personal data stays in the owning service (Arch v5 slide 35).
- ACE data only through the owner's contract or the `v_ace_*` views: the baseline reads no ACE table and no service table, and the panels read telemetry only.
- No alert to a person and no alert without a message ID: every rule names an owner role and an existing message ID of the catalogue.
- No secret in a dashboard, a rule or a collector file: the workspace connection and the export credentials come from the secret store at deploy time.
- Dashboards, rules and SLOs are code: the workspace is never edited by hand, a manual change is reported, and the next pipeline run restores the baseline.
- Every test payload is synthetic: the generator emits IDs and facts only, and no production payload or personal data is copied into a test, a dashboard example or a run book.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| ADR-023 | Observability per service | The collector configuration, the resource attributes and the one dashboard template that every service inherits | TC-PLT-N005-OPS-01, TC-PLT-N005-OPS-02 |
| NFR-064 | Logs, traces and metrics across the workflow, the decision service and the agents | The three signal types in the collector configuration and the golden-signal panel set | TC-PLT-N005-OPS-02, TC-PLT-N005-OPS-03 |
| NFR-065 | Business measures per decision from the decision log | The decision-measure panel of the golden-signal set, read from the decision log and not counted separately | TC-PLT-N005-OPS-05 |
| NFR-066 | Agent acceptance, override rate, latency and cost measured and reported | The agent panel group of the golden-signal set for the agent service | TC-PLT-N005-OPS-05 |
| NFR-067 | Every scheduled job has a run book, monitoring and an alert to the operations channel | The `runbooks/README` index, the platform panel groups and the alert rule set | TC-PLT-N005-OPS-04, TC-PLT-N005-OPS-05 |
| NFR-068 | A failing interface, job or agent alerts a named owner within its target (15 minutes) | The alert route to owner roles, the message ID per rule and the route test | TC-PLT-N005-OPS-04, TC-PLT-N005-OPS-06 |
| Arch v5 slides 35 and 49 | One trace across services, events and workflows; OpenTelemetry and W3C Trace Context | The `traceparent` propagation on REST, Kafka and Temporal and the canary trace | TC-PLT-N005-OPS-03 |

### 19. Out of scope

- The per-service business panels: each service OPS story adds its own panels on top of this baseline and owns them.
- The run books for the Workbench jobs: RWB-PLT-E1056-OPS owns the run book for every Epic 1 job, and this story only indexes where each alert points.
- The service-template instrumentation, the OpenTelemetry agent and the library hooks: RWB-PLT-TPL and RWB-PLT-LIB.
- The collector's own infrastructure, its sizing and its high availability: the platform infrastructure stories.
- The SIEM and the PII path to SOC: ACE Common and the infrastructure stories, per Arch v5 slides 8 and 35.
- The platform jobs JOB-21 and JOB-22 themselves: the platform workflow epic owns the stuck-workflow scan and the smoke workflow; this story renders their health and uses the smoke endpoint in the canary.
- The exact thresholds, targets, sampling rates, retention periods and names: the gap GAP-1418, for the solution architect to close before the baseline is Published.
