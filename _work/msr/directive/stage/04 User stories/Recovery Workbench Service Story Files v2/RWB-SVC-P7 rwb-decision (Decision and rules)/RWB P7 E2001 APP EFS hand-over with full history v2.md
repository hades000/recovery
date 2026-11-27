# RWB-P7-E2001-APP EFS hand-over with full history

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-001 for rwb-decision. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (18 resolved, 29 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P7-E2001-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-001 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Set by the squad at refinement (DOR-RWB-P7-E2001-APP-16) |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP18, DP19 |
| Parallel lane | L-P7-Q |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E2001-CON; RWB-P3-E1043-CON (product group map, client library RWB-PLT-E1043-CON) |
| Contract version | Not specified in the source documents (DOR-RWB-P7-E2001-APP-23); path /api/recovery/decision/v1 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to REQ-DRI-013, REQ-CHO-001, REQ-CHO-005, REQ-RDF-003) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **every case created or linked from the ACE hand-over record to carry one sealed decision entry in the central ledger of rwb-decision, naming the ACE business date, the entry rule in force and the EFS contact and promise history it carried**, so that **what happened before day 90 is provable from the decision record itself, and not only from the case timeline**.

This is the `rwb-decision` slice of legacy RWB-E2-001 (`Split (rework)`). The hand-over run, the ACE reads and the run summary stay with `rwb-integration` (RWB-P2-E2001-APP and RWB-P2-E2001-CON), the case and the account link with `rwb-case` (RWB-P3-E2001-APP), the ACE views with `rwb-source-data`, and the interaction ledger with `rwb-source-data` under the default ruling and DP-18. What this story owns is one thing done exactly: the decision record of each hand-over, its chain link, its inputs snapshot, its outcome and the two reads that return it.

### 2. Business rationale

An account enters Recovery at 90 days past due and the case starts the next morning; the collection history before day 90 arrives with it from the EFS source (REQ-CHO-001, REQ-RDF-003). An officer must be able to show what the bank did with the customer before the case existed, and an auditor must be able to show on what data and under which rule version the case was entered. In the monolith that proof was one row in the single `recovery` schema, written by SY-DECLOG in the same transaction as the case creation, holding the business date and the history it carried.

Architecture v5 keeps the proof and changes every mechanism around it. The decision record is written where the decision is taken, by the local decision-record library, and relayed on the shared topic `rwb.decision-record.v1` (DP-03, ADR-022); `rwb-decision` seals each record into `decision_log_entry` in `rwb_decision` within five minutes, hash-linked to the entry before it, and serves it on its own contract; the business date and the freshness of each input sit in the inputs snapshot, so a record is reproducible; and each hand-over record is one entry and never two, whatever the run does (R-UNI-40). The story meets REQ-DRI-013 and REQ-CHO-005 and is measured by CTL-06: no case exists in SIT without its entry.

### 3. Preconditions

- RWB-P7-E1008-APP is done: `decision_log_entry` exists in `rwb_decision` with the canonical form, `chain_seq`, `prev_hash`, `entry_hash`, the append-only trigger and the chain verifier.
- RWB-P7-E1027-CON is published: the record shape, the refusal with MSG-P7-009, the outbox relay, the shared topic `rwb.decision-record.v1` and the five-minute ingest target (DP-03).
- RWB-P7-E2005-CON is published: the `DecisionLogEntry` resource and the two reads on base `/api/recovery/decision/v1`, so the read side is fixed before the write side is built.
- RWB-P2-E2001-CON is live and faked (the one C row of this story): one record per account and business date, keyed on the account and the business date, naming the case or the link, the decision code and the entry rule with its version (DP-11).
- The platform contracts the pattern table adds are live: RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON and RWB-PLT-N001-CON. The story line carries no H row and the lane therefore starts on Day 1 (GAP-2468; ASM-4097).
- Parameters are read as data through DP-06: `case.entry.dpd_threshold` = 90 (DL16) and `handover.hold_until` = 09:00. No value is written in code.
- Reference data is read through DP-07: LOV-DECISION, LOV-PRODUCT and the EFS action codes of `efs_ledger_outcome` (DL29).
- The service login of `rwb-decision` holds INSERT and SELECT on `rwb_decision.decision_log_entry` and no grant on any other schema; the ACE views `v_ace_account`, `v_ace_customer` and `v_ace_efs_action` are read by `rwb-source-data` and never here (DP-01, DP-05).
- No approval stop: the story starts at status Draft (realignment v1) and only H rows block the build (Template and Rules §R5.7; ASM-4098).

### 4. Flow

