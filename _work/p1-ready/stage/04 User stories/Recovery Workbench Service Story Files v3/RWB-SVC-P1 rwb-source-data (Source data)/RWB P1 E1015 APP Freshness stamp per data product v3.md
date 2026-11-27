# RWB-P1-E1015-APP Freshness stamp per data product

Version 3. 27 November 2026.
SCB Collections and Recovery. Henka Group.
(C) Siam Commercial Bank and Henka Pte Ltd

### Version 3 changes

- Applied RD-P1-003, RD-P1-005, RD-P1-022, RD-P1-040 and RD-P1-041 (stamp state model, one business-date workflow, late event at 05:30, outbox events, wire names); fixed findings #1-#6, #8, #9, #11, #13-#15, #22, #27 and #28.
- Applied RD-P1-021 and RD-P1-024: the gate source set is data_product_source and P1 holds no case list; fixed findings #7 and #18.
- Applied RD-P1-004 (401 MSG-P4-001, unknown product 400 MSG-GEN-007) and RD-P1-001; fixed findings #10, #19 and #23.
- Findings #12, #16, #17, #20, #21 and #25 are fixed as far as the rulings go; what no source states is listed as pending, with a temporary gap ID each, in section 20.
- Findings #24 (test case rows) and #26 (contract and fake not yet published) are delivery steps in section 20.
- Applied RD-P1-043 for the feature flag; business rule IDs BR1 to BR11 and exception IDs X1 to X11 keep their version 2 meaning.
- Finishing pass (RD-P1-062, RD-P1-065, RD-P1-066, RD-P1-068; requests S11-stories-0362, W3-messages-0038, W5-runtime-0062; test case backfill): JOB-08 is rwb-integration's, the DP04 stamp and never-stamped message are stated, and Test Cases v9 IDs are cited.

| Item | Value |
|---|---|
| Story key | RWB-P1-E1015-APP |
| Work type | APP (App development) |
| Size | Not specified; set by the squad at refinement (DOR-RWB-P1-E1015-APP-16) |
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
| Ready to start | After RWB-P1-E1001-APP, RWB-P1-E1069-APP and RWB-P1-E1015-CON |
| Depends on (build) | RWB-P1-E1015-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| Contract dependencies | RWB-P1-E1015-CON, RWB-P3-E1043-CON, RWB-P7-E1027-CON |
| Integration dependencies | None |
| External dependencies | RWB-P1-E1015-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-014, FR-P1-015, FR-P1-016, FR-P1-017) |
| Contract version | rwb-source-data.yaml 5.1.0 and asyncapi/rwb-source-data.asyncapi.yaml 5.1.0 (Recovery Workbench API Specification v7) |
| Epic design sign-off | Pending (DOR-RWB-P1-E1015-APP-14) |
| Readiness decisions | RD-P1-001, RD-P1-002, RD-P1-003, RD-P1-004, RD-P1-005, RD-P1-020, RD-P1-021, RD-P1-022, RD-P1-024, RD-P1-028, RD-P1-040, RD-P1-041, RD-P1-043, RD-P1-062, RD-P1-065, RD-P1-066, RD-P1-068 |
| CON Done | Pending |
| Fake published | Pending |
| DEV test data | Pending |
| Status | Draft (RD-P1 decisions applied; delivery pending) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-015 for rwb-source-data. The freshness stamp, the stale flag and the daily gate move from a Quartz job over the one `recovery` schema to `AceIngestCheckWorkflow` on task queue `rwb-source-data`, started by a listener on `v_ace_batch_status` and by one Temporal Schedule per data product (DP-10). The stamps are written in `rwb_source_data` (DP-01, DP-02, DP-15); `AceDataReady` (EV-26) and `AceDataLate` (EV-27) are published on `rwb.source-data.events.v1` through the outbox (DP-09); the decision inputs snapshot stays P7's, read through `FreshnessQuery` (DP-03, DP-11). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1015-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (36 resolved, 23 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: applied the binding decisions and story review fixes. Agent: S3-stories.

### 1. Story

As a data steward and data product owner (RW-DATASTEW), I want one AceIngestCheck run per business date to stamp each product only after every mapped source has completed, expose freshness through the published contract, emit the ready and late events, and gate daily jobs on their mapped source set, so that consumers can see the age of their data and jobs never start on a partial source set.

RWB-P1-E1015-APP owns the AceIngestCheck workflow, freshness stamps, AceDataReady, AceDataLate, DailyCompletenessGate and GET /data-products/freshness. RWB-P1-E1013-APP owns the readiness handler and record; RWB-P1-E1015-CON publishes the freshness and readiness contracts. P1 does not own a case list or its table (RD-P1-022, RD-P1-024).

