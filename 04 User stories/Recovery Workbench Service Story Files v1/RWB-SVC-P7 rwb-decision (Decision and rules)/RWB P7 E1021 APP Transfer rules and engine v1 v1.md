# RWB-P7-E1021-APP Transfer rules and engine v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E1021-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-021 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P7-H |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E1021-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to REQ-CWC-010, REQ-CWC-016, REQ-WKM-003, REQ-CWC-005) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the transfer-record and TRANSFER-model slice of RWB-E1-021 moved into rwb-decision, so that every transfer of a case, rule-driven or manual, is explained from one append-only ledger entry that names the rule and its version or the caller and the coded reason, while the transfer engine itself stays with rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **team manager (RW-TEAMMGR), a litigation officer (RW-LITOFF) and the central ledger itself**, I want **every transfer of a case, rule-driven or manual, held in one decision log entry that names the rule ID and rule version that moved it or the caller and coded reason that moved it, the trigger event and the queues and owners it moved between, that refuses a record which claims a rule and no version, and that serves the compiled TRANSFER model it cites with its checksum and its row order**, so that **any transfer of any case is explained from the ledger alone, a manual transfer is as traceable as a rule transfer, and no entry exists that cannot be reproduced**.

Inside `rwb-decision` this is the transfer-record slice of the decision log and the model side of the rule registry:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1`, Temporal task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`.
- The transfer record is written by rwb-case in its own transaction and published as DecisionRecorded (EV-08) on the shared topic `rwb.decision-record.v1`; this service consumes it idempotently into `decision_log_entry` and never asks rwb-case to wait for the ledger.
- The TRANSFER version "TRF-2026.11" is served from `rule_package_version` and `rule_row` of this schema, with its checksum and its row order TRF-001 to TRF-009. The model is evaluated only in rwb-case (DP-04, TSD P7 T4).

The legacy facts are unchanged: eight triggers, first match in row order, the rule ID and package version on every rule transfer, and the caller and coded reason on every manual transfer (legacy AC1 to AC4, BR1, BR2, BR9). A transfer changes the queue, the team and the owner, never the status.

### 2. Business rationale

A case changes hands between the TDR, litigation, NPA and debt sale teams by email today. Legacy RWB-E1-021 moved the case by rule, and the email hand-off became a rule row. The remaining question in an audit is the one this story answers: why is the case in this queue with this owner, and who put it there. A rule ID with no version answers nothing; a manual transfer with no caller and no reason answers less.

The transfer engine is only as good as its ledger. rwb-decision is where every service's record meets:

1. One entry per transfer, written from the DecisionRecorded event rwb-case publishes, with the rule ID and the package version that fired, the trigger event code and the queues and owners on both sides.
2. A manual transfer held to the same standard: the caller, the coded reason and no rule ID, and a schema check that refuses a claimed rule with no version rather than storing a record nobody can reproduce.

This story is the rwb-decision part of legacy RWB-E1-021. The transfer engine, the eight-trigger listener, the queue and owner choice, the legal hold and the two endpoints stay with rwb-case (RWB-P3-E1021-APP) and its contract RWB-P3-E1021-CON; the ledger store, its trigger and the chain verifier stay with RWB-P7-E1008-APP; the record library every service writes with stays with RWB-P7-E1027-APP; authoring, the scenarios, the four eyes, the approval and the rollback stay with RWB-P7-E1073-APP. This slice delivers the records, their refusals, the read and the model read, nothing else. It meets REQ-CWC-010, REQ-CWC-016 and REQ-WKM-003, and supports REQ-CWC-005: the ledger holds the completed and the refused transfer of a case, so the one queue it ended in is provable after the fact.

### 3. Preconditions

- The `rwb_decision` baseline is in place from RWB-P7-E1008-APP: the `decision_log_entry` table with its required columns, the append-only trigger, the hash chain and the chain verifier, plus the service-template baseline (schema, login, base, topic, queue, chart). This story adds no table of its own.
- RWB-P3-E1021-CON is published: the rwb-case transfer contract fixes the transfer request and answer and the shape of the DecisionRecorded record a transfer publishes, and it carries the fake this story builds against (DP-11).
- The record library of RWB-P7-E1027-APP is in every service from the template (DP-03), so rwb-case writes its local record and publishes EV-08 without this story.
- Package TRANSFER version "TRF-2026.11" is loaded and approved by RW-RISK, who is not its author, and is in force from 2026-11-30, with the nine rows TRF-001 to TRF-009 and at least 50 passing scenarios (legacy section 3, D-RCV-36 T5, Temporal and Drools slide 15).
- The reference-data contract of DP-07 is in force for the decision code list; the values of LOV-DECISION are Not specified in the source documents (GAP-1323; ASM-2336).
- The synthetic facts the tests use: case RW-2026-000301 in queue "TDR-BKK-CO" with owner U-21, queue "LIT-BKK-OFF" of team "LIT-BKK" with owner U-31, route "R4", transfer reason "R03", record version 7, and event "EVT-88120" (legacy AC1, AC2, AC3, AC11).

### 4. Flow

