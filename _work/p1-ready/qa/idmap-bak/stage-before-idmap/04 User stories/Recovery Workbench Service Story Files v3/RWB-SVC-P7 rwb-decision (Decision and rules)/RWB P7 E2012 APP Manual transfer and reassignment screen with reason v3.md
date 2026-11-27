# RWB-P7-E2012-APP Manual transfer and reassignment screen with reason

**Version 3 changes.**

- RD-P1-004: Align the Error and Message Standard v6 wording.

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E2012-APP |
| Readiness decisions | RD-P1-004 |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-012 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P7-W |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P7-E2012-APP-16); the squad sizes it at refinement |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E2012-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to REQ-WKM-003, REQ-WKM-007, REQ-WKM-008, REQ-CWC-010, REQ-CWC-016) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-012 for rwb-decision — the transfer decision record, the central ledger read and the TRANSFER package version in force. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P7-E2012-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (29 resolved, 18 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **internal audit officer (RW-AUDIT)**, I want **the decision record of every manual transfer and reassignment sealed in the `rwb-decision` ledger with its rule ID, the TRANSFER package version in force, the reason code and the from and to queue and owner, and the TRANSFER version in force on a business date readable in one call**, so that **a hand-off is provable months later and no move can cite a rule version that was not in force when it happened**.

Inside `rwb-decision` this is the decision-and-ledger half of the legacy story RWB-E2-012:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1`, Temporal task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`, and the shared topic `rwb.decision-record.v1` on which the record of a move arrives (DP-03, DP-14).
- One deliverable and nothing else: the TRANSFER package row with its version rows ("TRF-2026.12" in force from 2026-12-01 and "TRF-2026.11" before it), the one call that answers which version is in force on a business date and refuses to default when none is, the acceptance of a `CASE_TRANSFERRED` record from `rwb.decision-record.v1` into the append-only, hash-chained `decision_log_entry` of `rwb_decision`, and the two reads an auditor uses on it.
- The move stays with `rwb-case`: the screen SCR-05, `POST /api/recovery/case/v1/cases/{caseId}/transfer`, the caps, the assignment swap and `rwb.case.CaseTransferred.v1` are RWB-P3-E2012-APP's. The open-deviation answer is `rwb-deviation`'s (RWB-S8-E2012-APP). The role, the right and the scope are `rwb-access`'s (P4).
- The ledger machinery — the continuous ingest of `rwb.decision-record.v1`, the single hash chain, the daily seal and the JOB-14 Schedule — is RWB-P7-E1008-APP's and is reused, not rebuilt; the TRANSFER package's authoring, four-eyes approval, promotion and rollback are RWB-P7-E1073-APP's and RWB-P7-E1021-APP's (ASM-4135, ASM-4137).
- The database login is the per-service login of DP-02 and it is Not specified in the source documents (GAP-2500; ASM-4133); this story writes "the rwb-decision login (DP-02)" and never the monolith login.

The legacy behaviour is carried unchanged: the same TRANSFER package code, the same rule ID "TRF-010" that refuses a move while a deviation is open, the same package version on the record as the version that decided, the same reason codes, the same append-only and hash-chained entry with the from and to queue and owner, the same "a failed record stops the action", and the same "no version in force is a refusal, never a default".

### 2. Business rationale

Audit found ownership changes agreed by email and debtors who met the criteria not transferred to the responsible unit (CTL-03). The legacy story ended that by giving every manual move a coded reason, a rule check, an assignment record and a decision log entry. This story is what makes the last two provable in the target: the move happens in `rwb-case`, the rule is evaluated there by the embedded Drools kit against the TRANSFER package that `rwb-decision` governs, and the record of the move is published once and sealed once, in one ledger, under one hash chain.

The realignment changes the mechanism, not the business rule:

1. The monolith's `recovery.decision_log_entry` row written through a P7 interface becomes a record published by the owning service on `rwb.decision-record.v1` and sealed by `rwb-decision` into `rwb_decision.decision_log_entry` (DP-01, DP-03, ADR-022). No caller writes this schema.
2. The rule row named on the record is still read only through the evaluated result; this story reads no workbook, no DRL source and no `rule_row` row, and it evaluates nothing (DP-04).
3. The version that decided a move is checked against the version in force on the move's business date, and a record that names a version not in force for that date is refused instead of sealed (BR2, BR5, BR11 of the legacy story; R-UNI-38).
4. The nightly copy to the data lake (JOB-13, RWB-E1-014) has no target and is gone (DP-17); the chain check becomes the JOB-14 Temporal Schedule at 02:00 on the `rwb-decision` queue, owned by RWB-P7-E1008-APP, and this story registers its entries with it (DP-10).
5. The reason list and the caps stay `rwb-case` data; the decision code and the version-state vocabulary stay reference data of `rwb-case` read with their version (DP-07). This story writes no business value in code.

This story meets REQ-WKM-003 and REQ-WKM-008 on the record side, carries REQ-CWC-016 (the rule ID and the package version on the entry), and keeps the version half of REQ-CWC-010 and of R-UNI-38: a move decided under "TRF-2026.12" keeps that version on its record even after a rollback.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P3-E2012-CON | The published rwb-case contract of the manual move: the transfer request and answer, and the element shape of the record the move publishes — decision code, final call `CASE_TRANSFERRED`, rule ID, rule version, from and to queue and owner, reason code, actor, decided time, idempotency key. Faked, one hop, 2 s where a call is made (DP-11); no case, assignment or queue row is read |
| RWB-P7-E1008-APP | The ledger it lands in: the append-only `decision_log_entry` with `chain_seq`, `prev_hash` and `entry_hash`, the continuous ingest of `rwb.decision-record.v1`, the dedupe on the platform inbox and the JOB-14 chain check. Reused; built against its published set and fake (ASM-4135) |
| RWB-P7-E1021-APP, RWB-P7-E1073-APP | The TRANSFER package and its version rows in the registry, and the authoring pipeline that loads, tests, approves, promotes and rolls back a version. This story names the versions and reads the one in force; it loads and approves none (ASM-4137) |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03) |
| RWB-PLT-TE006-CON | The outbox, inbox and idempotency library (DP-09): one envelope, one dedupe key, retry and `.dlt` |
| RWB-PLT-E1047-CON | The naming library (DP-14): the topic and event names of section 12 |
| RWB-PLT-E1044-CON | The per-service Flyway sequence and migration conventions (DP-15) |
| RWB-PLT-E1042-CON, RWB-PLT-E1071-CON, RWB-PLT-E1072-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-N001-CON, RWB-P7-E1073-APP | The parameters, workflow, Drools, reference-data and route baselines of the DP table of section 13; this story claims no business parameter and evaluates no package (ASM-4134). The DP-added platform and published contracts are non-blocking and built against their fakes (GAP-2501) |

Business preconditions carried from RWB-E2-012:

