# RWB-P6-E2021-CON Letter dispatch loop with proof of delivery from WIN

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- The ledger row is the case-scoped append with `InteractionRequest` 5.1.0, its header, keys and answers (RD-P1-001, RD-P1-007; finding #1).
- Proof results are a consumed answer of the rwb-source-data proof-of-delivery read, not of rwb-integration, and the consent fact is the DP02 records read (RD-P1-005, RD-P1-007; findings #2, #3).
- The rwb-source-data fake is the provider fake 5.1.0, the version is pinned and the events carry `ce_idempotencykey` (RD-P1-009, RD-P1-011; findings #4, #5).
- Pending: GAP-2096 (read timing), NEW-GAP-F14-9 (a row with no callback date) and NEW-GAP-D3 (WIN status mapping). The ledger keys and references are ruled (RD-P1-064; NEW-GAP-S10-16 and NEW-GAP-F14-2 closed).
- Finishing pass: ledger keys and references follow RD-P1-064; the proof of delivery is the rwb-source-data read, never an rwb-integration INT-15 result (request F15-affected-0021, confirmed); test case IDs of Test Cases v9 and the Error and Message Standard v6 wording applied.
- Test case citations aligned to Test Cases v9: identifiers of this story replace the placeholders and the shared legacy identifiers that now hold another story's case (W2-tests mapping).

| Item | Value |
|---|---|
| Story key | RWB-P6-E2021-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-021 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P6-E2021-CON-16); the squad sizes the story at refinement |
| Contract version | v1, as in the /v1 paths of section 12.2; rwb-source-data.yaml 5.1.0 with provider fake 5.1.0; the version of each other provider contract is Not specified in the source documents (DOR-RWB-P6-E2021-CON-23) |
| Patterns applied | DP01, DP03, DP05, DP07, DP09, DP10, DP11, DP13, DP18, DP19 |
| Readiness decisions | RD-P1-001; RD-P1-005; RD-P1-007; RD-P1-009; RD-P1-011, RD-P1-064, RD-P1-004 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | H RWB-PLT-E1027-CON; H RWB-PLT-E1043-CON; H RWB-PLT-TE006-CON; H RWB-PLT-E1071-CON; H RWB-PLT-E1044-CON; H RWB-PLT-N001-CON |
| Contract dependencies | C RWB-P3-E1043-CON (rwb-case reference-data contract); C rwb-source-data.yaml 5.1.0 (RWB-P1-E1055-APP proof read, RWB-P1-E1066-CON ledger, RWB-P1-E2021-APP DP02 consent rows and letter rules) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (FR-P6-010, FR-P6-013, FR-P6-015, FR-P6-016, FR-P6-017, FR-P6-018, FR-P6-019, FR-P6-020, FR-P6-021, FR-P6-022, FR-P6-027, FR-P6-028, FR-P6-029, FR-P6-030, FR-P6-031, FR-P6-036) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-021 for rwb-comms. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P6-E2021-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (24 resolved, 32 cross-document, 5 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, ledger row, proof-of-delivery and consent rows, fakes and event headers aligned with RD-P1-001, 005, 007, 009 and 011. Tool: Claude Code / Claude Sonnet 5.5.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the dispatch loop of rwb-comms — the notice request and the notice read on `/api/recovery/comms/v1`, the dispatch file contract with rwb-integration and WIN, the dispatch fields on `notice`, the hold reason and Unserved vocabulary, the three published event envelopes and the three consumed events, the JOB-10 Schedule and its handoff, the nine contract tables and the fakes**, so that **the app, operations and test stories of this legacy key build against one fixed, testable contract on Day 1 and a dispatch field, a hold reason, a file acknowledgement or an event name can never drift between rwb-comms, rwb-integration and WIN without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy loop of RWB-E2-021 crosses four call types in one service boundary: a POST and a GET for the officer, a file out to WIN through the integration service and the proof rows back through rwb-source-data, three Kafka events for the case, the litigation read model and the ledger, and a 16:00 batch window that used to be a Quartz job (legacy section 12; Architecture v5 slides 17, 41, 42 and 44). Each of those is now a contract that another team builds against, so each one has to be fixed before the app story starts: the field names on `notice`, the hold reason values, the event names on the topic, the file name and the acknowledgement, and the Schedule name the operator will look for.

The baseline also fixes the naming that the checks require: schema `rwb_comms`, base `/api/recovery/comms/v1`, topic `rwb.comms.events.v1` with retry and `.dlt` topics, event names `rwb.comms.<Event>.v1`, task queue `rwb-comms` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.comms`. It records that `NoticeDispatched` is event 14 and `NoticeDelivered` is event 15 of the event catalogue on `rwb.comms.events.v1`, that `DecisionRecorded` stays on the shared `rwb.decision-record.v1`, that JOB-10 is an Airflow file window plus the workers of rwb-comms and rwb-integration, and that JOB-11 is the outbox relay (Architecture v5 slides 42 and 44). The two contested points are carried as gaps and assumptions rather than decided quietly: the WIN dispatch file and the acknowledgement have no layout in the sources (INT-14), and the handoff from the Airflow window to the Temporal Schedule has no mechanism.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, the topic and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the CloudEvents 1.0 envelope and the retry and `.dlt` topic convention are the platform baseline (RWB-PLT-EVT, RWB-PLT-TE006-CON); where this document narrows them it does so explicitly.
- The notice generation contract RWB-P6-E1052-CON is published, so the NoticeRequest and the Notice shapes this story extends have one owner document and the added dispatch fields are an additive change to it.
- The proof capture design RWB-P6-E1055-CON is published, so the barcode, the call-back date and the result code map are fixed by the story that designs them and read here.
- The operations and their owners are taken from the Ownership Map only; this document never declares another service's operation as provided. The reference data of rwb-case is owned by P3, the approval of rwb-decision by P7, the contact stops of rwb-deviation by S8, the ledger by P1 and the file runs by P2.
- The owner of the daily reconciliation REC-05 that the legacy story names in its "done when" is not stated in the sources; this baseline therefore names no owner for it and carries the gap (GAP-1090; ASM-2038).
- The WIN dispatch file layout, the acknowledgement record and the proof result record are not stated in the sources; this baseline fixes the names it needs and marks the rest with the placeholder (GAP-1089; ASM-2037).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the additive change to the rwb-comms OpenAPI 3.1 document: the Notice resource with its dispatch and proof fields, the 201 and the 200 answers, the six error responses and the Idempotency-Key on the POST.
2. Fix the dispatch file contract with rwb-integration: the file name and its business date, the record the notice contributes, the acknowledgement the run reads back, and the proof result record of INT-15.
3. Fix the dispatch columns on `notice` (`sent_date`, `barcode`, `sent_type`, `dispatch_file_id`, `dispatch_attempts`) and the three indexes.
4. Fix the hold reason and outcome vocabulary: CONTACT_STOP_X1, LEGAL_HOLD, TEMPLATE_WITHDRAWN, the pending reason, and the Unserved outcomes UNDELIVERABLE, REFUSED and PENDING with the rules R-LIT-08 and R-LIT-09.
5. Record the three published event elements and the three consumed ones with their owner, their key and their payload.
6. Record the workflow element and the Schedule element of the 16:00 run, with the handoff from the Airflow file window.
7. Publish the nine contract tables of section 12 and the six contract fakes.
8. Add the contract tests: schema validation, the additive rule, the vocabulary, the file and acknowledgement shapes, the event validation against the registry, the absence of a cross-schema read, and the drift between a fake and the document.
9. Tag the baseline and hand it to RWB-P6-E2021-APP, RWB-P6-E2021-OPS and the wave 2 harness `RWB-ITG-E2021-ITG`.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | MSG-P3-030 | AC1 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC7 |
| X4 | The dispatch file or the acknowledgement has a layout the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC2 |
| X5 | A consumer cannot deserialise a `rwb.comms` event | The registry validation fails the build; the event is not published | None | AC5 |
| X6 | A retired element reappears in the document, a job or a topic | The absence test fails: no Quartz row, no shared job table, no second topic | None | AC8 |
| X7 | The document declares another service's operation as provided | The review fails the baseline; the operation is described as consumed and faked | None | AC8 |
| X8 | The Airflow window and the Schedule have no agreed handoff | The row carries the placeholder and the fake triggers the Schedule directly | None | AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the two same-service contracts it extends and the Ownership Map only |
| Negotiable | The file columns, the acknowledgement fields and the handoff mechanism are settled with the rwb-integration and WIN owners; the operations, the event names, the topic, the queue and the Schedule are fixed by the target architecture |
| Valuable | Unblocks the app, operations and test stories of this legacy key on Day 1, and the rwb-integration and WIN teams on the same day |
| Estimable | Two documents, one additive change, one file contract, nine contract tables, six fakes and eight contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the letter dispatch loop with proof of delivery

  Background:
    Given the service naming rule of the platform library is in force
    Given the rwb-comms event types are NoticeGenerated, NoticeDispatched and NoticeDelivered
    Given the notice generation contract RWB-P6-E1052-CON is published with the NoticeRequest and Notice shapes

  Scenario: AC1 The two notice operations are declared with the dispatch and proof fields (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-comms is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /cases/{caseId}/notices with the Notice answer of status 201 and GET /notices/{noticeId} with the Notice answer of status 200, both under the base /api/recovery/comms/v1 and owned by rwb-comms
    Then the Notice carries id, caseId, documentId, noticeType, sentDate, barcode, callbackDate, deliveryStatus and sentType beside holdReason, dispatchFileId and dispatchAttempts
    Then the POST declares the Idempotency-Key header and its stored answer, and the GET declares no Idempotency-Key
    Then both operations declare their capability area and right, their 2 s budget and their error responses 401, 403, 404, 409, 422 and 503 with one envelope and one message ID per condition
    Then every added property is optional in the schema, so a consumer of the previous version keeps working

  Scenario: AC2 The dispatch file contract with rwb-integration and WIN is fixed (new, D-RCV-60)
    Given the dispatch file section of the baseline
    When it is compared with the rwb-integration contract and the WIN interface INT-14
    Then it names the file of one business date, its feed, its record for one notice and the acknowledgement record the run reads back
    Then the notice record keys on the notice ID and carries the case ID, the document reference, the template code and version, the language, the notice type and the business date, and no name, address, account number or identity number
    Then the acknowledgement record carries the notice ID, the barcode, the sent date and the sent type, and it is the only source of those three facts on the notice
    Then the proof result of INT-15 is the ProofOfDeliveryRow of the rwb-source-data proof-of-delivery read, of which barcode, deliveryStatus and callbackDate are used, mapped to LOV-DELIVERY by the code map of RWB-P6-E1055-CON
    Then the file name, the file layout, the feed identifier and the acknowledgement field list are Not specified in the source documents (GAP-1089; ASM-2037) and the document marks them so
    Then every call on the file goes through the rwb-integration contract, one hop with a 2 s budget (DP-16, DP-11)

  Scenario: AC3 The dispatch fields on the notice and their indexes are fixed (new, D-RCV-60)
    Given the notice table of schema rwb_comms
    When the dispatch columns are reviewed
    Then sent_date, barcode and sent_type are set only from the acknowledgement record, and callback_date and delivery_status only from the proof result record
    Then dispatch_file_id holds the reference of the outbound item of rwb-integration and never a row of another schema
    Then dispatch_attempts counts the file selections of the notice and is never decremented
    Then the indexes ix_notice_barcode on barcode, ix_notice_sent_date on sent_date and state, and ix_notice_case_id on case_id are declared, and the legacy ix_notice_state_sent is retired in favour of ix_notice_sent_date
    Then the migration is one per-service Flyway step in rwb_comms (DP-15, ADR-021)
    Then no column of the table holds a name, an address, an identity number or an account number

  Scenario: AC4 The hold reason and Unserved vocabulary is closed and cited (new, D-RCV-60)
    Given the hold reason and outcome vocabulary of the baseline
    When it is compared with the rules of the legacy story
    Then the hold reasons are CONTACT_STOP_X1 under R-LIT-05, LEGAL_HOLD under R-UNI-20, TEMPLATE_WITHDRAWN under R-LIT-04 and the pending reason of the proof window under R-LIT-08
    Then the Unserved outcomes are UNDELIVERABLE and REFUSED under R-LIT-09 and PENDING under R-LIT-08, each mapped to LOV-DELIVERY as its owner holds it
    Then a notice with no proof inside the proof window is Unserved with delivery status PENDING and no notice period timer is asked of rwb-case
    Then the notice states of the baseline are Generated, Approved, Sent, Delivered, Unserved and Held, and the NOTICE_PERIOD timer is declared as rwb-case's and not as state of this service
    Then the proof window value and the statutory notice type list are declared as reference data of rwb-case and not as contract constants

  Scenario: AC5 The three published events and the three consumed events are fixed (new, D-RCV-60)
    Given the event section of the baseline
    When it is reviewed against the event catalogue
    Then NoticeDispatched is declared as event 14 and NoticeDelivered as event 15 on rwb.comms.events.v1, keyed by caseId, with no personal data field
    Then DecisionRecorded is declared on the shared rwb.decision-record.v1 through the local decision-record library (DP-03)
    Then DeviationRaised and DeviationCleared on rwb.deviation.events.v1 and CaseStateChanged on rwb.case.events.v1 are declared as consumed, each with its owner and its inbox dedupe
    Then every payload carries IDs, codes, dates and amounts only, and the AsyncAPI fragment validates against the registry with BACKWARD compatibility
    Then the document declares no second topic for this capability and no event on another service's topic
    Then NoticeDispatched and NoticeDelivered declare ce_idempotencykey equal to the ledger business key of the same action
    TC: TC-P6-E2021-CON-05, TC-P6-E2021-CON-10 (Test Cases v9)

  Scenario: AC6 The NoticeDispatchWorkflow run is a Schedule with a named handoff (new, D-RCV-60)
    Given the workflow and Schedule sections of the baseline
    When they are compared with the job map
    Then NoticeDispatchWorkflow is declared on task queue rwb-comms in namespace rwb-recovery with its proof-window step, its conduct check, its file activity and its durable proof timer
    Then the run is a Temporal Schedule at 16:00 with overlap policy SKIP and the catch-up window of the workflow kit, and no Quartz row and no shared job table are declared (DP-10)
    Then the handoff from the bank Airflow WIN file window to the Schedule is declared in one row, and its mechanism is Not specified in the source documents (GAP-1095; ASM-2043)
    Then the daily reconciliation REC-05 is owned by the reconciliation job JOB-04 of rwb-source-data, and the document declares no reconciliation job, series or runbook entry for it (GAP-1090)
    Then the outbox relay is declared as the platform's run and is not a Schedule of this service

  Scenario: AC7 The six contract fakes answer the document (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the event it serves
    Then the rwb-decision approval fake answers the D7.1 answer of RWB-P7-E2014-CON, granted, refused and delayed beyond 2 s
    Then the rwb-case fake answers the case read with legal hold, the scope read and the case facts, including a delayed answer beyond 2 s
    Then the rwb-deviation fake answers no stop, X1 with contact stop on and X2 with contact stop on
    Then the rwb-source-data provider fake 5.1.0 answers the DP02 consent rows, the proof-of-delivery results DELIVERED, REFUSED and UNDELIVERABLE and a no-row answer, and the ledger append with 201, 200, 409, 422 and 503
    Then the rwb-integration WIN fake answers the file of one business date, its acknowledgement with barcode RR223344556TH and sent date 15122026, and a missing acknowledgement
    Then the decision-record library stub answers a healthy chain and a stopped chain
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC8 The nine tables are complete and no cross-schema read or retired element is declared (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the tables named as owned are notice, template, merge_field and the library objects, and recovery_case, task, timer, deviation, decision_log_entry, document, interaction and outbound_item are named as other owners' and consumed only through their contracts
    Then the document declares no read of a v_ace_ view of this service, and the ACE proof rows of the legacy story are declared as the consumed proof-of-delivery read of rwb-source-data
    Then the document declares no Quartz row, no shared job table and no batch table, and the absence test fails a build that adds one

  Scenario: AC14 The file activity retry and timeout are declared and a retried or timed-out activity is covered (new, D-RCV-60)
    Given the NoticeDispatchWorkflow file activity of the baseline
    When its retry policy and activity timeout are compared with the workflow kit
    Then the retry policy and the activity timeout are declared with the values Not specified in the source documents (NEWAC-RWB-P6-E2021-CON-AC14)
    Then every call on the file still goes through the rwb-integration contract, one hop with a 2 s budget (DP-16, DP-11)

  Scenario: AC15 The rwb-source-data rows cite the published contract (new, RD-P1-007)
    Given the consumed element of the baseline
    When it is compared with rwb-source-data.yaml 5.1.0
    Then the ledger row is POST /api/recovery/source-data/v1/cases/{caseId}/interactions with the header Idempotency-Key (a UUID) and InteractionRequest 5.1.0, whose required fields are eventCode, occurredAt, actorType, actorRef, sourceRef and idempotencyKey
    Then the row states that for eventCode "LETTER" conductCheck is required when deliveryStatus is "SENT" or absent, externalRef (at most 60 characters) is required when deliveryStatus is present, and the answers are 201, 200, 400, 401, 403, 404, 409, 422 and 503
    Then the proof row is GET /api/recovery/source-data/v1/proof-of-delivery?businessDate= and the consent row is GET /api/recovery/source-data/v1/data-products/DP02/records?caseId=
    Then each row names contract version 5.1.0 and the provider fake of that version
    TC: TC-P6-E2021-CON-15 (Test Cases v9)
```

These eight criteria are new for the contract baseline and test the artefact only; they restate no business outcome owned by RWB-P6-E2021-APP and they copy no criterion of the legacy story. The wave 2 harness `RWB-ITG-E2021-ITG` consumes this baseline and copies none of these criteria.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/comms/v1`; the document never declares another service's path as provided | DP-13; Architecture v5 slide 41 notes |
| BR2 | Event names are `rwb.<short>.<Event>.v1` on the topic `rwb.<short>.events.v1`, with retry and `.dlt` topics | DP-14; Template and Rules §R4 |
| BR3 | Every event carries the CloudEvents 1.0 envelope, is keyed by caseId and carries no personal data | Architecture v5 slides 42 and 43 notes; DP-09 |
| BR4 | A read declares no Idempotency-Key; a POST declares it and stores its answer | Architecture v5 slide 11; DP-09 |
| BR5 | Error responses use one envelope and one message ID per condition; the business message texts are copied unchanged from the legacy story | Architecture v5 platform baseline; Template and Rules §R7.2 s14 |
| BR6 | A schema change is additive within a major version; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR7 | The document lists only operations owned by rwb-comms; a consumed operation is described as consumed, never as provided | Ownership Map v1 |
| BR8 | The dispatch facts of a notice are its own rows; the file and the acknowledgement are rwb-integration's and WIN's and the proof rows are read from rwb-source-data, all named as consumed; rwb-comms owns the notice and the Schedule; rwb-integration owns the file transport and its retry | DP-01; DP-16; Architecture v5 slide 17; GAP-2106; RD-P1-007 |
| BR9 | The 16:00 run is a Temporal Schedule and a workflow; no Quartz row, no shared job table and no batch table is declared | DP-10; Architecture v5 slide 44 |
| BR10 | No business value is fixed in the contract: the proof window, the statutory notice type list, the eligible states and the result code map stay data or reference data | Template and Rules §R7.2 s17 |
| BR11 | The decision record is the local library's entry on the shared topic, never a new event of this service | DP-03; Architecture v5 slide 42 (event 08) |
| BR12 | The letter body and the addressee are not part of this contract: the file carries a document reference and a barcode | Architecture v5 slides 42 and 43 notes; TSD P6 T3.1 |
| BR13 | The daily reconciliation REC-05 is owned by the reconciliation job of rwb-source-data (JOB-04, Architecture v5 slide 44); this document declares no reconciliation job, series or runbook entry for it | Legacy RWB-E2-021 section 13; GAP-1090 |
| BR14 | ACE data is reached only through the owner's contract or the `v_ace_*` views of the owner; this document declares no view of its own | DP-05; DP-18 |
| BR15 | A delivered notice starts the NOTICE_PERIOD timer in rwb-case from the callback date (NoticeDelivered); an undelivered notice is transferred by a call to rwb-case with reason NOTICE_UNSERVED and starts no timer; this service publishes NoticeDispatched with the delivery status | GAP-1609; Architecture v5 slides 41 and 42 |
| BR16 | Not specified in the source documents (GAP-1095): the handoff from the Airflow WIN file window to the 16:00 run and its rerun rule | GAP-1095 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the file contract, the vocabulary and the event rows are described | In review |
| In review | Consumer sign-off | The app, operations and test stories and the rwb-integration, rwb-decision, rwb-case, rwb-deviation and rwb-source-data owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1, for example a new proof result code | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, or a hold reason value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | Retired element reappears | The absence test of AC8 fails | In review |

The notice state machine that the document describes is the app story's; this baseline fixes its vocabulary and its guards and moves no notice.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-comms | Owns the OpenAPI and AsyncAPI documents and the fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes |
| Consuming teams (app, operations, test, and the rwb-integration, rwb-decision, rwb-case, rwb-deviation, rwb-source-data and rwb-document owners) | Review and sign off the parts they consume |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the naming rule and the outbox relay this document reuses |
| Data steward | Confirms that no personal data field is declared in an event, an answer or the dispatch file |
| rwb-access (DP-08) | Authorises each REST operation of section 12.2 through its authorise check; the check's operation name is Not specified in the source documents (DP-08) |

The per-service login name behind the document's security scheme is not part of this baseline; the document names the scheme "the rwb-comms login (DP-02)".

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Notice resource | The RWB-P6-E1052-CON Notice plus `holdReason`, `dispatchFileId` and `dispatchAttempts`; the existing properties are unchanged | Not specified in the source documents (DOR-RWB-P6-E2021-CON-7) |
| Dispatch fields | `sent_date` DF-LEG-019, `barcode` DF-LEG-020, `sent_type` DF-LEG-023, `dispatch_file_id` DF-LEG-033 and `dispatch_attempts` DF-LEG-034, all on `notice` | Not specified in the source documents (DOR-RWB-P6-E2021-CON-7) |
| Proof fields | `callback_date` DF-LEG-021 and `delivery_status` DF-LEG-022, on `notice`, set only from the proof result record | Not specified in the source documents (DOR-RWB-P6-E2021-CON-7) |
| Hold reason | `hold_reason` DF-LEG-032 with the closed vocabulary of AC4 | Not specified in the source documents (DOR-RWB-P6-E2021-CON-7) |
| File records | The dispatch record, the acknowledgement record and the proof result record of AC2; the field list beyond the IDs and dates named there is Not specified in the source documents (GAP-1089; ASM-2037) | Not specified in the source documents (DOR-RWB-P6-E2021-CON-7) |
| Event payloads | IDs, codes, dates and amounts only; no name, address, identity number or contact point | Not specified in the source documents (DOR-RWB-P6-E2021-CON-7) |
| Rule package | The conduct and consent checks as one versioned rule package governed in rwb-decision and evaluated in this service; the package name is Not specified in the source documents (GAP-1610), and its first version approval is Not specified in the source documents (GAP-1610) | Not specified in the source documents (GAP-1610) |

The field-level types, lengths and required flags of the added properties are settled in the baseline review; this story fixes the names, the optionality rule of AC1 and the vocabulary of AC4.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/notices` | NoticeRequest in, Notice of status 201 out, with the dispatch and proof fields of AC1 | Litigation, right C, scope applied | Idempotency-Key header, answer stored for 24 hours |
| GET | `/notices/{noticeId}` | Notice of status 200 out, with its dispatch and its proof | Litigation, right R, scope applied | Not applicable |

Both operations answer 401, 403, 404, 503 and the POST also answers 409 and 422, each with the error envelope and one message ID of section 14.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | the reference-data read of RWB-P3-E1043-CON | P3 rwb-case | LOV-NOTICE, LOV-DELIVERY, LOV-SENT-TYPE, the statutory notice type list and the proof window, faked (DP-07) |
| POST | the D7.1 demand and recall approval of RWB-P7-E2014-CON | P7 rwb-decision | The approval answer that moves a notice to Approved, faked |
| GET | the case read with legal hold, owner and queue | P3 rwb-case | The conduct check and the scope test, faked. The scope source and the shape of the read are Not specified in the source documents (GAP-1092; ASM-2040) |
| GET | `/api/recovery/deviation/v1/deviations?caseId={caseId}` | S8 rwb-deviation | The open X1 and X2 contact stops of the case, faked |
| POST | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data | `InteractionRequest` 5.1.0 with header `Idempotency-Key` (UUID): eventCode `LETTER`, occurredAt, actorType `SERVICE`, actorRef `rwb-comms`, sourceRef (at most 60), idempotencyKey (at most 120), channel, direction, conductCheck, deliveryStatus, externalRef (at most 60), summary. Dispatch key `LETTER-<caseNo>-<yyyyMMdd of sent date>-<noticeId>` with externalRef the WIN barcode, sourceRef `INT-14 WIN` and conductCheck `PASSED`; held key `LETTER-<caseNo>-<yyyyMMdd>-<notice record uuid>` with conductCheck `BLOCKED` and no externalRef; delivery entry: externalRef the row `barcode`, else its `noticeRef` (a row with neither gets no entry and is logged as unmatched), occurredAt the `callbackDate` at 00:00 Asia/Bangkok, key `LETTER-<caseNo>-<yyyyMMdd of callbackDate>-<u>` with `<u>` the UUID version 5 of `podKey` in the RFC 9562 URL namespace. Answers 201, 200 (repeated business key), 400, 401, 403, 404, 409, 422, 503; 503 MSG-P1-022 leaves the caller's action uncommitted; faked (DP-18; RD-P1-064) |
| GET | `/api/recovery/source-data/v1/data-products/DP02/records?caseId=` | P1 rwb-source-data | The postal contact point and `consentStatus` (GIVEN, WITHDRAWN, UNKNOWN); no address; faked |
| GET | `/api/recovery/source-data/v1/proof-of-delivery?businessDate=` | P1 rwb-source-data | `ProofOfDeliveryAnswer`; writes nothing; 401, 403, 422, 503; read timing Not specified in the source documents (GAP-2096); faked. Read by the rwb-comms workload identity only, which is the one appender of delivery entries (RD-P1-064 rule 6). Pending: the mapping of WIN `delivery_status` to SENT, DELIVERED, READ, FAILED (NEW-GAP-D3; interim: the values of the RWB-P6-E1055-APP fixture) |
| POST | the dispatch file and the acknowledgement read of the rwb-integration contract | P2 rwb-integration | INT-14 out, faked (DP-16). The operation names and the file shapes are Not specified in the source documents (GAP-1089; ASM-2037). The file layout is Not specified in the source documents (GAP-1602); the dispatch is built against a fake of the interface definition |
| POST | the case facts DELIVERY_FAILED, PROOF_WINDOW_EXPIRED and the queue transfer with NOTICE_UNSERVED | P3 rwb-case | The case move and the NOTICE_PERIOD timer, faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream. The `deviations` read path carries the Ownership Map gap of the S8 rows; the ledger and the ACE facts carry the P1 ruling of DP-18 and DP-05.

#### 12.3 Events published

| Event | Topic | Owner | Schema element |
|---|---|---|---|
| `rwb.comms.NoticeDispatched.v1` (event 14) | `rwb.comms.events.v1` | P6 rwb-comms | noticeId, caseId, noticeType, businessDate, dispatchFileId, barcode, sentDate, sentType, conductCheck; published by the app story when the acknowledgement lands |
| `rwb.comms.NoticeDelivered.v1` (event 15) | `rwb.comms.events.v1` | P6 rwb-comms | noticeId, caseId, barcode, result of DELIVERED, REFUSED or UNDELIVERABLE, deliveryStatus, callbackDate; published by the app story for every outcome |
| `rwb.decision.DecisionRecorded.v1` (event 08) | `rwb.decision-record.v1` | P7 rwb-decision | decision record reference, decision code, ruleId, ruleVersion, finalCall, decidedAt; the local decision-record library publishes it (DP-03) |

This story declares the three elements and publishes none itself.

#### 12.4 Events consumed

| Event | Topic | Owner | Consumer contract element |
|---|---|---|---|
| `rwb.deviation.DeviationRaised.v1` (event 06) | `rwb.deviation.events.v1` | S8 rwb-deviation | caseId, deviationCode, contactStop, raisedAt; consumed to hold the notices of the case at the next run |
| `rwb.deviation.DeviationCleared.v1` (event 07) | `rwb.deviation.events.v1` | S8 rwb-deviation | caseId, deviationCode, clearedAt, outcome; consumed to make a held notice eligible again |
| `rwb.case.CaseStateChanged.v1` (event 05) | `rwb.case.events.v1` | P3 rwb-case | caseId, fromState, toState, changedAt; consumed so a closed case is skipped by the run |

The three rows are consumed inside rwb-comms by RWB-P6-E2021-APP; this baseline fixes their shape and their key (caseId).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| NoticeDispatchWorkflow | Workflow, one run per business date; started by a notice request of section 12.2 or by a stage workflow that needs a letter; workflow ID form, signalWithStart and duplicate-start policy Not specified in the source documents (CG-ALL-6560) | `rwb-comms` | The proof-window step, the eligible selection, the conduct check, the file handoff and the durable proof timer |
| conductCheck | Activity | `rwb-comms` | Passed or blocked with the reason and the rule ID |
| generateLetter | Activity, owner rwb-document | `rwb-document` | The letter from the approved template version |
| decisionApproval | Child workflow, owner rwb-decision | `rwb-decision` | The D7.1 approval answer |
| deliverFile | Activity, owner rwb-integration | `rwb-integration` | The WIN dispatch file and its acknowledgement |
| recordDecision | Activity through the library | `rwb-comms` | The local decision record and its outbox row |

No activity is registered by this story; the six rows fix what the app story may assume about the writer and what the operations story must deploy.

#### 12.6 Schedules

| Name | Cron | Overlap policy | Contract element |
|---|---|---|---|
| The JOB-10 notice dispatch run | 16:00 on every business day | SKIP with the catch-up window of the workflow kit | Starts NoticeDispatchWorkflow on task queue `rwb-comms` with the business date |

The handoff from the bank Airflow WIN file window to this Schedule is one row of the document and its mechanism is Not specified in the source documents (GAP-1095; ASM-2043). No Quartz row, no shared job table and no batch table is declared (JOB-05 and TE-007 are retired). The outbox relay JOB-11 belongs to the platform and is not registered here. The daily reconciliation REC-05 has no owner in this baseline (GAP-1090; ASM-2038).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| notice | P6 (rwb_comms) | The notice, its dispatch fields and its proof dates; the table the two operations and the run read and write |
| template | P6 (rwb_comms) | The template version the conduct check reads |
| merge_field | P6 (rwb_comms) | The merge catalogue of the letter; read only by the loop |
| decision record (local) | P6 rows in `rwb_comms`, written through the P7 library | The held and unserved entries (DP-03) |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_comms` | The envelope of the three event rows, the inbox of the three consumed rows and the POST idempotency |

`recovery_case`, `task` and `timer` are P3's, `deviation` is S8's, `decision_log_entry` is P7's, `document` is P5's, `interaction` is P1's, and `outbound_item` and `interface_config` are P2's; the contract names them only as consumed answers (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-decision approval WireMock | The D7.1 answer of RWB-P7-E2014-CON for notice N-0101, granted, refused and delayed beyond 2 s | App story, operations smoke profile, contract tests |
| rwb-case WireMock | The case read with no legal hold and no open deviation, with legal hold true, the scope read with a case of another owner and queue, and no NOTICE_PERIOD timer | App story, operations smoke profile, contract tests |
| rwb-deviation WireMock | No stop, X1 with contact stop on, X2 with contact stop on | App story, operations smoke profile, contract tests |
| rwb-source-data provider fake 5.1.0 (consumed; released by P1, never edited here) | DP02 rows with consentStatus WITHDRAWN; proof rows DELIVERED, REFUSED and UNDELIVERABLE for barcode RR223344556TH and a no-row answer; ledger 201, 200, 409, 422 and 503 | App story, operations smoke profile, contract tests |
| rwb-integration WIN WireMock | The INT-14 file of business date 2026-12-14 and its acknowledgement with barcode RR223344556TH and sent date 15122026, and a missing acknowledgement | App story, operations smoke profile, contract tests |
| decision-record library stub | A healthy chain and outbox, and a stopped chain | App story, contract tests |

The file name, the record layout and the acknowledgement field list of the WIN fake are stubbed from the published document and carry the placeholder until the WIN owner confirms them (GAP-1089; ASM-2037).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 9 consumed | The notice request and read provided; reference data, approval, case read, contact stops, case facts, ledger append, consent read, proof-of-delivery read and the WIN file consumed; one hop, 2 s |
| Kafka | 3 declared as published by their owners, 3 declared as consumed | NoticeDispatched, NoticeDelivered and DecisionRecorded; DeviationRaised, DeviationCleared and CaseStateChanged |
| Temporal | 1 workflow, 3 activities and 1 child workflow, 1 Schedule | NoticeDispatchWorkflow, its three activities, the approval child and the 16:00 Schedule |
| File | 2 | The INT-14 dispatch file out through rwb-integration and the INT-15 proof result in through the rwb-source-data proof-of-delivery read |

### 13. Solution plan

**Deliverables.** The additive change to `openapi/rwb-comms-v1.yaml` for this loop, the dispatch file and acknowledgement schema as a shared component, the AsyncAPI fragment of `rwb.comms.events.v1` naming events 14 and 15, the contract README rows for the vocabulary, the file shapes and the Schedule, and the six WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/comms/v1` | none |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-16 is applied through the rwb-integration contract row of 12.2: the WIN file is never called by this service directly, and the file work of the loop lives in rwb-integration. DP-08 is not in the pattern set of this key: the capability area and the right are declared per operation and enforced at gateway-bff, and the scope read of AC1 carries the gap of GAP-1092.

**Build steps**

1. Add the dispatch and proof properties to the Notice resource and validate the additive rule of AC1 in the pipeline.
2. Write the dispatch file, acknowledgement and proof result schema of AC2 with the placeholder on the fields the sources do not give.
3. Record the five dispatch columns and the three indexes of AC3 in the physical schema note and the Flyway naming.
4. Close the hold reason and outcome vocabulary of AC4 and map each value to its rule and to LOV-DELIVERY.
5. Record the six event rows of AC5 and validate the AsyncAPI fragment against the registry.
6. Record the workflow and Schedule rows of AC6, the Airflow handoff row and the absence test for the retired job, table and second topic.
7. Publish the six fakes and the eight contract tests; a drift between a fake and the document fails the build.
8. Baseline tag and the consumer sign-off note, including the rwb-integration, WIN, rwb-decision, rwb-case, rwb-deviation and rwb-source-data owners and the wave 2 harness.

**Done when.** The OpenAPI and AsyncAPI artefacts validate in the pipeline, the eight contract tests pass, the six fakes answer every consumed path and the drift test is green, and the app, operations and test stories have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-030 | A response body or a query fails schema validation | The request could not be read: {detail}. |
| MSG-GEN-006 | A consumed call does not answer in time | {system} is not available. Try again in a few minutes. |
| MSG-P6-008 | A notice is refused, undeliverable or has no proof in the window | {notice} for case {case} was not served: {reason}. The case is in your queue to choose another service method. |
| MSG-P6-001 | A contact stop blocks the letter | Contact with this customer is stopped for {reason}. |
| MSG-P6-003 | The template was withdrawn before dispatch | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P6-004 | WIN acknowledged the notice | {notice} was sent for registered mail on {date}. |
| MSG-P3-004 | A legal hold or deviation blocks the letter | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-P7-003 | The decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The role lacks the Litigation right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The notice or the case is outside the scope | This case is not in your scope. |
| MSG-GEN-001 | Notice type missing | Enter {field}. |
| MSG-P6-005 | The template of the notice is not approved | Not specified in the source documents (GAP-1096; ASM-2044) |
| MSG-P3-005 | A notice of this type is already in progress for the case | Not specified in the source documents (GAP-1096; ASM-2044) |

The message IDs are contract elements; the text is the agreed text taken from the legacy story where the message already existed, and the `{system}` value of MSG-GEN-006 is fixed by the consumed row that failed. The two texts with the placeholder stand until their owners publish them.

### 15. Screens and states

The contract serves SCR-18 Notice approval in its Generated, Approved, Sent, Delivered, Unserved and Held states, with its empty, loading, error and no access states Not specified in the source documents (CG-ALL-6572); SCR-04 Case timeline for the ledger entry of each dispatch outcome, in its loading state, with its empty, error and no access states Not specified in the source documents (CG-ALL-6571); and SCR-44 Batch and job monitor for the 16:00 run, its file and its rerun, with its empty, loading, error and no access states Not specified in the source documents (CG-ALL-6573), all through the gateway-bff composite route (DP-19). The route calls rwb-comms for the notice, rwb-source-data for the ledger and the run view of the workflow, and rwb-access for the decision; this baseline fixes the rwb-comms answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-021-01 | AC1, BR1 | End to end | N-0101 Approved; acknowledgment RR223344556TH; the contract half answers the dispatch fields of AC3 and the event of AC5 |
| TC-E2-021-03 | AC3, BR6 | End to end | INT-15 UNDELIVERABLE; the contract half answers the Unserved vocabulary of AC4 |
| TC-E2-021-04 | AC4, BR2 | End to end | Open X1 with contact stop; the contract half answers the CONTACT_STOP_X1 hold reason |
| TC-E2-021-06 | AC6, BR7 | End to end | N-0102 sent 2026-12-15 and N-0103 sent 2026-12-16; the NoticeDispatchWorkflow Schedule run on 2026-12-22; the contract half answers the pending reason and the 16:00 Schedule |
| TC-E2-021-09 | AC9, BR9 (run by RWB-P6-E2021-APP) | End to end | Open X2 with stop; decision record stubbed unavailable; the contract half answers the stopped chain of the library stub |
| TC-E2-021-10 | AC10 (run by RWB-P6-E2021-APP) | End to end | POST repeated with one Idempotency-Key; the contract half answers the Idempotency-Key rule of AC1 |
| TC-E2-021-11 | AC11 (run by RWB-P6-E2021-APP) | End to end | N-0200 outside scope; the contract half answers the 404 of AC1 and the scope row of AC2 |
| TC-E2-021-12 | AC12 (run by RWB-P6-E2021-APP) | End to end | POST with no notice type; the contract half answers the 422 of AC1 |
| TC-E2-021-13 | Access | Component | RW-CASEOWN sends POST /cases/{caseId}/notices; refused with MSG-P4-002; the contract half answers the 403 of AC1 |
| TC-E2-021-14 | Principle 5 | NFR | Decision record write forced to fail on 10 unserved results; no notice changes; the contract half answers the stopped chain of AC7 |
| TC-P6-E2021-CON-01 | AC1 | Contract | The document validates; the two operations, the Notice fields, the Idempotency-Key rule and the six error responses are present |
| TC-P6-E2021-CON-02 | AC2, BR5 | Contract | The dispatch, acknowledgement and proof result records validate; the placeholder fields are marked; the file call is one hop; INT-15 DELIVERED, call-back 18122026; the contract half answers the proof record of AC2 and the NoticeDelivered element |
| TC-P6-E2021-CON-03 | AC3 | Contract | The five dispatch columns, the three indexes and the Flyway step; no personal column |
| TC-P6-E2021-CON-04 | AC4 | Contract | The hold reason and outcome vocabulary validated as a closed set with its rules and its LOV mapping |
| TC-P6-E2021-CON-05 | AC5, BR4, BR10 | Contract | The six event rows validate against the registry; no personal data field; the two events on `rwb.comms.events.v1`; Postal consent WITHDRAWN, DEMAND notice; the contract half answers the statutory branch of the consent gate |
| TC-P6-E2021-CON-06 | AC6 | Contract | The workflow rows, the 16:00 Schedule, the Airflow handoff row and the REC-05 gap row present; no Quartz row |
| TC-P6-E2021-CON-07 | AC7, BR3 | Component | The six fakes match the document; a drifted fake fails the build; Legal hold true; the contract half answers the LEGAL_HOLD hold reason |
| TC-P6-E2021-CON-08 | AC8, BR8 | Contract | The nine sub-tables present with owners; no cross-schema read; the absence test for the retired elements; DEMAND-SSME TH v1 withdrawn 2026-12-13; the contract half answers the TEMPLATE_WITHDRAWN hold reason |
| TC-P6-E2021-CON-09 | AC8 | Contract | Boundary test of the nine tables of section 12.7: owner, key and column limits at their edges; no column beyond the contracted list |
| TC-P6-E2021-CON-10 | AC5, BR11 | Contract | The decision record is the library's entry on the shared topic; no event of this service carries it |
| TC-P6-E2021-CON-11 | AC2, BR12 | Contract | The file carries a document reference and a barcode; no letter body or addressee field |
| TC-P6-E2021-CON-12 | AC6, BR13 | Contract | The REC-05 gap row is present and its owner is rwb-source-data JOB-04 and no reconciliation job is declared here |
| TC-P6-E2021-CON-13 | AC8, BR14 | Contract | No ACE table or view is declared; ACE is read only through the owner's contract or the owner's v_ace_* views |
| TC-P6-E2021-CON-14 | AC14 | Contract | A retried and a timed-out file activity; retry count and timeout Not specified in the source documents (NEWAC-RWB-P6-E2021-CON-AC14) |

The fourteen legacy cases keep their legacy order, their legacy level mapping (System to End to end, Access to Component, Resilience to NFR) and their legacy data; the fourteen contract cases test the artefact and are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID.

Version 3: rows that cite `TC-P6-E2021-CON-` identifiers are this story's rows of Recovery Workbench Test Cases v9. Where a shared legacy identifier now names another story's case there, this story's identifier replaces it, and cases run by one identifier are joined in one row.

### 17. Guardrails

- No business value in the contract: the proof window, the statutory notice type list, the eligible states and the result code map stay data, reference data or service configuration.
- No personal data in a schema, an example or a fake: IDs, codes, barcodes, dates and amounts only; the dispatch file carries a document reference and never an addressee.
- The contract names only rwb-comms tables and only operations owned by rwb-comms; the approval, the case read, the contact stops, the ledger and the file are consumed and faked, never declared as provided (DP-01, DP-07, DP-16, DP-18).
- One base, one topic and one queue per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- ACE data is reached only through the owner's contract or the owner's `v_ace_*` views; this document declares no ACE view and no cross-schema join (DP-05).
- No retired element is reintroduced: the absence test of AC8 fails a build that declares a Quartz row, a shared job table, a batch table or a second topic.
- Every example in the document is synthetic; no production payload and no production file is copied into a schema or a fake.
- The error envelope, the CloudEvents envelope and the naming rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-OCC-003 | Letters dispatched for print and post, proof of delivery returns | The two notice operations, the dispatch file and proof result records, and the NoticeDispatched and NoticeDelivered elements | TC-P6-E2021-CON-01, TC-P6-E2021-CON-02, TC-P6-E2021-CON-05 |
| REQ-OCC-005 | Every outbound contact carries a conduct check result | The hold reason and outcome vocabulary, the file record carrying the conduct result and the DecisionRecorded element | TC-P6-E2021-CON-02, TC-P6-E2021-CON-04 |
| REQ-OCC-006 | Withdrawn consent stops the channel; statutory notices continue | The statutory notice type list as reference data and the consent fact of the DP02 records row of 12.2 | TC-P6-E2021-CON-01, TC-P6-E2021-CON-04 |
| REQ-ILG-010 | Dispatch results, including proof of delivery, written to the ledger | The ledger write row of 12.2 and the proof fields of section 11 | TC-P6-E2021-CON-02, TC-P6-E2021-CON-07 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The seven consumed rows with their budget and breaker | TC-P6-E2021-CON-01, TC-P6-E2021-CON-02 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E2-021, disposition Split (rework) |
| Legacy criteria | AC1 to AC12 of the legacy story; AC1, AC2, AC4 and AC5 are owned by RWB-ITG-E2021-ITG and AC3, AC6 to AC12 by RWB-P6-E2021-APP. This baseline copies none of them |
| Test cases | The fourteen legacy cases as the evidence the contract serves, and the fourteen new contract cases TC-P6-E2021-CON-01 to -14 |
| Decoupling patterns | DP01, DP03, DP05, DP07, DP09, DP10, DP11, DP13, DP18, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (Kafka with outbox, inbox and CloudEvents), ADR-016 (reusable Temporal layer, Schedules replace Quartz), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-021 (per-service Flyway and migration ownership) |

### 19. Out of scope

- The implementation of the two operations, the conduct check, the run and the delivery handler (RWB-P6-E2021-APP).
- The deployment, the consumer groups, the dashboards, the alerts and the runbook (RWB-P6-E2021-OPS).
- The generation of a notice and the template catalogue (RWB-P6-E1052-CON and RWB-P6-E1046-CON).
- The proof capture design and its result code map (RWB-P6-E1055-CON); this baseline reads it and restates none of it.
- The SMS and LINE dispatch contract of the same service (RWB-P6-E2022-CON).
- The rwb-integration, WIN, rwb-decision, rwb-case, rwb-deviation and rwb-source-data contracts themselves: consumed and faked, never defined here.
- The gateway-bff composite route and the screen field list (RWB-PLT-N001-CON).
- The cross-service journey harness and its evidence (`RWB-ITG-E2021-ITG`).
- The daily reconciliation REC-05 and its mechanism, which no source assigns (GAP-1090).

### 20. Remaining delivery steps

- Size and epic design sign-off: Not specified / Pending. Owner: squad and solution architect.
- rwb-source-data provider fake 5.1.0 in the contract fake library: Pending. Owner: P1 contract owner.
- rwb-comms OpenAPI and AsyncAPI fragments, own fakes and baseline tag (CON Done): Pending. Owner: rwb-comms contract owner.
- Settle GAP-2096, NEW-GAP-F14-9 and NEW-GAP-D3: Pending. Owner: solution architect and contract owners.
- Test case rows in Test Cases v9: Pending. Owner: QA.
