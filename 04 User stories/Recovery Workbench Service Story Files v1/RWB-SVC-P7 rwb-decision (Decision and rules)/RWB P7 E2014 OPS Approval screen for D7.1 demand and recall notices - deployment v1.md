# RWB-P7-E2014-OPS Approval screen for D7.1 demand and recall notices

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E2014-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-014 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP19 |
| Parallel lane | L-P7-Z |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (FR-P7-019, FR-P7-027, FR-P7-028) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: deployment side of RWB-E2-014 for rwb-decision — the pipeline and image, the configuration and secrets, the migration run and the drift gate, the gateway-bff route registration and its budget, the cache warm-up, the dashboards and alerts, the run book and the rollback. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **DevOps engineer of the service**, I want **the D7.1 approval screen of rwb-decision deployed as one pipeline and one image behind the gateway-bff composite route, with its schema, its secrets, its reference-data warm-up, its route registration and timeout budget, its dashboards and alerts, and a run book with a rollback**, so that **the screen is served in SIT, UAT and PROD with the same configuration every time, an empty approval queue or a failing approval call is seen the same hour, and a bad release can be undone without a hand on a database**.

### 2. Business rationale

The screen is the first place a person approves a decision in the Workbench, so the deployment is the first place a failure becomes a business failure: an approval screen that answers but cannot write a decision record creates no record, an empty queue that nobody notices stops the litigation pipeline, and a route registered with a budget shorter than its composed reads shows an officer a panel that never loads. This story fixes the deployment of that capability: the pipeline and the image, the configuration and the secrets, the migration run and its drift gate, the route registration and its budget, the warm-up of the lists the screen needs, the dashboards and alerts, the run book and the rollback (Architecture v5 slides 20, 29, 33 and 44; ADR-021; ADR-023).

The legacy key had no deployment story of its own: the screen shipped with the monolith, its configuration was a property file and its job set carried a daily decision-log copy to the data lake. In the target there is no lake, the copy is continuous Kafka ingest in the owning service (DP-17, ADR-018), and the deployment owns no lake extract, no data-lake credential and no lake job in the run book (GAP-1261; ASM-2225).

### 3. Preconditions

