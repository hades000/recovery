# RWB-P7-E1028-APP Service levels, timers, escalation and prescription dates

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E1028-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-028 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P7-I |
| Ready to start | Day 1 |
| Size | Not set; the squad sizes it at refinement (DOR-RWB-P7-E1028-APP-16) |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-P7-E1028-APP-14) |
| Contract fake library | Not specified in the source documents (DOR-RWB-P7-E1028-APP-22) |
| Contract version | v1 (major version 1, as stated in RWB-P3-E1028-CON) |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E1028-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to REQ-CWC-011, REQ-CWC-012, REQ-CWC-016) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-028 for rwb-decision, so that the warning, the breach and the prescription date of a case are held in the central decision ledger as records an auditor reproduces from the ledger alone, append only, with the hash chain checked at 02:00 and a break reported the same day. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P7-E1028-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 15 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **auditor (RW-AUDIT), a compliance officer (RW-COMPLY) and a team manager (RW-TEAMMGR)**, I want **the warning, the breach and the prescription date of a case held in the central decision ledger as records that name the rule, its version, the inputs with their freshness and the escalation role and level, in a store that is append only and hash chained, with the chain checked every night at 02:00**, so that **the deadline that passed unseen, and the date a legal claim would expire, can be reproduced from one place without a second source, and no record of a deadline is ever altered unseen**.

Inside `rwb-decision` this is the deadline slice of the central ledger:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1`, Temporal task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`. The service consumes `DecisionRecorded` (EV-08) on the shared topic `rwb.decision-record.v1`, idempotently, into `decision_log_entry` in `rwb_decision`: the collecting side of the local record plus central ledger design (DP-03; Architecture v5 slide 28).
- The three records of this story are the deadlines of legacy RWB-E1-028: the **warning record** at the warning point of a service level, the **breach record** with rule ID `R-UNI-30` and escalation level 1 to `RW-TEAMMGR` of the queue's team, and the **prescription-date record** with the `LEGAL_PERIOD` version in force and the business date of each account date it used.
- Reproducibility is the deliverable (NFR-033, NFR-034): every entry carries the rule ID, the rule version, an inputs reference with the freshness of each input, `decided_at` and the escalation role. Nothing about a case is copied beside the reference: the entry holds `case_id` and no queue, no team, no owner, no product group and no prescription date, and the queue's team and the case number are read on the rwb-case contract at display time.
- The read is this service's: `GET /decision-log?caseId=...` returns the warning, the breach and the prescription decision of a case in `decided_at` order, each with `chainVerified`, and `GET /decision-log/{entryId}` returns one entry with its inputs and versions (API-P7-006 and API-P7-007 of TSD P7 T-A, re-based by DP-13).
- Append only and chained: an entry is never updated or deleted, a correction is a new entry that names the entry it corrects (`corrects_entry_id`), a re-hashed or edited entry is refused, and JOB-14 Hash-chain check runs as a Temporal Schedule at 02:00 in queue `rwb-decision` and reports a break the same day (NFR-035) with MSG-P7-012.
- No Drools package is evaluated in this story, because DP-04 is not in its pattern set: the timer rules, the service level rows, the working-day calendar and the prescription calculation stay with rwb-case, and the legal period rows and the parameter `legal.prescription.warn.days` = 180 stay with their owners (section 19).

### 2. Business rationale

Deadlines are tracked in personal diaries today, and audit found litigation not filed for debtors who met the criteria (CTL-18). Legacy RWB-E1-028 started the clock, warned the owner and wrote a decision log entry for the warning and for the breach (legacy BR9). A clock whose record can be rewritten, or whose record is a row beside the timer it describes, proves nothing to an auditor two years later: the timer row moves, the service level row is superseded, and the calendar is reloaded for the next year.

The central ledger is where a deadline has to survive all three. Each entry is written once, linked to the entry before it, and carries the rule, the version in force, the inputs with the freshness of each, the moment of the decision and the role the breach went to. A reader who has the entry has the deadline: the service level that applied, the value it held that day, the calendar in force, and the business dates of the accounts the prescription date came from. That is NFR-033 and NFR-034 in one row, and it is what makes a two-year prescription date defensible in court. The chain is what makes the row trustworthy: NFR-035 asks for a daily check and a same-day report to Compliance, and the daily anchor of the ledger hash in write-once storage (Architecture v5 slide 28) makes the day's set unarguable. This story is the rwb-decision part of legacy RWB-E1-028 and delivers the collecting side: the three deadline records, the append-only guarantee on them, the read an auditor uses and the 02:00 check. The timer, the service level rows, the warning and the breach raising, the calendar and the prescription calculation stay with rwb-case (RWB-P3-E1028-APP and RWB-P3-E1028-CON); the access answer stays with rwb-access (RWB-P4-E1028-APP); the store, the writer and the rule registry stay with RWB-P7-E1008-APP, RWB-P7-E1027-APP and RWB-P7-E1073-APP. It meets REQ-CWC-011, REQ-CWC-012 and REQ-CWC-016 on the ledger side and supports the measure "decisions within the delegation of authority" at 100 percent, because the escalation role and the level it went to are on the record and not in a note.

### 3. Preconditions

- RWB-P3-E1028-CON is published: the rwb-case contract with `GET /cases/{caseId}` on base `/api/recovery/case/v1`, whose answer carries the case number, the queue and the queue's team, with the error envelope, the not-found answer and its fake (DP-11). This story reads those three values and nothing else.
- The `rwb_decision` baseline is in place from the service-template work (RWB-PLT-TPL): the schema, the base `/api/recovery/decision/v1`, the topic `rwb.decision.events.v1`, the task queue `rwb-decision`, the topic subscription and the deployment chart, with the platform contracts the DP rows name already delivered in wave 1: the inbox library (DP-09), the workflow kit and its Schedules (DP-10), the naming library (DP-14), the per-service Flyway sequence (DP-15) and the gateway-bff composite route (DP-19).
- RWB-P7-E1008-APP delivers the store: the `decision_log_entry` columns of TSD P7 T3.1, the append-only trigger `tr_declog_append_only`, the hash rules and the indexes `ix_declog_case_time`, `ix_declog_rule` and `ix_declog_actor_time`. This story adds no build dependency of its own (metadata "Depends on (build)" = None) and its refusal and chain tests run against that store fixture.
- RWB-P7-E1027-APP delivers the writer and the local decision-record library, and every one of the 19 services publishes `DecisionRecorded` on `rwb.decision-record.v1` with the seven field groups of FSD P7 AC-ALT-P7-001-02 and the chain fields of TSD P7 T3.1. The same-transaction rule holds on that side: an action whose record cannot be written does not proceed (FSD P7 A2.5, R-UNI-39), so a record that arrives here is a record of an action that happened, and a record that does not arrive is an action that did not happen.
- The three synthetic facts the tests use, copied from the legacy story: case `RW-2026-000401` in queue `LIT-BKK-OFF`, team `LIT-BKK`, owner `U-31`, on a service level of 5 working days with warning percent 80 and escalation role `RW-TEAMMGR`, started 2026-12-01 09:00 with `warn_at` 2026-12-08 09:00 and `expires_at` 2026-12-09 09:00 (legacy AC1 and AC2); case `RW-2026-000402` for `HIRE_PURCHASE`, one account whose last payment date is 2026-03-15, a legal period of 2 years from the last payment date and a prescription date of 2028-03-15 (legacy AC3); and 2026-12-05 to 2026-12-07 as non-working days.
- Readers hold the Decision log right R in scope (TSD P7 T6.1): RW-AUDIT, RW-COMPLY, RW-TEAMMGR, RW-CASEOWN and RW-LITOFF hold it, and RW-PHONECOL holds no Decision log row there, which is the refusal of TC-E1-028-12.

