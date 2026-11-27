# RWB-ITG-E2017-ITG Contract, CA and mortgage document generation screens

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2017-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-017 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP11, DP13, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P6-E1034-APP, RWB-P5-E2017-APP, RWB-S2-E2017-APP, RWB-P7-E2017-APP, RWB-P6-E2017-APP, RWB-P4-E2017-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-DCM-012, REQ-OCC-002, REQ-OCC-009) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-017 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-ITG-E2017-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **member of the integration and QA team**, I want **a repeatable cross-service journey harness that runs the contract, credit approval and mortgage document set through gateway-bff and the owning services**, so that **the wave 2 document generation journey is proven end to end, with evidence, before the release is accepted**.

This story builds the harness and the evidence only. It builds no production screen, endpoint, table, workflow or schedule. The real behaviour is owned by the I stories RWB-P6-E1034-APP, RWB-P5-E2017-APP, RWB-S2-E2017-APP, RWB-P7-E2017-APP, RWB-P6-E2017-APP and RWB-P4-E2017-APP, and those stories block the ITG run.

### 2. Business rationale

The legacy RWB-E2-017 journey crosses more than one service: rwb-treatment holds the approved deed in lieu treatment, rwb-document holds the template versions, the generated documents and the write-once copies, rwb-comms holds the signature request, rwb-access answers the authorisation check and rwb-decision holds the decision records. Until the real services are exercised together through the gateway, the program cannot show that the set is produced, corrected and sent without re-keying, which is the outcome the program targets at 5 days from 23 days.

The harness gives one repeatable run per business date that proves the composite screen route composes the set one hop at a time inside the 2 s budget, that a correction is recorded before the draft is regenerated, that a send is write-once and idempotent, and that a failure in one service is isolated. It meets REQ-DCM-012, REQ-OCC-002 and REQ-OCC-009 at the integration level and leaves every business rule and every screen behaviour where the owning stories put them.

### 3. Preconditions

- The six I stories are published and deployed in the SIT environment: RWB-P6-E1034-APP (template versions and merge fields), RWB-P5-E2017-APP (generation, regenerate, review and write-once), RWB-S2-E2017-APP (treatment and the DEED_IN_LIEU set), RWB-P7-E2017-APP (decision record and ledger), RWB-P6-E2017-APP (signature request) and RWB-P4-E2017-APP (authorise).
- gateway-bff is deployed with the composite route of DP-19 available. The gateway-bff composite route path and its merge order: Not specified in the source documents (GAP-0401; ASM-0576).
- The contract fakes of §12.8 are published from the owning services' OpenAPI documents, so the harness can run from Day 1 before the I stories land.
- The document types CONTRACT, CREDIT_APPROVAL and MORTGAGE_DOCUMENT and the reference data that maps DEED_IN_LIEU to DIL-CONTRACT, DIL-CA and DIL-MORTGAGE are loaded by the owning stories.
- The harness environment, its test-data seeding and its evidence format and retention: Not specified in the source documents (GAP-0401; ASM-0576).

### 4. Flow

