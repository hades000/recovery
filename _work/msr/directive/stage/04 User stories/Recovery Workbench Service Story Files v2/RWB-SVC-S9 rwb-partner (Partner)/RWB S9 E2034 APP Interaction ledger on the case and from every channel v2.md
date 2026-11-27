# RWB-S9-E2034-APP Interaction ledger on the case and from every channel

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: the rwb-partner slice of legacy RWB-E2-034, split for the microservice estate. This story owns the partner half of the ledger: the ledger-facing attributes of the service's two facts, `InstructionIssued` (EV-20) and `PartnerResultSubmitted` (EV-21), published once each, keyed on the case ID, written in the same transaction as the change and its decision record, with who held the case before and after, the channel, the direction and the time, and with the contact point left as a reference. The ledger store, the retention class and the ordered timeline read are rwb-source-data's by the default ruling (DP-18); the fact-to-entry mapping and the composed timeline are rwb-integration's in `RWB-P2-E2034-CON`; the EFS read step of the legacy story belongs to rwb-source-data; the letters, offers and payments belong to rwb-comms and rwb-payment. No source publishes the payload of either event; `partner_instruction` has no ledger column; and the Work Package's H row is empty while the pattern set names ten platform contracts, all recorded in the registers (GAP-3149; ASM-5530 to ASM-5533). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S9-E2034-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 27 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S9-E2034-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-034 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Set by the squad at refinement (DOR-RWB-S9-E2034-APP-16) |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP08, DP09, DP10, DP11, DP13, DP15, DP18, DP19 |
| Parallel lane | L-S9-E |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E2034-CON; contract version Not specified in the source documents (DOR-RWB-S9-E2034-APP-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to REQ-ILG-009, REQ-ILG-010, REQ-ILG-011, REQ-ILG-012, REQ-ILG-013, REQ-ILG-014, REQ-ILG-007, REQ-ILG-008, REQ-ILG-006) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **the hand-over of a case to a partner and the result the partner returns announced once, with who held the case before and after, the channel, the direction, the source and the time, and with the contact point left as a reference**, so that **the one ledger shows the partner channel beside the EFS and Workbench entries and a contact is not found and then lost again**.

This is the rwb-partner slice of legacy RWB-E2-034. The legacy story writes seven event types and one EFS read into a single ledger inside the monolith; under D-RCV-60 the ledger is rwb-source-data's (DP-18), the read and the ordered timeline are rwb-source-data's, the mapping of a fact to a ledger entry and the composed timeline are rwb-integration's in `RWB-P2-E2034-CON`, and the EFS action rows are the source-data service's. What is left, and what only this service can state, is the partner fact itself:

- the two facts of the service, `rwb.partner.InstructionIssued.v1` (EV-20) and `rwb.partner.PartnerResultSubmitted.v1` (EV-21) on `rwb.partner.events.v1`, extended additively with the ledger attributes `eventCode`, `channel`, `direction`, `occurredAt`, `source`, `fromHolderRef` and `toHolderRef`, keyed on the case ID, in the CloudEvents envelope of the outbox library (DP-09);
- one read-only view `v_partner_ledger_fact` in `rwb_partner` over `partner_instruction` and `partner`, with its index, from which the fact is built (DP-01, DP-15);
- the transaction rule: the instruction row or the result, the local decision record and the outbox row commit together or not at all (DP-03);
- the emitter stays with the stories that first issue the instruction (RWB-S9-E6031-APP, RWB-S9-E6034-APP) and the story that takes the result (RWB-S9-E6033-APP); this story fixes the payload they write and asserts it against the contract (DP-11).

What this story does not own: the interaction table, the retention class, the ordered timeline read and the EFS read step (rwb-source-data, DP-18); the mapping and the composed timeline (rwb-integration, `RWB-P2-E2034-CON`); the letters, deliveries, offers and payments of the legacy criteria (rwb-comms and rwb-payment); the instruction operations API-S9-002 to API-S9-006 and their screens (the S9 instruction stories); and the end-to-end proof across rwb-partner, rwb-integration and rwb-source-data, which is `RWB-ITG-E2034-ITG`.

### 2. Business rationale

Contact outcomes from collections, letters sent through WIN and work held by partners sit in different systems, so a case owner who picks up a case does not know which number answered or who held the case last; for cases that came from EFS the share of open cases with a visible last right-party contact is zero (legacy section 2). The legacy story answered that with one ledger and one timeline. The split does not change the question; it changes who can answer it truthfully. A partner is instructed by a service that holds the instruction row, and a partner returns a result to that same service, so the only place where "who held the case, since when, under which channel and with which direction" is a fact and not a copy is `rwb_partner` (context pack ownership rows: `partner`, `partner_instruction`, EV-20 and EV-21).

Three target facts shape the slice.

1. **A fact, not a ledger row.** The ledger is another service's table by the default ruling (DP-18), and one service never reads another's schema (DP-01). So the partner channel travels as an event with identifiers and codes, and the entry, its retention class and its order are written and owned downstream. Sending more than the attributes the consumer element needs would copy a ledger into an event.
2. **A hand-over has two holders.** Legacy BR2 and AC2 say a hand-over to a partner names the holder before and the partner after, with channel PORTAL and direction OUTBOUND, and a partner result is INBOUND on the same channel. Those two values are the whole reason the partner channel is legible on the timeline: without them the timeline shows that something happened to the case and not that a firm took it.
3. **No contact point leaves the service.** Legacy BR5 stores the contact point as a reference to `v_ace_contact.contact_key` and forbids copying the number or the address. `partner_instruction` holds no contact column (TSD S9 T3.1), and this service holds no ACE grant, so the fact carries no contact value at all and the ledger resolves the reference through rwb-source-data (DP-05). The rule is met by omission, which is the strongest form it can take.

The slice serves REQ-ILG-011 (a hand-over names who held the case, who holds it now and when), REQ-ILG-014 (the contact point is a reference) and REQ-ILG-007 and REQ-ILG-008 (one entry per key, and no entry lost on a failure) at the producer end; the ledger rows, the ordering and the retention class are the consumers' and are traced in their own stories.

### 3. Preconditions