1. The hand-over run of `rwb-integration` selects the accounts at or above the threshold for business date D and, before it creates or links a case, submits one decision record through the local library, as SY-DECLOG did in the monolith (DP-03).
2. The library writes the local record and the outbox row in one transaction and the relay publishes `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` (EV-08, DP-09).
3. `DecisionRecordListener` consumes the record on the `rwb-decision` login, writes it to the inbox and skips a record whose idempotency key is already stored (BR6).
4. `DecisionRecordMapper` maps the record to one row of `decision_log_entry`: decision code D6, final call `CASE_CREATED`, actor `SY-CASEWF`, no approver and no approval level, `inputs_ref` naming business date D with the stamp of DP01 and DP05, `actions` holding the EFS history items, `outcome` naming the case created or the case an account was linked to.
5. `ChainSealer` reads the head of the chain, assigns `chain_seq` n+1 and `prev_hash`, computes `entry_hash` over the canonical form of the entry and inserts it in one transaction in `rwb_decision` (DP-01).
6. Where the insert fails, nothing is written, the inbox record stays unprocessed, the caller is refused with MSG-P7-003 and an incident is raised, so no case exists without its entry (BR7, R-UNI-39).
7. The entry is served on `GET /api/recovery/decision/v1/decision-log/{entryId}` and by the query of RWB-P7-E2005-APP; both reads hold SELECT only and change nothing.
8. The nightly chain check of RWB-P7-E1008-APP verifies the entry with the rest of the ledger; this story adds no timer, no purge and no correction.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The same account and business date arrive twice | No second entry; the entry already stored is returned; the repeat is counted under R-UNI-40 | None | AC3 |
| X2 | The ledger store of `rwb_decision` does not answer | The write is refused, nothing is stored, `chain_seq` is not used, an incident is raised and the record is redelivered | MSG-P7-003 | AC4, TC-E2-001-10 |
| X3 | An input of the record is stale | The entry is sealed and its inputs snapshot names the stale product with its data date; the response carries the warning | MSG-P1-001 | AC5 |
| X4 | The record names an account with no customer row | No entry is written for that account and no entry id is returned | None | AC7 |
| X5 | The record breaks the record shape | Refused by the library before it reaches the topic, naming the field | MSG-P7-009 | AC9 |
| X6 | The caller holds no Decision log right | 403; no entry is returned and nothing changes | MSG-P4-002 | AC8 |
| X7 | The entry is asked for and is absent | 404; nothing is read and nothing is recorded as a successful read | MSG-P4-003 | AC10, TC-E2-001-13 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on the store of RWB-P7-E1008-APP and the two published contracts; the hand-over record, the EFS history, the guard and the lists are contract fakes from the first run |
| Negotiable | The threshold, the hold time, the copied action codes and the lists are data rows; the story fixes the record shape, the chain rule and the fail-closed rule |
| Valuable | The hand-over of every case is provable from the central ledger, with its business date and its history, once and only once |
| Estimable | One listener, one mapper, one sealer, one notifier, one repeat counter and the two existing reads |
| Small | Within two weeks with its tests, as one slice of the legacy key |
| Testable | Each criterion in section 7 is one test in section 16, run against the fakes |

### 7. Acceptance criteria

