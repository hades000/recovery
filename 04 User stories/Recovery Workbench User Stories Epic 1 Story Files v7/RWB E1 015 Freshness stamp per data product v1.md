# RWB-E1-015 Freshness stamp per data product

SCB Collections and Recovery. Henka Group, 15 November 2026.

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
| Decision | D-RCV-35 (U1, U4); ADR-010; DL43 open |
| Priority | Must |
| Depends on | RWB-E1-001, RWB-E1-069, RWB-E1-027 |
| Status | Ready for build, Tier 2 behind a flag until RWB-ACE-001 lands (DL43) |

## 1. Story

As a **data steward and data product owner (RW-DATASTEW)**, I want **every data product to carry the business date, start time, completion time and status of the ACE batch it came from, exposed to every consumer and shown on the case record view, and every daily data job to start only when the sources it reads are complete for the business date**, so that **every decision input states how old it is, stale facts are visible, and no list is built from a half-loaded day**.

## 2. Business rationale

The Workbench loads no source data; ACE does (D-RCV-35 U1). A fact on the case can therefore be one day or one week old, and the Workbench cannot time its own load. ACE writes one `ace_batch_run` row per source and business date and the Workbench reads it through `v_ace_batch_status`. A stamp per product and business date, shown on the case record and copied into each decision's inputs snapshot, makes the age of every input visible to the person deciding and to audit. A product whose batch has not completed by its cut-off is flagged stale the same morning. The same reading closes the daily gate that the retired load checks used to provide: no data job for a business date starts until every source it reads is COMPLETED. Serves REQ-RDF-009; measure: the ACE batch is complete when the Workbench reads it on 99 percent of days.

## 3. Preconditions

- RWB-E1-001 is done: data_product holds DP01 to DP14 and data_product_load exists.
- RWB-E1-069 is done: `v_ace_batch_status` is created in Section B, over `public.ace_batch_run` owned by the ACE team. Until RWB-ACE-001 lands the feature stays behind its flag (DL43).
- RWB-E1-027 is done: the P7 decision log writer builds an inputs snapshot for each entry.
- The data product catalog is loaded with refresh cycle and expected-by time for each product (08:00 for daily products, MON 08:00 for weekly products; DL11).
- The reader holds Case record R (case roles) or Platform administration R (data steward, platform administrator).
- The recovery service identity (recovery_svc) holds SELECT on `recovery.v_ace_*` and no privilege on `public`.

## 4. Flow

