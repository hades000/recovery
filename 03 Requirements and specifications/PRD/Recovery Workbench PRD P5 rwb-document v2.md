SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

---
title: Recovery Workbench PRD P5 rwb-document v1
description: Product requirements for the Recovery Workbench document hub (P5 rwb-document) in the 19-service realignment; capabilities, functional and non-functional requirements, data and integration requirements, release slices by wave and acceptance criteria.
status: Draft
brd: 03 Requirements and specifications/Recovery Workbench Business Requirements Program v4.docx; 03 Requirements and specifications/Recovery Workbench Business Requirements Epic 1 v4.docx; 03 Requirements and specifications/Recovery Workbench Business Requirements Epic 2 v2.docx
fsd: 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v6/Recovery Workbench FSD P5 Document hub v3.md
service: P5 rwb-document
epic: RWB-SVC-P5
wave: 1
decision: D-RCV-60
---

# Recovery Workbench PRD P5 rwb-document v1

# 1. Document control and change log

## 1.1 Document control

| Attribute | Value |
|---|---|
| Document title | Recovery Workbench PRD P5 rwb-document |
| Document ID | P5-RWB-PRD-v1 |
| Version | 1 |
| Status | Draft |
| Classification | Confidential |
| Date | 22 November 2026 |
| Service | P5 rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epics | EP01 (Epic 1, wave 1); EP02 (Epic 2, wave 2); EP08 (Epic 8, wave 4, retention administration and legal hold only) |
| Schema | `rwb_document` |
| REST base | `/api/recovery/document/v1` |
| Topic | `rwb.document.events.v1` |
| Temporal task queue | `rwb-document` |
| Java package | `th.co.scb.ace.workbench.recovery.document` |
| Product owner role | Document hub owner (Business lead for the document scope) |
| Requirement owner role | Document hub owner with Legal counsel and Compliance and PDPA officer |
| Decision | D-RCV-60 (microservice realignment); inherits D-RCV-35 (U1 to U5), ADR-010, ADR-014, ADR-015, ADR-016, ADR-018, ADR-020, ADR-021, ADR-022 and ADR-023 |
| Upstream artifacts | Business Requirements Program v4; Business Requirements Epic 1 v4; Business Requirements Epic 2 v2; FSD P5 Document hub v3; TSD P5 Document hub v2; Architecture v5; Temporal and Drools Design v1 |
| Upstream requirement IDs | REQ-DCM-001 to REQ-DCM-020; REQ-ACA-006; REQ-DRI-004; REQ-ILG-005; NFR-004, NFR-009, NFR-012, NFR-016, NFR-017, NFR-020, NFR-021, NFR-022, NFR-023, NFR-025, NFR-026, NFR-027, NFR-028, NFR-029, NFR-033, NFR-034, NFR-035, NFR-036, NFR-039, NFR-040, NFR-042, NFR-045, NFR-046, NFR-047, NFR-049, NFR-050, NFR-051, NFR-052, NFR-053, NFR-054, NFR-056, NFR-057, NFR-058, NFR-059, NFR-062, NFR-064, NFR-067, NFR-068, NFR-069, NFR-071, NFR-072, NFR-073, NFR-074, NFR-076, NFR-078 |
| Upstream acceptance criteria | AC-P5-001-01, AC-ALT-P5-001-01 to -02, AC-EXC-P5-001-01 to -05; AC-P5-002-01, AC-ALT-P5-002-01 to -02, AC-EXC-P5-002-01 to -05; AC-P5-003-01, AC-ALT-P5-003-01 to -02, AC-EXC-P5-003-01 to -05; AC-P5-004-01, AC-ALT-P5-004-01 to -02, AC-EXC-P5-004-01 to -05; AC-P5-005-01, AC-ALT-P5-005-01 to -02, AC-EXC-P5-005-01 to -05; AC-P5-006-01, AC-ALT-P5-006-01 to -02, AC-EXC-P5-006-01 to -05; AC-P5-007-01, AC-ALT-P5-007-01 to -02, AC-EXC-P5-007-01 to -06; AC-P5-008-01, AC-ALT-P5-008-01 to -02, AC-EXC-P5-008-01 to -05; AC-P5-009-01, AC-ALT-P5-009-01 to -02, AC-EXC-P5-009-01 to -05; AC-P5-010-01, AC-ALT-P5-010-01 to -02, AC-EXC-P5-010-01 to -08; AC-P5-011-01, AC-ALT-P5-011-01 to -02, AC-EXC-P5-011-01 to -08; AC-P5-012-01, AC-ALT-P5-012-01 to -02, AC-EXC-P5-012-01 to -07; AC-P5-013-01, AC-ALT-P5-013-01 to -02, AC-EXC-P5-013-01 to -10; AC-P5-014-01, AC-ALT-P5-014-01 to -02, AC-EXC-P5-014-01 to -10; AC-P5-015-01, AC-ALT-P5-015-01 to -02, AC-EXC-P5-015-01 to -10; AC-P5-016-01, AC-ALT-P5-016-01 to -02, AC-EXC-P5-016-01 to -04; AC-P5-017-01, AC-ALT-P5-017-01 to -02, AC-EXC-P5-017-01 to -04; AC-P5-018-01, AC-ALT-P5-018-01 to -02, AC-EXC-P5-018-01 to -04; AC-P5-019-01, AC-ALT-P5-019-01 to -02, AC-EXC-P5-019-01 to -05; AC-P5-020-01, AC-ALT-P5-020-01 to -02, AC-EXC-P5-020-01 to -05; AC-P5-021-01, AC-ALT-P5-021-01 to -02, AC-EXC-P5-021-01 to -05; AC-P5-022-01, AC-ALT-P5-022-01 to -02, AC-EXC-P5-022-01 to -04; AC-BG-P5-001-01 to AC-BG-P5-022-01. Counts: 22 main, 44 alternate, 130 exception and 22 background criteria, 218 in all |
| Upstream message IDs | MSG-P5-001 to MSG-P5-008, MSG-P5-015 to MSG-P5-020 and MSG-P5-022; MSG-GEN-001, MSG-GEN-002, MSG-GEN-006; MSG-P3-027; MSG-P4-002; MSG-P7-002, MSG-P7-003 |
| Upstream feature IDs | FEAT-DCM-01 to FEAT-DCM-22 (no feature covers document generation, legal hold, discovery, backup or the records position: GAP-1580, GAP-1581, GAP-1582 and GAP-1583) |
| Upstream operations | API-P5-001 to API-P5-017 (TSD P5 v2 appendix T-A); the same 17 operations in the Ownership Map |
| Upstream events | EV-16 DocumentStored and EV-17 DocumentFieldsExtracted (published); EV-28 AgentRunCompleted (consumed) |
| Generated IDs | CAP-P5-001 to CAP-P5-019; FR-P5-001 to FR-P5-032; NFR-P5-001 to NFR-P5-033; AC-P5-001 to AC-P5-025; JRN-P5-01 to JRN-P5-06; ROL-P5-01 to ROL-P5-14; OQ-P5-01 to OQ-P5-14 |
| Run ID, branch, commit, pull request | Not applicable. This run writes documents only: no repository branch, commit or pull request is created, and no issue tracker is read or updated (rule 3, U6) |
| Source baseline | FSD P5 Document hub v3 (15 November 2026) and the BRD Program v4 / Epic 1 v4 / Epic 2 v2 (15 November 2026), realigned to Architecture v5 under D-RCV-60 |

## 1.2 Change log

| Version | Date | Change | Tool |
|---|---|---|---|
| 1 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |
| v2 | 26 November 2026 | D-RCV-60: cross-document changes under the programme directive (GAP-1590, R-21887, R-22529) | T3 Code / OpenCode / DeepSeek v4.1 Flash |

## 1.3 Inherited history and ID continuity

The product baseline is FSD P5 Document hub v3. Its history and its ID set are carried unchanged; the microservice realignment changes the owner, the store and the delivery wave, not the requirement substance (ASM-2712).

| Version | Date | Change carried from the FSD |
|---|---|---|
| 3 | 15 November 2026 | Re-based on the ACE database under D-RCV-35 (ADR-010). Source data is read only through the `recovery.v_ace_*` views and lands through ACE ingestion; no inbound load, load run or data quality exception in the Workbench. `document.party_id` becomes the business key `document.person_key`. Everything else unchanged from v2. |
| 2 | 28 October 2026 | The 22 features FEAT-DCM-01 to FEAT-DCM-22, the 20 requirements REQ-DCM-001 to REQ-DCM-020, the six document types and their 26 fields, the OCR, classification and extraction pipeline with the review queue, retention classes, virus scan and custody |
| 1 (PRD) | 22 November 2026 | First PRD of this family. CAP, FR, NFR, AC, journey and open-question IDs are new. The FSD requirement IDs (REQ-DCM-001 to REQ-DCM-020), feature IDs (FEAT-DCM-01 to FEAT-DCM-22), section IDs (A2.1 to A2.22), acceptance criteria IDs (AC-P5-xxx, AC-ALT-P5-xxx, AC-EXC-P5-xxx, AC-BG-P5-xxx), message IDs (MSG-P5-xxx), endpoint IDs (API-P5-001 to API-P5-017), table names, list-of-value names, job IDs (JOB-12, JOB-17), event IDs (EV-16, EV-17, EV-28) and container names are preserved character for character |

## 1.4 Documents this PRD is read against

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program v4 | BRD | Source of the business requirements REQ-DCM-001 to REQ-DCM-020 and the non-functional requirements |
| Recovery Workbench Business Requirements Epic 1 v4 | BRD | Source of the Epic 1 requirements the service serves (RWB-E1-024, E1-025, E1-026, E1-032, E1-033, E1-040, E1-041, E1-049, E1-050, E1-053, E1-054, E1-057) |
| Recovery Workbench Business Requirements Epic 2 v2 | BRD | Source of the Epic 2 requirements (RWB-E2-017, E2-024, E2-025, E2-026) |
| Recovery Workbench Functional Specifications by Module v6, FSD P5 Document hub v3 | FSD | Pair: the functional baseline this PRD re-expresses as product behaviour |
| Recovery Workbench Technical Specifications by Module v5, TSD P5 Document hub v2 | TSD | Source of the data dictionary, the 17 operations and the list of values |
| Recovery Workbench Architecture v5 | Architecture | Constraint: 19 services, one schema and login per service, Blob with WORM, Kafka, Temporal, no data lake, edge and gateway |
| Recovery Workbench Temporal and Drools Design v1 | Design | Constraint: task queue, workflow kit, Schedules, KEDA workers |
| Recovery Workbench Microservice Ownership Map v1 | Ownership | Owner of every table, operation, event, job and workflow |
| Recovery Workbench Non Functional Specification v3 | Non-functional | Source of the numeric targets |
| Recovery Workbench Microservice Story Template and Rules v1 | Rules | Header, versioning, precedence, placeholder and register rules |

# 2. Product overview and relationship to ACE

## 2.1 Purpose

rwb-document (P5) is the system of record for every Recovery Workbench document. It turns "documents are in folders, shared drives and with couriers" into a product: a write-once store for legal types; an index a document is found in; one intake from four channels; an OCR, classification and extraction pipeline with a review queue for anything a person must confirm; a checklist per case stage that makes a missing document visible; a retention class on every document and a disposal that is never silent; custody of the originals; the generated documents of Epic 2; and the evidence a court or an auditor accepts.

## 2.2 What is new in this release

