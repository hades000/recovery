# RWB-ITG-E2034-ITG Interaction ledger on the case and from every channel

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2034-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-034 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP08, DP09, DP10, DP11, DP13, DP15, DP18, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P3-E2016-APP, RWB-P1-E1069-APP, RWB-P1-E1066-APP, RWB-P1-E1067-APP, RWB-P2-E2034-APP, RWB-S9-E2034-APP, RWB-P3-E2034-APP, RWB-P4-E2034-APP, RWB-P1-E2034-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-ILG-009, REQ-ILG-010, REQ-ILG-011, REQ-ILG-012, REQ-ILG-013, REQ-ILG-014, REQ-ILG-007, REQ-ILG-008, REQ-ILG-006) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-034 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **member of the integration and QA team**, I want **a repeatable cross-service harness that drives the interaction ledger from the case, from the EFS history ACE holds and from the partner portal through gateway-bff, rwb-source-data, rwb-integration, rwb-case, rwb-access and rwb-partner and writes one evidence report per run**, so that **a contact, a letter, a delivery, an offer, a payment and a hand-over are proved to land in one ledger, to be read as one ordered timeline, to be written once, and to be refused or excluded as the legacy story defined — across services, on Day 1 and on every release after**.

This story is the wave 2 integration harness for the legacy key. It builds no production screen, endpoint, table, workflow or schedule and it owns no table. The ledger itself, the channel listener, the mapper, the EFS read step and the timeline are owned by the app stories of this legacy key: RWB-P1-E2034-APP (the ledger store and the ledger read), RWB-P2-E2034-APP (the channel listener, the mapper and the EFS intake rule), RWB-P3-E2034-APP (the timeline on the case record), RWB-P4-E2034-APP (the rights and scope check) and RWB-S9-E2034-APP (the partner result). The harness builds the runner, the fakes, the seeds and the evidence, and it owns the ten acceptance criteria listed in section 7. The criteria of AC8 stay with RWB-P2-E2034-APP.

### 2. Business rationale

Contact outcomes from collections, letters sent through WIN and work held by partners are recorded in different systems today, so a case owner who picks up a case does not know which number answered or who held the case last. The legacy story brought each of these into the one ledger built in Epic 1, read the EFS history from the ACE views instead of a Workbench load, added who held the case before and after each hand-over, gave each entry a retention class and showed the ledger as an ordered timeline on the case. In the target architecture that one journey is served by five services: rwb-source-data owns the ledger and reads ACE; rwb-integration owns the channel listener and the intake rule; rwb-case owns the case facts and the timeline; rwb-access answers the rights and scope check; rwb-partner holds the hand-over and the partner result. A defect at any seam — an event mapped to the wrong event code, an EFS row outside the outcome list, a duplicated delivery, a retention class taken from the decision log, a refusal that returns data — would only appear with a live case, unless the journey is exercised across the services as one flow.

This story is that exercise. It runs the ledger journey from gateway-bff through the fakes and then through the real services as their app stories land, reproduces every exclusion and refusal the legacy story defined in the same run, and attaches one evidence report per run keyed by story and business date, so the ledger can be shown to hold before the wave is accepted and after every change. It meets REQ-ILG-006, REQ-ILG-007, REQ-ILG-008, REQ-ILG-009, REQ-ILG-010, REQ-ILG-011, REQ-ILG-012, REQ-ILG-013 and REQ-ILG-014 at the integration level, and it leaves every business rule, every screen behaviour and every table with the owning stories.

### 3. Preconditions

- The nine I stories are published and deployed in the SIT environment as they land: RWB-P1-E2034-APP (the ledger store, the append and the ledger read), RWB-P1-E1066-APP (the ledger writer and its command), RWB-P1-E1067-APP (the Workbench events and the holder fields), RWB-P1-E1069-APP (the read-only ACE view contract), RWB-P2-E2034-APP (the channel listener, the mapper and the EFS intake rule), RWB-P3-E2034-APP (the timeline and the case-record section), RWB-P3-E2016-APP (the case record and its facts), RWB-P4-E2034-APP (the rights and scope check) and RWB-S9-E2034-APP (the partner result).
- gateway-bff is deployed with the composite case-record route of DP-19 available, so the ledger section is read as one gateway answer and not by the browser calling each service. The composite route path and its merge order, the harness environment, its seeding and its evidence format and retention are Not specified in the source documents (GAP-0416; ASM-0591).
- The contract fakes of §12.8 are published from the owning services' OpenAPI documents, so the harness runs green from Day 1 before any I story lands.
- The synthetic seeds of the legacy story exist: open case "RW-2026-000301" with account "ACC-SYN-0301" and owner "U-2001"; the EFS ledger outcome list holds action code "PTP" with channel CALL; the retention class for every event code is "ILG-STD"; the EFS batch for business date 14 December 2026 holds an action row for "ACC-SYN-0301" with action code "PTP", call result RIGHT_PARTY, contact time 14 December 2026 10:15, promise amount 12,500.00 and promise date 20 December 2026.
- The reference rows and parameters the journey reads are loaded by their owners through their contracts: LOV-LEDGER-EVENT with PARTNER_RESULT and OFFER, LOV-CHANNEL, LOV-DIRECTION, LOV-SOURCE, the EFS ledger outcome list and the retention classes; the harness holds no copy of any of them.
- The partner "LF-SYN-01", the notice "NT-SYN-0301" with barcode "EV000000001TH", the treatment "TRT-SYN-0301" and the proceeds "PRC-SYN-0301" of 5,000.00 are seeded through the S9, P6, S2 and P8 contracts or their fakes, and the case "RW-2026-000302" with no ledger entry and the case of team "MTG-BKK" owned by "U-2002" exist for the empty and out-of-scope cases.
- Feature `rwb.integration.ledger-channels` is on in the harness environment, so the listener and the EFS read step write; the harness reads the flag through the platform library and asserts the off state does not write.
- No build dependency: the harness starts on Day 1 against the fakes, and each fake is replaced by the real service as its I story lands.