1. rwb-case carries out the transfer and, in the same transaction in its own schema, writes the transfer record and a DecisionRecorded row to its outbox; the relay publishes it on `rwb.decision-record.v1` with the case ID as the key (EV-08, CloudEvents 1.0, DP-09). The transfer never waits for this service.
2. This service's consumer reads the event once per event ID: the inbox drops a duplicate, so a redelivery never appends a second entry (R-UNI-40).
3. The validator reads the decision code, the final call, the rule ID, the rule version and the payload. The decision code is checked against LOV-DECISION. A rule ID with an empty rule version is refused before any append. A record with final call CASE_TRANSFERRED and no rule version, model version or agent version at all is refused naming "versions" (FSD AC-ALT-P7-008-01).
4. The ledger appends one `decision_log_entry` in `rwb_decision`: id, case_id, decision_code, rule_id, rule_version, inputs_ref (the trigger event code), final_call, actions (the from and to queue and the from and to owner), decided_at, actor_user_id, chain_seq, prev_hash and entry_hash. The entry hash is the SHA-256 of the entry's canonical form and prev_hash is the entry hash before it; the first entry's prev_hash is 64 zeros.
5. A rule-driven transfer arrives with final call "CASE_TRANSFERRED", rule ID "TRF-007", rule version "TRF-2026.11", the trigger event code and from "TDR-BKK-CO"/U-21 to "LIT-BKK-OFF"/U-31. No name, account number, amount or document text is copied into the entry.
6. A second transfer refused on a changed record arrives with final call "TRANSFER_REJECTED", the same rule ID "TRF-007" and the same rule version "TRF-2026.11", and the same from and to values as the transfer that committed. The ledger then holds one CASE_TRANSFERRED and one TRANSFER_REJECTED for the case, which is how the one queue the case ended in stays provable (REQ-CWC-005).
7. A manual transfer arrives with final call "CASE_TRANSFERRED", the caller as actor_user_id, the reason "R03" in the payload, and no rule ID and no rule version. It passes the schema check because a rule version is required only when a rule ID is claimed.
8. The entry commits before the inbound coordinate commits, and the record is acknowledged within 5 minutes of the transfer (Temporal and Drools slide 31). A failed append commits neither, so a half entry never exists.
9. The read: `GET /decision-log` filters by case, rule and period and answers the page with `chainVerified` on each entry; `GET /decision-log/{entryId}` answers one entry with its rule, version, inputs reference and both hashes.
10. The registry: `GET /rule-models/{packageCode}/{version}` serves the compiled TRANSFER model "TRF-2026.11" with its SHA-256 and its rows in row order; JOB-20, a Temporal Schedule at 00:01 in queue `rwb-decision`, promotes a version and publishes `rwb.decision.RulePackageInForce.v1` (EV-30).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A record names rule ID "TRF-007" with an empty rule version | Refused before any append; nothing is stored and the refusal names the field | MSG-P7-009 naming "ruleVersion" | AC4 |
| X2 | A record carries decision code "D99", outside LOV-DECISION | Refused before any append; nothing is stored and the refusal names the field | MSG-P7-009 naming "decisionCode" | AC4 |
| X3 | A record carries final call "CASE_TRANSFERRED" with no rule version, model version or agent version | Refused; the refusal names "versions"; the transfer in the same transaction is rolled back by the writer | MSG-P7-009 naming "versions" | AC4 |
| X4 | The same event ID arrives a second time | One entry; the first entry ID is returned and the repeat is counted as an idempotency hit | None | AC1 |
| X5 | A manual call repeats with the same Idempotency-Key | One entry; the first entry ID is returned | None | AC3 |
| X6 | The ledger store is unavailable | Nothing is appended, the coordinate is not committed and the record stays on the topic; the caller that waits on the seal is refused | MSG-P7-003 (GAP-1323; ASM-2336) | AC7 |
| X7 | A version whose state is LOADED, APPROVED, SUPERSEDED, ROLLED_BACK or REFUSED is asked for | Refused rather than served; the client keeps the model it holds | MSG-P7-009 naming the version state | AC6 |
| X8 | The stored checksum does not match the compiled model | Refused and reported; the model is not served and no client swaps it in | MSG-P7-009 naming the checksum | AC6 |
| X9 | An entry fails the chain on a read | The page answers with `chainVerified` false on that entry and the warning | MSG-P7-012 | AC5 |

A record refused at X1, X2 or X3 is not retried: it is a defect in the calling service's record, and that service's own transaction rolls back with it. A record that fails on an unavailable store (X6) is different and is re-read, because the transfer already happened in rwb-case's schema.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the `rwb_decision` baseline of RWB-P7-E1008-APP, the RWB-P3-E1021-CON fake and the TRANSFER version already in force; it calls no other service at run time |
| Negotiable | Nothing business is fixed here: the rule rows, the reason list and the decision code list are data, and the policy is the package's |
| Valuable | One place where any transfer of any case is explained, and a ledger that refuses a record nobody could reproduce |
| Estimable | One consumer, one validator, one append, one read, one model read, one Schedule |
| Small | Fits one sprint with its tests, as a secondary slice of the legacy key |
| Testable | Every criterion in section 7 is one automated test against the event fake, the store fixture and the package fixture |

### 7. Acceptance criteria