| New | What it is | Business reason |
|---|---|---|
| The service rwb-document | One deployable with its own API and worker, schema `rwb_document`, login, topic `rwb.document.events.v1`, task queue `rwb-document` and lifecycle | The document hub becomes one owned contract inside ACE instead of a module of a single deployable |
| The store as a product behaviour | Azure Blob with WORM, a write-once container for legal types, a version chain and a SHA-256 hash per version | A legal document cannot be altered or deleted inside its retention period, and a superseded version stays readable |
| One intake with one pipeline | Branch scanners, the mailroom, partner SFTP and recovery mailboxes, then the field app, feed one intake, one OCR step, one classification and one extraction | No document is lost between paths and no document is filed by hand |
| The review queue as a governed control | Classification and extraction below the threshold stop at a person, and the correction feeds the labelled sample | No document is attached wrongly and the models improve on measured data |
| The index as the findability promise | Search by case, type, stored date, extracted field and free text within the caller's scope, every search logged | A document is found in seconds without opening cases one by one |
| The checklist as reference data | The required documents per stage and route are a versioned table; completeness is a flag on the case | A missing document shows on the case without a person checking a list |
| Retention, hold and disposal as product behaviour | A retention class per type, a legal hold that overrides it, a disposal that carries a recorded decision | The store holds what policy allows, keeps what a hold covers, and never removes anything silently |
| Generated documents | Contracts, credit applications and mortgage documents produced from Legal-approved template versions with case data | The documents of a treatment are produced without re-keying |
| Discovery and court-ready evidence | A production for a named population with metadata and version history, and per-document origin, entry date, alteration check and readers | The hub answers a legal request to the standard a court applies |

## 2.3 What is reused, and what leaves the service

| Capability | Verdict | Owner in v5 |
|---|---|---|
| Sign-in, access check, audit and PII logging | REUSE | ACE common sign-in; P4 rwb-access |
| Case record, case state and case ID | REUSE | P3 rwb-case (read through its contract) |
| Decision record and the audit chain | REUSE | P7 rwb-decision through the local decision-record library |
| Notification path | REUSE | P6 rwb-comms; ACE notification path |
| File exchange with branches and partners | REUSE, elsewhere | P2 rwb-integration (GAP-1587; ASM-2720) |
| OCR, classification and extraction engines | REUSE as an external contract | Not owned by P5: no source names the provider (GAP-1586; ASM-2719) |
| Template and merge field catalog | REUSE, elsewhere | P6 rwb-comms holds the templates; this service holds the reference (RWB-E1-046) |
| Signature capture and the e-signature journey | MOVED | P6 and S2 for the journey; this service records the document (GAP-1589; ASM-2722) |
| The ACE Attachment object as the authoritative copy | REMOVED | None. The hub is the record in Blob with WORM (GAP-1588; ASM-2721) |
| The data lake copy of the document log | REMOVED | None. No data lake in v5 (ADR-018, DP-17; GAP-1591; ASM-2724) |
| Case list, case screens, work queues | REUSE, elsewhere | P3 rwb-case. This service serves the Documents tab content and the checklist |

## 2.4 Constraints confirmed in Architecture v5 that bound the product

1. One ACE PostgreSQL server; a schema and a login per service; only rwb-source-data reads the 30 `recovery.v_ace_*` views (ADR-010, ADR-014).
2. The service writes only schema `rwb_document`; no cross-schema join and no foreign key into `public` (ADR-014, DP-01).
3. Documents are held in Azure Blob with WORM, and only rwb-document writes them (Arch v5 slides 8, 16 and 21).
4. REST is one hop from gateway-bff, with a 2 s timeout; the upload returns a link (Arch v5 slide 16; ADR-020, DP-11).
5. Events are CloudEvents on Kafka with outbox and inbox; topic `rwb.document.events.v1`; retry and `.dlt` topics; key `caseId` (ADR-015, DP-09, DP-14).
6. Temporal namespace `rwb-recovery`, task queue `rwb-document`; event-started `DocumentIntakeWorkflow` (OCR, classify, extract) with `generate` and `seal` activities; a 15-minute Temporal Schedule raises intake; JOB-17 retention is a Temporal Schedule on the 1st Sunday of each month; KEDA scales intake workers on the `rwb-document` backlog (ADR-016, DP-10).
7. Personal data stays out of events, workflow inputs and logs; payloads are encrypted by the PDPA codec; identifiers only in Kafka (Arch v5 slide 45; NFR-040).
8. There is no data lake and no Power BI connection: reporting reads events into rwb-reporting (ADR-018, DP-17).

# 3. Personas and roles

Roles only; no person is named anywhere in this document.

| ID | Persona | What they need from this product | Primary journeys |
|---|---|---|---|
| ROL-P5-01 | Case owner | Attach a document in one action, see the case's documents newest first, and see which required document is missing | JRN-P5-02 |
| ROL-P5-02 | Litigation officer | Court notices and judgments found by type, date or field; the original's custody and due-back date; a corrected extraction without a second filing | JRN-P5-02, JRN-P5-03, JRN-P5-05 |
| ROL-P5-03 | Legal counsel | Document types and their fields signed before extraction is built; write-once for legal types; a production and a document a court accepts | JRN-P5-04 |
| ROL-P5-04 | Compliance and PDPA officer | A retention class on every document, a disposal that carries a decision, a hold that overrides retention, and reads that are logged | JRN-P5-05 |
| ROL-P5-05 | Center of excellence analyst | Agreed types and fields, an extraction measure on the labelled sample, and corrections that return to it | JRN-P5-01, JRN-P5-03 |
| ROL-P5-06 | Reference data administrator | A full-file load of types, checklists and parameters that is refused whole rather than half applied, with the version in force kept | JRN-P5-02 |
| ROL-P5-07 | Restructuring officer (FCR) | Contracts, credit applications and mortgage documents generated from approved templates with no re-keying | JRN-P5-06 |
| ROL-P5-08 | Field collector | Photos and bills captured without a network, with capture time and position, and landed on the case on sync | JRN-P5-02 |
| ROL-P5-09 | Head of NPA | The NPA sign-off on the document types the NPA estate depends on | JRN-P5-02 |
| ROL-P5-10 | Internal audit | The version history, the readers and the alteration state of a produced document | JRN-P5-04 |
| ROL-P5-11 | Platform administrator | Intake runs, OCR, classification and extraction failures with an alert, and a quarantine list | JRN-P5-01, JRN-P5-03 |
| ROL-P5-12 | Document hub owner | Storage sized and costed, the estate measured, and a records management position signed by Compliance and Legal | JRN-P5-05 |
| ROL-P5-13 | Solution architect and IT lead | Backup on the bank schedule, a tested restore and a rollback by previous tag | JRN-P5-05 |
| ROL-P5-14 | Developer | A field contract for the index and the extracted fields, and a build that fails on a direct ACE read | JRN-P5-02 |

Non-human actors: the bank scheduler (Airflow) for the cross-system chain; the outbox relay; the Temporal worker and the KEDA-scaled OCR workers; the OCR, classification and extraction services; the malware scanning service; the archive tier of Blob; the consumers of DocumentStored and DocumentFieldsExtracted.

# 4. User journeys

## 4.1 Current state (as built in the monolith)

1. Documents arrive by post, by courier, by email to individual mailboxes, and by hand to the branch.
2. Each team keeps its own folder on a shared drive; a document is filed by hand under a case number a person reads.
3. OCR, where it exists, is a desktop step; the text is copied into notes rather than indexed.
4. An original leaves for a court or a law firm and the due-back date is kept in a diary.
5. At audit, the evidence is rebuilt from the shared drives, the mailboxes and the courier receipts.

Consequence: a document exists in more than one copy, the file a court sees cannot be tied to the file the bank holds, and no one can say which required documents a case is missing.

## 4.2 Target state (this product)

### JRN-P5-01 A document arrives and reaches its case without a person (unattended, every 15 minutes)

1. A 15-minute Temporal Schedule raises the intake and each intake event starts the event-started `DocumentIntakeWorkflow` on queue `rwb-document`, with KEDA workers; a scan, a partner file or a mailbox attachment is taken into the intake with its source, channel and capture time, and its SHA-256 hash is compared with the intake already held.
2. The malware scan runs before anything is stored; an infected file goes to quarantine and raises an audit event, and nothing is stored.
3. The OCR step reads every page, writes the page text with its quality, and marks an unreadable page for rescan.
4. Classification types the document against the agreed types and records its confidence; a low score, an unknown type or an unavailable classifier sends the item to the review queue.
5. Extraction writes the agreed fields with a confidence and a state per field, in Thai and in English.
6. The match step attaches the document to its case by the case ID read, then by the account number; two candidates or no match leave the item in the queue.
7. DocumentStored and DocumentFieldsExtracted are published, and the case's completeness flag is refreshed.

### JRN-P5-02 A case owner attaches and finds a document (daily, on the case)

1. The case owner uploads the file with its type; a type not in force is refused with the standard message, and a file type other than PDF, JPG or PNG is refused before anything is written.
2. The document shows at the top of the case list within 5 seconds and carries source UPLOAD and version 1.
3. The owner filters by type and date range and reads the extracted fields beside the document.
4. The Documents tab shows the checklist of the case's stage with what is present and what is missing.
5. A lawyer searches across cases by type, date and extracted field; the result is limited to the cases the role may see, and every search writes one access event.

### JRN-P5-03 A reviewer clears the review queue (daily, in scope)

1. The queue lists held intake items and stored documents with fields in review, oldest first, filtered by reason and limited to the reviewer's scope.
2. The reviewer reads the OCR text and the candidates, sets the type, corrects or confirms each field, and attaches the item to an open case in scope.
3. An empty correction, a type not in force, a date outside the allowed range, a field still in review, a closed case and a discard without a reason are each refused with their message, and nothing is stored.
4. The correction is recorded and feeds the labelled sample the extraction is measured on.

### JRN-P5-04 A legal document is stored once and produced for court (on demand)

1. A court notice is stored in the write-once container; a delete or a content replace through the service and directly on the container is refused, the hash and the row are unchanged, and an audit event records each attempt.
2. Every later version is a new row with its date, its source and its previous version, and the superseded version stays readable.
3. A produced document carries its origin, the date it entered the hub, whether it has been altered since (by hash) and who has read it.
4. A discovery request for a named population returns every document with its metadata, its version history and the date each version was created.

### JRN-P5-05 A document reaches the end of its retention period (monthly, 1st Sunday)

1. Every document carries the retention class of its type from the version of the type table in force at storage.
2. The retention run (JOB-17, a Temporal Schedule on the 1st Sunday of each month) lists every document at the end of its period, applies a legal hold where one covers the document or its case, and archives or extends by a recorded decision.
3. A class that is not in the retention table is listed as an exception and the document is left unchanged.
4. Nothing is deleted silently; every disposal carries its decision record.

### JRN-P5-06 Documents are generated for an approved treatment (Epic 2, per treatment)

1. The treatment is approved and the case facts are in force.
2. The generation step takes the current Legal-approved template version, fills the merge fields from the case, and stores the result as a generated document with its template version.
3. The officer reviews the draft; a correction of an overridable merge value regenerates the next version with a reason, and the earlier draft stays.
4. The signed copy returns to the case as a new version and the signature request is recorded as a document event and a metadata row on the document (GAP-1589; ASM-2722).

# 5. Capabilities and features

