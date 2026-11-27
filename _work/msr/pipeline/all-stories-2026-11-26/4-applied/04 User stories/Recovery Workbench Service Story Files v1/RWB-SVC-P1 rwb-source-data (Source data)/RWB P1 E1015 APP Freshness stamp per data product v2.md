# RWB-P1-E1015-APP Freshness stamp per data product

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1015-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-015 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP05, DP07, DP09, DP10, DP11, DP15, DP19 |
| Parallel lane | L-P1-A |
| Ready to start | After RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| Depends on (build) | RWB-P1-E1015-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P7-E1027-CON |
| Integration dependencies | None |
| External dependencies | RWB-P1-E1015-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-014, FR-P1-015, FR-P1-016, FR-P1-017) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-015 for rwb-source-data. The freshness stamp, the stale flag and the daily gate move from a Quartz job over the one `recovery` schema to `AceIngestCheckWorkflow` on task queue `rwb-source-data`, started by a listener on `v_ace_batch_status` and by one Temporal Schedule per data product (DP-10). The stamps are written in `rwb_source_data` (DP-01, DP-02, DP-15); `AceDataReady` (EV-26) and `AceDataLate` (EV-27) are published on `rwb.source-data.events.v1` through the outbox (DP-09); the decision inputs snapshot stays P7's, read through `FreshnessQuery` (DP-03, DP-11). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P1-E1015-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **data steward and data product owner (RW-DATASTEW)**, I want **every data product to carry the business date, start time, completion time and status of the ACE batch it came from, exposed to every consumer and shown on the case record view, and every daily data job to start only when the sources it reads are complete for the business date**, so that **every decision input states how old it is, stale facts are visible, and no list is built from a half-loaded day**.

The legacy story built the stamp as a service of the one `recovery-core` deployable: a `data_product_load` table in the shared `recovery` schema, an in-process `FreshnessStampService` behind `FreshnessQuery`, one Quartz trigger per product, and a `recovery_svc` login that read `recovery.v_ace_*`. D-RCV-60 keeps the behaviour and moves the ownership:

