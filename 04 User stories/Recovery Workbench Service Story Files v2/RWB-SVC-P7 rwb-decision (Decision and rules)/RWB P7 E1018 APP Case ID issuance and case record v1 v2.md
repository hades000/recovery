# RWB-P7-E1018-APP Case ID issuance and case record v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: the rwb-decision slice of RWB-E1-018, holding the case-creation profile of the central decision ledger, its refusals, its one read and the registry check that the cited ENTRY version is held, split out of the case creation that stays with rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P7-E1018-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 29 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P7-E1018-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Database login | The rwb-decision login is named in RWB-PLT-DB; the name is Not specified in the source documents (GAP-2438) |
| Service epic | RWB-SVC-P7 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P7-F |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P7-E1018-APP-16); the squad sizes it at refinement; whether it fits two weeks is Not specified in the source documents (DOR-RWB-P7-E1018-APP-15) |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E1018-CON (the contract this story depends on; no contract story is created under a new story key) |
| Contract fake library version | Not specified in the source documents (DOR-RWB-P7-E1018-APP-22) |
| Contract version built against | Not specified in the source documents (DOR-RWB-P7-E1018-APP-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to REQ-CWC-001, REQ-CWC-002, REQ-CWC-003, REQ-CWC-004, REQ-CWC-005, REQ-CWC-016, REQ-CHO-004) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **risk and model risk officer (RW-RISK), an internal audit reader (RW-AUDIT) and the ledger ingest of rwb-decision**, I want **every case creation of rwb-case sealed once in the central decision ledger of rwb-decision as an append-only, hash-chained entry that names the ENTER rule ID, the ENTRY version label in force on the ALS business date and the case reference, accepted only when the registry holds that version and answered for one case as the evidence of why the case exists**, so that **no case can stand in the book without a recorded basis that can be replayed, and that basis is read in one place**.

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1`, event names `rwb.decision.<Event>.v1`, Temporal task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`, and the shared record topic `rwb.decision-record.v1` (DP-03, DP-13, DP-14).
- The deliverable, and nothing else: `CaseCreationRecordProfile`, the profile that decides whether a `DecisionRecorded` record of a case creation may enter the ledger. It requires decision code "D6" and final call "CASE_CREATED", the ENTER rule ID of package ENTRY, a rule version label that `rule_package_version` holds for that package, and an inputs reference that carries the ALS business date.
- The read: the case-creation filter of the ledger query, `GET /api/recovery/decision/v1/decision-log?caseId={caseId}&finalCall=CASE_CREATED`, answering the creation entry with its rule ID, rule version, inputs reference, final call, `decidedAt`, actor, `prevHash`, `entryHash`, `chainSeq` and `chainVerified`, under Decision log R with the caller's scope applied.
- The refusals: a record with the rule ID and no version, or the version and no rule ID, or a version label the registry does not hold for package ENTRY, or a decision code outside LOV-DECISION, is refused with MSG-P7-009 naming the field and nothing is appended; an entry that does not match the chain is answered with `chainVerified` false and the warning MSG-P7-012 while the stored row stays untouched; an unavailable store blocks the case creation with MSG-P7-003.
- What this story does not do: it creates no case, issues no number, groups no account, applies no exclusion, evaluates no rule, authors no package, and owns neither the store baseline nor the writer. Those are section 19.
- The legacy facts are unchanged: one case creation writes one record with its decision code, final call, ENTRY rule ID and package version, in the same transaction as the case (legacy flow step 11 and BR8); a failed record write stops the creation (principle 5, R-UNI-39); a repeated run creates nothing new (legacy AC8); the case links to ACE by business key with no foreign key (legacy BR11, D-RCV-35 U4, ADR-010); a version not in force is never a default decision (legacy BR13, R-UNI-41).

### 2. Business rationale

Why a case was opened, under which rule and on which date is the first question an auditor asks of the recovery book. Legacy RWB-E1-018 made that answer a condition of creating a case: the entry and exclusion outcomes come only from the rules package, and the record is written in the same transaction as the case, so a case without its record does not exist (REQ-CWC-016, legacy BR8). D-RCV-60 keeps the promise and moves its home. Each of the 19 services writes its record locally in its own schema and publishes `DecisionRecorded`; `rwb-decision` collects the records into one central ledger that is chained, searchable and sealed (Arch v5 slides 20 and 28; ADR-022).

A record is worth little if the rule it names cannot be found. The case-creation record cites a rule ID and a version label, and the label must be one the registry actually holds for package ENTRY, because a record that cites a version the registry never had cannot be replayed, and a record that cites no version at all leaves the decision unexplained. That check is this story's reason to exist, and it is the only join this service makes between the ledger and the registry. The record stays a record of what was decided; it never becomes a second rule engine.

1. One entry per case creation, with "D6", "CASE_CREATED", the ENTER rule ID, the version label and the ALS business date (BR1, BR7).
2. A version label that the registry does not hold is a refusal, never a default and never a guess (BR4, BR11).
3. The basis of a case, read back for one case only and only by a role that may see it (BR5, BR9, BR12).

This is the rwb-decision part of legacy RWB-E1-018. Case creation, grouping, the yearly number, the entry and exclusion evaluation and the case state stay with rwb-case (RWB-P3-E1018-APP); the ACE view read stays with rwb-source-data (RWB-P1-E1018-APP); the access decision stays with rwb-access (RWB-P4-E1018-APP); the document binding stays with rwb-document (RWB-P5-E1018-APP); the store, the writer, the audit query and the registry are the other stories of this service (section 3). It meets REQ-CWC-016 and supports REQ-CWC-001 to REQ-CWC-005 and REQ-CHO-004, and it serves NFR-033 (every decision reproducible), NFR-034 (every action carries the rule version applied) and NFR-035 (the chain checked and a break reported).

### 3. Preconditions

- The W1J01 harness fixture for the ALS batch and the exact synthetic case set are Not specified in the source documents (GAP-0343).