### 4. Flow

1. Harness: starts a run for the story and the business date, takes the run lock, and records the build under test, the pack version and the fake or real mode of each of the owning services it touches.
2. Harness: seeds the run through the contract of each owning service, or through the fake in fake mode — the case "RW-2026-000301" with "ACC-SYN-0301" and owner "U-2001", the reference rows of the outcome list and the retention classes, the EFS batch rows of 14 December 2026, the partner "LF-SYN-01", the notice "NT-SYN-0301", the treatment "TRT-SYN-0301" and the proceeds "PRC-SYN-0301".
3. Harness: asserts the business date is ready through `GET /api/recovery/source-data/v1/data-products/freshness` and drives the Workbench call of 15 December 2026 09:30 to contact key "PHONE:CP-SYN-0301-M" with result NO_ANSWER through the append on the ledger, then reads the ledger through `GET /api/recovery/source-data/v1/cases/{caseId}/interactions` and asserts the two CONTACT entries of AC1 with their source, channel, occurred time, result, promise amount and date, and retention class "ILG-STD".
4. Harness: drives the transfer of "RW-2026-000301" from "U-2001" to "U-2002" on 16 December 2026 11:00 and the instruction "INS-SYN-0301" issued to "LF-SYN-01" on 17 December 2026 14:00, then asserts the holder before and after on the CASE_TRANSFERRED entry and the HANDOVER entry with channel PORTAL and direction OUTBOUND.
5. Harness: enters the partner result of "LF-SYN-01" in the partner portal on 18 December 2026 16:00 through the S9 contract and asserts the three entries in the order 14, 15 and 18 December 2026, each naming its source.
6. Harness: drives the four notice, treatment and payment events of 19 to 24 December 2026 through their owning contracts and asserts the LETTER entries with delivery status SENT and external reference "EV000000001TH" and DELIVERED on 22 December 2026, the OFFER entry linked to "TRT-SYN-0301" and the PAYMENT entry linked to "PRC-SYN-0301".
7. Harness: replays the event NoticeDispatched with event ID "EVT-SYN-0001" into the channel listener and asserts one entry for "EVT-SYN-0001" and a hit count of 2 for that key.
8. Harness: seeds the three EFS rows of 14 December 2026 — "PTP" for "ACC-SYN-0301", "SYS" not in the outcome list and "PTP" for "ACC-SYN-0999" on no open case — and asserts one new EFS entry and the read summary of 3 read, 1 written, 1 excluded by the outcome list and 1 not on a case.
9. Harness: makes the ledger store unavailable through the fake, delivers NoticeDispatched for "NT-SYN-0301", asserts no entry, the delivery in RETRYING and the incident, then returns the store and asserts one LETTER entry for "NT-SYN-0301" after the retry.
10. Harness: replays the late EFS row of contact time 14 December 2026 10:15 after the Workbench call and asserts the timeline order, opens the timeline of "RW-2026-000302" with no entry and asserts MSG-P3-024, and reads the ledger of the case owned by "U-2002" in team "MTG-BKK" as "U-3001" of team "HP-NE" with Own scope and asserts 404 with MSG-P4-003.
11. Harness: drives the exception of AC8 inside the same run — an InstructionIssued naming an instruction whose case does not exist, retried three times — and records it as cited, not as a criterion of this story.
12. Harness: publishes the evidence report keyed by story id and business date with one row per criterion, the seam each row exercised, the service or fake that answered, the entry or summary observed and the pass or fail result; the evidence format and its retention are Not specified in the source documents (GAP-0416; ASM-0591).
13. Harness: releases the run lock and, on any failed criterion, fails the run and names the criterion, the seam and the observed value.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | Covered by |
|---|---|---|---|---|
| X1 | The same event arrives twice with the same key | One entry exists; the repeat is counted as a hit | None | AC5 |
| X2 | An EFS row has an action code that is not in the outcome list | No entry; counted as excluded in the read summary | None | AC6 |
| X3 | An EFS row is for an account on no open case | No entry; counted as not on a case | None | AC6 |
| X4 | The ledger store cannot be written | No entry; the delivery stays RETRYING; an incident is raised; the retry writes one entry | None | AC7 |
| X5 | An event names a case that does not exist | No entry; after the retry limit the delivery is in the exception queue with a task for role RW-PLATADM | None | AC8 |
| X6 | An EFS row arrives after a later Workbench entry for the same case | The entry takes its own occurred time; the timeline orders by occurred time | None | AC9 |
| X7 | The case has no entry yet | Empty state on the timeline | MSG-P3-024 | AC10 |
| X8 | The reader's role does not hold Case record R | Refused; no entry returned | MSG-P4-002 | AC11; TC-E2-034-12-ITG |
| X9 | The case is outside the reader's scope | Refused with 404; no entry returned | MSG-P4-003 | AC11 |