- **Kept in substance:** one stamp per data product and business date, written from `v_ace_batch_status` only (BR9); the cut-off per product at `data_product.expected_by`; the stale flag with `stale_flagged_at`; the oldest business date for a product fed by several sources; the daily completeness gate; the two events; the two read operations.
- **The stamp now lives in P1's own schema:** `data_product_load` is in `rwb_source_data`, created by RWB-P1-E1001-APP and written only here (DP-01, DP-15). No other service reads it; a caller reaches freshness through the contract of RWB-P1-E1015-CON (DP-11).
- **Quartz becomes Temporal:** the freshness step is `AceIngestCheckWorkflow` on task queue `rwb-source-data` in namespace `rwb-recovery`, started by a listener on `v_ace_batch_status` and by one cut-off Schedule per source-fed data product at `data_product.expected_by`, Asia/Bangkok (DP-10).
- **In-process calls become events and a contract:** `AceDataReady` and `AceDataLate` are published as `rwb.source-data.AceDataReady.v1` and `rwb.source-data.AceDataLate.v1` on `rwb.source-data.events.v1` under a CloudEvents 1.0 envelope (DP-09); `FreshnessQuery` and `DailyCompletenessGate` are published interfaces of this service, reached over the contract, one hop and 2 s timeout (DP-11).
- **The decision log stays P7's:** this story writes no `decision_log_entry` and no inputs snapshot. P7 calls `FreshnessQuery` (contract dependency RWB-P7-E1027-CON) and writes each stamp into its own snapshot (DP-03).
- **Bases and names:** schema and login `rwb_source_data`, REST base `/api/recovery/source-data/v1`, topic `rwb.source-data.events.v1`, event names `rwb.source-data.<Event>.v1`, task queue `rwb-source-data` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.sourcedata` (DP-02, DP-13, DP-14). The panel reaches the record through the gateway-bff composite route (DP-19).

### 2. Business rationale

The Workbench loads no source data; ACE does (D-RCV-35 U1). A fact on the case can therefore be one day or one week old, and the Workbench cannot time its own load. ACE writes one batch row per source and business date and the Workbench reads it through `v_ace_batch_status`. A stamp per product and business date, shown on the case record and copied into each decision's inputs snapshot, makes the age of every input visible to the person deciding and to audit. A product whose batch has not completed by its cut-off is flagged stale the same morning. The same reading closes the daily gate that the retired load checks used to provide: no data job for a business date starts until every source it reads is COMPLETED. Serves REQ-RDF-009; measure: the ACE batch is complete when the Workbench reads it on 99 percent of days (FSD P1 A2.14.1).

**What D-RCV-60 changes.** Not the rationale. What changes is where the stamp is kept and how it is started and delivered: in `rwb_source_data` instead of the shared schema, by `AceIngestCheckWorkflow` on this service's own queue instead of one Quartz job, and by two Kafka events and two published interfaces instead of in-process calls into a monolith. The consumers named in the architecture stay the same people: rwb-case starts `DailyCaseRun` on `AceDataReady`, rwb-payment, rwb-deviation and rwb-writeoff consume it, and the stale banner reaches gateway-bff on `AceDataLate` (Arch v5 slide 43, rows 26 and 27).

**One source of truth.** Freshness is read from `v_ace_batch_status` only and never inferred from `data_as_of`, a row count or a file (BR9; FSD P1 A2.14.3 BR-P1-014-2). The Workbench writes no ACE data and holds product codes, source codes and times only.

### 3. Preconditions

- RWB-P1-E1001-APP is done: `data_product` holds DP01 to DP14 and `data_product_load` exists in `rwb_source_data` with its unique key on `(product_code, business_date)`.
- RWB-P1-E1069-APP is done: `v_ace_batch_status` is readable through the `rwb_source_data` login, which holds SELECT on the 30 `recovery.v_ace_*` views and no privilege on `public` (DP-02, DP-05). Until RWB-ACE-001 lands the feature stays behind its flag (DL43).
- RWB-P1-E1015-CON is published: the three operations, the two interface jars, the two event schemas and the activity contract are baselined and faked.
- The data product catalog carries refresh cycle and expected-by time for each product (08:00 for daily products, MON 08:00 for weekly products; DL11).
- The reader holds Case record R (case roles) or Platform administration R (data steward, platform administrator).
- The product-to-source map is loaded as reference rows through RWB-P1-E1001-APP's catalog path; it is not code (DP-07).
- RWB-PLT-E1071-CON (workflow kit and Schedule registration), RWB-PLT-TE006-CON (outbox and inbox), RWB-PLT-E1027-CON (local decision-record library), RWB-PLT-E1043-CON and RWB-P3-E1043-CON (reference data) and RWB-PLT-N001-CON (composite route) are in place.
- The source/load time mapping of the stamp is fixed by GAP-0492 and ASM-0684; the event envelope by GAP-0493 and ASM-0685; the Schedule names and the per-product cut-offs beyond the two seeded values by GAP-0494 and ASM-0686.

### 4. Flow

1. System: reads `v_ace_batch_status`, one row per source system and business date, and the listener takes a new or changed COMPLETED or FAILED row.
2. The listener starts `AceIngestCheckWorkflow` on `rwb-source-data` with the source system, the business date and the observed status as its input; the workflow ID is derived from the source system and the business date, so a redelivery starts no second run.
3. `stampProducts` activity: reads the product-to-source map and, in one transaction, writes or updates one `data_product_load` row for each product the source feeds, with the business date, `source_extracted_at` from `started_at`, `loaded_at` from `completed_at` and status LOADED; the transaction writes `rwb.source-data.AceDataReady.v1` to the outbox.
4. For a product fed by more than one source, the stamp carries the oldest business date among its sources and is STALE while any of them is late.
5. At each product's `expected_by` time the cut-off Schedule starts the same workflow in check mode: it asks whether a COMPLETED row exists for the expected business date.
6. For a product with no COMPLETED row, `markStale` sets its latest stamp in use (the previous complete business date) STALE with `stale_flagged_at`, writes `rwb.source-data.AceDataLate.v1` to the outbox and raises the operations alert. No row is written for a business date with no batch, because the stamp needs the source start and completion times.
7. On a FAILED batch row the product is marked STALE at once; the stamp for the last complete business date stays the one in use.
8. `DailyCompletenessGate`: at the cut-off for the day, reads `v_ace_batch_status` for the sources the day's jobs read; when every one is COMPLETED it returns COMPLETE and lets JOB-04 start; otherwise it returns HOLD, names the product and the source, and raises the alert.
9. Consumer (case record view through gateway-bff, P3 or P7): calls `GET /data-products/freshness` or `FreshnessQuery` and receives business date, source start time, completion time and status per product.
10. Case record view: shows the stamp in the data panel, with MSG-P1-001 when the product is stale.
11. P7 inputs snapshot builder: calls `FreshnessQuery.stampsFor()` for the products a decision reads and writes each stamp into the snapshot that `inputs_ref` points to; P1 writes nothing there.
12. System: a later COMPLETED batch for the same business date sets status LOADED, records the new `loaded_at`, and starts the daily jobs through `AceDataReady`.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No COMPLETED batch for the expected business date by the expected-by time | Product set STALE; `AceDataLate` published; operations alert sent; case record shows the stale warning | MSG-P1-001 | AC2 (other slice) |
| X2 | The batch row is FAILED | Product set STALE at once; the previous stamp stays in use; no daily job starts | MSG-P1-001 | AC4 (other slice) |
| X3 | The same COMPLETED batch row is read twice | One `data_product_load` row; the repeat is counted in `duplicate_count` (R-UNI-40); no second event | None | AC5 (other slice) |
| X4 | A late batch arrives after the stale flag | Status LOADED with the new completion time; the jobs start for that business date | None | AC6 (other slice) |
| X5 | A batch completes one minute before the expected-by time | Product not flagged stale | None | AC7 (other slice) |
| X6 | A weekly product inside its weekly cycle | Product not flagged stale on the days between batches | None | AC8 |
| X7 | One source of a multi-source product is late | The product carries the oldest business date among its sources and is STALE; `AceDataLate` names the late source | MSG-P1-001 | AC11 (other slice) |
| X8 | A source that the day's jobs do not read is late | The gate still returns COMPLETE; only the products that read that source are STALE | MSG-P1-001 | AC10 (other slice) |
| X9 | A role without the right reads the stamps | 403 | MSG-P4-002 | TC-E1-015-09 |
| X10 | P7's snapshot is read and P1 is unavailable | The read answers with the stamp last written; no snapshot is recomputed and no value is guessed | MSG-GEN-006 | AC3 |
| X11 | The outbox relay cannot reach the topic | The stamp stands; the event stays in the outbox and is retried, then dead-lettered with an alert | None | RWB-P1-E1015-OPS AC3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published contract of RWB-P1-E1015-CON and its fakes, on the tables of RWB-P1-E1001-APP and the views of RWB-P1-E1069-APP |
| Negotiable | Expected-by times, refresh cycles and the product-to-source map are data rows; the story fixes the stamping, the stale check and the gate |
| Valuable | Every decision and every case record shows the age of its data, and no list is built on an incomplete day |
| Estimable | One workflow, four activities, one repository, one gate, three endpoints, one panel |
| Small | Finished inside two weeks with its tests |
| Testable | Each criterion runs against a test clock and synthetic batch rows, plus one component test of the panel state |

### 7. Acceptance criteria

```gherkin
Feature: Freshness stamp per data product

  Background:
    Given data product "DP01" Account and arrears has refresh cycle "DAILY" and expected-by time 08:00
    Given data product "DP06" Collateral and asset has refresh cycle "WEEKLY" and expected-by time Monday 08:00

  Scenario: AC3 Freshness in the decision log (legacy RWB-E1-015 AC3)
    Given the rwb-decision decision-record contract mock returns the inputs snapshot for case RW-2026-000101
    Given a decision log entry for case "RW-2026-000101" read DP01 for 2026-11-30 and DP06 for 2026-11-23
    When the entry and its inputs snapshot are read
    Then the snapshot lists DP01 with load time 2026-12-01T05:40+07:00 and status "LOADED"
    Then the snapshot lists DP06 with load time 2026-11-24T04:40+07:00 and status "LOADED"

  Scenario: AC8 A weekly product between its batches (legacy RWB-E1-015 AC8)
    Given the DP06 batch for business date 2026-11-30 completed at 04:40 on Monday 2026-11-30
    When the freshness step runs at 08:00 on Thursday 2026-12-03
    Then the system does not flag DP06 stale
