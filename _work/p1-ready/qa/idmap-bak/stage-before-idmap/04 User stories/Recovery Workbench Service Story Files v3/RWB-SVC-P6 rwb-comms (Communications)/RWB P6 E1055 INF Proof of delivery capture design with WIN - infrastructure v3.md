# RWB-P6-E1055-INF Proof of delivery capture design with WIN

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- The delivery entry is appended by rwb-comms over REST after the proof-of-delivery read, which writes nothing (RD-P1-007; finding #1); the workload identity needs the read right and Case record C (finding #4).
- The late-batch alert fires on DP07 status `STALE` at the rwb-source-data expected-by time, not on a `COMPLETE` literal or a reviewed time of this story; the stale period is removed and MSG-P1-001 follows Error and Message Standard v6 (RD-P1-041; findings #2, #5, #6).
- The repeat test row no longer counts on `duplicate_count` (RD-P1-041; finding #3).
- Pending: NEW-GAP-F14-10 (the signal behind the DP07 alert and its owner beside the rwb-source-data stale alert).
- Finishing pass: the flag-closed answer follows the published read (request S5-stories-0288); the delivery entry is paired by barcode or notice reference (RD-P1-064); test case IDs of Test Cases v9 applied.
- Test case citations aligned to Test Cases v9: identifiers of this story replace the placeholders and the shared legacy identifiers that now hold another story's case (W2-tests mapping).

| Item | Value |
|---|---|
| Story key | RWB-P6-E1055-INF |
| Work type | INF (Infrastructure) |
| Suggested owner | SCB IT infrastructure (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-055 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P6-E1055-INF-16) |
| Contract version | Not specified in the source documents (DOR-RWB-P6-E1055-INF-23); fix the version with RWB-P6-E1055-CON |
| Patterns applied | DP01, DP05, DP07, DP09, DP10, DP11, DP15, DP18, DP19 |
| Readiness decisions | RD-P1-005; RD-P1-007; RD-P1-040; RD-P1-041, RD-P1-043, RD-P1-064 |
| Parallel lane | L-P6-H |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | No build dependency; runtime route to rwb-source-data.yaml 5.1.0 (proof-of-delivery read, freshness, ledger append) consumed by RWB-P6-E1055-APP |
| Integration dependencies | INT-14 WIN daily file (GAP-1602): file layout held as an interface definition owned by rwb-integration |
| External dependencies | RWB-ACE-001 view v_ace_pod for proof of delivery (GAP-1608): capture held behind the platform flag rwb.dataengine.pod-read until the view is available; until then the read answers 200 with rows empty and DP07 `STALE` with a null `businessDate`; the answer has no member for the reason (Pending: GAP-0579), and MSG-P1-001 is shown; never a guessed date and never a fallback to data_as_of |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (FR-P6-013, FR-P6-015, FR-P6-016, FR-P6-017, FR-P6-018, FR-P6-019, FR-P6-020, FR-P6-021, FR-P6-023) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-055 for rwb-comms (INF). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 26 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, ledger ownership, freshness alert, identity rights and repeat statements aligned with RD-P1-005, 007, 040 and 041. Tool: Claude Code / Claude Sonnet 5.5.

### 1. Story

As an **infrastructure engineer**, I want **the runtime for the WIN file exchange — the one-hop egress path from the rwb-comms and rwb-integration pods to the WIN SFTP endpoint, the client certificate and key that authenticate it, the file landing and staging area with its retention and its private access, the worker and KEDA scaling that carries the 16:00 dispatch burst and the proof-of-delivery ingest, the key-store entries for every credential, the storage that holds the dispatch files of the business date, and the observability signals with the freshness alert for a late WIN batch**, so that **the loop of RWB-E1-055 can run against an outside system under the bank's network and key rules, a late or failed WIN batch is visible to an operator within the business day, and no certificate, key or file ever sits in a values file, a log or a public location**.

### 2. Business rationale

The legacy story leaned on integration adapters that an ACE operator configured once, and the only production trace of a broken WIN edge was an operator noticing that notices stayed Generated. In the target the same edge is a service-to-service chain: rwb-comms builds the file, rwb-integration executes `deliverFile`, and the proof of delivery returns through the ACE ingestion that rwb-source-data reads (Architecture v5 slides 17, 41 and 44, JOB-10 "Airflow file window + workers"). Every one of those steps needs something the pod does not have by default: an egress path that reaches one host and nothing else, a certificate the WIN owner accepts, a staging area where a file waits without being world-readable, and enough workers to finish the 16:00 batch without stretching into the next business date.

Two of the failure modes are pure infrastructure. A certificate that expires silently stops every dispatch, and the only symptom is a notice that never goes Sent. A staging area that fills or is misclassified as a log destination leaks the one artefact of this loop that carries an addressee and an address, so the area has to be private, sized and swept. Neither is visible from the application metrics alone, which is why the freshness signal of the WIN batch and the file-age signal are part of this story rather than a dashboard line in the deployment story.

This story creates no `rwb_*` table, no topic, no queue, no Schedule and no business value. It provisions and configures the runtime, the identity, the storage and the signals; the app story builds the workflow and the read, and the deployment story registers the Schedule, the consumer groups, the dashboards and the runbook.

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The platform Blob account or object store, the platform key store and the workload identity mechanism of the platform are available (RWB-PLT-LIB), so no credential sits in a file, a chart or a repository.
- The Temporal workflow kit and the `rwb-recovery` namespace are available (RWB-PLT-WF, RWB-PLT-E1071-CON), and the KEDA scaler of the platform is available for the worker pools.
- The Kafka event platform, the schema registry and the observability stack are available (RWB-PLT-EVT, RWB-PLT-OBS, ADR-023).
- rwb-integration owns the file transport and its `outbound_item`; this story opens the path and provides the identity, and never builds the file.
- The WIN SFTP endpoint, the certificate subject, the certificate owner, the network zone, the storage container name and every size are Not specified in the source documents (GAP-1102; ASM-2050).
- The rwb-comms workload identity is the caller of the rwb-source-data proof-of-delivery read and of the ledger append (Case record C); both rights are granted with the identity in each environment (RD-P1-007).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Provision the workload identity of rwb-comms and the workload identity of rwb-integration for this exchange, each with the least grant it needs: read and write on the staging area for the exchange, read on the file store of the business date, and nothing else.
2. Open the egress path from the pods of both services to the WIN SFTP endpoint, on the reviewed port, one hop, with no broader internet egress, and record the allowed destinations as a reviewed list.
3. Provision the key-store entries: the SFTP client certificate and its private key reference, the host key of the WIN endpoint, the storage reference of the staging area and the Kafka and Temporal client material. No literal value reaches a values file, a chart template, a log or a ticket.
4. Provision the file landing and staging area for each environment: a private container with no anonymous access, the object layout by business date and interface, an immutability or versioning policy for the delivered copy, a retention period and a sweep that runs after the retention.
5. Size the staging area and the file store from the measured file size of the INT-14 batch and the INT-15 proof file, and record the figure as a reviewed value per environment.
6. Size the worker pools: a dispatch pool that carries the 16:00 burst of `NoticeDispatchWorkflow`, an ingest pool that carries the proof-of-delivery read and its retries, and a KEDA scaler that follows the queue depth of each pool, with the Temporal worker build ID pinned per release.
7. Expose the signals: the age of the newest delivered file per interface, the size and count of files in the staging area, the SFTP handshake result and its latency, the certificate expiry in days, the worker queue depth and the pod restarts of each pool.
8. Wire the freshness alert: the WIN batch is late when rwb-source-data answers DP07 with status `STALE` (no `LOADED` stamp for the expected business date at the product's expected-by time, or a failed source), and the alert names the product, the business date, the last load date and the interface. rwb-source-data raises its own stale alert; Pending: the signal this alert reads and how the two alerts are routed, owner platform operations with the solution architect, tracked as NEW-GAP-F14-10.
9. Hand the identity, the storage references and the signal names to RWB-P6-E1055-APP and RWB-P6-E1055-OPS; the app story builds the flow, the deployment story registers the Schedule, the consumer groups and the runbook.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The egress allow list is broader than one hop, or a destination outside it is reachable | The provisioning check fails the environment and the release is blocked | None | AC1 |
| X2 | The client certificate is missing, expired or not issued by the agreed authority | The handshake fails, the file is not delivered and the expiry alert fires before the expiry, not after | None | AC1, AC4 |
| X3 | The staging area allows anonymous access or is granted to a wider identity | The provisioning check fails and the environment is not marked ready | None | AC2 |
| X4 | The staging area passes its size or its object count | The staging alert fires and the sweep runs; the run is not blocked by a full area | None | AC2, AC6 |
| X5 | The dispatch burst outruns the worker pool | The queue depth alert fires and KEDA adds workers up to its cap; the run finishes inside the window or the cap is reviewed | None | AC3 |
| X6 | DP07 reads status `STALE` | The freshness alert fires with the product, the business date, the last load date and the interface, and the runbook entry opens | MSG-P1-001 | AC6 |
| X7 | A secret, key or certificate body appears in a values file, a log or a ticket | The pipeline check fails the build and the credential is rotated | None | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Provisions network, identity, storage, scaling, secrets and signals; builds no application code and creates no business object |
| Negotiable | The host name, the port, the sizes, the retention and the alert time are environment values settled with the platform team |
| Valuable | Makes the WIN edge reachable and watchable at all, and unblocks the app and deployment stories on Day 1 |
| Estimable | One egress list, two identities, four key-store entries, one staging area, two worker pools, six signals and one alert |
| Small | Fits one sprint with the provisioning checks |
| Testable | Every criterion tests an artefact: a reachable host, a refused destination, a private container, an expiry alert, a scaled pool and a fired alert |

### 7. Acceptance criteria

```gherkin
Feature: Infrastructure for the proof-of-delivery loop of rwb-comms

  Background:
    Given the platform object store, key store and service mesh are in force
    Given the target environment is SIT

  Scenario: AC1 The WIN file exchange reaches one host through one egress path (new, D-RCV-60)
    Given the egress policy of the rwb-comms and rwb-integration pods
    When the allowed destinations and the handshake are inspected
    Then the WIN SFTP endpoint is allowed on the reviewed port and no other outside destination is reachable
    Then the handshake uses the client certificate from the key store and accepts only the host key recorded for the endpoint
    Then a destination outside the reviewed list is dropped, counted and alerted
    Then the host name, the port, the network zone and the certificate owner are Not specified in the source documents (GAP-1102; ASM-2050)
    Then the provisioning check fails the environment when the path is broader than one hop

  Scenario: AC2 The file landing and staging area is private, sized and swept (new, D-RCV-60)
    Given the staging area of the environment and the delivered-file store of the business date
    When their access level, layout, retention and size are inspected
    Then neither has anonymous or public access, and each is reachable only by the two workload identities of this exchange
    Then the object layout is by business date and by interface, so the file of a date is found without a search
    Then the delivered copy is kept under an immutability or versioning policy for the reviewed retention period, and the sweep runs after it
    Then the size and the object count are reviewed values per environment and are not a template constant
    Then the container name, the retention period and the sizes are Not specified in the source documents (GAP-1102; ASM-2050)

  Scenario: AC3 The dispatch and ingest worker pools scale on their queue depth (new, D-RCV-60)
    Given the two worker pools and their KEDA scalers
    When the 16:00 burst of NoticeDispatchWorkflow and a proof-of-delivery ingest are replayed
    Then the dispatch pool scales out on the queue depth of rwb-comms up to its reviewed cap and finishes inside the file window
    Then the ingest pool scales on its own queue depth and does not consume the dispatch capacity
    Then each worker polls its own task queue in namespace rwb-recovery with the build ID of the release
    Then no replica count, resource size or scaler threshold is hard-coded in a template
    Then the pool sizes and the scaler caps are Not specified in the source documents (GAP-1102; ASM-2050)

  Scenario: AC4 Every credential comes from the key store and is rotated without a rebuild (new, D-RCV-60)
    Given the key-store entries of the environment
    When the service reads them at run time
    Then the SFTP client certificate and key, the host key, the storage reference, the Kafka credential and the Temporal mTLS material are read by the workload identity and never from a file or a chart value
    Then no secret, key or certificate body appears in a values file, a log, a dashboard or a ticket
    Then the certificate expiry is a monitored signal in days, with an alert before the expiry
    Then rotating the certificate or the key is a key-store operation with no rebuild of the service and no chart change

  Scenario: AC5 The dispatch files of a business date are stored and addressable (new, D-RCV-60)
    Given the file store of the service and the outbound item of rwb-integration
    When the files of a business date are listed
    Then the INT-14 file of the date is addressable by its file ID and its business date, and the address is what the outbound item carries
    Then the stored file is private, encrypted at rest and in transit, and no copy is written to a log or to a temporary public path
    Then the retention of the stored file follows the reviewed retention and the sweep does not delete a file that is under review
    Then the storage names, the retention and the encryption mechanism are Not specified in the source documents (GAP-1102; ASM-2050)

  Scenario: AC6 A late WIN batch is visible on the freshness signal (new, D-RCV-60)
    Given the six signals of this story and the freshness alert
    When rwb-source-data answers DP07 with status "STALE" because no "LOADED" stamp exists for the expected business date at the expected-by time, or a DP07 source reads "FAILED"
    Then the freshness alert fires with the product, the business date, the last load date and the interface, using MSG-P1-001 as its message
    Then the file-age signal, the staging signal, the handshake signal, the expiry signal and the queue-depth signal are each published with the environment and the business date
    Then no signal or alert payload carries a name, an address, an identity number or a contact value
    Then the alert time is the DP07 expected-by time held by rwb-source-data, and this story sets no time of its own; the signal the alert reads is Pending (NEW-GAP-F14-10) and its threshold Not specified in the source documents (GAP-1104; ASM-2050)
    TC: TC-P6-E1055-INF-01, TC-E1-055-06 (Test Cases v9)

  # AC7 to AC11 are legacy criteria of RWB-E1-055 that this story does not own (CG-ALL-6437), so their numbers are not reused here.

  Scenario: AC12 No rwb_* table, topic, queue, Schedule or business object is created by this story (new, D-RCV-60)
    Given the deployed schema, topics, queues, Schedules and business objects of the environment
    When they are listed after the deploy
    Then no rwb_* table, topic, queue, Schedule or business object is found
    Then the deliverable is identity, storage, network and signals only

  Scenario: AC14 The workload identity holds the rights of its two rwb-source-data calls (new, RD-P1-007)
    Given the rwb-comms workload identity is deployed in the environment
    When it calls GET /api/recovery/source-data/v1/proof-of-delivery?businessDate=2026-11-30 and POST /api/recovery/source-data/v1/cases/{caseId}/interactions with synthetic data
    Then neither call is answered 401 or 403
    Then the same calls with the rwb-integration identity are answered 403 and nothing is written
    TC: TC-P6-E1055-INF-02 (Test Cases v9)

  Scenario: AC13 A status change the model does not allow is refused (new, D-RCV-60)
    Given the state model of the proof-of-delivery loop
    When a status change that the model does not allow is requested
    Then the change is refused, the status does not move, and the refusal is recorded with its reason
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One service, one login: the runtime uses the rwb-comms login for the service and the rwb-integration identity for the file transport, and no other service's credential | DP-02; Architecture v5 slide 29 |
| BR2 | The WIN endpoint is reached one hop from the pods, on the reviewed port, and nothing outside the reviewed list is reachable | DP-11; ADR-020 |
| BR3 | Every secret and every certificate comes from the key store through the workload identity; none appears in a file, a chart, a log or a ticket | Template and Rules §R7.2 s17; NFR-052 |
| BR4 | The staging area is private, laid out by business date and interface, and swept after its retention; a file that carries an addressee and an address never sits in a public or shared location | Template and Rules §R7.2 s17; legacy section 17 |
| BR5 | No replica count, resource size, scaler threshold or alert value is hard-coded; all come from values files or the key store | Template and Rules §R7.2 s17 |
| BR6 | The file store carries the delivered file of the business date and its identifier, and the identifier is the one `outbound_item` records | DP-01; TSD P6 T3.3 (`dispatch_file_id` to `outbound_item`) |
| BR7 | Rows of source WIN are served only when its ACE batch record is `COMPLETED` for the business date, and a late batch shows as DP07 `STALE` and is signalled with MSG-P1-001 | legacy BR4 and BR7; MSG-P1-001; RD-P1-041 |
| BR8 | This story creates no `rwb_*` table, no topic, no queue, no Schedule and no business object; identity, storage, network and signals are the whole deliverable | Template and Rules §R7.2 s12 |
| BR9 (R-LIT-07) | The delivery date drives the notice period, so a late WIN batch delays a legal clock; the freshness signal is therefore an operational control and not a report | Temporal and Drools design slide 20 notes |
| BR10 (R-UNI-33) | A downstream endpoint that fails is retried, and the state does not advance until the retry succeeds; the retry policy is a values entry, not code | INT-14 error handling |
| BR11 (R-UNI-34) | A retried delivery that passes its limit leaves the file in the exception path with its reason, and the operator sees it on the file-age and staging signals | INT-14 error handling |
| BR12 (REQ-DRI-006) | No direct call to a system of record from a business component; the file moves only through rwb-integration, and this story opens the path it uses | REQ-DRI-006; DP-16 |

### 9. State transitions

The infrastructure of one environment moves through these states; no business object moves.

| From | Event | Condition | To |
|---|---|---|---|
| Not provisioned | Identity, key-store entries and egress path created | The two identities hold their least grant and one host is reachable | Provisioned |
| Provisioned | Staging area and file store created | Private access, layout, retention and sweep in place | Active |
| Active | Provisioning check fails after a platform change | A grant widens, a destination opens or the access level drifts | Degraded; the environment is not marked ready |
| Active | Certificate rotated | The key-store entry is updated and the pod reloads it | Active with the new certificate |
| Active | Certificate nears its expiry | The expiry signal passes its value | Alerted; rotation is due |
| Active | Staging area passes its size or count | The sweep runs and the alert fires | Active after the sweep |
| Degraded | Rollback of the platform change | The reviewed grant, destination and access level are restored | Active |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SCB IT infrastructure | Owns the egress path, the identities and their grants, the staging area, the file store, the sizing and the signals |
| ACE platform team | Owns the object store, the key store, the certificate authority, the KEDA scaler and the service mesh this story configures against |
| Security | Approves the identity grant, the certificate subject, the key-store entries and the network allow list |
| The rwb-comms and rwb-integration owner teams | Confirm the sizing and the file window after the burst test and consume the identity and the storage |
| Platform administrator | Rotates the certificate, extends the retention when the audit requirement changes, and acts on the freshness alert |
| ACE database administrator | Confirms that no database object is created by this story, since it creates none |

The identity names, the key-store entry names, the certificate subject and the host name are Not specified in the source documents (GAP-1102; ASM-2050); this story fixes their shape and leaves the names to the environment configuration.

### 11. Data

| Item | Content |
|---|---|
| Identities | The rwb-comms workload identity and the rwb-integration identity for the exchange, each with read and write on the staging area and read on the file store, and nothing else |
| Key-store entries | The SFTP client certificate and its key reference, the WIN host key, the storage reference, the Kafka credential and the Temporal mTLS material |
| Staging area | Private container, layout by business date and interface, retention and sweep, reviewed size and object count |
| File store | The delivered file of the business date, addressable by file ID and business date, private and encrypted |
| Egress list | The WIN SFTP endpoint on the reviewed port; no other outside destination |
| Worker pools | A dispatch pool and an ingest pool, each with its KEDA scaler, its queue and its reviewed cap |
| Signals | File age per interface, staging size and count, handshake result and latency, certificate expiry in days, queue depth, pod restarts of each pool |
| Alert | The freshness alert of the WIN batch, with MSG-P1-001 as its message |
| Screen states (SCR-44, SCR-45) | Empty, loading, error and no-access states: Not specified in the source documents (DOR-RWB-P6-E1055-INF-10) |

BR Field ID: Not specified in the source documents (DOR-RWB-P6-E1055-INF-7) for each of the eight rows above.

The host, the port, the zone, the certificate subject and its owner, the container names, the retention, the sizes and the alert time are Not specified in the source documents (GAP-1102; ASM-2050); they are reviewed values per environment and are recorded here as assumptions, not as business values. The staging area and the file store hold letter files, which are business documents and may carry an addressee and an address: they are private, encrypted and never copied into a log, a ticket or a test fixture, and every test file is synthetic.

### 12. Contract

#### 12.1 REST operations provided

None. This story exposes no API, no operator endpoint and no cache read. The readiness and liveness endpoints are cluster-internal and are owned by RWB-P6-E1055-OPS.

#### 12.2 REST operations consumed

None. The one-hop path that carries the rwb-comms calls to rwb-source-data and rwb-document is a platform route it sits on; the operations themselves are consumed by RWB-P6-E1055-APP and declared in RWB-P6-E1055-CON. This story adds no call of its own.

#### 12.3 Events published

None. The story provisions no topic and publishes no event; the two events of the loop are RWB-P6-E1055-APP's and their envelopes are RWB-P6-E1055-CON's.

#### 12.4 Events consumed

None. The three consumer groups of the service are provisioned by RWB-P6-E1055-OPS; this story only ensures the platform routes and the signals that their failure would show.

#### 12.5 Workflows and activities

None. No workflow, activity or task queue is created here. The worker pools this story sizes poll `rwb-comms` and the queue of the integration activity, and the workflow definition itself belongs to RWB-P6-E1055-APP.

#### 12.6 Schedules

None. The 16:00 dispatch Schedule is registered by RWB-P6-E1055-OPS against the workflow kit, and the cross-system edge is the bank Airflow file window (Architecture v5 slide 44). This story opens the network and the storage that the Schedule's workers need and registers no Schedule.

#### 12.7 Tables owned

None. This story creates no `rwb_*` table, no column and no index; the objects it provisions are a container, key-store entries, a network policy and a scaler, none of which is an ACE DB table. The `notice` columns of this loop arrive in the service's own Flyway sequence through RWB-P6-E1055-APP (DP-15).

#### 12.8 Contract fakes

None. The fakes run in the pipeline and in SIT and belong to RWB-P6-E1055-CON and RWB-P6-E1055-OPS; no fake is deployed or configured here. The WIN edge stub of SIT is a test folder and a test acknowledgment record on a synthetic fixture, and this story provisions it as a test-only destination outside the production allow list.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None | No operation is provided or consumed by this story |
| Kafka | None | No topic, no producer, no consumer |
| Temporal | None | No workflow, activity or Schedule; the worker pools it sizes serve the app story's workflow |
| File | 1 dotted grey path | P6 builds the INT-14 file, P2 delivers it to the WIN edge, the INT-15 proof file returns through ACE and rwb-source-data; this story provides the staging area, the file store, the identity and the egress for that path |

### 13. Solution plan

**Deliverables.** `infra/network/win-egress.yaml` (the one-hop allow list and the drop rule), `infra/identity/rwb-comms-workload.json` (the two identities and their least grants), `infra/keyvault/entries.md` (the certificate, the host key and the storage references), `infra/storage/staging.json` (the staging area, its layout, retention, sweep and sizes), `infra/storage/file-store.json` (the delivered-file store of the business date), `infra/sizing/workers.yaml` (the two pools and their scalers) and `infra/observability/signals.md` (the six signals and the freshness alert).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-11 is served by the one-hop egress list: the pods of the two services reach the WIN endpoint, the owners' contracts and their own storage endpoint, and nothing else. DP-05 is a prohibition here and DP-18 and DP-19 add no work. The platform H rows are delivered by the platform waves and are not repeated in the metadata H field, which stays empty.

**Build steps**

1. Create the egress allow list and the drop rule; test an allowed handshake and a dropped destination (AC1, X1).
2. Create the two identities and their least grants; test that a write outside the staging area and a read outside the file store are refused (AC2, X3).
3. Create the key-store entries; test the handshake with a valid, an expired and an unissued certificate, and the expiry signal (AC4, X2).
4. Create the staging area and the file store with their layout, retention and sweep; test privacy, the address of a file and the sweep (AC2, AC5).
5. Run the burst test of the dispatch pool and the ingest test of the second pool; record the sizes and the caps per environment (AC3, X5).
6. Publish the six signals and the freshness alert; replay a late WIN batch and a failed handshake and confirm each fires (AC6, X6).
7. Hand the identity, the storage references and the signal names to the app and deployment stories.

**Done when.** The egress list is one hop in all three environments, a destination outside it is dropped, the staging area and the file store are private and swept, the handshake succeeds only with the issued certificate, the burst test finishes inside the file window with the reviewed caps, and the freshness alert fires on a late batch with MSG-P1-001.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | DP07 is `STALE` | {product} is from {date}. Today's load has not arrived. ({product} is the catalog name DP07 and {date} is the last complete business date) |
| None | A policy, identity, certificate or sizing check fails | No business message is produced. The provisioning check fails the environment with the resource name and the violated rule, and the platform administrator acts on it. |

This story adds no message ID. The freshness alert carries MSG-P1-001 with the text of Error and Message Standard v6, and the product and date values the freshness answer holds. Every other condition is reported to the operator as a provisioning or signal condition, never to a Workbench user, and the platform administrator is the owner of the action in each case.

### 15. Screens and states

None. There is no screen in this story. The operator-facing surfaces are the provisioning check, the container and key-store policy views, the burst-test report and the six signals; SCR-44 Interface and job monitor and SCR-45 Data quality show the effects on the screens the deployment story serves (DP-19), and no screen is built or changed here. SCR-44 states: empty, loading, error and no access are Not specified in the source documents (CG-ALL-6440). SCR-45 states: loading is in Screen Specifications v1 section SCR-45; empty, error and no access are Not specified in the source documents (CG-ALL-6441).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-055-01 | AC1, BR1 | End to end | N-0001 Generated; acknowledgment with RR123456789TH |
| TC-E1-055-02 | AC2, BR2 | End to end | rwb-source-data contract fake pod row for 2026-11-30 with RR123456789TH, callback_date 2026-11-28 |
| TC-E1-055-03 | AC3 | End to end | WIN owner sample WIN-POD-SAMPLE-v1, 25 records ingested by ACE |
| TC-E1-055-04 | AC4, BR3 | End to end | No acknowledgment on three runs |
| TC-P6-E1055-INF-03 | AC5, BR4 | End to end | ACE batch for WIN FAILED at its record count |
| TC-E1-055-06 | AC6, BR4 | End to end | 30 rows, 1 unknown |
| TC-E1-055-07 | AC7; run by Not specified in the source documents (CG-ALL-6437) | End to end | rwb-source-data contract fake pod rows of 2026-11-30 read twice; the second read writes nothing in rwb-source-data (no ledger row, no duplicate_count change) and rwb-comms appends no second entry; row to be updated in Test Cases v9 (W2-tests) |
| TC-E1-055-08 | AC8; run by Not specified in the source documents (CG-ALL-6437) | End to end | JOB-10 rerun on 2026-11-25 |
| TC-E1-055-09 | AC9, BR5; run by Not specified in the source documents (CG-ALL-6437) | End to end | N-0002 with no barcode on 2026-11-28 |
| TC-E1-055-10 | AC10, BR6; run by Not specified in the source documents (CG-ALL-6437) | End to end | Repeat of RR123456789TH on 2026-12-07 |
| TC-E1-055-11 | AC11, BR7; run by Not specified in the source documents (CG-ALL-6437) | End to end | No COMPLETE WIN batch for 2026-11-30 |
| TC-E1-055-12 | Access | Component | RW-PHONECOL reads the notice dispatch detail; refused with MSG-P4-002 |
| TC-E1-055-13 | BR8 | Component | Deployed schema, topics, queues and Schedules listed after the deploy; no rwb_* table, topic, queue or Schedule found |
| TC-E1-055-14 | AC12, BR8 | Component | Deployed schema, topics, queues, Schedules and business objects listed after the deploy; no rwb_* table, topic, queue, Schedule or business object found |
| TC-E1-055-15 | AC13 | Component | Not specified in the source documents (NEWAC-RWB-P6-E1055-INF-AC13) |

The twelve are the legacy test cases of RWB-E1-055 in their legacy order, with the Level column added; System maps to End to end and Access to Component. TC-E1-055-13 is added for BR8, which no legacy test case covers. The provisioning checks of this story are named in section 13 and carry their own identifiers, because they test an environment and not a business case.

Version 3: rows that cite `TC-P6-E1055-INF-` identifiers are this story's rows of Recovery Workbench Test Cases v9. Where a shared legacy identifier now names another story's case there, this story's identifier replaces it, and cases run by one identifier are joined in one row.

### 17. Guardrails

- No business value in a policy or a values file: the eligible state, the attempt limit, the break days and the list values stay reference data of their owner, never a deployment value.
- No personal data in a container name, an object path, a signal or a log: the file store addresses a file by interface and business date, and no name, address, identity number or contact value is written there.
- One login per service; the runtime carries the rwb-comms login reference and the rwb-integration identity for the exchange, and no other service's credential (DP-02).
- The staging area and the file store are private and encrypted; no file that carries an addressee or an address is copied into a log, a ticket or a shared location.
- Every secret and every certificate comes from the key store through the workload identity; no value sits in a chart, a values file or a repository (NFR-052).
- The egress list is one hop and is reviewed; a destination outside it is dropped, counted and alerted (DP-11).
- The service writes only its own schema; this story writes none, and no signal query reads another service's schema or an ACE view (DP-01, DP-05).
- Files move only through rwb-integration: no component of this story calls WIN, and the test folder of SIT is outside the production allow list (REQ-DRI-006).

### 18. Traceability

| Requirement ID | Requirement (short) | Infrastructure element | Test cases |
|---|---|---|---|
| REQ-OCC-003 | Letters dispatched for print and post, proof of delivery returns to the case | The egress path, the staging area, the delivered-file store and the freshness alert | TC-E1-055-01, TC-E1-055-09 |
| REQ-ILG-004 | What happens in an interaction is recorded against that interaction | The runtime and storage that carry the ledger calls: rwb-comms appends the dispatch entry and one delivery entry per matched pod_key over REST; the proof-of-delivery read of rwb-source-data writes nothing | TC-E1-055-02 |
| REQ-DRI-006 | No direct call to a system of record; files move only through rwb-integration | The one-hop egress list and the two identities of the exchange | TC-E1-055-03, TC-E1-055-04 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The reviewed egress allow list | TC-E1-055-03 |
| ADR-023 | Observability per service | The six signals and the freshness alert | TC-E1-055-11 |

| Item | What it covers in this story |
|---|---|
| Legacy key RWB-E1-055 | The WIN exchange and the proof-of-delivery ingest of the legacy story, as environment work |
| DP-01 | No `rwb_*` table is created and no other schema is read by a signal query |
| DP-05 | No ACE view is granted to the service; the pod arrives through rwb-source-data |
| DP-07 | The list values stay reference data of rwb-case, not a deployment value |
| DP-09, DP-10 | The topics, the queue and the Schedule are provisioned by their owners; this story provides the runtime they need |
| DP-11 | The one-hop egress list to the WIN endpoint |
| DP-15 | The dispatch columns are migrated by the app story in the service's own schema |
| DP-18, DP-19 | The ledger is rwb-source-data's and the screens are the composite route's; neither is provisioned here |
| ADR-013, ADR-014, ADR-015, ADR-016 | 19 services, one login per service, Kafka with outbox and inbox, and a reusable Temporal layer |
| ADR-021 | Per-service migration ownership, unchanged by this story |

### 19. Out of scope

- The workflow, the notice read, the pod read and the reconciliation (RWB-P6-E1055-APP).
- The contract baseline and the fakes as published artefacts (RWB-P6-E1055-CON).
- The deployment, the Schedule registration, the consumer groups, the dashboards, the alerts and the runbook (RWB-P6-E1055-OPS).
- The legacy criteria AC1 and AC9 and the end-to-end proof of the loop (RWB-ITG-E1055-ITG).
- The file transport itself, the outbound item and the retry of a failed delivery: rwb-integration (RWB-P2-E1007-CON and the rwb-integration slices of RWB-E1-007).
- The ACE ingestion of INT-15 and the freshness stamp (rwb-source-data and the ACE ingestion).
- The platform products behind this story: the object store, the key store, the certificate authority, the service mesh, the KEDA scaler and the observability stack (RWB-PLT-LIB, RWB-PLT-EVT, RWB-PLT-OBS).
- The `rwb_comms` schema design, its tables and its migrations (the database stories of the service epic).
- The host name, the port, the zone, the container names, the retention, the sizes and the alert time, which are reviewed values and Not specified in the source documents (GAP-1102; ASM-2050).

### 20. Remaining delivery steps

- Size, endpoint, certificate, storage and sizing values: Not specified (GAP-1102; ASM-2050). Owner: platform administrator with the WIN owner.
- Grant the rwb-comms workload identity the proof-of-delivery read right and Case record C in DEV, SIT and production: Pending. Owner: platform administrator.
- Settle NEW-GAP-F14-10 before the alert is wired: Pending. Owner: platform operations with the solution architect.
- Test case rows in Test Cases v9 and synthetic data in DEV: Pending. Owner: QA.
- Epic design sign-off: Pending. Owner: solution architect.