Each capability is one releasable slice of product behaviour. Priorities follow the BRD: Must is needed for the epic to release; Should is planned in the epic.

| CAP ID | Capability | What changes for the user | BR IDs | MoSCoW | Wave | FSD features |
|---|---|---|---|---|---|---|
| CAP-P5-001 | Write-once document store | A legal document cannot be altered or deleted inside its period, and every version keeps its hash | REQ-DCM-001, REQ-DCM-003 | Must | 1 | FEAT-DCM-01 (A2.1) |
| CAP-P5-002 | The hub as system of record, with versions and custody | One authoritative copy per document, every version readable, every movement of an original recorded | REQ-DCM-002 | Must | 1 | FEAT-DCM-19 (A2.19), FEAT-DCM-20 (A2.20) |
| CAP-P5-003 | Index and search within a case | A document is found by type, date or extracted field without opening the file | REQ-DCM-008 | Must | 1 | FEAT-DCM-02 (A2.2), FEAT-DCM-05 (A2.5) |
| CAP-P5-004 | Search across cases with role scope and an access log | A lawyer or auditor finds a document across cases, only in the cases the role may see, and the search is logged | REQ-DCM-008, REQ-ACA-006 | Should | 1 | FEAT-DCM-06 (A2.6) |
| CAP-P5-005 | Document types, fields and sign-off as versioned data | The extraction pipeline has a signed target, and a type change is a data release | REQ-DCM-004 | Must | 1 | FEAT-DCM-03 (A2.3) |
| CAP-P5-006 | Checklist per case stage and the completeness flag | A missing document shows on the case without a person checking a list | REQ-DCM-011 | Must | 1 | FEAT-DCM-16 (A2.16) |
| CAP-P5-007 | OCR pipeline | Every inbound page becomes searchable text, and an unreadable page is sent back rather than dropped | REQ-DCM-001, REQ-DCM-006 | Must | 1 | FEAT-DCM-07 (A2.7) |
| CAP-P5-008 | Classification with confidence and review routing | A document is typed, and a doubtful one goes to a person instead of the case | REQ-DCM-005 | Must | 1 | FEAT-DCM-08 (A2.8) |
| CAP-P5-009 | Field extraction in Thai and English | The agreed fields fill the index with a confidence each | REQ-DCM-006 | Must | 1 | FEAT-DCM-09 (A2.9) |
| CAP-P5-010 | Review queue and correction | A person corrects in one screen, and the correction improves the next extraction | REQ-DCM-005 | Must | 1 | FEAT-DCM-10 (A2.10), FEAT-DCM-11 (A2.11) |
| CAP-P5-011 | Automatic attach to the case | No document is filed by hand; an unmatched document is queued, never guessed | REQ-DCM-007 | Must | 1 | FEAT-DCM-12 (A2.12) |
| CAP-P5-012 | One intake from branches, mailroom, partner SFTP, email and the field app | Every document path ends in the hub with its channel recorded | REQ-DCM-009, REQ-DCM-013 | Must (REQ-DCM-013 Should) | 1 for the four scanned paths; 2 for the field app | FEAT-DCM-13 (A2.13), FEAT-DCM-14 (A2.14), FEAT-DCM-15 (A2.15), FEAT-DCM-21 (A2.21) |
| CAP-P5-013 | Retention class, virus scan and disposal by recorded decision | The store holds only safe files, keeps each for the period policy sets, and never removes anything silently | REQ-DCM-010, REQ-DCM-019 | Must | 1 | FEAT-DCM-17 (A2.17), FEAT-DCM-18 (A2.18) |
| CAP-P5-014 | Legal hold that overrides retention | A held document or case stops expiring for as long as the hold is in place | REQ-DCM-016 | Must | 4 | No FSD feature (GAP-1581; ASM-2714) |
| CAP-P5-015 | Generated documents from approved templates | Contracts, credit applications and mortgage documents are produced without re-keying, and a correction is a new version | REQ-DCM-012 | Must | 2 | No FSD feature (GAP-1580; ASM-2713) |
| CAP-P5-016 | Field app photos and bills | An inspection is on the case the same day it is made, with its time and position | REQ-DCM-013 | Should | 2 | FEAT-DCM-21 (A2.21) |
| CAP-P5-017 | Extraction for the stage 2 and 3 types | The litigation pack and the treatment record fill themselves | REQ-DCM-006 | Must | 2 | FEAT-DCM-22 (A2.22) |
| CAP-P5-018 | E-discovery production and court-ready evidence | A legal request is answered from one store, with version history and the alteration state | REQ-DCM-017, REQ-DCM-018 | Must | 2 | No FSD feature (GAP-1582; ASM-2715) |
| CAP-P5-019 | Sizing, backup and the records management position | Storage is provisioned for the forecast, a restore is proven at each release, and the position is signed | REQ-DCM-014, REQ-DCM-015, REQ-DCM-020 | Must | 1 | No FSD feature (GAP-1583; ASM-2716) |

## 5.1 Capabilities not carried into the product

| Capability | Status | Later home |
|---|---|---|
| The ACE Attachment object as the authoritative document copy (TSD P5 v2 T3.1) | Removed | None. The hub is the record in Blob with WORM (GAP-1588; ASM-2721) |
| The nightly document copy to the data lake | Removed | None. No data lake in v5 (ADR-018, DP-17; GAP-1591; ASM-2724) |
| Direct file-folder, SFTP and mailbox polling inside the document module | Removed from this service | P2 rwb-integration, which hands the file to the intake (GAP-1587; ASM-2720) |
| A 15-minute scheduled intake job reading the file systems | Replaced | An event-started `DocumentIntakeWorkflow` with KEDA workers on queue `rwb-document`; a 15-minute Temporal Schedule raises the intake (GAP-1590; ASM-2723) |
| Signature capture inside the document module | Moved | P6 and S2 for the journey; this service records the document (GAP-1589; ASM-2722) |
| Document type and checklist tables read by other modules | Removed | Reached through this service's contract only (DP-01, DP-11) |

# 6. Functional requirements

Every requirement is specific and testable. The FSD REQ column keeps the trace to the source. Priorities follow the BRD.

