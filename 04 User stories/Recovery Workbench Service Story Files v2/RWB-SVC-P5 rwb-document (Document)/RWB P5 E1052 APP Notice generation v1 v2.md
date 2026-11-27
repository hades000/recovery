# RWB-P5-E1052-APP Notice generation v3

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1052-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-052 |
| Legacy disposition | Split (rework) |
| Source version | 1 |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP05, DP07, DP09, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P5-O |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P5-E1052-APP-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-P6-E1052-CON, version Not specified in the source documents (DOR-RWB-P5-E1052-APP-23); the path is /api/recovery/document/v1 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (no FR mapped to REQ-OCC-001) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the secondary P5 slice of RWB-E1-052. A notice produced by `rwb-comms` becomes a write-once generated document on the case in schema `rwb_document`, through `/api/recovery/document/v1` and against the contract `RWB-P6-E1052-CON`. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P5-E1052-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 32 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **every demand, recall and guarantor notice that `rwb-comms` produces for a case to be stored by `rwb-document` as one write-once generated document on that case, with its document type and retention class taken from the type in force, its template version identifier and its merge values carried as document facts, and its SHA-256 recorded**, so that **the letter that was issued is the letter that is kept, unchanged, and every reader can name its type, its template version and the values it carried**.

- Service `rwb-document`, schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1`, Temporal task queue `rwb-document` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.document`.
- **This is the secondary P5 slice of RWB-E1-052 and it owns no legacy acceptance criterion.** Legacy AC1 to AC9 and the eleven legacy test cases stay with `rwb-comms` in RWB-P6-E1052-APP and RWB-P6-E1052-CON; the end-to-end journey of legacy AC7 is RWB-ITG-E1052-ITG's. The nine criteria of section 7 are new under D-RCV-60 and test only the document side.
- **What stays with `rwb-comms`:** the template approval check, the merge value resolution, the two hold paths (MSG-P6-005, MSG-P6-003, MSG-P6-007), the rendering of the template body and the footer (case number, template code, template version, generation date), the `notice` row with its state and sent type, the D7.1 decision record, `rwb.comms.NoticeGenerated.v1`, the WIN dispatch and the proof of delivery read.
- **What this story owns:** the notice path of `POST /api/recovery/document/v1/cases/{caseId}/generated-documents` (API-P5-016) — the notice type to document type mapping, the retention class and the write-once flag from the type row in force, the file receipt and its SHA-256, the `document` row with `source` `GENERATED`, the `document_field` rows, the `DocumentStored` outbox row, the idempotent repeat, the correction by a new version, and the answer `rwb-comms` needs to name the notice.
- **What other stories of the service own:** the store path, the containers and the upload path are RWB-P5-E1024-APP's; the document type table is RWB-P5-E1025-APP's; the catalog binding that stamps `template_id` and writes the merge values as catalog-checked fields is RWB-P5-E1046-APP's; the generation engine for contract, CA and mortgage templates is RWB-P5-E2026-APP's. This story calls those and re-tests none of them.
- **No ACE read** (DP-05 as a prohibition): the customer name, the notice address, the phone and the outstanding are inside the PDF that `rwb-comms` renders; they reach the notice through `rwb-source-data`, the only reader of the `recovery.v_ace_*` views. This service opens no `v_ace_*` view, holds no grant on `public` and stores no party, contact or account copy.
- **DP-03 is a boundary, not a writer.** The D7.1 record is `rwb-comms`' and the `DOCATT` record of a store is the store path's (RWB-P5-E1024-APP); this path writes no decision record of its own and `rwb_document` holds no decision table. This path adds no case-side record and no code of its own. The final call and the outcome value of that record are Not specified in the source documents (GAP-0750).
- The call is inbound and synchronous: one hop from `rwb-comms`, 2 s budget, `Idempotency-Key` (DP-11). The database login is one per service (DP-02); its name is Not specified in the source documents (GAP-2348; ASM-3903), so the story says "the rwb-document login".

### 2. Business rationale

Legacy RWB-E1-052 ends with a letter on the case. The rule behind step 8 is CTL-14 and NFR-029 — a legal document that cannot be altered or deleted inside its retention period — and DT06, the document hub as the system of record for documents. If the notice were only a `rwb-comms` fact with a file reference, nothing would guard the file, name its type or show which wording and which values were sent, and the dispatch and its proof of delivery would rest on a document that can move under them.

The realignment changes the mechanics, not the rule:

1. **One schema, one base.** `rwb_document` replaces the recovery schema and `/api/recovery/document/v1` replaces the monolith base (DP01, DP13). No `recovery.*` table is named by a statement of this service, and the `notice` table remains `rwb_comms`'.
2. **The type decides the holding, not the code.** A generated notice is write-once and carries a retention class because its document type says so in the type table in force (NFR-028, NFR-029); a type code, a class, a flag and a container name are never constants.
3. **The notice type is data too.** Which document type a `DEMAND`, `RECALL` or `GUARANTOR_NOTICE` produces is a row, so Legal can add a notice type without a release (DL28).
4. **A repeat is answered, not re-stored.** The `Idempotency-Key` and the notice key answer the second request with the first document, so the legacy "one notice per case, notice type, person and business date" (R-UNI-40) holds on the document side as well.
5. **A correction is a new version.** The generated PDF is never overwritten; a correction writes `doc_version` n+1 with `previous_version_id` and a reason, and the earlier version keeps its bytes and its stamp.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P6-E1052-CON, published | The caller's shape of the generation request and answer: case, notice type, `person_key`, language, business date, template code and version, merge values, the claim-check file reference, the two event envelopes, the message IDs and the error envelope (DP11, C) |
| RWB-P6-E1052-APP | The caller itself: it renders the PDF, adds the footer and posts the request after its own template check and value resolution. Built against the fake of 12.8 |
| RWB-P5-E1024-APP, store path | The document identity, the container write, the `COPY_PENDING` → `STORED` step, the `DOCATT` record and the copy retry |
| RWB-P5-E1025-APP, type table | `document_type` in the version in force from 30 November 2026 with its retention class and write-once flag |
| RWB-P5-E1046-APP, binding step | `template_id` set to the catalog version identifier and one `document_field` row per merge code of that version |
| Reference-data contract (DP07) | LOV-DOC-TYPE, LOV-DOC-SOURCE, LOV-RETENTION in force, so no list value is typed in code |
| Outbox library (DP09) | `rwb.document.DocumentStored.v1` written in the same transaction as the row |
| Per-service Flyway sequence (DP15) and gateway-bff route (DP19) | The one migration step in `rwb_document`, and the documents tab of the case |