- `RWB-P2-E2034-CON` is published: the consumer element of the partner fact, its required attributes, the composed timeline element and its fake. This story builds against that fake on Day 1 and adds no operation to it (§R5.4, §R5.7).
- The platform libraries are on the service template: the local decision-record library (DP-03, RWB-PLT-E1027-CON), the outbox and inbox library with the CloudEvents envelope (DP-09, RWB-PLT-TE006-CON), the reference-data client (DP-07, RWB-PLT-E1043-CON), the parameters client (DP-06, RWB-PLT-E1042-CON), the authorise guard (DP-08, RWB-PLT-E1037-CON), the per-service Flyway sequence (DP-15, RWB-PLT-E1044-CON) and the gateway-bff composite route (DP-19, RWB-PLT-N001-CON). None of them is written into the H row of this secondary slice (GAP-3149; ASM-5532).
- `rwb_partner` and its login exist and the baseline carries `partner` (DF-PRT-001 to DF-PRT-007) and `partner_instruction` (DF-PRT-008 to DF-PRT-016) with the standard record columns of TSD S9 T3.0.
- A sibling operation commits an instruction or a result with its `Idempotency-Key`: API-S9-002 (issue), API-S9-005 (result). Both write the decision record before the change; this story writes the fact in that same transaction (DP-03).
- The lists LOV-LEDGER-EVENT with `HANDOVER` and `PARTNER_RESULT`, LOV-CHANNEL with `PORTAL`, LOV-DIRECTION with `OUTBOUND` and `INBOUND` and LOV-SOURCE with `WORKBENCH` are read at the version in force through the reference-data contract (legacy BR1, BR2, BR4; DP-07). Their row names and keys are Not specified in the source documents (GAP-3149; ASM-5533).
- The retry bound after which a fact goes to `rwb.partner.events.v1.dlt` is a parameter row; the legacy story names a retry limit of 3 and no parameter row (GAP-3149; ASM-5535).
- No approval stop: the FSD S9 is "In review" and the legacy story "Ready for build"; this story is Draft (realignment v1) (ASM-5539).
- Open decision DL10 remains open; its assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 are confirmed by the programme directive of 26 November 2026.

### 4. Flow

1. A sibling operation starts the change: API-S9-002 issues an instruction, API-S9-005 takes a result, each with its `Idempotency-Key` and its decision record written in the transaction (DP-03).
2. The guard library has already resolved the caller and its right, and the cached decision carries the caller's holder reference; the fact takes `fromHolderRef` from that decision and never from the request body (DP-08; BR2).
3. `LedgerFactReader` reads the instruction and its firm from `v_partner_ledger_fact` in `rwb_partner` — the instruction reference, the case reference, the partner reference and code, the instruction type, `instructed_at`, `due_at`, the status and `result_code` (DP-01).
4. `LedgerAttributeResolver` reads the lists at the version in force and resolves the fact to its `eventCode` (`HANDOVER` for an issue, `PARTNER_RESULT` for a result), its `channel` (`PORTAL`), its `direction` (`OUTBOUND` for an issue, `INBOUND` for a result) and its `source` (`WORKBENCH`) (DP-07; BR1, BR3, BR9).
5. `LedgerFactAssembler` builds the payload: the ledger attributes of step 4, `occurredAt` from `instructed_at` or the submitted time, `fromHolderRef` from the decision, `toHolderRef` as `PARTNER:<partner_code>` for a hand-over and as the same firm reference for a result, and the identifiers of step 3. No name, no contact value, no amount (BR10).
6. `LedgerFactOutbox` writes one row of `rwb.partner.events.v1` in the open transaction, keyed on the case ID, with the schema of the fact (DP-09).
7. The transaction commits: the instruction row or the result, the decision record and the outbox row together; a refusal of any of them writes nothing (AC4, BR6).
8. The relay publishes the fact once; the consumer of `RWB-P2-E2034-CON` maps it to the ledger entry and rwb-source-data writes it with its retention class in its own schema (not built here; BR8).
9. The case timeline shows the partner entry through the gateway-bff composite route of the edge; this service serves no timeline read (DP-19; AC3).
10. A repeat under the same key returns the first answer and writes no second fact; the repeat is counted (AC5, BR5).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The outbox insert refuses | The whole transaction rolls back: no instruction change, no record, no fact | MSG-P7-003 of the sibling operation | AC4 |
| X2 | The same fact is replayed or the same `Idempotency-Key` is submitted twice | One outbox row and one event exist; the repeat is counted | None | AC5 |
| X3 | The consumer keeps refusing the fact past the retry bound | The delivery goes to `rwb.partner.events.v1.dlt` with a task for RW-PLATADM | None | AC4 |
| X4 | The list or the parameter read misses the 2 s budget, or its breaker is open | Nothing is written; one retry with jitter; no fact is built on a guessed value | MSG-GEN-006 | AC7 |
| X5 | A caller without the Partner portal right, or a case outside its scope | Refused before a row is read; no fact is built | MSG-P4-002, MSG-P4-003 | AC6 |
| X6 | A list member of the version in force has no row for a fact | The fact is refused; no event is built from a code that is not in force | Not specified in the source documents (GAP-3149; ASM-5533) | AC3 |
| X7 | A component or a test reaches `interaction`, `recovery_case`, the ACE views or another `rwb_*` schema | The grant refuses the statement and the boundary test fails the build | None (pipeline log) | AC8 |

X1 to X3 are the failure paths legacy BR7 and BR8 name, moved to the producer of the fact; X4 to X7 are the platform rules of the split.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against the `RWB-P2-E2034-CON` fake and the template libraries; it waits for no in-lane story and changes no operation |
| Negotiable | The payload element names, the view name and the activity name are this story's; the codes, channels, directions and sources are list rows read at their version |
| Valuable | The partner channel of a case becomes visible once, with its two holders, and nothing about the customer leaves the service |
| Estimable | One view, one resolver, one assembler, one outbox adapter and one contract test per fact |
| Small | Fits one sprint as a secondary slice beside the instruction and result stories it extends |
| Testable | Each criterion runs on synthetic instructions and results through the contract fakes, plus the rollback, repeat, refusal and boundary cases |

### 7. Acceptance criteria

