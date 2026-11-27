# RWB-P6-E2018-OPS E-signature flow for customers and the bank

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E2018-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP05, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P6-N |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P6-E2018-OPS-16) |
| Depends on (build) | None |
| Contract dependencies | Not specified in the source documents (DOR-RWB-P6-E2018-OPS-21): no contract story is recorded; the rwb-treatment contract on /api/recovery/treatment/v1 is not in the plan (GAP-1183); DP-07 reference-data contract RWB-P3-E1043-CON; section 12.1 is the contract baseline for the three signature-request operations (GAP-1184) |
| Contract version | Not specified in the source documents (DOR-RWB-P6-E2018-OPS-23); the path is /v1 |
| Fake library version | Not specified in the source documents (DOR-RWB-P6-E2018-OPS-22) |
| Integration dependencies | None |
| External dependencies | None |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-P6-E2018-OPS-14): no signed epic design is recorded; the sign-off is to be confirmed against the epic design record |
| SIT harness, test tenant and evidence | Not specified in the source documents (GAP-0402): the EasyApp test tenant and route through INT-34, the harness environment, seeding, evidence format and gate wording agreement by the owner role is pending |
| Signature ownership split | rwb-document owns the signature request, its statuses and the signed version; rwb-comms owns the basis and the circuit; rwb-treatment owns the treatment, its signature record and the closure of its own window; the reconciling operation and the two events are Not specified in the source documents (GAP-2701) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (FR-P6-032, FR-P6-033, FR-P6-034) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-018 for rwb-comms. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P6-E2018-OPS). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 24 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform engineer**, I want **the e-signature capability of rwb-comms deployed from the service template with its Helm values and its own login, the per-service Flyway migration job, the egress to EasyApp through the ACE common module path with the certificate and the endpoint as secret references, the consumer groups of the consumed topics with their retry and `.dlt` paths around the platform relay JOB-11, the dashboards, the alerts on a stuck send and on a result that never arrives, a runbook for the five failures an operator meets, a SIT smoke profile against the fakes, the feature switch and the rollback**, so that **an operator can see within minutes that a signature request is not leaving, that a result has stopped coming back, or that the exception queue is growing, and repair it without reading code or waiting for a business report**.

This story deploys an existing capability. It builds no endpoint, no table, no topic and no workflow: the three operations are those of `RWB-P6-E2018-APP`, the request state is P5 rwb-document's, the send's durability is the outbox row in schema `rwb_comms`, and the every-minute retry is the platform outbox relay JOB-11.

### 2. Business rationale

The legacy capability leaned on one Quartz job and one exception log for two very different failures. A send that the ACE path never accepted and a signed result that never came back looked the same from operations: nothing on the job record, nothing on the case and a customer who had signed but whose case still waited. In the target the retry is the platform relay (Architecture v5 slide 44, JOB-11, every minute, every service), so the operational signal has to move from "did the job run" to "is a request leaving, is a result coming back, and is the exception queue growing".

There is a second operational fact that only deployment can carry: the e-signature is the one capability of rwb-comms whose failure reaches the customer outside the bank and whose completion changes a legal position. EasyApp is reached only through the ACE common module e-signature path (INT-34, Architecture v5 slide 7), and that egress needs an endpoint and a certificate the platform secret store holds and the chart only references (NFR-052). An operator who cannot see whether the egress is up will read the exception queue as a business problem.

