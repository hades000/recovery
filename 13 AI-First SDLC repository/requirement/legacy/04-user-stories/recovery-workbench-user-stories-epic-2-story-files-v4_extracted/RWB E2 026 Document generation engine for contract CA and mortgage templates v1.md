<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 026 Document generation engine for contract CA and mortgage templates v1.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 026 Document generation engine for contract CA and mortgage templates v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-026 Document generation engine for contract, CA and mortgage templates

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-026 |
| Epic | E2, release 31 December 2026 |
| Module | P5 Document hub |
| Feature | FEAT-OCC-07 Generate contract, credit approval and mortgage documents |
| Requirement IDs | REQ-DCM-012, REQ-OCC-002 |
| BRD section | Business Requirements Epic 2, section 3.5 |
| L3 process | 7.3 Negotiate settlement or deed in lieu; 13 Manage documents and correspondence |
| Decision | D6.4, D6.5 |
| Priority | Must |
| Depends on | RWB-E1-046, RWB-E1-034, RWB-E1-024, RWB-E1-027 |
| Status | Ready for build |

## 1. Story

As a **restructuring officer (FCR)**, I want **the generation engine that fills the contract, credit approval and mortgage templates from the case facts with the merge field catalog and Legal-approved versions**, so that **the documents the screens generate are correct and versioned**.

## 2. Business rationale

Deed in lieu and restructure document sets are typed today from the case file into Word templates, and a wrong amount or an old template wording reaches the customer. This engine fills each Legal-approved template version from the case facts held in the Workbench, refuses to produce a document with a missing value or an unapproved template, and records which template version and which inputs produced each document. It meets REQ-DCM-012 and REQ-OCC-002, applies control CTL-14 to the deed in lieu and restructure documents, and supports the target of 1,000 deed in lieu cases a month in 2027 (NFR-006).

## 3. Preconditions

- RWB-E1-046 (template and merge field catalog as data) and RWB-E1-034 (template versions with the Legal approval record) are done.
- RWB-E1-027 (decision log writer) and RWB-E1-024 (document store) are done.
- Templates DIL-CONTRACT, DIL-CA and DIL-MORTGAGE, and RES-AGREEMENT for restructure, are loaded in Thai with approved_by_legal = true (template codes assumed; DL28).
- The template-to-document-type mapping is in the document type table: DIL-CONTRACT to CONTRACT, DIL-CA to CREDIT_APPROVAL, DIL-MORTGAGE to MORTGAGE_DOCUMENT, RES-AGREEMENT to CONTRACT (assumed; DL19).
- The case has a treatment of type DEED_IN_LIEU or RESTRUCTURE with decision_log_id set (approved at D6.4) and no outcome yet.
- The merge field providers of P3 (case), S2 (treatment), P1 (party and collateral) are listed in the MergeFieldResolver configuration.
- The caller holds Documents C (RW-RESTRUCT or RW-CASEOWN), or is the service identity SY-CASEWF for rule-driven generation from Epic 3.

## 4. Flow

1. Restructuring officer or SY-CASEWF: requests generation for a case, a treatment and a list of template codes.
2. System: reads the treatment through TreatmentReader and checks it is approved and open.
3. System: for each template code, reads the current version from the template catalog for the language and product group: approved by Legal, active, highest version valid on the request date.
4. System: reads the merge field list of that version and asks each owning module's MergeFieldProvider for the values.
5. System: checks that every required merge field has a value; formats each value by its catalog format (Thai long date in Buddhist Era, amount with two decimals, amount in Thai words).
6. System: renders each template body to PDF/A-2b with the Thai fonts embedded, and stores each file and the merge snapshot in the draft area of the standard container.
7. System: writes one decision log entry with decision code D6.4, the inputs reference (merge snapshot), and per document the template code and version.
8. System: in the same transaction writes one document row per file with source GENERATED, state DRAFT, template code, template version and treatment ID, and one DocumentStored event (EV-16) per document.
9. System: returns the generated documents; the screens of RWB-E2-017 show them for review.

