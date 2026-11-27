# RWB-P7-E2043-APP Temporal and Drools integration pattern and reference case workflow

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E2043-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-043 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP07, DP09, DP10, DP11, DP14, DP15, DP19 |
| Parallel lane | L-P7-AP |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E2043-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (FR-P7-001, FR-P7-005, FR-P7-006, FR-P7-007, FR-P7-008, FR-P7-009, FR-P7-010, FR-P7-011, FR-P7-029) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-043 for rwb-decision — the collection of `DecisionRecorded` into the central decision ledger, the daily chain check and the two decision-log reads. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P7-E2043-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **developer of `rwb-decision` and the internal auditor (RW-AUDIT) who has to prove the order of a reference-case step**, I want **the central decision ledger of `rwb-decision` to collect every `rwb.decision-record.DecisionRecorded.v1` fact of `rwb.decision-record.v1` into `decision_log_entry` — one entry per reference-case step, append only and hash chained, deduplicated by event ID and idempotency key, keeping the rule ID and the rule version exactly as the owning service pinned them — inside the five-minute collection target, with JOB-14 checking the chain every day at 02:00 and reporting a break to Compliance the same day, and with the two reads `GET /api/recovery/decision/v1/decision-log` and `GET /api/recovery/decision/v1/decision-log/{entryId}`**, so that **the pattern "evaluate in an activity, record, then act" is provable from the ledger alone, and no decision of the reference run is a claim without a record**.

Inside `rwb-decision` this is the ledger half of the legacy story RWB-E2-043:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1`, Temporal task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`, and the shared topic `rwb.decision-record.v1` through the decision-record library of DP-03.
- One deliverable and nothing else: (a) the ingest of `rwb.decision-record.DecisionRecorded.v1` into `decision_log_entry`, the continuous consumption Arch v5 slide 44 calls JOB-13; (b) the inbox dedupe by event ID and by idempotency key, with the repeat counted for R-UNI-40; (c) the hash chain — `chain_seq`, `prev_hash` and `entry_hash` over the canonical form, a first `prev_hash` of 64 zeros, append only; (d) the rule ID and rule version held exactly as the fact carried them, with no lookup of the version in force; (e) the five-minute collection target of Arch v5 slide 28 and the completeness gap report; (f) JOB-14 at 02:00 on the `rwb-decision` queue, with a break reported to Compliance the same day (NFR-035); (g) the two reads API-P7-006 and API-P7-007; and (h) one entry per decision step of the reference run `ref-case-RW-2026-000777`.
- **Not this story:** the Temporal worker, `ReferenceCaseWorkflow`, `EvaluateRulesActivity`, `RecordAndApplyActivity`, the `CaseEventSignalRelay`, the synthetic case fixture and the replay gate — RWB-P3-E2043-APP and RWB-P3-E2043-OPS, with the replay gate of RWB-E2-040. This story names them only to say who writes the facts it collects, and it registers no worker, no workflow and no activity of the reference run.
- **Not this story:** the embedded Drools kit, which is RWB-PLT-E1072-CON's (DP-04). The story reads the `ruleId` and the `packageVersion` a fact carries and evaluates no package.
- **Not this story:** the cross-service proof. RWB-ITG-E2043-ITG publishes the case event, follows it into the workflow and reads this ledger beside the workflow history.
- The package RESTRUCTURE version "RES-2026.12" and rule R-RES-04 are the registry's (RWB-P7-E2042-APP), under the contract C RWB-P7-E1073-CON; this story records their identifiers and changes neither.
- The strict-mode acknowledgement before a point of no return and the daily seal of the ledger hash to write-once storage are named by Arch v5 slides 14 and 28 and sit outside this story, on the ledger built here (GAP-1310; ASM-2320).
- The decision code, the final call values and the approval level are reference data of `rwb-case` read through DP-07; the value set of LOV-DECISION is not enumerated by any source (GAP-1306; ASM-2316).
- The database login is the per-service login of DP-02. Its name is Not specified in the source documents (GAP-1307; ASM-2317); this story uses the phrase "the rwb-decision login (DP-02)" and never the shared monolith login.

The values carried from the legacy story are unchanged: the synthetic case `RW-2026-000777` with status IN_PROGRESS and route state IN_FCR_QUEUE, the reference workflow ID `ref-case-RW-2026-000777`, the case events `EV-CASE-0777-01` to `EV-CASE-0777-05`, the event keys `CASE_EVENT:EV-CASE-0777-01` to `CASE_EVENT:EV-CASE-0777-05`, package RESTRUCTURE version "RES-2026.12" in force from 2026-12-01 and "RES-2027.01" from 2027-01-01, rule R-RES-04 moving IN_FCR_QUEUE on CASE_PICKED_UP to WITH_FCR_OFFICER, the retry policy of 1 s, back-off 2 and 10 attempts, and the messages MSG-P7-003, MSG-P7-009 and MSG-P4-002. The ledger's own two values are the five-minute collection target of Arch v5 slide 28 and the 02:00 chain check of JOB-14 (Arch v5 slide 44). The chain facts are the ones FSD P7 v3 A2.1 writes for the decision log: the append-only trigger `tr_declog_append_only`, the missing `UPDATE` and `DELETE` grant for the service login, `entry_hash` as the SHA-256 of the entry's canonical form, the first `prev_hash` of 64 zeros, and a check that holds count 100 and last `chain_seq` 100 on a chain of 100 entries.

### 2. Business rationale

The legacy skeleton showed the order inside one module: the signalling relay, the evaluator, the decision-log writer and the case state service were called in process, against one schema and one transaction manager. Architecture v5 keeps the order and moves the record: each of the 19 services writes its own decision record in its own schema, in the same transaction as the state change, hash-linked to the record before it, and publishes `DecisionRecorded` on `rwb.decision-record.v1` (Arch v5 slides 20 and 28). `rwb-decision` consumes that topic into the central decision ledger. The order is therefore only provable if the collection is right: one entry per step, the rule and version untouched, no duplicate, no silent gap, and a chain a daily check can defend in an audit.

This story is that collection. It carries ADR-022 (a local decision record plus a central ledger) and the part of ADR-009 the target changes, and it makes the measure of RWB-E2-043 true: the pattern is one order, and the ledger shows it. Without the ledger, three of the legacy criteria degrade into statements about a workflow history that retention eventually removes — that the rule version was pinned at evaluation time, that the record exists before the state move, and that a retry wrote one decision and not two. With the ledger they are statements about an append-only, hash-chained row an auditor reaches through an operation of this service.

The realignment changes the mechanism, not the business rule:

1. The in-process `DecisionLogWriter` of the monolith becomes the decision-record library and its topic (DP-03): the owning service writes its record in its own transaction and publishes `DecisionRecorded`, and this story appends it to the central ledger with the append-only rule and the chain of FSD P7 v3 A2.1 (Arch v5 slide 28).
2. The order inside the workflow becomes an order in the ledger: the fact carries the rule and the version chosen at evaluation time, so a late collection still shows the version that decided and a later promotion cannot rewrite an earlier entry (R-UNI-38; design slides 6, 15 and 27).
3. The nightly copy of the log to a data lake is gone with the data lake (DP-17); the collection is continuous Kafka keyed by the case, with the five-minute target of Arch v5 slide 28 (JOB-13), and the daily anchor of the ledger hash to write-once storage is the separate step of that slide.
4. The Quartz job that walked the log becomes JOB-14, a Temporal Schedule at 02:00 on the `rwb-decision` queue with the overlap policy SKIP and the catch-up window of the job map (DP-10; Arch v5 slide 44).
5. The one decision-log path of the monolith becomes two operations on the service base (DP-13), reached through the gateway-bff composite route the decision-log screen uses (DP-19) and guarded by the decision-log baseline's authorise path (DP-11).
6. The rule ID and the rule version are no longer read from a catalogue at display time: they are columns of the entry written from the fact, so an entry explains itself even when the package has since been superseded (DP-04, without an evaluation).