- **Kept in substance:** one stamp per data product and business date, written from `v_ace_batch_status` only; the cut-off per product at `data_product.expected_by`; the stale flag with `stale_flagged_at`; the daily completeness gate; the two events.
- **The stamp lives in P1's own schema:** `data_product_load` is in `rwb_source_data`, created by RWB-P1-E1001-APP and written only here. No other service reads the table; a caller reaches freshness through the contract of RWB-P1-E1015-CON.
- **The decision log stays P7's:** this story writes no `decision_log_entry` and no inputs snapshot; P7 reads the stamps and writes its own snapshot.
- **Bases and names:** schema and login `rwb_source_data`, REST base `/api/recovery/source-data/v1`, topic `rwb.source-data.events.v1`, event names `rwb.source-data.<Event>.v1`, task queue `rwb-source-data` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.sourcedata`.

### 2. Business rationale

ACE owns source data; rwb-source-data reads recovery.v_ace_* through its service login and writes only its own freshness records. One owner for data_product_load, the two events and the completeness gate gives every consumer one contract-backed freshness answer and prevents daily jobs from starting while a required source is incomplete (D-RCV-35; RD-P1-022; RD-P1-041). Serves REQ-RDF-009; measure: the ACE batch is complete when the Workbench reads it on 99 percent of days (FSD P1 A2.14.1).

The workflow is started by the readiness handler, the 05:30 late-check Schedule and the flagged Control-M fallback poll. Each start reaches the same business-date workflow identity. Freshness is exposed through RWB-P1-E1015-CON; decision snapshots remain owned by rwb-decision.

Wave 1 asserts JOB-02 (rwb-case) and JOB-04 (rwb-source-data); the start of JOB-07 (rwb-payment) and JOB-08 (rwb-integration, RD-P1-066), both wave 2, is verified in RWB-ITG-W2.

### 3. Preconditions

- RWB-P1-E1001-APP has created data_product, data_product_source and data_product_load (unique key on product_code and business_date) in rwb_source_data.
- RWB-P1-E1069-APP has made recovery.v_ace_batch_status readable by the rwb_source_data login. Section B reads stay behind the feature flag in SIT, UAT and PROD until the ACE dependency gate passes; DEV and the pipeline database use the synthetic Section B fixture of RWB-P1-E1065-CON (RD-P1-043).
- RWB-P1-E1015-CON publishes rwb-source-data.yaml 5.1.0 and the matching event contract; the fake and DEV fixtures are still pending.
- data_product.refresh_cycle, data_product.expected_by (08:00 for daily products, Monday 08:00 for DP06; DL11), the DP14 holiday calendar and data_product_source rows are available to the worker. Confirm the source_system seed against the ACE code list (ASM-5695); owner ACE team lead.
- P1 owns data_product_source and data_product.expected_by; they change only through reference loads applied by the apply handler of RWB-P3-E1043-CON, and are read locally at run time (RD-P1-021).
- Settings: `ingest.poll.interval.minutes` = 5 and `rwb.dataengine.freshness.alert-channel` are per-environment values-file entries of rwb-source-data, not rows of the parameter catalog (RD-P1-028, RD-P1-040; ASM-5697). This story reads no rwb-case parameter.
- The caller of GET /data-products/freshness holds Case record R, the right of the published operation.
- RWB-P1-E1013-APP provides the readiness handler that starts AceIngestCheck; RWB-P1-E1011-APP and the daily job owners call the completeness gate for their product codes.
- RWB-PLT-E1071-CON (workflow kit and Schedule registration), RWB-PLT-TE006-CON (outbox), RWB-PLT-E1044-CON (migration sequence) and RWB-PLT-N001-CON (composite route) are in place.

### 4. Flow

1. **Starters.** (a) The handler of RWB-P1-E1013-APP behind POST /business-days/{date}/ready. (b) The Temporal Schedule rwb-source-data-ace-late-check, daily at 05:30 Asia/Bangkok, overlap SKIP, catch-up window 1 h: it starts the run for the expected business date when no run is open. A 05:30 occurrence missed by less than 1 h runs once on recovery; one missed by more than 1 h is not run. (c) The Control-M fallback poll, behind flag rwb.source-data.ingest-poll-fallback. The flag is off whenever the Airflow path is live. No source gives the time the poll starts on a run day (GAP-3277): until it is closed the poll is built and tested in DEV only and stays off in SIT, UAT and PROD.
2. **One run.** Workflow type AceIngestCheck (Java interface AceIngestCheckWorkflow), task queue rwb-source-data, namespace rwb-recovery, workflow ID ace-ingest-check-{businessDate} (ISO yyyy-MM-dd), input {businessDate, startedBy: AIRFLOW, SCHEDULE, POLL or ADMIN}. All system starts use conflict policy USE_EXISTING (a start while a run is open joins it and increments rwb_source_data_duplicate_start_total, ASM-5699) and reuse policy ALLOW_DUPLICATE (a start after the run closed opens a new run; the readiness handler of RWB-P1-E1013-APP requests no start once the readiness row is DONE or LATE, RD-P1-065). An admin rerun applies only to a FAILED run (RD-P1-012); the rerun operation arrives with RWB-P1-AD018 (ASM-5710). The run closes when every due source is COMPLETED and stamped, or 24 h after it started (ASM-5698).
3. **Read.** readBatchStatus(businessDate) reads v_ace_batch_status for every source system in data_product_source, by business date, so no view watermark is kept. A durable timer repeats the read every ingest.poll.interval.minutes = 5 until every source due that day is COMPLETED. A source is due when it feeds a DAILY product, or a WEEKLY product whose cycle day that is. RUNNING rows and rows with is_complete false create no stamp. A restarted worker resumes the run from Temporal history. Activity retry: 1 s initial interval, back-off 2, 10 attempts (Temporal catalog v3); start-to-close timeout and heartbeat are pending (GAP-0143). Pending: how a changed completed_at is detected where data_product_load holds only the latest completed_at of a multi-source product, or after the run for the date has closed; owner solution architect (GAP-3429).
4. **Stamp.** stampProducts reads data_product_source. For each product it writes a LOADED row only when every mapped source has a COMPLETED row for the same business date. source_system is the source whose completion completed the set; source_extracted_at is the latest source completed_at; loaded_at is the instant the row is written (RD-P1-005). The stamp and the AceDataReady outbox row commit in one transaction. AceDataReady is written once per source system and business date. DP04 is ON_CHANGE: its row is written when its mapped source (the core bank) completes, it is never set STALE by time and it is not in the DAILY gate set (RD-P1-068). Pending: how the `stampDp04` call of RWB-P1-E2010-APP relates to this write, owner solution architect, GAP-3525.
5. **Late at 05:30.** The run writes one AceDataLate outbox row for each due source system with no COMPLETED row for the expected business date, at most once per source and business date. The operations Load late alert and the gateway-bff banner follow it. Pending: the status value when the source has no batch row at all, owner solution architect (GAP-3430); completedAt is null.
6. **Stale at expected_by.** A durable timer per product checks the expected business date at data_product.expected_by (08:00 Asia/Bangkok for daily products, Monday 08:00 for DP06). If no LOADED row exists for that date, the latest earlier row (the stamp in use) is set STALE with stale_flagged_at, MSG-P1-001 applies and the stale alert is raised. If there is no earlier row, nothing is written and the read answers businessDate null, status STALE. This check writes no second AceDataLate. A weekly product is not checked between cycle days. Pending: which run holds the Monday timer of DP06, because the 05:30 start is for the previous bank business day (GAP-3288).
7. **Failed source.** A FAILED row marks the affected stamp STALE at once and writes one AceDataLate for that source and date: where the date has no stamp, the stamp in use is marked; where a COMPLETED source changes to FAILED, the rows of that date are marked. When the source set later completes, a new LOADED row is written and an earlier STALE row stays as history.
8. **Repeats and order.** An unchanged reread changes nothing. A changed completed_at after a date is stamped increments duplicate_count on each product row of that date, keeps the original stamp times, writes no event and raises the duplicate alert. An older date that completes after a newer date is stamped as history, never becomes the stamp in use and writes no AceDataReady.
9. **Gate.** DailyCompletenessGate.check(businessDate, productCodes) checks the sources mapped to the job's DAILY products (JOB-02, JOB-04, JOB-07, JOB-08). It returns COMPLETE only when every required source is COMPLETED; otherwise HOLD names the blocking product and source, is recorded in the owning run and raises MSG-P1-001.
10. **Children.** In the workflow task that commits the ALS stamp, AceIngestCheck starts ReconciliationWorkflow (recon-{businessDate}) and Stage2ProductWorkflow (stage2-dp04-{businessDate}) as child workflows with ParentClosePolicy ABANDON. rwb-source-data does not consume its own topic. Daily jobs of other services start only on AceDataReady with sourceSystem ALS and status COMPLETED. There is no case-list child workflow or P1 case-list read.
11. **Consumers.** Consumers read freshness through the contract (FreshnessQuery, GET /data-products/freshness). P7 writes its own snapshot; when P1 answers 503 or does not answer within 2 s, P7 keeps the snapshot already written unchanged (behaviour and criterion belong to the P7 story).
12. **Flag off.** With rwb.dataengine.freshness-stamp off, a started run writes no stamp, writes no event and starts no child; readiness status is LATE; freshness answers STALE with businessDate null and MSG-P1-001; the alert rules of the feature are not armed (RD-P1-043).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Expected date has no complete source set at expected_by | The stamp in use becomes STALE; if none exists, no row is written | MSG-P1-001 | AC15, AC33 |
| X2 | A mapped source reads FAILED | The affected stamp becomes STALE at once; one AceDataLate; the daily gate answers HOLD | MSG-P1-001 | AC16, AC38 |
| X3 | An unchanged COMPLETED row is read again | No row, counter or event changes | None | AC17 |
| X4 | A late batch completes after the stale flag | A new LOADED row for that date and AceDataReady; the STALE row stays as history | None | AC18 |
| X5 | A batch completes just before, or exactly at, expected_by | 07:59 is on time and the product is not flagged; 08:00:00 is late | MSG-P1-001 when late | AC19, AC39 |
| X6 | A weekly product is checked between cycle days | It remains LOADED and no late event is written | None | AC8 |
| X7 | One source of a multi-source product is late | No row for that date until all mapped sources complete; the stamp in use turns STALE at expected_by | MSG-P1-001 | AC20 |
| X8 | A source not mapped to the job's products is incomplete | It does not hold that job's gate | None | AC21 |
| X9 | A caller lacks the right or sends a bad query | Refused with the published Problem body | MSG-P4-001, MSG-P4-002, MSG-GEN-007 | AC22, AC23; TC-P1-E1015-APP-18 |
| X10 | P7 reads while P1 is unavailable | The call answers 503 or times out at 2 s; P7 shows its written snapshot unchanged; nothing is recomputed or guessed | MSG-GEN-006 | Criterion owned by the P7 story |
| X11 | The outbox relay cannot reach Kafka | The stamp stands; the outbox row is kept and retried | None | RWB-P1-E1015-OPS AC20 |
| X12 | DP14 holiday view is unreadable | The previous calendar day is used for the expected date and MSG-GEN-006 is logged (ASM-5700) | MSG-GEN-006 | AC37 |
| X13 | A restated or out-of-order batch arrives | duplicate_count or a history row only; the stamp in use never moves backwards | None | AC35 |
| X14 | The ACE view or the store is unavailable | No value is inferred and nothing is written; a read with the store down answers 503 | MSG-GEN-006 | AC31 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published contract of RWB-P1-E1015-CON and its fakes, on the tables of RWB-P1-E1001-APP and the views of RWB-P1-E1069-APP |
| Negotiable | Expected-by times, refresh cycles and the product-to-source map are data rows; the story fixes the stamping, the stale check and the gate |
| Valuable | Every decision and case record can show the age of its data, and daily jobs receive a COMPLETE or HOLD result for their mapped source set |
| Estimable | One workflow, four activities, one repository, one gate, one REST operation, one panel |
| Small | Finished inside two weeks with its tests |
| Testable | Each criterion runs against a test clock and synthetic batch rows, plus one component test of the panel states |

### 7. Acceptance criteria

```gherkin
Feature: Freshness stamp per data product

  Background:
    Given the E1015 contract baseline is version 5.1.0
    Given DP01 is DAILY with expected_by 08:00 Asia/Bangkok and is mapped to ALS in data_product_source
    Given DP06 is WEEKLY with expected_by Monday 08:00 and is mapped to CCMS, SVAF, AMIS and RPS

  Scenario: AC3 Freshness values are returned to a consumer
    Given DP01 is LOADED for 2026-11-30 with loadedAt 2026-12-01T05:41+07:00
    Given DP06 is LOADED for 2026-11-23 with loadedAt 2026-11-24T04:40+07:00
    When FreshnessQuery.stampsFor([DP01, DP06]) is called
    Then exactly those two stamps are returned with status LOADED
    And P1 writes no row and no decision snapshot

  Scenario: AC8 Weekly product between cycle days
    Given DP06 is LOADED for business date 2026-11-30, a Monday
    When the stale check is called directly for DP06 at 2026-12-03T08:00+07:00
    Then DP06 remains LOADED with stale_flagged_at empty and no AceDataLate is added to outbox_event

  Scenario: AC12 Freshness comes only from the ACE batch view
    Given DP01 is LOADED for 2026-11-27 and ALS has no COMPLETED row for 2026-11-30
    Given the ACE account facts show data_as_of 2026-11-30 and a row count
    When the 2026-12-01T08:00+07:00 timer fires
    Then the 2026-11-27 row is STALE and no row for 2026-11-30 is written
    And no stamp is inferred from data_as_of, a row count or a file

  Scenario: AC13 Workbench writes no ACE data
    Given a COMPLETED ACE batch row is available
    When its stamp transaction commits
    Then only data_product_load (DF-OPS-001 to DF-OPS-009) and outbox_event rows are written
    And a write to a recovery object by the rwb_source_data login is refused

  Scenario: AC14 One workflow run per business date and one late-check Schedule
    Given run ace-ingest-check-2026-11-30 is open, started by the readiness handler
    When the Schedule rwb-source-data-ace-late-check fires at 2026-12-01T05:30+07:00
    Then USE_EXISTING joins the open run, no second run starts and rwb_source_data_duplicate_start_total rises by 1
    And no per-product Schedule and no publish activity is registered

  Scenario: AC15 Expected date reaches the 08:00 cut-off
    Given DP01 is LOADED for 2026-11-27 and ALS has no COMPLETED row for 2026-11-30
    Given one AceDataLate for ALS and 2026-11-30 was written at 05:30
    When the 2026-12-01T08:00+07:00 timer fires
    Then the 2026-11-27 row is STALE with stale_flagged_at 2026-12-01T08:00+07:00
    And outbox_event still holds one AceDataLate for ALS and 2026-11-30 and no AceDataReady
    And the stale alert carries MSG-P1-001 with the productName of DP01 and the date 2026-11-27
    And GET /data-products/freshness?product=DP01 returns businessDate 2026-11-27, status STALE, staleSince 2026-11-30

  Scenario: AC16 A mapped source fails after completion
    Given ALS 2026-11-30 was COMPLETED and its DP01 stamp is LOADED
    When the source row changes to FAILED
    Then the 2026-11-30 DP01 row is STALE with stale_flagged_at set
    And one AceDataLate with sourceSystem ALS, businessDate 2026-11-30 and status FAILED is added and no AceDataReady is added
    And the stale alert carries MSG-P1-001

  Scenario: AC17 Unchanged batch row is reread
    Given ALS 2026-11-30 is stamped with duplicate_count 0
    When the next poll reads the same COMPLETED row with the same completed_at
    Then no data_product_load column changes, duplicate_count stays 0, no outbox row is added and no alert is raised

  Scenario: AC18 Late batch completes after the stale flag
    Given the DP01 row for 2026-11-27 is STALE and no 2026-11-30 row exists
    When ALS 2026-11-30 completes at 2026-12-01T08:40+07:00
    Then a DP01 row for 2026-11-30 is LOADED with sourceExtractedAt 2026-12-01T08:40+07:00
    And one AceDataReady for ALS, 2026-11-30, COMPLETED is added and recon-2026-11-30 starts as a child workflow
    And the 2026-11-27 row stays STALE with its stale_flagged_at

  Scenario: AC19 A batch completes one minute before expected_by
    Given one AceDataLate for ALS and 2026-11-30 was written at 05:30
    Given ALS 2026-11-30 completes at 2026-12-01T07:59:00+07:00
    When the 08:00 timer fires
    Then DP01 is LOADED for 2026-11-30, no row is set STALE and no further AceDataLate is added

  Scenario: AC20 One source of a multi-source product is late
    Given DP06 is LOADED for 2026-11-23, and CCMS, AMIS and RPS are COMPLETED for 2026-11-30 while SVAF is not
    When the DP06 stale check runs at 2026-11-30T08:00+07:00
    Then no DP06 row for 2026-11-30 is written and the 2026-11-23 row is STALE
    And a DP06 row for 2026-11-30 is written LOADED only after SVAF is COMPLETED

  Scenario: AC21 Gate ignores sources outside the job's products
    Given DP01 maps to ALS and DP13 maps to ALS and GL
    Given ALS and GL are COMPLETED for 2026-11-30 while SVAF is not
    When DailyCompletenessGate.check(2026-11-30, [DP01, DP13]) runs
    Then it returns COMPLETE and the gate marks no row STALE

  Scenario: AC22 Read without Case record R is refused
    Given a signed-in user whose role does not hold Case record R
    When the user calls GET /data-products/freshness
    Then the response is 403 with messageCode MSG-P4-002 and no freshness data
    And the refusal is counted and no alert is paged

  Scenario: AC23 Authentication and product validation use the contract
    Given three calls: no session, a role without Case record R, and a valid reader with product=DP99
    When each calls GET /data-products/freshness
    Then the responses are 401 MSG-P4-001, 403 MSG-P4-002 and 400 MSG-GEN-007 as application/problem+json

  Scenario: AC24 A repeated start joins the open run
    Given run ace-ingest-check-2026-11-30 is open, started by the readiness handler
    When the handler starts the workflow again for 2026-11-30 with startedBy AIRFLOW
    Then no second run starts and rwb_source_data_duplicate_start_total rises by 1

  Scenario: AC25 Retried stamp activity does not duplicate rows or events
    Given stampProducts committed the product rows and the AceDataReady outbox row, and the attempt then failed before reporting
    When the activity is retried under the 1 s, back-off 2, 10 attempts policy
    Then one row per product and date and one AceDataReady outbox row remain, and duplicate_count is unchanged

  Scenario: AC26 A status outside the list is refused
    Given a DP01 data_product_load row has status LOADED
    When a write sets its status to CURRENT
    Then the write is refused because DF-OPS-007 takes only LOV-FRESHNESS values LOADED and STALE, and the row stays LOADED

  Scenario: AC27 Stamp values from a COMPLETED batch
    Given ALS 2026-11-30 started at 2026-11-30T23:30+07:00 and completed at 2026-12-01T05:40+07:00
    When DP01 is stamped at 2026-12-01T05:41+07:00
    Then the row holds source_system ALS, source_extracted_at 05:40, loaded_at 05:41, status LOADED and duplicate_count 0
    And one AceDataReady outbox row is written in the same transaction

  Scenario: AC28 Gate holds for a required failed source
    Given EFS is FAILED for 2026-11-30 and DP05 is in the job's product set
    When DailyCompletenessGate.check(2026-11-30, [DP01, DP05]) runs
    Then it returns HOLD naming DP05 and EFS, the result is recorded in the owning run and MSG-P1-001 is raised

  Scenario: AC29 The readiness start opens the business-date run
    Given no open run exists for 2026-11-30
    When the readiness handler starts AceIngestCheck with input {businessDate 2026-11-30, startedBy AIRFLOW}
    Then one run ace-ingest-check-2026-11-30 starts on task queue rwb-source-data and reads v_ace_batch_status

  Scenario: AC30 A refused readiness call starts no run
    Given POST /business-days/2026-11-30/ready has no Idempotency-Key
    When the handler of RWB-P1-E1013-APP validates it
    Then it answers 400 MSG-PLT-N009-03 and no AceIngestCheck run exists for 2026-11-30

  Scenario: AC31 ACE view or store failure creates no guessed stamp
    Given v_ace_batch_status cannot be read
    When readBatchStatus fails on all 10 attempts
    Then no data_product_load row or outbox row is written or changed and the dependency alert carries MSG-GEN-006
    And with the store unreachable GET /data-products/freshness answers 503 MSG-GEN-006

  Scenario: AC32 Multi-product transaction rolls back atomically
    Given GL is COMPLETED for 2026-11-30, ALS then completes DP01 and DP13, and the DP13 write fails
    When stampProducts runs
    Then neither product row nor any outbox row is committed

  Scenario: AC33 Never-stamped product
    Given no data_product_load row exists for DP05
    When freshness is read for DP05
    Then productCode is DP05, businessDate is null, status is STALE and no sourceExtractedAt or loadedAt is returned

  Scenario: AC34 Concurrent completion and stale timer
    Given ALS 2026-11-30 completes while the 08:00 stale check for DP01 is running
    When both commit
    Then the committed row for 2026-11-30 is LOADED and no AceDataLate is written after its AceDataReady

  Scenario: AC35 Restated and out-of-order batches do not move freshness backwards
    Given DP01 is LOADED for 2026-11-30 with duplicate_count 0 and has no row for 2026-11-26
    When ALS 2026-11-30 is read COMPLETED with a different completed_at, and ALS 2026-11-26 then completes
    Then duplicate_count of the 2026-11-30 row is 1, its stamp times are unchanged, no event is added and the duplicate alert is raised
    And 2026-11-26 is stamped as history, adds no AceDataReady and does not replace the stamp in use

  Scenario: AC36 Case panel shows the freshness states
    Given SCR-03 loads its data panel through the composite route
    When DP01 is returned STALE with businessDate 2026-11-27
    Then the panel shows productName, businessDate, loadedAt, status and MSG-P1-001 "Account and arrears is from 2026-11-27. Today's load has not arrived."
    And a 503 answer shows the error state with MSG-GEN-006, and a 403 answer shows the no-access state with MSG-P4-002

  Scenario: AC37 Holiday view fallback uses the previous calendar day
    Given the DP14 holiday view is unreadable on 2026-12-01
    When the expected business date of a DAILY product is computed
    Then it is 2026-11-30 and MSG-GEN-006 is logged

  Scenario: AC38 A source fails before the date is stamped
    Given DP01 is LOADED for 2026-11-27 and has no row for 2026-11-30
    When ALS 2026-11-30 reads FAILED at 2026-12-01T05:20+07:00
    Then the 2026-11-27 row is STALE at once, no 2026-11-30 row is written and one AceDataLate for ALS and 2026-11-30 is added
    And the 05:30 check adds no second AceDataLate
    And DailyCompletenessGate.check(2026-11-30, [DP01]) returns HOLD naming DP01 and ALS

  Scenario: AC39 Completion exactly at expected_by is late
    Given DP01 is LOADED for 2026-11-27 and ALS 2026-11-30 has completed_at 2026-12-01T08:00:00+07:00
    When the 08:00 check and the next read of the batch row have run
    Then the 2026-11-27 row is STALE with stale_flagged_at set and a 2026-11-30 row is LOADED

  Scenario: AC40 Section B flag off
    Given rwb.dataengine.freshness-stamp is off
    When a run starts for 2026-11-30 and freshness is read
    Then no data_product_load row, outbox row or child workflow is created and readiness status is LATE
    And each product reads status STALE with businessDate null

  Scenario: AC41 Late event at 05:30
    Given ALS has no COMPLETED row for 2026-11-30
    When the 2026-12-01T05:30+07:00 check runs
    Then one AceDataLate with key ALS:2026-11-30, ce_subject ALS and completedAt null is added to outbox_event
    And no data_product_load row changes and a later poll adds no second AceDataLate