## 5. Exception paths

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

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the template catalog (RWB-E1-046), template versions (RWB-E1-034) and the decision log writer (RWB-E1-027), all in Epic 1 |
| Negotiable | Templates, merge fields, formats and the type mapping are data owned by Legal and the product owner |
| Valuable | Ends re-keying of deed in lieu and restructure documents |
| Estimable | One service, one renderer, one resolver, one endpoint, no screen |
| Small | Fits in two weeks with its tests |
| Testable | Each scenario below is one test with synthetic case data |

## 7. Acceptance criteria

```gherkin
Feature: Document generation engine for contract, CA and mortgage templates

  Background:
    Given case "RW-2026-000301" with product group "MORTGAGE"
    Given treatment "TRT-0301" of type "DEED_IN_LIEU" on that case with decision_log_id set and no outcome
    Given template "DIL-CONTRACT" version 2 in Thai for "MORTGAGE" with approved_by_legal true
    Given the merge fields of "DIL-CONTRACT" version 2 are case_no, borrower_name, title_doc_no, transfer_price and contract_date
    Given a restructuring officer with role RW-RESTRUCT in scope of the case

  Scenario: AC1 Generate
    Given the case facts give transfer_price 1250000.00, title_doc_no "12345" and contract_date 2026-12-10
    When the engine runs for treatment "TRT-0301" and template "DIL-CONTRACT"
    Then the system stores one document with document_type "CONTRACT", source "GENERATED", state "DRAFT" and write_once false
    Then the document carries template_code "DIL-CONTRACT", template_version 2 and treatment_id "TRT-0301"
    Then the PDF shows "1,250,000.00 บาท (หนึ่งล้านสองแสนห้าหมื่นบาทถ้วน)" and "10 ธันวาคม 2569"
    Then the system writes one decision log entry with decision code "D6.4" and an inputs reference to the merge snapshot
    Then one DocumentStored event is in the outbox

  Scenario: AC2 Missing field
    Given the case has no title_doc_no
    When the engine runs for template "DIL-CONTRACT"
    Then the response is 422 with MSG-P5-009 naming "DIL-CONTRACT" and "title_doc_no"
    Then no document, no file and no decision log entry is stored

  Scenario: AC3 Version
    Given template "DIL-CONTRACT" version 3 is approved by Legal and valid from 2026-12-15
    Given document "DOC-0310" was generated on 2026-12-10 from version 2
    When the engine runs on 2026-12-15
    Then the new document carries template_version 3
    Then "DOC-0310" still carries template_version 2 and its file opens
    Then template version 2 stays readable in the template catalog

  Scenario: AC4 A version not approved by Legal is refused
    Given template "DIL-CA" has only version 1 with approved_by_legal false
    When the engine runs for template "DIL-CA"
    Then the response is 422 with MSG-P5-010 naming "DIL-CA" version 1
    Then the system stores nothing

  Scenario: AC5 A withdrawn template holds generation
    Given template "DIL-MORTGAGE" version 1 is withdrawn and no later version is approved
    When the engine runs for template "DIL-MORTGAGE"
    Then the response is 422 with MSG-P6-003 naming "DIL-MORTGAGE"
    Then the system raises a task to the restructuring officer who requested it

  Scenario: AC6 A treatment that is not approved is refused
    Given treatment "TRT-0302" of type "DEED_IN_LIEU" with no decision_log_id
    When the engine runs for treatment "TRT-0302"
    Then the response is 409 with MSG-P5-011
    Then the system stores nothing

  Scenario: AC7 The decision log write fails
    Given the decision log store does not accept writes
    When the engine runs for treatment "TRT-0301" and template "DIL-CONTRACT"
    Then the response is 503 with MSG-P7-003
    Then no document row exists for "TRT-0301" and the draft file is removed from the container
    Then the system raises an incident as in R-UNI-39

  Scenario: AC8 A repeated request
    Given a request with Idempotency-Key "K-0301" generated document "DOC-0311"
    When the same request with Idempotency-Key "K-0301" arrives again
    Then the response is 201 with document "DOC-0311"
    Then no second document or decision log entry is written

  Scenario: AC9 Two requests at the same time
    Given two requests for treatment "TRT-0301" and template "DIL-CONTRACT" with different keys arrive together
    When both run
    Then one returns 201 with one DRAFT document
    Then the other returns 409 with MSG-GEN-004

  Scenario: AC10 A template body that cannot be rendered
    Given the body of "DIL-CONTRACT" version 2 is a damaged file
    When the engine runs
    Then the response is 503 with MSG-GEN-006 naming "document generation"
    Then the system stores nothing and an incident is raised

  Scenario: AC11 No template for the product group
    Given template "DIL-CONTRACT" exists only for product group "MORTGAGE"
    Given case "RW-2026-000305" has product group "HIRE_PURCHASE"
    When the engine runs for that case and "DIL-CONTRACT"
    Then the response is 422 with MSG-P5-010 naming "DIL-CONTRACT" for "HIRE_PURCHASE"

  Scenario: AC12 A case outside the caller's scope
    Given case "RW-2026-000306" is in team "HP-NE" and the officer's scope is team "FCR-BKK"
    When the officer requests generation for that case
    Then the response is 404 with MSG-P4-003

  Scenario: AC13 A set of three documents in one request
    Given templates "DIL-CONTRACT", "DIL-CA" and "DIL-MORTGAGE" are current and approved
    When the engine runs for treatment "TRT-0301" with the three template codes
    Then the system stores three documents with types "CONTRACT", "CREDIT_APPROVAL" and "MORTGAGE_DOCUMENT"
    Then one decision log entry names the three template codes and versions

  Scenario: AC14 A set is stored whole or not at all
    Given templates "DIL-CONTRACT" and "DIL-MORTGAGE" are current and approved
    Given template "DIL-CA" has no version approved by Legal
    When the engine runs for treatment "TRT-0301" with the three template codes
    Then the response is 422 with MSG-P5-010 naming "DIL-CA"
    Then the system stores none of the three documents and no decision log entry is written
```

