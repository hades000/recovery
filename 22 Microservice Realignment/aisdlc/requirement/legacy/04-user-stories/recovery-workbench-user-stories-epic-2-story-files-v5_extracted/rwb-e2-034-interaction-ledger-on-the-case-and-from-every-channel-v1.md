<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5.zip!RWB E2 034 Interaction ledger on the case and from every channel v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5.zip!RWB E2 034 Interaction ledger on the case and from every channel v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-034 Interaction ledger on the case and from every channel

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-034 |
| Epic | E2, release 31 December 2026 |
| Module | P2 Integration |
| Feature | FEAT-ILG-06 Bring contact outcomes into the ledger; FEAT-ILG-07 Bring dispatch outcomes into the ledger; FEAT-ILG-08 Record a hand-over in the ledger; FEAT-ILG-09 Read the ledger as a timeline on the case; FEAT-ILG-10 Set the retention class for ledger entries |
| Requirement IDs | REQ-ILG-009, REQ-ILG-010, REQ-ILG-011, REQ-ILG-012, REQ-ILG-013 |
| BRD section | Business Requirements Epic 2, section 3.2 |
| L3 process | 06 to 10 Recovery case processes; All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-027, RWB-E2-016, RWB-E1-069, RWB-E1-007, RWB-E1-066, RWB-E1-067, RWB-TE-006 |
| Status | Ready for build |

## 1. Story

As a **case owner (RW-CASEOWN)**, I want **every contact, letter, delivery, offer, payment and hand-over on the case recorded in one ledger, from the Workbench, from the EFS history ACE holds and from the partner portal**, so that **contactability is not found and then lost again**.

## 2. Business rationale

Contact outcomes from collections, letters sent through WIN and work held by partners are recorded in different systems today, so a case owner who picks up a case does not know which number answered or who held the case last. This story brings each of these into the one ledger built in Epic 1 (RWB-E1-066 and RWB-E1-067), reads the EFS history from v_ace_efs_action instead of a Workbench load, adds who held the case before and after each hand-over, gives each entry a retention class, and shows the ledger as an ordered timeline on the case. It meets REQ-ILG-009 to REQ-ILG-013. The business measure is the share of open cases whose last right-party contact is visible on the case, which today is zero for cases that came from EFS.

## 3. Preconditions

- RWB-E1-066 (ledger store and InteractionLedgerWriter), RWB-E1-067 (Workbench events into the ledger), RWB-E1-027 (decision log writer), RWB-E2-016 (case record timeline), RWB-E1-069 (read-only ACE source views) and RWB-TE-006 (outbox delivery) are done.
- v_ace_efs_action, v_ace_efs_action_code and v_ace_contact are granted SELECT to the recovery service identity (V0002).
- v_ace_efs_action carries contact_result and action_contact_status from Section B (V0003, RWB-ACE-001, DL43); the flag stays off in an environment without V0003.
- The EFS ledger outcome list (the action codes that enter the ledger, with their channel) is loaded in efs_ledger_outcome. Until the business lead names the list (DL29, option B), every action code in LOV-ACTION-CODE with a call result enters the ledger with channel CALL (assumed).
- The Retention classes reference table holds a class per ledger event code. Until Compliance sets the periods (DL26), every event code takes class "ILG-STD" (assumed).
- LOV-LEDGER-EVENT (RWB-E1-066) holds the added values PARTNER_RESULT and OFFER (addition).
- The case exists and is open; the reader holds a role with Case record R.
- Feature flag `rwb.integration.ledger-channels` is on.

## 4. Flow

