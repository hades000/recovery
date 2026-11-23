SCB Collections and Recovery. Henka Group, 22 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

Recovery Workbench

Document management design

| Item | Detail |
|---|---|
| Document | Recovery Workbench document management design |
| Version | 3 |
| Date | 22 November 2026 |
| Change | 3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Prepared by | Henka Group |
| Structure | arc42 building block and runtime views, C4 component view |
| Status | Draft. No approval is recorded for this version (ASM-B-TECH-13-11) |
| Source version | 1, as the source metadata table writes it, dated 28 October 2026; the file family of the folder is v2, so this is version 3 (CG-B-TECH-13-1; ASM-B-TECH-13-1; ASM-B-TECH-13-12) |
| Tool | T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60 |

# Change log

| Version | Date | Change |
|---|---|---|
| 3 | 22 November 2026 | D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash. The document hub is one service, rwb-document (P5), with schema rwb_document, login rwb_document, REST base /api/recovery/document/v1, topic rwb.document.events.v1 and task queue rwb-document; intake runs as DocumentIntakeWorkflow under JOB-12 and retention as a Temporal Schedule under JOB-17. Sections 1 to 8 carry the per-service reading; sections 9 and 10 are new; the change table is section 10 |
| 1 | 28 October 2026 | Document management design: the design on one page, intake and its seven sources, the first six document types, versions and legal documents, physical originals, search and access, retention and legal hold, and the three open decisions DL19, DL26 and DL27 (sections 1 to 8, copied unchanged) |

# 1. The design on one page

| Element | Design | Owner |
|---|---|---|
| System of record | The document hub in the recovery module is the system of record for recovery documents (DT06). In version 3 the hub is the service rwb-document (P5), reached at /api/recovery/document/v1, and no other service keeps a copy of a document or its index (ADR-013; DP-13) | P5 rwb-document |
| Storage | Blob storage; a write-once container for legal document types (DL27). Architecture v5 names the store as Azure Blob (WORM), holding the files as a claim-check: the case, the workflow and the events carry the file ID, never the bytes, with 2.8 TB by 2031 (Architecture v5 slide 16) | P5 rwb-document, on the Azure Blob platform |
| Index | document, document_field and document_custody tables in the ACE database. In version 3 they sit in schema rwb_document, together with document_intake, document_text, document_type, document_hub_parameter, document_checklist_item, case_document_check, signature_request, retention_rule and retention_action; no other service reads them (DP-01; ADR-014) | P5 rwb-document |
| Intake | Branch scanners, the mailroom, partner SFTP and uploads, recovery mailboxes, the field app and generated documents enter one intake. The intake is the DocumentIntakeWorkflow on task queue rwb-document, started every 15 minutes by JOB-12 with KEDA workers on the intake queue (Architecture v5 slides 16 and 44; DP-10; CG-B-TECH-13-6; ASM-B-TECH-13-6) | P5 rwb-document |
| Reading | OCR for Thai and English, classification by the intake agent, extraction of key fields with a confidence per field. The classify and extract runs are child workflows on task queue rwb-agent, requested by rwb-document (P10) and answered by AgentRunCompleted on rwb.agent.events.v1 (EV-28; Architecture v5 slide 16) | P5 rwb-document, with P10 rwb-agent |
| Review | Fields below the confidence floor go to the document review queue: GET /review-items and POST /documents/{documentId}/review of rwb-document, with MSG-P5-003 on the case | P5 rwb-document |
| Versions | Every change is a new version; legal documents cannot be overwritten. A new version is POST /documents/{documentId}/versions; every version keeps its own file ID and sha256 | P5 rwb-document |
| Originals | Physical originals tracked with holder, location and due-back date. The rows sit in document_custody and are written by POST /documents/{documentId}/custody | P5 rwb-document |
| Retention | A retention class per document type; a legal hold overrides it (DL26). Retention classes are retention_rule rows and each expiry is a retention_action row, both in rwb_document, run by the JOB-17 Temporal Schedule; the legal hold itself is recorded by rwb-case (P3) (CG-B-TECH-13-3; ASM-B-TECH-13-3) | P5 rwb-document, with P3 rwb-case |

# 2. Intake

