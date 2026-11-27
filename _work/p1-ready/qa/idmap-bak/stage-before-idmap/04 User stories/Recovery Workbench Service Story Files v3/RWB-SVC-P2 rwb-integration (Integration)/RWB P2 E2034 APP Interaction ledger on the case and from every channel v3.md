# RWB-P2-E2034-APP Interaction ledger on the case and from every channel

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P2-E2034-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-integration |
| Service epic | RWB-SVC-P2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Size | Not specified in the source documents (DOR-RWB-P2-E2034-APP-16); the squad sizes it at refinement |
| Legacy key | RWB-E2-034 |
| Legacy disposition | Split (rework) |
| Build status | Not started; build dependencies RWB-P2-E1007-APP and RWB-P2-E2034-OPS are not done yet |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP08, DP09, DP10, DP11, DP13, DP15, DP18, DP19 |
| Readiness decisions | RD-P1-001, RD-P1-003, RD-P1-004, RD-P1-007, RD-P1-008, RD-P1-010, RD-P1-011, RD-P1-040, RD-P1-041, RD-P1-066, RD-P1-067 |
| Parallel lane | L-P2-A |
| Ready to start | After RWB-P2-E1007-APP |
| Depends on (build) | RWB-P2-E2034-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P2-E1007-APP |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P4-E1037-CON, RWB-P7-E1027-CON, RWB-P3-E2016-CON, RWB-P1-E1066-CON, RWB-P1-E1067-CON, RWB-P1-E1015-CON (`AceDataReady`), and the `GET /efs-history` fragment of rwb-source-data |
| Integration dependencies | None |
| External dependencies | RWB-P2-E2034-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (no FR mapped to REQ-ILG-009, REQ-ILG-010, REQ-ILG-011, REQ-ILG-012, REQ-ILG-013, REQ-ILG-014, REQ-ILG-007, REQ-ILG-008, REQ-ILG-006) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-034 for rwb-integration. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P2-E2034-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (26 resolved, 34 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

- D-RCV-60 finishing pass: RD-P1-066, RD-P1-067; requests F05-affected-0152; Test Cases v9 mappings.

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- The ledger is appended with `InteractionRequest` 5.1.0 on the case-scoped path, with the business key form, a UUID `Idempotency-Key` header, 201 or 200 as success and 409 as a refusal; `sourceSystem` and the retention class are server-set (RD-P1-001, RD-P1-007; findings #2, #3).
- No ledger entry is appended for `NoticeDispatched` or `NoticeDelivered`: rwb-comms appends its own notice entries; the notice read and the contact-fact read are no longer called (RD-P1-007; finding #1, NEW-GAP-F05-3).
- The EFS read step starts on `AceDataReady` of ALS with status COMPLETED, reads `GET /efs-history` per account and uses the ruled EFS mapping and 201 or 200 counting (RD-P1-003, RD-P1-007, RD-P1-040; findings #4, #5, #6).
- `DecisionRecorded` type, error body and codes, resend idempotency, contract and fake versions (RD-P1-001, RD-P1-004, RD-P1-008, RD-P1-011; findings #8, #10, #11); AC20 to AC25, X12 and X13 added.
- Open: the account list and workflow ID of the daily EFS step (NEW-GAP-F18-5), who appends the treatment, partner and payment entries (NEW-GAP-F18-6), the EFS action-code filter (NEW-GAP-F18-4) and the eventCode of a promise row in the daily step (NEW-GAP-F05-4) (findings #4, #6, #7, #9).

### 1. Story

As a **platform operator of the channel intake (RW-PLATADM on call)**, I want **each of the six ledger events that the channels publish, plus `AceDataReady` of ALS, consumed, each ledger fact that this intake owns turned into one ledger entry by a consumer that appends through the rwb-source-data case-scoped ledger append, deduplicated by its own inbox, and a delivery whose case cannot be resolved parked in the exception queue with a task after three attempts, and the EFS read step to write its read summary**, so that **a contact, letter, hand-over, offer or payment is never lost between the channel that produced it and the ledger that records it, and no delivery disappears without an owner**.

The legacy story sat in module P2 Integration and did the whole job in one place: it owned the outbox consumer "ledger-channels", the event-to-entry mapping, the holder enrichment, the retention class, the EFS read step, the ledger columns and the timeline section. Under D-RCV-60 the ledger is not a P2 object. The R-PREC default ruling puts the interaction ledger and its intake rule in rwb-source-data (P1, DP-18; ownership map ruling on `interaction` and `efs_ledger_outcome`), the case timeline and the timeline read stay in rwb-case (P3), masking stays in rwb-access (P4) and the partner portal stays in rwb-partner (S9). What is left in module P2 — the outbound and event transport of the module — is the channel intake: a consumer on the owners' topics, a mapper, an idempotent append through the P1 contract, a delivery trail with its retries and its exception queue, and the EFS read step. That is what this story builds.

The ledger table, its append-only trigger `tr_interaction_append_only` and its read are not written here (DP-01, DP-18). The six business events are consumed on their owners' topics, never on a topic of this service (DP-14). Each append is one hop to the P1 contract with a 2 s budget (DP-11, DP-13). The append-only rule survives the split because the append operation is create-only and idempotent on the ledger business key, and the service that owns the table answers a repeated business key with 200 and the existing entry.

### 2. Business rationale

Contact outcomes from collections, letters sent through WIN and work held by partners are recorded in different systems today, so a case owner who picks up a case does not know which number answered or who held the case last. The legacy story answered that by bringing every channel into the one ledger built in Epic 1 and showing it as a timeline on the case. The business measure is unchanged: the share of open cases whose last right-party contact is visible on the case, which today is zero for cases that came from EFS.

The realignment keeps the measure and changes the seam. With 19 services, the ledger has one owner and it is not the integration module; if the intake also wrote the ledger there would be two writers of one append-only table, which is the failure the append-only trigger exists to prevent. The intake therefore has to be a transport: it must be allowed to fail, retry and park a delivery without the ledger knowing, and the ledger must be able to answer a repeated business key without writing a second entry and without the intake losing the event. That is what makes the channel set extensible: a seventh channel costs one mapping and one consumer group, not a change to the ledger.

The story meets REQ-ILG-009 (contact outcomes reach the ledger), REQ-ILG-010 (dispatched letters write their result, including proof of delivery), REQ-ILG-011 (a hand-over names who held the case, who holds it now and when), REQ-ILG-013 (each entry carries its retention class, resolved by the owner of the ledger), REQ-ILG-014 (the contact point is a reference and never a copy), REQ-ILG-007 (one entry per key, a repeat counted), REQ-ILG-008 (a failed write loses nothing) and REQ-ILG-006 (the timeline reads in time order, which the intake serves by carrying the occurred time unchanged). REQ-ILG-012 (the timeline is shown on the case record) is served by rwb-case and is cited here for traceability only.

### 3. Preconditions

- RWB-P2-E2034-CON is baselined: the consumed event contracts, the P1 append contract, the two admin operations, the delivery states, the dedupe key and the three-attempt rule (this key's contract story, Day 1).
- RWB-P2-E1007-APP is done: the rwb-integration service baseline, its `rwb_integration` schema, its login, its chart and its REST base `/api/recovery/integration/v1` (DP-01, DP-13).
- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03).
- RWB-PLT-E1042-CON and RWB-PLT-E1043-CON are published: the rwb-case parameters and reference-data contracts with their client library (DP-06, DP-07). The EFS ledger outcome list and the retention classes are P1 reference rows and are read by the P1 writer, not here.
- RWB-PLT-E1037-CON is published: the rwb-access authorise contract and the guard library (DP-08).
- RWB-PLT-TE006-CON is published: the outbox and inbox library, the CloudEvents 1.0 envelope, the retry topic and the `.dlt` topic of each owner's topic (DP-09).
- RWB-PLT-E1071-CON is published: the workflow kit, its worker and its retry policy (DP-10).
- RWB-PLT-E1044-CON is published: the per-service Flyway sequence and the migration conventions of `rwb_integration` (DP-15).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves the exception queue screen SCR-09 (DP-19).
- The six producers publish on their topics: `rwb.treatment.events.v1` (TreatmentApproved, EV-10), `rwb.comms.events.v1` (NoticeDispatched EV-14 and NoticeDelivered EV-15), `rwb.partner.events.v1` (InstructionIssued EV-20 and PartnerResultSubmitted EV-21), `rwb.payment.events.v1` (ProceedsMatched EV-25) and `rwb.source-data.events.v1` (AceDataReady EV-26). The two rwb-comms notice facts are consumed and counted but append nothing here: rwb-comms appends its notice entries itself (RD-P1-007; NEW-GAP-F05-3).
- The ledger append POST `/api/recovery/source-data/v1/cases/{caseId}/interactions` and the EFS history read `GET /api/recovery/source-data/v1/efs-history` are reachable inside the 2 s single-hop budget.
- Feature flag `rwb.integration.ledger-channels` exists in the platform flag library (legacy flag name kept), off by default in every environment.
- The service runs as the rwb-integration login (DP-02). The login name is Not specified in the source documents (GAP-0664; ASM-1168).
- The consumer group names, the offset policy, the retry scan interval, the lag and alert thresholds, the build ID format and the fixture owner are environment values set by RWB-P2-E2034-OPS and are Not specified in the source documents (GAP-0666); they are never coded.
- The retention class ILG-STD for every event code is an assumption until Compliance publishes the class list and its periods. The uuid link columns, the two LOV-LEDGER-EVENT values PARTNER_RESULT and OFFER, and the 422 refusal of an append with no class row are also assumptions (GAP-2184).
- Contract version built against: 5.0.0 of `rwb-integration.yaml` and of `rwb-integration.asyncapi.yaml` (Recovery Workbench API Specification v5); consumed rwb-source-data: `rwb-source-data.yaml` 5.1.0 and `asyncapi/rwb-source-data.asyncapi.yaml` 5.1.0 (API Specification v7), faked from `fakes/rwb-source-data/5.1.0/`.
- Open values of GAP-2321 are not set by this story and none is coded: the masking version label and the covered personal field IDs are settled with Compliance and the data steward at the wave-2 policy load; the AC-READ access-log granularity is confirmed with Internal audit; the parameter rows, their defaults and any login name still unnamed are named at build.

### 4. Flow

1. Outbox relay: delivers one CloudEvent per message to consumer `ledger-channels` on each owner's topic, with its retry topic and its `.dlt` topic (DP-09).
2. LedgerChannelListener: validates the CloudEvents 1.0 envelope and the event type against the seven declared types, then reads the event's idempotency key `<EV-nn>:<business key>:v1` through the inbox of `processed_event` (DP-09). A repeat is counted in `hit_count` and acknowledged without a second append. `AceDataReady` is deduped on `EV-26:ALS:<businessDate>`. `NoticeDispatched` and `NoticeDelivered` end here: inbox row, acknowledgement, no workflow, no delivery row and no append (RD-P1-007).
3. LedgerChannelIntakeWorkflow: starts one workflow execution per event, workflow ID `<eventId>` in namespace `rwb-recovery` on task queue `rwb-integration` (DP-10).
4. LedgerChannelMapper (activity `mapChannelEvent`): maps the event to exactly one `InteractionRequest` 5.1.0, by BR1 to BR4 and BR11: `eventCode`, `occurredAt`, `actorType`, `actorRef`, `sourceRef`, `idempotencyKey`, and where they apply `channel`, `direction`, the holder references and the business link. The case id goes in the path; `sourceSystem` and the retention class are set by the writer and are never sent.
5. FactResolution (activity `resolveChannelFacts`): reads the facts it needs through their owners' contracts, one hop each with a 2 s budget and no retry on a 4xx: the case, its case number and its holder from the rwb-case contract, the partner code from the rwb-partner contract, the treatment from the rwb-treatment contract and the proceeds from the rwb-payment contract (DP-11).
6. LedgerAppend (activity `appendLedgerEntry`): calls POST `/api/recovery/source-data/v1/cases/{caseId}/interactions` once with the request and a UUID `Idempotency-Key` header kept for every retry of that append, and receives the `Interaction`. 201 is a new entry; a replay of the same header key returns the stored answer; a new header key with a business key already in the ledger answers 200 with the existing entry (DP-18; RD-P1-001, RD-P1-007).
7. InboxCompletion: on a 201 or 200 answer the delivery moves to DELIVERED with its `delivered_at`, and the `processed_event` row is upserted with the key and the hit count. The append happens before the inbox mark, so a crash between the two replays the append and the P1 writer returns the same entry (BR5).
8. ExceptionPath (activity `parkDeliveryInException`): on a 5xx, a timeout or a case that cannot be resolved, the delivery stays PENDING or moves to RETRYING and its `next_attempt_at` is set by the retry policy. After the third failed attempt the delivery moves to EXCEPTION, `last_error_code` names the failure class, and a task `RESOLVE_OUTBOX_DELIVERY` is raised for role RW-PLATADM and linked in `task_id` (BR6).
9. EfsContactOutcomeReader: on `rwb.source-data.AceDataReady.v1` with `sourceSystem` ALS and `status` COMPLETED, starts one EfsLedgerReadWorkflow for the business date, not an outbox delivery; an event of another source system or status is acknowledged and ignored (BR8; RD-P1-003, RD-P1-040). The workflow ID literal is Pending (NEW-GAP-F18-5).
10. EfsLedgerReadWorkflow (activity `readEfsOutcomes`): calls `GET /api/recovery/source-data/v1/efs-history?accountKey=&businessDate=` once for each account linked to an open case (one account per call). Which operation lists those accounts is Pending (NEW-GAP-F18-5). The action-code filter of BR7 is Pending (NEW-GAP-F18-4).
11. EfsLedgerReadWorkflow (activity `appendEfsEntries`): maps each row by BR12 and calls POST `/api/recovery/source-data/v1/cases/{caseId}/interactions` once per row with the business key `EFS:<efsRecordKey>`.
12. EfsLedgerReadWorkflow (activity `writeEfsReadSummary`): closes the run with the read summary `businessDate`, `rowsRead`, `written`, `excluded`, `notOnCase`; `written` counts the 201 answers only, and a 200 answer (row already in the ledger) is not counted as written (RD-P1-007).
13. Platform administrator: opens SCR-09 through gateway-bff, filters the deliveries of consumer `ledger-channels` by status, consumer and event type, and resends a delivery in EXCEPTION (DP-19).
14. Resend: `POST /admin/outbox/deliveries/{deliveryId}/resend` sets the delivery PENDING with attempt count 0 under an `Idempotency-Key` (UUID; BR13), writes the resend to the decision record and starts the workflow again for the same event.
15. Screen states: SCR-09 has the states Loading, Filtered, Empty and Action failed; its Error and No access states are Not specified in the source documents (DOR-RWB-P2-E2034-APP-10), and a role without Platform administration is refused with MSG-P4-002 before any read or write (TC-E2-034-12). For SCR-04, the Loading state is as in Screen Specifications v1; the Empty, Error and No access states are Not specified in the source documents (DOR-RWB-P2-E2034-APP-10).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The same event arrives twice with the same CloudEvents id and business key | One entry exists; the repeat is counted in `hit_count` and no second append is made | None | AC8; BR5 |
| X2 | An EFS row carries an action code that the EFS ledger outcome list does not hold | No entry; the row is counted as excluded in the read summary | None | Carried by the P1 story of this legacy key (AC6) |
| X3 | An EFS row belongs to an account on no open case (counting of `notOnCase` Pending, NEW-GAP-F18-5) | No entry; the row is counted as not on a case | None | Carried by the P1 story of this legacy key (AC6) |
| X4 | The ledger append returns 503 (MSG-P1-022, MSG-PLT-N009-06 or MSG-GEN-006) or times out | The delivery stays PENDING or moves to RETRYING with `next_attempt_at`; an incident is raised and no entry is discarded | None | Carried by this story as the transport half of AC7 |
| X5 | The event names a case that does not exist | No entry after each attempt; after the third failed attempt the delivery is EXCEPTION with a task for role RW-PLATADM | MSG-P2-001 | AC8 |
| X6 | A fact read answers 404 | The mapper keeps the entry and leaves the link empty; the delivery is DELIVERED and the gap is logged without personal data | None | AC12; BR4 |
| X7 | A fact read answers 5xx or times out | Retryable: the activity fails and the workflow retries inside the 2 s budget; after the third attempt the delivery is EXCEPTION | MSG-P2-001 | AC8; AC18 |
| X8 | A message fails envelope validation, or carries a type this consumer does not declare | The message is refused before any state change and routed to `.dlt` with an alert | None | AC13; BR2 |
| X9 | A role without Platform administration opens the exception queue or resends | Refused before any read or write | MSG-P4-002 | AC14; carried by the CON story as a contract case |
| X10 | The delivery is resent while the workflow for the same event is running | Refused with 409; nothing changes and no second workflow is started | MSG-GEN-004 | AC15; BR6 |
| X11 | The ledger append answers 200 with the existing entry (repeated business key) | The answer is treated as success; the delivery is DELIVERED and no second entry exists | None | AC8; AC21; BR5 |
| X12 | The ledger append answers 409 (the business key with a different body, or the header key reused or still in flight) | Not a success: the attempt counts against the three attempts; after the third the delivery is EXCEPTION with its task | MSG-PLT-N009-05 | AC22; BR6 |
| X13 | `GET /efs-history` answers 409 (DP01 or DP05 is incomplete for the business date) | No row is appended for the account; the activity retries by the workflow kit policy and, after the third attempt, the run fails; a rerun of the date writes the rows | MSG-P1-001 | AC23; BR8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published contracts only: the P1 ledger append and EFS history read, the P3, S9, S2 and P8 fact reads, the platform outbox and workflow kit, and the rwb-integration baseline. Every one of them is faked |
| Negotiable | Retry intervals, alert thresholds, replica counts and consumer group names are environment values; the mapping, the dedupe key and the three-attempt rule are fixed by the CON story of this key |
| Valuable | Closes the last gap between a channel that produced an interaction and the ledger that records it, without a second writer of the append-only table |
| Estimable | One listener, one mapper, two workflows, five activities, one exception path, one admin surface and one migration |
| Small | Fits two weeks with the tests of section 16 |
| Testable | Each owned criterion and each transport path has a test in section 16, and every cross-service answer is stubbed in a contract fake |

### 7. Acceptance criteria

```gherkin
Feature: Channel intake of the interaction ledger for rwb-integration

  Background:
    Given open case "RW-2026-000301" with account "ACC-SYN-0301" and owner "U-2001"
    Given the EFS ledger outcome list holds action code "PTP" with channel CALL
    Given the retention class for every event code is "ILG-STD"

  Scenario: AC8 An event for an unknown case goes to the exception queue (legacy RWB-E2-034 AC8)
    Given event InstructionIssued names an instruction whose case does not exist
    Given the rwb-case contract mock returns no case for the instruction's case
    When the outbox has retried the delivery 3 times
    Then the system writes no entry
    Then the delivery is in the exception queue with a task for role RW-PLATADM

  Scenario: AC12 A fact read that answers 404 keeps the entry with an empty link (exception X6) (new, D-RCV-60)
    Given a fact read for the event answers 404
    When the mapper maps the event
    Then the entry is kept and its link is left empty
    Then the delivery is DELIVERED and the gap is logged without personal data

  Scenario: AC13 A message that fails envelope validation is refused before any state change (exception X8) (new, D-RCV-60)
    Given a message fails CloudEvents 1.0 envelope validation or carries an undeclared type
    When the message reaches the consumer ledger-channels
    Then the message is refused before any state change
    Then the message is routed to its .dlt topic with an alert

  Scenario: AC14 A role without Platform administration is refused before any read or write (exception X9) (new, D-RCV-60)
    Given a user whose role has no Platform administration
    When the user opens the exception queue or resends a delivery
    Then the request is refused before any read or write
    Then the refusal uses message MSG-P4-002

  Scenario: AC15 A resend while the workflow for the same event runs is refused with 409 (exception X10) (new, D-RCV-60)
    Given the workflow for the same event is running
    When the delivery is resent
    Then the request is refused with 409
    Then nothing changes and no second workflow is started
    Then the refusal uses message MSG-GEN-004

  Scenario: AC16 The intake publishes no business event and records its decisions locally (BR10) (new, D-RCV-60)
    Given a resend or an exception has been decided for a delivery
    When the decision is recorded
    Then the decision record is written through the local library in rwb_integration
    Then the decision record is published on rwb.decision-record.v1 and no other event is published

  Scenario Outline: AC17 A provided operation answers 401, 403 or 404 for a refused or unknown request (section 12 operations)
    Given a request to a provided operation with <case>
    When the request is received
    Then the operation answers <status> as application/problem+json with messageCode <code>

    Examples:
      | case | status | code |
      | no valid credential | 401 | MSG-P4-001 |
      | a role without Platform administration | 403 | MSG-P4-002 |
      | an unknown identifier | 404 | MSG-P4-003 |

  Scenario: AC18 A consumed call that fails or does not answer is retried and then goes to the exception queue (exception X7, BR6) (new, D-RCV-60)
    Given a consumed call answers 5xx or does not answer within its budget
    When the third attempt of the call fails
    Then the delivery is in the exception queue with a task RESOLVE_OUTBOX_DELIVERY for role RW-PLATADM
    Then the exception uses message MSG-P2-001

  Scenario: AC19 A status change that the delivery status model does not allow is refused (new, D-RCV-60)
    Given a delivery is in status DELIVERED
    When a status change is requested that the delivery status model does not allow
    Then the change is refused
    Then the delivery keeps status DELIVERED

  Scenario: AC20 A channel fact is appended as one InteractionRequest on the case-scoped path (BR1, BR11) (new, RD-P1-007)
    Given event TreatmentApproved for case "RW-2026-000301" with treatment "TRT-SYN-0301" and occurred date 2026-12-14
    When the intake processes the event
    Then it calls POST /api/recovery/source-data/v1/cases/{caseId}/interactions once with a UUID Idempotency-Key header
    Then the body has eventCode OFFER, occurredAt of the event, idempotencyKey "EV-10-RW-2026-000301-20261214-{treatment UUID}" and treatmentId, and has no sourceSystem, caseId or retentionClass
    Then on 201 the delivery is DELIVERED and the intake writes no decision record for the append

  Scenario: AC21 A repeated business key answers 200 and is a success (exception X11) (new, RD-P1-007)
    Given the ledger already holds the entry of the delivery's business key
    When the append is sent with a new Idempotency-Key header and the same body
    Then the answer is 200 with the existing entry
    Then the delivery is DELIVERED and no second entry exists

  Scenario: AC22 A 409 from the ledger append is not a success (exception X12) (new, RD-P1-001)
    Given the ledger append fake answers 409 with messageCode MSG-PLT-N009-05
    When the third attempt of the append fails
    Then the delivery is EXCEPTION with last_error_code set and a task RESOLVE_OUTBOX_DELIVERY for role RW-PLATADM

  Scenario: AC23 The EFS read step appends the history rows by the ruled mapping (BR8, BR12; exception X13) (new, RD-P1-007)
    Given AceDataReady with sourceSystem ALS, businessDate 2026-12-14 and status COMPLETED
    Given the efs-history fake answers two rows for account "ACC-SYN-0301", one with isPtp true, and the append answers 201 for one row and 200 for the other
    When EfsLedgerReadWorkflow runs
    Then one append per row is sent with idempotencyKey "EFS:{efsRecordKey}", actorType SERVICE, actorRef "rwb-integration" and sourceRef "EFS v_ace_efs_action"
    Then the summary has rowsRead 2 and written 1
    Then when the fake answers 409 MSG-P1-001 for the read instead, no row is appended for the account

  Scenario: AC24 Events that start or append nothing are acknowledged (BR1, BR8) (new, RD-P1-040)
    Given AceDataReady with sourceSystem EFS and status COMPLETED, or a NoticeDispatched or NoticeDelivered event
    When the event is consumed
    Then it is acknowledged and not dead-lettered
    Then no ledger append is sent and no workflow is started

  Scenario: AC25 A resend without a usable Idempotency-Key is refused (BR13) (new, RD-P1-001)
    Given a delivery in status EXCEPTION
    When RW-PLATADM sends the resend with no Idempotency-Key header or a value that is not a UUID
    Then the answer is 400 with messageCode MSG-PLT-N009-03
    Then the delivery stays EXCEPTION and no workflow is started
```

AC8 is the only legacy criterion this story owns, and it is copied word for word with one Given added for the mocked cross-service part: the rwb-case contract mock returns no case for the instruction's case, because rwb-case is now another service and the case lookup is a contract call. Every value of the legacy scenario is kept: the instruction event, the nonexistent case, the three retries, the empty ledger and the task for role RW-PLATADM.

The other legacy criteria are not owned here. AC1, AC6 and AC9 (the EFS contact entry, the EFS outcome list, the late EFS row) and AC3 (the ledger is one place, read through `GET /cases/{caseId}/interactions`) belong to the rwb-source-data stories of this legacy key, which own the ledger, the EFS intake rule and the interaction read. AC2 (a hand-over is recorded) is split: the CASE_ALLOCATED and CASE_TRANSFERRED entries and the holder enrichment are rwb-case's, and only the partner hand-over and partner result entries of BR2 are produced by this intake. AC4 (letter, delivery, offer and payment are recorded) is split: this story transports the offer and payment mapping, rwb-comms appends the letter and delivery entries (RD-P1-007), and the ledger assertions are the P1 story's. AC5 (nothing is written twice) is proved in three places — the inbox here in TC-E2-034-05, the append-only key in P1, and the timeline in P3. AC7 (a ledger write failure loses nothing) is the transport half carried here as exception path X4 and the ledger half carried by P1. AC10 (a case with no entry) and AC11 (a case outside the reader's scope) are the timeline and the scope rules of rwb-case, rwb-source-data and rwb-access.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Event to ledger event code: InstructionIssued to HANDOVER; PartnerResultSubmitted to PARTNER_RESULT; TreatmentApproved to OFFER; ProceedsMatched to PAYMENT; an EFS action row by BR12. NoticeDispatched and NoticeDelivered produce no entry from this intake (rwb-comms appends them, RD-P1-007; NEW-GAP-F05-3). Whether rwb-treatment, rwb-partner or rwb-payment also append these facts themselves is Pending (NEW-GAP-F18-6). The codes are kept character for character and are sent as they are | Legacy RWB-E2-034 BR1; LOV-LEDGER-EVENT |
| BR2 | The intake consumes exactly seven types on their owners' topics (the two notice types for inbox accounting only, BR1) and publishes none of its own: `rwb.treatment.TreatmentApproved.v1`, `rwb.comms.NoticeDispatched.v1`, `rwb.comms.NoticeDelivered.v1`, `rwb.partner.InstructionIssued.v1`, `rwb.partner.PartnerResultSubmitted.v1`, `rwb.payment.ProceedsMatched.v1` and `rwb.source-data.AceDataReady.v1` | Arch v5 slides 42 and 43; DP-14 |
| BR3 | A partner hand-over has channel PORTAL and direction OUTBOUND with the holder before and after; a partner result has channel PORTAL and direction INBOUND | Legacy BR2; LOV-CHANNEL; LOV-DIRECTION |
| BR4 | The contact point travels as a reference: the entry carries `contactKey` and never a number or an address; a fact that cannot be read leaves its link empty and never blocks the entry | Legacy BR5; REQ-ILG-014; CTL-11 |
| BR5 | One entry per idempotency key. The append is called before the inbox row is marked; the inbox dedupes the event on its own key and counts a repeat, and the ledger answers a repeated business key with 200 and the existing entry | Legacy BR7; R-UNI-40; REQ-ILG-007 |
| BR6 | A failed append or an unresolvable case never discards the delivery: it is retried, and after the third failed attempt it is EXCEPTION with a task `RESOLVE_OUTBOX_DELIVERY` for role RW-PLATADM | Legacy BR8; FSD P2 v3 AC-EXC-P2-001-01 and T4; REQ-ILG-008 |
| BR7 | An EFS row enters the ledger only when its action code is in the EFS ledger outcome list and only for an account linked to an open case; the list is a row set of rwb-source-data and is never copied into rwb_integration; the retention class is set by the ledger writer. Which component applies the list to rows read from `GET /efs-history` is Pending (NEW-GAP-F18-4) | Legacy BR3, BR6; DL29 (assumptions: Not specified in the source documents (DOR-RWB-P2-E2034-APP-18)); DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355); DP-18 |
| BR8 | The EFS read step is started by AceDataReady with `sourceSystem` ALS and `status` COMPLETED, once per business date, and is not an outbox delivery; a rerun for the same business date writes only the rows not yet written, by the key `EFS:<efsRecordKey>` (the others answer 200). A missing DP01 or DP05 completion for that date makes the read return 409 MSG-P1-001 | Legacy section 12 (EFS contact read step); EV-26 |
| BR9 | The intake writes no ledger row and reads no ledger table: the entry is created through the P1 append operation and the ledger is never queried from this service | DP-01; DP-18; ownership map ruling on `interaction` |
| BR10 | The intake publishes no business event of its own; the decision record of a resend and of an exception is written through the local library and published on `rwb.decision-record.v1` | DP-03; Arch v5 slide 42 row 08 |
| BR11 | The ledger business key of a channel entry is `<EV-nn>-<caseNo>-<yyyyMMdd of occurredAt>-<actionId>` (EV-10, EV-20, EV-21, EV-25), where actionId is the UUID of the producer's action record carried by the event; where the producer publishes `ce_idempotencykey`, that value is used. It is distinct from the inbox key. The `actorType`, `actorRef` and `sourceRef` values of these entries are Pending (GAP-0664) | RD-P1-007 rule 4 |
| BR12 | EFS row mapping: `eventCode` CONTACT (PROMISE when `isPtp`; the daily step's use of PROMISE is to be confirmed, NEW-GAP-F05-4), `occurredAt` = `contactAt`, `actionCode`, `contactResult` RIGHT_PARTY when `isRpc` else empty, `promiseAmount`, `promiseDate`, `actorType` SERVICE, `actorRef` `rwb-integration`, `sourceRef` `EFS v_ace_efs_action`, `idempotencyKey` `EFS:<efsRecordKey>` | RD-P1-007 rule 8 |
| BR13 | The resend takes a UUID `Idempotency-Key`: missing or not a UUID 400 MSG-PLT-N009-03; a replay returns the stored status and body; a different request or one still in flight 409 MSG-PLT-N009-05; store unavailable 503 MSG-PLT-N009-06; kept 24 hours | RD-P1-001 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| (none) | Event delivered to consumer `ledger-channels` | The envelope and the type validate | PENDING |
| PENDING | appendLedgerEntry returns 2xx | The entry exists in the ledger | DELIVERED |
| PENDING | Append or fact read fails | attempt_count < 3 | RETRYING |
| RETRYING | Retry attempt returns 2xx | The entry exists in the ledger | DELIVERED |
| RETRYING | Retry attempt fails | attempt_count = 3 | EXCEPTION |
| PENDING | The case cannot be resolved | attempt_count = 3 | EXCEPTION |
| EXCEPTION | Resend by RW-PLATADM | The delivery is in EXCEPTION and no workflow runs for the event | PENDING with attempt count 0 |

The four states are the values of LOV-OUTBOX-DELIVERY: PENDING, RETRYING, DELIVERED, EXCEPTION (TSD P2 v3 T3.2 and T4). The intake changes the state of its own deliveries only; it changes no case status and no ledger row, because the ledger is append-only and owned by rwb-source-data (legacy section 9, DP-18).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-INTGR, the rwb-integration service identity | Consumes the seven types, maps each event, calls the ledger append, `GET /efs-history` and the fact reads, and moves its own deliveries (service identity, no case right) |
| RW-PLATADM, platform administrator | Reads the exception queue and resends a delivery (Platform administration, RU) |
| RW-AUDIT, internal audit | Reads the deliveries, the resend record and the run summaries (Platform administration, R) |
| rwb-source-data contract | Creates the ledger entry from the append and owns the append-only rule; it answers a repeated business key with the existing entry and sets the retention class |
| rwb-case contract | Supplies the case and its holder; it owns the timeline and the scope check of the read |
| rwb-access contract | Supplies the role and scope decision of the exception queue operations |
| No approval applies | The intake takes no business decision; the resend is recorded, not approved |

The service runs as the rwb-integration login (DP-02). The login name is Not specified in the source documents (GAP-0664; ASM-1168). The `SY-CASEWF` actor and the "recovery service identity" of the legacy story are retired with the split: the EFS read step runs under the rwb-integration identity and reads EFS facts through the P1 contract, never through a view (DP-05, DP-18).

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-OPS-198 to DF-OPS-206 | outbox_delivery (rwb_integration) | event_id, consumer, status, attempt_count, next_attempt_at, last_error_code, delivered_at, task_id | Write |
| DF-OPS-178 to DF-OPS-183 | processed_event (rwb_integration) | consumer, idempotency_key, event_id, hit_count, last_seen_at | Write |
| DF-OPS-184 to DF-OPS-188 | idempotency_key (rwb_integration) | idempotency_key, endpoint, request_hash, response | Write (the two admin operations) |
| DF-DEC-001 to DF-DEC-018 | decision_record (library table in rwb_integration) | rule version, final call, actions and freshness of a resend and of an exception | Write (DP-03) |
| DF-INT-001 to DF-INT-029 | interaction through the P1 append contract | eventCode, channel, direction, occurredAt, actorType, actorRef, sourceRef, idempotencyKey, actionCode, contactResult, promiseAmount, promiseDate, fromHolderRef, toHolderRef, treatmentId, proceedsId (the case id is the path; source system and retention class are server-set) | Write through P1 only; no column of this table is in rwb_integration |
| DF-INT-036 | EFS contact result through `GET /efs-history` (`isRpc`) | contact_result | Read |
| DF-ACE-108, DF-ACE-109, DF-ACE-111, DF-ACE-114 | EFS action rows through `GET /efs-history` | efs_record_key, account_key, action_code, contact_at | Read |
| DF-CAS-001, DF-CAS-009, DF-CAS-025, DF-CAS-026 | case facts through the rwb-case contract | id, owner_user_id, case_id, account_key | Read |
| DF-PRT-002 | partner facts through the rwb-partner contract | partner_code | Read |
| DF-TRT-001 | treatment facts through the rwb-treatment contract | id | Read |
| DF-FIN-001 | proceeds facts through the rwb-payment contract | id | Read |

The ledger fields of DF-INT-001 to DF-INT-029 are written by rwb-source-data and are listed here only to fix what the mapper sends. No ACE view is read by this service and no ACE row is stored: the EFS facts come through the P1 contract and the case, partner, treatment and proceeds facts come through their owners' contracts (DP-01, DP-05). The JSON field names of the ledger append are those of `InteractionRequest` 5.1.0; the field names of the other owners' fact answers are Not specified in the source documents (GAP-0664; ASM-1168).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/integration/v1`; owner rwb-integration (P2). Two operations, the exception queue surface of this slice.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/admin/outbox/deliveries` | Lists the deliveries of consumer `ledger-channels` by status, consumer, event type and date window, with the attempt count, the next attempt time, the last error code and the linked task | Platform administration R | Not applicable |
| POST | `/admin/outbox/deliveries/{deliveryId}/resend` | Sends a delivery in EXCEPTION again: status PENDING, attempt count 0, the workflow started again for the same event | Platform administration U | `Idempotency-Key`; a delivery not in EXCEPTION answers 409; header answers of BR13 |

Both operations are the re-based forms of API-P2-003 and API-P2-004 of the legacy appendix (TSD P2 v3 T-A.1), whose paths sat under the monolith base. The outbound-item operations `GET /admin/outbound-items` and `POST /admin/outbound-items/{itemId}/resend` stay with the rwb-integration baseline of RWB-P2-E1007-CON and are not declared here. Errors are `application/problem+json` with the shared `Problem` schema (RD-P1-004). The request query parameters and the response fields of the two operations are Not specified in the source documents (GAP-0664; ASM-1168).

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| POST | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | rwb-source-data (P1) | One ledger entry per call: `InteractionRequest` 5.1.0 with a UUID `Idempotency-Key`; 201, or 200 on a repeated business key; 400, 401, 403, 404, 409 MSG-PLT-N009-05, 422, 503 (shared `Problem`) | One hop, 2 s (DP-11) |
| GET | `/api/recovery/source-data/v1/efs-history?accountKey=&businessDate=` | rwb-source-data (P1) | EFS contact and promise history of one account (caller: the rwb-integration workload identity); 409 MSG-P1-001 when DP01 or DP05 is incomplete for the business date | One hop, 2 s (DP-11) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | rwb-case (P3) | The case, its holder and its status (DP-06, DP-07 owner) | One hop, 2 s (DP-11) |
| GET | `/api/recovery/case/v1/cases` | rwb-case (P3) | The open case ids of an account (legacy `CaseQuery.openCaseIdsForAccount`) | One hop, 2 s (DP-11) |
| GET | The instruction-fact read of the rwb-partner contract | rwb-partner (S9) | The case and the partner code of an instruction (legacy `InstructionQuery.byId`) | One hop, 2 s (DP-11) |
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | rwb-treatment (S2) | The treatment id and its case behind an OFFER entry | One hop, 2 s (DP-11) |
| GET | The proceeds-fact read of the rwb-payment contract | rwb-payment (P8) | The proceeds id and its case behind a PAYMENT entry | One hop, 2 s (DP-11) |
| POST | `/api/recovery/access/v1/authorise` | rwb-access (P4) | The role and scope check of the two admin operations (DP-08) | One hop, 2 s (DP-11) |

The ledger append and the EFS history read are the published operations of `rwb-source-data.yaml` 5.1.0; no EFS read by business date and no contact-fact read is called by this story (the notice entries are rwb-comms's). The instruction read and the proceeds read are named by their legacy Java interfaces but have no path in the Ownership Map; their paths, query parameters and JSON field names are Not specified in the source documents (GAP-0664; ASM-1168). The case-list account filter is likewise unnamed.

#### 12.3 Events published

None by this service's topic. `rwb.integration.events.v1` carries FileDelivered and FileFailed from the outbound file side (Arch v5 slide 16) and this slice publishes neither. The decision record of a resend and of an exception is written by the local decision-record library, which publishes `rwb.decision.DecisionRecorded.v1` (EV-08) on `rwb.decision-record.v1` in the same transaction as the delivery change (DP-03, H RWB-PLT-E1027-CON).

#### 12.4 Events consumed

The service shares consumer group rwb-integration.rwb.source-data.events.v1 and one listener across its source-data event workflows, including JOB-08. It has READ on the main topic, READ and WRITE on retry topics and WRITE on the dead-letter topic (RD-P1-066).

| Event type | Topic | Owner | Consumer element |
|---|---|---|---|
| `rwb.treatment.TreatmentApproved.v1` | `rwb.treatment.events.v1` | S2 | Inbox dedupe, then one OFFER entry |
| `rwb.comms.NoticeDispatched.v1` | `rwb.comms.events.v1` | P6 | Inbox dedupe and acknowledgement only; rwb-comms appends the LETTER entry |
| `rwb.comms.NoticeDelivered.v1` | `rwb.comms.events.v1` | P6 | Inbox dedupe and acknowledgement only; rwb-comms appends the delivery entry |
| `rwb.partner.InstructionIssued.v1` | `rwb.partner.events.v1` | S9 | Inbox dedupe, then one HANDOVER entry, channel PORTAL, direction OUTBOUND |
| `rwb.partner.PartnerResultSubmitted.v1` | `rwb.partner.events.v1` | S9 | Inbox dedupe, then one PARTNER_RESULT entry, channel PORTAL, direction INBOUND |
| `rwb.payment.ProceedsMatched.v1` | `rwb.payment.events.v1` | P8 | Inbox dedupe, then one PAYMENT entry linked to the proceeds |
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 | Starts EfsLedgerReadWorkflow only for `sourceSystem` ALS and `status` COMPLETED; payload `sourceSystem`, `businessDate`, `status`, `completedAt`; not an outbox delivery |

All seven are CloudEvents 1.0 with the envelope attributes id, source, type, specversion, time, subject, datacontenttype, keyed by the case id where a case exists; `AceDataReady` has no case and its Kafka key is `{sourceSystem}:{businessDate}`. The dedupe key is the event's own business key in the form `<EV-nn>:<business key>:v1` for the six business events (`EV-10:TRT-SYN-0301:v1`, `EV-26:ALS:2026-11-10` are the documented shapes of the FSD) and `EFS:<efsRecordKey>` for an EFS row; these are inbox keys, and the ledger business key is that of BR11 and BR12. An `AceDataReady` of another source system is acknowledged and ignored, not dead-lettered. Delivery is at least once; the consumer is idempotent by key. A message without the envelope, or of a type not in this table, is routed to `.dlt` (DP-09).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| LedgerChannelIntakeWorkflow | Workflow, one execution per consumed event, workflow ID = the CloudEvents id | `rwb-integration` | Input: event type, CloudEvents id, business key, occurred time, case id, payload reference. Output: the ledger entry reference and the delivery state |
| mapChannelEvent | Activity | `rwb-integration` | Input: event type and payload. Output: one ledger entry command with the event code, channel, direction, occurred time, source system and links |
| resolveChannelFacts | Activity | `rwb-integration` | Input: the case id, instruction id, treatment id or proceeds id of the event. Output: the resolved facts; a 404 leaves a link empty, a 5xx is retryable |
| appendLedgerEntry | Activity | `rwb-integration` | Input: the `InteractionRequest`, the case id and the header key. Output: the ledger entry id and whether it was 201 or 200 |
| parkDeliveryInException | Activity | `rwb-integration` | Input: delivery id, failure class, attempt count. Output: status EXCEPTION, task `RESOLVE_OUTBOX_DELIVERY` for RW-PLATADM, decision record |
| EfsLedgerReadWorkflow | Workflow, started by AceDataReady of ALS with status COMPLETED, one per business date (ID literal Pending, NEW-GAP-F18-5) | `rwb-integration` | Input: business date. Output: `EfsReadSummary` |
| readEfsOutcomes | Activity | `rwb-integration` | Input: business date. Output: the kept and the excluded EFS rows |
| appendEfsEntries | Activity | `rwb-integration` | Input: the kept rows. Output: the count written, one append per row with key `EFS:<efsRecordKey>`; 201 counted as written |
| writeEfsReadSummary | Activity | `rwb-integration` | Input: the counts. Output: `EfsReadSummary(businessDate, rowsRead, written, excluded, notOnCase)` |

Every activity runs with the workflow kit's retry policy: initial interval 1 s, back-off 2, maximum 3 attempts, and a non-retryable classification for a 4xx of the append other than 409 (a 409 is retried inside the three attempts and is never a success) (DP-10). The workflow history carries ids, codes and counts only, never a contact point or an amount.

#### 12.6 Schedules

None. No Schedule is registered by this story. The intake is event-started from the seven consumed types, and the EFS read step is started by AceDataReady, not by a timer (BR8; Arch v5 slide 44 JOB-02 and JOB-04). The outbox relay itself is the platform relay of DP-09 and runs every minute in every service; it is not a Schedule of this story.

#### 12.7 Tables owned

| Table | Schema | Owner | Use in this story |
|---|---|---|---|
| outbound_item | rwb_integration | P2 | Read only, for the exception queue screen and its interface column; this slice writes no outbound file item |
| outbox_delivery | rwb_integration | PLT library, created in rwb_integration | One delivery per consumed event and consumer `ledger-channels`: status, attempt count, next attempt, last error, task |
| processed_event | rwb_integration | PLT library, created in rwb_integration | The inbox: consumer, idempotency key, CloudEvents id, hit count |
| idempotency_key | rwb_integration | PLT library, created in rwb_integration | The stored response of the two admin operations, kept 24 hours |
| decision_record | rwb_integration | PLT library, created in rwb_integration | The local decision record of a resend and of an exception (DP-03) |

`outbox_event` exists in `rwb_integration` from the service baseline and this story writes no row in it: the consumed events are produced by their owners, and the intake records their progress on `outbox_delivery` with the CloudEvents id as `event_id`. The `interaction` table, its append-only trigger and its read are rwb-source-data's; `efs_ledger_outcome` is rwb-source-data's reference table; the timeline is rwb-case's. None of them is read or written here (DP-01, DP-18).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-source-data WireMock — append | `POST /cases/{caseId}/interactions` of `fakes/rwb-source-data/5.1.0/` | 201 with the `Interaction`; 200 with the existing entry for a repeated business key; 409 MSG-PLT-N009-05; 503 MSG-P1-022 and a slow answer for the retry paths of TC-E2-034-07 |
| rwb-source-data WireMock — EFS history | `GET /efs-history` of `fakes/rwb-source-data/5.1.0/` | 200 with rows for one account (one with `isPtp` true) for business date 2026-12-14; 409 MSG-P1-001 |
| rwb-case WireMock | The P3 case contract | Case `RW-2026-000301` with holder "U-2001"; no case for instruction `INS-SYN-0304` (AC8); the open case ids of `ACC-SYN-0301` |
| rwb-partner WireMock | The S9 contract | Instruction `INS-SYN-0301` to partner `LF-SYN-01`; one partner result |
| rwb-treatment and rwb-payment WireMock | The S2 and P8 contracts | Treatment `TRT-SYN-0301`; proceeds `PRC-SYN-0301` of 5,000.00 |
| rwb-access WireMock | The P4 contract | `POST /authorise` granting and refusing Platform administration |
| Kafka stubs | The seven topics | One message per type, one duplicate, one malformed envelope, one unknown type |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided; the ledger append, the EFS history read, the authorise call and the P3, S9, S2 and P8 fact reads consumed | The two admin operations provided; the P1 append and EFS history, the P4 authorise call, the P3, S9, S2 and P8 fact reads; one hop, 2 s timeout |
| Kafka | 0 published, 7 types consumed | Four business events for one entry each, two notice events for inbox accounting only and AceDataReady for the EFS read step; inbox dedupe on every one |
| Temporal | 2 workflows, 6 activities | LedgerChannelIntakeWorkflow with four activities; EfsLedgerReadWorkflow with three activities end to end |
| File | None | The EFS rows are read through the P1 contract, not from a file or a view |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.integration`, module `ledgerintake`, Java package `th.co.scb.ace.workbench.recovery.integration.ledgerintake`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_integration`; the ledger table is never read or written here | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | ACE facts read through rwb-source-data's contract; this service reads no view | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case with the client library | H RWB-PLT-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case with the client library | H RWB-PLT-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library, CloudEvents, the owners' topics, retry and `.dlt` | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Event-started workflows and activities through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/integration/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in `rwb_integration` | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data; the intake appends through its contract | none |
| DP-19 | Screen, ace-web | gateway-bff composite route for SCR-09 | H RWB-PLT-N001-CON |

RWB-P2-E1007-APP is the same-service baseline story in the build dependency row: the schema, the login, the REST base and the relay of `rwb_integration` come from it.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| LedgerChannelListener | Listener | Envelope validation for the seven types, inbox dedupe, workflow start per appended event type; no workflow for the notice types (BR1, BR2, BR5) |
| LedgerChannelMapper | Service | One method per event type implementing BR1, BR3 and BR4; the codes are sent, never resolved, here |
| FactResolver | Client | The P3, S9, S2 and P8 fact reads behind one 2 s budget with no retry on 4xx (DP-11) |
| LedgerAppendClient | Client | The ledger append and `GET /efs-history`; one hop, 2 s, idempotent on the business key (DP-18) |
| DeliveryTracker | Service | The `outbox_delivery` row of a consumed event: attempt count, next attempt, status, task (BR6) |
| ChannelIntakeWorkflow | Workflow | LedgerChannelIntakeWorkflow with its four activities |
| EfsContactOutcomeReader | Workflow and activities | EfsLedgerReadWorkflow: read, append, summary (BR7, BR8) |
| ExceptionQueueController | Controller | The two admin operations, their validation and their problem responses (DP-13, DP-19) |
| DecisionRecordWriter | Library client | The record of a resend and of an exception through the local library (DP-03) |
| AccessCheckClient | Client | The role and scope check of the two admin operations (DP-08) |

**Database and migrations**

- Writes `outbox_delivery`, `processed_event`, `idempotency_key` and the library table `decision_record` in schema `rwb_integration`, through the rwb-integration login (DP-02, DP-15). The login name is Not specified in the source documents (GAP-0664; ASM-1168).
- One migration in the rwb-integration sequence: `Vnnnn__ledger_intake.sql` (nnnn is the next free number of the service's own Flyway sequence, which starts at V0001) adds the partial index on `processed_event (consumer, idempotency_key)` where the inbox is read and the index on `outbox_delivery (consumer, status, next_attempt_at)` where the retry scan reads.
- No ledger column, no ledger table and no EFS reference table is created here; the six legacy columns of `interaction` and the `efs_ledger_outcome` rows are P1's migration (legacy section 13, DP-18).

**Configuration and reference data**

- Feature flag `rwb.integration.ledger-channels` in the platform flag library; off by default, on in the environments of the release. Off: the consumer acknowledges the seven types without writing, the EFS read step does not run and no delivery row moves.
- The retry intervals of a delivery and the attempt limit of three are rows of the environment configuration, not code (ASM-1170). The EFS ledger outcome list is a rwb-source-data row set (who applies it: NEW-GAP-F18-4); the retention class is set by the ledger writer.
- The consumer name `ledger-channels` is kept from the legacy story as the logical consumer; its Kafka group names are deployment values of the OPS story.
- The two admin operations declare Platform administration R and U; no role name is written in code (DP-08).

**Build steps**

1. LedgerChannelListener and DeliveryTracker against the platform inbox, with one test per consumed type and the duplicate path; AC8, BR2, BR5.
2. LedgerChannelMapper, one method and one unit test per appended event type (BR11), with the codes of BR1 sent unchanged; BR1, BR3.
3. FactResolver over the four owner contracts and the contract fakes, with the 404 and 5xx split; BR4.
4. LedgerAppendClient over the ledger append and the EFS history read, with 201 and 200 as success and 409 as a failed attempt; BR5, BR9.
5. ChannelIntakeWorkflow with its four activities and the retry policy, then the exception path and the task for RW-PLATADM; AC8, BR6.
6. EfsContactOutcomeReader as the second workflow, with the summary and the `EFS:<efsRecordKey>` key; the summary reports `written` from the 201 answers; a 200 is a row already in the ledger; BR7, BR8.
7. ExceptionQueueController with the two admin operations, the scope check, the resend and the 409 on a running workflow; X9, X10.
8. DecisionRecordWriter on the resend and on the exception, with the rollback path; BR10.
9. The contract-fake run of every cross-service answer in isolation, so the story builds before the other services exist.
10. The migration and its indexes, then the load of the configuration rows.

**Feature switch.** `rwb.integration.ledger-channels`. On: the seven types are consumed, the four channel facts are appended, and the EFS read step runs. Off: the deliveries are acknowledged and counted but nothing is appended and no workflow is started; the ledger of P1 is unchanged and no delivery is dated.

**Done when.** The tests in section 16 pass, a duplicate of any of the four appended business events writes one entry and counts one repeat, a notice event writes none, an unresolvable case ends in EXCEPTION with a task for RW-PLATADM on the third attempt, a 503 from the append loses no delivery, and a rerun of the EFS read step for the same business date adds no entry and reports `written` 0 for rows already in the ledger.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-001 | A delivery is in the exception queue after its retries | Not specified in the source documents (GAP-0664; ASM-1168) |
| MSG-GEN-004 | The delivery is not in EXCEPTION, or a workflow runs for the same event | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-005 | A resend is accepted | Not specified in the source documents (GAP-0664; ASM-1168) |
| MSG-P4-002 | A role without Platform administration calls one of the two operations | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | A provided operation is called with no valid credential | Text per Error and Message Standard v6 |
| MSG-P4-003 | The delivery id is unknown | Text per Error and Message Standard v6 |
| MSG-P1-001 | `GET /efs-history` answers 409 (exception X13) | Text per Error and Message Standard v6 |
| MSG-P1-022 | The ledger append answers 503 | Text per Error and Message Standard v6 |
| MSG-PLT-N009-03, -05, -06 | Idempotency header missing or not a UUID; reused or in flight; store unavailable (BR13, X12) | Text per Error and Message Standard v6 |

MSG-P2-001 and MSG-GEN-005 are named by the FSD and the legacy exception flows but their texts are not in the source set; the placeholder is carried until the Error and Message Standard names them. MSG-GEN-004 and MSG-P4-002 are the agreed texts and are copied unchanged.

### 15. Screens and states

SCR-09 Exception queue, served by the gateway-bff composite route (DP-19). The platform administrator filters the deliveries of consumer `ledger-channels` by status PENDING, RETRYING, DELIVERED and EXCEPTION, by consumer, by event type and by date window, and reads the attempt count, the next attempt time, the last error code and the task. A delivery in EXCEPTION offers the resend action; the row then shows PENDING with attempt count 0 and the resend time. The screen has the states Loading, Filtered, Empty and Action failed; its Error and No access states are Not specified in the source documents (CG-ALL-3224), and the resend confirmation names the delivery and the event type only. The screen fields, their layout and their masking are Not specified in the source documents (GAP-0664; ASM-1168). No screen shows a ledger entry, a contact point or an amount: the timeline on the case is SCR-04 and belongs to rwb-case. The Loading state of SCR-04 is as in Screen Specifications v1; its Empty, Error and No access states are Not specified in the source documents (CG-ALL-3223).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-034-12 | Access | Component | A role without Platform administration opens the deliveries and resends; refused with MSG-P4-002 |
| TC-E2-034-01 | AC1, BR3, BR4, BR5, BR6 (run by owning story; Not specified in the source documents (CG-ALL-3219)) | End to end | One EFS action row with a promise; one Workbench call |
| TC-E2-034-02 | AC2, BR2 (run by owning story; Not specified in the source documents (CG-ALL-3219)) | End to end | One transfer; one instruction to partner LF-SYN-01 |
| TC-E2-034-03 | AC3, BR4, BR9 (run by owning story; Not specified in the source documents (CG-ALL-3219)) | End to end | Entries from EFS, Workbench and the partner portal |
| TC-E2-034-04 | AC4, BR1 (run by owning story; Not specified in the source documents (CG-ALL-3219)) | End to end | NoticeDispatched, NoticeDelivered (appended by rwb-comms), TreatmentApproved, ProceedsMatched |
| TC-E2-034-05 | AC5, BR7 (run by owning story; Not specified in the source documents (CG-ALL-3219)) | End to end | TreatmentApproved delivered twice with one event ID |
| TC-E2-034-06 | AC6, BR3 (run by owning story; Not specified in the source documents (CG-ALL-3219)) | End to end | Three EFS rows: listed, unlisted, no open case |
| TC-E2-034-07 | AC7, BR8 (run by owning story; Not specified in the source documents (CG-ALL-3219)) | End to end | Ledger store stopped, then restarted |
| TC-E2-034-08 | AC8 | End to end | InstructionIssued for a case that does not exist |
| TC-E2-034-09 | AC9, BR9 (run by owning story; Not specified in the source documents (CG-ALL-3219)) | End to end | EFS row processed after a later Workbench call |
| TC-E2-034-10 | AC10 (run by owning story; Not specified in the source documents (CG-ALL-3219)) | End to end | Case with no entry |
| TC-E2-034-11 | AC11 (run by owning story; Not specified in the source documents (CG-ALL-3219)) | End to end | Reader of team HP-NE with Own scope |
| TC-E2-034-13 | §12 operations, events and activities | Contract | Each operation, consumed event and activity of section 12 against its contract |
| TC-E2-034-14 | §12.7 tables (ASM-3438) | Boundary | Each table of section 12.7 at its limits |
| TC-E2-034-15 | AC12, BR4 | End to end | A fact read answers 404; the entry is kept with an empty link |
| TC-E2-034-16 | AC13, BR2 | Component | A message fails envelope validation; a message of an undeclared type |
| TC-E2-034-17 | AC14 | Component | Role without Platform administration opens the queue and resends |
| TC-E2-034-18 | AC15, BR6 | End to end | Resend while the workflow for the same event is running |
| TC-E2-034-19 | AC16, BR10 | Component | Resend and exception write the decision record and publish on rwb.decision-record.v1 |
| TC-E2-034-20 | AC17 | Contract | A provided operation called without a credential, by a role without Platform administration, and with an unknown identifier; answers 401, 403 and 404 |
| TC-E2-034-21 | AC18, BR6 | End to end | A consumed call answers 5xx on each of three attempts; the delivery is EXCEPTION with its task |
| TC-E2-034-22 | AC19 | Component | A DELIVERED delivery is asked to move to a status the model does not allow; refused and unchanged |
| TC-P2-E2034-APP-02 | AC20, BR11 | Contract | TreatmentApproved for RW-2026-000301; the exact `InteractionRequest` and header |
| TC-P2-E2034-APP-03 | AC21, X11 | Component | Append answers 200 for a repeated business key |
| TC-P2-E2034-APP-04 | AC22, X12 | Component | Append answers 409 MSG-PLT-N009-05 three times |
| TC-P2-E2034-APP-05 | AC23, BR12, X13 | Component | AceDataReady ALS 2026-12-14; two history rows, 201 and 200; a 409 MSG-P1-001 read |
| TC-P2-E2034-APP-06 | AC24 | Component | AceDataReady of EFS; NoticeDispatched; NoticeDelivered |
| TC-P2-E2034-APP-07 | AC25, BR13 | Contract | Resend without a header and with a non-UUID header |
| TC-P2-E2034-APP-01 | AC17 | Contract | AC17 A provided operation answers 401, 403 or 404 for a refused or unknown request (section 12 operations) |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end, Access to Component and Resilience to NFR; no test case of this legacy key carries the Resilience level. This story runs TC-E2-034-07 (the append fails and the delivery is retried and delivered), TC-E2-034-05 (the same event delivered twice writes one entry and counts one repeat) and TC-E2-034-08 (the unknown case reaches the exception queue with the task) against its own consumer, its own inbox and its own exception queue. The other nine are carried by the P1, P3, P4 and S9 stories of this legacy key, which own the ledger, the read, the masking and the partner portal; they are listed here so that the legacy key stays complete.

### 17. Guardrails

- No business value in code: the event codes, the channels, the directions, the retry intervals and the attempt limit are rows of reference data and environment configuration; the mapper sends codes and resolves none.
- No personal data in logs, events, workflow inputs or histories: the entry carries `contactKey` and the identifiers of the case, the notice, the instruction, the treatment and the proceeds, never a number, an address or an amount.
- `idempotency_key` of the ledger entry (DF-INT-018) is classed Confidential, Customer data, by Data Classification v5 and is handled by its rule: shown only within the role's scope; in an event or workflow input it is never beside a direct identifier; in a log, trace or metric only a code or an id appears, never the customer value.
- No read of another service's table and no ACE view: the ledger is reached only through the P1 append, the EFS facts only through `GET /efs-history`, and the case, partner, treatment and proceeds facts only through their owners' contracts (DP-01, DP-05, DP-18).
- The intake never updates or deletes a ledger entry: the append is create-only and idempotent on the key, and the append-only trigger of the ledger stays in the owner's schema.
- One login per service and one topic per service: the release carries the rwb-integration login and consumes the owners' topics; it publishes nothing on `rwb.integration.events.v1` for this slice (DP-02, DP-14).
- A delivery is never discarded: an unresolvable case or a failed append ends in EXCEPTION with a task for RW-PLATADM after three attempts (BR6).
- Every fake and every fixture is synthetic; no production payload, contact point or event is copied into a test.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ILG-009 | Contact outcomes from collections reach the ledger | Epic 2, section 3.2 | FEAT-ILG-06 | 06 to 10 Recovery case processes | R-UNI-40 | TC-E2-034-01, TC-E2-034-06, TC-E2-034-09 |
| REQ-ILG-010 | Dispatched letters write their result, including proof of delivery | Epic 2, section 3.2 | FEAT-ILG-07 | 06 to 10 Recovery case processes | R-UNI-40 | TC-E2-034-04, TC-E2-034-05, TC-E2-034-07 |
| REQ-ILG-011 | A hand-over names who held the case, who holds it now and when | Epic 2, section 3.2 | FEAT-ILG-08 | 06 to 10 Recovery case processes | None | TC-E2-034-02, TC-E2-034-08 |
| REQ-ILG-012 | The case record view shows the ledger as an ordered timeline | Epic 2, section 3.2 | FEAT-ILG-09 | 06 to 10 Recovery case processes | None | TC-E2-034-03, TC-E2-034-10, TC-E2-034-11, TC-E2-034-12 |
| REQ-ILG-013 | Ledger entries carry their own retention class | Epic 2, section 3.2 | FEAT-ILG-10 | All recovery processes | None | TC-E2-034-01 |
| REQ-ILG-014 | The contact point is stored as a reference and is never copied | Epic 2, section 3.2 | FEAT-ILG-06 | 06 to 10 Recovery case processes | CTL-11 | TC-E2-034-01 |
| REQ-ILG-007 | One entry per key; a repeat is ignored and counted | Epic 2, section 3.2 | FEAT-ILG-06 | 06 to 10 Recovery case processes | R-UNI-40 | TC-E2-034-05 |
| REQ-ILG-008 | A failed ledger write loses no entry and the delivery is retried | Epic 2, section 3.2 | FEAT-ILG-07 | 06 to 10 Recovery case processes | None | TC-E2-034-07 |
| REQ-ILG-006 | The timeline orders entries by occurred time and case sequence | Epic 2, section 3.2 | FEAT-ILG-09 | 06 to 10 Recovery case processes | None | TC-E2-034-03, TC-E2-034-09 |

Every requirement of this legacy key is cited; the ones whose ledger assertion is the P1 story's are listed with the test case that proves the transport half here and are proved end to end by the P1, P3 and P4 stories.

### 19. Out of scope

- The `interaction` table, its six added columns, the append-only trigger, the EFS ledger outcome list, the retention classes and the append and read operations: carried by the rwb-source-data stories of this legacy key (DP-18).
- The timeline and its read `GET /cases/{caseId}/interactions` and the empty state of the case record: carried by the rwb-case stories of this legacy key, with the sequence order of BR9 of the legacy story.
- Masking of the contact point by role and the scope refusals: carried by the rwb-access stories of RWB-E1-037.
- The CASE_ALLOCATED and CASE_TRANSFERRED entries and the holder enrichment of a bank-to-bank move: carried by rwb-case, which owns the allocation and the transfer.
- The partner instruction, the partner result capture and the partner portal screens: carried by the rwb-partner stories; this story only consumes their events.
- Notice entries (dispatch, proof of delivery, SMS and LINE results): rwb-comms appends them through the same ledger operation (RD-P1-007; RWB-E2-022).
- Proof of delivery capture from WIN and the notice period timer: RWB-E2-021.
- Retention periods and the disposal job: DL26 and JOB-17.
- The outbound file items, the WIN and debt-buyer files and the `outbound_item` resend: RWB-P2-E1007-APP and its contract.
- The Helm values, the consumer groups, the dashboards, the alerts and the runbook: RWB-P2-E2034-OPS.

### Remaining delivery steps

- Settle the account list, workflow ID and counts of the daily EFS step (NEW-GAP-F18-5) and who appends the treatment, partner and payment entries (NEW-GAP-F18-6); solution architect.
- Settle the EFS action-code filter (NEW-GAP-F18-4), the notice entry writer (NEW-GAP-F05-3), the promise-row eventCode (NEW-GAP-F05-4) and the DP05 hold (NEW-GAP-F04-6).
- Fix the actor, source and fact field names left open (GAP-0664) at contract review of RWB-P2-E2034-CON (service contract owner).
- Publish the rwb-source-data fake at version 5.1.0 and mark RWB-P2-E2034-CON Done (service contract owner).
- Size the story at refinement and obtain epic design sign-off (squad lead, solution architect).
- Add the new test cases in Test Cases v9 and load test data in DEV (test lead).
