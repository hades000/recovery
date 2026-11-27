# RWB-P3-E1013-APP Baseline measures

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1013-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | To be sized by the squad at refinement (DOR-RWB-P3-E1013-APP-16) |
| Patterns applied | DP01, DP03, DP05, DP07, DP10, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | L-P3-E |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P9-E1013-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (no FR mapped to REQ-RDF-012) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the rwb-case slice of RWB-E1-013, split from the legacy reporting story. The case facts that every baseline measure is computed from stay with the case service and are read over a REST contract instead of an in-process interface, banded by the reference version in force on the business date; the release of a business date is recorded once in the decision record; the INT-19 lake extract, its freshness stamp and trailer and the hold path of MSG-GEN-006 are removed (DP-17), and the measure definitions, the snapshot, the baseline flag and the Power BI data set are rwb-reporting's. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P3-E1013-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (24 resolved, 35 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Reporting and BI analyst (RW-BIANAL) and the Tribe lead (RW-TRIBE)**, I want **the case facts of a business date read once from `rwb-case` - one row per case with its product group, route, stage, queue, entry date, stage clock start, closed date and status, banded by the reference version in force on that date - so that the baseline measures are counted from the same Workbench records for every team**, so that **no measure is computed from a separate count or a copy of case data, and every later epic is measured against one baseline**.

