# RWB-E2-018 E-signature flow for customers and the bank

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-018 |
| Epic | E2, release 31 December 2026 |
| Module | P6 Communications |
| Feature | FEAT-OCC-08 Run the e-signature flow for the customer and the bank; FEAT-OCC-09 Record the signature result on the case |
| Requirement IDs | REQ-OCC-009 |
| BRD section | Business Requirements Epic 2, sections 3.6 and 4 |
| L3 process | 7.3 Negotiate settlement or deed in lieu |
| Decision | D6.4 |
| Priority | Must |
| Depends on | RWB-E2-017, RWB-E2-022 |
| Status | Ready for build |

## 1. Story

As a **customer (CU-BORROW)**, I want **to sign the agreement on EasyApp or at a branch, with the bank signature added and the signed document returned to the case**, so that **a settlement completes without paper where the law allows**.

## 2. Business rationale

Agreements are printed, signed and couriered today, and the case waits days for the signed copy before booking can start. This story sends the generated agreement for e-signature where Legal permits it, takes branch and paper signatures where Legal requires wet ink, stores the signed copy on the case and records signed or not signed on the treatment, which is the event the routing rules R-RES-16, R-SET-10 and R-DIL-18 act on. It serves REQ-OCC-009.

## 3. Preconditions

- RWB-E2-017 is done: the agreement, credit approval and mortgage documents are generated on the case and stored in the document hub.
- RWB-E2-022 is done: the conduct check for outbound contact is available.
- Each agreement template carries its signature basis: E_SIGNATURE_ALLOWED or WET_INK_REQUIRED, approved by Legal counsel (RWB-E1-046).
- The treatment exists with type, offer validity date and state Offer with customer (RWB-E2-004).
- EasyApp e-signature is reached through the ACE common module (INT-34) with the bank signing certificate held in the key store, assumed; DL12 and DL06. It is not yet in the integration inventory.
- The requester holds RW-RESTRUCT or RW-CASEOWN (Treatment and offer C and U).

## 4. Flow

