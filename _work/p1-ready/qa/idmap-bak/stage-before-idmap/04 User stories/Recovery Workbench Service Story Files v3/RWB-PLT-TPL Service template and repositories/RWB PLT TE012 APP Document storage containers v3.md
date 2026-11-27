# RWB-PLT-TE012-APP Document storage containers
SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-TE012-APP |
| Readiness decisions | RD-P1-004 |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-TPL |
| Wave | 0 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-012 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Size | Not sized; Not specified in the source documents (DOR-RWB-PLT-TE012-APP-16); the squad sizes it at refinement |
| Patterns applied | DP01, DP06, DP07, DP10, DP11, DP13, DP19 |
| Parallel lane | L-PLT-TPL-R |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | RWB-PLT-TE001-APP (not done yet; tracked, not blocking) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-029, blob storage with write-once policy; FR-PLT-028 is the event schema registry and is not used by this story) |
| Status | Draft (directive resolutions) |

**Version 3 changes**

- D-RCV-60 P1 developer readiness (RD-P1 register). Aligned the quoted English to Error and Message Standard v6.


**Change log.** D-RCV-60, 22 November 2026: RWB-TE-012 is moved with no impact, and this story is the target shape of the same storage. Every legacy rule, criterion, message and value is kept word for word: the four containers `rwb-intake`, `rwb-docs`, `rwb-docs-legal` and `rwb-quarantine`, blob versioning and 30 days of soft delete on `rwb-docs`, the time-based immutability policy of 3650 days locked in PROD only, managed-identity-only access with shared key access off and public network access off, the 10-second timeout, the identities RWB-DEV-SY-OCR, RWB-SIT-SY-OCR, RWB-UAT-SY-OCR, RWB-PROD-SY-OCR and RWB-SIT-SY-AGENT, the storage error strings, MSG-P5-002, MSG-GEN-006 and MSG-P4-002, and the `rwb.dochub.*` properties with the feature flag `rwb.dochub.storage-containers`. What changes is the shape: the storage now belongs to one owner, rwb-document (P5), so the in-process `DocumentContainers` interface becomes a published, versioned contract consumed one hop with a fake and a 2 s budget, the retention period, the soft-delete days and the container names become parameters and reference rows read through the contracts of rwb-case, the retention run becomes a Temporal Schedule on the task queue `rwb-document` instead of the legacy job, and the upload path a screen calls is the per-service base path `POST /api/recovery/document/v1/cases/{caseId}/documents` behind the gateway-bff composite route. AC1 to AC12 are the legacy criteria with the origin tag added and only that path re-pointed; AC13 is the one new criterion. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-PLT-TE012-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 10 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform administrator (RW-PLATADM)**, I want **one set of blob containers per environment — `rwb-intake`, `rwb-docs`, `rwb-docs-legal` with a time-based immutability policy, and `rwb-quarantine` — reached by managed identity only, published as the container contract of rwb-document with a fake, with the container names, the retention period and the soft-delete days read as parameters and reference rows, and swept by a Temporal Schedule on the task queue of rwb-document, instead of an in-process `DocumentContainers` interface reached from inside the monolith**, so that **legal documents cannot be overwritten, no service other than rwb-document holds a container client, a key or a shared access signature, and the storage is set up once for the single owner of documents with no business value in its code**.

The legacy story sets up the storage: one storage account per environment with a private endpoint, the four containers, blob versioning and soft delete on `rwb-docs`, a time-based immutability policy on `rwb-docs-legal` (locked in PROD only), managed-identity-only access, a readiness indicator that joins the health endpoint, an error mapper, a content-hash guard and the upload path that shows 409 MSG-P5-002 and 503 MSG-GEN-006. None of that behaviour is withdrawn here. What the realignment changes is who owns the storage and how the rest of the estate reaches it. Arch v5 gives documents to rwb-document (P5), which owns metadata, custody, OCR text and fields, signatures and retention, and states that documents go to Blob with WORM through rwb-document only (slides 16, 29 and 41). A container client can no longer be handed to another module, because there is no module that shares a process with it. The platform half this story owns is therefore the storage itself — the account settings, the four containers, the policies, the role assignments, the readiness check, the error mapper, the hash guard and the retention Schedule template — plus the rule that the containers are reached only through the published contract of rwb-document. No other service opens a container, no platform table reaches a container, and no screen is given a storage credential.

### 2. Business rationale

Audit findings record that evidence for decisions was incomplete or unreliable, and a notice or contract held in a shared folder can be replaced without trace. A write-once container whose immutability policy refuses any overwrite or delete inside its retention period is the control that answers this: the legal copy of a court notice stays byte-identical for its class period, and every refused attempt is visible. This story is the storage that the document store, the intake and the malware scan write to, and it meets REQ-DCM-003 (legal document types held in a write-once container that cannot be altered or deleted) and REQ-DCM-002 (the document hub is the system of record and no other store holds the authoritative copy), both of which are Must.

Arch v5 moves the storage behind one owner. Slide 29 pairs the 19 schemas with one login each and names the storage in the same breath: Blob storage with WORM holds documents and it is for rwb-document only. Slide 41 gives rwb-document the ownership of metadata, custody, OCR text and fields, signatures and retention, its schema `rwb_document`, its first API path and its task queue `rwb-document`; slide 16 spells out that the service accepts `POST /documents` and that it runs a Schedule for retention over its WORM files, and that the same service reaches rwb-agent as a tool for read extracted fields. Slide 9 draws the line for the whole estate: documents go to Blob with WORM through rwb-document only. Slide 7 places the workbench inside the ACE platform behind the shared App Gateway, so the containers are an internal resource of one service and never a path a browser reaches. Slide 20 gives every service its own block of the template — own task queue, own Schedules, `/health` and `/metrics` for the platform — and gives gateway-bff one hop to an owner with a 2 s timeout and a breaker per service.

