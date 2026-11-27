# RWB-P1-E2034-APP Interaction ledger on the case and from every channel

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E2034-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-034 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP08, DP09, DP10, DP11, DP13, DP15, DP18, DP19 |
| Parallel lane | L-P1-Y |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P1-E2034-APP-16); the squad sizes the story at refinement |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E2034-CON |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7), base path /api/recovery/source-data/v1 |
| Readiness decisions | RD-P1-001, RD-P1-004, RD-P1-005, RD-P1-007, RD-P1-009, RD-P1-023, RD-P1-045, RD-P1-064 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v2.md (FR-P1-029, FR-P1-030) |
| Status | Draft (directive resolutions) |

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- `InteractionRequest` and `Interaction` 5.1.0 on the case-scoped paths only; this story calls `InteractionLedgerWriter` in process; an append writes no decision record (RD-P1-007). Findings #1, #4.
- Header key, business key, replay and conflict follow the shared rule; replays are not counted (RD-P1-001). Shared Problem body and codes (RD-P1-004).
- The six columns already exist; the migration adds the index and is safe to repeat; `retention_class` is varchar(10).
- The EFS outcome read is `GET /efs-history`; the contact-fact read stays open (GAP-2186). Finding #2.
- AC6 and AC10 rewritten, AC12 to AC15 added, test case mappings aligned to Test Cases v8. Finding #3.
- RD-P1-064: the ledger callers, the partner append, the notice entries, the promise entry type and the failed-append rule are stated. Test case IDs follow Test Cases v9; message texts follow Error and Message Standard v6.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-034 for rwb-source-data. The legacy story appended channel entries in process to the shared `interaction` table, resolved the retention class with a local table read and showed the ledger as a timeline in the same module; in the target the ledger and the shape of one entry stay with rwb-source-data (DP-01, DP-18 and the R-PREC default ruling that the ledger belongs to rwb-source-data), the six columns the legacy story added become one version on this service's own Flyway sequence with the index `ix_interaction_retention_class` (DP-15), the append and the case read keep the two case-scoped operations the Ownership Map gives this service and gain the six fields on base `/api/recovery/source-data/v1` (DP-11, DP-13), the retention class is a reference-data read through the client library and never a constant in code (DP-07), a decision record is written by the local library (DP-03), a redelivered append is absorbed by the inbox of the platform library (DP-09), no workflow and no Schedule sits in this story (DP-10), and the screens arrive through gateway-bff (DP-19); the event consumer and the event-to-entry mapping go to RWB-P2-E2034-APP, the partner result to the S9 slice of this key, the timeline to RWB-P3-E2034-APP, the scope to the P4 slice and the EFS history read to RWB-P1-E2001-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E2034-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 22 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **every channel entry of a case to be appended to one ledger with the contact point it reached, the holder who held the case before and after a move, the treatment or the proceeds it refers to and the retention class of its event code, and the case ledger to give those entries back in the order they occurred**, so that **a contact, a letter, a hand-over, an offer and a payment are recorded once and read once, and no service has to read another service's row to show them on the case**.

This is the rwb-source-data slice of legacy RWB-E2-034, and it owns **the ledger store and the shape of one entry**, not the channels that fill it. Under D-RCV-60 the one legacy story is five owners: the six channel events and their mapping are rwb-integration's (RWB-P2-E2034-APP), the partner result and the partner portal are rwb-partner's (the S9 slice), the timeline and the case record section are rwb-case's (RWB-P3-E2034-APP), the scope and the masking rule are rwb-access's (the P4 slice), and the EFS contact and promise history read is RWB-P1-E2001-APP's. This story delivers what is left, on the two case-scoped operations the Ownership Map already gives this service:

- **the migration.** One version on this service's own Flyway sequence makes sure `interaction`, in schema `rwb_source_data`, holds `contact_key varchar(255)`, `from_holder_ref varchar(60)`, `to_holder_ref varchar(60)`, `treatment_id uuid`, `proceeds_id uuid` and `retention_class varchar(10)` (`ADD COLUMN IF NOT EXISTS`; the columns are in Physical Schema v8) and creates the index `ix_interaction_retention_class`. The keys, the append-only trigger and the indexes of RWB-P1-E1066-APP and RWB-P1-E1068-APP are kept unchanged.
- **`POST /cases/{caseId}/interactions`.** The append of one channel entry, extended with the six fields. A `CASE_ALLOCATED` or `CASE_TRANSFERRED` entry carries the holder before and after the move; a `CONTACT`, `PROMISE`, `LETTER`, `HANDOVER`, `PARTNER_RESULT`, `OFFER` or `PAYMENT` entry carries the contact key token and, where it has one, the treatment or the proceeds link **as a reference** and never the amount of another service's record. Every entry carries the retention class resolved from its event code.
- **`GET /cases/{caseId}/interactions`.** The case read, extended with the six fields and ordered by occurred time and then by case sequence, so that a late EFS row reads before the call that was saved earlier (legacy BR9).
- **`RetentionClassResolver`.** The class of an event code is reference data, read through the reference-data client library with the version in force; a code with no class row is refused and nothing is written. Every event code carries `ILG-STD` until Compliance sets the periods (legacy assumption, DL26), and that value is a fixture value, never a value in the code.

**It owns no legacy acceptance criterion.** Legacy RWB-E2-034 wrote eleven criteria and an access row, and each one tests a slice that is not this one: **AC1** and **AC4** (an interaction, a letter, an offer and a payment are recorded) with RWB-P2-E2034-APP; **AC2** (a hand-over) with RWB-P2-E2034-APP and the S9 slice; **AC3** (the ledger is one place) and **AC9**, **AC10** with RWB-P3-E2034-APP; **AC5** (nothing written twice) with RWB-P2-E2034-APP's consumer and the writer criterion of RWB-P1-E1066-APP; **AC6** with RWB-P2-E2034-APP and RWB-P1-E2001-APP; **AC7** and **AC8** with RWB-P2-E2034-APP; **AC11** with the P4 slice. The cross-service proof is **RWB-ITG-E2034-ITG**. This story is therefore written with six new criteria tagged D-RCV-60, and each one tests only the store, the two operations and the retention resolution.

**What it reads and what it does not.** The story reads two values through library clients and neither is a record of another service: the **retention class of an event code**, through the reference-data client library of DP-07 (the event codes themselves are the published `eventCode` enum); and the **Case record C or R answer** of the two operations, through the guard library of DP-08. It reads no case row, no notice, no partner, no instruction, no treatment, no proceeds and no ACE view: the case check is the writer's (RWB-P1-E1066-APP), the holder values and the two links arrive from the caller as references, and the contact point is a token. The shape the consumer fills is declared by **RWB-P2-E2034-CON**, whose fake this story builds against from Day 1.

### 2. Business rationale

Contactability that is found and then lost again is the failure legacy RWB-E2-034 exists to remove. A case owner who picks up a case must see which number answered, who held the case last and which offer or payment the contact produced, without asking EFS, WIN or a partner. One append-only ledger per case holds all of it, and every one of those facts arrives from a different service: the owner of the store guarantees that the six values of an entry are stored once and read back unchanged, and the channels guarantee that the entry is the fact they themselves observed.

In the monolith the six columns were an internal addition to a local table and the retention class was a local table read, so nothing had to be agreed. In the target three things change at once. `interaction` is P1's own table in `rwb_source_data`, and the other eighteen services reach it only over this contract (DP-01, DP-18; Architecture v5 slide 4). The append and the read are REST operations with one hop and a 2 s budget, called by the integration consumer and by the screens through gateway-bff (DP-11, DP-13, DP-19; Architecture v5 slide 11). And the values in the six fields are **references to records of other owners**: a contact key of the ACE contact view, a user or partner reference of the holder, the identifier of a treatment of rwb-treatment and of a proceeds record of rwb-payment. A reference can be stored; another service's amount, name or address cannot be copied, because the copy is wrong the next morning and puts personal data in a second place.