This story meets REQ-DRI-001 and REQ-CWC-016 on the collection side, REQ-DRI-005 as the reason both the owning service's transaction and the append fail closed, and REQ-DRI-007 through the retry and exception behaviour of the outbox consumer. It carries NFR-033, NFR-035 and the principle that no action stands without its record (R-UNI-39).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P3-E2043-CON | The published reference-workflow contract of `rwb-case` (P3): the workflow ID prefix `ref-case-`, the `CaseEventSignal` record with its `eventId` and `idempotencyKey`, and the statement that the record and the state change are one transaction which publishes `DecisionRecorded`. The contract is what fixes the fact shape on the producing side; the fact's own payload is Not specified in the source documents (GAP-1304; ASM-2314). Faked, one hop, 2 s (DP-11) |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the record fields of Arch v5 slide 28, the `DecisionRecorded` envelope, the append, `chain_seq`, `prev_hash`, `entry_hash`, the append-only rule and the fail-closed exception |
| RWB-PLT-E1072-CON | The embedded Drools kit (DP-04): it supplies `RuleResult` with `packageCode`, `packageVersion`, `ruleId` and `outputs`, so this story can read the two identifiers a fact carries without redefining them. Nothing is evaluated, compiled or cached here |
| RWB-PLT-TE006-CON | The outbox and inbox library with CloudEvents 1.0 in binary mode (DP-09): the `processed_event` inbox, the idempotency key, the `OutboxConsumer` convention, the retry topics of 1 min, 10 min and 1 h, the dead-letter topic and its alert |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the `rwb-case` reference-data contract (DP-07): LOV-DECISION, LOV-APPROVAL-LEVEL and the final call list with the version in force. The values of LOV-DECISION are not enumerated by any source (GAP-1306; ASM-2316) |
| The parameters client of the ledger baseline | The five-minute collection target and the 02:00 chain-check time, read as parameter rows of `rwb-case` at the version in force (Arch v5 slides 28 and 44). The parameter names are Not specified in the source documents (GAP-1305; ASM-2315). The parameters mechanism arrives with the decision-log baseline of the service (RWB-P7-E2024-APP) |
| RWB-PLT-E1071-CON | The Temporal workflow kit in namespace `rwb-recovery` (DP-10): the JOB-14 Schedule at 02:00 on the `rwb-decision` queue, its overlap policy and its catch-up window, and the worker the service template runs. This story registers the Schedule and the chain-check activity; it adds no workflow |
| RWB-PLT-E1047-CON | The naming library (DP-14): the topic, event and queue names of section 12 |
| RWB-PLT-E1044-CON | The per-service Flyway sequence and migration conventions in `rwb_decision` (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19): the route the decision-log screen reaches the two reads through. No screen is built here |
| RWB-P7-E2024-APP and the decision-log baseline of the service | `decision_log_entry`, its append-only trigger, its grants, the chain writer, the parameters client and the authorise path of the two reads. Reused where they have landed and built against their published set and fake; no build dependency of this story (ASM-2318) |

Business preconditions carried from RWB-E2-043 and from the target design:

- The reference run `ref-case-RW-2026-000777` of the synthetic case `RW-2026-000777` writes one `DecisionRecorded` fact per decision step on `rwb.decision-record.v1`, keyed by `CASE_EVENT:EV-CASE-0777-01` to `CASE_EVENT:EV-CASE-0777-05`; the steps themselves are RWB-P3-E2043-APP's (legacy sections 4 and 7).
- Package RESTRUCTURE version "RES-2026.12" is in force from 2026-12-01 with rule R-RES-04 moving IN_FCR_QUEUE on CASE_PICKED_UP to WITH_FCR_OFFICER; version "RES-2027.01" is in force from 2027-01-01 (legacy sections 3, 7 and 8).
- The synthetic case `RW-2026-000777` exists in the DEV and SIT data and is marked synthetic; no live case is used (legacy section 3).
- The two reads carry the access TSD P7 v2 T-A.1 fixes for them: capability area `DECISION_LOG`, right `R`, scope applied. Every role of TSD P7 v2 T6.1 holds `R` on the decision log; a role outside that matrix holds none.
- The chain-check outcome goes to Compliance and to RW-AUDIT; NFR-035 fixes the daily frequency and the same-day report, and no source fixes the report's shape (GAP-1309; ASM-2319).
- Synthetic data only: keys, case IDs, rule IDs, version labels, decision codes, times and hashes, never a name, an account number or a live decision (legacy section 17).
- No build dependency and no integration dependency. Day 1: the story builds against RWB-P3-E2043-CON and the platform contracts of section 13, and against their fakes.

### 4. Flow

1. `rwb-case` (P3, RWB-P3-E2043-APP): runs the reference step, evaluates the package in an activity, and writes the decision record and the state change in one transaction with the `DecisionRecorded` outbox row keyed by the case ID (design slide 14). None of that is built here.
2. The outbox relay of the producing service publishes `rwb.decision-record.DecisionRecorded.v1` with the CloudEvents 1.0 headers, the event ID, the idempotency key and the case ID as the key (DP-09; Arch v5 slides 11 and 42).
3. `DecisionLedgerIngestListener`: reads the fact, writes the inbox row of `processed_event` keyed by the event ID, and stops there when the event ID is already present; when the event ID is new but the idempotency key is not, the ledger's unique key on the source entry reference holds. Either way the listener answers with the entry ID it holds and appends nothing (BR6, BR7).
4. `DecisionLedgerRecorder`: reads LOV-DECISION, LOV-APPROVAL-LEVEL and the final call list through DP-07 and the two ledger values through the parameters client of the baseline, at the version in force on the business date, and composes the entry from the fact: case, decision code, rule ID and rule version as carried, inputs reference, recommendation, approver and level where named, final call, actions, outcome, actor and decided time. A fact outside the schema of section 11 is refused.
5. `DecisionLogAppender`, one transaction in `rwb_decision`: takes the next `chain_seq`, computes `prev_hash` from the last `entry_hash`, computes `entry_hash` as the SHA-256 of the canonical form, writes the `decision_log_entry` row with its source reference, and writes the outbox row of the append. A failed append leaves no entry, no chain position and no inbox row, so the fact is redelivered (BR2, BR12).
6. `DecisionLedgerCompletenessChecker`, on the window of the five-minute target: reports a fact of a case with no entry inside the target as a completeness gap with the case, the key and the age, and never invents or amends an entry (BR10).
7. JOB-14: the chain-check Schedule runs at 02:00 on `rwb-decision` (Arch v5 slide 44; DP-10). `ChainCheckActivity` walks from `chain_seq` 1 to the last, recomputes every `entry_hash`, compares every `prev_hash` with the entry before it and confirms the first is 64 zeros; the result holds the count, the last `chain_seq` and that entry's `entry_hash` (BR9).
8. A break — a hash that does not match, a link that does not hold, or a missing `chain_seq` — is reported the same day to Compliance and RW-AUDIT with the case, the `chain_seq` and the neighbouring hash, and the ledger is not rewritten (NFR-035).
9. RW-AUDIT, or another role holding `DECISION_LOG` R, reads the entries of a case with `GET /api/recovery/decision/v1/decision-log` and one entry with `GET /api/recovery/decision/v1/decision-log/{entryId}`, each guarded by the authorise path of DP-11 and refused with MSG-P4-002 or MSG-P4-003 (BR11).
10. Nothing else moves: the entry is appended beside the decision and changes no case, task, state or package; the two reads are the only operations this story publishes (BR8).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A fact carries a rule ID with an empty rule version, or a decision code outside the list in force | The append is refused for that fact, nothing is written, the refusal names the field, and the fact goes to the retry topic of the consumer and then to the dead-letter topic with its alert | MSG-P7-009 | AC4, TC-E2-043-04 |
| X2 | The same fact is delivered twice, or a second delivery carries a new event ID under the same idempotency key | One entry exists; the listener answers with the entry ID it holds and adds one to the repeat count for R-UNI-40; the chain is unchanged | None | AC3, TC-E2-043-03 |
| X3 | The decision-record library is unavailable, or the chain position cannot be taken | Nothing is written: no entry, no `chain_seq` and no inbox row; the fact is redelivered by the broker and an incident is raised | MSG-P7-003 | AC4, TC-E2-043-04 |
| X4 | A fact of a case has no entry inside the five-minute target | The case is reported as a completeness gap with the key and the age; no entry is invented, amended or back-dated, and the fact is still collected when it arrives | MSG-GEN-006 | AC5, TC-E2-043-05 |
| X5 | JOB-14 finds a hash that does not match, a `prev_hash` that does not link, or a missing `chain_seq` | A break is reported the same day to Compliance and RW-AUDIT with the case and the sequence; the ledger is not rewritten and no entry is inserted to fill the gap | MSG-GEN-006 | AC6, TC-E2-043-06 |
| X6 | A caller holds no `DECISION_LOG` right, or asks for a case or an entry outside its scope | 403 with MSG-P4-002, or 404 with MSG-P4-003; nothing is returned | MSG-P4-002, MSG-P4-003 | AC8, TC-E2-043-07 |
| X7 | A fact carries a personal-data field outside the schema — a name, an account number, a contact point | The append is refused, the fact is dead-lettered with an alert and the field is named in the incident, never copied into a log line | MSG-P7-009 | TC-E2-043-04 |
| X8 | A correction arrives for an entry that exists | A new entry is appended with `corrects_entry_id` naming the corrected entry; the corrected entry is unchanged and both stay in the chain | None | TC-E2-043-01 |
| X9 | Two consumers of the same partition attempt the chain head at once | The ledger serialises the head, one of them takes the next `chain_seq` and the other retries and appends after it; no two entries share a `chain_seq` | None | TC-E2-043-01 |
| X10 | An entry is amended or deleted through the service login or through the schema owner role | All statements are refused — by the missing `UPDATE` and `DELETE` grant for the service login and by the append-only rule of the table — and the refused attempts are written to the ACE audit log | None | TC-E2-043-01 |

