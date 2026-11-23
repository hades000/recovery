# RWB-PLT-N012-INF Blob, Key Vault and MFT/SFTP standard resources

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-N012-INF |
| Work type | INF (Infrastructure) |
| Suggested owner | SCB IT infrastructure (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-EVT |
| Wave | 0 |
| Business epic | NEW |
| Release | None (new story) |
| Legacy key | N012 |
| Legacy disposition | New |
| Build status | Not started |
| Patterns applied | None |
| Parallel lane | L-PLT-EVT-C |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: new platform story for RWB-PLT-EVT, legacy key N012. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **infrastructure engineer**, I want **the standard Blob, Key Vault and MFT/SFTP resources — the immutable document store, one AES-GCM codec key per Temporal namespace, and the PGP file-transfer endpoints — provisioned with private networking, scoped access and a rotation runbook**, so that **rwb-document, the Temporal workers and rwb-integration can store, encrypt and exchange data safely from Day 1 without each team inventing its own storage or secret layout**.

### 2. Business rationale

Documents reach 2.8 TB by 2031, and the legal document types must be write-once: once sealed, a document may not be changed or deleted by an application. Only rwb-document writes documents, so the write identity belongs to that service and to nothing else. Temporal payloads are encrypted by the payload codec (AES-GCM) with keys held in Key Vault per namespace, and a codec server lets authorised staff read those payloads in the Temporal UI, so the keys must exist before the first worker starts. A file message carries a claim-check SAS link for exactly one file for 15 minutes with a manifest, never the data itself. The WIN file (INT-14) and the debt-buyer files (INT-25) leave the bank over MFT/SFTP with PGP. Zero trust requires private endpoints and workload identity on every one of these resources. Three standard resources, built once in Wave 0, replace the alternative in which every service designs its own container layout, its own secret store entry and its own transfer endpoint.

### 3. Preconditions

- The platform subscription, the resource group and the network (virtual network, subnets, private DNS zones) are available.
- The workload identities of the services exist, so access is bound to an identity rather than to a shared credential.
- The Temporal namespace `rwb-recovery` is in place with its codec configuration (RWB-PLT-N003-INF).
- The rwb-document service identity is registered, and the rwb-integration endpoints are known to the network team.
- The platform naming library is in force, so resource names follow one rule rather than a local choice.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. List the three resource types, the consumers of each, and the settings the architecture fixes: immutable document store, codec key per Temporal namespace, PGP file-transfer endpoints.
2. Provision the Blob account and the containers, with encryption at rest and public access disabled, and apply the immutable policy to the containers that hold legal document types.
3. Create the Key Vault for the environment and one AES-GCM codec key per Temporal namespace, versioned, with the rotation metadata recorded.
4. Bind the codec server to the namespace and bind the access roles: the application read role, the operate role and the break-glass decode role, kept separate.
5. Create the MFT/SFTP endpoints for the WIN file (INT-14) and the debt-buyer files (INT-25), and exchange the PGP keys with the receiving parties.
6. Apply the private endpoints, the private DNS records and the network rules; confirm that no public endpoint answers on any of the three resource types.
7. Test the SAS scope (one file, 15 minutes, manifest with fileId, batchId, sha256 and record count) and the checksum path on receipt, including the failure path.
8. Publish the rotation runbook and the file-transfer runbook, and hand the resource references to rwb-document, the Temporal platform and rwb-integration.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A consumer presents a SAS link after its 15 minutes have elapsed | The request is refused with 403 and no partial read; the consumer asks rwb-document for a new link | MSG-PLT-N012-01 | AC2 |
| X2 | A consumer tries to read a second file through one link | The request is refused; one link answers one file only | MSG-PLT-N012-02 | AC2 |
| X3 | A write, overwrite or delete reaches a document under the immutable policy | The storage policy refuses the operation; no state changes | MSG-PLT-N012-03 | AC1 |
| X4 | A codec key is disabled, rotated out or unavailable | The codec fails closed: the worker stops and no clear-text payload is written to history or to a log; the key is restored or the version is re-bound under the runbook | None | AC3 |
| X5 | The sha256 or the manifest record count does not match on receipt | The file is rejected and not delivered; the failure path of rwb-integration raises FileFailed | MSG-PLT-N012-04 | AC5 |
| X6 | The PGP key of a receiver does not match the key used to encrypt the file | The transfer is refused and no clear file leaves the bank | MSG-PLT-N012-04 | AC5 |
| X7 | A connection arrives from outside the allow-list | The network rule refuses the connection before authentication | None | AC6 |

Message IDs MSG-PLT-N012-01 to MSG-PLT-N012-04 are the validation messages of section 14; the file-failure signal itself is the FileFailed event of rwb-integration and is not redefined here.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Provisions three infrastructure resource types; no application code and no dependency on a service build |
| Negotiable | Names, retention periods, rotation period and endpoint addresses are settled with the security and network teams; the resource types and their rules are fixed by the architecture |
| Valuable | Gives rwb-document, the Temporal workers and rwb-integration a safe standard to build on from Day 1 |
| Estimable | Three resource types, five configuration artefacts, two runbooks and four test areas |
| Small | Fits one sprint with the runbooks and the tests |
| Testable | Every criterion is tested against a provisioned resource, an access check or a transfer, never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Standard Blob, Key Vault and MFT/SFTP resources for Recovery

  Background:
    Given the platform subscription, the resource group and the private network are in place
    Given the three resource types are the immutable document store, the codec keys in Key Vault and the MFT/SFTP endpoints

  Scenario: AC1 The document store is immutable, private and written only by rwb-document (new, D-RCV-60)
    Given the Blob account and the document containers are provisioned
    Then the containers that hold legal document types carry the immutable policy
    Then public access on the account is disabled and the private endpoint is the only path to it
    Then encryption at rest is on and the key is held in the platform key store
    Then only the rwb-document workload identity holds a write grant, and no other service identity holds one
    Then the 2.8 TB by 2031 baseline is recorded against the account

  Scenario: AC2 A SAS link covers one file for 15 minutes and carries the manifest (new, D-RCV-60)
    Given rwb-document issues a claim-check link for one sealed file
    Then the link answers that one file and no other
    When the link is used after 15 minutes
    Then the request is refused with 403 and MSG-PLT-N012-01
    When a second file is requested through the same link
    Then the request is refused with MSG-PLT-N012-02
    Then the manifest carries fileId, batchId, sha256 and the record count
    Then no document content travels in the message that carries the link

  Scenario: AC3 One AES-GCM codec key per Temporal namespace (new, D-RCV-60)
    Given the Key Vault of the environment
    Then it holds one AES-GCM codec key per Temporal namespace, and the namespace rwb-recovery has its own key
    Then a Temporal client and a worker encrypt and decrypt a payload with that key
    When a worker runs without the key
    Then it cannot read the payload and the run fails closed
    Then previous key versions are kept and a payload sealed with an earlier version is still readable under the runbook

  Scenario: AC4 Key Vault access is scoped and audited (new, D-RCV-60)
    Given the access policies of the Key Vault
    Then an application reads a secret with its workload identity and with no shared credential
    Then the codec server decodes payloads only for the authorised decode role
    Then the operate role, the read role and the decode role are held by different role holders
    Then every secret read is written to the audit trail with the identity, the key and the time
    Then no secret appears in code, configuration, a test fixture or a log

  Scenario: AC5 The two file interfaces transfer over MFT/SFTP with PGP and a verified checksum (new, D-RCV-60)
    Given the MFT/SFTP endpoints of the platform
    Then the WIN outbound endpoint for INT-14 exists and the debt-buyer outbound endpoint for INT-25 exists
    Then every transfer is PGP protected with the key exchanged with the receiver
    Then the manifest and the sha256 are checked on receipt
    When the checksum or the PGP check fails
    Then the transfer fails with MSG-PLT-N012-04 and follows the FileFailed path of rwb-integration
    Then a re-delivery of the same file is safe because fileId is unique

  Scenario: AC6 The three resources are reachable only over private networking (new, D-RCV-60)
    Given the private endpoints and the network rules of the three resource types
    Then no public endpoint answers on the Blob account, the Key Vault or the SFTP service
    Then traffic in transit uses TLS
    Then the allow-list admits the AKS cluster and the named partner ranges and nothing else
    Then a configuration scan finds no public access setting on any of the three resources
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Documents are written only through rwb-document, and only one writer identity holds the write grant | Arch v5 slides 16 and 29 (Blob storage with WORM: documents, rwb-document only) |
| BR2 | A legal document type is write-once: the immutable policy is set at container level and is never relaxed by an application | Arch v5 slides 8 and 16 (Blob WORM) |
| BR3 | A file message is a claim-check: a SAS link for one file for 15 minutes plus a manifest with fileId, batchId, sha256 and the record count, never the data | Arch v5 slide 11 (File call type) |
| BR4 | Temporal payloads pass through the codec (AES-GCM) with keys in Key Vault per namespace, and the codec server serves the authorised decode role | Arch v5 slides 8, 24 and 35; ADR-016 |
| BR5 | No secret is written into code, configuration, a test fixture or a log; applications read secrets with their workload identity | Arch v5 slide 35 (zero trust, workload identity) |
| BR6 | A party outside the bank exchanges files over MFT/SFTP with PGP, and the checksum is verified on receipt | Arch v5 slide 11 (Transport: Blob + MFT/SFTP; PGP for outside parties) |
| BR7 | Every resource is reachable only through a private endpoint, and access is least privilege by workload identity | Arch v5 slides 11 and 35 (zero trust, private access) |
| BR8 | Retention classes stay reference data owned by rwb-document; this story provisions the policy mechanism and fixes no retention period | Template and Rules §R7.2 s17; Ownership Map v1 (retention is P5) |

### 9. State transitions

Resource lifecycle.

| From | Event | Condition | To |
|---|---|---|---|
| Requested | Provisioning approved | The naming library, the network and the identities are available | Provisioned |
| Provisioned | Access bound | The workload identity grants, the codec server binding and the transfer keys are in place | Access bound |
| Access bound | First consumer connected | rwb-document, the Temporal workers or rwb-integration uses the resource | In use |
| In use | Rotation started | The rotation runbook is opened and a new key version or credential is staged | Rotated |
| Rotated | Previous version retired | No payload or secret in use depends on the earlier version | In use |
| In use | Decommission approved | No consumer remains and the data is disposed of under the retention rule | Retired |

File row.

| From | Event | Condition | To |
|---|---|---|---|
| Created | Transfer started | The manifest and the sha256 are written by rwb-integration | Transferred |
| Transferred | Receipt confirmed | The receiver reports the file received | Checksum verified |
| Checksum verified | Delivery accepted | The manifest and the sha256 match on receipt | Delivered |
| Transferred | Checksum or PGP check failed | The sha256, the record count or the PGP key does not match | Failed |
| Failed | Operator retry | The cause is cleared and a new transfer is started | Transferred |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SCB IT infrastructure | Owns the story, the provisioning, the network rules and the two runbooks |
| Platform team | Owns the Blob account and containers and the Key Vault, including the key policy and the codec server binding |
| Security | Owns the access policy, the role separation and the break-glass decode right (RW-SECADM) |
| rwb-document owner | Decides which containers hold which document type and uses the store through its own identity |
| rwb-integration owner | Owns the two transfer endpoints and the file failure path that consumes them |
| Data steward | Confirms the retention classes that the immutable policy is applied for, as reference data |
| Audit (RW-AUDIT) | Reads the secret-access trail and the transfer trail; never decodes a payload |

The container names, the key names, the rotation period and the MFT/SFTP endpoint names are Not specified in the source documents (GAP-1399; ASM-2435).

### 11. Data

| Resource | Setting | Source |
|---|---|---|
| Blob account and container | One account for Recovery documents, containers per document class, encryption at rest on, public access disabled; 2.8 TB by 2031 as the capacity baseline | Arch v5 slide 16 (Azure Blob WORM: files, 2.8 TB by 2031); slide 29 (documents in Blob with WORM, rwb-document only) |
| Immutable policy | Write-once policy on the containers that hold legal document types, set at container level and not removable by an application | Arch v5 slides 8 and 16 (Blob WORM) |
| Key Vault | One vault per environment, one AES-GCM codec key per Temporal namespace, versioned, with the codec server bound to the namespace and the operate, read and decode roles separated | Arch v5 slides 8 and 24 (codec AES-GCM, Key Vault; codec server for the UI); slide 35 (keys in Key Vault, namespaces with their own keys) |
| Claim-check link | SAS link for one file, 15 minutes; manifest with fileId, batchId, sha256 and record count; a unique fileId so re-delivery is safe | Arch v5 slide 11 (File call type: identity, contract, duplicates) |
| MFT/SFTP endpoints | WIN outbound file (INT-14) and debt-buyer files per lot (INT-25), each PGP protected, with the manifest and the sha256 checked on receipt | Arch v5 slides 31 and 32 (WIN letters 16:00, INT-14; debt-buyer encrypted files, INT-25, over MFT or SFTP) |
| Private networking | Private endpoint, private DNS and network rules on all three resource types; TLS in transit; allow-list limited to the AKS cluster and the named partner ranges | Arch v5 slide 11 (transport) and slide 35 (zero trust, network edge to audit trail) |

The container names, the immutable retention period per container, the vault name, the key names, the rotation period, the endpoint names and the partner network ranges are Not specified in the source documents (GAP-1399; ASM-2435). They are deployment values of the resource files in section 13, and the story fixes only their shape.

### 12. Contract

#### 12.1 REST operations provided

None.

#### 12.2 REST operations consumed

None.

#### 12.3 Events published

None.

#### 12.4 Events consumed

None.

#### 12.5 Workflows and activities

None. The codec is a data converter on Temporal clients and workers; it is neither a workflow nor an activity, and this story registers no workflow, activity or task queue.

#### 12.6 Schedules

None.

#### 12.7 Tables owned

None. Blob and Key Vault are not ACE database tables, and no `rwb_*` table is owned by this story; the document metadata and its retention classes belong to the rwb-document DB stories.

#### 12.8 Contract fakes

None.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None | No operation is provided or consumed by the resources |
| Kafka | None | No topic is produced or consumed; rwb-document and rwb-integration publish their own events |
| Temporal | None | No workflow or activity; the codec keys serve the Temporal clients and workers of the namespace |
| File | 2 outbound interfaces | WIN (INT-14) and the debt-buyer files (INT-25) over MFT/SFTP with PGP; one file per SAS link for 15 minutes, with the manifest fileId, batchId, sha256 and record count |

### 13. Solution plan

**Deliverables.** `platform/storage/blob.yaml` (account, containers, immutable policy, private endpoint, role assignments), `platform/security/keyvault.yaml` (vault, one codec key per namespace, access policies, codec server binding), `platform/mft/endpoints.yaml` (the two MFT/SFTP endpoints, the PGP key references and the network rules), `runbooks/storage-rotation.md` (key and credential rotation, version retention, break-glass), `runbooks/file-transfer.md` (transfer, checksum, failure and re-delivery), and the tests for the SAS scope, the immutable policy, the PGP path and the network.

**Pattern application.** None of the §R5.5 DP markers appears in this new platform story: it replaces no legacy table, login, topic, path or scheduler, and it carries no dependency. DP-17 (no data lake) confirms the boundary that matters here: Blob holds documents only, so the account is provisioned for the document store and never as a reporting or lake landing zone; reporting reads events into rwb-reporting.

**Build steps**

1. Write the resource inventory: the three resource types, their consumers, the settings fixed by the architecture, and the values that stay open under the gap.
2. Provision the Blob account and the containers with encryption at rest and public access disabled, and apply the immutable policy to the legal document containers.
3. Assign the write grant to the rwb-document workload identity only, and confirm that no other identity holds write.
4. Create the Key Vault, one AES-GCM codec key per Temporal namespace, the codec server binding and the three separated roles.
5. Create the MFT/SFTP endpoints for INT-14 and INT-25, exchange the PGP keys with the receivers and record the checksum step.
6. Apply the private endpoints, the private DNS records and the allow-list, and run the public-access scan.
7. Test the SAS scope (one file, 15 minutes, manifest fields), the immutable policy, the checksum and PGP failure path, and the refused connection from outside the allow-list.
8. Publish the two runbooks and hand the resource references to rwb-document, the Temporal platform and rwb-integration.

**Done when.** The three resource types are provisioned in the environment, no public endpoint answers, the immutable policy refuses a write and a delete, one codec key per namespace encrypts and decrypts a payload while a worker without the key fails closed, the two transfer endpoints complete a PGP transfer with a verified sha256 and raise the failure path when the check fails, and both runbooks are reviewed by the security and on-call roles.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-PLT-N012-01 | A claim-check link is used after 15 minutes | This link has expired. Ask for a new link to the document. |
| MSG-PLT-N012-02 | A second file is requested through one link | This link covers one file only. |
| MSG-PLT-N012-03 | A write, overwrite or delete reaches an immutable document | This document is sealed and cannot be changed. |
| MSG-PLT-N012-04 | The checksum or the PGP check fails on receipt | The file could not be accepted: the integrity check failed. |

The four messages are the standard resource texts; the business messages of the owning services are unchanged, and a refused transfer is reported to the operator through the FileFailed path of rwb-integration with MSG-PLT-N012-04 as the detail.

### 15. Screens and states

None — the resources have no screen of their own. The storage and transfer status is read by the owning services: rwb-document shows a document and its custody state, and rwb-integration shows a file run and its delivery state. The dashboards over these signals are RWB-PLT-N005-OPS, not this story.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-N012-INF-01 | AC1 | Integration | A write by a second identity is refused; a write and a delete on an immutable container are refused with MSG-PLT-N012-03; public access is off; the 2.8 TB baseline is recorded |
| TC-PLT-N012-INF-02 | AC2 | Contract | One link answers one file; a second file and an expired link are refused with MSG-PLT-N012-02 and MSG-PLT-N012-01; the manifest carries fileId, batchId, sha256 and the record count; no content in the message |
| TC-PLT-N012-INF-03 | AC3 | Component | A client and a worker seal and open a payload with the namespace key; a worker without the key fails closed; a payload sealed with an earlier key version is still readable |
| TC-PLT-N012-INF-04 | AC4 | NFR | An identity reads only its permitted keys; the decode role is required to decode; every read appears in the audit trail; a secret scan finds no secret in code, configuration, a fixture or a log |
| TC-PLT-N012-INF-05 | AC5 | Integration | The INT-14 and INT-25 endpoints complete a PGP transfer with a matching sha256; a corrupted file and a mismatched PGP key raise MSG-PLT-N012-04 and the FileFailed path; a re-delivery of the same fileId is safe |
| TC-PLT-N012-INF-06 | AC6 | NFR | A connection to each resource from the public network is refused; a connection from the AKS cluster and from a named partner range succeeds; the scan reports no public access and TLS is enforced |

### 17. Guardrails

- No business value in a resource setting: the retention classes, the file windows and the document types stay data in the owning service, never a literal in a resource file.
- No personal data in a file name, a manifest, a log or a link: IDs, counts and hashes only.
- Documents are written only through rwb-document; no other service holds a write grant on the document containers (BR1).
- No secret in code, configuration, a test fixture or a log; every application reads its secret with its workload identity (BR5).
- The immutable policy is never relaxed without compliance approval, and a relaxation is recorded as a change with its reason.
- The private endpoints and the allow-list are mandatory on all three resource types; a public endpoint is a release blocker.
- Every transfer is PGP protected and every receipt is checked against the manifest and the sha256 (BR6).
- Only rwb-source-data reads the ACE views; the document store and Key Vault hold no ACE table copy (DP-05, DP-17).

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| Arch v5 slide 8 | Blob WORM for documents; Key Vault codec server with AES-GCM payload keys | `platform/storage/blob.yaml`, `platform/security/keyvault.yaml`, runbooks | TC-PLT-N012-INF-01, TC-PLT-N012-INF-03 |
| Arch v5 slide 11 | File call type: Blob + MFT/SFTP, PGP for outside parties, SAS link for one file for 15 minutes, manifest fileId, batchId, sha256, record count | SAS scope and manifest rule, `platform/mft/endpoints.yaml` | TC-PLT-N012-INF-02, TC-PLT-N012-INF-05 |
| Arch v5 slide 16 | Azure Blob (WORM) for files, 2.8 TB by 2031; rwb-document is the only writer | Blob account and immutable policy, capacity baseline | TC-PLT-N012-INF-01 |
| Arch v5 slide 24 | Codec AES-GCM with keys in Key Vault on every client and worker; codec server for the UI | Codec key per namespace, codec server binding, role separation | TC-PLT-N012-INF-03, TC-PLT-N012-INF-04 |
| Arch v5 slides 31–32 | WIN letters file at 16:00 (INT-14) and debt-buyer encrypted files (INT-25) over MFT or SFTP | The two transfer endpoints and the checksum step | TC-PLT-N012-INF-05 |
| ADR-016 | Reusable Temporal layer; each namespace carries its own certificates and codec keys | One codec key version set per namespace, version retention | TC-PLT-N012-INF-03 |
| Arch v5 slide 35 | Data layer: private access, one login per schema, encrypted payloads, keys in Key Vault | Private endpoints, allow-list, access audit | TC-PLT-N012-INF-04, TC-PLT-N012-INF-06 |

### 19. Out of scope

- The document metadata schema, the custody and retention classes and the retention job (the rwb-document DB and APP stories).
- The file builders and the manifest content (rwb-comms, rwb-debt sale and rwb-integration stories); this story provides the store, the keys and the endpoints they use.
- The Temporal cluster and the namespace itself (RWB-PLT-N003-INF); this story provisions the codec keys and the codec server binding for it.
- The dashboards and the alerts over storage and transfer (RWB-PLT-N005-OPS).
- The PGP key ceremony if the bank MFT team owns it; this story records the key reference and the check, not the ceremony.
- The naming, the immutable retention periods and the rotation period (GAP-1399).