| Source | How it arrives | Recorded as | Intake path |
|---|---|---|---|
| Branch scanner | Scanner folder picked up by the intake job | Scan, branch and scan time | DocumentIntakeWorkflow, JOB-12 pickup every 15 minutes |
| Mailroom | Scanner folder | Scan, mailroom | DocumentIntakeWorkflow, JOB-12 pickup every 15 minutes |
| Partner | Partner portal upload, or SFTP until external access (DL03) | Partner, firm ID | Upload link issued by rwb-document to the partner contract of rwb-partner (S9), then DocumentIntakeWorkflow (ADR-019) |
| Recovery mailbox | Attachment taken from the mailbox; the email is archived | Email, sender | DocumentIntakeWorkflow, mailbox connector; the email is stored as its own document (EV-16) |
| Field app | Photos and bills synced with location and time | Upload, field collector | DocumentIntakeWorkflow, sync from the field app |
| Generated | Notices and agreements produced from templates | Generated, template version | POST /cases/{caseId}/generated-documents and POST /documents/{documentId}/regenerate, inside rwb-document |
| Upload by staff | Case documents screen | Upload, user | POST /cases/{caseId}/documents through the gateway-bff composite route (DP-19) |

- Each file is scanned for malware before storage. A failed scan rejects the file and logs it. The scan is a step of DocumentIntakeWorkflow, before any byte reaches the container.

- The file is stored in Blob storage; legal types go to the write-once container. In version 3 the store is Azure Blob (WORM); rwb-document writes the file and keeps the file ID, and the case holds only that ID (Architecture v5 slide 16; CG-B-TECH-13-9; ASM-B-TECH-13-9).

- OCR produces text and layout. A page below the quality threshold is flagged for rescan.

- The intake agent classifies the type and matches the document to the case by case number, account or name. The agent run is a child workflow of rwb-agent (P10); the case match is read from the case contract of rwb-case (P3) over REST, one hop with a 2 s timeout (DP-11; CG-B-TECH-13-2; ASM-B-TECH-13-2).

- Key fields are extracted with a confidence per field. Fields below the floor go to the review queue (MSG-P5-003).

- The document appears on the case with its type, source, fields and review status. DocumentStored (EV-16) is published for rwb-agent and rwb-case, and DocumentFieldsExtracted (EV-17) for rwb-case, on topic rwb.document.events.v1.

# 3. The first six document types

| Type | Fields extracted | Retention class | Arrives as |
|---|---|---|---|
| Demand letter | Debtor name, account number, amount demanded, due date, sent date | Legal, write-once | Generated; scan of signed copy |
| Court notice | Court, case number, hearing date, parties | Legal, write-once | Law firm upload; scan |
| Appraisal report | Valuer, valuation date, market value, forced sale value, title number | Collateral | Valuer upload; SVAF |
| Title deed | Title number, land office, area in rai-ngan-wa, owner, encumbrances | Legal, write-once | Scan of the original |
| Settlement agreement | Parties, accounts, settlement amount, installments, signature date | Legal, write-once | Generated; e-signature or scan |
| Guarantor notice | Guarantor name, amount, sent date, delivery date | Legal, write-once | Generated; proof of delivery from WIN |

Further types are added as reference data with their fields and retention class, after Legal and the business sign the field list (DL19). In version 3 a type is a row of document_type and its checklist line a row of document_checklist_item, both in rwb_document (P5); the checklist of a case is case_document_check and is read by GET /cases/{caseId}/document-checklist of the same service, so no other service holds a copy of the type list (CG-B-TECH-13-5; ASM-B-TECH-13-5). The six types and their fields are copied unchanged (ASM-B-TECH-13-15).

# 4. Versions and legal documents

- A changed document is stored as a new version with a reason; earlier versions stay readable. The new version is POST /documents/{documentId}/versions; every version keeps its own file ID, its sha256 and its intake date.

- Legal types cannot be changed or deleted in their retention period (MSG-P5-002). rwb-document enforces the rule and the write-once container refuses an overwrite, including for the service's own login.

- A document produced for court carries its origin, intake date, version history and read history (NFR-076). The read history is the access log in rwb_access (P4), reached through the audit contract of rwb-access and one trace across the 19 services (ADR-023).

# 5. Physical originals

| Event | What is recorded |
|---|---|
| Original received | Holder Vault, location, received date |
| Sent out | Holder (branch, post, lawyer, court, land office), date out, due-back date |
| Returned | Date back, condition |
| Overdue | Task to document services; MSG-P5-004 on the case |

In version 3 the four rows are rows of document_custody in rwb_document and are written by POST /documents/{documentId}/custody. An overdue original raises its task through the task contract of rwb-case (P3), and MSG-P5-004 is carried on the case, so the officer sees the reminder in the case worklist and not in a second queue (CG-B-TECH-13-10; ASM-B-TECH-13-10).

