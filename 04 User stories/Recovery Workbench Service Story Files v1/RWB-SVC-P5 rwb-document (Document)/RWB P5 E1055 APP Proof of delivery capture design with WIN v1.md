# RWB-P5-E1055-APP Proof of delivery capture design with WIN

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1055-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-055 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP05, DP07, DP09, DP10, DP11, DP15, DP18, DP19 |
| Parallel lane | L-P5-P |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P6-E1055-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (no FR mapped to REQ-OCC-003, REQ-ILG-004, REQ-DRI-006) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-055 for rwb-document, so the dispatched notice and the WIN proof of delivery are held as write-once document evidence on the case with the document reference the dispatch file names. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **the dispatched notice and the WIN proof of delivery held as write-once documents on the case with the document reference the dispatch file names and the delivery facts on the receipt**, so that **R-LIT-07 can attach the proof and start the notice period from the delivered date without anyone chasing paper**.

Inside `rwb-document` this is the dispatch-evidence capability of the document service:

- Service `rwb-document`, schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with event names `rwb.document.<Event>.v1`, Temporal task queue `rwb-document` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.document`, module `dispatchevidence`.
- rwb-document owns document metadata, custody, OCR text and fields, signatures and retention in `rwb_document` (Architecture v5 slides 16, 41 and 20); the files themselves are Azure Blob under WORM (slide 16).
- This story is the **rwb-document part of legacy RWB-E1-055**: the dispatched notice and the WIN proof of delivery are held as documents on the case, write-once under the retention class of their document type, and their document ID is the document reference that the INT-14 dispatch file carries (legacy section 2, section 4 steps 2 to 4).
- rwb-comms owns the dispatch, the acknowledgment, the notice state, the barcode, the `v_ace_pod` read and the NoticeDispatched and NoticeDelivered events. rwb-case and P1 own the notice-period timer and the ACE proof of delivery. This slice owns only the document evidence and its metadata, custody-free, in `rwb_document`, and answers rwb-comms through the published contract RWB-P6-E1055-CON.

The notice and the receipt reach this slice as a file and a set of facts; what this slice gives back is one document row per document on the case, the delivery facts as document fields on the receipt, the write-once flag and the retention class taken from the document type in force, the file in the write-once container, and one `DocumentStored` event (Architecture v5 slide 42, event 16). The document types and their retention classes are the six of the type table version `DOCTYPE-2026.11` in force from 30 November 2026 (FSD P5 AC-ALT-P5-003-01), loaded and approved by RWB-P5-E1025-APP; this slice reads them and never types a type, a flag or a class in code.

### 2. Business rationale

Proof of delivery is chased by phone today, and a notice period counted from the print date can be challenged in court (legacy section 2). The dollar consequence is the notice itself: a demand letter or a court notice whose delivery cannot be evidenced from a stored document is a letter the bank may have to send again, and a notice period that starts on the wrong date is a period the borrower can dispute. The legacy story fixes the missing capability in one sentence — the case has to show what was sent and when it arrived — and its flow carries the document reference in the dispatch file (step 2) and the delivery facts of the acknowledgment and of the proof of delivery (steps 4 to 7).

This story is the rwb-document slice of that legacy key. It carries the evidence, not the dispatch: the notice state machine, the barcode, the acknowledgment, the `v_ace_pod` read, the reconciliation break list and the NoticeDispatched and NoticeDelivered events stay with rwb-comms in RWB-P6-E1055-APP; the notice-period timer stays with rwb-case in RWB-P3-E1055-APP; the ACE proof-of-delivery records and their freshness stay with rwb-source-data in RWB-P1-E1055-APP. What is left for rwb-document, and what this story builds, is the part that makes R-LIT-07 executable: a document on the case that cannot be altered inside its retention period, the delivery facts on that document, and a document reference that the dispatch file and the case screen can both name.

The reason it has to be a document and not a field on the notice is the retention regime. A legal type is held in a write-once container and cannot be altered or deleted inside its retention period (NFR-029, FSD P5 A2.1, AC-ALT-P5-001-01), and a document at the end of its retention period is disposed of or extended by a recorded decision and never removed silently (NFR-074). A notice PDF that a later edit could overwrite would fail both, so the notice becomes a document with `write_once` true and retention class `LEGAL10Y` from its type, and a change becomes a new version. The same rule gives the WIN receipt its place: the receipt is the partner's evidence, it arrives as a file with source `PARTNER` (LOV-DOC-SOURCE), and its facts — barcode, callback date, delivery status and sent type — are written as document fields beside it, so the case carries the proof and the facts that prove it.

The slice also keeps the service boundary honest. rwb-document is the system of record for documents (FSD P5 A2.19, DT06, REQ-DCM-002), not for notices, and it reads no ACE view and no other service's table (DP-01, DP-05 as a prohibition). The notice facts arrive through the published contract RWB-P6-E1055-CON, one hop with a 2 s timeout (DP-11), and the delivery facts of the legacy `v_ace_pod` read reach the receipt through that same answer rather than a document-side read of ACE data (DF-ACE-253 to DF-ACE-258). The slice serves REQ-OCC-003 (proof of delivery returns to the case), REQ-ILG-004 (what happens in an interaction is recorded against that interaction, by the ledger's owner from the event) and REQ-DRI-006 (no component calls a system of record directly).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P6-E1055-CON | The published rwb-comms contract of this legacy key: the notice read and the dispatch reference, with a fake, so the notice facts and the document reference arrive in a published shape and not from a `rwb_comms` table (DP-11, C dependency) |
| RWB-P5-E1025-APP | The document type table `document_type` with version `DOCTYPE-2026.11` in force from 30 November 2026, the six types, and the `write_once` flag, the retention class and the field list of each type |
| RWB-P5-E1024-APP | The store path this slice uses: `POST /cases/{caseId}/documents` returns the document in state COPY_PENDING with the upload link, the store command writes the document row, the field rows and the outbox row in one transaction, and the `copyPending` activity sets state STORED with `storage_ref` |
| RWB-PLT-TE006-CON | The outbox, inbox and idempotency library, so `rwb.document.DocumentStored.v1` is written in the same transaction as the document row (DP-09) |
| RWB-PLT-E1043-CON | The reference-data client library for LOV-DOC-SOURCE, LOV-RETENTION and LOV-SCAN-RESULT (DP-07) |
| RWB-PLT-E1044-CON | The per-service Flyway sequence that carries the document and type migrations of this service as ordered steps (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route that carries the documents tab of SCR-30 to rwb-document, one hop (DP-19) |
| RWB-PLT-E1071-CON | The workflow kit, present in the service template; this story runs no Schedule and contributes no activity to it (DP-10 as a prohibition) |
| RWB-P3-E1043-CON | The reference-data contract of rwb-case, which resolves the three lists; it reaches this story through the client library only |

Business preconditions carried from RWB-E1-055:

- The document type table version `DOCTYPE-2026.11` is in force from 30 November 2026 with `DEMAND_LETTER`, `COURT_NOTICE`, `APPRAISAL_REPORT`, `TITLE_DEED`, `SETTLEMENT_AGREEMENT` and `GUARANTOR_NOTICE`; `COURT_NOTICE` holds retention class `LEGAL10Y` with `write_once` true, `APPRAISAL_REPORT` holds `GENERAL05Y` with `write_once` false, and a demand letter is held with class `LEGAL10Y` and `write_once` true (FSD P5 AC-ALT-P5-003-01, AC-ALT-P5-017-01).
- The write-once container `rwb-docs-legal` and the standard container `rwb-docs` exist, with the path `rwb-docs-legal/{caseId}/{documentId}/v1` (FSD P5 AC-P5-001-01).
- The caller is rwb-comms through the contract (the notice path) or the receipt intake (source `PARTNER`); a reader holds the Documents right R with the case in scope.
- The notice `N-0001` of case `RC-2026-000123` exists in rwb-comms with notice type `DEMAND`, contract `CT-77001`, sent date 26 November 2026, barcode `RR123456789TH` and sent type `NPL` (legacy AC1 and AC2), and the WIN sample `WIN-POD-SAMPLE-v1` of 25 records is the receipt sample of the legacy interface story (legacy AC3).
- The feature flag `rwb.document.dispatch-evidence` is on; off means the slice stores no dispatch evidence and answers the caller with the store path's refusal, never with a silent success.

The field names of the rwb-comms answer that carry the notice and its document reference are Not specified in the source documents (GAP-1043; ASM-1991). The two module specifications this story reads — FSD P5 Document hub v3 and TSD P5 Document hub v2 — both carry the status "In review"; they are read as the source in force for a draft story and no approval is claimed.

### 4. Flow

1. rwb-comms, through the contract RWB-P6-E1055-CON, asks this slice for the document evidence of a notice: the notice reference, the case ID, the generated PDF reference and, for the proof of delivery, the receipt file of the business date. The call is one hop, with a 2 s timeout (DP-11), and carries an `Idempotency-Key`.
2. `DispatchEvidenceService`: reads the notice answer — notice type, the generated PDF, the template version and the document reference — and stores the notice PDF through `POST /api/recovery/document/v1/cases/{caseId}/documents` with source `GENERATED` and the document type of the notice. The document type of a dispatched notice is `DEMAND_LETTER` for notice type `DEMAND`; the mapping between a notice type and a document type is Not specified in the source documents (GAP-1044; ASM-1992).
3. `DispatchEvidenceService`: reads the type row in force from `document_type` (`valid_from` and `valid_to`) and takes `write_once`, `retention_class` and the field list from it: a demand letter is `write_once` true with class `LEGAL10Y`, a court notice is `write_once` true with class `LEGAL10Y`, and an appraisal report is `write_once` false with class `GENERAL05Y` (FSD P5 AC-ALT-P5-003-01). The caller never supplies the flag or the class.
4. The store path of RWB-P5-E1024-APP, in one transaction in `rwb_document`: writes the `document` row with `doc_version` 1 and state COPY_PENDING, writes the `document_field` rows of any field the type defines that the answer carries, and writes the `rwb.document.DocumentStored.v1` row to the outbox. A document so created answers with its document ID.
5. `DispatchEvidenceService`: returns the document ID to rwb-comms as the document reference that the INT-14 dispatch file carries for that notice (legacy section 4 step 2, DF-LEG-017). From here on the dispatch file names the document, and the notice carries the same reference.
6. `ProofOfDeliveryDocumentService`: when the receipt of a business date arrives, stores the receipt file with source `PARTNER` and the document type the type table in force holds for a proof-of-delivery receipt (the type code is Not specified in the source documents (GAP-1044; ASM-1992)), and writes the delivery facts as document fields through `DocumentFieldWriter`: barcode `RR123456789TH`, callback date `2026-11-28`, delivery status `DELIVERED` and sent type `NPL` for business date `2026-11-30`. The field names used in `document_field` for those facts are Not specified in the source documents (GAP-1045; ASM-1993).
7. `DocumentFieldWriter`: writes one `document_field` row per delivery fact with `field_name`, `field_value` and the confidence the answer carries, inside the same transaction as the receipt document row; a fact the type's field list does not hold is refused rather than stored, so the index of the case is never wider than the type in force.
8. `WriteOnceGuard`: on every change request against a document whose row carries `write_once` true, refuses a content replace and a delete inside the retention period with MSG-P5-002, leaves the row and its `content_sha256` unchanged, and writes the audit event `DOCUMENT_CHANGE_REFUSED` with the document ID and the caller (FSD P5 AC-ALT-P5-001-01).
9. `DocumentEventPublisher`: writes `rwb.document.DocumentStored.v1` to the outbox inside the store transaction, keyed by caseId; the relay publishes it on `rwb.document.events.v1` with `documentId`, `caseId`, `documentType`, `source` and `storedAt` and no personal data (Architecture v5 slides 11 and 42). The `copyPending` activity of the workflow kit then writes the file to `rwb-docs-legal` at `rwb-docs-legal/{caseId}/{documentId}/v1` and sets state STORED.
10. A reader opens the documents tab of the case through the gateway-bff composite route (DP-19): `GET /api/recovery/document/v1/documents/{documentId}` returns the metadata, the version list and the fields, and `GET /api/recovery/document/v1/documents/{documentId}/content` returns the file whose SHA-256 is the `content_sha256` of the row.
11. The same receipt file for the same business date stored twice returns the existing document ID, leaves one document row on the case, and the repeat is counted under R-UNI-40. The interaction-ledger entry of the letter and the notice-period timer are taken by their owners from the events, not by this slice.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A content replace or a delete inside the retention period of a write-once document | Refused; the document row and its `content_sha256` are unchanged; the audit event `DOCUMENT_CHANGE_REFUSED` is written with the document ID and the caller | MSG-P5-002 | AC3 |
| X2 | The document type of the notice or of the receipt is not in the type table in force, or the type carries no retention class | Refused; nothing is stored and no event is written | None in this slice; the store path answers with MSG-P5-006 | AC1, AC2 |
| X3 | The receipt file fails the virus scan on intake | Refused with 422; the file stays in the quarantine container and no document row exists; the receipt is not evidenced until a clean file arrives | MSG-P5-016 | AC2 |
| X4 | The rwb-comms contract does not answer within 2 s, or its breaker is open | Refused with 503; nothing is stored; the breaker shields rwb-comms and the call is not retried inside this service | MSG-GEN-006 | AC1 |
| X5 | The outbox row cannot be written with the document row | The transaction aborts; no document row, no field row and no event; the repeat is safe because the duplicate check runs before the insert | MSG-P7-003 | AC5 |
| X6 | The relay is down when the store commits | The document row, the fields and the outbox row are committed together; the event is published once when the relay recovers, with no second document | None | AC5 |
| X7 | The same receipt file for the same business date arrives twice | The existing document ID is returned; one row remains and the repeat is counted | None | AC6 |
| X8 | The dispatch file names a document reference this service does not hold | The read answers 404; no document is invented and the case screen shows the reference as unresolved to the owner | None in this slice; the 404 message ID is the store path's | AC4 |
| X9 | The caller's role holds no Documents right for the action, or the case is outside the scope | Refused before anything is read or written | MSG-P4-002, MSG-P4-003 | AC4 |

The ACE batch check of the legacy BR4 and the WIN held-row list are not exception paths of this slice: they belong to the rwb-comms dispatch slice (RWB-P6-E1055-APP) and to the data product of RWB-P1-E1055-APP, and the notice data product staleness message MSG-P1-001 is raised there, not here.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the `rwb_document` baseline, the type table of RWB-P5-E1025-APP, the store path of RWB-P5-E1024-APP and the published rwb-comms contract RWB-P6-E1055-CON with its fake; the rwb-case and rwb-source-data answers in the criteria are mocks inside that fake |
| Negotiable | The document types, the write-once flags, the retention classes and the receipt field names are rows of the type table and of the contract; the story fixes the store, the write-once refusal, the event and the read, and names no type and no field in code |
| Valuable | The case carries the notice and its proof of delivery as evidence, the notice period can start from a delivered date that a document supports, and the dispatch file names a document the case holds |
| Estimable | Two services classes, one field writer, one guard, one event publisher and a set of reads already on the store contract |
| Small | Fits one sprint with its tests, as a secondary slice of the legacy key |
| Testable | Every criterion in section 7 is one automated test over the stored documents, with every cross-service answer stubbed |

### 7. Acceptance criteria

```gherkin
Feature: Proof of delivery capture design with WIN — the rwb-document evidence

  Background:
    Given document type table version "DOCTYPE-2026.11" is in force from 30 November 2026 with "DEMAND_LETTER", "COURT_NOTICE", "APPRAISAL_REPORT", "TITLE_DEED", "SETTLEMENT_AGREEMENT" and "GUARANTOR_NOTICE"
    Given type "DEMAND_LETTER" has write_once true and retention class "LEGAL10Y"
    Given type "COURT_NOTICE" has write_once true and retention class "LEGAL10Y"
    Given type "APPRAISAL_REPORT" has write_once false and retention class "GENERAL05Y"
    Given the rwb-comms contract mock returns notice "N-0001" of case "RC-2026-000123" with notice type "DEMAND", contract "CT-77001", sent date 26 November 2026, barcode "RR123456789TH", sent type "NPL" and its document reference
    Given the rwb-source-data contract mock returns the interaction-ledger reference for an outbound "LETTER" entry of case "RC-2026-000123"

  Scenario: AC1 The dispatched notice is stored as a document on the case (new, D-RCV-60)
    Given notice "N-0001" of case "RC-2026-000123" is in state "Generated" with notice type "DEMAND" and its PDF has been generated
    Given the rwb-comms contract mock returns the generated PDF of notice "N-0001" with its template version and the document reference it expects the dispatch file to carry, the field name of that reference being Not specified in the source documents (GAP-1043; ASM-1991), and notice type "DEMAND" mapping to document type "DEMAND_LETTER", that mapping being Not specified in the source documents (GAP-1044; ASM-1992)
    When rwb-document stores the notice PDF on case "RC-2026-000123" through POST /api/recovery/document/v1/cases/{caseId}/documents with source "GENERATED"
    Then one document row exists with case "RC-2026-000123", document type "DEMAND_LETTER", source "GENERATED", write_once true, retention class "LEGAL10Y" from type table version "DOCTYPE-2026.11", doc_version 1 and its content_sha256
    And the file is in container "rwb-docs-legal" at "rwb-docs-legal/{caseId}/{documentId}/v1"
    And the document ID of that row is the documentReference that the INT-14 dispatch file carries for notice "N-0001"
    And rwb-document writes no custody row, no interaction-ledger entry and no timer for that store

  Scenario: AC2 The WIN receipt is stored with the delivery facts (new, D-RCV-60)
    Given the rwb-comms contract mock returns the WIN receipt of business date 2026-11-30 for case "RC-2026-000123" with barcode "RR123456789TH", callback_date 2026-11-28, delivery_status "DELIVERED" and sent_type "NPL"
    Given the document type the type table in force holds for a proof-of-delivery receipt is Not specified in the source documents (GAP-1044; ASM-1992)
    When rwb-document stores the receipt file with source "PARTNER"
    Then one document row exists for case "RC-2026-000123" with source "PARTNER", that document type, doc_version 1 and its content_sha256
    And one document_field row per delivery fact is written with field_name, field_value and confidence, the field names of the receipt being Not specified in the source documents (GAP-1045; ASM-1993)
    And the values are "RR123456789TH", 2026-11-28, "DELIVERED" and "NPL" character for character as the receipt carries them
    And the case holds one document for the receipt of business date 2026-11-30, whether a receipt is one document per file or one per notice being Not specified in the source documents (GAP-1045; ASM-1993)

  Scenario: AC3 A write-once document is refused a change inside its retention (new, D-RCV-60)
    Given the demand letter of notice "N-0001" on case "RC-2026-000123" is stored with write_once true and retention class "LEGAL10Y"
    When a content replace and a delete of that document are attempted through the document store and directly on container "rwb-docs-legal" inside the retention period
    Then each attempt is refused with MSG-P5-002
    And the document row and its content_sha256 are unchanged
    And an audit event "DOCUMENT_CHANGE_REFUSED" is written for each attempt with the document ID and the caller

  Scenario: AC4 The evidence is served in one hop within 2 s (new, D-RCV-60)
    Given the authorisation decision of rwb-access grants role "RW-LITOFF" the Documents right "R" with scope on case "RC-2026-000123"
    When the litigation officer opens the documents tab of case "RC-2026-000123" and GET /api/recovery/document/v1/documents/{documentId} is called through the gateway-bff route
    Then the answer carries the metadata, the version list and the extracted fields of the document within 2 s
    And the gateway-bff route calls rwb-document once, one hop, and rwb-document calls no other service to answer the read
    And GET /api/recovery/document/v1/documents/{documentId}/content returns the file whose SHA-256 is the content_sha256 of the row
    And a caller whose role holds no Documents right is refused before the read with MSG-P4-002, and a case outside the scope with MSG-P4-003

  Scenario: AC5 DocumentStored leaves in the store transaction (new, D-RCV-60)
    Given the outbox library of the service template and the relay of rwb.document.events.v1
    When the demand letter of AC1 is stored
    Then one rwb.document.DocumentStored.v1 row is in the outbox in the same transaction as the document row and its document_field rows
    And when that transaction commits the relay publishes the event on rwb.document.events.v1 keyed by caseId with documentId, caseId, documentType, source and storedAt
    And the payload carries no personal data, no field value and no file content
    And a transaction that fails leaves no document row, no field row and no outbox row

  Scenario: AC6 The same receipt stored twice gives one document (new, D-RCV-60)
    Given the WIN receipt of business date 2026-11-30 for case "RC-2026-000123" is stored from source "PARTNER"
    When the same receipt file with the same content_sha256 for the same business date is stored again on that case
    Then the existing document ID is returned and the case still holds one document row for that receipt
    And the repeat is counted under rule R-UNI-40
    And no second DocumentStored is written to the outbox for the repeat

  Scenario: AC7 No ledger entry and no timer from rwb-document (new, D-RCV-60)
    Given the rwb-source-data ledger listener mock records the interaction entries it writes from rwb.document.DocumentStored.v1
    Given the rwb-case contract mock records the notice-period timers it starts from NoticeDelivered of notice "N-0001"
    When the demand letter of AC1 and the WIN receipt of AC2 are stored and the relay publishes their DocumentStored events
    Then rwb-document writes no interaction-ledger entry and starts no "NOTICE_PERIOD" timer
    And the outbound "LETTER" entry for case "RC-2026-000123" is written by rwb-source-data from the event
    And the "NOTICE_PERIOD" timer on case "RC-2026-000123" is started by rwb-case from NoticeDelivered, not from a document event
    And the notice state, the sent date and the delivered date are read-only facts of rwb-comms in this slice
