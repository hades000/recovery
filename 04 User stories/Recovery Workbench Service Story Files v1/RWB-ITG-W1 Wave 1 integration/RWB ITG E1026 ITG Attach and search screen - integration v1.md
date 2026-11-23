# RWB-ITG-E1026-ITG Attach and search screen

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-026 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1026-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-026 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P3-E1045-APP, RWB-P3-E1030-APP, RWB-P5-E1026-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-DCM-008, REQ-DCM-001, REQ-DCM-010, REQ-DCM-011) |
| Status | Draft (realignment v1) |

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof of the RWB-E1-026 attach and search screen across rwb-document (P5, the owner of the document), rwb-case (P3, the parameter and reference-data owner) and the gateway-bff composite route for SCR-30**, so that **the upload, the case document list, the type-and-date search and the checklist are proved on the real services and through the one composite route the screen uses before wave 1 exits**.

### 2. Business rationale

The legacy screen is a case record view tab that calls the document endpoints and the case record view directly: upload with a type, list of every document on the case, search by type and stored date, and a checklist placeholder showing which of the six agreed types are present. Those facts matter to the case owner, and the legacy criteria that test the behaviour inside the document hub stay where they belong: AC1 to AC11 of RWB-E1-026 are owned by RWB-P5-E1026-APP and are not copied here. This integration story owns the ten criteria that no single service can prove, because in the target the screen is not a direct caller.

In the target architecture SCR-30 is a gateway-bff composite route (DP-19) over the P5 document contract and the P3 parameter and queue-measure contracts: the screen makes one call, gateway-bff composes it from the document list of P5 and the parameter, reference-data and case reads of P3, and the browser calls no service directly. The upload path is proved on the P5 contract, the parameters and the list values come from the P3 contracts (DP-06, DP-07), the decision record of a store is written by the local decision-record library (DP-03), and the document, its versions, its metadata and its stored file are owned by P5 rwb-document in `rwb_document` (DP-01). A test of the screen inside one service would pass while the composite, the parameter source or the storage ownership were wrong, and that is exactly what this story prevents.

No service contract is faked. The suite exercises the published wave 1 contracts of P5 rwb-document and P3 rwb-case, the composite route of gateway-bff and a real Blob container; the only stubs are the external ones named in section 12.8. The composite path, its aggregation shape and the source behind the malware scan are not published in the Ownership Map, so the suite asserts the composite response and the scan result only, and the open point is recorded as GAP-0351 and ASM-0445. The release date 30 November 2026 is copied unchanged and is tentative.

### 3. Preconditions

- RWB-P5-E1026-APP is done: the upload, the case document list, the document read, the document content read, the duplicate response, the idempotency handling and the checklist operation are in SIT, and `rwb_document` is the only writer of the document tables.
- RWB-P3-E1045-APP is done: the parameter contract publishes `INTAKE_MAX_FILE_MB` = 25 and `INTAKE_ALLOWED_TYPES` = PDF, JPG, PNG, and the document type and source lists are readable as reference data through the P3 contract.
- RWB-P3-E1030-APP is done: the case read and the queue-measure read of the case record view are published, so gateway-bff composes SCR-30 from real answers.
- The gateway-bff composite route for SCR-30 is deployed in SIT with its session and coarse-permission check (DP-19).
- The published contracts of P5 rwb-document and P3 rwb-case are versioned in the registry, and the suite consumes only those contracts.
- The harness RWB-ITG-W1J01-ITG is available with its synthetic case set, its 50-document case and its six document types.
- The environment is SIT, the topics of the wave 1 services are live with their retry and `.dlt` topics, and a Blob container with an intake and a quarantine path is available (Azurite in the lower environment).
- Feature flag `rwb.dochub.casedocs` is on.
- No production data is used and no production connection is opened; every case number, user identity, document and file is synthetic.
- The release date 30 November 2026 is tentative; a date is not a condition of this story.

### 4. Flow