- The service template, the Helm chart and the golden pipeline are available (RWB-PLT-TPL), and they deploy a service as an API deployment and a worker deployment on the same task queue (Architecture v5 slide 33).
- The `rwb_decision` schema and its login exist and are owned by the ACE DB story of this service (RWB-PLT-NF06-DB and the DB story of this key), so the deployment applies the migrations of its own schema only (ADR-014, ADR-021).
- The per-service Flyway sequence, the drift gate and the forward-only PROD rule are the platform deployment of RWB-PLT-E1044-OPS; this story supplies the rwb-decision values and proves the run.
- The key store holds the service's database login, its Kafka client credentials and its Temporal codec key as secret references (NFR-052).
- The gateway-bff route baseline is published (RWB-PLT-N001-CON) and its route registry accepts a route with its downstream, its method, its budget and its breaker.
- The parameters and reference-data contracts of rwb-case are live for the warm-up reads (RWB-P3-E1042-CON, RWB-P3-E1043-CON).
- The decision-record library and the outbox relay are part of the image and read their topic from configuration (DP-03, DP-09).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Pipeline: build the image of rwb-decision from the template, run the unit and contract tests of RWB-P7-E2014-CON, and publish the image with its digest.
2. Pipeline: run the drift gate of the platform against the `rwb_decision` target schema before the deployment to SIT, UAT and PROD, and stop on a difference.
3. Deployment: on start, Flyway applies each pending script of the rwb-decision sequence once, in version order, and writes the checksum to `flyway_schema_history` in `rwb_decision`.
4. Deployment: the pod reads its database login, its Kafka credentials and its codec key from the key store, and its base path, its topic, its queue and its schema name from the chart values of the environment.
5. Deployment: the service warms its reference lists — LOV-APPROVAL-STATUS, LOV-OVERRIDE-REASON and LOV-PRODUCT — and its age-limit parameters from the two rwb-case contracts before it reports ready.
6. Deployment: the gateway-bff route registration is applied with the downstream, the method, the 2 s budget and the breaker of the route, and the route health check passes through the edge.
7. Deployment: the smoke job reads the D7.1 queue through the route and the operation, and the deployment reports success only when both answer.
8. Operations: the dashboards show the approval-screen error rate, the latency of the route and of the three decisions, the age of the oldest waiting item and the size of the queue; the alerts fire on the conditions of section 14.
9. Operations: the run book names the checks, the rollback and the owner of each alert; a failed release is rolled back to the previous image digest and the previous route version.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The drift gate finds an object the migrations do not produce | The deployment stops before it starts and the object is named | MSG-P3-016 | AC3 |
| X2 | A secret cannot be read from the key store | The pod does not start and the failure is logged without the secret | None | AC2 |
| X3 | A warm-up read of the lists or the parameters fails | The pod stays not ready and retries; the screen is not registered as available | MSG-GEN-006 | AC5 |
| X4 | The route registration is refused by the route registry | The deployment fails and the previous route version stays | None | AC4 |
| X5 | The route answers beyond its budget under load | The alert fires and the route marks the panel temporarily unavailable | MSG-GEN-006 | AC4, AC6 |
| X6 | The D7.1 queue is empty for longer than the threshold | The empty-queue alert fires | None | AC6 |
| X7 | A release fails after the route registration | The rollback restores the previous image digest and the previous route version | None | AC7 |
| X8 | A lake extract, a lake credential or a lake job appears in the run book or the chart | The configuration test fails the pipeline | None | AC1, AC7 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the template, the chart, the schema and login, the key store, the route registry and the two rwb-case contracts |
| Negotiable | The alert thresholds, the dashboard names and the smoke schedule are settled with the platform observability team; the rules are fixed |
| Valuable | The capability can be released, observed and undone without a hand on a database, and a silent empty queue cannot happen |
| Estimable | One pipeline, one chart, one route registration, one warm-up step, one dashboard set and one run book |
| Small | Fits one sprint with its tests |
| Testable | Each criterion runs in a pipeline or an environment against the route and the service |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the D7.1 approval screen

  Background:
    Given the service is deployed as an API deployment and a worker deployment on the queue rwb-decision
    Given its schema is rwb_decision and its own login reads and writes that schema only

  Scenario: AC1 The pipeline builds one image and deploys the capability with no lake element (new, D-RCV-60)
    Given the golden pipeline of the platform template
    When the pipeline runs for this story
    Then it builds one image, runs the unit and contract tests of RWB-P7-E2014-CON and publishes the image with its digest
    Then the chart deploys the API deployment and the worker deployment on queue rwb-decision in namespace rwb-recovery
    Then the chart and the run book carry no data-lake extract, no data-lake credential and no lake job, because the lake is removed and the decision log ingest is continuous Kafka (GAP-1261; ASM-2225)
    Then the configuration test fails the pipeline when a lake element reappears

  Scenario: AC2 The configuration and the secrets are read from the environment and the key store (new, D-RCV-60)
    Given the chart values of SIT, UAT and PROD
    When the pod starts
    Then it reads the database login, the Kafka client credentials and the Temporal codec key as secret references from the key store
    Then it reads the schema name rwb_decision, the base path /api/recovery/decision/v1, the topic rwb.decision.events.v1, the record topic rwb.decision-record.v1 and the queue rwb-decision from the chart values of the environment
    Then the parameter and reference-data endpoints of rwb-case are configuration values and not code
    Then a scan of the image, the chart, the pipeline files and the logs finds no credential and no secret value

  Scenario: AC3 The migrations run on start and the drift gate stops a drifted schema (new, D-RCV-60)
    Given the rwb-decision Flyway sequence and the rwb_decision target schema
    When the service starts with pending scripts
    Then each script applies once in version order and flyway_schema_history records it with its checksum inside rwb_decision
    When a column has been added to rwb_decision by hand
    Then the drift gate of the platform stops the deployment before it starts and names the object with MSG-P3-016
    Then the deployment applies no script of another service and runs no clean in any profile

  Scenario: AC4 The gateway-bff route is registered with its downstream and its budget (new, D-RCV-60)
    Given the route of the approval screen and the route registry of the edge
    When the deployment registers the route
    Then the registration names the public route, the downstream host of rwb-decision, the method, the 2 s budget and the breaker per downstream
    Then the route is registered only after the service reports ready and the warm-up of AC5 has finished
    Then the smoke job calls the route and the queue operation and the deployment fails when either answers outside its budget
    Then the budget of this screen is recorded, and the exact budget of a screen that composes three reads is Not specified in the source documents (GAP-1270; ASM-2234)

  Scenario: AC5 The reference lists and the parameters are warm before the route is opened (new, D-RCV-60)
    Given a cold start of the service
    When it becomes ready
    Then LOV-APPROVAL-STATUS, LOV-OVERRIDE-REASON and LOV-PRODUCT are loaded from the reference-data contract and the two age-limit parameters from the parameters contract, each with its version
    Then a failed warm-up read keeps the pod not ready and retries, and the route is not opened to a pod without the lists
    Then the loaded versions are visible on the dashboard and the screen never shows a list version older than the one the service reports

  Scenario: AC6 The dashboards and the alerts cover the screen and its queue (new, D-RCV-60)
    Given the observability of the service under ADR-023
    When the dashboard and the alert rules are reviewed
    Then the dashboard shows the error rate and the p95 latency of the route and of the three decisions, the age of the oldest waiting D7.1 item and the size of the queue
    Then an alert fires on a 5xx rate above the threshold, on a route latency above the budget, on a decision record that cannot be written and on an empty D7.1 queue for longer than the threshold
    Then the alert names the service, the route and the owner role, and carries no case fact and no personal data
    Then the thresholds and the empty-queue window are Not specified in the source documents (GAP-1271; ASM-2235)

  Scenario: AC7 The run book and the rollback are proved (new, D-RCV-60)
    Given the run book of the capability
    When a release is rolled back in SIT
    Then the run book names the checks of a failed approval call, a failed record write, an empty queue and a refused route registration, each with its message ID and its owner
    Then the rollback restores the previous image digest and the previous route version, and the schema is not rolled back because PROD is forward only
    Then no run book step asks for a hand change on rwb_decision, a lake extract or a credential in a file
    Then the rollback is proved in SIT inside the release window of the environment