```gherkin
Feature: Transfer rules and engine v1 - the transfer records and the TRANSFER model of rwb-decision

  Background:
    Given package TRANSFER version "TRF-2026.11" is in force with its compiled model and checksum in "rwb_decision"
  Scenario: AC1 The rule-driven transfer is recorded with rule TRF-007 and version TRF-2026.11 (new, D-RCV-60)
    Given the rwb-case contract mock returns a DecisionRecorded event "EV-9a01-0001" with final call "CASE_TRANSFERRED" for case "RW-2026-000301", rule ID "TRF-007", rule version "TRF-2026.11", event code "ROUTE_APPROVED", from queue "TDR-BKK-CO" and owner U-21, to queue "LIT-BKK-OFF" and owner U-31
    When the event arrives on "rwb.decision-record.v1"
    Then one decision_log_entry exists for case "RW-2026-000301" with final_call "CASE_TRANSFERRED", rule_id "TRF-007" and rule_version "TRF-2026.11"
    Then the entry carries the event code "ROUTE_APPROVED" and the four identifiers "TDR-BKK-CO", U-21, "LIT-BKK-OFF" and U-31
    Then the entry holds no customer name, no account number, no amount and no document text
    Then the entry is appended at chain_seq n+1 with prev_hash equal to the entry_hash before it and entry_hash equal to the SHA-256 of its canonical form
    When the same event "EV-9a01-0001" arrives again
    Then one entry exists for the event and the first entry ID is returned
  Scenario: AC2 The refused second transfer is recorded as TRANSFER_REJECTED with its rule (new, D-RCV-60)
    Given the rwb-case contract mock returns a DecisionRecorded event "EV-9a03-0001" with final call "CASE_TRANSFERRED" for case "RW-2026-000303", rule ID "TRF-007" and rule version "TRF-2026.11", from queue "TDR-BKK-CO" and owner U-21, to queue "LIT-BKK-OFF" and owner U-31
    Given the rwb-case contract mock returns a second DecisionRecorded event "EV-9a03-0002" for case "RW-2026-000303" with final call "TRANSFER_REJECTED", the same rule ID "TRF-007" and the same rule version "TRF-2026.11", and the same from and to values
    When both events arrive on "rwb.decision-record.v1"
    Then two entries exist for case "RW-2026-000303", one with final_call "CASE_TRANSFERRED" and one with final_call "TRANSFER_REJECTED"
    Then both entries carry rule_id "TRF-007" and rule_version "TRF-2026.11"
    Then the second entry carries the same from and to queue and owner identifiers as the first
    Then the read for the case returns both entries, so the one queue the case ended in is explained by the pair
  Scenario: AC3 The manual transfer is recorded with its caller and reason and no rule ID (new, D-RCV-60)
    Given the rwb-case contract mock returns a DecisionRecorded event "EV-9a02-0001" with final call "CASE_TRANSFERRED" for case "RW-2026-000302", the caller as actor, the transfer reason "R03" and target owner U-22, with no rule ID and no rule version
    When the event arrives on "rwb.decision-record.v1"
    Then one decision_log_entry exists for case "RW-2026-000302" with final_call "CASE_TRANSFERRED"
    Then rule_id and rule_version are empty on the entry
    Then actor_user_id is the caller and the entry carries transfer reason "R03" and target owner U-22
    Then the entry passes the schema check and nothing is refused
    When the same manual call repeats with the same Idempotency-Key and event "EV-9a02-0001"
    Then one entry exists for the case and the first entry ID is returned
  Scenario: AC4 A record that fails the ledger schema is refused and nothing is appended (new, D-RCV-60)
    Given the rwb-case contract mock returns a DecisionRecorded event "EV-9a04-0001" for case "RW-2026-000304" with rule ID "TRF-007" and an empty rule version
    When the event arrives on "rwb.decision-record.v1"
    Then the record is refused with MSG-P7-009 naming "ruleVersion"
    Then no decision_log_entry is appended and no chain_seq is used
    Given the rwb-case contract mock returns a DecisionRecorded event "EV-9a04-0002" for case "RW-2026-000304" with decision code "D99"
    When the event arrives on "rwb.decision-record.v1"
    Then the record is refused with MSG-P7-009 naming "decisionCode"
  Scenario: AC5 The decision log read explains every transfer of a case in a period (new, D-RCV-60)
    Given three entries exist for case "RW-2026-000301" between "2026-11-01" and "2026-11-30", two of them with rule ID "TRF-007"
    When a reader holding Decision log R calls GET /api/recovery/decision/v1/decision-log for case "RW-2026-000301", rule ID "TRF-007" and that period
    Then the page returns the two entries with their rule ID and rule version, decided_at and hashes
    Then each entry carries chainVerified true
    When a role with no Decision log right calls the same read
    Then the read is refused with MSG-P4-002
    When one of the two entries has its stored payload changed in the test fixture and the read is repeated
    Then that entry carries chainVerified false and the page carries MSG-P7-012 naming the entry
  Scenario: AC6 The compiled TRANSFER model is served with its checksum and row order (new, D-RCV-60)
    Given version "TRF-2026.11" is IN_FORCE with checksum "SHA-256-TRF-2026-11"
    When a client holds the model on GET /api/recovery/decision/v1/rule-models/TRANSFER/TRF-2026.11
    Then the answer carries the compiled model, the checksum "SHA-256-TRF-2026-11" and the rows TRF-001 to TRF-009 in row order
    Then the row "TRF-007" sits in that order with event code "ROUTE_APPROVED", target queue "LIT-BKK-OFF" and route condition "R4"
    When a client holds a version of TRANSFER whose state is "LOADED"
    Then the version is refused rather than served and the client keeps the model it holds
    When the stored checksum of "TRF-2026.11" no longer matches the compiled model
    Then the model is refused rather than served and the mismatch is reported
  Scenario: AC7 An unavailable ledger store blocks the caller and appends nothing (new, D-RCV-60)
    Given the ledger store is unavailable
    When a DecisionRecorded event for case "RW-2026-000309" with transfer reason "R03" arrives on "rwb.decision-record.v1"
    Then the record is refused with 503 and MSG-P7-003
    Then no decision_log_entry is appended and no chain_seq is used
    Then the inbound coordinate is not committed, the record stays on the topic and the entry is appended when the store returns
```

