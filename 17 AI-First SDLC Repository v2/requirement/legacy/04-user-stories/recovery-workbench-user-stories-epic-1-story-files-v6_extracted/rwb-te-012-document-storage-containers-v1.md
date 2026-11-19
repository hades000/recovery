<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB TE 012 Document storage containers v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB TE 012 Document storage containers v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-TE-012 Document storage containers

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-TE-012 |
| Epic | E1, release 30 November 2026 |
| Module | P5 Document hub |
| Feature | None |
| Requirement IDs | REQ-DCM-003, REQ-DCM-002 |
| BRD section | Business Requirements Program, section 5.5 |
| L3 process | 13 Manage documents and correspondence |
| Decision | DL27 |
| Priority | Must |
| Depends on | RWB-TE-001 |
| Status | Ready for build |

## 1. Story

As a **platform administrator**, I want **blob containers for documents, with a write-once container for legal types, reached by managed identity**, so that **legal documents cannot be overwritten**.

## 2. Business rationale

Audit findings record that evidence for decisions was incomplete or unreliable, and a notice or contract held in a shared folder can be replaced without trace. This story sets up the storage that the document store (RWB-E1-024), the intake (RWB-E1-057) and the malware scan (RWB-E1-041) write to: an intake container, a standard container with version history, a write-once container whose immutability policy refuses any overwrite or delete inside its retention period, and a quarantine container, all reached only by managed identity. It meets REQ-DCM-003 and REQ-DCM-002 and is the storage behind control CTL-12 and the storage pattern recommended under DL27.

## 3. Preconditions

- RWB-TE-001 (recovery module folder and boundary test) is done.
- The ACE storage pattern is used (DL27, option A recommended): one storage account per environment in the SCB tenant with a private endpoint.
- The managed identities RWB-DEV-SY-OCR, RWB-SIT-SY-OCR, RWB-UAT-SY-OCR and RWB-PROD-SY-OCR exist, and the ACE service has its own managed identity in each environment.
- The retention period of the write-once policy is assumed at 3,650 days (10 years), matching the class LEGAL10Y, until the bank retention schedule is supplied (DL26).
- The infrastructure pipeline of the ACE repository can apply storage templates to DEV and SIT.

## 4. Flow

1. Platform administrator: applies the infrastructure template for the environment, which sets the storage account (shared key access off, public network access off, TLS 1.2 minimum, private endpoint) and creates the containers rwb-intake, rwb-docs, rwb-docs-legal and rwb-quarantine.
2. Template: turns on blob versioning and soft delete for rwb-docs, sets the time-based immutability policy on rwb-docs-legal (locked in PROD, unlocked in DEV, SIT and UAT), and assigns roles: the ACE service identity on rwb-intake, rwb-docs and rwb-docs-legal; SY-OCR on rwb-intake, rwb-docs and rwb-quarantine.
3. System: on start, StorageReadinessIndicator checks that the four containers exist and that rwb-docs-legal has its immutability policy; the document hub reports ready only if both hold.
4. Document store (RWB-E1-024): writes each file through BlobStorageAdapter with the managed identity, to rwb-docs-legal for a write-once type and to rwb-docs for any other type, at the name {caseId}/{documentId}/v{docVersion}.
5. Any client: an overwrite or delete of a blob in rwb-docs-legal is refused by the storage service; StorageErrorMapper turns the refusal into WriteOnceViolationException, which the store maps to 409 MSG-P5-002, and the attempt is written to the ACE audit log.
6. Document store: a new version is a new blob at v{n+1}; the earlier blob stays readable.
7. Platform administrator: sees the document hub readiness on SCR-44 Interface and job monitor.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Overwrite of a write-once blob | Storage refuses; blob unchanged; attempt in the audit log | MSG-P5-002 | AC1 |
| X2 | Delete of a write-once blob | Storage refuses; blob unchanged | MSG-P5-002 | AC2 |
| X3 | Access with an account key or a shared access signature | Storage refuses | None | AC6 |
| X4 | Access by an identity with no role on the container | Storage refuses | None | AC7 |
| X5 | Access from outside the private endpoint | Storage refuses | None | AC8 |
| X6 | A container or the write-once policy is missing at start | Document hub not ready; writes refused | MSG-GEN-006 | AC9 |
| X7 | Storage does not answer within the timeout | StorageUnavailableException; callers return 503 | MSG-GEN-006 | AC10 |
| X8 | A user session reads the quarantine container | Refused | None | AC11 |
| X9 | A write to an existing blob name in rwb-docs-legal with the same content | Refused by storage; the adapter checks the hash and returns the existing blob | None | AC12 |
| X10 | A role without Documents C uploads a document | 403 | MSG-P4-002 | Access test TC-TE-012-13 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the module folder (RWB-TE-001); RWB-E1-024, RWB-E1-041 and RWB-E1-057 build on it |
| Negotiable | The retention period and the soft delete days are template parameters; container names follow the ACE naming standard |
| Valuable | A legal document cannot be changed or removed inside its retention period |
| Estimable | One infrastructure template, one container configuration class, one readiness check, one error mapper |
| Small | Settings and one small adapter layer with tests |
| Testable | Each scenario below runs against the SIT storage account |