## 8. Business rules

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

## 9. State transitions

None. This story does not change a case status. It creates documents in state DRAFT.

| From | Event | Condition | To |
|---|---|---|---|
| (none) | Generation requested | BR1, BR3 and BR5 pass and the decision log write succeeds | document state DRAFT |

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT, restructuring officer (FCR) | Requests generation for a treatment in scope (Documents C) |
| RW-CASEOWN, case owner | Requests generation for a treatment in scope (Documents C) |
| SY-CASEWF, case workflow module | Calls DocumentGenerator for rule-driven generation from Epic 3 (R-DIL-14, R-DIL-16) |
| SY-DECLOG, decision log writer | Writes the decision log entry |
| RW-LEGAL, legal counsel | Approves template versions (Documents CRUA; RWB-E1-034); approval is a precondition, not part of this story |
| RW-TEAMMGR, team manager | Reads generated documents (Documents R); cannot generate |

No approval level from the delegation of authority applies in this story. The treatment itself was approved at D6.4 before generation.

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-002 | recovery_case | case_no | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-004 | recovery_case | primary_customer_id | Read |
| DF-TRT-001 | treatment | id | Read |
| DF-TRT-003 | treatment | decision_log_id | Read |
| DF-TRT-004 | treatment | treatment_type | Read |
| DF-TRT-007 | treatment | offer_amount | Read |
| DF-TRT-013 | treatment | outcome | Read |
| DF-PTY-004 | party | first_name | Read |
| DF-PTY-005 | party | last_name | Read |
| DF-COL-004 | collateral | title_doc_no | Read |
| DF-REF-045 to DF-REF-051 | template | all fields | Read |
| DF-DOC-001 to DF-DOC-011 | document | all fields | Write |
| DF-DOC-032 | document | template_id | Write |
| DF-DOC-032 | document | template_id | Write |
| DF-DOC-033 | document | treatment_id | Write |
| Standard column | document | state | Write |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**POST /cases/{caseId}/generated-documents** (new, recorded in the additions file)

