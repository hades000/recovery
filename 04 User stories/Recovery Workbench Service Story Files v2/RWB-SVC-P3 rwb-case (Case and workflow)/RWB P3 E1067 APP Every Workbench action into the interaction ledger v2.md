# RWB-P3-E1067-APP Every Workbench action into the interaction ledger

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1067-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-067 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | To be sized by the squad at refinement (DOR-RWB-P3-E1067-APP-16) |
| Patterns applied | DP01, DP03, DP07, DP09, DP11, DP15, DP18, DP19 |
| Parallel lane | L-P3-V |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P1-E1067-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (no FR mapped to REQ-ILG-005, REQ-ILG-002, REQ-ILG-007) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the case half of RWB-E1-067 becomes the producer of `rwb.case.CaseCreated.v1`, `rwb.case.CaseAllocated.v1`, `rwb.case.CaseTransferred.v1` and `rwb.case.TimerBreached.v1` on `rwb.case.events.v1` in schema `rwb_case`, each written to the outbox in the transaction of the action and keyed by caseId, while the listener, the entry, the duplicate table, the exception queue and the incident stay with rwb-source-data under DP-18. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P3-E1067-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (14 resolved, 15 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN) and the case workflow (SY-CASEWF)**, I want **the case created, allocated, transferred and escalated by the Workbench to reach the interaction ledger as one entry each, with the time and the actor that produced it**, so that **the case history shows what the Workbench did to my case between the customer contacts, in order, without anyone assembling it**.

This story is the `rwb-case` part of legacy RWB-E1-067 — the producer side of four ledger entries:

- Service `rwb-case`, schema `rwb_case`, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1`, task queue `rwb-case` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.case`.
- What this story owns is the ledger contract of four facts the service already publishes: a stable event ID, the idempotency key of the action, schema version 1, the occurred time and the actor in the header; the payload facts of each action and nothing else; the key caseId so the entries of a case keep their order; and the outbox row inside the transaction of the action.
- What it does not own, and must not build, is the ledger. The listener, the event-to-entry map, the duplicate service, the exception queue and the incident are rwb-source-data's in RWB-P1-E1067-APP; DOCUMENT_ATTACHED is rwb-document's in RWB-P5-E1067-APP; DECISION_TAKEN arrives from the shared decision-record topic. This service writes no `interaction` row for these actions (DP-18).
- The four actions belong to RWB-P3-E1018-APP (created by the entry rule), RWB-P3-E1020-APP (allocated), RWB-P3-E1021-APP (transferred) and RWB-P3-E1028-APP (escalated at a timer breach). This story adds the ledger contract of their events and its tests, and changes none of their rules.
- Entries a person records directly on a screen take the synchronous append of RWB-P3-E1066-APP, where the entry must come back in the same act. An action that both appends and publishes carries one idempotency key, so the ledger stores one entry and counts the second arrival (R-UNI-40).

The payloads carry references and codes only: case ID, case number, product group, queue and owner references, rule ID and version, timer type and escalation role. No person name, account number, identity number or contact detail is in a payload, a header or a log.

### 2. Business rationale

The Workbench creates, allocates, transfers and escalates cases by rule, often with no person involved and no caller waiting on a request. If those actions are not in the ledger, the case owner sees the customer contacts but not what the Workbench did between them: the case allocated overnight to another queue, the escalation a breach produced on 5 December. REQ-ILG-005 asks that every Workbench action on a case is written to the ledger as it happens, REQ-ILG-002 that every entry names the system or person that produced it, and REQ-ILG-007 that the same event twice with the same key gives one entry and counts the repeat.

Legacy RWB-E1-067 answered all three with one listener over one in-process outbox, mapping EV-01 to CASE_CREATED, EV-02 to CASE_ALLOCATED, EV-04 to CASE_TRANSFERRED and EV-19 to CASE_ESCALATED, and setting the source reference to "the owning module, event ID and event name" (legacy AC1 and AC2). In the target the same six events travel on three streams from three producers. The ledger does not move — DP-18 and the Template and Rules default ruling keep the writer and the entry in `rwb_source_data` — so the split changes what each service owes the listener. For rwb-case that debt is exact: a correct event, with a correct header, in the right order, in the same transaction as the action, once per action.

The architecture fixes each part of the debt. Every producer writes to its transactional outbox in its own schema in the same transaction as the state change, a relay publishes to its topic, the envelope is CloudEvents 1.0 in binary mode, the key is caseId, the registry keeps JSON Schema with BACKWARD compatibility, and every consumer dedupes in its inbox (Architecture v5 slide 11). The case topic carries the seven events of TSD P3 T5.3, the event catalogue names CaseCreated, CaseAllocated, CaseTransferred and TimerBreached (event 19) on `rwb.case.events.v1`, and JOB-11 Outbox sender runs every minute in every service (slide 44). The functional source states the same fact per action: "CaseCreated is published with case number RW-2026-000123" (AC-P3-004-01), "one CaseTransferred event is in the outbox" (AC-P3-040-01), and at a breach the timer is set EXPIRED and TimerBreached is published (AC-ALT-P3-011-01).

This slice carries no business decision of its own and needs none: it carries a contract. Its value is that the ledger can be trusted to be complete for case actions — the category produced by the workflow and the runs, with no request to piggyback on — without rwb-source-data reading `rwb_case`, without rwb-case writing `rwb_source_data`, and without either sharing a table (DP-01, DP-18).

### 3. Preconditions

