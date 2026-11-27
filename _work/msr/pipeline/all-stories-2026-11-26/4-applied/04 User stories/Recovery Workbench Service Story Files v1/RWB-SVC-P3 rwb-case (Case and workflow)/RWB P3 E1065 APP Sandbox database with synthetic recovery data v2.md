# RWB-P3-E1065-APP Sandbox database with synthetic recovery data

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1065-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-065 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP07, DP13, DP15, DP19 |
| Parallel lane | L-P3-T |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P1-E1065-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (no FR mapped to REQ-RDF-001, REQ-RDF-010) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-065 for rwb-case, carrying the case, queue, task, timer and reference estate of the DEV sandbox. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P3-E1065-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tribe lead and squad member (RW-TRIBE)** I want **the DEV sandbox to stand up `rwb_case` from the same per-service migration as SIT, with 2,812 synthetic cases across MORTGAGE, HIRE_PURCHASE and SSME, their accounts and parties linked by business key, the queues, members and assignments, the open task and the timers of every active case, the exception shapes the rules must handle and the reference rows at the version in force**, so that **every squad can build and test the case list, the case record, the allocation and the timers from the first day, before any ACE interface is available and with no production data**.

This story is the rwb-case part of legacy RWB-E1-065: the case estate of the DEV sandbox. The DEV database `rwb_sandbox`, the ACE-shaped test double with the 22 Tier 1 and 14 Tier 2 tables, the 30 `v_ace_*` views, the dictionary-driven value factory, the verifier of the whole sandbox, the pipeline stage, the rename and the read-only grant on schema `recovery` belong to RWB-P1-E1065-CON, RWB-P1-E1065-APP and RWB-P1-E1065-DB. What this slice owns is what answers for `rwb_case`: the synthetic cases with their case numbers, product groups, statuses and total outstanding at entry, the links to their ACE accounts and customers as business keys, the queues, members, assignments, the one open task and the timers per active case, the exception shapes of legacy BR4 that live in the case tables, the reference rows of the case module at the version in force, and the DEV read-only role's read of the schema.

rwb-case holds the case, the state, the queue, the owner and the clock (Architecture v5 slide 3, step 2 and step 6; slide 10), and its tables are the owner's own schema (slide 20; DP-01). A squad cannot see a case list, a queue, an owner or a service level in DEV until those rows exist, so the estate is only usable if it is written in `rwb_case` and not in a shared fixture. The volumes, the seed and the exception shapes are the ones the legacy story fixes: seed 20261128, 1,226 Mortgage, 1,296 Hire purchase and 290 SSME cases (10 percent of the 30 June 2026 inventory; DL15), 10 cases for each exception shape (legacy BR4), and accounts at 89 and at 90 days past due (DL16).

### 2. Business rationale

SIT reads the real ACE database; DEV has none. Without a seeded case estate, no squad can open the case list, see an owner and a queue, read a service level or test an allocation rule before SIT is connected: the tables are empty, the case list returns nothing and every case story would ask another team for a fixture. The legacy story builds a sandbox in DEV from the same DDL as SIT and fills it with synthetic rows; its AC1 fixes the case sentence — case "RW-2026-000001" has its accounts, parties, interactions and documents linked — its AC2 runs the product-group count over `recovery.recovery_case`, its AC5 fixes the total outstanding of that case at 1,845,200.00 and its AC8 fixes the 89 and 90 days past due boundary.

This story is the rwb-case part of that story; the primary slice is the rwb-source-data contract of the same key. The database, the ACE test double, the views, the generator, the verifier and the pipeline are not here. What is here is the estate that answers for this service: the cases, their links, the queue and owner structure, the tasks and the timers, the exception shapes of the case tables, the reference rows and the DEV read of the schema. It serves REQ-RDF-001 (each data product reachable in DEV without a request to another team) and REQ-RDF-010 (access per data product by role, personal data masked): the seed writes no personal value and no clear identity number, because an identity number lives only in the ACE-shaped tables of RWB-P1-E1065-CON (legacy BR9).

The queue codes, the product groups, the statuses, the reasons and the timer offsets are reference rows of `rwb_case` with a version and a valid-from date, never constants (DP-07; BR-P3-006). A new table version or a new queue therefore reaches the sandbox with a load, not with a release.

### 3. Preconditions

- The `rwb_case` baseline is in place: `recovery_case`, `case_account`, `case_party`, `case_entry_exclusion`, `queue`, `queue_member`, `queue_measure`, `assignment`, `task`, `timer`, `lov_value`, `reference_row`, `reference_version`, `parameter_catalog` and `parameter_value` exist with the standard record columns, at the platform migration version of DP-15.
- RWB-P1-E1065-CON is published: the rwb-source-data contract of this legacy key, which fixes the DEV sandbox build, the database name `rwb_sandbox`, the seed value `20261128`, the order in which the per-service migrations run after the sandbox build, the case list of the seed with its account keys and person keys, the boundary accounts at 89 and 90 days past due and the exception shapes (DP-11, C dependency). Its operation names and payload field lists are those it publishes and are not restated here.
- The case numbers of the seed follow the format of FSD P3 A2.1 (RW-YYYY-NNNNNN), and the seed starts at "RW-2026-000001"; the case creation story RWB-P3-E1018-APP issues a number in a running environment and this seed writes its rows directly.
- The queue rows are the 12 queues and 48 member rows of FSD P3 AC-P3-006-01 at table version 1 with valid from 2026-11-30, including "LIT-BKK-OFF" with team "LIT-BKK" and role RW-LITOFF, "TDR-BKK-CO" and its overflow queue "TDR-BKK-OVF", and capacity 40 for member U-11. The case for MORTGAGE in BKK goes to "MTG-BKK-CO" under ALLOC-014 (Temporal slide 4).
- The exclusion reason codes are those of the FSD P3 A2.5.3.2 shapes — deceased, fraud, bankruptcy, active plan and open dispute — and the exclusion rule version in force is "EXCL-2026.11" (FSD P3 AC-ALT-P3-001-01). The rule package itself belongs to rwb-decision (P7); this seed writes the reason code and the version on the row and evaluates no rule.
- The lists the seed validates against are rows of `lov_value` of this service at the version in force, including LOV-PRODUCT (MORTGAGE, HIRE_PURCHASE, SSME, UNSECURED), LOV-CASE-STATUS, LOV-STAGE and LOV-ROUTE (FSD P3 A2.6.3.2).
- The DEV-only read-only role is the legacy `rwb_sandbox_read`; the rwb-case login is the rwb-case login (DP-02). Both names for the target schema are Not specified in the source documents (GAP-2251; ASM-3709).
- The number of tasks and timers per synthetic case beyond one open task and one active timer, and the timer offsets of the seeded rows beyond the FSD P3 AC-ALT-P3-011 offsets, are Not specified in the source documents (GAP-2249; ASM-3707).
- The distribution of the 2,812 cases across the 12 queues and the 48 members is Not specified in the source documents (GAP-2250; ASM-3708).
- The field identifiers of `queue`, `queue_member`, `assignment`, `task`, `timer` and `reference_version` are Not specified in the source documents read, because legacy section 11 lists field ranges for the case, party, account, deviation, document, interaction and reference tables only (GAP-2251; ASM-3709).
- The seed reads no `v_ace_*` view, no `public` table and no table of another service (DP-05 applies as a prohibition) and evaluates no Drools rule (DP-04 applies as a prohibition).
- The parameter defaults arrive with the migrations of RWB-P3-E1042-APP: this story writes no row of `parameter_catalog` or `parameter_value`.
- The case list, the case record, the allocation, the transfer, the timers and the rebalancing are other stories of this service (RWB-P3-E1018-APP, RWB-P3-E1023-APP, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1028-APP, RWB-P3-E1030-APP); this story seeds the rows they read and changes none of them.