# 6. Search and access

- Documents are found by case, type, date and extracted field. Masked fields are not searchable. In version 3 the index is rwb_document; the searches are GET /documents across cases and GET /cases/{caseId}/documents on one case, and the screens are SCR-30 Case documents, SCR-31 Document review queue and SCR-32 Document custody of the functional specification of the module (FSD P5 Document hub v3).

- Opening a document checks the Documents capability area and the case scope. The check is the authorise contract of rwb-access (P4) with the guard library, called by rwb-document before it acts, against cached permission data (DP-08; H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON; ADR-020).

- Every open and download is written to the access log. The log is in rwb_access (P4); GET /documents/{documentId}/content returns a short-lived SAS link and the read is written before the link is handed over.

- A masked field is masked by the masking_rule rows of rwb-access (P4) at the API of rwb-document, and it is never written to the search index; the national ID and the other personal fields are indexed only in their masked form (CG-B-TECH-13-7; ASM-B-TECH-13-7; DP-08).

# 7. Retention and legal hold

- Each type carries a retention class; the period is set by Compliance (DL26). The class and the period are retention_rule rows in rwb_document (P5).

- A legal hold on a case or document stops expiry for as long as it is in place. The hold is recorded by rwb-case (P3), which owns POST /cases/{caseId}/legal-hold; rwb-document checks the hold before it proposes an expiry and never disposes of a document under one (CG-B-TECH-13-3; ASM-B-TECH-13-3).

- At the end of retention the document is disposed of or extended by a recorded decision, never silently. Each proposal is a retention_action row in rwb_document, listed by the JOB-17 Temporal Schedule on the first Sunday of the month, and the recorded decision is kept with the document.

- e-Discovery returns every document for a named population with metadata and versions. The population is read through GET /documents with the case, type and date filters, and each document is returned with its metadata and its version list; no separate e-discovery operation exists (CG-B-TECH-13-4; ASM-B-TECH-13-4).

# 8. Open decisions

| Decision | What is needed | Answer used until decided |
|---|---|---|
| DL19 | Document types and fields | The six types above |
| DL26 | Retention per type | Proposed classes; hold overrides |
| DL27 | Storage, backup, legal hold and e-discovery | ACE storage pattern with a write-once container and the bank backup |
| DL44 | Adopt Architecture v5 as the target, with 19 services | Decided on 22 November 2026 under D-RCV-60 |
| DL45 | One service epic per service, plus the business epic as a tag | Decided on 22 November 2026 under D-RCV-60 |
| DL46 | Soft ownership by team type, with no named person | Decided on 22 November 2026 under D-RCV-60 |
| DL47 | Epic 1 preservation rule for work built or in build | Decided on 22 November 2026 under D-RCV-60 |
| DL48 | Dates unchanged and read as tentative | Decided on 22 November 2026 under D-RCV-60 |
| DL49 | Gap and assumption registers held with the run material | Decided on 22 November 2026 under D-RCV-60 |

DL44 to DL49 are the Decision Log rows allocated for the realignment on 22 November 2026 (Rules v1 R8.4; `ids.json`). They are recorded here so that the open-decision list of the source keeps its shape and a reader of this document sees which of its statements are settled and which are not (ASM-B-TECH-13-14). DL19, DL26 and DL27 stay open and are copied word for word.

# 9. The service view of the document hub

Section 9 is new. It states, in one place, what rwb-document is and what it answers on, so that a developer of another service can build against it without reading the four sources. Every row is taken from Architecture v5 slides 16, 41, 42 and 44 and from the Microservice Ownership Map v1; no owner, path, table or event is invented (ASM-B-TECH-13-13).

## 9.1 Service identity

| Item | Value |
|---|---|
| Service code and name | P5, rwb-document, Document hub |
| Wave | 1 (Epic 1 of the service) |
| Service epic | RWB-SVC-P5 |
| Schema and login | rwb_document, one login with grants on that schema only (ADR-014; DP-02) |
| REST base | /api/recovery/document/v1 (DP-13) |
| Kafka topic | rwb.document.events.v1, with rwb.document.events.v1.retry.1m, .retry.10m, .retry.1h and .dlt (DP-14) |
| Temporal task queue and namespace | rwb-document, namespace rwb-recovery (ADR-016) |
| Java package | th.co.scb.ace.workbench.recovery.document |
| Owns | Metadata, custody, OCR text and fields, signatures, retention (Architecture v5 slide 41) |
| Audit and decision record | One trace across the 19 services (ADR-023); every decision writes a local record and the central ledger of rwb-decision (ADR-022; DP-03) |

