# RWB-P5-E2018-APP E-signature flow for customers and the bank

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E2018-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Size | Small; fits two weeks; set by the squad at refinement (DOR-RWB-P5-E2018-APP-16) |
| Legacy key | RWB-E2-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP05, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P5-W |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | Not specified in the source documents (DOR-RWB-P5-E2018-APP-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (no FR mapped to REQ-OCC-009) |
| Open decisions | DL26 is open; assumptions ASM-0247, ASM-0264, ASM-0275, ASM-0355; read path for the signature request status to be confirmed with P5 before wave 2 (GAP-1596) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-018 for rwb-document in the 19-service realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P5-E2018-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (27 resolved, 25 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **restructuring officer (RW-RESTRUCT)**, I want **the signature request and the signed copy of a generated agreement held by the document hub - the request with its document, party, method and expiry, the signed PDF as a new write-once version of the agreement, and the branch or paper scan linked to it as the signed document**, so that **the paper that proves a settlement is on the case once, cannot be altered inside its retention period, and is readable by the services that route from it**.

This story is the rwb-document slice of legacy RWB-E2-018, a secondary slice of a legacy key split across the services. `signature_request` is P5's (Ownership rows of the P5 context pack, Arch v5 slides 16 and 41); TSD P6 T3.1 defines the same table inside the communications module, and the ownership ruling wins, so the request is created, read and updated here and nowhere else (GAP-2353; ASM-3908). The signed copy is a version of the agreement in this service's own write-once Blob store, written through API-P5-005 (`POST /documents/{documentId}/versions`), and the branch scan is already a document of this service, because intake is JOB-12 Document intake.

The circuit of the legacy key is rwb-comms' (`RWB-P6-E2018-APP`): the signature basis of the template, the conduct check, the send to EasyApp through the ACE common module path, the retry and the exception queue. The treatment record is rwb-treatment's. This story builds no basis check, no conduct check, no EasyApp client and no outbox send, and it owns none of the eleven legacy criteria; its own criteria test the request row, the write-once version, the branch link, the expiry, the idempotency, the external-reference read, the check constraint and the access refusal.

### 2. Business rationale

Agreements are printed, signed and couriered today, and the case waits days for the signed copy before booking can start. The document hub is the system of record for the agreement that ends that wait (DT06, CTL-12): it must hold the request that says which document was sent to which party by which method with which expiry, and it must hold the signed copy as a version that no later write can replace. It serves REQ-OCC-009.

In the monolith the request row, the version add, the branch link and the treatment update were one module and one transaction. In the target the facts split by owner: the request and the signed copy are here, the treatment signature is rwb-treatment's, the send and its result are rwb-comms', and the case routing is rwb-case's. What this story keeps is the durable half - a request state that survives a restart, an immutable version, and a unique external reference so that the same EasyApp result has one effect whatever the caller retries.

### 3. Preconditions

- `RWB-P6-E2018-APP` is delivered as the caller of the five request operations: it checks the signature basis of the template, runs the conduct check, holds the send in its outbox, applies the EasyApp result and records the treatment signature. This story is called by it and calls nothing back.
- The reference-data contract `RWB-P3-E1043-CON` is published (DP-07), so LOV-SIGN-METHOD (E_SIGNATURE, BRANCH, PAPER) and LOV-SIGN-STATUS (QUEUED, SENT, SIGNED, DECLINED, EXPIRED) are data rows with a version and not values in code. The contract is not in this story's contract list, which the Work Package fixes as empty (GAP-2354; ASM-3909).
- The `rwb_document` baseline is in place with `document`, `document_field`, `document_type`, `document_custody`, `document_intake`, `document_text`, `document_hub_parameter` and `retention_action` (TSD P5 T3.1), and the per-service Flyway sequence is live (DP-15, RWB-PLT-E1044-CON). `signature_request` is not defined in TSD P5 T3.1; this story creates it in `rwb_document` from the legacy field list (GAP-2353; ASM-3908).
- API-P5-005 `POST /documents/{documentId}/versions` exists as the version add of the store story, and the Blob container of the agreement's retention class is write-once (NFR-029, NFR-069). The container, the WORM tier, the size limit and the byte transfer behind the call are Not specified in the source documents (GAP-2356; ASM-3911).
- The agreement and any branch scan are already documents of this service, in state `STORED`, written by `RWB-P5-E1024-APP` and by the intake story of JOB-12 (`RWB-P5-E1057-APP`); this story does not fetch, scan or classify a file.
- The outbox and inbox library is live in schema `rwb_document` (DP-09, RWB-PLT-TE006-CON) and the workflow kit is present for the platform relay (DP-10, RWB-PLT-E1071-CON); neither is in the story's build list (GAP-2354; ASM-3909).
- The caller's role is resolved by the guard library from the cached answer of rwb-access; a refusal is 403 MSG-P4-002 and an object outside the scope is 404 MSG-P4-003, never an empty answer.
- The login is the rwb-document login (DP-02) and the schema is `rwb_document`; no foreign key crosses a schema.
- The browser never calls this service: every call arrives from rwb-comms or through the gateway-bff composite route (DP-19).
- Wave-0 platform prerequisites of this story, named here and not in the empty contract or build rows (GAP-2354): RWB-PLT-E1043-CON (DP-07), RWB-P3-E1043-CON (DP-07 reference-data contract), RWB-PLT-TE006-CON (DP-09), RWB-PLT-E1071-CON (DP-10), RWB-PLT-E1044-CON (DP-15) and RWB-PLT-N001-CON (DP-19).
- The contract baseline for the operations in section 12.1 is that section, built from the legacy shapes and TSD P6 T-A.1; the service contract tests keep it, and a later CON story takes it over without a code change (GAP-1184).

### 4. Flow

1. rwb-comms answers its own `POST /treatments/{treatmentId}/signature-requests` after the basis check and the conduct check, and calls this service once, one hop with a 2 s timeout and an Idempotency-Key (DP-11).
2. `POST /api/recovery/document/v1/cases/{caseId}/signature-requests` arrives with `documentId`, `partyId`, `method` and `expiresAt`; the expiry is the treatment's offer validity that rwb-comms sends, and this service reads no treatment row.
3. The request is validated before any row is written: the case and the document exist and the document belongs to the case (404 MSG-P4-003), the method is a value of LOV-SIGN-METHOD (422 MSG-GEN-001 naming "method"), the party key is present (422 MSG-GEN-001 naming "party"), the expiry is present (422 MSG-GEN-001 naming "expiresAt"), and the caller holds Documents C for the case (403 MSG-P4-002).
4. The request row is written with `status` `QUEUED`, `case_id`, `treatment_id`, `document_id`, `person_key`, `method`, `expires_at` and the standard record columns, and the answer is 201 `SignatureRequest` with the reference `RS-0301`. No person name, no identity number and no document content is stored.
5. rwb-comms sends to EasyApp, and on the accepted reference it calls the update with `externalRef` `EA-30001` and `status` `SENT`; the reference is unique, so a second send of the same request answers the stored row rather than a second one.
6. For an e-signature result, rwb-comms calls the update with `status` `SIGNED`, `signedAt` `2026-12-11 10:15:00` and the signed document; this story first adds the signed PDF through API-P5-005 as the next version of the agreement with `write_once` true, then sets the request `SIGNED` with the signed-at time and the signed document in one transaction on its own schema.
7. For a branch or paper result, the scan is already a document of the case from JOB-12, and the update carries `signedDocumentId` `D-0602` and `signedAt` `2026-12-12`; no version is written on that path and the scan is linked to the request as the signed agreement.
8. A decline sets `DECLINED`; a cancel on offer expiry sets `EXPIRED`. A result that arrives for `EXPIRED`, `DECLINED` or `SIGNED` is refused with 409 and MSG-P3-005, nothing is stored and the request keeps its state.
9. A repeated result for the same `externalRef` is absorbed by the unique index and the stored answer: one version, one state, one signed-at time.
10. rwb-comms reads one request by its reference `EA-99999` to resolve an unknown result; the answer is 404, which it turns into its own exception-queue reason "unknown signature request".
11. The version add writes the `document` row, its version chain through `previous_version_id`, and its outbox row, so `rwb.document.DocumentStored.v1` leaves on `rwb.document.events.v1` exactly as for any stored document (DP-09). No signature event is invented (GAP-2355; ASM-3910).
12. SCR-14 shows the request list and its status, and SCR-30 shows the signed version linked to the generated agreement; both read this service through the gateway-bff composite route (DP-19) and show the version, the write-once flag, the method and the status, never the PDF content.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document is not on the case, or the case is outside the caller's scope | Refused before any row is written; no request, no version | MSG-P4-003 | AC1 |
| X2 | The method or the status is not a value of its list | Refused before any row is written, naming the field | MSG-GEN-001 | AC1 |
| X3 | A `SIGNED` update arrives with no signed document or no signed-at time | Refused; the request keeps its state and no version is written | MSG-GEN-001 | AC7 |
| X4 | The same result arrives twice, or the same send is repeated | The unique external reference and the stored answer absorb it; one version and one state | None | AC5 |
| X5 | A result arrives for a request already `EXPIRED`, `DECLINED` or `SIGNED` | Refused with 409; the state is unchanged and nothing is stored | MSG-P3-005 | AC4 |
| X6 | An external reference matches no request | 404; the caller holds the result on its own exception queue and nothing is stored | None | AC6 |
| X7 | The Blob container or the store does not answer inside the budget | The version add fails closed, the request keeps `SENT`, the caller retries the same result; one entry records the degraded write | MSG-GEN-006 | AC2 |
| X8 | A caller holds Documents R only and tries to create or update a request | 403 before any row is touched; no signature request row is written | MSG-P4-002 | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against the P3 reference-data fake and the store path of API-P5-005; the caller rwb-comms, the treatment and EasyApp are not needed to prove any criterion |
| Negotiable | The request field names, the reference format and the expiry source can move; the write-once version, the unique reference, the check constraint and the access refusal cannot |
| Valuable | The agreement that proves a settlement is on the case once, unalterable, with the request state that says how it was signed and when |
| Estimable | One table, five request operations, one version add, one check constraint, one migration |
| Small | Fits one iteration with its tests, as the document slice of a legacy key split across three services |
| Testable | Component tests over seeded `rwb_document` rows, contract tests against the caller's fake and one run against the Blob container stub |

### 7. Acceptance criteria

```gherkin
Feature: E-signature flow for customers and the bank - the rwb-document slice

  Background:
    Given case "RC-2026-000888" has settlement treatment "T-0501" with offer validity 2026-12-20
    Given agreement document "D-0601" on case "RC-2026-000888" was generated from template "SET-AGREE" with signature basis "E_SIGNATURE_ALLOWED"
    Given the borrower is party "P-0088"
    Given the rwb-access contract mock returns Documents CRU for "RS-0301" over case "RC-2026-000888"

  Scenario: AC1 A signature request is created with its document, party, method and expiry (new, D-RCV-60)
    Given the rwb-case reference-data contract mock returns LOV-SIGN-METHOD with "E_SIGNATURE", "BRANCH" and "PAPER"
    When "RS-0301" sends POST /api/recovery/document/v1/cases/RC-2026-000888/signature-requests with document "D-0601", party "P-0088", method "E_SIGNATURE" and expiry 2026-12-20
    Then the answer is 201 with request "RS-0301" of status "QUEUED", method "E_SIGNATURE" and expires_at 2026-12-20
    Then the row carries case "RC-2026-000888", treatment "T-0501", document "D-0601" and party key "P-0088"
    And the row carries no person name, no identity number and no document content
    When "RS-0301" sends the same call with method "COURIER"
    Then the answer is 422 with MSG-GEN-001 naming "method"
    And no second signature request row is written

  Scenario: AC2 The signed copy is a new write-once version and the request is SIGNED (new, D-RCV-60)
    Given request "RS-0301" for "D-0601" has status "SENT" and external reference "EA-30001"
    When "RS-0301" applies result "SIGNED" for "EA-30001" with the signed PDF and signed at 2026-12-11 10:15:00
    Then version 2 of "D-0601" holding the signed PDF is stored on case "RC-2026-000888" with write_once true and doc_version 2
    Then the request has status "SIGNED", signed_at 2026-12-11 10:15:00 and signed_document_id "D-0601"
    And version 1 of "D-0601" is still readable and unchanged, and its content hash is the one it had before
    And no answer, event or log line carries the PDF bytes or the party key
    When the Blob container does not answer inside the 2 second budget
    Then the request keeps status "SENT" and the version add is refused with 503 and MSG-GEN-006 naming "Document storage"

  Scenario: AC3 A branch or paper result links the scan as the signed agreement (new, D-RCV-60)
    Given request "RS-0301" for "D-0601" has method "BRANCH"
    Given the branch scan "D-0602" of the signed agreement arrived through JOB-12 document intake on 2026-12-12
    When "RS-0301" applies result "SIGNED" with signed document "D-0602" and signed at 2026-12-12
    Then the request has status "SIGNED", method "BRANCH" and signed_document_id "D-0602"
    And "D-0602" is readable as a document of case "RC-2026-000888" and no new version of "D-0601" is written
    When request "RS-0301" for "D-0601" has method "PAPER" and result "SIGNED" arrives with scan "D-0702" and signed at 2026-12-14
    Then the request has status "SIGNED", method "PAPER" and signed_document_id "D-0702"
    And no version is written on either path and the agreement keeps doc_version 1

  Scenario: AC4 A request past its offer validity is EXPIRED and refuses a later result (new, D-RCV-60)
    Given request "RS-0301" for "D-0601" has status "SENT" and expires_at 2026-12-20
    When "RS-0301" cancels "RS-0301" with reason "OFFER_EXPIRED" on 2026-12-21
    Then the request has status "EXPIRED" and keeps expires_at 2026-12-20
    When a result "SIGNED" arrives for "EA-30001" on 2026-12-21
    Then the answer is 409 with MSG-P3-005
    And the request keeps status "EXPIRED", no version is written and signed_at stays empty
    And the signed PDF is stored nowhere in "rwb_document"

  Scenario: AC5 The same result twice has one effect (new, D-RCV-60)
    Given the result "SIGNED" for reference "EA-30001" was applied and "D-0601" has doc_version 2 with write_once true
    When the same result for "EA-30001" arrives again under the same Idempotency-Key
    Then the answer of the first call is returned
    And "D-0601" still has doc_version 2 and one version holds the signed PDF
    And "signature_request" holds one row for external reference "EA-30001"
    And the request keeps status "SIGNED" and its signed_at time
    When the same request is sent to EasyApp a second time and the reference "EA-30001" is written again
    Then the unique index refuses the second reference and one request row remains

  Scenario: AC6 A request is read by its external reference (new, D-RCV-60)
    Given request "RS-0301" carries external reference "EA-30001" and status "SENT"
    When a caller reads the request by external reference "EA-30001"
    Then the answer is 200 with request "RS-0301", its document "D-0601", its method "E_SIGNATURE", its status, its expiry 2026-12-20 and its signed-at time
    When a caller reads the request by external reference "EA-99999"
    Then the answer is 404 and no request row is returned
    And no version is written and no state changes on either call

  Scenario: AC7 A SIGNED result without a signed document is refused (new, D-RCV-60)
    Given request "RS-0301" has method "BRANCH" and status "SENT"
    When "RS-0301" applies result "SIGNED" with no signed document
    Then the answer is 422 with MSG-GEN-001 naming "signed document"
    And the request keeps status "SENT", signed_at stays empty and no version is written
    When the same state is written past the controller
    Then the check constraint on method and status refuses the row and the transaction rolls back

  Scenario: AC8 Only a role with Documents C or U writes a signature request (new, D-RCV-60)
    Given user "U-PC-02" holds RW-PHONECOL with Documents R over case "RC-2026-000888"
    Given the rwb-access contract mock returns Documents R for "U-PC-02"
    When "U-PC-02" sends POST /api/recovery/document/v1/cases/RC-2026-000888/signature-requests for "D-0601"
    Then the answer is 403 with MSG-P4-002 for action "create a signature request"
    And no signature request row is written
    When "U-PC-02" applies a result to request "RS-0301"
    Then the answer is 403 with MSG-P4-002 and the request keeps its state
    Given request "RS-0311" belongs to case "RC-2026-000889" outside the scope of "U-PC-02"
    When "U-PC-02" reads request "RS-0311"
    Then the answer is 404 with MSG-P4-003 and no row is returned

  Scenario: AC9 The service reads its method and status from the reference data, reads no template or case row, and writes rwb_document only (new, D-RCV-60)
    Given the rwb-case reference-data contract mock returns LOV-SIGN-METHOD with "E_SIGNATURE", "BRANCH" and "PAPER"
    When "RS-0301" sends POST /api/recovery/document/v1/cases/RC-2026-000888/signature-requests with document "D-0601", party "P-0088", method "BRANCH" and expiry 2026-12-20
    Then the answer is 201 with method "BRANCH" taken from LOV-SIGN-METHOD
    And no template or deviation row is read by this service, and no case row is written
    And the only table written is "signature_request" in "rwb_document"
    And the row carries no person name, no identity number and no document content

  Scenario: AC10 A call without a valid credential is refused 401 on each provided operation (new, D-RCV-60)
    When a caller sends POST /api/recovery/document/v1/cases/RC-2026-000888/signature-requests for "D-0601" with no credential
    Then the answer is 401 and no signature request row is written
    When a caller reads the request by external reference "EA-30001" with no credential
    Then the answer is 401 and no request row is returned
    And the request keeps its status and no version is written
```

The ten criteria above are new and test only this slice: the request row with its document, party, method and expiry, the signed copy as a write-once version and its refusal when the store is late, the branch and paper link, the expiry and the closed request, the idempotency of a repeated result and the unique reference, the read by external reference, the check constraint and the access refusal. No legacy criterion is copied here: the eleven criteria of RWB-E2-018 are owned by `RWB-P6-E2018-APP`, and only the source values of the legacy story are reused - case "RC-2026-000888", treatment "T-0501", offer validity 2026-12-20, document "D-0601" from template "SET-AGREE", party "P-0088", request "RS-0301", reference "EA-30001", reference "EA-99999", scan "D-0602" of 2026-12-12, signed at 2026-12-11 10:15:00, scan "D-0702" signed 2026-12-14, and the methods E_SIGNATURE, BRANCH and PAPER.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A signature request is one row of `signature_request` in `rwb_document` carrying the case, the treatment, the document, the party key, the method, the status, the external reference, the sent-at time, the signed-at time, the signed document and the expiry; the expiry is the offer validity the caller sends and is never computed here | REQ-OCC-009; legacy DF-DOC-096 to DF-DOC-107 |
| BR2 | The method and the status are values of LOV-SIGN-METHOD and LOV-SIGN-STATUS read through the reference-data contract, never values in code | DP-07; legacy section 13 |
| BR3 | The signed copy of an electronically signed agreement is a new version of that agreement with `write_once` true; no version replaces another and a superseded version stays readable | CTL-12; DT06; NFR-029; legacy BR7 |
| BR4 | A request may be `SIGNED` only with a signed document and a signed-at time; the check constraint refuses the state without them | legacy section 13; BR7 |
| BR5 | The same result twice has one effect: the external reference is unique, an applied result is not applied again, and the stored answer of the Idempotency-Key is returned | R-UNI-40; legacy BR8 |
| BR6 | `SIGNED`, `DECLINED` and `EXPIRED` are closed states: a later result is refused and nothing is stored, so the routing rules never act on a second signature fact | legacy BR4, BR5; R-RES-17, R-RES-18 |
| BR7 | The signature basis of the template and the conduct check are rwb-comms': this service reads no template, no deviation and no case row, and stores the method and the party key it is given | DP-01; Arch v5 slides 16 and 41; `RWB-P6-E2018-APP` |
| BR8 | The party is carried as a key only: no person name, no identity number and no PDF content is stored in `signature_request`, put on an event, a workflow input or a log | DL26; legacy section 17 |
| BR9 | The service reads and writes `rwb_document` only; no foreign key crosses a schema and no other service's table is read | DP-01; Arch v5 slide 13 |
| BR10 | One base `/api/recovery/document/v1`, one hop, a 2 s timeout and an Idempotency-Key on every write | DP-11, DP-13; ADR-020 |
| BR11 | The service publishes DocumentStored from the version add and no signature event: no SignatureRecorded is invented, no comms event is published for a signature, and callers read the request state through the five operations | GAP-1185; GAP-2355; TSD P5 T5.3 |
| BR12 | The request, its statuses and the signed copy are owned by this service; the signature basis and the circuit by rwb-comms; the treatment and its offer window by rwb-treatment; the three reconcile on the operations of section 12.1 and the events of BR11, never on a shared table; any further event name is Not specified in the source documents (GAP-2701) | GAP-2701; GAP-1596; DP-01 |

### 9. State transitions

None in the case: the case state machine is rwb-case's and the treatment state is rwb-treatment's. This story sets the signature request status and nothing else.

| From | Event | Condition | To |
|---|---|---|---|
| no request | a create is requested | the document is on the case, the method is a list value, the caller holds Documents C | QUEUED - the row exists with its expiry |
| no request | a create is requested | the method or a field is refused, or the caller lacks the right | REFUSED - 422 or 403, no row written |
| QUEUED | the caller reports the accepted send | the external reference is new | SENT - `external_ref` and `sent_at` written |
| QUEUED or SENT | an e-signature result `SIGNED` | the version add succeeds and the signed-at time is present | SIGNED - version written write-once, `signed_document_id` set |
| QUEUED or SENT | a branch or paper result `SIGNED` | the signed document is a document of the case | SIGNED - the scan is `signed_document_id`, no version written |
| SENT | a result `DECLINED` | none | DECLINED - the treatment is not signed |
| QUEUED or SENT | a cancel on offer expiry | OFFER_EXPIRED | EXPIRED - a later result is refused |
| SIGNED, DECLINED or EXPIRED | any result | the request is closed | unchanged - 409 MSG-P3-005, nothing stored |

The two reads of 12.1 change no state and add no value to LOV-SIGN-METHOD or LOV-SIGN-STATUS; the closed lists are owned outside this story.

### 10. Authority

The rights are the Documents rights of TSD P5 T6.1; the signature request adds no capability area and no right of its own, and the caller's scope filters every read and write.

| Who | What they may do in this story | TSD P5 T6.1 row |
|---|---|---|
| RW-RESTRUCT, restructuring officer (FCR) | Creates requests and applies branch and paper results (Documents CRU) | Documents CRU |
| RW-CASEOWN, case owner | Creates requests and applies results on own cases (Documents CRU) | Documents CRU |
| RW-LEGAL, Legal counsel | Reads the requests and the signed versions of the case (Documents CRUA); sets no basis here | Documents CRUA |
| RW-PHONECOL, phone collector | Reads the requests; refused on the create and on the update with MSG-P4-002 (TC-E2-018-12) | Documents R |
| CU-BORROW, customer (borrower) | Signs or declines in EasyApp or at a branch; no Workbench login and no call to this service | no Workbench row |
| SY-CASEWF, case workflow module | No call in this story: the cancel arrives from rwb-comms, not from the case module | Documents R |
| rwb-comms service identity | Calls the five request operations and the version add for the sends and the results | service identity |

No role grants itself a right, and the access answer is the guard library's read of rwb-access: a missing Documents C or U is 403 MSG-P4-002 and a case outside the scope is 404 MSG-P4-003.

### 11. Data

| BR Field ID | Entity in `rwb_document` | Field | Read or write |
|---|---|---|---|
| DF-DOC-096 | signature_request | id - the request reference `RS-0301` | Write |
| DF-DOC-097 | signature_request | case_id | Write |
| DF-DOC-098 | signature_request | treatment_id - carried by value, no treatment row is read | Write |
| DF-DOC-099 | signature_request | document_id - the agreement `D-0601` | Write |
| DF-DOC-100 | signature_request | person_key of the party, `P-0088`, no name | Write |
| DF-DOC-101 | signature_request | method, a value of LOV-SIGN-METHOD | Write |
| DF-DOC-102 | signature_request | status, a value of LOV-SIGN-STATUS | Write |
| DF-DOC-103 | signature_request | external_ref, unique, `EA-30001` | Write |
| DF-DOC-104 | signature_request | sent_at | Write |
| DF-DOC-105 | signature_request | signed_at | Write |
| DF-DOC-106 | signature_request | signed_document_id, `D-0601` for a version or `D-0602` for a scan | Write |
| DF-DOC-107 | signature_request | expires_at - the offer validity the caller sends | Write |
| DF-DOC-001, DF-DOC-004 | document | id, document_type of the agreement and of the scan | Read |
| DF-DOC-006, DF-DOC-010, DF-DOC-011 | document | storage_ref, write_once, doc_version of the new version | Write through the version add |
| DF-DOC-025 | document | previous_version_id - the chain the signed version joins | Write through the version add |
| DF-DOC-026 | document | content_sha256 of the signed version | Write through the version add |
| DF-REF-219, DF-REF-220 | document_type | doc_type_code and label of the agreement and the scan | Read |
| DF-TRT-001, DF-TRT-010, DF-TRT-030 | treatment (owner rwb-treatment) | id, valid_until, signature_status | Not read and not written here; they arrive through rwb-comms and are written by rwb-treatment |
| DF-REF-068 | template (owner rwb-comms) | signature_basis | Not read here; the basis check is rwb-comms' |

No person name, identity number, account number or document body is stored in `signature_request`, and no `document_text` row is read by this story. The one personal-data field carried is `person_key` (DF-DOC-100), a reference by value with no name attached. `rwb_document` holds no foreign key into another schema: `case_id`, `treatment_id` and `person_key` are references by value (TSD P5 T3.3). Field IDs are those of the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-document (P5); base `/api/recovery/document/v1`. The five signature-request operations carry no API ID: TSD P5 T-A.1 holds the seventeen document operations and no signature path, because the legacy key is a communications module story while the table is P5's (GAP-2352; ASM-3907). Their paths are the legacy section 12 shapes on this service's base (DP-13) and are the contract baseline of the story until the API Specification carries them. API-P5-005 is the published version add that already exists.

| Operation | Method | Path | Request | Answer | Errors | Access | Idempotency | API ID |
|---|---|---|---|---|---|---|---|---|
| Create a signature request | POST | `/cases/{caseId}/signature-requests` | `SignatureRequestCreate`: documentId, partyId, method, expiresAt | 201 `SignatureRequest` | 401; 403 MSG-P4-002; 404 MSG-P4-003; 422 MSG-GEN-001; 503 MSG-GEN-006 | Documents C, scope applied | Idempotency-Key header, answer stored | none in T-A.1 |
| List the requests of a case | GET | `/cases/{caseId}/signature-requests` | query `treatmentId`, `status`; the query names are Not specified in the source documents (GAP-2352; ASM-3907) | 200 `SignatureRequest[]` | 401; 403; 404; 503 | Documents R, scope applied | Not applicable | none in T-A.1 |
| Read one request | GET | `/signature-requests/{requestId}` | none | 200 `SignatureRequest` | 401; 403; 404; 503 | Documents R, scope applied | Not applicable | none in T-A.1 |
| Read a request by external reference | GET | `/signature-requests` | query `externalRef` `EA-30001`; the query name is Not specified in the source documents (GAP-2352; ASM-3907) | 200 `SignatureRequest`, or 404 when no request carries the reference | 401; 403; 404; 503 | Documents R, scope applied | Not applicable | none in T-A.1 |
| Update a request | PATCH | `/signature-requests/{requestId}` | `SignatureRequestUpdate`: status, externalRef, sentAt, signedAt, signedDocumentId, cancelReason | 200 `SignatureRequest` | 401; 403 MSG-P4-002; 404 MSG-P4-003; 409 the request is closed MSG-P3-005; 422 MSG-GEN-001; 503 MSG-GEN-006 | Documents U, scope applied | Idempotency-Key header, answer stored | none in T-A.1 |
| Add the signed copy as a version | POST | `/documents/{documentId}/versions` | the signed PDF, the reason and the write-once flag of the version add; the element names are TSD P5 T-A.2's | 201 `Document` with doc_version 2 and write_once true | 401; 403; 404; 409 a write-once version cannot be replaced; 422; 503 | Documents U, scope applied | Idempotency-Key header | API-P5-005 |

`SignatureRequest` schema: id, caseId, treatmentId, documentId, partyId, method, status, externalRef, sentAt, signedAt, signedDocumentId, expiresAt - the legacy schema of RWB-E2-018 section 12 with the party key named `partyId` as the legacy names it.

#### 12.2 REST operations consumed

| Call | Owner | Use in this story |
|---|---|---|
| `GET` reference data for LOV-SIGN-METHOD and LOV-SIGN-STATUS - the reference-data contract `RWB-P3-E1043-CON` (DP-07) | P3 rwb-case | The method and status values as data rows with a version; faked. The contract is not in the story's C row (GAP-2354; ASM-3909) |
| The authorise answer of rwb-access through the guard library | P4 rwb-access | Documents C, R or U and the scope; cached per request; not a contract dependency of this story |

Every row is one hop with a 2 s timeout and a breaker, and a GET is retried once with jitter (DP-11, ADR-020). This story calls no other service: it reads no case, no treatment, no deviation and no template, and it calls no downstream of a downstream.

#### 12.3 Events published

| Event | Topic | Owner of the type | Payload (IDs and facts only) |
|---|---|---|---|
| `rwb.document.DocumentStored.v1` | `rwb.document.events.v1` | P5 rwb-document | caseid, documentid, source, type as Kafka Catalog v1 EV-16 names them; written to the outbox by the version add in the same transaction |

No signature event is published. The service owns two events, EV-16 and EV-17 of the ownership rows, which TSD P5 T5.3 names `DocumentStored` and `DocumentFieldsExtracted`; neither is a signature event, so this story adds no `SignatureRecorded` event and no signature payload, and the request state is read through the operations of 12.1 (GAP-2355; ASM-3910).

#### 12.4 Events consumed

None. The cancel of an expired offer arrives as the update operation from rwb-comms, not as an event, and this story subscribes to no topic. The inbox of schema `rwb_document` exists for the intake path of JOB-12 and belongs to its own story; no consumer group is created here.

#### 12.5 Workflows and activities

None. The create, the update, the read and the version add are synchronous requests inside the 2 s budget, and the signed copy is a transaction, not a workflow step. `DocumentIntakeWorkflow` on task queue `rwb-document` belongs to the intake story and is the path by which a branch scan arrives; this story reads the document it produced.

#### 12.6 Schedules

None. JOB-12 Document intake and JOB-17 retention run belong to their own P5 stories and are Temporal Schedules of this service; this story registers no Schedule, no cron entry and no job name. DP-10 is claimed for the substitution of the legacy Quartz job that retried a send (JOB-11 in the legacy story) by the platform outbox relay and the workflow kit; the retry itself is rwb-comms' sender and the relay window is the platform's.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| signature_request | P5 (`rwb_document`) | The request row: document, case, treatment by value, party key, method, status, external reference, sent-at, signed-at, signed document, expiry; created by this story |
| document | P5 (`rwb_document`) | The agreement and the scan; the signed copy is a new version with `write_once` true, `doc_version`, `previous_version_id` and `content_sha256` |
| document_type | P5 (`rwb_document`) | The type code of the agreement and of the scan, read for the version metadata only |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_document` | The `DocumentStored` row of the version add and the stored answers of the two POSTs and the PATCH |
| document_field, document_custody, document_intake, document_text, retention_action, retention_rule, case_document_check, document_hub_parameter | P5 (`rwb_document`) | Same service, each owned by its own story; this story writes none of them |

Not owned and never written: `treatment` is rwb-treatment's, `recovery_case` is rwb-case's, `template` is rwb-comms' and `decision_log_entry` is rwb-decision's. No foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| P3 reference-data WireMock (`RWB-P3-E1043-CON`) | LOV-SIGN-METHOD with E_SIGNATURE, BRANCH and PAPER; LOV-SIGN-STATUS with QUEUED, SENT, SIGNED, DECLINED and EXPIRED; an unknown value answered absent | AC1, AC7 |
| rwb-access authorise fake (guard library) | Documents CRU for RW-RESTRUCT and RW-CASEOWN, Documents R for RW-PHONECOL, an out-of-scope case with MSG-P4-003 | AC8 |
| rwb-case contract fake | Not specified in the source documents (DOR-RWB-P5-E2018-APP-22) | Not specified in the source documents (DOR-RWB-P5-E2018-APP-22) |
| Blob container stub behind API-P5-005 | A write-once container that accepts version 2 of `D-0601`, refuses a replace of a stored version, and answers late or 503 for the degraded path | AC2, X7 |
| Seeded `rwb_document` fixture | Case "RC-2026-000888" with agreement `D-0601` at version 1 and scan `D-0602`; case "RC-2026-000889" with `D-0701` and scan `D-0702`; requests `RS-0301`, `RS-0311`, references `EA-30001` and `EA-99999` | AC1 to AC8 |
| Synthetic PDF fixtures | A signed PDF of the agreement and a scan image, both synthetic and never a real customer document (legacy section 17) | AC2, AC3 |

The container, the WORM tier, the size limit and the byte transfer of the version add are Not specified in the source documents, so the stub answers with the API-P5-005 shape of TSD P5 T-A.2 (GAP-2356; ASM-3911).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 6 provided, 1 consumed, 1 cached | The five request operations and API-P5-005 provided on `/api/recovery/document/v1`; the reference-data read consumed; the authorise answer cached; one hop, 2 s |
| Kafka | 1 published, none consumed | `DocumentStored` on `rwb.document.events.v1` from the version add, with retry and `.dlt` topics; no signature event |
| Temporal | None | No workflow, no activity and no Schedule; the intake workflow that delivers a scan belongs to its own story |
| File | 2 | The signed PDF arrives on the version add and the version content is readable on demand from the write-once container; neither is a file of this service's own volume |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, module `esign`, Java package `th.co.scb.ace.workbench.recovery.document.esign`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_document`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/document/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H and C dependencies of this table are held by the platform release train and by the rwb-case contract story; the Work Package fixes this story's metadata rows as empty and they stay empty here, with the absence recorded in section 3 and in GAP-2354 (ASM-3909). DP-05 applies as a prohibition: this story reads no ACE view and no ACE table, because the party key arrives on the request. DP-10 is claimed for the relay substitution of section 12.6 only and registers no Schedule.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| SignatureRequestController | Controller | The five operations, the validation order and the problem mapping for 401, 403, 404, 409, 422 and 503 |
| SignatureRequestService | Service | The create, the state machine of section 9, the closed-request refusal and the idempotent update |
| SignatureRequestRepository | Repository | Reads and writes `signature_request`; finds by external reference; holds the unique index and the check constraint |
| SignatureListGuard | Service | Resolves LOV-SIGN-METHOD and LOV-SIGN-STATUS through the reference-data contract and refuses a value outside them |
| SignedVersionWriter | Service | Adds the signed PDF as the next write-once version through API-P5-005 and sets the signed-at time and the signed document in the same transaction |
| SignatureLinkService | Service | Links a branch or paper scan that is already a document of the case as the signed document, with no version written |
| SignatureRequestReader | Service | The list, the single read and the read by external reference, masked and scope-filtered |
| IdempotencyStore | Repository | The stored answers of the two POSTs and the PATCH under their keys, in `idempotency_key` |

**Database and migrations**

- Creates `signature_request` in `rwb_document`: `id`, `case_id`, `treatment_id`, `document_id`, `person_key`, `method`, `status`, `external_ref`, `sent_at`, `signed_at`, `signed_document_id`, `expires_at` and the standard record columns; a unique index on `external_ref`, an index on `(treatment_id, status)` and one on `(case_id, created_at desc)`, and a check constraint on `method`, on `status` and on the pair `SIGNED` with `signed_document_id` not null.
- Migration `V2018_1__signature_request.sql` in the per-service Flyway sequence of `rwb_document` (DP-15); the legacy story named the same table in `V2_018__signature_request.sql` of the monolith, which is not reused.
- No row of another schema is created, altered or indexed, and `document` is written only through the version add of the store path.

**Configuration and reference data**

- LOV-SIGN-METHOD and LOV-SIGN-STATUS as data rows with a version, read through the reference-data contract (DP-07); no method, status or expiry is a constant in Java.
- The signature basis (DF-REF-068) is rwb-comms' and is not read here; the method arrives decided.
- The 60-second target for the signed copy is service configuration, as it is in the legacy story.
- The feature switch `rwb.document.esign`, default off in DEV and on in SIT: off refuses the five operations closed with MSG-GEN-006 and writes nothing.
- The login is the rwb-document login (DP-02).

**Build steps**

1. The migration and the entity, with the unique reference and the check constraint; test AC1 and AC7 at the database level.
2. `SignatureRequestController` and `SignatureRequestService` with the idempotency store; test AC1, AC5 and the refusal order.
3. `SignatureListGuard` against the P3 reference-data fake; test AC1 and AC7.
4. `SignedVersionWriter` on API-P5-005 against the container stub, with the write-once refusal and the late store; test AC2 and X7.
5. `SignatureLinkService` for the branch and paper paths with the scan already stored by JOB-12; test AC3.
6. The closed-request refusal and the cancel on expiry; test AC4.
7. `SignatureRequestReader`, the list and the read by external reference, with the 404 of `EA-99999`; test AC6.
8. The access path against the rwb-access fake, the scope refusal and the contract run of the caller's five operations; test AC8.

**Feature switch.** `rwb.document.esign`, read as service configuration; off refuses closed and stores nothing.

**Done when.** The twelve test cases of section 16 are run with the slice of each that this story answers, the signed copy is version 2 with `write_once` true within 60 seconds, `signature_request` holds one row per external reference, a closed request refuses a later result, and no PDF content, party name or identity number appears in a log, an event or a workflow input.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field is missing, or a value is outside its list | Enter {field}. |
| MSG-P4-002 | The caller's role holds no Documents C, R or U for the case | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case, the document or the request is unknown or outside the caller's scope | This case is not in your scope. |
| MSG-P3-005 | The request is closed and cannot take the result | This case cannot move to {state} from {current}. |
| MSG-GEN-006 | The store or a consumed contract does not answer inside the budget | {system} is not available. Your request is queued and will be retried. |

The texts are copied unchanged from legacy RWB-E2-018 section 14 and the message standard. MSG-P6-009, MSG-P6-001 and MSG-P3-004 are raised by rwb-comms, not here: this service never sees a template basis, a contact stop or a legal hold. {field} names the request field the caller must correct - "method", "party", "expiresAt" or "signed document" - and never a case fact; {action} names the action - for example "create a signature request" - and never a role or a party; {state} and {current} of MSG-P3-005 carry the request status, and the text is kept as the legacy writes it. No source gives rwb-document a message of its own for a closed signature request, and no source names the operation-level right of the five request operations beyond the Documents area of TSD P5 T6.1; both are carried as GAP-2357 and ASM-3912.

### 15. Screens and states

| Screen | State | What the user sees from this story |
|---|---|---|
| SCR-14 Treatment record | Approved, offer with the customer | The request list with method, status, expiry, signed-at and the signed document reference; Send for signature itself is rwb-comms' |
| SCR-14 Treatment record | Refused | The refusal of the create or the update, MSG-P4-002, MSG-P4-003, MSG-GEN-001 or MSG-P3-005 |
| SCR-14 Treatment record | Empty | Not specified in the source documents (CG-ALL-6196) |
| SCR-14 Treatment record | Loading | Not specified in the source documents (CG-ALL-6196) |
| SCR-14 Treatment record | Error | Not specified in the source documents (CG-ALL-6196) |
| SCR-14 Treatment record | No access | Not specified in the source documents (CG-ALL-6196) |
| SCR-30 Case documents | Linked to the generated agreement | The signed version with its version number, its write-once flag and its stored date, linked to the agreement it belongs to |
| SCR-30 Case documents | Empty | Not specified in the source documents (CG-ALL-6197) |
| SCR-30 Case documents | Loading | Loading state per Screen Specifications v1; what the user sees is Not specified in the source documents (CG-ALL-6197) |
| SCR-30 Case documents | Error | Not specified in the source documents (CG-ALL-6197) |
| SCR-30 Case documents | No access | Not specified in the source documents (CG-ALL-6197) |
| SCR-09 Exception queue | Held result | The reference of the request the caller could not resolve; the queue itself is rwb-comms' |
| SCR-09 Exception queue | Empty | Not specified in the source documents (CG-ALL-6195) |
| SCR-09 Exception queue | Loading | Loading state per Screen Specifications v1; what the user sees is Not specified in the source documents (CG-ALL-6195) |
| SCR-09 Exception queue | Error | Not specified in the source documents (CG-ALL-6195) |
| SCR-09 Exception queue | No access | Not specified in the source documents (CG-ALL-6195) |

All three are gateway-bff composite routes (DP-19); this story builds no screen and provides the answers behind them. No screen shows the PDF content: it shows the version, the write-once flag, the method, the status and the expiry.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-018-01 | AC2, BR1, BR3, BR5 | Component | T-0501 settlement; D-0601 E_SIGNATURE_ALLOWED; result SIGNED at 2026-12-11 10:15:00; version 2 write-once within 60 seconds |
| TC-E2-018-02 | AC3, BR1 | Component | Branch scan D-0602 of 2026-12-12 linked as the signed document |
| TC-E2-018-03 | AC3, BR1, BR6 | Component | T-0502 DIL Mortgage; D-0701; scan D-0702 signed 2026-12-14; no version written |
| TC-E2-018-04 | No criterion here; the basis check and the wet ink refusal are RWB-P6-E2018-APP | Component | E_SIGNATURE on D-0701 WET_INK_REQUIRED; the method list offered by the caller |
| TC-E2-018-05 | AC1, AC4, BR6 | Component | Result DECLINED for RS-0301; the request closed to further results |
| TC-E2-018-06 | AC4, BR6 | Component | Cancel on 2026-12-21 after expiry 2026-12-20, then a SIGNED result refused 409 |
| TC-E2-018-07 | No criterion here; the conduct check is RWB-P6-E2022-APP and RWB-P6-E2018-APP | Component | Open X2 with contact stop, refused by the caller before any call here |
| TC-E2-018-08 | AC1, BR1 | Component | The request created QUEUED while the caller queues its send |
| TC-E2-018-09 | AC5, BR5 | Component | Result EA-30001 twice; one version, one row, the stored answer returned |
| TC-E2-018-10 | AC6 | Contract | Result EA-99999; the read by external reference answers 404 |
| TC-E2-018-11 | AC7, BR4 | Component | Branch SIGNED with no signed document; 422 MSG-GEN-001 and the check constraint |
| TC-E2-018-12 | AC8, BR10 | Component | RW-PHONECOL with Documents R sends the create; refused 403 with MSG-P4-002 |
| TC-E2-018-13 | No criterion here; boundary of the 12.7 tables | Component | SIGNED result for RS-0301 with the version add; only the tables of 12.7 are written, no other table |
| TC-E2-018-14 | AC9, BR2, BR7, BR8, BR9 | Component | LOV-SIGN-METHOD mock with E_SIGNATURE, BRANCH and PAPER; D-0601; P-0088; no table outside rwb_document written |
| TC-E2-018-15 | AC10 | Component | No credential on the create for D-0601 and on the read of EA-30001; 401 each time, no row written |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The twelve legacy identifiers are kept in their legacy order because they are the legacy test set of this key; TC-E2-018-13 is a new boundary case for section 12.7 and has no legacy identifier; the rows whose behaviour belongs to the caller carry no criterion here and name the story that owns it. Legacy level System maps to Component for a service slice proved against its fakes, Access maps to Component, and TC-E2-018-10 is a Contract test of the caller's read. The `-ITG` copies of the same twelve belong to `RWB-ITG-E2018-ITG` and are not here.

### 17. Guardrails

- No business value in code: the methods, the statuses, the expiry and the 60-second target are data rows or service configuration read with their version (BR2).
- No personal data in events, workflow inputs, logs, tests or prompts: `signature_request` holds the party key, never a name or an identity number; the signed PDF is stored in the container and never logged; tests use synthetic PDFs (BR8).
- ACE data only through the owner's contract or the `v_ace_*` views - and this story reads neither: the party key arrives on the request (DP-05).
- No cross-schema read and no foreign key across a schema: `case_id`, `treatment_id` and `person_key` are references by value (BR9, DP-01).
- Write-once: a stored version is never replaced, deleted or edited inside its retention period, and a legal hold is applied by the retention story of this service, not by a signed-copy write (NFR-029, NFR-072).
- The signed copy is written through API-P5-005 only; no direct object-store write is made by this story, and no service other than rwb-document writes to the document container.
- Every call is one hop with a 2 s timeout and a breaker, and a write carries an Idempotency-Key (BR10, DP-11).
- The bank signing certificate stays in the key store (NFR-052); this service holds no private key and takes no part in adding the bank signature.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-009 | Electronic signature where Legal permits it, wet ink where Legal requires it: the request with its method and expiry is recorded, and the signed copy is an unalterable version of the agreement on the case | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-08, FEAT-OCC-09 | 7.3 Negotiate settlement or deed in lieu | R-RES-16; R-RES-17; R-RES-18; R-UNI-40; CTL-12; DT06 | TC-E2-018-01, TC-E2-018-02, TC-E2-018-03, TC-E2-018-09, TC-E2-018-11 |

| Legacy reference | Where it is kept |
|---|---|
| Story RWB-E2-018 | Split across RWB-P6-E2018-APP (the basis check, the conduct check, the send, the result and AC1 to AC11), this story (the request row, the write-once version, the branch link), the rwb-treatment slice of the key, RWB-P6-E2018-OPS (the deployment) and RWB-ITG-E2018-ITG (the end-to-end proof) |
| Legacy section 7, AC1 to AC11 | RWB-P6-E2018-APP; here AC1 to AC8 test only the document slice, with the caller stubbed |
| Legacy section 8, BR1, BR4, BR5, BR7, BR8 | Section 8 of this story (BR3, BR4, BR5, BR6) and of RWB-P6-E2018-APP (BR1, BR2, BR4) |
| Legacy section 11, DF-DOC-096 to DF-DOC-107, DF-DOC-006, 010, 011 | Section 11 of this story, now rows of `signature_request` and `document` in `rwb_document` |
| Legacy section 12, the three signature endpoints, `SignatureApi`, `SignatureResultListener`, `DocumentHubApi.addVersion` and `linkSigned` | Section 12 of this story: the five request operations and API-P5-005 on base `/api/recovery/document/v1`; the cancel is an update from rwb-comms |
| Legacy section 13, `SignatureRequestEntity`, the migration `V2_018__signature_request.sql`, the components | Section 13 of this story; the send, the listener and the dialog stay with RWB-P6-E2018-APP |
| Legacy section 14, MSG-GEN-001, MSG-GEN-006, MSG-P3-005, MSG-P4-002, MSG-P4-003 | Section 14 of this story; MSG-P6-009, MSG-P6-001 and MSG-P3-004 stay with rwb-comms |
| Legacy section 16, TC-E2-018-01 to TC-E2-018-12 | Section 16 of this story, with the slice of each case this story answers |
| Legacy section 15, SCR-14, SCR-30, SCR-09 | Section 15 of this story as the data behind the screens; the screens are the edge's |
| Legacy `-ITG` copies | RWB-ITG-E2018-ITG |

### 19. Out of scope

- The signature basis of the template, the method choice, the conduct check, the send to EasyApp, the retry, the exception queue and AC1 to AC11: `RWB-P6-E2018-APP`.
- The treatment signature record and the OFFER_EXPIRED trigger: rwb-treatment and rwb-case.
- The case routing after a signature, the field inspection and the Land Office transfer: rwb-case and the Epic 3 stories.
- The deployment of the capability, its container and its monitoring: `RWB-P6-E2018-OPS`.
- The document store, its containers and the version chain: `RWB-P5-E1024-APP`; the generation of the agreement: `RWB-P5-E2017-APP` and `RWB-P5-E2026-APP`; the intake that delivers a branch scan: `RWB-P5-E1057-APP`.
- The retention, archive and legal hold of the signed version: `RWB-P5-E1017-APP` and the retention story of this service.
- The end-to-end proof of these values across rwb-comms, rwb-document, rwb-treatment and the gateway: `RWB-ITG-E2018-ITG`.
