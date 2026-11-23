<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5.zip!RWB E2 017 Contract CA and mortgage document generation screens v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5.zip!RWB E2 017 Contract CA and mortgage document generation screens v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-017 Contract, CA and mortgage document generation screens

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-017 |
| Epic | E2, release 31 December 2026 |
| Module | P5 Document hub |
| Feature | FEAT-OCC-07 Generate contract, credit approval and mortgage documents |
| Requirement IDs | REQ-DCM-012, REQ-OCC-002 |
| BRD section | Business Requirements Epic 2, section 3.5 |
| L3 process | 7.3 Negotiate settlement or deed in lieu; 13 Manage documents and correspondence |
| Decision | D6.4, D6.5 |
| Priority | Must |
| Depends on | RWB-E2-026, RWB-E1-034, RWB-E1-054, RWB-TE-012 |
| Status | Ready for build |

## 1. Story

As a **restructuring officer (FCR)**, I want **screens to generate the agreement, the credit approval and the mortgage documents from templates with the case facts, review them and send them for signature**, so that **deed in lieu and restructure documents are produced without re-keying**.

## 2. Business rationale

The officer today copies case facts into three Word files, prints them and walks them to signature, and a late change is made by hand on the printed copy with no record. These screens produce the set from the approved treatment through the generation engine, let the officer correct an allowed value with a recorded reason, and send the reviewed set for signature as write-once documents. It meets REQ-DCM-012 and REQ-OCC-002, applies CTL-12 and CTL-14 to the set, and shortens the restructure turnaround, which the program targets at 5 days from 23 days.

## 3. Preconditions

- RWB-E2-026 (generation engine), RWB-E1-034 (template versions with Legal approval), RWB-E1-054 (review endpoint) and RWB-TE-012 (write-once container) are done.
- RWB-E2-018 provides SignatureRequests in P6; until it is merged the send step is behind its flag.
- The document set per treatment type is in reference data: DEED_IN_LIEU uses DIL-CONTRACT, DIL-CA and DIL-MORTGAGE; RESTRUCTURE uses RES-AGREEMENT (assumed; DL28).
- The merge field catalog marks each merge field as overridable or locked. Amounts, parties, title numbers and the treatment terms are locked; dates of signing and witness details are overridable (assumed; DL28).
- CONTRACT, CREDIT_APPROVAL and MORTGAGE_DOCUMENT are legal types in the document type table (assumed; DL19).
- The officer holds RW-RESTRUCT (Documents CRU, Treatment and offer CRUA) with scope over the case.

## 4. Flow

1. Restructuring officer: opens SCR-14 Treatment record for an approved deed in lieu treatment and chooses Generate documents.
2. System: shows the document set for the treatment type and product, with the current approved version of each template.
3. Restructuring officer: confirms; the system calls the generation engine (RWB-E2-026) and shows the three drafts with their merge values.
4. Restructuring officer: opens a draft; the system shows the PDF next to the list of merge values, with locked values read only.
5. Restructuring officer: corrects an overridable value and enters the reason.
6. System: writes a decision log entry with the override and its reason, regenerates the draft as the next doc_version, and keeps the earlier version readable.
7. Restructuring officer: marks each draft reviewed; the system sets state REVIEWED.
8. Restructuring officer: chooses Send for signature.
9. System: checks every document of the set is REVIEWED, copies each final file to the write-once container, writes the decision log entry for the send, starts the signature request in P6 and sets each document to state SENT with write_once true.
10. System: shows MSG-P5-012; the documents show as sent on SCR-30 Case documents.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The treatment is not approved or is closed | Generate is refused | MSG-P5-011 | AC4 |
| X2 | A correction has no reason | 422; nothing changes | MSG-GEN-001 | AC5 |
| X3 | The value is locked in the merge field catalog | 422; nothing changes | MSG-P5-014 | AC6 |
| X4 | Send with a document of the set not reviewed | 422; nothing sent | MSG-P5-013 | AC7 |
| X5 | A change to a document already sent | 409; nothing changes | MSG-P5-002 | AC8 |
| X6 | The decision log write fails on a correction or a send | 503; nothing changes | MSG-P7-003 | AC9 |
| X7 | Send is chosen twice | One signature request; the second call returns the first result | None | AC10 |
| X8 | Two officers correct the same draft | The second save gets 409 | MSG-GEN-004 | AC11 |
| X9 | The signature service refuses the request | 503; documents stay REVIEWED | MSG-GEN-006 | AC12 |
| X10 | The template version changed after the drafts were made | Send is refused; the officer regenerates | MSG-P5-013 | AC13 |
| X11 | The user holds Documents R only | Actions hidden; a direct call gets 403 | MSG-P4-002 | Access test TC-E2-017-14 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the engine (RWB-E2-026) in the same epic and the write-once container from Epic 1 |
| Negotiable | The set per treatment type and which fields may be overridden are data owned by Legal |
| Valuable | The officer produces and sends the set without re-keying |
| Estimable | Two new endpoints, one reused endpoint, one panel on SCR-14, one review view on SCR-30 |
| Small | Fits in two weeks with its tests |
| Testable | Each scenario below is one test with synthetic data |

