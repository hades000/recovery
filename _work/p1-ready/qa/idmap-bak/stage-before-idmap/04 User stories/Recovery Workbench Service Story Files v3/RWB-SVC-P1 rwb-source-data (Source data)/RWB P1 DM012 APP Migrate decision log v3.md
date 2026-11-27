# RWB-P1-DM012-APP Migrate decision log

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-DM012-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-DM-012 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP15, DP19 |
| Parallel lane | L-P1-A |
| Size | Not specified in the source documents (DOR-RWB-P1-DM012-APP-16); the squad sizes it at refinement |
| Ready to start | After RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| Contract dependencies | None for this story's code beyond the decision-record library of RWB-PLT-E1027-CON; the result read of RWB-P1-E1011-CON, which it does not call |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7; RD-P1-005); event `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` (RD-P1-008) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-005, RD-P1-008, RD-P1-009, RD-P1-012, RD-P1-024, RD-P1-027, RD-P1-040, RD-P1-042, RD-P1-045, RD-P1-007, RD-P1-068, RD-P1-011 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-DM-012 for the P1 cutover extract of the legacy decision log entries, their recording as local decision records and publication as DecisionRecorded into the central ledger, and their cutover evidence. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-DM012-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (23 resolved, 6 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: targeted edits for version 3. Tool: Claude Sonnet 5.5.

**Version 3 changes** (D-RCV-60 P1 developer readiness):