```gherkin
Feature: Interaction ledger on the case — the rwb-partner facts

  Background:
    Given the rwb-integration ledger-contract mock returns the consumer element of the partner fact and the composed timeline
    Given the rwb-case reference-data contract mock returns LOV-LEDGER-EVENT with "HANDOVER" and "PARTNER_RESULT", LOV-CHANNEL with "PORTAL", LOV-DIRECTION with "OUTBOUND" and "INBOUND" and LOV-SOURCE with "WORKBENCH" at the version in force
    Given the rwb-access contract mock returns the Partner portal right C with holder "USER:U-2002" and team scope "MTG-BKK"

  Scenario: AC1 A hand-over to a partner is announced with who held the case before and after (new, D-RCV-60)
    Given instruction "INS-SYN-0301" is issued to partner "LF-SYN-01" on case "RW-2026-000301" by holder "USER:U-2002" on 17 December 2026 14:00
    When the instruction transaction commits
    Then exactly one outbox row holds rwb.partner.InstructionIssued.v1 keyed on "RW-2026-000301"
    Then the payload holds eventCode "HANDOVER", channel "PORTAL", direction "OUTBOUND", source "WORKBENCH", occurredAt 17 December 2026 14:00, fromHolderRef "USER:U-2002" and toHolderRef "PARTNER:LF-SYN-01"
    Then the instruction reference, the case reference, the partner reference, the instruction type and the due date are the only other values
    Then this service writes no interaction row, no retention class and no ledger entry

  Scenario: AC2 A partner result is announced inward and carries no contact point (new, D-RCV-60)
    Given partner "LF-SYN-01" returns a result on "INS-SYN-0301" entered on 18 December 2026 16:00 with contact key "PHONE:CP-SYN-0301-M"
    When the result transaction commits
    Then exactly one outbox row holds rwb.partner.PartnerResultSubmitted.v1 keyed on case "RW-2026-000301"
    Then the payload holds eventCode "PARTNER_RESULT", channel "PORTAL", direction "INBOUND", source "WORKBENCH", occurredAt 18 December 2026 16:00 and toHolderRef "PARTNER:LF-SYN-01"
    Then the result code and the document references are the only other values beside the identifiers
    Then no telephone number, address, person name or contact value is in the payload, the outbox row or a log, and the contact key is not copied

  Scenario: AC3 The fact fits the ledger contract and shows once on the case timeline (new, D-RCV-60)
    Given the two facts of AC1 and AC2 are validated against the consumer element of RWB-P2-E2034-CON
    When the mock consumer applies them to the composed timeline of "RW-2026-000301"
    Then every required attribute of the consumer element is present with the value this service published and none is missing
    Then the timeline holds one HANDOVER entry of 17 December 2026 14:00 and one PARTNER_RESULT entry of 18 December 2026 16:00
    Then each entry names its source and its channel and no second entry exists for the same fact
    Then a fact whose list member has no row in the version in force is refused and no event is built for it
    Then the timeline read, the order and the retention class are the ledger owner's and this service serves no timeline operation

  Scenario: AC4 The change, the record and the fact are one transaction (new, D-RCV-60)
    Given the outbox store refuses the insert of the fact row
    When the instruction of AC1 is issued
    Then no partner_instruction row, no decision record and no outbox row exists
    Then the refusal of the sibling operation is returned and the retry under the same Idempotency-Key writes one fact only
    Then when the store answers, the fact is published once and the consumer holds one entry for it
    Then a fact the consumer keeps refusing past the retry bound goes to rwb.partner.events.v1.dlt with a task for role RW-PLATADM

  Scenario: AC5 Nothing is announced twice (new, D-RCV-60)
    Given the hand-over fact of AC1 is published for "INS-SYN-0301"
    When the same instruction is replayed and the same Idempotency-Key is submitted again
    Then the outbox holds one row and the topic holds one event for "INS-SYN-0301"
    Then the repeat is counted, the first answer returns and no second entry is written by the consumer
    Then a second key on the same instruction writes a second fact only when the instruction itself changed

  Scenario: AC6 The holder comes from the access decision and the scope is enforced (new, D-RCV-60)
    Given identity "RW-REFADM" holds no Partner portal right and case "RW-2026-000301" is held by team "MTG-BKK"
    When "RW-REFADM" reads a partner instruction of that case
    Then the answer is 403 with MSG-P4-002, no row is read and no fact is built
    When a case owner of team "HP-NE" with Own scope reads the same instruction
    Then the answer is 404 with MSG-P4-003 and the fact of the case is unchanged
    Then every holder reference in a fact comes from the cached access decision and never from the request body

  Scenario: AC7 The access read that misses its budget writes nothing and guesses nothing (new, D-RCV-60)
    Given the instruction of AC1 is ready to be issued and the list or the parameter read misses the 2 s budget or its breaker is open
    When the instruction transaction is attempted
    Then nothing is written and one retry with jitter runs
    Then no fact is built on a guessed value and the answer carries MSG-GEN-006

  Scenario: AC8 A read of another schema is refused and fails the build (new, D-RCV-60)
    Given the service identity SY-PARTNER holds a grant on its own schema only
    When a component or a test reads `interaction`, `recovery_case`, the ACE views or another `rwb_*` schema
    Then the grant refuses the statement
    Then the boundary test fails the build

  Scenario: AC14 Every business rule BR1 to BR10 of section 8 holds on the partner fact (new, D-RCV-60)
    Given the two facts of AC1 and AC2 are published and the ledger contract mock of AC3 is in place
    When the rules of section 8 are checked against the facts, the outbox rows, the instruction transaction and the logs
    Then BR1 to BR3 hold for the payload values of AC1 and AC2, and BR4 holds: the contact key of AC2 is not copied
    Then BR5 to BR7 hold for the repeat, the rollback and the transaction boundary of AC4 and AC5
    Then BR8 and BR9 hold: this service writes no interaction row, computes no retention class, and reads every code, channel, direction, source and bound at the version in force
    Then BR10 holds: no person name, contact value, amount or free text is in a payload, an outbox row, a workflow input or a log

  Scenario: AC15 A consumed call that fails or does not answer writes nothing and returns MSG-GEN-006 (new, D-RCV-60)
    Given the rwb-access contract mock fails or does not answer the Partner portal right of "USER:U-2002"
    When the instruction transaction of AC1 is attempted
    Then no partner_instruction row, no decision record and no outbox row exists
    Then the answer carries MSG-GEN-006 and no fact is built

  Scenario: AC12 A list or parameter read that misses its budget or whose breaker is open returns 503 and builds no fact (new, D-RCV-60)
    Given a list or parameter read of the instruction misses the 2 s budget or its breaker is open
    When the instruction transaction is attempted
    Then nothing is written and one retry with jitter runs
    Then the answer carries status 503 and MSG-GEN-006 as section 14 maps, and no fact is built

  Scenario: AC13 A component or a test that reaches another schema is refused by the grant and the build fails (new, D-RCV-60)
    Given the service identity SY-PARTNER holds a grant on its own schema only
    When a component or a test reaches `interaction`, `recovery_case`, the ACE views or another `rwb_*` schema
    Then the grant refuses the statement
    Then the build fails and the pipeline log records the refusal
```