- The TRANSFER package exists with version "TRF-2026.12" in force from 2026-12-01 and "TRF-2026.11" in force before it; row "TRF-010" refuses a move while a deviation is open (legacy sections 3, 7 and 8; FSD P7 AC-EXC-P7-007-05).
- The reason codes are the six of LOV-TRANSFER-REASON in force — R01 Capacity, R02 Customer deceased, R03 Skill, R04 Owner absent, R05 Legal referral, R06 Wrong queue (DL23) — held as rwb-case reference data and never frozen here. Who may add, change or retire a code is Not specified in the source documents (GAP-0712).
- RW-TEAMMGR holds Decision log R and Queue and allocation U; RW-CAPACITY holds Queue and allocation RU with scope All; RW-AUDIT holds Decision log R; RW-CASEOWN holds Decision log R and cannot transfer. No approval level from the delegation of authority applies: a transfer moves work, not money (legacy section 10; ASM-4136).
- The business date of the move is the date the version in force is resolved against, and it is the date carried on the record; a move of 2026-12-15 under "TRF-2026.12" stays under it (legacy BR11).
- The rwb-decision login (DP-02) is in the platform secret store; its name is Not specified in the source documents (GAP-2500; ASM-4133).
- Synthetic data only: cases, queues, owners, rule IDs and reason codes of the legacy story, never a real account, customer or assignment.
- Contract version of RWB-P3-E2012-CON that this story builds against: Not specified in the source documents (DOR-RWB-P7-E2012-APP-23).
- HTTP 404 for an unknown package code or entry: message ID Not specified in the source documents (DOR-RWB-P7-E2012-APP-8).
- Activity timeouts of EvaluateRules and RecordAndApply, and the five alert thresholds (move rate, refusal rate by code, at-cap hits, budget breaches, dead-letter depth): Not specified in the source documents (GAP-0713).
- The operations of the consumed contracts other than RWB-P3-E2012-CON (the LOV-TRANSFER-REASON reference-data read, the rwb-decision package read, the rwb-access authorise call and the rwb-source-data case-facts read) are taken from each owner's CON story as published and called through the generated client; the 2 s budget and the breaker of DP-11 apply (GAP-3092).

### 4. Flow

1. Team manager: moves a case in `rwb-case` — one call per case, single or a selection — with the reason code, the target queue or owner and the note; `rwb-case` checks the reason, the case state, the hold and the scope, evaluates the TRANSFER package through its embedded Drools kit, swaps the assignment and writes its local decision record in the same transaction (RWB-P3-E2012-APP; legacy section 4).
2. `rwb-case`: publishes the record on `rwb.decision-record.v1` through its outbox in that transaction, in the CloudEvents 1.0 envelope, keyed by the case ID and carrying the record's idempotency key (DP-09).
3. `rwb-decision` ingest (RWB-P7-E1008-APP): receives the envelope, drops it when `source` is this service, dedupes on the inbox key and hands the `CASE_TRANSFERRED` record to this story's validator.
4. `TransferRecordValidator`: checks the record against the contract element of RWB-P3-E2012-CON — decision code present and a value of LOV-DECISION, final call `CASE_TRANSFERRED`, rule ID and rule version both present, reason code present, actor and decided time present, and at least one queue or owner on each side of the move. A malformed record is not sealed: it is refused with MSG-P7-009, sent to `rwb-decision.dlt`, and an incident is raised (BR3, BR6).
5. `VersionInForceService`: resolves the TRANSFER version in force on the record's business date from `rule_package_version`. A record that names a version other than the one in force for its date is refused with MSG-P7-009 naming `ruleVersion`; no default version is ever substituted (BR5, BR11).
6. The ingest chain of RWB-P7-E1008-APP: appends one `decision_log_entry` in `rwb_decision` with the next `chain_seq`, `prev_hash` set to the entry before it (64 zeros for the first), `entry_hash` as the SHA-256 of the canonical form, the decision code, the rule ID, the rule version, the case ID, the inputs reference, the actions (from and to queue and owner, reason code) and the outcome — one transaction, one entry per record.
7. The same transaction marks the inbox key done, so a redelivery of the same envelope finds the entry and writes nothing.
8. RW-AUDIT: reads the transfer records with `GET /api/recovery/decision/v1/decision-log` by case, decision, rule, approver or date range, and one entry with `GET /api/recovery/decision/v1/decision-log/{entryId}`, with its inputs reference, rule ID, rule version, actor, final call, actions, outcome, decided time, previous hash and entry hash.
9. RW-AUDIT or RW-COE: reads `GET /api/recovery/decision/v1/admin/rule-packages/TRANSFER/versions` to see which version was in force on a business date and which one replaced it; on 2026-12-20 no version is in force and the answer says so with MSG-P3-027 instead of naming a default.
10. At 02:00 the JOB-14 Schedule of RWB-P7-E1008-APP verifies the chain from `chain_seq` 1 to the last entry, including the transfer entries, and reports a break to Compliance the same day (NFR-035).
11. Nothing in this story moves a case, picks an owner, checks a cap, reads a deviation or evaluates a package: the record, the ledger read and the version in force are the whole deliverable.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A record with no decision code, or one that is not a value of LOV-DECISION | Refused; no entry is written; the envelope goes to `rwb-decision.dlt` and an incident is raised | MSG-P7-009 | AC5 |
| X2 | A record with a rule ID and no rule version | Refused; no entry is written; the refusal names `ruleVersion` | MSG-P7-009 | AC5 |
| X3 | A record whose rule version was not in force on its business date | Refused; no entry is written; the entry of the version in force is untouched | MSG-P7-009 | AC6 |
| X4 | The same envelope is delivered twice | One entry; the second delivery finds the inbox key and writes nothing | None | AC2 |
| X5 | The ledger write fails inside the transaction (chain, unique key, database) | Nothing is committed, the envelope is retried and then sent to the `.dlt` with an incident; no partial entry and no gap in `chain_seq` | MSG-P7-003 | AC2, TC-E2-012-14 |
| X6 | A read from a role without Decision log R, or a case outside the caller's scope | 403 with MSG-P4-002; nothing is read | MSG-P4-002 | AC9, TC-E2-012-13 |
| X7 | No session, or no Recovery Workbench role | 401 with MSG-P4-001; nothing is read | MSG-P4-001 | AC9 |
| X8 | No TRANSFER version is in force on the requested business date | The version list answers that none is in force for that date with MSG-P3-027; no version is named as a default | MSG-P3-027 | AC6, TC-E2-012-15 |
| X9 | A chain break is found by the JOB-14 run | The run ends failed naming the first broken `chain_seq` and the break is reported to Compliance the same day; no entry is edited or removed | None | AC8 |

