# RWB-P1-E1013-APP Baseline measures

SCB Collections and Recovery. Henka Group, 22 November 2026.
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
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P9-E1013-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-032) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: P1 slice of RWB-E1-013 for rwb-source-data, split from the P9, P3 and integration slices. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As the **data steward and data product owner (RW-DATASTEW)**, with the **platform administrator (RW-PLATADM)** running the data jobs and the **Tribe lead (RW-TRIBE)** reading the freshness the baseline is computed from, I want **the readiness call for a business date answered once and idempotently, the daily completeness gate answered from the ACE batch record and the read-only views, the payments since entry answered one hop for an account, `AceDataReady` and `AceDataLate` published on `rwb.source-data.events.v1`, the `listEligibleAccounts` and `snapshot(page)` activities registered for the measures consumer, and the JOB-04 reconciliation started by `AceDataReady` and writing `reconciliation_result`**, so that **the baseline of RWB-E1-013 is computed and published only from a complete, fresh and reconciled ACE business date, and the INT-19 extract to the data lake is not built at all (DP-17)**.

### 2. Business rationale

Measures are counted by hand from spreadsheets at month end today, and each team counts a case differently, so the frozen baseline of business date 2026-11-27 is only worth having if the date it is counted from is complete and reconciled (REQ-RDF-012; NFR-065; FSD P1 A2.19). This story is **the rwb-source-data slice of RWB-E1-013 and nothing more**. The measure definitions, the snapshots, the baseline flag, the frozen flag, the measures Schedule and the publication are P9's: `measure_definition` and `measure_snapshot` stay in `rwb_reporting` under RWB-P9-E1013-APP, and **this story owns no measure calculation of its own and reads no measure table** (DP-01). It owns the facts and the gate the calculation needs: the readiness signal, the freshness stamp from the ACE batch record, the payments since entry read through `v_ace_payment`, the two events, the two activities P9 calls, and the JOB-04 reconciliation of the case list against `v_ace_account`.

The legacy story gave P1 three interfaces in its own section 12: `RecoveryDataApi.paymentsSinceEntry(businessDate)`, the `DailyCompletenessGate.check(businessDate, productCodes)` over `v_ace_batch_status`, and the case-fact feed P3 serves. In the target those three become contract-first surface on the P1 base `/api/recovery/source-data/v1`, with the residual `AceDataReady` and `AceDataLate` events of the Architecture v5 catalogue on `rwb.source-data.events.v1` (Arch v5 slides 15 and 32). The gate is what makes the baseline honest: no data job for a business date starts until the ALS batch for that date is COMPLETE, and a stale product is named with its date rather than published as today's number (BR4; BR-P1-014-4; CTL-02).

Two things change against the legacy text, and both are recorded. **DP-17 removes the data lake**: there is no INT-19 extract, no freshness-stamped extract file, no trailer count and no Power BI data set refreshed from a lake, so legacy AC3 and legacy AC7 - the two criteria that assert exactly those artefacts - have no P1 deliverable at all (GAP-0558; ASM-0799). The publish and the hold survive, on the P9 publication, and this slice answers the gate they read. Second, the legacy key is split four ways: the definitions, the snapshot, the flags, the Schedule and the publication are P9's, the case facts are P3's, the cross-service proof of AC2 and AC6 is RWB-ITG-E1013-ITG's, and this is the P1 side (GAP-0560; ASM-0801). The ITG suite names this surface as the one it calls, and the four operations here are exactly the four it lists.

The DPs that leave the legacy design behind are all applied: the owner's schema instead of `recovery` (DP-01), the local decision record (DP-03), the ACE views as the only read path (DP-05), reference data as data (DP-07), the event-started workflow instead of Quartz `JOB-04` (DP-10), one hop with a 2 s budget (DP-11), the per-service REST base (DP-13), the per-service Flyway sequence (DP-15), no data lake (DP-17) and the gateway-bff route for the screen and the banner (DP-19).

### 3. Preconditions

- RWB-P1-E1001-APP is done: the tables of `rwb_source_data` exist, among them `data_product`, `data_product_load`, `reconciliation_result`, `case_list_row`, `sys_objects`, `sys_fields` and the four extension tables, with their dictionary rows.
- RWB-P1-E1069-APP and RWB-P1-E1069-DB are done: the 30 `recovery.v_ace_*` views compile in DEV and SIT, the rwb-source-data login holds SELECT on them and nothing in `public`, and `v_ace_payment` returns `payment_date` and `payment_amount` (DF-ACE-045, DF-ACE-046).
- `v_ace_batch_status` is a Section B view over `public.ace_batch_run` and needs RWB-ACE-001 in place (DL43; OQ-P1-01, OQ-P1-02). Until it lands, the freshness of every source-fed product shows STALE with no business date and no data job starts on its own (TSD P1 T3.7).
- The platform libraries and their contracts are live: the local decision-record library and `rwb.decision-record.v1` (DP-03), the reference-data contract for LOV-DATA-PRODUCT, LOV-FRESHNESS, LOV-PUBLISH-STATUS and LOV-REC-RESULT (DP-07), the workflow kit with the namespace `rwb-recovery` (DP-10), the messaging library with outbox, inbox, retry and `.dlt` topics (DP-09 is not a pattern of this story, the library is), the per-service Flyway baseline (DP-15) and the gateway-bff route (DP-19).
- RWB-P9-E1013-CON is published: the measures contract that consumes the facts, so this story can build against its fake.
- The bank's Airflow DAG of the ACE ingestion chain is in place and its last task can call `POST /api/recovery/source-data/v1/business-days/{date}/ready`, and a sensor polls `GET /api/recovery/source-data/v1/business-days/{date}/status` (Arch v5 slide 32). While ACE ingestion is still on Control-M, the fallback poll of the ACE batch record stands in for the call (Arch v5 slide 31 notes).
- SIT holds the namespace `rwb-recovery`, the task queue `rwb-source-data`, the topic `rwb.source-data.events.v1` with its retry and `.dlt` topics and the schema registry with BACKWARD compatibility, and no production data is used.
- The late cut-off of a business date is 05:30 and the readiness chain is expected before the working day starts (Arch v5 slide 31; NFR-013; NFR-019). Release 30 November 2026 is tentative and a date is never a blocker.
- This is a secondary slice: it is Day 1 under Template and Rules §R5.7, it adds no build dependency of its own, and the H dependencies of the DP table arrive with the platform, database and operations stories of the epic (section 13). The story that registers the Schedules and the queue is not named by this Work Package (GAP-0561; ASM-0802).

### 4. Flow

