# RWB-P6-E2018-APP E-signature flow for customers and the bank

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E2018-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP05, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P6-A |
| Ready to start | After RWB-P6-E2022-APP |
| Depends on (build) | RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P6-E2022-APP |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P5-E2017-CON |
| Integration dependencies | None |
| External dependencies | RWB-P6-E2018-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (FR-P6-032, FR-P6-033, FR-P6-034) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-018 for rwb-comms in the 19-service realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P6-E2018-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **restructuring officer (RW-RESTRUCT)**, I want **a generated agreement sent for signature by e-signature, branch or paper with the template's signature basis applied, the conduct check run before the customer is contacted, the signed copy returned to the case as a write-once version and the result recorded on the treatment**, so that **a settlement completes without paper where the law allows and the routing rules have a signature fact to act on**.

This story is the rwb-comms orchestration of legacy RWB-E2-018. It provides the three signature-request operations on base `/api/recovery/comms/v1` (API-P6-009, API-P6-010, API-P6-011), applies the signature basis of the agreement's template, reuses the conduct check delivered by `RWB-P6-E2022-APP`, holds the send as an outbox row for the platform relay JOB-11 and the ACE common module path to EasyApp (INT-34), and applies the result: the signed PDF as a new write-once version through the rwb-document contract, the signature record on the treatment through the rwb-treatment contract, the decline, the expiry and the exception queue.

It builds no signature table. `signature_request` is P5 `rwb-document`'s (Architecture v5 slides 16 and 41, signatures; Ownership Map ruling), despite TSD P6 v2 T3.1 defining it, so the request state is created, read by external reference and updated only through the published rwb-document contract `RWB-P5-E2017-CON` (GAP-1181; ASM-2128). It builds no treatment field either: the signature record is the treatment's and is written through the published rwb-treatment contract (GAP-1183; ASM-2130).

### 2. Business rationale

Agreements are printed, signed and couriered today, and the case waits days for the signed copy before booking can start. This story sends the generated agreement for e-signature where Legal permits it, takes branch and paper signatures where Legal requires wet ink, stores the signed copy on the case and records signed or not signed on the treatment, which is the event the routing rules R-RES-16, R-SET-10 and R-DIL-18 act on. It serves REQ-OCC-009.

The realignment changes the ownership, not the business. The monolith held the signature request, the treatment field and the document version in one module and called EasyApp from one listener. In the target, rwb-comms orchestrates three calls and owns none of the three facts: the signature request is rwb-document's, the treatment and its signature status are rwb-treatment's, the signed copy is a document version in rwb-document's write-once Blob store, and the customer is reached only through the ACE common module e-signature path (INT-34, Architecture v5 slide 7). This story therefore publishes no comms event for a signature, because Architecture v5 slide 42 names only `NoticeGenerated`, `NoticeDispatched` and `NoticeDelivered` on `rwb.comms.events.v1`, and a signature is not a notice.

**Where the other criteria of the legacy key are owned.** This story owns AC1 to AC11 of the legacy key. The same journey across the services, with the real owners and the ACE common module test path in place of the fakes, is proved by `RWB-ITG-E2018-ITG` with the `-ITG` copies of the test cases; those copies are not here. The document side of the legacy key is `RWB-P5-E2018-APP` (the signed copy as a version, the signature request itself), the treatment side is `RWB-S2-E2018-APP` (the signature record on the treatment), and the deployment of this capability is `RWB-P6-E2018-OPS`. No `RWB-P6-E2018-CON` exists in the plan, so the contract baseline of this story is its own section 12.1 (GAP-1184; ASM-2131).

### 3. Preconditions

- `RWB-P6-E2022-APP` is delivered: the conduct check (legal hold, contact stop from the deviation state, consent on a verified contact point), the outbox and inbox library in schema `rwb_comms`, the idempotency store and the `template` row resolution exist and are reused, not rebuilt.
- `RWB-P5-E2017-CON` is published for the document contract: a document read, the add of a new version, and the signature-request operations of section 12.2. The operations that create, read by external reference and update a signature request are Not specified in the source documents (GAP-1182; ASM-2129); this story builds against the published P5 document and its fake until they are named.
- `RWB-P3-E1043-CON` is published for the reference data (DP-07), so LOV-SIGN-METHOD (E_SIGNATURE, BRANCH, PAPER), LOV-SIGN-STATUS (QUEUED, SENT, SIGNED, DECLINED, EXPIRED) and LOV-SIGNATURE-BASIS (E_SIGNATURE_ALLOWED, WET_INK_REQUIRED) are data rows and not values in code.
- The published rwb-treatment contract is available for the treatment read (type, offer validity, state) and for the signature record that the legacy calls `TreatmentApi.recordSignature`. The plan's C list of this story names no rwb-treatment contract story, and the exact operation and field names are Not specified in the source documents (GAP-1183; ASM-2130).
- The template row of `rwb_comms` carries `signature_basis` (DF-REF-068), set by Legal counsel on the template, and the agreement was generated from that template by `RWB-P5-E2017-APP`.
- The outbox and inbox library is live in schema `rwb_comms` (DP-09, RWB-PLT-TE006-CON) and the workflow kit is in the build dependency list for the relay dependency (DP-10, RWB-PLT-E1071-CON).
- The per-service Flyway sequence is live for schema `rwb_comms` (DP-15, RWB-PLT-E1044-CON); this story adds indexes only, because it owns no signature table.
- EasyApp is reached only through the ACE common module e-signature path (INT-34). The path's request and result shape, its endpoint, its certificate and its test tenant are Not specified in the source documents (GAP-1187; ASM-2134); the stub of section 12.8 stands behind the path until it is published.
- The bank signing certificate stays in the key store (NFR-052); the Workbench holds no private key and takes no part in adding the bank signature.
- The retry limit of 5 and the exception-queue rule R-UNI-34 are service configuration, not code; the 60-second target for the signed copy is service configuration too.
- The requester holds RW-RESTRUCT or RW-CASEOWN with the Treatment and offer right (C, R or U as the operation names it), and the treatment is in the requester's scope.

