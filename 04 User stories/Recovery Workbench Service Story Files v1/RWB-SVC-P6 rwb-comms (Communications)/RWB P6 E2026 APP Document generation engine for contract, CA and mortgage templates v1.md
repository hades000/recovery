# RWB-P6-E2026-APP Document generation engine for contract, CA and mortgage templates

SCB Collections and Recovery. Henka Group, 22 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E2026-APP |
| Work type | APP |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-026 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP-01, DP-03, DP-05, DP-06, DP-07, DP-09, DP-11, DP-15, DP-19 |
| Parallel lane | L-P6-Q |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P5-E2026-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (FR-P6-001, FR-P6-002, FR-P6-003, FR-P6-004, FR-P6-005, FR-P6-012, FR-P6-014) |
| Status | Draft (realignment v1) |

| Version | Date | Change | Tool |
|---|---|---|---|
| v1 | 22 November 2026 | D-RCV-60 realignment of RWB-E2-026 into rwb-comms | T3 Code / OpenCode / DeepSeek v4.1 Flash |

### 1. Story

As a **restructuring officer (FCR)**, I want **the rwb-comms generation engine that fills the contract, credit approval and mortgage templates from the case facts with the merge field catalog and the Legal-approved template versions**, so that **the documents the screens generate are correct and versioned, and no other service reads the template or merge field tables of rwb-comms**.

The engine owns templates, merge fields, selection and rendering. The document record, the stored file and the write-once copy belong to rwb-document (P5); the decision record goes to the local decision-record library and `rwb.decision-record.v1`.

### 2. Business rationale

Deed in lieu and restructure document sets are typed today from the case file into Word templates, and a wrong amount or an old template wording reaches the customer. This engine fills each Legal-approved template version from the case facts, refuses to produce a document with a missing value or an unapproved template, and records which template version and which inputs produced each document. It meets REQ-DCM-012 and REQ-OCC-002, applies control CTL-14 to the deed in lieu and restructure documents, and supports the target of 1,000 deed in lieu cases a month in 2027 (NFR-006).

In the microservice layout the template and merge field catalog is the asset of rwb-comms, so the generation decision sits with the owner of that data; the byte store and the document lifecycle (DRAFT, REVIEWED, SENT, write-once) stay with rwb-document. The split keeps one writer per table and lets another workbench reuse the engine through one REST contract.

### 3. Preconditions

- rwb-comms holds the template catalog and the merge field catalog as data (`rwb_comms.template`, `rwb_comms.merge_field`) with its own Flyway baseline, and the Legal approval record is a column set on the template version.
- Templates DIL-CONTRACT, DIL-CA, DIL-MORTGAGE and RES-AGREEMENT are loaded in Thai with approved_by_legal = true (template codes assumed, DL28).
- The template-to-document-type mapping is reference data of rwb-document: DIL-CONTRACT to CONTRACT, DIL-CA to CREDIT_APPROVAL, DIL-MORTGAGE to MORTGAGE_DOCUMENT, RES-AGREEMENT to CONTRACT (assumed, DL19).
- The case has a treatment of type DEED_IN_LIEU or RESTRUCTURE with decision_log_id set (approved at D6.4) and no outcome yet.
- The merge field providers of P3 (case), S2 (treatment) and P1 (party, collateral) are listed in the MergeFieldResolver configuration as contract clients.
- The caller holds Documents C (RW-RESTRUCT or RW-CASEOWN), or is the service identity SY-CASEWF for rule-driven generation from Epic 3.
- The rwb-document contract and its fake (RWB-P5-E2026-CON) are published; the story builds against them and never against rwb_document tables.

### 4. Flow