```

**Target reading.** Both criteria are the legacy lines, value for value, with their origin tags. The only addition is one `Given` on AC3 that stubs the rwb-decision decision-record contract the snapshot is read from; no legacy line is changed or dropped. What changes is where each assertion runs:

- **AC3.** The entry and its inputs snapshot are written by rwb-decision (P7) through the local decision-record library; this story writes neither (DP-03). P1's part is the two stamps: `data_product_load` in `rwb_source_data` holds DP01 for 2026-11-30 with load time 2026-12-01T05:40+07:00 and DP06 for 2026-11-23 with load time 2026-11-24T04:40+07:00, and `FreshnessQuery.stampsFor({DP01, DP06})` returns exactly those two values to P7 over the contract, one hop and 2 s (DP-11). The load time is `completed_at` of the batch row (FSD P1 A2.14.2); the source time is `started_at` (GAP-0492; ASM-0684).
- **AC8.** The weekly cut-off is a Temporal Schedule on `rwb-source-data` at `data_product.expected_by` for DP06, in Asia/Bangkok, with overlap policy SKIP, instead of a Quartz trigger (DP-10). The check on Thursday 2026-12-03 still runs, still reads `v_ace_batch_status`, and still finds the Monday batch inside its weekly cycle, so DP06 is not flagged. The scheduled job and its clock are the only change; the values, the batch row and the outcome are unchanged.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every COMPLETED ACE batch row writes one freshness stamp per product it feeds and business date, from `v_ace_batch_status` only, in the same transaction as the outbox write of the event | REQ-RDF-009; BR-P1-014-2 |
| BR2 | A product with no COMPLETED batch for its expected business date by its expected-by time is stale | data_product.expected_by; DL11 |
| BR3 | A failed ACE batch leaves the previous complete business date in use and marks the product stale at once | BR-P1-014; EV-27 |
| BR4 | A product fed by more than one source carries the oldest business date among its sources and is STALE while any of them is late | BR-P1-014-3 |
| BR5 | Every decision records, in its inputs snapshot, the product, business date, load time and status of each data product it read; the snapshot is P7's and is filled from `FreshnessQuery` | REQ-RDF-009; FEAT-DRI-12; DF-DEC-008 |
| BR6 | A repeat read of the same COMPLETED batch row is ignored and counted in `duplicate_count` | R-UNI-40 |
| BR7 | Expected-by times, refresh cycles and the product-to-source map are data rows, not code | Principle 1; DT02 |
| BR8 | No daily data job for a business date starts until every source it reads is COMPLETED for that date. When one is not, the case list holds, the previous list stays published and the data steward is alerted. This gate replaces the daily gate of the retired load checks | BR-P1-014-4; FSD P1 A2.14 |
| BR9 | Freshness is read from `v_ace_batch_status` only; the Workbench never infers it from `data_as_of`, a row count or a file | BR-P1-014-2 |
| BR10 | The Workbench writes no ACE data, and the stamp holds product codes, source codes and times only | D-RCV-35 U4; CTL-11 |
| BR11 | One product cut-off is one Temporal Schedule per source-fed product, in Asia/Bangkok, with overlap policy SKIP; a redelivered batch row starts no second workflow run (DP-10) | Arch v5 slide 44; DP-10 |

**Where each rule lives in the target.** The rule text is unchanged and the IDs are kept. BR1, BR2, BR4, BR6 and BR11 are answered inside `rwb_source_data` by `data_product_load` and the workflow; BR3, BR7 and BR9 are answered by the same code reading `v_ace_batch_status`; BR5 is answered by rwb-decision calling `FreshnessQuery`, because the snapshot table is P7's (DP-01, DP-03); BR8 is answered by `DailyCompletenessGate` as an activity the reconciliation workflow calls before its case list step; BR10 is answered by the login, which holds no privilege outside its schema and the views (DP-02, DP-05).

### 9. State transitions

None in the case model: this story changes no case status. It moves the freshness status of a data product load and the run state of the check workflow.

| From | To | Trigger |
|---|---|---|
| No row | LOADED | A COMPLETED batch row is stamped for the product and business date; `AceDataReady` goes to the outbox |
| LOADED | LOADED (`duplicate_count` + 1) | The same COMPLETED row is read again; nothing else is written and no event is produced |
| LOADED | STALE with `stale_flagged_at` | The cut-off passes with no COMPLETED row, or the batch row reads FAILED; `AceDataLate` goes to the outbox |
| STALE | LOADED with the new `loaded_at` | A later COMPLETED batch arrives for that business date; `AceDataReady` is published |
| Running | Completed | Every mapped product of the source system is stamped, or the cut-off check has flagged what is late |
| Running | Failed, then retried by the workflow | A stamp transaction fails; the workflow retries the activity and writes no partial event |

The daily gate result is held in the run of the reconciliation workflow, not in a table of its own.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The rwb-source-data service identity (`rwb_source_data` login) | Reads the batch view; writes `data_product_load`; marks products stale; writes `AceDataReady` and `AceDataLate` to the outbox; runs the gate |
| SY-DECLOG, decision log writer of rwb-decision | Reads stamps through `FreshnessQuery` for the inputs snapshot |
| RW-DATASTEW, data steward | Reads stamps and the gate result (Platform administration R); receives the stale alert |
| RW-PLATADM, platform administrator | Reads stamps and the gate result; receives the operations alert |
| Case roles with Case record R, for example RW-CASEOWN, RW-TEAMMGR | Read the stamp in the case record data panel |

Every "who" is a role code; the roles and their rights are held as data in rwb-access and reached through its authorise contract, not by a table read (DP-01, DP-08).

### 11. Data

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
| DF-DEC-008 | decision_log_entry | inputs_ref | Read (through the P7 contract only; no table read) |
| DF-RPT-002 | case_list_row | business_date | Read (gate) |
| DF-RPT-019 | case_list_row | publish_status | Read (gate) |

Field IDs are those in the Logical Data Model and Data Dictionary. `data_product_load` is in `rwb_source_data` and is written here only; `decision_log_entry` is P7's and is never read by this service (DP-01, DP-03). The stamp takes `source_extracted_at` from `started_at` and `loaded_at` from `completed_at` (FSD P1 A2.14.2; legacy AC1), which conflicts with TSD P1 T3.6 and is recorded in GAP-0492 with ASM-0684.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-source-data (P1); base `/api/recovery/source-data/v1`. The shapes are baselined in RWB-P1-E1015-CON; the operation IDs are those of the P1 API appendix.

| Method | Path | Shape | Access |
|---|---|---|---|
| GET | `/data-products/freshness` | `DataProductFreshness[]`: productCode, productName, businessDate, sourceExtractedAt, loadedAt, status (LOADED or STALE), staleSince; query product (optional, DP01 to DP14) and asOf (optional) | Case record R |
| GET | `/freshness` | The architecture alias of the same read: query businessDate; answers the ACE batch rows with sourceSystem, status, completedAt and isComplete | Case record R |
| POST | `/business-days/{date}/ready` | The Airflow signal that the business date is ready: no body, an idempotency key, and the gate result COMPLETE or HOLD with the product and source that hold it | Server to server (workload identity) |

Errors are the RFC 9457 problem body with MSG-GEN-001 (400), MSG-P4-001 (401), MSG-P4-002 (403) and MSG-GEN-006 (503).

#### 12.2 REST operations consumed

None at run time. This service reads ACE only through `recovery.v_ace_batch_status` and the other `v_ace_*` views (DP-05), and it calls no other service; the P7 snapshot builder calls it, not the other way round (DP-11).

#### 12.3 Events published

| Event | Topic | Trigger | Payload |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` (EV-26) | `rwb.source-data.events.v1` | A mapped source batch is COMPLETED and its products are stamped LOADED | eventId, occurredAt, schemaVersion, sourceSystem, businessDate, status, completedAt |
| `rwb.source-data.AceDataLate.v1` (EV-27) | `rwb.source-data.events.v1` | A product cut-off passes with no COMPLETED row, or the batch row reads FAILED | eventId, occurredAt, schemaVersion, sourceSystem, businessDate, status, completedAt |

