# RWB-P3-E1011-APP Reconciliation and data quality report

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1011-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-011 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP05, DP06, DP07, DP10, DP11, DP14, DP15, DP17, DP19 |
| Parallel lane | L-P3-D |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-004, FR-P3-019, FR-P3-021) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: RWB-E1-011 is split and reworked as the rwb-case APP story RWB-P3-E1011-APP, the case, queue and assignment slice of the daily reconciliation and its data quality report: the exclusions recorded at entry, every account key and person key on a case table and every queue and owner reference of an open case are reconciled against the data products this service reads through the rwb-source-data contract, and the case-side facts are served to the reconciliation and to the report through this service's own operations; the enterprise case-list run, `reconciliation_result` and the case-list publish stay with rwb-source-data, and the two data-lake extracts are removed. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P3-E1011-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **data steward and data product owner (RW-DATASTEW)**, I want **a daily quality run in rwb-case that reconciles the exclusion rows recorded at entry, every account key and person key on the case tables and every queue and owner reference of an open case for the business date, computes the variance against the tolerance in force, writes one result per check and product group, lists every row or key that breaks, and serves the case, queue and assignment facts of the date through this service's own operations**, so that **everyone sees whether the case side of today's case list and its links can be trusted, and the reconciliation of the date reads the exclusions of the case side from the owner of the rows rather than from a copy**.

The legacy story built one batch step, JOB-04 Daily reconciliation, that ran five checks REC-01 to REC-05 for the business date of the ACE batch, wrote one `reconciliation_result` row per check and product group, held or released the case-list publish, and pushed two CSV extracts to the data lake for a Power BI report. D-RCV-60 keeps the control and splits the ownership along the service boundaries of Architecture v5:

- The enterprise case-list reconciliation - the account count and the balance by product against the ACE account rows, the treatment and payment checks, every business key on the data engine's own tables, the `reconciliation_result` rows and the case-list publish status - becomes `ReconciliationWorkflow` in rwb-source-data (RWB-P1-E1011-APP), which owns `reconciliation_result` and `case_list_row` (Ownership Map; Architecture v5 slide 15 gives P1 the reconciliation and slide 44 gives it JOB-04).
- This story is the case and workflow slice and owns the facts rwb-case holds: the exclusions recorded at entry in `case_entry_exclusion`, the account keys of `case_account`, the person keys of `case_party` and of `recovery_case.primary_person_key`, and the queue and owner references of an open case in `recovery_case`, `queue`, `queue_member` and `assignment`. It runs the case side of REC-01 as FSD P3 v4 applies the exclusions to this module (FSD P3 v4 line 157, "a business key with no ACE row is listed by REC-05"), the case side of REC-05 (FSD P1 v3 A2.11, "business key, count and amount"), and the reference check the FSD P3 names "References" (FSD P3 v4 AC-EXC-P3-035-01).
- No `recovery.v_ace_*` view is read by this service: Architecture v5 slides 29, 37 and 45 give the 30 views to rwb-source-data alone, so the ACE side of every check arrives as data-product rows through that contract (DP-05, DP-11).
- The asset slice is RWB-S5-E1011-APP, the notice slice is RWB-P6-E1011-APP, the deployment slice is RWB-P1-E1011-OPS and the end-to-end proof of the whole of JOB-04 is RWB-ITG-E1011-ITG.

The legacy published interface is kept as an operation of this service rather than as an in-process call: the legacy story exposed `excludedAccountsByProduct(businessDate)` from P3 to the case-list step of RWB-E1-002, and the target serves the same facts on `GET /reconciliation-facts/{businessDate}` of this base (12.1), one hop, so no reader of the reconciliation reaches a `rwb_case` table (DP-01, DP-11).

The target also removes what the legacy story relied on. The data lake is gone (DP-17, ADR-018), so the reconciliation extract and the data quality extract that the legacy publish step wrote through INT-19 have no target, and the measures come to rwb-reporting from the business events and the read models of the services; this story therefore writes no extract file and no lake path (GAP-0740; ASM-1346). Every legacy report value that only the lake held - the two CSV extracts, the lake path of the date, the previous released lake date and the 07:30 Power BI data set - has no target and is answered by the reads of 12.1 instead (GAP-0740; ASM-1347).

This secondary slice owns no legacy acceptance criterion: the eight criteria of RWB-E1-011 are carried by RWB-P1-E1011-APP (AC5, AC6 and AC8) and by RWB-ITG-E1011-ITG (AC1, AC2, AC3, AC4 and AC7), and the nine legacy test case IDs of the key are kept here against this slice's own assertions, so the values the legacy story fixed are proved on the case side as well as on the enterprise run (GAP-0740; ASM-1352).

The slice writes no case, queue, assignment or exclusion row: it reads those rows, writes the state of its own run and its own result and break rows in `rwb_case`, publishes no event, holds no foreign key to another service and starts one workflow from one Schedule (DP-01, DP-10).

### 2. Business rationale

No one can say today whether the recovery teams' lists cover every account at 90 days past due, so missing accounts are found late or not at all. The legacy capability answered that question once a day for the whole Workbench: the account count and the balance by product, the treatments and the payments, and every business key on every Workbench table, with the breaks listed and the case list held when a product was outside its tolerance. In `rwb-case` the same idea is applied to the facts this service owns, because they are the facts the reconciliation cannot see for itself: the exclusions that explain a difference at entry, the account and person keys that must resolve to an ACE row, and the queue and owner references that decide who is answerable for a case.

Every business date the quality run compares three things. The exclusion rows of the date are checked for completeness - a row with no reason code, no rule ID or no rule version cannot explain anything - and the exclusion facts served for the date are compared with the rows behind them, so a served count can never disagree with the rows it stands for (BR1, BR2). Every account key on `case_account`, every person key on `case_party` and every primary person key on `recovery_case` is resolved against the account and customer data products read through the rwb-source-data contract, and every orphan is listed (BR3). Every open case must carry a queue in force, and every owner it carries must be a member of that queue on the date, because an owner outside the queue is an assignment the allocation story cannot explain (BR4).

It serves the FSD P1 measures that belong to this service's rows - referential completeness "every business key on a Workbench table resolves to a v_ace_* row, 100 percent" and validity "codes in their lists" (FSD P1 v3 A2.12) - and the control CTL-01 and the rule R-UNI-40 of the legacy key. It meets REQ-RDF-007 (the case list reconciles daily to the count in `v_ace_account` with no variance, and every business key resolves to an ACE row), REQ-RDF-008 (reconciliation breaks and referential completeness are reported to the data product owner) and REQ-CWC-004 (the exclusion rules are held as data and applied at creation).

Three edges of the legacy capability are no longer this service's to reach. The account count and the balance by product, the treatment and payment checks, the `reconciliation_result` rows and the case-list publish are rwb-source-data's; the asset keys are rwb-asset's; the notice keys are rwb-comms's; the end-to-end proof is the integration story's. What is left, and what this story owns, is the case side: what was excluded and why, which keys lead nowhere, and whether the queue and owner of a case are facts another service can act on.

The tolerance and the lists are data, never code. The parameter `recon.tolerance.pct` comes through the parameters contract of this service with the version in force (DP-06), and the product groups, the exclusion reasons, the queue codes, the result values and the run states come through its reference-data contract (DP-07); neither contract is in this story's Contract dependencies, which the plan sets to None, so both are read in process against the rows of this service and are faked where a test needs another version (GAP-0740; ASM-1344). The run is a Temporal Schedule plus a workflow in this service (DP-10), the tables live in `rwb_case` (DP-01, DP-15), the run record, the facts and the break rows are reached through the gateway-bff composite route (DP-19), and the topic name of the service comes from the naming library although this story publishes no event (DP-14).

The right of the two quality reads and of the facts read is the legacy one: Platform administration R for the data steward, the platform administrator and the readers of the break rows, and the rwb-source-data service identity for the exclusion and key facts of its own reconciliation run (BR13). TSD P3 v3 declares the Platform administration capability area for the workflow smoke operation (API-P3-027) but no right for a quality read, so the legacy story comes first in the fill order of Template and Rules §R7.3 and the right is kept (GAP-0740; ASM-1350).

