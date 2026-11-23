# RWB-P7-E1030-APP Daily rebalancing and queue measures

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E1030-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-030 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP17, DP19 |
| Parallel lane | L-P7-J |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E1030-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to REQ-CWC-015, REQ-RDF-012) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the rwb-decision slice of the daily rebalance, split from RWB-E1-030, so that every move the morning run makes is held once in the central ledger with its reason and the assignment rule and version, the count of the business date is reconciled to the moves the run reports, and the copy of the ledger to the data lake is removed under DP-17. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **team manager (RW-TEAMMGR), a data steward (RW-DATASTEW) and rwb-decision itself**, I want **every move of the morning rebalance held once in the central ledger as an append-only entry whose final call and actions payload explain it, a count of the entries of the business date compared with the moves the run reports, and no copy of the ledger in a data lake and no file**, so that **an assignment made only to bring a queue back inside its cap can be explained to an auditor from one place, a move that is missing from the ledger is found the same morning as a break for the data steward, and the ledger has exactly one home**.

Inside `rwb-decision` this is the rebalance record of the central ledger:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1`, the shared topic `rwb.decision-record.v1` for DecisionRecorded (EV-08), Temporal task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`.
- It consumes DecisionRecorded on `rwb.decision-record.v1` idempotently into `decision_log_entry`. One entry per move: final call "CASE_TRANSFERRED" for a case moved off an owner above the cap, final call "OWNER_ASSIGNED" for an unassigned case given an owner. The `actions` payload carries the assignment reason "REBALANCE", the assignment rule ID and rule version taken from the queue's ASSIGNMENT row, and the queue and owner identifiers only.
- The reconciliation read is `GET /api/recovery/decision/v1/decision-log?decision=...&from=...&to=...`. It counts the entries of the business date, and the count is compared with the moves the run reports on its record, read through the rwb-case contract of RWB-P3-E1030-CON. A difference of one holds the report and lists the case for the data steward.
- Append only and chained: an entry is never updated or deleted, a re-hashed or edited entry is refused, the page answers MSG-P7-012 for an entry that fails the chain, and an unreadable ledger store blocks the caller with MSG-P7-003 (principle 5).
- No data lake (DP-17): JOB-15's copy of the log to the lake and the INT-19 and INT-20 outbound batch are removed. DecisionRecorded on `rwb.decision-record.v1` is what rwb-reporting projects from. This story writes no file and reaches no outside system.

The legacy facts are unchanged: every move is logged before it takes effect and the log is append only and hash chained (legacy BR7, principle 5, R-UNI-39); a move keeps the case status and the clocks (R-UNI-18); an owner exactly at the cap loses no case, and a queue with no cap moves nothing (legacy AC5, AC10).

### 2. Business rationale

Queues are balanced by a morning run that assigns cases left without an owner and takes owners above the caseload cap back inside it (R-UNI-19). Each of those moves is a decision about a customer: a case changes hands because the queue is over its cap, not because the case itself changed. If the move is not recorded, or is recorded without the reason and the rule that produced it, the customer's history shows a case that changed owner for no visible cause, and an auditor has to reconstruct the morning run from a job log.

Legacy RWB-E1-030 answered this with a decision log entry per move and one measure snapshot per queue. In the target the case and workflow service makes the moves and this service holds the ledger, so the promise splits in two: rwb-case records why the run moved a case, and rwb-decision keeps that record in the one append-only, hash-chained ledger that audit reads. This story keeps the second half of that promise:

1. Every move is in the ledger once, with its final call, its reason and the assignment rule ID and version that produced it. A rebalancing decision that cannot be told apart from an ordinary allocation is not an auditable decision.
2. The count is checked, not assumed. The entries of the business date are counted and compared with the moves the run reports, once, and a difference of one is a break for the data steward rather than a rounding note.
3. One home for the ledger and no copy. There is no data lake in Arch v5 (DP-17): JOB-15's copy to the lake and the INT-19 and INT-20 batch are removed, and rwb-reporting builds its measures from events into its own projections (JOB-15 at 01:30 reads that projection, not a lake).

This story is the rwb-decision part of legacy RWB-E1-030. The rebalancing selection, the cap, the hold checks, the owner choice, the queue measure snapshot and the run record stay with rwb-case (RWB-P3-E1030-APP); the Power BI report and the queue, ageing and breach measures stay with rwb-reporting; the store, the writer and the rule authoring are the other P7 stories named in section 19. This slice delivers the rebalance mapping into the ledger and the reconciliation read, nothing else. It meets REQ-CWC-015 and REQ-RDF-012 and supports REC-01 (the counts reconcile) and principle 5 (no action proceeds unlogged).

### 3. Preconditions

- RWB-P3-E1030-CON is published: the rwb-case contract with the rebalancing run record of a business date and the case read, the error envelope and its fake (DP-11). The run record's operation, its request and the fields that carry the move count and the case IDs are Not specified in the source documents (GAP-1326; ASM-2339).
- The `rwb_decision` baseline is in place from the service-template work: schema `rwb_decision`, the per-service login, the base `/api/recovery/decision/v1`, the topics `rwb.decision.events.v1` and `rwb.decision-record.v1`, the task queue `rwb-decision`, the deployment chart and the inbox with its processed-id record (DP-09), so a repeated DecisionRecorded is recognised by case and business date.
- The decision-record library and the DecisionRecorded payload are platform work (RWB-PLT-E1027-CON, DP-03) and are in the baseline; this slice consumes the payload and adds no build dependency of its own.
- The `decision_log_entry` table, its append-only trigger, its hash chain and its chain verification are in place in this schema (RWB-P7-E1008-APP, named in section 19); this story adds the rebalance mapping, the idempotency key and the count, not the store.
- The queue, its method and cap, the owners and their open case counts, the run and the moves it reports are rwb-case's (RWB-P3-E1030-APP); the tests read all of them through the contract mock, and no business value is configured here.
- The synthetic facts the tests use: queue `TDR-BKK-CO` with method `LOWEST_LOAD` and cap 150; owners `U-61` with 140 and `U-62` with 144 open cases; 12 cases with no owner; business date 2026-12-02; the snapshot taken at 06:52; owner `U-63` with 153 open cases; queue `WO-BKK-CO` with no cap; case `RW-2026-000501` (legacy story AC1, AC2, AC5, AC6, AC10).
- Readers hold Decision log R and the producing services hold Decision log C in the capability area (TSD P7 T6.1); the authorisation decision itself is the cached permission decision the service template holds from rwb-access, and this story adds no guard of its own.