Inside `rwb-case` this is the case-facts capability of the case service: schema `rwb_case`, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1` with event names `rwb.case.<Event>.v1`, Temporal task queue `rwb-case` in namespace `rwb-recovery`, and the Java package `th.co.scb.ace.workbench.recovery.case`, whose trailing package segment `case` is a Java reserved word so that the package does not compile as written; the replacement segment ruled by the solution architect is Not specified in the source documents (CG-ALL-3419).

- The read answers the facts of one business date, paged, with the as-of time and the reference version it used. The facts are rows of `rwb_case` only: `recovery_case` joined to `queue` and to the rows of the age-band list in force (DP-01, DP-07).
- The band is resolved by the reference version in force on that business date, so the case list, the report and any later consumer band a case the same way.
- The release of a business date is a decision of this service, recorded once in the local decision record and published on `rwb.decision-record.v1` for the central ledger (DP-03): the decision-log half of the FSD P9 measure "measures read from the decision log and Workbench records, 100 percent".
- Nothing leaves as a file: with no data lake in Arch v5, the INT-19 extract, its freshness stamp and trailer and the hold path of MSG-GEN-006 have no counterpart here (DP-17).

The legacy facts are unchanged: the same nine fact fields, the same five age bands, and the same rule that measures are computed from Workbench records under a definition in force and never from a separate count.

### 2. Business rationale

Measures are counted by hand from spreadsheets at month end today, and each team counts a case differently. Legacy RWB-E1-013 answered this in one module: the definitions, the case and payment facts, the snapshot, the frozen baseline and the nightly lake extract sat together. In the target the case facts belong to the case service, the payments to the source-data service and the definitions, snapshot and baseline to reporting, so the legacy story splits. This story holds the case half:

1. **One source of case facts.** The measures count cases by route, age, queue, time in stage and turnaround, and every one of them is a column of a case record that only the case service may read (DP-01). Reporting reads them over one contract, once, for one business date (DP-11), so the counts cannot drift from the case list.
2. **One banding.** Age bands are a reference list (legacy BR6). If the report bands age from its own constants while the case list uses the list in force, the two disagree the day a band changes; so the band and its version travel with each fact (DP-07).
3. **No lake, no file.** The lake extract of the case facts is removed (DP-17, ADR-018): reporting builds its snapshot in its own projection from this read, and the freshness and the hold are its concern. Nothing is dropped on a floor here and no file is written.

It serves REQ-RDF-012, NFR-065, REC-01 and principle 1 (definitions are data). The measure definitions, the six measures, the snapshot, the baseline flag and the Power BI data set are RWB-P9-E1013-APP; the payments since entry and the completeness gate are RWB-P1-E1013-APP; the cross-service proof is RWB-ITG-E1013-ITG.

### 3. Preconditions

- The `rwb_case` baseline is in place from the service-template work: schema, login, base `/api/recovery/case/v1`, topic `rwb.case.events.v1`, task queue `rwb-case`, deployment chart and the decision-record table with its outbox (DP-01, DP-03, DP-13).
- The decision-record library is platform work (RWB-PLT-E1027-CON, DP-03) and is in the baseline: this slice calls it and adds no build dependency of its own.
- RWB-P3-E1043-APP is done: the age-band list is a versioned reference table in `rwb_case` with its rows, effective dates and approval, and the list read on `/admin/lists/{listCode}` is published. The list and table codes are Not specified in the source documents (GAP-2241; ASM-3697).
- RWB-P9-E1013-CON is published with its fake: the catalog of definitions in force, so a band list version cannot retire a band a definition still uses (DP-11). That read's path and shape are Not specified in the source documents (GAP-2240; ASM-3696).
- The reference rows in force on 2026-11-27 carry the five bands of the Background of section 7, with the effective dates of their version.
- The synthetic facts the tests use: business date 2026-11-27; 120 open cases - 60 Mortgage, 45 Hire purchase and 15 SSME - each with an entry date, a stage clock start, a queue and a status; a case list count of 120 at the same as-of time (legacy Background and AC2).
- The path, the query parameters and the response field names of the facts operation are Not specified in the source documents (GAP-2239; ASM-3695): the monolith offered a Java interface only.
- Readers hold Reporting R and Reporting and BI hold Reporting CRUD (legacy section 10); the authorisation decision is the cached permission decision the service template holds from `rwb-access`, and this story adds no guard of its own.

### 4. Flow

1. The 01:30 run of the previous business date is `rwb-reporting`'s: its JOB-15 reads this contract. The legacy Quartz job has no counterpart here and this service holds no job and no Schedule (DP-10).
2. `CaseFactController` receives the read for business date 2026-11-27 with the page and size of the standard query and checks Reporting R from the cached permission decision.
3. `AgeBandResolver` resolves the version of the age-band table in force on 2026-11-27 - the version whose effective range contains that date (DF-REF-163, DF-REF-164) - and its version number travels with the answer.
4. `CaseFactQuery` reads, in one REPEATABLE READ transaction, one row per case of the date: case ID, product group, route, stage, queue code, entry date, stage clock start, closed date and status, from `recovery_case` joined to `queue` inside `rwb_case` (AC1).
5. `AgeBandResolver` bands each case from its entry date and the rows of that version and writes the band code of the row on the fact; band values are rows, never constants (AC2).
6. `FactsReconciliationCheck` counts the facts and compares them with the case list count of the same date at the same as-of time inside the same transaction. Equal counts release the answer; a difference holds the release and lists the case behind it for the data steward (AC7).
7. `FactsReleaseRecorder` writes one local decision record for the date - decision code, business date, row count, reference version and as-of time, and nothing of a case - and publishes DecisionRecorded on `rwb.decision-record.v1` in the same transaction (DP-03, AC3). A repeat of the read writes no second record.
8. The answer carries the facts, the business date, the as-of time, the reference version and the row count. No file, no freshness stamp, no trailer and no lake call; `rwb-reporting` computes each of the six measures under its definition in force and writes its own snapshot (DP-17, AC4, AC5).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The caller's role holds no Reporting R | 403; no fact, no count and no as-of time is returned | MSG-P4-002 | AC6 |
| X2 | A caller posts a measure definition load to the reference-load path of this service | Refused; no definition row is written in `rwb_case`, and the definitions stay with rwb-reporting | MSG-P4-002 | AC6 |
| X3 | The facts count of the business date differs from the case list count at the same as-of time | The release of that business date is held, the case behind the difference is listed for the data steward, and no answer is released from the held read | The held-release message is Not specified in the source documents (GAP-2242; ASM-3698) | AC7 |
| X4 | The business date has no case | 200 with an empty page, the business date, the as-of time and the reference version; no decision record is written | None | AC8 |
| X5 | The reference version in force on the business date is not found, or the store cannot be read | 503 with the problem envelope of the service template; no fact and no band code is invented and no count of zero is returned | None | AC2, AC7, AC11 |
| X6 | The same business date is read twice | The facts are answered again; the decision record and the DecisionRecorded of the date are unchanged | None | AC3 |

Two target-service paths: the facts and the case list count are read in one transaction, so a difference is a real difference and not a page boundary; and a band list version is loaded through the reference-load path of RWB-P3-E1043-APP only, never through this read.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the reference-data tables, the decision-record library and the rwb-reporting contract fake (RWB-P9-E1013-CON); no screen and no other service at run time beyond the catalog read |
| Negotiable | Nothing business is fixed in code: the band values, their version and the case values are data |
| Valuable | One source of case facts and one banding for every later measure and epic |
| Estimable | One read, one resolver, one reconciliation check, one record write |
| Small | Fits one sprint with its tests, as a secondary slice of the legacy key |
| Testable | Every criterion in section 7 is one automated test over the synthetic 120-case set of the legacy story |

### 7. Acceptance criteria

```gherkin
Feature: Baseline measures - the case facts of rwb-case

  Background:
    Given the synthetic case set for business date 2026-11-27 holds 120 open cases: 60 Mortgage, 45 Hire purchase and 15 SSME
    Given age bands are "0-90", "91-180", "181-365", "366-730" and "over 730" days since entry

  Scenario: AC1 One fact per case for the business date (new, D-RCV-60)
    Given the 120 open cases of business date 2026-11-27 are rows of recovery_case in rwb_case
    When the reporting reader calls GET /api/recovery/case/v1/cases/facts with business date 2026-11-27 and page size 200
    Then the answer holds 120 facts, one per case, and no case appears twice
    Then every fact carries the case ID, the product group, the route code, the stage code, the queue code, the entry date, the stage clock start, the closed date and the status
    Then the product groups count to 60 Mortgage, 45 Hire purchase and 15 SSME, and the three counts add to 120
    Then no fact carries a party name, an identity number, an account number, a payment amount or a document reference

  Scenario: AC2 The band and its version come from the reference rows in force on the business date (new, D-RCV-60)
    Given the age-band reference table holds the five bands of the Background in a version whose effective range contains 2026-11-27
    When the facts of 2026-11-27 are read
    Then every fact carries a band code that is the code of exactly one row of the version in force on 2026-11-27
    Then the five bands are the only band codes the facts carry and their counts add to 120
    Then the answer names the version number of the reference version in force on that date
    When a later version of the list is loaded with a later effective date and the facts of a later business date are read
    Then the facts of 2026-11-27 keep the codes of the version in force on that date and the later facts carry the codes of the later version
    Then the band values and their boundaries are rows of the reference table and no band value is a constant in the Java of rwb-case

  Scenario: AC3 The release of a business date is recorded once in the decision record (new, D-RCV-60)
    Given the facts of 2026-11-27 have not been released
    When the reporting reader reads the facts of 2026-11-27 and the answer holds 120 facts
    Then one decision record is written for business date 2026-11-27 with the row count 120, the reference version and the as-of time
    Then one DecisionRecorded is published on topic "rwb.decision-record.v1" for that record
    When the same read is called again for 2026-11-27
    Then no second decision record and no second DecisionRecorded is written for that business date
    Then the record carries no case value other than the count, no party, no name and no amount

  Scenario: AC4 No extract, no freshness stamp and no data lake (new, D-RCV-60)
    Given the case facts are read by rwb-reporting and INT-19 is removed in Arch v5
    When the facts of 2026-11-27 are read
    Then the service writes no extract file, sets no freshness stamp and writes no trailer
    Then the artefact of rwb-case holds no lake client, no file writer and no outbound batch
    Then a request for a business date answers from rwb_case and depends on no outside system
    Then the legacy hold path and MSG-GEN-006 have no caller in this service

  Scenario: AC5 No measure definition, formula or value is published here (new, D-RCV-60)
    Given the six measures "CASES_BY_ROUTE", "CASES_BY_AGE", "CASES_BY_QUEUE", "REALIZED_RECOVERY", "TIME_IN_STAGE" and "TAT_BY_ROUTE" are definitions of rwb-reporting
    When the facts read answers for 2026-11-27
    Then the answer carries no measure code, no formula, no unit, no value, no approver and no approval date
    Then no table named measure_definition, measure_snapshot or measure_publish exists in schema rwb_case
    Then the baseline itself is read through the contract of RWB-P9-E1013-CON and this service holds no copy of it

  Scenario: AC6 A role without Reporting R is refused and a definition load is not accepted here (new, D-RCV-60)
    Given the role RW-BIANAL holds Reporting CRUD and the role RW-CASEOWN holds no right in the capability area Reporting
    When RW-CASEOWN reads the facts of 2026-11-27
    Then the read is refused with MSG-P4-002 and no fact, no count and no as-of time is returned
    When a caller posts a measure definition load to the reference-load path of rwb-case
    Then the load is refused with MSG-P4-002 and no definition row is written in rwb_case

  Scenario: AC7 The facts count equals the case list count at one as-of time (new, D-RCV-60)
    Given the case list of business date 2026-11-27 holds 120 cases at the as-of time of the read
    When the facts of 2026-11-27 are read
    Then the answer holds 120 facts and the counts are equal, and the facts and the case list are read in one transaction
    Then the as-of time of the answer is the as-of time of both reads
    When the facts count of a business date differs from its case list count
    Then the release of that business date is held, no answer is released from the held read, and the case behind the difference is listed for the data steward RW-DATASTEW with the business date

  Scenario: AC8 An empty business date answers an empty page and records nothing (new, D-RCV-60)
    Given a business date that has no case in recovery_case
    When the reporting reader calls GET /api/recovery/case/v1/cases/facts for that business date
    Then the answer is 200 with an empty page and carries the business date, the as-of time and the reference version
    Then no decision record and no DecisionRecorded is written for that business date

  Scenario: AC9 The facts read calls neither the completeness gate nor the payments of rwb-source-data (new, D-RCV-60)
    Given the completeness gate and the payments since entry of rwb-source-data are stubbed
    When the facts of 2026-11-27 are read
    Then the answer holds 120 facts and no call is made to the completeness gate or to the payments of rwb-source-data
    Then the gate and the payments stay with rwb-source-data and rwb-reporting joins them to these facts

  Scenario: AC10 The error answers of the provided operation are 401, 403 and 404 (new, D-RCV-60)
    Given the provided operation GET /api/recovery/case/v1/cases/facts
    When a caller calls it without a valid identity
    Then the answer is 401 with the problem envelope of the service template and no fact is returned
    When RW-CASEOWN calls it for business date 2026-11-27 without Reporting R
    Then the answer is 403 as in AC6
    When a caller calls a path of the service that is not defined
    Then the answer is 404 with the problem envelope of the service template

  Scenario: AC11 A consumed call that fails or does not answer releases nothing (new, D-RCV-60)
    Given the store of the reference version or the case store does not answer the read of business date 2026-11-27
    When the facts of 2026-11-27 are read
    Then the answer is 503 with the problem envelope of the service template
    Then no fact, no band code and no count of zero is returned and no decision record is written