1. Restructuring officer or SY-CASEWF: requests generation for a case, a treatment and a list of template codes on `POST /api/recovery/comms/v1/cases/{caseId}/generated-documents` with an Idempotency-Key.
2. System: reads the treatment through the rwb-treatment (S2) contract and checks it is approved and open.
3. System: for each template code, reads the current version from `rwb_comms.template` for the language and product group: approved by Legal, active, highest version valid on the request date.
4. System: reads the merge codes of that version from `rwb_comms.merge_field` and asks each owning service's contract (P3, S2, P1) for the values.
5. System: checks that every required merge field has a value; formats each value by its catalog format (Thai long date in Buddhist Era, amount to two decimals, amount in Thai words).
6. System: reads the template body through the rwb-document file contract and renders it to PDF/A-2b with the Thai font named in the parameters.
7. System: calls the rwb-document contract once per document to create the DRAFT document row with template code, template version and treatment ID, and to store the file; the service counts the calls and treats the set as whole or not at all.
8. System: publishes one decision record (decision code D6.4, inputs reference to the merge snapshot, per document the template code and version) through the local library and the outbox to `rwb.decision-record.v1`.
9. System: returns the generated documents; the screens of RWB-E2-017 show them for review. If any step fails, no document is created in rwb-document and any draft file written in this request is removed.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A required merge field has no value | Generation stops; nothing stored; the field is named | MSG-P5-009 | AC2 |
| X2 | The current template version is not approved by Legal | Generation stops; nothing stored | MSG-P5-010 | AC4 |
| X3 | The template is withdrawn | Generation stops; a task goes to the restructuring officer through the rwb-case contract, as R-LIT-04 does for notices | MSG-P6-003 | AC5 |
| X4 | The treatment is not approved, is closed, or is of another type | 409; nothing stored | MSG-P5-011 | AC6 |
| X5 | The decision record cannot be published | Nothing stored; draft file removed; incident raised | MSG-P7-003 | AC7 |
| X6 | The same request is repeated with the same Idempotency-Key | The first result is returned; nothing new is stored | None | AC8 |
| X7 | Two requests for the same treatment and template run at once | One succeeds; the other gets 409 | MSG-GEN-004 | AC9 |
| X8 | A template body cannot be rendered | 503; nothing stored; incident raised | MSG-GEN-006 | AC10 |
| X9 | No template exists for the product group or language | Generation stops and names the template | MSG-P5-010 | AC11 |
| X10 | The case is outside the caller's scope | 404 | MSG-P4-003 | AC12 |
| X11 | One template of a set fails its check | Nothing of the set is stored | MSG-P5-010 | AC14 |
| X12 | The caller lacks Documents C | 403 | MSG-P4-002 | TC-E2-026-15 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the rwb-document contract fake (RWB-P5-E2026-CON); the P3, S2 and P1 reads are contract clients with fakes; no build dependency in the lane (ASM-3978) |
| Negotiable | Templates, merge fields, formats, type mapping and font are data and parameters, owned by Legal and the product owner |
| Valuable | Ends re-keying of deed in lieu and restructure documents, and fixes template ownership with the service that holds the catalog |
| Estimable | One service, one renderer, one resolver, one endpoint, one decision record, no screen |
| Small | Fits in two weeks with its tests |
| Testable | Each AC is one contract or component test with synthetic case data and recorded contract payloads |

### 7. Acceptance criteria