The platform contracts behind DP-03, DP-07, DP-09, DP-15 and DP-19 are the service template's baseline, and the generation contract RWB-P5-E2026-CON and the rwb-case reference-data contract are consumed against their fakes; none of them is in the rows this Work Package fixes. Both facts are recorded rather than edited into the rows (GAP-2350; ASM-3905). The platform contract stories behind those patterns are RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON; they are held here and in the pattern table, not in the metadata rows (GAP-0754).

Business preconditions carried from RWB-E1-052, unchanged in value: template "DEMAND-MTG" "TH" version 2 is Approved and current with id "TPL-0002"; case "RW-2026-000123" is in product group "MORTGAGE" with borrower `person_key` "P-0001"; the rendered PDF of the notice is in the claim-check file store; the business date is 2026-11-25; the release date 30 November 2026 is tentative and is not a condition.

### 4. Flow

1. `rwb-comms` posts `POST /api/recovery/document/v1/cases/{caseId}/generated-documents` with the notice type, the template code and the catalog version identifier, the language, the business date, the merge code and value list, the rendered PDF as a claim-check file reference, and an `Idempotency-Key`. One hop, 2 s budget (DP11).
2. `GeneratedDocumentController`: validates the case ID, the file type (PDF) and the size, resolves the document type of the notice type from the mapping row in force, and refuses an unmapped notice type with 422 and MSG-P5-006 naming it.
3. `GenerationIdempotencyGuard`: answers a key already answered from the stored answer (document ID, `doc_version`, `source`, `write_once`); no second row, no second object and no second event.
4. `NoticeDocumentTypeResolver`: reads the `document_type` row in force and takes its `retention_class` and `write_once` flag; a notice is write-once because its type is, never because a constant says so.
5. `TemplateBindingClient`: the binding step of RWB-P5-E1046-APP stamps `template_id` with the version identifier the caller supplies from the catalog answer and writes one `document_field` row per merge code. A refused version, a code outside the catalog or a missing required value writes nothing and returns that story's message unchanged.
6. Store path: the document identity is created and the row is written with `case_id`, `document_type`, `source` `GENERATED`, `doc_version` 1, `template_id`, state `COPY_PENDING`.
7. `StorageWriter`: writes the file to the write-once legal container at `{container}/{caseId}/{documentId}/v1`, computes `content_sha256`, and sets the row `STORED`. A refused container leaves the row `COPY_PENDING`, answers 503 with MSG-GEN-006 naming "Document storage", and writes no outbox row; the copy retry stores it once.
8. `DocumentStoredPublisher`: writes the `rwb.document.DocumentStored.v1` outbox row in the same transaction as the `STORED` state, with the document ID, the case ID, the type and the source, and no field value (DP09).
9. Answer 201 with the document ID, `source` `GENERATED`, `write_once` true, `doc_version` 1 and the template version, which is what `rwb-comms` needs to write its `notice` row.
10. A correction posts `POST /documents/{documentId}/regenerate` (API-P5-017) with a reason: a new `doc_version` with `previous_version_id`, never a replace of version 1.
11. Reads: `GET /documents/{documentId}` and `/content` on the case documents tab through the gateway-bff route (DP19); the content returned hashes to the `content_sha256` of the row, and the read changes nothing.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The notice type has no mapping row in force | Refused with 422; no row, no file and no event | MSG-P5-006 | AC2 |
| X2 | The binding refuses the version, a merge code or a required value | Refused whole by the binding; nothing stored; the binding's message returned unchanged | MSG-P6-005, MSG-P6-006, MSG-GEN-001 | AC2 (the refusal itself is RWB-P5-E1046-APP's) |
| X3 | The same request arrives twice with the same `Idempotency-Key` | The first answer is replayed; one document, one object, one event | None | AC3 |
| X4 | The container refuses the write | Row `COPY_PENDING`; 503; no outbox row; the retry stores it once | MSG-GEN-006 ("Document storage") | AC4 |
| X5 | A replace or a delete is attempted on a stored notice version | Refused; the row and the file are unchanged; an audit event is written | MSG-P5-002 | AC5 |
| X6 | A statement names `rwb_comms`, `notice` or another schema, or the schema holds a cross-schema key | The build fails and names the statement or the constraint; at the database the statement fails with SQLSTATE 42501 | None (build log) | AC6, AC9 |
| X7 | A role without Documents C posts a generation, or without Documents U corrects one | Refused with 403 before any row is read | MSG-P4-002 | AC10 |
| X8 | A personal value reaches a log line, an event payload, a storage path or a test | The guard test fails the build; the value is replaced by the field name in a trace | None (build log) | AC7 |