### 3. Preconditions

- RWB-P3-E1018-APP is done: `recovery_case`, `case_account` and `case_party` exist in `rwb_case` with the case number, the product group, the queue, the owner, the status, the entry date, the primary person key and the account and party links, and case creation writes them. Those rows are this story's source facts.
- The exclusion rules are applied at case creation: `case_entry_exclusion` carries one row per account kept out of recovery on a business date, with its reason code, its rule ID and its rule version (TSD P3 v3 T3.1, DF-CAS-056 to DF-CAS-061). This story reads those rows and writes none.
- RWB-P3-E1019-APP is done: `queue` carries the queue code, the team and the role, and `queue_member` carries the membership of a user in a queue by version (DF-WRK-045 to DF-WRK-052). This story reads both.
- RWB-P3-E1020-APP is done: an open case carries its queue and its owner, and `assignment` records who holds it and from when (DF-WRK-009 to DF-WRK-016). This story reads the open assignment and writes none.
- The per-service Flyway sequence of rwb-case carries the migration of 11, after the case baseline of the case stories (DP-15; RWB-PLT-E1044-CON).
- The platform libraries are in place: the decision-record library (RWB-PLT-E1027-CON, DP-03), the parameters client (RWB-PLT-E1042-CON, DP-06), the reference-data client (RWB-PLT-E1043-CON, DP-07), the workflow kit with Schedules (RWB-PLT-E1071-CON, DP-10), the per-service Flyway sequence (RWB-PLT-E1044-CON, DP-15), the naming library (RWB-PLT-E1047-CON, DP-14) and the gateway-bff composite route (RWB-PLT-N001-CON, DP-19). None of them is in this story's Depends on (build) list, which the plan sets to None; they arrive through the platform release train of wave 0 and are assumed present before the wave-1 build (GAP-0740; ASM-1343).
- RWB-P3-E1042-CON and RWB-P3-E1043-CON are published with their client libraries, and in this service they read its own `parameter_catalog`, `parameter_value`, `reference_row` and `reference_version` rows, so no cross-service call is made for a parameter or a list value (DP-06, DP-07). Neither contract is in this story's Contract dependencies, which the plan sets to None (GAP-0740; ASM-1344).
- The rwb-source-data contract answers the freshness of a data product and the rows of DP01 Account and arrears and DP02 Customer and party for a business date, one hop with a 2 s timeout (DP-11, ADR-020). The element names behind the two operations are Not specified in the source documents (GAP-0740; ASM-1349); the contract is not in this story's Contract dependencies, so it is faked from the published document (GAP-0740; ASM-1344).
- The parameter `recon.tolerance.pct` is 0.00 in force for the REC-01 EXCL check on the business date, the legacy value under DL25; its owner is the centre-of-excellence analyst and a change needs the reference-data change process. The REC-05 KEY and REC-05 REF checks have no percent tolerance: their tolerance is zero orphans and zero unresolved references, as the FSD P1 REC table states ("zero orphans; every one listed").
- DP01 Account and arrears and DP02 Customer and party are LOADED for 2026-11-30 in the SIT fixture, or they answer STALE with their last load date; both are DAILY products expected by 08:00 (FSD P1 v3 A2.2).
- The check names EXCL, KEY and REF under their rec codes, the state names, the alert recipient groups and the Schedule cron are configuration of this service and are read with their version; no value is compiled in (GAP-0740; ASM-1348).
- The SIT fixture holds synthetic case, exclusion, queue, membership and assignment rows only: no production data, and no connection to a real ACE or to ALS, SCBPDM or the core bank.
- The login is the rwb-case login (DP-02); it holds no grant on any `recovery.v_ace_*` view, no grant on another service's schema and no other service's credential. Its name is Not specified in the source documents (GAP-0740; ASM-1354).

### 4. Flow

1. The Temporal Schedule of this service starts `CaseQualityWorkflow` for the business date on task queue `rwb-case` in namespace `rwb-recovery`, one run per business date; no event starts it (12.4).
2. The workflow asks the load-tolerance activity for the tolerance of each check of the run through the parameters contract of this service, with the version in force (DP-06); the value is 0.00 for the REC-01 EXCL check in the fixture of the date, and the REC-05 KEY and REC-05 REF checks carry their zero tolerance.
3. The workflow asks the read-ace-facts activity for the freshness answer of DP01 Account and arrears and DP02 Customer and party for the business date through the rwb-source-data contract; an answer that is not LOADED for the date writes no result and holds the date, with the last load date as the reason (AC4).
4. The same activity reads the DP01 and DP02 rows of the business date through the rwb-source-data contract, one hop with a 2 s timeout (DP-11); no ACE view and no ACE table is read by this service (DP-05).
5. The workflow reads the facts of the date from `rwb_case`: the `case_entry_exclusion` rows with their product group, reason code, rule ID and rule version; the account keys of `case_account`, the person keys of `case_party` and the primary person keys of `recovery_case`; and the open cases with their queue, their owner and their open `assignment` row.
6. The exclusion reconciler compares the exclusion rows held for the date with the exclusion facts served for the date, per product group, and counts the rows that carry no reason code, no rule ID or no rule version: both are unexplained exclusions, and the variance percent is the unexplained count over the rows held (BR1, BR2).
7. The key reconciler resolves every account key against the DP01 rows of the date and every person key and primary person key against the DP02 rows, and counts the orphans in both directions, listing each one with its table and its column (BR3).
8. The reference reconciler resolves the queue of every open case against `queue` and the owner of every open case against `queue_member` for the date, and counts the unresolved references: a case with no queue and an owner who is not a member of the case's queue are both breaks (BR4).
9. It compares each variance with the tolerance in force and sets the result of each check: PASS when the variance is equal to or below the tolerance, BREAK when it is above it, and for the two REC-05 checks PASS only at zero (AC2, AC3).
10. It writes one row per check and product group for the business date, the break rows of every row or key that does not resolve, and the run row, in one transaction, replacing the rows of that date on a rerun; the unique key is the rec code, the check name, the product group and the business date (AC5, AC6).
11. It sets the state of the run to TRUSTED when every check is PASS and to HELD when any check is BREAK or not run, and it writes the not-run reason of a held date; on a break it lists the breaking rows and keys for the data steward and, where the row is missing in ACE, for the ACE team, and it sends the break alert to the data steward, the platform administrator and the team managers with MSG-P1-012 (AC2, AC7, AC9).
12. It writes one decision record for the run through the local decision-record library, with the date, the nine results and the orphan count, and it writes no event and no file: DP-09 is not in the pattern set of this story, and the data lake, the INT-19 adapter and the two extracts of the legacy publish step do not exist in the target (AC8; GAP-0740; ASM-1346).
13. `GET /quality-runs/{businessDate}` answers the run record, `GET /quality-results` answers the result rows with their break rows, `GET /reconciliation-facts/{businessDate}` answers the exclusion, case, queue and assignment facts of the date with the state of the run, and `GET /reconciliation-facts/keys` answers the keys the case tables hold, so the data steward on SCR-45, rwb-source-data for the exclusion and key sides of its own reconciliation, rwb-reporting for the report and the integration run read the same rows (12.1).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A check's variance is above the tolerance | Result BREAK; the run state HELD; the breaking rows and keys listed; the alert sent | MSG-P1-012 | AC2 |
| X2 | The variance equals the tolerance | Result PASS | None | AC3 |
| X3 | DP01 Account and arrears or DP02 Customer and party is not LOADED for the business date | The run state is NOT_RUN, no result is written for the date and every check shows not run with the last load date as the reason; the facts read answers the same state | MSG-P1-001 | AC4 |
| X4 | The run repeats for the same date after a fix | The rows of that date are replaced and the run state is TRUSTED if every check is PASS | None | AC5 |
| X5 | Two runs for the same date on two workers | One row per check, product group and business date; no row written twice | None | AC6 |
| X6 | An account key, a person key or a primary person key has no data-product row | The check is BREAK with the orphan count; the key is listed with its table and its column for the data steward and, where the row is missing in ACE, for the ACE team; no case row changes | None | AC7 |
| X7 | A case carries no queue, or its owner is not a member of its queue on the date | The REC-05 REF check is BREAK with the unresolved count; each reference is listed; no case, queue, membership or assignment row changes | None | AC9 |
| X8 | The parameters contract or the rwb-source-data contract returns an error mid-run | No result is written for the date; the run state is FAILED with the system named; the rerun writes every row | MSG-GEN-006 | TC-E1-011-09 |
| X9 | A role without Platform administration R reads the run record, the results or the facts | 403, and nothing is written | MSG-P4-002 | AC10 |
| X10 | A caller reads a path outside `/api/recovery/case/v1`, a cross-schema read appears, or an extract file or lake path is written | The build fails the boundary test and nothing is released | None | BR11 |
| X11 | The token carries no Workbench role | 401, and nothing is written | MSG-P4-001 | AC10 |

