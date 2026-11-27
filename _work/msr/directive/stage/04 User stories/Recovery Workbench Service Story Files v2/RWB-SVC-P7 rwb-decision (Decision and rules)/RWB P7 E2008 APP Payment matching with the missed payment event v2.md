# RWB-P7-E2008-APP Payment matching with the missed payment event

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E2008-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P7-V |
| Ready to start | Day 1 |
| Size | To be sized by the squad at refinement |
| Contract version | v1 (path /api/recovery/decision/v1) |
| Depends on (build) | None |
| Contract dependencies | RWB-P8-E2008-CON, RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to REQ-CHO-007, REQ-CHO-009); served requirement REQ-S4-010 (enforcement proceeds) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the rwb-decision slice of RWB-E2-008 — the `PAYMENT_MATCH` row set that decides the match, the collection of every match and missed-payment decision record into the central ledger, the append-only hash chain, the refusal of a record that names no rule version, the read that names `R-RES-26` and the package version, and JOB-14 — is split from the payment engine (rwb-payment, RWB-P8-E2008-APP), the contract (RWB-P8-E2008-CON), the treatment plan (rwb-treatment), the ACE reads (rwb-source-data) and the deployment (RWB-P8-E2008-OPS). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P7-E2008-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (23 resolved, 49 cross-document, 8 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **center of excellence analyst (RW-COE), an internal audit officer (RW-AUDIT) and the rwb-decision service that decides the match**, I want **package `PAYMENT_MATCH` version `PM-2026.12` in force with its `EXACT` row as data — amount tolerance 0 percent, window 10 days before the due date and 0 days after, grace 0 days — every match and every missed-payment decision record of the daily run collected from the shared topic into one append-only, hash-chained central ledger that names decision code `D5`, rule `R-RES-26` and the package version, a record that names no version refused rather than defaulted, and JOB-14 checking the chain at 02:00**, so that **a broken plan is still known the day after it breaks and every match can be explained from one read — which rule fired, under which approved package version, in which order and unchanged since**.

Inside `rwb-decision` this is the decision and record half of RWB-E2-008:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1`, Temporal task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`, and the shared topic `rwb.decision-record.v1` (DP-03).
- The decision: the version of package `PAYMENT_MATCH` in force on the business date and the `EXACT` row it decides with, held as `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` rows (DP-01, DP-04). No rule value — tolerance, window, grace, match type — is a constant of this service or of the consuming one.
- The record: one `decision_log_entry` per match and per missed payment, collected from `rwb.decision.DecisionRecorded.v1` and appended after the owning service wrote its local record, with `chain_seq`, `prev_hash` and `entry_hash`, decision code `D5`, rule `R-RES-26`, the package version, an inputs reference, the final call, the actor and the decided time (DP-03, DP-09).
- The gate: a record whose rule version is empty is refused with MSG-P3-027 and parked on the retry topic; no default version is ever substituted.
- The read: `GET /decision-log` and `GET /decision-log/{entryId}` answer the match records by case, decision, rule, approver and date range, with the rule, the version and both hashes — the read SCR-38 Decision log query uses and the one the audit of a match starts from.
- The run control: JOB-14 hash chain check as a Temporal Schedule at 02:00 on queue `rwb-decision` (DP-10), which verifies the whole chain and reports a break to Compliance the same day.

It does not own: JOB-07, the ACE facts, the running plans, the match itself, the proceeds row, the treatment installment update, the exception list, the run summary and the `ProceedsMatched` (EV-25) and `PaymentMissed` (EV-12) events, which are rwb-payment's (RWB-P8-E2008-APP); the two operations, the event schemas, the error model and the fakes, which are RWB-P8-E2008-CON; the load, approval, promotion and rollback of the package, which are RWB-P7-E2027-APP with the authoring pipeline RWB-P7-E1073-APP; the store's own DDL and writer, which are RWB-P7-E1008-APP and RWB-PLT-E1027-CON; the plan state `PLAN_RUNNING` to `PLAN_CURE_PERIOD` under R-RES-27, which is rwb-case's; and the deployment of this build, which is outside this story.

The legacy facts are carried unchanged: case `RC-2026-000555`, account `A-0555`, plan `T-0701` at 12,500.00 THB due 2026-12-15, business date 2026-12-14, payments `PAY-90001` to `PAY-90005`, package `PM-2026.12`, rule `R-RES-26` and decision code `D5`. The boundary between a record "written locally by the owner" and "sealed centrally" is fixed by this story as an assumption (GAP-2493; ASM-4127).

### 2. Business rationale

Payment matching is package `PAYMENT_MATCH` under ADR-012, fixed by D-RCV-36 T10: the `EXACT`, `PARTIAL` and `WINDOW` rows carry match type, tolerance, window, grace and partial floor as decision-table columns, and the decision log names rule `R-RES-26` with the package version. In the monolith the rule was a table read by the matching class and the match was written into the same schema as the rule and the log, so a threshold could move under a decision already taken and no reader could prove what decided a match.

D-RCV-60 separates the three halves. rwb-payment owns the money row and the run (RWB-P8-E2008-APP); rwb-decision owns the rule set and the proof. Governance is central and evaluation is local (Arch v5 slide 27; ADR-017): the registry publishes the version in force, the owning service evaluates it, and the decision record of every evaluation is written in the owner's transaction and then collected into the central ledger of rwb-decision, where it is appended, hashed and checked nightly by JOB-14. That is the shape the Temporal and Drools design gives the record: "written by the owning service in its own schema, in the same transaction as the state change, then collected into the central ledger in rwb-decision ... JOB-14 checks the chain at 02:00".

Without this story the package has no in-force answer and no test-case set, the match decisions of a business date exist nowhere after the payment service's own schema is rotated, and the two questions an audit asks of every match — which rule fired, under which approved version — have no answer that survives the day. It serves REQ-CHO-007 and REQ-CHO-009 on the decision side and carries R-UNI-40 and R-UNI-41: one record per decision, and no version in force is a refusal and never a default.

The realignment changes the mechanism, not the business rule: the single recovery schema becomes `rwb_decision` (DP-01); the central `DecisionLogWriter` becomes the local record library plus the collector of this story (DP-03); the in-process `RuleEvaluator` and the rule table become the embedded kit and the package rows (DP-04); the Quartz chain check becomes JOB-14 on the workflow kit (DP-10); the monolith base becomes `/api/recovery/decision/v1` (DP-13); and the nightly copy to the data lake is gone, because rwb-reporting reads events (DP-17, out of scope here).

### 3. Preconditions

- RWB-P8-E2008-CON is published: the decision record a match and a missed payment write — decision code `D5`, rule `R-RES-26`, the package version, the inputs reference and the entry ID — with its fake and the drift test (DP-11, DP-13). The payload names below the three field names the legacy story gives are Not specified in the source documents (GAP-2494; ASM-4128).
- Package `PAYMENT_MATCH` is loaded, tested, approved and `IN_FORCE` from 2026-12-01 with version `PM-2026.12` and its `EXACT` row: amount tolerance 0 percent, window 10 days before the due date and 0 days after, grace 0 days (legacy sections 3 and 7; the two values the legacy story marks assumed stay assumed, DL25). The rows arrive from RWB-P7-E2027-APP; this story reads them and writes none of them.
- The `rwb_decision` baseline exists with `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` and `decision_log_entry` — `chain_seq`, `prev_hash`, `entry_hash`, the append-only trigger `tr_declog_append_only`, the first `prev_hash` of 64 zeros — plus the outbox, inbox and idempotency objects of DP-09 and the per-service login (DP-02). The login name is Not specified in the source documents (GAP-2497; ASM-4038).
- RWB-PLT-E1027-CON publishes the local decision-record library and the shared topic `rwb.decision-record.v1` with its CloudEvents writer; RWB-PLT-TE006-CON publishes the inbox and outbox library with the consumer-group registry, the `.retry` and `.dlt` topics and the dedupe key (DP-03, DP-09).
- RWB-PLT-E1072-CON publishes the embedded Drools kit with its checksum and first-match semantics; it is used here to read the compiled row set of a version and to run its test cases, never to evaluate a payment (DP-04).
- RWB-PLT-E1071-CON publishes the workflow kit with a Temporal Schedule, so JOB-14 exists as a Schedule on queue `rwb-decision` (DP-10).
- RWB-PLT-E1042-CON and RWB-PLT-E1043-CON publish the parameters and reference-data clients, and RWB-P3-E1042-CON and RWB-P3-E1043-CON the operations behind them: LOV-DECISION with code `D5` and the version-state list, plus the input age limit of FSD P7 VR-P7-001-3 (DP-06, DP-07). The parameter key of that limit is Not specified in the source documents (GAP-2494; ASM-4128).
- RWB-PLT-E1044-CON publishes the per-service Flyway sequence, its lint and its drift gate, so the one migration of section 13 is a numbered migration of `rwb_decision` (DP-15).
- RWB-PLT-N001-CON publishes the gateway-bff composite route that serves SCR-38 Decision log query, one hop, 2 s (DP-19).
- RWB-P7-E1073-CON (DP-04) and RWB-P4-E1037-CON are consumed contracts: the build runs against their fakes from Day 1, and the operation each publishes is Not specified in the source documents (GAP-2496); step D1 decides whether they enter the dependency map.
- The rwb-access fake answers `GET /me/session` for RW-AUDIT holding Decision log R, RW-COE holding Rules and parameters C and Decision log R, and a role without Decision log R that is refused with MSG-P4-002.
- Synthetic data only: package codes, version labels, rule IDs, entry IDs, payment codes and dates of the legacy story; no real account, customer or payment in a test, a log or an event (legacy section 17).

### 4. Flow

1. `RuleSetReader` reads the `PAYMENT_MATCH` package and the version in force for the business date through `RuleVersionRepository`, with the `EXACT` row at row order 1 and its columns: match type, amount tolerance 0 percent, window 10 days before the due date and 0 days after, grace 0 days. No tolerance, window or grace value exists in the code or in the configuration of this service (BR2).
2. The version's `rule_test_case` set is read with its expected and actual result, including the two boundary cases of the legacy window: `PAY-90004`, 10 days before its due date 2026-12-15, expected `MATCH` on row `EXACT`, and `PAY-90005`, 11 days before its due date 2026-12-16, expected `UNMATCHED`.
3. `RuleVersionController` answers the package list, the version list of the package and the dry-run result of a version to the roles of section 10. These are reads: this story loads, approves, promotes and rolls back nothing (RWB-P7-E2027-APP owns those operations).
4. rwb-payment runs JOB-07 for business date D, evaluates the version in force and writes one local decision record per match and per missed payment in its own transaction. It then publishes `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` with the entry ID as its key (RWB-P8-E2008-APP; DP-03).
5. The inbox of consumer group `rwb-decision.decision-recorded.v1` writes its row and dedupes on the entry ID; a redelivery of the same record is a no-op and raises the repeat count (DP-09).
6. `RecordGate` checks the record before anything is appended: decision code from LOV-DECISION, rule ID, rule version held for the package, an inputs reference, a final call and a decided time. A record with no rule version is refused with MSG-P3-027, parked on the retry topic and never defaulted (BR6).
7. `LedgerAppender`, one transaction: takes the next `chain_seq`, sets `prev_hash` to the `entry_hash` of the previous entry, computes `entry_hash` as the SHA-256 of the entry's canonical form, writes the `decision_log_entry`, sets `idempotency_key` to `<sourceService>:<sourceEntryId>`, and acknowledges the inbox row. The entry and the acknowledgement commit together or not at all (BR3, BR5).
8. The sealed entry carries decision code `D5`, rule `R-RES-26`, rule version `PM-2026.12`, the inputs reference to the payment facts of the business date, the recommendation, the final call, the actions, the actor and the decided time — and no personal data (BR9).
9. The match of `PAY-90001` to plan `T-0701` of case `RC-2026-000555` and the missed payment of the same plan for due date 2026-12-15 are two entries, in the order the payment service published them, both naming `PM-2026.12`.
10. `DecisionLogController` answers `GET /decision-log` by case, decision, rule, approver, date range and page, and `GET /decision-log/{entryId}` with the inputs reference, the rule, the version, the recommendation, the final call, the actions, the outcome and both hashes.
11. JOB-14 runs at 02:00 on queue `rwb-decision`: `ChainVerifier` walks `chain_seq` from 1 to the last entry, recomputes every `entry_hash`, compares every `prev_hash` with the entry before it, records the count, the last `chain_seq` and the last `entry_hash`, and writes nothing to the ledger (DP-10).
12. Nothing in this flow evaluates a payment, writes a proceeds row, updates a treatment, moves a case state, reads an ACE view or reads another service's table: the rule set, the sealed records, the read and the chain check are the whole deliverable.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A record names no rule version, or a version the package does not hold | Nothing is appended and `chain_seq` does not move; the event is parked on `rwb.decision-record.v1.retry`; no default version is substituted; one incident is opened | MSG-P3-027 | AC3 |
| X2 | The same record is delivered twice, or the matching run of a business date is repeated and republishes it | No second entry; the first entry ID is answered and the repeat is counted | None | AC5 |
| X3 | The append fails, or the ledger is unavailable | Nothing is committed: no entry and no `chain_seq` used; the inbox row stays unacknowledged; the event is retried on the platform policy and after the last attempt moves to `rwb.decision-record.v1.dlt` | MSG-GEN-006 | AC6 |
| X4 | The record is malformed — no decision code, no inputs reference, no final call or no decided time | The record is refused with 422 semantics on the retry topic and nothing is appended | MSG-GEN-001 | AC4, BR9 |
| X5 | An UPDATE or a DELETE of an entry is attempted through the service login or the schema owner | Both are refused: by the missing grant and by `tr_declog_append_only`; the entry is unchanged and the attempt is written to the ACE audit log | None | AC8, BR4 |
| X6 | JOB-14 finds a `prev_hash` or an `entry_hash` that does not match | The run ends FAILED, names the first broken `chain_seq`, writes nothing and reports the break to Compliance the same day | MSG-GEN-006 | AC8 |
| X7 | A caller whose role does not hold Decision log R calls a read of section 12.1 | 403 with MSG-P4-002; nothing is read and no entry is returned | MSG-P4-002 | AC9 |
| X8 | The parameters, the lists or the session contract does not answer inside 2 s, or its breaker is open | The read or the gate fails closed, retries on the one-hop client policy and writes nothing; no rule value is guessed | MSG-GEN-006 | AC1, AC9 |

X1 to X3 are the decision-side paths of the legacy rows X4 and X6 and of the record rule of DP-03; X4, X5 and X8 are the gates of the ledger and of the boundary; X6 is JOB-14; X7 is the access rule of every operation. The matcher paths X1, X2, X3, X5 of the legacy story belong to RWB-P8-E2008-APP, where the proceeds row, the exception list, the batch gate and the window are decided.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-P8-E2008-CON, the platform contracts and their fakes, on its own schema; it evaluates no payment and needs no live neighbour |
| Negotiable | The consumer-group name, the page size, the component names and the canonical form's field order are this story's choice; the package, its row, the decision code, the rule, the record fields and the hash chain are fixed |
| Valuable | Every match and every missed payment is explainable from one read, and no version reaches a decision without an approved, tested row set |
| Estimable | One reader, one gate, one appender, one collector, one chain verifier, two controllers and one migration |
| Small | Fits two weeks with its tests |
| Testable | Each criterion is a read, a consumed event, an append, a refusal or a chain check with a fixed Given, When and Then |

### 7. Acceptance criteria

```gherkin
Feature: Payment matching with the missed payment event — the rule set and the decision record

  Background:
    Given the service base is /api/recovery/decision/v1, the schema is rwb_decision and the topic is rwb.decision.events.v1
    Given package "PAYMENT_MATCH" version "PM-2026.12" is in force from 2026-12-01 with row "EXACT" at row order 1: amount tolerance 0 percent, window 10 days before the due date and 0 days after, grace 0 days
    Given the rwb-access contract mock returns RW-AUDIT holding Decision log R and RW-COE holding Rules and parameters C and Decision log R
    Given every value is synthetic and carries no personal data

  Scenario: AC1 The version in force and the row the match decides with (new, D-RCV-60)
    Given the rwb-access contract mock returns RW-AUDIT holding Decision log R
    When RW-AUDIT reads GET /api/recovery/decision/v1/admin/rule-packages
    Then the answer holds "PAYMENT_MATCH" with owner role RW-COE
    When RW-AUDIT reads GET /api/recovery/decision/v1/admin/rule-packages/PAYMENT_MATCH/versions
    Then the answer holds version "PM-2026.12" with status "IN_FORCE", valid from 2026-12-01, its checksum and its test result
    Then the registry holds row "EXACT" at row order 1 under "PM-2026.12" with amount tolerance 0 percent, window 10 days before the due date and 0 days after and grace 0 days, as columns of the row
    Then no amount tolerance, window or grace value is a constant of this service's code or configuration

  Scenario: AC2 The window boundary comes from the row set, not from code (new, D-RCV-60)
    Given the test-case set of version "PM-2026.12" holds the boundary case of "PAY-90004", 12,500.00 on "A-0555" dated 2026-12-05 against plan "T-0701" due 2026-12-15, expected "MATCH" on row "EXACT"
    Given it holds the boundary case of "PAY-90005", 12,500.00 on "A-0666" dated 2026-12-05 against plan "T-0702" due 2026-12-16, expected "UNMATCHED"
    When RW-AUDIT reads GET /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/dry-run for "PM-2026.12"
    Then the answer holds the expected and actual result of both boundary cases, the one at 10 days before its due date matched and the one at 11 days unmatched
    Then the counts report the test cases the package carries with all of them passed
    Then the read writes no proceeds row, no treatment row and no entry of the ledger

  Scenario: AC3 A record that names no rule version is refused and never defaulted (new, D-RCV-60)
    Given rwb.decision.DecisionRecorded.v1 for a match of "PAY-90001" with rule "R-RES-26" and an empty ruleVersion
    When the inbox of group rwb-decision.decision-recorded.v1 consumes it for business date 2026-12-15
    Then nothing is appended, chain_seq does not move, and the response is a problem with "messageId": "MSG-P3-027"
    Then the {table} is "PAYMENT_MATCH" and the {check} is "no package in force", and the message names no payment or account fact
    Then the event is parked on rwb.decision-record.v1.retry, no default version is substituted and one incident is opened

  Scenario: AC4 The D5 record of "PAY-90001" is sealed into the central ledger (new, D-RCV-60)
    Given the rwb-payment contract mock returns the decision record of the match of "PAY-90001" to plan "T-0701" of case "RC-2026-000555" with entry id "E-99001", decision code "D5", rule "R-RES-26", rule version "PM-2026.12", due date 2026-12-15, amount 12,500.00 and business date 2026-12-14
    When rwb.decision.DecisionRecorded.v1 arrives on rwb.decision-record.v1 and the inbox consumes it
    Then one decision_log_entry is appended with chain_seq 1 and a prev_hash of 64 zeros
    Then its decision_code is "D5", its rule_id "R-RES-26", its rule_version "PM-2026.12", with inputs_ref, final_call, actor_user_id and decided_at
    Then its idempotency_key is "rwb-payment:E-99001" and its entry_hash is the SHA-256 of its canonical form
    Then the inbox row and the entry commit together
    Then the missed-payment record of "T-0701" for due date 2026-12-15 is sealed with chain_seq 2 and a prev_hash equal to the entry_hash of chain_seq 1

  Scenario: AC5 A redelivered record writes no second entry (new, D-RCV-60)
    Given chain_seq 1 holds the record of "E-99001"
    When the same rwb.decision.DecisionRecorded.v1 is delivered again, and the repeated matching run of 2026-12-14 republishes it
    Then no second decision_log_entry is written and chain_seq stays 1
    Then the repeat is counted and the first entry id is answered
    When RW-AUDIT reads GET /api/recovery/decision/v1/decision-log with ruleId "R-RES-26"
    Then the answer holds one entry for "E-99001"

  Scenario: AC6 A failed append leaves the chain whole and goes to the dead letter (new, D-RCV-60)
    Given the ledger append is forced to fail once for "E-99002"
    When the event is consumed
    Then nothing is committed: no entry, no chain_seq used, and the inbox row stays unacknowledged
    Then the event is retried on rwb.decision-record.v1.retry and after the last attempt moves to rwb.decision-record.v1.dlt
    Then MSG-GEN-006 is raised for system "Decision log" and one incident is opened
    Then the next successful append takes the next chain_seq and the chain holds no gap

  Scenario: AC7 The decision log names the rule, the package version and the hashes (new, D-RCV-60)
    Given chain_seq 1 holds the match of "PAY-90001" under rule "R-RES-26" and version "PM-2026.12"
    When RW-AUDIT reads GET /api/recovery/decision/v1/decision-log with decision "D5", ruleId "R-RES-26", from 2026-12-14 to 2026-12-15, page 0 and size 50
    Then the answer is 200 with one entry and total 1
    Then the entry holds inputsRef, ruleId "R-RES-26", ruleVersion "PM-2026.12", recommendation, finalCall and decidedAt
    When RW-AUDIT reads the same entry with GET /api/recovery/decision/v1/decision-log/{entryId}
    Then the answer adds prevHash, entryHash, actions and outcome
    Then no answer carries a name, an e-mail address, a mobile number or an account number

  Scenario: AC8 JOB-14 checks the chain at 02:00 and reports a break the same day (new, D-RCV-60)
    Given the ledger holds 100 entries from chain_seq 1 to 100
    When the JOB-14 hash chain check Schedule runs at 02:00 on 2026-12-16 on task queue rwb-decision
    Then every entry_hash equals the SHA-256 of its entry's canonical form and every prev_hash equals the entry_hash before it
    Then the run records count 100, last chain_seq 100 and that entry's entry_hash, and writes nothing to the ledger
    Given the test double holds a copy of the ledger whose chain_seq 50 is altered
    When JOB-14 runs again
    Then the run ends FAILED with MSG-GEN-006 for system "Decision log", names chain_seq 50 and reports the break to Compliance the same day

  Scenario: AC9 Only the Decision log right reads, and only rwb_decision is touched (new, D-RCV-60)
    Given a user whose role does not hold Decision log R
    When they call GET /api/recovery/decision/v1/decision-log
    Then the call is refused with 403 and MSG-P4-002 and no entry is read
    Then every operation of section 12.1 declares the right it needs and the guard reads the caller's session once
    Then the boundary test finds no statement of this service against another rwb_* table, the recovery_case table or a v_ace_* view

  Scenario: AC10 Each rule BR1 to BR10 of section 8 has a criterion and a test (new, D-RCV-60)
    Given Not specified in the source documents (NEWAC-RWB-P7-E2008-APP-AC10)
    Then Not specified in the source documents (NEWAC-RWB-P7-E2008-APP-AC10)

  Scenario: AC11 An error on a provided operation answers 401 or 404 (new, D-RCV-60)
    Given a caller calls an operation of section 12.1 without a valid session
    Then the answer is 401
    Given a caller calls an operation of section 12.1 on a resource that does not exist
    Then the answer is 404

  Scenario: AC12 A consumed call that fails or does not answer commits nothing (new, D-RCV-60)
    Given a consumed call of this service fails or does not answer
    When the call is made
    Then nothing is appended, chain_seq does not move, and the failure is reported and not defaulted
```

The criteria AC1 to AC12 are new under D-RCV-60 and test only the rule set, the sealed record, the read and the chain check of this slice. They own no legacy criterion: the legacy criteria of RWB-E2-008 stay with the other slices — the match, the missed event and the exception list with RWB-P8-E2008-APP, the payment facts with RWB-P1-E2008-APP, the plan position with RWB-S2-E2008-APP — and the cross-service journey with RWB-ITG-E2008-ITG (GAP-2498; ASM-4131).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The rule registry and the central ledger are rwb-decision's, a version is never edited in place, and no other service reads either table | Arch v5 slide 41; R-PREC default ruling; DP-01 |
| BR2 | Match type, amount tolerance, window before and after, grace days and partial floor are columns of the rows of the version, never constants of this service or of the consuming one | legacy BR7; D-RCV-36 T10 |
| BR3 | A decision is recorded before anything acts on it: the owning service writes its local record in its own transaction, and the ledger seals it after; an entry whose append fails is never acknowledged | legacy BR9; DP-03 |
| BR4 | The ledger is append only and hash chained: no update and no delete, `prev_hash` is the previous `entry_hash`, the first is 64 zeros, and every `entry_hash` is the SHA-256 of the entry's canonical form | FSD P7 A2.1 and AC-P7-001-01 |
| BR5 | One entry per source decision: the key is the source service and the source entry ID, a redelivery is a no-op and the repeat is counted | legacy BR6; R-UNI-40 |
| BR6 | A record that names no rule version is refused with MSG-P3-027 and parked; no default version and no default row is ever substituted | legacy BR10; R-UNI-41; D-RCV-36 T7 |
| BR7 | A match record names decision code `D5`, rule `R-RES-26` and the package version that decided it, and a missed payment carries its own code from LOV-DECISION | legacy BR9 and AC9; TSD P7 T3.2 |
| BR8 | JOB-14 verifies the chain daily at 02:00 on queue `rwb-decision` and a break is reported to Compliance the same day | Arch v5 slide 44; FSD P7 AC-BG-P7-001-01 |
| BR9 | A record holds an inputs reference and identifiers only: no name, e-mail address, mobile number or account number reaches the ledger, a log line or an event | legacy section 17 |
| BR10 | Every read of the ledger needs Decision log R with scope applied, and every record is written by the service identity, never by a person | TSD P7 T6.1; FSD P7 A2.1.3.3 |

Coverage of BR1 to BR10 by criterion and test case: BR1 AC1 and AC9 (TC-E2-008-12); BR2 AC1 and AC2 (TC-E2-008-07, TC-E2-008-12); BR3 AC6 (TC-E2-008-11); BR4 AC4 and AC8 (TC-E2-008-09); BR5 AC5 (TC-E2-008-06); BR6 AC3 (TC-E2-008-08); BR7 AC4 and AC7 (TC-E2-008-01, TC-E2-008-09); BR8 AC8 (TC-E2-008-09); BR9 AC7 (TC-E2-008-09); BR10 AC9 (TC-E2-008-10), with the service-identity write in AC4.

### 9. State transitions

This story changes no case status and no plan state; the plan moves from `PLAN_RUNNING` to `PLAN_CURE_PERIOD` under R-RES-27 in rwb-case. It owns the state of a ledger entry.

| From | Event | Condition | To |
|---|---|---|---|
| (none) | A record arrives from the notice topic | The gate passes and the append commits | SEALED (one `decision_log_entry`, `chain_seq` taken) |
| (none) | A record arrives with no rule version, or malformed | MSG-P3-027 or MSG-GEN-001 | PARKED on `rwb.decision-record.v1.retry`; no entry and no `chain_seq` used |
| (none) | The append fails | The transaction rolls back | (no entry); retried, then `rwb.decision-record.v1.dlt` with an incident |
| PARKED | The record is republished with its version | The gate passes | SEALED, once, under the version it names |
| SEALED | Any later update or delete | Never | Refused: the entry is unchanged for the life of the ledger |

A sealed entry has no later state, which is the point of the chain: a correction is a new entry that names the one it corrects (`corrects_entry_id`), never an edit.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-AUDIT, internal audit officer | Reads the package, the versions, the dry run, the ledger and one entry (Decision log R) |
| RW-COE, center of excellence analyst | Owns package `PAYMENT_MATCH` and reads its versions, its rows and its test cases (Rules and parameters C, Decision log R); loads nothing here |
| Compliance and PDPA officer | Receives the chain break of JOB-14 and reads the ledger (Decision log R) |
| The rwb-decision service identity | Consumes the records, appends the entries, runs JOB-14 and writes the gap and break records of a run |
| SY-DECLOG, decision log writer | Supplies the canonical form, the hash chain and the append primitive of DP-03 (RWB-PLT-E1027-CON) |
| SY-RULES, Drools evaluator | Supplies the compiled row set, the first-match semantics and the checksum at read and dry run only (DP-04); it evaluates no payment here |
| RW-CREDITAD and RW-CASEOWN | Reach the match through RWB-P8-E2008-APP and the case through rwb-case; neither is an actor of this story |
| Any role without Decision log R | Refused with MSG-P4-002 on every operation of section 12.1 |
| rwb-access authorise check (DP-08) | Called before every operation of section 12.1 reads or appends a record; the check name is Not specified in the source documents (DOR-RWB-P7-E2008-APP-6) |

No person is named anywhere and no delegation of authority level applies: a package row and a ledger entry are not credit decisions, and the record says which rule and which version decided, not who approved a limit.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-274 to DF-REF-278 | `rule_package` (P7) | id, package_code, title, owner_role, hit_policy | Read: the `PAYMENT_MATCH` row and its owner role |
| DF-REF-279 to DF-REF-294 | `rule_package_version` (P7) | version label, status, checksum, valid_from, valid_to, author, approver, test_result, dry_run_counts | Read: the version in force and its result |
| DF-REF-002, DF-REF-003, DF-REF-296 to DF-REF-298 | `rule_row` (P7) | rule_id, rule_version, package_version_id, drools_rule_name, outputs | Read: row `EXACT` at row order 1 and its columns |
| DF-REF-185 to DF-REF-197, DF-REF-299 | `rule_test_case` (P7) | test case, expected result, actual result | Read: the two boundary cases and the counts |
| DF-DEC-001, DF-DEC-002, DF-DEC-003, DF-DEC-004, DF-DEC-005 | `decision_log_entry` (P7) | id, case_id, decision_code, rule_id, rule_version | Write at append; read through 12.1 |
| DF-DEC-008, DF-DEC-012, DF-DEC-014, DF-DEC-015, DF-DEC-016, DF-DEC-030 | `decision_log_entry` (P7) | inputs_ref, final_call, actions, outcome, decided_at, actor_user_id | Write at append; read |
| DF-DEC-017, DF-DEC-018, DF-DEC-028, DF-DEC-029, DF-DEC-031 | `decision_log_entry` (P7) | prev_hash, entry_hash, chain_seq, corrects_entry_id, idempotency_key | Write at append; read |
| DF-ACE-043 to DF-ACE-046, DF-ACE-028, DF-ACE-182 | `v_ace_payment`, `v_ace_account`, `v_ace_batch_status` | payment_code, account_key, payment_date, payment_amount, next_installment_date, status | Not read: they reach this story only inside the inputs reference of a record, through RWB-P8-E2008-CON |
| DF-FIN-002, DF-FIN-004, DF-FIN-006, DF-FIN-008 | `proceeds` (P8) | case_id, payment_code, amount, matched_to | Not read and not written: `proceeds` is rwb-payment's |

The five tables of `rwb_decision` and the outbox, inbox and idempotency tables are this service's and no other service reads them (DP-01). The field IDs are those of the Logical Data Model and Data Dictionary v9 and of TSD P7 v2 T3.1. The only structures this story adds are constraints — the unique key of section 13 — and not fields. The trigger `tr_declog_append_only` named in the baseline is a database constraint, not a field or entity of the Logical Data Model v9 or Data Classification v5, and carries no field ID. `payment_match_rule` and DF-REF-261 to DF-REF-273 are retired by D-RCV-36 T10 and no version may recreate them.

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-decision` (P7); base `/api/recovery/decision/v1`. The two decision-log paths are API-P7-006 and API-P7-007 of TSD P7 v2 T-A.1 on the service base; the three rule-package paths are the ownership map's P7 paths of the registry. This story publishes no write operation: the ledger is written from the inbox and the package is loaded by RWB-P7-E2027-APP. The dry-run answer beyond `testResult` and `dryRunCounts`, and the page default of the read, are Not specified in the source documents (GAP-2495; ASM-4129).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/admin/rule-packages` | List the packages of the registry with code and owner role; 200 with the list | Rules and parameters R | Not applicable, read only |
| GET | `/admin/rule-packages/{packageCode}/versions` | List the versions of a package with status, valid-from, checksum, test result and dry-run counts; 200 | Rules and parameters R | Not applicable, read only |
| GET | `/admin/rule-package-versions/{versionId}/dry-run` | Read the dry-run counts and the per-test-case result of a version, including the two boundary cases; 200, 404 an unknown version | Rules and parameters R | Not applicable, read only |
| GET | `/decision-log` | Search the ledger by caseId, decision, ruleId, approver, from, to, page and size; 200 with `DecisionLogPage` | Decision log R, scope applied | Not applicable, read only |
| GET | `/decision-log/{entryId}` | Read one entry with its inputs reference, rule, version, recommendation, final call, actions, outcome and both hashes; 200, 404 an unknown entry | Decision log R, scope applied | Not applicable, read only |

Errors: 401 no session (Not specified in the source documents (CG-ALL-7116)); 403 the role lacks the right (MSG-P4-002); 404 an unknown package, version or entry (Not specified in the source documents (CG-ALL-7116)); 422 a parameter outside its range (MSG-GEN-001); 503 the ledger could not be read (MSG-GEN-006). Every error is an RFC 9457 problem response with `messageId` set. `RuleVersionController` answers the three registry reads and `DecisionLogController` the two ledger reads.

API client states: a failed read answers 503 (MSG-GEN-006) and a caller without the right answers 403 (MSG-P4-002). The empty, loading, error and no-access states of SCR-14, SCR-28, SCR-38 and SCR-44 are Not specified in the source documents (DOR-RWB-P7-E2008-APP-10).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access, on RWB-P4-E1037-CON | The caller's role, scope and Decision log or Rules and parameters right behind every operation of 12.1; faked, one hop, 2 s (DP-11) |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case, on RWB-P3-E1042-CON | The input age limit of FSD P7 VR-P7-001-3, whose key is Not specified in the source documents (GAP-2494; ASM-4128); DP-06 |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case, on RWB-P3-E1043-CON | LOV-DECISION with code `D5` and the version-state list; DP-07 |

The three are published operations of their owners, called once per request behind a breaker with a 2 s budget, and each is answered by its fake of 12.8. The rwb-payment contract of the story line is not called: it is the shape the consumed record must match, and its fake delivers the records of 12.4. The platform H rows and the remaining C rows the pattern table adds are named in section 13 and carried in GAP-2496.

#### 12.3 Events published

None. This story publishes no event of its own and writes no outbox row: it is the collector, not the producer. `rwb.decision.RulePackageInForce.v1` (EV-30) and the governance records of `rwb.decision-record.v1` are RWB-P7-E2027-APP's, and `ProceedsMatched` (EV-25) and `PaymentMissed` (EV-12) are rwb-payment's on `rwb.payment.events.v1`. The sealing of an entry is an append, acknowledged on the inbox row of the consumed record.

#### 12.4 Events consumed

| Event | Topic | Consumer group | Producer | Key and dedupe | Payload (IDs and facts only) |
|---|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | `rwb-decision.decision-recorded.v1` | every service that decides, here rwb-payment for a match and a missed payment (RWB-P8-E2008-APP) | key `entryId`; dedupe on `entryId` through `idempotency_key` | the local record: source service, entry ID, decision code, rule ID, rule version, case ID, inputs reference, recommendation, final call, actions, outcome, decided at |

The retry topic `rwb.decision-record.v1.retry` and the dead-letter topic `rwb.decision-record.v1.dlt` back the consumer (DP-09). The envelope is CloudEvents 1.0 and the `data` element carries no personal data. The record shapes here three field names of the legacy story build on are Not specified in the source documents (GAP-2494; ASM-4128).

#### 12.5 Workflows and activities

None. The collection is a synchronous inbox consumer and the append is a database transaction of the same service; there is no workflow, no activity and no child workflow on queue `rwb-decision` in this story. JOB-14 is the Schedule of 12.6 and not a workflow (DP-10).

#### 12.6 Schedules

| Schedule | When | Mechanism | Owner and this story's part |
|---|---|---|---|
| JOB-14 Hash chain check | 02:00 daily, Asia/Bangkok | A Temporal Schedule on the `rwb-decision` queue that starts `ChainVerifier`: it walks the chain, records count, last `chain_seq` and last `entry_hash`, writes nothing to the ledger, and ends FAILED on a break (Arch v5 slide 44; Temporal and Drools slide 16) | P7 rwb-decision. This story builds the verifier and its break report; the shared Schedule infrastructure is RWB-PLT-E1071-CON |

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `rule_package` | P7 (`rwb_decision`) | The `PAYMENT_MATCH` row, its title, its owner role RW-COE and its hit policy |
| `rule_package_version` | P7 (`rwb_decision`) | The version, its status, checksum, valid-from and valid-to dates, author, approver, test result and dry-run counts |
| `rule_row` | P7 (`rwb_decision`) | Row `EXACT` at row order 1 with its condition and output columns |
| `rule_test_case` | P7 (`rwb_decision`) | The test cases of the version, with the two boundary cases and their expected and actual result |
| `decision_log_entry` | P7 (`rwb_decision`) | One append-only, hash-chained entry per match and per missed payment |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_decision` | Inbox, dedupe and idempotency objects of the service |
| `approval` | P7 (`rwb_decision`) | Not used: a match decision is not an approval of the delegation of authority |

Not owned and not read: `proceeds`, `treatment`, `v_ace_payment`, `v_ace_account` and `v_ace_batch_status` (P8, S2 and P1); `parameter_value`, `reference_row` and `lov_value` (P3). No foreign key crosses a schema.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-payment contract fake | RWB-P8-E2008-CON | The `DecisionRecorded` record of the match of `PAY-90001` (`E-99001`), the missed-payment record of `T-0701` for 2026-12-15 (`E-99002`), a variant with an empty rule version, a malformed variant with no decision code, and a duplicate of `E-99001` |
| rwb-access fake | RWB-P4-E1037-CON | `GET /me/session` for RW-AUDIT, RW-COE and a role without Decision log R |
| rwb-case parameters and reference-data fake | RWB-P3-E1042-CON, RWB-P3-E1043-CON | The input age limit, LOV-DECISION with `D5` and the version-state list |
| decision-record library fake | RWB-PLT-E1027-CON | The canonical form, the SHA-256 of an entry, the append primitive and a forced append failure |
| outbox and inbox fake | RWB-PLT-TE006-CON | The consumer group, the dedupe key, the retry and `.dlt` topics and a redelivery |
| Drools kit fake | RWB-PLT-E1072-CON | The compiled row set of `PM-2026.12`, its checksum, first-match semantics and the test-case runner |
| workflow kit fake | RWB-PLT-E1071-CON | A Schedule firing at 02:00, and a chain copy with one entry altered for AC8 |

Each fake is replaced by the real contract or the real library as its story lands, without a change to the scenarios. The fakes carry synthetic package codes, version labels, entry IDs and payment codes only.

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 5, consumed 3 | Three registry reads and two ledger reads provided; the session, the parameters and the lists consumed, one hop and 2 s |
| Kafka | Published 0, consumed 1 event type | `rwb.decision-record.v1` with `DecisionRecorded`, plus its `.retry` and `.dlt` topics |
| Temporal | 1 Schedule, 0 workflows | JOB-14 on queue `rwb-decision` in namespace `rwb-recovery` |
| File | None | No file is read, built or delivered |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `ledger`, Java package `th.co.scb.ace.workbench.recovery.decision.ledger`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

How this story applies each row. **DP-01**: the five tables are `rwb_decision`'s and the story reads no schema of another service; the payment facts never arrive as rows, only as an inputs reference. **DP-03**: the record is written by rwb-payment through the library in its own transaction and collected here through the shared topic rwb.decision-record.v1, which this service owns together with the central ledger, appended with the canonical form, the hash chain and the append primitive; a record that cannot be appended is never acknowledged (BR3). **DP-04**: the package, its version and its rows are read here and evaluated by the owning service; the C row RWB-P7-E1073-CON is this service's own rule-package contract, and the kit is a platform library, so nothing is rebuilt. **DP-05**: no ACE view is read; `v_ace_payment`, `v_ace_account` and `v_ace_batch_status` are named only as the facts a record refers to. **DP-06**: the input age limit of VR-P7-001-3 is a parameter and not a constant. **DP-07**: LOV-DECISION, the version states and the match types are reference data and row columns, never code. **DP-09**: the inbox writes its row, dedupes the entry and owns the retry and `.dlt` topics; no outbox row is written because the story publishes nothing. **DP-10**: JOB-14 is a Temporal Schedule at 02:00; the Quartz row and its table are gone. **DP-11**: the three consumed operations are one hop with a 2 s budget and a breaker, replacing the legacy in-process calls to the parameter, the list and the access check. **DP-13**: every path of section 12 uses `/api/recovery/decision/v1`. **DP-15**: one numbered migration of `rwb_decision` adds the unique key and the inbox objects; it is not the monolith's `V2_008__payment_matching.sql`. **DP-19**: SCR-38 reaches the read through the gateway-bff composite route.

The platform H rows of the table — RWB-PLT-E1027-CON, E1072-CON, E1042-CON, E1043-CON, TE006-CON, E1071-CON, E1044-CON and N001-CON — and the C rows RWB-P7-E1073-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON and RWB-P4-E1037-CON are **not** in the metadata rows, which name None and RWB-P8-E2008-CON: they are wave 0 platform contracts and published contracts, none blocks the build, and an APP story builds against the published set and its fake (GAP-2496; ASM-4130).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `RuleVersionController` | Controller | The package list, the version list and the dry run, with the guard and the problem mapping |
| `RuleSetReader` | Service | Reads the version in force and its `EXACT` row and test cases; refuses a read of a version the package does not hold |
| `DecisionRecordConsumer` | Consumer | The inbox of `rwb.decision-record.v1`: dedupe on the entry ID, the retry and `.dlt` path and the repeat count |
| `RecordGate` | Service | Checks decision code, rule, rule version, inputs reference, final call and decided time; refuses a record with no version (BR6) |
| `LedgerAppender` | Service | One transaction: next `chain_seq`, `prev_hash`, `entry_hash`, the entry, the idempotency key and the inbox acknowledgement (BR4) |
| `ChainVerifier` | Service | JOB-14: walks the chain, recomputes every hash, records the counts and reports the first break |
| `DecisionLogController` | Controller | `GET /decision-log` and `GET /decision-log/{entryId}` with paging, scope and hashes |

**Database.** One migration of the service's own Flyway sequence: the unique index `ux_declog_idempotency_key` on `decision_log_entry` (`idempotency_key`) where it is not null, the index on (`rule_id`, `decided_at`) of the read, and the inbox, dedupe and idempotency objects of the library in `rwb_decision`. No column is added to `decision_log_entry`, whose field set is TSD P7 T3.1 and whose DDL is RWB-P7-E1008-APP's.

**Build steps.** (1) Take the baseline and write the migration; test the keys. (2) Build `RuleSetReader` and the three registry reads against the Drools kit fake; test AC1 and AC2. (3) Build `RecordGate` and `LedgerAppender`; test AC3, AC4, AC5 and AC6. (4) Build `DecisionLogController`; test AC7 and the access test. (5) Build `ChainVerifier` and register JOB-14; test AC8. **Done when** the tests of section 16 pass, a synthetic month of match records chains without a gap, and every entry names `R-RES-26` with the package version it was decided under.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-027 | No `PAYMENT_MATCH` version is found for the record | The {table} load was refused: {check}. The version in force is unchanged. |
| MSG-GEN-006 | The append or the chain check fails | {system} could not complete the {action}. The run is marked failed and an incident is open. |
| MSG-GEN-001 | A record or a request misses a required field | Enter {field}. |
| MSG-P4-002 | The role lacks Decision log R or Rules and parameters R | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The owning service could not record its decision | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

For MSG-P3-027 in this story, {check} is "no package in force" and {table} names the package code "PAYMENT_MATCH" only, never a payment or an account fact. MSG-P7-003 is the caller's message on the rwb-payment side and is quoted here only because this story's refusal is what raises it.

### 15. Screens and states

SCR-38 Decision log query (E2) searches the ledger by case, rule, approver and date and shows one entry with its rule, version, inputs reference, final call and hashes; it calls the read of 12.1 through the gateway-bff composite route and this story builds the operations behind it, not the screen. SCR-44 Job monitor shows the JOB-14 run of 12.6 with its count, last `chain_seq` and break. No other screen is touched: the match itself is seen on SCR-28 Proceeds matching and the plan on SCR-14 Treatment record, both served by other services. Screen states: SCR-14 empty, loading, error and no access are Not specified in the source documents (CG-ALL-7128); SCR-28 empty, error and no access are Not specified in the source documents (CG-ALL-7129), its loading state as the screen specification gives it; SCR-38 empty, error and no access are Not specified in the source documents (CG-ALL-7130), its loading state as the screen specification gives it. SCR-44 empty, loading, error and no access are Not specified in the source documents (CG-ALL-7131).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-008-01 | AC1, AC4, AC7 — decision-side evidence: the proceeds row and the treatment update of the same facts are RWB-P8-E2008-APP's | Component | `PAY-90001` 12,500.00 on `A-0555` dated 2026-12-14; plan `T-0701` due 2026-12-15 |
| TC-E2-008-02 | AC2 — decision-side evidence: the missed-payment record of `T-0701` for 2026-12-15; the event and the plan move are other owners' | Component | no payment on `A-0555` between 2026-12-05 and 2026-12-15 |
| TC-E2-008-03 | AC3 — decision-side evidence: the record of the unmatched payment names the row that decided; the exception list is RWB-P8-E2008-APP's | Component | `PAY-90002` 3,000.00 on `A-0555` |
| TC-E2-008-04 | AC4 — decision-side evidence: no record is sealed for a payment on an account with no open case | Component | `PAY-90003` on `A-0999` with no open case |
| TC-E2-008-05 | AC5 — decision-side evidence: no record is sealed for a business date whose batch is not complete | Component | the ALS batch of 2026-12-15 failed |
| TC-E2-008-06 | AC6 — decision-side evidence: a repeated run publishes no second record and no second entry | Component | the matching run of 2026-12-14 repeated |
| TC-E2-008-07 | AC7 — the window boundary as row data and test case | Component | `PAY-90004` 10 days and `PAY-90005` 11 days before their due dates |
| TC-E2-008-08 | AC8 — no version named is a refusal and never a default | Contract | a record with no rule version on 2026-12-15 |
| TC-E2-008-09 | AC7, AC4, AC8 — the entry names the rule and the package version, and the chain verifies | Integration | `PAY-90001` matched under version `PM-2026.12` |
| TC-E2-008-10 | AC9 — the access refusal of the read | Contract | a role without Decision log R calls `GET /decision-log`; MSG-P4-002 |
| TC-E2-008-11 | AC6 — a record that cannot be appended is never acknowledged | Component | a record whose append fails |
| TC-E2-008-12 | AC1 — the boundary cases of the rule_test_case rows of the version in force are read as stored | Component | the two boundary cases of the version in force |
| TC-E2-008-13 | AC11 — an error on a provided operation answers 401 or 404 | Contract | Not specified in the source documents (NEWAC-RWB-P7-E2008-APP-AC11) |
| TC-E2-008-14 | AC12 — a consumed call that fails or does not answer commits nothing | Component | Not specified in the source documents (NEWAC-RWB-P7-E2008-APP-AC12) |

These are the ten legacy test cases of the key and the two added TC-E2-008-11 and TC-E2-008-12 and the added TC-E2-008-13 and TC-E2-008-14, kept in the Work Package's order with the legacy Level "System" mapped to Component and "Access" to Contract; the full Given, When and Then stay in Recovery Workbench Test Cases v8.xlsx under the same ID. Integration copies of these IDs end in `-ITG` and belong to RWB-ITG-E2008-ITG (GAP-2498; ASM-4131).

### 17. Guardrails

- No business value in code: amount tolerance, window before and after, grace days, partial floor and match types are columns of the rows of `PAYMENT_MATCH`; the LOV values are reference data of RWB-P3-E1043-CON.
- No personal data in logs, tests, events or prompts: a record carries an inputs reference and identifiers, payments are identified by payment code and account key, and account numbers are never logged.
- No read of another service's tables and no ACE table: the facts reach this story only inside the inputs reference of a record, through RWB-P8-E2008-CON.
- No write to the ledger except through the appender: no update, no delete, no manual insert, and no back-dating of `chain_seq`.
- Amounts use BigDecimal with scale 2 and the hash is computed over a canonical form that is tested against a fixed vector, so a change of the form is a deliberate, versioned act.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-007 | Plan timers run from the treatment; a missed payment raises an event | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-11 | 7.3 Negotiate settlement or deed in lieu | R-RES-27 | TC-E2-008-02, TC-E2-008-05 |
| REQ-CHO-009 | Payments matched to the plan; unmatched to an exception list | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-10, FEAT-PAY-01, FEAT-PAY-02 | 7.3 Negotiate settlement or deed in lieu | R-RES-26, R-UNI-03, R-UNI-40, R-UNI-41 | TC-E2-008-01, TC-E2-008-03, TC-E2-008-04, TC-E2-008-06, TC-E2-008-07, TC-E2-008-08, TC-E2-008-09, TC-E2-008-10, TC-E2-008-11, TC-E2-008-12 |

Both requirement rows are met on the decision side only: the event, the exception list and the plan timer stay with their owners and are traced from the legacy key and from RWB-ITG-E2008-ITG.

### 19. Out of scope

- JOB-07, the payment facts, the running plans, the match, the proceeds row, the treatment installment update, the exception list, the run summary and the `ProceedsMatched` and `PaymentMissed` events (RWB-P8-E2008-APP).
- The two operations, the event schemas, the error model and the contract fakes of rwb-payment (RWB-P8-E2008-CON).
- The load, approval, promotion and rollback of package `PAYMENT_MATCH`, and the authoring of its workbook (RWB-P7-E2027-APP, RWB-P7-E1073-APP).
- The DDL and the writer of the decision-log store, and the hash chain of an entry written in the owner's schema (RWB-P7-E1008-APP, RWB-PLT-E1027-CON).
- The plan state `PLAN_RUNNING` to `PLAN_CURE_PERIOD` under R-RES-27 and the transfer rule (rwb-case), and the cure-period rules R-RES-28 to R-RES-31 (rwb-treatment).
- Partial and late payments inside a window after the due date (RWB-E2-027), and settlement, auction and enforcement proceeds (Epic 4).
- The nightly copy of the ledger to the data lake (retired, D-RCV-60) and the reporting read model, which rwb-reporting builds from events.
- The screens themselves (SCR-38, SCR-44) and the deployment of this build, its Schedule, its alerts and its runbook.