```

The eleven criteria above are new and test only this deliverable: the case facts read, the band version, the release record, the removal of the lake path, the boundary against the measures, the empty business date, the error answers of the provided operation and the failed consumed call. The legacy criteria of RWB-E1-013 keep the assignment the integration slice already uses: AC1, AC4, AC5, AC7 and AC8 with rwb-reporting (RWB-P9-E1013-APP); AC2 and AC6 across services with RWB-ITG-E1013-ITG; the case facts with RWB-P3-E1013-APP; the readiness, the gate, the payments, the two events, the two activities and JOB-04 with RWB-P1-E1013-APP; and AC3 and AC7 recorded as removed by DP-17 rather than reassigned.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The case facts are read from the records of the case service, never from a separate count or a copy of case data | NFR-065; legacy BR3 |
| BR2 | A measure is published only under a definition in force that names its data product, formula, unit and approver; the definitions are rows of rwb-reporting and no definition, formula or value is held here | REQ-RDF-012; Principle 1; legacy BR1 |
| BR3 | Age bands are a reference list, and a case is banded by the version in force on the business date of the read | Legacy BR6; Principle 1 |
| BR4 | A measure is computed only from a complete ACE business date; the completeness gate and the payments since entry are rwb-source-data's and are read by rwb-reporting, not by this service | CTL-02; legacy BR4 |
| BR5 | The facts of a business date are released only when their count equals the case list count at one as-of time; a difference holds the release and is listed for the data steward, never rounded or noted | REC-01; legacy BR6 for the snapshot; DL25 |
| BR6 | The release of a business date is a decision of the case service and is recorded once, before the answer is released | Principle 5; legacy BR7 for the load; R-UNI-39 |
| BR7 | The band list version and the release are traceable: the answer names the version number, and the record names the business date and the row count | REQ-RDF-012; legacy BR2 |
| BR8 | There is no data lake and no file: the INT-19 extract, the freshness stamp, the trailer and the hold path are removed | DP-17; ADR-018; legacy BR5 |

How the rules hold in `rwb-case`:

- BR1 and BR5 are executed by `CaseFactQuery` and `FactsReconciliationCheck`: one transaction, one set of rows, and the case list count taken from the same table at the same as-of time.
- BR2 is executed by what is absent: no measure table, no definition column and no calculator exists here, and the read answers with facts only.
- BR3 and BR7 are executed by `AgeBandResolver`: the version comes from the effective dates of `reference_version`, its number is written into the answer, and no band boundary is typed in code.
- BR4 is a boundary: the gate and the payments are the source-data service's and reporting joins them to these facts; this service calls neither.
- BR6 is executed by `FactsReleaseRecorder` in the same transaction as the release: a record that cannot be written releases nothing.
- BR8 is executed by what is absent: no file writer, no lake client and no outbound batch exists in the service.
- DL25 is an open decision: BR5 holds a release on a count difference. Its assumptions are ASM-0728, ASM-0735, ASM-0743 and ASM-2602; the decision is still open, so no outcome is assumed here.

### 9. State transitions

None for the case. This story changes no case status, no stage and no clock. It sets the release state of a business date and it reads the reference version in force.

| Object | From | Event | To |
|---|---|---|---|
| release of a business date | not released | the facts count equals the case list count at one as-of time | released, with one decision record and one DecisionRecorded |
| release of a business date | not released | the facts count differs from the case list count | held, with the case listed for the data steward and no record released |
| release of a business date | released | the same business date is read again | unchanged; no second record and no second event |
| age-band list | version in force | a later version is loaded with a later effective date | the later version is in force from its effective date; the facts of earlier dates keep the earlier version |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-case service identity (the rwb-case login, DP-02) | Reads `recovery_case`, `queue` and the reference rows of its own schema, writes the decision record, and calls the catalog read of rwb-reporting; holds no grant on `rwb_reporting` and no file or lake access |
| RW-BIANAL, Reporting and BI analyst (Reporting CRUD) | Reads the facts of a business date and builds the Power BI data set from the snapshot of rwb-reporting |
| RW-TRIBE, Tribe lead and squad members (Reporting R) | Reads the baseline and the facts behind it; approves the definitions in rwb-reporting |
| RW-DATASTEW, data steward (Reporting CRU) | Receives a held release and the case behind the difference |
| RW-FINANCE, Finance and CFO delegate (Reporting R) | Reads the baseline |
| RW-CASEOWN, case owner (no right in Reporting) | Reads neither the facts nor the count; refused with MSG-P4-002 |
| RW-PLATADM, platform administrator (Platform administration U) | Reruns the 01:30 run of rwb-reporting; this service has no job to rerun |
| rwb-reporting (P9) | Owns the definitions, the measures, the snapshot, the baseline flag and the Power BI data set; reads these facts over the contract only |

The role codes are rows of the role model (legacy section 10) and are not fixed in code. The authorisation decision is the cached permission decision the service template's guard already holds; this story adds no guard, no endpoint of its own and no access entry. The read operation GET /api/recovery/case/v1/cases/facts is authorised by the rwb-access authorise check (DP-08) before any fact is built.

### 11. Data

| BR Field ID | Table in rwb_case | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | `recovery_case` | id | Read (the case ID on the fact) |
| DF-CAS-003 | `recovery_case` | product_group | Read (the product group on the fact) |
| DF-CAS-005 | `recovery_case` | status | Read |
| DF-CAS-006 | `recovery_case` | stage_code | Read |
| DF-CAS-008 | `recovery_case` | route_code | Read |
| DF-CAS-010 | `recovery_case` | queue_id | Read |
| DF-CAS-013 | `recovery_case` | entry_date | Read (the band is derived from it) |
| DF-CAS-018 | `recovery_case` | stage_clock_start | Read (time in stage) |
| DF-CAS-022 | `recovery_case` | closed_date | Read (turnaround) |
| DF-WRK-002 | `queue` | queue_code | Read (the queue code on the fact) |
| DF-REF-160, DF-REF-163, DF-REF-164 | `reference_version` | table_code, valid_from, valid_to | Read (the version in force on the business date) |
| DF-REF-183, DF-REF-184 | `reference_row` | row_key, row_data | Read (the band code of each row of that version) |
| DF-DEC-001 to DF-DEC-031 | decision-record table in `rwb_case` | the release record | Write (one record per business date) |
| (outbox) | outbox library table in `rwb_case` | the DecisionRecorded row | Write (published after the record commits) |

Field IDs are those in the Logical Data Model and Data Dictionary and in the reference-data story RWB-P3-E1043-APP. `case_account`, `case_party`, `assignment` and `timer` are not read by this story: the facts carry no account, no party, no owner and no timer. No table of another service is read (DP-01) and no `v_ace_*` view is read (DP-05). `measure_definition`, `measure_snapshot` and `measure_publish` are P9's; this service holds no grant on them and stores no measure.

### 12. Contract

The contract versions this story builds against are Not specified in the source documents (DOR-RWB-P3-E1013-APP-23); only the `/v1` base path is fixed.

#### 12.1 REST operations provided

| Method | Path | Status | Used for |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/facts` | Declared for this story; the path, the query parameters and the field names are Not specified in the source documents (GAP-2239; ASM-3695) | The facts of one business date: `businessDate`, `page`, `size`; the answer carries the items, the row count, the as-of time and the version number of the band list in force |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | Declared by the reference-data contract (RWB-P3-E1043-CON), owner P3 | The band rows of the version in force; the `listCode` of the age-band list is Not specified in the source documents (GAP-2241; ASM-3697) |