### 4. Flow

1. The sandbox build of RWB-P1-E1065-CON creates the DEV database `rwb_sandbox`, applies the ACE-shaped test double and the per-service migrations in order, and reaches the `rwb_case` step with the baseline in place and the case tables empty.
2. The rwb-case migration `V1065_1__case_estate_seed.sql` writes the reference estate in one transaction: the LOV rows of LOV-PRODUCT, LOV-CASE-STATUS, LOV-STAGE and LOV-ROUTE at table version 1 with valid_from 30 November 2026, one `reference_version` row per table version with the author, the approver and the approval time of the seeded test identities, and one `reference_row` per row it writes.
3. ReferenceEstateSeeder checks the written rows against the seed file: every product group, status, stage and route is a list value, exactly one table version is in force, and no code, list value or queue code appears in the Java source of the seed.
4. QueueEstateSeeder writes the 12 `queue` rows of FSD P3 AC-P3-006-01 with their codes, team codes, role codes and overflow queue, and the 48 `queue_member` rows with their capacity.
5. CaseEstateSeeder reads the case list of the RWB-P1-E1065-CON fixture and writes one `recovery_case` row per case: case number, product group, status, entry date, `primary_person_key` and `total_outstanding_at_entry`, distributed by product group as 1,226 MORTGAGE, 1,296 HIRE_PURCHASE and 290 SSME, with the case "RW-2026-000001" of the fixture carrying 1,845,200.00.
6. CaseLinkSeeder writes `case_account` and `case_party` for every case from the account keys and person keys of the fixture: one primary account row and one BORROWER party row per case, and the extra rows of the shapes that carry them.
7. AssignmentSeeder writes one open `assignment` per case with its queue and its owner, taken from the queue rows and the member rows, names the allocation rule ID "ALLOC-014" and its version, and keeps every member at or under the caseload cap of 40 open cases.
8. TaskTimerSeeder writes one open `task` per active case with its task code, its role and its due date, and one active `timer` per active case; the case "RW-2026-000001" carries the SLA timer with the warn on day 7 and the breach on day 8 escalating to RW-TEAMMGR under R-UNI-30, and a prescription timer whose warning falls 6 months before its legal deadline.
9. ExceptionShapeSeeder writes 10 cases for each shape of legacy BR4 into the case tables: the duplicate case for one customer and product, the deceased customer, the bankruptcy, the open deviation, the legal hold, the unmapped product code, the collateral with no account, the case with three accounts, the accounts at 89 and 90 days past due and the withdrawn consent; the exclusion shapes also write their `case_entry_exclusion` row with the reason code, the rule ID and the version "EXCL-2026.11".
10. DecisionRecordSeeder writes one local decision record per seeded exclusion entry and one for case "RW-2026-000001" through the decision-record library of DP-03, first in the transaction, so the case timeline and the decision query are demonstrable in DEV; the decision code of a seeded entry is Not specified in the source documents (GAP-2252; ASM-3710) and the story uses the code of the case story that owns the action, while the entries themselves stay in `rwb_case` because no relay runs.
11. CaseSeedVerifier reads the whole estate back: the count per product group, one primary account and one BORROWER party per case, one assignment, one open task and one active timer per active case, the 10 rows per exception shape, the boundary cases, one table version per reference table, every reason code in its list, and the row count per table; a failure fails the build and the previous sandbox stays in use.
12. The build grants the DEV-only read-only role `rwb_sandbox_read` SELECT on schema `rwb_case` and publishes the build result with the row count per table; the DEV service serves the seeded estate through the P3 reads of section 12.1.
13. The DEV sandbox has no Kafka broker, so no relay runs and no event leaves it: the synthetic cases announce no CaseCreated, CaseAllocated or TimerBreached, and a squad that needs a case event uses the SIT environment built by RWB-ITG-E1065-ITG.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A reference row names a product group, status, stage or route that is not a list value | The build fails naming the table, the row and the value; the previous sandbox stays in use | None (pipeline result) | AC5 |
| X2 | A case row names a product group outside LOV-PRODUCT, or two table versions are in force | The build fails naming the case and the value; no sandbox is published from that build | None (pipeline result) | AC4, AC5 |
| X3 | A case key of the seed is absent from the fixture's case list, or an account key or person key of a case is absent from it | The build fails naming the case and the key; no link is written for a key the fixture does not hold | None (pipeline result) | AC2, AC7 |
| X4 | An owner would hold more open cases than the caseload cap | The build fails naming the member and the count; the seed never exceeds the cap | None (pipeline result) | AC3 |
| X5 | A case has no assignment, no open task or no active timer while its status is open | The build fails naming the case and the missing row | None (pipeline result) | AC6 |
| X6 | A seed row is written into `public`, into a `v_ace_*` view or into another service's schema | The build fails naming the object; the seed writes only schema `rwb_case` | None (pipeline result) | AC9 |
| X7 | The same seed value and the same fixture run twice on a rebuilt database | The same cases, links, queues, assignments, tasks and timers are written, with no row of the previous build left | None | AC7 |
| X8 | A reader holding `rwb_sandbox_read` tries to change a seeded row | The write is refused by the database; the row is unchanged | None (database error) | AC8 |
| X9 | A role without Case record R calls the DEV case list, or a case outside its scope is read | Refused before any seeded row is read | MSG-P4-002; MSG-P4-003 | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the `rwb_case` baseline and the published RWB-P1-E1065-CON fixture. It reads no ACE view, calls no other service at run time and adds no build dependency of its own |
| Negotiable | The case-to-queue distribution, the task and timer counts per case, the login name and the field identifiers are parameters, rows or assumptions; the volumes, the seed, the boundary and the shapes are fixed |
| Valuable | Every squad sees a full case list, a queue structure, an owner, a service level and the exception shapes in DEV from Day 1, with no production data |
| Estimable | One migration, one repeatable companion, seven seeders, one verifier and one grant script |
| Small | Fits one sprint with its tests, as a secondary slice of the legacy key |
| Testable | Every criterion in section 7 is one automated test over the seeded schema, with the case list and the reference rows stubbed |

### 7. Acceptance criteria

