# RWB-P5-E2017-APP Contract, CA and mortgage document generation screens

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E2017-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-017 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP11, DP13, DP19 |
| Parallel lane | L-P5-G |
| Ready to start | After RWB-P5-E2026-APP |
| Depends on (build) | RWB-P5-E2017-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-N001-CON, RWB-P5-E2026-APP, RWB-P5-E1054-CON |
| Contract dependencies | RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | RWB-PLT-TE012-APP |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-026) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the generation, review and send screens of RWB-E2-017 move into `rwb-document` with the schema `rwb_document`, the topic `rwb.document.events.v1`, the REST base `/api/recovery/document/v1`, the store of RWB-P5-E1024-APP, the review operation of RWB-P5-E1054-APP, the generation engine of RWB-P5-E2026-APP and the contract baseline RWB-P5-E2017-CON; the thirteen legacy criteria, the eleven exception paths, the ten messages and the fifteen test cases are kept word for word in intent and values. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **restructuring officer (FCR)**, I want **screens to generate the agreement, the credit approval and the mortgage documents from templates with the case facts, review them and send them for signature**, so that **deed in lieu and restructure documents are produced without re-keying**.

Inside `rwb-document` this is the generation-screens capability of the document hub, and the same user story holds with the target service frame:

- Service `rwb-document`, schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with the retry and `.dlt` topics of the platform convention and event names `rwb.document.<Event>.v1`, Temporal task queue `rwb-document` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.document`.
- The generation engine is RWB-P5-E2026-APP in the same service: the panel calls `POST /api/recovery/document/v1/cases/{caseId}/generated-documents` with `GenerateRequest` (12.2), which runs the `generate` activity on queue `rwb-document`. This story owns the screens, the overrides, the review action and the send, and claims no part of the engine.
- The template set per treatment type and product group, the current approved version of each template and the merge field list of a version arrive through the template catalog contract of `rwb-comms` (RWB-P6-E1046-CON, DP-11, one hop, 2 s timeout, faked). `template` and `merge_field` are P6's in `rwb_comms`; this service holds no row of either and copies neither (DP-01, ASM-1863).
- The treatment, its type, its approval and its `decision_log_id` arrive through the `rwb-treatment` contract (S2, one hop, 2 s, faked), and the case and its product group through the `rwb-case` contract (RWB-P3-E1018-CON, one hop, 2 s, faked). Neither read is in the contract-dependency list of this story, which names the reference-data contract only (GAP-1016; ASM-1863).
- The product group, the document type, the review labels, the document source and the signature method and status values are read as reference data through the reference-data contract of `rwb-case` (DP-07, H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON). No list value is typed in code.
- Each correction and the send are recorded through the local decision-record library of DP-03 (H RWB-PLT-E1027-CON; the central ledger contract of `rwb-decision` is RWB-P7-E1027-CON, consumed and faked) in the same transaction as the document change, with decision code D6.4 and the final call the legacy criteria name. A failed record means nothing changes (MSG-P7-003, R-UNI-39).
- The document row is `document` in `rwb_document`; its state, `doc_version`, `review_status`, `storage_ref` and `write_once` are written through the store of RWB-P5-E1024-APP, which stays the only writer of the row and of the blob. The write-once copy on send goes to the container `rwb-docs-legal` through the platform storage product RWB-PLT-TE012-APP (the X dependency), at `{container}/{caseId}/{documentId}/v1`.
- Marking a draft reviewed is the review operation API-P5-014 `POST /api/recovery/document/v1/documents/{documentId}/review` action COMPLETE, owned by RWB-P5-E1054-APP and built against RWB-P5-E1054-CON; this story calls it in the same service (12.2).
- On send the signature request is started through the `rwb-comms` contract, the operation API-P6-009 `POST /api/recovery/comms/v1/treatments/{treatmentId}/signature-requests` (P6 rwb-comms, one hop, 2 s, faked, `ACCEPTED` with a request ID or `UNAVAILABLE`). The legacy P5 endpoint of section 12 of the story is therefore a consumed operation in the target and not a provided one (GAP-1016; ASM-1857). The requests themselves are stored in `signature_request`, which the Ownership Map gives to P5, and this story provides the operations `rwb-comms` uses to write and read them back.
- The screens are served through the gateway-bff composite route (DP-19, H RWB-PLT-N001-CON): SCR-14 Treatment record and SCR-30 Case documents are published inside the case record view and the browser never calls `rwb-document` directly.
- The legacy base `/api/recovery/v1` becomes `/api/recovery/document/v1` (DP-13). The legacy feature flags `rwb.dochub.generation-screens` and `rwb.dochub.generation-screens.send` become `rwb.document.generation-screens` and `rwb.document.generation-screens.send` (ASM-1867).
- The database login is one per service (DP-02). Its name is Not specified in the source documents (GAP-1016; ASM-1868); the story uses the phrase "the rwb-document login (DP-02)" and never a shared login.

The legacy behaviour is carried unchanged in intent and values: the same user story, rationale, preconditions, flow, eleven exception paths, ten business rules, ten messages, authority, data fields, thirteen acceptance criteria and fifteen test cases, adapted to the target service's schema, topic, API base and contracts.

### 2. Business rationale

The officer today copies case facts into three Word files, prints them and walks them to signature, and a late change is made by hand on the printed copy with no record. These screens produce the set from the approved treatment through the generation engine, let the officer correct an allowed value with a recorded reason, and send the reviewed set for signature as write-once documents. It meets REQ-DCM-012 and REQ-OCC-002, applies CTL-12 and CTL-14 to the set, and shortens the restructure turnaround, which the program targets at 5 days from 23 days.

The realignment changes the mechanics, not the business rule:

1. One schema, one topic, one API base: `rwb_document`, `rwb.document.events.v1` and `/api/recovery/document/v1` (DP-01, DP-13). No table of another service is read and no monolith table name survives.
2. The set is read from the catalog, not from a copy of it: the current version of each template, its Legal approval, its product group and its merge field list arrive through the `rwb-comms` contract with a fake (DP-11), and the locked-or-overridable rule is a property of that answer, never a value in code (BR3).
3. The case, the treatment and the reference lists become published contracts with mocks and a 2 s timeout (DP-11, DP-07) instead of the in-process module calls the legacy story names.
4. The decision log write becomes the local decision-record library of DP-03, written in the same transaction as the document change and published on `rwb.decision-record.v1`; `rwb-decision` seals it in the central ledger. A failed record changes nothing (BR9, AC9).
5. The document row and every byte stay with the store of RWB-P5-E1024-APP and the storage product: this story promotes a reviewed set to write-once, it never writes a blob itself and it never overwrites one (BR7).
6. Marking a draft reviewed is the review operation of RWB-P5-E1054-APP and not a second endpoint of this story; the state the button sets is the same REVIEWED the legacy story names.
7. Sending starts the signature request through the `rwb-comms` contract instead of the in-process `SignatureRequests` interface; P6 chooses the signature path by product and Legal rule (BR8, REQ-OCC-009), and a refused request leaves the set REVIEWED (AC12).
8. The screens move behind the gateway-bff composite route (DP-19), so SCR-14 and SCR-30 call the owner once and gateway-bff merges the answer; the two new panel reads of 12.1 exist because the legacy flow had no endpoint for them (GAP-1016; ASM-1858).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P5-E2017-CON | The published baseline of the two screen reads, the regenerate and send operations, the three signature-request operations `rwb-comms` calls, the shapes, the state values, the error envelope and the `Idempotency-Key` rule |
| RWB-PLT-E1027-CON | The decision-record library: the D6.4 record inside the caller's transaction, published on `rwb.decision-record.v1` (DP-03) |
| RWB-PLT-E1043-CON | The reference-data client library for the product group, document type, review, document source and signature lists (DP-07) |
| RWB-PLT-N001-CON | The gateway-bff composite route that publishes SCR-14 and SCR-30 inside the case record view (DP-19) |
| RWB-P5-E2026-APP | The generation engine and its `generate` activity: the `GenerateRequest`, the `GenerationResult`, the document row it creates in state DRAFT with `write_once` false, and the template code and version it keeps on that row |
| RWB-P5-E1054-CON | The review operation API-P5-014 `POST /documents/{documentId}/review` action COMPLETE, which sets a generated draft to REVIEWED and carries `review_status` |
| RWB-P3-E1043-CON | `rwb-case`'s reference-data contract, which resolves the six lists (DP-07) |
| RWB-PLT-TE012-APP | The platform storage product: the containers `rwb-docs`, `rwb-docs-legal` and `rwb-quarantine`, the managed identity and the WORM policy (the X dependency) |

Business preconditions carried from RWB-E2-017, in the target wording:

- RWB-E2-026 (generation engine) is done: in the target this is RWB-P5-E2026-APP in the same service, called through its published operation. RWB-E1-034 (template versions with Legal approval) is P6's catalog, consumed through RWB-P6-E1046-CON. RWB-E1-054 (review endpoint) is RWB-P5-E1054-APP. RWB-TE-012 (write-once container) is RWB-PLT-TE012-APP.
- RWB-E2-018 provides SignatureRequests in P6; in the target that is the `rwb-comms` operation API-P6-009 and its own story, and until it is live the send step stays behind its flag.
- The document set per treatment type is in reference data: DEED_IN_LIEU uses DIL-CONTRACT, DIL-CA and DIL-MORTGAGE; RESTRUCTURE uses RES-AGREEMENT (assumed; DL28). The set is a data row of the catalog, confirmed by Legal and the product owner; its field-level shape is Not specified in the source documents (GAP-1016; ASM-1861).
- The merge field catalog marks each merge field as overridable or locked. Amounts, parties, title numbers and the treatment terms are locked; dates of signing and witness details are overridable (assumed; DL28). The TSD P6 T3.1 `merge_field` table carries no such flag, so the flag is read as a property of the catalog answer and a field with no flag is treated as locked (GAP-1016; ASM-1859).
- CONTRACT, CREDIT_APPROVAL and MORTGAGE_DOCUMENT are legal types in the document type table (assumed; DL19). The type list is reference data with no enumerated value row for these three in TSD P5 T3.2 (GAP-1016; ASM-1861).
- The officer holds RW-RESTRUCT (Documents CRU, Treatment and offer CRUA) with scope over the case. The authorisation decision is `rwb-access`'s and is consumed as the cached permission decision the service holds; this story adds no guard of its own.
- The `rwb-comms` catalog contract, the `rwb-treatment` contract, the `rwb-case` contract and the `rwb-decision` ledger are reachable and faked; none of the four appears in this story's contract-dependency list, which names `RWB-P3-E1043-CON` only (ASM-1863).
- The release date 31 December 2026 is the legacy one and is tentative (ASM-1868), and the story carries Status Draft (realignment v1) because no approval of the realigned story is recorded (ASM-1868).
- Feature flags `rwb.document.generation-screens` and `rwb.document.generation-screens.send` are on; they replace the legacy `rwb.dochub.generation-screens` and `rwb.dochub.generation-screens.send` (ASM-1867).

The two screen reads of 12.1, the send path and the three signature-request operations are Not specified in the source documents (GAP-1016; ASM-1857, ASM-1858, ASM-1864); the baseline RWB-P5-E2017-CON fixes the names this story is built against.

### 4. Flow

1. Restructuring officer: opens SCR-14 Treatment record for an approved deed in lieu treatment through the gateway-bff composite route and chooses Generate documents. The panel reads the set through `GET /api/recovery/document/v1/cases/{caseId}/generated-documents` (12.1) and the template set through the `rwb-comms` catalog contract (DP-11).
2. System: shows the document set for the treatment type and product, with the current approved version of each template read from the catalog and its Legal approval (BR1, BR2, BR8).
3. Restructuring officer: confirms; the system calls the generation engine (RWB-P5-E2026-APP) at `POST /api/recovery/document/v1/cases/{caseId}/generated-documents` with `GenerateRequest` and an `Idempotency-Key`, and shows the three drafts with their merge values. The engine runs the `generate` activity on queue `rwb-document`.
4. Restructuring officer: opens a draft; the system shows the PDF next to the list of merge values through `GET /api/recovery/document/v1/documents/{documentId}/merge-values`, with locked values read only, and the PDF through the content read of RWB-P5-E1024-APP.
5. Restructuring officer: corrects an overridable value and enters the reason.
6. System: writes a decision record with the override and its reason through the DP-03 library, calls `POST /api/recovery/document/v1/documents/{documentId}/regenerate` with `RegenerateRequest` (the overrides and the `version` lock), which regenerates the draft as the next `doc_version` through the engine and keeps the earlier version readable.
7. Restructuring officer: marks each draft reviewed; the system calls the review operation API-P5-014 action COMPLETE (RWB-P5-E1054-APP) and the document state is REVIEWED.
8. Restructuring officer: chooses Send for signature.
9. System: checks every document of the set is REVIEWED and on the current template version (BR6); copies each final file to the write-once container `rwb-docs-legal` through the store of RWB-P5-E1024-APP and the storage product RWB-PLT-TE012-APP (ASM-1862); writes the decision record for the send with the final call the legacy criterion names through DP-03; starts one signature request through the `rwb-comms` operation API-P6-009 and records the request in `signature_request`; sets each document to state SENT with `write_once` true. The endpoint is `POST /api/recovery/document/v1/cases/{caseId}/generated-documents/send` (12.1).
10. System: shows MSG-P5-012; the documents show as sent on SCR-30 Case documents, read back through the contract.

The decision record is written before the change takes effect and inside the same transaction: a failed record leaves the document, its version and the signature request unchanged (R-UNI-39, AC9, AC15). The write-once copy is idempotent by the content hash, and the send is idempotent by the `Idempotency-Key` and by the state of the set (BR10, AC10).

### 5. Exception paths

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

Three target-service notes:

- X1 is answered by the `rwb-treatment` contract read before the panel enables Generate, and again by the engine on the same rule; the panel disables the button with MSG-P5-011 and the direct call to the generate operation answers 409 with MSG-P5-011, exactly as the legacy criterion states.
- X6 and X9 are the two failures of the send transaction: the record is written first, so a refused record leaves the set REVIEWED and no file in `rwb-docs-legal`; a refused `rwb-comms` answer leaves the same state, and a second send after the service returns completes with one signature request (AC12). Both raise MSG-GEN-006 or MSG-P7-003 naming the system that failed, with {system} = "e-signature".
- X11 is the authorisation decision of `rwb-access`, consumed as the cached permission decision of the service template; a role without Documents U hides the actions on both screens and a direct call answers 403 with MSG-P4-002.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the engine (RWB-P5-E2026-APP) in the same service, the review operation (RWB-P5-E1054-CON), the contract baseline (RWB-P5-E2017-CON), the store, the decision-record library, the reference-data library, the gateway route and the storage product, all earlier or contract work |
| Negotiable | The set per treatment type and which fields may be overridden are data owned by Legal and the product owner; the shapes come from the contract baseline |
| Valuable | The officer produces and sends the set without re-keying and every change is recorded |
| Estimable | Four operations, three internal signature-request operations, two panel reads on SCR-14 and one review view on SCR-30 |
| Small | Fits in two weeks with its tests |
| Testable | Each scenario below is one test with synthetic data |

### 7. Acceptance criteria

```gherkin
Feature: Contract, CA and mortgage document generation screens

  Background:
    Given case "RW-2026-000401" with product group "MORTGAGE" in team "FCR-BKK"
    Given treatment "TRT-0401" of type "DEED_IN_LIEU" approved at D6.4 with no outcome
    Given the set for "DEED_IN_LIEU" is "DIL-CONTRACT" version 2, "DIL-CA" version 1 and "DIL-MORTGAGE" version 1, all approved by Legal
    Given a restructuring officer with role RW-RESTRUCT and scope team "FCR-BKK"
    Given the rwb-comms template catalog contract mock returns "DIL-CONTRACT" version 2, "DIL-CA" version 1 and "DIL-MORTGAGE" version 1 in Thai for product group "MORTGAGE", each with approved_by_legal true
    Given the rwb-treatment contract mock returns treatment "TRT-0401" of type "DEED_IN_LIEU" approved with decision_log_id set and no outcome
    Given the rwb-case contract mock returns case "RW-2026-000401" with product group "MORTGAGE" for role RW-RESTRUCT
    Given the rwb-decision contract mock returns the central ledger reference for decision code "D6.4"
    Given the rwb-comms signature contract mock returns "ACCEPTED" with request "RS-0301"

  Scenario: AC1 Generate (legacy RWB-E2-017 AC1)
    Given the officer opens SCR-14 for "TRT-0401"
    When the officer chooses Generate documents and confirms
    Then the system produces three documents from the current template versions with the case facts filled
    Then they show as drafts of types "CONTRACT", "CREDIT_APPROVAL" and "MORTGAGE_DOCUMENT" with template versions 2, 1 and 1

  Scenario: AC2 Review (legacy RWB-E2-017 AC2)
    Given the contract draft "DOC-0411" at doc_version 1 has contract_date "2026-12-10"
    When the officer corrects contract_date to "2026-12-12" with reason "Signing appointment moved by the customer"
    Then the system writes a decision log entry with decision code "D6.4", the old and new value and the reason as override_reason
    Then the system regenerates "DOC-0411" as doc_version 2 showing "12 December 2569 BE"
    Then doc_version 1 stays readable

  Scenario: AC3 Send (legacy RWB-E2-017 AC3)
    Given the three drafts of "TRT-0401" are in state "REVIEWED"
    When the officer chooses Send for signature
    Then each file is in the write-once container and each document has write_once true and state "SENT"
    Then the system starts one signature request for the three documents in P6
    Then the system writes a decision log entry with final_call "SENT_FOR_SIGNATURE"
    Then the screen shows MSG-P5-012 with count 3

  Scenario: AC4 Generate for a treatment that is not approved (legacy RWB-E2-017 AC4)
    Given treatment "TRT-0402" of type "DEED_IN_LIEU" has no decision_log_id
    When the officer opens SCR-14 for "TRT-0402"
    Then the system disables generate documents with MSG-P5-011
    Then a direct call to POST generated-documents returns 409 with MSG-P5-011

  Scenario: AC5 A correction without a reason (legacy RWB-E2-017 AC5)
    Given the draft "DOC-0411"
    When the officer corrects contract_date with an empty reason
    Then the response is 422 with MSG-GEN-001 naming "Reason"
    Then "DOC-0411" stays at its doc_version

  Scenario: AC6 A locked value cannot be corrected (legacy RWB-E2-017 AC6)
    Given transfer_price is locked in the merge field catalog
    When the officer tries to change transfer_price on "DOC-0411" from 1250000.00 to 1200000.00
    Then the response is 422 with MSG-P5-014 naming "Transfer price"
    Then nothing changes

  Scenario: AC7 Send with a draft not reviewed (legacy RWB-E2-017 AC7)
    Given two drafts of "TRT-0401" are "REVIEWED" and "DIL-MORTGAGE" is still "DRAFT"
    When the officer chooses Send for signature
    Then the response is 422 with MSG-P5-013 naming the mortgage document
    Then the system copies no document to the write-once container and no signature request starts

  Scenario: AC8 A sent document cannot be changed (legacy RWB-E2-017 AC8)
    Given "DOC-0411" is in state "SENT"
    When the officer tries to correct contract_date
    Then the response is 409 with MSG-P5-002
    Then "DOC-0411" is unchanged

  Scenario: AC9 The decision log write fails on a correction (legacy RWB-E2-017 AC9)
    Given the decision log store does not accept writes
    When the officer corrects contract_date on "DOC-0411" with a reason
    Then the response is 503 with MSG-P7-003
    Then "DOC-0411" stays at its doc_version and no file is added

  Scenario: AC10 Send chosen twice (legacy RWB-E2-017 AC10)
    Given the officer chose Send for signature for "TRT-0401" with Idempotency-Key "S-0401"
    When the same request with Idempotency-Key "S-0401" arrives again
    Then the response returns the same three documents in state "SENT"
    Then only one signature request exists for "TRT-0401"

  Scenario: AC11 Two officers correct the same draft (legacy RWB-E2-017 AC11)
    Given two officers opened "DOC-0411" at version 4
    Given the first officer saved a correction, so the record is at version 5
    When the second officer saves a correction with version 4
    Then the response is 409 with MSG-GEN-004

  Scenario: AC12 The signature service refuses the request (legacy RWB-E2-017 AC12)
    Given SignatureRequests in P6 returns "UNAVAILABLE"
    When the officer chooses Send for signature for the three reviewed drafts
    Then the response is 503 with MSG-GEN-006 naming "e-signature"
    Then the documents stay in state "REVIEWED"
    Then a second send after the service returns completes with one signature request

  Scenario: AC13 The template changed after the drafts were made (legacy RWB-E2-017 AC13)
    Given the three drafts were made from "DIL-CONTRACT" version 2
    Given "DIL-CONTRACT" version 3 became current after the drafts were made
    When the officer chooses Send for signature
    Then the response is 422 with MSG-P5-013 naming the contract and "template version 3"
    Then the system sends no document
