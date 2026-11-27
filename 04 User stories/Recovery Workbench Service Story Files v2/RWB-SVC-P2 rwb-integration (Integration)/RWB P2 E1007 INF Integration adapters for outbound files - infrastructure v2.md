# RWB-P2-E1007-INF Integration adapters for outbound files

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P2-E1007-INF |
| Work type | INF (Infrastructure) |
| Suggested owner | SCB IT infrastructure (suggested; any team may pick up this story) |
| Service | rwb-integration |
| Service epic | RWB-SVC-P2 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Contract version | v1 of RWB-P2-E1007-CON, on `/api/recovery/integration/v1` |
| Size | Not specified in the source documents (DOR-RWB-P2-E1007-INF-16); the squad sizes it at refinement |
| Patterns applied | DP01, DP02, DP03, DP05, DP07, DP09, DP10, DP11, DP16, DP17, DP19 |
| Parallel lane | L-P2-C |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Fakes until publish | DP-03, DP-07, DP-09, DP-10, DP-19: build against the fakes of the six contracts; add the rows to the plan when they publish (GAP-1161) |
| Contract dependencies | RWB-P2-E1007-CON; rwb-source-data read of the postal addressee by party_id, contract ID Not specified in the source documents (GAP-1162); document hub upload contract, ID Not specified in the source documents (GAP-1164) |
| Integration dependencies | None |
| External dependencies | None |
| Infrastructure values | Not specified in the source documents (GAP-0649); set per environment by the bank MFT team, the network team and security |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (FR-P2-001, FR-P2-002, FR-P2-003, FR-P2-004, FR-P2-005, FR-P2-006, FR-P2-007, FR-P2-008, FR-P2-009, FR-P2-010, FR-P2-011, FR-P2-012, FR-P2-013, FR-P2-014, FR-P2-015, FR-P2-016, FR-P2-017, FR-P2-018, FR-P2-020, FR-P2-021, FR-P2-022) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-007 for rwb-integration. The legacy story assumed the SFTP outbound folders existed in DEV and SIT with credentials in the key store, and it assumed one identity with SELECT on the ACE views. On the infrastructure side this story replaces both assumptions with provisioned resources: two MFT/SFTP egress endpoints with exchanged PGP keys, the key-store layout for the credentials and certificates, the firewall and DNS rules, the file staging area and the claim-check storage, the size and timeout budgets, the no-inbound-listener rule, the network zones and the observability hooks the transfer emits. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 31 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **infrastructure engineer**, I want **the outbound egress of rwb-integration provisioned as infrastructure — the WIN endpoint (INT-14) and the debt-buyer endpoint (INT-25) over MFT/SFTP with exchanged PGP keys, the credentials and certificates in the key store behind workload identity with a rotation runbook, the firewall and DNS rules that admit the named receivers only, the file staging area and the claim-check storage, the enforced file-size and transfer-timeout budgets, no inbound listener and no inbound folder, the network zones and the observability hooks of the transfer**, so that **the app and operations stories of this key can send a real file over a real endpoint from Day 1, with nothing listening inward and no secret or partner credential in code, configuration or a values file**.

The legacy story had one paragraph for this work: "the SFTP outbound folders exist in DEV and SIT, with credentials in the key store (NFR-052)" and "the recovery service identity holds its Entra ID managed identity in each environment and SELECT on `recovery.v_ace_*` only". Both statements are wrong under D-RCV-60 in a way that matters. The views are read only by rwb-source-data (ADR-010), so no grant and no network path to ACE is provisioned for this service here, and no grant on the rwb_debtsale schema (debt_sale_account) is provisioned either; and the outbound path leaves the cluster through an MFT/SFTP endpoint with a PGP key per receiver (Arch v5 slides 7, 8 and 11), not through a folder that happens to exist. This story provisions the endpoint, the key, the route, the staging area and the budgets, and it proves that nothing listens inward.

The story is also where the split is enforced at the network layer. No inbound listener, no inbound folder, no pickup rule and no sign-off exist, because the Workbench loads no source data (D-RCV-35 U1; BR9 of the app story); the `receiveFile` activity is published in the contract and called by no flow. And no data-lake route, endpoint or landing container is provisioned, because the data lake is removed (DP-17): the reporting extract leaves as a `deliverFile` call to rwb-reporting and the decision feed is Kafka inside the cluster.

### 2. Business rationale

