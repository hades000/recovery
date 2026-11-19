<!-- source: 05 Technical architecture/Recovery Workbench Document Management Design v2.docx -->
<!-- converted: 2026-11-04 from DOCX -->

> **Source:** `05 Technical architecture/Recovery Workbench Document Management Design v2.docx`  
> **Converted from:** DOCX

Recovery Workbench

Document management design

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench document management design |
| Version | 1 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Structure | arc42 building block and runtime views, C4 component view |

# 1. The design on one page

| Element | Design |
|---|---|
| System of record | The document hub in the recovery module is the system of record for recovery documents (DT06) |
| Storage | Blob storage; a write-once container for legal document types (DL27) |
| Index | document, document_field and document_custody tables in the ACE database |
| Intake | Branch scanners, the mailroom, partner SFTP and uploads, recovery mailboxes, the field app and generated documents enter one intake |
| Reading | OCR for Thai and English, classification by the intake agent, extraction of key fields with a confidence per field |
| Review | Fields below the confidence floor go to the document review queue |
| Versions | Every change is a new version; legal documents cannot be overwritten |
| Originals | Physical originals tracked with holder, location and due-back date |
| Retention | A retention class per document type; a legal hold overrides it (DL26) |

# 2. Intake

| Source | How it arrives | Recorded as |
|---|---|---|
| Branch scanner | Scanner folder picked up by the intake job | Scan, branch and scan time |
| Mailroom | Scanner folder | Scan, mailroom |
| Partner | Partner portal upload, or SFTP until external access (DL03) | Partner, firm ID |
| Recovery mailbox | Attachment taken from the mailbox; the email is archived | Email, sender |
| Field app | Photos and bills synced with location and time | Upload, field collector |
| Generated | Notices and agreements produced from templates | Generated, template version |
| Upload by staff | Case documents screen | Upload, user |

- Each file is scanned for malware before storage. A failed scan rejects the file and logs it.

- The file is stored in Blob storage; legal types go to the write-once container.

- OCR produces text and layout. A page below the quality threshold is flagged for rescan.

- The intake agent classifies the type and matches the document to the case by case number, account or name.

- Key fields are extracted with a confidence per field. Fields below the floor go to the review queue (MSG-P5-003).

- The document appears on the case with its type, source, fields and review status.

# 3. The first six document types

| Type | Fields extracted | Retention class | Arrives as |
|---|---|---|---|
| Demand letter | Debtor name, account number, amount demanded, due date, sent date | Legal, write-once | Generated; scan of signed copy |
| Court notice | Court, case number, hearing date, parties | Legal, write-once | Law firm upload; scan |
| Appraisal report | Valuer, valuation date, market value, forced sale value, title number | Collateral | Valuer upload; SVAF |
| Title deed | Title number, land office, area in rai-ngan-wa, owner, encumbrances | Legal, write-once | Scan of the original |
| Settlement agreement | Parties, accounts, settlement amount, installments, signature date | Legal, write-once | Generated; e-signature or scan |
| Guarantor notice | Guarantor name, amount, sent date, delivery date | Legal, write-once | Generated; proof of delivery from WIN |

Further types are added as reference data with their fields and retention class, after Legal and the business sign the field list (DL19).

# 4. Versions and legal documents

- A changed document is stored as a new version with a reason; earlier versions stay readable.

- Legal types cannot be changed or deleted in their retention period (MSG-P5-002).

- A document produced for court carries its origin, intake date, version history and read history (NFR-076).

# 5. Physical originals

| Event | What is recorded |
|---|---|
| Original received | Holder Vault, location, received date |
| Sent out | Holder (branch, post, lawyer, court, land office), date out, due-back date |
| Returned | Date back, condition |
| Overdue | Task to document services; MSG-P5-004 on the case |

# 6. Search and access

- Documents are found by case, type, date and extracted field. Masked fields are not searchable.

- Opening a document checks the Documents capability area and the case scope.

- Every open and download is written to the access log.

# 7. Retention and legal hold

- Each type carries a retention class; the period is set by Compliance (DL26).

- A legal hold on a case or document stops expiry for as long as it is in place.

- At the end of retention the document is disposed of or extended by a recorded decision, never silently.

- e-Discovery returns every document for a named population with metadata and versions.

# 8. Open decisions

| Decision | What is needed | Answer used until decided |
|---|---|---|
| DL19 | Document types and fields | The six types above |
| DL26 | Retention per type | Proposed classes; hold overrides |
| DL27 | Storage, backup, legal hold and e-discovery | ACE storage pattern with a write-once container and the bank backup |
