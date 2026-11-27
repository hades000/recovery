# RWB-ITG-DM009-ITG Migrate debt sale

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-DM009-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-DM-009 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP15, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-DM009-ITG-16); the squad sizes it at refinement |
| Depends on (build) | RWB-P1-DM009-APP |
| Contract dependencies | Contract for POST /api/recovery/access/v1/authorise, not yet published (see CG-ALL-1030); its story key is Not specified in the source documents (DOR-RWB-ITG-DM009-ITG-8) |
| Contract version | Not specified in the source documents (DOR-RWB-ITG-DM009-ITG-23); only the /v1 path is stated |
| Integration dependencies | RWB-P1-DM009-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-DM-009 for the wave 4 cutover reconciliation harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-DM009-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 9 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **data steward (role code Not specified in the source documents (DOR-RWB-ITG-DM009-ITG-1))**, I want **a repeatable wave 4 cutover reconciliation harness that proves every business key on the migrated debt sale lot and debt sale account records resolves to its view row and lists every orphan with its reason and two owners, against the owning services' published contracts and their fakes**, so that **a sale in flight keeps its accounts, its reserve price and its buyer from the first day after cutover**.

This story builds the harness and the evidence, and nothing else. The real lot and account rows are loaded by rwb-debtsale on its own Flyway sequence (DP-15), from the records that RWB-P1-DM009-APP extracts and maps, and the reconciliation that produces the breaks is RWB-P1-DM009-APP's. RWB-P1-DM009-APP reads v_ace_account and v_ace_payment through the rwb-source-data data-product contract and writes no other service's schema. The cutover extract is read once through the cutover run from the legacy dump and lands nothing in rwb_source_data; one package per cutover business date goes to rwb-debtsale; the ten clean days are counted from the reconciliation_result rows of the migrated records, and the count and the sign-off are held in the cutover record of the release pipeline. The package layout, the cutover record format and the evidence location are agreed at the cutover rehearsal and recorded in the cutover procedure. The field list beyond the AC1 wording and the legacy dump layout, file name and read identity are Not specified in the source documents (GAP-0538; GAP-2173). The story builds no production endpoint, no table, no workflow, no schedule and no screen; it reads the owning services' published contracts, asserts what they answer, and writes one report per business date.

### 2. Business rationale

A debt sale in flight on the first day with an account_key that resolves to no ACE row is a lot that cannot be priced, awarded or transferred: the buyer sees a population that the bank cannot evidence, and the data steward sees a break only after a dispute. The failure is quiet, because the cutover load can report a clean run while the keys it wrote point at rows the ACE views do not hold, and a break that nobody lists is a silent data loss that surfaces as a shortfall in the buyer file or as an account that was sold and not transferred. DL25 puts zero tolerance on that, so the migrated lot and its account links are proven against the views before the cutover is called done, and every orphan is on a list with a reason and two owners.

The harness is decoupled the way the services are. ACE data is read only through rwb-source-data's data-product contract (DP-05), never from another service's schema and never by a direct view read (DP-01); the lot, its account links and the data room summary are read from rwb-debtsale, which owns debt_sale_lot and debt_sale_account; the case behind a sold account is read from rwb-case, which owns recovery_case; the cutover load runs on P1's own Flyway sequence (DP-15); where a screen exists the path is the gateway-bff composite route (DP-19), and the legacy story names the SCR-45 Data quality console, which this harness neither builds nor calls, so it renders no screen; every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget (DP-11). It carries REQ-RDF-007, REQ-RDF-008 and DL25 into evidence rather than restating them.

### 3. Preconditions

