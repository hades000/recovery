# RWB-P5-E1032-INF Automatic attach from the OCR intake

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1032-INF |
| Work type | INF (Infrastructure) |
| Suggested owner | SCB IT infrastructure (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Wave check | Wave 1 kept per R5.6; confirm at the wave 1 entry check that the S9 frame and its platform baseline are available to a wave 1 story (GAP-3139, R-22070). The build notes state that rwb-partner is delivered in wave 1 per R5.6 while its Arch v5 service wave is 4 (slide 41); its service wave governs its later stories, and one conflict row per service and business epic is raised under R5.6 (GAP-3174, R-28573) |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-032 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not sized in this story; the squad sizes it at refinement (DOR-RWB-P5-E1032-INF-16) |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP15, DP19; DP-03, DP-06, DP-07, DP-09, DP-10, DP-15 and DP-19 add platform H rows (RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON) held as the wave 0 shared baseline and listed as H dependencies in the build notes (GAP-3140, R-28574) |
| Parallel lane | L-P5-I |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P5-E1032-CON (build status Not started; not Done) |
| Contract version | Full contract version Not specified in the source documents (DOR-RWB-P5-E1032-INF-23) |
| Integration dependencies | None |
| Open register gaps | GAP-1197 (R-22061), GAP-1199 (R-22062), GAP-1201 (R-22063), GAP-1202 (R-22064), GAP-2444 (R-22065), GAP-2445 (R-22066), GAP-2447 (R-22067), GAP-3137 (R-22068), GAP-3138 (R-22069), GAP-3139 (R-22070). Secondary partner slice stands on the rwb-partner S9 frame under Template R4 naming until published (GAP-3137) |
| External dependencies | None |
| Base document baseline | FSD P6 Communications v3 and TSD P6 Communications v2 are In review; wave 1 build uses these reviewed versions and any change in approved text is a change request (GAP-1203, R-28568) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-015, FR-P5-017, FR-P5-018, FR-P5-019, FR-P5-032) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-032 for rwb-document. The legacy story assumed a Quartz job on a shared scheduler, a shared schema and a review queue an operator could open in the database; on the infrastructure side this story provisions the compute of the intake workers and the 15-minute Schedule they serve, the OCR text storage and its index, the hold container `rwb-quarantine`, the topic with its retry and `.dlt` topics and the least-privilege ACLs, the managed identity and secret layout, the private network path and the scanning capacity. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (28 resolved, 29 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **infrastructure engineer**, I want **the intake-match path of `rwb-document` provisioned as infrastructure — the container and compute sizing of the workers that run `matchStep` for the 15-minute JOB-12 Schedule in business hours, the `document_text` storage and its index sized for the OCR estate, the hold container `rwb-quarantine` with its rule and its clearing, the topic `rwb.document.events.v1` with its three retry topics and its `.dlt` topic and the least-privilege ACLs of the consumers, the managed identity and the secret layout of the service, the private network path to `rwb-case`, `rwb-decision` and Blob, and the scanning capacity of the intake path**, so that **the matcher, the reviewer's queue and the store run on Day 1 against provisioned capacity with no secret in a values file, no public route to a dependency and no file left in a container whose rule nobody wrote down**.

The legacy story had one line for this work: "JOB-12 Document intake: runs matchStep after the extraction step" inside a shared Quartz scheduler, a shared recovery schema and a review queue opened from the same database. Under D-RCV-60 each of those three is gone. The scheduler is a Temporal Schedule on queue `rwb-document` in namespace `rwb-recovery` (DP-10, Arch v5 slide 44); the tables are `document_intake`, `document_text` and `document` in `rwb_document`, reached with the rwb-document login only (DP-01, DP-02); and the review queue is the service's own list operation behind the gateway-bff composite route (DP-19). What is left for this story is capacity, storage, a container rule, a topic, ACLs, an identity, a route and the scan.

The path has one property that shapes the provisioning: the OCR text is the only personal-data-bearing artefact this service holds at scale. The text of a scanned notice sits in `document_text` until the document is attached or discarded, and the file sits in `rwb-quarantine` until the same moment. The provisioning therefore fixes three rules alongside the capacity: the text is never copied to a container or a topic, the hold container answers one claim-check read at a time through the storage product, and both are cleared by a stated rule rather than by an operator's memory.

### 2. Business rationale

About 860,000 documents arrive in 2027 (NFR-004) and the hub holds about 5.8 million documents and 2.8 TB by the end of 2031, including every version and every held document (NFR-069). The intake path is the door every one of them comes through: a scan, a partner file or an email becomes a row in `document_intake`, a page set in `document_text`, and then a document on a case or an item in the review queue. If the compute is sized for a demonstration, the 15-minute run falls behind and the queue grows; if the text has no index budget, the matcher's pattern scan and the reviewer's page read slow to a crawl at the 500-page sample of the module; if the hold container has no rule, a held file stays in a container for years and a copy of a customer document outlives its case.

The private path matters as much. Zero trust requires the service to reach `rwb-case`, `rwb-decision`, the Kafka brokers, the Temporal frontend and Blob over private endpoints with a workload identity (Arch v5 slide 35; NFR-052, NFR-053). A public endpoint added for a test is a security finding that survives to production, and a connection string pasted into a values file turns a rotation into a rebuild.

The scanning capacity is the one new element the legacy story did not have in its own words: every inbound file is scanned before it is stored (FSD P5 A2.18; RWB-P5-E1041-APP), so the intake rate is bounded by the scan rate and not by the OCR or the matcher. This story provisions that capacity and states the rule that an item waits in the hold container rather than entering the matcher unscanned.

The 15-minute cadence is the legacy one and the architecture one: JOB-12 runs every 15 minutes, owned by `rwb-document` (Arch v5 slide 44; FSD P5 AC-BG-P5-012-01). The legacy story says "every 15 minutes in business hours"; the architecture slide gives no business-hours qualifier, so the Schedule and the compute are sized for the business-hours cadence and the difference is recorded as `ASM-1762`.

### 3. Preconditions

- The platform subscription, the resource group and the network (virtual network, subnets, private DNS zones) of the environment are available, and the AKS cluster of the ACE platform is reachable from the `rwb-recovery` namespace.
- The workload identity of rwb-document is registered in each environment, so every access is bound to an identity and not to a shared credential (DP-02).
- RWB-PLT-N012-INF provisions the standard Blob account, the key store and the MFT/SFTP resources; this story consumes the Blob account and the key store for the three document containers.
- RWB-PLT-N002-INF provisions the 20 event topics with their 60 retry topics and their 20 dead-letter topics, so `rwb.document.events.v1`, its three retry topics and its `.dlt` topic exist before this story binds the ACLs.
- RWB-PLT-N003-INF provisions the namespace `rwb-recovery`, its certificates and the payload codec, so queue `rwb-document` can be polled.
- RWB-PLT-DB provisions the `rwb_document` schema and the rwb-document login; this story creates no schema, no table and no grant, and the migration is RWB-PLT-E1044-CON's sequence applied by the release of RWB-P5-E1032-OPS.
- The scanning product of RWB-P5-E1041-APP exists as a service call, so the capacity provisioned here is the cluster and network capacity around it and not a scanner binary.
- The baseline RWB-P5-E1032-CON is published, so the four operations of the app story and their status codes are known to the network and the identity work.
- No build dependency and no contract dependency in the plan of this key; this story is Day 1 by rule (Template and Rules §R5.7).
- The release date 30 November 2026 is the legacy one and is tentative (ASM-1760), and the story carries Status Draft (realignment v1) because no approval of the realigned story is recorded (ASM-1761).

### 4. Flow

1. List what the path needs: the worker compute for `matchStep`, the database storage and index for `document_text`, the three containers with their policies, the topic and its four derived topics, the six service principals it talks to, the four secret classes, the network routes and the scan rate.
2. Size the worker pool for the 15-minute business-hours cadence: the `matchStep` activity runs on queue `rwb-document`, the pool scales on the queue backlog through KEDA, and the request and limit set of the activity is fixed as values per environment.
3. Size the storage: `document_text` holds one row per page with its quality, `document_intake` holds the item, and both are measured against the 860,000 documents a year of NFR-004 and the 2.8 TB estate of NFR-069; the index budget is set for the matcher's pattern scan and the reviewer's page read.
4. Provision the container `rwb-quarantine` for held intake files with its access rule (managed identity only), its one-file-per-link claim-check read through the storage product and its clearing rule on attach, discard or age.
5. Bind the three containers `rwb-docs`, `rwb-docs-legal` and `rwb-quarantine` to the storage account, with `rwb-docs-legal` under the immutability policy the storage product owns; this story takes the policy as given and states that no blob is overwritten.
6. Verify the topic `rwb.document.events.v1` with its 12 partitions, replication factor 3, 7-day retention, key caseId, the three retry topics at 1 min, 10 min and 1 h and the `.dlt` topic; provision nothing new if RWB-PLT-N002-INF already did it.
7. Bind the ACLs: the rwb-document principal writes `rwb.document.events.v1` and `rwb.decision-record.v1` and reads nothing else; the consumer groups of `rwb-case` and `rwb-agent` read `rwb.document.events.v1`; no Recovery principal reads an ACE PII logging topic.
8. Put the login, the Kafka credential, the Temporal mTLS material and the storage identity in the key store behind the workload identity, and write the rotation entry for each of the four classes.
9. Apply the private route: private DNS for `rwb-case`, `rwb-decision`, the brokers, the Temporal frontend and Blob; no public inbound rule on the service; egress limited to the named endpoints.
10. Provision the scan capacity and the hold rule that makes an item wait unscanned, and run the six tests of section 16 against the provisioned state.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The worker pool is saturated and the queue backlog grows past its threshold | The pool scales out on the backlog; if the ceiling is reached the run takes longer and the run book names the ceiling as the cause | MSG-P5-E1032-INF-02 | AC1, AC5 |
| X2 | A page of OCR text pushes the `document_text` storage past its budget | The alert fires on the storage series; the run book names the retention and archiving step and the capacity request | MSG-P5-E1032-INF-03 | AC2 |
| X3 | The hold container is unreachable or refuses the write of a new item | The item stays `ocr_status` PENDING and no match runs; the scan alert fires and the run book names the container | MSG-P5-E1032-INF-04 | AC3 |
| X4 | A held file is older than the clearing rule allows | The clearing job records the item for the owner role and does not delete a file whose item is still open | MSG-P5-E1032-INF-04 | AC3 |
| X5 | A principal writes to a topic it does not own, or reads a topic where the event catalogue lists no consumer | The broker refuses the operation and the attempt is audited | MSG-P5-E1032-INF-01 | AC4 |
| X6 | A credential, certificate or identity binding expires or is rotated out | The dependency fails closed, the service health reports not ready and the rotation entry restores the version; no clear-text fallback exists | MSG-P5-E1032-INF-02 | AC5 |
| X7 | A network rule admits public egress, or a public inbound rule appears on the service | The network scan fails the change and the release is blocked | None | AC6 |
| X8 | The scan rate falls below the intake rate | Items wait in the hold container and the queue age rises; the alert fires and the run book names the scan capacity | MSG-P5-E1032-INF-03 | AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Provisions compute, storage, containers, topic bindings, ACLs, identity, route and scan capacity; no application code is built here and no service build blocks it |
| Negotiable | Replica counts, request and limit sets, storage budgets, the clearing age, the backlog threshold and the scan rate are environment values settled with the platform and network teams |
| Valuable | Gives the app and operations stories provisioned capacity, a ruled hold container and a private path on Day 1, with no secret in a values file |
| Estimable | One worker pool, one storage and index budget, three containers with rules, one topic binding, one ACL set, one identity layout, one route set and one scan capacity |
| Small | Fits one sprint with the runbook entries and the six tests |
| Testable | Every criterion is tested against provisioned state, a refused operation, a container rule or a scan, never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Infrastructure of the intake-match path for rwb-document

  Background:
    Given the platform subscription, the resource group and the private network of the environment are in place
    Given the workload identity of rwb-document is registered in the environment
    Given the target environment is SIT

  Scenario: AC1 The worker compute serves the 15-minute business-hours cadence (new, D-RCV-60)
    Given the worker pool of rwb-document
    Then the pool polls the task queue rwb-document in namespace rwb-recovery and nothing else
    Then the matchStep activity carries its request and limit set as environment values and not in code
    Then the pool scales on the queue backlog through KEDA, with a floor that keeps one poller and a ceiling that is a value
    When the backlog of a business-hour window is replayed
    Then every batch of the 15-minute cadence finishes before the next one starts
    Then the replica count, the request and limit set and the ceiling are Not specified in the source documents (GAP-0993; ASM-1763)

  Scenario: AC2 The OCR text storage and its index are sized for the estate (new, D-RCV-60)
    Given the storage of rwb_document in the environment
    When the storage of a synthetic month is measured against the storage budget
    Then document_text holds one row per page with its page number, its text and its quality, and the table has an index on intake_id and page_no
    Then document_intake has the held index on match_status and received_at and the pending index on match_status and received_at
    Then the storage budget is set against the 860,000 documents a year of NFR-004 and the 5.8 million documents and 2.8 TB of NFR-069
    Then the storage series and the index size series are emitted with the environment and the release as dimensions
    Then the exact growth figure of document_text and its index budget are Not specified in the source documents (GAP-0993; ASM-1763)

  Scenario: AC3 The hold container is provisioned with its rule and its clearing (new, D-RCV-60)
    Given the storage account and the three document containers
    When a held file reaches its clearing event
    Then rwb-quarantine exists with a private endpoint and access for the rwb-document workload identity only
    Then a held item's file is readable through one claim-check link at a time and is never copied into a second container or a queue
    Then rwb-docs-legal keeps the immutability policy of the storage product and no blob of any container is overwritten
    Then the clearing rule states the event that clears a held file: attach, discard, or the age carried as GAP-0993
    Then the clearing job never deletes a file whose item is still open, and it records the item for the owner role instead
    Then no DOCATT entry is written for a held item or a refused attach, because no document is stored; the hold stays a status on the intake item in rwb_document

  Scenario: AC4 The topic, its retry and dead-letter topics and the ACLs are bound to the service (new, D-RCV-60)
    Given the topics provisioned by the platform event epic
    Then rwb.document.events.v1 exists with 12 partitions, replication factor 3, 7-day retention and the key caseId
    Then the three retry topics at 1 min, 10 min and 1 h and the .dlt topic exist with the same partition count
    Then the rwb-document principal writes rwb.document.events.v1 and rwb.decision-record.v1 and reads no topic of another service
    Then the consumer groups of rwb-case and rwb-agent read rwb.document.events.v1 and nothing else of this service
    When the rwb-document principal writes another service's topic
    Then the write is refused and the attempt is audited
    Then no Recovery ACL opens an ACE PII logging topic

  Scenario: AC5 The secret layout and the identity bindings rotate under a runbook entry (new, D-RCV-60)
    Given the key store of the environment
    Then the rwb-document login, the Kafka credential, the Temporal mTLS material and the storage identity binding are held there and bound to the workload identity
    Then a secret scan of the values, the scripts and the runbook finds no secret and no connection string
    When a credential or a certificate reaches its rotation point
    Then the rotation entry stages the new version, switches the consumer and retires the previous version
    Then a dependency with an expired credential fails closed and the pod reports not ready

  Scenario: AC6 The route is private and the scanning capacity bounds the intake (new, D-RCV-60)
    Given the network rules and the scanning product of the environment
    Then the service reaches rwb-case, rwb-decision, the Kafka brokers, the Temporal frontend and Blob over private endpoints resolved by private DNS
    Then no public inbound rule answers on the service and egress is admitted to the named endpoints only
    Then every inbound file is scanned before it enters the matcher, and an unscanned item waits in rwb-quarantine
    Then the scan capacity of the environment is a value and the queue age alert is wired to it
    When a connection arrives from outside the allow-list
    Then it is refused before authentication and logged

  Scenario: AC7 The story registers no Schedule, builds no matcher and writes no business rule (new, D-RCV-60)
    Given the Temporal Schedule and the matcher code of rwb-document
    When the release of this story is inspected
    Then this story registers no Schedule, builds no matcher and writes no business rule
    Then the ledger completeness check runs on the ledger ingest window of DP-06 with no Temporal Schedule and no cron entry of this service

  Scenario: AC8 The provided operations answer 401, 403 and 404 as the contract states (new, D-RCV-60)
    Given a provided operation of rwb-document is called
    When the call is unauthenticated, not permitted or names an unknown resource
    Then the answers 401, 403 and 404 match the contract, which is Not specified in the source documents (NEWAC-RWB-P5-E1032-INF-AC8)

  Scenario: AC9 A consumed call that fails or does not answer is handled as the contract states (new, D-RCV-60)
    Given a consumed call of rwb-document to rwb-case, rwb-decision or the Temporal frontend
    When the call fails or does not answer
    Then the retry, timeout and fallback of the call are Not specified in the source documents (NEWAC-RWB-P5-E1032-INF-AC9)
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One worker pool polls one task queue: queue `rwb-document` in namespace `rwb-recovery`, and no other queue | Arch v5 slides 20, 41 and 44; DP-02 |
| BR2 | The intake cadence is 15 minutes in business hours (JOB-12), served by a Temporal Schedule and not by a Quartz job or a shared scheduler | Arch v5 slide 44; FSD P5 AC-BG-P5-012-01; DP-10 |
| BR3 | The OCR text lives in `document_text` in `rwb_document` only; it is never copied to a container, a topic or a workflow payload | DP-01; Arch v5 slide 11 |
| BR4 | Three containers exist with one rule each: `rwb-docs` standard, `rwb-docs-legal` write-once, `rwb-quarantine` hold; no blob is overwritten and a held file is read through one claim-check link at a time | RWB-P5-E1024-APP; Arch v5 slide 11 |
| BR5 | Every event topic has three retry topics and one dead-letter topic, and the ACLs are least privilege and separate from the ACE PII logging topics | Arch v5 slides 11 and 21; DP-09 |
| BR6 | No secret in code, configuration, a values file or a script; the four secret classes live in the key store behind the workload identity and rotate under a written entry | NFR-052; Arch v5 slide 35 |
| BR7 | Every dependency is reached over a private endpoint resolved by private DNS, with no public inbound rule on the service | Arch v5 slide 35 |
| BR8 | Every inbound file is scanned before it enters the matcher; the scan rate bounds the intake rate and an unscanned item waits in the hold container | FSD P5 A2.18; RWB-P5-E1041-APP |
| BR9 | Capacity is provisioned for the volume the sources state: about 860,000 documents a year (NFR-004) and 5.8 million documents and 2.8 TB by 2031 (NFR-069), including every held document | NFR-004; NFR-069 |
| BR10 | This story provisions capacity, storage, a container rule, a topic binding, an identity, a route and a scan: it registers no Schedule, builds no matcher and writes no business rule | Arch v5 slides 16, 38 and 44; Template and Rules §R7.2 s17 |

### 9. State transitions

Container lifecycle.

| From | Event | Condition | To |
|---|---|---|---|
| Requested | Provisioning approved | The identity, the private endpoint and the policy are known | Provisioned |
| Provisioned | Identity bound | The workload identity resolves to read and write on the container | In use |
| In use | Policy changed | The storage product changes the immutability policy of `rwb-docs-legal` | Changing |
| Changing | Policy in force | No blob write is in flight and no version depends on the earlier policy | In use |
| In use | Container retired | No item refers to a file of the container and the retention has elapsed | Retired |

Held file.

| From | Event | Condition | To |
|---|---|---|---|
| Received | Scan clean | The file passed the scan and the item row exists | In the hold container |
| In the hold container | Match runs | The item is selected by `matchStep` | Read by the matcher |
| In the hold container | Item attached | The store wrote the document | Cleared from the hold container |
| In the hold container | Item discarded | A reviewer discards it with a reason | Cleared from the hold container |
| In the hold container | Age rule reached | The item is still open and the age rule of the container is met | Reported to the owner role, not deleted |

Worker pool.

| From | Event | Condition | To |
|---|---|---|---|
| Provisioned | Backlog rises | The queue backlog passes the threshold value | Scaling out |
| Scaling out | Backlog clears | The backlog falls below the threshold | At floor |
| At floor | Ceiling reached | The backlog keeps rising at the ceiling | Saturated |
| Saturated | Capacity raised | The ceiling value is raised and applied | Scaling out |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SCB IT infrastructure | Owns the story, the compute, the storage budgets, the three containers, the identity bindings, the route and the scan capacity |
| ACE platform team | Owns the brokers, the schema subjects, the quotas and the namespace; approves every ACL change |
| Platform team | Owns the key store, the workload identity, the private DNS zones and the storage account |
| Security | Owns the access policy, the rotation requirement, the secret scan and the public-access scan; approves any relaxation |
| rwb-document owner | Consumes the queue, the storage and the container references; owns the matcher, the store and the migration |
| rwb-case and rwb-agent owners | Consume `rwb.document.events.v1` through their groups; they never write it |
| Data steward | Confirms that no topic, no container and no metric carries personal data beyond the ruled path |
| RW-AUDIT and RW-SECADM | Read the ACL trail, the key-rotation trail and the public-access scan |

The replica counts, the request and limit sets, the storage budgets, the clearing age, the backlog threshold and the scan rate are Not specified in the source documents (GAP-0993; ASM-1763). The rwb-document login name is Not specified in the source documents either; it is held as a secret reference and never written in a values file.

### 11. Data

| Resource | Setting | Source | BR Field ID |
|---|---|---|---|
| Worker pool | Queue `rwb-document` in namespace `rwb-recovery`, KEDA on the queue backlog, one floor poller, a ceiling, a request and limit set per activity, all as environment values | Arch v5 slides 20 and 44; GAP-0993 | BR1, BR2 |
| Database storage | `document_text` one row per page with its quality; `document_intake` one row per file; sized against NFR-004 and NFR-069 | TSD P5 T3.1; NFR-004; NFR-069 | BR3, BR9 |
| Index budget | `document_text (intake_id, page_no)`; `document_intake (match_status, received_at)` for the held set and for the pending set; `document_intake (file_sha256)` | TSD P5 T3.1; RWB-P5-E1032-APP section 13 | BR3, BR9 |
| Containers | `rwb-docs` standard, `rwb-docs-legal` write-once under the storage product's immutability policy, `rwb-quarantine` hold for intake files | RWB-P5-E1024-APP; Arch v5 slide 11 | BR4 |
| Hold rule | One claim-check read at a time through the storage product; cleared on attach, discard or the age rule; never deleted while the item is open | Arch v5 slide 11; GAP-0993 | BR4 |
| Topic binding | `rwb.document.events.v1` with 12 partitions, replication factor 3, 7-day retention, key caseId, three retry topics and one `.dlt` topic; `rwb.decision-record.v1` as the shared topic | Arch v5 slides 11 and 42; DP-09 | BR5 |
| ACLs | Producer: rwb-document on its own topic and the shared topic. Consumers: rwb-case and rwb-agent on `rwb.document.events.v1`. No ACL on a PII logging topic | Arch v5 slides 21, 35 and 42 | BR5 |
| Secrets | The rwb-document login, the Kafka credential, the Temporal mTLS material and the storage identity binding, in the key store behind the workload identity | NFR-052; Arch v5 slide 35 | BR6 |
| Network | Private DNS and private endpoints for `rwb-case`, `rwb-decision`, the brokers, the Temporal frontend and Blob; no public inbound rule; egress to the named endpoints only | Arch v5 slide 35 | BR7 |
| Scan capacity | The scanning product call of RWB-P5-E1041-APP, its throughput as a value, and the queue-age alert wired to it | FSD P5 A2.18; GAP-0993 | BR8 |
| Observability hooks | Queue backlog and age, batch duration against the 15-minute cadence, storage and index size, held-file age, retry and `.dlt` counts, dependency health; no page text and no personal data | ADR-023; CTL-11 | BR9 |
| Absent by design | No shared Quartz scheduler, no shared schema, no second copy of OCR text, no public inbound rule, no data-lake route, no ACE view grant | D-RCV-35 U1; ADR-010; DP-01; DP-05; DP-17 | BR2, BR3, BR7 |

The names, numbers and sizes of the table above are environment values of the resource files in section 13; they are Not specified in the source documents (GAP-0993; ASM-1763) and this story fixes only their shape and the rule that no value is written in code. Each value is set per environment from the SIT measurement and the scan product throughput, and recorded in the environment files of section 13.

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Owner | Notes |
|---|---|---|---|
| None | — | — | The infrastructure provides no REST operation and publishes no path to rwb-document.yaml. The four intake operations of 12.1 of RWB-P5-E1032-CON are the app story's; this story provisions the capacity they run on |

#### 12.2 REST operations consumed

| Method | Path | Owner | Story | Note |
|---|---|---|---|---|
| None | — | — | — | The infrastructure calls no service operation. The routes it provisions are used at run time by the app story's clients to `rwb-case` and `rwb-decision`, and the container references are injected by RWB-P5-E1032-OPS |

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| None | — | — | — | `rwb.document.DocumentAttached.v1` on `rwb.document.events.v1` is published by the app story; this story provisions the topic, the retry topics, the `.dlt` topic and the ACLs and holds no outbox |

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| None | — | — | The service consumes no event on this path; the trigger is the 15-minute Schedule |

#### 12.5 Workflows and activities

| Name | Kind | Queue | Note |
|---|---|---|---|
| None | — | — | No workflow and no activity is registered by this story; `DocumentIntakeWorkflow` and its `matchStep` activity are owned by RWB-P5-E1049-APP and RWB-P5-E1032-APP and run on queue `rwb-document`, which this story only sizes |

#### 12.6 Schedules

| Schedule | Workflow | Queue | Interval | Note |
|---|---|---|---|---|
| None | `DocumentIntakeWorkflow` | `rwb-document` | Every 15 minutes in business hours (JOB-12) | This story registers no Schedule; it provisions the compute the Schedule needs and the backlog rule that scales it. The Schedule is registered from the values of RWB-P5-E1032-OPS. Overlap policy and catch-up are Not specified in the source documents (GAP-0994). The business-hours window is Not specified in the source documents (GAP-0994). The run-failure, held-item age, KEDA and consumer-lag thresholds are environment values, Not specified in the source documents (GAP-0994). The lag alert message identifier is Not specified in the source documents (GAP-0994) |

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| rwb_case.case_document_link | P5 | The `rwb_document` schema and the rwb-document login are RWB-PLT-DB's and the migration is RWB-PLT-E1044-CON's, applied by RWB-P5-E1032-OPS. This story's migration V1032_1 creates rwb_case.case_document_link with case_id, document_id, checklist_state, extracted_field_count, linked_at and source_event_id, a unique key on (case_id, document_id) and no foreign key across services; field IDs Not specified in the source documents (GAP-0742). It creates no other table, column, index or grant and sizes the storage and the index budget of `document_intake` and `document_text` |

#### 12.8 Contract fakes

| Fake | Story | Used for |
|---|---|---|
| None | — | No fake is provisioned. The tests use a throwaway broker, a storage stub for the hold rule, a Temporal stub for the queue and the dependency stubs of the app story's contract |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None | No operation is provided or consumed by the infrastructure; the routes are used by the app story |
| Kafka | 1 topic bound with 3 retry topics and 1 dead-letter topic, 0 produced and 0 consumed here | The producer ACL of rwb-document and the consumer ACLs of rwb-case and rwb-agent |
| Temporal | 0 workflows, 0 activities, 1 queue sized | Queue `rwb-document` in namespace `rwb-recovery`; the pool and the KEDA rule serve the 15-minute Schedule |
| File | 3 containers and 1 hold rule | `rwb-docs`, `rwb-docs-legal`, `rwb-quarantine`; one claim-check read at a time and a clearing rule; no second copy of the OCR text |

### 13. Solution plan

**Deliverables.** `infra/compute/workers.yaml` (the pool, the KEDA rule, the floor and the ceiling, the request and limit set, the queue and the namespace), `infra/storage/database.yaml` (the storage and index budget of `document_intake` and `document_text`), `infra/storage/containers.yaml` (the three containers, their access rule, the hold rule and the clearing rule), `infra/kafka/bindings.yaml` (the topic settings, the retry and `.dlt` verification, the producer and consumer ACLs), `infra/security/identity.yaml` (the workload identity bindings, the four secret classes and the rotation entries), `infra/network/rules.yaml` (the private endpoints, the private DNS records, the egress allow-list and the absence of a public inbound rule), `infra/scan/capacity.yaml` (the scan rate and the queue-age alert) and `runbooks/hold-and-scan.md` (the hold rule, the clearing step, the scan capacity check and the escalation).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON (of the app story) |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON (of the app story) |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON (of the app story) |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON (of the app story) |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON (of the app story) |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON (of the app story) |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON (of the app story) |

Day 1 dependencies from the pattern table, built against their fakes on Day 1; the metadata rows keep the dependencies the work package fixes: H RWB-PLT-E1027-CON, H RWB-PLT-E1042-CON, H RWB-PLT-E1043-CON, H RWB-PLT-TE006-CON, H RWB-PLT-E1071-CON, H RWB-PLT-E1044-CON, H RWB-PLT-N001-CON, C RWB-P3-E1042-CON, C RWB-P3-E1043-CON and the authorise contract RWB-P4-E1037-CON.

DP-01 is applied by sizing one schema and one login: `document_intake` and `document_text` live in `rwb_document`, no cross-schema read is provisioned and no ACE view is granted. DP-03, DP-06, DP-07 and DP-09 appear because the capacity this story provisions carries the paths those patterns run on: the decision record, the parameters, the lists and the attach event all need the private routes, the identity and the topic binding that are provisioned here; their H dependencies are the app story's and are not carried by this story. DP-05 is applied by absence: no grant, no route and no view for this service, because only rwb-source-data reads ACE data. DP-10 is the substantive change: the Quartz job on a shared scheduler becomes a Temporal Schedule on queue `rwb-document`, so this story sizes a worker pool against a queue and a backlog rather than a scheduler table, and it registers no Schedule of its own. DP-11 fixes the four internal routes to private endpoints with a 2 s client budget. DP-15 keeps the migration with the service sequence; this story's only table is rwb_case.case_document_link from migration V1032_1, with no other table and no grant. DP-19 records that the reviewer's list is reached through the gateway-bff composite route, and the only network consequence here is that the service answers the edge privately.

**Build steps**

1. Write the compute inventory: the queue, the namespace, the KEDA rule, the floor and the ceiling, and the request and limit set of `matchStep`.
2. Size the storage: the page rows, the item rows, the three indexes and the growth budget against NFR-004 and NFR-069.
3. Provision the three containers, the private endpoint of each and the access rule that names the workload identity only.
4. Write the hold rule: one claim-check read at a time, the clearing events, the age rule and the rule that an open item is reported and never deleted.
5. Verify the topic settings and the retry and `.dlt` topics against RWB-PLT-N002-INF, and bind the producer and consumer ACLs.
6. Place the four secret classes in the key store, bind them to the workload identity and write the four rotation entries.
7. Apply the private endpoints, the private DNS records and the egress allow-list, and run the public-access scan that proves no inbound rule answers.
8. Set the scan rate as a value, wire the queue-age alert and add the hold-and-scan runbook entry that names the scan capacity as the cause of a rising queue.
9. Hand the queue, the storage budget, the container references, the identity and the scan rate to the app and operations stories, and run the six tests of section 16.

**Done when.** The pool scales on the queue backlog and keeps the 15-minute cadence in a replayed business-hour window, the storage and index budgets are measured and alerting, the three containers exist with their rule and the clearing rule is exercised, the topic and its four derived topics carry the ACLs of BR5, no secret appears in a values file or a script, the public-access scan finds no inbound rule, the scan capacity bounds the intake, and the six tests of section 16 pass against the provisioned state.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-E1032-INF-01 | A principal attempts an operation its ACL does not allow | The action is not authorised on the topic {topic}. |
| MSG-P5-E1032-INF-02 | The worker pool is saturated, a dependency is not ready, or a credential has expired | The intake path is not ready: {component}. Follow the rotation or capacity entry of the runbook. |
| MSG-P5-E1032-INF-03 | The storage or index budget, or the scan capacity, is passed | The intake path is at its {resource} budget. Raise it or follow the runbook entry. |
| MSG-P5-E1032-INF-04 | A held file is unreachable or past its age rule | The held file of item {item} needs attention. It is in the hold container. |

The four messages are the infrastructure texts of this story and are new; no legacy business message is renumbered or reworded by them. The business messages of section 14 of the app story are unchanged, and a refused match is reported to the operator through the hooks of AC1 to AC6 and, at run time, through MSG-GEN-006 of the app story naming "Case service".

### 15. Screens and states

None — the infrastructure has no screen of its own. The operator surfaces are the cluster and the queue views, the workbook "Recovery jobs" of the observability epic, the dashboards and the runbook of RWB-P5-E1032-OPS, and the SCR-31 Document review queue that the app story serves through the gateway-bff composite route. The states of section 9 are resource and container states, not screen states.

This infrastructure story has no screen; the SCR-31 states are in RWB-P5-E1032-CON (CG-ALL-5843).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P5-E1032-INF-01 | AC1, BR1, BR2 | Integration | A replayed business-hour backlog on queue `rwb-document`; every 15-minute batch finishes before the next; the KEDA floor and ceiling are values |
| TC-P5-E1032-INF-02 | AC2, BR3, BR9 | NFR | The page rows and item rows of a synthetic month; the three indexes exist; the storage and index series carry the environment and the release |
| TC-P5-E1032-INF-03 | AC3, BR4 | Contract | `rwb-quarantine` provisioned with a private endpoint and one identity; one claim-check read at a time; the clearing on attach, discard and age; no delete of an open item |
| TC-P5-E1032-INF-04 | AC4, BR5 | Contract | The topic settings and the four derived topics; the producer ACL and the two consumer groups; a foreign write refused and audited; no PII logging topic in any ACL |
| TC-P5-E1032-INF-05 | AC5, BR6 | NFR | The four secret classes bound to the workload identity; a secret scan clean; a rotation cycled; an expired credential fails closed and the pod reports not ready |
| TC-P5-E1032-INF-06 | AC6, BR7, BR8 | Integration | Private endpoints and private DNS for the five dependencies; an outside connection refused; every file scanned before the matcher; the scan rate and the queue-age alert wired |
| TC-P5-E1032-INF-07 | 12.7, BR9 | Contract | Boundary: the migration V1032_1 creates only rwb_case.case_document_link and no other table, column, index or grant; the link key is (case_id, document_id) and no foreign key crosses a service |
| TC-P5-E1032-INF-08 | AC7, BR10 | Contract | This story's release inspected; no Schedule registered, no matcher built and no business rule written |
| TC-P5-E1032-INF-09 | AC8 | Contract | Not specified in the source documents (NEWAC-RWB-P5-E1032-INF-AC8) |
| TC-P5-E1032-INF-10 | AC9 | Integration | Not specified in the source documents (NEWAC-RWB-P5-E1032-INF-AC9) |

### 17. Guardrails

- No business value in a resource file: the patterns, the threshold, the type list, the paging default and the clearing policy of a business rule stay parameters or reference rows, never a literal in the infrastructure.
- No personal data in a file name, a manifest, a log, a trace attribute or an alert: identifiers, counts, page counts, sizes and hashes only.
- No second copy of OCR text: `document_text` is the only store, no container and no topic receives the text, and the hold container keeps the file and not the text (BR3).
- No secret in code, configuration, a values file or a script; the four secret classes are read with the workload identity (BR6, NFR-052).
- No public inbound rule and no open egress: every dependency is reached over a private endpoint resolved by private DNS (BR7).
- No ACE grant and no ACE view for this service; only rwb-source-data reads the views (DP-05).
- No data-lake endpoint, route or landing container is provisioned, because the data lake is removed (DP-17).
- A held file is never deleted while its item is open: it is reported to the owner role by the clearing job (BR4).
- An item is never matched unscanned: the scan is a condition of entering the matcher (BR8).
- No Schedule, no workflow and no activity is registered by this story; the queue is sized and the Schedule is the deployment story's (BR10).

### 18. Traceability

| Requirement ID | Requirement (short) | Infrastructure element | Test cases |
|---|---|---|---|
| Arch v5 slide 16 | rwb-document runs `DocumentIntakeWorkflow` on queue `rwb-document` and writes `rwb.document.events.v1` | The worker pool, the queue binding and the topic binding | TC-P5-E1032-INF-01, TC-P5-E1032-INF-04 |
| Arch v5 slide 38 | Wave 0 provides the template, the schemas and logins, the Kafka topics and ACLs and Temporal before the wave 1 services | The bindings this story verifies against the platform and the namespace it consumes | TC-P5-E1032-INF-01, TC-P5-E1032-INF-04 |
| Arch v5 slide 44 | JOB-12 Document intake runs every 15 minutes, owned by rwb-document | The pool, the KEDA rule and the cadence test | TC-P5-E1032-INF-01 |
| Arch v5 slide 11 | Blob with a claim-check link for one file, retry topics at 1 min, 10 min and 1 h then `.dlt`, 2 s REST budget | The three containers, the hold rule, the topic binding and the private routes | TC-P5-E1032-INF-03, TC-P5-E1032-INF-04, TC-P5-E1032-INF-06 |
| Arch v5 slide 35 | Zero trust: private access, workload identity, keys in the key store | The identity layout, the private endpoints and the secret scan | TC-P5-E1032-INF-05, TC-P5-E1032-INF-06 |
| NFR-004 | The document store holds about 860,000 documents in 2027, rising with 15 percent inflow growth a year | The storage and index budget | TC-P5-E1032-INF-02 |
| NFR-069 | The document hub holds about 5.8 million documents and 2.8 TB by the end of 2031, including every version and held document | The storage budget and the hold container capacity | TC-P5-E1032-INF-02, TC-P5-E1032-INF-03 |
| NFR-052, NFR-053 | Secrets in the key store and never in code or configuration; data encrypted at rest and in transit | The four secret classes, the identity bindings, TLS and the secret scan | TC-P5-E1032-INF-05 |
| ADR-010, DP-05 | Only rwb-source-data reads ACE data | No ACE grant and no ACE route provisioned | TC-P5-E1032-INF-06 |
| ADR-023 | Observability per service | The hooks of section 11 and the queue-age alert | TC-P5-E1032-INF-01, TC-P5-E1032-INF-02 |
| REQ-DCM-007, REQ-DCM-005, REQ-DRI-004 | The attach path this capacity serves: one clear case attaches, an uncertain one is held, every decision is recorded | The pool, the storage, the hold rule and the topic binding the three behaviours depend on | TC-P5-E1032-INF-01, TC-P5-E1032-INF-03, TC-P5-E1032-INF-04 |

### 19. Out of scope

- The matcher, the activity, the two attach services and the four operations (RWB-P5-E1032-APP).
- The contract documents, the shapes, the event schema and the fakes (RWB-P5-E1032-CON).
- The chart, the values files, the Schedule registration, the dashboards, the alerts and the runbook of the deployment (RWB-P5-E1032-OPS).
- The `rwb_document` schema, the login and the Flyway sequence (RWB-PLT-DB, RWB-PLT-E1044-CON); this story sizes the storage and creates no table.
- The standard Blob account, key store and MFT resources (RWB-PLT-N012-INF) and the topic set with its retry and dead-letter topics (RWB-PLT-N002-INF); this story consumes and verifies them.
- The Temporal namespace, its certificates and the codec (RWB-PLT-N003-INF).
- The scanning product itself and its rule set (RWB-P5-E1041-APP); this story provisions the capacity around it.
- The dashboards, the alert routing and the runbook set of the platform (RWB-PLT-N005-OPS, RWB-PLT-E1056-OPS); this story adds the entries its own resources need.
- The real cross-service journey of the path (RWB-ITG-E1032-ITG).
- The replica counts, the request and limit sets, the storage budgets, the clearing age, the backlog threshold and the scan rate (GAP-0993).