Two files leave the bank on this path: the WIN registered-mail notice file daily at 16:00 (INT-14) and the debt-buyer data tape per awarded lot (INT-25), both over MFT/SFTP with PGP for a party outside the bank (Arch v5 slides 8, 11, 16 and 32). Neither can leave without a provisioned endpoint, an exchanged key, a routed network and a place to stage the file while the claim-check link is valid. Zero trust requires that every one of them is reachable only over a private path, by an identity, with the key in the key store and never in configuration (Arch v5 slide 35; NFR-052, NFR-053).

The prices of not doing this on Day 1 are concrete. An endpoint created ad hoc in SIT cannot be promoted, so the release date slips by a change request per environment. A credential copied into a values file becomes a security finding, and rotating it becomes a rebuild. A staging area that is shared with the document store breaks the claim-check rule, because a second service could read a file it is not entitled to. A missing size budget turns a malformed file into a transfer that hangs until the SFTP server closes it, and the retry ladder burns its three attempts on a cause that is not a transfer failure. Each of these is prevented by a provisioned value, not by code.

The two windows are the bank's, not this story's: the bank Airflow opens the WIN window at 16:00 and the debt-buyer window per lot, and rwb-integration still builds and sends the files (Arch v5 slides 16, 32 and 44). This story therefore provisions the transport and the route and registers no Schedule; the deployment, the alerts and the windows belong to RWB-P2-E1007-OPS.

### 3. Preconditions

- The platform subscription, the resource group and the network (virtual network, subnets, private DNS zones) of the environment are available.
- The AKS cluster of the ACE platform is reachable from the rwb-recovery namespace, with the workload identity of rwb-integration registered, so access is bound to an identity and not to a shared credential.
- The platform key store of the environment exists with its access policy (RWB-PLT-N012-INF provisions the standard Blob, key store and MFT/SFTP resources; this story consumes them for the two outbound interfaces).
- The rwb-document claim-check store exists and issues a SAS link for one file for 15 minutes with a manifest of fileId, batchId, sha256 and record count (Arch v5 slide 11).
- The bank MFT team has named the receiver-side contact and the key-exchange procedure for WIN and for the debt-buyer buyers, and the endpoint hosts and ports are known to the network team.
- The contract of this key is published (RWB-P2-E1007-CON): the manifest, the two events and the two activities fix what a transfer carries and what it reports.
- No build dependency and no contract dependency in the plan of this key; this story is Day 1 by rule (Template and Rules §R5.7). The two values it needs from the contract are read from RWB-P2-E1007-CON when it is published and do not block the provisioning.

### 4. Flow

1. List the two outbound interfaces and what each needs: the WIN endpoint (INT-14) and the debt-buyer endpoint (INT-25) per awarded lot, the PGP key of each receiver, the file pattern of each interface row and the staging location.
2. Provision the MFT/SFTP egress endpoints in each environment, one per receiver, with the account, the folder, the permissions and the transfer mode fixed by the interface row of `interface_config`.
3. Exchange the PGP keys with each receiver, record the key identifier and the fingerprint against the endpoint, and confirm the receiver's public key and the bank's key pair.
4. Put the credentials, the private keys and the certificates in the key store of the environment and bind each entry to the rwb-integration workload identity; write a rotation runbook for the credential, the certificate and the PGP key.
5. Apply the network rules: egress only to the named receiver ranges and ports, private DNS for the endpoint names, no public inbound rule on any of them, and TLS on the cluster side.
6. Provision the file staging area of the environment and confirm that the claim-check rule holds: one file per link, 15 minutes, manifest with fileId, batchId, sha256 and record count, and no file content in a queue.
7. Set the enforced budgets as environment values: the maximum file size, the transfer timeout, the connection and read timeouts, the concurrent transfer limit and the retry classification of a timeout as a transfer failure.
8. Confirm that nothing listens inward: no inbound listener, no inbound port, no inbound folder and no pickup or sign-off rule on either endpoint.
9. Wire the observability hooks: the endpoint health, the transfer attempt, the byte count, the checksum result, the failure class and the OpenTelemetry trace context, with no file name carrying personal data.
10. Hand the endpoint references, the key identifiers, the staging path and the budgets to the app and operations stories and run the four tests of section 16.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A receiver's PGP key does not match the key used to encrypt the file | The transfer is refused before any clear file leaves the bank and the attempt fails as a transfer failure | MSG-P2-E1007-INF-03 | AC2, AC5 |
| X2 | A credential or certificate has expired or is rotated out | The transfer fails closed, the endpoint health reports not ready and the rotation runbook restores the version; no clear-text fallback exists | MSG-P2-E1007-INF-02 | AC2 |
| X3 | A connection is attempted from outside the allow-list, or inward to the endpoint | The network rule refuses the connection before authentication; the refusal is logged and no listener answers | None | AC3, AC6 |
| X4 | The file exceeds the maximum size, or the transfer exceeds the timeout | The transfer is aborted and counted as a transfer failure, so it follows the retry ladder of the app story; the file is never truncated and never sent twice | MSG-P2-E1007-INF-03 | AC6 |
| X5 | The claim-check link has expired when the transfer starts | The request is refused with 403 and no partial read; the attempt fails and the next attempt asks rwb-document for a new link | MSG-P2-E1007-INF-04 | AC4 |
| X6 | The staging area holds a file whose sha256 does not match the manifest | The transfer is refused and the failure is reported with the checksum mismatch, never with a partial file | MSG-P2-E1007-INF-03 | AC4 |
| X7 | A second interface is configured against the same endpoint with a different key or folder | The configuration check fails the change, because one endpoint answers one receiver and one key | None | AC1 |
| X8 | A values file, a script or a runbook carries a secret | The secret scan fails the change and the value is moved to the key store | None | AC2 |