The move itself never waits on `rwb-decision`: the local record of `rwb-case` is written in the move's transaction, so a refusal here leaves the case, its assignment and its event exactly as the move left them (legacy BR8, kept at the owning service). The legacy criteria of the write failure stay with RWB-P3-E2012-APP for the move and with this story for the ledger copy.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P3-E2012-CON, the ledger of RWB-P7-E1008-APP, the TRANSFER versions of the registry and the platform contracts of its DP table; it moves no case and evaluates no package |
| Negotiable | Version labels, reason codes, decision codes and the page size are registry and reference data; the story fixes only the checks, the sealing and the read |
| Valuable | Every manual move is provable in one ledger with the rule and the version that decided it, and no record can name a version that was not in force |
| Estimable | One consumer, one validator, one version resolver, one repository and two read operations |
| Small | Fits one sprint with its tests |
| Testable | Each criterion is a consumed envelope, a refused record, a read or a version lookup, with a fixed Given, When and Then |

### 7. Acceptance criteria

```gherkin
Feature: Manual transfer and reassignment screen with reason

  Background:
    Given the rwb-access contract mock returns RW-AUDIT holding Decision log R, RW-TEAMMGR holding Decision log R and Queue and allocation U, and RW-CASEOWN holding Decision log R
    Given TRANSFER package version "TRF-2026.12" is in force from 2026-12-01 and version "TRF-2026.11" was in force before it, and row "TRF-010" refuses a move while a deviation is open
    Given the rwb-case contract mock returns the transfer of case "RW-2026-000401" from queue "MTG-BKK-CO" owner "U-CO-01" to queue "LIT-BKK-01" owner "U-LO-02" with reason code "R02", rule "TRF-010", rule version "TRF-2026.12", actor "U-TM-01" and decided at 2026-12-15T10:12:00Z

  Scenario: AC1 A transfer record is sealed into the ledger (new, D-RCV-60)
    Given the rwb-case contract mock returns the record with final call "CASE_TRANSFERRED" and decision code of the LOV-DECISION list
    When the record arrives on rwb.decision-record.v1
    Then one decision_log_entry is written in rwb_decision with case_id "RW-2026-000401", final_call "CASE_TRANSFERRED", rule_id "TRF-010" and rule_version "TRF-2026.12"
    And the entry holds the decision code from the LOV-DECISION list, the actor "U-TM-01", inputs_ref and decided_at 2026-12-15T10:12:00Z
    And actions hold fromQueue "MTG-BKK-CO", toQueue "LIT-BKK-01", fromOwner "U-CO-01", toOwner "U-LO-02" and reasonCode "R02"
    And the entry holds the next chain_seq, its prev_hash equal to the entry_hash of the entry before it and its entry_hash equal to the SHA-256 of its canonical form
    And no case, assignment, queue or owner row is changed by rwb-decision

  Scenario: AC2 A redelivery or a failed write leaves one entry and no gap (new, D-RCV-60)
    Given the record of AC1 is sealed with the inbox key of its envelope
    When the same envelope is delivered a second time
    Then the ingest finds the inbox key and writes no second entry
    And GET /api/recovery/decision/v1/decision-log?caseId=RW-2026-000401 returns one entry
    When a further record is delivered and the ledger write fails inside the transaction
    Then nothing is committed, the envelope is retried and then sent to rwb-decision.dlt with an incident
    And chain_seq holds no gap and no entry is edited

  Scenario: AC3 The transfer records are readable by case, rule and date (new, D-RCV-60)
    Given ten records of one selection are sealed, each with its own rule ID and rule version
    When RW-AUDIT reads GET /api/recovery/decision/v1/decision-log with caseId "RW-2026-000401", ruleId "TRF-010", from 2026-12-01 and to 2026-12-31
    Then the answer is 200 with the entry of the move of AC1
    When RW-AUDIT reads the same operation for the ten records with page 0 and size 20
    Then the answer is 200 with ten entries, each naming its own rule ID and rule version
    And no entry of another decision code is in either answer

  Scenario: AC4 One entry answers the audit question in full (new, D-RCV-60)
    Given the record of AC1 is sealed
    When RW-AUDIT reads GET /api/recovery/decision/v1/decision-log/{entryId}
    Then the answer is 200 with inputsRef, decisionCode, ruleId "TRF-010", ruleVersion "TRF-2026.12", actorUserId, finalCall "CASE_TRANSFERRED", decidedAt 2026-12-15T10:12:00Z, actions with the from and to queue and owner and the reason code "R02", outcome, prevHash, entryHash and chainSeq
    And no name, e-mail address, mobile number, national identity number or account number is in the answer

  Scenario: AC5 A malformed record is refused and not sealed (new, D-RCV-60)
    Given the rwb-case contract mock returns a record with rule "TRF-010" and an empty rule version
    When the record arrives on rwb.decision-record.v1
    Then it is refused with MSG-P7-009 naming "ruleVersion" and no decision_log_entry is written
    And the envelope is on rwb-decision.dlt and an incident is raised with the case ID and the missing field
    Given the rwb-case contract mock returns a record with decision code "D99"
    When the record arrives on rwb.decision-record.v1
    Then it is refused with MSG-P7-009 naming "decisionCode" and no entry is written

  Scenario: AC6 The version in force decides, and a record may not name another (new, D-RCV-60)
    When RW-AUDIT reads GET /api/recovery/decision/v1/admin/rule-packages/TRANSFER/versions
    Then the answer is 200 with "TRF-2026.12" at "IN_FORCE" from 2026-12-01 and "TRF-2026.11" at "SUPERSEDED"
    And the version in force on 2026-12-15 is "TRF-2026.12" and the version in force on 2026-11-30 is "TRF-2026.11"
    And the version in force on 2026-12-20 is none, answered with MSG-P3-027 for the package in force check naming the package code TRANSFER and the business date 2026-12-20, and no version is named as a default
    Given the rwb-case contract mock returns a record of 2026-12-20 naming rule version "TRF-2026.11"
    When the record arrives on rwb.decision-record.v1
    Then it is refused with MSG-P7-009 naming "ruleVersion" and no entry is written

  Scenario: AC7 A move keeps the version it was made under (new, D-RCV-60)
    Given the move of AC1 is sealed under "TRF-2026.12"
    When RW-COE rolls version "TRF-2026.12" back to "TRF-2026.11"
    Then the entry of the move keeps rule_version "TRF-2026.12"
    And a move made on 2026-11-30 is sealed with rule_version "TRF-2026.11"

  Scenario: AC8 The chain check covers the transfer entries (new, D-RCV-60)
    Given twenty transfer entries are sealed from chain_seq 1
    When the JOB-14 chain check Schedule runs at 02:00 on the rwb-decision queue
    Then the run verifies every entry from chain_seq 1 to the last and answers count 20, last chain_seq 20 and that entry's entry_hash
    And with one entry's canonical form altered, the run ends failed naming the first broken chain_seq and the break is reported to Compliance the same day

  Scenario: AC9 The ledger read needs the decision-log right and the scope (new, D-RCV-60)
    Given the rwb-access contract mock returns RW-CASEOWN holding Decision log R and a role holding no Decision log right
    When RW-CASEOWN reads GET /api/recovery/decision/v1/decision-log?caseId=RW-2026-000401
    Then the answer is 200 with the entry of AC1
    When the role with no Decision log right reads the same operation, or a caller of another scope reads the entry by id
    Then the answer is 403 with MSG-P4-002 and nothing is read
    When the call carries no session
    Then the answer is 401 with MSG-P4-001

  Scenario: AC10 The decision code and the version states come from reference data (new, D-RCV-60)
    Given the LOV-DECISION list and the version states of the registry are read as reference data
    When the record of AC1 is sealed
    Then the decision code of the entry is a value of LOV-DECISION and the version states come from reference data with the version in force
    And no decision code or version state is written in code

  Scenario: AC11 An unknown entry is answered 404 (new, D-RCV-60)
    Given the entry ID in the request is held by no decision_log_entry
    When RW-AUDIT reads GET /api/recovery/decision/v1/decision-log/{entryId} with that entry ID
    Then the answer is 404 and no entry is returned

  Scenario: AC12 A consumed call that fails or does not answer refuses the read (new, D-RCV-60)
    Given the rwb-access contract mock does not answer the Decision log right check
    When RW-CASEOWN reads GET /api/recovery/decision/v1/decision-log?caseId=RW-2026-000401
    Then the read is refused, nothing is read and an incident is raised
```