```

For every criterion above, the Test Cases v9 row is listed in section 16.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Only COMPLETED rows of v_ace_batch_status produce a stamp, one per product and business date; the stamp and the AceDataReady outbox row commit together | REQ-RDF-009; BR-P1-014-2; RD-P1-003, RD-P1-041 |
| BR2 | A product with no complete source set for its expected business date by expected_by is stale. DAILY: the latest bank business day strictly before the check date in Asia/Bangkok (DP14 v_ace_holiday; if unreadable, the previous calendar day, logging MSG-GEN-006, ASM-5700). WEEKLY: the most recent cycle day on or before the check. On time means completed_at < expected_by; exactly 08:00:00 is late | DL11; RD-P1-041 |
| BR3 | A failed ACE batch marks the affected stamp STALE at once and leaves earlier stamps as history; AceDataLate is written once for that source and date | BR-P1-014; EV-27; RD-P1-041 |
| BR4 | A product fed by more than one source is stamped for a date only when every source mapped in data_product_source is COMPLETED for it, so the stamp in use never claims a date a source has not reached. source_system, source_extracted_at and loaded_at follow flow step 4 | BR-P1-014-3; RD-P1-005, RD-P1-021, RD-P1-041 |
| BR5 | Every decision records, in its inputs snapshot, the product, business date, load time and status of each data product it read; the snapshot is P7's and is filled from FreshnessQuery | REQ-RDF-009; FEAT-DRI-12; DF-DEC-008 |
| BR6 | An unchanged reread is not a repeat. A restatement with a different completed_at is counted in duplicate_count, keeps the original stamp times and writes no event | R-UNI-40; RD-P1-041 |
| BR7 | Expected-by times, refresh cycles and the product-to-source map are data rows, not code | DT02; RD-P1-021, RD-P1-028 |
| BR8 | No daily job starts until every source mapped to the DAILY products it reads (JOB-02, JOB-04, JOB-07, JOB-08) is COMPLETED for the date; otherwise the job is held and the data steward is alerted | BR-P1-014-4; RD-P1-041 |
| BR9 | Freshness is read from v_ace_batch_status only; it is never inferred from data_as_of, a row count or a file | BR-P1-014-2 |
| BR10 | The Workbench writes no ACE data; its freshness rows carry product and source codes and times only | D-RCV-35 U4; CTL-11 |
| BR11 | AceIngestCheck runs once per business date with ID ace-ingest-check-{businessDate}; system starts use USE_EXISTING and ALLOW_DUPLICATE; one 05:30 Schedule plus durable expected_by timers, no per-product Schedule | RD-P1-022, RD-P1-040 |
| BR12 | AceDataReady and AceDataLate go through the transactional outbox with camelCase payloads and key {sourceSystem}:{businessDate}; P1 does not consume its own topic | RD-P1-003, RD-P1-040 |
| BR13 | The stamp in use is the row with the greatest business_date. A late completion adds a LOADED row and keeps the earlier STALE row; an older date never replaces it | RD-P1-041 |
| BR14 | AceDataLate is written at most once per source and business date, at 05:30 or at once on FAILED; the stale timers add none | RD-P1-040, RD-P1-041 |
| BR15 | Only this story writes data_product_load, including status, stale_flagged_at and duplicate_count | RD-P1-041 |

**Open decisions.** DL06, DL10, DL11 and DL43 apply. DL11 values (08:00, Monday 08:00) are used; DL43 recommended answer A is the planning basis (RD-P1-043; ASM-5703). Thai message texts follow DL10.

### 9. State transitions

This story changes no case status. A product with no earlier stamp has no row; FreshnessQuery returns businessDate null and status STALE.

| From | To | Trigger |
|---|---|---|
| No row for product and date | LOADED | Every mapped source is COMPLETED; stamp and AceDataReady outbox row commit atomically |
| Stamp in use, LOADED | STALE with stale_flagged_at | expected_by passes without a LOADED row for the expected date, or a source of the expected date reads FAILED |
| LOADED row of date D | STALE with stale_flagged_at | A source of D changes from COMPLETED to FAILED |
| No earlier row | No row | The expected date is missing or failed; nothing is fabricated |
| Earlier STALE row | Unchanged; a later date's row is LOADED | The late source set completes; the earlier row stays STALE as history |
| LOADED row | Unchanged | The same batch values are read again |
| LOADED row | LOADED, duplicate_count + 1 | A restatement has a different completed_at; original times kept, no event |
| Newer date in use | Older row added as history | An older date completes out of order; no AceDataReady |
| Workflow running | Closed | Every due source is stamped, or 24 h after the start |
| Activity failed | Retried | A transaction fails; all its stamp and outbox writes roll back together |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-source-data service identity (rwb_source_data login) | Read ACE views; write P1 freshness rows and event outbox records; run AceIngestCheck and DailyCompletenessGate |
| rwb-decision service identity | Read freshness through the published contract and write its own decision snapshot |
| Roles with Case record R, for example RW-CASEOWN and RW-TEAMMGR | Read freshness through GET /data-products/freshness and the case record panel |
| Readiness caller (workload identity, Platform administration U) | Call POST /business-days/{date}/ready, served by RWB-P1-E1013-APP |
| RW-DATASTEW, data steward | Receive stale and gate-hold alerts |
| RW-PLATADM, platform administrator | Receive operations alerts |

Roles and their rights are data in rwb-access, reached through its authorise contract and never by table read. Exact workload identity identifiers and their grants are pending with the solution architect (GAP-3433). No service reads another service's tables.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-178 | v_ace_batch_status | source_system | Read |
| DF-ACE-179 | v_ace_batch_status | business_date | Read |
| DF-ACE-180 | v_ace_batch_status | started_at | Read |
| DF-ACE-181 | v_ace_batch_status | completed_at | Read |
| DF-ACE-182 | v_ace_batch_status | status | Read |
| DF-ACE-183 | v_ace_batch_status | record_count | Read |
| DF-ACE-184 | v_ace_batch_status | checksum | Read |
| DF-ACE-185 | v_ace_batch_status | feed_version | Read |
| DF-ACE-186 | v_ace_batch_status | is_complete | Read |
| DF-REF-071 | data_product | product_code | Read |
| DF-REF-072 | data_product | product_name | Read |
| DF-REF-077 | data_product | refresh_cycle | Read |
| DF-REF-078 | data_product | expected_by | Read |
| DF-REF-300 | data_product_source | id | Read |
| DF-REF-301 | data_product_source | product_code | Read |
| DF-REF-302 | data_product_source | source_system | Read |
| DF-OPS-001 | data_product_load | id | Write |
| DF-OPS-002 | data_product_load | product_code | Write |
| DF-OPS-003 | data_product_load | source_system | Write |
| DF-OPS-004 | data_product_load | business_date | Write |
| DF-OPS-005 | data_product_load | source_extracted_at | Write |
| DF-OPS-006 | data_product_load | loaded_at | Write |
| DF-OPS-007 | data_product_load | status (LOV-FRESHNESS: LOADED, STALE) | Write |
| DF-OPS-008 | data_product_load | stale_flagged_at | Write |
| DF-OPS-009 | data_product_load | duplicate_count | Write |
| No Field ID cited | v_ace_holiday | Holiday dates for the expected business date | Read |
| DF-DEC-008 | decision_log_entry | inputs_ref | Written by P7 from the freshness contract; never read or written here |

Seeded product-to-source map (Proposed, RD-P1-021; codes to be confirmed, ASM-5695): DP01 ALS; DP02 SCBPDM and the core bank; DP04 the core bank; DP05 EFS; DP06 CCMS, SVAF, AMIS, RPS; DP07 LIT, WIN; DP11 COLLINS; DP13 ALS, GL. DP03, DP08, DP09, DP10, DP12 and DP14 have no row and are never STALE.

source_extracted_at is the latest completed_at among the product's sources for that date; loaded_at is the instant the Workbench records the stamp (RD-P1-005). For a never-stamped product the contract returns businessDate null and status STALE. Wire property staleSince is a date: the first business date with no completed batch, null when LOADED. The event data are sourceSystem, businessDate, status and nullable completedAt; eventId, occurredAt and schemaVersion are CloudEvents attributes (RD-P1-003). Pending: the event allows sourceSystem up to 10 characters while DF-REF-302 allows 20; owner data architect (GAP-3436).

### 12. Contract

#### 12.1 REST operations

Owner rwb-source-data (P1); base /api/recovery/source-data/v1; baseline rwb-source-data.yaml 5.1.0 (API Specification v7). Shapes are those of RWB-P1-E1015-CON; this story does not restate them.

| Method | Path | Built by | Access |
|---|---|---|---|
| GET | /data-products/freshness (queries product and asOf) | This story | Case record R |
| POST | /business-days/{date}/ready | RWB-P1-E1013-APP; starts this story's workflow | Platform administration U |
| GET | /business-days/{date}/status | RWB-P1-E1013-APP | Platform administration R |
| Pending (GAP-3274) | Account-page read used by rwb-case | RWB-P1-E1002-APP | Pending (GAP-3438) |

The freshness read answers 200 with DataProductFreshness[]; 400 MSG-GEN-007 for a product value outside DP01 to DP14; 401 MSG-P4-001; 403 MSG-P4-002; 503 MSG-GEN-006; all errors use the shared Problem body (RD-P1-004). Without asOf it returns the stamp in use per product. Pending: asOf meaning and format, ordering, and whether the products with no source appear (GAP-3432). The gate answer COMPLETE or HOLD is owned by DailyCompletenessGate and returned through this read (RD-P1-005); the published array has no member for it yet (GAP-3434). The version 2 alias GET /freshness is not in rwb-source-data.yaml 5.1.0 and is not built.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | /api/recovery/access/v1/authorise | P4 rwb-access | Authorise a read; one hop, 2 s client budget. The path is not yet published in rwb-access.yaml (GAP-3322) |

Reference changes reach P1 as reference loads through the apply handler of RWB-P3-E1043-CON; there is no run-time call for the product-to-source map. ACE facts are read only through recovery.v_ace_* views.

#### 12.3 Events published

| Event | Topic | Trigger | Key and payload |
|---|---|---|---|
| rwb.source-data.AceDataReady.v1 (EV-26) | rwb.source-data.events.v1 | Once per source system and business date when the batch is COMPLETED and its products are stamped | Key {sourceSystem}:{businessDate}; ce_subject is sourceSystem; data {sourceSystem, businessDate, status, completedAt} |
| rwb.source-data.AceDataLate.v1 (EV-27) | rwb.source-data.events.v1 | Once per due source system and business date: at 05:30 Asia/Bangkok when not COMPLETED, or at once when FAILED | Same key and four fields; completedAt is null when no batch completed |

Payload fields are camelCase. status is the v_ace_batch_status value copied unchanged; its value when no batch row exists is pending (GAP-3430). eventId, occurredAt and schemaVersion are not data fields: they are ce_id, ce_time and the .v1 of the event type. Both outbox rows are written in the freshness transaction; there are no publish activities. Topic consumers (Kafka catalog v3): rwb-case, rwb-payment, rwb-deviation, rwb-writeoff, the alerts and gateway-bff; P1 is not one.

#### 12.4 Events consumed

None from rwb.source-data.events.v1. The ledger-intake topics of P1 are deployed by RWB-P1-E1066-OPS and are outside this freshness flow.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AceIngestCheck | Workflow, one run per business date, ID ace-ingest-check-{businessDate} | rwb-source-data | Input {businessDate, startedBy}; started by the readiness handler, the 05:30 Schedule or the flagged fallback poll; USE_EXISTING + ALLOW_DUPLICATE |
| readBatchStatus(businessDate) | Activity | rwb-source-data | Reads the ACE batch status view for every mapped source |
| stampProducts | Activity | rwb-source-data | Writes complete product stamps and AceDataReady outbox rows atomically |
| markStale | Activity | rwb-source-data | Marks the stamp STALE at expected_by or on FAILED; writes no row for a missing date |
| checkDailyCompleteness | Activity | rwb-source-data | Checks the mapped sources for the job's product codes and returns COMPLETE or HOLD |

All activities retry with 1 s initial interval, back-off 2 and 10 attempts. Typed activity inputs and outputs beyond readBatchStatus, and the signatures of FreshnessQuery.stampFor and stampForRow, are pending (GAP-3437). FreshnessQuery and DailyCompletenessGate are typed interfaces of the contract jar.

#### 12.6 Schedules and timers

| Schedule or timer | Cadence | Registration and conditions | Owner |
|---|---|---|---|
| rwb-source-data-ace-late-check | 05:30 Asia/Bangkok | Registered by RWB-P1-E1015-OPS; overlap SKIP; catch-up window 1 h | P1 |
| Product expected-by timers | data_product.expected_by; daily, or the DP06 cycle day | Durable timers inside AceIngestCheck; no per-product Schedule | P1 |
| Control-M fallback poll | Start time pending (GAP-3277) | Flag rwb.source-data.ingest-poll-fallback; off whenever Airflow is live; until GAP-3277 closes, DEV only; joins the business-date run | Bank platform team |

#### 12.7 Tables owned or read

| Table or view | Owner | Use |
|---|---|---|
| data_product_load | P1 (rwb_source_data) | Written only here |
| data_product, data_product_source | P1 (rwb_source_data) | Read: names, cycles, expected-by and source map |
| outbox_event | Platform library in rwb_source_data | Transactional event delivery |
| decision_log_entry | P7 (rwb_decision) | Never read or written here; P7 owns its snapshot |
| v_ace_batch_status, v_ace_holiday | ACE views | Read only through the P1 service login |

#### 12.8 Contract fakes

| Fake | Serves | Used for |
|---|---|---|
| rwb-source-data provider fake, fakes/rwb-source-data/5.1.0/ (RWB-P1-E1015-CON; path is a working value, ASM-5690; publication pending) | Freshness, readiness and both event samples | Contract tests and consumers |
| rwb-decision contract mock (RWB-P7-E1027-CON) | The inputs snapshot read | The freshness regression of TC-P1-E1015-APP-16 |
| rwb-access fake | Granted and refused authorise answers | AC22, AC23 |
| Workflow kit fake (RWB-PLT-E1071-CON) | Schedule registration, timers and activity retry with a test clock | Timer and retry criteria |
| Event platform fake (RWB-PLT-TE006-CON) | Outbox and CloudEvents envelope | Event criteria |
| Reference-load apply fake (RWB-P3-E1043-CON) | A new version of the product-to-source map | Map change test |
| gateway-bff composite route fake (RWB-PLT-N001-CON) | The data panel route | AC36 |

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | Freshness read | rwb-access authorise | One hop, 2 s; readiness pair and account read are built by other stories |
| Kafka | Two event types | None on its own topic | Transactional outbox |
| Temporal | One workflow, four activities, one 05:30 Schedule and durable timers | None | rwb-source-data in rwb-recovery |
| File | None | None | ACE status is read through its view |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata.freshness`, with the published types in `...sourcedata.freshness.api`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | Legacy service login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*` | The service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-load apply handler of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AceIngestCheckWorkflow (registered type AceIngestCheck) | Workflow | One run per business date; polling, timers and child starts |
| readBatchStatus, stampProducts, markStale, checkDailyCompleteness | Activities | Read the view; write stamps, stale flags and outbox rows; answer the gate |
| FreshnessStampService | Service | The stamping rules of section 8 |
| DailyCompletenessGateImpl | Service | DailyCompletenessGate over v_ace_batch_status and data_product_source |
| DataProductLoadRepository | Repository | Reads and writes data_product_load; no statement names another service's schema |
| FreshnessController | Controller | GET /data-products/freshness |
| DataFreshnessPanel | React component | Data panel on SCR-03 through the composite route |

**Database.** data_product_load exists from RWB-P1-E1001-APP with its unique key on (product_code, business_date); the next free migration on the service sequence adds index (product_code, loaded_at desc). No new table.

**Build steps**

1. The index migration and DataProductLoadRepository with its unique key.
2. The business-date workflow with its workflow identity, poll timer and retry policy.
3. stampProducts: complete source sets only; freshness and outbox rows in one transaction.
4. markStale, the 05:30 late event and the expected_by timers; the stale, repeat, restatement and out-of-order rules.
5. DailyCompletenessGateImpl over data_product_source; unit test a late source the job does and does not read.
6. FreshnessQuery and FreshnessController.
7. The panel states on SCR-03 against the composite route fake.
8. Tests for the criteria with a fixed test clock, and the access test.

There are no publish activities, no per-product cut-off Schedules, no view listener and no P1 case-list objects.

**Feature flag.** rwb.dataengine.freshness-stamp (platform flag library) stays off in SIT, UAT and PROD until the Section B migration is applied and the ACE dependency gate passes (RD-P1-043).

**Done when.** The criteria pass against the published contract and the provider fake, and the delivery items of section 20 are recorded by their owner roles.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | A product is stale, or the gate returns HOLD | {product} is from {date}. Today's load has not arrived. (product = productName; date = business date of the stamp in use) |
| MSG-GEN-006 | Store or ACE view unavailable; holiday view unreadable (log) | {system} is not available. Try again in a few minutes. |
| MSG-GEN-007 | product value outside its list | {value} is not a valid value for {field}. Choose a value from the list. |
| MSG-GEN-001 | Malformed date or required value missing | Enter {field}. |
| MSG-P4-001 | No valid session, or no Recovery Workbench role (401) | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | Signed-in role lacks Case record R | You cannot {action} here. Your role does not include it. |
| MSG-PLT-N009-03 | Readiness POST without a valid Idempotency-Key (RWB-P1-E1013-APP) | The Idempotency-Key header is required and must be valid for {operation}. |

Texts are those of Error and Message Standard v6; Thai text follows DL10. Pending: the {date} wording of MSG-P1-001 for a never-stamped product, which has no business date, owner Error and Message Standard owner (GAP-3284; GAP-3284). Interim: `messageCode` MSG-P1-001 with `{product}` filled and `{date}` empty; tests assert the code and the product only (RD-P1-062).

### 15. Screens and states

SCR-03 Case record, state Read only: the data panel shows each product's productName, businessDate, loadedAt and status from the freshness contract, read through the gateway-bff composite route. State Stale input: MSG-P1-001 next to the stale product with its product name and stamp business date. State Loading: skeleton rows. State Error: the freshness read answers 503; the panel shows MSG-GEN-006. State No access: the read answers 403; the panel shows MSG-P4-002. Never stamped: businessDate is null and status STALE; no date is shown (the message text for this case is pending, GAP-3284). State Empty: not specified (CG-ALL-2119). The composite route specification and the panel field list beyond the contract fields remain with RWB-PLT-N001-CON.

The data steward sees stale products and the gate result on SCR-45 Data quality from Epic 2; in Epic 1 the same list comes from GET /data-products/freshness.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P1-E1015-APP-16 | AC3 | End to end | Freshness values are returned to a consumer |
| TC-P1-E1015-APP-17 | AC8 | End to end | Weekly product between cycle days |
| TC-P1-E1015-APP-18 | AC22 | Component | Read without Case record R is refused |
| TC-E1-015-13 | Operations, events and activities of section 12 | Contract | Operations, events and activities of section 12 |
| TC-E1-015-14 | Tables of section 12.7 | Component | Tables of section 12.7 |
| TC-E1-015-15 | AC12 | End to end | Freshness comes only from the ACE batch view |
| TC-E1-015-16 | AC13 | End to end | Workbench writes no ACE data |
| TC-E1-015-17 | AC14 | End to end | One workflow run per business date and one late-check Schedule |
| TC-E1-015-18 | AC15 | End to end | Expected date reaches the 08:00 cut-off |
| TC-E1-015-19 | AC16 | End to end | A mapped source fails after completion |
| TC-E1-015-20 | AC17 | End to end | Unchanged batch row is reread |
| TC-E1-015-21 | AC18 | End to end | Late batch completes after the stale flag |
| TC-E1-015-22 | AC19 | End to end | A batch completes one minute before expected_by |
| TC-E1-015-23 | AC20 | End to end | One source of a multi-source product is late |
| TC-E1-015-24 | AC21 | End to end | Gate ignores sources outside the job's products |
| TC-E1-015-26 | AC23 | Contract | Authentication and product validation use the contract |
| TC-E1-015-27 | AC24 | Component | A repeated start joins the open run |
| TC-E1-015-28 | AC25 | Component | Retried stamp activity does not duplicate rows or events |
| TC-E1-015-29 | AC26 | Component | A status outside the list is refused |
| TC-P1-E1015-APP-01 | AC27 | Component | Stamp values from a COMPLETED batch |
| TC-P1-E1015-APP-02 | AC28 | Component | Gate holds for a required failed source |
| TC-P1-E1015-APP-03 | AC29 | Component | The readiness start opens the business-date run |
| TC-P1-E1015-APP-04 | AC30 | Component | A refused readiness call starts no run |
| TC-P1-E1015-APP-05 | AC31 | Component | ACE view or store failure creates no guessed stamp |
| TC-P1-E1015-APP-06 | AC32 | Component | Multi-product transaction rolls back atomically |
| TC-P1-E1015-APP-07 | AC33 | Component | Never-stamped product |
| TC-P1-E1015-APP-08 | AC34 | Component | Concurrent completion and stale timer |
| TC-P1-E1015-APP-09 | AC35 | Component | Restated and out-of-order batches do not move freshness backwards |
| TC-P1-E1015-APP-10 | AC36 | Component | Case panel shows the freshness states |
| TC-P1-E1015-APP-11 | AC37 | Component | Holiday view fallback uses the previous calendar day |
| TC-P1-E1015-APP-12 | AC38 | Component | A source fails before the date is stamped |
| TC-P1-E1015-APP-13 | AC39 | Component | Completion exactly at expected_by is late |
| TC-P1-E1015-APP-14 | AC40 | Component | Section B flag off |
| TC-P1-E1015-APP-15 | AC41 | Component | Late event at 05:30 |

Legacy criteria AC1, AC2, AC4 to AC7 and AC9 to AC11 are owned by RWB-ITG-E1015-ITG; their component behaviour is asserted here by AC27, AC15, AC38, AC17, AC18, AC19, AC28 and AC20.

### 17. Guardrails

- P1 reads ACE only through recovery.v_ace_* and writes only rwb_source_data.
- No business value in code: expected-by times, refresh cycles, the product-to-source map and the alert channel are data rows or settings.
- Only RWB-P1-E1015-APP writes data_product_load, including status, stale_flagged_at and duplicate_count.
- Never infer freshness from data_as_of, row count or files.
- Keep event payloads to sourceSystem, businessDate, status and completedAt; no personal data in events, logs, tests or workflow inputs.
- Write each event to the outbox in the freshness transaction; do not publish through an activity or consume the service's own topic.
- The stale check never deletes a row or changes its stamp times.
- No cross-schema read and no cross-schema key; a caller reaches the stamps only through the contract.
- No P1 case list, case_list_row, CaseListBuildWorkflow or DailyCaseList is part of this story.

### 18. Traceability

| Requirement ID | Requirement (short) | Owned element | Test cases |
|---|---|---|---|
| REQ-RDF-009 | Freshness stamps come from the ACE batch record; decisions record the freshness of their data | AceIngestCheck, data_product_load and FreshnessQuery | TC-P1-E1015-APP-16 to TC-P1-E1015-APP-18, TC-E1-015-13 to TC-E1-015-24, TC-E1-015-26 to TC-E1-015-29, TC-P1-E1015-APP-01 to TC-P1-E1015-APP-15 |
| BR-P1-014-4 | Daily jobs wait for all mapped sources | DailyCompletenessGate | TC-E1-015-24, TC-P1-E1015-APP-02 |
| ADR-016 | Temporal Schedule replaces Quartz | 05:30 Schedule and durable timers | TC-E1-015-17 |
| ADR-023 | Service observability | Stamp, stale, gate and workflow measures | RWB-P1-E1015-OPS tests |

| Story | Relation to this story |
|---|---|
| RWB-P1-E1015-CON | H: contract, events, workflow and gate declaration, fakes |
| RWB-P1-E1001-APP | H: data_product, data_product_source, data_product_load |
| RWB-P1-E1069-APP | H: read-only ACE views |
| RWB-PLT-E1071-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON | H: workflow kit, outbox, migration sequence |
| RWB-PLT-N001-CON | H: composite route of the data panel |
| RWB-P7-E1027-CON | C: rwb-decision reads the stamps and writes its snapshot |
| RWB-P1-E1013-APP | Neighbour: builds the readiness pair that starts AceIngestCheck |
| RWB-P1-E1011-APP | Neighbour: ReconciliationWorkflow is a child of AceIngestCheck and calls the gate |
| RWB-P1-E1015-OPS | X: deployment, Schedule registration, alerts and runbook |
| RWB-ITG-E1015-ITG | Owns the legacy end-to-end criteria |

### 19. Out of scope

- Readiness record and handler (RWB-P1-E1013-APP); this story implements the workflow they start.
- Contract documents, API schemas, event schemas and published fakes (RWB-P1-E1015-CON).
- Deployment chart, topic verification, Schedule registration, dashboards, alert routing and runbook (RWB-P1-E1015-OPS).
- Decision snapshot storage and decision_log_entry (rwb-decision).
- The MSG-P7-006 warning on a decision screen when an input is past its age limit (decision screens, Epic 2).
- Same-day data for named triggers (DL06).
- The data quality console SCR-45 and the reconciliation report (RWB-P1-E1011-APP, RWB-P1-AD019-APP).
- Freshness of the stage 2 data products (RWB-P1-E2010-APP).
- ACE ingestion, its monitoring and the view definitions (RWB-ACE-001, RWB-P1-E1069-APP).
- Case list ownership and storage (rwb-case; RD-P1-024).

### 20. Remaining delivery steps

- Set story size at refinement; owner: squad.
- Record epic design sign-off; owner: solution architect.
- Complete and baseline RWB-P1-E1015-CON 5.1.0 and publish its provider fake; owner: rwb-source-data tech lead.
- Create and publish synthetic Section B test data in DEV; owner: data engineering and QA.
- Add the Test Cases v9 rows for AC3, AC8 and AC12 to AC41; owner: QA lead.
- Confirm the data_product_source source_system seed against the ACE code list (ASM-5695); owner: ACE team lead.
- Keep the Section B feature flag off in SIT, UAT and PROD until RWB-ACE-001 lands and the dependency gate passes; owner: release owner and ACE team lead.
- Set the Control-M fallback poll start time (GAP-3277); owner: bank platform team with solution architect.
- Restatement detection basis (GAP-3429); owner: solution architect.
- AceDataLate status when no batch row exists (GAP-3430); owner: solution architect.
- Message IDs, recipients and route of the Load late and Load failed alerts, repeat rule of the stale alert and format of {date} (GAP-3431); owner: solution architect with the data steward.
- asOf meaning, ordering and listing of products with no source (GAP-3432); owner: solution architect.
- Workload identity IDs and grants of service callers (GAP-3433); owner: solution architect with the security owner.
- Gate result member of the freshness answer (GAP-3434); owner: solution architect.
- MSG-P1-001 {date} and panel text for a never-stamped product, and the panel empty state (GAP-3284; CG-ALL-2119); owner: screen owner with the Error and Message Standard owner.
- Length of sourceSystem, 10 in the event and 20 in data_product_source (GAP-3436); owner: data architect.
- Typed signatures of activities and FreshnessQuery methods (GAP-3437); owner: rwb-source-data tech lead.
- Publication of the authorise path in rwb-access.yaml (GAP-3322); owner: rwb-access service owner.
- Run that holds the weekly DP06 timer and its late event (GAP-3288); owner: solution architect.