Message identifiers MSG-P2-E1007-INF-01 to MSG-P2-E1007-INF-04 are the infrastructure validation messages of section 14; the business messages of the app story are unchanged and the file failure signal itself is `FileFailed` on `rwb.integration.events.v1`.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Provisions two endpoints, the keys, the routes, the staging area and the budgets; no application code and no dependency on a service build |
| Negotiable | Endpoint hosts, ports, folders, key identifiers, firewall ranges, staging names, the size limit and the timeouts are environment values settled with the MFT and network teams; the resource types and their rules are fixed by the architecture |
| Valuable | Gives the app and operations stories a real endpoint, a real key and a real route on Day 1, with nothing listening inward and no secret in configuration |
| Estimable | Two endpoints, one key-store layout, one network rule set, one staging area, one budget set, one rotation runbook and four test areas |
| Small | Fits one sprint with the runbook and the tests |
| Testable | Every criterion is tested against a provisioned resource, a refused connection, a refused transfer or a scan, never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Outbound egress for rwb-integration

  Background:
    Given the platform subscription, the resource group and the private network of the environment are in place
    Given the two outbound interfaces are INT-14 WIN registered mail and INT-25 debt buyer tape
    Given the target environment is SIT

  Scenario: AC1 The two egress endpoints exist and nothing listens inward (new, D-RCV-60)
    Given the MFT/SFTP resources of the environment
    When the two egress endpoints are checked in the environment
    Then the WIN endpoint for INT-14 exists with its account, folder and transfer mode
    Then the debt-buyer endpoint for INT-25 exists and serves one awarded lot per transfer
    Then each endpoint is bound to exactly one receiver and one key
    Then no inbound listener, inbound port, inbound folder or pickup rule exists on either endpoint
    Then the service holds no grant on the recovery schema and no network route to an ACE view
    Then no data-lake target and no lake landing container is provisioned

  Scenario: AC2 The keys and the credentials live in the key store and rotate under a runbook (new, D-RCV-60)
    Given the key store of the environment
    Then the credentials, the private keys and the certificates of both endpoints are held there and bound to the rwb-integration workload identity
    Then each PGP key is recorded with its identifier and fingerprint and matches the receiver's key
    Then a secret scan of the configuration, the scripts and the values finds no secret
    When a credential or a certificate reaches its rotation point
    Then the rotation runbook stages the new version, switches the endpoint and retires the previous version
    Then a transfer with an expired credential fails closed and no clear-text fallback is used

  Scenario: AC3 The route to each receiver is private and allow-listed (new, D-RCV-60)
    Given the network rules of the environment
    Then egress is admitted to the named receiver ranges and ports only
    Then the endpoint names resolve through private DNS
    Then traffic in transit uses TLS on the cluster side
    Then no public inbound rule exists on either endpoint
    When a connection arrives from outside the allow-list
    Then it is refused before authentication and logged

  Scenario: AC4 The staging area and the claim-check storage hold one file per link (new, D-RCV-60)
    Given the file staging area of the environment
    Then a built file is staged with its manifest of fileId, batchId, sha256 and record count
    Then the claim-check link answers one file for 15 minutes and no other
    When the link is used after 15 minutes
    Then the request is refused with 403 and MSG-P2-E1007-INF-04
    Then a staged file whose sha256 does not match the manifest is refused with MSG-P2-E1007-INF-03
    Then no file content is placed on a queue, a topic or a workflow input

  Scenario: AC5 The transfer emits its observability hooks with the trace context (new, D-RCV-60)
    Given the observability configuration of the environment
    When one file is transferred and one transfer fails
    Then the endpoint health, the transfer attempt, the byte count, the checksum result and the failure class are emitted
    Then each signal carries the environment, the interface ID and the OpenTelemetry trace context
    Then no signal carries a file content, an address or an identity number
    Then the failed transfer is visible before the app story raises FileFailed

  Scenario: AC6 The size and timeout budgets are enforced as environment values (new, D-RCV-60)
    Given the budget set of the environment
    When a file or a transfer is checked against the budget set
    Then the maximum file size, the transfer timeout, the connection and read timeouts and the concurrent transfer limit are set as values and not in code
    Then a file above the maximum size is refused and counted as a transfer failure
    Then a transfer that exceeds the timeout is aborted and counted as a transfer failure
    Then the exact values are not in the source documents and are carried as GAP-0649 until the MFT team sets them
    Then the retry ladder of the interface row is the only retry and the infrastructure adds none

  Scenario: AC7 The transport registers no schedule, holds no business value and builds no file (new, D-RCV-60)
    Given the job and schedule registry of the environment
    When the transport provisioning is checked in the environment
    Then no Schedule is registered for either endpoint
    Then no business value is held in the transport configuration
    Then no file is built by the transport
