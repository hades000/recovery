# RWB-P5-E2026-APP Document generation engine for contract, CA and mortgage templates

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E2026-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-026 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP11, DP15, DP19 |
| Parallel lane | L-P5-G |
| Ready to start | After RWB-P5-E1024-APP |
| Depends on (build) | RWB-P5-E2026-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P5-E1024-APP |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P6-E1046-CON, RWB-P7-E1027-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-026) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the generation engine of legacy RWB-E2-026 is rebuilt inside `rwb-document` with the schema `rwb_document`, the topic `rwb.document.events.v1`, the REST base `/api/recovery/document/v1`, the template catalog read through the `rwb-comms` contract and the document written through RWB-P5-E1024-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P5-E2026-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **restructuring officer (FCR)**, I want **the generation engine that fills the contract, credit approval and mortgage templates from the case facts with the merge field catalog and Legal-approved versions**, so that **the documents the screens generate are correct and versioned**.

Inside `rwb-document` this is the generation capability of the document service:

- Service `rwb-document`, schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with event names `rwb.document.<Event>.v1`, Temporal task queue `rwb-document` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.document`.
- The engine reads the template version and the merge field list through the template catalog contract of `rwb-comms` (C `RWB-P6-E1046-CON`, DP-11, one hop, 2 s timeout, faked). It never reads the `template` or `merge_field` table: both are P6's in `rwb_comms` (DP-01).
- It reads the case through the `rwb-case` case contract `GET /api/recovery/case/v1/cases/{caseId}` with a fake, the parameters and the reference lists through the `rwb-case` parameters and reference-data contracts (C `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`, DP-06 and DP-07), the treatment through the `rwb-treatment` contract (S2, consumed and faked), and the party and collateral facts through the `rwb-source-data` contract (P1, consumed and faked, DP-05). Every call is one hop with a 2 s timeout and a breaker per downstream. The case contract, the S2 contract and the P1 contract are consumed by this story and appear in no C row of the work package (`ASM-1923`).
- It renders PDF/A-2b with the Thai fonts embedded and formats every value by its catalog format: the Thai long date in Buddhist Era, amounts with two decimals and amounts in Thai words.
- It records the decision through the local decision-record library of DP-03 (H `RWB-PLT-E1027-CON`; the central ledger contract of `rwb-decision` is C `RWB-P7-E1027-CON`) in the same transaction as the document row and the outbox row, with decision code D6.4 and final call GENERATED.
- It stores each generated document through RWB-P5-E1024-APP with `source` GENERATED, state DRAFT and `write_once` false; the store, not this engine, writes the blob, sets `storage_ref` and writes the `rwb.document.DocumentStored.v1` row per document. The path is `{container}/{caseId}/{documentId}/v1` as in RWB-P5-E1024-APP.
- Parameters are read through the parameters contract and client library of `rwb-case` (DP-06, H `RWB-PLT-E1042-CON`), and the document-hub rows they resolve to live in `document_hub_parameter` in `rwb_document`, which the Ownership Map gives to P5. The reference lists are read through the reference-data contract (DP-07, H `RWB-PLT-E1043-CON`). No parameter value and no list value is typed in code.
- The document row carries `template_id` (DF-DOC-032), `treatment_id` (DF-DOC-033), a `template_version` integer and the template code read from the catalog. The TSD P5 T3.1 table has `template_id` and `treatment_id` and no `template_code` or `template_version` column, while the legacy section 13 adds `template_code`, `template_version` and `treatment_id` in its own migration; the two added here are the assumption `ASM-1922` and the gap `GAP-1023`. The template codes themselves are Not specified in the source documents (GAP-1023; ASM-1925).
- The database login is one per service (DP-02). Its name is Not specified in the source documents (GAP-1023; ASM-1928); the story uses the phrase "the rwb-document login (DP-02)" and never a shared login.

The legacy behaviour is carried unchanged in intent and values: the same user story, rationale, preconditions, flow, exception paths, business rules, messages, authority, data fields, fourteen acceptance criteria and sixteen test cases, adapted to the target service's schema, topic, API base and contracts.

### 2. Business rationale

Deed in lieu and restructure document sets are typed today from the case file into Word templates, and a wrong amount or an old template wording reaches the customer. This engine fills each Legal-approved template version from the case facts held in the Workbench, refuses to produce a document with a missing value or an unapproved template, and records which template version and which inputs produced each document. It meets REQ-DCM-012 and REQ-OCC-002, applies control CTL-14 to the deed in lieu and restructure documents, and supports the target of 1,000 deed in lieu cases a month in 2027 (NFR-006).

The realignment changes the mechanics, not the business rule:

1. One service, one schema, one topic and one API base: `rwb-document`, `rwb_document`, `rwb.document.events.v1` and `/api/recovery/document/v1`. The legacy `recovery.dochub.generation` package is retired and the operation is rebased below the service base (DP-13).
2. Every cross-service part becomes a published contract with a fake and a 2 s timeout: the P6 catalog (C `RWB-P6-E1046-CON`), the P3 case, parameters and lists (C `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`), the S2 treatment and the P1 source data (consumed and faked, `ASM-1923`). No module is called in process and no foreign table is read.
3. The decision log write becomes the local decision-record library of DP-03, written in the same transaction as the document rows and the outbox rows and published on `rwb.decision-record.v1`; `rwb-decision` seals it in the central ledger.
4. The template catalog moves out of the document module: `template` and `merge_field` are P6's in `rwb_comms`, and the engine reads the current version and the merge field list through the catalog contract only (`ASM-1921`).
5. Parameters and reference data leave the code: `GEN_IDEMPOTENCY_HOURS`, `GEN_MAX_TEMPLATES` and the font come through the parameters contract (DP-06) and the type mapping and template codes are data rows (DP-07, DL19, DL28).
6. The renderer is target-side work: PDF/A-2b with the Thai fonts embedded, one component, one conformance test (`ASM-1926`).
7. Every generated draft is stored through RWB-P5-E1024-APP, so the blob, the hash, the retention class and the write-once policy stay with the store and the engine never writes a file itself.
8. The migration is one step in the per-service Flyway sequence (DP-15) with one partial unique index for the concurrent case, and no data lake is connected and no `INT-19`/`INT-20` path is used anywhere (DP-17).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P5-E2026-CON | The published contract baseline of the generation API: the generate operation, `GenerateRequest`, `GenerationResult`, the `Document` shape, the provider interfaces, the error envelope, the `Idempotency-Key` rule and the event schema |
| RWB-PLT-E1027-CON | The decision-record library: `RecordAndApply` writes the D6.4 record inside the caller's transaction and publishes it on `rwb.decision-record.v1` (DP-03) |
| RWB-PLT-E1042-CON | The parameters client library, so `GEN_IDEMPOTENCY_HOURS`, `GEN_MAX_TEMPLATES` and `GEN_FONT` are read through a published shape (DP-06) |
| RWB-PLT-E1043-CON | The reference-data client library for the type mapping list and the language list (DP-07) |
| RWB-PLT-TE006-CON | The outbox, inbox and idempotency library; the `DocumentStored` row and the idempotency row are written in the generation transaction (DP-09) |
| RWB-PLT-E1044-CON | The per-service Flyway sequence that carries the two added columns and the partial unique index as one step (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route through which the case documents screen reaches the generated drafts (DP-19) |
| RWB-P5-E1024-APP | The store command and the `Document` shape: source, storage reference, retention class, write-once flag, version, and the `DocumentStored` row per stored document |
| RWB-P3-E1042-CON | `rwb-case`'s parameters contract, which resolves the three generation parameters (DP-06) |
| RWB-P3-E1043-CON | `rwb-case`'s reference-data contract, which resolves the type mapping and language lists (DP-07) |
| RWB-P6-E1046-CON | The `rwb-comms` template catalog contract: the current version by code, language, product group and date, and the merge field list of a version (the C dependency that replaces the legacy in-process `TemplateCatalog`) |
| RWB-P7-E1027-CON | The central decision ledger contract that collects the local D6.4 record (DP-03) |

Business preconditions carried from RWB-E2-026:

- Templates DIL-CONTRACT, DIL-CA and DIL-MORTGAGE, and RES-AGREEMENT for restructure, are loaded in Thai with `approved_by_legal = true`. The template codes are assumed (DL28); their field-level identity is Not specified in the source documents (GAP-1023; ASM-1925).
- The template-to-document-type mapping is in the document type table: DIL-CONTRACT to CONTRACT, DIL-CA to CREDIT_APPROVAL, DIL-MORTGAGE to MORTGAGE_DOCUMENT, RES-AGREEMENT to CONTRACT (assumed; DL19). The mapping rows are data, never code; its field-level shape is Not specified in the source documents (GAP-1023; ASM-1925).
- The case has a treatment of type DEED_IN_LIEU or RESTRUCTURE with `decision_log_id` set (approved at D6.4) and no outcome.
- The merge field providers of P3 (case), S2 (treatment) and P1 (party and collateral) are listed in the `MergeFieldResolver` configuration and are reached through their contracts, never through their tables.
- The caller holds Documents C (RW-RESTRUCT or RW-CASEOWN), or is the service identity SY-CASEWF for rule-driven generation from Epic 3.
- The feature flag `rwb.document.generation-engine` is on. The legacy flag name `rwb.dochub.generation-engine` is retired with the monolith; the new name and the 24-hour idempotency window are assumed (`ASM-1929`).

The generation operation path is the Ownership Map and TSD P5 API-P5-016 name `/cases/{caseId}/generated-documents`, while Architecture v5 slide 16 names `POST /documents/generate`; the conflict is recorded as `GAP-1023` and resolved as `ASM-1920`. The database login name is Not specified in the source documents (GAP-1023; ASM-1928).

### 4. Flow

1. Restructuring officer or SY-CASEWF: calls `POST /api/recovery/document/v1/cases/{caseId}/generated-documents` with `GenerateRequest` (`treatmentId` required, `templateCodes` 1 to 10 required, `language` TH or EN default TH, the overrides the screens story uses) and an `Idempotency-Key` header. The controller passes it to the `generate` activity on queue `rwb-document` (12.5).
2. `DocumentGenerationService`: reads the treatment through the `rwb-treatment` contract `GET /api/recovery/treatment/v1/treatments/{treatmentId}` (S2, one hop, 2 s, breaker) and checks it is approved, open and of type DEED_IN_LIEU or RESTRUCTURE (BR5). The contract is consumed and faked and is not in the C list (`ASM-1923`).
3. `TemplateSelector`: for each template code, reads the current version through the `rwb-comms` catalog contract (C `RWB-P6-E1046-CON`) for the language and product group: approved by Legal, active, highest version valid on the request date; the most specific product group match wins over a template for all products (BR1, BR2).
4. `MergeFieldResolver`: reads the merge field list of that version through the same contract and asks each owning provider for the values through its contract: `rwb-case` (`GET /api/recovery/case/v1/cases/{caseId}`), `rwb-treatment` (the treatment read of step 2) and `rwb-source-data` (the party and collateral read, DP-05). Every call is one hop with a 2 s timeout and a breaker per downstream.
5. `MergeFieldResolver` and `ValueFormatter`: check that every required merge field has a value (BR3), then format each value by its catalog format: the Thai long date in Buddhist Era, amounts with two decimals and amounts in Thai words (BR4). A national ID number is filled from the token service at render time and never logged (BR11).
6. `TemplateRenderer`: renders each template body to PDF/A-2b with the Thai fonts embedded and writes the rendered file to the draft area of the quarantine container through the storage product RWB-PLT-TE012-APP that RWB-P5-E1024-APP also uses (the storage product is not a new X dependency of this story), at `{container}/{caseId}/{documentId}/v1`, keeping the merge snapshot beside it and never in a log.
7. `DocumentGenerationService`, one transaction in `rwb_document`: writes one decision record with decision code D6.4, an inputs reference to the merge snapshot and, per document, the template code and version, through the decision-record library of DP-03; stores each document through RWB-P5-E1024-APP with `source` GENERATED, state DRAFT, `write_once` false, the template code, the template version and the treatment ID; and writes one `rwb.document.DocumentStored.v1` outbox row per document (DP-09). A failed record aborts the whole set.
8. `GeneratedDocumentController`: returns 201 with `GenerationResult`: `decisionLogEntryId` and `documents[]` with `documentId`, `templateCode`, `templateVersion`, `documentType`. The screens story RWB-P5-E2017-APP shows the drafts for review.
9. Outbox relay: publishes `rwb.document.DocumentStored.v1` to `rwb.document.events.v1`, keyed by caseId, and the decision record to `rwb.decision-record.v1`; no payload carries a file byte or a personal value.

A failure at any step removes the draft file and writes nothing: no document row, no decision record and no outbox row for the set (X5, X11, AC2, AC7, AC14). The whole set is stored or none of it is (BR8).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A required merge field has no value | Generation stops; nothing stored; the field is named | MSG-P5-009 | AC2 |
| X2 | The current template version is not approved by Legal | Generation stops; nothing stored | MSG-P5-010 | AC4 |
| X3 | The template is withdrawn | Generation stops; a task goes to the restructuring officer, as R-LIT-04 does for notices | MSG-P6-003 | AC5 |
| X4 | The treatment is not approved, is closed, or is of another type | 409; nothing stored | MSG-P5-011 | AC6 |
| X5 | The decision log write fails | Nothing stored; draft files removed; incident raised | MSG-P7-003 | AC7 |
| X6 | The same request is repeated with the same Idempotency-Key | The first result is returned; nothing new is stored | None | AC8 |
| X7 | Two requests for the same treatment and template run at once | One succeeds; the other gets 409 | MSG-GEN-004 | AC9 |
| X8 | A template body cannot be rendered | 503; nothing stored; incident raised | MSG-GEN-006 | AC10 |
| X9 | No template exists for the product group or language | Generation stops and names the template | MSG-P5-010 | AC11 |
| X10 | The case is outside the caller's scope | 404 | MSG-P4-003 | AC12 |
| X11 | One template of a set fails its check | Nothing of the set is stored | MSG-P5-010 | AC14 |
| X12 | The caller lacks Documents C | 403 | MSG-P4-002 | Access test TC-E2-026-15 |

Three target-service notes:

- X7 is enforced by the partial unique index `ux_document_draft_per_template ON document (treatment_id, template_id) WHERE state = 'DRAFT' AND is_active` plus the pre-insert read, exactly as the legacy `template_code` index did; the second request receives 409 with MSG-GEN-004 and keeps no row.
- A repeat with the same `Idempotency-Key` inside the 24-hour window returns the first answer and creates nothing, including the AC8 case where the first answer carried document DOC-0311. The window and the header rule are `ASM-1929` and are declared by RWB-P5-E2026-CON.
- A downstream contract that does not answer within 2 s, or whose breaker is open, is refused with 503 and MSG-GEN-006 naming the system that failed; no partial set is stored and the drafting area is cleaned as in X5.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the contract baseline (RWB-P5-E2026-CON), the store (RWB-P5-E1024-APP), the P6 catalog contract, the decision-record, parameters, reference-data, outbox, Flyway and gateway contracts, all earlier work |
| Negotiable | Templates, merge fields, formats, the type mapping and the fonts are data rows or parameters owned by Legal and the product owner |
| Valuable | Ends re-keying of deed in lieu and restructure documents and makes every generated set traceable to a template version |
| Estimable | One service, one renderer, one resolver, one formatter, one operation, one migration, no screen |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion in section 7 is one test case in section 16, on synthetic case data |

### 7. Acceptance criteria

```gherkin
Feature: Document generation engine for contract, CA and mortgage templates

  Background:
    Given case "RW-2026-000301" with product group "MORTGAGE"
    Given treatment "TRT-0301" of type "DEED_IN_LIEU" on that case with decision_log_id set and no outcome
    Given template "DIL-CONTRACT" version 2 in Thai for "MORTGAGE" with approved_by_legal true
    Given the merge fields of "DIL-CONTRACT" version 2 are case_no, borrower_name, title_doc_no, transfer_price and contract_date
    Given a restructuring officer with role RW-RESTRUCT in scope of the case
    Given the rwb-comms template catalog contract mock returns template "DIL-CONTRACT" version 2 in Thai for "MORTGAGE" with approved_by_legal true
    Given the rwb-case contract mock returns case "RW-2026-000301" with product group "MORTGAGE" for role RW-RESTRUCT
    Given the rwb-treatment contract mock returns treatment "TRT-0301" of type "DEED_IN_LIEU" with decision_log_id set and no outcome
    Given the rwb-source-data contract mock returns the party and collateral facts of case "RW-2026-000301"
    Given the rwb-decision contract mock returns the central ledger reference for decision code "D6.4"

  Scenario: AC1 Generate (legacy RWB-E2-026 AC1)
    Given the case facts give transfer_price 1250000.00, title_doc_no "12345" and contract_date 2026-12-10
    When the engine runs for treatment "TRT-0301" and template "DIL-CONTRACT"
    Then the system stores one document with document_type "CONTRACT", source "GENERATED", state "DRAFT" and write_once false
    Then the document carries template_code "DIL-CONTRACT", template_version 2 and treatment_id "TRT-0301"
    Then the PDF shows "1,250,000.00 baht (one million two hundred fifty thousand baht)" and "10 December 2569 BE"
    Then the system writes one decision log entry with decision code "D6.4" and an inputs reference to the merge snapshot
    Then one DocumentStored event is in the outbox

  Scenario: AC2 Missing field (legacy RWB-E2-026 AC2)
    Given the case has no title_doc_no
    When the engine runs for template "DIL-CONTRACT"
    Then the response is 422 with MSG-P5-009 naming "DIL-CONTRACT" and "title_doc_no"
    Then no document, no file and no decision log entry is stored

  Scenario: AC3 Version (legacy RWB-E2-026 AC3)
    Given template "DIL-CONTRACT" version 3 is approved by Legal and valid from 2026-12-15
    Given document "DOC-0310" was generated on 2026-12-10 from version 2
    When the engine runs on 2026-12-15
    Then the new document carries template_version 3
    Then "DOC-0310" still carries template_version 2 and its file opens
    Then template version 2 stays readable in the template catalog

  Scenario: AC4 A version not approved by Legal is refused (legacy RWB-E2-026 AC4)
    Given template "DIL-CA" has only version 1 with approved_by_legal false
    When the engine runs for template "DIL-CA"
    Then the response is 422 with MSG-P5-010 naming "DIL-CA" version 1
    Then the system stores nothing

  Scenario: AC5 A withdrawn template holds generation (legacy RWB-E2-026 AC5)
    Given template "DIL-MORTGAGE" version 1 is withdrawn and no later version is approved
    When the engine runs for template "DIL-MORTGAGE"
    Then the response is 422 with MSG-P6-003 naming "DIL-MORTGAGE"
    Then the system raises a task to the restructuring officer who requested it

  Scenario: AC6 A treatment that is not approved is refused (legacy RWB-E2-026 AC6)
    Given treatment "TRT-0302" of type "DEED_IN_LIEU" with no decision_log_id
    When the engine runs for treatment "TRT-0302"
    Then the response is 409 with MSG-P5-011
    Then the system stores nothing

  Scenario: AC7 The decision log write fails (legacy RWB-E2-026 AC7)
    Given the decision log store does not accept writes
    When the engine runs for treatment "TRT-0301" and template "DIL-CONTRACT"
    Then the response is 503 with MSG-P7-003
    Then no document row exists for "TRT-0301" and the draft file is removed from the container
    Then the system raises an incident as in R-UNI-39

  Scenario: AC8 A repeated request (legacy RWB-E2-026 AC8)
    Given a request with Idempotency-Key "K-0301" generated document "DOC-0311"
    When the same request with Idempotency-Key "K-0301" arrives again
    Then the response is 201 with document "DOC-0311"
    Then no second document or decision log entry is written

  Scenario: AC9 Two requests at the same time (legacy RWB-E2-026 AC9)
    Given two requests for treatment "TRT-0301" and template "DIL-CONTRACT" with different keys arrive together
    When both run
    Then one returns 201 with one DRAFT document
    Then the other returns 409 with MSG-GEN-004

  Scenario: AC10 A template body that cannot be rendered (legacy RWB-E2-026 AC10)
    Given the body of "DIL-CONTRACT" version 2 is a damaged file
    When the engine runs
    Then the response is 503 with MSG-GEN-006 naming "document generation"
    Then the system stores nothing and an incident is raised

  Scenario: AC11 No template for the product group (legacy RWB-E2-026 AC11)
    Given template "DIL-CONTRACT" exists only for product group "MORTGAGE"
    Given case "RW-2026-000305" has product group "HIRE_PURCHASE"
    When the engine runs for that case and "DIL-CONTRACT"
    Then the response is 422 with MSG-P5-010 naming "DIL-CONTRACT" for "HIRE_PURCHASE"

  Scenario: AC12 A case outside the caller's scope (legacy RWB-E2-026 AC12)
    Given case "RW-2026-000306" is in team "HP-NE" and the officer's scope is team "FCR-BKK"
    When the officer requests generation for that case
    Then the response is 404 with MSG-P4-003

  Scenario: AC13 A set of three documents in one request (legacy RWB-E2-026 AC13)
    Given templates "DIL-CONTRACT", "DIL-CA" and "DIL-MORTGAGE" are current and approved
    When the engine runs for treatment "TRT-0301" with the three template codes
    Then the system stores three documents with types "CONTRACT", "CREDIT_APPROVAL" and "MORTGAGE_DOCUMENT"
    Then one decision log entry names the three template codes and versions

  Scenario: AC14 A set is stored whole or not at all (legacy RWB-E2-026 AC14)
    Given templates "DIL-CONTRACT" and "DIL-MORTGAGE" are current and approved
    Given template "DIL-CA" has no version approved by Legal
    When the engine runs for treatment "TRT-0301" with the three template codes
    Then the response is 422 with MSG-P5-010 naming "DIL-CA"
    Then the system stores none of the three documents and no decision log entry is written
