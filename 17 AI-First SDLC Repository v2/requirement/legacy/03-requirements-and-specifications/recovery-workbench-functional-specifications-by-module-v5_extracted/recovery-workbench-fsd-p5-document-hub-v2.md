<!-- source: 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v5.zip!Recovery Workbench FSD P5 Document hub v2.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v5.zip!Recovery Workbench FSD P5 Document hub v2.md`  
> **Converted from:** Markdown (extracted)

# Recovery Workbench P5 Document hub

Functional specification. SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | FSD P5 Document hub |
| Document ID | P5-RWB-FSD-v2 |
| Version | 2 |
| Status | In review |
| Classification | Confidential |
| Date | 28 October 2026 |
| FSD owner | Business analyst, P5 |
| Business owner | Business lead |

| Module code | Module name | First in |
|---|---|---|
| P5 | Document hub | E1 store and OCR; E2 generation |

**Feature scope.** Store, index, OCR, classification, extraction, review queue, retention, custody.

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program | BRD | Source |
| Recovery Workbench Technical Specification P5 Document hub | TSD | Pair |
| Recovery Workbench User Stories Epic 1 and Epic 2 | Backlog | Traceability |

## Existing capability check

| Capability | Verdict | Owning document | Note |
|---|---|---|---|
| Sign-in, access check, audit and PII logging | REUSE | ACE common module | No build in this module |
| Case record and shared entities | REUSE | ACE common module; Case and Workflow Model | Read through the P3 interfaces |
| Notification path | REUSE | ACE notification path | Recovery templates only |
| Workflow and state machine | REUSE | Workflow Engine Design | Stages and sentries from P3 |
| Decision record and audit trail | REUSE | Audit and Logging Design | Writes through P7 |
| Attachments and evidence | NEW | Document Management Design | Document hub is the system of record (DT06) |
| Role and permission matrix | REUSE | Users Roles and Permissions | Capability areas from P4 |
| Restructure calculator | REUSE | ACE common module | Not used |

## A1. Context and scope

### A1.1 Scope of work and deliverables

**In scope.** Store, index, OCR, classification, extraction, review queue, retention, custody.

**Out of scope.** Collections before day 90 on EFS; booking in the core bank, which the officer does; work owned by other modules, reached through their interfaces.

**Dependencies.** FEAT-CWC-23; FEAT-DCM-01; FEAT-DCM-02; FEAT-DCM-07; FEAT-DCM-07, FEAT-DCM-03; FEAT-DCM-08; FEAT-DCM-09; FEAT-DCM-10

**Constraints.** Built in the ACE service as part of the recovery module; data through COLLINS and file loads; every value a business person may change is a versioned data row (principle 1).

### A1.2 Feature overview

| Module | Feature code | Feature name | Kind | Description | First in | Section |
|---|---|---|---|---|---|---|
| P5 | FEAT-DCM-01 | Store documents with a write-once container for legal types | System | Holds every case document in blob storage, with legal types written to a container that cannot be overwritten. | E1 | A2.1 |
| P5 | FEAT-DCM-02 | Index documents by case, type, date and extracted fields | System | Builds the document index so a document is found by case, type, date or any extracted field. | E1 | A2.2 |
| P5 | FEAT-DCM-03 | Agree the six document types and their fields | Admin | Fixes the first six document types, the fields extracted from each, and the checklist each belongs to. | E1 | A2.3 |
| P5 | FEAT-DCM-04 | Attach a document to a case | User | Lets a user attach a document to the case from the case record view, with its type and date. | E1 | A2.4 |
| P5 | FEAT-DCM-05 | Search documents within a case | User | Finds any document on the case by type, date or extracted field, in seconds. | E1 | A2.5 |
| P5 | FEAT-DCM-06 | Search documents across cases | User | Searches the whole document index across cases, for audit, legal and recovery questions. | E1 | A2.6 |
| P5 | FEAT-DCM-07 | Run the OCR pipeline on inbound documents | System | Reads every inbound document through the OCR service and passes the text to classification. | E1 | A2.7 |
| P5 | FEAT-DCM-08 | Classify a document into one of the six types | System | Types each read document against the six agreed types and records the classification confidence. | E1 | A2.8 |
| P5 | FEAT-DCM-09 | Extract fields from the six document types | System | Pulls the agreed fields out of each typed document and writes them into the index with a confidence score. | E1 | A2.9 |
| P5 | FEAT-DCM-10 | Send a low-confidence extraction to the review queue | System | Routes any extraction below the confidence threshold to a person instead of writing it to the case. | E1 | A2.10 |
| P5 | FEAT-DCM-11 | Check a low-confidence extraction | User | Lets a person confirm or correct the extracted fields, which also feeds the extraction evaluation. | E1 | A2.11 |
| P5 | FEAT-DCM-12 | Attach an OCR-read document to its case automatically | System | Matches a read document to its case and attaches it with no person involved. | E1 | A2.12 |
| P5 | FEAT-DCM-13 | Take intake from branches and the mailroom | System | Accepts scanned documents from branch and mailroom scanning into the OCR pipeline. | E1 | A2.13 |
| P5 | FEAT-DCM-14 | Take intake from partner SFTP | System | Accepts partner document files over SFTP into the same OCR and indexing path. | E1 | A2.14 |
| P5 | FEAT-DCM-15 | Take intake from email | System | Accepts documents arriving by email into the OCR and indexing path, which replaces email hand-offs. | E1 | A2.15 |
| P5 | FEAT-DCM-16 | Hold the document checklist per case type as reference data | Admin | Keeps the list of documents each case type needs, so completeness is checked against data rather than memory. | E1 | A2.16 |
| P5 | FEAT-DCM-17 | Apply retention classes to stored documents | Admin | Sets the retention class on each document type and applies it through the document life. | E1 | A2.17 |
| P5 | FEAT-DCM-18 | Virus scan every document on intake | System | Scans every inbound document before it is stored, and quarantines anything that fails. | E1 | A2.18 |
| P5 | FEAT-DCM-19 | Keep the Workbench document hub as the system of record for documents | System | Writes the document to the Workbench document hub as the record and holds only the index and the working copy in the Workbench. | E1 | A2.19 |
| P5 | FEAT-DCM-20 | Version a document and keep its history | System | Keeps every version of a document with the date and the source, so a superseded version is still readable. | E1 | A2.20 |
| P5 | FEAT-DCM-21 | Take field app photos and bills into the OCR intake | System | Accepts photos and bills captured in the field into the same OCR, extraction and indexing path. | E2 | A2.21 |
| P5 | FEAT-DCM-22 | Extend extraction to the stage 2 and 3 document types | System | Adds the treatment and litigation document types to classification and field extraction. | E2 | A2.22 |

### A1.3 Background

Documents are in folders, shared drives and with couriers; originals go missing and evidence is rebuilt for each audit.

### A1.4 Preconditions

- The user holds a Workbench role with the right in the capability area of the screen or action.
- The data products the module reads carry today's business date, or show their date as stale.

## A2. Functional decomposition

### A2.1 Store documents with a write-once container for legal types

#### A2.1.1 Intent

**Business objective.** Holds every case document in blob storage, with legal types written to a container that cannot be overwritten.

**Problem.** Documents are in folders, shared drives and with couriers; originals go missing and evidence is rebuilt for each audit.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Fields extracted without review | Rising each month | Decision log and Workbench records | Monthly |

#### A2.1.2 Description

**Functional overview.** Holds every case document in blob storage, with legal types written to a container that cannot be overwritten.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Store documents with a write-once container for legal types | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Blob storage, the Workbench document hub

**Prerequisites.** None

#### A2.1.3 Business rules and structure

##### A2.1.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P5-001-1 | Upload of a file type not allowed | MSG-P5-001 This file type cannot be stored. Use PDF, JPG or PNG. |
| VR-P5-001-2 | Change to a write-once legal document | MSG-P5-002 Legal documents cannot be changed. Add a new version instead. |
| VR-P5-001-3 | An original document is overdue back | MSG-P5-004 {document} is due back from {holder} since {date}. |
| BR-P5-001 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.1.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Legal counsel, Compliance and PDPA officer | Also uses |

#### A2.1.4 Acceptance criteria

##### A2.1.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P5-001-01 | Stored against case | a scanned court notice "notice-0001.pdf" of 1.2 MB for case "RW-2026-000123" with source "SCAN" | it is stored | one document row exists with case "RW-2026-000123", type "COURT_NOTICE", source "SCAN", doc_version 1 and the stored date of today And its extracted field "black_case_no" with value "BC-TEST-0456" is in the index And the file is in container "rwb-docs-legal" at "rwb-docs-legal/{caseId}/{documentId}/v1" And DocumentStored is written to the outbox with the document ID, the case ID, the type and the source And the litigation officer opens it from the case documents screen and GET content returns the same SHA-256 hash | RWB-E1-024 |

##### A2.1.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P5-001-01 | Write once | the court notice from AC1 is stored with write_once true | a delete and a content replace are attempted through the document store and directly on the container | each attempt is refused with MSG-P5-002 And the file hash and the document row are unchanged And an audit event "DOCUMENT_CHANGE_REFUSED" is written for each attempt with the document ID and the caller | RWB-E1-024 |
| AC-ALT-P5-001-02 | Retention class | a document of type "APPRAISAL_REPORT" for case "RW-2026-000123" | it is stored | the document row carries retention class "GENERAL05Y" from type table version "DOCTYPE-2026.11" And write_once is false and the file is in container "rwb-docs" | RWB-E1-024 |

##### A2.1.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P5-001-01 | Unknown document type is refused | a file for case "RW-2026-000123" with type "BANK_STATEMENT" | it is stored | the call is refused with 422 and MSG-P5-006 And no document row, decision log entry or event is written | RWB-E1-024 |
| AC-EXC-P5-001-02 | File type not allowed | a file "macro-0001.docx" with Word content for case "RW-2026-000123" | it is stored | the call is refused with 415 and MSG-P5-001 And nothing is written to the containers or the tables | RWB-E1-024 |
| AC-EXC-P5-001-03 | The storage copy fails | container "rwb-docs" refuses writes | an appraisal report is stored for case "RW-2026-000123" | the document row is written with state "COPY_PENDING" And GET content returns 503 with MSG-GEN-006 naming "Document storage" And when the container accepts writes again the next document intake run copies the file and sets state "STORED" | RWB-E1-024 |
| AC-EXC-P5-001-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P5-001-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.1.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P5-001-01 | Document intake | Schedule | Every 15 minutes | Takes scans, SFTP files and emails into OCR | Documents on the case the same day | No document is lost between paths |

---

### A2.2 Index documents by case, type, date and extracted fields

#### A2.2.1 Intent

**Business objective.** Builds the document index so a document is found by case, type, date or any extracted field.

**Problem.** Documents are in folders, shared drives and with couriers; originals go missing and evidence is rebuilt for each audit.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Fields extracted without review | Rising each month | Decision log and Workbench records | Monthly |

#### A2.2.2 Description

**Functional overview.** Builds the document index so a document is found by case, type, date or any extracted field.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Index documents by case, type, date and extracted fields | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, the Workbench document hub

**Prerequisites.** FEAT-DCM-01

#### A2.2.3 Business rules and structure

##### A2.2.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P5-002-1 | Change to a write-once legal document | MSG-P5-002 Legal documents cannot be changed. Add a new version instead. |
| VR-P5-002-2 | An original document is overdue back | MSG-P5-004 {document} is due back from {holder} since {date}. |
| VR-P5-002-3 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P5-002 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.2.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.2.4 Acceptance criteria

##### A2.2.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P5-002-01 | Stored against case | a scanned court notice "notice-0001.pdf" of 1.2 MB for case "RW-2026-000123" with source "SCAN" | it is stored | one document row exists with case "RW-2026-000123", type "COURT_NOTICE", source "SCAN", doc_version 1 and the stored date of today And its extracted field "black_case_no" with value "BC-TEST-0456" is in the index And the file is in container "rwb-docs-legal" at "rwb-docs-legal/{caseId}/{documentId}/v1" And DocumentStored is written to the outbox with the document ID, the case ID, the type and the source And the litigation officer opens it from the case documents screen and GET content returns the same SHA-256 hash | RWB-E1-024 |

##### A2.2.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P5-002-01 | Write once | the court notice from AC1 is stored with write_once true | a delete and a content replace are attempted through the document store and directly on the container | each attempt is refused with MSG-P5-002 And the file hash and the document row are unchanged And an audit event "DOCUMENT_CHANGE_REFUSED" is written for each attempt with the document ID and the caller | RWB-E1-024 |
| AC-ALT-P5-002-02 | Retention class | a document of type "APPRAISAL_REPORT" for case "RW-2026-000123" | it is stored | the document row carries retention class "GENERAL05Y" from type table version "DOCTYPE-2026.11" And write_once is false and the file is in container "rwb-docs" | RWB-E1-024 |

##### A2.2.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P5-002-01 | Unknown document type is refused | a file for case "RW-2026-000123" with type "BANK_STATEMENT" | it is stored | the call is refused with 422 and MSG-P5-006 And no document row, decision log entry or event is written | RWB-E1-024 |
| AC-EXC-P5-002-02 | File type not allowed | a file "macro-0001.docx" with Word content for case "RW-2026-000123" | it is stored | the call is refused with 415 and MSG-P5-001 And nothing is written to the containers or the tables | RWB-E1-024 |
| AC-EXC-P5-002-03 | The storage copy fails | container "rwb-docs" refuses writes | an appraisal report is stored for case "RW-2026-000123" | the document row is written with state "COPY_PENDING" And GET content returns 503 with MSG-GEN-006 naming "Document storage" And when the container accepts writes again the next document intake run copies the file and sets state "STORED" | RWB-E1-024 |
| AC-EXC-P5-002-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P5-002-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.2.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P5-002-01 | Document intake | Schedule | Every 15 minutes | Takes scans, SFTP files and emails into OCR | Documents on the case the same day | No document is lost between paths |

---

### A2.3 Agree the six document types and their fields

#### A2.3.1 Intent

**Business objective.** Fixes the first six document types, the fields extracted from each, and the checklist each belongs to.

**Problem.** Documents are in folders, shared drives and with couriers; originals go missing and evidence is rebuilt for each audit.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Fields extracted without review | Rising each month | Decision log and Workbench records | Monthly |

#### A2.3.2 Description

**Functional overview.** Fixes the first six document types, the fields extracted from each, and the checklist each belongs to.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Center of excellence analyst | Opens the screen and agree the six document types and their fields | Checks the role, the capability area and the scope |
| 2 | Center of excellence analyst | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** None

#### A2.3.3 Business rules and structure

##### A2.3.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P5-003-1 | Change to a write-once legal document | MSG-P5-002 Legal documents cannot be changed. Add a new version instead. |
| VR-P5-003-2 | An original document is overdue back | MSG-P5-004 {document} is due back from {holder} since {date}. |
| BR-P5-003 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.3.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| document.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| document.party_id | The party this record belongs to | uuid | No | None | No |
| document.document_type | Type from the document checklist | varchar(30) | Yes | LOV-DOC-TYPE | No |
| document.source | Scan, upload, generated, partner, email | varchar(12) | Yes | LOV-DOC-SOURCE | No |
| document.storage_ref | Reference to the stored file | varchar(400) | Yes | None | No |
| document.classification_confidence | OCR classification confidence | numeric(5,4) | No | None | No |
| document.review_status | Not needed, pending, confirmed, corrected | varchar(12) | Yes | LOV-REVIEW | No |
| document.retention_class | Retention class | varchar(10) | Yes | LOV-RETENTION | No |

##### A2.3.3.3 Roles and permissions

| Role | Use |
|---|---|
| Center of excellence analyst | Primary |
| Legal counsel, Case owner | Also uses |

#### A2.3.4 Acceptance criteria

##### A2.3.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P5-003-01 | Field list signed | the six types and their 26 fields in load file "DOCTYPE-2026.11" And each row carries the legal counsel sign-off of user "TEST-LEGAL-01" dated 6 November 2026 And each row carries the NPA sign-off of user "TEST-HEADNPA-01" dated 6 November 2026 | "TEST-REFADM-01" loads the file for table "DOCUMENT_TYPE" with valid from 30 November 2026 | the load has status "LOADED" with 6 rows And every row holds both sign-off user IDs and both dates | RWB-E1-025 |

##### A2.3.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P5-003-01 | Reference data | the load from AC1 | "TEST-APPROVER-01" approves it | the document type table version "DOCTYPE-2026.11" is in force from 30 November 2026 And it holds DEMAND_LETTER, COURT_NOTICE, APPRAISAL_REPORT, TITLE_DEED, SETTLEMENT_AGREEMENT and GUARANTOR_NOTICE And COURT_NOTICE holds the fields court_name, black_case_no, notice_date and hearing_date with retention class "LEGAL10Y" and write_once true And APPRAISAL_REPORT has retention class "GENERAL05Y", write_once false and 4 fields | RWB-E1-025 |
| AC-ALT-P5-003-02 | The same version loaded twice | version "DOCTYPE-2026.11" is loaded | "TEST-REFADM-01" loads a file with version "DOCTYPE-2026.11" again | the request is refused with 409 and MSG-P3-027 naming "version already loaded" And the first load is unchanged | RWB-E1-025 |

##### A2.3.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P5-003-01 | Load without both sign-offs is refused | a load file where the GUARANTOR_NOTICE row has no NPA sign-off | "TEST-REFADM-01" loads it | the load is refused whole with MSG-P3-027 naming row 6 and "NPA sign-off missing" And no row of that file is written and the version in force is unchanged | RWB-E1-025 |
| AC-EXC-P5-003-02 | Invalid values are refused whole | a load file where the TITLE_DEED row has retention class "KEEP99" and a seventh row repeats the type code "COURT_NOTICE" | "TEST-REFADM-01" loads it | the load is refused whole with MSG-P3-027 listing both rows And the version in force is unchanged | RWB-E1-025 |
| AC-EXC-P5-003-03 | The loader cannot approve their own load | "TEST-REFADM-01" loaded version "DOCTYPE-2027.01" and also holds Reference data A in the test set | "TEST-REFADM-01" approves it | the request is refused with 409 and MSG-P7-002 And the load stays "LOADED" | RWB-E1-025 |
| AC-EXC-P5-003-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P5-003-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.3.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P5-003-01 | Document intake | Schedule | Every 15 minutes | Takes scans, SFTP files and emails into OCR | Documents on the case the same day | No document is lost between paths |

---

### A2.4 Attach a document to a case

#### A2.4.1 Intent

**Business objective.** Lets a user attach a document to the case from the case record view, with its type and date.

**Problem.** Documents are in folders, shared drives and with couriers; originals go missing and evidence is rebuilt for each audit.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Fields extracted without review | Rising each month | Decision log and Workbench records | Monthly |

#### A2.4.2 Description

**Functional overview.** Lets a user attach a document to the case from the case record view, with its type and date.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Case owner | Opens the screen and attach a document to a case | Checks the role, the capability area and the scope |
| 2 | Case owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench, the Workbench document hub

**Prerequisites.** FEAT-DCM-02

#### A2.4.3 Business rules and structure

##### A2.4.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P5-004-1 | Change to a write-once legal document | MSG-P5-002 Legal documents cannot be changed. Add a new version instead. |
| VR-P5-004-2 | An original document is overdue back | MSG-P5-004 {document} is due back from {holder} since {date}. |
| BR-P5-004 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.4.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| document.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| document.party_id | The party this record belongs to | uuid | No | None | No |
| document.document_type | Type from the document checklist | varchar(30) | Yes | LOV-DOC-TYPE | No |
| document.source | Scan, upload, generated, partner, email | varchar(12) | Yes | LOV-DOC-SOURCE | No |
| document.storage_ref | Reference to the stored file | varchar(400) | Yes | None | No |
| document.classification_confidence | OCR classification confidence | numeric(5,4) | No | None | No |
| document.review_status | Not needed, pending, confirmed, corrected | varchar(12) | Yes | LOV-REVIEW | No |
| document.retention_class | Retention class | varchar(10) | Yes | LOV-RETENTION | No |

##### A2.4.3.3 Roles and permissions

| Role | Use |
|---|---|
| Case owner | Primary |
| Restructuring officer (FCR), Litigation officer | Also uses |

#### A2.4.4 Acceptance criteria

##### A2.4.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P5-004-01 | Upload | "TEST-CO-01" is on the Documents tab of case "RW-2026-000123" | "TEST-CO-01" uploads "court-notice-0007.pdf" of 2 MB with type "COURT_NOTICE" | the response is 201 with source "UPLOAD" and doc_version 1 And the document shows at the top of the case document list within 5 seconds of submit And GET /cases/{caseId}/documents with type "COURT_NOTICE" returns it | RWB-E1-026 |

##### A2.4.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P5-004-01 | Search | case "RW-2026-000123" holds 50 documents of which 12 are "COURT_NOTICE" And 4 of the court notices were stored between 1 October 2026 and 31 October 2026 | "TEST-CO-01" searches type "COURT_NOTICE" from 1 October 2026 to 31 October 2026 | exactly the 4 court notices stored in October show, newest first And the result count reads 4 | RWB-E1-026 |
| AC-ALT-P5-004-02 | Checklist placeholder | case "RW-2026-000123" holds 12 court notices and 1 appraisal report and no other agreed type | the Documents tab opens | the checklist placeholder lists the six agreed types And COURT_NOTICE shows present with 12, APPRAISAL_REPORT shows present with 1 And DEMAND_LETTER, TITLE_DEED, SETTLEMENT_AGREEMENT and GUARANTOR_NOTICE show not present | RWB-E1-026 |

##### A2.4.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P5-004-01 | Upload that fails the malware scan | a test file "eicar-0001.pdf" holding the EICAR test signature | "TEST-CO-01" uploads it with type "COURT_NOTICE" | the response is 422 with MSG-P5-016 And the file is in the quarantine container and no document row exists | RWB-E1-026 |
| AC-EXC-P5-004-02 | File type not allowed | a file "minutes-0002.xlsx" with spreadsheet content | "TEST-CO-01" uploads it with type "SETTLEMENT_AGREEMENT" | the response is 415 with MSG-P5-001 shown in the upload dialog And no document is stored | RWB-E1-026 |
| AC-EXC-P5-004-03 | No document matches | case "RW-2026-000123" holds no "TITLE_DEED" | "TEST-CO-01" searches type "TITLE_DEED" | the list shows the empty state "No documents match this search." with the action "Clear the search" | RWB-E1-026 |
| AC-EXC-P5-004-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P5-004-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.4.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P5-004-01 | Document intake | Schedule | Every 15 minutes | Takes scans, SFTP files and emails into OCR | Documents on the case the same day | No document is lost between paths |

---

### A2.5 Search documents within a case

#### A2.5.1 Intent

**Business objective.** Finds any document on the case by type, date or extracted field, in seconds.

**Problem.** Documents are in folders, shared drives and with couriers; originals go missing and evidence is rebuilt for each audit.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Fields extracted without review | Rising each month | Decision log and Workbench records | Monthly |

#### A2.5.2 Description

**Functional overview.** Finds any document on the case by type, date or extracted field, in seconds.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Case owner | Opens the screen and search documents within a case | Checks the role, the capability area and the scope |
| 2 | Case owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-DCM-02

#### A2.5.3 Business rules and structure

##### A2.5.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P5-005-1 | Change to a write-once legal document | MSG-P5-002 Legal documents cannot be changed. Add a new version instead. |
| VR-P5-005-2 | An original document is overdue back | MSG-P5-004 {document} is due back from {holder} since {date}. |
| VR-P5-005-3 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P5-005 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.5.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| document.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| document.party_id | The party this record belongs to | uuid | No | None | No |
| document.document_type | Type from the document checklist | varchar(30) | Yes | LOV-DOC-TYPE | No |
| document.source | Scan, upload, generated, partner, email | varchar(12) | Yes | LOV-DOC-SOURCE | No |
| document.storage_ref | Reference to the stored file | varchar(400) | Yes | None | No |
| document.classification_confidence | OCR classification confidence | numeric(5,4) | No | None | No |
| document.review_status | Not needed, pending, confirmed, corrected | varchar(12) | Yes | LOV-REVIEW | No |
| document.retention_class | Retention class | varchar(10) | Yes | LOV-RETENTION | No |

##### A2.5.3.3 Roles and permissions

| Role | Use |
|---|---|
| Case owner | Primary |
| Litigation officer, Legal counsel | Also uses |

#### A2.5.4 Acceptance criteria

##### A2.5.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P5-005-01 | Upload | "TEST-CO-01" is on the Documents tab of case "RW-2026-000123" | "TEST-CO-01" uploads "court-notice-0007.pdf" of 2 MB with type "COURT_NOTICE" | the response is 201 with source "UPLOAD" and doc_version 1 And the document shows at the top of the case document list within 5 seconds of submit And GET /cases/{caseId}/documents with type "COURT_NOTICE" returns it | RWB-E1-026 |

##### A2.5.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P5-005-01 | Search | case "RW-2026-000123" holds 50 documents of which 12 are "COURT_NOTICE" And 4 of the court notices were stored between 1 October 2026 and 31 October 2026 | "TEST-CO-01" searches type "COURT_NOTICE" from 1 October 2026 to 31 October 2026 | exactly the 4 court notices stored in October show, newest first And the result count reads 4 | RWB-E1-026 |
| AC-ALT-P5-005-02 | Checklist placeholder | case "RW-2026-000123" holds 12 court notices and 1 appraisal report and no other agreed type | the Documents tab opens | the checklist placeholder lists the six agreed types And COURT_NOTICE shows present with 12, APPRAISAL_REPORT shows present with 1 And DEMAND_LETTER, TITLE_DEED, SETTLEMENT_AGREEMENT and GUARANTOR_NOTICE show not present | RWB-E1-026 |

##### A2.5.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P5-005-01 | Upload that fails the malware scan | a test file "eicar-0001.pdf" holding the EICAR test signature | "TEST-CO-01" uploads it with type "COURT_NOTICE" | the response is 422 with MSG-P5-016 And the file is in the quarantine container and no document row exists | RWB-E1-026 |
| AC-EXC-P5-005-02 | File type not allowed | a file "minutes-0002.xlsx" with spreadsheet content | "TEST-CO-01" uploads it with type "SETTLEMENT_AGREEMENT" | the response is 415 with MSG-P5-001 shown in the upload dialog And no document is stored | RWB-E1-026 |
| AC-EXC-P5-005-03 | No document matches | case "RW-2026-000123" holds no "TITLE_DEED" | "TEST-CO-01" searches type "TITLE_DEED" | the list shows the empty state "No documents match this search." with the action "Clear the search" | RWB-E1-026 |
| AC-EXC-P5-005-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P5-005-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.5.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P5-005-01 | Document intake | Schedule | Every 15 minutes | Takes scans, SFTP files and emails into OCR | Documents on the case the same day | No document is lost between paths |

---

### A2.6 Search documents across cases

#### A2.6.1 Intent

**Business objective.** Searches the whole document index across cases, for audit, legal and recovery questions.

**Problem.** Documents are in folders, shared drives and with couriers; originals go missing and evidence is rebuilt for each audit.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Fields extracted without review | Rising each month | Decision log and Workbench records | Monthly |

#### A2.6.2 Description

**Functional overview.** Searches the whole document index across cases, for audit, legal and recovery questions.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Legal counsel | Opens the screen and search documents across cases | Checks the role, the capability area and the scope |
| 2 | Legal counsel | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-DCM-02

#### A2.6.3 Business rules and structure

##### A2.6.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P5-006-1 | Change to a write-once legal document | MSG-P5-002 Legal documents cannot be changed. Add a new version instead. |
| VR-P5-006-2 | An original document is overdue back | MSG-P5-004 {document} is due back from {holder} since {date}. |
| BR-P5-006 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.6.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| document.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| document.party_id | The party this record belongs to | uuid | No | None | No |
| document.document_type | Type from the document checklist | varchar(30) | Yes | LOV-DOC-TYPE | No |
| document.source | Scan, upload, generated, partner, email | varchar(12) | Yes | LOV-DOC-SOURCE | No |
| document.storage_ref | Reference to the stored file | varchar(400) | Yes | None | No |
| document.classification_confidence | OCR classification confidence | numeric(5,4) | No | None | No |
| document.review_status | Not needed, pending, confirmed, corrected | varchar(12) | Yes | LOV-REVIEW | No |
| document.retention_class | Retention class | varchar(10) | Yes | LOV-RETENTION | No |

##### A2.6.3.3 Roles and permissions

| Role | Use |
|---|---|
| Legal counsel | Primary |
| Internal audit, Compliance and PDPA officer | Also uses |

#### A2.6.4 Acceptance criteria

##### A2.6.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P5-006-01 | Search by field | "TEST-LIT-01" is on the Document search page | "TEST-LIT-01" searches type "APPRAISAL_REPORT", field appraised_value greater than 5,000,000, stored from 1 October 2026 to 31 October 2026 | exactly the 9 matching documents list with case number, type, stored date and the field value And the response arrives within 2 seconds | RWB-E1-033 |

##### A2.6.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P5-006-01 | Role limit | user "TEST-LIT-02" holds RW-LITOFF with scope TEAM on team "MTG-BKK-LIT", whose cases are all product group "MORTGAGE" And 40 of the 500 documents are on "HIRE_PURCHASE" cases | "TEST-LIT-02" searches type "COURT_NOTICE" with no date | no document on a "HIRE_PURCHASE" case appears And one access event "DOCUMENT_SEARCH" is written with the user, the criteria, the result count and the case IDs returned | RWB-E1-033 |
| AC-ALT-P5-006-02 | Free text | the OCR text of 3 documents holds the synthetic guarantor name "ผู้ค้ำทดสอบ หนึ่ง" | "TEST-LIT-01" searches the free text "ผู้ค้ำทดสอบ หนึ่ง" | the 3 documents list with a snippet in which the name is highlighted And the access event holds the SHA-256 hash of the term and not the term | RWB-E1-033 |

##### A2.6.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P5-006-01 | Free text refused for a masked role | user "TEST-CO-01" holds RW-CASEOWN, whose masking rule hides party names | "TEST-CO-01" searches the free text "ผู้ค้ำทดสอบ" | the request is refused with 422 and MSG-P5-020 naming "document text" And no query runs | RWB-E1-033 |
| AC-EXC-P5-006-02 | No criterion | "TEST-LIT-01" is on the Document search page | "TEST-LIT-01" searches with every criterion empty | the request is refused with 422 and MSG-GEN-001 naming "a search criterion" | RWB-E1-033 |
| AC-EXC-P5-006-03 | Access log not confirmed | the PII access log does not confirm writes | "TEST-LIT-01" searches type "COURT_NOTICE" | the request returns 503 with MSG-P5-019 And no result row is returned | RWB-E1-033 |
| AC-EXC-P5-006-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P5-006-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.6.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P5-006-01 | Document intake | Schedule | Every 15 minutes | Takes scans, SFTP files and emails into OCR | Documents on the case the same day | No document is lost between paths |

---

### A2.7 Run the OCR pipeline on inbound documents

#### A2.7.1 Intent

**Business objective.** Reads every inbound document through the OCR service and passes the text to classification.

**Problem.** Documents are in folders, shared drives and with couriers; originals go missing and evidence is rebuilt for each audit.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Fields extracted without review | Rising each month | Decision log and Workbench records | Monthly |

#### A2.7.2 Description

**Functional overview.** Reads every inbound document through the OCR service and passes the text to classification.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Run the OCR pipeline on inbound documents | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** the Workbench document hub

**Prerequisites.** None

#### A2.7.3 Business rules and structure

##### A2.7.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P5-007-1 | Change to a write-once legal document | MSG-P5-002 Legal documents cannot be changed. Add a new version instead. |
| VR-P5-007-2 | An original document is overdue back | MSG-P5-004 {document} is due back from {holder} since {date}. |
| BR-P5-007 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.7.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Platform administrator | Also uses |

#### A2.7.4 Acceptance criteria

##### A2.7.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P5-007-01 | Sample processed | the 180 synthetic sample documents, 30 of each of the six agreed types, in Thai and English, each as a CLEAN intake item | JOB-12 Document intake runs | each of the 180 items has ocr_status "DONE" or "RESCAN" and an ocr_ref to its JSON output And each page has a document_text row with the page text and its quality And the text of the sample pages holds Thai and English words, and the languages recorded per item are "th" and "en" where both appear | RWB-E1-049 |

##### A2.7.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P5-007-01 | Throughput | 500 pages in 125 CLEAN intake items in SIT | they are processed by JOB-12 with 4 workers | all 125 items reach "DONE" or "RESCAN" within 60 minutes of the first item starting | RWB-E1-049 |
| AC-ALT-P5-007-02 | Unreadable page on a known case | an uploaded court notice of 4 pages on case "RW-2026-000123" owned by user "TEST-CO-01" And page 3 has quality 0.41 and the other pages are above 0.70 | the OCR step runs | the intake item has ocr_status "RESCAN" and rescan_pages "3" And "TEST-CO-01" receives MSG-P5-018 naming page 3, the document and case "RW-2026-000123" | RWB-E1-049 |

##### A2.7.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P5-007-01 | Unreadable page with no case yet | a mailroom scan of 2 pages with no case and page 1 at quality 0.30 | the OCR step runs | the intake item has ocr_status "RESCAN", rescan_pages "1" and review_reason "RESCAN" And no notification is sent | RWB-E1-049 |
| AC-EXC-P5-007-02 | OCR service unavailable | the OCR service stub returns HTTP 503 for every call | JOB-12 runs twice | each pending item has ocr_status "PENDING" and ocr_attempts 2 And the job monitor shows the OCR step failed in both runs and an alert is raised to the platform administrator And when the service answers again the next run sets the items "DONE" | RWB-E1-049 |
| AC-EXC-P5-007-03 | File that cannot be read | a password-protected PDF as a CLEAN intake item | the OCR step runs | the item has ocr_status "FAILED" and review_reason "UNREADABLE_FILE" And no document_text row exists for it | RWB-E1-049 |
| AC-EXC-P5-007-04 | Repeat run | 10 intake items already "DONE" with 25 document_text rows | JOB-12 runs again | the OCR service receives no call for those items And they still have 25 document_text rows | RWB-E1-049 |
| AC-EXC-P5-007-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P5-007-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.7.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P5-007-01 | Document intake | Schedule | Every 15 minutes | Takes scans, SFTP files and emails into OCR | Documents on the case the same day | No document is lost between paths |

---

### A2.8 Classify a document into one of the six types

#### A2.8.1 Intent

**Business objective.** Types each read document against the six agreed types and records the classification confidence.

**Problem.** Documents are in folders, shared drives and with couriers; originals go missing and evidence is rebuilt for each audit.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Fields extracted without review | Rising each month | Decision log and Workbench records | Monthly |

#### A2.8.2 Description

**Functional overview.** Types each read document against the six agreed types and records the classification confidence.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Classify a document into one of the six types | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** the Workbench document hub

**Prerequisites.** FEAT-DCM-07, FEAT-DCM-03

#### A2.8.3 Business rules and structure

##### A2.8.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P5-008-1 | Change to a write-once legal document | MSG-P5-002 Legal documents cannot be changed. Add a new version instead. |
| VR-P5-008-2 | An original document is overdue back | MSG-P5-004 {document} is due back from {holder} since {date}. |
| BR-P5-008 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.8.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.8.4 Acceptance criteria

##### A2.8.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P5-008-01 | Accuracy | the labeled sample of 180 synthetic documents, 30 of each type, with ocr_status "DONE" | ClassificationEvaluationRunner runs on the sample | at least 162 of the 180 documents get the labeled type as predicted_type And the report "evaluation/classification/2026-11-20.json" holds the accuracy, the 6 by 6 confusion matrix and the model version | RWB-E1-050 |

##### A2.8.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P5-008-01 | Low confidence routed | a scanned intake item whose scores are COURT_NOTICE 0.62, DEMAND_LETTER 0.21 and the rest below 0.10 | classification runs | the item has predicted_type "COURT_NOTICE", classification_confidence 0.6200 and review_reason "LOW_CONFIDENCE" And type_candidates holds COURT_NOTICE 0.62 and DEMAND_LETTER 0.21 And the item is passed to attach marked for type review, with write_once to be set false on the stored document | RWB-E1-050 |
| AC-ALT-P5-008-02 | Score at the threshold | a scanned intake item whose top score is APPRAISAL_REPORT 0.80 | classification runs | the item is classified as "APPRAISAL_REPORT" with no review_reason | RWB-E1-050 |

##### A2.8.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P5-008-01 | Classifier does not answer | the classifier stub does not answer within 60 seconds | classification runs for one item | the item has review_reason "MODEL_UNAVAILABLE" and no predicted_type And the item records that the fallback was used | RWB-E1-050 |
| AC-EXC-P5-008-02 | Type not in the table | the classifier returns "LOAN_CONTRACT" 0.91 for an item | classification runs | the item has review_reason "UNKNOWN_TYPE" And type_candidates holds the two highest agreed types | RWB-E1-050 |
| AC-EXC-P5-008-03 | Repeat run | 20 items already classified | JOB-12 runs again | the classifier receives no call for those 20 items and their results are unchanged | RWB-E1-050 |
| AC-EXC-P5-008-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P5-008-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.8.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P5-008-01 | Document intake | Schedule | Every 15 minutes | Takes scans, SFTP files and emails into OCR | Documents on the case the same day | No document is lost between paths |

---

### A2.9 Extract fields from the six document types

#### A2.9.1 Intent

**Business objective.** Pulls the agreed fields out of each typed document and writes them into the index with a confidence score.

**Problem.** Documents are in folders, shared drives and with couriers; originals go missing and evidence is rebuilt for each audit.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Fields extracted without review | Rising each month | Decision log and Workbench records | Monthly |

#### A2.9.2 Description

**Functional overview.** Pulls the agreed fields out of each typed document and writes them into the index with a confidence score.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Extract fields from the six document types | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** the Workbench document hub

**Prerequisites.** FEAT-DCM-08

#### A2.9.3 Business rules and structure

##### A2.9.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P5-009-1 | Change to a write-once legal document | MSG-P5-002 Legal documents cannot be changed. Add a new version instead. |
| VR-P5-009-2 | An original document is overdue back | MSG-P5-004 {document} is due back from {holder} since {date}. |
| BR-P5-009 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.9.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.9.4 Acceptance criteria

##### A2.9.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P5-009-01 | Fields extracted | intake item "IN-0001" classified "COURT_NOTICE" with confidence 0.9400 And its OCR text holds court "Civil Court", black case number "Por 1234/2569", notice date "1 ธันวาคม 2569" and hearing date "15 ธันวาคม 2569" | extractStep runs | extracted_fields of "IN-0001" holds court_name "Civil Court" 0.9600, black_case_no "Por 1234/2569" 0.9100, notice_date "2026-12-01" 0.9000 and hearing_date "2026-12-15" 0.8800, each with state "OK" and extractor version "EXT-TPL-1.0" And extract_status is "DONE" And when matchStep stores the document on case "RW-2026-000123" the four fields are in the index and review_status is "NOT_NEEDED" | RWB-E1-053 |

##### A2.9.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P5-009-01 | Precision and recall | the labeled sample of 180 documents and the pass marks precision 0.90 and recall 0.90 per field | the extraction evaluation run processes the sample | the report lists precision and recall for each of the 26 fields with the extractor version And TITLE_DEED area_sq_wa with precision 0.84 is listed as "review-only" And the run writes a proposed DOCTYPE load file with review_only true for area_sq_wa only And the version in force does not change until the proposed version is loaded and approved | RWB-E1-053 |
| AC-ALT-P5-009-02 | A field below the threshold goes to review | intake item "IN-0002" classified "COURT_NOTICE" And the extractor returns hearing_date with confidence 0.6200 | extractStep runs | hearing_date has state "REVIEW" and the other three fields state "OK" And when the document is stored its review_status is "PENDING" and SCR-30 shows MSG-P5-003 | RWB-E1-053 |

##### A2.9.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P5-009-01 | A value that cannot be converted goes to review | the OCR text of item "IN-0005" holds hearing date "32 ธันวาคม 2569" | extractStep runs | hearing_date keeps the value "32 ธันวาคม 2569" with confidence 0.0000 and state "REVIEW" | RWB-E1-053 |
| AC-EXC-P5-009-02 | The extractor does not answer | the extractor does not answer within 60 seconds on 3 attempts for item "IN-0007" | extractStep runs | extract_status is "FAILED" and review_reason is "EXTRACTION_FAILED" And extracted_fields is empty And matchStep does not attach "IN-0007" | RWB-E1-053 |
| AC-EXC-P5-009-03 | A repeated run has no effect | item "IN-0001" has extract_status "DONE" | extractStep runs again | "IN-0001" is not read again and extracted_fields is unchanged | RWB-E1-053 |
| AC-EXC-P5-009-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P5-009-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.9.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P5-009-01 | Document intake | Schedule | Every 15 minutes | Takes scans, SFTP files and emails into OCR | Documents on the case the same day | No document is lost between paths |

---

### A2.10 Send a low-confidence extraction to the review queue

#### A2.10.1 Intent

**Business objective.** Routes any extraction below the confidence threshold to a person instead of writing it to the case.

**Problem.** Documents are in folders, shared drives and with couriers; originals go missing and evidence is rebuilt for each audit.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Fields extracted without review | Rising each month | Decision log and Workbench records | Monthly |

#### A2.10.2 Description

**Functional overview.** Routes any extraction below the confidence threshold to a person instead of writing it to the case.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Send a low-confidence extraction to the review queue | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-DCM-09

#### A2.10.3 Business rules and structure

##### A2.10.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P5-010-1 | Change to a write-once legal document | MSG-P5-002 Legal documents cannot be changed. Add a new version instead. |
| BR-P5-010 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.10.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.10.4 Acceptance criteria

##### A2.10.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P5-010-01 | Queued | intake item "IN-0101" on which classification returned "COURT_NOTICE" 0.6200 and "DEMAND_LETTER" 0.2100 And its review_reason is "LOW_CONFIDENCE" | the officer opens SCR-31 | "IN-0101" is listed with reason "LOW_CONFIDENCE" and the candidates "COURT_NOTICE 0.62" and "DEMAND_LETTER 0.21" | RWB-E1-054 |

##### A2.10.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P5-010-01 | Corrected | intake item "IN-0101" in the review queue with hearing_date "2026-12-15" in state "REVIEW" | the officer sets type "COURT_NOTICE", corrects hearing_date to "2026-12-16", confirms the other fields, chooses case "RW-2026-000201" and chooses Attach | a document is stored on "RW-2026-000201" with type "COURT_NOTICE" and hearing_date field_value "2026-12-16", extracted_value "2026-12-15", state "CORRECTED" and confirmed_by the officer's user ID And the document review_status is "CORRECTED" and "IN-0101" has review_outcome "ATTACHED" And one DOCATT decision log entry is written by the store And LabeledSetReader returns "IN-0101" with predicted type, confirmed type, extracted value and corrected value | RWB-E1-054 |
| AC-ALT-P5-010-02 | A stored document with a field to check | document "DOC-0103" on case "RW-2026-000202" has black_case_no "Por 2001/2569" in state "REVIEW" and review_status "PENDING" | the officer chooses Confirm on black_case_no and completes the review | black_case_no has state "CONFIRMED" and confirmed_by the officer's user ID And the document review_status is "CONFIRMED" | RWB-E1-054 |

##### A2.10.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P5-010-01 | An empty correction is refused | document "DOC-0103" has court_name in state "REVIEW" | the officer chooses Correct on court_name with an empty value | the response is 422 with MSG-GEN-001 naming "Court name" And court_name is unchanged | RWB-E1-054 |
| AC-EXC-P5-010-02 | A type not in the list is refused | intake item "IN-0104" in the review queue | the officer sets the type to "PAYSLIP" | the response is 422 with MSG-P5-006 naming "PAYSLIP" | RWB-E1-054 |
| AC-EXC-P5-010-03 | A date outside the allowed range is refused | REVIEW_DATE_MIN is 2000-01-01 and REVIEW_DATE_MAX is 2100-12-31 | the officer corrects hearing_date on "IN-0101" to "2569-12-16" | the response is 422 with MSG-GEN-002 naming "Hearing date", "2000-01-01" and "2100-12-31" | RWB-E1-054 |
| AC-EXC-P5-010-04 | Attach with a field still in review is refused | intake item "IN-0105" has two fields in state "REVIEW" and the officer has confirmed one | the officer chooses Attach | the response is 422 with MSG-GEN-001 naming the field still in review And no document is stored | RWB-E1-054 |
| AC-EXC-P5-010-05 | A closed case is refused | intake item "IN-0106" with review_reason "CASE_CLOSED" and candidate case "RW-2026-000150" with status "Closed" | the officer chooses case "RW-2026-000150" and chooses Attach | the response is 422 with MSG-P5-005 naming "RW-2026-000150" And no document is stored | RWB-E1-054 |
| AC-EXC-P5-010-06 | Discard without a reason is refused | intake item "IN-0112" with review_reason "RESCAN" | the officer chooses Discard with an empty reason | the response is 422 with MSG-GEN-001 naming "Reason" And "IN-0112" stays in the queue | RWB-E1-054 |
| AC-EXC-P5-010-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P5-010-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.10.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P5-010-01 | Document intake | Schedule | Every 15 minutes | Takes scans, SFTP files and emails into OCR | Documents on the case the same day | No document is lost between paths |

---

### A2.11 Check a low-confidence extraction

#### A2.11.1 Intent

**Business objective.** Lets a person confirm or correct the extracted fields, which also feeds the extraction evaluation.

**Problem.** Documents are in folders, shared drives and with couriers; originals go missing and evidence is rebuilt for each audit.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Fields extracted without review | Rising each month | Decision log and Workbench records | Monthly |

#### A2.11.2 Description

**Functional overview.** Lets a person confirm or correct the extracted fields, which also feeds the extraction evaluation.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Case owner | Opens the screen and check a low-confidence extraction | Checks the role, the capability area and the scope |
| 2 | Case owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-DCM-10

#### A2.11.3 Business rules and structure

##### A2.11.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P5-011-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P5-011 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.11.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| document.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| document.party_id | The party this record belongs to | uuid | No | None | No |
| document.document_type | Type from the document checklist | varchar(30) | Yes | LOV-DOC-TYPE | No |
| document.source | Scan, upload, generated, partner, email | varchar(12) | Yes | LOV-DOC-SOURCE | No |
| document.storage_ref | Reference to the stored file | varchar(400) | Yes | None | No |
| document.classification_confidence | OCR classification confidence | numeric(5,4) | No | None | No |
| document.review_status | Not needed, pending, confirmed, corrected | varchar(12) | Yes | LOV-REVIEW | No |
| document.retention_class | Retention class | varchar(10) | Yes | LOV-RETENTION | No |

##### A2.11.3.3 Roles and permissions

| Role | Use |
|---|---|
| Case owner | Primary |
| Center of excellence analyst | Also uses |

#### A2.11.4 Acceptance criteria

##### A2.11.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P5-011-01 | Queued | intake item "IN-0101" on which classification returned "COURT_NOTICE" 0.6200 and "DEMAND_LETTER" 0.2100 And its review_reason is "LOW_CONFIDENCE" | the officer opens SCR-31 | "IN-0101" is listed with reason "LOW_CONFIDENCE" and the candidates "COURT_NOTICE 0.62" and "DEMAND_LETTER 0.21" | RWB-E1-054 |

##### A2.11.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P5-011-01 | Corrected | intake item "IN-0101" in the review queue with hearing_date "2026-12-15" in state "REVIEW" | the officer sets type "COURT_NOTICE", corrects hearing_date to "2026-12-16", confirms the other fields, chooses case "RW-2026-000201" and chooses Attach | a document is stored on "RW-2026-000201" with type "COURT_NOTICE" and hearing_date field_value "2026-12-16", extracted_value "2026-12-15", state "CORRECTED" and confirmed_by the officer's user ID And the document review_status is "CORRECTED" and "IN-0101" has review_outcome "ATTACHED" And one DOCATT decision log entry is written by the store And LabeledSetReader returns "IN-0101" with predicted type, confirmed type, extracted value and corrected value | RWB-E1-054 |
| AC-ALT-P5-011-02 | A stored document with a field to check | document "DOC-0103" on case "RW-2026-000202" has black_case_no "Por 2001/2569" in state "REVIEW" and review_status "PENDING" | the officer chooses Confirm on black_case_no and completes the review | black_case_no has state "CONFIRMED" and confirmed_by the officer's user ID And the document review_status is "CONFIRMED" | RWB-E1-054 |

##### A2.11.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P5-011-01 | An empty correction is refused | document "DOC-0103" has court_name in state "REVIEW" | the officer chooses Correct on court_name with an empty value | the response is 422 with MSG-GEN-001 naming "Court name" And court_name is unchanged | RWB-E1-054 |
| AC-EXC-P5-011-02 | A type not in the list is refused | intake item "IN-0104" in the review queue | the officer sets the type to "PAYSLIP" | the response is 422 with MSG-P5-006 naming "PAYSLIP" | RWB-E1-054 |
| AC-EXC-P5-011-03 | A date outside the allowed range is refused | REVIEW_DATE_MIN is 2000-01-01 and REVIEW_DATE_MAX is 2100-12-31 | the officer corrects hearing_date on "IN-0101" to "2569-12-16" | the response is 422 with MSG-GEN-002 naming "Hearing date", "2000-01-01" and "2100-12-31" | RWB-E1-054 |
| AC-EXC-P5-011-04 | Attach with a field still in review is refused | intake item "IN-0105" has two fields in state "REVIEW" and the officer has confirmed one | the officer chooses Attach | the response is 422 with MSG-GEN-001 naming the field still in review And no document is stored | RWB-E1-054 |
| AC-EXC-P5-011-05 | A closed case is refused | intake item "IN-0106" with review_reason "CASE_CLOSED" and candidate case "RW-2026-000150" with status "Closed" | the officer chooses case "RW-2026-000150" and chooses Attach | the response is 422 with MSG-P5-005 naming "RW-2026-000150" And no document is stored | RWB-E1-054 |
| AC-EXC-P5-011-06 | Discard without a reason is refused | intake item "IN-0112" with review_reason "RESCAN" | the officer chooses Discard with an empty reason | the response is 422 with MSG-GEN-001 naming "Reason" And "IN-0112" stays in the queue | RWB-E1-054 |
| AC-EXC-P5-011-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P5-011-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.11.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P5-011-01 | Document intake | Schedule | Every 15 minutes | Takes scans, SFTP files and emails into OCR | Documents on the case the same day | No document is lost between paths |

---

### A2.12 Attach an OCR-read document to its case automatically

#### A2.12.1 Intent

**Business objective.** Matches a read document to its case and attaches it with no person involved.

**Problem.** Documents are in folders, shared drives and with couriers; originals go missing and evidence is rebuilt for each audit.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Fields extracted without review | Rising each month | Decision log and Workbench records | Monthly |

#### A2.12.2 Description

**Functional overview.** Matches a read document to its case and attaches it with no person involved.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Attach an OCR-read document to its case automatically | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, the Workbench document hub

**Prerequisites.** FEAT-DCM-09

#### A2.12.3 Business rules and structure

##### A2.12.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P5-012-1 | Change to a write-once legal document | MSG-P5-002 Legal documents cannot be changed. Add a new version instead. |
| VR-P5-012-2 | An original document is overdue back | MSG-P5-004 {document} is due back from {holder} since {date}. |
| BR-P5-012 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.12.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.12.4 Acceptance criteria

##### A2.12.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P5-012-01 | Auto attach | a scanned notice with the case ID "RW-2026-000123" read by OCR, classified "COURT_NOTICE" at 0.93 by classifier version "CLS-1.0" | intake completes | the document is stored on case "RW-2026-000123" with type "COURT_NOTICE", source "SCAN", classification_confidence 0.9300 and review_status "NOT_NEEDED" without a person And one decision log entry "DOCATT" holds model version "CLS-1.0", confidence 0.93 and match method "CASE_ID" And DocumentStored is written and the intake item has match_status "MATCHED" and the document ID | RWB-E1-032 |

##### A2.12.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P5-012-01 | Two candidates | a scan whose account number "TEST-ACC-0003" is linked to open cases "RW-2026-000321" and "RW-2026-000654" | intake completes | the intake item has match_status "MULTIPLE" And candidate_case_ids holds both cases and the Unmatched list on SCR-31 offers both And no document row is written | RWB-E1-032 |
| AC-ALT-P5-012-02 | Match by account number | a scan with no case ID and the account number "TEST-ACC-0002", classified "DEMAND_LETTER" at 0.88 | intake completes | the document is stored on case "RW-2026-000456" And the decision log entry holds match method "ACCOUNT_NO" | RWB-E1-032 |

##### A2.12.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P5-012-01 | No match | a scan with no readable case ID and no readable account number | intake completes | the intake item has match_status "NO_MATCH" And GET /intake-items/{intakeItemId} returns its OCR text pages And no document row is written | RWB-E1-032 |
| AC-EXC-P5-012-02 | Case ID that does not exist | a scan with the case ID "RW-2026-999999" and no account number | intake completes | the intake item has match_status "NO_MATCH" | RWB-E1-032 |
| AC-EXC-P5-012-03 | Repeat run | 15 intake items already "MATCHED" | JOB-12 runs again | no further document row, decision log entry or DocumentStored event is written for them | RWB-E1-032 |
| AC-EXC-P5-012-04 | No agreed type | a scan with the case ID "RW-2026-000123" and review_reason "UNKNOWN_TYPE" from classification | intake completes | the intake item has match_status "NO_TYPE" with candidate "RW-2026-000123" | RWB-E1-032 |
| AC-EXC-P5-012-05 | Reviewer picks a type not in force | the item from AC2 and a reviewer with scope ALL | the reviewer attaches it to "RW-2026-000123" with type "PAYSLIP" | the request is refused with 422 and MSG-P5-006 naming "PAYSLIP" | RWB-E1-032 |
| AC-EXC-P5-012-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P5-012-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.12.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P5-012-01 | Document intake | Schedule | Every 15 minutes | Takes scans, SFTP files and emails into OCR | Documents on the case the same day | No document is lost between paths |

---

### A2.13 Take intake from branches and the mailroom

#### A2.13.1 Intent

**Business objective.** Accepts scanned documents from branch and mailroom scanning into the OCR pipeline.

**Problem.** Documents are in folders, shared drives and with couriers; originals go missing and evidence is rebuilt for each audit.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Fields extracted without review | Rising each month | Decision log and Workbench records | Monthly |

#### A2.13.2 Description

**Functional overview.** Accepts scanned documents from branch and mailroom scanning into the OCR pipeline.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Take intake from branches and the mailroom | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** the Workbench document hub

**Prerequisites.** FEAT-DCM-07

#### A2.13.3 Business rules and structure

##### A2.13.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P5-013-1 | Change to a write-once legal document | MSG-P5-002 Legal documents cannot be changed. Add a new version instead. |
| BR-P5-013 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.13.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Platform administrator | Also uses |

#### A2.13.4 Acceptance criteria

##### A2.13.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P5-013-01 | Branch scan | file "scan-0001.pdf" of 1.2 MB in the scanner folder of branch "BR-0123", created by the scanner at 2026-11-30 09:12 | the intake job runs at 09:15 | one document_intake row has source "SCAN", channel_code "BR-0123", captured_at 2026-11-30 09:12 and an empty scan_result And the file is in the intake container at the row's intake_ref And the file is no longer in the scanner folder and is in its processed folder | RWB-E1-057 |

##### A2.13.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P5-013-01 | Partner SFTP | file "LF-007-notice-0001.pdf" in the SFTP inbound subfolder "LF-007" | the job runs | one document_intake row has source "PARTNER", channel_code "LF-007" and partner_id of partner "LF-007" | RWB-E1-057 |
| AC-ALT-P5-013-02 | Mailbox | an email to recovery mailbox "MBX-RECOVERY-01" with one PDF attachment "reply-0001.pdf" | the job runs | one document_intake row has source "EMAIL", channel_code "MBX-RECOVERY-01" and the sender address recorded And the sender address is masked in every response and absent from the job record and the logs And the email is in the archive folder of "MBX-RECOVERY-01" | RWB-E1-057 |

##### A2.13.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P5-013-01 | A file type not allowed is refused | file "letter-0002.docx" in the scanner folder of branch "BR-0123" | the job runs | no document_intake row is written for it And the file is in the rejected folder of branch "BR-0123" And the job record shows 1 refused on "BR-0123" with MSG-P5-007 and reason MSG-P5-001 | RWB-E1-057 |
| AC-EXC-P5-013-02 | A file above the size limit is refused | file "scan-0003.pdf" of 25.1 MB and file "scan-0004.pdf" of 25.0 MB in the scanner folder of branch "BR-0123" | the job runs | "scan-0003.pdf" is refused with reason MSG-P5-017 and moved to the rejected folder And "scan-0004.pdf" has a document_intake row | RWB-E1-057 |
| AC-EXC-P5-013-03 | An unknown or suspended partner is refused | file "notice-0005.pdf" in the SFTP subfolder "LF-099", which is no partner_code And file "notice-0006.pdf" in the SFTP subfolder "LF-008", a partner with panel_status "SUSPENDED" | the job runs | no document_intake row is written for either file And the job record shows MSG-P5-007 with reasons "PARTNER_UNKNOWN" and "PARTNER_NOT_ACTIVE" | RWB-E1-057 |
| AC-EXC-P5-013-04 | A duplicate file is not taken in twice | file "scan-0001.pdf" with hash "H1" from branch "BR-0123" was taken in on 30 November | the same file arrives again from branch "BR-0123" on 2 December | no second document_intake row is written And the file is moved to the processed folder and counted as a duplicate | RWB-E1-057 |
| AC-EXC-P5-013-05 | The intake container does not accept writes | the intake container refuses writes | the job runs with file "scan-0007.pdf" in the folder of branch "BR-0123" | no document_intake row is written And "scan-0007.pdf" stays in the scanner folder And on the next run with the container available the file is taken in | RWB-E1-057 |
| AC-EXC-P5-013-06 | Two failed runs raise an alert | the run at 10:00 failed because the SFTP inbound folder could not be read | the run at 10:15 fails for the same reason | the platform administrator receives MSG-P5-008 naming "PARTNER_SFTP" And the run at 10:30 tries again | RWB-E1-057 |
| AC-EXC-P5-013-07 | An email with no usable attachment | an email to "MBX-RECOVERY-01" with no attachment And an email with only a 6 KB signature image | the job runs | no document_intake row is written for either email And both emails are in the archive folder | RWB-E1-057 |
| AC-EXC-P5-013-08 | A file seen again after a failed move | file "scan-0008.pdf" was taken in at 11:00 and the move to the processed folder failed | the run at 11:15 sees "scan-0008.pdf" again | no second document_intake row is written And the file is moved to the processed folder | RWB-E1-057 |
| AC-EXC-P5-013-09 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P5-013-10 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.13.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P5-013-01 | Document intake | Schedule | Every 15 minutes | Takes scans, SFTP files and emails into OCR | Documents on the case the same day | No document is lost between paths |

---

### A2.14 Take intake from partner SFTP

#### A2.14.1 Intent

**Business objective.** Accepts partner document files over SFTP into the same OCR and indexing path.

**Problem.** Documents are in folders, shared drives and with couriers; originals go missing and evidence is rebuilt for each audit.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Fields extracted without review | Rising each month | Decision log and Workbench records | Monthly |

#### A2.14.2 Description

**Functional overview.** Accepts partner document files over SFTP into the same OCR and indexing path.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Take intake from partner SFTP | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** SFTP, the Workbench document hub

**Prerequisites.** FEAT-DCM-07

#### A2.14.3 Business rules and structure

##### A2.14.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P5-014-1 | Change to a write-once legal document | MSG-P5-002 Legal documents cannot be changed. Add a new version instead. |
| VR-P5-014-2 | An original document is overdue back | MSG-P5-004 {document} is due back from {holder} since {date}. |
| BR-P5-014 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.14.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Partner and agency manager | Also uses |

#### A2.14.4 Acceptance criteria

##### A2.14.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P5-014-01 | Branch scan | file "scan-0001.pdf" of 1.2 MB in the scanner folder of branch "BR-0123", created by the scanner at 2026-11-30 09:12 | the intake job runs at 09:15 | one document_intake row has source "SCAN", channel_code "BR-0123", captured_at 2026-11-30 09:12 and an empty scan_result And the file is in the intake container at the row's intake_ref And the file is no longer in the scanner folder and is in its processed folder | RWB-E1-057 |

##### A2.14.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P5-014-01 | Partner SFTP | file "LF-007-notice-0001.pdf" in the SFTP inbound subfolder "LF-007" | the job runs | one document_intake row has source "PARTNER", channel_code "LF-007" and partner_id of partner "LF-007" | RWB-E1-057 |
| AC-ALT-P5-014-02 | Mailbox | an email to recovery mailbox "MBX-RECOVERY-01" with one PDF attachment "reply-0001.pdf" | the job runs | one document_intake row has source "EMAIL", channel_code "MBX-RECOVERY-01" and the sender address recorded And the sender address is masked in every response and absent from the job record and the logs And the email is in the archive folder of "MBX-RECOVERY-01" | RWB-E1-057 |

##### A2.14.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P5-014-01 | A file type not allowed is refused | file "letter-0002.docx" in the scanner folder of branch "BR-0123" | the job runs | no document_intake row is written for it And the file is in the rejected folder of branch "BR-0123" And the job record shows 1 refused on "BR-0123" with MSG-P5-007 and reason MSG-P5-001 | RWB-E1-057 |
| AC-EXC-P5-014-02 | A file above the size limit is refused | file "scan-0003.pdf" of 25.1 MB and file "scan-0004.pdf" of 25.0 MB in the scanner folder of branch "BR-0123" | the job runs | "scan-0003.pdf" is refused with reason MSG-P5-017 and moved to the rejected folder And "scan-0004.pdf" has a document_intake row | RWB-E1-057 |
| AC-EXC-P5-014-03 | An unknown or suspended partner is refused | file "notice-0005.pdf" in the SFTP subfolder "LF-099", which is no partner_code And file "notice-0006.pdf" in the SFTP subfolder "LF-008", a partner with panel_status "SUSPENDED" | the job runs | no document_intake row is written for either file And the job record shows MSG-P5-007 with reasons "PARTNER_UNKNOWN" and "PARTNER_NOT_ACTIVE" | RWB-E1-057 |
| AC-EXC-P5-014-04 | A duplicate file is not taken in twice | file "scan-0001.pdf" with hash "H1" from branch "BR-0123" was taken in on 30 November | the same file arrives again from branch "BR-0123" on 2 December | no second document_intake row is written And the file is moved to the processed folder and counted as a duplicate | RWB-E1-057 |
| AC-EXC-P5-014-05 | The intake container does not accept writes | the intake container refuses writes | the job runs with file "scan-0007.pdf" in the folder of branch "BR-0123" | no document_intake row is written And "scan-0007.pdf" stays in the scanner folder And on the next run with the container available the file is taken in | RWB-E1-057 |
| AC-EXC-P5-014-06 | Two failed runs raise an alert | the run at 10:00 failed because the SFTP inbound folder could not be read | the run at 10:15 fails for the same reason | the platform administrator receives MSG-P5-008 naming "PARTNER_SFTP" And the run at 10:30 tries again | RWB-E1-057 |
| AC-EXC-P5-014-07 | An email with no usable attachment | an email to "MBX-RECOVERY-01" with no attachment And an email with only a 6 KB signature image | the job runs | no document_intake row is written for either email And both emails are in the archive folder | RWB-E1-057 |
| AC-EXC-P5-014-08 | A file seen again after a failed move | file "scan-0008.pdf" was taken in at 11:00 and the move to the processed folder failed | the run at 11:15 sees "scan-0008.pdf" again | no second document_intake row is written And the file is moved to the processed folder | RWB-E1-057 |
| AC-EXC-P5-014-09 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P5-014-10 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.14.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P5-014-01 | Document intake | Schedule | Every 15 minutes | Takes scans, SFTP files and emails into OCR | Documents on the case the same day | No document is lost between paths |

---

### A2.15 Take intake from email

#### A2.15.1 Intent

**Business objective.** Accepts documents arriving by email into the OCR and indexing path, which replaces email hand-offs.

**Problem.** Documents are in folders, shared drives and with couriers; originals go missing and evidence is rebuilt for each audit.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Fields extracted without review | Rising each month | Decision log and Workbench records | Monthly |

#### A2.15.2 Description

**Functional overview.** Accepts documents arriving by email into the OCR and indexing path, which replaces email hand-offs.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Take intake from email | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** the Workbench document hub

**Prerequisites.** FEAT-DCM-07

#### A2.15.3 Business rules and structure

##### A2.15.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P5-015-1 | Change to a write-once legal document | MSG-P5-002 Legal documents cannot be changed. Add a new version instead. |
| BR-P5-015 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.15.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.15.4 Acceptance criteria

##### A2.15.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P5-015-01 | Branch scan | file "scan-0001.pdf" of 1.2 MB in the scanner folder of branch "BR-0123", created by the scanner at 2026-11-30 09:12 | the intake job runs at 09:15 | one document_intake row has source "SCAN", channel_code "BR-0123", captured_at 2026-11-30 09:12 and an empty scan_result And the file is in the intake container at the row's intake_ref And the file is no longer in the scanner folder and is in its processed folder | RWB-E1-057 |

##### A2.15.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P5-015-01 | Partner SFTP | file "LF-007-notice-0001.pdf" in the SFTP inbound subfolder "LF-007" | the job runs | one document_intake row has source "PARTNER", channel_code "LF-007" and partner_id of partner "LF-007" | RWB-E1-057 |
| AC-ALT-P5-015-02 | Mailbox | an email to recovery mailbox "MBX-RECOVERY-01" with one PDF attachment "reply-0001.pdf" | the job runs | one document_intake row has source "EMAIL", channel_code "MBX-RECOVERY-01" and the sender address recorded And the sender address is masked in every response and absent from the job record and the logs And the email is in the archive folder of "MBX-RECOVERY-01" | RWB-E1-057 |

##### A2.15.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P5-015-01 | A file type not allowed is refused | file "letter-0002.docx" in the scanner folder of branch "BR-0123" | the job runs | no document_intake row is written for it And the file is in the rejected folder of branch "BR-0123" And the job record shows 1 refused on "BR-0123" with MSG-P5-007 and reason MSG-P5-001 | RWB-E1-057 |
| AC-EXC-P5-015-02 | A file above the size limit is refused | file "scan-0003.pdf" of 25.1 MB and file "scan-0004.pdf" of 25.0 MB in the scanner folder of branch "BR-0123" | the job runs | "scan-0003.pdf" is refused with reason MSG-P5-017 and moved to the rejected folder And "scan-0004.pdf" has a document_intake row | RWB-E1-057 |
| AC-EXC-P5-015-03 | An unknown or suspended partner is refused | file "notice-0005.pdf" in the SFTP subfolder "LF-099", which is no partner_code And file "notice-0006.pdf" in the SFTP subfolder "LF-008", a partner with panel_status "SUSPENDED" | the job runs | no document_intake row is written for either file And the job record shows MSG-P5-007 with reasons "PARTNER_UNKNOWN" and "PARTNER_NOT_ACTIVE" | RWB-E1-057 |
| AC-EXC-P5-015-04 | A duplicate file is not taken in twice | file "scan-0001.pdf" with hash "H1" from branch "BR-0123" was taken in on 30 November | the same file arrives again from branch "BR-0123" on 2 December | no second document_intake row is written And the file is moved to the processed folder and counted as a duplicate | RWB-E1-057 |
| AC-EXC-P5-015-05 | The intake container does not accept writes | the intake container refuses writes | the job runs with file "scan-0007.pdf" in the folder of branch "BR-0123" | no document_intake row is written And "scan-0007.pdf" stays in the scanner folder And on the next run with the container available the file is taken in | RWB-E1-057 |
| AC-EXC-P5-015-06 | Two failed runs raise an alert | the run at 10:00 failed because the SFTP inbound folder could not be read | the run at 10:15 fails for the same reason | the platform administrator receives MSG-P5-008 naming "PARTNER_SFTP" And the run at 10:30 tries again | RWB-E1-057 |
| AC-EXC-P5-015-07 | An email with no usable attachment | an email to "MBX-RECOVERY-01" with no attachment And an email with only a 6 KB signature image | the job runs | no document_intake row is written for either email And both emails are in the archive folder | RWB-E1-057 |
| AC-EXC-P5-015-08 | A file seen again after a failed move | file "scan-0008.pdf" was taken in at 11:00 and the move to the processed folder failed | the run at 11:15 sees "scan-0008.pdf" again | no second document_intake row is written And the file is moved to the processed folder | RWB-E1-057 |
| AC-EXC-P5-015-09 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P5-015-10 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.15.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P5-015-01 | Document intake | Schedule | Every 15 minutes | Takes scans, SFTP files and emails into OCR | Documents on the case the same day | No document is lost between paths |

---

### A2.16 Hold the document checklist per case type as reference data

#### A2.16.1 Intent

**Business objective.** Keeps the list of documents each case type needs, so completeness is checked against data rather than memory.

**Problem.** Documents are in folders, shared drives and with couriers; originals go missing and evidence is rebuilt for each audit.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Fields extracted without review | Rising each month | Decision log and Workbench records | Monthly |

#### A2.16.2 Description

**Functional overview.** Keeps the list of documents each case type needs, so completeness is checked against data rather than memory.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Reference data administrator | Opens the screen and hold the document checklist per case type as reference data | Checks the role, the capability area and the scope |
| 2 | Reference data administrator | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-CWC-23

#### A2.16.3 Business rules and structure

##### A2.16.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P5-016-1 | Change to a write-once legal document | MSG-P5-002 Legal documents cannot be changed. Add a new version instead. |
| VR-P5-016-2 | An original document is overdue back | MSG-P5-004 {document} is due back from {holder} since {date}. |
| BR-P5-016 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.16.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| document.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| document.party_id | The party this record belongs to | uuid | No | None | No |
| document.document_type | Type from the document checklist | varchar(30) | Yes | LOV-DOC-TYPE | No |
| document.source | Scan, upload, generated, partner, email | varchar(12) | Yes | LOV-DOC-SOURCE | No |
| document.storage_ref | Reference to the stored file | varchar(400) | Yes | None | No |
| document.classification_confidence | OCR classification confidence | numeric(5,4) | No | None | No |
| document.review_status | Not needed, pending, confirmed, corrected | varchar(12) | Yes | LOV-REVIEW | No |
| document.retention_class | Retention class | varchar(10) | Yes | LOV-RETENTION | No |

##### A2.16.3.3 Roles and permissions

| Role | Use |
|---|---|
| Reference data administrator | Primary |
| Legal counsel, Litigation officer | Also uses |

#### A2.16.4 Acceptance criteria

##### A2.16.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P5-016-01 | Checklist by type | case "RW-2026-000123" at stage "LITIGATION" holds a demand letter and a court notice | the litigation officer opens the Documents tab | the checklist shows the 4 items from version "CHK-2026.11" for "LITIGATION" And DEMAND_LETTER and COURT_NOTICE are marked present And TITLE_DEED and APPRAISAL_REPORT are marked missing | RWB-E1-040 |

##### A2.16.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P5-016-01 | Change as data | version "CHK-2026.12" adds GUARANTOR_NOTICE for "DEED_IN_LIEU" and is approved with valid from 1 December 2026 | case "RW-2026-000456" at stage "DEED_IN_LIEU" is opened on 1 December 2026 | the checklist shows 4 items including GUARANTOR_NOTICE And no code was deployed between 30 November and 1 December 2026 | RWB-E1-040 |
| AC-ALT-P5-016-02 | Completeness flag | case "RW-2026-000456" at stage "DEED_IN_LIEU" holds a title deed and an appraisal report | the pack check runs after the appraisal report is stored | case_document_check for the case has complete false, missing count 1 and missing type SETTLEMENT_AGREEMENT And the case owner sees "1 missing" for the case on the case list | RWB-E1-040 |

##### A2.16.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P5-016-01 | The missing document arrives | the case from AC3 with SETTLEMENT_AGREEMENT missing | a settlement agreement is stored on the case | case_document_check has complete true and missing count 0 And the case list shows no missing documents for the case | RWB-E1-040 |
| AC-EXC-P5-016-02 | No checklist for the stage | case "RW-2026-000321" at stage "DEBT_SALE" and no rows for "DEBT_SALE" | the Documents tab opens | the checklist shows "No checklist for this case type" And case_document_check has complete empty and missing count 0 | RWB-E1-040 |
| AC-EXC-P5-016-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P5-016-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.16.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P5-016-01 | Document intake | Schedule | Every 15 minutes | Takes scans, SFTP files and emails into OCR | Documents on the case the same day | No document is lost between paths |

---

### A2.17 Apply retention classes to stored documents

#### A2.17.1 Intent

**Business objective.** Sets the retention class on each document type and applies it through the document life.

**Problem.** Documents are in folders, shared drives and with couriers; originals go missing and evidence is rebuilt for each audit.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Fields extracted without review | Rising each month | Decision log and Workbench records | Monthly |

#### A2.17.2 Description

**Functional overview.** Sets the retention class on each document type and applies it through the document life.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Compliance and PDPA officer | Opens the screen and apply retention classes to stored documents | Checks the role, the capability area and the scope |
| 2 | Compliance and PDPA officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Blob storage, the Workbench document hub

**Prerequisites.** FEAT-DCM-01

#### A2.17.3 Business rules and structure

##### A2.17.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P5-017-1 | Upload of a file type not allowed | MSG-P5-001 This file type cannot be stored. Use PDF, JPG or PNG. |
| VR-P5-017-2 | Change to a write-once legal document | MSG-P5-002 Legal documents cannot be changed. Add a new version instead. |
| VR-P5-017-3 | An original document is overdue back | MSG-P5-004 {document} is due back from {holder} since {date}. |
| BR-P5-017 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.17.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| document.case_id | The recovery_case this record belongs to | uuid | Yes | None | No |
| document.party_id | The party this record belongs to | uuid | No | None | No |
| document.document_type | Type from the document checklist | varchar(30) | Yes | LOV-DOC-TYPE | No |
| document.source | Scan, upload, generated, partner, email | varchar(12) | Yes | LOV-DOC-SOURCE | No |
| document.storage_ref | Reference to the stored file | varchar(400) | Yes | None | No |
| document.classification_confidence | OCR classification confidence | numeric(5,4) | No | None | No |
| document.review_status | Not needed, pending, confirmed, corrected | varchar(12) | Yes | LOV-REVIEW | No |
| document.retention_class | Retention class | varchar(10) | Yes | LOV-RETENTION | No |

##### A2.17.3.3 Roles and permissions

| Role | Use |
|---|---|
| Compliance and PDPA officer | Primary |
| Legal counsel | Also uses |

#### A2.17.4 Acceptance criteria

##### A2.17.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P5-017-01 | Malware blocked | a test file "eicar-0002.pdf" with the EICAR signature as an intake item from a branch scanner | JOB-12 runs the scan step | the item has scan_result "INFECTED" and the file is in the quarantine container And no document row exists for the file and the OCR step does not read it And the audit event "MALWARE_BLOCKED" is written with the intake ID and the source, and the platform administrator is alerted | RWB-E1-041 |

##### A2.17.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P5-017-01 | Retention class | a demand letter of type "DEMAND_LETTER" with class "LEGAL10Y" in the type table | the document is stored on case "RW-2026-000123" | the document row carries retention class "LEGAL10Y" and write_once true And the file is in the write-once container | RWB-E1-041 |
| AC-ALT-P5-017-02 | Expiry with end action archive | an appraisal report of class "GENERAL05Y" stored on 1 November 2021 on case "RW-2026-000123" with no legal hold | JOB-17 runs on 6 December 2026 | the document has state "ARCHIVED" and its blob is in the archive tier And one decision log entry "DOCRET" names the document, class "GENERAL05Y", version "RET-2026.11" and expiry date 1 November 2026 | RWB-E1-041 |

##### A2.17.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P5-017-01 | Scanning service unavailable | the scanning service stub returns no answer | JOB-12 runs twice with 3 unscanned intake items | the 3 items have no scan_result and the OCR step reads none of them And the platform administrator is alerted after the second run And an upload during the outage returns 503 with MSG-P5-022 and no document row or blob is written | RWB-E1-041 |
| AC-EXC-P5-017-02 | Class not in the retention table | a document with retention class "OLD03Y" that is not in version "RET-2026.11" | JOB-17 runs | the document is listed as exception "RETENTION_CLASS_MISSING" in the review list And the document is unchanged | RWB-E1-041 |
| AC-EXC-P5-017-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P5-017-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.17.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P5-017-01 | Document intake | Schedule | Every 15 minutes | Takes scans, SFTP files and emails into OCR | Documents on the case the same day | No document is lost between paths |

---

### A2.18 Virus scan every document on intake

#### A2.18.1 Intent

**Business objective.** Scans every inbound document before it is stored, and quarantines anything that fails.

**Problem.** Documents are in folders, shared drives and with couriers; originals go missing and evidence is rebuilt for each audit.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Fields extracted without review | Rising each month | Decision log and Workbench records | Monthly |

#### A2.18.2 Description

**Functional overview.** Scans every inbound document before it is stored, and quarantines anything that fails.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Virus scan every document on intake | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Blob storage

**Prerequisites.** FEAT-DCM-01

#### A2.18.3 Business rules and structure

##### A2.18.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P5-018-1 | Upload of a file type not allowed | MSG-P5-001 This file type cannot be stored. Use PDF, JPG or PNG. |
| VR-P5-018-2 | Change to a write-once legal document | MSG-P5-002 Legal documents cannot be changed. Add a new version instead. |
| VR-P5-018-3 | An original document is overdue back | MSG-P5-004 {document} is due back from {holder} since {date}. |
| BR-P5-018 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.18.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Platform administrator | Also uses |

#### A2.18.4 Acceptance criteria

##### A2.18.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P5-018-01 | Malware blocked | a test file "eicar-0002.pdf" with the EICAR signature as an intake item from a branch scanner | JOB-12 runs the scan step | the item has scan_result "INFECTED" and the file is in the quarantine container And no document row exists for the file and the OCR step does not read it And the audit event "MALWARE_BLOCKED" is written with the intake ID and the source, and the platform administrator is alerted | RWB-E1-041 |

##### A2.18.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P5-018-01 | Retention class | a demand letter of type "DEMAND_LETTER" with class "LEGAL10Y" in the type table | the document is stored on case "RW-2026-000123" | the document row carries retention class "LEGAL10Y" and write_once true And the file is in the write-once container | RWB-E1-041 |
| AC-ALT-P5-018-02 | Expiry with end action archive | an appraisal report of class "GENERAL05Y" stored on 1 November 2021 on case "RW-2026-000123" with no legal hold | JOB-17 runs on 6 December 2026 | the document has state "ARCHIVED" and its blob is in the archive tier And one decision log entry "DOCRET" names the document, class "GENERAL05Y", version "RET-2026.11" and expiry date 1 November 2026 | RWB-E1-041 |

##### A2.18.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P5-018-01 | Scanning service unavailable | the scanning service stub returns no answer | JOB-12 runs twice with 3 unscanned intake items | the 3 items have no scan_result and the OCR step reads none of them And the platform administrator is alerted after the second run And an upload during the outage returns 503 with MSG-P5-022 and no document row or blob is written | RWB-E1-041 |
| AC-EXC-P5-018-02 | Class not in the retention table | a document with retention class "OLD03Y" that is not in version "RET-2026.11" | JOB-17 runs | the document is listed as exception "RETENTION_CLASS_MISSING" in the review list And the document is unchanged | RWB-E1-041 |
| AC-EXC-P5-018-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P5-018-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.18.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P5-018-01 | Document intake | Schedule | Every 15 minutes | Takes scans, SFTP files and emails into OCR | Documents on the case the same day | No document is lost between paths |

---

### A2.19 Keep the Workbench document hub as the system of record for documents

#### A2.19.1 Intent

**Business objective.** Writes the document to the Workbench document hub as the record and holds only the index and the working copy in the Workbench.

**Problem.** Documents are in folders, shared drives and with couriers; originals go missing and evidence is rebuilt for each audit.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Fields extracted without review | Rising each month | Decision log and Workbench records | Monthly |

#### A2.19.2 Description

**Functional overview.** Writes the document to the Workbench document hub as the record and holds only the index and the working copy in the Workbench.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Keep the Workbench document hub as the system of record for documents | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** the Workbench document hub

**Prerequisites.** FEAT-DCM-01

#### A2.19.3 Business rules and structure

##### A2.19.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P5-019-1 | Change to a write-once legal document | MSG-P5-002 Legal documents cannot be changed. Add a new version instead. |
| VR-P5-019-2 | An original document is overdue back | MSG-P5-004 {document} is due back from {holder} since {date}. |
| BR-P5-019 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.19.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Compliance and PDPA officer | Also uses |

#### A2.19.4 Acceptance criteria

##### A2.19.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P5-019-01 | Stored against case | a scanned court notice "notice-0001.pdf" of 1.2 MB for case "RW-2026-000123" with source "SCAN" | it is stored | one document row exists with case "RW-2026-000123", type "COURT_NOTICE", source "SCAN", doc_version 1 and the stored date of today And its extracted field "black_case_no" with value "BC-TEST-0456" is in the index And the file is in container "rwb-docs-legal" at "rwb-docs-legal/{caseId}/{documentId}/v1" And DocumentStored is written to the outbox with the document ID, the case ID, the type and the source And the litigation officer opens it from the case documents screen and GET content returns the same SHA-256 hash | RWB-E1-024 |

##### A2.19.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P5-019-01 | Write once | the court notice from AC1 is stored with write_once true | a delete and a content replace are attempted through the document store and directly on the container | each attempt is refused with MSG-P5-002 And the file hash and the document row are unchanged And an audit event "DOCUMENT_CHANGE_REFUSED" is written for each attempt with the document ID and the caller | RWB-E1-024 |
| AC-ALT-P5-019-02 | Retention class | a document of type "APPRAISAL_REPORT" for case "RW-2026-000123" | it is stored | the document row carries retention class "GENERAL05Y" from type table version "DOCTYPE-2026.11" And write_once is false and the file is in container "rwb-docs" | RWB-E1-024 |

##### A2.19.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P5-019-01 | Unknown document type is refused | a file for case "RW-2026-000123" with type "BANK_STATEMENT" | it is stored | the call is refused with 422 and MSG-P5-006 And no document row, decision log entry or event is written | RWB-E1-024 |
| AC-EXC-P5-019-02 | File type not allowed | a file "macro-0001.docx" with Word content for case "RW-2026-000123" | it is stored | the call is refused with 415 and MSG-P5-001 And nothing is written to the containers or the tables | RWB-E1-024 |
| AC-EXC-P5-019-03 | The storage copy fails | container "rwb-docs" refuses writes | an appraisal report is stored for case "RW-2026-000123" | the document row is written with state "COPY_PENDING" And GET content returns 503 with MSG-GEN-006 naming "Document storage" And when the container accepts writes again the next document intake run copies the file and sets state "STORED" | RWB-E1-024 |
| AC-EXC-P5-019-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P5-019-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.19.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P5-019-01 | Document intake | Schedule | Every 15 minutes | Takes scans, SFTP files and emails into OCR | Documents on the case the same day | No document is lost between paths |

---

### A2.20 Version a document and keep its history

#### A2.20.1 Intent

**Business objective.** Keeps every version of a document with the date and the source, so a superseded version is still readable.

**Problem.** Documents are in folders, shared drives and with couriers; originals go missing and evidence is rebuilt for each audit.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Fields extracted without review | Rising each month | Decision log and Workbench records | Monthly |

#### A2.20.2 Description

**Functional overview.** Keeps every version of a document with the date and the source, so a superseded version is still readable.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Version a document and keep its history | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Blob storage, the Workbench document hub

**Prerequisites.** FEAT-DCM-01

#### A2.20.3 Business rules and structure

##### A2.20.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P5-020-1 | Change to a write-once legal document | MSG-P5-002 Legal documents cannot be changed. Add a new version instead. |
| VR-P5-020-2 | An original document is overdue back | MSG-P5-004 {document} is due back from {holder} since {date}. |
| BR-P5-020 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.20.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Legal counsel | Also uses |

#### A2.20.4 Acceptance criteria

##### A2.20.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P5-020-01 | Stored against case | a scanned court notice "notice-0001.pdf" of 1.2 MB for case "RW-2026-000123" with source "SCAN" | it is stored | one document row exists with case "RW-2026-000123", type "COURT_NOTICE", source "SCAN", doc_version 1 and the stored date of today And its extracted field "black_case_no" with value "BC-TEST-0456" is in the index And the file is in container "rwb-docs-legal" at "rwb-docs-legal/{caseId}/{documentId}/v1" And DocumentStored is written to the outbox with the document ID, the case ID, the type and the source And the litigation officer opens it from the case documents screen and GET content returns the same SHA-256 hash | RWB-E1-024 |

##### A2.20.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P5-020-01 | Write once | the court notice from AC1 is stored with write_once true | a delete and a content replace are attempted through the document store and directly on the container | each attempt is refused with MSG-P5-002 And the file hash and the document row are unchanged And an audit event "DOCUMENT_CHANGE_REFUSED" is written for each attempt with the document ID and the caller | RWB-E1-024 |
| AC-ALT-P5-020-02 | Retention class | a document of type "APPRAISAL_REPORT" for case "RW-2026-000123" | it is stored | the document row carries retention class "GENERAL05Y" from type table version "DOCTYPE-2026.11" And write_once is false and the file is in container "rwb-docs" | RWB-E1-024 |

##### A2.20.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P5-020-01 | Unknown document type is refused | a file for case "RW-2026-000123" with type "BANK_STATEMENT" | it is stored | the call is refused with 422 and MSG-P5-006 And no document row, decision log entry or event is written | RWB-E1-024 |
| AC-EXC-P5-020-02 | File type not allowed | a file "macro-0001.docx" with Word content for case "RW-2026-000123" | it is stored | the call is refused with 415 and MSG-P5-001 And nothing is written to the containers or the tables | RWB-E1-024 |
| AC-EXC-P5-020-03 | The storage copy fails | container "rwb-docs" refuses writes | an appraisal report is stored for case "RW-2026-000123" | the document row is written with state "COPY_PENDING" And GET content returns 503 with MSG-GEN-006 naming "Document storage" And when the container accepts writes again the next document intake run copies the file and sets state "STORED" | RWB-E1-024 |
| AC-EXC-P5-020-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P5-020-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.20.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P5-020-01 | Document intake | Schedule | Every 15 minutes | Takes scans, SFTP files and emails into OCR | Documents on the case the same day | No document is lost between paths |

---

### A2.21 Take field app photos and bills into the OCR intake

#### A2.21.1 Intent

**Business objective.** Accepts photos and bills captured in the field into the same OCR, extraction and indexing path.

**Problem.** Documents are in folders, shared drives and with couriers; originals go missing and evidence is rebuilt for each audit.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Fields extracted without review | Rising each month | Decision log and Workbench records | Monthly |

#### A2.21.2 Description

**Functional overview.** Accepts photos and bills captured in the field into the same OCR, extraction and indexing path.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Take field app photos and bills into the OCR intake | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Field app, the Workbench document hub

**Prerequisites.** FEAT-DCM-07

#### A2.21.3 Business rules and structure

##### A2.21.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P5-021-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P5-021 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.21.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Field collector | Also uses |

#### A2.21.4 Acceptance criteria

##### A2.21.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P5-021-01 | Capture | an inspection with eight photos and two bills, each with a client file ID, a capture time and a GPS position | the officer syncs at 2026-12-15 14:20 | ten documents are on case "RW-2026-000501" with source "UPLOAD": eight "INSPECTION_PHOTO" and two "UTILITY_BILL" And each document shows its capture time and its latitude and longitude, for example 13.7563 and 100.5018 And the two bills have intake items for OCR And ten DocumentStored events are in the outbox | RWB-E2-024 |

##### A2.21.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P5-021-01 | Offline | no signal during the visit and photos captured at 2026-12-14 10:05 | the officer syncs later at 2026-12-15 08:30 | each document has captured_at 2026-12-14 10:05 and its stored date 2026-12-15 08:30 | RWB-E2-024 |
| AC-ALT-P5-021-02 | Bill extracted | a utility bill photo showing amount "1,284.50" and due date "28/12/2569" | extraction runs | bill_amount "1284.50" and due_date "2026-12-28" are on the case in the document index | RWB-E2-024 |

##### A2.21.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P5-021-01 | A capture with no position | a photo with capture time 2026-12-15 13:58 and no GPS position | the officer syncs | the document is on the case with no latitude and longitude And the response and SCR-30 show MSG-P5-015 with count 1 | RWB-E2-024 |
| AC-EXC-P5-021-02 | A file type not allowed | a photo in HEIC format | the officer syncs | the item is refused with MSG-P5-001 And the other items in the same sync are accepted | RWB-E2-024 |
| AC-EXC-P5-021-03 | A manifest that does not match the files | a manifest of three items and two files | the officer syncs | the response is 422 with MSG-GEN-001 naming the client file ID with no file And nothing is stored | RWB-E2-024 |
| AC-EXC-P5-021-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P5-021-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.21.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P5-021-01 | Document intake | Schedule | Every 15 minutes | Takes scans, SFTP files and emails into OCR | Documents on the case the same day | No document is lost between paths |

---

### A2.22 Extend extraction to the stage 2 and 3 document types

#### A2.22.1 Intent

**Business objective.** Adds the treatment and litigation document types to classification and field extraction.

**Problem.** Documents are in folders, shared drives and with couriers; originals go missing and evidence is rebuilt for each audit.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Fields extracted without review | Rising each month | Decision log and Workbench records | Monthly |

#### A2.22.2 Description

**Functional overview.** Adds the treatment and litigation document types to classification and field extraction.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Extend extraction to the stage 2 and 3 document types | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** the Workbench document hub

**Prerequisites.** FEAT-DCM-09

#### A2.22.3 Business rules and structure

##### A2.22.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P5-022-1 | Change to a write-once legal document | MSG-P5-002 Legal documents cannot be changed. Add a new version instead. |
| VR-P5-022-2 | An original document is overdue back | MSG-P5-004 {document} is due back from {holder} since {date}. |
| VR-P5-022-3 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P5-022 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.22.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Restructuring officer (FCR), Litigation officer | Also uses |

#### A2.22.4 Acceptance criteria

##### A2.22.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P5-022-01 | Court notice | the 10 scanned court notices of the sample with 30 labeled values of court_name, black_case_no and hearing_date | extraction runs | court, case number and hearing date are on the index And at least 27 of the 30 values match the labels, which is 90% field accuracy on the sample | RWB-E2-025 |

##### A2.22.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P5-022-01 | Contract | a signed contract "DOC-0601" on case "RW-2026-000601" classified "CONTRACT" with confidence 0.9300 And its text names two parties, amount "2,400,000.00 บาท" and date "1 พฤศจิกายน 2569" | extraction runs | party_names holds the two party names, masked in responses for roles without the right And contract_amount is "2400000.00" and contract_date is "2026-11-01" | RWB-E2-025 |
| AC-ALT-P5-022-02 | Low confidence | a judgment "DOC-0602" whose judgment_amount is read with confidence 0.7100 | extraction runs | judgment_amount has state "REVIEW" And the document is in the review queue on SCR-31 with judgment_amount marked And SCR-30 shows MSG-P5-003 on "DOC-0602" | RWB-E2-025 |

##### A2.22.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P5-022-01 | A value that does not match its pattern | the pattern for red_case_no is two to four letters, a space, digits, "/" and four digits And the extractor reads red_case_no "Por345-2570" with confidence 0.9200 | extraction runs | red_case_no has state "REVIEW" And a value "Por 345/2570" with confidence 0.9200 has state "OK" | RWB-E2-025 |
| AC-EXC-P5-022-02 | A write-once document is not altered | judgment "DOC-0604" is held write-once with write_once true | extraction runs | four document_field rows are written And the stored file hash, storage_ref and write_once are unchanged | RWB-E2-025 |
| AC-EXC-P5-022-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P5-022-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.22.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P5-022-01 | Document intake | Schedule | Every 15 minutes | Takes scans, SFTP files and emails into OCR | Documents on the case the same day | No document is lost between paths |

---

## Requirements served

| Requirement | Text | Priority | Epic |
|---|---|---|---|
| REQ-DCM-001 | Every document is stored against its case with type, date, source and extracted fields. | Must | E1 |
| REQ-DCM-002 | The Workbench document hub is the system of record for recovery documents. No other store holds the authoritative copy. | Must | E1 |
| REQ-DCM-003 | Legal document types are held in a write-once container that cannot be altered or deleted. | Must | E1 |
| REQ-DCM-004 | The document types and their key fields are agreed and signed before the extraction pipeline is built. | Must | E1 |
| REQ-DCM-005 | Inbound documents are classified into one of the agreed types with a confidence score, and anything below the threshold goes to a review queue. | Must | E1 |
| REQ-DCM-006 | Fields are extracted into the index for the agreed document types, in Thai and in English. | Must | E1 |
| REQ-DCM-007 | A classified document attaches to its case without a person doing it. | Must | E1 |
| REQ-DCM-008 | Documents are searchable by case ID, type and date from the case record view. | Must | E1 |
| REQ-DCM-009 | Documents arrive from branches, the mailroom, partner file transfer and email through the same intake. | Must | E1 |
| REQ-DCM-010 | Every document carries a retention class, and intake runs a virus scan before the document is stored. | Must | E1 |
| REQ-DCM-011 | A document checklist per case type is held as reference data so that a missing document is visible. | Must | E1 |
| REQ-DCM-012 | Contracts, credit applications and mortgage documents are generated from approved templates with case data and no re-keying. | Must | E2 |
| REQ-DCM-013 | Field photographs and bills reach the same intake and index as scanned documents. | Should | E2 |
| REQ-DCM-014 | New scope. Document storage is sized, provisioned and costed for the inbound volume and its growth, and the cost belongs to the program's running cost. | Must | E1 |
| REQ-DCM-015 | New scope. Documents are backed up on a stated schedule, and a restore is tested before the first production release and at each subsequent release. | Must | E1 |
| REQ-DCM-016 | New scope. A legal hold applied to a case or a document stops deletion and expiry for as long as the hold is in place, overriding the retention class. | Must | E1 |
| REQ-DCM-017 | New scope. The hub answers an electronic discovery request by producing every document for a named population, with its metadata, its version history and the date each version was created. | Must | E2 |
| REQ-DCM-018 | New scope. A document produced from the hub carries what a court needs to accept it: its origin, the date it entered the hub, whether it has been altered since, and who has read it. | Must | E2 |
| REQ-DCM-019 | New scope. Records retention runs by class, and a document reaching the end of its retention period is disposed of or extended by a recorded decision, never silently. | Must | E2 |
| REQ-DCM-020 | New scope. The hub carries a records management position signed by Compliance and Legal covering storage, backup, legal hold, discovery and disposal. | Must | E1 |

## Screens

| Screen | What it is for | First in |
|---|---|---|
| SCR-30 Case documents | Documents on a case by type, with the extracted fields and versions | E1 |
| SCR-31 Document review queue | Low-confidence extractions to check and correct | E1 |
| SCR-32 Document custody | Originals out, their holder and their due-back date | E2 |

## Document sign-off

| Role | Name | Signature | Date |
|---|---|---|---|
| FSD owner, business analyst | | | |
| Business owner | | | |
| Solution architect | | | |
| QA lead | | | |

## Appendix A. Business glossary

Terms follow the Recovery Workbench Business Glossary.

| Term | Thai | Meaning |
|---|---|---|
| Document hub | ศูนย์เอกสาร | The Workbench store and index for recovery documents |
| Document type | ประเภทเอกสาร | The class a document belongs to on the document checklist |
| Custody | การเก็บรักษาต้นฉบับ | Where an original document is and who holds it |

## Appendix B. UI behavior

Components, field states, error display, confirmations and colors follow the Recovery Workbench Design System and Component Library. Message wording follows the Error and Message Standard.