Both are written to the outbox in the same transaction as the stamp and published by the relay under a CloudEvents 1.0 envelope; the field mapping is fixed in GAP-0493 with ASM-0685. Consumers of AceDataReady are rwb-case, rwb-payment, rwb-deviation and rwb-writeoff; consumers of AceDataLate are the alerts and the gateway-bff banner (Arch v5 slide 43).

#### 12.4 Events consumed

None. The story polls the batch view; the architecture's IN line states that Airflow calls the ready signal and that the fallback polls the ACE batch record (Arch v5 slide 15).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AceIngestCheckWorkflow | Workflow, one run per source system and business date, workflow ID from both | `rwb-source-data` | Input schema sourceSystem, businessDate, observedStatus, mode (stamp or cutoff) |
| stampProducts | Activity | `rwb-source-data` | Product-to-source map in; stamps written and outbox row out, one transaction |
| markStale | Activity | `rwb-source-data` | Product, business date and time in; STALE stamp and outbox row out |
| publishAceDataReady, publishAceDataLate | Activity (event library) | `rwb-source-data` | CloudEvents envelope and payload of 12.3 |
| checkDailyCompleteness | Activity | `rwb-source-data` | Business date and the products the day reads in; COMPLETE, or HOLD with product and source out |

`FreshnessQuery` and `DailyCompletenessGate` are also published as typed interfaces in the contract jar of RWB-P1-E1015-CON: `FreshnessQuery.stampFor`, `stampForRow` and `stampsFor`, and `DailyCompletenessGate.check`, with `FreshnessStamp` carrying productCode, businessDate, sourceExtractedAt, loadedAt, status and staleSince.