1. QA integration engineer: seeds the synthetic case set of the harness RWB-ITG-W1J01-ITG — case RW-2026-000123 with 50 documents, of which 12 are `COURT_NOTICE` and 4 were stored in October 2026, and 1 is `APPRAISAL_REPORT` — and signs in as the synthetic identity that holds RW-CASEOWN for that case; no production data is used.
2. Harness: calls the gateway-bff composite route for SCR-30 for case RW-2026-000123 and asserts that the response carries the document list that P5 publishes for the case, in the same order and with the same count.
3. Harness: uploads `court-notice-0007.pdf` of 2 MB with type `COURT_NOTICE` and source `UPLOAD` through `POST /api/recovery/document/v1/documents`, and asserts 201, the source and doc_version 1.
4. Harness: waits for `rwb.document.DocumentStored.v1` on `rwb.document.events.v1` and reads the list again through the composite; the new document is at the top within 5 seconds of submit.
5. Harness: searches type `COURT_NOTICE` from 1 October 2026 to 31 October 2026 and asserts the 4 October court notices, newest first, with count 4.
6. Harness: reads the checklist for the case and asserts the six agreed types with the present counts.
7. Harness: posts the negative uploads — no type, the EICAR file, the same file twice, the double submit with the same Idempotency-Key and the two files at the size boundary — and records every status and message.
8. Harness: posts the inverted date range and the empty search, and asserts the refusal and the empty sentence.
9. Harness: calls the composite with an identity whose scope excludes the case and asserts the 403 and that no document name is shown.
10. Harness: writes the evidence report with one verdict per test case, removes the synthetic documents and the quarantined file, and records the cleanup.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Upload with no document type | Refused by the owning service with 422; the composite passes the refusal through; nothing stored | MSG-GEN-001 | AC4 |
| X2 | The file fails the malware scan | Refused with 422; the file is held in quarantine; no document row exists | MSG-P5-016 | AC5 |
| X3 | The file type is not allowed | Refused with 415; nothing stored | MSG-P5-001 | TC-E1-026-06-ITG (regression) |
| X4 | The same file and type is already on the case | The existing document is returned and highlighted; no second document | MSG-P5-024 | AC6 |
| X5 | The submit is sent twice with the same Idempotency-Key | One document and one decision record; the second call returns the first result | None | AC7 |
| X6 | Date from is after date to | The owning service refuses the range, the composite passes the refusal through and no search runs | MSG-GEN-003 | AC8 |
| X7 | Search matches nothing | Empty state with the sentence and the clear filter action | None | AC8 |
| X8 | Case is outside the user's scope | Refused with 403 and no document name is shown | MSG-P4-003 | AC9 |
| X9 | Role without Documents C uploads | Refused with 403; the Upload action is not shown | MSG-P4-002 | TC-E1-026-12-ITG |
| X10 | The decision record write fails during the store | Nothing is stored; the dialog shows the message | MSG-P7-003 | TC-E1-026-13-ITG |
| X11 | A consumed contract drifts from the published one (path, field, status, list or event schema) | The preflight fails on the contract test and the run stops before any assertion; the drift is reported against the owning service and no fake is put in its place | None | Preflight; AC1, AC3 |
| X12 | The gateway-bff composite route for SCR-30 is missing or returns a server error | The run fails as a deployment fault and names the route; no upload and no search is asserted through a direct service call in its place | None | AC1, AC2, AC3 |
| X13 | The W1J01 synthetic set, its 50-document case or its six types do not match the run | The run fails as a fixture fault and names the mismatched element; no production value and no invented document is substituted | None | AC2, AC3 |
| X14 | A consumed call exceeds the 2 s budget | The call is recorded as a budget breach, the assertion is not written from a partial answer, and the evidence report names the operation and the elapsed time | None | AC1, AC2, AC9 |
| X15 | A suite step tries to read a service schema directly | The step does not exist: the suite ships with no client for a service schema, and the pipeline scan fails any change that adds one | None | Section 17 |

X1 to X10 are the legacy exception paths carried onto the real services; X11 to X15 are the cross-service failures that appear only when the run leaves one service.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is a module of its own and reuses the harness RWB-ITG-W1J01-ITG; it needs the three integration dependencies and the published contracts of P5 and P3 plus the composite route, not their source code, and it owns no schema and no table |
| Negotiable | The fixture composition, the poll interval and the report layout are configuration; the case number, the type list, the messages, the size limit and the 5 second expectation are fixed by the legacy story and the parameter contract |
| Valuable | Proves across services what no single service story can prove: the composite composition, the stored document at the top of the list, the type-and-date search, the checklist counts, the parameter-driven size limit and the scope refusal at the edge |
| Estimable | One suite module, one fixture pack, eight contract probes, one size-boundary pair and one report |
| Small | Ten scenarios over two services and one composite route; no service code and no schema change |
| Testable | Every criterion asserts a contract response, a composite field, a count, an exact message or a container state; all data is synthetic |

### 7. Acceptance criteria