## 9.2 REST operations provided

| Operation | Contract path |
|---|---|
| GET /cases/{caseId}/document-checklist | /api/recovery/document/v1/cases/{caseId}/document-checklist |
| GET /cases/{caseId}/documents | /api/recovery/document/v1/cases/{caseId}/documents |
| GET /documents | /api/recovery/document/v1/documents |
| GET /documents/{documentId} | /api/recovery/document/v1/documents/{documentId} |
| GET /documents/{documentId}/content | /api/recovery/document/v1/documents/{documentId}/content |
| GET /intake-items/{intakeItemId} | /api/recovery/document/v1/intake-items/{intakeItemId} |
| GET /intake-items/{intakeItemId}/content | /api/recovery/document/v1/intake-items/{intakeItemId}/content |
| GET /review-items | /api/recovery/document/v1/review-items |
| PATCH /documents/{documentId}/fields/{fieldId} | /api/recovery/document/v1/documents/{documentId}/fields/{fieldId} |
| POST /cases/{caseId}/documents | /api/recovery/document/v1/cases/{caseId}/documents |
| POST /cases/{caseId}/field-captures | /api/recovery/document/v1/cases/{caseId}/field-captures |
| POST /cases/{caseId}/generated-documents | /api/recovery/document/v1/cases/{caseId}/generated-documents |
| POST /documents/{documentId}/custody | /api/recovery/document/v1/documents/{documentId}/custody |
| POST /documents/{documentId}/regenerate | /api/recovery/document/v1/documents/{documentId}/regenerate |
| POST /documents/{documentId}/review | /api/recovery/document/v1/documents/{documentId}/review |
| POST /documents/{documentId}/versions | /api/recovery/document/v1/documents/{documentId}/versions |
| POST /intake-items/{intakeItemId}/resolve | /api/recovery/document/v1/intake-items/{intakeItemId}/resolve |

The 17 operations are the rows of the Endpoints sheet of the Microservice Ownership Map v1 that carry owner P5. The contract is OpenAPI 3.1 on the base above and every consumer builds against the published contract and its fake (ADR-020; DP-11).

## 9.3 REST operations consumed

| Provider | Operation | Why rwb-document calls it | Class |
|---|---|---|---|
| P3 rwb-case | GET /cases/{caseId} | To match an intake item to its case and to read the case scope of the caller (CG-B-TECH-13-2; ASM-B-TECH-13-2) | C |

The case contract is consumed as a published contract with a fake; the call never blocks the build of rwb-document.

## 9.4 Events published and consumed

| Call type | Event | Topic | Other party | Class |
|---|---|---|---|---|
| Kafka, published | DocumentStored (EV-16) | rwb.document.events.v1 | P10 rwb-agent, P3 rwb-case | C |
| Kafka, published | DocumentFieldsExtracted (EV-17) | rwb.document.events.v1 | P3 rwb-case | C |
| Kafka, consumed | AgentRunCompleted (EV-28) | rwb.agent.events.v1 | P10 rwb-agent | C |

Events carry IDs and facts, never personal data; the file itself stays in Azure Blob and the event carries the file ID only (DP-09; Architecture v5 slide 42).

## 9.5 Workflows, activities and schedules

| Kind | Name | What it does | Trigger |
|---|---|---|---|
| Workflow | DocumentIntakeWorkflow | Malware scan, OCR, classify, extract, attach to the case | JOB-12, every 15 minutes, with KEDA workers (Architecture v5 slides 16 and 44) |
| Activity | generate | Produces a document from a template and records the template version | Called inside rwb-document by the generation operations |
| Activity | seal | Writes the file to the write-once container and keeps its sha256 | Called inside rwb-document after generation or intake |
| Child workflow | classify, extract on rwb-agent | Classification and field extraction with a confidence per field | Requested by DocumentIntakeWorkflow (P10, C dependency) |
| Schedule | Retention (JOB-17) | Proposes the expiries of the month as retention_action rows and waits for the recorded decision | Monthly, first Sunday, Temporal Schedule with overlap SKIP (ADR-016; DP-10) |

## 9.6 Tables owned

