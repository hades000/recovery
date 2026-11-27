# RWB-P3-E2034-APP Interaction ledger on the case and from every channel

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2034-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-034 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP08, DP09, DP10, DP11, DP13, DP15, DP18, DP19 |
| Parallel lane | L-P3-AL |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E2034-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (no FR mapped to REQ-ILG-009, REQ-ILG-010, REQ-ILG-011, REQ-ILG-012, REQ-ILG-013, REQ-ILG-014, REQ-ILG-007, REQ-ILG-008, REQ-ILG-006) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-034 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P3-E2034-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **the timeline of my case to return one time-ordered list of the case events of rwb-case and the ledger entries of rwb-source-data, each item naming its source, channel, entry type and occurred time, paged and stable when two items share a time, with the empty state and the scope refusal of the legacy story, and a call I record on the case written once through rwb-source-data's append under its idempotency key**, so that **a contact, a letter, a hand-over, an offer and a payment are read where I already look and are not found and then lost again, without rwb-case holding or reading the interaction table**.

This is the case-timeline slice of legacy RWB-E2-034, in `rwb-case`: schema `rwb_case`, base `/api/recovery/case/v1` (DP-13), topic `rwb.case.events.v1` with names `rwb.case.<Event>.v1`, queue `rwb-case` in namespace `rwb-recovery`, package `th.co.scb.ace.workbench.recovery.case`, one schema and login per service (DP-01, DP-02).