Two target notes: the hold paths (a missing ADDRESS row, a withdrawn template) are `rwb-comms`' and never reach this operation — a request for a held notice is not posted, and one that is posted stores nothing. The message texts are the caller's and the store's, unchanged.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the `rwb_document` baseline, the type table, the store path, the binding step and the fake of RWB-P6-E1052-CON; it needs no P6 build and no ACE view |
| Negotiable | The notice type mapping, the type codes, the retention classes, the container name and the flag are data or placeholders; the repeat rule, the write-once rule and the version rule are fixed |
| Valuable | The notice that was issued is the document that is kept, write-once, with its type, its template version and its hash |
| Estimable | One operation path, one resolver, one guard, one storage write and one outbox row |
| Small | Under one week with its tests and its fake (size: Not specified in the source documents (DOR-RWB-P5-E1052-APP-16)) |
| Testable | Each criterion of section 7 is one test case of section 16, on the fixtures of 12.8 |

### 7. Acceptance criteria

```gherkin
Feature: Notice generation v1 in rwb-document

  Background:
    Given template "DEMAND-MTG" "TH" version 2 is Approved and current with id "TPL-0002" and merge codes "CASE_NO", "CUSTOMER_NAME", "POSTAL_ADDRESS" and "TOTAL_OUTSTANDING"
    Given case "RW-2026-000123" has product group "MORTGAGE" and borrower person_key "P-0001"
    Given the type mapping of notice type "DEMAND" is document type "DEMAND_LETTER" (a data row; Not specified in the source documents (GAP-2347; ASM-3902))
    Given document type table version "DOCTYPE-2026.11" is in force from 30 November 2026 and its "DEMAND_LETTER" row holds the retention class and the write-once flag of the type (both Not specified in the source documents (GAP-2347; ASM-3902))
    Given the business date is 2026-11-25

  Scenario: AC1 Stored as a generated write-once document (new, D-RCV-60)
    Given the rwb-comms contract mock posts a generation request for case "RW-2026-000123", notice type "DEMAND", template "DEMAND-MTG" version 2 with id "TPL-0002", the merge values "CASE_NO" "RW-2026-000123", "CUSTOMER_NAME", "POSTAL_ADDRESS" and "TOTAL_OUTSTANDING" 1,250,000.00, and the rendered PDF as a claim-check file reference, with Idempotency-Key "K-0001"
    When the request is served
    Then one document row exists with case_id of "RW-2026-000123", document_type "DEMAND_LETTER", source "GENERATED", write_once true, doc_version 1, template_id "TPL-0002" and state "STORED"
    Then content_sha256 equals the SHA-256 of the stored file and the file sits at "{container}/RW-2026-000123/{documentId}/v1"
    Then four document_field rows exist, one per merge code
    Then one rwb.document.DocumentStored.v1 row is in the outbox with the document ID, the case ID, the type and the source

  Scenario: AC2 The type and its holding are data, not code (new, D-RCV-60)
    Given the "DEMAND_LETTER" row in force holds the retention class and the write-once flag of the type
    When a "DEMAND" notice is stored
    Then the document row carries the retention_class and the write_once value read from that row
    Then the build names no type code, no retention class, no container name and no flag in Java source
    When a request for notice type "STATEMENT" is posted and no mapping row exists for it
    Then the answer is 422 with MSG-P5-006 naming "STATEMENT"
    Then no document row, no file and no outbox row is written

  Scenario: AC3 The same request twice stores one document (new, D-RCV-60)
    Given a notice for case "RW-2026-000123", notice type "DEMAND" and person_key "P-0001" was stored on 2026-11-25 with Idempotency-Key "K-0001"
    When the same request is posted again on 2026-11-25 with "K-0001"
    Then the first answer is replayed with the same documentId and doc_version 1
    Then the case still holds one "DEMAND_LETTER" generated document for 2026-11-25, one object in the container and one DocumentStored row

  Scenario: AC4 A refused copy leaves one pending row and one store (new, D-RCV-60)
    Given the storage container refuses the write of the notice file
    When the request of AC1 is served
    Then the document row is committed with state "COPY_PENDING"
    Then the answer is 503 with MSG-GEN-006 naming "Document storage"
    Then no DocumentStored row is written for the document
    When the container accepts the file and the copy runs again
    Then the row becomes "STORED" with content_sha256 equal to the file's and one DocumentStored row exists
    Then the case holds one document for the request and no second document is created

  Scenario: AC5 A correction is a new version, never an overwrite (new, D-RCV-60)
    Given the "DEMAND_LETTER" document of AC1 with doc_version 1 and content_sha256 "H1"
    When a content replace and a delete are attempted on that version through the document store and directly on the container
    Then each attempt is refused with MSG-P5-002 and the row and the file are unchanged
    When a correction is posted with a reason
    Then doc_version 2 is written with previous_version_id set to the document ID of version 1
    Then version 1 still holds content_sha256 "H1" and template_id "TPL-0002"

  Scenario: AC6 No notice fact is written here (new, D-RCV-60)
    Given the request of AC1
    When the document is stored
    Then rwb_document holds no notice row, no hold reason, no sent type and no delivery fact
    Then the boundary test fails a statement that names notice or rwb_comms, and a schema key that leaves rwb_document
    Then the notice state, the sent type and the delivery facts are read from the rwb-comms contract only

  Scenario: AC7 No personal data leaves the document (new, D-RCV-60)
    Given the request of AC1 carries the customer name "Anan Sukjai" and the address "88/1 Bangkok" inside the PDF only
    When the document is stored and its event is published
    Then no name, address, amount or person_key appears in the document row, the event payload, the storage path, a log line or a test fixture
    Then the merge values are held as document_field values, masked by role on read
    Then the decision record reference of the caller names the field IDs and never a value

  Scenario: AC8 One hop inside the budget on the published shape (new, D-RCV-60)
    Given the rwb-comms contract mock posts the request of AC1 in the published shape of RWB-P6-E1052-CON
    When the store answers inside the 2 s budget
    Then the answer is 201 with the document ID, source "GENERATED", write_once true, doc_version 1 and template version 2
    Then a request that carries a field outside the published shape is refused by the contract test with 422 and nothing is stored
    Then a request that passes 2 s is answered 503 and stores nothing

  Scenario: AC9 No ACE read and no cross-schema key (new, D-RCV-60)
    Given the build of the module, the grants of the rwb-document login and the schema rwb_document
    When the statements, the grants and the schema are inspected
    Then no statement names an ACE view, public or another service's schema
    Then the login holds no SELECT on any ACE view and rwb_document holds no key into another schema
    Then template_id and the notice reference are values, not foreign keys

  Scenario: AC10 A role without the right is refused before any row is read (new, D-RCV-60)
    Given a service identity without Documents C and a service identity without Documents U
    When the first posts a generation and the second posts a correction on a stored notice
    Then each answer is 403 with MSG-P4-002
    Then no document row is read and no row, file or outbox row is written

  Scenario: AC11 An error answer carries its status code on the provided operations (new, D-RCV-60)
    Given a generation request posted without a service identity, and a correction posted on a document ID that is not on the case
    When each request is served
    Then the first is answered 401 and nothing is stored; the message is Not specified in the source documents (NEWAC-RWB-P5-E1052-APP-AC11)
    Then the second is answered 404 and no row, file or outbox row is written
    Then a service identity without the right is answered 403 with MSG-P4-002, as in AC10
```