The twelve criteria are new under D-RCV-60 and test only the ledger and the version in force: no criterion moves a case, picks an owner, checks a cap, reads a deviation or evaluates the TRANSFER package. The legacy criteria of RWB-E2-012 stay with the other slices of the key — the screen, the endpoint and the caps with RWB-P3-E2012-APP, the deviation with RWB-S8-E2012-APP, the rights with the P4 stories — and the cross-service journey with RWB-ITG-E2012-ITG. This story has no screen; the empty, loading, error and no access states of SCR-05, SCR-07 and SCR-09 are RWB-P3-E2012-APP's.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The ledger is `rwb-decision`'s and no other service reads or writes `decision_log_entry`; a move's record arrives as an event and never as a call that writes the schema | DP-01; DP-03; ADR-022 |
| BR2 | The record of a move names the decision code, the final call `CASE_TRANSFERRED`, the rule ID, the rule version, the from and to queue and owner, the reason code, the actor and the decided time | legacy section 12 and AC1; FSD P7 AC-ALT-P7-002-01 |
| BR3 | A record missing the decision code, the rule version, the reason code, the actor or the decided time is refused and not sealed; a rule ID with no rule version is refused naming `ruleVersion` | FSD P7 AC-ALT-P7-002-01, AC-EXC-P7-002-01 and AC-EXC-P7-002-05 |
| BR4 | An entry is append only and hash chained: `chain_seq` without a gap, `prev_hash` equal to the entry before it and 64 zeros at the start, `entry_hash` the SHA-256 of the canonical form | FSD P7 AC-P7-001-01 and AC-ALT-P7-001-01; TSD P7 DF-DEC-017, DF-DEC-018, DF-DEC-028 |
| BR5 | The TRANSFER version in force on the business date decides the move and is the version on the record; a record naming another version is refused and a missing version is never defaulted | legacy BR11 and BR12; D-RCV-36 T3, T5, T7; R-UNI-38 |
| BR6 | One record, one entry: a redelivery of the same envelope finds its inbox key and writes nothing | legacy BR9; DP-09 |
| BR7 | A ledger write that fails commits nothing and never leaves a gap in the chain; the envelope is retried and then quarantined on `rwb-decision.dlt` with an incident | legacy BR8; FSD P7 AC-EXC-P7-002-07 |
| BR8 | The daily chain check covers every entry, reports a break to Compliance the same day, and never edits or removes an entry | FSD P7 AC-BG-P7-007-01; NFR-035; DP-10 |
| BR9 | The decision code is a value of LOV-DECISION and the version states are the vocabulary of the registry, read as reference data with the version in force and never written in code | legacy section 11; DP-07; TSD P7 T3.1 |
| BR10 | A move is read, never re-decided: this story changes no case status, no queue, no owner and no assignment, and it evaluates no rule package | legacy section 9; DP-04 |
| BR11 | The read needs Decision log R and applies the caller's scope; no approval level of the delegation of authority applies to a transfer | legacy section 10; TSD P7 T6.1 |

### 9. State transitions

This story changes no case status and no assignment. It owns the state of a consumed record and of a decision entry.

| From | Event | Condition | To |
|---|---|---|---|
| (none) | A record arrives | Every field is present, the version is in force on its date and the decision code is in the list | A new `decision_log_entry` with the next `chain_seq`; the inbox key is done |
| (none) | A record arrives | A field is missing, the decision code is unknown, or the version is not the one in force | No entry; the envelope is on `rwb-decision.dlt` with an incident |
| Sealed | The same envelope is delivered again | The inbox key is already done | Unchanged, no second entry |
| Sealed | The ledger write fails mid-transaction | The entry is not committed | Unchanged; retried, then quarantined |
| Sealed | The JOB-14 run | The chain verifies | Unchanged, the run records the last `chain_seq` and `entry_hash` |
| Sealed | The JOB-14 run | A canonical form was altered | Unchanged; the run fails and a break is reported to Compliance |

The case and assignment transitions of RWB-E2-012 — the ended assignment, the new assignment and the case's queue, owner and team — are `rwb-case`'s in the same transaction as its local record, and this story neither raises nor observes them.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-AUDIT, internal audit | Reads the transfer records and one entry with its hashes (Decision log R) |
| RW-TEAMMGR, team manager | Reads the record of a move it made (Decision log R) |
| RW-COE, center of excellence analyst | Reads the TRANSFER versions and calls the rollback that moves the pointer; this story holds no authoring (Rules and parameters C and R) |
| RW-CASEOWN, case owner | Reads the record of its own case (Decision log R); cannot transfer and cannot seal |
| The rwb-decision service identity | Consumes the envelope, validates, resolves the version and seals the entry |
| SY-DECLOG, decision-record writer | Supplies the record and its hash chain through DP-03 |
| SY-RULES, Drools evaluator | Evaluates the TRANSFER package in `rwb-case` (DP-04); this story only reads the version in force |
| Any role without Decision log R | Refused with MSG-P4-002 on every read of section 12.1 |

No person is named anywhere; the actors are roles and service identities. The preparer of the record is `rwb-case`'s actor and is carried unchanged on the entry.

Every REST operation of this story passes the rwb-access authorise check (DP-08) before it runs. The check is performed by rwb-access, this story calls it, and it holds no role table of its own. The eight roles in the table above are the roles this story recognises.

### 11. Data