- DecisionRecorded is published as `rwb.decision.DecisionRecorded.v1` with `ce_idempotencykey` and `ce_actor` (RD-P1-008, RD-P1-009), and the field list is closed by dictionary ID (RD-P1-027; findings #1, #2).
- An open conflict is recorded: the published event schema carries no chain fields and lets rwb-decision assign the chain (NEW-GAP-S13-4; finding #2).
- DL25 is applied with `recon.tolerance.pct` version 1 = 0.00 and the case-list references are removed (RD-P1-042, RD-P1-024, RD-P1-040).
- AC1 and AC3 are extended to check what is written, and AC8 and AC9 added (finding #5).
- Contract version, reads, screen states and rollback follow the register (RD-P1-005, RD-P1-012, RD-P1-045; findings #3, #4, #6).
- Batch D (RD-P1-068): rwb-decision owns `chain_seq` and `prev_hash` and this story sets no chain field; the chain-continuation rule is removed; publication of migrated entries stays behind the feature switch, off, until the event schema carries the legacy values (NEW-GAP-S13-4, blocks the publish step only) and the cutover evidence file lists every legacy `entry_hash` and the last legacy `entry_hash`; `model_version` is carried as a value at act time (closes NEW-GAP-S13-6); the library table `decision_record` of `rwb_source_data` is written through (DDL Pending, NEW-GAP-F08-7) with `ce_idempotencykey` the RD-P1-007 business key.

### 1. Story

As a **data steward (RW-DATASTEW)** and **an internal auditor (RW-AUDIT)**, I want **the decisions taken outside the Workbench on the open cases at cutover migrated with their rule and model version and their hash chain, each recorded as a local decision record and published as DecisionRecorded for the central ledger, together with the cutover evidence counted from the reconciliation results**, so that **the audit trail is unbroken from the first day, and no entry is rewritten, renumbered or re-hashed on the way**.

The legacy key is **not withdrawn and not preserved**: RWB-DM-012 stays a story, but its table moves. The Ownership Map puts `decision_log_entry` with **P7 rwb-decision**, which owns the central decision ledger, the approvals and the rule model registry, while the open-case set, the ACE business keys and the reconciliation stay with **P1 rwb-source-data**. The legacy story migrated entries into the monolith's one decision log; the target has no single log to migrate into (GAP-2176; ASM-3512).

- **Extract, in `rwb-source-data` (this story):** the cutover run reads the legacy decision log once, for the entries taken outside the Workbench on the open cases at cutover, **in chain order**, with the fields the legacy entry holds — the case, the decision code, the rule ID and its version, the model version, the approver and the approval level, the recommendation, the final call, the actions, the outcome and the decision time — plus its chain position, its `prev_hash` and its `entry_hash` (legacy Data table DF-DEC-001 to DF-DEC-031; AC1).
- **Record and publish, in `rwb-source-data` (this story):** for each entry the run writes a local decision record through the library of `RWB-PLT-E1027-CON` and its outbox row **in one transaction**, and the library's relay publishes **DecisionRecorded on `rwb.decision-record.v1`** (DP-03); publication of the migrated entries stays behind the feature switch, off, until the event schema carries the legacy values (RD-P1-068).
- **Seal, in P7 rwb-decision:** rwb-decision consumes DecisionRecorded idempotently into the central ledger and runs its own gap alerts and chain verification. This story writes **no `decision_log_entry` row**, holds **no ledger table** and has no grant on `rwb_decision`.
- **The chain is kept, never rebuilt, and this story sets no chain field:** rwb-decision owns `chain_seq` and `prev_hash`; no legacy entry is rewritten, renumbered or re-hashed; the legacy values are checked in the extract and the cutover evidence file lists every legacy `entry_hash` and the last legacy `entry_hash` (legacy AC1; RD-P1-068).
- **One transaction or nothing:** if the local record cannot be written, nothing is published and the run stops with MSG-P7-003; a decision that could not be recorded is never applied silently (legacy TC-DM-012-05).
- **Cutover evidence (this story):** ten consecutive business dates on which every REC-01 and REC-02 row is PASS under `recon.tolerance.pct` version 1 = 0.00 and no new REC-05 orphan appears on a migrated entry's case (DL25 option A applied by RD-P1-042); a break resets the count. The evidence is read from the `reconciliation_result` rows that JOB-04 writes; this story builds neither JOB-04 nor a counter table (legacy AC3; ASM-3514).
- **Per-service migration (DP-15):** one version on the sequence of `rwb_source_data`, which creates no ledger object, and whose description records the extract's definition, its field list and the chain ownership rule.
- **No endpoint and no screen of its own:** the legacy story states "No endpoint in this story" and "No screen in this story", and both stay true. The cutover states are read from the cutover record; SCR-44 Interface and job monitor shows the `ReconciliationWorkflow` runs behind the clean days through the gateway-bff composite route (DP-19; H `RWB-PLT-N001-CON`; RD-P1-012).

### 2. Business rationale

A decision log answers "who decided what, on which rule, and when" long after the officer, the rule version and the queue have moved on. Recovery is a business of decisions that cost money — a restructure granted, a write-off approved, a sale authorised, a route chosen — and each one must be explainable to internal audit and to the regulator in the order it happened, because the order is what shows an approval came before the money moved. A migrated log that restarts its numbering, or re-hashes its entries into a fresh chain, still reads like a log and is no longer evidence.

The legacy story states the position in its own words: "As a data steward, I want the decisions taken outside the Workbench on the open cases migrated with their rule and model version and their hash chain, so that the audit trail is unbroken from the first day." Its Data table names the two entities it migrates, quoted here character for character:

> | recovery_case | id, case_no, product_group, primary_person_key, status, stage_code and 27 more | DF-CAS-001 to DF-CAS-055 |
> | decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 16 more | DF-DEC-001 to DF-DEC-031 |

Its guardrails row fixes the boundary this story keeps: "No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views. A migrated record keeps its source and its migration date, and never a copy of an ACE row."

**Why the ledger is no longer P1's.** Architecture v5 gives rwb-decision "approvals, central decision ledger, DMN model registry" and gives rwb-source-data "ACE view contract, extension tables, freshness, reconciliation"; every service writes only its own schema, and the boundary is a build-breaking rule rather than a preference (DP-01). The target mechanism is stated just as plainly: a service writes a decision record in its own schema in the same transaction as the state change, hash-linked to the previous record, plus DecisionRecorded through its outbox to `rwb.decision-record.v1`, and rwb-decision consumes it idempotently into the central ledger with a completeness target, gap alerts and chain verification (ADR-022). A P1 story that inserted `decision_log_entry` rows would be writing in P7's schema. The legacy entries are still P1's cutover work because the open-case set at cutover is P1's, the ACE keys are resolved on P1's own views and login (DP-05), and P1 is the service that reads the legacy Workbench once at cutover for every migrated record of this key. The entries are read here, the record is written here in P1's own schema, and the ledger is sealed by P7: nothing is handed over as a file, because a file would be a second migration of the same records with its own date, its own failure mode and no transaction with the state change the record belongs to (GAP-2176; ASM-3512).

**Why the chain is kept and not rebuilt.** AC1 forbids rewriting, renumbering and re-hashing, because every entry is append-only. That rule does not soften because the log changes store: a renumbered entry would leave a `prev_hash` that no longer points at the entry recorded before it. One owner holds the chain: rwb-decision assigns `chain_seq` and `prev_hash` in the central ledger, and this story sets neither (RD-P1-068). The rule enforced here is narrow and provable — the legacy chain is checked as it is read, the cutover evidence file lists every legacy `entry_hash` and the last legacy `entry_hash`, and the chain check at 02:00 (JOB-14) stays with rwb-decision (legacy AC1; ASM-3513).

**Why the write and the publish are one transaction.** The dangerous outcome of a migration is a decision that is applied and not recorded, or recorded and not collected. The first is invisible to audit; the second leaves a hole the gap alert finds weeks later. Recording and applying in one transaction is the pattern the design states for every stage step, and this story applies it to the cutover: the local record and the outbox row commit together, the relay publishes afterwards, and a failed record write stops the run with MSG-P7-003 before anything is published (DP-03; legacy TC-DM-012-05).

**What the realignment adds that the legacy story could not say.** First, ownership: the ledger is P7's and the record is P1's, so the audit trail has one sealing point and nineteen writers rather than one log written from nineteen places (ADR-022). Second, the evidence is machine-readable: the ten clean days are a read over `reconciliation_result` rows that exist for every business date, not an assurance in a cutover meeting (ASM-3514). Third, the schema is honest: `rwb_source_data` holds the library's record and outbox and no ledger, so nobody later mistakes it for a second home of the decision log (DP-15).

**What carries over unchanged.** The case, the decision code, the rule ID and version, the model version, the approver and the approval level, the outcome, the decision time, the chain position and the two hashes of every migrated entry, kept in the extract and the evidence file until the event carries them (RD-P1-068); the append-only rule; the ten-clean-day gate with its sign-off; and the read-only retention of the legacy tables (legacy AC1 and AC3; section 7).

### 3. Preconditions

- The Ownership Map entry for `decision_log_entry` is accepted: it is **P7's**, and rwb-decision owns the central ledger, its gaps, its chain verification and JOB-14 (Ownership Map v1; DP-01; GAP-2176; ASM-3512).
- The decision-record contract `RWB-PLT-E1027-CON` is in place: the library that writes a local record with its chain link, writes the outbox row in the same transaction and publishes DecisionRecorded on `rwb.decision-record.v1`, with the platform retry and `.dlt` topics (DP-03; Template and Rules §R4).
- The per-service Flyway contract `RWB-PLT-E1044-CON` is in place, with the sequence of `rwb_source_data` and its baseline, so this story takes the next free version and writes one history row (DP-15; TSD P1 v3 T3.2).
- The data product catalogue of `RWB-P1-E1001-APP` is live: DP01 Account and arrears and DP02 Customer and party each name one system of record, so the case and the person on a migrated entry have one named owner before a key is resolved (FSD P1 v3 A2.2; TSD P1 v3 T3.6).
- The 30 read-only `recovery.v_ace_*` views exist and are granted to the `rwb_source_data` login by `RWB-P1-E1069-APP` and `RWB-P1-E1069-DB`; this story reads `v_ace_customer` to resolve the person keys on a migrated entry and nothing else of ACE for that purpose (FSD P1 v3 A2.1.2; TSD P1 v3 T3.3; T6.3).
- The open-case set at cutover is known: the `recovery_case` rows of the open cases in the legacy dump (the target keeps no `case_list_row`, RD-P1-024). `recovery_case` is **P3's** table; this story reads the case keys it needs and writes no case row (Ownership Map v1).
- JOB-04, `ReconciliationWorkflow`, a child of `AceIngestCheck` after the ALS stamp (RD-P1-040), writes `reconciliation_result` for REC-01, REC-02 and REC-05, graded PASS or BREAK under `recon.tolerance.pct` version 1 = 0.00; a run that cannot proceed writes no row (RD-P1-042). It is the build of `RWB-P1-E1011-APP`; this story consumes its rows and changes none of them (FSD P1 v3 A2.11).
- rwb-decision's `decision_log_entry` carries `migration_source varchar(20)` and `migrated_at timestamptz`, added by rwb-decision in its own Flyway step (RD-P1-027 item 3); the values of list LOV-MIGRATION-SOURCE are Pending: owner data owner (NEW-GAP-B4).
- **Open conflict that blocks the publish step only.** The published `rwb.decision-record.v1` contract (API Specification v7) names no rule ID or version, model version, approval level, outcome, decision time or chain field in the DecisionRecorded data, and its ingest rule has rwb-decision assign `chain_seq` and `prev_hash` under its chain lock; rwb-decision owns both (RD-P1-068). Pending: carrying the legacy `prev_hash`, `entry_hash`, rule ID and rule version on DecisionRecorded, owner rwb-decision contract owner with compliance (NEW-GAP-S13-4). The extract, chain guard, mapper and local decision records are built now; publication of the migrated entries stays behind `rwb.source-data.decision-cutover`, off, until the schema carries the fields.
- The gateway-bff composite route of `RWB-PLT-N001-CON` is in place, so the reconciliation runs behind the cutover can be read on SCR-44 without a screen of this story's own (DP-19).
- The synthetic fixture of the legacy decision log with a hash chain, the decision-record library fake, the `v_ace_customer` fixture and the reconciliation fixture exist before the first build, so the story needs no legacy and no production data (section 12.8).
- `rwb_source_data` holds the library's local `decision_record` table that every service owns, created by the shared library migration of `RWB-PLT-E1027-CON` (Architecture v5; RD-P1-068); this story and the sandbox write through it. Pending: its DDL in the physical schema, owner platform lead (library owner), tracked as NEW-GAP-F08-7; the interim Testcontainers build runs the library's own migration.
- The extract's source, its format, the ledger's sealing acknowledgement and the place that holds the sign-off are given by no source document (GAP-2177; ASM-3512; ASM-3514).

### 4. Flow

1. The release pipeline starts the decision-log cutover run for the cutover business date, under the `rwb_source_data` service identity and one Idempotency-Key per run. The run is a pipeline step, not an API call: this service publishes no operation for it (section 12.1).
2. DecisionLogExtractReader reads the legacy decision log once, for the entries taken outside the Workbench on the open cases at cutover, and selects the `decision_log_entry` fields of the legacy Data table plus `chain_seq`, `prev_hash` and `entry_hash`. It orders the entries by their chain position and by nothing else: no created-at, no id and no import order decides the sequence (legacy AC1).
3. DecisionChainGuard checks every entry before it is written: the entry carries its three chain fields, its `prev_hash` equals the `entry_hash` of its predecessor, and no `chain_seq` appears twice. A gap or a break stops the run and names the entry; nothing is renumbered to close it (ASM-3513).
4. DecisionRecordMapper maps the legacy entry onto the local `decision_record` of the library — the case, the decision code, `ruleId`, `ruleVersion`, the model version, `recommendation`, `approverUserId`, `approvalLevel`, `finalCall`, `actions`, `outcome` and `decidedAt`. It sets no chain field: the legacy `chain_seq`, `prev_hash` and `entry_hash` stay in the extract and the evidence file (RD-P1-068). It adds no field and invents no value.
5. DecisionKeyResolver resolves the case and person keys on the entry against this service's views on its own login. A key that resolves to no view row does not stop the extract: the entry is recorded with its key as it stands and the orphan is listed for the data steward and the ACE team, because a suppressed break is a silent loss (BR-P1-001-2; DP-05).
6. DecisionRecordWriter writes, **in one transaction in `rwb_source_data`**, the local decision record through the library and its outbox row. If that write fails, nothing is committed, nothing is published, and the run stops with MSG-P7-003 (DP-03; legacy TC-DM-012-05).
7. Publication of the migrated entries is behind `rwb.source-data.decision-cutover` (RD-P1-068). While it is off, no DecisionRecorded of a migrated entry reaches the topic and the cutover evidence file lists every legacy `entry_hash` and the last legacy `entry_hash`. When it is on, after the event schema carries the legacy values, the library's outbox relay publishes **DecisionRecorded** (`ce_type` `rwb.decision.DecisionRecorded.v1`, with `ce_idempotencykey`, which is the RD-P1-007 rule 4 business key, and `ce_actor`; RD-P1-008, RD-P1-009) on `rwb.decision-record.v1` for each committed record, in chain order. A relay failure is retried from the outbox and finally lands on the topic's `.dlt`; nothing is lost and nothing is published twice (DP-03). Pending: how the library holds the outbox rows of migrated entries unpublished while the switch is off, owner platform lead (library owner), tracked as NEW-GAP-G4-1.
8. rwb-decision consumes each DecisionRecorded idempotently into the central ledger and names any record that never arrives; its load writes `migration_source` and `migrated_at`, under the workload identity and migration owner of rwb-decision, because SY-DATALOAD is retired (RD-P1-068). The ledger intake of this service also consumes the topic and writes a DECISION_TAKEN entry for an event with `data.caseId` (RD-P1-009). Pending: whether a migrated decision is ledgered as an interaction and with which `ce_actor`, owner solution architect (NEW-GAP-S13-5). That consumer, its alerts and JOB-14 are P7's and are not built here (ADR-022; GAP-2176).
9. The run writes the cutover evidence file: every legacy `entry_hash`, the last legacy `entry_hash` and the entry count. No record of this service takes a legacy hash as its `prev_hash`: the chain of the central ledger is rwb-decision's (RD-P1-068).
10. From the business date after the cutover, JOB-04 reconciles the business keys to the views and writes its results. CutoverEvidenceCounter reads the `reconciliation_result` rows of each business date and counts a clean day when every REC-01 and REC-02 row is PASS under `recon.tolerance.pct` version 1 and no new REC-05 orphan appears on a migrated entry's case (RD-P1-042 item 4); a break resets the count to zero, a date with no result row is not a clean day, and the counter holds no table (ASM-3514).
11. When the count reaches ten consecutive business dates the cutover record moves to ready for sign-off. The data steward signs off in the cutover record of the release pipeline, the legacy decision log stays read-only for its retention period, and the migrated entries are read from the central ledger through the rwb-decision contract (legacy AC3).
12. The version of this story is applied on the sequence of `rwb_source_data`. It creates no ledger object, adds no column to a library table, and records the extract's definition, its field list and the chain ownership rule in its history description.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The legacy decision-log extract is absent, unreadable or not the extract of the cutover business date | The run stops before any record is written; nothing is published, the pipeline step is FAILED and the cutover record names the extract and the date | None | AC1, component test |
| X2 | An entry lacks its case, its decision code, its rule ID, its rule version or its approver | The entry is refused and listed for the data steward; no partial record is written and no value is invented | MSG-GEN-001 | AC1, TC-DM-012-01 |
| X3 | Two entries share a `chain_seq`, or a position is missing from the sequence | The run stops and names both entries; the entries are never renumbered to close the gap, and the cutover is not signed off until the log's owner explains it | None | AC1, TC-DM-012-01 |
| X4 | An entry's `prev_hash` does not equal the `entry_hash` of its predecessor | The run stops and names the entry and the chain position; nothing is re-hashed and nothing is rewritten | None | AC1, TC-DM-012-01 |
| X5 | The local decision record or its outbox row cannot be written | The transaction rolls back, no DecisionRecorded is published, the run stops with MSG-P7-003 and the entry is named | MSG-P7-003 | AC4, TC-DM-012-05 |
| X6 | The outbox relay cannot publish a committed record | The record stays in the outbox, the relay retries, and the topic's `.dlt` holds it after the last attempt; nothing is written twice | None | AC1, component test |
| X7 | rwb-decision does not confirm an entry into the ledger within its completeness target | The gap alert in rwb-decision names the record; this story neither re-publishes by hand nor writes a ledger row | None | AC3, integration |
| X8 | A person key on a migrated entry resolves to no `v_ace_customer` row | The entry is recorded with its key unchanged and the orphan is listed for the data steward and the ACE team; nothing is deleted and nothing is rewritten | None | AC1, AC3 (a break day is not counted) |
| X9 | The ACE batch of a business date is not COMPLETED, so the reconciliation cannot run and writes no row | The date counts as no clean day and the product is named with its last completed business date; a stale product is never treated as a clean day | MSG-P1-001 | AC3, AC9 |
| X10 | A caller without the Platform administration right asks for the cutover result or starts the run | The call is refused before the extract is read or any record written | MSG-P4-002 | AC5, TC-DM-012-04 |
| X11 | The version of this story is applied a second time, or the run is repeated for the same business date | Flyway reports the version as already applied; a repeated run publishes nothing twice, because each record carries its idempotency key | None | AC1 |

The message texts are the legacy ones, unchanged (section 14), except MSG-P1-001, which is copied from the Error and Message Standard (current version v6). X1, X3, X4, X6 and X11 are exercised inside the story's own tests and carry no new message ID.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | One reader over the legacy log, one chain guard, one mapper, one key resolver, one record writer and publisher pair, one evidence counter and one Flyway version; the ledger, its consumer and JOB-14 are P7's |
| Negotiable | The extract's format and location, the cutover record's layout and the retention period of the legacy tables are agreed at the wave 4 entry check; this story fixes the fields, the chain rules and the no-rewrite rule only |
| Valuable | Every decision taken before cutover keeps its rule version, its approver and its place in the chain, and the cutover is signed off on ten counted clean days rather than on assurance |
| Estimable | One reader, one chain guard, one mapper, one resolver, one writer and relay pair, one counter, one evidence file, one no-ledger migration version and the test cases of section 16 |
| Small | Fits one sprint; the ledger, the consumer, JOB-14 and the cross-service chain proof belong to other stories |
| Testable | Every criterion in section 7 runs against synthetic fixtures with no legacy data and no ACE data |

### 7. Acceptance criteria

```gherkin
Feature: Migrate decision log

  Scenario: AC1 Extract the Workbench records (legacy RWB-DM-012 AC1)
    Given the legacy Workbench decisions taken outside it on the open cases at cutover
    Given the rwb-decision contract mock returns the sealed entry with its chain position, its prev_hash and its entry_hash from the central ledger
    When the migration reads them
    Then each entry keeps its case, its decision code, its rule and model version, its approver and its position in the chain
    And no entry is rewritten, renumbered or re-hashed, because every entry is append-only
    And each source entry has one committed local decision record and one outbox row in "rwb_source_data" holding every section 11 field unchanged except the legacy chain values, with no chain field set by this story
    And each outbox row carries "ce_type" "rwb.decision.DecisionRecorded.v1", "ce_idempotencykey" and "ce_actor"
    And the cutover evidence file lists every legacy "entry_hash" and the last legacy "entry_hash"
    And no row is written in "rwb_decision" and no ledger table exists in "rwb_source_data"

  Scenario: AC3 Cut over (legacy RWB-DM-012 AC3)
    Given ten clean days on the migrated records
    Given the rwb-decision contract mock returns the migrated entries served from schema "rwb_decision"
    When the data steward signs off
    Then the legacy tables stay read-only for their retention period
    And the migrated records are served from the new schema
    And the ten clean days are ten consecutive business dates on which every REC-01 and REC-02 row is "PASS" under "recon.tolerance.pct" version 1 = 0.00 and no new REC-05 orphan appears on a migrated entry's case
    And the cutover record holds the sign-off, the ten result sets, the entry count, every legacy "entry_hash", the last legacy "entry_hash" and the retention window

  Scenario: AC4 The local decision record cannot be written and nothing is published (new, D-RCV-60)
    Given the decision-record library fake is switched to fail the local record write
    When the cutover run records an entry
    Then the local record and its outbox row roll back together
    And no DecisionRecorded is published and the run stops with MSG-P7-003 naming the entry

  Scenario: AC5 A caller without the Platform administration right is refused (new, D-RCV-60)
    Given a caller whose Platform administration right is absent
    When the caller starts the cutover run or reads the cutover result
    Then the call is refused before the extract is read or any record is written
    And the refusal carries MSG-P4-002

  Scenario: AC6 Publication of migrated entries stays off until the event carries the legacy values
    Given the feature switch "rwb.source-data.decision-cutover" is off and the decision-record library fake holds three migrated entries in chain order
    When the cutover run completes
    Then no DecisionRecorded of a migrated entry is on rwb.decision-record.v1
    And no record carries a chain field set by this story
    And the evidence file lists the three legacy "entry_hash" values and the last of them
    Given the switch is turned on after the event schema carries the legacy values
    When the relay publishes the three records
    Then the events leave in chain order, each "ce_idempotencykey" being the record's business key, and a rerun publishes nothing twice

  Scenario: AC7 A sign-off before ten clean days is refused (new, D-RCV-60)
    Given the cutover record has nine consecutive clean business dates
    When the data steward signs off
    Then the sign-off is refused
    And the cutover record is not marked signed off and records the refusal with the date and the count of nine

  Scenario: AC8 A chain break stops the run and nothing is rewritten (new, X3, X4)
    Given a synthetic log whose third entry has a "prev_hash" unequal to the "entry_hash" of the second
    When the run validates and records the log
    Then the run stops FAILED and names the third entry and its "chain_seq"
    And no record, outbox row or event exists for the third entry or any later one
    And the committed records of the first two entries stay unchanged, and no entry is renumbered or re-hashed

  Scenario: AC9 A missing or breaking date resets the count (new, RD-P1-042)
    Given nine consecutive clean business dates
    When the next date has a "BREAK" row, a new REC-05 orphan or no "reconciliation_result" row, and the data steward asks to sign off
    Then that date adds no clean day, the count restarts at zero and the date is listed
    And the sign-off is refused, and MSG-P1-012 is shown for a "BREAK" and MSG-P1-001 for a batch that is not "COMPLETED"
```

AC1 and AC3 are copied character for character from legacy RWB-DM-012. The two added Givens are the rwb-decision contract answers — the ledger is P7's, so the sealed entry and the served records are answered by that contract and its mock — and they change no legacy value. The added And lines of AC1 and AC3 state what is written (RD-P1-008, RD-P1-027, RD-P1-042, RD-P1-068). The message ID shown for a refused sign-off is Pending: owner Error and Message Standard owner (NEW-GAP-S13-2). AC2 Reconcile the business keys, the REC-05 step and its break list are owned by `RWB-ITG-DM012-ITG` and are not copied here; this story only reads the reconciliation results the evidence is counted from (ASM-3515).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | `decision_log_entry` is P7's: this story writes no `decision_log_entry` row, holds no ledger table and gets no grant on `rwb_decision` | Ownership Map v1; DP-01; GAP-2176 |
| BR2 | The extract and the cutover evidence keep, for every migrated entry, the fields the legacy Data table names plus its `chain_seq`, `prev_hash` and `entry_hash`; the local record holds every field except the three legacy chain values; nothing is invented | Legacy RWB-DM-012 AC1 and Data table; RD-P1-068 |
| BR3 | The local decision record and the outbox row are written in one transaction in `rwb_source_data`; if the record cannot be written nothing is published and the run stops with MSG-P7-003 | DP-03; ADR-022; legacy TC-DM-012-05 |
| BR4 | DecisionRecorded (`rwb.decision.DecisionRecorded.v1`, with `ce_idempotencykey` and `ce_actor`) is published on `rwb.decision-record.v1` through the decision-record library and its outbox, in chain order; publication of migrated entries is off until the event schema carries the legacy chain and rule values (Pending, NEW-GAP-S13-4) | DP-03; ADR-022; RD-P1-008; RD-P1-009; RD-P1-068 |
| BR5 | rwb-decision consumes DecisionRecorded idempotently into the central ledger; its gap alert, its completeness target and its chain verification are that service's | ADR-022; GAP-2176 |
| BR6 | rwb-decision owns `chain_seq` and `prev_hash`; this story sets no chain field, rewrites none and continues no chain; the cutover evidence file lists every legacy `entry_hash` and the last legacy `entry_hash` | Legacy RWB-DM-012 AC1; RD-P1-068; ASM-3513 |
| BR7 | No entry is rewritten, renumbered or re-hashed; an order that is out of sequence stops the run instead of being closed by renaming | Legacy RWB-DM-012 AC1; ASM-3513 |
| BR8 | ACE data is read only through `recovery.v_ace_*` views, on the service's own login, with SELECT and nothing else; a person key that resolves to no row is listed, never repaired in place | BR-P1-001-2; TSD P1 v3 T6.3; DP-05 |
| BR9 | The cutover evidence is ten consecutive business dates on which every REC-01 and REC-02 row is PASS under `recon.tolerance.pct` version 1 = 0.00 with no new REC-05 orphan on a migrated entry's case; a break resets the count and no counter table is created | Legacy RWB-DM-012 AC3; FSD P1 v3 A2.11; DL25 option A (RD-P1-042); ASM-3514 |
| BR10 | The sign-off is held in the cutover record of the release pipeline, and the legacy tables stay read-only for their retention period | Legacy RWB-DM-012 AC3; ASM-3514 |
| BR11 | The service runs its own Flyway sequence in its own schema; the version of this story creates no ledger object and records the extract, its field list and the chain rule in its description | DP-15; ADR-021; TSD P1 v3 T3.2 |
| BR12 | `model_version` (DF-DEC-006) is carried as a value at act time, which ACE cannot answer later, although the dictionary names COLLINS as its system of record; the migrated row carries `migration_source` and `migrated_at` | Legacy RWB-DM-012 AC1; RD-P1-027 as amended by RD-P1-068; LDM v11 DF-DEC-006 |

Where each rule lives in the target: BR1 is the boundary, proved by writing nothing in `rwb_decision` while naming `decision_log_entry` only as a read. BR2 and BR7 are the content and the order of the extract, proved by the field list and by the chain guard's refusals. BR3 to BR5 are the record, the publication and the seal; only the first two are built here and the third is proved through the contract fake. BR6 is the chain ownership rule, proved by the absence of any chain field set here and by the evidence file. BR8 is the grant and the orphan handling. BR9 and BR10 are the cutover gate, and BR11 is the schema's honesty.

### 9. State transitions

None for a case. This story changes no case status, no stage and no task: the case state machine lives in rwb-case. The moves below are the states of the cutover itself, as the cutover record shows them, and of one migrated entry from the legacy log to the central ledger.

| From | Event | Condition | To |
|---|---|---|---|
| Not started | The cutover run reads the legacy decision log | The extract is the extract of the cutover business date | Extracted: every entry holds its fields and its three chain fields, and the chain guard passes |
| Extracted | DecisionRecordWriter commits the local record and its outbox row | One transaction, one entry at a time | Recorded: the record is in `rwb_source_data` and nothing has left the service yet |
| Recorded | The outbox relay publishes DecisionRecorded | The outbox row is committed and the feature switch is on | Published: the event is on `rwb.decision-record.v1` in chain order |
| Published | rwb-decision consumes the event into the central ledger | Once only, inside the completeness target | Sealed: the entry is in the central ledger under P7 with its chain position intact |
| Extracted | The chain guard finds a gap, a duplicate `chain_seq` or a broken `prev_hash` | The entry under test | Stopped: the run ends with the entry named and nothing written for it or after it |
| Recorded | The local record or the outbox row cannot be committed | The write under test | Rolled back: no record, no event, the run ends with MSG-P7-003 |
| Sealed | JOB-04 writes a PASS result set for a business date | Every REC-01 and REC-02 row PASS and no new REC-05 orphan | Ten clean days running: the count moves to the next business date |
| Ten clean days running | JOB-04 writes a BREAK result or raises a REC-05 orphan | The business date under test | Break: the count resets to zero and the date and its rows are listed |
| Ten clean days running | The data steward signs off in the cutover record | The count is ten | Signed off: the legacy log stays read-only for its retention period and the entries are read from the central ledger |

The record of each move is the cutover record of the release pipeline, the outbox row of the entry and the `reconciliation_result` rows for the business date. This story publishes no event that announces a move of the cutover itself; DecisionRecorded is the business fact of the decision, not of the migration.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward and data product owner | Runs the extract for the cutover date, reads the chain report and the clean-day count, and signs off in the cutover record (Platform administration R) |
| RW-AUDIT, internal audit | Reads the chain report, the entry list and the clean-day count, and confirms that no entry was renumbered or re-hashed (Platform administration R) |
| RW-COE, RW-COMPLY, RW-PLATADM, RW-SECADM | Read the cutover result and the reconciliation results; each holds Platform administration R |
| RW-TRIBE, squad member and tribe lead | Builds the reader, the chain guard, the mapper, the resolver, the writer and relay, and the counter; runs the tests; applies the version on the per-service sequence |
| The rwb-decision service identity (the `rwb_decision` login) | Consumes DecisionRecorded into the central ledger and owns JOB-14; this story never uses that login |
| The rwb-source-data service identity (the `rwb_source_data` login) | Reads the extract and `v_ace_customer`, writes the local record and its outbox row, and writes one Flyway history row; it holds no write on `rwb_decision` and none on any `public` table |
| The ACE team lead | Answers for a person key that resolves to no `v_ace_customer` row, and receives the orphan list |
| No delegation of authority level applies | The cutover takes no credit decision and changes no case fact |

The role codes are rows of rwb-access, and the read of the cutover result authorises through the guard of the published operation; this story adds no role and no grant of its own. The legacy permission row for the key is Platform administration R for the six roles above, and it is kept unchanged.

### 11. Data

The record fields are one row per Logical Data Model v11 field of `decision_log_entry` (RD-P1-027). The same rows are to be held in Source to Target Mapping v7, sheet Migration packages.

| BR Field ID | Entity | Field | Disposition | Note (classification, Data Classification v6) |
|---|---|---|---|---|
| DF-DEC-001 | `decision_log_entry` | `id` | CARRY | Not personal, Internal |
| DF-DEC-002 | `decision_log_entry` | `case_id` | CARRY | Not personal, Internal |
| DF-DEC-003 | `decision_log_entry` | `decision_code` | CARRY | Customer data, Confidential |
| DF-DEC-004 | `decision_log_entry` | `rule_id` | CARRY | Customer data, Confidential |
| DF-DEC-005 | `decision_log_entry` | `rule_version` | CARRY | Customer data, Confidential |
| DF-DEC-006 | `decision_log_entry` | `model_version` | CARRY | Customer data, Confidential; value at act time: ACE cannot answer it later (RD-P1-068; LDM source system COLLINS); with `migration_source` and `migrated_at` |
| DF-DEC-007 | `decision_log_entry` | `agent_version` | CARRY | Customer data, Confidential |
| DF-DEC-008 | `decision_log_entry` | `inputs_ref` | CARRY | Customer data, Confidential |
| DF-DEC-009 | `decision_log_entry` | `recommendation` | CARRY | Customer data, Confidential |
| DF-DEC-010 | `decision_log_entry` | `approver_user_id` | CARRY | Staff identifier, Internal |
| DF-DEC-011 | `decision_log_entry` | `approval_level` | CARRY | Customer data, Confidential |
| DF-DEC-012 | `decision_log_entry` | `final_call` | CARRY | Customer data, Confidential |
| DF-DEC-013 | `decision_log_entry` | `override_reason` | CARRY | Customer data, Confidential |
| DF-DEC-014 | `decision_log_entry` | `actions` | CARRY | Customer data, Confidential |
| DF-DEC-015 | `decision_log_entry` | `outcome` | CARRY | Customer data, Confidential |
| DF-DEC-016 | `decision_log_entry` | `decided_at` | CARRY | Customer data, Confidential |
| DF-DEC-017 | `decision_log_entry` | `prev_hash` | CARRY | Customer data, Confidential; this story sets no chain field; kept in the extract and the evidence file; publication off until the event carries it (NEW-GAP-S13-4) |
| DF-DEC-018 | `decision_log_entry` | `entry_hash` | CARRY | Customer data, Confidential; this story sets no chain field; kept in the extract and the evidence file; publication off until the event carries it (NEW-GAP-S13-4) |
| DF-DEC-028 | `decision_log_entry` | `chain_seq` | CARRY | Customer data, Confidential; this story sets no chain field; kept in the extract and the evidence file; publication off until the event carries it (NEW-GAP-S13-4) |
| DF-DEC-029 | `decision_log_entry` | `corrects_entry_id` | CARRY | Not personal, Internal |
| DF-DEC-030 | `decision_log_entry` | `actor_user_id` | CARRY | Staff identifier, Internal |
| DF-DEC-031 | `decision_log_entry` | `idempotency_key` | CARRY | Customer data, Confidential |
| DF-CAS-001 to DF-CAS-023, DF-CAS-046 to DF-CAS-055 | `recovery_case` | all fields | EXCLUDE | Read for the open-case set; the case travels as DF-DEC-002 `case_id` |
| DF-ACE-055 to DF-ACE-074 | `v_ace_customer` | `person_key` and the other view fields | Not carried; read | Read only, to resolve a person key |
| DF-OPS-118 to DF-OPS-129 | `reconciliation_result` | reconciliation row fields | Not carried; read | The cutover evidence, written by JOB-04 |
| None (standard columns, LDM v11 sheet Standard columns) | `decision_log_entry` (rwb-decision) | `migration_source`, `migrated_at` | Provenance | Written by rwb-decision's load |
| None: library table | `decision_record` (the decision-record library's table) and `outbox` | Record fields, the library's own chain link, event payload, idempotency key, publish state | Write | One record and one outbox row per entry, in one transaction |
| None: framework table | `flyway_schema_history` | Version, description, checksum | Write | One row, at deploy only |

**`decision_log_entry` is P7's** and `rwb_source_data` holds **no ledger table** before or after this story: the service holds the library's own objects, which `RWB-PLT-E1027-CON` creates, and no decision log, no approval row and no rule registry. The legacy log is read once from its cutover extract; the record is written in this service's schema; the entry is served afterwards from the central ledger through the rwb-decision contract (BR1; GAP-2176). No chain field is set or recomputed here (BR6, BR7; RD-P1-068; ASM-3513). `recovery_case` is read for the open-case set and is P3's. The legacy values are Customer data: they appear in the library store and the event only, never in a log, a metric or a prompt. The extract's format and location, the record format of the cutover record and the retention period are Pending: owner data steward (GAP-2177).

### 12. Contract

**12.1 REST operations provided**

None. The legacy story states "No endpoint in this story", and the cutover is a release-pipeline command that reads an extract and writes records: it has no caller to address it, and no path of `/api/recovery/source-data/v1` is added here. The result of the cutover is read through operations that other RWB-SVC-P1 stories already publish and that this story neither claims nor changes:

| Operation | Base | Owner story | What it shows of this story |
|---|---|---|---|
| `GET /admin/reconciliation/results` (API-P1-003) | `/api/recovery/source-data/v1` | RWB-P1-E1011-APP | The PASS and BREAK rows the clean-day count is read from |
| `GET /admin/jobs` (API-P1-001) | `/api/recovery/source-data/v1` | RWB-P1-AD018-APP (contract RWB-P1-AD018-CON) | The `ReconciliationWorkflow` runs behind the clean days; the cutover step is not a job of the P1 job set (RD-P1-012) |

**Contract version.** This story builds against `rwb-source-data.yaml` 5.1.0 (API Specification v7; RD-P1-005), which holds `/admin/jobs` and `GET /admin/reconciliation/results` (RWB-P1-E1011-CON); its fake is pinned at 5.1.0 under `fakes/rwb-source-data/5.1.0/` (RD-P1-011).

**12.2 REST operations consumed**

None. The run reads its own extract file and its own views on its own login, writes its own record and publishes through its own library; it calls no service and holds no C dependency. The rwb-decision contract is used as a fake in the tests and as the read-back of the sealed entry, and it adds no run-time dependency (section 12.8).

**12.3 Events published**

| Event | Topic | Mechanism | Payload | Consumer |
|---|---|---|---|---|
| DecisionRecorded, `ce_type` `rwb.decision.DecisionRecorded.v1`, headers `ce_idempotencykey` and `ce_actor` | `rwb.decision-record.v1` (the shared topic of Template and Rules §R4) | The local decision-record library of `RWB-PLT-E1027-CON` and its outbox, in the same transaction as the local record | The case and decision code, `ruleId`, `ruleVersion`, the model version, `recommendation`, `approverUserId`, `approvalLevel`, `finalCall`, `actions`, `outcome` and `decidedAt`, with no legacy chain value (Pending, NEW-GAP-S13-4); published for migrated entries only when the feature switch is on; classed as Personal data (Data Classification and Personal Data Inventory v5); no name, identity number, contact point or address | rwb-decision (the central ledger); rwb-reporting; rwb-source-data (ledger intake, RD-P1-009) |

DecisionRecorded is raised by all 19 services and consumed by rwb-decision and rwb-reporting (ADR-022). This story publishes it through the library and never writes a Kafka record of its own. **`rwb.source-data.events.v1` gains no event**: AceDataReady and AceDataLate remain the topic's only events, published by `RWB-P1-E1015-APP` (RD-P1-003). The payload column states what the migrated entry holds; the published data schema does not yet name most of these fields (NEW-GAP-S13-4), so publication of migrated entries stays off (RD-P1-068).

**12.4 Events consumed**

None. No event starts the cutover: it is started by the release pipeline for the cutover business date. The reconciliation whose results are counted is a child workflow of `AceIngestCheck` in `RWB-P1-E1011-APP` (RD-P1-040).

**12.5 Workflows and activities**

None added. The cutover is a pipeline step; it calls the decision-record library's writer directly and starts no workflow on task queue `rwb-source-data`. RecordAndApply is the activity contract of each service's stage workflow; this story neither creates nor changes it.

**12.6 Schedules**

None. No Temporal Schedule and no legacy Quartz job sits in this story: the cutover is a one-off pipeline run, and JOB-14, the chain check at 02:00, is a Temporal Schedule in rwb-decision (GAP-2176).

**12.7 Tables owned**

| Table | Schema | Owner (ownership map) | This story |
|---|---|---|---|
| `decision_record` (library table) | `rwb_source_data` | P1, created by the shared library migration of `RWB-PLT-E1027-CON` (DDL Pending, NEW-GAP-F08-7) | Write, one record per migrated entry, in the same transaction as its outbox row |
| `outbox` | `rwb_source_data` | P1, created by the library | Write, one row per migrated entry; the relay publishes from it |
| `idempotency_key` | `rwb_source_data` | P1, created by the library | Write, one key per run and one per entry, so a rerun publishes nothing twice |
| `flyway_schema_history` | `rwb_source_data` | P1 | Write, one row for its own version at deploy |
| `decision_log_entry` | `rwb_decision` | P7 | **Not owned and not written here**: read once from the legacy extract, sealed into the central ledger by rwb-decision |
| `reconciliation_result` | `rwb_source_data` | P1 | Read only: the cutover evidence, written by JOB-04 (`RWB-P1-E1011-APP`) |

There is no ledger table in `rwb_source_data`, and this story adds none. No statement of the story names a table in `public`, and the only cross-schema read is the granted `recovery.v_ace_customer` view (DP-01, DP-05).

**12.8 Contract fakes**

| Fake | Serves | Used for |
|---|---|---|
| Legacy decision-log fixture with a chain | Synthetic `decision_log_entry` rows for the open cases at cutover with `chain_seq` 1 to 5, each `prev_hash` the `entry_hash` of its predecessor, one entry with a broken `prev_hash` and one duplicate `chain_seq` for the refusal paths | AC1, X1 to X4, from Day 1 |
| rwb-decision contract mock | The sealed entry with its chain position, its `prev_hash` and its `entry_hash`, and the migrated entries served from schema `rwb_decision` | AC1 and AC3, and the read-back of the seal |
| Decision-record library fake | The writer and its relay over an in-memory store and outbox, with a switch that forces the record write to fail | AC1, TC-DM-012-05, X5 and X6 |
| View fixture (`v_ace_customer`) | The view as synthetic rows in a container, with one person key that resolves and one that resolves to no row | AC1 and X8 |
| Reconciliation fixture (`reconciliation_result` rows) | PASS result sets for ten consecutive business dates, one BREAK set and one new REC-05 orphan for the counter-reset case | AC3 and X9 |

Each fake is generated from a fixture or from the published contract and its version is pinned in the cutover record, so a contract change shows up as a failed test rather than as a silent pass. The extract's real source and format, the ledger's acknowledgement and the place that holds the sign-off are Not specified in the source documents (GAP-2177; ASM-3512).

**12.9 Call-type summary**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | None | The cutover is a pipeline command; the result is read through API-P1-003 and API-P1-001, which other stories own |
| Kafka | One event: DecisionRecorded on `rwb.decision-record.v1` | None | Published by the library and its outbox; `rwb.source-data.events.v1` gains no event |
| Temporal | None | None | No workflow, activity or schedule; JOB-14 is rwb-decision's |
| File | None | One | The legacy decision-log extract, read once per cutover run |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata.decisioncutover`, in the service root `th.co.scb.ace.workbench.recovery.sourcedata`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`, login `rwb_source_data`, topic `rwb.source-data.events.v1` and task queue `rwb-source-data` (the last two are named for completeness and used by no part of this story).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DecisionLogExtractReader | Repository | Reads the legacy extract once and selects the entries of the open cases with the legacy fields and the chain fields; no write, no `public` table, no other schema |
| DecisionChainGuard | Service | Orders the entries by `chain_seq`, checks that every `prev_hash` equals its predecessor's `entry_hash` and that no position repeats, and names the entry that breaks the chain |
| DecisionRecordMapper | Service | Maps a legacy entry onto the library's decision record with every field the entry holds except the legacy chain values, sets no chain field and invents nothing |
| DecisionKeyResolver | Service | Resolves the case and person keys against this service's views on its own login, and names every key that resolves to no row |
| DecisionRecordWriter | Service | Writes the local decision record through the library and its outbox row in one transaction; on failure rolls back and raises MSG-P7-003 |
| DecisionRecordPublisher | Service | While the feature switch is on, runs the library's outbox relay for the run, publishes DecisionRecorded in chain order and leaves an unpublished record in the outbox for retry; while it is off, publishes nothing |
| CutoverEvidenceCounter | Service | Reads `reconciliation_result` per business date and counts ten consecutive clean dates under RD-P1-042; a break resets the count and no table holds it |
| `V<next>__dm012_decision_log_cutover.sql` | Migration | The next free version of the service's own Flyway sequence, V0001 to Vnnnn (Service Template Specification v1 §3.1): creates no ledger object, adds no column to a library table, and records the extract's definition, its field list and the chain ownership rule |

**Pattern application**

| DP code | legacy marker | microservice pattern | dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the heart of the story: the legacy `DecisionLogWriter` wrote the monolith's single log inside every call, and in the target the same act is a local record in the writer's own schema plus DecisionRecorded on the shared topic, sealed by the service that owns the ledger (ADR-022; GAP-2176). DP-05 applies in its own-service form: this is the service that owns the 30 views, so the key resolution is its own SQL on its own login and adds no contract hop. DP-15 gives this story its version and its history row, and gives each owner the sequence that holds its own objects, so no cross-schema write is needed. DP-19 applies to the read of the reconciliation runs on SCR-44 and adds no screen. No other pattern of the table applies: the outbox and its relay are the library's under DP-03 and not a separate DP-09 build, and there is no parameter or reference read (DP-06, DP-07), no guard library of this story's own (DP-08), no outbound call (DP-11), no cross-service adapter (DP-16) and no schedule (DP-10).

**Database and migrations**

- Reads the extract and `v_ace_customer`; writes one local decision record and one outbox row per migrated entry, and one Flyway history row at deploy.
- The library's objects are created by `RWB-PLT-E1027-CON` on the same sequence, and this story's version adds no column to any of them (DP-15; BR11).
- The version creates no ledger object: `rwb_source_data` holds no decision log, no approval row and no rule registry before or after it, and it grants nothing on `rwb_decision` (BR1). Its description records the extract's definition, the field list of the legacy entry, the chain fields and the chain ownership rule, so a later reader of the schema and of the history finds all four facts (GAP-2177; ASM-3513).
- The version number is the next free one on the sequence, after the baseline and the Section A and Section B versions of TSD P1 v3 T3.2. No source names the legacy migration file, so the story asserts that no version of the sequence names a decision-log extract, a ledger or a chain.
- The ledger's tables, its sequence and its consumer are rwb-decision's, and this story neither describes nor applies them (DP-15).
- The schema `rwb_decision` is owned by rwb-decision (Ownership Map v1); this story names it only to refuse any write or grant (BR1).

**Configuration and reference data**

- Parameters read: the feature switch `rwb.source-data.decision-cutover` from the platform flag library, which gates publication of the migrated entries (RD-P1-068). No reference list is read: DP-06 and DP-07 are not in the pattern set, and the reference-data contract is Not specified in the source documents (DOR-RWB-P1-DM012-APP-20). The cutover business date, the extract's location and the retention period are configuration of the release pipeline, agreed at the wave 4 entry check, and no value is written in code; where a source gives none the story names the assumption rather than a number (GAP-2177; ASM-3512).
- The library's topic name, its retry and `.dlt` topics and its idempotency key format are the contract's, not this story's; the story consumes them and re-implements none of them (DP-03).
- No chain rule is configured in this service: the chain of the central ledger is rwb-decision's, and the legacy hashes go to the evidence file (RD-P1-068).
- The feature switch is `rwb.source-data.decision-cutover`, from the platform flag library, off at deploy: off, the extract and the local decision records are built, no DecisionRecorded of a migrated entry is published and the cutover cannot be signed off; it stays off until the event schema carries the legacy values (RD-P1-068; NEW-GAP-S13-4).
- The login is `rwb_source_data`: SELECT on the 30 views, USAGE on `rwb_source_data`, no privilege in `public` and none in `rwb_decision` (TSD P1 v3 T6.3).

**Build steps**

1. DecisionLogExtractReader over the extract fixture, with the legacy fields and the chain fields; prove one read per run and no write outside the record and its outbox row.
2. DecisionChainGuard: a clean chain passes; a broken `prev_hash`, a duplicate `chain_seq` and a missing position each stop the run with the entry named; tests for AC1, X3 and X4.
3. DecisionRecordMapper: every field the legacy entry holds, and the assertion that the mapped record adds, drops and invents nothing; test for AC1.
4. DecisionKeyResolver over `v_ace_customer` with a resolvable and an unresolvable person key, and the orphan list for the data steward and the ACE team; tests for AC1 and X8.
5. DecisionRecordWriter over the library fake: the record and the outbox row in one transaction, and the forced failure that rolls both back and raises MSG-P7-003; test for TC-DM-012-05.
6. DecisionRecordPublisher: with the switch off nothing is published; with it on the relay publishes in chain order, the retry keeps an unpublished record in the outbox, and a rerun with the same idempotency keys publishes nothing twice; tests for AC1, AC6 and X6.
7. The evidence file test: it lists every legacy `entry_hash` and the last one, and no record carries a chain field set by this story; tests for AC1, AC6 and BR6.
8. CutoverEvidenceCounter over the reconciliation fixture: ten consecutive PASS dates, a BREAK on the sixth, a missing ACE batch and a new REC-05 orphan; tests for AC3 and X9.
9. The read-back of the sealed entry and of the served records through the rwb-decision contract fake, so the story proves the ledger and the chain position of a migrated entry; tests for AC1 and AC3.
10. The refusal path through the guard of the published operations, with no extract read after a deny; test for TC-DM-012-04.
11. The migration as a no-ledger version with the extract, the field list and the chain ownership rule in its description, and the repeated-apply check; test for AC1.

**Feature flag.** `rwb.source-data.decision-cutover`, from the platform flag library, gates publication of the migrated entries (RD-P1-068). Off: nothing of a migrated entry is published; the extract, the local records and the evidence file are built, and the migration still applies because it creates nothing.

**Rollback (RD-P1-045).** Switch `rwb.source-data.decision-cutover` off first; redeploy the previous image tag and chart version only if the flag does not cover the fault, naming in the release note every P1 capability the redeploy reverts. A migration is never reversed and no `U*.sql` or down script exists; a faulty version is corrected by a new forward version. Records already written and events already published are not deleted or rewritten, because the decision record is append only; Kafka consumer offsets are not reset.

**Done when.** The tests of section 16 pass, `rwb_source_data` holds no ledger table, the evidence file lists every legacy `entry_hash` and the last one, no record carries a chain field set by this story, no migrated entry is published while the switch is off, a forced record write publishes nothing and stops with MSG-P7-003, the counter reads ten clean days from the reconciliation results and resets on a break, and no class of the service writes `rwb_decision` or names a `public` table.

### 14. Validation and messages

| ID | Type | When | Message |
|---|---|---|---|
| MSG-P1-001 | Warning | The ACE batch for a business date of the ten clean days is not COMPLETED, so the reconciliation for that date cannot run | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-001 | Error | An entry lacks its case, its decision code, its rule ID, its rule version or its approver | Enter {field}. |
| MSG-P4-002 | Error | The caller's Platform administration right R is absent | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The local decision record or its outbox row cannot be written, so the entry is not recorded and nothing is published | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-012 | Warning | A REC-01 or REC-02 row of a date in the ten is BREAK, raised by the reconciliation and shown here as evidence | The case list for {date} does not reconcile to ALS for {product}: a difference of {variance} accounts, {pct} percent. |

The messages are copied character for character from their sources: MSG-P1-012 from the Error and Message Standard, MSG-P1-001 from the Error and Message Standard (current version v6), and the other three from the legacy story. For MSG-P1-001, {product} is the product code of the source-fed product under test ("DP01" or "DP02") and {date} is its last completed business date. For MSG-GEN-001, {field} is the field name of the refused entry ("case_id", "decision_code", "rule_id", "rule_version" or "approver_user_id"). For MSG-P4-002, {action} is "run the decision-log cutover" or "read the cutover result" and never a decision fact or a field value. For MSG-P7-003, the action is the recording of one entry, and the message is raised before any DecisionRecorded leaves the service, so a caller never sees a decision that was published and not recorded. No other message is raised by this story.

### 15. Screens and states

No screen in this story, and the legacy story states the same: "No screen in this story." The cutover step is not a job of the P1 job set, so SCR-44 Interface and job monitor shows only the `ReconciliationWorkflow` runs behind the clean days (DP-19; H `RWB-PLT-N001-CON`; RD-P1-012). The chain report of the run, the entry list and the clean-day count are read from the cutover record, with the reconciliation results of API-P1-003 published by `RWB-P1-E1011-CON`. The empty, loading, error and no-access states of SCR-44 belong to its console stories and this story defines none.

| State | What the cutover record shows |
|---|---|
| Extracted | The extract read once, the entry count by chain position, every legacy `entry_hash` with the last one, and the orphan list of any person key that resolved to no view row |
| Recorded | The local records written and their outbox rows, with the count and the run's idempotency key |
| Published | Only with the feature switch on: the DecisionRecorded events published in chain order, and any record left in the outbox for retry |
| Stopped | The entry that broke the chain or the write that failed, its chain position, and the stated fact that nothing after it was written or published |
| Ten clean days running | The business dates counted so far, each with the PASS results of its reconciliation |
| Break | The date of the break, its BREAK result rows or its REC-05 orphan, and a count reset to zero |
| Signed off | The count of ten, the sign-off in the cutover record, and the legacy log read-only for its retention period |

A run that cannot start is recorded as FAILED in the cutover record, with the extract and the business date named and no record produced, so a cutover that did not happen is never read as a cutover that happened.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-012-01 | AC1; BR1, BR2, BR6, BR7, BR11 | End to end | The legacy decision-log fixture with five chained entries on an open case, one entry on a person key with no `v_ace_customer` row, and the last legacy `entry_hash`; the decision-record library fake; the rwb-decision contract fake answering the sealed entry with its chain position and both hashes; the record count in `rwb_source_data` before and after; the story's version applied once and again |
| TC-DM-012-03 | AC3; BR5, BR9, BR10 | End to end | The reconciliation fixture with PASS result sets for ten consecutive business dates, then one BREAK set and one new REC-05 orphan on a later date; a business date whose ACE batch is absent; the rwb-decision contract fake answering the migrated entries served from schema "rwb_decision" |
| TC-DM-012-04 | AC5; Access refusal; BR8 | Component | A caller whose Platform administration right is absent in the authorise fake, starting the run and reading the result; a second call with the right present for the contrast; a record count of `rwb_source_data` before and after the refusal |
| TC-DM-012-05 | AC4; Principle 5; BR3 | Component | The library fake switched to fail the local record write on the third entry; the outbox count and the topic before and after; the assertion that no DecisionRecorded is published, the run ends with MSG-P7-003, and the two committed entries are the only ones present |
| TC-DM-012-06 | AC6; BR4; ADR-022 | Component | The library fake holding three migrated entries; switch off: nothing on the topic and the evidence file lists the legacy hashes; switch on: the topic read in order, and a rerun with the same idempotency keys adds nothing |
| TC-DM-012-07 | AC7; BR9, BR10 | Component | The cutover record at nine consecutive clean business dates; the data steward's sign-off attempt; the cutover record state before and after the attempt |
| TC-P1-DM012-APP-01 | AC8; X3, X4 | Component | A five-entry log with a broken `prev_hash` on the third entry |
| TC-P1-DM012-APP-02 | AC9; BR9 | Component | Nine clean dates, then a BREAK, a new orphan and a date with no row |

TC-DM-012-01 and TC-DM-012-03 are End to end because the run leaves the service's own boundary: it reads an extract, resolves keys against views and publishes to a shared topic that another service seals. TC-DM-012-04 and TC-DM-012-05 are Component because they exercise the guard and the record transaction at the boundary of the service. AC2 Reconcile the business keys and its test case belong to `RWB-ITG-DM012-ITG` as `TC-DM-012-02-ITG`, where the chain is proved across the services; the legacy test text of TC-DM-012-02 is not repeated here (ASM-3515). The rows are held in Test Cases v9, tab Story test cases; the AC6 row is to be updated to the batch D text (section 20).

**Cutover reconciliation harness pack.** Agreed at the wave 4 entry check by the Integration lead: the SIT environment and its base hosts per hop are Not specified in the source documents (GAP-0452); the cutover extract fixture holds two cases, three entries and the chain manifest of `prev_hash` and `entry_hash`; the reconciliation extract holds one row per orphan with its reason; the report is produced per business date; the retention matches the wave evidence; the gate fails on any broken link, missing position or unresolved key; one documented point forces the ledger fake to fail. The break-list fields, the extract format and the data seeding set are Not specified in the source documents (GAP-0452).

### 17. Guardrails

- No business value in code: the cutover business date, the extract's location and the retention period are configuration of the release pipeline; the story writes no threshold, no percentage, no currency amount and no date.
- No personal data in logs, tests or prompts: the fixtures are synthetic, and no name, identity number, contact point or address enters a record, an event or a log. `approverUserId` is a user reference; the decision record fields carried on `rwb.decision-record.v1` are classed as Personal data (Data Classification and Personal Data Inventory v5) and are handled as such.
- Personal data in events: DecisionRecorded carries IDs and rule facts only, with no name, identity number, contact point or address; its payload is classed as Personal data (Data Classification and Personal Data Inventory v5).
- ACE data only through the owner's contract or `v_ace_*` views, and here the service is the owner of the views: one login, SELECT only, no `public` table named in any statement (BR8).
- No cross-schema write: the ledger is sealed by rwb-decision through its own consumer, and this story holds no grant on `rwb_decision` and no writer for `decision_log_entry` (BR1; DP-01).
- One transaction, or nothing: a record that cannot be written is not published, and a publish that cannot be made stays in the outbox (BR3; MSG-P7-003).
- The chain is append-only and has one owner: no entry is rewritten, renumbered or re-hashed, a break in the extract stops the run, and this story sets no chain field (BR6, BR7; RD-P1-068; ASM-3513).
- An orphan is listed and never repaired: no migrated entry is deleted or changed to make a key resolve (BR8).
- A break is never waived: a BREAK result or a new REC-05 orphan resets the count, and a date with no result row is never counted as a clean day (BR9; MSG-P1-001).
- The sign-off is an artefact of the release, not a Workbench row: no table is invented for it, and no counter table is invented for the ten days (BR10; ASM-3514).
- One version on the per-service sequence, never edited in place; a later change is a new version with its own history row (DP-15).

### 18. Traceability

| Legacy RWB-DM-012 item | Value (verbatim) | Where it lands | Feature | L3 process |
|---|---|---|---|---|
| Module | P1 Recovery data engine | Service rwb-source-data, service epic RWB-SVC-P1; `decision_log_entry` is P7's and is sealed by rwb-decision | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) |
| Epic | E1, release 30 November 2026 | Wave 4 tag from EP08; release 30 November 2026 (tentative) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) |
| Depends on | RWB-E1-001, RWB-E1-069 | RWB-P1-E1001-APP (the data products and the catalogue of this service) and RWB-P1-E1069-APP (the views and the grant) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) |
| Decision | DL25 | BR9; the ten clean days; DL25 option A applied by RD-P1-042, `recon.tolerance.pct` v1 = 0.00, for Data lead confirmation; ASM-0728, ASM-0735, ASM-0743 confirmed with the tolerance named, ASM-2602 closed | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) |
| Data | recovery_case DF-CAS-001 to DF-CAS-055; decision_log_entry DF-DEC-001 to DF-DEC-031 | Section 2 quotation; section 11; AC1; TC-DM-012-01 | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) |
| Endpoints | No endpoint in this story. The migration is a cutover step run by the recovery service identity, and its breaks are listed on the reconciliation extract. | Section 12.1; API-P1-003 and API-P1-001 are the reads of the breaks and of the run, and belong to other stories | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) |
| Screen and states | No screen in this story. | Section 15; the cutover record holds the result, and SCR-44 shows the reconciliation runs through the gateway-bff composite route | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) |
| Permission checks | Platform administration R for RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Section 10 | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) |
| Guardrails | A migrated record keeps its source and its migration date, and never a copy of an ACE row. | BR2, BR8; AC1; section 17 | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) |
| AC1 and AC3 | Copied character for character into section 7 with the origin tag | Section 7; TC-DM-012-01 and TC-DM-012-03 | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) |
| AC2 and TC-DM-012-02 | Reconcile the business keys, REC-05 | Owned by RWB-ITG-DM012-ITG as TC-DM-012-02-ITG; not copied here | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) |