### 4. Flow

1. rwb-case runs the morning rebalance for the business date 2026-12-02 (Temporal Schedule 06:30, JOB-06, in the owning service) and, for each case it moves, writes its local decision record and the outbox row of DecisionRecorded in the same transaction. A move whose record cannot be written does not happen, and the run record lists the case with MSG-P7-003 (legacy AC6, principle 5).
2. DecisionRecorded arrives on `rwb.decision-record.v1` (EV-08). The payload carries the case ID, the business date, the queue ID, the owner before and after the move, the reason "REBALANCE" and the rule ID and rule version of the queue's ASSIGNMENT row.
3. rwb-decision: `DecisionRecordedListener` recognises the record by case and business date in the inbox (DP-09). A record already processed is answered with the first entry's ID and counted as a repeat (R-UNI-40); nothing is appended.
4. rwb-decision: a record that carries a move is mapped to one entry. Final call "CASE_TRANSFERRED" when the case left an owner above the cap, "OWNER_ASSIGNED" when a case with no owner was given one. A record that carries no move writes no entry.
5. rwb-decision: `RebalanceEntryWriter` writes the entry with `decision_code`, `case_id`, `rule_id`, `rule_version`, `inputs_ref`, `final_call`, `decided_at`, `actor_user_id`, the `actions` payload (reason "REBALANCE", queue and owner identifiers and the rule ID and version), the idempotency key of case and business date, and `chain_seq`, `prev_hash` and `entry_hash` from the chain. Nothing of the case is copied: no status, no stage, no amount, no party.
6. rwb-decision: the entry is appended, never updated. The append-only trigger refuses an update, a delete and a re-hash of any entry, and the attempt is audited (legacy BR7).
7. The reconciliation read: `LedgerReconciliationReader` counts the entries of the business date through `GET /decision-log` with `decision`, `from` and `to`, and reads the moves the run reports through the rwb-case contract, one hop within 2 s (DP-11).
8. rwb-decision: the two counts are compared. When they are equal the reconciliation for the business date passes and the count is released to the reader. When they differ the reconciliation is held, and the case of the missing move is listed on the reconciliation break list for the data steward (RW-DATASTEW) with the business date. The entry is appended before the count is taken, and a count read while the consumer is still behind is a held reconciliation, not a passing one.
9. rwb-decision: the ledger store cannot be read at the moment of the count. The read is refused with 503 and MSG-P7-003, and no count of zero and no release is produced from a failed read (principle 5).
10. rwb-reporting builds its measures and its queue, ageing and breach report from DecisionRecorded and the other events into its own projections; no file leaves this service and nothing is copied to a data lake (DP-17).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The DecisionRecorded of the same case and business date arrives twice | One entry; the repeat answers the first entry's ID and adds one to the repeat count; no second `chain_seq` | None | AC3 |
| X2 | A record carries no move, for example a queue with no cap | No entry is appended and the count is unchanged; the run record reports the queue with zero moves | None | AC4 |
| X3 | The count of the business date differs from the moves of the run by one | The reconciliation for the business date is held, the case of the missing move is listed for the data steward, and no count is released | The break message, whose ID is Not specified in the source documents (GAP-1326; ASM-2339) | AC6 |
| X4 | An entry fails the chain, or an update, a delete or a re-hash is attempted | The entry is returned flagged, never hidden, and the attempt is refused; one incident goes to the Compliance queue | MSG-P7-012 | AC7 |
| X5 | The ledger store cannot be read when the count is taken | 503; no count, no zero and no release; the reader retries | MSG-P7-003 | AC7 |
| X6 | The rwb-case run record does not answer inside the 2 s budget | One hop, 2 s (DP-11); the reconciliation is held for the business date and no count is released from a partial answer | MSG-P7-003 | TC-E1-030-12 |
| X7 | The caller's role holds no Decision log R | 403; no entry, no count and no case ID is returned | MSG-P4-002 | TC-E1-030-11 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published rwb-case contract and its fake (RWB-P3-E1030-CON) and the decision-record library; it calls no other service at run time and holds no Quartz job |
| Negotiable | Nothing business is fixed here: the queue, the cap, the method, the owners and the moves are rwb-case's values, read through the contract |
| Valuable | Every rebalance move in the ledger once with its reason and rule, a count that is reconciled to the run, and no second copy of the ledger |
| Estimable | One inbox consumer, one mapping, one append, one count read, one comparison |
| Small | Fits one sprint with its tests, as a secondary slice of the legacy key |
| Testable | Every criterion in section 7 is one automated test against the contract fake and the synthetic values of the legacy story |

### 7. Acceptance criteria