The nine criteria are new under D-RCV-60 and test only the partner fact and its seam with the ledger contract; no legacy criterion text is copied, because AC1 to AC11 of RWB-E2-034 belong to `RWB-P2-E2034-APP`, `RWB-ITG-E2034-ITG` and the ledger owner's stories. Two legacy values are reused because the sources publish them — case `RW-2026-000301`, instruction `INS-SYN-0301`, partner `LF-SYN-01`, holders `USER:U-2002` and `PARTNER:LF-SYN-01`, the dates 17 and 18 December 2026 and the contact key `PHONE:CP-SYN-0301-M` (legacy AC2 and AC3) — and they are asserted on this service's payload, not on the ledger.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The fact maps to one ledger event code: `InstructionIssued` to `HANDOVER`, `PartnerResultSubmitted` to `PARTNER_RESULT`; no other fact of this service enters the ledger from this key | Legacy BR1; LOV-LEDGER-EVENT |
| BR2 | A hand-over to a partner has channel `PORTAL` and direction `OUTBOUND`, with the holder before from the access decision and the partner after; a partner result has channel `PORTAL` and direction `INBOUND` | Legacy BR2; LOV-CHANNEL; LOV-DIRECTION |
| BR3 | A partner fact carries source `WORKBENCH`, because it is entered on a Workbench or portal operation of this service | Legacy BR4; LOV-SOURCE |
| BR4 | The contact point is never copied: the fact carries no contact key, number or address, and the ledger resolves the reference through rwb-source-data | Legacy BR5; REQ-ILG-014; DP-05 |
| BR5 | One fact per idempotency key; a repeat writes no second row, no second event and no second entry, and is counted | Legacy BR7; REQ-ILG-007 |
| BR6 | A failed fact write rolls the change back; a consumer that keeps refusing sends the delivery to the topic's `.dlt` with a task for RW-PLATADM and no entry is lost | Legacy BR8; REQ-ILG-008; DP-09 |
| BR7 | The fact is written in the transaction that writes the instruction row and the local decision record; there is no fact without its record and no change without its fact | DP-03; FSD S9 BR-S9-005 |
| BR8 | The ledger, its retention class and the ordered read are rwb-source-data's by the default ruling; this service writes no interaction row and computes no retention class | DP-18; legacy BR6; R3 default rulings |
| BR9 | The event code, the channel, the direction, the source and the retry bound are rows read at the version in force; no code, channel or bound is a constant in the module | FSD S9 BR-S9-001; principle 1; DP-06, DP-07 |
| BR10 | A payload carries identifiers, codes, dates and document references only: no person name, contact value, amount or free text in the payload, an outbox row, a workflow input or a log | Template and Rules §R7.2 (s17); legacy guardrail 2 |

BR1 to BR3 are the payload values of AC1 and AC2; BR4 is the omission AC2 asserts; BR5 is AC5; BR6 is the rollback and the `.dlt` path of AC4; BR7 is the transaction boundary of step 7; BR8 is why 12.1 has no ledger operation; BR9 is the resolver of step 4, and a build check fails on a code in the source; BR10 is a property test on the payload, the row and the log.

Coverage: BR1, BR2 and BR3 by AC1 and AC2 (TC-E2-034-15); BR4 by AC2 (TC-E2-034-16); BR5 by AC5 (TC-E2-034-17); BR6 by AC4 (TC-E2-034-18); BR7 by AC4 (TC-E2-034-19); BR8 by AC3 (TC-E2-034-20); BR9 by AC3 (TC-E2-034-21); BR10 by AC2 (TC-E2-034-22).

### 9. State transitions

This story changes no case status and no instruction status: the instruction states of LOV-INSTR-STATUS belong to the issue, accept, result and recall steps of this service. The only state machine it moves is the delivery state of the fact.

| From | Event | Condition | To |
|---|---|---|---|
| — | The change commits | The instruction row or the result and the record are written | Outbox row `NEW` |
| `NEW` | The relay publishes | The broker acknowledges | `PUBLISHED` |
| `NEW`, `RETRYING` | The broker refuses | The retry bound is not reached | `RETRYING` |
| `RETRYING` | The retry bound is reached | The consumer keeps refusing | `DLT`, with a task for RW-PLATADM |
| `PUBLISHED` | The same key arrives again | The idempotency key exists | No change; the repeat is counted |

The case side — the stage, the status and the timeline's place in the case sequence — is rwb-case's and the ledger owner's, and this slice neither reads nor writes it.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner (Partner portal R) | Reads the partner instruction and result of the cases in scope; causes no fact |
| RW-AGENCYMG, partner and agency manager (CRUDA) | Issues and reads instructions and results; the fact is written for the issue it makes |
| RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT (CRU) | Create and read instructions inside their capability area; the fact follows their change |
| RW-HEADLIT, RW-HEADNPA, RW-HEADASL (RA) | Read only; approve nothing here |
| PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION, PT-BUYER, PT-RAMC (Partner portal RU) | Return a result on their own firm's instruction; the fact is written inward |
| RW-AUDIT, RW-COE, RW-CONDUCT (R) | Read the instruction, the result and the fact it produced |
| RW-PLATADM, platform administrator | Works the `.dlt` task of a fact the consumer refused; reads the payload only |
| SY-PARTNER, service identity (login `rwb_partner`) | Writes the outbox row in its own schema; holds no grant on another schema and no `v_ace_*` grant |
| Role without Partner portal R or C | Refused with MSG-P4-002 before a row is read |