1. Harness: seeds the synthetic case, the approved treatment and the three approved template versions through the owning contracts or the published fakes.
2. Harness: calls the gateway-bff composite route for the document set of the treatment and asserts the set, the template versions and the authorised action.
3. Harness: chooses Generate documents and confirms, then reads the three produced drafts through the rwb-document contract.
4. Harness: corrects an overridable merge value with a reason, asserts the decision record first, then the regenerated doc_version, then that the earlier version is still readable.
5. Harness: marks each document reviewed and sends the set with one Idempotency-Key.
6. Harness: asserts the write-once copy, the document state, the single signature request and the decision record with final_call.
7. Harness: repeats the send with the same Idempotency-Key and asserts that no second signature request exists.
8. Harness: forces each failure of §5 through the fakes, asserts the message and that nothing moved, then returns the fake to its healthy answer and completes the send.
9. Harness: writes one run report per business date, keyed by story and business date; the report format and retention are Not specified in the source documents (GAP-0401; ASM-0576).

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case |
|---|---|---|---|---|
| X1 | The treatment is not approved or is closed | Generate is refused; a direct POST generated-documents returns 409 and nothing is created | MSG-P5-011 | TC-E2-017-04-ITG |
| X2 | A correction has no reason | 422; the document stays at its doc_version | MSG-GEN-001 | TC-E2-017-05-ITG |
| X3 | The value is locked in the merge field catalog | 422; nothing changes | MSG-P5-014 | TC-E2-017-06-ITG |
| X4 | Send with a document of the set not reviewed | 422; no write-once copy and no signature request | MSG-P5-013 | TC-E2-017-07-ITG |
| X5 | A change to a document already sent | 409; the document is unchanged | MSG-P5-002 | TC-E2-017-08-ITG |
| X6 | The decision record write fails on a correction or a send | 503; nothing moves | MSG-P7-003 | TC-E2-017-09-ITG, TC-E2-017-15-ITG |
| X7 | Send is chosen twice | One signature request; the second call returns the first result | None | TC-E2-017-10-ITG |
| X8 | Two officers correct the same draft | The second save gets 409 | MSG-GEN-004 | TC-E2-017-11-ITG |
| X9 | The signature service refuses the request | 503; documents stay REVIEWED; the retry with the same key completes once | MSG-GEN-006 | TC-E2-017-12-ITG |
| X10 | The template version changed after the drafts were made | Send is refused; the officer regenerates | MSG-P5-013 | TC-E2-017-13-ITG |
| X11 | The user holds Documents R only | 403 on a direct call; the composite route hides the action | MSG-P4-002 | TC-E2-017-14-ITG |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs on its own once the six I stories are deployed; until then it runs against the §12.8 fakes |
| Negotiable | The harness pack, the data seeding and the evidence format are agreed with QA; no business value is fixed by the harness |
| Valuable | The document journey is evidenced across services rather than per service |
| Estimable | One harness project, one journey specification, one fake pack and one run report |
| Small | Fits in one iteration with the owning stories' contract tests |
| Testable | Each scenario of §7 is one automated journey with synthetic data and a machine-checkable result |

### 7. Acceptance criteria

```gherkin
Feature: Contract, CA and mortgage document generation screens - wave 2 integration harness

  Background:
    Given case "RW-2026-000401" with product group "MORTGAGE" in team "FCR-BKK"
    Given treatment "TRT-0401" of type "DEED_IN_LIEU" approved at D6.4 with no outcome
    Given the set for "DEED_IN_LIEU" is "DIL-CONTRACT" version 2, "DIL-CA" version 1 and "DIL-MORTGAGE" version 1, all approved by Legal
    Given a restructuring officer with role RW-RESTRUCT and scope team "FCR-BKK"

  Scenario: AC1 The composite document set through gateway-bff (new, D-RCV-60)
    Given the harness calls the composite document set route at "Not specified in the source documents (GAP-0401; ASM-0576)" for "TRT-0401"
    When gateway-bff composes the answer from rwb-treatment, rwb-document, rwb-comms and rwb-access
    Then the route returns the set "DIL-CONTRACT" version 2, "DIL-CA" version 1 and "DIL-MORTGAGE" version 1 for the treatment type "DEED_IN_LIEU"
    And every call in the composition is one hop with the 2 s budget
    And no service reads another service's schema
    And the run report holds one trace spanning the gateway and each owning service

  Scenario: AC2 Generate, correct and regenerate three documents (new, D-RCV-60)
    Given the officer opens the document set for "TRT-0401" and chooses Generate documents and confirms
    When the harness reads the produced documents through the rwb-document contract
    Then three documents of types "CONTRACT", "CREDIT_APPROVAL" and "MORTGAGE_DOCUMENT" exist with template versions 2, 1 and 1
    When the harness corrects contract_date on "DOC-0411" from "2026-12-10" to "2026-12-12" with reason "Signing appointment moved by the customer"
    Then one decision record exists with decision code "D6.4", the old value, the new value and the reason as override_reason
    And "DOC-0411" is served at doc_version 2
    And doc_version 1 stays readable

  Scenario: AC3 Send the reviewed set for signature (new, D-RCV-60)
    Given the three documents of "TRT-0401" are in state "REVIEWED"
    When the harness sends the set for signature with header Idempotency-Key "S-0401"
    Then one signature request exists for the three documents
    And each document has write_once true and state "SENT"
    And one decision record exists with final_call "SENT_FOR_SIGNATURE"
    And the route response shows MSG-P5-012 with count 3

  Scenario: AC4 Failure isolation and the idempotent retry (new, D-RCV-60)
    Given rwb-comms returns "UNAVAILABLE" for the signature request
    When the harness sends the three reviewed documents for signature
    Then the response is 503 with MSG-GEN-006
    And the documents stay in state "REVIEWED"
    And no copy is written to the write-once container
    When the same send with Idempotency-Key "S-0401" is repeated after rwb-comms recovers
    Then one signature request exists for "TRT-0401" and the documents are in state "SENT"
```