```gherkin
Feature: EFS hand-over with full history — the rwb-decision slice

  Background:
    Given parameter "case.entry.dpd_threshold" is 90
    Given the ACE batch for ALS with business date 2026-12-14 is COMPLETED at 05:20
    Given the rwb-integration contract mock returns one hand-over record for account "A-0001", customer "C-0001", product group "MORTGAGE" and business date 2026-12-14

  Scenario: AC1 The hand-over entry is sealed in the central ledger (new, D-RCV-60)
    Given the rwb-source-data contract mock returns 14 contact rows and 2 promise rows for "A-0001" in its collection period
    When the record for "A-0001" and business date 2026-12-14 arrives on rwb.decision-record.v1
    Then one entry is stored in rwb_decision.decision_log_entry with case "RW-2026-000123", decision code "D6", final call "CASE_CREATED" and actor "SY-CASEWF"
    Then the entry holds chain_seq 1, prev_hash of 64 zeros and an entry_hash that is the SHA-256 of its canonical form
    Then GET /api/recovery/decision/v1/decision-log/{entryId} returns the same entry_hash

  Scenario: AC2 The entry carries the business date and the EFS history (new, D-RCV-60)
    Given the hand-over entry of "A-0001" was sealed
    When the entry is read with GET /api/recovery/decision/v1/decision-log/{entryId}
    Then inputs_ref names business date 2026-12-14 with the load time and status of DP01 Account and arrears and DP05 Contact and promises
    Then actions holds 16 EFS history items, each with source system "EFS", its action code and its contact time
    Then outcome names a case with status "NEW", product group "MORTGAGE" and entry date 2026-12-15

  Scenario: AC3 A repeat run adds no second entry (new, D-RCV-60)
    Given the entry for account "A-0001" and business date 2026-12-14 exists with idempotency key "A-0001:2026-12-14"
    When the same record is delivered again on rwb.decision-record.v1
    Then no second entry is stored
    Then the response returns the id of the first entry
    Then the repeat count of R-UNI-40 increases by 1

  Scenario: AC4 A failed write leaves nothing behind (new, D-RCV-60)
    Given the ledger store of rwb_decision is unavailable
    When the record for account "A-0004" is submitted
    Then the call is refused with status 503 and message MSG-P7-003
    Then no entry is stored and no chain_seq is used
    Then one incident is raised and the record is redelivered on the next attempt

  Scenario: AC5 The entry shows the freshness of its inputs (new, D-RCV-60)
    Given the ACE batch for ALS with business date 2026-12-15 is not COMPLETE by 09:00 on 2026-12-16
    When the record for business date 2026-12-15 is submitted
    Then the entry is sealed and its inputs snapshot names DP01 Account and arrears as stale from 2026-12-14
    Then the response carries MSG-P1-001 naming "DP01 Account and arrears" and 2026-12-14

  Scenario: AC6 An account linked to the open case is recorded (new, D-RCV-60)
    Given customer "C-0002" has open case "RW-2026-000210" for product group "SSME"
    Given the rwb-integration contract mock returns that account "A-0002" of "C-0002" is linked to "RW-2026-000210" with linked from 2026-12-15 and is primary false
    When the record for "A-0002" is submitted
    Then one entry is stored with final call "CASE_CREATED"
    Then its outcome names "RW-2026-000210", linked from 2026-12-15 and is primary false, and no new case

  Scenario: AC7 An account with no customer row leaves no entry (new, D-RCV-60)
    Given account "A-0003" reaches 90 days past due and the rwb-source-data contract mock returns no customer row for its person_key
    When the hand-over for business date 2026-12-14 is processed
    Then no entry is stored for "A-0003" and no entry id is returned for it
    Then the count for business date 2026-12-14 names "A-0003" in neither the sealed entries nor the repeats

  Scenario: AC8 A role without the Decision log right is refused (new, D-RCV-60)
    Given test user "U-8201" holds RW-PHONECOL, whose Decision log letter is "-"
    When "U-8201" calls GET /api/recovery/decision/v1/decision-log/{entryId}
    Then the response is 403 with message MSG-P4-002
    Then no entry is returned and the ledger is unchanged

  Scenario: AC9 A record that breaks the record shape is refused before the topic (new, D-RCV-60)
    Given the record for "A-0001" carries a field that breaks the record shape
    When the record is submitted to the library
    Then the record is refused before it reaches rwb.decision-record.v1
    Then the refusal names the field and carries MSG-P7-009

  Scenario: AC10 An entry that is absent is refused and not recorded as read (new, D-RCV-60)
    Given no decision log entry exists for the entryId requested
    When GET /api/recovery/decision/v1/decision-log/{entryId} is called for that entryId
    Then the response is 404 with message MSG-P4-003
    Then no entry is returned and no successful read is recorded

  Scenario: AC11 The ledger is written only in its own table (new, D-RCV-60)
    Given the hand-over record for "A-0001" and business date 2026-12-14 is processed
    When the entry is sealed
    Then the only table written is decision_log_entry in rwb_decision
    Then no table of another service is read or written

  Scenario: AC12 The threshold is read as the parameter in force (new, D-RCV-60)
    Given the hand-over record for "A-0001" and business date 2026-12-14 is processed
    When the threshold is applied
    Then the threshold of 90 is read from the threshold parameter (Not specified in the source documents (DOR-RWB-P7-E2001-APP-4)) with the version in force for business date 2026-12-14

  Scenario: AC13 The hand-over facts arrive on the shared topic only (new, D-RCV-60)
    Given the record for "A-0001" is published on rwb.decision-record.v1
    When the hand-over is processed
    Then the facts are taken from the message on rwb.decision-record.v1
    Then no ACE view is read and no call is made into another schema

  Scenario: AC14 No personal value is written into an event, a log or a workflow input (new, D-RCV-60)
    Given the entry for "A-0001" and business date 2026-12-14 is sealed
    When its event, its log lines and its workflow inputs are produced
    Then each carries IDs, codes, versions, dates, counts and hashes only
    Then no personal value appears in any of them

  Scenario: AC15 A call with no session is refused with 401 (new, D-RCV-60)
    Given no session accompanies the request
    When GET /api/recovery/decision/v1/decision-log/{entryId} is called
    Then the response is 401 with message Not specified in the source documents (CG-ALL-7033)
    Then no entry is returned and no successful read is recorded
```