```

Every Given, When and Then line above is the legacy line unchanged. The cross-service parts are mocked by the five added Background Givens on the `rwb-comms` catalog, the `rwb-case` case, the `rwb-treatment` treatment, the `rwb-source-data` party and collateral facts and the `rwb-decision` central ledger. In AC1 the "PDF" is the PDF/A-2b file stored through RWB-P5-E1024-APP, and the "document" carries the template code, the template version and the treatment ID of the target `document` row. In AC7 the "decision log store" is the decision-record library and the central ledger contract of `rwb-decision`. In AC5 the task is raised through the `rwb-case` task contract; the operation is not part of this story.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A document is generated only from the current template version: approved by Legal, active and valid on the request date; the most specific product group match wins over a template for all products | DF-REF-047, DF-REF-049, DF-REF-051; CTL-14; R-LIT-03 |
| BR2 | A withdrawn template with no approved successor holds generation and raises a task | R-LIT-04; R-LIT-06 |
| BR3 | Every required merge field must have a value; otherwise nothing is generated and the field is named | Merge field catalog (RWB-E1-046); FEAT-OCC-07 |
| BR4 | Values are formatted by the catalog format: Thai long date in Buddhist Era, amounts with two decimals and in Thai words | Merge field catalog; Principle 1 |
| BR5 | Generation is allowed only for an approved, open treatment of type DEED_IN_LIEU or RESTRUCTURE | DF-TRT-003, DF-TRT-004, DF-TRT-013; R-DIL-14; R-DIL-16 |
| BR6 | A generated document carries the template code and version, the treatment and the source GENERATED; it is a DRAFT and not write-once until it is sent (RWB-E2-017) | DF-DOC-005, DF-DOC-010; CTL-12 |
| BR7 | Generation that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39; CTL-06 |
| BR8 | A set is generated whole or not at all | Events rule "Transactions" |
| BR9 | A repeat with the same Idempotency-Key returns the first result | R-UNI-40 |
| BR10 | A new template version applies to documents generated from its valid-from date; earlier documents keep their version | R-UNI-38 |
| BR11 | A national ID number is filled from the token service at render time; the clear value exists only inside the stored PDF | DF-PTY-007; CTL-11; DL26 |

Target-service statements that make the rules hold in `rwb-document`:

- BR1 and BR10 are executed by `TemplateSelector` against the P6 catalog contract: the answer carries the version, its Legal approval, its valid-from date and its product group, and the engine keeps the version on the document row. The legacy in-process `TemplateCatalog` is retired; the catalog is `rwb-comms`'s table and this service holds no copy (`ASM-1921`).
- BR2 is executed by the refused generation plus the task raised through the `rwb-case` task contract; the engine writes no task row of its own (DP-01, DP-11).
- BR3, BR4 and BR11 are executed by `MergeFieldResolver` and `ValueFormatter`: the required flag comes from the catalog answer, the format comes from the catalog answer, the token service is called at render time, and no merge value, snapshot or clear ID number is ever written to a log (section 17).
- BR5 is executed by the treatment read through the `rwb-treatment` contract: the type, the approval and the `decision_log_id` arrive in one answer, and no treatment table is read (S2 owns `treatment`).
- BR6 is executed by the document row: `source` GENERATED, `state` DRAFT, `write_once` false, `template_id`, `template_version` and `treatment_id` written in one transaction, and by the store that keeps `write_once` false until the document is sent.
- BR7 and BR8 are executed by the decision-record library of DP-03 inside the generation transaction: the record, every document row and every outbox row commit together or not at all (R-UNI-39); a partial set is impossible.
- BR9 is executed twice: the `Idempotency-Key` row of the outbox and idempotency library (DP-09) returns the first answer inside 24 hours, and the partial unique index refuses a second active DRAFT for the same treatment and template.
- The parameters and reference lists arrive through DP-06 and DP-07; the migration is one step in the per-service Flyway sequence (DP-15); the event is in the outbox (DP-09); the engine evaluates no rule package and loads no Drools kit.

### 9. State transitions

None. This story does not change a case status. It creates documents in state DRAFT.

| From | Event | Condition | To |
|---|---|---|---|
| (none) | Generation requested | BR1, BR3 and BR5 pass and the decision log write succeeds | document state DRAFT |

Target columns written by the same transition:

| Column | Value in this story |
|---|---|
| `document.state` | DRAFT |
| `document.source` | GENERATED |
| `document.write_once` | false |
| `document.doc_version` | 1 |
| `document.template_id` | The identifier of the current catalog version (DF-DOC-032) |
| `document.template_version` | The version number read from the catalog (the added column, `ASM-1922`) |
| `document.treatment_id` | The treatment of the request (DF-DOC-033) |
| `document.is_active` | true |

No transition out of DRAFT happens in this story: review, send and the write-once switch on send belong to RWB-P5-E2017-APP (BR6). No case state, no treatment state and no template state is changed here; the template state belongs to `rwb-comms` and the treatment state to `rwb-treatment`.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT, restructuring officer (FCR) | Requests generation for a treatment in scope (Documents C) |
| RW-CASEOWN, case owner | Requests generation for a treatment in scope (Documents C) |
| SY-CASEWF, case workflow module | Calls the generation operation for rule-driven generation from Epic 3 (R-DIL-14, R-DIL-16) |
| SY-DECLOG, decision record writer | Writes the D6.4 record inside the generation transaction |
| RW-LEGAL, legal counsel | Approves template versions (Documents CRUA; RWB-E1-034); approval is a precondition of this story, not part of it |
| RW-TEAMMGR, team manager | Reads generated documents (Documents R); cannot generate |
| the rwb-document login (DP-02) | The service identity that writes the document rows, the decision record and the outbox rows |

No approval level from the delegation of authority applies in this story. The treatment itself was approved at D6.4 before generation.

Service identities and owners: `rwb-document` owns the `document` row and the generation transaction; the decision-record library writes the local record and `rwb-decision` (P7) owns the central ledger; `rwb-comms` (P6) owns the template version, its Legal approval and the merge field catalog; `rwb-treatment` (S2) owns the treatment; `rwb-case` (P3) owns the case, the parameters and the reference lists; `rwb-source-data` (P1) owns the party and collateral facts.

The authorisation decision is `rwb-access`'s (Recovery roles as data, scope, masking and DoA in `rwb_access`) and is consumed as the cached permission decision the service holds. This story adds no guard, no role and no scope rule of its own: the refusal shapes are 403 with MSG-P4-002, 403 or 404 with MSG-P4-003, exactly as the legacy endpoints had them. Where the legacy guard is replaced by the shared guard library (DP-08) is another story's deliverable; this story inherits it.

The database login is per service (DP-02). Its name is Not specified in the source documents (GAP-1023; ASM-1928); the story refers to "the rwb-document login (DP-02)".

### 11. Data

| BR Field ID | Table in `rwb_document` or contract | Field | Read or write |
|---|---|---|---|
| DF-DOC-001 to DF-DOC-011 | `document` | id, case_id, party_id, document_type, source, storage_ref, classification_confidence, review_status, retention_class, write_once, doc_version | Write |
| DF-DOC-032 | `document` | template_id | Write |
| DF-DOC-033 | `document` | treatment_id | Write |
| (added column) | `document` | template_version integer | Write |
| (added column) | `document` | template_code varchar(30) | Write |
| Standard column | `document` | state, is_active, version | Write |
| DF-REF-045 to DF-REF-051 | `rwb-comms` template catalog, through the contract | the template version and its approval, valid-from, product group and merge field list | Read |
| DF-CAS-001, DF-CAS-002, DF-CAS-003, DF-CAS-004 | `rwb-case` case, through the contract | id, case_no, product_group, primary_person_key | Read |
| DF-TRT-001, DF-TRT-003, DF-TRT-004, DF-TRT-007, DF-TRT-013 | `rwb-treatment` treatment, through the contract | id, decision_log_id, treatment_type, offer_amount, outcome | Read |
| DF-ACE-057, DF-ACE-058, DF-ACE-197 | `rwb-source-data` party and collateral, through the contract | first_name, last_name, title_doc_no | Read |
| (decision record) | decision-record library table in `rwb_document` | chain_seq, inputsRef, ruleId, finalCall, decidedAt, prev_hash, entry_hash | Write |
| (outbox) | outbox library table in `rwb_document` | the row for DocumentStored and the row for the decision record | Write |
| (idempotency) | idempotency library table in `rwb_document` | the request key and the first answer | Write |
| (parameter) | `rwb-case` parameters, through the contract | `GEN_IDEMPOTENCY_HOURS`, `GEN_MAX_TEMPLATES`, `GEN_FONT` | Read |
| (reference list) | `rwb-case` reference data, through the contract | the type mapping list and the language list | Read |

Field IDs are those in the Logical Data Model and Data Dictionary and the TSD P5 T3.1 table. The legacy section 11 lists DF-DOC-032 twice; the target table lists it once.

No `rwb_case` row and no ACE view is read by this service: the case fields arrive inside the `rwb-case` contract answer and the customer name and title-doc number arrive inside the `rwb-source-data` contract answer, masked by policy and read in one hop (DP-05, DP-01). The template fields are read through the `rwb-comms` contract and are not copied. The `template_code` and `template_version` columns are added beside `template_id` and `treatment_id` because the legacy data model carries all four and the TSD P5 T3.1 carries only two (`ASM-1922`). No personal value and no file byte enters an event payload, a workflow input, a decision record or a log.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Notes |
|---|---|---|---|
| POST | `/api/recovery/document/v1/cases/{caseId}/generated-documents` | P5 | `GenerateRequest`: `treatmentId` uuid required, `templateCodes` array of string 1 to 10 required, `language` TH or EN default TH, `overrides` for the screens story; header `Idempotency-Key` required; answer 201 `GenerationResult` with `decisionLogEntryId` and `documents[]` (`documentId`, `templateCode`, `templateVersion`, `documentType`) |

The Ownership Map and TSD P5 API-P5-016 give this path; Architecture v5 slide 16 names `POST /documents/generate`. The conflict is recorded as `GAP-1023` and resolved as `ASM-1920` in favour of the Ownership Map name. The field-level definition of `GenerateRequest` and `GenerationResult` is fixed by RWB-P5-E2026-CON and is Not specified in the source documents beyond the legacy section 12 (`ASM-1924`).

`POST /api/recovery/document/v1/documents/{documentId}/regenerate` is API-P5-017 and belongs to RWB-P5-E2017-APP; this story declares it neither as provided nor as consumed.

#### 12.2 REST operations consumed

| Operation | Path | Owner | Story | Note |
|---|---|---|---|---|
| GET | the template catalog current version and merge field list | P6 rwb-comms | RWB-P6-E1046-CON | The current version by code, language, product group and date, and the merge field list of a version; the path is Not specified in the source documents (GAP-1023; ASM-1921) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | RWB-P3-E1018-CON (consumed and faked; in no C row, `ASM-1923`) | The case facts of the merge fields, in one hop with a 2 s timeout and a breaker (DP-11) |
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | the S2 contract, consumed and faked | The treatment type, approval and `decision_log_id` of BR5; not in the C list (`ASM-1923`) |
| GET | the party and collateral read of the source data | P1 rwb-source-data | the P1 contract, consumed and faked | `first_name`, `last_name` and `title_doc_no`, masked by policy (DP-05); the path is Not specified in the source documents (GAP-1023; ASM-1923) |
| GET | `/api/recovery/case/v1/admin/parameters/{paramCode}` | P3 rwb-case | RWB-P3-E1042-CON | `GEN_IDEMPOTENCY_HOURS`, `GEN_MAX_TEMPLATES`, `GEN_FONT` (DP-06) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | RWB-P3-E1043-CON | The type mapping and language lists (DP-07) |
| POST | the central ledger sealing operation of `rwb-decision` | P7 rwb-decision | RWB-P7-E1027-CON | The seal of the local D6.4 record; consumed, not in the C list as a separate read (`ASM-1923`) |

The case contract `RWB-P3-E1018-CON`, the S2 treatment contract, the P1 source-data contract and the P7 read are consumed by this story and are not in its C list as the WP gives it: the gap `GAP-1023` and the assumption `ASM-1923` record that, and the C list is left exactly as the WP gives it. Every row is one hop with a 2 s timeout, a GET retry once with jitter and a breaker per downstream (DP-11, ADR-020). A failed read maps to 503 with MSG-GEN-006 naming the system that failed and never to a partial set.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.document.DocumentStored.v1` (EV-16) | `rwb.document.events.v1` | P5 | caseId | documentId, caseId, documentType, source, storedAt |
| decision record (decision code D6.4, final call GENERATED) | `rwb.decision-record.v1` | PLT library, consumed by P7 | caseId | the hash-chained record with the merge snapshot reference, not the snapshot itself |