1. System: reads `v_ace_batch_status`, one row per source system and business date, for a new or changed COMPLETED row.
2. FreshnessStampService: reads the product-to-source map (section 12) and, in one transaction, writes or updates one data_product_load row for each product the source feeds, with the business date, `source_extracted_at` from `started_at`, `loaded_at` from `completed_at` and status LOADED.
3. System: for a product fed by more than one source, sets the stamp to the oldest business date among its sources and marks it STALE while any of them is late.
4. System: at each product's `expected_by` time, checks that a COMPLETED row exists in `v_ace_batch_status` for the expected business date.
5. System: for a product with no COMPLETED row, marks its latest stamp in use (the previous complete business date) STALE with `stale_flagged_at`, publishes EV-27 AceDataLate and sends the operations alert. No row is written for a business date with no batch, because the stamp needs the source start and completion times.
6. System: on a FAILED batch row, marks the product STALE at once; the stamp for the last complete business date stays the one in use.
7. DailyCompletenessGate: at the cut-off for the day, reads `v_ace_batch_status` for the sources the day's data jobs read; when every one is COMPLETED, returns COMPLETE and lets JOB-04 start; otherwise returns HOLD, names the product and the source, and raises the alert.
8. Consumer (case record view, P3 or P7): calls FreshnessQuery or GET /data-products/freshness and receives business date, source start time, completion time and status per product.
9. Case record view: shows the stamp in the data panel, with MSG-P1-001 when the product is stale.
10. P7 inputs snapshot builder: calls FreshnessQuery.stampsFor() for the products a decision reads and writes each stamp into the snapshot that inputs_ref points to.
11. System: a later COMPLETED batch for the same business date sets status LOADED, records the new `loaded_at`, and starts the daily jobs through EV-26.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No COMPLETED batch for the expected business date by the expected-by time | Product set STALE; EV-27 published; operations alert sent; case record shows the stale warning | MSG-P1-001 | AC2 |
| X2 | The batch row is FAILED | Product set STALE at once; the previous stamp stays in use; no daily job starts | MSG-P1-001 | AC4 |
| X3 | The same COMPLETED batch row is read twice | One data_product_load row; the repeat is counted (R-UNI-40); no second event | None | AC5 |
| X4 | A late batch arrives after the stale flag | Status LOADED with the new completion time; the jobs start for that business date | None | AC6 |
| X5 | A batch completes one minute before the expected-by time | Product not flagged stale | None | AC7 |
| X6 | A weekly product inside its weekly cycle | Product not flagged stale on the days between batches | None | AC8 |
| X7 | One source of a multi-source product is late | The product carries the oldest business date among its sources and is STALE; EV-27 names the late source | MSG-P1-001 | AC11 |
| X8 | A source that the day's jobs do not read is late | The gate still returns COMPLETE; only the products that read that source are STALE | MSG-P1-001 | AC10 |
| X9 | A role without the right reads the stamps | 403 | MSG-P4-002 | TC-E1-015-09 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the tables (RWB-E1-001), the batch view (RWB-E1-069) and the decision log writer (RWB-E1-027) |
| Negotiable | Expected-by times, refresh cycles and the product-to-source map are data rows; the story fixes the stamping, the stale check and the gate |
| Valuable | Every decision and every case record shows the age of its data, and no list is built on an incomplete day |
| Estimable | One table, one service, one listener, one gate, two endpoints, one panel |
| Small | Finished inside two weeks with its tests |
| Testable | Each criterion runs against a test clock and synthetic batch rows |

## 7. Acceptance criteria

