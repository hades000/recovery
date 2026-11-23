# RWB-P1-DM006-APP Migrate collateral and assets
SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd


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
| Patterns applied | DP-05, DP-15, DP-19 |
| Parallel lane | L-P1-A |
| Ready to start | After RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| Depends on (build) | RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

Change log: v1, 22 November 2026, D-RCV-60, T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a data steward, I want the listings, the case asset links and the open sale instructions migrated from the legacy Workbench, so that an asset already offered for sale is not lost at cutover while the collateral, appraisal and NPA asset records are read from ACE.

After the realignment this story carries the part of that sentence that belongs to `rwb-source-data`:

- the appraisal-acceptance decision, held in the extension table `valuation_ext` and keyed by `valuation_key`, because it is a Workbench decision about an ACE appraisal and not a copy of it;
- the DP06 read path — `v_ace_collateral`, `v_ace_collateral_detail`, `v_ace_valuation`, `v_ace_asset`, `v_ace_npa_asset`, `v_ace_npa_sale` — read through the service's own views and its published contract, never a `public.*` table;
- the cutover gate for DP06 in the service's own schema: the migration run, its break list and the evidence the data steward signs off.

The `listing` and `asset_sale` rows are not in the `rwb_source_data` table list. The owning service for those two tables is Not specified in the source documents (GAP-2167; ASM-3479); the default ruling of this story places them with `rwb-asset` (S5), read through that service's contract mock in AC1 (ASM-3479).

### 2. Business rationale

An asset already offered for sale must survive the switch from the legacy Workbench to the 19 services. Under the realignment nothing of the collateral or NPA estate is carried across: ACE holds it, ingested from CCMS, SVAF, AMIS and RPS, and the Workbench reads it (DP-05). What the Workbench does own is the decision about an appraisal — accepted, by whom, when, which panel valuer, stale after its cycle — and that decision belongs in exactly one schema.

Two consequences drive this story:

1. **One number, one source.** DP06 "Collateral and assets" names one system of record for each part: ACE for the collateral, appraisal, NPA asset and NPA sale records, the Workbench for the appraisal acceptance and the sale instruction. Copying an ACE row into `rwb_source_data` would create a second copy that disagrees with ACE and is owned by nobody who maintains the source (D-RCV-35 U1).
2. **Cutover is a data decision, not a deployment step.** The legacy estate is a live estate: a property listed for auction, a sale instruction open with a vendor and an appraisal accepted last month are all in flight at the switch. The cutover therefore keeps a gate — extract, map to business keys, load, check, sign off — and the gate is only passed on evidence.

DP-15 puts the migration on the service's own Flyway sequence, so the change ships with the service and rolls back with it, and DP-19 keeps the data quality screen behind one gateway-bff composite route, so the service exposes no screen of its own.

### 3. Preconditions

| # | Precondition |
|---|---|
| 1 | The `rwb_source_data` schema, its login and the 92-table baseline including the four extension tables are deployed, `valuation_ext` among them (RWB-P1-E1001-APP). |
| 2 | The 16 Section A views and the 14 Section B views are deployed and the conformance test is green; the Section B views over `valuation`, `collateral_detail`, `npa_asset` and `npa_sale` need RWB-ACE-001 (RWB-P1-E1069-APP; DL43). |
| 3 | The per-service Flyway sequence is available at the next free version in `rwb_source_data` (DP-15; RWB-PLT-E1044-CON). |
| 4 | The data quality screen is reachable through the gateway-bff composite route (DP-19; RWB-PLT-N001-CON). |
| 5 | The user holds Platform administration, right R: RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM or RW-SECADM (legacy RWB-DM-006 permission table; TSD P1 T6.1). |
| 6 | The legacy Workbench tables are available read only for the one-off extract, and the ACE batch record shows a COMPLETED row for every DP06 source for the cutover business date (T3.7). |

### 4. Flow

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System (recovery service identity) | Reads the legacy listing, case asset link, sale instruction and appraisal acceptance records at cutover | Rejects a row with no `asset_key` or no `valuation_key`, counts it and lists it |
| 2 | System | Maps each row to the new schema: acceptance to `valuation_ext` by `valuation_key`, every asset link to `asset_key` as `varchar(255)` with no foreign key | Applies BR-P1-001-3 and BR-P1-001-5 |
| 3 | System | Runs the cutover migration at the next free Flyway version in `rwb_source_data` | Commits one batch, writes the row count per object, leaves no partial load |
| 4 | System | Checks the DP06 read path: the six DP06 views answer and `valuation_ext` joins `v_ace_valuation` 1:1 | Writes the break list and the orphan list |
| 5 | System | Publishes the cutover evidence to the reconciliation extract behind SCR-45 Data quality | Shows counts, breaks and the DP06 freshness stamp (LOADED or STALE) |
| 6 | Data steward | Reviews the breaks and signs off (section 10) | Records the sign-off |
| 7 | System | Serves the migrated records from `rwb_source_data` and keeps the legacy tables read only | Cutover complete |