The retention class is the second reason the store needs its own rule. Compliance sets a class per record type and a period per class (DL26), and every entry must carry its own class independently of the decision log (REQ-ILG-013). The class therefore cannot be a constant in the writer and cannot be guessed when the row is missing: it is data, it is read when the entry is appended, and a code with no class row is refused rather than defaulted, because a default files a record under a period nobody agreed to.

**What D-RCV-60 changes.** Not one legacy value. The case, the account, the contact key, the transfer time, the partner, the notice, the barcode, the treatment, the proceeds, the promise and the event ID keep their meaning and their spelling. What changes is where the fact is stored and who guarantees it: the six columns move onto this service's own migration sequence, the append and the case read become the two operations of one resource family, and the class becomes a reference-data read.

### 3. Preconditions

Nothing in this list is a build dependency: the story is Day 1 and builds against the published baseline, the published operations of RWB-P1-E1066-APP and RWB-P1-E1068-APP, and the fake of RWB-P2-E2034-CON, which is why the build dependency list is empty (Template and Rules §R5.7).

- RWB-P1-E1001-APP has run: schema `rwb_source_data` holds the base `interaction` table and the dictionary rows of P1.
- The ledger columns, the case-sequence allocator, the unique keys, the append-only trigger `tr_interaction_append_only`, the indexes, `InteractionLedgerWriter` and `POST` and `GET /cases/{caseId}/interactions` of RWB-P1-E1066-APP and RWB-P1-E1068-APP are used. Until those stories are merged this story builds against the published contract and its fake; it is Done only against the real writer and read.
- RWB-P2-E2034-CON is published with its fake: the append command as the integration consumer fills it, the answer it expects, the repeated-key answer and the 2 s budget (C).
- The callers of the ledger are fixed: in process RWB-P1-E1067-APP and this story; over REST, each under its own workload identity, rwb-case, rwb-comms, rwb-integration, rwb-document, rwb-payment, rwb-treatment and rwb-partner. rwb-partner appends its results itself (`eventCode` PARTNER_RESULT, `actorType` PARTNER, `actorRef` the partner code). rwb-comms appends the notice entries itself: LETTER for postal notices and CONTACT with channel SMS or LINE for messages, so the channel listener of rwb-integration appends nothing for `NoticeDispatched` or `NoticeDelivered`. An entry that records a promise to pay is PROMISE, otherwise CONTACT. On 503 MSG-P1-022 a caller does not commit its action, or retries with the same header key and business key (RD-P1-007, RD-P1-064).
- The reference-data client library (DP-07) and the authorise guard library (DP-08) are on the classpath as platform artefacts, and the event-code list and the class rows are served through the former. Their contracts are not in this Work Package's list, so both are fixture reads until those contracts are published (GAP-2184; ASM-3546).
- The idempotency and inbox library (DP-09) is in place in `rwb_source_data`, so a replayed header key is answered from the stored response. An append records no decision record; the acting service records its own (RD-P1-007 rule 6).
- The login and role of `rwb_source_data` exist in DEV and SIT, and the credential is held by the platform and never written in code, a test or a runbook (DP-02).
- The event codes that reach this store are the values of the published `Interaction.eventCode` enum (**LOV-LEDGER-EVENT**), with the two values the legacy story adds, `PARTNER_RESULT` and `OFFER` (GAP-2184; ASM-3543).
- The retention class list and the periods behind it are not published; until Compliance sets them every event code takes `ILG-STD` (GAP-2184; ASM-3543).
- The ownership of `interaction` is a plan ruling and not a source statement: the default ruling of R-PREC and DP-18 give the ledger to rwb-source-data (ASM-3542).

### 4. Flow

1. The consumer of rwb-integration, the rwb-integration hand-over run, or a recording screen of rwb-case through gateway-bff, calls `POST /api/recovery/source-data/v1/cases/{caseId}/interactions` with `InteractionRequest` 5.1.0 and a UUID `Idempotency-Key` header (DP-11, DP-13, DP-19; RD-P1-007).
2. `InteractionController` binds the body against the `InteractionRequest` schema of RWB-P1-E1066-APP extended by the six fields; a missing required member is refused with 422 naming the field, a `caseId` that is not a uuid or a bad header key with 400, and nothing is written.
3. `ChannelEntryValidator` checks the **event code** against the published `Interaction.eventCode` enum; a value outside it is refused with 422 and MSG-GEN-007 (RD-P1-004, RD-P1-007).
4. `ChannelEntryValidator` checks the **holder pair**: a `CASE_ALLOCATED` or `CASE_TRANSFERRED` entry carries both `fromHolderRef` and `toHolderRef`, and any other event code carries neither. The values are the references the caller supplies (`USER:<user id>` or `PARTNER:<partner code>`) and are never resolved into a name.
5. `ChannelEntryValidator` checks the **link rule**: an `OFFER` entry carries `treatmentId`, a `PAYMENT` entry carries `proceedsId`, neither carries the amount of the record it refers to, and a `CONTACT`, `LETTER` or `HANDOVER` entry carries the contact key token and no link.
6. `RetentionClassResolver` reads the class of the event code against the version in force; the class is written on the entry, a code with no class row is refused, and a class supplied by the caller is refused.
7. `InteractionLedgerWriter` of RWB-P1-E1066-APP, called in process in the same transaction, runs its own checks (the case exists, the occurred time, the actor and the source, the key), allocates the next case sequence inside one transaction on this service's table, and the unique key `(case_id, case_seq)` decides a race.
8. `InteractionRepository` inserts the entry with the six values beside the fields the writer already stores; no update and no delete method exists on it (BR7).
9. The transaction commits and the controller answers **201** with the stored entry, read back through the case read of this story inside the same call. No decision record and no event is written (RD-P1-007 rule 6).
10. A repeat of the same header `Idempotency-Key` with the same body replays the stored 201; a new header key whose business `idempotencyKey` is already in the ledger answers 200 with the existing entry; neither adds a row and neither is counted (RD-P1-001, RD-P1-007; R-UNI-40 counting applies to consumed events in the intake).
11. `GET /api/recovery/source-data/v1/cases/{caseId}/interactions` answers the entries of the case with the six fields, filtered by channel, actor and date range and paged, ordered by occurred time and then by case sequence (BR9); the authorise answer of DP-08 decides the read.
12. A database failure rolls the transaction back and answers 503; the incident hook of RWB-P1-E1066-APP fires with the case ID and the error class and no personal data.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A required value of the entry is missing or malformed, or a link is carried on an event code that has none | 422; nothing written; the field is named | MSG-GEN-001 | AC1 |
| X2 | The event code has no retention class row | 422; nothing written; the class is never defaulted | MSG-GEN-001 | AC2 |
| X3 | The event code is not a value of the published enum | 422; nothing written; the field is named | MSG-GEN-007 | AC13 |
| X4 | A `CASE_ALLOCATED` or `CASE_TRANSFERRED` entry carries no holder before or no holder after | 422; nothing written | MSG-GEN-001 | AC3 |
| X5 | The same header key with a different body or path, or the same business key with a different body | 409; the stored entry is not replaced and no second row is written | MSG-PLT-N009-05 | AC12 |
| X6 | The case does not exist, or is outside the scope of a user token | 404; nothing written and nothing returned (the rwb-case workload identity skips the case-exists read, RD-P1-007 rule 5) | MSG-P4-003 | AC10 |
| X7 | The caller holds no Case record C on the append or no R on the read | 403; nothing written and nothing returned | MSG-P4-002 | AC1, AC4 |
| X8 | The reference-data or authorise library does not answer inside 2 s, or answers an error | 503; nothing written, because a class that cannot be read is never guessed | MSG-GEN-006 | AC2 |
| X9 | The entry cannot be inserted | 503 with the rollback; the incident hook fires; nothing is discarded silently | MSG-P1-022 | AC7 |
| X10 | `caseId` not a uuid, or the `Idempotency-Key` header missing or not a UUID | 400; nothing written | MSG-GEN-001; MSG-PLT-N009-03 | AC12 |
| X11 | No valid credential | 401 | MSG-P4-001 | AC10 |
| X12 | Flag `rwb.source-data.ledger-channels` is off | The six fields are not accepted or answered; the operations of RWB-P1-E1066-APP and RWB-P1-E1068-APP behave as before this story | None | AC14 |