The eleven criteria are new under D-RCV-60 and test the document side only. Legacy AC1 to AC9 of RWB-E1-052 stay with RWB-P6-E1052-APP and the composed proof is RWB-ITG-E1052-ITG. No legacy criterion text is copied into this file.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A notice document is stored with `source` `GENERATED` and `write_once` true, and both the flag and its retention class come from the document type row in force | RWB-E1-052 BR5; CTL-12; DT06; NFR-028, NFR-029 |
| BR2 | One document per case, notice type, `person_key` and business date: the `Idempotency-Key` answers a repeat with the first document | RWB-E1-052 BR8; R-UNI-40 |
| BR3 | The generated PDF is never overwritten; a correction writes a new `doc_version` with `previous_version_id` and a reason, and the earlier version keeps its bytes and its stamp | RWB-E1-052 section 17; CTL-12 |
| BR4 | Which document type a notice type produces is a data row, and no type code, class, flag or container name is a Java constant | RWB-E1-052 section 17; DL28 |
| BR5 | The name, the address and the amounts reach the PDF and its masked field rows only: never the document row, the event, the storage path, the decision record or a log | NFR-040; PDPA; RWB-E1-052 section 17 |
| BR6 | The template version identifier and the merge values are the binding step's, written on the document by RWB-P5-E1046-APP; this path never checks the catalog itself | RWB-E1-052 BR1, BR10; DP-11 |
| BR7 | The row, the file and the event agree: a `COPY_PENDING` document publishes no `DocumentStored` until its file is stored, and a retried copy creates no second document | R-UNI-24; FSD P5 AC-EXC-P5-001-03 |
| BR8 | `rwb-document` writes no notice fact: the state, the hold reason, the sent type, the delivery facts and the D7.1 record are `rwb-comms`' | RWB-E1-052 flow step 9, BR11; DP-01; D-RCV-35 |

Where each rule lives in the target: BR1 is a read of `document_type` plus the row columns `retention_class` and `write_once`; BR2 is the platform idempotency row keyed by the notice key; BR3 is the version chain of `document`; BR4 is the mapping and type tables; BR5 is a masking call and a guard test; BR6 is a call into the binding step; BR7 is the state change that gates the outbox row; BR8 is the absence of any `rwb_comms` statement. No business value is a constant in Java.

### 9. State transitions

None for the case. This story moves the document state only, on the standard record columns of TSD P5 T3.0.

| From | Event | Condition | To |
|---|---|---|---|
| None | Generation request (API-P5-016) | The type mapping resolves, the binding accepts the version and the values | A `document` row, `source` `GENERATED`, `doc_version` 1, `COPY_PENDING` |
| `COPY_PENDING` | The file is written and hashed | The container accepts the write | `STORED`, and the `DocumentStored` row is written |
| `COPY_PENDING` | The container refuses the write | The write fails | Stays `COPY_PENDING`; 503; the copy retry runs |
| `STORED` | A correction with a reason (API-P5-017) | The caller holds Documents U | A new `doc_version` with `previous_version_id`; the earlier row is unchanged |
| `STORED` | A replace or a delete on the same version | Any caller | Refused with MSG-P5-002; nothing moves |

The notice state (Generated, Held, Sent, Delivered) is `rwb-comms`' and is not a transition of any `rwb_document` row.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Opens the notice document on the case documents tab (Documents R) |
| RW-LEGAL, legal counsel | Reads the document and its merge values unmasked (Documents CRUA) |
| RW-COE, centre of excellence analyst | Reads the generated notice and its hash (Documents R) |
| SY-CASEWF, case workflow module | Reads the document reference the notice carries (Documents R) |
| `rwb-comms` service identity | Posts the generation request and the correction with an `Idempotency-Key` (Documents C and U) |
| The rwb-document service identity (the rwb-document login, DP-02) | Writes `document` and `document_field`, writes the file and the outbox row, and refuses a change to a stored notice |
| The decision-record library identity | Writes the store's `DOCATT` record as RWB-P5-E1024-APP invokes it; this story writes no record and no new decision code |