The entry, its chain position and its outbox row commit together, so a fact can never leave a half record and an entry can never exist for a decision the owning service did not take (BR13). A refusal writes nothing at all: no chain position is consumed, so a refused fact does not create a gap that JOB-14 would then have to explain.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P3-E2043-CON, the platform libraries of its DP table and the decision-log baseline; it builds no workflow, no activity of the reference run, no fixture, no worker and no evaluation. **The Temporal worker, `ReferenceCaseWorkflow`, `EvaluateRulesActivity`, `RecordAndApplyActivity`, the signal relay, the synthetic case fixture and the replay gate are RWB-P3-E2043-APP's and RWB-P3-E2043-OPS's, the embedded Drools kit is RWB-PLT-E1072-CON's, and the cross-service proof is RWB-ITG-E2043-ITG's** |
| Negotiable | The decision code, the final call set and the approval level are reference data of their owner; the two ledger parameter names, the fact payload and the break report's shape are agreed with the owners; the story fixes only the append, the chain, the dedupe, the target, the check and the two reads |
| Valuable | Every decision of the reference run is one immutable, chained row that an auditor reaches by an operation of this service, with the rule and the version that decided it |
| Estimable | One listener with the inbox, one recorder, one appender with the chain, one completeness checker, one Schedule and one chain-check activity, one query controller with two operations, one migration and one fake set |
| Small | Fits one sprint with its tests; it is the ledger slice of the legacy key |
| Testable | Each criterion of section 7 runs as one automated test on the contract fakes with a fixed business date, a fixed chain and a fixed set of facts |

### 7. Acceptance criteria

```gherkin
Feature: Temporal and Drools integration pattern and reference case workflow — the rwb-decision central decision ledger

  Background:
    Given the environment is SIT with synthetic data and no live case
    Given the rwb-case reference-data contract mock returns LOV-DECISION in force with its version
    Given the parameters of the decision-log baseline return the collection target of 5 minutes and the chain-check time of 02:00
    Given package RESTRUCTURE version "RES-2026.12" is in force from 2026-12-01 and rule R-RES-04 decided the route move of the reference run
    Given the reference run "ref-case-RW-2026-000777" of case "RW-2026-000777" publishes one DecisionRecorded fact per decision step on rwb.decision-record.v1

  Scenario: AC1 Each reference-case step becomes one chained entry that keeps its rule and version (new, D-RCV-60)
    Given the DecisionRecorded facts of the reference run for the keys "CASE_EVENT:EV-CASE-0777-01", "CASE_EVENT:EV-CASE-0777-03" and "CASE_EVENT:EV-CASE-0777-04", each carrying caseId "RW-2026-000777", ruleId "R-RES-04", ruleVersion "RES-2026.12", an inputsRef, an actor reference, a final call and the decision code the package's route move carries
    When the three facts are consumed from rwb.decision-record.v1
    Then three decision_log_entry rows exist in rwb_decision for case "RW-2026-000777", one per key and no more
    Then each entry carries ruleId "R-RES-04" and ruleVersion "RES-2026.12" exactly as the fact carried them, and the decision code is a member of LOV-DECISION in force
    Then each entry holds its inputsRef, the recommendation, the final call, the actions, the outcome, the actor reference and decidedAt
    Then the entries carry chain_seq 1, 2 and 3, the first prevHash is 64 zeros, and every prevHash equals the entryHash of the entry before it
    Then every entryHash equals the SHA-256 of the entry's canonical form
    When RW-AUDIT reads GET /api/recovery/decision/v1/decision-log with caseId "RW-2026-000777"
    Then the answer is 200 with the three entries in chain order, and GET /api/recovery/decision/v1/decision-log/{entryId} returns one entry with its rule, its version, its inputsRef and its two hashes
    Then a statement that changes, or a DELETE, on one of the three entries is refused through the rwb-decision login (DP-02) and through the schema owner role, and the entry is unchanged

  Scenario: AC2 The version is carried unchanged and the ledger substitutes none (new, D-RCV-60)
    Given the fact of the key "CASE_EVENT:EV-CASE-0777-04" carries ruleVersion "RES-2026.12" as pinned by the evaluation of the reference run
    Given package version "RES-2027.01" is in force from 2027-01-01
    When that fact is consumed after 2027-01-01
    Then its entry carries ruleVersion "RES-2026.12" and not "RES-2027.01"
    Then the ledger asks no registry for the version in force and holds no default version
    And a later fact of the run that carries ruleVersion "RES-2027.01" gets its own entry with that version and the next chain_seq
    And the two entries stand side by side on the case with different rule versions and neither is amended

  Scenario: AC3 A redelivered fact writes no second entry (new, D-RCV-60)
    Given the three entries of AC1 exist for case "RW-2026-000777" with the last chain_seq 3 and its entryHash
    When the fact of the key "CASE_EVENT:EV-CASE-0777-01" is delivered again with the same event ID
    And the same decision is delivered again with a new event ID and the same idempotency key
    Then no second decision_log_entry is written for the key and the case still holds three entries
    Then the listener answers with the entry ID it holds, "DLE-SYN-3012", and appends nothing
    Then the repeat count of the key for R-UNI-40 is 2
    Then the chain is unchanged: the last chain_seq is still 3 and its entryHash is the one of AC1

  Scenario: AC4 A fact the ledger cannot accept leaves nothing (new, D-RCV-60)
    Given a fact of the run carrying ruleId "R-RES-04" and an empty ruleVersion
    When it is consumed
    Then the append is refused with MSG-P7-009 naming "ruleVersion", and no entry, no chain_seq and no inbox row is written
    Given a fact of the run carrying decision code "D99"
    When it is consumed
    Then the append is refused with MSG-P7-009 naming "decisionCode", and the retry topics and the dead-letter topic carry the fact with an alert
    Given the decision-record library is forced to fail the append
    When the fact of the key "CASE_EVENT:EV-CASE-0777-01" is consumed
    Then the answer is MSG-P7-003, no entry and no chain_seq is written, and an incident is raised for the platform administrator queue
    Then the fact is redelivered and collected once the library answers again, and the case then holds its entry

  Scenario: AC5 The entry is in the ledger inside the collection target and a gap is reported (new, D-RCV-60)
    Given the fact of the key "CASE_EVENT:EV-CASE-0777-01" is published at 2026-12-01T06:10+07:00 and reaches the ledger at 06:11
    Then the entry is in rwb_decision with decidedAt 2026-12-01T06:10+07:00 and an ingest lag of 60 seconds
    And the case counts as complete for the target of 5 minutes
    Given the fact of the key "CASE_EVENT:EV-CASE-0777-03" is published at 2026-12-01T06:20+07:00 and reaches the ledger at 06:31
    Then the case is reported as a completeness gap of 11 minutes, naming the case, the key and the age
    Then no entry is invented, amended or back-dated for the key, and the entry is written when the fact arrives
    Then the target of 5 minutes is read from its parameter and never from a constant

  Scenario: AC6 JOB-14 checks the chain at 02:00 and a break is reported the same day (new, D-RCV-60)
    Given the ledger holds 100 chained entries, chain_seq 1 to 100, and every prevHash links to the entryHash of the entry before it
    When the JOB-14 hash-chain check runs at 02:00 on the rwb-decision queue
    Then the result holds count 100, last chain_seq 100 and the entryHash of that entry
    And no break is reported and the run carries its start time and its end time
    Given a chain fixture in which the entry of chain_seq 57 is absent, as a restore from a partial backup leaves it
    When JOB-14 runs again
    Then a break is reported the same day to Compliance and RW-AUDIT with the case, the missing chain_seq 57 and the entryHash of chain_seq 56
    Then the ledger is not rewritten and no entry is inserted to fill the gap
    Then the Schedule skips a run that overlaps the previous one and catches up the missed run inside its window

  Scenario: AC7 The order evaluate, record, act is provable from the ledger (new, D-RCV-60)
    Given the rwb-case contract mock returns case "RW-2026-000777" with route state "WITH_FCR_OFFICER" and routeStateChangedAt 2026-12-01T06:12+07:00
    Given the entry of the key "CASE_EVENT:EV-CASE-0777-01" carries ruleId "R-RES-04", ruleVersion "RES-2026.12" and decidedAt 2026-12-01T06:11+07:00
    When RW-AUDIT reads the entry and the case
    Then the entry's decidedAt precedes routeStateChangedAt, so the record exists before the state moved
    And the rule and the version on the entry are the ones the reference run's evaluation produced, unchanged
    And no entry of the case has a decidedAt after the state change it explains
    And the key "CASE_EVENT:EV-CASE-0777-05", which reached no decision because the signal never arrived, holds no entry

  Scenario: AC8 The two reads answer by case, rule, approver and date and refuse what they must (new, D-RCV-60)
    Given the three entries of AC1 and one further entry of the case carrying approverUserId "U-6101" and approvalLevel "L6"
    When RW-AUDIT reads GET /api/recovery/decision/v1/decision-log with caseId "RW-2026-000777", ruleId "R-RES-04", approver "U-6101", from 2026-12-01 to 2026-12-02, page 0 and size 200
    Then the answer is 200 with items, page, size and total, and only the entries that match every filter
    When a role without the DECISION_LOG right calls the same operation
    Then the answer is 403 with MSG-P4-002 and nothing is returned
    When an entry outside the caller's scope, or an unknown entry ID, is read with GET /api/recovery/decision/v1/decision-log/{entryId}
    Then the answer is 404 with MSG-P4-003
    When the read is asked with size 201
    Then the answer is 422 with MSG-GEN-002 for "size" between 1 and 200
```