These four criteria are new for the ITG harness and do not restate the app criteria owned by the I stories.

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

The harness asserts these rules against the owning services; it does not re-implement them. No BR row is changed by this story.

### 9. State transitions

The document states below are the states the harness observes. The harness changes no case status and no document state itself; every transition is caused by a call to the owning service.

| From | Event | Condition | To |
|---|---|---|---|
| document state DRAFT | Correction saved | Overridable field, reason given, decision log written | DRAFT, doc_version + 1 |
| document state DRAFT | Marked reviewed | None | REVIEWED |
| document state REVIEWED | Correction saved | As above | DRAFT, doc_version + 1 |
| document state REVIEWED | Send for signature | All of the set REVIEWED, current template version, decision log written, signature request accepted | SENT, write_once true |

A failed send leaves every document in REVIEWED and writes no copy to the write-once container.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT, restructuring officer (FCR) | The synthetic user the harness drives: generates, corrects, marks reviewed and sends in scope (Documents CRU) |
| RW-CASEOWN, case owner | Generates, corrects, marks reviewed and sends in scope (Documents CRU) |
| RW-TEAMMGR, team manager | Reads the drafts and sent documents (Documents R); used by the access case |
| RW-LEGAL, legal counsel | Reads the set; owns which fields are overridable (Documents CRUA) |
| SY-DECLOG, decision log writer | Writes the correction and send entries |

No approval level from the delegation of authority applies in this story; the treatment was approved at D6.4 before generation. Authorisation is answered by rwb-access through POST /authorise.

### 11. Data

The harness owns no table. It reads the fields below through the owning services' contracts and asserts them; the field IDs are those of the Logical Data Model and Data Dictionary.

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
| DF-DOC-006 | document | storage_ref | Read |
| DF-DOC-008 | document | review_status | Read |
| DF-DOC-010 | document | write_once | Read |
| DF-DOC-011 | document | doc_version | Read |
| DF-DOC-032 | document | template_id | Read |
| DF-DOC-033 | document | treatment_id | Read |
| Standard column | document | state, version | Read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Read |

Test data is synthetic. No production case, party or document is used, and no personal data is written to a run report.

### 12. Contract

#### 12.1 REST operations provided

None. The harness calls the owning services; it serves no operation.

#### 12.2 REST operations consumed