The fifteen criteria are new, tagged `(new, D-RCV-60)`, and test only the deliverable: the sealed hand-over entry and the two reads that return it. The story line carries `acs: []`, so no legacy criterion is copied verbatim; every value is a legacy value of RWB-E2-001 or of FSD P7 v3 (90, the business dates 2026-12-14 to 2026-12-16, 14 contact and 2 promise rows, `A-0001` to `A-0004`, `C-0001` and `C-0002`, `RW-2026-000210`, `MORTGAGE` and `SSME`, the messages).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every case created or linked at hand-over carries exactly one sealed decision entry; no case exists without it | Principle 5; R-UNI-39; CTL-06; FEAT-DRI-02 |
| BR2 | The entry names the ACE business date in its inputs snapshot, so the case is reproducible from the date it was built on | Legacy AC1; FEAT-DRI-03 |
| BR3 | The entry carries the EFS contact and promise history the hand-over read, with the source system of each item | Legacy BR5; DL29; FEAT-ILG-06 |
| BR4 | No case is created from a business date whose ACE batch is not COMPLETE, and an entry that is sealed from a stale input says so in its snapshot and carries the warning | Legacy BR4; MSG-P1-001 |
| BR5 | One case per customer and product group; a further account is linked to the open case and the entry records the link, not a second creation | DL17; REQ-CHO-005 |
| BR6 | A record seen twice for the same account and business date is stored once and the repeat is counted under R-UNI-40 | Legacy BR6; R-UNI-40; GAP-2463; ASM-4092 |
| BR7 | A record that cannot be sealed does not proceed: nothing is stored, the caller is refused and an incident is raised | Legacy BR7; R-UNI-39; MSG-P7-003 |
| BR8 | An account whose person_key has no customer row is not taken and leaves no entry; it stays on the REC-05 break | Legacy BR8; REC-05; DQ-040 |
| BR9 | The ledger is `decision_log_entry` in `rwb_decision` and it is P7's: this story writes and reads that table only, and no other service's table is read or written | Architecture v5 slides 14 and 41; DP-01 |
| BR10 | The threshold, the hold time, the lists and the copied action codes are parameters and reference rows read with the version in force; the decision code of the hand-over entry is a row of LOV-DECISION read as data | DP-06; DP-07; DL16; DL29 |
| BR11 | The hand-over facts arrive on the shared decision-record topic, never as a read of an ACE view and never as a call into another schema | DP-03; DP-05; ADR-022 |
| BR12 | The entry carries IDs, codes, versions, dates, counts and hashes; no personal value is written into an event, a log or a workflow input | NFR-039; NFR-040; Template and Rules §R7.2 s17 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| No entry | `DecisionRecorded` consumed for one account and business date | The record shape passes and the account has a customer row | Sealed, `chain_seq` n+1 |
| Sealed | The same record delivered again | The idempotency key is already stored | Sealed, unchanged, repeat counted |
| Sealed | The chain check runs | `entry_hash` matches the canonical form and `prev_hash` matches the entry before it | Sealed, verified |
| Sealed | An append fails, or an update or a delete is attempted | The store is unavailable, or the statement touches a stored entry | Unchanged; refusal and incident |

The entry has no other state: it is append only, it is never corrected in place, and a correction is a new entry naming the one it corrects (DF-DEC-029).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The hand-over run of `rwb-integration` with SY-DECLOG | Submits one record per account and business date (Decision log, C) |
| SY-CASEWF, case workflow module | Is the actor of the entry, and names the case or the link (Decision log, C) |
| `rwb-decision` service identity | Consumes the topic, seals the entry in `rwb_decision` and serves the two reads (Decision log, C, R) |
| RW-CASEOWN, case owner | Reads the entry of a case in scope once allocated (Decision log, R) |
| RW-DATASTEW, data steward | Reads the entries of a business date on the REC-05 break (Decision log, R) |
| RW-COE, RW-AUDIT and RW-COMPLY | Read entries with the Decision log right R (Decision log, R) |
| RW-PHONECOL and roles without the right | Refused with MSG-P4-002 |

The letters are the legacy letters of RWB-E2-001 section 10 and the matrix of TSD P7 T6.1, unchanged. No role name and no right is written in code.

### 11. Data