1. Bank Airflow: the ACE ingestion DAG for the business date completes and its last task calls `POST /api/recovery/source-data/v1/business-days/2026-11-27/ready`, once per business date (Arch v5 slide 32).
2. rwb-source-data: `ReadinessController` records the call against the business date through the idempotency object of the library and answers **202** at once with the business date and the state RUNNING; a second call for the same date answers 202, publishes nothing and starts nothing.
3. rwb-source-data: `AceIngestCheck` reads `v_ace_batch_status` for the business date, one row per source system, and maps each source-fed product to its sources (DP01 and DP13 to ALS and GL, DP02 to SCBPDM, DP05 to EFS, DP06 to CCMS, SVAF, AMIS and RPS, DP07 to LIT and WIN, DP11 to COLLINS; DP03, DP04 and the other Workbench products on change).
4. rwb-source-data: for every mapped source with `is_complete` true, the freshness stamp of every product it feeds is written in `data_product_load` with the source system, the business date, the source time from `started_at`, the load time from `completed_at` and status LOADED; a repeat COMPLETED read adds one to `duplicate_count` and writes nothing else.
5. rwb-source-data: `AceDataReadyPublisher` writes `rwb.source-data.AceDataReady.v1` to the outbox in the same transaction as the stamps and the relay publishes it on `rwb.source-data.events.v1`, keyed by the business date. rwb-case starts `DailyCaseRun` on it (JOB-02, JOB-03), rwb-payment starts its matching, and this service starts its own JOB-04 reconciliation (Arch v5 slide 31 notes).
6. rwb-source-data: `FreshnessGate` answers the daily gate for the business date - **COMPLETE** when every mapped source of the date is complete, **HOLD** otherwise - and names each product, its business date and its status with MSG-P1-001 where it is stale.
7. rwb-source-data: `PaymentFactsQuery` answers `GET /payments?accountId=` from `v_ace_payment` with the payment facts of the account, one hop, inside the 2 s budget, and only the fields the caller's masking answer allows.
8. rwb-source-data: `ReconciliationWorkflow`, started by the `AceDataReady` event after the case creation of the date, runs REC-01, REC-02 and REC-05 for the one business date of the batch and writes `reconciliation_result` per check and product group with its counts, amounts, variance and result; the publish status of the `case_list_row` rows of the date is set to RELEASED when every REC-01 and REC-02 result is PASS and to HELD otherwise.
9. rwb-source-data: `ListEligibleAccountsActivity` answers the accounts eligible for the business date and `SnapshotActivity.snapshot(page)` answers one page of the facts for a business date, repeatably and in a stable order, for the measures consumer of RWB-P9-E1013-CON.
10. rwb-source-data: `AceDataLateCheck` runs at 05:30. Where a business date is still not ready, the product is flagged STALE with its stale flag time, `rwb.source-data.AceDataLate.v1` is published with the source system, the business date and the latest status, the alarm goes to the operations channel and the banner carries the text of MSG-P1-001.
11. rwb-source-data: the `status` operation answers RUNNING while the chain runs, DONE when the stamps and the reconciliation of the date are written, and LATE when the cut-off passed without a complete batch. Nothing in steps 1 to 11 writes a measure row, an extract file or a lake object (DP-17).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A second readiness call for the same business date | 202 is answered again from the idempotency record; no stamp is rewritten, no event is published and no workflow is started twice | None | AC1 |
| X2 | The readiness call for a date whose ACE batch record holds no ALS row | 202 is still answered and the state stays RUNNING; the gate answers HOLD for the date and no data job starts | MSG-P1-001 | AC2, AC4 |
| X3 | The cut-off of 05:30 passes with a source not complete | The product is STALE, `AceDataLate` is published, the alarm is raised and the banner shows the stale product and date | MSG-P1-001 | AC4 |
| X4 | `v_ace_batch_status` or another view is unavailable during the check | The run ends FAILED, no stamp and no event is written for the date, and the rerun writes them; the state stays RUNNING | MSG-GEN-006 | AC2 |
| X5 | A third party answers the payments read out of budget | The call fails after the 2 s budget and is not retried into a pass; nothing is cached as if it had answered | MSG-GEN-006 | AC5 |
| X6 | A consumed event or a published event is refused by the broker | The library retries and then moves the message to the `.dlt` topic of the owner topic; the duplicate is absorbed by the inbox key | None | AC3 |
| X7 | A class of the service names a data-lake endpoint or the INT-19 extract | The build fails on the rule and names the class; nothing merges | Build log | AC7 |
| X8 | JOB-04 starts for a business date whose batch is not complete | The workflow does not start, no `reconciliation_result` row is written for the date and the case list of the date keeps its previous publish status | MSG-P1-001 | AC7 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the tables of RWB-P1-E1001-APP, the views of RWB-P1-E1069-APP and the fake of RWB-P9-E1013-CON; it reads no measure table and calls no other service at run time |
| Negotiable | Product codes, message ids, the 05:30 cut-off and the retry policy are data or configuration; the operations, the two event types and the two activities are fixed by the Architecture v5 catalogue |
| Valuable | The baseline is computed only from a business date that is complete, fresh and reconciled, and the lake step that used to be needed for it is gone |
| Estimable | Five components, two events, one workflow, two activities, one migration that adds no table |
| Small | Fits one sprint with its tests, as a secondary slice of the legacy key |
| Testable | Every criterion of section 7 is one automated test against a synthetic ACE batch fixture and a synthetic payment set |

### 7. Acceptance criteria