| BR Field ID | Table in `rwb_decision` | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 | `decision_log_entry` | id | Write, from the record |
| DF-DEC-002 | `decision_log_entry` | case_id | Write |
| DF-DEC-003 | `decision_log_entry` | decision_code | Write, a value of LOV-DECISION read at run time from the reference data |
| DF-DEC-004, DF-DEC-005 | `decision_log_entry` | rule_id, rule_version | Write: "TRF-010" and "TRF-2026.12" in the tests |
| DF-DEC-008 | `decision_log_entry` | inputs_ref | Write |
| DF-DEC-012 | `decision_log_entry` | final_call | Write: `CASE_TRANSFERRED` |
| DF-DEC-014, DF-DEC-015 | `decision_log_entry` | actions, outcome | Write: from and to queue and owner, reason code, outcome |
| DF-DEC-016 | `decision_log_entry` | decided_at | Write |
| DF-DEC-017, DF-DEC-018, DF-DEC-028 | `decision_log_entry` | prev_hash, entry_hash, chain_seq | Write by the chain |
| DF-DEC-030, DF-DEC-031 | `decision_log_entry` | actor_user_id, idempotency_key | Write |
| DF-REF-274 to DF-REF-278 | `rule_package` | id, package_code, title, owner_role | Read: the TRANSFER package row |
| DF-REF-279 to DF-REF-294 | `rule_package_version` | id, version_label, status, valid_from, valid_to | Read: the version in force on a business date |
| DF-REF-002, DF-REF-281, DF-REF-282 | `rule_row`, `rule_package_version` | rule_id, version_label, status | Not read: they reach this story only as the rule ID and version on the record (DP-04) |
| DF-CAS-001, DF-CAS-009, DF-CAS-010, DF-CAS-011, DF-WRK-039, DF-WRK-040 | `recovery_case`, `assignment` (P3) | id, owner, queue, team, queue_id, transfer_reason_code | Not read: they arrive as the record's actions through RWB-P3-E2012-CON |

The ledger and the registry are `rwb-decision`'s and no other service reads them (DP-01). The field IDs of `decision_log_entry` are those of TSD P7 v2 T3.1; the registry field IDs are those the P7 registry stories cite from the Logical Data Model and Data Dictionary. No new field is added by this story: the migration of section 13 adds two indexes and no column. The event this story consumes is rwb.decision.DecisionRecorded.v1 on the shared topic rwb.decision-record.v1 (DP-14); the ingest, the single hash chain, the daily seal and the JOB-14 Schedule stay with RWB-P7-E1008-APP, and this story registers the transfer acceptance and the version in force only. The element shapes of DecisionLogPage and DecisionLogEntry are the field names of TSD P7 v2 T3.1; their required fields are Not specified in the source documents (GAP-2500). The page size of the decision-log read is service configuration, not a value of this story. The reason code, the rule ID and the package version of a move are held in `decision_log_entry` only; the deviation table holds none of them and this story adds no column to it (GAP-3096).

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-decision` (P7); base `/api/recovery/decision/v1`. The version list is the ownership map's P7 path; the two decision-log paths are API-P7-006 and API-P7-007 of TSD P7 v2 T-A.1 on the service base. The element shape of the answer is Not specified beyond the field names TSD P7 v2 T3.1 gives (GAP-2500; ASM-4133).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/admin/rule-packages/{packageCode}/versions` | List the versions of TRANSFER with status, valid-from and valid-to dates, so a caller names the version in force on a business date; 200, or MSG-P3-027 when none is in force for the date asked | Rules and parameters R | Not applicable, read only |
| GET | `/decision-log` | Read the decision entries by caseId, decision, ruleId, approver, from, to, page and size; 200 with the page, scope applied | Decision log R, scope applied | Not applicable, read only |
| GET | `/decision-log/{entryId}` | Read one entry with its inputs reference, decision code, rule ID, rule version, actor, final call, actions, outcome, decided time, chain sequence, previous hash and entry hash; 200 | Decision log R, scope applied | Not applicable, read only |

Errors: 401 no session (MSG-P4-001); 403 no Decision log R or outside the scope (MSG-P4-002); 404 an unknown package code or entry (message ID Not specified in the source documents (CG-ALL-7134)); 422 or 200 with MSG-P3-027 when no version is in force on the date asked, the exact status being Not specified in the source documents (GAP-2500; ASM-4133); 503 the ledger is unavailable (MSG-P7-003). Every error is an RFC 9457 problem response with `messageId`, `detail`, `instance` and `traceId`. No operation writes an entry: the record arrives on the topic of 12.4.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access, on RWB-P4-E1037-CON | The caller's role, scope and Decision log right behind every read of 12.1; faked, one hop, 2 s (DP-11) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case, on RWB-P3-E1043-CON | LOV-DECISION and the version-state list with the version in force (DP-07); faked |

The record of a move makes no call into this service and this service makes no call into rwb-case for it: the record arrives on `rwb.decision-record.v1` and its element shape is fixed by RWB-P3-E2012-CON, which this story builds against and fakes (12.8). The platform contracts the DP table adds are listed in section 13 and carried in GAP-2501.

#### 12.3 Events published

None. This story publishes no event of its own: it seals a record that another service already published, and the chain check of RWB-P7-E1008-APP owns the break report. `rwb.decision.RulePackageInForce.v1` belongs to the registry stories and this story only reads the state it announces.

#### 12.4 Events consumed

| Event | Topic | Owner | Key | Payload used |
|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 ledger library, published by the owning service | caseId | the whole record: entry id, decision code, final call `CASE_TRANSFERRED`, rule ID, rule version, case id, inputs reference, from and to queue and owner, reason code, actor, decided time, idempotency key |

Filtered on `source` so this service does not re-ingest its own records; deduped on the inbox key; retried and then quarantined on `rwb-decision.dlt` (DP-09). No payload carries a name, an e-mail address, a mobile number, a national identity number or an account number.

#### 12.5 Workflows and activities

None of this story's own. The ingest is the event-started consumer of RWB-P7-E1008-APP and the chain check is the `DecisionChainCheckWorkflow` of that story on the `rwb-decision` queue; this story adds no workflow, no activity and no timer, and the manual move's `ManualTransferWorkflow` runs on the `rwb-case` queue and is RWB-P3-E2012-APP's (DP-10; ASM-4135).

#### 12.6 Schedules

| Schedule | When | Mechanism | Owner and this story's part |
|---|---|---|---|
| JOB-14 chain check | 02:00 | A Temporal Schedule on the `rwb-decision` queue that verifies the chain from `chain_seq` 1 to the last entry, writes the daily seal and reports a break to Compliance the same day (FSD P7 AC-BG-P7-007-01; NFR-035; DP-10) | P7 rwb-decision, created by RWB-P7-E1008-APP. This story adds no Schedule and asserts the coverage of its entries in AC8 (ASM-4135) |

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `decision_log_entry` | P7 (`rwb_decision`) | One append-only, hash-chained entry per move, with the rule ID and the TRANSFER version; read by the two operations of 12.1 |
| `rule_package` | P7 (`rwb_decision`) | The TRANSFER package row: code, title, owner role |
| `rule_package_version` | P7 (`rwb_decision`) | "TRF-2026.12" at IN_FORCE from 2026-12-01, "TRF-2026.11" at SUPERSEDED, and the answer when none is in force |
| `rule_row`, `rule_test_case` | P7 (`rwb_decision`) | Not used: the rule ID and version arrive on the record and this story evaluates nothing |
| `processed_event`, `outbox_event`, `idempotency_key` | PLT library, created in `rwb_decision` | Inbox dedupe, outbox and the stored envelope of the ingest |