The seven criteria above are new and test only this deliverable: the transfer records of the central ledger, their refusals, the read that explains them, the model read and the promotion event. The legacy criteria of RWB-E1-021 are owned elsewhere: AC1, AC2, AC3, AC4, AC5, AC10 and AC12 of the legacy story are the transfer engine and the queue and owner choice of rwb-case (RWB-P3-E1021-APP); AC6, AC7, AC8, AC9 and AC13 are its request validation and the legal hold; the access refusal stays with rwb-access (RWB-P4-E1021-APP); AC14 is the no-match path of rwb-case, which writes no record and therefore sends nothing here.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every transfer, rule-driven or manual, has exactly one decision log entry, appended when the transfer records it and never dropped; the ledger holds the completed and the refused transfer of a case, so the queue the case ended in stays provable | REQ-CWC-016; REQ-CWC-005; FSD P7 A2.2; principle 5 |
| BR2 | A rule transfer entry names the rule ID and the package version that fired; a manual entry names the caller and the coded transfer reason and names no rule ID | REQ-CWC-010; REQ-WKM-003; legacy BR2, BR9 |
| BR3 | A record that claims a rule ID must name its rule version; a claimed rule with no version is refused before any append and the refusal names the field | FSD P7 AC-EXC-P7-008-01; legacy BR9 |
| BR4 | A decision code outside LOV-DECISION is refused before any append and the refusal names the field | FSD P7 AC-EXC-P7-008-05; TSD P7 T3.1 (DF-DEC-003) |
| BR5 | The ledger is append only and hash chained: prev_hash is the entry_hash of chain_seq minus one, the first prev_hash is 64 zeros, and each entry_hash is the SHA-256 of the entry's canonical form | FSD P7 AC-ALT-P7-001-01; TSD P7 T3.1; Temporal and Drools slide 16 |
| BR6 | An event with the same event ID, and a manual call with the same Idempotency-Key, each give one entry, and the repeat returns the first entry ID | R-UNI-40; FSD P7 AC-EXC-P7-008-03; legacy BR8 |
| BR7 | The read answers every transfer of a case in a period, by case, rule and version, with chainVerified on each entry, and a break is reported on the page rather than hidden | API-P7-006; FSD P7 AC-BG-P7-002-01; NFR-035; TSD P7 T6.1 |
| BR8 | A package version is served only when its state is IN_FORCE and its checksum matches the compiled model; no rule is evaluated in this service, and a version not in force is never a default | Temporal and Drools slide 15; DP-04; TSD P7 T4 |
| BR9 | The ledger blocks rather than drops: when the store cannot be written nothing is appended, the coordinate is not committed and the record stays on the topic, so the history never has a silent gap | R-UNI-39; FSD P7 VR-P7-008-2 (MSG-P7-003); Temporal and Drools slide 28 |

How the rules hold in `rwb-decision`:

- BR1 and BR2 are executed by `TransferRecordConsumer` and `LedgerAppend`: the entry is built from the event only, and the actor, the rule ID, the rule version and the reason come from fields of the event, never from a lookup in another schema.
- BR3, BR4 and BR8 are executed before a byte is stored: `TransferRecordValidator` refuses a bad record in the same consumer call, and `RuleModelReader` reads the version state and the checksum and refuses before it serves.
- BR5, BR6 and BR7 are executed by the store and the read: the append-only trigger and the chain columns are the store story's, the inbox and the unique idempotency key (`DF-DEC-031`) hold the repeat, and `DecisionLogQuery` answers the stored hash with its verified flag.
- BR9 is executed by the commit order: the append and the inbound coordinate are one transaction, so a failure leaves both out.

### 9. State transitions

The case state machine is not this service's (TSD P7 T4: "No case state machine of its own"). This slice changes no case state; it records what rwb-case did.

| From | Event | Condition | To |
|---|---|---|---|
| none | DecisionRecorded arrives | The event ID is unseen, the decision code is in LOV-DECISION, a claimed rule ID carries its version and the required fields are present | Appended at chain_seq n+1 with final_call CASE_TRANSFERRED or TRANSFER_REJECTED |
| none | DecisionRecorded arrives | The schema check fails | Nothing appended, no chain_seq used, MSG-P7-009; the record is not retried |
| appended | the same event ID or Idempotency-Key arrives again | The idempotency key matches an existing entry | No second row; the first entry ID is returned |

The package version moves through its own states, and only one of them is served:

| From | Event | Condition | To |
|---|---|---|---|
| none | a workload is uploaded and passes the load checks | Compile, schema, overlap, unreachable row, default row, at least 50 scenarios and the dry run pass | LOADED |
| LOADED | RW-RISK approves | The approver is not the author | APPROVED |
| APPROVED | JOB-20 at 00:01 on the valid-from date | The version is approved and its valid-from date has arrived | IN_FORCE, and RulePackageInForce is published |
| IN_FORCE | a later version is promoted, or a rollback | The later version reaches its valid-from date, or RW-RISK calls rollback once | SUPERSEDED, or ROLLED_BACK with the earlier version back IN_FORCE |
| LOADED, APPROVED | a load check fails | Any check fails | REFUSED |

Only IN_FORCE is served on `/rule-models/{packageCode}/{version}`; the other five states answer a refusal (AC6).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-decision service identity (the rwb-decision login, DP-02) | Consumes DecisionRecorded, appends the entry, serves the model read and publishes RulePackageInForce; holds no grant on another schema |
| SY-CASEWF and SY-RULES | C on the decision log (TSD P7 T6.1): fetch the model and write their own record before this service collects it |
| RW-TEAMMGR, RW-LITOFF, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-CASEOWN and every role with Decision log R | Read the entries of a case in their scope, with `chainVerified` |
| RW-COE and RW-RISK | Author a package version, and approve one that is not their own (the authoring story) |
| rwb-case (P3) | Owns the transfer, the trigger, the queue and owner choice and the record it publishes; this service reads none of its tables |

The authorisation decision is the cached permission decision from rwb-access that the service template's guard already holds; DP-08 is not in this slice's pattern set, so this story adds no guard of its own. The refusals are 403 with MSG-P4-002 for a role without the right, 404 with the not-found answer for an entry that does not exist, and 503 with MSG-P7-003 when the ledger cannot be read or written. The role codes are rows of the role model in `rwb_access` (TSD P7 T6.1) and are not fixed in code.

### 11. Data