X5 is driven inside the same run but AC8 is owned by RWB-P2-E2034-APP; the harness asserts the same seam and does not claim the criterion.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs on its own once the nine I stories are deployed; until then it runs against the §12.8 fakes, with no work order inside another team's lane |
| Negotiable | The seeds, the fakes and the assertions are configuration and data; the criteria are the legacy ones |
| Valuable | The ledger is proved to be one place across five services and the EFS history, with the exclusions and refusals the business asked for |
| Estimable | One runner, one fake pack, one seed set, one evidence publisher and one gate |
| Small | Fits in one iteration with the owning stories' contract tests |
| Testable | Each of the twelve `-ITG` test cases of section 16 is one run of the harness and one row of the evidence report |

### 7. Acceptance criteria

```gherkin
Feature: Interaction ledger on the case and from every channel

  Background:
    Given open case "RW-2026-000301" with account "ACC-SYN-0301" and owner "U-2001"
    Given the EFS ledger outcome list holds action code "PTP" with channel CALL
    Given the retention class for every event code is "ILG-STD"

  Scenario: AC1 An interaction is recorded (legacy RWB-E2-034 AC1)
    Given the ACE batch for EFS with business date 14 December 2026 holds an action row for account "ACC-SYN-0301" with action code "PTP", call result RIGHT_PARTY, contact time 14 December 2026 10:15, promise amount 12,500.00 and promise date 20 December 2026
    Given case owner "U-2001" records a call on 15 December 2026 09:30 to contact key "PHONE:CP-SYN-0301-M" with result NO_ANSWER
    When the EFS batch is complete and the call is saved
    Then the ledger holds a CONTACT entry with source EFS, channel CALL, occurred 14 December 2026 10:15, result RIGHT_PARTY, promise 12,500.00 for 20 December 2026 and retention class "ILG-STD"
    Then the ledger holds a CONTACT entry with source WORKBENCH, channel CALL, occurred 15 December 2026 09:30, contact key "PHONE:CP-SYN-0301-M" and result NO_ANSWER

  Scenario: AC2 A hand-over is recorded (legacy RWB-E2-034 AC2)
    Given case "RW-2026-000301" is transferred from "U-2001" to "U-2002" on 16 December 2026 11:00
    Given instruction "INS-SYN-0301" is issued to partner "LF-SYN-01" on 17 December 2026 14:00
    When both moves complete
    Then the CASE_TRANSFERRED entry of 16 December 2026 11:00 holds from "USER:U-2001" and to "USER:U-2002"
    Then the ledger holds a HANDOVER entry with channel PORTAL, direction OUTBOUND, from "USER:U-2002", to "PARTNER:LF-SYN-01", occurred 17 December 2026 14:00

  Scenario: AC3 The ledger is one place (legacy RWB-E2-034 AC3)
    Given the EFS entry of 14 December 2026, the Workbench call of 15 December 2026 and a partner result from "LF-SYN-01" entered in the partner portal on 18 December 2026 16:00
    When the case is read
    Then GET /cases/{caseId}/interactions returns the 3 entries in the order 14, 15 and 18 December 2026
    Then each entry names its source: EFS, WORKBENCH, and WORKBENCH with channel PORTAL and event code PARTNER_RESULT

  Scenario: AC4 Letter, delivery, offer and payment are recorded (legacy RWB-E2-034 AC4)
    Given notice "NT-SYN-0301" is dispatched on 19 December 2026 with barcode "EV000000001TH"
    Given WIN returns delivered for it on 22 December 2026
    Given treatment "TRT-SYN-0301" is approved on 23 December 2026
    Given proceeds "PRC-SYN-0301" of 5,000.00 are matched to the case on 24 December 2026
    When the four events are processed
    Then the ledger holds a LETTER entry with delivery status SENT and external reference "EV000000001TH"
    Then a LETTER entry with delivery status DELIVERED on 22 December 2026
    Then an OFFER entry linked to "TRT-SYN-0301" and a PAYMENT entry linked to "PRC-SYN-0301"

  Scenario: AC5 Nothing is written twice (legacy RWB-E2-034 AC5)
    Given event NoticeDispatched with event ID "EVT-SYN-0001" has been processed by "ledger-channels"
    When the same event is delivered again
    Then the ledger holds one entry for "EVT-SYN-0001"
    Then the hit count for that key becomes 2

  Scenario: AC6 EFS rows outside the list or outside a case are not written (legacy RWB-E2-034 AC6)
    Given the EFS rows for 14 December 2026 hold 3 rows: action code "PTP" for "ACC-SYN-0301", action code "SYS" not in the outcome list for "ACC-SYN-0301", and action code "PTP" for account "ACC-SYN-0999" on no open case
    When the EFS batch is complete
    Then the ledger holds 1 new EFS entry
    Then the read summary shows 3 read, 1 written, 1 excluded by the outcome list and 1 not on a case

  Scenario: AC7 A ledger write failure loses nothing (legacy RWB-E2-034 AC7)
    Given the ledger store is unavailable
    When event NoticeDispatched for "NT-SYN-0301" is delivered
    Then the system writes no entry and the delivery stays in the outbox with status RETRYING
    Then an incident is raised
    Then when the store is available the retry delivers the event and the ledger holds one LETTER entry for "NT-SYN-0301"

  Scenario: AC9 A late EFS row reads in time order (legacy RWB-E2-034 AC9)
    Given the ledger holds the Workbench call of 15 December 2026 09:30
    When the EFS row with contact time 14 December 2026 10:15 is processed on 15 December 2026 at 10:00
    Then the timeline shows the EFS entry before the call

  Scenario: AC10 A case with no entry (legacy RWB-E2-034 AC10)
    Given open case "RW-2026-000302" with no ledger entry
    When the case owner opens the timeline
    Then the timeline shows the empty state with message MSG-P3-024

  Scenario: AC11 A case outside the reader's scope is refused (legacy RWB-E2-034 AC11)
    Given case "RW-2026-000301" is owned by "U-2002" in team "MTG-BKK"
    When case owner "U-3001" of team "HP-NE" with Own scope reads its ledger
    Then the response is 404 with message MSG-P4-003
```