The rights are the rows of TSD S9 T6.1 and T-A.1 and are not widened. No delegation of authority applies: a fact records a change, it decides nothing about the customer. No personal name appears in this story, a test or a log.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-PRT-008, DF-PRT-009, DF-PRT-010 | partner_instruction (S9, `rwb_partner`) | id, case_id, partner_id | Read, the identifiers of the fact |
| DF-PRT-011, DF-PRT-012, DF-PRT-013 | partner_instruction (S9) | instruction_type, instructed_at, due_at | Read; `instructed_at` is `occurredAt` of a hand-over |
| DF-PRT-014 | partner_instruction (S9) | status | Read, to tell an issued instruction from a closed one |
| DF-PRT-015 | partner_instruction (S9) | result_code | Read, the result of the fact |
| DF-PRT-016 | partner_instruction (S9) | fee_amount | Not read: the fee is FEAT-PRM-07's |
| DF-PRT-002 | partner (S9, `rwb_partner`) | partner_code | Read, into `toHolderRef` as `PARTNER:<code>` |
| Standard columns | partner_instruction, partner (S9) | version, created_at, created_by, updated_at, updated_by | Read only; this story writes no business column |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_partner` | the fact row, the write key | Write through the library, in the transaction (DP-09) |
| DF-DEC-001 to DF-DEC-018 | decision_record (S9, `rwb_partner`) | the record of the change | Not written here: written by the sibling operation in the same transaction (DP-03) |
| DF-INT-001 to DF-INT-029 | interaction (P1, `rwb_source_data`) | event_code, channel, direction, occurred_at, source, from_holder_ref, to_holder_ref, retention_class | Not written and not read: the ledger's (DP-18, BR8) |
| DF-ACE-075 to DF-ACE-123 | v_ace_contact, v_ace_efs_action | contact_key, person_key, action rows | Not read: rwb-source-data's contract, and this service holds no `v_ace_*` grant (DP-05, DP-18) |
| DF-CAS-001, DF-CAS-009, DF-CAS-025, DF-CAS-026 | recovery_case, case_account (P3) | id, owner_user_id, case_id, account_key | Not read: the case reference travels as the event key |

Field IDs are those of the Logical Data Model and Data Dictionary v9 and TSD S9 T3.1. **No business column, table or constraint is added**: the ledger attributes are derived from rows the instruction and result steps already write, and the one migration adds a read-only view and its index in `rwb_partner` (DP-15; ASM-5538). No personal data is written, and the payload carries no contact value.

The names `v_partner_ledger_fact` (a read-only view created by this story's migration, ASM-5538) and `decision_record` (a PLT library table) are not fields or entities of LDM v9 or Data Classification v5; they are this service's own objects.

### 12. Contract

#### 12.1 REST operations provided

None. The service's six operations are baselined and built by their own stories (API-S9-001 to API-S9-006; TSD S9 T-A.1), and this story adds no path, no request property and no answer property to any of them. The base stays `/api/recovery/partner/v1` (DP-13) and the partner gateway and the composite route are unchanged (DP-19); what changes is the payload the two facts carry.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | The reference-data read of the `RWB-P3-E1043-CON` contract (path Not specified in the source documents (GAP-3149; ASM-5533)) | P3 rwb-case | LOV-LEDGER-EVENT, LOV-CHANNEL, LOV-DIRECTION and LOV-SOURCE at the version in force (DP-07) |
| GET | The parameter read of the `RWB-P3-E1042-CON` contract (path Not specified in the source documents (GAP-3149; ASM-5535)) | P3 rwb-case | The retry bound after which a fact goes to the `.dlt` (DP-06) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The right, the scope and the holder reference of the caller, cached per session by the guard library; the sibling operation makes the call and this story reads its answer (DP-08) |

Each row is one hop with a 2 s client budget and a breaker (ADR-020; DP-11). The three are class C in fact and none is in the Work Package's C row, which holds `RWB-P2-E2034-CON`; they arrive with the platform libraries of the service template (GAP-3149; ASM-5532).

#### 12.3 Events published

| Event | Schema | Topic | Key | Payload carries | Purpose |
|---|---|---|---|---|---|
| `rwb.partner.InstructionIssued.v1` (EV-20) | `rwb_partner_instruction_issued` | `rwb.partner.events.v1`, with its retry and `.dlt` topics | `caseId` | instruction, case and partner references, partner code, instruction type, `dueAt`; `eventCode` `HANDOVER`, `channel` `PORTAL`, `direction` `OUTBOUND`, `source` `WORKBENCH`, `occurredAt`, `fromHolderRef`, `toHolderRef` | Announces the hand-over of the case to the firm for the ledger entry and the case |
| `rwb.partner.PartnerResultSubmitted.v1` (EV-21) | `rwb_partner_partner_result_submitted` | `rwb.partner.events.v1`, with its retry and `.dlt` topics | `caseId` | instruction, case and partner references, partner code, result code, document references; `eventCode` `PARTNER_RESULT`, `channel` `PORTAL`, `direction` `INBOUND`, `source` `WORKBENCH`, `occurredAt`, `toHolderRef` | Announces the partner's result for the ledger entry and the case |

| Envelope element | Value |
|---|---|
| Mode | CloudEvents 1.0, binary |
| ce_type | `rwb.partner.InstructionIssued.v1` or `rwb.partner.PartnerResultSubmitted.v1` |
| ce_source | rwb-partner |
| ce_subject and key | The case ID of the instruction |
| ce_id and traceparent | The event identifier and the W3C trace context of the call |
| Payload | Identifiers, codes, dates and document references; no personal data, no contact value, no amount, no free text |

The two events are the service's own pair (context pack events EV-20 and EV-21; TSD S9 T5.3) and their emitters are the instruction stories and the result story; this story fixes the ledger attributes they carry and adds no third event, no second topic and no second outbox. The seven attributes are additive and are named by no source document, so the names are this story's design choice and are fixed with the contract owner (GAP-3149; ASM-5531). The outbox row is written in the change's transaction and relayed after the commit.

#### 12.4 Events consumed

None. The fact is built from the service's own rows; the ledger's read and the composed timeline are consumed by the screen through the composite route and by `RWB-P2-E2034-CON`, not by this story. No inbox row, no consumer group and no subscription is added.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `InstructionWorkflow` | Workflow, one execution per instruction; workflow ID form and start rule: Not specified in the source documents (CG-ALL-11771); the one workflow the S9 ownership row carries | `rwb-partner`, namespace `rwb-recovery` | The change's stage; this story adds no signal and no stage |
| `writeLedgerFact` (name is this story's design choice) | Activity | `rwb-partner` | Builds the fact and writes the outbox row inside the change's transaction (BR7) |
| The outbox relay | Library component, not an activity of this service | — | Publishes the row after the commit; a refusal retries, then the `.dlt` (BR6) |

The activity name and the payload element names are fixed by no source (GAP-3149; ASM-5531); a replay reuses the recorded outcome and writes no second fact.

#### 12.6 Schedules

None. The legacy EFS read step was a step of JOB-02 inside the monolith; in the target the EFS product is read by rwb-source-data and its step is that service's, so this service owns no job (ownership rows: Jobs 0) and adds no Temporal Schedule. The instruction clock is a durable timer of `InstructionWorkflow`, not a Schedule.

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `partner_instruction` | `rwb_partner` | S9 | Read only, through the view; the row is written by the instruction and result steps |
| `partner` | `rwb_partner` | S9 | Read only, the firm and its code |
| `v_partner_ledger_fact` | `rwb_partner` | S9 | A read-only view, not an LDM v9 entity (ASM-5538), created by this story's migration: the fact rows of the two events with their holders and dates |
| `outbox_event` | `rwb_partner` | PLT library applied here | Written in the change's transaction (DP-09) |
| `processed_event` | `rwb_partner` | PLT library applied here | Present for the service's consumers; this story writes none of its rows |
| `idempotency_key` | `rwb_partner` | PLT library applied here | The write key of the sibling operation, read here to refuse a repeated fact |
| `decision_record` | `rwb_partner` | PLT library applied here | Written by the sibling operation in the same transaction; not written here (DP-03); a PLT library table, not an LDM v9 entity |

Not owned and never read as a table: `interaction` (P1), `recovery_case`, `task` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), the document tables (P5), the notice tables (P6) and the `v_ace_*` views (P1 only). `case_id` is a reference and not a key across schemas, and no foreign key leaves `rwb_partner` (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| `RWB-P2-E2034-CON` consumer fake | The consumer element of the partner fact with its required attributes, an accepted entry, and the composed timeline holding one entry per fact | AC1, AC2, AC3, AC5 |
| `RWB-P2-E2034-CON` refusal fixture | A consumer that refuses every delivery, and the `.dlt` answer with the task for RW-PLATADM | AC4 |
| rwb-case reference-data fake | The four lists at the version in force, a member without a row, and an answer beyond 2 s | AC1, AC2, AC3, X4, X6 |
| rwb-case parameter fake | The retry bound 3 and a second version of it | AC4, X3 |
| rwb-access decision fake | A granted Partner portal right C with holder `USER:U-2002` and team scope `MTG-BKK`; a refusal for `RW-REFADM`; a case outside the scope | AC6, X5 |

The fakes are test-only and are replaced by the real services in SIT. No fake carries personal data: every instruction, case and partner in the fixtures is synthetic, and the contact key is a synthetic reference.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 3 consumed | No new operation; the reference-data read, the parameter read and the access decision, each one hop with 2 s and a breaker |
| Kafka | 2 published, 0 consumed | `rwb.partner.InstructionIssued.v1` and `rwb.partner.PartnerResultSubmitted.v1` on `rwb.partner.events.v1`, keyed on the case ID, with the ledger attributes this story adds and the emitters it extends |
| Temporal | 1 workflow, 1 activity of this story | `InstructionWorkflow` on `rwb-partner` with `writeLedgerFact`; no Schedule |
| File | None | No file is read, built or delivered here; the EFS product is rwb-source-data's and the letters are rwb-comms's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.partner`, module `ledgerfact`. No front-end file: the entry is shown by the timeline the ledger owner serves.