Not owned and not read: `recovery_case`, `assignment`, `queue` and `queue_member` (P3), `deviation` (S8), `approval` (P7, not used: no approval level applies). No foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case transfer fake | RWB-P3-E2012-CON | The record of "RW-2026-000401" from MTG-BKK-CO/U-CO-01 to LIT-BKK-01/U-LO-02, reason R02, rule TRF-010, version TRF-2026.12, actor U-TM-01, decided 2026-12-15T10:12:00Z; the ten records of one selection; a record with an empty rule version; a record with decision code D99; a record of 2026-12-20 naming TRF-2026.11 |
| rwb-access fake | RWB-P4-E1037-CON | `GET /me/session` for RW-AUDIT, RW-TEAMMGR and RW-CASEOWN with Decision log R, a role without it refused with MSG-P4-002, and a caller of another scope |
| rwb-case reference-data fake | RWB-P3-E1043-CON | LOV-DECISION and the version-state list with their versions |
| decision-record library fake | RWB-PLT-E1027-CON | The append, the hash chain, the inbox key, a redelivery and a forced failure for the quarantine case |
| ledger fake | RWB-P7-E1008-APP | The chain append and the JOB-14 verifier with a clean chain and one altered canonical form |

Each fake is replaced by the real contract or the real component as its story lands, without a change to the scenarios. The fakes carry synthetic case IDs, queue codes, user references and reason codes only.

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 3, consumed 2 | The version list, the decision-log page and one entry provided; the session read and the reference list consumed, one hop and 2 s |
| Kafka | Published 0, consumed 1 event type | `rwb.decision.DecisionRecorded.v1` on the shared topic `rwb.decision-record.v1`, through the inbox; the `.dlt` of the service on a refused record |
| Temporal | None of its own | The ingest is event-started and the chain check is the shared JOB-14 Schedule (DP-10) |
| File | None | No file is read or written; the seal of the chain check is RWB-P7-E1008-APP's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `ledger/transfer`, Java package `th.co.scb.ace.workbench.recovery.decision.ledger.transfer`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-APP |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

How each row is applied. **DP-01**: the entry and the two registry tables are `rwb_decision` rows; the case, the assignment and the queue are never read, they arrive as the record's actions. **DP-03**: the record is consumed from `rwb.decision-record.v1` and sealed with the local library, so the ledger is the second copy and never the only one. **DP-04**: the kit stays in `rwb-case` where the move is decided; this story reads only the version in force, and the C dependency RWB-P7-E1073-APP is this service's own authoring pipeline, built against its published set. **DP-05**: no ACE view is read; the transfer facts reach this story only as the record. **DP-07**: LOV-DECISION and the version-state list are read with their version; the decision code is never a constant (BR9). **DP-09**: the inbox key makes one record one entry, the outbox of the move is `rwb-case`'s, and the `.dlt` of this service holds the refused envelope. **DP-10**: the JOB-14 chain check is the Schedule of 12.6 and this story creates no workflow and no Schedule. **DP-11**: the two consumed operations are one hop with a 2 s timeout and a breaker. **DP-13**: every path of section 12 uses `/api/recovery/decision/v1`. **DP-14**: the topic is the shared `rwb.decision-record.v1` and the event is `rwb.decision.DecisionRecorded.v1`; no `rwb.p7.` or `rwb.casewf.` name survives. **DP-15**: the two indexes of this story go into the per-service Flyway sequence of `rwb_decision`, after the baseline of RWB-P7-E1008-APP. **DP-19**: no screen is built; SCR-05 is composed by gateway-bff from `rwb-case` and this story serves the read behind an audit view of the case. The composite route path, its merge order, the harness repository and environment, the test-data seeding, the evidence format and retention and the pass/fail gate are Not specified in the source documents (GAP-0396); none is set here.

The platform H dependencies of the table — DP-03, DP-04, DP-07, DP-09, DP-10, DP-14, DP-15 and DP-19 — and the C dependencies C RWB-P7-E1073-APP and C RWB-P3-E1043-CON are not in the metadata rows, which name None and RWB-P3-E2012-CON. They are recorded in GAP-2501 and ASM-4134: all are wave 0 platform contracts or published contracts, none blocks the build, and an APP story builds against the published set and its fake.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TransferRecordConsumer | Consumer | Reads `rwb.decision-record.v1`, filters on `source` and the decision code, dedupes on the inbox key |
| TransferRecordValidator | Service | Checks the record against the element of RWB-P3-E2012-CON: decision code, final call, rule ID and version, reason code, actor, decided time, from and to side; refuses with MSG-P7-009 and quarantines |
| VersionInForceService | Service | Resolves the TRANSFER version in force on the record's business date; refuses a record naming another version and never defaults |
| TransferLedgerWriter | Service | Appends the entry through the chain of RWB-P7-E1008-APP in one transaction with the inbox key |
| RuleVersionReadController | Controller | `GET /admin/rule-packages/{packageCode}/versions` with the guard, the scope and the problem mapping |
| DecisionLogController | Controller | `GET /decision-log` and `GET /decision-log/{entryId}` with the scope and the hashes |
| DecisionLogQueryRepository | Repository | The paged read of `decision_log_entry` by case, decision, rule, approver and date range |
| RuleVersionRepository | Repository | The `rule_package` and `rule_package_version` reads of the version in force |
| SessionClient, ReferenceListClient | Clients | The two consumed operations of 12.2, one hop with a 2 s timeout and a breaker |
| TransferRecordFakeAdapter, ChainFakeAdapter | Test adapter | The rwb-case transfer fake and the ledger fake of 12.8 |

**Database and migrations.** One migration in the per-service Flyway sequence of DP-15, `V2027_3__decision_transfer_ledger.sql`, adds the unique index `ux_decision_log_idempotency` on `decision_log_entry (idempotency_key) WHERE idempotency_key IS NOT NULL`, so a redelivery cannot write a second entry even if the inbox loses its key, and the read index `ix_decision_log_case_decided` on `(case_id, decided_at)`. It adds no column and writes no seed row. The TRANSFER package row and its two version rows are written by the registry stories; where they have not landed, this story's seed registers "TRF-2026.12" from 2026-12-01 and "TRF-2026.11" before it under the label check of ASM-4137. Append only is enforced by the trigger of RWB-P7-E1008-APP; this story adds none.

**Configuration and reference data.** No business parameter is read (DP-06 is not claimed). LOV-DECISION and the version-state list are read with their version in force. The version labels, dates and rule IDs are the legacy values: "TRF-2026.12" in force from 2026-12-01, "TRF-2026.11" before it, row "TRF-010" refusing while a deviation is open. The reason codes are `rwb-case` reference data and this story stores the code it receives without validating it against the list. `ledger.transfer.page-size-max` is a read guard for the pager and Not specified in the source documents (GAP-2500; ASM-4133).

**Build steps**