```gherkin
Feature: Attach and search screen, proven across the wave 1 services and the SCR-30 composite route

  Background:
    Given document type table version "DOCTYPE-2026.11" is in force
    Given user "TEST-CO-01" holds RW-CASEOWN and owns case "RW-2026-000123"
    Given the wave 1 services rwb-document and rwb-case are deployed in SIT behind gateway-bff
    Given the RWB-ITG-W1J01-ITG synthetic set is loaded and no production data is used

  Scenario: AC1 The composite returns the P5 list and a new upload shows at the top (new, D-RCV-60)
    Given the gateway-bff composite route for SCR-30 serves case "RW-2026-000123"
    When "TEST-CO-01" opens the Documents tab of the case
    Then the composite returns the document list that P5 publishes for the case, with the same items and count
    When "TEST-CO-01" uploads "court-notice-0007.pdf" of 2 MB with type "COURT_NOTICE"
    Then the P5 response is 201 with source "UPLOAD" and doc_version 1
    Then the document shows at the top of the composite list within 5 seconds of submit

  Scenario: AC2 Type-and-date search returns exactly the October court notices (new, D-RCV-60)
    Given case "RW-2026-000123" holds 50 documents of which 12 are "COURT_NOTICE"
    Given 4 of the court notices were stored between 1 October 2026 and 31 October 2026
    When "TEST-CO-01" searches type "COURT_NOTICE" from 1 October 2026 to 31 October 2026
    Then exactly the 4 court notices stored in October return, newest first
    Then the result count reads 4

  Scenario: AC3 The checklist lists the six agreed types with their present counts (new, D-RCV-60)
    Given case "RW-2026-000123" holds 12 court notices and 1 appraisal report and no other agreed type
    When the Documents tab opens through the composite route
    Then the checklist lists the six agreed types of the type table in force
    Then COURT_NOTICE shows present with 12 and APPRAISAL_REPORT shows present with 1
    Then DEMAND_LETTER, TITLE_DEED, SETTLEMENT_AGREEMENT and GUARANTOR_NOTICE show not present

  Scenario: AC4 An upload without a document type is refused and nothing is stored (new, D-RCV-60)
    Given "TEST-CO-01" picks "scan-0009.pdf" and no document type
    When "TEST-CO-01" submits the upload through the composite route
    Then the P5 response is 422 with MSG-GEN-001 naming "Document type"
    Then the composite shows the refusal and the system stores no document

  Scenario: AC5 A file that fails the malware scan is refused and quarantined (new, D-RCV-60)
    Given a test file "eicar-0001.pdf" holding the EICAR test signature
    When "TEST-CO-01" uploads it with type "COURT_NOTICE"
    Then the P5 response is 422 with MSG-P5-016
    Then the file is held in the quarantine container and no document row exists for the case

  Scenario: AC6 A repeated upload of the same file and type returns the existing document (new, D-RCV-60)
    Given "court-notice-0007.pdf" is stored on case "RW-2026-000123" as "COURT_NOTICE"
    When "TEST-CO-01" uploads the same file with the same type
    Then the response is 200 with the existing document and MSG-P5-024
    Then the case still holds one copy of that court notice and the composite shows it once

  Scenario: AC7 A double submit returns one document and one decision record (new, D-RCV-60)
    Given "TEST-CO-01" submits "appraisal-0003.pdf" with Idempotency-Key "TEST-TOKEN-0001"
    When the same request with Idempotency-Key "TEST-TOKEN-0001" arrives a second time within 1 second
    Then both responses carry the same document ID
    Then one document row and one decision record exist for it, written by the local decision-record library

  Scenario: AC8 The date filters are validated and an empty search shows the empty state (new, D-RCV-60)
    Given case "RW-2026-000123" holds no document of type "TITLE_DEED"
    When "TEST-CO-01" searches from 31 October 2026 to 1 October 2026
    Then the owning service refuses the range with MSG-GEN-003 and the composite passes the refusal through
    Then no search is run for the inverted range
    When "TEST-CO-01" searches type "TITLE_DEED" from 1 October 2026 to 31 October 2026
    Then the composite returns no item and the screen shows "No documents match this search."

  Scenario: AC9 A case outside the caller's scope is refused and shows no document name (new, D-RCV-60)
    Given user "TEST-CO-02" holds RW-CASEOWN with scope OWN and does not own case "RW-2026-000123"
    When "TEST-CO-02" opens the Documents tab of that case through the composite route
    Then the call returns 403 with MSG-P4-003
    Then the system shows no document name

  Scenario: AC10 The size limit comes from the parameter contract and holds at the exact byte (new, D-RCV-60)
    Given the P3 parameter contract publishes INTAKE_MAX_FILE_MB as 25
    When "TEST-CO-01" uploads a file of 26,214,400 bytes with type "COURT_NOTICE"
    Then the response is 201 and the document is stored
    When "TEST-CO-01" uploads a file of 26,214,401 bytes with type "COURT_NOTICE"
    Then the response is 413 with MSG-P5-017 and the system stores no document
```