- RWB-P7-E1008-APP delivers the `decision_log_entry` baseline in `rwb_decision`, the append-only trigger, the grants, the single hash chain, the continuous ingest of `rwb.decision-record.v1` and the JOB-14 chain check at 02:00 (DP-03, DP-10). This story adds a profile to that ingest and rebuilds none of it.
- RWB-P7-E1027-APP and RWB-PLT-E1027-CON supply the writer, the record shape, the canonical form, the SHA-256 and the chain append that a case creation uses (DP-03, DP-09); this story validates the record a case creation carries and never writes a second record type.
- RWB-P7-E1073-APP holds the registry: version "ENTRY-2026.11" of package ENTRY and version "EXCL-2026.11" of package EXCLUSION are approved and in force from 2026-11-30 (legacy precondition RWB-E1-073). The load, the checks, the four-eyes approval, JOB-20 and the rollback are that story's; this story reads `rule_package`, `rule_package_version` and `rule_row` in its own schema to answer whether a cited label is held.
- RWB-PLT-E1043-CON and RWB-P3-E1043-CON are published: LOV-DECISION with the value "D6" and its version in force, read through DP-07; no decision code is a constant of this service's code.
- RWB-PLT-TE006-CON supplies the outbox and inbox library (DP-09), RWB-PLT-E1047-CON the naming library (DP-14), RWB-PLT-E1044-CON the Flyway sequence (DP-15) and RWB-PLT-N001-CON the gateway-bff composite route behind SCR-38 (DP-19).
- RWB-P3-E1018-CON is published and defines the case ID value that the record cites. This story calls no rwb-case operation at run time: the case reference arrives inside the record, and its synthetic values come from the contract fake of 12.8.
- The synthetic facts are the legacy story's own: case `RW-2026-000123` for borrower `P-0101` with account `A-5001`, the ALS business date 2026-12-01, the last number issued `RW-2026-000122`, account `A-5002` at 92 days past due with `tdr_flag` true and reason "ACTIVE_PLAN" under rule ID "EXCL-004", account `A-5005` with `dispute_open` true under rule ID "EXCL-006". Readers hold Decision log R (TSD P7 T6.1); the scope decision is the cached permission decision the service template holds from rwb-access; the `rwb-decision` service identity and the per-service login of DP-02 sit in the platform secret store, and the login's own name is Not specified in the source documents (GAP-2438; ASM-4010).

### 4. Flow

1. rwb-case creates a case and, as the last step before commit, writes its local decision record with decision code "D6", final call "CASE_CREATED", the ENTER rule ID of package ENTRY, version "ENTRY-2026.11", the case reference and an inputs reference naming the ALS business date 2026-12-01, and publishes `DecisionRecorded` (EV-08) on `rwb.decision-record.v1` (legacy flow step 11 and BR8; DP-03, DP-09).
2. The ingest of RWB-P7-E1008-APP consumes the event and holds its event ID in the inbox as the idempotency key. A record whose event ID is already held appends nothing, answers the first entry ID and moves the repeat count by one (R-UNI-40).
3. `CaseCreationRecordProfile` reads the record and checks the five facts of the profile: decision code "D6" against LOV-DECISION through DP-07, final call "CASE_CREATED", the rule ID present with its version label, the label held by `rule_package_version` for package ENTRY, and the inputs reference carrying a business date.
4. A record that fails a check is refused with MSG-P7-009 naming the field, nothing is appended, `chain_seq` is not used, and the refusal is logged against the case reference and the field with no rule value in the log.
5. A record that passes is handed to the appender of RWB-P7-E1008-APP, which seals one row with the case reference, "D6", "CASE_CREATED", the rule ID, "ENTRY-2026.11", the inputs reference, `decided_at`, the producing service identity in `actor_user_id`, the event ID in `idempotency_key`, `prev_hash`, `entry_hash` and `chain_seq` (BR5).
6. No case attribute is copied and no `rwb_case` table is read: the case reference `RW-2026-000123` is an indexed business key with no foreign key (DP-01). The append publishes no event, because the ledger is the seal (BR6).
7. An audit reader with Decision log R opens SCR-38 Decision log query or the decision list of a case and calls `GET /api/recovery/decision/v1/decision-log?caseId=RW-2026-000123&finalCall=CASE_CREATED`. The answer carries the creation entry with its rule ID, rule version, inputs reference, final call, `decidedAt`, actor, hashes, `chainSeq` and `chainVerified`.
8. The read recomputes the hash of the answered entry and compares `prev_hash` with the entry before it. A mismatch answers `chainVerified` false with the warning MSG-P7-012 naming the `chainSeq` and raises one incident to the Compliance queue; the row is never rewritten, renumbered or deleted (BR8).
9. A store that cannot be appended or read blocks the caller: nothing is committed, no entry is invented, MSG-P7-003 is answered, and the record waits in the outbox of rwb-case until the store answers (BR10).
10. While `v_ace_batch_status` does not exist, the answer to an entry read for a date whose batch record does not exist yet is Not specified in the source documents (GAP-0574). The gate is read from the view only and is never inferred from `data_as_of`, a row count or a file.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A record carries the ENTER rule ID with an empty version label, or a version label with no rule ID | Refused before any append; nothing is written and `chain_seq` is not used | MSG-P7-009 naming "ruleVersion" or "ruleId" | AC2 |
| X2 | A record cites a version label that `rule_package_version` does not hold for package ENTRY, for example "ENTRY-2026.12" before it is loaded | Refused; no default and no earlier label is put in its place; the refusal is logged against the case reference, the package code and the label | MSG-P7-009 | AC3 |
| X3 | A record carries a decision code outside LOV-DECISION, for example "D99" | Refused with the field named; nothing is appended | MSG-P7-009 | AC2 |
| X4 | The same event ID arrives again | One entry; the repeat answers the first entry ID and moves the repeat count by one | None | AC4 |
| X5 | An entry does not match the chain, because it was changed with the append trigger disabled | `chainVerified` false, the MSG-P7-012 warning naming the `chainSeq`, one incident to Compliance, and the stored row untouched | MSG-P7-012 | AC7 |
| X6 | The caller's role holds no Decision log R, or the case sits outside the caller's scope | 403 with no case attribute in the answer; the stored entry is unchanged | MSG-P4-002 or MSG-P4-003 | AC5 |
| X7 | The ledger store is unavailable for the append or the read | Nothing is committed and no entry is invented; the record waits in the outbox of rwb-case | MSG-P7-003 | AC6 |