- RWB-P1-E1067-CON is published: the listener, the event-to-entry map (EV-01 to CASE_CREATED, EV-02 to CASE_ALLOCATED, EV-04 to CASE_TRANSFERRED, EV-19 to CASE_ESCALATED), the duplicate rule of R-UNI-40, the Case record C authority behind the writer, the source reference form and the exception queue with owner RW-PLATADM. This service calls none of it (DP-11 as a contract dependency, not a call).
- RWB-PLT-TE006-CON is in place: the library that creates `outbox_event`, `processed_event` and `idempotency_key` in `rwb_case` and provides the relay client of JOB-11 (DP-09). The tables exist at the `rwb_case` baseline; this story writes no DDL for them.
- The four action stories are done or in the same wave: RWB-P3-E1018-APP writes the case row and CaseCreated, RWB-P3-E1020-APP the queue, owner and CaseAllocated, RWB-P3-E1021-APP the assignment and CaseTransferred, RWB-P3-E1028-APP the EXPIRED timer and TimerBreached.
- The topic `rwb.case.events.v1` exists with its retry topics and `.dlt` topic, and its JSON Schema registry subject is registered with BACKWARD compatibility (slide 11; RWB-PLT-TE006-CON). Each of the four types is at schema version 1.
- LOV-LEDGER-EVENT, LOV-PRODUCT, LOV-TIMER and LOV-TRANSFER-REASON are read through the reference-data contract of rwb-case (DP-07, H RWB-PLT-E1043-CON, C RWB-P3-E1043-CON); no list value is written in code.
- The `rwb_case` login holds SELECT and INSERT in `rwb_case` and no privilege on another schema (DP-02, DP-15); the login name is Not specified in the source documents (GAP-2257; ASM-3716).
- A manual transfer caller holds Queue and allocation U with the case in scope (API-P3-006); the workflow acts as SY-CASEWF and the allocation run as SY-RULES.
- The switch `rwb.case.ledger-events` can stop the four events without touching the action; off means the row and the decision record commit and no outbox row is written.
- The CloudEvents attributes that carry the idempotency key and the actor, the key format per event, the relay retry limit and the registry subject are Not specified in the source documents (GAP-2257; ASM-3716), (GAP-2257; ASM-3717) and (GAP-2257; ASM-3718).

### 4. Flow

1. Trigger: one of four actions commits in `rwb_case` — the entry rule creates the case, the allocation run gives it a queue and an owner, a transfer moves it, or the SERVICE_LEVEL durable timer reaches `expires_at`.
2. The action service writes its rows in one transaction: `recovery_case`, `assignment` or `timer` with its status and escalation, and the decision record through the decision-record library (DP-03).
3. `CaseLedgerEventFactory` builds the payload from the row it is given, not from a fresh read: caseId, caseNo, productGroup, accounts and businessDate for CaseCreated; caseId, queueId, ownerId, ruleId and ruleVersion for CaseAllocated; caseId, fromOwner, toOwner, reasonCode and ruleId for CaseTransferred; caseId, caseNo, timerId, timerType, expiresAt and escalateTo for TimerBreached.
4. `EventHeaderBuilder` sets the header: an event ID new for this action, the idempotency key of the action, schema version 1, the occurred time of the action and the actor — SY-CASEWF for the entry rule and the timer, SY-RULES for a rule allocation or transfer, the user id for a manual transfer, never a display name.
5. `CaseKeyedPartitioner` fixes the record key to caseId and asserts that the subject of the envelope and the key agree, so every event of one case lands on one partition and the written order of that case is preserved.
6. `OutboxEventWriter` inserts one row into `outbox_event` inside the same transaction, with the CloudEvents attributes and the payload, in state pending.
7. Commit. The action row, its decision record and its outbox row commit together or not at all; a rolled-back action leaves no event.
8. JOB-11 Outbox sender: the platform relay runs every minute, publishes every pending row to `rwb.case.events.v1` in the CloudEvents 1.0 binary envelope with acks=all, and marks the row published.
9. rwb-source-data listener: checks the schema version against the current and the previous version, maps the event to its entry code, sets the source system WORKBENCH, the source reference "P3 case and workflow, EV-02 CaseAllocated" (per event) and the actor from the header, and appends one entry with the next `case_seq` (RWB-P1-E1067-APP; not this story).
10. Redelivery: the same event arrives with the same event ID and key; the listener writes no second entry and adds one hit (R-UNI-40). This service produced nothing new.
11. A retried command: the transfer repeats with the same `Idempotency-Key`; the duplicate check returns the existing assignment and writes no second row and no second outbox row.
12. A second action on the same case: a new action row, event ID and key, keyed to the same caseId and published after the first, so the entries follow the order of the actions.

