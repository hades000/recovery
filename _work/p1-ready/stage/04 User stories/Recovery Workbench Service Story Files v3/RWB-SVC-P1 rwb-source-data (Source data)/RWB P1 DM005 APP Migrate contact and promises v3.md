# RWB-P1-DM005-APP Migrate contact and promises

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (27 November 2026, D-RCV-60 P1 developer readiness, RD-P1 register)

- RD-P1-027: `person_key` and `contact_key` are DF-INT-003 and DF-INT-022; the package is a closed field list; `action_code` and `contact_result` are not carried; `migration_source` and `migrated_at` are added (findings #1, #7).
- RD-P1-021 and RD-P1-007: this story is the cutover writer of `contact_point_ext` in the same transaction as the interaction rows, written through `InteractionLedgerWriter` (finding #2).
- RD-P1-012, RD-P1-040 and RD-P1-042: the job rerun call is removed, the case read is recorded as a dependency, and clean days are defined (findings #3, #8, #9).
- AC3 extended, AC4 and AC5 rewritten, AC6 to AC8 added with fixtures (findings #4, #5, #6). Pending items and delivery steps are in sections 11 and 20.
- Batch D and the finishing pass: the `contact_point_ext` cardinality and absent-row clause moves here from RWB-P1-DM002-APP (AC9, BR13; RD-P1-068); the load runs under the target service's own workload identity and migration owner (RD-P1-068); a refused sign-off answers MSG-P1-023 (RD-P1-042); message references are Error and Message Standard v6; test case IDs of Test Cases v9 cited.

| Item | Value |
|---|---|
| Story key | RWB-P1-DM005-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-DM-005 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P1-DM005-APP-16); the squad sizes it at refinement |
| Patterns applied | DP05, DP15, DP19 |
| Parallel lane | L-P1-A |
| Ready to start | After RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| Depends on (build) | RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| Contract dependencies | rwb-case case read `GET /cases/{caseId}` (rwb-case.yaml, API Specification v7) |
| Contract version | rwb-source-data.yaml 5.1.0 and rwb-case.yaml of API Specification v7; the paths use /v1 |
| Readiness decisions | RD-P1-001; RD-P1-007; RD-P1-012; RD-P1-021; RD-P1-027; RD-P1-040; RD-P1-042; RD-P1-045; RD-P1-068 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: P1 slice of RWB-DM-005 for rwb-source-data — the one-off cutover load of the Workbench contact notes and open promises held outside EFS into this service's own `interaction` and `contact_point_ext`, the no-copy boundary of the EFS history, the ten clean days and the sign-off; legacy AC1 and AC2 move to RWB-ITG-DM005-ITG and this story owns legacy AC3. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-DM005-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 10 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **data steward (RW-DATASTEW)** and a **squad member (RW-TRIBE)**, I want **the open promises and contact notes the legacy Workbench holds outside EFS extracted once at cutover and loaded into this service's own `interaction` and `contact_point_ext` tables in `rwb_source_data`, each interaction keeping its case, its person key, its contact key, its promise date and its promise amount, with the EFS history read from `v_ace_efs_action` and never copied, and the ten clean days and the sign-off recorded as the cutover evidence**, so that **no promise a customer made is lost at cutover while the EFS history itself is read from ACE**.

**This is the P1 slice of legacy RWB-DM-005, not a withdrawal of it.** The legacy key keeps its epic E1, its release 30 November 2026 and its decision DL25; the realignment changes who owns the rows. The interaction ledger is rwb-source-data's (DP-18; ASM-0067), `contact_point_ext` is one of the four extension tables P1 owns (Architecture v5 slide 41; TSD P1 v3 T3.5), and DP05 Contact and promises names `interaction` with the three EFS views as its reads (FSD P1 v3 A2.2). `recovery_case` is P3 rwb-case's and is read through its contract, never written (DP-01). The slice is exactly four things: the one-off cutover load of the two tables on this service's login and per-service Flyway sequence (DP-15), the no-copy boundary of the EFS history, the ten clean days counted from the `reconciliation_result` rows of JOB-04, and the sign-off that closes the cutover.

**What this story does not build.** No REST operation of its own, no Kafka event, no workflow, no Schedule and no screen: the cutover is one-off bulk work from the release pipeline, and its result and breaks are read on SCR-44 Interface and job monitor and SCR-45 Data quality through the gateway-bff composite route (DP-19; Architecture v5 slide 32). Section 12 says so table by table.

### 2. Business rationale

A promise date or amount lost at cutover cannot be recovered afterwards: the customer keeps a commitment the bank no longer sees, the arrears strategy runs on a wrong date, and the next call opens with no record of what was agreed. The opposite risk is as costly: a copy of the EFS history into the Workbench makes the two stores drift, holds personal data under a retention rule the Workbench does not own, and answers the same case twice. The legacy story says what it protects:

> **Epic** E1, release 30 November 2026 · **Module** P1 Recovery data engine · **Depends on** RWB-E1-001, RWB-E1-069 · **Decision** DL25
>
> **Story** As a data steward, I want the open promises and contact notes held outside EFS migrated to the case, so that no promise a customer made is lost at cutover while the EFS history itself is read from ACE.

**Why this service loads its own tables.** Three ownership facts agree here: Architecture v5 slide 41 and the default ruling put the interaction ledger with rwb-source-data (DP-18; ASM-0067); the FSD gives DP05 `interaction` with the three EFS views (refresh DAILY, expected by 08:00); and the TSD defines `contact_point_ext` as a P1 extension table keyed by `contact_key`, holding a Workbench decision about an ACE record and never a copy of it (TSD P1 v3 T3.5). The service that owns the rows reads the dump and writes on its own login, with no handover and no C dependency of its own.

**Why the EFS history is read and never copied.** EFS is ingested into ACE (INT-07, owner the ACE team: TSD P1 v3 T5.1) and read through views 9, 10 and 11; the monolith copy `collections_history` is removed as a copy of EFS data (TSD P1 v3 T3.10; D-RCV-35 U1), and DL29 keeps twelve months readable. The Workbench holds the promise the customer made to us; ACE holds the contact history that was always ACE's. The extract therefore refuses a legacy row whose EFS record key resolves to a view row (legacy AC1, owned by RWB-ITG-DM005-ITG).

**Why ten clean days, and why the load is idempotent.** The cutover ends when the moved rows are seen to reconcile day after day: JOB-04 writes one `reconciliation_result` row per check and product group, REC-05 included (FSD P1 v3 A2.11; TSD P1 v3 T3.6). Ten consecutive clean days, with a break resetting the count, is that evidence; the count, the record that holds it and the sign-off shape are not fixed beyond AC3, so they are one assumption rather than an invention (GAP-2166; ASM-3477). And because the ledger is append only with no update path (RWB-P1-E1066-APP), each legacy row carries its own record key and the load is idempotent on it.

### 3. Preconditions

- **The views exist and are granted.** RWB-P1-E1069-APP creates the Section A views on the per-service sequence, views 9 to 11 with fields `DF-ACE-108` to `DF-ACE-139` among them (TSD P1 v3 T3.2, T3.3), and the `rwb_source_data` login holds SELECT on them and nothing in `public` (TSD P1 v3 T6.3).
- **The two target tables exist.** `interaction` arrives with RWB-P1-E1001-APP and its ledger shape, unique keys, sequence allocator and append-only trigger with RWB-P1-E1066-APP; `contact_point_ext` arrives with RWB-P1-E1069-DB (TSD P1 v3 T3.5). This story creates neither; its version adds the two provenance columns to both (RD-P1-027).
- **The reconciliation writes its rows.** JOB-04, its REC-01, REC-02 and REC-05 checks and `reconciliation_result` belong to RWB-P1-E1011-APP; until it lands a fixture stands in for the rows the count reads (12.8).
- **The per-service Flyway contract is in place.** RWB-PLT-E1044-CON gives the sequence with its `V0001` baseline and the view versions (DP-15); this story takes the next free version and creates nothing in it.
- **The gateway-bff composite route exists**, because RWB-PLT-N001-CON is the H dependency of DP-19: the result and its breaks are read through a route, not stitched by a screen.
- **The cutover has a place to run.** The release pipeline runs it for one business date as a pipeline command under one Idempotency-Key (a UUID) and never touches a `rwb_*` schema itself (Architecture v5 slide 32; RD-P1-001). **The pipeline step name, the cutover record format and the dump layout:** Not specified in the source documents (GAP-2166; ASM-3474).
- **No dependency blocks the start.** The two platform stories are contract stories and the two P1 stories are in-lane APP work, so the story starts after RWB-P1-E1001-APP and RWB-P1-E1069-APP (§R5.7 rules 2, 3 and 8); the wave 4 tag is the W-MAP tag of EP08 and does not delay the build.

### 4. Flow

1. The cutover window opens; the release pipeline starts the step for one business date and one environment as one-off bulk work, as a pipeline command and not as a REST operation or a P1 job type (RD-P1-012). No scheduler runs it.
2. CutoverContactPromiseExtract reads the legacy cutover dump once, only for the promises and notes held outside EFS: the case rows of their cases (to select and key), their `interaction` rows and the `contact_point_ext` rows of their contact keys, with the fields section 11 marks CARRY or KEY.
3. EfsDuplicateGuard reads `v_ace_efs_action` (view 9) once for the account keys of the extract and refuses every legacy row whose EFS record key resolves to a view row; `action_code` and `contact_result` are EFS facts, are not carried and are checked against no list (RD-P1-027).
4. InteractionCutoverMapper maps each remaining interaction to its case and keeps the five facts whole — case, `person_key`, `contact_key`, `promise_date`, `promise_amount` — copying and deriving nothing. `person_key` goes to `interaction.person_key` (DF-INT-003) and `contact_key` to `interaction.contact_key` (DF-INT-022).
5. CaseContractCheck calls the P3 case read for each case and refuses the batch when a case does not answer, so no migrated row points at a case the case service does not serve; the answer is a mock in the tests and adds no C dependency (12.2).
6. ContactPromiseCutoverLoader inserts both tables in one transaction per cutover business date: one `interaction` row per note or promise, written by calling `InteractionLedgerWriter` in process (the only component that writes the ledger), with `source_system` and `source_ref` carrying what the legacy row holds, and `migration_source` and `migrated_at` set; one `contact_point_ext` row per contact key, with consent carried as `consent_given` plus `consent_at` — WITHDRAWN as false with its date, UNKNOWN as no row at all (TSD P1 v3 T3.5), with `migration_source` and `migrated_at` set. The `contact_point_ext` rows are written in the same transaction as the interaction rows (RD-P1-021). With SY-DATALOAD retired, the load runs under the workload identity and migration owner of rwb-source-data, the target service of both tables (RD-P1-068; RD-P1-021).
7. CutoverEvidenceReader reads the `reconciliation_result` rows JOB-04 writes after the load (`DF-OPS-118` to `DF-OPS-129`) and counts the clean days: a business date on which every REC-01 and REC-02 row is PASS under `recon.tolerance.pct` version 1 = 0.00 and no new REC-05 orphan appears adds a day; non-business days (DP14 holiday calendar, Asia/Bangkok) neither add nor reset; a business date with no row adds nothing; a BREAK row or new orphan resets the count to zero and names the day.
8. On the tenth consecutive clean day the data steward signs off, held in the cutover record beside the ten day rows; the legacy tables are then set read-only for their retention period (Pending: the period, owner data steward, tracked as GAP-3541) and the records are served from the new schema through this service's interaction read.
9. At deploy the version applies on the per-service sequence, writes one `flyway_schema_history` row, adds the nullable columns `migration_source varchar(20)` and `migrated_at timestamptz` to `interaction` and `contact_point_ext`, and creates no table or index; its description carries the extract definition, the field list, the legacy record key and the read-only window (DP-15).

The extract is a one-off read of the legacy cutover dump keyed on the legacy record key; its formats, file name and dump layout are fixed at the cutover rehearsal and recorded in this version's description, and the cutover record is the release pipeline record that holds the counts, the ten day rows and the sign-off. Open promises and contact notes land in `rwb_source_data.interaction`, with the consent flags in `contact_point_ext`; EFS history stays a read through `v_ace_efs_action`.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The dump is absent, unreadable or read twice for the same business date | The step stops before any mapping; no row is written and the record names the date and the reason | MSG-GEN-001 | AC3, AC6 |
| X2 | An interaction carries no case, or its case does not answer | The row is refused whole, the step stops and the record names the row and the case; no partial load | MSG-GEN-001 | AC3 |
| X3 | A required key is empty: case, `person_key`, `contact_key`, `promise_date`, `promise_amount`, `contact_type` or `source_system` | The row is refused whole with the field named; no default and no derived value | MSG-GEN-001 | AC3 |
| X4 | `v_ace_efs_action` holds the EFS record key a legacy row carries | The legacy row is not migrated — that history is read from the view — and is counted as skipped; the record holds the count and the legacy record keys, no personal data | None | AC7 |
| X5 | A view read fails: relation absent or statement error | The step stops with no partial load and no stale history carried as current; the record holds the view name and the business date | MSG-GEN-006 | AC7 |
| X6 | The transaction of a business date fails during the load | Nothing of that date is committed; the rerun is idempotent on the legacy record key; the record holds the date and the step FAILED | None | AC6 |
| X7 | JOB-04 writes a BREAK row or a new orphan for a migrated record during the ten days | The count resets to zero, the day is named and the break is listed; the sign-off cannot be recorded | MSG-P1-012 | AC3 |
| X8 | A caller without a session, or without the Platform administration right, starts the step | 401 or 403 before the dump or a view is read; nothing is written | MSG-P4-001, MSG-P4-002 | AC8 |
| X9 | A sign-off is asked while the count of clean days is below ten | The sign-off is refused with the count and no sign-off record is written | MSG-P1-023 | AC3 |

The message texts are the legacy ones (section 14). MSG-P1-001 is raised by the freshness read of this service when the EFS batch is late; this story asserts it and does not produce it.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | One extract reader, one duplicate guard, one mapper, one case check, one loader, one evidence reader and one migration; the case is mocked |
| Negotiable | The dump layout and the cutover record are agreed at the rehearsal; this story fixes only the five facts, the no-copy rule and the idempotency key |
| Valuable | Every promise and consent held outside EFS survives cutover in the schema that now owns it, evidenced by ten clean days |
| Estimable | One batch step, five components, one migration, five fixtures and two test cases |
| Small | Fits one sprint, as the P1 slice of a split legacy key |
| Testable | AC3 runs end to end on a synthetic extract and synthetic reconciliation rows; no production and no ACE data needed |

### 7. Acceptance criteria

```gherkin
Feature: Migrate contact and promises

  Scenario: AC3 Cut over (legacy RWB-DM-005 AC3)
    Given ten clean days on the migrated records
    Given the rwb-case contract mock returns the case of each migrated interaction
    When the data steward signs off
    Then the legacy tables stay read-only for their retention period
    And the migrated records are served from the new schema
    And every migrated "interaction" and "contact_point_ext" row carries "migration_source" and "migrated_at"
    And the sign-off opens only when ten consecutive business dates are clean: every REC-01 and REC-02 row PASS under "recon.tolerance.pct" version 1 = 0.00 and no new REC-05 orphan
    When a date holds a "reconciliation_result" row with result "BREAK" or a new REC-05 orphan
    Then the count is 0, the date, REC code and key are listed in the cutover record and MSG-P1-012 is shown
    When a sign-off is asked with 9 clean days
    Then it is refused with "MSG-P1-023" "The cutover cannot be signed off. It has 9 clean days and needs 10." and no sign-off record is written

  Scenario: AC4 The load keeps the five facts and writes within its rules (new, D-RCV-60)
    Given a synthetic legacy promise with case "RW-2026-000601", person_key "PERS-SYN-000601", contact_key "PHONE:PH-SYN-0001", promise_date "2026-12-15" and promise_amount 5000.00, and a second one whose contact_key "PHONE:PH-SYN-0099" has no "v_ace_contact" row
    When the cutover loads business date "2026-11-30"
    Then "interaction" holds both rows with those values in "case_id", "person_key", "contact_key", "promise_date" and "promise_amount", and "action_code" and "contact_result" empty
    And "contact_point_ext" holds its rows in the same transaction with no column copied from ACE
    And "PHONE:PH-SYN-0099" is listed as an orphan and no row is deleted or changed
    And no log line carries a person_key, a contact_key or a summary text
    And no event or outbox row is written

  Scenario: AC5 A migrated interaction cannot be changed or deleted
    Given a migrated "interaction" row
    When an UPDATE or a DELETE of that row is attempted under the "rwb_source_data" login
    Then the append-only trigger of the ledger refuses the statement and the row is unchanged

  Scenario: AC6 A failed date commits nothing and a rerun inserts each row once
    Given the second insert of business date "2026-11-30" fails
    When the step ends
    Then no "interaction" and no "contact_point_ext" row of that date is committed and the step is FAILED
    When the step is run again for the date, and then a third time
    Then each legacy record key has exactly one row and the third run inserts 0 rows and reports them as already loaded

  Scenario: AC7 An EFS duplicate is skipped and a failed view read stops the date
    Given one legacy row whose EFS record key resolves to a "v_ace_efs_action" row and one that resolves to none
    When the step runs
    Then only the second is inserted and the record counts 1 skipped
    Given the read of "v_ace_efs_action" fails
    Then no row of the date is written, the step is FAILED and the record names the view with "MSG-GEN-006"

  Scenario: AC8 A caller without the right cannot start the step
    Given a request with no session and a caller without the Platform administration right
    When each starts the cutover step for "2026-11-30"
    Then the answers are 401 "MSG-P4-001" and 403 "MSG-P4-002" "You cannot run the contact and promise cutover extract here. Your role does not include it."
    And the dump and the views are not read and no row is written

  Scenario: AC9 Contact extension rows are zero or one per contact key (moved from RWB-P1-DM002-APP, RD-P1-068)
    Given person_key "PERS-SYN-000601" with contact keys "PHONE:PH-SYN-0001", "EMAIL:EM-SYN-0001" and "ADDRESS:AD-SYN-0001", where the dump holds a consent row for the phone key only
    When the cutover loads business date "2026-11-30"
    Then "contact_point_ext" holds exactly one row for "PHONE:PH-SYN-0001" and no row for the other two keys
    And the absent rows mean the table defaults: "consent_given" false, "failed_count" 0 and "source" "WORKBENCH"
    And the person keeps one entry per PHONE, EMAIL and ADDRESS contact point and no row is created to answer a read
```

The legacy lines of AC3 are copied character for character from legacy RWB-DM-005. The added Given is the rwb-case contract answer — the case of each interaction is read through the contract and never from a table — and it changes no legacy value in the When or Then lines. AC1 Extract the Workbench records and AC2 Reconcile the business keys are owned by RWB-ITG-DM005-ITG and are claimed by neither this file nor this story.

The lines added to AC3 state the clean-day rule of RD-P1-042 and the provenance columns of RD-P1-027. A sign-off asked below ten clean days answers MSG-P1-023 (RD-P1-042; it settles GAP-3545); MSG-P1-012 stays the break warning. Pending: confirmation of that message text and its applicability, owner Error and Message Standard owner. AC9 carries the contact cardinality and absent-row clause of RD-P1-027, moved to this story by RD-P1-068.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The interaction ledger is P1's in `rwb_source_data` and is written only by this service; `recovery_case` is P3's, read through its contract and never written | ASM-0067; DP-01, DP-18; Architecture v5 slide 41 |
| BR2 | `contact_point_ext` is P1's extension table keyed by `contact_key`, holding a Workbench decision about an ACE record; it belongs to data product DP02; this story writes its rows at cutover, in the same transaction as its interaction rows, the legacy consent and contact-quality rows (`DF-EXT-013` to `DF-EXT-026`) included, and copies no ACE column into it; zero or one row per `contact_key`; RWB-P1-DM002-APP verifies the customer read that shows them and writes none (RD-P1-068) | TSD P1 v3 T3.5; FSD P1 v3 A2.2; DP-01 |
| BR3 | The EFS history is read from `v_ace_efs_action`, `v_ace_efs_action_code` and `v_ace_efs_assignment` and never copied; a legacy row whose EFS record key resolves to a view row is not migrated | Legacy RWB-DM-005 AC1; DL29 (assumption: Not specified in the source documents (DOR-RWB-P1-DM005-APP-18)); TSD P1 v3 T3.3, T3.10; REQ-RDF-003 |
| BR4 | A migrated interaction keeps its case, `person_key`, `contact_key`, promise date and promise amount; no value is derived or defaulted; the two keys are held in `interaction.person_key` (DF-INT-003) and `interaction.contact_key` (DF-INT-022) | Legacy RWB-DM-005 AC1 (owned by RWB-ITG-DM005-ITG); RD-P1-027 |
| BR5 | The load is idempotent on the legacy record key: a second run of the same business date inserts no row and reports it as already loaded | AC3; RWB-P1-E1066-APP (append-only ledger) |
| BR6 | Ten clean days are counted from the `reconciliation_result` rows of JOB-04 on the migrated records; a business date on which every REC-01 and REC-02 row is PASS under `recon.tolerance.pct` version 1 = 0.00 and no new REC-05 orphan appears adds a day and a break resets the count | Legacy RWB-DM-005 AC3; FSD P1 v3 A2.11; DL25 option A applied by RD-P1-042; ASM-3477 |
| BR7 | The sign-off is held in the cutover record, the legacy tables stay read-only for their retention period, and the records are served from the new schema | Legacy RWB-DM-005 AC3; REQ-RDF-013; ASM-3474 |
| BR8 | The service runs its own Flyway sequence in its own schema; this story's version creates no table and no index and adds only the nullable columns `migration_source` and `migrated_at` to `interaction` and `contact_point_ext` | DP-15; ADR-021; TSD P1 v3 T3.2; RD-P1-027 |
| BR9 | ACE data is read only through `recovery.v_ace_*` views, on the service's own login, SELECT only, with no `public` table in any statement | BR-P1-001-2, BR-P1-001-4; ADR-010; DP-05; TSD P1 v3 T6.3 |
| BR10 | A business key with no view row is an orphan: listed for the data steward and, where the row is missing in ACE, for the ACE team, and it never deletes or changes the record | BR-P1-011-3; FSD P1 v3 A2.11.3.1; REQ-RDF-008 |
| BR11 | No value a business person may change is written in code, and no personal data appears in the extract, a log, a fixture or a prompt | Legacy RWB-DM-005 guardrails; FSD P1 v3 BR-P1-011; §R7.2 s17 |
| BR12 | A package carries only fields whose system of record is Workbench, with the linking business keys; `action_code` and `contact_result` are EFS facts and are read through the views, never carried. Every migrated row carries `migration_source` and `migrated_at`; `source_system` and `source` keep the business source | RD-P1-027 |
| BR13 | `contact_point_ext` holds zero or one row per `contact_key` and any number of rows per `person_key`, one per PHONE, EMAIL or ADDRESS contact point; an absent row means `consent_given` false, `failed_count` 0 and `source` 'WORKBENCH'; the contacts of a person are a list | RD-P1-027 as amended by RD-P1-068 |

BR1 and BR2 are the schema of `rwb_source_data`, proved by the load's own inserts and by the absence of any write to `rwb_case`; BR3 by the guard and by no ledger row mirroring an EFS action; BR4 on the load row; BR5 by the unique key on the source reference; BR6 and BR7 by the cutover evidence; BR8 by the migration; BR9 by the grant and boundary test of RWB-P1-E1069-DB; BR10 by the reconciliation the count relies on; BR11 by the review rule for the cutover code and its fixtures.

### 9. State transitions

None for the case: this story changes no case status, stage, task or promise state. The moves are the cutover's own, and they are six.

| From | Event | Condition | To |
|---|---|---|---|
| Cutover not started | The step is started for the business date | The dump is readable and every case of the extract is in it | Extract ready |
| Extract ready | The loader commits the business date | Every row carries its five facts and its legacy record key | Loaded: rows in both tables |
| Loaded | The loader is started again for the same business date | The legacy record key is already present | Loaded, unchanged: nothing inserted, the repeat reported |
| Loaded | JOB-04 writes PASS rows for the migrated records | Every REC-01 and REC-02 row PASS and no new REC-05 orphan on the day | Ten clean days running, at the consecutive count |
| Ten clean days running | A BREAK row or a new orphan appears | The break is listed for the data steward | Ten clean days running, at zero |
| Ten clean days running | The tenth clean day is reached and the steward signs off | The sign-off is recorded in the cutover record | Signed off: tables read-only, records served from the new schema |

The cutover record is the ledger of each move and the Flyway history row is the schema's record of the deploy; this story publishes no event for any move.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward and data product owner | Runs the cutover for a business date, owns the ten day evidence and records the sign-off (FSD P1 v3 A2.11.3.3) |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Hold the Platform administration right R of the legacy permission check and may read the record, the evidence and the extract for their scope (TSD P1 v3 T6.1) |
| RW-TRIBE, squad member | Builds the components and applies the version on the per-service sequence |
| The rwb-source-data service identity (`rwb_source_data` login) | Its workload identity and migration owner run the load (RD-P1-068); reads views 9 and 11 and the reconciliation rows, writes the migrated rows and its own history row |
| P3 rwb-case and its identity | Owns `recovery_case` and answers the case read; this story takes no right over the table |

The role codes are rows of rwb-access and the step authorises through the rwb-access guard before the dump is read; this story adds no role and no grant.

### 11. Data

| BR Field ID | Entity | Field | Disposition |
|---|---|---|---|
| DF-INT-001, DF-INT-002, DF-INT-004 to DF-INT-006, DF-INT-009 to DF-INT-021, DF-INT-023 to DF-INT-029 | `interaction` | `id`, `case_id`, `occurred_at`, `channel`, `direction`, `promise_amount`, `promise_date`, `summary`, `conduct_check`, `source_system`, `event_code`, `actor_type`, `actor_ref`, `source_ref`, `idempotency_key`, `case_seq` (allocated by the writer), `decision_log_id`, `corrects_entry_id`, `from_holder_ref`, `to_holder_ref`, `treatment_id`, `proceeds_id`, `retention_class`, `delivery_status`, `external_ref` | CARRY: written at cutover only; no update, no delete |
| DF-INT-003, DF-INT-022 | `interaction` | `person_key`, `contact_key` | KEY |
| DF-INT-007, DF-INT-008 | `interaction` | `action_code`, `contact_result` | ACE_READ: EFS facts, never carried |
| DF-EXT-013 | `contact_point_ext` | `contact_key` | KEY |
| DF-EXT-014 to DF-EXT-026 | `contact_point_ext` | `contact_type`, `consent_given`, `consent_at`, `verified_at`, `failed_count`, `source` and the standard columns | CARRY: written at cutover only |
| DF-CAS fields | `recovery_case` | The case of each interaction | EXCLUDE: P3's table; read from the dump to select and key; the case travels as DF-INT-002 `case_id` |
| DF-ACE-108 to DF-ACE-127 | `v_ace_efs_action` | `efs_record_key` and `account_key` first | ACE_READ: read for the duplicate guard; never copied |
| DF-ACE-131 to DF-ACE-139 | `v_ace_efs_assignment` | Keyed by `account_key` | ACE_READ: hand-over history of a promise account |
| DF-OPS-118 to DF-OPS-129 | `reconciliation_result` | The fields of a reconciliation row | Read for the count; written by JOB-04, never here |
| None (standard columns, LDM v11) | `interaction`, `contact_point_ext` | `migration_source`, `migrated_at` | Provenance: added by this story's version and set on every migrated row |
| None: framework table | `flyway_schema_history` | Version, description and checksum of this story's version | Write, one row, at deploy only |

Field IDs are those of TSD P1 v3 T3.3, T3.5 and T3.6 and of the Logical Data Model and Data Dictionary v11; the same package rows are held in Source to Target Mapping v7, sheet Migration packages. The migrated row is a legacy Workbench fact and never a copy of an ACE row: the ACE side of a promise stays in `v_ace_efs_action` (BR3). The two business keys are `interaction.person_key` (DF-INT-003) and `interaction.contact_key` (DF-INT-022). The seven standard record columns of TSD P1 v3 T3.0 are carried by both target tables and never by a view. No list of values and no parameter is read by this load. LOV-MIGRATION-SOURCE values are Pending, owner data owner (GAP-3275). Pending: the dump file layout, owner data steward, tracked as GAP-3541.

### 12. Contract

**12.1 REST operations provided**

None. The cutover is one-off bulk work from the release pipeline and is not a public operation: this story adds no path, no query parameter and no response field. The reconciliation read it relies on and the interaction read its tests use belong to other RWB-SVC-P1 stories and are named in 12.2, not claimed here (Architecture v5 slide 32).

**12.2 REST operations consumed**

One at run time: the case read `GET /api/recovery/case/v1/cases/{caseId}`, one call per case, 2 s with a breaker (CaseContractCheck). The step is a pipeline command; the pipeline reads the reconciliation results and the tests read the interaction:

| Caller | Operation | Owner | Why it is not a dependency of this story |
|---|---|---|---|
| The release pipeline | `GET /api/recovery/source-data/v1/admin/reconciliation/results` | P1 rwb-source-data (RWB-P1-E1011-APP) | Same service; the cutover record reads its evidence from it |
| CaseContractCheck and the ledger writer | `GET /api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | Contract dependency; a mock in the tests |
| The tests | `GET /api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data (RWB-P1-E1068-APP) | Same service: proves the records are served from the new schema |

The story holds one C dependency, the case read, and no I dependency. One hop and 2 s apply to it.

**12.3 Events published**

None. The cutover writes no outbox row and adds no schema to `rwb.source-data.events.v1`; `AceDataReady` and `AceDataLate` belong to RWB-P1-E1015-APP (TSD P1 v3 T5.3).

**12.4 Events consumed**

None. The step is started for a business date by the release pipeline; it reads no topic and no inbox row, and the `reconciliation_result` rows it counts are read from the table.

**12.5 Workflows and activities**

None added. JOB-04 Reconciliation is ReconciliationWorkflow of this service, a child of AceIngestCheck, exercised through its rows and unchanged. The cutover is a batch job of the release pipeline, not a Temporal workflow, because it runs once per cutover business date and not on a schedule or an event.

**12.6 Schedules**

None. No Temporal Schedule and no Quartz job sits here; JOB-04 is a child of AceIngestCheck and belongs to RWB-P1-E1011-APP.

**12.7 Tables owned**

| Table | Schema | Owner | This story |
|---|---|---|---|
| `interaction` | `rwb_source_data` | P1 (ASM-0067; DP-18) | Write at the cutover: one INSERT per note or promise, idempotent on the legacy record key, through `InteractionLedgerWriter`, which allocates `case_seq`; no UPDATE, no DELETE |
| `contact_point_ext` | `rwb_source_data` | P1 | Write at the cutover: one row per contact key of a migrated interaction, with the standard columns |
| `flyway_schema_history` | `rwb_source_data` | P1 | One row for its own version at deploy |
| `recovery_case` | `rwb_case` | P3 | Not written: read through the P3 contract only (DP-01) |
| `reconciliation_result` | `rwb_source_data` | P1 | Not written here: read for the count, written by JOB-04 |

Two tables are written and three are not, and that split is the boundary. `contact_point_ext` is P1's table in data product DP02, and its cutover rows are written by this story in the same transaction as its interaction rows (RD-P1-021). No statement names a `public` table, another service's schema or a cross-schema foreign key (DP-01, DP-05), and the append-only rule is respected, so a wrong row is corrected by its own record and not by an edit.

**12.8 Contract fakes**

| Fake | Serves | Used for |
|---|---|---|
| Legacy cutover extract fixture | The notes and promises held outside EFS, as synthetic rows with their cases, person keys, contact keys and promises | AC3, from Day 1, with no legacy data |
| View fixture (`v_ace_efs_action`, `v_ace_efs_assignment`) | Synthetic EFS rows: one series matching a legacy EFS record key and one matching none | AC3 and the skip path of X4 |
| rwb-case contract mock | The case of each migrated interaction, and one case that does not answer | AC3 and the refusal path of X2 |
| Reconciliation extract fixture | The `reconciliation_result` rows: PASS, BREAK and the REC-05 orphan | AC3 and the reset path of X7 |
| P1 interaction read mock | The migrated records served from `rwb_source_data` | AC3, in the last Then line |

Each fake is generated from the published contract it fronts or from the fixture set agreed at the rehearsal, so a contract change shows up as a test failure. Pending: the fixture layouts and the dump file name, owner data steward, tracked as GAP-3541.

**12.9 Call-type summary**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 new operations | 1: the case read | The step is a pipeline command; the case read is one hop, 2 s |
| Kafka | None | None | No event published or consumed |
| Temporal | None | None | No workflow, activity or schedule added; JOB-04 is exercised, not changed |
| File | None | One | The extract is read once from the legacy cutover dump, and the cutover record carries the evidence |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata.cutover`, in the service root `th.co.scb.ace.workbench.recovery.sourcedata`. Service base `/api/recovery/source-data/v1`, schema and login `rwb_source_data`, topic `rwb.source-data.events.v1`, task queue `rwb-source-data`; the topic and the queue are named for completeness and this story uses neither.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CutoverContactPromiseExtract | Batch job | The one-off read of the dump for the promises and notes held outside EFS; one pass per business date |
| EfsDuplicateGuard | Service | One SELECT on `v_ace_efs_action`, a failed read stopping the date, and the refusal of every row whose EFS record key resolves to a view row; no copy, no write |
| InteractionCutoverMapper | Service | Maps each interaction to its case and keeps the five facts whole, carrying the two business keys and only the CARRY and KEY fields of section 11 |
| CaseContractCheck | Client | One call of the P3 case read per case, 2 s, one retry of the GET with jitter and a breaker, so no row points at a case the service does not serve |
| ContactPromiseCutoverLoader | Repository | The only write path of the story: for one business date, in one transaction, calls `InteractionLedgerWriter` for each interaction and inserts the `contact_point_ext` rows, idempotent on the legacy record key |
| CutoverEvidenceReader | Service | Counts the clean days, resets on a break, and holds the ten day rows beside the sign-off |
| `V<seq>__rwb_p1_dm005_contact_cutover.sql` | Migration | Adds `migration_source` and `migrated_at` to `interaction` and `contact_point_ext`; records the extract definition, field list, legacy record key and read-only window in its description |

**Pattern application**

| DP code | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies in its own-service form: this is the service that owns the views, so the EFS reads are its own SQL on its own login and add no contract hop (Architecture v5 slide 45; ADR-010). DP-15 gives the sequence the version runs on and the history row that records the cutover definition, and is also why the load is this service's and not a handover. DP-19 puts the result and its breaks behind the composite routes of SCR-44 and SCR-45. No other pattern applies: no event (DP-09), no parameter or reference read (DP-06, DP-07), no guard library of its own (DP-08), no outbound call (DP-11), no cross-service adapter (DP-16) and no rule evaluation (DP-04).

**Database and migrations.** The story reads views 9 and 11 and the `reconciliation_result` rows and writes `interaction`, `contact_point_ext` and its own history row; no other table of any schema is named. The version creates no table, index or constraint and adds the two nullable provenance columns — `interaction` comes from RWB-P1-E1001-APP and RWB-P1-E1066-APP and `contact_point_ext` from RWB-P1-E1069-DB (BR8). No grant is made or changed: the login and its SELECT on the 30 views are RWB-P1-E1069-DB's. The version number is the next free one on the sequence and is not fixed here (TSD P1 v3 T3.2; ADR-021).

**Configuration and reference data.** No parameter and no reference list is read: DP-06 and DP-07 are not patterns of this story, and the ten day target, the business date and the retention period are data of the cutover record, not constants. The feature switch is `rwb.source-data.dm005-cutover-extract` from the platform flag library: off, the step refuses to start and no row is written, while the migration still applies because it creates nothing (ASM-3478). **Rollback (RD-P1-045).** Flag off first; redeploy the previous tag only if the flag does not cover the fault; never reverse the migration, since the added columns are nullable and the previous tag runs against them.

**Build steps**

1. Extract over the cutover fixture, one pass per business date, with the absent-dump and double-read cases; AC3 and X1.
2. Guard over the view fixtures, one row whose EFS record key matches and one that matches nothing, proving the match is skipped and no view field is written; AC7 and X4.
3. Mapper and case check: five facts whole, two business keys kept, no derived value or default, and one case that does not answer; AC3, X2 and X3.
4. Loader: one transaction per business date, `InteractionLedgerWriter`, the consent mapping of GIVEN, WITHDRAWN and UNKNOWN, the repeat run that inserts nothing, and the rollback of X6; AC4, AC5, AC6 and X6.
5. Evidence reader: ten PASS rows count up, a BREAK row or a new orphan resets the count, and the sign-off is refused below ten; AC3 and X7.
6. The version on the next free sequence with the two provenance columns, plus the repeated-apply check, and the refusal path through the rwb-access guard; AC8 and TC-DM-005-04.

**Done when.** The tests of section 16 pass, the migrated promises and consents answer from `rwb_source_data` through this service's own read and no EFS row has been copied, AC3 counts ten clean days and records the sign-off, a repeat of the same business date inserts nothing, and no class of the service names a `public` table or another service's schema.

### 14. Validation and messages

| ID | Type | When | Message |
|---|---|---|---|
| MSG-GEN-001 | Error | The extract lacks a required field or record: a case, a person key, a contact key, a promise date, a promise amount or a contact type | Enter {field}. |
| MSG-P4-002 | Error | A caller without the Platform administration right starts the cutover step | You cannot {action} here. Your role does not include it. |
| MSG-P1-001 | Warning | The EFS feed behind DP05 is late for the business date, so the history cannot be carried as current | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-001 | Error | No session when the step is started | As published in the Error and Message Standard |
| MSG-GEN-006 | Error | A view read fails | As published in the Error and Message Standard |
| MSG-P1-012 | Warning | A date inside the ten clean days has a BREAK row or a new REC-05 orphan | As published in the Error and Message Standard |
| MSG-P1-023 | Error | A sign-off is asked below the required count of clean days | The cutover cannot be signed off. It has {count} clean days and needs {required}. |

The MSG-P1-001 text matches Error and Message Standard v6; the other two message texts are copied character for character from the legacy master, and those three message IDs are those of that master (legacy RWB-DM-005 validation table; FSD P1 v3 VR-P1-011-1; TSD P1 v3 T3.7). This story raises MSG-GEN-001 and MSG-P4-002 itself: {field} is the field or record the extract lacks, and {action} is "run the contact and promise cutover extract", never a case fact or a value. MSG-P1-001 is raised by the freshness read of this service and asserted here as evidence.

Pending: the ACE view statement timeout, retry and database breaker policy, owner solution architect, tracked as GAP-3566 (Error Handling and Resilience Standard v5 section 8.4). A view read that fails stops the step with MSG-GEN-006 and is retried only by a rerun of the date (AC6, AC7).

### 15. Screens and states

SCR-44 Interface and job monitor states (Running; failed; complete; empty: Not specified in the source documents (CG-ALL-1922); loading: Not specified in the source documents (CG-ALL-1922); error: as RWB-P1-AD018-APP holds it; no access: a role without the Platform administration right is refused with MSG-P4-002).

SCR-45 Data quality states (Loading; breaks; empty: Not specified in the source documents (CG-ALL-1923); error: Not specified in the source documents (CG-ALL-1923); no access: a role without the Platform administration right is refused with MSG-P4-002).

No screen in this story. The cutover result is read on SCR-44 Interface and job monitor (Pending: how a pipeline command that is not a P1 job type appears there, owner solution architect, tracked as GAP-3320), and the breaks that reset the count are shown on SCR-45 Data quality, which RWB-P1-AD019-APP owns. Both are read through the gateway-bff composite route (DP-19; H RWB-PLT-N001-CON); this story adds no route, field or rendering, and the route path and merge order are Not specified in the source documents (GAP-2166; ASM-3474).

| State | What the cutover record holds | What the monitor shows |
|---|---|---|
| Extract ready | Business date, rows read, rows refused as EFS duplicates, cases resolved | The step is running and the extract is ready |
| Loaded | Rows written per table, with their legacy record keys | The rows are in `rwb_source_data` and answer through this service's read |
| Repeated run | Rows already present, rows written as zero, business date | The rerun completed and nothing was duplicated |
| Ten clean days running | Consecutive clean days and the last clean day | The count, its date and the remaining days |
| Break | The BREAK row or orphan, its date, code and owner role, count at zero | The break is listed and the count is reset |
| Signed off | The ten day rows, the extract, the sign-off and the read-only window | The cutover is complete and the legacy tables are read-only |

A cutover that has not reached ten clean days shows as a count and not as a pass, so one break in the window is visible as a reset and the sign-off cannot be recorded below ten (AC3).

The named states Running, failed, complete, Loading and breaks are those of Screen Specifications v1, which also gives Platform administration as the access of both screens. This story renders none of these states.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-005-03 | AC3; BR1 to BR7, BR10 | End to end | The cutover fixture with two open promises and two contact notes, one an EFS duplicate; the three view fixtures; the rwb-case mock with two cases and one that does not answer; ten PASS `reconciliation_result` rows, then one BREAK row and one orphan, then ten clean rows again; a repeated run of the same business date; the sign-off recorded once at ten |
| TC-DM-005-04 | Access; BR9 | Component | A caller whose Platform administration right R is absent in the authorise fake, starting the cutover for a business date; a second call with the right present for contrast |
| TC-DM-005-05 | BR8; BR11 | Component | The migration run on this story's version only, with its version history row read back; the cutover fixture and the captured logs of the extract, scanned for personal data and for any value a business person may change |
| TC-DM-005-06 | AC4; BR2, BR4, BR8, BR10, BR11, BR12 | Component | The two synthetic promises of AC4 (cases "RW-2026-000601", keys "PERS-SYN-000601", "PHONE:PH-SYN-0001" and the orphan "PHONE:PH-SYN-0099"), the contact view fixture and the captured logs |
| TC-DM-005-07 | AC5 | Component | A migrated row for the update and delete attempts |
| TC-P1-DM005-APP-01 | AC6 | Component | A fixture whose second insert fails, then two reruns of the date |
| TC-P1-DM005-APP-02 | AC7 | Component | The EFS view fixture with one matching and one unmatched key and a failing read |
| TC-P1-DM005-APP-03 | AC8 | Component | The authorise fake with no session and a missing right |
| TC-P1-DM005-APP-04 | AC9; BR13; the MSG-P1-023 refusal of AC3 (X9) | Component | The three-contact fixture of AC9 and a sign-off asked at nine clean days |

The legacy test case numbers are kept. `TC-DM-005-01`, the extract test, and `TC-DM-005-02`, the reconcile test, sit with AC1 and AC2 on RWB-ITG-DM005-ITG as `TC-DM-005-01-ITG` and `TC-DM-005-02-ITG` and are not repeated here; `TC-DM-005-03-ITG` and `TC-DM-005-04-ITG` are the integration copies of TC-DM-005-03 and TC-DM-005-04 above, so this story owns the End to end and the Component ones. The full test, with its Given, When and Then, is recorded in the Recovery Workbench Test Cases workbook, tab Story test cases, under the same ID; TC-DM-005-05 and the two version 3 rows are to be recorded there (Test Cases v9, W2-tests).

The cutover reconciliation harness pack (SIT hosts, a cutover extract fixture of one case and two contact keys, a break list with one row per orphan carrying key type, key value, reason and owner role, the extract format and retention, the gate signature, the data seeding set, and the no-copy assertion on `migration_source` and `migrated_at` with a zero count of EFS-shaped ledger rows) is agreed at the wave 4 entry check.

### 17. Guardrails

- No business value in code: the five facts are data on the load row, and the ten day target, the business date and the retention period are data of the cutover record, never a constant, an amount or a date in a class.
- No personal data in the extract, the logs, the fixtures or the prompts: it carries case and promise facts and ACE business keys, and no customer name, phone number, e-mail address or identity field; the fixtures are synthetic (BR11).
- ACE data only through the owner's contract or `v_ace_*` views, and here the service is the owner of the views: one login, SELECT only, no `public` table in any statement (BR9).
- No copy of an ACE row: the EFS history is read through views 9 to 11 and never copied, and a legacy row that resolves to an EFS record is not migrated at all (BR3).
- No cross-schema write and no cross-schema join: `recovery_case` is read through the P3 contract and no statement names `rwb_case` (BR1; DP-01).
- The ledger is append only and one version on the per-service sequence is never edited in place: the load inserts, never updates and never deletes, and a later change is a new version (BR5, BR8).
- A cutover is never declared on a count that has been reset: a break sets the count to zero and the sign-off stays closed (BR6, BR7).

### 18. Traceability

| Legacy RWB-DM-005 row | Value (verbatim) | Where it lands | Feature | L3 process |
|---|---|---|---|---|
| Epic | E1, release 30 November 2026 | Metadata wave and release; section 2 | None | All recovery processes |
| Module | P1 Recovery data engine | Service rwb-source-data, service epic RWB-SVC-P1 | None | All recovery processes |
| Feature | None | No feature grouping is used | None | All recovery processes |
| Process | All recovery processes | The cutover covers the notes and promises of every process the key names | None | All recovery processes |
| Priority | Must | Sections 1, 2 and 19 | None | All recovery processes |
| Depends on | RWB-E1-001, RWB-E1-069 | Rebased by D-RCV-60 onto RWB-P1-E1001-APP and RWB-P1-E1069-APP, plus the two platform contracts | None | All recovery processes |
| Decision | DL25 | BR6; the ten clean days as cutover evidence | None | All recovery processes |
| Story | As a data steward, I want the open promises and contact notes held outside EFS migrated to the case, so that no promise a customer made is lost at cutover while the EFS history itself is read from ACE. | Section 1; section 2 quotation; BR1 to BR5 | None | All recovery processes |
| Data | recovery_case, interaction, contact_point_ext with their field ranges | Section 11; AC3 | None | All recovery processes |
| Endpoints | No endpoint in this story. The migration is a cutover step run by the recovery service identity, and its breaks are listed on the reconciliation extract. | Sections 12.1, 12.2 and 15 | None | All recovery processes |
| Screen and states | No screen in this story. | Section 15 | None | All recovery processes |
| Permission checks | Platform administration R: RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Section 10; TC-DM-005-04 | None | All recovery processes |
| Validation and messages | MSG-P1-001, MSG-GEN-001, MSG-P4-002 | Section 14 (also MSG-P4-001, MSG-GEN-006, MSG-P1-012, MSG-P1-023) | None | All recovery processes |
| Test cases | TC-DM-005-01 to TC-DM-005-04 | Section 16; 01 and 02 sit on RWB-ITG-DM005-ITG; TC-DM-005-05 to TC-DM-005-07 and TC-P1-DM005-APP-01 to -03 are added in section 16 | None | All recovery processes |
| Guardrails | No value that a business person may change is written in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views. A migrated record keeps its source and its migration date, and never a copy of an ACE row. | BR3, BR9, BR11; section 17 | None | All recovery processes |

Patterns: DP-05 — views 9 to 11 are read by this service on its own login and by no other service (section 13). DP-15 — the version on the per-service sequence, with the history row that records the cutover definition and the load written by the schema's owner (section 13; AC3). DP-19 — the result and its breaks are read through the composite routes behind SCR-44 and SCR-45 (section 15).

Related stories: RWB-PLT-E1044-CON and RWB-PLT-N001-CON are the H contract dependencies (the sequence and the composite route); RWB-P1-E1001-APP and RWB-P1-E1069-APP are the H in-lane dependencies (the `interaction` base table and the Section A views); RWB-P1-E1066-APP and RWB-P1-E1068-APP supply the append-only ledger and the interaction read and are changed by neither; RWB-P1-E1069-DB creates the extension tables and grants and RWB-P1-E1011-APP writes the rows the count reads; RWB-P1-DM002-APP verifies the customer read that shows `contact_point_ext` consent and writes none of it (RD-P1-068), and the rwb-case case read is a contract dependency; RWB-ITG-DM005-ITG owns AC1 and AC2. External dependencies: None.

### 19. Out of scope

- The extract, the REC-05 reconciliation of the business keys and the ITG test copies: RWB-ITG-DM005-ITG, which owns legacy AC1 and AC2 and proves them against this service's contract.
- JOB-04, its REC-01, REC-02 and REC-05 checks, and the `reconciliation_result` rows: RWB-P1-E1011-APP.
- The `interaction` table's shape, its unique keys, its sequence allocator and its append-only trigger: RWB-P1-E1001-APP and RWB-P1-E1066-APP; this story inserts rows and changes none of them.
- The interaction read `GET /cases/{caseId}/interactions` with its filters, paging and masking: RWB-P1-E1068-APP.
- The four extension tables and every grant: RWB-P1-E1069-DB; and the customer read that shows consent on the case screen: `GET /customers/{personKey}` of RWB-P1-E1069-APP, verified by RWB-P1-DM002-APP (RD-P1-060; RD-P1-068).
- The views themselves and the DP05 catalog row with its freshness: RWB-P1-E1069-APP, RWB-P1-E1001-APP and RWB-P1-E1015-APP.
- The SCR-44 and SCR-45 screens and their break list, and the retention rule behind the read-only window: RWB-P1-AD018-APP, RWB-P1-AD019-APP and RWB-P1-E1017-APP.
- The legacy EFS history beyond the twelve months DL29 keeps, and every EFS copy: none exists in the target (TSD P1 v3 T3.10).
- The case record, its status, its stage and its timeline — P3 rwb-case, read through its contract and never written here — and the platform configuration of Kafka, Temporal and the gateway routes, which belongs to the platform epics.
- Any REST operation, Kafka event, Temporal workflow, Schedule or screen: this story builds none, and section 12 says so table by table.

### 20. Remaining delivery steps

- Size the story (squad, role RW-TRIBE).
- Record the signed epic design of EP08 (product owner).
- Publish and verify the contract fakes and record their versions (solution architect).
- Agree the dump layout and the legacy read-only retention period at the cutover rehearsal (data steward; GAP-3541).
- Confirm the MSG-P1-023 sign-off message and its applicability (Error and Message Standard owner).
- Provide the synthetic cutover and view fixtures in DEV (squad).
- Add the version 3 test rows to Test Cases v9 and the traceability matrix (QA).