## 7. Acceptance criteria

```gherkin
Feature: Contract, CA and mortgage document generation screens

  Background:
    Given case "RW-2026-000401" with product group "MORTGAGE" in team "FCR-BKK"
    Given treatment "TRT-0401" of type "DEED_IN_LIEU" approved at D6.4 with no outcome
    Given the set for "DEED_IN_LIEU" is "DIL-CONTRACT" version 2, "DIL-CA" version 1 and "DIL-MORTGAGE" version 1, all approved by Legal
    Given a restructuring officer with role RW-RESTRUCT and scope team "FCR-BKK"

  Scenario: AC1 Generate
    Given the officer opens SCR-14 for "TRT-0401"
    When the officer chooses Generate documents and confirms
    Then the system produces three documents from the current template versions with the case facts filled
    Then they show as drafts of types "CONTRACT", "CREDIT_APPROVAL" and "MORTGAGE_DOCUMENT" with template versions 2, 1 and 1

  Scenario: AC2 Review
    Given the contract draft "DOC-0411" at doc_version 1 has contract_date "2026-12-10"
    When the officer corrects contract_date to "2026-12-12" with reason "Signing appointment moved by the customer"
    Then the system writes a decision log entry with decision code "D6.4", the old and new value and the reason as override_reason
    Then the system regenerates "DOC-0411" as doc_version 2 showing "12 December 2569 BE"
    Then doc_version 1 stays readable

  Scenario: AC3 Send
    Given the three drafts of "TRT-0401" are in state "REVIEWED"
    When the officer chooses Send for signature
    Then each file is in the write-once container and each document has write_once true and state "SENT"
    Then the system starts one signature request for the three documents in P6
    Then the system writes a decision log entry with final_call "SENT_FOR_SIGNATURE"
    Then the screen shows MSG-P5-012 with count 3

  Scenario: AC4 Generate for a treatment that is not approved
    Given treatment "TRT-0402" of type "DEED_IN_LIEU" has no decision_log_id
    When the officer opens SCR-14 for "TRT-0402"
    Then the system disables generate documents with MSG-P5-011
    Then a direct call to POST generated-documents returns 409 with MSG-P5-011

  Scenario: AC5 A correction without a reason
    Given the draft "DOC-0411"
    When the officer corrects contract_date with an empty reason
    Then the response is 422 with MSG-GEN-001 naming "Reason"
    Then "DOC-0411" stays at its doc_version

  Scenario: AC6 A locked value cannot be corrected
    Given transfer_price is locked in the merge field catalog
    When the officer tries to change transfer_price on "DOC-0411" from 1250000.00 to 1200000.00
    Then the response is 422 with MSG-P5-014 naming "Transfer price"
    Then nothing changes

  Scenario: AC7 Send with a draft not reviewed
    Given two drafts of "TRT-0401" are "REVIEWED" and "DIL-MORTGAGE" is still "DRAFT"
    When the officer chooses Send for signature
    Then the response is 422 with MSG-P5-013 naming the mortgage document
    Then the system copies no document to the write-once container and no signature request starts

  Scenario: AC8 A sent document cannot be changed
    Given "DOC-0411" is in state "SENT"
    When the officer tries to correct contract_date
    Then the response is 409 with MSG-P5-002
    Then "DOC-0411" is unchanged

  Scenario: AC9 The decision log write fails on a correction
    Given the decision log store does not accept writes
    When the officer corrects contract_date on "DOC-0411" with a reason
    Then the response is 503 with MSG-P7-003
    Then "DOC-0411" stays at its doc_version and no file is added

  Scenario: AC10 Send chosen twice
    Given the officer chose Send for signature for "TRT-0401" with Idempotency-Key "S-0401"
    When the same request with Idempotency-Key "S-0401" arrives again
    Then the response returns the same three documents in state "SENT"
    Then only one signature request exists for "TRT-0401"

  Scenario: AC11 Two officers correct the same draft
    Given two officers opened "DOC-0411" at version 4
    Given the first officer saved a correction, so the record is at version 5
    When the second officer saves a correction with version 4
    Then the response is 409 with MSG-GEN-004

  Scenario: AC12 The signature service refuses the request
    Given SignatureRequests in P6 returns "UNAVAILABLE"
    When the officer chooses Send for signature for the three reviewed drafts
    Then the response is 503 with MSG-GEN-006 naming "e-signature"
    Then the documents stay in state "REVIEWED"
    Then a second send after the service returns completes with one signature request

  Scenario: AC13 The template changed after the drafts were made
    Given the three drafts were made from "DIL-CONTRACT" version 2
    Given "DIL-CONTRACT" version 3 became current after the drafts were made
    When the officer chooses Send for signature
    Then the response is 422 with MSG-P5-013 naming the contract and "template version 3"
    Then the system sends no document
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The set of templates for a treatment comes from reference data by treatment type and product group | Template catalog (RWB-E1-046); DL28 |
| BR2 | Only an approved, open treatment can have its set generated | DF-TRT-003, DF-TRT-013; R-DIL-14; R-DIL-16 |
| BR3 | Only an overridable merge field can be corrected, and only with a reason | Merge field catalog; R-UNI-14 (coded reason when departing from the system result) |
| BR4 | Each correction is written to the decision log with the old value, the new value and the reason before the draft is regenerated | Principle 5; CTL-07 |
| BR5 | A correction creates the next doc_version; earlier versions stay readable | FEAT-DCM-20; DF-DOC-011 |
| BR6 | A set is sent only when every document is REVIEWED and every document was made from the current template version | CTL-14; R-LIT-03 |
| BR7 | On send, legal types are copied to the write-once container and cannot be changed after | CTL-12; VR-P5-001-2; RWB-TE-012 |
| BR8 | The signature path (e-signature or wet ink) is chosen by P6 by product and Legal rule | R-DIL-18; R-RES-16; REQ-OCC-009 |
| BR9 | A send that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39; CTL-06 |
| BR10 | A repeat send with the same Idempotency-Key returns the first result | R-UNI-40 |

## 9. State transitions

None. This story does not change a case status. It changes the document state.

| From | Event | Condition | To |
|---|---|---|---|
| document state DRAFT | Correction saved | Overridable field, reason given, decision log written | DRAFT, doc_version + 1 |
| document state DRAFT | Marked reviewed | None | REVIEWED |
| document state REVIEWED | Correction saved | As above | DRAFT, doc_version + 1 |
| document state REVIEWED | Send for signature | All of the set REVIEWED, current template version, decision log written, signature request accepted | SENT, write_once true |

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT, restructuring officer (FCR) | Generates, corrects, marks reviewed and sends in scope (Documents CRU) |
| RW-CASEOWN, case owner | Generates, corrects, marks reviewed and sends in scope (Documents CRU) |
| RW-TEAMMGR, team manager | Reads the drafts and sent documents (Documents R) |
| RW-LEGAL, legal counsel | Reads the set; owns which fields are overridable (Documents CRUA) |
| SY-DECLOG, decision log writer | Writes the correction and send entries |

No approval level from the delegation of authority applies; the treatment was approved at D6.4 before generation.

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-002 | recovery_case | case_no | Read |
| DF-TRT-001 | treatment | id | Read |
| DF-TRT-003 | treatment | decision_log_id | Read |
| DF-TRT-004 | treatment | treatment_type | Read |
| DF-TRT-013 | treatment | outcome | Read |
| DF-REF-046 | template | template_code | Read |
| DF-REF-047 | template | template_version | Read |
| DF-REF-051 | template | approved_by_legal | Read |
| DF-DOC-001 | document | id | Read |
| DF-DOC-004 | document | document_type | Read |
| DF-DOC-006 | document | storage_ref | Write |
| DF-DOC-008 | document | review_status | Write |
| DF-DOC-010 | document | write_once | Write |
| DF-DOC-011 | document | doc_version | Write |
| DF-DOC-032 | document | template_id | Read |
| DF-DOC-033 | document | treatment_id | Read |
| Standard column | document | state, version | Write |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**POST /api/recovery/v1/cases/{caseId}/generated-documents** (defined in RWB-E2-026): used for step 3.

**POST /documents/{documentId}/regenerate** (new, recorded in the additions file)

| Item | Value |
|---|---|
| Request | RegenerateRequest: overrides (array of mergeField, value, reason; 1 to 10), version (integer) |
| Response | Document at the new doc_version |
| Errors | 401; 403 no Documents U (MSG-P4-002); 404 (MSG-P4-003); 409 document SENT (MSG-P5-002) or stale version (MSG-GEN-004); 422 empty reason (MSG-GEN-001), locked field (MSG-P5-014), missing value after override (MSG-P5-009); 503 decision log write failed (MSG-P7-003) |
| Authorization | Documents, right U, scope applied |
| Idempotency | Idempotency-Key header |

**POST /api/recovery/v1/documents/{documentId}/review** (new in RWB-E1-054), action COMPLETE: sets a generated draft to state REVIEWED.

**POST /treatments/{treatmentId}/signature-requests** (new, recorded in the additions file)

| Item | Value |
|---|---|
| Request | SendForSignatureRequest: treatmentId (uuid), documentIds (array of uuid), header Idempotency-Key (required) |
| Response | 200 DocumentPage with the sent documents |
| Errors | 401; 403 no Documents U (MSG-P4-002); 404 (MSG-P4-003); 409 a document already SENT (MSG-P5-002); 422 a document not REVIEWED or not on the current template version (MSG-P5-013); 503 decision log write failed (MSG-P7-003) or signature service unavailable (MSG-GEN-006) |
| Authorization | Documents, right U, scope applied |
| Idempotency | Idempotency-Key header, kept 24 hours |

**Published interface called (P6, RWB-E2-018)**

```java
package recovery.comms.signature;
public interface SignatureRequests {
    SignatureStart start(UUID caseId, UUID treatmentId, List<UUID> documentIds, String idempotencyKey); // ACCEPTED with requestId, or UNAVAILABLE
}
```

**Published interface called (P5, RWB-E2-026):** DocumentGenerator.generate(GenerationRequest) with overrides for the regenerate step.

## 13. Solution plan

**Package.** folder `recovery/dochub/generation/ui` for the controller and service, Java package `recovery.dochub.generation`; front end folder `recovery/dochub/generation`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| GeneratedDocumentController | Controller | Adds POST /documents/{documentId}/regenerate and POST /cases/{caseId}/generated-documents/send |
| DocumentSetService | Service | Regenerate with overrides (BR3 to BR5), mark reviewed, send (BR6, BR7, BR9, BR10) |
| BlobStorageAdapter | Service | From RWB-E1-024; copies final files to the write-once container, idempotent by file hash through ContentHashGuard (RWB-TE-012) |
| DocumentHubRepository | Repository | Document state, version and write_once updates |
| GenerateDocumentsPanel | React component | On SCR-14: the set, template versions, Generate and Send buttons, disabled states |
| GeneratedDocumentReview | React component | On SCR-30: PDF preview, merge values with locked ones read only, correction form with reason, Mark reviewed |

**Database**

- Updates document (storage_ref, review_status, write_once, doc_version, state, version, updated_at, updated_by). Reads template_code, template_version, treatment_id added by RWB-E2-026.
- Writes decision_log_entry through DecisionLogWriter only. No new table.

**Configuration and reference data**

- Template set per treatment type and product, and overridable or locked per merge field (P6 template catalog, RWB-E1-046; owner legal counsel; DL28).
- Legal flag per document type (document type table, DL19).
- document_hub_parameter row GEN_IDEMPOTENCY_HOURS 24 (assumed), from RWB-E2-026.

**Build steps**

1. Build the regenerate endpoint: version check, SENT check, locked and reason checks, decision log write, call DocumentGenerator with overrides, store as next doc_version.
2. Extend POST /documents/{documentId}/review action COMPLETE for GENERATED drafts: set state REVIEWED and review_status CONFIRMED or CORRECTED.
3. Build the send endpoint: idempotency, BR6 checks, write-once copy, decision log write, SignatureRequests.start, state SENT, in that order with the failure handling of AC9 and AC12.
4. Build GenerateDocumentsPanel on SCR-14 with the disabled state and MSG-P5-011.
5. Build GeneratedDocumentReview on SCR-30 with the correction form and the read-only state for locked fields and for RW-TEAMMGR.
6. Add contract tests for the two new endpoints (RWB-TE-003) and browser tests (RWB-TE-010).

**Feature flag:** `rwb.dochub.generation-screens`, with `rwb.dochub.generation-screens.send` for the send step until RWB-E2-018 is merged. Off: the panel is hidden.

**Done when:** the tests in section 16 pass and a restructuring officer generates, corrects and sends one synthetic deed in lieu set in UAT.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-011 | Treatment not approved or not open | Documents can be generated only for an approved {treatment} that is still open. |
| MSG-P5-012 | Set sent for signature (new) | {count} documents were sent for signature. |
| MSG-P5-013 | Send with a document not reviewed or on an old template version (new) | {document} cannot be sent yet: {reason}. |
| MSG-P5-014 | Correction to a locked merge field (new) | {field} comes from the approved treatment and cannot be changed here. |
| MSG-P5-002 | Change to a sent document | Legal documents cannot be changed. Add a new version instead. |
| MSG-GEN-001 | Correction without a reason | Enter {field}. |
| MSG-GEN-004 | Saved against an old version | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-006 | Signature service unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without Documents U | You cannot {action} here. Your role does not include it. |

Thai text for each message follows decision DL10.

## 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-14 Treatment record | Approved | Sees the document set with template versions; chooses Generate documents; Send for signature when all are reviewed |
| SCR-14 Treatment record | Draft, submitted | Generate documents is disabled with MSG-P5-011 |
| SCR-30 Case documents | List | Opens a draft, sees the PDF and the merge values, corrects an overridable value with a reason, marks it reviewed |
| SCR-30 Case documents | Read only (common state) | A sent document, or any document for RW-TEAMMGR, shows without edit controls |

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-017-01 | AC1, BR1, BR2 | System | Synthetic mortgage DIL treatment, three approved templates |
| TC-E2-017-02 | AC2, BR3, BR4, BR5 | System | Contract date moved by two days |
| TC-E2-017-03 | AC3, BR6, BR7, BR8 | System | Three reviewed drafts; P6 stub returns ACCEPTED |
| TC-E2-017-04 | AC4, BR2 | System | Treatment with no decision_log_id |
| TC-E2-017-05 | AC5, BR3 | System | Empty reason |
| TC-E2-017-06 | AC6, BR3 | System | Locked transfer price |
| TC-E2-017-07 | AC7, BR6 | System | One draft not reviewed |
| TC-E2-017-08 | AC8, BR7 | System | Document in state SENT |
| TC-E2-017-09 | AC9, BR4 | System | Decision log stub refusing writes on a correction |
| TC-E2-017-10 | AC10, BR10 | System | Same send key twice |
| TC-E2-017-11 | AC11 | System | Two sessions on one draft |
| TC-E2-017-12 | AC12 | System | P6 stub returns UNAVAILABLE, then ACCEPTED |
| TC-E2-017-13 | AC13, BR6 | System | Template version 3 made current after the drafts |
| TC-E2-017-14 | Access | Access | RW-TEAMMGR user (Documents R) calls POST generated-documents/send; refused with MSG-P4-002 |
| TC-E2-017-15 | Principle 5 | Resilience | Decision log write forced to fail on send; nothing sent, documents stay REVIEWED, MSG-P7-003, incident raised |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the set per treatment type, the locked and overridable fields and the legal flag are data.
- No personal data in logs, tests or prompts: merge values, reasons and file names are not logged; tests use synthetic parties.
- No read of another module's tables: treatments, templates and signature requests are reached through published interfaces.
- A document copied to the write-once container is never changed; a later change is a new document version created before send only.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-012 | Contracts, credit applications and mortgage documents generated from approved templates with no re-keying | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-OCC-07 | 7.3 Negotiate settlement or deed in lieu; 13 Manage documents and correspondence | R-DIL-14, R-DIL-16, R-DIL-18, R-UNI-39, R-UNI-40 | TC-E2-017-01 to TC-E2-017-12, TC-E2-017-14, TC-E2-017-15 |
| REQ-OCC-002 | Templates versioned with the Legal approval recorded against the version | Business Requirements Program, section 5.6; Epic 2, section 3.5 | FEAT-OCC-07 | 13 Manage documents and correspondence | R-LIT-03 | TC-E2-017-01, TC-E2-017-13 |

## 19. Out of scope

- The generation engine, template selection and merge rules (RWB-E2-026).
- The e-signature flow, the wet ink path and the return of the signed copy (RWB-E2-018).
- Rule-driven generation on the deed in lieu route (FEAT-TRT-18, Epic 3).
- Settlement offer letters (R-SET-04, Epic 3).