| Pattern | Source | Applied as | Feature | L3 process |
|---|---|---|---|---|
| DP-03 | Template and Rules §R5.5 | The local decision record and its outbox row written in one transaction through `RWB-PLT-E1027-CON`, and DecisionRecorded on `rwb.decision-record.v1` sealed by rwb-decision (sections 4 and 12.3) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) |
| DP-05 | Template and Rules §R5.5 | The case and person keys are resolved against the views this service owns, on its own login, and an orphan is listed (section 4) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) |
| DP-15 | Template and Rules §R5.5 | One version on the per-service sequence, holding no ledger object and recording the extract, its field list and the chain rule (section 13) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) |
| DP-19 | Template and Rules §R5.5 | The reconciliation runs behind the cutover are read on SCR-44 through the gateway-bff composite route and the story renders no screen (section 15) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) |

| Story | Work type | Relation to this story | Feature | L3 process |
|---|---|---|---|---|
| RWB-PLT-E1027-CON | Contract | H build dependency: the decision-record library, the outbox row and the shared topic | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) |
| RWB-PLT-E1044-CON | Contract | H build dependency: the per-service Flyway sequence and its history | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) |
| RWB-PLT-N001-CON | Contract | H build dependency: the gateway-bff composite route that serves SCR-44 | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) |
| RWB-P1-E1001-APP | App development | H build dependency: the data products and the catalogue the case and person keys resolve against | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) |
| RWB-P1-E1069-APP | App development | H build dependency: the 30 read-only views, the login and the grant | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) |
| RWB-P1-E1011-APP | App development | Builds JOB-04 and writes `reconciliation_result`, which is the cutover evidence | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) |
| RWB-P1-E1002-APP | App development | Builds the account read of the case list rwb-case composes; no `case_list_row` exists in P1 (RD-P1-024) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) |
| RWB-ITG-DM012-ITG | Integration | Owns AC2 and proves the intact chain across the services; its I dependency is this story | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) |
| The rwb-decision ledger consumer and JOB-14 (P7) | App development | Consumes DecisionRecorded into the central ledger and checks the chain at 02:00; the ledger and its checks are P7's | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM012-APP-2) |