AC1 to AC7 and AC9 to AC11 are the legacy criteria owned by this story and are copied word for word from RWB-E2-034 with the origin tag on the scenario line. AC8 stays with RWB-P2-E2034-APP and is not restated.

### 8. Business rules

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

The harness asserts these nine rules against the owning services and the published contracts; it does not re-implement them, and no BR row is changed by this story.

### 9. State transitions

None. This story changes no case status and no case state; it reads and drives records only, and the harness adds no transition of its own. The facts below are caused by the owning services and are observed and asserted by the harness.

| Observed fact | Caused by | Asserted as |
|---|---|---|
| EFS contact row written to the ledger | rwb-source-data EFS contact read step after AceDataReady | A CONTACT entry with source EFS and retention class "ILG-STD" (TC-E2-034-01-ITG) |
| Workbench call written to the ledger | rwb-source-data ledger append through the P1 and P2 contracts | A CONTACT entry with source WORKBENCH (TC-E2-034-01-ITG) |
| Case transferred between bank owners | rwb-case transfer | The CASE_TRANSFERRED entry with the holder before and after (TC-E2-034-02-ITG) |
| Instruction issued to a partner | rwb-partner instruction workflow | A HANDOVER entry with channel PORTAL (TC-E2-034-02-ITG) |
| Partner result submitted | rwb-partner result endpoint | A PARTNER_RESULT entry with channel PORTAL and direction INBOUND (TC-E2-034-03-ITG) |
| Notice dispatched and delivered | rwb-comms notice workflow | LETTER entries with SENT and DELIVERED (TC-E2-034-04-ITG) |
| Treatment approved | rwb-treatment approval | An OFFER entry linked to the treatment (TC-E2-034-04-ITG) |
| Proceeds matched | rwb-payment matching | A PAYMENT entry linked to the proceeds (TC-E2-034-04-ITG) |
| Delivery stuck in RETRYING | The outbox library | No entry, then one entry after the retry (TC-E2-034-07-ITG) |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-CASEWF, case workflow module | Runs the "ledger-channels" consumer and appends entries (Case record C); driven and asserted by the harness |
| The recovery service identity, EFS read step | Reads the ACE views after the EFS batch (Case record C); driven and asserted by the harness |
| RW-CASEOWN, case owner | Reads the ledger of cases in scope (Case record R); the synthetic user the harness drives |
| RW-TEAMMGR, RW-CONDUCT | Read the ledger of cases in scope (Case record R) |
| RW-COMPLY, Compliance and PDPA officer | Sets the retention class per event code through a reference data change (Reference data U) |
| RW-REFADM, reference data administrator | Loads the EFS ledger outcome list and the retention classes (Reference data C) |
| RW-PLATADM, platform administrator | Receives the exception-queue task of the cited AC8 |
| QA lead | Owns the harness pack, the seeds, the evidence format and the gate |
| Integration lead | Owns the fake pack, the run of record and the replacement of each fake by its I story |
| Platform edge owner | Owns the gateway-bff composite case-record route in SIT and UAT |
| No approval applies | The story takes no decision and the harness asserts the decisions of the owning stories |

### 11. Data

The harness owns no table (DP-01, DP-18). It seeds and reads the fields below through the owning services' contracts and asserts them; the field IDs are those of the Logical Data Model and Data Dictionary.

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-INT-001 to DF-INT-013 | interaction | all fields | Read through the P1 contract |
| DF-INT-014 | interaction | event_code | Read through the P1 contract |
| DF-INT-018 | interaction | idempotency_key | Read through the P1 contract |
| DF-INT-028 | interaction | delivery_status | Read through the P1 contract |
| DF-INT-029 | interaction | external_ref | Read through the P1 contract |
| DF-INT-022 | interaction | contact_key | Read through the P1 contract |
| DF-INT-023 | interaction | from_holder_ref | Read through the P1 contract |
| DF-INT-024 | interaction | to_holder_ref | Read through the P1 contract |
| DF-INT-025 | interaction | treatment_id | Read through the P1 contract |
| DF-INT-026 | interaction | proceeds_id | Read through the P1 contract |
| DF-INT-027 | interaction | retention_class | Read through the P1 contract |
| DF-CAS-001 | recovery_case | id | Read through the P3 contract |
| DF-CAS-009 | recovery_case | owner_user_id | Read through the P3 contract |
| DF-CAS-022 | recovery_case | closed_date | Read through the P3 contract |
| DF-CAS-025 | case_account | case_id | Read through the P3 contract |
| DF-CAS-026 | case_account | account_key | Read through the P3 contract |
| DF-ACE-075 | v_ace_contact | contact_type | Read by the P1 step, asserted on the entry |
| DF-ACE-076 | v_ace_contact | contact_key | Read by the P1 step, asserted on the entry |
| DF-ACE-077 | v_ace_contact | person_key | Read by the P1 step, asserted on the entry |
| DF-ACE-108 | v_ace_efs_action | efs_record_key | Read by the P1 step, asserted on the entry |
| DF-ACE-109 | v_ace_efs_action | account_key | Read by the P1 step, asserted on the entry |
| DF-ACE-110 | v_ace_efs_action | person_key | Read by the P1 step, asserted on the entry |
| DF-ACE-111 | v_ace_efs_action | action_code | Read by the P1 step, asserted on the entry |
| DF-ACE-114 | v_ace_efs_action | contact_at | Read by the P1 step, asserted on the entry |
| DF-ACE-122 | v_ace_efs_action | promise_date | Read by the P1 step, asserted on the entry |
| DF-ACE-123 | v_ace_efs_action | promise_amount | Read by the P1 step, asserted on the entry |
| DF-INT-036 | v_ace_efs_action | contact_result | Read by the P1 step, asserted on the entry (Section B, RWB-ACE-001) |
| DF-LEG-015 | notice | id | Read through the P6 contract |
| DF-LEG-016 | notice | case_id | Read through the P6 contract |
| DF-LEG-020 | notice | barcode | Read through the P6 contract |
| DF-LEG-022 | notice | delivery_status | Read through the P6 contract |
| DF-PRT-002 | partner | partner_code | Read through the S9 contract |
| DF-TRT-001 | treatment | id | Read through the S2 contract |
| DF-FIN-001 | proceeds | id | Read through the P8 contract |
| DF-ACE-002 | v_ace_account | account_code | Read by the P1 step, asserted on the entry |