Three consequences follow, and they are the whole target change of this story. First, a single owner means a single contract: what the monolith expressed as the in-process `DocumentContainers` interface (four container clients and a readiness value) becomes a published, versioned contract of rwb-document, consumed by any other service one hop with a fake and a 2 s budget, so no caller can hold a container handle (DP-11). Second, a single owner means the storage carries no business value: the retention period, the soft-delete days and the four container names are parameters read through the parameters contract of rwb-case and reference rows read through its reference-data contract, because the platform carries no values of its own (DP-06, DP-07). Third, the legacy job that swept retention becomes a Temporal Schedule in the owning service, on the task queue `rwb-document` in the namespace `rwb-recovery`, with an overlap policy and a catch-up window, because Arch v5 replaces shared Quartz with Schedules in the owning service and JOB-17 retention is owned by rwb-document (DP-10; slide 44). The value the bank keeps is unchanged: a legal document cannot be changed or removed inside its retention period, and the standard container keeps earlier versions and restores a deleted blob inside the soft-delete window. What changes is that the guarantee now survives the split: one service issues the credential, one service writes the blob, one contract is the only way in, and the retention run cannot be started by a service that does not own the store.

### 3. Preconditions

- **RWB-PLT-E1042-CON** is published: the parameters contract of rwb-case and its client library (DP-06). The retention period of a retention class, the soft-delete days and the cadence of the retention Schedule are parameter values read through it and never values in code.
- **RWB-PLT-E1043-CON** is published: the reference-data contract of rwb-case (DP-07). The retention classes — the class `LEGAL10Y` that the legacy story assumes at 3,650 days — and the document types with the class of each are reference rows read through it.
- **RWB-PLT-E1071-CON** is published: the Temporal workflow kit that carries the Scheduled job template and the overlap policy and catch-up window of a Schedule (DP-10). The retention Schedule is declared through it and not built by hand.
- **RWB-PLT-N001-CON** is published: the gateway-bff composite route contract (DP-19). The staff upload and the readiness surface are reached through it; this story publishes no route of its own.
- The **two service CON dependencies** are published: **RWB-P3-E1042-CON** (the rwb-case contract behind the parameters) and **RWB-P3-E1043-CON** (the rwb-case contract behind the reference data). Both are consumed as published contracts and their fakes, so neither blocks the build (Template and Rules §R5.4, C).
- **RWB-PLT-TE001-APP** is done: the recovery module folder and the boundary test that the storage code sits in. It is external, team-type work and is tracked, not blocking.
- The ACE storage pattern is used (DL27, option A): one storage account per environment in the SCB tenant with a private endpoint, shared key access off, public network access off and TLS 1.2 minimum.
- The managed identities RWB-DEV-SY-OCR, RWB-SIT-SY-OCR, RWB-UAT-SY-OCR and RWB-PROD-SY-OCR exist, and rwb-document has its own managed identity in each environment: the legacy ACE service identity becomes the identity of rwb-document, which is the only holder of a container role.
- The infrastructure pipeline of the service template can apply storage templates to DEV and SIT.
- The feature flag `rwb.dochub.storage-containers` is a platform-library flag, read at start.
- Whether the storage account and the four containers stay one set per environment shared by the 19 services or become one set per service when only rwb-document may reach them, the container naming standard in the target, where the retention period and the retention classes are held now that they are parameters and reference rows, the name of the retention Schedule and the exact surface the readiness is read on are Not specified in the source documents (GAP-1438; ASM-2531). They are applied as the working defaults of section 13 until the gap closes.

### 4. Flow

1. Platform administrator: applies the storage infrastructure template for the environment, which sets the storage account (shared key access off, public network access off, TLS 1.2 minimum, private endpoint) and creates the containers `rwb-intake`, `rwb-docs`, `rwb-docs-legal` and `rwb-quarantine`, whose names come from the container properties and not from a literal in the template body.
2. Template: turns on blob versioning and soft delete for `rwb-docs`, sets the time-based immutability policy on `rwb-docs-legal` with the retention days read as a parameter (locked in PROD, unlocked in DEV, SIT and UAT), and assigns roles: the rwb-document service identity on `rwb-intake`, `rwb-docs` and `rwb-docs-legal`; SY-OCR on `rwb-intake`, `rwb-docs` and `rwb-quarantine`. No other identity receives a container role.
3. System: on start, StorageReadinessIndicator reads the parameters and the reference rows, checks that the four containers exist and that `rwb-docs-legal` has its immutability policy, and joins the result to the service health endpoint (`/health`), so the platform collects one readiness per service.
4. rwb-document: writes each file through its storage adapter with its managed identity, to `rwb-docs-legal` for a write-once type and to `rwb-docs` for any other type, at the name `{container}/{caseId}/{documentId}/v{docVersion}`.
5. Any client: an overwrite or delete of a blob in `rwb-docs-legal` is refused by the storage service; StorageErrorMapper turns the refusal into `WriteOnceViolationException`, which rwb-document maps to 409 MSG-P5-002 on its own contract, and the attempt is written to the audit log.
6. rwb-document: a new version is a new blob at `v{n+1}`; the earlier blob stays readable.
7. Platform administrator: sees the document hub readiness on the interface and job monitor surface, which gateway-bff composes from the service health (DP-19), and the case owner uploads on the case documents screen through `POST /api/recovery/document/v1/cases/{caseId}/documents` on rwb-document's per-service base.
8. RetentionScheduleTemplate: creates the retention Schedule on the task queue `rwb-document`; when it fires, the service's own worker runs the retention activity, which reads the retention class of each document type through the reference-data contract and the retention period through the parameters contract, and acts on the store it owns.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Overwrite of a write-once blob | The storage service refuses; the blob is unchanged; rwb-document records the attempt in the audit log with the identity and the time | MSG-P5-002 | AC1 |
| X2 | Delete of a write-once blob | The storage service refuses; the blob is unchanged and still readable | MSG-P5-002 | AC2 |
| X3 | Access with an account key or a shared access signature | The storage service refuses the request | None | AC6 |
| X4 | Access by an identity with no role on the container | The storage service refuses the request | None | AC7 |
| X5 | Access from outside the private endpoint | The storage service refuses the request | None | AC8 |
| X6 | A container or the write-once policy is missing at start | rwb-document reports not ready and refuses every write; the readiness names the container | MSG-GEN-006 | AC9 |
| X7 | Storage does not answer within the 10-second timeout | `StorageUnavailableException`; the caller returns 503 on rwb-document's contract | MSG-GEN-006 | AC10 |
| X8 | A user session reads the quarantine container | Refused; only SY-OCR writes there | None | AC11 |
| X9 | A write to an existing blob name in `rwb-docs-legal` with the same content | The storage service refuses; the adapter compares the hash and returns the existing blob | None | AC12 |
| X10 | A role without Documents C uploads a document | 403 on the upload path | MSG-P4-002 | AC14 |
| X11 | The reference-data contract does not answer when the retention class of a document type is asked | The write is refused, fail closed: no container is chosen, no blob is written and no document row is created, because the class that decides the container and the period is unknown | MSG-GEN-006 | AC9, AC13 |
| X12 | The retention Schedule does not run | The readiness and the job monitor report it; no document is deleted and no policy is applied outside its period | None | AC13 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the four platform contracts, the two rwb-case contracts and the module folder (RWB-PLT-TE001-APP); the document service builds against the container contract and its fake, so no service has to be finished first; no screen |
| Negotiable | The retention period, the soft-delete days and the container names are parameters and reference rows; the Schedule's cadence and overlap policy are configuration of the Scheduled job template; the account count per environment is the recorded assumption |
| Valuable | A legal document cannot be changed or removed inside its retention period, and no service other than rwb-document can reach the containers at all |
| Estimable | One storage template, one published contract with a fake, one configuration class, one readiness indicator, one error mapper, one hash guard and one Schedule declaration |
| Small | Settings, one small adapter layer and one Schedule template with tests; no business logic |
| Testable | Each criterion below runs against the SIT storage account and the two contract fakes, with the container contract fake of rwb-document for the caller side |