```

These seven criteria are new, test only the deployment of the capability and repeat no legacy criterion.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One pipeline, one image and one chart per service; the same image is promoted through SIT, UAT and PROD with different values only | Architecture v5 slides 29 and 33; ADR-021 |
| BR2 | The service reads and writes `rwb_decision` only, with its own login, and applies no script of another service | ADR-014; DP-01 |
| BR3 | Every credential is a secret reference from the key store; no credential appears in a chart value, an image layer, a pipeline file, a log or a prompt | NFR-052 |
| BR4 | Migrations run on start and the drift gate stops a drifted schema before SIT, UAT and PROD; PROD is forward only | RWB-PLT-E1044-OPS BR3, BR4 |
| BR5 | The route is registered with its downstream, its budget and its breaker, and only after the service is ready and warm | Architecture v5 slides 10, 20 and 35; DP-19 |
| BR6 | Every cross-service call behind the screen is one hop with a 2 s budget; the route is never registered with a shorter budget than its composed reads need | ADR-020; DP-11 |
| BR7 | The lists and the parameters the screen needs are warmed with their version and the pod is not ready without them | DP-06, DP-07 |
| BR8 | Every service has its own dashboards and alerts (ADR-023), and an alert carries identifiers, codes and facts only | ADR-023; Template and Rules §R7.2 s17 |
| BR9 | An empty approval queue is a defect and is alerted, because an unapproved notice stops the dispatch run | REQ-APD-006; CTL-14 |
| BR10 | No data lake: the deployment carries no lake extract, no lake credential and no lake job, and JOB-13 is continuous Kafka ingest in the owning service | DP-17; ADR-018 |
| BR11 | A rollback restores the image and the route version and never rolls a schema back | RWB-PLT-E1044-OPS BR4; ADR-021 |
| BR12 | No business value in the chart or in a run book step: age limits, thresholds and route role codes stay parameters and reference data | DP-06, DP-07 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Pipeline starts | The contract tests pass and the drift gate passes | Building |
| Building | Image published | The digest is recorded | Deploying |
| Deploying | Migrations applied and the warm-up finished | The lists and the parameters carry a version | Registering |
| Registering | Route registered and the smoke job passes | The route and the queue operation answer inside the budget | Serving |
| Serving | A release fails or an alert is accepted | The run book step is taken | Rolled back |
| Rolled back | Previous image and route version restored | The schema is unchanged | Serving |

The approval and screen states themselves — READY, STALE_INPUT, DECIDED and the panel states — are the app story's and are declared in RWB-P7-E2014-CON; this story deploys them and observes them.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer of the service | Owns the pipeline, the chart, the route registration, the dashboard and the run book |
| RW-PLATADM, platform administrator | Reads the deployment, the route and the alert state; runs the run book steps that are platform-side |
| RW-AUDIT, internal audit | Reads the deployment history and the alert history (Platform administration R) |
| Key store administrator | Owns the secret entries and their rotation; not a Workbench role |
| Platform route owner | Owns the route registry and approves a route registration and its budget |
| Platform observability owner | Owns the dashboard and alert platform and the threshold review |
| Service owner of rwb-decision | Accepts the release and the rollback |

No deployment step names a person; the run book names roles and on-call rotations, never individuals.

### 11. Data

No business field is written by this story. The deployment writes the migration history inside `rwb_decision` and the deployment and alert records of the platform, and it reads the two contracts of rwb-case for the warm-up. The deployment record carries the service, the environment, the image digest, the migration versions applied, the drift result, the route version, `startedAt`, `endedAt` and a status.

The dashboard names, the alert thresholds and the empty-queue window are Not specified in the source documents (GAP-1271; ASM-2235), and the budget of a screen that composes three reads is Not specified in the same way (GAP-1270; ASM-2234). The working values of this story are a 2 s route budget inherited from the platform, an alert on any 5xx in five minutes, and a 24-hour empty-queue window that follows the 1 working day service level of D7.1.

### 12. Contract

#### 12.1 REST operations provided

None. The deployment provides no REST operation; it registers the route of the screen, which is the edge's, and consumes the service's own operations to prove the release.

#### 12.2 REST operations consumed

| Method and path | Owner | Use |
|---|---|---|
| GET `/api/recovery/approvals/{approvalId}` | PLT gateway-bff, RWB-PLT-N001-CON | The smoke probe of the registered route after the deployment and on every release |
| GET `/api/recovery/decision/v1/approvals` | P7 rwb-decision, RWB-P7-E2014-CON | The readiness probe of the queue read, with `decision=D7.1` and a page of one |

#### 12.3 Events published

None. A deployment publishes no event; the `DecisionRecorded` event of the screen is published by the service at run time and not by the deployment.

#### 12.4 Events consumed

None. A deployment consumes no event. The consumer groups of the service are created by its deployment from the topic configuration and are not event-schema elements of this story.

#### 12.5 Workflows and activities

None. `ApprovalWorkflow` is started at run time by RWB-P7-E2013-APP; the deployment starts no workflow and registers no activity, and it verifies only that the worker deployment polls the queue `rwb-decision`.

#### 12.6 Schedules

None. The two Schedules of the service — the rule promote at 00:01 (JOB-20) and the hash-chain check at 02:00 (JOB-14) — belong to the rule registry story and the decision log store story, and this deployment neither creates nor owns a Schedule.

#### 12.7 Tables owned

None. The deployment owns no business table; Flyway writes `flyway_schema_history` inside `rwb_decision`, and `approval`, `decision_log_entry` and the library objects are the service's rows written at run time.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| gateway-bff route fake | The registered route answering the two panels with the 200, the 401, the 403, the 404 and the 503 examples, and a delayed answer beyond the budget | Smoke job, rollback test, NFR cases |
| rwb-decision readiness fake | The queue read answering a page with one D7.1 approval and an empty page for the empty-queue alert test | Smoke job, alert test |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 consumed | The route smoke probe and the queue readiness probe |
| Kafka | None | The deployment publishes and consumes no event |
| Temporal | None | The deployment starts no workflow; it verifies the worker polls `rwb-decision` |
| File | None | The image carries the migration scripts; no file crosses the deployment |

### 13. Solution plan

**Deliverables.** The pipeline stage that runs the contract tests and the drift gate for rwb-decision, the chart values per environment with the secret references, the warm-up step for the lists and the parameters, the route registration with its budget and breaker, the dashboard and the four alert rules, the smoke job and the run book with its rollback.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_decision`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/decision/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-15 is not claimed as a pattern of this story: the per-service Flyway sequence, its drift gate and the forward-only PROD rule are the platform deployment of RWB-PLT-E1044-OPS, and this story supplies the rwb-decision values and proves the run (AC3). No pattern is claimed for DP-02, DP-04, DP-08, DP-12, DP-14, DP-16, DP-17, DP-18 or DP-20 either: this story declares no login, no rule package, no authorise call, no case workflow, no renamed topic, no integration adapter, no lake element, no ledger entry and no agent client. DP-17 is the removal this deployment must honour: the run book and the chart carry no lake extract, no lake credential and no lake job (GAP-1261; ASM-2225).