Every "who" is a role code; the rights are the legacy ones and are enforced by the guard library the service template carries, with the decision held in `rwb-access`. Each REST operation of API-P5-016 is checked against this table by the authorise check in `rwb-access`; its name is Not specified in the source documents (DOR-RWB-P5-E1052-APP-6). The pattern set carries no access pattern, so this story adds no guard and no role table. No delegation of authority applies: the approval behind a notice is the Legal approval on the catalog version, and it is `rwb-comms`' check.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DOC-001 | document | id | Write |
| DF-DOC-002 | document | case_id | Write |
| DF-DOC-004 | document | document_type | Write |
| DF-DOC-005 | document | source | Write (`GENERATED`) |
| DF-DOC-006 | document | storage_ref | Write |
| DF-DOC-009 | document | retention_class | Write (from the type row) |
| DF-DOC-010 | document | write_once | Write (from the type row) |
| DF-DOC-011 | document | doc_version | Write |
| DF-DOC-025 | document | previous_version_id | Write, on a correction |
| DF-DOC-026 | document | content_sha256 | Write |
| DF-DOC-032 | document | template_id | Write (the catalog version identifier) |
| DF-DOC-012 to DF-DOC-017 | document_field | id, document_id, field_name, field_value, confidence, confirmed_by | Write, one row per merge code |
| Standard column | document | state, version, created_by, updated_by | Write |
| DF-REF-218 to DF-REF-233 | document_type | doc_type_code, retention_class, write_once | Read, in the version in force |
| DF-DOC-091 to DF-DOC-095 | retention_action | all fields | Not written: the monthly retention run writes it (RWB-P5-E1017-APP) |
| DF-LEG-015 to DF-LEG-023, DF-LEG-030 to DF-LEG-032 | notice | all fields | Not written and not read: the notice row is `rwb_comms`' |
| DF-ACE-056 to DF-ACE-083, DF-ACE-001 to DF-ACE-036 | `v_ace_*` customer, contact and account | all fields | Not read: they are inside the PDF and belong to `rwb-source-data` |

Field IDs are those of the Logical Data Model and Data Dictionary and the TSD P5 T3.1 tables. `document`, `document_field` and `document_type` are P5's in `rwb_document` (ownership map). The merge values arrive in the request and are written as `document_field` rows by the binding step; the decision record reference the caller writes names the field IDs and never a value; the `DOCATT` record of the store carries inputs references only. No field value, no file byte and no personal value enters an event payload or a log line. The `field_value` of `document_field` is classed as personal data for the merge codes that carry personal values.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Right | This story |
|---|---|---|---|
| API-P5-016 | POST `/api/recovery/document/v1/cases/{caseId}/generated-documents` | Documents C | The notice path of the operation: steps 2 to 9 of section 4. The generation engine for contract, CA and mortgage templates is RWB-P5-E2026-APP's |
| API-P5-003 | GET `/api/recovery/document/v1/documents/{documentId}` | Documents R | Answers the metadata, the version list and the fields of the stored notice |
| API-P5-004 | GET `/api/recovery/document/v1/documents/{documentId}/content` | Documents R | Answers the file whose SHA-256 is `content_sha256` |
| API-P5-017 | POST `/api/recovery/document/v1/documents/{documentId}/regenerate` | Documents U | The correction path: a new version with a reason, never a replace |

No new path is added. The request field names of the generation request, the reason field of the correction and the field names of the answer are Not specified in the source documents (GAP-2348; ASM-3903); they are fixed by RWB-P5-E2026-CON and matched to the caller's published shape of RWB-P6-E1052-CON. Every operation is published as OpenAPI 3.1 before code, with `Idempotency-Key` on the two POSTs.

#### 12.2 REST operations consumed

| Operation | Provider | Why | Pattern |
|---|---|---|---|
| GET `/api/recovery/case/v1/admin/lists/{listCode}` | rwb-case (P3), reference-data contract | LOV-DOC-TYPE, LOV-DOC-SOURCE and LOV-RETENTION in force, so no list value is a constant | DP07 |
| The store command of RWB-P5-E1024-APP (in service) | rwb-document | Identity, container write, `COPY_PENDING` → `STORED` and the copy retry | DP01 |

The rwb-case list read is consumed against its fake and is in no C row of this Work Package, which fixes one entry (GAP-2350; ASM-3905). No parameter is read: nothing of this story is tunable by parameter. The caller's request shape is the document part of RWB-P6-E1052-CON's flow and is the contract-test oracle of 12.8.

#### 12.3 Events published

| Event | Topic | Key | Payload |
|---|---|---|---|
| `rwb.document.DocumentStored.v1` (EV-16) | `rwb.document.events.v1` | caseId | documentId, caseId, source |

CloudEvents 1.0 binary mode, outbox row in the same transaction as the `STORED` state, published once per committed store by the relay, with retry and `.dlt` topics (DP09). The payload carries no file byte, no field value and no personal data; the envelope is the platform library's and the schema is `rwb_document_stored`. EV-17 `DocumentFieldsExtracted` is the extraction path's and is not published here.

#### 12.4 Events consumed

None. The generation is a synchronous call from `rwb-comms`, not an event, and the notice-derived events (`NoticeGenerated`, `NoticeDispatched`, `NoticeDelivered`) are `rwb-comms`'.

#### 12.5 Workflows and activities

None. `DocumentIntakeWorkflow` is the intake workflow of the service (RWB-P5-E1049-APP); this path runs in the caller's thread and waits for the store's answer. DP-10 is not a pattern of this story.

#### 12.6 Schedules

None. JOB-12 document intake (every 15 minutes) belongs to RWB-P5-E1049-APP and JOB-17 retention (monthly, first Sunday, 02:30 Asia/Bangkok) to RWB-P5-E1017-APP. Two other service story files attribute JOB-17 to this key; the mapping is recorded as a conflict and this story claims no Schedule (GAP-2351; ASM-3906).

#### 12.7 Tables owned

| Table | Schema | Owner (ownership map) | This story |
|---|---|---|---|
| document | rwb_document | P5 | Writes the row, `source` `GENERATED`, `write_once`, `retention_class`, `doc_version`, `template_id` and `content_sha256` |
| document_field | rwb_document | P5 | Writes one row per merge code through the binding step |
| document_type | rwb_document | P5 | **Reads** the row in force for `doc_type_code`, `retention_class` and `write_once` |
| notice, template, merge_field | rwb_comms | P6 | **Never read and never written.** The notice facts arrive in the caller's request and the merge values in its payload |