```gherkin
Feature: Freshness stamp per data product

  Background:
    Given data product "DP01" Account and arrears has refresh cycle "DAILY" and expected-by time 08:00
    Given data product "DP06" Collateral and asset has refresh cycle "WEEKLY" and expected-by time Monday 08:00

  Scenario: AC1 Freshness from the ACE batch
    Given v_ace_batch_status holds source "ALS", business date 2026-11-30, started 2026-11-30T23:30+07:00, completed 2026-12-01T05:40+07:00, status "COMPLETED" and record count 184,500
    When EV-26 AceDataReady is processed and GET /data-products/freshness?product=DP01 is called
    Then data_product_load holds DP01 for 2026-11-30 with source time 2026-11-30T23:30+07:00, load time 2026-12-01T05:40+07:00 and status "LOADED"
    Then FreshnessQuery.stampForRow("DP01", 2026-11-30) returns the same stamp
    Then GET /data/freshness?sourceSystem=ALS returns the same ACE batch row with isComplete true and ageDays 1
    Then JOB-02, JOB-04, JOB-07 and JOB-08 are started for 2026-11-30

  Scenario: AC2 Stale product flagged at the cut-off
    Given no COMPLETED ALS row for 2026-11-30 is in v_ace_batch_status at 08:00 on 2026-12-01
    When the DP01 cut-off passes
    Then EV-27 AceDataLate is in the outbox with sourceSystem "ALS", businessDate 2026-11-30 and the latest status
    Then the DP01 stamp for 2026-11-27 is "STALE" with stale_flagged_at 2026-12-01T08:00+07:00
    Then the alert goes to the data steward and the operations channel
    Then the case record view shows the stamp in the data panel with "Account and arrears is from 2026-11-27. Today's ACE batch has not arrived."

  Scenario: AC3 Freshness in the decision log
    Given a decision log entry for case "RW-2026-000101" read DP01 for 2026-11-30 and DP06 for 2026-11-23
    When the entry and its inputs snapshot are read
    Then the snapshot lists DP01 with load time 2026-12-01T05:40+07:00 and status "LOADED"
    Then the snapshot lists DP06 with load time 2026-11-24T04:40+07:00 and status "LOADED"

  Scenario: AC4 A failed ACE batch marks the product stale at once
    Given v_ace_batch_status shows ALS for 2026-11-30 with status "FAILED" at 05:20
    When the row is read
    Then the DP01 stamp for 2026-11-27 is marked "STALE" from 05:20 and EV-27 is published
    Then the stamp for business date 2026-11-27 stays the one in use
    Then no data job is started for 2026-11-30

  Scenario: AC5 The same batch read twice
    Given the DP01 stamp for 2026-11-30 is LOADED
    When the same COMPLETED ALS row is read again
    Then data_product_load still holds one DP01 row for 2026-11-30 with duplicate_count 1
    Then no second EV-26 is processed and no data job starts twice

  Scenario: AC6 A late batch clears the stale flag
    Given DP01 was flagged "STALE" at 08:00 on 2026-12-01
    When the ALS batch for 2026-11-30 completes at 08:40
    Then EV-26 is raised
    Then DP01 is "LOADED" with load time 2026-12-01T08:40+07:00
    Then JOB-02, JOB-04, JOB-07 and JOB-08 start for 2026-11-30

  Scenario: AC7 A batch one minute before the expected-by time
    Given the ALS batch for 2026-11-30 completes at 07:59 on 2026-12-01
    When the freshness step runs at 08:00
    Then the system does not flag DP01 stale

  Scenario: AC8 A weekly product between its batches
    Given the DP06 batch for business date 2026-11-30 completed at 04:40 on Monday 2026-11-30
    When the freshness step runs at 08:00 on Thursday 2026-12-03
    Then the system does not flag DP06 stale

  Scenario: AC9 Daily completeness gate holds the case list
    Given at 08:00 on 2026-12-01 the ALS, SCBPDM, LIT, WIN, COLLINS and GL batches for 2026-11-30 are COMPLETED
    Given the EFS batch for 2026-11-30 is FAILED
    When the daily completeness gate runs
    Then it returns HOLD and names DP05 Contact and promises and source "EFS"
    Then the case list step of JOB-04 does not start and no case_list_row for 2026-11-30 is written
    Then the lake keeps the released case list of 2026-11-27
    Then the data steward and the team manager group receive MSG-P1-001 "DP05 Contact and promises is from 2026-11-27. Today's ACE batch has not arrived."

  Scenario: AC10 Daily completeness gate releases when every source is complete
    Given at 08:00 on 2026-12-01 every source the day's jobs read is COMPLETED for 2026-11-30
    Given the SVAF batch for 2026-11-30 is absent and no job of the day reads DP06
    When the daily completeness gate runs
    Then it returns COMPLETE and records the business date, the sources read and the completion time
    Then DP06 is not marked stale by the gate, and its own weekly cut-off decides its stamp
    Then JOB-04 starts and the case list step runs for 2026-11-30

  Scenario: AC11 A product fed by several sources
    Given v_ace_batch_status shows CCMS COMPLETED for 2026-11-27 and SVAF COMPLETED only up to 2026-11-20
    When the DP06 cut-off passes at MON 08:00 on 2026-11-30
    Then DP06 carries business date 2026-11-20 and status "STALE"
    Then EV-27 names sourceSystem "SVAF"
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every COMPLETED ACE batch row writes one freshness stamp per product it feeds and business date, from `v_ace_batch_status` only, in the same transaction as the event handling | REQ-RDF-009; BR-P1-014-2 |
| BR2 | A product with no COMPLETED batch for its expected business date by its expected-by time is stale | data_product.expected_by; DL11 |
| BR3 | A failed ACE batch leaves the previous complete business date in use and marks the product stale at once | BR-P1-014; EV-27 |
| BR4 | A product fed by more than one source carries the oldest business date among its sources and is STALE while any of them is late | BR-P1-014-3 |
| BR5 | Every decision records, in its inputs snapshot, the product, business date, load time and status of each data product it read | REQ-RDF-009; FEAT-DRI-12; DF-DEC-008 |
| BR6 | A repeat read of the same COMPLETED batch row is ignored and counted | R-UNI-40 |
| BR7 | Expected-by times, refresh cycles and the product-to-source map are data rows, not code | Principle 1; DT02 |
| BR8 | No daily data job for a business date starts until every source it reads is COMPLETED for that date. When one is not, the case list holds, the previous list stays published and the data steward is alerted. This gate replaces the daily gate of the retired load checks | BR-P1-014-4; FSD P1 A2.14 |
| BR9 | Freshness is read from `v_ace_batch_status` only; the Workbench never infers it from `data_as_of`, a row count or a file | BR-P1-014-2 |
| BR10 | The Workbench writes no ACE data, and the stamp holds product codes, source codes and times only | D-RCV-35 U4; CTL-11 |

## 9. State transitions

None. This story does not change a case status. It changes the freshness status of a data product load: LOADED to STALE when the expected batch is missing or failed, and STALE to LOADED when a later COMPLETED batch arrives. The daily gate result is held in the job run, not in a table of its own.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| recovery_svc, recovery service identity | Reads the batch view; writes data_product_load; marks products stale; publishes EV-26 and EV-27; runs the daily gate |
| SY-DECLOG, decision log writer | Reads stamps through FreshnessQuery for the inputs snapshot |
| RW-DATASTEW, data steward | Reads stamps and the gate result (Platform administration R); receives the stale alert |
| RW-PLATADM, platform administrator | Reads stamps and the gate result; receives the operations alert |
| Case roles with Case record R, for example RW-CASEOWN, RW-TEAMMGR | Read the stamp in the case record data panel |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-178 | v_ace_batch_status | source_system | Read |
| DF-ACE-179 | v_ace_batch_status | business_date | Read |
| DF-ACE-180 | v_ace_batch_status | started_at | Read |
| DF-ACE-181 | v_ace_batch_status | completed_at | Read |
| DF-ACE-182 | v_ace_batch_status | status | Read |
| DF-ACE-183 | v_ace_batch_status | record_count | Read |
| DF-ACE-185 | v_ace_batch_status | feed_version | Read |
| DF-ACE-186 | v_ace_batch_status | is_complete | Read |
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
| DF-DEC-008 | decision_log_entry | inputs_ref | Read |
| DF-RPT-002 | case_list_row | business_date | Read (gate) |
| DF-RPT-019 | case_list_row | publish_status | Read (gate) |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Endpoints**

| Item | Value |
|---|---|
| Method and path | GET /data-products/freshness |
| Request | Query: product (optional, DP01 to DP14), asOf (optional, business date) |
| Response | DataProductFreshness[]: productCode, productName, businessDate, sourceExtractedAt, loadedAt, status (LOADED or STALE), staleSince |
| Errors | 400 malformed product or date (MSG-GEN-001); 401 no session (MSG-P4-001); 403 role lacks the right (MSG-P4-002); 503 store down (MSG-GEN-006) |
| Authorization | Case record, R. No case scope applies: the stamp holds no case data |
| Idempotency | Not applicable |

| Item | Value |
|---|---|
| Method and path | GET /data/freshness |
| Request | Query: sourceSystem (optional), businessDate (optional) |
| Response | DataFreshness[]: sourceSystem, businessDate, startedAt, completedAt, status, recordCount, feedVersion, isComplete, ageDays |
| Authorization | Case record, R |
| Note | Reads `v_ace_batch_status`; no Workbench row is written by the read |

**Published interfaces** (P1 to P3, P7 and JOB-04)

```java
package recovery.dataengine.freshness.api;