```gherkin
Feature: The rwb-source-data side of the baseline measures

  Background:
    Given v_ace_batch_status holds a COMPLETED ALS row for business date 2026-11-27
    Given the ACE batch record is read through the view v_ace_batch_status, one row per source system and business date
    Given the source-fed data products of the date are "DP01" Account and arrears and "DP03" Case
    Given message MSG-P1-001 reads "{product} is from {date}. Today's ACE batch has not arrived."
    Given the late cut-off of a business date is 05:30
    Given the service is rwb-source-data, on the base /api/recovery/source-data/v1, the topic rwb.source-data.events.v1 and the task queue rwb-source-data

  Scenario: AC1 The readiness call for a business date is idempotent and answers 202 once (new, D-RCV-60)
    Given the ACE batch record holds the COMPLETED ALS row for business date 2026-11-27
    When Airflow calls POST /api/recovery/source-data/v1/business-days/2026-11-27/ready
    Then the call answers 202 with the business date 2026-11-27 and the state RUNNING
    And one readiness record is held for the business date and one AceDataReady event is written to the outbox
    When the same call is made a second time for 2026-11-27
    Then the call answers 202 again with the same date and the same state
    And no second event is written, no workflow is started twice and no freshness stamp is rewritten
    And the repeat is recorded as a duplicate read of the date and nothing else changes
    When the chain of the date completes
    Then GET /api/recovery/source-data/v1/business-days/2026-11-27/status answers DONE

  Scenario: AC2 The freshness gate answers COMPLETE for a complete date and HOLD otherwise (new, D-RCV-60)
    Given the ALS row of business date 2026-11-27 is COMPLETED and the stamp of DP01 for that date is LOADED
    When GET /api/recovery/source-data/v1/data-products/freshness?asOf=2026-11-27 is called
    Then the gate answers COMPLETE for the business date 2026-11-27
    And every product answers its business date, its status and the ACE batch completion time
    Given no COMPLETED ALS row for business date 2026-11-28 exists and the stamp of DP01 is STALE with business date 2026-11-27
    When the gate is asked for 2026-11-28
    Then the gate answers HOLD
    And the answer names "DP01 Account and arrears" as {product} and 2026-11-27 as {date}
    And the answer carries the text of MSG-P1-001 with those two values
    And no data job for 2026-11-28 is started by the gate

  Scenario: AC3 A complete business date publishes AceDataReady once, in the CloudEvents envelope, with IDs and facts only (new, D-RCV-60)
    Given the stamp of every product fed by ALS is LOADED for business date 2026-11-27
    When the ingest check of the date completes
    Then exactly one rwb.source-data.AceDataReady.v1 is in the outbox in the same transaction as the stamps
    And the relay publishes it on rwb.source-data.events.v1 with the key 2026-11-27
    And the envelope holds id, source, type, specversion, time, subject and datacontenttype of CloudEvents 1.0
    And the payload holds eventId, occurredAt, schemaVersion, sourceSystem "ALS", businessDate "2026-11-27", status and completedAt only
    And the payload holds no field marked personal in sys_fields
    When the same COMPLETED row is read again
    Then no second AceDataReady event is published and the duplicate count of the stamp rises by one
    When a consumer fails the message
    Then it is retried on the retry topic and, after the last attempt, it is on the .dlt topic of rwb.source-data.events.v1

  Scenario: AC4 A business date still not ready at 05:30 publishes AceDataLate with the alarm and the banner (new, D-RCV-60)
    Given no COMPLETED ALS row for business date 2026-11-28 exists at 05:30
    When the late check of the cut-off runs at 05:30
    Then one rwb.source-data.AceDataLate.v1 is published on rwb.source-data.events.v1 with sourceSystem "ALS", businessDate "2026-11-28" and the latest status
    And DP01 carries status STALE with its stale flag time and the business date it last had
    And the alarm reaches the operations channel and the alerts consumer of the event
    And the banner carries the text of MSG-P1-001 with "DP01 Account and arrears" and the stale date
    And no data job for 2026-11-28 is started
    When the ALS batch of 2026-11-28 completes later
    Then the next ingest check stamps the date LOADED and publishes AceDataReady once for it

  Scenario: AC5 The payments read answers the payment facts of an account, one hop, inside 2 s (new, D-RCV-60)
    Given v_ace_payment holds payment "PAY-0001" for account "ACC0000017" with a payment_date and a payment_amount
    When a caller holding case record read calls GET /api/recovery/source-data/v1/payments?accountId=ACC0000017
    Then the answer holds one row per payment with payment_code, account_key, payment_date, payment_amount and data_as_of, read from v_ace_payment
    And payment_date is the date the view returns through the ACE text-date rule and payment_amount is the amount of the view
    And the call is one hop on the P1 base and is answered inside the 2 s budget
    And a personal field of the answer is returned only as the masking answer of the authorise decision allows, and masked otherwise
    And the answer carries no measure value, no total and no currency amount of its own

  Scenario: AC6 listEligibleAccounts and snapshot(page) are registered on rwb-source-data and the snapshot is paged and repeatable (new, D-RCV-60)
    Given the worker of rwb-source-data is registered in the namespace rwb-recovery on the task queue rwb-source-data
    When the measures consumer of RWB-P9-E1013-CON asks for the snapshot of business date 2026-11-27
    Then listEligibleAccounts and snapshot(page) are registered on rwb-source-data and listed in the workflow and activity catalogue of the service
    And a first call with page 1 returns one page of the facts of 2026-11-27 with a cursor for the next page
    And a call with that cursor returns the next page and no row of the first page
    When page 1 of 2026-11-27 is asked for twice
    Then both calls return the same rows in the same order
    When the snapshot of a business date is asked for after a rerun of the date
    Then it returns the facts of that business date only and no row of another date

  Scenario: AC7 JOB-04 is event-started, writes reconciliation_result and the service holds no lake path (new, D-RCV-60)
    Given the ALS row of business date 2026-11-27 is COMPLETED and the case creation of JOB-02 for that date is complete
    When rwb-source-data consumes its own AceDataReady for 2026-11-27
    Then the reconciliation workflow starts on rwb-source-data, started by the event and not by a Schedule
    And it writes reconciliation_result rows in schema rwb_source_data for REC-01 and REC-02 per product group, each with its source count, its workbench count, its variance count, its variance percent, its tolerance percent and a result of PASS or BREAK
    And every row carries the one business date 2026-11-27 and no row mixes two business dates
    And the case_list_row rows of the date carry publish_status RELEASED when every REC-01 and REC-02 result is PASS and HELD otherwise
    And the service holds no INT-19 extract, no extract file writer, no freshness-stamped file, no trailer count and no data-lake client
    And a build rule fails a class of the service that names a data-lake endpoint, the INT-19 identification or a lake container
```