| BR Field ID | Table in rwb_decision | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 | decision_log_entry | id | Write |
| DF-DEC-002 | decision_log_entry | case_id (the case the transfer moved) | Write |
| DF-DEC-003 | decision_log_entry | decision_code | Write; checked against LOV-DECISION |
| DF-DEC-004 | decision_log_entry | rule_id | Write (empty on a manual transfer) |
| DF-DEC-005 | decision_log_entry | rule_version (the package version label) | Write (empty on a manual transfer; refused when rule_id is set and it is empty) |
| DF-DEC-008 | decision_log_entry | inputs_ref (the trigger event code of the eight) | Write |
| DF-DEC-012 | decision_log_entry | final_call | Write (CASE_TRANSFERRED or TRANSFER_REJECTED) |
| DF-DEC-014 | decision_log_entry | actions (from and to queue, from and to owner, the reason on a manual transfer) | Write; the field names inside the JSONB are Not specified in the source documents (GAP-1323; ASM-2336) |
| DF-DEC-016 | decision_log_entry | decided_at | Write (the time of the transfer, not of the ingest) |
| DF-DEC-017, DF-DEC-018, DF-DEC-028 | decision_log_entry | prev_hash, entry_hash, chain_seq | Write |
| DF-DEC-030 | decision_log_entry | actor_user_id | Write (SY-CASEWF on a rule transfer, the caller on a manual transfer) |
| DF-DEC-031 | decision_log_entry | idempotency_key (the event ID, or the Idempotency-Key of a manual call) | Write |
| DF-REF-279 to DF-REF-295 | rule_package_version | id, version_label, status, checksum, valid_from, author, approver and the rest of the version row | Read |
| DF-REF-002, DF-REF-003, DF-REF-006, DF-REF-007, DF-REF-052 to DF-REF-054 | rule_row | rule_id, rule_version, event_code, condition_expr, rule_table, row_order, target_queue_code | Read |

Field IDs are those in the Technical Specification P7 Decision center and log v2 T3.1 and the API Specification v4 rule-package schemas. `decision_log_entry` is the only table this slice writes. No customer name, account number, amount, document text or free text reason is held in the entry: the manual reason is a list value ("R03") and the transfer detail is identifiers only.

### 12. Contract

Base `/api/recovery/decision/v1`, owner rwb-decision (P7), schema `rwb_decision`, topic `rwb.decision.events.v1`, task queue `rwb-decision`.

#### 12.1 REST operations provided

| Method | Path | API ID | Access | Use in this story |
|---|---|---|---|---|
| GET | `/decision-log` | API-P7-006 | Decision log R | Search by case, rule, rule version, approver and period; `caseId`, `caseIds`, `decision`, `ruleId`, `ruleVersion`, `approver`, `from`, `to`, `page`, `size` (1 to 500) and `text/csv` export; each entry carries `chainVerified` and the page carries MSG-P7-012 on a break |
| GET | `/decision-log/{entryId}` | API-P7-007 | Decision log R | One entry with its rule ID, rule version, inputs reference, final call and both hashes |
| GET | `/rule-models/{packageCode}/{version}` | none in API Specification v4 (Arch v5 slide 14: `GET /rule-models/{n}/{v}`) | C on the decision log for the owning service identity (SY-RULES, SY-CASEWF) | The compiled TRANSFER model with its SHA-256 and its rows in row order; the full path decorator and response shape are Not specified in the source documents (GAP-1323; ASM-2336) |

#### 12.2 REST operations consumed

None. The transfer record arrives as an event, not as a call, and this service calls no other service at run time. The decision code list is resolved by the writer story through the reference-data contract of DP-07, and the model rows are read from this service's own schema.

#### 12.3 Events published