| Table | What it holds |
|---|---|
| document | The document header, its type, its case and its current version |
| document_field | The extracted fields with the confidence of each field |
| document_text | The OCR text and layout of each page |
| document_intake | One row per intake item, its source and its state |
| document_type | The type list, its field list and its retention class |
| document_checklist_item | The checklist line of a case type |
| case_document_check | The checklist of one case and what is present |
| document_custody | The physical original: holder, location, dates and condition |
| document_hub_parameter | The parameters of the hub, held as data |
| signature_request | The e-signature request, its parties and its result (CG-B-TECH-13-8; ASM-B-TECH-13-8) |
| retention_rule | The retention class and the period of each type (DL26) |
| retention_action | The disposal or the extension of one document, with its decision |

The 12 tables are the rows of the Tables sheet of the Ownership Map v1 that carry owner P5. rwb-document writes rwb_document only: no grant on another schema, no cross-schema join, view or foreign key (DP-01; ADR-014). The outbox, inbox and idempotency tables are the library tables created in every service schema (DP-09).

## 9.7 Call-type summary

| Call type | Provided | Consumed |
|---|---|---|
| REST | 17 operations on /api/recovery/document/v1 | 1 operation of rwb-case (section 9.3) |
| Kafka | 2 events on rwb.document.events.v1 (EV-16, EV-17) | 1 event on rwb.agent.events.v1 (EV-28) |
| Temporal | 1 workflow, 2 activities and 1 schedule on queue rwb-document; 1 activity contract for the callers of generation and e-signature | 1 child workflow on queue rwb-agent |
| File | 1 store: Azure Blob (WORM), files, 2.8 TB by 2031 | None |

# 10. Realignment changes in version 3 (D-RCV-60)

The table records what version 3 changes, where, why and under which decision. Every other statement, table, ID and number of the source is unchanged, including the six document types, the four custody events, the three message codes MSG-P5-002, MSG-P5-003 and MSG-P5-004, the requirement NFR-076 and the three open decisions DL19, DL26 and DL27.

| # | Section | Change from the source | Version 3 statement | Decision and pattern |
|---|---|---|---|---|
| 1 | 1, 9 | The hub is "the recovery module" with one schema and no service boundary | The hub is the service rwb-document (P5) with schema rwb_document, login, REST base /api/recovery/document/v1, topic and task queue of its own | ADR-013, ADR-014; DP-02, DP-13 |
| 2 | 1, 9 | The index is "document, document_field and document_custody tables in the ACE database" | The same three tables and nine more, all in rwb_document, owned by P5; no other service reads them | DP-01; ADR-014 |
| 3 | 1, 2 | "The intake job" picks up the scanner folder | DocumentIntakeWorkflow on queue rwb-document, started every 15 minutes by JOB-12 with KEDA workers | DP-10; ADR-016 |
| 4 | 1, 2 | "The intake agent" classifies and extracts, with no owner | Child workflows on queue rwb-agent (P10), requested by rwb-document, answered by AgentRunCompleted (EV-28) | DP-20 |
| 5 | 2 | The file is stored in "Blob storage" | Azure Blob (WORM), claim-check with the file ID, 2.8 TB by 2031 | Architecture v5 slide 16 |
| 6 | 2, 9 | The case match is named but no call is | The case contract of rwb-case (P3) over REST, one hop, 2 s timeout, with a fake | DP-11; CG-B-TECH-13-2 |
| 7 | 1, 6 | The capability area and the case scope are checked by the Workbench | The authorise contract of rwb-access (P4) with the guard library, called by rwb-document | DP-08; H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| 8 | 6 | "Every open and download is written to the access log" | The access log is in rwb_access (P4); the content operation hands over a short-lived SAS link and writes the read first | ADR-023 |
| 9 | 7 | Retention classes and the legal hold sit together in the hub | retention_rule and retention_action in rwb_document (P5); the hold is recorded by rwb-case (P3) | CG-B-TECH-13-3; ADR-014 |
| 10 | 7 | e-Discovery is named with no interface | GET /documents of rwb-document with the population filters, returning metadata and versions | CG-B-TECH-13-4 |
| 11 | 5, 9 | The four custody events are recorded with no interface | document_custody written by POST /documents/{documentId}/custody; the overdue task through the task contract of rwb-case | CG-B-TECH-13-10 |
| 12 | 8 | Three open decisions | DL19, DL26 and DL27 kept, and DL44 to DL49 added as decided on 22 November 2026 | Rules v1 R8.4; ids.json |

End of document. Version 3, 22 November 2026, D-RCV-60, T3 Code / OpenCode / DeepSeek v4.1 Flash.