## 7. Acceptance criteria

```gherkin
Feature: Document storage containers

  Background:
    Given the SIT storage account has containers "rwb-intake", "rwb-docs", "rwb-docs-legal" and "rwb-quarantine"
    Given "rwb-docs-legal" has a time-based immutability policy of 3650 days

  Scenario: AC1 Write-once
    Given court notice "DOC-0701" stored at "rwb-docs-legal/RW-2026-000701/DOC-0701/v1" with hash "H701"
    When a client using the ACE service managed identity tries to overwrite it
    Then storage refuses the write with "BlobImmutableDueToPolicy"
    Then the blob hash is still "H701"
    Then the attempt is in the audit log with the identity and the time
    Then DocumentStore.replaceContent for "DOC-0701" raises WriteOnceViolationException, shown as 409 with MSG-P5-002

  Scenario: AC2 Delete is refused
    Given court notice "DOC-0701" in "rwb-docs-legal"
    When a client using the ACE service managed identity tries to delete it
    Then storage refuses the delete
    Then the blob is still readable

  Scenario: AC3 A new blob in the write-once container is allowed
    Given court notice "DOC-0701" at "v1" in "rwb-docs-legal"
    When the ACE service identity writes "rwb-docs-legal/RW-2026-000701/DOC-0701/v2"
    Then the write succeeds and both "v1" and "v2" are readable

  Scenario: AC4 The standard container keeps earlier versions
    Given "rwb-docs/RW-2026-000702/DOC-0702/v1" holds an appraisal report
    When the blob is overwritten by the ACE service identity in SIT
    Then the previous blob version is still readable through blob versioning
    Then a deleted blob can be restored within the 30 days of soft delete

  Scenario: AC5 The identities hold only their roles
    Given the role assignments applied by the template in SIT
    When the assignments are listed
    Then the ACE service identity holds Storage Blob Data Contributor on "rwb-intake", "rwb-docs" and "rwb-docs-legal" only
    Then "RWB-SIT-SY-OCR" holds Storage Blob Data Contributor on "rwb-intake", "rwb-docs" and "rwb-quarantine" only

  Scenario: AC6 Key-based access is refused
    Given the storage account has shared key access disabled
    When a client calls "rwb-docs" with the account key or with a shared access signature
    Then storage refuses the request with "KeyBasedAuthenticationNotPermitted"

  Scenario: AC7 An identity with no role is refused
    Given managed identity "RWB-SIT-SY-AGENT" has no role on "rwb-docs-legal"
    When it tries to read "rwb-docs-legal/RW-2026-000701/DOC-0701/v1"
    Then storage refuses with "AuthorizationPermissionMismatch"

  Scenario: AC8 Public network access is refused
    Given public network access is disabled on the storage account
    When a client outside the private endpoint calls the account
    Then the system refuses the request

  Scenario: AC9 A missing immutability policy stops the document hub
    Given the immutability policy is removed from "rwb-docs-legal" in DEV
    When the service starts
    Then the readiness check reports the document hub as not ready, naming "rwb-docs-legal"
    Then an upload through POST /api/recovery/v1/cases/{caseId}/documents returns 503 with MSG-GEN-006
    Then the system writes no document row

  Scenario: AC10 Storage does not answer
    Given the storage account does not answer within 10 seconds
    When BlobStorageAdapter writes a file to "rwb-docs"
    Then it raises StorageUnavailableException after 10 seconds
    Then the upload endpoint returns 503 with MSG-GEN-006

  Scenario: AC11 The quarantine container is closed to user sessions
    Given file "Q-0001" in "rwb-quarantine"
    When the ACE service tries to read it on behalf of a case owner
    Then the system refuses the read
    Then only "RWB-SIT-SY-OCR" can write to "rwb-quarantine"

  Scenario: AC12 A repeated write of the same file is not an overwrite
    Given "rwb-docs-legal/RW-2026-000703/DOC-0703/v1" holds a file with hash "H703"
    When BlobStorageAdapter is asked to write the same file with hash "H703" to the same name
    Then the system attempts no overwrite and the existing blob reference is returned
    Then the same name with a different hash raises WriteOnceViolationException
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The write-once container refuses overwrite and delete for the retention period; the policy is locked in PROD and unlocked in DEV, SIT and UAT so test data can be removed | NFR-029; CTL-12; template parameter legalRetentionDays 3650, assumed; DL26 |
| BR2 | A change to a stored document is a new blob at the next version; earlier versions stay readable | FEAT-DCM-20; VR-P5-001-2 |
| BR3 | Storage is reached only by managed identity; account keys and shared access signatures are disabled | Story intent; CTL-09 |
| BR4 | Each identity holds a role only on the containers it needs | Least privilege; roles of SY-OCR in roles.txt (Documents CRU) |
| BR5 | The document hub reports ready only when the four containers exist and the write-once policy is in place | DL27 |
| BR6 | The standard container keeps blob versions and soft-deleted blobs for 30 days | Template parameter softDeleteDays 30, assumed; DL27 |
| BR7 | A write of identical content to an existing write-once name returns the existing blob; different content is a violation | R-UNI-40; CTL-12 |

## 9. State transitions

None. This story does not change a case status or a document status. It sets up containers, policies and role assignments.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM, platform administrator | Applies the infrastructure template and reads the readiness check (Platform administration CRUD) |
| RW-SECADM, security administrator | Reviews the role assignments on the containers (Platform administration CRUDA) |
| SY-OCR, OCR and extraction pipeline | Writes to rwb-intake, rwb-docs and rwb-quarantine with its managed identity |
| RW-CASEOWN, case owner | Uploads documents through the store, which uses the ACE service identity (Documents CRU) |
| Solution architect with Compliance | Owns DL27 |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DOC-006 | document | storage_ref | Read (format {container}/{caseId}/{documentId}/v{docVersion}) |
| DF-DOC-010 | document | write_once | Read |
| DF-DOC-011 | document | doc_version | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

No endpoint of its own. The upload endpoint POST /api/recovery/v1/cases/{caseId}/documents (RWB-E1-026, RWB-E1-024) uses these containers: Documents, right C, scope applied; 403 without the right (MSG-P4-002); 503 when storage is unavailable or the document hub is not ready (MSG-GEN-006).

**Container configuration (P5, used by BlobStorageAdapter in RWB-E1-024, QuarantineMover in RWB-E1-041 and IntakeService in RWB-E1-057)**

```java
package recovery.dochub.storage;
public interface DocumentContainers {
    BlobContainerClient intake();       // rwb.dochub.container.intake
    BlobContainerClient standard();     // rwb.dochub.container.standard
    BlobContainerClient legal();        // rwb.dochub.container.legal
    BlobContainerClient quarantine();   // rwb.dochub.container.quarantine
    StorageReadiness readiness();       // containers present, legal policy present
}
// Exceptions raised to callers: WriteOnceViolationException, StorageUnavailableException
```

## 13. Solution plan

**Package.** folder `recovery/dochub/storage`, Java package `recovery.dochub.storage`; the infrastructure template in the ACE infrastructure folder, in the format the ACE team uses.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| Storage infrastructure template | Configuration | Account settings, four containers, versioning and soft delete on rwb-docs, immutability policy on rwb-docs-legal, role assignments |
| DocumentContainers | Published interface | Container clients and readiness |
| DocumentContainersConfig | Service | Builds the clients with DefaultAzureCredential restricted to managed identity, and the 10-second timeout |
| StorageReadinessIndicator | Service | BR5; joins the ACE health endpoint |
| StorageErrorMapper | Service | Maps BlobImmutableDueToPolicy and conflicts on rwb-docs-legal to WriteOnceViolationException, timeouts to StorageUnavailableException; writes the audit event for a refused overwrite or delete |
| ContentHashGuard | Service | BR7: compares the SHA-256 of an existing write-once blob before a write |

**Database**

- No table or column. storage_ref values follow {container}/{caseId}/{documentId}/v{docVersion}, within varchar(400).

**Configuration and reference data**

- Properties per environment: rwb.dochub.storage.account-url, rwb.dochub.container.intake, rwb.dochub.container.standard, rwb.dochub.container.legal, rwb.dochub.container.quarantine, rwb.dochub.storage.timeout-seconds 10.
- Template parameters: legalRetentionDays 3650 (assumed; DL26), legalPolicyLocked true in PROD only, softDeleteDays 30 (assumed; DL27).

**Build steps**

1. Write the infrastructure template with the account settings, the four containers, the policies and the role assignments; apply it in DEV and SIT.
2. Build DocumentContainersConfig with managed identity credentials only; test that key-based clients are refused.
3. Build StorageErrorMapper with the audit event; test AC1 and AC2 against SIT.
4. Build ContentHashGuard; test AC12.
5. Build StorageReadinessIndicator and wire it into the ACE health endpoint; test AC9 in DEV.
6. Run the SIT tests of section 16, including the role listing of AC5, and hand the assignment list to the security administrator.

**Feature flag:** `rwb.dochub.storage-containers`. Off: the readiness check reports not ready and every document write is refused with 503 rather than written outside the write-once container.

**Done when:** the tests in section 16 pass in SIT, the template is applied in DEV and SIT, and the security administrator has reviewed the role assignments.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-002 | Overwrite or delete of a write-once document | Legal documents cannot be changed. Add a new version instead. |
| MSG-GEN-006 | Storage unavailable or document hub not ready | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | Role without Documents C | You cannot {action} here. Your role does not include it. |

Thai text for each message follows decision DL10.

## 15. Screens and states

No screen in this story. The platform administrator sees the document hub readiness on SCR-44 Interface and job monitor. The case owner uploads on SCR-30 Case documents (RWB-E1-026).

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-012-01 | AC1, BR1 | System | Synthetic court notice in rwb-docs-legal |
| TC-TE-012-02 | AC2, BR1 | System | Delete attempt on the same blob |
| TC-TE-012-03 | AC3, BR2 | System | v2 blob for the same document |
| TC-TE-012-04 | AC4, BR6 | System | Overwrite and delete in rwb-docs in SIT |
| TC-TE-012-05 | AC5, BR4 | System | Role assignment listing in SIT |
| TC-TE-012-06 | AC6, BR3 | System | Client with account key and with a shared access signature |
| TC-TE-012-07 | AC7, BR4 | System | Managed identity RWB-SIT-SY-AGENT |
| TC-TE-012-08 | AC8, BR3 | System | Client outside the private endpoint |
| TC-TE-012-09 | AC9, BR5 | System | Policy removed in DEV |
| TC-TE-012-10 | AC10 | System | Storage stub with a 10-second timeout |
| TC-TE-012-11 | AC11, BR4 | System | File in rwb-quarantine |
| TC-TE-012-12 | AC12, BR7 | System | Same and different content to an existing write-once name |
| TC-TE-012-13 | Access | Access | RW-REFADM user (Documents -) calls POST /cases/{caseId}/documents; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the retention period, soft delete days and container names come from template parameters and properties.
- No personal data in logs, tests or prompts: blob names carry case and document IDs only, never a customer name or ID number; test files are synthetic.
- No read of another module's tables.
- No account key, connection string or shared access signature in code, configuration or the pipeline.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-003 | Legal document types held in a write-once container that cannot be altered or deleted | Business Requirements Program, section 5.5 | FEAT-DCM-01 | 13 Manage documents and correspondence | R-UNI-40 | TC-TE-012-01 to TC-TE-012-03, TC-TE-012-09, TC-TE-012-12 |
| REQ-DCM-002 | The document hub is the system of record; no other store holds the authoritative copy | Business Requirements Program, section 5.5 | FEAT-DCM-19 | 13 Manage documents and correspondence | None | TC-TE-012-04 to TC-TE-012-08, TC-TE-012-10, TC-TE-012-11, TC-TE-012-13 |

## 19. Out of scope

- Choosing the container per document type and writing the document row (RWB-E1-024).
- Retention classes, archive and the retention job (RWB-E1-041, JOB-17).
- Legal hold on a case or a document (REQ-DCM-016; DL27).
- Backup and restore test of the document store (REQ-DCM-015; DL27).
- Sizing and cost of the storage (REQ-DCM-014; NFR-069).
