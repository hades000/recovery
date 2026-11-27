# RWB-P1-DM001-APP Migrate account and arrears

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (27 November 2026, D-RCV-60 P1 developer readiness, RD-P1 register)

- RD-P1-041: the batch gate reads the DP01 freshness stamp through `FreshnessQuery` (owner RWB-P1-E1015-APP), not `v_ace_batch_status`; late, failed, never-stamped and business-date rules are stated (findings #3, #9).
- RD-P1-004 and RD-P1-005: every refusal is the published problem body with a fixed status and message code (findings #4, #8); AC1, AC4 to AC9 rewritten and AC10 to AC12 added (findings #6, #7).
- RD-P1-040, RD-P1-045 and X-01: reconciliation and freshness ownership corrected; rollback follows the forward-only standard.
- RD-P1-060 settles the account entity path and response (GAP-0549). The delivery steps are in section 20 (findings #1, #10).
- Batch D: RD-P1-060 specifies the ungated account entity read. RD-P1-062 defines the never-stamped freshness response and the interim gated error (GAP-3284). Test citations use Test Cases v9.

| Item | Value |
|---|---|
| Story key | RWB-P1-DM001-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-DM-001 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP15 |
| Parallel lane | L-P1-D |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P1-DM001-APP-16) |
| Depends on (build) | RWB-PLT-E1044-CON |
| Contract dependencies | RWB-P1-E1015-CON (freshness answer of DP01); RWB-P4-E1037-CON (authorise) |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7), including getAccount, freshness and problem responses |
| Readiness decisions | RD-P1-004; RD-P1-005; RD-P1-011; RD-P1-040; RD-P1-041; RD-P1-043; RD-P1-045; RD-P1-062; RD-P1-060 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the account and arrears read path that replaces the withdrawn RWB-DM-001 migration, and the per-service Flyway version that records the removal, split for rwb-source-data. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-DM001-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (16 resolved, 18 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **data steward (RW-DATASTEW) and a squad member (RW-TRIBE)**, I want **the account and arrears read path of rwb-source-data to answer for an account_key from `v_ace_account`, `v_ace_bucket_log`, `v_ace_product` and `v_ace_branch` at the ACE business date with no Workbench copy, and the per-service Flyway sequence to create nothing for those rows and to record the removal of the legacy migration**, so that **every recovery screen reads the one copy ACE holds, and no second copy of an account or of its arrears can ever disagree with it**.

**The legacy key is withdrawn, and this story is the rework that replaces it.** RWB-DM-001 Migrate account and arrears carries **Status: Removed** and **Decision: D-RCV-35 (U1)**: "ACE ingests the ALS account, arrears and balance data and holds the one copy. The Workbench loads none of it, so there is nothing to extract, transform, load or reconcile." AC1 to AC3 and TC-DM-001-01 to TC-DM-001-04 are withdrawn by the same row. This story therefore extracts nothing, transforms nothing, loads nothing, reconciles no migrated row and cuts nothing over, and it builds no staging table, no load job and no cutover plan: there is nothing to migrate. The story title is kept because Template and Rules §R5.2 keeps the legacy compact and the legacy title; the deliverable under it is the read path.

What it builds instead is exactly what the legacy "Read path instead" row names, and the boundary of the realignment holds it:

- **Stays in rwb-source-data (P1), schema `rwb_source_data`:** the account and arrears read path, its repository and the read service, and the Flyway history row of this story's own version. DP01 Account and arrears stays in the data product catalog with system of record "ACE (ingested from ALS)" and its view list; only the migration story leaves (legacy "Data product" row; FSD P1 v3 A2.2).
- **Stays in ACE, where it already is:** the account, the arrears, the balances, the classification, the ACE business date, the monthly bucket history and the product and branch lists, read through the four Section A views (FSD P1 v3 A2.3 "What this module does instead"; TSD P1 v3 T3.3 views 1, 12, 13 and 14).
- **Removed by D-RCV-35 (U1) and not carried anywhere:** `loan_account`, `account_payment`, `collections_history`, `load_run`, `dq_exception` and the inbound interfaces and the load job of the legacy key (TSD P1 v3 T3.10; FSD P1 v3 A2.3 "Removed objects"). Any column the Workbench still needs is raised once in RWB-ACE-001 and never copied here.
- **Database access:** one login per service (DP-02), the `rwb_source_data` login of Architecture v5 slide 29, which holds SELECT on the 30 `recovery.v_ace_*` views and nothing in `public`. Only rwb-source-data reads those views (Architecture v5 slides 8, 9, 29 and 41; ADR-010).
- **Per-service migrations:** the per-service Flyway sequence in `rwb_source_data` (DP-15, ADR-021). This story's version adds no table, no column and no index for an account or an arrears row; it records that the legacy migration does not ship.
- **Read contract:** the read path is answered behind the P1 read contract that RWB-P1-E1069-APP publishes on base `/api/recovery/source-data/v1`, and the freshness that RWB-P1-E1015-APP stamps. This story adds no path of its own and claims neither operation.
- **Events, workflows, screens:** none. The story publishes no Kafka event, starts no workflow and adds no screen.

### 2. Business rationale

An account is held in ACE. ACE ingests it from ALS overnight, with its arrears, its balances, its classification and its monthly bucket history, and it is the one copy that a branch, a collector and a recovery officer all see. The legacy Workbench held a second copy, loaded it every night and reconciled the two, and the two disagreed sooner or later. D-RCV-35 (U1) ended that: the Workbench holds the case and the decision, ACE holds the account, and a view joins them.

The legacy story states the position in its own rows, quoted here character for character:

> **Status** Removed
>
> **Decision** D-RCV-35 (U1)
>
> **Why** ACE ingests the ALS account, arrears and balance data and holds the one copy. The Workbench loads none of it, so there is nothing to extract, transform, load or reconcile.
>
> **Read path instead** v_ace_account for the account, the arrears, the balances, the classification and the ACE business date; v_ace_bucket_log for the monthly bucket history; v_ace_product and v_ace_branch for the product and branch lists
>
> **Data product** DP01 stays in the catalog with system of record "ACE (ingested from ALS)" and its view list. Only the migration story leaves.
>
> **Withdrawn IDs** AC1 to AC3; TC-DM-001-01 to TC-DM-001-04
>
> **Later home** None. Any column the Workbench still needs is raised once in RWB-ACE-001.

That "Read path instead" row is the whole of the work this story carries. It is not a smaller migration: it is the opposite of one. The legacy key left a gap where a load used to be, and the gap is closed by a read that copies nothing, so REQ-RDF-002's account, arrears, balance and classification facts reach a recovery case from one named source, current to the business date ACE itself records, with no Workbench row to reconcile and no cutover to sign off.

The realignment adds three things the legacy story did not have to say. **First**, the read is a service boundary: the four views are read by rwb-source-data and by no one else, on one login, so the rest of the estate reaches an account through this service's contract and never through a view (Architecture v5 slides 8, 9 and 41; DP-05). **Second**, the migration itself is a delivered artifact that must be seen to create nothing: the per-service sequence carries a version whose only effect is in the dictionary of what shipped, so a later reader of the schema finds no account table and a later reader of the history finds out why (DP-15; TSD P1 v3 T3.2). **Third**, the freshness of the account is a product of the ACE batch, not of a Workbench load: a late ALS batch makes DP01 stale and says so on the read, instead of a load failing quietly and leaving yesterday's copy in place (FSD P1 v3 A2.14; TSD P1 v3 T3.7).

The legacy key also sits in a Work Package that still asks for an APP story under the legacy title, which is a documentation mismatch rather than a build question: the story is required, and what it builds is the read path (GAP-0546; ASM-0782).

### 3. Preconditions

- The 30 read-only `recovery.v_ace_*` views exist and are granted. RWB-P1-E1069-DB creates the per-service login, the grant and the four extension tables; RWB-P1-E1069-APP creates the Section A views on the per-service Flyway sequence and runs the conformance test (FSD P1 v3 A2.1.2; TSD P1 v3 T3.2 and T3.3). The four views this story reads are TSD P1 v3 T3.3 views 1, 12, 13 and 14: `v_ace_account` (42 fields, DF-ACE-001 to DF-ACE-042), `v_ace_bucket_log` (6, DF-ACE-140 to DF-ACE-145), `v_ace_product` (5, DF-ACE-146 to DF-ACE-150) and `v_ace_branch` (4, DF-ACE-151 to DF-ACE-154).
- RWB-P1-E1015-APP stamps DP01 and supplies it through FreshnessQuery. The never-stamped fixture answers businessDate null, status STALE and staleSince null, with sourceExtractedAt and loadedAt absent (RD-P1-043, RD-P1-062).
- The platform Flyway contract RWB-PLT-E1044-CON is in place: the per-service sequence of `rwb_source_data` with its V0001 baseline, and the versions for the Section A and Section B views (TSD P1 v3 T3.2; DP-15). This story takes the next free version after those at build time and creates no account or arrears object in it.
- No build dependency blocks the start: RWB-PLT-E1044-CON is a platform contract story, so the story is Day 1 under Template and Rules §R5.7 rules 1 and 8. The wave 4 tag is the W-MAP tag of EP08 and does not delay the build (GAP-0548; ASM-0784). The read path is released with the wave 1 service deploy, where the P1 read contract and the freshness stamp are live; the release date is confirmed at the wave entry check.
- The parameters and the reference data of rwb-case are not preconditions of this build: DP-06 and DP-07 are not in this story's pattern set, and the story reads no parameter and no reference list. The cut-off that marks DP01 late is `data_product.expected_by`, applied by the stamp component; this story reads the stamp and writes no constant (RD-P1-041).
- RWB-P1-E1069-APP owns GET /accounts/{accountKey} (getAccount) on /api/recovery/source-data/v1. The entity response contains account facts, relations and DP01 freshness, with no freshness refusal (RD-P1-060).
- The rwb_source_data login exists (Architecture v5 slide 29) and holds SELECT on the views only, with no INSERT, UPDATE, DELETE or TRUNCATE on any view and no privilege in `public` (BR-P1-001-4; Architecture v5 slides 29 and 41).
- The service template, the outbox and inbox libraries and the feature flag library are present in the repository (Architecture v5 slide 20). This story publishes no event and writes no outbox row.

### 4. Flow

1. A caller requests account facts by the ACE account key through GET /accounts/{accountKey}. A date-qualified read that requires daily completeness, such as listEligibleAccounts, follows the DP01 gate in step 3.
2. The guard of the published operation answers first: the read path runs only on an allow, and a caller whose Case record right R is absent is refused before any view is touched (MSG-P4-002).
3. For a gated read, AccountArrearsBatchGate checks the DP01 stamp through FreshnessQuery. The expected business date is the latest bank business day before the test or run date in Asia/Bangkok, using DP14. The gated read returns 409 MSG-P1-001 unless the expected date is LOADED. getAccount carries the stamp on its entity response (RD-P1-060, RD-P1-062).
4. AccountArrearsReadRepository issues one SELECT per view, keyed by `account_key`, on the `rwb_source_data` login: `v_ace_account` for the account, the arrears, the balances, the classification, the flags and `data_as_of`; `v_ace_bucket_log` for the month-end bucket history; `v_ace_product` for the product and product group; `v_ace_branch` for the branch and the region (DP-05).
5. AccountArrearsQueryService assembles one answer: the account fields in field-ID order, the bucket history newest month first, and the product and branch names resolved from the two list views. It carries the ACE business date and the status of DP01 and nothing derived by the Workbench. The answer is shaped by the P1 read contract of RWB-P1-E1069-APP, and the late case is decided from the stamp of step 3, whose cut-off is `data_product.expected_by`, with no parameter read (RD-P1-041).
6. No row in `v_ace_account` for the `account_key` means the account is not in ACE at that business date: the answer is 404 with messageCode MSG-P4-003, no bucket, product or branch is returned, and nothing is written (AC4).
7. A value that a source does not give to this deliverable is never guessed on the read: for example the 7 ALS columns that RWB-ACE-001 adds to `account` are not in `v_ace_account` yet, so the read answers without them and the column is raised once in RWB-ACE-001 (TSD P1 v3 T3.4 note; T3.11 point 1; legacy "Later home" row).
8. No step writes a row: the read path holds no INSERT, no UPDATE and no DELETE, and the service never caches an ACE row into its own schema. The only row the story writes is the Flyway history row of its own version, at deploy (AC1, AC3).
9. Every view read is a single statement on the service's own login, under the statement timeout of the SQL view grant (Architecture v5 slides 29 and 41). No statement names a table in `public` and no statement names another service's schema (BR-P1-001-2, BR-P1-001-4).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A view read fails or is cancelled by its statement timeout: the relation is absent or the statement errors, also after another view has answered | The answer is 503 with no partial account, no bucket history and no product or branch; nothing is written and no stale row is served as current | MSG-GEN-006 | AC10 |
| X2 | A gated read sees DP01 STALE, for another business date or never stamped | 409 with DP01 and its last stamped date, if present. An eligible getAccount read still returns 200 with DP01 freshness | MSG-P1-001 for the gated read | AC5, AC11 |
| X3 | The caller's Case record right R is absent | 403; the call is refused before any view is read; no row is returned and nothing is written | MSG-P4-002 | AC6 |
| X8 | No session, or no Workbench role | 401 before any view is read | MSG-P4-001 | AC12 |
| X9 | The authorise call does not answer within 2 s | 503; no field is returned and no view row is served | MSG-GEN-006 | AC12 |
| X4 | `v_ace_account` holds no row for the `account_key`, or the account is outside the caller's scope | 404, with no bucket, product or branch, and nothing is written | MSG-P4-003 | AC4 |
| X5 | The `account_key` in the path is blank | 400 naming `id` as the failing field; no view is read | MSG-GEN-001 | AC7 |
| X6 | The read would need a column that `v_ace_account` does not carry | The field is absent from the answer and the column is raised once in RWB-ACE-001; no value is invented and no copy is created | None | AC8 |
| X7 | The story's Flyway version is applied a second time | Flyway reports it as already applied; no row is written twice and no version is edited in place | None | AC1 |

The message texts are those of the Error and Message Standard (section 14). Every 4xx and 5xx answer is `application/problem+json` with the `Problem` schema of rwb-source-data.yaml 5.1.0 (`type`, `title`, `status`, `messageCode`, `instance`).

Pending: the ACE view statement timeout, retry and database breaker policy, owner solution architect, tracked as GAP-3566 (Error Handling and Resilience Standard v5 section 8.4). A REST read that times out answers 503 MSG-GEN-006; the authorise call is a POST and is not retried automatically.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | One repository over four views, one query service, one Flyway version and the fixtures of the P1 read contract; nothing else in the service is touched |
| Negotiable | The answer shape, the paging and the freshness cut-off are the published contract's and the parameter's; this story fixes the four views, the key and the no-copy rule only |
| Valuable | The one copy of the account and its arrears reaches every recovery screen, and no Workbench row can disagree with ACE |
| Estimable | One repository, one service, one migration, one set of view fixtures and two test cases |
| Small | Fits one sprint, as the rework of a withdrawn key |
| Testable | Every criterion in section 7 is one automated test on synthetic view fixtures; no ACE data is needed |

### 7. Acceptance criteria

```gherkin
Feature: The account and arrears read path that replaces the withdrawn migration

  Background:
    Given the 30 read-only views exist in schema "recovery" and the "rwb_source_data" login holds SELECT on them and nothing in "public"
    Given "v_ace_account" holds one row for account_key "ACC0000017" with days_past_due 90, tdr_flag true and data_as_of "2026-11-30"
    Given "v_ace_bucket_log" holds the month-end rows of "ACC0000017" for 2026-10 and 2026-11
    Given "v_ace_product" holds the product row of "ACC0000017" and "v_ace_branch" holds its branch row
    Given the DP01 stamp in use answered by FreshnessQuery is business date "2026-11-30" with status LOADED

  Scenario: AC1 The Flyway sequence creates nothing for account and arrears and records the removal (new, D-RCV-60)
    Given the per-service Flyway sequence of schema "rwb_source_data" with its V0001 baseline applied, and the list of its tables, views, columns and indexes recorded
    When the version of this story is applied
    Then the recorded list is unchanged
    And the schema holds no table named "loan_account", "account_payment", "collections_history", "load_run" or "dq_exception"
    And no table of the schema holds an account, a payment, a balance, an arrears position, a bucket, a product or a branch row copied from ACE
    And "flyway_schema_history" holds one row for the version of this story, whose description records the removal of the account and arrears migration
    And the history holds no version whose description names an extract, a transform, a load or a reconciliation of migrated account or arrears rows
    When the same version is applied a second time
    Then Flyway reports it as already applied and no row is written twice

  Scenario: AC2 The read path answers from the four views at the ACE business date (new, D-RCV-60)
    Given "v_ace_account" holds the balances, the classification, the arrears and the flags of "ACC0000017" as the view returns them
    When the account and arrears read path is asked for account_key "ACC0000017" for business date "2026-11-30"
    Then the answer carries the account fields of "v_ace_account" with days_past_due 90, tdr_flag true and data_as_of "2026-11-30"
    And it carries the two month-end bucket rows of "v_ace_bucket_log", newest month first
    And it carries the product name from "v_ace_product" and the branch name from "v_ace_branch"
    And it names the ACE business date "2026-11-30" and data product "DP01" with status LOADED
    And the count of account, payment, balance, arrears, bucket, product and branch rows in schema "rwb_source_data" is 0 before and after the read

  Scenario: AC3 The read path returns no account copy and the Workbench holds zero account or arrears rows (new, D-RCV-60)
    Given the service is deployed with the read path live and the four views reachable
    When a caller asks for account_key "ACC0000017"
    Then the answer holds only view fields: "DF-ACE-001" to "DF-ACE-042", "DF-ACE-140" to "DF-ACE-145", "DF-ACE-146" to "DF-ACE-150" and "DF-ACE-151" to "DF-ACE-154"
    And no field of the answer comes from a table in schema "rwb_source_data"
    And the service holds no entity, no table and no repository class named "loan_account", "account_payment" or "collections_history"
    And schema "rwb_source_data" holds no table for an account, a payment, a balance, an arrears position, a bucket, a product or a branch

  Scenario: AC4 An account with no view row answers 404 and writes nothing (new, D-RCV-60)
    Given "v_ace_account" holds no row for account_key "ACC0000099"
    When the read path is asked for account_key "ACC0000099"
    Then the answer is 404 "application/problem+json" with status 404 and messageCode "MSG-P4-003"
    And it carries no account field, no bucket history, no product and no branch
    And no query is run on "v_ace_bucket_log", "v_ace_product" or "v_ace_branch"
    And no row is written to any table of schema "rwb_source_data" and no event or decision record is written

  Scenario: AC5 The read is held when the DP01 stamp of the business date is not LOADED (new, D-RCV-60)
    Given the DP01 fake serves the bank business day before the expected date with status STALE and staleSince equal to the expected date
    When the eligible-accounts read checks the expected business date
    Then the answer is 409 "application/problem+json" with messageCode "MSG-P1-001"
    And the detail identifies DP01 and the preceding bank business day
    And the answer carries no account field and no arrears field
    And no query is run on the four views, no stamp is written and no row is written to any table of schema "rwb_source_data"

  Scenario: AC6 A caller without the read right is refused with MSG-P4-002 (new, D-RCV-60)
    Given a caller whose Case record right R is absent in the authorise answer of the rwb-access contract fake
    When the caller asks for account_key "ACC0000017"
    Then the answer is 403 "application/problem+json" with messageCode "MSG-P4-002" and detail "You cannot read the account and arrears data here. Your role does not include it."
    And the read path runs no query on "v_ace_account", "v_ace_bucket_log", "v_ace_product" or "v_ace_branch"
    And no row is written to any table of schema "rwb_source_data"

  Scenario: AC7 A blank account_key is refused and names the field before any view is read (new, D-RCV-60)
    Given a caller whose Case record right R is present
    When the caller asks the read path with a blank account_key in the path
    Then the answer is 400 "application/problem+json" with messageCode "MSG-GEN-001", field "id" and detail "Enter account_key."
    And the read path runs no query on "v_ace_account", "v_ace_bucket_log", "v_ace_product" or "v_ace_branch"

  Scenario: AC8 A column the view does not carry is absent from the answer, with no value invented (new, D-RCV-60)
    Given the published fixture of "v_ace_account" omits one of the columns that RWB-ACE-001 is still to add
    When the read path is asked for account_key "ACC0000017" for business date "2026-11-30"
    Then the answer is 200 and has no property for the omitted column
    And every property of the account answer maps to a column of the four views
    And no table, column or row for it exists in schema "rwb_source_data"
    And the column is listed once in RWB-ACE-001

  Scenario: AC9 The grant, constraint and type rules of BR3, BR4, BR5 and BR10 are proved by check (new, D-RCV-60)
    Given the deployed schema "rwb_source_data" and the "rwb_source_data" login
    When the grants of the login, the constraints of the schema and the columns of "rwb_source_data.account_ext" are queried, and "recovery.ace_to_date" is given a dirty text date and "recovery.ace_to_boolean" a dirty Y/N flag
    Then the login holds SELECT and no INSERT, UPDATE, DELETE or TRUNCATE on the 30 views and holds no privilege in "public"
    And no foreign key on "account_key" references a table outside the schema, "account_ext" holds no column copied from ACE, and the dirty date and the dirty flag each return NULL

  Scenario: AC10 A view failure after a successful view read answers 503 with no partial answer
    Given "v_ace_account" answers for "ACC0000017" and the statement on "v_ace_bucket_log" is cancelled by its statement timeout
    When the read path is asked for account_key "ACC0000017" for business date "2026-11-30"
    Then the answer is 503 "application/problem+json" with messageCode "MSG-GEN-006"
    And it carries no account, bucket, product or branch field
    And no row, event or decision record is written

  Scenario: AC11 The business date and the population of the read follow the stamp and apply no days-past-due filter
    Given "v_ace_account" also holds account_key "ACC0000018" with days_past_due 89
    And the DP01 stamp in use is business date "2026-11-30" with status LOADED
    When "ACC0000017" and "ACC0000018" are each asked for business date "2026-11-30" on "2026-12-01"
    Then both answers are 200 with business date "2026-11-30"
    Given an ALS batch whose "completed_at" equals the "expected_by" of DP01 for the expected date
    When the gated read checks DP01
    Then the stamp component reports the batch late, DP01 answers STALE and the gated read answers 409 MSG-P1-001
    Given FreshnessQuery answers DP01 with businessDate null, status STALE and staleSince null, with sourceExtractedAt and loadedAt absent
    When the gated read checks DP01
    Then it answers 409 MSG-P1-001 identifying DP01 and returns no account fact
    When an authorised caller reads the account through getAccount
    Then the answer is 200 with account facts and the never-stamped DP01 freshness
    And a reader requiring a data date omits X-Data-As-Of and shows the stale banner

  Scenario: AC12 Authentication and field masking follow the authorise answer
    Given a request with no session, a session denied by authorise, an allow that marks "account_name" and "special_memo" masked, and an allow that marks them clear
    When each requests account_key "ACC0000017"
    Then the answers are 401 "MSG-P4-001", 403 "MSG-P4-002", 200 with both fields masked and 200 with both fields clear
    And the two refused calls run no query on the four views
    Given the authorise fake does not answer within 2 s
    Then the answer is 503 "MSG-GEN-006" with no field
```

The twelve criteria above are new and test only this deliverable: the read path over the four views and the Flyway version that replaces the migration. They belong to no legacy criterion, because RWB-DM-001 withdrew AC1 to AC3 with the migration (legacy "Withdrawn IDs" row), so no legacy AC text is copied into this story. AC1 and AC3 are the removal in the schema and in the build; AC2, AC4 and AC5 are the read; AC6 is the refusal; AC7 is the refusal of a request without account_key; AC8 is the column the view does not carry. AC9 is the grant, constraint and type check of BR3, BR4, BR5 and BR10; AC10 is the partial failure, AC11 the business date and population, and AC12 authentication and masking. This read applies no days-past-due filter: the accounts at 90 or more days past due of REQ-RDF-002 are selected for case entry by `listEligibleAccounts` (RD-P1-010), and every one of them is readable here by its `account_key`. No threshold, no volume, no percentage, no currency amount and no date that a source does not give appears in them.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | ACE holds the one copy of the account, the arrears, the balances, the bucket history and the product and branch lists, and the Workbench loads none of it: these rows are read through the views and never copied, staged or loaded | Legacy RWB-DM-001 "Why" row; D-RCV-35 (U1); FSD P1 v3 A2.3 "What this module does instead"; TSD P1 v3 T3.10 |
| BR2 | The recovery module reads ACE only through `recovery.v_ace_*`; a direct `public.*` read in a story, a spec or a query is a defect | BR-P1-001-2; ADR-010; DP-05 |
| BR3 | No constraint in schema `recovery` references a table outside it: a link to an ACE record is a business-key column `varchar(255)` with no foreign key, and `account_key` is that link here | BR-P1-001-3; TSD P1 v3 T3.9 |
| BR4 | The recovery service identity holds SELECT on the views and the recovery tables it needs and no INSERT, UPDATE, DELETE or TRUNCATE on any view or any `public` table | BR-P1-001-4; Architecture v5 slides 29 and 41; DP-02 |
| BR5 | An extension table holds a Workbench decision about an ACE record and never a copy of an ACE column; `account_ext` is keyed by `account_key` and holds `dispute_open`, and this story writes none of it | BR-P1-001-5; FSD P1 v3 A2.1.3.2 (DF-EXT-027, DF-EXT-028); TSD P1 v3 T3.5 |
| BR6 | DP01 stays in the catalog with system of record "ACE (ingested from ALS)" and its view list; only the migration story leaves | Legacy RWB-DM-001 "Data product" row; FSD P1 v3 A2.2.2 DP01 row; BR-P1-002-2 |
| BR7 | For DP01 a failed or late batch leaves the product STALE. Operations that require daily completeness return 409 MSG-P1-001 with the product and last stamped date, when present. getAccount returns DP01 freshness without gating the entity response | RD-P1-041; RD-P1-060; RD-P1-062 |
| BR8 | The service runs its own Flyway sequence in its own schema; the legacy migration is not carried, and no version of the sequence creates an account or arrears table | DP-15; ADR-021; TSD P1 v3 T3.2; legacy "Withdrawn IDs" row |
| BR9 | Every read that shows ACE data shows the business date and the status of its data product | TSD P1 v3 T3.7 "Display" row (API-P1-009, API-P1-010) |
| BR10 | A text date becomes a date through `recovery.ace_to_date` and a Y/N flag becomes a boolean through `recovery.ace_to_boolean`, both returning NULL rather than failing, so a dirty ACE row never breaks a read | BR-P1-001-7; TSD P1 v3 T3.2 helper functions |

Where each rule lives in the target: BR1, BR6 and BR8 are the removal and the catalog, and this story proves them in the schema and in the history. BR2 and BR4 are the boundary, proved by the grant and by the boundary test of the service. BR3 and BR5 keep the Workbench decision tables apart from the ACE rows. BR7 and BR9 make the freshness visible on the read. BR10 is the view contract's own type rule, consumed here and not re-implemented.

### 9. State transitions

None for the case. This story changes no case status, no stage and no task: the case state machine lives in rwb-case and this story never reads or writes it. The only two moves are the version of the schema and the go-live of the read path.

| From | Event | Condition | To |
|---|---|---|---|
| `rwb_source_data` at the baseline and the view versions | this story's Flyway version is applied | The four views exist and the grant is in place | The history holds the version, the schema is unchanged, and the removal of the legacy migration is recorded |
| The read path not deployed | The service is deployed with the read path and the flag on | The P1 read contract answers | The read path serves the account and arrears answer; no row is written by the move |
| The account and arrears read path live | The flag is switched off | The platform flag library answers | The read path serves nothing and the screens show no account or arrears value; no data changes |

The efs ledger style record of the deploy is the Flyway history row and the pipeline log; this story publishes no event that announces either move.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward and data product owner | Owns DP01, its system of record "ACE (ingested from ALS)" and its view list, and reads the freshness the read answers with (FSD P1 v3 A2.2.3.3) |
| RW-TRIBE, squad member and tribe lead | Builds the read path, runs the contract and component tests, and applies the version on the per-service sequence |
| RW-COE, center of excellence analyst | Reads the catalog entry and the view list that DP01 names (FSD P1 v3 A2.2.3.3) |
| The rwb-source-data service identity (the `rwb_source_data` login) | Runs the SELECT on the four views and writes no row of any ACE or Workbench table at run time |
| No delegation of authority level applies | The read takes no credit decision and changes no case |

The role codes are rows of rwb-access, and the read authorises through the guard of the published operation; this story adds no role and no grant of its own. The read calls the authorise operation of rwb-access once per request (RWB-P4-E1037-CON), and returns each field clear or masked as the answer marks it; `account_name` and `special_memo` are masked unless the answer marks them clear. The four role codes named in the Work Package reduce to the three a source holds: RW-DATASTEW, RW-TRIBE and RW-COE. RW-CUSTSERV is named by no source document, is not a role in Users Roles and Permissions v5, and is not used here (GAP-0551; ASM-0787).

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-001 to DF-ACE-042 | `v_ace_account` | `account_key` to `expiry_date`, 42 fields: the account, the arrears, the balances, the classification, the flags and `data_as_of` | Read, one SELECT per request, keyed by `account_key`; never written |
| DF-ACE-140 to DF-ACE-145 | `v_ace_bucket_log` | 6 fields: the month-end bucket history, keyed by `account_key`, year and month | Read, one SELECT per request; never written |
| DF-ACE-146 to DF-ACE-150 | `v_ace_product` | 5 fields: the product, the product group and the category lists, keyed by `product_code` | Read, one SELECT per request; never written |
| DF-ACE-151 to DF-ACE-154 | `v_ace_branch` | 4 fields: the branch and region lists, keyed by `branch_code` | Read, one SELECT per request; never written |
| None: framework table | `flyway_schema_history` | The version, the description and the checksum of this story's version | Write, one row, at deploy only |

Field IDs are those in the Logical Data Model and Data Dictionary v9 and in TSD P1 v3 T3.3 and T3.4. `rwb_source_data` holds no copy of any of these four views: no account table, no payment table, no balance or arrears table, no bucket table, no product table and no branch table exists in the schema, and this story's version creates none. The seven standard record columns of TSD P1 v3 T3.0 are carried by Workbench tables and never by a view, so no view field of this story is written or versioned by the Workbench.

`account_ext` is not touched here: it is an extension table keyed by `account_key` that holds the Workbench decision `dispute_open` and never a copy of an ACE column (BR5), and it belongs to RWB-P1-E1069-DB.

The names `loan_account`, `account_payment`, `collections_history`, `load_run` and `dq_exception` are removed objects of the withdrawn key (D-RCV-35 (U1)). They are not fields or entities of Logical Data Model v9 or Data Classification v5, and this story names them only as removed objects and in the negative tests of section 16.

### 12. Contract

**12.1 REST operations provided**

None new. The account and arrears read is answered behind the P1 read contract of this service, and this story adds no path, no query parameter and no response field of its own. The two operations the read sits behind belong to other RWB-SVC-P1 stories and are named here, not claimed:

| Operation | Base | Owner story | What this story puts behind it |
|---|---|---|---|
| GET /accounts/{accountKey} (getAccount) | /api/recovery/source-data/v1 | RWB-P1-E1069-APP | Account with relations, accountFacts and DP01 freshness; no freshness refusal (RD-P1-060) |
| `GET /data-products/freshness` | `/api/recovery/source-data/v1` | RWB-P1-E1015-APP (contract RWB-P1-E1015-CON) | The business date and status the read answers with |

The single-account entity read follows the published contract. Eligibility and daily completeness on listEligibleAccounts follow RD-P1-010. The legacy extraction and load operations are withdrawn.

**12.2 REST operations consumed**

One call: `POST /api/recovery/access/v1/authorise` (P4 rwb-access, contract RWB-P4-E1037-CON), once per read, one hop, 2 s; a timeout answers 503 and returns no field. The DP01 stamp is read in process through `FreshnessQuery`, and the four views are read over the service's own login. The read is reached by its callers through the P1 read contract above.

**12.3 Events published**

None. The read is synchronous and this story publishes no Kafka event, writes no outbox row and adds no schema to `rwb.source-data.events.v1`. The AceDataReady and AceDataLate events of this service are outbox rows of RWB-P1-E1015-APP.

**12.4 Events consumed**

None. Nothing starts the read: it is asked for by a caller and answered in the caller's thread.

**12.5 Workflows and activities**

None. No Temporal workflow, no activity and no child workflow is in this story. ReconciliationWorkflow (JOB-04) is a child of AceIngestCheck owned by RWB-P1-E1011-APP.

**12.6 Schedules**

None. No Temporal Schedule and no Quartz job sits in this story.

**12.7 Tables owned**

| Table | Schema | Owner (ownership map) | This story |
|---|---|---|---|
| `flyway_schema_history` | `rwb_source_data` | P1 | Writes one row for its own version at deploy |
| `data_product`, `data_product_load`, `sys_objects`, `sys_fields`, `data_contract`, `data_product_access` | `rwb_source_data` | P1 | Not written and not read: the catalog and the freshness stamp belong to RWB-P1-E1001-APP and RWB-P1-E1015-APP; the stamp is read only through `FreshnessQuery` |
| `account_ext`, `party_ext`, `contact_point_ext`, `valuation_ext` | `rwb_source_data` | P1 | Not written and not read: the extension tables belong to RWB-P1-E1069-DB |

There is no account or arrears table in `rwb_source_data`, and this story adds none: the four views are read on the `rwb_source_data` login, and the schema stores no copy of an account, a payment, a balance, an arrears position, a bucket, a product or a branch. No statement in this story names a table in `public` and no statement names another service's schema (DP-01, DP-05).

**12.8 Contract fakes**

| Fake | Serves | Used for |
|---|---|---|
| View fixture (`v_ace_account`, `v_ace_bucket_log`, `v_ace_product`, `v_ace_branch`) | The four views, as synthetic rows in a container | AC2 to AC5, from Day 1, with no ACE data |
| P1 read contract fake (RWB-P1-E1069-APP) | GET /accounts/{accountKey} on /api/recovery/source-data/v1 | Entity response, freshness and 404 path |
| rwb-access authorise fake (RWB-P4-E1037-CON via the guard of the published operation) | The Case record right R answer, the field markers and a timeout | AC6, AC12 |
| FreshnessQuery stub | The DP01 stamp in use: LOADED, STALE and never stamped | AC5 and AC11, with no freshness table written |

**12.9 Call-type summary**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 new operations | 1: authorise | getAccount answers entity facts with DP01 freshness; date-qualified gated operations apply the DP01 gate |
| Kafka | None | None | No event published or consumed |
| Temporal | None | None | No workflow, activity or schedule |
| File | None | None | The read is a request and an answer; no file and no claim-check store |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata.arrears`, in the service root `th.co.scb.ace.workbench.recovery.sourcedata`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`, login `rwb_source_data`, topic `rwb.source-data.events.v1` and task queue `rwb-source-data` (neither used by this story).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AccountArrearsReadRepository | Repository | The only SQL of the story: one SELECT per view on `v_ace_account`, `v_ace_bucket_log`, `v_ace_product` and `v_ace_branch`, keyed by `account_key` and `product_code` or `branch_code`; no write, no `public` table, no other schema |
| AccountArrearsQueryService | Service | Assembles the answer: the account fields, the bucket history newest month first, the product and branch names, the ACE business date and the DP01 status; a missing account is a 404 MSG-P4-003 and writes nothing |
| AccountArrearsBatchGate | Service | Checks the DP01 stamp for daily completeness and returns 409 MSG-P1-001 on a gated read; getAccount includes the stamp in its answer |
| `V<seq>__rwb_p1_dm001_account_arrears_read_path.sql` | Migration | The next free version of the per-service sequence at build time: creates no table, no column, no index and no grant, and records in its description that the legacy account and arrears migration does not ship |
| ViewFixture | Test fixture | Synthetic rows for the four views, in a container, with no ACE data |

**Pattern application**

| DP code | legacy marker | microservice pattern | dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |

DP-05 applies in its own-service form: this is the service that owns the views, so the read is its own SQL on its own login and no contract hop is added. DP-15 gives the sequence the version runs on and the history row that records the removal. No other pattern of the table applies: there is no event (DP-09), no parameter or reference read (DP-06, DP-07), no guard library of this story's own (DP-08), no outbound call (DP-11), no cross-service adapter (DP-16) and no screen (DP-19).

**Database and migrations**

- Reads the four views; writes no row at run time. The only write of the story is the Flyway history row of its own version.
- The version creates no table, no column, no index and no constraint: the account and arrears rows are ACE's and the schema stores no copy of them (BR1, BR8). It carries the description that records the removal, so the next reader of the schema and of the history finds both facts.
- No grant is made or changed: the `rwb_source_data` login and its SELECT on the 30 views are RWB-P1-E1069-DB's, and the view definitions are RWB-P1-E1069-APP's.
- The version number is the next free one on the sequence at build time. The legacy migration file name of the withdrawn key is given by no source: the story asserts that no version names an extract, a transform, a load or a reconciliation of migrated account or arrears rows, rather than naming a file that the sources do not hold (GAP-0550; ASM-0786).

**Configuration and reference data**

- No parameter and no reference list is read: DP-06 and DP-07 are not in this story's pattern set. The business date and the status come from the DP01 stamp, and the cut-off is `data_product.expected_by`, never a value in code (RD-P1-041).
- The entity response shape and field names follow getAccount in rwb-source-data.yaml 5.1.0 (RD-P1-060).
- The feature switch is `rwb.source-data.account-arrears-read`, from the platform flag library: off, the read serves no account or arrears row and the screens show no value from it.
- The login is `rwb_source_data` (Architecture v5 slide 29): SELECT on the 30 views and no privilege in `public`.

**Build steps**

1. AccountArrearsReadRepository over the four views with the ViewFixture; prove one SELECT per view and no write; tests for AC2.
2. AccountArrearsQueryService: the field-ID order of the answer, the bucket history newest month first, the product and branch names, and the ACE business date; tests for AC2 and AC3.
3. The 404 path with no bucket, no product and no branch and no write; test for AC4.
4. AccountArrearsBatchGate on the `FreshnessQuery` stub with the LOADED, STALE and never-stamped cases; tests for AC5 and AC11.
5. The refusal path through the guard of the published operation, with no view read after a deny; test for AC6.
6. The migration `V<seq>__rwb_p1_dm001_account_arrears_read_path.sql` as a no-op on the schema with the removal in its description, and the repeated-apply check; test for AC1.
7. The contract-fake run of the whole path, so the story builds before the read contract, the freshness stamp and the database story are live.

**Feature flag.** `rwb.source-data.account-arrears-read`, from the platform flag library. Off: the read path serves nothing, the migration still applies because it creates nothing, and the history row still records the removal. **Rollback (RD-P1-045).** Switch the flag off first; redeploy the previous image tag only if the flag does not cover the fault; never reverse a migration, and correct a faulty one with a new forward version.

**Done when.** Section 16 verifies the account facts and freshness, the 409 path on a gated read, the ungated getAccount response, and the zero-write and schema boundaries.

### 14. Validation and messages

| ID | Type | When | Message |
|---|---|---|---|
| MSG-P1-001 | Warning | 409: the DP01 stamp in use is not LOADED for the requested business date | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-001 | Error | 401: no session or no Workbench role | As published in the Error and Message Standard |
| MSG-P4-003 | Error | 404: no view row, or outside the caller's scope | As published in the Error and Message Standard |
| MSG-GEN-006 | Error | 503: a view read fails or times out, or authorise does not answer | As published in the Error and Message Standard |
| MSG-GEN-001 | Error | The request carries no `account_key` | Enter {field}. |
| MSG-P4-002 | Error | The caller's Case record right R is absent | You cannot {action} here. Your role does not include it. |

MSG-GEN-001 and MSG-P4-002 are copied character for character from the legacy master (legacy RWB-DM-001 sibling sections and FSD P1 v3 VR-P1-001-1). MSG-P1-001 is copied from the Error and Message Standard v4 (CG-ALL-1888), whose stale-load text reads 'load' (FSD P1 v3 OQ-P1-07). For MSG-P1-001, {product} is the product code the read answers with ("DP01") and {date} is the last completed business date of the ACE batch; for MSG-GEN-001, {field} is "account_key"; for MSG-P4-002, {action} is "read the account and arrears data" and never a case fact or a field value. When DP01 has never been stamped, the gated read refuses with 409 MSG-P1-001 with {product} filled and {date} left empty, and tests assert the code and the product only (RD-P1-062). Pending: the MSG-P1-001 wording for a product never stamped, owner Error and Message Standard owner (UX content lead), tracked as GAP-3284. No other message is raised by this story.

### 15. Screens and states

No screen in this story. The account and the arrears are shown by the case screens that RWB-P1-E1069-APP's read contract serves and by the case and collection screens owned by other services; this story adds no screen, no route and no rendering. The states it exposes to those screens are two:

| State | What the read answers |
|---|---|
| Current | The account fields, the bucket history, the product and the branch, with the ACE business date of the COMPLETED batch and the status of DP01 |
| Stale | Show DP01 STALE. The gated read returns 409 MSG-P1-001; getAccount still returns the entity. If DP01 has never been stamped, omit X-Data-As-Of, show the stale banner, leave data_as_of and input age null, and fail any input-age check that needs the date (RD-P1-062) |

An account with no view row answers 404 and not as an empty account, so a case whose account_key resolves to nothing is visible as a broken link rather than as a zero balance (AC4; the REC-05 orphan rule of the reconciliation story).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-001-01 | AC1, AC2, AC3, AC4, AC5; BR1, BR2, BR6, BR7, BR8, BR9 | Component | One synthetic account_key "ACC0000017" with a `v_ace_account` row, two `v_ace_bucket_log` rows, one `v_ace_product` row and one `v_ace_branch` row; an ALS batch COMPLETED for 2026-11-30 and one with 2026-11-27 as its last complete date; account_key "ACC0000099" with no view row; the story's version applied once and again; a row count of every table of `rwb_source_data` before and after |
| TC-DM-001-04 | AC6; BR4 | Component | A caller whose Case record right R is absent in the authorise fake, asking for "ACC0000017"; a second call with the right present for the contrast |
| TC-DM-001-05 | AC7, AC8, AC9; BR3, BR5, BR10 | Component | A request with no `account_key`; a read that would need a column `v_ace_account` does not carry; a constraint check of schema `recovery` showing `account_key` with no foreign key; `account_ext` checked for ACE columns; a dirty text date and Y/N flag through `recovery.ace_to_date` and `recovery.ace_to_boolean` returning NULL |
| TC-P1-DM001-APP-01 | AC2 | Component and contract | Synthetic view fixture with "ACC0000017", FreshnessQuery stub |
| TC-P1-DM001-APP-02 | AC4 | Component | An `account_key` with no view row |
| TC-P1-DM001-APP-03 | AC5 | Component | A DP01 stamp that is not LOADED for the requested business date |
| TC-P1-DM001-APP-04 | AC8 | Component | A read needing a column the view does not carry |
| TC-P1-DM001-APP-05 | AC9 | Component | The grant, constraint and type checks |
| TC-P1-DM001-APP-06 | AC10 | Component | A view failure after a successful view read |
| TC-P1-DM001-APP-07 | AC11 | Component | Late and never-stamped stamps, days past due 89 and 90 |
| TC-P1-DM001-APP-08 | AC12 | Component and contract | rwb-access authorise fake: 401, 403, masked, clear and timeout; "ACC0000018" |

The two legacy test case IDs are kept, with their legacy numbering. The legacy test text of TC-DM-001-01 to TC-DM-001-04 is withdrawn with the migration (legacy "Withdrawn IDs" row), so the Covers column names the new criteria of this story and not a legacy AC. The full new test, with its Given, When and Then, is recorded in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID. Both levels are Component: TC-DM-001-01 exercises the repository, the query service and the migration in one container against the view fixture, and TC-DM-001-04 exercises the refusal at the component boundary of the published operation. No integration copy of these cases exists, because the read path is inside this service.

### 17. Guardrails

- No business value in code: the business date, the status, the product and the branch all come from ACE rows; the story writes no threshold, no cut-off, no currency amount and no date, and it names no product or branch value.
- Personal data is carried by this read and never appears as real data in logs, tests or prompts: the fixtures are synthetic and the account_key is synthetic. Data Classification v5 classes view fields of this answer as personal data, among them `account_key`, `account_code` and `contract_no` (indirect identifiers, Confidential), `account_name` and `special_memo` (direct identifiers, Restricted, masked unless the role may see them), the balance and arrears facts and the branch `address` and `phone` (Confidential), and `collection_officer`, `relationship_manager` and `relationship_manager_phone` (staff identifiers). Logs carry the id of the read and never the clear `account_key`, `account_code` or `contract_no`, and never `account_name` or `special_memo`; a read of those two is audited through the ACE Common PII path. The customer record of DP02 and `v_ace_customer` belong to RWB-P1-DM002-APP and are not in this answer.
- ACE data only through the owner's contract or `v_ace_*` views, and here the service is the owner of the views: one login, SELECT only, no `public` table named in any statement (BR2, BR4).
- No copy of an ACE row: there is no account, payment, balance, arrears, bucket, product or branch table in `rwb_source_data`, and the version of this story creates none (BR1, BR8).
- The read never writes: no INSERT, no UPDATE and no DELETE at run time, and the only write of the story is the Flyway history row at deploy.
- A stale product is never served as current: the read names the business date, the status and MSG-P1-001 instead (BR7, BR9).
- A dirty ACE row never breaks the read: the view's `ace_to_date` and `ace_to_boolean` return NULL rather than failing (BR10).
- One version on the per-service sequence, never edited in place; a later change is a new version with its own history row (DP-15).

### 18. Traceability

| Legacy RWB-DM-001 row | Value (verbatim) | Where it lands |
|---|---|---|
| Module | P1 Recovery data engine | Service rwb-source-data, service epic RWB-SVC-P1 |
| Status | Removed | Section 1, section 2 and section 19 of this file |
| Decision | D-RCV-35 (U1) | BR1, BR8; the removal recorded in the migration description |
| Why | ACE ingests the ALS account, arrears and balance data and holds the one copy. The Workbench loads none of it, so there is nothing to extract, transform, load or reconcile. | Section 2 quotation; BR1 |
| Read path instead | v_ace_account for the account, the arrears, the balances, the classification and the ACE business date; v_ace_bucket_log for the monthly bucket history; v_ace_product and v_ace_branch for the product and branch lists | Section 2 quotation; sections 4, 11 and 13; AC2 and AC3 |
| Data product | DP01 stays in the catalog with system of record "ACE (ingested from ALS)" and its view list. Only the migration story leaves. | BR6; AC5 names DP01 |
| Withdrawn IDs | AC1 to AC3; TC-DM-001-01 to TC-DM-001-04 | Section 7 note; section 16 note |
| Later home | None. Any column the Workbench still needs is raised once in RWB-ACE-001. | Section 4 step 7; X6; section 19 |

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-002 | Account balance, arrears, payments and classification for every account at 90 or more days past due are read from ACE through `v_ace_account`, current to the previous working day | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-01 | All recovery processes | BR1, BR2, BR7, BR9 | TC-DM-001-01 |

| Pattern | Source | Applied as |
|---|---|---|
| DP-05 | Template and Rules §R5.5 | The four views are read by this service on its own login, and by no other service (section 13) |
| DP-15 | Template and Rules §R5.5 | The version on the per-service sequence, with the history row that records the removal (section 13, AC1) |
| DP-06 | Template and Rules | Not applied: not in this story's pattern set and no reference list of rwb-case is read; product and branch names come from `v_ace_product` and `v_ace_branch` (sections 3 and 4) |
| DP-07 | Template and Rules | Not applied: not in this story's pattern set; the story reads no parameter (section 3) |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1044-CON | Contract | H build dependency: the per-service Flyway sequence and its history |
| RWB-P1-E1069-APP | App development | Publishes the P1 read contract the account read is answered behind; out of scope here |
| RWB-P1-E1069-DB | ACE DB | Creates the login, the grant and the extension tables; X, tracked and not blocking |
| RWB-P1-E1015-APP | App development | Alone stamps the freshness of DP01 and answers it through `FreshnessQuery` |
| RWB-P1-E1013-APP | App development | The business-day readiness operations; not called by this story |
| RWB-P1-DM002-APP | App development | The customer and party read path, the same pattern on DP02; not this story |
| RWB-P1-E1011-APP | App development | ReconciliationWorkflow, including REC-05 on the rwb-case key list; not this story |
| RWB-ITG-DM003-ITG | Integration | Proves the business keys across the services, with DP01 read through this service's contract |

External dependencies: None. The story adds no X row of its own; RWB-P1-E1069-DB is tracked as the external dependency of the legacy key at the story that owns it.

### 19. Out of scope

- The extract, the transform, the load, the load checks, the reconciliation of migrated rows and the cutover of the legacy migration: withdrawn by D-RCV-35 (U1) with AC1 to AC3 and TC-DM-001-01 to TC-DM-001-04, and built nowhere.
- The views themselves, the per-service login and its grant: RWB-P1-E1069-DB and RWB-P1-E1069-APP. This story neither creates, alters nor grants a view.
- The P1 read contract and the freshness stamp: RWB-P1-E1069-APP and RWB-P1-E1015-APP. This story adds no operation and no path.
- The readiness trigger, the AceDataReady and AceDataLate events and the freshness report: RWB-P1-E1013-APP (readiness trigger) and RWB-P1-E1015-APP (events, stamps and freshness).
- DP02 Customer and party, `v_ace_customer`, `v_ace_contact`, `v_ace_ca_relation`, `v_ace_party_product`, `party_ext` and `contact_point_ext`: RWB-P1-DM002-APP.
- Data product catalogs, the dictionary, the data contracts and the access rows: RWB-P1-E1001-APP.
- The reconciliation to `v_ace_account`, REC-01, REC-02, REC-05 and the break list: RWB-P1-E1011-APP. P1 holds no case list.
- The data lake, INT-19 and INT-20: removed, and no story of this key needs lake data (DP-17).
- The columns RWB-ACE-001 adds to `account`: raised once with the ACE team and read here after they land, never copied.
- The case state machine, the screens that show an account and the routes that compose them: rwb-case and the screen owners, not this story.

### 20. Remaining delivery steps

- Size the story (squad, role RW-TRIBE); size is not specified (finding #10).
- Record the signed epic design of EP08 (product owner).
- Publish the pinned getAccount contract fake at 5.1.0 (contract owner).
- Provide the contract fake and the synthetic view fixtures in DEV (squad).
