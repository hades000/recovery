# RWB-P1-DM001-APP Migrate account and arrears

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

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
| Depends on (build) | RWB-PLT-E1044-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the account and arrears read path that replaces the withdrawn RWB-DM-001 migration, and the per-service Flyway version that records the removal, split for rwb-source-data. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P1-DM001-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **data steward (RW-DATASTEW) and a squad member (RW-TRIBE)**, I want **the account and arrears read path of rwb-source-data to answer for an account_key from `v_ace_account`, `v_ace_bucket_log`, `v_ace_product` and `v_ace_branch` at the ACE business date with no Workbench copy, and the per-service Flyway sequence to create nothing for those rows and to record the removal of the legacy migration**, so that **every recovery screen reads the one copy ACE holds, and no second copy of an account or of its arrears can ever disagree with it**.

**The legacy key is withdrawn, and this story is the rework that replaces it.** RWB-DM-001 Migrate account and arrears carries **Status: Removed** and **Decision: D-RCV-35 (U1)**: "ACE ingests the ALS account, arrears and balance data and holds the one copy. The Workbench loads none of it, so there is nothing to extract, transform, load or reconcile." AC1 to AC3 and TC-DM-001-01 to TC-DM-001-04 are withdrawn by the same row. This story therefore extracts nothing, transforms nothing, loads nothing, reconciles no migrated row and cuts nothing over, and it builds no staging table, no load job and no cutover plan: there is nothing to migrate. The story title is kept because Template and Rules §R5.2 keeps the legacy compact and the legacy title; the deliverable under it is the read path.

What it builds instead is exactly what the legacy "Read path instead" row names, and the boundary of the realignment holds it:

- **Stays in rwb-source-data (P1), schema `rwb_source_data`:** the account and arrears read path, its repository and the read service, and the Flyway history row of this story's own version. DP01 Account and arrears stays in the data product catalog with system of record "ACE (ingested from ALS)" and its view list; only the migration story leaves (legacy "Data product" row; FSD P1 v3 A2.2).
- **Stays in ACE, where it already is:** the account, the arrears, the balances, the classification, the ACE business date, the monthly bucket history and the product and branch lists, read through the four Section A views (FSD P1 v3 A2.3 "What this module does instead"; TSD P1 v3 T3.3 views 1, 12, 13 and 14).
- **Removed by D-RCV-35 (U1) and not carried anywhere:** `loan_account`, `account_payment`, `collections_history`, `load_run`, `dq_exception` and the inbound interfaces and the load job of the legacy key (TSD P1 v3 T3.10; FSD P1 v3 A2.3 "Removed objects"). Any column the Workbench still needs is raised once in RWB-ACE-001 and never copied here.
- **Database access:** one login per service (DP-02), the `rwb_source_data` login of Architecture v5 slide 29, which holds SELECT on the 30 `recovery.v_ace_*` views and nothing in `public`. Only rwb-source-data reads those views (Architecture v5 slides 8, 9, 29 and 41; ADR-010).
- **Per-service migrations:** the per-service Flyway sequence in `rwb_source_data` (DP-15, ADR-021). This story's version adds no table, no column and no index for an account or an arrears row; it records that the legacy migration does not ship.
- **Read contract:** the read path is answered behind the P1 read contract that RWB-P1-E1069-APP publishes on base `/api/recovery/source-data/v1`, and the freshness that RWB-P1-E1013-APP stamps. This story adds no path of its own and claims neither operation.
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
- The ACE batch record and the freshness of DP01 are live: RWB-P1-E1013-APP stamps `data_product_load` from `v_ace_batch_status` and gates the daily data jobs on a complete ACE batch (FSD P1 v3 A2.14; TSD P1 v3 T3.7). `v_ace_batch_status` is a Section B view, so until RWB-ACE-001 lands every source-fed product shows STALE with no business date and no data job starts on its own (TSD P1 v3 T3.7, "Before Section B").
- The platform Flyway contract RWB-PLT-E1044-CON is in place: the per-service sequence of `rwb_source_data` with its V0001 baseline, and the versions for the Section A and Section B views (TSD P1 v3 T3.2; DP-15). This story takes the next free version after those (V0004 at the time of writing, proposed) and creates no account or arrears object in it.
- No build dependency blocks the start: RWB-PLT-E1044-CON is a platform contract story, so the story is Day 1 under Template and Rules §R5.7 rules 1 and 8. The wave 4 tag is the W-MAP tag of EP08 and does not delay the build (GAP-0548; ASM-0784).
- The parameters and the reference data of rwb-case are not preconditions of this build: DP-06 and DP-07 are not in this story's pattern set, and the story reads no parameter and no reference list. Where a configurable value would be needed (the per-source cut-off that marks DP01 late), no source gives it to this deliverable, so the story answers from the ACE batch row and writes no constant: a parameter would be a rwb-case read and would need its own change (GAP-0547; ASM-0783).
- The read is reached through the P1 read contract on base `/api/recovery/source-data/v1`, one hop, 2 s (the service standard of Template and Rules §R5.5 DP-11 and ADR-020), and the operation is RWB-P1-E1069-APP's. Architecture v5 slide 15 names `GET /accounts/{id}` in the P1 contract; the TSD P1 v3 Appendix T-A endpoint inventory does not list it, so the story puts its read path behind that path and adds none of its own (GAP-0549; ASM-0785).
- The rwb_source_data login exists (Architecture v5 slide 29) and holds SELECT on the views only, with no INSERT, UPDATE, DELETE or TRUNCATE on any view and no privilege in `public` (BR-P1-001-4; Architecture v5 slides 29 and 41).
- The service template, the outbox and inbox libraries and the feature flag library are present in the repository (Architecture v5 slide 20). This story publishes no event and writes no outbox row.