X8 is the only path that leaves no result row for a date the run had started: the store and the two contracts are read in one activity, so a failure anywhere in it rolls the date back rather than writing half a date.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the case, exclusion, queue, membership and assignment rows that RWB-P3-E1018-APP, RWB-P3-E1019-APP and RWB-P3-E1020-APP write, and builds against the rwb-source-data contract fake and the parameter and reference fixtures of 12.8; it changes no case and reads no table of another service |
| Negotiable | The tolerance is a parameter with a version, the product groups, exclusion reasons, queue codes and result values are reference data, and the check names, the alert groups and the Schedule are configuration, not code |
| Valuable | The data steward sees each morning which exclusions of the date cannot be explained, which keys lead nowhere and which owner sits outside the queue, before the case list of the date is relied on |
| Estimable | One workflow, one Schedule, three checks, three read operations, two consumed operations and three tables |
| Small | Fits two weeks with its tests, as the secondary slice of the legacy key |
| Testable | Each criterion below is one automated test on synthetic rows and the three contract fakes, with no ACE view and no data lake |

### 7. Acceptance criteria

```gherkin
Feature: Reconciliation and data quality of the case, queue and assignment facts, in rwb-case

  Background:
    Given the business date is 2026-11-30
    Given the parameter recon.tolerance.pct = 0.00 is in force for the REC-01 EXCL check
    Given the rwb-source-data contract mock returns the freshness answer LOADED for DP01 Account and arrears and DP02 Customer and party for 2026-11-30

  Scenario: AC1 No break for the date (new, D-RCV-60)
    Given rwb-case holds 21 case_entry_exclusion rows for 2026-11-30: 12 MORTGAGE, 6 HIRE_PURCHASE and 3 SSME, each with a reason code, a rule ID and a rule version
    Given the exclusion facts served for 2026-11-30 hold the same 21 rows in the same product groups
    Given every account_key on case_account, every person_key on case_party and every primary_person_key on recovery_case of 2026-11-30 resolves to a row of the DP01 and DP02 rows of the contract mock
    Given every open case of 2026-11-30 carries a queue in force, and every owner it carries is a member of that queue on 2026-11-30
    When the quality run of 2026-11-30 runs
    Then the system writes nine rows for 2026-11-30, REC-01 EXCL, REC-05 KEY and REC-05 REF for each of the three product groups, each with variance 0 and result PASS
    Then the run state of 2026-11-30 is TRUSTED
    Then GET /quality-results answers the nine rows with their counts, the tolerance 0.00 and no break row
    Then GET /reconciliation-facts/2026-11-30 answers the 21 exclusions, the case, queue and assignment counts and the state TRUSTED

  Scenario: AC2 A break over the tolerance (new, D-RCV-60)
    Given rwb-case holds 3 SSME case_entry_exclusion rows for 2026-11-30 and one of them carries no rule version
    Given the exclusion facts served for 2026-11-30 hold the same 3 SSME rows
    When the quality run of 2026-11-30 runs
    Then the REC-01 EXCL result for SSME is BREAK with variance count 1 and variance percent 33.33
    Then the exclusion row without a rule version is on the break list with its account key, its reason code and its business date
    Then the run state of 2026-11-30 is HELD
    Then the data steward, platform administrator and team manager groups receive MSG-P1-012 "The case list for 2026-11-30 does not reconcile to ACE for SSME: a difference of 1 accounts, 33.33 percent."
    Then the REC-05 KEY and REC-05 REF results for SSME are unchanged

  Scenario: AC3 Variance equal to the tolerance (new, D-RCV-60)
    Given the parameter recon.tolerance.pct for the REC-01 EXCL check is changed by a reference load to 0.10 from 2026-11-30
    Given MORTGAGE holds 1,000 exclusion rows of 2026-11-30 and 1 of them carries no reason code, a variance of 0.10 percent
    Given SSME holds 900 exclusion rows of 2026-11-30 and 1 of them carries no reason code, a variance of 0.11 percent
    When the quality run of 2026-11-30 runs
    Then the MORTGAGE result is PASS and the SSME result is BREAK

  Scenario: AC4 The account and customer data products are not loaded for the date (new, D-RCV-60)
    Given the rwb-source-data contract mock returns no LOADED answer for DP01 Account and arrears for 2026-11-30 and the stale marker naming "DP01 Account and arrears" and 2026-11-27
    When the Schedule starts the quality run of 2026-11-30
    Then the run writes no quality result for 2026-11-30 and its state is NOT_RUN
    Then GET /quality-runs/2026-11-30 shows REC-01 EXCL, REC-05 KEY and REC-05 REF as not run with the reason "DP01 is from 2026-11-27"
    Then the data steward, platform administrator and team manager groups receive MSG-P1-001 naming the product and the date
    Then GET /reconciliation-facts/2026-11-30 answers the facts of the date with the state NOT_RUN and the same reason

  Scenario: AC5 Rerun after the fact is fixed (new, D-RCV-60)
    Given the REC-01 EXCL result for SSME on 2026-11-30 is BREAK and the run state is HELD
    Given the exclusion row of the date has since been given its rule version and the exclusion facts of the date hold the 3 SSME rows in full
    When the platform administrator restarts the quality run for 2026-11-30
    Then the run replaces the nine rows for 2026-11-30 and all are PASS
    Then the run state of 2026-11-30 is TRUSTED
    Then GET /quality-results answers the nine rows of the rerun and no row of the earlier run

  Scenario: AC6 Two runs for the same date (new, D-RCV-60)
    Given two quality runs for 2026-11-30 start on two workers
    When both reach the reconciliation activity
    Then case_quality_result holds one row per check, product group and business date, nine rows in all
    Then no row is written twice for the same rec_code, quality_check, product_group and business_date

  Scenario: AC7 A business key with no source row (new, D-RCV-60)
    Given case_party on case "RW-2026-000140" carries person_key "P0099881", which has no row in the DP02 rows of the contract mock
    When the REC-05 KEY check of 2026-11-30 runs
    Then the REC-05 KEY result for the product group of the case is BREAK with 1 orphan
    Then "case_party.person_key P0099881" is on the break list for the data steward and the ACE team
    Then the case and its case_party row are unchanged
    Then the run state of 2026-11-30 is HELD

  Scenario: AC8 No data-lake extract (new, D-RCV-60)
    Given the quality run of 2026-11-30 has finished with PASS on its nine rows
    When the run completes
    Then the nine rows and their break rows are readable through GET /quality-runs/2026-11-30 and GET /quality-results
    Then no reconciliation extract and no data quality extract is written, no INT-19 adapter is called and no lake path exists for the date
    Then no Power BI data set is written for the date, and the measures of the date are answered by the reads of section 12.1

  Scenario: AC9 A queue or an owner that does not resolve (new, D-RCV-60)
    Given case "RW-2026-000150" sits in queue "MTG-BKK-CO" and carries owner "U-1001", who is not a member of queue "MTG-BKK-CO" on 2026-11-30
    Given case "RW-2026-000151" carries no queue
    When the REC-05 REF check of 2026-11-30 runs
    Then the REC-05 REF result for MORTGAGE is BREAK with 2 unresolved references
    Then "case RW-2026-000150 owner U-1001 not a member of MTG-BKK-CO" is on the break list for the data steward
    Then "case RW-2026-000151 no queue" is on the break list for the data steward
    Then no case, queue, queue_member or assignment row changes

  Scenario: AC10 A role without the right (new, D-RCV-60)
    Given the caller holds role RW-CASEOWN with no Platform administration right
    When the caller reads GET /quality-results for 2026-11-30
    Then the response is 403 with message MSG-P4-002 and no row is read
    Then a token with no Recovery Workbench role is refused with 401 and message MSG-P4-001
```