| FR ID | Requirement | CAP | BR | FSD REQ | Priority | Wave |
|---|---|---|---|---|---|---|
| FR-P5-001 | The service SHALL store every document against exactly one case with its type, its source, its stored date, its version and its extracted fields, and SHALL refuse to store a document whose case does not resolve to an open case in the caller's scope. | CAP-P5-001 | REQ-DCM-001 | REQ-DCM-001 | Must | 1 |
| FR-P5-002 | The service SHALL accept only PDF, JPG and PNG content, SHALL refuse any other content with the message MSG-P5-001 before a row or a blob is written, and SHALL refuse a type not in force with MSG-P5-006. | CAP-P5-001 | REQ-DCM-001 | REQ-DCM-001 | Must | 1 |
| FR-P5-003 | The service SHALL hold a legal document type in the write-once container, SHALL refuse a delete or a content replace both through the service and on the container, SHALL leave the row and the hash unchanged, and SHALL write one audit event per refused attempt naming the document and the caller. | CAP-P5-001 | REQ-DCM-003 | REQ-DCM-003 | Must | 1 |
| FR-P5-004 | The service SHALL be the only system of record for a recovery document: it SHALL hold the file in Blob with WORM and the metadata, text, fields, custody, signatures and retention in `rwb_document`, and SHALL create no authoritative copy in any other store. | CAP-P5-002 | REQ-DCM-002 | REQ-DCM-002 | Must | 1 |
| FR-P5-005 | The service SHALL keep every version of a document as its own row with the version number, the previous version, the source, the stored date and the SHA-256 hash, and SHALL return a superseded version on request for as long as its retention class allows. | CAP-P5-002 | REQ-DCM-002 | REQ-DCM-002 | Must | 1 |
| FR-P5-006 | The service SHALL record every movement of an original document with when it moved, from where, to where, who holds it and its due-back date, and SHALL raise the overdue message MSG-P5-004 for an original past its due-back date. | CAP-P5-002 | REQ-DCM-002 | REQ-DCM-002 | Must | 1 |
| FR-P5-007 | The service SHALL index every document by case, type, stored date and every extracted field, and SHALL return the documents of a case filtered by type and date range, newest first, within 5 seconds of storage. | CAP-P5-003 | REQ-DCM-008 | REQ-DCM-008 | Must | 1 |
| FR-P5-008 | The service SHALL search the documents of one case by type, stored date range and extracted field with its operator, and SHALL return case number, type, stored date and the matching field value for each result. | CAP-P5-003 | REQ-DCM-008 | REQ-DCM-008 | Must | 1 |
| FR-P5-009 | The service SHALL search active documents across every case in the caller's scope by type, stored date range, extracted field and free text, SHALL limit the result to cases the role may see, and SHALL write one access event per search with the user, the criteria, the result count and the case IDs returned. | CAP-P5-004 | REQ-DCM-008, REQ-ACA-006 | REQ-DCM-008 | Should | 1 |
| FR-P5-010 | The service SHALL refuse a free-text search for a role whose masking rules hide the searched class of data, SHALL name "document text" in the refusal, and SHALL record the SHA-256 hash of the search term in the access event rather than the term. | CAP-P5-004 | REQ-ACA-006 | REQ-ACA-006 | Should | 1 |
| FR-P5-011 | The service SHALL hold the agreed document types, the fields extracted from each, the checklist each belongs to, the retention class, the write-once flag and the Legal and NPA sign-off as one versioned reference load, and SHALL refuse the load whole when a row has no sign-off, names a class not in the retention table, repeats a type code or is otherwise invalid, keeping the version in force. | CAP-P5-005 | REQ-DCM-004 | REQ-DCM-004 | Must | 1 |
| FR-P5-012 | The service SHALL hold the document checklist per stage and route as a versioned table, SHALL show the checklist of the case's stage with each type present or missing, and SHALL set a completeness flag with the missing count and the missing types so that a new checklist version takes effect from its valid-from date with no code release. | CAP-P5-006 | REQ-DCM-011 | REQ-DCM-011 | Must | 1 |
| FR-P5-013 | The service SHALL read every inbound page through the OCR contract, SHALL write the text of each page with its page number and quality, SHALL mark an unreadable page for rescan with the page numbers, and SHALL record the OCR engine version and the languages read. | CAP-P5-007 | REQ-DCM-001, REQ-DCM-006 | REQ-DCM-006 | Must | 1 |
| FR-P5-014 | The service SHALL make the OCR step idempotent on an intake item already read, SHALL retry a failed call on a schedule, SHALL leave the item pending and alert the platform administrator when the OCR contract is unavailable across repeated runs, and SHALL mark a file it cannot read as FAILED with the reason UNREADABLE_FILE and write no text for it. | CAP-P5-007 | REQ-DCM-001 | REQ-DCM-001 | Must | 1 |
| FR-P5-015 | The service SHALL classify every read document into one of the agreed types with a confidence, SHALL route an item below the threshold of the type version in force to the review queue with the two highest candidates, SHALL route a type not in the agreed list and an unavailable classifier to the review queue with their reasons, and SHALL record the classifier version and the fallback flag. | CAP-P5-008 | REQ-DCM-005 | REQ-DCM-005 | Must | 1 |
| FR-P5-016 | The service SHALL extract the agreed fields of a typed document in Thai and in English, SHALL write each field with its value, its confidence and its state, SHALL put a field below its threshold or unconvertible to a date into review while keeping the value read, and SHALL leave a document whose extraction failed unattached. | CAP-P5-009 | REQ-DCM-006 | REQ-DCM-006 | Must | 1 |
| FR-P5-017 | The service SHALL present one review queue of held intake items and of stored documents with fields in review, oldest first, filterable by kind and reason, and limited to the reviewer's scope. | CAP-P5-010 | REQ-DCM-005 | REQ-DCM-005 | Must | 1 |
| FR-P5-018 | The service SHALL let a reviewer set the type of a held item, correct or confirm each extracted field, attach the item to an open case in scope, or discard it with a reason, SHALL refuse an empty correction, a type not in force, a date outside the allowed range, an attach with a field still in review, a closed case and a discard without a reason, and SHALL record the correction for the labelled sample. | CAP-P5-010 | REQ-DCM-005 | REQ-DCM-005 | Must | 1 |
| FR-P5-019 | The service SHALL attach a read document to its case automatically by the case ID read and then by the account number read, SHALL record the match method in the decision record, SHALL hold an item with two candidates, no match or no agreed type in the queue with its candidates, and SHALL write no document row for an item it could not match. | CAP-P5-011 | REQ-DCM-007 | REQ-DCM-007 | Must | 1 |
| FR-P5-020 | The service SHALL take every inbound file through one intake with its source, its channel, its capture time, its size and its SHA-256 hash, SHALL accept the four channels of branch scanner, mailroom, partner SFTP and recovery mailbox, SHALL not take in the same hash twice from the same channel, SHALL refuse a file type not allowed and a file above the size limit with their messages, and SHALL raise an alert after two failed runs of a channel. | CAP-P5-012 | REQ-DCM-009 | REQ-DCM-009 | Must | 1 |
| FR-P5-021 | The service SHALL take field app photos, bills and checklists with their capture time and GPS position into the same intake, SHALL accept a capture made with no network and upload it on sync with the original capture time, SHALL store a capture with no position and warn the officer, and SHALL refuse a manifest whose items do not match the files. | CAP-P5-016 | REQ-DCM-013 | REQ-DCM-013 | Should | 2 |
| FR-P5-022 | The service SHALL carry the retention class of the document type version in force at storage on every document row, SHALL derive the period from the retention table, and SHALL list a document whose class is not in the retention table as an exception without changing the document. | CAP-P5-013 | REQ-DCM-010 | REQ-DCM-010 | Must | 1 |
| FR-P5-023 | The service SHALL scan every inbound file for malware before it is stored, SHALL place an infected file in the quarantine container with no document row and no OCR read, SHALL write the audit event MALWARE_BLOCKED with the intake and the source, SHALL alert the platform administrator, and SHALL refuse an upload with MSG-P5-022 while the scan contract is unavailable. | CAP-P5-013 | REQ-DCM-010 | REQ-DCM-010 | Must | 1 |
| FR-P5-024 | The service SHALL, at the end of a document's retention period, archive it, extend it, or hold it, and SHALL record every outcome as a decision entry naming the document, its class, the retention-table version and the expiry date, so that no document is removed silently. | CAP-P5-013 | REQ-DCM-019 | REQ-DCM-019 | Must | 2 |
| FR-P5-025 | The service SHALL stop the deletion and the expiry of a document and of every document of a case for as long as a legal hold covers it, SHALL take the hold from the hold recorded by rwb-case, and SHALL release the document to its retention class when the hold is lifted. | CAP-P5-014 | REQ-DCM-016 | REQ-DCM-016 | Must | 4 |
| FR-P5-026 | The service SHALL generate a document from the current Legal-approved version of its template with the merge fields filled from the case, SHALL store it as a generated document naming its template version, and SHALL regenerate the next version with a reason when an overridable merge value is corrected. | CAP-P5-015 | REQ-DCM-012 | REQ-DCM-012 | Must | 1 for letters and notices; 2 for contracts, credit applications and mortgage documents (GAP-1580; ASM-2713) |
| FR-P5-027 | The service SHALL extend classification and extraction to the stage 2 and 3 types, SHALL carry a per-field state and confidence for them as for the first six types, and SHALL leave the stored file, its hash, its storage reference and its write-once flag unchanged by an extraction. | CAP-P5-017 | REQ-DCM-006 | REQ-DCM-006 | Must | 2 |
| FR-P5-028 | The service SHALL answer an electronic discovery request for a named population with every document of that population, its metadata, its version history and the date each version was created, within the response target once Compliance sets one. | CAP-P5-018 | REQ-DCM-017 | REQ-DCM-017 | Must | 2 |
| FR-P5-029 | The service SHALL produce with every document it releases its origin, the date it entered the hub, whether it has been altered since by comparison with its recorded hash, and who has read it. | CAP-P5-018 | REQ-DCM-018 | REQ-DCM-018 | Must | 2 |
| FR-P5-030 | The service SHALL report the storage it holds against the forecast, SHALL be backed up on the bank schedule, and SHALL provide a tested restore before the first production release and at every release after it. | CAP-P5-019 | REQ-DCM-014, REQ-DCM-015 | REQ-DCM-015 | Must | 1 |
| FR-P5-031 | The service SHALL hold a records management position signed by Compliance and Legal covering storage, backup, legal hold, discovery and disposal, and SHALL not release a document behaviour that contradicts the position in force. | CAP-P5-019 | REQ-DCM-020 | REQ-DCM-020 | Must | 1 |
| FR-P5-032 | The service SHALL write the decision record of every document action before the change takes effect, SHALL write the document attachment to the interaction ledger, and SHALL refuse the action with the standard message and raise an incident when either write fails. | CAP-P5-002 | REQ-DRI-004, REQ-ILG-005 | REQ-DRI-004 | Must | 1 |

Reading note: FSD A2.10 and A2.11 assert the same acceptance criteria for the review queue and for its correction, so the two are read as one behaviour with two requirements here, and the correction feed that RWB-E1-054 requires is stated once in FR-P5-018 (GAP-1593; ASM-2725).

# 7. Non-functional requirements

Targets are copied from the Non Functional Specification v3, the BRDs and the Architecture v5. A target marked open is carried as an open question, never as a value.
Outbound file size, outbound file count, daily tape volume, the 16:00 window and the 01:30 extract targets are open under DL11 with placeholder R9; Not specified in the source documents (GAP-1544).

| NFR ID | Requirement | Target | BR | Priority | Test |
|---|---|---|---|---|---|
| NFR-P5-001 | The case documents list loads for a case that holds 50 documents. | Under 2 seconds | NFR-009 | Must | Performance test in SIT |
| NFR-P5-002 | A search inside a case, and a search across documents, returns inside its target. | Under 2 seconds within a case; under 5 seconds across documents | NFR-012 | Must | Performance test at the stated volume |
| NFR-P5-003 | The intake pipeline processes its throughput in the test environment. | 500 pages per hour | NFR-016 | Must | Throughput test with 500 pages in 125 intake items |
| NFR-P5-004 | Classification is correct on the labelled sample, and anything below the threshold goes to the review queue. | 90 percent correct, which is at least 162 of the 180 sample documents | NFR-017 | Must | Classification evaluation run on the labelled sample |
| NFR-P5-005 | Extraction meets its pass mark on every field of the labelled sample, in Thai and in English. | Precision 0.90 and recall 0.90 per field | REQ-DCM-006, NFR-057 | Must | Extraction evaluation run on the labelled sample |
| NFR-P5-006 | The hub holds the full recovery document estate as a system of record, every version and every held document included, sized for growth. | About 5.8 million documents and 2.8 TB by the end of 2031 | NFR-069 | Must | Volume test and storage forecast review |
| NFR-P5-007 | The store holds the annual inbound volume with its growth rate. | About 860,000 documents in 2027, rising 15 percent a year; about 64,000 to 74,000 documents a month | NFR-004 | Must | Volume test at the stated inflow |
| NFR-P5-008 | The service is available during business hours and outside them, when intake, OCR and retention run. | 99.9 percent in business hours; 99.5 percent outside business hours excluding the change window | NFR-020, NFR-021 | Must | Availability read monthly from monitoring |
| NFR-P5-009 | The service inherits the ACE recovery point and recovery time. | The ACE recovery point objective and recovery time objective | NFR-022, NFR-023 | Must | Failover and restore test before the first release |
| NFR-P5-010 | Documents are backed up on the bank schedule and a restore is proven at each release. | Backup on the bank schedule; restore tested before the first production release and at every release after it | NFR-071 | Must | Restore test in SIT at each release |
| NFR-P5-011 | A legal document in the write-once container cannot be altered or deleted inside its retention period. | Write-once for legal types, proven through the service and on the container | NFR-029 | Must | Write-once attempt test, both paths |
| NFR-P5-012 | Every document type carries a retention class, and the class sets how long the document is kept. | A class on every type; the periods are not set (OQ-P5-10; GAP-1584; ASM-2717) | NFR-028 | Must | Reference-data load review; retention run in SIT |
| NFR-P5-013 | A legal hold stops deletion and expiry for the document or case it covers, for as long as it is in place, overriding the retention class. | Hold overrides retention | NFR-072 | Must | Retention run with a held document |
| NFR-P5-014 | A document at the end of its period is disposed of or extended by a recorded decision, and is never removed silently. | Recorded decision on every disposal | NFR-074 | Must | Retention run audit over a month |
| NFR-P5-015 | Every read of a document and of its extracted fields is logged. | Every read | NFR-042 | Must | Access log reconciliation against reads |
| NFR-P5-016 | Every document type carries a data classification, and the classification sets its handling. | A classification per type; the scheme is applied (OQ-P5-11) | NFR-047 | Must | Classification review per type |
| NFR-P5-017 | Every decision is reproducible, and every action carries the rule, model, classifier and extractor versions and the approver that allowed it. | Every decision and every action | NFR-033, NFR-034, NFR-078 | Must | Decision record inspection |
| NFR-P5-018 | The decision log chain is checked daily and a break is reported the same day. | Daily check, same-day report | NFR-035 | Must | Chain break drill |
| NFR-P5-019 | An electronic discovery request is answered with every document of the population, its metadata, its version history and the date each version was created. | The response target is not set (OQ-P5-09; GAP-1582; ASM-2715) | NFR-073 | Must | Discovery run against a named population in SIT |
| NFR-P5-020 | A document produced from the hub carries its origin, the date it entered the hub, whether it has been altered since, and who has read it, to the standard a court applies. | Every document produced | NFR-076 | Must | Production pack review with Legal counsel |
| NFR-P5-021 | An audit or regulatory request is answered inside its deadline with the decision history and the supporting documents. | Inside the deadline set by the requester | NFR-036 | Must | Audit request rehearsal |
| NFR-P5-022 | Data is encrypted at rest and in transit, secrets are held in the key store, and the build blocks a change carrying a secret, personal data in code or logs, or an unapproved dependency. | Encrypted; no secret in code, configuration or prompt; pipeline checks pass | NFR-052, NFR-053, NFR-054 | Must | Security review, secret scan and pipeline negative test |
| NFR-P5-023 | Staff authenticate with single sign-on and multi-factor authentication; jobs and agents use service identities; a partner account is scoped to its own cases. | Entra ID single sign-on with multi-factor; service identities; partner scope | NFR-049, NFR-050, NFR-051 | Must | Sign-in, identity and partner scope test |
| NFR-P5-024 | Party identifiers are masked at rest and in use by role, and each screen and each agent receives only the personal data it needs. | Masked at rest and in use; minimisation per screen and per agent | NFR-039, NFR-040 | Must | Masking matrix test across roles |
| NFR-P5-025 | Logs, traces and metrics cover intake, OCR, classification, extraction and retention; every job has a run book, monitoring and an alert to a named owner. | Every job covered; alert within 15 minutes | NFR-064, NFR-067, NFR-068 | Must | Observability review and alert drill |
| NFR-P5-026 | A failing call or a failing job is retried on a schedule and, after three retries, moves to an exception queue with a task for a named owner; an event that cannot be processed goes to the dead-letter topic and is replayed. | Three retries, then the exception queue; dead-letter and replay | NFR-025, NFR-026 | Must | Failure injection |
| NFR-P5-027 | Document text is read and extracted in Thai and in English, and a customer document is produced in the customer's language. | Thai and English; Thai by default, English where the customer chose English | NFR-057, NFR-058, NFR-059 | Must | Sample set in both languages |
| NFR-P5-028 | Document data stays in the bank's own cloud tenancy in the agreed region. | SCB Azure, Southeast Asia | NFR-046 | Must | Tenancy review |
| NFR-P5-029 | A production release rolls back by redeploying the previous tag, and the service carries its own migration sequence in its own schema. | Rollback by previous tag; per-service migration | NFR-027 | Must | Rollback rehearsal |
| NFR-P5-030 | The field app captures evidence with no network connection and uploads when it reconnects. | Offline capture | NFR-062 | Must | Offline capture test |
| NFR-P5-031 | No personal data appears in an event, a workflow input, a workflow history or a log; they carry identifiers only. | Identifiers only | NFR-040, NFR-042 | Must | Payload and log inspection |
| NFR-P5-032 | No production data is used in development, and the user acceptance environment uses masked copies. | Synthetic in development, masked in user acceptance | NFR-045 | Must | Environment data review |
| NFR-P5-033 | Penetration testing and a security review are completed before the first production release. | Before the first production release | NFR-056 | Must | Security sign-off |