Both paths answer 401, 403 without Reporting R, 422 for a business date that cannot be read, and 503 when the store or the reference version cannot be read. This story adds no filter to the case list, the case record read or the export.

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | the measure-catalog read of the definitions in force, path Not specified in the source documents (GAP-2240; ASM-3696) | rwb-reporting (P9), under RWB-P9-E1013-CON | The definitions in force on the effective date of a band list version, so a version that retires a band a definition still uses is refused before it is in force | One hop, 2 s (DP-11) |
| GET | the payments since entry of rwb-source-data (legacy `RecoveryDataApi.paymentsSinceEntry`), path Not specified in the source documents (GAP-2567) | rwb-source-data (P1), under RWB-P1-E1013-APP | The payments of the business date that the 01:30 run of JOB-15 joins to these facts; consumed by rwb-reporting, not by this read | Not specified in the source documents (GAP-2567) |
| GET | the daily completeness gate of rwb-source-data (legacy `DailyCompletenessGate.check`), path Not specified in the source documents (GAP-2567) | rwb-source-data (P1), under RWB-P1-E1013-APP | The freshness answer for the business date that the 01:30 run of JOB-15 reads before the baseline is published; consumed by rwb-reporting, not by this read | Not specified in the source documents (GAP-2567) |

The contract is consumed as the published OpenAPI 3.1 document plus its fake, and the call is made on the reference-load path of RWB-P3-E1043-APP, not on this read. The two rwb-case rows of the plan are RWB-P3-E1043-CON, the age-band list of 12.1, and RWB-P3-E1018-CON, whose path and use are Not specified in the source documents (GAP-2567). No other service is called by this read: the payments since entry and the daily completeness gate are class C rows of the key that rwb-reporting reads in its 01:30 run, and this service calls neither.

