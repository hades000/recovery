# RWB-P1-DM013-APP Migrate money and closure

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-DM013-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-DM-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP15, DP19 |
| Parallel lane | L-P1-A |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-P1-DM013-APP-14) |
| Size | Not specified in the source documents (DOR-RWB-P1-DM013-APP-16); squad sizes at refinement |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7), additive inside /v1 (RD-P1-005); this story provides no operation, event or workflow of its own |
| Ready to start | After RWB-P1-E1001-APP, RWB-P1-E1069-APP; not started until both are done |
| Depends on (build) | RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| Contract dependencies | None for this story's code; the result read of RWB-P1-E1011-CON, which it does not call |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-005, RD-P1-011, RD-P1-012, RD-P1-024, RD-P1-027, RD-P1-040, RD-P1-042, RD-P1-045, RD-P1-068 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-DM-013 for the P1 cutover extract of the open proceeds matches, the closures and the write-off decisions of the open cases, its handover to the three owning services, and the cutover evidence counted from the reconciliation results. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 8 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: targeted edits for version 3. Tool: Claude Sonnet 5.5.

**Version 3 changes** (D-RCV-60 P1 developer readiness):

- A handover specification is added: three files, their fields, resolution stamp, count, checksum and run record, loaded only by the owning service's own load step (CDC-02565; GAP-2533; finding #1).
- The field list is closed by dictionary ID with `migration_source` and `migrated_at`; ACE-sourced fields are not carried, except the legacy proceeds amount and received date kept by directive (RD-P1-027; GAP-2533).
- AC4 is made executable and AC5 to AC7 added (findings #3, #4).
- DL25 is applied with `recon.tolerance.pct` version 1 = 0.00 (RD-P1-042).
- Contract version, workflow, screen references and rollback follow the register (RD-P1-005, RD-P1-012, RD-P1-040, RD-P1-045; findings #2, #5, #6).
- Batch D (RD-P1-068): the legacy proceeds `amount` and `received_date` are CARRY with the reason value at act time (GAP-2533), each with `migration_source` and `migrated_at`; each owner loads under its own workload identity and migration owner; MSG-GEN-006 follows Error and Message Standard v6; test case IDs of Test Cases v9 cited.

### 1. Story

As a **data steward (RW-DATASTEW)** I want **the P1 cutover extract of the legacy Workbench proceeds, closure and write-off decision records of the open cases, resolved to the ACE business keys and handed over to rwb-payment, rwb-writeoff and rwb-case, with the cutover evidence counted from the reconciliation results**, so that **money already received stays matched to its case, a closed case keeps its closure reason, the write-off decisions arrive with their committee dates, and no payment and no GL posting is copied**.

The legacy key is kept; what changes is who holds each table. The context pack puts no proceeds table and no write-off table in `rwb_source_data` and lists `proceeds`, `write_off` and `recovery_case` under other owners (GAP-2178; ASM-3516). The story therefore reads once, resolves twice and hands over three parts:

- **Extract, in rwb-source-data (this story).** The cutover run reads the legacy Workbench cutover dump once for the open cases at cutover, selects the `proceeds` rows, the closure facts of the case row and the `write_off` decisions, resolves `payment_code` against `v_ace_payment` and `write_off_key` against `v_ace_write_off` on the `rwb_source_data` login, and writes one file per owner with a checksum. It lands no row in `rwb_source_data` (ASM-3517).
- **Load, in the owner's own load step.** rwb-payment loads the proceeds rows into `rwb_payment` keeping each open row's matching state; rwb-writeoff loads the write-off decisions into `rwb_writeoff` keeping each `committee_date` and `tax_criteria_met`; rwb-case loads the closure facts with the case row it already migrates into `rwb_case`. Each owner uses its own schema, its own login and its own sequence (DP-15); P1 posts no load and calls no owner's load.
- **Evidence, in rwb-source-data.** Ten consecutive business dates on which every REC-01 and REC-02 row is PASS under `recon.tolerance.pct` version 1 = 0.00, no new REC-05 orphan appears on a migrated record (DL25 option A applied by RD-P1-042) and every `payment_code` of a migrated proceeds row resolves; a break resets the count. The evidence is a read over the `reconciliation_result` rows that JOB-04 writes; this story builds neither JOB-04 nor a table for the count (ASM-3518).
- **Sign-off, in the release pipeline.** The data steward signs off in the cutover record; the legacy tables stay read-only for their retention period and the migrated records are served from the three new schemas (ASM-3519).
- **Per-service migration (DP-15).** One version on the `rwb_source_data` sequence that creates no proceeds, closure or write-off object, whose description records the extract's definition, its field list and the read-only window.
- **No screen, no REST operation, no event, no workflow.** SCR-45 Data quality is a gateway-bff composite route that shows the reconciliation behind the clean days (DP-19; ASM-3520). The cutover is a release-pipeline command: it adds no path to `/api/recovery/source-data/v1`, publishes nothing on `rwb.source-data.events.v1` and starts no workflow on the queue rwb-source-data.

### 2. Business rationale

Money and closure are the two ends of a case. A receipt that is not matched to its case is a receipt the bank cannot account for and an officer will chase twice. A closure that arrives without its date and its reason is a case nobody can explain to audit, to the regulator or to the customer. Between the two sits the write-off decision, which carries the date the committee answered.

The legacy story states the aim in its own words: "As a data steward, I want the open proceeds matches and the closures recorded in the legacy Workbench migrated, so that money already received stays matched to its case and a closed case keeps its closure reason." Its Data table names the three entities, quoted here character for character:

> | recovery_case | id, case_no, product_group, primary_person_key, status, stage_code and 27 more | DF-CAS-001 to DF-CAS-055 |
> | proceeds | id, case_id, treatment_id, payment_code, source, amount and 3 more | DF-FIN-001 to DF-FIN-009 |
> | write_off | id, case_id, decision_log_id, amount, tax_criteria_met, committee_date and 5 more | DF-FIN-010 to DF-FIN-020 |

Its guardrail fixes the boundary this story keeps: "A migrated record keeps its source and its migration date, and never a copy of an ACE row." ACE holds the payment and the GL posting, and P1 reads them through `v_ace_payment` and `v_ace_write_off` on its own login; a copied payment is a payment that drifts, and nothing in the target would reconcile the copy back.

**Why one extract and three loads.** Each entity belongs to a different service, and a service writes only its own schema, with no cross-schema join and no foreign key across services (DP-01, DP-05). Only P1 can read the legacy dump once, and only P1 is the sole reader of the ACE views that hold the keys, so the extract is P1's work; each load follows the schema its owner holds (GAP-2178; ASM-3516).

**Why the evidence is P1's.** REC-05 resolves every business key on a Workbench row, `payment_code` included, against its view, and JOB-04 writes one `reconciliation_result` per check and product group for every business date (FSD P1 v3 A2.11; TSD P1 v3 T3.6). The three loads see no reconciliation, so the ten clean days are counted from rows that already exist; a break resets the count, because ten clean days that ignore a break are ten days of money that does not reconcile to ACE (ASM-3518).

### 3. Preconditions

- The Ownership Map entry is accepted: `proceeds` is P8's, `write_off` is S7's and `recovery_case` is P3's, each with the cutover migration of its own rows on its own sequence (DP-01; GAP-2178; ASM-3516).
- `RWB-PLT-E1044-CON` gives the `rwb_source_data` sequence and its baseline, so this story takes the next free version and writes one history row (DP-15; TSD P1 v3 T3.2).
- The tables and the data product catalog of `RWB-P1-E1001-APP` are live, `data_product` carrying DP13 Money and closure with one system of record (FSD P1 v3 A2.2).
- The read-only ACE views exist and are granted to the `rwb_source_data` login by `RWB-P1-E1069-APP`: this story reads `v_ace_payment` (DF-ACE-043 to DF-ACE-054) and `v_ace_write_off` (DF-ACE-261 to DF-ACE-269) and nothing else of ACE (TSD P1 v3 T3.3, T6.3).
- JOB-04, `ReconciliationWorkflow`, a child of `AceIngestCheck` after the ALS stamp (RD-P1-040), writes `reconciliation_result` with REC-01, REC-02 and REC-05, graded PASS or BREAK under `recon.tolerance.pct` version 1 = 0.00; a run that cannot proceed writes no row (RD-P1-042). It is the build of `RWB-P1-E1011-APP`, and this story reads its rows and changes none (FSD P1 v3 A2.11).
- rwb-payment, rwb-writeoff and rwb-case have added `migration_source varchar(20)` and `migrated_at timestamptz` to `proceeds`, `write_off` and `recovery_case` in their own Flyway steps (RD-P1-027 item 3). The values of list LOV-MIGRATION-SOURCE are Pending: owner data owner (GAP-3275).
- The gateway-bff composite route of `RWB-PLT-N001-CON` is in place, so the reconciliation breaks behind the cutover are read on SCR-45 without a screen of this story's own (DP-19; ASM-3520).
- The dump fixture, the view fixture and the three contract mocks exist before the first build, so the story needs no production data (section 12.8).
- The source of the legacy dump, its format and the place that holds the sign-off are Not specified in the source documents (GAP-2178; ASM-3517).

### 4. Flow

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Release pipeline | Starts the cutover run for the cutover business date | Checks the version of the extract definition in force and the caller's Platform administration right |
| 2 | The run | Reads the legacy cutover dump once and selects the open cases' `proceeds`, closure facts and `write_off` | Counts rows per entity and records the dump's checksum |
| 3 | The run | Maps each record to its fields and to its ACE business key | Keeps the section 11 CARRY and KEY fields, among them `payment_code`, the case, the closed date and reason, `committee_date`, `tax_criteria_met`, and the legacy proceeds `amount` and `received_date`; drops every ACE_READ field |
| 4 | The run | Resolves each key against `v_ace_payment` and `v_ace_write_off` on the service login | Marks each row resolved or orphan; lists every orphan for the data steward and, where the ACE row is missing, for the ACE team |
| 5 | The run | Writes the three handover files as the handover specification below gives them | Records the run, its counts, its checksums and its orphans in the cutover record; writes nothing to `rwb_source_data` and posts no load |
| 6 | Data steward | Reads the count of clean days, each a PASS result, and at ten signs off in the cutover record of the release pipeline | The legacy tables stay read-only for their retention period and the migrated records are served from the three new schemas |

**Handover specification (CDC-02565).**

| Item | Rule |
|---|---|
| Files | One file per owner for the cutover business date: proceeds to rwb-payment, write-off decisions to rwb-writeoff, closure facts to rwb-case |
| Fields | The section 11 fields marked CARRY or KEY, under their dictionary names |
| Per row | A resolution stamp, `resolved` or `orphan`, for the ACE key of the row where it has one, and the `migration_source` value |
| Per file | Cutover business date, row count and checksum; a file is written whole or not at all |
| Load | The owner's own pipeline load step on its own sequence and login, never a call or post by P1. The owner records the load run (file checksum, accepted and refused counts) in the cutover record |
| Retry | A refused file is handed to the owner's load step once more by the pipeline; a second refusal fails the handover (X5) |
| Provenance | The owner's load writes `migration_source` and `migrated_at` (RD-P1-027), the legacy proceeds `amount` and `received_date` included (RD-P1-068) |
| Loader identity | Each owner's load runs under that service's own workload identity and migration owner: rwb-payment, rwb-writeoff and rwb-case; the retired SY-DATALOAD identity is used by none (RD-P1-068; RD-P1-021) |
| Pending | File format, field order, checksum algorithm, location, access, retention, the load command's name and the rights to run it: owner data steward with the rwb-payment solution architect and the rwb-source-data owner (GAP-2178, GAP-2533), to be published in the Data Migration Approach |

### 5. Exception paths

| # | Situation | What happens | Covered by |
|---|---|---|---|
| X1 | The dump for the cutover date is absent or unreadable | The run fails before any part is written; the cutover record names the dump and the date; no count moves | AC1 |
| X2 | A record carries no `payment_code`, no case, no closed date or reason, or no `committee_date` | That record is refused and listed with its entity and its missing field; the other records of the part are not held back | AC1 |
| X3 | A `payment_code` or `write_off_key` resolves to no view row | The row is listed as an orphan for the data steward and the ACE team; the record is never deleted or changed to make the key resolve (BR-P1-011-3) | AC2 (proved by `RWB-ITG-DM013-ITG`) |
| X4 | The dump carries an ACE amount, a posting date or a GL field | The field is dropped by the mapper and the drop is counted; no copy of a payment or of a GL posting is created | AC1 |
| X5 | An owner's load step refuses its file | The pipeline runs the owner's load step once more; if it still fails, the run reports the owner, the file and the checksum, and the count does not start | AC1 |
| X6 | A reconciliation result for a business date is BREAK, holds a new REC-05 orphan on a migrated record, or leaves a `payment_code` unresolved | The count resets to zero and the date, its result rows and its rows are listed (ASM-3518) | AC3, AC7 |
| X7 | The ACE batch for DP13 is not COMPLETED for the business date, so no reconciliation row is written | The date is not counted as clean; the report shows the product stale with MSG-P1-001 and the senders of the data product see it | AC3 |
| X8 | The caller holds no Platform administration right | Refused with MSG-P4-002 and the cutover record shows the refusal; nothing is read and nothing is written | AC5; TC-DM-013-04 |
| X9 | A `v_ace_*` view fails during the run | The run fails with MSG-GEN-006 naming "ACE database"; no part and no count is written, and the rerun writes all three parts | AC1, AC6 |

### 6. INVEST check

| Letter | Check | How this story meets it | Result |
|---|---|---|---|
| I | Independent | Builds against the four H dependencies and their fakes; the three owner contracts are fixtures only, so no C or I dependency exists | Met |
| N | Negotiable | The extract definition, the handover format and the ten-day rule are stated; the file format and the dump location stay open (ASM-3517) | Met |
| V | Valuable | Money already received stays matched and a closed case keeps its reason at go-live, which is the legacy aim | Met |
| E | Estimable | The entity list, the field list, the two views and the evidence rows are all named; nothing rests on an unknown volume | Met |
| S | Small | One reader, one mapper, one resolver, one writer and one count over rows another story writes | Met |
| T | Testable | Two legacy criteria plus the exception paths, each with a fixture and a Level in section 16 | Met |

### 7. Acceptance criteria

```gherkin
Feature: Migrate money and closure

  Scenario: AC1 Extract the Workbench records (legacy RWB-DM-013 AC1)
    Given the legacy Workbench proceeds, closure and write-off decision records at cutover
    Given the rwb-payment contract mock returns the migrated proceeds row with its payment_code and its case
    Given the rwb-writeoff contract mock returns the migrated write-off decision with its committee date
    Given the rwb-case contract mock returns the migrated closure with its closed date and its closure reason
    When the migration reads them
    Then each proceeds row carries its payment_code and its case, each closure keeps its closed date and reason, and each write-off decision its committee date
    And no payment and no GL posting is copied, because both are read from v_ace_payment and v_ace_write_off
    And each of the three files holds exactly the section 11 CARRY and KEY fields, a resolution stamp per row, "migration_source", the business date, a row count and a checksum
    And the proceeds file keeps the legacy "amount" and "received_date" of each row and no file holds "posting_ref", a write-off "amount", "posted_date" or a GL field
    And the cutover record lists the three checksums and counts and every orphan, and no row of any "rwb_source_data" table is added or changed

  Scenario: AC3 Cut over (legacy RWB-DM-013 AC3)
    Given ten clean days on the migrated records
    Given the rwb-case contract mock returns the migrated records served from schema "rwb_case"
    When the data steward signs off
    Then the legacy tables stay read-only for their retention period
    And the migrated records are served from the new schema
    And the ten clean days are ten consecutive business dates on which every REC-01 and REC-02 row is "PASS" under "recon.tolerance.pct" version 1 = 0.00, no new REC-05 orphan appears and every migrated "payment_code" resolves
    And the cutover record holds the sign-off, the ten result sets, the three checksums, the three load run records and the retention window

  Scenario: AC4 The extract changes no state (rewritten from NEWAC-RWB-P1-DM013-APP-AC4)
    Given a synthetic proceeds row with "matched_to" "UNMATCHED" and a closed case with "closure_reason" "PAID_IN_FULL"
    When the run maps and hands over the files
    Then the proceeds file carries "matched_to" "UNMATCHED" and the closure file "closure_reason" "PAID_IN_FULL" unchanged
    And no row of "rwb_payment", "rwb_writeoff", "rwb_case" or "rwb_source_data" is added or changed by this story

  Scenario: AC5 A caller without the Platform administration right is refused (new, X8)
    Given a caller without the Platform administration right in the authorise fake
    When the caller starts the cutover run
    Then the run is refused with MSG-P4-002 "You cannot run the money and closure cutover here. Your role does not include it."
    And the cutover record shows the refusal, no dump or ACE view is read and no file is written

  Scenario: AC6 A failing view stops the run (new, X9)
    Given the SELECT on "v_ace_write_off" fails
    When the run resolves the keys
    Then the run is FAILED with MSG-GEN-006 "ACE database is not available. Try again in a few minutes."
    And no file and no count is written, and a later run with the view readable writes all three files

  Scenario: AC7 A break or unresolved key resets the count (new, X6, X7)
    Given nine consecutive clean business dates after the loads
    When the next date has a "BREAK" row, a new REC-05 orphan or an unresolved "payment_code"
    Then the count is 0 and the cutover record names the date and its rows and the sign-off is refused
    And a date with no "reconciliation_result" row adds no clean day and MSG-P1-001 is shown when the DP13 batch is not "COMPLETED"
```

AC1 and AC3 are copied character for character from legacy RWB-DM-013. The four added Givens are the contract answers of the three owners — the loads are theirs, so the migrated proceeds row, the migrated write-off decision, the migrated closure and the served schema are answered by their contracts and their mocks — and they change no legacy value. AC2 Reconcile the business keys is proved across the services by `RWB-ITG-DM013-ITG` as its AC1 with `TC-DM-013-02-ITG`, over the REC-05 rows this service writes. The added And lines of AC1 and AC3 state the handover specification of section 4 and the clean-day rule of RD-P1-042. Refusing a status change that a matching, committee or case model does not allow belongs to the owning state machine. Pending: the disallowed proceeds, write-off or case transition each owner's load refuses and the story that proves it, owner the rwb-payment, rwb-writeoff and rwb-case service owners (GAP-3550). The message ID shown for a refused sign-off is Pending: owner Error and Message Standard owner (GAP-3545). The cutover reconciliation harness pack for money and closure is Not specified in the source documents (GAP-0453); the fixture layout of the cutover extract, the break-list fields, the report shape, the evidence format and retention, the pass or fail gate and the synthetic data set are not set here.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | `proceeds` is P8's, `write_off` is S7's and `recovery_case` is P3's: this story extracts and hands over, and writes no row of `rwb_payment`, `rwb_writeoff` or `rwb_case` and no other service's schema | DP-01; GAP-2178; ASM-3516 |
| BR2 | The extract carries the `payment_code` and the case of a proceeds row, the closed date and the closure reason of a closure, and the `committee_date` and `tax_criteria_met` of a write-off decision, with every section 11 CARRY and KEY field | Legacy RWB-DM-013 AC1; RD-P1-027 |
| BR3 | No payment and no GL posting is copied: no ACE_READ field of section 11, ACE view amount, payment date or posting field enters a file or lands in `rwb_source_data`. The proceeds `amount` and `received_date` recorded by the legacy Workbench are values at act time and are kept with their provenance | Legacy RWB-DM-013 AC1 and guardrails; DP-05; GAP-2533 (directive); RD-P1-027 as amended by RD-P1-068 |
| BR4 | `payment_code` and `write_off_key` are resolved against `v_ace_payment` and `v_ace_write_off` on the service's own login, with SELECT and nothing else | TSD P1 v3 T3.3 and T6.3; DP-05 |
| BR5 | A link to ACE is a business key with no foreign key into ACE; `payment_code` and `write_off_key` are that link and REC-05 checks it | BR-P1-001-3; FSD P1 v3 A2.11 |
| BR6 | A migrated record keeps its source and its migration date, never a copy of an ACE row; each owner sets both and this story reads them through the owner's contract | Legacy RWB-DM-013 guardrails |
| BR7 | A REC-05 orphan never deletes or changes a Workbench record: it is listed for the data steward and, where the row is missing in ACE, for the ACE team | FSD P1 v3 A2.11.3.1 BR-P1-011-3 |
| BR8 | The cutover evidence is ten consecutive business dates on which every REC-01 and REC-02 row is PASS under `recon.tolerance.pct` version 1 = 0.00, no new REC-05 orphan appears on a migrated record and every migrated `payment_code` resolves; a break resets the count and no counter table is created | Legacy RWB-DM-013 AC3; DL25 option A (RD-P1-042); ASM-3518 |
| BR9 | The service runs its own Flyway sequence in its own schema; this version creates no money or closure object and records the extract, its field list and the read-only window in its description | DP-15; TSD P1 v3 T3.2 |

BR1, BR5 and BR9 are the boundary, proved in the history and in the refusal to write another schema. BR2, BR3 and BR6 are the extract's content, proved by the field list and by the absence of any ACE amount, posting date or GL field. BR4 is the grant. BR7 is an orphan, listed and never repaired in place. BR8 is the cutover gate.

### 9. State transitions

No case, no proceeds row and no write-off decision changes state here: the case state machine is rwb-case's, the matching state is rwb-payment's and the committee state is rwb-writeoff's. The moves below are the states of the cutover itself, as the cutover record shows them.

| From | Event | Condition | To |
|---|---|---|---|
| Not started | The run reads the dump for the cutover date | The dump is the dump of that business date | Extract ready: every open proceeds row holds its `payment_code` and its case, every closure its closed date and reason, every write-off decision its `committee_date`; nothing is written to `rwb_source_data` |
| Extract ready | The three owners' load steps load their files | Each file accepted with its checksum | Loaded: the rows are served from `rwb_payment`, `rwb_writeoff` and `rwb_case` with `migration_source` and `migrated_at`; the count is zero |
| Loaded | JOB-04 writes a PASS result set for a business date | Every REC-01 and REC-02 row PASS, no new REC-05 orphan, every `payment_code` resolved | One clean day: the count moves to the next business date |
| One clean day | JOB-04 writes a BREAK result, raises a REC-05 orphan or leaves a `payment_code` unresolved | The business date under test | Break: the count resets to zero and the date and its rows are listed |
| Ten clean days | The data steward signs off in the cutover record | The count is ten | Signed off: the legacy tables stay read-only for their retention period and the migrated records are served from the three new schemas |

This story announces no move by event, because a cutover is not a business event of a payment, a case or a write-off.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward and data product owner | Runs the extract for the cutover date, reads the clean-day count, signs off in the cutover record (Platform administration R) |
| RW-TRIBE, squad member and tribe lead | Builds the reader, the mapper, the resolver, the handover and the count; runs the tests; applies the version |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Read the cutover result and the reconciliation results; each holds Platform administration R |
| The ACE team lead | Receives every listed orphan whose row is missing in ACE and answers for the view row |
| The rwb-payment, rwb-writeoff and rwb-case service identities | Load the handed-over parts into their own schemas; this story never uses their logins |
| The rwb-source-data service identity | Reads the dump and the two views and writes one history row; holds no write on any other schema and none on `public` |

The legacy permission row for the key is kept unchanged: Platform administration R for the six roles above. The role codes are rows of rwb-access; this story adds no role and no grant.

### 11. Data

The handover fields are one row per Logical Data Model v11 field (RD-P1-027): CARRY, KEY, ACE_READ (never carried, read through the views) and EXCLUDE. The same rows are to be held in Source to Target Mapping v7, sheet Migration packages.

| BR Field ID | Entity | Field | Disposition | Note (classification, Data Classification v6) |
|---|---|---|---|---|
| DF-CAS-001 | `recovery_case` | `id` | CARRY | Not personal, Internal |
| DF-CAS-022 | `recovery_case` | `closed_date` | CARRY | Closure fact |
| DF-CAS-023 | `recovery_case` | `closure_reason` | CARRY | Closure fact |
| DF-CAS-002 to DF-CAS-021, DF-CAS-046 to DF-CAS-055 | `recovery_case` | all other fields | EXCLUDE | Not a closure fact; the case travels with RWB-DM-003 |
| DF-FIN-001 | `proceeds` | `id` | CARRY | Not personal, Internal |
| DF-FIN-002 | `proceeds` | `case_id` | CARRY | Not personal, Internal |
| DF-FIN-003 | `proceeds` | `treatment_id` | CARRY | Not personal, Internal |
| DF-FIN-004 | `proceeds` | `payment_code` | KEY | Indirect identifier, Confidential; masked in UAT |
| DF-FIN-005 | `proceeds` | `source` | CARRY | Customer data, Confidential; the business source |
| DF-FIN-006 | `proceeds` | `amount` | CARRY | Customer data, Confidential; value at act time: the recorded legacy value, which ACE cannot answer later (RD-P1-068; system of record ALS via COLLINS; GAP-2533); with `migration_source` and `migrated_at` |
| DF-FIN-007 | `proceeds` | `received_date` | CARRY | Customer data, Confidential; value at act time: the recorded legacy value (RD-P1-068; system of record ALS via COLLINS; GAP-2533); with `migration_source` and `migrated_at` |
| DF-FIN-008 | `proceeds` | `matched_to` | CARRY | Customer data, Confidential; the matching target (LOV-MATCH) |
| DF-FIN-009 | `proceeds` | `posting_ref` | ACE_READ | System of record ALS via COLLINS |
| DF-FIN-010 | `write_off` | `id` | CARRY | Not personal, Internal |
| DF-FIN-011 | `write_off` | `case_id` | CARRY | Not personal, Internal |
| DF-FIN-012 | `write_off` | `decision_log_id` | CARRY | Not personal, Internal |
| DF-FIN-013 | `write_off` | `amount` | ACE_READ | System of record GL; read through `v_ace_write_off` (GAP-3551) |
| DF-FIN-014 | `write_off` | `tax_criteria_met` | CARRY | Customer data, Confidential |
| DF-FIN-015 | `write_off` | `committee_date` | CARRY | Customer data, Confidential |
| DF-FIN-016 to DF-FIN-019 | `write_off` | `posted_date`, `responsibility_center`, `cost_center`, `gl_product` | ACE_READ | System of record GL |
| DF-FIN-020 | `write_off` | `recovered_after` | CARRY | Customer data, Confidential |
| DF-ACE-043 to DF-ACE-054 | `v_ace_payment` | view fields | Not carried; read | Read only, to resolve `payment_code` |
| DF-ACE-261 to DF-ACE-269 | `v_ace_write_off` | view fields | Not carried; read | Read only; `write_off_key` is resolved and no view field is copied |
| DF-OPS-010 to DF-OPS-020 | `data_contract` | `contract_code`, `source_system`, `status`, `published_at` | Not carried; read | Names the DP13 contract in force in the cutover record |

`write_off.amount` is mandatory in the dictionary but its system of record is GL. Pending: how rwb-writeoff fills it for a decision with no `v_ace_write_off` row, owner data architect with the rwb-writeoff service owner (GAP-3551).

The legacy proceeds `amount` travels with its record (GAP-2533); the write-off `amount` and the `amount` of `v_ace_write_off` are ACE facts and are never copied. P1 extracts the proceeds rows, the closures and the write-off decisions, hands proceeds to rwb-payment, write-off decisions to rwb-writeoff and closures to rwb-case, and copies no payment and no GL posting. How the matching state is kept through the handover is Not specified in the source documents (GAP-0543). The extract carries personal data as Data Classification v5 classes it, all Confidential: the indirect identifiers `case_no`, `primary_person_key` and `payment_code`, and the customer data `source`, `amount`, `received_date` and `matched_to` of `proceeds`, `tax_criteria_met`, `committee_date` and `recovered_after` of `write_off`; `write_off_key`, an indirect identifier, is read only to resolve the key. The Confidential handling rules apply: encrypted at rest and in transit, shown within the role's scope with indirect identifiers masked in UAT, export within the role's scope and logged, and no clear key or customer value in logs. No name, identity number, contact point or address is read. Reference data read: the `data_contract` view only (DF-OPS-010 to DF-OPS-020); the parameters read are Not specified in the source documents (DOR-RWB-P1-DM013-APP-20), and DP-06 and DP-07 are not applied by this story.

### 12. Contract

**12.1 REST operations provided**

None. The legacy story states "No endpoint in this story": the cutover is a release-pipeline command that reads a dump and hands over a file, so no caller could address it, and no path of `/api/recovery/source-data/v1` is added. The breaks and the result are read through the reconciliation result list `GET /admin/reconciliation/results` (API-P1-003, contract RWB-P1-E1011-CON) that `RWB-P1-E1011-APP` builds, which this story neither claims nor changes.

**12.2 REST operations consumed**

None at run time. The run reads its own dump, resolves its keys against its own views on its own login and writes its own history row. The three owner contracts are used as fixtures and as the read-back of what was loaded, which adds no run-time dependency (section 12.8).

**12.3 Events published**

None. No Kafka event, no outbox row and no schema on `rwb.source-data.events.v1`. AceDataReady and AceDataLate belong to `RWB-P1-E1015-APP` (RD-P1-003) and are not consumed by rwb-source-data; ProceedsMatched and WriteOffApproved belong to the two owner services.

**12.4 Events consumed**

None. The release pipeline starts the cutover; the reconciliation that produces the evidence is a child workflow of `AceIngestCheck` in `RWB-P1-E1011-APP` (RD-P1-040).

**12.5 Workflows and activities**

None added. JOB-04 `ReconciliationWorkflow`, whose results are counted, is the child workflow of `AceIngestCheck` built by `RWB-P1-E1011-APP` on the queue rwb-source-data (RD-P1-040); the payment matching of JOB-07 is rwb-payment's and the write-off scan of JOB-16 is rwb-writeoff's. This story creates and changes no workflow, activity or child workflow.

**12.6 Schedules**

None. No Temporal Schedule and no legacy Quartz job: the cutover is a one-off pipeline run and the daily count is a read over rows another story's trigger already writes.

**12.7 Tables owned**

| Table | Schema | Owner (ownership map) | This story |
|---|---|---|---|
| `flyway_schema_history` | `rwb_source_data` | P1 | Writes one row for its own version at deploy |
| `reconciliation_result` | `rwb_source_data` | P1 | Read only: the cutover evidence, written by JOB-04 (`RWB-P1-E1011-APP`) |
| `data_contract` | `rwb_source_data` | P1 | Read only: names the DP13 contract in force |
| `proceeds` | `rwb_payment` | P8 | Not owned and not written here: extracted to a file and loaded by its owner's load step |
| `write_off` | `rwb_writeoff` | S7 | Not owned and not written here: extracted to a file and loaded by its owner's load step |
| `recovery_case` | `rwb_case` | P3 | Not owned and not written here: the closure facts travel with the case row |

`rwb_source_data` holds no proceeds table and no write-off table, and this story adds none. No statement names a table in `public` and none names another service's schema; the only cross-schema read is the granted `recovery.v_ace_*` view (DP-01, DP-05).

**12.8 Contract fakes**

| Fake | Serves | Used for |
|---|---|---|
| Legacy cutover extract fixture | The `proceeds`, closure and `write_off` rows of the open cases at cutover, synthetic: proceeds row "PRC-SYN-000601" with `payment_code` "PAY-SYN-000601" on case "RW-2026-000601"; the closure of that case with closed date "2026-11-20" and reason "PAID_IN_FULL"; write-off decision "WO-SYN-000601" with `committee_date` "2026-11-18" | AC1 and AC3, and X1 to X4, from Day 1 |
| View fixture (`v_ace_payment`, `v_ace_write_off`) | The two views as synthetic rows, with one row for "PAY-SYN-000601" and one for "WO-SYN-000601", and none for "PAY-SYN-000777" | AC1 key resolution and the orphan path, X3 |
| rwb-payment contract mock (`GET /cases/{caseId}/payments`) | The migrated proceeds row with its `payment_code`, its case and its matching state, served from `rwb_payment` | AC1 and the load report |
| rwb-writeoff contract mock (`GET /write-offs`) | The migrated write-off decision with its `committee_date`, served from `rwb_writeoff` | AC1, X5 and the load report |
| rwb-case contract mock (`GET /cases/{caseId}`) | The migrated closure with its closed date and its reason, served from `rwb_case` | AC1 and AC3 |
| Reconciliation fixture (`reconciliation_result` rows) | PASS result sets for ten consecutive business dates and one BREAK set for the reset case | AC3, X6 and X7 |

The reconciliation fixture follows the answer shape of rwb-source-data.yaml 5.1.0; the owner fake versions are recorded when their contracts are published (RD-P1-011). Each fake is generated from a fixture or from the published contract and its version is pinned in the cutover record, so a contract change fails a test rather than passing silently.

**12.9 Call-type summary**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | None | A pipeline command; the result is read through API-P1-003, which another story owns |
| Kafka | None | None | No event published or consumed |
| Temporal | None | None | No workflow, activity or schedule; JOB-04, JOB-07 and JOB-16 are other stories' |
| File | None | One | The legacy cutover dump, read once per run, and the three handed-over parts with their checksums |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata.cutover`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`, login `rwb_source_data`, topic `rwb.source-data.events.v1` and queue rwb-source-data are named for completeness and used by no part of this story.

| Component | Type | Responsibility |
|---|---|---|
| MoneyClosureExtractReader | Repository | Reads the dump once and selects `proceeds`, the closure facts of `recovery_case` and `write_off` with the fields of the legacy Data table; no write, no `public` table |
| MoneyClosureKeyMapper | Service | Maps each record to the section 11 CARRY and KEY fields and drops every ACE_READ and EXCLUDE field |
| AceKeyResolver | Service | Resolves `payment_code` against `v_ace_payment` and `write_off_key` against `v_ace_write_off` on the service login; marks each row resolved or orphan (DP-05) |
| CutoverHandoverWriter | Service | Writes one file per owner as the handover specification gives it, and records the run, its counts, checksums and orphans in the cutover record; posts no load |
| CleanDayCounter | Service | Counts consecutive clean dates under RD-P1-042 with every migrated `payment_code` resolved; resets on a break (ASM-3518) |
| `V<next>__dm013_money_closure_cutover.sql` | Flyway version | Records the extract's definition, its field list and the read-only window in its description; creates no table, column or index (DP-15) |

**Build order.** The reader and the mapper first, against the dump fixture; then the resolver and the handover writer, against the view fixture; then the counter, against the reconciliation fixture; the version is applied and re-applied last, to prove the second run is a no-op. DP-19 is satisfied by reading, not building: SCR-45 is the composite route of `RWB-PLT-N001-CON` over API-P1-003.

**Estimate.** Five components, one SQL version and four fixtures: a small APP story, whose largest cost is the field-by-field mapping of section 11.

**Rollback (RD-P1-045).** The cutover step is behind its release switch: switch it off first; redeploy the previous image tag and chart version only if that does not cover the fault, naming in the release note every P1 capability the redeploy reverts. A migration is never reversed and no `U*.sql` or down script exists; a faulty version is corrected by a new forward version. This version creates no object. A file already loaded by an owner is not undone by P1. Pending: the key of the feature flag of this step, owner solution architect (GAP-3552).

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-012 | Warning | The case list for {date} does not reconcile to ALS for {product}: a difference of {variance} accounts, {pct} percent. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-GEN-006 | Error | {system} is not available. Try again in a few minutes. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

MSG-P1-001 and MSG-P1-012 are the two messages the legacy key carries and are copied unchanged (Error and Message Standard, current version v6); they are raised by the reconciliation of `RWB-P1-E1011-APP` and read here as the reason a date is not counted clean. MSG-GEN-001 carries the missing field of X2, MSG-GEN-006 the failing view of X9, and MSG-P4-002 the refusal of X8. Pending: the ACE view statement timeout, retry and database breaker policy, owner solution architect, tracked as GAP-3566 (Error Handling and Resilience Standard v5 section 8.4); a failed view read fails the run and the rerun writes all three parts (X9). No message text is held in code: the texts are rows of the message catalog in force.

### 15. Screens and states

This story renders no screen. The legacy screen SCR-45 Data quality stays the read of the result in its Loading and breaks states, and it is a gateway-bff composite route over the published reads (DP-19; H `RWB-PLT-N001-CON`; FSD P1 v3 SCR-45 "Reconciliation breaks, referential completeness (REC-05), quality measures and stale data products"). The reconciliation result list of API-P1-003, published by `RWB-P1-E1011-APP`, is the read behind it.

| State | What the cutover record shows |
|---|---|
| Loading | The dump read once, the counts of the three parts, the checksum, and the orphan list |
| Loaded | Each part accepted by its owner, the load reported through the three contracts, and a count of zero |
| Ten clean days running | The business dates counted, each with its PASS results |
| Break | The date of the break, its BREAK rows, its orphan or its unresolved key, and a count reset to zero |
| Signed off | The count of ten, the sign-off in the cutover record, and the legacy tables read-only for their retention period |
| Empty, loading, error and no access of SCR-45 | Defined by the console stories, not by this story |

A run that cannot start is recorded as FAILED in the cutover record with the dump and the business date named and no file written, so a cutover that did not happen is never read as one that did; a refused caller is recorded with MSG-P4-002.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-013-01 | AC1; BR1, BR2, BR3, BR4, BR6, BR9 | End to end | The dump fixture with proceeds row "PRC-SYN-000601" carrying `payment_code` "PAY-SYN-000601" on case "RW-2026-000601", the closure with closed date "2026-11-20" and reason "PAID_IN_FULL", and write-off decision "WO-SYN-000601" with `committee_date` "2026-11-18"; the view fixture with one row per key; a dump row carrying an ACE amount and a GL product, to prove both are dropped; the row counts of the three entities in `rwb_source_data` before and after; the version applied once and again |
| TC-DM-013-03 | AC3; BR5, BR7, BR8 | End to end | The reconciliation fixture with PASS sets for ten consecutive business dates, then one BREAK set, one new REC-05 orphan and one unresolved `payment_code`; a business date whose ACE batch is absent; the three contract mocks answering the migrated rows with their source and migration date from `rwb_payment`, `rwb_writeoff` and `rwb_case` |
| TC-DM-013-04 | AC5; Access refusal; BR4 | Component | A caller whose Platform administration right is absent in the authorise fake, starting the run and reading the result; a second call with the right present for the contrast; the row counts of `rwb_source_data` before and after the refusal |
| TC-P1-DM013-APP-01 | AC5 | Component | Authorise fake refuses the missing Platform administration right, with no data read or written |
| TC-DM-013-05 | AC4 | Component | A synthetic proceeds row with `matched_to` UNMATCHED and a closure with `closure_reason` PAID_IN_FULL; row counts of the four schemas' mocks before and after |
| TC-P1-DM013-APP-02 | AC6; X9 | Component | A `v_ace_write_off` fixture whose SELECT fails, then a readable run |
| TC-P1-DM013-APP-03 | AC7; X6, X7 | Component | Nine clean dates, then a BREAK, a new orphan, an unresolved `payment_code` and a date with no row |

AC5 is covered by TC-DM-013-04 and TC-P1-DM013-APP-01. The rows are held in Test Cases v9, tab Story test cases.

TC-DM-013-01 and TC-DM-013-03 are End to end because the run leaves the service's own boundary: it reads a file, resolves keys against views and reports three loads that other services performed. TC-DM-013-04 is Component because it exercises the guard at the boundary of the published operation. AC2 and its test case are proved across the services by `RWB-ITG-DM013-ITG` as `TC-DM-013-02-ITG`, where the REC-05 reconciliation of the migrated business keys is asserted; the live matching of a payment that arrives after cutover belongs to the rwb-payment story of the same legacy key and is not tested here.

### 17. Guardrails

- No business value in code: the cutover date, the handover location and the retention period are configuration of the release pipeline; the story writes no threshold, no percentage, no currency amount and no date.
- No clear personal data in logs, tests or prompts: the extract and its handover parts carry Confidential personal data (section 11) and are handled by the Confidential rules of Data Classification v5; the fixtures are synthetic, logs hold the id of the read, a code or an id and never a clear key or customer value, and no name, identity number, contact point or address enters the extract.
- ACE data only through the owner's contract or `v_ace_*` views, and here the service is the owner of the views: one login, SELECT only, no `public` table named in any statement.
- No copy of an ACE row: no ACE amount, payment date, posting date or GL field enters the extract (BR3).
- `rwb_source_data` holds no proceeds and no write-off table before or after this story; a closure is a case fact in `rwb_case`, not a record of its own (BR1).
- No cross-schema write: each owner loads its part through its own migration, and this story holds no grant on any of the three schemas (DP-01).
- An orphan is listed and never repaired: no migrated record is deleted or changed to make a key resolve (BR7).
- A break is never waived: a BREAK result, a new orphan or an unresolved key resets the count, and a stale product is never counted as a clean day (BR8; MSG-P1-001).
- The sign-off and the count are artefacts of the release, not Workbench rows: no table is invented for either (ASM-3518; ASM-3519).
- One version on the per-service sequence, never edited in place; a later change is a new version with its own history row (DP-15).

### 18. Traceability

| Legacy RWB-DM-013 item | Value (verbatim) | Where it lands |
|---|---|---|
| Module | P1 Recovery data engine | Service rwb-source-data, epic RWB-SVC-P1; `proceeds` is P8's, `write_off` is S7's and the closure is P3's |
| Epic | E2, release 31 December 2026 | Wave 4 tag from EP08; release 31 December 2026 (tentative) |
| Depends on | RWB-E1-001, RWB-E1-069 | RWB-P1-E1001-APP (tables and catalog) and RWB-P1-E1069-APP (views and grant) |
| Decision | DL25 (option A applied by RD-P1-042, `recon.tolerance.pct` v1 = 0.00, for Data lead confirmation; ASM-0728, ASM-0735, ASM-0743 confirmed with the tolerance named, ASM-2602 closed) | BR8, BR9: the ten clean days |
| Data | `recovery_case` DF-CAS-001 to DF-CAS-055; `proceeds` DF-FIN-001 to DF-FIN-009; `write_off` DF-FIN-010 to DF-FIN-020 | Section 2 quotation; section 11, the closed field list (RD-P1-027); AC1; TC-DM-013-01 |
| Endpoints | "No endpoint in this story." | Section 12.1; API-P1-003 is the read of the breaks and belongs to RWB-P1-E1011-APP |
| Screen and states | SCR-45 Data quality: Loading; breaks | Section 15; the screen is a gateway-bff composite route |
| Permission checks | Platform administration R for RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Section 10 |
| Guardrails | A migrated record keeps its source and its migration date, and never a copy of an ACE row. | BR3, BR6; AC1; section 17 |
| AC1 and AC3 | Copied character for character into section 7 with the origin tag | Section 7; TC-DM-013-01 and TC-DM-013-03 |
| AC2 and TC-DM-013-02 | Reconcile the business keys, REC-05 | Proved by RWB-ITG-DM013-ITG as its AC1 and TC-DM-013-02-ITG; not copied here |

| Pattern | Source | Applied as |
|---|---|---|
| DP-05 | Template and Rules §R5.5 | `v_ace_payment` and `v_ace_write_off` are read by this service on its own login, to resolve the two keys and to copy nothing (section 13) |
| DP-15 | Template and Rules §R5.5 | One version on the per-service sequence for the extract's record, and one load sequence for each owner (BR9, AC1, AC3) |
| DP-19 | Template and Rules §R5.5 | The reconciliation breaks behind the cutover are read on SCR-45 through the gateway-bff composite route (section 15) |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1044-CON | Contract | H: the per-service Flyway sequence and its history |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route that serves SCR-45 |
| RWB-P1-E1001-APP | App development | H: the tables of this service and the data product catalog DP13 resolves in |
| RWB-P1-E1069-APP | App development | H: the read-only views, the login and the grant |
| RWB-P1-E1011-APP | App development | Writes `reconciliation_result` through JOB-04, which is the cutover evidence |
| RWB-ITG-DM013-ITG | Integration | Proves AC2 across the services and asserts the keys, the break list and the cutover |
| The rwb-payment, rwb-writeoff and rwb-case stories of RWB-DM-013 | App development | Load the three handed-over parts into their own schemas and own the live behaviour afterwards |

### 19. Out of scope

- The load of a proceeds row, a closure or a write-off decision: each belongs to the service that owns the schema, and none is written here.
- The live proceeds matching, the payment event and the posting file of rwb-payment, and the committee, eligibility and posting of rwb-writeoff.
- The case state machine, the case record migration and the closure action of rwb-case.
- JOB-04, REC-01, REC-02, REC-05 and the reconciliation report: they are the build of `RWB-P1-E1011-APP`, and this story only reads their result rows.
- The data-quality console, its deployment and the SCR-45 screen itself: they belong to the P1 console stories and to the gateway-bff route.
- The ACE ingestion of ALS and GL, the continuance of `v_ace_payment` and `v_ace_write_off`, and the Interface Specifications of INT-02 and INT-16: the ACE team owns them.
- The retirement of the legacy Workbench tables: the retention period runs outside the Workbench and no statement of this story drops or truncates a table.

### 20. Remaining delivery steps

- Size the story at refinement (owner: squad).
- Record the EP08 epic design sign-off (owner: solution architect).
- Publish the handover file format, location, checksum algorithm, retention, load command and rights in the Data Migration Approach (owner: data steward with the rwb-payment solution architect and the rwb-source-data owner; GAP-2178, GAP-2533).
- Record the DP-15 split of this key in the split plan (owner: rwb-source-data owner).
- Agree the harness fixtures, evidence and pass gate (owner: integration lead; GAP-0453).
- Settle the write-off amount of an unposted decision (owner: data architect with rwb-writeoff; GAP-3551) and the feature flag key (owner: solution architect; GAP-3552).
- Name the disallowed transition each owner's load refuses (owner: payment, write-off and case service owners; GAP-3550).
- Bring RWB-PLT-E1044-CON, RWB-PLT-N001-CON and RWB-P1-E1011-CON to Done and publish the owner fakes at pinned versions (owner: contract owners).
- Load the synthetic fixtures in DEV (owner: squad).
