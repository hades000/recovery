# RWB-P5-E1049-INF OCR pipeline on the Workbench document hub

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1049-INF |
| Work type | INF (Infrastructure) |
| Suggested owner | SCB IT infrastructure (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-049 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P5-M |
| Ready to start | Day 1 |
| Size | Not set; the squad sizes it at refinement |
| Depends on (build) | None |
| Contract dependencies | RWB-P5-E1049-CON (build status Not started; contract not yet published) |
| Contract version | Not specified in the source documents (DOR-RWB-P5-E1049-INF-23); set when RWB-P5-E1049-CON is published |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-013, FR-P5-016, FR-P5-020, FR-P5-022, FR-P5-023, FR-P5-027) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-049 for the infrastructure of the OCR pipeline. The legacy story assumed the OCR service was already reachable through an in-process adapter under the identity SY-OCR; on the infrastructure side this story turns that assumption into provisioned resources, capacity and a private network path. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (14 resolved, 17 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **infrastructure engineer**, I want **the infrastructure of the OCR pipeline of `rwb-document` provisioned — the OCR engine capacity and its queue, the `rwb-document` worker pool that serves the 15-minute Schedule, the blob containers for the intake file and the OCR text, the topic with its retry and `.dlt` topics and its ACLs, the secret and the managed identity, the private network path to the OCR provider, and the storage sizing for the text pages —** so that **the pipeline can read 500 pages an hour in business hours from Day 1, scale to zero between bursts, and never reach an engine, a container or a topic that was created by hand or by a credential in a values file**.

The legacy story had three lines for this work: the OCR service run by Autonomous Ops is reachable from SIT through the `OcrClient` adapter under the service identity SY-OCR; the intake and standard containers exist (RWB-TE-012); and the full OCR output is stored at `ocr/{intakeId}.json`. Under D-RCV-60 those become a provisioned engine endpoint with its own capacity and queue, two containers with their access and sizing, the topic and its ACLs, a key-store entry and a private route. None of them is created by application code, and none is a value an operator types into a console.

The story is also where the burst profile is made real. OCR is one of the two bursty workloads of the estate (Arch v5 slide 38), so the worker pool is scaled on the Temporal task-queue backlog and back to zero when the queue drains (Arch v5 slide 20: KEDA's Temporal scaler on bursty queues such as document OCR), and the engine capacity is sized on the 500-pages-an-hour target of Arch v5 slide 46 rather than on the average. This story provisions the capacity, the ceiling and the observability hooks; the deployment, the alerts and the runbook belong to RWB-P5-E1049-OPS.

### 2. Business rationale

The document estate is the largest data object of the Workbench: about 860,000 documents in 2027 (NFR-004) and about 5.8 million documents and 2.8 TB by the end of 2031 (NFR-069), with the OCR estate at 2.8 TB on Blob (Arch v5 slide 6). Every one of those documents passes this pipeline once, and the pipeline's throughput is the gate on the same-day promise of the legacy story: a document that is not read is not classified, extracted or attached.

Four prices of not provisioning it on Day 1 are concrete. An engine endpoint opened ad hoc in SIT cannot be promoted, so the release slips by a change request per environment. A credential copied into a values file becomes a security finding and rotating it becomes a rebuild. An engine capacity sized on the average turns the morning upload burst into a queue that grows all day, and the 60-minute throughput promise of legacy AC2 fails. A text container without a lifecycle and a size plan turns the 2.8 TB estate into a cost incident, and a shared staging area breaks the claim-check rule because a second service could read a file it is not entitled to.

Zero trust requires that each of these is reachable only over a private path, by an identity, with the credential in the key store and never in configuration (Arch v5 slide 35; NFR-052, NFR-053). The topics are not created here: RWB-PLT-N002-INF provisions one event topic per service with three retry topics and one dead-letter topic, and this story consumes that set for `rwb.document.events.v1` and confirms the ACLs the pipeline needs.

### 3. Preconditions

- The platform subscription, the resource group and the private network (virtual network, subnets, private DNS zones) of the environment are available.
- The AKS cluster of the ACE platform is reachable with the workload identity of rwb-document registered, so access is bound to an identity and not to a shared credential.
- The platform key store of the environment exists with its access policy (RWB-PLT-N012-INF provisions the standard Blob, key store and MFT/SFTP resources; this story consumes them for the OCR pipeline).
- The Temporal namespace `rwb-recovery` and the workflow kit are in force (RWB-PLT-N003-INF, RWB-PLT-E1071-CON), so the worker pool of this story polls a queue that exists.
- RWB-PLT-N002-INF has provisioned `rwb.document.events.v1` with its three retry topics and its `.dlt` topic and the ACLs of the service principal.
- The OCR engine is a bank-approved external provider with a private endpoint option; its product, endpoint, engine version and capacity are Not specified in the source documents (GAP-1000; ASM-1782).
- The contract of this key is published (RWB-P5-E1049-CON): the four operations, the three shapes and the event schema fix what the pipeline carries and what it reports.
- No build dependency and no contract dependency in the plan of this key; this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. List what the pipeline needs per environment: the engine endpoint and its quota, the worker pool that serves the Schedule, the intake container, the text container and the path `ocr/{intakeId}.json`, the topic and its ACLs, the secret and the identity, the private route and the sizing of the text estate.
2. Provision the OCR engine capacity: the endpoint, the quota or throughput ceiling sized on 500 pages an hour with headroom for the morning burst, the request timeout of `OCR_TIMEOUT_SECONDS` = 120 and the concurrency the engine accepts.
3. Provision the engine queue as the decoupling element: requests are admitted at a bounded depth, a request beyond the ceiling waits rather than fails, and the depth is exposed as a metric for the worker pool to scale on.
4. Provision the `rwb-document` worker pool: the worker deployment's replica range, the KEDA Temporal scaler on the `rwb-document` task-queue backlog, the scale-to-zero floor between bursts and the maximum concurrent `ocr` activities equal to `OCR_WORKERS` = 4 per pod.
5. Provision the two containers: the intake container that holds the file to read and the text container that holds the OCR JSON at `ocr/{intakeId}.json`, each with its access policy, its lifecycle rule and no public access.
6. Confirm the topic side: `rwb.document.events.v1` exists with its three retry topics and its `.dlt` topic, the principal may publish its own topic and the shared decision-record topic and read only `rwb.document.events.v1`, and no Recovery ACL opens an ACE PII logging topic.
7. Put the engine credential and the client certificate in the key store of the environment, bind each entry to the rwb-document workload identity, and write a rotation runbook for the credential and the certificate.
8. Apply the network rules: a private endpoint or an allow-listed egress route to the engine, private DNS for the endpoint name, TLS on the route, and no inbound listener on any element of the pipeline.
9. Size the text estate: the bytes per page and per item, the expected annual growth from 860,000 documents in 2027 to 5.8 million and 2.8 TB by 2031, the container quota and the lifecycle that keeps the OCR JSON for as long as the intake item and its document are retained.
10. Wire the observability hooks: the engine latency and error rate, the queue depth, the worker backlog and scale events, the container write failures and the topic publish failures, each with no page text and no personal data in the metric labels.
11. Hand the endpoint reference, the capacity ceiling, the container paths and the identity to the app and operations stories and run the six tests of section 16.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The engine quota is exhausted, or the queue depth passes its ceiling | Requests wait in the queue and the worker pool scales up to its maximum; no request is dropped silently and the depth metric alerts | MSG-P5-E1049-INF-02 | AC1, AC2 |
| X2 | The worker pool cannot reach the queue, or the task queue has no poller | Items stay PENDING; the queue-depth and no-poller signals fire and the stuck-workflow scan of the platform escalates | MSG-P5-E1049-INF-03 | AC2 |
| X3 | A container write is refused, or the container quota is reached | The item stays PENDING with its attempt counted; the write failure is reported and no partial JSON is left behind | MSG-P5-E1049-INF-04 | AC3 |
| X4 | The principal publishes to a topic it does not own, or reads one where the catalogue lists it as no consumer | The broker refuses the operation and the attempt is audited | MSG-P5-E1049-INF-02 | AC4 |
| X5 | The credential or the certificate is expired or rotated out | The engine call fails closed, the endpoint health reports not ready and the rotation runbook restores the version; no unauthenticated fallback exists | MSG-P5-E1049-INF-01 | AC5 |
| X6 | A connection to the engine is attempted over a public route, or from outside the allow-list | The network rule refuses it before authentication; the refusal is logged and no listener answers | None | AC6 |
| X7 | A secret appears in a values file, a script or a container image | The secret scan fails the change and the value is moved to the key store | None | AC5 |
| X8 | The text estate passes its sizing plan before the next review | The container quota is raised from the sizing row and the lifecycle review is reopened; nothing is deleted inside the retention period | None | AC3 |

Message identifiers MSG-P5-E1049-INF-01 to MSG-P5-E1049-INF-04 are the infrastructure validation messages of section 14; the business messages of the app story are unchanged and the file failure signal itself is `rwb.document.OcrCompleted.v1` with a non-DONE status.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Provisions the engine capacity, the worker pool, the containers, the topic ACLs, the secret, the route and the sizing; no application code and no dependency on a service build |
| Negotiable | Endpoint, quota, replica range, container names, lifecycle, size plan and network ranges are environment values settled with the platform and security teams; the resource types and their rules are fixed by the architecture |
| Valuable | Gives the pipeline a provisioned engine, a worker pool that scales to zero and a text store that holds the 2.8 TB estate, with nothing listening inward and no secret in configuration |
| Estimable | One engine endpoint and queue, one worker pool, two containers, one ACL confirmation, one key-store layout, one network rule set, one sizing row and six tests |
| Small | Fits one sprint with the rotation runbook and the tests |
| Testable | Every criterion is tested against a provisioned resource, a refused operation, a scale event or a scan, never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Infrastructure of the OCR pipeline of rwb-document

  Background:
    Given the platform subscription, the resource group and the private network of the environment are in place
    Given the OCR engine is a bank-approved external provider and RWB-P5-E1049-INF provisions its capacity and its route
    Given the target environment is SIT

  Scenario: AC1 The OCR engine capacity and its queue are provisioned (new, D-RCV-60)
    Given the engine endpoint of the environment
    When a request is submitted to the engine endpoint
    Then the endpoint admits requests under the rwb-document workload identity only
    Then the capacity ceiling is sized on 500 pages an hour with headroom for the morning upload burst
    Then the engine queue admits up to its configured depth and reports the depth as a metric
    Then the request timeout is OCR_TIMEOUT_SECONDS = 120 and the per-request page limit is reported by the engine
    Then a request beyond the queue ceiling waits and is never dropped silently
    Then the product, the endpoint and the engine version are Not specified in the source documents (GAP-1000; ASM-1782)

  Scenario: AC2 The worker pool for the 15-minute Schedule is provisioned and scales to zero (new, D-RCV-60)
    Given the rwb-document worker deployment in namespace rwb-recovery
    When an event starts the intake workflow on task queue rwb-document
    Then it polls task queue rwb-document with the build ID of the release
    Then the KEDA Temporal scaler is bound to the task-queue backlog and the replica range is set in the environment values
    Then the pool scales to zero when the queue drains and scales up when a Schedule tick enqueues work
    Then the maximum concurrent ocr activities per pod is OCR_WORKERS = 4
    Then a Schedule tick with no poller leaves the items PENDING and raises the no-poller signal

  Scenario: AC3 The intake and text containers exist, with the text path and its sizing (new, D-RCV-60)
    Given the storage account of the environment
    When the OCR step writes the OCR JSON to the text container
    Then the intake container holds the file to read and the text container holds the OCR JSON at ocr/{intakeId}.json
    Then neither container allows public access and each is reachable by the rwb-document workload identity only
    Then the text container has a lifecycle rule that keeps the JSON for as long as the intake item and its document are retained
    Then the sizing row records the bytes per page and per item, the 860,000 documents of 2027 and the 5.8 million documents and 2.8 TB by 2031 of NFR-069
    Then the per-page text size and the container quota are Not specified in the source documents (GAP-1000; ASM-1782)
    Then a refused write leaves no partial JSON at the path

  Scenario: AC4 The topic, its retry and dead-letter topics and its ACLs are confirmed (new, D-RCV-60)
    Given the topics of RWB-PLT-N002-INF in the environment
    When the rwb-document principal publishes to or reads a topic
    Then rwb.document.events.v1 exists with 12 partitions, replication factor 3, 7-day retention and the key caseId
    Then its three retry topics and its .dlt topic exist with 12 partitions
    Then the rwb-document principal may publish its own topic and rwb.decision-record.v1 and may read only its own topic
    Then a publish to another service's topic and a read where the catalogue lists no consumer are both refused
    Then no Recovery ACL opens an ACE PII logging topic and no topic is created by this story

  Scenario: AC5 The secrets and the managed identity are provisioned and rotate (new, D-RCV-60)
    Given the key store of the environment
    Then the engine credential and the client certificate are held there and bound to the rwb-document workload identity
    Then the storage access uses the same identity and no storage key
    Then a secret scan of the values files, the scripts and the image finds no secret
    When the credential or the certificate reaches its rotation point
    Then the rotation runbook stages the new version, switches the endpoint and retires the previous version
    Then an expired credential fails closed with no unauthenticated fallback

  Scenario: AC6 The route to the OCR provider is private and allow-listed (new, D-RCV-60)
    Given the network rules of the environment
    Then the engine endpoint is reached over a private endpoint or an allow-listed egress route only
    Then the endpoint name resolves through private DNS and the route uses TLS
    Then no inbound listener exists on the engine route, the worker pool or either container
    When a connection arrives over a public route or from outside the allow-list
    Then the network rule refuses it before authentication and the refusal is logged
```

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | One schema, one login, one identity: the pipeline uses the rwb-document login and the rwb-document workload identity and no other service's credential | DP-02, DP-14; Architecture v5 slide 29 | Not specified in the source documents (DOR-RWB-P5-E1049-INF-4) |
| BR2 | The topics are the platform's: `rwb.document.events.v1` with three retry topics and one `.dlt` topic, provisioned by RWB-PLT-N002-INF and never created here | DP-09; Architecture v5 slides 11 and 22 | Not specified in the source documents (DOR-RWB-P5-E1049-INF-4) |
| BR3 | The worker pool scales on the Temporal task-queue backlog and to zero between bursts, because OCR is one of the two bursty workloads of the estate | Arch v5 slide 20 | Not specified in the source documents (DOR-RWB-P5-E1049-INF-4) |
| BR4 | Engine capacity is sized on 500 pages an hour with headroom for the morning burst, not on the average | Arch v5 slides 32 and 46; legacy AC2 | Not specified in the source documents (DOR-RWB-P5-E1049-INF-4) |
| BR5 | No secret in code, configuration, a values file or an image: the engine credential and the certificate live in the key store behind the workload identity | Architecture v5 slide 35; NFR-052, NFR-053 | Not specified in the source documents (DOR-RWB-P5-E1049-INF-4) |
| BR6 | Every element is reached over a private path only, and nothing listens inward | Architecture v5 slide 35 | Not specified in the source documents (DOR-RWB-P5-E1049-INF-4) |
| BR7 | The file is read from the intake container and the OCR JSON written to the text container through the claim-check rule; no file byte enters the database or a queue | Arch v5 slide 11; RWB-E1-049 section 17 | Not specified in the source documents (DOR-RWB-P5-E1049-INF-4) |
| BR8 | No business value lives in the infrastructure: the threshold, the workers, the timeout and the attempts are parameters held in document_hub_parameter and read by the app story, and this story only sizes the capacity they imply | Template and Rules §R7.2 s17 | Not specified in the source documents (DOR-RWB-P5-E1049-INF-4) |
| BR9 | The text estate is sized for growth and retained with the document it belongs to; nothing is deleted inside the retention period | NFR-069; NFR-028 | Not specified in the source documents (DOR-RWB-P5-E1049-INF-4) |

### 9. State transitions

The provisioned resources move through these states; no business object moves.

| From | Event | Condition | To |
|---|---|---|---|
| Not provisioned | Apply of the environment file | The engine endpoint, the worker pool, the containers, the ACL confirmation, the key-store entries and the network rules are applied | Provisioned |
| Provisioned | Verification | Every element answers its check of section 16 and the six negative tests pass | Verified |
| Verified | First Schedule tick | A worker polls `rwb-document`, the engine admits the request and the text is written at `ocr/{intakeId}.json` | In use |
| In use | Burst | The queue depth rises and KEDA adds workers up to the maximum | Scaling |
| Scaling | Queue drained | The backlog returns to zero and the pool scales down to the floor | In use |
| In use | Rotation | The credential or the certificate version is switched under the runbook | Verified |
| Verified | Sizing review | The size plan is raised from the sizing row and the change is applied from the file | In use |
| In use | Credential expired, route refused or quota exhausted | The element fails closed and the operator is alerted | Degraded, repaired from the runbook |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SCB IT infrastructure | Owns this story, the environment files, the apply and the sizing row |
| ACE platform team | Owns the cluster, the namespaces, the key store, the brokers and the quotas; approves the capacity ceiling and every change to a setting |
| Security architecture | Approves the identity model, the private route and the key-store layout |
| Database administrator | Owns schema `rwb_document` and the login the pipeline uses |
| OCR provider owner (the bank team that runs the engine) | Confirms the endpoint, its quota, the engine version and the rotation procedure |
| Service team of rwb-document | States the capacity and the container needs; it never creates an element by hand |
| Data steward | Confirms that no page text, no file name with personal data and no personal value reaches a metric label, a log line or a test payload |

The per-service login used by the pipeline is a secret reference resolved at deploy time; the story refers to "the rwb-document login (DP-02)" and never to a literal name. The engine product, endpoint, engine version, per-page text size and capacity ceiling are Not specified in the source documents (GAP-1000; ASM-1782).

### 11. Data

| Item | Content | BR Field ID |
|---|---|---|
| Engine capacity | 500 pages an hour with headroom for the morning burst (Arch v5 slide 46); `OCR_TIMEOUT_SECONDS` = 120; concurrency accepted per endpoint Not specified in the source documents (GAP-1000; ASM-1782) | Not specified in the source documents (DOR-RWB-P5-E1049-INF-7) |
| Engine queue | A bounded admission depth, reported as a metric and consumed by the worker scaler; the depth value Not specified in the source documents (GAP-1000), set as an environment value at the capacity review | Not specified in the source documents (DOR-RWB-P5-E1049-INF-7) |
| Engine identity | Engine product, endpoint, engine version and per-request page limit Not specified in the source documents (GAP-0997); service identity SY-OCR; business-hours window Not specified in the source documents (GAP-0997) | Not specified in the source documents (DOR-RWB-P5-E1049-INF-7) |
| Worker pool | Replica range, KEDA Temporal scaler on the `rwb-document` backlog, floor 0, `OCR_WORKERS` = 4 as the concurrency cap per pod (concurrent `ocr` activities), read as data from document_hub_parameter; the platform scales replicas on queue depth | Not specified in the source documents (DOR-RWB-P5-E1049-INF-7) |
| Containers | The intake container for the file to read and the text container for `ocr/{intakeId}.json`; access by the workload identity only; no public access; container quota Not specified in the source documents (GAP-1000) | Not specified in the source documents (DOR-RWB-P5-E1049-INF-7) |
| Storage sizing | About 860,000 documents in 2027 (NFR-004); about 5.8 million documents and 2.8 TB by the end of 2031 (NFR-069); the OCR estate at 2.8 TB on Blob (Arch v5 slide 6); bytes per page and per item Not specified in the source documents (GAP-1000; ASM-1782) | Not specified in the source documents (DOR-RWB-P5-E1049-INF-7) |
| Topic | `rwb.document.events.v1`, 12 partitions, replication factor 3, 7-day retention, key caseId, three retry topics and one `.dlt` topic, provisioned by RWB-PLT-N002-INF | Not specified in the source documents (DOR-RWB-P5-E1049-INF-7) |
| Secrets | The engine credential, the client certificate, the storage access through the workload identity, the Kafka client credential and the Temporal mTLS material, all from the platform key store | Not specified in the source documents (DOR-RWB-P5-E1049-INF-7) |
| Metrics | Engine latency, engine error rate, engine queue depth, worker backlog, scale events, container write failures, topic publish failures | Not specified in the source documents (DOR-RWB-P5-E1049-INF-7) |

No business data and no personal data are held by this story: the sizes, the counts, the capacities and the metric names carry no page text and no customer value. The threshold, the worker count, the timeout and the attempt limit are parameters of the app story and are named here only because the capacity is sized on them.

### 12. Contract

#### 12.1 REST operations provided

None. This story provides no REST operation; the four operations of the pipeline are RWB-P5-E1049-APP's and declared by RWB-P5-E1049-CON.

#### 12.2 REST operations consumed

None. This story provisions the network path the pipeline uses and adds no call of its own.

#### 12.3 Events published

None. `rwb.document.OcrCompleted.v1` is the app story's event and `DocumentStored` the store's; this story creates no topic and changes no schema, and `rwb.document.events.v1` with its three retry topics and its `.dlt` topic is provisioned by RWB-PLT-N002-INF and reused as provisioned.

#### 12.4 Events consumed

None. The pipeline's consumption of `DocumentStored` is the app story's; this story confirms the read ACL the consumer group needs and adds no subscription of its own.

#### 12.5 Workflows and activities

None. The `DocumentIntakeWorkflow` and its five activities are deployed by RWB-P5-E1049-OPS and contracted by RWB-P5-E1049-CON; this story provisions only the worker pool, its replica range and the scaler that serves them.

#### 12.6 Schedules

None. The 15-minute business-hours Schedule of legacy JOB-12 is registered from configuration by RWB-P5-E1049-OPS; this story sizes the pool that the Schedule's ticks feed.

#### 12.7 Tables owned

None. Schema `rwb_document` and its login are the database story's; this story creates no table and runs no migration.

#### 12.8 Contract fakes

None. The orchestration module of section 16 uses a throwaway engine stub and the container emulator of the environment; the WireMock fakes are test-only workloads of RWB-P5-E1049-CON and are not provisioned into SIT, UAT or production.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None | No operation is provided or consumed by this story |
| Kafka | 0 created, 1 topic set confirmed | `rwb.document.events.v1` with three retry topics and a `.dlt` topic, its ACLs and its per-case key; the set belongs to RWB-PLT-N002-INF |
| Temporal | 1 worker pool, 1 scaler, 0 Schedules | The pool polls `rwb-document` in namespace `rwb-recovery` and scales on the backlog; the Schedule belongs to RWB-P5-E1049-OPS |
| File | 2 containers | The intake container for the file to read and the text container for `ocr/{intakeId}.json`, with the lifecycle and the sizing row of section 11 |

### 13. Solution plan

**Deliverables.** `infra/ocr/environments.yaml` (endpoint references, capacity ceiling, queue depth, replica range and the sizing row per environment), `infra/ocr/containers.yaml` (the two containers, their access policy and their lifecycle), `infra/ocr/network.yaml` (the private endpoint or the allow-listed route, private DNS and TLS), `infra/ocr/keyvault.yaml` (the credential and certificate entries and their identity bindings), `infra/ocr/acl-check.yaml` (the read and write lists the topic confirmation asserts) and `runbook/rotation.md` (the credential and certificate rotation).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The nine rows are the patterns of the legacy key after the split; the H, C, I and X lists of the metadata table stay empty because this story adds no build dependency of its own (Day 1 by rule) and the platform contracts it needs are published before it starts. DP-10 is the substantive one here: the worker pool and its scaler exist because the Quartz step of JOB-12 became a Temporal Schedule, and the capacity of the pool is expressed as the concurrency of the `ocr` activity. DP-09 matters because the topic set, its retry ladder and its `.dlt` topic are the failure path of a publish, and this story must confirm the ACLs rather than create them. The remaining rows are recorded because the capacity this story provisions is sized on parameters read through DP-06, on lists read through DP-07 and on the schema of DP-01 and DP-15; the deployment of the pool is DP-19's route only in the read direction, which is the app story's.

**Build steps**

1. `environments.yaml`: the endpoint reference, the capacity ceiling, the queue depth and the replica range per environment.
2. Provision the engine endpoint, the quota and the admission queue; verify the request timeout of 120 s and the page limit the engine reports.
3. Provision the worker pool: the deployment range, the KEDA Temporal scaler on `rwb-document`, the floor of zero and the concurrency of 4 `ocr` activities per pod.
4. `containers.yaml`: the intake container and the text container with the path `ocr/{intakeId}.json`, the access policy, the lifecycle and the sizing row.
5. `acl-check.yaml`: assert the topic settings, the three retry topics, the `.dlt` topic and the principal's read and write lists; assert that no Recovery ACL opens a PII logging topic.
6. `keyvault.yaml`: the engine credential and the client certificate, the identity bindings and the rotation runbook.
7. `network.yaml`: the private endpoint or the allow-listed route, private DNS, TLS and the no-inbound assertions.
8. Wire the metrics of section 11 and confirm that no label carries page text or a personal value.
9. Run the six tests of section 16 in SIT, one of them a burst that fills the queue and then drains it.

**Done when.** The engine endpoint admits the pipeline under its workload identity, the worker pool scales from zero on a Schedule tick and back to zero when the queue drains, the two containers hold the file and the OCR JSON at the documented path, the topic and ACL assertions pass, the secret scan is clean, the route is private, and the sizing row is signed by the data steward and the platform team.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-E1049-INF-01 | The engine credential or the certificate has expired, or the endpoint health is not ready | The OCR endpoint is not ready. The credential or the certificate must be rotated from the runbook before the pipeline can read documents. |
| MSG-P5-E1049-INF-02 | The engine quota is exhausted or an ACL refuses an operation | The OCR engine is at its capacity or the operation is not authorised. The pipeline waits and the alert names the environment and the endpoint. |
| MSG-P5-E1049-INF-03 | The worker pool cannot reach the task queue, or no worker polls | The rwb-document worker pool is not polling. The pending items stay PENDING until a worker returns. |
| MSG-P5-E1049-INF-04 | A container write is refused or its quota is reached | The document text store refused the write. The item stays PENDING and the sizing or the access is reviewed. |

The four message IDs belong to this story; they are operator and platform messages and not business messages.

### 15. Screens and states

None. The infrastructure has no screen: the environment files are reviewed as code, and every state of section 9 is a pipeline, a broker or a container state. The operator sees the effect on SCR-44 Interface and job monitor and on the dashboards of RWB-P5-E1049-OPS, which read the metrics of section 11. SCR-44 states empty, loading, error and no access are Not specified in the source documents (CG-ALL-5932).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P5-E1049-INF-01 | AC1 | Integration | The engine endpoint under the workload identity; 500 pages submitted in one hour; the queue depth stays under its ceiling and the timeout of 120 s holds |
| TC-P5-E1049-INF-02 | AC2 | Component | A Schedule tick on an idle pool scales the workers from zero, drains the queue and scales back to zero; a tick with no poller raises the no-poller signal |
| TC-P5-E1049-INF-03 | AC3 | Integration | One intake file and one four-page OCR JSON written at `ocr/{intakeId}.json`; a refused write leaves no partial object; the sizing row matches the NFR-004 and NFR-069 volumes |
| TC-P5-E1049-INF-04 | AC4 | Contract | The topic settings, the three retry topics, the `.dlt` topic and the principal's lists; a write to another service's topic and an unlisted read are refused |
| TC-P5-E1049-INF-05 | AC5 | NFR | A secret scan of the values files, the scripts and the image; a rotation of the credential and the certificate with a fail-closed request in between |
| TC-P5-E1049-INF-06 | AC6 | Component | A connection over the public route and one from outside the allow-list; both refused before authentication; the private route negotiated with TLS and private DNS |

### 17. Guardrails

- No business value in the environment files: the capacity ceiling, the queue depth, the replica range, the lifecycle and the sizing row are environment values and never a parameter of a business rule.
- No personal data in a metric label, a log line, a runbook example or a test payload: counts, durations, sizes, statuses and identifiers only, and never a page text or a file name carrying a customer value.
- No secret in code, configuration, a values file or an image; the engine credential and the certificate live in the key store and are rotated under the runbook.
- No inbound listener on any element, and no public route to the engine or the containers.
- No topic created here and no ACL beyond the principal's own read and write lists; a Recovery ACL never opens an ACE PII logging topic.
- No table and no migration: schema `rwb_document` belongs to the database story and this story reads no data.
- No file byte leaves the containers except through the storage product and the claim-check rule; nothing is copied into the database or a queue.
- Every test payload is synthetic; no production document or page text is copied into a test, a runbook or a sizing row.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| NFR-004 | The document store holds the annual inbound document volume with its growth rate, about 860,000 documents in 2027 | The sizing row of section 11 and the text container lifecycle | TC-P5-E1049-INF-03 |
| NFR-069 | The document hub holds the full recovery document estate with storage sized for growth, about 5.8 million documents and 2.8 TB by 2031 | The sizing row and the container quota and lifecycle | TC-P5-E1049-INF-03 |
| NFR-052, NFR-053 | No secret in configuration, and every external party reached over a private path by an identity | The key-store layout, the network rules and the rotation runbook | TC-P5-E1049-INF-05, TC-P5-E1049-INF-06 |
| ADR-014 | Schema and login per service in ACE PostgreSQL | The rwb-document login and the workload identity in every element | TC-P5-E1049-INF-01, TC-P5-E1049-INF-05 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The topic set, its retry ladder and its `.dlt` topic, confirmed and not created | TC-P5-E1049-INF-04 |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz | The worker pool, its scaler and the queue a Schedule tick feeds | TC-P5-E1049-INF-02 |
| Arch v5 slide 20 | KEDA scales bursty queues such as document OCR to zero | The replica range, the floor of zero and the Temporal backlog scaler | TC-P5-E1049-INF-02 |
| Arch v5 slide 46 | OCR and document intake are a burst of uploads at 500 pages an hour | The capacity ceiling and the queue depth | TC-P5-E1049-INF-01 |

The legacy key is RWB-E1-049; its AC1 to AC9 are owned by RWB-P5-E1049-APP and its contract by RWB-P5-E1049-CON. This story proves the provisioned state that those criteria depend on.

### 19. Out of scope

- The pipeline, the activities, the engine client and the quality rule: RWB-P5-E1049-APP.
- The contract baseline and its fakes: RWB-P5-E1049-CON.
- The deployment, the Schedule registration, the dashboards, the alerts and the runbook: RWB-P5-E1049-OPS.
- The Kafka topic set and its ACL model: RWB-PLT-N002-INF.
- The Temporal namespace, the cluster capacity and the worker scaling standard: RWB-PLT-N003-INF.
- The Blob, key store and MFT standard resources: RWB-PLT-N012-INF.
- The database schema, its login and the migration: the database story of `rwb-document` (DP-15).
- The OCR engine's own product selection, licence and model quality, which belong to the provider owner and to RWB-P5-E1049-APP's evaluation.