| BR Field ID | Entity in `rwb_decision` | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 | decision_log_entry | id | Write |
| DF-DEC-002 | decision_log_entry | case_id | Write (the created case or the open case an account was linked to) |
| DF-DEC-003 | decision_log_entry | decision_code | Write (D6) |
| DF-DEC-004, DF-DEC-005 | decision_log_entry | rule_id, rule_version | Write (the entry rule in force, as the record carries it) |
| DF-DEC-006, DF-DEC-007, DF-DEC-009, DF-DEC-010, DF-DEC-011, DF-DEC-013, DF-DEC-029 | decision_log_entry | model_version, agent_version, recommendation, approver_user_id, approval_level, override_reason, corrects_entry_id | Not written: no model, no agent, no recommendation, no approver and no correction at the hand-over |
| DF-DEC-008 | decision_log_entry | inputs_ref | Write (business date D and the stamp of each input) |
| DF-DEC-012 | decision_log_entry | final_call | Write (`CASE_CREATED`) |
| DF-DEC-014 | decision_log_entry | actions | Write (the EFS history items the hand-over carried) |
| DF-DEC-015 | decision_log_entry | outcome | Write (created, or linked to an open case) |
| DF-DEC-016 | decision_log_entry | decided_at | Write |
| DF-DEC-017, DF-DEC-018, DF-DEC-028 | decision_log_entry | prev_hash, entry_hash, chain_seq | Write (the chain link) |
| DF-DEC-030 | decision_log_entry | actor_user_id | Write (`SY-CASEWF`) |
| DF-DEC-031 | decision_log_entry | idempotency_key | Write (account and business date) |
| DF-ACE-108, DF-ACE-111, DF-ACE-114, DF-ACE-119, DF-ACE-122, DF-ACE-123 | v_ace_efs_action, through the record payload | efs_record_key, action_code, contact_at, is_ptp, promise_date, promise_amount | Write inside `actions`, carried by the caller; the view is never read here (DP-05) |
| DF-OPS-178 to DF-OPS-183 | processed_event, outbox_event, idempotency_key in `rwb_decision` | all fields | Write, through the inbox and outbox library (DP-09) |

The inner shape of `actions` and `outcome` is Not specified in the source documents (GAP-2462; ASM-4091), and so is the exact LOV-DECISION value behind the decision code D6 that the legacy story names (GAP-2467; ASM-4096); the story writes the history items and the created-or-linked result and asserts counts, source system and action codes only. Field IDs are those in the Logical Data Model and Data Dictionary, and TSD P7 T3.1 types.

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-decision` (P7); base `/api/recovery/decision/v1`. The shapes are those fixed in RWB-P7-E2005-CON; this story adds no path.

| ID | Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|---|
| API-P7-006 | GET | `/decision-log` | The hand-over entries of a case or of a business date, paged | Decision log, right R | Read only |
| API-P7-007 | GET | `/decision-log/{entryId}` | One hand-over entry with its inputs snapshot, its history items and its chain verdict | Decision log, right R | Read only |

Request: the query parameters fixed in RWB-P7-E2005-CON — case, decision, rule, approver, `from`, `to`, `page` and `size` (GAP-2464; ASM-4093). Answer: `DecisionLogPage` and `DecisionLogEntry` as fixed there. Errors: 401 no session (Not specified in the source documents (CG-ALL-7033)); 403 the role lacks the right (MSG-P4-002); 404 the entry is absent (MSG-P4-003); 503 the store does not answer (MSG-GEN-006).

#### 12.2 REST operations consumed

| Method and path | Owner | Contract | Use in this story |
|---|---|---|---|
| POST `/api/recovery/access/v1/authorise` | P4 rwb-access | RWB-P4-E1037-CON through the guard library RWB-PLT-E1037-CON; faked | The Decision log right R of the caller of either read. The guard is the platform pattern DP-08, which the story line does not list (GAP-2468; ASM-4097) |
| GET `/api/recovery/case/v1/admin/parameters/{code}` | P3 rwb-case | RWB-P3-E1042-CON through RWB-PLT-E1042-CON; faked | `case.entry.dpd_threshold` and `handover.hold_until`, used to check the record of the business date (DP-06) |
| GET `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | RWB-P3-E1043-CON through RWB-PLT-E1043-CON; faked | LOV-DECISION, LOV-PRODUCT and the EFS action codes of `efs_ledger_outcome` (DP-07) |

Every row is one hop with a 2 s timeout and a breaker per downstream (DP-11, ADR-020). The hand-over record itself is not a consumed operation: it arrives on the shared topic (section 12.4).

#### 12.3 Events published

None. This story seals a record and serves it; it publishes no business fact of its own, and `rwb.decision.events.v1` stays empty here. `DecisionRecorded` (EV-08) is a type P7 owns and each of the 19 services publishes for its own records (Ownership Map EV-08 row), so the hand-over record is published by `rwb-integration` through RWB-PLT-E1027-CON and never republished here, and no loop is created.

#### 12.4 Events consumed