```

The seven criteria above are new and test only this deliverable: the two documents on the case, the delivery facts as document fields, the write-once refusal, the read, the event, the idempotent store and the prohibitions that keep the ledger and the timer with their owners. This story owns no legacy acceptance criterion: legacy AC1 to AC11 of RWB-E1-055 are held by the primary slice rwb-comms in RWB-P6-E1055-CON and RWB-P6-E1055-APP, by the timer slice in RWB-P3-E1055-APP and by the ACE data slice in RWB-P1-E1055-APP, and legacy test case TC-E1-055-12 belongs to RWB-P6-E1055-APP. No legacy criterion text is copied into this section.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR2 | A notice period starts only from the delivery date on the proof of delivery; in this slice the delivered date is a document field of the receipt and the timer is rwb-case's (legacy BR2) | CTL-15; R-LIT-07; legacy BR2 |
| BR4 | A `v_ace_pod` row is read only when the ACE batch for source WIN is COMPLETE for its business date, and a row with an unknown reference is held; the check and the read are rwb-comms' in RWB-P6-E1055-APP, the data product freshness is RWB-P1-E1055-APP's, and this slice stores only the receipt that answer names (legacy BR4) | ACE batch record; INT-15 error handling; legacy BR4 |
| BR6 | The same receipt twice produces one effect and the repeat is counted (legacy BR6) | R-UNI-40; legacy BR6 |
| BR7 | A write-once document is never changed or deleted inside its retention period; a change is a new version | NFR-029; FSD P5 A2.1 and AC-ALT-P5-001-01; DT06 |
| BR8 | A document reaching the end of its retention period is disposed of or extended by a recorded decision and is never removed silently, and every document type carries a retention class that sets how long the document is kept | NFR-074; NFR-028; FSD P5 A2.17 |
| BR9 | The write-once flag, the retention class and the field list of a type come from the document type table version in force, never from the caller; no value a business person may change is written in code | BR-P5-004; FSD P5 A2.4.3.1; TSD P5 T3.1 (document_type) |
| BR10 | The document reference the INT-14 dispatch file carries is the document ID of the stored notice PDF; the reference is data read through the rwb-comms contract and is never derived from a case number, a notice number or a file name | Legacy RWB-E1-055 section 4 step 2; DF-LEG-017 |
| BR11 | rwb-document writes only its own schema: no `v_ace_*` view, no `public` table and no other service's table is read, and the case, the notice and the ledger arrive through their owners' contracts | DP-01; DP-05; Architecture v5 slides 20 and 41 |
| BR12 | rwb-document writes no interaction-ledger entry and starts no timer; the ledger belongs to rwb-source-data and the notice-period timer to rwb-case | DP-18; DP-10; Architecture v5 slide 20 |
| BR13 | The receipt carries the delivery facts as document fields so that the case shows what was delivered and when, and a fact the type's field list does not hold is refused rather than stored | FSD P5 A2.9; TSD P5 T3.1 (document_field); legacy section 4 steps 4 to 7 |

Target statements that make these rules hold in `rwb-document`:

- BR7 is executed by `WriteOnceGuard` on every change request and by the blob path being immutable per version, with the container's own WORM policy behind it; the row, the `content_sha256` and the file stay as stored, and the attempt is recorded as the audit event `DOCUMENT_CHANGE_REFUSED` (FSD P5 AC-ALT-P5-001-01, NFR-029).
- BR8 is executed by carrying the retention class on the document row from the type in force and by leaving every expiry action to the monthly retention job of RWB-P5-E1052-APP; this slice stores, it never archives, extends or disposes.
- BR9 is executed by reading `document_type` in the version in force (`valid_from` and `valid_to`) inside the same service, by the three lists arriving through the reference-data contract (DP-07), and by a boundary test that fails the build when a type code, a retention class or a source value appears in Java.
- BR10 is executed by returning the document ID of the stored notice PDF as the document reference, so the dispatch file, the notice and the case screen all name the same document; the reference is a value, not a formula.
- BR11 is executed by the schema and login per service and by the boundary test that fails on any cross-schema read; the notice facts arrive in the contract answer and no `v_ace_*` view is opened by this service (DP-01, DP-05).
- BR12 is executed by the absence of a ledger call and of a Schedule in this story: the `LETTER` entry is written by rwb-source-data from `DocumentStored` or from `NoticeDispatched`, and the `NOTICE_PERIOD` timer by rwb-case from `NoticeDelivered` (DP-18, DP-10).
- BR13 is executed by `DocumentFieldWriter`, which writes one `document_field` row per fact of the type's field list and refuses a fact outside it, so the index of the case is never wider than the type in force.

### 9. State transitions

No case state machine in this story: the slice changes no case status and starts no timer (TSD P5 T4). It uses the document lifecycle of the store path — COPY_PENDING to STORED, as RWB-P5-E1024-APP defines it and as RWB-P5-E1026-APP reads it — and reads the notice states of rwb-comms as facts:

| From | Event | Condition | To |
|---|---|---|---|
| (no document row) | the store transaction commits with the outbox row | The type is in force and the caller holds the Documents right | `document.state` = COPY_PENDING, `doc_version` 1 |
| COPY_PENDING | the `copyPending` activity of the workflow kit stores the file and sets `storage_ref` | The container accepts the write and the SHA-256 matches `content_sha256` | STORED |
| COPY_PENDING | the copy fails | The container refuses the write or the storage product does not answer | COPY_PENDING, retried by the next run of the activity |
| STORED, `is_active` = true | a new version is added with `POST /documents/{documentId}/versions` on the latest version | The new file passes the type and signature checks | the earlier row becomes the superseded version with `is_active` = false and `previous_version_id` on the new row, which is COPY_PENDING then STORED; both versions stay readable |
| STORED, `write_once` = true | a content replace or a delete inside the retention period | The retention period has not ended and no legal hold release exists | no transition: refused with MSG-P5-002, the row and the file unchanged |

The notice states Generated, Sent and Delivered are read-only facts of rwb-comms in this slice: this story never writes them, and the `NOTICE_PERIOD` timer that rwb-case starts from `NoticeDelivered` is not a transition of any `rwb_document` row. The end-of-retention states — ARCHIVED, LISTED, HELD and EXCEPTION of LOV-RETENTION-ACTION — belong to the monthly retention job of RWB-P5-E1052-APP, which writes `retention_action`; this slice writes no such row.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-document service identity (the rwb-document login, DP-02) | Stores the notice PDF and the receipt, writes the field rows, writes the outbox row, serves the reads and refuses a change to a write-once document |
| rwb-comms service identity, through RWB-P6-E1055-CON | Asks for the document evidence of a notice and receives the document reference; reads no `rwb_document` table directly |
| Decision-record library identity | Writes the DOCATT record of the store path as RWB-P5-E1024-APP invokes it; this slice writes no second record and no new decision code (DP-03 is not a pattern of this story) |
| SY-DATALOAD, data load | Runs the receipt load that hands the partner file to this slice; the WIN outbound file itself is rwb-comms' and rwb-integration's (legacy authority table) |
| RW-LITOFF, litigation officer | Reads the notice document, the receipt, its delivery facts and its versions inside the scope (Documents R, Litigation R) |
| RW-CASEOWN, case owner | Reads the documents of the case inside the scope (Documents R) |
| RW-PLATADM, platform administrator | Reads the document and its state on SCR-30, including a COPY_PENDING document; reruns nothing, because this slice runs no job or Schedule |
| RW-DATASTEW, data steward | Reads the document index and the receipt facts for a case in scope; writes nothing |
| Nobody | Changes or deletes a write-once document inside its retention period, or writes a notice state, a ledger entry or a timer from this service |

The authorisation decision is taken by rwb-access (DP-08, roles, scope and masking held as data in `rwb_access`) and reaches this slice as the permission decision the service template's guard holds; this story adds no guard of its own and no operation of its own, and the refusal shapes are MSG-P4-002 for a role without the right and MSG-P4-003 for a case outside the scope. TC-E1-055-12, in which RW-PHONECOL is refused the notice dispatch detail, is not a case of this slice: the dispatch detail is rwb-comms' and that test case belongs to RWB-P6-E1055-APP. SY-OCR, the OCR and extraction pipeline, is not used here: the OCR text and the extracted fields of a scanned receipt belong to the intake path of RWB-P5-E1049-APP, and this slice writes the receipt facts it is given.

### 11. Data

| BR Field ID | Entity in `rwb_document` | Field | Read, write or read through the contract |
|---|---|---|---|
| DF-DOC-001 to DF-DOC-011 | `document` | id, case_id, party_id, document_type, source, storage_ref, classification_confidence, review_status, retention_class, write_once, doc_version | Write |
| DF-DOC-004 | `document` | document_type (taken from the type in force, never from the caller) | Write |
| DF-DOC-005 | `document` | source (`GENERATED` for the notice PDF, `PARTNER` for the receipt, from LOV-DOC-SOURCE) | Write |
| DF-DOC-009 | `document` | retention_class (`LEGAL10Y` for a demand letter and a court notice, `GENERAL05Y` for an appraisal report) | Write |
| DF-DOC-010 | `document` | write_once (true for a legal type, false for a general type) | Write |
| DF-DOC-026 | `document` | content_sha256 | Write |
| DF-DOC-025 | `document` | previous_version_id, set only when a new version exists | Write |
| Standard columns | `document` | state, is_active, version | Write |
| DF-DOC-027 to DF-DOC-033 | `document` | captured_at, capture_latitude, capture_longitude, client_file_id, capture_kind, template_id, treatment_id | Not written: the capture columns belong to the field app path of Epic 2 and stay empty in this slice |
| DF-DOC-012 to DF-DOC-017 | `document_field` | id, document_id, field_name, field_value, confidence, confirmed_by | Write (the delivery facts of the receipt) |
| DF-DOC-014 | `document_field` | field_name (the receipt fact: barcode, callback date, delivery status, sent type, with the field names themselves Not specified in the source documents (GAP-1045; ASM-1993)) | Write |
| DF-DOC-015 | `document_field` | field_value (`RR123456789TH`, 2026-11-28, `DELIVERED`, `NPL`) | Write |
| DF-REF-218 to DF-REF-233 | `document_type` | id, doc_type_code, label_en, label_th, write_once, retention_class, field_definitions, the two sign-offs and their dates, table_version, valid_from, valid_to, reference_version_id, classify_threshold | Read (the type row in force) |
| DF-REF-222 | `document_type` | write_once | Read |
| DF-REF-223 | `document_type` | retention_class | Read |
| DF-REF-224 | `document_type` | field_definitions (the field list the receipt facts must match) | Read |
| DF-REF-229 | `document_type` | table_version (`DOCTYPE-2026.11`) | Read |
| DF-DOC-018 to DF-DOC-024 | `document_custody` | id, document_id, moved_at, from_location, to_location, held_by, due_back | Not written: this slice is custody-free and records no movement of an original |
| DF-DOC-091 to DF-DOC-095 | `retention_action` | id, document_id, run_month, action, decision_log_id | Not written: the monthly retention job of RWB-P5-E1052-APP writes it |
| DF-LEG-015 to DF-LEG-023 | rwb-comms notice | id, case_id, document_id, notice_type, sent_date, barcode, callback_date, delivery_status, sent_type | Read through the contract RWB-P6-E1055-CON |
| DF-ACE-253 to DF-ACE-258 | the ACE proof of delivery, behind rwb-comms and rwb-source-data | notice_ref, sent_date, barcode, callback_date, delivery_status, sent_type | Read through the rwb-comms answer; never read here, and no `v_ace_pod` view is opened by this service |
| LOV-DOC-SOURCE, LOV-RETENTION, LOV-SCAN-RESULT | reference data of rwb-case | `SCAN`, `UPLOAD`, `GENERATED`, `PARTNER`, `EMAIL`; the retention classes; `CLEAN`, `INFECTED` | Read through the reference-data contract (DP-07); no list value is written in code |

The two documents of this slice write `document` and `document_field` only, plus their outbox rows. No custody row, no `retention_action` row, no `document_intake` row and no `document_text` row is written here, because custody belongs to the originals path, the retention action to RWB-P5-E1052-APP and the intake, OCR text and extraction to RWB-P5-E1049-APP and its extraction stories. Field IDs are those in the Logical Data Model and Data Dictionary and the TSD P5 T3.1 tables. No `rwb_case` row is copied, no ACE view is read and no personal data enters the event payload, the fields of the event, a log line or a test: the addressee of the notice stays inside the PDF, and the receipt carries a barcode and dates, not a person.

### 12. Contract

#### 12.1 REST operations provided

None new. The four operations this slice uses are the ones of the store and read contract on base `/api/recovery/document/v1`, owner rwb-document (P5), built by RWB-P5-E1024-APP. This story adds no path, no query parameter and no response field, and answers behind them:

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/api/recovery/document/v1/cases/{caseId}/documents` | Store a notice PDF or a receipt on the case: the document row in COPY_PENDING with its metadata, the field rows, the outbox row, and the upload link of the storage product for the file (API-P5-001) | Documents right C, scope applied; rwb-comms for the notice, the receipt intake for the partner file | `Idempotency-Key` header, plus the unique partial index on case, type and active hash |
| GET | `/api/recovery/document/v1/documents/{documentId}` | Read the metadata, the version list and the extracted fields of a document (API-P5-003) | Documents right R, scope applied | Not applicable |
| GET | `/api/recovery/document/v1/documents/{documentId}/content` | Download the file of a document; 503 while the state is COPY_PENDING (API-P5-004) | Documents right R, scope applied | Not applicable |
| POST | `/api/recovery/document/v1/documents/{documentId}/versions` | Add a new version to the latest version of a document; the change of a write-once document is a new version and never a replace (API-P5-005) | Documents right U, scope applied | `Idempotency-Key` header |