- **Provided:** `GET /cases/{caseId}/timeline` on that base, the case timeline operation the Ownership Map keeps with P3, returning the case events of this service plus the ledger entries of `rwb-source-data` read one hop away through the P1 contract.
- **Consumed:** the case-scoped ledger read and the ledger append on `/api/recovery/source-data/v1`; the append is called once per Workbench-raised interaction with an `Idempotency-Key`.
- **Not this slice:** the ledger row, the EFS intake rule, the dedupe and the exception queue (rwb-source-data's under the R-PREC ruling and DP-18); the channel consumer, retry and exception queue (RWB-P2-E2034-APP); the letter, payment and offer objects; roles, scope and masking rows (DP-08); the full seven-type timeline and item-type rights filter (RWB-P3-E2016-APP). `interaction` is not a table of `rwb_case`.

The ruling is one sentence: the ledger and its intake rule are rwb-source-data's, the case timeline and the case-scoped interaction read stay with rwb-case, and every ledger read and write crosses one published contract, one hop, inside 2 s.

### 2. Business rationale

Contact outcomes from collections, letters sent through WIN and work held by partners sit in different systems today, so a case owner who picks up a case does not know which number answered or who held it last. The measure is unchanged: the share of open cases whose last right-party contact is visible on the case, today zero for cases that came from EFS. REQ-ILG-012 asks for the ledger as an ordered timeline on the case record and REQ-ILG-006 for it to read back as one filtered sequence; this slice answers both on the case screen, serves REQ-ILG-009 to REQ-ILG-011 by reading the entries their channels produce, REQ-ILG-014 by showing a masked reference and REQ-ILG-013 by leaving the retention class to the entry's owner. REQ-ILG-007 and REQ-ILG-008 are cited for the one behaviour this slice owns: a call is written once under its key, and a refused write leaves no half item.

The realignment keeps the measure and moves the seam: one append-only ledger has one writer, so the case service asks its owner to write an entry instead of writing one itself, and the timeline is composed at the read rather than projected into `rwb_case`. Six moves carry the rule across that seam:

1. The legacy `interaction` table in the recovery schema becomes rwb-source-data's table in its own schema (DP-01, DP-18); the case service holds no column of it and reads what it shows through the P1 contract, turning the legacy in-process call into one hop with a 2 s timeout and a breaker (DP-11).
2. The legacy base `/api/recovery/v1` becomes `/api/recovery/case/v1` for the timeline and `/api/recovery/source-data/v1` for the ledger (DP-13).
3. Page size and source timeout become parameter rows (DP-06), and channel, source and entry-type values come from the reference-data contract with the version in force (DP-07): no code holds a LOV value.
4. `RecoveryAccessGuard` becomes the authorise contract of rwb-access with the guard library (DP-08), so the right, the scope and the mask are answered by their owner.
5. The case screen is composed at the edge by gateway-bff (DP-19): one composite route, never an owner service from the browser.
6. The order is the one value the sources do not settle: the timeline contract serves its page newest first, while the legacy story, its AC3 and AC9 and REQ-ILG-006 read the ledger in occurred-time order with case sequence on a tie. This slice fixes the sequence of the merged items and the tie-break and keeps the page order of the timeline contract (GAP-2226; ASM-3668).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P2-E2034-CON is baselined | The append as consumed: one entry per call, create-only, idempotent on the key, the same reference on a repeat, 409 for a held key, 503 when the store is down; the case-scoped read; the fakes. Element names of the append command, the case-scoped read and the intake result are Not specified in the source documents (GAP-2225; ASM-3667) |
| The rwb-source-data stories of this key are published | The ledger table, its append-only trigger, the append, the case-scoped read, the EFS outcome list and the retention classes: consumed, never restated (DP-18) |
| The rwb-case baseline and the timeline contract of RWB-P3-E2016-CON | `rwb_case`, the base with `GET /cases/{caseId}`, the `rwb-case` queue and login (DP-02); the `TimelinePage` and `TimelineItem` shapes, the item types including `INTERACTION`, the paging parameters, the page order and the item-type rights filter |
| The parameters, reference-data and access contracts | Page default and maximum and the source timeout as parameter rows (DP-06); LOV-SOURCE, LOV-CHANNEL, LOV-LEDGER-EVENT and type labels with versions (DP-07); authorise and masking policies (DP-08) |
| The gateway-bff route and SIT data | The DP-19 route that merges the case answer and the timeline answer; case "RW-2026-000301" in team "MTG-BKK" with the transfer of 16 December 2026 11:00; case "RW-2026-000302" with no entry; the users of section 10 |

Business preconditions carried from the legacy story: the case is open and the reader holds Case record R with the case in scope; action code "PTP" carries channel CALL and every event code carries retention class "ILG-STD" until Compliance sets the periods, both as rwb-source-data reference rows read there and never here; the contact point travels as a reference such as "PHONE:CP-SYN-0301-M"; a case with no ledger entry is normal and shows the empty state.

### 4. Flow

1. The case owner opens SCR-04, or the ledger section of SCR-03; the browser calls the gateway-bff composite route (DP-19).
2. gateway-bff calls `GET /api/recovery/case/v1/cases/{caseId}/timeline` with the `type`, `channel`, `from`, `to`, `page` and `size` of the screen, one hop inside the 2 s budget (DP-11).
3. rwb-case asks rwb-access `POST /api/recovery/access/v1/authorise` for `CASE_RECORD` right `R` with the case as object reference and receives the decision, the scope and the masking policy. Missing right is 403; a case outside scope is 404.
4. rwb-case reads `recovery_case` and its own case events from `assignment` with `queue_code`: allocation, assignment and transfer, with holder before and after, reason and rule ID.
5. rwb-case reads `timeline.ledger-timeout-ms` and the page default and maximum through the parameters contract (DP-06); no budget or bound is a constant.
6. rwb-case calls `GET /api/recovery/source-data/v1/cases/{caseId}/interactions` with the date range, channel and actor filters, `page` and `size`, under the parameter timeout and a breaker, and receives `occurredAt`, `channel`, `eventCode`, `sourceSystem`, `direction`, `contactResult`, `contactKey`, `caseSeq` and the entry ID.
7. rwb-case maps each ledger entry to one `TimelineItem` of type `INTERACTION` and each case event to one item of its type, with source marker, channel, entry type and occurred time; the text is built from codes and reference labels, never from another service's free text (BR1, BR5).
8. rwb-case orders the merged items by occurred time then `caseSeq` (BR2), masks the contact reference through the ACE common masking path with the policy from rwb-access (BR6), pages the list and returns `items[]`, `page`, `size` and `total`; a page past the last returns an empty `items[]` with the same total.
9. The owner filters by channel, source and date range; a `to` before a `from`, a `size` outside its bounds or an unknown type is refused before any source is called.
10. The owner records a call: the front end sends the `Idempotency-Key`, rwb-case calls the P1 append once with the entry command and that key, keeps no copy, and stores the answer of its own call in `idempotency_key`, so a repeat returns the first answer without a second append (BR4).
11. The owner reopens the timeline: the new entry shows as one `INTERACTION` item, source WORKBENCH, channel CALL, in its occurred-time place, because the list is composed at the read.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Role without Case record R | Refused with 403 before the case facts are read; nothing returned, nothing written | MSG-P4-002 | TC-E2-034-12 |
| X2 | Case outside the reader's scope | Refused with 404; no item, case number or contact reference returned | MSG-P4-003 | AC5 |
| X3 | Case with no ledger entry | Empty `items[]`, total 0; the ledger section shows the empty state | MSG-P3-024 | AC4 |
| X4 | Date `to` before date `from` | Refused before any source is called; nothing read, nothing written | MSG-GEN-003 | AC2 |
| X5 | `size` outside its bounds, or a type outside the seven | Refused before any source is called, naming the field and its bounds | MSG-GEN-002 | AC2 |
| X6 | Ledger read slow past the parameter timeout, or breaker open | The case events return with 200 and the missing source is named by the timeline contract; the read does not fail | MSG-GEN-006 | AC1 |
| X7 | Append answers 409 for a held key | The first answer is returned as success: the entry exists once and the call is a repeat | None | AC7 |
| X8 | Append answers 503 or times out | No item is added and nothing is half written in `rwb_case`; a repeat with the same key appends once when the store is back | None | AC7 |
| X9 | Intake result cannot be read | The items still show with 200 and the note says the intake result is unavailable; no count is invented | None | AC8 |
| X10 | Two entries at the same occurred-at time | The lower `caseSeq` reads first on every page and on a repeated query | None | AC3 |

The read never returns another case's item: the scope is answered by rwb-access before the case facts are read and the ledger read is case-scoped.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against `RWB-P2-E2034-CON` and the published rwb-source-data operations with their fakes; case facts come from its own schema |
| Negotiable | Page bounds, source timeout and labels are parameter and reference rows; sequence, refusal and empty state are fixed |
| Valuable | The owner reads the one history of the case without asking another team, and no second writer of the append-only ledger exists |
| Estimable | One provided operation, two consumed ledger paths, one rights call, one masking read, three components and one page section |
| Small | Fits one iteration; the ledger, the intake, the exception queue and the screen's other sections are other stories' |
| Testable | Every criterion of section 7 is one test of section 16, against a contract fake or a seeded `rwb_case` row; no test reaches another schema |

### 7. Acceptance criteria

```gherkin
Feature: Interaction ledger on the case and from every channel

  Background:
    Given open case "RW-2026-000301" with account "ACC-SYN-0301", held by "U-2001" in team "MTG-BKK"
    Given the rwb-source-data contract mock returns the 3 ledger entries of "RW-2026-000301": a CONTACT entry with source EFS, channel CALL, occurred 14 December 2026 10:15, result RIGHT_PARTY, promise 12,500.00 for 20 December 2026 and retention class "ILG-STD"; a CONTACT entry with source WORKBENCH, channel CALL, occurred 15 December 2026 09:30, contact key "PHONE:CP-SYN-0301-M" and result NO_ANSWER; and a PARTNER_RESULT entry with source WORKBENCH, channel PORTAL, direction INBOUND, occurred 18 December 2026 16:00
    Given the rwb-access contract mock returns Case record R and the scope Own over team "MTG-BKK" for "U-2001"

  Scenario: AC1 One time-ordered list of the case events and the ledger entries (new, D-RCV-60)
    Given case "RW-2026-000301" was transferred from "U-2001" to "U-2002" on 16 December 2026 11:00, held as one assignment row of "rwb_case"
    When "U-2001" opens the timeline of "RW-2026-000301"
    Then the answer holds one list of 4 items in this order: the CONTACT entry of 14 December 2026 10:15, the CONTACT entry of 15 December 2026 09:30, the case event of 16 December 2026 11:00 and the PARTNER_RESULT entry of 18 December 2026 16:00
    Then each item names its source marker (EFS, then WORKBENCH, WORKBENCH, WORKBENCH), its channel (CALL, CALL, none, PORTAL), its entry type (CONTACT, CONTACT, CASE_TRANSFERRED, PARTNER_RESULT) and its occurred-at time
    Then the contact point is the reference "PHONE:CP-SYN-0301-M" and no number and no address appears in any item
    Then the ledger items are read through the rwb-source-data contract and no interaction table is read or held in "rwb_case"

  Scenario: AC2 A long case is read page by page with one total (new, D-RCV-60)
    Given the timeline of "RW-2026-000301" holds the 4 items of AC1
    When "U-2001" reads page 0 and then page 1 with a page size of 2
    Then page 0 returns the items of 14 and 15 December 2026 and page 1 the items of 16 and 18 December 2026, and both answers carry the same total 4
    Then a request for page 2 returns an empty items[] with the same total 4, and the same query repeated returns the same items in the same order, none lost and none doubled
    When "U-2001" asks with a page size of 500, and again with the date from 2026-12-18 and to 2026-12-14
    Then both requests are refused before any source is called, with MSG-GEN-002 for the size and MSG-GEN-003 for the dates

  Scenario: AC3 Two entries at the same instant keep their case sequence (new, D-RCV-60)
    Given the rwb-source-data contract mock returns two entries of "RW-2026-000301" at the same occurred-at time of 17 December 2026 14:00 with case sequence 7 and case sequence 8
    When "U-2001" reads the timeline with a page size of 1
    Then the entry with case sequence 7 reads before the entry with case sequence 8 on every page and on a repeated query
    Then the two entries never appear on two pages at once and neither is dropped

  Scenario: AC4 A case with no ledger entry shows the empty state (new, D-RCV-60)
    Given open case "RW-2026-000302" with no ledger entry
    Given the rwb-source-data contract mock returns no entry for "RW-2026-000302"
    When the case owner opens its timeline with the ledger items selected
    Then the answer holds an empty items[] and a total of 0
    Then the ledger section of the screen shows message MSG-P3-024 with the filters still shown, no error is raised and nothing is written

  Scenario: AC5 A case outside the reader's scope is refused (new, D-RCV-60)
    Given case "RW-2026-000301" is owned by "U-2002" in team "MTG-BKK"
    Given the rwb-access contract mock returns no scope for "U-3001" over team "MTG-BKK"
    When case owner "U-3001" of team "HP-NE" with Own scope reads its timeline
    Then the response is 404 with message MSG-P4-003
    Then no item, no case number and no contact reference is returned, and no ledger read is made for that case

  Scenario: AC6 A late ledger entry reads in time order (new, D-RCV-60)
    Given the ledger holds the Workbench call of 15 December 2026 09:30 for "RW-2026-000301"
    Given the rwb-source-data contract mock returns the EFS entry with contact time 14 December 2026 10:15, written on 15 December 2026 at 10:00
    When "U-2001" reads the timeline
    Then the EFS entry of 14 December 2026 10:15 reads before the call of 15 December 2026 09:30
    Then the written time of the EFS row is not used as its occurred time

  Scenario: AC7 A Workbench-raised interaction is written to the ledger once (new, D-RCV-60)
    Given case owner "U-2001" records a call on 15 December 2026 09:30 to contact key "PHONE:CP-SYN-0301-M" with result NO_ANSWER, and the client sends the Idempotency-Key "IDK-SYN-0301-01"
    When the call is saved
    Then rwb-case calls the rwb-source-data append once with case "RW-2026-000301", entry type CONTACT, channel CALL, occurred 15 December 2026 09:30, contact key "PHONE:CP-SYN-0301-M", result NO_ANSWER and the key "IDK-SYN-0301-01"
    Then the rwb-source-data contract mock answers 201 with one entry reference, and "rwb_case" holds no interaction row, no copy of the entry and no ledger column
    When the same call is saved again with the same key "IDK-SYN-0301-01"
    Then the append is answered with the same entry reference and the hit count for that key becomes 2
    Then the timeline holds one CONTACT entry with source WORKBENCH, channel CALL, occurred 15 December 2026 09:30 and result NO_ANSWER

  Scenario: AC8 The ledger's intake result is read through the rwb-source-data contract (new, D-RCV-60)
    Given the EFS rows for 14 December 2026 hold 3 rows: action code "PTP" for "ACC-SYN-0301", action code "SYS" not in the outcome list for "ACC-SYN-0301", and action code "PTP" for account "ACC-SYN-0999" on no open case
    Given the rwb-source-data contract mock returns the intake result of business date 14 December 2026 as 3 read, 1 written, 1 excluded by the outcome list and 1 not on a case
    When "U-2001" opens the timeline of "RW-2026-000301" for that business date
    Then the ledger items hold the one CONTACT entry with source EFS, channel CALL, occurred 14 December 2026 10:15
    Then the timeline note names 3 read, 1 written, 1 excluded and 1 not on a case, read through the rwb-source-data contract
    Then rwb-case writes no EFS row, no outcome-list row and no read summary of its own
```

This secondary slice owns no legacy AC. AC1 to AC11 of RWB-E2-034 are carried by rwb-integration (RWB-P2-E2034-APP, RWB-P2-E2034-CON) and by the rwb-source-data stories of this key; the eight criteria above carry this slice's assertions with the legacy values unchanged. Behind them: the ledger is read one hop away, never from an `interaction` table in `rwb_case` (DP-18); every criterion that needs another service carries its contract mock; the Workbench entry is written by the ledger's owner, which is what makes "nothing is written twice" provable across two services; order is occurred time then case sequence, with the screen's page order left to the timeline contract; and the element names of the item, the append command and the intake result are assumed and renamed at contract review if the published contract differs (GAP-2225; ASM-3667).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The timeline is one list of the case events of `rwb_case` and the ledger entries of rwb-source-data read through the P1 contract; each item names its source marker, channel, entry type and occurred-at time | REQ-ILG-006; REQ-ILG-012 |
| BR2 | Items are ordered by occurred time and, at the same instant, by `caseSeq`, so order is stable across pages; the screen's page order stays the timeline contract's | Legacy BR9, AC3, AC9; REQ-ILG-006 |
| BR3 | `interaction` is not a table of `rwb_case`: no entry, field or summary is copied into this schema and no ACE view is read here | DP-01; DP-18; ownership ruling |
| BR4 | A Workbench-raised interaction is written by one append call under the request's `Idempotency-Key`; a repeat returns the first answer and is counted; a 409 is a repeat, not a failure | Legacy BR7; R-UNI-40; REQ-ILG-007 |
| BR5 | Source marker, channel and entry type are the values the ledger holds, from LOV-SOURCE, LOV-CHANNEL and LOV-LEDGER-EVENT with the version in force; no code holds one | DP-07; legacy BR4; TSD P3 v3 T3.2 |
| BR6 | The contact point is a reference: the item carries the contact key and the caller's mask, never a number, an address or an unmasked value | REQ-ILG-014; CTL-11; DP-08 |
| BR7 | The retention class belongs to the entry and its owner; this slice neither shows a class of its own nor recomputes one | REQ-ILG-013; DP-18 |
| BR8 | Paging is part of the operation: `page` starts at 0, `size` starts at the parameter default, its maximum is the parameter value, and an out-of-bounds size or a `to` before a `from` is refused before any source is called | DP-06; legacy contract |
| BR9 | Right and scope are answered by rwb-access: 403 without Case record R, 404 outside scope, both before any case fact or ledger item is read | DP-08; legacy AC11; CTL-09 |
| BR10 | The intake result is read through the P1 contract and named as received; this service writes no EFS row, applies no outcome list and keeps no summary | Legacy AC6; DP-18; REQ-ILG-009 |
| BR11 | The read writes nothing: no row, decision record, event or workflow state, and a refusal writes nothing either | Legacy section 9; Template and Rules §R7.2 s17 |
| BR12 | A ledger that does not answer inside the parameter timeout does not fail the read: the case events return with 200 and the missing source is named by the timeline contract | NFR-008; legacy AC6 |

### 9. State transitions

None. This story changes no case status and moves no case; the one write it causes is a ledger entry created by rwb-source-data, which moves none either. The ledger is append-only and has no state; the delivery states PENDING, RETRYING, DELIVERED and EXCEPTION belong to the integration slice and are not read here.

| Observed fact | Written by | Appears as |
|---|---|---|
| Case allocated to a queue | rwb-case allocation (RWB-P3-E1020-APP) | One case event with queue and owner |
| Case transferred with a reason code | rwb-case transfer (RWB-P3-E1021-APP) | One case event from "U-2001" to "U-2002" |
| A call recorded on the case | rwb-source-data through its append, on this slice's request | One `INTERACTION` item, source WORKBENCH, channel CALL |
| A letter, partner result, offer or payment recorded | rwb-comms, rwb-partner, rwb-treatment, rwb-payment through the intake of RWB-P2-E2034-APP | One `INTERACTION` item of its entry type |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Reads the timeline of a case in scope (Case record R); records a call on a case they hold (Case record U; the entry is created by rwb-source-data) |
| RW-TEAMMGR; RW-CONDUCT; RW-AUDIT | Read the timeline of a case in scope (Case record R), the contact reference masked by role; change nothing |
| SY-CASEWF, the rwb-case service identity | Applies the access check, reads `recovery_case` and `assignment`, calls the P1 read, the P1 append and the masking read, one hop each; writes no ledger row |
| rwb-source-data contract | Owns the ledger, the append, the case-scoped read, the entry codes, the retention class and the intake rule; refuses a repeated key and answers the same reference |
| rwb-access contract | Answers the right, the scope and the masking policy of the caller's roles |
| RW-REFADM and every role without Case record R | Refused on the operation with MSG-P4-002 |
| No approval applies | The story takes no business decision and records none |

The reader's right is `CASE_RECORD` right `R` with the scope of the caller's team; no role name and no scope value sits in code. The service runs as the rwb-case login (DP-02), which no source names.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001, DF-CAS-002 | recovery_case | id, case_no | Read |
| DF-CAS-009, DF-CAS-011, DF-CAS-022 | recovery_case | owner_user_id, team_code, closed_date | Read |
| DF-WRK-010, DF-WRK-039 | assignment | case_id, queue_id | Read |
| DF-WRK-012 to DF-WRK-016, DF-WRK-040 | assignment | assignee_user_id, assigned_at, ended_at, reason, rule_id, transfer_reason_code | Read |
| DF-INT-001, DF-INT-002, DF-INT-019 | interaction | id (the item reference), case_id, case_seq (tie-break) | Read through the P1 contract |
| DF-INT-004 to DF-INT-006 | interaction | occurred_at, channel, direction | Read through the P1 contract |
| DF-INT-008, DF-INT-011 | interaction | contact_result, summary masked by role | Read through the P1 contract |
| DF-INT-013, DF-INT-014 | interaction | source_system (source marker), event_code (entry type) | Read through the P1 contract |
| DF-INT-018 | interaction | idempotency_key | Write through the P1 append only |
| DF-INT-022 to DF-INT-024 | interaction | contact point reference, from_holder_ref, to_holder_ref | Read through the P1 contract, masked by role |
| DF-INT-027 | interaction | retention_class | Not read: kept by the owner of the entry |
| DF-REF-132 to DF-REF-184 | parameter_catalog, parameter_value, reference_version, reference_row | source timeout, page default and maximum, LOV-SOURCE, LOV-CHANNEL, LOV-LEDGER-EVENT, type labels, with versions in force | Read |
| (idempotency) | idempotency_key in `rwb_case` | the stored answer of the append call under its key | Write |

Field IDs are those of the Logical Data Model and Data Dictionary v9. Every `interaction` row keeps its legacy field IDs and belongs to rwb-source-data (DP-18), so all of them are read through the P1 contract and none is a column of `rwb_case`; the physical names, lengths and required flags of the item, the append command and the intake result are Not specified in the source documents (GAP-2225; ASM-3667). The contact reference is masked before it leaves the service (BR6), and item text is built from codes and labels, never from another service's free text.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/case/v1`; owner rwb-case (P3).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/cases/{caseId}/timeline` | One page of the case timeline: `items[]`, `page`, `size`, `total`; each item carries `at`, `type`, `source`, `channel`, `entryType`, `summary`, `by`, `reference`; query `caseId` (path), `type` (`INTERACTION` selects the ledger items), `channel`, `from`, `to`, `page` (default 0), `size` (default and maximum from the parameters) | Case record R, scope applied by rwb-access, contact reference masked by role | Not applicable: the read writes nothing |

`TimelinePage` and `TimelineItem` are the shapes of the case timeline contract of RWB-P3-E2016-CON; this slice adds no field and removes none, and fills four of them for an interaction item: `source`, `channel`, `entryType`, `at`. Errors: 401 (MSG-P4-001); 403 (MSG-P4-002); 404 unknown case or outside scope (MSG-P4-003); 422 a `to` before a `from` (MSG-GEN-003), a `size` out of bounds or a type outside the seven (MSG-GEN-002); 503 the case store down. A slow ledger is not a 5xx here: the case events return with 200 and the missing source is named by the timeline contract (BR12). The operation is the Ownership Map's `GET /cases/{caseId}/timeline` (owner P3) on the rwb-case base, the re-based form of API-P3-003 of TSD P3 v3 T-A.1; the interaction read and the append are rwb-source-data's and appear in 12.2 as consumed.

#### 12.2 REST operations consumed

One hop per call, no chaining; the parameter timeout `timeline.ledger-timeout-ms` and a breaker per downstream apply to every row.

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | rwb-source-data (P1) | The case's entries for the date range, channel and actor filters: `occurredAt`, `channel`, `eventCode`, `sourceSystem`, `direction`, `contactResult`, `contactKey`, `caseSeq`, entry ID | One hop, parameter timeout, breaker |
| POST | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | rwb-source-data (P1) | The append of one Workbench-raised interaction, create-only and idempotent on `Idempotency-Key`: 201 with a reference, the same reference on a repeat, 409 for a held key, 503 when the store is down | One hop, parameter timeout, no retry on a 4xx |
| GET | The ledger intake-result read of the rwb-source-data contract, for a business date | rwb-source-data (P1) | The intake result: `businessDate`, `rowsRead`, `written`, `excluded`, `notOnCase`; the path and element names are Not specified in the source documents (GAP-2225; ASM-3667) | One hop, parameter timeout, breaker |
| POST | `/api/recovery/access/v1/authorise` | rwb-access (P4) | Case record R, the scope and the masking policy of the caller's roles, cached by the guard library (DP-08) | One hop, 2 s, cached |
| GET | `/api/recovery/access/v1/masking-policies` | rwb-access (P4) | The mask the ACE common masking path applies to a contact reference by role (CTL-11) | One hop, 2 s, cached |

The two ledger operations are the re-based forms of API-P3-014 and API-P3-015 of TSD P3 v3 T-A.1 on the rwb-source-data base, which the Ownership Map records as P1's. RWB-P2-E2034-CON restates the append as consumed with its command, its four answers and the rule that the append is called before the caller marks anything; this story consumes that restatement and defines no part of it.

#### 12.3 Events published

None. The timeline is a read and the append is a synchronously owned write, so this slice has no outbox row and no topic of its own; the case events it shows are rows written by the allocation, transfer and timer stories. A decision record of a case action is written by the library of the story that takes the action (DP-03), never here.

#### 12.4 Events consumed

None. Entries reach rwb-source-data through its intake and its EFS step and this slice reads them when the case is opened, so it holds no projection and no inbox: a late or corrected entry reads correctly at the next open and no stale ledger copy exists in `rwb_case`.

#### 12.5 Workflows and activities

None added. The timeline is served inside the request and the append is one synchronous call under its key. The case workflow of RWB-P3-E2043-APP owns the case lifecycle and is not touched.

#### 12.6 Schedules

None. No Schedule and no Quartz row: the read has no clock and the append is started by a person.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| recovery_case | P3 (`rwb_case`) | The case facts of the item and the access object: ID, case number, owner, team, entry date, closed date |
| assignment | P3 (`rwb_case`) | The case events of the timeline: allocation, assignment and transfer with owner, queue, reason, rule ID |
| idempotency_key | PLT library, created in `rwb_case` | The stored answer of the append call under the request's key |
| outbox_event, processed_event | PLT library, created in `rwb_case` | Present in the schema; this slice reads and writes none of them |

`interaction` is not a table of this contract: rwb-source-data owns it (DP-18) and it is read and written only through 12.2. `efs_ledger_outcome`, the retention classes and the intake summary are rwb-source-data's too. No table of another service is read and no foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-source-data WireMock, ledger read | The P1 case-scoped read | The 3 entries of 14, 15 and 18 December 2026; two entries at 17 December 2026 14:00 with case sequence 7 and 8; an empty answer for "RW-2026-000302"; one delayed answer beyond the parameter timeout |
| rwb-source-data WireMock, append | The P1 append | 201 with a reference; the same reference on a repeat with the same key; 409 for a held key; 503 and a slow answer for the retry path of AC7 |
| rwb-source-data WireMock, intake result | The P1 intake-result read | 3 read, 1 written, 1 excluded and 1 not on a case for 14 December 2026; one unavailable answer |
| rwb-access WireMock | The P4 contract | Allow `RW-CASEOWN` in team "MTG-BKK" with Case record R; refuse `RW-REFADM` with MSG-P4-002; refuse "U-3001" over team "MTG-BKK" with MSG-P4-003; the caller's masking policy |
| gateway-bff route WireMock | The DP-19 composite route of SCR-04 | The merged case and timeline answer, and the refusal that must not read as an empty timeline |
| `rwb_case` fixture | This story's own test data | Case "RW-2026-000301" held by "U-2001" in team "MTG-BKK" with the transfer of 16 December 2026 11:00; case "RW-2026-000302" with no entry |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 5 consumed | The timeline operation provided; the P1 case-scoped read, append and intake-result read, and the P4 authorise and masking read consumed; one hop, parameter timeout, breaker |
| Kafka | None | No event published or consumed (12.3, 12.4) |
| Temporal | None | No workflow and no activity added; the read is served inside the request |
| File | None | No file read or written; the EFS rows reach the ledger through its owner |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `timeline`, Java package `th.co.scb.ace.workbench.recovery.case.timeline`, extending the timeline module of RWB-P3-E2016-APP; front end folder `src/modules/recovery/case/timeline` with the ledger section of the timeline page and the log-interaction panel of the case record page.

**Pattern application.** DP-01: `recovery_case` and `assignment` in `rwb_case` only, `interaction` absent. DP-03: no instance, a read writes no decision record (H RWB-PLT-E1027-CON). DP-05: no instance, no view is read here. DP-06: the timeout and page default and maximum rows (H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON). DP-07: LOV-SOURCE, LOV-CHANNEL, LOV-LEDGER-EVENT and type labels (H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON). DP-08: right, scope and contact mask (H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON). DP-09: the `idempotency_key` row of the append call only (H RWB-PLT-TE006-CON). DP-10: no instance, no workflow and no Schedule (H RWB-PLT-E1071-CON). DP-11: the two ledger operations with their fakes (none; C from the legacy dependency). DP-13: both bases. DP-15: no instance, no table and no column added (H RWB-PLT-E1044-CON). DP-18: the read and the append of 12.2. DP-19: the route of SCR-03 and SCR-04 (H RWB-PLT-N001-CON). Metadata H is None and correct: those platform contracts are pulled by the rwb-case baseline stories and the timeline contract, so this slice is Day 1 and builds against the published `RWB-P2-E2034-CON` and the P1, P4 and gateway-bff fakes.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TimelineController | REST controller | The operation, query and page validation, problem responses with their message IDs |
| TimelineService | Service | Merges case events and ledger items, applies the sequence of BR2, pages and returns the total |
| CaseEventReadRepository | Repository | Reads `recovery_case` and `assignment` with `queue_code` for a case and a date range |
| LedgerReadClient, LedgerAppendClient, IntakeResultClient | Clients | The P1 read under the timeout and breaker (BR1); the command sent once under the key with a 409 read as a repeat (BR4); the intake result named as received (BR10) |
| TimelineItemMapper, ContactMaskAdapter | Service, library adapter | The item from codes and reference labels; the contact reference masked through the ACE common masking path (BR6) |
| LedgerSection, LogInteractionPanel | React component | The ledger section of SCR-04 and SCR-03, the Loading, Filtered, Empty and Degraded states, the filters and the save panel |

**Database and migrations.** Reads `recovery_case` and `assignment` in `rwb_case` and writes one `idempotency_key` row per append call; no new table, no new column, no migration of this story. The indexes used, `ix_assignment_case_assigned_at` and `ix_timer_case_started_at`, come from `V2016_1__timeline_indexes.sql` of RWB-P3-E2016-APP in the same Flyway sequence (DP-15). The `interaction` table, its trigger and its indexes are rwb-source-data's migration and are never created, altered or indexed here (DP-18).

**Configuration and reference data.** Parameter rows through the parameters contract (DP-06): `timeline.ledger-timeout-ms`, `timeline.page-size-default`, `timeline.page-size-max`; breaker and bulkhead settings are the resilience library's defaults and no number is fixed here. Reference rows (DP-07): LOV-SOURCE, LOV-CHANNEL, LOV-LEDGER-EVENT and the seven item type labels with the version in force; the type list is a list value, not a Java enum. The mask of a role is read from rwb-access and applied by the ACE common masking path.

**Build steps**

1. `CaseEventReadRepository` over `recovery_case` and `assignment`, with one test per case event and the transfer of AC1.
2. `LedgerReadClient` against the P1 fake with the parameter timeout, the breaker and the delayed answer (AC1, X6).
3. `TimelineItemMapper` with source marker, channel and entry type from reference rows and the masked contact reference (AC1).
4. The sequence of BR2 and the paging of BR8, with the bounds and date refusals (AC2, AC3).
5. `TimelineController` with the 403, the 404, the empty state and the total (AC4, AC5, TC-E2-034-12).
6. `LedgerAppendClient` and the save panel: the key, the stored answer, the repeat and the 409 (AC7); then `IntakeResultClient` and the note (AC8).
7. The contract-fake run of every consumed answer in isolation, then the composite-route test with gateway-bff; and the read test on a case whose ledger holds 500 entries, first page inside 2 s (NFR-070), case indexes only.

**Feature switch.** None of its own: a case timeline must read and the operation has no off state. The save path is offered only where the append is reachable; elsewhere the timeline still reads and the save panel is not shown. The legacy flag `rwb.integration.ledger-channels` stays the integration slice's.

**Done when.** The tests of section 16 pass; a case whose ledger holds 500 entries returns its first page inside 2 s at the parameter page size; a save with one key writes one entry and a repeat writes none; a case outside scope answers 404 with MSG-P4-003 and a case with no entry answers total 0 with MSG-P3-024; no statement of the service reads `interaction`, an EFS list or an ACE view.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-024 | The case has no ledger entry | No interactions are recorded on this case yet. |
| MSG-P4-002 | A role without Case record R opens the timeline | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is outside the reader's scope | This case is not in your scope. |
| MSG-GEN-002 | The page size is out of bounds, or the type is outside the seven | {field} must be between {min} and {max}. |
| MSG-GEN-003 | The date `to` is before the date `from` | {field} cannot be before {other}. |
| MSG-GEN-006 | The ledger source does not answer inside the parameter timeout | {system} is not available. Your request is queued and will be retried. |

For MSG-GEN-006 {system} is "Interaction ledger", the display name the timeline contract gives rwb-source-data; for MSG-GEN-003 the fields are "to" and "from"; for MSG-GEN-002 the field is "size" or "type" with the parameter bounds; for MSG-P4-002 {action} is "read the timeline of this case" or "record an interaction on this case". MSG-P3-024 is new in the legacy story and keeps its text; the other texts are copied unchanged from the legacy story and the message catalogue. Thai text for each follows DL10.

### 15. Screens and states

The ledger section of SCR-04 Case timeline and of SCR-03 Case record, served by the gateway-bff composite route (DP-19) and built on the timeline page of RWB-P3-E2016-APP; the field list, layout and field-level masking are that contract's and change not here.

| Screen | State | What the user does |
|---|---|---|
| SCR-04 Case timeline | Loading | Sees skeleton rows while the composite route answers |
| SCR-04 Case timeline | Filtered | Filters by channel, source and date range, pages a long history, reads each item's source, channel, entry type and time |
| SCR-04 Case timeline | Empty | Reads MSG-P3-024 when the case has no entry, filters still shown and no error |
| SCR-04 Case timeline | Degraded | Reads the case events with the notice naming "Interaction ledger" when the ledger does not answer (BR12) |
| SCR-03 Case record | Read only, and Saving a call | Opens the timeline, records a call with its contact reference, channel and result, and sees it saved once; a repeat returns the first answer |

No screen shows a retention class, a decision log entry or another service's free text, and none shows a contact number or an address: the contact point is the masked reference.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-034-12 | AC5, BR9 | Component | A role without Case record R calls the timeline of "RW-2026-000301"; 403 with MSG-P4-002, nothing returned |
| TC-E2-034-01 | AC1, AC7, BR4, BR6 | Contract | One EFS action row with promise 12,500.00 for 20 December 2026; one Workbench call of 15 December 2026 09:30 to "PHONE:CP-SYN-0301-M" with NO_ANSWER; the append answers once under its key and the read returns both items with their source markers |
| TC-E2-034-02 | AC1, BR1 | Contract | One transfer from "U-2001" to "U-2002" on 16 December 2026 11:00; one instruction "INS-SYN-0301" to partner "LF-SYN-01" on 17 December 2026 14:00; the case event and the PARTNER_RESULT item with their holder references |
| TC-E2-034-03 | AC1, AC2, AC3, BR1, BR2 | End to end | The 3 entries of 14, 15 and 18 December 2026, the case event of 16 December 2026, two entries at one instant with case sequence 7 and 8; order, total, pages, source markers |
| TC-E2-034-04 | AC1, BR5 | Contract | NoticeDispatched and NoticeDelivered for "NT-SYN-0301" with barcode "EV000000001TH"; TreatmentApproved "TRT-SYN-0301"; ProceedsMatched "PRC-SYN-0301" of 5,000.00; LETTER, OFFER and PAYMENT types read as items |
| TC-E2-034-05 | AC7, BR4 | Contract | The same call saved twice with one `Idempotency-Key`; one entry, hit count 2, one item (the transport half is proved by RWB-P2-E2034-APP) |
| TC-E2-034-06 | AC8, BR10 | Contract | Three EFS rows of 14 December 2026: "PTP" for "ACC-SYN-0301", "SYS" unlisted, "PTP" for "ACC-SYN-0999" on no open case; 3 read, 1 written, 1 excluded, 1 not on a case through the P1 contract, one item on the timeline |
| TC-E2-034-07 | AC7, BR4, BR11 | Contract | The P1 append answers 503 and then succeeds: the timeline keeps its items and gains none in between; the retry with the same key writes one (the delivery half is proved by RWB-P2-E2034-APP) |
| TC-E2-034-08 | AC1, BR3 | Contract | InstructionIssued for a case that does not exist: no item on any timeline and no ledger row read from `rwb_case`; the exception queue is RWB-P2-E2034-APP's |
| TC-E2-034-09 | AC6, BR2 | Contract | The EFS row of contact time 14 December 2026 10:15 written on 15 December 2026 at 10:00 after the call of 09:30; the EFS item reads before the call |
| TC-E2-034-10 | AC4 | Component | Case "RW-2026-000302" with no entry; empty `items[]`, total 0, MSG-P3-024 |
| TC-E2-034-11 | AC2, AC5, BR8, BR9 | End to end | Case "RW-2026-000301" owned by "U-2002" in team "MTG-BKK" read by "U-3001" of "HP-NE" with Own scope: 404 and MSG-P4-003, no ledger read; a page size of 500 and a `to` before a `from` refused before any source |

The legacy level System maps to End to end and Access to Component, because this slice asserts a read composed from two owners and a refusal answered before any read. Legacy AC7 and AC8 are the integration slice's assertions, proved by RWB-P2-E2034-APP and listed here for the read side so the legacy key stays complete in one place. No `-ITG` suffix is used here: the integration copy is RWB-ITG-E2034-ITG, whose `TC-E2-034-01-ITG` to `TC-E2-034-12-ITG` prove the same facts with the real services. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID.

### 17. Guardrails

- No business value in code: source, channel and entry-type values, type labels, page bounds and source timeout are reference and parameter rows read through their contracts (BR5, BR8).
- No personal data in logs, tests or prompts: an item carries identifiers, codes and a contact key, never a number, an address or another party's amount; the contact reference is masked by role before it leaves the service and is never logged; all test data is synthetic.
- No read of another service's tables: the ledger, the EFS list, the retention classes and the intake summary come only through the P1 contract, and `interaction` is not a table of `rwb_case` (BR3, DP-01, DP-18). No ACE view is read here: only rwb-source-data reads the `recovery.v_ace_*` views.
- One hop, no chaining: the timeline never calls a downstream of a downstream; breaker and bulkhead are per downstream (DP-11).
- The entry is never written twice and never rewritten: the append is create-only, keyed by the request's `Idempotency-Key`, and a 409 is a repeat (BR4). The timeline writes no ledger row, copy, projection or event; its only row is the stored answer of its own append call (BR11).
- A refusal returns no data: no item, case number or contact reference, with the catalogue message ID and an RFC 9457 problem body; the case number on screen comes from the case contract, never from a copy.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ILG-006 | The ledger reads back in one ordered, filtered sequence through one interface | Business Requirements Epic 2, section 3.2 | FEAT-ILG-09 | 06 to 10 Recovery case processes | BR1; BR2 | TC-E2-034-03, TC-E2-034-09 |
| REQ-ILG-007 | The same event twice with the same key produces one entry, the repeat counted | Business Requirements Epic 2, section 3.2 | FEAT-ILG-06 | 06 to 10 Recovery case processes | BR4; R-UNI-40 | TC-E2-034-01, TC-E2-034-05 |
| REQ-ILG-008 | A failed ledger write loses no entry and the failure is visible | Business Requirements Epic 2, section 3.2 | FEAT-ILG-07 | 06 to 10 Recovery case processes | BR4; BR11 | TC-E2-034-07 |
| REQ-ILG-009 | Contact outcomes from collections reach the ledger | Business Requirements Epic 2, section 3.2 | FEAT-ILG-06 | 06 to 10 Recovery case processes | BR10; BR1 | TC-E2-034-01, TC-E2-034-06 |
| REQ-ILG-010 | Dispatched letters write their result, including proof of delivery | Business Requirements Epic 2, section 3.2 | FEAT-ILG-07 | 06 to 10 Recovery case processes | BR5 | TC-E2-034-04 |
| REQ-ILG-011 | A hand-over names who held the case, who holds it now and when | Business Requirements Epic 2, section 3.2 | FEAT-ILG-08 | 06 to 10 Recovery case processes | BR1 | TC-E2-034-02 |
| REQ-ILG-012 | The case record view shows the ledger as an ordered timeline | Business Requirements Epic 2, section 3.2 | FEAT-ILG-09 | 06 to 10 Recovery case processes | BR1; BR2; BR12 | TC-E2-034-03, TC-E2-034-10, TC-E2-034-11, TC-E2-034-12 |
| REQ-ILG-013 | Ledger entries carry their own retention class, independent of the decision log | Business Requirements Epic 2, section 3.2 | FEAT-ILG-10 | All recovery processes | BR7 | TC-E2-034-01 |
| REQ-ILG-014 | Personal data in the ledger is masked by role on the case record rules | Business Requirements Epic 2, section 3.2 | FEAT-ILG-06 | 06 to 10 Recovery case processes | BR6 | TC-E2-034-01, TC-E2-034-11 |

Every requirement of this legacy key is cited. REQ-ILG-007, REQ-ILG-008 and REQ-ILG-013 are proved here only for what this slice owns: the one-call write under its key, the absence of a half item when the write fails, and the retention class left to the entry's owner; their full proof is the rwb-source-data story of this key and the integration slice.

### 19. Out of scope

- The `interaction` table, its columns, its append-only trigger, its indexes, the append, the case-scoped read and the intake-result read: the rwb-source-data stories of this legacy key (DP-18); with them the EFS intake rule, the outcome list, the dedupe, the retention classes and the late-row write.
- The channel consumer, the mapper, the two workflows, the retry, the three-attempt exception rule and the exception queue screen SCR-09: RWB-P2-E2034-APP and its deployment story.
- The letter, its dispatch and proof of delivery; the payment and its matching; the offer and the treatment: RWB-P6-E2021-APP, the rwb-payment stories and the rwb-treatment stories; this slice shows their ledger entry and nothing of the objects.
- The full seven-type case timeline, the item-type rights filter, the queue history and the unavailable-source notice of SCR-04 (RWB-P3-E2016-APP); the roles, scope data, permission matrix, masking rows and refusals of rwb-access (RWB-P4-E2034-APP slice); the partner screens (rwb-partner stories); the composite route (RWB-PLT-N001-CON).
- The definition of the key's order across the real services: RWB-ITG-E2034-ITG.