Deployment is therefore part of the capability: the chart carries the rwb-comms login and no other credential (DP-02), the migration job runs the per-service Flyway sequence in schema `rwb_comms` (DP-15) and creates no signature table, because `signature_request` is P5 rwb-document's (GAP-1181; ASM-2128), the consumer groups are provisioned with retry and `.dlt` paths so a contact stop is never missed (DP-09), and the runbook names the five failures an operator will actually see.

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The Kafka event platform provisions topics with a retry topic and a `.dlt` topic (RWB-PLT-EVT, RWB-PLT-TE006-CON), and `rwb.case.events.v1`, `rwb.deviation.events.v1` and `rwb.treatment.events.v1` are provisioned by their owners.
- The observability stack of the platform is available (RWB-PLT-OBS, ADR-023): metrics, traces and logs with one trace across REST, Kafka and the outbound call.
- The three environments DEV, SIT and UAT exist with their parameter scope, their Kafka and Temporal endpoints and their egress rules to the ACE common module path.
- `RWB-P6-E2018-APP` is delivered, so the three operations, the outbox row, the result handling and the exception state exist to be deployed and observed.
- The ACE common module e-signature path's endpoint, its client certificate and the secret names that hold them are Not specified in the source documents (GAP-1187; ASM-2134); the chart references them as secret references until the path owner and the platform security team fix the names.
- The signed PDF object store behind the P5 version add is P5's and is Not specified in the source documents (GAP-1186; ASM-2133); no dashboard panel and no alert payload carries a byte or a storage reference of a signed copy.
- The retry limit of 5, the exception-queue rule R-UNI-34 and the 60-second signed-copy target are service configuration of rwb-comms, not deployment values of the chart.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The pipeline builds one image and one chart version from the same commit, runs the unit, component and contract tests, scans the image and the dependencies, and publishes the chart.
2. The chart deploys rwb-comms with the rwb-comms login, the pre-deploy migration job for schema `rwb_comms`, the readiness and liveness probes and the api deployment that serves the three operations.
3. The migration job runs the per-service Flyway sequence and creates the `rwb_comms` objects the capability reads and the library objects it writes - `template`, `merge_field`, `notice`, `outbox_event`, `processed_event` and `idempotency_key` - and creates no signature table (DP-15, DP-01).
4. The egress step declares one outbound route to the ACE common module e-signature path (INT-34), with the client certificate, the trust material and the endpoint as secret references resolved at deploy time; no chart value, values file or runbook holds a literal endpoint, certificate or secret (NFR-052).
5. The provisioning step declares one consumer group `rwb-comms` on `rwb.case.events.v1`, `rwb.deviation.events.v1` and `rwb.treatment.events.v1`, each with its retry topic and its `.dlt` topic, and confirms that the relay window of JOB-11 drains the outbox rows of `rwb_comms` without a new Schedule.
6. The dashboards are published: requests by status, queued sends and queue depth, time to an accepted reference, result latency, expiry count, exception count, egress error rate, the MSG-GEN-006 rate and the refused counts.
7. The alerts are wired to the message IDs of section 14 and to the runbook entries of section 13; the thresholds and the evaluation windows are values of the release, not template constants.
8. A smoke step runs one e-signature journey for a synthetic case against the fakes and the SIT profile: create the request for the agreement, exercise the relay window, drive a `SIGNED` result and a `SIGNED` version 2 with write_once true, drive a `DECLINED` result, hold an unknown reference, and assert the exception state at attempt 5.
9. The runbook is published and reviewed with the on-call rota: a stuck send, an egress that is down, a result that never arrives, an unknown reference held on the exception queue, and an exception queue that grows.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The migration job fails | The deployment stays unready and the pipeline stops; no traffic reaches the new version | None | AC1 |
| X2 | The egress route or the certificate reference is missing | The release fails the egress check and the send answers 503 on its first attempt; the egress-down runbook entry starts | MSG-GEN-006 | AC2 |
| X3 | A consumer group is provisioned without its retry or `.dlt` topic | The provisioning step fails the release and the consumer refuses to start | None | AC3 |
| X4 | A release declares a Schedule for the retry or creates a topic for the capability | The retired-element check fails the release | None | AC3 |
| X5 | The attempt count of a send reaches the limit of 5 | The send moves to the exception state and the attempt-limit alert fires | None | AC5 |
| X6 | The result of an accepted request never arrives | The result-latency alert fires and the missing-result runbook entry names the reference | None | AC5, AC6 |
| X7 | An unknown reference is held on the exception queue | The exception count rises and the unknown-reference runbook entry names the check | None | AC4, AC6 |
| X8 | The feature switch is off in an environment | The send is refused closed with MSG-GEN-006 and nothing leaves; the refusal is counted, not paged | MSG-GEN-006 | AC8 |
| X9 | A rollback is ordered | The previous chart version is redeployed and the migration is reversed by its own script; the outbox rows are left for the earlier version to drain | None | AC8 |
| X10 | A refused send is counted as a failure | The refused count is a separate series and never opens a release incident | MSG-P4-002, MSG-P6-009, MSG-P6-001 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the platform topic provisioning, the secret store and the observability stack; builds no application code |
| Negotiable | Replica counts, resource sizes, alert thresholds and retention are environment values, not story decisions |
| Valuable | Makes an outbound capability observable: a request that does not leave, a result that does not return and a queue that grows each have a signal and an owner |
| Estimable | One chart, one pipeline stage, one migration job, two probes, three subscriptions, the egress step, eight dashboard panels, five alert rules and five runbook entries |
| Small | Fits one sprint with the runbook |
| Testable | Every criterion tests an artefact: the chart renders, the egress check passes, the groups exist, the panels carry data, the alerts fire on a synthetic metric, the runbook entry resolves |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the e-signature flow for customers and the bank

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the target environment is SIT

  Scenario: AC1 The Helm chart and values deploy rwb-comms with its own login and the per-service migration (new, D-RCV-60)
    Given the rwb-comms Helm chart and its values-dev.yaml, values-sit.yaml and values-uat.yaml
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the release declares the rwb-comms login reference and no other service's credential
    Then the migration job runs the per-service Flyway sequence in schema rwb_comms before the deployment is marked ready, creating template, merge_field and notice with the outbox, inbox and idempotency objects, and creating no signature table
    Then the readiness probe answers healthy only when the schema is at the expected version and the consumer group is subscribed
    Then no replica count, resource size, timeout, threshold or cadence is hard-coded in the template

  Scenario: AC2 The egress to EasyApp runs through the ACE common module path with referenced credentials (new, D-RCV-60)
    Given the egress step of the release
    When it is rendered for each environment
    Then the release declares one outbound route to the ACE common module e-signature path (INT-34) and no route to EasyApp directly
    Then the client certificate, the trust material and the endpoint are secret references resolved at deploy time, and no values file, chart template or runbook holds a literal endpoint, certificate or secret
    Then the egress check fails the release when the route or the certificate reference is missing, and the send answers 503 with MSG-GEN-006 on its first attempt
    Then the concrete endpoint, the certificate issuer and the secret names are Not specified in the source documents (GAP-1187; ASM-2134)

  Scenario: AC3 The subscriptions carry retry and .dlt and the retry is the platform relay JOB-11 (new, D-RCV-60)
    Given the outbox rows of schema rwb_comms and the platform relay of JOB-11
    When the release is deployed and the provisioning step runs
    Then the send request is picked up by the every-minute relay window and executed by the rwb-comms sender, and no Temporal Schedule, cron entry or job row is registered by this release
    Then one consumer group rwb-comms subscribes to rwb.case.events.v1 for CaseStateChanged, rwb.deviation.events.v1 for DeviationRaised and DeviationCleared, and rwb.treatment.events.v1 for TreatmentApproved, each with its retry topic and its .dlt topic, and the consumer never acknowledges an event it could not process
    Then rwb.decision-record.v1 is produced to as its owner provisions it and is not recreated, and no new topic is created for this capability
    Then the provisioning step fails the release when a retry or .dlt topic is missing, and the retired-element check fails a release that declares a Schedule for the retry or a topic of its own

  Scenario: AC4 The dashboards carry the request, send and result series (new, D-RCV-60)
    Given the published dashboard
    When a synthetic day is replayed with requests by status, a queued send, a signed result, a declined result, an expiry, an unknown reference and five sends that reached the limit
    Then the panels show requests by status, queued sends and queue depth, time to an accepted reference, result latency, the expiry count, the exception count and the egress error rate
    Then every panel names its service, its environment and its business date
    Then a refused send is counted on its own series and never opens a release incident
    Then no panel carries a signed PDF byte, a storage reference, a party identity or an account number, only references and counts

  Scenario: AC5 The alerts fire on a stuck send and on a result that never arrives (new, D-RCV-60)
    Given the published alert rules and the message IDs of section 14
    When the attempt count of one send reaches the retry limit of 5, the egress answers 503 on a share of sends, an accepted reference has no result inside its window, and the exception count passes its value
    Then each condition has exactly one alert with the environment, the channel or operation, the reference and the age of the oldest affected row
    Then the attempt-limit alert links the stuck-send runbook entry and names the ACE common module path owner as the second-line contact
    Then the alerts do not fire on a first attempt, and the refused and switch-off counts never page
    Then the threshold and the evaluation window of every alert are values of the release with provisional defaults recorded in the runbook

  Scenario: AC6 The runbook covers a stuck send, a down egress, a missing result, an unknown reference and a growing exception queue (new, D-RCV-60)
    Given the published runbook and the alert rules
    When a send sits in the queued state beyond its window, the egress answers 503, an accepted reference has no result, a result names a reference no request holds, or the exception count passes its value
    Then each of the five conditions has one runbook entry with the check, the owner role and the recovery step
    Then the stuck-send entry names the outbox row, the attempt count, the last error and the external reference, and the step that is safe to repeat
    Then the missing-result entry names the external reference and states that a resend uses a new Idempotency-Key only after the first reference is confirmed lost
    Then the unknown-reference entry names the read by external reference on the rwb-document contract and the exception queue, and creates no request
    Then every alert links exactly one runbook entry and every entry names the escalation path when the step fails

  Scenario: AC7 The SIT smoke profile runs the journey against the fakes (new, D-RCV-60)
    Given the SIT smoke profile with the fakes of section 12.8
    When the smoke step runs on the release build
    Then it creates a signature request for document "D-0601" of treatment "T-0501" for party "P-0088" against the rwb-document and rwb-treatment fakes and asserts the 201 answer and the request status
    Then it asserts the outbox row, the relay window and the accepted external reference, and it asserts version 2 of "D-0601" with write_once true inside the 60-second target
    Then it drives a DECLINED result, an unknown reference "EA-99999", a wet ink refusal with MSG-P6-009 and the attempt path to the retry limit of 5 with the egress fake answering unavailable
    Then it asserts that no signed PDF byte, party identity or document body appears in a log line or a metric label

  Scenario: AC8 The feature switch and the rollback are safe (new, D-RCV-60)
    Given the feature switch rwb.comms.esign in the values files
    When the switch is off in an environment and a signature request is made
    Then the send is refused closed with MSG-GEN-006, nothing leaves for the ACE common module path and the refusal is counted on its own series
    When a rollback is ordered
    Then the previous chart version and its image digest are redeployed, the migration is reversed by its own script, and the outbox rows are left for the earlier version to drain without a duplicate send or a duplicate signature record
    Then the rollback is rehearsed once in SIT and the rehearsal is recorded in the runbook
