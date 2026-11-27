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
| Legacy key | RWB-E2-034 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP08, DP09, DP10, DP11, DP13, DP15, DP18, DP19 |
| Parallel lane | L-P2-A |
| Ready to start | After RWB-P2-E1007-APP |
| Depends on (build) | RWB-P2-E2034-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P2-E1007-APP |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P4-E1037-CON, RWB-P7-E1027-CON, RWB-P3-E2016-CON, RWB-P1-E1066-CON, RWB-P1-E1067-CON |
| Integration dependencies | None |
| External dependencies | RWB-P2-E2034-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (no FR mapped to REQ-ILG-009, REQ-ILG-010, REQ-ILG-011, REQ-ILG-012, REQ-ILG-013, REQ-ILG-014, REQ-ILG-007, REQ-ILG-008, REQ-ILG-006) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-034 for rwb-integration. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P2-E2034-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform operator of the channel intake (RW-PLATADM on call)**, I want **each of the six ledger events that the channels publish, plus AceDataReady for EFS, turned into one ledger entry by a consumer that appends through the rwb-source-data `InteractionLedgerWriter` contract, deduplicated by its own inbox, and a delivery whose case cannot be resolved parked in the exception queue with a task after three attempts, and the EFS read step to write its read summary**, so that **a contact, letter, hand-over, offer or payment is never lost between the channel that produced it and the ledger that records it, and no delivery disappears without an owner**.

The legacy story sat in module P2 Integration and did the whole job in one place: it owned the outbox consumer "ledger-channels", the event-to-entry mapping, the holder enrichment, the retention class, the EFS read step, the ledger columns and the timeline section. Under D-RCV-60 the ledger is not a P2 object. The R-PREC default ruling puts the interaction ledger and its intake rule in rwb-source-data (P1, DP-18; ownership map ruling on `interaction` and `efs_ledger_outcome`), the case timeline and the timeline read stay in rwb-case (P3), masking stays in rwb-access (P4) and the partner portal stays in rwb-partner (S9). What is left in module P2 — the outbound and event transport of the module — is the channel intake: a consumer on the owners' topics, a mapper, an idempotent append through the P1 contract, a delivery trail with its retries and its exception queue, and the EFS read step. That is what this story builds.

The ledger table, its append-only trigger `tr_interaction_append_only` and its read are not written here (DP-01, DP-18). The six business events are consumed on their owners' topics, never on a topic of this service (DP-14). Each append is one hop to the P1 contract with a 2 s budget (DP-11, DP-13). The append-only rule survives the split because the append operation is create-only and idempotent on the entry key, and the service that owns the table refuses a second key.

### 2. Business rationale

Contact outcomes from collections, letters sent through WIN and work held by partners are recorded in different systems today, so a case owner who picks up a case does not know which number answered or who held the case last. The legacy story answered that by bringing every channel into the one ledger built in Epic 1 and showing it as a timeline on the case. The business measure is unchanged: the share of open cases whose last right-party contact is visible on the case, which today is zero for cases that came from EFS.

The realignment keeps the measure and changes the seam. With 19 services, the ledger has one owner and it is not the integration module; if the intake also wrote the ledger there would be two writers of one append-only table, which is the failure the append-only trigger exists to prevent. The intake therefore has to be a transport: it must be allowed to fail, retry and park a delivery without the ledger knowing, and the ledger must be able to refuse a repeated key without the intake losing the event. That is what makes the channel set extensible: a seventh channel costs one mapping and one consumer group, not a change to the ledger.

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
- The six producers publish on their topics: `rwb.treatment.events.v1` (TreatmentApproved, EV-10), `rwb.comms.events.v1` (NoticeDispatched EV-14 and NoticeDelivered EV-15), `rwb.partner.events.v1` (InstructionIssued EV-20 and PartnerResultSubmitted EV-21), `rwb.payment.events.v1` (ProceedsMatched EV-25) and `rwb.source-data.events.v1` (AceDataReady EV-26).
- The P1 append contract, the P1 EFS outcome read and the P1 contact read are reachable inside the 2 s single-hop budget.
- Feature flag `rwb.integration.ledger-channels` exists in the platform flag library (legacy flag name kept), off by default in every environment.
- The service runs as the rwb-integration login (DP-02). The login name is Not specified in the source documents (GAP-0664; ASM-1168).

### 4. Flow