**Target reading.** These ten criteria are new and belong to this story alone; the legacy AC1 to AC11 of RWB-E1-026 stay with RWB-P5-E1026-APP and are regression evidence here. The screen is proved through the gateway-bff composite route (DP-19) and the upload through the P5 contract (DP-11, DP-13); the parameters and the list values are read through the P3 contracts (DP-06, DP-07); the decision record is the local library write (DP-03); the document tables are P5's alone (DP-01). The composite path, its aggregation shape and the source behind the malware scan are not published in the Ownership Map, so the suite asserts the composite response and the scan result only (GAP-0351; ASM-0445).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A user upload carries a document type from the type table in force and source UPLOAD | RWB-E1-026 BR1; REQ-DCM-001; LOV-DOC-SOURCE |
| BR2 | Every upload is scanned for malware before it is stored | RWB-E1-026 BR2; REQ-DCM-010 |
| BR3 | The list and the search show only cases in the user's scope | RWB-E1-026 BR3; CTL-09 |
| BR4 | The date filter applies to the stored date of the document | RWB-E1-026 BR4; FSD P5 A2.5; REQ-DCM-008 |
| BR5 | The checklist lists the types of the type table in force; the required items per case type come in RWB-E1-040 | RWB-E1-026 BR5; REQ-DCM-011 |
| BR6 | A repeated upload with the same file, type and case returns the existing document | RWB-E1-026 BR6; R-UNI-40 |
| BR7 | A store that cannot be written to the decision record does not proceed | RWB-E1-026 BR7; Principle 5; R-UNI-39 |
| BR8 | P5 rwb-document owns the document, its versions, its metadata and its stored file in `rwb_document`; no other service writes a document table | DP-01; Ownership Map (document, document_type, document_checklist_item, document_custody) |
| BR9 | P3 rwb-case owns the parameter contract and the reference data that the screen reads: the size limit, the allowed types, the document types and the source list | DP-06; DP-07; Ownership Map (parameter_catalog, parameter_value, lov_value) |
| BR10 | gateway-bff composes SCR-30 in one composite route over the P5 and P3 contracts; the screen calls no service directly and the composite makes one hop per owner with a 2 s budget | DP-19; ADR-020; Architecture v5 slide 20 |
| BR11 | No cross-schema read: the suite and gateway-bff read every fact through the owner's contract, never through a table or a view of another service | DP-01; ADR-020 |
| BR12 | The size limit and the allowed file types are read from the P3 parameter contract in force, never from code; the front end size check does not replace the service check | DP-06; RWB-E1-026 section 17 |
| BR13 | The decision record of a store is written by the local decision-record library (DP-03), and a failed write stores no document | DP-03; RWB-E1-026 BR7 |
| BR14 | No personal data in the composite response, the evidence report, the fixtures or the logs: document IDs, types, dates, counts and case numbers only | RWB-E1-026 section 17; ADR-015 |

### 9. State transitions

None. This story changes no case status. The document record it creates follows the states of RWB-P5-E1026-APP, and the suite observes them through the P5 contract.

| Object | State | Meaning |
|---|---|---|
| Document record | COPY_PENDING | The row exists and the file copy is not yet confirmed |
| Document record | STORED | The file is stored and the document is returned by the list and the read |
| Document record | QUARANTINED | The scan found a threat; no document row is created and the file is held in the quarantine container |
| Checklist item | Present | The count of stored documents of that type is at least one |
| Checklist item | Not present | No stored document of that type on the case |
| Suite run | Not started, running, passed, failed with the failing test case named | The evidence report per test case |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Owns the suite module, the fixture pack, the size-boundary pair and the evidence report |
| Service owner of rwb-document | Owns the document, its versions, the metadata, the stored file, the checklist operation and the scan integration |
| Service owner of rwb-case | Owns the parameter contract, the reference data, the case read and the queue measures the composite composes |
| Platform owner of gateway-bff | Owns the composite route for SCR-30, the session in Redis and the coarse-permission check |
| Case owner (RW-CASEOWN) | Uploads, lists and searches inside the scope of the own case, as the synthetic test identity |
| Roles with Documents R (for example RW-TEAMMGR, RW-AUDIT) | List, search and open documents inside their scope; no upload |
| Partner roles PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION | No access in this story; partners reach the Workbench only through the external gateway (DL03) |
| No role | Reads a service schema directly, or takes production data into the run |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case (P3 rwb-case) | id | Read, through the P3 case contract |
| DF-DOC-001 to DF-DOC-011 | document (P5 rwb-document) | all fields | Written by P5 on the store; read through the P5 contract |
| Standard column | document (P5 rwb-document) | created_at | Read, as the stored date |
| DF-DOC-026 | document (P5 rwb-document) | content_sha256 | Read, for the duplicate case |
| DF-REF-219 | document_type (P5 rwb-document) | doc_type_code | Read through the P5 contract and the P3 reference-data contract |
| DF-REF-220 | document_type (P5 rwb-document) | label_en | Read through the P5 contract and the P3 reference-data contract |
| DF-REF-246 | document_hub_parameter (P5 rwb-document) | param_value | Read through the P3 parameter contract for the size limit (DP-06) |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry (written by the local decision-record library in P5 rwb-document; ledger P7 rwb-decision) | all fields | Written by the store through the local library; read through the P7 contract only when a run needs the ledger |
| Cross-service composition | SCR-30 composite route, its aggregation shape and the scan trigger | Route, response shape and scan trigger | Not specified in the source documents (GAP-0351; ASM-0445) |

Field IDs are those of RWB-E1-026 and are copied unchanged. The suite owns no field and no table: every row is seeded synthetically by the harness RWB-ITG-W1J01-ITG or read through an owner's contract, and no production value is used. The document tables are P5's alone, the parameter and reference-data tables are P3's, and the composite shape and the scan source are the open point named above.

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation. The names reserved for P2 rwb-integration — the base `/api/recovery/integration/v1`, the topic `rwb.integration.events.v1`, the queue `rwb-integration` and the schema `rwb_integration` — are not used, and no `rwb_integration` table is written.