- The published contracts of S6 rwb-debtsale (lot and data room), P3 rwb-case (case), P1 rwb-source-data (DP01, DP02, freshness and the JOB-04 rerun) and P4 rwb-access (authorise) are in the contract registry, and a stub set is generated from each one.
- The data product catalog holds DP01 Account and arrears and DP02 Customer and party, each with one system of record, so account_key and person_key have one named owner before a key is resolved (FSD P1 v3, A2.2).
- The cutover load of P1's own Flyway sequence (DP-15) has run in SIT for the business date under test, or the stub of §12.8 answers in its place on Day 1.
- RWB-P1-DM009-APP owns the reconciliation and the break list; until it lands, the reconciliation extract fixture stands in for its output.
- The harness environment and base hosts, the synthetic cutover extract fixture and its field layout, the break-list fields, the extract format and retention, and the pass or fail gate with its seeding set: Not specified in the source documents (GAP-0449; ASM-0641).
- The synthetic lot, the synthetic keys, the field values and the business date are held in the fixture as data, not written in code.
- No build dependency. Day 1, with the stubs in place from the first run; the one wait is RWB-P1-DM009-APP, which replaces its stub and never blocks the lane.

### 4. Flow

1. Harness: loads the cutover extract fixture for business date 2026-11-30: debt sale lot LOT-SYN-0009 with lot_no, cut_off_date 2026-11-30, segment, reserve_price and buyer_partner_id PART-SYN-0009, the account links ACC-SYN-000909 and ACC-SYN-000917 with borrower_code, selling_price, put_back_status, source and migrated_at, and the case that holds the sold account with primary_person_key PERS-SYN-000909. On Day 1, before the cutover load is in SIT, the stub of §12.8 returns the same records.
2. Harness: triggers JOB-04 reconciliation on rwb-source-data with one Idempotency-Key per business date, through `POST /api/recovery/source-data/v1/admin/jobs/JOB-04/rerun`.
3. Harness: reads the lot through `GET /api/recovery/debtsale/v1/debt-sale-lots/{lotId}` and asserts lot_no, cut_off_date, segment, reserve_price and buyer_partner_id against the fixture.
4. Harness: reads the data room summary through `GET /api/recovery/debtsale/v1/partner/data-room/{lotId}` and asserts that the lot is named with the accounts it offers and that the answer carries no balance and no payment.
5. Harness: reads the case behind the sold account through `GET /api/recovery/case/v1/cases/{caseId}` and takes primary_person_key from it, then resolves account_key through `GET /api/recovery/source-data/v1/data-products/{productCode}/records?caseId={caseId}` for DP01 and person_key through the same operation for DP02, with `GET /api/recovery/source-data/v1/data-products/freshness?product=DP01` for the business date and the load time.
6. Harness: reads the break list from the reconciliation extract fixture for the business date, with one row per orphan and its reason; the legacy story states that the breaks are listed on the reconciliation extract and that there is no screen.
7. Harness: reruns JOB-04 for the same business date with the same Idempotency-Key and compares the break list and the counts of lots, account links, resolved keys and breaks with the first run, and asserts that the migrated lot and account link hold no balance and no payment of their own.
8. Harness: calls `POST /api/recovery/access/v1/authorise` as a synthetic caller with role RW-OFF and no Platform administration right, and asserts 403 with MSG-P4-002, no reconciliation run started and no break row written.
9. Harness: writes one run report per business date, keyed by story and business date, naming the contract version of each hop, whether the hop was a stub or the owner, the counts, the break rows and the four criteria.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case | Covered by |
|---|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no criterion is marked passed | None | TC-DM-009-01-ITG (ITG AC1) | AC1 |
| X2 | The cutover extract fixture lacks a required key on a migrated lot or account link | The run fails and the report names the lot and the missing field; a record without a key is never reported as reconciled | None | TC-DM-009-01-ITG (ITG AC1) | AC1 |
| X3 | A key has no view row and the extract does not list it | The run fails on AC1 and the report names the lot, the key type and the key value, so a suppressed break is a failure and not a pass | None | TC-DM-009-02-ITG (ITG AC2) | AC1, AC2 |
| X4 | A rerun lists the same break twice | The run fails on AC3 and the report names the two rows and the business date | None | TC-DM-009-03-ITG (ITG AC3) | AC3 |
| X5 | JOB-04 is refused because the ACE batch is late | The run fails before any assertion and the report names the product, the date and the message; a stale product is never treated as an empty result | MSG-P1-001 | TC-DM-009-01-ITG (ITG AC1) | AC1 |
| X6 | A caller without the Platform administration right starts a run | The run fails on AC4 and the report names the caller role and the operation; a run that started is reported as started | MSG-P4-002 (expected, and missing) | TC-DM-009-04-ITG (ITG AC4) | AC4 |
| X7 | The counts the owner returns disagree with the extract | The run fails on AC3 and the report names each count and its two values | None | TC-DM-009-03-ITG (ITG AC3) | AC3 |
| X8 | A balance or a payment value appears on a migrated lot or account link | The run fails on AC3 and the report names the lot or the link, the field and the ACE view that owns the value | None | TC-DM-009-03-ITG (ITG AC3) | AC3 |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stubs from Day 1; the only wait is RWB-P1-DM009-APP, and its stub answers until it lands |
| Negotiable | The fixture layout, the break-list fields, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | The migrated lot and its account keys are proven against the ACE views, no balance and no payment is copied, and every orphan is on a list with two owners before wave 4 opens |
| Estimable | One runner, one stub set, two fixtures, one key resolver, one break-list assertion, one no-copy assertion and one report |
| Small | Fits in one sprint with its four tests |
| Testable | Each criterion runs against the stubs and again against the real owner as the I story lands |