# 8. Data requirements

## 8.1 Entities owned by the service

Schema `rwb_document`. Every table carries the seven standard record columns of the platform library. Retention is stated by class; the periods are open (GAP-1584; ASM-2717).

| Entity | Kind | Key fields | Classification | Source | Retention |
|---|---|---|---|---|---|
| `document` | Record, one row per version (EXTEND ACE Attachment in the legacy model; the hub is the record in v5: GAP-1588; ASM-2721) | `id`; `case_id`; `person_key` (ACE customer business key, no foreign key: GAP-1594; ASM-2726); `document_type`; `source`; `storage_ref`; `classification_confidence`; `review_status`; `retention_class`; `write_once`; `doc_version`; `previous_version_id`; `content_sha256`; `captured_at`; `capture_latitude`; `capture_longitude`; `client_file_id`; `capture_kind`; `template_id`; `treatment_id` | [CONFIDENTIAL] metadata; the file it points to is [PII] where it names a customer | Workbench and the four intake channels | Its retention class (open) |
| `document_field` | Record | `id`; `document_id`; `field_name`; `field_value`; `confidence`; `confirmed_by`; `extracted_value`; `extractor_version` | [PII] | The document text through extraction, or a reviewer | Life of the document |
| `document_text` | Record, one row per page | `id`; `intake_id`; `document_id`; `page_no`; `text_content`; `quality` | [PII] | The OCR contract | Life of the document |
| `document_intake` | Record, one row per inbound file | `id`; `source`; `source_ref`; `channel_code`; `file_name`; `file_size`; `captured_at`; `sender_address`; `partner_id`; `received_at`; `file_sha256`; `intake_ref`; `scan_result`; `scanned_at`; `case_id`; `document_id`; `ocr_ref`; `ocr_status`; `ocr_attempts`; `page_count`; `rescan_pages`; `ocr_quality`; `languages`; `ocr_engine_version`; `predicted_type`; `classification_confidence`; `type_candidates`; `classifier_version`; `classify_fallback`; `match_status`; `candidate_case_ids`; `extracted_fields`; `extract_status`; `extract_attempts`; `review_reason`; `review_outcome`; `resolved_by`; `resolved_at`; `discard_reason` | [PII] | The four intake channels and the field app | Workbench record class |
| `document_custody` | Record, one row per movement | `id`; `document_id`; `moved_at`; `from_location`; `to_location`; `held_by`; `due_back` | [CONFIDENTIAL] | The officer who moves the original | Life of the document |
| `document_type` | Versioned reference | `id`; `doc_type_code`; `label_en`; `label_th`; `write_once`; `retention_class`; `field_definitions`; `legal_signoff_by`; `legal_signoff_date`; `npa_signoff_by`; `npa_signoff_date`; `table_version`; `valid_from`; `valid_to`; `classify_threshold` | [PUBLIC] for the label and the type code; [CONFIDENTIAL] for the field definitions | Workbench reference data, signed by Legal and NPA | Versioned; superseded versions kept |
| `document_checklist_item` | Versioned reference | `id`; `stage_code`; `route_code`; `document_type`; `required`; `sort_order`; `table_version`; `valid_from`; `valid_to` | [CONFIDENTIAL] | Workbench reference data | Versioned; superseded versions kept |
| `document_hub_parameter` | Versioned reference | `id`; `param_code`; `param_value`; `unit`; `table_version`; `valid_from`; `valid_to` | [CONFIDENTIAL] | Workbench parameter data | Versioned; superseded versions kept |
| `case_document_check` | Record, one row per case | `id`; `case_id`; `checklist_version`; `required_count`; `present_count`; `missing_types`; `complete`; `checked_at`; `last_event_id` | [CONFIDENTIAL] | Workbench computation from the checklist and the documents | Life of the case |
| `retention_rule` | Versioned reference | Fields: Not specified in the source documents (GAP-1584; ASM-2717) | [CONFIDENTIAL] | Compliance with Legal through reference data | Versioned; superseded versions kept |
| `retention_action` | Record, one row per document per run | `id`; `document_id`; `run_month`; `action`; `decision_log_id` | [CONFIDENTIAL] | The retention run | Workbench record class |
| `signature_request` | Record | Fields: Not specified in the source documents (GAP-1589; ASM-2722) | [PII] | The signature request raised on a document | Life of the document |

Not carried: any table holding an authoritative copy of a document outside Blob with WORM, and any lake-copy watermark table. Both are legacy with no target in v5.

## 8.2 Data read but not owned

| Data | Owner | Direction | Classification |
|---|---|---|---|
| The document file in Azure Blob with WORM, the archive tier and the quarantine container | Platform storage, written by this service only | Read and write by claim-check reference | [PII] and [CONFIDENTIAL] according to the document type |
| Case identity, case status, case scope and the legal hold of a case | P3 rwb-case | In, through its contract | [CONFIDENTIAL] |
| Roles, scope, capability rights and field masking policy | P4 rwb-access | In, through its contract, cached | [CONFIDENTIAL] |
| The ACE person key behind a case party | P1 rwb-source-data, through its contract | In, on demand | [PII] |
| Classification and extraction results of an AgentRunCompleted event | P10 rwb-agent | In, by event | [CONFIDENTIAL] |
| Template and merge field definitions | P6 rwb-comms | In, by reference on the generated document | [CONFIDENTIAL] |
| Partner code and panel status for a partner SFTP subfolder | S9 rwb-partner | In, through its contract | [CONFIDENTIAL] |
| Decision record identity and the central ledger | P7 rwb-decision | Out, through the local record and the shared topic | [CONFIDENTIAL] |

The service reads no ACE table and no `recovery.v_ace_*` view directly (ADR-010, DP-05).

## 8.3 Field-level requirements for personal and financial data

| Field | Meaning | Classification | Requirement |
|---|---|---|---|
| `document.person_key` | The ACE customer the document belongs to | [PII] | Masked in every response unless the role holds an unmasked row; never in an event |
| `document_field.field_value`, `document_field.extracted_value` | A value read from a document: party name, court case number, amount, date | [PII] or [SENSITIVE_FINANCIAL] by field | Returned masked by role; the assessment amount and the judgment amount are [SENSITIVE_FINANCIAL] |
| `document_text.text_content` | The OCR text of a page | [PII] | Read only by a role whose masking rules allow the free text; a free-text search by any other role is refused |
| `document_intake.sender_address` | The mailbox sender of an inbound document | [PII] | Masked in every response and in every log |
| `document_intake.file_name`, `source_ref` | The file name and the path it arrived from | [CONFIDENTIAL] | Returned to the reviewer only |
| `document_custody.held_by` | Who holds an original | [CONFIDENTIAL] | Read by the case team and Legal counsel |
| `document.content_sha256` | The hash that proves the file unchanged | [PUBLIC] | Returned with the document as its alteration evidence |
| `document.retention_class`, `document_type.retention_class` | The class that sets the period | [CONFIDENTIAL] | Read by Compliance; a class not in the table is an exception, never a deletion |

## 8.4 Data rules

1. A value a business person may change is a versioned data row read at run time, never a constant in code (BR-P5-001 to BR-P5-022).
2. A stored file is never overwritten; a change is a new version row with its own hash.
3. A link to an ACE record is the business key `person_key` of type `varchar(255)` with no foreign key (GAP-1594; ASM-2726).
4. No personal data is carried in an event, a workflow input or a log; a payload carries identifiers only.
5. Every document row carries the retention class of the type version in force at storage.
6. OCR text, extracted fields and capture positions are personal data and are handled as such.
7. A document is never deleted by an operator; disposal is a recorded action of the retention run under a class or a hold.

# 9. Integration points

Paths and call types are the confirmed v5 constraints. Nothing here is a design decision of this document.

| System or consumer | Direction | Protocol and call | Owner | Notes |
|---|---|---|---|---|
| Azure Blob with WORM, the archive tier and the quarantine container | Out and in | File claim-check over HTTPS, SAS link | Platform storage (RWB-PLT-DB and the platform infrastructure); written by this service only | Files of 2.8 TB by 2031. A write-once container for legal types; nothing else writes a document |
| gateway-bff | In | REST composite route, one hop, 2 s timeout | Platform edge (RWB-PLT-EDGE) | The Documents tab, the document search page and the review queue; the composite route joins this answer with rwb-case |
| rwb-case (P3) | In and out | REST and Temporal activity | P3 | Case identity, status and scope; the legal hold of a case and of a document is recorded by P3 (GAP-1581; ASM-2714); DocumentStored and DocumentFieldsExtracted are consumed by P3 |
| rwb-access (P4) | In | REST, cached | P4 | Authorise, role scope, capability rights and field masking policy |
| rwb-source-data (P1) | In | REST | P1 | The ACE person key behind a case party; no direct view read from this service |
| rwb-agent (P10) | In and out | Kafka event `AgentRunCompleted` in; Temporal child run out; REST tool call in | P10 | Classification and extraction as a child run of the intake workflow (GAP-1586; ASM-2719) |
| rwb-integration (P2) | In and out | Temporal activity and REST file fetch by ID with a SAS link | P2 | File intake from branch scanners, partner SFTP and recovery mailboxes; the file is handed to this service as an intake item (GAP-1587; ASM-2720) |
| rwb-comms (P6) | In and out | Temporal activity and REST | P6 | A letter or notice generated from a template (P6 raises the request; this service stores and versions the result); the template and merge field catalog is P6's |
| rwb-partner (S9) | In | REST | S9 | Partner code and panel status for a partner file channel; a suspended or unknown partner is refused |
| rwb-decision (P7) | Out | Decision-record library, the shared topic `rwb.decision-record.v1` | P7 | One record per document action before the change; the retention decision DOCRET |
| rwb-reporting (P9) | Out | Kafka events | P9 | Document volumes and the estate from DocumentStored and DocumentFieldsExtracted; no extract leaves this service |
| Kafka topic `rwb.document.events.v1` | Out | CloudEvents 1.0, AsyncAPI contract, outbox, retry 1 min, 10 min, 1 h then `.dlt`, key `caseId` | This service | EV-16 DocumentStored and EV-17 DocumentFieldsExtracted |
| The malware scanning service | Out | REST | Platform security service | Scan before storage; a scanning outage blocks the store (GAP-1586; ASM-2719) |
| The bank backup and archive service | Out | Platform backup schedule | IT lead | Backup on the bank schedule; a tested restore at each release |
| The data lake and Power BI (INT-19, INT-20) | Removed | None | None | Removed in v5; no document or document log leaves this service (GAP-1591; ASM-2724) |