### 4. Flow

1. A service takes a decision about a deadline: the case side moves a timer to its warning point, or to its breach, or sets a prescription date on case creation. It writes the decision record and its own state change in one transaction and publishes `DecisionRecorded` through its outbox to `rwb.decision-record.v1`, keyed on the case ID (Architecture v5 slides 28 and 42; DP-03, DP-09).
2. `rwb-decision`: `DecisionRecordConsumer` reads the event. The inbox (`processed_event`) is checked on the event ID and on `idempotency_key`; an event already processed is answered with the first entry's ID, adds 1 to the repeat count for R-UNI-40, and writes no row.
3. `rwb-decision`: `DeadlineLedgerWriter` checks the shape of the record against the rule of the writer story: the decision code in LOV-DECISION, `inputs_ref` present, `rule_id` with its `rule_version`, `decided_at` present, and a value for every field the chain hashes. A record that fails is refused with MSG-P7-009, the message is logged with the case ID and the missing field, and nothing is written.
4. `rwb-decision`: `ChainHasher` computes `entry_hash` as the SHA-256 of the canonical form and takes `prev_hash` from the entry with the highest `chain_seq`, the first entry carrying 64 zeros; `chain_seq` is allocated once and never reused, and an append that fails leaves the sequence unused. The writer then inserts one row with `case_id`, the decision code, `rule_id`, `rule_version`, `inputs_ref`, `decided_at`, `prev_hash`, `entry_hash`, `chain_seq`, `final_call`, `actions` and `outcome`. The three deadline records are stored as they arrive: the warning carries the warning point and the computed `warn_at` in its inputs reference, the breach carries `R-UNI-30` with escalation role `RW-TEAMMGR` and escalation level 1, and the prescription record carries the `LEGAL_PERIOD` version in force and the business date of each account date it used, 2026-03-15 in the test. No case fact is written.
5. The reader: `GET /api/recovery/decision/v1/decision-log?caseId=...` reads the entries of the case in `decided_at` order, computes `chainVerified` per entry, and calls RWB-P3-E1028-CON once for the case number, the queue and the team, one hop inside the 2 s budget. A case the contract does not return is answered 404 and no entry is listed. `GET /api/recovery/decision/v1/decision-log/{entryId}` returns one entry with its inputs reference, its rule ID and version, its chain fields and `chainVerified`: the read an auditor uses to reproduce one deadline.
6. The chain: JOB-14 Hash-chain check runs as a Temporal Schedule at 02:00 in queue `rwb-decision`. It reads the entries from `chain_seq` 1 in pages, recomputes every `entry_hash`, compares every `prev_hash` with the `entry_hash` before it, and reports the first break with the entry, its `chain_seq` and the expected `prev_hash`, raising MSG-P7-012 to the Compliance queue the same day (NFR-035). The check writes no entry, repairs nothing and deletes nothing.
7. A correction: an entry that is wrong is never changed. A new entry is appended with `corrects_entry_id` naming the entry it corrects, and the read returns both in `decided_at` order.

The append is the moment of truth: the row, its `chain_seq`, its `prev_hash` and its `entry_hash` are written in one statement, and a failed append leaves no row and no consumed sequence, so the chain has no hole to hide in.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The same `DecisionRecorded` arrives twice, or a replay re-delivers it | One entry; the first entry's ID is returned and the repeat count is raised by 1 | None | AC6, TC-E1-028-08 |
| X2 | The record fails the shape check: no `inputs_ref`, a `rule_id` with no `rule_version`, or a decision code outside LOV-DECISION | Refused before the append; the error is logged with the case ID and the missing field; no row and no `chain_seq` | MSG-P7-009 | AC1 |
| X3 | The append fails, or the store is unavailable | Nothing is written, `chain_seq` is not used, the offset is not committed and the event is redelivered; the ledger never holds half a record | MSG-P7-003 and MSG-P7-012 on the read while the entry is missing | AC7, TC-E1-028-09, TC-E1-028-13 |
| X4 | A record has not arrived within five minutes of its `decided_at` | The case is listed with one missing record and its `decided_at`; the gap is alerted once, and the late record is appended with the next `chain_seq` when it arrives | MSG-P7-012 while the entry is missing | AC7 |
| X5 | An UPDATE, a DELETE or a rewrite of `prev_hash` or `entry_hash` is attempted | Refused by the grant and by `tr_declog_append_only`, the entry unchanged, and the attempt written to the ACE audit log with the table, the operation and the entry ID | None | AC4, TC-E1-028-14 |
| X6 | An entry does not verify on the read | Returned as it is with `chainVerified` false and the warning naming it; one incident to the Compliance queue per entry | MSG-P7-012 | AC5, TC-E1-028-12 |
| X7 | The JOB-14 run is missed or fails | The next run catches up from the last verified `chain_seq` and reports every break with its business date; the missed run is visible on the job monitor | MSG-P7-012 | AC5 |
| X8 | The rwb-case contract does not answer inside the 2 s budget | 404 with the not-found answer and no case fact; the entries are not listed rather than listed without the case they belong to, and the caller retries | The not-found message of RWB-P3-E1028-CON | AC3, AC12, AC13 |
| X9 | The caller holds no Decision log right R | Refused before any entry is read: 403 with no case fact and no entry | MSG-P4-002 | AC8, AC9, AC11, TC-E1-028-12 |

Where the read meets an incomplete day and a failed entry, the answer carries both facts in separate fields and neither hides the other.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P3-E1028-CON and its fake, the store fixture of RWB-P7-E1008-APP and the topic fixture of DP-03; reads its own schema only and calls no other service at run time |
| Negotiable | Nothing business is fixed here: the service levels, the calendar, the legal periods and the parameter are other owners' data; this story fixes the record, the read and the check |
| Valuable | The deadline and the prescription date survive the timer row, the parameter change and the calendar reload, and a break is found the same day |
| Estimable | One consumer, one writer, one hasher, one reader, one Schedule and one chain workflow |
| Small | Fits one sprint with its tests, as a secondary slice of the legacy key |
| Testable | Every criterion in section 7 is one automated test against the topic fixture and the store fixture, with the synthetic case, timer and account date of the legacy story |

### 7. Acceptance criteria