| Event | Topic | Key | Payload (IDs and facts only) | Handling | Owner (producing service) |
|---|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` (shared) | The local entry id, with the case id and the business date as the idempotency key of this story | entryId, caseId, decisionCode, approver, the entry rule and version, the business date, the inputs snapshot reference, the EFS history items, the created-or-linked outcome | Consumed with the inbox; one entry sealed per idempotency key; five-minute target (GAP-2465; ASM-4094) | Not specified in the source documents (DOR-RWB-P7-E2001-APP-24) |

#### 12.5 Workflows and activities

None. The ingest is a Kafka listener in the api deployment of `rwb-decision`; it has no wait, no human step and no durable timer, so no workflow and no activity is declared, and DP-10 is applied only by not claiming it (section 13).

#### 12.6 Schedules

None. JOB-13 is a continuous Kafka ingest and not a Schedule, and the chain check of JOB-14 at 02:00 and the daily WORM seal belong to RWB-P7-E1008-APP (section 19). This story registers no cron entry and no job name.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| decision_log_entry | P7 (`rwb_decision`) | INSERT and SELECT here: the sealed hand-over entry of BR1 to BR8; no column, key or trigger is changed |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_decision` | The inbox of the consumed record and the outbox of the library (DP-09) |

Not owned and not declared: `recovery_case`, `case_account` and `interaction` are `rwb-case`'s and `rwb-source-data`'s, `rule_package` and `approval` are P7's own but belong to RWB-P7-E1073-APP and RWB-P7-E2013-APP, and `parameter_*`, `reference_*`, `lov_value` and `efs_ledger_outcome` are `rwb-case`'s. No foreign key crosses a service boundary (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Documented answers used by this story |
|---|---|---|
| rwb-integration hand-over fake (RWB-P2-E2001-CON) | The record of each account and business date | "A-0001" created for "RW-2026-000123"; "A-0002" linked to "RW-2026-000210"; "A-0004" for the failure path; the same record delivered twice; a record with a missing field, refused with MSG-P7-009 |
| rwb-source-data EFS history fake | The 14 contact rows and 2 promise rows of a collection period, and an absent customer row | The history of "A-0001"; no customer row for "A-0003" |
| Decision-record library fake (RWB-PLT-E1027-CON) | The local write, the outbox and the topic | A sealed write with the local entry id; the stale-input warning; a failed store |
| rwb-access authorise fake (RWB-P4-E1037-CON) | The right and the scope of either read | RW-CASEOWN and RW-COE allowed; RW-PHONECOL refused with MSG-P4-002 |
| rwb-case parameter and reference fakes (RWB-P3-E1042-CON, RWB-P3-E1043-CON) | The threshold, the hold time and the three lists | 90 and 09:00 as rows; LOV-DECISION, LOV-PRODUCT and the EFS action codes |
| Ledger fixture (RWB-P7-E1008-APP baseline) | `decision_log_entry` and the canonical form | An empty ledger for the first entry; a head at `chain_seq` n for the chain link; one entry changed with the trigger disabled |

The fakes are derived from the published contracts and the legacy values of section 16, so a component and a contract test read the same fixtures.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | API-P7-006 and API-P7-007 provided; the guard, the parameter and the reference reads consumed; one hop, 2 s |
| Kafka | 0 published, 1 consumed | `DecisionRecorded` (EV-08) on `rwb.decision-record.v1`, through the inbox |
| Temporal | None | No workflow, no activity and no Schedule |
| File | None | No file is read or written: the hand-over arrives from the ACE views through `rwb-source-data` |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, modules `handover` and `ledger`, Java packages `th.co.scb.ace.workbench.recovery.decision.handover` and `...decision.ledger`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_decision`; never read another service's tables | none |
| DP03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP05 | AceSourceQuery, `v_ace_*` | The EFS history arrives on the record from `rwb-source-data`; no view is read here | none |
| DP06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP09 | Application event, EV-nn, outbox | Outbox and inbox library; the owner's topic; CloudEvents | H RWB-PLT-TE006-CON |
| DP10 | Quartz, JOB-nn | No Quartz remains in this path: JOB-02 is an event-started workflow of `rwb-integration`, and this ingest is a listener | H RWB-PLT-E1071-CON (named, not claimed) |
| DP11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (the C row RWB-P2-E2001-CON comes from the legacy dependency) |
| DP18 | Interaction ledger | The ledger is `rwb-source-data`'s; this story records the history items on the entry and writes no ledger row | none (GAP-2466; ASM-4095) |
| DP19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The story line carries no H row, so the six platform H rows above are named here and in section 3, 12.2 and 12.8 and carried as one gap and one assumption (GAP-2468; ASM-4097). DP-02, DP-04, DP-12 to DP-17 and DP-20 are not claimed; DP-08 is used as the platform guard of the two reads (section 12.2) and is not built here.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DecisionRecordListener | Listener | Consumes EV-08 on `rwb.decision-record.v1` through the inbox and the idempotency key |
| DecisionRecordMapper | Service | Maps the record to one `decision_log_entry` row: code, final call, actor, inputs snapshot, actions, outcome |
| ChainSealer | Service | Reads the head, assigns `chain_seq` and `prev_hash`, computes `entry_hash` and inserts in one transaction |
| EntryWriteGuard | Service | Refuses the write when the store or the shape fails, and leaves nothing behind |
| RepeatCounter | Service | Records the R-UNI-40 repeat per account and business date |
| HandoverNotifier | Service | Raises the incident of a failed write and the stale-input warning |
| DecisionLogController | Controller | The two reads, with the problem mapping for 401, 403, 404 and 503 |

**Database and migrations.** No new table and no migration: this story inserts into `decision_log_entry` and the library tables that RWB-P7-E1008-APP and the service template already create in `rwb_decision` (DP-15 applies to the service, not to this story).

**Configuration and reference data.** `case.entry.dpd_threshold` = 90 (DL16) and `handover.hold_until` = 09:00 read as parameters; LOV-DECISION, LOV-PRODUCT and the `efs_ledger_outcome` action codes read as reference rows (DL29). The feature switch `rwb.decision.efs-handover` is a parameter; off, the listener stops consuming and no entry is sealed.

**Build steps**

1. DecisionRecordListener and the inbox, with the idempotency key of the account and the business date; tests for AC3.
2. DecisionRecordMapper against the record shape of RWB-PLT-E1027-CON; tests for AC1, AC2 and AC6.
3. ChainSealer, the canonical form and the head read; tests for AC1 and the boundary at `chain_seq` 1.
4. EntryWriteGuard and HandoverNotifier on the fail-closed path; tests for AC4 and TC-E2-001-10.
5. The stale-input stamp in `inputs_ref` and the warning; tests for AC5.
6. The absent-customer path with the REC-05 break, which is `rwb-source-data`'s and is faked; test for AC7.
7. The guard on the two reads and the 403 path; test for AC8.

**Done when.** The tests of section 16 pass, the contract tests of RWB-P7-E2005-CON stay green, and no case exists in SIT for business date 2026-12-14 without its entry.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The entry cannot be sealed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | An input of the record is stale | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | The caller holds no Decision log right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The entry is absent | This case is not in your scope. |
| MSG-P7-009 | The record breaks the record shape (X5) | Text fixed in RWB-PLT-E1027-CON |
| MSG-GEN-006 | Not specified in the source documents (DOR-RWB-P7-E2001-APP-9) | Not specified in the source documents (DOR-RWB-P7-E2001-APP-9) |

MSG-P7-003, MSG-P1-001 and MSG-P4-002 are copied unchanged from RWB-E2-001 section 14, and MSG-P4-003 is the access message of its section 12. Thai text follows DL10. MSG-P7-009 of X5 is the library's refusal and its text is fixed in RWB-PLT-E1027-CON.

### 15. Screens and states

No new screen. The hand-over entry is read on SCR-38 Decision log query through the gateway-bff composite route (DP-19), and the field list, the masking and the timeout of the route belong to RWB-PLT-N001-CON. The case owner sees the history on SCR-04 Case timeline, which is `rwb-source-data`'s read of the ledger and not this story.

| Screen | State | What the user does |
|---|---|---|
| SCR-38 Decision log query | Results | Reads the hand-over entries with case, decision, rule and version, final call and decided at |
| SCR-38 Decision log query | Empty | Sees a sentence saying no entry matches the filters |
| SCR-38 Decision log query | Refused | Sees MSG-P4-002 when the role lacks the right |
| SCR-38 Decision log query | Loading | Not specified in the source documents (CG-ALL-7039) |
| SCR-38 Decision log query | Error | Not specified in the source documents (CG-ALL-7039) |
| SCR-38 Decision log query | No access | Not specified in the source documents (CG-ALL-7039) |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-001-01 | AC1, AC2, BR1, BR3, BR5 | Component | Account A-0001 with 14 contact rows and 2 promise rows in the history fake |
| TC-E2-001-02 | AC2, BR6 | Component | The same record for the same account and business date delivered twice |
| TC-E2-001-03 | AC3, BR4 | Contract | Stale DP01 and DP05 stamps for business date 2026-12-15 |
| TC-E2-001-04 | AC4, BR2 | Component | Customer C-0002 with open SSME case RW-2026-000210 |
| TC-E2-001-05 | AC5, BR8 | Component | Account A-0003 with no customer row in the fake |
| TC-E2-001-06 | AC6, BR4 | Contract | Records for 2026-12-15 and 2026-12-16 after a missed day |
| TC-E2-001-07 | AC7, BR7 | Component | The ledger store stopped |
| TC-E2-001-08 | AC8, BR6 | Contract | A run in flight and the same record delivered again |
| TC-E2-001-09 | AC8 | Contract | Test user U-8201 with RW-PHONECOL, refused with MSG-P4-002 |
| TC-E2-001-10 | AC4, BR7 | NFR | The write forced to fail over 50 synthetic records; no entry without a case |
| TC-E2-001-11 | §12.7, BR9 | Contract | Write and read attempts on decision_log_entry and on each table not owned in §12.7 |
| TC-E2-001-12 | AC9, X5 | Contract | A record that breaks the record shape, submitted to the library |
| TC-E2-001-13 | AC10, X7 | Component | Entry id requested that is absent from the ledger |
| TC-E2-001-14 | AC11, BR9 | Component | Hand-over of A-0001 for 2026-12-14 with the ledger writes observed |
| TC-E2-001-15 | AC12, BR10 | Contract | Threshold parameter with the version in force for 2026-12-14 |
| TC-E2-001-16 | AC13, BR11 | Contract | Record published on rwb.decision-record.v1 with no ACE view reachable |
| TC-E2-001-17 | AC14, BR12 | Contract | Sealed entry with its event, log lines and workflow inputs captured |
| TC-E2-001-18 | AC15, §12.1 | Contract | Call to API-P7-007 with no session |

The ten legacy test case IDs of RWB-E2-001 are kept in their legacy order, with the Level column of §R7.2; TC-E2-001-11 to TC-E2-001-18 are added (new, D-RCV-60) for the boundary of §12.7 and the criteria and rules that had no test case. The full Given, When and Then of TC-E2-001-01 to TC-E2-001-10 is in Recovery Workbench Test Cases, tab Story test cases, under the same ID; TC-E2-001-11 to TC-E2-001-18 are to be added to that tab. Until the element lists of the actions and outcome columns are fixed in RWB-P7-E2005-CON, TC-E2-001-01 and TC-E2-001-14 assert the counts, the source system and the action codes only. Until RWB-P3-E1043-CON is published, the product group tests run on the map fixture, and an unmapped product code is answered as unresolved.

### 17. Guardrails

- No business value in code: the 90, the 09:00, the lists and the copied action codes are parameters and reference rows.
- No personal data in events, workflow inputs, logs or tests: the record carries keys, codes, dates, counts and hashes, and the synthetic keys of section 16.
- ACE data only through the owner's contract or `v_ace_*` views: this service reads no ACE view and no `recovery.*` table (DP-01, DP-05).
- No case without its entry: the write is fail-closed, and a failed write raises an incident instead of a silent gap (BR7, R-UNI-39, NFR-077).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-013 | Hand-over arrives in the daily ALS batch | Program 5.2; Epic 2 3.2 | FEAT-CHO-01 | 6.1 Take over the case at 90 days past due | R-UNI-40 | TC-E2-001-01, TC-E2-001-02, TC-E2-001-03 |
| REQ-CHO-001 | Case with full contact and promise history | Program 5.3; Epic 2 3.2 | FEAT-CHO-01 | 6.1 Take over the case at 90 days past due | None | TC-E2-001-01, TC-E2-001-04, TC-E2-001-05 |
| REQ-CHO-005 | Workbench is the system of record for case state after hand-over | Program 5.3; Epic 2 3.2 | FEAT-CHO-04 | 6.1 Take over the case at 90 days past due | R-UNI-39 | TC-E2-001-01 |
| REQ-RDF-003 | EFS history transfers to the case | Program 5.1; Epic 2 3.2 | FEAT-CHO-05 | 6.1 Take over the case at 90 days past due | None | TC-E2-001-01, TC-E2-001-07 |

### 19. Out of scope

- The hand-over run, JOB-02, the run summary, the REC-01 result and the rerun refusal: RWB-P2-E2001-APP and RWB-P2-E2001-CON.
- The case, the account link and CaseCreated (EV-01): RWB-P3-E2001-APP.
- The ACE views `v_ace_account`, `v_ace_customer` and `v_ace_efs_action` and the append to the interaction ledger: `rwb-source-data` (DP-05, DP-18).
- The ledger store, the canonical form, the append-only trigger, the JOB-14 chain check and the WORM seal: RWB-P7-E1008-APP; the local writer and the outbox relay: RWB-P7-E1027-APP and RWB-PLT-E1027-CON.
- Allocation of the new case: RWB-P7-E1020-APP. The daily reconciliation against open cases and the REC-01 break list: RWB-E1-011. A same-day hand-over event: DL06.