CloudEvents 1.0 envelope, binary mode. The store RWB-P5-E1024-APP writes the `DocumentStored` row per stored document in its own transaction; this engine contributes the decision record and the document rows that the store commits. Neither payload carries a personal value, a merge value or a file byte. `rwb.document.DocumentFieldsExtracted.v1` is the service's other event and is published by the extraction path, never by this story.

#### 12.4 Events consumed

None. This story consumes no Kafka event: the treatment, the case, the source data, the parameters and the lists are synchronous reads, and the trigger is the HTTP request.

#### 12.5 Workflows and activities

| Name | Kind | Queue | Note |
|---|---|---|---|
| `generate` | Activity | `rwb-document` | Renders and stores one requested set inside the caller's request; called synchronously by `GeneratedDocumentController` and by the screens story RWB-P5-E2017-APP |
| `DocumentIntakeWorkflow` | Workflow, from the L3 workflow kit template "Document intake" | `rwb-document` | Named only: owned by RWB-P5-E1049-APP, and its generate step is the same activity; this story neither registers nor changes the workflow |

#### 12.6 Schedules

None. JOB-17 retention belongs to RWB-P5-E1017-APP; this story starts no Schedule and no timer.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `document` | P5 | Write: one row per generated document, state DRAFT, source GENERATED |
| `document_type` | P5 | Read only: the document type and retention class behind the template-to-type mapping |
| decision-record library table | PLT library, created in `rwb_document` | The D6.4 record in the generation transaction |
| outbox, inbox and idempotency library tables | PLT library, created in `rwb_document` | The DocumentStored and decision-record rows and the `Idempotency-Key` row |