## 9.1 Integration questions

| Question | Owner role | Why it blocks |
|---|---|---|
| Which service performs OCR, classification and field extraction, and under which contract and version scheme? | Solution architect with the AI product owner | Decides the OCR, classifier and extractor versions the decision record carries (GAP-1586; ASM-2719) |
| Does rwb-integration own the branch scanner folders, the partner SFTP subfolders and the recovery mailboxes, and in which wave? | Solution architect | Decides whether P5 receives files or polls channels (GAP-1587; ASM-2720) |
| Who records the legal hold, and in which wave is the hold behaviour releaseable? | Solution architect with Legal counsel | Decides the owner of the hold and whether wave 1 can claim REQ-DCM-016 (GAP-1581; ASM-2714) |
| Which request carries a generated document from rwb-comms, and who approves the template version used? | Solution architect with Legal counsel | Decides the generated-document contract shared by notices and contracts (GAP-1580; ASM-2713) |
| What is the signature record, and which part of the e-signature journey lands here? | Solution architect with P6 and S2 | Signature capture has no requirement text yet (GAP-1589; ASM-2722) |

# 10. Release slicing proposal

The service is wave 1: it is created with Epic 1 (release 30 November 2026 (tentative)). Each slice is a list of capabilities, not stories.

## 10.1 Wave 0 — platform prerequisites (no product capability of its own)

The service consumes platform contracts before its own work starts: the service template and repositories, the shared libraries including the outbox and inbox library, the Temporal workflow kit, the schema and login provision, the Kafka event platform and naming library, the edge and gateway route, the observability stack, Blob with WORM, and the malware scanning service. These belong to the platform epics and are not capabilities of this product.

## 10.2 Wave 1 — Epic 1 (release 30 November 2026 (tentative))

| Slice | Capabilities | Why now |
|---|---|---|
| 1.1 Store and index | CAP-P5-001, CAP-P5-002, CAP-P5-003 | Nothing is stored, versioned or found until the store, the version chain and the index exist |
| 1.2 Signed types and fields | CAP-P5-005 | The pipeline has no target until Legal and NPA have signed the types and their fields |
| 1.3 One intake | CAP-P5-012 (four scanned paths) | Every later step consumes an intake item, so the intake and its duplicate and size rules come before the pipeline |
| 1.4 OCR | CAP-P5-007 | The case record view is only as good as the text behind it |
| 1.5 Classification | CAP-P5-008 | A document is attached by its type; the low-confidence route is what keeps the attach honest |
| 1.6 Extraction | CAP-P5-009 | The index and the search by field depend on the extracted fields |
| 1.7 Review queue | CAP-P5-010 | No document is attached wrongly once a person can correct in one screen |
| 1.8 Automatic attach | CAP-P5-011 | The Epic 1 outcome, no document is filed by hand, is this slice |
| 1.9 Cross-case search | CAP-P5-004 | A lawyer or auditor finds a document in seconds, in scope, with the search logged |
| 1.10 Checklist and completeness | CAP-P5-006 | A missing document shows on the case without a person checking a list |
| 1.11 Retention class and virus scan | CAP-P5-013 (class and scan) | The class must exist with the first stored document, and no unscanned file is stored |
| 1.12 Sizing, backup and records position | CAP-P5-019 | The forecast, the restore test and the signed position are release gates |
| 1.13 Generated letters and notices | CAP-P5-015 (letters and notices) | The P5 part of notice generation serves rwb-comms in the same wave |

Rationale: the wave-1 slice is the smallest set that delivers the Epic 1 outcome, one document hub with documents found by case and no document filed by hand, and each slice is independently demonstrable. Retention administration and legal hold are not in wave 1 even though REQ-DCM-016 is an Epic 1 Must, because the administration story RWB-AD-021 is an Epic 8 story at wave 4 (GAP-1581; ASM-2714); the class and the scan land in wave 1 so that no document is stored without them.

## 10.3 Wave 2 — Epic 2 (release 31 December 2026 (tentative))

| Slice | Capabilities | Why now |
|---|---|---|
| 2.1 Generated contracts, credit applications and mortgage documents | CAP-P5-015 | The documents of a treatment are produced without re-keying once treatments are live (REQ-DCM-012) |
| 2.2 Field app photos and bills | CAP-P5-016 | An inspection is on the case the same day it is made |
| 2.3 Stage 2 and 3 extraction | CAP-P5-017 | The litigation pack and the treatment record fill themselves |
| 2.4 Discovery and court-ready evidence | CAP-P5-018 | A legal request is answered from one store, with version history and the alteration state |

Rationale: Epic 2 adds the treatment journey and the litigation pack; each of the four slices is what that release needs from the document hub, and each one is independently demonstrable.

## 10.4 Wave 4 — Epic 8 (release 30 June 2027 (tentative))

| Slice | Capabilities | Why now |
|---|---|---|
| 4.1 Retention administration and legal hold | CAP-P5-014 | The hold and the retention classes as administered policy follow the administration story RWB-AD-021 (GAP-1581; ASM-2714) |

## 10.5 Later increments

| Increment | What unlocks it |
|---|---|
| Signature request and the e-signature return path | A signature requirement and its owner (GAP-1589; ASM-2722) |
| Discovery at a contracted response time | A response target from Legal counsel (NFR-073; GAP-1582; ASM-2715) |
| Retention periods in force | Compliance approval of the periods behind each class (DL26; GAP-1584; ASM-2717) |
| A file intake in this service | Only if rwb-integration does not take the channel (GAP-1587; ASM-2720) |

# 11. Acceptance criteria and validation evidence

Each criterion is written GIVEN/WHEN/THEN. The evidence column points at the source criterion that proves it, so a criterion is never invented where the source has one. Every criterion is verified in SIT against synthetic data; no production data is used.

## 11.1 Acceptance criteria