1. `TransferLedgerWriter` against the chain of RWB-P7-E1008-APP and the migration's unique index; tests AC1 and AC2.
2. `TransferRecordValidator` with the six checks and MSG-P7-009 naming the field; tests AC5 and X1, X2.
3. `VersionInForceService` over `rule_package_version` and the refusal of a version not in force on the date; tests AC6, AC7 and X3.
4. `DecisionLogQueryRepository` and the two reads with the pager, the scope and the hashes; tests AC3, AC4 and AC9.
5. The consumer with the inbox key, the `source` filter, the retry policy and the `.dlt` path with its incident; tests AC2 and X5.
6. The JOB-14 assertion against the ledger fake with a clean chain and one altered canonical form; test AC8.
7. The privacy test: every entry, answer and envelope holds IDs, codes, rule IDs, version labels and dates only.
8. The contract tests of the two consumed operations against their fakes, with a 2 s budget and a breaker.

**Feature switch.** No flag of its own. The move stays behind `rwb.p3.manual-transfer`, which is `rwb-case`'s (RWB-P3-E2012-APP), and the ingest stays behind the platform ingest switch of RWB-P7-E1008-APP. With the move switched off, this story receives no record and its reads stay available.

**Done when.** The tests in section 16 pass; in SIT a move of "RW-2026-000401" appears once in the ledger with `TRF-010` and "TRF-2026.12", a redelivery writes nothing, a record naming "TRF-2026.11" on 2026-12-20 is refused and quarantined, the version list names "TRF-2026.12" as in force on 2026-12-15 and none on 2026-12-20, and the JOB-14 run verifies the chain end to end.

**Platform pickup gate.** The eight platform H rows of the DP table are tracked here: RWB-PLT-E1027-CON (DP-03), RWB-PLT-E1072-CON (DP-04), RWB-PLT-E1043-CON (DP-07), RWB-PLT-TE006-CON (DP-09), RWB-PLT-E1071-CON (DP-10), RWB-PLT-E1047-CON (DP-14), RWB-PLT-E1044-CON (DP-15) and RWB-PLT-N001-CON (DP-19). The pickup gate for these contracts is Not specified in the source documents (GAP-3091). Depends on (build) stays None and Ready to start stays Day 1 (GAP-3091).

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P7-009 | A record is missing the decision code, the rule version, the reason code, the actor or the decided time, or its decision code is not in the list, or its rule version was not in force on its business date | Not specified in the source documents (GAP-2500; ASM-4133) | This story, on the ingest |
| MSG-P7-003 | The ledger write fails | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on the ingest and the reads |
| MSG-P3-027 | No TRANSFER version is in force on the business date asked | The rule version was refused at the {check} check: {detail}. | This story, on the version list |
| MSG-P4-002 | The role holds no Decision log R, or the entry is outside the scope | You cannot {action} here. Your role does not include it. | This story, through the session read |
| MSG-P4-001 | No session, or no Recovery Workbench role | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. | This story, on every read |

For MSG-P7-009 the field named is `decisionCode`, `ruleVersion`, `reasonCode`, `actor` or `decidedAt`, and the case ID is logged with the missing field and nothing else; its text is named by FSD P7 AC-ALT-P7-002-01 and AC-EXC-P7-002-01 and written out in no source this story may read, so the placeholder stands. For MSG-P3-027 {check} is "package in force" and {detail} names the package code TRANSFER and the business date only. The legacy message of the move itself, MSG-P3-033 with the refusing rule ID, stays with RWB-P3-E2012-APP and is not produced here. Thai text follows DL10 (open; assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863). Open decision DL23 is still open; its assumptions are ASM-1232, ASM-1237, ASM-1259 and ASM-1560.

### 15. Screens and states

No screen is built in this story. SCR-05 Transfer case is `rwb-case`'s and is composed by the gateway-bff route of DP-19 (RWB-P3-E2012-APP); SCR-07 Team queues and SCR-09 Exception queue are unchanged. What this story gives a screen is the read of the record behind the case timeline and the audit view.

| Where | State | What the caller sees |
|---|---|---|
| The version list | IN_FORCE | The TRANSFER version, its valid-from date and the version it superseded |
| The version list | SUPERSEDED | The version, its date range and the version that replaced it |
| The version list | No version in force | MSG-P3-027 naming the package and the business date; no version is offered as a default |
| The case audit view | Read | The entry of a move with its rule ID, version, reason code, from and to queue and owner, actor and decided time |
| The entry read | Read | The same entry with `inputsRef`, `actions`, `outcome`, `prevHash`, `entryHash` and `chainSeq` |
| SCR-05 Transfer case | Saved, Refused | The move's own states, from `rwb-case`; the record is written behind them and never waits on this story |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-012-01 | AC1, BR1, BR2, BR4 | Component | Record of RW-2026-000401 to LIT-BKK-01, reason R02, rule TRF-010, version TRF-2026.12 |
| TC-E2-012-02 | AC2, BR5, BR10 | Component | Record of RW-2026-000402 naming rule TRF-010 under version TRF-2026.12 |
| TC-E2-012-03 | AC3, BR4, BR5 | Component | Ten records of one selection, each with its own rule ID and version |
| TC-E2-012-04 | AC4, BR3 | Component | Record with no reason code and record with no decision code |
| TC-E2-012-05 | AC5, BR2 | Component | Record of a reassignment to U-CO-04 with reason R01 |
| TC-E2-012-06 | AC6, BR5 | Contract | Record naming rule R-UNI-18 under version TRF-2026.12; TRANSFER versions TRF-2026.11 and TRF-2026.12 |
| TC-E2-012-07 | AC7, BR3 | Component | Record of RW-2026-000403 under a legal hold, with reason R05 |
| TC-E2-012-08 | AC8, BR4 | Component | Two envelopes of one record in the same second |
| TC-E2-012-09 | AC9, BR6 | Component | Same envelope and inbox key twice |
| TC-E2-012-10 | AC10, BR7 | NFR | Ledger write forced to fail; no entry, no chain gap, envelope quarantined |
| TC-E2-012-11 | AC11, BR4 | Component | Eight sealed records and two refused records of one selection |
| TC-E2-012-12 | AC12, BR2 | Component | Record of a queue transfer to LIT-BKK-01 with reason R05 |
| TC-E2-012-13 | Access | Contract | RW-CASEOWN reads the decision log; a role with no Decision log right refused with MSG-P4-002 |
| TC-E2-012-14 | Principle 5 | NFR | Ledger unavailable; case, assignment and outbox of the move unchanged, incident raised |
| TC-E2-012-15 | AC6, BR5 | Contract | No TRANSFER version in force on 2026-12-20; MSG-P3-027 and no default |
| TC-E2-012-16 | AC4 | Component | Paged read of decision_log_entry by case, decision, rule, approver and date range |
| TC-E2-012-17 | AC7 | Component | Record naming TRF-2026.11 on 2026-12-20 refused and quarantined |
| TC-E2-012-18 | AC8 | Component | JOB-14 check against the ledger fake: clean chain passes; one altered canonical form fails |
| TC-E2-012-19 | AC9 | Component | Decision log read returns the scope and the hashes |
| TC-E2-012-20 | Tables of 12.7 (ASM-3438) | Component | Boundary rows of decision_log_entry, rule_package and rule_package_version; bound values Not specified in the source documents (ASM-3438) |
| TC-E2-012-21 | AC4 of this story | Component | Sealed move of AC1 read by entryId; the answer holds the fields of AC4 and no personal data |
| TC-E2-012-22 | AC7 of this story | Component | Move of AC1 sealed under TRF-2026.12, version rolled back to TRF-2026.11; move of 2026-11-30 sealed under TRF-2026.11 |
| TC-E2-012-23 | AC8 of this story, BR8 | Component | Twenty transfer entries from chain_seq 1; JOB-14 at 02:00 passes; one altered canonical form fails and is reported to Compliance |
| TC-E2-012-24 | AC9 of this story, BR11 | Contract | RW-CASEOWN read 200; role with no Decision log right refused with MSG-P4-002; no session refused with MSG-P4-001 |
| TC-E2-012-25 | BR9 | Component | Move decision code read from LOV-DECISION; version states read as reference data with the version in force |
| TC-E2-012-26 | AC10 of this story, BR9 | Component | Move of AC1 sealed; decision code read from LOV-DECISION; version states read as reference data with the version in force |
| TC-E2-012-27 | AC11 of this story | Component | Entry ID held by no decision_log_entry read by entryId; answer 404 |
| TC-E2-012-28 | AC12 of this story | NFR | rwb-access contract does not answer the Decision log right check; read refused and incident raised |

