# RWB-P4-E1039-OPS Access log into the decision log and break-glass admin

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: DevOps slice of legacy RWB-E1-039 for rwb-access — the Helm values, the Kafka ACLs on the access and decision topics with their retry and dead-letter paths, the secrets, the alerting of a failed or refused access-log write and of break-glass use, and the run book. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P4-E1039-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-039 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP11, DP13, DP17, DP19 |
| Parallel lane | L-P4-V |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (FR-P4-023, FR-P4-024, FR-P4-025, FR-P4-026, FR-P4-027, FR-P4-028, FR-P4-029, FR-P4-030, FR-P4-031) |
| Status | Draft (realignment v1) |

### 1. Story

As a **platform engineer**, I want **the access-log and break-glass capability of `rwb-access` deployed as one service from the service template, with its Helm chart and values, its migration job invocation, its probes, the Kafka ACLs on `rwb.access.events.v1` and `rwb.decision-record.v1` with their retry and `.dlt` topics, the three secret references, the alerting of a failed or refused access-log write and of break-glass use routed to the security administrator queue, and the run book**, so that **the capability runs predictably in every environment and an operator can see and act on a failure of the log or of the grant without reading code**.

This is the DevOps slice of legacy key RWB-E1-039 under epic RWB-SVC-P4. It delivers no application code, **provisions no database object** — the four tables, the grants and the partitions are RWB-P4-E1039-DB's — and **changes no business rule**: every threshold, window and message id it uses is the one the contract and the app story already fix.

**The division of this legacy key is fixed and is the same in all four stories.** **RWB-P4-E1039-APP** owns the ten legacy acceptance criteria and implements the writer, the grant and the read. **RWB-P4-E1039-CON** owns the published contract of the four operations, the entry shape, the two-person rule, the time box, the refusal vocabulary and the fail-closed rule. **RWB-P4-E1039-DB** owns the ACE DB slice in `rwb_access`, provisions every table of the key and runs the migration. **RWB-P4-E1039-OPS** owns the deployment, the topics and their ACLs, the secrets, the alerts and the run book. **The end-to-end proof is RWB-ITG-E1039-ITG**, and the two neighbours of the same legacy key are **RWB-P5-E1039-APP** on the document side and **RWB-P7-E1039-APP** on the ledger side.

The story covers:

- the chart and its values for three environments, with the image digest and the chart version pinned, no replica count, resource size, threshold or cadence in a template;
- the pre-deploy invocation of the per-service Flyway migration job, which is owned and written by RWB-P4-E1039-DB and only invoked here;
- the readiness and liveness probes, neither of which writes to the database;
- the topic ACLs of the service identity, the topic provisioning of the retry and `.dlt` paths, and the shared decision topic that is reused and never recreated;
- the three secret references from the platform secret store;
- the alert rules of a failed or refused access-log write, of a break-glass activation, of a refused break-glass request and of a lagging outbox, each with its message id and one runbook entry;
- the run book of six entries.

### 2. Business rationale

The legacy story depended on one shared log table, an in-process publisher and a set of standing alert conditions that lived in an operations note. In the target a service is a Helm release built by one pipeline, with its own schema, login, topic, queue and secret references (DP-02, DP-09, DP-15), and two of its behaviours are security controls rather than features: an access log that silently stops recording, and a break-glass grant that nobody sees. Neither can be caught by a stack trace, so both have to be made observable at deployment time.

**The division is fixed and is the same in all four stories.** The app slice is **RWB-P4-E1039-APP**, the contract is **RWB-P4-E1039-CON**, the schema and the tables are **RWB-P4-E1039-DB**, and **RWB-ITG-E1039-ITG** proves the key end to end; **RWB-P5-E1039-APP** records the document side and **RWB-P7-E1039-APP** owns the central ledger. **RWB-P4-E1039-OPS** adds no behaviour to any of them: it deploys what they build, grants the service identity exactly the topics it writes, and turns two silent failures into paged or queued alerts.