```gherkin
Feature: Document generation engine for contract, CA and mortgage templates

  Background:
    Given case "RW-2026-000301" with product group "MORTGAGE"
    Given treatment "TRT-0301" of type "DEED_IN_LIEU" on that case with decision_log_id set and no outcome
    Given rwb_comms.template holds "DIL-CONTRACT" version 2 in Thai for "MORTGAGE" with approved_by_legal true
    Given rwb_comms.merge_field holds case_no, borrower_name, title_doc_no, transfer_price and contract_date for "DIL-CONTRACT" version 2
    Given a restructuring officer with role RW-RESTRUCT in scope of the case

  Scenario: AC1 Generate (new, D-RCV-60)
    Given the case facts give transfer_price 1250000.00, title_doc_no "12345" and contract_date 2026-12-10
    Given the rwb-document contract mock returns document "DOC-0311" in state "DRAFT" with document_type "CONTRACT"
    When the engine runs for treatment "TRT-0301" and template "DIL-CONTRACT"
    Then the response is 201 with document "DOC-0311" carrying templateCode "DIL-CONTRACT", templateVersion 2 and treatmentId "TRT-0301"
    Then the rendered PDF shows "1,250,000.00 baht (one million two hundred fifty thousand baht)" and "10 December 2569 BE"
    Then one decision record is published to rwb.decision-record.v1 with decision code "D6.4" and an inputs reference to the merge snapshot
    Then rwb-document received one create call and no document row was written in rwb_comms

  Scenario: AC2 Missing field (new, D-RCV-60)
    Given the case has no title_doc_no
    When the engine runs for template "DIL-CONTRACT"
    Then the response is 422 with MSG-P5-009 naming "DIL-CONTRACT" and "title_doc_no"
    Then no create call reaches rwb-document and no decision record is published

  Scenario: AC3 Version (new, D-RCV-60)
    Given "DIL-CONTRACT" version 3 is approved by Legal and valid from 2026-12-15 in rwb_comms.template
    Given the rwb-document contract mock returns document "DOC-0310" generated on 2026-12-10 from version 2
    When the engine runs on 2026-12-15
    Then the new document is created with templateVersion 3
    Then "DOC-0310" still carries templateVersion 2 and its file opens
    Then version 2 stays readable in rwb_comms.template

  Scenario: AC4 A version not approved by Legal is refused (new, D-RCV-60)
    Given template "DIL-CA" has only version 1 with approved_by_legal false
    When the engine runs for template "DIL-CA"
    Then the response is 422 with MSG-P5-010 naming "DIL-CA" version 1
    Then nothing is created in rwb-document

  Scenario: AC5 A withdrawn template holds generation (new, D-RCV-60)
    Given template "DIL-MORTGAGE" version 1 is withdrawn and no later version is approved
    Given the rwb-case contract mock accepts one task for the requesting officer
    When the engine runs for template "DIL-MORTGAGE"
    Then the response is 422 with MSG-P6-003 naming "DIL-MORTGAGE"
    Then one task is raised to the restructuring officer who requested it and nothing is created in rwb-document

  Scenario: AC6 A treatment that is not approved is refused (new, D-RCV-60)
    Given the rwb-treatment contract mock returns treatment "TRT-0302" of type "DEED_IN_LIEU" with no decision_log_id
    When the engine runs for treatment "TRT-0302"
    Then the response is 409 with MSG-P5-011
    Then nothing is created in rwb-document and no decision record is published

  Scenario: AC7 The decision record cannot be published (new, D-RCV-60)
    Given the rwb.decision-record.v1 publisher is unavailable for the request
    When the engine runs for treatment "TRT-0301" and template "DIL-CONTRACT"
    Then the response is 503 with MSG-P7-003
    Then no DRAFT document stays in rwb-document for "TRT-0301" and the draft file is removed
    Then the message sits in the retry topic and an incident is raised as in R-UNI-39

  Scenario: AC8 A repeated request (new, D-RCV-60)
    Given a request with Idempotency-Key "K-0301" created document "DOC-0311"
    When the same request with Idempotency-Key "K-0301" arrives again
    Then the response is 201 with document "DOC-0311"
    Then rwb-document received one create call and one decision record exists

  Scenario: AC9 Two requests at the same time (new, D-RCV-60)
    Given two requests for treatment "TRT-0301" and template "DIL-CONTRACT" with different keys arrive together
    When both run
    Then one returns 201 with one DRAFT document
    Then the other returns 409 with MSG-GEN-004
    Then rwb-document received one create call

  Scenario: AC10 A template body that cannot be rendered (new, D-RCV-60)
    Given the body of "DIL-CONTRACT" version 2 is a damaged file
    When the engine runs
    Then the response is 503 with MSG-GEN-006 naming "document generation"
    Then nothing is created in rwb-document and an incident is raised

  Scenario: AC11 No template for the product group (new, D-RCV-60)
    Given template "DIL-CONTRACT" exists only for product group "MORTGAGE"
    Given case "RW-2026-000305" has product group "HIRE_PURCHASE"
    When the engine runs for that case and "DIL-CONTRACT"
    Then the response is 422 with MSG-P5-010 naming "DIL-CONTRACT" for "HIRE_PURCHASE"

  Scenario: AC12 A case outside the caller's scope (new, D-RCV-60)
    Given the rwb-access contract mock reports case "RW-2026-000306" outside the officer's team scope
    When the officer requests generation for that case
    Then the response is 404 with MSG-P4-003
    Then no template is selected and nothing is created in rwb-document

  Scenario: AC13 A set of three documents in one request (new, D-RCV-60)
    Given templates "DIL-CONTRACT", "DIL-CA" and "DIL-MORTGAGE" are current and approved
    Given the rwb-document contract mock returns DRAFT documents of types "CONTRACT", "CREDIT_APPROVAL" and "MORTGAGE_DOCUMENT"
    When the engine runs for treatment "TRT-0301" with the three template codes
    Then the response is 201 with three documents of those types
    Then rwb-document received three create calls and one decision record names the three template codes and versions

  Scenario: AC14 A set is stored whole or not at all (new, D-RCV-60)
    Given templates "DIL-CONTRACT" and "DIL-MORTGAGE" are current and approved
    Given template "DIL-CA" has no version approved by Legal
    When the engine runs for treatment "TRT-0301" with the three template codes
    Then the response is 422 with MSG-P5-010 naming "DIL-CA"
    Then rwb-document received no create call and no decision record is published
```