```gherkin
Feature: Service levels, timers, escalation and prescription dates - the deadline decisions in the central ledger

  Background:
    Given the rwb-case contract mock returns case "RW-2026-000401" with case number "RW-2026-000401", queue "LIT-BKK-OFF", team "LIT-BKK" and owner "U-31"
    Given the timer of case "RW-2026-000401" started at 2026-12-01 09:00 on a service level of 5 working days with warn_at 2026-12-08 09:00 and expires_at 2026-12-09 09:00

  Scenario: AC1 The three deadline decisions are held in the ledger (new, D-RCV-60)
    Given DecisionRecorded events arrive on "rwb.decision-record.v1" for the warning, the breach and the prescription date of case "RW-2026-000401"
    When the consumer reads them
    Then three decision_log_entry rows exist for case "RW-2026-000401", one for each record, each with its chain_seq, its prev_hash and its entry_hash
    Then the breach row carries rule_id "R-UNI-30", escalation role "RW-TEAMMGR" and escalation level 1, and the prescription row carries the LEGAL_PERIOD version in force and the business date 2026-03-15 of the last payment date it used
    Then each row carries case_id only: no queue, no team, no owner, no product group and no prescription date is stored

  Scenario: AC2 The deadline is reproduced from the entry alone (new, D-RCV-60)
    Given the warning entry of case "RW-2026-000401" is stored with decided_at 2026-12-08 09:05
    When a reader calls GET /api/recovery/decision/v1/decision-log/{entryId} for it
    Then the answer carries ruleId, ruleVersion, decidedAt, the escalation role and the inputs reference
    Then the inputs reference carries the freshness of each input and names the service level row and its version, the working-day calendar in force and the business date of each account date used, with the timer start 2026-12-01 09:00, warn_at 2026-12-08 09:00 and expires_at 2026-12-09 09:00, so the reader recomputes the deadline without a second source
    Then the rule version is the timer version label in force, the placeholder of section 8 (GAP-1324; ASM-2337)
    Then the answer carries no queue, no team, no owner and no case number read from a column of rwb_decision

  Scenario: AC3 The case read returns the three decisions in decided_at order (new, D-RCV-60)
    Given the prescription, the warning and the breach entries of case "RW-2026-000401" are stored with decided_at 2026-12-01 09:02, 2026-12-08 09:05 and 2026-12-09 09:05
    Given the chain check of 02:00 verified the three entries
    When a reader holding the Decision log right R calls GET /api/recovery/decision/v1/decision-log?caseId=RW-2026-000401
    Then the three entries return in decided_at order: the prescription date, the warning and the breach
    Then each entry carries chainVerified true and its chainSeq, and the answer carries total 3 and no warning
    Then the case number, the queue "LIT-BKK-OFF" and the team "LIT-BKK" are read from the rwb-case contract in that request, once, within the 2 s budget, and no queue, team or case number is read from a column of rwb_decision
    Then a case the contract does not return is answered 404 with no entry listed

  Scenario: AC4 An entry is never updated and a correction is a new entry (new, D-RCV-60)
    Given the breach entry of case "RW-2026-000401" is stored with chain_seq 231 and entry_hash "H-231"
    When an UPDATE of its final_call and a DELETE of the row are attempted through the service role and again through the schema owner role
    Then both are refused and the entry is unchanged
    Then a correction naming the entry is appended as a new row with corrects_entry_id of the breach entry and the next chain_seq
    Then an entry whose prev_hash or entry_hash was rewritten is refused by the same check and reported by the chain check of 02:00, and the case read returns the original and the correction in decided_at order, each with its own chainVerified

  Scenario: AC5 A broken chain is found at 02:00 and reported the same day (new, D-RCV-60)
    Given the entry with chain_seq 230 was changed in the SIT database with the append-only trigger disabled
    When JOB-14 Hash-chain check runs as a Temporal Schedule at 02:00 in queue "rwb-decision"
    Then the check recomputes every entry_hash from chain_seq 1 and finds the break at chain_seq 230
    Then one break report names the entry, its chain_seq and the expected prev_hash, and the break is reported to the Compliance queue the same day
    Then a read of that case returns the entry with chainVerified false and warning MSG-P7-012 naming the entry, and the entries after the break keep their values
    Then the check writes no entry, repairs nothing and deletes nothing

  Scenario: AC6 A repeated event gives one entry (new, D-RCV-60)
    Given event "EV-7f3a-0001" of case "RW-2026-000401" was ingested as one entry with chain_seq 231
    When the same event with the same idempotency key arrives again
    Then one entry exists for the event, the consumer returns the first entry's ID and adds 1 to the repeat count
    Then chain_seq 231 is not used again and no second entry_hash is computed for the event

  Scenario: AC7 A record that has not arrived in five minutes is a gap (new, D-RCV-60)
    Given the breach of case "RW-2026-000401" was decided at 2026-12-09 09:05 and no DecisionRecorded for it arrived by 09:10
    When the completeness check runs
    Then the case is listed with one missing record, naming its decided_at 2026-12-09 09:05, and the gap is alerted to the operations channel once, not once per minute
    Then the case read returns the entries it has, each chainVerified true, and names the missing record, and the record arriving at 09:20 is appended with the next chain_seq and clears the gap

  Scenario: AC8 A caller without the Decision log right R is refused before any entry is read (new, D-RCV-60)
    Given the caller holds no Decision log right R
    When the caller calls GET /api/recovery/decision/v1/decision-log?caseId=RW-2026-000401
    Then the answer is 403 with MSG-P4-002 and carries no case fact and no entry
    Then no decision_log_entry row is read

  Scenario: AC9 A role that holds no Decision log row is refused on the read (new, D-RCV-60)
    Given the caller holds role RW-PHONECOL, which holds no Decision log row in TSD P7 T6.1
    When the caller calls GET /api/recovery/decision/v1/decision-log?caseId=RW-2026-000401
    Then the answer is 403 with MSG-P4-002 and carries no case fact and no entry
    Then no decision_log_entry row is read

  Scenario: AC10 The module holds no rule engine and computes no rule answer (new, D-RCV-60)
    Given the rwb-decision module is built
    When its code and dependencies are scanned for a KieBase, a rule package and a rule registry call
    Then none is found
    When the breach of case RW-2026-000401 is consumed
    Then the entry is stored with its rule and version and no rule call is made

  Scenario: AC11 Both provided operations refuse a caller without the Decision log right R (new, D-RCV-60)
    Given the caller holds no Decision log right R
    When the caller calls GET /api/recovery/decision/v1/decision-log/{entryId} for the warning entry of case RW-2026-000401
    Then the answer is 403 with MSG-P4-002 and carries no case fact and no entry
    Then no decision_log_entry row is read

  Scenario: AC12 A contract read that times out is answered 404 and lists no entry (new, D-RCV-60)
    Given the rwb-case contract does not answer case RW-2026-000401 inside the 2 s budget
    When a reader holding the Decision log right R calls GET /api/recovery/decision/v1/decision-log?caseId=RW-2026-000401
    Then the answer is 404 with the not-found answer and no case fact
    Then no entry is listed without the case it belongs to, and the caller retries

  Scenario: AC13 A failed call to the rwb-case contract gives the answer named in the source and lists no entry (new, D-RCV-60)
    Given the rwb-case contract call for case RW-2026-000401 fails
    When a reader holding the Decision log right R calls GET /api/recovery/decision/v1/decision-log?caseId=RW-2026-000401
    Then the answer is Not specified in the source documents (NEWAC-RWB-P7-E1028-APP-AC17)
    Then no entry is listed without the case it belongs to
```