### 4. Flow

1. A caller of the P1 read contract asks for one account by `account_key` for a business date. The account_key is the business key of the ACE account; the Workbench holds no identifier of its own for it (BR-P1-001-3).
2. The guard of the published operation answers first: the read path runs only on an allow, and a caller whose Case record right R is absent is refused before any view is touched (MSG-P4-002).
3. AccountArrearsBatchGate reads `v_ace_batch_status` for source system ALS and the business date under test, on the same login and the same view contract as the rest of the read. On a COMPLETED row it carries that business date to the answer. On a late or absent row it serves no account or arrears row as current for that date and answers DP01 as stale with its last completed date and MSG-P1-001 (BR7, AC5). The freshness stamp that the data-product read and the screens display is RWB-P1-E1013-APP's; this story reads the batch row for its own answer, writes no stamp and calls no service for it.
4. AccountArrearsReadRepository issues one SELECT per view, keyed by `account_key`, on the `rwb_source_data` login: `v_ace_account` for the account, the arrears, the balances, the classification, the flags and `data_as_of`; `v_ace_bucket_log` for the month-end bucket history; `v_ace_product` for the product and product group; `v_ace_branch` for the branch and the region (DP-05).
5. AccountArrearsQueryService assembles one answer: the account fields in field-ID order, the bucket history newest month first, and the product and branch names resolved from the two list views. It carries the ACE business date and the status of DP01 and nothing derived by the Workbench.
6. No row in `v_ace_account` for the `account_key` means the account is not in ACE at that business date: the answer is not-found, no bucket, product or branch is returned, and nothing is written (AC4).
7. A value that a source does not give to this deliverable is never guessed on the read: for example the 7 ALS columns that RWB-ACE-001 adds to `account` are not in `v_ace_account` yet, so the read answers without them and the column is raised once in RWB-ACE-001 (TSD P1 v3 T3.4 note; T3.11 point 1; legacy "Later home" row).
8. No step writes a row: the read path holds no INSERT, no UPDATE and no DELETE, and the service never caches an ACE row into its own schema. The only row the story writes is the Flyway history row of its own version, at deploy (AC1, AC3).
9. Every view read is a single statement on the service's own login, under the statement timeout of the SQL view grant (Architecture v5 slides 29 and 41). No statement names a table in `public` and no statement names another service's schema (BR-P1-001-2, BR-P1-001-4).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A view read fails: the relation is absent or the statement errors | The answer is 503 with no partial account, no bucket history and no product or branch; nothing is written and no stale row is served as current | None | AC1 (the version asserts the views are the only source), component test |
| X2 | The ALS batch for the business date is not COMPLETE | The batch gate holds the row: the read answers DP01 as stale with its last completed business date and serves no account or arrears row as current for that date | MSG-P1-001 | AC5 |
| X3 | The caller's Case record right R is absent | The call is refused before any view is read; no row is returned and nothing is written | MSG-P4-002 | AC6 |
| X4 | `v_ace_account` holds no row for the `account_key` | The answer is not-found, with no bucket, product or branch, and nothing is written | None | AC4 |
| X5 | The request carries no `account_key` | The answer is refused and names the field; no view is read | MSG-GEN-001 | Component test |
| X6 | The read would need a column that `v_ace_account` does not carry | The field is absent from the answer and the column is raised once in RWB-ACE-001; no value is invented and no copy is created | None | Not a legacy AC; the legacy "Later home" row |
| X7 | The story's Flyway version is applied a second time | Flyway reports it as already applied; no row is written twice and no version is edited in place | None | AC1 |