| Component | Type | Responsibility |
|---|---|---|
| `LedgerFactReader` | Repository | Reads `v_partner_ledger_fact` in `rwb_partner`, and nothing else |
| `LedgerAttributeResolver` | Service | Reads the four lists at the version in force and resolves the event code, the channel, the direction and the source (BR1, BR2, BR3, BR9) |
| `LedgerFactAssembler` | Service | Builds the payload: the attributes, `occurredAt`, `fromHolderRef` from the decision, `toHolderRef` as `PARTNER:<code>`, the identifiers; no contact value (BR4, BR10) |
| `LedgerFactOutbox` | Library adapter | Writes the outbox row of the fact in the change's transaction; one row per key (BR5, BR7) |
| `HolderRefResolver` | Service | Takes the holder reference from the cached access decision and refuses a body-supplied holder (BR2, AC6) |
| `ReferenceDataClient`, `ParameterClient`, `DecisionClient` | Client | The three consumed contracts, one hop, 2 s, breaker, cached per request |
| `writeLedgerFact` | Activity | The step of `InstructionWorkflow` that runs the four components inside the transaction |

**Database.** One step in the per-service Flyway sequence of `rwb_partner` (DP-15): `V2034_1__partner_ledger_fact.sql`, which creates the read-only view `v_partner_ledger_fact` over `partner_instruction` joined to `partner` — the instruction, the case, the partner and its code, the type, `instructed_at`, `due_at`, the status and `result_code`, with the standard columns — and one index on `(case_id, instructed_at)`. No business table, column or constraint is added, and no migration of this service touches another schema. The view and index names are a design choice fixed by no source (ASM-5538).

**Configuration and reference data.** The four lists are read at the version in force (DP-07); the retry bound is a parameter row, 3 in the legacy retry, with no published parameter name (DP-06; ASM-5535); the 2 s budget, the single hop and the breaker are ADR-020. The flag `rwb.partner.ledger-fact` is a flag of the platform library: off means the change commits without an outbox row and no fact is published, while no ledger entry is created downstream, and the timeline shows the case entries only (BR8).

**Build steps**

1. The view and its index in the service's Flyway sequence, applied on an empty and on a loaded `rwb_partner` (AC1, DP-15).
2. `LedgerFactReader` and its two projections, for an issued instruction and for a result (AC1, AC2).
3. `LedgerAttributeResolver` over the reference-data fake, with the two event codes, the two directions and a member the version does not carry (AC1, AC2, AC3, X6).
4. `LedgerFactAssembler` with the property test that a synthetic contact value, address and name never reach the payload, the row or a log (AC2, BR10).
5. `HolderRefResolver` and the refusal of a holder supplied by the body; the right and the scope cases (AC6, X5).
6. `LedgerFactOutbox` inside the transaction of the sibling operation, with the rollback case and the repeat case (AC4, AC5, X1, X2).
7. The `.dlt` path and its task for RW-PLATADM past the retry bound (AC4, X3).
8. The contract test against the `RWB-P2-E2034-CON` consumer element and the composed timeline (AC3, BR1).

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

This is a secondary slice: the metadata H row stays `None` and the C row stays `RWB-P2-E2034-CON` exactly as the Work Package fixes them, so the ten platform contracts the DP table names arrive with the service template and are not written into either row (GAP-3149; ASM-5532). **DP-09** is the core of the story: the fact row and the CloudEvents envelope in the change's transaction. **DP-18** is why no ledger table appears in 12.7: the entry, its retention class and its order are rwb-source-data's by the default ruling. **DP-05** is met by omission: no view and no ACE grant in this service, because the contact reference is resolved by the ledger owner. **DP-03** puts the record and the fact in one transaction, **DP-07** and **DP-06** are the lists and the retry bound, and **DP-08** is the holder reference. **DP-10** replaces the legacy JOB-02 step with the event-started instruction workflow and adds no Schedule. **DP-11** is the contract-with-mock rule the consumer test uses, **DP-13** and **DP-19** leave the base and the route unchanged, and **DP-15** is the view. The wave is the Work Package's 2, the W-MAP wave of EP02, earlier than the service's wave 4 and kept per §R5.6.