| Item | Value |
|---|---|
| Request | GenerateRequest: treatmentId (uuid, required), templateCodes (array of string, 1 to 10, required), language (TH or EN, default TH); header Idempotency-Key (required) |
| Response | 201 DocumentPage with the generated documents |
| Errors | 401 (MSG-P4-001); 403 no Documents C (MSG-P4-002); 404 case or treatment not found or out of scope (MSG-P4-003); 409 treatment not approved or open (MSG-P5-011), or a concurrent request (MSG-GEN-004); 422 missing merge value (MSG-P5-009), template not approved or not found (MSG-P5-010), template withdrawn (MSG-P6-003), empty templateCodes (MSG-GEN-001); 503 decision log write failed (MSG-P7-003) or render failed (MSG-GEN-006) |
| Authorization | Documents, right C, scope applied |
| Idempotency | Idempotency-Key header, kept 24 hours (document_hub_parameter GEN_IDEMPOTENCY_HOURS) |

**Published interface (P5)**

```java
package recovery.dochub.generation;
public interface DocumentGenerator {
    GenerationResult generate(GenerationRequest request);
}
// GenerationRequest: caseId, treatmentId, templateCodes, language, requestedBy, idempotencyKey, overrides (List<MergeOverride>, used by RWB-E2-017)
// GenerationResult: decisionLogEntryId, documents (documentId, templateCode, templateVersion, documentType)
```

**Published interfaces called**

```java
// P6, RWB-E1-046
TemplateVersion TemplateCatalog.current(String templateCode, String language, String productGroup, LocalDate asOf);
List<MergeField> TemplateCatalog.mergeFields(UUID templateId);
// P7, RWB-E1-027
UUID DecisionLogWriter.write(DecisionRecord record);
// S2
TreatmentSummary TreatmentReader.find(UUID treatmentId);
// P3, S2, P1 each implement
Map<String, Object> MergeFieldProvider.resolve(UUID caseId, UUID treatmentId, Set<String> mergeFieldCodes);
```

**Events published:** DocumentStored (EV-16) per document, payload documentId, caseId, type, source.

## 13. Solution plan

**Package.** folder `recovery/dochub/generation`, Java package `recovery.dochub.generation`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| GeneratedDocumentController | Controller | POST /cases/{caseId}/generated-documents |
| DocumentGenerator | Published interface | Generation entry point for the controller, RWB-E2-017 and SY-CASEWF |
| DocumentGenerationService | Service | Steps 2 to 8; BR1 to BR10; one transaction; removes draft files on failure |
| TemplateSelector | Service | Picks the current version by language, product group and date (BR1, BR2) |
| MergeFieldResolver | Service | Calls each MergeFieldProvider listed in its configuration; checks required fields (BR3) |
| ValueFormatter | Service | Thai dates, amounts and amounts in words (BR4) |
| TemplateRenderer | Service | Renders the template body with merge tags in the form {{merge_field_code}} to PDF/A-2b with embedded Thai fonts |
| BlobStorageAdapter | Service | From RWB-E1-024; writes draft files and the merge snapshot to the standard container (RWB-TE-012). Drafts do not go through DocumentStore.store, which would place a legal type in the write-once container at once |
| DocumentHubRepository | Repository | Writes document rows |
| IdempotencyRepository | Repository | Holds the request key and result |

**Database**

- Writes document (all fields, state DRAFT, source GENERATED) and the new columns template_code varchar(30), template_version integer, treatment_id uuid.
- Flyway migration in this story for the three columns, with index `ux_document_draft_per_template ON document (treatment_id, template_code) WHERE state = 'DRAFT' AND is_active` for AC9.
- Writes decision_log_entry only through DecisionLogWriter. Reads template only through TemplateCatalog. The uk_template constraint on template_code alone allows one row per code; AC3 needs one row per version, so the constraint must be on (template_code, template_version). This is raised with the P6 owner of RWB-E1-046.

**Configuration and reference data**

- Templates and merge field catalog (P6, RWB-E1-046), owner legal counsel (DL28).
- Template-to-document-type mapping and retention class per type in the document type table (RWB-E1-025, DL19).
- document_hub_parameter rows GEN_IDEMPOTENCY_HOURS 24, GEN_MAX_TEMPLATES 10, GEN_FONT "TH Sarabun New", loaded by the reference data administrator. Values assumed.

**Build steps**