```

Every Given, When and Then line above is the legacy line unchanged, with every identifier, amount, date and message kept character for character. The only added lines are the six Background Givens that mock the cross-service parts: the `rwb-comms` template catalog contract, the `rwb-treatment` treatment, the `rwb-case` case, the `rwb-decision` central ledger and the `rwb-comms` signature contract. In the target the legacy endpoints of section 12 of the story map to the operations of 12.1 and 12.2 as `POST monolith-base/cases/{caseId}/generated-documents` → `POST /api/recovery/document/v1/cases/{caseId}/generated-documents` (RWB-P5-E2026-APP, same service), `POST /documents/{documentId}/regenerate` → `POST /api/recovery/document/v1/documents/{documentId}/regenerate`, `POST monolith-base/documents/{documentId}/review` → `POST /api/recovery/document/v1/documents/{documentId}/review` (API-P5-014, RWB-P5-E1054-APP) and `POST /treatments/{treatmentId}/signature-requests` → `POST /api/recovery/comms/v1/treatments/{treatmentId}/signature-requests` (API-P6-009, P6 rwb-comms, consumed). In AC3 the "write-once container" is `rwb-docs-legal` and the "signature request in P6" is the `rwb-comms` operation; in AC9 the "decision log store" is the decision-record library and the ledger contract of `rwb-decision`.

### 8. Business rules

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

Target-service statements that make the rules hold in `rwb-document`:

- BR1 and BR2 are executed against the `rwb-comms` catalog answer and the `rwb-treatment` answer: the treatment type, the approval and the `decision_log_id` arrive in one answer, and the set and the version are the catalog's, so no set and no version is held in this service (DP-01, DP-11).
- BR3 and BR4 are executed by `OverrideValidator` over the catalog answer (the lock flag and the reason) and by the decision-record library of DP-03 written inside the caller's transaction before the regeneration is called (R-UNI-39).
- BR5 is executed by the engine: the regeneration is a new `document` row at `doc_version + 1` through the store, and an earlier version is never overwritten because the store writes every version at a new blob path.
- BR6 is executed by `DocumentSetService` over the set read and the catalog answer: the state of every document of the set and its `template_version` are compared with the current version before the first byte is copied, and the refusal names the document and the reason.
- BR7 is executed by the store of RWB-P5-E1024-APP and the storage product: the file goes to `rwb-docs-legal`, `write_once` becomes true and is never reset, and a later change is a new version created before send only.
- BR8 is executed by `rwb-comms`: this story never chooses the path, it passes the treatment and the documents and shows the answer of P6 (REQ-OCC-009).
- BR9 and BR10 are executed by the decision-record library, the `Idempotency-Key` row of the platform library in `rwb_document` and the state check of the send.
- The lists of BR1 and BR3 arrive through the reference-data contract (DP-07); the two panel reads are published behind the gateway-bff composite route (DP-19); the legacy base is rebased (DP-13).

### 9. State transitions

None. This story does not change a case status. It changes the document state.

| From | Event | Condition | To |
|---|---|---|---|
| document state DRAFT | Correction saved | Overridable field, reason given, decision log written | DRAFT, doc_version + 1 |
| document state DRAFT | Marked reviewed | None | REVIEWED |
| document state REVIEWED | Correction saved | As above | DRAFT, doc_version + 1 |
| document state REVIEWED | Send for signature | All of the set REVIEWED, current template version, decision log written, signature request accepted | SENT, write_once true |

Target columns written by the same transitions:

| Column | Value in this story |
|---|---|
| `document.state` | DRAFT, REVIEWED or SENT, written through the store of RWB-P5-E1024-APP |
| `document.doc_version` | The next integer on a correction, written by the engine and the store |
| `document.review_status` | CONFIRMED or CORRECTED on a correction, per LOV-REVIEW; the review operation of RWB-P5-E1054-APP writes it |
| `document.write_once` | false until the send, true after it, never reset |
| `document.storage_ref` | The new blob path of each version, written by the store |
| `signature_request.status` | QUEUED when P6 accepts the request; SENT, SIGNED, DECLINED and EXPIRED belong to `rwb-comms` and its own story |

The three state values DRAFT, REVIEWED and SENT are the legacy values and no list enumerates them in any source; the baseline RWB-P5-E2017-CON declares them as the values of the field (GAP-1016; ASM-1860). No transition out of SENT happens: the signed copy is a new version added by `rwb-comms` through the contract, never a change of a sent document.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT, restructuring officer (FCR) | Generates, corrects, marks reviewed and sends in scope (Documents CRU) |
| RW-CASEOWN, case owner | Generates, corrects, marks reviewed and sends in scope (Documents CRU) |
| RW-TEAMMGR, team manager | Reads the drafts and sent documents (Documents R) |
| RW-LEGAL, legal counsel | Reads the set; owns which fields are overridable (Documents CRUA) |
| SY-DECLOG, decision log writer | Writes the correction and send entries |

No approval level from the delegation of authority applies; the treatment was approved at D6.4 before generation.

In the target the authorisation decision is taken by `rwb-access` (roles as data, scope, masking and DoA in `rwb_access`) and consumed as the cached permission decision the service holds; this story adds no guard of its own and inherits the 403 shapes of MSG-P4-002 and MSG-P4-003. SY-DECLOG is the local decision-record library of DP-03 in the target, called inside the caller's transaction, and it publishes the record on `rwb.decision-record.v1`; `rwb-decision` (P7) owns the central ledger. The service identity that writes the `signature_request` rows and the outbox rows is the rwb-document login (DP-02), whose name is Not specified in the source documents (GAP-1016; ASM-1868).

### 11. Data

| BR Field ID | Table in `rwb_document` or contract | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | `rwb-case` case, through the contract | id | Read |
| DF-CAS-002 | `rwb-case` case, through the contract | case_no | Read |
| DF-CAS-003 | `rwb-case` case, through the contract | product_group | Read |
| DF-TRT-001 | `rwb-treatment` treatment, through the contract | id | Read |
| DF-TRT-003 | `rwb-treatment` treatment, through the contract | decision_log_id | Read |
| DF-TRT-004 | `rwb-treatment` treatment, through the contract | treatment_type | Read |
| DF-TRT-013 | `rwb-treatment` treatment, through the contract | outcome | Read |
| DF-REF-046 | `rwb-comms` template catalog, through the contract | template_code | Read |
| DF-REF-047 | `rwb-comms` template catalog, through the contract | template_version | Read |
| DF-REF-051 | `rwb-comms` template catalog, through the contract | approved_by_legal | Read |
| DF-DOC-001 | `document` | id | Read, through the store |
| DF-DOC-004 | `document` | document_type | Read, through the store |
| DF-DOC-006 | `document` | storage_ref | Write, through the store |
| DF-DOC-008 | `document` | review_status | Write, through the store and the review operation |
| DF-DOC-010 | `document` | write_once | Write, through the store |
| DF-DOC-011 | `document` | doc_version | Write, through the store |
| DF-DOC-032 | `document` | template_id | Read, through the store |
| DF-DOC-033 | `document` | treatment_id | Read, through the store |
| (added column) | `document` | template_code and template_version, added by RWB-P5-E2026-APP | Read |
| Standard column | `document` | state, version | Write, through the store |
| DF-DOC-096 to DF-DOC-107 | `signature_request` | id, case_id, treatment_id, document_id, party_id, method, status, external_ref, sent_at, signed_at, signed_document_id, expires_at | Write on send, read on the repeat |
| DF-DEC-001 to DF-DEC-018 | decision-record library table in `rwb_document` | all fields, with decision code D6.4, the final call and the inputs reference | Write, through the library |
| (parameter) | `document_hub_parameter` | `GEN_IDEMPOTENCY_HOURS`, whose value 24 is loaded as a row | Read |
| (reference list) | `rwb-case` reference data, through the contract | the product group, document type, review, document source and signature lists | Read |
| (merge value) | the catalog answer, not persisted | the merge code, its value, its format and its locked or overridable flag | Read |

Field IDs are those in the Logical Data Model and Data Dictionary and the TSD P5 T3.1 table. No `recovery_case`, `treatment`, `template`, `merge_field` or `decision_log_entry` row is read or copied: those arrive inside the four contract answers, and DP-01 forbids a foreign-schema read. Merge values are read on the reviewer's screen and are never written to a log, an event or a decision record: the record carries the inputs reference, never the value. The `signature_request` rows carry identifiers and status values only, never a signature image and never a party name; the table itself is created by the per-service migration sequence of `rwb_document` and not by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-document (P5); base `/api/recovery/document/v1`; the shapes are those of RWB-P5-E2017-CON.

| Method | Path | Owner | Notes |
|---|---|---|---|
| GET | `/api/recovery/document/v1/cases/{caseId}/generated-documents` | P5 | The generated set of a case for the SCR-14 panel: query `treatmentId`, `state`; answer 200 `GeneratedDocumentSetPage` with the documents of the case, each carrying `documentId`, `treatmentId`, `documentType`, `templateCode`, `templateVersion`, `state`, `writeOnce`, `docVersion` and `reviewStatus`; Documents R with scope applied. The path and the shape are Not specified in the source documents (GAP-1016; ASM-1858) |
| GET | `/api/recovery/document/v1/documents/{documentId}/merge-values` | P5 | The merge values of one generated draft for the review view: answer 200 `MergeValuePage` with `documentId`, `docVersion`, `templateCode`, `templateVersion`, `state`, `writeOnce` and `values[]`, each `mergeCode`, `label`, `value`, `formattedValue`, `locked` and `reason`; each read written to the PII access log. The path and the shape are Not specified in the source documents (GAP-1016; ASM-1858) |
| POST | `/api/recovery/document/v1/documents/{documentId}/regenerate` | P5 | API-P5-017. `RegenerateRequest`: `overrides[]` of `mergeField`, `value` and `reason` (1 to 10), and `version` as the optimistic lock; header `Idempotency-Key` required; answer 200 `Document` at the new `doc_version`; Documents U, scope applied |
| POST | `/api/recovery/document/v1/cases/{caseId}/generated-documents/send` | P5 | The send for signature: `SendForSignatureRequest` (`treatmentId` uuid required, `documentIds[]` uuid required) and a required `Idempotency-Key`; answer 200 `DocumentPage` with the sent documents. Documents U, scope applied. No API ID exists for this operation in TSD P5 T-A.1 (GAP-1016; ASM-1857) |
| POST | `/api/recovery/document/v1/treatments/{treatmentId}/signature-requests` | P5 | Internal operation `rwb-comms` calls: writes a `signature_request` row with document, party, method and expiry and answers 201 `SignatureRequest`; service identity only. The name and the field names are Not specified in the source documents (GAP-1016; ASM-1864) |
| GET | `/api/recovery/document/v1/signature-requests` | P5 | Internal operation `rwb-comms` calls to resolve a result by `externalRef`; answer 200 `SignatureRequest` or 404; service identity only. The name is Not specified in the source documents (GAP-1016; ASM-1864) |
| PATCH | `/api/recovery/document/v1/signature-requests/{requestId}` | P5 | Internal operation `rwb-comms` calls to set status, `sent_at`, `signed_at` and `signed_document_id`; answer 200 `SignatureRequest`; service identity only. The name and the field names are Not specified in the source documents (GAP-1016; ASM-1864) |

#### 12.2 REST operations consumed

| Method | Path | Owner | Story | Note |
|---|---|---|---|---|
| POST | `/api/recovery/document/v1/cases/{caseId}/generated-documents` | P5 rwb-document | RWB-P5-E2026-APP | The generation engine, same service: `GenerateRequest` in, 201 `GenerationResult` out; one hop, 2 s, breaker |
| POST | `/api/recovery/document/v1/documents/{documentId}/review` | P5 rwb-document | RWB-P5-E1054-APP | API-P5-014 action COMPLETE: sets a generated draft to REVIEWED; the shape is RWB-P5-E1054-CON's; one hop, 2 s |
| POST | `/api/recovery/document/v1/documents/{documentId}/store` | P5 rwb-document | RWB-P5-E1024-APP | The store command: the row, the promotion to `write_once` true and the file in `rwb-docs-legal`; same service, one hop |
| GET | `/api/recovery/comms/v1/admin/templates` | P6 rwb-comms | RWB-P6-E1046-CON | The current version by code, language, product group and date, with its Legal approval. Consumed and faked; in no C row (ASM-1863) |
| GET | the template catalog merge field list of a version | P6 rwb-comms | RWB-P6-E1046-CON | The merge codes, their required flag, their format and their locked or overridable flag; the path is Not specified in the source documents (GAP-1016; ASM-1859) |
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | the S2 contract, consumed and faked | The type, the approval, the `decision_log_id` and the outcome; in no C row (ASM-1863) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | RWB-P3-E1018-CON, consumed and faked | The case and its product group for the set and the reference-data match; in no C row (ASM-1863) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | RWB-P3-E1043-CON | The product group, document type, review, document source and signature lists (DP-07) |
| POST | `/api/recovery/comms/v1/treatments/{treatmentId}/signature-requests` | P6 rwb-comms | API-P6-009, consumed and faked | Starts the signature request; answer `ACCEPTED` with a request ID or `UNAVAILABLE`; in no C row (ASM-1857) |
| POST | the central ledger sealing operation of `rwb-decision` | P7 rwb-decision | RWB-P7-E1027-CON, consumed and faked | The seal of the local D6.4 record; in no C row (ASM-1863) |

Every row is one hop with a 2 s timeout, a GET retry once with jitter and a breaker per downstream (DP-11, ADR-020). A failed read maps to 503 with MSG-GEN-006 naming the system that failed and never to a sent set. The three in-service operations of RWB-P5-E2026-APP, RWB-P5-E1054-APP and RWB-P5-E1024-APP are same-service calls and appear in 12.9 as REST consumed inside the service.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (decision record, decision code D6.4) | `rwb.decision-record.v1` | PLT library, consumed by P7 | caseId | the hash-chained record with the decision code D6.4, the final call the legacy criteria name (`GENERATED`, the override final call and `SENT_FOR_SIGNATURE`), the old and new value and the reason of an override as the inputs reference, never the merge value itself |

CloudEvents 1.0 envelope, binary mode. The record is written to the outbox inside the caller's transaction by the DP-03 library, so it exists exactly when the document change exists. This story declares no new `rwb.document.*` event: the service has exactly `rwb.document.DocumentStored.v1` and `rwb.document.DocumentFieldsExtracted.v1` (Architecture v5 slide 42), neither of which is the state change of this key, and the state is read back through the contract of 12.1 (GAP-1016; ASM-1866).

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| None | — | — | The path is started by the officer's request, not by an event: the set, the treatment, the case, the catalog and the lists are synchronous reads, and the signature result reaches this service through the `rwb-comms` contract, not through a topic |

#### 12.5 Workflows and activities

| Name | Kind | Queue | Note |
|---|---|---|---|
| `generate` | Activity, owned by RWB-P5-E2026-APP | `rwb-document` | Called synchronously by the generate and the regenerate operations; named here only, not registered and not changed by this story |
| None in this story | — | `rwb-document` | The reads, the review action and the send are synchronous REST operations in one transaction each; this story registers no workflow, no activity and no child workflow |

#### 12.6 Schedules

| Schedule | Workflow | Queue | Interval | Note |
|---|---|---|---|---|
| None | — | `rwb-document` | — | This story starts no Schedule and no timer; JOB-12 and JOB-17 belong to RWB-P5-E1032-APP and RWB-P5-E1017-APP |

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `document` | P5 | Read for the two panel reads; state, `doc_version`, `review_status`, `storage_ref` and `write_once` written only through the store of RWB-P5-E1024-APP |
| `document_type` | P5 | Read only: the legal flag and the retention class of a generated type |
| `signature_request` | P5 | Written on send and read back for the repeat and for `rwb-comms` (DF-DOC-096 to DF-DOC-107) |
| `document_hub_parameter` | P5 | Read only: the `GEN_IDEMPOTENCY_HOURS` row, which is this service's own parameter table |
| decision-record library table | PLT library, created in `rwb_document` | The D6.4 record of a correction and of a send, inside the caller's transaction |
| outbox, inbox and idempotency library tables | PLT library, created in `rwb_document` | The record row and the `Idempotency-Key` row; platform objects of the service template |

No foreign-schema table is read (DP-01): `template` and `merge_field` are P6's, `recovery_case`, `lov_value`, `parameter_catalog` and `reference_row` are P3's, `treatment` is S2's, `decision_log_entry` is P7's and the ACE views are P1's. The outbox, inbox and idempotency tables are platform library objects created in `rwb_document` (Architecture v5 slide 20); this key claims no outbox-pattern and no migration-pattern dependency of its own, the record being written by the DP-03 library and `signature_request` being created by the per-service migration sequence of the service's DB story.

#### 12.8 Contract fakes

| Fake | Story | Used for |
|---|---|---|
| rwb-comms template catalog fake | RWB-P6-E1046-CON | The three approved templates of AC1 with versions 2, 1 and 1; version 3 current from 2026-12-15 for AC13; a withdrawn and an unapproved version; the merge field list with the locked flag of transfer_price for AC6 |
| rwb-treatment fake | the S2 contract, consumed and faked | The approved deed in lieu treatment "TRT-0401" and the refused "TRT-0402" of AC4 |
| rwb-case case fake | RWB-P3-E1018-CON | The case and its product group, and the scope refusal behind MSG-P4-003 |
| reference-data fake | RWB-P3-E1043-CON (through RWB-PLT-E1043-CON) | The product group, document type, review, document source and signature lists |
| rwb-comms signature fake | API-P6-009, consumed and faked | `ACCEPTED` with request "RS-0301" for AC3 and AC10, and `UNAVAILABLE` for AC12 |
| decision-record and central ledger fake | RWB-PLT-E1027-CON and RWB-P7-E1027-CON | The local D6.4 record and its seal; the refusing write of AC9 and TC-E2-017-15 |
| store fake or stub | RWB-P5-E1024-APP | The `Document` answer, the promotion to `write_once` true and the COPY_PENDING state |
| generation engine stub | RWB-P5-E2026-APP | The `GenerationResult` of AC1 and the regenerate answer of AC2, so the panel and the review view build before the engine lands |
| review operation stub | RWB-P5-E1054-CON | The REVIEWED state of AC3 and the refusal of AC8 |
| screen baseline fake | RWB-P5-E2017-CON | The two reads, the regenerate, the send and the three signature-request operations, so the screens build on Day 1 |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 7, consumed 7 cross-service plus 3 in-service | The two panel reads, the regenerate, the send and the three signature-request operations; the catalog, treatment, case, list, signature-start and ledger calls; the engine, the review action and the store of the same service |
| Kafka | Published 1 decision record; consumed 0 | `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`; no new `rwb.document.*` event |
| Temporal | 1 activity observed | `generate` on queue `rwb-document`, owned by RWB-P5-E2026-APP; no workflow and no Schedule |
| File | 1 copy and 1 read | The final file copied to `rwb-docs-legal` through the storage product RWB-PLT-TE012-APP; the PDF read through the content operation of the store |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, module `document/generation/screens`; front end folder `recovery/documents/generation`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| GeneratedDocumentController | Controller | The four public operations of 12.1 and the three internal signature-request operations; access check, scope filter and the RFC 9457 error mapping |
| DocumentSetService | Service | The set read; the correction flow with the decision record; the review action through API-P5-014; the send with BR6, BR7, BR9 and BR10 |
| OverrideValidator | Service | Reads the lock flag and the required flag from the catalog answer, refuses a locked field (MSG-P5-014) and an empty reason (MSG-GEN-001) |
| WriteOncePromoter | Service | Copies each final file to `rwb-docs-legal` through the storage product and the store, idempotent by the content hash, and sets `write_once` |
| SignatureRequestClient | Client | Calls the `rwb-comms` operation API-P6-009 with a 2 s budget and a breaker; maps `UNAVAILABLE` to MSG-GEN-006 |
| SignatureRequestRepository | Repository | Reads and writes `signature_request` only; `version` is the optimistic lock |
| DocumentHubRepository | Repository | Reads `document` and `document_type`; writes nothing directly, every document write going through the store |
| GenerateDocumentsPanel | React component | On SCR-14: the set, the template versions, Generate and Send, the disabled states and MSG-P5-011 |
| GeneratedDocumentReview | React component | On SCR-30: the PDF, the merge values with locked ones read only, the correction form with a reason, Mark reviewed |

**Database.**

- No new table and no new column of this story: the `document` columns are written through the store of RWB-P5-E1024-APP, and `signature_request` is created by the per-service migration sequence of the service's DB story.
- `signature_request` is read and written by `SignatureRequestRepository`; the send writes one row per request with `status` QUEUED, `sent_at` and `external_ref`, and the result path of `rwb-comms` sets `status`, `signed_at` and `signed_document_id`.
- No index is added by this story; the store's own unique key on the document and the state check of the send carry the duplicate rule.

**Configuration and reference data.**

- Template set per treatment type and product, the merge field list with its locked or overridable flag, and the type mapping (P6 catalog; owner Legal counsel and the product owner; DL28, DL19).
- The six lists through the reference-data contract (DP-07); no list value is typed in code.
- Parameter `GEN_IDEMPOTENCY_HOURS` 24, read from `document_hub_parameter` in `rwb_document` (ASM-1865).
- Decision code D6.4 and the final calls of the legacy criteria; the LOV-DECISION list is the data steward's (ASM-1866).
- Feature flags `rwb.document.generation-screens` and `rwb.document.generation-screens.send`. Off: the panel is hidden; off on the second only: the send button is hidden and a direct call answers 404 (ASM-1867).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 moves every table the legacy story touched into its owner's schema: `document`, `document_type`, `signature_request` and `document_hub_parameter` are `rwb_document`'s, and `template`, `merge_field`, `recovery_case`, `treatment` and `decision_log_entry` stay with P6, P3, S2 and P7 and are reached only through their contracts. DP-03 replaces `DecisionLogWriter` with the local library, so the override record, the send record and the document change share one transaction and the record is published on the shared topic. DP-07 keeps the six lists out of the code through the reference-data contract and its client library. DP-11 turns the in-process `SignatureRequests` interface and the legacy catalog, treatment and case reads into published contracts with fakes and a 2 s timeout each. DP-13 rebases the legacy `/api/recovery/v1` paths on `/api/recovery/document/v1`. DP-19 puts SCR-14 and SCR-30 behind the gateway-bff composite route, so the browser calls the owner once and the merge happens in gateway-bff.

**Build steps**

1. Build the two panel reads over the store and the catalog fake; unit test the set answer and the merge value answer with locked and overridable fields.
2. Build `OverrideValidator`; unit test AC5 and AC6, including a field with no lock flag treated as locked.
3. Build the correction flow with the decision record and the regenerate call; integration test AC2, AC9 and AC11.
4. Build the review action call to API-P5-014 and test the REVIEWED transition and the refusal of AC8.
5. Build the send: BR6 checks, the write-once copy through the store and the storage product, the record, the `rwb-comms` call and the state SENT, with the failure handling of AC9 and AC12.
6. Build the three internal signature-request operations and test them against the `rwb-comms` fake.
7. Build `GenerateDocumentsPanel` on SCR-14 with the disabled state of AC4 and MSG-P5-011, and `GeneratedDocumentReview` on SCR-30 with the correction form, the read-only state for locked fields and for RW-TEAMMGR.
8. Add the contract tests against RWB-P5-E2017-CON and the browser tests through the gateway-bff route; run the access test TC-E2-017-14 and the resilience test TC-E2-017-15.

**Done when.** The tests in section 16 pass and a restructuring officer generates, corrects and sends one synthetic deed in lieu set in UAT, with the three files in `rwb-docs-legal`, one signature request, one D6.4 record per correction and per send, and no merge value in any log, event or record.

### 14. Validation and messages

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

Delivery shape: every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. The HTTP mapping is the legacy one and is fixed by AC4 to AC12 and the baseline RWB-P5-E2017-CON: 403 for MSG-P4-002, 404 for a document or a treatment that is not found or lies outside the scope (MSG-P4-003), 409 for MSG-P5-002, MSG-GEN-004 and MSG-P5-011, 422 for MSG-GEN-001, MSG-P5-013 and MSG-P5-014, and 503 for MSG-P7-003 and MSG-GEN-006 naming "e-signature". MSG-P5-012 is not an error response: it is the confirmation of a completed send on SCR-14. The 401 message and the not-found message ID are Not specified in the source documents (GAP-1016; ASM-1868).

### 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-14 Treatment record | Loading | Skeleton on the document set while the panel read loads through the gateway-bff composite route |
| SCR-14 Treatment record | Approved | Sees the document set with template versions; chooses Generate documents; Send for signature when all are reviewed |
| SCR-14 Treatment record | Draft, submitted | Generate documents is disabled with MSG-P5-011 |
| SCR-14 Treatment record | refused | A refused send shows MSG-P5-013 naming the document and the reason, and the set keeps its states |
| SCR-30 Case documents | List | Opens a draft, sees the PDF and the merge values, corrects an overridable value with a reason, marks it reviewed |
| SCR-30 Case documents | Read only (common state) | A sent document, or any document for RW-TEAMMGR, shows without edit controls |
| SCR-30 Case documents | reviewed | The document shows state REVIEWED with `write_once` false until the send, then SENT with `write_once` true |

The two screens are reached from SCR-03 Case record and published inside it by the gateway-bff composite route of DP-19 (H RWB-PLT-N001-CON); the browser never calls `rwb-document` directly. The document list, the search and the upload form are RWB-P5-E1026-APP, the store and the version history RWB-P5-E1024-APP, and the review queue RWB-P5-E1054-APP; this story adds the generation panel on SCR-14 and the generation review view on SCR-30. The route path and the fields gateway-bff merges are Not specified in the source documents (GAP-1016; ASM-1858).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-017-14 | Access | Component | RW-TEAMMGR user (Documents R) calls POST generated-documents/send; refused with MSG-P4-002 |
| TC-E2-017-01 | AC1, BR1, BR2 | End to end | Synthetic mortgage DIL treatment, three approved templates |
| TC-E2-017-02 | AC2, BR3, BR4, BR5 | End to end | Contract date moved by two days |
| TC-E2-017-03 | AC3, BR6, BR7, BR8 | End to end | Three reviewed drafts; P6 stub returns ACCEPTED |
| TC-E2-017-04 | AC4, BR2 | End to end | Treatment with no decision_log_id |
| TC-E2-017-05 | AC5, BR3 | End to end | Empty reason |
| TC-E2-017-06 | AC6, BR3 | End to end | Locked transfer price |
| TC-E2-017-07 | AC7, BR6 | End to end | One draft not reviewed |
| TC-E2-017-08 | AC8, BR7 | End to end | Document in state SENT |
| TC-E2-017-09 | AC9, BR4 | End to end | Decision log stub refusing writes on a correction |
| TC-E2-017-10 | AC10, BR10 | End to end | Same send key twice |
| TC-E2-017-11 | AC11 | End to end | Two sessions on one draft |
| TC-E2-017-12 | AC12 | End to end | P6 stub returns UNAVAILABLE, then ACCEPTED |
| TC-E2-017-13 | AC13, BR6 | End to end | Template version 3 made current after the drafts |
| TC-E2-017-15 | Principle 5 | NFR | Decision log write forced to fail on send; nothing sent, documents stay REVIEWED, MSG-P7-003, incident raised |

The legacy level System maps to End to end, Access to Component and Resilience to NFR. The wave-2 integration harness copies TC-E2-017-03 as RWB-ITG-E2017-ITG, where the real `rwb-comms`, `rwb-treatment`, `rwb-case` and `rwb-decision` services replace the fakes. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the set per treatment type, the locked and overridable fields, the legal flag, the six lists and the 24-hour window are data or parameters, read through the catalog, the reference-data contract and the service's own parameter row.
- No personal data in logs, tests or prompts: merge values, reasons and file names are not logged; tests use synthetic parties; the merge value answer is masked by role and every read is written to the PII access log.
- No read of another module's or service's tables: the treatment, the templates, the case, the lists and the signature service are reached through published contracts, one hop, 2 s timeout, and no `v_ace_*` view is read by this service (DP-01).
- A document copied to the write-once container is never changed; a later change is a new document version created before send only, and the store never overwrites a blob.
- The decision record is written in the same transaction as the document change and the signature request; a failure stores nothing and leaves the set REVIEWED (R-UNI-39).
- The send is idempotent twice over: `Idempotency-Key` on the POST, and the state check of the set plus the store's duplicate rule.
- No merge value, no merge snapshot and no file byte in an event, a record or a workflow input: the record carries the inputs reference only.
- The feature flags `rwb.document.generation-screens` and `rwb.document.generation-screens.send` remove the capability without a rollback of the schema (ASM-1867).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-012 | Contracts, credit applications and mortgage documents generated from approved templates with no re-keying | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-OCC-07 | 7.3 Negotiate settlement or deed in lieu; 13 Manage documents and correspondence | R-DIL-14, R-DIL-16, R-DIL-18, R-UNI-39, R-UNI-40 | TC-E2-017-01 to TC-E2-017-12, TC-E2-017-14, TC-E2-017-15 |
| REQ-OCC-002 | Templates versioned with the Legal approval recorded against the version | Business Requirements Program, section 5.6; Epic 2, section 3.5 | FEAT-OCC-07 | 13 Manage documents and correspondence | R-LIT-03 | TC-E2-017-01, TC-E2-017-13 |
| REQ-OCC-009 | A customer signs an agreement electronically where Legal permits it, and by wet ink where Legal requires it | Business Requirements Program, section 5.6; Epic 2, section 4 | FEAT-OCC-07 | 7.3 Negotiate settlement or deed in lieu | R-DIL-18, R-RES-16 | TC-E2-017-03, TC-E2-017-12 |

| Legacy reference | Where it is kept |
|---|---|
| Screens SCR-14 Treatment record and SCR-30 Case documents | Sections 1, 4, 13, 15 |
| Documents DRAFT, REVIEWED and SENT, and the write-once switch | Sections 4, 8, 9, 11, 12.7 |
| Decision code D6.4, the override reason and final_call SENT_FOR_SIGNATURE | Sections 4, 7, 8, 11, 12.3, 13, 14 |
| MSG-P5-011, MSG-P5-012, MSG-P5-013, MSG-P5-014, MSG-P5-002, MSG-GEN-001, MSG-GEN-004, MSG-GEN-006, MSG-P7-003, MSG-P4-002 | Section 14 and the exception paths |
| Rules R-DIL-14, R-DIL-16, R-DIL-18, R-RES-16, R-UNI-14, R-UNI-39, R-UNI-40, R-LIT-03; controls CTL-06, CTL-07, CTL-12, CTL-14 | Sections 2, 8, 17, 18 |
| Template codes DIL-CONTRACT, DIL-CA, DIL-MORTGAGE and RES-AGREEMENT; the type mapping | Preconditions, sections 1, 3, 7, 13 |
| Containers rwb-docs, rwb-docs-legal and rwb-quarantine | Sections 4, 12.9, 13 |
| Legacy key RWB-E2-017, AC1 to AC13, TC-E2-017-01 to TC-E2-017-15 | Metadata, section 7, section 16 |

### 19. Out of scope

- The generation engine, the template selection, the merge rules and the renderer (RWB-P5-E2026-APP; legacy RWB-E2-026).
- The e-signature flow, the wet ink path and the return of the signed copy (`rwb-comms`, API-P6-009 to API-P6-011; legacy RWB-E2-018).
- The store, the write-once container policy, the version history and the content read (RWB-P5-E1024-APP) and the platform storage product (RWB-PLT-TE012-APP).
- The review queue, the field review and the correction of a stored document's type (RWB-P5-E1054-APP; legacy RWB-E1-054).
- Template upload, the merge field catalog and the Legal approval of a version (P6 `rwb-comms`, RWB-P6-E1046-APP; legacy RWB-E1-034 and RWB-E1-046).
- The case documents list, the search and the upload form (RWB-P5-E1026-APP).
- Rule-driven generation on the deed in lieu route (FEAT-TRT-18, Epic 3) and settlement offer letters (R-SET-04, Epic 3).
- The published contract artefacts of this key, their fakes and their versioning (RWB-P5-E2017-CON); the cross-service proof (RWB-ITG-E2017-ITG).
- The Helm chart, the retry policy values, the topic and DLT provisioning, the metrics, the alerts and the runbook.