```

These eight criteria are new for the deployment and test artefacts only; they restate no business outcome owned by RWB-P6-E2018-APP.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | A customer signs electronically only where the template's signature basis allows it, and by wet ink where Legal requires it; the deployment seeds no basis | REQ-OCC-009; DF-REF-068 | AC7; TC-E2-018-01, TC-E2-018-03, TC-E2-018-04 |
| BR2 | No signature request leaves while a contact stop or a legal hold applies; the deployment holds no copy of either | CTL-16; R-SET-12; R-UNI-20 | AC7; TC-E2-018-07 |
| BR3 | A system that is unavailable queues the send and retries; after the retry limit of 5 the send moves to the exception queue and the attempt-limit alert fires | R-UNI-33, R-UNI-34 | AC5, AC6; TC-E2-018-08 |
| BR4 | The same result twice has one effect; a resend after a lost reference uses a new Idempotency-Key only when the first is confirmed lost | R-UNI-40 | AC9; TC-E2-018-09 |
| BR5 | The signed copy is write-once on the case and is stored only through the P5 contract; the deployment stores no signed PDF | CTL-12; DT06; DP-01 | AC7; TC-E2-018-01 |
| BR6 | One service, one schema, one login: the release uses the rwb-comms login and no other service's credential | DP-02; Architecture v5 slide 41 | AC1; TC-E2-018-01 |
| BR7 | The migration is a per-service Flyway sequence in schema rwb_comms and runs before the deployment is ready; it creates no signature table | DP-15; GAP-1181 | AC1; TC-E2-018-01 |
| BR8 | Every subscription has a retry topic and a `.dlt` topic, and a consumer never acknowledges an event it could not process | DP-09; Architecture v5 slide 22 notes | AC3; TC-E2-018-08 |
| BR9 | No Schedule and no new topic is created for this capability: the retry is the platform relay JOB-11 and the topics belong to their owners | DP-10; Architecture v5 slide 44 | AC3; TC-E2-018-01 |
| BR10 | No literal endpoint, certificate or secret is written into a values file, a chart template, a dashboard or the runbook; the chart carries references only | NFR-052; TSD P6 T7 | AC2; TC-E2-018-02 |
| BR11 | No environment value is hard-coded: replica counts, resource sizes, timeouts, thresholds and the retry limit are values or service configuration | Template and Rules §R7.2 s17 | AC1; TC-E2-018-01 |
| BR12 | An alert carries a message ID where the condition maps to one, and links one runbook entry | Template and Rules §R7.2 s14 | AC5; TC-E2-018-08 |
| BR13 | No dashboard series, log line, alert payload or runbook entry carries a signed PDF byte, a party identity, an account number or a document body; references and counts only | Template and Rules §R7.2 s17; legacy section 17 | AC4, AC7; TC-E2-018-01 |
| BR14 | No comms event is created by this release: the signature result is read from the rwb-document contract and the decision record goes on the shared topic | DP-09; GAP-1185 | AC3; TC-E2-018-08 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart, the migration job and the egress check pass the pipeline | Deploying |
| Deploying | Migration complete and probes healthy | The schema is at the expected version and the consumer is subscribed | Ready |
| Ready | Release superseded | A new chart version is promoted | Rolling |
| Rolling | All pods on the new version | The old ReplicaSet drains | Ready |
| Ready | Egress check failed | The route or the certificate reference is missing | Failed |
| Failed | Rollback | The previous chart version is redeployed and the migration is reversed by its own script | Ready |

The request lifecycle - QUEUED, SENT, SIGNED, DECLINED, EXPIRED - is the capability's own and is described in RWB-P6-E2018-APP; the request row itself is P5 rwb-document's. This story observes it and changes no state of it.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the egress step, the provisioning step, the dashboards, the alerts and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the topic provisioning and the platform relay window |
| Platform security team | Owns the client certificate and the secret material of the egress, and approves the reference the chart carries |
| ACE database administrator | Owns schema rwb_comms, the login and its grants, and approves the migration job |
| Release manager | Approves the promotion of one artefact through the environments and the rollback rehearsal |
| On-call operator | Runs the runbook entries and opens an incident when a send is stuck, a result is missing or the exception queue grows beyond its value |
| ACE common module path owner | Is paged by the egress-down and missing-result alerts and owns the repair beyond the rwb-comms breaker |
| RW-PLATADM, platform administrator | Reads the exception queue in the running service, not in the cluster |

The per-service login name and the egress certificate and secret names used by the chart are secret references resolved at deploy time; the chart references "the rwb-comms login (DP-02)" and the egress material by reference, never by literal value.

### 11. Data

| Item | Content | BR Field ID |
|---|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, the feature switch `rwb.comms.esign`, the client and egress timeouts, the alert thresholds | Not specified in the source documents (DOR-RWB-P6-E2018-OPS-7) |
| Schema | rwb_comms, migrated by the per-service Flyway sequence; the tables template, merge_field and notice with the library objects outbox_event, processed_event and idempotency_key, and no signature table | Not specified in the source documents (DOR-RWB-P6-E2018-OPS-7) |
| Topics | `rwb.case.events.v1` subscribes CaseStateChanged; `rwb.deviation.events.v1` subscribes DeviationRaised and DeviationCleared; `rwb.treatment.events.v1` subscribes TreatmentApproved; `rwb.decision-record.v1` is produced to as its owner provisions it; `rwb.comms.events.v1` is not created or extended by this capability | Not specified in the source documents (DOR-RWB-P6-E2018-OPS-7) |
| Egress | One outbound route to the ACE common module e-signature path (INT-34), with the client certificate, the trust material and the endpoint as secret references | Not specified in the source documents (DOR-RWB-P6-E2018-OPS-7) |
| Dashboard series | requests by status, queued sends and queue depth, time to an accepted reference, result latency, expiry count, exception count, attempt distribution up to 5, egress error rate, MSG-GEN-006 rate, refused counts, consumer lag | Not specified in the source documents (DOR-RWB-P6-E2018-OPS-7) |
| Runbook entries | stuck send, egress down, result never arrives, unknown reference, exception queue grows | Not specified in the source documents (DOR-RWB-P6-E2018-OPS-7) |
| Secrets | The rwb-comms login secret, the Kafka client credential, the egress client certificate and the endpoint, all from the platform secret store | Not specified in the source documents (DOR-RWB-P6-E2018-OPS-7) |

The egress endpoint, the certificate issuer and the secret names are Not specified in the source documents (GAP-1187; ASM-2134), and the signed PDF object store is P5's and is Not specified here (GAP-1186; ASM-2133). The exact cluster topology, node pools, replica counts and probe timings are deployment values of the platform chart and are not fixed here. The retry limit of 5 and the exception-queue rule are service configuration of rwb-comms, not chart values.

### 12. Contract

#### 12.1 REST operations provided

None new. The deployment exposes the three operations of the app story behind gateway-bff: `POST /api/recovery/comms/v1/treatments/{treatmentId}/signature-requests`, `GET /api/recovery/comms/v1/treatments/{treatmentId}/signature-requests` and `POST /api/recovery/comms/v1/signature-requests/{requestId}/result`, owner rwb-comms (P6), API-P6-009, API-P6-010 and API-P6-011, with the `SignatureRequest` answer and the Idempotency-Key header. The probes are cluster-internal and are not part of the API surface.

#### 12.2 REST operations consumed

None by the deployment. The outbound call of the capability is not a REST operation of a service in this workspace: it is the ACE common module e-signature path (INT-34), whose request and result shapes, endpoint and certificate are Not specified in the source documents (GAP-1187; ASM-2134). Its endpoint and certificate are the secret references of AC2, and the deployment adds no consumer of the P5 document contract, the rwb-treatment contract or the reference-data contract: those are the app story's and are faked for the smoke profile.

#### 12.3 Events published

None. This capability publishes no comms event - Architecture v5 slide 42 names only `NoticeGenerated`, `NoticeDispatched` and `NoticeDelivered` on `rwb.comms.events.v1` and a signature is not a notice (GAP-1185; ASM-2132) - and its one relayed element is `rwb.decision-record.DecisionRecorded.v1` on the shared topic `rwb.decision-record.v1`, written by the local library and provisioned by its owner, a library that the plan build list does not carry (GAP-1196; ASM-2143). This deployment creates no topic and publishes no comms event.

#### 12.4 Events consumed

| Event | Topic | Owner | Group |
|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` (event 05) | `rwb.case.events.v1` | P3 rwb-case | rwb-comms |
| `rwb.deviation.DeviationRaised.v1` (event 06) | `rwb.deviation.events.v1` | S8 rwb-deviation | rwb-comms |
| `rwb.deviation.DeviationCleared.v1` (event 07) | `rwb.deviation.events.v1` | S8 rwb-deviation | rwb-comms |
| `rwb.treatment.TreatmentApproved.v1` (event 10) | `rwb.treatment.events.v1` | S2 rwb-treatment | rwb-comms |