```gherkin
Feature: Sandbox database with synthetic recovery data — the rwb-case estate

  Background:
    Given the sandbox build uses seed 20261128
    Given the rwb-source-data contract mock returns the DEV sandbox build result for seed 20261128 with database "rwb_sandbox", schema "rwb_case" after the baseline and the per-service migration order
    Given the rwb-source-data contract mock returns the case list of the seed with case "RW-2026-000001", the 2,812 synthetic cases plus 10 cases for each exception shape, and the 10 boundary accounts at 89 and the 10 at 90 days past due with their account keys and person keys
    Given the reference rows of the seed name the exclusion rule version "EXCL-2026.11" and the allocation rule "ALLOC-014"

  Scenario: AC1 The case estate loads at the seed volumes (new, D-RCV-60)
    When the rwb-case migration runs in schema "rwb_case" after the baseline
    Then "recovery_case" holds 2,812 cases: 1,226 MORTGAGE, 1,296 HIRE_PURCHASE and 290 SSME
    And "SELECT product_group, count(*) FROM rwb_case.recovery_case GROUP BY product_group" returns exactly those three groups with those counts
    And every case number matches RW-YYYY-NNNNNN and no number is used twice
    And case "RW-2026-000001" exists with its product group, its entry date and total_outstanding_at_entry 1,845,200.00
    And every case names a primary_person_key of the fixture and no case number exists that the fixture does not hold

  Scenario: AC2 Every case is linked to its accounts and parties by business key (new, D-RCV-60)
    Given the fixture returns case "RW-2026-000001" with its account keys and its person keys
    When the link seeder writes "case_account" and "case_party"
    Then each "case_account" row holds its account_key from the fixture with its primary flag, and each "case_party" row its person_key with the role code BORROWER
    And "recovery_case.primary_person_key" equals the person key of the fixture for every case
    And the account keys of "case_account" of a case are exactly the account keys the fixture links to it
    And no column of "rwb_case" holds a foreign key into "public" or into another schema

  Scenario: AC3 Queues, members and one assignment per case (new, D-RCV-60)
    Given the queue rows of the seed at table version 1 with valid from 30 November 2026
    When the queue and assignment seeders run
    Then "queue" holds 12 rows with their queue code, their team code and the role that works them, and "LIT-BKK-OFF" names team "LIT-BKK" and role RW-LITOFF
    And "queue_member" holds 48 rows, and member "U-11" of "TDR-BKK-CO" carries capacity 40
    And "TDR-BKK-OVF" exists as the overflow queue of "TDR-BKK-CO"
    And every case holds exactly one open "assignment" with its queue and its owner, and the assignment names the rule ID "ALLOC-014" and its version
    And no member holds more than 40 open cases

  Scenario: AC4 The exception shapes the rules must handle (new, D-RCV-60)
    Given the fixture returns 10 cases for each shape: duplicate case for one customer and product, deceased customer, bankruptcy, open deviation, legal hold, unmapped product code, collateral with no account, case with three accounts, accounts at 89 and at 90 days past due, and withdrawn consent
    When the exception shape seeder runs
    Then exactly 10 cases exist for each shape and each shape is identifiable from its own rows
    And each exclusion shape holds its "case_entry_exclusion" row with its account_key, its reason code, its rule ID and the version "EXCL-2026.11"
    And the three-account shape holds 3 "case_account" rows and the duplicate shape holds 2 cases for the same person key and product group
    And each of the 10 accounts at 90 days past due holds one open case and each of the 10 at 89 days past due holds none
    And no case carries a product group outside LOV-PRODUCT

  Scenario: AC5 The reference estate is in force at one version (new, D-RCV-60)
    Given the seed file of table version 1 with valid from 30 November 2026
    When the reference seeder runs
    Then "lov_value" holds LOV-PRODUCT with MORTGAGE, HIRE_PURCHASE, SSME and UNSECURED, and LOV-CASE-STATUS, LOV-STAGE and LOV-ROUTE with the values of the seed file
    And "reference_version" holds one row per table version with valid_from 30 November 2026, the author, the approver and the approval time of the seeded test identities of RWB-P4-E1065-APP
    And exactly one table version is in force per reference table
    And no product group code, status code, stage code, route code, reason code, queue code or rule ID appears in the Java source of the seed

  Scenario: AC6 Every active case carries its task and its timers (new, D-RCV-60)
    When the task and timer seeder runs
    Then every case whose status is open holds exactly one open "task" with its task code, its role and its due date, and at least one active "timer"
    And case "RW-2026-000001" holds the SLA timer with the warning on day 7 and the breach on day 8 escalating to RW-TEAMMGR under R-UNI-30
    And it holds a prescription timer whose warning falls 6 months before its legal deadline
    And no timer row holds a state the seed did not write, because the seed starts no clock and fires nothing
    And every task role and every escalation target is a role the reference rows hold

  Scenario: AC7 The rebuild is idempotent (new, D-RCV-60)
    Given schema "rwb_case" holds the estate for commit "a1b2c3d" and seed 20261128
    When the same migration and the same seed value run again in a rebuilt database
    Then the case count per product group is 1,226 MORTGAGE, 1,296 HIRE_PURCHASE and 290 SSME
    And case "RW-2026-000001" holds the same total_outstanding_at_entry 1,845,200.00
    And the counts of "case_account", "case_party", "queue", "queue_member", "assignment", "task" and "timer" are the same
    And no row of the previous build remains

  Scenario: AC8 The DEV read-only role reads the estate and cannot change it (new, D-RCV-60)
    Given the DEV-only read-only role "rwb_sandbox_read" over the sandbox
    When a member of that role runs the product-group query of AC1 and then an UPDATE on a row of "recovery_case"
    Then the read returns MORTGAGE, HIRE_PURCHASE and SSME with the counts of AC1
    And the same role reads "case_account", "case_party", "queue", "queue_member", "task" and "timer"
    And the UPDATE is refused by the database and the row is unchanged

  Scenario: AC9 The seed writes only rwb_case and no event leaves the sandbox (new, D-RCV-60)
    Given the DEV profile runs with no Kafka broker and no outbox relay
    When the migration and the seeders run
    Then every write lands in schema "rwb_case"
    And no "public" table, no "v_ace_*" view row and no table of another service is written
    And no CaseCreated, CaseAllocated or TimerBreached event is produced and no "outbox_event" row is written
    And one local decision record per seeded exclusion entry and one for case "RW-2026-000001" are written and stay in "rwb_case"
```

The nine criteria above are new and test only this deliverable: the case, queue, task, timer and reference estate of the DEV sandbox. No legacy criterion text is copied here. The legacy criteria AC1 to AC9 of RWB-E1-065 are owned elsewhere — the schema, the dictionary, the views, the generator, the verifier and the pipeline by RWB-P1-E1065-CON and RWB-P1-E1065-APP; the roles, the permission matrix and the test identities by RWB-P4-E1065-APP; the document estate by RWB-P5-E1065-APP. Three legacy lines are answered here: the case sentence of legacy AC1, the product-group count of legacy AC2 now run on `rwb_case.recovery_case`, and the 1,845,200.00 of legacy AC5.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | No production data in DEV: the sandbox holds synthetic cases, synthetic names, synthetic keys and synthetic reference rows only (legacy BR1) | NFR-045; CTL-11; legacy BR1 |
| BR2 | The sandbox is built from the same DDL as SIT: here the per-service migration of `rwb_case`, applied after the baseline and inside the build order of RWB-P1-E1065-CON (legacy BR2) | Legacy RWB-E1-065 BR2; DP-15 |
| BR3 | Values come from the data dictionary and the lists of values, never from code: product groups, statuses, stages, routes, queue codes, reason codes and timer offsets are rows or list values (legacy BR3) | sys_fields; lov_value; Principle 1; BR-P3-006 |
| BR4 | Case volumes follow the product split of the 30 June 2026 inventory at 10 percent: 1,226 MORTGAGE, 1,296 HIRE_PURCHASE and 290 SSME (legacy BR5) | DL15; legacy BR5 |
| BR5 | The exception shapes are generated, 10 cases each: duplicate case for one customer and product (R-UNI-17), deceased (R-UNI-05), bankruptcy (R-UNI-07), open deviation, legal hold (R-UNI-20), unmapped product code, collateral with no account, case with three accounts, accounts at 89 and 90 days past due (DL16), withdrawn consent (R-UNI-10) (legacy BR4) | rules.txt; DL16; legacy BR4 |
| BR6 | Every case carries one queue and one owner from the queue rows, and no owner exceeds the caseload cap; a case with no matching allocation rule states its overflow queue | FSD P3 A2.7, A2.8, A2.9; FEAT-CWC-07, 08, 09; DL22 |
| BR7 | Every active case carries one open task and one active timer, and the SLA timer escalates to the named role under R-UNI-30 without moving the case | FSD P3 A2.11, A2.13; FEAT-CWC-11, 13; Temporal slide 4 |
| BR8 | Every role has a test identity before it has real users (legacy BR6); the identities themselves are rows of RWB-P4-E1065-APP and this seed writes no role row and no user row | DL39; legacy BR6 |
| BR9 | There is no copy and no load table, and no clear identity number outside the ACE-shaped tables: `rwb_case` holds business keys and synthetic values only (legacy BR8, BR9) | D-RCV-35; ADR-010; CTL-11; legacy BR8, BR9 |