No foreign-schema table is read (DP-01): `template`, `merge_field`, `recovery_case`, `treatment`, `decision_log_entry`, `lov_value`, `parameter_catalog` and the ACE views belong to P6, P3, S2, P7 and P1.

#### 12.8 Contract fakes

| Fake | Story | Used for |
|---|---|---|
| rwb-comms template catalog fake | RWB-P6-E1046-CON | The current version by code, language, product group and date; the approved, unapproved, withdrawn and future-version cases of BR1, BR2 and BR10; the merge field list and its required flags |
| rwb-case case fake | RWB-P3-E1018-CON (consumed and faked; in no C row, `ASM-1923`) | `GET /cases/{caseId}` for the case facts, and the scope refusal of AC12 |
| rwb-treatment fake | consumed S2 contract | The approved, open treatment of DEED_IN_LIEU and the refused `TRT-0302` of AC6 |
| rwb-source-data fake | consumed P1 contract | `first_name`, `last_name` and `title_doc_no` of the merge fields, with the missing-value case of AC2 |
| rwb-case parameters and reference-data fake | RWB-P3-E1042-CON and RWB-P3-E1043-CON (through RWB-PLT-E1042-CON and RWB-PLT-E1043-CON) | `GEN_IDEMPOTENCY_HOURS` 24, `GEN_MAX_TEMPLATES` 10, the font, the type mapping and the language list |
| decision-record fake and central ledger fake | RWB-PLT-E1027-CON and RWB-P7-E1027-CON | The local D6.4 record and its seal; the refused write of AC7 and TC-E2-026-16 |
| storage product stub | RWB-PLT-TE012-APP | The draft write at `{container}/{caseId}/{documentId}/v1` and the removal of a failed draft |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 1, consumed 7 | The generate operation; the P6 catalog read, the P3 case read, the S2 treatment read, the P1 source-data read, the P3 parameters read, the P3 reference-list read and the P7 seal |
| Kafka | Published 1 event and 1 decision record; consumed 0 | `rwb.document.events.v1` and `rwb.decision-record.v1` |
| Temporal | 1 activity, no workflow of its own | `generate` on queue `rwb-document`; the `DocumentIntakeWorkflow` is named only |
| File | Blob through RWB-PLT-TE012-APP | The draft at `{container}/{caseId}/{documentId}/v1` and the merge snapshot beside it, removed on failure |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, module `document/generation`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| GeneratedDocumentController | Controller | The operation of 12.1; `Idempotency-Key` handling; error mapping to RFC 9457 problem responses with `messageId`; access check and scope |
| DocumentGenerator | Published interface | The generation entry point for the controller and for RWB-P5-E2017-APP, with `GenerationRequest` and `GenerationResult` |
| DocumentGenerationService | Service | Steps 2 to 8; BR1 to BR10; one transaction; removes the draft files on any failure |
| TemplateSelector | Service | Picks the current version by language, product group and date through the catalog contract (BR1, BR2, BR10) |
| MergeFieldResolver | Service | Calls each provider contract listed in its configuration and checks the required fields (BR3) |
| ValueFormatter | Service | Thai long dates in Buddhist Era, amounts with two decimals, amounts in Thai words (BR4) |
| TemplateRenderer | Service | Renders `{{merge_field_code}}` bodies to PDF/A-2b with the Thai fonts embedded |
| DocumentStoreClient | Client | Calls RWB-P5-E1024-APP with source GENERATED, state DRAFT and `write_once` false; never writes a file itself |
| DecisionRecordWriter | Service | Writes the D6.4 record and its merge snapshot reference through the decision-record library (DP-03) |
| DocumentHubRepository | Repository | Reads and writes `document` and reads `document_type` in `rwb_document` |
| IdempotencyRepository | Repository | Holds the request key and the first answer (DP-09) |