The ACLs are the tightest statement of the split the workbench makes about the log. `rwb-access` **writes** `rwb.decision-record.v1` because every service publishes its own decision records (Architecture v5 slides 28 and 42), and it **writes** `rwb.access.events.v1` because that is the service's own topic for `AccessPolicyChanged` and `DoaLimitChanged`. It **reads** neither of another service's business topics, because P4 consumes no event (slide 14), and it has no ACL on `rwb.decision.events.v1`: the central ledger of P7 consumes the decision topic and answers the query, and the access owner never reads the ledger's topic or its tables. A deployment that granted a read on `rwb.decision-record.v1` would let the access owner keep a second copy of the ledger, which is exactly what DP-01 and DP-03 forbid.

The alert routes follow from who can act. A **failed access-log write** is a fail-closed condition: the read was refused, so a caller is blocked and the platform on-call queue is paged with MSG-P7-003 and the operation, route and trace id. A **refused access-log write** — a 403 on an admin read — is counted on the dashboard and never pages anyone, because a refusal is the control working. A **break-glass activation** and a **refused break-glass request** are security events: they go to the security administrator queue with MSG-P4-004 and MSG-P4-007, so the reviewer sees the use inside the review window of one working day rather than finding it in a monthly report. The thresholds and the review window are parameter values and not deployment values, so a business person changes them without a release (DP-06).

The values copied from the sources are the service, the base, the two topic names, the retry and `.dlt` suffixes, the message ids of the legacy story and the parameter names of the break-glass window and the review window. Where no source names the alert thresholds, the Kubernetes topology or the secret names, the story carries the placeholder and the assumption in force (GAP-0783; ASM-1430).

### 3. Preconditions

- The service template, chart skeleton and pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The Kafka event platform provisions topics with a retry topic and a `.dlt` topic, and the shared topic `rwb.decision-record.v1` exists as a platform asset (RWB-PLT-EVT, RWB-PLT-TE006-CON).
- The three environments DEV, SIT and UAT exist with the parameter scope of LOV-ENVIRONMENT, and the parameter rows of the break-glass window, the incident pattern, the reason bounds and the review window are loaded through RWB-P3-E1042-CON.
- RWB-P4-E1039-DB has published the migration folder of the service, so the pre-deploy job has a sequence to run; this story invokes it and owns no statement of it.
- The platform error envelope and the message catalogue are in force, so an alert can carry a message id and the agreed text.
- The platform secret store and the ACE Common PII and SOC logging path are available; the second copy of an access event still leaves the service through ACE Common (Architecture v5 slide 30).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7), and the per-service login name is Not specified in the source documents (GAP-0783; ASM-1427).

### 4. Flow