**Build steps**

1. Add the pipeline stage: build, the contract tests of RWB-P7-E2014-CON, the image digest and the drift gate.
2. Set the chart values per environment: `rwb_decision`, the base path, the topic, the record topic, the queue and the two rwb-case endpoints, with the secrets as key-store references.
3. Add the warm-up step of the lists and the parameters and make readiness depend on it.
4. Register the route with its downstream, its budget and its breaker after readiness, and add the smoke job.
5. Build the dashboard and the four alert rules of AC6, with role-based routing and no case fact in the alert payload.
6. Write the run book with the four checks, the rollback and the owner role of each alert.
7. Prove the rollback in SIT and prove the configuration test that fails on a lake element.

**Done when.** The seven cases of section 16 pass in SIT, the drift gate stops a drifted `rwb_decision`, the route is registered with its budget and the smoke job is green, the dashboard and the four alerts are live with a tested firing, and the rollback is proved inside the release window.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-016 | Drift found, checksum mismatch or a refused clean | Schema check failed in {schema}: {object}. The deployment was stopped. |
| MSG-GEN-006 | A consumed call, the warm-up or the smoke probe does not answer in time | {system} is not available. Your request is queued and will be retried. |
| MSG-P7-003 | The record write fails on a deployed release probe | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A role without Platform administration R reads the deployment or the alerts | You cannot {action} here. Your role does not include it. |