### 7. Acceptance criteria

```gherkin
Feature: Migrate debt sale - wave 4 cutover reconciliation harness

  Background:
    Given the synthetic cutover extract holds debt sale lot "LOT-SYN-0009" with cut_off_date "2026-11-30" and its segment, reserve_price and buyer_partner_id "PART-SYN-0009"
    Given the lot links account_key "ACC-SYN-000909" and account_key "ACC-SYN-000917"
    Given the rwb-source-data data-product contract returns one row for account_key "ACC-SYN-000909" and one row for person_key "PERS-SYN-000909"
    Given JOB-04 has run for business date "2026-11-30"

  Scenario: AC1 Reconcile the business keys (legacy RWB-DM-009 AC2)
    Given the migrated records
    When the REC-05 step runs
    Then every business key on a migrated record resolves to its view row, account_key and person_key included
    And each orphan is listed for the data steward and the ACE team

  Scenario: AC2 An orphan account_key is listed with its reason and its two owners (new, D-RCV-60)
    Given a migrated debt_sale_account link on lot "LOT-SYN-0009" carries account_key "ACC-SYN-000917"
    And the rwb-source-data data-product contract returns no row for account_key "ACC-SYN-000917"
    When the harness reads the reconciliation result for business date "2026-11-30"
    Then the break list holds one row for lot "LOT-SYN-0009" with key type "ACCOUNT" and key value "ACC-SYN-000917"
    And the row names the reason "NO_ACE_ROW" and the owner role "RW-DATASTEW"
    And the migrated lot and its account links stay readable through the rwb-debtsale contract
    And the run report names the ACE team as the second owner of the break

  Scenario: AC3 No balance and no payment is copied, and a rerun lists the same break once (new, D-RCV-60)
    Given the reconciliation for business date "2026-11-30" has run once
    When JOB-04 is rerun for the same business date
    Then no balance and no payment is copied, because both are read through the rwb-source-data data-product contract
    And the migrated account link holds account_key "ACC-SYN-000909" and no amount of its own
    And the break list holds exactly one row for account_key "ACC-SYN-000917"
    And the counts of lots, account links, resolved keys and breaks equal the first run
    And the run report holds one entry per business date and not one per run

  Scenario: AC4 A caller without the platform administration right is refused (new, D-RCV-60)
    Given a synthetic user with role "RW-OFF" and no Platform administration right
    When the harness calls the reconciliation run for business date "2026-11-30"
    Then the answer is 403 with "MSG-P4-002"
    And no reconciliation run starts and no break row is written

  Scenario: AC5 The harness reads each owning service only through its published contract (new, D-RCV-60)
    Given the owning services publish the rwb-debtsale, rwb-case and rwb-source-data contracts
    When the reconciliation run reads the migrated records and their ACE rows
    Then every read goes through one of those contracts
    And no table of another service's schema is read

  Scenario: AC6 Each business rule of section 8 is asserted on the migrated records (new, D-RCV-60)
    Given the migrated records for business date "2026-11-30"
    When the reconciliation run reads them and their data-product rows through the published contracts
    Then no lot is offered, awarded or transferred while a business key on its migrated record has no data-product row
    And no break is suppressed and every break carries its reason
    And wave 4 does not open while one migrated record has an unresolved key
    And no balance and no payment is stored on the migrated record
    And the migrated record keeps its source and its migration date
    And a sale in flight keeps its accounts, its reserve price and its buyer
    And each service applies its own Flyway sequence in its own schema

  Scenario: AC7 A consumed call that fails or does not answer stops the run at that hop (new, D-RCV-60)
    Given a call on the rwb-source-data contract fails or does not answer for account_key "ACC-SYN-000909"
    When the harness runs the reconciliation for business date "2026-11-30"
    Then the run fails at the hop that failed or did not answer
    And the run report names that hop and its contract version
```

