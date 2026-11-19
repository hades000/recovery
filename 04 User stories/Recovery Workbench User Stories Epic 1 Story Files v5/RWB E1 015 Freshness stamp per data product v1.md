# RWB-E1-015 Freshness stamp per data product

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-015 |
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | FEAT-RDF-14 Stamp each data product with its freshness; FEAT-DRI-12 Carry a freshness stamp on every decision input |
| Requirement IDs | REQ-RDF-009 |
| BRD section | Business Requirements Epic 1, section 3.1 (story) and section 4 (REQ-RDF-009) |
| L3 process | All recovery processes; 17 Run the decision center |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-003, RWB-E1-001, RWB-E1-064, RWB-E1-006 |
| Status | Ready for build |

## 1. Story

As a **data steward and data product owner (RW-DATASTEW)**, I want **every data product to carry the source extract time and the load time, exposed to every consumer and shown on the case record view**, so that **every decision input states how old it is and stale facts are visible**.

## 2. Business rationale

Recovery data arrives by end of day batch and weekly or monthly file loads (ADR-005), so a fact on the case can be one day or one week old, and nobody can see which. A stamp per product and load, shown on the case record and copied into each decision's inputs snapshot, makes the age of every input visible to the person deciding and to audit. A product whose load has not arrived by its expected time is flagged stale the same morning. Serves REQ-RDF-009; measure: loads on time and complete on 99 percent of days (FSD P1 A2.14.1).

## 3. Preconditions

- RWB-E1-001 is done: the recovery tables exist, and loan_account and account_payment carry data_as_of.
- RWB-E1-003 is done: the ALS load (JOB-01) commits DP01 rows and publishes LoadCompleted or LoadRefused.
- RWB-E1-064 is done: the data_product table holds DP01 to DP14 with refresh cycle and expected-by time (assumed 08:00 for daily COLLINS products and Monday 08:00 for weekly file products; DL11).
- RWB-E1-006 is done: the data quality exception list exists and GET /admin/data-quality/exceptions reads it.
- RWB-E1-027 is done: the P7 decision log writer builds an inputs snapshot for each entry.
- The reader holds Case record R (case roles) or Platform administration R (data steward, platform administrator).

## 4. Flow

1. Load job (JOB-01 or JOB-09): commits a load for product DP01 and business date D.
2. FreshnessStampService: in the same transaction, writes one data_product_load row with business date D, the source extract time from the COLLINS control record and the load time.
3. JOB-01 freshness step: at each product's expected-by time, checks that a load for the expected business date exists.
4. FreshnessStampService: for a product with no load, sets the latest row to status STALE, writes a data quality exception with check FRESHNESS and sends the operations alert.
5. StaleMarkerListener: on LoadRefused, marks the product STALE at once.
6. Consumer (case record view, P3 or P7): calls FreshnessQuery or GET /data-products/freshness and receives business date, source extract time, load time and status per product.
7. Case record view: shows the stamp in the data panel, with MSG-P1-001 when the product is stale.
8. P7 inputs snapshot builder: calls FreshnessQuery.stampsFor() for the products a decision reads and writes each stamp into the snapshot that inputs_ref points to.
9. Load job: a later load for date D sets status LOADED and clears the stale flag.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No load for the expected business date by the expected-by time | Product set STALE; exception FRESHNESS written; operations alert sent; case record shows the stale warning | MSG-P1-001 | AC2 |
| X2 | The load is refused at a check | LoadRefused marks the product STALE at once; previous stamp stays in use | MSG-P1-002, MSG-P1-001 | AC4 |
| X3 | The same load is stamped twice for one product and business date | One data_product_load row; the repeat is counted (R-UNI-40) | None | AC5 |
| X4 | A late load arrives after the stale flag | Status LOADED; stale flag cleared; exception closed | None | AC6 |
| X5 | A load is committed one minute before the expected-by time | Product not flagged stale | None | AC7 |
| X6 | A weekly product inside its weekly cycle | Product not flagged stale on the days between loads | None | AC8 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the tables (RWB-E1-001), the ALS load (RWB-E1-003), the data product table (RWB-E1-064) and the exception list (RWB-E1-006) |
| Negotiable | Expected-by times and refresh cycles are data rows on data_product; the story fixes the stamping and the stale check |
| Valuable | Every decision and every case record shows the age of its data |
| Estimable | One new table, one service, one listener, one endpoint, one panel |
| Small | Finished inside two weeks with its tests |
| Testable | Each criterion runs against a test clock and synthetic loads |