These eight criteria are new under D-RCV-60 and test only the ledger and the decision-record deliverable of this key. `acs` is empty for this story: no legacy criterion of RWB-E2-043 is owned verbatim here, because every legacy criterion asserts the order of the workflow, its retries, its pinned result, its outbox or its flag, and those belong to RWB-P3-E2043-APP and RWB-P3-E2043-OPS. The values are the legacy and target values — the synthetic case `RW-2026-000777`, the workflow ID `ref-case-RW-2026-000777`, the events `EV-CASE-0777-01` to `EV-CASE-0777-05` with their `CASE_EVENT:` keys, the package versions "RES-2026.12" from 2026-12-01 and "RES-2027.01" from 2027-01-01, rule R-RES-04, the route states IN_FCR_QUEUE and WITH_FCR_OFFICER, the entry ID shape "DLE-SYN-3012" of FSD P7 v3 A2.29, the business date 2026-12-01 of FSD P7 v3 A2.29, the approver "U-6101" and level "L6" of FSD P7 v3 AC-ALT-P7-001-02, the collection target of 5 minutes of Arch v5 slide 28, the chain check of 02:00 and the 100-entry chain of FSD P7 v3 AC-ALT-P7-001-01 — and no new business value is introduced. The decision code of a reference-case step, the payload of `DecisionRecorded`, the two parameter names, the login name and the break report's shape are Not specified in the source documents (GAP-1304; ASM-2314), (GAP-1305; ASM-2315), (GAP-1306; ASM-2316), (GAP-1307; ASM-2317) and (GAP-1309; ASM-2319).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The central decision ledger is `rwb-decision`'s, and it holds one entry per decision the services publish; no other service reads `decision_log_entry` and this service reads no other service's table | Arch v5 slides 27, 28 and 41; DP-01; ownership.json `decision_log_entry` |
| BR2 | An entry is append only and hash chained: `entry_hash` is the SHA-256 of the entry's canonical form, `prev_hash` is the `entry_hash` of the entry before it, the first `prev_hash` is 64 zeros, an `UPDATE` and a `DELETE` are refused and a correction is a new entry naming the corrected one in `corrects_entry_id` | FSD P7 v3 A2.1 AC-P7-001-01 and AC-ALT-P7-001-01; REQ-DRI-002; REQ-DRI-003; FEAT-DRI-01 |
| BR3 | The entry carries the fields of the decision record of Arch v5 slide 28 and TSD P7 v2 T3.1: the case, the decision code, the rule ID and rule version, the model and agent versions where the fact names them, the inputs reference, the recommendation, the approver and approval level, the final call, the override reason, the actions, the outcome, the decided time, the chain position, the two hashes, the actor and the idempotency key | TSD P7 v2 T3.1 `decision_log_entry`; Arch v5 slide 28; legacy section 11 |
| BR4 | The rule ID and the rule version are written exactly as the fact carries them; the ledger looks up no version in force, applies no default and substitutes nothing, so an entry recorded under an earlier version keeps it after a later version is promoted | R-UNI-38; design slides 6, 15 and 27; REQ-CWC-016 |
| BR5 | A fact that carries a rule ID with no rule version, or a decision code outside the list in force, is refused with MSG-P7-009 naming the field, and nothing is written | FSD P7 v3 A2.2.4.3 AC-EXC-P7-002-01 and AC-EXC-P7-002-05; BR-P7-001; DP-07 |
| BR6 | One entry per fact: the inbox dedupe by event ID and the ledger's unique key on the source entry reference make a second entry impossible, and the repeat is counted for R-UNI-40 | FSD P7 v3 AC-EXC-P7-002-03; R-UNI-40; DP-09 |
| BR7 | A repeated delivery answers with the entry ID the ledger already holds, so the producer's retry is idempotent end to end | R-UNI-40; legacy BR3; DP-09 |
| BR8 | The story records and exposes; it changes no case, no task, no state, no package and no approval, and its only operations are the two reads | Arch v5 slides 14 and 41; legacy section 19 |
| BR9 | JOB-14 checks the whole chain every day at 02:00 and a break is reported to Compliance the same day; the check rewrites nothing and inserts nothing | NFR-035; REQ-DRI-003; FSD P7 v3 A2.1.4.4 AC-BG-P7-001-01; Arch v5 slide 44 |
| BR10 | The collection target is five minutes: a fact of a case that has no entry inside the target is reported as a completeness gap with the case, the key and the age, and no entry is invented, amended or back-dated | Arch v5 slide 28; ASM-2315 |
| BR11 | The two reads declare capability area `DECISION_LOG` and right `R` with the scope applied; a role outside the matrix is refused with MSG-P4-002, an entry out of scope with MSG-P4-003, and the page size stays between 1 and 200 | TSD P7 v2 T-A.1, T-A.2 and T6.1; FSD P7 v3 A2.28 AC-EXC-P7-028-02 |
| BR12 | The entry, its chain position and its outbox row are written in one transaction; a failed append leaves nothing and the fact is redelivered | R-UNI-39; principle 5; DP-03 |
| BR13 | The decision code, the final call values and the approval level are reference data of `rwb-case` read at the version in force; no code and no state is a constant of this service | FSD P7 v3 A2.14.3.2 field catalogue; BR-P7-001; DP-07 |
| BR14 | No personal data in the entry, the fact, the outbox row or a log line: references, codes, versions, times and hashes only, and a fact that carries a personal-data field is refused and dead-lettered | Legacy BR5 and section 17; NFR-034; design slide 27; DP-09 |
| BR15 | The collection is continuous Kafka and is not a schedule; JOB-13 is the ingest and JOB-14 is the check, and the daily seal of the ledger hash to write-once storage is the step of Arch v5 slide 28 that sits outside this story | Arch v5 slides 28 and 44; GAP-1310 |

Target-service statements that make the rules hold in `rwb_decision`:

- BR1 is the schema boundary: the entry lives in `rwb_decision`, the facts arrive on `rwb.decision-record.v1`, and no table of `rwb_document`, `rwb_case` or `rwb_access` is read (DP-01).
- BR2 is the table's trigger `tr_declog_append_only` plus the missing `UPDATE` and `DELETE` grant for the service login, inherited from the decision-log baseline, and the chain writer that computes the two hashes.
- BR3, BR4 and BR13 are the entry composition: the T3.1 columns filled from the fact, with `rule_id` and `rule_version` copied and never resolved, and one read of DP-07 at the version in force.
- BR6 and BR7 are the `processed_event` inbox keyed by event ID plus the partial unique key `ux_declog_source_entry` on the source service and the source entry reference.
- BR9 and BR10 are `ChainCheckService` and the completeness checker, with their two values read as parameters; BR11 is the guard the baseline already carries, on which this story declares only the area and the right.
- BR12 and BR14 are the single transaction of `DecisionLogAppender`, the fail-closed mapping of `DecisionLogUnavailableException` to MSG-P7-003, and the schema check that refuses a personal-data field before anything is written.

### 9. State transitions

The story changes no case status, no route state, no task and no package version; those belong to `rwb-case` and to the registry. The states below are the states of an entry, and an entry has no state column of its own: it is appended and then immutable.

| From | Event | Condition | To |
|---|---|---|---|
| Absent | A `DecisionRecorded` fact arrives | The decision code, the rule version and the case are readable at the version in force | Appended with the next `chain_seq`, its `prev_hash` and its `entry_hash`, in one transaction with its outbox row |
| Absent | A `DecisionRecorded` fact arrives | The decision code is unknown, the rule ID has no version, or the fact carries a field outside the schema | Absent: refused with MSG-P7-009, nothing written, the fact dead-lettered with its alert |
| Absent | A `DecisionRecorded` fact arrives | The library is unavailable or the chain head cannot be taken | Absent: MSG-P7-003, no chain position consumed, the fact redelivered, an incident raised |
| Absent | The same fact arrives again with the same event ID or the same idempotency key | The inbox or the unique key holds the entry | Absent: the first entry's ID is returned and the repeat is counted |
| Appended | A correction of the decision is taken | The correction names the entry it corrects | A new entry is appended with `corrects_entry_id`; the corrected entry is unchanged |
| Appended | An `UPDATE` or a `DELETE` is attempted | Any caller, including the schema owner role | Unchanged: the statement is refused by the append-only rule |
| Appended | JOB-14 runs | The chain links from `chain_seq` 1 to the last | Unchanged: the run reports count, last `chain_seq` and last `entry_hash` |
| Appended | JOB-14 runs | A hash does not match, a `prev_hash` does not link, or a `chain_seq` is missing | Unchanged: a break is reported the same day; no row is rewritten and no row is inserted |