The message texts are the legacy ones, unchanged (section 14). X1 and X5 are component tests of this story and carry no new message ID.

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
    Given "v_ace_batch_status" shows the ALS batch COMPLETED for business date "2026-11-30"

  Scenario: AC1 The Flyway sequence creates nothing for account and arrears and records the removal (new, D-RCV-60)
    Given the per-service Flyway sequence of schema "rwb_source_data" with its V0001 baseline applied
    When the version of this story is applied
    Then the schema holds no table named "loan_account", "account_payment", "collections_history", "load_run" or "dq_exception"
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
    And it names the ACE business date "2026-11-30" and the status of data product DP01
    And the count of account, payment, balance, arrears, bucket, product and branch rows in schema "rwb_source_data" is 0 before and after the read

  Scenario: AC3 The read path returns no account copy and the Workbench holds zero account or arrears rows (new, D-RCV-60)
    Given the service is deployed with the read path live and the four views reachable
    When a caller asks for account_key "ACC0000017"
    Then the answer holds only view fields: "DF-ACE-001" to "DF-ACE-042", "DF-ACE-140" to "DF-ACE-145", "DF-ACE-146" to "DF-ACE-150" and "DF-ACE-151" to "DF-ACE-154"
    And no field of the answer comes from a table in schema "rwb_source_data"
    And the service holds no entity, no table and no repository class named "loan_account", "account_payment" or "collections_history"
    And schema "rwb_source_data" holds no table for an account, a payment, a balance, an arrears position, a bucket, a product or a branch

  Scenario: AC4 An account with no view row answers not-found and writes nothing (new, D-RCV-60)
    Given "v_ace_account" holds no row for account_key "ACC0000099"
    When the read path is asked for account_key "ACC0000099"
    Then the answer is not-found, with no account, no bucket history, no product and no branch
    And no row is written to any table of schema "rwb_source_data"
    And no freshness stamp is written for the read
    And the read leaves "v_ace_account" and the three list views unchanged

  Scenario: AC5 The batch gate holds the read when the ALS batch of the business date is not COMPLETE (new, D-RCV-60)
    Given "v_ace_batch_status" holds no COMPLETED row for source system ALS and business date "2026-11-30"
    And its last COMPLETED row for ALS is business date "2026-11-27"
    When the read path is asked for account_key "ACC0000017" for business date "2026-11-30"
    Then no account and no arrears row is served as current for "2026-11-30"
    And the answer names data product "DP01" with business date "2026-11-27" and status STALE
    And the message is MSG-P1-001 "{product} is from {date}. Today's ACE batch has not arrived." with "{product}" as "DP01" and "{date}" as "2026-11-27"

  Scenario: AC6 A caller without the read right is refused with MSG-P4-002 (new, D-RCV-60)
    Given a caller whose Case record right R is absent in the authorise answer of the rwb-access contract fake
    When the caller asks for account_key "ACC0000017"
    Then the call is refused with 403 and message MSG-P4-002 "You cannot {action} here. Your role does not include it."
    And the read path runs no query on "v_ace_account", "v_ace_bucket_log", "v_ace_product" or "v_ace_branch"
    And no row is written to any table of schema "rwb_source_data"