The thirteen criteria above are new and test only this deliverable: the deadline records in the central ledger, their read and their chain. The legacy criteria of RWB-E1-028 are owned elsewhere: the timer start, the warning, the breach and the prescription date itself, with AC1, AC4, AC5, AC6, AC7, AC8, AC10, AC11 and AC12 of the legacy story, are rwb-case's (RWB-P3-E1028-APP); AC9 and the block when the record cannot be written are the writer story's (RWB-P7-E1027-APP); X9 and the access decision behind a timer read are rwb-access's (RWB-P4-E1028-APP). The legacy test cases this story answers are listed in section 16.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every decision of the Workbench or of a person is written to the central ledger once, and a warning, a breach and a prescription date are decisions of a case like any other | FSD P7 A2.2; TSD P7 T3.1; REQ-CWC-016 |
| BR2 | A breach is recorded with rule ID `R-UNI-30`, the escalation role it went to and escalation level 1, and the case does not move | R-UNI-30; FSD P7 AC-EXC-P7-015-01; legacy AC2 and BR3 |
| BR3 | A deadline is reproducible from its entry alone: the rule ID, the rule version, an inputs reference carrying the freshness of each input, `decided_at` and the escalation role are on the row, and a reader needs no second source | NFR-033; NFR-034; FSD P7 A2.3 and A2.9; legacy BR9 |
| BR4 | Nothing about a case is copied beside the reference: `case_id` is the only case value in `rwb_decision`, and the case number, the queue and the team are read on the rwb-case contract at display time | DP-01; DP-11; Architecture v5 slide 29; legacy AC2 |
| BR5 | The prescription-date record carries the `LEGAL_PERIOD` version in force and the business date of each account date it used, so the date stays recomputable after the legal period changes | REQ-CWC-012; legacy BR4; FSD P7 AC-ALT-P7-009-02 |
| BR6 | The ledger is append only: no entry is updated or deleted, a correction is a new entry that names the entry it corrects, and a re-hashed or edited entry is refused and reported | FSD P7 A2.1 and AC-P7-001-01; TSD P7 T3.1 (DF-DEC-029); ADR-022 |
| BR7 | An action whose record cannot be written does not proceed on the producing side, so a record that arrives here is a record of an action that happened; an append that fails leaves no row and no consumed `chain_seq` | FSD P7 A2.5; R-UNI-39; legacy AC9 |
| BR8 | The stage clock may pause and resume and the prescription clock never does; a pause, a resume or a reload of the calendar writes no new deadline entry and changes no stored one | R-DEV-01; R-UNI-43; legacy BR5 and BR6 |
| BR9 | The chain is checked daily at 02:00, a break is reported to Compliance the same day, and the read carries the failure rather than hiding it; the version in force behind a warning or a breach is the timer version label of the date, and its format and value are Not specified in the source documents (GAP-1324; ASM-2337) | NFR-035; FSD P7 AC-BG-P7-001-01; FSD P3 AC-EXC-P3-037-01 |
| BR10 | A repeated event gives one entry, the repeat is counted, and no `chain_seq` and no hash is computed twice for it | R-UNI-40; FSD P7 AC-EXC-P7-002-03; DP-09 |
| BR11 | The ledger records the rule and the version and evaluates nothing: no Drools package is called from this service and no rule answer is computed here | DP-04 (not applied); Architecture v5 slide 14 |

How the rules hold in `rwb-decision`:

- BR1 and BR10 are executed by `DecisionRecordConsumer`: one event, one inbox row, one entry, and the first entry's ID on a repeat. BR2 and BR3 are executed by the shape check and the columns: a deadline record without its rule ID, its version, its inputs reference or its escalation role is refused rather than stored with a hole.
- BR4 is executed by the schema and the reader: `rwb_decision` holds no queue, team, owner, product group or prescription date column, and the case number, the queue and the team come from the contract on each read.
- BR5 to BR8 are executed by the columns, by `corrects_entry_id` and by the trigger; this story adds no column and no trigger, and a pause of the clock writes nothing. BR9 is executed by JOB-14 and by the per-entry check on the read, and BR11 by the absent dependency: the module holds no KieBase, no rule package and no call to the rule registry.

### 9. State transitions

The case state machine and the timer state machine are not this service's. `rwb-decision` holds no case state and no timer state, and this slice reads no timer row and changes none. What this section fixes is the life of an entry, which has one direction:

| From | Event | Condition | To |
|---|---|---|---|
| None | `DecisionRecorded` on `rwb.decision-record.v1` | The inbox check and the shape check pass | One `decision_log_entry` row with the next `chain_seq`, its `prev_hash` and its `entry_hash` |
| Stored | A correction `DecisionRecorded` | The record names the entry it corrects | A new row with `corrects_entry_id` set and the next `chain_seq`; the corrected row is unchanged |
| Stored | JOB-14 at 02:00 | The `entry_hash` or the `prev_hash` does not match | One break report and `chainVerified` false on the read; the row is unchanged and nothing is repaired |
| Stored | A repeated `DecisionRecorded` | The same event ID or `idempotency_key` | No row, no `chain_seq`, one repeat count |
| Stored | An UPDATE, a DELETE or a hash rewrite | None | Refused; the row is unchanged and the attempt is audited |

An entry never leaves the stored state: there is no delete, no rollback of a stored entry, and no state column that this slice sets.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-decision service identity | Consumes `DecisionRecorded`, appends entries, runs the chain check, and writes no record of its own |
| RW-AUDIT, internal audit; RW-COMPLY, compliance and PDPA officer | Read the deadline decisions of any case in scope and reproduce a deadline from one entry |
| RW-TEAMMGR, team manager | Read the deadline decisions of the cases of the team, including the breach it was escalated to |
| RW-CASEOWN, case owner; RW-LITOFF, litigation officer | Read the deadline decisions of their cases, including the prescription date entry |
| SY-CASEWF, case workflow module; SY-DECLOG, decision log writer | Publish `DecisionRecorded` for the records this service collects; neither holds a read on `rwb_decision` |
| RW-PLATADM, platform administrator | Run and rerun JOB-14 through the job operations of the platform, and see the break report and the gap alert |
| Every service of the 19 | Publishes its own decision records on `rwb.decision-record.v1`; none of them writes or reads `rwb_decision`; rwb-case (P3) owns the timer, the service level row, the calendar, the warning, the breach and the prescription date, and this service reads the case number, the queue and the team through the contract only |

The authorisation decision is the cached permission decision from rwb-access that the service template's guard already holds; DP-08 is not in this slice's pattern set, so this story adds no guard, no decision endpoint and no access row of its own. The role codes above are rows of the role model in `rwb_access` and are not fixed in code. The per-service login is fixed by the platform DB story of this service; DP-02 is not in this slice's pattern set and its name is not used here.

### 11. Data