## 7. Acceptance criteria

```gherkin
Feature: Freshness stamp per data product

  Background:
    Given data product "DP01" Account and arrears has refresh cycle "DAILY" and expected-by time 08:00
    Given data product "DP06" Collateral and asset has refresh cycle "WEEKLY" and expected-by time Monday 08:00

  Scenario: AC1 Freshness on the row
    Given the account and arrears product for business date 2026-11-30 loaded at 06:50 on 2026-12-01 from an extract taken at 23:30 on 2026-11-30
    Given loan account "ACC-SYN-000101" has data_as_of 2026-11-30
    When the row is read through FreshnessQuery.stampForRow("DP01", 2026-11-30) and GET /data-products/freshness?product=DP01
    Then the row carries source time 2026-11-30T23:30+07:00 and load time 2026-12-01T06:50+07:00
    Then the status is "LOADED"

  Scenario: AC2 Stale product flagged
    Given no DP01 load for business date 2026-11-30 exists at 08:00 on 2026-12-01
    When the freshness step runs at 08:00
    Then the system flags the product "STALE"
    Then a data quality exception with product "DP01" and check "FRESHNESS" is raised on 2026-12-01
    Then the alert goes to the operations channel
    Then the case record view shows the stamp in the data panel with "Account and arrears is from 2026-11-30. Today's load has not arrived."

  Scenario: AC3 Freshness in the decision log
    Given a decision log entry for case "RW-2026-000101" read DP01 for 2026-11-30 and DP06 for 2026-11-23
    When the entry and its inputs snapshot are read
    Then the snapshot lists DP01 with load time 2026-12-01T06:50+07:00 and status "LOADED"
    Then the snapshot lists DP06 with load time 2026-11-24T04:40+07:00 and status "LOADED"

  Scenario: AC4 A refused load marks the product stale at once
    Given the DP01 load for 2026-11-30 is refused at check "Control totals" at 05:20
    When LoadRefused is processed
    Then DP01 is "STALE" from 05:20
    Then the stamp for business date 2026-11-30 stays the one in use

  Scenario: AC5 The same load stamped twice
    Given DP01 for business date 2026-11-30 is stamped at 06:50
    When the same stamp is written again for DP01 and 2026-11-30
    Then one data_product_load row exists for DP01 and 2026-11-30
    Then the duplicate count for that stamp is 1

  Scenario: AC6 A late load clears the stale flag
    Given DP01 was flagged "STALE" at 08:00 on 2026-12-01
    When the DP01 load for 2026-11-30 commits at 08:40
    Then DP01 status is "LOADED" with load time 2026-12-01T08:40+07:00
    Then the FRESHNESS exception for DP01 on 2026-12-01 is closed

  Scenario: AC7 A load one minute before the expected-by time
    Given the DP01 load for 2026-11-30 commits at 07:59 on 2026-12-01
    When the freshness step runs at 08:00
    Then the system does not flag DP01 stale

  Scenario: AC8 A weekly product between its loads
    Given the DP06 load for business date 2026-11-30 committed at 04:40 on Monday 2026-11-30
    When the freshness step runs at 08:00 on Thursday 2026-12-03
    Then the system does not flag DP06 stale
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every committed load writes one freshness stamp per product and business date, in the same transaction as the load | REQ-RDF-009; mapping rule "Business date", s2t.txt |
| BR2 | A product with no load for its expected business date by its expected-by time is stale | data_product.expected_by (RWB-E1-064); DL11 |
| BR3 | A refused load leaves the previous load in use and marks the product stale | DQ checks "Refuse the load", dq.txt; CTL-02 |
| BR4 | Every decision records the freshness of each data product it read | REQ-RDF-009; FEAT-DRI-12; DF-DEC-008 meaning |
| BR5 | A repeat stamp for the same product and business date is ignored and counted | R-UNI-40 |
| BR6 | Expected-by times and refresh cycles are data rows, not code | Principle 1; DT02 |

## 9. State transitions

None. This story does not change a case status. It changes the freshness status of a data product load: LOADED to STALE when the expected load is missing or refused, and STALE to LOADED when a later load commits.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-DATALOAD, data load | Writes data_product_load rows; marks products stale; writes the FRESHNESS exception |
| SY-DECLOG, decision log writer | Reads stamps through FreshnessQuery for the inputs snapshot |
| RW-DATASTEW, data steward | Reads stamps and stale exceptions (Platform administration R) |
| RW-PLATADM, platform administrator | Reads stamps and stale exceptions; receives the operations alert |
| Case roles with Case record R, for example RW-CASEOWN, RW-TEAMMGR | Read the stamp in the case record data panel |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACC-021 | loan_account | data_as_of | Read |
| DF-ACC-028 | account_payment | data_as_of | Read |
| DF-DEC-008 | decision_log_entry | inputs_ref | Read |
| DF-REF-071 | data_product | product_code | Read |
| DF-REF-072 | data_product | product_name | Read |
| DF-REF-077 | data_product | refresh_cycle | Read |
| DF-REF-078 | data_product | expected_by | Read |
| DF-OPS-001 | data_product_load | id | Write |
| DF-OPS-002 | data_product_load | product_code | Write |
| DF-OPS-003 | data_product_load | source_system | Write |
| DF-OPS-004 | data_product_load | business_date | Write |
| DF-OPS-005 | data_product_load | source_extracted_at | Write |
| DF-OPS-006 | data_product_load | loaded_at | Write |
| DF-OPS-007 | data_product_load | status | Write |
| DF-OPS-008 | data_product_load | stale_flagged_at | Write |
| DF-OPS-009 | data_product_load | duplicate_count | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Endpoint (new, see additions)**

| Item | Value |
|---|---|
| Method and path | GET /data-products/freshness |
| Request | Query: product (optional, DP01 to DP14), asOf (optional, business date) |
| Response | DataProductFreshness[]: productCode, productName, businessDate, sourceExtractedAt, loadedAt, status (LOADED or STALE), staleSince |
| Errors | 400 malformed product or date (MSG-GEN-001); 401 no session (MSG-P4-001); 403 role lacks the right (MSG-P4-002); 503 store down (MSG-GEN-006) |
| Authorization | Case record, R. No case scope applies: the stamp holds no case data |
| Idempotency | Not applicable |

**Published interface (P1 to P3 and P7)**

```java
package recovery.dataengine.freshness.api;