The seven criteria above are new and test only the deliverable in this story's title, on values and names the sources give: the business dates, the product codes, the message text, the 05:30 cut-off and the payment field IDs of RWB-E1-013 and the P1 module. No measure value, threshold, volume, percentage, currency amount or measure code is asserted here, because none of them is computed in this slice (GAP-0562; ASM-0803). The legacy criteria sit elsewhere: AC1, AC4, AC5, AC7 and AC8 with RWB-P9-E1013-APP; AC2 and AC6 across services with RWB-ITG-E1013-ITG, which reads this slice through the four operations of section 12.1 and the readiness call. Legacy AC6 names "DP03 Case" and 2026-11-26 in its run record; the same gate answer path serves that naming, and this story names whichever product the gate holds.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Each measure is published only under a definition in force that names its data product, formula, unit and approver | RWB-E1-013 BR1; REQ-RDF-012; Principle 1 |
| BR2 | The baseline is the snapshot of the configured baseline business date and is frozen once written | RWB-E1-013 BR2; REQ-RDF-012; FEAT-RPT-01 |
| BR3 | Measures are computed from Workbench records read through the owning modules, never from a separate count | RWB-E1-013 BR3; NFR-065 |
| BR4 | A measure is computed only from a COMPLETED ACE batch; stale data is not published as the baseline | RWB-E1-013 BR4; CTL-02; MSG-P1-001 rule |
| BR5 | The extract to the data lake holds the publish and alerts on failure, and runs again in the next window | RWB-E1-013 BR5; INT-19 error handling |
| BR6 | Age bands are a reference list | RWB-E1-013 BR6; Principle 1 |
| BR7 | A definition load with any invalid row is refused in full | RWB-E1-013 BR7; refdata.txt change process, step 3 |
| BR8 | No data job for a business date starts until the ALS batch for that date is COMPLETE, and freshness is read from `v_ace_batch_status` only: never inferred from a row count, a file or a `data_as_of` | FSD P1 BR-P1-014-2 and BR-P1-014-4; TSD P1 T3.7 |
| BR9 | There is no data lake, no INT-19 extract and no Power BI feed: the service calls no lake endpoint and writes no extract file, and reporting reads events into `rwb_reporting` | DP-17; Arch v5 slides 8, 37 and 41; ADR-018 |
| BR10 | Every call is one hop to the owning service on its own base with a 2 s budget; no service is called through another service and a call outside the budget fails rather than being retried into a pass | DP-11; DP-13; ADR-020 |
| BR11 | Both events are CloudEvents 1.0 on `rwb.source-data.events.v1`, keyed by the business date, carrying IDs and facts only and no personal data field, with the owner's retry and `.dlt` topics and the BACKWARD compatibility of the schema registry | ADR-015; Arch v5 slides 42 and 43; TSD P1 T5.3 |
| BR12 | Every message is raised by its ID and its text from the message standard, never as a literal in code, and the values it carries are the product and the date of the freshness answer | FSD P1 VR-P1-001-1; TSD P1 T3.7; this story |
| BR13 | `measure_definition` and `measure_snapshot` are P9's and are neither read nor written here; this service owns no measure, no definition and no snapshot | Ownership Map (`measure_definition`, `measure_snapshot` P9); DP-01; FSD P1 A2.19 |
| BR14 | The readiness call is idempotent on the business date: a repeat answers 202, publishes nothing and starts nothing | Arch v5 slide 32; TSD P1 T3.7 (repeat rule) |

BR5 is read with BR9 and with DP-17: the publish and the hold survive on the P9 publication, and the lake destination of the legacy rule is removed, so this slice asserts the gate and the reconciliation that the publication reads and no lake step at all (GAP-0558; ASM-0799). BR1, BR2, BR6 and BR7 are P9's to enforce; they are copied here because the legacy story holds them and because the gate and the facts of this story are what they are enforced on.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| a business date, no readiness call yet | the Airflow call lands | The date is recorded and the ingest check starts | RUNNING |
| RUNNING | the stamps and the reconciliation of the date are written | Every mapped source of the date is complete | DONE |
| RUNNING | the 05:30 cut-off passes | A mapped source is not complete or its batch failed | LATE; the product is STALE and `AceDataLate` is published |
| LATE | a late batch completes | The next ingest check of the date succeeds | RUNNING and then DONE for the date; the stale flag is cleared by the LOADED stamp |
| a product stamp for a business date | a COMPLETED read of the same product and date | It is already LOADED | LOADED, `duplicate_count` + 1, nothing else written |
| a reconciliation result | the workflow of the date completes | Every REC-01 and REC-02 result is PASS | The case list rows of the date are RELEASED |
| a reconciliation result | the workflow of the date completes | A result is BREAK | The case list rows of the date stay HELD |

Only the states a source gives are listed. The status answer uses RUNNING, DONE and LATE, the three values of the Airflow interface contract (Arch v5 slide 32). The gate answers COMPLETE or HOLD; the freshness stamp carries LOADED or STALE (TSD P1 T3.7, LOV-FRESHNESS); the reconciliation result carries PASS or BREAK (LOV-REC-RESULT); the case list carries PENDING, HELD or RELEASED (LOV-PUBLISH-STATUS). The gate pair and the stamp pair are two levels of one condition and are kept apart, the gate for the date and the stamp for the product (GAP-0564; ASM-0805). A readiness vocabulary of NOT_READY and READY appears in no source and is not used (GAP-0563; ASM-0804). This story changes no case status: the case, its stage, its route and its queue move in rwb-case, and the baseline and frozen flags of `measure_snapshot` move in rwb_reporting.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-source-data service identity (the rwb-source-data login) | Serves the four operations, runs the ingest check, the JOB-04 reconciliation and the 05:30 late check, publishes both events, serves the two activities and writes the stamps and the reconciliation results |
| RW-DATASTEW, data steward and data product owner | Reads the freshness and the gate answer, reads the reconciliation results and the break list, and receives the stale and break alerts; changes no stamp and no result |
| RW-PLATADM, platform administrator | Reruns the JOB-04 reconciliation for a business date through the rerun operation of the service, and reads the run record; changes no business value |
| RW-TRIBE, Tribe lead and squad members | Reads the freshness the baseline is computed from and the baseline itself in the report P9 publishes; runs nothing in this service |
| RW-BIANAL, Reporting and BI analyst | Reads the events and the snapshot the measures are built from; builds no extract here and reads no lake data set, because there is none |
| No role | May read a `recovery.v_ace_*` view directly, write a stamp, edit a reconciliation result or ask for a measure value from this service |