### 5. Exception paths

| # | Condition | Handling |
|---|---|---|
| 1 | A legacy row carries no `asset_key` or no `valuation_key` | The row is refused, counted and listed for the data steward; nothing is written for it (BR-P1-001-3). |
| 2 | A `valuation_key` has no row in `v_ace_valuation` | The REC-05 orphan is listed for the data steward and the ACE team; no Workbench record is deleted or changed (BR-P1-011-3). |
| 3 | Section B is not deployed when the cutover runs | The acceptance rows stay behind their feature flag, DP06 shows STALE with no business date, and the cutover is not signed off (T3.7, DL43). |
| 4 | A view returns an error during the check | No reconciliation row is written for the business date; the run shows FAILED with MSG-GEN-006 for system "ACE database"; the rerun from the job monitor writes the rows. |
| 5 | The migration is run twice | Flyway reports the version as already applied; the row counts per object are unchanged; no batch is written twice. |
| 6 | A user without the right tries the action | Refused with MSG-P4-002; nothing changes. |
| 7 | The legacy tables are held read only past the retention period | The period is Not specified in the source documents (GAP-2168; ASM-3480); the default in ASM-2 applies. |

### 6. INVEST check

| Letter | Check | Verdict |
|---|---|---|
| I | Independent | Yes: one service, one schema, one Flyway version; it builds against CON stories and their fakes. |
| N | Negotiable | Yes: the break thresholds and the evidence format are open until the PRD (C1). |
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

  Scenario: AC3 Cut over (legacy RWB-DM-006 AC3)
    Given ten clean days on the migrated records
    When the data steward signs off
    Then the legacy tables stay read-only for their retention period
    And the migrated records are served from the new schema