The four events on three topics are consumed by one group `rwb-comms` with the inbox of schema `rwb_comms`, each with its retry topic and its `.dlt` topic (DP-09).

#### 12.5 Workflows and activities

None. The retry worker of this capability is not a Temporal workflow: it is the platform relay window of JOB-11 calling the rwb-comms sender, plus the result handling in the service. No worker deployment polls a task queue for this capability, and no activity is registered on `rwb-comms`.

#### 12.6 Schedules

None. JOB-11 Outbox sender is the platform's outbox relay, every minute, with every service as its owner (Architecture v5 slide 44); this release registers no Schedule and no cron entry, and the retry limit of 5 is applied inside the send attempt rather than by a scheduler (DP-10).

#### 12.7 Tables owned

None new. The migration job creates and migrates the tables of `rwb_comms` - template, merge_field, notice, outbox_event, processed_event and idempotency_key - and touches no other schema (DP-01). `signature_request` and `document` stay with P5, `treatment` with S2, `recovery_case` with P3, `deviation` with S8 and `decision_log_entry` with P7; no dashboard query reads any of them and no signature table is created (GAP-1181).

#### 12.8 Contract fakes

| Fake | Deployment use |
|---|---|
| rwb-document WireMock | Runs in the pipeline and in the SIT smoke profile: the created request, the read by external reference for `EA-30001` and for `EA-99999`, the update, and the version add answering version 2 of `D-0601` with write_once true |
| rwb-treatment WireMock | Same profile: treatment `T-0501` with offer validity 2026-12-20 and state OFFER_WITH_CUSTOMER_SET, and the signature record answering accepted for signed true and signed false |
| rwb-deviation WireMock | Same profile: the open deviation `X2` with contact stop on and an empty answer |
| rwb-case WireMock | Same profile: legal hold false and true, and a delayed answer beyond 2 s |
| ACE common module e-signature path stub (INT-34) | An accepted reference, a `SIGNED` result with a synthetic signed PDF, a `DECLINED` result and an `unavailable` answer for six attempts |