External dependencies: None. The story adds no X row of its own.

### 19. Out of scope

- The central ledger, its consumer, its gap alerts, its completeness target and its daily seal: P7 rwb-decision's own work (GAP-2176; ASM-3512).
- JOB-14, the chain check at 02:00, its Temporal Schedule and its alert: rwb-decision.
- AC2 Reconcile the business keys, the cross-service chain proof and its break list: `RWB-ITG-DM012-ITG` owns AC2 and `TC-DM-012-02-ITG` (ASM-3515).
- The decision-record library itself, its store, its outbox, its inbox, its idempotency keys and its relay: `RWB-PLT-E1027-CON`.
- JOB-04, its workflow, its activity, its rerun operation and the `reconciliation_result` rows: `RWB-P1-E1011-APP`.
- The daily case list: rwb-case composes it; P1 has no `case_list_row` and no publish status (RD-P1-024).
- `recovery_case` and the case state machine: P3 rwb-case; this story reads the case keys of the open-case set only.
- The 30 read-only views, the `rwb_source_data` login and its grant, and the boundary test: `RWB-P1-E1069-APP` and `RWB-P1-E1069-DB`.
- The data product catalogue, the dictionary, the data contracts and the access rows: `RWB-P1-E1001-APP`.
- SCR-44 Interface and job monitor and its route: `RWB-P1-AD018-APP`, its CON story and the gateway-bff composite route.
- The retention period itself, the archival of the legacy decision log and the decommissioning of the legacy Workbench: the cutover plan and the data steward, and no source gives the period (GAP-2177; ASM-3514).
- The migration of the other legacy records of the same cutover: `RWB-P1-DM003-APP`, `RWB-P1-DM010-APP`, `RWB-P1-DM011-APP`, `RWB-P1-DM013-APP` and `RWB-P1-DM014-APP`.
- The data lake, INT-19 and INT-20, and the decision-log copy to it (JOB-13): removed with the data lake, and no story of this key needs lake data (DP-17).

### 20. Remaining delivery steps

- Size the story at refinement (owner: squad).
- Record the EP08 epic design sign-off (owner: solution architect).
- Settle how DecisionRecorded carries the legacy `prev_hash`, `entry_hash`, rule ID and rule version; the publish step stays switched off until then (owner: rwb-decision contract owner with compliance; NEW-GAP-S13-4).
- Publish the `decision_record` DDL in the physical schema (owner: platform lead, library owner; NEW-GAP-F08-7), and settle how the library holds unpublished outbox rows while the switch is off (NEW-GAP-G4-1).
- Decide whether migrated decisions are ledgered as interactions and with which actor (owner: solution architect; NEW-GAP-S13-5).
- Agree the extract source, format, location, retention and sign-off place at the wave 4 entry check (owner: data steward; GAP-2177), and the harness environment and break-list fields (owner: integration lead; GAP-0452).
- Bring RWB-PLT-E1027-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON and RWB-P1-E1011-CON to Done and publish the library and rwb-decision fakes at pinned versions (owner: contract owners).
- Update the AC6 test row of Test Cases v9 and the traceability matrix to the batch D text (owner: test lead).
- Load the synthetic fixtures in DEV (owner: squad).