#### 12.6 Schedules

| Schedule | Cadence | Policy | Legacy reference |
|---|---|---|---|
| The cut-off check of each source-fed data product (DP01, DP02, DP05, DP06, DP07, DP11, DP13), at `data_product.expected_by` in Asia/Bangkok | Daily 08:00, or MON 08:00 for the weekly product, as data rows | Overlap SKIP; catch-up window; one Schedule per product | The legacy Quartz trigger per product at `expected_by` |

The Schedule names and the per-product expected-by values beyond 08:00 and MON 08:00 are Not specified in the source documents (GAP-0494; ASM-0686); the story keeps one Schedule per product, driven by the data row.

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| data_product_load | rwb_source_data | P1 | Writes the stamp, the stale flag and the duplicate count |
| data_product | rwb_source_data | P1 | Reads refresh cycle and expected-by only |
| outbox_event, processed_event | rwb_source_data | PLT library (DP-09) | Writes the outbox row of each event; deduplicates the listener |
| decision_log_entry | rwb_decision | P7 | **Never read and never written** (DP-01); reached through `FreshnessQuery` and the P7 contract |
| v_ace_batch_status | recovery | ACE team | Read only, through the `rwb_source_data` login (DP-05) |

#### 12.8 Contract fakes

| Fake | Serves | Used for |
|---|---|---|
| rwb-decision decision-record contract mock (RWB-P7-E1027-CON) | The inputs snapshot of AC3 | The AC3 test from Day 1, without a running rwb-decision |
| rwb-case reference-data fake (RWB-P3-E1043-CON) | The product-to-source map and the two expected-by rows | Every stamping test, so no list of values is a constant (DP-07) |
| Workflow kit fake (RWB-PLT-E1071-CON) | Schedule registration and activity retry | The cut-off tests with a test clock (DP-10) |
| Event platform fake (RWB-PLT-TE006-CON) | The outbox, the inbox and the envelope | The two event assertions (DP-09) |
| gateway-bff composite route fake (RWB-PLT-N001-CON) | The route the data panel uses | The panel state test (DP-19) |
| Flyway sequence fake (RWB-PLT-E1044-CON) | The service's migration sequence | The index migration on the service's own sequence (DP-15) |

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 3 | None | Two freshness reads and one Airflow signal on `/api/recovery/source-data/v1`; one hop, 2 s (DP-11) |
| Kafka | 2 published | None | AceDataReady and AceDataLate on `rwb.source-data.events.v1`, with retry and `.dlt`, CloudEvents 1.0 (DP-09) |
| Temporal | 1 workflow, 5 activities, 7 Schedules | None | `rwb-source-data` in namespace `rwb-recovery` (DP-10) |
| File | None | None | No file is read or written; the batch status arrives as a view row |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata.freshness`, with the published types in `...sourcedata.freshness.api`. Base `/api/recovery/source-data/v1`, schema and login `rwb_source_data`, topic `rwb.source-data.events.v1`, queue `rwb-source-data`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is applied without a decision log of this service: the library and the shared topic are the route by which the entry that AC3 reads is written by rwb-decision, and this service only answers the query.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `AceIngestCheckWorkflow` | Workflow | One run per source system and business date; stamp mode and cut-off mode |
| `stampProducts`, `markStale` | Activities | Write the stamp, the stale flag and the outbox row in one transaction; count the repeat |
| `FreshnessStampService` | Service | The stamping rules of BR1 to BR6 and BR11 |
| `DailyCompletenessGateImpl` | Service | Implements `DailyCompletenessGate` over `v_ace_batch_status` and the map |
| `BatchStatusListener` | Listener | Takes a new or changed COMPLETED or FAILED row and starts the workflow |
| `DataProductLoadRepository` | Repository | Reads and writes `data_product_load` in `rwb_source_data`; no statement names another schema |
| `FreshnessController` | Controller | The three operations of 12.1 |
| `DataFreshnessPanel` | React component | Data panel on SCR-03 through the composite route (DP-19) |

**Database.** `data_product_load` exists from RWB-P1-E1001-APP with its unique key on `(product_code, business_date)`; the next free migration on the service sequence adds index `(product_code, loaded_at desc)`. No new table. The service reads `data_product` in its own schema and `recovery.v_ace_batch_status` through its login (DP-01, DP-05, DP-15).

**Configuration and reference data.** `data_product.refresh_cycle` and `expected_by`, the product-to-source map and the alert channel `rwb.dataengine.freshness.alert-channel` are data rows or properties, set by the platform administrator and the data steward (DP-07).

**Build steps**

1. The index migration on the service sequence, and `DataProductLoadRepository` with its unique key.
2. `FreshnessStampService.recordBatch(productCode, businessDate, startedAt, completedAt)` from `stampProducts`; a repeat adds to `duplicate_count` and publishes no second event.
3. `AceIngestCheckWorkflow` in cut-off mode, one Schedule per product built from `data_product`; STALE, `AceDataLate` and the alert.
4. The listener on a FAILED row, idempotent on the source, the business date and the status.
5. `DailyCompletenessGateImpl` over the map; unit test a late source the day does not read and a late source it does.
6. `FreshnessQuery` and `FreshnessController` with the two response shapes and the Airflow signal.
7. The panel state on SCR-03 with MSG-P1-001, against the composite route fake.
8. Tests for the owned criteria and the neighbouring ones with a fixed test clock, and the access test.

**Feature flag.** `rwb.dataengine.freshness-stamp`. The flag is on only after RWB-ACE-001 creates the batch table and the view exists (DL43); before that the panel shows no stamp rather than a guessed one.

**Done when.** The tests in section 16 pass, every daily data job calls `DailyCompletenessGate` before it starts, and P7 reads the stamps through the published interface.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | A product is stale, or the gate holds a job, shown in the case record data panel and the alert | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-001 | Malformed product code or date in the query | Enter {field}. |
| MSG-GEN-006 | The store or the view is unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-001 | No session on the read | Sign in to continue. |
| MSG-P4-002 | Role without Case record R | You cannot {action} here. Your role does not include it. |

Thai text for each message follows decision DL10. The texts are the legacy ones, character for character.

### 15. Screens and states

SCR-03 Case record, state Read only (Epic 1): the data panel shows each product's business date and load time, read through the gateway-bff composite route (DP-19). State Stale input: the panel shows MSG-P1-001 next to the stale product. State Loading: skeleton rows. The data steward sees stale products and the gate result on SCR-45 Data quality from Epic 2; in Epic 1 the same list comes from `GET /data-products/freshness` and the job listing. The composite route specification and the panel field list are Not specified in the source documents (GAP-0494; ASM-0686); this story fixes the service side only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-015-09 | Access | Component | RW-REFADM calls GET /data-products/freshness; refused with MSG-P4-002 |
| TC-E1-015-01 | AC1, BR1 | End to end | ALS batch row for 2026-11-30, started 23:30, completed 05:40; DP01 |
| TC-E1-015-02 | AC2, BR2 | End to end | No COMPLETED ALS row at 08:00; test clock |
| TC-E1-015-03 | AC3, BR5 | End to end | Decision for RW-2026-000101 reading DP01 and DP06 |
| TC-E1-015-04 | AC4, BR3 | End to end | ALS batch row FAILED at 05:20 |
| TC-E1-015-05 | AC5, BR6 | End to end | Same COMPLETED row read twice |
| TC-E1-015-06 | AC6 | End to end | Late ALS batch at 08:40 after the stale flag |
| TC-E1-015-07 | AC7 | End to end | ALS batch at 07:59 |
| TC-E1-015-08 | AC8, BR7 | End to end | Weekly DP06 batch on Monday; check on Thursday |
| TC-E1-015-10 | AC9, BR8 | End to end | EFS batch FAILED at the 08:00 cut-off; case list step stub |
| TC-E1-015-11 | AC10, BR8 | End to end | Every source COMPLETED for 2026-11-30 |
| TC-E1-015-12 | AC11, BR4 | End to end | CCMS COMPLETED 2026-11-27; SVAF only to 2026-11-20 |

This story owns legacy AC3 and AC8, so TC-E1-015-03 and TC-E1-015-08 prove what it owns and the other ten rows stand as the legacy cases of the key with their IDs, their Covers and their Data kept in legacy order and character for character. The criteria AC1, AC2, AC4 to AC7 and AC9 to AC11 sit with the other slices of RWB-E1-015 and are not in this story's gherkin. The legacy level "System" maps to "End to end" and "Access" to "Component". The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: expected-by times, refresh cycles, the product-to-source map and the alert channel are data rows or properties (DP-07).
- No personal data in logs, tests, events, workflow inputs or prompts; the stamp carries product codes, source codes and times only (DP-09).
- ACE data only through the owner's contract or the `recovery.v_ace_*` views: this story reads `v_ace_batch_status` and writes nothing to ACE (DP-05).
- No cross-schema read and no cross-schema key: every statement names `rwb_source_data` only, and P7 reaches the stamps through `FreshnessQuery` (DP-01, DP-11).
- The stale check never deletes or changes a loaded row; the previous complete business date stays in use.
- One hop and a 2 s timeout on every call to another service; this story makes none at run time.
- Every Schedule is data-driven per product and never a constant cadence in code (DP-10).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-009 | Every data product carries a freshness stamp from the ACE batch record; every decision records the freshness of the data it used | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-14, FEAT-DRI-12 | All recovery processes; 17 Run the decision center | R-UNI-40; BR-P1-014-2 to BR-P1-014-4 | TC-E1-015-03, TC-E1-015-08, and the ten legacy rows of section 16 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1015-CON | Contract | H: the baselined operations, interfaces, events, workflow and Schedule declaration |
| RWB-P1-E1001-APP | App development | H: `data_product_load`, `data_product` and the dictionary in `rwb_source_data` |
| RWB-P1-E1069-APP | App development | H: the read-only ACE views, among them `v_ace_batch_status` |
| RWB-PLT-E1071-CON | Contract | H: the workflow kit and Schedule registration (DP-10) |
| RWB-PLT-TE006-CON | Contract | H: the outbox, the inbox and the CloudEvents envelope (DP-09) |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library the entry of AC3 is written through (DP-03) |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | Contract | H and C: the reference-data contract carrying the product-to-source map (DP-07) |
| RWB-PLT-E1044-CON | Contract | H: the per-service Flyway sequence (DP-15) |
| RWB-PLT-N001-CON | Contract | H: the composite route the data panel uses (DP-19) |
| RWB-P7-E1027-CON | Contract | C: rwb-decision calls `FreshnessQuery` and writes the inputs snapshot (DP-03, DP-11) |
| RWB-P1-E1015-OPS | DevOps | X: deployment, the listener and KEDA, the topic, the Schedules, the alerts and the runbook |
| RWB-P1-E1011-APP | App development | Neighbour: its reconciliation workflow calls `checkDailyCompleteness` before the case list step |

### 19. Out of scope

- The MSG-P7-006 warning on a decision screen when an input is past its age limit (decision screens, Epic 2).
- Same-day data for named triggers (DL06).
- The data quality console SCR-45 (Epic 2) and the reconciliation report (RWB-P1-E1011-APP).
- Freshness of the stage 2 data products (RWB-E2-010, RWB-P1-E2010-APP).
- ACE's own ingestion monitoring and its alerting (RWB-ACE-001).
- The deployment, the chart, the topic provisioning, the Schedule registration, the dashboards and the runbook (RWB-P1-E1015-OPS).
- The contract documents and the fakes as published artefacts (RWB-P1-E1015-CON); this story only consumes them.
- The inputs snapshot itself and the decision log table (P7; RWB-P7-E1027-CON).
