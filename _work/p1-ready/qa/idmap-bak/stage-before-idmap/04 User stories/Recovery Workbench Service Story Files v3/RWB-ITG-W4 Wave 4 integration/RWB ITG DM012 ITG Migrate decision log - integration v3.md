# RWB-ITG-DM012-ITG Migrate decision log

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes**

- JOB-04 is started by the readiness call as a child of `AceIngestCheck`; the invalid rerun call is removed (RD-P1-012, RD-P1-040; findings #1, #12).
- Migrated entries reach the ledger as `rwb.decision.DecisionRecorded.v1`; keeping their chain is an open conflict (RD-P1-008; NEW-GAP-S13-4; #2).
- Orphans on the real services come from the orphan list of RWB-P1-DM012-APP (RD-P1-022; #3); `migration_source`, `migrated_at` and no publish status (RD-P1-027, RD-P1-024; #9, #10).
- Freshness, readiness, rights, error body and contract version aligned to rwb-source-data.yaml 5.1.0; AC8 added (#4 to #7, #11).
- Finishing pass: test case IDs of Test Cases v9 cited in place of the placeholders.
- A repeated readiness call answers 202 and starts nothing once every due source is stamped and the run has ended (RD-P1-065, register XD-11).
- rwb-decision owns the chain fields, migrated entries stay unpublished behind the DM012 switch until the legacy hashes can be carried (NEW-GAP-S13-4), and `model_version` is carried at act time (RD-P1-068).

| Item | Value |
|---|---|
| Story key | RWB-ITG-DM012-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-DM-012 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP15, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement |
| Depends on (build) | RWB-P1-DM012-APP |
| Contract dependencies | RWB-P1-E1015-CON (readiness and freshness), RWB-P1-E1011-CON (reconciliation result reads), RWB-P1-E1016-CON (data product records); the CON stories of rwb-decision, rwb-case and rwb-access: Not specified in the source documents |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7); rwb-decision, rwb-case and rwb-access 5.1.0 |
| Integration dependencies | RWB-P1-DM012-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-001, RD-P1-004, RD-P1-005, RD-P1-008, RD-P1-011, RD-P1-012, RD-P1-021, RD-P1-022, RD-P1-024, RD-P1-027, RD-P1-040, RD-P1-041, RD-P1-042, RD-P1-065, RD-P1-068 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-DM-012 for the wave 4 cutover reconciliation harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-DM012-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (18 resolved, 8 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3; cutover reconciliation harness aligned to the readiness chain, the decision event name, the migration field mapping and the published reads.

### 1. Story

As a **RW-DATASTEW (data steward)**, I want **a repeatable wave 4 cutover reconciliation harness that proves every decision migrated from outside the Workbench on the open cases keeps its case, its decision code, its rule and model version, its approver and its position in the hash chain, and that lists every orphan business key for the data steward and the ACE team, against the owning services' published contracts and their fakes**, so that **the audit trail is unbroken from the first day after cutover**.

This story builds the harness and the evidence, and nothing else. The real decision records are published by RWB-P1-DM012-APP as `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` and sealed into the central ledger by rwb-decision (RD-P1-008); the reconciliation is JOB-04 of RWB-P1-E1011-APP (RD-P1-022). rwb-decision owns `chain_seq` and `prev_hash`; `model_version` (DF-DEC-006) is carried as the value at act time (RD-P1-068 rules 1 and 2). Pending: carrying the legacy `prev_hash`, `entry_hash`, rule ID and rule version on DecisionRecorded, owner rwb-decision contract owner with compliance, NEW-GAP-S13-4, which blocks the publish step only: until then RWB-P1-DM012-APP builds the extract and the local decision records, publication stays behind its feature switch (off), and the cutover evidence file lists every legacy `entry_hash` and the last legacy hash. The story builds no production endpoint, no table, no workflow, no schedule and no screen; it reads the owning services' published contracts, asserts what they answer, and writes a report per business date. It writes no ledger row of its own, and it never recomputes a hash.

### 2. Business rationale

An audit trail is only worth what its continuity proves. A migrated decision entry that loses its rule version, its approver or its place in the chain cannot be defended afterwards: the entry still exists, the case still opens, and nobody can show that the decision recorded on day one is the decision that was taken. The failure is quiet in exactly the way the legacy story warned about — a migration can report a clean extract while the chain it wrote no longer links, and an entry that is rewritten, renumbered or re-hashed to make the link close is worse than a gap, because it hides the very thing the ledger exists to show. DL25 puts zero tolerance on the migrated data, so the chain is read back through the owner's contract, compared entry by entry, and every unresolved business key is listed with a reason and two owners before wave 4 opens.

The harness is decoupled the way the services are. The central ledger and the rule registry belong to rwb-decision (P7), so the chain is read through P7's published decision-log contract and never from its schema (DP-01); the decision record itself is carried by the local decision-record library and the shared topic `rwb.decision-record.v1`, whose producer is the owner and whose consumer is P7 (DP-03, Architecture v5 slide 28); business keys are resolved only through rwb-source-data's data-product contract (DP-05), never by a direct view read; the migrated entries are loaded by rwb-decision, which owns its schema and Flyway sequence (DP-15); where a screen exists the path is the gateway-bff composite route (DP-19), and this legacy story states that no screen exists. Every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget (DP-11). It carries DL25, ADR-009 and ADR-022 into evidence rather than restating them.

### 3. Preconditions

- The published contracts of P7 rwb-decision (the central decision ledger, read only), P3 rwb-case (the case and its primary person key), P1 rwb-source-data (rwb-source-data.yaml 5.1.0: DP01 and DP02 records, freshness, readiness call and status, reconciliation result reads; fake `fakes/rwb-source-data/5.1.0/`) and P4 rwb-access (authorise) are in the contract registry, and a stub set is generated from each one. The reconciliation result reads are published (`getAdminReconciliationResults`, RD-P1-063 rule 1).
- The harness caller of the readiness call holds Platform administration U; the caller of the record and freshness reads holds Case record R, and of the readiness status and reconciliation result reads Platform administration R. A key field that the record read returns with `masked` true fails the run and is reported.
- The data product catalog holds DP01 Account and arrears and DP02 Customer and party, each with one system of record, so account_key and person_key have one named owner before a key is resolved (FSD P1 v3, A2.2).
- The rwb-decision load of the migrated entries has run in SIT for the business date under test, or the stub of §12.8 answers in its place on Day 1.
- RWB-P1-DM012-APP owns the extract, its key check, the cutover and the clean-day count, and JOB-04 of RWB-P1-E1011-APP owns the reconciliation (RD-P1-022); until it lands, the cutover extract fixture and the reconciliation extract fixture stand in for its output.
- The harness environment and base hosts, the synthetic cutover extract fixture and its field layout, the break-list fields, the extract format and retention, the pass or fail gate, the seeding set and the way a forced ledger failure is injected: Not specified in the source documents (GAP-0452; ASM-0644).
- The synthetic cases, the synthetic keys, the synthetic entry identifiers, the hashes and the business date are held in the fixtures as data, not written in code.
- No build dependency. Day 1, with the stubs in place from the first run; the one wait is RWB-P1-DM012-APP, which replaces its stub and never blocks the lane.

### 4. Flow

1. Harness: loads the cutover extract fixture for business date 2026-11-30. It holds two open cases, RW-2026-000601 with primary_person_key PERS-SYN-000601 and RW-2026-000602 with primary_person_key PERS-SYN-000777, and three decision entries: DL-SYN-0001 and DL-SYN-0002 on case RW-2026-000601 at chain_seq 1 and 2, and DL-SYN-0003 on case RW-2026-000602 at chain_seq 1. On Day 1, before the cutover load is in SIT, the stub of §12.8 returns the same records.
2. Harness: starts the chain for business date 2026-11-30 with `POST /api/recovery/source-data/v1/business-days/{date}/ready` and a UUID `Idempotency-Key` (202), and waits until `AceIngestCheck` has stamped the ALS batch and its child `ReconciliationWorkflow` (`recon-2026-11-30`, JOB-04) has completed, after rwb-case answers its allocation or at 07:15 (RD-P1-040). The harness never reruns JOB-04: `POST /admin/jobs/{jobId}/rerun` takes the run uuid of a FAILED run only (RD-P1-012).
3. Harness: reads each case through `GET /api/recovery/case/v1/cases/{caseId}` and asserts the case number and its primary_person_key.
4. Harness: reads the ledger for each case through `GET /api/recovery/decision/v1/decision-log?caseId={caseId}`, then reads each entry again through `GET /api/recovery/decision/v1/decision-log/{entryId}`, and asserts on every entry its decision_code, rule_id, rule_version, model_version, approver and chain_seq.
5. Harness: compares the chain it read with the chain manifest in the cutover extract fixture: for every entry above chain_seq 1 the prev_hash equals the entry_hash of the entry before it, and every entry_hash equals the one the fixture holds for that entry. The harness compares and never recomputes a hash.
6. Harness: asserts that the entries read are the whole log for the case, that no entry is missing between the lowest and the highest chain_seq, and that the two reads of the same entry return the same values, so an entry rewritten or renumbered between the reads is a failure.
7. Harness: resolves each person_key through `GET /api/recovery/source-data/v1/data-products/DP02/records?caseId={caseId}`, with `GET /api/recovery/source-data/v1/data-products/freshness?product=DP01` for `status`, `businessDate` and `loadedAt`, and reads the break list from the reconciliation extract fixture for the business date, one row per orphan with its reason; it reads the REC rows through `GET /api/recovery/source-data/v1/admin/reconciliation/results?from=2026-11-30&to=2026-11-30`. P1 stores no key-level break row (RD-P1-022): on the real services the orphans are read from the orphan list that the DecisionKeyResolver of RWB-P1-DM012-APP records.
8. Harness: replays the three entries through the local decision-record library (DP-03) into the in-memory ledger fake with the forced-failure stub switched on, and asserts that the replay stops, that MSG-P7-003 is reported, and that no entry is appended and no chain value changes. The replay writes no production row: it is a test-scope vessel for the legacy principle 5 assertion, and the fake is not a service.
9. Harness: repeats the readiness call for the same business date with a new UUID `Idempotency-Key`, asserts no second set of result rows and compares the break list and the counts of cases, decision entries and orphans with the first run. The repeated call answers 202 with the stored state and starts nothing; a second run of the date exists only through the rerun of a FAILED run (RD-P1-065 rule 3, register XD-11).
10. Harness: calls `POST /api/recovery/access/v1/authorise` as a synthetic caller with role RW-OFF and no Platform administration right, and asserts 403 with MSG-P4-002; then sends the readiness call as that caller and asserts 403 with `messageCode` MSG-P4-002, no reconciliation run started and no break row written.
11. Harness: writes one run report per business date, keyed by story and business date, naming the contract version of each hop, whether the hop was a stub or the owner, the entry counts, the chain comparison result, the break rows and the criteria of section 7.

Harness pack (GAP-0452, agreed at the wave 4 entry check): the cutover extract fixture holds two cases, three entries and the chain manifest of prev_hash and entry_hash per entry; the reconciliation extract holds one row per orphan with its reason; the report is written per business date; the gate fails on any broken link, missing chain_seq position or unresolved business key; the ledger fake is forced to fail at the one point set in step 8. SIT environment and base hosts per hop, and the retention of extracts and reports: Not specified in the source documents (GAP-0452).

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case | Covered by |
|---|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no criterion is marked passed | None | TC-DM-012-01-ITG (ITG AC2) | ITG AC2 |
| X2 | The cutover extract fixture lacks a required field on a migrated entry | The run fails and the report names the entry and the missing field; an entry without its chain values is never reported as migrated | None | TC-DM-012-01-ITG (ITG AC2) | ITG AC2 |
| X3 | A prev_hash does not equal the entry_hash of the entry before it | The run fails on AC2 and the report names the two entries, their chain_seq and both values; the harness reports the break and never re-hashes an entry to close it | None | TC-DM-012-01-ITG (ITG AC2) | ITG AC2 |
| X4 | A migrated entry is missing between the lowest and the highest chain_seq of a case | The run fails on AC2 and the report names the case and the missing position, so a gap in the chain is a failure and not a shorter list | None | TC-DM-012-01-ITG (ITG AC2) | ITG AC2 |
| X5 | A person_key has no DP02 row and the reconciliation extract does not list it | The run fails on AC1 and the report names the case, the key type and the key value, so a suppressed break is a failure and not a pass | None | TC-DM-012-02-ITG (ITG AC1) | ITG AC1 |
| X6 | The ALS batch is late (no ALS stamp, so JOB-04 is not started), or the product read answers `status` `STALE` | The readiness status reads `LATE`, or the freshness read answers `STALE` (`businessDate` null when never stamped); the run is reported as not run, never as passed | MSG-P1-001 | Test Cases v9: TC-DM-012-02-ITG, TC-DM-012-09-ITG | ITG AC1, ITG AC8 |
| X7 | The ledger fake refuses the replayed entry | The run stops on AC3, the report names the entry and MSG-P7-003 with its substituted values, and no entry is appended and no chain value changes | MSG-P7-003 | TC-DM-012-05-ITG (ITG AC3) | ITG AC3 |
| X8 | A repeated run lists the same break twice or returns a different count | The run fails on AC2 and the report names the two rows or the two counts and the business date | None | TC-DM-012-01-ITG (ITG AC2) | ITG AC2 |
| X9 | A caller without the Platform administration right starts a run | The run fails on AC4 and the report names the caller role and the operation; a run that started is reported as started | MSG-P4-002 (expected, and missing) | TC-DM-012-04-ITG (ITG AC4) | ITG AC4 |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stubs from Day 1; the only wait is RWB-P1-DM012-APP, and its stub answers until it lands |
| Negotiable | The fixture layout, the break-list fields, the report shape, the gate and the failure-injection point are configuration agreed at the wave entry check, not business values in code |
| Valuable | The chain of every migrated decision is proven through the owner's contract, and every orphan business key is on a list with a reason and two owners, before wave 4 opens |
| Estimable | One runner, one stub set, two fixtures, one chain comparator, one break-list assertion, one failure-injection check and one report |
| Small | Fits in one sprint with its five tests |
| Testable | Each criterion runs against the stubs and again against the real owners as the I story lands |

### 7. Acceptance criteria

```gherkin
Feature: Migrate decision log - wave 4 cutover reconciliation harness

  Background:
    Given the synthetic cutover extract holds open case "RW-2026-000601" with primary_person_key "PERS-SYN-000601" at chain_seq 1 and 2, and open case "RW-2026-000602" with primary_person_key "PERS-SYN-000777" at chain_seq 1
    Given entry "DL-SYN-0001" of case "RW-2026-000601" carries decision_code "ALLOC", rule_id "ALLOC-SYN-01", rule_version "ALLOC-2026.12", model_version "ALLOC-2026.12" and approver "RW-APPR" at chain_seq 1
    Given the DP02 records hold one row for person_key "PERS-SYN-000601" and no row for person_key "PERS-SYN-000777"
    Given ReconciliationWorkflow "recon-2026-11-30" (JOB-04) has completed for business date "2026-11-30" as the child of AceIngestCheck

  Scenario: AC1 Reconcile the business keys (legacy RWB-DM-012 AC2)
    Given the migrated records
    When the harness resolves the keys of the migrated records for business date "2026-11-30"
    Then every business key on a migrated record resolves to its view row, account_key and person_key included
    And each orphan is listed for the data steward and the ACE team: person_key "PERS-SYN-000777" appears with reason "NO_ACE_ROW" in the break list of the reconciliation extract fixture
    And on the real services the orphan is read from the orphan list of RWB-P1-DM012-APP, because rwb-source-data stores no key-level REC-05 row

  Scenario: AC2 The hash chain is intact through the decision contract and a repeated run changes nothing (new, D-RCV-60)
    Given the migrated entries of case "RW-2026-000601" are read through the rwb-decision contract
    When the harness reads the log for the case and then reads each entry by its entryId
    Then each entry keeps its case, its decision_code, its rule_id, its rule_version, its model_version, its approver and its chain_seq
    And for every entry above chain_seq 1 the prev_hash equals the entry_hash of the entry before it
    And every entry_hash equals the value the cutover extract holds for that entry, and no entry is rewritten, renumbered or re-hashed
    And no entry is missing between the lowest and the highest chain_seq of the case
    And after POST /business-days/2026-11-30/ready is called again with a new UUID Idempotency-Key, the call starts nothing (no second ReconciliationWorkflow run), no second set of reconciliation result rows exists and the run for "2026-11-30" returns the same entries in the same positions with the same hashes, lists one break row, returns equal counts of cases, entries and orphans, and leaves one report per business date
    And on the real services the chain assertions are pending the contract that carries a migrated entry with its chain (NEW-GAP-S13-4)

  Scenario: AC3 A forced ledger write failure stops the run with MSG-P7-003 (new, D-RCV-60)
    Given the ledger fake of the replay is set to fail on the next append
    When the harness replays entry "DL-SYN-0001" through the local decision-record library
    Then the run stops before any criterion is marked passed and the report holds "MSG-P7-003"
    And no entry is appended and no chain_seq, prev_hash or entry_hash in the ledger changes
    And the report names the entry that could not be recorded and the ledger as the hop that refused

  Scenario: AC4 A caller without the platform administration right is refused (new, D-RCV-60)
    Given a synthetic user with role "RW-OFF" and no Platform administration right
    When that user calls POST /business-days/2026-11-30/ready with a UUID Idempotency-Key
    Then the answer is 403 with a problem body whose messageCode is "MSG-P4-002"
    And no reconciliation run starts and no break row is written

  Scenario: AC5 Each migrated record keeps its migration_source and its migrated_at and the harness migrates nothing (new, D-RCV-60)
    Given the migrated records of an open case carry migration_source and migrated_at
    When the harness reads the case through the rwb-case contract and the entries through the rwb-decision contract
    Then each migrated record keeps its migration_source and its migrated_at
    And the harness reads no schema, applies no Flyway sequence and writes no row

  Scenario: AC6 Zero tolerance keeps wave 4 closed while one break or one orphan is listed (new, D-RCV-60)
    Given the reconciliation for a business date lists at least one break row or one orphan
    When the harness completes the run
    Then the report marks wave 4 as not open, with a clean-day count of 0 and sign-off not open, and no criterion is marked passed
    And wave 4 stays closed while the break row or the orphan remains listed, and no publish status is read from rwb-source-data

  Scenario: AC7 A consumed call that fails or does not answer stops the run and is reported (new, D-RCV-60)
    Given the DP02 record read fake answers 503 with messageCode "MSG-GEN-006", or does not answer within 2 s
    When the harness makes that call
    Then the run stops before any criterion is marked passed and the report names the hop that failed
    And no break row, decision entry or migrated record is written because of the failed call

  Scenario: AC8 A late or never stamped batch is reported as not run (new, RD-P1-040, RD-P1-041)
    Given the readiness status fake answers status "LATE" for business date "2026-11-30"
    And the freshness fake answers DP01 with status "STALE" and businessDate null
    When the harness runs for business date "2026-11-30"
    Then the run report records "not run" with DP01, the business date and "MSG-P1-001"
    And no key is resolved, no break row is asserted and the run is not marked passed
```

Legacy AC1 and AC3 belong to RWB-P1-DM012-APP, and the eight criteria above are the ones this ITG story owns.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every decision entry migrated from outside the Workbench keeps its case, its decision code, its rule and model version, its approver and its position in the chain | Legacy RWB-DM-012 AC1; DL25 |
| BR2 | Every entry is append-only: no entry is rewritten, renumbered or re-hashed, and a broken link is reported and never repaired in place | Legacy RWB-DM-012 AC1; DL25 |
| BR3 | Every business key on a migrated record resolves to its ACE view row before the record is served, and every break is listed with a reason and never suppressed | Legacy RWB-DM-012 AC2 |
| BR4 | A decision that cannot be recorded is not taken: the step stops and the caller is told, rather than carrying on without the record | Legacy RWB-DM-012, principle 5; MSG-P7-003; R-UNI-39 |
| BR5 | The central ledger and the rule registry belong to rwb-decision, read through its contract and never from its schema; the local record and the shared topic belong to the owner | ADR-009; ADR-022; DP-01; DP-03 |
| BR6 | Each service applies its own Flyway sequence in its own schema, and the migrated records keep their `migration_source` and `migrated_at` | DP-15; ADR-021; legacy RWB-DM-012 guardrails; RD-P1-027 |
| BR7 | Zero tolerance: wave 4 does not open while one migrated entry breaks the chain or one migrated key has no view row | DL25; DL25 option A applied by RD-P1-042, `recon.tolerance.pct` v1 = 0.00; no P1 publish status (RD-P1-024) |

The harness asserts these rules and changes none of them.

Historical decision entries are published by RWB-P1-DM012-APP as `rwb.decision.DecisionRecorded.v1` on rwb.decision-record.v1 in chain order (RD-P1-008), each with its original chain_seq, prev_hash and entry_hash; rwb-decision seals them into the central ledger, and RWB-P1-DM012-APP writes no decision_log_entry row. Pending: the published event schema carries no chain field and has rwb-decision assign the chain, so the contract that keeps the original chain is open (NEW-GAP-S13-4, owner rwb-decision contract owner with compliance). Interim: publication of migrated entries stays behind the DM012 feature switch (off) and the cutover evidence file lists every legacy `entry_hash` and the last legacy hash; rwb-decision alone sets `chain_seq` and `prev_hash` (RD-P1-068 rule 1). The harness reads them only through the rwb-decision contract.

Coverage: BR1, BR2 and BR5 are asserted by ITG AC2 (TC-DM-012-01-ITG); BR3 by ITG AC1 (TC-DM-012-02-ITG); BR4 by ITG AC3 (TC-DM-012-05-ITG); BR6 by ITG AC5 (TC-DM-012-06-ITG); BR7 by ITG AC6 (TC-DM-012-07-ITG).

DL25 option A is applied by RD-P1-042 pending the data lead's confirmation. Its assumptions ASM-0728, ASM-0735, ASM-0743 and ASM-2602 are confirmed by the programme directive of 26 November 2026, and BR1, BR2 and BR7 rest on DL25.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| The migrated chain, linked with no gap | The chain is read for the business date | `recon-2026-11-30` completes and every prev_hash matches the entry_hash before it | The migrated chain, linked with no gap, unchanged; the report holds the comparison |
| The migrated chain, linked with no gap | A forced failure on the replayed append | The ledger fake refuses the entry | The migrated chain, linked with no gap, unchanged, and the run stops with MSG-P7-003 |
| The migrated chain, linked with no gap | An entry between two positions is missing | The read returns a chain_seq with no entry | The migrated chain, linked with no gap, unchanged, and the gap is reported as a failure |
| The migrated chain, linked with no gap | An orphan is listed and later resolves | A DP02 row appears for the key and the reconciliation of a later business date runs, or a FAILED run of the date is rerun | The break is no longer listed; the entry is unchanged and is not re-hashed |

The harness changes no state. Every change in the table is made by the owner: P1 rwb-source-data writes the reconciliation result and publishes the migrated decision records, P7 rwb-decision collects the decision records into the central ledger and checks the chain, and P4 rwb-access answers the authorisation. The harness reads, asserts and reports; a state it had set by hand would prove nothing, so the report names the owner and the operation behind every value it asserts.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward | Reads the reconciliation result for a business date; holds Platform administration R and Case record R; owns the break list with the ACE team and signs off the migrate. Does not start or rerun a run |
| Harness caller | Holds Platform administration U for the readiness call, Platform administration R for the status and result reads and Case record R for the record and freshness reads |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Read the same chain evidence and the same break list; each holds Platform administration R |
| QA lead | Owns the harness configuration, the fixtures, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | P1 rwb-source-data runs JOB-04 as a child of `AceIngestCheck` and writes the reconciliation result, P7 rwb-decision collects the ledger and checks the chain at 02:00, P3 rwb-case holds the case and its person key, and P4 rwb-access answers the authorisation; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; the DoA table of rwb-access is reference data it does not change, and authorisation is answered by rwb-access |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018, DF-DEC-028 to DF-DEC-031 | decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version, approver | Read through the rwb-decision contract |
| DF-DEC-001 to DF-DEC-018, DF-DEC-028 to DF-DEC-031 | decision_log_entry | chain_seq, prev_hash, entry_hash, decided_at, final_call, outcome | Read through the rwb-decision contract, compared and never recomputed |
| DF-CAS-001 to DF-CAS-023, DF-CAS-046 to DF-CAS-055 | recovery_case | case_no, primary_person_key, status | Read through the rwb-case contract |
| Standard column | recovery_case, decision_log_entry | migration_source, migrated_at (RD-P1-027) | Read through the rwb-case and rwb-decision contracts |

Field IDs are those in the Logical Data Model and Data Dictionary v9. Both tables are owned elsewhere — decision_log_entry by P7 rwb-decision and recovery_case by P3 rwb-case — and the harness reads them only through the published contracts. The record shape it asserts is the decision record of the Temporal and Drools design: chain_seq, inputsRef, ruleId, ruleVersion, recommendation, approverUserId, approvalLevel, finalCall, actions, outcome, decidedAt, prev_hash and entry_hash, append-only and hash-chained, with JOB-14 checking the chain at 02:00 (Temporal and Drools Detailed Design v1, slide 16). The ACE side of the keys is DP01 Account and arrears for account_key and DP02 Customer and party for person_key, read through the rwb-source-data data-product contract, never from a view and never from a table. The harness owns no table and writes no row. Lists and parameters the harness reads go through the reference-data contract under DP-06 and DP-07; the parameter keys are Not specified in the source documents (DOR-RWB-ITG-DM012-ITG-20).

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | The entries of the central decision ledger for the case, in chain_seq order (AC1, AC2) |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | P7 rwb-decision | One entry read again by its entryId, so a rewrite between the two reads is a failure (AC2, AC3) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | Case number and primary_person_key of the open case (AC1, AC2) |
| GET | `/api/recovery/source-data/v1/data-products/{productCode}/records?caseId={caseId}` | P1 rwb-source-data | The DP02 party rows that resolve person_key, and the DP01 account rows the cases link (AC1) |
| GET | `/api/recovery/source-data/v1/data-products/freshness?product=DP01` | P1 rwb-source-data | `status`, `businessDate` and `loadedAt` of the product (AC1, AC8) |
| POST | `/api/recovery/source-data/v1/business-days/{date}/ready` | P1 rwb-source-data | Start `AceIngestCheck`, whose child is JOB-04, with a UUID `Idempotency-Key`; 202 (AC1, AC2, AC4) |
| GET | `/api/recovery/source-data/v1/business-days/{date}/status` | P1 rwb-source-data | `RUNNING`, `DONE` or `LATE` for the business date (AC8) |
| GET | `/api/recovery/source-data/v1/admin/reconciliation/results` | P1 rwb-source-data | The REC rows of the business date (AC1, AC6); pending in the yaml file (RWB-P1-E1011-CON) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The Platform administration right and the refusal path (AC4) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). Every error of rwb-source-data is an `application/problem+json` body with `messageCode` (RD-P1-004). No operation is invented in this story: each path is the owner's published operation, and where a screen would compose them the path would be the gateway-bff composite route (DP-19).

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

None. The shared topic `rwb.decision-record.v1`, carrying `ce_type` `rwb.decision.DecisionRecorded.v1` (RD-P1-008), is the DP-03 transport of the decision record: the owning service writes it and P7 rwb-decision collects it into the central ledger within 5 minutes (Architecture v5 slide 28). The harness reads no event from that topic; it reads the collected result through P7's contract and starts JOB-04 through the readiness call.

#### 12.5 Workflows and activities

None added. Two workflows of the owners are touched, and neither is created, changed or triggered by this story beyond what is written here. JOB-04, `ReconciliationWorkflow` on rwb-source-data (Architecture v5 slides 15 and 44), workflow ID `recon-{businessDate}`, runs as the child of `AceIngestCheck` (RD-P1-040) and is exercised through the readiness call. JOB-14 hash-chain check, the Temporal Schedule that runs at 02:00 on rwb-decision (Architecture v5 slide 44), is read only: no published operation starts it, so the harness does not start it, does not claim to have run it, and asserts on the chain the same properties the check asserts — every entry linked to the one before, no gap, nothing rewritten.

#### 12.6 Schedules

None. JOB-04 runs as a child of `AceIngestCheck` and JOB-14 is rwb-decision's own Schedule at 02:00; the harness sets no cron and starts nothing on a timer.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); decision_log_entry is P7's and recovery_case is P3's, and the harness writes no ledger row.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-decision | `GET /decision-log?caseId={caseId}` and `GET /decision-log/{entryId}` of §12.2 | The three entries DL-SYN-0001, DL-SYN-0002 and DL-SYN-0003 with their chain_seq, prev_hash and entry_hash exactly as the cutover extract fixture holds them |
| Stub for rwb-case | `GET /cases/{caseId}` | Case RW-2026-000601 with primary_person_key PERS-SYN-000601 and case RW-2026-000602 with primary_person_key PERS-SYN-000777 |
| Stub for rwb-source-data | `fakes/rwb-source-data/5.1.0/`: the P1 operations of §12.2 | DP02 returns one row for PERS-SYN-000601 and none for PERS-SYN-000777, DP01 returns the account rows of the two cases, freshness returns `status` LOADED, business date 2026-11-30 with a load time, the readiness call answers 202, the status answers DONE, and the result read returns the REC rows of the date |
| Stub for rwb-access | `POST /authorise` | Allows RW-DATASTEW with Platform administration R; refuses RW-OFF with 403 and MSG-P4-002 |
| Cutover extract fixture | The migrated records of the legacy story, with the chain manifest | Two cases, three entries with decision_code, rule_id, rule_version, model_version, approver and chain_seq, and the prev_hash and entry_hash of each entry, plus migration_source and migrated_at |
| Reconciliation extract fixture | The break list of the reconciliation | One row for case RW-2026-000602 with key type PERSON, key value PERS-SYN-000777, reason NO_ACE_ROW, owner role RW-DATASTEW and the ACE team as second owner |
| Forced-failure ledger stub | The in-memory ledger fake of the replay, not a service and not an operation | Refuses the next append and answers MSG-P7-003, so the run stops with no entry appended and no chain value changed |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The harness environment and base hosts, the fixture layout, the break-list fields, the extract format and retention, the gate, the seeding set and the injection point of the forced failure are Not specified in the source documents (GAP-0452; ASM-0644).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 9 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published and none consumed; `rwb.decision-record.v1` is the owner's transport into the ledger, read back through P7's contract (DP-03) |
| Temporal | None added; JOB-04 `ReconciliationWorkflow` is exercised as the child of `AceIngestCheck` and JOB-14 chain check is read only, never started |
| File | The cutover extract fixture and the reconciliation extract fixture, both read as files |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies in the table above (RWB-PLT-E1027-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON) are delivered by the platform waves and are recorded here only: they are not repeated in the metadata H field of this story, which stays empty as the plan requires. The one blocking dependency is the I story RWB-P1-DM012-APP, which replaces its stub; until it is live the run uses the stub, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the criteria of section 7 in order for a business date and holds the run lock |
| StubSet | Fake | The four service stubs of §12.8 generated from the published contracts, with the contract version pinned |
| CutoverExtractFixture | Fixture | The two synthetic cases, their person keys, the three entries and the chain manifest of prev_hash and entry_hash |
| Reconciler | Service | Sends the readiness call, resolves each person_key through DP02 with the freshness read, and names each key that does not resolve |
| ChainComparator | Service | Compares the chain read through P7's contract with the chain manifest: link by link, position by position, two reads of each entry, and never a recomputed hash |
| LedgerReplayFailureCheck | Service | Replays an entry through the local decision-record library into the in-memory ledger fake with the forced failure on, and asserts the stop and MSG-P7-003 |
| BreakListAssertion | Service | Compares the read result with the reconciliation extract fixture: one row per orphan, its reason and its two owners, and one row only on a repeated run |
| EvidenceReport | Service | Writes one report per business date keyed by story, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real services as the I story lands, on the synthetic cases RW-2026-000601 with primary_person_key PERS-SYN-000601 and RW-2026-000602 with primary_person_key PERS-SYN-000777, the synthetic entries DL-SYN-0001, DL-SYN-0002 and DL-SYN-0003, the synthetic approver RW-APPR and business date 2026-11-30. In SIT the records come from the rwb-decision load of the published decision records (NEW-GAP-S13-4). The environment and base hosts, the fixture layout, the break-list fields, the extract format and retention, the gate, the seeding set and the injection point of the forced failure are Not specified in the source documents (GAP-0452; ASM-0644). The harness seeds nothing by hand and never writes a schema row.

**Build steps**

1. Generate the four stubs from the published contracts and pin each contract version in the run report; fail the run on a mismatch (X1).
2. Build the CutoverExtractFixture with the two cases, the three entries and the chain manifest, and prove it is read for business date 2026-11-30 (X2).
3. Build the JourneyRunner for AC1: send the readiness call with a UUID Idempotency-Key, wait for `recon-2026-11-30`, read each case through rwb-case, resolve person_key through DP02 with the freshness read, and list each orphan (X5, X6).
4. Add the ChainComparator for AC2: read the log per case and each entry by its entryId, assert the kept fields and the chain_seq, compare every prev_hash with the entry_hash before it and every entry_hash with the fixture, assert no gap and no rewrite between the two reads (X3, X4).
5. Add the determinism check: repeat the readiness call for the same business date, assert the same entries in the same positions with the same hashes, one break row, equal counts of cases, entries and orphans, and one report entry per business date (X8).
6. Add AC3: the LedgerReplayFailureCheck with the forced-failure ledger stub, asserting the stop, MSG-P7-003 with its substituted values, no appended entry and no changed chain value (X7).
7. Add the access path for AC4 through `POST /api/recovery/access/v1/authorise`, then the BreakListAssertion, the EvidenceReport and the gate, and swap a stub for the real owner as its I story lands (X9).

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-P1-DM012-APP when it lands, and the wave entry check holds a run report keyed by story and business date that names every entry compared, every break row and the result of the chain comparison.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text.

### 15. Screens and states

The legacy story has no screen, and neither does this harness: the chain comparison and the breaks are read from the extracts, which the data steward and the ACE team read as files. The decision center and its log screen belong to P7 rwb-decision and are not part of this legacy key; the harness reads the same entries through the published contract and renders nothing.

| State | What the report and the extract hold |
|---|---|
| Chain intact, no break | One line for the business date with the counts of cases, entries and orphans, the chain comparison agreeing entry by entry, and no break row |
| Chain intact, break | One row per orphan with the case number, the key type, the key value, the reason, the data steward and the ACE team as owners |
| Chain broken | The run fails and the report names the two entries, their chain_seq, the two hash values and the case; the entry is never repaired or re-hashed to close the gap |
| Run stopped | The report names the entry that could not be recorded, the ledger as the refusing hop and MSG-P7-003, and holds no passed criterion |

The harness renders no screen. What the wave entry check looks at is the run report, whose environment, layout, format and retention are Not specified in the source documents (GAP-0452; ASM-0644).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-012-01-ITG | AC1 (legacy, owned by RWB-P1-DM012-APP); ITG AC2 | Integration | Two cases, three entries, the chain manifest with prev_hash and entry_hash per entry, business date 2026-11-30 |
| TC-DM-012-02-ITG | AC2 (legacy); ITG AC1 | Integration | person_key PERS-SYN-000777 with no DP02 row on case RW-2026-000602 |
| TC-DM-012-03-ITG | AC3 (legacy, owned by RWB-P1-DM012-APP); ITG AC2 | Integration | Ten clean days on the migrated records; the cutover assertions are RWB-P1-DM012-APP's |
| TC-DM-012-04-ITG | Access; ITG AC4 | Component | RW-OFF caller without Platform administration R |
| TC-DM-012-05-ITG | Principle 5; ITG AC3 | Component | The forced-failure ledger stub on the replay of entry DL-SYN-0001 |
| TC-DM-012-06-ITG | BR6; ITG AC5 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-DM012-ITG-AC5) |
| TC-DM-012-07-ITG | BR7; ITG AC6 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-DM012-ITG-AC5) |
| TC-DM-012-08-ITG | ITG AC7 (new, D-RCV-60); a consumed call that fails or does not answer | Integration | Not specified in the source documents (NEWAC-RWB-ITG-DM012-ITG-AC6) |
| TC-DM-012-04-ITG, TC-DM-012-06-ITG, TC-DM-012-07-ITG, TC-DM-012-08-ITG, TC-DM-012-09-ITG, TC-DM-012-02-ITG, TC-DM-012-01-ITG, TC-DM-012-03-ITG | New ITG AC8 and the changed assertions of ITG AC1, AC2, AC4 to AC7 | Integration | Values of section 7 |

The Covers column names the legacy AC or test the copy derives from and the ITG AC it asserts; the cutover copy names RWB-P1-DM012-APP as the owner of the cutover assertions, which this harness does not restate. The full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx under the same legacy test case ID.

### 17. Guardrails

- No business value in code: the synthetic cases, keys, entry identifiers, hashes, approver, decision codes, rule identifiers, versions and the business date are data.
- No personal data in logs, fixtures or reports: every key is synthetic and no customer record is read at all.
- No read of another service's schema and no direct view read: the chain comes from rwb-decision, the case from rwb-case and the ACE side from the rwb-source-data contract (DP-01, DP-05).
- No entry is ever rewritten, renumbered or re-hashed by the harness or by a report; a broken link is reported and fixed in the owner's data, never closed by recomputing a hash.
- No ledger row is written and no production table is touched: the failure path runs against an in-memory fake in the test scope only (DP-01, DP-03).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11).
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never writes a row by hand.
- A failing criterion is fixed in the service that owns it or reported as a gap; it is never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-DM-012 Migrate decision log | Recovery Workbench Data Migration Stories v3, lines 800 to 878 | Sections 1, 3, 11 and 19 of this file |
| Legacy AC2 Reconcile the business keys, verbatim | The same, lines 825 to 829 | Section 7, AC1, marked (legacy RWB-DM-012 AC2) |
| Legacy AC1 Extract the Workbench records and AC3 Cut over | The same, lines 819 to 823 and 831 to 835 | Stay with RWB-P1-DM012-APP (section 19); AC1 is read back here as the chain evidence of ITG AC2 |
| Legacy test cases TC-DM-012-01 to TC-DM-012-05 | The same, lines 868 to 876 | Section 16, copied as -ITG |
| Legacy message table, MSG-P1-001, MSG-GEN-001, MSG-P4-002 and MSG-P7-003 | The same, lines 859 to 866 | Section 14 |
| DF-DEC-001 to DF-DEC-031 and DF-CAS-001 to DF-CAS-055 | Logical Data Model and Data Dictionary v9 | Section 11 |
| DL25, zero tolerance on the migrated data | Decision Log, DL25 | Section 8, BR1, BR2 and BR7 |
| The decision record shape: chain_seq, inputsRef, ruleId, ruleVersion, recommendation, approverUserId, approvalLevel, finalCall, actions, outcome, decidedAt, prev_hash, entry_hash | Temporal and Drools Detailed Design v1, slide 16 | Sections 7 and 11 |
| JOB-14 hash-chain check at 02:00 and the daily ledger seal to WORM | Architecture v5 slide 28 and the job map on slide 44 | Sections 12.5 and 13 |
| ADR-009 and ADR-022, local record plus central ledger | Decision Log; ADR-022 | Section 8, BR5; sections 12.3 and 12.4 |
| DP-03, DP-05, DP-15 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application |
| The harness gap and assumption | This file, the missing environment, fixture and gate values | Sections 3, 12.8, 13 and 15, where the placeholder names the pair |