#### 12.3 Events published

| Event | Topic | Key | Payload |
|---|---|---|---|
| DecisionRecorded (EV-08) | `rwb.decision-record.v1` | business date | the release record: decision code, business date, row count, reference version, as-of time, actor and the hash-chained entry |

CloudEvents 1.0 envelope, published after the record commits. This story adds no event to `rwb.case.events.v1`: the facts are served on request, not streamed, and no payload carries a case value, an amount or personal data.

No reporting event is declared. The Ownership Map gives rwb-reporting no event row and a service topic that is Not specified in the source documents (GAP-2569), while RWB-ITG-E1013-ITG names `rwb.reporting.ReportPublished.v1` on the same service topic as the freshness signal of its journey and cites this story as the publisher. The topic stays provisioned by the platform, this story publishes nothing on it, and the owner of the reporting read model decides whether a freshness event is published; if it is, that is raised as its own story with the outbox library row RWB-PLT-TE006-CON of DP-09, which is in no pattern set of this key (GAP-2569).

#### 12.4 Events consumed

None. This story consumes no event: the facts are read on the contract, and the completeness signal of a business date is rwb-reporting's to read.

#### 12.5 Workflows and activities

None. This story starts no workflow and runs no activity; the read is synchronous on the task queue's API deployment, and the case workflows of this service are untouched.

#### 12.6 Schedules

None. The Quartz trigger of JOB-15 is rwb-reporting's to replace with its own Temporal Schedule; this service holds no job, no Schedule and no Quartz table (DP-10).

One Schedule is registered for JOB-15, in rwb-reporting, at 01:30 Asia/Bangkok; no Airflow call is wired to that run, the bank's Airflow triggering no report extract of this story, and whether any extract trigger returns and what it calls is settled in the batch and scheduling work (GAP-2573). The 05:30 late check is a Temporal Schedule of rwb-source-data, and its workflows and activities need the rwb-source-data worker, the task queue, the namespace and the topic with its retry and `.dlt` topics registered: that registration stands in the platform workflow and operations stories of the epic, so it is an external or operations dependency of the plan and no build dependency of this slice (GAP-0561).

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `recovery_case` | P3 (rwb_case) | Read only: the nine fact fields per case of the business date |
| `queue` | P3 | Read only: the queue code of the fact |
| `reference_version`, `reference_row` | P3 | Read only: the band version in force and its rows |
| decision-record, outbox and inbox tables | PLT library, created in `rwb_case` | Written: one release record per business date |