The request of the store operation carries the case ID, the document type, the source (`GENERATED` or `PARTNER`), the file reference in the intake container with its SHA-256, and any extracted field the type defines; the answer carries the document ID, the state, the retention class, the write-once flag and the version, and the document ID is the value rwb-comms takes as the document reference of the dispatch file. Errors follow RFC 9457 with `messageId`: 401, 403 (MSG-P4-002, MSG-P4-003), 404, 409 on a version race, 413, 415, 422 (MSG-P5-006, MSG-P5-016), 503 (MSG-GEN-006, MSG-P7-003). The exact request and response field names of the four operations are those of the store contract; the field name by which rwb-comms names the document reference in its own answer is Not specified in the source documents (GAP-1043; ASM-1991).

The rest of the P5 surface — the case document list `GET /cases/{caseId}/documents` (API-P5-002), the checklist read (API-P5-008), the cross-case search (API-P5-009), the review queue and the intake reads (API-P5-010 to API-P5-013), the field review (API-P5-014), the field captures (API-P5-015), the generation and regeneration operations (API-P5-016, API-P5-017) and the custody operation (API-P5-007) — belongs to the other P5 stories; this slice adds none of them and changes the shape of none of them.

#### 12.2 REST operations consumed

| Operation | Owner | Contract | Note |
|---|---|---|---|
| The notice read and the dispatch reference — the operation of RWB-P6-E1055-CON whose field names are Not specified in the source documents (GAP-1043; ASM-1991) | rwb-comms (P6) | RWB-P6-E1055-CON | Called once per notice, one hop, 2 s timeout, circuit breaker per downstream (DP-11); returns the notice type, the case ID, the generated PDF reference, the sent date, the barcode, the sent type, the callback date, the delivery status and the document reference |