One hop per call, no chaining; the 2 s timeout and the circuit breaker per downstream of DP-11 apply to every row.

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | Treatment type, decision_log_id and outcome for the set |
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` | P5 rwb-document | The set, the document states and doc_version |
| GET | `/api/recovery/document/v1/cases/{caseId}/document-checklist` | P5 rwb-document | The checklist the set is asserted against |
| POST | `/api/recovery/document/v1/cases/{caseId}/generated-documents` | P5 rwb-document | Generate the set; 409 when the treatment is not approved |
| POST | `/api/recovery/document/v1/documents/{documentId}/regenerate` | P5 rwb-document | Correction with overrides and reason; next doc_version |
| POST | `/api/recovery/document/v1/documents/{documentId}/review` | P5 rwb-document | Mark a draft REVIEWED |
| POST | `/api/recovery/comms/v1/treatments/{treatmentId}/signature-requests` | P6 rwb-comms | Send the set; Idempotency-Key required |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Role, scope and DoA check used by the composite route and by the direct calls (Architecture v5 slide 14: rwb-access IN POST /authorise) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The decision records of the correction and the send |
| GET | `/api/recovery/comms/v1/admin/templates` | P6 rwb-comms | The template code, version and Legal approval of the set |

The composite screen route itself is gateway-bff (DP-19), owned by the platform edge story RWB-PLT-N001-CON. Its path and merge order are Not specified in the source documents (GAP-0401; ASM-0576).

#### 12.3 Events published

None. The harness produces no event.

#### 12.4 Events consumed

| Event | Topic | Owner | What the harness asserts |
|---|---|---|---|
| rwb.decision-record.DecisionRecorded.v1 | rwb.decision-record.v1 | P7 rwb-decision (ledger); every service publishes its own record | The correction record and the send record reach the ledger within 5 minutes of the call |

#### 12.5 Workflows and activities

None added. The harness starts no workflow and adds no activity; it drives REST only.

#### 12.6 Schedules

None. The harness run is started by the test pipeline, not by a Temporal Schedule and not by Airflow.

#### 12.7 Tables owned

None.

#### 12.8 Contract fakes

| Fake | Serves | Stubbed answers |
|---|---|---|
| rwb-treatment | GET /treatments/{treatmentId} | TRT-0401 approved at D6.4 of type DEED_IN_LIEU; TRT-0402 with no decision_log_id |
| rwb-document | documents, document-checklist, generated-documents, regenerate, review | Three drafts with template versions 2, 1 and 1; DOC-0411 at doc_version 1; locked transfer_price; 409 on a sent document; 422 for an empty reason and for a stale version |
| rwb-comms | signature-requests, admin/templates | ACCEPTED with one requestId; UNAVAILABLE for the failure case; DIL-CONTRACT 2, DIL-CA 1, DIL-MORTGAGE 1 approved |
| rwb-access | authorise | Allow RW-RESTRUCT in scope; refuse RW-TEAMMGR for Documents U with MSG-P4-002 |
| rwb-case | case facts for the composite route | RW-2026-000401, product group MORTGAGE, team FCR-BKK |
| rwb-decision | decision-log, DecisionRecorded | The correction record with decision code D6.4; the send record with final_call SENT_FOR_SIGNATURE; a forced write failure for the 503 case |

The fakes are replaced by the real service as each I story lands, contract by contract. The harness repository and its environment: Not specified in the source documents (GAP-0401; ASM-0576).

#### 12.9 Call-type summary

| Call type | Used | Detail |
|---|---|---|
| REST | Yes | Ten consumed operations of §12.2 through gateway-bff and the owning services; one hop, 2 s timeout, breaker per downstream |
| Kafka | Yes | Consumes rwb.decision-record.DecisionRecorded.v1 on rwb.decision-record.v1; publishes nothing |
| Temporal | No | Starts no workflow and adds no activity or Nexus operation |
| File | No | Reads no file itself; the write-once copy is asserted through rwb-document metadata (write_once true, storage_ref) |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies named by this table are delivered by the platform wave and are not repeated in the metadata H list. The blocking dependencies of this story are the I stories.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Test harness | Runs one journey per business date, keyed by story and business date, and stops at the first failed assertion with the trace |
| CompositeRouteClient | Harness adapter | Calls the gateway-bff composite route and the ten consumed operations of §12.2 with the Idempotency-Key header where the operation requires one |
| FakePack | WireMock project | Serves rwb-treatment, rwb-document, rwb-comms, rwb-access, rwb-case and rwb-decision from the published OpenAPI documents of §12.8 |
| SchemaBoundaryCheck | Assertion | Fails the run on any cross-schema reference found in the trace, so a service never reads another service's tables |
| CounterVerifier | Assertion | Checks MSG-P5-012 with count 3, one signature request per Idempotency-Key, and the presence of one decision record per action |
| RunReportWriter | Reporter | Writes one run report with the trace and the per-assertion result; format and retention Not specified in the source documents (GAP-0401; ASM-0576) |

**Environment and test data**

- Environment: SIT, one namespace, the owning services deployed from their wave 2 builds or replaced by the §12.8 fakes. Harness repository, environment and data seeding: Not specified in the source documents (GAP-0401; ASM-0576).
- Data: synthetic case RW-2026-000401, treatment TRT-0401 of type DEED_IN_LIEU approved at D6.4, the three approved templates, the synthetic officer with RW-RESTRUCT in team FCR-BKK, and the send key S-0401. No production record is copied.
- Reset: each run starts from the seeded state, so a repeated run is deterministic and the same report is produced.

**Build steps**

1. Build JourneyRunner and CompositeRouteClient against the published OpenAPI documents of the owning services.
2. Publish FakePack for the six owning services from the same documents, and prove the harness runs green from Day 1 on the fakes.
3. Add the composite route assertion of AC1, including the 2 s per-call budget and the SchemaBoundaryCheck.
4. Add the generate, correct and regenerate journey of AC2, asserting the decision record before the new doc_version.
5. Add the send journey of AC3 and the idempotent repeat, then the failure isolation of AC4.
6. Replace each fake with the real service as its I story lands, contract by contract, keeping the same assertions.
7. Publish the run report per business date and add the pass/fail gate agreed with QA; the gate definition: Not specified in the source documents (GAP-0401; ASM-0576).

**Feature switch:** the harness has no production feature flag and runs in the test environment only. The production switch it exercises is `rwb.dochub.generation-screens` with `rwb.dochub.generation-screens.send` from the legacy solution plan; the harness asserts the disabled state and the enabled state of the send step.

**Done when:** the journey runs green against the six deployed I stories in SIT, the run report for the business date holds every assertion of §7 and §16 with its trace, and the pass/fail gate agreed with QA is met for one full business date.

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

The harness asserts the message ID and the substituted values; it does not own the message text. Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | State | What the harness asserts |
|---|---|---|
| SCR-14 Treatment record | Approved | The document set and its template versions are returned by the composite route; Generate documents is available; Send for signature is available when all are reviewed |
| SCR-14 Treatment record | Draft, submitted | Generate documents is disabled and the answer carries MSG-P5-011 |
| SCR-30 Case documents | List | A draft, its merge values and the correction form with a reason are returned; the reviewed state is set on request |
| SCR-30 Case documents | Read only (common state) | A sent document, or any document for RW-TEAMMGR, is returned without edit controls |

The harness opens no screen and renders no page; it asserts the composite route answer that the screen consumes. Screen-level behaviour remains with the owning APP stories. The harness environment and evidence detail: Not specified in the source documents (GAP-0401; ASM-0576).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-017-01-ITG | AC1, BR1, BR2; ITG AC1, ITG AC2 | Integration | Synthetic mortgage DIL treatment, three approved templates |
| TC-E2-017-02-ITG | AC2, BR3, BR4, BR5; ITG AC2 | Integration | Contract date moved by two days |
| TC-E2-017-03-ITG | AC3, BR6, BR7, BR8; ITG AC3 | Integration | Three reviewed drafts; rwb-comms returns ACCEPTED |
| TC-E2-017-04-ITG | AC4, BR2 | Integration | Treatment with no decision_log_id |
| TC-E2-017-05-ITG | AC5, BR3 | Integration | Empty reason |
| TC-E2-017-06-ITG | AC6, BR3 | Integration | Locked transfer price |
| TC-E2-017-07-ITG | AC7, BR6 | Integration | One draft not reviewed |
| TC-E2-017-08-ITG | AC8, BR7 | Integration | Document in state SENT |
| TC-E2-017-09-ITG | AC9, BR4 | Integration | Decision record fake refusing writes on a correction |
| TC-E2-017-10-ITG | AC10, BR10; ITG AC4 | Integration | Same send key twice |
| TC-E2-017-11-ITG | AC11 | Integration | Two sessions on one draft |
| TC-E2-017-12-ITG | AC12; ITG AC4 | Integration | rwb-comms returns UNAVAILABLE, then ACCEPTED |
| TC-E2-017-13-ITG | AC13, BR6 | Integration | Template version 3 made current after the drafts |
| TC-E2-017-14-ITG | Access | Component | RW-TEAMMGR user (Documents R) calls POST generated-documents/send; refused with MSG-P4-002 |
| TC-E2-017-15-ITG | Principle 5 | NFR | Decision record write forced to fail on send; nothing sent, documents stay REVIEWED, MSG-P7-003, incident raised |

The AC column in Covers is the legacy AC of RWB-E2-017 that the copy is derived from; the ITG AC is the criterion of §7 that the copy asserts at integration level. The full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the legacy test case ID.

### 17. Guardrails

- No business value in code: the set per treatment type, the locked and overridable fields, the legal flag and the thresholds are data held by the owning services; the harness reads them and never holds a copy.
- No personal data in logs, tests, traces or reports: merge values, reasons and file names are not logged; the harness uses synthetic parties and stores IDs and assertions only.
- No read of another service's schema: every read goes through the owner's contract, the SchemaBoundaryCheck fails the run on a cross-schema reference, and only rwb-source-data reads the ACE views.
- No production data and no outside system: the harness calls only the owning services and their fakes, never an outside gateway or a production endpoint, and it never writes to the write-once container itself.
- A document copied to the write-once container is never changed; the harness asserts that state and does not create it.
- One hop only: the harness fails a run when the trace shows a call chain deeper than the gateway and one owner.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-012 | Contracts, credit applications and mortgage documents generated from approved templates with no re-keying | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-OCC-07 | 7.3 Negotiate settlement or deed in lieu; 13 Manage documents and correspondence | R-DIL-14, R-DIL-16, R-DIL-18, R-UNI-39, R-UNI-40 | TC-E2-017-01-ITG to TC-E2-017-12-ITG, TC-E2-017-14-ITG, TC-E2-017-15-ITG |
| REQ-OCC-002 | Templates versioned with the Legal approval recorded against the version | Business Requirements Program, section 5.6; Epic 2, section 3.5 | FEAT-OCC-07 | 13 Manage documents and correspondence | R-LIT-03 | TC-E2-017-01-ITG, TC-E2-017-13-ITG |
| REQ-OCC-009 | The customer signs electronically where Legal permits it and by wet ink where Legal requires it | Business Requirements Program, section 5.6; Epic 2, section 3.6 | FEAT-OCC-07 | 7.3 Negotiate settlement or deed in lieu; 13 Manage documents and correspondence | R-DIL-18, R-RES-16 | TC-E2-017-03-ITG, TC-E2-017-12-ITG |

### 19. Out of scope

- The owning service APP stories: RWB-P6-E1034-APP, RWB-P5-E2017-APP, RWB-S2-E2017-APP, RWB-P7-E2017-APP, RWB-P6-E2017-APP and RWB-P4-E2017-APP, and every screen, endpoint, table and rule they build.
- Production code in any service: the harness is test and evidence only.
- The contract baselines of rwb-treatment, rwb-document, rwb-comms, rwb-access, rwb-case and rwb-decision, which their CON stories own.
- Platform deployment, the gateway-bff composite route implementation (RWB-PLT-N001-CON) and the platform configuration of Kafka, Temporal and the observability stack.
- The e-signature flow, the wet ink path and the return of the signed copy (RWB-E2-018); the letter dispatch loop and proof of delivery (RWB-E2-021); SMS and LINE dispatch (RWB-E2-022); and the generation engine, template selection and merge rules (RWB-E2-026).
- Rule-driven generation on the deed in lieu route (FEAT-TRT-18, Epic 3) and settlement offer letters (R-SET-04, Epic 3).