1. Outbox (RWB-TE-006): delivers to consumer "ledger-channels" the events InstructionIssued, PartnerResultSubmitted, NoticeDispatched, NoticeDelivered, TreatmentApproved and ProceedsMatched.
2. LedgerChannelListener: checks the event's idempotency key through IdempotencyGuard (RWB-E1-007) and passes the event to LedgerChannelMapper.
3. LedgerChannelMapper: maps the event to one LedgerEntryCommand with event code, channel, direction, occurred time, source, holder references and links (BR1 to BR5), reading the facts it needs through the owning module's published interface.
4. EfsContactOutcomeReader (on AceDataReady, EV-26, for EFS): reads the day's EFS action rows for accounts linked to open cases from v_ace_efs_action, keeps the action codes in efs_ledger_outcome, and maps each row to a CONTACT entry with source EFS and the person_key of the row; the contact_key of a Workbench or notice entry is the one v_ace_contact holds.
5. HolderEnricher: for CaseAllocated and CaseTransferred, which RWB-E1-067 maps to CASE_ALLOCATED and CASE_TRANSFERRED, adds the holder before and after the move to the same entry.
6. RetentionClassResolver: sets the retention class from the Retention classes reference table by event code, for every entry the writer appends.
7. LedgerChannelListener: calls InteractionLedgerWriter.append for each entry inside the delivery's transaction; the writer refuses a repeated idempotency key and counts the repeat (R-UNI-40).
8. Case owner: opens the case record (SCR-03) and the timeline (SCR-04).
9. Front end: calls GET /api/recovery/v1/cases/{caseId}/interactions with the channel, actor and date filters.
10. Front end: shows the entries in case sequence order with time, channel, contact point reached (masked by role), outcome, promise, offer or payment link, holder change and source.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The same event arrives twice with the same key | One entry exists; the repeat is counted | None | AC5 |
| X2 | An EFS row has an action code that is not in efs_ledger_outcome | No entry; counted as excluded in the read summary | None | AC6 |
| X3 | An EFS row is for an account on no open case | No entry; counted as not on a case | None | AC6 |
| X4 | The ledger store cannot be written | The delivery fails and stays in the outbox for retry; an incident is raised; no entry is lost | None | AC7 |
| X5 | An event names a case that does not exist | No entry; after the retry limit the delivery goes to the exception queue with a task for the platform administrator | None | AC8 |
| X6 | An EFS row arrives after a later Workbench entry for the same case | The entry takes its own occurred time; the timeline orders by occurred time | None | AC9 |
| X7 | The case has no entry yet | Empty state on the timeline | MSG-P3-024 | AC10 |
| X8 | The reader's role does not hold Case record R | Refused with 403 | MSG-P4-002 | Access test TC-E2-034-12 |
| X9 | The case is outside the reader's scope | Refused with 404 | MSG-P4-003 | AC11 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the Epic 1 ledger writer, the outbox, the ACE views and the published events; no change to the modules that publish them |
| Negotiable | The EFS outcome list and the retention classes are data (DL29, DL26); the mapping rules are fixed here |
| Valuable | The case owner sees which number answered and who held the case, without asking EFS or the partner |
| Estimable | One listener, one mapper, one read step, six added columns and a timeline section |
| Small | Each event type is one mapping with one test |
| Testable | Each criterion below has one test with fixed synthetic events |

## 7. Acceptance criteria