| AC ID | Covers | GIVEN | WHEN | THEN | Evidence |
|---|---|---|---|---|---|
| AC-P5-001 | FR-P5-001, FR-P5-002, NFR-P5-011 | a scanned court notice of 1.2 MB for a case, with source SCAN, and a Word file offered against a settlement agreement | the first is stored and the second is uploaded | one document row exists with the case, the type, the source, version 1 and today's stored date; its field is in the index; the file is in the write-once container at its case and document path; DocumentStored is in the outbox; the same SHA-256 hash comes back on read; the Word file is refused with MSG-P5-001 and nothing is written | AC-P5-001-01, AC-P5-004-01, AC-EXC-P5-001-02 |
| AC-P5-002 | FR-P5-003 | a court notice stored with write-once set | a delete and a content replace are attempted through the service and directly on the container | each attempt is refused with MSG-P5-002; the hash and the row are unchanged; an audit event DOCUMENT_CHANGE_REFUSED is written per attempt with the document and the caller | AC-ALT-P5-001-01 |
| AC-P5-003 | FR-P5-004, FR-P5-005 | a document with three versions | the versions are read, and a superseded version is requested | three rows exist, each with its version, its previous version, its source, its date and its hash; the superseded version is returned; no other store holds an authoritative copy | AC-P5-001-01, AC-ALT-P5-020-01 |
| AC-P5-004 | FR-P5-006 | an original court notice handed to a law firm with a due-back date | the movement is recorded and the due-back date passes | one custody row names when it moved, from where, to where, the holder and the due-back date; the overdue message MSG-P5-004 names the document, the holder and the date | FSD P5 A2.1.3.1 VR-P5-001-3 (MSG-P5-004); TSD P5 v2 API-P5-007 and LOV-CUSTODY |
| AC-P5-005 | FR-P5-007, FR-P5-008 | a case holding 50 documents of which 12 are court notices and 4 were stored in October | the case documents are listed and searched by type with an October range | the uploaded document shows at the top within 5 seconds; the search returns exactly those 4, newest first, with the count; case number, type, stored date and the matching field value are on each result | AC-P5-004-01, AC-ALT-P5-004-01 |
| AC-P5-006 | FR-P5-009, FR-P5-010, NFR-P5-015 | a litigation user scoped to one team, 40 of 500 documents on cases of another product group, and a case owner whose masking rule hides party names | each searches across documents, the first by type and free text, the second by free text | the first sees no document outside the scope; one access event DOCUMENT_SEARCH carries the user, the criteria, the count and the case IDs; the free-text term appears only as its SHA-256 hash; the second is refused with MSG-P5-020 naming document text and no query runs | AC-P5-006-01, AC-ALT-P5-006-01, AC-ALT-P5-006-02, AC-EXC-P5-006-01 |
| AC-P5-007 | FR-P5-011 | a load of the six types and their fields with the Legal and NPA sign-off, and three faulty loads: one row with no NPA sign-off, one with an unknown retention class and a repeated type code, and one loaded twice | each load is validated and one approver approves | the good load is in force with both sign-off users and dates; each faulty load is refused whole with MSG-P3-027 naming the row, the version in force is unchanged, and the loader cannot approve their own load | AC-P5-003-01, AC-ALT-P5-003-01, AC-EXC-P5-003-01, AC-EXC-P5-003-02, AC-EXC-P5-003-03 |
| AC-P5-008 | FR-P5-012 | a case at LITIGATION holding a demand letter and a court notice, and a case at DEED_IN_LIEU holding a title deed and an appraisal report | the Documents tab opens, and a new checklist version adds guarantor notice for DEED_IN_LIEU from its valid-from date | the checklist shows the four items of the version in force with present and missing marked; the completeness flag is false with one missing type SETTLEMENT_AGREEMENT; the new version takes effect with no code deployed; a stage with no checklist shows its empty state with no flag | AC-P5-016-01, AC-ALT-P5-016-01, AC-ALT-P5-016-02, AC-EXC-P5-016-02 |
| AC-P5-009 | FR-P5-013, FR-P5-014, NFR-P5-003 | the 180-document sample of 30 per type, 500 pages in 125 intake items, a four-page notice with an unreadable page 3, and an OCR contract that returns 503 | the intake workflow runs, and then runs again over completed items | each item is DONE or RESCAN with its page text and quality and its engine version; all 125 items finish inside 60 minutes with 4 workers; the unreadable page is named for rescan; a failed run leaves the item PENDING with its attempt count and alerts the platform administrator; a repeated run calls the OCR contract for no completed item | AC-P5-007-01, AC-ALT-P5-007-01, AC-ALT-P5-007-02, AC-EXC-P5-007-02, AC-EXC-P5-007-03, AC-EXC-P5-007-04 |
| AC-P5-010 | FR-P5-015, NFR-P5-004 | the labelled sample of 180 documents, an item scored 0.62 for court notice and 0.21 for demand letter, an item at the 0.80 threshold, and a classifier that times out or returns a type not in force | classification runs | at least 162 of 180 get their labelled type; the 0.62 item carries the reason LOW_CONFIDENCE with its two candidates; the 0.80 item is classified with no review reason; the timeout records MODEL_UNAVAILABLE with no predicted type and the fallback; the unknown type records UNKNOWN_TYPE with the two highest agreed types; a repeated run classifies nothing twice | AC-P5-008-01, AC-ALT-P5-008-01, AC-ALT-P5-008-02, AC-EXC-P5-008-01, AC-EXC-P5-008-02, AC-EXC-P5-008-03 |
| AC-P5-011 | FR-P5-016, NFR-P5-005 | a typed court notice whose text holds the court, the black case number and two Thai dates, a hearing date read at 0.62, a hearing date of 32 in a month, and an extractor that does not answer | extraction runs | the four fields are in the index with their values and confidences; the 0.62 field and the impossible date are in REVIEW with the value kept; the item whose extraction failed is FAILED with its reason, its fields empty and no attach; the labelled sample meets precision 0.90 and recall 0.90 per field | AC-P5-009-01, AC-ALT-P5-009-01, AC-ALT-P5-009-02, AC-EXC-P5-009-01, AC-EXC-P5-009-02 |
| AC-P5-012 | FR-P5-017, FR-P5-018 | a queue holding a low-confidence item, a stored document with one field in review, and attempted corrections that are empty, of a type not in force, outside the date range, with a field still in review, on a closed case, and a discard with no reason | the reviewer opens the queue and each action is attempted | the queue lists held items and stored documents oldest first with the reason and candidates, limited to scope; a completed correction stores the document and confirms its fields; each faulty action is refused with its message and changes nothing; a valid discard names its reason and leaves the queue | AC-P5-010-01, AC-ALT-P5-010-01, AC-ALT-P5-010-02, AC-EXC-P5-010-01, AC-EXC-P5-010-02, AC-EXC-P5-010-03, AC-EXC-P5-010-04, AC-EXC-P5-010-05, AC-EXC-P5-010-06 |
| AC-P5-013 | FR-P5-019 | a scan carrying a readable case ID, a scan carrying only the account number, a scan whose account number links to two open cases, a scan with neither, a case ID that does not exist, and a scan with no agreed type | intake completes | the first two are stored on their case and the decision record names the match method; the two-candidate item is MULTIPLE with both cases offered and nothing stored; the unmatched and the unknown case ID are NO_MATCH with the OCR text readable and no document row; the untyped item is NO_TYPE; a repeated run writes no second document, record or event | AC-P5-012-01, AC-ALT-P5-012-01, AC-ALT-P5-012-02, AC-EXC-P5-012-01, AC-EXC-P5-012-02, AC-EXC-P5-012-04, AC-EXC-P5-012-03 |
| AC-P5-014 | FR-P5-020 | a branch scan, a partner file in its partner subfolder, a mailbox attachment, a Word file, a 25.1 MB file and a 25.0 MB file, an unknown and a suspended partner, a duplicate of a file already taken in, and a channel that fails twice | the intake runs | one intake row per accepted file with its source, channel, capture time and hash; the Word file goes to the rejected folder with the job record naming it; the larger file is refused with MSG-P5-017 and the 25.0 MB file is accepted; the unknown and the suspended partner write no row; the duplicate writes no second row; the platform administrator is alerted with MSG-P5-008 after the second failed run | AC-P5-013-01, AC-ALT-P5-013-01, AC-ALT-P5-013-02, AC-EXC-P5-013-01, AC-EXC-P5-013-02, AC-EXC-P5-013-03, AC-EXC-P5-013-04, AC-EXC-P5-013-06 |
| AC-P5-015 | FR-P5-021, NFR-P5-030 | an inspection of eight photos and two bills, a capture made offline, a photo with no position, an HEIC photo, and a manifest of three items with two files | the officer syncs | ten documents are on the case with their capture time, position and client file ID, and the bill amount and due date are in the index; the offline capture keeps its capture time and takes the sync date as its stored date; the photo with no position is stored and the officer sees MSG-P5-015; the HEIC photo is refused while the others in the sync are accepted; the short manifest is refused with MSG-GEN-001 and nothing is stored | AC-P5-021-01, AC-ALT-P5-021-01, AC-ALT-P5-021-02, AC-EXC-P5-021-01, AC-EXC-P5-021-02, AC-EXC-P5-021-03 |
| AC-P5-016 | FR-P5-022, FR-P5-023, NFR-P5-012 | a demand letter of class LEGAL10Y, an appraisal report of class GENERAL05Y, a document whose class is not in the retention table, and a file with the EICAR signature | the documents are stored and the retention and scan steps run | each row carries the class of the type version in force and the write-once flag of its type; the qualified class puts the file in the write-once container; the unknown class is listed as RETENTION_CLASS_MISSING and the document is unchanged; the infected file is INFECTED, in quarantine, with no row and no OCR read, an audit event MALWARE_BLOCKED and an alert | AC-ALT-P5-017-01, AC-EXC-P5-017-02, AC-P5-018-01 |
| AC-P5-017 | FR-P5-023, FR-P5-024, NFR-P5-014 | an appraisal report of class GENERAL05Y stored on 1 November 2021 with no legal hold, and a store whose scanning service does not answer | the retention run runs on 6 December 2026, and the scan step runs twice | the document is ARCHIVED in the archive tier with one decision entry DOCRET naming the document, the class, the retention-table version and the expiry date; no document is removed without an entry; while scanning is down no unscanned item is read and an upload is refused with MSG-P5-022 | AC-ALT-P5-017-02, AC-EXC-P5-017-01 |
| AC-P5-018 | FR-P5-025, NFR-P5-013 | a document at the end of its period, and a case under legal hold | the retention run runs before and after the hold is lifted | no document of the held case is archived or deleted while the hold is in place; on release each document returns to its class; every change is a decision entry (GAP-1581; ASM-2714) | REQ-DCM-016, NFR-072; no FSD criterion exists (GAP-1581) |
| AC-P5-019 | FR-P5-026 | an approved treatment and the Legal-approved template version in force, and a draft with one overridable merge value wrong | documents are generated, then the value is corrected and regenerated | the document is stored with its template version and the case data filled; the correction produces the next version with its reason and the earlier draft stays readable; no field is re-keyed | REQ-DCM-012, RWB-E2-017, RWB-E2-026, Arch v5 slide 16 (POST /documents/generate), TSD P5 v2 API-P5-016 and API-P5-017; no FSD criterion exists (GAP-1580) |
| AC-P5-020 | FR-P5-027 | the 10 scanned court notices of the sample with 30 labelled values, a signed contract naming two parties and an amount, a judgment with one field at 0.71, a court case number that does not match its pattern, and a write-once judgment | extraction runs on the stage 2 and 3 types | the court, the case number and the hearing date are on the index and at least 27 of the 30 values match their labels; party names, amount and date are on the contract and masked by role; the 0.71 field is in review and the document is in the queue; the mismatched value is in review with the value read; the write-once file, hash and flag are unchanged | AC-P5-022-01, AC-ALT-P5-022-01, AC-ALT-P5-022-02, AC-EXC-P5-022-01, AC-EXC-P5-022-02 |
| AC-P5-021 | FR-P5-028, FR-P5-029, NFR-P5-019, NFR-P5-020 | a named population of cases and every version of their documents | a discovery production is requested and one document is produced | every document of the population is returned with its metadata, its version history and the date each version was created; the produced document carries its origin, its entry date, its alteration state by hash and the readers | REQ-DCM-017, REQ-DCM-018, NFR-076; no FSD criterion exists (GAP-1582) |
| AC-P5-022 | FR-P5-030, NFR-P5-006, NFR-P5-007, NFR-P5-010 | the forecast volume and a backup set | the volume test runs and a restore is performed in SIT | the store holds the forecast estate of about 5.8 million documents and 2.8 TB with every version and held document; about 860,000 documents a year at 15 percent growth are carried; the restore completes on the bank schedule and its evidence is attached to the release | NFR-004, NFR-069, NFR-071; no FSD criterion exists (GAP-1583) |
| AC-P5-023 | FR-P5-031 | the records management position drafted by the hub owner | Compliance and Legal review it | the position covers storage, backup, legal hold, discovery and disposal, is signed by both, and no document behaviour in release contradicts it | REQ-DCM-020; no FSD criterion exists (GAP-1583) |
| AC-P5-024 | FR-P5-032, NFR-P5-017, NFR-P5-018 | a document action, and a decision log that is unavailable | the action is taken and the record write is attempted | the decision record names the rule version, the classifier and extractor versions and the approver; the attachment is on the interaction ledger; when the record cannot be written nothing changes, MSG-P7-003 is shown and an incident is raised; the chain break drill reports the break the same day | AC-EXC-P5-001-05, AC-EXC-P5-004-05; REQ-DRI-004, REQ-ILG-005 |
| AC-P5-025 | FR-P5-001, FR-P5-002, NFR-P5-031, NFR-P5-024 | a document naming a customer, and a set of events, workflow histories and logs from an intake run | the document is read by three roles and the payloads are inspected | the customer key and the extracted personal values are masked for each role that has no unmasked row; no event, workflow input, history or log holds a personal value, only identifiers; every read is in the access log | AC-P5-015-01, AC-P5-006-01; NFR-039, NFR-040, NFR-042 |

## 11.2 Requirement trace summary

