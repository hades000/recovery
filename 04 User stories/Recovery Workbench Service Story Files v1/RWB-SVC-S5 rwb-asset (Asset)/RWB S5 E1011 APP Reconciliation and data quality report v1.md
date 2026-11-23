# RWB-S5-E1011-APP Reconciliation and data quality report

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E1011-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-011 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP05, DP06, DP07, DP10, DP11, DP14, DP15, DP17, DP19 |
| Parallel lane | L-S5-A |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to REQ-RDF-007, REQ-RDF-008, REQ-CWC-004) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: RWB-E1-011 is split and reworked as the rwb-asset APP story RWB-S5-E1011-APP, the asset slice of the daily reconciliation: the assets this service holds on the books and every asset key on its own tables are reconciled against the collateral and assets data product read through the rwb-source-data contract; the enterprise case-list reconciliation stays with rwb-source-data; the two data-lake extracts are removed. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **data steward and data product owner (RW-DATASTEW)**, I want **a daily quality run in rwb-asset that reconciles the assets this service holds on the books against the collateral and assets data product it reads through the rwb-source-data contract, resolves every asset key on its own tables to a data product row, computes the variance against the tolerance in force, writes one result per check for the business date and lists every asset or key that breaks, and answers the run record and the quality facts through this service's own operations**, so that **the data steward can say each morning whether the assets on the books match ACE, whether every asset key of the Workbench resolves, and whether the asset side of the reconciliation can be trusted**.

The legacy story built one batch step, JOB-04 Daily reconciliation, that ran five checks REC-01 to REC-05 for the business date of the ACE batch, wrote one `reconciliation_result` row per check and product group, held or released the case list publish, and pushed two CSV extracts to the data lake for a Power BI report. D-RCV-60 keeps the behaviour of the legacy key and splits the ownership along the service boundaries of Architecture v5:

- The enterprise case-list reconciliation - the account count and the balance by product against `v_ace_account`, the treatment and payment checks, the `reconciliation_result` rows and the publish gate of the case list - becomes the rwb-source-data workflow `ReconciliationWorkflow` (RWB-P1-E1011-APP), with the exclusions and the publish gate in the rwb-case slice (RWB-P3-E1011-APP), the notice quality slice in rwb-comms (RWB-P6-E1011-APP), and the end-to-end proof of the whole of JOB-04 in RWB-ITG-E1011-ITG.
- This story owns the facts this service holds: the `listing` and `asset_sale` rows of `rwb_asset`, the asset rows it reads in its own schema, and the asset keys that link them to ACE. It runs the asset side of REC-05, which the FSD P1 defines as the resolution of every `asset_key` on a Workbench table compared on "business key, count and amount" (FSD P1 A2.11.2).
- The asset rows come from DP06 Collateral and assets, whose source is ACE ingested from CCMS, SVAF, AMIS and RPS and whose Workbench objects are `asset`, `listing` and `asset_sale` (FSD P1 A2.2; TSD S5 T3.1). This service reads no view behind that product: only rwb-source-data reads the 30 `recovery.v_ace_*` views (Architecture v5 slides 29, 37 and 45), so the DP06 rows arrive through its contract (DP-05).
- The two lake extracts and the Power BI data set are removed, and the quality facts are served by this service's own read model (DP-17).

### 2. Business rationale

An asset the bank has taken on but never booked, or an asset key on a listing or a sale that points at no ACE asset, is a disposal nobody can complete: the repossession is on the books, the sale is negotiated, and the property or the vehicle cannot be transferred because the record it depends on does not exist. Today nobody sees the gap. The legacy capability reconciled the case list to ACE, the treatments, the payments and every business key, and it wrote its report to a data lake that the target does not have.

In `rwb-asset` the same idea is applied to the facts this service owns: every business date the quality run compares the assets held on the books with the rows of the collateral and assets data product it is allowed to see, computes the count and the book value by asset type, resolves every asset key on the asset, listing and asset_sale rows, compares the variance with the tolerance in force, writes one result per check for the date, and lists every asset or key that breaks. It meets REQ-RDF-007 (the case list reconciles daily to ACE with no variance, and every business key on a Workbench table resolves to an ACE row) and REQ-RDF-008 (breaks, referential completeness and the quality measures are reported to the data product owner), and it applies control CTL-01 and rule R-UNI-40 of the legacy key.

It also serves the FSD S5 precondition - "the data products the module reads carry today's business date, or show their date as stale" - and its staleness rule VR-S5-001-1, which refuses a run whose data product is stale with MSG-P1-001 (FSD S5 A1.4 and A2.1.3.1). The check code REC-05 and its "business key, count and amount" comparison are kept from the legacy key; the three check names COUNT, VALUE and KEY are this story's design and carry no source (GAP-2972; ASM-4880).