`measure_definition`, `measure_snapshot` and `measure_publish` are P9's, `queue_measure` is P3's from RWB-P3-E1030-APP and is not touched here, and no `v_ace_*` view is read (DP-05).

No screen is built in this story, so SCR-37 and SCR-44 have no state here. The states of the facts read are: empty, X4 (200 with an empty page); no access, X1 (403, refused with MSG-P4-002); error, X5 (503 with the problem envelope of the service template). The service holds no loading state.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-reporting contract fake (RWB-P9-E1013-CON) | The measure catalog | Six definitions in force on 2026-11-21 with their data product and formula; a definition in force that names a band; a catalog that answers slowly past the 2 s budget |
| decision-record library fixture (RWB-PLT-E1027-CON) | The release record and the topic | The record of 2026-11-27, its repeat, and a record write forced to fail |
| reference-data fixture (RWB-P3-E1043-APP) | `reference_version` and `reference_row` | The version in force on 2026-11-27 with the five bands; a later version with a later effective date; a business date with no version in force |
| case fact fixture | `recovery_case` and `queue` | The 120 cases of 2026-11-27 - 60 Mortgage, 45 Hire purchase, 15 SSME - with entry dates across the five bands, stage clock starts, closed dates and a case list count of 120; a set of 119 against 120 for the held release; an empty business date |
| rwb-source-data contract fake (RWB-P1-E1013-APP) | The payments since entry and the daily completeness gate that the 01:30 run of JOB-15 reads | The payments of 2026-11-27 and a completeness answer that is fresh; a completeness answer that does not answer |

The field names inside the catalog read are stubbed from the published fixture of RWB-P9-E1013-CON; their list is Not specified in the source documents (GAP-2240; ASM-3696).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 1 consumed by this read, 2 more class C rows of the key | The facts read on `/api/recovery/case/v1/cases/facts` and the band list on `/admin/lists/{listCode}`; one hop to the rwb-reporting catalog within 2 s (DP-11); the payments since entry and the completeness gate of rwb-source-data are read by the JOB-15 run in rwb-reporting |
| Kafka | 1 published, 0 consumed | DecisionRecorded on `rwb.decision-record.v1`; nothing on `rwb.case.events.v1` |
| Temporal | None | No workflow, no activity and no Schedule in this story (DP-10) |
| File | None | No extract, no freshness stamp and no trailer; the lake path is removed (DP-17) |

### 13. Solution plan

**Package.** Module `case/facts`. The Java packages `th.co.scb.ace.workbench.recovery.case` and `th.co.scb.ace.workbench.recovery.case.facts` carry `case`, a Java reserved word, as their last package segment and do not compile as written; the replacement segment ruled by the solution architect is Not specified in the source documents (CG-ALL-3419; CG-ALL-3420).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseFactController | Controller | Reporting R, paging, the problem envelope, the as-of time and the row count |
| CaseFactQuery | Service | One row per case of the business date in one REPEATABLE READ transaction, from `recovery_case` and `queue` only |
| AgeBandResolver | Service | The version of the band list in force on the date, and the band code of its row on each fact |
| FactsReconciliationCheck | Service | Counts the facts, compares with the case list count at the same as-of time, releases or holds |
| FactsReleaseRecorder | Service | The release record and its outbox row in the same transaction, once per business date |
| MeasureCatalogClient | REST client | The rwb-reporting catalog on the reference-load path, one hop and 2 s (DP-11); refuses a version a definition still uses |
| CaseFactRepository | Repository | `recovery_case`, `queue`, `reference_version`, `reference_row`; no foreign table |

**Database and migrations**

- Writes the decision-record and outbox rows only; no case column and no measure column is added.
- Migration in this story, in the per-service Flyway sequence of DP-15 (`V0001` to `Vnnnn`, owned by the service): the facts-read migration, whose next free number and file name are Not specified in the source documents (CG-ALL-3421), adds the covering index on `recovery_case (entry_date, product_group, route_code, stage_code, queue_id, closed_date)` for the facts read and the index on `reference_version (table_code, valid_from, valid_to)` for the version lookup. It creates no table and adds no column.
- No row is seeded here: the cases are the case stories' data and the bands are the reference-data story's.

**Configuration and reference data**

- No business value: the bands, their boundaries and their version are reference rows; the product groups, routes, stages and queues are case data.
- Two settings only: the rwb-reporting catalog base and the rwb-case login (DP-02); the 2 s timeout and the one-hop rule are the platform values of DP-11.
- Feature flag `rwb.p3.case-facts`. Off: the read answers 503 and no release record is written. No tolerance is configured for the count comparison: the difference must be zero.

**Build steps**

1. `CaseFactQuery` and the covering index over the 120-case set of 2026-11-27; tests for AC1 and AC7.
2. `AgeBandResolver` against the reference-data fixture, with the version in force and a later version; test for AC2.
3. `FactsReconciliationCheck` with the equal and the different count, in one transaction; test for AC7.
4. `FactsReleaseRecorder` with the record, the outbox row and the repeat; test for AC3.
5. The boundary: no measure table, no measure field in the answer and no definition load accepted; tests for AC5 and AC6.
6. The removal check on the artefact: no lake client, no file writer, no freshness stamp and no trailer; test for AC4.
7. `MeasureCatalogClient` against the rwb-reporting fake with the found, the slow and the failed answer; contract test TC-E1-013-01.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