The legacy AC1 to AC14 of RWB-E2-026 are re-stated above for the rwb-comms deliverable; document rows, files and EV-16 now belong to rwb-document, so every cross-service step is asserted against the contract mock.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A document is generated only from the current template version: approved by Legal, active and valid on the request date; the most specific product group match wins over a template for all products | DF-REF-047, DF-REF-049, DF-REF-051; CTL-14; R-LIT-03 |
| BR2 | A withdrawn template with no approved successor holds generation and raises a task | R-LIT-04; R-LIT-06 |
| BR3 | Every required merge field must have a value; otherwise nothing is generated and the field is named | Merge field catalog (RWB-E1-046); FEAT-OCC-07 |
| BR4 | Values are formatted by the catalog format: Thai long date in Buddhist Era, amounts with two decimals and in Thai words | Merge field catalog; Principle 1 |
| BR5 | Generation is allowed only for an approved, open treatment of type DEED_IN_LIEU or RESTRUCTURE | DF-TRT-003, DF-TRT-004, DF-TRT-013; R-DIL-14; R-DIL-16 |
| BR6 | A generated document carries the template code, the template version, the treatment ID and the source GENERATED; rwb-document creates it as a DRAFT and it is not write-once until it is sent (RWB-E2-017) | DF-DOC-005, DF-DOC-010; CTL-12 |
| BR7 | Generation whose decision record cannot be published does not proceed; the record is written through the local library and the outbox | Principle 5; R-UNI-39; CTL-06; DP-03, DP-09 |
| BR8 | A set is generated whole or not at all | Events rule "Transactions" |
| BR9 | A repeat with the same Idempotency-Key returns the first result | R-UNI-40 |
| BR10 | A new template version applies to documents generated from its valid-from date; earlier documents keep their version | R-UNI-38 |
| BR11 | A national ID number is filled from the token service at render time; the clear value exists only inside the generated PDF and never in a log, an event or a workflow input | DF-PTY-007; CTL-11; DL26 |

### 9. State transitions

None at case level: this story does not change a case status. The only state it starts is the document state DRAFT, held by rwb-document.

