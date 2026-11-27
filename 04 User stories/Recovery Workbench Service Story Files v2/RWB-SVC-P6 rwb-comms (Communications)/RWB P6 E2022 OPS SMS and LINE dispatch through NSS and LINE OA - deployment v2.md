# RWB-P6-E2022-OPS SMS and LINE dispatch through NSS and LINE OA

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E2022-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-022 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP07, DP09, DP10, DP11, DP13, DP18, DP19 |
| Parallel lane | L-P6-P |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P6-E2022-OPS-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-P6-E2022-CON (build status Not started, not Done); contract version Not specified in the source documents (DOR-RWB-P6-E2022-OPS-23), path /v1; fake library version Not specified in the source documents (DOR-RWB-P6-E2022-OPS-22) |
| Integration dependencies | None |
| External dependencies | None |
| Rule package | The conduct and consent checks are one versioned rule package governed in rwb-decision and evaluated in rwb-comms; the package identifier is Not specified in the source documents (GAP-1610); the owner approves its first version |
| Case-state guard | rwb-comms keeps a local guard that refuses closed when the case answer is missing; the gateway-bff composite route to SCR-03 answers refusal messages MSG-P4-002 and MSG-P4-003 |
| Contact and consent data | The contact point, its consent state and its failed count are read and written through the rwb-source-data contract; enforcement of stop, consent refusal and the statutory exception stays in rwb-comms |
| Message outcome | The message outcome (channel, direction, conduct check result, delivery status and channel reference) is held as an interaction ledger entry owned by rwb-source-data and read back through its contract; rwb_comms holds no message table (GAP-1599) |
| Notification path interim | Until the ACE notification path publishes its request and result contract with the NSS and LINE OA result-code maps, RWB-P6-E2022-APP and RWB-ITG-E2022-ITG use the stub of section 12.8 of the CON story (RWB-P6-E2022-CON) |
| Dispatch route | P6 rwb-comms calls the ACE Common notification path for SMS and LINE and builds its own dispatch only if the ACE team confirms that no bank-wide service exists; DL30 stays open until then |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (FR-P6-010, FR-P6-017, FR-P6-018, FR-P6-020, FR-P6-022, FR-P6-023, FR-P6-024, FR-P6-025, FR-P6-026, FR-P6-027, FR-P6-028, FR-P6-029, FR-P6-030, FR-P6-031, FR-P6-036) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-022 for rwb-comms. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P6-E2022-OPS). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (18 resolved, 19 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform engineer**, I want **the SMS and LINE dispatch capability of rwb-comms deployed from the service template with its Helm values and its own login, its egress path to NSS and LINE OA through the ACE notification path with its credential and certificate references, the retry worker around the platform relay JOB-11, the alert on the five-attempt limit, the dashboards for the FAILED and exception-queue counts, a runbook for a stuck send, a smoke profile against the fakes, the feature switch and the rollback**, so that **an operator can see within minutes that a message is not leaving, that a channel's results have stopped arriving, or that sends are piling up in the exception queue, and repair it without reading code or waiting for a business report**.

This story deploys an existing capability. It builds no endpoint, no table, no topic and no workflow: the send is the operation of `RWB-P6-E2022-CON`, the message lifecycle is the outbox row in schema `rwb_comms`, and the every-minute retry is the platform outbox relay JOB-11.

### 2. Business rationale

The legacy capability leaned on one Quartz job and one exception log for two very different failures. A message that the ACE notification path never accepted and a message whose result never came back looked the same from operations: nothing on the job record, nothing on the case, and a customer who was never reached. In the target the retry is the platform relay (Architecture v5 slide 44, JOB-11, every minute, every service), so the operational signal has to move from "did the job run" to "is a send leaving, is a result coming back, and is the exception queue growing".

There is a second operational fact that only deployment can carry: this is the one capability of rwb-comms whose failure reaches a customer outside the bank. NSS and LINE OA are reached only through the ACE notification path (REQ-DRI-006, INT-17 and INT-18), and that egress needs a certificate, an endpoint and a secret that the platform secret store holds and the chart only references. An operator who cannot see whether the egress is up will read the exception queue as a business problem.

Deployment is therefore part of the capability: the chart carries the rwb-comms login and no other credential (DP-02), the migration job runs the per-service Flyway sequence in schema `rwb_comms` (DP-15), the three consumer groups are provisioned with retry and `.dlt` paths so a contact stop is never missed (DP-09), and the runbook names the four failures an operator will actually see.

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The Kafka event platform provisions topics with a retry topic and a `.dlt` topic (RWB-PLT-EVT, RWB-PLT-TE006-CON), and `rwb.deviation.events.v1` and `rwb.case.events.v1` are provisioned by their owners.
- The observability stack of the platform is available (RWB-PLT-OBS, ADR-023): metrics, traces and logs with one trace across REST, Kafka and the outbound call.
- The three environments DEV, SIT and UAT exist with their parameter scope, their Kafka and Temporal endpoints and their egress rules to the ACE notification path.
- `RWB-P6-E2022-CON` is published, so the smoke profile and the drift test run against the operation and the four fakes of that baseline.
- `RWB-P6-E2022-APP` is delivered, so the send attempt, the result mapping and the exception state exist to be deployed and observed.
- The ACE notification path's endpoint, its client certificate and the secret names that hold them are Not specified in the source documents (GAP-1074; ASM-2022); the chart references them as secret references until the path owner and the platform security team fix the names.
- The attempt limit of 5 and the exception-queue rule R-UNI-34 are service configuration of rwb-comms, not deployment values of the chart (GAP-1071; ASM-2019).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The pipeline builds one image and one chart version from the same commit, runs the unit, component and contract tests, scans the image and the dependencies, and publishes the chart.
2. The chart deploys rwb-comms with the rwb-comms login, the pre-deploy migration job for schema `rwb_comms`, the readiness and liveness probes and the api deployment that serves the operation.
3. The egress step declares the outbound route to the ACE notification path for the two channels, the client certificate reference and the endpoint from the secret store; no chart value carries a literal endpoint, certificate or secret.
4. The provisioning step declares the consumer groups of `rwb-comms` on `rwb.deviation.events.v1` and `rwb.case.events.v1`, each with its retry topic and its `.dlt` topic, and confirms that the relay window of JOB-11 picks up the outbox rows of `rwb_comms` without a new Schedule.
5. The dashboards are published: sends by channel, sends by delivery status including FAILED, queue depth and exception count, accepted-reference latency, result latency, the attempt distribution up to the limit, the egress error rate, the MSG-GEN-006 rate and the refused counts.
6. The alerts are wired to the message IDs of section 14 and to the runbook entries of section 13; the thresholds are values and carry the placeholder of section 14 until they are confirmed.
7. A smoke step sends one SMS and one LINE message for a synthetic case against the fakes and the SIT profile, so the operation, the outbox row, the retry window, the result mapping and the fake of the notification path are exercised together.
8. The runbook is published and reviewed with the on-call rota: a stuck send, an egress that is down, a result that never arrives, an exception queue that grows, and a refused send that is not an incident.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The migration job fails | The deployment stays unready and the pipeline stops; no traffic reaches the new version | None | AC1 |
| X2 | The egress route or the certificate reference is missing | The release fails the egress check and the send answers 503 on its first attempt; the runbook entry for an egress that is down starts | MSG-GEN-006 | AC2 |
| X3 | A consumer group is provisioned without its retry or `.dlt` topic | The provisioning step fails the release and the consumer refuses to start | None | AC3 |
| X4 | The attempt count of a send reaches the limit of 5 | The send moves to the exception state and the attempt-limit alert fires | None | AC4 |
| X5 | The result of an accepted send never arrives | The result-latency alert fires and the runbook entry for a result that never arrives names the reference and the channel | None | AC5, AC6 |
| X6 | The FAILED count or the exception count passes its value | The dashboard panel and its alert fire with the channel and the environment | None | AC5 |
| X7 | The feature switch is off in an environment | The send is refused closed with MSG-GEN-006 and nothing leaves; the refusal is counted, not paged | MSG-GEN-006 | AC8 |
| X8 | A rollback is ordered | The previous chart version is redeployed and the migration is reversed by its own script; the outbox rows are left for the earlier version to drain | None | AC8 |
| X9 | A refused send is counted as a failure | The refused count is a separate series and never opens a release incident | MSG-P4-002, MSG-P6-001 | AC5 |
| X10 | A release declares a new topic or a Schedule for the retry | The pipeline fails the release on the retired-element check of AC3 | None | AC3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the platform topic provisioning, the secret store and the observability stack; builds no application code |
| Negotiable | Replica counts, resource sizes, alert thresholds and retention are environment values, not story decisions |
| Valuable | Makes an outbound capability observable: a send that does not leave, a result that does not return and a queue that grows each have a signal and an owner |
| Estimable | One chart, one pipeline stage, one migration job, two probes, three consumer groups, the egress step, eight dashboard panels, five alert rules and five runbook entries |
| Small | Fits one sprint with the runbook |
| Testable | Every criterion tests an artefact: the chart renders, the egress check passes, the groups exist, the panels carry data, the alerts fire on a synthetic metric, the runbook entry resolves |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of SMS and LINE dispatch through NSS and LINE OA

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the target environment is SIT

  Scenario: AC1 The Helm chart and values deploy rwb-comms with its own login (new, D-RCV-60)
    Given the rwb-comms Helm chart and its values-dev.yaml, values-sit.yaml and values-uat.yaml
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the release declares the rwb-comms login reference and no other service's credential
    Then the migration job runs the per-service Flyway sequence in schema rwb_comms before the deployment is marked ready, creating template, notice, merge_field and the outbox, inbox and idempotency objects
    Then the readiness probe answers healthy only when the schema is at the expected version and the consumer groups are subscribed
    Then no replica count, resource size, timeout, threshold or cadence is hard-coded in the template

  Scenario: AC2 The egress to NSS and LINE OA runs through the ACE notification path with referenced credentials (new, D-RCV-60)
    Given the egress step of the release for the two channels
    When it is rendered for each environment
    Then the release declares one outbound route to the ACE notification path (INT-17, INT-18) and no route to NSS or LINE OA directly
    Then the client certificate, the trust material and the endpoint are secret references resolved at deploy time, and no values file, chart template or runbook holds a literal endpoint, certificate or secret
    Then the egress check fails the release when the route or the certificate reference is missing, and the send answers 503 with MSG-GEN-006 on its first attempt
    Then the concrete endpoint, the certificate issuer and the secret names are Not specified in the source documents (GAP-1074; ASM-2022)

  Scenario: AC3 The retry worker and JOB-11 are deployed without a new Schedule or topic (new, D-RCV-60)
    Given the outbox rows of schema rwb_comms and the platform relay of JOB-11
    When the release is deployed and the provisioning step runs
    Then the send request is picked up by the every-minute relay window and executed by the rwb-comms send attempt, and no Temporal Schedule, cron entry or job row is registered by this release
    Then a consumer group rwb-comms subscribes to rwb.deviation.events.v1 for DeviationRaised and DeviationCleared and to rwb.case.events.v1 for CaseStateChanged, each with its retry topic and its .dlt topic, and the consumer never acknowledges an event it could not process
    Then rwb.decision-record.v1 is produced to as its owner provisions it and is not recreated, and no new topic is created for this capability
    Then the provisioning step fails the release when a retry or .dlt topic is missing, and the retired-element check fails a release that declares a Schedule for the retry

  Scenario: AC4 The five-attempt limit raises its alert (new, D-RCV-60)
    Given a send whose attempts are counted from 1 to 5 in schema rwb_comms
    When the attempt count of one send reaches 5 and the row moves to the exception state under rule R-UNI-34
    Then one alert fires with the channel, the environment, the attempt count, the send reference and the age of the oldest affected row
    Then the alert links the exception-queue runbook entry and names the ACE notification path owner as the second-line contact
    Then the alert does not fire on a first or second attempt, and it fires once per send and not once per window
    Then the alert threshold and its evaluation window are deployment values with provisional defaults

  Scenario: AC5 The dashboards carry the delivery and exception series (new, D-RCV-60)
    Given the published dashboard
    When a synthetic day is replayed with delivered, read, failed and queued sends on both channels, one unavailable window and five sends that reached the limit
    Then the panels show sends by channel, sends by delivery status including FAILED, queue depth, the exception count, accepted-reference latency, result latency and the attempt distribution up to 5
    Then every panel names its service, its environment and its business date
    Then a refused send is counted on its own series and never opens a release incident
    Then no panel carries a phone number, a LINE identifier, a message body, an addressee or an account number, only references and counts

  Scenario: AC6 The runbook covers a stuck send, a down egress, a missing result and a growing exception queue (new, D-RCV-60)
    Given the published runbook and the five alert rules
    When a send sits in the queued state beyond its window, the egress answers 503, an accepted reference has no result, or the exception count passes its value
    Then each condition has one runbook entry with the check, the owner role and the recovery step
    Then the stuck-send entry names the outbox row, the attempt count, the last error and the send reference, and the step that is safe to repeat
    Then the missing-result entry names the external reference and the channel and states that a resend uses a new Idempotency-Key only after the first reference is confirmed lost
    Then every alert links exactly one runbook entry and every entry names the escalation path when the step fails

  Scenario: AC7 The smoke profile runs against the fakes before a real send (new, D-RCV-60)
    Given the SIT smoke profile with the four fakes of RWB-P6-E2022-CON
    When the smoke step runs on the release build
    Then it sends one SMS and one LINE message for case "RC-2026-000777" and party "P-0077" with synthetic tokens and test numbers only
    Then it asserts the 202 answer, the outbox row, the retry window, the DELIVERED and READ statuses and one refusal with MSG-P6-002
    Then it exercises the MSG-GEN-006 path with the notification path fake answering unavailable and asserts the exception state at attempt 5
    Then it asserts that no phone number, LINE identifier or message body appears in a log line or a metric label

  Scenario: AC8 The feature switch and the rollback are safe (new, D-RCV-60)
    Given the feature switch rwb.comms.sms-line and the two channel switches in the values files
    When the switch is off in an environment and a send is requested
    Then the send is refused closed with MSG-GEN-006, nothing leaves for the ACE notification path and the refusal is counted on its own series
    When a rollback is ordered
    Then the previous chart version and its image digest are redeployed, the migration is reversed by its own script, and the outbox rows are left for the earlier version to drain without a duplicate send
    Then the rollback is rehearsed once in SIT and the rehearsal is recorded in the runbook
```

These eight criteria are new for the deployment and test artefacts only; they restate no business outcome owned by RWB-P6-E2022-APP.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | Every outbound message carries a conduct check result on its ledger entry | REQ-OCC-005; FEAT-OCC-05 | AC5; TC-E2-022-03 |
| BR2 | No message is sent while a contact stop is in force | CTL-16; R-UNI-04, R-UNI-05 | AC5; TC-E2-022-04 |
| BR3 | Deviation codes that block SMS and LINE are a reference list, loaded as data by their owner | R-DEV-16; R-UNI-12 | Owned by RWB-P6-E2022-APP; no deployment criterion |
| BR4 | Messages go only to a verified contact point with consent GIVEN for that channel; the deployment holds no copy of a contact point | CTL-17; R-UNI-10 | AC7; TC-E2-022-01, TC-E2-022-02 |
| BR5 | A legal hold stops every outbound action | R-UNI-20 | AC5; TC-E2-022-11 |
| BR6 | A system that is unavailable queues the send and retries; after the limit of 3 retries (NFR-026; the solution architect confirms the number before wave 2) it goes to the exception queue and the attempt-limit alert fires | R-UNI-33, R-UNI-34, R-UNI-36 | AC3, AC4; TC-E2-022-07 |
| BR7 | A refusal that cannot be written to the decision record is not completed, and the 503 is counted as an incident path, not as a business refusal | Principle 5; R-UNI-39 | AC5; TC-E2-022-10, TC-E2-022-14 |
| BR8 | Only the current Approved template for the channel is used; the deployment seeds no template | R-LIT-03; CTL-14 | AC1; TC-E2-022-01 |
| BR9 | The same request twice sends one message; a resend after a lost reference uses a new key only when the first is confirmed lost | R-UNI-40 | AC6; TC-E2-022-09 |
| BR10 | A message raised by a route rule — the offer letter of R-RES-09 — is not part of this deployment's traffic | R-RES-09; legacy section 19 | Out of scope for this deployment; no criterion |
| BR11 | One service, one schema, one login: the release uses the rwb-comms login and no other service's credential | DP-02; Architecture v5 slide 29 | AC1; TC-E2-022-01 |
| BR12 | The migration is a per-service Flyway sequence in schema rwb_comms and runs before the deployment is ready | DP-15; RWB-PLT-E1044-CON | AC1; TC-E2-022-01 |
| BR13 | Every subscription has a retry topic and a `.dlt` topic, and a consumer never acknowledges an event it could not process | DP-09; Architecture v5 slide 22 notes | AC3; TC-E2-022-07 |
| BR14 | No Schedule and no new topic is created for this capability: the retry is the platform outbox relay JOB-11 (owner PLT), no second job retries a notification, and the topics belong to their owners | DP-10, DP-14; Architecture v5 slide 44 | AC3; TC-E2-022-07 |
| BR15 | No environment value is hard-coded: replica counts, resource sizes, timeouts, thresholds and the attempt limit are values or service configuration | Template and Rules §R7.2 s17 | AC1; TC-E2-022-01 |
| BR16 | An alert carries a message ID where the condition maps to one, and links one runbook entry | Template and Rules §R7.2 s14 | AC4, AC6; TC-E2-022-07 |
| BR17 | No dashboard series, log line, alert payload or runbook entry carries a phone number, a LINE identifier, a message body or an addressee; references and counts only | Template and Rules §R7.2 s17; legacy section 17 | AC5, AC7; TC-E2-022-02 |
| BR18 | No literal endpoint, certificate or secret is written into a values file, a chart template, a dashboard or the runbook; the chart carries references only | NFR-052; TSD P6 T7 | AC2; TC-E2-022-01 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart, the migration job and the egress check pass the pipeline | Deploying |
| Deploying | Migration complete and probes healthy | The schema is at the expected version and the consumers are subscribed | Ready |
| Ready | Release superseded | A new chart version is promoted | Rolling |
| Rolling | All pods on the new version | The old ReplicaSet drains | Ready |
| Ready | Egress check failed | The route or the certificate reference is missing | Failed |
| Failed | Rollback | The previous chart version is redeployed and the migration is reversed by its own script | Ready |

The message lifecycle — QUEUED, SENT, DELIVERED, READ, FAILED, EXCEPTION — is the capability's own and is described in RWB-P6-E2022-APP; this story observes it and changes no state of it.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the egress step, the provisioning step, the dashboards, the alerts and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the topic provisioning and the platform relay window |
| Platform security team | Owns the client certificate and the secret material of the egress, and approves the reference the chart carries |
| ACE database administrator | Owns schema rwb_comms, the login and its grants, and approves the migration job |
| Release manager | Approves the promotion of one artefact through the environments and the rollback rehearsal |
| On-call operator | Runs the runbook entries and opens an incident when a send is stuck or the exception queue grows beyond its value |
| ACE notification path owner | Is paged by the egress-down and missing-result alerts and owns the repair beyond the rwb-comms breaker |
| RW-PLATADM, platform administrator | Reads the exception queue in the running service, not in the cluster |

The per-service login name, the certificate and the secret names used by the chart are secret references resolved at deploy time; the chart references "the rwb-comms login (DP-02)" and the egress material by reference, never by literal value.

### 11. Data

| Item | Content | BR Field ID |
|---|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, the feature switch `rwb.comms.sms-line` and the two channel switches, the client timeouts, the edge and the egress timeouts, the alert thresholds | Not specified in the source documents (DOR-RWB-P6-E2022-OPS-7) |
| Schema | rwb_comms, migrated by the per-service Flyway sequence; the tables template, notice and merge_field with the library objects outbox_event, processed_event and idempotency_key | Not specified in the source documents (DOR-RWB-P6-E2022-OPS-7) |
| Topics | `rwb.deviation.events.v1` subscribes DeviationRaised and DeviationCleared; `rwb.case.events.v1` subscribes CaseStateChanged; `rwb.decision-record.v1` is produced to as its owner provisions it; `rwb.comms.events.v1` is not created or extended by this capability | Not specified in the source documents (DOR-RWB-P6-E2022-OPS-7) |
| Egress | One outbound route to the ACE notification path for SMS and LINE, with the client certificate, the trust material and the endpoint as secret references | Not specified in the source documents (DOR-RWB-P6-E2022-OPS-7) |
| Dashboard series | sends by channel, sends by delivery status, queue depth, exception count, accepted-reference latency, result latency, attempt distribution, egress error rate, MSG-GEN-006 rate, refused counts, consumer lag | Not specified in the source documents (DOR-RWB-P6-E2022-OPS-7) |
| Runbook entries | stuck send, egress down, result never arrives, exception queue grows, refused send is not an incident | Not specified in the source documents (DOR-RWB-P6-E2022-OPS-7) |
| Secrets | The rwb-comms login secret, the Kafka client credential, the egress client certificate and the endpoint, all from the platform secret store | Not specified in the source documents (DOR-RWB-P6-E2022-OPS-7) |

The alert values, the egress endpoint, the certificate issuer and the secret names are Not specified in the source documents (GAP-1074; ASM-2022). The exact cluster topology, node pools, replica counts and probe timings are deployment values of the platform chart and are not fixed here. The attempt limit of 3 (NFR-026) and the exception-queue rule are service configuration of rwb-comms, not chart values (GAP-1071; ASM-2019). An attempt is counted once per outbox relay window (JOB-11) as this message capability's own send attempt; the ACE notification path's internal retries are excluded from the count, and the platform relay owner confirms the window semantics. The masking version label, the covered ledger field IDs, the access-log granularity, the parameter defaults and the authorise element are Not specified in the source documents (GAP-2321); no rule, criterion or test value depends on them until they are settled.

### 12. Contract

#### 12.1 REST operations provided

None new. The deployment exposes the one operation of `RWB-P6-E2022-CON` behind gateway-bff: `POST /api/recovery/comms/v1/cases/{caseId}/messages`, owner rwb-comms (P6), API-P6-008, with the 202 `Interaction` answer, the seven refusal conditions and the Idempotency-Key header. The probes are cluster-internal and are not part of the API surface.

#### 12.2 REST operations consumed

None by the deployment. The outbound call of the capability is not a REST operation of a service in this workspace: it is the ACE notification path (INT-17, INT-18), an ACE common module interface whose request and result shapes are Not specified in the source documents (GAP-1069; ASM-2017). Its endpoint and certificate are secret references of AC2, and the deployment adds no consumer of the P1, P3, S8 or P7 contracts: those are the app story's and are faked for the smoke profile.

#### 12.3 Events published

None. The capability's one published element is `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`, written by the local decision-record library and relayed by the platform relay; the shared topic is provisioned by its owner and is reused, not recreated (DP-03, DP-09). This deployment creates no topic and publishes no comms event.

#### 12.4 Events consumed

None provisioned by this story as a new group for the capability's own logic beyond the three subscriptions of AC3: `rwb.deviation.DeviationRaised.v1` and `rwb.deviation.DeviationCleared.v1` on `rwb.deviation.events.v1`, and `rwb.case.CaseStateChanged.v1` on `rwb.case.events.v1`. All three are consumed by one group `rwb-comms` with the inbox of schema `rwb_comms`, each with its retry topic and its `.dlt` topic.

#### 12.5 Workflows and activities

None. The retry worker of this capability is not a Temporal workflow: it is the platform relay window of JOB-11 calling the rwb-comms send attempt, plus the result handling in the service. No worker deployment polls a task queue for this capability, and no activity is registered on `rwb-comms`.

#### 12.6 Schedules

None. JOB-11 Outbox sender is the platform's outbox relay, every minute, with every service as its owner (Architecture v5 slide 44); this release registers no Schedule and no cron entry, and the five-attempt limit is applied inside the send attempt rather than by a scheduler (GAP-1071; ASM-2019).

#### 12.7 Tables owned

None new. The migration job creates and migrates the tables of `rwb_comms` — template, notice, merge_field, outbox_event, processed_event and idempotency_key — and touches no other schema (DP-01). `interaction` and `contact_point_ext` stay with P1, `recovery_case` and `task` with P3, `deviation` with S8 and `decision_log_entry` with P7; no dashboard query reads any of them.

#### 12.8 Contract fakes

| Fake | Deployment use |
|---|---|
| ACE notification path stub | Runs in the pipeline and in the SIT smoke profile: an accepted reference with DELIVERED, the LINE delivered then read, a FAILED result and an `unavailable` answer for six attempts |
| rwb-source-data WireMock | Same profile: the consent GIVEN and WITHDRAWN answers and the failed-count update |
| rwb-case WireMock | Same profile: legal hold false and true, and a delayed answer beyond 2 s |
| rwb-deviation WireMock | Same profile: the open deviation X1 with contact stop on and an empty answer |

The fakes are test-only workloads; they are not deployed into UAT or production, and each is replaced by the real owner as its story lands.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 1 consumed outside the workspace | The send operation provided; the outbound call to the ACE notification path (INT-17, INT-18); one hop, 2 s |
| Kafka | 1 produced to a shared topic, 3 consumed | `DecisionRecorded` on `rwb.decision-record.v1` reused; `DeviationRaised`, `DeviationCleared` and `CaseStateChanged` consumed with retry and `.dlt` |
| Temporal | None | No workflow, no activity and no Schedule; the retry is the platform relay JOB-11 |
| File | None | The release reads no runtime file; values files and chart templates are build inputs |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_comms`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/comms/v1` | none |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-10 is claimed only for the relay dependency: no Schedule is registered by this release. DP-05 applies as a prohibition: no dashboard and no smoke step reads an ACE view.

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-comms/` | Chart with the api deployment, service, migration job, config map, secret references, probes, the egress configuration and the Schedule hook that registers nothing for this capability |
| `helm/rwb-comms/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, `rwb.comms.sms-line` and the two channel switches, the client and egress timeouts, the alert thresholds |
| Egress step | One outbound route to the ACE notification path, the client certificate and endpoint references, and the check that fails the release when either is missing |
| Pipeline stage | Build, unit, component and contract tests, retired-element check, egress check, image and dependency scan, chart publish, promote the same artefact |
| Provisioning step | Consumer group `rwb-comms` on `rwb.deviation.events.v1` and `rwb.case.events.v1` with retry and `.dlt`; reuse of `rwb.decision-record.v1`; confirmation that the relay window of JOB-11 drains `rwb_comms` |
| Dashboards | Eight panels: sends by channel; sends by delivery status; queue depth; exception count; accepted-reference latency; result latency; attempt distribution up to 5; egress error rate, MSG-GEN-006 rate and refused counts |
| Alerts | Five rules, each with a message ID where one applies and one runbook entry |
| Runbook | Five entries: stuck send, egress down, result never arrives, exception queue grows, refused send is not an incident |

**Probes.** Readiness answers healthy only when the migration is at the expected schema version and the consumer groups are subscribed; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database, calls another service or calls the ACE notification path.

**Alert mapping.**

| Message ID | Condition | Alert | Route |
|---|---|---|---|
| None | The attempt count of a send reaches 5 and the row moves to the exception state | Attempt-limit alert with the channel, the attempt count, the send reference and the age of the oldest affected row | Platform on-call, ticket to the ACE notification path owner |
| MSG-GEN-006 | The egress answers 503 or the notification path is unavailable on a share of sends | Egress error-rate alert with the breaker state and the environment | Platform on-call, page, ACE notification path owner |
| None | An accepted reference has no result inside the result window | Result-latency alert with the reference, the channel and the oldest affected send | Platform on-call, ticket |
| None | The exception count passes its value | Exception-queue alert with the count and its change against the trailing hour | Platform on-call, page |
| MSG-P4-002 and MSG-P6-001 | A send is refused for want of a right or for a contact stop | Refused count on the dashboard | No page |
| MSG-GEN-006 | The feature switch is off and the send is refused closed | Switch-off count on the dashboard | No page |

Every alert carries its message ID where the condition maps to one, and the three conditions without a message ID carry the series name instead. The alert thresholds, the result window and the pending values are Not specified in the source documents (GAP-1074; ASM-2022); the values are provisional defaults until they are confirmed.

**Done when.** The chart renders in all three environments, the pipeline promotes one artefact and fails on a fake drift, a missing retry topic, a missing egress reference or a retired element, the three consumer groups exist with their retry and `.dlt` paths, the eight panels carry the synthetic day, the five alert conditions fire on synthetic metrics, the smoke profile passes against the fakes with no personal data in a log line or a metric label, and the five runbook entries are reviewed by the on-call rota.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-001 | A contact stop applies | Contact with this customer is stopped for {reason}. |
| MSG-P6-002 | No consent for the channel | The customer has not consented to {channel}. Use another channel. |
| MSG-P6-003 | The template is withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P3-004 | A legal hold is on the case | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-P4-002 | The role lacks Case record C | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is outside the caller's scope | This case is not in your scope. |
| MSG-P7-003 | The decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-001 | Channel or template missing | Enter {field}. |
| MSG-GEN-006 | NSS or LINE OA is unavailable, the egress is down, or the switch is off | {system} is not available. Your request is queued and will be retried. |

The alert values, the egress endpoint and the secret names are Not specified in the source documents (GAP-1074; ASM-2022); the message texts are copied unchanged from the legacy story and the deployment adds the routing, the threshold and the runbook link, never a new wording.

### 15. Screens and states

The deployment serves SCR-03 Case record with the Send message action in its editable, loading and refused states, with its empty, error and no access states Not specified in the source documents (CG-ALL-6610), SCR-04 Case timeline with the message row in its Loading and filtered states, with its empty, error and no access states Not specified in the source documents (CG-ALL-6611), showing the channel, the conduct check and the delivery status only (GAP-1077), and SCR-09 Exception queue, served as a P6 administrative read over the outbox rows in the exception state (GAP-1078), with its loading state, and its empty, error and no access states Not specified in the source documents (CG-ALL-6612), all through the gateway-bff composite route (DP-19). The operator-facing surfaces of this story are the pipeline run view, the release view, the egress check result, the eight dashboard panels and the runbook; the smoke step sends one SMS and one LINE message for a synthetic case in SIT and asserts the 202 answer, the outbox row, the retry window, the two channel statuses and one refusal inside the 2 s budget.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-022-01 | AC1, AC2, AC7 | NFR | P-0077 MOBILE consent GIVEN; NSS stub reference NSS-7781 |
| TC-E2-022-02 | AC2, AC5, AC7 | NFR | P-0077 LINE consent GIVEN; LINE OA stub delivered and read |
| TC-E2-022-03 | AC4, AC5 | NFR | Open X6; the MSG-P6-001 refusal on its own series |
| TC-E2-022-04 | AC4, AC5 | NFR | Open X1 with contact stop; the MSG-P6-001 refusal on its own series |
| TC-E2-022-05 | AC5 | NFR | MOBILE consent WITHDRAWN; the MSG-P6-002 refusal on its own series |
| TC-E2-022-06 | AC5 | NFR | SMS-REMIND TH v1 Withdrawn; the MSG-P6-003 refusal on its own series |
| TC-E2-022-07 | AC2, AC3, AC4, AC6 | NFR | Notification path stub unavailable for 6 attempts; the attempt-limit alert and the egress-down runbook entry |
| TC-E2-022-08 | AC5, AC7 | NFR | NSS result FAILED, failed count 0; the FAILED series and the result latency |
| TC-E2-022-09 | AC5, AC6 | NFR | Same Idempotency-Key twice; one send counted and one row in the queue |
| TC-E2-022-10 | AC5 | NFR | Open X6; decision log stubbed unavailable; the 503 counted on the incident path |
| TC-E2-022-11 | AC5 | NFR | Legal hold true; the MSG-P3-004 refusal on its own series |
| TC-E2-022-12 | AC7 | NFR | No channel; the MSG-GEN-001 answer in the smoke profile |
| TC-E2-022-13 | AC1, AC5 | Component | RW-PHONECOL sends POST /cases/{caseId}/messages; refused with MSG-P4-002 and counted |
| TC-E2-022-14 | AC4, AC6 | NFR | Decision log write forced to fail on 10 refusals; none recorded as sent, none paged as a send failure |
| TC-E2-022-15 | AC8 | NFR | Feature switch rwb.comms.sms-line off and a send refused with MSG-GEN-006; SIT rollback rehearsal |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end on the app and integration copies and to NFR on this deployment, Access to Component and Resilience to NFR; the fourteen legacy cases are kept in their legacy order because each is replayed in the deployment's smoke and synthetic-day profiles, TC-E2-022-15 is the new case for AC8, and the `-ITG` copies belong to the integration story.

### 17. Guardrails

- No business value in a values file: the blocking deviation codes, the result-code maps, the templates and their languages, and the attempt limit are data or service configuration held by their owner, never a deployment value.
- No personal data in logs, dashboard series, alert payloads, the smoke output or the runbook: references, counts, channel names, durations and staff user IDs only. The phone number, the LINE identifier, the message body and the addressee never appear.
- One login per service; the chart carries the rwb-comms login reference and no other service's credential (DP-02).
- The service writes only schema rwb_comms; the migration job never touches another schema and no dashboard query reads one (DP-01).
- Every subscription has a retry topic and a `.dlt` topic, and the consumer dedupes through the inbox (DP-09).
- No new topic and no Schedule for the retry: the capability reuses `rwb.deviation.events.v1` and `rwb.case.events.v1`, produces to `rwb.decision-record.v1` as its owner provisions it, and relies on the platform relay JOB-11 (DP-10, DP-14).
- No literal endpoint, certificate or secret in a values file, a chart template, a dashboard or the runbook; the chart carries references resolved at deploy time (NFR-052).
- ACE data is read only through the owner's contract or the `v_ace_*` views; no dashboard and no smoke step reads an ACE view or another service's schema.
- The release pins the image digest and the chart version, and the rollback is rehearsed once in SIT before the wave 2 release.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-OCC-004 | SMS and LINE through the bank's channel platforms, result on the case | The send operation deployment, the two channel switches and the delivery-status panels | TC-E2-022-01, TC-E2-022-02, TC-E2-022-08, TC-E2-022-09 |
| REQ-OCC-005 | Every outbound contact carries a conduct check result | The refused counts on the dashboard and the decision-record path in the release | TC-E2-022-03, TC-E2-022-04, TC-E2-022-10, TC-E2-022-11, TC-E2-022-14 |
| REQ-OCC-006 | Withdrawn consent stops the channel | The consent refusal on the refused series, answered from the P1 contract fake | TC-E2-022-05 |
| REQ-ILG-010 | Messages dispatched write their result to the ledger | The result-latency series and the FAILED series | TC-E2-022-01, TC-E2-022-02, TC-E2-022-08 |
| REQ-DRI-006 | No direct call to NSS or LINE OA; only the ACE notification path | The egress step of AC2 and its route check | TC-E2-022-01, TC-E2-022-02, TC-E2-022-07 |
| RWB-E2-022 | The legacy key this deployment belongs to | The chart, the egress, the retry worker, the alert, the dashboards, the runbook, the smoke profile, the switch and the rollback | All fifteen cases |
| DP set | DP01, DP03, DP05, DP07, DP09, DP10, DP11, DP13, DP18, DP19 | The chart, the provisioning step and the egress step | TC-E2-022-07, TC-E2-022-08 |
| ADR-013 | 19 services inside ACE | One chart, one schema and one login for rwb-comms | TC-E2-022-01 |
| ADR-014 | One schema and one login per service in ACE PostgreSQL | The migration job in rwb_comms and the login reference | TC-E2-022-01 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The three subscriptions with retry and `.dlt` and the shared decision-record topic | TC-E2-022-07 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The 2 s client budget and the egress timeout of the chart | TC-E2-022-01, TC-E2-022-03 |
| ADR-023 | Observability per service | Eight panels, five alerts and five runbook entries | TC-E2-022-07, TC-E2-022-08 |

### 19. Out of scope

- The application code of the operation, the conduct check, the outbox row and the result mapping (RWB-P6-E2022-APP).
- The contract documents and the fakes as published artefacts (RWB-P6-E2022-CON); this story only deploys the test copies.
- The cross-service journey and its evidence (RWB-ITG-E2022-ITG).
- The ACE notification path itself, its own retries and its endpoint and certificate ownership: the path owner's, not this release's.
- The platform topic provisioning, the platform relay window, the Temporal cluster and the observability stack (the platform epics RWB-PLT-EVT, RWB-PLT-WF and RWB-PLT-OBS).
- The rwb_comms schema design and the logical model (the database stories of the service epic).
- The notice, letter and proof-of-delivery deployment of the same epic (RWB-P6-E1055-OPS and RWB-P6-E2021-OPS).
- The template catalog and its screens (RWB-P6-E1046-APP).
- Data migration from the legacy schema and the reconciliation run (Epic 2 and rwb-source-data).