**Database.**

- Writes `document` with DF-DOC-001 to DF-DOC-011, DF-DOC-032, DF-DOC-033, the standard columns, and the two added columns `template_code` varchar(30) and `template_version` integer.
- Reads `document_type` in `rwb_document` for the document type and the retention class of each generated document.
- One migration in the per-service Flyway sequence (DP-15): step `V2026_1` adds `document.template_code` varchar(30) null, `document.template_version` integer null and the partial unique index `ux_document_draft_per_template ON document (treatment_id, template_id) WHERE state = 'DRAFT' AND is_active`.
- No other table is touched; `template`, `merge_field`, `decision_log_entry` and every P3, S2, P1, P7 table stay with their owners (DP-01).

**Configuration and reference data.**

- Template codes DIL-CONTRACT, DIL-CA, DIL-MORTGAGE and RES-AGREEMENT and the template-to-document-type mapping are data rows loaded by the reference data administrator (DL19, DL28); the codes are assumed and their identity is Not specified in the source documents (GAP-1023; ASM-1925).
- Parameters `GEN_IDEMPOTENCY_HOURS` 24, `GEN_MAX_TEMPLATES` 10 and `GEN_FONT` "TH Sarabun New", assumed and read through the parameters contract (DL28) (`ASM-1926`, `ASM-1929`).
- Decision code D6.4 with final call GENERATED, assumed; the LOV-DECISION list is owned by the data steward (`ASM-1927`).
- Feature flag `rwb.document.generation-engine`. Off: the operation answers 404 and `DocumentGenerator` refuses every call (`ASM-1929`).