Test data is synthetic. No production case, party, contact point or EFS row is used, and no personal data is written to a run report.

### 12. Contract

#### 12.1 REST operations provided

None. The harness provides no REST operation.

#### 12.2 REST operations consumed

One hop per call, no chaining; the 2 s timeout and the breaker per downstream of DP-11 apply to every row.

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data | The ledger read of a case with the channel, actor, date, page and size parameters (AC3, AC9, AC10, AC11) |
| POST | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data | The append the harness drives for the Workbench call of AC1 and for the refusals of X8 (AC1, AC11) |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | The business date readiness the EFS contact read step follows (AC1, AC6, AC9) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case facts: id, owner, team and accounts the ledger is read for (AC2, AC10, AC11) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The role, scope and rights the reader holds, asserted on AC11 and on the access case |
| GET | `/api/recovery/partner/v1/partners` | S9 rwb-partner | The partner facts behind the hand-over and the partner result (AC2, AC3) |
| POST | `/api/recovery/partner/v1/partner/instructions/{instructionId}/results` | S9 rwb-partner | The partner result entered in the partner portal on 18 December 2026 16:00 (AC3) |
| GET | `/api/recovery/comms/v1/notices/{noticeId}` | P6 rwb-comms | The notice, its barcode and its delivery status (AC4, AC7) |
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | The approved treatment the OFFER entry links to (AC4) |
| GET | `/api/recovery/payment/v1/proceeds` | P8 rwb-payment | The proceeds matched to the case (AC4) |

The composite case-record route the ledger section is read through is gateway-bff (DP-19), owned by the platform edge story RWB-PLT-N001-CON. Its path and merge order are Not specified in the source documents (GAP-0416; ASM-0591).

#### 12.3 Events published

None. The harness publishes no Kafka event.

#### 12.4 Events consumed

| Event | Topic | Owner | What the harness asserts |
|---|---|---|---|
| rwb.source-data.AceDataReady.v1 | rwb.source-data.events.v1 | P1 rwb-source-data | The business date is ready and the EFS contact read step has run; the entries of AC1 and AC6 exist and the read summary is published for the run (AC1, AC6, AC9) |
| rwb.case.CaseAllocated.v1 | rwb.case.events.v1 | P3 rwb-case | The CASE_ALLOCATED entry keeps its holder before and after and carries no channel (AC2) |
| rwb.case.CaseTransferred.v1 | rwb.case.events.v1 | P3 rwb-case | The CASE_TRANSFERRED entry of 16 December 2026 11:00 carries from "USER:U-2001" and to "USER:U-2002" (AC2) |
| rwb.partner.InstructionIssued.v1 | rwb.partner.events.v1 | S9 rwb-partner | The HANDOVER entry with channel PORTAL, direction OUTBOUND and occurred 17 December 2026 14:00 (AC2) |
| rwb.partner.PartnerResultSubmitted.v1 | rwb.partner.events.v1 | S9 rwb-partner | The PARTNER_RESULT entry with channel PORTAL and direction INBOUND, in the third position of the timeline (AC3) |
| rwb.comms.NoticeDispatched.v1 | rwb.comms.events.v1 | P6 rwb-comms | The LETTER entry with delivery status SENT and external reference "EV000000001TH" (AC4, AC5, AC7) |
| rwb.comms.NoticeDelivered.v1 | rwb.comms.events.v1 | P6 rwb-comms | The LETTER entry with delivery status DELIVERED on 22 December 2026 (AC4) |
| rwb.treatment.TreatmentApproved.v1 | rwb.treatment.events.v1 | S2 rwb-treatment | The OFFER entry linked to "TRT-SYN-0301" (AC4) |
| rwb.payment.ProceedsMatched.v1 | rwb.payment.events.v1 | P8 rwb-payment | The PAYMENT entry linked to "PRC-SYN-0301" (AC4) |
| rwb.decision-record.DecisionRecorded.v1 | rwb.decision-record.v1 | All 19 services; P7 rwb-decision seals the central ledger | The retention class of each entry is set from the reference data and not from the decision record (BR6) |

The harness consumes these topics as a test consumer with its own group and asserts the entries through the P1 ledger read; it holds no inbox table of its own, gets no production record, and publishes nothing.

#### 12.5 Workflows and activities

None added. The harness starts no Temporal workflow, calls no activity and uses no queue `rwb-source-data`. The EFS contact read step it watches is an event-started step of rwb-source-data on AceDataReady (DP-10), owned by RWB-P1-E2034-APP and RWB-P2-E2034-APP; the case-creation step of JOB-02 stays with rwb-case and is not driven by this harness.