Every criterion above is new under D-RCV-60; no legacy acceptance criterion of RWB-E1-011 is owned or restated here. The legacy criteria of the key are owned by `RWB-P1-E1011-APP` (AC5, AC6 and AC8) and proved end to end by `RWB-ITG-E1011-ITG` (AC1, AC2, AC3, AC4 and AC7), whose contract and deployment slices `RWB-P1-E1011-CON` and `RWB-P1-E1011-OPS` carry the same ids. The one Given line each criterion adds over a pure unit test is the mock of the rwb-source-data contract, because the ACE side of the key check is the only cross-service part and is mocked with 12.8 (DP-11). The legacy values the criteria keep character for character are the business date 2026-11-30, the stale reason "DP01 is from 2026-11-27", the case "RW-2026-000140" and its person key "P0099881" of legacy AC7, and the tolerance change to 0.10 with the variances 0.10 and 0.11 percent of legacy AC3.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every business date, rwb-case reconciles the exclusion rows it recorded for the date with the exclusion facts it serves for the date, per product group, and counts as unexplained every row that carries no reason code, no rule ID or no rule version | REC-01; REQ-RDF-007; REQ-CWC-004; FSD P1 v3 A2.11 "zero unexplained"; legacy RWB-E1-011 BR8 |
| BR2 | The variance count is the difference between the two sides of a check; the variance percent is that difference over the source side of the check, and both are written on the result row with the tolerance applied | TSD P1 v3 `reconciliation_result` (DF-OPS-122 to DF-OPS-129); legacy section 7 |
| BR3 | Every `account_key` on `case_account`, every `person_key` on `case_party` and every `primary_person_key` on `recovery_case` must resolve to a row of DP01 Account and arrears or DP02 Customer and party; zero orphans, and every one is listed with its table and its column | REC-05; REQ-RDF-007; FSD P1 v3 A2.11 and A2.12 "referential completeness, 100 percent"; legacy RWB-E1-011 BR5 and AC7 |
| BR4 | Every open case must carry a queue in force, and every owner it carries must be a member of that queue on the business date; zero unresolved references, and every one is listed with its case, its queue and its owner | REC-05 as FSD P3 v4 applies it; FSD P3 v4 check "References" (AC-EXC-P3-035-01); DF-CAS-010, DF-WRK-002, DF-WRK-046, DF-WRK-047 |
| BR5 | No reconciliation runs until the owner of the account and customer data products answers LOADED for the business date; a run that cannot obtain that answer writes no result and holds the date with the last load date as its reason | Legacy BR9; FSD P1 v3 VR-P1-002-1; MSG-P1-001 |
| BR6 | A result is BREAK when the variance percent is above the tolerance and PASS when it is equal to or below it; the boundary value is a PASS; the two REC-05 checks are PASS only at zero | Legacy AC3 and BR6; parameter recon.tolerance.pct, 0.00 assumed (DL25) |
| BR7 | A break lists the exclusion row, the key or the reference with its product group, its table, its column and its reason, for the data steward and, where the row is missing in ACE, for the ACE team | Legacy BR7 and BR13; FEAT-RDF-12; FSD P1 v3 A2.12 |
| BR8 | A repeated run for the same date replaces that date's rows, and a passing rerun releases the date; two runs for the same date produce one row per check, product group and business date | Legacy BR11, AC5 and AC6; R-UNI-40 |
| BR9 | The exclusion, case, queue and assignment facts of a date are served only from `rwb_case` and only through the reads of 12.1; no reader is given a `rwb_case` table, a view or a copy | DP-01; DP-11; legacy section 12 (the P3 published interface) |
| BR10 | The state of the run is TRUSTED, HELD, NOT_RUN or FAILED, and a date that is not TRUSTED answers the reason with the state wherever the facts of the date are read | Legacy BR10 (green, red, not run with the reason) |
| BR11 | The quality facts are this service's own rows: no data lake, no INT-19 adapter, no extract file, no Power BI data set and no outbound item is written for the date, and no table of another service is read | DP-17; ADR-018; Architecture v5 slides 37 and 44; legacy section 4 step 11 reversed |
| BR12 | The run uses one business date only, the business date in force of the data products it reconciles against, and never a mix of two business dates | Legacy BR12; BR-P1-011-2 |
| BR13 | A break never changes or deletes an exclusion row, a case row, a queue row, a membership row, an assignment row or an ACE row; the rerun through the workflow is the only path that replaces the rows of a date | Legacy BR13; FSD P1 v3 BR-P1-011-3 |
| BR14 | A role without the right of the capability area is refused with MSG-P4-002 and nothing is read or written | FSD P1 v3 A2.11.4.3 AC-EXC-P1-011-03; legacy section 5 X8 |

The three checks are REC-01 with the check name EXCL, and REC-05 with the check names KEY and REF. EXCL and KEY are the legacy codes of the exclusion side of REC-01 and of the business-key rule; REF carries the REC-05 code because the FSD P3 v4 names a reference that does not resolve "References" and lists it on the same break list (AC-EXC-P3-035-01). The three check names are this story's design and carry no source (GAP-0740; ASM-1345). REC-02, REC-03, REC-04, REC-06 to REC-09, the account count of REC-01 and the case-list publish are not this service's and are listed in section 19.

### 9. State transitions

None for a case status, a queue, a membership or an assignment. This story changes no case and no exclusion; it writes the state of its own run row and the result rows of the business date.

| From | Event | Condition | To |
|---|---|---|---|
| Not run | The Schedule starts the run | DP01 and DP02 answer LOADED for the business date | Running |
| Not run | The Schedule starts the run | An answer is not LOADED, or cannot be read | Not run, with the not-run reason and the last load date on the run row |
| Running | The three checks are computed | Every check is PASS | Trusted |
| Running | The three checks are computed | At least one check is BREAK | Held |
| Running | A source read fails | The parameters or the data-product rows cannot be read | Failed, with the system named and no result row for the date |
| Held | A rerun for the same date | The rows of the date are replaced and every check is PASS | Trusted |
| Trusted | A rerun for the same date | A check is BREAK | Held |

The result value of a check is the legacy value set of `reconciliation_result.result`, LOV-REC-RESULT: PASS and BREAK, plus the not-run grade and its reason that legacy BR10 defines and that this story writes on the run row only, never as a third result value. The four state names are this story's design, kept in the vocabulary of the legacy case-list publish so that the registers and the report stay readable (GAP-0740; ASM-1345).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-case service identity | Runs the workflow, reads the parameters, the reference data and the data-product rows through their owners' operations, and writes the run row, the result rows and the break rows of `rwb_case`; it holds no grant on another schema and no grant on `recovery.v_ace_*` |
| RW-DATASTEW, data steward and data product owner | Platform administration R: reads the run record, the results, the break rows and the facts of the date, and signs the daily case-side quality result |
| RW-PLATADM, platform administrator | Platform administration R and U: reads the results and restarts the run for a business date |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-SECADM | Read the results, the break rows and the facts of the date in the Platform administration area, right R |
| rwb-source-data service identity | Reads `GET /reconciliation-facts/{businessDate}` for the exclusion side of REC-01 and `GET /reconciliation-facts/keys` for the case side of REC-05 of its own reconciliation run; no write and no other operation |
| rwb-reporting service identity | Reads the two quality operations and the facts read for the report of the date; no write |
| RW-TEAMMGR, RW-BIANAL and other report readers | Reporting R on the report of the date; RW-BIANAL builds it with Reporting CRUD, outside this story |
| ACE team | Reads the break rows of a key whose row is missing in ACE, through the data steward's listing |