The four roles are the ones the legacy story gives, with the capability areas of the FSD P1 role tables. The service identity holds SELECT on the views and on its own schema only (DP-02, BR-P1-001-4). No approval level of the delegation of authority applies: the story takes no business decision and approves nothing.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-043, DF-ACE-044, DF-ACE-045, DF-ACE-046, DF-ACE-054 | `v_ace_payment` (`recovery.v_ace_payment`) | payment_code, account_key, payment_date, payment_amount, data_as_of | Read |
| DF-ACE-178 to DF-ACE-186 | `v_ace_batch_status` (`recovery.v_ace_batch_status`) | source_system, business_date, started_at, completed_at, status, record_count, checksum, feed_version, is_complete | Read |
| DF-ACE-001 to DF-ACE-042 | `v_ace_account` (`recovery.v_ace_account`) | the account, balance and days-past-due fields of REC-01 and REC-02 | Read |
| DF-REF-070 to DF-REF-079 | `data_product` (`rwb_source_data`) | product_code, system_of_record, expected_by, refresh_cycle | Read |
| DF-OPS-001 to DF-OPS-009 | `data_product_load` (`rwb_source_data`) | product_code, source_system, business_date, source_extracted_at, loaded_at, status, stale_flagged_at, duplicate_count | Write; Read |
| DF-OPS-118 to DF-OPS-129 | `reconciliation_result` (`rwb_source_data`) | rec_code, business_date, product_group, source_count, workbench_count, source_amount, workbench_amount, variance_count, variance_pct, tolerance_pct, result | Write; Read |
| DF-RPT-002, DF-RPT-019 | `case_list_row` (`rwb_source_data`) | business_date, publish_status | Write (the release or hold of the date); Read |
| DF-REF-087 to DF-REF-093 | `sys_objects` (`rwb_source_data`) | object_name, data_product, system_of_record | Read |
| DF-REF-094 to DF-REF-110 | `sys_fields` (`rwb_source_data`) | field_id, is_personal, source_system | Read (the proof that no personal field enters a payload) |
| DF-RPT-032 to DF-RPT-040 | `measure_definition` (`rwb_reporting`) | measure_code to valid_from | Not read and not written: P9's table |
| DF-RPT-041 to DF-RPT-052 | `measure_snapshot` (`rwb_reporting`) | id to published_at | Not read and not written: P9's table |

Field IDs are those in the Logical Data Model and Data Dictionary and are copied from the P1 module and the legacy story. The measure tables are P9's, arrive with RWB-P9-E1013-APP and are not read here: this story supplies the facts and the gate, and the measure values of business date 2026-11-27 are computed and frozen in `rwb_reporting` (BR13; GAP-0562; ASM-0803). The rest of the `case_list_row` fields (DF-RPT-001 and DF-RPT-003 to DF-RPT-018) belong to the case list story of the epic and are not cited here.

### 12. Contract

#### 12.1 REST operations provided