**Build steps**

1. Add the Flyway step `V2026_1` with the two columns and the partial unique index; repository tests, including a second active DRAFT for the same treatment and template being refused.
2. Build `TemplateSelector` against a stub catalog for approved, unapproved, withdrawn, product-specific, all-product and future-version templates with a valid-from date; unit tests for BR1, BR2 and BR10.
3. Build `MergeFieldResolver` and its provider list against the three provider fakes; unit tests for a missing required field (BR3, AC2).
4. Build `ValueFormatter` with tests for the Buddhist Era long date and the amount in Thai words ("10 December 2569 BE", "1,250,000.00 baht (one million two hundred fifty thousand baht)").
5. Build `TemplateRenderer` with a sample Thai template; check PDF/A-2b conformance and the embedded fonts, and the damaged-body path of AC10.
6. Build `DocumentGenerationService`: the order of checks, the render, the draft write, the decision record, the store call per document, the outbox row and the removal of every draft on failure; integration test that a forced record failure leaves nothing (AC7, AC14, TC-E2-026-16).
7. Build `GeneratedDocumentController` with the `Idempotency-Key` handling, the concurrent case of AC9 and the status mapping of section 12 and section 14.
8. Add the contract test against RWB-P5-E2026-CON and the API tests for AC1 to AC14 and the access test TC-E2-026-15.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 removes the four cross-module reads of the legacy engine: the template catalog becomes the P6 contract, the case the P3 contract, the treatment the S2 contract and the party and collateral facts the P1 contract, each with a fake. DP-03 replaces the in-process decision-log writer with the local library inside the generation transaction. DP-05 is the legacy `AceSourceQuery` path: the customer name and the title-doc number come from the P1 contract and from no `v_ace_*` view of this service. DP-06 and DP-07 keep the three parameters and the two lists out of the code. DP-09 puts the event, the record and the idempotency row in the outbox and inbox library. DP-11 gives every consumed call one hop and a 2 s budget. DP-15 gives the service its own migration step. DP-19 puts the generated drafts on the case documents screen through the composite route.

