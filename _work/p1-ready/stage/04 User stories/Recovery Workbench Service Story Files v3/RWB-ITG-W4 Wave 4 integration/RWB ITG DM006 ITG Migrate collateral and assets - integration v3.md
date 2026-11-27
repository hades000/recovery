# RWB-ITG-DM006-ITG Migrate collateral and assets

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes**

- JOB-04 is a child of `AceIngestCheck` started by the readiness call; the invalid rerun call and the AceDataReady start are removed (RD-P1-012, RD-P1-040; finding #1).
- `asset_key` is outside the REC-05 scope: the real-service listing of the asset orphan is pending (GAP-3308; #2), and break rows have no store (GAP-1508; #3).
- Rights, reads, contract version, `migration_source` and the DP06 and Section B behaviour aligned (RD-P1-005, RD-P1-027, RD-P1-041, RD-P1-043; #4 to #7).
- Finishing pass: test case IDs of Test Cases v9 cited in place of the placeholders.
- A repeated readiness call answers 202 and starts nothing once every due source is stamped and the run has ended (RD-P1-065, register XD-11).
- The `asset_key` orphan check is this story's own cutover check through rwb-source-data; GAP-3308 is closed (RD-P1-068).
- The reconciliation result reads are cited as published in rwb-source-data.yaml 5.1.0 (`getAdminReconciliationResults`, RD-P1-063).

| Item | Value |
|---|---|
| Story key | RWB-ITG-DM006-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-DM-006 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP15, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement |
| Depends on (build) | RWB-P1-DM006-APP |
| Contract dependencies | RWB-P1-E1011-CON (reconciliation result reads), RWB-P1-E1015-CON (readiness and freshness); the CON stories of rwb-asset, rwb-case, rwb-access and the data-product records read: Not specified in the source documents (DOR-RWB-ITG-DM006-ITG-21) |
| Integration dependencies | RWB-P1-DM006-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-001, RD-P1-004, RD-P1-005, RD-P1-011, RD-P1-012, RD-P1-022, RD-P1-027, RD-P1-040, RD-P1-041, RD-P1-042, RD-P1-043, RD-P1-065, RD-P1-068, RD-P1-063 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-DM-006 for the wave 4 cutover reconciliation harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-DM006-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 11 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3; cutover reconciliation harness aligned to the readiness chain, the REC-05 key scope and published reads.

### 1. Story

As a **RW-DATASTEW, data steward**, I want **a repeatable wave 4 cutover reconciliation harness that proves every business key on the migrated listing, sale and appraisal records resolves to its ACE view row and lists every orphan for the data steward and the ACE team, against the owning services' published contracts and their fakes**, so that **an asset already offered for sale is not lost at cutover while the collateral, appraisal and NPA records are read from ACE**.

This is a harness story and nothing else. It builds no production endpoint, table, workflow, schedule or screen, and it changes no business state: the migrated rows are put in place by the cutover loads of the owning services (S5's own Flyway sequence for `listing` and `asset_sale`, P1's for `valuation_ext`), RWB-P1-DM006-APP owns the extract and the reconciliation, and the harness only triggers the reconciliation, reads the owning services' answers and writes its evidence. The extract and the cut-over criteria of the legacy story stay with RWB-P1-DM006-APP, and every collateral, appraisal, NPA asset and NPA sale fact is read from its ACE view through rwb-source-data and never copied.

### 2. Business rationale

An asset that is already offered for sale at cutover is a live instruction with money behind it. If the listing or an accepted appraisal loses its asset link during the migration, the sale instruction is worked against the wrong asset, the floor price and the auction round belong to a record nobody can find, and the loss surfaces only when a buyer or an auditor asks for the asset behind the listing. The two failures that matter are therefore narrow and testable: a business key on a migrated row that resolves to no view row, and a break that exists but is not listed for the person who must clear it.

The migration answer is not to copy the ACE facts. Listing and asset_sale stay with S5 rwb-asset, valuation_ext stays with P1 rwb-source-data, recovery_case stays with P3 rwb-case, and the collateral, asset, valuation and NPA views are read through rwb-source-data (DP-05). The cutover is per-service Flyway from the owning service's own sequence (DP-15), so what the harness asserts is the state three owners reached and not a row a script wrote. Where a screen would show the breaks, the harness calls the gateway-bff composite route (DP-19) so the evidence matches what the data steward sees.

DP06 Collateral and assets is the data product that carries the collateral, asset, collateral-detail, valuation and NPA views with the listing, asset_sale and valuation_ext tables, and DP01 and DP02 carry the account and person keys the case links. The measure is the worst case allowed by DL25: a difference of one is a break, REQ-RDF-007 requires every key on a migrated record to reconcile, and REQ-RDF-008 requires every failed row to carry its reason, so zero unlisted and zero unresolved is the only passing answer.

### 3. Preconditions

- The S5 asset contract is published, and a WireMock stub set is generated from it: `GET /api/recovery/asset/v1/assets/{assetKey}` returns the asset with its listings and sale instructions.
- rwb-source-data.yaml 5.1.0 is published, and its fakes (`fakes/rwb-source-data/5.1.0/`) answer the readiness call and status, `GET /data-products/DP01/records`, `GET /data-products/DP02/records`, `GET /data-products/DP06/records`, `GET /data-products/freshness` and the reconciliation result reads (published, RD-P1-063).
- The data product catalog holds DP01, DP02 and DP06 as versioned rows with their systems of record and their refresh expectations, DP06 being WEEKLY with MON 08:00.
- For the real-service run the Section B views are deployed and their flag is on: while it is off, `AceIngestCheck` writes no stamp and starts no reconciliation, the readiness status reads LATE and freshness reads STALE with no business date (RD-P1-043). The harness caller of the readiness call holds Platform administration U, of the records and freshness reads Case record R, and of the result reads Platform administration R.
- RWB-P1-DM006-APP is the integration dependency: until it lands, its stub returns the migrated records. S5's cutover load for `listing` and `asset_sale` and P1's cutover load for `valuation_ext`, each from its own Flyway sequence (DP-15), provide the same records in SIT, so the harness seeds nothing by hand in either case.
- The rwb-case and rwb-access contracts are published, with a stub for the case read and one for the authorise call, the latter able to allow and to refuse.
- The SCR-45 Data quality composite route exists on gateway-bff for the break list; its path and its merge order are Not specified in the source documents (GAP-0446; ASM-0638).
- The synthetic cutover extract fixture, the reconciliation extract format and retention, the harness environment and base hosts, the break-list fields and the pass or fail gate are Not specified in the source documents (GAP-0446; ASM-0638).
- No build dependency. Day 1, with the fakes in place from the first run, and each fake replaced by the real owner as its integration story lands.

### 4. Flow

1. Harness: takes the migrated records as they are, from the §12.8 stub on Day 1 and from the cutover loads of S5 and P1 in SIT, and seeds nothing by hand (the listing, the sale and the case asset link reach S5 as one handover package per cutover business date, with the case asset link carried as the case key beside the asset_key and no table of its own, and the source tag and cutover business date riding on the handover row and in the Flyway history description): case "RW-2026-000606", listing "LIST-0606" on asset_key "AST-SYN-0606" with sale_channel "AUCTION", round_no 1 and status "LISTED", valuation_key "VAL-SYN-0606" accepted, account_key "ACC-SYN-000606", person_key "PERS-SYN-000606", and the orphan asset_key "AST-SYN-0777".
2. Harness: starts the chain for business date "2026-12-31" with `POST /api/recovery/source-data/v1/business-days/{date}/ready` and a UUID `Idempotency-Key` (202), and waits until `AceIngestCheck` has stamped the ALS batch and its child `ReconciliationWorkflow` (`recon-2026-12-31`, JOB-04) has written the results. The harness never reruns JOB-04: the rerun operation takes the run uuid of a FAILED run only.
3. Harness: reads the asset and its listings and sale instructions through `GET /api/recovery/asset/v1/assets/{assetKey}` for "AST-SYN-0606", and for "AST-SYN-0777" to prove the orphan asset is absent from S5 while the listing that names it is still readable at "LISTED". The listing and sale instructions are owned by rwb-asset (S5), and the asset_key links are validated against the rwb-asset contract fake.
4. Harness: reads the case through `GET /api/recovery/case/v1/cases/{caseId}`, its status, stage and the account and person keys the case links.
5. Harness: resolves the asset and valuation keys through `GET /api/recovery/source-data/v1/data-products/DP06/records?caseId={caseId}` and the account and person keys through the DP01 and DP02 records, then reads `GET /api/recovery/source-data/v1/data-products/freshness?product=DP06` and asserts `status` LOADED (DP06 is weekly, so the stamp in use is that of its last cycle day) before it counts a key as resolved (DP-05). The asset_key is proved from Day 1 against v_ace_asset and v_ace_collateral. Until the Section B views answer, the valuation_key is proved against the contract fake, and the cutover stays behind its feature switch so that no day is counted on a STALE DP06 stamp.
6. Harness: reads the breaks from the reconciliation extract of the run and from the SCR-45 Data quality composite route on gateway-bff, and asserts the two answers name the same rows, each with its key type and key value, and not one more on either side (DP-19).
7. Harness: asserts exactly one break row for listing "LIST-0606" with key type "ASSET", key value "AST-SYN-0777", reason "NO_ACE_ROW" and owner role "RW-DATASTEW", and asserts no sale is recorded for "AST-SYN-0777" through the rwb-asset contract. The daily REC-05 of rwb-source-data does not check `asset_key`: on the real services this row is this story's own cutover check, counted in its evidence, reading the keys through rwb-source-data (`GET /collateral/{assetKey}`) (RD-P1-068 rule 5).
8. Harness: repeats the readiness call for the same business date with a new UUID `Idempotency-Key`, then compares the break list and the counts of listings, sale instructions and valuation acceptances with the first run, and asserts one break row and one report entry for the business date and not one per run. The migrated batch is described by the existing LOADED and STALE freshness values and the AC3 gate, with no new list of values, and its evidence is the reconciliation extract rows. The repeated call answers 202 with the stored state and starts nothing; a second run of the date exists only through the rerun of a FAILED run (RD-P1-065 rule 3, register XD-11).
9. Harness: sends the readiness call as a synthetic user with role "RW-OFF" and no Platform administration right, asserts 403 with `messageCode` "MSG-P4-002", asserts no run started and no break row was written, then writes the report keyed by story and business date with the contract and fixture versions named. The harness pack (SIT environment and base hosts, the cutover fixture layout, the composite route path and break-list fields, the reconciliation extract format, delivery and retention, the gate and the seeding set) is Not specified in the source documents (GAP-0446); it is agreed at the wave 4 entry check, recorded in the harness README and pinned in the run report.
10. Harness: counts the ten clean days from the reconciliation_result rows of JOB-04 on the migrated records. A PASS day with no unexplained variance and no new REC-05 orphan on a LOADED DP06 stamp counts; a BREAK row, a new orphan or a STALE DP06 day resets the count to zero, and a day whose DP06 stamp is STALE is never counted as clean. The ten day rows, the DP06 stamps and the data steward sign-off are held in the cutover record of the release pipeline, with no counter table and no sign-off table.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop before any assertion; the report names the service, the operation and the contract version | None | AC1 |
| X2 | The cutover fixture lacks a required key, for example the listing without its asset_key | The run fails and the report names the fixture and the row; the run is not marked passed | None | AC1, AC2 |
| X3 | A missing view row is not listed for the data steward and the ACE team | The run fails on AC1 and AC2 and the report names the key and the view it did not resolve to | None | AC2 |
| X4 | The break row is duplicated on the repeated run for the same business date | The run fails on AC3 and the report names both rows and the two run identifiers | None | AC3 |
| X5 | The ACE batch of the business date is late, or the Section B flag is off, or DP06 reads STALE | No reconciliation starts without the ALS stamp and the readiness status reads LATE; a STALE DP06 day counts no key as unresolved and no clean day; the report names the product and its date | MSG-P1-001 | AC1, AC3 |
| X6 | The SCR-45 answer and the reconciliation extract disagree | The run fails on AC2 and the report names the row present on one side only and the composite route | MSG-P1-012 | AC2 |
| X7 | A caller without the Platform administration right has a run started anyway | The run fails on AC4 regardless of the break list; the report names the caller role, the operation and the job identifier | MSG-P4-002 | AC4 |

The report text is for the wave entry check and is not part of the message standard. The business messages above are asserted as the owner returns them, so a run failure points at a service and a message and not only at a date.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and their fakes from Day 1; the waits are RWB-P1-DM006-APP and, for the real-service run, the Section B views |
| Negotiable | The fixture layout, the break-list fields, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | Proves before the wave opens that no migrated listing or appraisal loses its asset link and that every orphan is listed once |
| Estimable | One runner, one stub set, two file fixtures, one key resolver, one break-list assertion, one report |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion runs against the fakes and again against RWB-P1-DM006-APP when it lands, and a stub pass is reported as a stub pass |

### 7. Acceptance criteria

```gherkin
Feature: Migrate collateral and assets - wave 4 cutover reconciliation harness

  Background:
    Given listing "LIST-0606" on asset_key "AST-SYN-0606" of case "RW-2026-000606" with sale_channel "AUCTION", round_no 1 and status "LISTED"
    Given valuation_key "VAL-SYN-0606" is accepted on the case
    Given the ACE asset and valuation views hold rows for "AST-SYN-0606" and "VAL-SYN-0606"
    Given the case links account_key "ACC-SYN-000606" and person_key "PERS-SYN-000606"
    Given ReconciliationWorkflow "recon-2026-12-31" (JOB-04) has completed for business date "2026-12-31" as the child of AceIngestCheck

  Scenario: AC1 Reconcile the business keys (legacy RWB-DM-006 AC2)
    Given the migrated records
    When the REC-05 step runs
    Then every business key on a migrated record resolves to its view row, account_key and person_key included
    And each orphan is listed for the data steward and the ACE team

  Scenario: AC2 An orphan asset key is listed and the listing is not sold (new, D-RCV-60)
    Given migrated listing "LIST-0606" carries asset_key "AST-SYN-0777"
    And the ACE asset view holds no row for asset_key "AST-SYN-0777"
    When the harness reads the reconciliation extract fixture for business date "2026-12-31"
    Then the break list holds one row for listing "LIST-0606" with key type "ASSET" and key value "AST-SYN-0777"
    And the row names the reason "NO_ACE_ROW" and the owner role "RW-DATASTEW"
    And the listing stays readable at status "LISTED" through the rwb-asset contract
    And no sale is recorded for the orphan asset
    And on the real services the asset_key orphan is listed by this story's own cutover check, read through rwb-source-data (RD-P1-068)

  Scenario: AC3 A repeated run is deterministic and one break is listed once (new, D-RCV-60)
    Given the reconciliation for business date "2026-12-31" has run once
    When POST /business-days/2026-12-31/ready is called again with a new UUID Idempotency-Key and answers 202
    Then the repeated call starts nothing: no second ReconciliationWorkflow run for "2026-12-31", because every due source of the date is stamped and the run has ended
    And no second set of reconciliation result rows exists for 2026-12-31
    And the break list holds exactly one row for asset_key "AST-SYN-0777"
    And the counts of listings, sale instructions and valuation acceptances equal the first run
    And the run report holds one entry per business date and not one per run

  Scenario: AC4 A caller without the platform administration right is refused (new, D-RCV-60)
    Given a synthetic user with role "RW-OFF" and no Platform administration right
    When that user calls POST /business-days/2026-12-31/ready with a UUID Idempotency-Key
    Then the answer is 403 with a problem body whose messageCode is "MSG-P4-002"
    And no reconciliation run starts and no break row is written

  Scenario: AC5 Each business rule BR1 to BR7 is covered by a criterion or a guardrail test (new, D-RCV-60)
    Given the business rules BR1 to BR7 in section 8
    When the story is verified against its test cases in section 16
    Then each rule BR1 to BR7 is covered by a criterion in section 7 or by a guardrail test in section 16
    And a rule with no covering criterion or test is a gap and not a pass

  Scenario: AC6 A consumed call that fails or does not answer is not a pass (new, D-RCV-60)
    Given the consumed call `GET /api/recovery/source-data/v1/data-products/DP06/records?caseId={caseId}` for case "RW-2026-000606" fails or does not answer within its 2 s budget
    When the harness reads the reconciliation result for business date "2026-12-31"
    Then the run is recorded as a failure and not as a pass
    And no asset or valuation key of case "RW-2026-000606" is counted as resolved

  Scenario: AC7 Migrated records are read through their owners and are not copied or changed (BR4, BR5, BR6, BR7) (new, D-RCV-60)
    Given the migrated listing, asset_sale and valuation_ext records
    When the harness reads the case, asset and source-data records through the rwb-case, rwb-asset and rwb-source-data contracts
    Then ACE collateral, asset, valuation and NPA data is read only through the views owned by rwb-source-data and never from a schema
    And no collateral, appraisal or NPA record is copied into a Workbench table
    And each migrated record keeps its migration_source and migrated_at, and the harness writes neither
```

Legacy AC1 and AC3 belong to RWB-P1-DM006-APP, and the seven criteria above are the ones this ITG story owns.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every business key on a migrated record resolves to its view row, account_key and person_key included, or it is a break | REQ-RDF-007; DL25 |
| BR2 | Every break is listed for the data steward and the ACE team with its key type, its key value, its reason and its owner role | REQ-RDF-008 |
| BR3 | Zero tolerance: a difference of one holds the wave, and a run that lists no break for a missing view row is a failure and not a pass | DL25 |
| BR4 | ACE collateral, asset, valuation and NPA data is read only through the views owned by rwb-source-data and never from a schema | D-RCV-35; ADR-010 |
| BR5 | No collateral, appraisal or NPA record is copied into a Workbench table; each is read from its view | legacy RWB-DM-006 AC1 |
| BR6 | A migrated record keeps `migration_source` and `migrated_at`, and the harness asserts both and writes neither | legacy RWB-DM-006 guardrails; RD-P1-027 |
| BR7 | Each service migrates and loads its own schema through its own Flyway sequence, so the harness reads three owners and not one schema | DP-15 |

### 9. State transitions

The harness changes no state. Listing "LIST-0606" stays "LISTED" and valuation_key "VAL-SYN-0606" stays accepted from the first read to the last assertion of the run, an orphan asset stays readable through the rwb-asset contract and is listed as a break, and a listed orphan that resolves on a later run is no longer listed while the earlier run's evidence keeps the row it wrote. No sale is recorded for an orphan asset, and no break row is deleted or edited by the harness: a break that clears is cleared by the reconciliation of the owning service on its next run. Every one of those moves belongs to S5 rwb-asset, which owns the asset, the listing, the auction round and the sale instruction, and S5 owns every state change the harness asserts; the harness reads the state the owners reached and writes no row in any schema (DP-01).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward | Reads the break list, the reason and the owner role for every orphan, and owns the disposition of each break |
| RW-COE, Centre of Excellence | Reads the same run evidence and the counts behind it |
| RW-AUDIT, audit | Reads the run report and the break list as retained evidence for the cutover |
| RW-COMPLY, compliance | Reads the same evidence for the collateral, appraisal and NPA data lineage |
| RW-PLATADM, platform administration | Holds the Platform administration right; with U it starts the chain, and it may rerun a FAILED run only |
| RW-SECADM, security administration | Holds the same right for the environment under test |
| QA lead | Owns the harness configuration, the fixtures, the break-list fields, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to RWB-P1-DM006-APP |
| S5 and P1 identities | rwb-asset owns every state the harness asserts and rwb-source-data runs the reconciliation and publishes the freshness; neither is configured or changed here |
| No delegation of authority level applies | The harness takes no business decision: a break is cleared by the data steward in the owner's process, not in the harness |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023, DF-CAS-046 to DF-CAS-055 | recovery_case | id, case_no, product_group, primary_person_key, status, stage_code and 27 more | Read, through the rwb-case contract |
| DF-CAS-024 to DF-CAS-029 | case_account | id, case_id, account_key, is_primary, linked_from, linked_to | Read, through the rwb-case contract |
| DF-CAS-030 to DF-CAS-035 | case_party | id, case_id, person_key, party_role, role_from, role_to | Read, through the rwb-case contract |
| DF-CAS-036 to DF-CAS-045 | deviation | id, case_id, deviation_code, raised_at, raised_by, paused_state, handler_user_id, contact_stop, cleared_at, outcome | Not read: section 12.2 consumes no rwb-deviation operation |
| DF-SAL-001 to DF-SAL-008 | listing | id, asset_key, sale_channel, start_price, floor_price, round_no, listed_at, status | Read, through the rwb-asset contract |
| DF-SAL-009 to DF-SAL-019 | asset_sale | id, asset_key, listing_id, contract_date, sale_date, sale_price and 5 more | Read, through the rwb-asset contract |
| DF-EXT-036 to DF-EXT-049 | valuation_ext | valuation_key, accepted, accepted_at, accepted_by, valuer_partner_id, stale_flag and 8 more | Read, through the rwb-source-data contract |
| Standard column | listing, asset_sale, valuation_ext | migration_source (RD-P1-027; list LOV-MIGRATION-SOURCE values pending, GAP-3275) | Read, through the owning contract |
| Standard column | listing, asset_sale, valuation_ext | migrated_at | Read, through the owning contract |

DP06 Collateral and assets carries the collateral, asset, collateral-detail, valuation and NPA views together with the listing, asset_sale and valuation_ext tables, and its refresh is WEEKLY with MON 08:00; DP01 Account and arrears and DP02 Customer and party carry the account_key and person_key that the case links and that the harness resolves through the same contract (DP-05). The harness owns no table and writes no row directly: it reads and writes through the API of the owning service only, and the data seeding set, the cutover fixture layout and the evidence retention are Not specified in the source documents (GAP-0446; ASM-0638). The reference data is read under the reference-data contract named by DP-06 and DP-07, and the parameters it reads are Not specified in the source documents (DOR-RWB-ITG-DM006-ITG-20).

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/source-data/v1/business-days/{date}/ready` | P1 rwb-source-data | Starts the chain that runs JOB-04 for the date, UUID `Idempotency-Key`, 202; Platform administration U (AC1, AC3, AC4) |
| GET | `/api/recovery/source-data/v1/business-days/{date}/status` | P1 rwb-source-data | RUNNING, DONE or LATE for the date |
| GET | `/api/recovery/source-data/v1/admin/reconciliation/results` | P1 rwb-source-data (RWB-P1-E1011-CON) | REC-01 and REC-02 rows of the date; Platform administration R |
| GET | `/api/recovery/source-data/v1/data-products/DP06/records?caseId={caseId}` | P1 rwb-source-data | Resolve the asset and valuation keys of the case to their view rows (AC1, AC2) |
| GET | `/api/recovery/source-data/v1/data-products/DP01/records?caseId={caseId}` | P1 rwb-source-data | Resolve the account_key of the case to its view row (AC1) |
| GET | `/api/recovery/source-data/v1/data-products/DP02/records?caseId={caseId}` | P1 rwb-source-data | Resolve the person_key of the case to its view row (AC1) |
| GET | `/api/recovery/source-data/v1/data-products/freshness?product=DP06` | P1 rwb-source-data | `status` LOADED or STALE and `businessDate` of DP06 before a key is counted as resolved (AC1, AC3) |
| GET | `/api/recovery/asset/v1/assets/{assetKey}` | S5 rwb-asset | Read the asset, its listing, its round and its sale instruction, including the orphan asset and the LISTED listing (AC1, AC2, AC3) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | Read the case, its status and the account and person keys it links (AC1, AC3) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Authorise each call and prove the refusal path for a caller without the Platform administration right (AC4) |

Every operation is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget and a circuit breaker per downstream (DP-11, DP-13). Where a screen would compose them, the harness calls the gateway-bff composite route (DP-19). No operation is invented in this story. Contract version fixed: rwb-source-data.yaml 5.1.0 (API Specification v7); v1, the /v1 major version, for the other consumed paths. Refusals are `application/problem+json` read by `messageCode` (RD-P1-004).

The SCR-45 Data quality break list is read through the gateway-bff composite route and not composed by the harness: the route path and the merge order of the rwb-source-data breaks with the rwb-asset listing state are Not specified in the source documents (GAP-0446; ASM-0638).

#### 12.3 Events published

None. The harness publishes no Kafka event; it reads the owners' answers and writes its report to the wave record.

#### 12.4 Events consumed

None. The harness subscribes to no topic: it starts the chain through the readiness call, and `AceIngestCheck` starts JOB-04 as its child (RD-P1-040).

#### 12.5 Workflows and activities

None added. The harness exercises the existing JOB-04 `ReconciliationWorkflow`, a child of `AceIngestCheck` in rwb-source-data, and asserts its effect through the reconciliation extract, the data product records and the break list. No workflow, activity or Schedule is created, changed or owned by this story.

#### 12.6 Schedules

None. JOB-04 runs as a child of `AceIngestCheck` and is started for the business date under test through the readiness call; no cron, overlap policy or catch-up window is set by this story.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); listing and asset_sale are S5's, valuation_ext is P1's, recovery_case is P3's, and the reconciliation result is P1's.

#### 12.8 Contract fakes

| Fake | Contract | Use in the run |
|---|---|---|
| `fakes/rwb-source-data/5.1.0/` (WireMock) | The readiness call and status, the DP01, DP02 and DP06 records, the freshness read and the result reads | Day-1 run of AC1 to AC4 before RWB-P1-DM006-APP and the S5 and P1 cutover loads are live |
| WireMock stub for rwb-asset | `GET /assets/{assetKey}` | Day-1 assertions on the asset, the listing at LISTED, the absence of the orphan asset and the absence of a sale |
| WireMock stub for rwb-case | `GET /cases/{caseId}` | Day-1 assertion on the case and the account and person keys it links |
| WireMock stub for rwb-access | `POST /authorise` | Day-1 authorisation and the refusal path for RW-OFF |
| Cutover extract fixture | The migrated listing, asset_sale and valuation_ext rows of RWB-P1-DM006-APP and of the S5 cutover load | The migrated records the harness reconciles, keyed by asset_key, valuation_key and business date |
| Reconciliation extract fixture | Harness data until the break-detail contract exists (GAP-1508) | The breaks the harness compares with the SCR-45 answer |
| SCR-45 composite route stub | The gateway-bff composite route for the Data quality break list | The second answer the harness compares with the extract, and the screen-shaped evidence |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The harness environment and base hosts, the cutover fixture layout, the reconciliation extract format and retention, the break-list fields, the composite route path and merge order, the pass or fail gate and the data seeding set are Not specified in the source documents (GAP-0446; ASM-0638).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 10 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13), composed through gateway-bff where a screen would (DP-19) |
| Kafka | None published and none consumed; the reconciliation is started through the readiness call |
| Temporal | None added; `AceIngestCheck` and its child `ReconciliationWorkflow` exercised |
| File | The cutover extract fixture and the reconciliation extract fixture, both read-only in the run |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies in the table above (RWB-PLT-E1044-CON and RWB-PLT-N001-CON) are delivered by the platform waves and are not repeated in the metadata H field of this story, which stays empty. The one blocking dependency is the integration dependency RWB-P1-DM006-APP: until it is live the run uses its stub, and on SIT the migrated records come from the cutover loads of S5 and P1, so a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the four owned criteria in order for a business date and holds the run lock, with one UUID Idempotency-Key per readiness call |
| StubSet | Fake | The six stubs generated from the published contracts, with each contract version pinned |
| CutoverExtractFixture | Fixture | The migrated listing, asset_sale and valuation_ext rows, keyed by asset_key, valuation_key and business date |
| AssetKeyResolver | Service | Resolves each business key of a migrated record to its view row through DP06, DP01 and DP02 after the freshness check |
| BreakListAssertion | Service | Compares the reconciliation extract with the SCR-45 composite route answer and asserts one row per break with its reason and owner role |
| EvidenceReport | Service | Writes the per-business-date report keyed by story and date, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real owners as RWB-P1-DM006-APP lands, on the synthetic set of the legacy criteria: case "RW-2026-000606", listing "LIST-0606" on asset_key "AST-SYN-0606" with sale_channel "AUCTION", round_no 1 and status "LISTED", valuation_key "VAL-SYN-0606" accepted, account_key "ACC-SYN-000606", person_key "PERS-SYN-000606", the orphan asset_key "AST-SYN-0777" and business date "2026-12-31". The harness seeds nothing by hand: on Day 1 the stub returns the migrated records, and in SIT the cutover loads of S5 for `listing` and `asset_sale` and of P1 for `valuation_ext` (DP-15) provide them. The environment and base hosts, the fixture layout, the extract format and retention, the break-list fields, the gate and the seeding set are Not specified in the source documents (GAP-0446; ASM-0638).

**Build steps**

1. Generate the six stubs from the published contracts (rwb-source-data at 5.1.0) and pin each contract version in the run report; fail the run on a version mismatch (X1).
2. Build the cutover extract fixture and the reconciliation extract fixture, and prove one read of the LISTED listing and one read of the DP06 records against the stub (X2).
3. Build the JourneyRunner for AC1: send the readiness call with a UUID Idempotency-Key, wait for `recon-{businessDate}`, read the freshness, resolve the asset, valuation, account and person keys, and assert every key resolves and every orphan is listed for the data steward and the ACE team.
4. Add AC2: the orphan asset_key "AST-SYN-0777", one break row with key type "ASSET", reason "NO_ACE_ROW" and owner role "RW-DATASTEW", the listing still readable at "LISTED", no sale, and the extract and the SCR-45 answer agreeing (X3, X6).
5. Add AC3: repeat the readiness call for the same business date with a new Idempotency-Key, and assert one break row, the same counts of listings, sale instructions and valuation acceptances, and one report entry for the business date (X4).
6. Add AC4: the synthetic role "RW-OFF" with no Platform administration right, assert 403 with "MSG-P4-002", no run started and no break row written (X7).
7. Add the EvidenceReport and the gate, then rerun the four criteria against RWB-P1-DM006-APP when it lands and against the S5 and P1 cutover loads in SIT (X5).

**Feature switch.** None. The harness carries no feature switch of its own; it reads the environment it is pointed at and writes its report.

**Done when.** The tests of section 16 pass for the four owned criteria; the four criteria pass against the stubs on Day 1 and again against RWB-P1-DM006-APP when it lands; and the wave entry check holds one run report per business date with the contract and fixture versions named and each hop marked as a stub or the real owner.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | The ACE batch or the DP06 stamp of the date is late (X5) | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-012 | The reconciliation does not agree with ACE for the product | The case list for {date} does not reconcile to ALS for {product}: a difference of {variance} accounts, {pct} percent. |
| MSG-GEN-001 | A required field of the synthetic set or of a call is missing | Enter {field}. |
| MSG-P4-002 | A caller without the Platform administration right tries to start the chain | You cannot {action} here. Your role does not include it. |

The harness produces none of these messages itself; it asserts the message the owning service returns and names the message ID in the report, so a run failure points at a service and a message and not only at a business date.

### 15. Screens and states

Legacy SCR-45 Data quality is the screen the data steward opens for the break list, and it is built by RWB-AD-019.

| State | What the harness asserts through the composite route |
|---|---|
| Loading | The route answers with a defined loading state while JOB-04 is running, and a break is never asserted from a partly merged answer |
| Breaks | One row for listing "LIST-0606" with key type "ASSET", key value "AST-SYN-0777", reason "NO_ACE_ROW" and owner role "RW-DATASTEW", matching the reconciliation extract row for row, on the stubs; on the real services this story's own cutover check counts the orphan in its evidence (RD-P1-068); the stored break list stays pending (GAP-1508) |
| Loading | Not specified in the source documents (CG-ALL-1010) |
| Empty | Not specified in the source documents (CG-ALL-1010) |
| Error | Not specified in the source documents (CG-ALL-1010) |
| No access | Not specified in the source documents (CG-ALL-1010) |

The harness renders no screen. It reads the two populated states through the SCR-45 composite route and the reconciliation extract, and it asserts the same rows a data steward would see, so a passed run means the screen has the right data behind it. Screen behaviour, including the empty, loading, error and no access states of SCR-45, stays with the owning APP stories, and the console itself is RWB-AD-019; the evidence report the wave entry check looks at instead has a format and retention that are Not specified in the source documents (GAP-0446; ASM-0638).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-006-01-ITG | AC1 (legacy); ITG AC1; BR1 | Integration | Synthetic listing LIST-0606 with DP01, DP02 and DP06 rows present |
| TC-DM-006-02-ITG | AC2 (legacy); ITG AC1, ITG AC2; BR1, BR2, BR3 | Integration | One asset_key AST-SYN-0777 with no view row |
| TC-DM-006-03-ITG | AC3 (legacy, owned by RWB-P1-DM006-APP); ITG AC3 | Integration | The readiness call for business date 2026-12-31 sent twice |
| TC-DM-006-04-ITG | Access; ITG AC4 | Component | RW-OFF caller without Platform administration R |
| TC-DM-006-05-ITG | ITG AC5; BR1, BR2, BR3, BR4, BR5, BR6, BR7 | Guardrail | Rules BR1 to BR7 of section 8 against the criteria of section 7 and the test cases of section 16 |
| TC-DM-006-06-ITG | ITG AC6; BR3 | Integration | Consumed DP06 records call for case RW-2026-000606 that fails or does not answer within 2 s |
| TC-DM-006-07-ITG | ITG AC7; BR4, BR5, BR6, BR7 | Integration | Synthetic listing LIST-0606 and valuation VAL-SYN-0606, read through the rwb-case, rwb-asset and rwb-source-data contracts |
| TC-DM-006-08-ITG, TC-DM-006-03-ITG, TC-DM-006-04-ITG, TC-DM-006-07-ITG | Changed assertions of ITG AC2, AC3, AC4, AC7 | Integration | Values of section 7 |

The integration cases above are the ITG copies of the legacy cases of the same number and carry the synthetic data unchanged; the component copy keeps the legacy level. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: floor price, sale channel, tolerances, the fixture contents, the reason codes and the break-list fields are data.
- No personal data in logs, fixtures, reports, tests or prompts: the synthetic set carries keys and codes only, and no customer name, address or contact point is used.
- No cross-schema read: every read and every trigger goes through the owning contract (DP-01), and ACE data only through the views that rwb-source-data owns (DP-05, ADR-010).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11).
- A stub pass is never reported as a real-service pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never sets a listing, a valuation, a break or a sale state by hand.
- A failing criterion is fixed in the service that owns it or reported as a gap; it is never waived in the script, and zero tolerance is not relaxed for a run.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-DM-006 Migrate collateral and assets | Recovery Workbench Data Migration Stories v4, section RWB-DM-006 | Split: AC1 and AC3 to RWB-P1-DM006-APP, AC2 to this story, with sections 1, 7, 11 and 16 realigned |
| Legacy AC2 Reconcile the business keys | Recovery Workbench Data Migration Stories v3, RWB-DM-006 AC2, copied word for word | Section 7, AC1, and TC-DM-006-02-ITG |
| Legacy TC-DM-006-01 Extract the Workbench records | Recovery Workbench Data Migration Stories v4, RWB-DM-006 test cases | TC-DM-006-01-ITG, run against the migrated records the owner supplies |
| Legacy TC-DM-006-02 Reconcile the business keys | Recovery Workbench Data Migration Stories v4, RWB-DM-006 test cases | TC-DM-006-02-ITG, and section 7 AC1 and AC2 |
| Legacy TC-DM-006-03 Cut over | Recovery Workbench Data Migration Stories v4, RWB-DM-006 test cases | TC-DM-006-03-ITG, as the deterministic repeated run of AC3 within the harness and not the cut-over sign-off |
| Legacy TC-DM-006-04 A role without the right is refused with MSG-P4-002 | Recovery Workbench Data Migration Stories v4, RWB-DM-006 test cases | TC-DM-006-04-ITG, and section 7 AC4 |
| DF-CAS-001 to DF-CAS-055, DF-SAL-001 to DF-SAL-019, DF-EXT-036 to DF-EXT-049 | Recovery Workbench Data Migration Stories v4, RWB-DM-006 data table | Section 11, read through the owning contracts |
| DL25 zero tolerance | Decision Log, cited by RWB-DM-006 | Section 8, BR1 and BR3, and section 7 AC3 |
| DL25 Reconciliation tolerance, recommended option A: zero; any difference holds the publish | Decision Log, DL25; ASM-0728, ASM-0735, ASM-0743, ASM-2602 | Applied in this story under the programme directive: section 8, BR3 |
| D-RCV-35 and ADR-010, ACE data only through the owner's views | Decision Log; Architecture Decision Records; Architecture v5 slide 11 | Section 8, BR4, and section 17 |
| RWB-E1-011 Reconciliation and data quality report | Recovery Workbench User Stories Epic 1 v7, and RWB-AD-019 | The JOB-04 reconciliation the harness starts through the readiness call and the SCR-45 break list it reads |
| DP-05, DP-15, DP-19 | Template and Rules v1, section R5.5 | Section 13, and the metadata patterns applied |

### 19. Out of scope

- RWB-P1-DM006-APP: the extract, the reconciliation and legacy AC1 and AC3. The cutover loads of `listing`, `asset_sale` and `valuation_ext` are S5's and P1's own Flyway sequences.
- S5 production code and its CON, APP and DB stories, including the asset, listing and auction-round behaviour the harness only reads.
- The SCR-45 console and its screen behaviour, which are RWB-AD-019.
- The cutover plan, the run book and the sign-off, which sit with the release, not with this story.
- ACE ingestion and the `v_ace_*` views, which are RWB-ACE-001.
- The auction and sale workflows themselves, and every collateral, appraisal or NPA record write.
- Platform configuration, the harness environment build and the evidence retention decision, which are carried as a gap and an assumption, not decided here.
- The other data migration keys of the migration set, each with its own story.

### Remaining delivery steps

- Size the story at refinement (squad).
- Epic design sign-off for EP08 (solution architect).
- Build the story's own `asset_key` orphan cutover check and its evidence count, reading `GET /collateral/{assetKey}` (RD-P1-068 rule 5).
- Add the reconciliation result reads to rwb-source-data.yaml 5.1.0 and publish the fakes (rwb-source-data contract owner).
- Publish the break-detail store and detail response (P1 data architect, GAP-1508).
- Deploy the Section B views before the real-service run (ACE team lead, DL43).
- Fix the SIT environment, fixtures and break-list fields at the wave 4 entry check (QA lead, GAP-0446).
- Add the changed test case rows in Test Cases v9 and the Requirements Traceability Matrix (test writer).