1. Outbox relay: delivers one CloudEvent per message to consumer `ledger-channels` on each owner's topic, with its retry topic and its `.dlt` topic (DP-09).
2. LedgerChannelListener: validates the CloudEvents 1.0 envelope and the event type against the seven declared types, then reads the event's idempotency key `<EV-nn>:<business key>:v1` through the inbox of `processed_event` (DP-09). A repeat is counted in `hit_count` and acknowledged without a second append.
3. LedgerChannelIntakeWorkflow: starts one workflow execution per event, workflow ID `<eventId>` in namespace `rwb-recovery` on task queue `rwb-integration` (DP-10).
4. LedgerChannelMapper (activity `mapChannelEvent`): maps the event to exactly one ledger entry command, by BR1 to BR4: event code, channel, direction, occurred time, source system, the case id, the contact key, the holder references and the business link.
5. FactResolution (activity `resolveChannelFacts`): reads the facts it needs through their owners' contracts, one hop each with a 2 s budget and no retry on a 4xx: the case and its holder from the rwb-case contract, the notice barcode and delivery status from the rwb-comms contract, the partner code from the rwb-partner contract, the treatment from the rwb-treatment contract and the proceeds from the rwb-payment contract (DP-11).
6. LedgerAppend (activity `appendLedgerEntry`): calls the P1 append operation once with the entry command and the idempotency key, and receives the ledger entry reference. The append is create-only and idempotent on the key, so a replay after a timeout returns the same reference and writes nothing (DP-18).
7. InboxCompletion: on a 2xx answer the delivery moves to DELIVERED with its `delivered_at`, and the `processed_event` row is upserted with the key and the hit count. The append happens before the inbox mark, so a crash between the two replays the append and the P1 writer returns the same entry (BR5).
8. ExceptionPath (activity `parkDeliveryInException`): on a 5xx, a timeout or a case that cannot be resolved, the delivery stays PENDING or moves to RETRYING and its `next_attempt_at` is set by the retry policy. After the third failed attempt the delivery moves to EXCEPTION, `last_error_code` names the failure class, and a task `RESOLVE_OUTBOX_DELIVERY` is raised for role RW-PLATADM and linked in `task_id` (BR6).
9. EfsContactOutcomeReader: on AceDataReady (EV-26) for the EFS source, starts EfsLedgerReadWorkflow, not an outbox delivery (BR8).
10. EfsLedgerReadWorkflow (activity `readEfsOutcomes`): reads the EFS action rows of the business date for accounts linked to open cases through the P1 EFS outcome read, and keeps only the action codes the EFS ledger outcome list holds (BR7).
11. EfsLedgerReadWorkflow (activity `appendEfsEntries`): maps each kept row to a CONTACT entry with source EFS and the idempotency key `EFS:<efs_record_key>`, and calls the same P1 append operation once per row.
12. EfsLedgerReadWorkflow (activity `writeEfsReadSummary`): closes the run with the read summary `businessDate`, `rowsRead`, `written`, `excluded`, `notOnCase`.
13. Platform administrator: opens SCR-09 through gateway-bff, filters the deliveries of consumer `ledger-channels` by status, consumer and event type, and resends a delivery in EXCEPTION (DP-19).
14. Resend: `POST /admin/outbox/deliveries/{deliveryId}/resend` sets the delivery PENDING with attempt count 0 under an `Idempotency-Key`, writes the resend to the decision record and starts the workflow again for the same event.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The same event arrives twice with the same CloudEvents id and business key | One entry exists; the repeat is counted in `hit_count` and no second append is made | None | AC8; BR5 |
| X2 | An EFS row carries an action code that the EFS ledger outcome list does not hold | No entry; the row is counted as excluded in the read summary | None | Carried by the P1 story of this legacy key (AC6) |
| X3 | An EFS row belongs to an account on no open case | No entry; the row is counted as not on a case | None | Carried by the P1 story of this legacy key (AC6) |
| X4 | The P1 append returns 5xx or times out | The delivery stays PENDING or moves to RETRYING with `next_attempt_at`; an incident is raised and no entry is discarded | None | Carried by this story as the transport half of AC7 |
| X5 | The event names a case that does not exist | No entry after each attempt; after the third failed attempt the delivery is EXCEPTION with a task for role RW-PLATADM | MSG-P2-001 | AC8 |
| X6 | A fact read answers 404 | The mapper keeps the entry and leaves the link empty; the delivery is DELIVERED and the gap is logged without personal data | None | BR4 |
| X7 | A fact read answers 5xx or times out | Retryable: the activity fails and the workflow retries inside the 2 s budget; after the third attempt the delivery is EXCEPTION | MSG-P2-001 | AC8 |
| X8 | A message fails envelope validation, or carries a type this consumer does not declare | The message is refused before any state change and routed to `.dlt` with an alert | None | BR2 |
| X9 | A role without Platform administration opens the exception queue or resends | Refused before any read or write | MSG-P4-002 | Carried by the CON story as a contract case |
| X10 | The delivery is resent while the workflow for the same event is running | Refused with 409; nothing changes and no second workflow is started | MSG-GEN-004 | BR6 |
| X11 | The P1 append refuses the key as a repeat | The answer is treated as success; the delivery is DELIVERED and the hit count rises | None | AC8; BR5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published contracts only: the P1 append, EFS and contact reads, the P3, P6, S9, S2 and P8 fact reads, the platform outbox and workflow kit, and the rwb-integration baseline. Every one of them is faked |
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
```

AC8 is the only legacy criterion this story owns, and it is copied word for word with one Given added for the mocked cross-service part: the rwb-case contract mock returns no case for the instruction's case, because rwb-case is now another service and the case lookup is a contract call. Every value of the legacy scenario is kept: the instruction event, the nonexistent case, the three retries, the empty ledger and the task for role RW-PLATADM.

The other legacy criteria are not owned here. AC1, AC6 and AC9 (the EFS contact entry, the EFS outcome list, the late EFS row) and AC3 (the ledger is one place, read through `GET /cases/{caseId}/interactions`) belong to the rwb-source-data stories of this legacy key, which own the ledger, the EFS intake rule and the interaction read. AC2 (a hand-over is recorded) is split: the CASE_ALLOCATED and CASE_TRANSFERRED entries and the holder enrichment are rwb-case's, and only the partner hand-over and partner result entries of BR2 are produced by this intake. AC4 (letter, delivery, offer and payment are recorded) is the mapping this story transports, but the ledger assertions are the P1 story's. AC5 (nothing is written twice) is proved in three places — the inbox here in TC-E2-034-05, the append-only key in P1, and the timeline in P3. AC7 (a ledger write failure loses nothing) is the transport half carried here as exception path X4 and the ledger half carried by P1. AC10 (a case with no entry) and AC11 (a case outside the reader's scope) are the timeline and the scope rules of rwb-case, rwb-source-data and rwb-access.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Event to ledger event code: InstructionIssued to HANDOVER; PartnerResultSubmitted to PARTNER_RESULT; NoticeDispatched and NoticeDelivered to LETTER; TreatmentApproved to OFFER; ProceedsMatched to PAYMENT; an EFS action row to CONTACT. The codes are kept character for character and are sent as they are | Legacy RWB-E2-034 BR1; LOV-LEDGER-EVENT |
| BR2 | The intake consumes exactly seven types on their owners' topics and publishes none of its own: `rwb.treatment.TreatmentApproved.v1`, `rwb.comms.NoticeDispatched.v1`, `rwb.comms.NoticeDelivered.v1`, `rwb.partner.InstructionIssued.v1`, `rwb.partner.PartnerResultSubmitted.v1`, `rwb.payment.ProceedsMatched.v1` and `rwb.source-data.AceDataReady.v1` | Arch v5 slides 42 and 43; DP-14 |
| BR3 | A partner hand-over has channel PORTAL and direction OUTBOUND with the holder before and after; a partner result has channel PORTAL and direction INBOUND; a notice entry has channel LETTER and carries the delivery status and the barcode as its external reference | Legacy BR2; LOV-CHANNEL; LOV-DIRECTION |
| BR4 | The contact point travels as a reference: the entry carries `contactKey` and never a number or an address; a fact that cannot be read leaves its link empty and never blocks the entry | Legacy BR5; REQ-ILG-014; CTL-11 |
| BR5 | One entry per idempotency key. The append is called before the inbox row is marked, both are idempotent on the key, and a repeat is counted rather than rejected | Legacy BR7; R-UNI-40; REQ-ILG-007 |
| BR6 | A failed append or an unresolvable case never discards the delivery: it is retried, and after the third failed attempt it is EXCEPTION with a task `RESOLVE_OUTBOX_DELIVERY` for role RW-PLATADM | Legacy BR8; FSD P2 v3 AC-EXC-P2-001-01 and T4; REQ-ILG-008 |
| BR7 | An EFS row enters the ledger only when its action code is in the EFS ledger outcome list and only for an account linked to an open case; the list and the retention classes are rows of rwb-source-data and are never copied into rwb_integration | Legacy BR3, BR6; DL29; DL26; DP-18 |
| BR8 | The EFS read step is started by AceDataReady and is not an outbox delivery; a rerun for the same business date writes only the rows not yet written, by the key `EFS:<efs_record_key>` | Legacy section 12 (EFS contact read step); EV-26 |
| BR9 | The intake writes no ledger row and reads no ledger table: the entry is created through the P1 append operation and the ledger is never queried from this service | DP-01; DP-18; ownership map ruling on `interaction` |
| BR10 | The intake publishes no business event of its own; the decision record of a resend and of an exception is written through the local library and published on `rwb.decision-record.v1` | DP-03; Arch v5 slide 42 row 08 |

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
| SY-INTGR, the rwb-integration service identity | Consumes the seven types, maps each event, calls the P1 append, the P1 EFS read and the fact reads, and moves its own deliveries (service identity, no case right) |
| RW-PLATADM, platform administrator | Reads the exception queue and resends a delivery (Platform administration, RU) |
| RW-AUDIT, internal audit | Reads the deliveries, the resend record and the run summaries (Platform administration, R) |
| rwb-source-data contract | Creates the ledger entry from the append and owns the append-only rule; it refuses a repeated key and resolves the retention class |
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
| DF-INT-001 to DF-INT-029 | interaction through the P1 append contract | event_code, channel, direction, occurred_at, source_system, case_id, contact_key, from_holder_ref, to_holder_ref, treatment_id, proceeds_id, delivery_status, external_ref, idempotency_key | Write through P1 only; no column of this table is in rwb_integration |
| DF-INT-036 | EFS contact result through the P1 EFS outcome read | contact_result | Read |
| DF-ACE-108, DF-ACE-109, DF-ACE-111, DF-ACE-114 | EFS action rows through the P1 EFS outcome read | efs_record_key, account_key, action_code, contact_at | Read |
| DF-ACE-076, DF-ACE-077 | v_ace_contact facts through the P1 contact read | contact_key, person_key | Read |
| DF-CAS-001, DF-CAS-009, DF-CAS-025, DF-CAS-026 | case facts through the rwb-case contract | id, owner_user_id, case_id, account_key | Read |
| DF-LEG-015, DF-LEG-020, DF-LEG-022 | notice facts through the rwb-comms contract | id, barcode, delivery_status | Read |
| DF-PRT-002 | partner facts through the rwb-partner contract | partner_code | Read |
| DF-TRT-001 | treatment facts through the rwb-treatment contract | id | Read |
| DF-FIN-001 | proceeds facts through the rwb-payment contract | id | Read |

The ledger fields of DF-INT-001 to DF-INT-029 are written by rwb-source-data and are listed here only to fix what the mapper sends. No ACE view is read by this service and no ACE row is stored: the EFS and contact facts come through the P1 contract and the case, notice, partner, treatment and proceeds facts come through their owners' contracts (DP-01, DP-05). The JSON field names of the command and of the fact answers are Not specified in the source documents (GAP-0664; ASM-1168); this story uses the element names of the table above and leaves the physical names to the CON story of this key.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/integration/v1`; owner rwb-integration (P2). Two operations, the exception queue surface of this slice.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/admin/outbox/deliveries` | Lists the deliveries of consumer `ledger-channels` by status, consumer, event type and date window, with the attempt count, the next attempt time, the last error code and the linked task | Platform administration R | Not applicable |
| POST | `/admin/outbox/deliveries/{deliveryId}/resend` | Sends a delivery in EXCEPTION again: status PENDING, attempt count 0, the workflow started again for the same event | Platform administration U | `Idempotency-Key`; a delivery not in EXCEPTION answers 409 |

Both operations are the re-based forms of API-P2-003 and API-P2-004 of the legacy appendix (TSD P2 v3 T-A.1), whose paths sat under the monolith base. The outbound-item operations `GET /admin/outbound-items` and `POST /admin/outbound-items/{itemId}/resend` stay with the rwb-integration baseline of RWB-P2-E1007-CON and are not declared here. The request query parameters, the response fields and the error bodies of the two operations are Not specified in the source documents (GAP-0664; ASM-1168).

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| POST | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | rwb-source-data (P1) | The `InteractionLedgerWriter` append: one ledger entry per call, create-only and idempotent on the key (ownership map: `POST /cases/{caseId}/interactions`, owner P1) | One hop, 2 s (DP-11) |
| GET | The EFS contact-outcome read of the rwb-source-data contract, for a business date | rwb-source-data (P1) | The EFS action rows of the business date for accounts on open cases (legacy `EfsContactHistory.outcomesFor`) | One hop, 2 s (DP-11) |
| GET | The contact-fact read of the rwb-source-data contract, by contact key | rwb-source-data (P1) | The contact key behind a Workbench or notice entry (legacy `ContactQuery.byKey`) | One hop, 2 s (DP-11) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | rwb-case (P3) | The case, its holder and its status (DP-06, DP-07 owner) | One hop, 2 s (DP-11) |
| GET | `/api/recovery/case/v1/cases` | rwb-case (P3) | The open case ids of an account (legacy `CaseQuery.openCaseIdsForAccount`) | One hop, 2 s (DP-11) |
| GET | `/api/recovery/comms/v1/notices/{noticeId}` | rwb-comms (P6) | The case, the contact key, the notice type, the barcode and the delivery status of a notice | One hop, 2 s (DP-11) |
| GET | The instruction-fact read of the rwb-partner contract | rwb-partner (S9) | The case and the partner code of an instruction (legacy `InstructionQuery.byId`) | One hop, 2 s (DP-11) |
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | rwb-treatment (S2) | The treatment id and its case behind an OFFER entry | One hop, 2 s (DP-11) |
| GET | The proceeds-fact read of the rwb-payment contract | rwb-payment (P8) | The proceeds id and its case behind a PAYMENT entry | One hop, 2 s (DP-11) |
| POST | `/api/recovery/access/v1/authorise` | rwb-access (P4) | The role and scope check of the two admin operations (DP-08) | One hop, 2 s (DP-11) |

The EFS outcome read, the contact read, the instruction read and the proceeds read are named by their legacy Java interfaces but have no path in the Ownership Map; their paths, query parameters and JSON field names are Not specified in the source documents (GAP-0664; ASM-1168). The case-list account filter is likewise unnamed and follows the same placeholder. The RWB-P1-E1066-CON and RWB-P1-E1067-CON published interfaces are the ones this story calls; the shape of the append command is the P1 contract's and is restated in RWB-P2-E2034-CON only.

#### 12.3 Events published

None by this service's topic. `rwb.integration.events.v1` carries FileDelivered and FileFailed from the outbound file side (Arch v5 slide 16) and this slice publishes neither. The decision record of a resend and of an exception is written by the local decision-record library, which publishes `rwb.decision-record.DecisionRecorded.v1` (EV-08) on `rwb.decision-record.v1` in the same transaction as the delivery change (DP-03, H RWB-PLT-E1027-CON).

#### 12.4 Events consumed

| Event type | Topic | Owner | Consumer element |
|---|---|---|---|
| `rwb.treatment.TreatmentApproved.v1` | `rwb.treatment.events.v1` | S2 | Inbox dedupe, then one OFFER entry |
| `rwb.comms.NoticeDispatched.v1` | `rwb.comms.events.v1` | P6 | Inbox dedupe, then one LETTER entry with delivery status SENT |
| `rwb.comms.NoticeDelivered.v1` | `rwb.comms.events.v1` | P6 | Inbox dedupe, then one LETTER entry with delivery status DELIVERED |
| `rwb.partner.InstructionIssued.v1` | `rwb.partner.events.v1` | S9 | Inbox dedupe, then one HANDOVER entry, channel PORTAL, direction OUTBOUND |
| `rwb.partner.PartnerResultSubmitted.v1` | `rwb.partner.events.v1` | S9 | Inbox dedupe, then one PARTNER_RESULT entry, channel PORTAL, direction INBOUND |
| `rwb.payment.ProceedsMatched.v1` | `rwb.payment.events.v1` | P8 | Inbox dedupe, then one PAYMENT entry linked to the proceeds |
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 | Starts EfsLedgerReadWorkflow for the EFS source; not an outbox delivery |

All seven are CloudEvents 1.0 with the envelope attributes id, source, type, specversion, time, subject, datacontenttype, keyed by the case id where a case exists. The dedupe key is the event's own business key in the form `<EV-nn>:<business key>:v1` for the six business events (`EV-10:TRT-SYN-0301:v1`, `EV-26:ALS:2026-11-10` are the documented shapes of the FSD) and `EFS:<efs_record_key>` for an EFS row. Delivery is at least once; the consumer is idempotent by key. A message without the envelope, or of a type not in this table, is routed to `.dlt` (DP-09).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| LedgerChannelIntakeWorkflow | Workflow, one execution per consumed event, workflow ID = the CloudEvents id | `rwb-integration` | Input: event type, CloudEvents id, business key, occurred time, case id, payload reference. Output: the ledger entry reference and the delivery state |
| mapChannelEvent | Activity | `rwb-integration` | Input: event type and payload. Output: one ledger entry command with the event code, channel, direction, occurred time, source system and links |
| resolveChannelFacts | Activity | `rwb-integration` | Input: the case id, notice id, instruction id, treatment id or proceeds id of the event. Output: the resolved facts; a 404 leaves a link empty, a 5xx is retryable |
| appendLedgerEntry | Activity | `rwb-integration` | Input: the entry command and the idempotency key. Output: the ledger entry reference; a repeat returns the same reference |
| parkDeliveryInException | Activity | `rwb-integration` | Input: delivery id, failure class, attempt count. Output: status EXCEPTION, task `RESOLVE_OUTBOX_DELIVERY` for RW-PLATADM, decision record |
| EfsLedgerReadWorkflow | Workflow, started by AceDataReady for the EFS source | `rwb-integration` | Input: business date, source EFS. Output: `EfsReadSummary` |
| readEfsOutcomes | Activity | `rwb-integration` | Input: business date. Output: the kept and the excluded EFS rows |
| appendEfsEntries | Activity | `rwb-integration` | Input: the kept rows. Output: the count written, one append per row with key `EFS:<efs_record_key>` |
| writeEfsReadSummary | Activity | `rwb-integration` | Input: the counts. Output: `EfsReadSummary(businessDate, rowsRead, written, excluded, notOnCase)` |

Every activity runs with the workflow kit's retry policy: initial interval 1 s, back-off 2, maximum 3 attempts, and a non-retryable classification for a 4xx of the append other than 409 (DP-10). The workflow history carries ids, codes and counts only, never a contact point or an amount.

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
| rwb-source-data WireMock — append | The P1 append contract | 201 with an entry reference; 200 with the same reference for a repeated key; 409 for a key already held; 503 and a slow answer for the fifth-attempt paths of TC-E2-034-07 |
| rwb-source-data WireMock — EFS and contact | The P1 EFS outcome read and the P1 contact read | Three EFS rows (listed, unlisted, not on a case) for business date 2026-12-14; a contact view for `PHONE:CP-SYN-0301-M`; a 404 for an unknown key |
| rwb-case WireMock | The P3 case contract | Case `RW-2026-000301` with holder "U-2001"; no case for instruction `INS-SYN-0304` (AC8); the open case ids of `ACC-SYN-0301` |
| rwb-comms WireMock | The P6 notice contract | Notice `NT-SYN-0301` with barcode "EV000000001TH" and delivery status SENT, then DELIVERED |
| rwb-partner WireMock | The S9 contract | Instruction `INS-SYN-0301` to partner `LF-SYN-01`; one partner result |
| rwb-treatment and rwb-payment WireMock | The S2 and P8 contracts | Treatment `TRT-SYN-0301`; proceeds `PRC-SYN-0301` of 5,000.00 |
| rwb-access WireMock | The P4 contract | `POST /authorise` granting and refusing Platform administration |
| Kafka stubs | The seven topics | One message per type, one duplicate, one malformed envelope, one unknown type |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 9 named paths and 3 named-by-interface reads consumed | The two admin operations provided; the P1 append, EFS, contact and authorise reads, the P3, P6, S9, S2 and P8 fact reads consumed; one hop, 2 s timeout |
| Kafka | 0 published, 7 types consumed | Six business events for one entry each and AceDataReady for the EFS read step; inbox dedupe on every one |
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
| LedgerChannelListener | Listener | Envelope validation for the seven types, inbox dedupe, workflow start per event (BR2, BR5) |
| LedgerChannelMapper | Service | One method per event type implementing BR1, BR3 and BR4; the codes are sent, never resolved, here |
| FactResolver | Client | The P3, P6, S9, S2 and P8 fact reads behind one 2 s budget with no retry on 4xx (DP-11) |
| LedgerAppendClient | Client | The P1 append and the P1 EFS and contact reads; one hop, 2 s, idempotent on the key (DP-18) |
| DeliveryTracker | Service | The `outbox_delivery` row of a consumed event: attempt count, next attempt, status, task (BR6) |
| ChannelIntakeWorkflow | Workflow | LedgerChannelIntakeWorkflow with its four activities |
| EfsContactOutcomeReader | Workflow and activities | EfsLedgerReadWorkflow: read, append, summary (BR7, BR8) |
| ExceptionQueueController | Controller | The two admin operations, their validation and their problem responses (DP-13, DP-19) |
| DecisionRecordWriter | Library client | The record of a resend and of an exception through the local library (DP-03) |
| AccessCheckClient | Client | The role and scope check of the two admin operations (DP-08) |

**Database and migrations**

- Writes `outbox_delivery`, `processed_event`, `idempotency_key` and the library table `decision_record` in schema `rwb_integration`, through the rwb-integration login (DP-02, DP-15). The login name is Not specified in the source documents (GAP-0664; ASM-1168).
- One migration in the rwb-integration sequence: `V2034_1__ledger_intake.sql` adds the partial index on `processed_event (consumer, idempotency_key)` where the inbox is read and the index on `outbox_delivery (consumer, status, next_attempt_at)` where the retry scan reads.
- No ledger column, no ledger table and no EFS reference table is created here; the six legacy columns of `interaction` and the `efs_ledger_outcome` rows are P1's migration (legacy section 13, DP-18).

**Configuration and reference data**

- Feature flag `rwb.integration.ledger-channels` in the platform flag library; off by default, on in the environments of the release. Off: the consumer acknowledges the seven types without writing, the EFS read step does not run and no delivery row moves.
- The retry intervals of a delivery and the attempt limit of three are rows of the environment configuration, not code (ASM-1170). The EFS ledger outcome list, the retention classes and the channel list are rows of rwb-source-data and are read there.
- The consumer name `ledger-channels` is kept from the legacy story as the logical consumer; its Kafka group names are deployment values of the OPS story.
- The two admin operations declare Platform administration R and U; no role name is written in code (DP-08).

**Build steps**

1. LedgerChannelListener and DeliveryTracker against the platform inbox, with one test per consumed type and the duplicate path; AC8, BR2, BR5.
2. LedgerChannelMapper, one method and one unit test per event type, with the codes of BR1 sent unchanged; BR1, BR3.
3. FactResolver over the five owner contracts and the contract fakes, with the 404 and 5xx split; BR4.
4. LedgerAppendClient over the P1 append and the two P1 reads, with the repeat answer treated as success; BR5, BR9.
5. ChannelIntakeWorkflow with its four activities and the retry policy, then the exception path and the task for RW-PLATADM; AC8, BR6.
6. EfsContactOutcomeReader as the second workflow, with the summary and the `EFS:<efs_record_key>` key; BR7, BR8.
7. ExceptionQueueController with the two admin operations, the scope check, the resend and the 409 on a running workflow; X9, X10.
8. DecisionRecordWriter on the resend and on the exception, with the rollback path; BR10.
9. The contract-fake run of every cross-service answer in isolation, so the story builds before the other services exist.
10. The migration and its indexes, then the load of the configuration rows.

**Feature switch.** `rwb.integration.ledger-channels`. On: the seven types are consumed and appended, and the EFS read step runs. Off: the deliveries are acknowledged and counted but nothing is appended and no workflow is started; the ledger of P1 is unchanged and no delivery is dated.

**Done when.** The tests in section 16 pass, a duplicate of any of the six business events writes one entry and counts one repeat, an unresolvable case ends in EXCEPTION with a task for RW-PLATADM on the third attempt, a 503 from the append loses no delivery, and the EFS read summary of a rerun is identical to the first run for the same business date.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-001 | A delivery is in the exception queue after its retries | Not specified in the source documents (GAP-0664; ASM-1168) |
| MSG-GEN-004 | The delivery is not in EXCEPTION, or a workflow runs for the same event | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-005 | A resend is accepted | Not specified in the source documents (GAP-0664; ASM-1168) |
| MSG-P4-002 | A role without Platform administration calls one of the two operations | You cannot {action} here. Your role does not include it. |

MSG-P2-001 and MSG-GEN-005 are named by the FSD and the legacy exception flows but their texts are not in the source set; the placeholder is carried until the Error and Message Standard names them. MSG-GEN-004 and MSG-P4-002 are the agreed texts and are copied unchanged.

### 15. Screens and states

SCR-09 Exception queue, served by the gateway-bff composite route (DP-19). The platform administrator filters the deliveries of consumer `ledger-channels` by status PENDING, RETRYING, DELIVERED and EXCEPTION, by consumer, by event type and by date window, and reads the attempt count, the next attempt time, the last error code and the task. A delivery in EXCEPTION offers the resend action; the row then shows PENDING with attempt count 0 and the resend time. The screen has the states Loading, Filtered, Empty and Action failed, and the resend confirmation names the delivery and the event type only. The screen fields, their layout and their masking are Not specified in the source documents (GAP-0664; ASM-1168). No screen shows a ledger entry, a contact point or an amount: the timeline on the case is SCR-04 and belongs to rwb-case.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-034-12 | Access | Component | A role without Platform administration opens the deliveries and resends; refused with MSG-P4-002 |
| TC-E2-034-01 | AC1, BR3, BR4, BR5, BR6 | End to end | One EFS action row with a promise; one Workbench call |
| TC-E2-034-02 | AC2, BR2 | End to end | One transfer; one instruction to partner LF-SYN-01 |
| TC-E2-034-03 | AC3, BR4, BR9 | End to end | Entries from EFS, Workbench and the partner portal |
| TC-E2-034-04 | AC4, BR1 | End to end | NoticeDispatched, NoticeDelivered, TreatmentApproved, ProceedsMatched |
| TC-E2-034-05 | AC5, BR7 | End to end | NoticeDispatched delivered twice with one event ID |
| TC-E2-034-06 | AC6, BR3 | End to end | Three EFS rows: listed, unlisted, no open case |
| TC-E2-034-07 | AC7, BR8 | End to end | Ledger store stopped, then restarted |
| TC-E2-034-08 | AC8 | End to end | InstructionIssued for a case that does not exist |
| TC-E2-034-09 | AC9, BR9 | End to end | EFS row processed after a later Workbench call |
| TC-E2-034-10 | AC10 | End to end | Case with no entry |
| TC-E2-034-11 | AC11 | End to end | Reader of team HP-NE with Own scope |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end, Access to Component and Resilience to NFR; no test case of this legacy key carries the Resilience level. This story runs TC-E2-034-07 (the append fails and the delivery is retried and delivered), TC-E2-034-05 (the same event delivered twice writes one entry and counts one repeat) and TC-E2-034-08 (the unknown case reaches the exception queue with the task) against its own consumer, its own inbox and its own exception queue. The other nine are carried by the P1, P3, P4 and S9 stories of this legacy key, which own the ledger, the read, the masking and the partner portal; they are listed here so that the legacy key stays complete.

### 17. Guardrails

- No business value in code: the event codes, the channels, the directions, the retry intervals and the attempt limit are rows of reference data and environment configuration; the mapper sends codes and resolves none.
- No personal data in logs, events, workflow inputs or histories: the entry carries `contactKey` and the identifiers of the case, the notice, the instruction, the treatment and the proceeds, never a number, an address or an amount.
- No read of another service's table and no ACE view: the ledger is reached only through the P1 append, the EFS and contact facts only through the P1 reads, and the case, notice, partner, treatment and proceeds facts only through their owners' contracts (DP-01, DP-05, DP-18).
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
- SMS and LINE dispatch results: RWB-E2-022, which appends through the same P1 contract.
- Proof of delivery capture from WIN and the notice period timer: RWB-E2-021.
- Retention periods and the disposal job: DL26 and JOB-17.
- The outbound file items, the WIN and debt-buyer files and the `outbound_item` resend: RWB-P2-E1007-APP and its contract.
- The Helm values, the consumer groups, the dashboards, the alerts and the runbook: RWB-P2-E2034-OPS.