1. Add the Flyway migration and the partial unique index; repository tests.
2. Build TemplateSelector against a stub TemplateCatalog for approved, unapproved, withdrawn, product-specific and all-product templates, and a valid-from date.
3. Build MergeFieldResolver and its list of providers; unit tests for a missing required field.
4. Build ValueFormatter with tests for Buddhist Era dates and amounts in Thai words.
5. Build TemplateRenderer with a sample Thai template; check PDF/A-2b conformance and embedded fonts.
6. Build DocumentGenerationService: order of checks, render, store drafts, write the decision log, write documents and outbox, remove drafts on any failure.
7. Build the controller with Idempotency-Key handling and the error mapping in section 12.
8. Add the contract test for the new endpoint (RWB-TE-003).

**Feature flag:** `rwb.dochub.generation-engine`. Off: the endpoint returns 404 and DocumentGenerator refuses calls.

**Done when:** the tests in section 16 pass; a sample deed in lieu set is checked by legal counsel against the approved wording.

## 14. Validation and messages

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

## 15. Screens and states

No screen in this story. The restructuring officer reaches the engine through the screens of RWB-E2-017. Generated documents appear on SCR-30 Case documents in the list state with state DRAFT.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-026-01 | AC1, BR1, BR4, BR6 | System | Synthetic mortgage case and DIL treatment, template DIL-CONTRACT v2 |
| TC-E2-026-02 | AC2, BR3 | System | Case with no title deed number |
| TC-E2-026-03 | AC3, BR10 | System | Template v3 valid from 2026-12-15 |
| TC-E2-026-04 | AC4, BR1 | System | DIL-CA v1 not approved |
| TC-E2-026-05 | AC5, BR2 | System | DIL-MORTGAGE withdrawn |
| TC-E2-026-06 | AC6, BR5 | System | Treatment with no decision_log_id |
| TC-E2-026-07 | AC7, BR7 | System | Decision log stub refusing writes |
| TC-E2-026-08 | AC8, BR9 | System | Same Idempotency-Key twice |
| TC-E2-026-09 | AC9 | System | Two parallel requests |
| TC-E2-026-10 | AC10 | System | Damaged template body |
| TC-E2-026-11 | AC11, BR1 | System | Hire purchase case, mortgage-only template |
| TC-E2-026-12 | AC12 | System | Case of team HP-NE, officer of team FCR-BKK |
| TC-E2-026-13 | AC13 | System | Three current templates |
| TC-E2-026-14 | AC14, BR8 | System | Three templates, DIL-CA not approved |
| TC-E2-026-15 | Access | Access | RW-TEAMMGR user (Documents R) calls POST generated-documents; refused with MSG-P4-002 |
| TC-E2-026-16 | Principle 5 | Resilience | Decision log write forced to fail during a three-document set; no document, no file, MSG-P7-003, incident raised |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: template codes, merge fields, formats, type mapping and fonts are data and parameters.
- No personal data in logs, tests or prompts: merge values and the snapshot are never logged; tests use synthetic parties; the clear ID number is used only at render time.
- No read of another module's tables: templates, treatments, case facts, parties and collateral come through published interfaces.
- No document is produced from a template version without approved_by_legal = true.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-012 | Contracts, credit applications and mortgage documents generated from approved templates with no re-keying | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-OCC-07 | 7.3 Negotiate settlement or deed in lieu; 13 Manage documents and correspondence | R-DIL-14, R-DIL-16, R-UNI-39, R-UNI-40 | TC-E2-026-01, TC-E2-026-02, TC-E2-026-06 to TC-E2-026-16 |
| REQ-OCC-002 | Letter templates versioned, with the Legal approval recorded against the version | Business Requirements Program, section 5.6; Epic 2, section 3.5 | FEAT-OCC-07 | 13 Manage documents and correspondence | R-LIT-03, R-LIT-04, R-LIT-06, R-UNI-38 | TC-E2-026-03 to TC-E2-026-05, TC-E2-026-11 |

## 19. Out of scope

- The generation, review and send screens (RWB-E2-017).
- The e-signature flow (RWB-E2-018).
- Rule-driven generation when the deed in lieu route reaches TRANSFER_PRICE_SET (FEAT-TRT-18, Epic 3).
- Template upload and Legal approval (RWB-E1-034) and the merge field catalog (RWB-E1-046).
- Debt sale agreements and notices (FEAT-DBS-10, Epic 6).