This secondary slice owns no legacy acceptance criterion of a build story, so it adds no new build dependency (metadata "Depends on (build)" = None) and builds on the `rwb_case` baseline. Read one by one:

- DP-01, DP-13 and DP-15 are the target shape itself: the facts of `rwb_case`, the base `/api/recovery/case/v1` and the facts-read migration of the service's own `Vnnnn` sequence, with no new dependency.
- DP-03 is live: the release record and the DecisionRecorded come from the platform library, and the ledger entry is rwb-decision's.
- DP-05 is a boundary: no ACE value, no `v_ace_*` view and no `account_ext` field is read; the payments and the gate stay with rwb-source-data for reporting to join.
- DP-07 is live: the band list is a versioned reference table of this service, read in force on the date; its load stays RWB-P3-E1043-APP's.
- DP-10 is a prohibition: no Quartz table, no job and no Schedule here; the 01:30 run is rwb-reporting's Schedule over this read (GAP-2573), and the worker, the task queue and the namespace of rwb-source-data are registered by the platform workflow and operations stories as an operations dependency of the plan, not a build dependency of this slice (GAP-0561).
- DP-11 is live twice: the legacy in-process `CaseReportingApi.caseFacts` becomes this contract with its fake, and one hop away the catalog is called as a contract, never as a table.
- DP-17 is a removal: the INT-19 extract, the freshness stamp, the trailer, the hold and MSG-GEN-006 are gone and no file replaces them.
- DP-19 covers where a held release is seen: SCR-44 through the gateway-bff composite route, which is not this story's.

**Done when.** The tests in section 16 pass, SIT answers the 120 facts of 2026-11-27 with the five band codes of the version in force, the count equals the case list count, one release record exists for that date and a repeat writes none, a difference of one holds the release and lists the case, and the artefact holds no file writer, no lake client and no measure table.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | The caller's role holds no Reporting R, or a measure definition load is posted here | You cannot {action} here. Your role does not include it. |
| The held-release message, whose ID and wording are Not specified in the source documents (GAP-2242; ASM-3698) | The facts count of a business date differs from its case list count | The facts of {date} were not released: {count}. |
| MSG-GEN-006 | No caller in this service | {system} is not available. Your request is queued and will be retried. |
| MSG-P1-001 | No caller in this service: the ACE batch gate is rwb-source-data's and rwb-reporting's | {product} is from {date}. Today's load has not arrived. |
| MSG-P9-003 | No caller in this service: a measure without a definition in force is rwb-reporting's | {measure} has no approved definition. It is not published. |

Every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. MSG-GEN-006, MSG-P1-001 and MSG-P9-003 are listed so that the reader sees where the legacy messages went: the lake hold is removed with DP-17, and the gate and the definition checks are rwb-reporting's.

### 15. Screens and states

No new screen. The facts are read by a service, not by a person: the Reporting and BI analyst sees them only through the snapshot and the Power BI data set of rwb-reporting, and the Tribe lead reads the baseline there.

States this story makes visible: the release state of a business date (released, held) with its row count and the case behind a held release, on SCR-44 Interface and job monitor, and on the data steward's break list. Both are served through the gateway-bff composite route (DP-19), which calls this service; the route, its masking and its specification are Not specified in the source documents (GAP-2242; ASM-3698). SCR-37 Steering dashboard and its data set come in RWB-P3-E2009-APP. For SCR-37, empty, error and no access are Not specified in the source documents (CG-ALL-3422). For SCR-44, empty, loading, error and no access are Not specified in the source documents (CG-ALL-3423).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-013-01 | AC1, BR2, BR3: the definitions stay with rwb-reporting and the band version of a definition in force is checked against its catalog | Contract | Six definitions in force on 2026-11-21 with a data product and a formula; a band list version that retires a band they use; the rwb-reporting fake |
| TC-E1-013-02 | AC2, BR1: one fact per case and the count equal to the case list at one as-of time | Integration | 120 cases on 2026-11-27 - 60 Mortgage, 45 Hire purchase, 15 SSME; an empty business date for the empty page |
| TC-E1-013-03 | AC3, BR8: no extract, no freshness stamp, no trailer and no lake client remain | Component | The 2026-11-27 read; a scan of the artefact for a file writer, a lake client and an outbound batch |
| TC-E1-013-04 | AC4, BR2: a measure definition load is not accepted here and is refused with MSG-P4-002 | Contract | A definition load posted to the reference-load path of rwb-case; no row in `rwb_case` |
| TC-E1-013-05 | AC5, BR6, BR7: the release of a business date is recorded once and a repeat writes no second record | Integration | The 2026-11-27 read twice; one decision record and one DecisionRecorded for the date |
| TC-E1-013-06 | AC6, BR5: a business date that does not reconcile is not released; the case behind the difference is listed | Component | A case list count of 120 against 119 facts for 2026-11-27; the held release and the listed case |
| TC-E1-013-07 | AC7, BR8: the legacy lake-unavailable path has no caller, because no lake is called | Component | The read with the lake load area stubbed unavailable; the same 120 facts answered, no hold and no MSG-GEN-006 |
| TC-E1-013-08 | AC8, BR2: no measure code, value, formula or approver is returned by the facts read | Contract | The 2026-11-27 answer; no `measureCode`, no `value` and no approver field in the response schema |
| TC-E1-013-09 | AC6, BR6: a role without Reporting R reads neither the facts nor the count; refused with MSG-P4-002 | Component | RW-BIANAL reads the facts; RW-CASEOWN is refused with MSG-P4-002 |
| TC-E1-013-10 | AC1, BR1, BR8: boundary of the tables of section 12.7 (ASM-3438); the facts read writes only the decision record | Component | The 2026-11-27 read with a write probe on `recovery_case`, `queue`, `reference_version` and `reference_row`; one decision-record row written and no other row |
| TC-E1-013-11 | AC8: an empty business date answers an empty page and writes no record | Integration | A business date with no case; the reference version in force; the empty answer and the absent decision record |
| TC-E1-013-12 | AC9, BR4: the facts read calls neither the completeness gate nor the payments of rwb-source-data | Component | The 2026-11-27 read with the gate and the payments stubbed; no call to either |
| TC-E1-013-13 | AC10: the provided operation answers 401, 403 and 404 with the problem envelope of the service template | Contract | Not specified in the source documents (NEWAC-RWB-P3-E1013-APP-AC11) |
| TC-E1-013-14 | AC11: a consumed call that fails or does not answer answers 503 and releases nothing | Component | The 2026-11-27 read with the reference version store stubbed unavailable; no fact, no band code and no decision record |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The legacy level System is answered here at Integration or Component for the slice this story owns, Access at Component and Contract for the definition boundary; no -ITG copy of these cases sits here: they belong to RWB-ITG-E1013-ITG, which proves the same values across rwb-case, rwb-source-data and rwb-reporting end to end.