Four operations on the base `/api/recovery/source-data/v1`, owned by P1 rwb-source-data. They are the four the integration suite of RWB-ITG-E1013-ITG calls, on the same paths.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/business-days/{date}/ready` | The readiness signal of a business date from the bank's Airflow, answered 202: records the date, starts the ingest check and publishes `AceDataReady` when the date is complete | Service caller with client credentials (Airflow) | Idempotent on the business date; the `Idempotency-Key` header carries the date; a repeat answers 202 and changes nothing |
| GET | `/business-days/{date}/status` | The state of the readiness chain of a business date: RUNNING while it runs, DONE when the date is stamped and reconciled, LATE when the cut-off passed without a complete batch. The Airflow sensor polls it | Service caller with client credentials (Airflow) | Not applicable |
| GET | `/data-products/freshness` | The daily completeness gate of a business date: COMPLETE or HOLD, and per product its business date, its status LOADED or STALE and the ACE batch completion time | Case record read; the DPs of the service | Not applicable |
| GET | `/payments?accountId={accountId}` | The payments of an ACE account from `v_ace_payment`, with the payment facts the measures read, masked by the caller's masking answer | Case record read | Not applicable |

Answers: the readiness answer holds the business date and the state; the status answer holds the date, the state and the time of the last change; the freshness answer holds the gate value of the date and one row per product; the payments answer holds one row per payment of the account. Errors: 400 a date or an account that cannot be read, 401 no session, 403 no right in the capability area (MSG-P4-002 of the access contract), 404 an unknown business date, 503 a view or the messaging library unavailable (MSG-GEN-006). The exact field names of the four responses are Not specified in the source documents (GAP-0563; ASM-0804). The read operations over `customers/{id}`, `accounts/{id}` and `collateral/{id}` of the same contract are delivered by the read contract story of the epic (RWB-P1-E1069-APP) and are not part of this slice.

#### 12.2 REST operations consumed

None at run time. rwb-source-data calls no service: it reads ACE through its own views, reads its own tables, and publishes and consumes its own events. **RWB-P9-E1013-CON is a contract dependency and not a call**: it is the measures contract that consumes the facts of this service, this story builds against its fake, **and P1 never calls P9 at run time**. The one hop and the 2 s budget of DP-11 apply to the inbound call of every operation above and to the activity invocation of section 12.5.

#### 12.3 Events published

| Event | Topic | Key | Payload | Delivery |
|---|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | the business date, `2026-11-27` | eventId, occurredAt, schemaVersion, sourceSystem, businessDate, status, completedAt | Outbox in the same transaction as the freshness stamps, at least once, one event per business date and source |
| `rwb.source-data.AceDataLate.v1` | `rwb.source-data.events.v1` | the business date of the late batch | the same seven elements, status being the latest status of the ACE batch row | Outbox, at least once, one event per cut-off and source |

Both are CloudEvents 1.0 with the attributes id, source, type, specversion, time, subject and datacontenttype, on the owner topic with its retry topic and its `.dlt` topic, under the topic and event naming rule of the platform (Arch v5 slide 15 names the two events and the topic; Template and Rules §R4 fixes `rwb.<short>.events.v1` and `rwb.<short>.<Event>.v1`; ADR-015 and the messaging library of the platform fix the envelope, the outbox, the inbox, the retry and the `.dlt` topics and the BACKWARD compatibility of the registry). DP-14 is not a pattern of this story: the names are the platform's standard, no naming work is added here and no dependency row is raised for it. The payload carries IDs, codes, a status and a time and no personal data field, and the two consumers named in the catalogue are the case service, the payment service and this service's own reconciliation (BR11).

#### 12.4 Events consumed

None. The readiness signal is the REST call of 12.1 and not an event: the Architecture v5 catalogue records "EVT (none: Airflow call; fallback polls ACE batch record)" for this service, so no topic is consumed here. The event that starts the reconciliation is this service's own `AceDataReady`, taken from its own outbox through the library and not from a consumed topic of another owner.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AceIngestCheck | Workflow, started by the readiness call of the business date | `rwb-source-data` | Input: business date, source systems of the date. Output: the freshness stamps of the date, the gate value and the `AceDataReady` event of a complete date |
| reconciliation (JOB-04) | Workflow, event-started by `AceDataReady` | `rwb-source-data` | Input: business date, the source systems of the ALS batch. Output: the `reconciliation_result` rows of the date and the publish status of the case list rows |
| listEligibleAccounts | Activity | `rwb-source-data` | Input: business date. Output: the accounts eligible for the date, read from `v_ace_account`, as the case set of the date and the eligible base of the measures |
| snapshot(page) | Activity | `rwb-source-data` | Input: business date and page cursor. Output: one page of the facts of the date with a cursor for the next page; the same page of the same date returns the same rows |

All four are registered on the namespace `rwb-recovery` and the task queue `rwb-source-data` by this story, and are the elements the Architecture v5 catalogue gives this service ("TMP Act: listEligibleAccounts, snapshot(page) · Workflow: AceIngestCheck, reconciliation"). They run with the workflow kit's retry policy: initial interval 1 s, back-off 2, and a non-retryable classification for a 4xx of a view read. The workflow history carries the business date, the source systems, the product codes and the counts only, never a personal field and never an amount that is not an aggregate of the date. The `DailyCaseRun` of rwb-case, the payment matching of rwb-payment and the measures Schedule of rwb-reporting are not registered here.

#### 12.6 Schedules

| Cadence | Owner of the cadence | Registration | Legacy reference |
|---|---|---|---|
| The readiness signal of the business date, when the ACE ingestion DAG completes (about 04:30) | Bank Airflow, outside the cluster | The Airflow task calls `POST /business-days/{date}/ready`; no Schedule of this service is created for it | The ACE batch-complete record that used to start JOB-04 |
| The late check at 05:30 | rwb-source-data | A Temporal Schedule of the workflow platform in the service, registered by the platform workflow story of the epic, not by this story | The source cut-off that raises `AceDataLate` (EV-27) |

There is no Quartz job here: the legacy `JOB-04` and the nightly chain become an event-started workflow and a Schedule of the workflow kit, and the ACE shared Quartz tables are not used (DP-10; Arch v5 slide 44). The registration of the 05:30 Schedule, of the two workers and of the queue belongs to the platform and operations stories of the epic, which this Work Package does not name; the dependency is therefore recorded as a note and a gap rather than as a build dependency (GAP-0561; ASM-0802). DP-10 is applied as the pattern of the job and adds no dependency row to this secondary slice.

#### 12.7 Tables owned

| Table | Schema | Owner | Use in this story |
|---|---|---|---|
| `data_product_load` | `rwb_source_data` | P1 | The freshness stamp of a product and business date; written by the ingest check, read by the gate |
| `reconciliation_result` | `rwb_source_data` | P1 | REC-01, REC-02 and REC-05 results per check and product group of the date |
| `case_list_row` | `rwb_source_data` | P1 | The publish status of the date, RELEASED or HELD by the reconciliation; the other fields are the case list story's |
| `outbox_event`, `processed_event`, `idempotency_key` | `rwb_source_data` | PLT library, created in this schema | The outbox of the two events, the inbox dedupe and the idempotency of the readiness call |

No table of another service is read and no foreign key crosses a schema (DP-01). `data_product`, `data_product_access`, `data_contract`, `sys_objects`, `sys_fields` and `sys_field_version` are P1's as well and are read here; they arrive with RWB-P1-E1001-APP and no row of theirs is written by this story. `measure_definition` and `measure_snapshot` are P9's and are not touched (BR13).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-P9-E1013-CON fake | The measures contract that consumes `listEligibleAccounts` and `snapshot(page)` | A consumer that asks for one page, a consumer that asks for the next page, and a consumer that asks for the same page twice |
| ACE batch fixture | `v_ace_batch_status` and the other views of the gate | A COMPLETED ALS row for 2026-11-27, its absence for 2026-11-28, a FAILED row, and a repeat COMPLETED read |
| Airflow trigger stub | The bank scheduler, outside the cluster | Calls `POST /business-days/{date}/ready` and polls `GET /business-days/{date}/status`; it holds no business rule |
| messaging library stub | The outbox, relay, retry and `.dlt` path | A healthy broker, a refused consumer that ends on `.dlt`, and a repeat read that publishes nothing |

The views are not faked in the component tests: they run against the container of the service with synthetic rows. No contract of another service is faked beyond the measures contract of RWB-P9-E1013-CON.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 0 consumed | The readiness call, the status call, the freshness and gate, the payments read; one hop, 2 s (DP-11, DP-13) |
| Kafka | 2 published, 0 consumed | `AceDataReady` and `AceDataLate` on `rwb.source-data.events.v1`, keyed by the business date, with the retry and `.dlt` topics |
| Temporal | 2 workflows, 2 activities | `AceIngestCheck` and `reconciliation` (event-started); `listEligibleAccounts` and `snapshot(page)`; queue `rwb-source-data` |
| File | None | No extract file, no lake object, no Power BI feed (DP-17) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata`, modules `readiness`, `freshness`, `payment`, `events`, `reconciliation` and `snapshot`, in the service root of rwb-source-data.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `ReadinessController` | Controller | The four operations of 12.1; validates the date and the account, maps an error to a problem response, answers the readiness call from the idempotency record and 202 |
| `AceIngestCheck` | Workflow | Reads `v_ace_batch_status` of the business date, maps the products to their sources, writes the stamps, computes the gate value and publishes `AceDataReady` once |
| `FreshnessGate` | Service | Answers COMPLETE or HOLD for the date, per product its business date, status and completion time, and the MSG-P1-001 text of a stale product |
| `PaymentFactsQuery` | Service | Reads `v_ace_payment` by `account_key` and returns the payment facts of the account, masked by the role answer |
| `AceDataReadyPublisher` | Service | Writes the two events to the outbox in the transaction of the stamps, with the envelope of 12.3 and the business date as the key |
| `AceDataLateCheck` | Workflow and Schedule handler | The 05:30 cut-off: flags STALE, publishes `AceDataLate`, raises the alarm and feeds the banner |
| `ListEligibleAccountsActivity` | Activity | The accounts eligible for the date, read from `v_ace_account` |
| `SnapshotActivity` | Activity | `snapshot(page)`: one page of the facts of the date, with a cursor and a stable order |
| `ReconciliationWorkflow` | Workflow, event-started | REC-01, REC-02 and REC-05 of the date, writing `reconciliation_result` and setting the publish status of the case list rows |
| `LakeFreeRule` | ArchUnit rule in the test source | Fails the build on a class that names a data-lake endpoint, the INT-19 identification or a lake container (DP-17) |

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

Every DP is applied as the pattern the table fixes. DP-01: the stamps and the reconciliation results sit in `rwb_source_data` and no other schema is read. DP-03: the readiness call, the gate answer of a rerun and the reconciliation result are recorded through the local decision-record library before they are returned or written. DP-05: the ACE data of this service comes only through the 30 `recovery.v_ace_*` views, which only rwb-source-data reads. DP-07: the product codes, the freshness status, the publish status and the reconciliation result are read from the reference-data contract, never written in code. DP-10: the legacy JOB-04 becomes the event-started reconciliation workflow and the 05:30 cut-off becomes a Schedule of the workflow kit. DP-11 and DP-13: four operations on the per-service base with a 2 s budget. DP-15: one migration in the service's own sequence. DP-17: no lake path anywhere, enforced by the build rule. DP-19: the banner and the run monitor are read through the gateway-bff route. **This is a secondary slice and it adds no build dependency of its own**: the H dependencies named above arrive with the platform, database, workflow and edge stories of the epic, and the metadata rows of this story stay exactly as this Work Package fixes them (section 3; GAP-0561).