X1 to X4 are the validation paths the six fields add to the append of RWB-P1-E1066-APP. X5 and X6 are the writer's own paths, kept unchanged because this story extends the same operation. X7 is the access path of both operations, answered through the guard library of DP-08. X8 is the path that a class read across a boundary adds: in the monolith the class was a local table read that could not time out. X9 is the writer's failure path, carried unchanged.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published table and operations of RWB-P1-E1066-APP and RWB-P1-E1068-APP and the RWB-P2-E2034-CON fake from Day 1; the reference-data and authorise reads are library reads with fixtures, so no other service has to exist |
| Negotiable | The order of the checks, the class split of the validator and the read-back call are the squad's choice behind the operations; the six columns, their types, the index, the keys and the trigger are fixed |
| Valuable | One store where the contact point, the holder change, the treatment or proceeds link and the retention class of an entry are held once and read back unchanged, in time order |
| Estimable | One migration, two extended operations, one validator, one resolver, one repository method, two library reads and one fixture set |
| Small | Fits one sprint with its tests, as the store slice of the legacy key |
| Testable | Every criterion in section 7 is one call, one refused call or one statement against the ledger fixture |
| Day 1 | No build dependency; the store, the operations and the fake are published artefacts, so the tests run on the first day of wave 2 |

### 7. Acceptance criteria

```gherkin
Feature: Interaction ledger on the case and from every channel

  Background:
    Given open case "c0000000-0000-4000-8000-000000000301" (case number "RW-2026-000301") with account "ACC-SYN-0301" and owner "U-2001"
    Given the retention class list holds class "ILG-STD" for every event code
    Given the rwb-integration contract mock returns an accepted append for instruction "INS-SYN-0301" of case "RW-2026-000301" with partner "LF-SYN-01"

  Scenario: AC1 A channel entry stores its six values and the case read gives them back (new, D-RCV-60)
    Given a PROMISE entry of 14 December 2026 10:15 with event code "PROMISE", channel CALL, result RIGHT_PARTY, promise 12,500.00 for 20 December 2026 and contact key "PHONE:CP-SYN-0301-M"
    Given a LETTER entry for notice "NT-SYN-0301" dispatched on 19 December 2026 with external reference "EV000000001TH"
    Given an OFFER entry linked to treatment "TRT-SYN-0301" and a PAYMENT entry linked to proceeds "PRC-SYN-0301" of 5,000.00
    When each entry is appended through POST /cases/{caseId}/interactions and the case is read through GET /cases/{caseId}/interactions
    Then each append answers 201 and the read returns the four entries with their contact key, holder references, treatment link, proceeds link and retention class "ILG-STD"
    Then the OFFER entry carries no offer amount and the PAYMENT entry no proceeds amount, so 5,000.00 stays in "PRC-SYN-0301" of rwb-payment
    Then no entry, answer or log holds a phone number, a postal address, a person name or an account number

  Scenario: AC2 The retention class comes from the event code and a code with no row writes nothing (new, D-RCV-60)
    Given the retention class list holds class "ILG-STD" for event code "LETTER" and no row for event code "PARTNER_RESULT"
    When the caller appends a LETTER entry for notice "NT-SYN-0301" and then a PARTNER_RESULT entry
    Then the LETTER entry carries retention_class "ILG-STD"
    Then the PARTNER_RESULT append is refused with 422 and MSG-GEN-001 for "event code"
    Then the ledger holds no PARTNER_RESULT entry and the case stays at its last case sequence
    Then no class value stands in the code and the list is read through the reference-data client library

  Scenario: AC3 A move stores the holder before and after on the entry of the move (new, D-RCV-60)
    Given case "RW-2026-000301" is transferred from "U-2001" to "U-2002" on 16 December 2026 11:00
    When the CASE_TRANSFERRED entry of 16 December 2026 11:00 is appended
    Then the entry carries event code "CASE_TRANSFERRED", from_holder_ref "USER:U-2001" and to_holder_ref "USER:U-2002"
    Then the entry carries no channel and no direction
    Then an entry of the same event code with no from_holder_ref is refused with 422 and MSG-GEN-001 for "from holder"
    Then the case read returns both holder references unchanged

  Scenario: AC4 The contact point is a token and never a number or an address (new, D-RCV-60)
    Given case owner "U-2001" records a call on 15 December 2026 09:30 to contact key "PHONE:CP-SYN-0301-M" with result NO_ANSWER
    When the CONTACT entry is appended and the case is read
    Then the entry stores "PHONE:CP-SYN-0301-M" as contact_key and the read returns the same token
    Then the row, the 201 answer and the read hold no phone number, no postal address and no electronic mail address
    Then the contact value is resolved only from the owner of the ACE contact view when a screen displays it

  Scenario: AC5 A late entry reads in occurred-time order (new, D-RCV-60)
    Given the ledger holds the Workbench call of 15 December 2026 09:30 at case sequence 1
    When the EFS entry with contact time 14 December 2026 10:15 and key "EFS:EFS-SYN-0301-01" is appended on 15 December 2026 10:00
    Then the EFS entry takes occurred_at 14 December 2026 10:15 and its own later case sequence
    Then GET /cases/{caseId}/interactions returns the EFS entry before the call
    Then two entries with the same occurred time read in case sequence order

  Scenario: AC6 A repeated append writes one entry and the read returns one (new, D-RCV-60)
    Given a LETTER entry for notice "NT-SYN-0301" was appended with Idempotency-Key "b1000000-0000-4000-8000-000000000001" and business idempotencyKey "EV-14-RW-2026-000301-20261219-9e000000-0000-4000-8000-000000000301"
    When the same body is posted again with the same header key
    Then the stored 201 answer is replayed with the same caseSeq
    When the same body is posted with header key "b1000000-0000-4000-8000-000000000002"
    Then the answer is 200 with the existing entry
    Then the ledger holds one entry for that business key, the case sequence has no gap and no repeat, and no processed_event row is written

  Scenario: AC7 A failed insert rolls back, answers 503 and raises the incident (new, D-RCV-60)
    Given the ledger store cannot insert a row for case "RW-2026-000301"
    When a LETTER entry for notice "NT-SYN-0301" is appended through POST /cases/{caseId}/interactions
    Then the append answers 503 with MSG-P1-022 and nothing is returned
    Then no row is written and the case stays at its last case sequence
    Then the incident hook fires with the case ID and the error class and no personal data
    Then no entry is discarded silently

  Scenario: AC8 An entry is never updated or deleted and a correction is a new entry (new, D-RCV-60)
    Given a LETTER entry for notice "NT-SYN-0301" is stored on case "RW-2026-000301"
    When an update or a delete of that entry is attempted on the ledger
    Then the change is refused and the stored entry is unchanged
    Then the ledger repository exposes no update and no delete method for the interaction table
    Then a correction is stored as a new entry with its own case sequence and the original entry stays in the ledger

  Scenario: AC9 One ledger holds every entry of a case in rwb_source_data (new, D-RCV-60)
    Given the entries of case "RW-2026-000301" are stored by this service
    When the case is read through GET /cases/{caseId}/interactions
    Then every entry of the case is returned from the one interaction table of rwb_source_data
    Then no other service holds a copy of the ledger and each reads it only through the case read

  Scenario: AC10 The provided operations answer 401, 403 and 404 on their refusal paths (new, D-RCV-60)
    Given a user token without Case record C on the case
    When it appends through POST /api/recovery/source-data/v1/cases/c0000000-0000-4000-8000-000000000301/interactions
    Then the append answers 403 with MSG-P4-002 and nothing is written
    When a user token reads the ledger of case "c0000000-0000-4000-8000-000000000399" that rwb-case answers 404 for
    Then the read answers 404 with MSG-P4-003 and nothing is returned
    When either operation is called with no valid credential
    Then it answers 401 with MSG-P4-001

  Scenario: AC11 A consumed call that fails or does not answer writes nothing and guesses no value (new, D-RCV-60)
    Given the reference-data library does not answer inside 2 s for event code "LETTER"
    When a LETTER entry for notice "NT-SYN-0301" is appended through POST /cases/{caseId}/interactions
    Then the append answers 503 and nothing is written
    Then no retention class is guessed for the entry

  Scenario: AC12 Key conflicts and unusable identifiers are refused (new, D-RCV-60)
    Given the entry of AC6 is stored
    When header key "b1000000-0000-4000-8000-000000000001" is reused with a different body, and a new header key carries business key "EV-14-RW-2026-000301-20261219-9e000000-0000-4000-8000-000000000301" with a different body
    Then each answers 409 with MSG-PLT-N009-05 and the stored entry is unchanged
    When the header is missing, and when caseId is "RW-2026-000301"
    Then each answers 400 (MSG-PLT-N009-03, MSG-GEN-001) and nothing is written

  Scenario: AC13 Values the caller may not send are refused (new, D-RCV-60)
    When an append carries eventCode "FAX", and another carries retentionClass "ILG-STD"
    Then the first answers 422 with MSG-GEN-007 and the second 422 with MSG-GEN-001, each naming the field, and nothing is written

  Scenario: AC14 With the flag off the six fields are not applied (new, D-RCV-60)
    Given flag "rwb.source-data.ledger-channels" is off
    When an entry is appended and the case is read
    Then the append and the read behave as before this story and answer none of the six fields

  Scenario: AC15 A case with no entry answers an empty page (new, D-RCV-60)
    Given case "c0000000-0000-4000-8000-000000000302" exists and has no entry
    When its ledger is read
    Then the answer is 200 with an empty page
```

