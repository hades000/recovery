# RWB-P1-DM006-APP Migrate collateral and assets
SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd


**Version 3 changes** (27 November 2026, D-RCV-60 P1 developer readiness, RD-P1 register)

- RD-P1-021 and RD-P1-027: P1 extracts, S5 writes `listing` and `asset_sale`, P1 writes only `valuation_ext`; section 11 is a closed field list and migrated rows carry `migration_source` and `migrated_at` (findings #1, #2).
- RD-P1-001, RD-P1-012, RD-P1-042 and RD-P1-043: replay, trigger and identity, clean day, Section B absence and exception messages are fixed (findings #4, #7, #8, #9).
- AC1, AC3, AC4, AC7 and AC8 rewritten and AC9 to AC11 added (findings #2, #3, #4); SCR-45 inputs stated (finding #6).
- Still pending: legacy retention period (GAP-2168), package layout and delivery steps in section 20 (findings #5, #10).
- Batch D and the finishing pass: the `asset_key` orphan check is this story's own cutover check through `GET /collateral/{assetKey}`, counted in its evidence and not a REC-05 row (AC12; RD-P1-068; RD-P1-060); S5 loads under its own workload identity (RD-P1-068); a refused sign-off answers MSG-P1-023 (RD-P1-042); MSG-GEN-006 follows Error and Message Standard v6; test case IDs of Test Cases v9 cited.

| Item | Value |
|---|---|
| Story key | RWB-P1-DM006-APP |
| Work type | APP |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-DM-006 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not set; the squad sizes it at refinement |
| Patterns applied | DP-05, DP-15, DP-19 |
| Parallel lane | L-P1-A |
| Ready to start | After RWB-P1-E1001-APP, RWB-P1-E1069-APP (both not yet built; named in Depends on (build)) |
| Depends on (build) | RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| Contract dependencies | None |
| Integration dependencies | None |
| Reference data | The extract and the load read no list and no parameter; `recon.tolerance.pct` version 1 = 0.00 is applied by JOB-04 (RD-P1-042) |
| Contract version | rwb-source-data.yaml 5.1.0 and rwb-asset.yaml of API Specification v7 |
| Readiness decisions | RD-P1-001; RD-P1-005; RD-P1-012; RD-P1-021; RD-P1-024; RD-P1-027; RD-P1-041; RD-P1-042; RD-P1-043; RD-P1-045; RD-P1-060; RD-P1-068 |
| External dependencies | None |
| Harness pack | Contents fixed (GAP-0446; ASM-0638): SIT environment and base hosts for rwb-source-data, rwb-asset, rwb-case, rwb-access and gateway-bff; cutover fixture layout; SCR-45 composite route path and break-list fields; extract format, delivery and retention; pass or fail gate; seeding set. The environment values are recorded in the harness README and pinned in the run report. Owner: integration lead. |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 8 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Change log: v1, 22 November 2026, D-RCV-60, T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a data steward, I want the listings, the case asset links and the open sale instructions migrated from the legacy Workbench, so that an asset already offered for sale is not lost at cutover while the collateral, appraisal and NPA asset records are read from ACE.

After the realignment this story carries the part of that sentence that belongs to `rwb-source-data`:

- the appraisal-acceptance decision, held in the extension table `valuation_ext` and keyed by `valuation_key`, because it is a Workbench decision about an ACE appraisal and not a copy of it;
- the DP06 read path — `v_ace_collateral`, `v_ace_collateral_detail`, `v_ace_valuation`, `v_ace_asset`, `v_ace_npa_asset`, `v_ace_npa_sale` — read through the service's own views and its published contract, never a `public.*` table;
- the cutover gate for DP06 in the service's own schema: the migration run, its break list and the evidence the data steward signs off.

The `listing` and `asset_sale` rows are S5 rwb-asset's, in schema `rwb_asset`: this story extracts them and hands them over, S5 writes them on its own sequence, and P1 writes only `valuation_ext` (RD-P1-021).

### 2. Business rationale

An asset already offered for sale must survive the switch from the legacy Workbench to the 19 services. Under the realignment nothing of the collateral or NPA estate is carried across: ACE holds it, ingested from CCMS, SVAF, AMIS and RPS, and the Workbench reads it (DP-05). What the Workbench does own is the decision about an appraisal — accepted, by whom, when, which panel valuer, stale after its cycle — and that decision belongs in exactly one schema.

Two consequences drive this story:

1. **One number, one source.** DP06 "Collateral and assets" names one system of record for each part: ACE for the collateral, appraisal, NPA asset and NPA sale records, the Workbench for the appraisal acceptance and the sale instruction. Copying an ACE row into `rwb_source_data` would create a second copy that disagrees with ACE and is owned by nobody who maintains the source (D-RCV-35 U1).
2. **Cutover is a data decision, not a deployment step.** The legacy estate is a live estate: a property listed for auction, a sale instruction open with a vendor and an appraisal accepted last month are all in flight at the switch. The cutover therefore keeps a gate — extract, map to business keys, load, check, sign off — and the gate is only passed on evidence.

DP-15 puts the migration on the service's own Flyway sequence, so the change ships with the service and rolls back with it, and DP-19 keeps the data quality screen behind one gateway-bff composite route, so the service exposes no screen of its own.

### 3. Preconditions

| # | Precondition |
|---|---|
| 1 | The `rwb_source_data` schema, its login and the baseline including the four extension tables are deployed, `valuation_ext` among them (RWB-P1-E1001-APP). |
| 2 | The 16 Section A views and the 14 Section B views are deployed and the conformance test is green; the Section B views over `valuation`, `collateral_detail`, `npa_asset` and `npa_sale` need RWB-ACE-001 (RWB-P1-E1069-APP; DL43 planning basis A, RD-P1-043). In DEV and the pipeline the Section B views run over the synthetic fixture. |
| 3 | The per-service Flyway sequence is available at the next free version in `rwb_source_data` (DP-15; RWB-PLT-E1044-CON). |
| 4 | The data quality screen is reachable through the gateway-bff composite route (DP-19; RWB-PLT-N001-CON). |
| 5 | The user holds Platform administration, right R: RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM or RW-SECADM (legacy RWB-DM-006 permission table; TSD P1 T6.1). |
| 6 | The legacy Workbench tables are available read only for the one-off extract, and the ACE batch record shows a COMPLETED row for every DP06 source for the cutover business date (T3.7). |
| 7 | S5's `listing` and `asset_sale` carry `migration_source varchar(20)` and `migrated_at timestamptz`, added by S5 in its own Flyway step (RD-P1-027). Pending: the values of LOV-MIGRATION-SOURCE, owner data owner (GAP-3275). |

### 4. Flow

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System (recovery service identity) | The release pipeline starts the step for one cutover business date under the `rwb_source_data` service identity and one Idempotency-Key (a UUID); it reads the legacy listing, case asset link, sale instruction and appraisal acceptance records | Rejects a row with no `asset_key` or no `valuation_key`, counts it and lists it |
| 2 | System | Maps each row to the new schema: acceptance to `valuation_ext` by `valuation_key`, every asset link to `asset_key` as `varchar(255)` with no foreign key, and the listing, sale and case asset link rows to one package per cutover business date for S5 with the section 11 fields, row counts and checksum | Applies BR-P1-001-3 and BR-P1-001-5 |
| 3 | System | Runs the cutover migration at the next free Flyway version in `rwb_source_data` | Adds `migration_source` and `migrated_at` to `valuation_ext`, commits one batch of `valuation_ext` rows with both set, writes the row count per object, leaves no partial load; writes no `rwb_asset` or `rwb_case` row |
| 4 | System | Checks the DP06 read path: the six DP06 views answer and `valuation_ext` joins `v_ace_valuation` 1:1; runs this story's own `asset_key` orphan check, reading each key through `GET /collateral/{assetKey}` | Writes the break list and the orphan list; an `asset_key` orphan is counted in the cutover evidence and writes no REC-05 row (RD-P1-068) |
| 5 | System | Publishes the cutover evidence as reconciliation extract rows behind SCR-45 Data quality | Shows counts, breaks and the DP06 freshness stamp (LOADED or STALE) |
| 6 | Data steward | Reviews the breaks and signs off (section 10) | Records the sign-off |
| 7 | System | Serves the migrated records from `rwb_source_data` and keeps the legacy tables read only | Cutover complete |

### 5. Exception paths

| # | Condition | Handling | Covered by |
|---|---|---|---|
| 1 | A legacy row carries no `asset_key` or no `valuation_key` | The row is refused, counted and listed for the data steward; nothing is written for it (BR-P1-001-3). MSG-GEN-001 with {field} the missing key. | AC1 |
| 2 | A `valuation_key` has no row in `v_ace_valuation` | The REC-05 orphan is listed for the data steward and the ACE team; no Workbench record is deleted or changed (BR-P1-011-3). The date is not clean; MSG-P1-012 is shown with the reconciliation result. | AC5 |
| 3 | Section B is not deployed when the cutover runs | The acceptance rows stay behind their feature flag, DP06 shows STALE with no business date and MSG-P1-001, no day counts as clean and the cutover is not signed off (T3.7; RD-P1-043). | AC3 |
| 4 | A view returns an error during the check | No reconciliation row is written for the business date; the run shows FAILED with MSG-GEN-006 for system "ACE database"; `POST /admin/jobs/{jobId}/rerun` of the FAILED JOB-04 run writes the rows (RD-P1-012). | AC6 |
| 5 | The migration is run twice | Flyway reports the version as already applied; the row counts per object are unchanged; no batch is written twice. No message. | AC7 |
| 6 | A user without the right tries the action | Refused with 403 MSG-P4-002 (401 MSG-P4-001 with no session); nothing changes. | AC8 |
| 7 | The legacy tables are held read only past the retention period | Pending: the period, owner data steward, tracked as GAP-2168. No message. | AC3 |
| 8 | The package write fails, or S5 is unavailable or refuses rows | No package is accepted from a failed write; the record shows the handover outcome and the refused keys; a retry for the date delivers each source key once and P1 writes no S5 row. No message. | AC9 |
| 9 | The step fails after the `valuation_ext` write and before S5 accepts the package | The record stays open; the retry leaves each acceptance and each handed key exactly once and no sign-off is possible until both are done. No message. | AC10 |
| 10 | A handed `asset_key` has no collateral row (`GET /collateral/{assetKey}` answers 404) | The key is listed by this story's own orphan check and counted in the cutover evidence; no Workbench record is deleted or changed and no REC-05 row is written, so the clean-day count of RD-P1-042 does not count it. No message. | AC12 |
| 11 | A sign-off is asked below ten clean days | The sign-off is refused with the count and no sign-off record is written. MSG-P1-023. | AC3 |

GAP-0531 sequencing: asset_key is proven against v_ace_asset and v_ace_collateral from Day 1; valuation_key is proven against v_ace_valuation from the week RWB-ACE-001 is deployed and against its contract fake before that week; the appraisal acceptance rows load in both cases; the cutover stays behind its feature switch until the Section B views answer, so no day counts as clean on a STALE DP06 stamp. Owner: solution architect with the ACE team lead and the data steward.

GAP-0529 handover: P1 extracts the listing, the case asset link, the sale instruction and the appraisal acceptance; it loads the appraisal acceptances into valuation_ext idempotently on valuation_key; it hands the listing, the sale and the case asset link to S5 in one package per cutover business date; S5 loads them into rwb_asset on its own sequence, under the workload identity and migration owner of rwb-asset, because SY-DATALOAD is retired (RD-P1-068). The case asset link rides on the handover row as the case key beside the asset_key and lands in no table of its own. The source tag and the cutover business date ride on the handover row and in the Flyway history description. Owner: solution architect with the data steward and the S5 rwb-asset tech lead.

### 6. INVEST check

| Letter | Check | Verdict |
|---|---|---|
| I | Independent | Yes: one service, one schema, one Flyway version; it builds against CON stories and their fakes. |
| N | Negotiable | Yes: the evidence format is open until the cutover rehearsal; the tolerance is fixed (RD-P1-042). |
| V | Valuable | Yes: an asset in flight at cutover is not lost, and DP06 has one owner per number. |
| E | Estimable | Yes: four legacy objects, two tables in scope for this service, one cutover gate. |
| S | Small | Yes: four TCs, two ACs, one migration version. |
| T | Testable | Yes: counts, an orphan list and a sign-off are observable. |

### 7. Acceptance criteria

```gherkin
Feature: Migrate collateral and assets

  Scenario: AC1 Extract the Workbench records (legacy RWB-DM-006 AC1)
    Given the rwb-asset contract mock returns the listing and asset_sale records for each asset_key
    Given the legacy Workbench listing, case asset link, sale instruction and appraisal acceptance records at cutover
    When the migration reads them
    Then each listing and each sale carries its asset_key, and each appraisal decision its valuation_key
    And no collateral, appraisal, NPA asset or NPA sale record is copied, because each is read from v_ace_collateral, v_ace_valuation, v_ace_asset, v_ace_npa_asset or v_ace_npa_sale
    And the appraisal acceptances are inserted into "rwb_source_data.valuation_ext" keyed by "valuation_key" with "migration_source" and "migrated_at"
    And one package for the cutover business date holds the listing, sale and case asset link rows with the CARRY and KEY fields of section 11, row counts and checksum
    And P1 writes no row in "rwb_asset" or "rwb_case" and no event or outbox row

  Scenario: AC3 Cut over (legacy RWB-DM-006 AC3)
    Given ten clean days on the migrated records, counted from the JOB-04 reconciliation_result rows: a day on which every REC-01 and REC-02 row is PASS under "recon.tolerance.pct" version 1 = 0.00, no new REC-05 orphan appears and DP06 is LOADED counts; a BREAK row, a new orphan or a STALE DP06 day resets the count to zero
    When the data steward signs off
    Then the legacy tables stay read-only for their retention period
    And the ten day rows, the DP06 stamps and the sign-off are held in the cutover record of the release pipeline
    And the migrated records are served from the new schema
    And "GET /data-products/DP06/records" with the "caseId" of a migrated case returns the accepted valuation rows
    When a sign-off is asked with 9 clean days
    Then it is refused with "MSG-P1-023" "The cutover cannot be signed off. It has 9 clean days and needs 10." and no sign-off record is written

  Scenario: AC4 The extract changes no listing or sale status (new, D-RCV-60)
    Given a synthetic listing with a "status" held in the legacy record and a synthetic asset sale linked to it
    When the extract is mapped and handed over
    Then the package carries the "status" unchanged
    And P1 writes no row in "rwb_asset" and changes no listing or sale status

  Scenario: AC5 A valuation_key orphan is listed and nothing is deleted (new, D-RCV-60)
    Given a valuation_key that has no row in v_ace_valuation
    When the REC-05 check runs
    Then the orphan is listed for the data steward and the ACE team
    And no Workbench record is deleted or changed

  Scenario: AC6 A view error during the check fails the run (new, D-RCV-60)
    Given a view returns an error during the check
    When the check runs for a business date
    Then no reconciliation row is written for that business date
    And the run shows FAILED with MSG-GEN-006 for system "ACE database"
    And "POST /admin/jobs/{jobId}/rerun" of that FAILED run writes the rows

  Scenario: AC7 A second apply of the version writes nothing twice (new, D-RCV-60)
    Given the Flyway version of this story has been applied
    When it is applied again
    Then Flyway reports the version as already applied
    And the row counts of "valuation_ext" are unchanged and no batch is written twice

  Scenario: AC8 A user without the right is refused (new, D-RCV-60)
    Given a request with no session and a user without the Platform administration right to run the cutover
    When each starts the cutover step for a business date
    Then the answers are 401 "MSG-P4-001" and 403 "MSG-P4-002" "You cannot run the collateral and asset cutover here. Your role does not include it."
    And the legacy records are not read, no row is written and no package is produced

  Scenario: AC9 A repeated or failed handover delivers each key once
    Given the package of business date "2026-12-31" is recorded and the rwb-asset contract fake accepted every key
    When the step is started again for "2026-12-31"
    Then the recorded result is returned and the fake holds each "asset_key" row once
    Given the rwb-asset fake is unavailable on first delivery
    Then the record shows the handover outcome as failed and a retry delivers each key once

  Scenario: AC10 A failure between the two writes leaves one acceptance and one handover
    Given the step fails after the "valuation_ext" batch commits and before the package is accepted
    When the step is run again for the date
    Then each "valuation_key" has one row, each handed key appears once and no sign-off is open before both are done

  Scenario: AC11 Section B absent keeps the cutover gated
    Given the Section B views are not deployed and DP06 answers STALE with no business date
    When the clean-day check runs for the date
    Then the day does not count, the record states DP06 STALE with MSG-P1-001 and the sign-off stays closed

  Scenario: AC12 An asset_key orphan is found by the story's own check
    Given a handed listing whose "asset_key" "ASSET-SYN-0999" makes "GET /collateral/ASSET-SYN-0999" answer 404
    When the cutover orphan check runs
    Then "ASSET-SYN-0999" is listed for the data steward and counted in the cutover evidence
    And no Workbench record is deleted or changed and no "reconciliation_result" row is written for it
```

The legacy AC2 (reconcile the business keys, the REC-05 step) is not owned by this story; it sits with the reconciliation deliverable of the same legacy key, together with TC-DM-006-02 (ASM-3482).

S5 rwb-asset owns `listing` and `asset_sale` (RD-P1-021). This story writes `valuation_ext`, hands the S5 rows over and validates each `asset_key` link against the rwb-asset contract fake. AC4 states what the extract does not change; Pending: the disallowed listing or sale status transition and the S5 story that proves it, owner rwb-asset service owner, tracked as GAP-3542.

### 8. Business rules

| BR ID | Rule text (legacy wording kept, schema named for this service) |
|---|---|
| BR-P1-001-2 | The recovery module reads ACE only through `recovery.v_ace_*` — here `rwb_source_data`'s own `v_ace_*` views. A direct `public.*` read in a story, spec or query is a defect. |
| BR-P1-001-3 | No constraint in this service's schema references a table outside it. A link to a source record is a business-key column of type `varchar(255)` with no foreign key. |
| BR-P1-001-5 | An extension table holds a Workbench decision about an ACE record and never a copy of an ACE column. It is 1:1 with the ACE record and carries the seven standard record columns. |
| BR-P1-011-3 | A REC-05 orphan never deletes or changes a Workbench record; it is listed for the data steward and, where the row is missing in ACE, for the ACE team. |
| RD-P1-068 | The `asset_key` orphan check is this story's own cutover check, counted in its evidence; the REC-05 scope of RD-P1-022 holds no `asset_key`. |
| BR-P1-014-3 | A product fed by more than one source carries the oldest business date among its sources, and is STALE while any of them is late. DP06 is fed by CCMS, SVAF, AMIS and RPS. |
| Not specified in the source documents (DOR-RWB-P1-DM006-APP-4); pattern DP-15 | The migration runs at the next free Flyway version in `rwb_source_data`. No object is created in another service's schema and no shared baseline is reused. |
| Not specified in the source documents (DOR-RWB-P1-DM006-APP-4); pattern DP-19 | The data quality screen is one gateway-bff composite route. The service publishes no screen route of its own. |

### 9. State transitions

State names for a migration batch are Not specified in the source documents (GAP-2169; ASM-3481). The transitions below use the existing lists LOV-FRESHNESS (LOADED, STALE) and the cutover gate of AC3.

| From | To | Trigger | Evidence |
|---|---|---|---|
| (none) | Extracted | the cutover run reads the legacy records | row count per legacy object |
| Extracted | Loaded | the Flyway version commits in `rwb_source_data` | row count per object; package accepted by S5; DP06 LOADED |
| Loaded | Reconciled | REC-05 lists no `valuation_key` orphan and the story's own check lists no `asset_key` orphan | empty orphan list |
| Reconciled | Signed off | the data steward signs off | sign-off recorded; ten clean days of AC3 |
| Signed off | Cut over | the cutover date arrives | legacy tables read only; acceptances served from `rwb_source_data` and listings and sales from `rwb_asset` |
| Loaded, Reconciled | Held | an orphan, a refused row or a missing Section B view | break list on SCR-45: Data quality |
| LOADED | STALE | a DP06 source batch is late or failed | DP06 freshness stamp (T3.7) |

### 10. Authority

| Decision | Role that holds it | Right |
|---|---|---|
| Run or rerun the cutover step (a pipeline command under the `rwb_source_data` identity, SELECT on the views and DML on `valuation_ext` only) | Platform administrator (RW-PLATADM) | Platform administration, C and U |
| Read the break list and the cutover evidence | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Platform administration, R |
| Sign off the cutover | Data steward and data product owner (RW-DATASTEW) | Platform administration, R, as the legacy RWB-DM-006 permission table gives it |
| Change the reconciliation tolerance used by AC3 | Centre of excellence (parameter `recon.tolerance.pct`, version 1 = 0.00, DL25 option A) | n/a; a parameter, not a code value |

The story starts no approval workflow and holds no authority of its own; every action is checked by the capability area of the screen or the job, and the sign-off is the data steward's right, not a new role.

### 11. Data

| Entity | Fields | Field IDs | Disposition (RD-P1-027) |
|---|---|---|---|
| `valuation_ext` | `valuation_key` | DF-EXT-036 | KEY: written by this story in `rwb_source_data` |
| `valuation_ext` | `accepted`, `accepted_at`, `accepted_by`, `valuer_partner_id`, `stale_flag`, `age_days` and the seven standard columns | DF-EXT-037 to DF-EXT-049 | CARRY: written by this story |
| `listing` | `id`, `sale_channel`, `start_price`, `floor_price`, `round_no`, `listed_at`, `status` | DF-SAL-001, DF-SAL-003 to DF-SAL-008 | CARRY: handed to S5, which writes `rwb_asset` |
| `listing`, `asset_sale` | `asset_key` | DF-SAL-002, DF-SAL-010 | KEY |
| `asset_sale` | `id`, `listing_id`, `gain_loss` | DF-SAL-009, DF-SAL-011, DF-SAL-018 | CARRY: handed to S5 |
| `asset_sale` | `contract_date`, `sale_date`, `sale_price`, `transfer_fee`, `specific_business_tax`, `corporate_income_tax`, `incentive_amount` | DF-SAL-012 to DF-SAL-017, DF-SAL-019 | ACE_READ (AMIS): never carried |
| `recovery_case` (the case asset link) | `id` | DF-CAS-001 | KEY: rides on the package row beside `asset_key`; lands in no table of its own. All other case fields EXCLUDE |
| ACE reads | `v_ace_collateral` 8 fields; `v_ace_asset` 9; `v_ace_valuation` 9; `v_ace_collateral_detail` 12; `v_ace_npa_asset` 12; `v_ace_npa_sale` 11 | DF-ACE-091 to DF-ACE-107, DF-ACE-187 to DF-ACE-230 | ACE_READ: read only, never copied |
| `valuation_ext`, `listing`, `asset_sale` | `migration_source`, `migrated_at` | Standard columns, LDM v11 | Provenance: P1 adds and sets them on `valuation_ext`; S5 on its tables |

The same rows are to be held in Source to Target Mapping v7, sheet Migration packages. Pending: the package file layout, location and access, agreed at the cutover rehearsal, owner data steward, tracked as GAP-3541.

### 12. Contract

Contract version built against: rwb-source-data.yaml 5.1.0 (API Specification v7) for the own-service reads and `rwb-asset.yaml` of the same folder for the `rwb-asset` contract fake.

**12.1 REST operations provided**

None. The legacy story states that it has no endpoint: "the migration is a cutover step run by the recovery service identity, and its breaks are listed on the reconciliation extract." The realignment keeps that, so this story adds no operation to `/api/recovery/source-data/v1`.

**12.2 REST operations consumed**

| Operation | Service | Use in this story |
|---|---|---|
| GET /api/recovery/source-data/v1/data-products/freshness | rwb-source-data (own service) | Reads the DP06 stamp (LOADED or STALE) for the cutover evidence |
| GET /api/recovery/source-data/v1/data-products/DP06/records?caseId={caseId} | rwb-source-data (own service) | Proves the migrated records and the ACE views answer together after the cutover |
| GET /api/recovery/source-data/v1/admin/reconciliation/results | rwb-source-data (own service) | Reads the REC-05 orphan list that gates the sign-off |
| GET /api/recovery/source-data/v1/collateral/{assetKey} (getCollateral) | rwb-source-data (own service, RWB-P1-E1069-APP) | The `asset_key` orphan check of step 4 (RD-P1-068; RD-P1-060) |

No operation of another service is called; the `rwb-asset` payload in AC1 is a contract fake (12.8).

**12.3 Events published**

None. The migration publishes no fact; EV-26 AceDataReady and EV-27 AceDataLate (`rwb.source-data.AceDataReady.v1`, `rwb.source-data.AceDataLate.v1`) belong to RWB-P1-E1015-APP.

**12.4 Events consumed**

None.

**12.5 Workflows and activities**

None. The service runs no Temporal workflow for this story and the queue `rwb-source-data` carries none; the cutover is a one-off migration run, not a workflow.

**12.6 Schedules**

None. The cutover is a one-off run at the cutover date, not a Temporal Schedule; JOB-01 and JOB-09 are retired and JOB-04 is ReconciliationWorkflow, delivered by RWB-P1-E1011-APP.

**12.7 Tables owned**

| Schema | Table | Key | Written by this story |
|---|---|---|---|
| rwb_source_data | valuation_ext | valuation_key, `varchar(255)`, no foreign key | Yes: one row per acceptance, with the seven standard columns |

`listing` and `asset_sale` are not in this schema (GAP-2167; ASM-3479).

**12.8 Contract fakes**

| Fake | Used for | Values kept |
|---|---|---|
| `rwb-asset` contract fake | The listing and asset_sale payload of AC1, AC9 and AC10 | `asset_key` on every listing and every sale |

**12.9 Call-type summary**

| Call type | Used | Detail |
|---|---|---|
| REST | Yes | Three own-service reads of 12.2; no other service is called |
| Kafka | No | No event is published or consumed |
| Temporal | No | No workflow, activity or task queue |
| File | Yes | One cutover evidence extract (counts, breaks, orphan list) handed to SCR-45 |

### 13. Solution plan

| Component | Work in this story |
|---|---|
| Cutover migration | One new Flyway version on the `rwb_source_data` sequence (DP-15): `V<seq>__rwb_p1_dm006_valuation_cutover.sql` adds `migration_source` and `migrated_at` to `valuation_ext` and inserts it from the legacy extract by `valuation_key`, rerun safe, one transaction per batch |
| RecoveryDataEngineService | Maps the extract, applies BR-P1-001-3 and BR-P1-001-5, counts rows per object, builds the break and orphan lists |
| RecoveryDataEngineRepository | Reads and writes `valuation_ext` only; no other table of the schema is touched |
| S5 handover | Builds the package per cutover business date with the section 11 fields, row counts and checksum; accepted only when the written file matches both |
| AceSourceReadRepository | SELECT only on the six DP06 views for the AC1 proof; names no `public` table |
| SCR-45 Data quality | Gateway-bff composite route (DP-19); shows LOADED or STALE, the counts and the break list |
| Acceptance tests | TC-DM-006-01 (component), TC-DM-006-03 (end to end), TC-DM-006-04 (contract) and the version 3 rows of section 16 |

No view and no table is created; the only schema change is the two provenance columns: those are the H dependencies (`RWB-P1-E1001-APP`, `RWB-P1-E1069-APP`). The `rwb-asset` side of the payload is not built here.

**Rollback (RD-P1-045).** Switch the feature flag off first; redeploy the previous tag only if the flag does not cover the fault; never reverse a migration. A faulty row set is corrected by a new forward version.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-012 | Warning | The case list for {date} does not reconcile to ALS for {product}: a difference of {variance} accounts, {pct} percent. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-GEN-006 | Error | {system} is not available. Try again in a few minutes. |
| MSG-P1-023 | Error | The cutover cannot be signed off. It has {count} clean days and needs {required}. |
| MSG-P4-001 | Error | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

Pending: the ACE view statement timeout, retry and database breaker policy, owner solution architect, tracked as GAP-3566 (Error Handling and Resilience Standard v5 section 8.4); a failed view read fails the run and the FAILED run is rerun (AC6). Confirmation of the MSG-P1-023 text is Pending, owner Error and Message Standard owner.

### 15. Screens and states

| Screen | States |
|---|---|
| SCR-45 Data quality | Loading; breaks. This story supplies the DP06 stamp, the row counts per object, the break list and the orphan list through the composite route. Pending: the empty, error and no access states (CG-ALL-1929) and how the pipeline step appears (GAP-3320), owner solution architect |

The screen is read through the gateway-bff composite route (DP-19); the service adds no screen route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-006-01 | AC1 | Component | SIT: legacy extract with listing, sale instruction and appraisal acceptance rows; the six DP06 views seeded; the `rwb-asset` contract fake returning `asset_key` |
| TC-DM-006-03 | AC3 | End to end | SIT: ten clean business dates on the migrated `valuation_ext` rows; legacy tables read only; records served from `rwb_source_data` |
| TC-DM-006-04 | Access | Contract | A role with no Platform administration right is refused with MSG-P4-002 |
| TC-DM-006-05 | AC4 | Component | Synthetic listing and sale with a held status; assertion that no `rwb_asset` row is written |
| TC-DM-006-06 | AC5 | Component | A `valuation_key` with no row in `v_ace_valuation`; the orphan is listed and no Workbench record is deleted or changed |
| TC-DM-006-07 | AC6 | Component | A view returning an error during the check; no reconciliation row, run FAILED with MSG-GEN-006 for "ACE database", rerun writes the rows |
| TC-DM-006-08 | AC7 | Component | The migration run twice; version reported as already applied, row counts per object unchanged |
| TC-DM-006-09 | AC8 | Contract | A user without the right tries the action; refused with MSG-P4-002, nothing changes |
| TC-P1-DM006-APP-01 | AC9 | Component and end to end | Legacy fixture with listing, sale, case link and acceptance; rwb-asset fake with an unavailable and a refusing case |
| TC-P1-DM006-APP-02 | AC10 | Component | A failure injected between the two writes |
| TC-P1-DM006-APP-03 | AC11 | Component | DP06 STALE with Section B absent |
| TC-P1-DM006-APP-04 | AC12; the MSG-P1-023 refusal of AC3 | Component | Collateral fake answering 404 for one key; a sign-off asked at nine clean days |

### 17. Guardrails

- No value a business person may change is written in code; it is read from reference data with its version (BR-P1-001).
- No personal data in logs, tests, prompts or the cutover extract: the extract carries keys and counts, never a name, an identity number or a contact value.
- ACE data only through this service's own `v_ace_*` views or its published contract; a `public.*` read is a defect.
- No foreign key from `rwb_source_data` into ACE, and no copy of an ACE collateral, appraisal, NPA asset or NPA sale row.
- The legacy tables are read only; the migration never writes to the legacy Workbench.
- The migration is rerun safe and leaves no partial load.

### 18. Traceability

| Legacy | This story | Feature | L3 process | Deliverable | Source |
|---|---|---|---|---|---|
| AC1, TC-DM-006-01 | RWB-P1-DM006-APP | FEAT-RDF-01 | Not specified in the source documents (DOR-RWB-P1-DM006-APP-2) | Cutover migration plus the DP06 read path | FSD P1 A2.2 (DP06), A2.1; TSD P1 T3.3, T3.5 |
| AC3, TC-DM-006-03 | RWB-P1-DM006-APP | Not specified in the source documents (DOR-RWB-P1-DM006-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM006-APP-2) | Cutover gate, sign-off and read-only legacy tables | FSD P1 A2.17 retention; TSD P1 T6.1 |
| Access, TC-DM-006-04 | RWB-P1-DM006-APP | Not specified in the source documents (DOR-RWB-P1-DM006-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM006-APP-2) | RBAC on the cutover screen and the rerun | TSD P1 T6.1, T6.2 |
| AC2, TC-DM-006-02 | Not this story | Not specified in the source documents (DOR-RWB-P1-DM006-APP-2) | Not specified in the source documents (DOR-RWB-P1-DM006-APP-2) | REC-05 business-key reconciliation | ASM-3482 |

Requirement IDs: none is allocated to this story in this work package. REQ-RDF-004 (collateral and appraisal read from ACE) is served through `RWB-P1-E1001-APP` and `RWB-P1-E1069-APP`; the DP06 system of record is REQ-RDF-001. Features: FEAT-RDF-01 (read path), FEAT-RDF-12/13 (report and publish hold, read here). Decisions: D-RCV-35, ADR-010, DL25, DL43. DL25 option A is applied (RD-P1-042; assumptions ASM-0728, ASM-0735, ASM-0743, ASM-2602); DL43 planning basis A is applied (RD-P1-043; assumptions ASM-0193, ASM-0737, ASM-0748, ASM-0816).

### 19. Out of scope

- The collateral, appraisal, NPA asset and NPA sale records themselves: ACE holds them, ingested from CCMS, SVAF, AMIS and RPS. No load, no copy, no staging table.
- Creating the views, the schema, the dictionary rows or the data product catalog: `RWB-P1-E1001-APP` and `RWB-P1-E1069-APP`.
- Writing `listing` and `asset_sale`: S5 rwb-asset writes them in `rwb_asset` from the package this story hands over (RD-P1-021).
- REC-01 and REC-02 reconciliation, REC-05 as an owned AC, and the daily reconciliation report.
- The JSON payload of the `rwb-asset` contract: this story uses its fake and does not build it.
- The retention period of the legacy tables: Not specified in the source documents (GAP-2168; ASM-3480).
- The data lake copy and Power BI: no data lake in the target (DP-17).

### 20. Remaining delivery steps

- Size the story (squad, role RW-TRIBE).
- Record the signed epic design of EP08 (product owner).
- Publish and verify the rwb-asset contract fake and record its version (S5 tech lead).
- Agree the package layout and location at the cutover rehearsal (data steward; GAP-3541).
- Fix the legacy retention period (data steward; GAP-2168).
- Provide the synthetic cutover fixtures and Section B fixture in DEV (squad).
- Add the version 3 test rows to Test Cases v9 and the traceability matrix (QA).