Three edges of the legacy capability are no longer this service's to reach. The enterprise reconciliation of the case list, the REC-01 to REC-04 checks and the `reconciliation_result` rows are rwb-source-data's (Ownership Map: `reconciliation_result` is P1's; Architecture v5 slides 15 and 44 give P1 the reconciliation and JOB-04). The exclusions and the publish gate are rwb-case's. The notice person keys are rwb-comms's. The target also removes what the legacy story relied on: the data lake is gone (DP-17, ADR-018), so the reconciliation and data-quality extracts written through INT-19 have no target, and the measures reach rwb-reporting from the services' read models and events; this story therefore writes no extract file and no lake path (GAP-2972; ASM-3163).

No ACE view is read by rwb-asset: Architecture v5 slides 13, 29, 37 and 45 give the views to rwb-source-data alone and give the S5 row no call to P1, so the ACE side of every check arrives as the DP06 rows of the rwb-source-data contract (DP-05, DP-11), while the FSD S5 field catalog still names `v_ace_npa_asset`, `v_ace_asset` and `v_ace_collateral` as the module integration point (FSD S5 A2.6.3.2). The source precedence of Template and Rules R3 resolves that conflict in favour of Architecture v5 (GAP-2972; ASM-3162).

The tolerance and the lists are data. The parameter `recon.tolerance.pct` comes through the parameters contract of rwb-case with its version (DP-06), and the asset types, holding statuses and sale channels come through its reference-data contract (DP-07): LOV-ASSET-TYPE, LOV-HOLDING and LOV-SALE-CHANNEL (TSD S5 T3.2). Neither contract is in this story's Contract dependencies, which the plan sets to None, so both are faked from the published documents (GAP-2972; ASM-3161). The run is a Temporal Schedule and a workflow in this service (DP-10), the tables live in `rwb_asset` (DP-01, DP-15), the run record and the quality facts are reached through the gateway-bff composite route (DP-19), and the topic name of the service comes from the naming library although this story publishes no event (DP-14).

### 3. Preconditions

- The asset objects of `rwb_asset` exist with their baseline: `asset`, `listing` and `asset_sale`, declared by TSD S5 T3.1 and created by the take-on and disposal stories RWB-S5-E3019-APP to RWB-S5-E3021-APP, RWB-S5-E3029-APP and RWB-S5-E4030-APP. Those stories are wave-2 and wave-3 stories and are not in this story's Depends on (build), which the plan sets to None; the run is built and tested against fixtures of their rows (GAP-2972; ASM-4881).
- The per-service Flyway sequence of rwb-asset carries the migration that adds the three quality tables after the asset baseline (DP-15; RWB-PLT-E1044-CON).
- The platform libraries are in place: the decision-record library (RWB-PLT-E1027-CON, DP-03), the parameters client (RWB-PLT-E1042-CON, DP-06), the reference-data client (RWB-PLT-E1043-CON, DP-07), the workflow kit with Schedules (RWB-PLT-E1071-CON, DP-10), the per-service Flyway sequence (RWB-PLT-E1044-CON, DP-15), the naming library (RWB-PLT-E1047-CON, DP-14) and the gateway-bff composite route (RWB-PLT-N001-CON, DP-19). None of them is in this story's Depends on (build) list, which the plan sets to None; they arrive through the platform release train of wave 0 and are assumed present before the wave-1 build (GAP-2972; ASM-3160).
- RWB-P3-E1042-CON is published for the parameter `recon.tolerance.pct` per check with its version, and RWB-P3-E1043-CON for LOV-ASSET-TYPE, LOV-HOLDING and LOV-SALE-CHANNEL by version; neither is in the Contract dependencies row, so both are faked from the published documents (GAP-2972; ASM-3161).
- The rwb-source-data contract is published for the freshness answer of a data product and for the DP06 rows of a business date; it is not in the Contract dependencies row, so it is faked, and the element names behind the two operations are not specified in the source documents (GAP-2972; ASM-3161).
- The parameter `recon.tolerance.pct` is 0.00 in force for the REC-05 COUNT and VALUE checks on the business date, the legacy value under DL25, owned by the center of excellence analyst; the REC-05 KEY check has no percent tolerance: its tolerance is zero orphans (FSD P1 A2.11.2 REC table).
- DP06 Collateral and assets is LOADED for the business date in force in the SIT fixture, or it answers STALE with its last load date; the DP06 refresh is WEEKLY at MON 08:00 (FSD P1 A2.2), so a business date between two refreshes answers the last load date and the run follows that answer (GAP-2972; ASM-3167).
- The check names, the state names, the alert groups and the Schedule cron are configuration of this service read with their version; no value is compiled in (GAP-2972; ASM-4880).
- The SIT fixture holds synthetic asset, listing and sale rows only: no production data and no connection to a real ACE, AMIS, RPS, CCMS or SVAF system.
- The login is the rwb-asset login (DP-02); it holds no grant on any `recovery.v_ace_*` view, no grant on another service's schema and no other service's credential.

### 4. Flow

1. The Temporal Schedule of this service starts `AssetQualityWorkflow` for the business date on task queue `rwb-asset` in namespace `rwb-recovery`, one run per business date; no event starts it (12.4).
2. The workflow asks the tolerance activity for the tolerance of each check through the parameters contract of rwb-case, with the version in force (DP-06); the value is 0.00 for the COUNT and VALUE checks in the fixture of the date, and the KEY check carries the zero-orphan tolerance of REC-05.
3. It asks the read-asset-facts activity for the freshness answer of DP06 for the business date through the rwb-source-data contract; an answer that is not LOADED for the business date in force writes no result and holds the date, with the last load date as the reason (AC4).
4. The same activity reads the DP06 rows of the business date in force through the rwb-source-data contract, one hop with a 2 s timeout (DP-11); no ACE view and no ACE table is read by this service (DP-05).
5. The workflow reads the asset rows of `rwb_asset`: the assets taken on with their asset type, transfer-in type and date, book value and holding status; the listing rows with their asset reference, floor price and status; and the asset_sale rows with their asset reference and sale date.
6. The reconciler computes, per check, the source count, the workbench count, the variance count and the variance percent: COUNT compares the assets held on the books per asset type with the DP06 asset rows of the business date in force, VALUE compares the sum of the book value of the same populations, and KEY resolves every asset key on the asset, listing and asset_sale rows to a DP06 row and counts the orphans (FSD P1 A2.11.2, REC-05 "business key, count and amount").
7. It compares each variance percent with the tolerance in force: PASS when it is equal to or below the tolerance, BREAK when it is above, and for the KEY check PASS only at zero orphans (AC2, AC3).
8. It writes one row per check for the business date, the break rows of every asset or key that does not match in either direction, and the run row, in one transaction, replacing the rows of that date on a rerun; the unique key is the check code, the check name and the business date (AC5, AC6).
9. It sets the run state to RELEASED when every check is PASS and to HELD when any check is BREAK or not run, and it writes the not-run reason of a held run.
10. On a break it lists the breaking assets and keys with their asset type, transfer-in date and the table that holds the key, for the data steward and, where the row is missing in ACE, for the ACE team, and sends the break alert to the data steward, the platform administrator and the team managers with MSG-P1-012 (AC2, AC7).
11. It writes one decision record for the run through the local decision-record library, with the date, the three results and the orphan count, and writes no event and no file: DP-09 is not in this story's pattern set, and the lake, the INT-19 adapter and the two legacy extracts do not exist in the target (AC8; GAP-2972; ASM-3163; ASM-3164).
12. `GET /quality-runs/{businessDate}` answers the run record and `GET /quality-results` answers the quality facts with their break rows from `rwb_asset` alone, and `GET /assets` answers the asset keys of a case or of a business date for the REC-05 resolution that rwb-source-data and the integration proof run (12.1).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A check's variance is above the tolerance | Result BREAK; run state HELD; breaking assets and keys listed; the alert sent | MSG-P1-012 | AC2 |
| X2 | The variance equals the tolerance | Result PASS | None | AC3 |
| X3 | DP06 is not LOADED for the business date in force | The run is HELD, writes no result for the date, shows every check as not run with the last load date as the reason | MSG-P1-001 | AC4 |
| X4 | The run repeats for the same date after a fix | The rows of that date are replaced and the run is RELEASED if every check is PASS | None | AC5 |
| X5 | Two runs for the same date on two workers | One row per check and business date; no row written twice | None | AC6 |
| X6 | An asset key has no DP06 row, or a listing or sale references an asset key that no asset row holds | The key is a break with its table and its reason; no asset, listing or ACE row changes | None | AC7 |
| X7 | The parameters contract or the rwb-source-data contract fails mid-run | No result for the date; run state FAILED with the system named; the rerun writes every row | MSG-GEN-006 | TC-E1-011-09 |
| X8 | A role without Platform administration R reads the run record or the break rows | 403, and nothing is written | MSG-P4-002 | TC-E1-011-07 |
| X9 | A caller reads a path outside `/api/recovery/asset/v1`, a cross-schema read appears, or an extract file or lake path is written | The build fails the boundary test and nothing is released | None | BR10 |
| X10 | The token carries no Workbench role | 401, and nothing is written | MSG-P4-001 | TC-E1-011-07 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the rows the take-on and disposal stories write and builds against their fixtures and the fakes of 12.8; it changes no asset, listing or sale and reads no table of another service |
| Negotiable | The tolerance is a parameter with a version, the asset types and statuses are reference data, and the check names, alert groups and Schedule are configuration, not code |
| Valuable | The data steward sees each morning which assets of the date are on the books in ACE but not in the service, or the other way round, and which asset keys lead nowhere |
| Estimable | One workflow, one Schedule, three checks, three tables and three read operations |
| Small | Fits two weeks with its tests, as the secondary slice of the legacy key |
| Testable | Each criterion below is one automated test on synthetic rows and the four contract fakes, with no ACE view and no data lake |

### 7. Acceptance criteria

```gherkin
Feature: Reconciliation and data quality of the assets on the books, in rwb-asset

  Background:
    Given the business date is 2026-11-30
    Given the parameter recon.tolerance.pct = 0.00 is in force for the REC-05 COUNT and VALUE checks
    Given the rwb-source-data contract mock returns the freshness answer LOADED for DP06 Collateral and assets for 2026-11-30

  Scenario: AC1 Variance zero (new, D-RCV-60)
    Given the rwb-asset asset rows of 2026-11-30 hold 12 assets taken on: 6 DETACHED_HOUSE, 4 CONDOMINIUM and 2 VEHICLE
    Given the rwb-source-data contract mock returns 12 DP06 asset rows of 2026-11-30, one for each of the 12 asset keys, with equal book value sums per asset type
    Given every asset key on the asset, listing and asset_sale rows of 2026-11-30 resolves to one of the 12 rows
    When the quality run of 2026-11-30 runs
    Then the system writes three rows for 2026-11-30, REC-05 COUNT, REC-05 VALUE and REC-05 KEY, each with variance 0 and result PASS
    Then the run state of 2026-11-30 is RELEASED
    Then GET /quality-results answers the three rows with their counts, the tolerance in force and no break row

  Scenario: AC2 Variance over the tolerance (new, D-RCV-60)
    Given the rwb-asset asset rows of 2026-11-30 hold 48 VEHICLE assets taken on
    Given the rwb-source-data contract mock returns 45 DP06 VEHICLE asset rows of 2026-11-30, a variance of 3 assets, 6.25 percent
    When the quality run of 2026-11-30 runs
    Then the REC-05 COUNT result for VEHICLE is BREAK with variance count 3 and variance percent 6.25
    Then the 3 asset keys that no asset row holds are on the break list for the data steward, with their transfer-in dates from the data product
    Then the run state of 2026-11-30 is HELD
    Then the data steward, platform administrator and team manager groups receive MSG-P1-012 "The case list for 2026-11-30 does not reconcile to ACE for VEHICLE: a difference of 3 accounts, 6.25 percent."
    Then SCR-45 shows the REC-05 COUNT break with the 3 break rows and the REC-05 KEY result is unchanged

  Scenario: AC3 Variance equal to the tolerance (new, D-RCV-60)
    Given the parameter recon.tolerance.pct for the REC-05 COUNT check is changed by a reference load to 6.25 from 2026-11-30
    Given the VEHICLE variance is 6.25 percent and the DETACHED_HOUSE variance is 6.30 percent
    When the quality run of 2026-11-30 runs
    Then the VEHICLE result is PASS and the DETACHED_HOUSE result is BREAK

  Scenario: AC4 The collateral and assets data product is not loaded for the date (new, D-RCV-60)
    Given the rwb-source-data contract mock returns no LOADED answer for DP06 Collateral and assets for 2026-11-30 and the stale marker naming "DP06 Collateral and assets" and 2026-11-23
    When the Schedule starts the quality run of 2026-11-30
    Then the run writes no quality result for 2026-11-30 and its state is HELD
    Then GET /quality-runs/2026-11-30 shows REC-05 COUNT, REC-05 VALUE and REC-05 KEY as not run with the reason "DP06 Collateral and assets is from 2026-11-23"
    Then the data steward, platform administrator and team manager groups receive MSG-P1-001 naming the product and the date

  Scenario: AC5 Rerun after the fact is fixed (new, D-RCV-60)
    Given the REC-05 COUNT result for VEHICLE is BREAK and the run state of 2026-11-30 is HELD
    Given the 3 missing assets have since been taken on and their asset rows carry the three asset keys of the data product
    When the platform administrator restarts the quality run for 2026-11-30
    Then the run replaces the three rows for 2026-11-30 and all are PASS
    Then the run state of 2026-11-30 is RELEASED
    Then GET /quality-results answers the three rows of the rerun and no row of the earlier run

  Scenario: AC6 Two runs for the same date (new, D-RCV-60)
    Given two quality runs for 2026-11-30 start on two workers
    When both reach the reconciliation activity
    Then asset_quality_result holds one row per check and business date, three rows in all
    Then no row is written twice for the same rec_code, quality_check and business_date

  Scenario: AC7 An asset key with no data product row (new, D-RCV-60)
    Given the rwb-asset asset row of case "RW-2026-000140" carries the ACE asset key "AK-0099881", which has no row in the DP06 rows of 2026-11-30
    Given a listing row of 2026-11-30 carries the asset key "AK-0000777", which no asset row of rwb_asset holds
    When the REC-05 KEY check of 2026-11-30 runs
    Then the REC-05 KEY result for 2026-11-30 is BREAK with 2 orphans
    Then "asset AK-0099881" is on the break list for the data steward and the ACE team
    Then "listing AK-0000777" is on the break list for the data steward
    Then no asset row, listing row or ACE row changes

  Scenario: AC8 No data-lake extract (new, D-RCV-60)
    Given the quality run of 2026-11-30 has finished with PASS on its three checks
    When the run completes
    Then the three rows and their break rows are readable through GET /quality-runs/2026-11-30 and GET /quality-results
    Then no reconciliation extract and no data quality extract is written, no INT-19 adapter is called and no lake path exists for the date
```

Every criterion above is new under D-RCV-60; no legacy acceptance criterion of RWB-E1-011 is owned or restated here. The legacy criteria of the key are owned by RWB-P1-E1011-APP (AC5, AC6 and AC8) and proved end to end by RWB-ITG-E1011-ITG (AC1, AC2, AC3, AC4 and AC7), whose contract and deployment slices carry the same ids (GAP-2972; ASM-4882). The one Given line each criterion adds over a pure unit test is the mock of the rwb-source-data contract, because the asset side of every check is the only cross-service part and is mocked with 12.8 (DP-11).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every business date, rwb-asset reconciles the assets it holds on the books against the rows of the collateral and assets data product of the business date in force, by count and by sum of book value per asset type | REC-05; REQ-RDF-007; FSD P1 A2.11.2; legacy BR1 and BR2 |
| BR2 | The variance count is the difference between the two sides of a check; the variance percent is that difference over the source side, and both are written on the result row with the tolerance applied | TSD P1 `reconciliation_result` (DF-OPS-122 to DF-OPS-129); legacy section 7 |
| BR3 | A result is BREAK when the variance percent is above the tolerance and PASS when it is equal to or below it; the boundary value is a PASS | Legacy AC3 and BR6 |
| BR4 | The tolerance per check is the parameter `recon.tolerance.pct` read through the parameters contract of rwb-case with the version in force, never a value in code; 0.00 is the value of the date under DL25 | DP-06; legacy preconditions and BR6; DL25 |
| BR5 | Every `asset_key` on the asset, listing and asset_sale rows of `rwb_asset` must resolve to a row of the collateral and assets data product; zero orphans, and every one is listed with its table and its key | REC-05; REQ-RDF-007; FSD P1 A2.11.2; legacy BR5 |
| BR6 | No reconciliation runs until the owner of the data product answers LOADED for the business date in force; a run that cannot obtain that answer writes no result and holds the date with the last load date as its reason | Legacy BR9; FSD S5 VR-S5-001-1 and A1.4; MSG-P1-001 |
| BR7 | A repeated run for the same date replaces that date's rows, and a passing rerun releases the date | Legacy BR11 and AC5; R-UNI-40 |
| BR8 | Two runs for the same date produce one row per check and business date; the unique key is the rec code, the check name and the business date | Legacy AC6; R-UNI-40 |
| BR9 | A break lists the asset key or business key, the asset type where the row carries one, the transfer-in date from the data product and the table that holds the key, for the data steward and, where the row is missing in ACE, for the ACE team | Legacy BR7 and BR13; FEAT-RDF-12 |
| BR10 | The quality facts are this service's own rows: no data lake, no INT-19 adapter, no extract file and no outbound item is written for the date, and no table of another service is read | DP-17; ADR-018; Architecture v5 slides 37 and 44; legacy section 12 reversed |
| BR11 | Grades of the run: PASS, BREAK, and not run with its reason | Legacy BR10; FEAT-RDF-12 |
| BR12 | The run uses one business date only, the business date in force of the data product it reconciles against, and never a mix of two business dates | Legacy BR12; BR-P1-011-2 |
| BR13 | An asset break never changes or deletes an asset, listing, sale or ACE row; the rerun through the workflow is the only path that replaces the rows of a date | Legacy BR13; FSD P1 BR-P1-011-3 |
| BR14 | A role without the right of the capability area is refused with MSG-P4-002 and nothing is written | FSD P1 AC-EXC-P1-011-03; legacy section 5 X8 |

The check code of all three checks is REC-05, because the FSD P1 defines REC-05 as the resolution of every business key on a Workbench table compared on "business key, count and amount", and the asset keys are the part of that check this service owns. REC-06 to REC-09, named in the legacy out-of-scope list, are not this story's and are listed in section 19.

### 9. State transitions

None for a case status and none for an asset. This story changes no asset, listing or sale; it writes the state of its own run row and the result rows of the business date.

| From | Event | Condition | To |
|---|---|---|---|
| Not run | The Schedule starts the run | The data product answers LOADED for the business date in force | Running |
| Not run | The Schedule starts the run | The answer is not LOADED, or cannot be read | Held, with the not-run reason and the last load date on the run row |
| Running | The three checks are computed | Every check is PASS | Released |
| Running | The three checks are computed | At least one check is BREAK | Held |
| Running | A source read fails | The parameters or the asset facts cannot be read | Failed, with the system named and no result row for the date |
| Held | A rerun for the same date | The rows of the date are replaced and every check is PASS | Released |
| Released | A rerun for the same date | A check is BREAK | Held |

The result value set is the legacy `reconciliation_result.result`, LOV-REC-RESULT: PASS and BREAK, plus the not-run grade and its reason that legacy BR10 defines and that this story writes on the run row only, never as a third result value (GAP-2972; ASM-4880).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-asset service identity | Runs the workflow, reads the parameters, the reference data and the asset facts through their owners' operations, and writes the run row, the result rows and the break rows of `rwb_asset`; it holds no grant on another schema and no grant on `recovery.v_ace_*` |
| RW-DATASTEW, data steward and data product owner | Platform administration R: reads the run record, the results and the break rows, and signs the daily asset quality result |
| RW-PLATADM, platform administrator | Platform administration R and U: reads the results and restarts the run for a business date |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-SECADM | Read the results and the break rows in the Platform administration area, right R |
| RW-NPAMGR, RW-HEADNPA, RW-SALEOFF and the other asset and disposal readers | Asset and disposal R on `GET /assets`, scope applied (TSD S5 T6.1) |
| rwb-source-data and the integration run service identities | Read `GET /assets` for the REC-05 resolution of the enterprise reconciliation; no write and no other operation |

The right of the two quality reads is declared in the Platform administration capability area, right R, as the legacy story declares it for its job listing. TSD S5 T6.1 declares only the Asset and disposal column, so the module matrix neither grants nor refuses a Platform administration right; the legacy story comes first in the fill order of Template and Rules R7.3 and the right is kept (GAP-2972; ASM-3166). DP-08 is not in the patterns applied: the declared area and right are enforced at gateway-bff for the screen path, and where a local guard is required on the operation itself the guard and its story are not named in the sources.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-COL-028 | asset | id | Read |
| DF-COL-029 | asset | case_id | Read, to answer the asset keys of a case on `GET /assets` |
| DF-COL-031 | asset | asset_ref | Read |
| DF-COL-032 | asset | asset_code | Read |
| DF-COL-033 | asset | asset_type | Read, the grouping key of the COUNT and VALUE checks |
| DF-COL-034 | asset | transfer_in_type | Read |
| DF-COL-036 | asset | transfer_in_date | Read |
| DF-COL-037 | asset | book_value | Read, the amount side of the VALUE check |
| DF-COL-041 | asset | holding_status | Read, to select the assets on the books |
| DF-SAL-001 | listing | id | Read |
| DF-SAL-002 | listing | asset_id | Read |
| DF-SAL-003 | listing | sale_channel | Read |
| DF-SAL-008 | listing | status | Read |
| DF-SAL-009 | asset_sale | id | Read |
| DF-SAL-010 | asset_sale | asset_id | Read |
| DF-SAL-013 | asset_sale | sale_date | Read |
| The column that holds the ACE asset key on the `asset` row | asset | the ACE `asset_key` the listing and the sale link by | Read; the column is not named in TSD S5 T3.1, which declares `asset_ref` and `asset_code` (GAP-2972; ASM-4881) |
| DF-ACE-100 | v_ace_asset / the DP06 asset rows | asset_key | Read, through the rwb-source-data contract only |
| No BR Field ID | the DP06 asset rows (P1) | the asset key, asset type, transfer-in date and book value of each asset | Read through the rwb-source-data contract; the element names are not specified in the source documents (GAP-2972; ASM-3161) |
| No BR Field ID | asset_quality_run, asset_quality_result, asset_quality_break | the run state, the check, the counts, the amounts, the variance, the tolerance and the break reason | Write; the service's own tables, whose columns carry no field ID in the sources (GAP-2972; ASM-4880) |

**Indexes and migration.** The three tables arrive in the per-service Flyway sequence (DP-15), as `V1011_1__asset_quality.sql` by the convention of the service, after the `asset`, `listing` and `asset_sale` baseline: `asset_quality_run` with a unique business date, `asset_quality_result` with a unique (rec_code, quality_check, business_date), and `asset_quality_break` with an index on (business_date, rec_code) and on the asset key.

**The data product link.** The asset rows of DP06 are rwb-source-data's data product and are read through its contract only; the asset key is the match key and is held on the asset row of `rwb_asset` by the take-on stories. Nothing in this story is a foreign key across schemas (DP-01).

**No personal data.** The run row, the result rows and the break rows carry an asset key, an asset reference, a case ID, an asset type, a holding status, a sale channel, dates, counts, amounts and a percent. No party, contact value, identity number or address enters these tables, and no such value is logged or read by this run.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1`.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | The asset keys and identifiers of a case, or of the business date in force, with the asset type, transfer-in date, holding status and asset reference, for the REC-05 resolution that rwb-source-data and the integration run run; no price, no party and no valuation is answered | Asset and disposal R, scope applied; the rwb-source-data and integration service identities for the reconciliation run | Not applicable |
| GET | `/quality-runs/{businessDate}` | The run record of the business date: the state RELEASED, HELD or FAILED, each check with PASS, BREAK or not run and its reason, the variance count and percent, the tolerance in force, the count of break rows and the times of the run | Platform administration R, scope applied | Not applicable |
| GET | `/quality-results` | The quality facts of a business date with their break rows: rec code, check, source and workbench counts, amounts, variance count, variance percent, tolerance percent, result, and per break row the asset key, the table, the asset type and the reason | Platform administration R, scope applied; Reporting R for the report reader | Not applicable |

All three are reads: they declare no Idempotency-Key, answer 401, 403, 404 and 503 with the platform error envelope, and answer from `rwb_asset` only. The asset list path is the first API path that Architecture v5 slide 41 gives rwb-asset and the one RWB-ITG-E1011-ITG calls for the asset keys of REC-05; the two quality operations and their paths are this story's design, because no source names a quality run record, a result read or a break list for rwb-asset (GAP-2972; ASM-4880).

#### 12.2 REST operations consumed

| Method | Path | Owner | Used for |
|---|---|---|---|
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | The LOADED or STALE answer of DP06 Collateral and assets for the business date in force, with its last load date, before any check runs (AC4); faked (GAP-2972; ASM-3161) |
| GET | `/api/recovery/source-data/v1/data-products/DP06/records` | P1 rwb-source-data | The asset rows of DP06 for the business date in force, for the count, the value and the key side of REC-05; faked, and the element names are not specified in the source documents (GAP-2972; ASM-3161) |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The parameter `recon.tolerance.pct` per check with the version in force (DP-06, AC3); faked (GAP-2972; ASM-3161) |
| The reference-data read of the rwb-case contract (RWB-P3-E1043-CON) | P3 rwb-case | LOV-ASSET-TYPE, LOV-HOLDING and LOV-SALE-CHANNEL by version, so no list value is in code (DP-07); faked, and the path is not named in the source documents (GAP-2972; ASM-3161) |

Every row is one hop with a 2 s timeout, one GET retry with jitter and a breaker per downstream (DP-11, ADR-020). The quality facts are handed over through the two quality reads of 12.1: rwb-reporting reads them for the report of the date and rwb-source-data reads the asset keys for the REC-05 resolution of its own run. No operation of rwb-reporting accepts a push - its operations are `GET /dashboards/{id}`, `GET /reports/{id}` and `POST /reports/{id}/run` (Architecture v5 slide 15) - so the hand-off is this service's read model and no target operation for a push is named in the sources (GAP-2972; ASM-3163).

#### 12.3 Events published

None. DP-09 is not in the pattern set of this story, so no event is written to the outbox and no Kafka record is published by this run. The topic `rwb.asset.events.v1` carries `rwb.asset.AssetTakenOn.v1` and `rwb.asset.AssetSold.v1` from the take-on and sale stories (Architecture v5 slide 19) and none of this story; the quality facts are served by the reads of 12.1 (GAP-2972; ASM-3164).

#### 12.4 Events consumed

None. The run is started by the Schedule of 12.6 and reads no event; the asset facts arrive synchronously through the rwb-source-data contract, and a redelivered event cannot start a second run. The events that judge a disposal - `rwb.litigation.JudgmentRecorded.v1`, `rwb.litigation.AuctionResult.v1` and `rwb.payment.ProceedsMatched.v1` - belong to the disposal workflows of this service and not to this quality run (Architecture v5 slide 19).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Element |
|---|---|---|---|
| `AssetQualityWorkflow` | Workflow from the kit template; one per business date | `rwb-asset` in namespace `rwb-recovery` | Owns the run: the parameter read, the freshness gate, the three checks, the rows of the date and the run state |
| `loadTolerance` | Activity, calls rwb-case (P3) | `rwb-asset` | Reads `recon.tolerance.pct` per check with its version before any check runs |
| `readAssetFacts` | Activity, calls rwb-source-data (P1) | `rwb-asset` | Reads the freshness answer and the DP06 asset rows of the business date; writes nothing when the answer is not LOADED |
| `reconcileAssets` | Activity, reads `rwb_asset` only | `rwb-asset` | Computes the three checks, their counts, amounts, variance and percent, and the break rows of the date |
| `writeQualityFacts` | Activity, writes `rwb_asset` only | `rwb-asset` | Writes the run row, the result rows and the break rows in one transaction and replaces the rows of the date |

The workflow is idempotent by business date and check: a retried run does not write a second row for the same key and does not restart a released date without a rerun request. The decision record of the run is written through the local decision-record library in the same transaction as the rows.

#### 12.6 Schedules

One Schedule, owned by this service.

| Schedule | Cron | Overlap | Catch-up | What it starts |
|---|---|---|---|---|
| The asset quality Schedule of rwb-asset (RWB-PLT-E1071-CON) | Not specified in the source documents (GAP-2972; ASM-4880) | SKIP | Catch-up window of the workflow kit | `AssetQualityWorkflow` for the business date, after the DP06 refresh window of the catalog (MON 08:00) has passed |

No Quartz row, no shared job table entry and no Control-M job is registered for this run; JOB-04 stays rwb-source-data's event-triggered workflow (Architecture v5 slide 44), and the only Schedule this service already owns is JOB-19 re-appraisal, monthly (Architecture v5 slides 19 and 44).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| listing | S5 (rwb_asset) | The listings with their asset reference, floor price and status; read only |
| asset_sale | S5 (rwb_asset) | The sales with their asset reference and sale date; read only |
| asset_quality_run | S5 (rwb_asset) | The run of one business date: state, not-run reason, times and break count |
| asset_quality_result | S5 (rwb_asset) | One row per check and business date: counts, amounts, variance, percent, tolerance and result |
| asset_quality_break | S5 (rwb_asset) | One row per breaking asset or key of a check, with its table and its reason |

The three quality tables are this story's design and carry no field ID in the sources (GAP-2972; ASM-4880). The `asset` object is declared by TSD S5 T3.1 as an S5 object but is absent from the Ownership Map's S5 table row, which names `asset_sale` and `listing`; it is read inside `rwb_asset` and its ownership row is carried as a gap (GAP-2972; ASM-4881). Not owned and never read as a table: `reconciliation_result`, `case_list_row` and the DP06 rows (P1), `recovery_case` and `case_entry_exclusion` (P3), `treatment` (S2), `proceeds` (P8), `document` (P5), `notice` (P6).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data freshness fake | LOADED for DP06 Collateral and assets for 2026-11-30 with its load time; not LOADED, with the stale marker naming "DP06 Collateral and assets" and 2026-11-23; an error after the first read | AC1, AC2, AC3, AC4, AC7 |
| rwb-source-data DP06 records fake | 12 asset rows of 2026-11-30 matched to the 12 asset rows, with equal book value sums; 45 VEHICLE rows against 48 asset rows; one row whose asset key matches no asset row | AC1, AC2, AC3, AC5, AC7 |
| rwb-case parameters fake | `recon.tolerance.pct` 0.00 for the COUNT and VALUE checks, and the 6.25 version in force from 2026-11-30 of AC3 | AC1, AC2, AC3 |
| rwb-case reference-data fake | LOV-ASSET-TYPE with DETACHED_HOUSE, TOWNHOUSE, CONDOMINIUM, LAND, COMMERCIAL_BUILDING and VEHICLE; LOV-HOLDING; LOV-SALE-CHANNEL, by version | AC1, AC2, AC7 |

The fakes are test-only and are replaced by the real services in SIT; the drift between a fake and the published document is a build failure. The fixture values are synthetic asset rows of the take-on and disposal stories, and no production value is used.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 4 consumed | The asset keys, the run record and the quality facts; the freshness answer, the DP06 rows, the parameter read and the reference read; one hop and 2 s each |
| Kafka | 0 published, 0 consumed | DP-09 is not in the pattern set of this story and the run is Schedule-started |
| Temporal | 1 workflow, 4 activities | `AssetQualityWorkflow` on `rwb-asset` with `loadTolerance`, `readAssetFacts`, `reconcileAssets` and `writeQualityFacts` |
| File | 0 | No extract file and no outbound item: the data lake and the INT-19 adapter are removed (DP-17) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.asset`, module `quality`, Java package `th.co.scb.ace.workbench.recovery.asset.quality`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

Seven patterns add a platform CON in the DP table and two add a contract of rwb-case, while the plan sets this story's Depends on (build) and Contract dependencies to None. Both lists stay None as the plan sets them: the platform CONs land through the platform release train of wave 0, before the wave-1 build, and are not a lane dependency of an APP story (GAP-2972; ASM-3160); the two rwb-case contracts and the rwb-source-data contract are built against their published documents and fakes and never block the build (GAP-2972; ASM-3161). DP-05 applies as a prohibition and as a read: this service reads no ACE view and no ACE table, and the DP06 rows arrive through the rwb-source-data contract, the only reader of `recovery.v_ace_*` (Architecture v5 slides 29, 37 and 45); the view names of FSD S5 A2.6.3.2 are read as the data product behind that contract (GAP-2972; ASM-3162). DP-17 is applied as the removal of the lake target: the two extracts of the legacy publish step are dropped and the quality facts are served from this service's read model (GAP-2972; ASM-3163). DP-14 applies to the naming only: this story publishes no event. DP-03 is applied where a rule decides the handling of a break; the record is written first through the library and a failed write stops the run.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AssetQualityController | Controller | `GET /quality-runs/{businessDate}` and `GET /quality-results`, with the problem mapping for 401, 403, 404 and 503 |
| AssetKeyController | Controller | `GET /assets` for the REC-05 asset keys, scoped and without price or party |
| AssetQualityWorkflow | Workflow | The run of section 4: parameter read, freshness gate, the three checks, the rows and the state |
| ToleranceReader | Service | Reads `recon.tolerance.pct` per check with its version through the parameters contract |
| AssetFactReader | Service | Reads the freshness answer and the DP06 asset rows of the business date through the rwb-source-data contract, and returns nothing when the answer is not LOADED |
| AssetReconciler | Service | Computes the source and workbench counts, the amounts, the variance, the variance percent and the result of the COUNT, VALUE and KEY checks |
| QualityFactWriter | Service | Writes the run, the results and the break rows in one transaction, replacing the rows of the date |
| QualityBreakNotifier | Service | Sends the MSG-P1-012 and MSG-P1-001 wording to the configured groups |
| QualityReadModel | Service | Answers the three reads of 12.1 from `rwb_asset` only |

**Database and migrations.** `V1011_1__asset_quality.sql` creates `asset_quality_run`, `asset_quality_result` and `asset_quality_break` with the unique keys and indexes of section 11, after the asset baseline of the take-on and disposal stories. No column is added to `asset`, `listing` or `asset_sale`, and no column carries another service's data (DP-01, DP-15). The column that holds the ACE asset key on the asset row is fixed by the take-on stories; where it is not yet named, this story reads the key from the column they declare (GAP-2972; ASM-4881).

**Configuration and reference data.** The parameter key of each check, the check names COUNT, VALUE and KEY under the rec code REC-05, the state names, the alert recipient groups and the Schedule cron are configuration and reference data read with a version, owned by the platform administrator; the tolerance value is the parameter of 12.2 and is never compiled in. The asset types, holding statuses and sale channels are reference data through DP-07 (TSD S5 T3.2).

**Build steps**

1. Write the migration and test the three unique keys and the two query indexes.
2. Build `ToleranceReader` and `AssetFactReader` over the two fakes, with the freshness gate and the stale marker; test AC4.
3. Build `AssetReconciler` for the COUNT and VALUE checks per asset type; unit test variance 0, the tolerance boundary and a break; tests for AC1, AC2 and AC3.
4. Build the KEY check over the asset, listing and asset_sale rows, both directions; test AC7 and the no-change rule.
5. Build `QualityFactWriter` with the replace of one date and the unique key; tests for AC5 and AC6.
6. Build `QualityReadModel` and the three controllers over the read model; test the access refusal and the no-extract assertion of AC8.
7. Build `AssetQualityWorkflow` with the Schedule hook and the retry rule by business date and check.
8. Add the run to the job monitor surface of SCR-44 and to the break list of SCR-45 through the gateway-bff route, and prove that no file, no outbound item and no lake path is written.

**Feature flag.** `rwb.asset.quality-run-v1`, read as a flag of the platform library; off means the Schedule starts no run, the read model answers nothing for the date and no result row is written.

**Done when.** The tests in section 16 pass, the contract test of the asset list path stays green for the integration run, and a SIT week shows one run per business date, three result rows per date, a HELD date on a break and on a stale DP06, a RELEASED date after the rerun, no asset changed by the run, and no extract file, outbound item or lake path for any date.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-012 | A check breaks the tolerance | The case list for {date} does not reconcile to ACE for {product}: a difference of {variance} accounts, {pct} percent. |
| MSG-P1-001 | The collateral and assets data product is not loaded; the run is held | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-006 | A contract or the store is unavailable during the run | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | A role without the Platform administration right reads the run or the breaks | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | The token carries no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. |

The five texts are copied unchanged from the legacy story, the FSD S5 staleness rule and the platform message catalog, and the placeholders are the values the tests of section 7 assert: the business date, the asset type VEHICLE, the variance 3 and the percent 6.25 for MSG-P1-012, and "DP06 Collateral and assets is from 2026-11-23" for MSG-P1-001. The legacy wording of MSG-P1-012 speaks of the case list and of accounts, which is rwb-source-data's check; the text is kept because the legacy message set is kept, and the asset type and count fill the same placeholders.

### 15. Screens and states

No screen is built in this story. Existing surfaces show what it writes, through the gateway-bff composite route (DP-19):

| Surface | What it shows |
|---|---|
| SCR-44 Interface and job monitor | The quality run of the business date in the states Running, failed and complete, with the state RELEASED or HELD, the three checks, the variance and the break count |
| SCR-45 Data quality | The results of the date with PASS, BREAK or not run and the reason, the break rows of each check with their table and asset key, and the quality facts that rwb-reporting reads for the report |
| The report "Reconciliation and data quality" (rwb-reporting) | Read-only for RW-BIANAL and the report readers: the asset quality result of the date beside the enterprise reconciliation result that rwb-source-data publishes |
| The asset screens of this service | Their asset keys come from the same rows the KEY check reads, so a broken key is visible on the asset record where the officer works it |

The route merges the answers of this service with the case and the report; the screen field lists and the masking of customer fields belong to RWB-PLT-N001-CON and the edge stories, not here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-011-07 | Access; the run record, the quality facts and the asset keys of 12.1 | Component | RW-CASEOWN calls `GET /quality-runs/2026-11-30`; refused with MSG-P4-002; no token is refused with MSG-P4-001 |
| TC-E1-011-01 | AC1, AC8, BR1, BR2, BR10, BR11 | End to end | 12 assets of 2026-11-30, 6 DETACHED_HOUSE, 4 CONDOMINIUM and 2 VEHICLE; 12 DP06 rows with equal book value sums; no extract file and no lake path |
| TC-E1-011-02 | AC2, BR3, BR9, BR11 | End to end | 48 VEHICLE assets against 45 DP06 rows, a variance of 3 assets, 6.25 percent |
| TC-E1-011-03 | AC3, BR3, BR4 | End to end | Tolerance 6.25; variances 6.25 and 6.30 percent |
| TC-E1-011-04 | AC4, BR6, BR11 | End to end | No LOADED DP06 for 2026-11-30; stale marker "DP06 Collateral and assets is from 2026-11-23" |
| TC-E1-011-05 | AC5, BR7, BR8 | End to end | Break of 3 VEHICLE assets, the three assets taken on, restart |
| TC-E1-011-06 | AC6, BR8 | End to end | Two runs for 2026-11-30 on two workers |
| TC-E1-011-08 | AC7, BR5, BR9, BR13 | End to end | Asset row with asset key AK-0099881 absent from the DP06 rows; listing with asset key AK-0000777 held by no asset row |
| TC-E1-011-09 | AC4, BR6, BR12 | NFR | The rwb-source-data contract forced to fail after the first read; MSG-GEN-006 naming the system; the rerun writes all three rows |

The nine legacy test cases of the key are kept with their legacy IDs and legacy data and are run on the fixtures of this slice. TC-E1-011-07 has no acceptance criterion of its own: the legacy Access case is carried as the access row of this story, exactly as the legacy table carries it. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the tolerance, the check names, the state names, the alert groups and the cron are configuration or parameters read with a version; the asset types, holding statuses and sale channels are reference data.
- No personal data in logs, tables, tests or prompts: the run, the results and the break rows carry an asset key, an asset reference, a case ID, an asset type, a status, dates, counts, amounts and a percent only; no party, contact value, identity number or address is read or written.
- ACE data only through the owner's contract: the asset rows of DP06 arrive through the rwb-source-data contract, and this service holds no grant on any `recovery.v_ace_*` view and opens no ACE table (DP-05).
- No read of another service's tables and no cross-schema join: `reconciliation_result` stays rwb-source-data's and is not read here, the case is rwb-case's, the report is rwb-reporting's (DP-01).
- No data lake and no extract: no INT-19 adapter, no outbound item and no extract file is written or read for any date, and the boundary test fails the build if a lake path appears (DP-17).
- The run is Schedule-started only: no event starts it and no Kafka record is published by it, because DP-09 is not in this story's pattern set.
- Every consumed call is one hop with a 2 s budget, one GET retry with jitter and a breaker per downstream; no call chain.
- A break never changes an asset, a listing, a sale, a case or an ACE row; the rerun through the workflow is the only path that replaces the rows of a date.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-007 | The case list reconciles daily to the count of accounts in `v_ace_account` with no variance, and every business key on a Workbench table resolves to an ACE row | Epic 1, 3.1; Program, 5.1 | FEAT-RDF-11, FEAT-RDF-13, FEAT-RPT-05 | All recovery processes | REC-05; CTL-01; R-UNI-40 | TC-E1-011-01, TC-E1-011-02, TC-E1-011-08 |
| REQ-RDF-008 | Data quality checks run in ACE ingestion; the Workbench reports breaks, referential completeness and its quality measures, each break with a reason visible to the data product owner | Epic 1, 3.1 and 3.8; Program, 5.1 | FEAT-RDF-12, FEAT-RPT-09 | 15 Manage performance, data and AI | REC-05; CTL-01 | TC-E1-011-02, TC-E1-011-03, TC-E1-011-04, TC-E1-011-05 |
| REQ-CWC-004 | Exclusion rules for deceased, fraud, bankruptcy, an active restructure plan and an open dispute are held as data and applied at creation | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-05 | 6.1 Take over the case at 90 days past due | None in this slice | None in this slice; the exclusions are RWB-P1-E1011-APP's and RWB-P3-E1011-APP's |

REC-01 to REC-04 are not in the rules column of this story: they compare the case list with `v_ace_account`, the treatments and the payments and belong to the enterprise reconciliation, owned by RWB-P1-E1011-APP and proved end to end by RWB-ITG-E1011-ITG. CTL-01 is the control the legacy key applies and REC-05 is the check this slice owns, restricted to the asset keys.

| Item | What it covers in this story |
|---|---|
| Legacy key RWB-E1-011 | The asset slice of the daily reconciliation: the assets on the books and their keys; no legacy AC owned here, since AC1 to AC8 belong to RWB-P1-E1011-APP, RWB-ITG-E1011-ITG and the P1 contract and deployment slices (GAP-2972; ASM-4882) |
| RWB-P1-E1011-APP, -CON, -OPS | The enterprise JOB-04 workflow, its `reconciliation_result` rows, REC-01 to REC-04 and the REC-05 resolution of P1's own tables |
| RWB-ITG-E1011-ITG | The end-to-end proof of JOB-04 across the wave-1 services, which reads `GET /assets` of this service for the asset keys of REC-05 |
| RWB-P3-E1011-APP / RWB-P6-E1011-APP | The exclusion resource and publish gate of the case list / the notice quality slice of the same legacy key |
| The P1 `reconciliation_result` table and the DP06 data product | Owned by P1; the DP06 rows are read through its contract and never as a table |
| The P9 reporting model | Reads the quality facts of 12.1 and the business events of the date; no event of this story feeds it |
| The lake removal | The two legacy extracts and the INT-19 adapter are dropped (DP-17, ADR-018) |
| DP-01, DP-02, DP-03, DP-05, DP-06, DP-07, DP-10, DP-11, DP-14, DP-15, DP-17, DP-19 | The twelve patterns of the metadata row, applied as the table of section 13 states |
| ADR-013, ADR-014, ADR-018, ADR-020, ADR-021 | 19 services; schema and login per service; no data lake; contract-first REST with one hop and 2 s; per-service Flyway |

### 19. Out of scope

- The enterprise reconciliation of the case list to ACE, its REC-01 to REC-04 checks, the REC-05 resolution of P1's own tables, the `reconciliation_result` rows and the publish gate of the case list: RWB-P1-E1011-APP, RWB-P1-E1011-CON and RWB-P1-E1011-OPS.
- The end-to-end proof of JOB-04 across the wave-1 services, including the call of `GET /assets` for the asset keys of REC-05: RWB-ITG-E1011-ITG.
- The exclusion rules and the exclusion resource of rwb-case: RWB-P3-E1011-APP; the notice quality slice of rwb-comms: RWB-P6-E1011-APP.
- The build of the asset records themselves - take-on from repossession, deed in lieu and LED, the holding and its provisions, the floor price, the listing, the auction rounds and the sale: RWB-S5-E3019-APP to RWB-S5-E4034-APP, in particular RWB-S5-E3024-APP for the stock balance and RWB-S5-E3029-APP for the listing.
- DP06 and its freshness stamp, the ACE view contract and the freshness answer: rwb-source-data (RWB-P1-E1001-APP, RWB-P1-E1015-APP, RWB-P1-E1069-APP).
- The other legacy reconciliations of the legacy out-of-scope list - REC-06 write-offs, REC-07 assets taken on as a separate reconciliation, REC-08 the decision log copy and REC-09 the notice barcodes: not in this slice.
- The data quality console SCR-45 and the quality measure definitions of the reporting module (Epic 2 and Epic 8); this story only writes the rows those surfaces read.
- The rwb-reporting model - its measure definitions, snapshots, steering dashboard and 07:30 refresh, and whether it reads the quality facts of this service or receives a quality event in wave 2 (GAP-2972; ASM-3163).
- Any data lake, lake copy, INT-19 adapter or INT-20 extract: removed under DP-17, so none is built, migrated, provisioned or tested here.
- The platform job monitor and its alerting beyond the read-only SCR-44 answer of this run, and the deployment, Schedule registration, dashboards, alerts and runbook of this run: the platform observability epic and the OPS slice of this legacy key.
- Working a break to closure with an owner and a date: FEAT-RPT-09 full scope, Epic 2.
