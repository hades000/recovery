# RWB-P6-E1055-CON Proof of delivery capture design with WIN

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E1055-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-055 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP05, DP07, DP09, DP10, DP11, DP15, DP18, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (FR-P6-013, FR-P6-015, FR-P6-016, FR-P6-017, FR-P6-018, FR-P6-019, FR-P6-020, FR-P6-021, FR-P6-023) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-055 for rwb-comms (CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the proof-of-delivery loop of rwb-comms — `GET /api/recovery/comms/v1/notices/{noticeId}` with its dispatch and proof-of-delivery fields, the internal digest write, the INT-14 and INT-15 file elements (record layout, feed version, business date and batch status), the LOV-DELIVERY and LOV-SENT-TYPE contract elements, the idempotent digest of a repeated proof-of-delivery row, the `rwb.comms.NoticeDispatched.v1` and `rwb.comms.NoticeDelivered.v1` envelopes, the `outbound_item` reference of `dispatch_file_id`, the four consumed contracts and the four fakes**, so that **the app, infrastructure, deployment and test stories of this legacy key build against a fixed, testable contract on Day 1 and a field named differently in the P1, P3 or P5 contract can never empty a notice panel or a delivery fact at run time without failing a build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The capability of RWB-E1-055 reads one notice and one proof of delivery, and it writes two facts that other services act on: the dispatch, which rwb-reporting consumes, and the delivery, which rwb-case turns into a `NOTICE_PERIOD` timer and rwb-litigation and rwb-guarantee read (Architecture v5 slide 42, events 14 and 15). Both are composed from answers that are no longer local: the proof-of-delivery row and the freshness stamp come from rwb-source-data, the letter behind the notice comes from rwb-document, the timer is rwb-case's, and the file item is rwb-integration's. A field renamed on any of those four edges is exactly the failure that no single-service suite sees.

The baseline also fixes the naming the checks require: schema `rwb_comms`, REST base `/api/recovery/comms/v1`, topic `rwb.comms.events.v1`, event names `rwb.comms.<Event>.v1`, task queue `rwb-comms` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.comms`. It records that JOB-10 is the bank Airflow file window plus the dispatch Schedule and workers of this service (Architecture v5 slide 44), so no contract in this story declares a Quartz row, a shared job table or a Control-M job.

This document is the rwb-comms contract slice of legacy RWB-E1-055 and it owns no legacy acceptance criterion; the criteria of the key are owned by RWB-P6-E1055-APP (AC2 to AC8 and AC10 to AC11) and by `RWB-ITG-E1055-ITG` (AC1 and AC9). It restates no business outcome and makes no runtime claim: it fixes shapes, envelopes, list values and fakes.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the topic, event, queue and package names follow the platform rule rather than a local choice.
- The platform error envelope, the CloudEvents 1.0 envelope and the retry and `.dlt` topic convention are the platform baseline (RWB-PLT-EVT, RWB-PLT-TE006-CON); where this document narrows them it does so explicitly.
- RWB-P6-E1055-APP and RWB-P6-E1052-APP define the fields the baseline declares; this document fixes their shape and never their computation.
- RWB-P1-E1066-CON, RWB-P3-E1043-CON, RWB-P3-E1028-CON and RWB-P5-E1054-CON are the consumed contracts of section 12.2. The exact element names behind RWB-P1-E1066-CON and RWB-P5-E1054-CON are not in the source documents (GAP-1097; ASM-2045; GAP-1099; ASM-2047).
- The fixed layouts and the transport of INT-14 and INT-15 are the WIN owner's documents, which are not in the source material (GAP-1100; ASM-2048).
- The operations and their owners are taken from the Ownership Map only; this document never declares another service's operation as provided.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the rwb-comms OpenAPI 3.1 document fragment for `GET /notices/{noticeId}` and the internal digest write, and the AsyncAPI fragment for the two `rwb.comms.events.v1` events.
2. Fix the notice shape: the identity, the two dates of the dispatch, the barcode, the two list values, the callback date, the dispatch file reference, the attempts and the hold reason, with the optionality rule of AC1.
3. Fix the file contract element: the INT-14 record set and its trailer, the feed version, the business date and the batch status the read is gated on, and record that the fixed layout is the WIN owner's (AC2).
4. Fix the delivery list: LOV-DELIVERY and LOV-SENT-TYPE as versioned reference data, with the state that each value drives, and no literal value in the document's examples beyond the ones the sources name (AC3).
5. Fix the idempotent digest of a repeated proof-of-delivery row: the key, the answer and the counter (AC4).
6. Fix the two event envelopes and their key, with the no-personal-data rule (AC5).
7. Fix the `dispatch_file_id` reference to `outbound_item` of rwb-integration, its cardinality and the fact that it is an identifier and not a foreign key (AC6).
8. Fix the four consumed rows with their owner, the 2 s budget and the degraded shape, and the four fakes with documented answers (AC7, AC8).
9. Tag the baseline and hand it to RWB-P6-E1055-APP, RWB-P6-E1055-INF, RWB-P6-E1055-OPS and RWB-ITG-E1055-ITG.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | None | AC1 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A list value is written into the document as an enumeration instead of a versioned reference | The list test fails the build | None | AC3 |
| X4 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC7 |
| X5 | The consumed row of P1 or P5 names no element the sources fix | The row carries the placeholder, its gap and its assumption, and the fake is derived from the owner's published document | None | AC8 |
| X6 | The WIN fixed layout is not available | The INT-14 element is declared as a shape only, with the gap and the assumption, and no field order is invented | None | AC2 |
| X7 | An event carries a personal field or loses its key | The envelope test fails the build | None | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the four consumed contracts and the Ownership Map only |
| Negotiable | Field-level detail is settled with the consumers; the two events, the two list values and the four consumed rows are fixed by the target architecture |
| Valuable | Unblocks the app, infrastructure, deployment and test stories on Day 1 and every consumer of the two dispatch facts |
| Estimable | Two documents, eight contract tests, four consumed rows and four fakes |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion tests the artefact, not a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the proof-of-delivery loop of rwb-comms

  Background:
    Given the service naming rule of the platform library is in force
    Given the base path of rwb-comms is /api/recovery/comms/v1 and its topic is rwb.comms.events.v1

  Scenario: AC1 The notice read declares the dispatch and proof-of-delivery fields (new, D-RCV-60)
    Given the OpenAPI 3.1 fragment of GET /notices/{noticeId} is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error and is owned by rwb-comms on base /api/recovery/comms/v1
    Then the Notice resource carries noticeId, caseId, noticeType, state, sentDate, barcode, sentType, callbackDate, deliveryStatus, dispatchFileId, dispatchAttempts, holdReason and templateVersion
    Then sentDate, barcode, sentType, callbackDate and deliveryStatus are optional, so a notice that is not yet dispatched is a valid answer
    Then the operation names its Litigation R right, its 2 s budget and its error responses 401, 403, 404 and 503, and takes no Idempotency-Key
    Then the internal digest write POST /internal/pod-digests declares the Idempotency-Key header as required and the service identity as its only caller
    Then no answer field carries a name, an address, an identity number or a contact value

  Scenario: AC2 The INT-14 file element fixes the record set, the feed version, the business date and the batch status (new, D-RCV-60)
    Given the file element of the document
    When it is reviewed against the legacy job description and the ACE batch record
    Then the INT-14 element names one record per notice with the contract number of the case's primary account, the addressee, the address, the notice type, the template version and the document reference, and a trailer with the record count
    Then it names the business date, the file ID, the feed version and the attempt number of the file
    Then it names the INT-15 side as barcode, sent date, callback date, delivery status and sent type, read only when the batch status of source WIN is COMPLETE for the business date
    Then the fixed field order, the lengths, the delimiters, the encoding and the transport are Not specified in the source documents (GAP-1100; ASM-2048)
    Then the document states that the layout is the WIN owner's and that a change of layout is a new file version, never an edit in place

  Scenario: AC3 LOV-DELIVERY and LOV-SENT-TYPE are the only delivery list elements (new, D-RCV-60)
    Given the list element of the document
    When it is compared with the TSD P6 list of values and the reference-data contract
    Then LOV-DELIVERY is DELIVERED, REFUSED, UNDELIVERABLE and PENDING, and no other value is valid on deliveryStatus
    Then LOV-SENT-TYPE is BEFORE_NPL and NPL, and no other value is valid on sentType
    Then both lists are read with their version through the rwb-case reference-data contract and are never enumerated in a schema
    Then the document states which notice state each delivery value leads to, and that the queue transfer on a refusal is RWB-E2-021 and not this service
    Then the hold reason list is carried as a reference element with TEMPLATE_WITHDRAWN as its only named value (GAP-1105; ASM-2053)

  Scenario: AC4 The digest of a repeated proof-of-delivery row is idempotent (new, D-RCV-60)
    Given the internal digest element of the document
    When the same business date, feed version and digest are posted twice with the same Idempotency-Key
    Then the second call returns the first answer with status 200 and writes no second row
    Then the document states the digest key as the business date with the feed version and the digest of the batch
    Then the document states that a second delivery for the same barcode and callback date changes no notice, writes no second NoticeDelivered and is counted under R-UNI-40
    Then the document names the counter and the collection that holds it, without a personal field

  Scenario: AC5 The two event envelopes carry IDs and facts only (new, D-RCV-60)
    Given the AsyncAPI fragment of rwb.comms.events.v1
    When the two events are validated against the CloudEvents 1.0 envelope and the registry
    Then rwb.comms.NoticeDispatched.v1 declares noticeId, caseId, sentDate, barcode and sentType, keyed by caseId
    Then rwb.comms.NoticeDelivered.v1 declares noticeId, caseId, deliveredDate, callbackDate and deliveryStatus, keyed by caseId
    Then neither payload declares a name, an address, an identity number or a contact value
    Then each has its retry topic and its .dlt topic and is versioned with BACKWARD compatibility
    Then the document states that each is written to the outbox in the same transaction as the notice change

  Scenario: AC6 dispatch_file_id is a reference to outbound_item of rwb-integration (new, D-RCV-60)
    Given the data element of the document
    When the dispatch file reference is reviewed
    Then dispatchFileId is declared as an identifier of the outbound item of rwb-integration, many to 0 or 1 from the notice
    Then the document states that it is stored as an identifier and never as a foreign key across schemas, and that the file itself is read through the owner's contract
    Then dispatchAttempts is declared as an integer with a default of 0 and is incremented once per file the notice enters
    Then the document names no path of rwb-integration as provided by this service

  Scenario: AC7 The four consumed rows carry their owner, the budget and the degraded shape (new, D-RCV-60)
    Given the consumed element of the document
    When it is compared with the Ownership Map
    Then the DP07 records read and the freshness read name P1 rwb-source-data and the ledger write names P1 rwb-source-data
    Then the stored letter read names P5 rwb-document, the timer read names P3 rwb-case and the list read names P3 rwb-case
    Then every row states one hop, the 2 s timeout, one GET retry with jitter and a breaker per downstream
    Then the document states the degraded shape of a failed pod read, a failed freshness read and a failed document read, and that a failed pod read never sets a notice Delivered
    Then the pod and document elements carry their gap and assumption where no source names them (GAP-1097; GAP-1099)

  Scenario: AC8 The four fakes answer the document and the drift test fails the build (new, D-RCV-60)
    Given the fakes of section 12.8
    When each one is compared with the shapes of 12.1 to 12.4
    Then the rwb-source-data fake answers 25 of 25 records with 0 refused, the 30-row batch with one held row, the repeat row, the three batch states and the stale marker
    Then the rwb-document fake answers one stored letter per notice, the rwb-case fake answers a running NOTICE_PERIOD timer started on 2026-11-28, and the rwb-integration fake answers one outbound item and the acknowledgment record
    Then every fake value is the legacy value of RWB-E1-055 and no business value is added
    Then a fake that drifts from the document fails the build
```

These eight criteria are new for the contract baseline and test the artefact only. The legacy criteria of RWB-E1-055 are owned by RWB-P6-E1055-APP (AC2 to AC8 and AC10 to AC11) and by RWB-ITG-E1055-ITG (AC1 and AC9), and none of them is restated here.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/comms/v1`; the document never declares another service's path as provided | DP-13; Architecture v5 slide 41 notes |
| BR2 | Event names are `rwb.<short>.<Event>.v1` on `rwb.<short>.events.v1`, with retry and `.dlt` topics | DP-14; Template and Rules §R4 |
| BR3 | Every event carries the CloudEvents 1.0 envelope, is keyed by caseId and carries no personal data | Architecture v5 slides 42 and 43 notes; DP-09 |
| BR4 | A read declares no Idempotency-Key; a POST declares it, stores its response and returns the first answer on a repeat | Architecture v5 slide 11; DP-09 |
| BR5 | Error responses use one envelope and one message ID per condition, and the business message texts are copied unchanged from the legacy story | Template and Rules §R7.2 s14 |
| BR6 | A schema change is additive within a major version; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR7 | The document lists only operations owned by rwb-comms; a consumed operation is described as consumed, never as provided | Ownership Map v1 |
| BR8 | The list values are versioned reference data, read through the rwb-case contract, and are never an enumeration in a schema or a constant in code | DP-07; TSD P6 T3.2 |
| BR9 | The proof of delivery is read by rwb-source-data, not by this service: the contract declares a consumed answer and no `v_ace_*` view | DP-05; legacy BR4 |
| BR10 | The notice period is started by rwb-case from the delivered date on the event, and no contract element of this story declares a timer | R-LIT-07; DP-09 |
| R-LIT-07 | A notice period starts only from the delivery date, so the event carries the delivered date and the callback date beside it | Temporal and Drools design slide 20 notes; legacy BR2 |
| R-LIT-08 | The proof window is 7 days from dispatch and belongs to RWB-E2-021; this baseline declares no window field | Temporal and Drools design slide 20 notes; RWB-E2-021 |
| R-LIT-09 | An undeliverable result moves the notice to Unserved in RWB-E2-021; this baseline only fixes the list value that carries it | FSD P6 A2.2 AC-ALT-P6-002-02 |
| R-UNI-33 | A downstream system that fails is retried, and the record state does not advance until the retry succeeds | INT-14 error handling |
| R-UNI-34 | A retried call that passes its limit leaves the record in the exception queue with its reason | INT-14 error handling |
| R-UNI-40 | The same event, the same digest and the same proof-of-delivery row produce one effect, and the repeat is counted | legacy BR6; FSD P6 A2.2 AC7 |

### 9. State transitions

The baseline declares the notice states as contract elements; it writes none of them.

| From | Event | Condition | To |
|---|---|---|---|
| Generated | The file of the business date holds the notice | The notice is in the dispatch-eligible state and has no sent date | Generated, with the file reference and the attempt count |
| Generated | `rwb.comms.NoticeDispatched.v1` content | A barcode is present in the acknowledgment | Sent |
| Sent | `rwb.comms.NoticeDelivered.v1` content | A callback date is present on the row | Delivered |
| Sent | A delivery value of REFUSED or UNDELIVERABLE | The row carries that value | Unserved; the queue transfer is RWB-E2-021 |
| Generated or Sent | A hold | The holding condition applies | Held, with the hold reason |
| Held | The hold is released | The condition is cleared | The previous state, and the notice is eligible again |

The lifecycle column and the four delivery values are declared here so a consumer never invents a state. The `NOTICE_PERIOD` timer is rwb-case's state: the `rwb.comms.NoticeDelivered.v1` envelope carries the delivered date, and rwb-case starts the timer from it. No contract element of this story declares a timer, a case status or a queue.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-comms | Owns the OpenAPI and AsyncAPI fragments and the fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version and the correction of a consumed ownership row |
| Consuming teams (app, infrastructure, deployment, test and the P1, P3 and P5 owners) | Review and sign off the parts they consume |
| Platform library owner | Owns the CloudEvents envelope, the error envelope and the naming rule this document reuses |
| Data steward | Confirms that no personal field is declared in an answer or an event |

The rights of the capability itself are the rows of TSD P6 T6.1 — RW-LITOFF Litigation CRUA, RW-LEGAL Litigation RA, RW-CASEOWN Documents CRU and Litigation R, RW-PLATADM Documents R — and they are declared on the operations by name only. DP-08 is not in the patterns of this story: the operation declares its capability area and right, and the enforcement point of the declared right is gateway-bff; where a local guard is required the guard is not specified in the source documents (GAP-1098; ASM-2046). The per-service login name behind the security scheme is not part of this baseline; the document names the scheme "the rwb-comms login (DP-02)".

### 11. Data

The baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Notice resource | `noticeId`, `caseId`, `noticeType`, `state`, `sentDate`, `barcode`, `sentType`, `callbackDate`, `deliveryStatus`, `dispatchFileId`, `dispatchAttempts`, `holdReason`, `templateVersion`, from DF-LEG-015 to DF-LEG-023, DF-LEG-032 to DF-LEG-034 and DF-REF-047 |
| Dispatch and proof dates | `sentDate` and `callbackDate` are dates in the ISO form on the wire and DDMMYYYY in the WIN file only; the conversion is the app story's |
| File element | The INT-14 record set and trailer, the business date, the file ID, the feed version and the attempt number; the INT-15 read fields |
| List elements | LOV-DELIVERY and LOV-SENT-TYPE with their version, and the hold reason reference element |
| Event payloads | IDs, dates, a barcode and list values only; no name, address, identity number or contact value |
| Reference | `dispatchFileId` is an identifier of `outbound_item` in `rwb_integration`, many to 0 or 1; no foreign key crosses the schema boundary |

The field-level types, lengths and required flags of the added properties are settled in the baseline review; this story fixes the names, the optionality rule of AC1 and the list rule of AC3.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| GET | `/notices/{noticeId}` | The Notice resource of AC1 with the dispatch and proof fields, all optional except the identity, the case, the notice type and the state | Litigation R, scope applied |
| POST | `/internal/pod-digests` | The business date, the feed version, the row count and the digest of the batch; the answer is the digest record; Idempotency-Key required, service identity only | Service identity |

Both answer with the platform error envelope; the read answers 401, 403, 404 and 503, the internal write answers 401, 409, 422 and 503.

#### 12.2 REST operations consumed

| Method | Path | Owner | Shape the baseline fixes |
|---|---|---|---|
| GET | `/api/recovery/source-data/v1/data-products/DP07/records` | P1 rwb-source-data (RWB-P1-E1066-CON) | The proof-of-delivery records of a business date, with the fields of DF-ACE-253 to DF-ACE-258; the element names are not in the source documents (GAP-1097) |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data (RWB-P1-E1066-CON) | The batch status of source WIN, the feed version and the stale marker |
| POST | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data (DP-18) | The outbound LETTER entry; ids, dates, direction, channel and a summary with no personal field |
| GET | `/api/recovery/document/v1/documents/{documentId}` | P5 rwb-document (RWB-P5-E1054-CON) | The stored letter of a notice; the element is not named in the source documents (GAP-1099) |
| GET | `/api/recovery/case/v1/cases/{caseId}/timers` | P3 rwb-case (RWB-P3-E1028-CON) | The `NOTICE_PERIOD` timer, observed only to assert the start date |
| The LOV read of the reference-data contract | P3 rwb-case (RWB-P3-E1043-CON) | LOV-NOTICE, LOV-DELIVERY, LOV-SENT-TYPE and the hold reason reference, by version |

Every row is one hop with a 2 s timeout, one GET retry with jitter and a breaker per downstream. The baseline fixes the shapes and the failure mapping only; it makes no runtime claim.

#### 12.3 Events published

| Event | Topic | Schema element |
|---|---|---|
| `rwb.comms.NoticeDispatched.v1` (event 14) | `rwb.comms.events.v1` | noticeId, caseId, sentDate, barcode, sentType; key caseId; no personal field |
| `rwb.comms.NoticeDelivered.v1` (event 15) | `rwb.comms.events.v1` | noticeId, caseId, deliveredDate, callbackDate, deliveryStatus; key caseId; no personal field |

Both are declared here and published by RWB-P6-E1055-APP; this baseline writes neither. `rwb.decision-record.DecisionRecorded.v1` on the shared `rwb.decision-record.v1` is declared as a dependency of the capability where a rule decides, and the envelope belongs to the platform library (DP-03, DP-09).

#### 12.4 Events consumed

| Event | Topic | Owner | Contract element |
|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` (event 05) | `rwb.case.events.v1` | P3 rwb-case | caseId, from state, to state; holds the pending notices of a case that leaves a dispatchable state |
| `rwb.deviation.DeviationRaised.v1` (event 06) | `rwb.deviation.events.v1` | S8 rwb-deviation | caseId, deviation code, raised at, contact stop; holds the notices |
| `rwb.deviation.DeviationCleared.v1` (event 07) | `rwb.deviation.events.v1` | S8 rwb-deviation | caseId, deviation code, cleared at, outcome; releases the hold |

The three are declared as consumed by the capability; this baseline subscribes to none of them and fixes only their key and their contract element.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `NoticeDispatchWorkflow` | Workflow from the kit template, one per business date and dispatch run | `rwb-comms` | The dispatch run and the two events; the workflow declares its input as the business date and the eligible notice IDs only |
| `generateLetter` | Activity, P6 | `rwb-comms` | The document ID of each eligible notice, resolved through the document contract |
| `approveNotice` | Child workflow in rwb-decision | `rwb-decision` | The approval outcome where a rule decides, recorded before any state change |
| `deliverFile` | Activity, P2 | `rwb-integration` | The file ID, the business date and the `FileDelivered` or `FileFailed` fact |

No activity is registered by this story; the four rows fix what the app story may assume and what the deployment story must have on each queue.

#### 12.6 Schedules

One element, declared and not registered here.

| Schedule | Cron | Overlap | What it starts |
|---|---|---|---|
| The dispatch Schedule of rwb-comms (RWB-PLT-E1071-CON) | 16:00 Asia/Bangkok | SKIP, with the catch-up window of the kit | `NoticeDispatchWorkflow` for the business date |

The cross-system edge of JOB-10 is the bank Airflow file window (Architecture v5 slide 44). This baseline declares no Quartz row, no shared job table entry and no Control-M job, and the deployment story registers the Schedule.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| notice | P6 (rwb_comms) | The notice and its dispatch and proof-of-delivery fields |
| template | P6 (rwb_comms) | `template_version`, the version the letter was generated from |
| merge_field | P6 (rwb_comms) | The merge codes of the catalog, read only |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_comms` | The envelope of the two events, the inbox of the three consumed events and the key of the internal digest write |

`document` and `signature_request` are P5's, `interaction` is P1's, `recovery_case`, `timer` and `case_account` are P3's, `decision_log_entry` is P7's and `outbound_item` is P2's; the contract names them only as consumed answers (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data pod batch fake | 25 of 25 records with 0 refused and feed version `WIN-POD-SAMPLE-v1`; the 30-row batch of 2026-11-30 with 29 matchable rows and one held row with check `References`; the second record of 2026-11-28 for `RR123456789TH`; batch states COMPLETE, FAILED at the record count check and not COMPLETE; the stale marker with MSG-P1-001 naming "DP07 Legal" and 2026-11-23 | App story, deployment smoke profile, contract tests |
| rwb-document PDF fake | One stored letter per notice of the fixture set, answered behind the document ID; a delayed answer beyond 2 s | App story, contract tests |
| rwb-case timer and reference fake | A running `NOTICE_PERIOD` timer on `RC-2026-000123` started on 2026-11-28 and none on 2026-11-26; LOV-NOTICE, LOV-DELIVERY, LOV-SENT-TYPE and the hold reason list at their version | App story, contract tests |
| rwb-integration WIN file fake | One `outbound_item` for the file of 2026-11-25 in state ACKNOWLEDGED, one unacknowledged file per run from 2026-11-26 to 2026-11-28, and the acknowledgment record with sent date 26112026, barcode `RR123456789TH` and sent type `NPL` for contract `CT-77001` | App story, deployment smoke profile, contract tests |

No real WIN connection is opened and no production payload is copied into a fake.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 6 consumed | The notice read and the internal digest write; DP07 records, freshness, ledger, document, timers and the list read; one hop and 2 s |
| Kafka | 2 declared as published by the app story, 3 declared as consumed | NoticeDispatched and NoticeDelivered; CaseStateChanged, DeviationRaised and DeviationCleared |
| Temporal | 1 workflow, 3 activities, 1 Schedule declared | `NoticeDispatchWorkflow` with `generateLetter`, the decision child and `deliverFile`; the Schedule is registered by the deployment story |
| File | 1 | The INT-14 outbound file and its trailer; the INT-15 side is declared as the read fields only, and no file content enters a message or a workflow input |

### 13. Solution plan

**Deliverables.** The additive fragment of `openapi/rwb-comms-v1.yaml` with the Notice resource and the internal digest write, the AsyncAPI fragment of `rwb.comms.events.v1` with the two events, the contract README rows for the file element, the two lists, the digest and the consumed rows, and the four WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H rows of the table are delivered by the platform waves and are not repeated in the metadata H field of this story, which stays empty by rule (Template and Rules §R5.7). DP-05 applies as a prohibition and DP-18 as "the ledger is a consumed operation of rwb-source-data".

**Build steps**

1. Add the Notice resource and the internal digest write; validate the optionality rule of AC1 and the additive rule of BR6 in the pipeline.
2. Write the file element of AC2, with the gap and the assumption where the fixed layout is the WIN owner's.
3. Write the list element of AC3 and the state that each delivery value leads to.
4. Write the digest element of AC4 and the repeat counter.
5. Write the two event envelopes of AC5 and the no-personal-data check.
6. Record the `dispatchFileId` reference and its cardinality (AC6).
7. Record the six consumed rows with their owner, the budget and the degraded shape, with the two gap rows where no source names the element (AC7).
8. Publish the four fakes and the eight contract tests; a drift between a fake and the document fails the build (AC8).
9. Baseline tag and the consumer sign-off note, including the P1, P3, P5 and P2 owners and the wave 1 harness.

**Done when.** The OpenAPI and AsyncAPI fragments validate in the pipeline, the eight contract tests pass, the four fakes answer every consumed path and the drift test is green, and the app, infrastructure, deployment and test stories have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-004 | A notice is acknowledged by WIN | {notice} was sent for registered mail on {date}. |
| MSG-GEN-006 | WIN has not acknowledged after the third attempt | {system} is not available. Your request is queued and will be retried. |
| MSG-P1-001 | The WIN batch is late or not COMPLETE | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | A role without the Litigation right reads the notice | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written where a rule decided | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message IDs are contract elements and the texts are the legacy wording of RWB-E1-055, copied unchanged. {date} in MSG-P6-004 is the sent date of the acknowledgment and {product} in MSG-P1-001 is the data product name the freshness answer carries; the {system} value of MSG-GEN-006 is fixed by the consumed row that failed.

### 15. Screens and states

No screen is built in this story. The baseline serves SCR-03 Case record, SCR-30 Case documents, SCR-44 Interface and job monitor and SCR-45 Data quality through the gateway-bff composite route (DP-19): SCR-03 shows the notice state, the sent date, the barcode, the callback date and the delivery status from this answer, and SCR-44 and SCR-45 show the run and the break that this baseline names. The composite route specification, the screen field list and the masking of customer fields belong to RWB-PLT-N001-CON and the edge stories.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-055-01 | AC1, BR1 | End to end | N-0001 Generated; acknowledgment with RR123456789TH |
| TC-E1-055-02 | AC2, BR2 | End to end | v_ace_pod row for 2026-11-30 with RR123456789TH, callback_date 2026-11-28 |
| TC-E1-055-03 | AC3 | End to end | WIN owner sample WIN-POD-SAMPLE-v1, 25 records ingested by ACE |
| TC-E1-055-04 | AC4, BR3 | End to end | No acknowledgment on three runs |
| TC-E1-055-05 | AC5, BR4 | End to end | ACE batch for WIN FAILED at its record count |
| TC-E1-055-06 | AC6, BR4 | End to end | 30 rows, 1 unknown |
| TC-E1-055-07 | AC7 | End to end | v_ace_pod rows of 2026-11-30 read twice |
| TC-E1-055-08 | AC8 | End to end | JOB-10 rerun on 2026-11-25 |
| TC-E1-055-09 | AC9, BR5 | End to end | N-0002 with no barcode on 2026-11-28 |
| TC-E1-055-10 | AC10, BR6 | End to end | Repeat of RR123456789TH on 2026-12-07 |
| TC-E1-055-11 | AC11, BR7 | End to end | No COMPLETE WIN batch for 2026-11-30 |
| TC-E1-055-12 | Access | Component | RW-PHONECOL reads the notice dispatch detail; refused with MSG-P4-002 |

The twelve are the legacy test cases of RWB-E1-055 in their legacy order, with the Level column added; System maps to End to end and Access to Component. The contract tests of this baseline are named in section 13 and are not legacy test case IDs; they run in the pipeline against the four fakes and the documents.

### 17. Guardrails

- No business value in the contract: the eligible state, the attempt limit, the break days, the stale period, the hold reasons and the retry intervals stay data, reference data or service configuration.
- No personal data in a schema, an example or a fake: IDs, codes, dates, a barcode and list values only; no name, address, identity number or contact value.
- The contract names only rwb-comms tables and only operations owned by rwb-comms; the P1, P3 and P5 operations are consumed and faked, never declared as provided (DP-01).
- ACE data is reached only through the owner's contract or the owner's `v_ace_*` views; this document declares no ACE view and no cross-schema join (DP-05).
- One REST base and one topic per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- Every event is keyed by case ID, carries the CloudEvents envelope and no personal field, and its repeat is deduped through the inbox (DP-09, R-UNI-40).
- No timer, no case status and no queue element is declared: the notice period is started by rwb-case from the event (BR10).
- Every example in the document is synthetic; no production payload is copied into a schema or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-OCC-003 | Letters dispatched for print and post, proof of delivery returns to the case | The Notice resource, the file element, the two lists and the two events | TC-E1-055-01 to TC-E1-055-11 |
| REQ-ILG-004 | What happens in an interaction is recorded against that interaction | The ledger row of 12.2 and the idempotent digest of AC4 | TC-E1-055-02, TC-E1-055-12 |
| REQ-DRI-006 | No direct call to a system of record; ACE data through the owner's contract and files only through rwb-integration | The consumed rows of 12.2 and the `dispatchFileId` reference of AC6 | TC-E1-055-03, TC-E1-055-05 to TC-E1-055-07 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The six consumed rows with their budget and breaker | TC-E1-055-03, TC-E1-055-05 |
| ADR-021 | Per-service Flyway and migration ownership | The `rwb_comms` tables of 12.7 and the dispatch columns they carry | TC-E1-055-04, TC-E1-055-08 |

| Item | What it covers in this story |
|---|---|
| Legacy key RWB-E1-055 | The contract baseline of the dispatch and proof-of-delivery loop; no legacy AC is owned here |
| DP-01 | Only `rwb_comms` tables are owned; the letter, ledger, timer and file item are consumed |
| DP-05 | The pod and the batch status are a consumed answer of rwb-source-data, and no ACE view is declared |
| DP-07 | The three lists and the hold reasons are versioned reference data |
| DP-09 | The two events and the three consumed events, with the envelope and the inbox rule |
| DP-10 | The dispatch Schedule and the workflow replace the Quartz job |
| DP-11 | Six consumed rows, one hop and 2 s each |
| DP-15 | The service's own Flyway sequence carries the dispatch columns |
| DP-18 | The ledger entry is a consumed operation of rwb-source-data |
| DP-19 | The four screens are reached through the composite route |
| ADR-013, ADR-014, ADR-015, ADR-016 | 19 services, a schema and login per service, Kafka with outbox and inbox, and a reusable Temporal layer |
| ADR-020, ADR-021 | One hop and 2 s; per-service migration ownership |

### 19. Out of scope

- The implementation of the two operations, the workflow, the pod read and the reconciliation: RWB-P6-E1055-APP.
- The legacy criteria AC1 and AC9, and the end-to-end proof of the loop: RWB-ITG-E1055-ITG.
- The network, certificates, storage and scaling of the WIN file exchange: RWB-P6-E1055-INF.
- The deployment, the Schedule registration, the dashboards, the alerts and the runbook: RWB-P6-E1055-OPS.
- Notice generation and the template and merge-field catalog: RWB-P6-E1052-APP and RWB-P6-E1046-APP.
- The WIN acknowledgment loop of Epic 2, the refused and undeliverable letters, the proof window and the queue transfer: RWB-E2-021, R-LIT-08, R-LIT-09.
- SMS and LINE dispatch: RWB-P6-E2022-APP.
- The ACE ingestion, the pod records, the freshness stamp and the ledger tables: rwb-source-data and RWB-P1-E1066-CON.
- The `NOTICE_PERIOD` timer and its start: rwb-case and RWB-P3-E1028-CON.
- The stored letter, its content and its retention: rwb-document and RWB-P5-E1054-CON.
- The gateway-bff composite route and the screen field lists: RWB-PLT-N001-CON.