Database access uses the rwb-document login (DP02); its name is Not specified in the source documents (GAP-2348; ASM-3903). No statement names a table in another schema and `rwb_document` holds no key into another schema.

#### 12.8 Contract fakes

| Fake | Serves | Used for |
|---|---|---|
| RWB-P6-E1052-CON WireMock | The caller's generation request for case "RW-2026-000123", notice type "DEMAND", template "DEMAND-MTG" version 2 with id "TPL-0002", the four merge codes and the PDF reference; the repeat with "K-0001"; the unmapped notice type; a request outside the published shape; a delayed post | Every criterion of section 7 |
| type-table fixture "DOCTYPE-2026.11" | "DEMAND_LETTER", "GUARANTOR_NOTICE" and "COURT_NOTICE" in force from 30 November 2026, with the retention class and write-once flag of each row (the class and flag of the notice types are Not specified in the source documents (GAP-2347; ASM-3902)) | AC1, AC2, AC5 |
| notice-type mapping fixture | "DEMAND" → "DEMAND_LETTER", "GUARANTOR_NOTICE" → "GUARANTOR_NOTICE" (the mapping is Not specified in the source documents (GAP-2347; ASM-3902)); "STATEMENT" unmapped | AC2 |
| reference-data fake (DP07) | LOV-DOC-SOURCE with GENERATED; LOV-DOC-TYPE; LOV-RETENTION | AC2 |
| storage fake | The write-once legal container accepting the file, refusing it, and refusing a replace and a delete | AC1, AC4, AC5 |
| document fixture pack | Case "RW-2026-000123" with no generated document, and one stored "DEMAND_LETTER" version 1 with hash "H1" | AC1, AC3, AC5 |
| rwb-source-data contract fake | Customer, contact, account and POD data read inside the PDF (rwb-source-data contract) | TC-E1-052-07, TC-E1-052-11 |

A fake that drifts from RWB-P6-E1052-CON fails the contract test of that baseline.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 1 operation path extended (API-P5-016) and the two reads and the correction reused (12.1) | 1 read (the reference-data lists) | Inbound one hop from `rwb-comms`, 2 s budget; `Idempotency-Key` on the POSTs |
| Kafka | 1 event (`rwb.document.DocumentStored.v1`) | None | Outbox row in the store transaction, IDs only |
| Temporal | None | None | No workflow, activity or Schedule |
| File | 1 inbound claim-check PDF, written once to the write-once legal container | 0 | Path `{container}/{caseId}/{documentId}/v1`; `content_sha256` recorded |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, module `notices`. Base `/api/recovery/document/v1`, schema `rwb_document`, topic `rwb.document.events.v1`, task queue `rwb-document` (not used).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| GeneratedDocumentController | Controller | The notice path of API-P5-016: validation, the type resolution, the answer and the problem response |
| NoticeDocumentTypeResolver | Service | Maps the notice type to a document type row and takes its `retention_class` and `write_once`; refuses an unmapped type with MSG-P5-006 |
| NoticeDocumentService | Service | The store transaction: the binding call, the row with `source` `GENERATED`, the field rows, the state change and the outbox row |
| GenerationIdempotencyGuard | Service | Replays the first answer for a repeated `Idempotency-Key`; writes no second row, object or event |
| StorageWriter | Client of the store path | Writes the file once to the legal container, computes `content_sha256`, sets `STORED`, and leaves `COPY_PENDING` on a refused write |
| DocumentStoredPublisher | Service | Writes the `DocumentStored` outbox row when the row becomes `STORED` |
| NoticeDocumentConfig | Configuration | Feature flag, the container name from `document_hub_parameter`, the timeouts |

**Database.** No column is added: `document` and `document_field` already carry every field of section 11 (TSD P5 T3.1). One index, `ix_document_generated_notice` on `document` (`case_id`, `document_type`, `created_at`), so the one-document rule of a case and a type is one index range. One Flyway step in the per-service sequence after the V0001 baseline (DP15). The index name and the step name are Not specified in the source documents (GAP-2348; ASM-3903). No key into another schema: `template_id` is a value.

**Configuration and reference data.** The notice-type mapping, the type codes, the retention classes, the write-once flags, the container name and the source value are rows; none is a constant. The three lists arrive through the reference-data contract (DP07). Feature flag `rwb.document.notice-generation` (ASM-3903): off, a generation answers 503 with the feature-off error and stores nothing.

**Build steps**

1. Write the type resolver and the mapping fixture; test AC2 and the unmapped refusal.
2. Build the notice path of the controller over the store path; test AC1 and AC8.
3. Add the idempotency guard; test AC3 and the repeat of AC4.
4. Wire the `COPY_PENDING` → `STORED` step and the copy retry; test AC4.
5. Add the correction path and the write-once refusals; test AC5.
6. Run the boundary, guard and masking tests of AC6, AC7 and AC9 with the migration step and the index.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | none here: the D7.1 record is `rwb-comms`' and the store's `DOCATT` record is RWB-P5-E1024-APP's (H RWB-PLT-E1027-CON arrives through the store path) |
| DP-05 | AceSourceQuery, `v_ace_*` | ACE data through rwb-source-data's contract | none, as a prohibition: this service reads no view |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, outbox | Outbox and inbox library; owner topic; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

Each row in place. DP-01 keeps the notice row with its owner and the document in `rwb_document`, so the two agree by contract and by the stored reference, not by a key. DP-02 gives the service its own login. DP-03 stops a third record: the caller records the decision, the store records the store, this path records nothing. DP-05 is why no ACE read appears in the story. DP-07 makes the lists data, DP-09 puts the event in the store transaction, DP-11 makes the inbound call one hop with a fake, DP-13 rebases the path, DP-15 is the one migration step and DP-19 is the documents tab.