A completeness gap does not put an entry into a state either: the entry simply is not there yet, the case is reported as a gap, and the fact is collected when it arrives (BR10).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-AUDIT, internal audit | Reads the entries of a case and one entry with its inputs reference, its versions and its chain position (`DECISION_LOG` R, scope `ALL`), and receives the break report of JOB-14 |
| RW-COMPLY, Compliance and PDPA officer | Reads the same entries and receives the same-day break report (`DECISION_LOG` R) |
| RW-CASEOWN, case owner | Reads the entries of the cases in own scope; shows them beside the case (`DECISION_LOG` R) |
| RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COE and every other role of TSD P7 v2 T6.1 | Holds `R` on the decision log and reads the entries of the cases in its scope |
| A role outside the T6.1 matrix | Refused with MSG-P4-002 on both reads; nothing is returned |
| RW-PLATADM, platform administrator | Reads the JOB-14 run in the job monitor, receives the incident of a failed append and of a chain break, and takes no decision on an entry |
| RW-COE, center of excellence analyst | Owns the RESTRUCTURE versions and rule R-RES-04 the reference uses; this story records their identifiers on an entry and changes neither |
| The `rwb-decision` service identity | Consumes the fact, takes the inbox row and the chain position, and appends the entry and its outbox row (DP-02) |
| SY-DECLOG, decision log writer | Supplies the hash-chained record write, the `prev_hash` and the `entry_hash` of DP-03 |
| SY-RULES, Drools evaluator | Produces the rule ID and the package version inside the reference workflow's activity, in `rwb-case`; the ledger only carries them |
| No delegation of authority level applies | The ledger takes no credit decision and approves nothing; the approval level and the approver on an entry are facts the owning service recorded |

The authorisation behind the two reads is `rwb-access`'s role, scope and right data, taken through the guard the decision-log baseline already carries (DP-11); this story adds no guard of its own and holds no role, scope or delegation row. The database login is per service (DP-02) and its name is Not specified in the source documents (GAP-1307; ASM-2317); the story refers to "the rwb-decision login (DP-02)".

### 11. Data

