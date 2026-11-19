# TB0001-1246 [RWB-TE-012] Document storage containers

| Field | Value |
|---|---|
| Jira | [TB0001-1246](https://scbjira.atlassian.net/browse/TB0001-1246) |
| Type | Story |
| Status | Hold |
| Resolution | - |
| Parent | TB0001-1234 |
| Epic link | TB0001-1234 |
| Assignee | PONGCHAI CHAROENRUNGRODKUN |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | Block, R-Decision, R-Dependency |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Design - Grooming |
| Team | RWB_SQ1 |
| Created | 2026-11-05T16:11:19.072+0700 |
| Updated | 2026-11-18T08:56:23.559+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 4 |
| Comments | 4 |

## Description

As a platform administrator, I want blob containers for documents, with a write-once container for legal types, reached by managed identity, so that legal documents cannot be overwritten.

## Acceptance criteria

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

## Attachments

- [image-20261118-015602.png](../../Attachments/TB0001-1246/image-20261118-015602.png) (19992 bytes, Pe Chichareon, 2026-11-18T08:56:23.347+0700)

## Comments (4)

### Comment 1: Pe Chichareon, 2026-11-16T13:33:35.684+0700, edited 2026-11-16T14:03:20.729+0700

Comment ID 1792401

Next action: 

   Henka connect with SCB Infra first to see which item can be configured by SCB Infra Blob storage

A1 - pending Blob path structure define from Henka.   

   → *Package.* folder {{recovery/dochub/storage}}

A2 - Henka should discuss with SCB infra team to config the allow managed identity

       Note: use case of blob storage is the user upload file through the application Recovery Workbench

A3 - should handle by Blob storage configuration

A4 - ContentHashGuard? TBC whether should be applied at Application Level or Blob storage?

A5 / AC9 should be include in story that require to upload file to blob storage

### Comment 2: Chitchaya Muanchonchana, 2026-11-16T14:01:08.794+0700, edited 2026-11-16T17:30:02.545+0700

Comment ID 1792487

Question in Grooming session @CHANISSARA MAHAKITTIKUN 

# SCBTechX might not take care this story , Henka will talk to SCB team and assign to SCB.
# A4 ContentHahGuard, Is applied at a Blob level , or hash in DB (application)? if Blob level , it should be SCB infrastructure team.

### Comment 3: CHANISSARA MAHAKITTIKUN, 2026-11-17T12:14:35.066+0700

Comment ID 1794345

@PONGCHAI CHAROENRUNGRODKUN This user story is about Infrastructure. It builds and secures the Azure Blob Storage foundation used by the Document Hub to store actual Recovery document. Please clarify who will be responsible for this user story?

### Comment 4: Pe Chichareon, 2026-11-18T08:56:23.559+0700

Comment ID 1795773

Regarding Azure Blob storage, refer K. Pratchya suggestion below

Utilizing the current ACE blob storage

!image-20261118-015602.png|width=737,alt="image-20261118-015602.png"!


## Other Jira fields

| Field | ID | Value |
|---|---|---|
| App Owner | customfield_10188 | - |
| App Owner (migrated 3) | customfield_11031 | - |
| Approver2 | customfield_11586 | Nuttakorn Leeviravanich |
| AR: Atlassian-TemplateO | customfield_11656 | emaile,role |
| AR: Atlassian_Template | customfield_11654 | \|\|Full Name \|\| Email \|\| Role \|\| Company \|\| \|{Full Name}\|{Email}\|{Role}\|{Company}\| \|\|\|\| |
| BI Status | customfield_10169 | To be Confirmed |
| Build % | customfield_12531 | 0% |
| Bulk Backlog Detail Uploaded | customfield_11628 | No |
| CCB Status | customfield_10228 | New |
| Created Date | customfield_10249 | 2026-11-05 |
| Customer Impact | customfield_10246 | No |
| CX Status | customfield_10217 | To be Confirmed |
| Defect Re-Opened? | customfield_10619 | No |
| Defect Re-Opened? (Checkbox) | customfield_10174 | No |
| Demand type | customfield_10244 | Project |
| Demand types(Migrated on 29 Mar 2024) | customfield_11926 | Incident |
| Deploy Status | customfield_10170 | Initial |
| DGO Approval | customfield_10113 | Pending |
| DPO Approval | customfield_10122 | Pending |
| Epic Type | customfield_10275 | Project |
| Epic Type OLD | customfield_10052 | Project |
| Execution Method | customfield_10240 | Manual |
| Grooming Status | customfield_10212 | Not Started |
| Grooming Status (migrated) | customfield_10649 | Not Started |
| Has been Approved | customfield_10232 | No |
| Independent Story | customfield_10101 | No |
| Is Required Downtime | customfield_10245 | N |
| Is Required Downtime | customfield_11847 | N |
| Issue Priority | customfield_10102 | Medium |
| IT Risk Approval | customfield_10133 | Pending |
| Logs / Description | customfield_11491 | Log: xxxx URL: xxxx |
| Penetration Test Status | customfield_10183 | Not Started |
| Penetration Test Status (migrated) | customfield_10654 | Not Started |
| Priority | customfield_10610 | Medium |
| QbD Status OLD | customfield_10050 | Not Required |
| Regulatory Related | customfield_10260 | No |
| Regulatory Status | customfield_10201 | No Issues |
| Regulatory Status (migrated) | customfield_10647 | No Issues |
| Release Confirmation | customfield_10637 | Not Confirmed Internal |
| Release Confirmation (API) | customfield_10200 | Not Confirmed Internal |
| Requirement Status | customfield_10207 | Not Completed |
| Root Cause | customfield_12535 | Unknown |
| SAT Process | customfield_10274 | PENDING |
| SAT Status(Migrated) | customfield_12360 | Not Start |
| SD Required | customfield_10257 | no |
| Segment | customfield_10193 | Retail |
| Severity | customfield_10168 | 3 - Medium |
| Severity (migrated) | customfield_10597 | 3 - Medium |
| SIT retest failure tracking | customfield_15014 | 0.0 |
| SIT Shakedown Status | customfield_10189 | Not Started |
| Solution Remark (Nonstd) | customfield_10216 | To be Confirmed |
| Solution Status | customfield_10640 | To be Confirmed |
| Squad Estimation Status | customfield_10229 | Estimation In Progress |
| Target Fix Date Adjustment Flag | customfield_15017 | No |
| Test Cases Review | customfield_10150 | In-progress |
| Testing environment | customfield_15163 | Non-Aging |
| Toggle Flag | customfield_11588 | No Toggle Flag |
| Training Material Status | customfield_10176 | Not Started |
| UAT Estimation Status | customfield_10234 | Estimation In Progress |
| UAT Execution By | customfield_13554 | UAT Team |
| UAT Execution By | customfield_10237 | Squad Team |
| UAT Owner | customfield_10184 | KANRUTHAI ASAVAROONGPAISAL |
| UAT retest failure tracking | customfield_15015 | 0.0 |
| UAT Shakedown Status | customfield_10194 | Not Started |