Legacy AC1 and AC3 belong to RWB-P1-DM009-APP, and the seven criteria above are the ones this ITG story owns.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | Every business key on a migrated debt sale lot or debt sale account link resolves to an ACE view row before the lot is offered, awarded or transferred | REQ-RDF-007; DL25 | AC1, AC2, AC6; TC-DM-009-01-ITG, TC-DM-009-02-ITG, TC-DM-009-06-ITG |
| BR2 | Every break is listed with a reason the data product owner can see, and no break is suppressed | REQ-RDF-008 | AC2, AC3, AC6; TC-DM-009-02-ITG, TC-DM-009-03-ITG, TC-DM-009-06-ITG |
| BR3 | Zero tolerance holds the publish: wave 4 does not open while one migrated record has an unresolved key | DL25 | AC1, AC2, AC6; TC-DM-009-01-ITG, TC-DM-009-02-ITG, TC-DM-009-06-ITG |
| BR4 | No balance and no payment is copied into the Workbench; the outstanding at cut-off is read from v_ace_account and the payment from v_ace_payment | REQ-RDF-002; D-RCV-35; ADR-010 | AC3, AC6; TC-DM-009-03-ITG, TC-DM-009-06-ITG |
| BR5 | A migrated record keeps its source and its migration date, and never a copy of an ACE row | Legacy RWB-DM-009 guardrail; D-RCV-35 (U1) | AC3, AC6; TC-DM-009-03-ITG, TC-DM-009-06-ITG |
| BR6 | A sale in flight keeps its accounts, its reserve price and its buyer from cutover | Legacy RWB-DM-009 story; DL25 | AC2, AC6; TC-DM-009-02-ITG, TC-DM-009-06-ITG |
| BR7 | Each service applies its own Flyway sequence in its own schema | DP-15; ADR-021 | AC5, AC6; TC-DM-009-05-ITG, TC-DM-009-06-ITG |

The harness asserts these rules and changes none of them.

DL25 is carried as a decision of record with its assumptions ASM-0728, ASM-0735, ASM-0743 and ASM-2602, all confirmed by the programme directive.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| AWARDED | Reconciliation for the business date with every key resolved | JOB-04 completes and every account_key and person_key has a DP01 or DP02 row | AWARDED, unchanged |
| AWARDED | Reconciliation for the business date with one orphan | account_key ACC-SYN-000917 has no DP01 row | AWARDED, unchanged, and the orphan is listed |
| AWARDED | A listed orphan resolves and is reconciled | A DP01 row appears for the key and JOB-04 is rerun for the same business date | The break is no longer listed; the lot status is unchanged |