| BR Field ID | Entity in `rwb_decision` | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 | `decision_log_entry` | id | Write, the ledger's own entry ID, returned to the producer on a repeat |
| DF-DEC-002 | `decision_log_entry` | case_id (the case of the reference step) | Write |
| DF-DEC-003 | `decision_log_entry` | decision_code | Write, from the fact, a member of LOV-DECISION |
| DF-DEC-004 | `decision_log_entry` | rule_id ("R-RES-04" for the reference route move) | Write, unchanged from the fact |
| DF-DEC-005 | `decision_log_entry` | rule_version ("RES-2026.12", or "RES-2027.01" after 2027-01-01) | Write, unchanged from the fact |
| DF-DEC-006 | `decision_log_entry` | model_version | Write where the fact names a model; the reference route move names none |
| DF-DEC-007 | `decision_log_entry` | agent_version | Write where the fact names an agent; no agent runs on the reference path |
| DF-DEC-008 | `decision_log_entry` | inputs_ref (the inputs snapshot the owning service recorded) | Write |
| DF-DEC-009 | `decision_log_entry` | recommendation | Write where the fact carries it |
| DF-DEC-010 | `decision_log_entry` | approver_user_id | Write where the fact names an approver; the reference route move carries none |
| DF-DEC-011 | `decision_log_entry` | approval_level | Write where the fact names a level, a member of LOV-APPROVAL-LEVEL |
| DF-DEC-012 | `decision_log_entry` | final_call | Write |
| DF-DEC-013 | `decision_log_entry` | override_reason | Write where the fact carries one |
| DF-DEC-014 | `decision_log_entry` | actions | Write |
| DF-DEC-015 | `decision_log_entry` | outcome | Write where the fact carries one |
| DF-DEC-016 | `decision_log_entry` | decided_at (the owning service's time, not the ingest time) | Write |
| DF-DEC-017 | `decision_log_entry` | prev_hash | Write |
| DF-DEC-018 | `decision_log_entry` | entry_hash | Write |
| DF-DEC-028 | `decision_log_entry` | chain_seq | Write |
| DF-DEC-029 | `decision_log_entry` | corrects_entry_id | Write on a correction only |
| DF-DEC-030 | `decision_log_entry` | actor_user_id (the actor the fact names, or the service identity of a system step) | Write |
| DF-DEC-031 | `decision_log_entry` | idempotency_key (the key of the fact) | Write; read by the dedupe |
| (assumed columns) | `decision_log_entry` | source_service, source_entry_ref, ingest_at | Write; Not specified in the source documents (GAP-1304; ASM-2314) |
| (inbox) | `processed_event` | event_id, consumer, processed_at | Write |
| (outbox) | outbox library table in `rwb_decision` | the append row | Write |
| — | `rwb_case` reference data | LOV-DECISION, LOV-APPROVAL-LEVEL and the final call list with the version in force | Read through the reference-data contract of DP-07, never a table |
| — | `rwb_case` parameters | the collection target of 5 minutes and the chain-check time of 02:00 | Read through the parameters client of the baseline, never a table |
| — | `rule_package_version`, `rule_row` (P7, same schema) | rule_id, rule_version, package version window | Not read by the ingest: the identifiers are carried on the fact (BR4). Read by the registry's own stories |

Field IDs are those of the Logical Data Model and Data Dictionary v9 and TSD P7 v2 T3.1. The ledger adds no business field: it copies the record fields of Arch v5 slide 28 and adds the three ingest columns of the assumed shape of section 12.4, which are a source reference and a collection time and nothing else. No row of `recovery_case`, `task`, `timer`, `document`, `role`, `permission`, `parameter_value` or `reference_row` is copied into `rwb_decision`: the facts arrive on `rwb.decision-record.v1` and the lists on their contract. The decisions of the reference run are synthetic and hold no personal data (BR14).

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-decision` (P7); base `/api/recovery/decision/v1`. Both paths are the ones TSD P7 v2 T-A.1 carries (API-P7-006 and API-P7-007); this story fills them with the entries of the central ledger and adds no third path. The answer field set of the two operations is fixed by T-A.2 only as `DecisionLogPage` and `DecisionLogEntry`, so the body this story reads is the field list below and its exact types are Not specified in the source documents (GAP-1304; ASM-2314).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/decision-log` | API-P7-006: search the decision log by `caseId`, `decision`, `ruleId`, `approver`, `from`, `to`, `page` and `size`; 200 with the DecisionLogPage | Decision log, right `R`, scope applied through the guard of DP-11 | Not applicable, read only |
| GET | `/decision-log/{entryId}` | API-P7-007: read one entry with its inputs reference, its versions, its final call, its actions, its outcome and its two hashes; 200 with the DecisionLogEntry | Decision log, right `R`, scope applied | Not applicable, read only |

The `DecisionLogPage` body carries `items`, `page`, `size` and `total`, with `size` between 1 and 200. The `DecisionLogEntry` body carries `entryId`, `chainSeq`, `caseId`, `decisionCode`, `ruleId`, `ruleVersion`, `modelVersion`, `agentVersion`, `inputsRef`, `recommendation`, `approverUserId`, `approvalLevel`, `finalCall`, `overrideReason`, `actions`, `outcome`, `decidedAt`, `ingestAt`, `sourceService`, `sourceEntryRef`, `prevHash`, `entryHash`, `correctsEntryId` and `actorUserId` — the T3.1 columns of the entry plus the three ingest columns assumed in section 11.

Errors: 401 no session; 403 the role lacks the right (MSG-P4-002); 404 the entry or the case is absent or out of scope (MSG-P4-003); 422 a query value is outside its list, or `size` is above 200 (MSG-GEN-002); 503 the ledger is unavailable (MSG-GEN-006). Every error is an RFC 9457 problem response with `messageId` set. No write operation is published: the ledger has no producer-facing endpoint, because its producer is the topic.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case, on RWB-P3-E1043-CON | LOV-DECISION, LOV-APPROVAL-LEVEL and the final call list with the version in force (DP-07); faked, one hop, 2 s (DP-11) |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case, on the parameters contract of the decision-log baseline | The collection target of 5 minutes and the chain-check time of 02:00 with the version in force (Arch v5 slides 28 and 44); faked. The parameters contract is the one the ledger baseline already consumes; its parameter names are Not specified in the source documents (GAP-1305; ASM-2315) |

The authorise answer behind the two reads is taken through the guard library of the decision-log baseline (DP-11) and is not a row of this table. The fact arrives on `rwb.decision-record.v1` and not over REST. The contract dependency recorded on the story is RWB-P3-E2043-CON, which fixes the producing side of the reference run; the platform and published contracts the DP table adds are listed in section 13 and carried in the gap of GAP-1308.

#### 12.3 Events published

None. This story publishes no event of its own. The entries of the central ledger are read through the operations of 12.1 and are not announced on a topic. `DecisionRecorded` on `rwb.decision-record.v1` is published by each of the 19 services for its own decisions and this service is its consumer (Arch v5 slide 42). `ApprovalRequested`, `ApprovalDecided` and `RulePackageInForce` of `rwb.decision.events.v1` belong to the approval and rule-registry stories of this service and are not touched here.

#### 12.4 Events consumed

| Event | Topic | Owner | Handler |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 ledger library; published by all 19 services for their own decisions | `DecisionLedgerIngestListener`: inbox dedupe by event ID, then `DecisionLedgerRecorder` and `DecisionLogAppender` for the entry of the decision |

The fact carries the record of Arch v5 slide 28 — the chain position, the inputs reference, the rule ID, the rule version, the recommendation, the approver and the approval level, the final call, the actions, the outcome, the decided time, `prev_hash` and `entry_hash` — plus the CloudEvents envelope and the case ID as the key. The envelope the consumer needs is the event ID, the idempotency key, the source service, the source entry reference, the case ID and the `synthetic` flag of the reference run. Which of those fields travel on the topic, and whether the entry ID is the producer's or the ledger's, is Not specified in the source documents (GAP-1304; ASM-2314); the reading this story applies is that of ASM-2314, and the ledger keys its row on the source entry reference so that a producer retry is idempotent end to end.

No other topic is consumed. `rwb.decision.events.v1` belongs to the service's approval and registry stories, and the case events of `rwb.case.events.v1` reach the reference workflow through the case router and never through this service.

#### 12.5 Workflows and activities

None of the reference run is here: `ReferenceCaseWorkflow`, `EvaluateRulesActivity`, `RecordAndApplyActivity` and the signal relay are RWB-P3-E2043-APP's, on the `rwb-case` queue. This story registers one activity, for its own Schedule, and no workflow.

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| `ChainCheckActivity` | Activity, started by the JOB-14 Schedule | `rwb-decision` | Walks the ledger from `chain_seq` 1 to the last, recomputes every `entry_hash`, checks every `prev_hash` and reports a break |
| `DecisionLedgerIngestListener` | Kafka consumer with the inbox, not a worker | not a worker | Reads the fact, deduplicates it and appends the entry |

The worker that runs the activity is the service template's (RWB-PLT-E1071-CON) and the story adds no worker of its own. No workflow state is created by this story, and the Temporal Web UI is read only for the JOB-14 run.

#### 12.6 Schedules

| Schedule | When | Mechanism | Owner and this story's part |
|---|---|---|---|
| JOB-14 Hash-chain check | 02:00 daily | A Temporal Schedule on the `rwb-decision` queue that runs `ChainCheckActivity` with the overlap policy SKIP and a catch-up window, walks the chain and reports a break the same day (Arch v5 slide 44; NFR-035) | P7 rwb-decision, decision-log baseline. This story registers the Schedule and the activity and asserts the run in AC6 |
| JOB-13 Decision log copy | Continuous | Not a Schedule: the ingest of `rwb.decision-record.v1` is continuous Kafka and the job map states it as such (Arch v5 slide 44) | The ingest of this story; no clock and no trigger |
| JOB-20 Rule promote | 00:01 daily | The registry's Schedule on the same queue (RWB-P7-E2027-APP) | Not this story's; it shares the queue and the worker |

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `decision_log_entry` | P7 (`rwb_decision`) | The entry of each decision: the T3.1 columns, the chain position, the two hashes, the source reference and the ingest time; append only |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_decision` | The outbox row of the append, the inbox row of the fact and the idempotency key of the repeat (DP-09) |

Not owned and never read: `recovery_case`, `task`, `timer`, `parameter_value`, `reference_row` and `lov_value` (P3); `role`, `permission` and `delegation_limit` (P4); `document` and `retention_rule` (P5); `agent_run` and the agent tables (P10); `write_off` (S7); `proceeds` (P8); `approval`, `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are P7 but are not touched by this story — the identifiers arrive on the fact and the registry's own stories write them. No foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| decision-record topic stub | `rwb.decision-record.v1`, DP-03 and DP-09 | The `DecisionRecorded` facts of the reference run for the keys `CASE_EVENT:EV-CASE-0777-01`, `-03` and `-04` with rule `R-RES-04` and version `RES-2026.12`; a fact carrying `RES-2027.01`; a fact with an empty rule version; a fact with decision code `D99`; a fact carrying a personal-data field; the same fact replayed under the same event ID and under the same idempotency key |
| decision-record library fake | RWB-PLT-E1027-CON | The append, the next `chain_seq`, the `prev_hash`, the `entry_hash` over the canonical form, the first `prev_hash` of 64 zeros, the append-only refusal and the forced failure that raises `DecisionLogUnavailableException` |
| `rwb-case` reference-data fake | RWB-P3-E1043-CON, DP-07 | LOV-DECISION in force with the route-move code, LOV-APPROVAL-LEVEL with `L6`, the final call list, and an unknown list for the refusal case |
| `rwb-case` parameters fake | parameters contract of the baseline | The collection target of 5 minutes and the chain-check time of 02:00 with the version in force, and an unavailable answer |
| `rwb-case` case-read fake | RWB-P3-E2043-CON | Case `RW-2026-000777` at route state `WITH_FCR_OFFICER` with `routeStateChangedAt` 2026-12-01T06:12+07:00, for AC7 |
| `rwb-access` authorise fake | guard of the decision-log baseline, DP-11 | The allow answer for `DECISION_LOG` right `R` in scope, the refusal with MSG-P4-002 for a role without the right, and 404 with MSG-P4-003 for an entry out of scope |
| chain-check fixture | JOB-14 | A chain of 100 entries that links, and a variant in which the entry of `chain_seq` 57 is absent |

Each fake is replaced by the real service as RWB-P3-E2043-APP, RWB-P7-E2024-APP and the platform libraries land, without a change to the scenarios. Every fact, case, key, entry ID and hash in the fakes is synthetic.

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2, consumed 2 | `GET /decision-log` and `GET /decision-log/{entryId}` provided; the reference lists and the parameters consumed, one hop and 2 s with a breaker per downstream |
| Kafka | Published 0, consumed 1 | `rwb.decision-record.v1` with `rwb.decision-record.DecisionRecorded.v1`; no event published and no new topic |
| Temporal | 1 activity, 1 Schedule, 0 workflows | `ChainCheckActivity` on the `rwb-decision` queue under the JOB-14 Schedule at 02:00; the reference workflow is `rwb-case`'s |
| File | None | No file input and no file output; the ledger holds rows and hashes, never a payload |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `log/ledger`, Java package `th.co.scb.ace.workbench.recovery.decision.log.ledger`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_decision`; the entries live here and no other service reads them, and no other service's table is read | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`: the ledger is the collection end of it | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit of the owning service; the ledger carries the rule ID and the package version a fact names and evaluates nothing | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | No ACE view is read: the facts arrive on the topic and no case fact is fetched from ACE | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case for the decision code, approval level and final call lists with the version in force | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library, CloudEvents envelope, the inbox dedupe, the retry topics and the dead-letter topic | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | The JOB-14 chain check as a Temporal Schedule through the workflow kit, instead of a Quartz job and a shared job table | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | One-hop REST with a mock and the 2 s timeout for the reference lists and the parameters, and the guard of the two reads | none (C from the legacy dependency) |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | Topic `rwb.decision.events.v1`, the shared `rwb.decision-record.v1` and the queue `rwb-decision` through the naming library; this story adds no topic | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | One migration in the per-service Flyway sequence of `rwb_decision`; no table of another service | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route: the route the decision-log screen reaches the two reads through; no screen is built here | H RWB-PLT-N001-CON |

How this story applies each row. **DP-01** is the boundary: `decision_log_entry` is a `rwb_decision` table, the facts arrive on the topic and the lists on their contract. **DP-03** is the reason the story exists: the owning service writes its record locally and the central ledger is the collection Arch v5 slide 28 describes, with its chain, its append-only rule and its fail-closed exception. **DP-04** is read-only here: the `RuleResult` of the embedded kit names the package code, the package version and the rule ID, and those reach the ledger on the fact; no KieBase is loaded, compiled or cached. **DP-05** has no instance: no ACE data is read, because a record names its inputs by reference. **DP-07** is LOV-DECISION, LOV-APPROVAL-LEVEL and the final call list at the version in force, and an unknown code is refused rather than stored. **DP-09** is the outbox row of the append, the inbox row of the fact, the idempotency key of the repeat and the retry and dead-letter behaviour of the consumer. **DP-10** is JOB-14 as a Schedule on `rwb-decision` with SKIP and a catch-up window, replacing the Quartz job of the monolith. **DP-11** is the two consumed operations, one hop with a 2 s budget and a breaker, and the guard the baseline carries on the two reads. **DP-14** is the topic and queue names of section 12 and the shared `rwb.decision-record.v1`, which is P7's own. **DP-15** is the one migration of the slice. **DP-19** is the composite route the reads are reached through, not built here.

The platform H dependencies of the table — H RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON — and the C dependencies C RWB-P7-E1073-CON and C RWB-P3-E1043-CON, with the authorise contract RWB-P4-E1037-CON the guard consumes, are the DP-added dependencies that are **not** in the metadata rows, which name `Depends on (build)` = None and `Contract dependencies` = RWB-P3-E2043-CON. They are recorded in GAP-1308 and ASM-2318. **Ready to start stays Day 1**: every H is a platform CON story of wave 0 or the service's own ledger baseline, and every C is a published contract built against its fake (Template and Rules §R5.4 and §R5.7).

The work of the legacy key that sits with other slices: the worker, `ReferenceCaseWorkflow`, `EvaluateRulesActivity`, `RecordAndApplyActivity`, the `CaseEventSignalRelay`, the `ref-case-` prefix, the synthetic guard and the fixture are `rwb-case`'s (RWB-P3-E2043-APP and RWB-P3-E2043-OPS); the package RESTRUCTURE versions and rule R-RES-04 are the registry's (RWB-P7-E2042-APP); the replay gate is RWB-E2-040's; and the journey across the two services and the topics is RWB-ITG-E2043-ITG's. This story builds the ledger that proves the order and nothing beside it.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DecisionLedgerIngestListener` | Kafka consumer with the inbox | Reads `DecisionRecorded`, deduplicates by event ID and idempotency key, and hands the facts to the recorder; answers the repeat with the entry ID it holds (BR6, BR7) |
| `DecisionLedgerRecorder` | Service | Composes the entry from the fact — case, decision code, rule ID and version unchanged, inputs reference, recommendation, approver and level, final call, actions, outcome, actor and decided time — at the versions in force, and decides nothing (BR3, BR4, BR13) |
| `DecisionLogAppender` | Service | Takes the next `chain_seq` under the ledger's head lock, computes `prev_hash` and `entry_hash`, and writes the entry and its outbox row in one transaction (BR2, BR12) |
| `DecisionRecordFailClosedHandler` | Service | Maps `DecisionLogUnavailableException` to MSG-P7-003, leaves no chain position consumed, and raises the incident for the platform administrator queue (X3) |
| `DecisionLedgerCompletenessChecker` | Service | Compares the facts of a case with its entries inside the five-minute target and reports a gap with the case, the key and the age (BR10) |
| `ChainCheckActivity` and `ChainCheckService` | Activity and service | Walk the chain from `chain_seq` 1 to the last, recompute every hash, verify every link, and report a break to Compliance and RW-AUDIT the same day (BR9) |
| `DecisionLogQueryController` | Controller | `GET /decision-log` and `GET /decision-log/{entryId}` with the declared area and right, the scope, the paging and the problem mapping for 401, 403, 404, 422 and 503 |
| `DecisionLogRepository` | Repository | `decision_log_entry` in `rwb_decision`, with the chain columns, the source reference, the idempotency key and the append-only rule |
| `ReferenceDataClient` | Client | LOV-DECISION, LOV-APPROVAL-LEVEL and the final call list at the version in force (DP-07) |
| `LedgerParameterClient` | Client | The collection target and the chain-check time at the version in force (DP-06 mechanism of the baseline) |
| `AccessGuardClient` | Client | The cached authorise decision behind the two reads, through the guard of the baseline (DP-11) |
| `FactSchemaCheck` | Service | Refuses a fact whose field set is outside section 11, including a personal-data field, before anything is written (BR14, X7) |

**Database and migrations**

- Writes `decision_log_entry` and the library objects, all in schema `rwb_decision`; reads no other schema (DP-01).
- One migration in the per-service Flyway sequence of DP-15, `V2043_1__decision_central_ledger.sql`: it adds the three ingest columns of section 11 — `source_service`, `source_entry_ref` and `ingest_at` — the partial unique key `ux_declog_source_entry ON decision_log_entry (source_service, source_entry_ref) WHERE source_entry_ref IS NOT NULL`, so a repeated fact is refused by the database as well as by the inbox, and the indexes the two reads need on `(case_id, decided_at)`, `(rule_id, rule_version)` and `(approver_user_id, decided_at)`. The column names and types are Not specified in the source documents (GAP-1304; ASM-2314).
- The append-only rule is the table's: the trigger `tr_declog_append_only` refuses an `UPDATE` and a `DELETE` even from the schema owner role, and the service login holds no `UPDATE` and no `DELETE` grant, as FSD P7 v3 AC-P7-001-01 fixes it.
- Where the ledger baseline of RWB-P7-E2024-APP has not landed, this migration is reconciled with that baseline at the first joint environment (ASM-2318); it creates no table of its own beyond the columns and keys above.

**Configuration and reference data**

- The collection target of 5 minutes and the chain-check time of 02:00 are parameter rows with the version in force; their names are Not specified in the source documents (GAP-1305; ASM-2315) and the story holds no default in code.
- LOV-DECISION, LOV-APPROVAL-LEVEL and the final call list are reference data of `rwb-case` read at the version in force through DP-07; the value set of LOV-DECISION is not enumerated by any source (GAP-1306; ASM-2316).
- The consumer group is `rwb-decision`, one per service; the retry topics of 1 min, 10 min and 1 h and the dead-letter topic with its alert are the platform's (RWB-PLT-TE006-CON).
- The chain-check run keeps its result and its start and end time in the operational report of the service; the report's shape, the alert route and whether the check writes an entry of its own are Not specified in the source documents (GAP-1309; ASM-2319).

**Build steps**

1. `DecisionLogRepository` and the migration, with the partial unique key on the source reference and the append-only trigger and grants; test that a second entry for the same source entry and an `UPDATE` are both refused (AC1, AC3).
2. `DecisionLedgerIngestListener` with the inbox, the dedupe by event ID and by idempotency key, the repeat count for R-UNI-40 and the answer-with-the-held-entry behaviour; test the replay and the second delivery (AC3).
3. `FactSchemaCheck` and `DecisionLedgerRecorder` with `ReferenceDataClient`: the entry composed from the fact, the rule ID and version copied and never resolved, the refusal of an empty rule version and of an unknown decision code (AC1, AC2, AC4).
4. `DecisionLogAppender` and the chain: the head lock, `chain_seq`, `prev_hash`, `entry_hash` over the canonical form, the 64-zero first hash, and the one-transaction append with its outbox row; test the concurrent head (AC1, TC-E2-043-01).
5. `DecisionRecordFailClosedHandler`: the `DecisionLogUnavailableException` path to MSG-P7-003 with no chain position consumed, the incident and the redelivery; test the forced failure (AC4).
6. `DecisionLedgerCompletenessChecker` with `LedgerParameterClient`: the 60-second and 11-minute cases of AC5, the gap report and the no-invention rule (AC5).
7. JOB-14: register the Schedule at 02:00 with the overlap policy SKIP and the catch-up window, build `ChainCheckActivity` and `ChainCheckService`, and test the 100-entry chain and the missing `chain_seq` 57 (AC6).
8. `DecisionLogQueryController` with the two operations, the declared area and right, the scope, the paging of 1 to 200 and the problem mapping; tests for AC1, AC7 and the refusals of AC8.
9. The contract-fake run of the whole slice: the topic stub, the library fake, the reference-data and parameters fakes, the case-read fake and the authorise fake, green from Day 1 (AC1 to AC8).
10. The boundary and privacy tests: no write to `rwb_case`, `rwb_document` or `rwb_access`, no read of their tables, and no personal-data field in an entry, a fact, an outbox row, a log line or the chain-check report (BR14, AC4).

**Feature switch.** None of its own, and the ingest must have no off state: a decision that cannot be collected is a decision the audit cannot see, so a switch that silenced the ingest would break BR10 and the principle that no decision stands unrecorded. The legacy flags `rwb.p3.temporal` and `rwb.p3.drools` stay `rwb-case`'s and are legacy references here; with them off the reference run publishes no fact and this story has nothing to collect.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P3-E2043-CON stay green, and a SIT day shows one entry per decision step of `ref-case-RW-2026-000777` with rule `R-RES-04` and the version the fact carried; a chain with no break and no entry changed or deleted; no second entry for a replayed fact and a repeat count of 1 or more for R-UNI-40; a case reported as a completeness gap when a fact is late and no entry invented for it; a JOB-14 run at 02:00 that reports count, last `chain_seq` and last `entry_hash`, and the same-day report of a break in the fixture; both reads answering by case, rule, approver and date and by entry; and not one case, task, state, package or approval changed by this story.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P7-003 | The decision record of a fact cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on the fail-closed handler; the legacy text is copied unchanged |
| MSG-P7-009 | A fact carries a rule ID with no version, a decision code outside the list in force, or a field outside the schema | Not specified in the source documents (GAP-1304; ASM-2314) | This story, on the append, naming `ruleVersion`, `decisionCode` or the field |
| MSG-P4-002 | The role holds no right in the `DECISION_LOG` area | You cannot {action} here. Your role does not include it. | This story, through the guard of the two reads |
| MSG-P4-003 | The entry or the case is outside the caller's scope | This case is not in your scope. | This story, through the guard of the two reads |
| MSG-GEN-002 | A query value is outside its list, or `size` is above 200 | Not specified in the source documents (GAP-1304; ASM-2314) | This story, on the two reads |
| MSG-GEN-006 | The ledger, the reference list or the parameters are unavailable, or a completeness gap or a chain break is reported | Not specified in the source documents (GAP-1309; ASM-2319) | This story, on the read, the completeness check and the chain check |

The four texts above that exist are copied unchanged from the legacy story and FSD P7 v3; the two that no source writes are named by FSD P7 v3 exception flows and left as placeholders. The {field} of MSG-P7-009 is `ruleVersion`, `decisionCode` or the name of the offending field and never a case value. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen is built in this story. The two reads are what the decision-log screen reads: SCR-38 Decision log query (FSD P7 v3, Screens) searches the decision log by case, rule, approver and date, with export, and is built by its own story. The gateway-bff composite route of DP-19 carries the read; this story extends no route and renders no page. SCR-44 Interface and job monitor is not used: the JOB-14 run is read in the job monitor of the platform and in the operational report of the service.

| Where | State | What the reader sees |
|---|---|---|
| `GET /decision-log` | Page | The entries that match the filters, with `items`, `page`, `size` and `total`, in chain order |
| `GET /decision-log/{entryId}` | Entry | The entry with its decision code, rule ID and version, inputs reference, recommendation, approver and level, final call, actions, outcome, decided time, ingest time, source reference and the two hashes |
| The same entry | Append only | No edit and no delete is offered, because neither is allowed; a correction appears as a new entry naming the one it corrects |
| The chain-check report | Complete | Count, last `chain_seq`, last `entry_hash`, start and end time, and no break |
| The chain-check report | Break | The case, the `chain_seq` and the neighbouring hash of the break, reported the same day to Compliance and RW-AUDIT |
| The service's operational report | Gap | The case, the key and the age of a fact that has no entry inside the five-minute target |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-043-01 | AC1, AC7, BR1, BR2, BR3, BR12 | Component | Three facts of the reference run, keys `CASE_EVENT:EV-CASE-0777-01`, `-03` and `-04`, rule `R-RES-04`, version `RES-2026.12`, 100-entry chain fixture |
| TC-E2-043-02 | AC2, BR4, BR13 | Contract | A fact carrying `RES-2026.12` consumed after 2027-01-01 with `RES-2027.01` in force; a fact carrying `RES-2027.01` |
| TC-E2-043-03 | AC3, BR6, BR7 | Component | The same fact replayed under the same event ID and under the same idempotency key; repeat count for R-UNI-40 |
| TC-E2-043-04 | AC4, BR5, BR14 | Unit | Empty rule version, decision code `D99`, a fact with a personal-data field, and the library forced to fail |
| TC-E2-043-05 | AC5, BR10 | NFR | Fact at 06:10 collected at 06:11; fact at 06:20 collected at 06:31; target 5 minutes |
| TC-E2-043-06 | AC6, BR9 | Component | 100 linking entries; a chain with `chain_seq` 57 absent; JOB-14 at 02:00 with SKIP and catch-up |
| TC-E2-043-07 | AC7, AC8, BR8, BR11, BR15 | End to end | Case `RW-2026-000777` at `WITH_FCR_OFFICER` after the entry's `decidedAt`; reads by case, rule, approver and date; size 200 and 201; a role without the right |

The Covers column names the criteria and rules of this story, not the legacy numbering of RWB-E2-043: the seven test cases of the legacy key are kept as identifiers, and each one here proves the ledger half of the criterion it is derived from — the order for `-01`, the pinned version for `-04`, the idempotent retry for `-03`, the failure path for `-02`, the unreachable-service path for `-05`, the flag and synthetic guard for `-06` and the operational registration for `-07`. The workflow, its activities and its fixture are asserted by RWB-P3-E2043-APP and RWB-P3-E2043-OPS under the same identifiers, and the cross-service copy of all seven ends in `-ITG` and belongs to RWB-ITG-E2043-ITG. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the legacy level System maps to Component or End to end, Resilience to NFR and Operational to Component.

### 17. Guardrails

- No business value in code: the decision code, the final call values and the approval level are reference data, and the collection target and the chain-check time are parameters; no literal of either is written in Java.
- No personal data in the entry, the fact, the outbox row, the chain-check report or a log line: references, codes, versions, times and hashes only, and a fact that carries a personal-data field is refused and dead-lettered.
- No read of another service's tables and no other service reading `rwb_decision` (DP-01): the lists arrive on their contract, the parameters on theirs, and the decisions on `rwb.decision-record.v1`.
- Append only in the database and not only in the code: the trigger `tr_declog_append_only` and the missing `UPDATE` and `DELETE` grant refuse an amendment even from the schema owner, and a correction is a new entry naming the one it corrects.
- The entry, its chain position and its outbox row are one transaction; a failed append consumes no chain position, so a refusal never creates the gap JOB-14 would then have to explain (BR12).
- The version is never resolved here: the rule ID and version are copied from the fact, so an entry keeps the version it was recorded under and no default version exists anywhere in the ledger.
- One entry per fact: the inbox by event ID and the unique key on the source reference make a second entry impossible, and the repeat is counted rather than ignored silently.
- No silent gap: a fact with no entry inside the target is reported as a gap and the daily check reports a break the same day, because a ledger with silent gaps is trusted and wrong.
- The ledger is not a producer: it publishes no event, exposes no write operation and changes no case, task, state, package or approval.
- The chain-check and completeness reports hold case IDs, keys, sequence numbers and hashes only; no payload and no decision value is copied into either.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-001 | Every decision writes one record holding the rule and the versions that made it, collected and readable | Business Requirements Epic 2, section 3.7; Program, section 5.7 | FEAT-DRI-01, FEAT-DRI-02, FEAT-DRI-03 | All recovery processes | R-UNI-38, R-UNI-39 | TC-E2-043-01, TC-E2-043-02, TC-E2-043-07 |
| REQ-DRI-005 | No action proceeds if its decision record cannot be written — carried here as the fail-closed append and no half record | Business Requirements Epic 2, section 3.7; Program, section 5.7 | FEAT-DRI-05 | All recovery processes | R-UNI-39 | TC-E2-043-04 |
| REQ-CWC-016 | Every allocation, assignment, transfer and timer event is logged with the rule ID and the rule version that caused it — here the identifiers are carried unchanged | Business Requirements Epic 2, section 3.7; Program, section 5.3 | FEAT-DRI-03 | All recovery processes | R-UNI-38 | TC-E2-043-01, TC-E2-043-02 |
| REQ-DRI-007 | A failing step retries on a defined schedule and leaves a visible exception with an owner — here the consumer's retry topics, the dead-letter topic and the incident | Program, section 5.2 | FEAT-DRI-05 | All recovery processes | R-UNI-39, R-UNI-40 | TC-E2-043-03, TC-E2-043-04 |

- REQ-DRI-002 and REQ-DRI-003 (append only and hash chained, checked every day and reported to Compliance the same day) are carried by BR2 and BR9 and proved by TC-E2-043-01 and TC-E2-043-06; NFR-033 and NFR-035 are their non-functional statements.
- ADR-022 (a local decision record plus a central ledger) and the ADR-009 change that Arch v5 slide 28 proposes: this story is the collection half of ADR-022 and needs the Risk and Internal Audit sign-off the slide names, which sits outside the story (GAP-1310; ASM-2320).
- D-RCV-60: the realignment that splits RWB-E2-043 into the `rwb-case`, `rwb-decision` and integration stories; this story is the ledger slice.
- RWB-P3-E2043-CON, RWB-P3-E2043-APP and RWB-ITG-E2043-ITG: the producing contract, the reference run that writes the facts and the cross-service proof that reads this ledger.
- The legacy story's BRD citation "Business Requirements Epic 2, section 3.2" is read here as section 3.7, the P7 Decision center and log section of that BRD; the program sections 5.2, 5.3 and 5.7 are unchanged.

### 19. Out of scope

- **The Temporal worker, `ReferenceCaseWorkflow`, `EvaluateRulesActivity`, `RecordAndApplyActivity` and the `CaseEventSignalRelay`** — RWB-P3-E2043-APP. This story registers no worker, no workflow and no activity of the reference run.
- **The synthetic case fixture, the `ref-case-` prefix, the synthetic guard, the flag behaviour and the replay gate** — RWB-P3-E2043-APP and RWB-P3-E2043-OPS, with RWB-E2-040. This story reads the facts those produce and asserts none of it.
- **The embedded Drools kit** — RWB-PLT-E1072-CON: the compile, the checksum, first-match semantics, the KieBase cache and `NoPackageInForce`. This story carries the identifiers a fact names and evaluates nothing.
- **The cross-service proof of the pattern** — RWB-ITG-E2043-ITG: the harness, the case-event stub, the journey across `rwb-case`, `rwb-decision` and the topics, and the run report.
- The rule package governance and the registry operations (RWB-P7-E2042-APP, RWB-P7-E1073, RWB-P7-E2027-APP): the package, its versions, rows and test cases, the four-eyes approval, the promotion at 00:01 and the rollback.
- The approval path of the service — the `approval` table, DoA routing, the approve, return and refuse operations and `ApprovalWorkflow` (RWB-P7-E2019-APP and the approval stories). An entry may carry an approver and a level as facts, and the ledger records them.
- The strict-mode acknowledgement before a point of no return and the daily seal of the ledger hash to write-once storage (Arch v5 slides 14 and 28; GAP-1310; ASM-2320). The stories of the points of no return consume the ledger built here.
- The decision-log screen SCR-38, its export, the composite route and the other screens of the service (Epic 8 and the screen stories); this story serves the two reads and renders nothing.
- The platform and `rwb-case` deliverables this story consumes — the parameters contract, the reference-data contract, the outbox and inbox library, the workflow kit, the naming library, the Flyway conventions and the gateway-bff route (RWB-PLT-E1042, RWB-PLT-E1043, RWB-PLT-TE006, RWB-PLT-E1071, RWB-PLT-E1047, RWB-PLT-E1044, RWB-PLT-N001, RWB-P3-E1043).
- The retention and disposal of a ledger entry (RWB-P7-E1017-APP), the ACE audit of a refused statement (the ACE common module), and the case lifecycle and production case workflows of Epic 3.
-PLT-E1047, RWB-PLT-E1044, RWB-PLT-N001, RWB-P3-E1043).
- The retention and disposal of a ledger entry, which is the retention story's and the database's (RWB-P7-E1017-APP), and the ACE audit of a refused statement, which is the ACE common module's.
- The case lifecycle, its state model and the production case workflows of Epic 3.
