# RWB-ITG-E2018-ITG E-signature flow for customers and the bank

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2018-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP05, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P5-E2017-APP, RWB-P6-E2018-APP, RWB-P5-E2018-APP, RWB-S2-E2018-APP |
| Contract dependencies | RWB-P3-E1043-CON |
| Platform dependencies (wave 0) | RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Integration dependencies | RWB-P5-E2017-APP, RWB-P6-E2018-APP, RWB-P5-E2018-APP, RWB-S2-E2018-APP |
| External dependencies | None |
| Size | Not specified in the source documents (DOR-RWB-ITG-E2018-ITG-16) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-OCC-009) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-018 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E2018-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (13 resolved, 24 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **integration engineer (RW-TRIBE)**, I want **a repeatable cross-service journey harness for the e-signature flow that runs the signed, branch and paper, decline, expiry, duplicate-result and unavailable-path journeys against the owning services' contracts, the contract fakes and the ACE common module test path, and records the evidence of every run**, so that **the signed copy on the case and the signature result on the treatment are proven end to end across rwb-comms, rwb-document, rwb-treatment, rwb-access and rwb-decision before the wave 2 release**.

This story builds the harness and its evidence only. It builds no production screen, endpoint or table, and it changes no service code.

### 2. Business rationale

A settlement completes without paper only where Legal permits it, and the case waits for the signed copy before booking can start (REQ-OCC-009; legacy RWB-E2-018 business rationale). The legacy story delivers that inside one module, where the document hub, the treatment record, the conduct check and the decision log are all in one process. In the target architecture the same journey crosses four services and the ACE common module: rwb-comms creates the request and receives the result, rwb-document stores the signed copy as a new write-once version, rwb-treatment records signed or not signed, rwb-access authorises each call, and rwb-decision holds the record (Architecture v5 Text Extract v1 slides 13, 16, 17 and 18).

Each of those behaviours is owned by a service story in this wave, and each of those stories tests its own part against a contract fake. Nothing in the wave proves the whole journey: that a SIGNED result from EasyApp becomes version 2 of D-0601 on the case within 60 seconds (legacy RWB-E2-018 §12 target), that the branch scan D-0602 is linked and BRANCH is recorded, that the paper deed in lieu reaches rwb-case with CUSTOMER_ACCEPTED and signature basis WET_INK, that a decline records not signed, that an expired request refuses a later result without touching rwb-treatment, and that the same EA-30001 result twice stores one version and records the signature once (R-UNI-40).

The harness does that. It calls each owner on its own base `/api/recovery/<short>/v1` (DP-13), one hop with a 2-second timeout (DP-11), through the gateway-bff composite route where a screen is in the journey (DP-19), and it reads the topic `rwb.decision-record.v1` to check that the journey is recorded (DP-09). It is the evidence the wave 2 exit needs, and it is repeatable, so the same journeys are re-run when an owning service changes its contract.

### 3. Preconditions

- The four integration dependencies are in build or published as contracts: RWB-P6-E2018-APP (requests and results), RWB-P5-E2018-APP (signed copy as a version), RWB-P5-E2017-APP (generated agreement and its signature basis), RWB-S2-E2018-APP (signature status on the treatment). This story does not wait for them: from Day 1 it runs against their contracts and the fakes of §12.8.
- Each owning service publishes its OpenAPI contract before code, and a contract fake exists for every operation of §12.2 (Architecture v5 slide 11).
- The e-signature request and result paths sit on the rwb-comms base `/api/recovery/comms/v1`; the signed copy on the rwb-document base `/api/recovery/document/v1`; the treatment record on the rwb-treatment base `/api/recovery/treatment/v1`; the authorise check on the rwb-access base `/api/recovery/access/v1`; the decision log on the rwb-decision base `/api/recovery/decision/v1` (DP-13; Architecture v5 slide 41).
- EasyApp is reached only through the ACE common module e-signature path (INT-34). The EasyApp test tenant and the route to it through the ACE common module are Not specified in the source documents (GAP-0402; ASM-0577).
- The signature basis per template is available as data on the generated agreement (E_SIGNATURE_ALLOWED or WET_INK_REQUIRED); the method list is E_SIGNATURE, BRANCH, PAPER and the request status list is QUEUED, SENT, SIGNED, DECLINED, EXPIRED (legacy RWB-E2-018 §13).
- The harness runs in SIT. The harness environment, the data seeding, the signed PDF fixture, the evidence format and the evidence retention are Not specified in the source documents (GAP-0402; ASM-0577).
- No build dependency. Day 1.

### 4. Flow

1. Harness: reads the journey file and the run settings (base per service, 2-second timeout, the 60-second signed-copy target, the retry limit of 5).
2. Harness: seeds the case facts for the journey: case RC-2026-000888, settlement T-0501 with offer validity 2026-12-20 and state OFFER_WITH_CUSTOMER_SET, agreement D-0601 generated from template SET-AGREE TH with signature basis E_SIGNATURE_ALLOWED, borrower party P-0088 with no contact stop.
3. Harness: calls `POST /api/recovery/comms/v1/treatments/{treatmentId}/signature-requests` with the document, the party and the method, and keeps the returned request id as RS-0301.
4. Harness: calls `GET /api/recovery/comms/v1/treatments/{treatmentId}/signature-requests` to read the request state after each step of the journey.
5. Harness: drives the EasyApp result through the ACE common module test path, or posts the same result on `POST /api/recovery/comms/v1/signature-requests/{requestId}/result` where the journey is a branch or paper result, and records the signed document and the signed date it sends.
6. Harness: reads `GET /api/recovery/document/v1/documents/{documentId}` on D-0601 and checks that version 2 exists, that write_once is true and that the stored version is the signed copy, within the 60-second target.
7. Harness: calls `PATCH /api/recovery/treatment/v1/treatments/{treatmentId}` to record the signature and reads `GET /api/recovery/treatment/v1/treatments/{treatmentId}` to check signed true or false and the method (E_SIGNATURE, BRANCH or PAPER) on S2.
8. Harness: reads `GET /api/recovery/decision/v1/decision-log` for the case and checks that the journey is recorded, and consumes `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` to check the event of the journey.
9. Harness: exercises `POST /api/recovery/access/v1/authorise` for the acting role on every call of the journey, so an operation refused by authority is seen as a refusal and not as an error.
10. Harness: exercises JOB-11 Outbox sender on the unavailable path: the send stays in the outbox, the relay retries every minute, and the journey stops at the retry limit of 5 (Architecture v5 slide 44; legacy RWB-E2-018 AC8).
11. Harness: writes one run report keyed by story key and business date, with the journey, the requests, the observed results, the pass or fail of each step and the evidence references, and attaches it to the wave 2 run record.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | An owning service answers 404 or a 5xx on its base | The journey stops at that step; the report names the step, the service and the operation, and the run fails | None | AC1 |
| X2 | The signed copy is not version 2 or not write_once within 60 seconds | The report names the document, the observed version and the elapsed seconds, and the run fails | None | AC1 |
| X3 | The treatment record is not updated with signed and method | The report names the treatment and the values it read, and the run fails | None | AC1 |
| X4 | EasyApp is not reachable at the test route | The request returns 201 QUEUED with MSG-GEN-006 naming EasyApp and the outbox path is exercised to the retry limit of 5 | MSG-GEN-006 | AC5 |
| X5 | An expired request receives a later SIGNED result | The result is held on the exception queue, S2 is not called and the report shows the held result | None | AC3 |
| X6 | A service answers a refusal the journey expects (MSG-P4-002, MSG-P6-009 or MSG-P6-001) | The refusal is recorded as the expected result of that step, not as an error | MSG-P4-002, MSG-P6-009, MSG-P6-001 | AC2 |
| X7 | The authorise check refuses the acting role | The step is recorded as refused and the journey continues only where the journey file marks a refusal as expected | MSG-P4-002 | AC2 |

The report text is for the integration and QA teams and is not part of the message standard. Business messages are those of section 14 and are copied from legacy RWB-E2-018 §14.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs on the four contracts and the fakes of §12.8 from Day 1; no build dependency, and each fake is replaced by the real service as its I story lands |
| Negotiable | The journey file, the run settings, the seeded facts and the evidence envelope are data and configuration, never code |
| Valuable | The wave 2 exit is decided on one repeatable run of every e-signature journey instead of four separate component tests |
| Estimable | One journey runner, one contract-fake set, one evidence writer, one gate |
| Small | Fits in one sprint with its tests |
| Testable | Each journey ends in an asserted state, and every failure names the step, the service and the observed value |

### 7. Acceptance criteria

```gherkin
Feature: E-signature flow for customers and the bank, run as one cross-service journey

  Background:
    Given the harness runs in SIT on the per-service bases /api/recovery/<short>/v1 through gateway-bff
    Given every call is one hop with a 2-second timeout
    Given case "RC-2026-000888" has settlement treatment "T-0501" with offer validity 2026-12-20 and state "OFFER_WITH_CUSTOMER_SET"
    Given agreement document "D-0601" on the case was generated from template "SET-AGREE" "TH" with signature basis "E_SIGNATURE_ALLOWED"
    Given the borrower is party "P-0088" with no contact stop

  Scenario: AC1 The signed copy reaches the case and S2 records the signature (new, D-RCV-60)
    Given "RS-0301" sent "D-0601" for e-signature to party "P-0088" on 2026-12-10
    When EasyApp returns signing result "SIGNED" with the bank signature applied at 2026-12-11 10:15:00
    Then within 60 seconds version 2 of "D-0601" holding the signed PDF is stored on case "RC-2026-000888" with write_once true
    Then the signature request has status "SIGNED"
    Then the harness reads signed true and method "E_SIGNATURE" on "T-0501" through GET /api/recovery/treatment/v1/treatments/{treatmentId}
    Then the decision log read on GET /api/recovery/decision/v1/decision-log holds the journey for case "RC-2026-000888"

  Scenario: AC2 The branch scan and the paper deed in lieu finish the same journey (new, D-RCV-60)
    Given "RS-0301" created a signature request for "D-0601" with method "BRANCH"
    Given the branch scan "D-0602" of the signed agreement arrived through document intake on 2026-12-12
    When "RS-0301" records result "SIGNED" with signed document "D-0602" and signed date 2026-12-12
    Then the signature request has status "SIGNED" and method "BRANCH"
    Then the harness reads "D-0602" linked to case "RC-2026-000888" as the signed agreement
    Given case "RC-2026-000889" has deed in lieu treatment "T-0502" for product "MORTGAGE"
    Given its contract document "D-0701" was generated from template "DIL-CONTRACT-MTG" with signature basis "WET_INK_REQUIRED"
    Given "RS-0301" created a signature request for "D-0701" with method "PAPER"
    When "RS-0301" records result "SIGNED" with scan "D-0702" and signed date 2026-12-14
    Then the signature request has status "SIGNED" and method "PAPER"
    Then the harness reads signed true and method "PAPER" on "T-0502"
    Then P3 receives event CUSTOMER_ACCEPTED with signature basis "WET_INK" and moves the case to "WITH_FIELD_INSPECTION" under R-DIL-18

  Scenario: AC3 The decline and the expired request do not sign the treatment (new, D-RCV-60)
    Given "D-0601" was sent for e-signature on 2026-12-10
    When EasyApp returns signing result "DECLINED" on 2026-12-11
    Then the signature request has status "DECLINED"
    Then the harness reads signed false on "T-0501"
    Given "D-0601" was sent for e-signature on 2026-12-10 and has status "SENT"
    Given P3 raised OFFER_EXPIRED for "T-0501" on 2026-12-21 and called SignatureApi.cancel
    When EasyApp returns signing result "SIGNED" for that request on 2026-12-21
    Then the signature request keeps status "EXPIRED"
    Then the harness holds the result on the exception queue
    Then the harness reads no signature call on "T-0501" for that result

  Scenario: AC4 The same signing result twice stores one version and records the signature once (new, D-RCV-60)
    Given the signing result "SIGNED" for request reference "EA-30001" was applied
    When the same result for "EA-30001" arrives again
    Then the harness reads no second version of "D-0601"
    Then the harness reads one signature call on "T-0501"
    Then the harness counts the repeat under rule R-UNI-40

  Scenario: AC5 The EasyApp path unavailable queues the send and retries to the limit (new, D-RCV-60)
    Given the ACE path to EasyApp returns "unavailable"
    When "RS-0301" sends "D-0601" for e-signature
    Then the response is status 201 with status "QUEUED" and MSG-GEN-006 naming "EasyApp"
    Then JOB-11 retries the send until it is accepted or the retry limit of 5 is reached
    Then the harness reads the attempt count of 5 in its report

  Scenario: AC6 A status change the model does not allow is refused (new, D-RCV-60)
    Given "D-0601" was sent for e-signature on 2026-12-10 and has status "DECLINED"
    When EasyApp returns signing result "SIGNED" for that request on 2026-12-11
    Then the signature request keeps status "DECLINED"
    Then the harness reads the result held on the exception queue
    Then the harness reads no signature call on "T-0501" for that result
```

These six criteria are new for the ITG harness and do not restate the app criteria owned by the I stories.

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
| BR9 | A system that is unavailable queues the send and retries | R-UNI-33 |

The rules are the legacy rules of RWB-E2-018. This story asserts them across services; it owns none of them, and the rule text and the rule package stay with rwb-decision and the owning service.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Waiting customer | Customer responds, or the validity timer expires | Signature recorded, decline recorded, or OFFER_EXPIRED | In progress |

P3 makes the case status change on the treatment update this story sends. This story sets the signature request status: Queued, Sent, Signed, Declined, Expired.

The harness changes no state itself: it reads the state the owning services hold through their contracts, and it changes a case, a document, a request or a treatment only by calling the owner's operation of §12.2.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, tribe lead and squad members | Write and change the journey file, start a run, read the evidence |
| QA lead | Owns the journey set, the pass criteria and the evidence sign-off |
| Integration lead | Owns the contract-fake set and the cut-over from a fake to the real service |
| RW-RESTRUCT, restructuring officer (FCR) | The acting role the harness uses for create and result calls, with its own rights, in SIT |
| RW-PHONECOL | The refusal role of the access journey (MSG-P4-002) |
| RW-LEGAL, Legal counsel | Reads the evidence; sets the signature basis on the template in RWB-E1-034, not in this story |
| No approval level from the delegation of authority applies | The harness takes no business decision and approves nothing |

The authority inside the journey is that of legacy RWB-E2-018 §10 and is enforced by rwb-access and by the owning services. This story adds no authority.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read, through the rwb-case contract |
| DF-TRT-001 | treatment | id | Read, through the rwb-treatment contract |
| DF-TRT-030 | treatment | signature_status | Read, through the rwb-treatment contract |
| DF-DOC-001 | document | id | Read, through the rwb-document contract |
| DF-DOC-011 | document | doc_version | Read, through the rwb-document contract |
| DF-DOC-010 | document | write_once | Read, through the rwb-document contract |
| DF-REF-068 | template | signature_basis | Read, through the rwb-document contract |
| DF-DOC-102 | signature_request | status | Read, through the rwb-comms contract |

The harness owns no table and reads no service schema directly (DP-01). Field IDs are those of the Logical Data Model and Data Dictionary. The seeded facts of the journey come from the SIT data set and the harness fixture.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test capability and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/comms/v1/treatments/{treatmentId}/signature-requests` | P6 rwb-comms | Create the request: documentId, partyId, method (E_SIGNATURE, BRANCH, PAPER) |
| GET | `/api/recovery/comms/v1/treatments/{treatmentId}/signature-requests` | P6 rwb-comms | Read the request state and method after each step |
| POST | `/api/recovery/comms/v1/signature-requests/{requestId}/result` | P6 rwb-comms | Record a branch or paper result: result, signedDocumentId, signedAt |
| GET | `/api/recovery/document/v1/documents/{documentId}` | P5 rwb-document | Read the document version, write_once and storage reference of the signed copy |
| POST | `/api/recovery/document/v1/documents/{documentId}/versions` | P5 rwb-document | Add the signed copy as version 2, write-once, as the EasyApp path does |
| PATCH | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | The treatment contract that records signature_status, which the legacy TreatmentApi.recordSignature writes |
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | Read back the recorded signature_status and method for the journey assertion |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The authorise check on every acting role (Architecture v5 slide 41 first API path `/authorise`; slide 14 `POST /authorise`) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | Read the decision log for the case, and the record of the journey |

Every call is one hop from the harness to the owner on the owner's base (DP-11, DP-13), with a 2-second timeout and an Idempotency-Key on every POST (Architecture v5 slide 11). Where a screen is in the journey the call is made through the gateway-bff composite route (DP-19). The request and response schemas are those of the owning service's published OpenAPI; this story introduces none. Contract version: the /v1 path major version; the exact OpenAPI version is Not specified in the source documents (DOR-RWB-ITG-E2018-ITG-23).

#### 12.3 Events published

None. The harness publishes no Kafka event; its evidence goes to the wave 2 run record.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | all 19 services | Assert that the journey is recorded against the case (Architecture v5 slide 42, event 08) |

#### 12.5 Workflows and activities

None added. JOB-11 Outbox sender is exercised: the unavailable path of AC5 watches the outbox relay retry every minute to the retry limit of 5 (Architecture v5 slide 44). The harness starts no workflow and no activity, and the service workflows of the journey stay with their owning stories.

#### 12.6 Schedules

None. JOB-11 is the outbox relay of every service and needs no Schedule from this story; the harness creates no Temporal Schedule (DP-10 resolves to "exercise the relay, add no job").

#### 12.7 Tables owned

None. The harness owns no table, creates no schema and reads no service's tables (DP-01).

Ownership of the signature facts the journey asserts (Architecture v5 slides 16 and 41; Ownership Map ruling):

- P5 rwb-document owns `signature_request`, its statuses and the signed version, including the migration `V2018_1__signature_request.sql` in the `rwb_document` sequence (RWB-P5-E2018-APP).
- P6 rwb-comms owns the signature basis check and the circuit: it creates the request through the rwb-document contract, receives the result and calls rwb-treatment. It holds no signature table.
- S2 rwb-treatment owns the signature record of its treatment, the offer validity and the closure of the signature window.
- Request status read path: the stored status is rwb-document's, listed by `GET /api/recovery/document/v1/cases/{caseId}/signature-requests`; the harness reads it through the rwb-comms operation `GET /api/recovery/comms/v1/treatments/{treatmentId}/signature-requests`.
- The three services are reconciled through their published operations and the events `rwb.treatment.SignatureRecorded.v1` and `rwb.treatment.SignatureWindowClosed.v1` on `rwb.treatment.events.v1`, never through a shared table.

#### 12.8 Contract fakes

| Fake | Covers | Replaced by |
|---|---|---|
| WireMock stub of rwb-comms | The three signature-request operations of §12.2 | RWB-P6-E2018-APP |
| WireMock stub of rwb-document | Document read and version add, with version 2 and write_once | RWB-P5-E2018-APP and RWB-P5-E2017-APP |
| WireMock stub of rwb-treatment | Treatment read and the signature status write | RWB-S2-E2018-APP |
| WireMock stub of rwb-access | `POST /authorise`, allow and refuse | RWB-P4-E2018-APP |
| WireMock stub of rwb-decision | Decision-log read | RWB-P7-E2018-APP |
| Stub of the ACE common module notification and e-signature path | The EasyApp send and result (INT-34) | The ACE common module test path, once the test tenant is agreed |

The fake replaces only the owner's REST answer. Each fake is removed from the journey set as its I story lands, and the run report records which fakes were in use. The EasyApp test tenant and the route through the ACE common module are Not specified in the source documents (GAP-0402; ASM-0577).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 9 consumed, one hop per call, 2-second timeout, Idempotency-Key on every POST |
| Kafka | 1 consumed (`rwb.decision.DecisionRecorded.v1`), 0 published |
| Temporal | None added; the JOB-11 outbox relay is exercised, no workflow or Schedule |
| File | None, except the signed PDF object store read through the rwb-document contract |

### 13. Solution plan

**Package.** Folder `integration/recovery/esign` in the ACE repository, package `<ACE base package>.recovery.integration.esign`. Not part of a deployed service.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyFile | Rule table | One row per journey: steps, acting role, method, seeded facts, expected result |
| RunSettings | Rule table | Base per service, 2-second timeout, 60-second signed-copy target, retry limit 5 |
| SeedFixture | Service | Seeds the case, treatment, documents and party facts of the journey in SIT |
| JourneyRunner | Service | Calls each owner on its base, one hop, and records the observed result of every step |
| EasyAppDriver | Service | Drives the EasyApp send and result through the ACE common module test path and the result operation |
| DuplicateReplay | Service | Replays the same EA-30001 result and counts the repeat under R-UNI-40 |
| OutboxProbe | Service | Watches the JOB-11 relay on the unavailable path and counts the attempts to the limit of 5 |
| EvidenceWriter | Service | Writes the run report keyed by story key and business date, with the fake set and the gate result |
| HarnessGate | Service | Passes or fails the run against the pass criteria of the journey file |

**Database.** None. The harness owns no schema and uses the API only (DP-01; DP-15 applies to the owning services, not here).

**Environment and test data.** SIT, against the owning services' published contracts and the contract fakes of §12.8, with the EasyApp test path of the ACE common module. The harness environment, the data seeding and the evidence format and retention are Not specified in the source documents (GAP-0402; ASM-0577). The journey uses the legacy facts: case RC-2026-000888, settlement T-0501, agreement D-0601, party P-0088, request RS-0301, branch scan D-0602, deed in lieu contract D-0701 with scan D-0702, case RC-2026-000889 and treatment T-0502, and the result references EA-30001 and EA-99999.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H rows of this table (DP-07, DP-09, DP-10, DP-15, DP-19) are delivered by platform wave 0 stories and are not repeated in the metadata H column, which stays empty for this story. The harness reads reference data and party facts through the owner's contract rather than through a table (DP-05), and every event it sees is read from the owner's topic (DP-09). The dependencies that block the journey's Done are the I stories of the metadata: the real services replace the fakes.

**Build steps**

1. Write the journey file and the run settings, with the facts and the pass criteria of section 16.
2. Stand up the five WireMock fakes and the ACE common module path stub of §12.8, and wire the journey to them.
3. Write SeedFixture and JourneyRunner; run AC1 end to end against the fakes.
4. Add the branch and paper journeys and the scan link; run AC2.
5. Add the decline and the OFFER_EXPIRED cancel path with the held result; run AC3.
6. Add DuplicateReplay and the R-UNI-40 count; run AC4.
7. Add OutboxProbe and the retry limit of 5; run AC5.
8. Write EvidenceWriter and HarnessGate, attach one run to the wave 2 run record, then replace each fake with its real service as the I story lands and re-run.

**Feature switch.** `rwb.integration.esign.journey`, switched on for the SIT run and off in production. The harness runs in SIT only.

**Done when.** The twelve test cases of section 16 pass against the fakes on Day 1, and the same twelve pass with every fake replaced by the real service when RWB-P6-E2018-APP, RWB-P5-E2018-APP, RWB-P5-E2017-APP and RWB-S2-E2018-APP are done, with the signed-copy evidence signed off by the integration and QA leads.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-009 | E-signature asked for a document that needs wet ink | Legal requires a wet ink signature for {document}. Use the branch or paper path. |
| MSG-P6-001 | A contact stop is in force | Contact with this customer is stopped for {reason}. |
| MSG-P3-004 | A legal hold is on the case | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-GEN-006 | The EasyApp path is unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-GEN-001 | A branch or paper result has no scan | Enter {field}. |
| MSG-P3-005 | The request is not open, or the treatment is not with the customer | This case cannot move to {state} from {current}. |
| MSG-P4-002 | The access step of AC2 is refused | Not specified in the source documents (DOR-RWB-ITG-E2018-ITG-9) |

MSG-GEN-006 is asserted by AC5, MSG-P4-002 by the access step of AC2, and the remaining messages are recorded as the expected refusals of the journey file. The message text is copied from legacy RWB-E2-018 §14 and stays owned by rwb-comms and the owning services.

### 15. Screens and states

SCR-14 Treatment record (states Draft; submitted; approved; booked; broken): in state approved, while the offer is with the customer, the officer sees Send for signature and the request list with status. SCR-30 Case documents (states Loading; list; upload) shows the signed copy linked to the generated agreement. SCR-09 Exception queue (states Loading; list) lists held signing results. The customer sees EasyApp only.

SCR-09, SCR-14 and SCR-30 handle these states as follows (Screen inventory and navigation v2, Common states; the wording comes from the error and message standard). The harness builds none of them.

| State | How it shows on SCR-09, SCR-14 and SCR-30 |
|---|---|
| Loading | Skeleton rows while data arrives; no spinner over the whole page |
| Empty | A plain sentence saying there is nothing to show, and the action to take if one applies |
| Error | The message from the error and message standard next to the field or at the top |
| No access | Access is checked on every request; an action outside the role's permission is refused with MSG-P4-002, shown as in the Error state |

The harness reads those states through the contracts of §12.2 and adds no screen and no state. The screenshot evidence and its retention are Not specified in the source documents (GAP-0402; ASM-0577).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-018-01-ITG | AC1 (legacy AC1), BR2, BR7 | Integration | T-0501 settlement; D-0601 E_SIGNATURE_ALLOWED; EasyApp stub SIGNED |
| TC-E2-018-02-ITG | AC2 (legacy AC2), BR1 | Integration | Branch scan D-0602 |
| TC-E2-018-03-ITG | AC2 (legacy AC3), BR1, BR3 | Integration | T-0502 DIL Mortgage; D-0701 WET_INK_REQUIRED; scan D-0702 |
| TC-E2-018-04-ITG | AC2 (legacy AC4), BR1 | Integration | E_SIGNATURE on D-0701; method list offered for WET_INK_REQUIRED |
| TC-E2-018-05-ITG | AC3 (legacy AC5), BR4 | Integration | EasyApp stub DECLINED |
| TC-E2-018-06-ITG | AC3 (legacy AC6), BR5 | Integration | Cancel on 2026-12-21, then SIGNED result |
| TC-E2-018-07-ITG | AC1 (legacy AC7), BR6 | Integration | Open X2 with contact stop |
| TC-E2-018-08-ITG | AC5 (legacy AC8), BR9 | Integration | EsignPort stub unavailable |
| TC-E2-018-09-ITG | AC4 (legacy AC9), BR8 | Integration | Result EA-30001 twice |
| TC-E2-018-10-ITG | AC3 (legacy AC10), exception queue | Integration | Result EA-99999 |
| TC-E2-018-11-ITG | AC2 (legacy AC11), BR1 | Integration | Branch SIGNED with no document |
| TC-E2-018-12-ITG | Access (legacy TC-E2-018-12) | Component | RW-PHONECOL sends POST /api/recovery/comms/v1/treatments/{treatmentId}/signature-requests; refused with MSG-P4-002 |
| TC-E2-018-13-ITG | AC6 (new) | Integration | Signature request DECLINED; EasyApp stub SIGNED result; status stays DECLINED, the result is held on the exception queue and no signature call is made on the treatment |

The legacy TC IDs keep their numbering, and every ITG copy ends in `-ITG` (§R7.2 s16). The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same legacy test case ID.

### 17. Guardrails

- No business value in code: the signature basis, the methods, the statuses, the expiry, the 60-second target and the retry limit of 5 are data or configuration.
- No personal data in logs, evidence, tests or prompts: the journey uses the SIT masked data set, the signed PDF is a synthetic fixture, and the evidence holds IDs, states and numbers only.
- No read of another service's tables: every read and write goes through the owner's contract (DP-01).
- The harness never runs against UAT or production, and never holds the bank signing certificate (NFR-052); it calls the ACE common module path only and never EasyApp directly.
- An exception to a limit is never added to a journey file; a limit that must change is changed in the configuration through a reviewed pull request.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-009 | Electronic signature where Legal permits it, wet ink where Legal requires it | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-08, FEAT-OCC-09 | 7.3 Negotiate settlement or deed in lieu | R-RES-16, R-RES-17, R-RES-18, R-SET-10, R-SET-11, R-SET-12, R-DIL-18, R-DIL-27, R-UNI-33, R-UNI-40 | TC-E2-018-01-ITG to TC-E2-018-12-ITG |

### 19. Out of scope

- The owning service stories and their production code: RWB-P6-E2018-APP, RWB-P5-E2018-APP, RWB-P5-E2017-APP and RWB-S2-E2018-APP, and the generation story RWB-E2-017.
- The contract baselines of the owning services, which are their CON stories; this story consumes the published contracts and changes none.
- Booking the signed treatment in ALS and NLEADS (R-RES-22, Epic 3).
- The deed in lieu field inspection and Land Office transfer screens (Epic 3).
- Signature in customer self-service (FEAT-COM-02, Epic 4).
- Generating the documents to be signed (RWB-E2-017, RWB-E2-026).
- UAT and production runs, and the EasyApp test tenant agreement, which the ACE common module owner holds.