#### 12.6 Schedules

None. The harness run is started by the test pipeline, not by a Temporal Schedule and not by Airflow, and it creates no Schedule.

#### 12.7 Tables owned

None. The harness owns no table and no schema (DP-01); it seeds and reads through the owning services' contracts only, and the ledger table `interaction` in the schema `rwb_source_data` is owned by RWB-P1-E2034-APP.

#### 12.8 Contract fakes

| Fake | Serves | Used by |
|---|---|---|
| rwb-source-data (WireMock, from its OpenAPI) | `GET` and `POST /api/recovery/source-data/v1/cases/{caseId}/interactions` and `GET /api/recovery/source-data/v1/data-products/freshness`, with the ledger fixtures of "RW-2026-000301", the empty case "RW-2026-000302", the 3-entry order of 14, 15 and 18 December 2026, the 1-entry answer of AC6 and the read summary of 3 read, 1 written, 1 excluded and 1 not on a case | AC1, AC3, AC6, AC9, AC10; every ledger read of the run |
| rwb-integration (WireMock, from its OpenAPI) | The channel listener seam: the six consumed events replayed into "ledger-channels", the duplicate of "EVT-SYN-0001" with a hit count of 2, and the RETRYING delivery of "NT-SYN-0301" while the store is unavailable | AC4, AC5, AC7 |
| rwb-case (WireMock, from its OpenAPI) | `GET /api/recovery/case/v1/cases/{caseId}` with the owner "U-2001", the team "MTG-BKK", the case of "U-2002" and the accounts "ACC-SYN-0301" and "ACC-SYN-0999" | AC1, AC2, AC6, AC11 |
| rwb-access (WireMock, from its OpenAPI) | `GET /api/recovery/access/v1/me/session` for RW-CASEOWN in scope, for RW-REFADM without Case record R, and for "U-3001" of team "HP-NE" with Own scope | AC11; TC-E2-034-12-ITG |
| rwb-partner (WireMock, from its OpenAPI) | `GET /api/recovery/partner/v1/partners` and `POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results` with partner "LF-SYN-01" and the instruction "INS-SYN-0301" | AC2, AC3 |
| rwb-comms, rwb-treatment, rwb-payment (WireMock, from their OpenAPI) | `GET /api/recovery/comms/v1/notices/{noticeId}`, `GET /api/recovery/treatment/v1/treatments/{treatmentId}` and `GET /api/recovery/payment/v1/proceeds` with notice "NT-SYN-0301", treatment "TRT-SYN-0301" and proceeds "PRC-SYN-0301" | AC4, AC7 |
| gateway-bff composite case-record route (WireMock) | The one gateway answer the ledger section is read from, composing the ledger read and the case facts | AC3, AC10 |

The fakes are published from the owning services' OpenAPI documents and are versioned with the harness pack. The composite route path and merge order, the harness environment, its seeding and its evidence format and retention are Not specified in the source documents (GAP-0416; ASM-0591).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 10 consumed, each one hop on the owner's `/api/recovery/<short>/v1` base with a 2 s timeout (DP-11, DP-13) |
| Kafka | 0 published, 10 consumed: the nine business events of §12.4 on the owner's `rwb.<short>.events.v1` topic and `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` |
| Temporal | None: no workflow, no activity, no queue |
| File | None |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies named in the table (RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON) are delivered by the platform waves and are not repeated in the metadata H column; DP-15 resolves to "no migration", because the harness owns no schema. DP-18 is the ruling this harness proves: the ledger and the EFS intake rule are rwb-source-data's, the timeline is rwb-case's, and every read crosses one contract. The blocking dependencies of this story are the nine I stories, which replace the fakes with the real behaviour; they gate the done state, not the Day-1 start.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| LedgerJourneyRunner | Test harness | Runs the twelve `-ITG` cases of §16 in one run per business date, in fake or real mode per service, and stops at the first failed assertion with the trace |
| LedgerClient | Harness adapter | Calls the ten consumed operations of §12.2 through one hop with the channel, actor, date, page and size parameters, and records the answer |
| LedgerEventReplayer | Harness adapter | Replays the nine business events of §12.4 into the channel listener, including the duplicate of "EVT-SYN-0001", and reads the record on `rwb.decision-record.v1` |
| FakePack | WireMock project | Serves the owning services and the gateway-bff route of §12.8 from the published OpenAPI documents |
| LedgerSeedLoader | Service | Seeds the case, the EFS batch rows, the reference rows and the partner, notice, treatment and proceeds fixtures through the owner's contract or the fake |
| EntryAsserter | Assertion | Asserts each entry's event code, channel, direction, occurred time, source, contact key, holder references, links, delivery status, external reference and retention class |
| SummaryAsserter | Assertion | Asserts the read summary of AC6 — 3 read, 1 written, 1 excluded by the outcome list and 1 not on a case |
| RefusalAsserter | Assertion | Asserts the status and the message of each refusal and the empty state: 404 with MSG-P4-003, and MSG-P3-024 with no items |
| SchemaBoundaryCheck | Assertion | Fails the run on any cross-schema reference in the trace, so only rwb-source-data reads the ACE views |
| RunLock | Service | One run at a time in the harness environment |
| EvidenceReportPublisher | Reporter | Writes the per-run evidence report keyed by story id and business date and attaches it to the release record |
| JourneyGate | Assertion | Passes the run only when every owned criterion passes; fails and names the criterion, the seam and the observed value otherwise |

