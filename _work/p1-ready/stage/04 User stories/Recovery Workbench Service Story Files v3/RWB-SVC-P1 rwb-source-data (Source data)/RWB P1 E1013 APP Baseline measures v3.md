# RWB-P1-E1013-APP Baseline measures

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1013-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP07, DP10, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | L-P1-H |
| Ready to start | After the P1 baseline and ACE view dependencies, platform kit and E1015 contracts are available. Validate the chain with E1011 and E1018. |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-P1-E1013-APP-14) |
| Size | Not specified in the source documents (DOR-RWB-P1-E1013-APP-16) |
| Depends on (build) | RWB-P1-E1001-APP, RWB-P1-E1069-APP, RWB-P1-E1069-DB, RWB-P1-E1015-APP, RWB-P1-E1011-APP, RWB-P1-E1018-APP, RWB-PLT-E1027-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-TE006-CON |
| Contract dependencies | RWB-P1-E1015-CON, RWB-P9-E1013-CON |
| Contract version | API Specification v7 `rwb-source-data.yaml` 5.1.0 (RD-P1-005); readiness fake 5.1.0; Temporal contract jar major 1 |
| Open decisions | DL25 option A in E1011 (ASM-5702). DL43 option A as planning basis, real Section B release pending ACE team lead (ASM-5703, RWB-ACE-001). |
| Integration dependencies | None |
| External dependencies | RWB-P1-E1015-OPS owns the 05:30 Schedule, ingest worker and event topic infrastructure (RD-P1-022) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-032) |
| Readiness decisions | RD-P1-001, RD-P1-002, RD-P1-003, RD-P1-004, RD-P1-005, RD-P1-006, RD-P1-008, RD-P1-010, RD-P1-011, RD-P1-012, RD-P1-020, RD-P1-021, RD-P1-022, RD-P1-024, RD-P1-025, RD-P1-040, RD-P1-041, RD-P1-042, RD-P1-043, RD-P1-061, RD-P1-065 |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: P1 slice of RWB-E1-013 for rwb-source-data, split from the P9, P3 and integration slices. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1013-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (28 resolved, 38 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Version 3 changes**

- RD-P1-010/022/024 retain E1013 readiness, payments and snapshot and the E1015, E1011 and E1018 ownership boundaries (RWB-P1-E1013-APP#1–#3, #9, #12, #21–#23, #29).
- RD-P1-003/020/021/040/041/043 align readiness storage, source grain, late cutoffs and E1015 handoffs (RWB-P1-E1013-APP#4–#7, #10–#16, #25, #27).
- RD-P1-001/004/005/006/011/012 pin the contracts and align authentication, Problem mapping, idempotency, fixtures and delivery dependencies (RWB-P1-E1013-APP#8, #17–#20, #24, #26, #28).
- Finishing pass (RD-P1-061, RD-P1-065; requests S3-stories-0149, W3-messages-0037; test case backfill): `GET /payments` is one operation with the `businessDate` or `accountKey` form, a repeated ready call after DONE or LATE starts nothing, and Test Cases v9 IDs are cited.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: applied RD-P1-001, RD-P1-002, RD-P1-003, RD-P1-004, RD-P1-005, RD-P1-006, RD-P1-008, RD-P1-010, RD-P1-011, RD-P1-012, RD-P1-020, RD-P1-021, RD-P1-022, RD-P1-024, RD-P1-025, RD-P1-040, RD-P1-041, RD-P1-042, RD-P1-043.

### 1. Story

As a **data steward (RW-DATASTEW)**, I want **a durable readiness signal and status for each business date and authorised payment and snapshot facts for reporting**, so that **Airflow can track ingest and reporting can use dated source facts**.

### 2. Business rationale

This is the rwb-source-data slice of RWB-E1-013 (REQ-RDF-012, NFR-065, FSD P1 A2.19). E1013 owns readiness call and status, payment facts through `v_ace_payment` and `snapshot(page)`. P9 owns measure definitions, calculation, snapshots and publication. E1015 owns ingest, stamps, events and the completeness gate. E1011 owns JOB-04. E1018 owns `listEligibleAccounts`.

The readiness pair and payments use the P1 base `/api/recovery/source-data/v1`. E1015-CON publishes the readiness pair in the shared contract. E1013 builds both handlers and initiates E1015’s workflow.

DP-17 withdraws the legacy lake and Power BI assertions (GAP-0558, ASM-0799). P3 supplies dated case facts. P9 owns publication decisions. RWB-ITG-E1013-ITG proves the cross-service baseline flows (GAP-0560, ASM-0801).

This story uses the owner's schema (DP-01), the local decision record (DP-03), ACE views only for its own payments read (DP-05), reference data as data (DP-07), one hop with a 2 s budget (DP-11), the per-service REST base (DP-13), the per-service Flyway sequence (DP-15), no data lake (DP-17) and the gateway-bff route (DP-19). Workflow, event and freshness ownership stays with E1015 and E1011 as ruled by RD-P1-022.

### 3. Preconditions

- The RWB-P1-E1001-APP baseline is applied. RD-P1-025 fixes the baseline at 123 dictionary objects and 1,379 fields, with retired rows marked retired.
- RWB-P1-E1069-APP and RWB-P1-E1069-DB are done: the 30 `recovery.v_ace_*` views compile in DEV and SIT, the rwb-source-data login holds SELECT on them and nothing in `public`, and `v_ace_payment` returns `payment_date` and `payment_amount` (DF-ACE-045, DF-ACE-046).
- RWB-P1-E1015-APP owns the read of `v_ace_batch_status`, the freshness stamps and completeness gate; this story consumes the resulting readiness status (RD-P1-022). The view dependency and RWB-ACE-001 remain with E1015.
- The platform workflow kit, idempotency and decision-record libraries and Flyway baseline are available. E1013 uses LOV-READINESS from RD-P1-020. LOV-FRESHNESS and the product-source map are inputs to E1015.
- Use the RWB-P9-E1013-CON consumer contract for payments. The P1 snapshot activity contract alignment awaits GAP-3425.
- This slice supplies only the readiness record and call, the payments read and `snapshot(page)`. RWB-P1-E1018-APP supplies `listEligibleAccounts`; E1015 supplies freshness and the gate; E1011 supplies reconciliation. It produces no measure code, definition version, baseline date value or total; every measure figure stays with RWB-P9-E1013-APP (RD-P1-010, RD-P1-022).
- The bank's Airflow DAG of the ACE ingestion chain is in place and its last task can call `POST /api/recovery/source-data/v1/business-days/{date}/ready`, and a sensor polls `GET /api/recovery/source-data/v1/business-days/{date}/status` (Arch v5 slide 32). While ACE ingestion is still on Control-M, the fallback poll of the ACE batch record stands in for the call (Arch v5 slide 31 notes).
- SIT has the `rwb-recovery` Temporal namespace and `rwb-source-data` task queue. Use synthetic data only.
- E1015 owns the 05:30 schedule and fallback poll. Build and test with the E1065 Section B fixtures; external deployment is gated on DL43 and RWB-ACE-001 (RD-P1-043).
- Build and contract dependencies are listed in the header.

### 4. Flow

1. Bank Airflow calls `POST /api/recovery/source-data/v1/business-days/{date}/ready` with its authorised workload identity and a canonical UUID key.
2. The first accepted POST writes one `business_day_readiness` row for the date in RUNNING with `received_at`, `changed_at` and the UUID header, then requests E1015’s `AceIngestCheck` start with `{businessDate, startedBy: AIRFLOW}`. Use `ace-ingest-check-{businessDate}`, USE_EXISTING and ALLOW_DUPLICATE. A different canonical UUID for the same date does not create a second readiness row or modify its first key; its workflow request attaches to an open run (USE_EXISTING), and once the row is DONE or LATE a repeat answers 202 with the stored state and starts nothing, so no second `ReconciliationWorkflow` run of a date exists except through the rerun of a FAILED run (RD-P1-065). Keep readiness state timestamp changes tied to state transitions.
3. An authorised `GET /business-days/{date}/status` reads the durable state and last change time. DONE follows the ALS stamp, independently of the reconciliation and other source stamps. LATE follows the E1015 AceDataLate signal while ALS is incomplete.
4. E1015 uses durable five-minute status polls for the due source set and owns the 05:30 Asia/Bangkok Schedule and DEV-only Control-M fallback until GAP-3277 closes. The expected date is the latest prior bank business date from DP14 (RD-P1-041). Weekly products follow their cycle day.
5. E1015 stamps a product only once its entire mapped source set is COMPLETED for that date. DP01 maps to ALS, DP13 to ALS and GL under RD-P1-021 (ASM-5695), and DP03 is Workbench-only. Freshness timestamps and notices are in section 12.5.
6. Authorised consumers use the payment and snapshot contracts in sections 12.1 and 12.5.

### 5. Exception paths

| ID | Trigger | Outcome | Covered by |
|---|---|---|---|
| X1 | Same ready request and key within 24 h | Replay the original 202 and body without another start | AC1 |
| X2 | Early Airflow call with ALS incomplete | 202 RUNNING; E1015 continues its status polls | AC12 |
| X3 | ALS still incomplete at 05:30 Asia/Bangkok, or FAILED earlier | E1015 owns AceDataLate and its alert; status becomes LATE | AC4, AC13 |
| X4 | Readiness store or Temporal starter is unavailable | Shared Problem 503 MSG-GEN-006, or MSG-PLT-N009-06 for the idempotency store. E1015 owns ACE batch read failures | AC15, AC24 |
| X5 | Payment query exceeds 2 s | 503 MSG-GEN-006 and no cached success | AC19 |
| X6 | ACE outbox relay cannot reach the broker | E1015 retains the committed outbox row for retry | AC18 |
| X7 | Code references a retired lake endpoint | Architecture test fails | AC7 |
| X8 | ALS is stamped while JOB-04 is still running | Readiness answers DONE | AC2 |
| X9 | Malformed date, refused caller or key conflict | Problem mapping of section 12.1 | AC10, AC17, AC22 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Depends on the P1 baseline, E1015 and ACE views and on the consumer contracts in the header |
| Negotiable | The payment and snapshot details need provider and consumer agreement |
| Valuable | Readiness status and dated payment/snapshot facts are available to the measure consumer; P9 computes the baseline |
| Estimable | Readiness record, three operations, payment query, snapshot activity and one table migration |
| Small | Pending squad sizing |
| Testable | Section 7 is tested with synthetic readiness, payment and snapshot data |

### 7. Acceptance criteria

```gherkin
Feature: Readiness status and baseline source facts

  Scenario: AC1 First readiness call and replay
    Given an authorised Airflow caller and no readiness row for 2026-11-27
    When it posts the readiness signal and repeats it with the same canonical UUID key within 24 h
    Then both responses are the same 202 BusinessDayStatus with businessDate 2026-11-27, status RUNNING and the original changedAt
    And one readiness row retains the first UUID and one ace-ingest-check-2026-11-27 starts with input businessDate 2026-11-27 and startedBy AIRFLOW

  Scenario: AC2 ALS stamp controls DONE
    Given readiness for 2026-11-27 is RUNNING and E1011 has yet to finish reconciliation
    When E1015 commits the ALS stamp and Airflow reads the date status
    Then the status operation returns 200 with status DONE, the same businessDate and changedAt of the ALS-stamp transition

  Scenario: AC3 Multi-source status boundary
    Given ALS is COMPLETED and GL is incomplete for 2026-11-27
    When the E1015-owned ingest workflow updates its status and freshness
    Then E1013 reports DONE for the stamped ALS date and E1015 keeps DP13 unstamped for that date and its gate on HOLD
    And the DP01 stamp can be LOADED and DP03 does not require an ACE batch

  Scenario: AC4 Late source projection
    Given the expected bank business date has no ALS row at 05:30 Asia/Bangkok
    When the E1015 Schedule evaluates that date
    Then E1015 emits one AceDataLate with completedAt null for ALS and the date status becomes LATE
    And the per-product expected_by transition does not emit a second AceDataLate
    And the missing-row status literal awaits GAP-3430

  Scenario: AC5 Authorised payment data
    Given v_ace_payment holds synthetic PAY-0001 for account ACC0000017 with dated facts and rwb-access grants Case record R within scope
    When the caller requests GET /payments?accountKey=ACC0000017
    Then the response projection is limited to payment_code, account_key, payment_date, payment_amount and data_as_of from the view and applies the masking decision
    And the answer is the PaymentsAnswer shape with businessDate of the DP01 stamp in use and rows ordered by paymentDate then paymentCode, and it answers 409 MSG-P1-001 while the gate refuses
    And a call with both businessDate and accountKey, or with neither, answers 400 MSG-GEN-001 with `field`
    And the masked representation awaits GAP-3427

  Scenario: AC6 Repeat the same dated snapshot page
    Given snapshot(page) is registered on rwb-source-data with a two-page fixture for 2026-11-27
    When the consumer reads both pages and repeats the first cursor
    Then each row is dated 2026-11-27, the two pages do not overlap and the repeated first cursor returns the same rows and order
    And the dated contract and fixture schema await GAP-3425

  Scenario: AC7 Lake endpoint architecture check
    Given a test fixture names the retired INT-19 lake endpoint
    When LakeFreeRule runs
    Then the build fails and reports the offending component

  Scenario: AC9 Ownership boundary for writes and registration
    Given an E1013 readiness call and its payment and snapshot components
    When the schema writes and Temporal registrations are inspected
    Then this slice writes business_day_readiness as its business state and starts the E1015 workflow through its contract
    And it owns neither stamps, source events, reconciliation, gate logic nor listEligibleAccounts

  Scenario: AC10 Authentication and authorization by operation
    Given otherwise accepted ready, status and payment inputs with a missing token or a caller without the applicable right and scope
    When each operation is called
    Then the corresponding response is a 401 MSG-P4-001 or 403 MSG-P4-002 Problem and no business state is written or returned

  Scenario: AC12 ALS completes after the readiness call
    Given a ready call for 2026-11-27 returned 202 RUNNING before ALS completed
    When ALS becomes COMPLETED and the next E1015 durable poll detects and stamps it
    Then the status changes to DONE with changedAt of that transition and no new readiness row is made
    And a further ready call for that date with a new UUID key answers 202 with status DONE and the same changedAt, starts no workflow and causes no second reconciliation run

  Scenario: AC13 Failed ALS belongs to the ingest owner
    Given E1015 reads a FAILED ALS row before the 05:30 Schedule
    When the parent handles the failure
    Then E1015 emits AceDataLate once, marks the stamp in use STALE and keeps the gate on HOLD
    And E1013 reports LATE for the date unless it already reached DONE

  Scenario: AC14 DP13 late source does not block readiness
    Given the current date has ALS COMPLETED, GL incomplete and a prior DP13 stamp
    When E1015 projects readiness and the DP13 gate
    Then status returns DONE for the ALS-stamped date and DP13 gate returns HOLD with no new DP13 stamp

  Scenario: AC15 E1015 batch status view outage boundary
    Given E1015 cannot read v_ace_batch_status after the readiness call has been accepted
    When the owning workflow handles the failure
    Then E1013 does not infer DONE or write any freshness row and the E1015 failure paths are exercised in E1015-APP

  Scenario: AC16 Concurrent calls with different keys
    Given two first requests for the same date have distinct canonical UUID keys
    When they overlap and the date execution remains open
    Then one business_day_readiness row holds the winning first key and USE_EXISTING leaves one open ingest workflow

  Scenario: AC17 Bad date and key validation
    Given a ready request has an invalid date, a missing key or a non-UUID key
    When the request is validated
    Then the invalid date yields 400 MSG-GEN-001 or the invalid key yields 400 MSG-PLT-N009-03
    And no readiness row or workflow is created

  Scenario: AC18 Outbox ownership during broker outage
    Given the E1015 ALS stamp and source event commit while the broker is unavailable
    When the shared relay retries after the broker recovers
    Then E1015’s committed outbox entry is retained for delivery and E1013 creates no duplicate source event

  Scenario: AC19 Payment read exceeds budget
    Given the payment view query cannot finish within the 2 s caller budget
    When the authorised payment read is called
    Then it returns a 503 MSG-GEN-006 Problem and caches no successful result

  Scenario: AC20 Section B gate off
    Given E1015’s Section B flag is off
    When an authorised readiness request uses a new UUID key
    Then ready returns 202 and the status becomes LATE under RD-P1-043
    And E1015 writes no stamp or event and starts no downstream child

  Scenario: AC21 Decision record and replay minimisation
    Given a first ready call is accepted for 2026-11-27
    When the service records the acceptance through DP-03 and the same UUID request is replayed
    Then one decision record holds the business date and readiness outcome and carries no account, case or customer identifier
    And replay writes no second decision record

  Scenario: AC22 Key conflict and unavailable key store
    Given a key is in flight, is reused for a different resolved date path or the idempotency store is unavailable
    When ready is called
    Then the first two conditions return 409 MSG-PLT-N009-05 and the last returns 503 MSG-PLT-N009-06

  Scenario: AC23 Unknown readiness date
    Given an authorised caller requests a date that has no readiness row
    When it calls GET /business-days/{date}/status
    Then it receives a 404 MSG-P4-003 Problem

  Scenario: AC24 Readiness dependency outage
    Given the readiness repository is unavailable to an authorised status caller
    When that caller requests a syntactically accepted date
    Then status returns a 503 MSG-GEN-006 Problem

  Scenario: AC25 Repeat signal after a closed LATE run
    Given a prior ingest execution closed before the ALS batch arrived and status is LATE
    When Airflow retries with a new UUID key for the same date
    Then it answers 202 with status LATE and the unchanged changedAt, the same date row is retained and no new workflow execution starts
```

AC11 is withdrawn because there is no public readiness state mutation. AC8 and legacy baseline measure assertions belong to P9. The E1015 outcome scenarios here verify the readiness projection and owner boundary. E1015-APP owns the source and relay failure tests.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR8 | E1015 owns source completeness and per-product stamping. Readiness is DONE once ALS is stamped. | RD-P1-020/040/041 |
| BR9 | There is no data lake, no INT-19 extract and no Power BI feed: this story calls no lake endpoint and writes no extract file; E1015 owns source events consumed by reporting | DP-17; Arch v5 slides 8, 37 and 41; ADR-018 |
| BR10 | Every call is one hop to the owning service on its own base with a 2 s budget; no service is called through another service and a call outside the budget fails rather than being retried into a pass | DP-11; DP-13; ADR-020 |
| BR11 | E1015 owns ACE source events. E1013 consumes no source event and publishes no competing ACE event. DP-03 records use the platform library. | RD-P1-003/008/022/040 |
| BR12 | Errors from this story use the message IDs and texts of the published readiness/payment contract; freshness messages belong to E1015 | FSD P1 VR-P1-001-1; TSD P1 T3.7; this story |
| BR13 | P9 owns measure computation and its measure tables. E1013 supplies the P1 snapshot activity for source facts. | DP-01, RD-P1-022 |
| BR14 | Same-key replay and date deduplication are independent: RD-P1-001 governs the UUID response cache, RD-P1-040 governs workflow reuse and RD-P1-065 starts nothing once the row is DONE or LATE. | RD-P1-001/020/040/065 |

The legacy measure definition, age bands, rules and publication belong to RWB-P9-E1013-APP. E1015 and E1011 own the gate and reconciliation respectively.

### 9. State transitions

| From | Trigger | To |
|---|---|---|
| No row | First accepted readiness start for date | RUNNING |
| RUNNING | ALS stamp committed | DONE |
| RUNNING | AceDataLate is out while ALS remains incomplete, or the Section B flag-off outcome applies | LATE |
| LATE | ALS stamp committed on re-check or subsequent execution | DONE |
| Existing date | Same-key readiness replay | State and timestamps unchanged |

Store the transition in `business_day_readiness` with `changed_at`. LATE remains observable while an incomplete batch is rechecked. A repeat signal for a row that is DONE or LATE answers 202 with the stored state and starts nothing; a second reconciliation run of a date exists only through the rerun of a FAILED run (RD-P1-065). Pending: how a date whose ingest run failed or closed before the ALS batch arrived is recovered before the AD018 rerun (wave 4), owner solution architect, tracked as GAP-3390. A later freshness issue on a completed date is projected through E1015 freshness rather than a public mutation of the readiness row.

### 10. Authority

| Caller | Access |
|---|---|
| Airflow workload identity with client credentials | Ready requires Platform administration U; status requires Platform administration R. Use the approved readiness identity |
| Authorised payment client | Case record R and applicable scope, with the field-level masking answer |
| RWB-P1-E1013-APP service identity | Owns readiness writes, reads authorised payment facts and registers the snapshot activity |
| RW-PLATADM | Runs AD018’s operational rerun with Platform administration U after wave 4 |
| P9 measures consumer | Source facts only under the scoped contract and identity in sections 12.1 and 12.5 |

Apply rwb-access `POST /authorise` for capability and scope. Return 401 for missing identity and 403 for an identity without the required grant. User identity alone does not grant access to the Airflow readiness pair.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-043, DF-ACE-044, DF-ACE-045, DF-ACE-046, DF-ACE-054 | `v_ace_payment` (`recovery.v_ace_payment`) | payment_code, account_key, payment_date, payment_amount, data_as_of | Read |
| DF-OPS-252 to DF-OPS-257 | `business_day_readiness` (`rwb_source_data`) | id, business_date, state, received_at, changed_at, idempotency_key | Write; Read |
| DF-ACE-182, DF-ACE-186 | `v_ace_batch_status` | E1015 reads text `status` and derived boolean `is_complete` (`status = COMPLETED`), per ACE Source Views v1 | Owner boundary only |
| DF-OPS-001 to DF-OPS-009 | `data_product_load` (`rwb_source_data`) | freshness stamp fields | Owned and written by RWB-P1-E1015-APP; not read or written here |
| DF-OPS-118 to DF-OPS-129 | `reconciliation_result` (`rwb_source_data`) | reconciliation result fields | Owned and written by RWB-P1-E1011-APP; not read or written here |
| DF-RPT-032 to DF-RPT-052 | `measure_definition`, `measure_snapshot` (`rwb_reporting`) | measure definitions and snapshots | Not read or written: P9 tables |

The readiness record follows RD-P1-020 F. DF-OPS-252 `id` UUID (generated), 253 `business_date` date, 254 `state` varchar(10) initial RUNNING, 255 `received_at` and 256 `changed_at` timestamptz, 257 `idempotency_key` varchar(120) carrying the first UUID header, nullable for a start without an HTTP key. If polling or scheduling first creates the date row, record the UUID of the first subsequent accepted POST without duplicating the row or changing its `received_at`. Only one row per date via `uk_business_day_readiness UNIQUE (business_date)`. Unknown status date returns 404 MSG-P4-003.

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Success | Access |
|---|---|---|---|
| POST | `/business-days/{date}/ready` | 202 `BusinessDayStatus` | Readiness workload identity, Platform administration U |
| GET | `/business-days/{date}/status` | 200 `BusinessDayStatus` | Readiness workload identity, Platform administration R |
| GET | `/payments` with exactly one of `businessDate` or `accountKey` (operationId `getPayments`) | 200 `PaymentsAnswer` | Case record R, scope and masking for the `accountKey` form; the payment-matching run of rwb-payment for the `businessDate` form |

E1015-CON publishes the readiness pair in API Specification v7 `rwb-source-data.yaml` 5.1.0 (RD-P1-005). `BusinessDayStatus` is `{businessDate, status, changedAt}`. The `date` path parameter and `businessDate` are ISO dates, `status` is RUNNING/DONE/LATE, and `changedAt` is a date-time. E1015 also publishes and implements the separate freshness read via its owning stories.

RD-P1-001 requires canonical UUID Idempotency-Key on POST. Missing, blank or malformed key yields 400 MSG-PLT-N009-03. Same key, resolved endpoint and request digest replays the original status and body for 24 h, without another start. Different endpoint/digest or a request still in flight yields 409 MSG-PLT-N009-05. A bodyless POST uses SHA-256 of the empty string. An unavailable idempotency store yields 503 MSG-PLT-N009-06. Temporal’s workflow ID and the database unique date handle concurrency across different keys.

`GET /payments` is one operation with two query forms, built here and published in RWB-P1-E1015-CON (RD-P1-061). Exactly one of `businessDate` (date) or `accountKey` (string, at most 255) is given; both or neither answers 400 MSG-GEN-001 with `field`. The `accountKey` form answers the `v_ace_payment` rows of the account, ordered by `paymentDate` then `paymentCode`, as `PaymentsAnswer` with `businessDate` = the DP01 stamp in use. The `businessDate` form answers one row per `paymentCode` ordered by `paymentCode`; its rules are the acceptance criteria of RWB-P1-E2008-APP, which depends on this story (H). Both forms answer 409 MSG-P1-001 when the gate refuses. Interim: both forms are unpaged. Pending: paging and row cap, owner data architect, tracked as GAP-0601 and GAP-3508; the answer for an unknown account and any "since entry" date rule, owner P1 contract owner with the P9 consumer, tracked as GAP-3426. Do not infer an entry date from the current view.

DF-ACE-043, DF-ACE-045, DF-ACE-046 and DF-ACE-054 are Confidential customer data, shown within authorised scope. DF-ACE-044 is a Confidential indirect identifier, masked in UAT (Data Classification v5). Apply the rwb-access masking decision before serialisation. Pending: concrete mask/omit rule and P9 service identity and scope, owner access contract owner with the P9 service owner, tracked as GAP-3427.

Pending: admissible future business dates and their refusal/acceptance behavior, owner P1 contract owner with bank platform, tracked as GAP-3428.

A malformed date, or a payments query with both or neither of `businessDate` and `accountKey`, gives 400 MSG-GEN-001, a refused payments gate 409 MSG-P1-001, absent identity 401 MSG-P4-001, denied right or scope 403 MSG-P4-002, unknown readiness date 404 MSG-P4-003 and unavailable system of record 503 MSG-GEN-006. Error responses use `application/problem+json` (RD-P1-004). Required members are `type`, `title`, `status`, `messageCode` and `traceId` (W3C 32-hex). Optional members are `detail`, `instance`, `messageTh`, `field` and `errors`. The `errors` array contains `{field, messageCode, detail}` entries only for 400 or 422 with multiple failing inputs. GET carries neither Idempotency-Key nor If-Match (RD-P1-001/006).

#### 12.2 REST operations consumed

No consumed business REST read is needed for readiness or payments. Use the platform authorise contract for rights, scope and masking. Start E1015 through Temporal. P9 is a consumer, and E1013 does not call P9 at runtime.

#### 12.3 Events published

E1015 publishes `rwb.source-data.AceDataReady.v1` and `rwb.source-data.AceDataLate.v1` on `rwb.source-data.events.v1`, once per source and business date for each type, with key `{sourceSystem}:{businessDate}`. The stamp transaction writes the outbox, with sourceSystem, businessDate, status and nullable completedAt. Pending: AceDataLate status literal when no batch row exists, owner E1015 event contract owner, tracked as GAP-3430. Only the DP-03 library emits a decision record for this slice, `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` (RD-P1-003/008).

#### 12.4 Events consumed

None. E1013 starts E1015 through the shared Temporal contract. The E1015 workflow uses durable reads and consumes no P1 source topic event (RD-P1-040).

#### 12.5 Workflows and activities

The first accepted POST writes one `business_day_readiness` row for the date in RUNNING with `received_at`, `changed_at` and the UUID header, then requests E1015’s `AceIngestCheck` start with `{businessDate, startedBy: AIRFLOW}`. Use `ace-ingest-check-{businessDate}`, USE_EXISTING and ALLOW_DUPLICATE. A different canonical UUID for the same date does not create a second readiness row or modify its first key; its workflow request attaches to an open run (USE_EXISTING), and once the row is DONE or LATE a repeat answers 202 with the stored state and starts nothing, so no second `ReconciliationWorkflow` run of a date exists except through the rerun of a FAILED run (RD-P1-065). Keep readiness state timestamp changes tied to state transitions.

Pending: `snapshot(page)` dated field set and sources, stable sort/tie-break, cursor, page size, historical repeatability and typed errors, owner P1 contract owner with the P9 measures owner, tracked as GAP-0563 and GAP-3425. Architecture v5 keeps the activity on `rwb-source-data`. RWB-P9-E1013-CON v2 names it but declares no remote invocation or schema. E1018 owns `listEligibleAccounts` under RD-P1-010.

E1015 owns the due-source gate and the multi-source product stamp on `(product_code, business_date)`, with `source_system` identifying the completing source, `source_extracted_at` from the latest source completion and `loaded_at` from the write instant (RD-P1-005/041). The 05:30 late event and alarm (or immediate FAILED notice) are separate from the `expected_by` stale transition (08:00 daily and Monday 08:00 for DP06). E1015 owns the stale banner and the never-stamped STALE/null-date answer. E1011 runs JOB-04 after the ALS stamp and the rwb-case allocation wait under RD-P1-024/040. E1013 readiness does not await JOB-04.

#### 12.6 Schedules

None. Bank Airflow calls the readiness operation. The 05:30 late check and fallback poll are owned by RWB-P1-E1015-APP/OPS; E1013 registers no Schedule or Quartz job (RD-P1-022).

#### 12.7 Tables owned

| Table | Schema | Owner | Use in this story |
|---|---|---|---|
| `business_day_readiness` | `rwb_source_data` | P1 | One readiness status row per business date, written and read here (RD-P1-020) |
| `idempotency_key` | `rwb_source_data` | PLT library | Idempotency record for the readiness call |
| `data_product_load` | `rwb_source_data` | P1 | Owned by RWB-P1-E1015-APP; not written or read here |
| `reconciliation_result` | `rwb_source_data` | RWB-P1-E1011-APP | Reconciliation owned by E1011 |

No other service table is read and no foreign key crosses a schema (DP-01). E1015 owns freshness; E1011 owns reconciliation (RD-P1-022).

#### 12.8 Contract fakes

| Provider | Fixtures |
|---|---|
| RWB-P1-E1015-CON | API and provider fake 5.1.0; ready 202 and identical replay, bad key, conflict, idempotency-store outage; status RUNNING, DONE, LATE, unknown date and shared errors |
| Airflow trigger stub | Canonical UUID requests, polling, same-key replay and concurrent distinct keys |
| Payment view and auth fixture | PAY-0001 and ACC0000017, allowed and masked decisions, timeout and known-empty case when published |
| Contract jar major 1 | E1015 ingest starter contract fixture; snapshot page/repeat/error fixture pending GAP-3425 |

The payment provider fixture holds the `PaymentsAnswer` shape (RD-P1-061); its masked values wait on GAP-3427. E1015 owns and verifies ALS, GL, multi-source, late and Section B ingest fixtures. Fakes are for DEV/SIT verification.

#### 12.9 Call-type summary

| Call type | Contract |
|---|---|
| REST | Readiness/status, payments; shared authorise |
| Kafka | E1015 source events; E1013 uses DP-03 only |
| Temporal | Start E1015 through its type; host `snapshot(page)` on `rwb-source-data` |
| File | None |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata`, modules `readiness`, `payment` and `snapshot`, in the service root of rwb-source-data.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `ReadinessController` | Controller | Validates the date, writes `business_day_readiness`, answers 202 and starts E1015 `AceIngestCheck` |
| `ReadinessStatusQuery` | Service | Reads RUNNING, DONE or LATE from `business_day_readiness` |
| `PaymentFactsQuery` | Service | Reads `v_ace_payment` by `account_key` or by business date (the two forms of `GET /payments`) and applies the authorization masking answer |
| `SnapshotActivity` | Activity | `snapshot(page)`: one stable page of dated facts for the measures consumer |
| `LakeFreeRule` | ArchUnit rule in test source | Fails the build on a class that names a lake endpoint, INT-19 or a lake container (DP-17) |

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

DP-01 and DP-15 apply to the readiness table. DP-03 handles decision evidence. DP-05 applies to the payment view. DP-11 and DP-13 protect the one-hop API. DP-17 withdraws lake delivery. E1015 keeps ingest, freshness and source events, E1011 keeps reconciliation, and E1018 keeps eligibility.

**Database and migrations.** One E1013-owned migration in the per-service Flyway sequence creates `business_day_readiness` with fields DF-OPS-252 to DF-OPS-257 and `uk_business_day_readiness UNIQUE (business_date)` (RD-P1-020). The E1013 story does not create an index on `reconciliation_result`; that object and its index are owned by RWB-P1-E1011-APP (RD-P1-022).

**Configuration and reference data**

- The business date and account ID are request inputs; masking is determined by the authorization response.
- Product-to-source mapping, `expected_by`, the 05:30 cut-off, freshness policy and retry settings belong to RWB-P1-E1015-APP/OPS.
- `recon.tolerance.pct` belongs to RWB-P1-E1011-APP.
- The E1015 Section B release and fallback flags follow RD-P1-040/043. `rwb.source-data.daily-gate` is scoped to E1011 under RD-P1-022.
- The login is the rwb-source-data login (DP-02), holding SELECT on views and its schema only.

**Build steps**

1. Create `business_day_readiness` and apply the unique date constraint using the E1013 Flyway migration.
2. Integrate the platform idempotency helper and E1015 starter. Verify replay, competing keys, closed-run recheck and Problem mappings.
3. Expose status with unchanged `changedAt` on replay and DONE at the ALS stamp.
4. Verify the payment query, masking, caller budget and snapshot activity after their contract gaps close.
5. Exercise the ownership and no-lake boundary checks in section 7.

**Done when.** The pinned readiness pair and consumer fixtures pass, the readiness state is durable, and the payments and Temporal contracts have been settled and verified against section 7.

### 14. Validation and messages

| Message code | Trigger |
|---|---|
| MSG-GEN-001 | 400 invalid date syntax, missing required request input, or both or neither of the two payments query parameters |
| MSG-P1-001 | 409 the payments read while the gate refuses |
| MSG-P4-001 | 401 missing credentials |
| MSG-P4-002 | 403 missing capability grant or scope. “You cannot {action} here. Your role does not include it.” (Error and Message Standard v6) |
| MSG-P4-003 | 404 unknown readiness date |
| MSG-PLT-N009-03 / MSG-PLT-N009-05 / MSG-PLT-N009-06 | 400 invalid UUID key, 409 in-flight/conflicting key, 503 idempotency store unavailable |
| MSG-GEN-006 | 503 unavailable readiness dependency or payment view |

E1015 owns the 05:30 Load late alert and gateway-bff banner through the freshness read. MSG-P1-001 uses the Error and Message Standard v6 wording “{product} is from {date}. Today's load has not arrived.” E1011 owns the reconciliation alert. AD018 owns the failed-run rerun and its messages from wave 4.

### 15. Screens and states

The platform edge and screen owners serve SCR-44 Interface and job monitor through gateway-bff. AD018 supplies job and rerun data from wave 4. E1015 supplies freshness and banner state. Authorised Airflow polls the readiness pair independently. Pending: SCR-44 loading, empty, error and no-access states, owner screen product owner, tracked as CG-ALL-2101. SCR-37 belongs to RWB-E2-009.

### 16. Test cases

| TC reference | Covers | Data |
|---|---|---|
| TC-P1-E1013-APP-15, TC-P1-E1013-APP-16, TC-P1-E1013-APP-01, TC-P1-E1013-APP-05, TC-P1-E1013-APP-06, TC-P1-E1013-APP-11 to TC-P1-E1013-APP-14 | AC1, AC2, AC12, AC16, AC17, AC22, AC23, AC24, AC25 | Canonical UUID, first write, replay, competing UUIDs, unknown date, late completion, key conflict and store outage |
| TC-P1-E1013-APP-17, TC-P1-E1013-APP-18, TC-P1-E1013-APP-02 to TC-P1-E1013-APP-04, TC-P1-E1013-APP-07, TC-P1-E1013-APP-09 | AC3, AC4, AC13, AC14, AC15, AC18, AC20 | E1015 contract fixtures for ALS, GL, DP01 and DP13, late, failed, unavailable view, relay recovery and Section B off |
| TC-P1-E1013-APP-19, TC-E1-013-21, TC-P1-E1013-APP-08 | AC5, AC10, AC19 | PAY-0001 and ACC0000017, scoped client, absent or refused credential, masking decision and payment outage |
| TC-P1-E1013-APP-20, TC-P1-E1013-APP-21, TC-E1-013-20, TC-P1-E1013-APP-10 | AC6, AC7, AC9, AC21 | Snapshot pages, no-lake rule, ownership and decision-record replay minimisation |
| Access | TC-P1-E1013-APP-22 | Applicable right and scope per operation |
| Contract of section 12.1; tables of section 12.7 | TC-P1-E1013-APP-23, TC-P1-E1013-APP-24 | Contract and ownership |
| BR6, BR8 to BR14 | TC-P1-E1013-APP-25 to TC-P1-E1013-APP-30, TC-E1-013-18, TC-P1-E1013-APP-31 | Business rules |

In Test Cases v9, TC-E1-013-08 stays with RWB-P9-E1013 and TC-E1-013-22 is retired. Cross-service proofs belong to RWB-ITG-E1013-ITG.

### 17. Guardrails

- No business value in code: the product codes, the product-to-source map, the expected-by time, the 05:30 cut-off, the tolerance and the message text are data rows or configuration, read with the version in force. No date, amount, percentage or threshold appears in Java.
- Apply payment data classification and authorised field masking before returning data. Keep personal identifiers out of readiness, workflow history and decision records.
- ACE data is read only through the views owned by rwb-source-data; this story reads only `v_ace_payment` for its payment operation (DP-01, DP-05, DP-02).
- **DP-17: no data lake and no lake call.** There is no INT-19 extract, no extract file, no freshness-stamped file, no trailer count, no lake container, no Power BI data set and no lake client in this service; `LakeFreeRule` fails the build on a class that names one, and the test suite fails if a lake assertion is added back.
- One hop and a 2 s budget on every call and on every activity invocation; a timeout fails the test rather than being retried into a pass (DP-11).
- A same-key replay returns the stored response without a new start or readiness write. A different key uses the date uniqueness constraint and the Temporal policy in section 12.1.
- E1015 owns source event envelopes and outbox retry. E1013 neither emits nor consumes those source events.
- No measure table is read or written, and no measure value is computed here: `measure_definition` and `measure_snapshot` are P9's (BR13).
- One migration per story in the service's own Flyway sequence, a repeated run with no effect, and no applied version edited in place (DP-15).
- Synthetic data only in the tests: the ACE batch fixture rows and the payment rows of the fixture account, never a production row.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-012 | Baseline measures for cases by route, age and queue, realized recovery, time in stage and turnaround per route are published, with definitions agreed by the Tribe, from a complete and reconciled ACE business date | Business Requirements Epic 1, sections 3.8 and 4 | FEAT-RDF-19, FEAT-RPT-01 | 15 Manage performance, data and AI | RWB-E1-013 BR1 to BR7; CTL-02; BR-P1-014-2 and BR-P1-014-4; DP-17 | TC-P1-E1013-APP-15 to TC-P1-E1013-APP-21, TC-E1-013-20, TC-E1-013-21, TC-P1-E1013-APP-01 to TC-P1-E1013-APP-14 |

| Element | Owner | What it carries of the legacy key |
|---|---|---|
| RWB-P9-E1013-APP | P9 rwb-reporting | The definition load, `measure_definition` and `measure_snapshot`, the baseline and frozen flags, the measures Schedule, the publication and the measures read |
| RWB-P3-E1013-APP | P3 rwb-case | The case facts the baseline is counted from: route, stage, queue, entry date and stage clock start of the date |
| RWB-ITG-E1013-ITG | Integration, wave 1 | The cross-service proof of the operations this story provides on the real services in SIT |
| RWB-P1-E1069-APP | P1 rwb-source-data | The views, grant and read contract used by this story for payment facts |
| RWB-P1-E1001-APP | P1 rwb-source-data | Shared data dictionary baseline, RD-P1-025 |
| RWB-P1-E1013-APP | P1 rwb-source-data | Builds and writes the dedicated readiness table |
| RWB-P1-E1015-CON | P1 rwb-source-data | Publishes readiness pair and `getPayments` in the shared 5.1.0 contract |
| RWB-P1-E2008-APP | P1 rwb-source-data | Holds the criteria of the `businessDate` form of `GET /payments` and depends on this story (H) |

The requirement, the two features and CTL-02 keep their legacy IDs. DP-17 removes the INT-19 extract and Power BI feed. Reporting consumes source events owned by E1015 and facts from `snapshot(page)` (GAP-0558; GAP-0559; ASM-0799; ASM-0800). Cross-service tests belong to RWB-ITG-E1013-ITG.

### 19. Out of scope

- The measure definition load, baseline flag, frozen flag, 01:30 measures Schedule and publication: RWB-P9-E1013-APP. This story supplies `snapshot(page)`.
- The case facts of the baseline and case creation of JOB-02: RWB-P3-E1013-APP and RWB-P3-E1018-APP.
- The cross-service proof of readiness, payments and snapshot and every `-ITG` copy of a test case: RWB-ITG-E1013-ITG.
- The view definitions, the grant, the per-service login and the boundary rule: RWB-P1-E1069-APP and RWB-P1-E1069-DB.
- The P1 base tables and catalog loads are owned by their respective stories. The case list is owned by rwb-case under RD-P1-024.
- The three read operations over customers, accounts and collateral of the same contract: RWB-P1-E1069-APP.
- SCR-44 Interface and job monitor, the case work surfaces and the banner rendering: the edge and screen stories of the platform and the case service; SCR-37 Steering dashboard is RWB-E2-009.
- E1015 owns ingest, stamps, source events, the gate and 05:30 Schedule. E1011 owns reconciliation. E1018 owns eligibility.
- **The data lake, INT-19, INT-20 and the Power BI feed, removed from the target architecture by DP-17**: no extract, no lake container, no data set and no lake assertion is built here or anywhere else in wave 1.
- The non-functional epic RWB-ITG-NFR and its performance, resilience and observability criteria.


### Remaining delivery steps

- Size: pending refinement; owner squad.
- Epic design sign-off: pending; owner product owner.
- Contract marked Done and published: pending; owner contract owner.
- Fake published: pending; owner contract owner.
- Test data loaded in DEV: pending; owner data engineer.