### 7. Acceptance criteria

```gherkin
Feature: Document storage containers

  Background:
    Given the SIT storage account has containers "rwb-intake", "rwb-docs", "rwb-docs-legal" and "rwb-quarantine"
    Given "rwb-docs-legal" has a time-based immutability policy of 3650 days

  Scenario: AC1 Write-once (legacy RWB-TE-012 AC1)
    Given court notice "DOC-0701" stored at "rwb-docs-legal/RW-2026-000701/DOC-0701/v1" with hash "H701"
    When a client using the ACE service managed identity tries to overwrite it
    Then storage refuses the write with "BlobImmutableDueToPolicy"
    Then the blob hash is still "H701"
    Then the attempt is in the audit log with the identity and the time
    Then DocumentStore.replaceContent for "DOC-0701" raises WriteOnceViolationException, shown as 409 with MSG-P5-002

  Scenario: AC2 Delete is refused (legacy RWB-TE-012 AC2)
    Given court notice "DOC-0701" in "rwb-docs-legal"
    When a client using the ACE service managed identity tries to delete it
    Then storage refuses the delete
    Then the blob is still readable

  Scenario: AC3 A new blob in the write-once container is allowed (legacy RWB-TE-012 AC3)
    Given court notice "DOC-0701" at "v1" in "rwb-docs-legal"
    When the ACE service identity writes "rwb-docs-legal/RW-2026-000701/DOC-0701/v2"
    Then the write succeeds and both "v1" and "v2" are readable

  Scenario: AC4 The standard container keeps earlier versions (legacy RWB-TE-012 AC4)
    Given "rwb-docs/RW-2026-000702/DOC-0702/v1" holds an appraisal report
    When the blob is overwritten by the ACE service identity in SIT
    Then the previous blob version is still readable through blob versioning
    Then a deleted blob can be restored within the 30 days of soft delete

  Scenario: AC5 The identities hold only their roles (legacy RWB-TE-012 AC5)
    Given the role assignments applied by the template in SIT
    When the assignments are listed
    Then the ACE service identity holds Storage Blob Data Contributor on "rwb-intake", "rwb-docs" and "rwb-docs-legal" only
    Then "RWB-SIT-SY-OCR" holds Storage Blob Data Contributor on "rwb-intake", "rwb-docs" and "rwb-quarantine" only

  Scenario: AC6 Key-based access is refused (legacy RWB-TE-012 AC6)
    Given the storage account has shared key access disabled
    When a client calls "rwb-docs" with the account key or with a shared access signature
    Then storage refuses the request with "KeyBasedAuthenticationNotPermitted"

  Scenario: AC7 An identity with no role is refused (legacy RWB-TE-012 AC7)
    Given managed identity "RWB-SIT-SY-AGENT" has no role on "rwb-docs-legal"
    When it tries to read "rwb-docs-legal/RW-2026-000701/DOC-0701/v1"
    Then storage refuses with "AuthorizationPermissionMismatch"

  Scenario: AC8 Public network access is refused (legacy RWB-TE-012 AC8)
    Given public network access is disabled on the storage account
    When a client outside the private endpoint calls the account
    Then the system refuses the request

  Scenario: AC9 A missing immutability policy stops the document hub (legacy RWB-TE-012 AC9)
    Given the rwb-document upload contract mock returns 503 with MSG-GEN-006 while the document hub is not ready
    Given the immutability policy is removed from "rwb-docs-legal" in DEV
    When the service starts
    Then the readiness check reports the document hub as not ready, naming "rwb-docs-legal"
    Then an upload through POST /api/recovery/document/v1/cases/{caseId}/documents returns 503 with MSG-GEN-006
    Then the system writes no document row

  Scenario: AC10 Storage does not answer (legacy RWB-TE-012 AC10)
    Given the storage account does not answer within 10 seconds
    When BlobStorageAdapter writes a file to "rwb-docs"
    Then it raises StorageUnavailableException after 10 seconds
    Then the upload endpoint returns 503 with MSG-GEN-006

  Scenario: AC11 The quarantine container is closed to user sessions (legacy RWB-TE-012 AC11)
    Given file "Q-0001" in "rwb-quarantine"
    When the ACE service tries to read it on behalf of a case owner
    Then the system refuses the read
    Then only "RWB-SIT-SY-OCR" can write to "rwb-quarantine"

  Scenario: AC12 A repeated write of the same file is not an overwrite (legacy RWB-TE-012 AC12)
    Given "rwb-docs-legal/RW-2026-000703/DOC-0703/v1" holds a file with hash "H703"
    When BlobStorageAdapter is asked to write the same file with hash "H703" to the same name
    Then the system attempts no overwrite and the existing blob reference is returned
    Then the same name with a different hash raises WriteOnceViolationException

  Scenario: AC13 One owner, one contract and a Schedule for retention (new, D-RCV-60)
    Given the rwb-document container contract is published with its fake and a 2 s client budget
    Given the four container names and the retention period are read as parameters and reference rows
    When another service needs a document
    Then it calls the rwb-document contract one hop and holds no container client of its own
    Then no service but rwb-document holds a role or a credential on "rwb-intake", "rwb-docs", "rwb-docs-legal" or "rwb-quarantine"
    When the retention run starts
    Then the run is a Temporal Schedule on task queue "rwb-document" in namespace "rwb-recovery", and its cadence is a parameter
    When a case owner uploads a document on the case documents screen
    Then the screen calls POST /api/recovery/document/v1/cases/{caseId}/documents through the gateway-bff composite route, which is the per-service base path of rwb-document

  Scenario: AC14 A role without Documents C is refused the upload (new, D-RCV-60)
    Given a user session whose role has no Documents C permission
    When the user uploads a document through POST /api/recovery/document/v1/cases/{caseId}/documents
    Then the system returns 403 with MSG-P4-002

  Scenario: AC15 Only rwb-document and SY-OCR hold a container and the retention run is its Schedule (new, D-RCV-60)
    Given the role assignments and the job definitions of the platform
    When they are listed
    Then no service other than rwb-document and SY-OCR holds a container client, a key or a shared access signature
    Then no platform table reaches a container
    Then the retention run is a Temporal Schedule of rwb-document on task queue "rwb-document" in namespace "rwb-recovery"

  Scenario: AC16 A retried or timed-out upload does not create a second version (new, D-RCV-60)
    Given "rwb-docs-legal/RW-2026-000703/DOC-0703/v1" holds a file with hash "H703"
    When the upload activity of rwb-document is retried or runs past its timeout
    Then a write of identical content returns the existing blob
    Then a different content on the same name is refused with MSG-P5-002 at 409
```