| BR Field ID | Table in rwb_decision | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 | decision_log_entry | id | Write; read back on the case read and the single read |
| DF-DEC-002 | decision_log_entry | case_id (the only case reference on the entry) | Write; taken from the record, never from a copy of the case |
| DF-DEC-003 | decision_log_entry | decision_code | Write; validated against LOV-DECISION |
| DF-DEC-004 | decision_log_entry | rule_id | Write; for a breach, `R-UNI-30` |
| DF-DEC-005 | decision_log_entry | rule_version | Write; for a breach, the timer version label in force |
| DF-DEC-008 | decision_log_entry | inputs_ref | Write; with the freshness of each input and the business dates used |
| DF-DEC-012 | decision_log_entry | final_call | Write |
| DF-DEC-014 | decision_log_entry | actions | Write; a breach carries its escalation role and level here |
| DF-DEC-015 | decision_log_entry | outcome | Write; empty at the decision, filled by the outcome record of its own story |
| DF-DEC-016 | decision_log_entry | decided_at | Write; the order of the case read |
| DF-DEC-017 | decision_log_entry | prev_hash, entry_hash | Write; the `entry_hash` of the entry before or 64 zeros, and the SHA-256 of the canonical form |
| DF-DEC-028 | decision_log_entry | chain_seq | Write; allocated once, never reused |
| DF-DEC-029 | decision_log_entry | corrects_entry_id | Write; empty, or the entry this one corrects |
| DF-DEC-030, DF-DEC-031 | decision_log_entry | actor_user_id, idempotency_key | Write; the inbox duplicate check |
| DF-DEC-006, DF-DEC-007, DF-DEC-010, DF-DEC-011, DF-DEC-013 | decision_log_entry | model_version, agent_version, approver_user_id, approval_level, override_reason | Write as the record carries them; empty for a deadline record of a timer |
| (standard columns, TSD P7 T3.0) | decision_log_entry | created_at, created_by | Write |
| processed_event | inbox of the PLT library | event id, idempotency key, repeat count | Write |
| case_no, queue, team through RWB-P3-E1028-CON | case | case_no, queue, team | Read only, on each read; never written |

Field IDs are those in TSD P7 T3.1 and the Logical Data Model and Data Dictionary. `case_id` is the only case value in the schema: there is no queue, team, owner, product group, status or prescription date column and no foreign key to `rwb_case` (BR4). The escalation role and the escalation level of a breach have no column of their own in TSD P7 T3.1 and ride in `actions` (DF-DEC-014) until the schema fixes them (GAP-1324; ASM-2337). The timer version label is the placeholder of section 8 (GAP-1324; ASM-2337). The trigger `tr_declog_append_only` is a database object created by the store story RWB-P7-E1008-APP, not a field or entity of the logical data model, so it has no row in section 11.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path on base `/api/recovery/decision/v1` | Response | Access |
|---|---|---|---|
| API-P7-006 | `GET /decision-log?caseId={caseId}` | `DecisionLogPage`: `items`, `page`, `size`, `total`, `warning`; each item is a `DecisionLogEntry` with `chainVerified` and `chainSeq` | Decision log, right R, scope applied |
| API-P7-007 | `GET /decision-log/{entryId}` | `DecisionLogEntry` with its inputs reference, its rule ID and version, its chain fields and `chainVerified` | Decision log, right R, scope applied |

Both are declared in TSD P7 T-A.1 and T-A.2 with the error answers 401, 403, 404 and 503; DP-13 re-bases them from `/api/recovery/v1` to `/api/recovery/decision/v1` and changes no path segment, no query name and no response field. This story fixes what they return for the deadline decisions of a case: the `caseId` filter, the `decided_at` order, the `chainVerified` flag computed per entry, and the warning MSG-P7-012 when an entry fails. The other filters (`decision`, `ruleId`, `approver`, `from`, `to`), the paging, the size limit, the export and the search behaviour are the read story's (RWB-P7-E2005-APP); this story adds no operation, no filter and no field of its own.

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | rwb-case (P3), under RWB-P3-E1028-CON | The case number, the queue and the queue's team of a case read, so that no case value is stored on an entry and an escalation is read against the team it went to | One hop, 2 s (DP-11); held for the request only |

The contract is consumed as the published OpenAPI 3.1 document plus its fake. This slice calls no other service: the account dates, the legal period and the service level arrive inside the record, and no ACE view is read (DP-05).

#### 12.3 Events published

None. `rwb.decision.events.v1` carries `ApprovalRequested`, `ApprovalDecided` and `RulePackageInForce` from the approval and rule slices of the same service (Architecture v5 slide 14). A deadline decision publishes nothing: the record already exists in the producer's schema and the ledger is the collector (DP-03).

#### 12.4 Events consumed

| Event | Topic | Producer | Used for |
|---|---|---|---|
| `DecisionRecorded` (EV-08) | `rwb.decision-record.v1` | Every one of the 19 services, through its outbox | The three deadline records and every other decision this service collects into the central ledger |

The topic is the shared decision-record topic of R-4 and Architecture v5 slide 42: CloudEvents binary mode, keyed on the case ID, with the retry topics and the dead-letter topic of DP-09. The consumer dedupes on the inbox by event ID and `idempotency_key`, commits the offset only after the append commits, and targets the five-minute completeness of Architecture v5 slide 28 with the gap alert of AC7. The continuous ingest is JOB-13, which is this consumer and not a Schedule (Architecture v5 slide 44).

#### 12.5 Workflows and activities

| Workflow or activity | Queue | Purpose |
|---|---|---|
| `HashChainCheckWorkflow` with `verifyChainSegment` (activity) | `rwb-decision` | The workflow JOB-14 starts: reads the entries in `chain_seq` pages, recomputes and compares, and produces the break report; the activity verifies one page and is idempotent, so a retry re-reads the same page and reports the same break |

No other workflow and no other activity belongs to this story. The retry policy is the workflow kit's default (DP-10), and the activity writes nothing.

#### 12.6 Schedules

| Schedule | Job | When | Queue | What it does |
|---|---|---|---|---|
| `hash-chain-check` | JOB-14 Hash-chain check | 02:00 daily | `rwb-decision` | Starts `HashChainCheckWorkflow`; overlap policy SKIP with the catch-up window of the kit; reports every break with its business date |

JOB-14 is a Temporal Schedule, not a Quartz job and not a platform batch (DP-10; Architecture v5 slide 44). JOB-13 is not a Schedule: the ingest is continuous on Kafka (12.4). JOB-20 Rule promote at 00:01 and its `RulePackageInForce` are RWB-P7-E1073-APP's, and this story holds no rule Schedule.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `decision_log_entry` | P7 (rwb_decision) | One row per decision, append only and hash chained; this slice writes the deadline records and reads them for a case and by entry ID |
| `approval` | P7 (rwb_decision) | The approval queue, owned by the approval slices; this slice reads nothing from it. `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are also P7's, owned by RWB-P7-E1073-APP, and this slice calls no rule package |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_decision` | Outbox, inbox and idempotency objects (DP-09); this slice writes the inbox and idempotency rows |