The H, C, I and X rows are the Work Package's: the build row is empty and the contract row is one entry, although DP-03, DP-07, DP-09, DP-15 and DP-19 name platform contracts and DP-07 names the rwb-case contract. The platform contracts are the service template's baseline, the rwb-case list read is consumed against its fake, and neither is added to a row (GAP-2350; ASM-3905). The platform contract stories are RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON, held in this table and in section 3, not duplicated in the story metadata (GAP-0754).

**Done when.** The tests of section 16 pass, a generated notice in SIT sits `STORED` in the legal container with a hash that matches its row, a replace is refused with MSG-P5-002, a repeat stores nothing, and the boundary test of AC9 is green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-002 | A change to a write-once legal document | Legal documents cannot be changed. Add a new version instead. |
| MSG-P5-006 | The notice type has no document type in force | Not specified in the source documents (GAP-2348; ASM-3903); the FSD names the code and the refused type only |
| MSG-GEN-006 | The storage copy does not complete inside the budget | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | The caller holds no Documents right for the operation | You cannot {action} here. Your role does not include it. |
| MSG-P6-005, MSG-P6-006, MSG-P6-003, MSG-GEN-001 | Raised by the binding step of RWB-P5-E1046-APP | Returned unchanged, with the binding's placeholders filled |

MSG-P5-002 is quoted from FSD P5 VR-P5-001-2 word for word; for MSG-GEN-006 the {system} value is "Document storage". Delivery shape: an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled and `instance` naming the request; a refused generation answers 403, 415, 422 or 503 and stores nothing.

### 15. Screens and states

No screen in this story. The generated notice appears on SCR-30 Case documents as a document of type "DEMAND_LETTER" with its template version, its state and its hash, read through the gateway-bff route (DP19). SCR-01 My work and SCR-18 Notice approval are `rwb-comms`' and `rwb-case`'s. The only state this story writes is the document state of section 9.

Screen states (Screen Specifications v1): SCR-01 My work has empty and loading as the specification gives them; error and no access: Not specified in the source documents (CG-ALL-5978). SCR-18 Notice approval: empty, loading, error and no access: Not specified in the source documents (CG-ALL-5979). SCR-30 Case documents has loading as the specification gives it; empty, error and no access: Not specified in the source documents (CG-ALL-5980).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-052-01 | AC1, AC2, AC7, BR1, BR5 (legacy AC1, the document part) | Component | Case RW-2026-000123; DEMAND-MTG TH v2 with id TPL-0002; the four merge codes; the PDF reference; type DOCTYPE-2026.11 |
| TC-E1-052-02 | AC2, BR4 (legacy AC2: a refused template leaves no document) | Component | RECALL-HP TH v1 Draft; the binding refuses and this path stores nothing |
| TC-E1-052-03 | AC4, BR7 (legacy AC3: a held notice has no document) | Component | P-0001 with no ADDRESS row; the hold is rwb-comms'; a posted request stores nothing |
| TC-E1-052-04 | AC2, BR4 (legacy AC4: a withdrawn template has no document) | Component | DEMAND-MTG TH v2 Withdrawn; no row, no file and no event |
| TC-E1-052-05 | AC4, BR7 (legacy AC5: a failed decision record writes no document) | Component | The caller's D7.1 record fails, so no request reaches this path; a request that does is stored once the answer is given |
| TC-E1-052-06 | AC3, BR2 (legacy AC6) | Component | The same request twice on 2026-11-25 with K-0001; one document, one object, one event |
| TC-E1-052-07 | AC1, BR1 (legacy AC7: the document keeps the date it was given) | Component | rwb-source-data contract fake: account data_as_of 2026-11-24 in the PDF text; the row and the event carry identifiers only |
| TC-E1-052-08 | AC2 (legacy AC8: refused before the store) | Component | P-0999 not on the case; the refusal is rwb-comms'; the store is not called |
| TC-E1-052-09 | AC8, BR6 (legacy Access) | Component | Service identity without Documents C posts API-P5-016; refused with MSG-P4-002 |
| TC-E1-052-10 | AC4, AC7 (legacy Principle 5) | Component | The storage copy forced to fail on 20 requests; 20 rows COPY_PENDING, no DocumentStored, no orphan file |
| TC-E1-052-11 | AC5, AC6, BR3, BR8 (legacy AC9, TC-E1-052-11) | Component | Notice with notice_ref WIN-77001 and a POD record in the rwb-source-data contract fake; the read is rwb-comms' and the document row is unchanged |
| TC-E1-052-12 | AC1, AC3, AC4, AC8, AC9, BR7 | Contract | The RWB-P6-E1052-CON fake, a post outside the published shape, a delayed post, and the boundary build check that no statement names rwb_comms or a view |
| TC-E1-052-13 | AC6, AC9 (section 12.7 tables) | Contract | Boundary test of the four tables of section 12.7: each statement and each key is checked against its owner schema; a statement naming notice, rwb_comms or a table outside rwb_document fails the build |
| TC-E1-052-14 | AC10, BR6 (X7) | Component | Service identity without Documents C posts a generation, and without Documents U posts a correction; refused with MSG-P4-002 before any row is read |
| TC-E1-052-15 | AC11 | Component | Generation posted without a service identity (401); correction on a document ID not on the case (404); the 401 and 404 messages are Not specified in the source documents (NEWAC-RWB-P5-E1052-APP-AC11) |

TC-E1-052-01 to TC-E1-052-11 are the legacy test cases, carried in the legacy order with the part this service answers named in the Covers column; their legacy acceptance criteria are owned by RWB-P6-E1052-APP and the composed cross-service proof is RWB-ITG-E1052-ITG, whose copies carry the `-ITG` suffix and are not listed here. TC-E1-052-12 is new under D-RCV-60 for the contract shape and the boundary build check. TC-E1-052-13, TC-E1-052-14 and TC-E1-052-15 are new under D-RCV-60 for the section 12.7 boundary, the X7 refusal and the error answers. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID where one exists.