### 19. Out of scope

- RWB-P1-DM012-APP: the extract, its key check and orphan list, the cutover and legacy AC1 and AC3. The reconciliation is JOB-04 of RWB-P1-E1011-APP (RD-P1-022), and the real entries are published by RWB-P1-DM012-APP as `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` and sealed into the central ledger by rwb-decision (RD-P1-008).
- P1 production code and its CON, APP and DB stories, and the tables of `rwb_source-data`; P7 production code, its CON and APP stories, the central ledger, the rule registry, the approvals and the daily WORM seal; P3 production code and its case tables; P4 production code and the DoA table.
- The decision center and its log screen on rwb-decision.
- The strict-mode behaviour of points of no return, which belongs to the services that own those steps and not to this legacy key.
- The retention period of the legacy tables, the ten clean days and the data steward sign-off of legacy AC3.
- ACE ingestion and the 30 views (RWB-ACE-001).
- Platform deployment and configuration, and the go-live cutover rehearsal.
- The other four data migration keys of this wave.

### 20. Remaining delivery steps

- Size the story (RW-TRIBE).
- Record the signed epic design of EP08 (product owner).
- Publish the rwb-source-data 5.1.0 fake and add the reconciliation result reads to the yaml file (rwb-source-data contract owner).
- Settle the break-detail store (rwb-source-data data architect; GAP-1508, NEW-GAP-S2B-03).
- Fix the contract that carries a migrated decision entry into the central ledger with its legacy hashes (rwb-decision contract owner with compliance; NEW-GAP-S13-4; blocks the publish step only, RD-P1-068).
- Add the authorise path to the rwb-access yaml (rwb-access contract owner).
- Provide the stubs and synthetic fixtures in DEV (integration lead).
- Add the new and changed test case rows in Test Cases v9 and the Requirements Traceability Matrix (test writer).
