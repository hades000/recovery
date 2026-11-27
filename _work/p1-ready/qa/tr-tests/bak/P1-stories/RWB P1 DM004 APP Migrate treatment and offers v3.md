# RWB-P1-DM004-APP Migrate treatment and offers

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (27 November 2026, D-RCV-60 P1 developer readiness, RD-P1 register)

- RD-P1-027: the package is a closed field list by dictionary ID; the plan lookup key is (`plan_ref`, `account_key`); migrated rows carry `migration_source` and `migrated_at` (findings #1, #2, #3, #5).
- RD-P1-001, RD-P1-012, RD-P1-040 and RD-P1-042: replay and partial handover are defined, the job rerun call is removed, and the clean day is counted under `recon.tolerance.pct` version 1 = 0.00 (finding #4).
- AC1, AC3, AC4 and AC6 extended; AC7 to AC9 added; message texts cited from Error and Message Standard v6 (finding #7).
- Still pending: package format and location (GAP-0524), confirmation of MSG-P1-023 and the delivery steps in section 20 (findings #1, #6).
- Batch D and the finishing pass: the `plan_ref` orphan check is this story's own cutover check, counted in its evidence and not a REC-05 row, with the account key read through `GET /accounts/{accountKey}`; DP04 is ON_CHANGE with its plan part stamped when the core bank source completes (RD-P1-068); S2 loads under its own workload identity (RD-P1-068); a refused sign-off answers MSG-P1-023 (RD-P1-042); test case IDs of Test Cases v9 cited.

| Item | Value |
|---|---|
| Story key | RWB-P1-DM004-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 4 |
| Size | Sized by the squad at refinement; not specified in the source documents (DOR-RWB-P1-DM004-APP-16) |
| Business epic | EP08 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-DM-004 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP15, DP19 |
| Parallel lane | L-P1-A |
| Ready to start | After RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| Depends on (build) | RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| Contract dependencies | None |
| Contract version | v1 of the RWB-PLT-E1044-CON migration contract, v1 of the RWB-PLT-N001-CON public route surface, and rwb-source-data.yaml 5.1.0 (API Specification v7) for the reconciliation results |
| Readiness decisions | RD-P1-001; RD-P1-012; RD-P1-021; RD-P1-024; RD-P1-027; RD-P1-040; RD-P1-042; RD-P1-045; RD-P1-060; RD-P1-068 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split of RWB-DM-004 for the rwb-source-data cutover slice of the treatment and offer records, the handover to rwb-treatment and the cutover evidence, with the live records with S2 rwb-treatment and the dated DP04 copies built from events. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-DM004-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 5 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **data steward (RW-DATASTEW) and a squad member (RW-TRIBE)**, I want **the legacy Workbench treatment and approval records for the open cases extracted once at cutover and handed to rwb-treatment with each treatment keeping its case, its type, its offer amount, its approval level and its outcome, and its plan read from `v_ace_plan`, together with the cutover evidence of ten clean days, the sign-off and the read-only legacy tables**, so that **a restructure, settlement or deed already promised to a customer continues without a break at cutover**.

**The legacy key is not withdrawn: its Workbench-only part stays, and this story is the P1 slice of it.** RWB-DM-004 Migrate treatment and offers keeps its place in the legacy master, with its epic E2, its release 31 December 2026 and its decision DL25. What the realignment changes is *where the rows live and who moves them*. The Ownership Map rules that the live treatment records are S2 rwb-treatment's, in schema `rwb_treatment`, with its own Flyway sequence (DP-15); the dated DP04 copies in `rwb_source_data` (`dp_treatment`, `dp_guarantee_claim`) are P1's, built from Kafka events rather than from this extract, and read-only for reporting (Ownership Map ruling on `treatment`, `dp_treatment` and `dp_guarantee_claim`; ASM-0080). This story therefore carries exactly three things and nothing else:

- **The cutover extract of the legacy Workbench records.** The legacy Workbench treatment and approval records of the open cases at cutover are read once from the cutover dump, mapped to the case and to its ACE business keys, and kept whole: each treatment keeps its case, its type (`treatment_type`, LOV-TREATMENT), its offer amount (`offer_amount`), its approval level (`approval_level`, LOV-APPROVAL-LEVEL) and its outcome (`outcome`, LOV-TRT-OUTCOME). The plan a treatment refers to is read from `v_ace_plan` view 16, keyed by `plan_ref` (DF-ACE-160) and `account_key`; no plan record is copied and no plan is booked by the migration (AC1; TSD P1 v3 T3.3 view 16; legacy RWB-DM-004 AC1).
- **The handover to rwb-treatment.** The extract leaves as one handover package per cutover business date. The load into `rwb_treatment` is S2's own cutover migration on S2's own Flyway sequence: P1 writes no other service's schema and holds no INSERT into a `rwb_treatment` table (DP-01; ASM-0719). The dated DP04 copies in `rwb_source_data` are built from events by their own writer and this story adds none: `dp_treatment` and `dp_guarantee_claim` are named here for the boundary and for nothing else (TSD P1 v3 T3.6; ASM-0080).
- **The cutover evidence.** Ten clean days are counted from the `reconciliation_result` rows that JOB-04 writes for the migrated records: a day on which every REC-01 and REC-02 row is PASS under `recon.tolerance.pct` version 1 = 0.00 and no new REC-05 orphan appears continues the count, and a break resets it to zero (ASM-0721). The data steward's sign-off is held in the cutover record of the release pipeline, the legacy tables stay read-only for their retention period, and the migrated records are served from the new schema (AC3; FSD P1 v3 A2.11 and A2.13; Arch v5 slide 44 JOB-04).

**The per-service Flyway version (DP-15)** is the fourth artifact, and it is deliberately empty of schema: it creates no table, no column and no index for a treatment row and none for a plan row, and it records the extract's definition, the field list it carries and the read-only window of the legacy tables in its history description. The version number is the next free one on the sequence and is not fixed here (TSD P1 v3 T3.2; ADR-021).

**What this story does not build.** No REST operation, no Kafka event, no workflow, no schedule and no screen: the cutover step runs as one-off bulk work from the release pipeline as a pipeline command, and the cutover result is read on SCR-44 Interface and job monitor through the gateway-bff composite route (DP-19, H RWB-PLT-N001-CON; Arch v5 slide 32 "One-off bulk work"; slide 44). Section 12 states the emptiness table by table.

### 2. Business rationale

An agreed but unbooked treatment is a promise already made. A settlement at a discount, a restructure over a longer tenor, a deed in lieu: each one was approved at a level, offered at an amount and accepted by a customer, and none of it has been booked in ACE yet. At cutover that promise survives only if the migrated record still finds its case, still shows the approval level it was granted under, still carries the amount that was offered and still points at the plan it belongs to. A treatment that loses its case is a case a customer cannot continue; a treatment that loses its approval level is an agreement the bank cannot show it was allowed to make; a treatment whose plan link is invented by the migration is a balance that may be booked twice or not at all. The legacy story says this in its own words:

> **Epic** E2, release 31 December 2026
>
> **Module** P1 Recovery data engine
>
> **Depends on** RWB-E1-001, RWB-E1-069
>
> **Decision** DL25
>
> **Story** As a data steward, I want the agreed but unbooked treatments and their approvals migrated from the legacy Workbench, so that a restructure, settlement or deed already promised to a customer continues without a break at cutover.

**Why P1 extracts and S2 loads.** Two ownership rulings meet at this boundary and neither can be ignored. The live treatment is S2's: Architecture v5 slide 41 gives rwb-treatment "treatments, contracts, settlement and deed-in-lieu agreements, plan timers", schema `rwb_treatment`, topic `rwb.treatment.events.v1` and wave 2, and DP-15 gives every service its own Flyway sequence in its own schema. The cutover evidence and the reconciliation are P1's: slide 41 gives rwb-source-data "ACE view contract, extension tables, freshness, reconciliation", slide 44 puts JOB-04 Reconciliation with rwb-source-data as an event-triggered workflow, and the `reconciliation_result` table is P1's. DP-01 then forbids the one thing that would make this simple: a service never writes another service's tables, and no cross-schema join, foreign key or write is allowed. So the only lawful shape is the one this story takes: P1, which is the only reader of the `recovery.v_ace_*` views (Architecture v5 slides 8, 9, 41 and 45; ADR-010), reads the legacy dump and the plan view, keeps the referential proof and the cutover evidence in its own schema, and hands the treatment rows to the service that owns them so that S2 loads them on S2's sequence. A P1 that loaded `rwb_treatment` would break the boundary the architecture test enforces; an S2 that read `v_ace_plan` would break the single-reader rule. The split is the boundary, not an inconvenience of it (GAP-0523; ASM-0719).

**Why a plan is read and never copied or booked.** The plan is ACE's record. `v_ace_plan` is Section A view 16, over `ace_case`, `cfsc_mg_ssme_tdr_case`, `tdr_calculation` and `ai_recommended_plan`, keyed by `plan_ref` and `account_key`, 18 fields, and it carries the plan's status, its booked date and its closure facts as ACE holds them (TSD P1 v3 T3.3 view 16 and T3.4 column list). Copying it would put a second copy of an ACE plan into a Workbench schema, which is the copy rule the whole data engine was rebuilt to remove (TSD P1 v3 T1.1; `| No copy |` rule, T1). Booking it would be worse: booking is S2's act, from an approved treatment and its own contract, on the payment and booking events that rwb-payment and rwb-treatment own (Architecture v5 slide 42, TreatmentApproved and TreatmentBooked), and a cutover migration that booked a plan would produce a booking with no approval chain behind it. So the migration reads the plan's reference and status, links it to the treatment, copies no plan field and books nothing; AC1 says so in one line and section 8 turns it into a rule the build can be tested against.

**Why the evidence is ten clean days and not a checklist.** The cutover does not end when the rows move; it ends when the migrated rows are seen to be reconciling day after day. JOB-04 already compares ACE accounts with the open case accounts of rwb-case by product group and resolves every business key against its view row (REC-01, REC-02, REC-05; P1 holds no case list, RD-P1-024), and it writes one `reconciliation_result` row per check and product group (FSD P1 v3 A2.11.2 and A2.13). Ten consecutive clean days on the migrated records, with a break resetting the count, is the evidence that the moved records behave like records that were always there. The count, the sign-off record and where they are kept are not specified by any source beyond AC3 and the sibling migration slice, so the story fixes the mechanism in the assumption and cites it rather than inventing a number (GAP-0524; ASM-0721).

### 3. Preconditions

- **The plan view exists and is granted.** RWB-P1-E1069-APP creates the 16 Section A views on the per-service Flyway sequence, view 16 `v_ace_plan` among them, with its 18 fields `DF-ACE-160` to `DF-ACE-177`, keyed by `plan_ref` and `account_key` (TSD P1 v3 T3.2, T3.3; FSD P1 v3 A2.1.2). The `rwb_source_data` login holds SELECT on the views and no privilege in `public` (Architecture v5 slide 29; TSD P1 v3 T6.3).
- **The reconciliation runs and writes its rows.** RWB-P1-E1011-APP owns the reconciliation and data quality report, which covers JOB-04, its REC-01, REC-02 and REC-05 checks and the `reconciliation_result` table it writes (FSD P1 v3 A2.11 and A2.12; TSD P1 v3 T3.6; Arch v5 slide 44). Until that story lands, a reconciliation fixture stands in for the rows the clean-day count reads (section 12.8).
- **The per-service Flyway contract is in place.** RWB-PLT-E1044-CON gives the sequence of `rwb_source_data` with its `V0001` baseline and the two view versions (TSD P1 v3 T3.2; DP-15). This story takes the next free version after them and creates nothing in it.
- **The published contracts of the owning services are in the registry.** The P1 admin and reconciliation operations this story calls and puts its result behind, the P3 case read that supplies a case and its keys, and the S2 treatment read that answers with the migrated treatment and with the migrated records served from `rwb_treatment` (TSD P1 v3 Appendix T-A; Arch v5 slide 41). The S2 read is used as a mock in the tests and adds no C dependency, because the load it fronts is S2's own cutover step on S2's own sequence (ASM-0719; section 12.2).
- **The gateway-bff composite route behind SCR-44 exists.** RWB-PLT-N001-CON is the H dependency of DP-19, and the cutover result is read through that route rather than stitched together by a screen (Template and Rules §R5.5 DP-19).
- **The cutover step has a place to run.** The release pipeline runs the cutover as one-off bulk work for a business date, under one Idempotency-Key per run (a UUID), and it never reads or writes a `rwb_*` schema directly (Architecture v5 slide 32, "One-off bulk work" and "Airflow never reads or writes rwb_* schemas"). The pipeline step, its job name and the shape of its cutover record: Not specified in the source documents (GAP-0523; ASM-0719).
- **The legacy cutover dump is available once.** The extract is read once from the legacy Workbench cutover dump at the cutover window, on the read-only identity the cutover grants for it. Its layout, its file name and the identity that holds the read: Not specified in the source documents (GAP-0524; ASM-0720).
- **The data product catalog holds DP04.** DP04 Treatment and offers is a Workbench product, refreshed ON_CHANGE (FSD P1 v3 A2.14.2; TSD P1 v3 T3.7). Its plan part has a mapped source, the core bank (`data_product_source`, RD-P1-021): a stamp row is written when that source completes, it is never set STALE by time and DP04 is not in the DAILY gate set (RD-P1-068). RWB-P1-E1001-APP owns the catalog rows; this story reads none of them.
- **S2's target table carries the migration columns.** `treatment` carries `migration_source varchar(20)` and `migrated_at timestamptz`, added by S2 in its own Flyway step (RD-P1-027 item 3; DP-15). Pending: the values of list LOV-MIGRATION-SOURCE, owner data owner, tracked as NEW-GAP-B4.
- **The parameters and the reference data of rwb-case are not preconditions.** DP-06 and DP-07 are not in this story's pattern set: the cutover reads no parameter and no reference list, and writes no configurable value in code.
- **No build dependency blocks the start.** RWB-PLT-E1044-CON and RWB-PLT-N001-CON are platform contract stories, and RWB-P1-E1001-APP and RWB-P1-E1069-APP are in-lane APP and DB work; the story starts after those two (Template and Rules §R5.7 rules 2, 3 and 8). The wave 4 tag is the W-MAP tag of EP08 and does not delay the build.

### 4. Flow

1. The cutover window opens and the release pipeline starts the cutover step for one business date and one environment, as one-off bulk work, under one Idempotency-Key (a UUID) recorded in the cutover record with the business date. A run for a business date whose handover is recorded returns the recorded result and writes no second package. No scheduler runs it and no operator touches a schema (Architecture v5 slide 32).
2. CutoverTreatmentExtract reads the legacy Workbench cutover dump once for the open cases at cutover, and only those: the `recovery_case` rows of the open cases, used to select and to key, and the `treatment` rows with their approvals. The read is a single pass; the dump is never re-read inside the same cutover business date (AC1). The field list is section 11; the dump format is Pending (GAP-0524).
3. TreatmentCutoverMapper maps each treatment to its case and to that case's ACE business keys, then keeps the five facts the promise rests on: the case, `treatment_type`, `offer_amount`, `approval_level` and `outcome`. It copies values and derives none: a code stays the code the legacy record held, in the lists LOV-TREATMENT, LOV-APPROVAL-LEVEL and LOV-TRT-OUTCOME (TSD P1 v3 T3.8; legacy RWB-DM-004 data row).
4. PlanRefReader resolves the plan of each treatment through `v_ace_plan` view 16, one SELECT keyed by `plan_ref` (DF-ACE-160, the case's DF-CAS-046) and `account_key` (the case account's DF-CAS-026), both predicates always, and carries back the plan's reference and its status as ACE holds them. It reads the plan; it copies no plan field into any Workbench row, and it books nothing (AC1; DP-05; TSD P1 v3 T3.3 view 16). A `plan_ref` with no view row is found by this story's own cutover orphan check, which reads the account key of each treatment through `GET /accounts/{accountKey}` of this service (RD-P1-060) and counts the orphans in the cutover evidence; it writes no REC-05 row, because the REC-05 scope holds no `plan_ref` (RD-P1-022; RD-P1-068).
5. TreatmentHandoverPackage assembles the handover: one row per treatment with the CARRY and KEY fields of section 11, plus the cutover business date and `migration_source`. The package is written to the cutover record of the release pipeline, not to a table, with its row count and checksum, and is accepted only when the written file matches both.
6. The package is handed to rwb-treatment. S2's own cutover step loads the rows into `rwb_treatment` on S2's own Flyway sequence (DP-15): P1 writes no row of that schema, holds no INSERT against it and joins nothing across the boundary (DP-01).
7. CutoverEvidenceReader reads the `reconciliation_result` rows that JOB-04 writes for the business dates after the load (`DF-OPS-118` to `DF-OPS-129`) and counts the clean days: a date on which every REC-01 and REC-02 row is PASS under `recon.tolerance.pct` version 1 = 0.00 and no new REC-05 orphan appears moves the count up by one day; a date with no row adds nothing; a BREAK row or a new orphan resets the count to zero and names the day (AC3; ASM-0721).
8. On the tenth consecutive clean day, the data steward signs off. The sign-off is held in the cutover record of the release pipeline beside the ten day rows and the reconciliation extract they came from; nothing is written to a schema for it (AC3; ASM-0721). The record of the ten clean days and of the sign-off, its format and where the pipeline keeps it: Not specified in the source documents (GAP-0524; ASM-0721).
9. The legacy tables are set read-only for their retention period, and the migrated records are served from the new schema: a reader of a treatment after the sign-off reads `rwb_treatment` through the rwb-treatment contract and not the legacy Workbench table (AC3).
10. At deploy, the version of this story applies on the per-service sequence, writes one `flyway_schema_history` row and creates no table, no column and no index for a treatment or a plan row; its description carries the extract's definition, the field list and the read-only window, so the next reader of the schema and of the history finds out what shipped and why (AC1, AC3; DP-15).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The legacy cutover dump is absent, unreadable or read twice for the same cutover business date | The cutover step stops before any mapping; nothing is handed over and the cutover record names the business date and the reason | MSG-GEN-001 | AC1 |
| X2 | A treatment row carries no case, or its case is not in the extract | The row is refused whole, the step stops and the cutover record names the treatment and the missing case; no partial package is handed over | MSG-GEN-001 | AC1 |
| X3 | A required key is empty on a treatment row, such as `treatment_type`, `offer_amount`, `approval_level` or `outcome` | The row is refused whole with the field named; no default and no derived value is substituted | MSG-GEN-001 | AC1 |
| X4 | `v_ace_plan` holds no row for the `plan_ref` a treatment carries | The treatment is still extracted and handed over with its `plan_ref` and no plan facts; the orphan is listed by this story's cutover orphan check for the data steward and the ACE team and counted in the cutover evidence, and no plan is invented, copied or booked; it is not a REC-05 row, so the clean-day count of RD-P1-042 does not count it | None | AC1; AC8 |
| X5 | A read of `v_ace_plan` fails: the relation is absent or the statement errors | The cutover step stops with no partial handover and no stale plan carried as current; the cutover record names the view and the business date | None | AC1 |
| X6 | JOB-04 writes a BREAK row or a new REC-05 orphan for a migrated record during the ten days | The clean-day count resets to zero, the day is named in the cutover record and the break is listed for the data steward; the sign-off cannot be recorded | MSG-P1-012 | AC3 |
| X7 | The migration's Flyway version is applied a second time | Flyway reports it as already applied; no row is written twice and no version is edited in place | None | AC1 |
| X8 | A caller without the Platform administration right starts the cutover step | 403; the step is refused before any read of the dump or of the plan view, and nothing is written | MSG-P4-002 | AC4; TC-DM-004-04 |
| X9 | The step is started again for a business date whose handover is recorded | The recorded result is returned; no second package, count or sign-off is created | None | AC7 |
| X10 | The package write fails, or rwb-treatment's load refuses rows | A failed write leaves no accepted package and the step is FAILED; refused ids are listed in the cutover record, the count does not start, and P1 writes and repairs no row | None | AC7 |

The message texts are those of the legacy story and Error and Message Standard v6 (section 14). X1, X2, X3, X5, X7, X9 and X10 are component tests of this story and carry no new message ID.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | One extract reader, one mapper, one plan reader, one handover package, one evidence reader and one Flyway version; the load is S2's and is mocked |
| Negotiable | The package layout and the cutover record are agreed at the cutover rehearsal; this story fixes the five facts, the plan link and the no-copy rule only |
| Valuable | Every promised treatment keeps its case, its type, its amount, its approval level, its outcome and its plan at cutover, and the cutover is evidenced rather than asserted |
| Estimable | One batch step, three components, one migration, four fixtures and three test cases |
| Small | Fits one sprint, as the P1 slice of a split legacy key |
| Testable | AC1 and AC3 run end to end on a synthetic cutover extract and synthetic reconciliation rows; no production data and no ACE data are needed |

### 7. Acceptance criteria

```gherkin
Feature: Migrate treatment and offers

  Scenario: AC1 Extract the Workbench records (legacy RWB-DM-004 AC1)
    Given the legacy Workbench treatment and approval records for the open cases at cutover
    Given the rwb-treatment contract mock returns the migrated treatment with its case, its type, its offer amount, its approval level and its outcome
    When the migration reads them
    Then each treatment keeps its case, its type, its offer amount, its approval level and its outcome, and the plan it refers to is read from v_ace_plan
    And no plan record is copied and no plan is booked by the migration
    And the plan is looked up with both "plan_ref" and "account_key"
    And the handed-over package holds the CARRY and KEY fields of section 11 and no other field, with its row count, checksum and business date recorded in the cutover record
    And no row of any "rwb_source_data" table and no row of "rwb_treatment" is written by P1 and no event or outbox row is written

  Scenario: AC3 Cut over (legacy RWB-DM-004 AC3)
    Given ten clean days on the migrated records
    Given the rwb-treatment contract mock returns the migrated records served from schema "rwb_treatment"
    When the data steward signs off
    Then the legacy tables stay read-only for their retention period
    And the migrated records are served from the new schema
    And every migrated record answered by the contract mock carries "migration_source" and "migrated_at"
    And the sign-off opens only when ten consecutive business dates are clean: every REC-01 and REC-02 row PASS under "recon.tolerance.pct" version 1 = 0.00 and no new REC-05 orphan
    When a date holds a "reconciliation_result" row with result "BREAK" or a new REC-05 orphan
    Then the count is 0, the date, REC code and key are listed in the cutover record and MSG-P1-012 is shown

  Scenario: AC4 A caller without the Platform administration right is refused the cutover step (new, D-RCV-60)
    Given a caller whose Platform administration right is absent
    When the caller starts the cutover step for a business date
    Then the step is refused with 403 "MSG-P4-002" "You cannot run the treatment cutover extract here. Your role does not include it."
    And the dump and the plan view are not read, and no package or cutover state is written

  Scenario: AC5 The migration stays inside the service's schema, login and content rules (new, D-RCV-60)
    Given the rwb-source-data Flyway sequence is applied to an empty schema and then a second time
    Given the service login and the cutover code and fixtures
    When the sequence and the code are checked
    Then the version creates no table, no column and no index for a treatment row or a plan row
    And ACE is read only through recovery.v_ace_* views with SELECT only and no public table appears in any statement
    And no value a business person may change is written in code, no personal data appears in a log or a prompt, fixtures are synthetic, and the extract carries no personal data other than the keys plan_ref and account_key

  Scenario: AC6 A sign-off below ten clean days is refused (new, D-RCV-60)
    Given a cutover record with a count of 9 consecutive clean days
    When the data steward attempts the sign-off
    Then the sign-off is refused with "MSG-P1-023" "The cutover cannot be signed off. It has 9 clean days and needs 10.", no sign-off is recorded in the cutover record and the count stays 9

  Scenario: AC7 A repeated or partly failed handover adds no duplicate
    Given the handover of business date "2026-12-31" is recorded with its row count and checksum
    When the step is started again for "2026-12-31"
    Then the recorded result is returned and the handover location holds one package for the date
    Given the write of the package fails after the first row for a date with no recorded handover
    Then the step is FAILED and no package is accepted
    And a second run for that date produces exactly one accepted package

  Scenario: AC8 The plan key is the pair plan_ref and account_key
    Given "v_ace_plan" holds two rows with the same "plan_ref" "PLAN-SYN-0001" and "account_key" "ACC-SYN-000601" and "ACC-SYN-000777"
    And a treatment of a case whose account is "ACC-SYN-000777"
    When the plan of the treatment is resolved
    Then only the row of "ACC-SYN-000777" is associated
    Given no row holds the pair
    Then the treatment is handed over with its "plan_ref" and "account_key", is listed as an orphan by the cutover orphan check and counted in the cutover evidence, no plan fact is carried and no "reconciliation_result" row is written for it

  Scenario: AC9 Every field of the package follows section 11
    Given a treatment source row holding a value in every field of the "treatment" entity, and one empty optional field
    When the package is assembled
    Then every CARRY field is present under its dictionary name with the source value and the empty field stays empty
    And "installments" and "booked_at" are not in the package
```

The legacy lines of AC1 and AC3 are copied character for character from legacy RWB-DM-004. The two added Givens are the rwb-treatment contract answers: the load into `rwb_treatment` is S2's own cutover step, so the story states the answer it builds against rather than claiming the load, and neither Given changes a legacy value in the When or the Then lines. The lines added to AC1 and AC3 state the closed field list and plan key (RD-P1-027) and the clean-day rule (RD-P1-042). Pending: the message ID shown when a sign-off is refused below ten clean days, owner Error and Message Standard owner, tracked as NEW-GAP-S13-2. AC2 Reconcile the business keys is owned by RWB-ITG-DM004-ITG, carries the REC-05 proof across the services and is not copied here; the sibling DM003 slice left its AC2 in the same way.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The live treatment records are S2 rwb-treatment's in `rwb_treatment` and the dated DP04 copies are P1's in `rwb_source_data`; P1 extracts and hands over and never loads another service's schema; the dated DP04 copies are built from events, not from the extract | Ownership Map ruling on `treatment`, `dp_treatment` and `dp_guarantee_claim`; ASM-0080; DP-01; Architecture v5 slide 41 |
| BR2 | The extract is read once from the legacy Workbench cutover dump and lands nothing in `rwb_source_data`: the schema holds no treatment table and no copy of a plan | Legacy RWB-DM-004 AC1; TSD P1 v3 T3.10; GAP-0524 |
| BR3 | The plan of a treatment is read from `v_ace_plan` by the pair (`plan_ref`, `account_key`), both carried as the plan link, read only; no plan record is copied and no plan is booked by the migration | Legacy RWB-DM-004 AC1; TSD P1 v3 T3.3 view 16; D-RCV-35; ADR-010; GAP-0524 |
| BR4 | A migrated record carries `migration_source` and `migrated_at`, written by S2's load, and never a copy of an ACE row | Legacy RWB-DM-004 guardrails; TSD P1 v3 T1.1 "No copy" rule; RD-P1-027 |
| BR5 | Ten clean days are counted from the `reconciliation_result` rows of JOB-04 on the migrated records; a date on which every REC-01 and REC-02 row is PASS under `recon.tolerance.pct` version 1 = 0.00 and no new REC-05 orphan appears extends the count and a break resets it | Legacy RWB-DM-004 AC3; FSD P1 v3 A2.11; DL25 option A applied by RD-P1-042; ASM-0721 |
| BR6 | The sign-off is held in the cutover record of the release pipeline, the legacy tables stay read-only for their retention period, and the migrated records are served from the new schema | Legacy RWB-DM-004 AC3; REQ-RDF-013 |
| BR7 | The service runs its own Flyway sequence in its own schema; the version of this story creates no table, no column and no index for a treatment row or a plan row | DP-15; ADR-021; TSD P1 v3 T3.2 |
| BR8 | ACE data is read only through `recovery.v_ace_*` views, on the service's own login, with SELECT only and no `public` table in any statement | BR-P1-001-2; BR-P1-001-4; ADR-010; DP-05 |
| BR9 | A business key on a migrated record that has no view row is an orphan, is listed for the data steward and, where the row is missing in ACE, for the ACE team, and never deletes or changes the record; a `plan_ref` orphan is listed and counted by this story's own cutover check and is not in the REC-05 scope | BR-P1-011-3; FSD P1 v3 A2.11.3.1; REQ-RDF-008; RD-P1-022; RD-P1-068 |
| BR10 | No value a business person may change is written in code, no personal data appears in a log or a prompt, fixtures are synthetic, and the extract carries no personal data other than the keys plan_ref and account_key | Legacy RWB-DM-004 guardrails; FSD P1 v3 A2.11.3.1 (BR-P1-011); Template and Rules §R7.2 s17 |

Where each rule lives in the target: BR1 and BR2 are the boundary and are proved by the schema of `rwb_source_data` and by the absence of a write to `rwb_treatment`; BR3 is proved by the plan read and by the extract holding no plan field; BR4 is carried on the handover row; BR5 and BR6 are the cutover evidence; BR7 is the migration; BR8 and BR9 are the view contract and the reconciliation contract it relies on; BR10 is the review rule for the cutover code and its fixtures.

Reference data: the step reads no parameter and no reference list; the lists LOV-TREATMENT, LOV-APPROVAL-LEVEL and LOV-TRT-OUTCOME are copied as stored codes and not validated here (DP-06 and DP-07 are not in the pattern set).

### 9. State transitions

None for the case. This story changes no case status, no stage, no task and no treatment state: the treatment state machine lives in S2 rwb-treatment, and this story reads it and never writes it. The moves are the cutover's own, and they are five.

| From | Event | Condition | To |
|---|---|---|---|
| Cutover not started | The cutover step is started for the business date | The dump is readable and every open case is in it | Extract ready: the rows are mapped and the plan of each treatment is resolved |
| Extract ready | The handover package is assembled | Every row carries its section 11 fields, `migration_source` and the business date | Handed over: the package is in the cutover record and with rwb-treatment |
| Handed over | S2's own cutover step applies its Flyway version | S2's sequence is at the version that creates `rwb_treatment` | Loaded: the migrated records are served from `rwb_treatment` through the S2 contract |
| Loaded | JOB-04 writes its PASS rows for the migrated records | Every REC-01 and REC-02 row PASS and no new REC-05 orphan on the day | Ten clean days running, with the count at the number of consecutive clean days |
| Ten clean days running | A BREAK row or a new REC-05 orphan appears | The break is listed for the data steward | Ten clean days running, with the count at zero |
| Ten clean days running | The tenth consecutive clean day is reached and the data steward signs off | The sign-off is recorded in the cutover record | Signed off: the legacy tables are read-only for their retention period and the migrated records are served from the new schema |

The cutover record of the release pipeline is the ledger of each move, and the Flyway history row of this story's version is the schema's own record of the deploy. This story publishes no event that announces any move.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward and data product owner | Runs the cutover step for a business date, owns the ten day evidence and records the sign-off (FSD P1 v3 A2.11.3.3) |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Hold the Platform administration right R in the legacy permission check of this key and may read the cutover record, the evidence and the reconciliation extract for their scope (legacy RWB-DM-004 permission check; TSD P1 v3 T6.1) |
| RW-TRIBE, squad member | Builds the extract, the mapper, the plan read, the handover package and the evidence reader, and applies the version on the per-service sequence |
| RW-AUDIT, RW-COMPLY | Read the cutover record, the ten day rows and the sign-off as evidence; they take no cutover decision of their own |
| The rwb-source-data service identity (the `rwb_source_data` login) | Reads `v_ace_plan` and the reconciliation rows, and writes no row of the schema except the Flyway history row of its own version; the load into `rwb_treatment` runs under the workload identity and migration owner of rwb-treatment (RD-P1-068) |
| S2 rwb-treatment and its identity | Owns `rwb_treatment`, its Flyway sequence and the load of the rows this story hands over; this story takes no right over them |
| No approval level from the delegation of authority applies | The migration books no plan and approves no treatment; the approval level is a copied fact, not a decision |

The role codes are rows of rwb-access, and the step authorises through the rwb-access guard before the dump is read; this story adds no role and no grant of its own.

### 11. Data

| BR Field ID | Entity | Field | Disposition |
|---|---|---|---|
| DF-TRT-001 to DF-TRT-008, DF-TRT-010, DF-TRT-011, DF-TRT-013, DF-TRT-014, DF-TRT-027 to DF-TRT-033 | `treatment` | `id`, `case_id`, `decision_log_id`, `treatment_type`, `proposed_by`, `proposed_at`, `offer_amount`, `haircut_amount`, `valid_until`, `approval_level`, `outcome`, `outcome_at`, `interest_rate`, `booking_difference`, `first_due_date`, `signature_status`, `installment_amount`, `installments_paid`, `installment_shortfall` | CARRY: handed over; `rwb_treatment` is S2's |
| DF-TRT-009, DF-TRT-012 | `treatment` | `installments`, `booked_at` | ACE_READ: never carried |
| DF-CAS-046, DF-CAS-026 | `recovery_case`, `case_account` | `plan_ref`, `account_key` | KEY: the plan link of each row |
| Other DF-CAS fields | `recovery_case` | All other fields | EXCLUDE: P3's table; read from the dump only to select and key the open cases; the case travels as DF-TRT-002 `case_id` |
| DF-ACE-160 to DF-ACE-177 | `v_ace_plan` | 18 fields, keyed by `plan_ref` and `account_key` | ACE_READ: one SELECT per treatment; never copied |
| DF-TRT-034 to DF-TRT-061 | `dp_treatment`, `dp_guarantee_claim` | P1's dated DP04 copies | Not carried and not written here (ASM-0080) |
| DF-OPS-118 to DF-OPS-129 | `reconciliation_result` | The fields of a reconciliation row | Read for the clean-day count; written by JOB-04 |
| None (standard columns, LDM v11) | S2 `treatment` | `migration_source`, `migrated_at` | Provenance: written by S2's load |
| None: framework table | `flyway_schema_history` | The version, the description and the checksum of this story's version | Write, one row, at deploy only |

Field IDs are those in the Logical Data Model and Data Dictionary v11 and in TSD P1 v3 T3.3 and T3.6; the same package rows are to be held in Source to Target Mapping v7, sheet Migration packages (RD-P1-027). `rwb_source_data` holds no treatment table and no copy of a plan: there is no `treatment` object in the schema, and this story's version creates none. The extract itself is a file read once and a package handed over, not a table; Pending: its file layout, field order, record format, location, access and retention, agreed at the cutover rehearsal, owner data steward, tracked as GAP-0524 (ASM-0720).

The seven standard record columns of TSD P1 v3 T3.0 are carried by Workbench tables and never by a view, so no view field of this story is written or versioned by the Workbench. The DP04 copies are named in this table for the boundary only: the `business_date` snapshot that makes them a dated copy is their own writer's concern, and this story neither builds it nor seeds it (TSD P1 v3 T3.6 note on DF-TRT-050 and DF-TRT-051).

### 12. Contract

**12.1 REST operations provided**

None. The cutover runs from the release pipeline as one-off bulk work and is not a public operation: this story adds no path, no query parameter and no response field. The reconciliation read it relies on belongs to another RWB-SVC-P1 story and is named in 12.2, not claimed here. Architecture v5 slide 32 is the reason the shape is this one: a bulk cutover reaches Recovery through its APIs and never through its schemas.

**12.2 REST operations consumed**

One at run time by this story's own code, the account read of its own orphan check on this service's contract (RD-P1-060; RD-P1-068). The cutover step is a pipeline command, not a job of `GET /admin/jobs`, and the rerun operation does not apply to it (RD-P1-012); the pipeline reads the reconciliation results, and the tests read the case and the treatment through their owners' published contracts as mocks:

| Caller | Operation | Owner | Why it is not a dependency of this story |
|---|---|---|---|
| The cutover orphan check | `GET /api/recovery/source-data/v1/accounts/{accountKey}` (getAccount) | P1 rwb-source-data (RWB-P1-E1069-APP) | Same service, already a build dependency; reads the account key of each treatment |
| The release pipeline | `GET /api/recovery/source-data/v1/admin/reconciliation/results` | P1 rwb-source-data (API-P1-003) | Same service; the cutover record reads its evidence from it |
| The tests | `GET /api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | A contract mock only; the extract carries the case as the legacy dump holds it |
| The tests | `GET /api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | A contract mock only; the load into `rwb_treatment` is S2's own cutover step |

The story therefore holds no C dependency and no I dependency (metadata; ASM-0719). DP-11 is not a pattern of this story: there is no outbound call to build against, and no timeout of its own is added.

**12.3 Events published**

None. The cutover publishes no Kafka event, writes no outbox row and adds no schema to `rwb.source-data.events.v1`. The `AceDataReady` and `AceDataLate` events of this service belong to its freshness stories, and the treatment events of `rwb.treatment.events.v1` belong to S2 (Architecture v5 slides 42 and 43).

**12.4 Events consumed**

None. The cutover is started for a business date by the release pipeline; it reads no topic and no inbox row. The `reconciliation_result` rows it counts are written by JOB-04 and read from the table, not from an event.

**12.5 Workflows and activities**

None added. JOB-04 Reconciliation is ReconciliationWorkflow of this service, a child of AceIngestCheck, exercised here through its rows and not changed by this story (Architecture v5 slide 44). The cutover step itself is a batch job of the release pipeline, not a Temporal workflow, because it runs once per cutover business date and not on a schedule or on an event.

**12.6 Schedules**

None. No Temporal Schedule and no Quartz job sits in this story: the cutover is one-off bulk work, and the ten day count reads rows that JOB-04 already writes as a child of AceIngestCheck (Architecture v5 slides 32 and 44).

**12.7 Tables owned**

| Table | Schema | Owner (ownership map) | This story |
|---|---|---|---|
| `flyway_schema_history` | `rwb_source_data` | P1 | Writes one row for its own version at deploy |
| `reconciliation_result` | `rwb_source_data` | P1 | Read for the clean day count; written by JOB-04 and by no code of this story |
| `treatment` | `rwb_treatment` | S2 | Not written here: the load is S2's own cutover migration (DP-01) |
| `dp_treatment` | `rwb_source_data` | P1 | Not written here: the dated DP04 copy is built from events (ASM-0080) |
| `dp_guarantee_claim` | `rwb_source_data` | P1 | Not written here, for the same reason |

There is no treatment table in `rwb_source_data` and no copy of a plan in it, and this story adds neither. No statement in this story names a table in `public` and no statement names another service's schema (DP-01, DP-05).

**12.8 Contract fakes**

| Fake | Serves | Used for |
|---|---|---|
| Legacy cutover extract fixture | The legacy Workbench treatment and approval records of the open cases at cutover, as synthetic rows with their cases and their plan references | AC1, from Day 1, with no legacy data |
| View fixture (`v_ace_plan`) | Synthetic plan rows for the synthetic `plan_ref` values, one series with a plan row and one without | AC1 and the orphan path of X4 |
| rwb-treatment contract mock | The migrated treatment with its case, its type, its offer amount, its approval level and its outcome; and the migrated records served from schema `rwb_treatment` | AC1 and AC3, and the added Given of each |
| Reconciliation extract fixture | The `reconciliation_result` rows JOB-04 writes, PASS, BREAK and the REC-05 orphan row | AC3 and the reset path of X6 |

Each fake is generated from the published contract it fronts or from the fixture set agreed at the cutover rehearsal, so a contract change shows up as a test failure and not as a silent pass. The fixture layouts, the file name of the cutover dump and the cutover record format: Not specified in the source documents (GAP-0524; ASM-0720).

**12.9 Call-type summary**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 new operations | 0 from this story's code | The cutover is a pipeline command; its evidence is read from this service's reconciliation results, one hop, 2 s, the service standard of §R5.5 DP-11 |
| Kafka | None | None | No event published or consumed |
| Temporal | None | None | No workflow, activity or schedule added; JOB-04 is exercised, not changed |
| File | None | One | The cutover extract is read once from the legacy Workbench cutover dump, and the handover package leaves through the cutover record of the release pipeline |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata.cutover`, in the service root `th.co.scb.ace.workbench.recovery.sourcedata`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`, login `rwb_source_data`, topic `rwb.source-data.events.v1` and task queue `rwb-source-data`; the topic and the queue are named for completeness and this story uses neither.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CutoverTreatmentExtract | Batch job | The one-off read of the legacy Workbench cutover dump for the open cases at cutover; one pass per cutover business date, no table, no re-read |
| TreatmentCutoverMapper | Service | Maps each treatment to its case and its ACE business keys and keeps the CARRY and KEY fields of section 11, the five facts of AC1 among them; derives no value and defaults none |
| PlanRefReader | Repository | The only SQL of the story: one SELECT on `v_ace_plan` keyed by `plan_ref` and `account_key`; no write, no `public` table, no other schema |
| TreatmentHandoverPackage | Service | Assembles the handover row per treatment with its section 11 fields, `migration_source` and the cutover business date, with row count and checksum, and writes it to the cutover record |
| CutoverEvidenceReader | Service | Counts the clean days from the `reconciliation_result` rows of JOB-04 on the migrated records, resets on a break, and holds the ten day rows beside the sign-off |
| The next free version of the per-service sequence | Migration | Creates no table, no column and no index for a treatment or a plan row; records the extract's definition, the field list and the read-only window in its description |
| Cutover fixtures | Test fixture | The legacy cutover extract, the `v_ace_plan` rows, the rwb-treatment contract mock and the reconciliation rows, all synthetic |

**Pattern application**

| DP code | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies in its own-service form: this is the service that owns the views, so the plan read is its own SQL on its own login and adds no contract hop, and S2 never reads `v_ace_plan` for itself (Architecture v5 slide 45, "Who reads ACE's data?"). DP-15 gives the sequence the version runs on and the history row that records the cutover definition. DP-19 puts the cutover result behind the composite route of SCR-44 rather than one screen stitching two sources. No other pattern of the table applies: there is no event (DP-09), no parameter or reference read (DP-06, DP-07), no guard library of this story's own (DP-08), no outbound call (DP-11), no cross-service adapter (DP-16) and no rule evaluation (DP-04).

**Database and migrations**

- Reads `v_ace_plan`; writes no row at run time. The only write of the story is the Flyway history row of its own version.
- The version creates no table, no column, no index and no constraint: the treatment rows are S2's and the plan rows are ACE's, and `rwb_source_data` stores neither (BR1, BR7). Its description carries the extract's definition, its field list and the read-only window, so the next reader of the schema and of the history finds both facts.
- No grant is made or changed: the `rwb_source_data` login and its SELECT on the 30 views are RWB-P1-E1069-DB's, and the view definitions are RWB-P1-E1069-APP's.
- The version number is the next free one on the per-service sequence, after the `V0001` baseline and the two view versions of TSD P1 v3 T3.2. This story fixes no number and invents none; the cutover rehearsal applies it on the next free version of the day.
- The extract's field list is the CARRY and KEY rows of section 11 (RD-P1-027).

**Configuration and reference data**

- No parameter and no reference list is read: DP-06 and DP-07 are not in this story's pattern set. The ten day threshold, the cutover business date and the retention period of the legacy tables are data of the cutover record, not constants in code.
- Pending: the handover point, the package layout and the cutover record format, owner data steward, tracked as GAP-0524 (agreed at the cutover rehearsal).
- The feature switch is `rwb.source-data.dm004-cutover-extract`, from the platform flag library: off, the cutover step refuses to start and no package is handed over; the migration still applies because it creates nothing.
- The login is `rwb_source_data`: SELECT on the 30 views and no privilege in `public`.

**Build steps**

1. CutoverTreatmentExtract over the legacy cutover extract fixture, one pass per business date, with the absent-dump and the double-read cases; tests for AC1, AC7 and X1.
2. TreatmentCutoverMapper: the section 11 fields, the case key and the ACE business keys, no derived value and no default; tests for AC1, AC9, X2 and X3.
3. PlanRefReader over `v_ace_plan` with the plan-present and the plan-absent fixtures; prove one SELECT per treatment and no write; tests for AC1, AC8 and X4.
4. TreatmentHandoverPackage: the package assembled from the mapper and the plan read, with `migration_source` and the business date, and no row written to any schema; tests for AC1.
5. CutoverEvidenceReader: ten PASS rows count up, one BREAK row resets the count, a new REC-05 orphan resets it, and the sign-off is refused below ten; tests for AC3 and X6.
6. The migration on the next free version, as a no-op on the schema with the definition, the field list and the read-only window in its description, and the repeated-apply check; tests for AC1 and X7.
7. The refusal path through the rwb-access guard, with no read of the dump or of the plan view after a deny; test for TC-DM-004-04, and the mock run of the whole cutover so the story builds before S2's load and before JOB-04's real rows are live.

**Feature flag.** `rwb.source-data.dm004-cutover-extract`, from the platform flag library. Off: the step refuses to start, no package leaves, and the migration still applies because it creates nothing. **Rollback (RD-P1-045).** Flag off first; redeploy the previous tag only if the flag does not cover the fault; never reverse a migration. A repeated run for a recorded business date adds no package.

**Done when.** The tests of section 16 pass, `rwb_source_data` holds no treatment table and no plan copy, AC1 hands over a complete package with the plan read and never copied, AC3 counts ten clean days from `reconciliation_result` rows and records the sign-off, and no class of the service names a `public` table or another service's schema.

### 14. Validation and messages

| ID | Type | When | Message |
|---|---|---|---|
| MSG-GEN-001 | Error | The extract is missing a required field or record, such as a case, a treatment type, an offer amount, an approval level or an outcome | Enter {field}. |
| MSG-P4-002 | Error | A caller without the Platform administration right starts the cutover step | You cannot {action} here. Your role does not include it. |
| MSG-P1-001 | Warning | The ACE batch the plan read depends on is late for the business date, so the plan facts cannot be carried as current | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-023 | Error | A sign-off is asked below the required count of clean days | The cutover cannot be signed off. It has {count} clean days and needs {required}. |
| MSG-P1-012 | Warning | A reconciliation row for a migrated record is BREAK during the ten days, so the count resets | The case list for {date} does not reconcile to ALS for {product}: a difference of {variance} accounts, {pct} percent. |

A sign-off refused below ten clean days answers MSG-P1-023 (RD-P1-042; confirmation of its text is Pending, owner Error and Message Standard owner). Pending: the ACE view statement timeout, retry and database breaker policy, owner solution architect, tracked as NEW-GAP-W3M-003 (Error Handling and Resilience Standard v5 section 8.4); a failed view read stops the step (X5).

The other four messages are those of the legacy master (legacy RWB-DM-004 validation table; FSD P1 v3 VR-P1-011-1 and VR-P1-013-1); MSG-GEN-001 and MSG-P4-002 are copied character for character from it. This story raises MSG-GEN-001 and MSG-P4-002 itself: for MSG-GEN-001, {field} is the field or the record the extract lacks, and for MSG-P4-002, {action} is "run the treatment cutover extract" and never a case fact or a field value. MSG-P1-001 and MSG-P1-012 are raised by JOB-04 and by the freshness read of this service, and this story asserts them as evidence rather than producing them. No other message is raised by this story. The text of MSG-P1-001 and MSG-P1-012 is identical in Error and Message Standard v5. Pending: the message of a refused sign-off, tracked as NEW-GAP-S13-2.

### 15. Screens and states

SCR-44 screen states (empty: not specified in the source documents, CG-ALL-1912; loading: not specified in the source documents, CG-ALL-1912; error: not specified in the source documents, CG-ALL-1912; no access: not specified in the source documents, CG-ALL-1912). Screen Specifications v1 section SCR-44 lists Running, failed and complete.

SCR-45 screen states (empty: not specified in the source documents, CG-ALL-1913; loading: as listed in Screen Specifications v1; error: not specified in the source documents, CG-ALL-1913; no access: not specified in the source documents, CG-ALL-1913). Screen Specifications v1 section SCR-45 lists Loading and breaks.

No screen in this story. The cutover result is read on SCR-44 Interface and job monitor (FSD P1 v3 Screens table; Pending: how a pipeline command that is not a P1 job type appears there, owner solution architect, tracked as NEW-GAP-S12-3), and the breaks that reset the count are shown on SCR-45 Data quality, which RWB-AD-019 owns. Both are read through the gateway-bff composite route (DP-19, H RWB-PLT-N001-CON); this story adds no route, no field and no rendering, and the route's path, its merge order across the cutover record and the reconciliation rows are Not specified in the source documents (GAP-0524; ASM-0720). The states the cutover exposes are six:

| State | What the cutover record holds | What the monitor shows |
|---|---|---|
| Extract ready | The business date, the count of treatments mapped and the plan references resolved | The step is running and the extract is ready for handover |
| Handed over | The count handed over and the package identifier of the cutover record | The step is complete for the handover and the rows are with rwb-treatment |
| Loaded | The confirmation that the migrated records answer from `rwb_treatment` | The rows are served from the new schema |
| Ten clean days running | The count of consecutive clean days and the row of the last clean day | The count, its business date and the remaining days |
| Break | The BREAK row or the orphan, its date, its code and its owner role, and the count at zero | The break is listed and the count is reset |
| Signed off | The ten day rows, the reconciliation extract they came from and the sign-off of the data steward, with the read-only window of the legacy tables | The cutover is complete and the legacy tables are read-only |

A cutover that has not reached ten clean days shows as a count and not as a pass, so a cutover with one break in it is visible as a reset rather than as a zero, and the sign-off cannot be recorded below ten (AC3).



### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-004-01 | AC1; BR1, BR2, BR3, BR4 | End to end | The legacy cutover extract fixture with two open cases and three treatments, one with a plan row in `v_ace_plan` and one with a `plan_ref` that has none; the rwb-treatment contract mock; a row count of every table of `rwb_source_data` before and after |
| TC-DM-004-03 | AC3; BR5, BR6, BR9 | End to end | Ten consecutive PASS `reconciliation_result` rows for the migrated records, then one BREAK row and one REC-05 orphan row, then ten clean rows again; the sign-off recorded once at ten |
| TC-DM-004-04 | AC4; Access | Component | A caller whose Platform administration right R is absent in the authorise fake, starting the cutover step for a business date; a second call with the right present for the contrast |
| TC-DM-004-05 | AC5; BR7, BR8, BR10 | Component | The rwb-source-data Flyway sequence applied to an empty schema and then a second time; the service login with SELECT only and a statement scan for any public table; a scan of the cutover code and fixtures for business-value literals and personal data |
| TC-DM-004-06 | AC6; BR5, BR6 | End to end | Fewer than ten consecutive PASS `reconciliation_result` rows for the migrated records; the data steward's sign-off attempted; the cutover record read after the attempt |
| TC-P1-DM004-APP-01 | AC7 | Component and end to end | Repeated and failed handover of one business date |
| TC-P1-DM004-APP-02 | AC8 | Component | View fixture with a duplicate `plan_ref` on two accounts and a pair with no row |
| TC-P1-DM004-APP-03 | AC9 | Component | Cutover extract fixture with every treatment field |

The legacy test case numbers are kept, with their legacy numbering. `TC-DM-004-02`, the reconcile test of the legacy key, sits with the AC2 copy on RWB-ITG-DM004-ITG as `TC-DM-004-02-ITG` and is not repeated here; TC-DM-004-01-ITG and TC-DM-004-03-ITG are the integration copies of the two cases above, and this story owns the end to end ones. The full test, with its Given, When and Then, is recorded in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID.

The cutover reconciliation harness pack is agreed at the wave 4 entry check (owner role: Integration lead): SIT hosts per hop; a cutover extract fixture with the four keys and the orphan `plan_ref` as named fields; the SCR-45 composite route path and the break-list fields; the extract format and report retention; a gate that passes only on one break row per orphan and equal counts across a rerun; and a seeding set that is stub-served on Day 1 and replaced hop by hop as RWB-P1-DM004-APP lands.

### 17. Guardrails

- No business value in code: the five facts are data on the cutover row, the ten day target and the retention period are data of the cutover record, and the story writes no threshold, no currency amount and no date.
- Personal data: the extract carries case and treatment facts and ACE business keys, among them `plan_ref` (Confidential, Customer data; shown within the role's scope) and `account_key` (Confidential, Indirect identifier; shown within the role's scope and masked in UAT), as the data classification inventory classes them. It carries no other personal data and no contact or identity field. Neither key value is written to a log or a prompt; the fixtures are synthetic.
- ACE data only through the owner's contract or `v_ace_*` views, and here the service is the owner of the views: one login, SELECT only, no `public` table named in any statement (BR8).
- No copy of an ACE row: `v_ace_plan` is read and its plan facts are referenced, never copied, and `rwb_source_data` holds no plan row (BR3, BR4).
- No cross-schema write: the load into `rwb_treatment` is S2's own cutover step on S2's own sequence, and this story holds no INSERT against another service's schema (BR1, DP-01).
- No booking and no approval: the migration books no plan and approves no treatment; the approval level is a copied fact (BR3).
- One version on the per-service sequence, never edited in place; a later change is a new version with its own history row (DP-15).
- A cutover is never declared on a count that has been reset: a break sets the count to zero and the sign-off stays closed (BR5, BR6).

### 18. Traceability

| Legacy RWB-DM-004 row | Value (verbatim) | Feature link | L3 process link | Where it lands |
|---|---|---|---|---|
| Epic | E2, release 31 December 2026 | None | All recovery processes | Metadata release and wave; section 2 quotation |
| Module | P1 Recovery data engine | None | All recovery processes | Service rwb-source-data, service epic RWB-SVC-P1 |
| Feature | None | None | All recovery processes | No feature grouping is used |
| Process | All recovery processes | None | All recovery processes | The cutover covers the treatment records of every process the legacy key names |
| Priority | Must | None | All recovery processes | Sections 1, 2 and 19 |
| Depends on | RWB-E1-001, RWB-E1-069 | None | All recovery processes | Rebased by D-RCV-60 onto RWB-P1-E1001-APP and RWB-P1-E1069-APP, with RWB-PLT-E1044-CON and RWB-PLT-N001-CON (metadata) |
| Decision | DL25 | None | All recovery processes | BR5; the ten clean days as the cutover evidence; DL25 option A applied by RD-P1-042, with assumptions ASM-0728, ASM-0735, ASM-0743, ASM-2602 |
| Story | As a data steward, I want the agreed but unbooked treatments and their approvals migrated from the legacy Workbench, so that a restructure, settlement or deed already promised to a customer continues without a break at cutover. | None | All recovery processes | Section 1 statement; section 2 quotation; BR1 to BR4 |
| Data | recovery_case, treatment, v_ace_plan with their field ranges | None | All recovery processes | Section 11; AC1 |
| Screen and states | SCR-45 Data quality; Loading, breaks | None | All recovery processes | Section 15, with the cutover result read on SCR-44 and the breaks on SCR-45 |
| Permission checks | Platform administration R, six roles | None | All recovery processes | Section 10; TC-DM-004-04 |
| Validation and messages | MSG-P1-001, MSG-P1-012, MSG-GEN-001, MSG-P4-002 | None | All recovery processes | Section 14 |
| Test cases | TC-DM-004-01 to TC-DM-004-04 | None | All recovery processes | Section 16; TC-DM-004-02 sits on RWB-ITG-DM004-ITG; TC-DM-004-05 covers BR7, BR8, BR10; TC-DM-004-06 covers AC6 |
| Guardrails | No value a business person may change in code; no personal data; no read of another module's tables; a migrated record keeps its source and its migration date and never a copy of an ACE row | None | All recovery processes | BR4, BR8, BR10; section 17 |

| Pattern | Source | Applied as |
|---|---|---|
| DP-05 | Template and Rules §R5.5 | `v_ace_plan` is read by this service on its own login, and by no other service (section 13) |
| DP-15 | Template and Rules §R5.5 | The version on the per-service sequence, with the history row that records the cutover definition (section 13, AC1) |
| DP-19 | Template and Rules §R5.5 | The cutover result is read through the gateway-bff composite route behind SCR-44, not stitched by a screen (section 15) |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1044-CON | Contract | H build dependency: the per-service Flyway sequence and its history |
| RWB-PLT-N001-CON | Contract | H build dependency: the gateway-bff composite route behind SCR-44 |
| RWB-P1-E1001-APP | App development | H build dependency: the recovery tables and the data product catalog of the service |
| RWB-P1-E1069-APP | App development | H build dependency: the Section A views, `v_ace_plan` among them |
| RWB-P1-E1011-APP | App development | Writes the `reconciliation_result` rows the clean-day count reads |
| RWB-P1-DM003-APP | App development | The case and ownership slice of the same cutover, which supplies the case keys |
| RWB-ITG-DM004-ITG | Integration | Owns the AC2 reconciliation across the services and the ITG copies of the test cases |
| S2 rwb-treatment stories | App development | Own `rwb_treatment`, its Flyway sequence and the load of the rows this story hands over |

External dependencies: None. The story adds no X row of its own.

### 19. Out of scope

- The load into `rwb_treatment`, S2's Flyway sequence and every table of S2: they are S2 rwb-treatment's, and this story hands the rows over and stops (DP-01, DP-15).
- The dated DP04 copies `dp_treatment` and `dp_guarantee_claim`: built from events by their own writer and read-only for reporting; this story adds no writer, no seed and no rebuild (ASM-0080).
- The AC2 reconciliation of the business keys and its REC-05 orphan list across the services: RWB-ITG-DM004-ITG, with the ITG copies of the test cases.
- JOB-04, its REC-01, REC-02 and REC-05 checks, and the `reconciliation_result` rows: RWB-P1-E1011-APP.
- The SCR-45 Data quality console and its break list: RWB-AD-019.
- The views themselves, the per-service login and its grant: RWB-P1-E1069-DB and RWB-P1-E1069-APP. This story neither creates, alters nor grants a view.
- The data product catalog rows and DP04's definition: RWB-P1-E1001-APP.
- The booking of a plan, the treatment state machine, the approval decision and the contract of a treatment: S2 rwb-treatment, rwb-payment and rwb-decision, not a migration.
- The retention rule and the archive mechanics behind the read-only window: RWB-P1-E1017-APP.
- The platform configuration of Kafka, Temporal, the gateway and its routes: the platform epics.
- Any REST operation, Kafka event, Temporal workflow, Schedule or screen: this story builds none and section 12 says so table by table.

### 20. Remaining delivery steps

- Size the story (squad, role RW-TRIBE).
- Record the signed epic design of EP08 (product owner).
- Confirm the platform contracts as Done and their fakes published (solution architect).
- Agree the package layout, location, access and retention at the cutover rehearsal (data steward; GAP-0524).
- Confirm the MSG-P1-023 sign-off message and its applicability (Error and Message Standard owner).
- Provide the synthetic cutover, plan view and reconciliation fixtures in DEV (squad).
- Add the version 3 test rows to Test Cases v9 and the traceability matrix (QA).