| From | Event | Condition | To |
|---|---|---|---|
| (none) | Generation requested | BR1, BR3 and BR5 pass and the decision record is published | document DRAFT (rwb-document) |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT, restructuring officer (FCR) | Requests generation for a treatment in scope (Documents C) |
| RW-CASEOWN, case owner | Requests generation for a treatment in scope (Documents C) |
| SY-CASEWF, case workflow module | Calls the generation endpoint for rule-driven generation from Epic 3 (R-DIL-14, R-DIL-16) |
| SY-DECLOG, decision record library | Publishes the decision record (service side; no person) |
| RW-LEGAL, legal counsel | Approves template versions (Documents CRUA); approval is a precondition, not part of this story |
| RW-TEAMMGR, team manager | Reads generated documents (Documents R); cannot generate |

No approval level from the delegation of authority applies in this story. The treatment itself was approved at D6.4 before generation.

### 11. Data

| BR Field ID | Entity | Field | Read or write | Where |
|---|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read | P3 contract |
| DF-CAS-002 | recovery_case | case_no | Read | P3 contract |
| DF-CAS-003 | recovery_case | product_group | Read | P3 contract |
| DF-CAS-004 | recovery_case | primary_person_key | Read | P3 contract |
| DF-TRT-001 | treatment | id | Read | S2 contract |
| DF-TRT-003 | treatment | decision_log_id | Read | S2 contract |
| DF-TRT-004 | treatment | treatment_type | Read | S2 contract |
| DF-TRT-007 | treatment | offer_amount | Read | S2 contract |
| DF-TRT-013 | treatment | outcome | Read | S2 contract |
| DF-ACE-057 | v_ace_customer | first_name | Read | P1 contract |
| DF-ACE-058 | v_ace_customer | last_name | Read | P1 contract |
| DF-ACE-197 | v_ace_collateral_detail | title_doc_no | Read | P1 contract |
| DF-REF-045 to DF-REF-051 | template | all fields | Read | own schema rwb_comms |
| DF-REF-252 to DF-REF-260 | merge_field | all fields | Read | own schema rwb_comms |
| DF-DOC-001 to DF-DOC-011 | document | all fields | Write | rwb-document contract |
| DF-DOC-032 | document | template_id | Write | rwb-document contract |
| DF-DOC-033 | document | treatment_id | Write | rwb-document contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write | decision-record library and topic |

Field IDs are those in the Logical Data Model and Data Dictionary. rwb-comms writes no row into any table of rwb-document, rwb_case or rwb_decision.

### 12. Contract

### 12.1 REST operations provided

| Method | Path | Purpose | Auth | Errors |
|---|---|---|---|---|
| POST | `/api/recovery/comms/v1/cases/{caseId}/generated-documents` | Generate one to ten documents for a treatment from approved template versions | Documents, right C, scope applied | 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 409 MSG-P5-011, MSG-GEN-004; 422 MSG-P5-009, MSG-P5-010, MSG-P6-003, MSG-GEN-001; 503 MSG-P7-003, MSG-GEN-006 |

Request: GenerateRequest — treatmentId (uuid, required), templateCodes (array of string, 1 to 10, required), language (TH or EN, default TH); header Idempotency-Key (required), kept 24 hours. Response 201 DocumentPage: documentId, templateCode, templateVersion, documentType, state.

The endpoint is a new addition to the P6 inventory (legacy additions file; prepared by RWB-E2-026) and carries no API-P6-nnn ID (GAP-2394; ASM-3977). The other ten owned operations (template admin, notices, messages, signature requests) are delivered by the E1 template story and the notice, message and signature stories of this epic.

### 12.2 REST operations consumed