| Event | Topic | Key | When | Payload |
|---|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` | `rwb.decision.events.v1` | packageCode | JOB-20 at 00:01, or a rollback | EV-30; the owning service takes the package code and the version label from it, fetches the model on 12.1 and verifies the checksum |

#### 12.4 Events consumed

| Event | Topic | Producer | Key | Handling |
|---|---|---|---|---|
| DecisionRecorded (EV-08) | `rwb.decision-record.v1` | every service; for a transfer, rwb-case (P3) | caseId | CloudEvents 1.0; inbox deduplication on the event ID; one `decision_log_entry` per event; acknowledged within 5 minutes; a schema failure is refused and not retried, a store failure is re-read |

#### 12.5 Workflows and activities

None. The ingestion is a Kafka consumer and the promotion is a Schedule; this story starts no workflow and runs no activity, and it holds no case state. `ApprovalWorkflow` is the approval story's.

#### 12.6 Schedules

| Job | Time | Queue | What it does |
|---|---|---|---|
| JOB-20 Rule promote | 00:01 | `rwb-decision` | Promotes an approved version whose valid-from date has arrived, sets it IN_FORCE, supersedes the version it replaces and publishes `rwb.decision.RulePackageInForce.v1` (DP-10) |

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `decision_log_entry` | P7 (rwb_decision) | The append-only, hash-chained ledger row; this slice appends and reads it |
| `rule_package_version` | P7 (rwb_decision) | One row per uploaded version of the package TRANSFER, with its label, state, checksum, valid-from, author and approver; read here |
| `rule_row` | P7 (rwb_decision) | The parsed catalogue, TRF-001 to TRF-009, with event code, condition, row order and target queue; read here |
| inbox and processed-event objects | PLT library, created in `rwb_decision` | The inbox that drops a duplicate event and the coordinate this slice commits with the entry |

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case transfer contract fake (RWB-P3-E1021-CON) | The DecisionRecorded record a transfer publishes | Case `RW-2026-000301` with rule "TRF-007", version "TRF-2026.11", event code "ROUTE_APPROVED", `TDR-BKK-CO`/U-21 to `LIT-BKK-OFF`/U-31; case `RW-2026-000303` with the completed and the refused record; case `RW-2026-000302` with reason "R03" and no rule ID; a rule ID with an empty version; decision code "D99" |
| ledger store fixture (RWB-P7-E1008-APP) | The append, the chain and the read | An append returning chain_seq n+1 and both hashes; an append that fails; an entry with a broken hash for MSG-P7-012; three entries for `RW-2026-000301` |
| package fixture (RWB-P7-E1073-APP data) | `rule_package_version` and `rule_row` | "TRF-2026.11" IN_FORCE with checksum `SHA-256-TRF-2026-11` and nine rows TRF-001 to TRF-009; a version in state LOADED; a checksum that does not match |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 0 consumed | `GET /decision-log`, `GET /decision-log/{entryId}`, `GET /rule-models/{packageCode}/{version}` |
| Kafka | 1 published, 1 consumed | Publishes `rwb.decision.RulePackageInForce.v1`; consumes DecisionRecorded on `rwb.decision-record.v1` |
| Temporal | 1 Schedule, no workflow | JOB-20 at 00:01 in queue `rwb-decision` (DP-10) |
| File | None | The workbook and the generated DRL are stored by the authoring story; this slice serves the compiled model |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `transferrecord`, Java package `th.co.scb.ace.workbench.recovery.decision.transferrecord`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TransferRecordConsumer | Kafka consumer | Reads DecisionRecorded once per event ID, takes the decision code, final call, rule ID, rule version, actor and payload, and calls the validator; commits the inbound coordinate with the entry |
| TransferRecordValidator | Service | Checks the decision code against LOV-DECISION, requires a rule version when a rule ID is claimed, requires the version group on a completed transfer, and refuses with MSG-P7-009 before any append |
| LedgerAppend | Service | Appends the entry with chain_seq, prev_hash and entry_hash in one transaction, holds the idempotency key and returns the first entry ID on a repeat |
| DecisionLogQuery | Service | The read by case, rule, version and period, with `chainVerified` per entry and MSG-P7-012 on a break |
| RuleModelReader | Service | Serves the compiled model with its checksum and row order, refuses a state other than IN_FORCE and a checksum that does not match |
| TransferRecordController | Controller | The three reads of 12.1 with the access check and the problem response |

**Database and migrations**

- Appends `decision_log_entry`; reads `rule_package_version`, `rule_row` and `rule_package`; writes no other schema.
- Index `(case_id, rule_id, decided_at)` on `decision_log_entry`, which serves the read of AC5 and the period filter of the screen.
- Migration in this story, in the per-service Flyway sequence of DP-15: `V1021_1__transfer_record.sql` adds that index and nothing else. The table, its required columns, the append-only trigger and the chain are the store story's, and no row is seeded here: the TRANSFER version and its nine rows arrive through the authoring story.

**Configuration and reference data**

- No business value is configured here: the rule rows, the target queues, the condition "R4" and the reason "R03" are data of the package and of the reason list; the decision codes are the LOV-DECISION list.
- Two settings only: the rwb-case transfer contract base (the fake in a build, the service in a run) and the rwb-decision login (DP-02), named by the DB story of this service. The 5-minute acknowledgement target and the commit order are configuration of the consumer, not code branches.

**Build steps**

1. `TransferRecordConsumer` and `TransferRecordValidator` against the event fake, with the completed transfer, the refused transfer and the manual transfer; tests for AC1, AC2 and AC3.
2. The refusals of BR3, BR4 and BR9 before any append, and the assertion that a refused record uses no chain_seq; tests for AC4 and AC7.
3. `LedgerAppend` with the idempotency key and the repeat path; tests for AC1 and AC3.
4. `DecisionLogQuery` with the period and rule filters, `chainVerified` and MSG-P7-012; test for AC5.
5. `RuleModelReader` with the IN_FORCE state and the checksum check, and `RulePromotionSchedule` with a shortened schedule in SIT; test for AC6.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_decision`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

This is a secondary slice with no owned legacy acceptance criteria of a build story: it adds no new build dependency of its own (metadata "Depends on (build)" = None) and builds against the `rwb_decision` baseline and the RWB-P3-E1021-CON fake. Read one by one:

- DP-01, DP-02 and DP-13 are the target shape itself: the schema `rwb_decision`, the rwb-decision login and the base `/api/recovery/decision/v1`, with no new dependency.
- DP-03, DP-09 and DP-14 are the live patterns of the record: DecisionRecorded arrives on `rwb.decision-record.v1` through the inbox, RulePackageInForce leaves through the outbox, and both names come from the naming library.
- DP-04 applies divided: the registry half is here (the version, its checksum and its rows are served) and the evaluation half is rwb-case's; this service holds no KieBase, which is what lets the record and the row that fired be read side by side.
- DP-05, DP-07 and DP-10 are statements of what is not done here (no ACE view, no list value in code, no Quartz job), DP-11 is the record crossing as a published event with the model read as a one-hop 2 s contract, DP-15 is `V1021_1__transfer_record.sql`, and DP-19 is the composite route behind the decision log page and SCR-03.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P3-E1021-CON stay green, and a SIT week shows every transfer of every case in the ledger with its rule ID and version or its caller and reason, no entry for a record that failed the schema, one entry per event on a redelivery, the model read answering IN_FORCE only, and a break on the read visible as MSG-P7-012 rather than hidden.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-009 | A record fails the ledger schema: a rule ID with no rule version (names "ruleVersion"), a decision code outside LOV-DECISION (names "decisionCode"), a completed transfer with no version at all (names "versions"), or a version that is not IN_FORCE or whose checksum does not match (names the state or the checksum) | Not specified in the source documents (GAP-1323; ASM-2336) |
| MSG-P7-003 | The ledger store cannot be written or read | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-012 | An entry on the page fails the chain | Not specified in the source documents (GAP-1323; ASM-2336) |
| MSG-P4-002 | The caller's role holds no Decision log R, or no Decision log C for the model read | You cannot {action} here. Your role does not include it. |