**Done when.** The tests in section 16 pass, a sample deed in lieu set is checked by legal counsel against the approved wording, a three-document set is generated in SIT inside the 2 s budget per downstream, `rwb.document.DocumentStored.v1` is on the topic once per document with no personal data, and no draft file remains after a refused set.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-009 | A required merge field has no value (new) | {template} cannot be generated. {field} has no value on the case. |
| MSG-P5-010 | No current template version approved by Legal (new) | {template} has no version approved by Legal for {product} in {language}. |
| MSG-P5-011 | The treatment is not approved or not open (new) | Documents can be generated only for an approved {treatment} that is still open. |
| MSG-P6-003 | The template is withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P7-003 | The decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-001 | templateCodes is empty | Enter {field}. |
| MSG-GEN-004 | A concurrent request for the same treatment and template | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-006 | The renderer fails | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | Caller lacks Documents C | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the caller's scope | This case is not in your scope. |

Thai text for each message follows decision DL10.

HTTP mapping from the legacy section 12, unchanged: 401 for an unauthenticated caller (MSG-P4-001, whose wording is outside this story), 403 for MSG-P4-002, 404 for a case or a treatment that is not found or lies outside the scope (MSG-P4-003), 409 for MSG-P5-011 and MSG-GEN-004, 422 for MSG-P5-009, MSG-P5-010, MSG-P6-003 and MSG-GEN-001, 503 for MSG-P7-003 and MSG-GEN-006.

Delivery shape: every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. For MSG-GEN-006 the {system} value is "document generation" for a renderer failure and the name of the contract that failed for a downstream timeout. For MSG-P5-010 the {language} value is the `language` of the request and the {product} value is the product group of the case, read from the `rwb-case` answer.

### 15. Screens and states