The harness changes no state. Every change in the table is made by the owner: S6 rwb-debtsale holds the lot, its accounts, its reserve price, its buyer and its status, and P1 rwb-source-data writes the reconciliation result and the break list. The harness reads, asserts and reports; a state it had set by hand would prove nothing, so the report names the owner and the operation behind every value it asserts.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward | Runs and reads the reconciliation for a business date; holds Platform administration R; owns the break list with the ACE team |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Read the same reconciliation evidence; each holds Platform administration R |
| QA lead | Owns the harness configuration, the fixtures, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | P1 rwb-source-data runs JOB-04 and writes the reconciliation result, S6 rwb-debtsale holds the lot and its accounts, P3 rwb-case holds the case, and P4 rwb-access answers the authorisation; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; authorisation is answered by rwb-access |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-SAL-020 to DF-SAL-030 | debt_sale_lot | lot_no, cut_off_date, segment, reserve_price, buyer_partner_id, status | Read through the rwb-debtsale contract |
| DF-SAL-031 to DF-SAL-037 | debt_sale_account | lot_id, account_key, borrower_code, selling_price, put_back_status | Read through the rwb-debtsale contract |
| DF-CAS-001 to DF-CAS-023, DF-CAS-046 to DF-CAS-055 | recovery_case | case_no, primary_person_key, status, stage_code | Read through the rwb-case contract |
| No BR Field ID (ACE view) | v_ace_account, v_ace_payment | account_key, total_balance, payment_code | Read through the rwb-source-data data-product contract |
| Standard column | debt_sale_lot, debt_sale_account | source, migrated_at | Read through the rwb-debtsale contract |