### 17. Guardrails

- **No business value in code.** The notice-type mapping, the type codes, the retention classes, the write-once flags, the source value, the container name and the merge codes are rows or fixtures; none is a Java constant.
- **No personal data in logs, events, workflow inputs, tests or prompts.** The name, the address and the amounts sit inside the PDF and its masked field rows only; a value is replaced by its field name in a trace, and the fixtures of sections 7 and 16 are synthetic.
- **No cross-schema read and no cross-schema key** (DP01): no statement names `notice`, `template`, `rwb_comms` or any `v_ace_*` view, and `template_id` carries no foreign key.
- **ACE data only through the owner's contract or `v_ace_*` views.** This module reads no ACE view and holds no grant on `public`; the customer, contact and account facts reach the notice through `rwb-comms` and `rwb-source-data`.
- **The notice is write-once because its type is** (BR1): a class or a flag typed in code fails AC2.
- **A correction is a new version** (BR3): the stored bytes and the stamp of an earlier version are never touched.
- **The row, the file and the event agree** (BR7): no `DocumentStored` for a `COPY_PENDING` document, and no second document from a retried copy.
- **The guard is the service template's.** This story configures the Documents right of four operations and builds no guard, no role table and no access row.
- **No event, workflow or Schedule is added.** `DocumentFieldsExtracted` and `DocumentIntakeWorkflow` are other stories', and the two jobs belong to the intake and retention stories.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-001 | Notices from Legal-approved templates with merge fields from case data, stored on the case | Business Requirements Epic 1, sections 3.6 and 4 | FEAT-DRI-14 | 8.1 Prepare pre-litigation; 13 Manage documents and correspondence | R-LIT-03; BR1, BR2, BR4 | TC-E1-052-01, TC-E1-052-02, TC-E1-052-04, TC-E1-052-06, TC-E1-052-07, TC-E1-052-12, TC-E1-052-13 |
| NFR-029, CTL-12 | A legal document is write-once and cannot be altered inside its retention period | Non-functional requirements, legal documents; CTL-12 | FEAT-DRI-14 | 13 Manage documents and correspondence | BR1, BR3, BR7 | TC-E1-052-01, TC-E1-052-05, TC-E1-052-10, TC-E1-052-11, TC-E1-052-12 |

| Legacy reference | Where it is kept |
|---|---|
| Case RW-2026-000123, person_key P-0001, template DEMAND-MTG TH v2, business date 2026-11-25 | Background, AC1, sections 12.8 and 16 |
| Legacy step 8, the write-once store of the PDF on the case | Section 1, section 4, BR1 |
| Legacy BR5 (write-once), BR8 (one notice per key), BR11 (delivery facts from ACE) | Section 8, AC3, AC5, AC6 |
| MSG-P5-002, MSG-P5-006, MSG-GEN-006, MSG-P4-002, and the binding's messages | Section 14, exception paths |
| document, document_field, document_type field sets DF-DOC-* and DF-REF-218 to DF-REF-233 | Section 11, section 12.7 |
| Legacy key RWB-E1-052 and the split of its AC1 to AC9 | Metadata, section 1, section 7 closing note, section 16 |
| Legacy test cases TC-E1-052-01 to TC-E1-052-11 | Section 16 |

| Decision or pattern | Where it sits in this story |
|---|---|
| DP-01 | The document in `rwb_document`; the notice over its contract; no cross-schema key |
| DP-02 | The rwb-document login |
| DP-03 | No third record: the D7.1 and the `DOCATT` records stay with their owners |
| DP-05 | The ACE facts stay inside the PDF; no view is opened |
| DP-07 | The three lists and their fake |
| DP-09 | The `DocumentStored` outbox row in the store transaction |
| DP-11 | The inbound one-hop operation and the RWB-P6-E1052-CON fake |
| DP-13 | Base `/api/recovery/document/v1` |
| DP-15 | The one Flyway step in the service's own sequence |
| DP-19 | The documents tab behind gateway-bff |
| ADR-013, ADR-014 | The service owns its schema inside ACE PostgreSQL, with one login |
| ADR-015 | Kafka with outbox, inbox and CloudEvents |
| ADR-020 | Contract-first REST, one hop, 2 s timeout |

The legacy key is RWB-E1-052; its AC1 to AC9 and all eleven legacy test cases are owned by RWB-P6-E1052-APP, the contract baseline is RWB-P6-E1052-CON, and the composed proof is RWB-ITG-E1052-ITG. This file owns no legacy acceptance criterion (GAP-2349; ASM-3904).

### 19. Out of scope

- The template approval check, the merge value resolution, the two hold paths, the rendering and the footer, the `notice` row, the sent type, the D7.1 record, `NoticeGenerated`, dispatch to WIN and the proof of delivery read: RWB-P6-E1052-CON, RWB-P6-E1052-APP, RWB-P6-E1055-APP, RWB-P6-E2021-APP and RWB-P6-E2022-APP.
- The template and merge field catalog and its approval: RWB-P6-E1046-CON and RWB-P6-E1046-APP.
- The store path, the containers, the upload path and the `COPY_PENDING` retry: RWB-P5-E1024-APP.
- The document type table and its load: RWB-P5-E1025-APP.
- The catalog binding that stamps `template_id` and writes the catalog-checked fields: RWB-P5-E1046-APP.
- The generation engine for contract, CA and mortgage templates: RWB-P5-E2026-APP and RWB-P5-E2026-CON.
- The monthly retention run, the holds and the end-of-retention dispositions: RWB-P5-E1017-APP and RWB-P5-AD021-APP.
- The refusals of the case contract (MSG-P4-002, MSG-P4-003) and the roles and scope data: RWB-P4 and rwb-access.
- The cross-service proof of the notice journey: RWB-ITG-E1052-ITG.