**Done when.** The tests of section 16 pass, `INS-SYN-0301` produces one `HANDOVER` fact with `USER:U-2002` and `PARTNER:LF-SYN-01`, a result produces one `INBOUND` `PARTNER_RESULT` fact with no contact value, a refused outbox insert leaves no instruction column, no record and no fact, a repeat writes one row, the consumer element of `RWB-P2-E2034-CON` is satisfied for both facts, and no statement outside `rwb_partner` exists in the build.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | The caller holds no Partner portal right R or C (X5) | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case of the instruction is outside the caller's scope (AC6) | This case is not in your scope. |
| MSG-GEN-006 | The list or the parameter read misses the 2 s budget (X4) | {system} is not available. Your request is queued and will be retried. |
| MSG-P7-003 | The local decision record cannot be written, so no change and no fact exist (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| Not specified in the source documents (GAP-3149; ASM-5533) | A list member has no row in the version in force (X6) | No source names a message for a fact refused on a code that is not in force |

The four identifiers and their texts are the legacy and FSD message set, copied unchanged; MSG-P7-003 is the answer the sibling operation returns when the record refuses, and this story only guarantees that nothing is committed. Status mapping: 403 MSG-P4-002, 404 MSG-P4-003, 503 MSG-GEN-006. Thai text follows DL10. No message is added by this story.

### 15. Screens and states

No screen is built here. The partner entry appears on SCR-04 Case timeline, whose states — Loading, Filtered and Empty with MSG-P3-024, Error (Not specified in the source documents, CG-ALL-11776) and No access (Not specified in the source documents, CG-ALL-11776) — belong to the timeline owner and the screen owner, and which reads through the gateway-bff composite route (DP-19). The merged list is sequenced by occurred time with the case sequence as tie-break, as rwb-source-data's ordered read (BR8); the page order of the screen is the case timeline contract's and is not set here (ASM-B2-P3-010-2). The partner half of an entry is this story's payload: the channel "Portal", the direction, the firm reference, the holder before and after, the time and the source. SCR-34 Partner list and SCR-35 Placement and allocation are the instruction and result stories' and are untouched: this story adds no column and no action to them. Their states are those of the instruction and result stories; Empty, Error and No access are Not specified in the source documents (CG-ALL-11777 for SCR-34, CG-ALL-11778 for SCR-35).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-034-12 | AC6 for the refusal: an identity without Partner portal right C is refused with 403 and MSG-P4-002 before a row is read, and no fact is built | Component | RW-REFADM refused; RW-AGENCYMG granted on the same instruction |
| TC-E2-034-01 | No criterion here: the EFS `CONTACT` entry, its contact key and its retention class are rwb-source-data's by the default ruling | Component | One EFS action row with a promise; the ledger fixture |
| TC-E2-034-02 | AC2 for the hand-over half: an instruction to `LF-SYN-01` produces one `HANDOVER` fact with `USER:U-2002` and `PARTNER:LF-SYN-01` at 17 December 2026 14:00 | Component | Instruction `INS-SYN-0301`, case `RW-2026-000301`, holder `USER:U-2002` |
| TC-E2-034-03 | AC2 and AC3 for the partner entry: the result of `LF-SYN-01` on 18 December 2026 16:00 appears once on the composed timeline with its source and channel; the ordering and the read are the ledger's | Component | Three source entries in the mock; the partner result of AC2 |
| TC-E2-034-04 | No criterion here: the letter, delivery, offer and payment entries are rwb-comms's and rwb-payment's, and their facts are not this service's | Component | NoticeDispatched, NoticeDelivered, TreatmentApproved, ProceedsMatched fixtures |
| TC-E2-034-05 | AC5 for the repeat: a replayed instruction and a repeated key produce one outbox row, one event and one entry, and the repeat is counted | Component | The same instruction twice under one key, then a second key |
| TC-E2-034-13 | AC7 for X4: a list or parameter read that misses the 2 s budget writes nothing, retries once with jitter and builds no fact | Component | The rwb-case list stub times out or its breaker is open |
| TC-E2-034-14 | AC8 for X7: a read of `interaction`, `recovery_case`, a `v_ace_*` view or another `rwb_*` schema is refused and fails the build | Component | A statement from a component and from a test against each forbidden schema |
| TC-E2-034-15 | BR1 to BR3 for the payload values of AC1 and AC2: event code, channel, direction and source | Component | The hand-over and the partner result each committed |
| TC-E2-034-16 | BR4 for AC2: no contact key, number or address in the fact | Component | The partner result carrying a contact key |
| TC-E2-034-17 | BR5 for AC5: one fact per idempotency key | Component | The same key submitted twice |
| TC-E2-034-18 | BR6 for AC4: a failed write rolls back and a refused delivery goes to the .dlt | Component | The outbox store refusing the insert and a consumer refusing past the bound |
| TC-E2-034-19 | BR7 for AC4: the fact commits with the instruction row and the decision record | Component | The instruction transaction committed and rolled back |
| TC-E2-034-20 | BR8 for AC3: this service writes no interaction row and computes no retention class | Component | The instruction transaction with the ledger tables observed |
| TC-E2-034-21 | BR9 for AC3: codes, channels, directions, sources and the retry bound are read at the version in force | Component | A list stub with a changed version and a build scan for constants |
| TC-E2-034-22 | BR10 for AC2: the payload, the outbox row and the log carry no personal value | Component | Property test over the payload, the row and the log |
| TC-E2-034-06 | No criterion here: an EFS row outside the outcome list or outside a case is rwb-source-data's and rwb-integration's filter | Component | Three EFS rows: listed, unlisted, no open case |
| TC-E2-034-07 | AC7 for the rollback: a refused outbox insert leaves no instruction change, no record and no fact, and the retry writes one | Component | Outbox store refusing one insert, then answering |
| TC-E2-034-08 | AC8 for the `.dlt`: a consumer that keeps refusing past the retry bound sends the delivery to `rwb.partner.events.v1.dlt` with a task for RW-PLATADM and writes no entry | Component | Retry bound 3 from the parameter fake; a refusing consumer |
| TC-E2-034-09 | No criterion here: the order by occurred time, including a late EFS row, is the ledger read's | Component | Workbench entry 15 December 2026 09:30; EFS row 14 December 2026 10:15 |
| TC-E2-034-10 | No criterion here: the empty timeline and MSG-P3-024 belong to the screen and the ledger read | Component | Case `RW-2026-000302` with no entry |
| TC-E2-034-11 | AC11 for the scope: a case of team `MTG-BKK` read by an owner of team `HP-NE` with Own scope answers 404 with MSG-P4-003 and the fact is unchanged | Component | Case `RW-2026-000301` in `MTG-BKK`; reader in `HP-NE` |
| TC-E2-034-13 | Contract of the operations, events and activities of section 12.5: `InstructionWorkflow`, `writeLedgerFact`, and the facts `InstructionIssued` (EV-20) and `PartnerResultSubmitted` (EV-21) with their ledger attributes | Contract | The baselined event pair; the workflow and activity definitions of section 12.5 |
| TC-E2-034-14 | Boundary of the tables of section 12.7 (ASM-3438): the service reads and writes only the tables listed as owned or read here, and a read of a table not listed is refused | Component | Read attempt on `recovery_case` from `rwb_partner`; a foreign key candidate across schemas |
| TC-E2-034-23 | AC15: a consumed call that fails or does not answer writes no row, no record and no fact, and the answer carries MSG-GEN-006 | Component | Not specified in the source documents (NEWAC-RWB-S9-E2034-APP-AC15) |
| TC-E2-034-24 | AC14 for BR1 to BR10: every business rule of section 8 holds on the partner fact, checked in the order of the AC14 steps | Component | Not specified in the source documents (NEWAC-RWB-S9-E2034-APP-AC14) |
| TC-E2-034-25 | AC12 for X4: a list or parameter read that misses the 2 s budget or whose breaker is open writes nothing, retries once with jitter, builds no fact and returns 503 with MSG-GEN-006 | Component | The rwb-case list stub times out or its breaker is open |
| TC-E2-034-26 | AC13 for X7: a component or a test that reaches `interaction`, `recovery_case`, a `v_ace_*` view or another `rwb_*` schema is refused by the grant and fails the build | Component | A statement from a component and from a test against each forbidden schema |

The twelve legacy cases keep their identifiers and their legacy order, with the Level column added; the legacy table publishes no level, so each is assigned here — legacy "System" maps to Component for a single-service half and "Access" maps to Component (GAP-3149; ASM-5537). Six cases carry a criterion of this slice and six are listed with "no criterion here", because the behaviour they test is another owner's after the split. No `-ITG` copy is written here: the same values across rwb-partner, rwb-integration and rwb-source-data are `RWB-ITG-E2034-ITG`'s. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases, tab Story test cases, under the same ID.

### 17. Guardrails

- No business value in code: the event codes, the channel, the directions, the source and the retry bound are rows read at the version in force, and a build check fails on any of them in source or configuration (BR9).
- No personal data in the payload, an outbox row, a workflow input, a log or a span: identifiers, codes, dates and document references only; the contact key is not copied (BR4, BR10).
- No read of another service's tables and no cross-schema join: `interaction` (P1), `recovery_case` (P3), the decision ledger (P7), the document tables (P5) and the notice tables (P6) are reached only through their owners (DP-01).
- ACE data only through the owner's contract or a `v_ace_*` view: this service holds no `v_ace_*` grant and reads no ACE table; the contact reference is rwb-source-data's (DP-05, DP-18).
- The record, the change and the fact are one transaction; a refusal of any of them writes nothing (BR7, AC4).
- One fact per key and one entry per fact: the write key, the `Idempotency-Key` and the consumer's key carry the rule (BR5, AC5).
- An applied migration is never edited: the view and the index are a new version in the service's own sequence (DP-15).
- No retired element is reintroduced: no Quartz job, no JOB-02 step, no shared ledger table in this schema, no monolith base and no login of the retired service.

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases | Feature | L3 process |
|---|---|---|---|---|---|
| REQ-ILG-011 | A hand-over names who held the case, who holds it now and when (Business Requirements Epic 2, section 3.2; FEAT-ILG-08) | `fromHolderRef` and `toHolderRef` of the `HANDOVER` fact, with `occurredAt` | TC-E2-034-02 | FEAT-ILG-08 | Not specified in the source documents (DOR-RWB-S9-E2034-APP-2) |
| REQ-ILG-014 | The contact point is a reference and never a copied value (Epic 2, section 3.2) | No contact column, no contact value in the payload; the ledger resolves it through rwb-source-data | TC-E2-034-01 (no criterion here), TC-E2-034-03 | Not specified in the source documents (DOR-RWB-S9-E2034-APP-2) | Not specified in the source documents (DOR-RWB-S9-E2034-APP-2) |
| REQ-ILG-007 | One entry per idempotency key; a repeat is ignored and counted (Epic 2, section 3.2) | The write key and the outbox row of the fact | TC-E2-034-05 | Not specified in the source documents (DOR-RWB-S9-E2034-APP-2) | Not specified in the source documents (DOR-RWB-S9-E2034-APP-2) |
| REQ-ILG-008 | A failed write loses no entry and raises an incident (Epic 2, section 3.2) | The rollback of AC4 and the `.dlt` task for RW-PLATADM | TC-E2-034-07, TC-E2-034-08 | Not specified in the source documents (DOR-RWB-S9-E2034-APP-2) | Not specified in the source documents (DOR-RWB-S9-E2034-APP-2) |
| REQ-ILG-012 | The case record view shows the ledger as an ordered timeline (Epic 2, section 3.2; FEAT-ILG-09) | The partner entry's values on the composed timeline; the read and the order are the ledger owner's | TC-E2-034-03, TC-E2-034-10 (no criterion here) | FEAT-ILG-09 | Not specified in the source documents (DOR-RWB-S9-E2034-APP-2) |
| REQ-ILG-009 | Contact outcomes from collections reach the ledger (Epic 2, section 3.2; FEAT-ILG-06) | Not answered here: the EFS and Workbench contact entries are rwb-source-data's | TC-E2-034-01, TC-E2-034-06 (no criterion here) | FEAT-ILG-06 | Not specified in the source documents (DOR-RWB-S9-E2034-APP-2) |
| REQ-ILG-010 | Dispatched letters write their result, including proof of delivery (Epic 2, section 3.2; FEAT-ILG-07) | Not answered here: the letter entries are rwb-comms's | TC-E2-034-04 (no criterion here) | FEAT-ILG-07 | Not specified in the source documents (DOR-RWB-S9-E2034-APP-2) |
| REQ-ILG-013 | Ledger entries carry their own retention class (Epic 2, section 3.2; FEAT-ILG-10) | Not answered here: the class is the ledger owner's row, set independently of the decision record | TC-E2-034-01 (no criterion here) | FEAT-ILG-10 | Not specified in the source documents (DOR-RWB-S9-E2034-APP-2) |
| REQ-ILG-006 | The timeline orders entries by occurred time and case sequence (Epic 2, section 3.2) | `occurredAt` is supplied on every fact so the order is computable downstream; the order itself is the read's | TC-E2-034-09 (no criterion here), TC-E2-034-03 | Not specified in the source documents (DOR-RWB-S9-E2034-APP-2) | Not specified in the source documents (DOR-RWB-S9-E2034-APP-2) |

| Story or item | Relation to this story |
|---|---|
| RWB-P2-E2034-CON | C: the consumer element, the composed timeline and the fakes; the mapping and the read are its stories' |
| RWB-S9-E6031-APP, RWB-S9-E6034-APP | Emit EV-20 with the ledger attributes this story fixes |
| RWB-S9-E6033-APP | Emits EV-21 with the ledger attributes this story fixes |
| RWB-ITG-E2034-ITG | Proves the same values across rwb-partner, rwb-integration and rwb-source-data |
| rwb-source-data (P1) | Owns the interaction ledger, the retention class and the ordered read (DP-18) |
| RWB-S9-E2033-CON (AD022) | The service's event pair and the topic are baselined there; no event is added here |
| Legacy RWB-E2-034 sections 2, 3, 4, 7, 8, 11, 12, 14 and 16 | Sections 1 to 8, 11, 12, 14 and 16 of this story; AC1 to AC11 stay with the legacy owners |
| Legacy BR1, BR2, BR4, BR5, BR7, BR8 | BR1 to BR6 of this story |
| TC-E2-034-01 to TC-E2-034-12 | Section 16, with the Level column added |

### 19. Out of scope

- The interaction table, the retention class, the ordered timeline read and the EFS contact read step: rwb-source-data (P1), by the default ruling (DP-18).
- The fact-to-entry mapping, the `"ledger-channels"` consumer, the read operation of the ledger and the composed timeline: rwb-integration and rwb-source-data in `RWB-P2-E2034-CON`'s stories.
- Legacy AC1 to AC11 and the end-to-end proof of the three sources on one timeline: `RWB-P2-E2034-APP` and `RWB-ITG-E2034-ITG`.
- The letter, delivery, offer and payment entries: rwb-comms (P6) and rwb-payment (P8), and their events.
- The issue, acceptance, decline, result and invoice operations API-S9-001 to API-S9-006 and their screens: the instruction and result stories of this service.
- The case status, the stage, the case sequence and the timeline screen SCR-04: rwb-case (P3) and the edge.
- The decision record itself, its chain and its seal: the sibling operations and rwb-decision (P7).
- The partner gateway route, the composite route and the masking rules by role: the platform edge story and rwb-access.
- The physical schema files, the grants and the deployment of this build.