**Note on the criteria.** SCR-30 (Case documents) states in the screen specification are loading, list and upload; its empty, error and no-access states are not specified in the source documents (DOR-RWB-PLT-TE012-APP-10). AC1 to AC12 are the legacy criteria of RWB-TE-012, copied word for word with the origin tag added to each `Scenario` line; no legacy line and no legacy value was changed, and only the upload path in AC9 is re-pointed, because the single base of the legacy service is replaced by the per-service base of the owning service. AC9 gains one `Given` line as its first `Given`: the rwb-document upload contract fake returns 503 with MSG-GEN-006 while the document hub is not ready, so the same criterion can be proved with the fake before SIT carries a broken policy. AC13 to AC16 are the new criteria; AC13 carries no business value: it tests the container contract, the single storage owner, the parameter and reference-data read, the retention Schedule and the upload path behind gateway-bff. The storage owner is rwb-document (P5) and no business rule changed.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The write-once container of rwb-document refuses overwrite and delete for the retention period; the policy is locked in PROD and unlocked in DEV, SIT and UAT so test data can be removed, and the period is the parameter `legalRetentionDays` 3650 read through the parameters contract, not a literal | NFR-029; CTL-12; template parameter legalRetentionDays 3650, assumed; DL26; DP-06 |
| BR2 | A change to a stored document is a new blob at the next version; earlier versions stay readable, and the version in the name is the `doc_version` of the owning service | FEAT-DCM-20; VR-P5-001-2; Arch v5 slide 41 |
| BR3 | Storage is reached only by managed identity; account keys and shared access signatures are disabled, and the identity that writes is the managed identity of rwb-document and of SY-OCR only | Story intent; CTL-09; Arch v5 slides 20 and 29 |
| BR4 | Each identity holds a role only on the containers it needs, and the four names are container properties read at start rather than literals in code or in the pipeline; the storage account is Not specified in the source documents (GAP-1031), the per-environment container naming is Not specified in the source documents (GAP-1031), and the managed identity assignment is Not specified in the source documents (GAP-1031), while the immutability period per retention class is the parameter of BR1 | Least privilege; roles of SY-OCR in roles.txt (Documents CRU); DP-06 |
| BR5 | rwb-document reports ready only when the four containers exist and the write-once policy is in place; the readiness joins the service health endpoint the platform collects | DL27; Arch v5 slide 20 |
| BR6 | The standard container keeps blob versions and soft-deleted blobs for 30 days, and the days are a parameter (`softDeleteDays` 30) read through the parameters contract | Template parameter softDeleteDays 30, assumed; DL27; DP-06 |
| BR7 | A write of identical content to an existing write-once name returns the existing blob; different content is a violation, and the period that decides the class comes from a reference row | R-UNI-40; CTL-12; DP-07 |
| BR8 | One owner holds the store: rwb-document (P5) owns metadata, custody, OCR text and fields, signatures and retention in `rwb_document`, and the containers with WORM are reached only through its published, versioned contract, consumed one hop with a fake and a 2 s budget; no other service holds a container client, a key or a shared access signature, and no platform table reaches a container | Arch v5 slides 9, 16, 29 and 41; DP-01; DP-11; ASM-2531 |
| BR9 | The retention run is a Temporal Schedule of rwb-document on the task queue `rwb-document` in namespace `rwb-recovery`, with an overlap policy and a catch-up window from the Scheduled job template; the cadence and the period it applies are configuration and reference rows, and no shared scheduler table is used | Arch v5 slide 44 (JOB-17, monthly, 1st Sunday); Ownership Map JOB-17; DP-10; Temporal design v1 slide 12 |

### 9. State transitions

None. This story does not change a case status or a document status. It sets up containers, policies and role assignments.

The states below are the states of the readiness of rwb-document and of the retention run, and they change no business object.