1. The pipeline builds the service image, runs the unit, component and contract tests, scans the image and the dependencies, and publishes the Helm chart version; the image digest and the chart version come from the same commit.
2. The chart deploys the service with its own login reference, the pre-deploy migration job of RWB-P4-E1039-DB and the two probes; the migration job runs before the deployment is marked ready.
3. The provisioning step creates `rwb.access.events.v1` with its retry topic and its `.dlt` topic, joins `rwb.decision-record.v1` as a producer, and creates the retry and `.dlt` topics of the shared topic where the platform has not already created them; the shared topic itself is reused and never recreated.
4. The ACL step applies the service identity's rights: WRITE on `rwb.access.events.v1`, WRITE on `rwb.decision-record.v1` and on the retry topics, DESCRIBE on both, and READ on a `.dlt` topic for the operator replay identity only.
5. The secret references are mounted from the platform secret store: the rwb-access login, the Kafka client credential and the Temporal mTLS material. No value of any of them is written in a values file, a chart template, a dashboard or the run book.
6. The dashboards are published: entries written, entries refused, entries failed, grant activations by environment, grants ended, the active grant count, and the outbox and ledger lag.
7. The alert rules are wired to the message ids of section 14 and to the run book entries, with the platform on-call queue for a failed write and the security administrator queue for break-glass.
8. A smoke step writes one synthetic access entry and one synthetic grant in a test namespace, checks that both appear once on the topic and on the dashboard, and checks that both alerts fire on a forced failure.
9. The run book is published with the six entries and is reviewed by the on-call rota before the SIT release.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The migration job fails | The deployment stays unready and the pipeline stops; no traffic to the new version | None | AC1 |
| X2 | The readiness probe fails after the start-up window | The pod is removed from the service and the pipeline marks the release failed | None | AC1 |
| X3 | The topic is missing its retry or `.dlt` topic | The provisioning step fails the release; the relay refuses to start | None | AC3 |
| X4 | The service identity is granted READ on `rwb.decision-record.v1` or on another service's business topic | The ACL review fails the release: a read right would let the service keep a second copy of the ledger | None | AC3 |
| X5 | A secret value is found in a values file, a chart template or the run book | The pipeline scan fails the release | None | AC4 |
| X6 | Access-log entries fail to be written | The alert carries MSG-P7-003, the operation and the trace id, and pages the platform on-call queue | MSG-P7-003 | AC5 |
| X7 | Access-log entries are refused for want of a right | The refused count rises on the dashboard and nothing pages; a refusal is the control working | MSG-P4-002 | AC5 |
| X8 | A break-glass grant is activated | The alert carries MSG-P4-004, the grant id and the end time, and routes to the security administrator queue | MSG-P4-004 | AC5 |
| X9 | A break-glass request is refused | The alert carries MSG-P4-007 and the reason code NO_BREAKGLASS_GRANT and routes to the security administrator queue | MSG-P4-007 | AC5 |
| X10 | The outbox relay lags beyond the alert threshold | The lag alert names the topic and the delay; the entries are already committed and the ledger catches up | None | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the platform topic provisioning and the secret store; no application code and no database object is built here |
| Negotiable | Replica counts, resource sizes, alert thresholds and the lag window are environment values, not story decisions |
| Valuable | Makes a silent failure of the log and an unseen break-glass use visible and actionable in every environment |
| Estimable | One chart, one pipeline stage, one migration job invocation, two probes, one provisioning and ACL step, four dashboard series and six alert rules |
| Small | Fits one sprint with the run book |
| Testable | Every criterion tests an artefact: the chart renders, the probes answer, the ACLs are exact, the secrets are references, the alerts fire on a synthetic metric |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the access-log and break-glass capability of rwb-access

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the target environment is SIT

  Scenario: AC1 The chart and values deploy rwb-access (new, D-RCV-60)
    Given the rwb-access Helm chart and its values files
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the release declares the rwb-access login reference and no other service's credential
    Then the migration job of RWB-P4-E1039-DB runs as a pre-deploy job before the deployment is marked ready
    Then the readiness probe is false until the migration, the outbox relay and the worker are up, and liveness stays true
    Then neither probe writes to the database
    Then no replica count, resource size, alert threshold or cadence is hard-coded in the template

  Scenario: AC2 The pipeline builds, tests and promotes one artefact (new, D-RCV-60)
    Given a commit on the main line
    When the pipeline runs
    Then it builds one image and one chart version from the same commit
    Then it runs the unit, component and contract tests of the four operations and fails on a contract drift
    Then it scans the image and the dependencies and fails on a critical finding
    Then it promotes the same artefact through DEV, SIT and UAT without a rebuild

  Scenario: AC3 The topic ACLs grant exactly what the service writes (new, D-RCV-60)
    Given the provisioning and ACL step for rwb-access
    When it runs against the environment
    Then the topic rwb.access.events.v1 exists with its retry topic and its .dlt topic
    Then the service identity has WRITE on rwb.access.events.v1 and on rwb.decision-record.v1 and on the retry topics, and DESCRIBE on both
    Then the shared topic rwb.decision-record.v1 is reused as a platform asset and is never recreated
    Then the service identity has no READ on rwb.decision-record.v1 and no ACL on any other service's business topic
    Then the operator replay identity is the only principal with READ on a .dlt topic

  Scenario: AC4 The secrets are references to the platform store (new, D-RCV-60)
    Given the chart and the values files of the three environments
    Then the rwb-access login, the Kafka client credential and the Temporal mTLS material are mounted from the platform secret store by reference
    Then no secret value appears in a values file, a chart template, a dashboard, an alert payload or the run book
    Then a rotated credential is picked up without a chart change

  Scenario: AC5 A failed write pages and a break-glass use is queued to the security administrator (new, D-RCV-60)
    Given the six alert rules of the capability
    When a forced failure of the access-log write, a forced refusal, a grant activation and a refused grant are replayed in a test namespace
    Then the failed write raises its alert with MSG-P7-003, the operation and the trace id, and routes to the platform on-call queue
    Then the refusal count rises on the dashboard and raises no page, and the alert carries MSG-P4-002
    Then the grant activation routes to the security administrator queue with MSG-P4-004, the grant id and the end time
    Then the refused grant routes to the same queue with MSG-P4-007 and the reason code NO_BREAKGLASS_GRANT
    Then every alert links one runbook entry with the check, the owner role and the recovery step

  Scenario: AC6 The run book covers the six conditions (new, D-RCV-60)
    Given the published run book
    Then it holds one entry for a failed access-log write, one for a refused write, one for a grant activation, one for a refused grant, one for an outbox or ledger lag and one for a failed migration or probe
    Then each entry names the check, the owner role, the recovery step and the message id
    Then no entry of the run book changes a business rule, a window or a threshold: each points at the parameter row instead
    Then no entry carries a personal value or a credential