MSG-P3-016 is the migration message of RWB-PLT-E1044-OPS, carried unchanged; MSG-GEN-006, MSG-P7-003 and MSG-P4-002 are the platform catalog's and the decision record's. They are shown in the pipeline log, on the dashboard and in the run book, not to business users.

### 15. Screens and states

No new screen. SCR-44 Interface and job monitor shows the deployment, the migration run and the route registration of the service, with the image digest, the schema, the versions applied, the drift result and the route version. The approval screens themselves — SCR-10, SCR-11 and SCR-18 — are served through the composite route and are deployed here and built in RWB-P7-E2014-APP; their states belong to RWB-P7-E2014-CON.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P7-E2014-OPS-01 | AC1 | Component | The pipeline of the template: one image, the contract tests, the digest, the two deployments, and the configuration test that fails on a lake element |
| TC-P7-E2014-OPS-02 | AC2 | NFR | A scan of the image, the chart, the pipeline files and the logs; every credential a key-store reference; the values of the three environments |
| TC-P7-E2014-OPS-03 | AC3 | End to end | The rwb-decision sequence on a clean schema; a hand-added column in SIT, UAT and PROD stops the deployment with MSG-P3-016 |
| TC-P7-E2014-OPS-04 | AC4 | End to end | The route registration with its downstream, budget and breaker; the smoke probe; a probe beyond the budget fails the release |
| TC-P7-E2014-OPS-05 | AC5 | Component | A cold start with the three lists and the two parameters; a failed warm-up keeps the pod not ready and the route closed |
| TC-P7-E2014-OPS-06 | AC6 | NFR | The dashboard and the four alerts: a 5xx spike, a latency above budget, a failed record write and an empty queue |
| TC-P7-E2014-OPS-07 | AC7 | End to end | The run book steps and a rollback in SIT: the previous digest and the previous route version, with the schema unchanged |