The right of the two quality reads and of the facts read is declared in the Platform administration capability area, right R, as the legacy story declares it for its job listing. TSD P3 v3 has no Platform administration right for a quality read, so the module matrix neither grants nor refuses it; the legacy story comes first in the fill order and the right is kept (GAP-0740; ASM-1350). DP-08 is not in the patterns applied to this story: the declared area and right are enforced at gateway-bff for the screen path, and where a local guard is required on the operation itself the guard and its story are not named in the sources.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-002 | recovery_case | case_no | Read, the case of a break row |
| DF-CAS-003 | recovery_case | product_group | Read, the grouping key of the three checks |
| DF-CAS-004 | recovery_case | primary_person_key | Read, resolved by REC-05 KEY |
| DF-CAS-005 | recovery_case | status | Read, to select the open cases |
| DF-CAS-009 | recovery_case | owner_user_id | Read, the owner reference of REC-05 REF |
| DF-CAS-010 | recovery_case | queue_id | Read, the queue reference of REC-05 REF |
| DF-CAS-013 | recovery_case | entry_date | Read, to select the cases of the date |
| DF-CAS-026 | case_account | the account key the case links, named account_id in TSD P3 v3 and account_key in the FSD P3 v4 re-base | Read, resolved by REC-05 KEY (GAP-0740; ASM-1351) |
| DF-CAS-032 | case_party | the party key of the case, named party_id in TSD P3 v3 and person_key in the FSD P3 v4 re-base | Read, resolved by REC-05 KEY (GAP-0740; ASM-1351) |
| DF-CAS-056 | case_entry_exclusion | id | Read |
| DF-CAS-057 | case_entry_exclusion | the account key kept out at entry, named account_id in TSD P3 v3 | Read, the break row of REC-01 EXCL |
| DF-CAS-058 | case_entry_exclusion | business_date | Read, to select the exclusions of the date |
| DF-CAS-059 | case_entry_exclusion | reason_code | Read, LOV-EXCLUSION-REASON; an empty value is an unexplained exclusion |
| DF-CAS-060 | case_entry_exclusion | rule_id | Read; an empty value is an unexplained exclusion |
| DF-CAS-061 | case_entry_exclusion | rule_version | Read; an empty value is an unexplained exclusion |
| DF-WRK-001 | queue | id | Read |
| DF-WRK-002 | queue | queue_code | Read, the queue reference of REC-05 REF |
| DF-WRK-004 | queue | team_code | Read, the team a break row names |
| DF-WRK-045 | queue_member | id | Read |
| DF-WRK-046 | queue_member | queue_id | Read |
| DF-WRK-047 | queue_member | user_id | Read, the membership an owner is resolved against |
| DF-WRK-051 | queue_member | valid_from | Read, the membership in force on the business date |
| DF-WRK-052 | queue_member | valid_to | Read |
| DF-WRK-009 | assignment | id | Read |
| DF-WRK-010 | assignment | case_id | Read |
| DF-WRK-012 | assignment | assignee_user_id | Read, the open assignment of a case |
| DF-WRK-014 | assignment | ended_at | Read, to select the open assignment |
| DF-ACE-001 | the DP01 rows (P1) | account_key | Read through the rwb-source-data contract only |
| DF-ACE-056 | the DP02 rows (P1) | person_key | Read through the rwb-source-data contract only |
| No BR Field ID | case_quality_run, case_quality_result, case_quality_break | the run state, the check, the counts, the variance, the tolerance and the break reason | Write; the service's own tables, whose columns carry no field ID in the sources (GAP-0740; ASM-1351) |

**Indexes and migration.** The three tables arrive in the service's per-service Flyway sequence (DP-15), as `V1011_1__case_quality.sql` by the convention of the service, after the case baseline of RWB-P3-E1018-APP, the queue baseline of RWB-P3-E1019-APP and the assignment baseline of RWB-P3-E1020-APP: `case_quality_run` with a unique business date, `case_quality_result` with a unique (rec_code, quality_check, product_group, business_date), and `case_quality_break` with an index on (business_date, rec_code) and on (key_type, key_value). No column is added to `recovery_case`, `case_account`, `case_party`, `case_entry_exclusion`, `queue`, `queue_member` or `assignment`, and no column carries another service's data (DP-01, DP-15).

**The key columns.** The case links are the ACE business keys of the FSD P3 v4 re-base under D-RCV-35 (account_key, person_key, primary_person_key, no foreign key across services), while TSD P3 v3 declares the same columns as uuid cross-references named account_id and party_id; this story reads whatever key value the column of the writing story holds and resolves it against the data-product rows by that key, so the check is the same under either declaration (GAP-0740; ASM-1351).