| From | Event | Condition | To |
|---|---|---|---|
| Not ready | The service starts | A container is missing, or the immutability policy on `rwb-docs-legal` is absent, or the parameters or reference rows do not answer | Not ready (the readiness names the container or the contract) |
| Not ready | The readiness check passes | The four containers exist and the policy is present | Ready |
| Not ready | A write arrives | None | Refused with 503 and MSG-GEN-006; no blob and no document row |
| Ready | A write arrives | None | Ready (the write follows the class of the document type) |
| Ready | The immutability policy is removed or lapses | None | Policy lapsed (ready drops to not ready at the next check; writes refused) |
| Policy lapsed | The platform administrator reapplies the template | The policy is locked again | Ready |
| Ready | The retention Schedule fires | The Schedule is enabled and the worker polls its queue | Retention scheduled |
| Retention scheduled | A worker of rwb-document picks the run | None | Retention running |
| Retention running | The run completes | None | Retention scheduled (waiting for the next fire) |
| Retention running | The run fails | A storage error, or the parameters or reference rows do not answer | Retention failed (reported on the job monitor; no document deleted) |
| Retention failed | The platform administrator reruns the run or the next fire starts | None | Retention scheduled |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM, platform administrator | Applies the infrastructure template, reads the readiness check on the interface and job monitor surface, and reruns a failed retention run (Platform administration CRUD) |
| RW-SECADM, security administrator | Reviews the role assignments on the containers (Platform administration CRUDA) |
| SY-OCR, OCR and extraction pipeline | Writes to `rwb-intake`, `rwb-docs` and `rwb-quarantine` with its managed identity |
| RW-CASEOWN, case owner | Uploads documents through the contract of rwb-document, which uses its own managed identity (Documents CRU) |
| Solution architect with Compliance | Owns DL27 |
| No role | May reach a container directly, hold a container key or a shared access signature, ask rwb-document for a container handle, or delete inside the immutability period; every one of these is refused, and a role without Documents C is refused with MSG-P4-002 |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DOC-006 | document | storage_ref | Read (format {container}/{caseId}/{documentId}/v{docVersion}) |
| DF-DOC-010 | document | write_once | Read |
| DF-DOC-011 | document | doc_version | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

`document`, `document_field` and `document_type` live in `rwb_document`, the schema of rwb-document (P5), per the Ownership Map and Arch v5 slide 41; no other service's schema is read by this story, and no platform table reaches a container (DP-01). `storage_ref` keeps the format `{container}/{caseId}/{documentId}/v{docVersion}` within varchar(400), and the three fields above are read by the storage and the retention code; the row that holds them is written by rwb-document and not by this story. The retention class of a document type is a reference row read through the reference-data contract of rwb-case, so no class value and no period sits in this code (DP-07).

### 12. Contract

The service row of this story is `platform`, which is not one of the 19 service rows of Template and Rules §R4: it publishes no REST base, no topic, no task queue and no schema of its own. The store it sets up belongs to rwb-document (P5), and the names below are the names of that owner. The contract version this story builds against is v1, the version segment of the base path `/api/recovery/document/v1/`.

#### 12.1 REST operations provided

None by this story. The upload path `POST /api/recovery/document/v1/cases/{caseId}/documents` (Ownership Map row `POST /cases/{caseId}/documents`, owner P5; Arch v5 slide 16 gives `POST /documents`) belongs to rwb-document and is named here only as the path its callers use; this story adds no operation, and the platform reserves no REST base of its own.

#### 12.2 REST operations consumed

None as a path of this story. The contract dependencies are consumed as published contracts and their fakes, and no path, version or payload of one is repeated here:

| Contract dependency | Owner | What this story needs from it |
|---|---|---|
| `RWB-P3-E1042-CON` | P3 rwb-case (the platform contract behind it is `RWB-PLT-E1042-CON`, epic RWB-PLT-LIB) | The parameters that carry the retention period of a class (3650 days, or the value of the class in force), the soft-delete days (30) and the cadence of the retention Schedule (DP-06) |
| `RWB-P3-E1043-CON` | P3 rwb-case (the platform contract behind it is `RWB-PLT-E1043-CON`, epic RWB-PLT-LIB) | The retention classes as reference rows — the class `LEGAL10Y` at 3650 days and the document types with the class of each — so the container and the period are chosen from a row and not from code (DP-07) |

The published container contract of rwb-document is consumed by the other services of the estate with a fake, one hop, a 2 s budget and a breaker per service (DP-11). Its operations and payloads belong to the contract stories of rwb-document and are not repeated here; this story only requires that the contract exists, is versioned, and hands out no container client.

#### 12.3 Events published

None. This story publishes nothing on a Kafka topic: the platform carries no topic of its own, and the document events `DocumentStored` and `DocumentFieldsExtracted` on `rwb.document.events.v1` belong to rwb-document (Arch v5 slides 16 and 42).

#### 12.4 Events consumed

None. The readiness check and the retention run read contracts and their own configuration; nothing in this story waits on a topic, and a document event is not a trigger for storage setup.

#### 12.5 Workflows and activities

| Workflow or activity | Task queue | Namespace | Owner | Use |
|---|---|---|---|---|
| Retention activity of the document hub (the retention run of JOB-17) | `rwb-document` | `rwb-recovery` | P5 rwb-document | Reads the reference row of each document type and its parameters, then applies retention to the store it owns; the platform contributes the Scheduled job template and the readiness of the run, not a worker of its own |

Arch v5 slide 16 gives rwb-document a `DocumentIntakeWorkflow` and a retention Schedule, and slide 44 gives JOB-17 the owner rwb-document with the mechanism Schedule; the Ownership Map gives JOB-17 the replacement "Temporal Schedule retention in rwb-document". The worker that runs the activity is the worker of rwb-document, so no platform worker is deployed and the platform task queue is not used.

#### 12.6 Schedules

| Schedule | Decides by | Overlap policy | Catch-up window | Instance |
|---|---|---|---|---|
| The retention Schedule of rwb-document (JOB-17), whose name is Not specified in the source documents (GAP-1438; ASM-2533) and whose cadence is a parameter, with the value given by Arch v5 slide 44 at monthly, 1st Sunday | A reference row and a parameter read through the reference-data and parameters contracts, never a value in code | Skip, as the overlap policy of the Scheduled job template | Bounded, as the catch-up window of the Scheduled job template | The Schedule and its worker belong to rwb-document on the task queue `rwb-document` in namespace `rwb-recovery`; this story declares the template, not the instance |

The value of the cadence comes from the job map, and the row that decides the run is the class of each document type; both are configuration of the owning service so that a change to either needs no code change. No shared scheduler table is created and no Quartz job is registered (DP-10; Temporal design v1 slide 32, "jobs as Schedules, no Quartz").

#### 12.7 Tables owned