```gherkin
Feature: Interaction ledger on the case and from every channel

  Background:
    Given open case "RW-2026-000301" with account "ACC-SYN-0301" and owner "U-2001"
    Given the EFS ledger outcome list holds action code "PTP" with channel CALL
    Given the retention class for every event code is "ILG-STD"

  Scenario: AC1 An interaction is recorded
    Given the ACE batch for EFS with business date 14 December 2026 holds an action row for account "ACC-SYN-0301" with action code "PTP", call result RIGHT_PARTY, contact time 14 December 2026 10:15, promise amount 12,500.00 and promise date 20 December 2026
    Given case owner "U-2001" records a call on 15 December 2026 09:30 to contact key "PHONE:CP-SYN-0301-M" with result NO_ANSWER
    When the EFS batch is complete and the call is saved
    Then the ledger holds a CONTACT entry with source EFS, channel CALL, occurred 14 December 2026 10:15, result RIGHT_PARTY, promise 12,500.00 for 20 December 2026 and retention class "ILG-STD"
    Then the ledger holds a CONTACT entry with source WORKBENCH, channel CALL, occurred 15 December 2026 09:30, contact key "PHONE:CP-SYN-0301-M" and result NO_ANSWER

  Scenario: AC2 A hand-over is recorded
    Given case "RW-2026-000301" is transferred from "U-2001" to "U-2002" on 16 December 2026 11:00
    Given instruction "INS-SYN-0301" is issued to partner "LF-SYN-01" on 17 December 2026 14:00
    When both moves complete
    Then the CASE_TRANSFERRED entry of 16 December 2026 11:00 holds from "USER:U-2001" and to "USER:U-2002"
    Then the ledger holds a HANDOVER entry with channel PORTAL, direction OUTBOUND, from "USER:U-2002", to "PARTNER:LF-SYN-01", occurred 17 December 2026 14:00

  Scenario: AC3 The ledger is one place
    Given the EFS entry of 14 December 2026, the Workbench call of 15 December 2026 and a partner result from "LF-SYN-01" entered in the partner portal on 18 December 2026 16:00
    When the case is read
    Then GET /cases/{caseId}/interactions returns the 3 entries in the order 14, 15 and 18 December 2026
    Then each entry names its source: EFS, WORKBENCH, and WORKBENCH with channel PORTAL and event code PARTNER_RESULT

  Scenario: AC4 Letter, delivery, offer and payment are recorded
    Given notice "NT-SYN-0301" is dispatched on 19 December 2026 with barcode "EV000000001TH"
    Given WIN returns delivered for it on 22 December 2026
    Given treatment "TRT-SYN-0301" is approved on 23 December 2026
    Given proceeds "PRC-SYN-0301" of 5,000.00 are matched to the case on 24 December 2026
    When the four events are processed
    Then the ledger holds a LETTER entry with delivery status SENT and external reference "EV000000001TH"
    Then a LETTER entry with delivery status DELIVERED on 22 December 2026
    Then an OFFER entry linked to "TRT-SYN-0301" and a PAYMENT entry linked to "PRC-SYN-0301"

  Scenario: AC5 Nothing is written twice
    Given event NoticeDispatched with event ID "EVT-SYN-0001" has been processed by "ledger-channels"
    When the same event is delivered again
    Then the ledger holds one entry for "EVT-SYN-0001"
    Then the hit count for that key becomes 2

  Scenario: AC6 EFS rows outside the list or outside a case are not written
    Given the EFS rows for 14 December 2026 hold 3 rows: action code "PTP" for "ACC-SYN-0301", action code "SYS" not in the outcome list for "ACC-SYN-0301", and action code "PTP" for account "ACC-SYN-0999" on no open case
    When the EFS batch is complete
    Then the ledger holds 1 new EFS entry
    Then the read summary shows 3 read, 1 written, 1 excluded by the outcome list and 1 not on a case

  Scenario: AC7 A ledger write failure loses nothing
    Given the ledger store is unavailable
    When event NoticeDispatched for "NT-SYN-0301" is delivered
    Then the system writes no entry and the delivery stays in the outbox with status RETRYING
    Then an incident is raised
    Then when the store is available the retry delivers the event and the ledger holds one LETTER entry for "NT-SYN-0301"

  Scenario: AC8 An event for an unknown case goes to the exception queue
    Given event InstructionIssued names an instruction whose case does not exist
    When the outbox has retried the delivery 3 times
    Then the system writes no entry
    Then the delivery is in the exception queue with a task for role RW-PLATADM

  Scenario: AC9 A late EFS row reads in time order
    Given the ledger holds the Workbench call of 15 December 2026 09:30
    When the EFS row with contact time 14 December 2026 10:15 is processed on 15 December 2026 at 10:00
    Then the timeline shows the EFS entry before the call

  Scenario: AC10 A case with no entry
    Given open case "RW-2026-000302" with no ledger entry
    When the case owner opens the timeline
    Then the timeline shows the empty state with message MSG-P3-024

  Scenario: AC11 A case outside the reader's scope is refused
    Given case "RW-2026-000301" is owned by "U-2002" in team "MTG-BKK"
    When case owner "U-3001" of team "HP-NE" with Own scope reads its ledger
    Then the response is 404 with message MSG-P4-003
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Event to ledger event code: InstructionIssued to HANDOVER; PartnerResultSubmitted to PARTNER_RESULT; NoticeDispatched and NoticeDelivered to LETTER; TreatmentApproved to OFFER; ProceedsMatched to PAYMENT; an EFS action row to CONTACT | events.txt EV-10, EV-14, EV-15, EV-20, EV-21, EV-25, EV-26; LOV-LEDGER-EVENT |
| BR2 | A hand-over between bank owners is the CASE_ALLOCATED or CASE_TRANSFERRED entry of RWB-E1-067, with no channel, enriched with the holder before and after; a hand-over to a partner has channel PORTAL and direction OUTBOUND; a partner result has channel PORTAL and direction INBOUND | REQ-ILG-011; LOV-CHANNEL; LOV-DIRECTION |
| BR3 | An EFS row enters the ledger only when its action code is in efs_ledger_outcome, and only for an account linked to an open case | DL29; INT-07 |
| BR4 | Entries from EFS carry source_system EFS; every other entry carries WORKBENCH, including partner portal entries, which are entered on Workbench screens | LOV-SOURCE; INT-24 |
| BR5 | The contact point is stored as a reference to v_ace_contact.contact_key; the number or address is never copied into the entry | REQ-ILG-014; CTL-11 |
| BR6 | Each entry carries the retention class of its event code from the Retention classes reference table, set independently of the decision log | REQ-ILG-013; NFR-075; DL26 |
| BR7 | One entry per idempotency key; a repeat is ignored and counted | R-UNI-40; REQ-ILG-007 |
| BR8 | A failed ledger write raises an incident and the delivery is retried; no entry is discarded | REQ-ILG-008; NFR-077 |
| BR9 | The timeline orders entries by occurred time, then by case sequence | REQ-ILG-006 |

## 9. State transitions

None. This story does not change a case status. It creates interaction records and changes the state of the "ledger-channels" outbox deliveries.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-CASEWF, case workflow module | Runs the "ledger-channels" consumer and appends entries (Case record C) |
| The recovery service identity, EFS read step | Reads v_ace_efs_action and v_ace_contact after the EFS batch (Case record C) |
| RW-CASEOWN, case owner | Reads the ledger of cases in scope (Case record R) |
| RW-TEAMMGR, RW-CONDUCT | Read the ledger of cases in scope (Case record R) |
| RW-COMPLY, Compliance and PDPA officer | Sets the retention class per event code through a reference data change (Reference data U) |
| RW-REFADM, reference data administrator | Loads the EFS ledger outcome list and the retention classes (Reference data C) |
| No approval applies | The story takes no decision |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-INT-001 to DF-INT-013 | interaction | all fields | Write |
| DF-INT-014 | interaction | event_code | Write |
| DF-INT-018 | interaction | idempotency_key | Write |
| DF-INT-028 | interaction | delivery_status | Write |
| DF-INT-029 | interaction | external_ref | Write |
| DF-INT-022 | interaction | contact_key | Write |
| DF-INT-023 | interaction | from_holder_ref | Write |
| DF-INT-024 | interaction | to_holder_ref | Write |
| DF-INT-025 | interaction | treatment_id | Write |
| DF-INT-026 | interaction | proceeds_id | Write |
| DF-INT-027 | interaction | retention_class | Write |
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-009 | recovery_case | owner_user_id | Read |
| DF-CAS-022 | recovery_case | closed_date | Read |
| DF-CAS-025 | case_account | case_id | Read |
| DF-CAS-026 | case_account | account_key | Read |
| DF-ACE-075 | v_ace_contact | contact_type | Read |
| DF-ACE-076 | v_ace_contact | contact_key | Read |
| DF-ACE-077 | v_ace_contact | person_key | Read |
| DF-ACE-108 | v_ace_efs_action | efs_record_key | Read |
| DF-ACE-109 | v_ace_efs_action | account_key | Read |
| DF-ACE-110 | v_ace_efs_action | person_key | Read |
| DF-ACE-111 | v_ace_efs_action | action_code | Read |
| DF-ACE-114 | v_ace_efs_action | contact_at | Read |
| DF-ACE-122 | v_ace_efs_action | promise_date | Read |
| DF-ACE-123 | v_ace_efs_action | promise_amount | Read |
| DF-INT-036 | v_ace_efs_action | contact_result | Read (Section B, RWB-ACE-001) |
| DF-LEG-015 | notice | id | Read |
| DF-LEG-016 | notice | case_id | Read |
| DF-LEG-020 | notice | barcode | Read |
| DF-LEG-022 | notice | delivery_status | Read |
| DF-PRT-002 | partner | partner_code | Read |
| DF-TRT-001 | treatment | id | Read |
| DF-FIN-001 | proceeds | id | Read |
| DF-ACE-002 | v_ace_account | account_code | Read |

Reads of other modules' records go through their published interfaces; the ACE rows are read through the P1 interfaces over the views, never from a public table. Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Events consumed** (outbox consumer "ledger-channels", RWB-TE-006): EV-10 TreatmentApproved, EV-14 NoticeDispatched, EV-15 NoticeDelivered, EV-20 InstructionIssued, EV-21 PartnerResultSubmitted and EV-25 ProceedsMatched. EV-02 CaseAllocated and EV-04 CaseTransferred stay with the RWB-E1-067 consumer, which this story extends with the holder fields. The EFS read step starts on EV-26 AceDataReady for the EFS source; it is not an outbox delivery. Delivery is at least once; the consumer is idempotent by key. No event is published.

**Published interfaces called**

```java
// recovery.dataengine.ledger.api, RWB-E1-066; must run in the caller's transaction
LedgerEntryRef InteractionLedgerWriter.append(LedgerEntryCommand command);
//   This story adds to LedgerEntryCommand: String contactKey, String fromHolderRef, String toHolderRef,
//   UUID treatmentId, UUID proceedsId, String retentionClass (deliveryStatus and externalRef come from RWB-E2-022)
// RWB-E1-007
boolean IdempotencyGuard.firstTime(String consumer, String idempotencyKey);
// P1 EFS data, over recovery.v_ace_efs_action (RWB-E1-069)
List<EfsContactOutcome> EfsContactHistory.outcomesFor(LocalDate businessDate);
// P1 contact facts, over recovery.v_ace_contact
Optional<ContactView> ContactQuery.byKey(String contactKey);
// P3 case facts
Optional<CaseSummary> CaseQuery.byId(UUID caseId);
List<UUID> CaseQuery.openCaseIdsForAccount(String accountKey);
// P6 notice facts
Optional<NoticeSummary> NoticeQuery.byId(UUID noticeId);   // caseId, contactKey, noticeType, barcode
// S9 instruction facts
Optional<InstructionSummary> InstructionQuery.byId(UUID instructionId); // caseId, partnerCode
```

**GET /api/recovery/v1/cases/{caseId}/interactions** (operationId getCasesCaseidInteractions, existing)

| Item | Value |
|---|---|
| Parameters used | caseId (path), channel, actor, from, to, page, size |
| Response 200 | InteractionPage of Interaction, with the fields of RWB-E1-068 and RWB-E2-022 plus contactKey, fromHolderRef, toHolderRef, treatmentId, proceedsId and retentionClass (recorded in the additions file) |
| 403 | Role lacks Case record R (MSG-P4-002) |
| 404 | Case does not exist or is outside scope (MSG-P4-003) |
| Authorization | Case record, right R; summary masked by role |
| Idempotency | Read only |

**EFS contact read step**

| Item | Value |
|---|---|
| Trigger | AceDataReady (EV-26) for the EFS source, after P1 stamps DP05 |
| Job | A step of JOB-02 after the case creation step, run under the recovery service identity |
| Input | The v_ace_efs_action rows of the business date for accounts linked to open cases |
| Output | Ledger entries; a read summary with read, written, excluded and not-on-a-case counts |
| Idempotency key | "EFS:" + efs_record_key |
| Restart | A rerun for the same business date writes only the entries not yet written |

## 13. Solution plan

**Package.** Folder `recovery/integration/ledger`, Java package `<ACE base package>.recovery.integration.ledger`, for the channel consumer and the EFS read step. The holder enrichment is a change to the RWB-E1-067 mapper in `recovery.dataengine.ledger`, reviewed by its code owners. Front end folder `src/modules/recovery/caserecord/ledger`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| LedgerChannelListener | Listener | Outbox consumer "ledger-channels" for the six events; idempotency check; calls the mapper and the writer |
| LedgerChannelMapper | Service | One method per event type implementing BR1, BR2, BR4 and BR5 |
| EfsContactOutcomeReader | Job | Read step after the EFS batch; applies BR3; writes the read summary |
| EfsLedgerOutcomeList | Rule table | Reference rows: action code, channel, in ledger; loaded by RW-REFADM (DL29) |
| HolderEnricher | Service | Adds fromHolderRef and toHolderRef to the CASE_ALLOCATED and CASE_TRANSFERRED commands of RWB-E1-067 |
| RetentionClassResolver | Service | Retention class by event code (BR6), called by InteractionLedgerWriter for every entry |
| InteractionLedgerWriter | Published interface | From RWB-E1-066; this story extends its command |
| LedgerTimelineSection | React component | The ledger section of SCR-03 and the ledger filters on SCR-04: channel, source, actor, date range |

**Database.** Migration in the P1 ledger migration folder adds to interaction: contact_key varchar(255), from_holder_ref varchar(60), to_holder_ref varchar(60), treatment_id uuid, proceeds_id uuid, retention_class varchar(10). The unique key on idempotency_key comes from RWB-E1-066; the append-only trigger tr_interaction_append_only stays in place; the index ix_interaction_case_time serves the read. No import table and no load table are created: the EFS rows are read from v_ace_efs_action.

**Configuration and reference data.** efs_ledger_outcome rows (DL29; assumed default as in section 3); Retention classes reference table (DL26; assumed "ILG-STD"); LOV-LEDGER-EVENT with the added values PARTNER_RESULT and OFFER; LOV-CHANNEL, LOV-DIRECTION, LOV-SOURCE. All loaded by RW-REFADM through the reference data service (RWB-E1-043). Consumer "ledger-channels" listed in rwb.integration.outbox.consumers (RWB-TE-006), not holding a case step, owner role RW-PLATADM.

**Build steps**

1. Add the migration for the six columns; extend LedgerEntryCommand and the Interaction schema in the API specification; regenerate types.
2. Write LedgerChannelMapper with one unit test per event type (BR1, BR2, BR4, BR5).
3. Write RetentionClassResolver against the reference data interface and call it from the writer (BR6).
4. Write LedgerChannelListener with the idempotency check and the failure path that fails the delivery and raises an incident (AC5, AC7, AC8).
5. Write HolderEnricher in the RWB-E1-067 mapper (AC2).
6. Write EfsContactOutcomeReader as a step after the EFS batch, reading v_ace_efs_action and v_ace_contact, with the read summary (AC1, AC6, AC9).
7. Add the ledger section to SCR-03 and the filters to SCR-04 with the empty state (AC3, AC10); run the access and scope tests (AC11).

**Feature flag.** `rwb.integration.ledger-channels`. Off: the consumer acknowledges the six events without writing, the EFS read step does not run and the holder fields stay empty; the Epic 1 ledger is unchanged.

**Done when.** The tests in section 16 pass; a case with 500 entries reads its first page in under 2 seconds (NFR-070).

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-024 | The case has no ledger entry (new) | No interactions are recorded on this case yet. |
| MSG-P4-002 | Role lacks Case record R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the reader's scope | This case is not in your scope. |

Thai text for each message follows decision DL10.

## 15. Screens and states

SCR-03 Case record, states Loading, Read only, Editable and On hold: the ledger section shows the latest 20 entries. SCR-04 Case timeline, states Loading and Filtered: the case owner filters by channel, source, actor and date range and reads each entry's time, channel, contact point (masked by role), outcome, promise, linked offer or payment, delivery status, holder change and source. The Empty state shows MSG-P3-024.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-034-01 | AC1, BR3, BR4, BR5, BR6 | System | One EFS action row with a promise; one Workbench call |
| TC-E2-034-02 | AC2, BR2 | System | One transfer; one instruction to partner LF-SYN-01 |
| TC-E2-034-03 | AC3, BR4, BR9 | System | Entries from EFS, Workbench and the partner portal |
| TC-E2-034-04 | AC4, BR1 | System | NoticeDispatched, NoticeDelivered, TreatmentApproved, ProceedsMatched |
| TC-E2-034-05 | AC5, BR7 | System | NoticeDispatched delivered twice with one event ID |
| TC-E2-034-06 | AC6, BR3 | System | Three EFS rows: listed, unlisted, no open case |
| TC-E2-034-07 | AC7, BR8 | System | Ledger store stopped, then restarted |
| TC-E2-034-08 | AC8 | System | InstructionIssued for a case that does not exist |
| TC-E2-034-09 | AC9, BR9 | System | EFS row processed after a later Workbench call |
| TC-E2-034-10 | AC10 | System | Case with no entry |
| TC-E2-034-11 | AC11 | System | Reader of team HP-NE with Own scope |
| TC-E2-034-12 | Access | Access | RW-REFADM reads the ledger; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the EFS outcome list, event codes, channels and retention classes are reference data.
- No personal data in logs, tests or prompts; the contact point is a reference and the summary is masked by role.
- No read of another module's tables: case, notice, instruction, treatment, proceeds and EFS facts come through published interfaces; the ACE rows come through the P1 interfaces over the views (boundary rule, RWB-E1-069).
- The ledger is append only; the story never updates or deletes an entry.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ILG-009 | Contact outcomes from collections reach the ledger | Business Requirements Epic 2, section 3.2 | FEAT-ILG-06 | 06 to 10 Recovery case processes | R-UNI-40 | TC-E2-034-01, TC-E2-034-06, TC-E2-034-09 |
| REQ-ILG-010 | Dispatched letters write their result, including proof of delivery | Business Requirements Epic 2, section 3.2 | FEAT-ILG-07 | 06 to 10 Recovery case processes | R-UNI-40 | TC-E2-034-04, TC-E2-034-05, TC-E2-034-07 |
| REQ-ILG-011 | A hand-over names who held the case, who holds it now and when | Business Requirements Epic 2, section 3.2 | FEAT-ILG-08 | 06 to 10 Recovery case processes | None | TC-E2-034-02, TC-E2-034-08 |
| REQ-ILG-012 | The case record view shows the ledger as an ordered timeline | Business Requirements Epic 2, section 3.2 | FEAT-ILG-09 | 06 to 10 Recovery case processes | None | TC-E2-034-03, TC-E2-034-10, TC-E2-034-11, TC-E2-034-12 |
| REQ-ILG-013 | Ledger entries carry their own retention class | Business Requirements Epic 2, section 3.2 | FEAT-ILG-10 | All recovery processes | None | TC-E2-034-01 |

## 19. Out of scope

- Contact and promise history attached at case creation: RWB-E2-001.
- SMS and LINE dispatch results: RWB-E2-022, which writes them through the same InteractionLedgerWriter.
- Proof of delivery capture from WIN and the notice period timer: RWB-E2-021.
- Ledger entries for Workbench actions such as creation, allocation and decisions: RWB-E1-067.
- Retention periods and disposal of ledger entries: DL26 and the retention job JOB-17.
- Masking rules by role: RWB-E1-037.