```

These six criteria are new and test the deployment artefacts only. No legacy acceptance criterion is copied: AC1 to AC10 of RWB-E1-039 belong to RWB-P4-E1039-APP, and the legacy test cases are named in section 18.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One service, one schema, one login: the release uses the rwb-access login reference and no other service's credential | DP-02; Architecture v5 slide 41 notes |
| BR2 | The migration is the per-service Flyway sequence of RWB-P4-E1039-DB and runs before the deployment is ready; this story invokes it and provisions no database object | DP-15; RWB-PLT-E1044-CON |
| BR3 | Every topic the service uses has a retry topic and a `.dlt` topic, and the shared decision topic is reused and never recreated | DP-09; Architecture v5 slide 42 notes |
| BR4 | The service identity writes the decision topic and its own topic and reads neither of another service's business topics, because P4 consumes no event | DP-01, DP-09; Architecture v5 slide 14 |
| BR5 | No environment value is hard-coded: replica counts, resource sizes, thresholds, the lag window and the cadences come from values files and parameters | DP-06; Template and Rules §R7.2 s17 |
| BR6 | An alert carries a message id and the agreed text, and links one runbook entry | Template and Rules §R7.2 s14 |
| BR7 | A failed access-log write pages the platform on-call queue; a refused write is counted and never pages | RWB-E1-039 BR2; MSG-P7-003, MSG-P4-002 |
| BR8 | A break-glass activation and a refused break-glass request route to the security administrator queue, so the review inside the window is possible | RWB-E1-039 BR7; MSG-P4-004, MSG-P4-007 |
| BR9 | No secret is written in a values file, a chart template, a dashboard, an alert payload or the run book | NFR-052 |
| BR10 | The deployment changes no business rule: the window, the incident pattern, the reason bounds and the review window stay parameter rows | DP-06; RWB-P4-E1039-CON BR11 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the migration job pass the pipeline | Deploying |
| Deploying | Migration job complete and probes healthy | The schema is at the expected version and both probes answer | Ready |
| Ready | Release superseded | A new chart version is promoted | Rolling |
| Rolling | All pods on the new version | The old ReplicaSet drains | Ready |
| Ready | Migration job failed | The schema is not at the expected version | Failed |
| Failed | Rollback | The previous chart version is redeployed and the migration is reversed by its own script | Ready |

The grant and entry states of the capability belong to the app story; this story shows them only as dashboard and alert facts.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the provisioning and ACL step, the dashboards and the run book |
| Platform administrator | Owns the Kafka provisioning rights, the shared decision topic and the secret store |
| ACE database administrator | Owns the rwb_access schema, the login and its grants, and approves the migration job invocation |
| Release manager | Approves the promotion of one artefact through the environments |
| Security administrator | Receives the break-glass alerts and reviews the use inside the window |
| On-call operator | Runs the runbook entries and opens an incident when MSG-P7-003 or a break-glass anomaly persists |
| RW-PLATADM | Uses the grant in the running service, not in the cluster |
| RW-AUDIT, RW-COMPLY | Read the access log through the operation; neither holds a cluster right |

The per-service login name used by the chart is Not specified in the source documents (GAP-0783; ASM-1427); the chart references "the rwb-access login (DP-02)" through a secret reference and never a literal name.

### 11. Data

| Item | Content |
|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, the `rwb.access.access-log` switch, environment name |
| Schema | `rwb_access`, migrated by the pre-deploy job of RWB-P4-E1039-DB; this story creates no object of it |
| Topics | `rwb.access.events.v1` with retry and `.dlt`; `rwb.decision-record.v1` with its retry path, reused as a platform asset |
| ACLs | WRITE and DESCRIBE for the service identity on the two topics and on the retry topics; READ on a `.dlt` topic for the operator replay identity only |
| Dashboard series | entries written, entries refused, entries failed, grant activations by environment, grants ended, active grant count, outbox lag, ledger lag |
| Alert rules | failed write, refused write, grant activation, refused grant, outbox lag, migration or probe failure |
| Runbook entries | failed access-log write, refused write, grant activation, refused grant, outbox or ledger lag, failed migration or probe |
| Secrets | the rwb-access login, the Kafka client credential and the Temporal mTLS material, all by reference from the platform secret store |

The deployment topology detail (cluster names, node pools, replica counts, resource sizes, zone spread, ingress class and the exact probe timings) is Not specified in the source documents (GAP-0783; ASM-1430); the chart exposes them as values and this story fixes only their names and the rule that they are not hard-coded. The alert thresholds and the lag window are Not specified in the source documents (GAP-0783; ASM-1430) and are values with a parameter row behind them.

### 12. Contract

#### 12.1 REST operations provided

The deployment exposes the four operations of RWB-P4-E1039-CON behind gateway-bff: `GET /api/recovery/access/v1/admin/access-log`, `POST /api/recovery/access/v1/admin/break-glass-grants`, `POST /api/recovery/access/v1/admin/break-glass-grants/{grantId}/end` and `GET /api/recovery/access/v1/admin/break-glass-grants/{grantId}`. Owner rwb-access (P4). The probes are cluster-internal and are not part of the API surface.

#### 12.2 REST operations consumed

| Method | Path | Owner | Deployment need |
|---|---|---|---|
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The session and the break-glass state, at the readiness smoke and at each request |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The window of 4 hours, the incident pattern, the reason bounds and the review window; 2 s client budget with a breaker (DP-11) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-DECISION, LOV-CAPABILITY, LOV-SCOPE and LOV-ROLE with the version in force (DP-07) |

#### 12.3 Events published

| Event | Topic | Provisioning | Producing story |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | Shared topic reused with its retry and `.dlt` path; WRITE for the service identity through the outbox relay | RWB-P4-E1039-APP |
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | Topic with retry and `.dlt`; WRITE for the service identity | RWB-P4-E1037-APP |
| `rwb.access.DoALimitChanged.v1` | `rwb.access.events.v1` | Same topic, same retry and `.dlt` path | The delegation story of RWB-SVC-P4 |

The chart grants the write rights of all three because they share one service identity; the two policy events are not produced by this legacy key and are listed so that the ACL set is complete and reviewed once.

#### 12.4 Events consumed

None. `rwb-access` is the reference-data owner of Architecture v5 slide 14, whose contract line records no consumed event; the deployment creates no consumer group and subscribes to no topic, which is why the inbox of the service stays empty.

#### 12.5 Workflows and activities

None. The capability starts no workflow and registers no activity; the `rwb-access` task queue carries the access review Schedule of RWB-P4-AD008-APP and this story does not register it.

#### 12.6 Schedules

None. The six-monthly access review list (JOB-18) is a Schedule of rwb-access but belongs to RWB-P4-AD008-APP, and the retention action of the access log is a partition drop owned by RWB-P4-E1039-DB and the platform retention job, not a Temporal Schedule.

#### 12.7 Tables owned

None provisioned here. The four tables of this key — the local decision-record table of the DP-03 library, `outbox_event`, `processed_event` and `idempotency_key`, plus `break_glass_grant` — are created by RWB-P4-E1039-DB in `rwb_access`, and **this story creates no database object and no grant**. It invokes that migration job, and it provisions only Kafka topics and ACLs, secret references, dashboards and alerts. `decision_log_entry` and the central ledger are P7's and appear in no chart, no ACL and no dashboard of this service.

#### 12.8 Contract fakes

| Fake | Deployment use |
|---|---|
| rwb-case WireMock | Runs in the pipeline and in the SIT smoke profile, so the release can start without the parameters and reference-data service |
| rwb-decision WireMock | Same, for the `GET /decision-log` answer the audit smoke reads |
| rwb-access contract fake | The seven fakes of RWB-P4-E1039-CON run as the SIT smoke profile of this service |
| IAM group fake | The member and non-member answers of the break-glass group for the smoke of AC5 |

The fakes are test-only workloads; they are not deployed into UAT or production.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 3 consumed in the deployment path | The four operations; the session, parameters and reference-data reads; one hop, 2 s |
| Kafka | 3 published, 0 consumed | `rwb.decision-record.v1` and `rwb.access.events.v1` with their retry and `.dlt` topics; no consumer group |
| Temporal | 0 | No workflow, activity or Schedule is registered by this story |
| File | None | The release reads no runtime file; values files are build inputs |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. The chart references one schema and one login | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`. The deployment grants the write right on the shared topic and its retry path | referred to; the consuming story carries the dependency H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library. The thresholds, the window and the review window are parameter rows and values, never chart literals | referred to; the consuming story carries the dependency H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case. The event codes and areas the smoke uses come from the list with its version | referred to; the consuming story carries the dependency H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout. The three consumed calls are configured with their budget and breaker | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/access/v1`. The route and the probes sit under the service base; the route is registered on gateway-bff | none |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting. The deployment provisions no lake sink and no lake export for the log | none; no lake data is deployed |
| DP-19 | Screen, ace-web | gateway-bff composite route. The route target, the banner state and the health check of the two reads are registered here | referred to; the consuming story carries the dependency H RWB-PLT-N001-CON |

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-access/` | Chart with deployment, service, pre-deploy migration job invocation, config map, secret references, probes and the route registration |
| `helm/rwb-access/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, the `rwb.access.access-log` switch, alert thresholds, environment name |
| Pipeline stage | Build, unit and contract tests, image and dependency scan, chart publish, promote the same artefact |
| Provisioning and ACL step | `rwb.access.events.v1` with retry and `.dlt`, producer rights on `rwb.decision-record.v1` and its retry path, no consumer group |
| Dashboards | Entries written, refused and failed; grant activations, ends and the active count; outbox lag; ledger lag |
| Alerts | Six rules, each with a message id, a route and one runbook entry |
| Runbook | Six entries, each with the check, the owner role, the recovery step and the message id |

**Probes.** Readiness answers healthy only when the migration is at the expected schema version, the outbox relay is running and the worker has polled; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database or to the log. Exact paths and timings are values.

**Migration job.** Invokes the per-service Flyway sequence of RWB-P4-E1039-DB with the rwb-access login as a pre-deploy job with a backoff limit; a failed job blocks the rollout and the release, and this story owns no statement of the migration.

**Alert mapping carried from the legacy story.**

| Message ID | Condition | Alert | Route |
|---|---|---|---|
| MSG-P7-003 | An access-log entry cannot be written; the read was refused | Failed-write alert with the operation and the trace id, page | Platform on-call queue |
| MSG-P4-002 | An admin read is refused for want of a right | Refused-write count on the dashboard, no page | No route |
| MSG-P4-004 | A break-glass grant is activated | Activation alert with the grant id, the incident and the end time, ticket | Security administrator queue |
| MSG-P4-007 | A break-glass request is refused for want of an approval or a membership | Refused-grant alert with the reason code NO_BREAKGLASS_GRANT, ticket | Security administrator queue |
| None | The outbox relay or the ledger falls behind the lag window | Lag alert naming the topic and the delay | Platform on-call queue, no page below the window |
| None | The migration job or a probe fails | Release-failure alert naming the version | Platform on-call queue, page |

**Done when.** The chart renders in all three environments, the pipeline promotes one artefact, the probes answer without a write, the two topics and their retry and `.dlt` paths are verified by a test, the ACL set is exactly WRITE and DESCRIBE on the two topics with no READ on the decision topic, the six alerts fire on synthetic conditions with their message ids, the runbook entries are reviewed by the on-call rota, and the security administrator has accepted the break-glass route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | An access-log entry cannot be written and the read is refused | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | An admin read or write is refused for want of a right | You cannot {action} here. Your role does not include it. |
| MSG-P4-004 | A break-glass grant is activated; the banner and the activation alert | Emergency access is on until {time}. Every action is recorded. |
| MSG-P4-007 | A break-glass request is refused | Emergency access needs an approved break-glass request in the bank IAM with an open incident. |

The texts are copied unchanged from the legacy story; the deployment adds the alert routing and the runbook link, never a new wording and never a new message id. An alert payload carries the message id, the operation, the grant or incident id and the trace id, and **no personal value**: the case id of an entry is an identifier and the actor is a staff user reference.

### 15. Screens and states

The deployment serves the banner of the ACE front-end shell (break-glass active, with the end time) and the access-log and grant panels of SCR-43 Roles and access, behind the gateway-bff composite route (DP-19). The operator-facing surfaces of this story are the pipeline run view, the release view, the dashboards, the alert queue and the run book. The composite route specification and the screen field list belong to RWB-PLT-N001-CON and to the Epic 8 screen work; the deployment registers the route target and the health check of the two reads only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-039-OPS-01 | AC1 | NFR | The chart renders for DEV, SIT and UAT with a pinned digest, the login reference, the migration job and the two probes |
| TC-E1-039-OPS-02 | AC2 | NFR | One pipeline run produces one image and one chart version and fails on a contract drift or a critical scan finding |
| TC-E1-039-OPS-03 | AC3 | NFR | The two topics with retry and `.dlt`, the ACL list per principal, and the refusal of a READ on `rwb.decision-record.v1` |
| TC-E1-039-OPS-04 | AC4 | NFR | The three secret references mounted from the store, and the scan for a value in a values file, a template or the run book |
| TC-E1-039-OPS-05 | AC5 | NFR | Six synthetic conditions raise the six mapped alerts with the legacy text and one runbook entry each, routed to the two queues |
| TC-E1-039-OPS-06 | AC6 | NFR | The six runbook entries reviewed, each with the check, the owner role, the recovery step and the message id |

### 17. Guardrails

- No business value in a values file: the window, the incident pattern, the reason bounds, the review window and the event codes are parameters and reference data, never a deployment value (BR5, BR10).
- No personal data in logs, dashboard series, alert payloads or the run book: identifiers, references, codes, counts and durations only.
- One login per service; the chart carries the rwb-access login reference and no other service's credential (DP-02, BR1).
- The service writes only `rwb_access`; the migration job is invoked, never edited, and this story provisions no database object (BR2).
- Every topic has a retry topic and a `.dlt` topic, and the shared decision topic is reused and never recreated (BR3).
- The service identity has no read on the decision topic and no ACL on another service's business topic (BR4).
- No secret is written into a values file, a chart template, a dashboard, an alert payload or the run book; all secrets come from the platform secret store (BR9).
- An alert never changes a rule: it points at the parameter row and at the runbook entry, and a business person changes the value without a release.
- The release pins the image digest and the chart version; a rebuild between environments is not allowed.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-ACA-006 | Every read of the case store and the document store written to the access log | The producer ACL on `rwb.decision-record.v1`, the outbox lag panel and the MSG-P7-003 failed-write alert | TC-E1-039-OPS-03, TC-E1-039-OPS-05 |
| REQ-ACA-008 | Break-glass with its own approval, written to the access log | The grant activation and refused-grant alerts routed to the security administrator queue, and the runbook entries of the grant | TC-E1-039-OPS-05, TC-E1-039-OPS-06 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P4-E1039-APP | App development | X dependency tracked: the writer, the grant and the read this deployment runs |
| RWB-P4-E1039-CON | Contract | Sibling: the operations, the vocabulary and the fakes this deployment registers and alerts on |
| RWB-P4-E1039-DB | ACE DB | X dependency tracked: the migration job this chart invokes and the four tables it creates |
| RWB-PLT-EVT, RWB-PLT-TE006-CON | Contract | The topic provisioning, the retry and `.dlt` rule and the outbox and inbox library |
| RWB-PLT-OBS | Platform | The dashboards, the alert route and the trace identifier the alerts carry |
| RWB-P5-E1039-APP | App development | Neighbour of the same legacy key on the document side: its entries arrive on the same shared topic |
| RWB-P7-E1039-APP | App development | Neighbour of the same legacy key on the ledger side: consumes the decision topic and answers the query this deployment does not host |
| RWB-ITG-E1039-ITG | Integration | The end-to-end proof that runs against this deployment |

The legacy test cases of this key — TC-E1-039-01, TC-E1-039-02, TC-E1-039-03, TC-E1-039-04, TC-E1-039-05, TC-E1-039-06, TC-E1-039-07, TC-E1-039-08, TC-E1-039-09, TC-E1-039-10, TC-E1-039-11 and TC-E1-039-12 — are executed by RWB-P4-E1039-APP and, as the cross-service copy, by RWB-ITG-E1039-ITG; this story proves the environment in which they run.

### 19. Out of scope

- The application code of the writer, the grant and the read (RWB-P4-E1039-APP).
- The contract documents and the fakes as published artefacts (RWB-P4-E1039-CON); this story only deploys the test copies.
- The schema, the four tables, the grants, the partitions and the retention action (RWB-P4-E1039-DB); this story provisions no database object.
- The platform topic provisioning implementation, the Kafka cluster, the Temporal cluster and the secret store themselves (the platform epics).
- The exact cluster topology, node pools, replica counts, resource sizes and probe timings (GAP-0783).
- The alert thresholds and the lag window as business values; they are values with a parameter row behind them (GAP-0783).
- The access review list and its Schedule (RWB-P4-AD008-APP), and the unreviewed-use escalation to the head of SCB IT security and Compliance (Epic 8, FEAT-ADM-12).
- The screen SCR-43 Roles and access and the composite route specification (RWB-PLT-N001-CON and the Epic 8 screen work).
- The central ledger deployment, its ingest, its seal and its chain check (P7 rwb-decision and the platform).
- The cross-service journey harness and its evidence (RWB-ITG-E1039-ITG).
