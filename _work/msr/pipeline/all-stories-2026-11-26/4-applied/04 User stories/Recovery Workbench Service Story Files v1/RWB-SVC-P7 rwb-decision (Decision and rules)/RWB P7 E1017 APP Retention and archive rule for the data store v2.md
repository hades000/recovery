# RWB-P7-E1017-APP Retention and archive rule for the data store

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E1017-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-017 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P7-E |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P1-E1017-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to REQ-RDF-013) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the P7 slice of RWB-E1-017 is the ledger side of the retention key — one append-only decision record per archive or purge action of the store, the exclusion of every table of `rwb_decision` from any retention or archive rule, the JOB-14 chain check at 02:00 and the two decision-log reads on the service base. The rule rows, their load, the archive run, the write-once container and JOB-17 are `rwb-document`'s (RWB-P5-E1017-APP), the data store and the interaction ledger are `rwb-source-data`'s (RWB-P1-E1017-APP, RWB-P1-E1017-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P7-E1017-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **internal audit lead (RW-AUDIT)**, I want **one decision record for every archive or purge action of the data store, held in an append-only and hash-chained ledger that no retention rule may name, checked daily at 02:00 and readable by decision and date range**, so that **a row that has been archived or purged can still be explained after it has gone, and the ledger that explains it can never be pruned, archived or quietly edited**.

Inside `rwb-decision` this is the ledger half of RWB-E1-017, and it is one deliverable:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1` (DP-13), topic `rwb.decision.events.v1`, Temporal task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`, and the shared topic `rwb.decision-record.v1` on which every service publishes the record of its decisions (DP-03).
- The ledger is `decision_log_entry` in `rwb_decision` (Ownership Map; TSD P7 Decision center and log v2 T3.1). Each service writes its record locally in the same transaction as its change and publishes `DecisionRecorded`; this service collects it into the ledger, alerts a gap and verifies the chain.
- **One record per action**, an action being one table and one rule within one run. The record names the run, the data product and the table, the rule version in force, the counts archived and kept, the hold report reference and the archive location (BR2, AC1).
- **The record and the action are one transaction**, written through the library of DP-03, so a unit whose record cannot be written deletes nothing (BR3, AC2; R-UNI-39).
- **The ledger is never a target.** No table of `rwb_decision` carries an age-basis column, a purge setting or an archive rule, the rwb-decision login holds no UPDATE or DELETE grant, the trigger refuses both, and a record that names a table of this schema is refused in full (BR1, AC3). This keeps legacy BR5 and legacy AC8 on the P7 side.
- **The chain is checked daily at 02:00** by JOB-14, a Temporal Schedule on queue `rwb-decision` (DP-10), reporting a break to Compliance the same day and repairing nothing by edit (BR5, AC5, AC6; NFR-035).
- **The records are read** through `GET /decision-log` (API-P7-006) and `GET /decision-log/{entryId}` (API-P7-007) of TSD P7 v2 T-A.1, by decision and date range, with the Decision log right `R` and the caller's scope (BR6, AC7).

Not this story's: the retention rule rows and their load, the archive execution, the write-once container and JOB-17 (`rwb-document`, RWB-P5-E1017-APP); the store tables, `data_product`, `sys_objects`, `sys_fields` and the interaction ledger (`rwb-source-data`, RWB-P1-E1017-APP); the reference data of the rule (`rwb-case`, DP-07); the deployment (RWB-P1-E1017-OPS) and the cross-service proof (RWB-ITG-E1017-ITG).

This story owns **no legacy acceptance criterion**: the nine criteria of RWB-E1-017 are proved by RWB-P1-E1017-APP, RWB-P5-E1017-APP and RWB-ITG-E1017-ITG, and the eight criteria in section 7 are new, tagged `(new, D-RCV-60)`, and test only this deliverable (GAP-2432; ASM-4040).

### 2. Business rationale

PDPA and the bank retention schedule limit how long personal data is kept, and the retention rule of RWB-E1-017 removes what is past its period from the live store. Removal is only defensible if the removal itself is on record: what was archived, under which rule version, how many rows went, how many a legal hold kept and where the archive copy is. That record cannot live in the rows it describes, which are gone by design, and it cannot live in a rule table, because a rule is exactly what must never expire it.

The legacy story put the rule in one line — "the decision log is not archived by this job; its retention is set by Compliance" (BR5, NFR-030, DL26) — and refused a retention load that named `decision_log_entry`. D-RCV-60 keeps the rule and gives it an owner: `decision_log_entry` is P7's table, the record is collected from `rwb.decision-record.v1` and sealed daily, and the chain is checked every day (NFR-035; JOB-14 at 02:00). Retention is P5's, the ledger stays P7's, and a refusal on this side keeps the two apart.

What the realignment changes:

1. The legacy job-run log line "count 1,250 for DP05 interaction under rule version RET-2026.11" becomes one `decision_log_entry` row per action, written through the library in the archive transaction (DP-03).
2. The payload is fixed here: run, product and table, rule version, counts, hold report reference and archive location (BR2). TSD P7 v2 T3.1 carries `rule_version` and leaves the rest to `inputs_ref`, `actions` and `outcome`; that placement is Not specified in the source documents (GAP-2426; ASM-4034).
3. Quartz JOB-17 splits into the P5 retention Schedule and the P7 chain check JOB-14 (DP-10); the lake copy of the legacy RWB-E1-014 is retired with the data lake (DP-17).

The story carries REQ-RDF-013 on the record side, REQ-DRI-002 (append only), NFR-030 (log retention is Compliance's) and NFR-035 (daily chain check, same-day report).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P1-E1017-CON | The published `rwb-source-data` retention-run contract: run start, run record and the fact shape, so the record can be asserted against a published set and its fake. The story's only contract dependency (C) |
| RWB-PLT-E1027-CON | The decision-record library of DP-03: the append, the next `chain_seq`, `prev_hash`, `entry_hash`, the `DecisionRecorded` outbox row, the append-only refusal and `DecisionLogUnavailableException` |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client and the `rwb-case` reference-data contract (DP-07): LOV-DECISION with the archive and purge codes, and the final-call and action lists, in force |
| RWB-PLT-E1071-CON | The Temporal workflow kit in namespace `rwb-recovery` (DP-10): the JOB-14 Schedule, its workflow, its activities, retry and overlap policy |
| RWB-PLT-E1044-CON, RWB-PLT-N001-CON | The per-service Flyway sequence of `rwb-decision` (DP-15) and the gateway-bff composite route (DP-19) the readers arrive through |
| RWB-P7-E1008-APP, RWB-P7-E1008-CON | The decision-log store baseline — the table, the chain columns, the append-only trigger and grants, one migration — reused, not rebuilt |
| The `rwb-access` authorise contract (P4) | The role, the scope and the Decision log right behind the two reads; consumed through the guard and faked |
| RWB-P5-E1017-APP, RWB-P1-E1017-APP | The sibling slices that perform the actions and compose the records this story holds; neither is built or changed here |

Business preconditions, read on the ledger side:

- Retention rule version "RET-2026.11" is in force with product "DP05", table `interaction` at 24 months on `occurred_at` (legacy value, assumed until Compliance supplies the bank schedule; DL26; GAP-2426; ASM-4041). This service holds no rule row.
- A legal hold keeps every row of the case (R-UNI-20, NFR-072). The count kept and the hold report reference reach the record as facts; this service reads no case and no hold.
- JOB-14 runs daily at 02:00 on queue `rwb-decision`; its timezone, page size and overlap values are Not specified in the source documents (GAP-2428; ASM-4036).
- The rwb-decision login (DP-02) is in the platform secret store; its name is Not specified in the source documents (GAP-2430; ASM-4038).
- The decision code, the final-call values and the payload placement are Not specified in the source documents (GAP-2426; ASM-4034), and so are the message ids and texts this slice adds (GAP-2427; ASM-4035).
- The release date 30 November 2026 is tentative and is copied unchanged.

### 4. Flow

1. The archive or purge action itself is performed by its owner, not here: `rwb-document` archives and deletes the rows it owns (RWB-P5-E1017-APP), `rwb-source-data` applies the same rule version to its own tables and to the interaction ledger (RWB-P1-E1017-APP).
2. For one table and one rule the owner composes one record and calls `DecisionRecordWriter` of the DP-03 library with it: run reference, data product, table, rule version in force, counts archived and kept, hold report reference, archive location (BR2).
3. The library takes the next `chain_seq` under a row lock, reads the previous `entry_hash` as `prev_hash`, computes `entry_hash` as the SHA-256 of the canonical form, and writes the entry with its `DecisionRecorded` outbox row in the action's transaction (BR1, BR3).
4. The transaction commits and only then do the archive copy and the delete become visible; a refused append rolls the unit back, so nothing is deleted and no archive copy is claimed (BR3, AC2).
5. The relay publishes `DecisionRecorded` on `rwb.decision-record.v1`; this service consumes it idempotently — dedupe on the event ID and `idempotency_key` — and collects it within the target, alerting a gap when the target is missed (BR7, AC1).
6. `ArchiveRecordGuard` validates the collected record: the decision code is a LOV-DECISION value in force, `ruleVersion` and `inputsRef` are present, and the target is no table of `rwb_decision`. A record that fails is not appended: it goes to the dead-letter topic with the check named, an incident is raised and the owning caller gets the refusal (BR1, BR4, AC3).
7. JOB-14 fires at 02:00 on queue `rwb-decision` and starts `DecisionChainCheckWorkflow`, which reads the chain in pages, recomputes every `entry_hash` and compares every `prev_hash` (BR5, AC5).
8. On a break the run ends `BROKEN`, names the first `chain_seq` whose `prev_hash` differs with both hashes, raises an incident and a Compliance task the same day, and writes no entry (BR5, AC6).
9. RW-AUDIT or RW-COMPLY reads the records through the two operations of 12.1 by decision code and date range, inside scope and with the right `R` (BR6, AC7, AC8).

Nothing here archives a row, deletes a row of the store, loads or approves a rule, runs JOB-17, writes to the archive container or changes a case status.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The record of an action cannot be written | `DecisionLogUnavailableException`, the unit's transaction rolls back, no entry, no `chain_seq` consumed, no row deleted; incident raised | MSG-P7-003 | AC2 |
| X2 | A record names a table of `rwb_decision` | Refused in full with the legacy check name; no entry, no `chain_seq` consumed | MSG-P7-009 | AC3 |
| X3 | The decision code is outside LOV-DECISION, or `ruleVersion` or `inputsRef` is absent | Refused at the schema check, the missing field named; nothing written | MSG-P7-009 | AC3 |
| X4 | An UPDATE or a DELETE on an entry is attempted | Refused four times over: the missing grant for the login, and "decision_log_entry is append only" from the trigger for the schema owner; each attempt audited | none; the database refusal | AC4 |
| X5 | The daily check finds a break | Ends `BROKEN` with the first broken `chain_seq` and both hashes; incident and Compliance task the same day; no entry edited | the break report, id Not specified (GAP-2427; ASM-4035) | AC6 |
| X6 | The same `DecisionRecorded` fact arrives twice | One entry, the first entry's ID returned, no second `chain_seq` consumed | none | AC1 |
| X7 | The ledger is unavailable for a read | Status 503, retry asked, no partial page | MSG-GEN-006 | AC7 |
| X8 | No Decision log right, or the entry is outside scope | Status 403, nothing read | MSG-P4-002 | AC7 |
| X9 | A record arrives after the collection target, or an action of a run has none | The gap is alerted and listed in the collection report; a late record is still collected; an action with no record is reported to Compliance | the gap alert, id Not specified (GAP-2427; ASM-4035) | AC1 |

X1 to X3 are the legacy AC8 family on the ledger side: the record is what cannot be written, cannot name the ledger and cannot be malformed. X4 is the append-only property, X5 the daily check of NFR-035, X6 idempotency, X7 and X8 the read errors, X9 the completeness target. The legacy X6 wording is kept as the check name of X2, because RWB-P1-E1017-CON and RWB-P5-E1017-APP already assert it.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against RWB-P1-E1017-CON, the decision-record library, the reference-data contract, the workflow kit and the gateway route, each with the fake of 12.8; the `decision_log_entry` baseline of RWB-P7-E1008-APP is reused |
| Negotiable | The decision code, the final call and the action values are reference data; the run, the counts and the location are facts of the action. The story fixes only the record, the exclusion, the check and the reads |
| Valuable | A removed row can still be explained after it is gone, and the ledger that explains it cannot be pruned, archived or edited |
| Estimable | One consumer with an inbox, one guard, one contract, one repository, two reads, one workflow with three activities and one Schedule |
| Small | Two weeks with its tests, as one of six slices of a key already split across P1, P5, P7, the wave 1 integration story and the deployment story |
| Testable | Every criterion runs on synthetic facts with a fixed clock, a stubbed library and a stubbed chain; no ACE data and no production data |

### 7. Acceptance criteria

```gherkin
Feature: The decision ledger records every archive or purge action of the store

  Background:
    Given retention rule version "RET-2026.11" holds product "DP10", table "document", age basis "created_at", 24 months
    Given the run date is Sunday 2026-12-06
    Given the rwb-source-data retention-run contract mock returns run "run-2026-12-06" of 2026-12-06 with rule version "RET-2026.11", 1,250 interaction rows archived under "retention/2026-12-06/interaction/" and 40 rows kept for case "RW-2024-000311"
    Given the rwb-case reference-data contract mock returns LOV-DECISION with the archive and purge decision codes in force
    Given the decision-record library takes the next chain_seq, the previous entry's entry_hash as prev_hash and the SHA-256 of the canonical form as entry_hash
    Given the rwb-decision property "rwb.decision.ledger.archive-excluded-tables" names decision_log_entry, approval, rule_package, rule_package_version, rule_row and rule_test_case

  Scenario: AC1 One record per action, written with the action (new, D-RCV-60)
    Given 1,250 document rows of product "DP10" are archived under "retention/2026-12-06/document/" and 40 rows of case "RW-2024-000311" are kept
    When rwb-document writes the record of that action through the decision-record library
    Then one "decision_log_entry" row exists with chain_seq 4821, that record as its canonical form and the SHA-256 of it as entry_hash
    And the record holds the archive decision code from LOV-DECISION, run reference "run-2026-12-06" in inputsRef, rule_version "RET-2026.11", product "DP10", table "document", 1,250 archived, 40 kept, the hold report reference and the archive location "retention/2026-12-06/document/"
    And the record holds no name, no person key, no case number and no row content
    And the same transaction writes the DecisionRecorded outbox row on rwb.decision-record.v1 and commits the archive and the delete of the 1,250 rows
    When the same DecisionRecorded fact is replayed with the same event ID and idempotency key
    Then one entry exists for the action and no second chain_seq is consumed

  Scenario: AC2 A record that cannot be written deletes nothing (new, D-RCV-60)
    Given the decision-record library refuses the append with DecisionLogUnavailableException
    When rwb-document runs the archive action of 1,250 rows
    Then no "decision_log_entry" row is stored and chain_seq 4821 is not consumed
    And the unit's transaction rolls back, so no row is deleted and no archive copy is claimed
    And the caller receives MSG-P7-003 and an incident is raised to the platform administrator queue

  Scenario: AC3 No rule may name the ledger (new, D-RCV-60)
    Given an archive action whose rule names product "DP12", table "decision_log_entry"
    When the record of that action is offered to the ledger
    Then the ledger refuses the record with MSG-P7-009 and the check "decision_log_entry is not archived by the retention job"
    And no "decision_log_entry" row is written and no chain_seq is consumed
    And the record of an action on "approval", "rule_package", "rule_package_version", "rule_row" or "rule_test_case" is refused with the same check
    And no table of "rwb_decision" carries an age-basis column, a purge setting or an archive rule
    And the record of an action on "document" of product "DP10" is accepted unchanged

  Scenario: AC4 An update and a delete are refused (new, D-RCV-60)
    Given an entry with chain_seq 1 and final call "ARCHIVED" is stored for run "run-2026-12-06"
    When an UPDATE of its final_call and a DELETE of the entry are attempted through the rwb-decision login and again through the schema owner role
    Then all four statements are refused, by the missing grant for the service login and with "decision_log_entry is append only" from the trigger for the schema owner
    And the entry is unchanged with the same final call, the same prev_hash and the same entry_hash
    And each refused attempt is written to the ACE audit log with the table, the operation and the entry ID

  Scenario: AC5 The daily chain check on an intact chain (new, D-RCV-60)
    Given 100 entries with chain_seq 1 to 100 and the first prev_hash of 64 zeros
    When the JOB-14 chain check runs at 02:00 on 2027-01-01
    Then every entry_hash equals the SHA-256 of the entry's canonical form
    And every prev_hash equals the entry_hash of the entry before it
    And the check record holds count 100, last chain_seq 100 and that entry's entry_hash
    And the check ends "OK" and writes no entry and changes no entry

  Scenario: AC6 A break is reported the same day and nothing is repaired by edit (new, D-RCV-60)
    Given entry 4,821 of the ledger has a prev_hash that differs from the entry_hash of entry 4,820
    When the JOB-14 chain check runs at 02:00 on 2027-01-01
    Then the check ends "BROKEN" and names chain_seq 4,821 with both hashes
    And an incident and a task to Compliance are raised the same day
    And no entry is updated, deleted or rewritten, and the correction is a new entry that names the entry it corrects

  Scenario: AC7 The records are read by decision and date range (new, D-RCV-60)
    Given the archive actions of run "run-2026-12-06" wrote 2 records under the archive decision code
    When RW-AUDIT reads GET /api/recovery/decision/v1/decision-log with decision, from "2026-12-06" and to "2026-12-06"
    Then the answer is 200 with the DecisionLogPage holding 2 items and total 2
    When RW-AUDIT reads GET /api/recovery/decision/v1/decision-log/{entryId} for one of them
    Then the answer holds inputsRef "run-2026-12-06", ruleVersion "RET-2026.11", the actions with product, table, archive location, 1,250 archived and 40 kept, the outcome, decidedAt, prevHash and entryHash
    And a role without the Decision log right R is refused with status 403 and MSG-P4-002
    And an unknown entry ID answers status 404

  Scenario: AC8 The record outlives the rows it describes (new, D-RCV-60)
    Given the run of 2026-12-06 deleted its 1,250 archived rows from the live store
    When RW-AUDIT reads the record of that action one year later
    Then the record is still readable with the same run reference, table, rule version, counts, hold report reference and archive location
    And the live store holds no row of that set
    And the record names the archive location that proves where the rows went
```

The eight criteria test only this deliverable and reuse the legacy values that are its content: "RET-2026.11", 24 months, the run date Sunday 2026-12-06, 1,250 archived, case "RW-2024-000311" with 40 kept, the path `retention/2026-12-06/<table>/`, product "DP12" and table `decision_log_entry` of legacy AC8, the 100-entry chain with its 64-zero first `prev_hash`, and MSG-P7-003, MSG-P7-009, MSG-P4-002 and MSG-GEN-006. The rule rows, the load, the archive, the container and JOB-17 are not in these criteria; the two "writes the record" steps are the owners' calls of the DP-03 library, exercised here through the fakes of 12.8, and the end-to-end journey is RWB-ITG-E1017-ITG's.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The ledger is append only and hash chained: never updated, never deleted, first `prev_hash` 64 zeros, each `prev_hash` the `entry_hash` before it, a correction a new entry naming the one it corrects, and no table of `rwb_decision` a retention or archive target | FSD P7 v3 A2.1, AC-P7-001-01; NFR-030; ADR-009; DL26; legacy BR5 and AC8 |
| BR2 | One record per archive or purge action, naming the run, the product, the table, the rule version in force, the counts archived and kept, the hold report reference and the archive location, with codes, counts and identifiers only | Legacy section 4 step 9 and section 11; REQ-RDF-013; TSD P7 v2 T3.1 |
| BR3 | The record and the action are one transaction, and an action whose record cannot be written is not taken: nothing commits, no `chain_seq` is consumed, an incident is raised | Legacy BR4; R-UNI-39; FSD P7 v3 VR-P7-001-2, AC-EXC-P7-001-01 |
| BR4 | A record that fails the schema check or names a table of `rwb_decision` is refused in full, the check named, and nothing is appended | Legacy BR6 and AC8; FSD P7 v3 AC-EXC-P7-002-01, AC-EXC-P7-002-05 |
| BR5 | The chain is checked daily at 02:00, a break is reported to Compliance the same day, and the check repairs nothing by edit | NFR-035; Architecture v5 slide 44 (JOB-14); FSD P7 v3 AC-BG-P7-001-01 |
| BR6 | The records are read through the two decision-log operations by decision and date range, inside the caller's scope and with the Decision log right `R` | TSD P7 v2 T-A.1 API-P7-006 and API-P7-007, T-A.2 |
| BR7 | A record is collected within the target, a gap is alerted, and a late record is still collected; the record outlives the rows it describes | Architecture v5 slide 28; legacy section 2 |
| BR8 | The decision code, the final call and the action values are reference data read in the version in force; no code, period or table name is written in code | Principle 1; FSD P7 v3 BR-P7-001; DP-07 |

How each rule holds in `rwb-decision`: BR1 and BR4 by the absent grant, the trigger's refusal, the unique key on `chain_seq`, the property `rwb.decision.ledger.archive-excluded-tables` and `ArchiveRecordGuard`; BR3 by the library call inside the owner's transaction with `DecisionLogUnavailableException` propagating; BR2 and BR8 by the record contract of 12.1 and the reference-data client; BR5 by the JOB-14 Schedule and `DecisionChainCheckWorkflow`, with no activity that writes an entry; BR6 by the two operations, the declared right, the scope filter and the paging.

### 9. State transitions

No case status, document state or rule version changes here. The record and the check have these states:

| From | Event | Condition | To |
|---|---|---|---|
| (none) | The owner writes the record in the action's transaction | The append succeeds | Entry appended and committed with the action |
| (none) | The owner writes the record | The append fails | No entry, `chain_seq` free, the unit rolled back |
| Published | The `DecisionRecorded` fact reaches the topic | The guard passes | Collected within the target |
| Published | The fact reaches the topic | The guard refuses it | Not collected; dead-letter fact, incident and named check |
| Collected | The same fact is replayed | Same event ID and idempotency key | Unchanged; one entry, one `chain_seq` |
| Chain OK | The JOB-14 check at 02:00 | Every hash matches | Check record `OK` with the last `chain_seq` and hash |
| Chain OK | The JOB-14 check at 02:00 | A `prev_hash` differs | `BROKEN` with the first break, incident and Compliance task; the ledger unchanged |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-AUDIT, internal audit | Read the archive and purge records and their hashes (Decision log R) |
| RW-COMPLY, Compliance and PDPA officer | Read the same records, own the log retention (NFR-030), receive the chain-break task the same day |
| RW-PLATADM, platform administrator | Read the check record and the collection gaps; take the incident a refused record raises |
| The rwb-decision service identity | Run the JOB-14 check, collect the facts, append to the ledger, raise the incidents |
| The rwb-document and rwb-source-data service identities | Write the record of their own action through the library, in that action's transaction |
| `rwb-case` (P3) | Own LOV-DECISION and the value lists; answer the reference-data read |
| `rwb-access` (P4) | Own the roles, the scope and the Decision log right |
| Nobody | Update or delete an entry, archive the ledger, add a purge setting or an age-basis column, or repair a break by edit |

Separation of duty: the role that reads is not the role that writes, and the appending identity writes no business row. No person is named. The login is the rwb-decision login (DP-02); its name is Not specified in the source documents (GAP-2430; ASM-4038).

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-003 | `decision_log_entry` | id, case_id, decision_code | Write; `decision_code` from LOV-DECISION in force and read by the search |
| DF-DEC-004 to DF-DEC-007 | `decision_log_entry` | rule_id, rule_version, model_version, agent_version | Write `rule_version` with the version in force; `rule_id` empty, because no Drools rule decides an archive action; model and agent empty |
| DF-DEC-008 | `decision_log_entry` | inputs_ref | Write the run reference, "run-2026-12-06" in the scenarios |
| DF-DEC-009 to DF-DEC-011 | `decision_log_entry` | recommendation, approver_user_id, approval_level | Write `recommendation` with the payload of 12.1; approver and level empty, because an archive action carries no delegation approval |
| DF-DEC-012 to DF-DEC-015 | `decision_log_entry` | final_call, override_reason, actions, outcome | Write the final call from its list and the actions and outcome of 12.1; `override_reason` empty |
| DF-DEC-016, DF-DEC-029, DF-DEC-030 | `decision_log_entry` | decided_at, corrects_entry_id, actor_user_id | Write the action time and the acting service identity; the correction reference on a correction only |
| DF-DEC-017, DF-DEC-018, DF-DEC-028 | `decision_log_entry` | prev_hash, entry_hash, chain_seq | Written by the library under a row lock; read by the guard and the check |
| DF-DEC-031 | `decision_log_entry` | idempotency_key | Write from the event ID and the action reference; read by the inbox |
| (library objects) | `outbox_event`, `processed_event`, `idempotency_key` | event, payload, published_at; event_id, consumer, processed_at; key, request_hash, answer | Write the `DecisionRecorded` outbox row, the inbox row of the collection and the key of a replayed fact |

Not read and not written here: `retention_rule` and `retention_action` (P5); `document`, `document_type` (P5); `interaction`, `data_product`, `data_product_load`, `sys_objects`, `sys_fields` and the extension tables (P1); `parameter_*`, `reference_*`, `lov_value` and `recovery_case` (P3); `role` and `permission` (P4); and the other P7 tables `approval`, `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case`, which this story names in the exclusion list only. The run, the product, the table, the counts, the hold report reference and the archive location have no column of TSD P7 v2 T3.1: they travel in `inputs_ref`, `actions` and `outcome`, and that placement is Not specified in the source documents (GAP-2426; ASM-4034).

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-decision` (P7); base `/api/recovery/decision/v1` (DP-13). Both paths are TSD P7 v2 T-A.1 API-P7-006 and API-P7-007 on the service base; this story fills them with the archive and purge records and adds no third path.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/decision-log` | API-P7-006: search by `caseId`, `decision`, `ruleId`, `approver`, `from`, `to`, `page`, `size`; the archive records are found by `decision` and the date range | Decision log R, scope applied | Not applicable, read only |
| GET | `/decision-log/{entryId}` | API-P7-007: one entry with its inputs reference, rule version, actions, outcome, decided time and hashes | Decision log R, scope applied | Not applicable, read only |

Answer bodies are `DecisionLogPage` (`items`, `page`, `size`, `total`) and `DecisionLogEntry` (`entryId`, `chainSeq`, `caseId`, `decisionCode`, `ruleId`, `ruleVersion`, `inputsRef`, `recommendation`, `approverUserId`, `approvalLevel`, `finalCall`, `actions`, `outcome`, `decidedAt`, `prevHash`, `entryHash`, `correctsEntryId`, `actorUserId`) of TSD P7 v2 T-A.2.

| Element of the record | Value |
|---|---|
| `decisionCode`, `finalCall` | Values of LOV-DECISION and of the final-call list in force; the values are Not specified in the source documents (GAP-2426; ASM-4034) |
| `ruleId` | Empty: an archive or purge action fires no Drools rule |
| `ruleVersion`, `inputsRef` | The rule version in force ("RET-2026.11" in the scenarios) and the run reference, so one run's records group |
| `actions`, `outcome` | Data product, table, counts archived and kept, hold report reference, archive location, result and manifest reference |

Errors: 401 no session; 403 no right or out of scope (MSG-P4-002); 404 no entry (id Not specified, GAP-2427; ASM-4035); 422 a query value outside its list (MSG-GEN-001); 503 the ledger unavailable (MSG-GEN-006). Each is an RFC 9457 problem response with `messageId` set.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 `rwb-case`, RWB-P3-E1043-CON | LOV-DECISION, the final-call and action lists in force (DP-07); read through the client library, faked; one hop, 2 s (DP-11) |
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` | The cached role, scope and Decision log right behind every read of 12.1; faked; one hop, 2 s (DP-11) |

No other service is called at run time. The facts of an action arrive on `rwb.decision-record.v1` (12.4), shaped by RWB-P1-E1017-CON, the recorded contract dependency. Both consumed contracts are carried in the dependency rows of section 13 rather than in the metadata (GAP-2429; ASM-4037).

#### 12.3 Events published

None. The topic of the service is `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1` (DP-14), and its events — EV-08, EV-09 and EV-30 — belong to the approval and rule-registry stories; a collection, a refused record and a chain check publish no event. The `DecisionRecorded` fact is published by the owner of the action through the library of DP-03, not by this story.

#### 12.4 Events consumed

| Event | Topic | Owner | Handler |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 ledger library; published here by `rwb-document` and `rwb-source-data` | `ArchiveRecordListener`: inbox dedupe on the event ID and the record's `idempotency_key`, then `ArchiveRecordGuard`, then `DecisionLogAppender` |

The fact carries the decision code, the rule version, the inputs reference, the product and table, the counts, the hold report reference, the archive location and the decided time: codes, counts, table names and identifiers only, with no row content, no name, no account number and no document (BR2). Its required fields are Not specified in the source documents (GAP-2426; ASM-4034); the shape of the P1 side is RWB-P1-E1017-CON's.

#### 12.5 Workflows and activities

| Name | Kind | Queue | Note |
|---|---|---|---|
| `DecisionChainCheckWorkflow` | Workflow, Schedule-started from the kit template "Scheduled job" | `rwb-decision` | The JOB-14 run: reads the chain in pages, verifies it, ends `OK` or `BROKEN`, reports a break |
| `readChainPage` | Activity | `rwb-decision` | One page from a `chain_seq` with `chain_seq`, `prev_hash`, `entry_hash` and the canonical form reference; page size is a property |
| `verifyChain` | Activity | `rwb-decision` | Recomputes every `entry_hash`, compares every `prev_hash`, returns count, last `chain_seq`, last `entry_hash` and the first break |
| `reportChainBreak` | Activity | `rwb-decision` | Raises the incident and the Compliance task with the first broken `chain_seq` and both hashes; writes no entry |

The workflow writes nothing to `decision_log_entry`, is the only workflow this story registers and starts no child. `ApprovalWorkflow`, the rule promotion, the continuous ingest of the topic and the JOB-17 archive run are other stories'.

#### 12.6 Schedules

| Job | Name | When | Owner | Mechanism |
|---|---|---|---|---|
| JOB-14 | Hash-chain check | Daily, 02:00 | rwb-decision | Temporal Schedule on queue `rwb-decision` starting `DecisionChainCheckWorkflow`, with an overlap policy so one check runs at a time and a catch-up window (DP-10) |

The time 02:00 is fixed by Architecture v5 slide 44; its timezone, the page size and the overlap and catch-up values are Not specified in the source documents (GAP-2428; ASM-4036). No shared Quartz table is written and no other service's job row is read. JOB-17 "Retention" is `rwb-document`'s Schedule, not registered, started or read here.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `decision_log_entry` | P7 (`rwb_decision`) | One append-only, hash-chained entry per archive or purge action; read through the two operations; never updated or deleted |
| decision-record library objects | P7 rows in `rwb_decision`, written through the library of DP-03 | The append and its chain |
| `outbox_event`, `processed_event`, `idempotency_key` | Platform library, created in `rwb_decision` | The `DecisionRecorded` outbox row, the inbox of the collection and the replayed key |
| `approval`, `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` | P7 (`rwb_decision`) | Named in the exclusion list only; not read and not written here |

Not owned and never read: `retention_rule` and `retention_action` (P5), `document` and `document_type` (P5), `interaction` and the data-product tables (P1), `parameter_*`, `reference_*`, `lov_value` and `recovery_case` (P3), `role` and `permission` (P4). No foreign key crosses a schema (DP-01). The one migration adds the keys and the search indexes named in section 13 and no age-basis column or purge setting, so this schema has nothing for a retention rule to act on (BR1, AC3).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-source-data retention-run fake | RWB-P1-E1017-CON | Run "run-2026-12-06" with rule version "RET-2026.11", 1,250 rows under `retention/2026-12-06/interaction/` and 40 kept for case "RW-2024-000311"; a completed run, a run with no archived row, a run with no record |
| rwb-case reference-data fake | RWB-P3-E1043-CON (DP-07) | LOV-DECISION with the archive and purge codes, the final-call and action lists, and an unknown code for X3 |
| rwb-access authorise fake | P4 authorise contract (DP-11) | The allow answer for Decision log `R` in scope, the refusal with MSG-P4-002, and an entry out of scope |
| decision-record library fake | RWB-PLT-E1027-CON | The append, the next `chain_seq`, `prev_hash`, `entry_hash` and the canonical SHA-256, the 64-zero first `prev_hash`, the append-only refusal, the replayed key and the forced `DecisionLogUnavailableException` of AC2 |
| chain fixture and workflow kit fake | This story; RWB-PLT-E1071-CON | 100 intact entries, the same 100 with 4,821's `prev_hash` changed, a 12,480-entry chain, and the 02:00 Schedule with its overlap and retry policy |
| gateway-bff route fake | RWB-PLT-N001-CON | The route a reader reaches the two reads through, so the scope and the refusals can be asserted |

Each fake is replaced by the real contract or library as its story lands, without a change to the scenarios, and carries synthetic references, versions, codes and counts only.

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2, consumed 2 | `GET /decision-log` and `GET /decision-log/{entryId}`; the reference list and the authorise decision, one hop and 2 s with a breaker per downstream (DP-11) |
| Kafka | Published 0, consumed 1 | `rwb.decision-record.v1` consumed into the ledger with an inbox; no event published and no new topic |
| Temporal | 1 workflow, 3 activities, 1 Schedule | `DecisionChainCheckWorkflow` on queue `rwb-decision` with `readChainPage`, `verifyChain` and `reportChainBreak`, started by JOB-14 at 02:00 |
| File | None | No file is read or written; the archive copy and its manifest are `rwb-document`'s and `rwb-source-data`'s |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `log/archive-records`, Java package `th.co.scb.ace.workbench.recovery.decision.archive`.

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

How each row is applied: **DP-01** every table it touches sits in `rwb_decision`, the facts arrive on the shared topic and the six excluded tables are refused targets, never queried. **DP-03** is the centre: the library appends in the action's transaction, publishes `DecisionRecorded` and fails closed. **DP-07** keeps LOV-DECISION and the value lists out of the code. **DP-10** is the JOB-14 Schedule and its workflow, **DP-11** the one-hop shape of the two consumed calls, **DP-13** the service base, **DP-15** the one migration, **DP-19** the composite route. The dependency rows the metadata does not carry are recorded in GAP-2429 and ASM-4037; ready to start stays Day 1, because every H is a wave 0 platform contract and a C never blocks (R5.7 rules 2 and 8).

| Component | Type | Responsibility |
|---|---|---|
| ArchiveRecordListener | Kafka consumer with an inbox | Reads `DecisionRecorded`, dedupes on event ID and key, hands the record to the guard and the appender |
| ArchiveRecordGuard | Service | The LOV check, the required-field check and the exclusion list (BR1, BR8) |
| DecisionLogAppender, DecisionRecordFailClosedHandler | Services | Next `chain_seq`, `prev_hash`, `entry_hash`, entry and outbox row in one transaction through the library; a failure maps to MSG-P7-003 and an incident (BR3) |
| LedgerCollectionMonitor | Service | Reports an action with no record and a record after the target |
| ChainCheckWorkflowImpl, ChainVerifier, ChainBreakReporter | Workflow and services | The JOB-14 run, the recomputation and the report of the first break (BR5) |
| DecisionLogQueryController, DecisionLogRepository | Controller and repository | The two operations with the right, the scope and the paging over `decision_log_entry` |
| ReferenceDataClient, AccessCheckClient | Clients | The two consumed calls, one hop with a 2 s timeout and a breaker |

**Migration (DP-15).** One step on the per-service Flyway sequence, `V1017_1__decision_archive_records.sql`: `ux_decision_log_entry_chain_seq` on `(chain_seq)` and `ux_decision_log_entry_idempotency` on `(idempotency_key)`, plus `ix_decision_log_entry_decision_time` on `(decision_code, decided_at)` and `ix_decision_log_entry_inputs` on `(inputs_ref)` — no column, no age-basis column, no purge setting, no archive rule, no seed row (BR1, AC3). The trigger and grants are the baseline's (RWB-P7-E1008-APP), reused and reconciled at the first joint environment.

**Configuration and reference data.** `rwb.decision.ledger.archive-excluded-tables` names the six tables and is the only place the list exists; `rwb.decision.chain-check.run-time=02:00`, `page-size=5000` and `rwb.decision.ledger.collection-target=5m` hold the check and the completeness target. Everything but the 02:00 time and the table list is Not specified in the source documents (GAP-2428; ASM-4036). LOV-DECISION and the value lists are read through DP-07 (BR8); the decision code and final-call values are Not specified in the source documents (GAP-2426; ASM-4034).

**Build steps.**

1. The migration and a test that an UPDATE and a DELETE are still refused and that no table of `rwb_decision` gained an age-basis column or a purge setting.
2. `DecisionLogAppender` over the library — next `chain_seq` under a row lock, `prev_hash`, `entry_hash`, the outbox row, one transaction (AC1, TC-E1-017-09).
3. `DecisionRecordFailClosedHandler` and the rollback path of AC2 with the forced library failure of 12.8.
4. `ArchiveRecordListener` with the inbox and the key; the replay of X6 and the gap report of X9.
5. `ArchiveRecordGuard` with the LOV, required-field and exclusion checks (AC3, X3).
6. `DecisionLogRepository` and `DecisionLogQueryController` with the search, the paging, the scope and the 401 to 503 answers (AC7, TC-E1-017-10).
7. `ChainVerifier`, `ChainCheckWorkflowImpl` and `ChainBreakReporter` (AC5, AC6, TC-E1-017-05), with the page boundary of a 12,480-entry chain.
8. The JOB-14 Schedule at 02:00 with its overlap policy, and a test that two runs cannot overlap and a break is reported the same day.
9. The privacy test: record, fact, check report and read answers hold references, codes, table names, counts, a location and hashes only.

**Feature flag.** `rwb.decision.ledger.archive-records`. Off: the collection pauses, the check does not run and the two reads answer as of the last committed entry, so an audit answer is never silently complete; the exact answer is Not specified in the source documents (GAP-2428; ASM-4036).

**Done when.** The tests in section 16 pass; SIT shows one entry per action of a synthetic run on 2026-12-06 with its run reference, table, rule version, 1,250 and 40 counts, hold report reference and archive location; a forced library failure deletes nothing and raises MSG-P7-003; a record naming `decision_log_entry` is refused with the legacy check name; an UPDATE and a DELETE are refused with "decision_log_entry is append only"; the 02:00 check returns `OK` on an intact 12,480-entry chain and `BROKEN` on a tampered one; the two reads return the run's records by decision and date range.

### 14. Validation and messages

| ID | When | Message | Produced by |
|---|---|---|---|
| MSG-P7-003 | The record of an action cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The library path, on the action's transaction (AC2) |
| MSG-P7-009 | A record is refused: the code is outside LOV-DECISION, `ruleVersion` or `inputsRef` is absent, or the target is a table of `rwb_decision` | Not specified in the source documents (GAP-2427; ASM-4035) | The guard, on the collection (AC3) |
| MSG-P4-002 | No Decision log right, or the entry is outside scope | You cannot {action} here. Your role does not include it. | The guard, on the two reads (AC7) |
| MSG-GEN-006 | The ledger is unavailable for a read | {system} is not available. Your request is queued and will be retried. | The two reads (X7) |
| (not-found response) | No entry for the ID | Not specified in the source documents (GAP-2427; ASM-4035) | The entry read |
| (break report) | The JOB-14 check finds a break | Not specified in the source documents (GAP-2427; ASM-4035) | `reportChainBreak` (AC6) |
| (gap alert) | An action has no record, or its record is late | Not specified in the source documents (GAP-2427; ASM-4035) | `LedgerCollectionMonitor` (X9) |

MSG-P7-003 and MSG-P4-002 are copied unchanged from the legacy story and FSD P7 v3 A2.1.3.1; MSG-P7-009 is the message the FSD names for a record refused at the schema check without writing it out, so its text stands as Not specified; MSG-GEN-006 is the generic unavailability text. The check name of AC3 is the legacy AC8 wording character for character, because RWB-P1-E1017-CON and RWB-P5-E1017-APP already assert it. Thai text follows decision DL10. HTTP mapping: 403 for MSG-P4-002, 422 for MSG-GEN-001, 503 for MSG-GEN-006; a refused record is not an HTTP answer of this service.

### 15. Screens and states

No screen is built here. The two reads serve the decision-log view an audit or compliance reader uses, and that screen belongs to the Epic 8 administration work; the gateway-bff route of DP-19 is the path. The check has no screen either: its result is the check record and the incident of a break.

| Where | State | What the reader sees |
|---|---|---|
| Decision-log read | Collected | The record with its run reference, product, table, rule version, counts, hold report reference, archive location, decided time and hashes |
| Decision-log read | Refused record | Nothing: a refused record is not in the ledger; the owning caller has its message and the platform administrator the incident |
| Entry read | Appended | The same fields of one entry with `prevHash`, `entryHash`, `chainSeq` and the correction reference |
| Check record of JOB-14 | OK | The count, the last `chain_seq`, the last `entry_hash` and the run time |
| Check record of JOB-14 | BROKEN | The first broken `chain_seq`, both hashes and the Compliance task of the same day |

The record has no state a person sets: it is appended, collected and read. Its retention is Compliance's and outside this story (NFR-030).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-017-01 | AC1, BR2 | Component | Run "run-2026-12-06"; product DP10 `document`, 1,250 archived and 40 kept; rule version RET-2026.11; library fake with `chain_seq` 4821 |
| TC-E1-017-02 | AC2, BR3 | Component | Library fake forced to `DecisionLogUnavailableException`; no entry, `chain_seq` 4821 free, no delete |
| TC-E1-017-03 | AC3, BR1, BR4 | Contract | A record naming product DP12 table `decision_log_entry` and five naming the other tables; one naming `document` accepted |
| TC-E1-017-04 | AC4, BR1 | Component | An UPDATE of `final_call` and a DELETE through the service login and the schema owner; "decision_log_entry is append only" |
| TC-E1-017-05 | AC5, BR5, NFR-035 | NFR | 100 intact entries and a 12,480-entry chain; the 02:00 run inside the Schedule window |
| TC-E1-017-06 | AC6, BR5 | Component | Entry 4,821 with a `prev_hash` differing from 4,820's `entry_hash`; `BROKEN`, incident and Compliance task the same day |
| TC-E1-017-07 | AC7, BR6 | Contract | Decision code, from 2026-12-06 to 2026-12-06, page 1 size 20; the entry read of one record |
| TC-E1-017-08 | AC8, BR2, BR7 | End to end | The run of 2026-12-06 after its 1,250 rows are deleted; the record read a year later with the same content |
| TC-E1-017-09 | AC1, BR1 | Unit | The canonical form and its SHA-256, the 64-zero first `prev_hash`, the chain arithmetic and the page boundary |
| TC-E1-017-10 | AC7, BR6 | Contract | A role without Decision log `R` refused with MSG-P4-002; an unknown entry ID answering 404 |

The ten legacy test case IDs are kept in their legacy order and no ID is added; the P7 copy of each proves the ledger half. The legacy Level System maps to Component, Contract or End to end and Access to Contract, and NFR serves the daily check of NFR-035. The Covers column names this slice's criteria, because the legacy AC1 to AC9 are proved by RWB-P1-E1017-APP, RWB-P5-E1017-APP and RWB-ITG-E1017-ITG; the `-ITG` copies belong to RWB-ITG-E1017-ITG, and the full test with its Given, When and Then is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID.

### 17. Guardrails

- No business value in code: the decision code, the final call, the action values and the table names are data rows or properties, and the exclusion list is a property.
- No personal data in events, workflow inputs, records or logs: a run reference, codes, table names, counts, a location, a report reference and hashes only.
- No read of another service's table (DP-01): the facts arrive on `rwb.decision-record.v1`, the values on the reference-data contract, and no foreign schema appears in a query.
- The ledger is never archived, purged or edited: no age-basis column, no purge setting, no archive rule, no UPDATE or DELETE grant, and a record naming a table of `rwb_decision` is refused (BR1).
- The record and the action are one transaction, and an action whose record cannot be written is not taken (BR3).
- A chain break is reported, never repaired: the correction is a new entry naming the one it corrects, and the check runs with an overlap policy (BR5).
- One hop and a 2 s timeout on every consumed call, with a breaker per downstream (DP-11, ADR-020); a replayed fact yields one entry and one chain position.
- No data lake (DP-17), one writer of an entry (the library), and a flag that pauses the collection and the check without making an audit answer look complete when it is not.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-013 | Retention and archive rule by record class — here the record of the archive and purge action and the exclusion of the ledger from the rule | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-17 | All recovery processes | R-UNI-20, R-UNI-38, R-UNI-39; CTL-08; DL26 | TC-E1-017-01 to TC-E1-017-10 |

| Requirement or decision | Where it is carried |
|---|---|
| REQ-DRI-002, R-UNI-39 | BR1, BR3, BR4, AC1, AC2, AC4, AC6 |
| NFR-030, NFR-035, NFR-072 | BR1, BR5, AC5, AC6, section 15 |
| ADR-022; Architecture v5 slides 28 and 44 | Sections 1, 2, 4, 12.4, 12.6 |
| TSD P7 v2 T3.1, T3.2, T-A.1 API-P7-006 and API-P7-007, T-A.2 | Section 11, BR1, 12.1, AC7 |
| FSD P7 v3 A2.1 (append only, chain, nightly check), A2.2 (a failed write stops the action) | BR1, BR3, BR5 |

| Legacy reference | Where it is kept |
|---|---|
| RET-2026.11, 24 months, product DP05 table `interaction`, product DP10 table `document` | Background, sections 3, 7 and 11 |
| Run date 2026-12-06, 1,250 archived, 40 kept for case RW-2024-000311 | Background, AC1, AC2, AC8 |
| Archive path `retention/YYYY-MM-DD/<table>/`, the hold report, the AC8 check name | BR2, BR4, AC1, AC3, 12.8 |
| MSG-P7-003, MSG-P7-009, MSG-P4-002, MSG-GEN-006, the 100-entry chain with its 64-zero first `prev_hash` | Section 14, section 5, AC5, TC-E1-017-05, TC-E1-017-09 |

The legacy key is RWB-E1-017, disposition Split (rework). The other slices are RWB-P1-E1017-CON and RWB-P1-E1017-APP (the store and the interaction ledger), RWB-P5-E1017-APP (the rule, the run, the archive and JOB-17), RWB-P1-E1017-OPS and RWB-ITG-E1017-ITG. This story owns none of their criteria and keeps the ledger half of legacy BR5 and AC8.

### 19. Out of scope

- The retention rule rows, their loads, validation and approval, the archive execution, the selection, the write-once container and its manifest, JOB-17 and its Schedule with every period, table and age-basis field: `rwb-document`, P5, RWB-P5-E1017-APP; Architecture v5 slides 16, 41 and 44.
- The store tables, the data products, `data_product_load`, `sys_objects`, `sys_fields`, the extension tables and the interaction ledger: `rwb-source-data`, P1, RWB-P1-E1017-APP and RWB-P1-E1017-CON.
- The reference data of the rule and the roles: `rwb-case`, P3, DP-07 (RWB-P3-E1043-CON); `rwb-access`, P4.
- The decision-log store baseline, its trigger, its chain columns and the daily seal to write-once storage: RWB-P7-E1008-APP and RWB-P7-E1008-CON.
- The rule-promote Schedule JOB-20 at 00:01 and the rule-registry stories: RWB-P7-E2042-APP, RWB-P7-E2043-APP; the lake copy of legacy RWB-E1-014 and the retention step of JOB-13, retired with the data lake (DP-17, ADR-018).
- The chain-break screen, the decision-log screen and the administration screens that read them (Epic 8), and the personal data screen SCR-47.
- The deployment, the alerts and the runbook of the retention run: RWB-P1-E1017-OPS.
- The real cross-service proof of the rule, the hold, the archive and the ledger exclusion across P1, P3, P5 and P7: RWB-ITG-E1017-ITG.