That contract is the only C dependency of this story. The case read and the duplicate check of the store path are RWB-P5-E1024-APP's, and its rwb-case contract (RWB-P3-E1018-CON) remains that story's dependency and not this one's; the rwb-case answer in the Background is the fake of that store path. The interaction-ledger write is not consumed here: rwb-source-data writes it from the event (DP-18).

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.document.DocumentStored.v1` (event 16) | `rwb.document.events.v1` | P5 | caseId | documentId, caseId, documentType, source, storedAt |

CloudEvents 1.0 envelope in binary mode, JSON Schema registry with BACKWARD compatibility, retry topics and a dead-letter topic (Architecture v5 slides 11 and 42). The event row is written to the outbox in the same transaction as the document row and its field rows, so the event exists exactly when the document exists; the relay publishes it once per committed store. The payload carries no personal data, no field value and no file content: the case, the type and the source are the facts others react to, and a consumer that needs a facet of the notice asks rwb-comms for it. Its consumers are rwb-agent and rwb-case by the catalogue, and the letter ledger entry is written by rwb-source-data from it. The DOCATT decision record on `rwb.decision-record.v1` is published by the store path of RWB-P5-E1024-APP, not by this story: DP-03 is not a pattern of this slice.

#### 12.4 Events consumed

None. This slice consumes no Kafka event. The document states and facts that change are written through the store path and read through the contract; `DocumentFieldsExtracted` is published by the extraction path and consumed by rwb-case, and `NoticeDispatched` and `NoticeDelivered` are rwb-comms' events consumed by rwb-source-data, rwb-case, rwb-litigation, rwb-guarantee and rwb-reporting, not by this service (Architecture v5 slide 42).

#### 12.5 Workflows and activities

None. This story starts no workflow and contributes no activity. The `DocumentIntakeWorkflow` template — OCR, classify, extract — is registered and owned by RWB-P5-E1049-APP, and the `copyPending` activity that sets a stored document from COPY_PENDING to STORED is contributed by RWB-P5-E1024-APP; this slice calls the store path and waits for its answer in the caller's thread. DP-10 applies as a prohibition here: this service's dispatch-evidence module holds no Schedule and no event-started workflow.

#### 12.6 Schedules

None. The 15-minute document intake (JOB-12) belongs to RWB-P5-E1049-APP, the monthly retention run (JOB-17, monthly on the first Sunday) to RWB-P5-E1052-APP, and the daily WIN outbound file (JOB-10, 16:00) to rwb-comms with the integration adapters (Architecture v5 slide 44). This slice runs on the call of rwb-comms and on the receipt intake, never on a timer of its own.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `document` | P5 (`rwb_document`) | The evidence row: metadata, type, source, storage reference, retention class, write-once flag, version, hash |
| `document_field` | P5 (`rwb_document`) | The delivery facts of the receipt as index rows |
| `document_type` | P5 (`rwb_document`) | Read only: the type row in force with its flag, class and field list; the load is RWB-P5-E1025-APP's |
| `document_custody`, `retention_action`, `document_intake`, `document_text` | P5 (`rwb_document`) | Not written by this story: custody, the retention action and the intake path belong to their own stories |
| outbox, inbox and idempotency library tables | PLT library, created in `rwb_document` | The `DocumentStored` row and the `Idempotency-Key` of the store (DP-09) |

rwb-document reads no table of another service and holds no foreign key across services (DP-01): `recovery_case` is rwb-case's, the notice is rwb-comms' and the ledger is rwb-source-data's, and each reaches this story through its owner's contract or its owner's event. No `v_ace_*` view and no `public` table is read by this service.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-P6-E1055-CON fake | The rwb-comms contract of this legacy key (DP-11) | The notice answer for notice `N-0001` of case `RC-2026-000123` with notice type `DEMAND`, contract `CT-77001`, the generated PDF, sent date 26 November 2026, barcode `RR123456789TH`, sent type `NPL`, callback date 2026-11-28, delivery status `DELIVERED` and the document reference; a refused, a timed-out and a not-found variant for X4 and X8 |
| rwb-case contract fake (RWB-P3-E1018-CON) | The case read of the store path (RWB-P5-E1024-APP's dependency) | Case `RC-2026-000123` in the caller's scope, with a case-out-of-scope variant for MSG-P4-003 |
| reference-data fake (RWB-P3-E1043-CON, through the client library of RWB-PLT-E1043-CON) | DP-07 | LOV-DOC-SOURCE with `SCAN`, `UPLOAD`, `GENERATED`, `PARTNER`, `EMAIL`; LOV-RETENTION with `LEGAL10Y` and `GENERAL05Y`; LOV-SCAN-RESULT with `CLEAN` and `INFECTED` |
| storage product stub | The container write of the store path | `rwb-docs-legal` accepting the file at `rwb-docs-legal/{caseId}/{documentId}/v1`, and a container that refuses the write for the COPY_PENDING path |
| rwb-source-data ledger listener fake | DP-18 | The outbound `LETTER` entry it writes from `DocumentStored`, and the assertion that no entry is written by rwb-document |
| rwb-case timer fake | DP-10, read only | The `NOTICE_PERIOD` timer it starts from `NoticeDelivered`, and the assertion that no document event starts a timer |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 1 consumed | The store, the document read, the content read and the version add on `/api/recovery/document/v1`; the notice read and dispatch reference of RWB-P6-E1055-CON, one hop, 2 s timeout, breaker per downstream |
| Kafka | 1 published, 0 consumed | `rwb.document.DocumentStored.v1` on `rwb.document.events.v1`, keyed by caseId, written to the outbox in the store transaction |
| Temporal | None | No workflow, no activity and no Schedule in this slice (DP-10 as a prohibition) |
| File | 2 blobs per case | The notice PDF and the receipt in `rwb-docs-legal` at `rwb-docs-legal/{caseId}/{documentId}/v1` through the storage product the store path already depends on; this slice adds no new external dependency |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, module `dispatchevidence`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DispatchEvidenceService | Service | Reads the notice answer of RWB-P6-E1055-CON, stores the notice PDF with source `GENERATED` and the type of the notice, and returns the document ID as the document reference the dispatch file carries |
| ProofOfDeliveryDocumentService | Service | Stores the receipt file of a business date with source `PARTNER` and the type the table in force holds for a proof-of-delivery receipt, and hands the delivery facts to the field writer |
| DocumentFieldWriter | Service | Writes one `document_field` row per delivery fact in the same transaction as the receipt row, checks each fact against the field list of the type in force, and refuses a fact outside it |
| WriteOnceGuard | Service | Refuses a content replace and a delete inside the retention period with MSG-P5-002, leaves the row and the hash unchanged, and writes the audit event `DOCUMENT_CHANGE_REFUSED` with the document ID and the caller |
| DocumentEventPublisher | Service | Writes `rwb.document.DocumentStored.v1` to the outbox inside the store transaction through the DP-09 library, with the case key and no personal data |

**Database and migrations**

- Writes `document` and `document_field`, and the outbox row, in schema `rwb_document`; reads `document_type` in the same schema. No other schema is read (DP-01).
- No new table and no new column in this slice; the type rows are RWB-P5-E1025-APP's. The migration this slice relies on is the one RWB-P5-E1024-APP contributes to the per-service Flyway sequence — `V1024_1__document_store.sql`, which adds `document.previous_version_id`, `document.content_sha256`, `document_hub_parameter` and the unique partial index `uk_document_case_type_hash` on `(case_id, document_type, content_sha256)` where the row is active — and the type load of RWB-P5-E1025-APP. This slice adds no migration step of its own, so DP-15 is the ordering rule that keeps its two dependencies before the code (DP-15).
- The duplicate rule of AC6 rests on that unique partial index plus the pre-insert read; no separate key is introduced for the business date, because the receipt is a document like any other and its facts are fields.

**Configuration and reference data**

- `rwb.document.dispatch-evidence.notice-source` = `GENERATED` and `rwb.document.dispatch-evidence.receipt-source` = `PARTNER`, both values of LOV-DOC-SOURCE read through the reference-data contract and set as properties per environment.
- `rwb.document.dispatch-evidence.receipt-type` names the type code the type table in force holds for a proof-of-delivery receipt; its value is Not specified in the source documents (GAP-1044; ASM-1992), and the code is resolved against `document_type` at start-up, so an unknown code stops the module rather than storing a receipt of no type.
- `rwb.document.dispatch-evidence.notice-type-map` maps a notice type to a document type and holds `DEMAND` to `DEMAND_LETTER`; the mapping between a notice type and a document type is Not specified in the source documents beyond that pair (GAP-1044; ASM-1992).
- `rwb.document.dispatch-evidence.receipt-fields` lists the delivery facts written as document fields, by field name; the names are Not specified in the source documents (GAP-1045; ASM-1993).
- `rwb.document.dispatch-evidence.write-once-container` = `rwb-docs-legal` and `rwb.document.dispatch-evidence.path-template` = `{container}/{caseId}/{documentId}/v1`; the account and its immutability policy belong to the storage product the store path already depends on.
- The feature switch is `rwb.document.dispatch-evidence`: on in wave 1; off means the slice stores no dispatch evidence and rwb-comms receives the store path's refusal, never a silent success.

**Build steps**

1. `DispatchEvidenceService` over the RWB-P6-E1055-CON fake, with the notice answer, the type resolution and the document reference returned; test AC1 and the not-found and timeout paths of X8 and X4.
2. `ProofOfDeliveryDocumentService` over the receipt answer, with the type from the table in force and source `PARTNER`; test AC2 and the unknown-type path of X2.
3. `DocumentFieldWriter` with one row per delivery fact, the field list check of the type and the refusal of a fact outside it; test AC2 and X3.
4. `WriteOnceGuard` with the content replace and the delete on the store path and on the container, the unchanged hash and the `DOCUMENT_CHANGE_REFUSED` audit event; test AC3 against the write-once container of SIT.
5. `DocumentEventPublisher` inside the store transaction, with the forced-failure test that leaves no row, no field and no event, and the relay-recovery test of X6; test AC5.
6. The reads of AC4 with the permission decision of the guard, the scope check, the 2 s budget through the gateway-bff route and the content read compared against `content_sha256`; test AC4 and the refusals of X9.
7. The duplicate path of AC6 on the same receipt and business date, and the prohibition test of AC7: no ledger call and no timer registration in the module, with the two listener fakes asserting who writes what.
8. The boundary test over the module: no `v_ace_*` view, no `public` table and no foreign schema in any SQL or entity of `dispatchevidence`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 puts both documents in `rwb_document` and removes every cross-module read: the notice arrives through RWB-P6-E1055-CON, the case through the store path, and no `recovery` table name survives.

DP-05 applies as a prohibition: this service opens no `v_ace_*` view and no `public` table. The legacy `v_ace_pod` read belongs to the rwb-comms slice with the data product of RWB-P1-E1055-APP, and the delivery facts reach the receipt inside the contract answer (DF-ACE-253 to DF-ACE-258).

DP-07 keeps LOV-DOC-SOURCE, LOV-RETENTION and LOV-SCAN-RESULT in reference data through the contract and the client library, so `GENERATED`, `PARTNER`, `LEGAL10Y` and `GENERAL05Y` are values and never code.

DP-09 is the outbox: `DocumentStored` is written in the store transaction with the document row and its fields, keyed by caseId, and the relay publishes it once with no personal data; an inbox is wired by the template and nothing is consumed in this slice.

DP-10 applies as a prohibition: no Quartz job, no Schedule and no event-started workflow is created here. The intake and the retention Schedules stay with RWB-P5-E1049-APP and RWB-P5-E1052-APP, and the notice-period timer with rwb-case.

DP-11 is the one-hop contract to rwb-comms: REST, a mock and a 2 s timeout with a breaker per downstream, and no call chain from rwb-document onward while the caller waits.

DP-15 is the per-service Flyway sequence: this slice contributes no migration step, and it builds only after the store migration of RWB-P5-E1024-APP and the type load of RWB-P5-E1025-APP are in the sequence, in their own schema and never in the shared baseline.

DP-18 makes the interaction ledger rwb-source-data's: this slice publishes the event and writes no `LETTER` entry, and the ledger listener of rwb-source-data records the interaction from the event (REQ-ILG-004).

DP-19 is the gateway-bff composite route: the documents tab of SCR-30 reaches rwb-document in one hop, in parallel with the other tabs, and the answer is composed at the edge, so no service is asked to call another on behalf of a screen.

**Done when.** The tests in section 16 pass, a notice PDF and a WIN receipt are stored on case `RC-2026-000123` with the type, the write-once flag and the retention class of the type in force, a content replace and a delete inside the retention period are refused with MSG-P5-002 and the hash is unchanged, `rwb.document.DocumentStored.v1` is on `rwb.document.events.v1` once per store with no personal data, the document is read with its metadata, versions and fields within 2 s through the gateway-bff route, the same receipt stored twice leaves one document and counts the repeat, and the boundary test shows no cross-schema read, no ledger entry and no timer in this module.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-004 | The notice is acknowledged by WIN and the case record shows the dispatch | {notice} was sent for registered mail on {date}. |
| MSG-GEN-006 | The rwb-comms contract does not answer within 2 s, or the storage copy has not completed | {system} is not available. Your request is queued and will be retried. |
| MSG-P1-001 | The WIN batch is late or not COMPLETE for the business date of a receipt | {product} is from {date}. Today's load has not arrived. |
| MSG-P5-002 | A content replace or a delete of a write-once document inside its retention period | Legal documents cannot be changed. Add a new version instead. |
| MSG-P5-016 | The virus scan finds malware in the receipt or the notice file on intake | Not specified in the source documents (GAP-1046; ASM-1994) |
| MSG-P4-002 | The caller's role holds no Documents right for the action | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is absent or outside the caller's scope | This case is not in your scope. |
| MSG-P7-003 | The store path cannot write its decision record, so nothing is stored | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

MSG-P6-004 is raised by rwb-comms, not by this slice: the case record line is quoted here because the document reference this slice returns is what makes the line nameable, and the wording is the legacy wording unchanged. MSG-P5-016 is named by the FSD P5 upload exception flow with the ID and the meaning "malware found" only, so its text is Not specified in the source documents (GAP-1046; ASM-1994) and the story does not invent one. MSG-P7-003 belongs to the store path of RWB-P5-E1024-APP, which writes the DOCATT record; this slice inherits the refusal and writes no record of its own. For MSG-P4-002 in this story {action} names the action the caller tried — for example "attach the proof of delivery" — and never a case fact or a role name.

### 15. Screens and states

No screen is built in this story. The evidence is read on two screens that other stories own, both read only for this slice:

| Screen | What this slice makes visible |
|---|---|
| SCR-03 Case record | The notice and its proof of delivery as documents of the case, with the type, the stored date and the write-once label |
| SCR-30 Case documents | The two documents in the case document list with their type, source, stored date and version, the delivery facts of the receipt as document fields, and the download of the file through the content read |

| State | What the user sees |
|---|---|
| Loading | The tab skeleton while the document list or the document detail arrives through the gateway-bff composite route |
| List | The documents of the case with type, source, stored date, version and the write-once label; a COPY_PENDING document shows its state and its download disabled with MSG-GEN-006 |
| Error | The message of section 14 when a read is refused (MSG-P4-002, MSG-P4-003, MSG-GEN-006) with a retry action, and a document reference the service does not hold shown as unresolved to the owner |

The tab is reached only through the gateway-bff composite route (DP-19), which asks rwb-document once for the documents of the case and never asks this service to call another; the full tab, its search and its upload form are RWB-P5-E1026-APP's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-055-01 | AC1, BR1 (legacy) — AC1, AC5 and BR10 here | End to end | Notice "N-0001" of case "RC-2026-000123", generated PDF, type "DEMAND_LETTER", source "GENERATED", container "rwb-docs-legal"; one document row, one `DocumentStored`, and the document ID equal to the documentReference of the INT-14 file |
| TC-E1-055-02 | AC2, BR2 (legacy) — AC2 here; the notice state and the timer belong to RWB-P6-E1055-APP and RWB-P3-E1055-APP | End to end | The WIN receipt of business date 2026-11-30 with barcode "RR123456789TH", callback_date 2026-11-28, delivery_status "DELIVERED" and sent_type "NPL", source "PARTNER"; one document row and its `document_field` rows |
| TC-E1-055-03 | AC3 (legacy) — No criterion here; the ingestion of the WIN sample into `v_ace_pod` and `v_ace_batch_status` belongs to RWB-P1-E1055-APP | End to end | WIN owner sample "WIN-POD-SAMPLE-v1" of 25 records, ingested by ACE; the receipt documents of AC2 are stored from the records the contract answer names |
| TC-E1-055-04 | AC4, BR3 (legacy) — No criterion here; the dispatch retry and the task after the third failure belong to RWB-P6-E1055-APP | End to end | No acknowledgment on three runs of the WIN file of 2026-11-25 holding "N-0001" |
| TC-E1-055-05 | AC5, BR4 (legacy) — No criterion here; the ACE batch check belongs to RWB-P6-E1055-APP and the data product freshness to RWB-P1-E1055-APP | End to end | The ACE batch for source "WIN" of 2026-11-30 fails its record count check |
| TC-E1-055-06 | AC6, BR4 (legacy) — AC6 here for the count of receipt documents; the matching of a row to a notice by barcode and notice_ref belongs to RWB-P6-E1055-APP | End to end | 30 receipt rows for 2026-11-30 of which 1 names barcode "RR000000000TH" and notice_ref "WIN-99999"; 29 receipts match a case and one document row exists for each |
| TC-E1-055-07 | AC7 (legacy) — AC6 here for the repeat counted under R-UNI-40 | End to end | The receipt rows of 2026-11-30 read twice; one document row per receipt and the repeat counted |
| TC-E1-055-08 | AC8 (legacy) — No criterion here; the repeated JOB-10 run from the job monitor belongs to RWB-P6-E1055-APP | End to end | JOB-10 rerun on 2026-11-25 after it wrote "N-0001" |
| TC-E1-055-09 | AC9, BR5 (legacy) — No criterion here; the REC-05 barcode reconciliation belongs to RWB-P6-E1055-APP | End to end | "N-0002" in the file of 2026-11-25 with no barcode on 2026-11-28 |
| TC-E1-055-10 | AC10, BR6 (legacy) — AC3 and AC6 here: the stored row and its file hash are unchanged and the repeat is counted; the notice fields and the second NoticeDelivered belong to RWB-P6-E1055-APP | End to end | A second receipt row with barcode "RR123456789TH" and callback_date 2026-11-28 on 2026-12-07 |
| TC-E1-055-11 | AC11, BR7 (legacy) — No criterion here; the late WIN batch and the stale marker belong to RWB-P1-E1055-APP and RWB-P6-E1055-APP | End to end | No COMPLETE WIN batch for 2026-11-30 on 2026-12-01 |
| TC-E1-055-12 | Access (legacy) — No criterion here; RW-PHONECOL refused the notice dispatch detail belongs to RWB-P6-E1055-APP | Component | Role RW-PHONECOL reading the notice dispatch detail; refused with MSG-P4-002. The equivalent refusal of this slice is the Documents right of AC4, tested with a role that holds no Documents right |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end and Access to Component. Every legacy test case of RWB-E1-055 is listed above with the part of the behaviour this slice answers — the stored notice, the stored receipt and its facts, the write-once refusal, the repeat and the read for TC-E1-055-01, TC-E1-055-02, TC-E1-055-06, TC-E1-055-07 and TC-E1-055-10 — and no criterion for the dispatch, the acknowledgment, the batch, the reconciliation and the access cases, which belong to the rwb-comms slice. The `-ITG` copies of these cases are not here: they belong to RWB-ITG-E1055-ITG, which proves the same values across rwb-comms, rwb-document, rwb-source-data and rwb-case end to end.

### 17. Guardrails

- No business value in code: the document type, the write-once flag, the retention class, the source, the container, the path template and the delivery field names are rows of the type table, values of a reference list or properties read at start-up. The boundary test fails a build in which a type code, a retention class or a source value appears in Java.
- No personal data in events, workflow inputs, payloads, logs, tests or prompts. The event carries IDs and business facts only (`documentId`, `caseId`, `documentType`, `source`, `storedAt`); the addressee of a notice stays inside the PDF; the receipt carries a barcode, a delivery status and dates; no person name, no address, no identity number and no account number is written by this slice, and a field value is replaced by its field name in a log line.
- ACE data only through the owner's contract or the owner's `v_ace_*` views — and this story reads neither: DP-05 applies as a prohibition, the ACE proof of delivery reaches the receipt inside the rwb-comms answer, and no `v_ace_pod` row is opened by this service.
- No cross-schema read: `rwb_document` holds no foreign key into another schema and no copy of a case, a notice or a ledger entry (DP-01); the case, the notice and the ledger arrive through their owners' contracts or events.
- Write once: a legal document is stored in `rwb-docs-legal` with `write_once` true, is never overwritten, replaced or deleted inside its retention period, and every change is a new version at a new blob path with the earlier version still readable (NFR-029, FSD P5 AC-ALT-P5-001-01).
- Retention class from the type in force: the class and the flag come from `document_type` in the version in force, are carried on the row for the life of the document, and no end-of-retention action is taken by this slice (NFR-028, NFR-074, RWB-P5-E1052-APP).
- No ledger entry and no timer from this service: the interaction ledger is rwb-source-data's (DP-18) and the notice-period timer is rwb-case's (DP-10); the module registers no ledger call, no Schedule and no timer, and the test of AC7 fails if one appears.
- The document reference is data: it is the document ID returned by the store and read through the contract, never a value computed from a case number, a notice number, a barcode or a file name, so the dispatch file, the notice and the case screen name the same document or name none.
- One event per committed store, written in the store transaction: a failed transaction leaves no document row, no field row and no outbox row, and a repeated receipt leaves one row and a counted repeat (R-UNI-40).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-003 | Letters dispatched for print and post, proof of delivery returns to the case | Business Requirements Epic 2, section 4 | FEAT-DRI-17 | 13 Manage documents and correspondence | R-LIT-07, R-UNI-33, R-UNI-34, R-UNI-40 | TC-E1-055-01, TC-E1-055-02, TC-E1-055-06, TC-E1-055-07, TC-E1-055-10 |
| REQ-ILG-004 | What happens in an interaction is recorded against that interaction | Business Requirements Epic 1, sections 3.6 and 4 | FEAT-DRI-17 | 13 Manage documents and correspondence | R-UNI-40; DP-18 | TC-E1-055-01, TC-E1-055-02 |
| REQ-DRI-006 | No component calls a system of record directly: source data is read through the ACE views and leaves through the paths ACE already has | Business Requirements Epic 1, section 4 | FEAT-DRI-17 | 13 Manage documents and correspondence | D-RCV-35; ADR-010; DP-01, DP-05 | TC-E1-055-01, TC-E1-055-02 |

The supporting feature of the document evidence is FEAT-DCM-01 (the write-once container for legal types) with FEAT-DCM-17 (retention classes on stored documents), FEAT-DCM-19 (the hub as the system of record) and FEAT-DCM-20 (versions kept), which the FSD P5 module pairs with REQ-DCM-001, REQ-DCM-002, REQ-DCM-003 and REQ-DCM-010 in RWB-E1-024 and RWB-E1-041; this slice answers them only for the notice and the receipt of a notice dispatched to WIN, and changes neither the store design nor the retention design. The `-ITG` copies of the test cases are carried by RWB-ITG-E1055-ITG.

| Legacy reference | Where it is kept |
|---|---|
| The slice statement — the rwb-document part of RWB-E1-055, with the dispatch, the timer and the ACE proof of delivery held by other slices | Sections 1, 2, 19 |
| Legacy section 4 step 2, the document reference in the INT-14 file | Sections 1, 4, 8 (BR10), 12.1, 16 |
| Notice "N-0001", case "RC-2026-000123", contract "CT-77001", notice type "DEMAND", barcode "RR123456789TH", sent date 26 November 2026, sent type "NPL", callback date 2026-11-28, delivery status "DELIVERED", business date 2026-11-30 | Sections 3, 4, 7, 12, 16 |
| The WIN sample "WIN-POD-SAMPLE-v1" of 25 records | Sections 3, 16 (TC-E1-055-03, with RWB-P1-E1055-APP) |
| The six document types of version "DOCTYPE-2026.11" from 30 November 2026 and their retention classes, "LEGAL10Y" for "COURT_NOTICE" with `write_once` true and "GENERAL05Y" for "APPRAISAL_REPORT" with `write_once` false | Sections 1, 3, 4, 6, 7, 8, 11, 13 |
| Container "rwb-docs-legal" and the path "rwb-docs-legal/{caseId}/{documentId}/v1" | Sections 1, 3, 4, 7, 13, 17 |
| Legacy rules BR2, BR4, BR6 and rules CTL-15, R-LIT-07, R-UNI-40 | Sections 2, 7, 8, 9 |
| Messages MSG-P6-004, MSG-GEN-006, MSG-P1-001, MSG-P5-002, MSG-P5-016, MSG-P4-002, MSG-P4-003, MSG-P7-003 | Section 14, exception paths |
| Event 16 `DocumentStored`, topic `rwb.document.events.v1`, job map rows JOB-10, JOB-12 and JOB-17, and the schema `rwb_document` | Sections 1, 4, 12.3, 12.6, 12.7, 13 |
| Legacy key RWB-E1-055, story RWB-P5-E1055-APP, legacy test cases TC-E1-055-01 to TC-E1-055-12 | Metadata, sections 7, 16 |

### 19. Out of scope

- The whole dispatch and acknowledgment path: the notice state machine, the barcode, the INT-14 file, the acknowledgment, the retry after three failures, the REC-05 reconciliation and the NoticeDispatched and NoticeDelivered events — RWB-P6-E1055-CON and RWB-P6-E1055-APP.
- The `v_ace_pod` read, the ACE batch check and the data product freshness of the notice — RWB-P1-E1055-APP, with the data product of the notice.
- The notice-period timer and the case history item that shows the dispatch and the delivery — RWB-P3-E1055-APP.
- The WIN file interface, its SFTP and MFT path, the PGP handling and its infrastructure — RWB-P6-E1055-INF and RWB-P6-E1055-OPS.
- The document intake, the OCR, the classification and the field extraction of a scanned receipt, and the review queue of a low-confidence extraction — RWB-P5-E1049-APP and the extraction stories of P5.
- The monthly retention run, the retention action rows and the end-of-retention dispositions — RWB-P5-E1052-APP.
- The document type table load, its Legal and NPA sign-offs and its version — RWB-P5-E1025-APP.
- The store path itself, the upload form, the case document list, the search and the generation of a document from a template — RWB-P5-E1024-APP, RWB-P5-E1026-APP and the generation story of P5.
- Custody of originals and electronic discovery — the Epic 2 stories of P5.
- The end-to-end proof of these values across rwb-comms, rwb-document, rwb-source-data and rwb-case — RWB-ITG-E1055-ITG.
- The `rwb_document` schema baseline, the platform migration role, the topic and DLT provisioning, the container provisioning and its WORM policy, the observability and the runbook of this service.