**Database and migrations.** One migration in the per-service Flyway sequence of `rwb_source_data`, `V1013_1__reconciliation_result_index.sql`, at the next free sequence at merge (DP-15). It adds no table and no column: the tables arrive with RWB-P1-E1001-APP. Its statement is the covering index on `reconciliation_result (business_date, rec_code, product_group)` for the JOB-04 rerun and the read of the date, created idempotently so a repeated pipeline run has no effect. The readiness idempotency is the `idempotency_key` object of the library and adds no table of this story.

**Configuration and reference data**

- The late cut-off of 05:30 and the expected-by time of each product are configuration and the `data_product.expected_by` row, never a constant (BR12). The 05:30 time is the one Arch v5 slides 15 and 32 give.
- The product-to-source map of section 4 is read from `data_product` and `data_contract`, not written in code.
- The currency, the tolerance of REC-01 and REC-02 and every amount are not set by this story: the tolerance is `recon.tolerance.pct` under DL25, and this story carries the value it reads.
- The feature switch is `rwb.source-data.daily-gate`, read as a parameter: off answers HOLD for every product and starts no data job, and the readiness call still answers 202. The switch name is this story's own configuration, not a business value.
- The login is the rwb-source-data login (DP-02), holding SELECT on the views and on `rwb_source_data` only.

**Build steps**

1. The migration `V1013_1__reconciliation_result_index.sql`, with a repeated run proving no effect; test that the index is used by the read of the date.
2. `ReadinessController` and the idempotency object: the first call 202, the repeat 202 with nothing published and nothing started, and the status answering RUNNING and DONE; tests for AC1.
3. `AceIngestCheck` against the ACE batch fixture: the product-to-source map, the stamps, the repeat read and the duplicate count; tests for AC3.
4. `FreshnessGate` with COMPLETE, HOLD and the stale naming of MSG-P1-001; tests for AC2.
5. `AceDataReadyPublisher` with the envelope, the business-date key and the no-personal-field check against `sys_fields`; the retry and `.dlt` path of the library stub; tests for AC3.
6. `AceDataLateCheck` at 05:30 with the STALE flag, the event, the alarm and the banner feed; tests for AC4.
7. `PaymentFactsQuery` with the account path, the 2 s budget of the client and the masked field path; tests for AC5.
8. `ListEligibleAccountsActivity` and `SnapshotActivity` with the cursor, the stable order and the repeat of a page; tests for AC6.
9. `ReconciliationWorkflow` event-started by `AceDataReady`, with the one-date rule, the six rows of REC-01 and REC-02 per product group and the publish status; tests for AC7.
10. `LakeFreeRule` with a fixture class on a lake endpoint and on the INT-19 identification, and a contract-fake run of the whole path so the story builds before rwb-reporting is live.

**Feature switch.** `rwb.source-data.daily-gate`, read as a parameter; off answers HOLD and starts no data job, and the readiness call still answers 202.

**Done when.** The tests in section 16 pass, the four operations answer on `/api/recovery/source-data/v1` in SIT, the readiness call is 202 on the first and the second call, the gate answers COMPLETE for business date 2026-11-27 and HOLD for a date whose ALS batch is absent, one `AceDataReady` and one `AceDataLate` are on `rwb.source-data.events.v1` with their envelope and key, the two activities are registered on `rwb-source-data`, the reconciliation writes `reconciliation_result` for the date, and the build is red on a lake endpoint and green without one.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | The ACE batch for the business date is not COMPLETE | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-006 | A system the answer depends on is unavailable | {system} is not available. Your request is queued and will be retried. |

These two are the ones this service raises: MSG-P1-001 in the gate answer, in the run record and in the banner, with {product} and {date} the two values of the freshness answer, and MSG-GEN-006 for the ACE database or the messaging library when it does not answer. Its text is the FSD P1 wording of VR-P1-001-1 and TSD P1 T3.7, which names the ACE batch; the legacy story and the integration copy still read "Today's load has not arrived", and the difference is recorded (GAP-0565; ASM-0806).

MSG-GEN-001 (a definition row lacks a required value), MSG-P9-001 (the baseline is published again) and MSG-P9-003 (a measure has no definition in force) are P9's: they are raised by RWB-P9-E1013-APP on the definition load and the publication, this service raises none of them, and their texts are not copied here. The hold of the case list raises MSG-P1-012 of the FSD P1 message table; it is not one of the five message IDs this Work Package fixes and is copied from that table when the hold path is tested.

### 15. Screens and states

No screen is built by this story. Two reader surfaces show what it produces, and both are served by the **gateway-bff composite route** (DP-19), which calls this service for the freshness and the run state and rwb-access for the role and masking answer, one hop each:

- **SCR-44 Interface and job monitor** shows the ACE batch status per source and business date and the data jobs with their state and their rerun, which is where the platform administrator reads the RUNNING, DONE and LATE states of section 9. The screen comes first in E2 and is full in E8; it is not built here.
- **The stale banner** on the case work surfaces carries the text of MSG-P1-001 with the product and the stale date, as Arch v5 slide 31 gives it ("rwb-source-data still publishes AceDataLate at 05:30 with an alarm and a banner").

The route, its composition and the field-level rendering of the banner are the platform's and the screen owner's. DP-19 is a pattern of this story and its H dependency is not in the metadata, because this secondary slice builds no route: the dependency stands with the platform edge story (GAP-0561). SCR-37 Steering dashboard is RWB-E2-009 and is out of scope.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-013-01 | AC1, BR1 | End to end | Definition file of 6 rows approved by TRB-0001 |
| TC-E1-013-02 | AC2, BR2, BR3 | End to end | 120 synthetic cases on 2026-11-27 with known totals |
| TC-E1-013-03 | AC3, BR5 | End to end | JOB-15 on 2026-12-02 for business date 2026-12-01 |
| TC-E1-013-04 | AC4, BR7 | End to end | TIME_IN_STAGE with no formula |
| TC-E1-013-05 | AC5, BR2 | End to end | JOB-15 rerun for 2026-11-27 |
| TC-E1-013-06 | AC6, BR4 | End to end | No COMPLETED ALS row for 2026-11-27 |
| TC-E1-013-07 | AC7, BR5 | End to end | Data lake load area stubbed unavailable |
| TC-E1-013-08 | AC8, BR1 | End to end | COST_PER_CASE with no definition |
| TC-E1-013-09 | Access | Component | RW-BIANAL calls POST /admin/reference-loads with table measure_definition; refused with MSG-P4-002 |