No `rwb_case` table is read and no `v_ace_*` view is read (DP-01, DP-05). `rwb_decision` holds no foreign key into another schema, the case is reached through the contract, and the case number is never stored.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case contract fake (RWB-P3-E1028-CON) | The P3 case read | Case `RW-2026-000401` with case number `RW-2026-000401`, queue `LIT-BKK-OFF`, team `LIT-BKK`, owner `U-31`; case `RW-2026-000402` for `HIRE_PURCHASE`; a not-found answer for `RW-2026-000499`; a slow answer past the 2 s budget |
| decision-record topic fixture (DP-03, RWB-PLT-E1027-CON) | `rwb.decision-record.v1` | A warning record, a breach record with `R-UNI-30` and escalation role `RW-TEAMMGR`, a prescription record with the `LEGAL_PERIOD` version and the business date 2026-03-15, a repeated event, and an event that never arrives |
| store fixture (RWB-P7-E1008-APP) | `decision_log_entry` and its trigger | The append-only trigger, the sequence for `chain_seq`, and a row rewritten with the trigger disabled for the chain test |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 1 consumed | `GET /decision-log` and `GET /decision-log/{entryId}` on `/api/recovery/decision/v1`; `GET /cases/{caseId}` on the rwb-case contract, one hop within 2 s (DP-11) |
| Kafka | 0 published, 1 consumed | `DecisionRecorded` on `rwb.decision-record.v1`, idempotent into `decision_log_entry` |
| Temporal | 1 Schedule, 1 workflow, 1 activity | JOB-14 at 02:00 starts `HashChainCheckWorkflow` with `verifyChainSegment` (DP-10) |
| File | None | This slice writes no file; the daily ledger seal to write-once storage is the store story's (RWB-P7-E1008-APP) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `deadlines`, Java package `th.co.scb.ace.workbench.recovery.decision.deadlines`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DecisionRecordConsumer | Kafka listener | Reads `DecisionRecorded`, checks the inbox and the shape, and answers a repeat with the first entry's ID and one repeat count |
| DeadlineLedgerWriter and ChainHasher | Service | Checks the record, allocates `chain_seq`, takes `prev_hash`, computes `entry_hash` as the SHA-256 of the canonical form, and appends one row in one statement |
| ChainCompletenessChecker | Service | Lists a decision whose record has not arrived within five minutes of its `decided_at`, alerts once, and clears the gap |
| DecisionLogReader | Service | Reads the deadline decisions of a case in `decided_at` order and one entry by ID, computes `chainVerified`, and takes the case number, the queue and the team from the contract |
| CaseReferenceClient | REST client | Calls `GET /cases/{caseId}` on the rwb-case contract, one hop and 2 s, and maps 404 and the slow answer |
| DecisionLogController and DecisionLogRepository | Controller and repository | The two reads, `decision_log_entry` and the inbox in `rwb_decision`; no other schema is read |
| HashChainCheckWorkflow and verifyChainSegment | Workflow and activity | JOB-14: the page-by-page verification and the break report |

**Database and migrations**

- Writes `decision_log_entry` (the DF-DEC fields of section 11) and the inbox row; reads the same table for the two reads and the chain check, and uses the index `ix_declog_case_time` on `(case_id, decided_at)` for the case read, which RWB-P7-E1008-APP creates; this slice adds no index.
- This story adds no column, no index, no trigger and no migration: the table, the columns, `tr_declog_append_only`, the hash rules and the indexes are the store story's, and DP-15 applies to this service's Flyway sequence as the sequence the store story opens. No row is seeded here; LOV-DECISION and LOV-APPROVAL-LEVEL are loaded by their reference-data story, and no list value is written in code.

**Configuration and reference data**

- No business value is configured here: the service levels, the warning percentage, the escalation roles, the calendar, the legal periods and the parameter `legal.prescription.warn.days` = 180 belong to rwb-case and to the reference-data and parameter owners; this service receives them inside the record and stores the reference. Three settings only: the rwb-case contract base, the topic subscription of `rwb.decision-record.v1`, and the completeness window of five minutes (Architecture v5 slide 28); the 2 s timeout and the one-hop rule are the platform values of DP-11, set in the client configuration.

**Build steps**