**No personal data.** The run row, the result rows and the break rows carry a case number, a product group, a queue code, a team code, an owner identifier, an account key, a person key, a business date, counts, a variance, a percent and a reason. No name, address, contact value or identity number enters these tables, is logged by the run or is part of any break row.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-case (P3); base `/api/recovery/case/v1`.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/quality-runs/{businessDate}` | The run record of the business date: the state TRUSTED, HELD, NOT_RUN or FAILED with its reason, each check with PASS, BREAK or not run, the tolerance in force, the count of break rows and the times of the run | Platform administration R, scope applied | Not applicable |
| GET | `/quality-results` | The quality facts of a business date with their break rows: rec code, check, product group, source and workbench counts, variance count, variance percent, tolerance percent, result, and per break row the key or the reference, the table, the column and the reason | Platform administration R, scope applied; Reporting R for the report reader | Not applicable |
| GET | `/reconciliation-facts/{businessDate}` | The case, queue and assignment facts rwb-case serves for the reconciliation of the date: per product group the open case count, the assigned and unassigned counts, the exclusion count by reason code and rule version, the count of its own rows, and the state of the run of the date with its reason; no personal data | Platform administration R, scope applied; the rwb-source-data service identity for the exclusion side of REC-01; Reporting R for the report reader | Not applicable |
| GET | `/reconciliation-facts/keys` | The business keys the case tables hold for a business date - account keys of `case_account`, person keys of `case_party` and primary person keys of `recovery_case` - with the table and the column of each, for the REC-05 resolution of the enterprise reconciliation and of the integration proof | Platform administration R, scope applied; the rwb-source-data service identity for the case side of REC-05 | Not applicable |

All four are reads: they declare no Idempotency-Key, answer 401, 403, 404 and 503 with the platform error envelope, and answer from `rwb_case` only. The four paths and their element names are Not specified in the source documents (GAP-0740; ASM-1345); they follow the service base, the problem response and the read shape of the rwb-case service contract. The facts read carries the exclusion count of the legacy published interface `excludedAccountsByProduct(businessDate)` of RWB-E1-011 section 12, which was an in-process call from the case-list step and is a read operation here (DP-11; BR9).

#### 12.2 REST operations consumed

| Method | Path | Owner | Used for |
|---|---|---|---|
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | The LOADED or STALE answer of DP01 Account and arrears and DP02 Customer and party for the business date, with the last load date, before any check runs (AC4); faked (GAP-0740; ASM-1349) |
| GET | `/api/recovery/source-data/v1/data-products/{productCode}/records` | P1 rwb-source-data | The DP01 account rows and the DP02 customer rows of the business date, for the key side of REC-05; faked, and the element names are Not specified in the source documents (GAP-0740; ASM-1349) |

Every row is one hop with a 2 s timeout, one GET retry with jitter and a breaker per downstream (DP-11, ADR-020). The parameter and reference rows are read in process through RWB-P3-E1042-CON and RWB-P3-E1043-CON: library reads of this same service, not cross-service calls (DP-06, DP-07). The connection matrix of Architecture v5 slide 13 gives the P3 row a Temporal and event cell for P1 and no REST cell, while Template and Rules §R5.5 DP-11 and the sibling slices of this key use the published REST reads of P1's data-product operations; this story follows DP-11 and the published API of P1, and the bulk snapshot activity of P1 (`snapshot(page)`, `listEligibleAccounts`) is not used here (GAP-0740; ASM-1349).

#### 12.3 Events published

None. DP-09 is not in the pattern set of this story, so no event is written to the outbox and no Kafka record is published by this run. The topic `rwb.case.events.v1` with the names `rwb.case.CaseCreated.v1`, `rwb.case.CaseAllocated.v1`, `rwb.case.CaseTransferred.v1`, `rwb.case.CaseStateChanged.v1` and `rwb.case.TimerBreached.v1` carries the case, allocation, transfer, state and timer facts of the case stories under DP-14 (Architecture v5 slide 19); this slice publishes none of them and adds no event, and the quality facts are served by the reads of 12.1 (GAP-0740; ASM-1345).

#### 12.4 Events consumed

None. The run is started by the Schedule of 12.6 and reads no event; the data-product rows arrive synchronously through the rwb-source-data contract, and a redelivered event cannot start a second run.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Element |
|---|---|---|---|
| `CaseQualityWorkflow` | Workflow from the kit template; one per business date | `rwb-case` in namespace `rwb-recovery` | Owns the run: the parameter read, the freshness gate, the three checks, the rows of the date and the run state |
| `loadTolerance` | Activity, reads the parameters of this service (DP-06) | `rwb-case` | Reads `recon.tolerance.pct` per check with its version before any check runs |
| `readAceFacts` | Activity, calls rwb-source-data (P1) | `rwb-case` | Reads the freshness answer and the DP01 and DP02 rows of the business date; writes nothing when an answer is not LOADED |
| `reconcileCaseFacts` | Activity, reads `rwb_case` only | `rwb-case` | Computes the three checks, their counts, variance and percent, and the break rows of the date |
| `writeQualityFacts` | Activity, writes `rwb_case` only | `rwb-case` | Writes the run row, the result rows and the break rows in one transaction and replaces the rows of the date |

The workflow is idempotent by business date, check and product group: a retried run does not write a second row for the same key and does not restart a trusted date without a rerun request. The decision record of the run is written through the local decision-record library in the same transaction as the rows (DP-03).

#### 12.6 Schedules

One Schedule, owned by this service.

| Schedule | Cron | Overlap | Catch-up | What it starts |
|---|---|---|---|---|
| The case quality Schedule of rwb-case (RWB-PLT-E1071-CON) | Not specified in the source documents (GAP-0740; ASM-1348) | SKIP | Catch-up window of the workflow kit | `CaseQualityWorkflow` for the business date, after the DP01 and DP02 window of the morning (08:00) has passed |

No Quartz row, no shared job table entry and no Control-M job is registered for this run; JOB-04 stays rwb-source-data's event-started workflow (Architecture v5 slide 44), and the Schedules this service already owns - the daily case run and the rebalancing run - are not changed here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| recovery_case | P3 (rwb_case) | The case row behind every check: number, product group, status, queue, owner, entry date and primary person key; read only in this story |
| case_account | P3 (rwb_case) | The account links of a case; the account key side of REC-05 KEY; read only |
| case_party | P3 (rwb_case) | The party roles of a case; the person key side of REC-05 KEY; read only |
| case_entry_exclusion | P3 (rwb_case) | The accounts kept out at entry with their reason code, rule ID and rule version; the REC-01 EXCL source; read only |
| queue | P3 (rwb_case) | The queue code, team and role; the queue reference of REC-05 REF; read only |
| queue_member | P3 (rwb_case) | The membership of a user in a queue by version; the owner reference of REC-05 REF; read only |
| assignment | P3 (rwb_case) | Who holds a case and from when; the open assignment of a case; read only |
| case_quality_run | P3 (rwb_case) | The run of one business date: state, not-run reason, times and break count |
| case_quality_result | P3 (rwb_case) | One row per check, product group and business date: counts, variance, percent, tolerance and result |
| case_quality_break | P3 (rwb_case) | One row per breaking row, key or reference of a check, with its table, its column and its reason |

The three quality tables are this story's design and carry no field ID in the sources (GAP-0740; ASM-1351). Not owned and never read as a table: `reconciliation_result` and `case_list_row` (P1), `treatment` (S2), `proceeds` (P8), `notice` (P6), `asset`, `listing` and `asset_sale` (S5), `task` and `timer` (P3, not read by this run).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data freshness fake | LOADED for DP01 and DP02 for 2026-11-30 with their load time; not LOADED for DP01, with the stale marker naming "DP01 Account and arrears" and 2026-11-27; an error after the first read | AC1, AC2, AC3, AC4, AC7, AC9 |
| rwb-source-data records fake | The DP01 account rows and the DP02 customer rows of 2026-11-30, one row for every key of the case tables; one run with no row for person_key `P0099881` | AC1, AC7 |
| Parameter and reference fixtures of this service | `recon.tolerance.pct` 0.00 for the REC-01 EXCL check and the 0.10 version in force from 2026-11-30 of AC3; LOV-PRODUCT with MORTGAGE, HIRE_PURCHASE and SSME; LOV-EXCLUSION-REASON; LOV-REC-RESULT with PASS and BREAK | AC1, AC2, AC3, AC4 |
| rwb-case seed set | 21 exclusion rows of 2026-11-30 (12 MORTGAGE, 6 HIRE_PURCHASE, 3 SSME); cases `RW-2026-000140`, `RW-2026-000150` and `RW-2026-000151`; queues `MTG-BKK-CO` and `SME-NTH-CO` with their members | AC1, AC2, AC5, AC7, AC9 |

The fakes are test-only and are replaced by the real services in SIT; the drift between a fake and the published document is a build failure. The fixture values are synthetic case and exclusion rows of the same SYN convention as the legacy story, and no production value is used (GAP-0740; ASM-1353).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 2 consumed | The run record, the quality facts, the facts of the date and the keys; the freshness answer and the data-product rows; one hop and 2 s each |
| Kafka | 0 published, 0 consumed | DP-09 is not in the pattern set of this story and the run is Schedule-started |
| Temporal | 1 workflow, 4 activities | `CaseQualityWorkflow` on `rwb-case` with `loadTolerance`, `readAceFacts`, `reconcileCaseFacts` and `writeQualityFacts` |
| File | 0 | No extract file and no outbound item: the data lake and the INT-19 adapter are removed (DP-17) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `quality`, Java package `th.co.scb.ace.workbench.recovery.case.quality`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_case`; the run reads `recovery_case`, `case_account`, `case_party`, `case_entry_exclusion`, `queue`, `queue_member` and `assignment` of this service only | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.case.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