```gherkin
Feature: Daily rebalancing and queue measures - the rebalance record of rwb-decision

  Background:
    Given queue "TDR-BKK-CO" uses "LOWEST_LOAD" with cap 150
    Given the business date is 2026-12-02

  Scenario: AC1 Every move of the run is in the ledger once with its reason and its rule (new, D-RCV-60)
    Given the rwb-case contract mock returns 12 cases with no owner in queue "TDR-BKK-CO", owners U-61 with 140 and U-62 with 144 open cases, and a run for 2026-12-02 that reports 12 moves with reason "REBALANCE"
    Given the queue's ASSIGNMENT row in force carries a rule ID and a rule version, whose values are Not specified in the source documents (GAP-1326; ASM-2339)
    When the 12 DecisionRecorded events of the run arrive on topic "rwb.decision-record.v1"
    Then 12 entries exist in decision_log_entry for business date 2026-12-02
    Then every entry has final call "OWNER_ASSIGNED", 8 carry owner U-61 and 4 carry owner U-62
    Then every entry's actions payload carries reason "REBALANCE", the rule ID and rule version of the ASSIGNMENT row, queue "TDR-BKK-CO" and the owner identifier
    Then no entry holds a case status, a stage, an amount or a party attribute, no name, address or identity number is written, and every entry carries chain_seq, prev_hash and entry_hash from the chain

  Scenario: AC2 A case moved off an over-cap owner is recorded as transferred and explains itself (new, D-RCV-60)
    Given the rwb-case contract mock returns owner U-63 with 153 open cases in queue "TDR-BKK-CO"
    Given the rwb-case contract mock returns a run for 2026-12-02 in which 2 of the 3 newest cases move off U-63 with reason "REBALANCE" and the third stays with "MSG-P7-003" on the run record
    When the 2 DecisionRecorded events for those cases arrive on topic "rwb.decision-record.v1"
    Then 2 entries exist with final call "CASE_TRANSFERRED" and each names the queue "TDR-BKK-CO" and the owner it left and the owner it went to
    Then the case that stayed with U-63 has no entry for 2026-12-02, because the run recorded no move for it, and the 2 entries and the count of the business date name no reason other than "REBALANCE"

  Scenario: AC3 A repeated event gives one entry and answers the first entry ID (new, D-RCV-60)
    Given case "RW-2026-000501" was moved off owner U-63 on business date 2026-12-02 and its entry exists with an entry ID and chain_seq 230
    When the same DecisionRecorded event arrives again for case "RW-2026-000501" and business date 2026-12-02
    Then one entry exists for that case and business date
    Then the consumer answers the first entry's ID and adds one to the repeat count for R-UNI-40
    Then no second entry, no new chain_seq and no second entry_hash is written

  Scenario: AC4 A queue with no cap moves nothing and records nothing (new, D-RCV-60)
    Given the rwb-case contract mock returns queue "WO-BKK-CO" with no capacity cap
    Given the rwb-case contract mock returns a run for 2026-12-02 that reports no move in "WO-BKK-CO"
    When the run's DecisionRecorded events arrive on topic "rwb.decision-record.v1"
    Then no entry of business date 2026-12-02 names a case of "WO-BKK-CO"
    Then the count of the business date is unchanged by the queue and the run reports 0 moves for it

  Scenario: AC5 The count of the business date reconciles to the moves of the run (new, D-RCV-60)
    Given the rwb-case contract mock returns a run for 2026-12-02 that reports 12 moves, and the snapshot at 2026-12-02 06:52
    Given 12 entries exist for business date 2026-12-02, 10 with final call "OWNER_ASSIGNED" and 2 with "CASE_TRANSFERRED"
    When the reader calls GET /api/recovery/decision/v1/decision-log with the decision of each final call and from and to of 2026-12-02
    Then the two totals add to 12 and the totals are read from decision_log_entry only
    Then the count equals the 12 moves the run reports, the difference is 0 and nothing is listed
    Then the reconciliation for 2026-12-02 passes and the count is released to the reader

  Scenario: AC6 A difference of one holds the report and lists the case (new, D-RCV-60)
    Given the rwb-case contract mock returns a run for 2026-12-02 that reports 12 moves, including case "RW-2026-000501"
    Given the ledger holds 11 entries for business date 2026-12-02
    When the count is compared with the moves of the run
    Then the difference is 1 and the reconciliation for 2026-12-02 is held
    Then case "RW-2026-000501" of the missing move is listed for the data steward RW-DATASTEW with the business date 2026-12-02
    Then no count is released for 2026-12-02, no report is produced from the held reconciliation, and the break carries the message whose ID is Not specified in the source documents (GAP-1326; ASM-2339)

  Scenario: AC7 The ledger is append only, a broken chain is answered and an unreadable store blocks the caller (new, D-RCV-60)
    Given an entry for case "RW-2026-000501" on business date 2026-12-02 with chain_seq 230, its prev_hash and its entry_hash
    When an UPDATE of its final call and a DELETE of the entry are attempted through the rwb-decision login
    Then both statements are refused, the entry is unchanged and its entry_hash still matches its canonical form
    When the entry is re-hashed and edited and the page is read
    Then the page answers MSG-P7-012 naming entry 230 and the entry is returned flagged, never hidden
    When the ledger store cannot be read at the moment the count is taken
    Then the read answers 503 with MSG-P7-003 and releases no count and no zero
```

