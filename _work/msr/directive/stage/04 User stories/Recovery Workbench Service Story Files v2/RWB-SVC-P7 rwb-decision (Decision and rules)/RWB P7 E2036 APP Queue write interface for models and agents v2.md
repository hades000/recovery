# RWB-P7-E2036-APP Queue write interface for models and agents

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E2036-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-036 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP08, DP09, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P7-AM |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E2036-CON |
| Contract version | Not specified in the source documents (DOR-RWB-P7-E2036-APP-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to REQ-CWC-017, REQ-CWC-018, REQ-CWC-019, REQ-CWC-020, REQ-ACA-010) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-036 for rwb-decision, the ledger record of a queue placement made by a model or an agent. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P7-E2036-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 15 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **center of excellence analyst (RW-COE)**, I want **every placement that an approved model or agent makes on a queue recorded as one append-only, hash-chained decision entry that names the caller, its version, the reason and the queue it placed the case on, and readable afterwards**, so that **analytical output reaching a person the next working day stays answerable to audit on the same terms as a decision a person took, and no model or agent write exists in Recovery without its record**.

Inside `rwb-decision` this is the decision-record slice of the legacy story RWB-E2-036:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1`, shared topic `rwb.decision-record.v1`, Temporal task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`.
- One deliverable and nothing else: the placement entry of decision code D6 in the central decision ledger. It takes the facts of one admitted placement off the shared topic, validates the decision code, the final call and the version, appends one `decision_log_entry` in `rwb_decision` with the hash link of the entry before it, marks the delivery in its inbox, and serves the entry back on the two decision-log reads under the Decision log right and the case scope.
- The record is written through the decision-record path of DP-03 and never through another service's table. The entry, its chain link and its inbox mark commit together or not at all, and the row is never updated and never deleted (REQ-DRI-002).
- The interface itself is not here. The caller-facing operation on the integration base, the approved callers list, the feature flag, the request validation and the forwarding stay in `rwb-integration` (P2, RWB-P2-E2036-APP and RWB-P2-E2036-CON); the placement, the allocation method, the caseload cap, the overflow queue and the local decision record of the placement transaction stay in `rwb-case` (P3); the right, the scope and the masking stay in `rwb-access` (P4).
- The legacy decision-log mapping is carried unchanged: case `RW-2026-000501`, decision code D6, the model or agent version `MDL-SYN-PRIORITY 1.4.0`, the reason `High cure score`, the caller identity SY-AGENT and the final call `PLACED MTG-BKK-PRI`.
- The legacy behaviour carried into the decision service is unchanged: one entry per placement even when the request repeats (legacy AC7), the entry in the same transaction as the change it records (legacy AC3, now the owner's local record), and no placement without a record (legacy BR5, BR6, R-UNI-39).
- The database login used by the capability is the per-service login of DP-02. Its name is Not specified in the source documents (GAP-2412; ASM-4016); this story uses the phrase "the `rwb-decision` login (DP-02)" and never the shared monolith login.

### 2. Business rationale

Model scores and agent findings reach the queues today through a weekly file that a person loads by hand, so a case flagged on Monday is worked the following week. The interface of the legacy key lets an approved caller place a case on a queue the day the decision is made, under the queue's own allocation rules. What audit asks of it is the other half, and it is this story: which caller placed the case, under which model or agent version, on which queue, and why (REQ-CWC-018, NFR-078). Without the entry the bank can show that a case sits on a queue but not who put it there or on what basis, and a model or agent write would rank below a decision a person took (FSD P7 v3 A2.2).

Under Architecture v5 the ledger is `rwb-decision`'s (slides 14, 20 and 41) and the realignment changes the mechanism, not the business rule. The legacy wrote the entry through `DecisionLogWriter` with `Propagation.MANDATORY`, inside the placement transaction; one database transaction cannot span services, so the owner of the placement writes its own local `decision_record` in its transaction and publishes `DecisionRecorded` on `rwb.decision-record.v1` (DP-03, ADR-022), and this service holds the central ledger entry and reads it back. The decision code and the final call become reference data read with the version in force (DP-07); the record arrives on the outbox and inbox with CloudEvents (DP-09, DP-14); the read guard comes from the authorise contract (DP-08); the reads are served on the service base (DP-13) through the composite route (DP-19).

The body of the placement stays with its owners: the allocation engine and the queue data are `rwb-case`'s (DP-11), the caller list and the flag are the admission contract's, and the account data never enters this service at all.

This story carries the record half of REQ-CWC-017 and REQ-CWC-018 and the version half of REQ-ACA-010: identifiers, a decision code, a version, a reason, a caller identity, a queue code and dates, and no name, e-mail address, mobile number, national identity number or account number.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P2-E2036-CON | The admission contract baseline of the legacy key: the caller-supplied facts (case, reason, caller code, version), the caller's service identity, the record obligation of NFR-078 and the refusal codes the fact must agree with. The element names of the fact on the shared topic are Not specified in the source documents (GAP-2412; ASM-4013) |
| The owner's local record (`rwb-case` for the placement, `rwb-integration` for the admission) | The `decision_record` row and the `DecisionRecorded` fact written in the owner's own transaction by the decision-record library of DP-03, one key per placement |
| RWB-PLT-E1027-CON, RWB-PLT-TE006-CON | The decision-record library with the chain, and the outbox, inbox and CloudEvents envelope on `rwb.decision-record.v1`; carried in the DP application table of section 13 and in the gap |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-E1037-CON, RWB-P4-E1037-CON | The reference-data contract for LOV-DECISION and the final-call list with the version in force, and the authorise answer behind the two reads; carried in the same way |

Business preconditions carried from RWB-E2-036 (legacy sections 3 and 4):

- Feature flag `rwb.casewf.queue-placement` is on, and permission matrix version "PM-SIT-02" gives service identity SY-AGENT Queue and allocation C (legacy section 3).
- The approved callers list holds caller "MDL-SYN-PRIORITY" of type MODEL for service identity SY-AGENT, with version "1.4.0" (legacy section 3, AC1).
- Queue "MTG-BKK-PRI" of team "MTG-BKK" uses method ROUND_ROBIN with caseload cap 150 and overflow queue "MTG-BKK-OVF" (legacy section 3).
- Case "RW-2026-000501" has status NEW, no owner and no open deviation; case "RW-2026-000503" has status CLOSED; case "RW-2026-000504" has deviation X2 open (legacy section 7).
- No build dependency. Day 1: the fact is consumed against the admission contract baseline and its fake, so the entry can be built and tested before the callers are switched on.

### 4. Flow

1. A model job or an agent, under service identity SY-AGENT, sends the placement to `rwb-integration` with case "RW-2026-000501", reason "High cure score", caller "MDL-SYN-PRIORITY" and version "1.4.0" (P2, legacy section 4 step 1).
2. `rwb-integration` checks the flag, the approved callers list and the matrix through the access check, forwards the placement to `rwb-case`, and takes its answer (P2 and P3; not this story).
3. `rwb-case` places the case, applies the queue's method and cap, ends any previous assignment, writes its local `decision_record` row of code D6 and the outbox row in one transaction, and returns the placement result (P3, legacy steps 6 to 8).
4. The outbox relay publishes `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` in CloudEvents 1.0, keyed by the entry ID (DP-09, DP-14).
5. `rwb-decision` `PlacementRecordListener` consumes the delivery through its inbox, filtering on decision code D6, and refuses a delivery it has already processed (X3).
6. `rwb-decision` `PlacementRecordValidation`: reads the decision code D6 and the final-call value `PLACED MTG-BKK-PRI` through the reference-data contract of DP-07 with the version in force, and checks that the entry names a model version or an agent version; a value out of its list or a missing version is refused with MSG-P7-009 naming the field and nothing is written (X1, X4).
7. `rwb-decision` `ChainWriter`: takes the last `entry_hash` and `chain_seq` of the ledger under the append lock, computes the entry hash over the canonical form, and builds the row with `prev_hash` equal to that last hash and `chain_seq` equal to the next number.
8. `rwb-decision` `PlacementRecordAppendService`, one transaction in `rwb_decision`: the `decision_log_entry` row is inserted with the case, decision code D6, the model or agent version, the reason as the recommendation, the caller identity as the actor, the final call and the queue code, and the inbox mark is written; then the transaction commits (AC1, AC2).
9. A failure of the append rolls the transaction back, keeps the chain at its last entry, and leaves the delivery to the retry topic and then the dead-letter topic with an incident under R-UNI-39; the owner's local record and the placement stand unchanged (X2, AC6).
10. A reader with the Decision log right R and the case in scope reads the entry with `GET /api/recovery/decision/v1/decision-log/{entryId}` or the page of one case with `GET /api/recovery/decision/v1/decision-log?caseId=…`, and sees the code D6, the version, the reason, the caller, the final call and the two hashes (AC3, AC8).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The record names neither a model version nor an agent version | Refused before anything is written; no entry and no chain sequence consumed; the delivery is held on the retry topic and then the dead-letter topic with a task for the platform administration role naming the case and the field | MSG-P7-009 | AC5 |
| X2 | The chain append, the insert or the inbox mark fails | The transaction rolls back; no entry, no chain sequence consumed, the chain at its last entry; the delivery is retried and then held; an incident is raised under R-UNI-39; the placement and the owner's local record are unchanged | MSG-P7-003 | AC6 |
| X3 | The same placement fact is delivered twice, or two placements of one case arrive at once | The inbox mark and the unique placement key give one entry; the repeat is acknowledged, adds no chain link and consumes no sequence | None | AC4 |
| X4 | The decision code or the final call is not a value of its list | Refused with the field named; nothing is written and the delivery is held as X1 | MSG-P7-009 | AC5 |
| X5 | The reader holds no Decision log right, or the read reaches the service without the declared right | 403 and nothing returned | MSG-P4-002 | AC8 |
| X6 | The case of the entry is outside the reader's scope | 404 and nothing returned | MSG-P4-003 | AC8 |
| X7 | The placement was refused by the case side (closed case, open deviation, caller not approved, flag off, unknown queue or case) | No fact is published, so no entry is written and no chain sequence is consumed; the refusal and its message are the owners' | MSG-P3-005, MSG-P2-021, MSG-P2-020, MSG-P2-025, MSG-P4-003 (produced by `rwb-case` and `rwb-integration`) | AC7 |

An entry is never updated and never deleted: a wrong entry is corrected by a new entry that names the one it corrects in `corrects_entry_id`, so the ledger stays append only (REQ-DRI-002). The entry, its chain link and its inbox mark are always written together, so an entry cannot exist without its chain link and a delivery cannot be counted twice.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the admission contract baseline of RWB-P2-E2036-CON, the decision-record library, the authorise answer and the case read, and their fakes; no adapter, no allocation engine, no queue data and no rule engine is rebuilt here |
| Negotiable | The code values, the final-call list and the message texts are reference data or the message standard; the story fixes only one entry per placement, the chain, the version guard and the read guard |
| Valuable | Every model or agent write is on the ledger with its version, so the queue can be audited and the model review stands on a stored fact |
| Estimable | One listener, one validation service, one chain writer, one append service, two reads, one migration |
| Small | Fits one sprint with its tests; it is the decision-record slice of the legacy key |
| Testable | Each of the eight criteria in section 7 runs as an automated test against the contract fakes, a seeded chain and a fixed clock |

### 7. Acceptance criteria

```gherkin
Feature: Queue write interface for models and agents — the rwb-decision ledger entry of a placement

  Background:
    Given the environment is SIT
    Given feature flag "rwb.casewf.queue-placement" is on
    Given the permission matrix version "PM-SIT-02" gives service identity SY-AGENT Queue and allocation C
    Given the approved callers list holds caller "MDL-SYN-PRIORITY" of type MODEL for service identity SY-AGENT
    Given queue "MTG-BKK-PRI" of team "MTG-BKK" uses method ROUND_ROBIN with caseload cap 150 and overflow queue "MTG-BKK-OVF"
    Given case "RW-2026-000501" has status NEW, no owner and no open deviation

  Scenario: AC1 One admitted placement writes one D6 entry (new, D-RCV-60)
    Given the rwb-integration contract mock returns the admission of caller "MDL-SYN-PRIORITY" version "1.4.0" for case "RW-2026-000501" on queue "MTG-BKK-PRI" with reason "High cure score" under service identity SY-AGENT
    When the decision record of that placement arrives once on rwb.decision-record.v1
    Then the ledger holds one entry for case "RW-2026-000501" with decision code "D6", model version "MDL-SYN-PRIORITY 1.4.0", the reason "High cure score", the caller identity SY-AGENT and final call "PLACED MTG-BKK-PRI"
    Then the entry carries no name, no e-mail address, no mobile number, no national identity number and no account number

  Scenario: AC2 The entry, its chain link and its inbox mark commit together (new, D-RCV-60)
    Given the decision-record library mock holds a ledger of 100 entries that verify from chain_seq 1 to 100, the first previous hash being 64 zeros
    Given the rwb-integration contract mock returns the admission of case "RW-2026-000501" on queue "MTG-BKK-PRI"
    When the placement fact is delivered once
    Then the new entry has chain_seq 101, a prev_hash equal to the entry hash of the entry before it and an entry_hash equal to the SHA-256 of its canonical form
    Then the inbox holds one processed mark for the delivery and it is acknowledged once

  Scenario: AC3 The entry is readable afterwards with its model version and its caller (new, D-RCV-60)
    Given a decision record with decision code "D6" and model version "MDL-SYN-PRIORITY 1.4.0" was recorded for case "RW-2026-000501" on queue "MTG-BKK-PRI"
    Given the rwb-access contract mock returns the allow answer on the Decision log right R to the reader who holds RW-COE
    Given the rwb-case contract mock returns case "RW-2026-000501" in the reader's scope
    When the reader sends GET /api/recovery/decision/v1/decision-log/{entryId} for the entry and then GET /api/recovery/decision/v1/decision-log for case "RW-2026-000501"
    Then the single read carries decision code "D6", model version "MDL-SYN-PRIORITY 1.4.0", the reason "High cure score", the caller identity SY-AGENT, final call "PLACED MTG-BKK-PRI", the decided time, the previous hash and the entry hash
    Then the page of the case holds the same entry

  Scenario: AC4 One entry per placement, however often it is delivered (new, D-RCV-60)
    Given a decision record with decision code "D6" for case "RW-2026-000501" on queue "MTG-BKK-PRI" was recorded at 08:10
    When the same placement is delivered again at 08:11 and the caller sends the same placement again
    Then the ledger still holds one entry for case "RW-2026-000501" on queue "MTG-BKK-PRI"
    Then the repeated delivery is acknowledged and adds no chain link and consumes no chain sequence
    Then the refusal of the repeated request with 409 and MSG-P2-024 is rwb-case's and is not produced here

  Scenario: AC5 A record that names no version is refused and held (new, D-RCV-60)
    Given the rwb-integration contract mock returns the admission of caller "MDL-SYN-PRIORITY" for case "RW-2026-000501" on queue "MTG-BKK-PRI" with no model version and no agent version
    When the decision record of that placement arrives on rwb.decision-record.v1
    Then no entry is written and no chain sequence is consumed
    Then the delivery is held on the retry topic and then the dead-letter topic with MSG-P7-009 naming "versions"
    Then a task for the platform administration role names case "RW-2026-000501" and the missing field

  Scenario: AC6 A ledger write that fails loses no placement (new, D-RCV-60)
    Given the rwb-integration contract mock returns the admission of case "RW-2026-000501" on queue "MTG-BKK-PRI"
    Given the decision-record library mock refuses the append and raises its unavailable condition
    When the placement fact is delivered
    Then the delivery is retried on the retry topic and then held on the dead-letter topic
    Then an incident is raised under R-UNI-39 naming the case, the queue and the record key
    Then the owner's local record, the assignment and the case are unchanged, and the one missing central entry is visible to the platform administration role against that local record

  Scenario: AC7 A write that is not admitted leaves no entry (new, D-RCV-60)
    Given the rwb-integration contract mock returns no admission for case "RW-2026-000503", which has status CLOSED, and none for case "RW-2026-000504", which has deviation X2 open
    Given the rwb-integration contract mock returns no admission for caller "MDL-SYN-UNLISTED", and none for any caller while feature flag "rwb.casewf.queue-placement" is off
    When the ledger is read for the two cases and for the two refused paths
    Then no entry with decision code "D6" exists for case "RW-2026-000503", for case "RW-2026-000504" or for the refused paths
    Then MSG-P3-005, MSG-P2-021, MSG-P2-020 and MSG-P2-025 are produced by rwb-case and rwb-integration and this story produces none of them

  Scenario: AC8 The ledger is guarded by the Decision log right and the case scope (new, D-RCV-60)
    Given a decision record with decision code "D6" was recorded for case "RW-2026-000501"
    Given the rwb-access contract mock returns the refusal on the Decision log right R to a caller who holds Queue and allocation C only
    When the caller sends GET /api/recovery/decision/v1/decision-log/{entryId} for that entry
    Then the answer is 403 with MSG-P4-002 and nothing is returned
    When a reader who holds RW-COE sends the same read for a case outside their scope
    Then the rwb-case contract mock returns no case and the answer is 404 with MSG-P4-003

  Scenario: AC9 The entry names no approver and no approval level (new, D-RCV-60)
    Given the rwb-integration contract mock returns the admission of case "RW-2026-000501" on queue "MTG-BKK-PRI"
    When the placement fact is delivered once
    Then the entry carries the caller's reason as its recommendation field and the queue code "MTG-BKK-PRI" in its actions
    Then the entry holds no approver and no approval level

  Scenario: AC10 The event, the trail and the logs carry no personal data (new, D-RCV-60)
    Given the rwb-integration contract mock returns the admission of case "RW-2026-000501" on queue "MTG-BKK-PRI"
    When the placement fact is delivered once
    Then the DecisionRecorded event, the inbox row and the log entries carry case and queue references, a decision code, a caller identity, a version, a reason phrase and dates only
    Then none of them carries a name, an e-mail address, a mobile number, a national identity number or an account number

  Scenario: AC11 The approved callers list, the queue data, the matrix and the feature flag are not copied (new, D-RCV-60)
    Given the rwb-integration contract mock returns the admission of case "RW-2026-000501" on queue "MTG-BKK-PRI"
    When the placement fact is delivered once
    Then no table of this service holds a copy of the approved callers list, the queue data, the permission matrix or the feature flag
    Then the placement is read from the shared topic only and no call is made to rwb-case or rwb-access for those lists

  Scenario: AC12 A provided operation answers 401 when the caller is not authenticated (new, D-RCV-60)
    Given the rwb-access contract mock returns no authenticated identity for the caller of GET /api/recovery/decision/v1/decision-log/{entryId}
    When the caller sends that read without an authenticated service identity
    Then the answer is 401 and nothing is returned
```

These twelve criteria are new for the `rwb-decision` slice of RWB-E2-036 and are the ledger criteria of the key; every value in them is a legacy value of RWB-E2-036 sections 3, 4, 7, 8, 12 and 14 — case `RW-2026-000501` and its NEW status with no owner and no deviation, case `RW-2026-000503` CLOSED, case `RW-2026-000504` with deviation X2 open, queue `MTG-BKK-PRI` of team `MTG-BKK` with cap 150 and overflow `MTG-BKK-OVF`, caller `MDL-SYN-PRIORITY` of type MODEL for SY-AGENT at version 1.4.0, caller `MDL-SYN-UNLISTED`, the reason `High cure score`, matrix `PM-SIT-02`, the flag `rwb.casewf.queue-placement`, decision code D6, the final call `PLACED MTG-BKK-PRI`, R-UNI-39, and the messages MSG-P7-003, MSG-P7-009, MSG-P4-002, MSG-P4-003, MSG-P2-020, MSG-P2-021, MSG-P2-024, MSG-P2-025 and MSG-P3-005 — and no new business value is introduced; the chain sequence and the hash values are the seeded test state of FSD P7 v3 AC-ALT-P7-001-01 and AC-P7-006-01. `acs` is empty for this story: no legacy criterion is owned verbatim here, because every legacy criterion of the key either performs the placement, checks the admission or asserts the allocation engine, and all three belong to `rwb-integration` (P2) and `rwb-case` (P3).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every admitted placement leaves one entry in the central ledger, and no entry exists without a committed placement | Legacy BR5, BR6; REQ-CWC-018; NFR-078; CTL-06 |
| BR2 | The entry carries the decision code D6, a value of LOV-DECISION read with the version in force; the code is data and never a constant of the code | Legacy AC3; TSD P7 v2 T3.1 (DF-DEC-003); DP-07; ASM-4013 |
| BR3 | The entry names the model or agent version of the caller and the caller's service identity; an entry that names neither a model version nor an agent version is refused | Legacy BR5; AC3; NFR-078; TSD P7 v2 T7 |
| BR4 | The recommendation field holds the caller's reason and the actions hold the target queue code; the placement moves work and approves no treatment, so no approver and no approval level is written | Legacy AC3 and section 10 (no delegation of authority applies); TSD P7 v2 T3.1 (DF-DEC-009, DF-DEC-014) |
| BR5 | The final call is `PLACED <queueCode>`, read as reference data with the version in force; the queue code is the one on the placement, never a constant | Legacy AC3 ("PLACED MTG-BKK-PRI"); DP-07; ASM-4013 |
| BR6 | One entry per placement: the placement key and a unique key of the ledger make a second entry impossible, and a repeated delivery is acknowledged and writes nothing | Legacy AC7; R-UNI-40; TSD P7 v2 T3.1 (DF-DEC-031); ASM-4014 |
| BR7 | A placement the case side refused publishes no fact, so the ledger holds no entry: closed case, open deviation, unapproved caller, flag off, unknown queue or case | Legacy BR7, BR8; AC4, AC5, AC8, AC9, AC10 |
| BR8 | The entry is append only and hash chained: an entry hash over its canonical form, a previous hash equal to the entry hash before it, a sequence number that is never reused, and no update and no delete; a wrong entry is corrected by a new entry that names the one it corrects | REQ-DRI-002; TSD P7 v2 T3.1 (DF-DEC-017, DF-DEC-018, DF-DEC-028, DF-DEC-029); FSD P7 v3 A2.1 |
| BR9 | The entry, its chain link and its inbox mark commit in one transaction; a failure writes nothing, consumes no sequence and raises an incident under R-UNI-39 instead of discarding the delivery | Legacy BR6; R-UNI-39; NFR-077; DP-03; DP-09 |
| BR10 | The ledger is read under the Decision log right R and the caller's scope; the right is `rwb-access`'s to answer and the scope filter is applied to the case read of `rwb-case`; this service holds no role, no scope and no masking rule of its own | TSD P7 v2 T6.1 and T6.2; legacy sections 10 and 14 (MSG-P4-002, MSG-P4-003) |
| BR11 | No personal data in the entry, the event, the trail or the logs: case and queue references, a decision code, a caller identity, a version, a reason phrase and dates only | Template and Rules §R7.2 s17; legacy section 17; Architecture v5 slides 42 and 43 |
| BR12 | The approved callers list, the queue data, the matrix and the feature flag are the case and admission sides'; this story reads none of them and holds no copy | Legacy BR1, BR2, BR3, BR8; DP-06; DP-07 |

### 9. State transitions

The states below are the states of a ledger entry of this story. The case, the assignment, the queue and the caller admission are not state of this service and are named only so the boundary is visible.

| From | Event | Condition | To |
|---|---|---|---|
| Absent | A placement fact arrives for a committed placement, with a code and a final call of their lists and a version | The append writes the entry, the chain link and the inbox mark in one transaction | Appended, with a chain sequence, a previous hash and an entry hash |
| Absent | A fact arrives with no model version and no agent version, or with a value that is not of its list | The validation refuses the record | Absent: refused with MSG-P7-009 naming the field, the delivery held; no sequence consumed |
| Absent | The chain append, the insert or the inbox mark fails | The transaction rolls back | Absent: retried, then held with an incident under R-UNI-39; the chain at its last entry |
| Absent | The placement was refused by the case side | No fact is published | Absent, permanently |
| Absent | The same placement is delivered twice | The inbox mark and the placement key hold | Appended: unchanged, acknowledged once |
| Appended | A wrong entry must be corrected | A person decides the correction | Appended: a new entry with `corrects_entry_id` naming the wrong one; the wrong one stays |
| Appended | Any update or delete is attempted | Through the service role or the schema owner | Appended: refused, and the attempt is written to the ACE audit log |

The final call has one form on this path; a later call value is a new reference row and a new entry, never an update. The placement stays where `rwb-case` has it and the caller admission stays where `rwb-integration` has it.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-AGENT, agent platform | Places cases under its service identity once the matrix gives it Queue and allocation C and its caller is approved; the entry names it as the actor (legacy section 10) |
| SY-CASEWF, case workflow module | Places the case and writes its local record and the fact this story consumes; it writes nothing in `rwb_decision` |
| SY-DECLOG, decision log writer | The library identity that writes the entry, the chain link and the inbox mark in this service |
| RW-COE, center of excellence analyst | Reads the entry of a case in scope; requests a caller entry in the approved callers list (legacy section 10) |
| RW-RISK, risk and model risk officer | Approves a caller entry before it is loaded; reads the ledger under the Decision log right R |
| RW-TEAMMGR, team manager | Reads the entries of the cases in the team's queues (Decision log R) |
| RW-AUDIT and RW-COMPLY | Read the ledger for an audit or a regulatory request (Decision log R, NFR-036) |
| RW-PLATADM, platform administrator | Takes the task of a held record, reads the incident and switches the admission flag on after approval |
| The `rwb-decision` service identity | Writes its own `rwb_decision` rows, the chain link and the inbox mark, and reads the case through the P3 contract (the `rwb-decision` login, DP-02) |
| No approval level from the delegation of authority applies | A placement moves work; it does not approve a treatment (legacy section 10) |

The authorisation decision is `rwb-access`'s and is consumed as the authorise answer the read declares; the refusal shape stays 403 with MSG-P4-002 and 404 with MSG-P4-003. The database login is per service (DP-02) and its name is Not specified in the source documents (GAP-2412; ASM-4016).

### 11. Data

| BR Field ID | Entity in `rwb_decision` | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 | `decision_log_entry` | id | Write |
| DF-DEC-002 | `decision_log_entry` | case_id | Write, from the fact |
| DF-DEC-003 | `decision_log_entry` | decision_code | Write, the value D6 of LOV-DECISION |
| DF-DEC-004, DF-DEC-005 | `decision_log_entry` | rule_id, rule_version | Not written: a placement by a model or an agent is not a rule answer |
| DF-DEC-006 | `decision_log_entry` | model_version | Write, "MDL-SYN-PRIORITY 1.4.0" from the fact |
| DF-DEC-007 | `decision_log_entry` | agent_version | Write when the caller is an agent, empty when the caller is a model |
| DF-DEC-008 | `decision_log_entry` | inputs_ref | Write, the reference of the placement's input set carried on the fact |
| DF-DEC-009 | `decision_log_entry` | recommendation | Write, the reason "High cure score" |
| DF-DEC-010, DF-DEC-011 | `decision_log_entry` | approver_user_id, approval_level | Not written: a placement approves no treatment and no delegation of authority applies |
| DF-DEC-012 | `decision_log_entry` | final_call | Write, "PLACED MTG-BKK-PRI" |
| DF-DEC-013 | `decision_log_entry` | override_reason | Not written on this path |
| DF-DEC-014 | `decision_log_entry` | actions | Write, {"queueId", "queueCode", "callerType"} |
| DF-DEC-015 | `decision_log_entry` | outcome | Not written: the outcome of the placement is the case's |
| DF-DEC-016 | `decision_log_entry` | decided_at | Write, from the fact |
| DF-DEC-017, DF-DEC-018 | `decision_log_entry` | prev_hash, entry_hash | Write |
| DF-DEC-028 | `decision_log_entry` | chain_seq | Write |
| DF-DEC-029 | `decision_log_entry` | corrects_entry_id | Write only on an entry that corrects an earlier one |
| DF-DEC-030 | `decision_log_entry` | actor_user_id | Write, the caller's service identity |
| DF-DEC-031 | `decision_log_entry` | idempotency_key | Write, the placement key |
| DF-DEC-001 to DF-DEC-031 | decision record | all fields | Read through the two ledger operations of section 12.1 |
| DF-WRK-001, DF-WRK-002, DF-WRK-006, DF-WRK-007, DF-WRK-008 | `queue` in `rwb_case` | id, queue_code, assignment_method, capacity_cap, overflow_queue_id | Not read here: they are `rwb-case`'s and reach this story only as the queue code and the queue ID on the fact |
| DF-CAS-001, DF-CAS-005, DF-CAS-009, DF-CAS-010, DF-CAS-011, DF-CAS-019, DF-CAS-022 | `recovery_case` | id, status, owner_user_id, queue_id, team_code, deviation_open, closed_date | Read through the P3 case read, for the scope filter only |
| DF-WRK-009 to DF-WRK-016 | `assignment` | all fields | Not read here: the assignment is `rwb-case`'s and the fact names the owner only as its result |
| DF-REF-042, DF-REF-043 | `permission` | capability_area, letters | Not read here: the right is `rwb-access`'s answer |
| (inbox) | library table in `rwb_decision` | event_id, consumer, processed_at | Write |
| (outbox) | library table in `rwb_decision` | the outbox row | Not written: this story publishes nothing |

No row of `queue`, `assignment`, `recovery_case`, `delegation_limit`, `role`, `permission` or `masking_rule` is copied into `rwb_decision`: the case facts arrive on the P3 read for the scope filter, the right on the authorise answer, and the placement facts on the shared topic. Field IDs are those in the Logical Data Model and Data Dictionary v9.

### 12. Contract

Contract baseline. The placement operation POST /queues/{queueId}/placements is provided on the rwb-integration base with the four legacy body fields (caseId, reason, modelOrAgent, version), a required Idempotency-Key and the 201 answer of the legacy story. The case-base placement is consumed and owned by P3. The JSON element names of the consumed contracts are Not specified in the source documents (GAP-0671) until their owners publish them. The 24-hour replay window is the platform rule. A refusal carries one of RIGHT_NOT_HELD, CALLER_KIND or SCOPE_NOT_ALL with 403 and MSG-P4-002. The 422 and 503 codes keep MSG-GEN-001, MSG-GEN-002 and MSG-P7-003, and their code names are Not specified in the source documents (GAP-0958). A non-human caller is admitted on scope ALL only; any other scope is refused with SCOPE_NOT_ALL. The presented queue team code is recorded and compared with nothing. The caller code and type are recorded and not resolved to a role. The subject resolves through the role of the service identity at the matrix version in force, with the class check NON_HUMAN_ACTOR. The deviation hold is carried on DeviationRaised (EV-06) and DeviationCleared (EV-07); their element names are Not specified in the source documents (GAP-3102). The approved callers list, the matrix version, the overflow answer shape, the caller mapping, the login name and the legacy criteria are configuration, contract or deployment values held in the places named by GAP-0735, not in this story.

#### 12.1 REST operations provided

Owner `rwb-decision` (P7); base `/api/recovery/decision/v1`. The two reads are API-P7-006 and API-P7-007 of TSD P7 v2 T-A.1 and of the Ownership Map. The write of this story is not a REST operation: the record arrives as a fact on the shared topic of 12.4, because the legacy record must be written inside the placement's own transaction and that transaction is the owner's.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/decision-log` | API-P7-006: search the ledger by case, decision, rule, approver and date, one page at a time; the placement entry is found by case and decision code D6 | Decision log, right R, scope applied through the authorise answer and the case read of P3 | Not applicable, read only |
| GET | `/decision-log/{entryId}` | API-P7-007: read one entry with its inputs, its model or agent version, its caller, its final call and its two hashes | Decision log, right R, scope applied | Not applicable, read only |

Errors: 401 no session (messageId Not specified in the source documents (CG-ALL-7395)); 403 the caller holds no Decision log right (MSG-P4-002); 404 the entry or the case is absent or out of scope (MSG-P4-003); 503 the ledger is unavailable (MSG-P7-003). Every error is an RFC 9457 problem response with `messageId` set. The page and entry shapes are the API Specification v5 shapes of API-P7-006 and API-P7-007; the element names of the ledger read are Not specified in the source documents (GAP-2412; ASM-4013).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The owner, team, region and product group the scope filter of the ledger read is applied to; faked, one hop with a 2 s timeout |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The Decision log right R and the scope of the reader behind the two reads; faked, one hop |

The two operations are the P3 and P4 rows of the Ownership Map and of Architecture v5 slides 14 and 41, and their request and answer shape is Not specified in the source documents (GAP-2412; ASM-4013). The reference-data read of DP-07 for LOV-DECISION and the final-call list is consumed through its client library; no source this story may read gives its operation path, so it is carried in GAP-2412. The case placement and the admission contract of RWB-P2-E2036-CON are not called here: they shape the fact and are consumed as its contract, not as a call.

#### 12.3 Events published

None. This story writes the central entry and publishes no fact of its own; the `DecisionRecorded` event of the placement is published by the owner of the local record in its own transaction, and this service acknowledges it on its inbox. The outbox objects in `rwb_decision` stay for the slices that publish from this service.

#### 12.4 Events consumed

| Event | Topic | Owner of the event | Key | Use in this story |
|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 owns the event type; the placement instance is published by its local record's owner (`rwb-case` for the placement, `rwb-integration` for the admission) | entryId | The facts of one admitted placement: case, decision code D6, model or agent version, inputs reference, reason, caller identity, queue and queue code, decided time and the placement key |

The delivery is consumed once through the inbox of DP-09, in the CloudEvents 1.0 envelope, with the retry and `.dlt` topics of the shared subscription; a repeat is acknowledged and writes nothing (X3). This story filters on decision code D6 and leaves every other fact of the topic to the slices that own it. No event carries a name, an e-mail address, a mobile number, a national identity number or an account number.

#### 12.5 Workflows and activities

None of this story's own. The append is one synchronous step inside the consuming transaction, not a workflow or an activity. `rwb-decision` holds `ApprovalWorkflow` of the workflow kit, the rule promotion JOB-13 and the chain check JOB-14 for other slices; this story starts no workflow, signals none, and registers no activity on the `rwb-decision` queue.

#### 12.6 Schedules

None. The chain check JOB-14 at 02:00 and the rule promotion JOB-13 belong to other slices of this service and run on their own Temporal Schedules; this story adds neither and polls nothing.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `decision_log_entry` | P7 (`rwb_decision`) | The placement entry: the code, the version, the inputs reference, the reason, the caller, the final call, the queue, the decided time, the hashes and the chain sequence; written once and read |
| inbox library table | PLT library, created in `rwb_decision` | The processed mark of one delivery (DP-09) |

Not owned and never read by this story: `queue`, `assignment`, `recovery_case` and the local `decision_record` (P3), `delegation_limit`, `role`, `permission` and `masking_rule` (P4), `agent_policy` and `agent_run` (P10), and the ACE views (P1). No foreign key crosses a schema and no row of another service is copied (DP-01). The `approval`, `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` tables are this service's but another story's, and this story writes none of them.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| admission and placement fake | RWB-P2-E2036-CON | The admitted placement of caller `MDL-SYN-PRIORITY` version "1.4.0" for case `RW-2026-000501` on queue `MTG-BKK-PRI` with reason "High cure score" under SY-AGENT; the same placement with no version; the placement of case `RW-2026-000502` into overflow `MTG-BKK-OVF` with no owner; case `RW-2026-000505` transferred with an owner; the refusals of cases `RW-2026-000503` and `RW-2026-000504`, of caller `MDL-SYN-UNLISTED` and of the flag-off run; the request journal for the repeat and ordering assertions |
| rwb-case case read fake | The P3 case read | Case `RW-2026-000501` in scope with owner, team, region and product group; a case outside the reader's scope; the reference-data answer for LOV-DECISION and the final-call list (DP-07) |
| rwb-access fake | The P4 authorise call | The allow answer on the Decision log right R for the RW-COE reader and the refusal for a caller who holds Queue and allocation C only (MSG-P4-002) |
| decision-record fake | RWB-PLT-E1027-CON | The append, the chain sequence allocation and the hash link; a seeded ledger of 100 entries and the chain verifier; a forced failure and an unavailable condition for AC6 and TC-E2-036-14 |

Each fake is replaced by the real service as its contract lands, without a change to the criteria. The decision-record fake stands only for the chain and the failure tests, because the library is the service's own DP-03 baseline.

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2, consumed 2 | `GET /decision-log` and `GET /decision-log/{entryId}` provided; the case read and the authorise call consumed, one hop each with the 2 s timeout |
| Kafka | Published 0, consumed 1 event type | `rwb.decision.DecisionRecorded.v1` consumed from `rwb.decision-record.v1` through the inbox; nothing published |
| Temporal | None | No workflow, no activity and no Schedule registered; JOB-13 and JOB-14 stay with their owners |
| File | None | No file input and no file output |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `ledger/queueplacement`, Java package `th.co.scb.ace.workbench.recovery.decision.queueplacement`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_decision`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/decision/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 and DP-09 are the core of the slice: the legacy `DecisionLogWriter` call inside the placement transaction becomes the owner's local record plus the shared topic, and this service consumes that fact through its inbox into the central ledger, so the entry, its chain link and the inbox mark commit together. DP-14 fixes the topic name and the CloudEvents envelope, and DP-07 is where the decision code D6 and the final-call list live, read with the version in force and never as constants here. DP-08 is the guard library and the authorise contract behind the two reads. DP-11 is the one hop on the case read; DP-01 keeps the entry in `rwb_decision` alone; DP-13 and DP-19 put the two reads on the service base behind the composite route, and this story adds no route and serves no screen. DP-15 is the per-service Flyway sequence of the one migration below.

The platform H rows of the table (H RWB-PLT-E1027-CON, H RWB-PLT-E1043-CON, H RWB-PLT-E1037-CON, H RWB-PLT-TE006-CON, H RWB-PLT-E1047-CON, H RWB-PLT-E1044-CON, H RWB-PLT-N001-CON) and the two C rows DP-07 and DP-08 bring (C RWB-P3-E1043-CON, C RWB-P4-E1037-CON) are not in the metadata rows, which copy the story line (`H` empty, `C` = RWB-P2-E2036-CON); they are recorded in GAP-2412 and ASM-4015. None blocks the build beyond Day 1: they are platform contracts of wave 0 and published contracts of another service.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| PlacementRecordListener | Listener | Consumes `DecisionRecorded` on the shared topic, filters on decision code D6, drives the inbox mark, and maps a refused record to the held path |
| PlacementRecordValidation | Service | Reads LOV-DECISION and the final-call list with the version in force, and refuses a code, a final call or a missing version with MSG-P7-009 |
| ChainWriter | Service | Reads the head of the chain under the append lock, computes the entry hash over the canonical form and builds the previous hash and the sequence number |
| PlacementRecordAppendService | Service | One transaction: the entry, the chain link and the inbox mark, or nothing; maps the failure to the incident of R-UNI-39 |
| DecisionRecordRepository | Repository | `decision_log_entry` in `rwb_decision`, with the unique key of the chain sequence, of the placement key and of the inbox delivery |
| DecisionRecordQueryService | Service | The ledger page and the single entry, with the scope filter applied to the case read |
| AccessCheckClient, CaseScopeClient | Client | The authorise answer of the Decision log right and the P3 case read behind the two reads |

**Database and migrations**

- Writes `decision_log_entry` and the inbox objects of the library, all in schema `rwb_decision`; reads no other schema.
- The `decision_log_entry` baseline, its append-only trigger, its grants and its chain-sequence unique key belong to the decision-log store slice of this service (legacy RWB-E1-008) and are not rebuilt here.
- Migration in this story, in the per-service Flyway sequence of DP-15: `V2036_1__decision_queue_placement.sql` adds the unique key `ux_declog_placement ON decision_log_entry (idempotency_key) WHERE idempotency_key IS NOT NULL`, the index `ix_declog_case_decided ON decision_log_entry (case_id, decided_at)` for the page of one case, and the check that a D6 entry carries a model version or an agent version.
- No row is updated and no row is deleted by this story; the store has no update path and no delete path.

**Configuration and reference data**

- LOV-DECISION with the code D6 and the final-call list with `PLACED <queueCode>` are read through the reference-data contract of DP-07 with the version in force; neither is a constant in code (ASM-4013).
- The approved callers list, the queue data with its method, cap and overflow queue, and the permission matrix are rows of `rwb-case` and `rwb-access` and are not read or written here (DP-06, DP-07).
- The feature flag `rwb.casewf.queue-placement` stays with RWB-P2-E2036-APP and never gates the ledger: a placement that committed always writes its entry (ASM-4012).
- The `rwb-decision` login of DP-02, the Flyway user and the topic subscription values are environment configuration and not values of this story.

**Build steps**

1. The migration `V2036_1__decision_queue_placement.sql`; test that a repeated placement key and a D6 entry without a version are refused (BR3, BR6).
2. `ChainWriter` with the head read, the canonical form and the entry hash; test the seeded chain of 100 entries and the first-entry case of 64 zeros (AC2).
3. `PlacementRecordValidation` with the two lists of DP-07 and the version guard; tests for AC1, AC5 and X4.
4. `PlacementRecordAppendService` and the fail-closed transaction; tests for AC1, AC2, AC6 and TC-E2-036-14.
5. `PlacementRecordListener` with the inbox, the retry and `.dlt` topics and the D6 filter; tests for AC4 and the held paths of AC5 and AC6.
6. `DecisionRecordQueryService` with the authorise answer, the scope filter and the page; tests for AC3, AC8 and TC-E2-036-13.
7. The absence tests: closed case, open deviation, unapproved caller, flag off and unknown queue leave no entry (AC7).
8. The privacy test: the entry, the inbox row and the log entries carry no name, e-mail address, mobile number, national identity number or account number (AC1).

**Done when.** The tests in section 16 pass, the contract tests of RWB-P2-E2036-CON stay green, and a SIT day shows one D6 entry per admitted placement with the version `MDL-SYN-PRIORITY 1.4.0` and the final call `PLACED MTG-BKK-PRI`, a chain that verifies from its first entry, one entry for a repeated delivery, no entry for a refused placement, an incident and no lost placement when the ledger cannot be written, and no personal data in any entry or log.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P7-009 | The decision code, the final call or the model or agent version is not a value it must have | Not specified in the source documents (GAP-2412; ASM-4017) | This story, on the validation; FSD P7 v3 names only the identifier and the field |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on the append transaction and the incident |
| MSG-P4-002 | The caller holds no Decision log right | You cannot {action} here. Your role does not include it. | This story, through the authorise answer |
| MSG-P4-003 | The entry or the case is outside the reader's scope, or the queue or case is unknown | This case is not in your scope. | This story, through the authorise answer and the case read |
| MSG-GEN-001 | A required field of the request is empty | Enter {field}. | `rwb-integration`, on the admission |
| MSG-GEN-002 | reason or version outside its length | {field} must be between {min} and {max}. | `rwb-integration`, on the admission |
| MSG-P2-020 | The caller is not in the approved callers list | {caller} is not approved to place cases on queues. | `rwb-integration`, on the admission |
| MSG-P2-021 | The case has an open deviation | This case has an open deviation and stays with the deviation handler. | `rwb-case`, on the placement |
| MSG-P2-024 | The case is already in the target queue | This case is already in {queue}. | `rwb-case`, on the placement; this story writes no second entry |
| MSG-P2-025 | The feature flag is off | Queue placement by models and agents is switched off. | `rwb-integration`, on the admission |
| MSG-P3-005 | The case is closed | This case cannot move to {state} from {current}. | `rwb-case`, on the placement |
| MSG-GEN-004 | The case changed during the placement | Someone else changed this record. Reload it to see their change. | `rwb-case`, on the placement |

Every message except MSG-P7-009 is copied unchanged from the legacy story RWB-E2-036 section 14; MSG-P7-009 is named by FSD P7 v3 A2.2.4.3 and A2.3.4.2 and its text is not written out in any source this story may read, so the placeholder stands under ASM-4017. Thai text for each message follows decision DL10, which is open; its assumptions are ASM-2250, ASM-2357, ASM-2377 and ASM-2863.

### 15. Screens and states

No screen is built in this story. The placed case appears in its queue on SCR-07 Team queues and SCR-02 Case list like any other case, and those screens are other stories'. The entry is shown by SCR-38 Decision log query, which is the decision-log query slice of this service and not this story, reached through the composite route of DP-19; this story adds no route and renders nothing.

| Where | State | What the reader sees |
|---|---|---|
| The shared topic, one delivery | Accepted | One inbox mark, one entry, one chain link; nothing on a screen |
| The shared topic, a record with no version or a value out of its list | Held | The retry topic and then the dead-letter topic, MSG-P7-009 and a task for the platform administration role |
| The shared topic, the append fails | Held | The retry topic, an incident under R-UNI-39, no entry and no sequence consumed |
| The shared topic, a repeated delivery | Acknowledged | The first entry unchanged; no new chain link |
| `GET /decision-log` | One page | The entries of a case in scope with code D6, version, final call and decided time |
| `GET /decision-log/{entryId}` | One entry | Code D6, the model or agent version, the reason, the caller identity, final call `PLACED MTG-BKK-PRI`, decided time, previous hash and entry hash |
| `GET /decision-log`, `GET /decision-log/{entryId}` | 403 or 404 | MSG-P4-002 for a caller without the right, MSG-P4-003 for an entry out of scope |
| SCR-02 Case list | Empty | As Screen Specifications v1, section SCR-02 |
| SCR-02 Case list | Loading | As Screen Specifications v1, section SCR-02 |
| SCR-02 Case list | Error | Not specified in the source documents (CG-ALL-7402) |
| SCR-02 Case list | No access | Not specified in the source documents (CG-ALL-7402) |
| SCR-07 Team queues | Empty | Not specified in the source documents (CG-ALL-7403) |
| SCR-07 Team queues | Loading | As Screen Specifications v1, section SCR-07 |
| SCR-07 Team queues | Error | Not specified in the source documents (CG-ALL-7403) |
| SCR-07 Team queues | No access | Not specified in the source documents (CG-ALL-7403) |
| SCR-38 Decision log query | Empty | Not specified in the source documents (CG-ALL-7404) |
| SCR-38 Decision log query | Loading | As Screen Specifications v1, section SCR-38 |
| SCR-38 Decision log query | Error | Not specified in the source documents (CG-ALL-7404) |
| SCR-38 Decision log query | No access | Not specified in the source documents (CG-ALL-7404) |

The screen field list, the composite route specification and the field-level masking belong to RWB-PLT-N001-CON and to the stories that own each screen.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-036-01 | AC1, BR1, BR2, BR3 | Contract | Admitted placement of caller `MDL-SYN-PRIORITY` version "1.4.0" for case `RW-2026-000501` on `MTG-BKK-PRI`; one D6 entry with the caller SY-AGENT and final call `PLACED MTG-BKK-PRI` |
| TC-E2-036-02 | AC1, BR5 | Contract | Owners at 150 and 149, then both at 150; the entry of the first placement carries `MTG-BKK-PRI` and the entry of the overflow placement carries `MTG-BKK-OVF` with no owner in the fact |
| TC-E2-036-03 | AC2, BR8, BR9 | Component | One placement; the entry, its chain link and the inbox mark in one transaction, with the code, version, reason, caller and final call checked |
| TC-E2-036-04 | AC7, BR7 | Component | Flag `rwb.casewf.queue-placement` off; no admission, no fact and no entry |
| TC-E2-036-05 | AC7, BR7 | Component | Caller `MDL-SYN-UNLISTED`; no admission, no fact and no entry |
| TC-E2-036-06 | AC7, BR7 | Component | Admission with no reason; no fact and no entry |
| TC-E2-036-07 | AC4, BR6 | Component | The same placement delivered twice; one entry and the first entry returned |
| TC-E2-036-08 | AC7, BR7 | Component | Case `RW-2026-000503` CLOSED; no fact and no entry |
| TC-E2-036-09 | AC7, BR7 | Component | Case `RW-2026-000504` with deviation X2 open; no fact and no entry |
| TC-E2-036-10 | AC7, BR7 | Component | A queue ID that does not exist; no fact and no entry |
| TC-E2-036-11 | AC4, BR6 | Component | Two placements of one case against one version; one commits and one entry exists |
| TC-E2-036-12 | AC1, BR3 | Contract | Case `RW-2026-000505` IN_PROGRESS with owner "U-5100", placed on `MTG-BKK-PRI`; the entry carries the new queue and the new owner in the fact |
| TC-E2-036-13 | AC8, BR10 | Component | A caller holding Queue and allocation C only reads the entry; 403 with MSG-P4-002 |
| TC-E2-036-14 | AC6, BR9 | NFR | The ledger append forced to fail; 503 MSG-P7-003 to the owner, the delivery held, the incident raised, the entry absent and the placement unchanged |
| TC-E2-036-15 | AC3, BR2, BR3 | Component | Admitted placement of caller `MDL-SYN-PRIORITY` version "1.4.0" for case `RW-2026-000501` on `MTG-BKK-PRI`; one D6 entry with the model version, the reason `High cure score`, the caller and the final call `PLACED MTG-BKK-PRI` |
| TC-E2-036-16 | AC5, BR3 | Component | A D6 entry with no model version and no agent version; refused, no entry written |
| TC-E2-036-17 | §12.7, DP-01 | Component | The migration and the writes of this story touch only `decision_log_entry` and the inbox table in `rwb_decision`; no other schema or table is read or written |
| TC-E2-036-18 | AC9, BR4 | Component | Admitted placement of case `RW-2026-000501` on `MTG-BKK-PRI`; the entry holds the reason as recommendation and the queue code in actions, with no approver and no approval level |
| TC-E2-036-19 | AC10, BR11 | Component | Admitted placement; the event, the inbox row and the log entries checked for personal data; none present |
| TC-E2-036-20 | AC11, BR12 | Component | Admitted placement; the ledger write and read make no call to the approved callers list, queue data, matrix or flag and hold no copy of them |
| TC-E2-036-21 | AC12 | Component | Not specified in the source documents (NEWAC-RWB-P7-E2036-APP-AC12) |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to Component or Contract as the row shows, Access to Component and Resilience to NFR. The whole legacy set is kept because this slice carries the record of every placement of the key; the tests whose reading lives in `rwb-integration` or `rwb-case` assert this story's entry through the contract fake for the rest. The `-ITG` copies of the same cases are RWB-ITG-W2-ITG and are not written here.

The composite placement route path and merge order, the harness repository, the SIT environment, the seeded callers and queues, the evidence format and retention, and the pass/fail gate are held as data in the harness pack, not in this story (GAP-0419).

### 17. Guardrails

- No business value in code: the decision code, the final-call form, the queue code, the cap, the matrix and the caller list are reference-data or parameter rows; nothing of them is a constant here.
- No personal data in the entry, the inbox row, the trail, the tests or the logs: case and queue references, a decision code, a caller identity, a version, a reason phrase and dates only (legacy section 17).
- No read of another service's tables (DP-01): the case arrives on its read, the right on the authorise answer and the placement facts on the shared topic; no `queue`, `assignment`, `recovery_case`, `decision_record`, `delegation_limit`, `role` or `permission` row is copied into `rwb_decision`.
- ACE data only through the owner's contract or `v_ace_*` views: this story reads no ACE data at all.
- One recorder and no mover: this story changes no case, no queue, no assignment and no caller admission, and it never places a case itself.
- No entry without its chain link and no delivery without its inbox mark: the append is one transaction, and a failure changes nothing and raises an incident instead of discarding the delivery (R-UNI-39).
- Append only and hash chained: no update path and no delete path exist, the sequence number is never reused, and a wrong entry is corrected by a new entry naming the one it corrects (REQ-DRI-002).
- One entry per placement: the placement key and the unique key make a second entry impossible, and a repeated delivery is acknowledged and writes nothing.
- One base, one topic, one queue: `/api/recovery/decision/v1`, `rwb.decision.events.v1` and `rwb-decision` in namespace `rwb-recovery`, with the shared topic `rwb.decision-record.v1` for the record facts; no story in this key declares another service's base or topic as its own (DP-13).
- One hop and 2 s on the case read and the authorise call, with a breaker per downstream; a missing answer never produces an entry from a guessed case or a guessed right.
- A model or an agent never bypasses the allocation engine or the access check: the entry records the placement that those checks allowed, and it never authorises one (legacy section 17).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-017 | A queue accepts a write from a model or an agent with the case and the reason | Business Requirements Epic 2, section 3.2 | FEAT-CWC-29 | All recovery processes | R-DEV-01 | TC-E2-036-01, TC-E2-036-02, TC-E2-036-03, TC-E2-036-12, TC-E2-036-15 |
| REQ-CWC-018 | The write passes the same permission checks and is logged with the model or agent version | Business Requirements Epic 2, section 3.2 | FEAT-CWC-29 | All recovery processes | R-UNI-39 | TC-E2-036-03, TC-E2-036-13, TC-E2-036-14, TC-E2-036-16 |
| REQ-CWC-019 | The interface ships behind a feature flag | Business Requirements Epic 2, section 3.2 | FEAT-CWC-29 | All recovery processes | None | TC-E2-036-04, TC-E2-036-05 |
| REQ-CWC-020 | Model work and rule work sit in one queue in one priority order | Business Requirements Epic 2, section 3.2 | FEAT-CWC-29 | All recovery processes | None | TC-E2-036-01, TC-E2-036-02 |
| REQ-ACA-010 | Agents run under service identities and are subject to the same role checks as people | Business Requirements Program, section 5.4 | FEAT-CWC-29 | All recovery processes | R-UNI-39 | TC-E2-036-01, TC-E2-036-13 |

| Legacy reference | Where it is kept |
|---|---|
| One decision log entry per placement, with decision code D6, the model version, the reason, the caller identity and the final call | Sections 1, 2, 4, 7 (AC1, AC3), 8 (BR2 to BR5) |
| The entry in the same transaction as the change, and no placement without a record | Sections 2, 4, 5 (X2), 7 (AC6), 8 (BR9), 13 (DP-03) |
| One placement per case and queue; a repeat writes no second entry | Sections 5 (X3), 7 (AC4), 8 (BR6), TC-E2-036-07 |
| The record obligation of NFR-078 and the model or agent version | Sections 7 (AC1, AC5), 8 (BR3), 11, 14 |
| Refused placements (closed case, open deviation, unapproved caller, flag off, unknown queue) | Sections 5 (X7), 7 (AC7), 8 (BR7), 14 |
| MSG-P4-002, the Decision log right and the scope | Sections 5 (X5, X6), 7 (AC8), 10, 14 |
| Case `RW-2026-000501`, queue `MTG-BKK-PRI` with cap 150 and overflow `MTG-BKK-OVF`, caller `MDL-SYN-PRIORITY` 1.4.0, reason `High cure score`, final call `PLACED MTG-BKK-PRI` | Background and scenarios of section 7; sections 3 and 11 |
| Legacy key RWB-E2-036, story RWB-P7-E2036-APP, contract RWB-P2-E2036-CON | Metadata, sections 3 and 12 |
| Test cases TC-E2-036-01 to TC-E2-036-21 | Section 16 |
| Decoupling patterns DP01, DP03, DP07, DP08, DP09, DP11, DP13, DP14, DP15, DP19 | Metadata, section 13 |

The other slices of the key answer the rest: RWB-P2-E2036-APP and RWB-P2-E2036-CON the caller-facing operation, the approved callers list, the flag, the validation and the error mapping; the placement, the allocation, the cap and the overflow are `rwb-case`'s (P3); the rights, the scope and the masking are `rwb-access`'s (P4); RWB-ITG-W2-ITG the cross-service harness and the `-ITG` copies of the test cases.

### 19. Out of scope

- The caller-facing operation on the integration base, the approved callers list, the feature flag `rwb.casewf.queue-placement`, the request validation, the forwarding and the error mapping: RWB-P2-E2036-APP and RWB-P2-E2036-CON.
- The placement, the queue's assignment method, the caseload cap, the overflow queue, the assignment row and the local decision record of the placement transaction: `rwb-case` (P3) and its queue and allocation stories.
- The right, the scope, the permission matrix, the approved caller approval step and the masking policy: `rwb-access` (P4) and `rwb-case`; this story consumes their answers and holds no rule of them.
- The model or the agent that calls the interface: the `rwb-agent` stories (P10), for example RWB-E2-028 of the legacy set.
- The decision-log store of this service — the append-only trigger, the grants, the chain verifier and the daily chain check JOB-14 at 02:00: the decision-log store slice (legacy RWB-E1-008) and the service baseline.
- Building or training a model, its score and the queue order by priority (REQ-CWC-020): the model owner and the queue order story, outside this slice.
- The approval routing, `ApprovalWorkflow`, the rule package registry, the rule promotion JOB-13 and the decision center screens SCR-10, SCR-11 and SCR-38: the other slices of `rwb-decision`.
- The integration harness and the `-ITG` copies of the test cases: RWB-ITG-W2-ITG.
- The ACE DB story, the infrastructure story and the deployment story of this legacy key: their own DB, INF and OPS stories; the Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability are the OPS story's.

The release 31 December 2026 is copied unchanged from the legacy story and stays tentative; no date is changed by this story.