Two statements complete the flow for the reader who owns the other side. An event for an unknown case cannot come from this producer: the event is written in the transaction that creates the case or changes one that exists, and the reference sits inside `rwb_case`, so the legacy "case not found" path (legacy AC8) stays with the listener. A failed publish never loses an event: it stays in `outbox_event` in state pending, the relay retries it, and only the relay's own limit moves it to a failed state.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The action transaction rolls back after the payload is built | No action row, no decision record and no outbox row exist; no event is ever published for that attempt | None | AC3 |
| X2 | The same command is retried with the same `Idempotency-Key` | The existing assignment is returned; one outbox row stays; one entry in the ledger | None | AC3 |
| X3 | The payload cannot be built from the row (for example a timer type outside LOV-TIMER) | The transaction aborts on the payload rule; nothing moves; the reference version is the cause and is named in the log | None (build and action failure) | AC1 |
| X4 | Two instances take the same action at the same moment | One action row wins on its unique constraint, one outbox row exists, one entry results and one hit is counted | None | AC7 |
| X5 | The relay cannot reach the broker | The row stays pending; the next run publishes it once; no duplicate row and no duplicate event | None (relay incident, platform side) | AC3, AC5 |
| X6 | The registry rejects the schema version of the row | The relay does not publish; the row stays pending and the platform alerts on the registry subject | None (platform alert) | AC4 |
| X7 | The listener cannot append the entry | The listener retries and then moves the event to its own exception queue with an incident; this service has published as designed and the event is not lost | MSG-P1-022 (the listener's incident detail) | AC5 |
| X8 | An identity without Queue and allocation U calls the transfer | Refused before the action; no assignment row, no decision record and no event | MSG-P4-002 | AC2 |
| X9 | The case is outside the caller's scope | Refused with 404 on the transfer before the action; no row and no event | MSG-P4-003 | AC2 |

Rows X1 to X6 are properties of the action transaction and of the relay, quoted so the ledger reader knows when an event can be missing: an event exists exactly when its action row exists, apart from the deliberate case of the feature switch.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published rwb-source-data contract RWB-P1-E1067-CON, the outbox library RWB-PLT-TE006-CON and the four action stories, all contract or earlier work |
| Negotiable | The topic, the schema version, the relay interval and the retry limit are configuration; the story fixes the header, the payload, the key, the transaction and the entry map |
| Valuable | Every case action of the Workbench reaches the case history as one ordered entry with its time and actor, from the first day of wave 1 |
| Estimable | One event factory, one header builder, one partitioner, one outbox writer and one contract test over four event types |
| Small | Fits one sprint with its tests, as a secondary slice of the legacy key |
| Testable | Each criterion in section 7 is one automated test over the outbox row and the published envelope, with the ledger side stubbed |

### 7. Acceptance criteria

```gherkin
Feature: Every Workbench action into the interaction ledger — the rwb-case case-action events

  Background:
    Given the rwb-source-data contract mock returns the ledger write path of RWB-P1-E1067-CON for a received event
    Given the rwb-source-data contract mock returns that "rwb.case.CaseCreated.v1" maps to entry CASE_CREATED, "rwb.case.CaseAllocated.v1" to CASE_ALLOCATED, "rwb.case.CaseTransferred.v1" to CASE_TRANSFERRED and "rwb.case.TimerBreached.v1" to CASE_ESCALATED with source system "WORKBENCH"
    Given the rwb-source-data contract mock returns one entry per idempotency key and one hit for a key it has already seen

  Scenario: AC1 Case actions reach the ledger (new, D-RCV-60)
    Given the rwb-source-data contract mock returns the four entry codes of RWB-P1-E1067-CON
    Given case "RW-2026-000301" is created at 2026-12-01T06:10+07:00 by SY-CASEWF
    Given it is allocated to queue "MTG-BKK-CO" at 06:40 by SY-RULES
    Given it is transferred by user "u-teammgr-03" at 2026-12-03T14:05+07:00
    Given timer "SLA-ASSIGNED" is breached at 2026-12-05T08:00+07:00
    When each action commits
    Then four outbox rows hold "rwb.case.CaseCreated.v1", "rwb.case.CaseAllocated.v1", "rwb.case.CaseTransferred.v1" and "rwb.case.TimerBreached.v1" with an event ID, an idempotency key, schema version 1, the occurred time of the action and its actor
    And the payloads carry caseId "RW-2026-000301" with caseNo, productGroup, accounts and businessDate for CaseCreated; queueId, ownerId, ruleId and ruleVersion for CaseAllocated; fromOwner, toOwner, reasonCode and ruleId for CaseTransferred; timerId, timerType, expiresAt and escalateTo for TimerBreached
    And the rwb-source-data contract mock returns 4 entries for case "RW-2026-000301" with events CASE_CREATED, CASE_ALLOCATED, CASE_TRANSFERRED and CASE_ESCALATED
    And each entry carries the case identifier, the event, the timestamp and the actor
    And no payload, header, log line or test fixture carries a person name, an account number or an identity number

  Scenario: AC2 The entry names its source (new, D-RCV-60)
    Given the CASE_ALLOCATED entry of case "RW-2026-000301"
    When it is read
    Then it names source system "WORKBENCH", source reference "P3 case and workflow, EV-02 CaseAllocated" and actor "SY-RULES"
    And the CASE_TRANSFERRED entry names actor type "USER" and actor "u-teammgr-03"
    And the CASE_CREATED entry names actor "SY-CASEWF" and the CASE_ESCALATED entry names actor "SY-CASEWF"
    And a transfer by rule names actor "SY-RULES" and no entry ever carries a display name
    And an identity without Queue and allocation U is refused with MSG-P4-002 and a case outside the scope with MSG-P4-003, before any row is written

  Scenario: AC3 Nothing is written twice (new, D-RCV-60)
    Given CaseAllocated for case "RW-2026-000301" with idempotency key "EV-02-RW-2026-000301-20261201" was published
    When the same event arrives again with the same key
    And the transfer command is retried with the same Idempotency-Key
    Then one CASE_ALLOCATED entry and one CASE_TRANSFERRED entry exist
    And the hit count for key "EV-02-RW-2026-000301-20261201" is 1
    And rwb-case wrote one assignment row and one outbox row for the transfer

  Scenario: AC4 An event with an unknown schema version (new, D-RCV-60)
    Given CaseTransferred is at schema version 1 and the registry accepts the current and the previous version
    When a producer build would publish CaseTransferred at schema version 3
    Then the registry refuses the subject and the relay publishes nothing
    And the outbox row stays pending and the item is on the exception queue with owner RW-PLATADM and reason "schema version 3 not accepted"
    And the relay retry limit is read from the platform relay configuration
    And the listener accepts the current version 1 and the previous version, as the rwb-source-data contract mock returns

  Scenario: AC5 A ledger write fails for an event (new, D-RCV-60)
    Given every append of the listener fails
    When CaseTransferred for case "RW-2026-000301" is delivered
    Then the delivery is tried 4 times in all
    Then the event is in the exception queue of rwb-source-data with owner RW-PLATADM
    Then the listener raises incident "LEDGER_WRITE_FAILED" for case "RW-2026-000301"
    And the event is not lost on this side: its outbox row stays published and the incident detail is MSG-P1-022

  Scenario: AC6 Entries follow the order the events were written (new, D-RCV-60)
    Given CaseCreated and CaseAllocated for case "RW-2026-000301" are written to the outbox in that order
    When both are processed
    Then CASE_CREATED has case_seq 1 and CASE_ALLOCATED has case_seq 2
    And both records carry case "RW-2026-000301" as their key and share one partition
    And the transfer of 2026-12-03T14:05+07:00 and the breach of 2026-12-05T08:00+07:00 follow as case_seq 3 and case_seq 4

  Scenario: AC7 The same action on two threads at once (new, D-RCV-60)
    Given CaseCreated for case "RW-2026-000301" is delivered to two consumer threads at the same moment
    And the same case action is attempted by two instances at the same moment
    When both threads process it and both instances commit
    Then one CASE_CREATED entry exists and one "recovery_case" row and one outbox row exist
    Then the hit count for its key is 1

  Scenario: AC8 An event for a case that does not exist (new, D-RCV-60)
    Given no case with ID "00000000-0000-0000-0000-000000000998" exists in "rwb_case"
    When a producer build attempts to publish CaseCreated or TimerBreached for that case ID
    Then rwb-case writes no case row, no timer row and no outbox row, and refuses before an event exists
    And the rwb-source-data contract mock never receives an event of this service for a case that does not exist
    And the legacy listener path with reason "case not found" stays with RWB-P1-E1067-APP

  Scenario: AC9 An error answer of a provided operation is 401, 403 or 404 (new, D-RCV-60)
    Given a provided operation of rwb-case is called
    When the call has no valid identity, the identity lacks the right, or the case ID does not exist
    Then the answer is 401, 403 or 404
    And the code for each cause is Not specified in the source documents (NEWAC-RWB-P3-E1067-APP-AC10)

  Scenario: AC10 A consumed call fails or does not answer (new, D-RCV-60)
    Given the rwb-source-data contract mock fails or does not answer the delivery of an event
    When CaseCreated for case "RW-2026-000301" is delivered
    Then the event is not lost: its outbox row stays in the outbox and the relay retries it
    And rwb-case writes no ledger row for the failed call

  Scenario: AC11 Payloads, outbox write and ledger boundary hold (new, D-RCV-60)
    Given case "RW-2026-000301" is created at 2026-12-01T06:10+07:00 by SY-CASEWF
    When the action commits
    Then one outbox row for CaseCreated is written in the same transaction and JOB-11 Outbox sender publishes it every minute
    And the payload carries references and codes only: case, case number, product group, queue and owner references, rule and timer codes
    And no `interaction` row is written and no ledger writer is called from rwb_case for these actions
```

The eight criteria above are new and test only this deliverable: the header, the payload, the transaction, the key, the order, the version and the prohibition of a second ledger. No legacy criterion text is copied as a criterion; the legacy ACs 1 to 8 belong to RWB-P1-E1067-APP, which owns the listener, the map, the duplicate table, the exception queue and the incident, and to RWB-P5-E1067-APP for the document entry. The values reused are the ones the sources already carry: case "RW-2026-000301", the action times 2026-12-01T06:10+07:00, 06:40, 2026-12-03T14:05+07:00 and 2026-12-05T08:00+07:00, queue "MTG-BKK-CO", timer "SLA-ASSIGNED", the user id "u-teammgr-03", SY-CASEWF and SY-RULES, the entry codes, the source system "WORKBENCH" and the key "EV-02-RW-2026-000301-20261201".

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Case creation, allocation, transfer and escalation each reach the ledger as they happen; here one event per action, written in the transaction of the action (legacy BR1) | REQ-ILG-005; FSD P3 AC-P3-004-01, AC-P3-040-01, AC-ALT-P3-011-01; legacy BR1 |
| BR2 | Every entry names the system or person that produced it; the header carries the actor — a service identity for a rule action and a user id for a person — never a display name (legacy BR2) | REQ-ILG-002; TSD P3 T6.1; legacy BR2 |
| BR3 | The same action with the same key produces one entry and the repeat is counted; the producer keeps the event ID and key stable for one action (legacy BR3) | R-UNI-40; REQ-ILG-007; legacy BR3 |
| BR4 | Events for one case are processed in the order they were written; the case events are keyed by caseId and hold the written order of that case (legacy BR4) | Events rule "Ordering"; Architecture v5 slide 11; legacy BR4 |
| BR5 | A consumer failure retries and then goes to the exception queue with its owner; on this side the event waits in the outbox and is retried by the relay, never lost (legacy BR5) | Events rule "Failure"; R-UNI-36; legacy BR5 |
| BR6 | The producer writes schema version 1, the consumer accepts the current and the previous version, and the registry keeps BACKWARD compatibility (legacy BR6) | Events rule "Versioning"; Architecture v5 slide 11; legacy BR6 |
| BR7 | Event payloads carry references and codes and no personal data: case, case number, product group, queue and owner references, rule and timer codes (legacy BR7) | Events rule "Payload"; Architecture v5 slides 11 and 42; legacy BR7 |
| BR8 | DP-09: the event is written to the outbox in `rwb_case` in the same transaction as the action, and JOB-11 Outbox sender publishes it every minute | DP-09; Architecture v5 slides 11, 20 and 44 |
| BR9 | DP-18: the interaction ledger is rwb-source-data's; this story writes no `interaction` row, holds no ledger and calls no ledger writer | DP-18; Template and Rules R3 default ruling |

How the rules hold in `rwb-case`:

- BR1: one outbox row per committed action and no other path — no manual re-send and no batch that regenerates events for old cases; a case created in error is corrected by its case action story, not by a second creation event.
- BR2: `EventHeaderBuilder` takes the actor from the identity of the action and refuses to substitute a display name; TSD P3 T6.1 gives RW-TEAMMGR Queue and allocation CRUA and SY-CASEWF Case record CRU.
- BR3: both the event ID and the key derive from the action, so a redelivery carries the same pair and the unique key gives one entry and one hit; an action appended synchronously by RWB-P3-E1066-APP carries the same key, so the two paths still give one entry.
- BR4: the record key is caseId, so the events of a case share a partition, the relay's order per key becomes the written order, and the listener assigns `case_seq` in that order.
- BR5 to BR7: a failed publish leaves the row unchanged and is retried on the next minute; each type is published at the constant version 1 with a BACKWARD registry subject, so a version the registry does not hold is never published; each payload is built from a closed column list, and a personal-data pattern fails the build's test of AC1 (BR9 is a prohibition with an owner elsewhere, enforced by the negative test that no ledger table and no writer call exist in this service for these actions).

### 9. State transitions

No case transition is added: the four actions and their case transitions belong to their own stories. This story adds the lifecycle of one outbox row.

| From | Event | Condition | To |
|---|---|---|---|
| (no outbox row) | the action transaction commits | The action row, the decision record and the outbox row commit together | outbox row `pending` |
| pending | JOB-11 Outbox sender publishes the row to `rwb.case.events.v1` | The broker accepts with acks=all and the registry holds the schema version | `published` |
| pending | the publish fails (broker unreachable, registry refusal, timeout) | The row is unchanged and the next run retries it | `pending` |
| pending | the relay reaches its parameterised limit | The platform owns the item from this point; the event is not discarded | `failed`, and the relay incident is raised |
| published | a consumer redelivers the event | At-least-once delivery | `published`; no new row is written by this service |

Read-only, for the reader of the event: CaseCreated, CaseAllocated and CaseTransferred say the fact and its occurred time (status and stage stay in `rwb_case`, read only through the case contract), and TimerBreached says the timer was set EXPIRED with escalation level 1 and the role named in `escalateTo`, the case keeping its queue and owner. The action row and the outbox row share one transaction, so an action exists without its event only when the feature switch is off.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-CASEWF, case workflow module | Creates the case by the entry rule and escalates at a timer breach (Case record CRU); is the actor of CaseCreated and TimerBreached |
| SY-RULES, Drools evaluator | Takes the allocation and rule transfers (Case record R, Queue and allocation R) and is the actor of a rule allocation or transfer |
| RW-TEAMMGR, team manager | Transfers a case by hand with Queue and allocation U and reason code; is the actor of that CaseTransferred |
| RW-CASEOWN, case owner | Reads the entries through RWB-P3-E1035-APP and the P1 read on SCR-03; takes no action here |
| RW-PLATADM, platform administrator | Owns the exception queue item and the `.dlt` topic of `rwb.case.events.v1`; Case record R and Queue and allocation R |
| SY-AGENT, agent platform | Case record R: reads a case through the contract and may not create, allocate, transfer or escalate; it produces no event |
| The rwb-case service identity (the `rwb_case` login, DP-02) | Writes the action row, the decision record and the outbox row in one transaction, and runs the relay client of JOB-11 |
| Nobody | Writes an `interaction` row for these four actions, or names an actor in a request field; the actor is the session or workload identity |

The refusals are the transfer operation's and are quoted, not built, here: MSG-P4-002 without Queue and allocation U, MSG-P4-003 for a case outside the scope (404 on this operation). MSG-P1-022 belongs to the listener's incident.

Every REST operation of this story calls the rwb-access authorise check (DP-08) before the action runs, and the refusals above apply after that check.

### 11. Data

| BR Field ID | Table in `rwb_case` | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | `recovery_case` | id | Write (the action), then Read into the payload as caseId and as the record key |
| DF-CAS-002 | `recovery_case` | case_no | Write (the action), then Read into the payload as caseNo |
| DF-CAS-003 | `recovery_case` | product_group (LOV-PRODUCT) | Read into the CaseCreated payload as productGroup |
| DF-CAS-009 | `recovery_case` | owner_user_id | Read as ownerId and toOwner; never as a name |
| DF-CAS-010 | `recovery_case` | queue_id | Read into the CaseAllocated payload as queueId |
| DF-CAS-021 | `recovery_case` | rule_version | Read into the CaseAllocated payload as ruleVersion |
| DF-WRK-009 | `assignment` | id | Write (the action), then Read as the action reference of CaseAllocated and CaseTransferred |
| DF-WRK-012 | `assignment` | assignee_user_id | Read as fromOwner and toOwner references |
| DF-WRK-039, DF-WRK-040 | `assignment` | queue_id, transfer_reason_code (LOV-TRANSFER-REASON) | Read into the CaseTransferred payload as the queue and reasonCode |
| DF-WRK-027, DF-WRK-030, DF-WRK-032, DF-WRK-036, DF-WRK-043 | `timer` | id, timer_type (LOV-TIMER), expires_at, escalation_level, escalated_to_role | Read into the TimerBreached payload as timerId, timerType, expiresAt and escalateTo |
| DF-OPS-178 to DF-OPS-183 | `outbox_event` and `processed_event` (PLT library) | the outbox row: event ID, event type, key, CloudEvents attributes, payload, state, occurred time, actor; the inbox row | Write (the outbox row); Read (the inbox row in tests only) |
| DF-INT-014 to DF-INT-020 | `interaction`, schema `rwb_source_data` | event_code, actor_type, actor_ref, source_ref, idempotency_key, case_seq, decision_log_id | Never written here; named only as the listener's columns |

The action row and the event carry different things on purpose: `recovery_case` holds the exposure, the accounts, the parties and the prescription date; `assignment` holds the holder and the reason; `timer` holds the clocks. The events carry a closed list of references and codes, because the ledger needs to know *that* the Workbench acted, on which case, when and by whom, not what the customer owes. Field IDs are those in the Logical Data Model and Data Dictionary and TSD P3 T3.1.

### 12. Contract

#### 12.1 REST operations provided

No new path. The four events ride operations and runs of the `rwb-case` contract; this story changes none of their shapes and adds the outbox row inside their transaction.

| ID | Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|---|
| API-P3-006 | POST | `/cases/{caseId}/transfer` | Transfer the case to another owner or queue with a reason; request TransferRequest; response Assignment; errors 401, 403, 404, 409, 422, 503 | Queue and allocation, right U, scope applied | `Idempotency-Key` header |

The other three have no path: CaseCreated is written by the entry activity of `CaseWorkflow`, CaseAllocated by the allocation run, TimerBreached by the durable timer of RWB-P3-E1028-APP. A caller learns nothing new from the transfer response: no event ID, no outbox reference and no ledger reference is returned.

#### 12.2 REST operations consumed

None at run time. This service calls no service to publish an event and calls no ledger writer for these actions (DP-18). Two contracts are consumed as facts and fixtures:

| Fact | Owner | Story | Note |
|---|---|---|---|
| The ledger listener and its event-to-entry map (EV-01, EV-02, EV-04, EV-19), the duplicate rule and the exception queue | P1 rwb-source-data | RWB-P1-E1067-CON | The reason the events exist; this story neither calls it nor fixes its field names, and uses it as a stub in every test of section 7 |
| The read of the entries of one case | P1 rwb-source-data | RWB-P1-E1067-CON | Read by RW-CASEOWN through RWB-P3-E1035-APP and the P1 read, not by this service |

#### 12.3 Events published

| Event | Topic | Key | Envelope | Payload |
|---|---|---|---|---|
| `rwb.case.CaseCreated.v1` (EV-01) | `rwb.case.events.v1` | caseId | CloudEvents 1.0, binary mode, `application/json` | caseId, caseNo, productGroup, accounts, businessDate |
| `rwb.case.CaseAllocated.v1` (EV-02) | `rwb.case.events.v1` | caseId | same | caseId, queueId, ownerId, ruleId, ruleVersion |
| `rwb.case.CaseTransferred.v1` (EV-04) | `rwb.case.events.v1` | caseId | same | caseId, fromOwner, toOwner, reasonCode |
| `rwb.case.TimerBreached.v1` (EV-19) | `rwb.case.events.v1` | caseId | same | caseId, timerId, escalateTo |

The attributes are fixed below; the ones that carry the idempotency key and the actor are Not specified in the source documents (GAP-2257; ASM-3716), and so is the registry subject (GAP-2257; ASM-3718).

| Attribute | Value |
|---|---|
| `specversion` | `1.0` |
| `id` | The event ID: one per committed action, stable across every redelivery of that action |
| `source` | The rwb-case service identity and the service path that produced the event |
| `type` | One of the four types above |
| `subject` | The case ID, so the subject of the envelope and the record key agree |
| `time` | The occurred time of the action: 2026-12-03T14:05+07:00 in the criterion, never the publish time |
| `datacontenttype` | `application/json` |
| `dataschema` | The registry subject of the type at schema version 1 |
| extension: the idempotency key | The key of the action, stable across a redelivery and new for a new action; the format follows the legacy example `EV-02-RW-2026-000301-20261201` (ASM-3716) |
| extension: the actor | "SY-CASEWF", "SY-RULES" or the user id of a manual transfer (ASM-3716) |

```yaml
asyncapi: 3.0.0
info: { title: rwb.case events, version: 1.0.0 }
channels:
  rwb.case.events.v1:
    address: rwb.case.events.v1
    messages: { CaseCreated: {}, CaseAllocated: {}, CaseTransferred: {}, TimerBreached: {} }
components:
  messages:
    CaseCreated:
      payload: { required: [caseId, caseNo, productGroup, accounts, businessDate],
        properties: { caseId: {type: string}, caseNo: {type: string}, productGroup: {type: string},
                      accounts: {type: array, items: {type: string}}, businessDate: {type: string, format: date} } }
    CaseAllocated:
      payload: { required: [caseId, queueId, ownerId, ruleId, ruleVersion],
        properties: { caseId: {type: string}, queueId: {type: string}, ownerId: {type: string},
                      ruleId: {type: string}, ruleVersion: {type: string} } }
    CaseTransferred:
      payload: { required: [caseId, fromOwner, toOwner, reasonCode],
        properties: { caseId: {type: string}, fromOwner: {type: string}, toOwner: {type: string},
                      reasonCode: {type: string} } }
    TimerBreached:
      payload: { required: [caseId, timerId, escalateTo],
        properties: { caseId: {type: string}, timerId: {type: string},
                      escalateTo: {type: string} } }
```

The other three events of TSD P3 T5.3 — CaseAllocationFailed, CaseStateChanged and TimerDue — are not ledger events and are untouched here; TimerDue is retired as a timer inside the workflow (RWB-P3-E1028-APP). The registry subject is registered with BACKWARD compatibility: a new optional field keeps version 1 readable for the listener.

#### 12.4 Events consumed

None. This story subscribes to no topic and creates no consumer group in `rwb_case`; the inbox table exists by the library and is written by no path of this story.

#### 12.5 Workflows and activities

| Workflow or run | Step | Story | What this story adds |
|---|---|---|---|
| `CaseWorkflow` (queue `rwb-case`) | entry activity that writes `recovery_case` | RWB-P3-E1018-APP | the CaseCreated outbox row in the same transaction |
| `CaseWorkflow` | allocation step that writes queue, owner and `assignment` | RWB-P3-E1020-APP | the CaseAllocated outbox row |
| `CaseWorkflow` | transfer step that ends and writes `assignment` | RWB-P3-E1021-APP | the CaseTransferred outbox row |
| `CaseWorkflow` | SERVICE_LEVEL durable timer at `expires_at` | RWB-P3-E1028-APP | the TimerBreached outbox row |

No workflow, activity, worker or task-queue entry is added: the write is a service call inside a transaction that already exists.

#### 12.6 Schedules

None for this story. The morning case creation and the allocation run are the Schedules of RWB-P3-E1018-APP and RWB-P3-E1020-APP (JOB-02, JOB-03), and the durable timers are Temporal timers of RWB-P3-E1028-APP. The outbox relay is the platform's one-minute Schedule — JOB-11 Outbox sender, owner "every service" (slide 44).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `recovery_case` | P3 (`rwb_case`) | The case the events describe; written by the action stories, read here for the payload |
| `assignment` | P3 (`rwb_case`) | The holder, queue and reason of an allocation or transfer; written by the action, read here |
| `timer` | P3 (`rwb_case`) | The timer, its expiry and escalation; written by the breach, read here |
| `outbox_event` | PLT library, created in `rwb_case` | One row per action, written in the action transaction (DP-09) |
| `processed_event` | PLT library, created in `rwb_case` | The inbox; present and empty, because this story consumes nothing |
| `idempotency_key` | PLT library, created in `rwb_case` | The key of the transfer operation, so a retried command writes one row and one event |

No foreign-schema table is read (DP-01); this service never reads `rwb_source_data`, and `interaction` belongs to rwb-source-data in its own schema.

#### 12.8 Contract fakes

| Fake | Story | Used for |
|---|---|---|
| rwb-source-data ledger fake | RWB-P1-E1067-CON | The four entry codes, the source reference form, the one-entry-per-key and hit answers of every criterion, and the failing append of AC5 |
| outbox and relay stub | RWB-PLT-TE006-CON | A pending row that the stub publishes, a publish that fails once and then succeeds (X5), and a registry refusal (X6) |
| case action fixtures | RWB-P3-E1018-APP, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1028-APP | A committed case row, an assignment row, a timer row at EXPIRED, and the rolled-back transaction of X1 |
| reference-data fake | RWB-P3-E1043-CON (through RWB-PLT-E1043-CON) | LOV-LEDGER-EVENT, LOV-PRODUCT, LOV-TIMER and LOV-TRANSFER-REASON with their values |
| parameters fake | RWB-P3-E1042-CON | The relay interval and the retry limit as versioned rows |
| decision-record stub | RWB-PLT-E1027-CON | The decision record written in the action transaction, and the failed record that aborts the action |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided (unchanged), 0 consumed | The transfer of `rwb-case` on `/api/recovery/case/v1`; no outbound call, one hop within 2 s |
| Kafka | 4 published, 0 consumed | CaseCreated, CaseAllocated, CaseTransferred and TimerBreached on `rwb.case.events.v1`, key caseId, CloudEvents binary mode |
| Temporal | None new | No workflow, activity or Schedule; the events are written inside existing activity and timer transactions |
| File | None | No file is read or written |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `ledgerevents`, Java package `th.co.scb.ace.workbench.recovery.case.ledgerevents`.

| Component | Type | Responsibility |
|---|---|---|
| CaseLedgerEventFactory | Service | Builds one of the four payloads from the committed action row, from a closed column list, and refuses a code outside its list |
| EventHeaderBuilder | Service | Sets the event ID, the idempotency key of the action, schema version 1, the occurred time and the actor from the identity of the action |
| CaseKeyedPartitioner | Service | Fixes the record key to caseId and asserts that the subject of the envelope and the key agree |
| OutboxEventWriter | Service | Inserts one `outbox_event` row in the caller's transaction in state pending; idempotent for a retried command |
| LedgerEventContractTest | Test component | Asserts each envelope against the AsyncAPI fragment, the registry subject and the ledger fake: attributes, key, payload, version and entry code |

**Database and migrations.** None, and that is the DP-15 statement: the per-service Flyway sequence of `rwb_case` is not extended. `outbox_event`, `processed_event` and `idempotency_key` are created by the platform library at the `rwb_case` baseline (RWB-PLT-TE006-CON, H RWB-PLT-E1044-CON), and this story writes rows, not DDL.

**Configuration.**

- `rwb.case.events.topic` = `rwb.case.events.v1`, with the retry and `.dlt` topics named by the naming library; `rwb.case.events.schema-version` = 1 per type; a version outside the registry is never published.
- `rwb.case.events.relay-interval` is the platform's one-minute Schedule of JOB-11, read as a property; `rwb.case.events.retry-limit` is read as a parameter whose value is Not specified in the source documents (GAP-2257; ASM-3717). The consumer cadence of NFR-026 (1 min, 10 min, 1 h, then the dead-letter topic) belongs to RWB-P1-E1067-APP.
- `rwb.case.events.idempotency-key` selects the derivation of the key from the action; the exact format is Not specified in the source documents (GAP-2257; ASM-3716); the registry subject and the AsyncAPI path are Not specified in the source documents (GAP-2257; ASM-3718).
- Switch `rwb.case.ledger-events`, read as a parameter: off means the action commits and writes no outbox row; it is never left off in SIT or production and is visible in the runbook.

**Build steps**

1. `CaseLedgerEventFactory` with one builder per action and a test per forbidden field (no exposure, account number, party reference or contact detail); a code outside its list aborts the transaction (X3).
2. `EventHeaderBuilder` with the event ID, key, occurred time and actor; tests for AC1 and AC2, including a rule transfer and a manual transfer.
3. `CaseKeyedPartitioner` and the key assertion; test that the events of one case carry the same key and are published in commit order (AC6).
4. `OutboxEventWriter` inside the action transactions, with the rollback (X1), retried command (X2) and two-instance (X4) tests.
5. The AsyncAPI fragment and the registry registration with BACKWARD compatibility; `LedgerEventContractTest` over the four types and entry codes (AC1, AC4) and the "outside the registry" path (X6).
6. The JOB-11 relay wiring with the pending-to-published loop and the parameterised limit (AC3, AC5), then the contract-fake run of RWB-P1-E1067-CON so the four entries, the source reference and the hit are proven before the listener is live, and the same run on the real topic in SIT.

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

This is a secondary slice: it adds no new build dependency of its own. Metadata "Depends on (build)" stays `None` and "Contract dependencies" stays `RWB-P1-E1067-CON` exactly as the Work Package fixes them, and the platform libraries of DP-03, DP-07, DP-09, DP-15 and DP-19 arrive with the baseline of `rwb_case`. DP-09 carries the story — the outbox, the relay client of JOB-11 and the topic with its retry and `.dlt` topics. DP-18 is the prohibition: no ledger for these actions and no writer call. DP-11 is the one-hop transfer call, which answers in its own thread within 2 s and chains nothing.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-022 | The listener could not append the entry; carried on the listener's incident and exception queue item | The entry was not saved because the interaction ledger could not be written. Try again in a few minutes. |
| MSG-P4-002 | An identity without Queue and allocation U calls the transfer | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is outside the caller's scope | This case is not in your scope. |

Thai text for each message follows decision DL10. The first message is rwb-source-data's and appears here as the text the consumer side shows; this story adds no message of its own.

### 15. Screens and states

No screen in this story. The case owner reads the entries on SCR-03 Case record through the timeline of RWB-P3-E1035-APP (Read only), and the platform administrator sees a failed or unaccepted event on SCR-09 Exception queue (List) through the listener's item.

| Surface | State in this story | What changes |
|---|---|---|
| SCR-03 Case record, timeline panel | Read only; loading as Screen Specifications v1 SCR-03; empty, error and no access: Not specified in the source documents (CG-ALL-3906) | Four item types appear as their actions happen: created, allocated, transferred, escalated |
| SCR-09 Exception queue | List; loading as Screen Specifications v1 SCR-09; empty, error and no access: Not specified in the source documents (CG-ALL-3908) | An item appears only when the listener or the relay fails; its owner is RW-PLATADM |
| SCR-05 Transfer case | Read and update; empty, loading, error and no access: Not specified in the source documents (CG-ALL-3907) | Unchanged: the same TransferRequest and the same Assignment |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-067-01 | AC1, BR1, BR7, BR8 | Contract | Four synthetic actions for case RW-2026-000301, one per event type |
| TC-E1-067-02 | AC2, BR2 | Contract | CASE_ALLOCATED and CASE_TRANSFERRED envelopes, their source reference and actor |
| TC-E1-067-03 | AC3, BR3 | Component | CaseAllocated delivered twice with key EV-02-RW-2026-000301-20261201; a transfer retried |
| TC-E1-067-04 | AC4, BR6 | Contract | CaseTransferred at schema version 3 against the registry; relay pending-to-published loop with retry limit read from platform relay configuration |
| TC-E1-067-05 | AC5, BR5 | Component | Listener append forced to fail; 4 attempts in all; exception queue and incident |
| TC-E1-067-06 | AC6, BR4 | Contract | CaseCreated then CaseAllocated in the outbox; case_seq 1 and 2 |
| TC-E1-067-07 | AC7, BR3 | Component | One event on two consumer threads; one action attempted by two instances |
| TC-E1-067-08 | AC8 | Component | CaseCreated and TimerBreached for an unknown case ID |
| TC-E1-067-09 | Access | Component | SY-AGENT and a user without Queue and allocation U; refused with MSG-P4-002 |
| TC-E1-067-10 | 12.7, BR9 | Component | Read and write attempts on `interaction` and on rwb_source_data tables from the rwb_case login; each refused |
| TC-E1-067-11 | BR2, 12.3 | Contract | Relay envelope of a CaseAllocated event asserted against the AsyncAPI fragment of section 12.3; actor extension attribute present |
| TC-E1-067-12 | AC9 | Contract | Not specified in the source documents (NEWAC-RWB-P3-E1067-APP-AC10) |
| TC-E1-067-13 | AC10 | Component | rwb-source-data contract mock forced to fail or not answer one CaseCreated delivery for case RW-2026-000301 |
| TC-E1-067-14 | AC11, BR7, BR8, BR9 | Component | CaseCreated committed for case RW-2026-000301; outbox row, payload fields and attempted writes to `interaction` from the rwb_case login |

The legacy test case IDs are kept so the test masters stay traceable; the level is the target's, and the full Given, When and Then of each is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID. No `-ITG` copy exists here: the cross-service proof is RWB-ITG-E1067-ITG.

### 17. Guardrails

- No business value in code: the event-to-entry map, the topic, the schema version, the relay interval and the retry limit are configuration and reference data; the payload field lists are the contract's.
- No personal data in events, workflow inputs, logs or tests: the payloads carry case, queue, owner, rule, timer and role references and codes only; test data is synthetic.
- ACE data only through the owner's contract or the `v_ace_*` views; this story reads no ACE view and no foreign schema (DP-01, DP-05).
- The listener never acknowledges an event it has not written or moved to the exception queue, and this service never commits an action whose outbox row is missing.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ILG-005 | Every Workbench action on a case writes to the ledger as it happens | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-01 | All recovery processes | R-UNI-36 | TC-E1-067-01, TC-E1-067-04, TC-E1-067-05, TC-E1-067-06, TC-E1-067-08 |
| REQ-ILG-002 | Every entry carries case, event, time, actor and source | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-01 | All recovery processes | None | TC-E1-067-02 |
| REQ-ILG-007 | The same event twice with the same key gives one entry; the repeat is counted | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-04 | All recovery processes | R-UNI-40 | TC-E1-067-03, TC-E1-067-07 |

### 19. Out of scope

- The ledger store, the listener, the event-to-entry map, the duplicate table, the exception queue and the incident (RWB-P1-E1066-APP and RWB-P1-E1067-APP).
- The DOCUMENT_ATTACHED entry and its event (RWB-P5-E1067-APP), and the DECISION_TAKEN entry, which arrives from the shared decision-record topic.
- The synchronous append a person records on a screen and its link row (RWB-P3-E1066-APP, RWB-P3-E2034-APP), and the timeline read itself (RWB-P3-E1035-APP, RWB-P3-E2016-APP).
- The other case events of TSD P3 T5.3 that are not ledger entries: CaseAllocationFailed, CaseStateChanged and the retired TimerDue.
- The cross-service proof of the four entries (RWB-ITG-E1067-ITG).