The message text of MSG-P7-009 and of MSG-P7-012 is not given in the P7 sources, which name only the field each one names and the entry each one names; the two IDs and the field they name are the contract until the message catalogue fixes the sentences. Every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. The read answers 401, 403 with MSG-P4-002, 404 for an entry that does not exist, and 503 with MSG-P7-003. For MSG-P4-002 the {action} value names the action the caller tried - "read this decision log" or "hold this rule model" - and never a case fact.

### 15. Screens and states

No screen of its own in this story. The read plane is what the screens use: the decision log page reads `GET /decision-log` by case and period and shows, for each transfer, the rule ID, the rule version, the from and to queue and owner, the final call and the chain flag; the decision tab of SCR-03 Case record shows the same entries for one case, beside the case header read from rwb-case. Both are served by the gateway-bff composite route (DP-19), one hop to rwb-decision and one to rwb-case. The states this story makes visible are three: an entry that verifies (`chainVerified` true), an entry that does not (false, with MSG-P7-012 on the page and no silent pass), and the refusal when a reader's role holds no right (403 with MSG-P4-002). The page layout, its filters, its loading and empty states and its export belong to the decision-log screen story; the case number shown beside an entry is read from the rwb-case contract at display time and is never stored in `rwb_decision`.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-021-15 | AC5, BR7: the decision log read answers a role with Decision log R and refuses one without it with MSG-P4-002; the transfer call's own refusal stays with rwb-case | Component | Role RW-CASEOWN reads case `RW-2026-000301`; a role with no Decision log R is refused with MSG-P4-002 |
| TC-E1-021-01 | AC1, BR1, BR2, BR5: the rule transfer entry names TRF-007 and TRF-2026.11 with the trigger code and both queue and owner pairs, and is chained | End to end | Case `RW-2026-000301` in `TDR-BKK-CO` owner U-21, route "R4" approved, queue `LIT-BKK-OFF` owner U-31, package TRANSFER "TRF-2026.11" |
| TC-E1-021-02 | AC3, BR2: the manual transfer entry names the caller and reason "R03" and names no rule ID, and still passes the schema check | End to end | Case `RW-2026-000302`, team manager of `TDR-BKK`, reason "R03", target owner U-22 |
| TC-E1-021-03 | AC2, BR1: the refused second transfer is recorded as TRANSFER_REJECTED with the same rule and version, so the case's one queue is provable | End to end | Case `RW-2026-000303` at record version 7; a rule transfer to `LIT-BKK-OFF` and a manual transfer to `DIL-BKK-CO` in the same second; MSG-GEN-004 on the second |
| TC-E1-021-04 | AC1, BR2: each of the eight triggers carries its own event code into the entry, and the row that fired is named | Component | Rows TRF-001 CaseStateChanged, TRF-002 ROUTE_APPROVED, TRF-003 TimerDue, TRF-004 DeviationRaised, TRF-005 DeviationCleared, TRF-006 ApprovalRequested, TRF-008 DocumentStored, TRF-009 PaymentMissed; case `RW-2026-000304` |
| TC-E1-021-05 | AC3, BR1: a reassignment and a hold and lift each give one entry with its own reason | End to end | Case `RW-2026-000305`; reassign to U-23 with reason "R04"; hold with reason "Court order" and reference "ORD-2026-0412", then lift |
| TC-E1-021-06 | AC4, BR3: a manual call with no transfer reason leaves no entry behind; the refusal itself is rwb-case's | Contract | Case `RW-2026-000306`, no transfer reason, MSG-P3-001 at rwb-case; no DecisionRecorded published and no entry appended |
| TC-E1-021-07 | AC4, BR9: a transfer to an owner at the cap leaves no entry behind; the cap check is rwb-case's | Contract | U-24 at 150 open cases in `TDR-BKK-CO`, case `RW-2026-000307`, MSG-P3-002 at rwb-case |
| TC-E1-021-08 | AC4, BR9: a refused transfer of a closed case leaves no entry behind | Contract | Case `RW-2026-000308` with status `CLOSED`, MSG-P3-005 at rwb-case |
| TC-E1-021-09 | AC7, BR9: an unavailable ledger store appends nothing and blocks the caller with MSG-P7-003; the record is re-read when the store returns | NFR | Store down during a manual transfer of case `RW-2026-000309` with reason "R03"; the event held on `rwb.decision-record.v1` |
| TC-E1-021-10 | AC4, BR1: a trigger that moves no case writes no entry; the legal hold check stays with rwb-case | Component | Case `RW-2026-000310` with legal_hold true; TimerDue matching row TRF-003; R-UNI-20 |
| TC-E1-021-11 | AC1, BR6: the same event ID gives one entry and returns the first entry ID | Component | PaymentMissed event "EVT-88120" for case `RW-2026-000311` to `TDR-BKK-CO`, delivered twice |
| TC-E1-021-12 | AC2, BR2: the entry carries the overflow queue as the to queue with an empty to owner when the target queue is full | Component | Every member of `LIT-BKK-OFF` at 150; row TRF-007 for case `RW-2026-000312`; overflow queue `LIT-BKK-OVF`; MSG-P3-011 at rwb-case |
| TC-E1-021-13 | AC4, BR9: a hold on a case already on hold gives no third transfer record; the refusal is rwb-case's | Contract | Case `RW-2026-000313` at `ON_HOLD` with a legal hold, MSG-P3-005 |
| TC-E1-021-14 | AC4, BR8: no matching row means no record is published and none is appended | Unit | DocumentStored for case `RW-2026-000314` with no TRANSFER row matching; no DecisionRecorded and no entry |
| TC-E1-021-16 | AC7, BR9: a failed append for a rule transfer leaves no entry, and the transfer is not half recorded | NFR | The append forced to fail while the event for a rule transfer of case `RW-2026-000301` is consumed; the event retried and the entry appended once the store returns; R-UNI-39 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to End to end, Access to Component and Resilience to NFR. Every legacy test case of RWB-E1-021 is listed above with the slice of the behaviour this story answers; the -ITG copies belong to the integration slice RWB-ITG-E1021-ITG and are not rows of this table.