The seven criteria above are new and test only this deliverable: the rebalance mapping of the central ledger, the count of the business date and its comparison with the run, and the removal of the lake copy. The legacy criteria of RWB-E1-030 are owned elsewhere: AC1, AC2, AC4, AC5, AC9 and AC10 of the legacy story are held by rwb-case (RWB-P3-E1030-APP), and AC7 with them for the run; AC3's alert is rwb-case's and its measure rwb-reporting's; AC6 and AC8 are rwb-case's run record and hold checks, and this story holds their consequence, the absent entry. The legacy test cases this story answers are listed in section 16.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every move of the rebalance is held once in the central ledger: one `decision_log_entry` per move of the case and business date, written from the DecisionRecorded record of the owning service | FSD P7 A2.2 (FEAT-DRI-02); Architecture v5 (local record, then central ledger within 5 minutes); ADR-022 |
| BR2 | The final call of the entry says what the move was: "CASE_TRANSFERRED" for a case moved off an owner above the cap, "OWNER_ASSIGNED" for an unassigned case given an owner | FSD P7 A2.2 AC-P7-002-01; FSD P3 A2.17; final call list |
| BR3 | The `actions` payload carries the reason "REBALANCE", the assignment rule ID and rule version taken from the queue's ASSIGNMENT row, and the queue and owner identifiers only. No case attribute, no amount and no personal data is copied into the entry | REQ-CWC-015; legacy BR1, BR7; TSD P7 T3.1 (DF-DEC-014) |
| BR4 | The idempotency key is the case and the business date. A repeated record adds no second entry, writes no new `chain_seq` and answers the first entry's ID | R-UNI-40; TSD P7 T3.1 (DF-DEC-031); DP-09 |
| BR5 | A queue with no cap moves no case, and a non-move records nothing: the ledger holds decisions, not intentions | Legacy AC5, BR4; DL23 |
| BR6 | The ledger is append only and hash chained: an entry is never updated or deleted, a re-hashed or edited entry is refused, and a read that fails the chain answers MSG-P7-012 and returns the entry flagged | REQ-DRI-002; FSD P7 A2.1 AC-P7-001-01, AC-ALT-P7-001-01; R-UNI-39; NFR-035 |
| BR7 | The count of the entries of the business date reconciles to the moves the run reports with zero difference. A difference holds the reconciliation and lists the case for the data steward; it is never rounded, ignored or published as a note | Legacy BR6; DL25; REC-01; REQ-RDF-012 |
| BR8 | An action whose decision cannot be recorded does not happen, and a count that cannot be read is not a zero: an unreadable ledger store blocks the caller with MSG-P7-003 | Principle 5; R-UNI-39; FSD P7 A2.5, A2.1 AC-EXC-P7-001-03 |
| BR9 | There is no data lake and no file: the lake copy of the log and the INT-19 and INT-20 batch are removed, and reporting is built from events into rwb-reporting | DP-17; ADR-018; Architecture v5 slide 37 and slide 44 |

How the rules hold in `rwb-decision`:

- BR1 and BR2 are executed by `DecisionRecordedListener` and `RebalanceEntryWriter`: the final call is taken from the move the record describes, never guessed from the case state, and a record with no move writes no entry.
- BR3 is executed by the mapping: the `actions` payload is built from the record's reason, rule ID, rule version, queue and owners. The case ID is the only case reference on the entry, and no case status, stage, amount or party value is written.
- BR4 is executed by the inbox key `(case_id, business_date)` and by the idempotency key of the entry; the repeat path answers the first entry's ID and writes nothing.
- BR5 is executed by the record itself: rwb-case publishes DecisionRecorded for a move only, so this service never needs to know about a cap.
- BR6 is executed by the store's trigger and chain (RWB-P7-E1008-APP) and by the chain check of the read; this story adds no path around either.
- BR7 and BR8 are executed by `LedgerReconciliationReader`: the count is read from `decision_log_entry` in `rwb_decision`, the run is read through the contract, and a failed read or a failed contract answer holds the reconciliation instead of releasing it.
- BR9 is executed by what is absent: no file writer, no lake client and no outbound batch exists in this service.

### 9. State transitions

The case state machine is not this service's: rwb-case owns the case status, its stage and the assignment (TSD P7 T4, "No case state machine of its own"). A rebalance move changes the owner of a case in `rwb_case` and leaves the case status, the stage clock and the prescription date as they are (R-UNI-18). This slice changes no case state and writes no case attribute.

| Object | From | Event | To |
|---|---|---|---|
| `decision_log_entry` | absent | a DecisionRecorded that carries a move, and no entry for that case and business date | one entry appended, with `final_call`, `actions`, the idempotency key, `chain_seq`, `prev_hash` and `entry_hash` |
| `decision_log_entry` | appended | any UPDATE, DELETE or re-hash through the service login or the schema owner | refused; the entry stays as it is and the attempt is audited |
| `decision_log_entry` | appended | a repeated DecisionRecorded for the same case and business date | unchanged; the first entry's ID is answered and the repeat is counted |
| reconciliation of a business date | not taken | the count is read and compared with the run | released when the difference is 0; held when it is not, with the case listed |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-decision service identity (the rwb-decision login, DP-02) | Consumes DecisionRecorded, appends the entry, counts the entries of a business date and reads the run through the rwb-case contract; holds no grant on `rwb_case` and no lake or file access |
| SY-CASEWF, case workflow module (Decision log C) | Produces the DecisionRecorded record of a move through the decision-record library; this service consumes it, and the local record and the event are written by the writer in the owning service (SY-DECLOG) |
| RW-TEAMMGR, team manager (Decision log R) | Reads the entries of the business date and the count of the rebalance in team scope |
| RW-DATASTEW, data steward and data product owner (Decision log R) | Receives the reconciliation break and the case of the missing move |
| RW-AUDIT, internal audit; RW-COMPLY, Compliance and PDPA officer (Decision log R) | Reads every entry with its rule and version; receives the incident for an entry that fails the chain |
| RW-PLATADM, platform administrator (Decision log R) | Reads the count and the break for a platform check; a rerun of the run itself is rwb-case's and needs Platform administration U |
| rwb-case (P3) | Owns the run, the moves, the cap, the queue and the owner; this service reads the run through the contract only |

The authorisation decision is the cached permission decision from rwb-access that the service template's guard already holds; DP-08 is not in this slice's pattern set, so this story adds no guard, no decision endpoint and no access entry of its own. The refusals are 403 with MSG-P4-002 for a role without Decision log R, and 503 with MSG-P7-003 when the ledger store or the run record cannot be read. The role codes above are rows of the role model in `rwb_access` (TSD P7 T6.1) and are not fixed in code.

### 11. Data