BR2 to BR7 are the case-specific reading of the legacy rules. BR3 is enforced twice: the seed reads every code from the seed file and the reference rows, and the verifier fails a row outside its list. BR6 and BR7 turn the queue table, the member cap and the timer table into behaviour on every seeded row, so a squad sees an owner, a cap and a service level without any engine running. BR8 keeps the identities out of this schema: the seed names roles and test identities as values, and the role and permission rows stay with RWB-P4-E1065-APP.

### 9. State transitions

No case status change: the seed writes the status each row holds and moves nothing afterwards.

| From | Event | Condition | To |
|---|---|---|---|
| no sandbox in DEV | the sandbox build of RWB-P1-E1065-CON starts | A merge to main that changes the ACE DDL, a recovery migration or the dictionary, or a manual start | Building |
| Building | the migrations and the seeders finish and the verifier passes | Every check of section 4 step 11 passes | Published |
| Building | a seeder or the verifier fails | A reference row, a link key, an assignment, a task, a timer or a shape fails its check | Failed, and the previous sandbox stays in use |
| Published | the next build is published | The same database is renamed for the new build | Published with the rows of the new build only |

| Object | State the seed writes | Note |
|---|---|---|
| recovery_case | NEW for a case of the entry shape, ASSIGNED for a case with an owner, OPEN_UNASSIGNED-equivalent of LOV-CASE-STATUS only where the shape says so | LOV-CASE-STATUS values as rows of the seed file; no move is made by this story |
| assignment | OPEN | One row per case, with the queue, the owner, the rule ID and the version |
| task | OPEN | One row per active case, with its role and due date |
| timer | ACTIVE | One row per active case; the state is written, never reached by a clock |

The sandbox build state is moved by the pipeline of RWB-P1-E1065-CON, never by the service; the case, assignment, task and timer states are rows this seed writes and the engines of RWB-P3-E1018-APP, RWB-P3-E1020-APP and RWB-P3-E1028-APP move them in a running environment.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-case service identity (the rwb-case login, DP-02) | Runs the migration and the seeders, reads and writes the twelve tables of `rwb_case` it seeds, writes the local decision records and serves the seeded rows through the P3 reads |
| RW-TRIBE, tribe lead and squad members | Read and extract the sandbox through `rwb_sandbox_read`, and open a seeded case, its tasks and its timers through the DEV service |
| RW-PLATADM, platform administrator | Owns the sandbox database and the pipeline stage that calls this migration; owns the DEV grant and the retirement of the read-only role |
| RW-CASEOWN, case owner | Opens the seeded cases of the estate through the case record and the case list in DEV, with the rights of the role |
| RW-TEAMMGR, team manager | Reads the queues, the owners and the escalations of the seeded estate, the escalation target of the SLA timer under R-UNI-30 |
| RW-REFADM, reference data administrator | Prepares and approves the table version the sandbox mirrors; in the sandbox the same rows are written by the migration and no approval is taken in DEV |
| Test identities per role | Call the DEV service against the seeded estate with their role's rights, as RWB-P4-E1065-APP seeds them |
| ACE team lead and ACE DBA | Own the DDL of the ACE-shaped test double and the 14 Tier 2 tables; that DDL is used by RWB-P1-E1065-CON and is not written, read or changed here |

The per-service login name and the DEV-only read-only role are Not specified in the source documents for the target schema (GAP-2251; ASM-3709); the story keeps the legacy name `rwb_sandbox_read` and "the rwb-case login (DP-02)". The refusal shapes a role meets are MSG-P4-002 when the role holds no Case record right and MSG-P4-003 when the case is outside the caller's scope; both are answered by rwb-access and the guard the service template wires, not by the seed. No identity of this story may change a seeded row, and the role rows and capability letters are rows of RWB-P4-E1065-APP, not of `rwb_case`.

### 11. Data

| BR Field ID | Entity in `rwb_case` | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023, DF-CAS-046 to DF-CAS-055 | recovery_case | all 33 fields: case number, product group, status, stage, route, owner, primary person key, entry date, total outstanding at entry | Write (seed), then Read |
| DF-CAS-024 to DF-CAS-029 | case_account | account key, primary flag and the remaining fields of the range | Write (seed), then Read |
| DF-CAS-030 to DF-CAS-035 | case_party | person key, role code and the remaining fields of the range | Write (seed), then Read |
| Not specified in the source documents (GAP-2251; ASM-3709) | case_entry_exclusion | account key, reason code, rule ID, rule version, excluded at | Write (seed), then Read |
| Not specified in the source documents (GAP-2251; ASM-3709) | queue | queue code, team code, role code, overflow queue, table version, valid from | Write (seed), then Read |
| Not specified in the source documents (GAP-2251; ASM-3709) | queue_member | queue code, member identity, capacity | Write (seed), then Read |
| Not specified in the source documents (GAP-2251; ASM-3709) | assignment | case, queue, owner, rule ID, rule version, state, assigned at | Write (seed), then Read |
| Not specified in the source documents (GAP-2251; ASM-3709) | task | case, task code, role code, due date, state | Write (seed), then Read |
| Not specified in the source documents (GAP-2251; ASM-3709) | timer | case, timer code, due at, escalation role, state | Write (seed), then Read |
| DF-REF-027, DF-REF-028, DF-REF-029 | lov_value | id, lov_code, value_code | Write (seed), then Read |
| Not specified in the source documents (GAP-2251; ASM-3709) | reference_row | the row of each reference table it mirrors | Write (seed), then Read |
| Not specified in the source documents (GAP-2251; ASM-3709) | reference_version | table code, version, valid from, author, approver, approval time | Write (seed), then Read |
| DF-DEC-001 to DF-DEC-018, DF-DEC-028 to DF-DEC-031 | local decision record | decision code, actor, case, actions, decided at, chain sequence and hash link | Write |
| DF-REF-132 to DF-REF-158 | parameter_catalog, parameter_value | the parameter entries and their values | Not written by this story; Read only where the estate needs a parameter |