**Database.** None. The harness owns no schema, runs no Flyway migration and holds no table; seeds and assertions go through the contracts (DP-01, DP-15).

**Environment and test data.** SIT for the run of record and UAT for the acceptance run, with `rwb.integration.ledger-channels` on in both. The data are the synthetic seeds of the legacy story: case "RW-2026-000301" with account "ACC-SYN-0301" and owner "U-2001"; the EFS batch for 14 December 2026 with the "PTP", "SYS" and "ACC-SYN-0999" rows; the case "RW-2026-000302" with no entry; partner "LF-SYN-01" with instruction "INS-SYN-0301"; notice "NT-SYN-0301" with barcode "EV000000001TH"; treatment "TRT-SYN-0301"; proceeds "PRC-SYN-0301" of 5,000.00; users "U-2001", "U-2002" and "U-3001" with their teams and scopes; the business date 20 December 2026 for the run key. Each run starts from the seeded state, so a repeated run is deterministic. The harness environment, its seeding and its evidence format and retention are Not specified in the source documents (GAP-0416; ASM-0591).

**Build steps**

1. Build LedgerJourneyRunner and LedgerClient against the published OpenAPI documents of the owning services and the gateway-bff route.
2. Publish FakePack for the owning services and the composite route from the same documents, and prove the harness runs green from Day 1 on the fakes.
3. Write LedgerSeedLoader and the seed files, with the run lock and the fake or real mode per service.
4. Write EntryAsserter and SummaryAsserter for AC1 to AC6 and AC9, with a unit test on fixtures for every entry field and for the read summary.
5. Write RefusalAsserter and SchemaBoundaryCheck for AC10, AC11 and the access case.
6. Write LedgerEventReplayer for the duplicate delivery of AC5 and the failed-store run of AC7, including the incident assertion.
7. Replace each fake with the real service as its I story lands, in the order rwb-source-data, rwb-integration, rwb-case, rwb-access, rwb-partner, and rerun in UAT.
8. Write JourneyGate and EvidenceReportPublisher, and attach the report to the release record for the build under test.

**Feature switch.** `rwb.integration.ledger-channels`, the legacy switch of this story: on in SIT and UAT. The harness asserts the off state on the fakes — the listener acknowledges the six events without writing, the EFS read step does not run and the holder fields stay empty — and asserts that the Epic 1 ledger is unchanged in that state.

**Done when.** The twelve `-ITG` test cases of section 16 pass in SIT and UAT with the nine I stories in place and not only against the fakes; the evidence report for the run is attached to the release record with the ten owned criteria green; and the access case and the empty state are green with the messages of section 14.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-024 | The case has no ledger entry | No interactions are recorded on this case yet. |
| MSG-P4-002 | Role lacks Case record R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the reader's scope | This case is not in your scope. |

The harness asserts the message id and the rendered text of each row and never rewrites the text. Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | State | What the harness asserts |
|---|---|---|
| SCR-03 Case record | Read only | The ledger section is read through the composite route and shows the latest 20 entries of the case with time, channel, contact point masked by role, outcome, promise, linked offer or payment, delivery status, holder change and source |
| SCR-03 Case record | On hold | The same ledger section is returned and no edit is possible; the harness writes nothing |
| SCR-04 Case timeline | Loading | The first call of a run returns the entries of "RW-2026-000301" in the order 14, 15 and 18 December 2026 |
| SCR-04 Case timeline | Filtered | The channel, source, actor and date filters narrow the answer without dropping the entry's source or its retention class |
| SCR-04 Case timeline | Empty | The case "RW-2026-000302" returns MSG-P3-024 with no items |

The harness builds no screen and renders no page: it asserts the composite route answer the screen consumes, and the screen-level behaviour stays with RWB-P3-E2034-APP and RWB-P3-E2016-APP.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-034-12-ITG | Access; X8 | Component | RW-REFADM reads the ledger of "RW-2026-000301"; refused with MSG-P4-002, no entry returned |
| TC-E2-034-01-ITG | AC1, BR3, BR4, BR5, BR6 | Integration | One EFS action row with a promise of 12,500.00 for 20 December 2026; one Workbench call to "PHONE:CP-SYN-0301-M" |
| TC-E2-034-02-ITG | AC2, BR2 | Integration | One transfer from "U-2001" to "U-2002"; one instruction "INS-SYN-0301" to partner "LF-SYN-01" |
| TC-E2-034-03-ITG | AC3, BR4, BR9 | Integration | Entries from EFS, Workbench and the partner portal in the order 14, 15 and 18 December 2026 |
| TC-E2-034-04-ITG | AC4, BR1 | Integration | NoticeDispatched, NoticeDelivered, TreatmentApproved, ProceedsMatched |
| TC-E2-034-05-ITG | AC5, BR7 | Integration | NoticeDispatched delivered twice with the one event ID "EVT-SYN-0001" |
| TC-E2-034-06-ITG | AC6, BR3 | Integration | Three EFS rows: listed, unlisted, no open case |
| TC-E2-034-07-ITG | AC7, BR8 | Integration | Ledger store stopped, then restarted |
| TC-E2-034-08-ITG | AC8 (driven; AC8 is owned by RWB-P2-E2034-APP) | Integration | InstructionIssued for a case that does not exist; 3 retries |
| TC-E2-034-09-ITG | AC9, BR9 | Integration | EFS row processed after a later Workbench call |
| TC-E2-034-10-ITG | AC10 | Integration | Case "RW-2026-000302" with no entry |
| TC-E2-034-11-ITG | AC11 | Integration | Reader "U-3001" of team "HP-NE" with Own scope |