The nine legacy test case IDs of RWB-E1-013 are kept in their legacy order with the legacy Covers and Data text, and the legacy level System is carried as End to end and the legacy level Access as Component. **The `-ITG` copies belong to RWB-ITG-E1013-ITG**, and the P9 and P3 slices own their part of each case:

- TC-E1-013-01, -04, -05 and -08 are P9's: the definition load, the refusal of a row without a formula, the frozen rerun and the measure without a definition. Here they are regression evidence only, and the P1 part of -01 is that the definition load is not served by this service.
- TC-E1-013-02 exercises here the gate of AC2 and the payment facts of AC5, read through the two operations of 12.1; the 120-case arithmetic is P9's and the cross-service roll-up is the `-ITG` copy.
- TC-E1-013-06 exercises here the HOLD answer of AC2, the missing stamp of AC3 and the fact that no reconciliation result is written for the date (AC7); the MSG-P1-001 naming and the publication that follows are P9's and the `-ITG` copy.
- TC-E1-013-03 and -07 lose their lake step to DP-17: there is no extract, no freshness stamp in a file, no trailer and no unavailable lake to stub. Their P1 part is the gate and the freshness stamp of the date, and the publication that follows is P9's (GAP-0558; ASM-0799).
- TC-E1-013-09 exercises here the service identity and the refusal of a write on the views and on the reference load path this service does not serve; the reference-load refusal itself is P9's.

The full test, with its Given, When and Then, stays in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the product codes, the product-to-source map, the expected-by time, the 05:30 cut-off, the tolerance and the message text are data rows or configuration, read with the version in force. No date, amount, percentage or threshold appears in Java.
- No personal data in events, workflow inputs, logs, tests or prompts: both payloads carry IDs, codes, a status and a time only, the workflow history carries the business date and the counts only, and the proof is the `is_personal` flag of `sys_fields` over every field of the payload.
- ACE data only through the owner's contract or the `v_ace_*` views: this service is the owner of the views, reads them and nothing in `public`, and holds SELECT on them and on `rwb_source_data` only (DP-01, DP-05, DP-02).
- **DP-17: no data lake and no lake call.** There is no INT-19 extract, no extract file, no freshness-stamped file, no trailer count, no lake container, no Power BI data set and no lake client in this service; `LakeFreeRule` fails the build on a class that names one, and the test suite fails if a lake assertion is added back.
- One hop and a 2 s budget on every call and on every activity invocation; a timeout fails the test rather than being retried into a pass (DP-11).
- The readiness call is idempotent on the business date and no repeat publishes an event or starts a workflow (BR14).
- Both events are CloudEvents 1.0 on the owner topic with the retry and `.dlt` topics and the BACKWARD compatibility of the registry; a message without the envelope or of an unknown type goes to `.dlt` (BR11).
- No measure table is read or written, and no measure value is computed here: `measure_definition` and `measure_snapshot` are P9's (BR13).
- One migration per story in the service's own Flyway sequence, a repeated run with no effect, and no applied version edited in place (DP-15).
- Synthetic data only in the tests: the ACE batch fixture rows and the payment rows of the fixture account, never a production row.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-012 | Baseline measures for cases by route, age and queue, realized recovery, time in stage and turnaround per route are published, with definitions agreed by the Tribe, from a complete and reconciled ACE business date | Business Requirements Epic 1, sections 3.8 and 4 | FEAT-RDF-19, FEAT-RPT-01 | 15 Manage performance, data and AI | RWB-E1-013 BR1 to BR7; CTL-02; BR-P1-014-2 and BR-P1-014-4; DP-17 | TC-E1-013-01 to TC-E1-013-09 |

| Element | Owner | What it carries of the legacy key |
|---|---|---|
| RWB-P9-E1013-APP | P9 rwb-reporting | The definition load, `measure_definition` and `measure_snapshot`, the baseline and frozen flags, the measures Schedule, the publication and the measures read |
| RWB-P3-E1013-APP | P3 rwb-case | The case facts the baseline is counted from: route, stage, queue, entry date and stage clock start of the date |
| RWB-ITG-E1013-ITG | Integration, wave 1 | The cross-service proof of legacy AC2 and AC6, calling the four operations of 12.1 on the real services in SIT |
| RWB-P1-E1069-APP | P1 rwb-source-data | The views, the grant and the read contract this story reads ACE through |
| RWB-P1-E1001-APP | P1 rwb-source-data | The tables and the dictionary rows this story writes and reads |

The requirement, the two features and the control CTL-02 keep their legacy IDs. DP-17 is the pattern that changes the legacy deliverable: there is no INT-19 extract and no Power BI feed, and the reporting side reads events into `rwb_reporting` (GAP-0558; GAP-0559; ASM-0799; ASM-0800). The `-ITG` copies of the nine test cases are carried by RWB-ITG-E1013-ITG.

### 19. Out of scope

- The measure definition load, the snapshot, the baseline flag, the frozen flag, the measures Schedule at 01:30 and the publication: RWB-P9-E1013-APP.
- The case facts of the baseline and the case creation of JOB-02: RWB-P3-E1013-APP and RWB-P3-E1018-APP.
- The cross-service proof of AC2 and AC6 and every `-ITG` copy of a test case: RWB-ITG-E1013-ITG.
- The view definitions, the grant, the per-service login and the boundary rule: RWB-P1-E1069-APP and RWB-P1-E1069-DB.
- The tables and dictionary rows of `rwb_source_data`, the case list build itself and the catalog loads: RWB-P1-E1001-APP and the other P1 stories of the epic.
- The three read operations over customers, accounts and collateral of the same contract: RWB-P1-E1069-APP.
- SCR-44 Interface and job monitor, the case work surfaces and the banner rendering: the edge and screen stories of the platform and the case service; SCR-37 Steering dashboard is RWB-E2-009.
- The registration of the 05:30 Schedule, of the two workers, of the queue and of the topics: the platform workflow, DevOps and event stories of the epic.
- **The data lake, INT-19, INT-20 and the Power BI feed, removed from the target architecture by DP-17**: no extract, no lake container, no data set and no lake assertion is built here or anywhere else in wave 1.
- The non-functional epic RWB-ITG-NFR and its performance, resilience and observability criteria.