The Covers column keeps the legacy criterion and rule labels of RWB-E2-012 that each case was written for — the ACn and BRn of the legacy story, not the numbers of sections 7 and 8 of this story — and the Data column keeps the legacy data. The P7 copy of each case proves the ledger half: the sealed entry and the hash chain for the move cases, the refusal and the quarantine for the invalid-record cases, the version in force for the version cases and the right for the access case. The move, the cap, the deviation and the screen are RWB-P3-E2012-APP's, RWB-S8-E2012-APP's and the P4 stories'; the `-ITG` copies of all fifteen cases belong to RWB-ITG-E2012-ITG. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the legacy level System maps to Component or Contract here, Access to Contract and Resilience to NFR.

### 17. Guardrails

- No business value in code: the decision code, the version states and the reason codes are reference and registry data; the version labels and dates are rows, not constants.
- No personal data in events, entries, logs, tests or prompts: the record and the entry carry case IDs, queue and team codes, user references, rule IDs, version labels and reason codes only.
- No read of another service's tables and no other service reads `rwb_decision` (DP-01): the case and assignment facts arrive as the record, and the session and the lists arrive on their operations.
- Append only, hash chained: no code path updates or deletes an entry, and the daily run reports a break instead of repairing it.
- One record, one entry: the inbox key and the unique index both refuse a second write, so a redelivery can never fork the chain.
- No second rule engine: this story evaluates no package and reads no workbook, `drl_source` or `rule_row`; the rule ID and version are read from the record.
- A version is never defaulted: no version in force is a refusal with the package code and the date, never a fallback to the latest row.
- No secret in the run material: the rwb-decision login (DP-02) and the certificate come from the platform secret store, and the test data is synthetic.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-003 | Manual transfer or reassignment only with a reason code from the agreed list — the reason code is sealed on the record here | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-03 | All recovery processes | R-DEV-02, R-UNI-20, R-UNI-39, R-UNI-40 | TC-E2-012-01, TC-E2-012-02, TC-E2-012-04, TC-E2-012-07 to TC-E2-012-10, TC-E2-012-13 to TC-E2-012-15 |
| REQ-WKM-007 | An absent or over-cap owner's cases reallocated inside the team, keeping state and clocks — the reallocation is recorded here | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-04, FEAT-WKM-10 | All recovery processes | R-UNI-18, R-UNI-46 | TC-E2-012-03, TC-E2-012-05, TC-E2-012-06, TC-E2-012-11, TC-E2-012-12 |
| REQ-WKM-008 | Queue and transfer history visible on the case — the transfer entry read here is its source | Business Requirements Epic 2, section 4; Program, section 5.3 | FEAT-WKM-03 | All recovery processes | R-UNI-18 | TC-E2-012-01, TC-E2-012-03 |
| REQ-CWC-010 | A manual move is decided by the TRANSFER rules and a refused move is not made — cited by legacy BR1 and BR2; its text is in the Epic 2 BRD and not copied in the legacy story (GAP-2500; ASM-4133) | Business Requirements Epic 2, section 3.3 | FEAT-WKM-03 | All recovery processes | R-DEV-02, R-DEV-03 | TC-E2-012-02, TC-E2-012-06, TC-E2-012-15 |
| REQ-CWC-016 | The rule ID and the package version are on the decision record | Business Requirements Epic 2, section 4 | FEAT-WKM-03 | All recovery processes | R-UNI-38 | TC-E2-012-01, TC-E2-012-03, TC-E2-012-06 |

- ADR-022 and D-RCV-36 T3, T5 and T7: a local record per decision plus a central ledger, and a decision that keeps the rule version it was taken under.
- D-RCV-60: the realignment that splits RWB-E2-012 into the P3, S8, P4, P7 and ITG stories; the P7 slice is this story.
- RWB-P7-E1008-APP and RWB-P7-E1021-APP: the ledger and the TRANSFER registry this story uses and does not rebuild.
- NFR-033, NFR-034 and NFR-035: every decision reproducible, the rule version on every action, and the daily chain check (TSD P7 v2 T7).

### 19. Out of scope

- The screen SCR-05, the transfer operation, the caps, the assignment swap and `rwb.case.CaseTransferred.v1` (RWB-P3-E2012-APP, P3); the open-deviation read and the X1 screening (RWB-S8-E2012-APP, S8).
- The session, the roles, the rights, the delegation of authority and the reason list (the P4 stories; RWB-P3-E1043-CON).
- The ledger machinery itself — the ingest pipeline, the single hash chain, the daily seal, the append-only trigger and the JOB-14 Schedule (RWB-P7-E1008-APP); the retention of entries (RWB-P7-E1017-APP).
- The TRANSFER package's rows, its authoring, its test cases, its four-eyes approval, its promotion at 00:01 and its rollback (RWB-P7-E1073-APP, RWB-P7-E1021-APP, RWB-P7-E2042-APP).
- The evaluation of the TRANSFER package, the assignment engine and the rule-driven transfers on stage change, route decision and timer expiry (RWB-P3-E1021-APP, RWB-P3-E1020-APP).
- Automatic reallocation when an owner is absent or over the cap (R-UNI-18, R-UNI-19, JOB-06) and the queue history view on the case (RWB-E2-016).
- Partner placement and recall (Epic 6) and the transfer decision of a route approval (RWB-P7-E2013-APP).
- The real cross-service proof of the move, its record and its entry across the four services (RWB-ITG-E2012-ITG).