**Target reading.** Every assertion above is new, because this story owns no legacy criterion; each one tests only the store, the two operations and the retention resolution. What the legacy story asserted of the channels is proved in the slice that owns it: the consumer and the mapping in RWB-P2-E2034-APP, the partner result in the S9 slice, the timeline in RWB-P3-E2034-APP, the scope and masking in the P4 slice, the EFS history in RWB-P1-E2001-APP, and the whole key against live contracts in RWB-ITG-E2034-ITG. The legacy values are kept: case `RW-2026-000301`, account `ACC-SYN-0301`, owner `U-2001` and `U-2002`, contact key `PHONE:CP-SYN-0301-M`, action code `PTP`, result `RIGHT_PARTY` and `NO_ANSWER`, promise 12,500.00 for 20 December 2026, notice `NT-SYN-0301`, barcode `EV000000001TH`, treatment `TRT-SYN-0301`, proceeds `PRC-SYN-0301` of 5,000.00, event ID `EVT-SYN-0001`, instruction `INS-SYN-0301`, partner `LF-SYN-01`, the transfer of 16 December 2026 11:00 and the class `ILG-STD`. The `Given` of the contract mock in the Background is the fake of the C dependency RWB-P2-E2034-CON, which is how the consumer's write arrives (DP-11). AC5 proves the legacy ordering rule of BR9 on this store: the entry keeps the occurred time it is given, the case sequence is allocated at insert, and the read sorts on the time and not on the sequence. AC6 and AC12 prove the header key and the business key on the store (RD-P1-001, RD-P1-007), because this story extends the body they are stored with; the repeat of a redelivered *event* is legacy AC5 and is proved in RWB-P2-E2034-APP.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One ledger holds every interaction on a case, and this service owns the store and the shape of an entry | REQ-ILG-012; DP-18; R-PREC default ruling |
| BR2 | A hand-over between bank owners is the entry of the move, enriched with the holder before and after; the two references sit on that entry and carry no channel | REQ-ILG-011; legacy BR2 |
| BR3 | An offer or a payment is recorded as a reference to the treatment or the proceeds, never as its amount | legacy BR1, BR3; REQ-ILG-010 |
| BR4 | Every entry carries the retention class of its event code, set independently of the decision log; a code with no class row is refused | REQ-ILG-013; NFR-075; DL26; legacy BR6 |
| BR5 | The contact point is stored as a reference to the ACE contact key; the number or the address is never copied into the entry | REQ-ILG-014; CTL-11; legacy BR5 |
| BR6 | One entry per business idempotency key; a replayed header key answers the stored response and a repeated business key answers the existing entry | R-UNI-40; REQ-ILG-007; legacy BR7; RD-P1-001; RD-P1-007 |
| BR7 | Entries are append only; a correction is a new entry naming the original, with its own case sequence | legacy BR7; tr_interaction_append_only |
| BR8 | A ledger write that fails rolls back and raises an incident; no entry is discarded and no value is guessed | REQ-ILG-008; NFR-077; legacy BR8 |
| BR9 | The case read returns entries by occurred time and then by case sequence | REQ-ILG-006; legacy BR9 |

**Where each rule lives in the target.** BR1 is a schema rule as well: `interaction` exists once, in `rwb_source_data`, and the other eighteen services reach it only over this contract (DP-01, DP-18). BR2 is the holder pair of steps 4 and 8: two `varchar(60)` business references with no foreign key, supplied by the caller because rwb-case knows who holds the case and this service does not (DP-11). BR3 is the link rule of step 5: `treatment_id` and `proceeds_id` hold a reference and no amount of the linked record; the one amount the ledger itself keeps is the promise a contact produced, which is the interaction's own fact (legacy BR3). BR4 is `RetentionClassResolver`, and it is where the target changes the legacy mechanism: the class is not a local table read but a reference-data read with its version in force (DP-07), and a code with no row is refused rather than defaulted (X2, X8). BR5 is enforced twice: the request carries a key and the schema has no column for a number, an address or a name, so the copy is impossible rather than forbidden. BR6 keeps the legacy shape: the unique key on `idempotency_key` refuses the second insert, and a REST replay is not counted; redeliveries of consumed events are counted by the intake (DP-09; RD-P1-001). BR7 is the trigger kept unchanged plus the absence of any update or delete method on the repository. BR8 becomes 503 with MSG-P1-022 and the incident hook, with no discard. BR9 is the read order of the case read: `occurred_at`, then `case_seq`.

### 9. State transitions

None in the business sense. This story changes no case status, and an entry has no status and is never changed. The only states it moves are the entry's existence and the schema version it lives on.

