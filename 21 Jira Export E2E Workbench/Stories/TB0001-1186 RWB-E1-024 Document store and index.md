# TB0001-1186 [RWB-E1-024] Document store and index

| Field | Value |
|---|---|
| Jira | [TB0001-1186](https://scbjira.atlassian.net/browse/TB0001-1186) |
| Type | Story |
| Status | In Design - Solution |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | CHANISSARA MAHAKITTIKUN |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | DEV-Reviewed, QA-Reviewed, R-Dependency, R-Spec |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Design - Grooming |
| Team | RWB_SQ1 |
| Created | 2026-11-05T12:37:24.833+0700 |
| Updated | 2026-11-18T17:48:44.713+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 6 |
| Comments | 12 |

## Description

As a litigation officer (RW-LITOFF), I want every document stored against its case with its type, date, source and extracted fields, legal types held in a write-once container, and every version kept, so that I find a document by case ID, type and date, and a legal document cannot be changed after it is stored.

## Acceptance criteria

```gherkin
Feature: Document store and index

  Background:
    Given document type table version "DOCTYPE-2026.11" is in force
    Given type "COURT_NOTICE" has write_once true and retention class "LEGAL10Y"
    Given type "APPRAISAL_REPORT" has write_once false and retention class "GENERAL05Y"
    Given parameter INTAKE_MAX_FILE_MB is 25 and INTAKE_ALLOWED_TYPES is "PDF,JPG,PNG"
    Given case "RW-2026-000123" exists with product group "MORTGAGE" in team "MTG-BKK-LIT"

  Scenario: AC1 Stored against case
    Given a scanned court notice "notice-0001.pdf" of 1.2 MB for case "RW-2026-000123" with source "SCAN"
    When it is stored
    Then one document row exists with case "RW-2026-000123", type "COURT_NOTICE", source "SCAN", doc_version 1 and the stored date of today
    Then its extracted field "black_case_no" with value "BC-TEST-0456" is in the index
    Then the file is in container "rwb-docs-legal" at "rwb-docs-legal/{caseId}/{documentId}/v1"
    Then the system writes documentStored to the outbox with the document ID, the case ID, the type and the source
    Then the litigation officer opens it from the case documents screen and GET content returns the same SHA-256 hash

  Scenario: AC2 Write once
    Given the court notice from AC1 is stored with write_once true
    When a delete and a content replace are attempted through the document store and directly on the container
    Then the system refuses each attempt with MSG-P5-002
    Then the file hash and the document row are unchanged
    Then the system writes an audit event "DOCUMENT_CHANGE_REFUSED" for each attempt with the document ID and the caller

  Scenario: AC3 Retention class
    Given a document of type "APPRAISAL_REPORT" for case "RW-2026-000123"
    When it is stored
    Then the document row carries retention class "GENERAL05Y" from type table version "DOCTYPE-2026.11"
    Then write_once is false and the file is in container "rwb-docs"

  Scenario: AC4 A new version keeps the history
    Given the appraisal report from AC3 at doc_version 1
    When a user with Documents U adds a new file with reason "Revised valuation"
    Then a document row with doc_version 2 and previous_version_id of version 1 exists and is active
    Then version 1 is inactive and its content is still returned by GET content
    Then GET for version 2 lists versions 1 and 2 with their stored dates and sources

  Scenario: AC5 Unknown document type is refused
    Given a file for case "RW-2026-000123" with type "BANK_STATEMENT"
    When it is stored
    Then the system refuses the call with 422 and MSG-P5-006
    Then no document row, decision log entry or event is written

  Scenario: AC6 File type not allowed
    Given a file "macro-0001.docx" with Word content for case "RW-2026-000123"
    When it is stored
    Then the system refuses the call with 415 and MSG-P5-001
    Then the system writes nothing to the containers or the tables

  Scenario: AC7 Size limit boundary
    Given two PDF files for case "RW-2026-000123" of 26,214,400 bytes and 26,214,401 bytes
    When each is stored
    Then the system stores the file of 26,214,400 bytes
    Then the system refuses the file of 26,214,401 bytes with 413 and MSG-P5-017 showing 25 MB

  Scenario: AC8 The same file stored twice
    Given the court notice from AC1 is stored on case "RW-2026-000123"
    When the same file with the same hash and type is stored again on that case
    Then the system returns the existing document ID
    Then the case still holds one court notice row, one decision log entry and one DocumentStored event for it

  Scenario: AC9 Two versions added at the same time
    Given the appraisal report at doc_version 2
    When two users add a new version at the same time
    Then one request returns 200 with doc_version 3
    Then the other returns 409 with MSG-GEN-004
    Then exactly one row with doc_version 3 exists

  Scenario: AC10 Version on a superseded document
    Given the appraisal report version 1 is inactive
    When a user adds a new version to version 1
    Then the system refuses the request with 409 and MSG-P5-025
    Then the system writes no new row

  Scenario: AC11 The storage copy fails
    Given container "rwb-docs" refuses writes
    When an appraisal report is stored for case "RW-2026-000123"
    Then the system writes the document row with state "COPY_PENDING"
    Then GET content returns 503 with MSG-GEN-006 naming "Document storage"
    Then when the container accepts writes again the next document intake run copies the file and sets state "STORED"

  Scenario: AC12 Case outside the reader's scope
    Given a phone collector with scope OWN who does not own case "RW-2026-000123"
    When the phone collector requests the court notice from AC1
    Then the system refuses the request with 403 and MSG-P4-003
    Then no metadata or content is returned
```

## Attachments

- [image-20261117-025516.png](../../Attachments/TB0001-1186/image-20261117-025516.png) (122124 bytes, Nuttapon Jittachotisak, 2026-11-17T10:01:13.599+0700)
- [image-20261117-031756.png](../../Attachments/TB0001-1186/image-20261117-031756.png) (117504 bytes, Nuttapon Jittachotisak, 2026-11-17T10:42:28.243+0700)
- [image-20261117-032016.png](../../Attachments/TB0001-1186/image-20261117-032016.png) (152989 bytes, Nuttapon Jittachotisak, 2026-11-17T10:42:28.424+0700)
- [image-20261117-034906.png](../../Attachments/TB0001-1186/image-20261117-034906.png) (205757 bytes, Nuttapon Jittachotisak, 2026-11-17T10:49:10.654+0700)
- [image-20261117-035035.png](../../Attachments/TB0001-1186/image-20261117-035035.png) (26116 bytes, Nuttapon Jittachotisak, 2026-11-17T10:51:22.383+0700)

## Comments (12)

### Comment 1: RAPEEPAT CHULAOTRAKUL, 2026-11-17T07:40:42.523+0700, edited 2026-11-17T09:00:46.341+0700

Comment ID 1793654

@CHANISSARA MAHAKITTIKUN 

h3. 
Concerns (Dependencies)

Before this story can be fully worked on/tested, the following prerequisite stories need to be completed first:

* *RWB-E1-001* — Document and document_field table creation in the recovery schema. Without these tables, there is nowhere to store document metadata.
* *RWB-TE-012* — Blob storage containers (rwb-docs, rwb-docs-legal, rwb-quarantine) with managed identity access through DocumentStorage interface. Without the containers and the write-once immutability policy on rwb-docs-legal, the story cannot store files safely.
* *RWB-E1-025* — Document type table (DOCTYPE-2026.11) with write_once and retention_class fields populated for all six types. Without this, there is no way to enforce write-once semantics or retention periods.
* *RWB-E1-018* — CaseDirectory published interface (CaseDirectory.findById) to validate that the case exists before accepting a document. Without this, the duplicate-check logic and case association are not possible.
* *RWB-E1-027* — DecisionLogWriter interface to append a decision log entry (DOCATT, final call STORED) inside the same transaction. Without this, every document store will fail per BR8.



h3. Clarification Needed

# *Delete and Replace Permissions for Non-Write-Once Documents*
Exception path X1 covers “Delete or content replace of a write-once document → refused with MSG-P5-002.”
But there’s no AC or exception path covering the *opposite case*: what should happen when a user tries to delete or replace a *non-write-once* document (e.g., APPRAISAL_REPORT with write_once=false)?
Should:
#* Option A: Delete/replace be *refused* (immutable by policy)?
#* Option B: Delete/replace be *allowed* (since it’s not legally required to be immutable)?
#* Option C: Delete/replace be *deferred to RWB-E1-041* (retention job) and prohibited before retention expires?
# Currently, section 19 (Out of scope) mentions “Retention periods, the retention job and the virus scan (RWB-E1-041)” but doesn’t clarify whether RWB-E1-024 should build delete() / replaceContent() or leave it to a follow-up story.
# *AC1 Stored against case*
#* Please clarify on the {color:#0747a6}*outbox*{color} mentioned in *AC1 Stored against case*. Specifically, how should it be implemented (e.g., a transactional outbox table in the database), and which user story covers its initial setup and publishing mechanism?
#* Is AC1 Required OCR intake (RWB-E1-050, RWB-E1-053, RWB-E1-032) to extract field "black_case_no" from document?
# *AC2 Write once*
#* Is the write-once enforcement at the service level (service.delete() / service.replaceContent() refuse the call), or only at the blob level (immutability policy on rwb-docs-legal)?
#* If a user somehow modifies the blob directly (not through the service), does the service have a way to detect/audit this, or is it assumed the blob immutability policy prevents it entirely?
#* Should there be an AC covering “if someone tries to modify a write-once blob outside the service, audit event DOCUMENT_CHANGE_REFUSED is written” (as shown in X1)?
# *AC4 A new version keeps the history*
#* When reading GET /documents/{documentId}, does the response include all versions, or only the latest? The contract says “versions” in the response, but doesn’t specify the structure.
#* How to get content of previous version document via *GET /api/recovery/v1/documents/{documentId}/content*? No version specific in request.
# *AC8 The same file stored twice*
#* How is “the same file” determined? By SHA-256 hash alone, or by (case_id, document_type, content_sha256) tuple?
#* What if the same file (same hash) is stored on the same case but with a *different* type (e.g., once as COURT_NOTICE, once as DEMAND_LETTER)? Should this be allowed, or refused as a duplicate?
# *AC9 Two versions added at the same time*
#* Is POST /documents/{documentId}/versions use the Idempotency-Key header to prevent duplicate versions? For example:
#** User adds version 2 with Idempotency-Key ‘X’ → succeeds, creates version 2
#** User retries the same request with the same Idempotency-Key ‘X’ → returns the same version 2 (idempotent)?
#* Or if the user adds version 2 with Idempotency-Key ‘X’, then adds a different file with Idempotency-Key ‘Y’, should the system create version 3, or refuse with 409 (concurrent change)?
# *AC10 Version on a superseded document*
#* Does this AC test that you *cannot add a new version to an old/inactive document*?
For example:
#** Document has version 1 (Inactive) → version 2 (Inactive) → version 3 (latest Active)
#** User tries to add a new version to version 1 or version 2
#** System refuses: 409 MSG-P5-025
#* So the only document version that can receive a new version is the *latest one*?” How to test this AC with *POST /documents/{documentId}/versions* to update at a specific document version?
# *AC11 The storage copy fails*
#* Is JOB-12 need to implement in this story or is it out of scope for this story?
#* When a user POSTs a new file (POST /documents), the system should:
#*# *Succeed at the database level* — create the document row and set state = {{COPY_PENDING}}
#*# *Fail at the blob storage level* — the asynchronous copy to rwb-docs or rwb-docs-legal container fails (e.g., network error, quota exceeded, permission denied)
#* After this failure, the expected behavior is:
#** *GET /documents/{documentId}* → 200 OK, returns metadata with state={{COPY_PENDING}} and doc_version=1
#** *GET /documents/{documentId}/content* → 503 (Service Unavailable), MSG-GEN-006 “The document is not available. Your request is queued and will be retried.”
#* The document row persists with metadata visible, but content is unreachable until JOB-12 (the document intake retry job) copies the file successfully on the next run.
Does AC11 verify this behavior?

### Comment 2: Nuttapon Jittachotisak, 2026-11-17T10:01:13.762+0700, edited 2026-11-17T10:56:19.608+0700

Comment ID 1793853

@CHANISSARA MAHAKITTIKUN 

!image-20261117-025516.png|width=1027,alt="image-20261117-025516.png"!

# rwb-docs-legal/rwb-docs is blob storage path right? for example this path would be {path-to-rwb-storage}/rwb-docs-legal/{caseId}/{documentid}/v1 if write_once is true right?
# {{JOB-12}} Is scheduled job run in schedule. If store fail where to get the file to retry when schedule run.

!image-20261117-031756.png|width=732,alt="image-20261117-031756.png"!

# Is UI implemented in scope?

!image-20261117-032016.png|width=732,alt="image-20261117-032016.png"!

# *POST /documents/{documentId}/versions* Is this api for upload new version of file? So what is documentId should be as I understand it was id generated for {{document}} table so this mean we use previous id to refer? what if It first one uploaded.

!image-20261117-034906.png|width=732,alt="image-20261117-034906.png"!

# This story mention about extract field. Do you have specific mapping for an extraction? or just get header and row.

!image-20261117-035035.png|width=732,alt="image-20261117-035035.png"!

### Comment 3: Chanapai Gingpuwaluck, 2026-11-17T10:57:19.891+0700

Comment ID 1794063

These points add to the dependency, version and JOB-12 questions already on this card.

# *No scan before write-once.* The virus scan is in RWB-E1-041, outside this story. An infected or misfiled file that reaches {{rwb-docs-legal}} cannot be deleted for 10 years.
#* Proposal: scan, then classify, then confirm, then commit to write-once. Alternatively, hold legal-type files in a non-locked container until checked.
# *No access log table.* BR9 requires an access log entry when a document is opened, but Physical Schema v6 has no access log table (feedback #49). The same gap affects RWB-E1-033 and RWB-E1-068.
#* Question: where is the access log, and who owns it (recovery schema or ACE logging)?
# *403 or 404.* An out-of-scope read returns 403 (MSG-P4-003) here, but 404 in RWB-E1-066 and RWB-E1-068. Please choose one status for the whole module.
# *Tables after D-RCV-35.* Please confirm that the {{document}} and {{document_field}} tables are still in Physical Schema v6, since RWB-E1-001 changed under D-RCV-35.

Who answers: Security architect, Document SME, Solution architect.

### Comment 4: Chitchaya Muanchonchana, 2026-11-18T10:24:02.808+0700, edited 2026-11-18T11:09:09.330+0700

Comment ID 1796024

@CHANISSARA MAHAKITTIKUN 

1. Remove AC9 as not possible to happen. S*ame time condition* is possible to test.

# condition for AC is V1 is inaction and V2 is active.
Scenario: AC10 Version on a superseded document
Given the appraisal report version 1 is inactive
When a user adds a new version to version 1
Then the system refuses the request with 409 and MSG-P5-025
Then the system writes no new row

### Comment 5: Chanapai Gingpuwaluck, 2026-11-18T10:28:30.406+0700, edited 2026-11-18T10:53:11.214+0700

Comment ID 1796046

Dependency check for RWB-E1-024 against the Jira sprints (18 Nov 2026). E1-024 is in "Design - Pre-analyze".

*1. On "implement after E1-006 and OCR ticket":*

* RWB-E1-006 (Data quality rules) was removed by D-RCV-35. Did you mean RWB-TE-006 (outbox), which E1-024 needs for the DocumentStored event in AC1?
* The OCR ticket (RWB-E1-049) depends on E1-024: it starts from the DocumentStored event and reads the stored file. If E1-024 waits for OCR, the two wait on each other. Please confirm the order: E1-024 first, then E1-049.

*2. Declared dependencies – none is ready in Q4S2:*

* RWB-E1-001 (document tables): Delivery Q4S2 Squad1, waiting on RWB-E1-043 (Hold).
* RWB-TE-012 (blob containers): Design - Grooming, Hold, may move to SCB Infra.
* RWB-E1-025 (DOCTYPE): Design - Grooming, waiting on v2 and DL19.
* RWB-E1-018 (CaseDirectory) and RWB-E1-027 (DecisionLogWriter): no sprint.

*3. Used but not in "Depends on" (please add):*

* RWB-TE-006 outbox (AC1): no sprint.
* RWB-E1-019 / E1-022 / E1-037 roles and permissions, and RWB-E1-016 scope (AC12, 403/404): no sprint.
* RWB-E1-042 / E1-043 intake parameters: Q4S2 Squad2, Hold.
* JOB-12 retry for COPY_PENDING (X8, AC11): built in RWB-E1-049 / E1-057.
* ACE PII access log (DEP-04, overdue since 9 Nov).

*4. Decision needed:* (a) pull E1-018, E1-027 and TE-006 into Q4S2, or (b) build E1-024 against stubs and move AC1 (decision log and outbox), AC11 and AC12 to a later integration test. Which one?

### Comment 6: VAISHNAVI KAULGE, 2026-11-18T14:38:40.884+0700

Comment ID 1796765

@RAPEEPAT CHULAOTRAKUL 

h2. Dependencies

*From the story.* The five stories you list are already in the story's "Depends on" and Preconditions, and each is needed for the reason you give. Two more are missing from the list:

* *RWB-TE-006 (outbox).* It is needed for the {{DocumentStored}} event in AC1.
* *RWB-E1-049 (document intake).* It creates JOB-12, which AC11 relies on.

*Needs decision:* please add both to the story's "Depends on". Also, TE-006 depends on E1-027, and E1-027's preconditions mention the outbox, so the team should confirm the build order.

----

h2. Delete and replace for documents that are not write-once

*Needs decision.* The story doesn't say what should happen.

* This story builds the {{delete()}} and {{replaceContent()}} methods and makes them refuse write-once documents (build step 7).
* Option C doesn't apply as written. The retention job (JOB-17, RWB-E1-041) never deletes a document or a blob (E1-041 rule BR5).
* The story's guardrail says the service never overwrites a blob. Every version is a new blob.
* *Proposed answer: Option A for this story.* Delete and replace are refused for every document, and a change is a new version. If the bank needs real deletion later, it goes in a separate story with its own role and rules. The Product Owner should confirm, and then an exception path and an AC should be added.

----

h2. AC1: Stored against case

*Outbox: how is it built, and which story covers it?*

* *From the story.* It is a transactional outbox table in the database.
* The {{document}} row, the decision log entry and the outbox event are written in one transaction. All commit or none do.
* RWB-TE-006 builds the outbox: the tables, {{OutboxWriter.publish}} and the sender job (JOB-11).
* RWB-E1-024 only calls it, to write the event {{DocumentStored}}.
* AC1 only checks that the event row exists. It does not check delivery.

*Is OCR intake required to extract* {{black_case_no}}*?*

* *From the story.* No.
* The caller passes the extracted fields with the store request. This story does not extract anything.
* The OCR stories (E1-050, E1-053 and E1-032) are out of scope (section 19).
* For the AC1 test, send {{black_case_no = BC-TEST-0456}} as input and check it is in the index.

----

h2. AC2: Write once

*Is the rule enforced in the service or in the blob storage?*

* *From the story.* Both layers enforce it.
* *Service:* {{delete()}} and {{replaceContent()}} throw {{WriteOnceViolationException}} when the type is write-once. This maps to MSG-P5-002.
* *Storage:* {{rwb-docs-legal}} has an immutability policy of 3,650 days (RWB-TE-012). Storage refuses overwrite or delete even from a direct call.

*If someone changes the blob directly, can the service detect it?*

* *From the story, partly.*
* Direct access is blocked in layers: shared keys are off, only named identities have roles, and only the private endpoint is allowed.
* An attempt through the app's storage adapter is refused by storage. {{StorageErrorMapper}} converts it and writes the audit event to the ACE audit log.
* A client that bypasses the app never reaches the app, so no app code can record it.
* *Needs decision:* confirm with the platform team whether Azure storage diagnostic logs capture those attempts.

*Should there be an AC for "audit event when someone modifies the blob outside the service"?*

* *Needs decision.* AC2 already says "directly on the container" and "an audit event for each attempt".
* *Proposed:* split AC2 into two. 2a covers attempts through the service, with the audit event. 2b covers attempts on the container, refused by storage. State clearly which of these the app can audit.

----

h2. AC4: A new version keeps the history

*Does GET return all versions or only the latest?*

* *From the story.* It returns all versions. AC4 says the list shows versions 1 and 2 with their stored dates and sources.
* *Needs decision:* the structure isn't written in the contract. *Proposed:* one entry per version with the row ID, {{docVersion}}, {{isActive}}, {{storedAt}}, {{source}} and {{previousVersionId}}.

*How do I get the content of an older version?*

* *From the story.* Each version is its own {{document}} row with its own ID. {{previous_version_id}} points to the row it replaces.
* Call {{GET /documents/{thatVersionId}/content}} with the older version's ID, taken from the versions list.
* No version parameter is needed. The contract says it returns "the file of that version".

----

h2. AC8: The same file stored twice

*How is "same file" decided?*

* *From the story.* By the tuple *case + document type + SHA-256 hash*, among active documents only.
* The hash alone is not enough. This is flow step 5, rule BR6 and the unique index {{uk_document_case_type_hash}}.

*Same hash, same case, different type?*

* *From the story.* It is allowed. The key includes the type, so it is stored as a second document. It is not refused as a duplicate.

----

h2. AC9: Two versions added at the same time

*Does the Idempotency-Key prevent duplicate versions?*

* *From the story.* Yes, for retries. The same key sent again returns the first result and creates nothing new.

*Key X, then a different file with key Y: version 3 or 409?*

* *From the story.* It depends on where Y is sent and when.

||Request Y||Result||
|Sent to the latest version after X has finished|200, creates version 3|
|Sent to an older, inactive version|409 MSG-P5-025|
|Sent at the same moment as another request, both on the latest|One wins; the other gets 409 MSG-GEN-004|

The key covers retries by the same user. The 409 conflict comes from the state of the record (the optimistic lock), not from the key.

----

h2. AC10: Version on a superseded document

*Is the only document that can take a new version the latest one?*

* *From the story.* Yes.
* With v1 (inactive), v2 (inactive) and v3 (active), a new version on v1 or v2 returns 409 with MSG-P5-025 and writes no row.
* A new version on v3 succeeds and creates v4.

*How to test it:*

# Build the chain v1 to v3.
# Get each version's row ID from {{GET /documents/{id}}}.
# {{POST /documents/{v1 row ID}/versions}} returns 409 MSG-P5-025. Repeat for v2.
# {{POST /documents/{v3 row ID}/versions}} returns 200.

----

h2. AC11: The storage copy fails

*Is JOB-12 built in this story?*

* *From the story.* No. RWB-E1-049 creates JOB-12.
* This story builds only {{CopyPendingStep}}, the step that retries copies for {{COPY_PENDING}} rows (build step 5).
* If E1-049 isn't ready, test the step by calling it directly.

*Your description of the behavior* It is right in outline, with two corrections:

* The upload endpoint is {{POST /cases/{caseId}/documents}} (RWB-E1-026). E1-024 itself exposes the Java method {{DocumentStore.store}}, not a {{POST /documents}}.
* The message text is "{system} is not available. Your request is queued and will be retried." With {{{system}}} = "Document storage", it reads "Document storage is not available...".

*Does AC11 verify the metadata read?*

* *From the story.* No. AC11 checks three things: the row is {{COPY_PENDING}}, {{GET content}} returns 503 with MSG-GEN-006, and after the container recovers the next run copies the file and sets {{STORED}}.
* *Needs decision:* the "metadata visible" part isn't written. *Proposed:* add a line to AC11 saying {{GET /documents/{id}}} returns 200 with state {{COPY_PENDING}} and {{doc_version}} 1. The GET contract also lists 503, so one of them should be corrected.

### Comment 7: VAISHNAVI KAULGE, 2026-11-18T14:44:57.671+0700

Comment ID 1796799

@Nuttapon Jittachotisak 


h2. 1. Is the path a blob storage path?

*From the story.* Yes, your reading is right.

* {{rwb-docs-legal}} and {{rwb-docs}} are *containers* in the environment's Azure storage account (one account per environment, reached through a private endpoint, RWB-TE-012).
* The part after the container name is the *blob name*: {{{caseId}/{documentId}/v1}}.
* So the full location is {{{storage account}/rwb-docs-legal/{caseId}/{documentId}/v1}} when {{write_once}} is true, and {{{storage account}/rwb-docs/{caseId}/{documentId}/v1}} when it is false.
* Container names are properties per environment, not hard-coded.
* The container comes from the type table ({{write_once}}), never from the caller.

----

h2. 2. JOB-12 is scheduled. Where does it get the file to retry?

*From the story, partly.* The source is the *intake container (*{{rwb-intake}}*)*.

* {{DocumentStore.store}} is called with "the file in the intake container" and its blob reference (flow step 1).
* The retry copies from that intake blob to {{rwb-docs}} or {{rwb-docs-legal}}, then sets {{storage_ref}} and the state {{STORED}}.

*Needs decision.* The story doesn't say two things:

* *Where the intake blob reference is kept* while the row is {{COPY_PENDING}}. The retry step must be able to find it. A column on {{document}}, or a field in the intake record, would do.
* *How long the intake file is kept.* If an intake clean-up runs before JOB-12 retries, the file is gone and the copy can never finish.

*Proposed:* keep the intake blob until the state is {{STORED}}, and store its reference on the row. Please confirm with the RWB-E1-049 owner, because JOB-12 and the intake container rules belong there. The schedule for JOB-12 isn't in this story either.

----

h2. 3. Is the UI in scope?

*From the story.* Only a small part.

*In scope:* the {{DocumentDetailPanel}}, a React component opened from a row on SCR-30 (build step 9, section 15). It shows:

* metadata and extracted fields
* the list of versions
* a download button
* the "Write once" label, with no edit control on write-once documents
* the error state with the message ID when a read is refused

*Out of scope:* SCR-30 itself, the upload form, the document list and search. They belong to RWB-E1-026.

----

h2. 4. What is {{documentId}} in {{POST /documents/{documentId}/versions}}?

*From the story.* Yes, this endpoint uploads a new file as a new version. You are reading {{documentId}} correctly: it is the {{id}} of a row in the {{document}} table.

* It must be the id of the *latest (active) version*. Any older version returns 409 with MSG-P5-025 (AC10).
* The response returns the *new row*, with its own new id and {{doc_version}} n+1. Use that new id for the next version.
* *The first upload doesn't use this endpoint.* It goes through the store ({{POST /cases/{caseId}/documents}} in RWB-E1-026, which calls {{DocumentStore.store}}). That creates version 1 and its id.

Sequence: store → v1 (id A) → POST versions on A → v2 (id B) → POST versions on B → v3 (id C).

*Needs decision.* The blob name format {{{caseId}/{documentId}/v{n}}} doesn't say whether version 2's blob uses id A or id B. Either works if {{storage_ref}} records it. Confirm, so that tests check the right path.

----

h2. 5. Extraction: is there a specific mapping, or just header and row?

*From the story.* This story does no extraction and has no mapping.

* The caller passes the fields in the store request as name/value pairs. Each pair becomes one row in {{document_field}}.
* {{document_field}} columns: {{field_name}}, {{field_value}}, {{confidence}}, {{extracted_value}}, {{extractor_version}}, {{state}}, {{confirmed_by}}.
* The *list of fields per type* comes from the type table, in {{field_definitions}} (RWB-E1-025). For example, COURT_NOTICE has {{court_name}}, {{black_case_no}}, {{notice_date}} and {{hearing_date}}. In total there are six types and 26 fields.
* How OCR output is mapped to those field names belongs to the OCR stories (RWB-E1-050 and RWB-E1-053).

### Comment 8: VAISHNAVI KAULGE, 2026-11-18T14:47:33.584+0700

Comment ID 1796808

@Chanapai Gingpuwaluck 


h2. 1. No scan before write-once

*From the story, partly.* The scan does happen before the write-once step, but E1-024 itself doesn't enforce it.

* *Upload path (RWB-E1-041, flow step 4):* the upload calls {{MalwareScanService.scanNow}} *before* {{DocumentStore.store}}.
** An infected file returns 422 with MSG-P5-016.
** If the scanner doesn't answer, the upload returns 503 and nothing is kept.
* *OCR intake path (E1-041, flow steps 1 to 3):* JOB-12 runs {{scanStep}} before {{ocrStep}}. An infected file goes to the quarantine container ({{rwb-quarantine}}) and is never stored.
* *Holding area:* the file sits in the unlocked intake container ({{rwb-intake}}) until the document row is committed. Only then is it copied to {{rwb-docs-legal}} (flow step 7). So the "hold in a non-locked container until checked" alternative is already how the flow works.
* *Misfiled files:* on the OCR path, the match step stores a document or holds it for a person (RWB-E1-032). Low-confidence classification goes to review. On the upload path, the case owner picks the type from the list, and there is no confirm step.

*Needs decision (Security architect):*

* {{DocumentStore.store}} doesn't check a scan result. It trusts the callers, and E1-024 doesn't list E1-041 as a dependency. A direct call to {{store}}, for example in a test, skips the scan.
* *Proposed:* {{store}} refuses a file unless the scan result is CLEAN, and E1-041 is added to "Depends on".
* For misfiled types, the Document SME should decide between two options. One is to accept the rule as designed, since the lock is a legal requirement (CTL-12), and add a confirmation on the upload screen for write-once types, such as "This will be locked for 10 years". The other is a staging step before the lock.

----

h2. 2. No access log table

*From the story.* The access log isn't meant to be in the recovery schema.

* E1-024's guardrail says the PII access log entry for each read is written by the *ACE common module*, never by this package.
* E1-033 says the same: "The ACE common module writes access events to the PII access log and confirms each write."
* Physical Schema v6 has no access log table, which matches this. The table sits on the ACE side.

*Answer to "who owns it":* ACE logging owns it, not the recovery schema. E1-024, E1-033 and E1-068 only call the ACE common module.

*Needs decision (Solution architect):* I can't see the ACE code from this workspace. Please confirm the table name and that the ACE module is in place before these stories are tested. Also confirm what happens when a log write isn't confirmed. E1-033 returns 503 and no results (MSG-P5-019), while E1-024 doesn't say.

----

h2. 3. 403 or 404 for an out-of-scope read

*From the story.* The stories disagree, as you say.

||Story||Out-of-scope case||Status||Message||
|E1-024 (AC12)|Out of scope|403|MSG-P4-003|
|E1-066|Missing or out of scope|404|MSG-P4-003|
|E1-068|Missing or out of scope|404|MSG-P4-003|

*Needs decision (Security architect):* choose one status for the whole module.

* *404* doesn't reveal that the case or document exists, so it is safer for personal data. E1-066 and E1-068 already use it, and it merges "missing" and "out of scope".
* *403* tells the user honestly why they are refused, and E1-024's message "This case is not in your scope" fits it.
* *Proposed:* 404 with MSG-P4-003 for any case or document outside the caller's scope. Keep 403 with MSG-P4-002 for a role that lacks the right. If chosen, E1-024 AC12, X9 and the contract change from 403 to 404.

----

h2. 4. Are {{document}} and {{document_field}} still in Physical Schema v6?

*From the schema, yes.* Physical Schema v6 contains both tables, {{document}} and {{document_field}}, with the columns E1-024 uses, including {{doc_version}} and {{previous_version_id}}.

* Documents and extracted fields are data product DP10, sourced from the *Recovery Workbench document hub*. They are Workbench-owned data, not ACE source data.
* D-RCV-35 concerns source data that ACE owns (read through {{recovery.v_ace_*}} views) and the extension tables. On the evidence I have, it doesn't move the document tables.
* E1-024's migration adds columns to {{document}} and creates {{document_hub_parameter}}, so it needs {{document}} to exist from E1-001.

### Comment 9: VAISHNAVI KAULGE, 2026-11-18T14:59:09.148+0700

Comment ID 1796854

@Chitchaya Muanchonchana 
*AC9 should stay. Removing it, or combining it with the duplicate scenario (AC8), leaves gaps.*

*Why the simultaneous case is real and testable*

* Two requests can both read version 2 as the latest before either commits, and both then try to create version 3. Without the lock, two version 3 rows would break the history.
* A test can force the overlap. Pause the first request just before its commit, run the second, then release the first. Or release two parallel requests together and repeat many times. Both are automated integration tests.
* A request that arrives _after_ the first one commits gets AC10's result (409 MSG-P5-025). Only an overlapping request gets AC9's result (409 MSG-GEN-004).

*Why AC9 can't be combined with AC8*

|| ||AC8 duplicate||AC9 two versions||
|Operation|Store a new document|Add a version to an existing document|
|What protects it|Same case, type and hash check, plus the unique index|The optimistic lock on the document row|
|Result|Returns the existing document, no error|409 with MSG-GEN-004|

*Gap in AC8:* it only covers the same file stored one after the other. Two identical stores at the same moment hit the unique index, and the story doesn't say what the second caller receives. This needs its own scenario or an extra line in AC8.

*What is lost if AC9 is removed*

* Exception path X6 and MSG-GEN-004 have no AC.
* The traceability link from REQ-DCM-003 to TC-E1-024-09 breaks.
* The lock code in build step 6 is built but never tested.

*Proposed AC9*

{noformat}Scenario: AC9 Two versions added before either finishes
  Given the appraisal report has version 1 inactive and version 2 active
  When two users submit a new version of version 2 and both requests are in progress together
  Then one request returns 200 with doc_version 3
  Then the other returns 409 with MSG-GEN-004
  Then exactly one row with doc_version 3 exists
{noformat}

*Proposed AC10.* The condition "version 1 inactive, version 2 active" is correct and should be written into the AC.

{noformat}Scenario: AC10 Version on a superseded document
  Given the appraisal report has version 1 inactive and version 2 active
  When a user with Documents U adds a new version to version 1
  Then the system refuses the request with 409 and MSG-P5-025
  Then the system writes no new row
  Then version 2 is still the only active version
{noformat}

To test AC10, get the version 1 row ID from {{GET /documents/{id}}} and call {{POST /documents/{version 1 row ID}/versions}}.

*Fallback if fewer ACs are required:* merge AC9 into AC10. Both use the same endpoint, both return 409, and both mean "this version is no longer the latest". Keep the simultaneous case as an automated test (TC-E1-024-09) and keep MSG-GEN-004 in the AC text.

*Decision needed (Product Owner):* keep AC9 as reworded, merge it into AC10, or remove it and accept the gaps above. The recommendation is to keep it and add the simultaneous-duplicate case to AC8.

### Comment 10: VAISHNAVI KAULGE, 2026-11-18T15:05:01.550+0700

Comment ID 1796874

@Chanapai Gingpuwaluck 
1. "Implement after E1-006 and the OCR ticket"

* *The outbox ticket is RWB-TE-006.* E1-024 needs it to write the {{DocumentStored}} event in AC1 (flow step 6). RWB-E1-006 was removed by D-RCV-35 and isn't needed.
* *The order is E1-024 first, then E1-049.* The build sequence has E1-049 depending on E1-024, and E1-041 and E1-057 depending on E1-049. E1-024 must not wait for OCR.
* *JOB-12 doesn't block E1-024.* E1-049 creates JOB-12, so E1-024 builds {{CopyPendingStep}} as a plain class and tests it by calling it directly. E1-049 then registers it as a step of JOB-12. The end-to-end check "the next intake run copies the file" (AC11) is verified in E1-049.

----

h3. 2. Declared dependencies

||Dependency||Status||What it blocks in E1-024||
|E1-001 (document tables)|Waiting on E1-043 (Hold)|Everything that uses the database, including E1-024's own migration|
|TE-012 (blob containers)|Design, Hold|Real file writes, and the container half of AC2|
|E1-025 (DOCTYPE)|Design, waiting on v2 and DL19|Type lookup, AC3 and AC5 (can be stubbed with a test table)|
|E1-018 (CaseDirectory)|No sprint|The case check (can be stubbed)|
|E1-027 (DecisionLogWriter)|No sprint|The decision log entry (can be stubbed)|

The root blocker is *E1-043 (Hold)*. The chain is E1-043, then E1-001, then E1-024. It also holds back the roles stories E1-022 and E1-037 and the scope story E1-016.

----

h3. 3. Used but not in "Depends on"

||Item||How E1-024 uses it||Action||
|RWB-TE-006 (outbox)|{{DocumentStored}} event, AC1|Add to "Depends on"|
|E1-019, E1-022, E1-037 (roles and permissions) and E1-016 (scope)|Documents C, R and U rights, AC12 and X10|Add as integration dependencies for AC12 and X10 only|
|ACE PII access log (DEP-04)|Read logging, BR9|Add as an integration dependency; stub in tests|
|JOB-12|Retry of {{COPY_PENDING}}, AC11|Don't add. It is built in E1-049, which depends on E1-024|
|E1-049, E1-041, E1-057|Intake, scan, retention|Don't add. They depend on E1-024, and adding them would create a loop|
|E1-042 and E1-043 (parameters)|{{document_hub_parameter}}|E1-024's own migration creates the table. No story I've read defines how its two rows are loaded, so tests seed {{INTAKE_ALLOWED_TYPES}} and {{INTAKE_MAX_FILE_MB}} directly|

----

h3. 4. Decision: option (a) or (b)

*Proposal for the team to confirm: option (b). Build RWB-E1-024 against stubs, and unblock RWB-E1-043 in parallel.*

*Why not (a)*

* Pulling in E1-018, E1-027 and TE-006 brings more tickets with it. E1-027 also needs E1-008 and E1-056, and TE-006 also needs E1-044 and E1-007. E1-018 has no sprint.
* It doesn't remove the main blocker. E1-001 waits on E1-043 (Hold), so the database work is blocked either way.

*What can be built and tested now (with stubs)* Stub {{CaseDirectory}}, {{DecisionLogWriter}}, {{OutboxWriter}}, {{DocumentStorage}} and the document type table. Use a test database created from Physical Schema v6.

* AC3 to AC10: retention class, new versions, unknown type, file type, size limit, duplicate file, concurrent versions, version on a superseded document.
* AC2, service half: delete and replace of a write-once document are refused with MSG-P5-002 and the audit event.
* AC1, core behavior: the document row, the extracted field and the hash read-back.

*What would move to a later integration test*

||Check||Needs||
|AC1: decision log entry, outbox event, file in the real container|E1-027, TE-006, TE-012|
|AC2, container half: immutability policy refuses overwrite and delete|TE-012 on SIT|
|AC11: the retry run copies the file and sets {{STORED}}|TE-012 and E1-049 (JOB-12)|
|AC12 and X10: role and scope checks, and the access log entry|E1-037, E1-016 and the ACE PII access log|

*Conditions proposed*

* Code to the published interfaces in the story, and keep the stubs minimal, so the stubs don't drift from the real components.
* The story is not done until the integration checks above pass against the real components. They stay open items on the card.
* E1-024's migration {{V1_5_024}} merges after E1-001's, as in the migration merge order map. This is the one point where (b) still depends on E1-001.
* RWB-E1-043 (Hold) needs to be unblocked now, whichever option is chosen.

*Proposed order:* RWB-TE-006 and the other dependencies as sequenced, then E1-024, then E1-049, which creates JOB-12 and registers {{CopyPendingStep}} as a step.

*Confirmation needed from the team:* please confirm (b), or choose (a), so the sprint plan can be set.

### Comment 11: RAPEEPAT CHULAOTRAKUL, 2026-11-18T16:54:33.908+0700, edited 2026-11-18T16:54:43.836+0700

Comment ID 1797357

@VAISHNAVI KAULGE @CHANISSARA MAHAKITTIKUN 


Waiting for the updated {{.md}} file with the agreed details on delete and replace for non-write-once documents.




h2. Delete and replace for documents that are not write-once
*Needs decision.* The story doesn't say what should happen.
* This story builds the {{delete()}} and {{replaceContent()}} methods and makes them refuse write-once documents (build step 7).
* Option C doesn't apply as written. The retention job (JOB-17, RWB-E1-041) never deletes a document or a blob (E1-041 rule BR5).
* The story's guardrail says the service never overwrites a blob. Every version is a new blob.
* *Proposed answer: Option A for this story.* Delete and replace are refused for every document, and a change is a new version. If the bank needs real deletion later, it goes in a separate story with its own role and rules. The Product Owner should confirm, and then an exception path and an AC should be added.

h2. 

### Comment 12: Nuttapon Jittachotisak, 2026-11-18T17:37:52.316+0700, edited 2026-11-18T17:48:44.687+0700

Comment ID 1797555

h2. 1. {color:#36b37e}[clear]{color}Is the path a blob storage path?

*Clear.*

----

h2. 2. {color:#ff5630}[block]{color}JOB-12 is scheduled. Where does it get the file to retry?

*Wait for method to retain file for JOB-12 from* [https://scbjira.atlassian.net/browse/TB0001-1210|https://scbjira.atlassian.net/browse/TB0001-1210|smart-link] 

----

h2. 3. {color:#36b37e}[clear]{color}Is the UI in scope?

*Clear. No UI in scope.*

----

h2. 4. {color:#b38600}[non-block]{color}What is {{documentId}} in {{POST /documents/{documentId}/versions}}?

*Beware* [https://scbjira.atlassian.net/browse/TB0001-1188?xpis=eyJicmlkZ2UiOiJzbWFydExpbmtzIiwiaWQiOiIxNzk0OTk4NjYyODg5Iiwic291cmNlIjoiamlyYS1KU1cifQ%3D%3D|https://scbjira.atlassian.net/browse/TB0001-1188?xpis=eyJicmlkZ2UiOiJzbWFydExpbmtzIiwiaWQiOiIxNzk0OTk4NjYyODg5Iiwic291cmNlIjoiamlyYS1KU1cifQ%3D%3D|smart-link] need to finish first.

documentId is latest version in table {{document}}. The first version was upload at {{POST /cases/{caseId}/documents}} in [https://scbjira.atlassian.net/browse/TB0001-1188|https://scbjira.atlassian.net/browse/TB0001-1188|smart-link] .

----

h2. 5. {color:#ff5630}[block][need clarify from henka]{color}Extraction: is there a specific mapping, or just header and row?

@CHANISSARA MAHAKITTIKUN Please help clarify a little bit more about this.

For about extraction field to {{document_field}} table

This story only insert row to {{document}} table and store new added version of file to blob storage?

Then [https://scbjira.atlassian.net/browse/TB0001-1214|https://scbjira.atlassian.net/browse/TB0001-1214|smart-link]  will handle about extract field and insert to {{document_field}} table.



If process be like this *AC1 Stored against case* could not be done.


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