| Operation | Owner | Contract story | Purpose | Timeout |
|---|---|---|---|---|
| Create a DRAFT document and store its file — path and payload per the P5 contract (Not specified in the source documents (GAP-2393; ASM-3976)) | rwb-document (P5) | RWB-P5-E2026-CON | One call per document; document type, template code and version, treatment ID, source GENERATED | 2 s |
| Read a template body file | rwb-document (P5) | RWB-P5-E2026-CON | Render input for the selected version | 2 s |
| Read the document-type mapping | rwb-document (P5) | RWB-P5-E2026-CON | Template code to document type (legacy RWB-E1-025, DL19) | 2 s |
| Read the treatment summary | rwb-treatment (S2) | S2 treatment read contract | BR5 approval and type check, offer amount | 2 s |
| Read case facts | rwb-case (P3) | RWB-P3-E1042-CON; RWB-P3-E1043-CON | Case, product group, party key; template-to-type reference data | 2 s |
| Read customer and collateral values | rwb-source-data (P1) | rwb-source-data contract | Merge values from the ACE views, masked by policy | 2 s |
| Raise a task for a withdrawn template | rwb-case (P3) | RWB-P3-E1042-CON | X3 and AC5 | 2 s |
| Authorise the request | rwb-access (P4) | RWB-P4-E1037-CON | Capability and scope, cached permission data | 2 s |

### 12.3 Events published

| Event | Topic | Trigger | Payload (no PII) |
|---|---|---|---|
| DecisionRecorded (shared record contract) | `rwb.decision-record.v1` | Each successful set and each refusal under X1 to X11 | decision code, rule IDs, case ID, treatment ID, template codes and versions, merge snapshot key |

This story publishes no comms-owned event: EV-13 NoticeGenerated, EV-14 NoticeDispatched and EV-15 NoticeDelivered belong to the notice stories, and EV-16 DocumentStored is published by rwb-document. Publication is through the outbox (DP-09) with a retry topic and `rwb.decision-record.v1.dlt`.

### 12.4 Events consumed

| Event | Topic | Action |
|---|---|---|
| None | None | The engine is called synchronously; it reads no event |

### 12.5 Workflows and activities

| Item | Type | Note |
|---|---|---|
| None | None | Generation is one synchronous REST operation; no Temporal workflow, child workflow or activity is started. NoticeDispatchWorkflow of this service is not used |

### 12.6 Schedules

None. JOB-10 of this service belongs to notice dispatch; this story has no schedule and no timer.

### 12.7 Tables owned

| Table | Schema | Note |
|---|---|---|
| template | rwb_comms | Template version, language, product group, approval by Legal, valid-from, body reference, merge codes. Unique key on (template_code, template_version) replaces the legacy uk_template on template_code alone, which AC3 needs (raised with the P6 owner of RWB-E1-046) |
| merge_field | rwb_comms | Merge code, source entity and field, required flag, personal-data flag, catalog version, valid-from |

### 12.8 Contract fakes

| Fake | Serves | Used by |
|---|---|---|
| rwb-document fake (RWB-P5-E2026-CON) | Document create, body read, type mapping; records every call and can refuse a create | AC1, AC3, AC7, AC8, AC9, AC13, AC14 |
| rwb-treatment fake | Treatment summary, approved and open or not | AC3, AC6 |
| rwb-case fake | Case facts, task create, parameters and reference data | AC1, AC5, AC11 |
| rwb-source-data fake | Customer and collateral merge values | AC1, AC2 |
| rwb-access fake | Capability and object scope | AC12, TC-E2-026-15 |
| decision-record fake | In-memory record store with a refusal switch | AC7, TC-E2-026-16 |

### 12.9 Call-type summary

