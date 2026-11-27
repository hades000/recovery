# RWB-P1-DM009-APP Migrate debt sale

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-DM009-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-DM-009 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P1-DM009-APP-16) |
| Patterns applied | DP05, DP15, DP19 |
| Parallel lane | L-P1-A |
| Ready to start | After RWB-P1-E1001-APP, RWB-P1-E1069-APP; the platform contract stories RWB-PLT-E1044-CON and RWB-PLT-N001-CON published |
| Depends on (build) | RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| Contract dependencies | None |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7), additive inside /v1 (RD-P1-005); this story provides no operation, event or workflow of its own |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-005, RD-P1-011, RD-P1-012, RD-P1-021, RD-P1-027, RD-P1-040, RD-P1-042, RD-P1-045 |

**Change log.** D-RCV-60, 22 November 2026: realignment of legacy RWB-DM-009 into the rwb-source-data cutover extract of the debt sale lots and their account links, the no-copy boundary against `v_ace_account` and `v_ace_payment`, the handover to rwb-debtsale and the cutover evidence; AC1 and AC3 kept word for word, AC2 moved to RWB-ITG-DM009-ITG. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-DM009-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (16 resolved, 13 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: targeted edits for version 3. Tool: Claude Sonnet 5.5.

**Version 3 changes** (D-RCV-60 P1 developer readiness):

- The handover is a closed field list by dictionary ID; of the case only the case key travels; `outstanding` is not carried (RD-P1-027; findings #2, #12).
- `migration_source` and `migrated_at` replace the undefined source and migration tags (RD-P1-027; finding #2).
- DL25 option A with `recon.tolerance.pct` version 1 = 0.00 and one clean-day definition (RD-P1-042; finding #9).
- Exception paths and the sign-off refusal now have criteria, and replay is covered (AC7 to AC11; findings #3, #4).
- Consumed reads, rerun, workflows, rollback and the classification of the carried identifiers follow the register and Data Classification v6 (findings #1, #5, #6, #11, #13).
- The story no longer lists SCR-45 empty, loading, error or no-access states as its own (finding #10).
- Finishing pass: a refused sign-off answers MSG-P1-023 (RD-P1-042); message references are Error and Message Standard v6; test case IDs of Test Cases v9 cited.

### 1. Story

As a **data steward (RW-DATASTEW)**, I want **the legacy Workbench debt sale lot and debt sale account records extracted once at cutover and handed to rwb-debtsale with every lot fact and every account key kept whole, together with the evidence of ten clean days and the sign-off**, so that **a sale in flight keeps its accounts, its reserve price and its buyer**.

The legacy key is not withdrawn: RWB-DM-009 Migrate debt sale keeps its place in the legacy master with its epic E2, its release 31 December 2026 and its decision DL25. The realignment changes where the rows live and who moves them. DP09 Debt sale is a Workbench-only data product with **no ACE source system** (FSD P1 v3 A2.2.2 data product table; A2.14.2), and the live lot and account-link records belong to S6 rwb-debtsale in schema `rwb_debtsale` on S6's own Flyway sequence (DP-15). This story therefore carries exactly three things and nothing else:

- **The cutover extract.** The legacy Workbench `debt_sale_lot` rows (`DF-SAL-020` to `DF-SAL-030`, `lot_no`, `cut_off_date`, `segment`, `reserve_price` and `buyer_partner_id` first among them), the `debt_sale_account` rows (`DF-SAL-031` to `DF-SAL-037`, with `lot_id`, `account_key`, `borrower_code`, `selling_price` and `put_back_status`) and the `recovery_case` rows of the cases a sold account sits in are read once from the cutover dump. The lot and link fields of section 11 are kept whole; of the case only its key (`DF-CAS-001`) travels (data minimisation, RD-P1-027). Values are copied, never derived; P3 rwb-case keeps the case table and this story writes no row of it (AC1).
- **The no-copy boundary, proved rather than asserted.** AC1 says no balance and no payment is copied *because both are read from `v_ace_account` and `v_ace_payment`*. The step therefore reads view 1 `v_ace_account` (42 fields, `DF-ACE-001` to `DF-ACE-042`, keyed by `account_key`) and view 2 `v_ace_payment` (12 fields, `DF-ACE-043` to `DF-ACE-054`, keyed by `payment_code` and `account_key`) on the service's own login and carries no amount into the package (TSD P1 v3 T3.3 views 1 and 2; DP-05). `debt_sale_account.outstanding` (`DF-SAL-035`) is an ACE reuse of `v_ace_account.total_balance` in the dictionary and the package carries no value for it.
- **The handover and the cutover evidence.** The extract leaves as one handover package per cutover business date; the load into `rwb_debtsale` is S6's own cutover step, and P1 holds no INSERT against another service's schema (DP-01; ASM-3498). Ten clean days are counted from the `reconciliation_result` rows that JOB-04 writes for the migrated records, a break resetting the count; the data steward then signs off, the legacy tables stay read-only for their retention period and the migrated records are served from the new schema (AC3; ASM-3500, ASM-3501).

The per-service Flyway version (DP-15) is the fourth artifact and is deliberately empty of schema: it creates no table, no column and no index for a lot or for an account link, and records the extract's definition, its field list and the read-only window in its history description (TSD P1 v3 T3.2). The version number is the next free one on the sequence and is not fixed here.

**What this story does not build.** No REST operation, no Kafka event, no Temporal workflow, no Schedule and no screen: the cutover runs as one-off bulk work from the release pipeline against the service's own admin operations, and the reconciliation behind the cutover result is read on SCR-45 Data quality through the gateway-bff composite route (DP-19, H RWB-PLT-N001-CON). Section 12 states the emptiness table by table.

### 2. Business rationale

A debt sale lot is a promise to a buyer before it is a transfer of accounts. The lot was cut off at a date, split into a segment, priced with a reserve and awarded to a buyer, and every account on it was offered under a selling price and a put-back term. At cutover that sale in flight survives only if the migrated record still shows the cut-off date the buyer bid against, the same segment, the same reserve price and the same buyer, and if every account link still carries the `account_key` that resolves to the ACE row holding the balance and the payment. A lot that loses its cut-off date is a sale the bank cannot evidence; an `account_key` that resolves to nothing is an account sold and not transferred. The legacy story says it in its own words:

> **Epic** E2, release 31 December 2026
>
> **Module** P1 Recovery data engine
>
> **Depends on** RWB-E1-001, RWB-E1-069
>
> **Decision** DL25
>
> **Story** As a data steward, I want the debt sale lots and their accounts migrated from the legacy Workbench, so that a sale in flight keeps its accounts, its reserve price and its buyer.

**Why P1 extracts and S6 loads.** The lot is S6's: rwb-debtsale is the debt sale service, with schema `rwb_debtsale` and its own Flyway sequence (DP-15). The cutover machinery and the reconciliation are P1's: the service owns the ACE view contract, the extension tables, freshness and reconciliation (context pack P1 ownership rows; `reconciliation_result` is a P1 table) and DP-01 forbids a service writing another service's tables. So the only lawful shape is the one this story takes: P1, the reader of the `recovery.v_ace_*` views (DP-05), reads the legacy dump and the two views, keeps the referential proof and the cutover evidence in its own schema, and hands the lot rows to the service that owns them. A P1 that loaded `rwb_debtsale` would break the boundary; an S6 that read `v_ace_account` would break the single-reader rule (ASM-3498).

**Why no balance and no payment is copied.** A balance is a value ACE recomputes every business date and a payment is a value ACE owns outright; a copy of either is a second answer to a question that already has one. AC1 states the rule in one line: the sale record carries the lot facts and the account key, and the money is read from the two views when a screen, a buyer file or a proceeds match needs it (TSD P1 v3 T1.1 "no copy"). DP-05 sits in the pattern set of a migration story for exactly this reason: the boundary is only proved if the reader that replaces the copy exists.

**Why ten clean days, and why they rest on the reconciliation rows.** DP09 is a Workbench-only product: it has no ACE source system, no `data_product_source` row and so no freshness stamp, and is never STALE (RD-P1-021). Its records are S6's, and the P1 records operation answers 400 E400 for DP09, naming the owning service: FSD P1 v3 puts it in the "None; Workbench records, current on change" line of the product-to-source map, so no ACE batch and no `data_product_load` row can date it. Its recency proof can only be the daily reconciliation, which already resolves every business key against its view row (REC-05) and writes one `reconciliation_result` row per check and product group (FSD P1 v3 A2.11). Ten consecutive clean days on the migrated records, a break resetting the count, is the evidence that the moved records behave like records that were always there (AC3; ASM-3500).

### 3. Preconditions

- **The two views exist and are granted.** RWB-P1-E1069-APP creates the `recovery.v_ace_*` views, `v_ace_account` and `v_ace_payment` among them, on the per-service Flyway sequence, and RWB-P1-E1069-DB grants SELECT on them to the `rwb_source_data` login with no privilege in `public` (TSD P1 v3 T3.2, T3.3; DP-05).
- **The reconciliation runs and writes its rows.** RWB-P1-E1011-APP owns JOB-04 (`ReconciliationWorkflow`, a child of `AceIngestCheck` after the ALS stamp, RD-P1-040), its REC-01, REC-02 and REC-05 checks and the `reconciliation_result` table it writes, graded PASS or BREAK under `recon.tolerance.pct` version 1 = 0.00 (DL25 option A applied by RD-P1-042; a run that cannot proceed writes no row). Until that story lands, a reconciliation fixture stands in for the rows the clean-day count reads (section 12.8).
- **The per-service Flyway contract is in place.** RWB-PLT-E1044-CON gives the `rwb_source_data` sequence with its `V0001` baseline (TSD P1 v3 T3.2; DP-15); this story takes the next free version after it.
- **The contracts the tests mock.** The P1 reconciliation results read (`GET /api/recovery/source-data/v1/admin/reconciliation/results`, contract RWB-P1-E1011-CON), the P3 case read and the S6 debt sale read that answers with the migrated lot and its account links served from `rwb_debtsale`. They are fakes in the tests (section 12.8) and this story's code calls none of them, so none is a C dependency, because the load the S6 read fronts is S6's own cutover step (ASM-3498; section 12.2).
- **The gateway-bff composite route behind SCR-45 exists.** RWB-PLT-N001-CON is the H dependency of DP-19; the reconciliation behind the cutover result is read through that route and no screen stitches two sources.
- **The cutover step has a place to run.** The release pipeline runs it as one-off bulk work against the service's own API for a business date and never reads or writes a `rwb_*` schema directly. The pipeline step, its job name and its cutover record format: Not specified in the source documents (GAP-2173; ASM-3499).
- **The legacy cutover dump is available once.** The extract is read once from the legacy Workbench cutover dump at the cutover window on the read-only identity granted for it. Its layout, its file name and that identity: Not specified in the source documents (GAP-2173; ASM-3499).
- **The catalog holds DP09.** DP09 Debt sale is a Workbench product, refreshed ON_CHANGE, with `debt_sale_lot` and `debt_sale_account` as its Workbench tables and no ACE source system (FSD P1 v3 A2.2.2; A2.14.2). RWB-P1-E1001-APP owns the catalog rows; this story reads and writes none of them.
- **S6's target tables carry the migration columns.** `debt_sale_lot` and `debt_sale_account` carry `migration_source varchar(20)` and `migrated_at timestamptz`, added by S6 in its own Flyway step (RD-P1-027 item 3; DP-15). The values of list LOV-MIGRATION-SOURCE are Pending: owner data owner (NEW-GAP-B4).
- **No build dependency blocks the start.** RWB-PLT-E1044-CON and RWB-PLT-N001-CON are platform contracts and the other two are in-lane P1 work; the story starts after RWB-P1-E1001-APP and RWB-P1-E1069-APP (Template and Rules §R5.7 rules 2, 3 and 8). The wave 4 tag is the W-MAP tag of EP08 and does not delay the build.

### 4. Flow

1. The cutover window opens and the release pipeline starts the step for one business date and one environment against the service's own admin operations. No scheduler runs it and no operator touches a schema.
2. CutoverDebtSaleExtract reads the legacy cutover dump once: the lot rows (`DF-SAL-020` to `DF-SAL-030`), the account-link rows (`DF-SAL-031` to `DF-SAL-037`) and the case rows of the cases a sold account sits in, from which only the case key `DF-CAS-001` is taken. One pass; the dump is not re-read inside the same cutover business date (AC1).
3. DebtSaleCutoverMapper links each account to its lot and each lot to its case, and keeps the facts the sale rests on whole: `lot_no`, `cut_off_date`, `segment`, `reserve_price`, `buyer_partner_id`, then `account_key`, `borrower_code`, `selling_price` and `put_back_status`, each beside its own `id`. It derives no value and defaults none, and carries no field for a balance and none for a payment (AC1).
4. NoCopyBoundaryReader reads `v_ace_account` keyed by each `account_key` and `v_ace_payment` keyed by `payment_code` and `account_key`, and records per link whether the key resolves. It reads the views, copies no amount and writes no row of ACE (AC1; DP-05).
5. DebtSaleHandoverPackage assembles one handover row per lot and per account link with the section 11 fields, the case key of each link, the cutover business date and its `migration_source` value, and writes the package to the cutover record of the release pipeline, not to a table.
6. The package is handed to rwb-debtsale; S6's own cutover step loads it into `rwb_debtsale` on S6's own sequence. P1 writes no row of that schema and joins nothing across the boundary (DP-01, DP-15). S6's load writes `migration_source` from the package and `migrated_at` as the UTC instant it wrote the row (RD-P1-027 item 3).
7. CutoverEvidenceReader reads the `reconciliation_result` rows JOB-04 writes for the business dates after the load (`DF-OPS-118` to `DF-OPS-129`) and counts the clean days. A day is clean when every REC-01 and REC-02 row of the date is PASS under `recon.tolerance.pct` version 1 and no new REC-05 orphan appears (RD-P1-042 item 4). A BREAK row or a new orphan resets the count to zero and names the day; a date with no result row is not a clean day and does not add to the count (AC3, AC10; ASM-3500).
8. On the tenth consecutive clean day the data steward signs off. The sign-off is held in the cutover record beside the ten day rows and the reconciliation extract they came from; nothing is written to a schema for it (AC3; ASM-3501). Its format and where the pipeline keeps it are agreed at the cutover rehearsal and recorded in the cutover procedure (GAP-2173; ASM-3501).
9. The legacy tables are set read-only for their retention period and the migrated records are served from the new schema: after the sign-off a lot is read from `rwb_debtsale` through the rwb-debtsale contract and not from the legacy table (AC3).
10. At deploy the story's version applies on the per-service sequence, writes one `flyway_schema_history` row and creates no table, no column and no index: its description carries the extract's definition, the field list and the read-only window, so the next reader of the schema finds out what shipped and why (AC1, AC3; DP-15).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The cutover dump is absent, unreadable, or read twice for the same cutover business date | The step stops before any mapping; nothing is handed over and the cutover record names the business date and the reason | MSG-GEN-001 | AC1 |
| X2 | An account link carries no lot, or its lot is not in the extract | The row is refused whole, the step stops and the cutover record names the link and the missing lot; no partial package is handed over | MSG-GEN-001 | AC1 |
| X3 | A required key is empty on a lot or a link, such as `lot_no`, `cut_off_date`, `segment`, `reserve_price`, `buyer_partner_id` or `account_key` | The row is refused whole with the field named; no default and no derived value is substituted | MSG-GEN-001 | AC1 |
| X4 | `v_ace_account` holds no row for an `account_key` | The link is still extracted and handed over with its key and its selling price; the REC-05 step lists the orphan for the data steward and the ACE team, and no balance is invented, copied or defaulted | None | AC1; AC3 (the count resets) |
| X5 | A read of `v_ace_account` or `v_ace_payment` fails: the relation is absent or the statement errors | The step stops with no partial handover and no stale amount carried as current; the cutover record names the view and the business date | None | AC1 |
| X6 | JOB-04 writes a BREAK row or a new REC-05 orphan for a migrated record during the ten days | The clean-day count resets to zero, the day is named and the break is listed for the data steward; the sign-off cannot be recorded | MSG-P1-012 | AC3 |
| X7 | The migration's version is applied a second time | Flyway reports it as already applied; no row is written twice and no version is edited in place | None | AC1 |
| X8 | A caller without the Platform administration right starts the cutover step | The step is refused before any read of the dump or of the views and nothing is written | MSG-P4-002 | AC4; TC-DM-009-04 |

The message texts are the legacy ones, unchanged (section 14). X1, X2, X3, X5 and X7 are component tests of this story and raise no new message ID.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | One extract reader, one mapper, one boundary reader, one handover package, one evidence reader and one Flyway version; the load is S6's and is mocked |
| Negotiable | The package layout and the cutover record are agreed at the cutover rehearsal; this story fixes the lot facts, the account link and the no-copy rule only |
| Valuable | Every lot in flight keeps its cut-off date, segment, reserve price and buyer, every link keeps its key, and the cutover is evidenced rather than asserted |
| Estimable | One batch step, five components, one migration, four fixtures and three test cases |
| Small | Fits one sprint as the P1 slice of a split legacy key |
| Testable | AC1 and AC3 run end to end on a synthetic cutover extract and synthetic reconciliation rows; no production data and no ACE data are needed |

### 7. Acceptance criteria

```gherkin
Feature: Migrate debt sale

  Scenario: AC1 Extract the Workbench records (legacy RWB-DM-009 AC1)
    Given the legacy Workbench debt sale lot and debt sale account records at cutover
    Given the rwb-debtsale contract mock returns the migrated lot with its cut-off date, its segment, its reserve price and its buyer and its account link with its account_key
    When the migration reads them
    Then each lot keeps its cut-off date, its segment, its reserve price and its buyer, and each account link carries an account_key
    And no balance and no payment is copied, because both are read from v_ace_account and v_ace_payment
    And the package holds each source lot and account link exactly once, with every section 11 CARRY and KEY field unchanged, the case key of each link, the cutover business date and "migration_source"
    And the package has no "outstanding" value and no other "recovery_case" field
    And the cutover record lists each "account_key" as resolved or orphan against "v_ace_account"
    And no row of any "rwb_source_data" table is added or changed

  Scenario: AC3 Cut over (legacy RWB-DM-009 AC3)
    Given ten clean days on the migrated records
    Given the rwb-debtsale contract mock returns the migrated records served from schema "rwb_debtsale"
    When the data steward signs off
    Then the legacy tables stay read-only for their retention period
    And the migrated records are served from the new schema
    And the ten clean days are ten consecutive business dates on which every REC-01 and REC-02 row is "PASS" under "recon.tolerance.pct" version 1 = 0.00 and no new REC-05 orphan appears
    And the cutover record holds the sign-off, the ten day rows, the reconciliation extract and the read-only window

  Scenario: AC4 A caller without the Platform administration right is refused before any read (new, D-RCV-60)
    Given a caller whose Platform administration right is absent in the authorise fake
    When the caller starts the cutover step for a business date
    Then the step is refused before any read of the dump or of the views, nothing is written and MSG-P4-002 "You cannot run the debt sale cutover extract here. Your role does not include it." is shown
    And the same call with the right present reaches the first read of the dump

  Scenario: AC5 The migration version creates no table, column or index for a lot or a link (new, D-RCV-60)
    Given a schema of the service with no flyway_schema_history row for the migration version
    When the service's own Flyway sequence applies the migration version twice
    Then exactly one flyway_schema_history row exists for the version
    And a schema comparison shows no table, column, index or constraint added by the version
    And the second apply changes no row and no object

  Scenario: AC6 A sign-off before the tenth clean day is refused (new, D-RCV-60)
    Given the cutover record holds nine consecutive clean days
    When the data steward signs off
    Then the sign-off is refused with "MSG-P1-023" "The cutover cannot be signed off. It has 9 clean days and needs 10." and no sign-off entry is written
    And the count stays at nine, the cutover stays in the Ten clean days running state and the refusal is recorded with the business date and the count

  Scenario: AC7 An absent, unreadable or already read dump stops the step (new, X1)
    Given the cutover dump is absent, unreadable or already read for the cutover business date
    When the extract step starts
    Then it stops before mapping with MSG-GEN-001
    And no handover package is written and the cutover record names the business date and the reason

  Scenario: AC8 A malformed lot or link stops the whole run (new, X2 and X3)
    Given a link whose lot is not in the extract, or a lot with an empty "cut_off_date"
    When the mapper processes the extract
    Then the run stops with MSG-GEN-001 naming the field or record
    And the cutover record names the offending row and no partial package is handed over

  Scenario: AC9 A failing view read stops the run (new, X5)
    Given a SELECT on "v_ace_account" or "v_ace_payment" fails
    When the boundary check runs
    Then the run stops without a handover package
    And the cutover record names the view and the business date, and no amount is carried

  Scenario: AC10 A break resets the clean-day count (new, RD-P1-042)
    Given nine consecutive clean business dates after the load
    When the next date holds a "reconciliation_result" row with result "BREAK", or a new REC-05 orphan on a migrated key
    Then the clean-day count is 0 and the cutover record names the date, the REC code and the orphan key
    And the sign-off stays closed and MSG-P1-012 is shown for the date
    And a business date with no "reconciliation_result" row adds no clean day

  Scenario: AC11 Customer data stays inside the handover (new, Data Classification v6)
    Given synthetic links with "account_key", "borrower_code", "selling_price" and "put_back_status" values
    When the extract step writes the package, its logs and its metrics
    Then those values appear in the handover package and, for orphan keys, as "account_key" in the cutover record
    And no log line, metric label, error message or prompt holds one of them
```

AC1 and AC3 are copied character for character from legacy RWB-DM-009. The two added Givens are the rwb-debtsale contract answers: the load into `rwb_debtsale` is S6's own cutover step, so the story states the answer it builds against rather than claiming the load, and neither Given changes a legacy value in the When or Then lines. The added And lines of AC1 and AC3 state the closed field list (RD-P1-027), the clean-day rule (RD-P1-042) and the evidence recorded. A sign-off refused below ten clean days answers MSG-P1-023 (RD-P1-042; it settles NEW-GAP-S13-2); confirmation of its text is Pending, owner Error and Message Standard owner. AC2 Reconcile the business keys is owned by RWB-ITG-DM009-ITG, carries the REC-05 proof across the services and is not copied here (ASM-3503).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The live lot and account-link records are S6 rwb-debtsale's in `rwb_debtsale`; P1 extracts and hands over and never loads another service's schema | Context pack P1 ownership rows; DP-01; DP-15 |
| BR2 | The extract is read once from the legacy cutover dump and lands nothing in `rwb_source_data`: the schema holds no debt sale table and no copy of a lot | Legacy RWB-DM-009 AC1; TSD P1 v3 T3.6; GAP-2173 |
| BR3 | A lot keeps its cut-off date, its segment, its reserve price and its buyer, and a link carries its `account_key`; no value is derived and no default substituted | Legacy RWB-DM-009 AC1; `DF-SAL-020` to `DF-SAL-037` |
| BR4 | No balance and no payment is copied, because both are read from `v_ace_account` and `v_ace_payment`; `outstanding` (`DF-SAL-035`) is ACE-sourced and is not carried | Legacy RWB-DM-009 AC1; TSD P1 v3 T3.3 views 1 and 2; DP-05; RD-P1-027 |
| BR5 | A migrated record keeps its source and its migration date (`migration_source`, `migrated_at`, written by S6's load) and never a copy of an ACE row | Legacy RWB-DM-009 guardrails; TSD P1 v3 T1.1; RD-P1-027 |
| BR6 | Ten consecutive clean days are counted from the JOB-04 `reconciliation_result` rows: a day is clean when every REC-01 and REC-02 row is PASS under `recon.tolerance.pct` version 1 = 0.00 and no new REC-05 orphan appears; a break resets the count | Legacy RWB-DM-009 AC3; FSD P1 v3 A2.11; DL25 option A (RD-P1-042); ASM-3500 |
| BR7 | An ON_CHANGE product with no ACE source system is dated by its reconciliation and not by a freshness stamp, so the count of clean days is its recency proof | FSD P1 v3 A2.2.2 (DP09) and A2.14.2; ASM-3500 |
| BR8 | The sign-off is held in the cutover record, the legacy tables stay read-only for their retention period, and the migrated records are served from the new schema | Legacy RWB-DM-009 AC3; REQ-RDF-013 |
| BR9 | The service runs its own Flyway sequence in its own schema; this story's version creates no table, no column and no index for a lot or a link | DP-15; ADR-021; TSD P1 v3 T3.2 |
| BR10 | ACE data is read only through `recovery.v_ace_*` views, on the service's own login, SELECT only, with no `public` table in any statement; a key with no view row is listed, never deleted or changed | BR-P1-011-3; DP-05; TSD P1 v3 T3.3 |
| BR11 | The package carries only fields of S6's tables whose dictionary system of record is Workbench, the ACE linking key `account_key` and the case key; every other ACE-sourced field is read through the views and never carried. `account_key` and `borrower_code` are indirect identifiers and `selling_price` and `put_back_status` Customer data, Confidential: they leave only inside the handover package and are masked in UAT | RD-P1-027 item 2; Data Classification v6 |

BR1 and BR2 are proved by the schema of `rwb_source_data` and by the absence of a write to `rwb_debtsale`; BR3 by the mapper and the handover row; BR4 by the two view reads and the package holding no amount; BR5 to BR8 by the cutover evidence; BR9 by TC-DM-009-05; BR10 by the view contract it reads.

### 9. State transitions

None for the case: this story changes no case status, stage or task, because the lot status machine is S6's and the case state machine is P3's. The moves are the cutover's own, and they are six.

| From | Event | Condition | To |
|---|---|---|---|
| Cutover not started | The step is started for the business date | The dump is readable and every lot is in it with its links | Extract ready: the rows are mapped and the boundary read is done |
| Extract ready | The handover package is assembled | Every lot carries its four facts and its buyer, every link its `account_key` | Handed over: the package is in the cutover record and with rwb-debtsale |
| Handed over | S6's own cutover step applies its version | S6's sequence is at the version that creates `rwb_debtsale` | Loaded: the migrated records are served from `rwb_debtsale` through the S6 contract |
| Loaded | JOB-04 writes its rows for the business date | Every REC-01 and REC-02 row PASS and no new REC-05 orphan on the day | Ten clean days running, the count at the number of consecutive clean days |
| Ten clean days running | A BREAK row or a new REC-05 orphan appears | The break is listed for the data steward | Ten clean days running, the count at zero |
| Ten clean days running | The tenth day is reached and the data steward signs off | The sign-off is recorded in the cutover record | Signed off: the legacy tables are read-only for their retention period and the records are served from the new schema |

The cutover record is the ledger of each move and the Flyway history row of this story's version is the schema's own record of the deploy. No event announces a move: the sale events belong to rwb-debtsale and rwb-payment, and a migration raises none of them.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward and data product owner | Runs the cutover step for a business date, owns the ten day evidence and records the sign-off (FSD P1 v3 A2.11) |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Hold the Platform administration right R of the legacy permission check and may read the cutover record, the evidence and the reconciliation extract within their scope (legacy RWB-DM-009 permission check) |
| RW-TRIBE, squad member | Builds the extract, the mapper, the boundary read, the package and the evidence reader, and applies the version on the per-service sequence |
| The rwb-source-data service identity (`rwb_source_data` login) | Reads the two views and the reconciliation rows and writes no row of the schema except the Flyway history row of its own version |
| S6 rwb-debtsale and its identity | Owns `rwb_debtsale`, its sequence and the load of the rows handed over; this story takes no right over them |
| No delegation-of-authority level applies | The migration approves no sale and awards no lot; the reserve price and the buyer are copied facts, not decisions |

The role codes are rows of rwb-access and the step authorises through the guard of the published admin operation; this story adds no role and no grant.

### 11. Data

The package fields are one row per Logical Data Model v11 field (RD-P1-027): CARRY is an S6 field whose system of record is Workbench, KEY a linking key, ACE_READ is read through the views and never carried, EXCLUDE does not leave in the package. The same rows are to be held in Source to Target Mapping v7, sheet Migration packages.

| BR Field ID | Entity | Field | Disposition | Note (classification, Data Classification v6) |
|---|---|---|---|---|
| DF-SAL-020 | `debt_sale_lot` | `id` | CARRY | Not personal, Internal |
| DF-SAL-021 | `debt_sale_lot` | `lot_no` | CARRY | Not personal, Internal |
| DF-SAL-022 | `debt_sale_lot` | `cut_off_date` | CARRY | Not personal, Internal |
| DF-SAL-023 | `debt_sale_lot` | `segment` | CARRY | Not personal, Internal |
| DF-SAL-024 | `debt_sale_lot` | `reserve_price` | CARRY | Not personal, Internal |
| DF-SAL-025 | `debt_sale_lot` | `buyer_partner_id` | CARRY | Not personal, Internal |
| DF-SAL-026 | `debt_sale_lot` | `buyer_class` | CARRY | Not personal, Internal |
| DF-SAL-027 | `debt_sale_lot` | `signing_date` | CARRY | Not personal, Internal |
| DF-SAL-028 | `debt_sale_lot` | `approval_authority` | CARRY | Not personal, Internal |
| DF-SAL-029 | `debt_sale_lot` | `payment_terms` | CARRY | Not personal, Internal |
| DF-SAL-030 | `debt_sale_lot` | `status` | CARRY | Not personal, Internal |
| DF-SAL-031 | `debt_sale_account` | `id` | CARRY | Not personal, Internal |
| DF-SAL-032 | `debt_sale_account` | `lot_id` | CARRY | Not personal, Internal |
| DF-SAL-033 | `debt_sale_account` | `account_key` | KEY | Indirect identifier, Confidential; masked in UAT |
| DF-SAL-034 | `debt_sale_account` | `borrower_code` | CARRY | Indirect identifier, Confidential; masked in UAT |
| DF-SAL-035 | `debt_sale_account` | `outstanding` | ACE_READ | System of record core bank (ALS) via COLLINS; read as `v_ace_account.total_balance` |
| DF-SAL-036 | `debt_sale_account` | `selling_price` | CARRY | Customer data, Confidential |
| DF-SAL-037 | `debt_sale_account` | `put_back_status` | CARRY | Customer data, Confidential |
| DF-CAS-001 | `recovery_case` | `id` | KEY | The case of a sold account, as a reference only |
| DF-CAS-002 to DF-CAS-023, DF-CAS-046 to DF-CAS-055 | `recovery_case` | all other fields | EXCLUDE | P3's table; not needed by the debt sale load (data minimisation, RD-P1-027) |
| DF-ACE-001 to DF-ACE-042 | `v_ace_account` | account view fields | Not carried; read | Read keyed by `account_key` to prove the boundary |
| DF-ACE-043 to DF-ACE-054 | `v_ace_payment` | payment view fields | Not carried; read | Read keyed by `payment_code` and `account_key` |
| DF-OPS-118 to DF-OPS-129 | `reconciliation_result` | reconciliation row fields | Not carried; read | Read for the clean day count; written by JOB-04 |
| None (standard columns, LDM v11 sheet Standard columns) | the two S6 tables | `migration_source`, `migrated_at` | Provenance | The package states `migration_source` (values Pending, NEW-GAP-B4); S6's load writes both |
| None: framework table | `flyway_schema_history` | version, description, checksum | Write | One row, at deploy only |
| None: file | The legacy cutover dump | lot, link and case rows | Read | Read once on the cutover read-only identity; never landed in a schema |

`rwb_source_data` holds no debt sale table and no copy of an ACE amount, and this story's version creates none. The segment is carried as the extract holds it and no list is read (LOV-SEGMENT stays the target owner's check). The extract's layout, field order and record format, and the package's location, access and retention, are Pending: agreed at the cutover rehearsal, owner data steward (GAP-2173; ASM-3499).

### 12. Contract

**12.1 REST operations provided**

None. The cutover runs from the release pipeline as one-off bulk work and is not a public operation: this story adds no path, no query parameter and no response field. The admin and reconciliation operations it is started and read through belong to other RWB-SVC-P1 stories and are named in 12.2, not claimed here.

**12.2 REST operations consumed**

None at run time by this story's own code. The step is started and its result read by the pipeline through this service's own admin operations, and the tests read the case and the lot through their owners' published contracts as mocks:

| Caller | Operation | Owner | Why it is not a dependency of this story |
|---|---|---|---|
| The release pipeline | `POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` (API-P1-002, contract RWB-P1-AD018-CON) | P1 rwb-source-data | Same service. Used only to rerun a FAILED `ReconciliationWorkflow` run, with a UUID `Idempotency-Key` (RD-P1-001, RD-P1-012); the cutover is not a job of the job set and this operation does not start it |
| The release pipeline | `GET /api/recovery/source-data/v1/admin/reconciliation/results` (API-P1-003, contract RWB-P1-E1011-CON; replaces the withdrawn `/admin/data-quality/exceptions`) | P1 rwb-source-data | Same service; the cutover record reads its evidence from it |
| The tests | The published rwb-case case read, REST base `/api/recovery/case/v1` | P3 rwb-case | A contract mock only; the extract carries the case as the dump holds it |
| The tests | The published rwb-debtsale lot read, REST base `/api/recovery/debtsale/v1` | S6 rwb-debtsale | A contract mock only; the load into `rwb_debtsale` is S6's own cutover step |

The story therefore holds no C dependency and no I dependency (metadata; ASM-3498). DP-11 is not a pattern of this story: there is no outbound call to build against and no timeout of its own is added.

**12.3 Events published**

None. The cutover publishes no event, writes no outbox row and adds no schema to `rwb.source-data.events.v1`. The service's own two events (EV-26, EV-27) belong to its freshness stories, and the sale events are rwb-debtsale's and rwb-payment's; a migration raises none of them.

**12.4 Events consumed**

None. The step is started for a business date by the release pipeline and reads no topic and no inbox row. The `reconciliation_result` rows it counts are read from the table, not from an event.

**12.5 Workflows and activities**

None added: the story declares no workflow, activity or task queue consumer. JOB-04 `ReconciliationWorkflow`, a child of `AceIngestCheck` (RD-P1-040, RD-P1-012), is a workflow of the service and is exercised here through its rows, not changed. The rwb-debtsale saga that reserves accounts, takes the buyer's payment, transfers the accounts and posts the proceeds is not started, called or changed here.

**12.6 Schedules**

None. The cutover is one-off bulk work and not a Schedule; the daily run that produces the counted rows is JOB-04's own and belongs to RWB-P1-E1011-APP.

**12.7 Tables owned**

| Table | Schema | Owner | This story |
|---|---|---|---|
| `flyway_schema_history` | `rwb_source_data` | P1 | Writes one row for its own version at deploy |
| `reconciliation_result` | `rwb_source_data` | P1 | Read for the clean day count; written by JOB-04 and by no code of this story |
| `debt_sale_lot` | `rwb_debtsale` | S6 | Not written here: the load is S6's own cutover migration (DP-01) |
| `debt_sale_account` | `rwb_debtsale` | S6 | Not written here, for the same reason |
| `recovery_case` | `rwb_case` | P3 | Not written here: the case keys come from the dump and the case is read through the P3 contract |
| `v_ace_account`, `v_ace_payment` | `recovery` | ACE team (views) | Read only, SELECT on the service login; never written |

There is no debt sale table in `rwb_source_data` and no copy of a balance or a payment in it, and this story adds neither. No statement names a table in `public` and none names another service's schema (DP-01, DP-05).

**12.8 Contract fakes**

| Fake | Serves | Used for |
|---|---|---|
| Legacy cutover extract fixture | Synthetic lot, link and case rows with their lots and keys | AC1, from Day 1, with no legacy data |
| View fixture (`v_ace_account`, `v_ace_payment`) | Synthetic account and payment rows for the synthetic `account_key` values, one series with a view row and one without | AC1 and the orphan path of X4 |
| rwb-debtsale contract mock | The migrated lot with its four facts and its buyer, its link with its `account_key`, and the records served from schema `rwb_debtsale` | AC1 and AC3, and the added Given of each |
| Reconciliation extract fixture | The `reconciliation_result` rows JOB-04 writes, PASS, BREAK and the REC-05 orphan row, in the answer shape of `GET /admin/reconciliation/results` of rwb-source-data.yaml 5.1.0 | AC3, AC10 and the reset path of X6 |
| Authorise fake | The Platform administration right R present and absent | TC-DM-009-04 and X8 |

Each fake is generated from the published contract it fronts or from the fixture set agreed at the cutover rehearsal, carries that contract's version (RD-P1-011), so a contract change shows up as a test failure and not as a silent pass. The rwb-debtsale and rwb-case fake versions are recorded when those contracts are published (section 20). Fixture layouts, the dump's file name and the cutover record format: Not specified in the source documents (GAP-2173; ASM-3499).

**12.9 Call-type summary**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 new operations | 0 from this story's code | The cutover is started and read through this service's own admin operations, one hop, 2 s |
| Kafka | None | None | No event published or consumed; the sale events are rwb-debtsale's |
| Temporal | None | None | No workflow, activity or Schedule added; JOB-04 is exercised, not changed |
| File | None | Two | The extract is read once from the legacy cutover dump and the handover package leaves through the cutover record |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata.cutover`, in the service root `th.co.scb.ace.workbench.recovery.sourcedata`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`, login `rwb_source_data`, topic `rwb.source-data.events.v1`, task queue `rwb-source-data`; the topic and the queue are named for completeness and this story uses neither.

| Component | Type | Responsibility |
|---|---|---|
| CutoverDebtSaleExtract | Batch job | The one-off read of the legacy dump for the lots, their links and the cases behind them; one pass per business date, no table, no re-read |
| DebtSaleCutoverMapper | Service | Links each account to its lot and each lot to its case and keeps the facts whole; derives no value and defaults none |
| NoCopyBoundaryReader | Repository | The only SQL of the story: one SELECT on `v_ace_account` keyed by `account_key` and one on `v_ace_payment` keyed by `payment_code` and `account_key`; no write, no `public` table, no other schema |
| DebtSaleHandoverPackage | Service | Assembles the handover rows per lot and per link with the section 11 fields, the case key, `migration_source` and the cutover business date, and writes them to the cutover record |
| CutoverEvidenceReader | Service | Counts the clean days from the JOB-04 rows on the migrated records, resets on a break, and holds the ten day rows beside the sign-off |
| The next free version of the per-service sequence | Migration | Creates no table, no column and no index; records the extract's definition, the field list and the read-only window in its description |
| Cutover fixtures | Test fixture | The legacy extract, the two view fixtures, the rwb-debtsale mock, the reconciliation rows and the authorise fake, all synthetic |

| DP code | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies in its own-service form: this is the service that owns the views, so the boundary read is its own SQL on its own login and adds no contract hop, and no other service reads the two views for itself. DP-15 gives the sequence the version runs on and the history row that records the cutover definition. DP-19 puts the reconciliation behind the cutover result on the composite route of SCR-45 rather than one screen stitching two sources. No other pattern applies: no event (DP-09), no parameter or reference read (DP-06, DP-07), no guard library of this story's own (DP-08), no outbound call (DP-11), no cross-service adapter (DP-16) and no rule evaluation (DP-04).

**Database and migrations.** The story reads the two views and writes no row at run time; its only write is the Flyway history row of its own version. The version creates no table, no column, no index and no constraint, because the lot rows are S6's and the money is ACE's (BR1, BR9). No grant is made or changed: the views and the SELECT of `rwb_source_data` are RWB-P1-E1069-APP's and RWB-P1-E1069-DB's. The version number is the next free one after the `V0001` baseline (TSD P1 v3 T3.2) and is not fixed here.

**Configuration and reference data.** No parameter and no reference list is read: DP-06 and DP-07 are not in the pattern set. The ten day threshold, the cutover business date and the retention period are data of the cutover record, not constants in code. The feature switch is `rwb.source-data.dm009-cutover-extract` from the platform flag library: off, the step refuses to start and no package leaves, while the migration still applies because it creates nothing (ASM-3502). The login is `rwb_source_data`: SELECT on the `recovery.v_ace_*` views and no privilege in `public`. The handover point, the package layout and the cutover record format: Not specified in the source documents (GAP-2173; ASM-3499).

**Rollback (RD-P1-045).** Switch `rwb.source-data.dm009-cutover-extract` off first; redeploy the previous image tag and chart version only if the flag does not cover the fault, and name in the release note every P1 capability the redeploy reverts. A migration is never reversed and no `U*.sql` or down script exists; a faulty version is corrected by a new forward version. This version creates no object, so the previous tag runs unchanged against the schema. A package already loaded by S6 is not undone by P1.

**Build steps.**

1. CutoverDebtSaleExtract over the extract fixture, one pass per business date, with the absent-dump and double-read cases; AC1 and X1.
2. DebtSaleCutoverMapper: the lot facts and the link whole, the case key and the link's keys, no derived value and no default; AC1, X2 and X3.
3. NoCopyBoundaryReader over the two views with the row-present and row-absent fixtures; one SELECT per key series, no write, no amount field in the package; AC1 and X4.
4. DebtSaleHandoverPackage from the mapper and the boundary read, with `migration_source` and the business date, and no row written to a schema; AC1.
5. CutoverEvidenceReader: ten PASS rows count up, a BREAK row resets, a new orphan resets, and the sign-off is refused below ten; AC3 and X6.
6. The migration on the next free version as a no-op with the definition, the field list and the read-only window in its description, plus the repeated-apply check; AC1 and X7.
7. The refusal path through the guard of the admin operation with no read after a deny; TC-DM-009-04 and X8. Then the whole cutover against the mocks, so the story builds before S6's load and before JOB-04's real rows are live.

**Done when.** The tests of section 16 pass, `rwb_source_data` holds no debt sale table and no ACE amount, AC1 hands over a complete package with the two view reads and no copied balance or payment, AC3 counts ten clean days from `reconciliation_result` rows and records the sign-off, and no class of the service names a `public` table or another service's schema.

### 14. Validation and messages

| ID | Type | When | Message |
|---|---|---|---|
| MSG-GEN-001 | Error | The extract lacks a required field or record, such as a lot, a cut-off date, a segment, a reserve price, a buyer or an `account_key` | Enter {field}. |
| MSG-P4-002 | Error | A caller without the Platform administration right starts the cutover step | You cannot {action} here. Your role does not include it. |
| MSG-P1-001 | Warning | The ACE batch behind the boundary read is late for the business date, so the view facts cannot be carried as current | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-012 | Warning | A reconciliation row for a migrated record is BREAK during the ten days, so the count resets | The case list for {date} does not reconcile to ALS for {product}: a difference of {variance} accounts, {pct} percent. |
| MSG-P1-023 | Error | A cutover sign-off is asked below the required count of clean days | The cutover cannot be signed off. It has {count} clean days and needs {required}. |

MSG-GEN-001 and MSG-P4-002 are copied character for character from the legacy master (legacy RWB-DM-009 validation table); MSG-P1-001 and MSG-P1-012 are copied character for character from the Error and Message Standard (current version v6). This story raises MSG-GEN-001 and MSG-P4-002 itself: {field} is the field or record the extract lacks, and {action} is "run the debt sale cutover extract" and never a lot fact. MSG-P1-001 and MSG-P1-012 are raised by the freshness read and by JOB-04, and this story asserts them as evidence rather than producing them. Where section 5 shows "None", no user message is raised and the cutover record holds the reason. A sign-off refused below ten clean days answers MSG-P1-023 (RD-P1-042; it settles NEW-GAP-S13-2); confirmation of its text is Pending, owner Error and Message Standard owner. Pending: the ACE view statement timeout, retry and database breaker policy, owner solution architect, tracked as NEW-GAP-W3M-003 (Error Handling and Resilience Standard v5 section 8.4).

### 15. Screens and states

No screen in this story. The cutover step is not a job of the P1 job set, so its states are read from the cutover record (RD-P1-012); the reconciliation behind the clean days is read behind SCR-45 Data quality, which shows reconciliation breaks, referential completeness (REC-05), quality measures and stale data products (FSD P1 v3 screens table) and belongs to RWB-P1-AD019-APP and RWB-P3-AD019-APP. The route is the gateway-bff composite route (DP-19, H RWB-PLT-N001-CON); this story adds no route, field or rendering, and the route's path and its merge order are Not specified in the source documents (GAP-2173; ASM-3501). The states the cutover exposes are the six below. The empty, loading, error and no-access states of SCR-45 belong to the console stories and this story defines none of them.

| State | What the cutover record holds | What the data steward reads from it |
|---|---|---|
| Extract ready | The business date, the count of lots and links mapped, the view keys resolved | The step is running and the extract is ready for handover |
| Handed over | The count handed over and the package identifier | The step is complete for the handover and the rows are with rwb-debtsale |
| Loaded | The confirmation that the migrated records answer from `rwb_debtsale` | The rows are served from the new schema |
| Ten clean days running | The count of consecutive clean days and the last clean day | The count, its business date and the days remaining |
| Break | The BREAK row or the orphan, its date, its code and its owner role, the count at zero | The break is listed and the count is reset |
| Signed off | The ten day rows, the extract they came from, the sign-off and the read-only window | The cutover is complete and the legacy tables are read-only |

The legacy screen row names the loading and breaks states of the legacy console; those are the "Extract ready" and "Break" rows above, read through the same composite route and not rendered here. A cutover with one break shows as a reset rather than a zero, and the sign-off cannot be recorded below ten (AC3).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-009-01 | AC1; BR1, BR2, BR3, BR4, BR5 | End to end | The extract fixture with two lots and three links, one lot with a buyer and a reserve price, one link whose `account_key` has a row in `v_ace_account` and one whose key has none; the rwb-debtsale contract mock; a row count of every table of `rwb_source_data` before and after |
| TC-DM-009-03 | AC3; BR6, BR7, BR8 | End to end | Ten consecutive PASS `reconciliation_result` rows for the migrated records, then one BREAK row and one REC-05 orphan row, then ten clean rows again; the sign-off recorded once at ten |
| TC-DM-009-04 | AC4; Access; BR10 | Component | A caller whose Platform administration right R is absent in the authorise fake, starting the step for a business date; a second call with the right present, for the contrast |
| TC-DM-009-05 | AC5; BR9; X7 | Component | The story's version on the per-service sequence against a schema with no history row, then applied a second time; the table, column and index lists of `rwb_source_data` before and after, and the `flyway_schema_history` row count |
| TC-DM-009-06 | AC6; BR6 | Component | The cutover record at nine consecutive PASS `reconciliation_result` rows for the migrated records, then a sign-off attempt; the cutover record before and after the attempt |
| TC-P1-DM009-APP-01 | AC7; X1 | Component | An absent dump, an unreadable dump and a second read for one business date |
| TC-P1-DM009-APP-02 | AC8; X2, X3 | Component | A link with a missing lot and a lot with an empty `cut_off_date` |
| TC-P1-DM009-APP-03 | AC9; X5 | Component | A view fixture whose SELECT fails |
| TC-P1-DM009-APP-04 | AC10; X6 | Component | Nine clean dates, then a BREAK row, a new orphan and a date with no row |
| TC-P1-DM009-APP-05 | AC11; BR11 | Component | Synthetic links; captured package, logs and metrics |

The legacy test case numbers are kept. `TC-DM-009-02`, the reconcile test of the legacy key, sits with the AC2 copy on RWB-ITG-DM009-ITG as `TC-DM-009-02-ITG` and is not repeated here; the integration copies of TC-DM-009-01, TC-DM-009-03 and TC-DM-009-04 are `TC-DM-009-01-ITG`, `TC-DM-009-03-ITG` and `TC-DM-009-04-ITG`, held by the same integration story. The rows are held in Test Cases v9, tab Story test cases. The cutover reconciliation harness pack for debt sale (GAP-0449) is agreed at the wave 4 entry check, owner Integration lead: the SIT environment and its base hosts per hop, a cutover extract fixture with the lot, its two account links and the orphan account_key with its source and migrated_at, a reconciliation extract with one row per orphan and its reason, a report per business date, and a retention that matches the wave evidence. Its gate fails on any unresolved key, any stored balance or payment, or a suppressed break. The environment, base hosts and retention values are Not specified in the source documents (GAP-0449).

### 17. Guardrails

- No business value in code: the lot facts are data on the cutover row, and the ten day target and the retention period are data of the cutover record; the story writes no threshold, no reserve price and no date.
- No direct identifier in the extract: it carries lot facts, `account_key`, `borrower_code`, the two link values and the case key, and no name, contact or national identity field. `account_key` and `borrower_code` are indirect identifiers and `selling_price` and `put_back_status` Customer data: none of them appears in a log, a metric, an error message or a prompt, UAT data masks them, and the fixtures are synthetic.
- ACE data only through the owner's contract or `v_ace_*` views, and here the service owns the views: one login, SELECT only, no `public` table named in any statement (BR10).
- No copy of an ACE row and no copy of an ACE amount: the two views are read for the key and their amounts are never carried; `rwb_source_data` holds no balance and no payment (BR4, BR5).
- No cross-schema write: the load into `rwb_debtsale` is S6's own cutover step on S6's own sequence, and this story holds no INSERT against another service's schema (BR1, DP-01).
- No award, no transfer and no proceeds match: the migration moves records and takes no sale decision, and the sale events are raised by their owners.
- One version on the per-service sequence, never edited in place; a later change is a new version with its own history row (DP-15).
- A cutover is never declared on a count that has been reset: a break sets the count to zero and the sign-off stays closed (BR6, BR8).

### 18. Traceability

| Legacy RWB-DM-009 row | Value (verbatim) | Where it lands |
|---|---|---|
| Epic | E2, release 31 December 2026 | Metadata release and wave; section 2 quotation |
| Module | P1 Recovery data engine | Service rwb-source-data, service epic RWB-SVC-P1 |
| Feature | None | No feature grouping is used |
| L3 process | Not specified in the source documents (DOR-RWB-P1-DM009-APP-2) | Section 18; the Process row below gives the scope only, not an L3 process |
| Process | All recovery processes | The cutover covers the debt sale records of every process the legacy key names |
| Priority | Must | Sections 1, 2 and 19 |
| Depends on | RWB-E1-001, RWB-E1-069 | Rebased by D-RCV-60 onto RWB-P1-E1001-APP and RWB-P1-E1069-APP, with RWB-PLT-E1044-CON and RWB-PLT-N001-CON (metadata) |
| Decision | DL25 (option A applied by RD-P1-042, `recon.tolerance.pct` v1 = 0.00, for Data lead confirmation; ASM-0728, ASM-0735, ASM-0743 confirmed with the tolerance named, ASM-2602 closed) | BR6; the ten clean days as the cutover evidence |
| Story | As a data steward, I want the debt sale lots and their accounts migrated from the legacy Workbench, so that a sale in flight keeps its accounts, its reserve price and its buyer. | Section 1 statement; section 2 quotation; BR1 to BR4 |
| Data | recovery_case `DF-CAS-001` to `DF-CAS-055`; debt_sale_lot `DF-SAL-020` to `DF-SAL-030`; debt_sale_account `DF-SAL-031` to `DF-SAL-037` | Section 11, which carries only the case key of `recovery_case` (RD-P1-027); AC1 |
| Endpoints | No endpoint in this story. The migration is a cutover step run by the recovery service identity, and its breaks are listed on the reconciliation extract. | Sections 4 and 12; the admin operations it is started and read through are named in 12.2 |
| Screen and states | SCR-45 Data quality \| Loading; breaks | Section 15, read through the composite route behind SCR-45 |
| Permission checks | Platform administration \| R \| RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Section 10; TC-DM-009-04 |
| Validation and messages | MSG-P1-001, MSG-P1-012, MSG-GEN-001, MSG-P4-002 | Section 14 |
| Test cases | TC-DM-009-01 to TC-DM-009-04 | Section 16; TC-DM-009-02 sits on RWB-ITG-DM009-ITG as TC-DM-009-02-ITG |
| Guardrails | No value a business person may change in code. No personal data in logs, tests or prompts. No read of another module's tables; ACE data only through recovery.v_ace_* views. A migrated record keeps its source and its migration date, and never a copy of an ACE row. | BR4, BR5, BR10; section 17 |

| Pattern | Source | Applied as |
|---|---|---|
| DP-05 | Template and Rules §R5.5 | The two views are read by this service on its own login and by no other service (section 13) |
| DP-15 | Template and Rules §R5.5 | The version on the per-service sequence with the history row that records the cutover definition (section 13; AC1) |
| DP-19 | Template and Rules §R5.5 | The reconciliation behind the cutover result is read through the gateway-bff composite route behind SCR-45 (section 15) |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1044-CON | Contract | H build dependency: the per-service Flyway sequence and its history |
| RWB-PLT-N001-CON | Contract | H build dependency: the gateway-bff composite route behind SCR-45 |
| RWB-P1-E1001-APP | App development | H build dependency: the recovery tables, the catalog and the DP09 row |
| RWB-P1-E1069-APP | App development | H build dependency: the Section A views, the two views among them |
| RWB-P1-E1011-APP | App development | Writes the `reconciliation_result` rows the clean-day count reads |
| RWB-P1-DM003-APP | App development | The case and ownership slice of the same cutover, which supplies the case keys |
| RWB-ITG-DM009-ITG | Integration | Owns the AC2 reconciliation across the services and the ITG copies of the test cases; P1 supplies to it the per-link resolved or orphan list of flow step 4 and the cutover record |
| The rwb-debtsale stories | App development | Own `rwb_debtsale`, its sequence, the lot status machine and the load of the rows handed over |

External dependencies: None. The story adds no X row of its own.

### 19. Out of scope

- The load into `rwb_debtsale`, S6's Flyway sequence and every table of S6: this story hands the rows over and stops (DP-01, DP-15).
- The AC2 reconciliation of the business keys and its REC-05 orphan list across the services: RWB-ITG-DM009-ITG, with TC-DM-009-02-ITG and the ITG copies of the other cases (ASM-3503).
- The debt sale award, the transfer, the proceeds match and the lot status machine: the rwb-debtsale stories and rwb-payment, with the sale events published there and not by a migration.
- JOB-04, its REC-01, REC-02 and REC-05 checks, the `reconciliation_result` rows and the reconciliation results read: RWB-P1-E1011-APP.
- The SCR-45 Data quality console and its break list: RWB-P1-AD019-APP and RWB-P3-AD019-APP.
- The views themselves, the per-service login and its grant: RWB-P1-E1069-APP and RWB-P1-E1069-DB. This story neither creates, alters nor grants a view.
- The catalog rows and DP09's definition: RWB-P1-E1001-APP.
- The balance and the payment themselves and any read of them outside this boundary proof: they stay in `v_ace_account` and `v_ace_payment` and are read through this service's contract by the services that need them.
- The retention rule and the archive mechanics behind the read-only window: RWB-P1-E1017-APP.
- The platform configuration of Kafka, Temporal and the gateway routes: the platform epics.
- Any REST operation, Kafka event, Temporal workflow, Schedule or screen: this story builds none and section 12 says so table by table.

### 20. Remaining delivery steps

- Size the story at refinement (owner: squad).
- Record the EP08 epic design sign-off (owner: solution architect).
- Bring the contract stories this story builds against to Done and publish their fakes at the pinned versions, including rwb-debtsale and rwb-case (owner: contract owners).
- Agree the dump layout and identity, the package format, location, access and retention, the replay key at S6's load and the cutover record format at the cutover rehearsal (owner: data steward with the squad; GAP-2173).
- Agree the harness environment, base hosts and retention of the wave 4 entry check (owner: integration lead; GAP-0449).
- Give the values of LOV-MIGRATION-SOURCE (owner: data owner; NEW-GAP-B4).
- Update the Test Cases v9 rows and the traceability matrix for the sign-off refusal message MSG-P1-023 (QA).
- Load the synthetic fixtures in DEV (owner: squad).
