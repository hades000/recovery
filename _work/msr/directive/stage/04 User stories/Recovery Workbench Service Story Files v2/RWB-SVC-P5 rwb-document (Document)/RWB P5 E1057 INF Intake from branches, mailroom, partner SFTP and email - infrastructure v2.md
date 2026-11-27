# RWB-P5-E1057-INF Intake from branches, mailroom, partner SFTP and email

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1057-INF |
| Work type | INF (Infrastructure) |
| Suggested owner | SCB IT infrastructure (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-057 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P5-R |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P5-E1057-INF-16); the squad sizes it at refinement |
| Depends on (build) | None |
| Contract dependencies | RWB-P5-E1057-CON (build status Not started) |
| Contract version | 5.0.0 (Recovery Workbench API Specification v5, rwb-document.yaml, info.version) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-020, FR-P5-022, FR-P5-023) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-057 for rwb-document. The legacy story assumed four channels configured as Spring properties on a single monolith node, a shared scheduler, a shared schema and an operator who could open the job record in the database. On the infrastructure side this story provisions the branch-folder, mailroom, partner SFTP and mailbox pickup channels as environment configuration with their credentials and their folder lifecycle, the compute of the intake workers against queue `rwb-document`, the storage and the hold container `rwb-quarantine` with its clearing rule, the topic `rwb.document.events.v1` with its retry and `.dlt` topics and its least-privilege ACLs, the managed identity and the secret layout, the partner file route and the DMZ position, and the scanning capacity that bounds the intake. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (14 resolved, 14 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **infrastructure engineer**, I want **the channel-intake path of `rwb-document` provisioned as infrastructure — the branch scanner folders and the mailroom folder on the bank file service, the partner SFTP inbound root with one subfolder per partner code and its PGP and key handling, the recovery mailboxes and the mailbox reader identity, the intake worker pool that serves the 15-minute business-hours run on queue `rwb-document`, the storage and the hold container `rwb-quarantine` with its clearing rule, the topic `rwb.document.events.v1` with its three retry topics, its `.dlt` topic and its least-privilege ACLs, the workload identity and the four secret classes of the path, the private route to `rwb-case`, `rwb-partner` and Blob with no public inbound rule, and the scanning capacity that bounds the rate at which files enter the matcher**, so that **the pickup activity runs on Day 1 against provisioned folders, mailboxes, queue and storage, a file that comes from a partner over the DMZ path reaches the hold container without a public endpoint anywhere, and no secret, no partner key and no mailbox credential sits in a values file or in a script**.

The legacy story had one paragraph for this work: the channels "are set per environment by the platform administrator in properties", the mailboxes "are read by the SY-OCR managed identity", the intake and quarantine containers "exist and SY-OCR writes to the intake container by managed identity", and the partner panels "are loaded". Under D-RCV-60 each of those is provisioned separately and none of them is a property of a monolith node any more:

- the four channels become four environment configuration blocks of one service deployed on AKS in the `rwb-recovery` namespace, with their own credentials (ASM-1844);
- the SFTP inbound root becomes a platform MFT/SFTP resource with one subfolder per partner code and PGP for the outside party, and it is the same file path the platform provisions for the outside file transfers of the architecture (Arch v5 slide 11; ASM-1845);
- the mailboxes become a mailbox reader identity with its own grant and its own scope, because reading a shared recovery mailbox is a permission and not a folder (ASM-1846);
- the intake compute becomes a Temporal worker pool on queue `rwb-document` scaled on the queue backlog, because the trigger is a Schedule and not a Quartz row (DP-10);
- the intake container and the quarantine container are one hold container `rwb-quarantine` with one rule and one clearing step (RWB-P5-E1032-INF);
- the partner side of the network becomes an explicit DMZ decision, because partners reach the bank only through the partner gateway, and a partner file path that is not the gateway must be shown to be private as well (Arch v5 slide 35; ASM-1847);
- the scan becomes a capacity, because the intake rate is bounded by the scan rate and not by the matcher (FSD P5 A2.18; ASM-1849).

The path has one property that shapes the provisioning: a picked-up file is personal data from the moment it is copied, and a recovery mailbox is a shared inbox nobody owns. The provisioning therefore fixes three rules alongside the capacity: a file is scanned before it is matched and the unscanned file waits in `rwb-quarantine`, the mailbox reader sees only the declared mailboxes and never the whole tenant, and the hold container is cleared by a stated rule rather than by an operator's memory.

### 2. Business rationale

About 860,000 documents arrive in 2027 (NFR-004) and the hub holds about 5.8 million documents and 2.8 TB by the end of 2031, including every version and every held document (NFR-069). Every one of them comes through this path: a branch scan, a mailroom scan, a partner file or a mailbox attachment becomes one `document_intake` row and one file in the hold container, and then a page set in `document_text` and a document on a case. If the worker pool is sized for a demonstration, the 15-minute run falls behind and the channels accumulate; if a branch folder has no lifecycle, a processed folder fills the branch file share and the scanner stops writing; if a mailbox is read with a grant wider than the four declared mailboxes, a personal inbox is read by a machine identity; if the partner subfolder is reachable from anywhere but the private path, a partner's evidence file is one hop from the internet.

The private path matters as much. Zero trust requires the service to reach `rwb-case`, `rwb-partner`, the Kafka brokers, the Temporal frontend and Blob over private endpoints with a workload identity (Arch v5 slide 35; NFR-052, NFR-053). A public endpoint added for a test is a security finding that survives to production, and a partner SFTP key pasted into a values file turns a rotation into a rebuild.

The 15-minute cadence is the legacy one and the architecture one: JOB-12 runs every 15 minutes, owned by `rwb-document` (Arch v5 slide 44; FSD P5 AC-BG-P5-013-01). The legacy story says "every 15 minutes in business hours"; the architecture slide gives no business-hours qualifier, so the Schedule and the compute are sized for the business-hours cadence and the difference is recorded as `GAP-1014`.

The scan capacity is the one element the legacy story names only as an existing step: every inbound file is scanned before it is stored (FSD P5 A2.18; RWB-P5-E1041-APP), so the intake rate is bounded by the scan rate and not by the OCR or the matcher. This story provisions that capacity and states the rule that an item waits in the hold container rather than entering the matcher unscanned.

### 3. Preconditions

- The platform subscription, the resource group and the network (virtual network, subnets, private DNS zones) of the environment are available, and the AKS cluster of the ACE platform is reachable from the `rwb-recovery` namespace.
- The workload identity of rwb-document is registered in each environment, so every access is bound to an identity and not to a shared credential (DP-02).
- RWB-PLT-N012-INF provisions the standard Blob account, the key store and the MFT/SFTP resources; this story consumes the Blob account, the key store and the MFT/SFTP root for the channel path.
- RWB-PLT-N002-INF provisions the 20 event topics with their 60 retry topics and their 20 dead-letter topics, so `rwb.document.events.v1`, its three retry topics and its `.dlt` topic exist before this story binds the ACLs.
- RWB-PLT-N003-INF provisions the namespace `rwb-recovery`, its certificates and the payload codec, so queue `rwb-document` can be polled.
- RWB-PLT-DB provisions the `rwb_document` schema and the rwb-document login; this story creates no schema, no table and no grant, and the migration is RWB-PLT-E1044-CON's sequence applied by the release of RWB-P5-E1057-OPS.
- The partner gateway of the edge epic is in place in its DMZ, fronting `rwb-partner` with FAPI 2.0, so a partner API call has a route and a partner file path has a boundary to be measured against (Arch v5 slide 35).
- The scanning product of RWB-P5-E1041-APP exists as a service call, so the capacity provisioned here is the cluster and network capacity around it and not a scanner binary.
- The baseline RWB-P5-E1057-CON is published, so the three admin operations of the app story and their status codes are known to the network and the identity work.
- No build dependency and no contract dependency in the plan of this key; this story is Day 1 by rule (Template and Rules §R5.7).
- The release date 30 November 2026 is the legacy one and is tentative (ASM-1826), and the story carries Status Draft (realignment v1) because no approval of the realigned story is recorded (ASM-1843).

### 4. Flow

1. List what the path needs: the four channel configurations, the file-service folders and their lifecycle, the SFTP inbound root and its partner subfolders with their key material, the mailbox reader identity and its scope, the worker pool and its queue, the storage and the hold container, the topic and its four derived topics, the six service principals it talks to, the five secret classes, the network routes with their DMZ position, and the scan rate.
2. Provision the branch-folder channel: a scanner folder per branch code, a processed folder and a rejected folder per branch, the write grant the branch scanner holds and the read, move and delete grants the rwb-document identity holds, and the age rule that clears a processed folder after the stated period.
3. Provision the mailroom channel: one mailroom folder with its processed and rejected folders and the same grant pattern.
4. Provision the partner SFTP channel: the inbound root, one subfolder per partner code, the processed and rejected subfolders, the host key and the client key of each partner in the key store, the PGP key pair for the encrypted file of an outside party, and the read-only grant the partner holds on its own subfolder only.
5. Provision the mailbox channel: the four declared mailboxes, the mailbox reader identity with its application permission scoped to those mailboxes and to no other, the archive folder per mailbox, and the rule that the reader may move a message and may not delete one.
6. Size the worker pool for the 15-minute business-hours cadence: the `pickup` activity runs on queue `rwb-document`, the pool scales on the queue backlog through KEDA, and the request and limit set of the activity is fixed as values per environment.
7. Size the storage for `document_intake` and its two indexes against the 860,000 documents a year of NFR-004 and the 2.8 TB estate of NFR-069.
8. Provision the hold container `rwb-quarantine` for a picked-up file with its access rule (managed identity only), its one-file-per-link claim-check read through the storage product and its clearing rule on scan, discard or age; verify the two containers `rwb-docs` and `rwb-docs-legal` against the store's own provisioning.
9. Verify the topic `rwb.document.events.v1` with its 12 partitions, replication factor 3, 7-day retention and key caseId and its four derived topics; provision nothing new if RWB-PLT-N002-INF already did it, and bind the ACLs: the rwb-document principal writes its own topic and the shared `rwb.decision-record.v1` and reads nothing of another service.
10. Put the login, the Kafka credential, the Temporal mTLS material, the storage identity binding and the channel credentials in the key store behind the workload identity, and write the rotation entry for each class.
11. Apply the private route: private DNS and private endpoints for `rwb-case`, `rwb-partner`, the brokers, the Temporal frontend and Blob; the partner file path documented against the DMZ position of the partner gateway; no public inbound rule on the service; egress to the named endpoints only.
12. Set the scan rate as a value, wire the queue-age alert to it, and run the six tests of section 16 against the provisioned state.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A branch or mailroom folder does not exist, or the scanner's write grant is missing | The channel is reported failed, the run names the branch code and the other channels still run | MSG-P5-E1057-INF-01 | AC1 |
| X2 | The partner SFTP host key or a partner client key does not match | The handshake is refused, the subfolder is not read, and the failure counts towards the two-run alert of the app story | MSG-P5-E1057-INF-01 | AC1, AC4 |
| X3 | The mailbox reader identity has no grant on a declared mailbox, or a grant wider than the declared mailboxes | The read is refused and audited; a wider grant fails the access review and the release | MSG-P5-E1057-INF-01 | AC1, AC4 |
| X4 | The worker pool is saturated and the queue backlog grows past its threshold | The pool scales out on the backlog; if the ceiling is reached the run takes longer and the run book names the ceiling as the cause | MSG-P5-E1057-INF-02 | AC1 |
| X5 | The hold container is unreachable or refuses the write of a new file | The file stays at its channel, the run fails and no row is committed; the storage alert fires and the run book names the container | MSG-P5-E1057-INF-03 | AC2 |
| X6 | A processed or rejected folder is past its age rule | The clearing job moves the file to the archive tier and records the count; no file of a channel is deleted while a run refers to it | MSG-P5-E1057-INF-03 | AC2 |
| X7 | A principal writes to a topic it does not own, or reads a topic where the event catalogue lists no consumer | The broker refuses the operation and the attempt is audited | MSG-P5-E1057-INF-01 | AC3 |
| X8 | A credential, certificate, partner key or identity binding expires or is rotated out | The dependency fails closed, the channel reports not ready and the rotation entry restores the version; no clear-text fallback exists | MSG-P5-E1057-INF-02 | AC4 |
| X9 | A partner subfolder is reachable from a public address, or a public inbound rule appears on the service | The network scan fails the change and the release is blocked | MSG-P5-E1057-INF-04 | AC5 |
| X10 | The scan rate falls below the intake rate | Files wait in the hold container and the queue age rises; the alert fires and the run book names the scan capacity | MSG-P5-E1057-INF-03 | AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Provisions channels, folders, mailboxes, compute, storage, a container rule, a topic binding, ACLs, identity, route and scan capacity; no application code is built here and no service build blocks it |
| Negotiable | Branch codes, folder names, mailbox codes, replica counts, request and limit sets, storage budgets, the clearing age, the backlog threshold and the scan rate are environment values settled with the platform and network teams |
| Valuable | Gives the app and operations stories provisioned channels, a ruled hold container and a private path on Day 1, with no secret in a values file and no partner key in a script |
| Estimable | Four channel configurations, one worker pool, one storage and index budget, one hold container with a rule, one topic binding, one ACL set, one identity layout with five secret classes, one route set and one scan capacity |
| Small | Fits one sprint with the runbook entries and the six tests |
| Testable | Every criterion is tested against provisioned state, a refused operation, a folder rule, a route or a scan, never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Infrastructure of the channel-intake path for rwb-document

  Background:
    Given the platform subscription, the resource group and the private network of the environment are in place
    Given the workload identity of rwb-document is registered in the environment
    Given the MFT/SFTP resources and the key store of the platform are provisioned
    Given the target environment is SIT

  Scenario: AC1 The four pickup channels and the intake worker compute are provisioned (new, D-RCV-60)
    Given the branch, mailroom, partner SFTP and mailbox channels of the environment
    Then a scanner folder exists for each branch code with its processed and rejected folders, and the rwb-document identity holds read, move and delete on them and the scanner holds write only
    Then the mailroom folder exists with its processed and rejected folders and the same grant pattern
    Then the SFTP inbound root exists with one subfolder per partner code, its processed and rejected subfolders, and a read-only grant to each partner on its own subfolder only
    Then the four declared mailboxes exist and the mailbox reader identity holds an application permission scoped to those mailboxes and to no other, with move but no delete
    Then the worker pool polls the task queue rwb-document in namespace rwb-recovery and nothing else, and the pickup activity carries its request and limit set as environment values and not in code
    Then the pool scales on the queue backlog through KEDA, with a floor that keeps one poller and a ceiling that is a value
    Then each channel and the pool report the states empty, loading, error and no access
    When a business-hour backlog is replayed
    Then every batch of the 15-minute cadence finishes before the next one starts
    Then the branch codes, the folder names, the mailbox codes, the replica count, the request and limit set and the ceiling are Not specified in the source documents (GAP-1014; ASM-1848)

  Scenario: AC2 The intake storage and the hold container are provisioned with their rule and their clearing (new, D-RCV-60)
    Given the storage of rwb_document and the storage account of the environment
    When the pickup activity writes a picked-up file to the hold container
    Then document_intake carries its unique key on channel code, source reference and file hash and its indexes on the channel, the hash and the run, and the storage budget is set against the 860,000 documents a year of NFR-004 and the 5.8 million documents and 2.8 TB of NFR-069
    Then rwb-quarantine exists with a private endpoint and access for the rwb-document workload identity only
    Then a picked-up file is readable through one claim-check link at a time and is never copied into a second container or a message
    Then rwb-docs and rwb-docs-legal exist as the store provisions them, rwb-docs-legal keeps the immutability policy of the storage product and no blob of any container is overwritten
    Then the clearing rule states the three events that clear a held file: the scan result, a discard by the owner role, or the age rule carried as GAP-1014
    Then the clearing job never deletes a file whose item is still open, and it records the item for the owner role instead
    Then the processed and rejected folders of every channel carry an age rule and a move to the archive tier

  Scenario: AC3 The topic, its retry and dead-letter topics and the ACLs are bound to the service (new, D-RCV-60)
    Given the topics provisioned by the platform event epic
    Then rwb.document.events.v1 exists with 12 partitions, replication factor 3, 7-day retention and the key caseId
    Then the three retry topics at 1 min, 10 min and 1 h and the .dlt topic exist with the same partition count
    Then the rwb-document principal writes rwb.document.events.v1 and rwb.decision-record.v1 and reads no topic of another service
    Then the consumer groups of rwb-case and rwb-agent read rwb.document.events.v1 and nothing else of this service
    Then this path binds no consumer group for the pickup, because the pickup writes rows and publishes no event
    When the rwb-document principal writes another service's topic
    Then the write is refused and the attempt is audited
    Then no Recovery ACL opens an ACE PII logging topic

  Scenario: AC4 The identity, the secret layout and the channel credentials rotate under a runbook entry (new, D-RCV-60)
    Given the key store of the environment and the workload identity of rwb-document
    Then the rwb-document login, the Kafka credential, the Temporal mTLS material, the storage identity binding and the channel credentials are held there and bound to the workload identity
    Then the channel credentials are the mailbox reader secret or certificate, the partner SFTP host key, one client key per partner and the PGP key pair of the outside-party file
    Then a secret scan of the values, the scripts, the runbook and the image finds no secret, no partner key and no connection string
    When a credential, a partner key or a certificate reaches its rotation point
    Then the rotation entry stages the new version, switches the channel or the principal and retires the previous version
    Then a channel with an expired credential fails closed, reports not ready and reads nothing
    Then the mailbox permission is re-reviewed at every rotation and a wider grant blocks the release

  Scenario: AC5 The partner file route is private and the DMZ position is documented (new, D-RCV-60)
    Given the network rules, the partner gateway of the edge epic and the MFT/SFTP resources
    Then the service reaches rwb-case, rwb-partner, the Kafka brokers, the Temporal frontend and Blob over private endpoints resolved by private DNS
    Then the partner SFTP inbound root is reachable only over the private MFT/SFTP path and never from a public address, and the partner's own side reaches it outbound from its own network
    Then the document records the DMZ position: partner API traffic terminates at the partner gateway with FAPI 2.0 and partner file traffic terminates at the MFT/SFTP root, and neither reaches the service directly
    Then no public inbound rule answers on the service and egress is admitted to the named endpoints only
    When a connection arrives from outside the allow-list, on the SFTP root or on the service
    Then it is refused before authentication and logged
    Then an outside-party file is PGP-encrypted and its checksum is verified on receipt

  Scenario: AC6 The scanning capacity bounds the intake and the queue age is alerted (new, D-RCV-60)
    Given the network rules and the scanning product of the environment
    Then every inbound file is scanned before it enters the matcher, and an unscanned item waits in rwb-quarantine
    Then the scan rate of the environment is a value and the queue-age alert of the intake is wired to it
    When the scan rate is set below a replayed intake rate
    Then the queue age rises, the alert fires with MSG-P5-E1057-INF-03 naming the scan capacity, and no file enters the matcher unscanned
    Then the capacity is sized against the 15-minute cadence and the 860,000 documents a year of NFR-004
    Then the scan product and its provider are Not specified in the source documents (GAP-1014; ASM-1849)

  Scenario: AC7 This path registers no Schedule, builds no reader and writes no business rule (new, D-RCV-60)
    When this story is delivered to SIT
    Then no Temporal Schedule is registered by this path
    Then no reader is built and no business rule is written by this path

  Scenario: AC8 No REST operation is provided, so no 401, 403 or 404 answer is set here (new, D-RCV-60)
    Given this story exposes no REST operation (DP-08)
    When this story is delivered to SIT
    Then no provided operation answers 401, 403 or 404 under this story; those answers belong to RWB-P5-E1057-CON

  Scenario: AC9 A consumed call that fails or does not answer is reported, logged and held (new, D-RCV-60)
    When a consumed call to rwb-case, rwb-partner, the Kafka brokers, the Temporal frontend or Blob fails or does not answer
    Then the caller reports the failure and no file enters the matcher
    Then the failure is logged and the item stays in rwb-quarantine
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One worker pool polls one task queue: queue `rwb-document` in namespace `rwb-recovery`, and no other queue | Arch v5 slides 20, 41 and 44; DP-02 |
| BR2 | The intake cadence is 15 minutes in business hours (JOB-12), served by a Temporal Schedule and not by a Quartz job or a shared scheduler | Arch v5 slide 44; FSD P5 AC-BG-P5-013-01; DP-10 |
| BR3 | A channel is configuration and not code: a branch folder, the mailroom folder, the SFTP root and the mailboxes are environment values, and no path, address or branch code is written in a class | RWB-E1-057 section 8 BR8; DP-15 |
| BR4 | The SFTP inbound root is one subfolder per partner code and a partner holds a read-only grant on its own subfolder only | RWB-E1-057 section 8 BR4; Arch v5 slide 11 |
| BR5 | The mailbox reader identity holds a grant on the declared mailboxes only, may move a message and may never delete one | CTL-11; Arch v5 slide 35 |
| BR6 | A picked-up file lives in the hold container `rwb-quarantine` until it is scanned; it is never copied into a second container and never put in a message | Arch v5 slide 11; RWB-P5-E1041-APP |
| BR7 | Every event topic has three retry topics and one dead-letter topic, and the ACLs are least privilege and separate from the ACE PII logging topics | Arch v5 slides 11 and 21; DP-09 |
| BR8 | No secret in code, configuration, a values file or a script; the five secret classes live in the key store behind the workload identity and rotate under a written entry | NFR-052; Arch v5 slide 35 |
| BR9 | Every dependency is reached over a private endpoint resolved by private DNS, and a partner file path reaches the bank only through the private MFT/SFTP route or the partner gateway in its DMZ | Arch v5 slide 35 |
| BR10 | Capacity is provisioned for the volume the sources state: about 860,000 documents a year (NFR-004) and 5.8 million documents and 2.8 TB by 2031 (NFR-069), including every held file | NFR-004; NFR-069 |
| BR11 | Every inbound file is scanned before it enters the matcher; the scan rate bounds the intake rate and an unscanned item waits in the hold container | FSD P5 A2.18; RWB-P5-E1041-APP |
| BR12 | This story provisions channels, capacity, storage, a container rule, a topic binding, an identity, a route and a scan: it registers no Schedule, builds no reader and writes no business rule (AC7) | Arch v5 slides 16, 38 and 44; Template and Rules §R7.2 s17 |

### 9. State transitions

Channel lifecycle.

| From | Event | Condition | To |
|---|---|---|---|
| Requested | Provisioning approved | The grant, the endpoint and the credential are known | Provisioned |
| Provisioned | Identity bound | The workload identity resolves to read and move on the folder or the mailbox | In use |
| In use | Credential rotated | The rotation entry stages a new version | Rotating |
| Rotating | Version switched | The channel answers with the new credential | In use |
| In use | Credential expired and not rotated | The channel fails closed | Not ready |
| Not ready | Rotation entry applied | The version is restored or advanced | In use |
| In use | Channel retired | No partner subfolder or mailbox is declared and the age rule has run | Retired |

Picked-up file.

| From | Event | Condition | To |
|---|---|---|---|
| At the channel | `pickup` accepts the file | The type, the size and the duplicate check pass | In the hold container with a row |
| In the hold container | The scan step runs | The scan answers | CLEAN and matched, or INFECTED and quarantined |
| At the channel | `pickup` refuses the file | A rule refuses it | In the rejected folder of the channel |
| In the hold container | The item is attached or discarded | The owner role resolves it | Cleared from the hold container |
| In the hold container | The age rule is reached | The item is still open | Reported to the owner role, not deleted |
| In a processed folder | The age rule is reached | The file has been moved for the stated period | Archive tier |

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
| SCB IT infrastructure | Owns the story, the four channels, the folders and their lifecycle, the capture compute, the storage budgets, the hold container, the identity bindings, the route and the scan capacity |
| ACE platform team | Owns the brokers, the schema subjects, the quotas and the namespace; approves every ACL change |
| Platform team | Owns the key store, the workload identity, the private DNS zones, the storage account and the MFT/SFTP resources |
| Network and security | Own the partner gateway and its DMZ, the private endpoints, the public-access scan and the PGP requirement; approve any relaxation |
| Branch operations and the mailroom | Own the scanners and the folders their scan writes into; confirm the branch codes and the mailroom folder |
| Partner and agency manager | Confirms the partner codes, the SFTP subfolders and the PGP keys of the partners (partner portal CRUDA) |
| rwb-document owner | Consumes the queue, the storage, the container references and the channel configuration; owns the pickup, the run record and the migration |
| rwb-case and rwb-agent owners | Consume `rwb.document.events.v1` through their groups; they never write it |
| Data steward | Confirms that no folder, no mailbox, no topic and no metric carries personal data beyond the ruled path |
| RW-AUDIT and RW-SECADM | Read the ACL trail, the key-rotation trail, the mailbox permission review and the public-access scan |

The branch codes, the folder names, the mailbox codes, the replica counts, the request and limit sets, the storage budgets, the clearing age, the backlog threshold and the scan rate are Not specified in the source documents (GAP-1014; ASM-1848). The rwb-document login name is Not specified in the source documents (GAP-1014) either; it is held as a secret reference and never written in a values file. This story exposes no REST operation and calls no rwb-access authorise check (DP-08); the channel path is authorised by the workload identity and the ACLs of section 11. The run record, the rerun operation and the fields of the run answer are owned by RWB-P5-E1057-CON; the partner check goes through the rwb-partner contract with a fake and carries no C row (GAP-1012). The JOB-12 run read and rerun go through the rwb-source-data admin job contract, and the four channels are proven through the intake contract and DocumentIntakeWorkflow (GAP-0367). The business-hours window, the overlap policy and the catch-up window of the intake Schedule are Not specified in the source documents (GAP-1012); the Schedule owner confirms them before the wave 1 release. The mail service of the mailbox channel, the partner DMZ position and the scan rate are Not specified in the source documents (GAP-1014); the network and security owners confirm them before the wave 1 release.

### 11. Data

| Resource | Setting | Source | BR Field ID |
|---|---|---|---|
| Branch channels | One scanner folder per branch code with a processed and a rejected folder; the scanner holds write, the service holds read, move and delete; an age rule on the processed folder | RWB-E1-057 section 3; GAP-1014 | BR3 |
| Mailroom channel | One mailroom folder coded MAILROOM with its processed and rejected folders and the same grants | RWB-E1-057 section 3; FSD P5 A2.13 | BR3 |
| Partner SFTP channel | The inbound root, one subfolder per partner code, its processed and rejected subfolders, the host key, one client key per partner and the PGP key pair of an outside-party file | RWB-E1-057 section 3; Arch v5 slide 11 | BR4, BR9 |
| Mailbox channel | The declared recovery mailboxes, the archive folder per mailbox, the reader identity with a scoped application permission, move but no delete | RWB-E1-057 section 3; CTL-11; ASM-1846 | BR5 |
| Worker pool | Queue `rwb-document` in namespace `rwb-recovery`, KEDA on the queue backlog, one floor poller, a ceiling, a request and limit set per activity, all as environment values | Arch v5 slides 20 and 44; GAP-1014 | BR1, BR2 |
| Database storage | `document_intake` one row per file with its seven intake columns and its two indexes; sized against NFR-004 and NFR-069 | TSD P5 T3.1; NFR-004; NFR-069 | BR10 |
| Hold container | `rwb-quarantine`, a private endpoint, one claim-check read at a time, cleared on scan, discard or the age rule, never deleted while the item is open | Arch v5 slide 11; RWB-P5-E1032-INF | BR6 |
| Topic binding | `rwb.document.events.v1` with 12 partitions, replication factor 3, 7-day retention, key caseId, three retry topics and one `.dlt` topic; `rwb.decision-record.v1` as the shared topic | Arch v5 slides 11 and 42; DP-09 | BR7 |
| ACLs | Producer: rwb-document on its own topic and the shared topic. Consumers: rwb-case and rwb-agent on `rwb.document.events.v1`. No consumer group for the pickup. No ACL on a PII logging topic | Arch v5 slides 21, 35 and 42 | BR7 |
| Secrets | The rwb-document login, the Kafka credential, the Temporal mTLS material, the storage identity binding and the channel credentials, in the key store behind the workload identity | NFR-052; Arch v5 slide 35 | BR8 |
| Network | Private DNS and private endpoints for `rwb-case`, `rwb-partner`, the brokers, the Temporal frontend and Blob; the SFTP root on the private MFT path; the partner gateway in its DMZ; no public inbound rule; egress to the named endpoints only | Arch v5 slide 35; ASM-1847 | BR9 |
| Scan capacity | The scanning product call of RWB-P5-E1041-APP, its throughput as a value, and the queue-age alert wired to it | FSD P5 A2.18; ASM-1849 | BR11 |
| Observability hooks | Queue backlog and age, batch duration against the 15-minute cadence, channel failures per channel code, folder age, held-file age, scan rate, retry and `.dlt` counts, dependency health; no file name, no sender address and no page text | ADR-023; CTL-11 | Not specified in the source documents (DOR-RWB-P5-E1057-INF-7) |
| Absent by design | No shared Quartz scheduler, no shared schema, no second copy of a picked-up file, no public inbound rule, no tenant-wide mailbox grant, no data-lake route, no ACE view grant | D-RCV-35 U1; ADR-010; DP-01; DP-17 | BR6, BR9 |

The names, numbers and sizes of the table above are environment values of the resource files in section 13; they are Not specified in the source documents (GAP-1014; ASM-1848) and this story fixes only their shape and the rule that no value is written in code.

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Owner | Notes |
|---|---|---|---|
| None | — | — | The infrastructure provides no REST operation. The three admin operations of RWB-P5-E1057-CON are the app story's; this story provisions the capacity, the channels and the routes they run on |

#### 12.2 REST operations consumed

| Method | Path | Owner | Story | Note |
|---|---|---|---|---|
| None | — | — | — | The infrastructure calls no service operation. The routes it provisions are used at run time by the app story's client to `rwb-partner` and by the shared clients to `rwb-case` and the brokers, and the container and channel references are injected by RWB-P5-E1057-OPS |

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| None | — | — | — | This path publishes no event; `rwb.document.events.v1` and `rwb.decision-record.v1` are bound here and written by the store and by the decision-record library. This story provisions the topic, the retry topics, the `.dlt` topic and the ACLs and holds no outbox |

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| None | — | — | The service consumes no event on this path; the trigger is the 15-minute Schedule |

#### 12.5 Workflows and activities

| Name | Kind | Queue | Note |
|---|---|---|---|
| None | — | — | No workflow and no activity is registered by this story; `DocumentIntakeWorkflow` is owned by RWB-P5-E1049-APP and its `pickup` activity by RWB-P5-E1057-APP, and both run on queue `rwb-document`, which this story only sizes |

#### 12.6 Schedules

| Schedule | Workflow | Queue | Interval | Note |
|---|---|---|---|---|
| None | `DocumentIntakeWorkflow` | `rwb-document` | Every 15 minutes in business hours (JOB-12) | This story registers no Schedule; it provisions the compute the Schedule needs, the channels it reads and the backlog rule that scales it. The Schedule is registered from the values of RWB-P5-E1057-OPS |

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| None | — | The `rwb_document` schema and the rwb-document login are RWB-PLT-DB's and the migration is RWB-PLT-E1044-CON's, applied by RWB-P5-E1057-OPS. This story creates no table, no column, no index and no grant; it sizes the storage and the index budget of `document_intake` |

#### 12.8 Contract fakes

| Fake | Story | Used for |
|---|---|---|
| None | — | No fake is provisioned. The tests use a throwaway broker, a folder and SFTP fixture with a stub host key, a mailbox stub with a stub reader identity, a storage stub for the hold rule, a Temporal stub for the queue and the dependency stubs of the app story's contract |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None | No operation is provided or consumed by the infrastructure; the routes are used by the app story |
| Kafka | 1 topic bound with 3 retry topics and 1 dead-letter topic, 0 produced and 0 consumed here | The producer ACL of rwb-document and the consumer ACLs of rwb-case and rwb-agent |
| Temporal | 0 workflows, 0 activities, 1 queue sized | Queue `rwb-document` in namespace `rwb-recovery`; the pool and the KEDA rule serve the 15-minute Schedule |
| File | 4 channels, 10 folder classes and 1 hold container | Branch scanner, processed and rejected folders per branch; the mailroom, processed and rejected folders; the SFTP root with per-partner, processed and rejected subfolders; the four mailboxes with their archive folders; `rwb-quarantine` with one claim-check read at a time and a clearing rule |

### 13. Solution plan

**Deliverables.** `infra/channels/branch.yaml` and `infra/channels/mailroom.yaml` (the folder set, the grants and the age rule of each branch and of the mailroom), `infra/channels/sftp.yaml` (the inbound root, the per-partner subfolders, the host key reference, the per-partner client key references, the PGP key pair and the grants), `infra/channels/mailbox.yaml` (the four mailboxes, the archive folder, the reader identity, its scoped grant and the move-only rule), `infra/compute/workers.yaml` (the pool, the KEDA rule, the floor and the ceiling, the request and limit set, the queue and the namespace), `infra/storage/database.yaml` (the storage and index budget of `document_intake`), `infra/storage/hold.yaml` (the hold container, its private endpoint, its rule and its clearing rule, and the two store containers verified), `infra/kafka/bindings.yaml` (the topic settings, the retry and `.dlt` verification, the producer and consumer ACLs), `infra/security/identity.yaml` (the workload identity bindings, the five secret classes and the rotation entries), `infra/network/rules.yaml` (the private endpoints, the private DNS records, the DMZ position of the partner paths, the egress allow-list and the absence of a public inbound rule), `infra/scan/capacity.yaml` (the scan rate and the queue-age alert) and `runbooks/channels-hold-and-scan.md` (the channel check, the hold rule, the clearing step, the scan capacity check and the escalation).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON (of the app story) |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON (of the app story) |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON (of the app story) |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON (of the app story) |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/document/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON (of the app story) |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON (of the app story) |

DP-01 is applied by sizing one schema and one login: `document_intake` lives in `rwb_document`, no cross-schema read is provisioned and no ACE view is granted. DP-06, DP-07 and DP-09 appear because the capacity this story provisions carries the paths those patterns run on: the parameters, the lists and the idempotency rows all need the private routes, the identity and the topic binding that are provisioned here; their H dependencies are the app story's and are not carried by this story. DP-10 is the substantive change: the Quartz job on a shared scheduler becomes a Temporal Schedule on queue `rwb-document`, so this story sizes a worker pool against a queue and a backlog, provisions the four channels a poller reads, and registers no Schedule of its own. DP-11 fixes the partner read to a private endpoint with a 2 s client budget. DP-13 is applied by absence: this story exposes no REST path of its own, and the rebased base is the app story's. DP-15 keeps the migration with the service sequence, so this story creates no table and no grant. DP-19 records that the run record is reached through the gateway-bff composite route, and the only network consequence here is that the service answers the edge privately.

**Build steps**

1. Write the branch and mailroom channel inventory: the folder set per branch code, the grants, the age rule and the scanner write pattern.
2. Write the SFTP channel: the inbound root, one subfolder per partner code, the processed and rejected subfolders, the host key, one client key per partner, the PGP key pair and the read-only per-partner grant.
3. Write the mailbox channel: the four mailboxes, the archive folder, the reader identity, the scoped application permission and the move-only rule; run the permission review that proves no wider grant.
4. Write the compute inventory: the queue, the namespace, the KEDA rule, the floor and the ceiling, and the request and limit set of `pickup`.
5. Size the storage: the item rows, the unique key, the two indexes and the growth budget against NFR-004 and NFR-069.
6. Provision the hold container `rwb-quarantine` and verify the two store containers; write the clearing rule and the folder age rules.
7. Verify the topic settings and the retry and `.dlt` topics against RWB-PLT-N002-INF, and bind the producer and consumer ACLs.
8. Place the five secret classes in the key store, bind them to the workload identity and write the five rotation entries.
9. Apply the private endpoints, the private DNS records, the DMZ position of the two partner paths and the egress allow-list, and run the public-access scan that proves no inbound rule answers on the service or on the SFTP root.
10. Set the scan rate as a value, wire the queue-age alert and add the channels-hold-and-scan runbook entry that names the scan capacity as the cause of a rising queue.
11. Hand the queue, the channel configuration, the storage budget, the container references, the identity and the scan rate to the app and operations stories, and run the six tests of section 16.

**Done when.** The four channels exist with their grants and their lifecycle, the pool scales on the queue backlog and keeps the 15-minute cadence in a replayed business-hour window, the hold container exists with its rule and its clearing rule is exercised, the topic and its four derived topics carry the ACLs of BR7, no secret or partner key appears in a values file or a script, the public-access scan finds no inbound rule on the service or on the SFTP root, the mailbox grant is scoped to the four mailboxes, the scan capacity bounds the intake, and the six tests of section 16 pass against the provisioned state.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-E1057-INF-01 | A channel is not reachable, a grant is missing, a key does not match, or a principal attempts an operation its ACL does not allow | The channel or the topic {component} refused the operation. Follow the rotation or grant entry of the runbook. |
| MSG-P5-E1057-INF-02 | The worker pool is saturated, a dependency is not ready, or a credential has expired | The intake path is not ready: {component}. Follow the rotation or capacity entry of the runbook. |
| MSG-P5-E1057-INF-03 | The storage budget, the folder age or the scan capacity is passed | The intake path is at its {resource} budget. Raise it or follow the runbook entry. |
| MSG-P5-E1057-INF-04 | A public route is found on the service or on the SFTP root | A public route is open on {component}. The release is blocked until it is closed. |

The four messages are the infrastructure texts of this story and are new; no legacy business message is renumbered or reworded by them. The business messages of section 14 of the app story are unchanged, and a refused channel is reported to the operator through the run record of AC1 and, at run time, through MSG-P5-008 of the app story naming the channel code.

### 15. Screens and states

None — the infrastructure has no screen of its own. The operator surfaces are the cluster and the queue views, the folder and mailbox inventories of the file service and the mail service, the workbook "Recovery jobs" of the observability epic, the dashboards and the runbook of RWB-P5-E1057-OPS, and the SCR-44 Interface and job monitor that the app story feeds through the gateway-bff composite route. The states of section 9 are resource, channel and file states, not screen states. The SCR-44 states empty, loading, error and no access are Not specified in the source documents (CG-ALL-6085).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P5-E1057-INF-01 | AC1, BR1, BR2, BR3 | Integration | A scanner folder per branch code, the mailroom folder, the SFTP root with per-partner subfolders and the four mailboxes; the grants proven per channel; a replayed business-hour backlog on queue `rwb-document` with every 15-minute batch finishing before the next; the KEDA floor and ceiling are values; every channel and the pool report the states empty, loading, error and no access |
| TC-P5-E1057-INF-02 | AC2, BR6, BR10 | NFR | The item rows of a synthetic month; the unique key and the two indexes exist; the hold container with its private endpoint; one claim-check read at a time; the clearing on scan, discard and age; the folder age rule; no delete of an open item |
| TC-P5-E1057-INF-03 | AC3, BR7, BR12 | Contract | The topic settings and the four derived topics; the producer ACL and the two consumer groups; no consumer group for the pickup; a foreign write refused and audited; no PII logging topic in any ACL; no Schedule, reader or business rule registered by this path |
| TC-P5-E1057-INF-04 | AC4, BR4, BR5, BR8 | NFR | The five secret classes bound to the workload identity; the mailbox grant scoped to four mailboxes; a secret scan clean; a partner key and a certificate rotation cycled; an expired credential fails closed and the channel reports not ready |
| TC-P5-E1057-INF-05 | AC5, BR9 | Integration | Private endpoints and private DNS for the five dependencies; the SFTP root and the partner gateway in their DMZ positions; an outside connection refused on both; a PGP-encrypted file checksum verified |
| TC-P5-E1057-INF-06 | AC6, BR11 | Integration | The scan rate set below a replayed intake rate; the queue age rises and the alert fires with MSG-P5-E1057-INF-03; every file scanned before the matcher; the queue-age alert wired to the scan rate |
| TC-P5-E1057-INF-07 | AC2, BR10 | Contract | Boundary: no table, column, index or grant of the rwb_document schema created by this story; document_intake sized at 860,000 documents a year with 15 percent yearly inflow growth (NFR-004) |
| TC-P5-E1057-INF-08 | AC7, BR12 | Contract | No Temporal Schedule, reader or business rule registered or written by this path |
| TC-P5-E1057-INF-09 | AC8 | Contract | No provided operation in this story; the 401, 403 and 404 answers are proven under RWB-P5-E1057-CON |
| TC-P5-E1057-INF-10 | AC9 | Integration | Each consumed dependency made to fail or not answer; the failure reported and logged; the item kept in rwb-quarantine; no file in the matcher |

The legacy test cases this path serves are owned by the app story RWB-P5-E1057-APP and are not copied here: TC-E1-057-01 branch scan, TC-E1-057-02 partner SFTP, TC-E1-057-03 mailbox, TC-E1-057-04 mailroom scan, TC-E1-057-05 file type refused, TC-E1-057-06 size refused, TC-E1-057-07 unknown or suspended partner, TC-E1-057-08 duplicate, TC-E1-057-09 empty run, TC-E1-057-10 container refuses writes, TC-E1-057-11 two failed runs, TC-E1-057-12 one run across two instances, TC-E1-057-13 email with no usable attachment, TC-E1-057-14 file seen again after a failed move, TC-E1-057-15 outside business hours, TC-E1-057-16 scanned before OCR and TC-E1-057-17 rerun without the right. The contract-level copies of the same seventeen sit in RWB-P5-E1057-CON.

### 17. Guardrails

- No business value in a resource file: the type list, the size limit, the duplicate window, the alert threshold and the channel values stay parameters or reference rows, never a literal in the infrastructure.
- No personal data in a file name, a manifest, a log, a trace attribute or an alert: channel codes, counts, sizes, states and hashes only, and never a sender address, a partner's file name or a page text.
- No second copy of a picked-up file: the hold container is the only store until the scan, no topic and no message receives the file, and the claim-check link is one read at a time (BR6).
- No secret, no partner key and no mailbox credential in code, configuration, a values file or a script; the five secret classes are read with the workload identity (BR8, NFR-052).
- No public inbound rule and no open egress: every dependency is reached over a private endpoint resolved by private DNS, and the SFTP root is reachable only over the private MFT path (BR9).
- The mailbox reader grant is scoped to the declared mailboxes and is re-reviewed at every rotation; a wider grant blocks the release (BR5).
- A partner holds a read-only grant on its own subfolder only, never on the root and never on another partner's subfolder (BR4).
- No ACE grant and no ACE view for this service; only rwb-source-data reads the views (DP-01).
- No data-lake endpoint, route or landing container is provisioned, because the data lake is removed (DP-17).
- A file is never deleted while its item is open, and a processed folder is cleared by move to the archive tier and never by delete (BR6).
- An item is never matched unscanned: the scan is a condition of entering the matcher (BR11).
- No Schedule, no workflow and no activity is registered by this story; the queue and the channels are provisioned and the Schedule is the deployment story's (BR12).

### 18. Traceability

| Requirement ID | Requirement (short) | Infrastructure element | Test cases |
|---|---|---|---|
| REQ-DCM-009 | Documents arrive from branches, the mailroom, partner file transfer and email through the same intake | The four channels, their grants, their lifecycle and the one worker pool that reads them | TC-P5-E1057-INF-01 |
| REQ-DCM-010 | Every document carries a retention class, and intake runs a virus scan before the document is stored | The hold container, its rule, the clearing step and the scan capacity | TC-P5-E1057-INF-02, TC-P5-E1057-INF-06 |
| Arch v5 slide 11 | Blob with a claim-check link for one file, retry topics at 1 min, 10 min and 1 h then `.dlt`, MFT/SFTP with PGP for outside parties | The hold container, the topic binding and the SFTP path with its PGP key pair | TC-P5-E1057-INF-02, TC-P5-E1057-INF-03, TC-P5-E1057-INF-05 |
| Arch v5 slide 16 | rwb-document runs `DocumentIntakeWorkflow` on queue `rwb-document` and writes `rwb.document.events.v1` | The worker pool, the queue binding and the topic binding | TC-P5-E1057-INF-01, TC-P5-E1057-INF-03 |
| Arch v5 slide 35 | Zero trust: private access, workload identity, keys in the key store, partners only through the partner gateway in a separate DMZ | The identity layout, the secret classes, the private endpoints and the DMZ position of the two partner paths | TC-P5-E1057-INF-04, TC-P5-E1057-INF-05 |
| Arch v5 slide 38 | Wave 0 provides the template, the schemas and logins, the Kafka topics and ACLs and Temporal before the wave 1 services | The bindings this story verifies against the platform and the namespace it consumes | TC-P5-E1057-INF-01, TC-P5-E1057-INF-03 |
| Arch v5 slide 44 | JOB-12 Document intake runs every 15 minutes, owned by rwb-document | The pool, the KEDA rule and the cadence test | TC-P5-E1057-INF-01 |
| NFR-004 | The document store holds about 860,000 documents in 2027, rising with 15 percent inflow growth a year | The storage budget and the scan capacity | TC-P5-E1057-INF-02, TC-P5-E1057-INF-06, TC-P5-E1057-INF-07 |
| NFR-069 | The document hub holds about 5.8 million documents and 2.8 TB by the end of 2031, including every version and held document | The storage budget and the hold container capacity | TC-P5-E1057-INF-02 |
| NFR-052, NFR-053 | Secrets in the key store and never in code or configuration; data encrypted at rest and in transit | The five secret classes, the identity bindings, TLS and the secret scan | TC-P5-E1057-INF-04 |
| ADR-010, DP-01 | Only rwb-source-data reads ACE data | No ACE grant and no ACE route provisioned | TC-P5-E1057-INF-05 |
| ADR-023 | Observability per service | The hooks of section 11 and the queue-age alert | TC-P5-E1057-INF-01, TC-P5-E1057-INF-06 |

### 19. Out of scope

- The pickup activity, the channel readers, the intake service, the alert service and the run record (RWB-P5-E1057-APP).
- The contract documents, the shapes, the enumerations and the fakes (RWB-P5-E1057-CON).
- The chart, the values files, the Schedule registration, the flag values, the dashboards, the alerts and the runbook of the deployment (RWB-P5-E1057-OPS).
- The `rwb_document` schema, the login and the Flyway sequence (RWB-PLT-DB, RWB-PLT-E1044-CON); this story sizes the storage and creates no table.
- The standard Blob account, key store and MFT/SFTP resources (RWB-PLT-N012-INF) and the topic set with its retry and dead-letter topics (RWB-PLT-N002-INF); this story consumes and verifies them.
- The Temporal namespace, its certificates and the codec (RWB-PLT-N003-INF).
- The partner gateway itself, its FAPI 2.0 profile and its penetration test (the edge epic, RWB-PLT-EDGE); this story records its DMZ position as a boundary condition.
- The scanning product itself and its rule set (RWB-P5-E1041-APP); this story provisions the capacity around it.
- The branch scanners and the mailroom equipment, and the mailbox tenant configuration beyond the four declared mailboxes (branch operations, the mailroom and the mail team).
- The dashboards, the alert routing and the runbook set of the platform (RWB-PLT-N005-OPS, RWB-PLT-E1056-OPS); this story adds the entries its own resources need.
- The real cross-service journey of the path (RWB-ITG-E1057-ITG).
- The branch codes, the folder names, the mailbox codes, the replica counts, the request and limit sets, the storage budgets, the clearing age, the backlog threshold and the scan rate (GAP-1014).