X6 is the refusal of the read, not of the record: the entry stays in the ledger for a reader who holds the scope, and no entry is deleted to satisfy a scope. A correction is a new entry naming the one it corrects, never an update; the store's rules for that belong to RWB-P7-E1008-APP.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the `rwb_decision` baseline of RWB-P7-E1008-APP and the record shape of RWB-PLT-E1027-CON; it creates no case, issues no number and reads no `rwb_case` table |
| Negotiable | The decision code, the final call, the version labels and the rule IDs are list and registry values; the story fixes the profile, the refusals and the read |
| Valuable | Every case in the book explains itself from one entry, and no entry can cite a rule version the registry never held |
| Estimable | One profile validator, one controller filter, one chain check on the answer, one registry-hold repository; it fits one sprint with its tests as a secondary slice of the legacy key |
| Small | Four components and one migration index, with no store, writer or registry of its own |
| Testable | Every criterion in section 7 runs against the topic fixture, the registry fixture and the reference-data fake |

### 7. Acceptance criteria

```gherkin
Feature: Case ID issuance and case record v1 - the case-creation entry of rwb-decision

  Background:
    Given the rwb-case contract mock returns LOV-DECISION with the value "D6" and its version in force
    Given the rwb.decision-record.v1 fixture holds the case-creation record of case "RW-2026-000123" for account "A-5001" and borrower "P-0101" with decision code "D6", final call "CASE_CREATED", the ENTER rule ID of package ENTRY, rule version "ENTRY-2026.11" and the ALS business date 2026-12-01
    Given the rwb-decision registry fixture holds "ENTRY-2026.11" of package ENTRY in force from 2026-11-30
    Given the caller holds Decision log R in scope for case "RW-2026-000123"

  Scenario: AC1 One sealed entry per case creation, read back as the basis of the case (new, D-RCV-60)
    Given the last case number issued in 2026 is RW-2026-000122
    When the record is consumed and the caller reads GET /api/recovery/decision/v1/decision-log?caseId=RW-2026-000123&finalCall=CASE_CREATED
    Then exactly one decision_log_entry row exists for case reference "RW-2026-000123" with decision code "D6" and final call "CASE_CREATED"
    Then the entry carries the ENTER rule ID of package ENTRY, rule version "ENTRY-2026.11", an inputs reference naming the ALS business date 2026-12-01, decided_at, the producing service identity in actor_user_id, prev_hash, entry_hash and chain_seq
    Then the entry holds no product group, no owner, no queue, no status, no stage, no case number and no account balance
    Then rwb_decision holds no foreign key to rwb_case and the ingest read no rwb_case table
    Then the answer is 200 with chainVerified true and the rule version "ENTRY-2026.11" on the entry

  Scenario: AC2 A record with half a rule reference, or a code outside the list, is refused (new, D-RCV-60)
    Given the fixture holds a record for case "RW-2026-000124" with final call "CASE_CREATED", the ENTER rule ID and no version label
    When the record is consumed
    Then it is refused with MSG-P7-009 naming "ruleVersion" and no chain_seq is used
    Given the rwb-case contract mock returns LOV-DECISION without the value "D99" and the fixture holds a record for case "RW-2026-000124" with decision code "D99"
    When the record is consumed
    Then it is refused with MSG-P7-009 naming "decisionCode", nothing is appended to the chain and the refusal is logged with the case reference and the field
    Then the case-creation read returns no entry for case "RW-2026-000124"

  Scenario: AC3 A version label the registry does not hold is refused, never defaulted (new, D-RCV-60)
    Given the fixture holds a record for case "RW-2026-000125" citing rule version "ENTRY-2026.12" and the registry holds no version of package ENTRY with that label
    When the record is consumed
    Then it is refused with MSG-P7-009 naming "ruleVersion" and nothing is appended
    Then no default label, no earlier label and no label in force is substituted, and the last chain_seq of the ledger is unchanged
    When the registry later holds "ENTRY-2026.12" and the same record is consumed again
    Then one entry is appended with rule version "ENTRY-2026.12"

  Scenario: AC4 A repeated event gives one entry and the first entry id (new, D-RCV-60)
    Given event "EV-7f3a-0001" for the case creation of "RW-2026-000123" was consumed and one entry was appended
    When the same event with idempotency key "EV-7f3a-0001" arrives again
    Then one entry exists for the case creation, no second row is appended and the last chain_seq of the ledger is unchanged
    Then the ingest answers the first entry's ID and the repeat count of the inbox row is 1

  Scenario: AC5 The read is refused without Decision log R and outside the caller's scope (new, D-RCV-60)
    Given a caller whose role holds no Decision log R
    When the caller reads GET /api/recovery/decision/v1/decision-log?caseId=RW-2026-000123&finalCall=CASE_CREATED
    Then the call is refused with 403 and MSG-P4-002, and no decision code, rule ID, rule version or hash is answered
    Given a caller with Decision log R whose scope excludes case "RW-2026-000126"
    When the caller reads the same query for case "RW-2026-000126"
    Then the call is refused with 403 and MSG-P4-003, and the stored entry of case "RW-2026-000126" is unchanged

  Scenario: AC6 The ledger unavailable blocks the case creation and never loses the record (new, D-RCV-60)
    Given the decision log store is unavailable
    When rwb-case creates case "RW-2026-000123" and publishes its DecisionRecorded event
    Then the record is not appended and the last chain_seq of the ledger is unchanged
    Then the creation is stopped with MSG-P7-003 at the caller, and the record waits in the outbox of rwb-case
    When the store answers again
    Then the record is consumed once and one entry is appended

  Scenario: AC7 An entry that fails the chain is answered with a warning (new, D-RCV-60)
    Given six entries exist for case "RW-2026-000123" and the entry at chain_seq 230 was changed with the append trigger disabled
    When the caller reads the case-creation query for case "RW-2026-000123"
    Then the entry at chain_seq 230 carries chainVerified false and the other five carry chainVerified true
    Then the answer carries the warning MSG-P7-012 naming chain_seq 230 and one incident is raised to the Compliance queue
    Then no entry is updated, deleted, renumbered or rewritten by the read

  Scenario: AC8 The append writes no further record and publishes no event (new, D-RCV-60)
    When the record of case "RW-2026-000123" is consumed and one entry is appended
    Then no row other than the entry is written to any table and no event is published

  Scenario: AC9 A read without a token is answered 401 and a case with no entry is answered 404 (new, D-RCV-60)
    When a caller without a token reads GET /api/recovery/decision/v1/decision-log?caseId=RW-2026-000123&finalCall=CASE_CREATED
    Then the answer is 401 and no entry value is answered
    Given case "RW-2026-000124" holds no entry
    When the caller with Decision log R reads GET /api/recovery/decision/v1/decision-log?caseId=RW-2026-000124&finalCall=CASE_CREATED
    Then the answer is 404 and no entry value is answered
```