#### 12.2 REST operations consumed

| Method and path | Owner | Use | Budget |
|---|---|---|---|
| `POST /api/recovery/document/v1/documents` | P5 rwb-document | Upload with type, source UPLOAD and an Idempotency-Key; the store, the duplicate answer and the size and type refusals | 2 s |
| `GET /api/recovery/document/v1/cases/{caseId}/documents` | P5 rwb-document | The case document list, the type-and-date search and the result count | 2 s |
| `GET /api/recovery/document/v1/documents/{documentId}` | P5 rwb-document | The stored document: source, doc_version, stored date and content hash | 2 s |
| `GET /api/recovery/document/v1/documents/{documentId}/content` | P5 rwb-document | The stored file of the uploaded court notice, read back for the content assertion | 2 s |
| `GET /api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case the composite composes: case number, status and scope check | 2 s |
| `GET /api/recovery/case/v1/admin/parameters` | P3 rwb-case | The parameter in force: `INTAKE_MAX_FILE_MB` = 25 and `INTAKE_ALLOWED_TYPES` (DP-06) | 2 s |
| `GET /api/recovery/case/v1/queues/{queueId}/cases` | P3 rwb-case | The queue measures of RWB-P3-E1030-APP that the case record view shows next to the tab | 2 s |
| gateway-bff composite route for SCR-30 | gateway-bff (platform edge) | The one call the screen makes: the document list, the checklist, the case and the parameters composed into the SCR-30 model (DP-19); the path and the aggregation shape are not published (GAP-0351; ASM-0445) | 2 s |

Every call is one hop to the owning service, or to gateway-bff, on its own base (DP-11, DP-13, DP-19) with the 2 s client budget; the suite calls no service through another service.

#### 12.3 Events published

None. The suite publishes no event.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| `rwb.document.DocumentStored.v1` | `rwb.document.events.v1` | P5 rwb-document | The upload is stored; the suite waits for it before it reads the top of the list and the stored document |

The envelope is CloudEvents 1.0, the key is the document ID, and the payload carries identifiers, types and dates only; the suite asserts no personal data field.

#### 12.5 Workflows and activities

| Workflow or activity | Owner | Task queue | Use |
|---|---|---|---|
| DocumentIntakeWorkflow | P5 rwb-document | `rwb-document` | The store path of the uploaded file: intake, classification and the scan step before the document row is confirmed |

The scan step inside the intake is not named in the Ownership Map, so the suite asserts the scan by its result only — the 422 with MSG-P5-016 and the quarantined file with no document row — and never by an internal path (GAP-0351; ASM-0445). The suite starts no workflow of its own.

#### 12.6 Schedules

| Job | Name | When | Owner | Use |
|---|---|---|---|---|
| JOB-12 | Document intake | Every 15 min, event plus KEDA workers | P5 rwb-document | Used only to place the synthetic documents of the case set; not the path of a user upload |

#### 12.7 Tables owned

None. The suite owns no table and never reads another service's schema (DP-01). The document tables are P5's, the parameter and reference-data tables are P3's, and every fact is read through a contract of 12.2, 12.4 or 12.5.

#### 12.8 Contract fakes

External stubs only:

| Stub | Use |
|---|---|
| EICAR test file | The file that the scan must refuse; a test signature, not a real threat |
| RWB-ITG-W1J01-ITG synthetic case set | Case RW-2026-000123 with 50 documents, 12 court notices, 4 in October 2026, 1 appraisal report and the six agreed types |
| Blob container (Azurite in the lower environment) | The intake path, the stored file and the quarantine path |
| Mock Entra sign-in | Synthetic test identities for the case owner, the reader and the out-of-scope user |

No service contract is faked: every P5 and P3 call and the gateway-bff composite go to the real deployment in SIT.

#### 12.9 Call-type summary

| Call type | Provided by the suite | Consumed by the suite |
|---|---|---|
| REST | 0 | 8: seven to P5 and P3 and one to the SCR-30 composite route |
| Kafka | 0 | 1 event type: `rwb.document.DocumentStored.v1` |
| Temporal | 0 | 1 workflow: DocumentIntakeWorkflow on `rwb-document`; 1 job start: JOB-12 |
| File | 0 | 2: the intake container and the quarantine container |

### 13. Solution plan

**Deliverables.** One suite module that reuses the harness RWB-ITG-W1J01-ITG: a fixture pack for the 50-document case and the six types, a composite probe for SCR-30, a document probe for the P5 upload and search, a parameter probe for the size limit, a scan probe that asserts the result only, and an evidence report with one verdict per test case. No service code and no schema change.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| SuiteRunner | Test harness | Preflight against the published contracts and the composite route, run order, report and exit code |
| FixtureDriver | Test harness | Seeds the W1J01 case set, the 50-document case and the six types through the P5 and P3 published paths |
| CompositeProbe | Test harness | Calls the SCR-30 composite route and asserts the list, the checklist, the case and the parameter parts against the owners' answers |
| DocumentProbe | Test harness | Uploads, lists, searches and reads the document through the P5 contract, including the duplicate, the inverted range and the empty state |
| ParameterProbe | Test harness | Reads `INTAKE_MAX_FILE_MB` and `INTAKE_ALLOWED_TYPES` through the P3 parameter contract and drives the 26,214,400 and 26,214,401 byte uploads |
| ScanProbe | Test harness | Uploads the EICAR file and asserts the 422, MSG-P5-016, the quarantined object and the absence of a document row, without an internal path |
| EventProbe | Test harness | Consumes `rwb.document.DocumentStored.v1` and asserts the envelope, the key and the absence of a personal data field |
| ReportWriter | Test harness | One row per test case with the evidence and the elapsed time, and the cleanup record |

**Database.** None of its own. The suite writes no service table and no schema object (DP-01).

**Configuration and reference data**

- The SIT endpoints of P5 and P3, the composite route of gateway-bff, the topic name, the queue name and the namespace `rwb-recovery`, all as configuration.
- The synthetic case number RW-2026-000123, the user identities, the 50-document case, the 2 MB court notice and the two size-boundary files.
- The size limit and the allowed types, read through the P3 parameter contract and never written in the suite code (DP-06, AC10).
- The six agreed types and the source list, read through the P3 reference-data contract (DP-07).
- The 2 s client budget, the 5 second list expectation and the poll interval of the run.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added | Where it sits |
|---|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none | The document tables stay in `rwb_document` (P5) and the suite asserts through the P5 contract; no suite step opens a schema |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON | The store writes its record through the local library; AC7 asserts one record for the double submit |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON | The size limit and the allowed types are read through `GET /api/recovery/case/v1/admin/parameters`; AC10 |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | The six document types and the source list are read through the P3 reference-data contract; AC3 |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | The one call the screen makes; every screen assertion of section 15 goes through the SCR-30 composite route |

The dependency-added column records the build dependency of the owning story. This story has no build dependency: an ITG story waits on no build of its own. It carries no H, C or X dependency, and its I dependencies are the three APP stories RWB-P3-E1045-APP, RWB-P3-E1030-APP and RWB-P5-E1026-APP listed in the metadata table.

**Fixtures**

| Fixture | Content | Used by |
|---|---|---|
| Document case set | Case RW-2026-000123 with 50 documents, 12 `COURT_NOTICE` of which 4 stored in October 2026, 1 `APPRAISAL_REPORT` and the other four types absent | AC2, AC3, AC8 |
| Upload file | `court-notice-0007.pdf` of 2 MB with type `COURT_NOTICE` and source `UPLOAD` | AC1, AC6 |
| Scan file | `eicar-0001.pdf` holding the EICAR test signature | AC5 |
| Size pair | A file of 26,214,400 bytes and a file of 26,214,401 bytes | AC10 |
| Idempotency pair | Two submissions of `appraisal-0003.pdf` with the same Idempotency-Key | AC7 |

**Build steps**

1. Create the suite module next to harness RWB-ITG-W1J01-ITG and wire it to the SIT endpoints of P5 and P3, the composite route, the topic and the queue, with the contract preflight that fails on any drift (X11, X12).
2. Build FixtureDriver and the document case set, and assert that the composite list matches the P5 list for the same case.
3. Build CompositeProbe for the list, the checklist, the case and the parameter parts of the SCR-30 answer, and assert that the composite adds no document that P5 does not publish.
4. Build DocumentProbe for the upload, the 5 second top-of-list expectation, the type-and-date search, the duplicate, the inverted range and the empty state.
5. Build ParameterProbe and the size-boundary pair, reading the limit through the P3 parameter contract and never from code.
6. Build ScanProbe for the EICAR file and assert the 422, MSG-P5-016, the quarantined object and the absence of a document row, with no internal scan path.
7. Build EventProbe and ReportWriter, including the cleanup of the synthetic documents and the quarantined file.
8. Run the suite twice in SIT against the wave 1 release candidate so that a repeated run adds no document and no decision record.

**Done when.** The thirteen test cases of section 16 pass in SIT against the published wave 1 contracts and the SCR-30 composite route, the ten criteria of section 7 are signed off, a 2 MB upload shows at the top of the composite list within 5 seconds, no service table was read, the synthetic set is cleaned up, and the evidence report names every criterion with its observable.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | Upload with no document type | Enter {field}. |
| MSG-GEN-003 | Date from after date to | {field} cannot be before {other}. |
| MSG-P5-001 | File type not allowed | This file type cannot be stored. Use PDF, JPG or PNG. |
| MSG-P5-016 | Malware found | This file was not stored because the malware scan found a threat. It is held in quarantine. |
| MSG-P5-017 | File above the size limit | This file is larger than {size} MB and cannot be stored. |
| MSG-P5-024 | Same file already on the case | This file is already on the case as {document}. |
| MSG-P5-006 | Type not in the table | {value} is not a document type in force. Choose a type from the list. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the scope | This case is not in your scope. |
| MSG-P7-003 | Decision record write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message IDs and wording are copied unchanged from RWB-E1-026 and this story adds no message ID. Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-30 Case documents, reached from SCR-03 Case record, served by the gateway-bff composite route (DP-19). The suite asserts each state through the composite and the same facts through the P5 and P3 contracts.

| State | What the user sees and does | What the suite asserts |
|---|---|---|
| Loading | Skeleton rows while the list and the checklist load | The composite returns one answer carrying the list, the checklist, the case and the parameters; no partial answer is asserted |
| list | Documents with type, stored date, source, version and the write-once label; the search bar with type and date range; the checklist with the six types | The composite list matches the P5 list and the P5 read of the document; the checklist counts match the P5 counts; the date range narrows to the 4 October court notices |
| upload | The upload dialog with the file, the document type and the size limit; errors from section 14 next to the field | The P5 upload response, the duplicate answer, the size refusal and the empty-type refusal, and the composite showing the same message |
| Empty | "No documents match this search." with the action "Clear the search" (common state) | The composite returns no item and the sentence is shown for a type with no document |
| Error | The message from section 14 at the top | The 403, the 415, the 422 and the 413 of sections 5 and 14 carried through the composite unchanged |

The Upload action shows only to roles with Documents C. A missing composite route is a deployment fault and is never replaced by a direct service call in the suite (X12).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-026-12-ITG | Access refusal at the composite; the legacy access case, owned by RWB-P5-E1026-APP, adds no new AC here | Integration | Team manager (RW-TEAMMGR, Documents R only) uploads through the composite; refused with MSG-P4-002 and the Upload action is not shown; end-to-end: real services on the wave 1 contracts |
| TC-E1-026-13-ITG | AC7 (one decision record) and Principle 5; regression of RWB-P5-E1026-APP AC1 | NFR | Decision record write forced to fail during an upload; nothing stored, MSG-P7-003; end-to-end: real services on the wave 1 contracts |
| TC-E1-026-01-ITG | AC1, BR1 | Integration | Synthetic 2 MB court notice PDF `court-notice-0007.pdf`, type COURT_NOTICE, source UPLOAD; end-to-end: real services on the wave 1 contracts |
| TC-E1-026-02-ITG | AC2, BR4 | Integration | Case RW-2026-000123 with 50 synthetic documents, 12 court notices, 4 in October 2026; end-to-end: real services on the wave 1 contracts |
| TC-E1-026-03-ITG | AC3, BR5 | Integration | Case with 12 court notices and 1 appraisal report and the other four types absent; end-to-end: real services on the wave 1 contracts |
| TC-E1-026-04-ITG | AC4, BR1 | Integration | Upload of `scan-0009.pdf` without a type; end-to-end: real services on the wave 1 contracts |
| TC-E1-026-05-ITG | AC5, BR2 | Integration | EICAR test file `eicar-0001.pdf`; end-to-end: real services on the wave 1 contracts |
| TC-E1-026-06-ITG | Regression of RWB-P5-E1026-APP AC6; no new AC in this story | Integration | Spreadsheet file `minutes-0002.xlsx` uploaded as SETTLEMENT_AGREEMENT, refused with MSG-P5-001; end-to-end: real services on the wave 1 contracts |
| TC-E1-026-07-ITG | AC6, BR6 | Integration | Same PDF `court-notice-0007.pdf` uploaded twice with the same type; end-to-end: real services on the wave 1 contracts |
| TC-E1-026-08-ITG | AC7, BR6 | Integration | Two requests with Idempotency-Key TEST-TOKEN-0001 within 1 second; end-to-end: real services on the wave 1 contracts |
| TC-E1-026-09-ITG | AC8 | Integration | Date range 31 October 2026 to 1 October 2026, refused with MSG-GEN-003; end-to-end: real services on the wave 1 contracts |
| TC-E1-026-10-ITG | AC8 | Integration | Search for TITLE_DEED on a case without one, empty state shown; end-to-end: real services on the wave 1 contracts |
| TC-E1-026-11-ITG | AC9, BR3 | Integration | Case owner with scope OWN opening another owner's case through the composite, refused with MSG-P4-003; end-to-end: real services on the wave 1 contracts |

The thirteen rows are the legacy test cases of RWB-E1-026 in their legacy order, each copied with the `-ITG` suffix. The Level column follows Template and Rules §R7.2: the legacy System level becomes Integration, the legacy Access level becomes Integration and the legacy Resilience level becomes NFR. TC-E1-026-01-ITG to TC-E1-026-05-ITG, TC-E1-026-07-ITG to TC-E1-026-11-ITG, TC-E1-026-12-ITG and TC-E1-026-13-ITG are run here on the real services; the criteria they also cover at component level stay with RWB-P5-E1026-APP.

### 17. Guardrails

- Synthetic data only: the harness RWB-ITG-W1J01-ITG loads every case number, user identity, document and file, and no production data is read, copied or connected to.
- No personal data in the composite response, the events, the logs, the evidence report or the fixtures: document IDs, types, dates, counts and case numbers only.
- No cross-service table read: every fact is read through a contract, and the suite ships with no client for a service schema (DP-01).
- No business value in test code: the size limit, the allowed types, the six document types and the source list are the parameter and the reference data in force, read through the P3 contracts (DP-06, DP-07).
- The front end size check does not replace the service check, and the suite asserts both answers on the same upload.
- The scan is asserted by its result only; no internal scan path is assumed (GAP-0351).
- One hop and a 2 s budget on every call, with no service called through another service (ADR-020).
- No production access and no production namespace: the run is pinned to SIT and refuses to start against any other environment.
- Clean-up in the same run: the synthetic documents, the quarantined file and the fixture rows are removed in a controlled order, and the report records what was cleaned.

### 18. Traceability

| Requirement or decision | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DCM-008 | Documents searchable by case ID, type and date from the case record view | `GET /api/recovery/document/v1/cases/{caseId}/documents` with type, dateFrom and dateTo; the SCR-30 composite; MSG-GEN-003 | TC-E1-026-02-ITG, TC-E1-026-03-ITG, TC-E1-026-09-ITG, TC-E1-026-10-ITG, TC-E1-026-11-ITG |
| REQ-DCM-001 | Every document stored against its case with type, date and source | `POST /api/recovery/document/v1/documents`, `GET /api/recovery/document/v1/documents/{documentId}`, `rwb.document.DocumentStored.v1` | TC-E1-026-01-ITG, TC-E1-026-04-ITG, TC-E1-026-06-ITG to TC-E1-026-08-ITG, TC-E1-026-12-ITG, TC-E1-026-13-ITG |
| REQ-DCM-010 | Every upload scanned for malware before it is stored | The scan result on the store path: 422 with MSG-P5-016 and the quarantined file | TC-E1-026-05-ITG |
| REQ-DCM-011 | Checklist of the agreed document types on the case | The checklist part of the SCR-30 composite over the P5 checklist operation and the P3 reference-data contract | TC-E1-026-03-ITG |
| DP-01 | Owner's schema, never another service's tables | `rwb_document` is P5's alone; every assertion goes through a contract | All |
| DP-03 | Local decision-record library and the shared topic | The decision record of a store; one record for a double submit (AC7) | TC-E1-026-08-ITG, TC-E1-026-13-ITG |
| DP-06 | Parameters contract of rwb-case | `GET /api/recovery/case/v1/admin/parameters`: `INTAKE_MAX_FILE_MB` = 25, `INTAKE_ALLOWED_TYPES` | TC-E1-026-01-ITG, TC-E1-026-04-ITG |
| DP-07 | Reference data contract of rwb-case | The six document types and the source list read through the P3 contract | TC-E1-026-03-ITG |
| DP-19 | gateway-bff composite route | The SCR-30 composite route of section 12.2 | TC-E1-026-01-ITG to TC-E1-026-05-ITG, TC-E1-026-07-ITG, TC-E1-026-10-ITG, TC-E1-026-11-ITG |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The eight calls of section 12.2 and the preflight contract test | All, at the preflight |
| ADR-021 | Per-service Flyway and migration ownership | The suite owns no schema and no migration; P5 owns the document tables and P3 the parameter tables | All, at the preflight |
| RWB-E1-026 (legacy story) | Attach and search screen: the ten new criteria of this story | The eight calls, the one event, the intake workflow and the SCR-30 composite of section 12 | All thirteen copies of section 16 |
| RWB-P5-E1026-APP (component copy) | The document hub behaviour of the legacy key, owning legacy AC1 to AC11 | The P5 upload, list, read, content and checklist operations | The regression copies of section 16 |

The legacy AC1 to AC11 of RWB-E1-026 stay with RWB-P5-E1026-APP; this story owns no legacy criterion (`acs` is empty for the legacy key). The integration dependencies are RWB-P3-E1045-APP, RWB-P3-E1030-APP and RWB-P5-E1026-APP, and their component-level criteria are owned by those stories.

### 19. Out of scope

- The P5 and P3 application builds this run depends on: RWB-P5-E1026-APP, RWB-P3-E1045-APP and RWB-P3-E1030-APP.
- The legacy AC1 to AC11 at component level, which RWB-P5-E1026-APP owns.
- The contract, database, operations and infrastructure stories of the legacy key.
- Required items per case type and the completeness flag (RWB-E1-040).
- Search across cases and free text search (RWB-E1-033) and search on extracted fields within a case.
- OCR, classification and extraction of an uploaded file (RWB-E1-049, RWB-E1-050, RWB-E1-053).
- Upload from the field app (RWB-E2-024) and from partners (Epic 5, DL03).
- The build of the harness RWB-ITG-W1J01-ITG.
- The non-functional epic RWB-ITG-NFR, including load, resilience and performance testing.