The `-ITG` cases assert the same behaviour as the legacy test cases under the same base id and add the seam each one exercises across services; the legacy test cases remain the record of the app stories. TC-E2-034-08-ITG is carried as the copy that drives the exception-queue seam, and its criterion AC8 stays with RWB-P2-E2034-APP. The full legacy test, with its Given, When and Then, is in the Test Cases workbook, tab Story test cases, under the legacy test case ID.

### 17. Guardrails

- No business value in code: the EFS outcome list, the event codes, the channels, the directions, the sources and the retention classes are reference data held by the owning services; the harness reads them and never holds a copy.
- No personal data in logs, tests, traces or reports: the contact point is a reference, the summary is masked by role, and the harness stores IDs, event codes, statuses and counts only.
- No read of another service's schema: every read goes through the owner's contract, the SchemaBoundaryCheck fails the run on a cross-schema reference, and only rwb-source-data reads the ACE views through its own interfaces (DP-05).
- No production data and no outside system: the harness calls only the owning services and their fakes, never an outside gateway or a production endpoint.
- One hop only: the harness fails a run when the trace shows a call chain deeper than the gateway and one owner.
- The ledger is append only: the harness asserts that a repeated delivery, a refusal and a successful read leave every entry unchanged and never update or delete one.
- The harness owns no table, no endpoint, no screen, no workflow and no schedule (DP-01, DP-18); it is test and evidence only.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ILG-009 | Contact outcomes from collections reach the ledger | Business Requirements Epic 2, section 3.2 | FEAT-ILG-06 | 06 to 10 Recovery case processes | R-UNI-40; BR3; BR4 | TC-E2-034-01-ITG, TC-E2-034-06-ITG, TC-E2-034-09-ITG |
| REQ-ILG-010 | Dispatched letters write their result, including proof of delivery | Business Requirements Epic 2, section 3.2 | FEAT-ILG-07 | 06 to 10 Recovery case processes | R-UNI-40; BR1 | TC-E2-034-04-ITG, TC-E2-034-05-ITG, TC-E2-034-07-ITG |
| REQ-ILG-011 | A hand-over names who held the case, who holds it now and when | Business Requirements Epic 2, section 3.2 | FEAT-ILG-08 | 06 to 10 Recovery case processes | BR2 | TC-E2-034-02-ITG, TC-E2-034-08-ITG |
| REQ-ILG-012 | The case record view shows the ledger as an ordered timeline | Business Requirements Epic 2, section 3.2 | FEAT-ILG-09 | 06 to 10 Recovery case processes | BR9 | TC-E2-034-03-ITG, TC-E2-034-10-ITG, TC-E2-034-11-ITG, TC-E2-034-12-ITG |
| REQ-ILG-013 | Ledger entries carry their own retention class | Business Requirements Epic 2, section 3.2 | FEAT-ILG-10 | All recovery processes | BR6 | TC-E2-034-01-ITG |
| REQ-ILG-014 | The contact point is a reference, never a copied number or address | Business Requirements Epic 2, section 3.2 | FEAT-ILG-06 | 06 to 10 Recovery case processes | BR5; CTL-11 | TC-E2-034-01-ITG |
| REQ-ILG-007 | One ledger entry per idempotency key; a repeat is counted | Business Requirements Epic 2, section 3.2 | FEAT-ILG-06 | 06 to 10 Recovery case processes | BR7; R-UNI-40 | TC-E2-034-05-ITG |
| REQ-ILG-008 | A failed ledger write loses nothing and is retried | Business Requirements Epic 2, section 3.2 | FEAT-ILG-07 | 06 to 10 Recovery case processes | BR8; NFR-077 | TC-E2-034-07-ITG |
| REQ-ILG-006 | The timeline orders entries by occurred time | Business Requirements Epic 2, section 3.2 | FEAT-ILG-09 | 06 to 10 Recovery case processes | BR9 | TC-E2-034-03-ITG, TC-E2-034-09-ITG |

The five requirements the legacy story tabulates keep their legacy BRD section and rule text. The four it does not tabulate keep the rule and test text the legacy story gives them, and are traced for completeness at the integration level only.

### 19. Out of scope

- The nine owning I stories and everything they build: RWB-P1-E2034-APP (the ledger store, the append and the ledger read), RWB-P1-E1066-APP (the ledger writer and its command), RWB-P1-E1067-APP (the Workbench events and the holder fields), RWB-P1-E1069-APP (the ACE view contract), RWB-P2-E2034-APP (the channel listener, the mapper and the EFS intake rule), RWB-P3-E2034-APP (the timeline and the case-record section), RWB-P3-E2016-APP (the case record and its facts), RWB-P4-E2034-APP (the rights and scope check) and RWB-S9-E2034-APP (the partner result).
- AC8 and the exception-queue handling of an event for an unknown case, which stay with RWB-P2-E2034-APP.
- Production code in any service: the harness is test and evidence only.
- The contract baselines of rwb-source-data, rwb-integration, rwb-case, rwb-access, rwb-partner, rwb-comms, rwb-treatment and rwb-payment, which their CON stories own.
- Platform deployment, the gateway-bff composite route implementation (RWB-PLT-N001-CON) and the platform configuration of Kafka, Temporal and the observability stack.
- Contact and promise history attached at case creation (RWB-E2-001) and SMS and LINE dispatch results (RWB-E2-022).
- Proof of delivery capture from WIN and the notice period timer (RWB-E2-021) and the retention periods and disposal of ledger entries (DL26 and the retention job JOB-17).
- Masking rules by role (RWB-E1-037) and the decision log query screen for audit (SCR-38, P7).