The nine criteria are new and test only the deliverable in the title: the case-creation entry of the ledger, its refusals, its repeat rule, its read and its chain answer. The legacy criteria of RWB-E1-018 are owned elsewhere: AC1, AC3, AC4, AC7, AC8, AC11, AC12 and AC15 are created, numbered and held by rwb-case (RWB-P3-E1018-APP); the ACE read behind them is rwb-source-data (RWB-P1-E1018-APP); AC14 is the access decision of rwb-access (RWB-P4-E1018-APP); the document binding is rwb-document (RWB-P5-E1018-APP).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One case creation writes one entry: "D6", "CASE_CREATED", the ENTER rule ID, the version label and the ALS business date; a run that creates no case appends no entry | Legacy flow step 11 and BR8; REQ-CWC-016; FSD P7 AC-P7-002-01 |
| BR2 | The rule ID and its version label travel together; a record with one and not the other is refused with MSG-P7-009 naming the field | FSD P7 AC-EXC-P7-002-01; BR-P7-003 |
| BR3 | The decision code is a value of LOV-DECISION read through DP-07 with the version in force; a code outside the list is refused and no code is a constant of the code | TSD P7 T3.1 DF-DEC-003; FSD P7 AC-EXC-P7-002-05; principle 1 |
| BR4 | The profile accepts a version label only when `rule_package_version` holds it for package ENTRY; a label that is not held is refused, and no default and no label in force is substituted | Legacy BR13; R-UNI-41; Arch v5 slide 27 |
| BR5 | The ledger is append-only and hash-chained: `prev_hash` is the `entry_hash` of the entry before it, the first is 64 zeros, no entry is updated or deleted, and a refused record uses no `chain_seq` | FSD P7 AC-P7-001-01 and AC-ALT-P7-001-01; RWB-P7-E1008-APP |
| BR6 | The append is the seal: it writes no further record and publishes no event | Arch v5 slide 28; ADR-022 |
| BR7 | The entry carries `decided_at`, the producing service identity, and an inputs reference that names the ALS business date; no case attribute is copied | TSD P7 T3.1 DF-DEC-008, DF-DEC-016, DF-DEC-030; legacy flow step 11 |
| BR8 | A repeat of the event ID appends nothing, answers the first entry ID and moves the repeat count by one | Legacy AC8; FSD P7 AC-EXC-P7-002-03; R-UNI-40 |
| BR9 | An entry that does not match the chain is answered with `chainVerified` false and the MSG-P7-012 warning, an incident is raised, and the stored row is untouched | FSD P7 AC-P7-001-01; TSD P7 NFR-035 |
| BR10 | A store that cannot be appended or read blocks the case creation: nothing is committed, no entry is invented, MSG-P7-003 is answered and the record waits in the producer's outbox | Principle 5; FSD P7 VR-P7-001-2 and AC-EXC-P7-001-01 |
| BR11 | The case reference is a business key: no foreign key to `rwb_case`, no case attribute column in `rwb_decision`, no `rwb_case` table read, and a reference with no case row is kept as it arrived | D-RCV-35 U4; ADR-010; legacy BR11; DP-01 |
| BR12 | The read applies Decision log R and the caller's scope before any entry value is answered, and a refusal answers no case attribute | TSD P7 T6.1 and T6.2; legacy AC14 |

How the rules hold: `CaseCreationRecordProfile` executes BR1 to BR4 before any append, reading LOV-DECISION through DP-07 and the registry hold from its own schema, and answering MSG-P7-009 with the field. The appender and the append-only trigger of RWB-P7-E1008-APP execute BR5 and BR7 in one transaction with the next `chain_seq`. BR6 is the shape of the append. BR8 is the inbox row on the event ID. BR9 is `CreationEntryChainCheck` on the answered entry. BR10 is the caller's transaction and its outbox. BR11 is the schema, and BR12 is the controller guard and the scope filter it reads from the template cache.

### 9. State transitions

This story owns no case state and no rule-version state machine; it owns the admission of a case-creation record and the answer for one entry.

| From | Event | Condition | To |
|---|---|---|---|
| (none) | `DecisionRecorded` (EV-08) for a case creation | The record passes the profile and its event ID is new | One `decision_log_entry` row appended at the next `chain_seq` |
| (none) | the same event ID arrives again | The inbox holds the event ID | No row appended; the first entry ID is answered; the repeat count moves by one |
| (none) | half a rule reference, a label the registry does not hold, or a code outside LOV-DECISION | A profile check fails | No row; MSG-P7-009 naming the field; `chain_seq` not used |
| (none) | the store is unavailable | The append or the read cannot run | No row; MSG-P7-003; the producer's outbox retries |

A version state is read here and changed only by the registry stories: a label is acceptable when the registry holds it, and this story makes no state move of its own.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The rwb-decision service identity (the per-service login of DP-02) | Consumes the record, applies the profile, calls the appender and answers the case-creation read; holds no grant on `rwb_case` |
| RW-RISK, RW-AUDIT and every role with Decision log R (RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-LITOFF and the other RW roles of TSD P7 T6.1) | Read the creation entry of a case in scope with its rule ID, rule version, inputs reference, hash and `chainVerified`; the approval of a version is RW-RISK's in RWB-P7-E1073-APP, not here |
| SY-CASEWF, case workflow module | Produces the record of a case creation on its own contract (Decision log C), which this service consumes; it writes no ledger row |
| SY-RULES, Drools evaluator | Evaluates ENTRY and EXCLUSION in rwb-case and stamps the rule ID and version on the record (DP-04); it evaluates nothing in this service |
| The registry owner of RWB-P7-E1073-APP | Holds and moves the version labels the profile tests against; this story reads them and changes none |
| A caller whose role holds no Decision log R | Refused with MSG-P4-002 on the read; the legacy refusal of the case read under Case record R is RWB-P4-E1018-APP's |
| The rwb-access authorise check (DP-08) | Authorises each request to the creation read against Decision log R and the caller's scope before any answer is given |