1. Restructuring officer: on SCR-14 Treatment record chooses Send for signature on a generated agreement.
2. System: reads the signature basis of the agreement's template; offers E-signature only when the basis is E_SIGNATURE_ALLOWED, otherwise Branch or Paper.
3. System: runs the conduct check for the customer (RWB-E2-022); a contact stop or legal hold refuses the request.
4. System: creates the signature request (method, document, party, expiry equal to the treatment's offer validity) and, for E-signature, writes the send to the outbox for the ACE path to EasyApp.
5. Customer: signs in EasyApp; EasyApp adds the bank signature with the bank certificate and returns the signed PDF through the ACE path.
6. System: stores the signed PDF as a new write-once version of the agreement on the case, sets the request Signed and calls TreatmentApi.recordSignature, which raises CUSTOMER_SIGNED in P3.
7. Customer at a branch: signs the paper agreement; the branch scan arrives through JOB-12 Document intake; the restructuring officer links the scan and records Signed.
8. For a deed in lieu with WET_INK_REQUIRED: the officer records the paper signature with the scan; P3 receives CUSTOMER_ACCEPTED with signature basis wet ink and routes to the field inspection and then the Land Office transfer (R-DIL-18, R-DIL-27).
9. System: a decline in EasyApp sets the request Declined and records not signed; an expiry from P3 cancels the request.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | E-signature requested for a document whose template requires wet ink | Refused | MSG-P6-009 | AC4 |
| X2 | The customer declines in EasyApp | Request Declined; treatment not signed | None | AC5 |
| X3 | The offer validity passes with no signature | Request Expired; a later result is refused | None | AC6 |
| X4 | A contact stop is in force | Request refused | MSG-P6-001 | AC7 |
| X5 | The ACE path to EasyApp is unavailable | Send queued and retried | MSG-GEN-006 | AC8 |
| X6 | The same signing result arrives twice | Ignored and counted | None | AC9 |
| X7 | A signing result names no known request | Held on the exception queue | None | AC10 |
| X8 | A branch or paper signature recorded with no scan | Refused | MSG-GEN-001 | AC11 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses documents from RWB-E2-017 and the conduct check from RWB-E2-022; booking after signature is Epic 3 |
| Negotiable | The signature basis per template and the expiry are data; the EasyApp path is the bank's |
| Valuable | A signed copy is on the case within a minute of signing, and routing starts from it |
| Estimable | Three endpoints, one result listener, one table |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion runs with the EasyApp path stubbed |

## 7. Acceptance criteria

```gherkin
Feature: E-signature flow for customers and the bank

  Background:
    Given case "RC-2026-000888" has settlement treatment "T-0501" with offer validity 2026-12-20 and state "OFFER_WITH_CUSTOMER_SET"
    Given agreement document "D-0601" on the case was generated from template "SET-AGREE" "TH" with signature basis "E_SIGNATURE_ALLOWED"
    Given the borrower is party "P-0088" with no contact stop

  Scenario: AC1 Customer signs
    Given "RS-0301" sent "D-0601" for e-signature to party "P-0088" on 2026-12-10
    When EasyApp returns signing result "SIGNED" with the bank signature applied at 2026-12-11 10:15:00
    Then within 60 seconds version 2 of "D-0601" holding the signed PDF is stored on case "RC-2026-000888" with write_once true
    Then the signature request has status "SIGNED" and signed at 2026-12-11 10:15:00
    Then the system calls treatmentApi.recordSignature for "T-0501" with signed true and method "E_SIGNATURE"

  Scenario: AC2 Branch
    Given "RS-0301" created a signature request for "D-0601" with method "BRANCH"
    Given the branch scan "D-0602" of the signed agreement arrived through document intake on 2026-12-12
    When "RS-0301" records result "SIGNED" with signed document "D-0602" and signed date 2026-12-12
    Then the signature request has status "SIGNED" and method "BRANCH"
    Then the system links "D-0602" to the case as the signed agreement
    Then the system calls treatmentApi.recordSignature for "T-0501" with signed true and method "BRANCH"

  Scenario: AC3 DIL paper
    Given case "RC-2026-000889" has deed in lieu treatment "T-0502" for product "MORTGAGE"
    Given its contract document "D-0701" was generated from template "DIL-CONTRACT-MTG" with signature basis "WET_INK_REQUIRED"
    Given "RS-0301" created a signature request for "D-0701" with method "PAPER"
    When "RS-0301" records result "SIGNED" with scan "D-0702" and signed date 2026-12-14
    Then the signature request has status "SIGNED" and method "PAPER"
    Then the system calls treatmentApi.recordSignature for "T-0502" with signed true and method "PAPER"
    Then P3 receives event CUSTOMER_ACCEPTED with signature basis "WET_INK" and moves the case to "WITH_FIELD_INSPECTION" under R-DIL-18

  Scenario: AC4 E-signature refused where Legal requires wet ink
    Given document "D-0701" has signature basis "WET_INK_REQUIRED"
    When "RS-0301" sends POST /treatments/T-0502/signature-requests with method "E_SIGNATURE" for "D-0701"
    Then the response is status 409 with MSG-P6-009 naming "DIL-CONTRACT-MTG"
    Then the system sends no request to EasyApp

  Scenario: AC5 Customer declines
    Given "D-0601" was sent for e-signature on 2026-12-10
    When EasyApp returns signing result "DECLINED" on 2026-12-11
    Then the signature request has status "DECLINED"
    Then the system calls treatmentApi.recordSignature for "T-0501" with signed false

  Scenario: AC6 Offer validity passes with no signature
    Given "D-0601" was sent for e-signature on 2026-12-10 and has status "SENT"
    Given P3 raised OFFER_EXPIRED for "T-0501" on 2026-12-21 and called SignatureApi.cancel
    When EasyApp returns signing result "SIGNED" for that request on 2026-12-21
    Then the signature request keeps status "EXPIRED"
    Then the system holds the result on the exception queue
    Then the system does not call treatmentApi.recordSignature

  Scenario: AC7 Contact stop
    Given case "RC-2026-000888" has an open deviation "X2" with contact stop on
    When "RS-0301" sends "D-0601" for e-signature
    Then the response is status 409 with MSG-P6-001 naming "X2 Vulnerable customer or hardship"
    Then the system sends no request to EasyApp

  Scenario: AC8 EasyApp path unavailable
    Given the ACE path to EasyApp returns "unavailable"
    When "RS-0301" sends "D-0601" for e-signature
    Then the response is status 201 with status "QUEUED" and MSG-GEN-006 naming "EasyApp"
    Then JOB-11 retries the send until it is accepted or the retry limit of 5 is reached

  Scenario: AC9 Signing result repeated
    Given the signing result "SIGNED" for request reference "EA-30001" was applied
    When the same result for "EA-30001" arrives again
    Then the system stores no second document
    Then the system calls treatmentApi.recordSignature once
    Then the system counts the repeat under rule R-UNI-40

  Scenario: AC10 Unknown request reference
    Given no signature request has external reference "EA-99999"
    When EasyApp returns a signing result for reference "EA-99999" that matches no request
    Then the system holds the result on the exception queue with reason "unknown signature request"
    Then the system stores no document

  Scenario: AC11 Branch result without a scan
    Given a signature request for "D-0601" with method "BRANCH"
    When "RS-0301" records result "SIGNED" with no signed document
    Then the response is status 422 with MSG-GEN-001 naming "signed document"
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A customer signs electronically only where the template's signature basis allows it, and by wet ink where Legal requires it | REQ-OCC-009; template signature basis approved by Legal |
| BR2 | A signed offer routes to operations for booking | R-RES-16, R-SET-10 |
| BR3 | A mortgage deed in lieu with a wet ink signature goes to the collateral inspection before the Land Office transfer | R-DIL-18, R-DIL-27 |
| BR4 | A decline returns the case under the route set's decline rule | R-RES-17 |
| BR5 | No signature by the end of the offer validity ends the offer | R-RES-18, R-SET-11 |
| BR6 | A signature request to the customer is an outbound contact and passes the conduct check | CTL-16; R-SET-12 |
| BR7 | The signed document is write-once on the case | CTL-12; DT06 |
| BR8 | The same result twice has one effect | R-UNI-40 |
| BR9 | A system that is unavailable queues the send and retries | R-UNI-33 |

## 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Waiting customer | Customer responds, or the validity timer expires | Signature recorded, decline recorded, or OFFER_EXPIRED | In progress |

P3 makes the case status change on the treatment update this story sends. This story sets the signature request status: Queued, Sent, Signed, Declined, Expired.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| CU-BORROW, customer (borrower) | Signs or declines in EasyApp, or signs at a branch; no Workbench login |
| RW-RESTRUCT, restructuring officer (FCR) | Creates signature requests and records branch and paper results (Treatment and offer CRUA) |
| RW-CASEOWN, case owner | Creates requests and records results on own cases (Treatment and offer CRU) |
| RW-LEGAL, Legal counsel | Sets the signature basis on the template (Documents A, RWB-E1-034); reads requests (Treatment and offer R) |
| SY-CASEWF, case workflow module | Receives the treatment update; calls cancel on offer expiry |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-ACE-056 | v_ace_customer | person_key | Read |
| DF-TRT-001 | treatment | id | Read |
| DF-TRT-004 | treatment | treatment_type | Read |
| DF-TRT-010 | treatment | valid_until | Read |
| DF-TRT-030 | treatment | signature_status | Write, through the treatment interface |
| DF-DOC-105 | signature_request | signed_at | Write, through the treatment interface |
| DF-DOC-001 | document | id | Read |
| DF-DOC-004 | document | document_type | Read |
| DF-DOC-011 | document | doc_version | Write, through the document hub interface |
| DF-DOC-006 | document | storage_ref | Write, through the document hub interface |
| DF-DOC-010 | document | write_once | Write, through the document hub interface |
| DF-REF-068 | template | signature_basis | Read |
| DF-DOC-096 | signature_request | id | Write |
| DF-DOC-097 | signature_request | case_id | Write |
| DF-DOC-098 | signature_request | treatment_id | Write |
| DF-DOC-099 | signature_request | document_id | Write |
| DF-DOC-100 | signature_request | person_key | Write |
| DF-DOC-101 | signature_request | method | Write |
| DF-DOC-102 | signature_request | status | Write |
| DF-DOC-103 | signature_request | external_ref | Write |
| DF-DOC-104 | signature_request | sent_at | Write |
| DF-DOC-105 | signature_request | signed_at | Write |
| DF-DOC-106 | signature_request | signed_document_id | Write |
| DF-DOC-107 | signature_request | expires_at | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

All three endpoints are new and recorded in the additions file. Base path /api/recovery/v1.

| Method and path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|
| POST /treatments/{treatmentId}/signature-requests | SignatureRequestCreate: documentId, partyId, method (E_SIGNATURE, BRANCH, PAPER) | 201 SignatureRequest | 401; 403 (MSG-P4-002); 404 (MSG-P4-003); 409 wet ink required (MSG-P6-009), contact stop (MSG-P6-001), legal hold (MSG-P3-004), treatment not with the customer (MSG-P3-005); 422 (MSG-GEN-001); 503 (MSG-GEN-006) | Treatment and offer C | Idempotency-Key header |
| GET /treatments/{treatmentId}/signature-requests | None | 200 SignatureRequest[] | 401, 403, 404, 503 | Treatment and offer R | Not applicable |
| POST /signature-requests/{requestId}/result | SignatureResultRequest: result (SIGNED, DECLINED), signedDocumentId, signedAt | 200 SignatureRequest | 401; 403; 404; 409 request not open (MSG-P3-005); 422 scan missing (MSG-GEN-001); 503 | Treatment and offer U | Idempotency-Key header |

SignatureRequest schema: id, caseId, treatmentId, documentId, partyId, method, status, externalRef, sentAt, signedAt, signedDocumentId, expiresAt.

**Published interfaces**

```java
// P6, called by the ACE common module when EasyApp returns a result
void SignatureResultListener.onEasyAppResult(String externalRef, String result, byte[] signedPdf, Instant signedAt);
// P6, called by P3 on OFFER_EXPIRED
void SignatureApi.cancel(UUID treatmentId, String reasonCode);
// Owned elsewhere
EsignAck EsignPort.send(EsignRequest request);                                         // ACE common module, INT-34
void TreatmentApi.recordSignature(UUID treatmentId, boolean signed, String method, Instant at); // P3, RWB-E2-004
DocumentRef DocumentHubApi.addVersion(UUID documentId, byte[] pdf, String reason);         // P5, signed copy as a new version
void DocumentHubApi.linkSigned(UUID sourceDocumentId, UUID signedDocumentId);           // P5
```

Target: the signed document is on the case within 60 seconds of the result reaching the Workbench, assumed; DL11. Sends go through JOB-11 Outbox sender with a retry limit of 5 (DL11).

## 13. Solution plan

- Package: folder `recovery/comms/esign`, Java package `recovery.comms.esign`; front end folder `recovery/comms/esign`.

| Component | Type | Responsibility |
|---|---|---|
| SignatureRequestEntity | Entity | Maps table signature_request |
| SignatureRequestRepository | Repository | Reads and writes signature_request; finds by external_ref |
| SignatureController | Controller | The three endpoints |
| SignatureService | Service | Method check against the signature basis, conduct check, outbox write, result recording |
| SignatureResultListener | Published interface | Applies EasyApp results: signed copy as a new document version, treatment update; idempotent on external_ref and result |
| SignatureApiService | Published interface | Implements SignatureApi.cancel |
| SendForSignatureDialog | React component | On SCR-14: method choice limited by the basis, result recording with scan picker |

- Database: new table signature_request with unique index on external_ref and index on (treatment_id, status); check constraint on method and status. Flyway migration `V2_018__signature_request.sql`.
- Configuration and reference data: signature basis per template (Legal counsel, RWB-E1-034); lists for method (E_SIGNATURE, BRANCH, PAPER) and request status (QUEUED, SENT, SIGNED, DECLINED, EXPIRED), recorded as additions; retry limit 5 and the 60-second target (DL11).
- Build steps:
  1. Write the migration and the entity; test the constraints.
  2. Build SignatureService.create with the basis and conduct checks; test AC4 and AC7.
  3. Add the outbox send through EsignPort with retry; test AC8 with the port stubbed.
  4. Build SignatureResultListener with addVersion, recordSignature and idempotency; test AC1, AC5, AC9, AC10.
  5. Build the branch and paper result endpoint; test AC2, AC3 and AC11.
  6. Build SignatureApi.cancel and the expired-result handling; test AC6.
  7. Build SendForSignatureDialog on SCR-14; browser test of the method choice for both bases.
- Feature flag: `rwb.comms.esign`.
- Done when: the tests in section 16 pass, and one end-to-end signature with the EasyApp test tenant passes in SIT.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-009 | E-signature asked for a document that needs wet ink | Legal requires a wet ink signature for {document}. Use the branch or paper path. |
| MSG-P6-001 | A contact stop is in force | Contact with this customer is stopped for {reason}. |
| MSG-P3-004 | A legal hold is on the case | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-GEN-006 | The EasyApp path is unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-GEN-001 | A branch or paper result has no scan | Enter {field}. |
| MSG-P3-005 | The request is not open, or the treatment is not with the customer | This case cannot move to {state} from {current}. |

## 15. Screens and states

SCR-14 Treatment record (states Draft; submitted; approved; booked; broken): in state approved, while the offer is with the customer, the officer sees Send for signature and the request list with status. SCR-30 Case documents shows the signed copy linked to the generated agreement. SCR-09 Exception queue lists held signing results. The customer sees EasyApp only.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-018-01 | AC1, BR2, BR7 | System | T-0501 settlement; D-0601 E_SIGNATURE_ALLOWED; EasyApp stub SIGNED |
| TC-E2-018-02 | AC2, BR1 | System | Branch scan D-0602 |
| TC-E2-018-03 | AC3, BR1, BR3 | System | T-0502 DIL Mortgage; D-0701 WET_INK_REQUIRED; scan D-0702 |
| TC-E2-018-04 | AC4, BR1 | System | E_SIGNATURE on D-0701; method list offered for WET_INK_REQUIRED |
| TC-E2-018-05 | AC5, BR4 | System | EasyApp stub DECLINED |
| TC-E2-018-06 | AC6, BR5 | System | Cancel on 2026-12-21, then SIGNED result |
| TC-E2-018-07 | AC7, BR6 | System | Open X2 with contact stop |
| TC-E2-018-08 | AC8, BR9 | System | EsignPort stub unavailable |
| TC-E2-018-09 | AC9, BR8 | System | Result EA-30001 twice |
| TC-E2-018-10 | AC10 | System | Result EA-99999 |
| TC-E2-018-11 | AC11 | System | Branch SIGNED with no document |
| TC-E2-018-12 | Access | Access | RW-PHONECOL sends POST /treatments/{treatmentId}/signature-requests; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: signature basis, methods, statuses, expiry and the retry limit are data or configuration.
- No personal data in logs, tests or prompts. The signed PDF is stored, never logged; tests use synthetic PDFs.
- No read of another module's tables. Treatment, case, documents and deviations go through their interfaces; treatment fields are written only by P3.
- The bank signing certificate stays in the key store (NFR-052); the Workbench never holds the private key.
- No direct call to EasyApp; only the ACE common module path.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-009 | Electronic signature where Legal permits it, wet ink where Legal requires it | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-08, FEAT-OCC-09 | 7.3 Negotiate settlement or deed in lieu | R-RES-16, R-RES-17, R-RES-18, R-SET-10, R-SET-11, R-SET-12, R-DIL-18, R-DIL-27, R-UNI-33, R-UNI-40 | TC-E2-018-01 to TC-E2-018-12 |

## 19. Out of scope

- Booking the signed treatment in ALS and NLEADS (R-RES-22, Epic 3).
- The deed in lieu field inspection and Land Office transfer screens (Epic 3).
- Signature in customer self-service (FEAT-COM-02, Epic 4).
- Generating the documents to be signed (RWB-E2-017, RWB-E2-026).