| From | Event | Condition | To |
|---|---|---|---|
| a case at case sequence n | a valid append | The event code is in the list, its class resolves, the holder pair and the link rule hold | One entry exists at case sequence n+1 with its six values |
| a case at case sequence n | a refused append | A value is missing, the code has no class row, or the holder pair is incomplete | The case is still at case sequence n and no entry exists |
| a stored entry at case sequence n | a repeated header key with the same body, or a new header key with the same business key | The stored response or the existing entry is the authority | One entry exists at case sequence n |
| a stored entry at case sequence n | a repeated `Idempotency-Key` with a different body | The key is already used with another body | No entry is written and the answer is 409 |
| a stored entry at case sequence n | an update or a delete statement | The append-only trigger is in place | The statement is refused and the entry keeps its six values |
| an applied migration version | a correction to the columns or the index | A fix is needed | A new Flyway version is merged; the applied version is never edited |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The consumer identity of rwb-integration, with a workload identity token | Appends channel entries through the append and reads the case ledger back with its six values (Case record C then R) |
| The rwb-case workload identity | Appends entries for case actions it records, with the holder references of a move |
| The rwb-integration hand-over run | Appends the EFS history rows read from `GET /efs-history`, one call per row with the business key `EFS:<efs_record_key>` (RD-P1-007 rule 8) |
| RW-CASEOWN, case owner | Records a contact on own cases through the recording screens of rwb-case and gateway-bff, and reads the ledger of cases in scope (Case record C then R) |
| RW-TEAMMGR, RW-CONDUCT and other roles with Case record R | Read the ledger of cases in scope; they append nothing here |
| RW-REFADM, reference data administrator | Loads LOV-LEDGER-EVENT and the retention class rows with their versions (Reference data C) |
| RW-COMPLY, Compliance and PDPA officer | Sets the class and the period of a record type (Reference data U); DL26 is theirs and open |
| RW-PLATADM, platform administrator | Receives the write-failure incident of a refused insert and reads the append series of the deployment |
| rwb-case (P3) | Owns the case, the case record and the timeline; answers the case check the append takes (C RWB-P3-E1018-CON) |
| rwb-access (P4) | Owns the roles, the scope and the masking policy; answers the authorise question of both operations (DP-08) |
| No approval level from the delegation of authority applies | The story takes no business decision |

The operations run as the service identity of rwb-source-data (DP-02), and the caller's identity travels in the token, so the case check and the authorise answer are made for the caller and not for the service. The holder references, the contact key and the two links are references to records of other owners; this story resolves none of them into a name, a number, an address or an amount.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-INT-001 to DF-INT-013 | interaction | the standard interaction fields | Write, through the append of RWB-P1-E1066-APP |
| DF-INT-014 | interaction | event_code | Write, validated against LOV-LEDGER-EVENT |
| DF-INT-018 | interaction | idempotency_key | Write, as the repeat key |
| DF-INT-022 | interaction | contact_key | Write, and Read on the case read |
| DF-INT-023 | interaction | from_holder_ref | Write, and Read on the case read |
| DF-INT-024 | interaction | to_holder_ref | Write, and Read on the case read |
| DF-INT-025 | interaction | treatment_id | Write, and Read on the case read |
| DF-INT-026 | interaction | proceeds_id | Write, and Read on the case read |
| DF-INT-027 | interaction | retention_class | Write, resolved from the event code, and Read |
| DF-CAS-001 | recovery_case | id | Read through the rwb-case case contract, never from the table |

**Which side is this story's.** `DF-INT-022` to `DF-INT-027` are this story's: the migration adds the six columns, the append writes them and the case read returns them. `DF-INT-001` to `DF-INT-018` are the writer's and stay as RWB-P1-E1066-APP created them; this story adds no column beside the six and changes no key. `DF-INT-028` `delivery_status` and `DF-INT-029` `external_ref` are not this story's columns: they stay with the comms slices of this key, which write them through this append (ASM-3547). `DF-CAS-001` is rwb-case's key, answered by the contract and never joined locally (DP-01). `tr_interaction_append_only` is a database trigger of RWB-P1-E1066-APP, not a dictionary field or entity, and is named here only as the trigger BR7 relies on.

**Legacy read fields and their home in the target.**

| BR Field ID | Entity | Home in the target |
|---|---|---|
| DF-ACE-075, DF-ACE-076, DF-ACE-077 | v_ace_contact | The contact-fact read of this service's contract, consumed by RWB-P2-E2034-APP; this story stores the token only |
| DF-ACE-108 to DF-ACE-111, DF-ACE-114, DF-ACE-122, DF-ACE-123, DF-INT-036 | v_ace_efs_action | The EFS history read of RWB-P1-E2001-APP (GAP-2186; ASM-3548) |
| DF-CAS-009, DF-CAS-022, DF-CAS-025, DF-CAS-026, DF-ACE-002 | recovery_case, case_account, v_ace_account | The case contract of P3 and the EFS read of RWB-P1-E2001-APP; never a local read here |
| DF-LEG-015, DF-LEG-016, DF-LEG-020, DF-LEG-022 | notice | The rwb-comms notice contract, consumed by RWB-P2-E2034-APP; the barcode reaches this store as the external reference |
| DF-PRT-002, DF-TRT-001, DF-FIN-001 | partner, treatment, proceeds | The rwb-partner, rwb-treatment and rwb-payment contracts, consumed by RWB-P2-E2034-APP; this store keeps the reference only |

Field IDs are those in the Logical Data Model and Data Dictionary. No row of another service's table is read, and no value of one is copied into an entry.

### 12. Contract

Contract versions built against: rwb-source-data.yaml 5.1.0 (API Specification v7, RD-P1-005); rwb-access.yaml and rwb-case.yaml as published for the same release.

#### 12.1 REST operations provided