public interface FreshnessQuery {
    FreshnessStamp stampFor(String productCode);
    FreshnessStamp stampForRow(String productCode, LocalDate dataAsOf);
    Map<String, FreshnessStamp> stampsFor(Set<String> productCodes);
}

public record FreshnessStamp(String productCode, LocalDate businessDate,
        OffsetDateTime sourceExtractedAt, OffsetDateTime loadedAt,
        FreshnessStatus status, OffsetDateTime staleSince) {}
```

**Job step and events**

| Item | Value |
|---|---|
| Trigger | Quartz trigger per product at data_product.expected_by, Asia/Bangkok |
| Job name | JOB-01 COLLINS load check and intake, freshness step (file products: JOB-09 File loads) |
| Input | data_product rows; data_product_load rows for the expected business date |
| Output | Status STALE on the product's latest stamp; data quality exception check FRESHNESS; operations alert |
| Events consumed | EV-27 LoadRefused (marks the product stale) |
| Events published | None |
| Idempotency key | Product code and business date (unique key on data_product_load) |
| Restart behavior | The step reads state each time; a rerun after a failure flags the same products and writes no second exception for the same product and day |

## 13. Solution plan

- Package: folder `recovery/dataengine/freshness`, Java package `recovery.dataengine.freshness`.

| Component | Type | Responsibility |
|---|---|---|
| FreshnessStampService | Service | Writes stamps in the load transaction; marks and clears stale |
| FreshnessCheckStep | Job | Freshness step of JOB-01 and JOB-09 at each expected-by time |
| StaleMarkerListener | Listener | Consumes LoadRefused from the outbox and marks the product stale |
| DataProductLoadRepository | Repository | Reads and writes data_product_load |
| DataProductLoad | Entity | One row per product and business date |
| FreshnessQuery | Published interface | Stamps for other modules |
| FreshnessController | Controller | GET /data-products/freshness |
| DataFreshnessPanel | React component | Data panel on SCR-03 with business date, load time and the stale warning |

- Database: table data_product_load (new, Flyway migration in this story) with columns id uuid, product_code varchar(4), source_system varchar(40), business_date date, source_extracted_at timestamptz, loaded_at timestamptz, status varchar(10), stale_flagged_at timestamptz, duplicate_count integer default 0, plus the standard columns; unique (product_code, business_date); index (product_code, loaded_at desc). Reads data_product (RWB-E1-064). Reads loan_account.data_as_of and account_payment.data_as_of for row stamps.
- Configuration and reference data: data_product.refresh_cycle and expected_by, loaded by the data steward through RWB-E1-064; property `rwb.dataengine.freshness.alert-channel` set by the platform administrator.
- Build steps:
  1. Flyway migration for data_product_load with its unique key.
  2. FreshnessStampService.recordLoad(productCode, businessDate, sourceExtractedAt, loadedAt) called by the DP01 load of RWB-E1-003 in its commit transaction; repeat increments duplicate_count.
  3. FreshnessCheckStep with one Quartz trigger per product built from data_product; writes STALE, the FRESHNESS exception and the alert.
  4. StaleMarkerListener on LoadRefused, idempotent on the event ID.
  5. FreshnessQuery and FreshnessController with DataProductFreshness responses.
  6. P7 inputs snapshot builder (RWB-E1-027) calls stampsFor() and writes each stamp into the snapshot.
  7. DataFreshnessPanel on SCR-03 with the Stale input state and MSG-P1-001.
  8. Tests for AC1 to AC8 with a fixed test clock, and the access test.
- Feature flag: `rwb.dataengine.freshness-stamp`.
- Done when: the tests in section 16 pass and every Epic 1 load job calls recordLoad.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | A product is stale, shown in the case record data panel and the alert | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-002 | The load was refused at a check (shown on the alert) | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | Malformed product code or date in the query | Enter {field}. |
| MSG-P4-002 | Role without Case record R | You cannot {action} here. Your role does not include it. |

Thai text for each message follows decision DL10.

## 15. Screens and states

SCR-03 Case record, state Read only (Epic 1): the data panel shows each product's business date and load time. State Stale input: the panel shows MSG-P1-001 next to the stale product. State Loading: skeleton rows. The data steward sees stale products on SCR-45 Data quality from Epic 2 (state Breaks); in Epic 1 the same list comes from GET /admin/data-quality/exceptions.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-015-01 | AC1, BR1 | System | DP01 load for 2026-11-30, extract 23:30, load 06:50; account ACC-SYN-000101 |
| TC-E1-015-02 | AC2, BR2 | System | No DP01 load at 08:00; test clock |
| TC-E1-015-03 | AC3, BR4 | System | Decision for RW-2026-000101 reading DP01 and DP06 |
| TC-E1-015-04 | AC4, BR3 | System | LoadRefused for DP01 at check Control totals |
| TC-E1-015-05 | AC5, BR5 | System | Same stamp written twice |
| TC-E1-015-06 | AC6 | System | Late DP01 load at 08:40 after the stale flag |
| TC-E1-015-07 | AC7 | System | DP01 load at 07:59 |
| TC-E1-015-08 | AC8, BR6 | System | Weekly DP06 load Monday; check on Thursday |
| TC-E1-015-09 | Access | Access | RW-REFADM calls GET /data-products/freshness; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: expected-by times, cycles and the alert channel are data rows or properties.
- No personal data in logs, tests or prompts; stamps carry product codes and times only.
- No read of another module's tables: P3 and P7 read stamps only through FreshnessQuery; this story writes no P7 table.
- The stale check never deletes or changes loaded rows; the previous load stays in use.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-009 | Every data product carries a freshness stamp; every decision records the freshness of its data | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-14, FEAT-DRI-12 | All recovery processes; 17 Run the decision center | R-UNI-40; CTL-02 | TC-E1-015-01 to TC-E1-015-08 |

## 19. Out of scope

- The MSG-P7-006 warning on a decision screen when an input is past its age limit (decision screens, Epic 2).
- Same-day data for named triggers (DL06).
- The data quality console SCR-45 (Epic 2) and the reconciliation report (RWB-E1-011).
- Freshness of the stage 2 data products (RWB-E2-010).