public interface FreshnessQuery {
    FreshnessStamp stampFor(String productCode);
    FreshnessStamp stampForRow(String productCode, LocalDate businessDate);
    Map<String, FreshnessStamp> stampsFor(Set<String> productCodes);
}

public record FreshnessStamp(String productCode, LocalDate businessDate,
        OffsetDateTime sourceExtractedAt, OffsetDateTime loadedAt,
        FreshnessStatus status, OffsetDateTime staleSince) {}

public interface DailyCompletenessGate {
    GateResult check(LocalDate businessDate, Set<String> productCodes); // COMPLETE, or HOLD with product and source
}
```

**Product-to-source map**

| Data product | Source systems in v_ace_batch_status |
|---|---|
| DP01 Account and arrears | ALS |
| DP02 Customer and party | SCBPDM |
| DP05 Contact and promises | EFS |
| DP06 Collateral and assets | CCMS, SVAF, AMIS, RPS |
| DP07 Legal events and cases | LIT, WIN |
| DP11 Scores and route economics | COLLINS |
| DP13 Money and closure | ALS, GL |
| DP03, DP04, DP08, DP09, DP10, DP12, DP14 | None; Workbench records, current on change |

The map is a reference row set owned by the data steward, loaded through RWB-E1-043, not code.

**Job step and events**

| Item | Value |
|---|---|
| Trigger | A new or changed row in v_ace_batch_status; and one Quartz trigger per product at data_product.expected_by, Asia/Bangkok |
| Job name | Freshness step, driven by the ACE batch listener and one Quartz trigger per product; the gate is called by JOB-04 before its case list step |
| Input | v_ace_batch_status rows; data_product rows; data_product_load rows for the expected business date |
| Output | data_product_load row or status STALE; EV-26 or EV-27; operations alert; gate result COMPLETE or HOLD |
| Events published | EV-26 AceDataReady, EV-27 AceDataLate |
| Events consumed | None; the story polls the batch view |
| Idempotency key | Product code and business date (unique key on data_product_load) |
| Restart behaviour | The step reads state each time; a rerun after a failure flags the same products and writes no second event for the same product, business date and batch row |

## 13. Solution plan

- Package: folder `recovery/dataengine/freshness`, Java package `recovery.dataengine.freshness`.

| Component | Type | Responsibility |
|---|---|---|
| FreshnessStampService | Service | Writes stamps from the batch row; marks and clears stale |
| FreshnessCheckStep | Job | Cut-off check per product at data_product.expected_by |
| DailyCompletenessGateImpl | Service | Implements DailyCompletenessGate over v_ace_batch_status and the product-to-source map |
| BatchStatusListener | Listener | Reads a new or changed COMPLETED or FAILED row and drives the stamp and the event |
| DataProductLoadRepository | Repository | Reads and writes data_product_load |
| DataProductLoad | Entity | One row per product and business date |
| FreshnessQuery | Published interface | Stamps for other modules |
| FreshnessController | Controller | GET /data-products/freshness and GET /data/freshness |
| DataFreshnessPanel | React component | Data panel on SCR-03 with business date, load time and the stale warning |

- Database: data_product_load is created by V0001 (RWB-E1-001) with id uuid, product_code varchar(25), source_system varchar(40), business_date date, source_extracted_at timestamptz, loaded_at timestamptz, status varchar(10) with values LOADED and STALE, stale_flagged_at timestamptz, duplicate_count integer default 0, plus the standard columns; unique (product_code, business_date). The next free migration adds index `(product_code, loaded_at desc)`. No new table. Reads data_product and `v_ace_batch_status`; no read of `data_as_of` for freshness.
- Configuration and reference data: data_product.refresh_cycle and expected_by, loaded by the data steward through RWB-E1-064; the product-to-source map loaded through RWB-E1-043; property `rwb.dataengine.freshness.alert-channel` set by the platform administrator.
- Build steps:
  1. Write the index migration and DataProductLoadRepository with its unique key.
  2. FreshnessStampService.recordBatch(productCode, businessDate, startedAt, completedAt) called from BatchStatusListener; a repeat increments duplicate_count and publishes no second event.
  3. FreshnessCheckStep with one Quartz trigger per product built from data_product; writes STALE, publishes EV-27 and the alert.
  4. BatchStatusListener on a FAILED row, idempotent on the source, business date and status; writes STALE at once.
  5. DailyCompletenessGateImpl over the map; unit test a late source that the day does not read and a late source that it does.
  6. FreshnessQuery and FreshnessController with DataProductFreshness and DataFreshness responses.
  7. P7 inputs snapshot builder (RWB-E1-027) calls stampsFor() and writes each stamp into the snapshot.
  8. DataFreshnessPanel on SCR-03 with the Stale input state and MSG-P1-001.
  9. Tests for AC1 to AC11 with a fixed test clock, and the access test.
- Feature flag: `rwb.dataengine.freshness-stamp`. The flag is on only after RWB-ACE-001 creates `public.ace_batch_run` and V0003 creates `v_ace_batch_status` (DL43); before that the panel shows no stamp rather than a guessed one.
- Done when: the tests in section 16 pass and every daily data job calls DailyCompletenessGate before it starts.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | A product is stale, or the gate holds a job, shown in the case record data panel and the alert | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-001 | Malformed product code or date in the query | Enter {field}. |
| MSG-GEN-006 | The store or the view is unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | Role without Case record R | You cannot {action} here. Your role does not include it. |

Thai text for each message follows decision DL10.

## 15. Screens and states

SCR-03 Case record, state Read only (Epic 1): the data panel shows each product's business date and load time. State Stale input: the panel shows MSG-P1-001 next to the stale product. State Loading: skeleton rows. The data steward sees stale products and the gate result on SCR-45 Data quality from Epic 2; in Epic 1 the same list comes from GET /data-products/freshness and the job listing.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-015-01 | AC1, BR1 | System | ALS batch row for 2026-11-30, started 23:30, completed 05:40; DP01 |
| TC-E1-015-02 | AC2, BR2 | System | No COMPLETED ALS row at 08:00; test clock |
| TC-E1-015-03 | AC3, BR5 | System | Decision for RW-2026-000101 reading DP01 and DP06 |
| TC-E1-015-04 | AC4, BR3 | System | ALS batch row FAILED at 05:20 |
| TC-E1-015-05 | AC5, BR6 | System | Same COMPLETED row read twice |
| TC-E1-015-06 | AC6 | System | Late ALS batch at 08:40 after the stale flag |
| TC-E1-015-07 | AC7 | System | ALS batch at 07:59 |
| TC-E1-015-08 | AC8, BR7 | System | Weekly DP06 batch on Monday; check on Thursday |
| TC-E1-015-09 | Access | Access | RW-REFADM calls GET /data-products/freshness; refused with MSG-P4-002 |
| TC-E1-015-10 | AC9, BR8 | System | EFS batch FAILED at the 08:00 cut-off; case list step stub |
| TC-E1-015-11 | AC10, BR8 | System | Every source COMPLETED for 2026-11-30 |
| TC-E1-015-12 | AC11, BR4 | System | CCMS COMPLETED 2026-11-27; SVAF only to 2026-11-20 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: expected-by times, cycles, the product-to-source map and the alert channel are data rows or properties.
- No personal data in logs, tests or prompts; stamps carry product codes, source codes and times only.
- No read of another module's tables: P3 and P7 read stamps only through FreshnessQuery; this story writes no P7 table.
- ACE data only through `recovery.v_ace_*` views; the story never reads `public.ace_batch_run` directly and writes nothing to ACE.
- The stale check never deletes or changes a loaded row; the previous complete business date stays in use.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-009 | Every data product carries a freshness stamp from the ACE batch record; every decision records the freshness of the data it used | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-14, FEAT-DRI-12 | All recovery processes; 17 Run the decision center | R-UNI-40; BR-P1-014-2 to BR-P1-014-4 | TC-E1-015-01 to TC-E1-015-12 |

## 19. Out of scope

- The MSG-P7-006 warning on a decision screen when an input is past its age limit (decision screens, Epic 2).
- Same-day data for named triggers (DL06).
- The data quality console SCR-45 (Epic 2) and the reconciliation report (RWB-E1-011).
- Freshness of the stage 2 data products (RWB-E2-010).
- ACE's own ingestion monitoring and its alerting (RWB-ACE-001).