Owner rwb-source-data (P1); base `/api/recovery/source-data/v1` (DP-13). Two operations, both case-scoped, and both already published by RWB-P1-E1066-APP and RWB-P1-E1068-APP; this story extends them with the six fields and adds no operation and no resource. The case-scoped form is the one the Ownership Map lists and the one the consumer contract fakes, and the flat append row of RWB-P1-E1066-APP is realigned to it rather than published a second time here (GAP-2185; ASM-3542).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/interactions` | Appends one channel entry to a case with its contact key, its holder pair, its treatment or proceeds link and its retention class, and answers 201 with the stored entry | An authenticated caller with Case record C on the case: the consumer identity of rwb-integration, the identities of rwb-case, and the recording screens through gateway-bff (DP-08) | Header `Idempotency-Key` (UUID) required; replay answers the stored 201; body `idempotencyKey` is the permanent business key (200 on a repeat); a conflict is 409 |
| GET | `/cases/{caseId}/interactions` | Reads the ledger of a case with the six values, filtered by `channel`, `actor`, `from` and `to` and paged, ordered by occurred time and then by case sequence | Case record R on the case, answered through the guard library (DP-08) | Read only; changes nothing |

The request body is `InteractionRequest` 5.1.0 (RD-P1-007 rule 3): required `eventCode`, `occurredAt`, `actorType` (USER, SERVICE, PARTNER), `actorRef` (at most 64), `sourceRef` (at most 60), `idempotencyKey` (at most 120); this story's members are `contactKey`, `fromHolderRef`, `toHolderRef`, `treatmentId`, `proceedsId`, beside the other optional members of that schema (`documentId` and `correctsEntryId` among them); `id`, `caseId`, `caseSeq`, `sourceSystem` and `retentionClass` are server-set. The the response is `Interaction` and `InteractionPage` extended with the same six. `retentionClass` is answered by the service for every entry and is not accepted from the caller, because the class is data of the event code and never a value of the caller (ASM-3541). `treatmentId` and `proceedsId` hold the identifier of the treatment and of the proceeds record and carry no foreign key; the type of the two cross-service references is not stated in the source documents (GAP-2184; ASM-3541), and this story fixes them as the `uuid` columns the legacy migration gives them.

Errors are `application/problem+json` with the shared `Problem` schema (RD-P1-004): 400 MSG-GEN-001 (non-uuid `caseId`) or MSG-PLT-N009-03; 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 409 MSG-PLT-N009-05; 422 MSG-GEN-001 (missing or refused member, a code with no class row) or MSG-GEN-007 (value not in its list); 503 MSG-P1-022 (ledger) or MSG-GEN-006 (a library). The order and the paging of the read are those of the read this story extends: occurred time, then case sequence (RD-P1-009 rule 7), with the size and the maximum that read takes from the rwb-case parameters contract (ASM-3545). A code with no class row is refused with 422 and nothing is written (GAP-2184; ASM-3541).

#### 12.2 REST operations consumed

None. This story calls no operation of another service with a client of its own; its C dependency is the contract story of its own key, RWB-P2-E2034-CON, which declares the append as the integration consumer fills it and is faked for this story's tests.

Two values reach the story as library reads rather than as calls of its own, and both are named because the criteria of section 7 depend on them.

| Value | Owner | Pattern |
|---|---|---|
| The retention class rows, with the version in force, read once per append and once per read | P3 rwb-case, reference data (DP-07) | Client library read; C RWB-P3-E1043-CON, whose contract is outside this Work Package's list, so a fixture until it is published (GAP-2184; ASM-3546) |
| The Case record C or R answer for the caller on the case | P4 rwb-access (DP-08) | Guard library read; C RWB-P4-E1037-CON, a fixture until published (ASM-3546) |

#### 12.3 Events published

None. This story publishes no event and writes no decision record or outbox row (RD-P1-007 rule 6). `AceDataReady` and `AceDataLate` on `rwb.source-data.events.v1` belong to RWB-P1-E1015-APP.

#### 12.4 Events consumed

None. The consumer of the six channel events (`rwb.treatment.TreatmentApproved.v1`, `rwb.comms.NoticeDispatched.v1`, `rwb.comms.NoticeDelivered.v1`, `rwb.partner.InstructionIssued.v1`, `rwb.partner.PartnerResultSubmitted.v1`, `rwb.payment.ProceedsMatched.v1`) is P2's consumer `ledger-channels` on the owners' topics (RWB-P2-E2034-APP). It appends no entry for `NoticeDispatched` or `NoticeDelivered`, because rwb-comms appends those entries itself, and the partner result reaches the ledger by the REST append of rwb-partner (RD-P1-007, RD-P1-064). This story subscribes to nothing: it is reached over REST and writes what it is given.

#### 12.5 Workflows and activities

None. The append and the read are synchronous REST steps that write or read rows in one transaction; this story starts no workflow and no activity. The task queue of the service is `rwb-source-data` in namespace `rwb-recovery`, and the workflows `AceIngestCheck` and `reconciliation` and the activities `listEligibleAccounts` and `snapshot(page)` belong to other P1 stories (DP-10).

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job sits in this story: an entry is written when the caller appends it, and no part of this store is swept on a timer (DP-10).

#### 12.7 Tables owned

| Object | Schema | Owner | This story |
|---|---|---|---|
| `interaction` | `rwb_source_data` | P1 rwb-source-data (DP-01, DP-18) | The ledger table: the migration ensures the six columns and adds `ix_interaction_retention_class`, and keeps the unique keys, the append-only trigger and the indexes of RWB-P1-E1066-APP and RWB-P1-E1068-APP; the append writes through `InteractionLedgerWriter` and the case read reads, with no update and no delete method |
| `processed_event` | `rwb_source_data` | Platform library, created in this schema (DP-09) | The inbox, read and written by the library and not by this story |
| `idempotency_key` | `rwb_source_data` | Platform library, created in this schema (DP-09) | The stored response of an append, 24 hours; it holds no hit count |
| `outbox_event` | `rwb_source_data` | Platform library, created in this schema (DP-09) | Not used by this story |

No table of another service is read and no foreign key crosses a schema (DP-01): `recovery_case` stays in `rwb_case`, `notice` in `rwb_comms`, `partner` in `rwb_partner`, `treatment` in `rwb_treatment` and `proceeds` in `rwb_payment`.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-P2-E2034-CON fake | The append command and answer the integration consumer uses | An accepted append answering 201 with the entry reference, a repeated key answering the same reference, the instruction "INS-SYN-0301" of case "RW-2026-000301" with partner "LF-SYN-01", a 409 for a conflicting key and a 503 for an unavailable store |
| Ledger fixture | `rwb_source_data` | A container at the baseline plus the migrations of RWB-P1-E1066-APP, RWB-P1-E1068-APP and this story, with the six columns, the keys, the trigger and the new index, so the append-only test and the repeat test run on the real constraints |
| Retention class fixture | The reference-data client library | `ILG-STD` for every event code, a code with no class row, a version with a different class, and a timeout |
| Authorise guard fixture | The guard library of DP-08 | Case record C and R granted for the calling roles, refused for a role without them, and an open breaker |

The four fakes are local: no live rwb-integration, rwb-case, rwb-access, rwb-treatment or rwb-payment is needed for the tests of section 16, and no production ledger row, contact value or personal data is copied into a fixture.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 operations on `/api/recovery/source-data/v1` (`POST` and `GET /cases/{caseId}/interactions`) | None across a service boundary | OpenAPI 3.1; one hop, 2 s budget, breaker per downstream (DP-11, DP-13) |
| Kafka | None | None | The topic and both events belong to RWB-P1-E1015-APP; the six channel events are consumed by RWB-P2-E2034-APP; this story publishes no `DecisionRecorded` (RD-P1-007) |
| Temporal | None | None | No workflow, no activity, no Schedule (DP-10) |
| File | None | None | No file is read or written |
| SQL | None | `interaction` in `rwb_source_data`, written and read by this story | One insert and one paged select; no read of another service's table (DP-01) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata`, module `ledger`, with the published types in `...sourcedata.ledger.api`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`, topic `rwb.source-data.events.v1` (not published here), task queue `rwb-source-data` in namespace `rwb-recovery` (not used here).

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

The platform contracts of the table are pulled by the baseline stories of this service (RWB-P1-E1066-APP, RWB-P1-E1068-APP), so the build dependency list of this story stays empty and the story is Day 1. DP-01 is the shape of the story: `interaction` is P1's own table and no other service reads it. DP-03 is a statement: an append writes no decision record (RD-P1-007). DP-09: the stored response absorbs a replay; this story writes no outbox row. DP-05 is a statement: no ACE value is read here. DP-06 is a statement: the page size and its maximum are read as data by the case read of RWB-P1-E1068-APP and are not redefined here. DP-07 is the retention class, a library read with a fixture, and DP-08 is the authorise answer of both operations, a library read with a fixture. The event-code list LOV-LEDGER-EVENT is the closed `eventCode` enum of the contract: a new value is a code change to the eventCode enum and is not read as data. DP-10 is a statement: no workflow, activity or Schedule. DP-11 and DP-13 are the two case-scoped operations on the service base. DP-15 is the migration. DP-18 is the ownership ruling. DP-19 is the edge route the responding screens arrive through.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `V<next>__rwb_e2_034_interaction_channel_columns.sql` (next version on the service sequence) | Migration | `ADD COLUMN IF NOT EXISTS` for the six columns and `CREATE INDEX IF NOT EXISTS ix_interaction_retention_class`; keeps the keys, the trigger and the existing indexes |
| `InteractionController` | Controller | The two operations of 12.1, extended with the six fields; RFC 9457 details; `Idempotency-Key` handling |
| `ChannelEntryValidator` | Service | The event code enum, the holder pair, the link rule and the contact key form; MSG-GEN-001 or MSG-GEN-007 naming the field |
| `RetentionClassResolver` | Service | The class of an event code from reference data; refuses a code with no row; never defaults |
| `InteractionLinkValidator` | Service | The treatment and proceeds rule: a reference on the event code that has one, no amount of the linked record, no foreign key |
| `InteractionRepository` | Repository | One insert with the six values and one paged read by case, ordered by occurred time then case sequence; no update and no delete method |
| `Interaction`, `InteractionRequest`, `InteractionPage` | Published types | The schemas of 12.1 extended with `contactKey`, `fromHolderRef`, `toHolderRef`, `treatmentId`, `proceedsId` and `retentionClass` |
| `ReferenceDataClient` | Client library use | The retention class rows as data, with the version in force (DP-07) |
| `AuthoriseClient` | Guard library use | The Case record C and R answers of both operations (DP-08) |

**Migration and sequence (DP-15).** One version on this service's own Flyway sequence, after the writer's columns and after the actor index of RWB-P1-E1068-APP. It runs `ADD COLUMN IF NOT EXISTS` for `contact_key varchar(255)`, `from_holder_ref varchar(60)`, `to_holder_ref varchar(60)`, `treatment_id uuid`, `proceeds_id uuid` and `retention_class varchar(10)` on `interaction` in `rwb_source_data` (the types of Physical Schema v8) and creates `ix_interaction_retention_class`; it leaves `tr_interaction_append_only`, the unique keys and the existing indexes as they are. A repeated run changes nothing; an applied version is never edited; rollback is the flag and a forward migration only (RD-P1-045).

**Configuration and reference data**

- The class of an event code is reference data of rwb-case under DP-07, read through the client library; the list and the periods behind it are Compliance's under DL26, and until they are set every event code takes `ILG-STD`, the legacy assumption, which the fixture carries and the code does not (GAP-2184; ASM-3543).
- The values of LOV-LEDGER-EVENT, `PARTNER_RESULT` and `OFFER` included, are the published `eventCode` enum; their Thai labels are reference data (ASM-3543; RD-P1-007).
- The holder reference form (`USER:<user id>` or `PARTNER:<partner code>`) and the contact key form (`<contact type>:<contact key>`) are the forms the legacy criteria use; the append validates the form and never resolves the reference into a name (ASM-3544).
- The 2 s budget and the breaker of the two library reads are client configuration (DP-11); a class read that does not answer inside 2 s refuses the append and writes nothing.
- The flag `rwb.source-data.ledger-channels` gates the six fields and their checks at deployment.

**Build steps**

1. The repeatable migration of the six columns and `ix_interaction_retention_class`, with the trigger and keys untouched (DP-15).
2. The three published types extended with the six fields and published with the service baseline (C).
3. `ChannelEntryValidator`: the event code enum, the holder pair, the link rule and the contact key form, with no insert on a refusal (AC1, AC3, AC4, AC13).
4. `RetentionClassResolver` against the reference-data client library and its fixture, called before the insert for every entry, with a code that has no row refused and a timeout refused (AC2, X2, X8).
5. `InteractionRepository`: the insert of the six values and the paged read of a case ordered by occurred time then case sequence, with no update and no delete method (AC1, AC5).
6. The 201 read-back through the case read, so the answer of an append is what was stored (AC1).
7. The replay, business repeat and conflict paths of the library and the writer (AC6, AC12).
8. `AuthoriseClient` through the guard library: Case record C on the append and R on the read, refused with MSG-P4-002, plus the timeout path (X7).
9. An architecture test that no class outside the `ledger` module uses `InteractionRepository`, that the repository has no update and no delete method, and that no class of this story names a table of another service (DP-01).

**Feature flag.** `rwb.source-data.ledger-channels`. Off, the six fields and their checks are not applied and the ledger operations behave as before this story (RD-P1-045; AC14).

**Done when.** The tests in section 16 pass, the six columns and the index are applied on the service sequence with the trigger and the keys still in place, an append answers 201 with the six values read back through the case read, an event code with no class row is refused with nothing written, a `CASE_TRANSFERRED` entry carries both holder references, a late entry reads in occurred-time order, a replayed key and a repeated business key leave one entry, and no entry of the fixture holds a number, an address, a name or another service's amount.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required value is missing or malformed, a class has no row for the code, a class is supplied by the caller, or a holder pair is incomplete | Enter {field}. |
| MSG-P1-022 | The entry could not be written | The entry was not saved because the interaction ledger could not be written. Try again in a few minutes. |
| MSG-P4-001 | No valid credential (401) | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-GEN-007 | An event code or other value not in its list | As Error and Message Standard v6 |
| MSG-PLT-N009-03, -05, -06 | Idempotency key missing, conflicting, or the store down | As Error and Message Standard v6 |
| MSG-P4-002 | The caller holds no Case record C on the append or no R on the read | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is unknown or outside the caller's scope | This case is not in your scope. |
| MSG-GEN-006 | The reference-data or authorise library does not answer inside 2 s | {system} is not available. Try again in a few minutes. |
| MSG-P3-024 | The case has no ledger entry (the timeline's empty state, owned by RWB-P3-E2034-APP) | Nothing is recorded in {section} yet. |

Thai text for each message follows decision DL10, which is open (assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863). MSG-GEN-001 names the field and is never filled with a data value; MSG-P4-002, MSG-P4-003 and MSG-P3-024 are raised by the access, case and screen slices and are carried here unchanged; MSG-GEN-006 names the failed system and never a key value. No message carries a number, an address, a name or a case summary. Decision DL26 is open (assumptions ASM-0247, ASM-0264, ASM-0275 and ASM-0355).

### 15. Screens and states

No screen in this story and no route of its own. The case owner records a contact through the recording screens of rwb-case and reads the ledger in SCR-03 Case record and SCR-04 Case timeline, both of which arrive through the gateway-bff composite route and belong to the screen owners (DP-19; RWB-PLT-N001-CON); the timeline is RWB-P3-E2034-APP's. The states shown there - Loading, Empty with MSG-P3-024, Error, and No access - belong to those screens; the No access state is Not specified in the source documents (CG-ALL-2477, CG-ALL-2478). This story serves the store behind the recording screen and the case read, and on a refused append the caller sees MSG-GEN-001 or MSG-P1-022 in the Error state of the recording screen; this story renders none of it.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-034-01 | AC1, BR3, BR4, BR5 | End to end | One EFS action row with a promise; one Workbench call |
| TC-E2-034-02 | AC2, BR2 | End to end | One transfer from "U-2001" to "U-2002" on 16 December 2026 11:00; one instruction "INS-SYN-0301" to partner "LF-SYN-01" |
| TC-P1-E2034-APP-01 | AC3 | Component | Ledger fixture |
| TC-E2-034-21 | AC3, BR9 (legacy regression; the timeline is RWB-P3-E2034-APP's) | End to end | Entries from EFS, Workbench and the partner portal |
| TC-E2-034-04 | AC4, BR3 | End to end | The OFFER and PAYMENT links without the linked amount |
| TC-E2-034-13 | AC4 | See Test Cases v9 | Contact key token |
| TC-E2-034-09 | AC5, BR9 | End to end | EFS row processed after a later Workbench call |
| TC-E2-034-05 | AC6, BR6 | End to end | The same body appended twice with one event ID "EVT-SYN-0001" |
| TC-P1-E2034-APP-02 | AC7 | Component | Store failure |
| TC-E2-034-16 | AC7, BR8 (legacy regression; delivery and outbox path is RWB-P2-E2034-APP's) | See Test Cases v9 | Ledger store stopped, then restarted |
| TC-E2-034-17 | AC8 | See Test Cases v9 | Update attempt and correcting entry |
| TC-E2-034-18 | AC9 | See Test Cases v9 | One ledger per case |
| TC-E2-034-19 | AC10 | See Test Cases v9 | Refusal paths |
| TC-E2-034-20 | AC11 | See Test Cases v9 | Library timeout |
| TC-P1-E2034-APP-03 | AC12 | Component | Header and business keys |
| TC-P1-E2034-APP-04 | AC13 | Component | Refused values |
| TC-P1-E2034-APP-05 | AC14 | Component | Flag off |
| TC-P1-E2034-APP-06 | AC15 | Component | Case with no entry |
| TC-E2-034-14 | Section 12 operations, contract test | See Test Cases v9 | Fake of 12.8 |
| TC-E2-034-15 | Section 12.7 tables, boundary test | See Test Cases v9 | Fixtures of 12.8 |

The IDs follow Test Cases v9. The legacy rows TC-E2-034-03, -06, -07, -08, -10, -11 and -12 belong to the slices that own those criteria and are not cited by this story; they run again in RWB-ITG-E2034-ITG against the live contracts. This is an application story with no integration copy of its own, so no row carries the `-ITG` suffix. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the event codes are list values of LOV-LEDGER-EVENT, the retention classes are reference rows, and the holder and contact key forms are validated formats and not codes (DP-07).
- No personal data in logs, tests, events or prompts: the six fields are references, the entry summary is the one personal field and is masked at the read by the policy of rwb-access, and a contact number, an address, a name and an account number are never read, logged or returned by this store (BR5).
- No read of another service's tables: the case is answered by the case contract, the authorise answer by the guard library, and the six fields hold references to records of rwb-case, rwb-comms, rwb-partner, rwb-treatment and rwb-payment reached over their contracts only (DP-01, DP-08, DP-11).
- ACE data only through the owner's contract or `v_ace_*` views: this story reads no ACE data; the contact key is a token the caller supplies (DP-05).
- No entry is ever updated or deleted by application code: the trigger refuses the statement, it keeps its behaviour unchanged on this story's migration, and the repository has no such method (BR7).
- The idempotency, inbox and outbox tables stay the library's: they are created in this schema and are never redefined here (DP-09).
- One login, one schema and one sequence: the release carries the `rwb_source_data` login, migrates `rwb_source_data` only, and an applied version is never edited (DP-02, DP-15).
- Both operations are one hop with a 2 s budget and a breaker per library; a class read that does not answer refuses the append and writes nothing (DP-11, X8).
- No screen is served here: the recording screens, the case record and the timeline arrive through the gateway-bff composite route and are the screen owners' (DP-19).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ILG-009 | Contact outcomes from collections reach the ledger | Business Requirements Epic 2, section 3.2 | FEAT-ILG-06 | 06 to 10 Recovery case processes | R-UNI-40 | TC-E2-034-01, TC-E2-034-05, TC-E2-034-09 |
| REQ-ILG-010 | Dispatched letters write their result, including proof of delivery | Business Requirements Epic 2, section 3.2 | FEAT-ILG-07 | 06 to 10 Recovery case processes | R-UNI-40 | TC-E2-034-04, TC-E2-034-05, TC-E2-034-16 |
| REQ-ILG-011 | A hand-over names who held the case, who holds it now and when | Business Requirements Epic 2, section 3.2 | FEAT-ILG-08 | 06 to 10 Recovery case processes | None | TC-E2-034-02, TC-E2-034-17, TC-E2-034-19 |
| REQ-ILG-012 | The case record view shows the ledger as an ordered timeline | Business Requirements Epic 2, section 3.2 | FEAT-ILG-09 | 06 to 10 Recovery case processes | None | TC-E2-034-21, TC-E2-034-19, TC-E2-034-20, TC-P1-E2034-APP-06 |
| REQ-ILG-013 | Ledger entries carry their own retention class | Business Requirements Epic 2, section 3.2 | FEAT-ILG-10 | All recovery processes | None | TC-E2-034-01 |
| REQ-ILG-014 | Personal data in the ledger is a reference, masked by role | Business Requirements Epic 2, section 3.2 | Not specified in the source documents (GAP-2184; ASM-3541) | All recovery processes | CTL-11 | TC-E2-034-01, TC-E2-034-19 |
| REQ-ILG-007 | The same key twice gives one entry; the ledger writer counts the repeat in its idempotency store | Business Requirements Epic 2, section 3.2 | Not specified in the source documents (GAP-2184; ASM-3541) | All recovery processes | R-UNI-40 | TC-E2-034-05 |
| REQ-ILG-008 | A failed ledger write raises an incident; no entry is discarded | Business Requirements Epic 2, section 3.2 | Not specified in the source documents (GAP-2184; ASM-3541) | All recovery processes | NFR-077 | TC-E2-034-16 |
| REQ-ILG-006 | The ledger reads in one ordered sequence, filterable by channel, actor and date range | Business Requirements Epic 2, section 3.2 | Not specified in the source documents (GAP-2184; ASM-3541) | All recovery processes | None | TC-E2-034-21, TC-E2-034-09 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P2-E2034-CON | Contract | C: the append command and answer the integration consumer uses, with its fake; this story implements the app side of it |
| RWB-P1-E1066-APP | App development | Adopted as published artefacts: the ledger table, the case-sequence allocator, the keys, the trigger and the append this story extends |
| RWB-P1-E1068-APP | App development | Adopted as published artefacts: the actor index this migration follows, and the case read this story extends |
| RWB-P2-E2034-APP | App development | The consumer and the mapper that supply the six values; owner of legacy AC1, AC4 to AC8 |
| RWB-P3-E2034-APP | App development | The timeline and the case record section; owner of legacy AC3, AC9, AC10 and MSG-P3-024 |
| RWB-P1-E2001-APP | App development | Sibling in this service: the EFS history read and its key behind legacy AC6 |
| RWB-P4-E2034-APP | App development | The scope and masking slice of this key; owner of legacy AC11 |
| RWB-ITG-E2034-ITG | Integration | Proves the whole legacy key against the live rwb-integration, rwb-case, rwb-access and this service |
| RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON | Contract | The platform libraries and the sequence this story adopts as published artefacts: decision record, reference data, guard, outbox and inbox, Flyway sequence, edge route |

### 19. Out of scope

- The event consumer, the event-to-entry mapping, the EFS outcome list and the exception queue of the six channel events (RWB-P2-E2034-APP); this story is reached over REST and subscribes to nothing.
- The partner result, the partner portal and the instruction facts (RWB-P2-E2034-APP and the S9 slice of this key).
- The case timeline, the case record section, the empty state MSG-P3-024 and the screen order (RWB-P3-E2034-APP).
- The roles, the scope model, the masking rule and the PII access log (the P4 slice of this key; DP-08).
- The EFS contact and promise history read, the collection period and the idempotency key of an EFS row (RWB-P1-E2001-APP). The EFS outcome read of the channel consumer is `GET /efs-history`; the contact-fact read is not part of this story (GAP-2186).
- The delivery status and the external reference of a letter or a message, and the send result of SMS and LINE: rwb-comms appends them through this append, with the members that RWB-P1-E2021-APP and RWB-P1-E2022-APP define (RD-P1-064).
- A complaint signal on the ledger: no `eventCode` identifies a complaint (Pending, owner product owner with compliance, NEW-GAP-F10-02; RD-P1-064).
- The retention period, the disposal of an entry and the retention job JOB-17 (DL26 and P5); this story stores a class and applies no period.
- The decision record of an action: the acting service records its own; an append writes none (RD-P1-007 rule 6).
- The case, notice, partner, treatment and proceeds records themselves and their amounts; this story stores a reference to each and none of their values.
- The screens and the gateway-bff composite route (the screen owners and RWB-PLT-N001-CON; DP-19).
- The real cross-service proof against the live consumer, the live timeline and the live contracts (RWB-ITG-E2034-ITG).

### 20. Remaining delivery steps

- Size the story (DOR-RWB-P1-E2034-APP-16): delivery lead with the squad.
- Sign off the epic design: solution architect.
- Publish rwb-source-data.yaml 5.1.0 and its fake, and align RWB-P2-E2034-CON: API contract owner.
- Publish the contact-fact read of the channel consumer (GAP-2186): solution architect.
- Publish the retention class list and periods (GAP-2184; DL26): Compliance and the reference data administrator.
- Load the synthetic ledger and class fixtures in DEV: data engineer.
