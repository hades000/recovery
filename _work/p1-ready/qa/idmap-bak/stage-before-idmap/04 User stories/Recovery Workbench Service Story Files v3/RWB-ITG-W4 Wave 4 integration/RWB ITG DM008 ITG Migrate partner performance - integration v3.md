# RWB-ITG-DM008-ITG Migrate partner performance

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes**

- JOB-04 is started by the readiness call as a child of `AceIngestCheck`; the invalid rerun call is removed (RD-P1-012, RD-P1-040; findings #1, #14).
- S9 rwb-partner loads its own tables; carried fields include `status`, `result_code`, `fee_amount`, `migration_source` and `migrated_at` (RD-P1-021, RD-P1-027; #8 to #10).
- The key listing on the real services is pending (GAP-1508, NEW-GAP-S2B-03; #3), and so is the person rule of `identity_ref` (NEW-GAP-F07-01; #2); no publish status (RD-P1-024; #11).
- Freshness, readiness, rights, error body and contract version aligned to rwb-source-data.yaml 5.1.0; AC11 added (#4 to #7, #12, #13).
- Finishing pass: test case IDs of Test Cases v9 cited in place of the placeholders.
- A repeated readiness call answers 202 and starts nothing once every due source is stamped and the run has ended (RD-P1-065, register XD-11).
- The reconciliation result reads are cited as published in rwb-source-data.yaml 5.1.0 (`getAdminReconciliationResults`, RD-P1-063).

| Item | Value |
|---|---|
| Story key | RWB-ITG-DM008-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-DM-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP15, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Size | Sized by the squad at refinement |
| Depends on (build) | RWB-P1-DM008-APP (build not done; also named as integration dependency) |
| Contract dependencies | RWB-P1-E1015-CON (readiness and freshness), RWB-P1-E1011-CON (reconciliation result reads), RWB-P1-E1016-CON (data product records); no contract story is named for rwb-partner, rwb-case or rwb-access; POST /api/recovery/access/v1/authorise is still to be published in rwb-access (see CG-ALL-1024) |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7); rwb-partner, rwb-case and rwb-access 5.1.0 |
| Integration dependencies | RWB-P1-DM008-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-001, RD-P1-004, RD-P1-005, RD-P1-011, RD-P1-012, RD-P1-021, RD-P1-022, RD-P1-024, RD-P1-027, RD-P1-040, RD-P1-041, RD-P1-042, RD-P1-065, RD-P1-063 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-DM-008 for the wave 4 cutover reconciliation harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-DM008-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (18 resolved, 8 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3; cutover reconciliation harness aligned to the readiness chain, the migration field mapping and the published reads.

### 1. Story

As a **RW-DATASTEW, data steward**, I want **a repeatable wave 4 cutover reconciliation harness that proves every business key on the migrated partner, partner user and partner instruction records resolves through rwb-source-data's data-product contract and lists every orphan with its reason and two owners, against the owning services' published contracts and their fakes**, so that **panel status and performance continue across cutover from the first day after it**.

This story builds the harness and the evidence, and nothing else. The real firms, their users and their instructions are handed over by the RWB-P1-DM008-APP extract and loaded by S9 rwb-partner into `rwb_partner` on S9's own Flyway sequence (DP-15; RD-P1-021, RD-P1-027), and the reconciliation that produces the breaks is RWB-P1-DM008-APP's. The story is a test package and is not part of any deployed service: it builds no production endpoint, no table, no workflow, no schedule and no screen; it reads the owning services' published contracts, asserts what they answer, and writes one report per business date.

### 2. Business rationale

A panel firm served on the first day with a partner_code, an identity_ref or an instruction case that resolves to no row loses the panel status and the performance that the recovery process routes on. The panel offers work to a firm that the record no longer evidences, the instruction moves with a case that nobody can open, and the score behind the ranking points at a firm the ACE views do not hold. The failure is quiet: the cutover load can report a clean run while the keys it wrote point at rows that the views do not hold, and a break that nobody lists is a silent data loss that surfaces weeks later as a misplaced instruction or a wrong panel measure. DL25 puts zero tolerance on that, so the migrated partner, partner user and partner instruction records are proven before the cutover is called done, and every orphan is on a list with a reason and two owners.

The harness is decoupled the way the services are. ACE data is read only through rwb-source-data's data-product contract (DP-05), never from another service's schema and never by a direct view read (DP-01); the panel firms and their instructions are read from rwb-partner, which owns partner, partner_user and partner_instruction; the case behind an instruction is read from rwb-case, which owns recovery_case; the cutover load runs on S9's own Flyway sequence (DP-15); where a screen exists the path is the gateway-bff composite route (DP-19), and the legacy story names the SCR-45 Data quality console, which this harness neither builds nor calls, so it renders no screen; every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget (DP-11). It carries REQ-RDF-007, REQ-RDF-008 and DL25 into evidence rather than restating them.

### 3. Preconditions

- The published contracts of S9 rwb-partner (partners and instructions), P3 rwb-case (case), P1 rwb-source-data (rwb-source-data.yaml 5.1.0: DP01 and DP02 records, freshness, readiness call and status, reconciliation result reads; fake `fakes/rwb-source-data/5.1.0/`) and P4 rwb-access (authorise) are in the contract registry, and a stub set is generated from each one. The reconciliation result reads are published (`getAdminReconciliationResults`, RD-P1-063).
- The harness caller of the readiness call holds Platform administration U; the caller of the record and freshness reads holds Case record R, and of the readiness status and reconciliation result reads Platform administration R. A key field that the record read returns with `masked` true fails the run and is reported.
- The data product catalog holds DP01 Account and arrears and DP02 Customer and party, each with one system of record, so person_key and account_key have one named owner before a key is resolved (FSD P1 v3, A2.2).
- The S9 rwb-partner cutover load, on S9's own Flyway sequence (DP-15), has run in SIT for the business date under test, or the stub of §12.8 answers in its place on Day 1.
- JOB-04 of RWB-P1-E1011-APP owns the reconciliation (RD-P1-022) and RWB-P1-DM008-APP owns the extract and the clean-day count; until they land, the reconciliation extract fixture stands in for its output.
- The harness environment and base hosts, the synthetic cutover extract fixture and its field layout, the break-list fields, the extract format and retention, and the pass or fail gate with its seeding set: Not specified in the source documents (GAP-0448; ASM-0640).
- The synthetic firm, the synthetic users, the synthetic instruction, the field values and the business date are held in the fixture as data, not written in code.
- No build dependency. Day 1, with the stubs in place from the first run; the one wait is RWB-P1-DM008-APP, which replaces its stub and never blocks the lane.

### 4. Flow

1. Harness: loads the cutover extract fixture for business date 2026-11-30: panel firm "PART-SYN-0008" with partner_name, partner_type, panel_status, contract_end and score, its user with identity_ref "PERS-SYN-000808", role_code, valid_from and valid_to, its second user with identity_ref "PERS-SYN-000818", and the instruction "INS-SYN-0008" on case "RW-2026-000801" with instruction_type, instructed_at, due_at and its result. On Day 1, before the cutover load is in SIT, the stub of §12.8 returns the same records.
2. Harness: starts the chain for business date 2026-11-30 with `POST /api/recovery/source-data/v1/business-days/{date}/ready` and a UUID `Idempotency-Key` (202), and waits until `AceIngestCheck` has stamped the ALS batch and its child `ReconciliationWorkflow` (`recon-2026-11-30`, JOB-04) has completed, after rwb-case answers its allocation or at 07:15 (RD-P1-040). The harness never reruns JOB-04: `POST /admin/jobs/{jobId}/rerun` takes the run uuid of a FAILED run only (RD-P1-012).
3. Harness: reads the panel firms through `GET /api/recovery/partner/v1/partners` and asserts partner_code, partner_name, partner_type, panel_status, contract_end and score against the fixture.
4. Harness: reads the instructions through `GET /api/recovery/partner/v1/partner/instructions` and asserts instruction_type, instructed_at, due_at, status, result_code and fee_amount, `migration_source` and `migrated_at`, and that each instruction names its case.
5. Harness: reads the case behind the instruction through `GET /api/recovery/case/v1/cases/{caseId}` and asserts the case number against the fixture.
6. Harness: resolves each business key through `GET /api/recovery/source-data/v1/data-products/{productCode}/records?caseId={caseId}`, person_key from identity_ref through DP02 and account_key from the instruction's case through DP01, with `GET /api/recovery/source-data/v1/data-products/freshness?product=DP01` for `status`, `businessDate` and `loadedAt`, and names each key that does not resolve. The record read is per case and returns rows of `fields` with `fieldName`, `value` and `masked`. Pending: whether `partner_user.identity_ref` is a person_key resolved against DP02, because RD-P1-027 carries it as a Workbench field and not as an ACE key and a firm user is not a party of a case, owner data architect with the rwb-partner service owner (NEW-GAP-F07-01).
7. Harness: reads the break list from the reconciliation extract fixture for the business date, with one row per orphan and its reason, and reads the REC rows through `GET /api/recovery/source-data/v1/admin/reconciliation/results?from=2026-11-30&to=2026-11-30`; the legacy story states that the breaks are listed on the reconciliation extract and that there is no screen. P1 stores no key-level break row and the REC-05 scope holds no partner key (RD-P1-022): on the real services the key listing is pending the break-detail store (GAP-1508, NEW-GAP-S2B-03).
8. Harness: asserts that no case record is duplicated and that no settlement figure sits on a migrated instruction record or in the cutover extract, and names the instruction and the field where one does.
9. Harness: repeats the readiness call for the same business date with a new UUID `Idempotency-Key`, asserts no second set of result rows and compares the break list and the counts of firms, partner users, instructions and break rows with the first run. The repeated call answers 202 with the stored state and starts nothing; a second run of the date exists only through the rerun of a FAILED run (RD-P1-065 rule 3, register XD-11).
10. Harness: calls `POST /api/recovery/access/v1/authorise` as a synthetic caller with role RW-OFF and no Platform administration right, and asserts 403 with MSG-P4-002; then sends the readiness call as that caller and asserts 403 with `messageCode` MSG-P4-002, no reconciliation run started and no break row written.
11. Harness: writes one run report per business date, keyed by story and business date, naming the contract version of each hop, whether the hop was a stub or the owner, the counts, the break rows and the criteria of section 7.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case | Covered by |
|---|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no criterion is marked passed | None | TC-DM-008-01-ITG (ITG AC1) | AC1 |
| X2 | The cutover extract fixture lacks a required key on a migrated firm, user or instruction | The run fails and the report names the record and the missing field; a record without a key is never reported as reconciled | None | TC-DM-008-01-ITG (ITG AC1) | AC1 |
| X3 | A key has no view row and the extract does not list it | The run fails on AC2 and the report names the firm, the key type and the key value, so a suppressed break is a failure and not a pass | None | TC-DM-008-02-ITG (ITG AC2) | AC2 |
| X4 | A repeated run lists the same break twice | The run fails on AC4 and the report names the two rows and the business date | None | TC-DM-008-03-ITG (ITG AC4) | AC4 |
| X5 | The ALS batch is late (no ALS stamp, so JOB-04 is not started), or the product read answers `status` `STALE` | The readiness status reads `LATE`, or the freshness read answers `STALE` (`businessDate` null when never stamped); the run is reported as not run, never as passed | MSG-P1-001 | Test Cases v9: TC-DM-008-01-ITG, TC-DM-008-11-ITG | AC1, AC11 |
| X6 | A caller without the Platform administration right starts a run | The run fails on AC5 and the report names the caller role and the operation; a run that started is reported as started | MSG-P4-002 (expected, and missing) | TC-DM-008-04-ITG (ITG AC5) | AC5 |
| X7 | The counts the owner returns disagree with the extract | The run fails on AC4 and the report names each count and its two values | None | TC-DM-008-03-ITG (ITG AC4) | AC4 |
| X8 | A case record is duplicated, or a settlement figure appears on an instruction record or in the extract | The run fails on AC1 and the report names the instruction, the field and the view that owns the value; a copied figure is never reported as a pass | None | TC-DM-008-01-ITG (ITG AC1) | AC1 |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stubs from Day 1; the only wait is RWB-P1-DM008-APP, and its stub answers until it lands |
| Negotiable | The fixture layout, the break-list fields, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | The migrated partner, partner user and partner instruction keys are proven, no case is duplicated and no settlement figure is read, and every orphan is on a list with two owners before wave 4 opens |
| Estimable | One runner, one stub set, two fixtures, one key resolver, one no-copy assertion, one break-list assertion and one report |
| Small | Fits in one sprint with its four tests |
| Testable | Each criterion runs against the stubs and again against the real owner as the I story lands |

### 7. Acceptance criteria

```gherkin
Feature: Migrate partner performance - wave 4 cutover reconciliation harness

  Background:
    Given the synthetic cutover extract holds panel firm "PART-SYN-0008" with its panel_status, contract_end and score
    Given the firm's partner user carries identity_ref "PERS-SYN-000808" with a role_code, valid_from and valid_to
    Given the firm's instruction "INS-SYN-0008" names case "RW-2026-000801"
    Given the ACE views hold one row for person_key "PERS-SYN-000808"
    Given ReconciliationWorkflow "recon-2026-11-30" (JOB-04) has completed for business date "2026-11-30" as the child of AceIngestCheck

  Scenario: AC1 Extract the Workbench records (legacy RWB-DM-008 AC1)
    Given the legacy Workbench partner, partner user and partner instruction records at cutover
    When the migration reads them
    Then each firm keeps its panel status, its contract end and its score, each user its role and its dates, and each instruction its case, its status, its result_code and its fee_amount
    And no case record is duplicated and no settlement figure is read by the migration

  Scenario: AC2 Reconcile the business keys (legacy RWB-DM-008 AC2)
    Given the migrated records
    When the harness resolves the keys of the migrated records for business date "2026-11-30"
    Then every business key on a migrated record resolves to its view row, account_key and person_key included
    And each orphan is listed for the data steward and the ACE team in the run report
    And no partner, partner user or partner instruction key is expected from the REC-05 step of JOB-04, whose scope does not hold them (RD-P1-022)
    And the person_key resolution of identity_ref on the real services is pending (NEW-GAP-F07-01)

  Scenario: AC3 An orphan identity_ref is listed with its reason and its two owners (new, D-RCV-60)
    Given a migrated partner_user record on firm "PART-SYN-0008" carries identity_ref "PERS-SYN-000818"
    And the ACE views hold no row for person_key "PERS-SYN-000818"
    When the harness reads the reconciliation outcome for business date "2026-11-30"
    Then the break list of the reconciliation extract fixture holds one row for firm "PART-SYN-0008" with key type "PERSON" and key value "PERS-SYN-000818"
    And the row names the reason "NO_ACE_ROW" and the owner role "RW-DATASTEW"
    And the migrated firm and its instructions stay readable through the rwb-partner contract
    And the run report names the ACE team as the second owner of the break
    And on the real services the listing of this key is pending the break-detail store (GAP-1508, NEW-GAP-S2B-03) and the identity_ref rule (NEW-GAP-F07-01)

  Scenario: AC4 A repeated run is deterministic and one break is listed once (new, D-RCV-60)
    Given the reconciliation for business date "2026-11-30" has run once
    When POST /business-days/2026-11-30/ready is called again with a new UUID Idempotency-Key and answers 202
    Then the repeated call starts nothing: no second ReconciliationWorkflow run for "2026-11-30", because every due source of the date is stamped and the run has ended
    And no second set of reconciliation result rows exists for 2026-11-30
    And the break list holds exactly one row for identity_ref "PERS-SYN-000818"
    And the counts of firms, partner users, instructions and break rows equal the first run
    And the run report holds one entry per business date and not one per run

  Scenario: AC5 A caller without the platform administration right is refused (new, D-RCV-60)
    Given a synthetic user with role "RW-OFF" and no Platform administration right
    When that user calls POST /business-days/2026-11-30/ready with a UUID Idempotency-Key
    Then the answer is 403 with a problem body whose messageCode is "MSG-P4-002"
    And no reconciliation run starts and no break row is written

  Scenario: AC6 The wave entry check holds while a migrated key is unresolved (new, D-RCV-60)
    Given the break list holds one row for identity_ref "PERS-SYN-000818"
    When the wave entry check reads the cutover record and the reconciliation outcome for business date "2026-11-30"
    Then the cutover record shows a clean-day count of 0 and sign-off is not open, so wave 4 does not open
    And no publish status is read, because rwb-source-data holds none
    And the check names the break row and its owner role "RW-DATASTEW"

  Scenario: AC7 ACE data is read only through rwb-source-data (new, D-RCV-60)
    Given the migrated firm "PART-SYN-0008" with person_key "PERS-SYN-000808"
    When the harness reads the ACE side of that person_key
    Then the read goes through the DP02 record read of rwb-source-data, which alone reads the recovery.v_ace_* views
    And no ACE row is copied into a migrated record

  Scenario: AC8 A migrated record keeps its migration source and migration date (new, D-RCV-60)
    Given the migrated partner_user record for identity_ref "PERS-SYN-000808"
    When the harness reads the record
    Then the record holds its migration_source and its migrated_at
    And the record holds no copy of an ACE row

  Scenario: AC9 Each service applies its own Flyway sequence in its own schema (new, D-RCV-60)
    Given the partner, partner_user and partner_instruction tables are migrated
    When the harness reads the Flyway history of each owning service
    Then each service applies its own sequence in its own schema
    And rwb-source-data creates no table in schema rwb_partner

  Scenario: AC10 A consumed call that fails or does not answer is not recorded as clean (new, D-RCV-60)
    Given the DP02 record read fake answers 503 with messageCode "MSG-GEN-006" for business date "2026-11-30"
    When the harness calls it
    Then the run report names the hop and the failed call
    And the run report does not mark that business date as clean

  Scenario: AC11 A late or never stamped batch is reported as not run (new, RD-P1-040, RD-P1-041)
    Given the readiness status fake answers status "LATE" for business date "2026-11-30"
    And the freshness fake answers DP01 with status "STALE" and businessDate null
    When the harness runs for business date "2026-11-30"
    Then the run report records "not run" with DP01, the business date and "MSG-P1-001"
    And no key is resolved, no break row is asserted and the run is not marked passed
```

Legacy AC3 Cut over belongs to RWB-P1-DM008-APP, and the eleven criteria above (AC1 to AC11) are the ones this ITG story owns.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | Every business key on a migrated firm, partner user or instruction resolves to its view row before the record is served | REQ-RDF-007; DL25 | AC2; TC-DM-008-02-ITG |
| BR2 | Every break is listed with a reason the data product owner can see, and no break is suppressed | REQ-RDF-008 | AC3; TC-DM-008-02-ITG |
| BR3 | Zero tolerance: a BREAK result or a new REC-05 orphan resets the clean-day count, and wave 4 does not open while one migrated record has an unresolved key | DL25; DL25 option A applied by RD-P1-042, `recon.tolerance.pct` v1 = 0.00; no P1 publish status (RD-P1-024) | AC6; TC-DM-008-05-ITG |
| BR4 | ACE data is read only through the rwb-source-data contract, which alone reads the recovery.v_ace_* views, and is never copied | D-RCV-35; ADR-010 | AC7; TC-DM-008-06-ITG |
| BR5 | A migrated record keeps its `migration_source` and `migrated_at`, and never a copy of an ACE row | Legacy RWB-DM-008 guardrail; D-RCV-35 (U1); RD-P1-027 | AC8; TC-DM-008-07-ITG |
| BR6 | A firm keeps its panel status, its contract end and its score, each user its role and its dates, and each instruction its case, its status, its result_code and its fee_amount, with no case duplicated and no settlement figure read | Legacy RWB-DM-008 AC1; DL25 | AC1; TC-DM-008-01-ITG |
| BR7 | Each service applies its own Flyway sequence in its own schema | DP-15; ADR-021 | AC9; TC-DM-008-08-ITG |

The harness asserts these rules and changes none of them.

The partner_instruction facts are handed over in two packages. RWB-P1-DM007-APP carries the instruction raised for a legal action (instruction id, case, firm, instruction type, instructed_at and due_at). RWB-P1-DM008-APP carries the panel performance facts of the same instruction. S9 rwb-partner loads both once, idempotent on the instruction id.

DL25 is open. Its assumptions ASM-0728, ASM-0735, ASM-0743 and ASM-2602 are confirmed by the programme directive, and BR1, BR3 and BR6 apply on that basis.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| The panel status of the firm as migrated | Reconciliation for the business date with every key resolved | `recon-2026-11-30` completes and every partner_code, identity_ref and instruction case has a DP01 or DP02 row | The same panel status, unchanged |
| The panel status of the firm as migrated | Reconciliation for the business date with one orphan | identity_ref PERS-SYN-000818 has no DP02 row | The same panel status, unchanged, and the orphan is listed |
| A panel status with a listed orphan | A listed orphan resolves and is reconciled | A DP02 row appears for the key and the reconciliation of a later business date runs, or a FAILED run of the date is rerun | The break is no longer listed; the panel status is unchanged |

The harness changes no state. Every change in the table is made by the owner: S9 rwb-partner holds the firm, its users, its instructions and their results, and P1 rwb-source-data writes the reconciliation result and the break list. The harness reads, asserts and reports; a state it had set by hand would prove nothing, so the report names the owner and the operation behind every value it asserts.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward | Reads the reconciliation result for a business date; holds Platform administration R and Case record R; owns the break list with the ACE team. Does not start or rerun a run |
| Harness caller | Holds Platform administration U for the readiness call, Platform administration R for the status and result reads and Case record R for the record and freshness reads |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Read the same reconciliation evidence; each holds Platform administration R |
| QA lead | Owns the harness configuration, the fixtures, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | P1 rwb-source-data runs JOB-04 as a child of `AceIngestCheck` and writes the reconciliation result, S9 rwb-partner holds the panel, the partner users, the instructions and their results, P3 rwb-case holds the case, and P4 rwb-access answers the authorisation; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; authorisation is answered by rwb-access |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-PRT-001 to DF-PRT-007 | partner | partner_code, partner_name, partner_type, panel_status, contract_end, score | Read through the rwb-partner contract |
| DF-REF-212 to DF-REF-217 | partner_user | identity_ref, partner_id, role_code, valid_from, valid_to | Read from the cutover extract fixture; the identity_ref resolves through the rwb-source-data contract |
| DF-PRT-008 to DF-PRT-016 | partner_instruction | case_id, partner_id, instruction_type, instructed_at, due_at, status, result_code, fee_amount (all CARRY; DF-PRT-014 to DF-PRT-016 are Customer data, Confidential) | Read through the rwb-partner contract |
| DF-CAS-002, DF-CAS-005, DF-CAS-006 | recovery_case | case_no, status, stage_code | Read through the rwb-case contract |
| Standard column | partner, partner_user, partner_instruction | migration_source, migrated_at (RD-P1-027) | Read through the rwb-partner contract and the cutover extract fixture |

Field IDs are those in the Logical Data Model and Data Dictionary v9. The three partner tables are S9's and the harness reads them only through the rwb-partner contract; partner_user is proven from the cutover extract fixture because the published contract of this wave exposes the panel and the instructions, and the fixture is the migrated record under test. The case is P3's and is read through the rwb-case contract. The ACE side of the keys is DP01 Account and arrears for account_key and DP02 Customer and party for person_key, read through the rwb-source-data data-product contract (FSD P1 v3, lines 283 and 284), never from a view and never from a table. The settlement figure is not on a migrated instruction record and is not read: it stays with the ACE view that owns it. The harness owns no table and writes no row.

Reference data: the lists and parameters the harness reads are governed by the reference-data contract DP-06 and DP-07; the parameter names are Not specified in the source documents (DOR-RWB-ITG-DM008-ITG-20).

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/partner/v1/partners` | S9 rwb-partner | partner_code, partner_name, partner_type, panel_status, contract_end and score of each panel firm (AC1, AC2) |
| GET | `/api/recovery/partner/v1/partner/instructions` | S9 rwb-partner | The instructions with their case, their dates and their result (AC1, AC3) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case behind an instruction (AC1) |
| GET | `/api/recovery/source-data/v1/data-products/{productCode}/records?caseId={caseId}` | P1 rwb-source-data | The DP01 and DP02 rows that resolve account_key and person_key (AC1, AC2, AC3) |
| GET | `/api/recovery/source-data/v1/data-products/freshness?product=DP01` | P1 rwb-source-data | `status`, `businessDate` and `loadedAt` of the product (AC1, AC11) |
| POST | `/api/recovery/source-data/v1/business-days/{date}/ready` | P1 rwb-source-data | Start `AceIngestCheck`, whose child is JOB-04, with a UUID `Idempotency-Key`; 202 (AC1, AC4, AC5) |
| GET | `/api/recovery/source-data/v1/business-days/{date}/status` | P1 rwb-source-data | `RUNNING`, `DONE` or `LATE` for the business date (AC11) |
| GET | `/api/recovery/source-data/v1/admin/reconciliation/results` | P1 rwb-source-data | The REC rows of the business date (AC2, AC3); pending in the yaml file (RWB-P1-E1011-CON) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The right and the refusal path (AC5) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). Every error of rwb-source-data is an `application/problem+json` body with `messageCode` (RD-P1-004). No operation is invented in this story: each path is the owner's published operation, and where a screen would compose them the path would be the gateway-bff composite route (DP-19).

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

None. The harness starts JOB-04 through the readiness call, not through an event, and reads the result through the same contract rather than from a topic.

#### 12.5 Workflows and activities

None added. JOB-04, `ReconciliationWorkflow` on rwb-source-data (Architecture v5 slides 15 and 44), workflow ID `recon-{businessDate}`, runs as the child of `AceIngestCheck` (RD-P1-040) and is exercised through the readiness call. The S9 InstructionWorkflow (SLA timers; Act: issueInstruction, recordResult) is out of scope: it belongs to the S9 partner stories, and this harness neither starts nor asserts it. No workflow, activity or Schedule is created or changed by this story.

#### 12.6 Schedules

None. The harness starts the chain for the business date under test with the readiness call and sets no cron.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); the firm, its users and its instructions are S9's, the case is P3's and the reconciliation result is P1's.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-source-data | `fakes/rwb-source-data/5.1.0/`: the P1 operations of §12.2 | DP02 returns one row for PERS-SYN-000808, DP01 returns one row for the account_key of case RW-2026-000801, freshness returns `status` LOADED, business date 2026-11-30 with a load time, the readiness call answers 202, the status answers DONE, and the result read returns the REC rows of the date |
| Stub for rwb-partner | `GET /partners`, `GET /partner/instructions` | The firm PART-SYN-0008 with its partner_name, partner_type, panel_status, contract_end and score; the instruction INS-SYN-0008 on case RW-2026-000801 with its instruction_type, instructed_at, due_at and result |
| Stub for rwb-case | `GET /cases/{caseId}` | The case RW-2026-000801 with its case_no, status and stage_code |
| Stub for rwb-access | `POST /authorise` | Allows RW-DATASTEW with Platform administration R; refuses RW-OFF with 403 and MSG-P4-002 |
| Cutover extract fixture | The migrated records of the legacy story | The firm, its two partner users with identity_ref PERS-SYN-000808 and PERS-SYN-000818, the instruction INS-SYN-0008, the orphan identity_ref on a partner_user record, and the migration_source and migrated_at of each record |
| Reconciliation extract fixture | The break list of the reconciliation | One row for firm PART-SYN-0008 with key type PERSON, key value PERS-SYN-000818, reason NO_ACE_ROW, owner role RW-DATASTEW and the ACE team as second owner |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The harness environment and base hosts, the synthetic cutover extract fixture and its field layout, the break-list fields, the extract format and retention, and the pass or fail gate with its seeding set are Not specified in the source documents (GAP-0448; ASM-0640).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 9 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published and none consumed; the run is triggered by an operation and read back through the same contract |
| Temporal | None added; `ReconciliationWorkflow` (JOB-04) is exercised as the child of `AceIngestCheck` |
| File | The cutover extract fixture and the reconciliation extract fixture, both read as files |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies in the table above (RWB-PLT-E1044-CON and RWB-PLT-N001-CON) are recorded here and are not repeated in the metadata H field of this story, which stays empty as the plan requires. The one blocking dependency is the I story RWB-P1-DM008-APP, which replaces its stub; until it is live the run uses the stub, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the criteria of section 7 in order for a business date and holds the run lock |
| StubSet | Fake | The four stubs of §12.8 generated from the published contracts, with the contract version pinned |
| CutoverExtractFixture | Fixture | The synthetic firm, its two partner users, the instruction on its case, the orphan identity_ref and the migration_source and migrated_at of each record |
| KeyResolver | Service | Resolves person_key from identity_ref through DP02 and account_key through DP01 with the freshness read, and names each key that does not resolve |
| NoCopyAssertion | Service | Asserts that no case record is duplicated and that no settlement figure sits on a migrated instruction record or in the cutover extract |
| BreakListAssertion | Service | Compares the read result with the reconciliation extract fixture: one row per orphan, its reason and its two owners, and one row only on a repeated run |
| EvidenceReport | Service | Writes one report per business date keyed by story, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real services as the I story lands, on the synthetic firm PART-SYN-0008, its partner users with identity_ref PERS-SYN-000808 and PERS-SYN-000818, the instruction INS-SYN-0008 on case RW-2026-000801 and business date 2026-11-30; the panel_status, contract_end and score of the firm, the role_code, valid_from and valid_to of each user, and the instruction_type, instructed_at, due_at and result of the instruction are carried as fixture data, not as values in code. In SIT the records come from the S9 rwb-partner cutover load on S9's own Flyway sequence (DP-15). The harness environment and base hosts, the fixture layout, the break-list fields, the extract format and retention, and the gate with its seeding set are Not specified in the source documents (GAP-0448; ASM-0640). The harness seeds nothing by hand and never writes a schema row.

**Build steps**

1. Generate the four stubs from the published contracts and pin each contract version in the run report; fail the run on a mismatch (X1).
2. Build the CutoverExtractFixture and the ReconciliationExtractFixture, and prove both are read for business date 2026-11-30 (X2).
3. Build the JourneyRunner for AC1: send the readiness call with a UUID Idempotency-Key and wait for `recon-2026-11-30`, read the panel firms and the instructions through rwb-partner, read the case through rwb-case, and resolve person_key and account_key through DP02 and DP01 with the freshness read (X5).
4. Add the KeyResolver assertion that every key on a migrated firm, user or instruction resolves, and that each orphan is on the list for the data steward and the ACE team (X3).
5. Add BreakListAssertion for AC3: one row for firm PART-SYN-0008 with key type PERSON, key value PERS-SYN-000818, reason NO_ACE_ROW and owner role RW-DATASTEW, the ACE team named as second owner in the report, and the firm and its instructions still readable through the rwb-partner contract.
6. Add NoCopyAssertion for AC1: no case record is duplicated and no settlement figure sits on a migrated instruction record or in the extract, with the instruction and the field named where one does (X8).
7. Add AC4: repeat the readiness call for the same business date, assert one break row, equal counts of firms, partner users, instructions and break rows, and one report entry per business date (X4, X7).
8. Add the access path for AC5 through `POST /api/recovery/access/v1/authorise`, then the EvidenceReport and the gate, and swap a stub for the real owner as its I story lands (X6).

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-P1-DM008-APP when it lands, and the wave entry check holds a run report keyed by story and business date.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text.

This story neither builds nor reads screen SCR-45, and the screen's empty, loading, error and no access states are Not specified in the source documents (DOR-RWB-ITG-DM008-ITG-10). The harness's own failures are the exception paths X1 to X8, and a refused run is AC5 with MSG-P4-002.

### 15. Screens and states

The legacy story names the SCR-45 Data quality console with its loading and breaks states, and this harness renders no screen: the breaks are listed on the reconciliation extract, which the data steward and the ACE team read as a file. The states the harness asserts on that extract are small.

| State | What the extract holds |
|---|---|
| No break | One line for the business date with the counts of firms, partner users, instructions and break rows, and no break row |
| Break | One row per orphan with the firm, the key type, the key value, the reason, the data steward and the ACE team as owners |

The harness renders no screen. The SCR-45 Data quality console that the legacy story names is not part of this legacy key: it is the screen of RWB-AD-019 and this story neither builds it nor reads it; its empty, loading, error and no access states are Not specified in the source documents (CG-ALL-1027). What the wave entry check looks at instead is the run report: one file extract per business date, retained with the wave record, carrying the break-list fields of firm, key type, key value, reason and the two owners, and one binary gate at the wave entry check. Its base hosts and layout are Not specified in the source documents (GAP-0448; ASM-0640).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-008-01-ITG | AC1 (legacy); ITG AC1 | Integration | Synthetic firm PART-SYN-0008 and its user PERS-SYN-000808 with DP01 and DP02 rows present |
| TC-DM-008-02-ITG | AC2 (legacy); ITG AC2, ITG AC3 | Integration | One identity_ref PERS-SYN-000818 with no view row |
| TC-DM-008-03-ITG | AC3 (legacy, owned by RWB-P1-DM008-APP); ITG AC4 | Integration | Two readiness calls for business date 2026-11-30, with no duplicated case and no settlement figure |
| TC-DM-008-04-ITG | Access; ITG AC5 | Component | RW-OFF caller without Platform administration R |
| TC-DM-008-05-ITG | BR3; ITG AC6 | Integration | Break list of business date 2026-11-30 with one row for PERS-SYN-000818 |
| TC-DM-008-06-ITG | BR4; ITG AC7 | Integration | Person key PERS-SYN-000808 read through the DP02 record read |
| TC-DM-008-07-ITG | BR5; ITG AC8 | Integration | Migrated partner_user PERS-SYN-000808 with its migration_source and migrated_at |
| TC-DM-008-08-ITG | BR7; ITG AC9 | Integration | Migrated partner, partner_user and partner_instruction records in their own schemas |
| TC-DM-008-09-ITG | ITG AC10 (new, D-RCV-60) | Integration | Synthetic cutover extract with one consumed call that fails or does not answer; test data Not specified in the source documents (NEWAC-RWB-ITG-DM008-ITG-AC7) |
| TC-DM-008-01-ITG, TC-DM-008-02-ITG, TC-DM-008-10-ITG, TC-DM-008-03-ITG, TC-DM-008-04-ITG, TC-DM-008-05-ITG, TC-DM-008-06-ITG, TC-DM-008-07-ITG, TC-DM-008-11-ITG, TC-DM-008-09-ITG | New ITG AC11 and the changed assertions of ITG AC1 to AC8 and AC10 | Integration | Values of section 7 |

The AC column names the legacy AC the copy derives from and the ITG AC it asserts, and the full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx under the same legacy test case ID. TC-DM-008-03-ITG is the cutover copy and names RWB-P1-DM008-APP as the owner of the cutover assertions it derives from.

### 17. Guardrails

- No business value in code: the synthetic firm, users, instruction, business date, fixture contents, break reasons and report layout are data.
- No personal data in logs, fixtures or reports: identity_ref is synthetic and no customer record is read at all.
- No read of another service's schema and no direct view read: the firm, its users and its instructions come from rwb-partner, the case from rwb-case and the ACE side from the rwb-source-data contract (DP-01, DP-05).
- No settlement figure is read or copied, and no case record is duplicated by the harness.
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11).
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never writes a row by hand.
- A failing criterion is fixed in the service that owns it or reported as a gap; it is never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-DM-008 Migrate partner performance | Recovery Workbench Data Migration Stories v3, lines 466 to 549 | Sections 1, 3, 11 and 19 of this file |
| Legacy AC1 Extract the Workbench records, verbatim | The same, lines 485 to 489 | Section 7, AC1, marked (legacy RWB-DM-008 AC1) |
| Legacy AC2 Reconcile the business keys, verbatim | The same, lines 491 to 495 | Section 7, AC2, marked (legacy RWB-DM-008 AC2) |
| Legacy AC3 Cut over, and the four legacy test cases TC-DM-008-01 to TC-DM-008-04 | The same, lines 497 to 501 and 540 to 545 | AC3 stays with RWB-P1-DM008-APP (section 19); the four cases are copied as -ITG in section 16 |
| DF-PRT-001 to DF-PRT-007, DF-REF-212 to DF-REF-217, DF-PRT-008 to DF-PRT-016 and DF-CAS-001 to DF-CAS-055 | Logical Data Model and Data Dictionary v9 | Section 11 |
| DL25, zero tolerance on the migrated data | Decision Log, DL25 | Section 8, BR1 to BR3 |
| REQ-RDF-007 and REQ-RDF-008 | BRD Program v4 and Epic 1 v4 | Section 8, BR1 and BR2 |
| D-RCV-35 and ADR-010, ACE data only through the views | Decision Log, D-RCV-35; ADR-010 | Section 8, BR4 and BR5; sections 12.2 and 12.8 |
| Job map JOB-04 Reconciliation, owner rwb-source-data | Architecture v5 slides 15 and 44 | Section 12.5, the JOB-04 reconciliation this harness exercises; the S9 InstructionWorkflow is out of scope |
| DP-05, DP-15 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application |

### 19. Out of scope

- RWB-P1-DM008-APP: the extraction, the cutover and legacy AC3 Cut over, together with the clean-day count; the reconciliation is JOB-04 of RWB-P1-E1011-APP (RD-P1-022). The cutover load of the records into rwb_partner is S9's own step on S9's Flyway sequence (RD-P1-021).
- S9 rwb-partner production code and its CON, APP and DB stories: the panel, the partner users, the instructions, the results, the fees, the scorecards and the tables are built there. The S9 InstructionWorkflow and the accept, result and invoice operations are not started or asserted here.
- The partner portal and its FAPI 2.0 path through the partner gateway.
- The SCR-45 Data quality console (RWB-AD-019).
- The cutover plan, the data steward sign-off and the legacy read-only period of legacy AC3.
- ACE ingestion and the 30 views (RWB-ACE-001).
- Platform deployment and configuration.
- The other four data migration keys of this wave.

### 20. Remaining delivery steps

- Size the story (RW-TRIBE).
- Record the signed epic design of EP08 (product owner).
- Publish the rwb-source-data 5.1.0 fake and add the reconciliation result reads to the yaml file (rwb-source-data contract owner).
- Settle the break-detail store (rwb-source-data data architect; GAP-1508, NEW-GAP-S2B-03).
- Settle whether `partner_user.identity_ref` resolves as a person key (data architect with the rwb-partner service owner; NEW-GAP-F07-01).
- Settle a staff read of the migrated partner instruction (rwb-partner contract owner).
- Add the authorise path to the rwb-access yaml (rwb-access contract owner).
- Provide the stubs and synthetic fixtures in DEV (integration lead).
- Add the new and changed test case rows in Test Cases v9 and the Requirements Traceability Matrix (test writer).