```

The six criteria above are new and test only this deliverable: the read path over the four views and the Flyway version that replaces the migration. They belong to no legacy criterion, because RWB-DM-001 withdrew AC1 to AC3 with the migration (legacy "Withdrawn IDs" row), so no legacy AC text is copied into this story. AC1 and AC3 are the removal in the schema and in the build; AC2, AC4 and AC5 are the read; AC6 is the refusal. No threshold, no volume, no percentage, no currency amount and no date that a source does not give appears in them.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | ACE holds the one copy of the account, the arrears, the balances, the bucket history and the product and branch lists, and the Workbench loads none of it: these rows are read through the views and never copied, staged or loaded | Legacy RWB-DM-001 "Why" row; D-RCV-35 (U1); FSD P1 v3 A2.3 "What this module does instead"; TSD P1 v3 T3.10 |
| BR2 | The recovery module reads ACE only through `recovery.v_ace_*`; a direct `public.*` read in a story, a spec or a query is a defect | BR-P1-001-2; ADR-010; DP-05 |
| BR3 | No constraint in schema `recovery` references a table outside it: a link to an ACE record is a business-key column `varchar(255)` with no foreign key, and `account_key` is that link here | BR-P1-001-3; TSD P1 v3 T3.9 |
| BR4 | The recovery service identity holds SELECT on the views and the recovery tables it needs and no INSERT, UPDATE, DELETE or TRUNCATE on any view or any `public` table | BR-P1-001-4; Architecture v5 slides 29 and 41; DP-02 |
| BR5 | An extension table holds a Workbench decision about an ACE record and never a copy of an ACE column; `account_ext` is keyed by `account_key` and holds `dispute_open`, and this story writes none of it | BR-P1-001-5; FSD P1 v3 A2.1.3.2 (DF-EXT-027, DF-EXT-028); TSD P1 v3 T3.5 |
| BR6 | DP01 stays in the catalog with system of record "ACE (ingested from ALS)" and its view list; only the migration story leaves | Legacy RWB-DM-001 "Data product" row; FSD P1 v3 A2.2.2 DP01 row; BR-P1-002-2 |
| BR7 | A source-fed product is stale when the ACE batch is late or failed, and the read carries the product, the business date and the message rather than serving the row as current | VR-P1-001-1; FSD P1 v3 A2.14; TSD P1 v3 T3.7 |
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

The role codes are rows of rwb-access, and the read authorises through the guard of the published operation; this story adds no role and no grant of its own. The four role codes named in the Work Package reduce to the three a source holds: RW-DATASTEW, RW-TRIBE and RW-COE. RW-CUSTSERV is named by no source document and is not used here (GAP-0551; ASM-0787).

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

### 12. Contract

**12.1 REST operations provided**

None new. The account and arrears read is answered behind the P1 read contract of this service, and this story adds no path, no query parameter and no response field of its own. The two operations the read sits behind belong to other RWB-SVC-P1 stories and are named here, not claimed:

| Operation | Base | Owner story | What this story puts behind it |
|---|---|---|---|
| `GET /accounts/{id}` | `/api/recovery/source-data/v1` | RWB-P1-E1069-APP | The account and arrears read path over the four views |
| `GET /data-products/freshness` | `/api/recovery/source-data/v1` | RWB-P1-E1013-APP | The business date and status the read answers with |

Architecture v5 slide 15 names `GET /accounts/{id}` in the P1 contract, while TSD P1 v3 Appendix T-A lists API-P1-001 to API-P1-016 and no account operation; the story therefore puts its read path behind the path the architecture names and claims no operation of its own (GAP-0549; ASM-0785). The extraction, the load, the load-check and the tracker operations of the legacy key are withdrawn with it and are not listed anywhere here.

**12.2 REST operations consumed**

None. At run time this story calls no service, uses no contract client and holds no C dependency: it reads four views over the service's own login. The read is reached by its callers through the P1 read contract above, one hop, with a 2 s budget. That budget is the service standard fixed in Template and Rules §R5.5 DP-11 and ADR-020; DP-11 is not a pattern this story applies, and it adds no timeout of its own.

**12.3 Events published**

None. The read is synchronous and this story publishes no Kafka event, writes no outbox row and adds no schema to `rwb.source-data.events.v1`. The AceDataReady and AceDataLate events of this service are RWB-P1-E1013-APP's.

**12.4 Events consumed**

None. Nothing starts the read: it is asked for by a caller and answered in the caller's thread.

**12.5 Workflows and activities**

None. No Temporal workflow, no activity and no child workflow is in this story, and the JOB-04 reconciliation workflow of this service is not part of the deliverable: it belongs to RWB-P1-DM003-APP's key.

**12.6 Schedules**

None. No Temporal Schedule and no Quartz job sits in this story.

**12.7 Tables owned**

| Table | Schema | Owner (ownership map) | This story |
|---|---|---|---|
| `flyway_schema_history` | `rwb_source_data` | P1 | Writes one row for its own version at deploy |
| `data_product`, `data_product_load`, `sys_objects`, `sys_fields`, `data_contract`, `data_product_access` | `rwb_source_data` | P1 | Not written and not read: the catalog and the freshness stamp belong to RWB-P1-E1001-APP and RWB-P1-E1013-APP |
| `account_ext`, `party_ext`, `contact_point_ext`, `valuation_ext` | `rwb_source_data` | P1 | Not written and not read: the extension tables belong to RWB-P1-E1069-DB |

There is no account or arrears table in `rwb_source_data`, and this story adds none: the four views are read on the `rwb_source_data` login, and the schema stores no copy of an account, a payment, a balance, an arrears position, a bucket, a product or a branch. No statement in this story names a table in `public` and no statement names another service's schema (DP-01, DP-05).

**12.8 Contract fakes**

| Fake | Serves | Used for |
|---|---|---|
| View fixture (`v_ace_account`, `v_ace_bucket_log`, `v_ace_product`, `v_ace_branch`, `v_ace_batch_status`) | The four views and the batch record, as synthetic rows in a container | AC2 to AC5, from Day 1, with no ACE data |
| P1 read contract fake (RWB-P1-E1069-APP) | `GET /accounts/{id}` on `/api/recovery/source-data/v1` | The answer shape and the not-found path, AC3 and AC4 |
| rwb-access authorise fake (RWB-P4-E1037-CON via the guard of the published operation) | The Case record right R answer | AC6 |
| Batch-status fixture | The `v_ace_batch_status` rows of source system ALS, COMPLETE and late | AC5, with no freshness table written |

**12.9 Call-type summary**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 new operations | 0 | The read is answered behind RWB-P1-E1069-APP's `GET /accounts/{id}` and RWB-P1-E1013-APP's freshness read; one hop, 2 s, the service standard of §R5.5 DP-11 |
| Kafka | None | None | No event published or consumed |
| Temporal | None | None | No workflow, activity or schedule |
| File | None | None | The read is a request and an answer; no file and no claim-check store |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata.arrears`, in the service root `th.co.scb.ace.workbench.recovery.sourcedata`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`, login `rwb_source_data`, topic `rwb.source-data.events.v1` and task queue `rwb-source-data` (neither used by this story).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AccountArrearsReadRepository | Repository | The only SQL of the story: one SELECT per view on `v_ace_account`, `v_ace_bucket_log`, `v_ace_product` and `v_ace_branch`, keyed by `account_key` and `product_code` or `branch_code`; no write, no `public` table, no other schema |
| AccountArrearsQueryService | Service | Assembles the answer: the account fields, the bucket history newest month first, the product and branch names, the ACE business date and the DP01 status; a missing account is a not-found and writes nothing |
| AccountArrearsBatchGate | Service | Reads `v_ace_batch_status` for source system ALS and the business date, and answers DP01 as stale with its last completed date and MSG-P1-001 when the batch is not COMPLETE; the freshness stamp itself is RWB-P1-E1013-APP's |
| `V0004__dm001_account_arrears_read_path.sql` | Migration | The next free version of the per-service sequence (V0004 at the time of writing, proposed): creates no table, no column, no index and no grant, and records in its description that the legacy account and arrears migration does not ship |
| ViewFixture | Test fixture | Synthetic rows for the four views and the batch record, in a container, with no ACE data |

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
- The version number is the next free one on the sequence (V0004 at the time of writing, proposed, after V0001, V0002 and V0003 of TSD P1 v3 T3.2). The legacy migration file name of the withdrawn key is given by no source: the story asserts that no version names an extract, a transform, a load or a reconciliation of migrated account or arrears rows, rather than naming a file that the sources do not hold (GAP-0550; ASM-0786).

**Configuration and reference data**

- No parameter and no reference list is read: DP-06 and DP-07 are not in this story's pattern set. The business date and the status come from the ACE batch row, and no cut-off value is written in code (GAP-0547; ASM-0783).
- The answer shape, the paging and the field names are the published P1 read contract's, not this story's (GAP-0549; ASM-0785).
- The feature switch is `rwb.source-data.account-arrears-read`, from the platform flag library: off, the read serves no account or arrears row and the screens show no value from it.
- The login is `rwb_source_data` (Architecture v5 slide 29): SELECT on the 30 views and no privilege in `public`.

**Build steps**

1. AccountArrearsReadRepository over the four views with the ViewFixture; prove one SELECT per view and no write; tests for AC2.
2. AccountArrearsQueryService: the field-ID order of the answer, the bucket history newest month first, the product and branch names, and the ACE business date; tests for AC2 and AC3.
3. The not-found path with no bucket, no product and no branch and no write; test for AC4.
4. AccountArrearsBatchGate on `v_ace_batch_status` with the COMPLETE and the late case; test for AC5 against the batch-status fixture.
5. The refusal path through the guard of the published operation, with no view read after a deny; test for AC6.
6. The migration `V0004__dm001_account_arrears_read_path.sql` as a no-op on the schema with the removal in its description, and the repeated-apply check; test for AC1.
7. The contract-fake run of the whole path, so the story builds before the read contract, the freshness stamp and the database story are live.

**Feature flag.** `rwb.source-data.account-arrears-read`, from the platform flag library. Off: the read path serves nothing, the migration still applies because it creates nothing, and the history row still records the removal.

**Done when.** The tests of section 16 pass, `rwb_source_data` holds no account or arrears table, the read answers the four views at the ACE business date with zero rows written, the late-batch answer names DP01 and MSG-P1-001, the refusal answers MSG-P4-002, and no class of the service names a `public` table.

### 14. Validation and messages

| ID | Type | When | Message |
|---|---|---|---|
| MSG-P1-001 | Warning | The ALS batch for the business date is not COMPLETE, so DP01 is stale | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-001 | Error | The request carries no `account_key` | Enter {field}. |
| MSG-P4-002 | Error | The caller's Case record right R is absent | You cannot {action} here. Your role does not include it. |

The three messages are copied character for character from the legacy master (legacy RWB-DM-001 sibling sections and FSD P1 v3 VR-P1-001-1); their wording follows the ACE batch and ACE rather than a load and ALS (FSD P1 v3 OQ-P1-07). For MSG-P1-001, {product} is the product code the read answers with ("DP01") and {date} is the last completed business date of the ACE batch; for MSG-GEN-001, {field} is "account_key"; for MSG-P4-002, {action} is "read the account and arrears data" and never a case fact or a field value. No other message is raised by this story.

### 15. Screens and states

No screen in this story. The account and the arrears are shown by the case screens that RWB-P1-E1069-APP's read contract serves and by the case and collection screens owned by other services; this story adds no screen, no route and no rendering. The states it exposes to those screens are two:

| State | What the read answers |
|---|---|
| Current | The account fields, the bucket history, the product and the branch, with the ACE business date of the COMPLETED batch and the status of DP01 |
| Stale | No account or arrears row served as current for the business date, with DP01's last completed business date, its status STALE and MSG-P1-001 |

An account with no view row shows as not-found and not as an empty account, so a case whose account_key resolves to nothing is visible as a broken link rather than as a zero balance (AC4; the REC-05 orphan rule of the reconciliation story).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-001-01 | AC1, AC2, AC3, AC4, AC5; BR1, BR2, BR6, BR7, BR8, BR9 | Component | One synthetic account_key "ACC0000017" with a `v_ace_account` row, two `v_ace_bucket_log` rows, one `v_ace_product` row and one `v_ace_branch` row; an ALS batch COMPLETED for 2026-11-30 and one with 2026-11-27 as its last complete date; account_key "ACC0000099" with no view row; the story's version applied once and again; a row count of every table of `rwb_source_data` before and after |
| TC-DM-001-04 | AC6; BR4 | Component | A caller whose Case record right R is absent in the authorise fake, asking for "ACC0000017"; a second call with the right present for the contrast |

The two legacy test case IDs are kept, with their legacy numbering. The legacy test text of TC-DM-001-01 to TC-DM-001-04 is withdrawn with the migration (legacy "Withdrawn IDs" row), so the Covers column names the new criteria of this story and not a legacy AC. The full new test, with its Given, When and Then, is recorded in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. Both levels are Component: TC-DM-001-01 exercises the repository, the query service and the migration in one container against the view fixture, and TC-DM-001-04 exercises the refusal at the component boundary of the published operation. No integration copy of these cases exists, because the read path is inside this service.

### 17. Guardrails

- No business value in code: the business date, the status, the product and the branch all come from ACE rows; the story writes no threshold, no cut-off, no currency amount and no date, and it names no product or branch value.
- No personal data in logs, tests or prompts: the fixtures are synthetic, the account_key is synthetic, and no customer, contact or identity field is in this story's answer at all (DP02 and `v_ace_customer` belong to RWB-P1-DM002-APP).
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

| Pattern | Source | Applied as |
|---|---|---|
| DP-05 | Template and Rules §R5.5 | The four views are read by this service on its own login, and by no other service (section 13) |
| DP-15 | Template and Rules §R5.5 | The version on the per-service sequence, with the history row that records the removal (section 13, AC1) |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1044-CON | Contract | H build dependency: the per-service Flyway sequence and its history |
| RWB-P1-E1069-APP | App development | Publishes the P1 read contract the account read is answered behind; out of scope here |
| RWB-P1-E1069-DB | ACE DB | Creates the login, the grant and the extension tables; X, tracked and not blocking |
| RWB-P1-E1013-APP | App development | Stamps the freshness of DP01 and gates on the ACE batch |
| RWB-P1-DM002-APP | App development | The customer and party read path, the same pattern on DP02; not this story |
| RWB-P1-DM003-APP | App development | The case-list reconciliation and its break list, including REC-05; not this story |
| RWB-ITG-DM003-ITG | Integration | Proves the business keys across the services, with DP01 read through this service's contract |

External dependencies: None. The story adds no X row of its own; RWB-P1-E1069-DB is tracked as the external dependency of the legacy key at the story that owns it.

### 19. Out of scope

- The extract, the transform, the load, the load checks, the reconciliation of migrated rows and the cutover of the legacy migration: withdrawn by D-RCV-35 (U1) with AC1 to AC3 and TC-DM-001-01 to TC-DM-001-04, and built nowhere.
- The views themselves, the per-service login and its grant: RWB-P1-E1069-DB and RWB-P1-E1069-APP. This story neither creates, alters nor grants a view.
- The P1 read contract and the freshness stamp: RWB-P1-E1069-APP and RWB-P1-E1013-APP. This story adds no operation and no path.
- The readiness trigger, the AceDataReady and AceDataLate events and the freshness report: RWB-P1-E1013-APP.
- DP02 Customer and party, `v_ace_customer`, `v_ace_contact`, `v_ace_ca_relation`, `v_ace_party_product`, `party_ext` and `contact_point_ext`: RWB-P1-DM002-APP.
- Data product catalogs, the dictionary, the data contracts and the access rows: RWB-P1-E1001-APP.
- The case-list reconciliation to `v_ace_account`, REC-01, REC-02, REC-05 and the break list: RWB-P1-DM003-APP.
- The data lake, INT-19 and INT-20: removed, and no story of this key needs lake data (DP-17).
- The columns RWB-ACE-001 adds to `account`: raised once with the ACE team and read here after they land, never copied.
- The case state machine, the screens that show an account and the routes that compose them: rwb-case and the screen owners, not this story.