The fakes are test-only workloads; they are not deployed into UAT or production, and each is replaced by the real owner as its story lands. The concrete path shape, endpoint and certificate are Not specified in the source documents (GAP-1187; ASM-2134).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 1 consumed outside the workspace | The three signature-request operations provided; the outbound call to the ACE common module e-signature path (INT-34); one hop, 2 s |
| Kafka | 1 produced to a shared topic, 4 consumed | `DecisionRecorded` on `rwb.decision-record.v1` reused; `CaseStateChanged`, `DeviationRaised`, `DeviationCleared` and `TreatmentApproved` consumed with retry and `.dlt` |
| Temporal | None | No workflow, no activity and no Schedule; the retry is the platform relay JOB-11 |
| File | None | The release reads no runtime file; values files and chart templates are build inputs |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_comms`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/comms/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-10 is claimed only for the relay dependency: no Schedule is registered by this release. DP-05 applies as a prohibition: no dashboard and no smoke step reads an ACE view. DP-13 adds nothing to the deployment beyond the base the chart exposes.

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-comms/` | Chart with the api deployment, service, migration job, config map, secret references and probes |
| `helm/rwb-comms/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, `rwb.comms.esign`, the client and egress timeouts, the alert thresholds |
| Egress step | One outbound route to the ACE common module e-signature path (INT-34), the client certificate and endpoint references, and the check that fails the release when either is missing |
| Pipeline stage | Build, unit, component and contract tests, retired-element check, egress check, image and dependency scan, chart publish, promote the same artefact |
| Provisioning step | Consumer group `rwb-comms` on `rwb.case.events.v1`, `rwb.deviation.events.v1` and `rwb.treatment.events.v1` with retry and `.dlt`; reuse of `rwb.decision-record.v1`; confirmation that the relay window of JOB-11 drains `rwb_comms` |
| Dashboards | Eight panels: requests by status; queued sends and queue depth; time to an accepted reference; result latency; expiry count; exception count; attempt distribution up to 5; egress error rate, MSG-GEN-006 rate and refused counts |
| Alerts | Five rules, each with a message ID where one applies and one runbook entry |
| Runbook | Five entries: stuck send, egress down, result never arrives, unknown reference, exception queue grows |

**Probes.** Readiness answers healthy only when the migration is at the expected schema version and the consumer group is subscribed; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database, calls another service or calls the ACE common module path.

**Alert mapping.**

| Message ID | Condition | Alert | Route |
|---|---|---|---|
| None | The attempt count of a send reaches 5 and the row moves to the exception state | Attempt-limit alert with the operation, the attempt count, the external reference and the age of the oldest affected row | Platform on-call, ticket to the ACE common module path owner |
| MSG-GEN-006 | The egress answers 503 or the path is unavailable on a share of sends | Egress error-rate alert with the breaker state and the environment | Platform on-call, page, ACE common module path owner |
| None | An accepted reference has no result inside the result window | Result-latency alert with the reference and the oldest affected request | Platform on-call, ticket |
| None | The exception count passes its value | Exception-queue alert with the count and its change against the trailing hour | Platform on-call, page |
| MSG-P4-002, MSG-P6-009 and MSG-P6-001 | A send is refused for want of a right, a wet ink basis or a contact stop | Refused count on the dashboard | No page |
| MSG-GEN-006 | The feature switch is off and the send is refused closed | Switch-off count on the dashboard | No page |

Every alert carries its message ID where the condition maps to one, and the conditions without a message ID carry the series name instead. The threshold, the result window and the evaluation window of every alert are set in the values file by the release manager and recorded in the runbook; no source document fixes them.

**Done when.** The chart renders in all three environments, the pipeline promotes one artefact and fails on a fake drift, a missing retry topic, a missing egress reference or a retired element, the three subscriptions exist with their retry and `.dlt` paths, the eight panels carry the synthetic day, the five alert conditions fire on synthetic metrics, the smoke profile passes against the fakes with no personal data or signed PDF content in a log line or a metric label, and the five runbook entries are reviewed by the on-call rota.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-009 | E-signature asked for a document that needs wet ink | Legal requires a wet ink signature for {document}. Use the branch or paper path. |
| MSG-P6-001 | A contact stop is in force | Contact with this customer is stopped for {reason}. |
| MSG-P3-004 | A legal hold is on the case | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-GEN-006 | The ACE path to EasyApp is unavailable, the egress is down, or the switch is off | {system} is not available. Your request is queued and will be retried. |
| MSG-GEN-001 | A branch or paper result has no scan | Enter {field}. |
| MSG-P3-005 | The request is not open, or the treatment is not with the customer | This case cannot move to {state} from {current}. |
| MSG-P4-002 | Not specified in the source documents (DOR-RWB-P6-E2018-OPS-9) | Not specified in the source documents (DOR-RWB-P6-E2018-OPS-9) |

The message texts are copied unchanged from the legacy story and the deployment adds the routing, the threshold and the runbook link, never a new wording. The {system} of MSG-GEN-006 is the name of the system that failed - `EasyApp` or the name of the consumed service.

### 15. Screens and states

The deployment serves SCR-14 Treatment record with the Send for signature action, the method choice and the request list with its status, SCR-30 Case documents with the signed copy linked to the generated agreement, and SCR-09 Exception queue with the held results and the sends in the exception state, all through gateway-bff composite routes (DP-19). The operator-facing surfaces of this story are the pipeline run view, the release view, the egress check result, the eight dashboard panels and the runbook; the smoke step runs one signature journey for a synthetic case in SIT and asserts the create, the relay window, the signed version, the decline, the unknown reference and the exception state at attempt 5.

Screen states (source: Screen Specifications v1). SCR-14: empty, loading, error and no access are Not specified in the source documents (CG-ALL-6534). SCR-30: loading is in Screen Specifications v1; empty, error and no access are Not specified in the source documents (CG-ALL-6535). SCR-09: loading is in Screen Specifications v1; empty, error and no access are Not specified in the source documents (CG-ALL-6533).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-018-01 | AC1, AC3, AC7 | NFR | T-0501 settlement; D-0601 E_SIGNATURE_ALLOWED; path stub SIGNED; version 2 write_once inside 60 seconds |
| TC-E2-018-02 | AC2 | NFR | Branch scan D-0602; the result operation in the smoke profile |
| TC-E2-018-03 | AC3 | NFR | T-0502 DIL Mortgage; D-0701 WET_INK_REQUIRED; scan D-0702 |
| TC-E2-018-04 | AC4 | NFR | E_SIGNATURE on D-0701; the MSG-P6-009 refusal on its own series |
| TC-E2-018-05 | AC5 | NFR | Path stub DECLINED; the DECLINED series |
| TC-E2-018-06 | AC4, AC5, AC6 | NFR | Cancel on 2026-12-21; the expiry count and the held result series |
| TC-E2-018-07 | AC4, AC7 | NFR | Open X2 with contact stop; the MSG-P6-001 refusal on its own series |
| TC-E2-018-08 | AC2, AC3, AC5, AC6 | NFR | Path stub unavailable for 6 attempts; the attempt-limit alert and the egress-down runbook entry |
| TC-E2-018-09 | AC9 | NFR | Result EA-30001 twice; one version, one signature record, one repeat count |
| TC-E2-018-10 | AC10 | NFR | Result EA-99999; the unknown-reference entry and the exception count |
| TC-E2-018-11 | AC11 | NFR | Branch SIGNED with no document; the MSG-GEN-001 answer in the smoke profile |
| TC-E2-018-12 | AC1, AC4 | Component | RW-PHONECOL sends POST /api/recovery/comms/v1/treatments/{treatmentId}/signature-requests; refused with MSG-P4-002 and counted |
| TC-E2-018-13 | AC8 | NFR | Switch rwb.comms.esign off in SIT; MSG-GEN-006 refusal on its own series; rollback rehearsal recorded in the runbook |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same legacy test case ID. Legacy levels map System to End to end on the app copy and to NFR on this deployment, and Access to Component; the twelve legacy cases are kept in their legacy order and TC-E2-018-13 is the deployment's own case for AC8, because each is replayed in the deployment's smoke and synthetic-day profiles, and the `-ITG` copies belong to `RWB-ITG-E2018-ITG`.

### 17. Guardrails

- No business value in a values file: the signature basis per template, the method and status lists and the retry limit of 5 are data or service configuration held by their owner, never a deployment value.
- No personal data and no signed PDF content in logs, dashboard series, alert payloads, the smoke output or the runbook: references, counts, statuses, durations and staff user IDs only.
- One login per service; the chart carries the rwb-comms login reference and no other service's credential (DP-02).
- The service writes only schema rwb_comms; the migration job never touches another schema, creates no signature table, and no dashboard query reads one (DP-01, DP-15).
- Every subscription has a retry topic and a `.dlt` topic, and the consumer dedupes through the inbox (DP-09).
- No new topic and no Schedule for the retry: the capability reuses the three owner topics, produces to `rwb.decision-record.v1` as its owner provisions it, and relies on the platform relay JOB-11 (DP-10).
- No literal endpoint, certificate or secret in a values file, a chart template, a dashboard or the runbook; the chart carries references resolved at deploy time (NFR-052).
- ACE data is read only through the owner's contract; no dashboard and no smoke step reads an ACE view or another service's schema (DP-05).
- The release pins the image digest and the chart version, and the rollback is rehearsed once in SIT before the wave 2 release.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-OCC-009 | Electronic signature where Legal permits it, wet ink where Legal requires it | The three operations deployed, the egress route to the ACE common module path, the expiry and status panels | TC-E2-018-01, TC-E2-018-02, TC-E2-018-03, TC-E2-018-04, TC-E2-018-06 |
| RWB-E2-018 | The legacy key this deployment belongs to | The chart, the migration, the egress, the subscriptions, the alerts, the dashboards, the runbook, the smoke profile, the switch and the rollback | All twelve legacy cases and TC-E2-018-13 |
| DP set | DP01, DP05, DP07, DP09, DP10, DP11, DP13, DP15, DP19 | The chart, the migration job, the provisioning step and the egress step | TC-E2-018-01, TC-E2-018-08 |
| ADR-013 | 19 services inside ACE | One chart, one schema and one login for rwb-comms | TC-E2-018-01 |
| ADR-014 | One schema and one login per service in ACE PostgreSQL | The migration job in rwb_comms and the login reference | TC-E2-018-01 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The three subscriptions with retry and `.dlt` and the shared decision-record topic | TC-E2-018-08 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The 2 s client budget and the egress timeout of the chart | TC-E2-018-01, TC-E2-018-09 |
| ADR-023 | Observability per service | Eight panels, five alerts and five runbook entries | TC-E2-018-08, TC-E2-018-10 |

### 19. Out of scope

- The application code of the three operations, the basis check, the conduct check reuse, the outbox row and the result handling (RWB-P6-E2018-APP).
- The signature request table and the signed copy as a document version, with the write-once object store (rwb-document, `RWB-P5-E2018-APP`).
- The signature record on the treatment (rwb-treatment, `RWB-S2-E2018-APP`).
- The cross-service journey and its evidence (`RWB-ITG-E2018-ITG`).
- The ACE common module e-signature path itself, its own retries and its endpoint and certificate ownership: the path owner's, not this release's.
- The platform topic provisioning, the platform relay window, the Temporal cluster and the observability stack (the platform epics RWB-PLT-EVT, RWB-PLT-WF and RWB-PLT-OBS).
- The rwb_comms schema design and the logical model (the database stories of the service epic).
- The notice, letter and proof-of-delivery deployment of the same epic (`RWB-P6-E1055-OPS` and `RWB-P6-E2021-OPS`).
- The SMS and LINE dispatch deployment of the same service (`RWB-P6-E2022-OPS`).