1. `DecisionRecordConsumer` with the inbox check, the repeat answer and the offset rule, and `DeadlineLedgerWriter` with `ChainHasher`: the shape check, the sequence allocation and the hash pair; tests for AC1, AC4 and AC6.
2. The three records end to end against the topic fixture, with the escalation role and level of the breach and the legal period version and account business date of the prescription record; tests for AC1 and AC2.
3. `DecisionLogReader` with the `caseId` filter, the `decided_at` order and `chainVerified`, and `CaseReferenceClient` for the case number, the queue and the team; tests for AC3 and the 404 of X8.
4. `ChainCompletenessChecker` with the five-minute window and the single alert, and `HashChainCheckWorkflow` with `verifyChainSegment` as the JOB-14 Schedule; tests for AC5, AC7 and X7.
5. A schema assertion that `rwb_decision` holds no queue, team, owner, product group or prescription date column, and a boundary test that no class outside the module updates an entry; tests for AC4 and TC-E1-028-14.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_decision`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

This is a secondary slice with no owned legacy acceptance criteria of a build story: it adds no new build dependency of its own (metadata "Depends on (build)" = None) and builds against the store fixture of RWB-P7-E1008-APP, the topic fixture of RWB-PLT-E1027-CON and the RWB-P3-E1028-CON fake. Read one by one:

- DP-01 and DP-13 are the target shape itself: `rwb_decision` and the base `/api/recovery/decision/v1` replace the shared recovery schema and the monolith base, with no new dependency. DP-03 is the one live data pattern: the record arrives on the shared topic from the library of every producer and this service collects it, and the library is a platform contract of the service lane, so no build dependency is added.
- DP-04 is not in the pattern set and is not applied: no Drools package is evaluated, no KieBase is held, and no rule answer is computed here.
- DP-05, DP-06 and DP-07 apply as prohibitions and statements: no ACE view is read, the parameter values reach this service only as facts inside a record, and the legal period rows and the lists stay with their owners.
- DP-09 applies to the consumer: the inbox dedupe, the CloudEvents envelope, the retry topics and the dead-letter topic, with the case ID as the key and IDs and facts only. DP-14 keeps every topic name in the naming library.
- DP-10 applies to JOB-14 as a Temporal Schedule in `rwb-decision`, DP-11 to the one case read with its 2 s timeout and fake, DP-15 to the per-service Flyway sequence the store story opens, and DP-19 to the gateway-bff route behind the read.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P3-E1028-CON stay green, and a SIT week shows three deadline records per case with their chain fields, no case value beyond `case_id` in `rwb_decision`, one entry on a repeated event, the JOB-14 run finishing inside its window with a break found and reported the same day, and the case read returning the three decisions in `decided_at` order with `chainVerified`.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-012 | An entry on the read does not match the chain, or a decision record has not arrived | Entry {entryId} does not match the decision log chain. Do not rely on it until Compliance has reviewed it. |
| MSG-P7-003 | The ledger cannot be written at the moment a record is collected | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-009 | A collected record is refused by the shape check | The decision record was refused: {field} is missing or not valid. |
| MSG-P4-002 | The caller's role holds no Decision log right R | You cannot {action} here. Your role does not include it. |
| MSG-GEN-003 | The read is called with `from` after `to` | {field} cannot be before {other}. |

The MSG-P7-012 text is the one RWB-P7-E2005-APP publishes for the read, and the {entryId} placeholder carries the entry ID, not a case fact. For MSG-P7-009 the {field} value names the missing field, for example "ruleVersion" or "inputsRef". For MSG-P4-002 the {action} value names the action the caller tried, "read the decision log", and never a case fact. For MSG-GEN-003 the {field} value names "to" and the {other} value names "from". Every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. The read answers 401 with MSG-P4-001 for a caller with no Recovery role, 403 with MSG-P4-002 for a role without the right, 404 for an entry ID or a case the contract does not return, 422 with MSG-GEN-003 for a date range out of order, and 503 when the ledger or the case contract cannot be reached. Read states: empty, a case with no entry is answered with total 0 and no entry; no access, 403 with MSG-P4-002; error, 503 with a messageId Not specified in the source documents (CG-ALL-6939); loading, Not specified in the source documents (DOR-RWB-P7-E1028-APP-10). The screen states of SCR-03 and SCR-38 belong to RWB-P3-E1028-APP, not to this service.

### 15. Screens and states

SCR-38 Decision log shows the entries of a case with the case number, the queue and the team read from the rwb-case contract, the decision, the rule ID and version, `decided_at`, the escalation role and `chainVerified`, and it shows MSG-P7-012 at the top when an entry fails the chain; the deadline panel of SCR-03 Case record shows the warning, the breach and the prescription date of the open case from the same read. Both are served by the gateway-bff composite route (DP-19), one hop each, and the screen itself with its filters, paging, export and empty state is RWB-P7-E2005-APP and RWB-P5-E1026-APP's. This story fixes only what the entries carry, the order they arrive in, the chain flag, and the two states it makes visible: an entry that fails the chain, and a day whose records are incomplete. Screen states: SCR-03 loading as Screen Specifications v1 gives it, and empty, error and no access Not specified in the source documents (CG-ALL-6938); SCR-38 loading as Screen Specifications v1 gives it, and empty, error and no access Not specified in the source documents (CG-ALL-6939).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-028-12 | X9, BR1: a role without the Decision log right R is refused, and a service identity whose letter is C is refused the read; the access answer behind a timer read is rwb-access's | Component | Role `RW-PHONECOL`, which holds no Decision log row in TSD P7 T6.1, calls `GET /decision-log` and is refused with MSG-P4-002; service identity `SY-OCR` holds C and is refused the same way |
| TC-E1-028-01 | AC2, BR3: the start of the timer and its computed `warn_at` and `expires_at` are reproducible from the warning entry; the clock itself is rwb-case's | End to end | Case `RW-2026-000401` placed in `LIT-BKK-OFF` at 2026-12-01 09:00; service level 5 working days, warning 80 percent, `warn_at` 2026-12-08 09:00, `expires_at` 2026-12-09 09:00 |
| TC-E1-028-02 | AC1, AC2, AC3, BR2, BR3, BR4: the warning and the breach are entries with their rule, version and escalation role, and the case keeps its queue and owner | End to end | Timer of case `RW-2026-000401` passing `warn_at` and then `expires_at`; rule `R-UNI-30`, escalation role `RW-TEAMMGR`, escalation level 1, owner `U-31` |
| TC-E1-028-03 | AC1, AC2, AC3, BR5: the prescription-date record carries the legal period version and the account business date | End to end | Case `RW-2026-000402`, `HIRE_PURCHASE`, one account, last payment date 2026-03-15, legal period 2 years, prescription date 2028-03-15, `warn_at` 2027-09-17 |
| TC-E1-028-04 | AC3, BR5: a case with no service level has no warning and no breach entry, so the read returns the prescription entry alone | Contract | Queue `NPA-BKK-CO` with no service level in force on 2026-12-01; MSG-P3-026 on the exception queue |
| TC-E1-028-05 | AC3, BR5: a product with no legal period has no prescription entry, so the read returns the warning and the breach only | Contract | Product `SSME` with no legal period row; MSG-P3-026 for "legal period" and "SSME" |
| TC-E1-028-06 | AC2, BR3, BR5: the record names the contract date it used when an account has no last payment date | End to end | Case `RW-2026-000405`, no last payment date, contract date 2025-06-30, prescription date 2027-06-30 |
| TC-E1-028-07 | AC1, AC3, AC6, BR10: three breaches from one pass are three entries with consecutive `chain_seq` and no repeat | Component | Timer worker paused from 10:00 to 10:40; three timers passing `expires_at`; the worker resumed at 10:45 delivers three events |
| TC-E1-028-08 | AC6, BR10: a repeated event gives one entry and one repeat count | Component | Timer already EXPIRED at escalation level 1; the same event with the same `idempotency_key` delivered twice; `EV-7f3a-0001` |
| TC-E1-028-09 | X3, AC7, BR7: an append that fails leaves no row and no consumed `chain_seq`, and the record is redelivered | NFR | Ledger store unavailable at 10:00 for case `RW-2026-000407`; the event redelivered at 10:05; MSG-P7-003 on the job record |
| TC-E1-028-10 | AC4, BR8: a pause and a resume of the stage clock write no entry here and change none, and the prescription entry keeps its date | End to end | Case `RW-2026-000408`, `DeviationRaised` 2026-12-02 and `DeviationCleared` 2026-12-04; prescription date 2028-03-15 unchanged; R-UNI-43 and R-DEV-01 |
| TC-E1-028-11 | AC2, BR3: the warning point of a five-day service level is reproducible from the entry for the run that sent it | Component | Timer of 5 working days from Monday 2026-12-14 08:00; run at 2026-12-18 08:05 sends one warning with end date Monday 2026-12-21; no warning from the run at 07:55 |
| TC-E1-028-13 | X3, X6, AC5, BR7, BR9: the record path is resilient and the chain reports every break it finds in one run | NFR | The append forced to fail for every breach in one run; the chain check then run over a day with two rewritten entries; two break reports and no lost record |
| TC-E1-028-14 | AC4, BR6: no class outside the module updates an entry, and the schema holds no case value beyond `case_id` | Component | A class outside `decision.deadlines` issues an UPDATE through the service role; `tr_declog_append_only` and the missing grant refuse it; the schema assertion finds no queue, team, owner or prescription date column |
| TC-E1-028-15 | Section 12.7 boundary: each table owned in section 12.7 accepts its boundary rows, the first and the last `chain_seq` of a case and the repeat of an inbox key | Component | Case `RW-2026-000401` with entries at its first and last `chain_seq` (Not specified in the source documents (DOR-RWB-P7-E1028-APP-12)); an event repeated with the same `idempotency_key` written to `processed_event` |
| TC-E1-028-17 | AC9, X9: a role with no Decision log row is refused on the list read | Component | Role `RW-PHONECOL`, which holds no Decision log row in TSD P7 T6.1, calls `GET /decision-log` for `RW-2026-000401`; refused with MSG-P4-002 |
| TC-E1-028-18 | AC10, BR11: no rule engine is in the module and no rule answer is computed for a breach | Component | Scan of the `rwb-decision` module for a KieBase, a rule package and a rule registry call; the breach of case `RW-2026-000401` (R-UNI-30) consumed with no rule call |
| TC-E1-028-19 | AC11, X9: both provided operations refuse a caller without right R with 403 | Component | Caller without the Decision log right R calls `GET /decision-log/{entryId}` for the warning entry of `RW-2026-000401`; 403 with MSG-P4-002 |
| TC-E1-028-20 | AC12, X8: a contract read over the 2 s budget is answered 404 and lists no entry | NFR | rwb-case contract stub silent beyond 2 s for `RW-2026-000401`; caller holds the Decision log right R; 404 with the not-found answer |
| TC-E1-028-21 | AC13, X8: a failed contract call gives the answer named in the source and lists no entry | NFR | rwb-case contract stub returns an error for `RW-2026-000401`; answer Not specified in the source documents (NEWAC-RWB-P7-E1028-APP-AC17) |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The legacy levels map as the other service stories of this set map them: System to End to end, Access to Component, Resilience to NFR and Build to Component. Every legacy test case of RWB-E1-028 is listed above with the slice of the behaviour this story answers, and the -ITG copies belong to RWB-ITG-E1028-ITG, which proves the same values across rwb-case, rwb-access and rwb-decision end to end.

### 17. Guardrails

- No business value in code: the service levels, the warning percentage, the escalation roles, the calendar, the legal periods and the parameter are data of other owners; this slice stores the version a record names and computes none of these values.
- No personal data in events, workflow inputs, logs or tests. This story writes case IDs, rule IDs, versions, entry IDs, hashes and business dates only; test data uses the synthetic keys of section 3.
- No cross-schema read (DP-01): `rwb_decision` reads no `rwb_case` table and no table of another service, and the case is reached only through the contract, one hop and 2 s; ACE data only through the owner's contract or `v_ace_*` views, and this service reads neither (DP-05), because the account dates behind a prescription record arrive as business dates inside the record.
- Append only is not a convention: the grant, the trigger and `corrects_entry_id` make an update, a delete and a re-hash impossible, and this story adds no path that could bypass them.
- The chain is written in one statement with the row: no `chain_seq` is reserved before an append, no hash is computed for a row that is not stored, and a failed append leaves the sequence unused; the chain check repairs nothing, so a break stays visible until a person decides what to do.
- No rule evaluation: the module holds no KieBase and no rule package (DP-04 is not applied), and no business rule of a deadline is evaluated here.
- The Kafka key of a collected record is the case ID (DP-09), and no topic name is typed in code (DP-14).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-011 | Service levels, warnings and escalation as data; a breach does not move the case and goes to the named point | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-11, FEAT-CWC-13 | All recovery processes | R-UNI-30 | TC-E1-028-02, TC-E1-028-07, TC-E1-028-08, TC-E1-028-11 |
| REQ-CWC-012 | Prescription dates set from the legal periods at creation and visible at all times | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-12 | 08 Litigate and enforce | R-DEV-01 | TC-E1-028-03, TC-E1-028-04, TC-E1-028-05, TC-E1-028-06, TC-E1-028-10 |
| REQ-CWC-016 | Every timer event logged with the rule ID and the rule version that caused it | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-13, FEAT-CWC-21 | All recovery processes | R-UNI-39, R-UNI-40 | TC-E1-028-01, TC-E1-028-02, TC-E1-028-09, TC-E1-028-12, TC-E1-028-13, TC-E1-028-14 |

FEAT-CWC-11, FEAT-CWC-12 and FEAT-CWC-13 are carried by the case service; this slice answers them on the ledger side, where the deadline has to survive the timer row, and FEAT-CWC-21 only for the record, the read and the chain. The -ITG copies are carried by RWB-ITG-E1028-ITG.

| Legacy reference | Where it is kept |
|---|---|
| Legacy key RWB-E1-028; story RWB-P7-E1028-APP; contract RWB-P3-E1028-CON; baseline `rwb_decision` | Metadata; sections 1, 3, 12 |
| The three deadline records: the warning, the breach with `R-UNI-30` and escalation level 1, the prescription date from the legal period | Sections 1, 4, 8 (BR2, BR3, BR5), 7 |
| Legacy BR9 and REQ-CWC-016; legacy BR4 and REQ-CWC-012 with the legal period of 2 years from the last payment date | Sections 2, 8 (BR3, BR5, BR9), 11, 16 |
| R-UNI-30, R-UNI-43, R-DEV-01 and the prescription clock that never pauses | Sections 8 (BR2, BR8), 9, 19 |
| NFR-033, NFR-034 and NFR-035; the 02:00 check; the five-minute completeness and the daily anchor | Sections 2, 4, 8 (BR3, BR9), 12.4, 12.5, 12.6 |
| Synthetic values: `RW-2026-000401`, `LIT-BKK-OFF`, `LIT-BKK`, `U-31`, `warn_at` 2026-12-08 09:00, `expires_at` 2026-12-09 09:00, `RW-2026-000402`, 2026-03-15, 2028-03-15, 2027-09-17 | Sections 3, 7, 11, 16 |
| MSG-P7-012, MSG-P7-003, MSG-P7-009, MSG-P4-002, MSG-GEN-003 | Section 14; exception paths |
| Field IDs DF-DEC-001 to DF-DEC-018 and DF-DEC-028 to DF-DEC-031 | Section 11 |
| Legacy test cases TC-E1-028-01 to TC-E1-028-14, and the other slices of RWB-E1-028 (rwb-case, rwb-access, the integration proof) | Sections 16, 1, 2, 19 |

### 19. Out of scope

- The timer itself, the `SERVICE_LEVEL` rows, the warning percentage, the escalation roles, the calendar, the warning and the breach raising and the prescription calculation: rwb-case (RWB-P3-E1028-APP), with its contract RWB-P3-E1028-CON.
- The legal period rows, owned by Legal, and the parameter `legal.prescription.warn.days` = 180, owned by the parameter owner: they reach this service only as facts inside a record (DP-07 and DP-06).
- The deviation pause and resume of the stage clock (R-DEV-01, R-UNI-43): rwb-deviation and rwb-case.
- The access decision behind a timer read and a case read, and the escalation grant: rwb-access (RWB-P4-E1028-APP).
- The store, its columns, its append-only trigger, its hash rules, its indexes and the daily ledger seal to write-once storage: RWB-P7-E1008-APP.
- The writer that makes a record at the point of a decision, with the block when it cannot write: RWB-P7-E1027-APP.
- Rule authoring, its test cases, the four eyes, the rollback and the 00:01 rule promotion with `RulePackageInForce`: RWB-P7-E1073-APP.
- The approval queue, its routing by the delegation of authority and the escalation of an overdue approval (Epic 2): the approval slices of this service; and the decision log search screen SCR-38 with its filters, paging, export and empty state (RWB-P7-E2005-APP), with the case screens (RWB-P5-E1026-APP and the case stories).
- The prescribed litigation review at the prescription warning threshold (R-UNI-31, CTL-18): Epic 2; the reporting projection of `DecisionRecorded` into rwb-reporting: rwb-reporting; and the end-to-end proof across rwb-case, rwb-access and rwb-decision: RWB-ITG-E1028-ITG.