| BR | Capability | Functional requirement | Non-functional requirement | Acceptance criteria |
|---|---|---|---|---|
| REQ-DCM-001 | CAP-P5-001, CAP-P5-007 | FR-P5-001, FR-P5-002, FR-P5-013, FR-P5-014 | NFR-P5-003 | AC-P5-001, AC-P5-009 |
| REQ-DCM-002 | CAP-P5-002 | FR-P5-004, FR-P5-005, FR-P5-006, FR-P5-032 | NFR-P5-017 | AC-P5-003, AC-P5-004, AC-P5-024 |
| REQ-DCM-003 | CAP-P5-001 | FR-P5-003 | NFR-P5-011 | AC-P5-002 |
| REQ-DCM-004 | CAP-P5-005 | FR-P5-011 | NFR-P5-016 | AC-P5-007 |
| REQ-DCM-005 | CAP-P5-008, CAP-P5-010 | FR-P5-015, FR-P5-017, FR-P5-018 | NFR-P5-004 | AC-P5-010, AC-P5-012 |
| REQ-DCM-006 | CAP-P5-007, CAP-P5-009, CAP-P5-017 | FR-P5-013, FR-P5-016, FR-P5-027 | NFR-P5-005, NFR-P5-027 | AC-P5-009, AC-P5-011, AC-P5-020 |
| REQ-DCM-007 | CAP-P5-011 | FR-P5-019 | NFR-P5-025 | AC-P5-013 |
| REQ-DCM-008 | CAP-P5-003, CAP-P5-004 | FR-P5-007, FR-P5-008, FR-P5-009 | NFR-P5-001, NFR-P5-002 | AC-P5-005, AC-P5-006 |
| REQ-DCM-009 | CAP-P5-012 | FR-P5-020 | NFR-P5-025, NFR-P5-026 | AC-P5-014 |
| REQ-DCM-010 | CAP-P5-013 | FR-P5-022, FR-P5-023 | NFR-P5-012 | AC-P5-016, AC-P5-017 |
| REQ-DCM-011 | CAP-P5-006 | FR-P5-012 | NFR-P5-001 | AC-P5-008 |
| REQ-DCM-012 | CAP-P5-015 | FR-P5-026 | NFR-P5-017 | AC-P5-019 |
| REQ-DCM-013 | CAP-P5-012, CAP-P5-016 | FR-P5-021 | NFR-P5-030 | AC-P5-015 |
| REQ-DCM-014 | CAP-P5-019 | FR-P5-030 | NFR-P5-006, NFR-P5-007 | AC-P5-022 |
| REQ-DCM-015 | CAP-P5-019 | FR-P5-030 | NFR-P5-009, NFR-P5-010 | AC-P5-022 |
| REQ-DCM-016 | CAP-P5-014 | FR-P5-025 | NFR-P5-013 | AC-P5-018 |
| REQ-DCM-017 | CAP-P5-018 | FR-P5-028 | NFR-P5-019 | AC-P5-021 |
| REQ-DCM-018 | CAP-P5-018 | FR-P5-029 | NFR-P5-020 | AC-P5-021 |
| REQ-DCM-019 | CAP-P5-013 | FR-P5-024 | NFR-P5-014 | AC-P5-017 |
| REQ-DCM-020 | CAP-P5-019 | FR-P5-031 | NFR-P5-021 | AC-P5-023 |
| REQ-ACA-006 | CAP-P5-004 | FR-P5-009, FR-P5-010 | NFR-P5-015, NFR-P5-024 | AC-P5-006, AC-P5-025 |
| REQ-DRI-004 | CAP-P5-002 | FR-P5-032 | NFR-P5-017, NFR-P5-018 | AC-P5-024 |
| REQ-ILG-005 | CAP-P5-002 | FR-P5-032 | NFR-P5-017 | AC-P5-024 |

BR coverage: all 20 program requirements REQ-DCM-001 to REQ-DCM-020 are covered by at least one functional requirement, and the three cross-cutting requirements the hub serves (REQ-ACA-006, REQ-DRI-004, REQ-ILG-005) are covered too. No BR is left without a functional requirement. Coverage gaps are in the source, not in the trace: REQ-DCM-012, REQ-DCM-016, REQ-DCM-017, REQ-DCM-018, REQ-DCM-019, REQ-DCM-020 and REQ-DCM-014/015 have no FSD feature section, so their product behaviour is taken from the BRD, the TSD operation list, the Ownership Map and the confirmed Architecture v5 constraint, and each one carries a gap row (GAP-1580, GAP-1581, GAP-1582, GAP-1583).

## 11.3 Validation evidence expected before approval

| Evidence | What it proves | Owner role |
|---|---|---|
| Write-once attempt test through the service and on the container | FR-P5-003, NFR-P5-011 | Developer with the security administrator |
| Version chain and hash comparison report | FR-P5-004, FR-P5-005, FR-P5-029 | Developer |
| Search test across scope with the access event extract | FR-P5-007, FR-P5-008, FR-P5-009, FR-P5-010, NFR-P5-002, NFR-P5-015 | Litigation officer with the QA team |
| Signed type load and the three refused loads | FR-P5-011 | Reference data administrator with Legal counsel |
| Checklist by stage and the completeness flag, with a new checklist version taking effect | FR-P5-012, NFR-P5-001 | Litigation officer with the QA team |
| Field app capture and offline sync with the manifest and file-type refusals | FR-P5-021, NFR-P5-030 | Field collector with the QA team |
| Intake run of the four channels with the duplicate, size, type and partner refusals | FR-P5-020, NFR-P5-007 | Document hub owner with the QA team |
| OCR throughput run of 500 pages in 125 items and the rescan cases | FR-P5-013, FR-P5-014, NFR-P5-003 | QA team |
| Classification and extraction evaluation reports on the 180-document sample | FR-P5-015, FR-P5-016, NFR-P5-004, NFR-P5-005 | Center of excellence analyst |
| Review queue refusals and the correction feed | FR-P5-017, FR-P5-018 | Litigation officer with the QA team |
| Automatic attach run with match, multiple, no match and no type | FR-P5-019 | QA team |
| Retention run with a held document, an unknown class and a disposal entry | FR-P5-022, FR-P5-024, FR-P5-025, NFR-P5-012, NFR-P5-013, NFR-P5-014 | Compliance and PDPA officer |
| Malware scan test with the EICAR sample and the scanning outage | FR-P5-023 | Security administrator |
| Decision record and interaction ledger write failure drill | FR-P5-032, NFR-P5-017, NFR-P5-018 | Developer with the QA team |
| Generation and regeneration of a contract, a credit application and a mortgage document | FR-P5-026 | Restructuring officer with Legal counsel |
| Discovery production and court-ready pack review | FR-P5-028, FR-P5-029, NFR-P5-019, NFR-P5-020 | Legal counsel with Internal audit |
| Volume test at the forecast estate and the restore test | FR-P5-030, NFR-P5-006, NFR-P5-010 | IT lead with the QA team |
| Records management position signed by Compliance and Legal | FR-P5-031 | Document hub owner |

# 12. Open questions

The FSD carries no open-question list of its own; the open decisions of the BRD and the non-functional specification are carried forward with their decision IDs, and product-level questions follow. No question is answered by invention: where an answer is assumed, the assumption is named.

| ID | Question | Owner role | Needed by | Blocks | Source |
|---|---|---|---|---|---|
| OQ-P5-01 | Which document types and fields does the hub classify and extract? Six types and 26 fields are counted but only two types name their fields. | Business lead with Legal counsel and the Head of NPA | Before the wave 1 type load | CAP-P5-005, CAP-P5-009 | DL19; GAP-1585; ASM-2718 |
| OQ-P5-02 | How long is each document type kept, and which fields are masked for which role? | Compliance and PDPA officer | Before the wave 1 release | CAP-P5-013, CAP-P5-004 | DL26; NFR-028; GAP-1584; ASM-2717 |
| OQ-P5-03 | Who owns the letter and document templates and the fields filled into them? | Product owner with Legal counsel | Before the wave 2 generation slice | CAP-P5-015 | DL28 |
| OQ-P5-04 | Who builds stage 2 and 3 extraction and document generation: a bank-wide service or this programme? | IT lead with the product owner | Before the wave 2 release | CAP-P5-015, CAP-P5-017 | DL30 |
| OQ-P5-05 | What backup schedule applies, and what restore evidence does each release need? | IT lead | Before the wave 1 release | CAP-P5-019 | NFR-071; DL27; GAP-1583; ASM-2716 |
| OQ-P5-06 | Which service performs OCR, classification and field extraction, and under which contract and version scheme? | Solution architect with the AI product owner | Before wave 1 system test | CAP-P5-007, CAP-P5-008, CAP-P5-009 | GAP-1586; ASM-2719 |
| OQ-P5-07 | Which service owns the branch scanner folders, the partner SFTP subfolders and the recovery mailboxes? | Solution architect | Before wave 1 system test | CAP-P5-012 | GAP-1587; ASM-2720 |
| OQ-P5-08 | Who records the legal hold, rwb-case or rwb-document, and in which wave is the hold released? | Solution architect with Legal counsel | Before the wave 1 release | CAP-P5-014 | GAP-1581; ASM-2714 |
| OQ-P5-09 | What is the response target for an electronic discovery request? | Legal counsel | Before the wave 2 release | CAP-P5-018 | NFR-073; GAP-1582; ASM-2715 |
| OQ-P5-10 | What are the periods behind the retention classes, and who approves them? | Compliance and PDPA officer | Before the wave 1 release | CAP-P5-013 | NFR-028; GAP-1584; ASM-2717 |
| OQ-P5-11 | Which classification applies to each document type, and who sets it? | Compliance with Security | Before the wave 1 release | CAP-P5-001, CAP-P5-013 | NFR-047; DL26 |
| OQ-P5-12 | Is the document table still an extension of the ACE Attachment object, or a P5-owned table? | Data architect | Before the wave 1 migration | CAP-P5-001, CAP-P5-002 | GAP-1588; ASM-2721 |
| OQ-P5-13 | What signature capture is required in this service, and where does the e-signature journey sit? | Solution architect with P6 and S2 | Before the wave 2 release | CAP-P5-002, CAP-P5-015 | GAP-1589; ASM-2722 |
| OQ-P5-14 | Which key identifies the customer on a document: the ACE person key of the FSD or the party id of the TSD? | Data architect | Before the wave 1 migration | CAP-P5-001 | GAP-1594; ASM-2726 |

# 13. Approval

The approval table is deliberately empty: this version is Draft and no approval is recorded in this run. A missing approval is carried as an assumption, not as an answer (GAP-1592; ASM-2711).

| Role | Name | Decision | Date | Notes |
|---|---|---|---|---|
| Product Owner | | | | |
| FDA | | | | |

# Appendix A. Sources and evidence

| Source | Sections used |
|---|---|
| Recovery Workbench Business Requirements Program v4 | 2 (business outcomes), 5.5 (P5 requirements, REQ-DCM-001 to REQ-DCM-020), 6 (NFR-001 to NFR-078), 7 (constraints), 8 (release plan), 9 (open decisions DL19, DL26, DL27, DL28, DL30) |
| Recovery Workbench Business Requirements Epic 1 v4 | 3.5 (P5 document hub at development detail, RWB-E1-024 to RWB-E1-057), 4 (program requirements met), 6 (acceptance), 7 (open decisions) |
| Recovery Workbench Business Requirements Epic 2 v2 | 3.5 (P5 document hub, RWB-E2-017, E2-024, E2-025, E2-026) |
| Recovery Workbench FSD P5 Document hub v3 | Document control, existing capability check, A1 (context and scope), A2.1 to A2.22 (functional decomposition, validation rules, field catalog, roles, acceptance criteria and background events), Requirements served (REQ-DCM-001 to REQ-DCM-020), Screens (SCR-30, SCR-31, SCR-32) |
| Recovery Workbench TSD P5 Document hub v2 | T3.1 to T3.3 (objects, lists of values, relationships), T5 (events), T6 (role matrix), T7 (non-functional targets), Appendix T-A (API-P5-001 to API-P5-017) |
| Recovery Workbench Architecture v5 | Slides 8, 9, 16 (P5 contract), 21 (immutable Blob), 41 (service catalogue), 42 (event catalogue EV-16, EV-17, EV-28), 44 (job map JOB-12, JOB-17), 45 (architect questions and PDPA) |
| Recovery Workbench Temporal and Drools Design v1 | L2 namespaces, L3 workflow kit (document intake), task queue per service, KEDA scaling, Schedules |
| Recovery Workbench Microservice Ownership Map v1 | The 12 tables, the 17 operations, EV-16 and EV-17, JOB-12 and JOB-17, and DocumentIntakeWorkflow owned by P5 |
| Recovery Workbench Non Functional Specification v3 | 1 (targets on one page), 2 (volumes), 3.1 to 3.12 (requirements by quality characteristic) |
| Recovery Workbench Microservice Story Template and Rules v1 | R1 (user decisions), R3 (source precedence and default rulings), R5 (target structure, DP table, wave map), R8 (outputs), R9 (gaps and assumptions) |