### 17. Guardrails

- No business value in code: the rule rows, the target queues, the condition "R4", the reason "R03" and the decision codes are data of the package and the lists, read at run time. No queue code, rule ID or reason code appears in this service's Java.
- No personal data in events, workflow inputs, logs or tests. This slice writes case IDs, queue codes, owner IDs, rule IDs, versions and hashes only; no name, address, identity number, account number or free-text reason is held or logged. Test data uses synthetic keys (`RW-2026-000301`, U-21, U-31, `TDR-BKK-CO`, `LIT-BKK-OFF`).
- No cross-schema read (DP-01): `rwb_decision` reads no `rwb_case` table and no table of another service; the transfer arrives as an event and the case is never queried.
- ACE data only through the owner's contract or `v_ace_*` views, and this service reads no view (DP-05): no customer or account fact enters the ledger.
- One evaluator, and it is not this one: TRANSFER is evaluated only in rwb-case (DP-04), and this service serves the model and records the answer. The ledger is append only: no code path updates or deletes a `decision_log_entry`, and a correction is a new entry with `corrects_entry_id`.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-010 | Cases move between queues and roles by transfer rules on eight triggers and a manual request with a reason code | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-10 | All recovery processes | BR1, BR2, BR6; R-UNI-40 | TC-E1-021-01, TC-E1-021-02, TC-E1-021-03, TC-E1-021-04, TC-E1-021-10, TC-E1-021-11, TC-E1-021-12, TC-E1-021-14 |
| REQ-CWC-016 | Every allocation, assignment, transfer and timer event is logged with the rule ID and the rule version that caused it | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-10 | All recovery processes | BR1, BR2, BR3, BR5, BR9; R-UNI-39 | TC-E1-021-01, TC-E1-021-03, TC-E1-021-05, TC-E1-021-09, TC-E1-021-16 |
| REQ-WKM-003 | A case is transferred or reassigned manually only with a reason code from the agreed list | Epic 2 BRD; Program BRD | FEAT-CWC-10; FEAT-CHO-01 | All recovery processes | BR2 | TC-E1-021-02, TC-E1-021-05, TC-E1-021-06 |
| REQ-CWC-005 | The case state model covers stage, status, route and the deviation flags, and a case holds exactly one state at a time | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-10 | All recovery processes | BR1 | TC-E1-021-02, TC-E1-021-03, TC-E1-021-05, TC-E1-021-13 |

| Legacy reference | Where it is kept |
|---|---|
| Legacy key RWB-E1-021; story RWB-P7-E1021-APP; contract RWB-P3-E1021-CON; schema `rwb_decision` | Metadata; sections 1, 3, 12 |
| Eight triggers, first match in row order, row order TRF-001 to TRF-009, the rule ID is the row name | Sections 1, 7, 8, 12.6, 16 |
| Rule transfer entry with rule ID and package version; manual entry with caller and reason and no rule ID | Sections 4, 8, 11, 16 |
| Schema refusals: rule ID with no rule version, decision code outside the list, no version at all | Sections 5, 7, 14 |
| Chain of the entry (chain_seq, prev_hash, entry_hash, 64 zeros first), idempotency, version states LOADED to REFUSED, JOB-20 at 00:01, EV-30, the checksum check | Sections 4, 8, 9, 11, 12, 13, 16 |
| Synthetic values: cases `RW-2026-000301` to `RW-2026-000314`, queues `TDR-BKK-CO` and `LIT-BKK-OFF`, owners U-21, U-31, U-22, route "R4", reason "R03", event "EVT-88120" | Sections 3, 7, 16 |
| MSG-P7-003, MSG-P7-009, MSG-P7-012, MSG-P4-002, MSG-GEN-004; field IDs DF-DEC-001 to DF-DEC-031, DF-REF-002 to DF-REF-294; TCs TC-E1-021-01 to TC-E1-021-16 | Sections 11, 14, 16 |
| The other slices of RWB-E1-021 (the engine, the hold, the access, the store, the writer, the authoring) | Sections 2, 19 |

### 19. Out of scope

- The transfer engine, the first-match evaluation, the eight-trigger listener, the queue and owner choice, the legal hold, the overflow queue, the endpoints `POST /cases/{caseId}/transfer` and `POST /cases/{caseId}/legal-hold` and the transfer request validation: rwb-case (RWB-P3-E1021-APP), against the contract RWB-P3-E1021-CON.
- The ledger store itself: the `decision_log_entry` table, its required columns, the append-only trigger, the chain verifier and JOB-14 at 02:00: RWB-P7-E1008-APP. The decision log writer library and the DecisionRecorded publication: RWB-P7-E1027-APP.
- Authoring a package, the 50 scenarios, the four-eyes approval, the validity dates, the dry run, the rollback and the admin endpoints: RWB-P7-E1073-APP.
- The approval queue, approve, return and refuse, `ApprovalWorkflow` and the `/approvals` paths: the approval stories of RWB-SVC-P7.
- The access matrix, the scope decision and the access log: rwb-access (RWB-P4-E1021-APP); this service consumes the cached decision from the template.
- The decision log copy to a data lake (JOB-13) and RWB-E1-014: retired, because there is no data lake in Arch v5; the reporting projection from the ledger belongs to rwb-reporting (RWB-SVC-P9).
- The schema baseline, the login, the topic and queue provisioning, the chart, the dashboards and the runbook of this service: the platform and DB stories of RWB-SVC-P7.