### 17. Guardrails

- One schema and one login per service: the deployment uses the login of rwb-decision and touches no other schema (DP-01, DP-02).
- No credential in a chart value, an image layer, a pipeline file, a log or a prompt; every account is a key-store reference.
- No drift gate bypass in SIT, UAT and PROD, and no clean and no undo in PROD; a fix is a new version through the pipeline.
- No business value in the chart or the run book: the age limits, the thresholds and the route role codes stay parameters and reference data.
- No personal data in a dashboard, an alert, a deployment record or a log: identifiers, codes and facts only.
- No data lake: no lake extract, no lake credential and no lake job in the chart, the pipeline or the run book (DP-17).
- One hop and a 2 s budget on every call behind the screen, and the route is registered with that budget and a breaker per downstream (DP-11, DP-19).
- ACE data only through the owner's contract; the deployment declares no ACE view and no SQL of its own.
- The rollback restores the image and the route version and never a schema; the forward-only rule stands (ADR-021).

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-APD-006 | Demand and recall notices approved through approval routing | The route registration, the smoke probe and the empty-queue alert that keep the approval path serving | TC-P7-E2014-OPS-04, TC-P7-E2014-OPS-06 |
| REQ-APD-002 | Recommendation, reasons, inputs and limit on one screen | The warm-up of the lists and the parameters behind the screen, and the latency budget of the route | TC-P7-E2014-OPS-04, TC-P7-E2014-OPS-05 |
| NFR-052 | Database and drift accounts held in the key store | The secret references of the chart and the credential scan | TC-P7-E2014-OPS-02 |
| NFR-008 | A screen responds within its target under normal load: under 2 seconds | The route budget and the latency alert | TC-P7-E2014-OPS-04, TC-P7-E2014-OPS-06 |
| ADR-021 | Per-service Flyway and migration ownership | The migration run on start, the drift gate and the forward-only rule | TC-P7-E2014-OPS-03, TC-P7-E2014-OPS-07 |
| ADR-023 | Observability per service | The dashboard and the four alerts | TC-P7-E2014-OPS-06 |
| ADR-018 | No data lake; reporting from events | The absence of every lake element from the chart, the pipeline and the run book | TC-P7-E2014-OPS-01, TC-P7-E2014-OPS-07 |

### 19. Out of scope

- The implementation of the screen, the checks, the notice calls and the record path: RWB-P7-E2014-APP.
- The contract baseline of the screen, its field list, its mask flags and its fakes: RWB-P7-E2014-CON.
- The per-service Flyway baseline, the drift gate implementation and the forward-only rule as a platform capability: RWB-PLT-E1044-OPS and RWB-PLT-E1044-APP-2.
- The creation of the `rwb_decision` schema and login and their grants: RWB-PLT-NF06-DB and the DB story of this key.
- The gateway-bff implementation, the session, the masking engine and the push: RWB-PLT-N001-APP; this story registers the route and proves it.
- The routing of a generated notice, the approval level matrix and the DoA table read: RWB-P7-E2013-APP.
- The platform dashboards and alerts beyond this service's four rules: RWB-PLT-OBS.
- The two Schedules of the service and their run books: the rule registry story and the decision log store story.
- Deployment slots and the release windows of the programme: DL34 and DL35.