No person is named anywhere: the actors are roles, service identities and the caller of a contract.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 | decision_log_entry | id | Write |
| DF-DEC-002 | decision_log_entry | case_id (the case reference, a business key) | Write; read; indexed, no foreign key |
| DF-DEC-003, DF-DEC-012 | decision_log_entry | decision_code ("D6", LOV-DECISION), final_call ("CASE_CREATED") | Write; read |
| DF-DEC-004, DF-DEC-005 | decision_log_entry | rule_id (the ENTER rule ID), rule_version ("ENTRY-2026.11") | Write; read |
| DF-DEC-008, DF-DEC-016 | decision_log_entry | inputs_ref (carries the ALS business date 2026-12-01), decided_at | Write; read |
| DF-DEC-017, DF-DEC-018, DF-DEC-028 | decision_log_entry | prev_hash, entry_hash, chain_seq | Write; read |
| DF-DEC-030, DF-DEC-031 | decision_log_entry | actor_user_id (the producing service identity), idempotency_key (the event ID) | Write; read |
| DF-REF-275 | rule_package | package_code ("ENTRY") | Read |
| DF-REF-281, DF-REF-282 | rule_package_version | version_label, status | Read |
| DF-REF-297 | rule_row | drools_rule_name (the rule ID, for example "EXCL-004") | Read, for the label the record cites |

Field IDs are those of the Logical Data Model and Data Dictionary v9 and TSD P7 v2 T3.1. `decision_log_entry` is P7's in `rwb_decision`, and no other service reads it (DP-01). The TSD still models `case_id` as a uuid in a relationship with `recovery_case` and gives the row no business-date column, so in the target the case reference is an indexed business key with no foreign key and the ALS business date travels inside `inputs_ref` (GAP-2435; ASM-4044). `DF-DEC-006` and `DF-DEC-007` stay empty on a case-creation entry: a creation reads no model and no agent. The literal value of the ENTER rule ID of package ENTRY is Not specified in the source documents (GAP-2436; ASM-4045); the entry carries the rule ID the published record carried. No case row, no ACE row and no `v_ace_*` view is read or copied here, and the criteria and test data of this story take the case reference and the ALS business date from the record, never from an ACE view.

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-decision` (P7); base `/api/recovery/decision/v1`. The path is API-P7-006 of TSD P7 v2 T-A.1, which RWB-P7-E2005-APP delivers as the audit query. This story provides the `finalCall=CASE_CREATED` filter on that path and the case-creation profile fields of the answer, and it owns neither the screen nor the export. The filter parameter and the profile field list are Not specified in the source documents (GAP-2434; ASM-4043).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/decision-log?caseId={caseId}&finalCall=CASE_CREATED` | Answer the case-creation entry of one case with `entryId`, `caseRef`, `decisionCode`, `finalCall`, `ruleId`, `ruleVersion`, `inputsRef`, `decidedAt`, `actorUserId`, `prevHash`, `entryHash`, `chainSeq` and `chainVerified`; 200 | Decision log R, scope applied | Not applicable, read only |

Errors: 401 no session; 403 the role lacks Decision log R (MSG-P4-002) or the case is outside the scope (MSG-P4-003); 404 no case-creation entry for the case; 503 the store is unavailable (MSG-P7-003). The answer is a page of `DecisionLogPage` of TSD P7 T-A.2 with the filter applied, and `chainVerified` is added per entry as FSD P3 AC-EXC-P3-037-01 requires. The search by case, rule, approver and date, the saved filters, the export and the audit population read are RWB-P7-E2005-APP's.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case, on RWB-P3-E1043-CON | LOV-DECISION with the value "D6" and its version in force, for the decision-code check of the profile (DP-07); faked, one hop, 2 s (DP-11) |

This is the only operation this story calls. The scope filter is the cached permission decision the service template holds from rwb-access, so no case read is made; RWB-P3-E1018-CON defines the case ID value the record cites and supplies its fake, and it is not called at run time.

#### 12.3 Events published

None. The append of a ledger entry writes no further record and publishes no event, because the ledger is the seal (BR6). The events of this service belong to other stories: `rwb.decision.RulePackageInForce.v1` (EV-30, RWB-P7-E1073-APP) and the records of the writer (RWB-P7-E1027-APP).

#### 12.4 Events consumed

| Event | Topic | Producer | Key | What this story does with it |
|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | rwb-case, when it creates a case | entryId, with the event ID and idempotency key held by the inbox | Applies `CaseCreationRecordProfile` and hands a passing record to the appender of RWB-P7-E1008-APP; a record for another decision is that story's to append, and a repeat appends nothing (DP-03, DP-09) |

The payload is the record shape of RWB-PLT-E1027-CON and the fields of TSD P7 T3.1, mapped one to one with no added field. No event carries a name, an e-mail address, a mobile number, an account number or any other personal value.

#### 12.5 Workflows and activities

None. The ingest is a Kafka listener with an inbox and a dead-letter topic, not a workflow; the read is synchronous REST; the chain check is `CreationEntryChainCheck` on the answered entry, not an activity. The promote workflow of JOB-20 is RWB-P7-E1073-APP's, and the evaluation of ENTRY and EXCLUSION is an activity in rwb-case (DP-04).

#### 12.6 Schedules