Field IDs are those in the Logical Data Model and Data Dictionary v9. The two debt sale tables are S6's and the harness reads them only through the rwb-debtsale contract; the case is P3's and is read through the rwb-case contract. The ACE side is DP01 Account and arrears for account_key and the balance at cut-off, and DP02 Customer and party for person_key, read through the rwb-source-data data-product contract (FSD P1 v3, lines 283 and 284), never from a view and never from a table. The outstanding at cut-off is an ACE reuse of v_ace_account.total_balance and is not stored on the migrated record (Logical Data Model and Data Dictionary v8, DF-SAL-035). The harness owns no table and writes no row. Reference data: the harness reads any list or parameter only through the reference-data contract (DP-06, DP-07); the parameter keys it reads are Not specified in the source documents (DOR-RWB-ITG-DM009-ITG-20).

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/debtsale/v1/debt-sale-lots/{lotId}` | S6 rwb-debtsale | Lot number, cut-off date, segment, reserve price, buyer and status (AC1, AC2) |
| GET | `/api/recovery/debtsale/v1/partner/data-room/{lotId}` | S6 rwb-debtsale | The accounts the lot offers, at the published data room level and with no balance (AC1, AC3) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case behind a sold account and its primary_person_key (AC1) |
| GET | `/api/recovery/source-data/v1/data-products/{productCode}/records?caseId={caseId}` | P1 rwb-source-data | The DP01 and DP02 rows that resolve account_key, person_key and the balance at cut-off (AC1, AC2, AC3) |
| GET | `/api/recovery/source-data/v1/data-products/freshness?product=DP01` | P1 rwb-source-data | The business date and the load time of the product (AC1) |
| POST | `/api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` | P1 rwb-source-data | Run JOB-04 reconciliation for the business date, with one Idempotency-Key (AC1, AC3) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The right and the refusal path (AC4) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). No operation is invented in this story: each path is the owner's published operation, and where a screen would compose them the path would be the gateway-bff composite route (DP-19).

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

None. The harness triggers JOB-04 through the owner's rerun operation, not through an event, and reads the result through the same contract rather than from a topic.

#### 12.5 Workflows and activities

None added. JOB-04 reconciliation, the event-triggered reconciliation workflow on rwb-source-data (Architecture v5 slides 15 and 44), is exercised through its rerun operation. The S6 DebtSaleWorkflow and the S6 award operation are out of scope: they belong to the S6 debt sale stories, and this harness neither starts nor asserts them. No workflow, activity or Schedule is created or changed by this story.

#### 12.6 Schedules

None. JOB-04 is event-triggered; the harness reruns it for the business date under test and sets no cron.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); the lots and the account links are S6's, the case is P3's and the reconciliation result is P1's.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-source-data | The three P1 operations of §12.2 | DP01 returns one row for ACC-SYN-000909 with its balance at cut-off, DP02 returns one row for PERS-SYN-000909, freshness returns business date 2026-11-30 with a load time, and the rerun is accepted once per Idempotency-Key |
| Stub for rwb-debtsale | `GET /debt-sale-lots/{lotId}`, `GET /partner/data-room/{lotId}` | The lot LOT-SYN-0009 with its cut_off_date, segment, reserve_price and buyer_partner_id; the data room answer lists ACC-SYN-000909 and ACC-SYN-000917 with no balance and no payment |
| Stub for rwb-case | `GET /cases/{caseId}` | The case behind the sold account with primary_person_key PERS-SYN-000909 |
| Stub for rwb-access | `POST /authorise` | Allows RW-DATASTEW with Platform administration R; refuses RW-OFF with 403 and MSG-P4-002 |
| Cutover extract fixture | The migrated records of the legacy story | The lot, its number, cut-off date, segment, reserve price and buyer, its two account links, the orphan account_key ACC-SYN-000917 on a debt_sale_account link, and the source and migrated_at of each record |
| Reconciliation extract fixture | The break list of the reconciliation | One row for lot LOT-SYN-0009 with key type ACCOUNT, key value ACC-SYN-000917, reason NO_ACE_ROW, owner role RW-DATASTEW and the ACE team as second owner |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. Contract fake library version: Not specified in the source documents (DOR-RWB-ITG-DM009-ITG-22); no fake version is recorded as published. The harness pack and its pass or fail gate are agreed at the wave 4 entry check (section 15). The harness environment and base hosts, the field layout of the synthetic cutover extract fixture, the break-list fields beyond one row per orphan and its reason, the extract format, the retention period and the data seeding set are Not specified in the source documents (GAP-0449; ASM-0641).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 7 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published and none consumed; the run is triggered by an operation and read back through the same contract |
| Temporal | None added; JOB-04 reconciliation, the event-triggered workflow on rwb-source-data, is exercised |
| File | The cutover extract fixture and the reconciliation extract fixture, both read as files |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies in the table above (RWB-PLT-E1044-CON and RWB-PLT-N001-CON) are recorded here and are not repeated in the metadata H field of this story, which stays empty as the plan requires. The one blocking dependency is the I story RWB-P1-DM009-APP, which replaces its stub; until it is live the run uses the stub, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the four owned criteria in order for a business date and holds the run lock |
| StubSet | Fake | The four stubs of §12.8 generated from the published contracts, with the contract version pinned |
| CutoverExtractFixture | Fixture | The synthetic lot, its two account links, the orphan account_key and the source and migrated_at of each record |
| KeyResolver | Service | Resolves account_key through DP01 and person_key through DP02 with the freshness read, and names each key that does not resolve |
| NoCopyAssertion | Service | Asserts that no balance and no payment sits on the migrated lot or account link, because both are read from v_ace_account and v_ace_payment |
| BreakListAssertion | Service | Compares the read result with the reconciliation extract fixture: one row per orphan, its reason and its two owners, and one row only on a rerun |
| EvidenceReport | Service | Writes one report per business date keyed by story, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real services as the I story lands, on the synthetic lot LOT-SYN-0009 with cut_off_date 2026-11-30, account_key ACC-SYN-000909, account_key ACC-SYN-000917, person_key PERS-SYN-000909, buyer_partner_id PART-SYN-0009 and business date 2026-11-30; the segment, the reserve_price, the selling_price and the put_back_status are carried as fixture data, not as values in code. In SIT the records come from the cutover load of P1's own Flyway sequence (DP-15). The harness environment and base hosts, the fixture layout, the break-list fields, the extract format and retention, and the gate with its seeding set are Not specified in the source documents (GAP-0449; ASM-0641). The harness seeds nothing by hand and never writes a schema row.

**Build steps**

1. Generate the four stubs from the published contracts and pin each contract version in the run report; fail the run on a mismatch (X1).
2. Build the CutoverExtractFixture and the ReconciliationExtractFixture, and prove both are read for business date 2026-11-30 (X2).
3. Build the JourneyRunner for AC1: trigger JOB-04 with one Idempotency-Key, read the lot and the data room summary through rwb-debtsale, read the case through rwb-case, resolve account_key and person_key through DP01 and DP02 with the freshness read, and list each orphan (X5).
4. Add the KeyResolver assertion that every key on a migrated lot or account link resolves, and that each orphan is on the list for the data steward and the ACE team (X3).
5. Add BreakListAssertion for AC2: one row for lot LOT-SYN-0009 with key type ACCOUNT, key value ACC-SYN-000917, reason NO_ACE_ROW and owner role RW-DATASTEW, the ACE team named as second owner in the report, and the lot and its links still readable through the rwb-debtsale contract.
6. Add NoCopyAssertion for AC3: no balance and no payment on the migrated record, the balance at cut-off read from v_ace_account and the payment from v_ace_payment through the P1 contract, then the rerun with one break row and equal counts of lots, account links, resolved keys and breaks, and one report entry per business date (X4, X7, X8).
7. Add the access path for AC4 through `POST /api/recovery/access/v1/authorise`, then the EvidenceReport and the gate, and swap a stub for the real owner as its I story lands (X6).

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-P1-DM009-APP when it lands, and the wave entry check holds a run report keyed by story and business date.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text.

### 15. Screens and states

The legacy story names the SCR-45 Data quality console with its loading and breaks states, and this harness renders no screen: the breaks are listed on the reconciliation extract, which the data steward and the ACE team read as a file. The states the harness asserts on that extract are small: empty (no break row and zero counts), loading (run in progress, no extract written), error (the run fails at the hop named in X1 to X8) and no access (the run is refused with MSG-P4-002, no extract written).

| State | What the extract holds |
|---|---|
| No break | One line for the business date with the counts of lots, account links, resolved keys and breaks, and no break row |
| Break | One row per orphan with the lot number, the key type, the key value, the reason, the data steward and the ACE team as owners |

The harness renders no screen. The SCR-45 Data quality console that the legacy story names is not part of this legacy key: it is the screen of RWB-AD-019 and this story neither builds it nor reads it. Its states are loading and breaks, as the legacy story names them; its empty, error and no access states are Not specified in the source documents (CG-ALL-1034). The wave 4 entry check agrees the harness pack: a harness environment and base hosts per hop; a cutover extract fixture with lot LOT-SYN-0009, its two account links with the orphan ACC-SYN-000917, and source and migrated_at; a reconciliation extract with one row per orphan and its reason; one run report per business date; a retention that matches the wave evidence; and a gate that fails on any unresolved key, any stored balance or payment, or a suppressed break. The environment, the base hosts, the data seeding set and the retention period are Not specified in the source documents (GAP-0449; ASM-0641).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-009-01-ITG | AC1 (legacy); ITG AC1 | Integration | Synthetic lot LOT-SYN-0009 with DP01 and DP02 rows present |
| TC-DM-009-02-ITG | AC2 (legacy); ITG AC1, ITG AC2 | Integration | One account_key ACC-SYN-000917 with no data-product row |
| TC-DM-009-03-ITG | AC3 (legacy, owned by RWB-P1-DM009-APP); ITG AC3 | Integration | Two JOB-04 runs for business date 2026-11-30, with no balance and no payment on the migrated record |
| TC-DM-009-04-ITG | Access; ITG AC4 | Component | RW-OFF caller without Platform administration R |
| TC-DM-009-05-ITG | ITG AC5 | Integration | Synthetic lot LOT-SYN-0009 read through the rwb-debtsale, rwb-case and rwb-source-data contracts only |
| TC-DM-009-06-ITG | ITG AC6 (section 8 rules BR1 to BR7) | Integration | Synthetic lot LOT-SYN-0009 with its two account links and the orphan ACC-SYN-000917 |
| TC-DM-009-07-ITG | ITG AC7 | Component | Stub of rwb-source-data that fails, and then does not answer, for account_key ACC-SYN-000909 |

The AC column names the legacy AC the copy derives from and the ITG AC it asserts, and the full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx under the same legacy test case ID. TC-DM-009-03-ITG is the cutover copy and names RWB-P1-DM009-APP as the owner of the cutover assertions it derives from.

### 17. Guardrails

- No business value in code: the synthetic keys, the business date, the fixture contents, the break reasons and the report layout are data.
- No personal data in logs, fixtures or reports: every key is synthetic and no customer record is read at all.
- No read of another service's schema and no direct view read: the lot and its links come from rwb-debtsale, the case from rwb-case and the ACE side from the rwb-source-data contract (DP-01, DP-05).
- No balance and no payment is copied into the Workbench or into the fixture of a migrated record; the ACE value is read where it is needed and named in the report.
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11).
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never writes a row by hand.
- A failing criterion is fixed in the service that owns it or reported as a gap; it is never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-DM-009 Migrate debt sale | Recovery Workbench Data Migration Stories v3, lines 551 to 633 | Sections 1, 3, 11 and 19 of this file |
| Legacy AC2 Reconcile the business keys, verbatim | The same, lines 576 to 580 | Section 7, AC1, marked (legacy RWB-DM-009 AC2) |
| Legacy AC1 and AC3, and the four legacy test cases TC-DM-009-01 to TC-DM-009-04 | The same, lines 570 to 574, 582 to 586 and 624 to 629 | AC1 and AC3 stay with RWB-P1-DM009-APP (section 19); the four cases are copied as -ITG in section 16 |
| DF-SAL-020 to DF-SAL-030, DF-SAL-031 to DF-SAL-037 and the ACE reuse of DF-SAL-035 | Logical Data Model and Data Dictionary v9 | Section 11 |
| DL25, zero tolerance on the migrated data | Decision Log, DL25 | Section 8, BR1 to BR3 |
| REQ-RDF-002, REQ-RDF-007 and REQ-RDF-008 | BRD Program v4 and Epic 1 v4 | Section 8, BR1, BR2 and BR4 |
| D-RCV-35 and ADR-010, ACE data only through the views | Decision Log, D-RCV-35; ADR-010 | Section 8, BR4 and BR5; sections 12.2 and 12.8 |
| Job map JOB-04 reconciliation, owner rwb-source-data | Architecture v5 slides 15 and 44 | Section 12.5, the JOB-04 reconciliation this harness exercises; the S6 DebtSaleWorkflow and award are out of scope |
| DP-05, DP-15 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application |

### 19. Out of scope

- RWB-P1-DM009-APP: the extraction, the cutover and legacy AC1 and AC3, together with the REC-05 reconciliation and the break list. The cutover load of the records into rwb_debtsale is P1's own Flyway sequence.
- S6 rwb-debtsale production code and its CON, APP and DB stories: the lot contract, the data room, the award, the transfer and the tables are built there. The S6 DebtSaleWorkflow and the S6 award operation are not started or asserted here.
- S6 debt sale records other than the two reads of §12.2: the data room pack, buyer terms, bids, award and transfer are not read.
- The SCR-45 Data quality console (RWB-AD-019).
- The cutover plan, the data steward sign-off and the legacy read-only period of legacy AC3.
- ACE ingestion and the 30 views (RWB-ACE-001).
- Platform deployment and configuration.
- The other four data migration keys of this wave.