Seven of these patterns add a platform CON in the DP table (RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON) and two add a contract of this same service (RWB-P3-E1042-CON and RWB-P3-E1043-CON), while the plan sets this story's Depends on (build) and Contract dependencies to None. Both lists stay None as the plan sets them: the platform CONs land through the platform release train of wave 0, before the wave-1 build, and they are not a lane dependency of an APP story (GAP-0740; ASM-1343); the two contracts of this service are read in process against its own rows and never block the build (GAP-0740; ASM-1344). DP-05 applies as a prohibition first: rwb-case reads no `recovery.v_ace_*` view and no ACE table, and every ACE-side fact arrives through the rwb-source-data contract, the only reader of the views (Architecture v5 slides 29, 37 and 45). DP-17 applies as the removal of the lake target: the two extracts, the INT-19 adapter, the lake path of the date and the Power BI data set are dropped and the facts are served by the reads of 12.1 (GAP-0740; ASM-1346). DP-11 is the read shape of the two consumed operations, mocked from Day 1, and the serving shape of the two fact reads of 12.1. DP-14 applies to the naming only: this story publishes no event, and the topic constant comes from the naming library for the events the case stories publish. DP-19 applies to the surfaces that render the run record and the break rows; the screens themselves are not built here. DP-03 applies where a rule decides the handling of a break; the record is written first through the library and a failed write stops the run.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseQualityController | Controller | `GET /quality-runs/{businessDate}` and `GET /quality-results`, with the problem mapping for 401, 403, 404 and 503 |
| ReconciliationFactController | Controller | `GET /reconciliation-facts/{businessDate}` and `GET /reconciliation-facts/keys`, scoped and without personal data |
| CaseQualityWorkflow | Workflow | The run of section 4: parameter read, freshness gate, the three checks, the rows and the state |
| ToleranceReader | Service | Reads `recon.tolerance.pct` per check with its version through the parameters contract (DP-06) |
| AceFactReader | Service | Reads the freshness answer and the DP01 and DP02 rows of the business date through the rwb-source-data contract, and returns nothing when an answer is not LOADED (DP-11) |
| ExclusionReconciler | Service | The REC-01 EXCL check: the rows held against the facts served, and the rows with no reason code, rule ID or rule version |
| KeyReconciler | Service | The REC-05 KEY check: every account key and person key against the DP01 and DP02 rows, both directions |
| ReferenceReconciler | Service | The REC-05 REF check: the queue and the owner of every open case against `queue` and `queue_member` |
| QualityFactWriter | Service | Writes the run, the results and the break rows in one transaction, replacing the rows of the date |
| QualityBreakNotifier | Service | Sends the MSG-P1-012 wording and the MSG-P1-001 wording to the configured groups |
| QualityReadModel | Service | Answers the four reads of 12.1 from `rwb_case` only, including the case, queue and assignment counts and the referential completeness rate of the date |
| DecisionRecordWriter | Component | Writes the run record through the local decision-record library before the rows are committed (DP-03) |

**Database and migrations.** `V1011_1__case_quality.sql` creates `case_quality_run`, `case_quality_result` and `case_quality_break` with the unique keys and indexes of section 11, after the case, queue and assignment baselines of RWB-P3-E1018-APP, RWB-P3-E1019-APP and RWB-P3-E1020-APP. No column is added to `recovery_case`, `case_account`, `case_party`, `case_entry_exclusion`, `queue`, `queue_member` or `assignment`, and no column carries another service's data (DP-01, DP-15).

**Configuration and reference data.** The parameter key of each check, the check names EXCL, KEY and REF under their rec codes, the four state names, the alert recipient groups and the Schedule cron are configuration and reference data of this service read with a version, owned by the platform administrator; the tolerance value is the parameter of 12.2 and is never compiled in. The product groups, the exclusion reasons, the queue codes, the result values and the run states are reference data through DP-07: LOV-PRODUCT, LOV-EXCLUSION-REASON, LOV-REC-RESULT and the queue rows (GAP-0740; ASM-1348).

**Build steps**

1. Write the migration and test the three unique keys and the two query indexes.
2. Build `ToleranceReader` and `AceFactReader` over the two fakes, with the freshness gate and the stale marker; test AC4.
3. Build `ExclusionReconciler` for REC-01 EXCL; unit test variance 0, the tolerance boundary and a break; tests for AC1, AC2 and AC3.
4. Build `KeyReconciler` for REC-05 KEY over the three key families, both directions; test AC7 and the no-change rule.
5. Build `ReferenceReconciler` for REC-05 REF over the queue and the membership of the date; test AC9.
6. Build `QualityFactWriter` with the replace of one date and the unique key; tests for AC5 and AC6.
7. Build `QualityReadModel` and the two controllers over the read model, including the facts read and the keys read; test AC1, AC10 and the no-extract assertion of AC8.
8. Build `CaseQualityWorkflow` with the Schedule hook, the retry rule by business date and check, and the decision record of the run.
9. Add the run to the job monitor surface of SCR-44 and to the break list of SCR-45 through the gateway-bff route, and prove that no file, no outbound item and no lake path is written.

**Feature flag.** `rwb.case.reconciliation-quality-v1`, read as a flag of the platform library; off means the Schedule starts no run, the read model answers nothing for the date and no result row is written.

**Done when.** The tests in section 16 pass, the contract test of the two fact reads stays green for the rwb-source-data reconciliation and the integration run, and a SIT week shows one run per business date, nine result rows per date, a HELD date on a break, a NOT_RUN date on a stale data product and a TRUSTED date after the rerun, no case, exclusion, queue, membership or assignment row changed by the run, and no extract file, outbound item, data set or lake path for any date.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-012 | A check breaks the tolerance | The case list for {date} does not reconcile to ACE for {product}: a difference of {variance} accounts, {pct} percent. |
| MSG-P1-001 | A data product is not loaded for the date; the run is not run | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-006 | A contract or the store is unavailable during the run | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | A role without the Platform administration right reads the run, the results or the facts | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | The token carries no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. |

The five texts are copied unchanged from the legacy story and the platform message catalog, and the placeholders are the values the tests of section 7 assert: the business date, the product group, the variance 1 and the percent 33.33 for MSG-P1-012, and "DP01 is from 2026-11-27" for MSG-P1-001. The legacy wording of MSG-P1-012 speaks of the case list, which is rwb-source-data's check; the text is kept because the legacy message set is kept, and the product group and the count of the case-side check fill the same placeholders.

### 15. Screens and states

No screen is built in this story. Existing surfaces show what it writes, through the gateway-bff composite route (DP-19):

| Surface | What it shows |
|---|---|
| SCR-44 Interface and job monitor | The quality run of the business date in the states Running, failed and complete, with the state TRUSTED, HELD or NOT_RUN, the three checks, the variance and the break count |
| SCR-45 Data quality | The results of the date with PASS, BREAK or not run and the reason, the break rows of each check with their table and column, and the case, queue and assignment facts of the date |
| The report "Reconciliation and data quality" (rwb-reporting) | Read-only for RW-BIANAL and the report readers: the case-side result of the date beside the enterprise reconciliation result that rwb-source-data publishes |
| The facts read of 12.1 | Read-only for the rwb-source-data service identity: the exclusion count of REC-01 and the case keys of REC-05, with the state of the run of the date |

The route merges the answers of this service with the case and the report; the screen field lists and the masking of customer fields belong to RWB-PLT-N001-CON and the edge stories, not here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-011-07 | AC10, BR14 | Component | RW-CASEOWN calls `GET /quality-results` and `GET /reconciliation-facts/2026-11-30`; refused with MSG-P4-002; no token is refused with MSG-P4-001 |
| TC-E1-011-01 | AC1, AC8, BR1, BR2, BR3, BR4, BR9 | End to end | 21 exclusion rows of 2026-11-30 (12 MORTGAGE, 6 HIRE_PURCHASE, 3 SSME), every key resolving and every owner a member of its queue; no extract file, no data set and no lake path |
| TC-E1-011-02 | AC2, BR1, BR6, BR7, BR10 | End to end | 3 SSME exclusion rows with one without a rule version; a variance of 1, 33.33 percent |
| TC-E1-011-03 | AC3, BR6 | Unit | Tolerance 0.10; 1 of 1,000 rows and 1 of 900 rows, 0.10 and 0.11 percent |
| TC-E1-011-04 | AC4, BR5, BR10 | End to end | No LOADED DP01 answer for 2026-11-30; the stale marker "DP01 is from 2026-11-27" |
| TC-E1-011-05 | AC5, BR8 | Component | Break on SSME, the rule version applied, the restart of the date |
| TC-E1-011-06 | AC6, BR8 | Component | Two runs for 2026-11-30 on two workers |
| TC-E1-011-08 | AC7, AC9, BR3, BR4, BR7, BR13 | End to end | person_key P0099881 absent from DP02 on case RW-2026-000140; owner U-1001 not a member of MTG-BKK-CO; case RW-2026-000151 with no queue |
| TC-E1-011-09 | AC4, BR5, BR12 | NFR | The rwb-source-data contract forced to fail after the first read; MSG-GEN-006 naming the system; the rerun writes all nine rows |