| Call type | Used | Detail |
|---|---|---|
| REST | Yes | One hop per call from gateway-bff; the engine calls P5, P3, P4, P1 and S2 with a 2 s timeout and a circuit breaker per downstream |
| Kafka | Yes | `rwb.decision-record.v1` through the outbox; retry and `.dlt` topics |
| Temporal | No | None |
| File | Yes | Template body read and PDF write through the rwb-document contract, claim-check style with the file ID in the message |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.comms.generation`.

| Component | Type | Microservice responsibility |
|---|---|---|
| GeneratedDocumentController | Controller | The 12.1 endpoint; Idempotency-Key; error mapping to problem responses |
| GenerationService | Service | Steps 2 to 8 of §4 in one unit of work; refuses the whole set on any failure; removes draft files |
| TemplateSelector | Service | Selects the version from `rwb_comms.template` by language, product group and date (BR1, BR2); never reads another schema (DP-01) |
| MergeFieldCatalog | Service | Reads the merge codes of the selected version from `rwb_comms.merge_field` (BR3) |
| MergeFieldResolver | Service | Calls the P3, S2 and P1 contract clients in parallel; checks required values |
| ValueFormatter | Service | Thai long date in Buddhist Era, amounts to two decimals, amounts in Thai words (BR4) |
| TemplateRenderer | Service | Merges `{{merge_field_code}}` tags, renders PDF/A-2b with the parameter font, reads the body through the P5 contract |
| DocumentDraftClient | Client | One create call per document to RWB-P5-E2026-CON; counts calls; compensates on failure (BR6, BR8) |
| DecisionRecordPublisher | Publisher | Local decision-record library and outbox to `rwb.decision-record.v1` (DP-03, DP-09) |
| GenerationRepository | Repository | Template and merge field reads; request key and request lock |
| ConfigClient | Client | Parameters and reference data through the P3 contracts (DP-06, DP-07) |
| TaskClient | Client | Raises the task for a withdrawn template through the rwb-case contract |

**Database.** Per-service Flyway sequence in `rwb_comms` (DP-15): template and merge_field with the standard record columns, the unique key on (template_code, template_version), and an index on (template_code, language, product_group, valid_from). The request key and the request lock of X6 and X7 are kept in `rwb_comms`; the table for them is Not specified in the source documents (GAP-2393; ASM-3976). No Flyway migration touches another schema.

**Configuration and reference data.** Parameters through the rwb-case contract (DP-06): GEN_IDEMPOTENCY_HOURS 24, GEN_MAX_TEMPLATES 10, GEN_FONT "TH Sarabun New" (values assumed). Reference data through the same owner (DP-07): language list TH and EN, product groups, and the template-to-document-type mapping held by rwb-document (DL19). Templates and merge fields stay data rows of this service, owner legal counsel (DL28).

**Build steps.**
1. Flyway baseline of `rwb_comms` with template and merge_field; repository and unique-key tests.
2. TemplateSelector against the own-schema tables: approved, unapproved, withdrawn, product-specific, all-product and valid-from cases.
3. MergeFieldCatalog and MergeFieldResolver with contract fakes; test the missing required field.
4. ValueFormatter with Buddhist Era date and Thai-words amount tests.
5. TemplateRenderer with a sample Thai template; check PDF/A-2b conformance and the embedded font.
6. GenerationService: order of checks, render, P5 create calls, decision record, compensation, all-or-nothing set.
7. Controller with Idempotency-Key, request lock and the 12.1 error mapping.
8. Contract test of the new endpoint against RWB-P5-E2026-CON and the note of the addition in the P6 API specification.

**Feature flag.** `rwb.comms.generation-engine`. Off: the endpoint returns 404.

**Done when:** the tests in section 16 pass; a sample deed in lieu set is checked by legal counsel against the approved wording; no rwb_document, rwb_case or rwb_decision table is read or written by the service.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-009 | A required merge field has no value (new) | {template} cannot be generated. {field} has no value on the case. |
| MSG-P5-010 | No current template version approved by Legal (new) | {template} has no version approved by Legal for {product} in {language}. |
| MSG-P5-011 | The treatment is not approved or not open (new) | Documents can be generated only for an approved {treatment} that is still open. |
| MSG-P6-003 | The template is withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P7-003 | The decision record could not be published | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-001 | templateCodes is empty | Enter {field}. |
| MSG-GEN-004 | A concurrent request for the same treatment and template | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-006 | The renderer or a downstream is unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | Caller lacks Documents C | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the caller's scope | This case is not in your scope. |

Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story. The restructuring officer reaches the engine through the screens of RWB-E2-017, which the gateway-bff calls through the composite route of RWB-PLT-N001-CON (DP-19). Generated documents appear on SCR-30 Case documents in the list state with state DRAFT, read from rwb-document.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-026-15 | Access | Integration | RW-TEAMMGR user (Documents R) calls POST generated-documents; refused with MSG-P4-002 |
| TC-E2-026-01 | AC1, BR1, BR4, BR6 | Component | Synthetic mortgage case and DIL treatment, template DIL-CONTRACT v2 in rwb_comms.template |
| TC-E2-026-02 | AC2, BR3 | Component | Case with no title deed number |
| TC-E2-026-03 | AC3, BR10 | Component | Template v3 valid from 2026-12-15; DOC-0310 from version 2 |
| TC-E2-026-04 | AC4, BR1 | Contract | DIL-CA v1 not approved |
| TC-E2-026-05 | AC5, BR2 | Contract | DIL-MORTGAGE withdrawn; rwb-case fake accepts a task |
| TC-E2-026-06 | AC6, BR5 | Contract | S2 fake returns a treatment with no decision_log_id |
| TC-E2-026-07 | AC7, BR7 | Component | Decision-record publisher refusing; P5 fake records no create |
| TC-E2-026-08 | AC8, BR9 | Component | Same Idempotency-Key twice |
| TC-E2-026-09 | AC9 | Component | Two parallel requests, request lock in rwb_comms |
| TC-E2-026-10 | AC10 | Component | Damaged template body |
| TC-E2-026-11 | AC11, BR1 | Contract | Hire purchase case, mortgage-only template |
| TC-E2-026-12 | AC12 | Contract | rwb-access fake reports a case outside the team scope |
| TC-E2-026-13 | AC13 | Contract | Three current templates; P5 fake returns three DRAFT documents |
| TC-E2-026-14 | AC14, BR8 | Contract | Three templates, DIL-CA not approved; P5 fake records no create |
| TC-E2-026-16 | Principle 5 | NFR | Decision record forced to fail during a three-document set; no document, no file, MSG-P7-003, incident raised |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID; the Level column replaces the legacy Level wording and the cross-service steps use the contract fakes of 12.8.

### 17. Guardrails

- No business value in code: template codes, merge codes, formats, type mapping, language list and font are data rows or parameters.
- No PII in events, workflow inputs or logs: merge values and the merge snapshot are never logged; tests use synthetic parties; the clear national ID number is used only at render time and exists only inside the PDF.
- ACE data only through the owner's contract: case, treatment, party and collateral values come from P3, S2 and P1, never from an ACE table and never from another service's schema.
- No document is produced from a template version without approved_by_legal = true; no row of rwb_document is read or written, only its contract.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-012 | Contracts, credit applications and mortgage documents generated from approved templates with no re-keying | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-OCC-07 | 7.3 Negotiate settlement or deed in lieu; 13 Manage documents and correspondence | R-DIL-14, R-DIL-16, R-UNI-39, R-UNI-40 | TC-E2-026-01, TC-E2-026-02, TC-E2-026-06 to TC-E2-026-16 |
| REQ-OCC-002 | Letter templates versioned, with the Legal approval recorded against the version | Business Requirements Program, section 5.6; Epic 2, section 3.5 | FEAT-OCC-07 | 13 Manage documents and correspondence | R-LIT-03, R-LIT-04, R-LIT-06, R-UNI-38 | TC-E2-026-03 to TC-E2-026-05, TC-E2-026-11 |

### 19. Out of scope

- The generation, review and send screens (RWB-E2-017).
- The e-signature flow (RWB-E2-018).
- Rule-driven generation when the deed in lieu route reaches TRANSFER_PRICE_SET (FEAT-TRT-18, Epic 3).
- Template upload and Legal approval screens and the merge field catalog maintenance screens; this story reads the rows (legacy RWB-E1-034, RWB-E1-046). Also the document record, the file store, the write-once copy and the DocumentStored event, which belong to rwb-document (RWB-P5-E2026-CON).
- Debt sale agreements and notices (FEAT-DBS-10, Epic 6).