None. This story owns no table of its own, and it writes no service table: `document`, `document_field` and `document_type` belong to `rwb_document`, the schema of rwb-document (P5), and the storage reference they carry is read by the storage code, never written by it (Ownership Map; Arch v5 slide 41; DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Documented answer used by the tests |
|---|---|---|
| rwb-case parameters fake | `RWB-P3-E1042-CON` behind `RWB-PLT-E1042-CON` | The retention period 3650 days, the soft-delete days 30 and the cadence of the retention Schedule, as the parameter values in force for the environment (AC13, TC-PLT-TE012-APP-14) |
| rwb-case reference-data fake | `RWB-P3-E1043-CON` behind `RWB-PLT-E1043-CON` | The retention class `LEGAL10Y` at 3650 days and the document types with the class of each, so the write-once container is chosen from a row (AC1, AC12, AC13) |
| rwb-document container and upload contract fake | The published, versioned contract of rwb-document (P5), consumed one hop with a 2 s budget | A container handle that is opaque to the caller and no storage credential, 503 with MSG-GEN-006 while the document hub is not ready, and 409 with MSG-P5-002 on a write-once overwrite (AC9, AC13) |

The storage account itself is not faked: AC1 to AC8, AC10, AC11 and AC12 run against the storage account of the environment, because the policy, the roles, the private endpoint and the key refusal are properties of the account and cannot be proved against a stub.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Count | Detail |
|---|---|---|
| REST | 1 consumed, 1 named as the caller's path | The container contract of rwb-document, consumed by the other services one hop with a fake and a 2 s budget (DP-11), and the upload path `POST /api/recovery/document/v1/cases/{caseId}/documents` behind gateway-bff that the staff screen calls (DP-13, DP-19); nothing provided by this story |
| Kafka | None | No event is published or consumed; the document events belong to rwb-document |
| Temporal | 1 | The retention Schedule and its activity on the task queue `rwb-document` in namespace `rwb-recovery` (DP-10; JOB-17) |
| File | 4 containers, plus claim-check content | `rwb-intake`, `rwb-docs`, `rwb-docs-legal` and `rwb-quarantine` on one storage account with a private endpoint; the content a claim-check message points at is served as a link by rwb-document, never as data in the message (Arch v5 slide 11) |

### 13. Solution plan

**Package.** `recovery/dochub/storage`, Java package `recovery.dochub.storage`, kept from the legacy story, plus the storage part of the service template: the infrastructure template fragment that every service of the 19 applies when it needs a container, and the Scheduled job declaration of the workflow kit that rwb-document reuses for its retention run. The container clients are packaged so that only the owning service can construct them; the published contract of rwb-document exposes no client type.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Components**

| Component | Type | Responsibility |
|---|---|---|
| Storage infrastructure template | Configuration | Account settings, four containers, versioning and soft delete on `rwb-docs`, the immutability policy on `rwb-docs-legal` with its days read as a parameter, and the role assignments of rwb-document and SY-OCR (BR1, BR3, BR4, BR6) |
| DocumentContainers published contract | Published contract | The versioned contract of rwb-document for a document and for the storage readiness of the hub; it hands out no container client, so a caller cannot reach a blob except through the owner (BR8; DP-11) |
| DocumentContainersConfig | Service | Builds the clients with DefaultAzureCredential restricted to managed identity, with the 10-second timeout and the four container names read from configuration (BR3, BR4) |
| StorageReadinessIndicator | Service | BR5: the four containers and the immutability policy are checked at start and on the readiness probe, and the result joins the service health endpoint |
| StorageErrorMapper | Service | Maps `BlobImmutableDueToPolicy` and the conflicts on `rwb-docs-legal` to `WriteOnceViolationException`, timeouts to `StorageUnavailableException`, and writes the audit event for a refused overwrite or delete (BR1, BR7) |
| ContentHashGuard | Service | BR7: compares the SHA-256 of an existing write-once blob before a write, and returns the existing reference when the content is identical |
| RetentionScheduleTemplate | Configuration | Declares the retention run as a Temporal Schedule on the task queue `rwb-document` with the overlap policy, the catch-up window, the cadence and the class of each document type read as configuration and reference rows (BR9; DP-10) |

**Database.** No new business table, and no table of its own. `storage_ref` values follow `{container}/{caseId}/{documentId}/v{docVersion}` within varchar(400) and are held by `document` in `rwb_document`, the schema of rwb-document (P5), owned by rwb-document and not by this story; this story reads the three fields of section 11 and writes none of them (DP-01).

**Configuration and reference data.**

- Properties per environment: `rwb.dochub.storage.account-url`, `rwb.dochub.container.intake`, `rwb.dochub.container.standard`, `rwb.dochub.container.legal`, `rwb.dochub.container.quarantine`, `rwb.dochub.storage.timeout-seconds` 10.
- Template parameters: `legalRetentionDays` 3650 (assumed; DL26), `legalPolicyLocked` true in PROD only, `softDeleteDays` 30 (assumed; DL27). The first and the third are the parameter values read through the parameters contract of rwb-case and are kept here only as the deployed defaults of the environment (DP-06).
- Retention classes as reference rows read through the reference-data contract of rwb-case: the class `LEGAL10Y` at 3650 days and the document types with the class of each; no class and no period is a literal in the code or in the pipeline (DP-07). The cadence of the retention Schedule and its overlap policy and catch-up window are configuration of the Scheduled job template (DP-10).
- Feature flag: `rwb.dochub.storage-containers`. Off, the readiness check reports not ready and every document write is refused with 503 rather than written outside the write-once container.
- Archive contract (GAP-0490): the write-once archive path is `retention/YYYY-MM-DD/<table>/` with a manifest of the row count and the SHA-256 per file; this story owns the container's account, credential scope and immutability policy.

**Build steps**

1. Write the infrastructure template with the account settings, the four containers whose names come from configuration, the policies and the role assignments, and the retention days read as a parameter; apply it in DEV and SIT.
2. Build DocumentContainersConfig with managed identity credentials only, and test that a key-based client and a shared access signature are refused (AC6, AC8).
3. Build StorageErrorMapper with the audit event, and test AC1 and AC2 against the storage account of SIT.
4. Build ContentHashGuard and test AC12, including the class that decides the container.
5. Build StorageReadinessIndicator, join it to the service health endpoint, and test AC9 in DEV with the immutability policy removed.
6. Publish the container contract of rwb-document with its fake: an opaque handle, a 2 s client budget, a breaker per caller, 503 MSG-GEN-006 while not ready and 409 MSG-P5-002 on a write-once overwrite; test AC13 with the two contract fakes.
7. Declare the retention Schedule through the Scheduled job template on the task queue `rwb-document`, with the cadence, the overlap policy and the catch-up window as configuration, and test that a failing run reports failed and deletes nothing.

**Done when.** The test cases of section 16 pass in SIT, the template is applied in DEV and SIT, the security administrator has reviewed the role assignments, only rwb-document holds a container role, and the retention Schedule has run once and reported on the job monitor.

The account count per environment, the container naming standard, where the retention period and the classes are held, the name of the Schedule and the readiness surface are Not specified in the source documents (GAP-1438; ASM-2531); the single set of four containers, the legacy values 3650 and 30 days, the four legacy container names and the one Schedule on the task queue `rwb-document` are ASM-2531, ASM-2532 and ASM-2533.

Open decisions DL10 (ASM-2250, ASM-2357, ASM-2377, ASM-2863), DL26 (ASM-0247, ASM-0264, ASM-0275, ASM-0355) and DL27 (ASM-1771, ASM-2532, ASM-2709, ASM-2716) stay open; each is answered by its listed assumption as confirmed by the directive.

The defaults recorded in ASM-B-PLT-TPL-03-TE012-1, ASM-B-PLT-TPL-03-TE012-2 and ASM-B-PLT-TPL-03-TE012-3 apply until the wave 0 storage review fixes the account and container count, the container naming standard, the home of the retention values and classes, the name of the retention Schedule and the readiness surface (GAP-1438).

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-002 | Overwrite or delete of a write-once document | Legal documents cannot be changed. Add a new version instead. |
| MSG-GEN-006 | Storage unavailable or document hub not ready | {system} is not available. Try again in a few minutes. |
| MSG-P4-002 | Role without Documents C | You cannot {action} here. Your role does not include it. |

The three texts are copied unchanged from RWB-TE-012 and this story adds no message text. In MSG-GEN-006 the {system} names the document hub when the readiness is the cause and the storage when the timeout is; X11 uses the same message because a write whose class cannot be read is a write the hub cannot serve. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story, and no new screen state. The platform administrator sees the readiness of the document hub on the interface and job monitor surface, which gateway-bff composes from the service health and the job state through its composite route (DP-19); the story publishes no route, and the surface names the container or the Schedule that is not healthy, never a business value. The case owner uploads on the case documents screen (SCR-30 Case documents), which calls `POST /api/recovery/document/v1/cases/{caseId}/documents` on the per-service base of rwb-document through the same composite route (DP-13). The upload response carries MSG-P5-002 at 409 when the write-once container refuses a change, MSG-GEN-006 at 503 when the storage or the hub is not ready, and MSG-P4-002 at 403 when the role holds no Documents C. The states of SCR-30 are: empty, Not specified in the source documents (CG-ALL-1623); loading, as in Screen Specifications v1 section SCR-30; error, Not specified in the source documents (CG-ALL-1623); no access, Not specified in the source documents (CG-ALL-1623).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-012-01 | AC1, BR1 | Component | Synthetic court notice in rwb-docs-legal |
| TC-TE-012-02 | AC2, BR1 | Component | Delete attempt on the same blob |
| TC-TE-012-03 | AC3, BR2 | Component | v2 blob for the same document |
| TC-TE-012-04 | AC4, BR6 | Component | Overwrite and delete in rwb-docs in SIT |
| TC-TE-012-05 | AC5, BR4 | Component | Role assignment listing in SIT |
| TC-TE-012-06 | AC6, BR3 | Component | Client with account key and with a shared access signature |
| TC-TE-012-07 | AC7, BR4 | Component | Managed identity RWB-SIT-SY-AGENT |
| TC-TE-012-08 | AC8, BR3 | Component | Client outside the private endpoint |
| TC-TE-012-09 | AC9, BR5 | Component | Policy removed in DEV |
| TC-TE-012-10 | AC10 | Component | Storage stub with a 10-second timeout |
| TC-TE-012-11 | AC11, BR4 | Component | File in rwb-quarantine |
| TC-TE-012-12 | AC12, BR7 | Component | Same and different content to an existing write-once name |
| TC-TE-012-13 | Access | End to end | RW-REFADM user (Documents -) calls POST /cases/{caseId}/documents; refused with MSG-P4-002 |
| TC-PLT-TE012-APP-14 | AC13 | Integration | The container contract of rwb-document with its fake and a 2 s budget, the parameters and reference-data fakes at 3650 days, 30 days and the class LEGAL10Y, and the retention Schedule on the task queue rwb-document, once with a failed run |
| TC-PLT-TE012-APP-15 | AC13 | Integration | Fake of the rwb-document container contract, every operation, event and activity of section 12 at a 2 s budget |
| TC-PLT-TE012-APP-16 | AC14 | End to end | User whose role has no Documents C uploads through POST /cases/{caseId}/documents; refused with MSG-P4-002 |
| TC-PLT-TE012-APP-17 | AC15, BR8, BR9 | Integration | Role assignments and job definitions of the platform listed against the owner rwb-document |
| TC-PLT-TE012-APP-18 | AC16 | Integration | Retried and timed-out upload activity against the fake of the rwb-document container contract at a 2 s budget |

The thirteen legacy test case rows keep their ID, Covers and Data cells word for word, and only the Level cell is mapped to the target shape: the legacy storage and configuration rows TC-TE-012-01 to TC-TE-012-12 become Component, and the legacy Access row TC-TE-012-13 becomes End to end. TC-PLT-TE012-APP-14 is the new row for AC13. The full test, with its Given, When and Then, stays in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same TC ID.

### 17. Guardrails

- No business value in code: the retention period, the soft-delete days and the four container names are parameters and reference rows read through the contracts of rwb-case (DP-06, DP-07), and the cadence of the retention Schedule is configuration of the owning service.
- No personal data in logs, tests or prompts: blob names carry case and document IDs only, never a customer name or ID number; test files are synthetic, and the readiness and the job monitor name a container or a Schedule, never content.
- No read of another service's tables (DP-01): `document`, `document_field` and `document_type` are read in `rwb_document` and nowhere else, and no platform table reaches a container. No other service holds a container client (DP-11): a caller reaches a document through the published contract of rwb-document, one hop, 2 s, with a breaker per service, and no container client, key or shared access signature leaves the owning service.
- No account key, connection string or shared access signature in code, configuration or the pipeline; shared key access stays off and public network access stays off, and access is only the managed identity of rwb-document and of SY-OCR.
- The immutability policy is locked in PROD only, and no role may delete inside the immutability period; the test environments stay unlocked so that synthetic data can be removed.
- No shared scheduler table and no Quartz job: the retention run is a Temporal Schedule in the owning service, so a failed run is visible and deletes nothing (DP-10; Temporal design v1 slide 32).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-003 | Legal document types held in a write-once container that cannot be altered or deleted | Business Requirements Program, section 5.5 | FEAT-DCM-01 | 13 Manage documents and correspondence | R-UNI-40, BR9 | TC-TE-012-01 to TC-TE-012-03, TC-TE-012-09, TC-TE-012-12, TC-PLT-TE012-APP-14 |
| REQ-DCM-002 | The document hub is the system of record; no other store holds the authoritative copy | Business Requirements Program, section 5.5 | FEAT-DCM-19 | 13 Manage documents and correspondence | BR8 | TC-TE-012-04 to TC-TE-012-08, TC-TE-012-10, TC-TE-012-11, TC-TE-012-13, TC-PLT-TE012-APP-14 |

| Target element | Source | What this story does with it | Test cases |
|---|---|---|---|
| DP-01 | Template and Rules §R5.5; Arch v5 slide 29 | The storage reference and the document fields are read in the schema of the owner, `rwb_document`, and no other schema is read | TC-TE-012-09, TC-PLT-TE012-APP-14 |
| DP-06 | Template and Rules §R5.5 | The retention period, the soft-delete days and the cadence are parameter values read through the parameters contract of rwb-case, never literals | TC-PLT-TE012-APP-14 |
| DP-07 | Template and Rules §R5.5 | The retention classes and the document types are reference rows read through the reference-data contract of rwb-case | TC-TE-012-01, TC-TE-012-12, TC-PLT-TE012-APP-14 |
| DP-10 | Template and Rules §R5.5; Arch v5 slide 44 | The retention run is a Temporal Schedule on the task queue `rwb-document`, with the overlap policy and catch-up window of the Scheduled job template | TC-PLT-TE012-APP-14 |
| DP-11 | Template and Rules §R5.5; Arch v5 slide 20 | The in-process `DocumentContainers` interface becomes a published contract with a fake, one hop and a 2 s budget, so no caller holds a container client | TC-PLT-TE012-APP-14, TC-PLT-TE012-APP-15 |
| DP-13 | Template and Rules §R5.5 | The upload path a screen calls is the per-service base path of rwb-document, not the legacy single base | TC-TE-012-09, TC-PLT-TE012-APP-14 |
| DP-19 | Template and Rules §R5.5; Arch v5 slide 16 | The staff upload and the readiness are reached through the gateway-bff composite route, and this story publishes no route | TC-TE-012-13, TC-PLT-TE012-APP-14 |
| Arch v5 slide 16 | rwb-document accepts `POST /documents`, runs a Schedule for retention, and keeps files in Azure Blob with WORM | The upload path of the owner and the retention Schedule of the owner | TC-PLT-TE012-APP-14 |
| Arch v5 slide 29 | Blob storage with WORM holds documents for rwb-document only; one login and one schema per service | The single owner of the containers and the refusal of a container client to any other service | TC-TE-012-04 to TC-TE-012-08, TC-PLT-TE012-APP-14 |
| Arch v5 slide 41 | P5 owns metadata, custody, OCR text and fields, signatures and retention, in `rwb_document`, with `rwb-document` as its task queue | The owner of the store, the schema of the three fields and the queue of the retention run | TC-TE-012-09, TC-PLT-TE012-APP-14 |
| Arch v5 slide 44 | JOB-17 retention, monthly on the 1st Sunday, owner rwb-document, mechanism Schedule, overlap policy skip and catch-up window | The retention Schedule, its cadence value and its instance in the owning service | TC-PLT-TE012-APP-14 |
| Arch v5 slide 9 and 7 | Documents go to Blob with WORM through rwb-document only, inside the ACE platform behind the shared App Gateway | The containers are an internal resource of one service and no browser reaches them | TC-TE-012-08, TC-PLT-TE012-APP-14 |
| Arch v5 slide 20 | Every service is built from the template with its own queue and Schedules and publishes `/health` and `/metrics`; gateway-bff makes one hop with a 2 s timeout and a breaker per service | The readiness on the health endpoint, the Schedule of the owning service and the contract budget | TC-TE-012-09, TC-PLT-TE012-APP-14 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON | Contract | H: the parameters contract, the reference-data contract, the workflow kit with the Scheduled job template, and the gateway-bff route contract this story builds against |
| RWB-P3-E1042-CON, RWB-P3-E1043-CON | Contract | C: the two rwb-case contracts consumed at run time through their fakes |
| RWB-PLT-TE001-APP | APP | X: the recovery module folder and the boundary test the storage code sits in; tracked, not blocking |
| RWB-PLT-TE004-APP | APP | The masked copy of the same storage: it loads the masked extract into the schemas of the 19 services and reads the intake container, so it depends on this template and on the owner of the store |
| The document service stories of rwb-document (P5) | APP, CON | The store itself: the document row, the container chosen per document type, the upload endpoint and its screen, the custody and the retention job on JOB-17 are owned there, and this story sets up the storage they use |

### 19. Out of scope

- Choosing the container per document type and writing the document row: rwb-document (P5) owns both, and this story only guarantees that a container is reachable through its contract.
- Retention classes, archive and the retention job: RWB-E1-041 in the legacy numbering, and JOB-17 which becomes the retention Schedule of rwb-document; the class values are reference rows of rwb-case.
- Legal hold on a case or a document (REQ-DCM-016; DL27).
- The backup and restore test of the document store (REQ-DCM-015; DL27).
- Sizing and cost of the storage (REQ-DCM-014; NFR-069).
- The upload endpoint and its screen: rwb-document (P5) owns `POST /api/recovery/document/v1/cases/{caseId}/documents` and SCR-30 Case documents, and this story names the path only as its caller's path.
- The storage part of RWB-PLT-TE004-APP, which is the masked copy of the same storage and is a story of its own.
- The contents of `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-N001-CON`, `RWB-P3-E1042-CON` and `RWB-P3-E1043-CON`; this story builds against them and adds no path.