None. The three jobs of this service belong to other stories: JOB-13, the continuous ingest, is RWB-P7-E1008-APP's; JOB-14, the 02:00 chain check, is RWB-P7-E1008-APP's; JOB-20, the 00:01 promotion, is RWB-P7-E1073-APP's. The legacy JOB-02, the case-creation job that raises the record, becomes the event-started workflow of rwb-case (DP-10).

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `decision_log_entry` | P7 (`rwb_decision`) | The creation entry: appended through the baseline of RWB-P7-E1008-APP and read by the profile read |
| `rule_package`, `rule_package_version` | P7 (`rwb_decision`) | The package row of ENTRY and the version label and state that answer whether a cited label is held |
| `rule_row` | P7 (`rwb_decision`) | The rule ID a label carries, read only to name the rule the record cites |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_decision` | The inbox of `DecisionRecorded` and the idempotency rows of the ingest (DP-09) |

Not owned and not read: every `rwb_case` table (no foreign key, no read, BR11), every `v_ace_*` view (DP-05; this service reads no ACE data), `approval` and `delegation_limit` (P7, but the stories of RWB-P7-E2013-APP), `rule_test_case` (RWB-P7-E1073-APP writes it) and the retired data-lake copies (DP-17). No foreign key crosses a schema.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case reference-data and contract fake | RWB-P3-E1043-CON and RWB-P3-E1018-CON | LOV-DECISION with "D6" and its version in force, without "D99"; the synthetic case `RW-2026-000123` for borrower `P-0101` and account `A-5001` |
| decision-record topic fixture | RWB-PLT-E1027-CON | The creation record of `RW-2026-000123`; a record of `RW-2026-000124` with the rule ID and no label; a record with code "D99"; a record of `RW-2026-000125` citing "ENTRY-2026.12"; a repeat of event `EV-7f3a-0001` |
| ledger and registry fixtures | RWB-P7-E1008-APP and RWB-P7-E1073-APP | The append at the next `chain_seq`, the append-only refusal, the 64-zero first `prev_hash`, a forced append failure and the entry at `chain_seq` 230 changed with the trigger disabled; "ENTRY-2026.11" of ENTRY in force, and no "ENTRY-2026.12" until AC3 loads it |
| rwb-source-data contract fake | Not specified in the source documents (CG-ALL-6888) | Account `A-5005` with an open dispute; reason "OPEN_DISPUTE" under rule ID "EXCL-006" |

Each fake is replaced by the real contract or the real library as its story lands, without a change to the scenarios. All values are the legacy story's synthetic keys, package codes, version labels and states.

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 1, consumed 1 | The case-creation filter of the ledger read; the LOV-DECISION list read, one hop and 2 s |
| Kafka | Consumed 1 event type, published 0 | `DecisionRecorded` on `rwb.decision-record.v1` from rwb-case; the append publishes nothing |
| Temporal | 0 | No Schedule, no workflow and no activity of this story's own |
| File | None | This story reads and writes no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `creation`, Java package `th.co.scb.ace.workbench.recovery.decision.creation`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or the recovery schema | Owner's schema `rwb_decision`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-APP |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/decision/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.decision.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

This is a secondary slice with no owned legacy acceptance criterion of a build story: it adds no build dependency of its own (metadata "Depends on (build)" is None; GAP-2437; ASM-4046) and builds against the baseline of RWB-P7-E1008-APP, the record library of RWB-PLT-E1027-CON and the registry rows of RWB-P7-E1073-APP. DP-01 and DP-02 are the target shape itself. DP-03 is the record shape this profile reads. DP-04 applies as a prohibition plus one reference: the packages are versioned by rwb-decision and evaluated in rwb-case with the kit of RWB-PLT-E1072-CON, and the profile only asks whether a label is held. DP-05 is a prohibition, because this service reads no ACE view. DP-06 adds nothing here, since the only tunable is an observability setting. DP-07 is the LOV-DECISION read. DP-09 is the inbox of the ingest. DP-10 is recorded and not built: the legacy JOB-02 becomes rwb-case's event-started workflow, and this service's schedules belong to the two stories named in 12.6. DP-11 is the list read. DP-13, DP-14 and DP-15 are the base, the names and the migration `V1018_2__case_creation_profile.sql`. DP-19 is the composite route behind SCR-38.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseCreationRecordProfile | Service | Applies BR1 to BR4 to a `CASE_CREATED` record before any append and answers the field of a refusal |
| RegistryHoldRepository | Repository | Answers whether `rule_package_version` holds a label for package ENTRY, and the rule ID behind it; reads only `rwb_decision` |
| CaseCreationLogController | Controller | Serves the `finalCall=CASE_CREATED` filter of the ledger read with the Decision log R guard, the scope filter and the problem mapping |
| CreationEntryChainCheck | Service | Recomputes the hash of the answered entry, sets `chainVerified`, answers MSG-P7-012 on a break and raises the Compliance incident |
| ReferenceDataClient | Client | The LOV-DECISION read of 12.2, one hop with a 2 s timeout and a breaker |

**Database and migrations.** Writes `decision_log_entry` and the library objects in `rwb_decision` through the baseline of RWB-P7-E1008-APP; reads `rule_package`, `rule_package_version` and `rule_row` in the same schema; reads no other schema and holds no foreign key into another schema. One migration in the per-service Flyway sequence of DP-15, `V1018_2__case_creation_profile.sql`, adds the partial index on `(case_id, final_call)` that serves the creation read; it adds no column, no constraint across schemas and no seed row.

**Configuration and reference data.** No business value is configured here: the decision code comes from LOV-DECISION with its version, the final call from the record shape, the version labels and rule IDs from the registry, and the case reference from the record. Two settings only: the base of the rwb-case reference-data contract and the `rwb-decision` service identity of DP-02. The feature switch `rwb.p7.creation.profile` holds the profile off in an environment where the registry is not yet loaded: the ledger stays readable, no creation entry is admitted, and the records wait in the producers' outboxes.

**Build steps**

1. `RegistryHoldRepository` over `rule_package`, `rule_package_version` and `rule_row` in `rwb_decision`; tests for AC3.
2. `CaseCreationRecordProfile` with the five checks and the refusals naming the field, including the LOV-DECISION read; tests for AC1, AC2 and AC3.
3. The ingest hook into the listener of RWB-P7-E1008-APP with the inbox dedupe and the first-entry-ID answer; test for AC4.
4. `CaseCreationLogController` with the `finalCall` filter, the guard, the scope filter, the 404 and the 503; tests for AC1, AC5 and AC6.
5. `CreationEntryChainCheck` with the recomputation, the `chainVerified` flag, the MSG-P7-012 warning and the Compliance incident; test for AC7.
6. The privacy test: the topic fixture, the entry and the answer hold IDs, codes, labels, dates and hashes only, and no name, e-mail address, mobile number, national identity number or account number.

**Done when.** The tests in section 16 pass; a SIT week shows one entry per case creation with "D6", "CASE_CREATED", the ENTER rule ID and "ENTRY-2026.11"; no case attribute column in `rwb_decision`; no foreign key into another service's schema; a label the registry does not hold refused with the field named; one entry on a repeated event; and a chain break reported with MSG-P7-012 while the stored row is unchanged.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-009 | Half a rule reference, a version label the registry does not hold, or a decision code outside LOV-DECISION | The message text is Not specified in the source documents (GAP-2433; ASM-4042); the detail names the field, "ruleId", "ruleVersion" or "decisionCode" |
| MSG-P7-012 | An answered entry does not match the chain | The warning text is Not specified in the source documents (GAP-2433; ASM-4042); the warning names the entry's `chainSeq` |
| MSG-P7-003 | The ledger store is unavailable for an append or a read | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The caller's role holds no Decision log R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The entry's case sits outside the caller's scope | This case is not in your scope. |

Every error is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled, and `instance` naming the request. For MSG-P4-002 the {action} value names the action the caller tried, "read the decision log of this case", and never a case fact. A refusal never echoes the rule ID, the version label or the case reference of another tenant's case.

Screen states: SCR-03 and SCR-38 have no empty, loading, error or no access state in this story; each is Not specified in the source documents (DOR-RWB-P7-E1018-APP-10).

### 15. Screens and states

SCR-38 Decision log query shows the entries with their decision code, rule ID, rule version, final call, actor, decided time and `chainVerified`, and the decision list of a case shows the same entries for one case, both through the gateway-bff composite route (DP-19). This slice fixes only what the read answers for a case creation and the MSG-P7-012 warning on a row that does not verify. The screen, its filters, its saved searches, its export and its loading, empty and filtered states are RWB-P7-E2005-APP's, first in Epic 2. SCR-38 error and no access states: Not specified in the source documents (CG-ALL-6890); the empty state is also Not specified in the source documents (CG-ALL-6890) and is not fixed by this slice. The creation entry has no screen of its own inside this service: the reader who wants the basis of a case sees it on that query, and the case owner sees the same entry on the case decision list of SCR-03, which rwb-case and rwb-decision serve through the composite route. SCR-03 loading state: as Screen Specifications v1 gives it; empty, error and no access states: Not specified in the source documents (CG-ALL-6889).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-018-02 | AC2, BR1, BR11: an excluded account has no case, so no "D6" entry is appended; the exclusion record is rwb-case's | Integration | Account `A-5002` at 92 days past due with `tdr_flag` true; package EXCLUSION "EXCL-2026.11"; reason "ACTIVE_PLAN"; rule ID "EXCL-004" |
| TC-E1-018-01 | AC1, BR1, BR2, BR4, BR7: one entry per case creation with "D6", "CASE_CREATED", the ENTER rule ID, "ENTRY-2026.11" and the ALS business date, read back with its versions | Integration | Case `RW-2026-000123`, borrower `P-0101`, account `A-5001`, business date 2026-12-01, last number `RW-2026-000122`; the literal ENTER rule ID is Not specified in the source documents (GAP-2436; ASM-4045) |
| TC-E1-018-03 | AC3, BR11: one case for the customer and product means one creation entry and no second one | Component | Borrower `P-0102` with hire purchase accounts `A-5003` at 300,000.00 and `A-5004` at 112,350.00 |
| TC-E1-018-04 | AC4, BR5: a closed case keeps its entry and its chain position, and the next creation appends after it | Component | Case `RW-2026-000123` closed on 2026-12-15; the next case `RW-2026-000124` created on 2026-12-16 |
| TC-E1-018-05 | AC5, BR3: a new decision code arrives as list data with a version and the profile accepts it without a code change | Contract | A code added to LOV-DECISION with valid from 2027-01-01, read through DP-07 with the version in force |
| TC-E1-018-06 | AC6, BR1: an account excluded for a disputed balance has no case and no entry; the exclusion rule is rwb-case's | Integration | Account `A-5005` with an open dispute, supplied by the rwb-source-data contract fake (§12.8); reason "OPEN_DISPUTE"; rule ID "EXCL-006" |
| TC-E1-018-07 | AC7, BR1: the account at 90 days past due has a case and an entry; the account at 89 has neither | Component | Accounts `A-5006` at 89 days past due and `A-5007` at 90 days past due |
| TC-E1-018-08 | AC8, BR8: a repeated run and a repeated event give one entry and the first entry ID | Integration | Case `RW-2026-000125` for account `A-5008` on 2026-12-01; event `EV-7f3a-0001` consumed twice |
| TC-E1-018-09 | AC9, BR1: no case before the ALS batch completes, so no entry is appended and the chain has no gap | Integration | ALS batch for 2026-12-02 at status "RUNNING" at the 09:00 cut-off; MSG-P1-001 on the job monitor for 2026-12-01 |
| TC-E1-018-10 | AC10, BR10: a failed append leaves nothing behind and the record is retried | NFR | Account `A-5009`; the ledger store forced unavailable for the whole run; MSG-P7-003; `chain_seq` unchanged |
| TC-E1-018-11 | AC1, BR5: the yearly number range is rwb-case's, so no entry is invented for `A-5010` and no `chain_seq` is consumed | Component | Last number issued `RW-2026-000999`; account `A-5010` qualifying on 2026-12-30; MSG-P3-025 for year 2026 |
| TC-E1-018-12 | AC1, BR11: two products give two cases and two entries, each with its own case reference | Component | Borrower `P-0103` with mortgage account `A-5011` and hire purchase account `A-5012` at 91 days past due |
| TC-E1-018-13 | AC5, BR12: a role without Decision log R is refused with MSG-P4-002, and a case outside the scope with MSG-P4-003 and no case attribute | Component | A caller without Decision log R reads case `RW-2026-000123`; a caller in scope for one region reads case `RW-2026-000126` of another |
| TC-E1-018-14 | AC6, AC7, BR9, BR10: a store failure and a broken chain leave the ledger untouched | NFR | The record write forced to fail for the whole run; the entry at `chain_seq` 230 changed with the trigger disabled |
| TC-E1-018-15 | AC1, BR11: a case reference whose key has no view row is held as it arrived and never invented; no case row is read | Component | Case `RW-2026-000126` linking `A-5013` and `P-0105` with no view row for 2026-12-01; REC-05 lists both keys for the data steward |
| TC-E1-018-16 | AC3, BR4: no EXCLUSION version in force means no case and no entry; a label the registry does not hold is refused | Integration | No EXCLUSION version in force on 2026-12-01; MSG-P3-027 for package "EXCLUSION"; a record citing "ENTRY-2026.12" before it is loaded |
| TC-E1-018-17 | BR11, section 12.7: only the owned tables are read or written; no `rwb_case` table, `v_ace_*` view or retired data-lake copy is read | Component | Case `RW-2026-000123` for account `A-5001` through the flow of section 4; the tables of section 12.7 only |
| TC-E1-018-18 | AC8, BR6: the append writes only the entry and publishes no event | Component | Case `RW-2026-000123` appended once; the event outbox and the tables of section 12.7 checked for any further row |
| TC-E1-018-19 | AC9, BR12: a read without a token is answered 401 and a case with no entry is answered 404 | Component | Caller without a token on GET /api/recovery/decision/v1/decision-log; case `RW-2026-000124` with no entry |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to End to end and Access to Component; the levels above are set for the slice this story answers, which is the creation entry and its basis rather than the case. The -ITG copies belong to RWB-ITG-E1018-ITG, which proves the same values across rwb-case, rwb-source-data, rwb-access, rwb-document and rwb-decision end to end.

### 17. Guardrails

- No business value in code: the decision code is a value of LOV-DECISION read with its version, the final call is a value of the record shape, and the version labels and rule IDs are registry rows; the case reference is a value of the record.
- No personal data in events, workflow inputs, logs, tests or answers. The record, the entry and the answer carry IDs, codes, labels, dates and hashes only; no name, address, identity number or account number is logged, and a refused record is logged with the case reference and the field only.
- No cross-schema read (DP-01), and ACE data only through the owner's contract or `v_ace_*` views, which this service reads neither (DP-05): `rwb_decision` reads no `rwb_case` table, holds no foreign key into another schema and holds no case attribute column.
- The ledger is append-only and the chain is checked on read into the answer only: this service has no update and no delete path on `decision_log_entry`, and a read never rewrites an entry, never renumbers a `chain_seq` and never deletes a row to satisfy a scope.
- One evaluator decides every ENTRY and EXCLUSION outcome and it is not here: the profile asks whether a label is held and never evaluates a rule, and a version that is not held is a refusal rather than a default.
- The partial index of the migration is the only schema change this story makes, and no topic, event or queue name is typed in code (DP-14).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-001 | One case for every non-excluded account at 90 days past due | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-04 | 6.1 Take over the case at 90 days past due | BR1; R-UNI-16 | TC-E1-018-01, TC-E1-018-07, TC-E1-018-09 |
| REQ-CWC-002 | Case ID RW-YYYY-NNNNNN, issued once and never reused, carried on every record | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-01 | 6.1 | BR1, BR7, BR11 | TC-E1-018-01, TC-E1-018-04, TC-E1-018-08 |
| REQ-CWC-003 | One case per customer and product, linked by business key | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-02 | 6.1 | BR11; R-UNI-17 | TC-E1-018-03, TC-E1-018-12, TC-E1-018-15 |
| REQ-CWC-004 | Exclusion rules held as data and applied at creation | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-05 | 6.1 | BR4, BR11 | TC-E1-018-02, TC-E1-018-06, TC-E1-018-16 |
| REQ-CWC-005 | One case state at a time, from the state model and the lists | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-03 | 6.1 | BR3 | TC-E1-018-05 |
| REQ-CWC-016 | Every workflow event logged with its rule ID and version | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-21 | 6.1 | BR1, BR2, BR5, BR7; R-UNI-39 | TC-E1-018-10, TC-E1-018-14 |
| REQ-CHO-004 | One agreed hand-over point in days past due for every rule and report | Epic 1, 3.3 | FEAT-CWC-01 to FEAT-CWC-05, FEAT-CWC-20, FEAT-CWC-21 | 6.1 | BR1, BR4 | TC-E1-018-01, TC-E1-018-07 |

The features FEAT-CWC-20 (the workflow admin API) and FEAT-CWC-21 (log every workflow event) are carried by the case service; this slice answers FEAT-CWC-21 for the record that reaches the ledger and for the version label it cites. The -ITG copies of the test cases are carried by RWB-ITG-E1018-ITG.

| Legacy reference | Where it is kept |
|---|---|
| Legacy key RWB-E1-018; story RWB-P7-E1018-APP; contract RWB-P3-E1018-CON; baseline `rwb_decision` | Metadata; sections 1, 3, 12 |
| Decision code "D6", final call "CASE_CREATED", the ENTER rule ID and the package version (legacy flow step 11 and BR8); versions "ENTRY-2026.11" and "EXCL-2026.11"; rule IDs "EXCL-004" and "EXCL-006" | Sections 1, 3, 4, 7, 8, 11, 12.8 |
| Legacy BR11 (business key, no foreign key), D-RCV-35 U4 and ADR-010; legacy AC8 and R-UNI-40; principle 5, R-UNI-39 and R-UNI-41 | Sections 1, 7, 8, 11, 12.7, 14, 16, 17 |
| MSG-P7-003, MSG-P7-009, MSG-P7-012, MSG-P4-002, MSG-P4-003, MSG-P1-001, MSG-P3-025, MSG-P3-027; field IDs DF-DEC-001 to DF-DEC-031, DF-REF-275 to DF-REF-297 | Sections 5, 7, 11, 14 |
| EV-08 `DecisionRecorded`; the synthetic cases `RW-2026-000122` to `RW-2026-000126`, `RW-2026-000999`, accounts `A-5001` to `A-5013`, `P-0101` to `P-0105`, `EV-7f3a-0001`, `chain_seq` 230 | Sections 3, 7, 12.8, 16 |
| Legacy test cases TC-E1-018-01 to TC-E1-018-16; the other slices of RWB-E1-018 | Sections 2, 16, 19 |

### 19. Out of scope

- Case creation, grouping by customer and product, the yearly number and its range, the entry and exclusion evaluation, the case state model and the case screens: rwb-case (RWB-P3-E1018-APP).
- The ACE view read behind the entry and exclusion decisions: rwb-source-data (RWB-P1-E1018-APP).
- The access matrix, the scope decision and the access log: rwb-access (RWB-P4-E1018-APP); this service reads the cached decision from the template.
- The document binding of a case: rwb-document (RWB-P5-E1018-APP).
- The ledger store, its append-only trigger, the chain, the ingest, the two ledger reads, the audit query, the saved filters and the export: RWB-P7-E1008-APP with its CON, DB and OPS stories, and RWB-P7-E2005-APP.
- The writer, its record shape and the `DecisionRecorded` publication: RWB-P7-E1027-APP with its CON story and the library RWB-PLT-E1027-CON.
- The registry, the workbook load, the checks, the scenario runner, the dry run, the four-eyes approval, JOB-20, the model served to the owning services, the rollback and the six version states: RWB-P7-E1073-APP. This story reads the labels that story holds and serves nothing.
- The recommendation read, the approval queue and the delegation of authority: RWB-P7-E2013-APP with its CON and OPS stories; and the end-to-end proof of these values across the five services: RWB-ITG-E1018-ITG.