### 4. Flow

1. The restructuring officer opens SCR-14 Treatment record through the gateway-bff composite route (DP-19), in the approved state with the offer with the customer, and chooses Send for signature on a generated agreement.
2. gateway-bff declares the Treatment and offer right C and the session, and calls `POST /api/recovery/comms/v1/treatments/{treatmentId}/signature-requests` with an Idempotency-Key; a role without the right is refused there with MSG-P4-002.
3. rwb-comms reads the idempotency store of schema `rwb_comms`; a key already answered returns the stored answer and no second request is made.
4. rwb-comms reads the agreement and the `signature_basis` of the template it was generated from (`template`, P6's own row). A basis of `WET_INK_REQUIRED` refuses a method of `E_SIGNATURE` with 409 and MSG-P6-009 naming the template, and no request leaves for EasyApp.
5. rwb-comms reads the treatment once through the published rwb-treatment contract (one hop, 2 s) for its type, offer validity and state; a treatment that is not with the customer is refused with 409 and MSG-P3-005.
6. rwb-comms runs the conduct check it already owns from `RWB-P6-E2022-APP`: the legal hold from the case facts, the contact stop from the deviation state of the inbox, and consent on a verified contact point. A contact stop refuses with 409 and MSG-P6-001; a legal hold refuses with 409 and MSG-P3-004; nothing is written to the outbox.
7. rwb-comms creates the signature request through the P5 contract with the method, the document, the party and the expiry equal to the treatment's offer validity, and answers 201 with the request.
8. For `E_SIGNATURE` only, rwb-comms writes the send request to `outbox_event` in the same transaction (DP-09). The answer carries status `QUEUED` when the ACE path is unavailable, with MSG-GEN-006.
9. The platform outbox relay (JOB-11, every minute) hands the outbox row to the rwb-comms sender, which calls the ACE common module e-signature path (INT-34) with the request reference, the document reference and the expiry; the accepted reference is stored as the external reference on the request through the P5 contract and the row moves from queued to sent. No Temporal Schedule is registered by this story.
10. The customer signs in EasyApp; EasyApp adds the bank signature with the bank certificate held in the key store and returns the signed PDF and the result through the ACE path.
11. rwb-comms receives the result, reads the request by external reference through the P5 contract, and applies it: `SIGNED` stores the signed PDF as a new write-once version of the agreement through the P5 contract, sets the request `SIGNED` with the signed-at time and the signed document, and calls the rwb-treatment signature record with signed true and the method. The signed copy is on the case within 60 seconds of the result reaching the Workbench.
12. `DECLINED` sets the request `DECLINED` and records not signed on the treatment. A repeated result for the same reference has one effect (R-UNI-40). A result whose reference matches no request is held on the exception queue with reason "unknown signature request" and nothing is stored.
13. The branch and paper path: the branch scan arrives through JOB-12 Document intake as a document on the case, and the officer records the result on `POST /api/recovery/comms/v1/signature-requests/{requestId}/result` with the signed document and the signed date; a result with no signed document is refused with 422 and MSG-GEN-001.
14. On offer expiry P3 raises OFFER_EXPIRED and calls the cancel on this service; the request is set `EXPIRED` through the P5 contract, and a later result for it is held on the exception queue without touching the treatment. The cancel is the legacy `SignatureApi.cancel` and has no named operation in the target catalogue (GAP-1188; ASM-2135).
15. The officer sees the request list and its status on SCR-14, the signed copy linked to the generated agreement on SCR-30 Case documents, and the held results and exception-queue entries on SCR-09, all through gateway-bff composite routes (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | E-signature requested for a document whose template requires wet ink | Refused before any call | MSG-P6-009 | AC4 |
| X2 | The customer declines in EasyApp | Request `DECLINED`; treatment not signed | None | AC5 |
| X3 | The offer validity passes with no signature | Request `EXPIRED`; a later result is held | None | AC6 |
| X4 | A contact stop is in force | Request refused | MSG-P6-001 | AC7 |
| X5 | The ACE path to EasyApp is unavailable | Send queued and retried; the row moves to the exception state at the retry limit of 5 under R-UNI-34 | MSG-GEN-006 | AC8 |
| X6 | The same signing result arrives twice | Ignored and counted under R-UNI-40 | None | AC9 |
| X7 | A signing result names no known request | Held on the exception queue with reason "unknown signature request" | None | AC10 |
| X8 | A branch or paper result recorded with no scan | Refused | MSG-GEN-001 | AC11 |
| X9 | The P5 document contract does not answer inside the 2 s budget on a result | The result is not applied, the request state is unchanged, the result is retried from the same reference and one entry records the degraded read | MSG-GEN-006 | AC1, ASM-2129 |
| X10 | The rwb-treatment signature record fails after the signed version is stored | The version stays stored write-once, the record is retried from the same result, and the inbox of `rwb_comms` absorbs a duplicate so the treatment carries one record | None | AC1, ASM-2130 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against `RWB-P5-E2017-CON`, `RWB-P3-E1043-CON` and the conduct check of `RWB-P6-E2022-APP`; the P5 document contract, the rwb-treatment contract, the rwb-deviation read and the ACE common module path are stubs |
| Negotiable | The signature basis per template, the method and status lists, the expiry source, the retry limit and the 60-second target are data or configuration; the P5 and rwb-treatment operation names are settled with their owners |
| Valuable | A signed copy is on the case within a minute of signing, and the routing rules get the signature fact on the treatment |
| Estimable | Three operations, one outbox row, one result receiver, one cancel handler, one screen action |
| Small | Fits one sprint with its tests, as the rwb-comms slice of a legacy key split five ways |
| Testable | Each criterion runs with the P5 document contract, the rwb-treatment contract, the rwb-deviation read and the ACE path stubbed at their documented answers |

### 7. Acceptance criteria

```gherkin
Feature: E-signature flow for customers and the bank

  Background:
    Given case "RC-2026-000888" has settlement treatment "T-0501" with offer validity 2026-12-20 and state "OFFER_WITH_CUSTOMER_SET"
    Given agreement document "D-0601" on the case was generated from template "SET-AGREE" "TH" with signature basis "E_SIGNATURE_ALLOWED"
    Given the borrower is party "P-0088" with no contact stop

  Scenario: AC1 Customer signs (legacy RWB-E2-018 AC1)
    Given "RS-0301" sent "D-0601" for e-signature to party "P-0088" on 2026-12-10
    Given the rwb-document contract mock returns version 2 of "D-0601" holding the signed PDF with write_once true
    Given the rwb-treatment contract mock returns the signature record for "T-0501" with signed true and method "E_SIGNATURE"
    When EasyApp returns signing result "SIGNED" with the bank signature applied at 2026-12-11 10:15:00
    Then within 60 seconds version 2 of "D-0601" holding the signed PDF is stored on case "RC-2026-000888" with write_once true
    Then the signature request has status "SIGNED" and signed at 2026-12-11 10:15:00
    Then the system calls treatmentApi.recordSignature for "T-0501" with signed true and method "E_SIGNATURE"

  Scenario: AC2 Branch (legacy RWB-E2-018 AC2)
    Given "RS-0301" created a signature request for "D-0601" with method "BRANCH"
    Given the branch scan "D-0602" of the signed agreement arrived through document intake on 2026-12-12
    Given the rwb-document contract mock returns "D-0602" linked to the case as the signed agreement
    Given the rwb-treatment contract mock returns the signature record for "T-0501" with signed true and method "BRANCH"
    When "RS-0301" records result "SIGNED" with signed document "D-0602" and signed date 2026-12-12
    Then the signature request has status "SIGNED" and method "BRANCH"
    Then the system links "D-0602" to the case as the signed agreement
    Then the system calls treatmentApi.recordSignature for "T-0501" with signed true and method "BRANCH"

  Scenario: AC3 DIL paper (legacy RWB-E2-018 AC3)
    Given case "RC-2026-000889" has deed in lieu treatment "T-0502" for product "MORTGAGE"
    Given its contract document "D-0701" was generated from template "DIL-CONTRACT-MTG" with signature basis "WET_INK_REQUIRED"
    Given "RS-0301" created a signature request for "D-0701" with method "PAPER"
    Given the rwb-treatment contract mock returns the signature record for "T-0502" with signed true and method "PAPER"
    When "RS-0301" records result "SIGNED" with scan "D-0702" and signed date 2026-12-14
    Then the signature request has status "SIGNED" and method "PAPER"
    Then the system calls treatmentApi.recordSignature for "T-0502" with signed true and method "PAPER"
    Then P3 receives event CUSTOMER_ACCEPTED with signature basis "WET_INK" and moves the case to "WITH_FIELD_INSPECTION" under R-DIL-18

  Scenario: AC4 E-signature refused where Legal requires wet ink (legacy RWB-E2-018 AC4)
    Given document "D-0701" has signature basis "WET_INK_REQUIRED"
    When "RS-0301" sends POST /treatments/T-0502/signature-requests with method "E_SIGNATURE" for "D-0701"
    Then the response is status 409 with MSG-P6-009 naming "DIL-CONTRACT-MTG"
    Then the system sends no request to EasyApp

  Scenario: AC5 Customer declines (legacy RWB-E2-018 AC5)
    Given "D-0601" was sent for e-signature on 2026-12-10
    Given the rwb-treatment contract mock returns the signature record for "T-0501" with signed false
    When EasyApp returns signing result "DECLINED" on 2026-12-11
    Then the signature request has status "DECLINED"
    Then the system calls treatmentApi.recordSignature for "T-0501" with signed false

  Scenario: AC6 Offer validity passes with no signature (legacy RWB-E2-018 AC6)
    Given "D-0601" was sent for e-signature on 2026-12-10 and has status "SENT"
    Given P3 raised OFFER_EXPIRED for "T-0501" on 2026-12-21 and called SignatureApi.cancel
    When EasyApp returns signing result "SIGNED" for that request on 2026-12-21
    Then the signature request keeps status "EXPIRED"
    Then the system holds the result on the exception queue
    Then the system does not call treatmentApi.recordSignature

  Scenario: AC7 Contact stop (legacy RWB-E2-018 AC7)
    Given case "RC-2026-000888" has an open deviation "X2" with contact stop on
    Given the rwb-deviation contract mock returns the open deviation "X2" with contact stop on for case "RC-2026-000888"
    When "RS-0301" sends "D-0601" for e-signature
    Then the response is status 409 with MSG-P6-001 naming "X2 Vulnerable customer or hardship"
    Then the system sends no request to EasyApp

  Scenario: AC8 EasyApp path unavailable (legacy RWB-E2-018 AC8)
    Given the ACE path to EasyApp returns "unavailable"
    When "RS-0301" sends "D-0601" for e-signature
    Then the response is status 201 with status "QUEUED" and MSG-GEN-006 naming "EasyApp"
    Then JOB-11 retries the send until it is accepted or the retry limit of 5 is reached

  Scenario: AC9 Signing result repeated (legacy RWB-E2-018 AC9)
    Given the signing result "SIGNED" for request reference "EA-30001" was applied
    Given the rwb-document contract mock returns one stored version of "D-0601" for reference "EA-30001"
    Given the rwb-treatment contract mock returns one recorded signature call for "T-0501" for reference "EA-30001"
    When the same result for "EA-30001" arrives again
    Then the system stores no second document
    Then the system calls treatmentApi.recordSignature once
    Then the system counts the repeat under rule R-UNI-40

  Scenario: AC10 Unknown request reference (legacy RWB-E2-018 AC10)
    Given no signature request has external reference "EA-99999"
    Given the rwb-document contract mock returns no signature request for external reference "EA-99999"
    When EasyApp returns a signing result for reference "EA-99999" that matches no request
    Then the system holds the result on the exception queue with reason "unknown signature request"
    Then the system stores no document

  Scenario: AC11 Branch result without a scan (legacy RWB-E2-018 AC11)
    Given a signature request for "D-0601" with method "BRANCH"
    When "RS-0301" records result "SIGNED" with no signed document
    Then the response is status 422 with MSG-GEN-001 naming "signed document"
```

The eleven criteria above are copied from legacy section 7 with every line, ID and value kept, each tagged with its origin. The cross-service lines added inside a scenario are the mock of the owner's published contract with the same values the legacy line already fixed; no business value is added, and no legacy line is dropped or reworded. The monolith path `POST /treatments/T-0502/signature-requests` inside AC4 is kept exactly as the legacy AC writes it; on the target base it is `POST /api/recovery/comms/v1/treatments/{treatmentId}/signature-requests`.

### 8. Business rules

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
| BR9 | A system that is unavailable queues the send and retries, and after the retry limit of 5 the send moves to the exception queue | R-UNI-33, R-UNI-34 |
| BR10 | `signature_request` is P5 rwb-document's. rwb-comms holds no signature table and creates, reads and updates the request only through the published rwb-document contract; the request state is never a row in `rwb_comms` | DP-01; Architecture v5 slides 16 and 41; Ownership Map ruling |
| BR11 | The treatment and its signature status are rwb-treatment's. rwb-comms writes the signature record only through the published rwb-treatment contract, with the legacy values signed true or false and method E_SIGNATURE, BRANCH or PAPER | DP-01; Architecture v5 slides 18 and 41 |
| BR12 | The signature basis, the method list and the status list are data rows read through the reference-data contract of rwb-case, never values in code | DP-07; RWB-P3-E1043-CON; FSD P6 BR-P6-008 |
| BR13 | No comms event is published for a signature. The only element this story relays is the decision record written by the local library in the same transaction, on the shared topic `rwb.decision-record.v1` | DP-09; Architecture v5 slide 42 |
| BR14 | No direct call to EasyApp: the send and the result go only through the ACE common module e-signature path (INT-34), and the Workbench never holds the bank private key | REQ-OCC-009; NFR-052; legacy section 17 |
| BR15 | One REST base per service, `/api/recovery/comms/v1`, one hop, a 2 s timeout and an Idempotency-Key on every POST; no personal data and no signed PDF content in an event, a workflow input or a log | DP-11, DP-13; ADR-020; legacy section 17 |

### 9. State transitions

None in the case. This story changes no case status: the case state machine is rwb-case's and the treatment state is rwb-treatment's. It sets the signature request status through the P5 contract - `QUEUED`, `SENT`, `SIGNED`, `DECLINED`, `EXPIRED` - and records signed or not signed on the treatment through the rwb-treatment contract.

| From | Event | Condition | To |
|---|---|---|---|
| Waiting customer | Customer responds, or the validity timer expires | Signature recorded, decline recorded, or OFFER_EXPIRED | In progress |
| no request | a send is requested | the basis allows the method and the conduct check passes | QUEUED - the request exists and, for E_SIGNATURE, the outbox row is written in the same transaction |
| no request | a send is requested | the basis refuses the method, a contact stop or a legal hold applies, or the treatment is not with the customer | REFUSED - 409, no request and no outbox row |
| QUEUED | the platform relay hands the row to the sender | the ACE path accepts the request | SENT - the accepted reference is stored as the external reference |
| SENT | a result arrives for the reference | `SIGNED` | SIGNED - the signed copy is a new write-once version and the treatment records signed true |
| SENT | a result arrives for the reference | `DECLINED` | DECLINED - the treatment records signed false |
| QUEUED or SENT | P3 cancels on offer expiry | OFFER_EXPIRED | EXPIRED - a later result is held on the exception queue |
| QUEUED | the retry window finds the path unavailable | the attempt count is below 5 | QUEUED - the next window retries |
| QUEUED | the retry window finds the attempt count at 5 | R-UNI-34 | EXCEPTION - the row is in the exception state, SCR-09 lists it, and the request stays not signed |

### 10. Authority

The rights below are the Treatment and offer rights the three operations declare (TSD P6 T-A.1: API-P6-009 C, API-P6-010 R, API-P6-011 U, scope applied). The role rows are the TSD P6 T6.1 rows for each role; T6.1 declares the Documents and Litigation areas, and the Treatment and offer area of these operations is the one the endpoint inventory names, so the right is declared by the operation and the role row is taken from T6.1.

| Who | What they may do in this story | TSD P6 T6.1 rows |
|---|---|---|
| CU-BORROW, customer (borrower) | Signs or declines in EasyApp, or signs at a branch; no Workbench login | no Workbench row |
| RW-RESTRUCT, restructuring officer (FCR) | Creates signature requests and records branch and paper results (Treatment and offer CRU) | Documents CRU |
| RW-CASEOWN, case owner | Creates requests and records results on own cases (Treatment and offer CRU) | Documents CRU; Litigation R |
| RW-LEGAL, Legal counsel | Sets the signature basis on the template, outside this story; reads requests (Treatment and offer R) | Documents CRUA; Litigation RA |
| RW-PHONECOL, phone collector | Refused on the create with MSG-P4-002 (TC-E2-018-12) | Documents R |
| SY-CASEWF, case workflow module | Raises OFFER_EXPIRED and calls the cancel on offer expiry | T6.2 service identities |

No role in this story may grant itself a right, and the basis is set by Legal counsel on the template, never by the officer who sends the agreement.

### 11. Data

| BR Field ID | Entity | Field | Owner | Read or write |
|---|---|---|---|---|
| DF-REF-068 | template | signature_basis | P6 (rwb_comms) | Read |
| DF-DOC-096, DF-DOC-097, DF-DOC-098, DF-DOC-099, DF-DOC-100, DF-DOC-101, DF-DOC-102, DF-DOC-103, DF-DOC-104, DF-DOC-105, DF-DOC-106, DF-DOC-107 | signature_request | id, case_id, treatment_id, document_id, party_id, method, status, external_ref, sent_at, signed_at, signed_document_id, expires_at | P5 (rwb_document) | Created, read by external reference and updated through the P5 contract; never a row in `rwb_comms` |
| DF-DOC-001, DF-DOC-004 | document | id, document_type | P5 (rwb_document) | Read through the P5 contract |
| DF-DOC-006, DF-DOC-010, DF-DOC-011 | document | storage_ref, write_once, doc_version | P5 (rwb_document) | Written and read through the P5 contract only |
| DF-TRT-001, DF-TRT-004, DF-TRT-010 | treatment | id, treatment_type, valid_until | S2 (rwb_treatment) | Read through the rwb-treatment contract |
| DF-TRT-030 | treatment | signature_status | S2 (rwb_treatment) | Written through the rwb-treatment contract |
| DF-CAS-001, DF-CAS-003 | recovery_case | id, product_group | P3 (rwb_case) | Read through the case-facts reader of the conduct check |
| DF-ACE-056 | v_ace_customer | person_key | P1 (rwb_source_data) | Not read here (DP-05); the party key arrives on the request and through the owners' contracts |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | the record of the request and of the result | P7 (rwb_decision) | Written through the local decision-record library (DP-03) |

`rwb_comms` holds no signature table and no copy of a treatment, a document or a case. The one business table this story reads in its own schema is `template`; the outbox, inbox and idempotency objects are the library's. Field IDs are those of the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`. The three operations are the legacy endpoints of RWB-E2-018 section 12 and the endpoint inventory T-A.1 (API-P6-009, API-P6-010, API-P6-011); the plan holds no `RWB-P6-E2018-CON` story, so this section is the contract baseline of the story and the fakes of section 12.8 stand in for the consumed contracts (GAP-1184; ASM-2131).

| Method | Path | API ID | Request | Answer | Access | Idempotency |
|---|---|---|---|---|---|---|
| POST | `/treatments/{treatmentId}/signature-requests` | API-P6-009 | `SignatureRequestCreate`: documentId, partyId, method (E_SIGNATURE, BRANCH, PAPER) | 201 `SignatureRequest` | Treatment and offer C, scope applied | Idempotency-Key header, response stored |
| GET | `/treatments/{treatmentId}/signature-requests` | API-P6-010 | None | 200 `SignatureRequest[]` | Treatment and offer R, scope applied | Not applicable |
| POST | `/signature-requests/{requestId}/result` | API-P6-011 | `SignatureResultRequest`: result (SIGNED, DECLINED), signedDocumentId, signedAt | 200 `SignatureRequest` | Treatment and offer U, scope applied | Idempotency-Key header, response stored |

`SignatureRequest` schema: id, caseId, treatmentId, documentId, partyId, method, status, externalRef, sentAt, signedAt, signedDocumentId, expiresAt.

Errors: 401 no session; 403 the role lacks the right (MSG-P4-002); 404 the object is outside the scope (MSG-P4-003); 409 wet ink required (MSG-P6-009), contact stop (MSG-P6-001), legal hold (MSG-P3-004), treatment not with the customer (MSG-P3-005); 422 a field is missing (MSG-GEN-001); 503 the ACE path or a consumed contract could not be reached (MSG-GEN-006).

#### 12.2 REST operations consumed

| Call | Owner | Use in this story |
|---|---|---|
| Create a signature request - the P5 rwb-document operation of `RWB-P5-E2017-CON`. The operation name and the field names are Not specified in the source documents (GAP-1182; ASM-2129) | P5 rwb-document | Writes the request with document, party, method and expiry; faked |
| Read a signature request by external reference - the P5 operation of `RWB-P5-E2017-CON`. The operation name is Not specified in the source documents (GAP-1182; ASM-2129) | P5 rwb-document | Resolves the result reference `EA-30001` or `EA-99999` to a request, or to none; faked |
| Update a signature request (status, sent_at, signed_at, signed_document_id) - the P5 operation of `RWB-P5-E2017-CON`. The operation name and the field names are Not specified in the source documents (GAP-1182; ASM-2129) | P5 rwb-document | Sets `QUEUED`, `SENT`, `SIGNED`, `DECLINED` and `EXPIRED` on the request and links the signed document; faked |
| `POST /api/recovery/document/v1/documents/{documentId}/versions` | P5 rwb-document | Adds the signed PDF as the next write-once version of the agreement; the byte transfer and the object store behind it are Not specified in the source documents (GAP-1186; ASM-2133); faked |
| `PATCH /api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | The treatment contract that carries the signature record the legacy calls `TreatmentApi.recordSignature`; the exact operation and field names are Not specified in the source documents (GAP-1183; ASM-2130); faked |
| `GET /api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | The treatment type, offer validity and state for the expiry and the MSG-P3-005 refusal; the exact element names are Not specified in the source documents (GAP-1183; ASM-2130); faked |
| `GET` reference data for LOV-SIGN-METHOD, LOV-SIGN-STATUS and LOV-SIGNATURE-BASIS - the P3 reference-data contract of `RWB-P3-E1043-CON` | P3 rwb-case | The method, status and basis values as data rows, never values in code (DP-07); faked |
| `GET /api/recovery/deviation/v1/cases/{caseId}/deviations` | S8 rwb-deviation | The open deviation with its contact stop and its code for the refusal text; faked only, because the runtime path is the deviation state of the inbox and the case facts reader (as in `RWB-P6-E2022-APP`) |

Every row is one hop with a 2 s timeout and a breaker, and a GET is retried once with jitter (DP-11, ADR-020). The case-facts read of the legal hold and the deviation state are the ones delivered by the conduct check of `RWB-P6-E2022-APP` and are not rebuilt here. This story reads no `rwb_document`, `rwb_treatment`, `rwb_case`, `rwb_deviation` or `rwb_decision` table (DP-01), and no `v_ace_*` view (DP-05).

#### 12.3 Events published

| Event | Topic | Owner of the type | Payload (IDs and facts only) |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (event 08) | `rwb.decision-record.v1` | P7 rwb-decision | decision record reference, the decision code, the final call, the rule and its version where one applied, the case ID, the treatment ID and the decided-at time; written by the local library in the same transaction and relayed by the outbox |

New `rwb.comms.*` events for this capability: None. Architecture v5 slide 42 names only `NoticeGenerated`, `NoticeDispatched` and `NoticeDelivered` on `rwb.comms.events.v1`, and a signature is not a notice, so this story publishes no new comms event, adds none to the AsyncAPI document of the topic and does not invent a `SignatureRecorded` event (GAP-1185; ASM-2132). The request state is read by its owners and the screens from the P5 contract, not from a comms event.

#### 12.4 Events consumed

| Event | Topic | Owner | Element used |
|---|---|---|---|
| `rwb.treatment.TreatmentApproved.v1` (event 10) | `rwb.treatment.events.v1` | S2 rwb-treatment | case ID, treatment ID, treatment type, approved-at; confirms the treatment the request belongs to is approved |
| `rwb.case.CaseStateChanged.v1` (event 05) | `rwb.case.events.v1` | P3 rwb-case | case ID, previous and new state, the changed-at time; keeps the case projection the refusal paths read |
| `rwb.deviation.DeviationRaised.v1` (event 06) | `rwb.deviation.events.v1` | S8 rwb-deviation | case ID, deviation code, raised at, the contact stop flag; refuses the send while a stop is on |
| `rwb.deviation.DeviationCleared.v1` (event 07) | `rwb.deviation.events.v1` | S8 rwb-deviation | case ID, deviation code, cleared at, outcome; releases the stop |

The four are consumed into the inbox of schema `rwb_comms` (`processed_event`), deduplicated by event ID, and each has its retry topic and its `.dlt` topic (DP-09). Their arrival is what lets the conduct check and the treatment confirmation answer while the case read is degraded.

#### 12.5 Workflows and activities

None. The three operations are synchronous REST requests, the durability of a send is the outbox row, and the retry is the platform relay's window. This story registers no workflow, no activity and no child workflow on task queue `rwb-comms`, and the request lifecycle is a transaction, not a workflow step.

#### 12.6 Schedules

None. JOB-11 Outbox sender is the platform's outbox relay, every minute, one owner for every service (Architecture v5 slide 44), and this story registers no Temporal Schedule, no cron entry and no job name. DP-10 is claimed for the relay dependency and the workflow kit only; the send attempt is the rwb-comms sender's code, called by the relay window. The legacy retry limit of 5 and the exception-queue rule R-UNI-34 are applied inside that call.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| template | P6 (rwb_comms) | The `signature_basis` of the agreement's template (DF-REF-068) and the template code and version |
| merge_field | P6 (rwb_comms) | Read only where the send carries the template reference; no merge value is written by this story |
| notice | P6 (rwb_comms) | Not written by this story: a signature request is not a notice |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_comms | The send request, the inbox of the four consumed events and the stored answer of the two POSTs |

Not owned and never written: `signature_request`, `document` and `document_field` are P5's, `treatment` is S2's, `recovery_case` is P3's, `deviation` is S8's and `decision_log_entry` is P7's. rwb-comms holds no foreign key across services and no copy of a signature request, a treatment or a document (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-document WireMock (RWB-P5-E2017-CON) | A created request `RS-0301`; the read by external reference returning `RS-0301` for `EA-30001` and none for `EA-99999`; the update answering accepted; the version add answering version 2 of `D-0601` with write_once true; the link of `D-0602` as the signed agreement; a delayed answer beyond 2 s | AC1, AC2, AC9, AC10 and the refusal-closed path of X9 |
| rwb-treatment WireMock | The treatment `T-0501` with offer validity 2026-12-20 and state OFFER_WITH_CUSTOMER_SET, `T-0502` for the deed in lieu, and the signature record answering accepted for signed true with E_SIGNATURE or BRANCH, signed true with PAPER, and signed false | AC1, AC2, AC3, AC5 and the retry path of X10 |
| rwb-deviation WireMock | The open deviation `X2` with contact stop on for `RC-2026-000888`; an empty answer; a delayed answer beyond 2 s | AC7 |
| rwb-case WireMock | The case facts reader of the conduct check reused from `RWB-P6-E2022-APP`: legal hold false and true | X4, the MSG-P3-004 refusal |
| P3 reference-data WireMock | LOV-SIGN-METHOD, LOV-SIGN-STATUS and LOV-SIGNATURE-BASIS as data rows | AC4 and the method list |
| decision-record library stub | A healthy chain and outbox, and a stopped chain for the 503 path | the refusal path |
| ACE common module e-signature path stub (INT-34) | An accepted reference, then a `SIGNED` result with the signed PDF and the signed-at time, a `DECLINED` result, and an `unavailable` answer for six attempts | AC1, AC5, AC8 and the exception state of section 9 |

The exact shape of the ACE common module e-signature path, its endpoint and its certificate are Not specified in the source documents (GAP-1187; ASM-2134), and the signed PDF object store behind the P5 version add is Not specified either (GAP-1186; ASM-2133). The stubs are derived from the legacy interface names (`EsignPort`, `SignatureResultListener`), the published P5 document and the published rwb-treatment base, and each is replaced by its real owner as the wave 2 stories land.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 8 consumed | The three signature-request operations provided; the three P5 signature-request operations, the P5 version add, the rwb-treatment read and record, the reference data and the deviation read consumed; one hop, 2 s |
| Kafka | 1 published, 4 consumed | `DecisionRecorded` published on the shared topic; `TreatmentApproved`, `CaseStateChanged`, `DeviationRaised` and `DeviationCleared` consumed with retry and `.dlt` |
| Temporal | None | No workflow, no activity and no Schedule in this story; JOB-11 is the platform relay |
| File | None | The signed PDF travels inside the P5 version-add call, never as a file of this service |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.comms`, module `esign`, Java package `th.co.scb.ace.workbench.recovery.comms.esign`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_comms`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/comms/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies as a prohibition as well as a permission: this story reads no ACE view and no ACE table, because the customer and party facts arrive through the owners' contracts and on the request. DP-10 is claimed for the relay dependency only; no Schedule is registered here. DP-05 and DP-13 add no dependency row. DP-03 is not in the pattern set of this key, although TSD P6 T2 requires the decision log entry before every change and this story writes one through the local decision-record library on `rwb.decision-record.v1`; the missing DP-03 row and its H `RWB-PLT-E1027-CON` are carried by GAP-1196 and ASM-2143.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| SignatureController | Controller | The three operations, validation and the problem mapping for 401, 403, 404, 409, 422 and 503 |
| SignatureRequestService | Service | The basis check, the conduct check reuse, the P5 create and update, the outbox write and the expiry source |
| SignatureBasisReader | Service | Reads `template.signature_basis` and the LOV lists as data, and refuses E_SIGNATURE on a wet ink basis |
| SignatureResultReceiver | Service | Applies an EasyApp result: read by external reference, version add, treatment record, idempotency on reference and result |
| SignatureCancelHandler | Service | The legacy `SignatureApi.cancel` on OFFER_EXPIRED: sets `EXPIRED` and holds a later result |
| SignatureSender | Service | The send attempt the relay window calls: the ACE common module e-signature path, the accepted reference and the attempt counter |
| SignatureRequestGateway | Service | The P5 contract calls of section 12.2, with the breaker and the 2 s budget |
| TreatmentSignatureRecorder | Service | The rwb-treatment read and the signature record, with the retry of X10 |
| IdempotencyStore | Repository | The stored answer of the two POSTs under their keys, in `idempotency_key` |
| SendForSignatureDialog | React component | On SCR-14: the method choice limited by the basis and the result recording with the scan picker |

**Database and migrations**

- Reads `template`; writes `outbox_event`, `processed_event` and `idempotency_key` in schema `rwb_comms`.
- Migration in this story: `V2018_1__esign_indexes.sql` adds the index on `idempotency_key (key, created_at)` used by the stored-answer read and the index on `outbox_event (state, next_attempt_at)` used by the relay window. No table is created for a signature request, because `signature_request` is P5's and rwb-comms holds no signature table (DP-15, DP-01).
- No row of `signature_request`, `document`, `treatment`, `recovery_case`, `deviation` or `decision_log_entry` is written by this migration, and none is written by its code except through the owners' contracts.

**Configuration and reference data**

- The signature basis per template (DF-REF-068), set by Legal counsel on the template, never a value in code.
- LOV-SIGN-METHOD, LOV-SIGN-STATUS and LOV-SIGNATURE-BASIS as data rows read through the reference-data contract (DP-07).
- The retry limit of 5, the exception-queue rule R-UNI-34 and the 60-second signed-copy target - service configuration read as data.
- The feature switch `rwb.comms.esign`, default off in DEV and on in SIT: off refuses the send closed with MSG-GEN-006 and sends nothing.
- The login is the rwb-comms login (DP-02).

**Build steps**

1. SignatureController and SignatureRequestService over this section's contract, with the idempotency store first; test AC11 and the refused-method path.
2. SignatureBasisReader with `template.signature_basis` and the three lists as data; test AC4 and the method list offered for `WET_INK_REQUIRED`.
3. The P5 contract gateway for create, read-by-external-reference and update against the rwb-document fake; test AC1, AC2 and AC10.
4. The outbox send through the ACE path with the attempt counter and the exception state at attempt 5; test AC8.
5. SignatureResultReceiver with the version add, the treatment record and the idempotency on reference and result; test AC1, AC2, AC3, AC5 and AC9.
6. The branch and paper result path with the scan requirement; test AC2, AC3 and AC11.
7. SignatureCancelHandler with the held result on expiry; test AC6.
8. The conduct check reuse from `RWB-P6-E2022-APP` with the deviation fake; test AC7 and the legal-hold path.
9. SendForSignatureDialog on SCR-14 and the request list read; the gateway-bff route behind SCR-14 and SCR-30; browser test of the method choice for both bases.
10. Contract-fake run of every cross-service answer in isolation, so the story builds before rwb-document, rwb-treatment and the ACE path are live in SIT.

**Feature switch.** `rwb.comms.esign`, read as service configuration; off refuses closed and allows nothing.

**Done when.** The twelve test cases of section 16 pass, one end-to-end signature with the ACE common module test path passes in SIT, the signed copy is a write-once version within 60 seconds, the treatment carries one signature record per result, and no signed PDF content, party identity or document body appears in a log, an event or a workflow input.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-009 | E-signature asked for a document that needs wet ink | Legal requires a wet ink signature for {document}. Use the branch or paper path. |
| MSG-P6-001 | A contact stop is in force | Contact with this customer is stopped for {reason}. |
| MSG-P3-004 | A legal hold is on the case | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-GEN-006 | The EasyApp path is unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-GEN-001 | A branch or paper result has no scan | Enter {field}. |
| MSG-P3-005 | The request is not open, or the treatment is not with the customer | This case cannot move to {state} from {current}. |

The texts are copied unchanged from the legacy story. The {reason} of MSG-P6-001 is the deviation code and its name as the reference data holds them, {document} of MSG-P6-009 is the template code the legacy AC names (`DIL-CONTRACT-MTG`), and {system} of MSG-GEN-006 is the name of the system that failed - `EasyApp` or the name of the consumed service.

### 15. Screens and states

SCR-14 Treatment record (states Draft; submitted; approved; booked; broken): in state approved, while the offer is with the customer, the officer sees Send for signature and the request list with its status. SCR-30 Case documents shows the signed copy linked to the generated agreement. SCR-09 Exception queue lists the held signing results and the sends in the exception state. The customer sees EasyApp only.

All three are gateway-bff composite routes (DP-19); this story provides the three operations and the answers behind them and builds no screen of its own. No screen shows the signed PDF content: it shows the version, the write-once flag, the method and the status.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-018-01 | AC1, BR2, BR7 | End to end | T-0501 settlement; D-0601 E_SIGNATURE_ALLOWED; EasyApp stub SIGNED |
| TC-E2-018-02 | AC2, BR1 | End to end | Branch scan D-0602 |
| TC-E2-018-03 | AC3, BR1, BR3 | End to end | T-0502 DIL Mortgage; D-0701 WET_INK_REQUIRED; scan D-0702 |
| TC-E2-018-04 | AC4, BR1 | End to end | E_SIGNATURE on D-0701; method list offered for WET_INK_REQUIRED |
| TC-E2-018-05 | AC5, BR4 | End to end | EasyApp stub DECLINED |
| TC-E2-018-06 | AC6, BR5 | End to end | Cancel on 2026-12-21, then SIGNED result |
| TC-E2-018-07 | AC7, BR6 | End to end | Open X2 with contact stop |
| TC-E2-018-08 | AC8, BR9 | End to end | EsignPort stub unavailable |
| TC-E2-018-09 | AC9, BR8 | End to end | Result EA-30001 twice |
| TC-E2-018-10 | AC10 | End to end | Result EA-99999 |
| TC-E2-018-11 | AC11 | End to end | Branch SIGNED with no document |
| TC-E2-018-12 | Access | Component | RW-PHONECOL sends POST /treatments/{treatmentId}/signature-requests; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end and Access to Component. All twelve cases are kept here in their legacy order, because this story owns AC1 to AC11; the `-ITG` copies of the same twelve belong to `RWB-ITG-E2018-ITG` and are not here.

### 17. Guardrails

- No business value in code: the signature basis, the methods, the statuses, the expiry source, the retry limit of 5 and the 60-second target are data or service configuration read with their version.
- No personal data in events, workflow inputs, logs, tests or prompts. The signed PDF is stored through the P5 contract, never logged and never carried in an event; tests use synthetic PDFs.
- No read of another service's tables: the signature request, the document and the treatment go through their contracts; rwb-comms writes only its own schema (DP-01).
- No ACE view and no ACE table is read: the customer and party facts arrive through the owners' contracts and on the request (DP-05).
- The bank signing certificate stays in the key store (NFR-052); the Workbench never holds the private key and never adds the bank signature itself.
- No direct call to EasyApp: the send and the result go only through the ACE common module e-signature path (INT-34).
- One REST base, one hop and a 2 s timeout: the three operations are on `/api/recovery/comms/v1`, the consumed calls carry the budget and a breaker, and no consumer is called twice for one result (DP-11, DP-13, ADR-020).
- No comms event is invented for a signature: the only element relayed is the decision record on the shared topic (DP-09).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-009 | Electronic signature where Legal permits it, wet ink where Legal requires it | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-08, FEAT-OCC-09 | 7.3 Negotiate settlement or deed in lieu | R-RES-16, R-RES-17, R-RES-18, R-SET-10, R-SET-11, R-SET-12, R-DIL-18, R-DIL-27, R-UNI-33, R-UNI-40 | TC-E2-018-01 to TC-E2-018-12 |
| RWB-E2-018 | The legacy key this story is split from, with AC1 to AC11 owned here | Legacy section 7 | FEAT-OCC-08, FEAT-OCC-09 | 7.3 Negotiate settlement or deed in lieu | BR1 to BR15 of section 8 | All twelve cases of section 16 |
| DP set | DP01, DP05, DP07, DP09, DP10, DP11, DP13, DP15, DP19 | Template and Rules §R5.5 | - | - | - | TC-E2-018-01, TC-E2-018-04, TC-E2-018-08 |
| ADR-013 | 19 services inside ACE, each with its own schema and login | Architecture v5 slides 20 and 41 | - | - | - | TC-E2-018-01 |
| ADR-014 | One schema and one login per service in ACE PostgreSQL | Architecture v5 slide 41 | - | - | - | TC-E2-018-01 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | Architecture v5 slides 22 and 42 | - | - | - | TC-E2-018-08 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | Template and Rules §R5.5, DP-11 | - | - | - | TC-E2-018-01, TC-E2-018-12 |

The document side of the same key is `RWB-P5-E2018-APP` (the signature request and the signed copy as a version), the treatment side is `RWB-S2-E2018-APP`, and the cross-service journey is `RWB-ITG-E2018-ITG`.

### 19. Out of scope

- Booking the signed treatment in ALS and NLEADS (R-RES-22, Epic 3).
- The deed in lieu field inspection and Land Office transfer screens (Epic 3).
- Signature in customer self-service (FEAT-COM-02, Epic 4).
- Generating the documents to be signed (RWB-E2-017, RWB-E2-026).
- The signature request table and the signed copy as a document version, with the write-once object store: rwb-document (`RWB-P5-E2018-APP`, `RWB-P5-E2017-CON`).
- The signature record on the treatment and its state machine: rwb-treatment (`RWB-S2-E2018-APP`).
- The ACE common module e-signature path, its certificate and its own retries: the path owner's (INT-34).
- The deployment of the egress, the retry window, the dashboards, the alerts and the runbook: `RWB-P6-E2018-OPS`.
- The cross-service journey and its evidence: `RWB-ITG-E2018-ITG`.
- The conduct check itself, which is delivered by `RWB-P6-E2022-APP` and reused here.
