# RWB-PLT-N003-INF Temporal namespace rwb-recovery and codec key

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-N003-INF |
| Work type | INF (Infrastructure) |
| Suggested owner | SCB IT infrastructure (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-WF |
| Wave | 0 |
| Business epic | NEW |
| Release | None (new story) |
| Legacy key | N003 |
| Legacy disposition | New |
| Build status | Not started |
| Patterns applied | None |
| Parallel lane | L-PLT-WF-A |
| Ready to start | Day 1 |
| Size | Squad sizes at refinement (DOR-RWB-PLT-N003-INF-16) |
| Depends on (build) | None |
| Contract dependencies | None: this story publishes and consumes no API contract, so no contract story, fake library version or contract version applies (DOR-RWB-PLT-N003-INF-21, -22, -23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: new platform story for RWB-PLT-WF, legacy key N003. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (8 resolved, 6 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform administrator (RW-PLATADM)**, I want **the Temporal namespace `rwb-recovery` and its codec key — the namespace registered on the shared cluster with its own retention, rate limits, certificates and encryption key, the AES-GCM payload key held in Azure Key Vault with a version policy and unwrap rights for the platform identity SY-CASEWF, the namespace entitlements and the four search attributes fixed, and the evidence pack that proves all of it**, so that **the 19 services' workers and the workflow kit run inside one isolated, encrypted tenant from Day 1, no history holds clear personal data, and no team opens a namespace or copies a key of its own**.

This is L2 of the five-layer Temporal design (Architecture v5 slides 23 and 24; Temporal and Drools Design slides 11 and 12). L1 is the cluster, one per environment on the ACE AKS clusters, with its own persistence database. L2 is the namespace: `rwb-recovery` and, when another workbench arrives, its own namespace beside it, each with its own retention, rate limits, certificates and encryption keys, because a new workbench takes a namespace on the same cluster and not a second cluster (Architecture v5 slides 23 and 46). This story provisions and operates the L2 record of the Recovery workbench and the key that protects its payloads.

The namespace is shared platform, not one of the 19 services. Template and Rules §R4 has no platform row, so this story creates no schema of the form `rwb_<name>`, publishes no `rwb.<short>.events.v1` topic, owns no `/api/recovery/<short>/v1` base and invents no service short; Architecture v5 slides 4 and 41 keep the shared platform pieces outside the service catalogue. The platform task queue is task queue `rwb-platform`, which the Ownership Map gives to JOB-22 and which RWB-PLT-E1071 owns.

The boundary with the sibling stories is explicit, because four other stories touch the same object and none of them owns the namespace record:

- **RWB-PLT-E1070-APP and RWB-PLT-E1070-CON** own the cluster, its two persistence databases, the frontend on port 7233, the Web UI behind Entra ID, the mTLS front door, the certificate profile, the namespace bootstrap job that applies a namespace record, and the codec server runtime. This story owns the content of that record and its evidence, and the two must ship the same retention and the same four search attributes.
- **RWB-PLT-NF08-INF** owns the baseline standard for the shared Temporal layer as one versioned record. This story conforms to that baseline and does not restate it.
- **RWB-PLT-E1071** owns the worker, the SDK wiring and the codec inside each worker; **RWB-PLT-E2038** owns the codec server, decode and the admin audit; **RWB-PLT-E2039** owns the backup, the failover, the upgrade and the archive of closed histories to Blob; **RWB-PLT-E2037** owns the dashboard, the alerts and the run book catalog; **RWB-PLT-N010** owns the workflow kit.
- This story owns the namespace record, its key versions, its entitlements, its search-attribute set, its quota record and the namespace-level evidence pack, and nothing else.

Four values the namespace needs are named by no read source: the platform's own login and admin base, the per-namespace quotas and rate limits, the namespace's certificate set beyond the frontend certificate, and the key rotation period and the exact retention the namespace must carry beyond the 30 days of the closed-workflow rule. They are carried as the working read of one assumption and remain placeholders where they are still open: Not specified in the source documents (GAP-1451; ASM-2546).

### 2. Business rationale

Isolation is the whole reason a namespace exists on a shared cluster. One cluster per environment is affordable; one cluster per workbench would be four environments multiplied by every workbench, so the platform isolates tenants with namespaces and task queues instead (Architecture v5 slides 23, 24 and 45). A namespace is therefore the unit that carries its own retention, its own rate limits, its own certificates and its own encryption keys, and a tenant that shares any of those with another tenant is not isolated at all.

The encryption key is the object whose misuse breaks the privacy rule of the platform. Personal data stays in the owning service; events and workflow histories carry identifiers; the payload codec encrypts every payload with AES-GCM and the keys live in Key Vault per namespace (Architecture v5 slides 8, 24 and 35; Temporal and Drools Design slides 11, 23 and 27). A key that is copied into a values file, shared between two namespaces or granted to every workload makes that rule a statement rather than a control, and a key without a version policy cannot be rotated when a member of staff leaves or when a security finding lands. The unwrap right is therefore the narrowest grant in the platform: the platform identity alone, on this namespace's key, with the operation recorded.

The namespace record is also the answer an auditor and an incident responder ask for. What is the retention, what are the quotas, which identities may operate or read this namespace, which fields are indexed, and is there any payload in a history that a scan could read? Each of those questions is answered by one evidence pack in this story, produced from the live namespace and from Key Vault and not from a document that drifts. That is why the story is Wave 0 and Day 1: nineteen worker deployments connect to the namespace and the codec in waves 1 to 4, and a namespace created by the first team that needs it, with a key copied from a sample, is far more expensive to correct afterwards than to fix now.

### 3. Preconditions

- The cluster of RWB-PLT-E1070-APP exists in DEV and SIT: the frontend on port 7233 behind mTLS, the Web UI behind Entra ID, and the two persistence databases `temporal` and `temporal_visibility` (Architecture v5 slides 23 and 24; RWB-PLT-E1070-APP).
- The namespace record this story owns is applied by the bootstrap job of RWB-PLT-E1070-APP; the two stories must carry the same retention and the same four search attributes, and this story owns the record and its evidence (RWB-PLT-E1070-APP AC5).
- The namespace `rwb-recovery` is fixed by Template and Rules §R4 and by Architecture v5; retention is 30 days and the search attributes are CaseId, Stage, ProductGroup and QueueCode as Keyword (Temporal and Drools Design slide 27; Architecture v5 slide 24).
- The codec is AES-GCM with keys in Key Vault per namespace, on every client and every worker, and the codec server for the Web UI is RWB-PLT-E2038's (Architecture v5 slides 8 and 24; Temporal and Drools Design slide 11).
- Azure Key Vault is available in the ACE subscription and the platform identity SY-CASEWF exists as a workload identity; SY-CASEWF is the working read of the assumption, because no read source names the platform login (GAP-1451; ASM-2546).
- The Workbench roles RW-PLATADM, RW-AUDIT and RW-SECADM exist through the environment group, published by RWB-P4-E1022-CON; this story maps them at the namespace and does not create them.
- The ACE internal certificate authority issues the certificates of the platform, and the client certificate profile is the one RWB-PLT-E1070-CON publishes.
- The archive destination for closed histories exists as the Blob container of RWB-PLT-E2039, so that the 30-day retention removes a history only after it has been archived.
- No production data is used in DEV or SIT: the namespaces hold synthetic histories only, and the mask rule of the user acceptance environment is unchanged (NFR-045).
- The security baseline of the platform applies: no secret in a manifest, an image, a repository or a log; no shared administrative credential; deny by default (Architecture v5 slide 35; NFR-052).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7), because it provisions infrastructure and builds nothing on another story. No approval is required to start, and the story is Draft (realignment v1).

### 4. Flow

1. Read the baseline record of RWB-PLT-NF08-INF and the namespace declaration of RWB-PLT-E1070-CON, and write the namespace record of this story from them: the name `rwb-recovery`, retention 30 days for closed workflows, the archive hand-off before expiry, the four Keyword search attributes, the entitlements and the quota set.
2. Verify the namespace on the cluster: status REGISTERED, retention 720 hours and 30 days, the four attributes present as Keyword, and no fifth attribute registered.
3. Create the codec key in Key Vault for this namespace with the AES-GCM algorithm and the key size the vault policy allows; record the key name, the current version and the version policy, and keep the exact rotation period as the placeholder until the platform infrastructure review.
4. Grant unwrap to the platform identity SY-CASEWF on this key only, and to no other identity: no service login, no human account and no shared operator identity holds unwrap.
5. Bind the namespace's certificate set: the frontend certificate from the ACE internal CA and the client certificates of the service workload identities under the profile of RWB-PLT-E1070-CON, with the namespace claim; record the set in the namespace register.
6. Set the per-namespace quotas and rate limits, record whether each value comes from a source or is the placeholder, and apply them to the namespace rather than to the cluster.
7. Map the entitlements at the namespace: RW-PLATADM operate, RW-AUDIT read, RW-SECADM decode under break-glass, every other Workbench role refused.
8. Turn on the evidence: the describe output, the key version list with the enabled version, the entitlement list, the attribute list, the quota record and the payload scan result, collected by one job and signed off as the evidence pack.
9. Test: a second apply changes nothing; a rotation moves the enabled version; an unwrap by another identity is refused; a namespace call with a certificate for another namespace is refused; a scan of the histories finds no clear personal value; a quota breach is refused with RESOURCE_EXHAUSTED.
10. Hand the namespace register and the evidence pack to RWB-PLT-E1070, RWB-PLT-E1071, RWB-PLT-E2038, RWB-PLT-E2039, RWB-PLT-NF08-INF and the 19 service teams, and record the enabled key version in the release evidence.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The namespace already exists with a different retention or a different attribute set | The apply refuses the change and reports the difference field by field; nothing is altered in place and no second namespace is created | MSG-PLT-N003-01 | AC1 |
| X2 | The enabled key version is disabled, or the key is absent when a worker starts | The data converter fails closed: no payload is written in clear, the workflow start is refused or retried under the worker policy, and an alert reaches RW-PLATADM and RW-SECADM | MSG-PLT-N003-02 | AC2, AC3 |
| X3 | An identity other than SY-CASEWF asks to unwrap the key | Key Vault refuses the operation, the attempt is recorded in the vault audit and an alert reaches security architecture | MSG-PLT-N003-03 | AC2, AC4 |
| X4 | A history, a payload, a log line or a metric label holds a clear personal value | The payload scan marks the run FAILED, the namespace is not signed off, and the finding goes to the owning service's story to fix the writer | MSG-PLT-N003-04 | AC3 |
| X5 | A client presents a certificate issued for another namespace, or names a foreign namespace | The call is refused with PERMISSION_DENIED, no workflow is started, and the client identity only is recorded | None (PERMISSION_DENIED) | AC4 |
| X6 | A namespace rate limit or quota is reached | The request is refused with RESOURCE_EXHAUSTED, the client retries under its own policy, and the quota record shows which value was hit | MSG-PLT-N003-05 | AC6 |
| X7 | A Workbench role other than the three mapped roles asks to operate, read or decode | The entitlement map refuses the role and no namespace operation is served | MSG-P4-002 | AC5 |

The sources fix the first statement of X2 without qualification: every client and every worker uses the payload codec with AES-GCM and keys in Key Vault per namespace (Architecture v5 slide 24), so a missing key is a hard failure of the write and not a fallback to clear text. What a worker does with a failed write — retry policy and alerting — belongs to RWB-PLT-E1071 and RWB-PLT-E2037, not to this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Provisions a namespace record, a key, an entitlement map, a quota record and an evidence pack; builds nothing on another story and needs no code change in a service |
| Negotiable | The key name, the rotation period, the quotas and rate limits, the certificate set and the exact retention beyond the closed-workflow rule are agreed at the platform infrastructure review; the namespace name, AES-GCM, the 30-day retention, the four search attributes and the three entitlements are fixed |
| Valuable | Gives every worker in waves 1 to 4 one isolated tenant and one encryption key on Day 1, and gives security and audit one record to read |
| Estimable | One namespace record, one codec key with its version policy, one entitlement map, one quota record, one evidence pack and six acceptance criteria |
| Small | Fits one sprint with the apply, the negative tests, the rotation and the evidence pack |
| Testable | Every criterion is tested against the live namespace, the vault and the evidence pack, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Temporal namespace rwb-recovery and its codec key

  Background:
    Given the shared Temporal cluster of the Recovery Workbench runs in DEV and SIT with its own persistence databases
    Given the namespace is the unit of isolation and carries its own retention, rate limits, certificates and encryption keys

  Scenario: AC1 The namespace rwb-recovery is registered with its own retention and quotas, and a second apply changes nothing (new, D-RCV-60)
    Given the namespace record of this story
    When it is applied to the cluster of an environment
    Then the namespace rwb-recovery is listed with status REGISTERED
    Then retention is 720 hours, 30 days, for closed workflows
    Then the namespace carries its own quotas and rate limits, recorded in the quota record with the source of each value
    Then the namespace carries its own certificate set and its own encryption key, and no setting is inherited from another namespace
    When the same record is applied a second time
    Then the namespace, its retention, its quotas and its certificates are unchanged and the run is recorded as a no-op
    When an existing namespace presents a different retention or a different attribute set
    Then the apply refuses the change and reports the difference, and nothing is altered in place

  Scenario: AC2 The codec key is an AES-GCM key in Key Vault, versioned, and only SY-CASEWF may unwrap it (new, D-RCV-60)
    Given the codec key of the namespace rwb-recovery
    When it is described in Key Vault
    Then its algorithm is AES-GCM and it belongs to this namespace only
    Then the enabled version is recorded in the namespace register and in the release evidence
    When the platform identity SY-CASEWF unwraps a payload of this namespace
    Then the operation succeeds and is recorded in the vault audit
    When any other identity asks to unwrap the same key
    Then the operation is refused, the attempt is audited and an alert reaches security architecture
    When the key is rotated under the version policy
    Then a new version becomes enabled, the previous version is kept for the overlap window and then disabled, and no payload is lost
    Then no key, no version identifier and no unwrap result appears in a manifest, a ConfigMap, an image, a repository or a pipeline log

  Scenario: AC3 No history, payload, log line or metric label holds clear personal data (new, D-RCV-60)
    Given the histories of the namespace rwb-recovery in an environment with synthetic data
    When the payload scan of the evidence pack runs
    Then every payload is codec-encrypted with the AES-GCM key of this namespace
    Then no history holds a name, an email address, an account number, a national identifier, a document or a contact detail in clear
    Then no log line, metric label or trace attribute of the platform carries a payload or a personal value
    When a history with a clear value is seeded for the test
    Then the scan marks the run FAILED, the namespace is not signed off and the finding is raised to the owner of the writer

  Scenario: AC4 The namespace entitlements are RW-PLATADM operate, RW-AUDIT read and RW-SECADM decode under break-glass, and no client reads across namespaces (new, D-RCV-60)
    Given the entitlement map of the namespace rwb-recovery
    When RW-PLATADM operates a workflow
    Then the operation is allowed and recorded
    When RW-AUDIT opens a workflow page
    Then the page is read-only and terminate, reset and signal are refused
    When RW-SECADM decodes a payload
    Then the decode is a break-glass action with a recorded reason and an audit entry
    When any other Workbench role asks to operate, read or decode
    Then the request is refused with MSG-P4-002 and no namespace operation is served
    When a client presents a certificate issued for another namespace, or names a foreign namespace
    Then the call is refused with PERMISSION_DENIED and no workflow is started

  Scenario: AC5 The only search attributes are CaseId, Stage, ProductGroup and QueueCode, and nothing else is indexed (new, D-RCV-60)
    Given the namespace rwb-recovery
    When its search attributes are listed
    Then exactly CaseId, Stage, ProductGroup and QueueCode are registered, all as Keyword
    Then no attribute holds a name, an email address, an account number, a national identifier or a document reference
    When a workflow is started with a custom search attribute that is not one of the four
    Then the start is refused and no workflow is created
    Then the attribute list of the evidence pack matches the namespace and the baseline record of RWB-PLT-NF08-INF

  Scenario: AC6 The per-namespace quotas and rate limits are applied and the namespace evidence pack is complete (new, D-RCV-60)
    Given the namespace rwb-recovery with its quota record
    When a client exceeds the request rate or the concurrent-workflow quota of the namespace
    Then the request is refused with RESOURCE_EXHAUSTED and the other namespaces on the cluster are unaffected
    Then the quota record states, for every value, either the source that fixes it or Not specified in the source documents (GAP-1451; ASM-2546)
    When the evidence pack is generated
    Then it holds the describe output, the key versions with the enabled version, the entitlement list, the search attributes, the quota record, the certificate set and the payload scan result
    Then it is signed off by SCB IT infrastructure and by security architecture, and it carries no personal value

  Scenario: AC7 The namespace keeps the boundary and business-rule constraints of section 8, BR1 to BR9 (new, D-RCV-60)
    Given the namespace rwb-recovery and the business rules BR1 to BR9 of section 8
    When the namespace, its schemas, topics, API bases, service shorts, key, entitlements, search attributes and settings are checked against the rules
    Then BR1: the namespace is the unit of isolation on the cluster, carries its own retention, rate limits, certificates and keys, and a new workbench takes a namespace and no second cluster
    Then BR2: no schema of the form rwb_<name>, no rwb.<short>.events.v1 topic, no /api/recovery/<short>/v1 base and no service short exists for the namespace
    Then BR3: the codec key is AES-GCM, one per namespace, held in Key Vault and read at run time through the workload identity, and the seed, the wrapped key and the unwrap result appear in no artefact or log
    Then BR4: the unwrap right on this namespace's key belongs to SY-CASEWF only, and no service login, human account or shared operator identity holds it
    Then BR5: no history holds clear personal data, and decode is a break-glass action of RW-SECADM through the codec server
    Then BR6: the search attributes are exactly CaseId, Stage, ProductGroup and QueueCode as Keyword, and a new attribute is a platform change and is never added quietly
    Then BR7: a closed workflow is retained for 30 days, and the archive run, its container and its immutability are not part of this story and belong to RWB-PLT-E2039
    Then BR8: RW-PLATADM operates the namespace, RW-AUDIT reads it, RW-SECADM decodes under break-glass, and every other Workbench role is refused
    Then BR9: quotas, rate limits, retention, the certificate set and the key policy are platform settings, and no business rule is expressed as a namespace setting and no namespace setting carries a business value
```

These seven criteria are new and test only the deliverable in the title: the namespace, its retention and quotas, its key, its entitlements, its attributes and its evidence. No legacy acceptance criterion is repeated here and no business value is asserted.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The namespace is the unit of isolation on one cluster per environment: `rwb-recovery` carries its own retention, rate limits, certificates and encryption keys, and a new workbench takes a namespace and not a second cluster | Architecture v5 slides 23, 24, 46; Template and Rules §R4 |
| BR2 | The namespace is shared platform and not one of the 19 services: no schema of the form `rwb_<name>`, no `rwb.<short>.events.v1` topic, no `/api/recovery/<short>/v1` base and no service short | Template and Rules §R4; Architecture v5 slides 4 and 41 |
| BR3 | The payload codec is AES-GCM, one key per namespace, held in Azure Key Vault and read at run time through the workload identity; the seed, the wrapped key and the unwrap result never appear in an artefact or a log | Architecture v5 slides 8, 24, 35; Temporal and Drools Design slides 11 and 23; NFR-052 |
| BR4 | The unwrap right belongs to the platform identity SY-CASEWF on this namespace's key only; no service login, no human account and no shared operator identity holds it | Temporal and Drools Design slide 11; Architecture v5 slide 35; ASM-2546 |
| BR5 | No history holds clear personal data: payloads carry identifiers and facts, and the personal values stay in the owning service's schema; decode is a break-glass action of RW-SECADM through the codec server | Temporal and Drools Design slide 27; Architecture v5 slide 35; NFR-053 |
| BR6 | The only search attributes are CaseId, Stage, ProductGroup and QueueCode as Keyword; a new attribute is a platform change and is never added quietly | Temporal and Drools Design slide 27; Architecture v5 slide 24; RWB-PLT-E1070-APP AC5 |
| BR7 | A closed workflow is retained for 30 days and is archived to Blob before the retention removes it; the archive run, its container and its immutability belong to RWB-PLT-E2039 | Temporal and Drools Design slide 27; Architecture v5 slide 23; RWB-PLT-E2039-APP |
| BR8 | RW-PLATADM operates the namespace, RW-AUDIT reads it and RW-SECADM decodes under break-glass; every other Workbench role is refused, and no client reads across namespaces | Temporal and Drools Design slide 11; Architecture v5 slide 35; RWB-PLT-E1070-CON |
| BR9 | Quotas, rate limits, retention, the certificate set and the key policy are platform settings with the sources of section 13; no business rule is expressed as a namespace setting and no namespace setting carries a business value | Template and Rules §R7.2 s17; NFR-052 |

### 9. State transitions

No case status changes in this story: no workflow is created, moved or closed here, and no business record is approved. What the story does have is a namespace lifecycle and a key-version lifecycle, described here so that the tests of AC1, AC2 and AC6 have something to assert.

| Object | From | Event | Condition | To |
|---|---|---|---|---|
| Namespace rwb-recovery | Absent | The namespace record is applied on the cluster | The retention, the four attributes and the quotas are the ones recorded | REGISTERED |
| Namespace rwb-recovery | REGISTERED | The record is applied a second time | Nothing differs | REGISTERED, unchanged |
| Namespace rwb-recovery | REGISTERED | A retention, attribute or quota value is changed | The change is accepted at the platform review and applied from the record | REGISTERED, with the new value |
| Namespace rwb-recovery | REGISTERED | The workbench is retired from this cluster | No open workflow remains and the archive of RWB-PLT-E2039 holds the closed histories | DEPRECATED |
| Namespace rwb-recovery | DEPRECATED | The archive is complete and the evidence pack is signed off | The namespace is removed from the register | Absent |
| Key version | Absent | The key is created in Key Vault for this namespace | The algorithm is AES-GCM | ENABLED |
| Key version | ENABLED | The version policy rotates the key | The new version is created and the previous one kept for the overlap | ENABLED (new version), the previous one ENABLED for the overlap |
| Key version | ENABLED (previous) | The overlap window ends | The new version is in use by every caller | DISABLED |
| Key version | ENABLED | A worker unwraps a payload and the grant is missing or the version is disabled | The caller is not SY-CASEWF, or the version is not enabled | UNWRAP-FAILED, refused and audited |

The transition owner is the platform identity SY-CASEWF for the key and SCB IT infrastructure for the namespace record. The rotation period, the overlap window, the namespace retirement path and the exact retention beyond the 30 days of the closed-workflow rule are Not specified in the source documents (GAP-1451; ASM-2546).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SCB IT infrastructure | Owns this story, the namespace record, the key, the entitlement map, the quota record and the evidence pack |
| ACE platform team | Owns the cluster, its persistence and the bootstrap job that applies the record; admits the namespace and its key into the platform |
| Security architecture | Approves the AES-GCM key policy, the unwrap grant, the 30-day retention, the search-attribute set and the break-glass decode path |
| Key Vault owner | Owns the vault, the key name, the version policy, the overlap window and the grant to SY-CASEWF; may not read a payload |
| Internal audit | Reads the entitlement list, the key versions and the evidence pack; confirms that no history can be read in clear |
| Platform on-call rota | Receives the alerts of section 14 and runs the checks of the run book of RWB-PLT-E2037 |
| RWB-PLT-E1070 owners | State the namespace, the certificate profile and the bootstrap job; they never change a namespace setting directly |
| RWB-PLT-NF08-INF owner | Owns the baseline standard this namespace record conforms to, and refuses a record that departs from it |
| RWB-PLT-E1071, RWB-PLT-E2038, RWB-PLT-E2039 owners | Consume the namespace and the key: the worker and its codec, the decode path and the archive; they never unwrap a payload outside their declared use |

The platform login and admin base, the per-namespace quotas and rate limits, the namespace certificate set beyond the frontend certificate, the key rotation period and the exact retention the namespace must carry beyond 30 days are Not specified in the source documents (GAP-1451; ASM-2546). The remaining values are agreed at the platform infrastructure review before wave 0 exit, and section 13 carries the assumption in force until then.

### 11. Data

| Item | Value |
|---|---|
| Sessions | None. The namespace holds no session; a staff session belongs to the edge store of RWB-PLT-N006-INF |
| Namespace settings | The name `rwb-recovery`, retention 720 hours and 30 days, the four Keyword search attributes, the quotas and rate limits, the certificate set and the record of where each value came from |
| Key versions | The key name, the algorithm AES-GCM, the enabled version identifier, the creation time of each version, the version policy and the identities that hold unwrap |
| Entitlements | RW-PLATADM operate, RW-AUDIT read, RW-SECADM decode under break-glass, and the refusal of every other Workbench role |
| Business data | None. No case, customer, account, document, decision, payment or partner value is held by the record, the key or the evidence pack |
| Personal data | None. The record names roles, identities and versions; no name, email address, account number, national identifier or contact detail appears |
| Workflow histories | Not held by this story. The histories live in the namespace and are the workers' records; this story sets the retention, the attributes and the key that protect them |
| Field identifiers | None owned. No DF-REF, DF-CAS or DF-DEC field is added or changed, and the Physical Schema is not changed |
| Retention | 30 days for a closed workflow, then the archive of RWB-PLT-E2039; the record and the key versions are kept for the life of the namespace and for the audit period the bank sets |
| Access | SCB IT infrastructure through the platform change process, RW-PLATADM through the Web UI, RW-AUDIT read-only, RW-SECADM break-glass decode; SY-CASEWF unwraps at run time and holds no account |

The record holds no field that a source does not define. None of the ten rows of this section carries a BR Field ID, because no row names a field of LDM v9 or Data Classification v5. Where a value the namespace needs is named by no source — the quotas, the rate limits, the certificate set and the rotation period — the record carries the placeholder and the value waits for the gap to close; no value is invented to fill it.

### 12. Contract

#### 12.1 REST operations provided

None. The platform has no service short (Template and Rules §R4 has no platform row), so it publishes no path under `/api/recovery/<short>/v1` and no Workbench endpoint. The namespace is reached through the Temporal frontend of RWB-PLT-E1070-CON, and its operational surface is the Web UI and the evidence pack.

#### 12.2 REST operations consumed

None. The namespace consumes no Workbench REST operation. The frontend gRPC call is the interface the workers use, and it is declared by RWB-PLT-E1070-CON; this story applies settings through the platform's own tooling and Key Vault.

#### 12.3 Events published

None. The namespace publishes no `rwb.<short>.events.v1` topic and no event schema; the decision-record, case and access events keep their owners, and the platform owns no topic at all (DP-14 declared as an absence).

#### 12.4 Events consumed

None. The namespace reacts to no Kafka event. A workflow that carries a case fact receives it through the owning service's worker and its own consumer, never through the namespace.

#### 12.5 Workflows and activities

None owned. The namespace hosts the workers of the 19 services, each polling only its own task queue `rwb-<service>`; the platform task queue `rwb-platform` carries the platform's own runs (JOB-21 and JOB-22) and belongs to RWB-PLT-E1071. This story creates no workflow, no activity and no worker.

#### 12.6 Schedules

None. No Temporal Schedule is created here; the archive Schedule belongs to RWB-PLT-E2039, the stuck-workflow scan and the smoke run to RWB-PLT-E1071 and RWB-PLT-E2037, and the namespace is not swept by a job of this story.

#### 12.7 Tables owned

None. The namespace owns no table in the ACE database and no `rwb_<name>` schema; its settings are namespace metadata on the cluster, and its histories live in the Temporal persistence of RWB-PLT-E1070. The row reads None for both platform stories.

#### 12.8 Contract fakes

None. A namespace has no service contract to fake; the tests run against a throwaway namespace on the test cluster, with a test key in a test vault and synthetic histories only, and the platform fake frontend of RWB-PLT-E1070-CON carries the same namespace name and settings.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 0 | No HTTP surface; the platform has no service short and no `/api/recovery` base |
| Kafka | 0 | 0 | The namespace owns no topic and consumes none |
| Temporal | The namespace itself: `rwb-recovery` with its retention, quotas, rate limits, certificates, entitlements, search attributes and codec key | 0 workflows and 0 activities of its own | The 19 services' workers run inside it; the platform task queue `rwb-platform` is not created here |
| File | 0 | 0 | No file is read or written; the archive file is RWB-PLT-E2039's |
| Platform | 1 (the namespace and its codec key) | None | One namespace, one AES-GCM key in Key Vault, one entitlement map, one quota record, one evidence pack |

The summary is five lines and not four because the namespace and its key are the call type of this story: a platform resource with no business surface and no business data.

### 13. Solution plan

**Deliverables.** The namespace record (name, retention, quotas, rate limits, certificate set, entitlements and search attributes) applied from configuration, the codec key in Key Vault with its version policy and the unwrap grant to SY-CASEWF, the entitlement map, the quota record, the payload scan job, the evidence pack generator, the negative test suite and the hand-over note to RWB-PLT-NF08-INF.

**Settings in force**

| Setting | Value |
|---|---|
| Namespace | `rwb-recovery` (Template and Rules §R4; Architecture v5 slides 23 and 24) |
| Version baseline | Temporal 1.30 or later, for Nexus and Worker Versioning (Temporal and Drools Design slide 32 item 6); the exact release is the one recorded in the environment design by RWB-PLT-E1070 |
| Retention | 720 hours, 30 days, for a closed workflow (Temporal and Drools Design slide 27) |
| Archive | A closed history is archived to Blob before retention removes it; the container and its immutability belong to RWB-PLT-E2039 |
| Search attributes | CaseId, Stage, ProductGroup, QueueCode, all Keyword; no fifth attribute (Temporal and Drools Design slide 27) |
| Key algorithm | AES-GCM, one key per namespace (Architecture v5 slides 8 and 24) |
| Key store | Azure Key Vault in the ACE subscription, read at run time through the workload identity; no key material in any artefact (NFR-052) |
| Key name and version policy | Not specified in the source documents (GAP-1451; ASM-2546); the working read is one key per namespace with an enabled version and one previous version kept for the overlap |
| Key rotation period | Not specified in the source documents (GAP-1451; ASM-2546) |
| Unwrap right | The platform identity SY-CASEWF on this namespace's key only (working read of ASM-2546) |
| Entitlements | RW-PLATADM operate, RW-AUDIT read, RW-SECADM decode under break-glass, every other role refused (Temporal and Drools Design slide 11) |
| Quotas and rate limits | Per namespace, not per cluster; the values are Not specified in the source documents (GAP-1451; ASM-2546) |
| Certificate set | The frontend certificate from the ACE internal CA and the client certificates under the profile of RWB-PLT-E1070-CON; any further certificate of the namespace is Not specified in the source documents (GAP-1451; ASM-2546) |
| Upgrade window | The platform maintenance window outside business hours (NFR-021 excludes the change window); the exact window is Not specified in the source documents (GAP-1451; ASM-2546) |
| Compatibility matrix | Server 1.30 or later with the SDK and the schema tool pinned per release; the exact triple is recorded by RWB-PLT-NF08-INF and the environment design, and where no source names it the value is Not specified in the source documents (GAP-1451; ASM-2546) |
| Region and tenancy | The bank's own cloud tenancy, SCB Azure, Southeast Asia (NFR-046) |
| Patching | The managed maintenance window of the platform, with the failover expected and alerted by RWB-PLT-E2037 |
| Runbook | Apply, verify, rotate, break-glass decode, retire and verify the evidence pack, each step with its owner role (registered through RWB-PLT-E1056-OPS) |

**Pattern application.** None of the decoupling-pattern markers of Template and Rules §R5.5 appears in this new platform story: it introduces no legacy table, no legacy login, no legacy topic name, no legacy task queue and no legacy API base, so no DP row is applied and the metadata row "Patterns applied" reads None. The two patterns the namespace serves are applied by the platform stories that use these resources: DP-02 (one login per service) is applied by the service DB stories against the schemas the namespace never touches, and DP-13 (`/api/recovery/<short>/v1`) is applied by the 19 service contract stories, because the platform publishes no path of its own. DP-01, DP-14 and DP-15 are declared as absences in BR2 and section 12: no schema, no topic, no migration.

**Build steps**

1. Write the namespace record as configuration: name, retention 720 hours and 30 days, the four Keyword attributes, the certificate set, the entitlements, the quota record and the source of each value, with the placeholder where none exists.
2. Apply the record to DEV and then SIT, and verify the describe output against the file; a difference fails the apply and is reported.
3. Create the AES-GCM key in Key Vault for the namespace, set the version policy with the rotation period as the placeholder, and record the enabled version.
4. Grant unwrap to SY-CASEWF only, and prove that every other identity is refused; confirm that no key material, version or unwrap result reaches a manifest, an image or a log.
5. Bind the certificate set under the profile of RWB-PLT-E1070-CON and record it in the register.
6. Apply the quotas and rate limits and run the quota test: the namespace refuses with RESOURCE_EXHAUSTED and the other namespaces are unaffected.
7. Map the entitlements and run the negative tests: RW-CASEOWN refused, RW-AUDIT read-only, RW-SECADM break-glass with a recorded reason, a foreign-namespace certificate refused.
8. Run the payload scan over the synthetic histories, seed a clear value once to prove the scan fails the run, and remove the seed.
9. Generate the evidence pack, sign it off with security architecture, and hand the register to the consuming stories and to RWB-PLT-NF08-INF.

**Done when.** The namespace exists in DEV and SIT with the settings of section 13, a second apply changes nothing, the key is an enabled AES-GCM version in Key Vault with unwrap held by SY-CASEWF alone, the four search attributes are the only ones registered, a quota breach is refused without touching another namespace, the payload scan is clean on the synthetic histories, and the evidence pack is signed off.

### 14. Validation and messages

| ID | When | Message | Raised to |
|---|---|---|---|
| MSG-PLT-N003-01 | An apply finds a namespace with a different retention or attribute set | The namespace {namespace} already holds {setting} = {current}; the record asks for {requested}. Nothing was changed. | SCB IT infrastructure and the ACE platform team |
| MSG-PLT-N003-02 | The enabled key version is absent or disabled when a payload is written | The codec key {keyName} has no enabled version for namespace {namespace}. The payload was not written. | RW-PLATADM, RW-SECADM and the platform on-call rota |
| MSG-PLT-N003-03 | An identity other than SY-CASEWF asks to unwrap | An unwrap of {keyName} was refused for {identity} at {time}. Only the platform identity may unwrap this key. | Security architecture and the Key Vault owner |
| MSG-PLT-N003-04 | The payload scan finds a clear value in a history | The scan found {pattern} in a payload of namespace {namespace}. The namespace is not signed off until the writer is fixed. | Security architecture, internal audit and the owner of the writer |
| MSG-PLT-N003-05 | A namespace quota or rate limit is reached | Namespace {namespace} refused {operation} with RESOURCE_EXHAUSTED at {time}; the applied value is {value}. | SCB IT infrastructure and the platform on-call rota |
| MSG-P4-002 | A role other than those named in BR8 asks for an action it is not entitled to | Not specified in the source documents (MSG-P4-002); the access contract owns the text | Not specified in the source documents (MSG-P4-002) |

The five message IDs belong to this story; they are operator and platform messages and not business messages, and none of them carries a user identifier, a payload or a personal value. The message a user sees when a role is refused is MSG-P4-002, owned by the access contract, and is not fixed here.

### 15. Screens and states

No Workbench screen in this story and no screen state either. The operational surfaces are three and none is composed by gateway-bff: the Temporal Web UI behind Entra ID, which shows the namespace with the two states of the baseline, operate for RW-PLATADM and read-only for RW-AUDIT, with the break-glass decode of RW-SECADM; the Key Vault view of the key versions, which shows the enabled version and the disabled overlap; and the evidence pack, which is a signed record and not a screen. The screens of the Workbench belong to gateway-bff and the front end, and this story adds nothing to them.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-N003-INF-01 | AC1 | Component | The namespace record applied to a clean namespace; REGISTERED, 720 hours, 30 days, the four Keyword attributes, the quotas and the certificate set; a second apply reports no change; a differing retention is refused and reported |
| TC-PLT-N003-INF-02 | AC2 | Integration | The AES-GCM key in a test vault; the enabled version recorded; an unwrap by SY-CASEWF succeeds and is audited; an unwrap by another identity is refused; a rotation enables a new version and disables the previous one after the overlap; a scan of manifests, ConfigMaps, images and pipeline logs finds no key material |
| TC-PLT-N003-INF-03 | AC3 | NFR | Synthetic histories with codec-encrypted payloads; a scan finds no name, email address, account number, national identifier, document or contact detail in clear; a seeded clear value fails the run; no log line or metric label carries a payload |
| TC-PLT-N003-INF-04 | AC4 | Component | RW-PLATADM operates, RW-AUDIT reads only, RW-SECADM decodes with a recorded reason, RW-CASEOWN and every other role refused with MSG-P4-002; a certificate issued for another namespace is refused with PERMISSION_DENIED; no cross-namespace read |
| TC-PLT-N003-INF-05 | AC5 | Component | The attribute list of the namespace; exactly CaseId, Stage, ProductGroup and QueueCode as Keyword; a start with a custom attribute is refused; the list matches the baseline record of RWB-PLT-NF08-INF |
| TC-PLT-N003-INF-06 | AC6 | NFR | A client above the rate limit and above the concurrent-workflow quota is refused with RESOURCE_EXHAUSTED while a second namespace is unaffected; the quota record carries a source or the placeholder for every value; the evidence pack holds all seven items and is signed off |
| TC-PLT-N003-INF-07 | AC7 | Component | The namespace record, schemas, topics, API bases, service shorts, key policy, entitlement map, search attributes and quota record checked against BR1 to BR9; no rwb_<name> schema, no rwb.<short>.events.v1 topic and no /api/recovery/<short>/v1 base exists; no second cluster is created; the archive is not run by this story; no namespace setting carries a business value |

### 17. Guardrails

- No business value in configuration: the retention, the quotas, the rate limits and the key policy are platform settings with the sources of section 13, and none of them is a parameter of a business rule (BR9).
- No personal data in a history, a payload, a metric label or a log line: the histories carry identifiers and facts, and a clear value fails the scan and blocks the sign-off (BR5, AC3).
- Secrets only in Key Vault: no key, seed, wrapped key, version identifier or unwrap result in a manifest, a ConfigMap, an image, a repository, a pipeline log or a runbook example (BR3, AC2).
- Private access only: the frontend on port 7233 inside the cluster network, the Web UI on its internal ingress, and no public listener (BR1, AC4).
- No shared administrative credential and no hand access: SY-CASEWF holds the unwrap right and no person unwraps a payload; a decode is RW-SECADM break-glass with a recorded reason (BR4, BR8).
- No cross-namespace read and no second namespace for the same workbench: a certificate issued for another namespace is refused, and a new workbench takes a namespace of its own (BR1, AC4).
- A decode is break-glass only: the codec server of RWB-PLT-E2038 is the only decode path, every decode is audited, and this story never decrypts a payload in a test or a log (BR5).
- The four search attributes are closed: a fifth attribute is a platform change and is never added quietly (BR6, AC5).
- No schema, no topic, no REST base and no migration: the platform is not one of the 19 services, and a gift of a schema or a topic here would undo the split (BR2, section 12).
- Every test payload is synthetic; no production history, payload or key is copied into DEV, SIT or a test (NFR-045).

### 18. Traceability

| Requirement ID | Requirement (short) | Source | What this story provides | Test cases |
|---|---|---|---|---|
| NFR-052 | Secrets are held in the key store and never in code, configuration files or prompts | Program BRD v4 §6.9 | The AES-GCM key in Key Vault with a version policy, an unwrap grant to one identity and a scan that no artefact carries key material | TC-PLT-N003-INF-02 |
| NFR-053 | Data is encrypted at rest and in transit | Program BRD v4 §6.9 | The codec key of the namespace, the encrypted payloads and the refusal of a clear value in a history | TC-PLT-N003-INF-02, TC-PLT-N003-INF-03 |
| NFR-020 | The Workbench is available during business hours: 99.9 percent | Program BRD v4 §6.4 | One namespace per environment with its own quotas, so a busy tenant cannot exhaust another and a namespace change is applied without a cluster restart | TC-PLT-N003-INF-06 |
| NFR-022 | Recovery point objective: the maximum data loss the business accepts | Program BRD v4 §6.4 (open; follows the ACE recovery point objective) | The key version record and the enabled version, so a restore of the persistence of RWB-PLT-E2039 is usable with the key that was in force | TC-PLT-N003-INF-02 |
| NFR-023 | Recovery time objective: the maximum time to restore service | Program BRD v4 §6.4 (open; follows the ACE recovery time objective) | The namespace record applied from configuration and the retirement path, so the namespace is rebuilt or replaced inside the platform objective | TC-PLT-N003-INF-01 |
| NFR-045 | No production data is used in development; user acceptance uses masked copies | Program BRD v4 §6.7 | Synthetic histories only in DEV and SIT, and a payload scan that refuses a clear value | TC-PLT-N003-INF-03 |

| Decision or source | What it fixes here |
|---|---|
| ADR-014 | Schema and login per service in ACE PostgreSQL: the namespace owns no schema and no login, and the separation the ADR fixes is never undone by a platform grant |
| ADR-016 | The reusable Temporal layer: one cluster per environment, a namespace per workbench, and a namespace rather than a second cluster for the next workbench |
| ADR-023 | Observability per service: the namespace produces the platform metrics that RWB-PLT-E2037 scrapes, and this story adds no per-service dashboard |
| Architecture v5 slides 8, 23, 24, 35, 46 | The codec keys in Key Vault, the five layers, one queue per service, the mTLS and role model, and the reuse rule for the next workbench |
| Temporal and Drools Design slides 11, 12, 27, 32 | The AES-GCM codec with keys per namespace, the L2 definition, the four search attributes and the 30-day retention, and version 1.30 or later |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1070-APP, RWB-PLT-E1070-CON | App development, Contract | Owners of the cluster, the persistence, the Web UI, the mTLS front door, the bootstrap job and the certificate profile this record is applied through |
| RWB-PLT-NF08-INF | Infrastructure | Owns the baseline standard this namespace record conforms to, and receives the namespace evidence as conformance evidence |
| RWB-PLT-E1071 | App development | Consumes the namespace and the key: the worker polls task queue `rwb-<service>` and runs the codec inside the worker |
| RWB-PLT-E2038 | App development, Contract | Owns the codec server, the decode path and the admin audit; this story owns the key and not the decode surface |
| RWB-PLT-E2039 | App development, Contract | Owns the backup, the failover, the upgrade and the archive that keeps a closed history after the 30 days |
| RWB-PLT-E2037 | App development, Contract | Owns the dashboard, the alerts and the run book the namespace is operated with |
| RWB-PLT-N010 | App development, Contract | Owns the workflow kit whose templates run in this namespace and never in workflow code with I/O |

The two open recovery objectives are the only requirement rows without a target: NFR-022 and NFR-023 are Open in the program BRD and follow the ACE objectives, so this story times the namespace apply and records the key version rather than inventing a number.

### 19. Out of scope

- The cluster, its two persistence databases, the frontend, the Web UI, the mTLS front door, the OIDC application and the namespace bootstrap job: RWB-PLT-E1070-APP and RWB-PLT-E1070-CON.
- The baseline standard, its compatibility matrix, the deterministic-workflow rule and the conformance evidence: RWB-PLT-NF08-INF.
- The worker, the SDK wiring, the client retry policy and the codec inside each worker: RWB-PLT-E1071.
- The codec server, the decode user interface and the Temporal admin audit: RWB-PLT-E2038.
- The backup, the point-in-time restore, the zone failover, the minor upgrade and the archive of closed histories to Blob: RWB-PLT-E2039.
- The dashboard, the alerts, the stuck-workflow scan and the run book catalog: RWB-PLT-E2037 and RWB-PLT-E1056-OPS.
- The workflow kit templates and their versioning: RWB-PLT-N010.
- The `ace-collection` namespace, its quotas and its keys; the platform registers and operates `rwb-recovery` only.
- The 19 services' schemas, topics, task queues, REST bases and business models; the platform owns none of them, and the namespace hosts their workers without owning their contracts.
- The Workbench screens and the admin console: gateway-bff and the front end, with the platform admin screens in a later epic.