```

The legacy AC2 (reconcile the business keys, the REC-05 step) is not owned by this story; it sits with the reconciliation deliverable of the same legacy key, together with TC-DM-006-02 (ASM-3482).

### 8. Business rules

| Rule | Rule text (legacy wording kept, schema named for this service) |
|---|---|
| BR-P1-001-2 | The recovery module reads ACE only through `recovery.v_ace_*` — here `rwb_source_data`'s own `v_ace_*` views. A direct `public.*` read in a story, spec or query is a defect. |
| BR-P1-001-3 | No constraint in this service's schema references a table outside it. A link to a source record is a business-key column of type `varchar(255)` with no foreign key. |
| BR-P1-001-5 | An extension table holds a Workbench decision about an ACE record and never a copy of an ACE column. It is 1:1 with the ACE record and carries the seven standard record columns. |
| BR-P1-011-3 | A REC-05 orphan never deletes or changes a Workbench record; it is listed for the data steward and, where the row is missing in ACE, for the ACE team. |
| BR-P1-014-3 | A product fed by more than one source carries the oldest business date among its sources, and is STALE while any of them is late. DP06 is fed by CCMS, SVAF, AMIS and RPS. |
| DP-15 | The migration runs at the next free Flyway version in `rwb_source_data`. No object is created in another service's schema and no shared baseline is reused. |
| DP-19 | The data quality screen is one gateway-bff composite route. The service publishes no screen route of its own. |

### 9. State transitions

State names for a migration batch are Not specified in the source documents (GAP-2169; ASM-3481). The transitions below use the existing lists LOV-FRESHNESS (LOADED, STALE) and the cutover gate of AC3.

| From | To | Trigger | Evidence |
|---|---|---|---|
| (none) | Extracted | the cutover run reads the legacy records | row count per legacy object |
| Extracted | Loaded | the Flyway version commits in `rwb_source_data` | row count per object; DP06 LOADED |
| Loaded | Reconciled | REC-05 lists no orphan for `asset_key` and `valuation_key` | empty orphan list |
| Reconciled | Signed off | the data steward signs off | sign-off recorded; ten clean days of AC3 |
| Signed off | Cut over | the cutover date arrives | legacy tables read only; records served from `rwb_source_data` |
| Loaded, Reconciled | Held | an orphan, a refused row or a missing Section B view | break list on SCR-45: Data quality |
| LOADED | STALE | a DP06 source batch is late or failed | DP06 freshness stamp (T3.7) |

### 10. Authority

| Decision | Role that holds it | Right |
|---|---|---|
| Run or rerun the cutover migration | Platform administrator (RW-PLATADM) | Platform administration, C and U |
| Read the break list and the cutover evidence | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Platform administration, R |
| Sign off the cutover | Data steward and data product owner (RW-DATASTEW) | Platform administration, R, as the legacy RWB-DM-006 permission table gives it |
| Change the reconciliation tolerance used by AC3 | Decision DL25 | n/a; the tolerance is a parameter, not a code value |

The story starts no approval workflow and holds no authority of its own; every action is checked by the capability area of the screen or the job, and the sign-off is the data steward's right, not a new role.

### 11. Data

| Entity | Fields | Field IDs | Owner after the realignment |
|---|---|---|---|
| valuation_ext | valuation_key, accepted, accepted_at, accepted_by, valuer_partner_id, stale_flag, age_days and the seven standard columns | DF-EXT-036 to DF-EXT-049 | rwb-source-data, schema `rwb_source_data` |
| listing | id, asset_key, sale_channel, start_price, floor_price, round_no, listed_at, status | DF-SAL-001 to DF-SAL-008 | Not specified in the source documents (GAP-2167; ASM-3479); default `rwb-asset` |
| asset_sale | id, asset_key, listing_id, contract_date, sale_date, sale_price and 5 more | DF-SAL-009 to DF-SAL-019 | Not specified in the source documents (GAP-2167; ASM-3479); default `rwb-asset` |
| recovery_case (the case asset link) | id, case_no, product_group, primary_person_key, status, stage_code and 27 more | DF-CAS-001 to DF-CAS-055 | rwb-case, read through its contract |
| ACE reads, never copied | v_ace_collateral 8 fields; v_ace_asset 9; v_ace_valuation 9; v_ace_collateral_detail 12; v_ace_npa_asset 12; v_ace_npa_sale 11 | DF-ACE-091 to DF-ACE-107, DF-ACE-187 to DF-ACE-230 | ACE (ingested from CCMS, SVAF, AMIS and RPS); read only |

### 12. Contract

**12.1 REST operations provided**

None. The legacy story states that it has no endpoint: "the migration is a cutover step run by the recovery service identity, and its breaks are listed on the reconciliation extract." The realignment keeps that, so this story adds no operation to `/api/recovery/source-data/v1`.

**12.2 REST operations consumed**

| Operation | Service | Use in this story |
|---|---|---|
| GET /api/recovery/source-data/v1/data-products/freshness | rwb-source-data (own service) | Reads the DP06 stamp (LOADED or STALE) for the cutover evidence |
| GET /api/recovery/source-data/v1/data-products/DP06/records | rwb-source-data (own service) | Proves the migrated records and the ACE views answer together after the cutover |
| GET /api/recovery/source-data/v1/admin/reconciliation/results | rwb-source-data (own service) | Reads the REC-05 orphan list that gates the sign-off |

No operation of another service is called; the `rwb-asset` payload in AC1 is a contract fake (12.8).

**12.3 Events published**

None. The migration publishes no fact; EV-26 AceDataReady and EV-27 AceDataLate (`rwb.source-data.AceDataReady.v1`, `rwb.source-data.AceDataLate.v1`) belong to the freshness story.

**12.4 Events consumed**

None.

**12.5 Workflows and activities**

None. The service runs no Temporal workflow for this story and the queue `rwb-source-data` carries none; the cutover is a one-off migration run, not a workflow.

**12.6 Schedules**

None. The cutover is a one-off run at the cutover date, not a Temporal Schedule; JOB-01 and JOB-09 are retired and JOB-04 is the daily reconciliation of the case list, delivered elsewhere.

**12.7 Tables owned**

| Schema | Table | Key | Written by this story |
|---|---|---|---|
| rwb_source_data | valuation_ext | valuation_key, `varchar(255)`, no foreign key | Yes: one row per acceptance, with the seven standard columns |

`listing` and `asset_sale` are not in this schema (GAP-2167; ASM-3479).

**12.8 Contract fakes**

| Fake | Used for | Values kept |
|---|---|---|
| `rwb-asset` contract fake | The listing and asset_sale payload of AC1 | `asset_key` on every listing and every sale |

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
| Cutover migration | One new Flyway version on the `rwb_source_data` sequence (DP-15): inserts `valuation_ext` from the legacy extract by `valuation_key`, rerun safe, one transaction per batch |
| RecoveryDataEngineService | Maps the extract, applies BR-P1-001-3 and BR-P1-001-5, counts rows per object, builds the break and orphan lists |
| RecoveryDataEngineRepository | Reads and writes `valuation_ext` only; no other table of the schema is touched |
| AceSourceReadRepository | SELECT only on the six DP06 views for the AC1 proof; names no `public` table |
| SCR-45 Data quality | Gateway-bff composite route (DP-19); shows LOADED or STALE, the counts and the break list |
| Acceptance tests | TC-DM-006-01 (component), TC-DM-006-03 (end to end), TC-DM-006-04 (contract) |

No view, dictionary row or schema object is created: those are the H dependencies (`RWB-P1-E1001-APP`, `RWB-P1-E1069-APP`). The `rwb-asset` side of the payload is not built here.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P1-012 | Warning | The case list for {date} does not reconcile to ACE for {product}: a difference of {variance} accounts, {pct} percent. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

### 15. Screens and states

| Screen | States |
|---|---|
| SCR-45 Data quality | Loading; breaks |

The screen is read through the gateway-bff composite route (DP-19); the service adds no screen route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-006-01 | AC1 | Component | SIT: legacy extract with listing, sale instruction and appraisal acceptance rows; the six DP06 views seeded; the `rwb-asset` contract fake returning `asset_key` |
| TC-DM-006-03 | AC3 | End to end | SIT: ten clean business dates on the migrated `valuation_ext` rows; legacy tables read only; records served from `rwb_source_data` |
| TC-DM-006-04 | Access | Contract | A role with no Platform administration right is refused with MSG-P4-002 |

### 17. Guardrails

- No value a business person may change is written in code; it is read from reference data with its version (BR-P1-001).
- No personal data in logs, tests, prompts or the cutover extract: the extract carries keys and counts, never a name, an identity number or a contact value.
- ACE data only through this service's own `v_ace_*` views or its published contract; a `public.*` read is a defect.
- No foreign key from `rwb_source_data` into ACE, and no copy of an ACE collateral, appraisal, NPA asset or NPA sale row.
- The legacy tables are read only; the migration never writes to the legacy Workbench.
- The migration is rerun safe and leaves no partial load.

### 18. Traceability

| Legacy | This story | Deliverable | Source |
|---|---|---|---|
| AC1, TC-DM-006-01 | RWB-P1-DM006-APP | Cutover migration plus the DP06 read path | FSD P1 A2.2 (DP06), A2.1; TSD P1 T3.3, T3.5 |
| AC3, TC-DM-006-03 | RWB-P1-DM006-APP | Cutover gate, sign-off and read-only legacy tables | FSD P1 A2.17 retention; TSD P1 T6.1 |
| Access, TC-DM-006-04 | RWB-P1-DM006-APP | RBAC on the cutover screen and the rerun | TSD P1 T6.1, T6.2 |
| AC2, TC-DM-006-02 | Not this story | REC-05 business-key reconciliation | ASM-3482 |

Requirement IDs: none is allocated to this story in this work package. REQ-RDF-004 (collateral and appraisal read from ACE) is served through `RWB-P1-E1001-APP` and `RWB-P1-E1069-APP`; the DP06 system of record is REQ-RDF-001. Features: FEAT-RDF-01 (read path), FEAT-RDF-12/13 (report and publish hold, read here). Decisions: D-RCV-35, ADR-010, DL25, DL43.

### 19. Out of scope

- The collateral, appraisal, NPA asset and NPA sale records themselves: ACE holds them, ingested from CCMS, SVAF, AMIS and RPS. No load, no copy, no staging table.
- Creating the views, the schema, the dictionary rows or the data product catalog: `RWB-P1-E1001-APP` and `RWB-P1-E1069-APP`.
- Migrating `listing` and `asset_sale` into this service: they are not in the `rwb_source_data` table list (GAP-2167; ASM-3479); the default is `rwb-asset`.
- REC-01 and REC-02 case-list reconciliation, REC-05 as an owned AC, and the daily reconciliation report.
- The JSON payload of the `rwb-asset` contract: this story uses its fake and does not build it.
- The retention period of the legacy tables: Not specified in the source documents (GAP-2168; ASM-3480).
- The data lake copy and Power BI: no data lake in the target (DP-17).