```

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The two outbound interfaces leave the bank over MFT/SFTP with PGP: INT-14 WIN registered mail daily at 16:00 and INT-25 debt buyers per awarded lot | Arch v5 slides 8, 11, 16 and 32 | AC1; TC-P2-E1007-INF-01 |
| BR2 | One endpoint answers one receiver and one key; the credentials, private keys and certificates live in the key store and are never in code, configuration, a values file or a runbook | NFR-052; Arch v5 slide 35; legacy RWB-E1-007 precondition | AC1, AC2; TC-P2-E1007-INF-01, TC-P2-E1007-INF-02 |
| BR3 | Nothing listens inward: no inbound listener, no inbound port, no inbound folder and no pickup or sign-off rule, because rwb-integration has no inbound adapter | D-RCV-35 U1; ADR-010; FSD P2 v3 A1.6; app story BR9 | AC1, AC3; TC-P2-E1007-INF-01, TC-P2-E1007-INF-03 |
| BR4 | Every endpoint is reachable only over a private route, with private DNS and an allow-list limited to the named receivers | Arch v5 slide 35; zero trust | AC3; TC-P2-E1007-INF-03 |
| BR5 | A file is staged with its manifest and its sha256, the claim-check link answers one file for 15 minutes, and no file content travels on a message | Arch v5 slide 11 | AC4; TC-P2-E1007-INF-04 |
| BR6 | The file-size limit, the transfer timeout and the concurrency limit are environment values, enforced by the transport, and a violation is a transfer failure that follows the interface retry ladder | Arch v5 slide 11; ASM-1083 | AC6; TC-P2-E1007-INF-06 |
| BR7 | No ACE grant and no ACE network path is provisioned for this service: only rwb-source-data reads the thirty `recovery.v_ace_*` views | Arch v5 slides 8, 9 and 29; ADR-010; DP-05 | AC1; TC-P2-E1007-INF-01 |
| BR8 | No data-lake endpoint, route or landing container is provisioned, because the data lake is removed: INT-19, INT-20, JOB-13 and JOB-15 are removed with no target in this service, and no lake file, lake copy or lake delivery row is created | DP-17; Arch v5 slides 2, 37 and 44; GAP-1163 | AC1; TC-P2-E1007-INF-01 |
| BR9 | The observability of the transfer carries counts, identifiers, the interface, the environment and the trace context only, never a file content, an address or an identity number | ADR-023; CTL-11 | AC5; TC-P2-E1007-INF-05 |
| BR10 | This story provisions transport and route only: it registers no Schedule, holds no business value and builds no file | Arch v5 slides 16, 32 and 44; Template and Rules §R7.2 s17 | AC7; TC-P2-E1007-INF-07 |

### 9. State transitions

Endpoint lifecycle.

| From | Event | Condition | To |
|---|---|---|---|
| Requested | Provisioning approved | The receiver, the folder, the key and the route are known | Provisioned |
| Provisioned | Key exchanged and access bound | The PGP key matches the receiver and the workload identity is bound | In use |
| In use | Rotation started | The credential, the certificate or the key reaches its rotation point | Rotating |
| Rotating | Previous version retired | No staged file and no running workflow depends on the earlier version | In use |
| In use | Endpoint suspended | The receiver asks for a stop or a security event is open | Suspended |
| Suspended | Endpoint resumed | The cause is cleared and the route is re-checked | In use |
| In use | Decommission approved | The interface is retired and no staged file remains | Retired |

File row.

| From | Event | Condition | To |
|---|---|---|---|
| Staged | Manifest written | fileId, batchId, sha256 and record count are recorded by the app story | Ready to transfer |
| Ready to transfer | Transfer started | The claim-check link is valid and the endpoint is in use | Transferring |
| Transferring | Transfer completed | The bytes arrive and the receiver confirms | Delivered to receiver |
| Transferring | Size, timeout, checksum or key check failed | Any budget or key check fails | Failed |
| Failed | Operator retry | The cause is cleared and the next attempt starts from the retry ladder | Transferring |
| Delivered to receiver | Link expired | The 15 minutes elapse | Cleared |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SCB IT infrastructure | Owns the story, the two endpoints, the network rules, the staging area and the two runbooks |
| Bank MFT team | Owns the MFT service, the receiver agreements, the key ceremony and the transfer logs; this story records the key identifier and the fingerprint |
| Platform team | Owns the key store, the workload identity binding and the private DNS zone |
| Security | Owns the access policy, the rotation requirement and the secret scan; approves a relaxation of the allow-list |
| rwb-integration owner | Consumes the endpoint references, the key identifiers and the budgets; owns the file build and the retry ladder |
| rwb-document owner | Issues the claim-check link and owns the claim-check store |
| Data steward | Confirms that no file name, manifest or log line carries personal data |
| Audit (RW-AUDIT) | Reads the transfer trail and the key-rotation trail |

The endpoint names, the accounts, the folders, the key identifiers, the receiver ranges, the staging names, the file-size limit, the timeouts and the rotation period are Not specified in the source documents (GAP-0649; ASM-1083, ASM-1084).

### 11. Data

| Resource | Setting | Source | BR Field ID |
|---|---|---|---|
| WIN endpoint (INT-14) | One MFT/SFTP endpoint, one account, one folder, one PGP key, the file pattern of its `interface_config` row, daily at 16:00 | Arch v5 slides 8, 11, 16 and 32; legacy RWB-E1-007 precondition | Not specified in the source documents (DOR-RWB-P2-E1007-INF-7) |
| Debt-buyer endpoint (INT-25) | One MFT/SFTP endpoint per buyer or one with a folder per buyer, one PGP key, one transfer per awarded lot | Arch v5 slides 8, 11, 16 and 32; FSD P2 v3 A1.5 | Not specified in the source documents (DOR-RWB-P2-E1007-INF-7) |
| Keys and certificates | The credentials, the private PGP keys and the certificates in the key store, bound to the rwb-integration workload identity, with the fingerprint recorded | NFR-052; Arch v5 slide 35 | Not specified in the source documents (DOR-RWB-P2-E1007-INF-7) |
| Claim-check storage | A SAS link for one file for 15 minutes with a manifest of fileId, batchId, sha256 and record count; a unique fileId so re-delivery is safe | Arch v5 slide 11 | Not specified in the source documents (DOR-RWB-P2-E1007-INF-7) |
| Staging area | One staging location per environment for the built file, written by the transport, readable only by the rwb-integration workload identity, cleared after the link expires | Arch v5 slide 11; DP-01 | Not specified in the source documents (DOR-RWB-P2-E1007-INF-7) |
| Network | Private DNS for both endpoints, egress allow-list limited to the receiver ranges and ports, TLS on the cluster side, no public inbound rule | Arch v5 slide 35 | Not specified in the source documents (DOR-RWB-P2-E1007-INF-7) |
| Budgets | Maximum file size, transfer timeout, connection and read timeouts, concurrent transfer limit, all as environment values; a violation is a transfer failure | Arch v5 slide 11; GAP-0649 | Not specified in the source documents (DOR-RWB-P2-E1007-INF-7) |
| Observability hooks | Endpoint health, transfer attempt, byte count, checksum result, failure class and the OpenTelemetry trace context; no file content and no personal data | ADR-023 | Not specified in the source documents (DOR-RWB-P2-E1007-INF-7) |
| Absent by design | No inbound listener, no inbound folder, no pickup rule, no sign-off, no ACE grant, no ACE network route, no data-lake endpoint | D-RCV-35 U1; ADR-010; DP-17 | Not specified in the source documents (DOR-RWB-P2-E1007-INF-7) |

The names, numbers and addresses of the table above are environment values of the resource files in section 13; they are Not specified in the source documents (GAP-0649; ASM-1083) and this story fixes only their shape and the rule that no value is written in code.

### 12. Contract

#### 12.1 REST operations provided

None.

#### 12.2 REST operations consumed

None. The infrastructure calls no service operation; the app story's transport calls rwb-document and rwb-source-data at run time and the endpoint references of this story are injected into the chart by RWB-P2-E1007-OPS.

#### 12.3 Events published

None. `rwb.integration.FileDelivered.v1` and `rwb.integration.FileFailed.v1` are published by the app story on `rwb.integration.events.v1`; this story emits no event and holds no outbox.

#### 12.4 Events consumed

None. The only subscription of the service is `rwb.source-data.AceDataReady.v1` and it belongs to the app story.

#### 12.5 Workflows and activities

None. No workflow, no activity and no task queue is registered by this story; `deliverFile(manifest)` and `receiveFile` are the app story's and run on queue `rwb-integration`.

#### 12.6 Schedules

None. The WIN window at 16:00 and the debt-buyer window per lot belong to the bank Airflow and the container of the release to RWB-P2-E1007-OPS; this story registers no Schedule and no timer.

#### 12.7 Tables owned

None. `interface_config`, `outbound_item` and `job_catalog` are the app story's tables in `rwb_integration` and this story creates no table, no column and no grant; it provisions no ACE view, because only rwb-source-data reads them (DP-05).

#### 12.8 Contract fakes

None. The endpoint test uses a receiver stub on the MFT/SFTP side, which is a test double of the infrastructure and not a contract fake; the contract fakes of the consumed services are RWB-P2-E1007-CON's.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None | No operation is provided or consumed by the infrastructure |
| Kafka | None | No topic is produced or consumed; the two events belong to the app story |
| Temporal | None | No workflow and no activity; the codec and the mTLS material come from the platform |
| File | 2 outbound interfaces | INT-14 WIN registered mail and INT-25 debt buyer tape over MFT/SFTP with PGP; one file per 15-minute SAS link with its manifest; no inbound interface and no data lake |

### 13. Solution plan

**Deliverables.** `infra/mft/endpoints.yaml` (the two endpoints, their accounts, their folders, the file patterns and the transfer mode), `infra/security/keys.yaml` (the key-store entries, the workload identity bindings, the PGP key identifiers and fingerprints), `infra/network/rules.yaml` (the private DNS records, the egress allow-list, the TLS settings and the absence of a public inbound rule), `infra/storage/staging.yaml` (the staging area, its access rule and its clearing rule), `infra/mft/budgets.yaml` (the size and timeout set of BR6), `runbooks/key-rotation.md` (credential, certificate and PGP rotation, version retention, break-glass) and `runbooks/file-transfer.md` (staging, manifest, checksum, failure and re-delivery).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | The staging area and the key store hold no table copy and no ACE row; the schema `rwb_integration` is not touched | none |
| DP-02 | `recovery_svc` login | One login and one workload identity per service; the credential of rwb-integration is its own and lives in the key store | none |
| DP-03 | DecisionLogWriter, decision log | No decision record is written by the infrastructure; the library of the app story publishes it | H RWB-PLT-E1027-CON (of the app story) |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | No ACE grant and no route to an ACE view is provisioned for this service | none |
| DP-07 | Reference data, LOV | The file patterns and the folders come from the `interface_config` rows and never from a resource file | H RWB-PLT-E1043-CON (of the app story) |
| DP-09 | Application event, EV-nn, outbox | No topic, no outbox and no inbox is provisioned here; the platform chart does it | H RWB-PLT-TE006-CON (of the app story) |
| DP-10 | Quartz, JOB-nn | No Schedule and no worker is provisioned here; the two windows are the bank's | H RWB-PLT-E1071-CON (of the app story) |
| DP-11 | In-process call, published interface | No REST call is made by the infrastructure; the 2 s budget is a value of the app story's client | none |
| DP-16 | `recovery.integration.adapter` | The endpoint serves the rwb-integration contract; it declares no path and no operation of its own | C RWB-P2-E1007-CON |
| DP-17 | Data lake, INT-19, INT-20 | No lake endpoint, route or landing container is provisioned | none |
| DP-19 | Screen, ace-web | No screen and no route is provisioned for the infrastructure; SCR-09 is the edge's | H RWB-PLT-N001-CON (of the app story) |

The H dependencies of the table are the app story's and are not carried by this story, whose plan holds no build dependency; they are listed to show where each pattern resolves.

**Build steps**

1. Write the endpoint inventory: the two interfaces, their receiver, their account, their folder, their file pattern and their transfer mode.
2. Provision the two endpoints in each environment and bind each to one receiver and one key.
3. Exchange the PGP keys, record the identifier and the fingerprint, and confirm the receiver's key.
4. Place the credentials, the private keys and the certificates in the key store and bind them to the rwb-integration workload identity.
5. Apply the private DNS records, the egress allow-list and the TLS settings of the environment, and run the public-access scan that proves no inbound rule answers on either endpoint.
6. Provision the staging area and the claim-check storage rule with the 15-minute single-file link, its access rule and its clearing rule.
7. Set the size and timeout budgets as environment values and classify a violation as a transfer failure.
8. Wire the observability hooks and the endpoint health signal with the trace context and no personal data.
9. Publish the two runbooks and hand the endpoint references, the key identifiers, the staging path and the budgets to the app and operations stories.

**Configuration.** The endpoint host, port, account, folder, key identifier, receiver range, staging name, maximum file size, transfer timeout, connection and read timeouts and concurrency limit are values of the environment files. None of them is in code, and none is in a values file that is committed with a secret (NFR-052).

**Done when.** Both endpoints are provisioned in the environment, no public inbound rule answers on either, a PGP transfer completes with a verified sha256, a mismatched key and an oversized file are refused with the documented message, the staging area clears after the link expires, a secret scan finds nothing, and both runbooks are reviewed by the security and on-call roles.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-E1007-INF-01 | An endpoint is requested with no receiver, no key or a second receiver on one endpoint | This endpoint needs one receiver and one key. |
| MSG-P2-E1007-INF-02 | A credential, a certificate or a PGP key has expired or is rotated out | The endpoint credential has expired. Follow the rotation runbook. |
| MSG-P2-E1007-INF-03 | The size, timeout, checksum or PGP check fails | The file could not be transferred: the integrity check failed. |
| MSG-P2-E1007-INF-04 | The claim-check link has expired | This link has expired. Ask for a new link to the document. |

The four messages are the infrastructure texts of this story and are new; no legacy business message is renumbered or reworded by them. A refused transfer is reported to the operator through the transfer hooks of AC5 and, at run time, through `FileFailed` of the app story.

### 15. Screens and states

None — the infrastructure has no screen of its own. SCR-09 states: loading, per Screen Specifications v1; empty, error and no access: Not specified in the source documents (CG-ALL-2988). The transfer status is read by the app story's SCR-09 Exception queue and by the dashboards of RWB-P2-E1007-OPS; the endpoint health signal of AC5 is what the operations story alerts on.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P2-E1007-INF-01 | AC1 | Integration | Both endpoints provisioned in SIT; a second receiver on one endpoint refused; no inbound listener, no inbound folder and no ACE route found |
| TC-P2-E1007-INF-02 | AC2 | NFR | Keys and certificates in the key store with a workload identity binding; a secret scan clean; a rotation cycled; an expired credential fails closed |
| TC-P2-E1007-INF-03 | AC3 | NFR | Egress admitted to the named ranges only; a connection from outside refused and logged; private DNS resolves; no public inbound rule |
| TC-P2-E1007-INF-04 | AC4 | Contract | A staged file with its manifest; one file per 15-minute link; an expired link refused with MSG-P2-E1007-INF-04; a checksum mismatch refused with MSG-P2-E1007-INF-03 |
| TC-P2-E1007-INF-05 | AC5 | Integration | One successful and one failed transfer; every hook emitted with the environment, the interface and the trace context; no personal data in any signal |
| TC-P2-E1007-INF-06 | AC6 | NFR | A file above the maximum size and a transfer past the timeout are refused as transfer failures; no infrastructure retry is added |
| TC-P2-E1007-INF-07 | AC7 | Integration | The job and schedule registry, the transport configuration and the staging area of SIT; no Schedule, no business value and no file built by the transport |
| TC-E1-007-05 | Retired inbound load (legacy section 16; no AC) | NFR | Asserts absence of the inbound FileLoadAdapter, the inbound folder listing, DQ-057, DQ-059 and interface_run; a file missing at the cut-off is ACE ingestion under RWB-ACE-001 and the EV-27 AceDataLate alert |
| TC-E1-007-06 | Retired inbound load (legacy section 16; no AC) | NFR | Asserts absence of the inbound file checks; the same file delivered twice is ACE ingestion under RWB-ACE-001 |

### 17. Guardrails

- No business value in a resource file: the file patterns, the folders, the attempt limits and the retry intervals stay `interface_config` rows, never a literal in the infrastructure.
- No personal data in a file name, a manifest, a log, a trace attribute or an alert: identifiers, counts and hashes only.
- No secret in code, configuration, a values file, a script or a runbook; every credential is read with the workload identity (NFR-052, BR2).
- Nothing listens inward: no inbound listener, no inbound port, no inbound folder and no pickup rule on either endpoint (BR3).
- No ACE grant and no ACE network path for this service; only rwb-source-data reads the views (BR7).
- No data-lake endpoint, route or landing container (BR8).
- The private route and the allow-list are mandatory on both endpoints; a public inbound rule is a release blocker.
- Every transfer is PGP protected and every receipt is checked against the manifest and the sha256 (BR5).

### 18. Traceability

| Requirement ID | Requirement (short) | Infrastructure element | Test cases |
|---|---|---|---|
| Arch v5 slide 8 | Recovery has no connection to the data lake; WIN and debt-buyer files leave rwb-integration over MFT/SFTP | The two endpoints and the absence of a lake route | TC-P2-E1007-INF-01, TC-P2-E1007-INF-03 |
| Arch v5 slide 11 | File call type: Blob plus MFT/SFTP, PGP for outside parties, SAS link for one file for 15 minutes, manifest of fileId, batchId, sha256 and record count | Claim-check storage, staging area and the manifest rule | TC-P2-E1007-INF-04 |
| Arch v5 slide 16 | rwb-integration sends the WIN file (INT-14) and the debt-buyer files per lot (INT-25) | The two endpoints and their file patterns | TC-P2-E1007-INF-01 |
| Arch v5 slides 32 and 44 | The bank Airflow owns the 16:00 WIN window and the per-lot buyer window; rwb-integration builds and sends the files | No Schedule and no timer is provisioned; the route is ready before the window | TC-P2-E1007-INF-01 |
| Arch v5 slide 35 | Zero trust: private access, workload identity, keys in the key store | Key-store layout, private DNS, allow-list and the secret rule | TC-P2-E1007-INF-02, TC-P2-E1007-INF-03 |
| NFR-052, NFR-053 | Secrets in the key store and never in code or configuration; data encrypted at rest and in transit | Key-store entries, workload identity bindings, TLS and the secret scan | TC-P2-E1007-INF-02 |
| ADR-010, DP-05 | Only rwb-source-data reads ACE data | No ACE grant and no ACE route provisioned | TC-P2-E1007-INF-01 |
| ADR-023 | Observability per service | The transfer hooks and the endpoint health signal | TC-P2-E1007-INF-05 |

### 19. Out of scope

- The file build, the transport code, the retry policy, the events and the admin operations (RWB-P2-E1007-APP).
- The contract documents, the manifest schema and the fakes (RWB-P2-E1007-CON).
- The Helm chart, the values files, the topic and queue provisioning, the alerts, the dashboards and the runbook of the deployment (RWB-P2-E1007-OPS).
- The standard platform resources themselves — the Blob account, the key store and the shared MFT service (RWB-PLT-N012-INF); this story consumes them for the two interfaces.
- The claim-check store of rwb-document, its custody, its WORM policy and its retention (P5 stories).
- The bank Airflow DAGs of the two windows (bank platform team, for discussion), and the PGP key ceremony if the bank MFT team owns it.
- The real cross-service journey of the path (RWB-ITG-E1007-ITG).
- The endpoint names, the receiver ranges, the key identifiers, the size limit, the timeouts and the rotation period (GAP-0649).