No screen in this story. The restructuring officer reaches the engine through the screens of RWB-P5-E2017-APP, which calls the same operation and the same `generate` activity. Generated documents appear on SCR-30 Case documents in the list state with state DRAFT, through the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON). The DRAFT label, the review action and the send action belong to RWB-P5-E2017-APP; this story fixes only the state a generated document is created in.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-026-15 | Access | Component | RW-TEAMMGR user (Documents R) calls the generate operation; refused with MSG-P4-002 |
| TC-E2-026-01 | AC1, BR1, BR4, BR6 | End to end | Synthetic mortgage case and DIL treatment, template DIL-CONTRACT v2 |
| TC-E2-026-02 | AC2, BR3 | End to end | Case with no title deed number |
| TC-E2-026-03 | AC3, BR10 | End to end | Template v3 valid from 2026-12-15 |
| TC-E2-026-04 | AC4, BR1 | End to end | DIL-CA v1 not approved |
| TC-E2-026-05 | AC5, BR2 | End to end | DIL-MORTGAGE withdrawn |
| TC-E2-026-06 | AC6, BR5 | End to end | Treatment with no decision_log_id |
| TC-E2-026-07 | AC7, BR7 | End to end | Decision log stub refusing writes |
| TC-E2-026-08 | AC8, BR9 | End to end | Same Idempotency-Key twice |
| TC-E2-026-09 | AC9 | End to end | Two parallel requests |
| TC-E2-026-10 | AC10 | End to end | Damaged template body |
| TC-E2-026-11 | AC11, BR1 | End to end | Hire purchase case, mortgage-only template |
| TC-E2-026-12 | AC12 | End to end | Case of team HP-NE, officer of team FCR-BKK |
| TC-E2-026-13 | AC13 | End to end | Three current templates |
| TC-E2-026-14 | AC14, BR8 | End to end | Three templates, DIL-CA not approved |
| TC-E2-026-16 | Principle 5 | NFR | Decision log write forced to fail during a three-document set; no document, no file, MSG-P7-003, incident raised |

The legacy level System maps to End to end, Access to Component and Resilience to NFR. The integration harness copies of these test cases end in `-ITG` and belong to RWB-ITG-E2026-ITG, where the real P6, P3, S2, P1 and P7 services replace the fakes. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: template codes, merge fields, formats, the type mapping, the decision code, the parameters and the font are data rows or parameters.
- No personal data in events, workflow inputs, payloads, logs, tests or prompts: merge values and the merge snapshot are never logged; tests use synthetic parties; the clear ID number is used only at render time and exists only inside the stored PDF.
- No read of another service's tables (DP-01): the template catalog, the case, the treatment, the party and collateral facts, the parameters, the lists and the central ledger come through published contracts. ACE data is reached only through the owner's contract or a `v_ace_*` view, and this service reads no view.
- No document is produced from a template version without `approved_by_legal = true`, and no template version and no merge field is held in this service's schema.
- No clear ID number outside the rendered PDF, and no merge snapshot in a log, an event or a decision-record payload: the record carries the reference only.
- The engine writes no blob itself: every draft goes through RWB-P5-E1024-APP at `{container}/{caseId}/{documentId}/v1` and is removed when the set is refused.
- The decision record is written in the same transaction as the document rows and the outbox rows; a failure stores nothing and raises an incident (R-UNI-39, R-UNI-40).
- The engine is idempotent twice over: `Idempotency-Key` on the POST and the partial unique index on treatment, template and DRAFT state.
- One evaluator if any: this story evaluates no rule package, so no Drools kit is loaded and no rule row is read.
- The feature flag `rwb.document.generation-engine` removes the capability without a rollback of the schema.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-012 | Contracts, credit applications and mortgage documents generated from approved templates with no re-keying | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-OCC-07 | 7.3 Negotiate settlement or deed in lieu; 13 Manage documents and correspondence | R-DIL-14, R-DIL-16, R-UNI-39, R-UNI-40 | TC-E2-026-01, TC-E2-026-02, TC-E2-026-06 to TC-E2-026-16 |
| REQ-OCC-002 | Letter templates versioned, with the Legal approval recorded against the version | Business Requirements Program, section 5.6; Epic 2, section 3.5 | FEAT-OCC-07 | 13 Manage documents and correspondence | R-LIT-03, R-LIT-04, R-LIT-06, R-UNI-38 | TC-E2-026-03 to TC-E2-026-05, TC-E2-026-11 |

| Legacy reference | Where it is kept |
|---|---|
| Template codes DIL-CONTRACT, DIL-CA, DIL-MORTGAGE and RES-AGREEMENT | Preconditions, sections 1, 3, 7, 13, 16 |
| Template-to-document-type mapping (CONTRACT, CREDIT_APPROVAL, MORTGAGE_DOCUMENT) | Preconditions, sections 1, 3, 7, 11 |
| Event DocumentStored (EV-16) | Sections 1, 4, 12.3, 17 |
| Decision code D6.4 and decision D6.5 | Metadata, sections 1, 4, 8, 12.3, 13, 14, 18 |
| MSG-P5-009, MSG-P5-010, MSG-P5-011, MSG-P6-003, MSG-P7-003, MSG-GEN-001, MSG-GEN-004, MSG-GEN-006, MSG-P4-002, MSG-P4-003 | Section 14, exception paths |
| Rules R-DIL-14, R-DIL-16, R-LIT-03, R-LIT-04, R-LIT-06, R-UNI-38, R-UNI-39, R-UNI-40 | Sections 2, 8, 9, 18 |
| Controls CTL-11, CTL-14 | Sections 2, 8, 18 |
| NFR-006 (1,000 deed in lieu cases a month in 2027) | Section 2 |
| Legacy key RWB-E2-026, story RWB-P5-E2026-APP, self-tests TC-E2-026-01 to TC-E2-026-16 | Metadata, sections 3, 12, 16 |

### 19. Out of scope

Legacy out-of-scope items of RWB-E2-026:

- The generation, review and send screens (RWB-E2-017).
- The e-signature flow (RWB-E2-018).
- Rule-driven generation when the deed in lieu route reaches TRANSFER_PRICE_SET (FEAT-TRT-18, Epic 3); this story supplies the operation that path calls.
- Template upload and Legal approval (RWB-E1-034) and the merge field catalog (RWB-E1-046).
- Debt sale agreements and notices (FEAT-DBS-10, Epic 6).

Target additions:

- The generation, review and send screens and the overrides form, including `POST /documents/{documentId}/regenerate`: RWB-P5-E2017-APP and RWB-P5-E2017-CON.
- The e-signature flow: RWB-P5-E2018-APP.
- Template upload and Legal approval within the target architecture: P6 `rwb-comms` and RWB-P5-E1046-APP, consumed here through the catalog contract only.
- Retention periods, the retention Schedule and disposal: RWB-P5-E1017-APP.
- The published contract artefacts of this service, their fakes and their versioning: RWB-P5-E2026-CON; the cross-service proof: RWB-ITG-E2026-ITG.
- The Helm chart, the retry policy values, the topic and DLT provisioning, the metrics, the alerts and the runbook.
