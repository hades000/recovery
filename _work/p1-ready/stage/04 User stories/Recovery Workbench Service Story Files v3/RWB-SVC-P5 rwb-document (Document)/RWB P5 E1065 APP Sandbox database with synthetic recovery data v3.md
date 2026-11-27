# RWB-P5-E1065-APP Sandbox database with synthetic recovery data

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1065-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-065 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP07, DP13, DP15, DP19 |
| Readiness decisions | RD-P1-004, RD-P1-046 |
| Parallel lane | L-P5-T |
| Ready to start | Day 1 |
| Size | Not sized; the squad sizes it at refinement |
| Depends on (build) | None |
| Contract dependencies | RWB-P1-E1065-CON |
| Contract version | The versioned fixture files of the RWB-P1-E1065-CON contract package: `case-seed-list.csv`, `seed-profile.json`, `shape-table.csv`; the package version number is Pending until the contract is published (service contract owner) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (no FR mapped to REQ-RDF-001, REQ-RDF-010) |
| Status | Draft (directive resolutions) |

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- One shared `rwb_sandbox` per environment: this slice applies the rwb-document sequence to `rwb_document` only; the database is never renamed or recreated and a failed seed rolls back (RD-P1-046; finding #1).
- The input is the versioned fixture files of RWB-P1-E1065-CON, not an operation, a mock build result or a P1 case list; the unused ACE account fake is removed (RD-P1-046; findings #2, #4, #5, #6).
- Open: the fixtures hold no case ID or case number, so the case reference of a seeded document is Pending (finding #3, GAP-3369).
- The 401, 403 and 404 answers name their message codes (finding #7); the TC-P5-E1065 rows are marked for Test Cases v9 (finding #8); AC11 added for the rollback.
- Test case citations aligned to Test Cases v9: identifiers of this story replace the placeholders and the shared legacy identifiers that now hold another story's case (W2-tests mapping).

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-065 for rwb-document, carrying the DEV sandbox document estate. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P5-E1065-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 32 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **tribe lead and squad member (RW-TRIBE)** I want **the DEV sandbox to stand up `rwb_document` from the same per-service migration as SIT, with the six document types at the version in force, one synthetic document per agreed type on every synthetic case with its extracted fields and no clear personal value**, so that **every squad can build and test the document screens, the OCR and extraction paths and the retention checks from the first day, before any ACE interface is available and with no production data**.

This story is the rwb-document part of legacy RWB-E1-065: the document estate of the DEV sandbox. The DEV database `rwb_sandbox`, the ACE-shaped test double, the 92 recovery tables, the 30 `v_ace_*` views, the dictionary-driven generator, the case volumes, the exception shapes, the verifier of the P1 schemas, the pipeline stage and the read-only grant on schema `recovery` belong to RWB-P1-E1065-CON, RWB-P1-E1065-APP and RWB-P1-E1065-DB. What this slice owns is what answers for `rwb_document`: the six document types at version "DOCTYPE-2026.11" with their fields and retention classes, one synthetic document per agreed type on every synthetic case with its extracted fields, the held intake items and their OCR text, the checklist and completeness rows, the custody and retention rows the sandbox needs to be demonstrable, the personal-data gate on `document_field.extracted_value` (legacy AC7 names exactly that column), and the DEV read-only role's read of the schema.

rwb-document owns metadata, custody, OCR text and fields, signatures and retention (Architecture v5 slide 41), and every document file is in Blob with WORM (slides 8 and 16). Every service runs from the service template, reads and writes only its own schema and holds its outbox and inbox there (slide 20), so the document estate is only usable for the squads if it exists in `rwb_document` and in the DEV container, not in a shared fixture. The type table version this slice seeds is the one in force from 30 November 2026: FSD P5 AC-ALT-P5-003-01 gives version "DOCTYPE-2026.11" with the six types, COURT_NOTICE with retention class "LEGAL10Y" and write_once true, and APPRAISAL_REPORT with "GENERAL05Y", write_once false and 4 fields. The checklist the sandbox carries is checklist version "CHK-2026.11" (FSD P5 A2.16) and the retention action the sandbox carries names retention version "RET-2026.11" (FSD P5 A2.17).

### 2. Business rationale

SIT reads the real ACE database and the real document store; DEV has neither. Without a seeded document estate, no squad can test the case documents screen, the OCR and extraction review queue or a retention or custody check before a real scan arrives: the tables are empty, the review list is empty and every document story would ask another team for a fixture. The legacy story builds a sandbox database in DEV from the same DDL as SIT, fills it with synthetic rows, and its AC1 fixes the document part of the outcome — the case "RW-2026-000001" has its accounts, parties, interactions and documents linked — while legacy BR3 requires the values to come from the data dictionary and the lists and legacy AC7 names `recovery.document_field.extracted_value` as the one column the personal-data gate scans.

This story is the rwb-document part of legacy RWB-E1-065; the primary slice is the rwb-source-data contract of the same key. The DEV database `rwb_sandbox`, the ACE-shaped test double, the 92 recovery tables, the 30 `v_ace_*` views, the dictionary-driven value factory, the case volumes, the exception shapes, the verifier of the P1 schemas, the pipeline stage and the read-only grant on schema `recovery` are not here. What is here is the estate that answers for this service: the six types at the version in force, one document per agreed type on every synthetic case with its fields, confidence and extracted value, the held intake items and their page text, the checklist items and the completeness row, one custody movement and one retention action, and the DEV read-only role's read of the tables the screens read.

The seed is the difference between a DEV environment where a document screen shows an empty list and one where it shows six types, their confidence and their retention class. It keeps BR1 (no production data in DEV) and BR9 (a clear identity number only in the ACE-shaped tables) because the seed writes synthetic type codes, synthetic file references, synthetic field values and a masked or synthetic national ID only, and it serves REQ-RDF-001 (one owner per data product, reachable in DEV without a request to another team) and REQ-RDF-010 (access per data product by role, with personal data masked). The type codes, the fields, the write-once flags, the retention classes and the checklist rows are data with a version, not code, so the same estate follows a new type table version without a release (FSD P5 A2.3, BR-P5-003; DP-07).

### 3. Preconditions

- The `rwb_document` baseline is in place: `document`, `document_field`, `document_custody`, `document_type`, `document_checklist_item`, `case_document_check`, `document_hub_parameter`, `document_intake`, `document_text` and `retention_action` exist with the standard record columns of TSD P5 T3.0 (`is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by`), at the platform migration version of DP-15.
- RWB-P1-E1065-CON is published with its versioned fixture files, not as an operation (RD-P1-046): `seed-profile.json` (seed `20261128`, total 2,812 cases), `case-seed-list.csv` (one row per seeded case: shape_id, product group, account_key, person_key, case entry date and total outstanding; no case ID and no case number), `shape-table.csv` (shape_id, row type, count, product group, is_case), the four stage fixtures full, empty, refused and timeout, and `tier2-ddl.sql`. This story builds against those files (DP-11, C dependency); the package version number is Pending (DOR-RWB-P5-E1065-APP-23).
- The DEV sandbox is one shared database `rwb_sandbox` (RD-P1-046): RWB-P1-E1065 creates it if it is absent, builds only `public`, `recovery` and `rwb_source_data`, and never drops it; this slice then applies the rwb-document Flyway sequence to `rwb_document` with the rwb-document login, in the service wave order of Architecture v5 slide 41, and no slice renames or recreates the database.
- Pending: how rwb-document obtains the case ID and case number of each row of `case-seed-list.csv`. rwb-case assigns every case number and P1 publishes none (RD-P1-046), and this service reads no schema of another service (DP-01); owner data architect with the rwb-case service owner, tracked as GAP-3369. Case "RW-2026-000001" in this story names the seeded case of that number once the rule exists.
- The type table version in force from 30 November 2026 is "DOCTYPE-2026.11" (FSD P5 AC-ALT-P5-003-01), loaded and approved by RWB-P5-E1025-APP in a running environment; in the sandbox the same version is written by the migration of this story, so no screen and no approval step is needed to build it.
- LOV-RETENTION holds the codes "LEGAL10Y" and "GENERAL05Y", assumed until the bank retention schedule arrives (DL26), and LOV-STAGE, LOV-DOC-SOURCE, LOV-REVIEW, LOV-CUSTODY, LOV-OCR-STATUS, LOV-INTAKE-REVIEW, LOV-INTAKE-MATCH, LOV-SCAN-RESULT and LOV-EXTRACT-STATUS hold the values of TSD P5 T3.2. They are read through the reference-data contract of rwb-case (DP-07, C RWB-P3-E1043-CON) and never copied into `rwb_document`.
- The DEV storage account and the DEV Blob containers of the sandbox exist and accept writes from the build. Their names and the location of the container holding the write-once legal types are Not specified in the source documents (GAP-1053; ASM-2001); the running containers named in FSD P5 A2.1 are "rwb-docs" and "rwb-docs-legal".
- The number of documents a synthetic case holds beyond the one per agreed type, and the number of versions a seeded document carries, are Not specified in the source documents (GAP-1051; ASM-1999); this story fixes one document per agreed type at doc_version 1 on every synthetic case and treats any further document as a parameter; the per-case document count and the version depth are seed parameters of this story and of RWB-P5-E1025-APP; the fixture files of RWB-P1-E1065-CON do not carry them (RD-P1-046; GAP-1051).
- The file name pattern of the synthetic PDFs the estate seeder writes to Blob is Not specified in the source documents (GAP-1052; ASM-2000).
- The count of held intake items per exception shape, and the pages each held item carries, are Not specified in the source documents (GAP-1054; ASM-2002); FSD P5 AC-P5-007-01 fixes only the 180-document OCR sample, 30 of each type, which is the sample of the OCR story and not the case estate. The held item count per exception shape and the page count per held item are seed parameters of this story; the fixture files of RWB-P1-E1065-CON do not carry them (RD-P1-046); the review reasons the DEV queue must show are named in the test data section of RWB-P5-E1049-APP.
- The login is the rwb-document login (DP-02), and the DEV-only read-only role keeps the legacy name `rwb_sandbox_read` and is granted SELECT only, on the seed tables of schema `rwb_document`, with no grant on the legacy single schema `recovery`; the DEV sandbox database is the shared `rwb_sandbox`, and each service slice seeds only its own schema (RD-P1-046; GAP-0501); the login name for the target schema is set at the platform schema story RWB-PLT-NF06-DB.
- The seed reads no `v_ace_*` view, no `public` table and no table of another service (DP-05 applies here as a prohibition), and it evaluates no rule (DP-04 as a prohibition): the personal-data pattern test of legacy AC7 is a value test on a seeded column, not a Drools decision.
- Each service seeds its own schema from its own baseline with seed `20261128`; the case rows are seeded once, in `rwb_case`, by RWB-P3-E1065-APP, and the document rows refer to them by plain key (source of that key: GAP-3369), with no cross-schema key and no seed of another service's schema.
- The document store, the upload, the OCR, the classification, the extraction, the review queue and the retention job JOB-17 (owned by RWB-P5-E1017-APP; GAP-2351; this story claims no Schedule) are other stories of this service (RWB-P5-E1024-APP, RWB-P5-E1049-APP, RWB-P5-E1052-APP and their siblings); this story seeds the rows they read and changes none of them.

### 4. Flow

1. The sandbox build of RWB-P1-E1065 creates `rwb_sandbox` if it is absent and builds `public`, `recovery` and `rwb_source_data`. This slice then applies the rwb-document Flyway sequence to schema `rwb_document` and reaches the seed step with the `rwb_document` baseline in place and the document tables empty (RD-P1-046).
2. The rwb-document migration `V1065_1__document_estate_seed.sql` applies the type table in one transaction: 6 `document_type` rows at table version "DOCTYPE-2026.11" with valid_from 30 November 2026, each with its label, its write-once flag, its retention class, its field definitions and its classification threshold.
3. DocumentTypeSeeder checks the written rows against the lists read through the reference-data contract: every retention class is in LOV-RETENTION, every field definition names a field of the type, and exactly one table version is in force.
4. DocumentEstateSeeder reads `case-seed-list.csv`, resolves the case ID of each row (Pending, GAP-3369) and writes one `document` row per agreed type on every synthetic case with case_id, document_type, source, doc_version 1, review_status, retention_class and write_once taken from its type row, content_sha256 over the synthetic file, and a storage_ref pointing at the file it writes to the DEV Blob container.
5. The seed writes the same file content for the same case, seed value and type, so the content_sha256 of a seeded document is stable across rebuilds. The file content is derived from the seed value, the case ID and the type; the file name pattern of the synthetic files is Not specified in the source documents (GAP-1052).
6. DocumentFieldSeeder writes one `document_field` row per field definition of the stored document with field_name, extracted_value, confidence and extractor_version; the value comes from the deterministic value factory with the seed, and the seeder masks an identity number and then runs the national ID check before it commits.
7. HeldIntakeSeeder writes at least one `document_intake` row per held shape with source, file_name, received_at, file_sha256, scan_result, ocr_status, ocr_attempts, page_count, predicted_type, classification_confidence, match_status, extract_status and review_reason, and one `document_text` row per page with page_no, text_content and quality.
8. ChecklistSeeder writes the `document_checklist_item` rows of checklist version "CHK-2026.11" for the stages and their required types with required and sort_order, then one `case_document_check` row for case "RW-2026-000001" with checklist_version, required_count, present_count, missing_types, complete and checked_at.
9. DocumentEstateSeeder writes one `document_custody` movement for an original document (from_location and to_location from LOV-CUSTODY, the holder and the due back date) and one `retention_action` row for the appraisal report stored on 1 November 2021 (run_month "2026-12", action "ARCHIVED", the decision record of FSD P5 AC-ALT-P5-017-02).
10. The retention action carries one local decision record written through the decision-record library, first in the transaction, with the decision code "DOCRET", the document, the class "GENERAL05Y", the retention version "RET-2026.11" and the expiry date 1 November 2026; the entry stays in `rwb_document`.
11. DocumentSeedVerifier reads the whole estate back: the six types at one table version, one document per agreed type per case of the fixture, one field row per field definition with a confidence, no extracted value matching the national ID pattern, the held items with their pages, the custody and retention rows, every storage_ref present in the container, and the row count per table; a failure fails the build, the seed migration rolls back and `rwb_document` keeps its previous rows.
12. This slice grants the DEV-only read-only role `rwb_sandbox_read` SELECT on the schema and publishes the build result with the row count per table; the DEV service serves the seeded estate through the P5 reads of section 12.1.
13. The DEV sandbox has no Kafka, so no relay runs and no event leaves it; the document rows and the seeded retention action stay in `rwb_document`, and a squad that needs a document event uses the SIT environment built by RWB-ITG-E1065-ITG.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A seeded type row has no `valid_from`, no `table_version`, or a retention class that is not in LOV-RETENTION | The sandbox build fails naming the row and the value; the seed rolls back and `rwb_document` keeps its previous rows | None (pipeline result) | AC1 |
| X2 | The same seed value and the same case list run twice on a rebuilt database | The same types, the same document rows per type and the same content_sha256 are written, with no row of the previous build left | None | AC5 |
| X3 | A seeded document row names a storage_ref that does not exist in the DEV container | The build fails naming the table, the row and the storage_ref; the document is not published | None (pipeline result) | AC2 |
| X4 | A seeded extracted value matches the 13-digit national ID pattern with a valid check digit | The build fails naming `document_field.extracted_value` and the document; no sandbox is published from that build | None (pipeline result) | AC3 |
| X5 | A held intake item has no review_reason, or no page text | The build fails naming the intake item and the review_reason column; the held shape is not published | None (pipeline result) | AC4 |
| X6 | A reader holding `rwb_sandbox_read` tries to change a seeded row | The write is refused by the database; the row is unchanged | None (database error) | AC6 |
| X7 | The seed writes a row into `public`, into a `v_ace_*` view or into another service's schema | The build fails naming the object; the seed writes only schema `rwb_document` | None (pipeline result) | AC7 |
| X8 | A case ID used by the seed matches no row of `case-seed-list.csv` (matching rule Pending, GAP-3369) | The build fails naming the case and the table; no document is written for a case the sandbox does not hold | None (pipeline result) | AC2, AC7 |
| X9 | A write-once document is changed through the DEV service or directly in the container | The change is refused; the file hash and the document row are unchanged | MSG-P5-002 | AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the `rwb_document` baseline and the published RWB-P1-E1065-CON fixture files. It reads no ACE view, calls no other service at run time and adds no dependency of its own |
| Negotiable | The number of documents per case beyond one per type, the synthetic file pattern, the container names and the held item count are parameters and rows; the story fixes the migration, the seeders, the verifier and the gate, and writes no type code, class or list value in code |
| Valuable | Every squad can open a seeded case, see its documents with their fields and confidence, open a held item and read a retention action in DEV from Day 1, with no production data |
| Estimable | One migration, one repeatable companion, six seeders, one verifier and one grant script |
| Small | Fits one sprint with its tests, as a secondary slice of the legacy key |
| Testable | Every criterion in section 7 is one automated test over the seeded schema, with the lists stubbed and `case-seed-list.csv` as the input; the criteria that name a case wait for GAP-3369 |

### 7. Acceptance criteria

```gherkin
Feature: Sandbox database with synthetic recovery data — the rwb-document estate

  Background:
    Given the sandbox build uses seed 20261128
    Given the shared database "rwb_sandbox" holds "public", "recovery" and "rwb_source_data" built by RWB-P1-E1065, and the rwb-document Flyway sequence is applied to schema "rwb_document" with the rwb-document login
    Given the RWB-P1-E1065-CON fixture files "seed-profile.json" (seed 20261128, total 2,812), "case-seed-list.csv" (one row per seeded case, no case ID and no case number) and "shape-table.csv" (count and is_case per shape, shaped cases inside the 2,812)
    Given the case reference of each row of "case-seed-list.csv" is available to the seeder (Pending: its source, GAP-3369)
    Given the held intake rows are seed data of this slice, at least one per held shape

  Scenario: AC1 The six document types load at version "DOCTYPE-2026.11" (new, D-RCV-60)
    Given the type table version in force from 30 November 2026 is "DOCTYPE-2026.11"
    When the rwb-document migration runs in schema "rwb_document" after the baseline
    Then 6 rows are in "document_type" with the codes DEMAND_LETTER, COURT_NOTICE, APPRAISAL_REPORT, TITLE_DEED, SETTLEMENT_AGREEMENT and GUARANTOR_NOTICE
    And COURT_NOTICE holds retention class "LEGAL10Y", write_once true and the field definitions court_name, black_case_no, notice_date and hearing_date
    And APPRAISAL_REPORT holds retention class "GENERAL05Y", write_once false and 4 field definitions
    And every row carries table_version "DOCTYPE-2026.11" and valid_from 30 November 2026
    And no row of another table version is in the schema

  Scenario: AC2 Every synthetic case holds its documents (new, D-RCV-60)
    Given a row of "case-seed-list.csv" resolves to case "RW-2026-000001" (Pending, GAP-3369)
    Given the DEV Blob container of the sandbox accepts the synthetic files
    When the estate seeder writes the documents of the cases of the fixture
    Then case "RW-2026-000001" holds one document per agreed type linked with its case_id, its document_type, its source, doc_version 1 and its content_sha256
    And each of its documents carries the write_once flag and the retention class of its type in "document_type"
    And every document row points at a file that exists in the DEV Blob container
    And no document row names a case that matches no row of "case-seed-list.csv"

  Scenario: AC3 Every field carries a synthetic value and no clear national ID (new, D-RCV-60)
    Given the type table "DOCTYPE-2026.11" holds the field definitions of each type
    When the field seeder writes "document_field" for the stored documents
    Then each stored document of a type with field definitions holds one row per field with its field_name, its extracted_value and a confidence
    And every extracted value is present and its confidence is a number between 0 and 1
    And no extracted value matches the 13-digit national ID pattern with a valid check digit, so the sandbox passes the personal-data gate that legacy AC7 names on "document_field.extracted_value"
    And a clear identity number in the ACE-shaped tables is not a failure of this slice, because those tables are the ACE test double and belong to RWB-P1-E1065-CON

  Scenario: AC4 The rows the document screens need are present (new, D-RCV-60)
    Given the held intake seed rows of this slice, at least one per held shape
    When the held intake, checklist and custody seeders run
    Then at least one "document_intake" item is held with a review_reason from LOV-INTAKE-REVIEW, its page_count and its ocr_status
    And that item holds its "document_text" pages with page_no, text_content and quality
    And one "document_custody" movement names its document, its from_location and to_location from LOV-CUSTODY, the holder and the due back date
    And "document_checklist_item" holds the required types of the stages at checklist version "CHK-2026.11" with required and sort_order
    And "case_document_check" holds one row for case "RW-2026-000001" with required_count, present_count, missing_types, complete and checked_at

  Scenario: AC5 The rebuild is idempotent (new, D-RCV-60)
    Given schema "rwb_document" holds the estate for commit "a1b2c3d" and seed 20261128
    When the same migration and the same seed value run again in a rebuilt database
    Then the document row count per document type is the same
    And the content_sha256 of every document of case "RW-2026-000001" is the same
    And no row of the previous build remains in "document", "document_field", "document_intake", "document_text", "document_custody", "document_checklist_item", "case_document_check" or "retention_action"

  Scenario: AC6 The DEV read-only role reads the estate and cannot change it (new, D-RCV-60)
    Given the DEV-only read-only role "rwb_sandbox_read" over the sandbox
    When a member of that role runs "SELECT doc_type_code, retention_class FROM rwb_document.document_type" and then an UPDATE on a row of "document"
    Then the read returns the rows of the six types
    And the same role reads "document" and "document_field"
    And the UPDATE is refused by the database and the row is unchanged

  Scenario: AC7 The seed writes only schema "rwb_document" (new, D-RCV-60)
    Given the shared database "rwb_sandbox" holds the schemas "public", "recovery", "rwb_source_data" and "rwb_document"
    When the rwb-document migration and the estate seeders run
    Then every write lands in schema "rwb_document"
    And no "public" table, no "v_ace_*" view row, no case row, no role row and no reference row of another service is written
    And every case ID the seed uses belongs to a row of "case-seed-list.csv" (source of the ID Pending, GAP-3369)
    And the database "rwb_sandbox" is neither renamed nor recreated
    And no foreign key of "rwb_document" points at another schema

  Scenario: AC8 No event leaves the sandbox (new, D-RCV-60)
    Given the DEV profile runs with no Kafka broker and no outbox relay
    When the estate is seeded and the one retention action is written
    Then no DocumentStored and no DocumentFieldsExtracted event is produced and no consumer group is created
    And the only record written for the seeded retention action is the local decision record of the decision-record library, which stays in "rwb_document"
    And the document rows carry no event and the seed writes no "outbox_event" row

  Scenario: AC9 Every seeded document carries the write-once flag and the retention class of its type (new, D-RCV-60)
    Given the type table version in force from 30 November 2026 is "DOCTYPE-2026.11"
    When the estate seeder writes the documents of every case of the fixture
    Then every document row carries the write_once value and the retention_class value of its "document_type" row
    And a document of type COURT_NOTICE carries retention class "LEGAL10Y" and write_once true
    And a document of type APPRAISAL_REPORT carries retention class "GENERAL05Y" and write_once false

  Scenario: AC10 The provided operations answer 401, 403 and 404 on their errors (new, D-RCV-60)
    Given the P5 operations on "/api/recovery/document/v1" are provided by the DEV service
    When a caller without a valid identity, a caller without the role of the operation and a caller who names a document identifier not in "document" each call an operation
    Then the answers are 401 with messageCode MSG-P4-001, 403 with MSG-P4-002 and 404 with MSG-P4-003, in that order, each as application/problem+json with the shared Problem schema
    And no document row is changed by any refused call

  Scenario: AC11 A failed seed leaves the previous rows and the shared database (new, RD-P1-046)
    Given "rwb_document" holds the estate of an earlier build
    And the seed holds a type row whose retention class is not in LOV-RETENTION
    When the seed migration runs
    Then the build fails naming "rwb_document.document_type", the row and the value, and the seed migration rolls back
    And "rwb_document" holds the same row count per table as before the run
    And no object of "public", "recovery", "rwb_source_data" or another "rwb_" schema changed, and "rwb_sandbox" is neither renamed nor recreated
```

The eleven criteria above are new and test only this deliverable: the document estate of the DEV sandbox — the six types at the version in force, one document per agreed type per case, their fields and extracted values, the held intake items with their text, the checklist and completeness rows, the custody and retention rows, the personal-data gate on `document_field.extracted_value` and the DEV read-only role's read. No legacy criterion text is copied into this section. The legacy criteria AC1 to AC9 of RWB-E1-065 are owned elsewhere: the P1 schemas, the dictionary, the case volumes, the exception shapes and the P1 verifier by RWB-P1-E1065-CON and RWB-P1-E1065-APP; legacy AC1's document sentence, legacy AC7's `document_field.extracted_value` gate and legacy BR3 are the three lines answered here.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | No production data in DEV: the sandbox holds synthetic documents, synthetic field values and synthetic file references only (legacy BR1) | NFR-045; CTL-11; legacy BR1 |
| BR2 | The sandbox is built from the same DDL as SIT: here that means the per-service migration applied after the `rwb_document` baseline, at the table version in force (legacy BR2) | Legacy RWB-E1-065 BR2; DP-15; TSD P5 T3.1 |
| BR3 | Values come from the data dictionary and the lists of values, never from code: the six type codes, their fields, the write-once flags, the retention classes and the checklist rows are rows or list values (legacy BR3) | sys_fields; lov_value; Principle 1; FSD P5 A2.3; TSD P5 T3.1, T3.2 |
| BR4 | Every seeded document carries the write-once flag and the retention class of its type at the version in force, so the DEV sandbox can show the write-once refusal and the retention class of a document | FSD P5 A2.1, A2.17 (AC-ALT-P5-001-01, AC-ALT-P5-017-01); TSD P5 T3.1 (DF-DOC-009, DF-DOC-010); NFR-028, NFR-029 |
| BR5 | The seeded estate is written in the owner's schema `rwb_document` only: no `v_ace_*` view, no `public` table and no table of another service is read or written by this seed (DP-01) | Architecture v5 slides 16, 20 and 41; DP-01 |
| BR6 | Every role has a test identity before it has real users: here the DEV read-only role `rwb_sandbox_read` over the seeded schema, with no role and no person name written in `rwb_document` (legacy BR6) | DL39; legacy BR6 |
| BR7 | The seeded estate is applied by the per-service Flyway sequence, versioned and repeatable, and it writes the one table version in force rather than a version chosen in code (DP-15, DP-07) | DP-15; DP-07; FSD P5 AC-ALT-P5-003-01 |
| BR8 | There is no copy and no load table: the Workbench reads source data only through the source-data contract, and this slice reads the seeded case rows from the fixture file `case-seed-list.csv`; the source of each case ID is Pending (GAP-3369) (legacy BR8) | D-RCV-35; ADR-010; DP-05; legacy BR8 |
| BR9 | A clear identity number is allowed only in the ACE-shaped tables; schema `rwb_document` holds masked or synthetic values only (legacy BR9) | D-RCV-35 U4; CTL-11; legacy BR9 |

The four document-specific statements are BR4, BR5, BR7 and the retention part of BR1. BR4 turns the type table into behaviour on every seeded row: `document.write_once` and `document.retention_class` (DF-DOC-009, DF-DOC-010) are copied from `document_type` when the row is written, so a squad sees "LEGAL10Y" and true on a court notice and "GENERAL05Y" and false on an appraisal report without any rule running in DEV. BR5 keeps the estate inside the one schema the service owns, so no squad's test depends on another service's rows and no seeded row can be mistaken for an ACE row. BR7 is what makes a rebuild comparable with SIT: the same migration family, applied in the same order, writing the table version that the type table says is in force. The retention rows of the estate — the class on each document and the one `retention_action` row with its decision record — make the retention check demonstrable before JOB-17 runs anywhere.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| `rwb_document` baseline applied, tables empty | the rwb-document seed starts in the sandbox pipeline | P1 has built `public`, `recovery` and `rwb_source_data` in `rwb_sandbox` | Seeding |
| Seeding | the seeders finish and the verifier passes | Every check of section 4 step 11 passes | Seeded |
| Seeding | a seeder or the verifier fails | A type row, a storage_ref, an extracted value, a held item or a case ID fails its check | Failed; the migration rolls back and `rwb_document` keeps its previous rows |
| Seeded | the next build runs | The repeatable migration of this slice writes the same rows again; `rwb_sandbox` is never renamed or recreated | Seeded with the rows of the new run only |

| From | Event | Condition | To |
|---|---|---|---|
| a document written by the seed | the estate seeder commits the file and the row | The file is in the DEV container and its `content_sha256` is on the row | state "STORED", doc_version 1 |
| a held intake item written by the seed | the seeder commits the item and its pages | The item carries a review_reason of LOV-INTAKE-REVIEW | ocr_status "DONE" (or "RESCAN" where the synthetic page quality is below the threshold) and match_status of LOV-INTAKE-MATCH |
| a document of class "GENERAL05Y" stored on 1 November 2021 | the seeded retention action is written | No legal hold covers the document | one `retention_action` row with action "ARCHIVED", run_month "2026-12" and its decision record |

The document states and the held item states above are data the seed writes, not a state machine of this story: the document life (COPY_PENDING, STORED, ARCHIVED), the OCR status and the match status are moved by the store, the OCR pipeline and the retention job of this service (RWB-P5-E1024-APP, RWB-P5-E1049-APP, RWB-P5-E1052-APP). The seed state of `rwb_document` is the only build state this story moves, and it moves it in the sandbox pipeline, never through the service. The seed adds no value to LOV-CUSTODY or LOV-DOC-SOURCE; the values it writes are read from the rwb-case reference-data contract (DP-07).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-document service identity (the rwb-document login, DP-02) | Runs the migration and the seeders, reads and writes the ten tables of `rwb_document`, writes the one local decision record and serves the seeded rows through the P5 reads |
| RW-TRIBE, tribe lead and squad members | Read and extract the sandbox through `rwb_sandbox_read`, and open a seeded case, its documents, a held item and its checklist through the DEV service |
| RW-PLATADM, platform administrator | Owns the shared sandbox database and the pipeline stage that calls this migration; owns the DEV container grant and the retirement of the read-only role |
| Test identities per role | Call the DEV service against the seeded estate with their role's rights, as RWB-P4-E1065-APP seeds them |
| ACE team lead and ACE DBA | Own the DDL of the ACE-shaped test double and the 14 Tier 2 tables; that DDL is used by RWB-P1-E1065-CON and is not written, read or changed here |
| Decision-record library identity | Writes the one local decision record of the seeded retention action, with its sequence and hash link; no relay runs in the sandbox (DP-03) |
| RW-REFADM, reference data administrator | Prepares and approves the type table version that the sandbox mirrors; in the sandbox the same rows are written by the migration, and no approval is taken in DEV |

The per-service login name and the DEV-only read-only role are Not specified in the source documents (GAP-1053); the story keeps the legacy name `rwb_sandbox_read` for the read-only role and "the rwb-document login (DP-02)" for the service. The refusal shapes a role meets are MSG-P4-002 when the role holds no right in the Documents capability area and MSG-P4-003 when the case is outside the caller's scope; both are answered by rwb-access and the guard, not by the seed. No identity of this story may change a seeded row, and the role list, the capability letters and the scope values are rows of RWB-P4-E1065-APP, not of `rwb_document`. Every REST operation of this story is checked by the rwb-access authorise call (DP-08) before it serves a seeded row; the seed does not make that check.

### 11. Data

| BR Field ID | Entity in `rwb_document` | Field | Read or write |
|---|---|---|---|
| DF-DOC-001 to DF-DOC-011 | document | id, case_id, party_id, document_type, source, storage_ref, classification_confidence, review_status, retention_class, write_once, doc_version | Write (seed), then Read |
| DF-DOC-002, DF-DOC-004, DF-DOC-005 | document | case_id, document_type, source | Write (seed), then Read |
| DF-DOC-009, DF-DOC-010, DF-DOC-011 | document | retention_class, write_once, doc_version | Write (seed), then Read |
| DF-DOC-025, DF-DOC-026 | document | previous_version_id (empty at doc_version 1), content_sha256 | Write (seed), then Read |
| DF-DOC-012 to DF-DOC-017, DF-DOC-034, DF-DOC-035 | document_field | id, document_id, field_name, field_value, confidence, confirmed_by, extracted_value, extractor_version | Write (seed), then Read |
| DF-DOC-034 | document_field | extracted_value (the column legacy AC7 gates) | Write (seed), then Read |
| DF-DOC-018 to DF-DOC-024 | document_custody | id, document_id, moved_at, from_location, to_location, held_by, due_back | Write (seed), then Read |
| DF-REF-218 to DF-REF-233 | document_type | id, doc_type_code, label_en, label_th, write_once, retention_class, field_definitions, the two sign-off pairs, table_version, valid_from, valid_to, reference_version_id, classify_threshold | Write (seed), then Read |
| DF-REF-222, DF-REF-223, DF-REF-229, DF-REF-230 | document_type | write_once, retention_class, table_version, valid_from | Write (seed), then Read |
| DF-REF-234 to DF-REF-243 | document_checklist_item | id, stage_code, route_code, document_type, required, sort_order, table_version, valid_from, valid_to, reference_version_id | Write (seed), then Read |
| DF-DOC-036 to DF-DOC-044 | case_document_check | id, case_id, checklist_version, required_count, present_count, missing_types, complete, checked_at, last_event_id | Write (seed), then Read |
| DF-DOC-045 to DF-DOC-084 | document_intake | id, source, source_ref, file_name, file_size, captured_at, received_at, file_sha256, intake_ref, scan_result, scanned_at, case_id, document_id, ocr_ref, ocr_status, ocr_attempts, page_count, rescan_pages, ocr_quality, languages, ocr_engine_version, predicted_type, classification_confidence, type_candidates, classifier_version, classify_fallback, match_status, candidate_case_ids, extracted_fields, extract_status, extract_attempts, review_reason, review_outcome | Write (seed), then Read (the held items) |
| DF-DOC-085 to DF-DOC-090 | document_text | id, intake_id, document_id, page_no, text_content, quality | Write (seed), then Read |
| DF-DOC-091 to DF-DOC-095 | retention_action | id, document_id, run_month, action, decision_log_id | Write (seed), then Read |
| DF-DEC-001 to DF-DEC-018 and DF-DEC-028 to DF-DEC-031 | local decision record | decision code, actor, case ID, actions, decided at, chain sequence and hash link | Write |
| DF-DEC-003 | local decision record | decision_code ("DOCRET") | Write |
| DF-REF-244 to DF-REF-251 | document_hub_parameter | param_code, param_value, unit, table_version, valid_from, valid_to, reference_version_id | Not written by this story; Read only where a document story needs a parameter |

The seed writes the ten tables of `rwb_document` and the one local decision record, and nothing else: no case row, no ACE row, no role row, no `lov_value` row and no reference row of another service is written here. `document_hub_parameter` keeps its schema but its rows arrive with their own load stories. The ACE-shaped tables (the 22 Tier 1 and the 14 Tier 2 tables) and the 30 `v_ace_*` views belong to RWB-P1-E1065-CON and are never written by this slice; the seed reads no view and no `public` table, and it takes the seeded case rows from `case-seed-list.csv` instead of from a case table (source of each case ID: GAP-3369). `document.party_id` (DF-DOC-003) is the ACE customer business key and no foreign key backs it; FSD P5 A2.3 calls the same field `document.person_key`. Field IDs are those in the Logical Data Model and Data Dictionary v9 and the TSD P5 field ranges above. The P2 criteria and test data that read ACE views directly are not rows of this slice: they read the views through RWB-P1-E1065-CON, and this slice adds no read of a view. The seed, the business date, the volumes and the identifiers of the synthetic set are Not specified in the source documents (GAP-2154); they stay configuration of RWB-ITG-W1J01-ITG. The seed applies the rwb_document baseline and seeds it only after that baseline; the per-schema volumes of the 19 baselines are published in the build report until a source fixes them (GAP-0374).

### 12. Contract

#### 12.1 REST operations provided

None at run time. The seed is a migration and the estate is read with SQL; the reads the squads use are SQL through `rwb_sandbox_read` and the DEV service. The DEV service serves the seeded estate through the P5 operations of appendix T-A on the normal base `/api/recovery/document/v1`, and this slice adds no path, no query parameter and no response field:

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/cases/{caseId}/documents` | List the documents on a seeded case, with type, source, version and retention class | Documents R, scope applied | Not applicable |
| GET | `/documents/{documentId}` | Read a seeded document's metadata, versions and extracted fields | Documents R, scope applied | Not applicable |
| GET | `/documents/{documentId}/content` | Download the synthetic file the row points at | Documents R, scope applied | Not applicable |
| GET | `/cases/{caseId}/document-checklist` | Read the required types of the case with present counts, from the seeded checklist items and the check row | Documents R, scope applied | Not applicable |
| GET | `/documents` | Search the seeded documents by type, date, extracted field and free text | Documents R, scope applied | Not applicable |
| GET | `/review-items` | List the held intake items and the documents with fields in review | Documents R, scope applied | Not applicable |
| GET | `/intake-items/{intakeItemId}` | Read one held item with its OCR text, candidates and extracted fields | Documents R, scope applied | Not applicable |
| GET | `/intake-items/{intakeItemId}/content` | Download the file of a held item | Documents R, scope applied | Not applicable |

The write operations of appendix T-A (API-P5-001, API-P5-005, API-P5-006, API-P5-007, API-P5-013, API-P5-014, API-P5-015, API-P5-016, API-P5-017) are the surface of the store, the review, the custody and the generation stories of this service; this story seeds the rows they act on and changes none of them. Every endpoint declares the Documents capability area and its right (TSD P5 T6.1, T6.2), which is why a role without the right is refused before any seeded row is read.

#### 12.2 REST operations consumed

None at run time. This story answers from its own schema and calls no service: the seeded case rows it needs arrive as the fixture files of RWB-P1-E1065-CON, which publishes no operation for them (RD-P1-046), and the lists it validates against arrive as a fixture of the rwb-case reference-data contract (DP-07).

Two contracts are consumed as fixtures only. RWB-P1-E1065-CON publishes the versioned files `seed-profile.json`, `case-seed-list.csv`, `shape-table.csv`, the four stage fixtures and `tier2-ddl.sql`; the build order is ACE schema, V0001, Section A, Section B and then each service's own sequence (RD-P1-046), and it is not an element of the P1 contract package. The rwb-case reference-data contract returns LOV-RETENTION, LOV-STAGE, LOV-DOC-SOURCE, LOV-REVIEW, LOV-CUSTODY, LOV-OCR-STATUS, LOV-INTAKE-REVIEW, LOV-INTAKE-MATCH, LOV-SCAN-RESULT and LOV-EXTRACT-STATUS, so the story builds before either service is live in DEV; the criteria that name a case wait for GAP-3369.

#### 12.3 Events published

None. The DEV sandbox has no Kafka broker, so nothing is produced and no outbox relay runs: DP-09 is not a pattern of this story and the seed writes no `outbox_event` row. In a running environment the store publishes `DocumentStored` (event 16) and the extraction publishes `DocumentFieldsExtracted` (event 17) on `rwb.document.events.v1`, which is the behaviour of RWB-P5-E1024-APP and RWB-P5-E1053-APP; here the seeded documents announce nothing.

#### 12.4 Events consumed

None. A migration consumes no topic, the seed is the file and the fixture, and the DEV profile wires no consumer group into `rwb_document`.

#### 12.5 Workflows and activities

None. The seed is a migration and its seeders run in the build thread; this story starts no `DocumentIntakeWorkflow`, no activity and holds no Temporal worker of its own (Architecture v5 slide 16). The sandbox pipeline stage that calls this migration is not a workflow of this service.

DP-04 applies as a prohibition here: this story evaluates no decision table. The national ID check of the personal-data gate is a value test on `document_field.extracted_value`, not a DRL rule, and the seed writes no rule package, no workbook and no decision table.

#### 12.6 Schedules

None. The two jobs of rwb-document are JOB-12 Document intake (every 15 minutes) and JOB-17 Retention (monthly, first Sunday), and they belong to RWB-P5-E1049-APP and RWB-P5-E1052-APP (Architecture v5 slide 44). The sandbox pipeline stage that calls this migration is not a Schedule of this service.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| document | P5 (`rwb_document`) | One row per synthetic document, each row synthetic |
| document_field | P5 (`rwb_document`) | One row per field definition per document, with a synthetic extracted value |
| document_custody | P5 (`rwb_document`) | One synthetic movement so the custody read is demonstrable |
| document_type | P5 (`rwb_document`) | The six rows at "DOCTYPE-2026.11", written by this seed and by RWB-P5-E1025-APP in a running environment |
| document_checklist_item | P5 (`rwb_document`) | The checklist rows of "CHK-2026.11", synthetic but the same shape as the loaded version |
| case_document_check | P5 (`rwb_document`) | One synthetic completeness row for case "RW-2026-000001" |
| document_intake | P5 (`rwb_document`) | The held synthetic items and their pages |
| document_text | P5 (`rwb_document`) | The OCR text of the held items' pages |
| retention_action | P5 (`rwb_document`) | One synthetic action of the seeded appraisal report, with its decision record |
| document_hub_parameter | P5 (`rwb_document`) | Present in the schema and not written by this story |
| local decision record | P5 rows in `rwb_document`, written through the P7 decision-record library | One entry for the seeded retention action, with no relay |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_document` | Present in the schema and not written by this story, because no event leaves the sandbox |

rwb-document reads no table of another service and holds no foreign key across services (DP-01); `recovery_case` is reached only as a case ID value (source Pending, GAP-3369), and `lov_value` and the reference tables belong to rwb-case (P3) and reach this story only through the reference-data contract (DP-07). Every row in this table, in this sandbox, is synthetic: no row of a running environment is copied into `rwb_document` and no row of `rwb_document` is promoted out of DEV.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-P1-E1065-CON fixture files | The P1 contract of this legacy key | `seed-profile.json` (seed `20261128`, total 2,812), `case-seed-list.csv` (no case ID, no case number), `shape-table.csv` and the four stage fixtures full, empty, refused and timeout |
| reference-data fake (RWB-P3-E1043-CON) | DP-07 | LOV-RETENTION with LEGAL10Y and GENERAL05Y, LOV-STAGE, LOV-DOC-SOURCE, LOV-REVIEW, LOV-CUSTODY, LOV-SCAN-RESULT, LOV-OCR-STATUS, LOV-INTAKE-MATCH, LOV-INTAKE-REVIEW and LOV-EXTRACT-STATUS of TSD P5 T3.2 |
| Blob container stub | The DEV file store | A container that accepts the synthetic files and returns their hash, and a container that refuses a write for the storage_ref path (X3) |
| decision-record library stub | DP-03 | A local chain that accepts the seeded entry, and a stopped chain that fails the build before a row is published |
| held intake seed rows | This slice | At least one item per held shape with its review reason and pages; not a P1 fixture (RD-P1-046) |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None outbound; the DEV service serves the eight reads of section 12.1 on `/api/recovery/document/v1` | The seed calls no service; the case list and the lists arrive as fixtures; one hop and 2 s timeout on the inbound read |
| Kafka | None | No topic produced and none consumed in the DEV sandbox; DP-09 is not a pattern of this story |
| Temporal | None | No workflow, no activity and no Schedule in this story |
| File | The synthetic documents of the estate | One file per seeded document in the DEV Blob container, plus the files of the held intake items; the write-once legal types go to the legal container |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, module `sandboxseed`, Java package `th.co.scb.ace.workbench.recovery.document.sandboxseed`. The sandbox database scope per service and the placement of the generator are Not specified in the source documents (GAP-0501).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

This is a secondary slice: it adds no new build dependency of its own. Metadata "Depends on (build)" stays `None` and "Contract dependencies" stays `RWB-P1-E1065-CON` exactly as the Work Package fixes them, and the platform contract libraries of DP-03, DP-04, DP-07, DP-15 and DP-19 arrive with the baseline, not with this story.

DP-01 is the first rule of the seed: every row lands in `rwb_document`, the type table is read from there, and the case ID is a value from the fixture, never a row read from another schema.

DP-03 applies as the local decision record written for the seeded retention action: the one `retention_action` row of the appraisal report carries one entry written through the decision-record library, with the decision code "DOCRET", the class "GENERAL05Y", the retention version "RET-2026.11" and the expiry date of FSD P5 AC-ALT-P5-017-02; the entry stays in `rwb_document` because no relay runs.

DP-04 applies as a prohibition: this seed evaluates no rule. The personal-data gate is a value test on `document_field.extracted_value`, and no DRL, workbook or rule package is written or read by the seed.

DP-05 applies as a prohibition: the seed reads no `v_ace_*` view and no `public` table. The seeded case rows arrive as `case-seed-list.csv` and the shape counts as `shape-table.csv` of RWB-P1-E1065-CON; the held intake rows are seed data of this slice.

DP-07 is the type and list read: the six type codes are rows of `document_type`, the retention classes of those rows are checked against LOV-RETENTION, and the checklist, source, review, custody, scan, OCR, match and extract values are checked against their lists, all read once per build through the rwb-case reference-data contract and never copied into `rwb_document`.

DP-15 is the per-service Flyway sequence that carries the seed: `V1065_1__document_estate_seed.sql` runs after the `rwb_document` baseline in the shared `rwb_sandbox`, which is never renamed or recreated, and `R__document_estate_seed_rebuild.sql` re-applies the same rows on a rebuild.

DP-13 is the base of the DEV service: the seeded estate is served at `/api/recovery/document/v1`, and the legacy `/api/recovery/v1` shape is not used by this story.

DP-19 is the route the screens use in DEV: SCR-30 Case documents and SCR-31 Document review queue reach the seeded rows through the gateway-bff composite route, one hop to rwb-document. The refusal shapes of both screens are MSG-P4-002 and MSG-P4-003 (section 10); the other states of both screens are Not specified in the source documents (CG-ALL-6129; CG-ALL-6130).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DocumentTypeSeeder | Service | Writes the six `document_type` rows at "DOCTYPE-2026.11" with their field definitions, write-once flags, retention classes, valid_from and table_version; refuses a row outside LOV-RETENTION or without a version |
| DocumentEstateSeeder | Service | Writes one `document` row per agreed type on every case of `case-seed-list.csv` with its storage_ref, content_sha256 and the write_once and retention_class of its type; writes the synthetic files to Blob; writes the custody movement and the one retention action |
| DocumentFieldSeeder | Service | Writes one `document_field` row per field definition with a deterministic extracted_value and a confidence, masks an identity number, and runs the national ID check before commit |
| HeldIntakeSeeder | Service | Writes the held `document_intake` items with their review reason, status and file hash, and their `document_text` pages |
| ChecklistSeeder | Service | Writes the `document_checklist_item` rows of "CHK-2026.11" and the `case_document_check` row of case "RW-2026-000001" |
| DocumentSeedVerifier | Service | Reads the whole estate back: one table version, one document per agreed type per case, one field row per field definition, the pattern scan, the held items and pages, the custody, retention and checklist rows, every storage_ref present, and the row count per table |
| DevGrantScript | Script | Grants SELECT on schema `rwb_document` to the DEV read-only role of section 10, with no UPDATE, no DELETE and no access to the local decision-record table |

**Database and migrations**

- Writes the ten tables of `rwb_document` and the one local decision record; writes no other table and reads no other schema (DP-01).
- Migration in this story: `V1065_1__document_estate_seed.sql`, the versioned per-service migration that carries the type rows and the estate, run after the `rwb_document` baseline, after the P1 build of `public`, `recovery` and `rwb_source_data` (RD-P1-046).
- Its companion `R__document_estate_seed_rebuild.sql` is the repeatable migration that writes the same rows again from the same seed value and the same fixture, so a rebuilt sandbox holds the same counts and the same `content_sha256` values (AC5).
- The seed is idempotent by construction: the repeatable migration clears the estate tables it writes and writes them again from the seed value, deletes nothing outside those tables, and refuses a type row that belongs to two table versions.
- No column, index or constraint is added for a case, an ACE value or an identity; the case ID is a value and the customer key is a business key with no foreign key.

**Configuration and reference data**

- `rwb.document.sandbox.seed=20261128` is the seed value of the deterministic value factory.
- `rwb.document.sandbox.type-table-version=DOCTYPE-2026.11` is the table version the seed writes, the version in force from 30 November 2026 (FSD P5 AC-ALT-P5-003-01).
- `rwb.document.sandbox.documents-per-case` is the number of documents beyond the one per agreed type; the value is Not specified in the source documents (GAP-1051; ASM-1999) and the story fixes one per type when it is unset.
- `rwb.document.sandbox.synthetic-file-pattern` is the file name pattern of the synthetic PDFs; the value is Not specified in the source documents (GAP-1052; ASM-2000).
- `rwb.document.sandbox.container` and `rwb.document.sandbox.legal-container` name the DEV containers; their names are Not specified in the source documents (GAP-1053; ASM-2001) and the running names of FSD P5 A2.1 are "rwb-docs" and "rwb-docs-legal".
- `rwb.document.sandbox.held-intake-per-shape` is the count of held items per shape; the value is Not specified in the source documents (GAP-1054; ASM-2002) and the story fixes at least one per shape.
- The type codes, fields, write-once flags, retention classes and checklist rows are rows of the seed file and the type table; the retention, stage, source, review, custody, scan, OCR, match and extract values are compared with the lists read through the rwb-case reference-data contract (DP-07), and no list is kept in `rwb_document`.
- The login is the rwb-document login (DP-02) and the DEV-only read-only role is the role of section 10; both are Not specified in the source documents (GAP-1053).
- The feature switch is `rwb.document.sandbox-estate`, read as a parameter: on in the DEV profile only; off means the seed does not apply and the document tables stay empty, never half filled.

**Build steps**

1. Value factory and `DocumentTypeSeeder` over the six types, with a test per list violation (an unknown retention class, a missing valid_from, a second table version) and a test that no type code, class or field name appears in the Java source.
2. `V1065_1__document_estate_seed.sql` and `R__document_estate_seed_rebuild.sql`, with the read-back of AC1 and the same-seed test of AC5.
3. `DocumentEstateSeeder` over the case list of the fixture, with the case reference of each row (GAP-3369), the per-type loop, the Blob write, the storage_ref check and the write_once and retention_class copy; tests for AC2.
4. `DocumentFieldSeeder` with the field definitions of each type, the deterministic value per field, the confidence, the identity mask and the national ID check; tests for AC3.
5. `HeldIntakeSeeder` over the held shapes with the review reason, the status, the file hash and the page text; test for AC4.
6. `ChecklistSeeder` over "CHK-2026.11" and the completeness row of case "RW-2026-000001"; tests for AC4.
7. `DocumentSeedVerifier` with every check of its row above, including the pattern scan and the storage_ref check, and the decision record of the one retention action; tests for AC3, AC5 and AC8.
8. `DevGrantScript` for the DEV read-only role of section 10: SELECT on the schema and no UPDATE, no DELETE and no SELECT on the decision-record table; test for AC6.
9. Contract-fake run of RWB-P1-E1065-CON and the reference data, so the story builds and proves every criterion before rwb-source-data and rwb-case are live in DEV; test for AC7.

**Feature switch.** `rwb.document.sandbox-estate`, read as a parameter; off leaves the tables empty and publishes nothing.

**Done when.** The tests in section 16 pass, the fixture files of RWB-P1-E1065-CON are read at their published version, GAP-3369 is closed, a rebuilt `rwb_document` holds the six types at "DOCTYPE-2026.11", one document per agreed type on every synthetic case with its fields and no clear national ID in `document_field.extracted_value`, the held items, the checklist and completeness rows, one custody movement and one retention action with its local decision record, and the DEV read-only role of section 10 reads the schema without being able to change it.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | The caller's role holds no right in the Documents capability area | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case of the read is absent or outside the caller's scope | This case is not in your scope. |
| MSG-P5-002 | A write-once document is changed through the DEV service or the container | Legal documents cannot be changed. Add a new version instead. |
| MSG-P5-003 | A document with fields below the confidence threshold is opened | Some fields need checking. The document is in the review queue. |

Seed failures are reported in the pipeline result with the table and the column named: a type row outside LOV-RETENTION, a missing valid_from or table_version, a storage_ref absent from the container, an extracted value that matches the national ID pattern, a held item without a review reason and a case ID absent from the fixture each fail the build with the row and the column, and no user message applies. For MSG-P4-002 in this story, {action} names the action the caller tried — for example "open the case documents" — and never a case fact, a field value or a role name.

### 15. Screens and states

No screen in this story. SCR-30 Case documents — documents on a case by type, with the extracted fields and versions (FSD P5 Screens; first in E1) — will show the six types, their confidence and their retention class that this seed writes, and SCR-31 Document review queue will show the held intake items and their pages, so both screens are demonstrable in DEV before a real scan and before SCR-31 is built. The screens themselves belong to RWB-P5-E1026-APP and the store, OCR and review stories of this service.

Both screens reach the estate only through the gateway-bff composite route (DP-19), which calls rwb-document for the documents and rwb-access for the decision, one hop each. The route specification and the field-level masking of the composite route are Not specified in the source documents (GAP-1053; ASM-2001).
The states of SCR-30 are loading (Screen Specifications v1); empty, error and no access are Not specified in the source documents (CG-ALL-6129).
The states of SCR-31 are loading (Screen Specifications v1); empty, error and no access are Not specified in the source documents (CG-ALL-6130).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P5-E1065-APP-01, TC-P5-E1065-APP-02, TC-P5-E1065-APP-03, TC-P5-E1065-APP-10 | AC1, AC2, AC4, AC7, BR2, BR3, BR4, BR5 | End to end | The six types at "DOCTYPE-2026.11" with COURT_NOTICE "LEGAL10Y" write_once true and APPRAISAL_REPORT "GENERAL05Y" write_once false; the documents of case "RW-2026-000001" with their fields, one custody movement, the checklist items and the check row; seed 20261128 |
| TC-E1-065-02 | AC6, BR6 | End to end | The DEV read-only role `rwb_sandbox_read`: SELECT on "document", "document_type" and "document_field", a refused UPDATE and the unchanged row |
| TC-P5-E1065-APP-11 | No criterion here; the dictionary build belongs to RWB-P1-E1065-CON | End to end | A test migration adding `recovery_case.risk_tier` with its dictionary row and list LOV-RISK-TIER |
| TC-E1-065-04 | No criterion here; the build gate on a missing dictionary entry belongs to RWB-P1-E1065-CON | End to end | A dictionary fixture without the row for `recovery_case.closure_reason` |
| TC-P5-E1065-APP-12 | AC5, BR2, BR7 | End to end | Two builds for commit "a1b2c3d" and seed 20261128; the same document row count per type and the same content_sha256 for the documents of case "RW-2026-000001" |
| TC-P5-E1065-APP-13 | No criterion here; the empty-list failure belongs to RWB-P1-E1065-CON | End to end | An empty LOV-PRODUCT seed |
| TC-E1-065-07 | AC3, BR1, BR9 | End to end | A 13-digit national ID with a valid check digit injected in `document_field.extracted_value` (fails the build) and a clear identity number in `public.customer` (allowed, RWB-P1-E1065-CON) |
| TC-E1-065-08 | No criterion here; the boundary accounts belong to RWB-P1-E1065-CON | End to end | Accounts at 89 and 90 days past due; they are account rows of the P1 sandbox, not cases, and are built by RWB-P1-E1065 (RD-P1-046) |
| TC-E1-065-09 | AC5 for the same-seed result; the build lock itself belongs to RWB-P1-E1065-CON | End to end | Two builds started together |
| TC-P5-E1065-APP-04 | AC8, BR8 | Component | The DEV profile with no broker: the seeded retention action carries one local decision record and no topic is produced to and no consumer group is created |
| TC-E1-065-10 | No criterion here; the access refusal belongs to RWB-P4-E1065-APP and RWB-P1-E1065-CON | Component | A test identity holding RW-REFADM calls the sandbox case list through the DEV service; refused with MSG-P4-002 by rwb-access with the identities seeded by RWB-P4-E1065-APP |
| TC-P5-E1065-APP-08 | Contract of section 12 (operations, events and activities) | Component | The P5 operations on `/api/recovery/document/v1` and the fakes of section 12.8, with no event published and each operation answering its contract |
| TC-P5-E1065-APP-09 | Boundary of the section 12.7 tables | Component | Each table of section 12.7 at its boundary values for seed 20261128 |
| TC-P5-E1065-APP-05 | AC9, BR4 | End to end | The seeded documents of all cases of the fixture at "DOCTYPE-2026.11": COURT_NOTICE "LEGAL10Y" write_once true and APPRAISAL_REPORT "GENERAL05Y" write_once false on every row; seed 20261128 |
| TC-P5-E1065-APP-06 | AC10 | Component | Each P5 operation on `/api/recovery/document/v1` called without identity, without the role of the operation and with a document identifier not in "document"; answers 401, 403 and 404 with no row changed |
| TC-P5-E1065-APP-07 | AC11 | Component | A seed with a retention class outside LOV-RETENTION over an `rwb_document` that holds an earlier estate; rolled back, row counts unchanged, no other schema changed |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end, Access to Component and Resilience to NFR. All ten legacy test cases of this key are listed above with the slice of behaviour this story answers: the document estate for TC-P5-E1065-APP-01, TC-P5-E1065-APP-02, TC-P5-E1065-APP-03, TC-P5-E1065-APP-10, the read-only role for TC-E1-065-02, the same-seed result for TC-P5-E1065-APP-12 and TC-E1-065-09, the `document_field.extracted_value` gate for TC-E1-065-07, and one new case, to be added in Test Cases v9, for the DEV profile with no broker that AC8 tests; the dictionary build, the missing dictionary entry, the empty-list failure, the boundary accounts and the build lock belong to RWB-P1-E1065-CON, and TC-E1-065-10 belongs to RWB-P4-E1065-APP and RWB-P1-E1065-CON. The -ITG copies of these cases are not here — they belong to RWB-ITG-E1065-ITG, which proves the same values across rwb-source-data, rwb-document, rwb-case and the DEV environment end to end.

Version 3: rows that cite `TC-P5-E1065-APP-` identifiers are this story's rows of Recovery Workbench Test Cases v9. Where a shared legacy identifier now names another story's case there, this story's identifier replaces it, and cases run by one identifier are joined in one row.

### 17. Guardrails

- No business value in code: the type codes, the fields, the write-once flags, the retention classes, the checklist rows, the seed value, the table version, the per-case count, the file pattern and the container names are rows, list values, parameters or the fixture. No type code, class or list value appears in Java, and the verifier fails a build whose seed names a retention class outside LOV-RETENTION.
- Synthetic only, and no clear personal value in `rwb_document`: every name, identifier and extracted value is synthetic, an identity number is masked, and the pattern scan blocks a value that looks real in `document_field.extracted_value`, in every other seeded text column and in the OCR text of a held item. A clear identity number in the ACE-shaped tables is allowed there and is not this slice's data.
- The verifier gate stands between the seed and the squads: a build that fails any check of section 4 step 11 rolls the seed back, so `rwb_document` keeps its previous rows and no squad ever reads a half-seeded estate.
- No cross-schema write and no cross-schema read: `rwb_document` holds no foreign key into another schema and no copy of a case, a list value or an ACE row (DP-01); the seeded case rows come from the RWB-P1-E1065-CON fixture files (case ID source: GAP-3369) and the lists from the reference-data contract (DP-07), and the ACE-shaped tables and the 30 views belong to RWB-P1-E1065-CON.
- No event leaves the sandbox: the seeded retention action carries one local decision record and no relay, and no `outbox_event` row is written (DP-03, and DP-09 is not a pattern of this story).
- One owner for retention and write-once: the seed copies the class and the flag from the type table and never decides a retention period or a hold; the retention job of RWB-P5-E1052-APP acts on the rows and the store of RWB-P5-E1024-APP enforces the write-once refusal.
- The seed is a per-service Flyway migration in `rwb_document`, versioned and repeatable, and no migration of this service touches another service's schema or the shared baseline (DP-15).
- Personal data rule: no personal data of a real person is written to `rwb_document`; names, identifiers and values are synthetic, an identity number is masked before commit, and the PDPA masking of REQ-RDF-010 applies (NFR-045).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-001 | 14 data products, each with one system of record and one owner, each reachable in DEV without a request to another team | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-DCM-01, FEAT-DCM-03, FEAT-DCM-09, FEAT-DCM-16, FEAT-DCM-17, FEAT-DCM-19, FEAT-DCM-20 | All recovery processes | R-UNI-17, R-UNI-05, R-UNI-07, R-UNI-20, R-UNI-10; DL15, DL16; D-RCV-35; CTL-11 | TC-P5-E1065-APP-01, TC-P5-E1065-APP-02, TC-P5-E1065-APP-03, TC-P5-E1065-APP-10, TC-P5-E1065-APP-12, TC-E1-065-09 |
| REQ-RDF-010 | Access per data product by role; personal data masked in line with PDPA | Program section 6.7 (NFR-045) | FEAT-DCM-01, FEAT-DCM-03, FEAT-DCM-09, FEAT-DCM-16, FEAT-DCM-17, FEAT-DCM-19, FEAT-DCM-20 | All recovery processes | CTL-11; D-RCV-35 U4; legacy BR1, BR9 | TC-E1-065-02, TC-E1-065-07 |

The supporting features of the document model are FEAT-DCM-01 (store with a write-once container for legal types), FEAT-DCM-03 (the six document types and their fields), FEAT-DCM-09 (extraction), FEAT-DCM-16 (the checklist as reference data), FEAT-DCM-17 (retention classes), FEAT-DCM-19 (the hub as system of record) and FEAT-DCM-20 (versioning), which the FSD P5 module pairs with its own requirements in RWB-E1-024, RWB-E1-025, RWB-E1-053, RWB-E1-040 and RWB-E1-041; this slice answers them only for the DEV document estate and changes none of their design. The -ITG copies of the test cases are carried by RWB-ITG-E1065-ITG.

| Legacy reference | Where it is kept |
|---|---|
| Legacy section 1 (the story statement) | Section 1 of this story, narrowed to the document estate; the sandbox itself is RWB-P1-E1065-CON |
| Legacy AC1 (the sandbox exists), document sentence | AC2 and AC4 of this story; the schemas, the 92 tables and the 30 views are RWB-P1-E1065-CON and RWB-P1-E1065-APP |
| Legacy AC7 (no clear personal value outside the ACE tables) | AC3 of this story for `document_field.extracted_value`; the verifier of the whole sandbox is RWB-P1-E1065-CON |
| Legacy BR1, BR2, BR3, BR6, BR8, BR9 | Section 8 of this story |
| Legacy BR4, BR5 (exception shapes and case volumes) | RWB-P1-E1065-CON and RWB-P1-E1065-APP; this story reads only the case list they produce |
| Legacy section 12 (pipeline stage and the DEV endpoint) | Section 12 of this story; the pipeline stage is RWB-P1-E1065-CON; the DEV read is the P5 operations on `/api/recovery/document/v1` |
| Legacy sections 13 to 17 | Sections 13, 15 and 17 of this story for the document estate; the generator, the verifier and the grant on schema `recovery` are RWB-P1-E1065-CON |
| Legacy TC-E1-065-01 to TC-E1-065-10 | Section 16 of this story, with the slice of behaviour each case answers |

Open decisions this story applies: DL15 (assumption ASM-5264); DL16 (ASM-1094, ASM-5264); DL26 (ASM-0247, ASM-0264, ASM-0275, ASM-0355); DL39 (ASM-1617, ASM-2705). Each decision is still open; each assumption is confirmed and the build proceeds on it.

### 19. Out of scope

- The DEV database `rwb_sandbox`, the ACE-shaped test double, the 92 recovery tables, the 30 `v_ace_*` views, the dictionary-driven generator, the P1 verifier, the pipeline stage and the read-only grant on schema `recovery`: RWB-P1-E1065-CON, RWB-P1-E1065-APP and RWB-P1-E1065-DB.
- The role list, the permission matrix and the synthetic test identities: RWB-P4-E1065-APP.
- The case rows, their volumes and the exception shapes: RWB-P3-E1065-APP and RWB-P1-E1065-CON.
- The deviation rows of the sandbox: RWB-S8-E1065-APP.
- The wave 1 contract-test harness, its pipeline wiring and the composition of the synthetic test data set: Not specified in the source documents (GAP-0384).
- The type maintenance screens and the load path of a type version in a running environment: RWB-P5-E1025-APP.
- The document store, the upload, the index and the search of the document screens: RWB-P5-E1024-APP and RWB-P5-E1026-APP.
- The OCR pipeline (JOB-12), the classification and extraction evaluation samples and the review queue behaviour: RWB-P5-E1049-APP and RWB-P5-E1050-APP, RWB-P5-E1053-APP.
- The checklist maintenance, the custody action and the retention job (JOB-17) with its decision entries in a running environment: RWB-P5-E1040-APP, RWB-P5-E1041-APP and RWB-P5-E1052-APP.
- The end-to-end proof of these values across the sandbox, rwb-source-data, rwb-document and rwb-case: RWB-ITG-E1065-ITG.
- The `rwb_document` schema baseline, the platform migration role, the `rwb.document.events.v1` topic and consumer groups, the observability and the runbook of this service.

### Remaining delivery steps

- Settle how rwb-document obtains the case ID and case number of the seeded cases (GAP-3369; data architect with the rwb-case service owner).
- Publish the RWB-P1-E1065-CON fixture files at a version and pin it (service contract owner).
- Confirm the shape counts (GAP-3278; data architect).
- Size the story at refinement and obtain epic design sign-off (squad lead, solution architect).
- Add the new test cases in Test Cases v9 and load test data in DEV (test lead).