The nine legacy test cases of the key are kept with their legacy IDs and their legacy Given, When and Then, and are run on the fixtures of this slice; the level column is the mapping of section R7.2 of Template and Rules, where the legacy level System maps to End to end on the run, to Component where the case is asserted on the operations of this service against seeded `rwb_case` rows and the fakes, to Unit where the comparator is proved without a database, and to NFR where the assertion is the failure and recovery of a consumed contract. TC-E1-011-07 has no acceptance criterion of its own in the legacy table; it is carried as the access row of this story and covers AC10 here. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the tolerance, the check names, the state names, the alert groups and the cron are configuration or parameters read with a version; the product groups, the exclusion reasons, the queue codes and the result values are reference data.
- No personal data in logs, tables, tests or prompts: the run, the results and the break rows carry a case number, a product group, a queue code, a team code, an owner identifier, an account key, a person key, a business date, counts, a variance, a percent and a reason only; no name, address, contact value or identity number is read or written.
- ACE data only through the owner's contract: the freshness answer and the DP01 and DP02 rows arrive through the rwb-source-data contract, and this service holds no grant on any `recovery.v_ace_*` view and opens no ACE table (DP-05).
- No read of another service's tables and no cross-schema join: `reconciliation_result` and `case_list_row` stay rwb-source-data's and are not read here, the treatment and payment rows are their owners', and the report is rwb-reporting's (DP-01).
- No data lake and no extract: no INT-19 adapter, no outbound item, no extract file, no data set and no lake path is written or read for any date, and the boundary test fails the build if a lake path appears (DP-17).
- The facts of a date leave this service only through the two fact reads of 12.1; no reader is given a table, a view or a copy (BR9).
- The run is Schedule-started only: no event starts it and no Kafka record is published by it, because DP-09 is not in this story's pattern set.
- Every consumed call is one hop with a 2 s budget, one GET retry with jitter and a breaker per downstream; no call chain.
- A break never changes a case, an exclusion, a queue, a membership, an assignment or an ACE row; the rerun through the workflow is the only path that replaces the rows of a date.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-007 | The case list reconciles daily to the count of accounts in v_ace_account with no variance, and every business key on a Workbench table resolves to an ACE row | Epic 1, 3.1; Program, 5.1 | FEAT-RDF-11, FEAT-RDF-13 | All recovery processes | REC-01; REC-05; CTL-01; R-UNI-40 | TC-E1-011-01, TC-E1-011-02, TC-E1-011-07, TC-E1-011-08 |
| REQ-RDF-008 | Data quality checks run in ACE ingestion; the Workbench reports reconciliation breaks, referential completeness and its quality measures, each break with a reason visible to the data product owner | Epic 1, 3.1 and 3.8; Program, 5.1 | FEAT-RDF-12, FEAT-RPT-09 | 15 Manage performance, data and AI | REC-01; REC-05; CTL-01 | TC-E1-011-02, TC-E1-011-03, TC-E1-011-04, TC-E1-011-05, TC-E1-011-09 |
| REQ-CWC-004 | Exclusion rules for deceased, fraud, bankruptcy, an active restructure plan and an open dispute are held as data and applied at creation | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-05 | 6.1 Take over the case at 90 days past due | REC-01; CTL-01 | TC-E1-011-01, TC-E1-011-02 |

| Item | What it covers in this story |
|---|---|
| Legacy key RWB-E1-011 | The case, queue and assignment slice of the reconciliation and of its data quality report; no legacy AC owned here, since AC1 to AC8 belong to RWB-P1-E1011-APP and RWB-ITG-E1011-ITG |
| The enterprise case-list reconciliation | rwb-source-data's JOB-04 workflow, its `reconciliation_result` rows, REC-02, REC-03, REC-04, the account count and balance of REC-01, the case-list publish status and REC-05 over P1's own tables (RWB-P1-E1011-APP) |
| RWB-ITG-E1011-ITG | The end-to-end proof of JOB-04 across the wave-1 services, which reads `GET /reconciliation-facts/keys` of this service for the case side of REC-05 |
| The P1 tables | `reconciliation_result` and `case_list_row` are P1's and are never written or read as a table here |
| The P9 reporting model | Reads the quality facts of 12.1 and the business events of the date; no event of this story feeds it |
| The lake removal | The two legacy extracts, the lake path, the previous released lake date and the Power BI data set are dropped (DP-17, ADR-018) |
| The job monitor | SCR-44 shows the run of the date with its state and its three checks |
| DP-01 | The case, exclusion, queue, membership, assignment and quality tables live in `rwb_case`; no table of another service is read |
| DP-02 | The rwb-case login runs the workflow and reads the two contracts |
| DP-03 | The decision record is written through the library where a rule decides the handling of a break |
| DP-05 | The freshness answer and the data-product rows arrive through the rwb-source-data contract; no ACE view is read |
| DP-06 | The tolerance is a parameter with a version, read through the parameters contract of this service |
| DP-07 | The product groups, exclusion reasons, queue codes and result values are reference data with a version |
| DP-10 | The run is a Temporal Schedule plus a workflow, not a Quartz row |
| DP-11 | Two consumed operations and two fact reads, one hop and 2 s each |
| DP-14 | The topic name comes from the naming library; this story publishes no event |
| DP-15 | The three tables arrive in the per-service Flyway sequence |
| DP-17 | The data lake, the two extracts and the data set are removed, and the facts are served from the read model |
| DP-19 | SCR-44, SCR-45 and the report are reached through the gateway-bff composite route |
| ADR-013 | 19 services inside ACE: the case quality run lives in rwb-case |
| ADR-014 | Schema and login per service: `rwb_case` and the rwb-case login |
| ADR-018 | No data lake; the reporting read model is fed from the services |
| ADR-020 | Contract-first REST, one hop and 2 s on every consumed row |
| ADR-021 | Per-service Flyway and migration ownership of the three tables |
| Gaps and assumptions | GAP-0740; ASM-1343 to ASM-1354 |

### 19. Out of scope

- The enterprise reconciliation of the case list to ACE, its REC-01 account count and balance, REC-02, REC-03, REC-04, its `reconciliation_result` rows, the case-list publish status and REC-05 over its own tables: `RWB-P1-E1011-APP`, `RWB-P1-E1011-CON` and `RWB-P1-E1011-OPS`.
- The end-to-end proof of JOB-04 across the wave-1 services, including the read of the two fact reads of this service: `RWB-ITG-E1011-ITG`.
- The asset keys of rwb-asset for the REC-05 resolution: `RWB-S5-E1011-APP`. The notice keys and the notice barcode check of rwb-comms: `RWB-P6-E1011-APP`.
- The exclusion rules themselves and their application at case creation, which write `case_entry_exclusion`: the case creation story of this service and the reference-data story of this service. This story reads those rows and reports on them.
- The queue measure snapshot, its reconciliation to the case list and the message MSG-P3-029: RWB-P3-E1030-APP. This story reads `queue` and `queue_member` for its own reference check and writes no snapshot.
- The uniqueness measure "one case per customer per product" and the timeliness measure of the ACE batch: the case creation rule of this service and the freshness answer of rwb-source-data (FSD P1 v3 A2.12); this run reports neither.
- The other legacy reconciliations REC-06 (write-offs), REC-07 (assets taken on), REC-08 (the decision log copy) and REC-09 (notice barcodes): not in this slice.
- The data quality console SCR-45 and the quality measure definitions of the reporting module (Epic 2 and Epic 8); this story only writes the rows those surfaces read.
- The reporting model of rwb-reporting: its measure definitions, its snapshots, its steering dashboard and its refresh time, and the question of whether it reads the quality facts of this service or receives a quality event in wave 2 (GAP-0740; ASM-1347).
- Any data lake, lake copy, INT-19 adapter or INT-20 extract: removed from the target under DP-17, so none is built, migrated, provisioned or tested here.
- The platform job monitor and its alerting beyond the read-only SCR-44 answer of this run, and the deployment, the Schedule registration, the dashboards, the alerts and the runbook of this run: the platform observability epic and the OPS slice of this legacy key.
- Working a break to closure with an owner and a date: FEAT-RPT-09 full scope, Epic 2.
- The report of the date itself and the reading of it by the report users: rwb-reporting and RWB-ITG-E1011-ITG.