The seed writes the twelve tables it owns and the local decision records, and nothing else: no case of another service, no ACE row, no role row, no `permission` row, no `queue_measure` row and no parameter row is written here. `queue_measure` is computed by the rebalancing job of RWB-P3-E1030-APP; `parameter_catalog` and `parameter_value` arrive with the migrations of RWB-P3-E1042-APP. The ACE-shaped tables and the 30 `v_ace_*` views belong to RWB-P1-E1065-CON and are never written by this slice: the seed takes the case list, the account keys, the person keys and the boundary accounts from the contract fixture. Field identifiers are those of the Logical Data Model and Data Dictionary v9; the ranges above are the ones legacy section 11 states, and a table it does not name carries its field identifiers from that model at implementation (GAP-2251; ASM-3709).

### 12. Contract

#### 12.1 REST operations provided

None at run time. The seed is a migration and the estate is read with SQL; the reads a squad uses in DEV are SQL through `rwb_sandbox_read` and the DEV service. The DEV service serves the seeded estate through the P3 reads on the base `/api/recovery/case/v1` (DP-13) and this slice adds no path, no query parameter and no response field:

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/cases` | List the seeded cases of the caller's scope with product group, stage, owner, queue and age | Case record R, scope applied | Not applicable |
| GET | `/cases/{caseId}` | Read a seeded case with its status, stage, owner, queue, entry date and total outstanding | Case record R, scope applied | Not applicable |
| GET | `/cases/{caseId}/accounts` | Read the seeded `case_account` rows with their account keys and primary flag | Case record R, scope applied | Not applicable |
| GET | `/cases/{caseId}/parties` | Read the seeded `case_party` rows with their person keys and role codes | Case record R, scope applied | Not applicable |
| GET | `/cases/{caseId}/timers` | Read the seeded stage and prescription timers with their due dates and escalation role | Case record R, scope applied | Not applicable |
| GET | `/cases/{caseId}/timeline` | Read the seeded decision records of the case on its timeline | Case record R, scope applied | Not applicable |
| GET | `/me/tasks` | Read the open tasks the seed wrote for the caller's role | Case record R, scope applied | Not applicable |
| GET | `/queues` | Read the 12 seeded queues with their team, role, overflow queue and depth | Queue R, scope applied | Not applicable |
| GET | `/queues/{queueId}/cases` | Read the seeded cases of one queue with their owner and age | Queue R, scope applied | Not applicable |
| GET | `/cases/export` | Extract the seeded cases of the caller's scope | Case record R, scope applied, row limit | Not applicable |

The write operations of the P3 surface (`POST /cases/{caseId}/transfer`, `POST /cases/{caseId}/legal-hold`, `POST /queues/{queueId}/placements`, `PATCH /tasks/{taskId}`) are the surface of the transfer, the legal-hold, the queue-write and the task stories of this service; this story seeds the rows they act on and changes none of them. Every operation declares the Case record or the Queue capability area and its right, which is why a role without the right is refused before any seeded row is read.

#### 12.2 REST operations consumed

None at run time. This story answers from its own schema and calls no service: the case list, the account keys, the person keys, the boundary accounts and the exception shapes arrive as a fixture of RWB-P1-E1065-CON (DP-11, C dependency), and the reference values it validates against are its own rows of `lov_value`.

RWB-P1-E1065-CON fixes the DEV sandbox build this migration runs inside: database `rwb_sandbox`, seed `20261128`, the migration order after the baseline, the case list of the seed and the build result the pipeline publishes. The roles and test identities the seed names as author, approver, task role and escalation target are values of RWB-P4-E1065-APP; this story calls no authorise operation to obtain them and stores no role row.

#### 12.3 Events published

None. The DEV sandbox has no Kafka broker, so nothing is produced and no outbox relay runs: DP-09 is not a pattern of this story and the seed writes no `outbox_event` row. In a running environment the case router publishes CaseCreated (EV-01), CaseAllocated (EV-02) and TimerBreached (EV-19) on `rwb.case.events.v1`, which is the behaviour of RWB-P3-E1018-APP, RWB-P3-E1020-APP and RWB-P3-E1028-APP; here the seeded cases announce nothing.

#### 12.4 Events consumed

None. A migration consumes no topic, the seed is the file and the fixture, and the DEV profile wires no consumer group into `rwb_case`.

#### 12.5 Workflows and activities

None. The seed is a migration and its seeders run in the build thread; this story starts no `CaseWorkflow`, no child workflow and no activity, and registers no worker on the `rwb-case` queue. The sandbox build stage that calls this migration is a pipeline stage of RWB-P1-E1065-CON, not a workflow of this service.

DP-04 applies as a prohibition here: this story evaluates no decision table. The exclusion rows carry the reason code and the version "EXCL-2026.11" as values of the seed file, and the seed writes no rule package, no workbook and no decision table.

#### 12.6 Schedules

None. The three jobs of rwb-case are JOB-02 case creation, JOB-03 rebalancing and JOB-06 timer check, and they belong to RWB-P3-E1018-APP, RWB-P3-E1030-APP and RWB-P3-E1028-APP; in the DEV sandbox no Schedule fires and no clock is started. The build stage that calls this migration is a pipeline stage of RWB-P1-E1065-CON, not a Schedule of this service.

#### 12.7 Tables owned

| Table | Schema | Owner | Note |
|---|---|---|---|
| recovery_case | rwb_case | P3 | The 2,812 synthetic cases plus the shape cases and the boundary cases |
| case_account | rwb_case | P3 | The account keys of each case, one primary row plus the rows of the shapes |
| case_party | rwb_case | P3 | The person keys of each case with their role codes |
| case_entry_exclusion | rwb_case | P3 | The exclusion rows of the excluded shapes, with reason code and rule version |
| queue | rwb_case | P3 | The 12 queue rows at table version 1 |
| queue_member | rwb_case | P3 | The 48 member rows with their capacity |
| assignment | rwb_case | P3 | One open assignment per case with its queue, owner, rule ID and version |
| task | rwb_case | P3 | One open task per active case |
| timer | rwb_case | P3 | One active timer per active case, including the SLA and prescription timers |
| lov_value | rwb_case | P3 | The list values of the case module at table version 1 |
| reference_row | rwb_case | P3 | One row per reference row the estate mirrors |
| reference_version | rwb_case | P3 | One version row per reference table with its valid from, author, approver and approval time |
| queue_measure | rwb_case | P3 | Present in the schema and not written by this story; the rebalancing job computes it |
| parameter_catalog | rwb_case | P3 | Present in the schema and not written by this story; the parameter migrations load it |
| parameter_value | rwb_case | P3 | Present in the schema and not written by this story; the parameter migrations load it |
| local decision record | rwb_case, written through the P7 decision-record library | P3 rows, DP-03 | One entry per seeded exclusion and one for case "RW-2026-000001" |
| outbox_event, processed_event, idempotency_key | rwb_case | PLT library | Present in the schema and not written by this story, because no event leaves the sandbox |

rwb-case reads no table of another service and holds no foreign key across services (DP-01): `case_account.account_key` and `case_party.person_key` are `varchar(255)` business keys with no foreign key (FSD P3 A1.5), the reference rows are its own, and the ACE-shaped tables and the 30 views belong to RWB-P1-E1065-CON. Every row in this table, in this sandbox, is synthetic: no row of a running environment is copied into `rwb_case` and no row of `rwb_case` is promoted out of DEV.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-P1-E1065-CON fixture | The P1 contract of this legacy key | The DEV sandbox build result for seed `20261128`: database `rwb_sandbox`, schema `rwb_case` after the baseline, the migration order, the case list with case `RW-2026-000001` and its keys, the 2,812 cases, the boundary accounts at 89 and 90 days past due and the exception shapes |
| reference fixture (own rows of `lov_value`) | DP-07 as the owner's own contract | LOV-PRODUCT with MORTGAGE, HIRE_PURCHASE, SSME and UNSECURED, LOV-CASE-STATUS, LOV-STAGE and LOV-ROUTE of the seed file |
| rwb-access authorise fake | The guard the service template wires | Case record R and Queue R for the seeded test identities, no Case record right for RW-REFADM, and a scope that excludes one case |
| decision-record library stub | DP-03 | A local chain that accepts the seeded entries, and a stopped chain that fails the build before a row is published |

The fake answers from fixtures and carries role codes, case numbers and business keys only; it never carries a customer name, a clear identity number, a contact value or an account number.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 10 reads on `/api/recovery/case/v1` in the DEV service over the seeded estate | 0 | OpenAPI 3.1, one hop, 2 s timeout and a breaker; the seed itself calls nothing |
| Kafka | 0 | 0 | No broker in the DEV sandbox, so no topic produced or consumed; DP-09 is not a pattern of this story |
| Temporal | 0 | 0 | No workflow, no activity and no Schedule; no clock is started by the seed |
| File | 0 | 1 | The seed file of the reference estate and the case list fixture; no runtime file exchange |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `sandboxseed`, Java package `th.co.scb.ace.workbench.recovery.case.sandboxseed`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. Every seeded row lands in `rwb_case` | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`. One entry per seeded exclusion and one for case "RW-2026-000001", kept in `rwb_case` because no relay runs | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision. Here a prohibition: the seed evaluates no rule and writes the reason code and the version "EXCL-2026.11" as values | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views. Here a prohibition: the case list, the keys and the boundary accounts come from the RWB-P1-E1065-CON fixture | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case. This service owns the reference rows, so the seed writes `lov_value`, `reference_row` and `reference_version` and validates every code against them | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON (the same-service contract) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`. The DEV service serves the seeded estate under `/api/recovery/case/v1`; the monolith base is not used | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema. `V1065_1__case_estate_seed.sql` runs after the `rwb_case` baseline | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route. SCR-02 Case list, SCR-03 Case record and SCR-07 Team queues read the seeded rows through the composite route | H RWB-PLT-N001-CON |

This is a secondary slice: it adds no new build dependency of its own. Metadata "Depends on (build)" stays `None` and "Contract dependencies" stays `RWB-P1-E1065-CON` exactly as the Work Package fixes them, and the platform contract libraries of DP-03, DP-04, DP-07, DP-15 and DP-19 arrive with the baseline, not with this story.

DP-01 is the first rule of the seed: every row lands in `rwb_case`, the links are business keys, and no case, account or person key is read from another schema. DP-03 applies as the local decision record behind every seeded exclusion and behind the one worked case. DP-04 and DP-05 apply as prohibitions, so the estate can be built before the ACE views and the rule packages exist in DEV. DP-07 is the reference read and write: the seed writes the list values and the version rows of its own service and validates every code against them, so no code, list value or queue code appears in Java. DP-15 carries the estate on the per-service sequence, DP-13 gives the DEV service its base, and DP-19 is the route the screens use.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ReferenceEstateSeeder | Service | Writes the LOV rows, the `reference_row` rows and one `reference_version` row per table version with valid from 30 November 2026, the author, the approver and the approval time; refuses a row outside its list and a second version in force |
| QueueEstateSeeder | Service | Writes the 12 `queue` rows with their codes, team codes, role codes and overflow queue, and the 48 `queue_member` rows with their capacity |
| CaseEstateSeeder | Service | Writes one `recovery_case` row per case of the fixture with its case number, product group, status, entry date, primary person key and total outstanding at entry |
| CaseLinkSeeder | Service | Writes `case_account` and `case_party` from the account keys and person keys of the fixture, one primary account and one BORROWER party per case, plus the extra rows of the shapes |
| AssignmentSeeder | Service | Writes one open `assignment` per case from the queue rows and the member rows, names rule ID "ALLOC-014" and its version, and enforces the cap of 40 open cases per member |
| TaskTimerSeeder | Service | Writes one open `task` and one active `timer` per active case, with the SLA offsets of FSD P3 AC-ALT-P3-011, the escalation to RW-TEAMMGR under R-UNI-30 and one prescription timer per case |
| ExceptionShapeSeeder | Service | Writes 10 cases for each shape of legacy BR4, with the exclusion rows and their reason codes, rule IDs and version "EXCL-2026.11" |
| DecisionRecordSeeder | Service | Writes the local decision records of the seeded exclusions and of case "RW-2026-000001" through the decision-record library, first in the transaction |
| CaseSeedVerifier | Service | Reads the whole estate back: counts per product group, the links per case, one assignment, task and timer per active case, the 10 rows per shape, the boundary cases, one version per reference table, every code in its list and the row count per table |
| DevGrantScript | Script | Grants SELECT on schema `rwb_case` to `rwb_sandbox_read`, with no UPDATE, no DELETE and no access to the local decision-record table |

**Database and migrations**

- Writes the twelve tables of `rwb_case` it seeds and the local decision records; writes no other table and reads no other schema (DP-01).
- Migration in this story: `V1065_1__case_estate_seed.sql`, the versioned per-service migration that carries the reference estate, the queues, the cases, the links, the assignments, the tasks, the timers and the shapes, run after the `rwb_case` baseline and inside the build order of RWB-P1-E1065-CON.
- Its companion `R__case_estate_seed_rebuild.sql` is the repeatable migration that writes the same rows again from the same seed value and the same fixture, so a rebuilt sandbox holds the same counts and the same total outstanding at entry (AC7).
- The seed is idempotent by construction: the repeatable migration clears the estate tables it writes and writes them again from the seed value, deletes nothing outside those tables, and refuses a row that belongs to two table versions.
- No column, index or constraint is added for a case, an ACE value or an identity; `case_account.account_key`, `case_party.person_key` and `recovery_case.primary_person_key` stay business keys with no foreign key.

**Configuration and reference data**

- `rwb.case.sandbox.seed=20261128` is the seed value of the deterministic value factory.
- `rwb.case.sandbox.cases.mortgage=1226`, `rwb.case.sandbox.cases.hire-purchase=1296` and `rwb.case.sandbox.cases.ssme=290` are the case volumes (DL15).
- `rwb.case.sandbox.shape-count=10` is the number of cases per exception shape (legacy BR4).
- `rwb.case.sandbox.queue-version=1` and `rwb.case.sandbox.valid-from=2026-11-30` are the table version and the valid-from date of the reference estate (FSD P3 AC-P3-006-01).
- `rwb.case.sandbox.boundary-count=10` is the number of accounts at 89 and at 90 days past due (DL16).
- `rwb.case.sandbox.tasks-per-case` and `rwb.case.sandbox.timers-per-case` are the counts per active case; their values are Not specified in the source documents (GAP-2249; ASM-3707) and the story fixes one open task and one active timer per active case.
- `rwb.case.sandbox.queue-distribution` is the case-to-queue distribution; its value is Not specified in the source documents (GAP-2250; ASM-3708) and the story distributes by product group to the queue rows of the seed file.
- The queue codes, product groups, statuses, stages, routes and reason codes are rows of the seed file and the reference tables; the rule IDs "ALLOC-014" and "EXCL-2026.11" are values of the seed file and the rows, never constants.
- The login is the rwb-case login (DP-02) and the DEV-only read-only role keeps the legacy name `rwb_sandbox_read`; both are Not specified in the source documents for the target schema (GAP-2251; ASM-3709).
- The feature switch is `rwb.case.sandbox-estate`, read as a parameter: on in the DEV profile only; off means the seed does not apply and the case tables stay empty, never half filled.

**Build steps**

1. Seed file, value factory and `ReferenceEstateSeeder` over the four reference tables, with a test per violation (a code outside its list, two versions in force, a missing valid-from) and a test that no code or list value appears in the Java source.
2. `QueueEstateSeeder` over the 12 queues and 48 members, with the overflow queue and the capacity of member U-11; test for AC3.
3. `V1065_1__case_estate_seed.sql` and `R__case_estate_seed_rebuild.sql`, with the read-back of AC1 and the same-seed test of AC7.
4. `CaseEstateSeeder` and `CaseLinkSeeder` over the fixture, with the per-product loop, the business-key links, the primary account and the BORROWER party; tests for AC1 and AC2.
5. `AssignmentSeeder` with the cap of 40 open cases and the rule ID and version; test for AC3.
6. `TaskTimerSeeder` with the one task and one timer per active case, the SLA offsets and the prescription timer; test for AC6.
7. `ExceptionShapeSeeder` over the ten shapes of legacy BR4, with their exclusion rows and the boundary cases; test for AC4.
8. `DecisionRecordSeeder` and `CaseSeedVerifier` with every check of its row above, plus the decision-record assertions of AC9; tests for AC1, AC4, AC7 and AC9.
9. `DevGrantScript` for `rwb_sandbox_read`: SELECT on the schema, no UPDATE, no DELETE and no SELECT on the decision-record table; test for AC8.
10. Contract-fake run of RWB-P1-E1065-CON, the rwb-access authorise fake and the reference fixture, so the story builds and proves every criterion before rwb-source-data and rwb-access are live in DEV.

**Feature switch.** `rwb.case.sandbox-estate`, read as a parameter; off leaves the case tables empty and publishes nothing.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P1-E1065-CON stay green, a rebuilt DEV sandbox holds 2,812 cases at the three product-group counts with their links, the 12 queues, the 48 members, one assignment, one open task and one active timer per active case, the 10 cases per exception shape, the boundary cases with the 90-day accounts holding one open case each and the reference estate at version 1, and `rwb_sandbox_read` reads the schema without being able to change it.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | The caller's role holds no Case record right, or no Queue right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case of the read is absent from the estate or outside the caller's scope | This case is not in your scope. |
| MSG-P3-001 | A transfer of a seeded case is attempted without a reason in DEV | Choose a reason for the transfer. |
| MSG-P3-002 | A seeded case is transferred to an owner at the caseload cap | {owner} is at the caseload cap. Choose another owner or the team queue. |

Seed failures are reported in the pipeline result with the table, the row and the column named: a code outside its list, a second version in force, a case or key absent from the fixture, an owner above the cap, a missing assignment, task or timer and a write outside `rwb_case` each fail the build, and no user message applies. For MSG-P4-002 in this story, {action} names the action the caller tried — for example "open the case list" — and never a case fact, a customer key or a role name.

### 15. Screens and states

No screen in this story. SCR-02 Case list (E1), SCR-03 Case record (E1 read only), SCR-07 Team queues and SCR-09 Exception queue (both E2) will show the seeded rows this story writes: the case list its cases with product group, stage, owner, queue and age, the case record its accounts, parties, stage, owner, clocks and history, the team queues the 12 queues with their depth and cap use, and the exception queue the shapes and the cases no rule matched. The screens themselves belong to RWB-P3-E1023-APP, RWB-P3-E1031-APP, RWB-P3-E2011-APP and RWB-P3-E2016-APP.

Every screen reads the estate only through the gateway-bff composite route (DP-19), which calls rwb-case for the case, the queue and the owner and rwb-source-data for the account columns, one hop each. The route specification and the field-level masking of the composite route are Not specified in the source documents (GAP-2251; ASM-3709).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-065-01 | AC1, AC2, AC4, BR2, BR3, BR4, BR5 | End to end | Seed 20261128; 2,812 cases at 1,226 MORTGAGE, 1,296 HIRE_PURCHASE and 290 SSME with their links and total_outstanding_at_entry 1,845,200.00 for case "RW-2026-000001"; the 10 cases per exception shape; the reference estate at version 1 |
| TC-E1-065-02 | AC8, BR8 | End to end | The DEV read-only role `rwb_sandbox_read`: the product-group query of AC1, the reads of the estate and a refused UPDATE on `recovery_case` |
| TC-E1-065-03 | AC5, BR3 | End to end | A test migration adding a case column with its dictionary row and list, and the reference estate rebuilt from it; no generator code changed |
| TC-E1-065-04 | No criterion here; the build gate on a missing dictionary entry belongs to RWB-P1-E1065-CON | End to end | A dictionary fixture without the row for `recovery_case.closure_reason` |
| TC-E1-065-05 | AC7, BR2 | End to end | Two builds for commit "a1b2c3d" and seed 20261128: the same counts per product group, queue, member, assignment, task and timer, and the same total outstanding at entry |
| TC-E1-065-06 | AC5 for a list value; the empty-list failure itself belongs to RWB-P1-E1065-CON | End to end | An empty LOV-PRODUCT seed; the reference seeder refuses the estate and names the list |
| TC-E1-065-07 | AC1, AC2, BR9 | End to end | The keys of the fixture only: no clear identity number, no name and no contact value in `rwb_case`; a clear identity number in `public.customer` is allowed, RWB-P1-E1065-CON |
| TC-E1-065-08 | AC4, BR5 | End to end | The boundary accounts of the fixture: 10 at 89 days past due with no case and 10 at 90 days past due with one open case each |
| TC-E1-065-09 | AC7 for the same-seed result; the build lock itself belongs to RWB-P1-E1065-CON | End to end | Two builds started together |
| TC-P3-E1065-01 | AC9, BR1 | Component | The DEV profile with no broker: the seeded exclusions and case "RW-2026-000001" carry their local decision records, no `outbox_event` row is written and no case event is produced |
| TC-E1-065-10 | No criterion here; the access refusal belongs to RWB-P4-E1065-APP and RWB-P1-E1065-CON | Component | A test identity holding RW-REFADM calls the sandbox case list through the DEV service; refused with MSG-P4-002 with the identities seeded by RWB-P4-E1065-APP |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end and Access to Component; the Level column is the target reading of each row. All ten legacy test cases of this key are listed with the slice of behaviour this story answers: the case estate for TC-E1-065-01, the read-only role for TC-E1-065-02, the reference rebuild for TC-E1-065-03, the same-seed result for TC-E1-065-05 and TC-E1-065-09, the list value for TC-E1-065-06, the synthetic keys for TC-E1-065-07 and the boundary cases for TC-E1-065-08; the dictionary build, the empty-list failure, the build lock and the access refusal belong to RWB-P1-E1065-CON and RWB-P4-E1065-APP. One new case, TC-P3-E1065-01, covers the DEV profile with no broker. The -ITG copies of these cases belong to RWB-ITG-E1065-ITG, which proves the same values across rwb-source-data, rwb-case, rwb-access and the DEV environment end to end.

### 17. Guardrails

- No business value in code: the seed value, the volumes, the shape count, the queue version, the valid-from date, the boundary count, the queue codes, the product groups, the statuses, the stages, the routes, the reason codes and the rule IDs are rows, parameters or the fixture; no such value appears in Java and the verifier fails a row outside its list.
- Synthetic only, and no clear personal value in `rwb_case`: the cases, the people and the accounts are synthetic, the links are business keys, and no name, contact value or identity number is written; a clear identity number in the ACE-shaped tables is allowed there and is not this slice's data (legacy BR9).
- The verifier gate stands between the seed and the squads: a build that fails any check of section 4 step 11 publishes no sandbox and the previous sandbox stays in use, so no squad reads a half-seeded estate.
- No cross-schema write and no cross-schema read: `rwb_case` holds no foreign key into another schema and no copy of a case, a list value or an ACE row (DP-01); the case list, the keys and the boundary accounts come from the RWB-P1-E1065-CON fixture (DP-05) and the roles and identities from RWB-P4-E1065-APP.
- No event leaves the sandbox: the seeded exclusions and case "RW-2026-000001" carry local decision records and no relay, and no `outbox_event` row is written (DP-03, and DP-09 is not a pattern of this story).
- One owner for the clock and the cap: the seed copies the timer offsets, the escalation role and the capacity from the reference rows and never decides a service level; the timer job of RWB-P3-E1028-APP fires the clock and the rebalancing job of RWB-P3-E1030-APP moves the cases in a running environment.
- The seed is a per-service Flyway migration in `rwb_case`, versioned and repeatable, and no migration of this service touches another service's schema or the shared baseline (DP-15).
- The DEV read-only role reads and never writes: no UPDATE, no DELETE and no access to the decision-record table, and no copy of the estate leaves DEV.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-001 | 14 data products, each with one system of record and one owner, each reachable in DEV without a request to another team | Business Requirements Epic 1, sections 3.1 and 4 | None | All recovery processes | R-UNI-17, R-UNI-05, R-UNI-07, R-UNI-20, R-UNI-10; DL15, DL16; D-RCV-35 | TC-E1-065-01, TC-E1-065-03, TC-E1-065-05, TC-E1-065-07, TC-E1-065-08, TC-E1-065-09 |
| REQ-RDF-010 | Access per data product by role; personal data masked in line with PDPA | Business Requirements Epic 1, sections 3.1 and 4; Program section 6.7 (NFR-045) | None | All recovery processes | CTL-11; D-RCV-35 U4; legacy BR1, BR9 | TC-E1-065-02, TC-E1-065-07 |

The features this slice seeds are FEAT-CWC-01 (the case ID), FEAT-CWC-02 (one case per customer and product), FEAT-CWC-04 (the entry rule at 90 days past due), FEAT-CWC-05 (the exclusion rules as data), FEAT-CWC-06 (roles, teams and queues as data), FEAT-CWC-07 to FEAT-CWC-09 (allocation, assignment and overflow), FEAT-CWC-11 (service levels and stage timers) and FEAT-CWC-12 (prescription dates), which the FSD P3 module pairs with RWB-E1-018, RWB-E1-019, RWB-E1-020, RWB-E1-028 and RWB-E1-029; this slice answers them only for the DEV case estate and changes none of their design.

| Legacy reference | Where it is kept |
|---|---|
| Legacy sections 1, 2, 3 and 4 (story, rationale, preconditions, flow) | Sections 1 to 4 of this story, narrowed to the case estate; the database, the ACE test double, the generator and the pipeline are RWB-P1-E1065-CON |
| Legacy AC1 (the sandbox exists), case sentence | AC1 and AC2 of this story; the schemas, the 92 tables, the 30 views and the dictionary are RWB-P1-E1065-CON |
| Legacy AC2 (readable and extractable), product-group query | AC1 and AC8 of this story, run on `rwb_case.recovery_case` |
| Legacy AC4, AC5, AC6, AC9 (dictionary gate, reset, constraint, two builds) | AC7 of this story for the same-seed and rebuild result; the dictionary gate, the constraint failure and the lock are RWB-P1-E1065-CON |
| Legacy AC7 (no clear personal value outside the ACE tables) | AC2 and AC9 of this story for the keys of `rwb_case`; the verifier of the whole sandbox is RWB-P1-E1065-CON |
| Legacy AC8 (accounts at the entry boundary) | AC4 of this story for the case side; the accounts themselves are the fixture of RWB-P1-E1065-CON |
| Legacy BR1, BR2, BR3, BR4, BR5, BR6, BR8, BR9 | Section 8 of this story |
| Legacy BR7 (the ACE-shaped tables as a test double) | RWB-P1-E1065-CON and RWB-P1-E1065-DB |
| Legacy sections 5, 6, 9, 10, 11, 12, 14, 15 and 17 | Sections 5, 6, 9, 10, 11, 12, 14, 15 and 17 of this story, for the case estate; the pipeline stage and the DEV endpoint of legacy section 12 are the reads of section 12.1 |
| Legacy TC-E1-065-01 to TC-E1-065-10 | Section 16 of this story, with the slice of behaviour each case answers |

### 19. Out of scope

- The DEV database `rwb_sandbox`, the ACE-shaped test double, the 92 recovery tables, the 30 `v_ace_*` views, the dictionary, the generator, the exception-shape builder, the verifier of the whole sandbox, the pipeline stage, the rename and the read-only grant on schema `recovery`: RWB-P1-E1065-CON, RWB-P1-E1065-APP and RWB-P1-E1065-DB.
- The role list, the permission matrix and the synthetic test identities: RWB-P4-E1065-APP.
- The document estate of the sandbox: RWB-P5-E1065-APP.
- The deviation rows of the sandbox: RWB-S8-E1065-APP.
- The parameter catalog and the parameter values, including the case parameters: RWB-P3-E1042-APP and RWB-P3-E1043-APP.
- The case ID issuance in a running environment and the case record: RWB-P3-E1018-APP and RWB-P3-E1023-APP.
- The allocation and assignment engine, the transfer engine and the queue rebalancing: RWB-P3-E1020-APP, RWB-P3-E1021-APP and RWB-P3-E1030-APP.
- The service levels, the timers, the escalation and the prescription dates as behaviour: RWB-P3-E1028-APP.
- The end-to-end proof of these values across the sandbox, rwb-source-data, rwb-access and rwb-case: RWB-ITG-E1065-ITG.
- The `rwb_case` schema baseline, the platform migration role, the `rwb.case.events.v1` topic and consumer groups, the observability and the runbook of this service.