| BR Field ID | Table in rwb_decision | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 | decision_log_entry | id | Write (the entry ID, answered on a repeat) |
| DF-DEC-002 | decision_log_entry | case_id | Write (the case of the move, and no other case value) |
| DF-DEC-003 | decision_log_entry | decision_code | Write (from the record; the list is LOV-DECISION) |
| DF-DEC-004 | decision_log_entry | rule_id | Write (the assignment rule ID of the queue's ASSIGNMENT row) |
| DF-DEC-005 | decision_log_entry | rule_version | Write (the version of that row in force at the run) |
| DF-DEC-008 | decision_log_entry | inputs_ref | Write (as the record carries it; the inputs snapshot is the writer's) |
| DF-DEC-012 | decision_log_entry | final_call | Write ("CASE_TRANSFERRED" or "OWNER_ASSIGNED") |
| DF-DEC-014 | decision_log_entry | actions | Write (reason "REBALANCE", rule ID and version, queue and owner identifiers; the inner keys are Not specified in the source documents (GAP-1326; ASM-2339)) |
| DF-DEC-016 | decision_log_entry | decided_at | Write (the decision time of the move; the business date is the one the record carries) |
| DF-DEC-017, DF-DEC-018 | decision_log_entry | prev_hash, entry_hash | Write (from the chain) |
| DF-DEC-028 | decision_log_entry | chain_seq | Write (from the chain; never reused, not consumed by a refused append) |
| DF-DEC-030 | decision_log_entry | actor_user_id | Write (the service identity of the run) |
| DF-DEC-031 | decision_log_entry | idempotency_key | Write (the case ID and the business date; the duplicate check of the repeated record) |
| DF-CAS-001, DF-CAS-009, DF-CAS-010, DF-WRK-002, DF-WRK-004 | case and queue, through the rwb-case contract of RWB-P3-E1030-CON | id, owner_user_id, queue_id, queue_code, team_code | Read only, per request, for the break listing; never written and never joined |
| (the run record) | through the rwb-case contract | the move count and the case IDs of the run | Read only; the fields are Not specified in the source documents (GAP-1326; ASM-2339) |

Field IDs are those in the Technical Specification P7 Decision center and log T3.1 and the Logical Data Model and Data Dictionary. The owners are the ownership map's: `decision_log_entry` and `approval` in `rwb_decision` by P7 rwb-decision; `queue_measure` by P3 rwb-case; `measure_definition`, `measure_snapshot` and `measure_publish` by P9 rwb-reporting. This story reads and writes none of the last four, and no case, queue or measure table is read across a schema boundary.

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Status | Used for |
|---|---|---|---|
| GET | `/api/recovery/decision/v1/decision-log` | Declared by API-P7-006 (TSD P7 T-A), owner P7 | The reconciliation read: `decision`, `from` and `to` of the business date, with `page` and `size` of the standard query, answering the items and their total |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | Declared by API-P7-007, owner P7 | One counted entry with its inputs and versions; answers MSG-P7-012 when the entry fails the chain |

This slice adds no path, no query parameter and no response field: it fixes what the count of a business date means and what the page answers when an entry does not match the chain. The value the `decision` filter takes for the rebalance entries, and how the business date is expressed in `from` and `to`, are Not specified in the source documents (GAP-1326; ASM-2339). Both paths answer 401, 403 without Decision log R, and 503 when the store cannot be read (TSD P7 T-A.2).

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | the rebalancing run record read, path Not specified in the source documents (GAP-1326; ASM-2339) | rwb-case (P3), under RWB-P3-E1030-CON | The moves the run reports for a business date: the count of moves and the case IDs behind them, for the reconciliation | One hop, 2 s (DP-11) |

The contract is consumed as the published OpenAPI 3.1 document plus its fake. This slice calls no other service: the entries come from the topic, and the case and queue values in a break listing are the IDs the run record and the entry already carry.

#### 12.3 Events published

None. This slice publishes no event of its own and adds nothing to `rwb.decision.events.v1`. The 5-minute completeness of the central ledger, its gap alerts and the daily chain check are the store's and the platform's; nothing is forwarded to a lake or a file (DP-17).

#### 12.4 Events consumed

| Event | Topic | Producer | Handling |
|---|---|---|---|
| DecisionRecorded (EV-08) | `rwb.decision-record.v1` | all 19 services, through the decision-record library (RWB-PLT-E1027-CON, DP-03) | Idempotent by case and business date into `decision_log_entry`; one entry per move; a record with no move writes nothing; the CloudEvents envelope and the key are the library's (DP-09) |

A record that fails the schema of the entry, or arrives out of order for a business date, is retried and then parked on the dead-letter topic with its headers; the retry and dead-letter policy is the event platform's (DP-09) and this story configures no policy of its own.

#### 12.5 Workflows and activities

None. The rebalance run, its Schedule and its activities are rwb-case's (RWB-P3-E1030-APP); this service consumes events and answers a read. It starts no workflow, runs no activity and holds no Quartz job (DP-10).

#### 12.6 Schedules

None. This service holds no Schedule in this story: JOB-06 rebalancing at 06:30 is a Temporal Schedule in rwb-case; JOB-13 is not a Schedule at all, because decision-log ingest is continuous on Kafka; JOB-14 hash-chain check at 02:00 and JOB-20 rule promote at 00:01 are Schedules of this service that belong to its store and rule stories; JOB-15 reporting extract at 01:30 is rwb-reporting's, from its own projections, with no data lake (Architecture v5 job map).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `decision_log_entry` | P7 (rwb_decision) | One entry per decision, append only and hash chained; this story appends the rebalance entries and counts them |
| processed_event, idempotency_key | PLT library, created in `rwb_decision` | Inbox and idempotency objects (DP-09); this slice writes them for the rebalance records |

No `rwb_case`, `rwb_access` or `rwb_reporting` table is read and no `v_ace_*` view is read (DP-01, DP-05). `queue_measure` is P3's and `measure_definition`, `measure_snapshot` and `measure_publish` are P9's; this story holds no grant on them.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case contract fake (RWB-P3-E1030-CON) | The run record and the case read | A run for 2026-12-02 reporting 12 moves in `TDR-BKK-CO` with 12 unassigned cases, owners `U-61` at 140 and `U-62` at 144, cap 150 and method `LOWEST_LOAD`; a run with 2 moves off `U-63` at 153 and one case left with `MSG-P7-003`; a run with no move in `WO-BKK-CO` at no cap; a run reporting 12 moves against 11 entries for the difference of one; a slow answer past the 2 s budget |
| decision-record library fixture (RWB-PLT-E1027-CON) | The DecisionRecorded payload | The 12 records of the run, the 2 transfers, a repeated record for case `RW-2026-000501`, and a record with no move |
| ledger fixture (RWB-P7-E1008-APP) | `decision_log_entry` and its chain | Appended entries with `chain_seq`, `prev_hash` and `entry_hash`; an entry `230` re-hashed and edited; a store closed for the failed read |

The field names inside the run record and inside the `actions` payload are stubbed from the published fixtures of RWB-P3-E1030-CON and the decision-record library; their list is Not specified in the source documents (GAP-1326 and GAP-1326; ASM-2339 and ASM-2339).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 1 consumed | The count read `GET /decision-log` and the entry read `GET /decision-log/{entryId}` on base `/api/recovery/decision/v1`; one hop to the rwb-case run record within 2 s (DP-11) |
| Kafka | 0 published, 1 consumed | DecisionRecorded (EV-08) on `rwb.decision-record.v1`, idempotently into `rwb_decision`; nothing published on `rwb.decision.events.v1` |
| Temporal | None | No workflow, no activity and no Schedule in this story; task queue `rwb-decision` serves the other P7 stories |
| File | None | This story reads and writes no file, and the copy of the decision log to the data lake is removed under DP-17 |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `rebalance`, Java package `th.co.scb.ace.workbench.recovery.decision.rebalance`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DecisionRecordedListener | Inbox consumer | Consumes DecisionRecorded on `rwb.decision-record.v1`, recognises a record by case and business date, answers the first entry's ID on a repeat, and parks a record that fails the schema |
| RebalanceEntryWriter | Service | Maps a move to one entry with its final call, its `actions` payload, its rule ID and version and its idempotency key, and appends it through the store; never updates and never deletes |
| LedgerReconciliationReader | Service | Counts the entries of a business date on `GET /decision-log`, compares the count with the run, releases it at zero difference and holds it with the case listed otherwise |
| RunRecordClient | REST client | Calls the rwb-case run record, one hop and 2 s (DP-11), and maps a failed or slow answer to a held reconciliation |

**Database and migrations**

- Writes `decision_log_entry` only, through the store of RWB-P7-E1008-APP, with the rebalance mapping of this story. No case, queue or measure column is added and no foreign key into another schema exists.
- Migration in this story, in the per-service Flyway sequence of DP-15: `V1030_1__rebalance_ledger.sql` adds the index `(decided_at, final_call)` used by the count of a business date and the unique index on `(idempotency_key)` used by the repeated record; it adds no column. The table, its trigger and its chain arrive with the store migration.
- No row is seeded by this story: the queue, the cap, the owners and the run are rwb-case's data, and the measure definitions are rwb-reporting's.

**Configuration and reference data**

- No business value is configured here: the method, the cap, the owners and the moves are rwb-case's, read through the contract; the final calls are rows of the final call list; the reason "REBALANCE" is a row of the assignment reason list (LOV-ASSIGN-REASON).
- Two settings only: the rwb-case contract base for the run record, and the rwb-decision login (DP-02). The 2 s timeout and the one-hop rule are the platform values of DP-11, set in the client configuration.
- No tolerance is configured: the difference must be zero, and a deliberate tolerance would need a business decision that the sources do not contain.

**Build steps**

1. `DecisionRecordedListener` against the library fixture, with the 12 records of the run and a repeated record; tests for AC1 and AC3.
2. The mapping of the final call and of the `actions` payload, with the rule ID and version taken from the record, and the no-move path so that a queue with no cap and a case that did not move write nothing; tests for AC1, AC2 and AC4.
3. `LedgerReconciliationReader` with the count of a business date and the zero-difference release; test for AC5.
4. `RunRecordClient` against the contract fake with the found, the slow and the failed answer; tests for AC5 and AC6.
5. The held path with the break listing for the data steward; test for AC6.
6. The refusals: an update, a delete and a re-hash refused, MSG-P7-012 on a broken chain, and MSG-P7-003 on an unreadable store; test for AC7.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

This is a secondary slice with no owned legacy acceptance criteria of a build story: it adds no new build dependency of its own (metadata "Depends on (build)" = None) and builds against the `rwb_decision` baseline, the contract fake of RWB-P3-E1030-CON and the decision-record library. Read one by one:

- DP-01, DP-13 and DP-15 are the target shape itself: schema `rwb_decision`, the base `/api/recovery/decision/v1` and the per-service migration `V1030_1__rebalance_ledger.sql`, with no new dependency.
- DP-03 is live: the entry is written from the DecisionRecorded record of the decision-record library, and no writer is written in this service. DP-04 is not in the pattern set, so no rule model is served here: the rule ID and version come from the record.
- DP-07, DP-09 and DP-14 apply to what surrounds the entry: the assignment reason and the final call are list rows read through the reference-data contract, the inbox, the idempotency key and the CloudEvents envelope come from the event platform, and no topic name or list value is written in this slice's code.
- DP-10 applies as a prohibition: no Quartz table and no job here. JOB-06 stays in rwb-case, JOB-13 is continuous on Kafka, and JOB-14 and JOB-20 stay with this service's store and rule stories.
- DP-11 is live for the reconciliation: the in-process read of the run becomes one REST hop to rwb-case with a 2 s timeout and the published fake.
- DP-17 is live as a removal: the lake copy of the log, the INT-19 and INT-20 batch and JOB-15's dependency on them are gone, and nothing in this service writes a file or reaches an outside system. DP-19 applies to the screen the entries are read on: SCR-38 Decision log query is served through the gateway-bff composite route, and the route itself is the query story's.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P3-E1030-CON stay green, and a SIT week shows every move of the 2026-12-02 run in `decision_log_entry` once with its reason and rule, the count of the business date equal to the moves of the run, a difference of one listed for the data steward and nothing released for that date, no update, delete or re-hash accepted, and no file and no lake client in the service.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The ledger store cannot be read when the count is taken, or the run record cannot be read | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-012 | A counted entry does not match the decision log chain | Entry {entryId} does not match the decision log chain. Do not rely on it until Compliance has reviewed it. |
| MSG-P4-002 | The caller's role holds no Decision log R | You cannot {action} here. Your role does not include it. |
| The break message, whose ID is Not specified in the source documents (GAP-1326; ASM-2339) | The count of the business date differs from the moves the run reports | The decision ledger count for {date} does not match the moves of the run: {count}. |

The break itself is a row on the reconciliation break list, owned by rwb-case (REC-01), with the business date, the two counts and the case ID of the missing move, addressed to the data steward RW-DATASTEW; its check name and its wording are the placeholder row above. Every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. The read answers 400 for an unreadable date range, 403 for a role without Decision log R, and 503 when the store or the run record cannot be read; a difference is not an error status, because the read succeeded and the reconciliation is held.

### 15. Screens and states

SCR-38 Decision log query shows the entries of the business date with their case, decision, rule and version, final call and time, and each entry carries its chain state; the count the reader sees is the total of the same query this story reconciles. The reconciliation break is shown on the reconciliation break list with the business date, the two counts and the case of the missing move. No new screen, no new state and no new filter belongs to this story: the screen, its empty state and its export are RWB-P7-E2005-APP, and the break list is rwb-case's screen.

Both are served through the gateway-bff composite route (DP-19), which calls rwb-decision for the entries and rwb-case for the break list. The field-level masking of the composite route and the route specification are Not specified in the source documents (GAP-1326; ASM-2339). The held state is visible on the break list only; the entry list itself shows no held flag, because the entries were written and only the count of the date is held.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-030-11 | AC7, BR6: a role without Decision log R reads neither the count nor an entry; the rerun itself is rwb-case's and refuses the same role with MSG-P4-002 | Component | Role `RW-CASEOWN` reads `GET /decision-log` and `GET /decision-log/{entryId}` and is refused with MSG-P4-002; the rerun of JOB-06 is refused with MSG-P4-002 |
| TC-E1-030-01 | AC1, AC2, BR1, BR2, BR3: the 12 moves of the run are 12 entries with their reason and rule, and a transfer off an over-cap owner is "CASE_TRANSFERRED" | Integration | Queue `TDR-BKK-CO` with `LOWEST_LOAD` and cap 150; 12 unassigned cases; `U-61` at 140 and `U-62` at 144; business date 2026-12-02; 8 entries to `U-61` and 4 to `U-62` |
| TC-E1-030-02 | AC5, BR7: the count of the business date equals the moves the run reports, with the snapshot at 06:52 as the run's own time | Integration | Snapshot at 2026-12-02 06:52; count 12 against 12 moves; depth 296 and 0 unassigned in `TDR-BKK-CO` are rwb-case's |
| TC-E1-030-03 | BR3: the ledger holds no breach measure; the breach alert MSG-P3-028 and the measure are rwb-case's and rwb-reporting's | Contract | Case `RW-2026-000501` in `TDR-BKK-CO` past its service level; the count read returns no breach field and no entry changes |
| TC-E1-030-04 | AC2, BR1: no member has capacity, so the run moves nothing and the ledger records nothing; MSG-P3-011 is rwb-case's | End to end | Every member of `TDR-BKK-CO` at 150 and 5 cases with no owner; 0 entries for the queue on 2026-12-02 |
| TC-E1-030-05 | AC4, BR5: a queue with no cap moves no case and therefore records nothing | Component | Queue `WO-BKK-CO` with no capacity cap; run for 2026-12-02; 0 entries and 0 moves |
| TC-E1-030-06 | AC2, AC7, BR8: the move whose record fails is not in the ledger and the run lists it; the ledger records 2 of 3 | End to end | Owner `U-63` at 153; the second of the 3 newest fails; 2 entries `CASE_TRANSFERRED`, 1 case stays with MSG-P7-003 on the run record |
| TC-E1-030-07 | AC3, BR4: a repeated run adds no second entry and answers the first entry ID | Integration | JOB-06 twice on 2026-12-02; one entry per case and business date; repeat count 12 |
| TC-E1-030-08 | AC2, BR1: a held case produces no move and no entry; the hold checks are rwb-case's | Unit | Owner `U-64` at 152 with the 2 newest held (`deviation_open` true); 2 entries for the next 2 newest and none for the held pair |
| TC-E1-030-09 | AC6, BR7: a difference of one holds the reconciliation and lists the case; the queue depth check is rwb-case's | Component | Depth 88 against count 87 in `DIL-BKK-CO`; 12 moves against 11 entries; case `RW-2026-000501` listed |
| TC-E1-030-10 | BR2, BR5: an owner exactly at the cap loses no case and gets no entry | Unit | Owner `U-65` at exactly 150; 0 entries `CASE_TRANSFERRED` for `U-65` on 2026-12-02 |
| TC-E1-030-12 | AC7, BR6, BR8, NFR-035: the ledger write is forced to fail for every move in the run, and the store is forced to be unreadable for the count | NFR | Store closed for the whole run and for the count; no entry appended without a record, 503 with MSG-P7-003, no count released, one incident per break |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The legacy level System is answered here at End to end or Integration for the slice this story owns, Access at Component, and Resilience at NFR; the Unit rows are the reduced slice of a System case. No -ITG copy of these cases sits here: they belong to RWB-ITG-E1030-ITG, which proves the same values across rwb-case, rwb-decision and rwb-reporting end to end.

### 17. Guardrails

- No business value in code: the queue, the cap, the method, the owners, the moves and the run are rwb-case's, read through the contract; the final calls and the assignment reasons are list rows. No cap, no queue code and no count threshold appears in this service's Java.
- No personal data in events, workflow inputs, logs or tests. This story writes case IDs, queue IDs, owner IDs, a rule ID and version and a count; no name, address, identity number, account number or amount is read, logged or copied into `actions`.
- No cross-schema read (DP-01) and no ACE view (DP-05): `rwb_decision` reads no `rwb_case`, `rwb_access` or `rwb_reporting` table and no `v_ace_*` view, and the account and party facts behind a case never reach the ledger.
- Append only and chained: nothing in this story updates, deletes, re-hashes or repairs an entry, and a broken chain is reported, never hidden.
- One hop, 2 s, to the run record, and a failed or slow answer holds the reconciliation instead of releasing a count (DP-11, principle 5).
- No file and no external call: the lake copy and the INT-19 and INT-20 batch are removed and no replacement path exists in this service (DP-17). The case ID is the Kafka key of the consumed topic (DP-09) and no topic name is typed in code (DP-14).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-015 | Daily rebalancing; queue counts, ageing and breaches reported | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-17, FEAT-CWC-18, FEAT-WKM-11 | All recovery processes | R-UNI-19, R-UNI-30, R-UNI-39, R-UNI-40 | TC-E1-030-01, TC-E1-030-04, TC-E1-030-05, TC-E1-030-06, TC-E1-030-07, TC-E1-030-08, TC-E1-030-10, TC-E1-030-12 |
| REQ-RDF-012 | Baseline measures for cases by queue and age published | Epic 1, 3.3; Program, 5.1 | FEAT-RPT-02 | 15 Manage performance, data and AI | REC-01; DL25 | TC-E1-030-02, TC-E1-030-03, TC-E1-030-09, TC-E1-030-11 |

REQ-CWC-015 is answered by this story only for the record of a move, not for the selection of the move: the run, the cap and the choice are RWB-P3-E1030-APP. REQ-RDF-012 is answered only for the count that reconciles, not for the measures themselves, which are rwb-reporting's. The -ITG copies of the test cases are carried by RWB-ITG-E1030-ITG.

| Legacy reference | Where it is kept |
|---|---|
| Legacy key RWB-E1-030; story RWB-P7-E1030-APP; contract RWB-P3-E1030-CON; baseline `rwb_decision` | Metadata; sections 1, 3, 12 |
| Legacy BR7 and principle 5 (every move logged before it takes effect); R-UNI-39 | Sections 1, 8 (BR1, BR8), 9 |
| Legacy BR2 and R-UNI-19 (the newest cases off an owner above the cap); the final call "CASE_TRANSFERRED" | Sections 1, 7 (AC2), 8 (BR2) |
| Legacy BR1 (unassigned cases assigned within the cap); the final call "OWNER_ASSIGNED" and reason "REBALANCE" | Sections 7 (AC1), 8 (BR2, BR3) |
| Legacy BR4 and AC5 (a queue with no cap is reported and not rebalanced) | Sections 7 (AC4), 8 (BR5) |
| Legacy BR6 and DL25, REC-01 (measures publish only on zero difference) | Sections 7 (AC6), 8 (BR7), 14 |
| Legacy AC6 and MSG-P7-003 (the case whose log write failed stays) | Sections 4, 5, 7 (AC2), 14 |
| Legacy BR8 and R-UNI-30 (a breach alerts and moves nothing) | Section 16 (TC-E1-030-03) |
| Legacy section 12 job table (JOB-06, JOB-15) and the data lake copy | Sections 2, 12.6, 12.9, 19 |
| MSG-P7-003, MSG-P7-012, MSG-P4-002 and the break message | Section 14, exception paths |
| Field IDs DF-DEC-001 to DF-DEC-018, DF-DEC-028, DF-DEC-030, DF-DEC-031 | Section 11 |
| Legacy test cases TC-E1-030-01 to TC-E1-030-12 | Section 16 |
| The other slices of RWB-E1-030 (rwb-case, rwb-reporting, the integration proof) | Sections 2, 19 |

### 19. Out of scope

- The rebalancing selection, the caseload cap, the hold checks, the owner choice, the assignment write, the run record and the JOB-06 Schedule: rwb-case (RWB-P3-E1030-APP), with the queue and the owner in its own schema.
- The queue measure snapshot, the ageing and breach measures, the Power BI report and JOB-15 at 01:30 from its own projections: rwb-reporting and its measure stories, and `measure_definition`, `measure_snapshot` and `measure_publish` are its tables.
- The decision log store, its append-only trigger, its hash chain, the chain verification and JOB-14 at 02:00: RWB-P7-E1008-APP.
- The decision log writer, the local record, the DecisionRecorded payload and its schema checks: RWB-P7-E1027-APP.
- Rule authoring, validation, test scenarios, four-eyes approval and rollback: RWB-P7-E1073-APP.
- The decision log query API as a whole, its filters, export and access events: RWB-P7-E2005-APP; this story only reads the count it needs.
- SCR-38 Decision log query as a screen, with its states, filters and export: RWB-P7-E2005-APP; the reconciliation break list as a screen: rwb-case. The access matrix, the scope decision and the access log: rwb-access (RWB-P4); this service consumes the cached decision from the template.
- The removal of the data lake and of INT-19 and INT-20 across the estate, and the last copy of any legacy log in a lake: the platform and reporting stories, under DP-17 and ADR-018; this story only confirms that its own service writes no file.
- The end-to-end proof of these values across rwb-case, rwb-decision and rwb-reporting: RWB-ITG-E1030-ITG; and the `rwb_decision` schema baseline, the login, the topic and queue provisioning, the chart, the dashboards and the runbook of this service.