### 17. Guardrails

- No business value in code: the bands and their boundaries are reference rows, the products, routes, stages and queues are case data, and the measures and their formulas are rwb-reporting's. No band, no product group and no count threshold appears in this service's Java.
- No personal data in the answer, the release record, the logs or the tests: the facts carry a case ID, a product group, codes and dates only - no name, address, identity number, account number or amount.
- No cross-schema read (DP-01) and no ACE view (DP-05): `rwb_case` reads no `rwb_reporting` or `rwb_source_data` table and no `v_ace_*` view; the ACE data behind a case reaches reporting through rwb-source-data's contract.
- No file and no external call (DP-17): the INT-19 extract, its freshness stamp and its trailer are removed and no replacement path exists.
- One hop, 2 s, to the rwb-reporting catalog, and a failed or slow answer refuses the band version instead of loading it (DP-11).
- The facts and the case list count are read in one transaction, so a difference is a real difference and never a page boundary.
- The release record is written in the same transaction as the release: a date whose record cannot be written is not released.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-012 | Baseline measures published with definitions agreed by the Tribe | Business Requirements Epic 1, sections 3.8 and 4 | FEAT-RDF-19, FEAT-RPT-01 | 15 Manage performance, data and AI | None; control CTL-02 applies | TC-E1-013-01 to TC-E1-013-12 |

REQ-RDF-012 is answered here only for the case facts and their banding; the definitions, the six measures, the snapshot and the frozen baseline are RWB-P9-E1013-APP, the payments and the completeness gate are RWB-P1-E1013-APP, and the -ITG copy of the test cases is carried by RWB-ITG-E1013-ITG.

| Legacy reference | Where it is kept |
|---|---|
| The nine fact fields of `CaseReportingApi.caseFacts` | Sections 1, 4, 11, 12.1 |
| The five age bands and their list | Sections 7 (Background, AC2), 8 (BR3), 12.1, 12.7 |
| The six measure codes and their definitions | Sections 7 (AC5), 8 (BR2), 12.2, 19 |
| The frozen baseline, the baseline flag and the snapshot | Section 19 (rwb-reporting) |
| JOB-15 Reporting extract at 01:30 | Sections 4, 12.6 (rwb-reporting's Schedule) |
| INT-19 extract, freshness stamp, trailer and MSG-GEN-006 | Sections 5 (X3 note), 8 (BR8), 14, 17 |
| MSG-P4-002, and MSG-GEN-001 with the definition load | Sections 5, 10, 14 |
| Legacy key RWB-E1-013, contract RWB-P9-E1013-CON | Metadata, sections 2, 3, 12 |

### 19. Out of scope

- The measure definitions, the six measures, the snapshot, the baseline flag and the frozen-row protection (RWB-P9-E1013-APP).
- The payments since entry, the daily completeness gate and the freshness stamp (RWB-P1-E1013-APP, RWB-P1-E1015-APP).
- The Power BI data set, the report layout and SCR-37 Steering dashboard (RWB-P3-E2009-APP for the case-side data set; the report itself is RW-BIANAL's).
- The JOB-15 Schedule, its chart and its runbook (RWB-P9-E1013-OPS) and the deployment of this service (its OPS story).
- The age-band reference table, its load, its approval and its rollback (RWB-P3-E1043-APP) and the band list screen (RW-REFADM's administration screens).
- Queue and ageing measures for team managers (FEAT-RPT-02, RWB-P3-E1030-APP) and benefit realisation tracking against the baseline (FEAT-RPT-06, Epic 6): the benefit-model measure set and where its membership is held, the business day and cut-off of the monthly step, the month key in `measure_snapshot`, the screen that carries the benefit view and the requirement ID the legacy key traces to are Not specified in the source documents (GAP-2579).
- The cross-service proof of the facts, the payments and the measures (RWB-ITG-E1013-ITG).
- The data lake copy of the decision log (RWB-E1-014, retired) and any INT-19 or INT-20 path (removed, DP-17).
