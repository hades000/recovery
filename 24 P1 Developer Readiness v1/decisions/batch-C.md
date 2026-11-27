# RD-P1 decision register, batch C (RD-P1-040 to RD-P1-048)

Run: D-RCV-60 P1 developer readiness (RD-P1 register). Service epic RWB-SVC-P1 (rwb-source-data). Design sub-agent, solution architect rulings. Date 2026-11-27.

Precedence used throughout (run brief rule 6): D-RCV-60 and Architecture v5 > RD-P1 decisions > 16 Temporal and Drools Adoption (D-RCV-36) > 15 ACE DB Alignment (D-RCV-35, ADR-010) > 14 Story Updates > all other documents. Every clock time is Asia/Bangkok, as in Batch and Scheduling Design v6, sheet Read me R2 and sheet Daily order R2 and R12.

Short names used below: Arch v5 = Recovery Workbench Architecture v5 Text Extract v1 (SET\22); TWAC v2 = Temporal Workflow and Activity Catalog v2; BSD v6 = Batch and Scheduling Design v6; KTEC v2 = Kafka Topic and Event Catalog v2; EDD v6 = Environment and Deployment Design v6; RRA v4 = Records Retention and Archiving v4; DQR v4 = Data Quality and Reconciliation Rules v4; DL v12 = Decision Log v12; NFS v5 = Non Functional Specification v5; OMD v5 = Observability and Monitoring Design v5; ASM v2 = Assumptions Register v2; GAP v2 = Gap Register v2; PS v8 = Physical Schema v8 (`rwb_source_data.sql`).

New gaps: where a ruling needs a value that no source gives and that this run must not choose, the entry says "NEW-GAP-Cn". The orchestrator registers each as the next free GAP number after GAP-3270 and replaces the label.

---

## RD-P1-040 · Daily ingest, case list and reconciliation triggers, hand-offs and workflow IDs

**Question.** What starts AceIngestCheck, CaseListBuildWorkflow and ReconciliationWorkflow? What is the workflow ID grain and the ID reuse policy for each? How do the three runs follow one another, which sourceSystem starts the downstream work, and when is AceDataLate raised (05:30 or 08:00)?

**Options considered.**
- A. Keep the stories as they are. AceIngestCheckWorkflow runs once per source and date, started by a listener on `v_ace_batch_status`, late at 08:00. CaseListBuildWorkflow and ReconciliationWorkflow both consume `rwb.source-data.AceDataReady.v1` with no ordering.
- B. Follow Arch v5 and TWAC v2 R18. There is one AceIngestCheck run per business date, started by `POST /v1/business-days/{date}/ready`, and AceDataLate is raised at 05:30. Inside rwb-source-data the later steps are chained by Temporal child workflows, not by consuming the service's own topic. The poll of the ACE batch record stays as the fallback.
- C. As B, but rwb-source-data also joins EV-26 as a Kafka consumer of its own event.

**Sources.**
- Arch v5, lines 1075–1080 and 1114–1115 (slide 15): `POST /business-days/{date}/ready (Airflow)`; Workflow: AceIngestCheck, reconciliation; `AceDataLate (05:30)`.
- Arch v5, lines 2286–2294 (slide 31): "rwb-source-data still publishes AceDataLate at 05:30 with an alarm and a banner"; "Fallback if ACE ingestion is still on Control-M at go-live: rwb-source-data polls ACE's batch record".
- Arch v5, lines 2341 and 2364 (slide 32): `POST /v1/business-days/{date}/ready → 202, idempotent on the date`; `GET /v1/business-days/{date}/status → RUNNING | DONE | LATE`.
- TWAC v2, sheet Workflows R18 (AceIngestCheck: one run per business date; raises AceDataLate at 05:30) and R19 (reconciliation: one run per business date); sheet Platform rules R8 (parent close policy ABANDON), R16 (overlap SKIP with a catch-up window) and R17 (KEDA on backlog).
- BSD v6, sheet Jobs R8 (JOB-04: "On the ACE batch-complete record, after JOB-02"; mechanism "AceIngestCheck then reconciliation"), R6 (JOB-02 "On the ACE batch-complete record for ALS"), R7 (JOB-03 by 07:00); sheet Daily order R14.
- KTEC v2: sheet Event topics R4 (consumers of `rwb.source-data.events.v1` are rwb-case, rwb-payment, rwb-deviation, rwb-writeoff, alerts and gateway-bff); sheet ACLs R4 (rwb-source-data consumes "None"); sheet Rules R13 (one consumer group per service per topic); EV-26 and EV-27 payloads.
- RWB-P1-E1015-APP v2, s1, s4 steps 1–12 and s12.5–12.6; RWB-P1-E1002-APP v2, s1 and s4 steps 1–7 (`DailyCaseList` 07:15, `caselist.allocation.wait.until` 07:15, check ALLOCATION_COMPLETE through the rwb-case allocation contract); RWB-P1-E1011-APP v2, s4 steps 1–2; RWB-P1-AD019-APP v2, s4 steps 1–4.
- ASM v2: ASM-0689 (recon-{businessDate}, ReconciliationWorkflow, activity reconciliation), ASM-0686 (one cut-off Schedule per product), ASM-0226, ASM-0227 and ASM-0230. GAP v2: GAP-0487, GAP-0494, GAP-0497, GAP-1513, GAP-0142, GAP-0145.
- NFS v5, NFR-013 (case list by 07:00, Proposed, DL43); OMD v5, lines 137–138 and 163–164 (Load late, "not arrived by 07:00").

**Precedence applied.** Arch v5 and TWAC v2 R18, which carries Arch v5 slides 15, 31 and 32, outrank every story. The stories' listener-only trigger, the per-source run grain and the 08:00 AceDataLate are therefore stale. KTEC v2 ACL R4 (rwb-source-data consumes nothing) is consistent with Arch v5 and is kept, so option C is rejected.

**Ruling.** Option B.

1. **AceIngestCheck.**
   - **Type and queue.** Temporal workflow type `AceIngestCheck`, the name in Arch v5 and TWAC v2 R18. The Java interface may be called `AceIngestCheckWorkflow`, but the registered type name is `AceIngestCheck`. It runs on task queue `rwb-source-data` in namespace `rwb-recovery`.
   - **Grain and ID.** One run per business date. Workflow ID `ace-ingest-check-{businessDate}`, where `{businessDate}` is ISO `yyyy-MM-dd`.
   - **Starters.** There are three, all with input `{businessDate, startedBy: AIRFLOW|SCHEDULE|POLL|ADMIN}`:
     - (a) `POST /v1/business-days/{date}/ready` on rwb-source-data. It answers 202 and is idempotent on the date.
     - (b) The Temporal Schedule `rwb-source-data-ace-late-check`, daily at 05:30 Asia/Bangkok, overlap SKIP, catch-up window 1 h. It starts the run for the expected business date (RD-P1-041 item 1) if no run is open, so that AceDataLate is raised even when Airflow never calls.
     - (c) The Control-M fallback poll, behind flag `rwb.source-data.ingest-poll-fallback`, which is off when the Airflow path is live. The time at which the fallback poll starts on a run day is not given by any source: Pending, owner bank platform team with the solution architect, tracked as NEW-GAP-C1. Interim build: the fallback is built and tested in DEV only; in SIT and later it stays off until NEW-GAP-C1 is closed.
   - **ID policy.** All starters use WorkflowIdConflictPolicy `USE_EXISTING` (a start while a run is open joins that run and starts nothing) and WorkflowIdReusePolicy `ALLOW_DUPLICATE` (once a run has closed, a new start opens a new run for the same date).
   - **Polling.** Inside the run, the activity `readBatchStatus(businessDate)` reads `v_ace_batch_status` for every source system in the product-to-source map. A durable timer repeats the read every `ingest.poll.interval.minutes` = 5 (Proposed, matching the five-minute platform checks of Arch v5 slide 32 and JOB-21), until every source due that day is COMPLETED. A source is due on a date when it feeds a DAILY product, or a WEEKLY product whose cycle day that is.
   - **Closing.** The run closes when every due source is COMPLETED and stamped, or 24 h after it started, whichever comes first (Proposed). A batch that arrives after the run has closed is picked up by a new start: a repeated ready call, an ADMIN rerun through `POST /admin/jobs/{jobId}/rerun` (API-P1-002), or the poll.
   - **Status answer.** `GET /v1/business-days/{date}/status` answers RUNNING while the run is open and the ALS batch is not yet stamped, DONE once ALS is stamped, and LATE once AceDataLate has been published for the date with ALS still not COMPLETED.
2. **AceDataReady.**
   - **When published.** One event per source system and business date, in the transaction that stamps that source's batch (RD-P1-041). The EV-26 payload is unchanged: sourceSystem, businessDate, status, completedAt. A source system that is not COMPLETED publishes nothing.
   - **What starts downstream work.** The downstream daily jobs start only on the event with `sourceSystem = ALS` and `status = COMPLETED`. This is BSD v6, JOB-02, JOB-07 and JOB-08: "on the ACE batch-complete record for ALS". Consumers ignore events for other source systems when deciding to start their daily run. This is stated for rwb-case DailyCaseRun, rwb-payment JOB-07 and JOB-08, rwb-deviation and rwb-writeoff. P1 does not edit those stories; the orchestrator routes the change as a REQUEST.
3. **AceDataLate** (Arch v5 outranks the story and ASM-0686).
   - **At 05:30.** AceIngestCheck publishes one AceDataLate per due source system with no COMPLETED row for the expected business date. The alarm and the gateway-bff banner go with it. This replaces the 08:00 AceDataLate of RWB-P1-E1015-APP, E1015-CON and E1015-OPS.
   - **FAILED rows.** A FAILED row publishes AceDataLate at once.
   - **At most once.** AceDataLate is published at most once per source system and business date.
   - **Stale flag.** The per-product stale flag at `data_product.expected_by` (08:00 for daily products, MON 08:00 for DP06, under DL11) remains, but it publishes no second AceDataLate (RD-P1-041 item 4).
   - **Alert timing.** The P1 "Load late" alert instance fires with AceDataLate at 05:30. The 07:00 alert in Arch v5 slides 31 and 32 is Airflow's SLA alert, which the bank platform owns and P1 does not build. OMD v5 lines 138 and 164 ("not arrived by 07:00") are stale for the P1 instance.
   - **Schedules.** The per-product cut-off Schedules of ASM-0686 are replaced by durable timers inside AceIngestCheck plus the one 05:30 Schedule. ASM-0686 is changed.
4. **CaseListBuildWorkflow** (GAP-0487 names kept).
   - **Type, ID and start.** Type `CaseListBuildWorkflow` on `rwb-source-data`, workflow ID `case-list-build-{businessDate}`. AceIngestCheck starts it as a child workflow with ParentClosePolicy `ABANDON` (TWAC v2 Platform rules R8), in the same workflow task in which it commits the ALS stamp. rwb-source-data does not consume its own topic and declares no consumer group on it.
   - **Waiting for allocation.** The run first calls the rwb-case allocation contract for the date every `caselist.allocation.poll.minutes` = 5 (Proposed), using durable timers. It builds as soon as the answer is ALLOCATION_COMPLETE YES, or at `caselist.allocation.wait.until` = 07:15 (legacy value, E1002 s3) with ALLOCATION_COMPLETE NO recorded on the run (X2, AC6).
   - **Fallback Schedule.** `DailyCaseList` stays at 07:15 Asia/Bangkok, overlap SKIP, as the fallback starter when no run for the expected business date exists, with conflict policy `USE_EXISTING` and reuse policy `ALLOW_DUPLICATE`. A Schedule-started run calls `DailyCompletenessGate` first. If the gate answers HOLD, it builds nothing and raises MSG-P1-001.
   - **Rerun.** The admin rerun (`POST /admin/jobs/{jobId}/rerun`, Idempotency-Key) uses conflict policy `FAIL`. A rerun while a run is open returns MSG-P1-011 (E1002 s4 step 2). A rerun after the run has closed starts a new run.
5. **ReconciliationWorkflow** (ASM-0689 confirmed).
   - **Type, ID and start.** Type `ReconciliationWorkflow`, activity `reconciliation`, on `rwb-source-data`, workflow ID `recon-{businessDate}`. CaseListBuildWorkflow starts it as a child workflow with ParentClosePolicy `ABANDON` after `case_list_row` for the date has been committed. The order is therefore ALS stamp, then case creation and allocation in rwb-case, then case list, then reconciliation. This satisfies BSD v6 JOB-04 "after JOB-02" without a race.
   - **Input.** `{businessDate, caseListRunId}`. There is no eventId; a rerun has none (E1011-CON#12).
   - **ID policy.** Conflict policy `USE_EXISTING`, reuse policy `ALLOW_DUPLICATE`. Each case-list rerun starts a new reconciliation run when it completes (E1002-APP#17).
   - **Case list gate.** The AD019 "case list gate retry window" becomes a single check, because the parent guarantees the rows exist. No row for the date fails the run at once with MSG-GEN-006 naming the case list step. That remains possible only for a direct admin start.
   - **Completeness gate.** The gate of AD019 s4 step 3 stays.
6. **Case list deadline** (E1002-OPS#3). The build starts as soon as allocation is complete; JOB-03 completes by 07:00 under BSD v6 R7. 07:15 is the latest start. NFR-013 "by 07:00" stays the target, but it is Proposed under DL43 and is not a test gate. The OPS capacity measure (built and released by 07:30 on 99 percent of days) is kept until the NFS owner moves NFR-013 out of Proposed.
7. **Catalog rows.** TWAC v2 gains or changes these rows:
   - R18: type `AceIngestCheck`, ID `ace-ingest-check-{businessDate}`, the three starters.
   - R19: type `ReconciliationWorkflow`, ID `recon-{businessDate}`, started as a child of CaseListBuildWorkflow.
   - A new workflow row for `CaseListBuildWorkflow`.
   - Two new Schedule rows: `rwb-source-data-ace-late-check` at 05:30 and `DailyCaseList` at 07:15, both owned by P1 on queue `rwb-source-data`.

   BSD v6 JOB-04 and Daily order R14 name the chain. KTEC v2 EV-26 consumers are unchanged (P1 is not added). The pending changes CDC-02650 and CDC-02790, which would add P1 as a consumer, are rejected.

**Rationale.** The architecture fixes one ready call per date and a 05:30 late alarm. Chaining inside the service with child workflows gives a deterministic order: list after allocation, reconciliation after list. It does this without a second consumer group or a self-consumption ACL that KTEC v2 does not grant, and a rerun re-triggers the next step. Conflict policy `USE_EXISTING` makes every system start idempotent. Reuse policy `ALLOW_DUPLICATE` lets a late or corrected batch run again after the first run has closed, which was the failure case of E1015-APP#2.

**Affected.**
- Services: rwb-source-data (P1), rwb-case (P3, consumer filter), rwb-payment (P8), rwb-deviation (S8), rwb-writeoff (S7), gateway-bff (banner).
- Stories: RWB-P1-E1015-APP, RWB-P1-E1015-CON, RWB-P1-E1015-OPS, RWB-P1-E1002-APP, RWB-P1-E1002-CON, RWB-P1-E1002-OPS, RWB-P1-E1011-APP, RWB-P1-E1011-CON, RWB-P1-E1013-APP, RWB-P1-AD018-APP, RWB-P1-AD019-APP.
- Documents: TWAC v2, BSD v6, KTEC v2 (note only), OMD v5 (Load late row), ASM v2 (ASM-0686, ASM-0689), RWB-P1-E1015-CON.

**Findings and themes settled.** TH-21: RWB-P1-E1011-APP#11, RWB-P1-E1015-APP#2, RWB-P1-AD019-APP#5, RWB-P1-AD019-APP#6, RWB-P1-E1011-APP#6, RWB-P1-E1002-APP#16, RWB-P1-E1002-APP#17, RWB-P1-E1013-APP#6, RWB-P1-E1002-APP#7, RWB-P1-E1015-APP#3, RWB-P1-E1013-APP#12, RWB-P1-AD018-APP#12, RWB-P1-E1015-APP#11, RWB-P1-E1015-APP#16, RWB-P1-E1002-CON#14, RWB-P1-E1011-CON#12, RWB-P1-E1015-CON#3, RWB-P1-E1015-CON#11, RWB-P1-E1002-OPS#3, RWB-P1-E1015-OPS#4, RWB-P1-E1015-OPS#14.
- AD018-APP#12: the monitor's job is due when the AceIngestCheck or child run of the date starts. The WAITING row is written by the run while it polls; a new run_no is created by a new run after the previous one closed.
- E1015-APP#11: no Schedule fires on Thursday. AC8 is restated as a direct call of the stale check, and DP06 stays LOADED.
- E1015-OPS#14: overlap SKIP and same-date dedup are separate rules. The dedup is conflict policy `USE_EXISTING`, counted by metric `rwb_source_data_duplicate_start_total` (Proposed).

**GAP and ASM.**
- Closes GAP-0497 (recon workflow ID), GAP-0487 (case list names and the Schedule overlap rule) and GAP-0494 (Schedule names, P1 part).
- Changes ASM-0686 (per-product Schedules replaced by durable timers and the 05:30 Schedule).
- Confirms ASM-0689.
- GAP-1513 stays resolved; ready call and poll are both described.
- Opens NEW-GAP-C1 (fallback poll start time).

**Status.** Proposed – Claude Opus 5.5 (applied).

**Reuse note.** Every later service fix takes these from this ruling:
- Daily work starts on AceDataReady with sourceSystem ALS and status COMPLETED, and on nothing else.
- Every system-started workflow uses conflict policy `USE_EXISTING` and reuse policy `ALLOW_DUPLICATE`; admin reruns use `FAIL`.
- In-service ordering uses child workflows with ABANDON, never a consumer of the service's own topic.
- AceDataLate fires at 05:30.
- Workflow IDs take the form `<kebab-type>-{businessDate}`.

---

## RD-P1-041 · Freshness stamp state model: expected date, multiple sources, repeats, late batches, STALE and the single writer

**Question.** Which row carries STALE when no batch exists? How is a product fed by several sources stamped in a table keyed on product and date with a single source column? What counts as a repeat? What happens to a restated, failed-after-completed or out-of-order batch? Which date is expected, at what instant is a batch late, and which stories may write the stamp?

**Options considered.**
- A. One row per product, date and source. This needs a schema change to the unique key and the read model.
- B. Keep the PS v8 key `uk_data_product_load (product_code, business_date)`. Write the row only when every source of the product is complete for the date, and put STALE on the stamp in use.
- C. Write the row at the first source and update it as other sources arrive.

**Sources.**
- PS v8 `rwb_source_data.sql`, lines 180–198: `data_product_load` with source_system, source_extracted_at and loaded_at NOT NULL, status default LOADED, stale_flagged_at, duplicate_count, unique on (product_code, business_date).
- RWB-P1-E1015-APP v2, s4 steps 3–12, X1–X8, BR2–BR4, BR9 and s9.
- ASM-0684 (started_at to source_extracted_at; completed_at to loaded_at) and ASM-0822 (DP07 delivery repeats).
- DL v12 DL11 (expected-by 08:00 daily, MON 08:00 weekly); BSD v6 JOB-02 ("No cases from a stale business date").
- RWB-P1-E1013-APP v2, s4; RWB-P1-E1055-APP v2, s4 step 8; RWB-P1-E1069-APP v2, s3 and s11; RWB-P1-E2007-APP v2; RWB-P1-E2010-CON v2, AC4; GAP-0511, GAP-0561, GAP-0547, GAP-0580.
- RD-P1-040.

**Precedence applied.** RD-P1-040, which derives from Arch v5, sets the late event at 05:30. PS v8 is kept unchanged because option B needs no schema change, so no DB story is reopened. Where E1013-APP, E1055-APP and E1069-APP write stamp fields, they conflict with E1015-APP's ownership of the stamp, and E1015-APP is kept as the writer.

**Ruling.** Option B.

1. **Expected business date.**
   - **DAILY products.** For a run at instant T in Asia/Bangkok, the expected business date is the latest bank business day strictly before the calendar date of T, using the holiday calendar of DP14 (`v_ace_holiday`). For example, a check on 2026-12-01 expects 2026-11-30.
   - **WEEKLY products.** For DP06 the expected business date is the business date of the most recent cycle day on or before T, the cycle day being the weekday of `data_product.expected_by`. Between cycle days the product is not checked and stays LOADED (X6, AC8).
   - **Missing calendar.** If the holiday calendar is not readable, the check runs on the previous calendar day and logs MSG-GEN-006. Proposed.
2. **On-time boundary.** A batch is on time when `completed_at` < `expected_by` of the expected date, compared to the second in Asia/Bangkok. A `completed_at` of exactly 08:00:00 is late (X5, AC19).
3. **Stamp rows.** These rows are written only by RWB-P1-E1015-APP through AceIngestCheck.
   - **When written.** A row for (product P, business date D) is inserted with status LOADED only once every source system mapped to P has a COMPLETED `v_ace_batch_status` row for D.
   - **Column values.** `source_system` is the source whose completion completed the set (the latest `completed_at`). `source_extracted_at` is the earliest `started_at` among P's sources for D. `loaded_at` is the latest `completed_at`. For a single-source product this reduces to ASM-0684.
   - **Effect.** The stamp in use for P is always the row with the greatest business_date. This is the "oldest business date among its sources" rule (BR4), because D is stamped only when its slowest source is complete.
   - **No other rows.** No row is written for a date that has no complete set.
4. **STALE.**
   - **Triggers.** At P's `expected_by` (a durable timer of AceIngestCheck, per RD-P1-040), if no LOADED row exists for P and the expected date D, the stamp in use (P's latest earlier row) is set to status STALE with `stale_flagged_at`. The same happens at once when any source of P for D reads FAILED.
   - **Notification.** MSG-P1-001 is shown and the stale alert raised. No second AceDataLate is published; AceDataLate is the 05:30 per-source event of RD-P1-040.
   - **No earlier row.** If P has no earlier row, nothing is written. FreshnessQuery then answers P with `businessDate` null, status STALE and MSG-P1-001, which is the never-stamped answer for E1013-APP#15 and E2010-CON#10.
5. **Late batch** (X4, AC18). When D completes later, a new row for D is inserted as LOADED with its own times, AceDataReady goes out for each newly COMPLETED source, and D becomes the stamp in use. The earlier row keeps status STALE and its `stale_flagged_at` as history. AC18 is restated as "the stamp of 2026-11-27 is STALE; then a row for 2026-11-30 is LOADED".
6. **Repeats and restatements.** These apply per (source system, business date).
   - **Unchanged rows.** An unchanged row seen by a later poll or ready call is not a repeat and changes nothing.
   - **Restatement.** A restatement (COMPLETED again with a different `completed_at`) after D is stamped increments `duplicate_count` on each of D's product rows. It keeps the original stamp times, publishes no event and raises the operations duplicate alert (X3, AC17: "no second AceDataReady").
   - **Failed after completed.** COMPLETED then FAILED for D sets D's rows STALE with `stale_flagged_at` and publishes AceDataLate for that source, once per source and date.
   - **Out of order.** An older business date that completes after a newer date has been stamped is stamped as history, but it never becomes the stamp in use and publishes no AceDataReady. This follows BSD v6 JOB-02, "No cases from a stale business date".
   - **Other statuses.** RUNNING rows and rows with `is_complete` false are ignored.
7. **Single writer.**
   - **E1015-APP.** Only RWB-P1-E1015-APP writes `data_product_load`, including status, `stale_flagged_at` and `duplicate_count`.
   - **E1055-APP.** It does not write `duplicate_count`. DP07 delivery repeats (ASM-0822) are counted in its own metric `rwb_source_data_win_delivery_repeat_total` (Proposed), and ASM-0822 is changed accordingly.
   - **Readers.** E1013-APP, E1055-APP (WinBatchGate), E2007-APP and DM001-APP read the stamp through `FreshnessQuery` only. "Marks DP07 STALE" is removed from E1055-APP s13, and its AC2 reads "the latest DP07 stamp in use is returned with status STALE".
   - **E1069-APP.** Its precondition clause that makes it the writer of DF-EXT-041 and DF-EXT-042 is removed, and E1069-APP writes no freshness data. The writer of those two fields is not ruled here and stays with GAP-1509.
8. **Gate source set** (E1013-APP#5). `DailyCompletenessGate` answers COMPLETE when every source mapped to a DAILY product read by JOB-02, JOB-04, JOB-07 or JOB-08 is COMPLETED for D. The product-to-source map is data. DP03 is on-change and not source-fed, so it is removed from the source-fed fixtures. The GL fixture row is added wherever DP01 maps to ALS and GL.

**Rationale.** Keeping the existing key avoids a schema change and an API change. The stamp in use can only move forward, and every story's AC becomes testable against one writer. Writing nothing for a missing date keeps the NOT NULL source times truthful.

**Affected.**
- Services: rwb-source-data.
- Stories: RWB-P1-E1015-APP, RWB-P1-E1015-CON, RWB-P1-E1013-APP, RWB-P1-E1055-APP, RWB-P1-E1069-APP, RWB-P1-E2007-APP, RWB-P1-DM001-APP, RWB-P1-E2010-CON.
- Documents: RWB-P1-E1015-CON s11 and s12.1 (rollup rule and never-stamped answer), ASM v2 (ASM-0822), PS v8 (no change).

**Findings and themes settled.** TH-24: RWB-P1-E1015-APP#8, RWB-P1-E1015-APP#14, RWB-P1-E1015-APP#15, RWB-P1-E1013-APP#4, RWB-P1-E1015-APP#1, RWB-P1-E1015-APP#9, RWB-P1-E1013-APP#13, RWB-P1-E1055-APP#14, RWB-P1-E2007-APP#9, RWB-P1-E1055-APP#5, RWB-P1-E1013-APP#5, RWB-P1-DM001-APP#3, RWB-P1-E1013-APP#15, RWB-P1-E1069-APP#7, RWB-P1-E1069-APP#8, RWB-P1-E1015-CON#14, RWB-P1-E2010-CON#10.
- E1069-APP#8: until Section B lands, the freshness answer follows RD-P1-043.

**GAP and ASM.**
- Closes GAP-0561 (two cut-offs), GAP-0547 (late, failed and no-prior cases) and GAP-0511 (DP04: STALE at expected_by 08:00, no 07:00 stale).
- Changes ASM-0822.
- Confirms ASM-0684.
- GAP-1509 stays open for the DF-EXT-041/042 writer.

**Status.** Proposed – Claude Opus 5.5 (applied).

**Reuse note.** Every consumer reads freshness only through FreshnessQuery. The stamp in use is the greatest LOADED or STALE business_date row. Never-stamped means STALE with a null date. Only P1 E1015 writes `data_product_load`.

---

## RD-P1-042 · Reconciliation tolerance (DL25)

**Question.** DL25: how large a difference between a load and its source is accepted? Under which parameter name and version? What do PASS, BREAK and NOT_RUN mean?

**Options considered.** Those of DL v12 DL25: A, zero (any difference holds the publish); B, a tolerance per measure.

**Sources.**
- DL v12, sheet Open decisions R30, DL25 "Reconciliation tolerance". Options: A zero, any difference holds the publish; B a tolerance per measure. **Recommendation: A.** Owner: Data lead. Date needed: 2026-11-06 (overdue). Affects: Data quality and reconciliation rules. Risk if late: "Differences between sources stay hidden".
- DQR v4, sheet Reconciliations R4 (REC-01 "Zero unexplained") and R5 (REC-02 "Zero").
- NFS v5, NFR-018 ("No unexplained variance; tolerance under DL25").
- RWB-P1-E1011-APP v2: s3 (`recon.tolerance.pct` 0.00, assumed), X1 and X2 (boundary inclusive), BR7. RWB-P1-E1002-APP v2 s3 (`recon.caselist.tolerance.pct` 0.00). RWB-P1-AD019-APP v2, s3 and X10.
- ASM v2: ASM-2602 (no tolerance until DL25; applied by version), ASM-0728, ASM-0735, ASM-0743.
- LOV-REC-RESULT (PASS, BREAK), as cited in AD019-APP#17.
- `parameter-catalog.csv` at the SET root is empty (0 lines), so it holds no row.

**Precedence applied.** DL25 is still open in DL v12, and no D-RCV entry takes it. DQR v4 already states zero for REC-01 and REC-02, so the decision log's recommendation and the data rules agree. The two parameter names in the stories are a story-level conflict; the name used by three stories and the console is kept.

**Ruling.** DL25 option A, the recommended answer, is applied.

1. **Parameter.** One parameter, `recon.tolerance.pct`, value `0.00` (percent), version 1, effective from the first release of RWB-P1-E1011-APP. It is held in the rwb-case parameter catalog and read through the parameter contract (RWB-P3-E1042-CON). It is never written in code; AD019 X10 stands, so an unreadable parameter means FAILED and no result row. `recon.caselist.tolerance.pct` in RWB-P1-E1002-APP s3 is replaced by `recon.tolerance.pct`. A later change of the value is a new parameter version and needs no code change (ASM-2602).
2. **PASS.** A REC-01 or REC-02 result is PASS when the absolute variance percent is at most `recon.tolerance.pct` (inclusive, X2). At 0.00 this means `variance_count` = 0 for REC-01 and the variance amount = 0.00 for REC-02, so any difference is BREAK. BREAK holds the publish: `publish_status` HELD, MSG-P1-012 (E1011 BR7).
3. **NOT_RUN.** There is no NOT_RUN value. LOV-REC-RESULT stays PASS and BREAK. A run that cannot proceed (gate HOLD, no case list, parameter unreadable) writes no `reconciliation_result` row. Its state is the FAILED or held run of ReconciliationWorkflow, shown by the run record and the job monitor. NOT_RUN is removed from RWB-P1-E1011-APP s12.8.
4. **Clean day** (DM008, DM009 and DM010, following ASM-0728, ASM-0735 and ASM-0743). A day is clean when every REC-01 and REC-02 row of the date is PASS under `recon.tolerance.pct` version 1 and no new REC-05 orphan appears (plus the DP06 LOADED condition of ASM-0735 for DM006). Each DM story cites "DL25 option A applied by RD-P1-042; `recon.tolerance.pct` v1 = 0.00".
5. **Decision log.** DL v12 DL25 is to be moved to Decisions taken with this ruling, for confirmation by the Data lead. The confirmation is a governance step, not a build blocker.

**Unblocks build.** Yes. REC-01 and REC-02 grading, the publish hold, the console answer and the DM clean-day count can all be built and tested with the zero tolerance.

**Rationale.** It is the decision log's recommended option. It matches the "Zero" tolerances already in DQR v4 and the NFR-018 intent, and ASM-2602 already makes a later change a data version.

**Affected.**
- Services: rwb-source-data, rwb-case (parameter catalog).
- Stories: RWB-P1-E1011-APP, RWB-P1-E1002-APP, RWB-P1-AD019-APP, RWB-P1-DM008-APP, RWB-P1-DM009-APP, RWB-P1-DM010-APP, RWB-P1-E2010-CON (BR4 cites DL25 option A and, separately, DL11 with GAP-0511 for 08:00).
- Documents: DL v12 (DL25), the parameter catalog (one row), NFS v5 NFR-018 (status note), ASM v2.

**Findings and themes settled.** TH-42: RWB-P1-DM008-APP#8, RWB-P1-DM009-APP#9, RWB-P1-DM010-APP#6, RWB-P1-AD019-APP#17, RWB-P1-E2010-CON#21.

**GAP and ASM.**
- Closes ASM-2602 (tolerance now set as version 1). ASM-0728, ASM-0735 and ASM-0743 are confirmed with the tolerance named.
- GAP-1490 is closed for the tolerance value.

**Status.** Proposed – Claude Opus 5.5 (applied); DL25 option A as recommended by DL v12, for Data lead confirmation.

**Reuse note.** Every service reconciliation slice (P3, S2, P8, S5 and others) reads `recon.tolerance.pct` v1 = 0.00 for zero-tolerance checks and writes only PASS or BREAK, with no row when the check cannot run. Checks with their own DQR v4 tolerance ("Zero after two days" and similar) keep it.

---

## RD-P1-043 · Section B views dependency (DL43): what builds, deploys and alerts while Section B is absent

**Question.** DL43 asks whether the ACE team accepts the RWB-ACE-001 scope and dates. What is the recommended answer? What do the P1 stories build, deploy and alert while the 14 Section B views are absent?

**Options considered.** Those of DL v12 DL43: A, yes, scope and dates as in RWB-ACE-001; B, no, with the scope or date change named. The fallback is costed but not recommended: "Tier 1 views plus the case list".

**Sources.**
- DL v12, sheet Open decisions R46, DL43 "ACE DB additions (RWB-ACE-001)". The scope is 14 new ACE tables, 12 new columns and 80 source fields. The date is 2026-11-21 for a 30 November release (tentative). **Recommendation: "Yes - scope and dates as in RWB-ACE-001."** Owner: ACE team lead. Date needed: 2026-11-21 (passed, with no taken entry). Risk if late: "Fallback: Tier 1 views plus the case list, costed but not recommended".
- EDD v6 s5: the two-migration rule (Section A is 16 Tier 1 views; Section B is 14 Tier 2 views and ships as a later sequence in the week RWB-ACE-001 lands; "Until then the features that read the Section B views stay behind their feature flags, switched off"). EDD v6 also covers the DEV and pipeline order (ACE schema, then V0001, then Section A, then Section B once the additions are present), the ACE dependency gate, Table 8 (flags), and the open-items row for DL43 ("Section A views only; the features that need the Section B views stay behind their flags").
- RWB-P1-E1002-APP v2, s3 (`v_ace_batch_status` is a Section B view; freshness line and gate behind flags until RWB-ACE-001 lands); RWB-P1-E1015-APP v2, s3; RWB-P1-E1065-CON v2, s3 and s12.8 (Tier 2 DDL fixture).

**Precedence applied.** EDD v6 s5 states the flag rule and the DL43 fallback behaviour, and no higher source contradicts it. DL43 itself is open and is not this run's to take; it is the ACE team lead's decision. The ruling therefore applies the recommended answer as the planning basis and fixes the absent-Section-B behaviour from EDD v6.

**Ruling.**

1. **Planning basis.** Build to DL43's recommended answer A: RWB-ACE-001 scope and dates as stated, with Section B landing for the 30 November 2026 release (tentative). The decision itself stays with the ACE team lead and is to be recorded as taken in the decision log.
2. **Build.** All P1 code that reads Section B views is built and tested now. That code covers the freshness stamp and DailyCompletenessGate (`v_ace_batch_status`), the case list freshness line and the AD019 gate. In DEV and the pipeline test database the Section B views are created over the synthetic Tier 2 DDL fixture of RWB-P1-E1065-CON s12.8 (14 tables and 12 columns), in the order ACE schema, then V0001, then Section A, then Section B (EDD v6 s5).
3. **Deploy.**
   - **Before Section B lands.** In SIT, UAT and PROD the Section B migration is not applied until RWB-ACE-001 has landed in that environment, which is the ACE dependency gate of EDD v6 s7. Images and charts deploy with each Section B feature's flag off. With the flag off:
     - (a) `POST /v1/business-days/{date}/ready` answers 202 and starts AceIngestCheck. The run writes no stamp and publishes no AceDataReady or AceDataLate, and `GET /v1/business-days/{date}/status` answers LATE. The daily chain therefore does not start on unverified data, following BSD v6 JOB-02 ("No cases from a stale business date").
     - (b) CaseListBuildWorkflow and ReconciliationWorkflow are registered but are not started by the 07:15 Schedule, which stays paused.
     - (c) FreshnessQuery answers every product with `businessDate` null, status STALE and MSG-P1-001, as in RD-P1-041 item 4.
   - **After Section B lands.** The release owner and the ACE team lead pass the gate, the Section B migration runs, and the flags are switched on per environment.
4. **Alerts.** While a feature's flag is off, its alert rules (Load late, Load failed, stale, gate HOLD, reconciliation break) are not armed, so there are no false pages. The deployment health check reports the flag state, and the release note names the services waiting on RWB-ACE-001. The view conformance test of EDD v6 s5 runs over the views that exist: Section A always, Section B once applied.
5. **If DL43 is answered B.** The DL v12 fallback ("Tier 1 views plus the case list") becomes the scope. The Section B features stay flag-off, and the solution architect re-plans through a new RD-P1 entry. No story invents a substitute source.

**Unblocks build.** Yes for build and DEV or pipeline test of every P1 story, against the synthetic Section B fixture. No for switching on any Section B feature in SIT, UAT or PROD, which waits for RWB-ACE-001 to land. That is a deployment dependency, not a build blocker (EDD v6, "Deployment dependency ... Blocking; DL43").

**Rationale.** EDD v6 already fixes the flag rule. Applying the recommended answer gives developers a stable target, and the flag-off behaviour keeps the overnight chain from running on data whose freshness cannot be proved.

**Affected.**
- Services: rwb-source-data; downstream consumers of AceDataReady (no change of their own).
- Stories: RWB-P1-E1002-OPS, RWB-P1-E1065-CON, RWB-P1-E1015-APP, RWB-P1-E1015-OPS, RWB-P1-E1002-APP, RWB-P1-AD019-APP, RWB-P1-E1069-APP.
- Documents: DL v12 (DL43 note), EDD v6 (no change).

**Findings and themes settled.** TH-78: RWB-P1-E1065-CON#18, RWB-P1-E1002-OPS#21. It also answers the pre-ACE-001 behaviour of RWB-P1-E1069-APP#8.

**GAP and ASM.** None closed. DL43 remains the ACE team lead's open decision.

**Status.** Proposed – Claude Opus 5.5 (applied); DL43 answer for the ACE team lead.

**Reuse note.** Every service that reads a Section B view through the P1 contract cites DL43 (recommended A), builds against the E1065 Tier 2 fixture, and ships with the feature flag off until the ACE dependency gate passes. It treats freshness while its flag is off as STALE with a null date.

---

## RD-P1-044 · One owner per shared rwb-source-data deployment object; no consumer of the service's own AceDataReady

**Question.** Several P1 OPS stories deploy the same chart, worker, KEDA rule, topics, consumer groups and alerts. Who owns each object, and what may the other stories state?

**Options considered.**
- A. Each OPS story deploys the full set, as now.
- B. One base owner for the service release. Every other OPS story states only its delta, and topics and ACLs stay with the platform.

**Sources.**
- EDD v6 s3.2 and s7: a service is one Helm release from one pipeline, any service may release alone on its own tag, and one flag per unfinished change belongs to the owning service.
- KTEC v2, Event topics R4 and DLT R4 (topic `rwb.source-data.events.v1` and `.dlt`, 12 partitions, replication factor 3, 7 days); ACLs R4 (rwb-source-data consumes none); Rules R13.
- RWB-PLT-N002-INF v2 (creates the topics, retry and dead-letter topics and ACLs).
- TWAC v2, Platform rules R17 (KEDA on task-queue backlog); OMD v5, line 27 (Load failed, Load late and Reconciliation break have an instance only in P1).
- The P1 OPS stories: RWB-P1-E1015-OPS, E1002-OPS, E1011-OPS, E1017-OPS, E1064-OPS and E1066-OPS (wave 1), E2010-OPS (wave 2), AD018-OPS and AD019-OPS (wave 4). E1064-OPS, E1066-OPS and E2010-OPS already presume "the chart of rwb-source-data ... exist[s] from the earlier P1 releases".
- RD-P1-040.

**Precedence applied.** Arch v5 and KTEC v2 (no P1 consumer) and RD-P1-040 (in-service child workflows) remove the AceDataReady consumer groups declared in E1002-OPS and E1011-OPS. EDD v6 fixes one release per service.

**Ruling.** Option B. The table below names the owner of each object.

| Object | Owner story | Others |
|---|---|---|
| rwb-source-data Helm chart skeleton and values; api and worker Deployments; probes; Flyway migration job; `rwb_source_data` login secret reference; KEDA ScaledObject on the `rwb-source-data` task-queue backlog (no consumer-lag trigger, because the service consumes no topic) | RWB-P1-E1015-OPS | Add values keys only; never redefine |
| AceIngestCheck worker registration; Schedule `rwb-source-data-ace-late-check` (05:30); `POST /v1/business-days/{date}/ready` and status route; P1 instances of the Load late and Load failed alerts and the stale alert (MSG-P1-001) for every data product | RWB-P1-E1015-OPS | E2010-OPS reuses them for DP04 and registers no stale or Load late alert of its own |
| Topics `rwb.source-data.events.v1` and `.dlt`, partitions, replication, retention, producer ACL | RWB-PLT-N002-INF | E1015-OPS verifies the settings and ACL in its AC; it creates nothing |
| Consumer groups on `rwb.source-data.events.v1` | The OPS story of each consuming service (rwb-case, rwb-payment, rwb-deviation, rwb-writeoff, gateway-bff): one group per service, under KTEC v2 R13 | No P1 story declares a consumer group on this topic |
| CaseListBuildWorkflow registration; Schedule `DailyCaseList` (07:15); case-list alerts | RWB-P1-E1002-OPS | — |
| ReconciliationWorkflow and activity `reconciliation` registration; Reconciliation break alert (MSG-P1-012) | RWB-P1-E1011-OPS | AD019-OPS adds only the console read operations, flag `rwb.source-data.reconciliation-run`, its dashboard panel and any added activities under a new worker build ID (TWAC v2 Platform rules R12, Worker Versioning) |
| Retention run worker registration and container credential | RWB-P1-E1017-OPS | — |
| Dictionary, ledger writer, Stage2ProductWorkflow, job monitor | E1064-OPS, E1066-OPS, E2010-OPS, AD018-OPS respectively | — |

Rules for every delta story:
- (a) Its precondition names RWB-P1-E1015-OPS as the base release.
- (b) Its AC asserts only its own additions, plus a rendered chart diff showing no change to objects it does not own.
- (c) Its rollback follows RD-P1-045.
- (d) The workflow and activity names are those of the APP stories as ruled in RD-P1-040: E1011-OPS's "workflow `reconciliation`" reads `ReconciliationWorkflow`.

E1015-OPS drops the declaration of other services' consumer groups and keeps topic provisioning out of scope, as its own s19 already says.

**Rationale.** One release has one owner, so a later release cannot overwrite scaling or groups. With no self-consumer, the single-group delivery risk disappears.

**Affected.**
- Services: rwb-source-data; platform (N002).
- Stories: RWB-P1-E1015-OPS, RWB-P1-E1002-OPS, RWB-P1-E1011-OPS, RWB-P1-AD019-OPS, RWB-P1-E2010-OPS, RWB-P1-E1017-OPS, RWB-P1-E1064-OPS, RWB-P1-E1066-OPS, RWB-P1-AD018-OPS.
- Documents: Service Contract Catalog v2 (P1 deployment owner note), KTEC v2 (no change).

**Findings and themes settled.** TH-48: RWB-P1-AD019-OPS#1, RWB-P1-E1002-OPS#6, RWB-P1-E1011-OPS#9, RWB-P1-E1015-OPS#10, RWB-P1-E2010-OPS#8 (the 07:00 against 08:00 conflict is settled by RD-P1-041, STALE at expected_by).

**GAP and ASM.** CDC-02790 and CDC-02650 (add P1 as consumer) are rejected. GAP-0511 is closed by RD-P1-041.

**Status.** Proposed – Claude Opus 5.5 (applied).

**Reuse note.** For every service with several OPS stories: the first wave-1 OPS story of the service owns the chart, Deployments, KEDA, migration job and base alerts. Topics and ACLs belong to N002. Consumer groups belong to the consuming service. Every other OPS story is a delta with a chart-diff AC.

---

## RD-P1-045 · Rollback standard with forward-only migrations

**Question.** The OPS and DB stories describe rollback as reversing the migration "by its own script", or list an "undone" state. The migration contract forbids undo files. What is the single rollback standard, and when is rollback triggered?

**Options considered.**
- A. Per-story undo scripts.
- B. Flag off first, then the previous tag. Schema stays forward-only and expand-only, and a fault is fixed by a forward migration with no down script.

**Sources.**
- EDD v6 s7, release path ("Rollback | Switch the feature flag off first; redeploy the previous tag of the service if a flag does not cover the fault | Release owner"); Table 8 (flags: off returns the previous path; removal in the release after the flag is on in production); s5 ("A migration that changes data shape runs behind a feature flag until both code paths are no longer needed"; the decision log and interaction ledger are append only).
- RWB-PLT-E1044-CON v2, BR7 ("PROD runs forward only: no clean, no undo file; a fix is a new version; an applied file is never edited") and X4 (an undo file `U*.sql` is refused).
- TWAC v2, Platform rules R12 (Worker Versioning plus `Workflow.getVersion`; the replay gate).
- RWB-P1-E1011-OPS v2 s9, RWB-P1-E1015-OPS v2 s9 and RWB-P1-E1017-OPS v2 s9 ("the migration is reversed by its own script"); RWB-P1-E1016-DB, RWB-P1-E1069-DB and RWB-P1-ACE001-DB s9 ("undone"; ACE001 AC5 down script).

**Precedence applied.** EDD v6 and RWB-PLT-E1044-CON (platform contract, DP-15 and ADR-021) outrank the OPS and DB stories. The stories' reverse scripts and "undone" states are stale.

**Ruling.** Option B, binding on every P1 OPS and DB story.

1. **Order.**
   - (1) Switch the change's feature flag off.
   - (2) Only if the flag does not cover the fault, redeploy the previous image tag and chart version of rwb-source-data. Because the chart is shared, the release note names every P1 capability the redeploy reverts.
   - (3) Never reverse a migration. A faulty migration is corrected by a new forward version `V<next>__<story>_<name>.sql` on the `rwb_source_data` sequence.
   - No `U*.sql` and no down script exists in any P1 story.
2. **Expand-only rule.** Every migration of a release must work with the previous tag. Tables, nullable columns, views, indexes and grants may be added. Dropping, renaming, narrowing or retyping an object is done only in a later release, after the flag protecting the old path has been removed under EDD v6 Table 8 "Removal". The previous tag must pass its smoke test against the migrated schema in the pipeline; that is the rollback AC every OPS story carries.
3. **Temporal.** Workers deploy with Worker Versioning. A rollback keeps the previous build ID serving its pinned runs, and running workflows are never terminated by a rollback. Schedules are restored to the previous tag's definition by the redeploy; a Schedule added by the faulty release is paused. Kafka consumer offsets are not reset.
4. **First release** (no previous tag). Rollback is flag off, the worker scaled to zero and the release's Schedules paused. The api answers 404 on the flagged operations (Table 8 pattern). Callers get the contract's unavailable answer.
5. **DB stories.**
   - **States.** The state set is Pending, Applied and Failed; "undone" is removed. Each DB story names its corrective forward script per file. For a wrong grant: REVOKE in a new version. For a view owner change: ALTER VIEW OWNER in a new version. A new empty table is dropped only by a new version, before any row is written, and with the release owner's approval.
   - **Seeds.** A seed fails on an existing key and does not overwrite.
   - **ACE001-DB.** The ACE tables and columns change only through the ACE team's own migrations (EDD v6 s5). The AC5 down script is removed. A correction is an ACE-team forward migration, preceded by P1 switching the Section B flags off (RD-P1-043). The 14 ingestion jobs are stopped by the ACE team's own job control, not by a P1 script.
6. **Rollback criterion.** The release owner rolls back when:
   - (a) the post-deploy checks of the OPS story fail (smoke, view conformance, contract or replay gate);
   - (b) the platform smoke workflow (JOB-22) reports no result for the day; or
   - (c) an incident is attributed to the release.

   Flag off is the first action in every case. HELD or PENDING case-list dates are not cleared by a rollback; they are released by a rerun after the fix (RD-P1-040 item 4).

**Rationale.** One standard that matches the platform migration contract and EDD v6. Expand-only schemas are what make "previous tag" safe.

**Affected.**
- Services: rwb-source-data.
- Stories: RWB-P1-ACE001-DB, RWB-P1-E1016-DB, RWB-P1-E1069-DB, RWB-P1-AD019-OPS, RWB-P1-E1002-OPS, RWB-P1-E1011-OPS, RWB-P1-E1015-OPS, RWB-P1-E1017-OPS, RWB-P1-E1066-OPS, RWB-P1-E2010-OPS.
- Documents: EDD v6 (no change; cited).

**Findings and themes settled.** TH-49: RWB-P1-ACE001-DB#15, RWB-P1-E1016-DB#15, RWB-P1-E1069-DB#18, RWB-P1-AD019-OPS#17, RWB-P1-E1002-OPS#16, RWB-P1-E1011-OPS#11, RWB-P1-E1015-OPS#2, RWB-P1-E1017-OPS#5 (the `refuse_change()` purge setting is an expand-only change compatible with the previous tag), RWB-P1-E1066-OPS#14 (TC-06 reads "the previous build ID"), RWB-P1-E2010-OPS#12.

**GAP and ASM.** None.

**Status.** Proposed – Claude Opus 5.5 (applied).

**Reuse note.** Every service's OPS and DB stories copy items 1 to 6 verbatim, with their own service, sequence and flag names substituted.

---

## RD-P1-046 · Sandbox scope (shared) and the published seed fixtures

**Question.** Is the sandbox one shared `rwb_sandbox` with public, recovery and 19 `rwb_*` schemas (ASM-0537), or one database per service release (ASM-0693)? Which case and shape fixtures does RWB-P1-E1065-CON publish for the other E1065 slices?

**Options considered.**
- A. A shared sandbox: one `rwb_sandbox` database, each service building and seeding only its own schema with its own login.
- B. Per service: a separate database for each service.

**Sources.**
- ASM v2: ASM-0537 (shared, 19 schemas, seed 20261128, 2,812 cases as the total split by owner), ASM-0693 (one DEV database per service release; generator builds its own schema only; Confirmed 26 November 2026), ASM-0694 (four stage fixtures: full, empty, refused, timeout; Confirmed) and ASM-5558 (19 sequences plus the view migrations).
- EDD v6 s2 and s5 (every environment holds the ACE schema the views read, with synthetic rows in DEV and the pipeline test database; ACE schema, then V0001, then Section A, then Section B; one Flyway sequence per service in its own schema; other logins hold USAGE on their own schema only).
- RWB-ITG-E1065-ITG v2 (one `rwb_sandbox` with 19 schemas).
- RWB-P1-E1065-APP, CON and DB v2; RWB-P3-, RWB-P4-, RWB-P5- and RWB-S8-E1065-APP v2 (they seed from the P1 case list fixture).
- GAP-0501, GAP-0502, GAP-2137, GAP-3086, GAP-0374, GAP-3168.

**Precedence applied.** Arch v5 slide 29 and DP-01 forbid cross-schema reads and writes, not a shared database. EDD v6 describes one database per environment holding all service schemas, which is the production topology. A shared sandbox mirrors it. ASM-0693's "one database per service release" therefore yields, while its other clauses (separate generator module, own schema only, no cross-schema read) are kept. ASM-0537 wins.

**Ruling.** Option A.

1. **Database.** One DEV sandbox database `rwb_sandbox` per environment that needs it (DEV and pipeline test) holds:
   - schema `public` (the ACE-shaped test double);
   - schema `recovery` (the `v_ace_*` views and helper functions, on P1's sequence);
   - one `rwb_<short>` schema per service.

   Build order: ACE schema, then V0001, then Section A, then Section B (with the Tier 2 fixture), then each service's own sequence in Arch v5 slide 41 wave order (ASM-0537, ASM-5558).
2. **Who builds what.** RWB-P1-E1065-DB and RWB-P1-E1065-APP build and seed only `public`, `recovery` and `rwb_source_data`. Each other service's E1065 slice applies its own sequence and seeds only its own schema with its own login. No slice writes another schema, and no slice renames or recreates `rwb_sandbox`; P1's build creates it if absent and never drops it. E1065-CON AC3, X3 and s12.7 read "P1 builds and checks only public, recovery and rwb_source_data; other `rwb_*` schemas may exist and are not P1's", and BR2 and AC8 are aligned to that wording.
3. **Published fixtures.** RWB-P1-E1065-CON publishes the fixtures as versioned file artefacts in its contract package, not as an operation. RWB-S8-E1065-APP s12.2 is corrected to read the file. The fixture list:
   - (1) `seed-profile.json`: seed 20261128, total 2,812 cases, the five profile elements of ASM-0694.
   - (2) `case-seed-list.csv`: one row per seeded case, with shape_id, product group, account_key, person_key, case entry date and total outstanding. The case number is assigned by rwb-case when P3 seeds; P1 publishes no case number.
   - (3) `shape-table.csv`: one row per shape, with shape_id, row type (case, account only, asset only), count, product group and is_case flag. Shaped cases are inside the 2,812 total, as ASM-0537 says. The 89-days-past-due boundary accounts and the collateral-with-no-account rows are account or asset rows, not cases.
   - (4) The four stage fixtures of ASM-0694: full, empty, refused, timeout.
   - (5) `tier2-ddl.sql`: the 14 Tier 2 tables and the 12 new columns of RWB-ACE-001.

   All are generated deterministically from the seed and versioned with the contract. The consumers (P3, P4, P5 and S8 E1065 slices, and RWB-PLT-TE004-APP) cite the file names. The migration run order and the personal-data field registry that consumers attribute to this contract are not P1 elements: run order is item 1 here, and the registry stays with its owner under GAP-1435.
4. **Shape counts.** The count per shape in `shape-table.csv` is taken from the existing shape list of RWB-P1-E1065-APP s7 and s8. Where that list does not give a count, the value is Pending, owner data architect, tracked as NEW-GAP-C2. Interim build: one row per shape, with the remainder of 2,812 assigned to the plain 90-days-past-due shape.
5. **Not ruled here.** The Tier 1 table count (21, 22 or 24) and the V0001 legacy-baseline question (E1065-APP#11, E1065-DB#9, E1065-DB#10, E1065-CON#14) stay with their existing gaps (GAP-3168, GAP-0566) and the data architect.

**Rationale.** A shared sandbox has the same topology as every real environment. It keeps DP-01 intact through per-schema logins and gives the cross-service fixtures one host. File artefacts are drift-checkable without inventing an operation.

**Affected.**
- Services: rwb-source-data, rwb-case, rwb-access, rwb-document, rwb-deviation, platform (TE004).
- Stories: RWB-P1-E1065-APP, RWB-P1-E1065-CON, RWB-P1-E1065-DB, RWB-ITG-E1065-ITG, RWB-P3-E1065-APP, RWB-P4-E1065-APP, RWB-P5-E1065-APP, RWB-S8-E1065-APP, RWB-PLT-TE004-APP.
- Documents: ASM v2 (ASM-0537, ASM-0693, ASM-0694).

**Findings and themes settled.** TH-59: RWB-P1-E1065-APP#4, RWB-P1-E1065-APP#10, RWB-P1-E1065-APP#12, RWB-P1-E1065-CON#1, RWB-P1-E1065-CON#2, RWB-P1-E1065-CON#3, RWB-P1-E1065-CON#4, RWB-P1-E1065-DB#3, RWB-P1-E1065-DB#12 (the APP generator seeds between apply and verify; E1065-DB tested alone uses `case-seed-list.csv` and `seed-profile.json`). Partly settled: RWB-P1-E1065-APP#11, RWB-P1-E1065-CON#14, RWB-P1-E1065-DB#9 and RWB-P1-E1065-DB#10, by item 5 (out of scope here).

**GAP and ASM.**
- ASM-0537 is confirmed.
- ASM-0693 is changed: the "one DEV database per service release" clause is retired and its generator and own-schema clauses are kept. ASM-0694 is confirmed and extended with fixtures (2), (3) and (5).
- Closes GAP-0501, GAP-0502, GAP-2137 and GAP-3086.
- Opens NEW-GAP-C2 (counts per shape, if not in the story).

**Status.** Proposed – Claude Opus 5.5 (applied).

**Reuse note.** Every other E1065 slice seeds only its own schema in the shared `rwb_sandbox` after P1's build, reads `case-seed-list.csv` and `seed-profile.json` from RWB-P1-E1065-CON, and never recreates the database.

---

## RD-P1-047 · Retention run interface between P5 JOB-17 and P1, and the held-cases read from P3

**Question.** RWB-P5-E1017-APP calls `POST /admin/retention-archive` with only the rule version and run date and expects synchronous counts. RWB-P1-E1017-APP and CON publish `POST /retention-runs` with the rules in the body, answering 202. Which interface is right? And where is the held-case read that P1 needs, given that `CaseHoldQuery` exists in no P3 contract?

**Options considered.**
- A. P1 adds P5's synchronous `/admin/retention-archive` call.
- B. P5 calls P1's asynchronous `/retention-runs` with the rules and polls.
- For the held-case read: C, P3 publishes a held-and-open case read in a named P3 CON; D, P1 reads `rwb_case`. D is refused by DP-01.

**Sources.**
- RRA v4, s3.1 Table 7: step 1 (JOB-17 reads `retention_rule` in `rwb_document`, "the only copy of the retention tables"); step 2 (holds and open cases are excluded; the case flag is `recovery_case.legal_hold` of `rwb_case`); step 4 (P5 asks each schema owner over the owner's REST contract, one hop with a 2 s timeout; GAP-0182, ASM-0266). Also RRA v4 s4.1 (the hold on a party or document is recorded on the case; GAP-0181, ASM-0265).
- BSD v6 JOB-17 (monthly, first Sunday, Temporal Schedule in rwb-document).
- RWB-P1-E1017-APP v2, s3, s4 steps 3–9 and X7–X9; RWB-P1-E1017-CON v2; RWB-P5-E1017-APP v2, items 6 and 47 and s3.
- RWB-P3-E1021-CON v2, line 233 (`POST /api/recovery/case/v1/cases/{caseId}/legal-hold`, P3).
- Service Contract Catalog v2, line 544.
- GAP-0489, GAP-0491, ASM-0681, ASM-0683, CDC-09545, CDC-03039.

**Precedence applied.** RRA v4 makes P5 the only holder of the rules, so a P1 call without rules cannot run, and the P5 story's request shape is stale. The 2 s one-hop budget fits an asynchronous accept, not a synchronous run over 5,000-row pages. DP-01 rules out reading `rwb_case`.

**Ruling.** Options B and C.

1. **P1 run contract** (RWB-P1-E1017-CON, base `/api/recovery/source-data/v1`):
   - **Start.** `POST /retention-runs`.
     - Header `Idempotency-Key` = `{runDate}:{ruleVersion}`.
     - Body `{ruleVersion, runDate, rules[]}`, each rule `{productCode, tableName, recordClass, retentionMonths, ageBasis, endAction}` with `endAction` ∈ {ARCHIVE, REVIEW}.
     - Answers: `202 {runId, status: ACCEPTED}`; `409` when a run for the run date is active (MSG-P2-006); `422` when the rules are refused in full (MSG-GEN-002, MSG-P1-002) or the key is replayed with a different body (MSG-GEN-001).
   - **Read.** `GET /retention-runs/{runId}` answers `{status: RUNNING|COMPLETED|FAILED, countsPerTable[] {tableName, selected, archived, deleted, listed, held}, archiveLocation, holdReport}`.
   - **Fake.** Success, 409, 422, timeout and 5xx.
   - **Workflow.** The run is `RetentionRunWorkflow` on `rwb-source-data`, workflow ID `retention-run-{runDate}`, conflict policy `FAIL` (which gives the 409).
2. **P5 caller** (RWB-P5-E1017-APP). `RetentionRunWorkflow` in rwb-document passes to P1 the rows of the in-force version whose `tableName` is a P1 table. It calls `POST /retention-runs` through an activity (one hop, 2 s), then polls `GET /retention-runs/{runId}` with durable timers every 5 minutes (Proposed) until COMPLETED or FAILED, and records P1's reported counts in its own run. `/admin/retention-archive` is withdrawn. P5 load validation accepts P1 table names for DP01, DP02, DP04, DP05 and DP06 rows, as listed in RRA v4 s1.1 for `rwb_source_data`.
3. **Held and open cases** (RWB-P3-E1021-CON, owner of the legal-hold operation; rwb-case.yaml).
   - **Path.** New operation `GET /api/recovery/case/v1/cases/retention-exclusions?page=&size=`, with page size up to 1,000 and a cursor.
   - **Items.** Each item is `{caseId, caseNumber, reason: LEGAL_HOLD|OPEN, closedAt (null unless reason is absent), accountKeys[], personKeys[]}`. It returns every case on legal hold or open, which together form the RRA v4 step 2 exclusion set.
   - **Closure dates.** A companion `GET /api/recovery/case/v1/cases/closure-dates?closedBefore=&page=&size=` returns `{caseId, closedAt, accountKeys[], personKeys[]}` for closed, unheld cases, which gives the age basis of RD-P1-048.
   - **Errors.** 400, 401, 403, 503, in the standard error envelope.
   - **Fake.** Published by P3.
   - **Consumer.** RWB-P1-E1017-CON lists it as its C dependency in place of `CaseHoldQuery`.
   - **Unreadable answer.** An exclusion answer that cannot be read within 2 s fails the run before selection (X8 kept).
4. **Ordering of the hold read.** The exclusion set is read at run start and read again before each delete unit (RD-P1-048 item 5).

**Rationale.** The rules stay in one place (P5), the call fits the one-hop budget, and P1 never reads another schema. P1 cannot apply "held or open" without account and person keys, so the P3 read carries them.

**Affected.**
- Services: rwb-source-data, rwb-document, rwb-case.
- Stories: RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P5-E1017-APP, RWB-P3-E1021-CON, RWB-ITG-E1017-ITG.
- Documents: rwb-case.yaml (API Specification), rwb-source-data.yaml, Service Contract Catalog v2 (two P3 rows, P1 retention rows), RRA v4 (Table 7, step 4 note).

**Findings and themes settled.** TH-71: RWB-P1-E1017-APP#1, RWB-P1-E1017-APP#2, RWB-P1-E1017-APP#7 (the ACs become a POST answered 202 or 422; "in force" is P5's and is not asserted by P1), RWB-P1-E1017-CON#1, RWB-P1-E1017-CON#2.

**GAP and ASM.**
- Closes GAP-0489 and GAP-0491; ASM-0681 and ASM-0683 are confirmed as ruled.
- Closes GAP-0182 and ASM-0266 for P1, since the expiry operation is now named.
- CDC-09545 and CDC-03039 are applied.

**Status.** Proposed – Claude Opus 5.5 (applied).

**Reuse note.** Every schema owner that P5 asks to archive (P3, P6, P8, S2, S4, S5, S6, S7, S9) publishes the same `POST /retention-runs` and `GET /retention-runs/{runId}` shape on its own base, and reads holds through the P3 retention-exclusions operation.

---

## RD-P1-048 · Retention scope, age basis, hold join, REVIEW and delete rules for rwb_source_data

**Question.** Which rows of RET-2026.11 apply to P1? Which P1 tables are in scope? How is a hold joined to tables with no `case_id`? What does REVIEW do, what is the age basis, and what happens to corrected ledger entries and to partial runs?

**Options considered.**
- A. Keep the 24-month `occurred_at` assumption and the eight-table list, as now.
- B. Use the RRA v4 per-schema periods as the planning values, pending Compliance (DL26). Base the age on case closure from P3 and join holds by case, account or person key. Use ARCHIVE only where the join is exact and REVIEW elsewhere.

**Sources.**
- RRA v4 s1: "Periods are proposed until Compliance issues the bank retention schedule for recovery records (DL26)"; Table 3 rows DP01, DP02, DP04, DP05, DP06 and DP11; s1.1 row `rwb_source_data` (DP01 10 years after the case closes, DP02 10 years after the last case closes, DP04 10 years after the treatment ends, DP05 5 years after the case closes; archive after 2 years closed, or 1 year for DP05); s3 (exclude holds and open cases; Compliance approves disposal before destruction); s3.1 (LAKE_COPY retired, GAP-0184).
- DL v12 DL26 (Compliance supplies the bank retention schedule; open, needed 2026-11-13).
- PS v8 `rwb_source_data.sql`: `interaction` (case_id, person_key, occurred_at, case_seq, corrects_entry_id), `case_list_row` (case_id, account_key, business_date), `party_ext` (person_key), `account_ext` (account_key), `contact_point_ext` (contact_key), `valuation_ext` (valuation_key), `dp_treatment` and `dp_guarantee_claim` (case_id), `efs_ledger_outcome`, `lake_copy_watermark`, outbox and inbox tables, `data_product*`, `sys_*`.
- RWB-P1-E1017-APP v2, s1, s4 steps 4–8 and X1–X10; RWB-P5-E1017-APP v2 s3 (RET-2026.11, DP10 24 months, assumed; GAP-1029, ASM-1972); ASM-4041.

**Precedence applied.** No source gives a confirmed regulatory period. RRA v4 periods are proposals pending DL26, and the 24-month `occurred_at` value is an assumption (ASM-1972) that contradicts RRA v4's DP05 basis. This run must not set a regulatory period, so periods stay Pending with Compliance and only the mechanism is ruled.

**Ruling.**

1. **Periods.** Pending, owner Compliance, tracked as GAP-1029 (DL26). Interim build: RET-2026.11 carries for P1 the RRA v4 s1.1 values as data, marked "proposed (RRA v4), pending DL26":
   - DP05 `interaction`: archive after 12 months closed;
   - DP01 `case_list_row`: archive after 24 months closed;
   - DP04 `dp_treatment` and `dp_guarantee_claim`: REVIEW only, because the treatment end date is S2's (see item 3).

   The run supports ARCHIVE and REVIEW only. No destruction step (removal from the archive) is built in P1 until DL26 is answered and Compliance approves disposal as an rwb-decision approval (RRA v4 s3 steps 3–4). A period is never written in code. The 24-month `occurred_at` precondition of RWB-P1-E1017-APP s3 is replaced by these rows.
2. **Age basis.**
   - **Case-bound tables** (`interaction`, `case_list_row`): age is measured from the case's `closedAt` given by the P3 closure-dates read (RD-P1-047 item 3). A row is selected when its case is closed and unheld and `runDate` minus `retentionMonths` is after `closedAt`.
   - **Boundaries.** A row exactly at the boundary is kept (AC7). Date columns compare as dates; timestamptz columns compare in Asia/Bangkok.
   - **Validation.** `ageBasis` in the request is validated against `sys_fields`. For these two tables it must name `case.closedAt`, the only allowed value.
3. **Tables.**
   - **In scope for ARCHIVE:** `interaction` (join by `case_id`, and by `person_key` against the exclusion `personKeys`) and `case_list_row` (join by `case_id`, and by `account_key` against `accountKeys`).
   - **In scope for REVIEW only:**
     - `party_ext` (by `person_key`), `account_ext` (by `account_key`), `contact_point_ext` and `valuation_ext`. These are current-state rows. A key is listed only when no case in the exclusion set carries it and its last linked case closed longer ago than the period (RRA v4 DP02: "after the last case closes"). `contact_point_ext` and `valuation_ext` have no case or person join in PS v8, so they are always REVIEW, never archived; their join key is Pending, owner data architect, NEW-GAP-C3.
     - `dp_treatment` and `dp_guarantee_claim` (DP04 report copies, join by `case_id`).
   - **Excluded, with reason:**
     - `reconciliation_result`, `data_product_load` and `efs_ledger_outcome`: operational control records with no personal data. Retention is Pending, owner Compliance (GAP-1029); interim, kept.
     - `lake_copy_watermark`: retired with the lake (GAP-0184). It is removed by a forward migration in a later release, not by the run.
     - `outbox_event`, `outbox_delivery`, `processed_event` and `idempotency_key`: platform technical retention (RWB-PLT-TE006).
     - `data_product`, `data_product_access`, `data_contract` and `sys_*`: DP14 reference data, 10 years after superseded, archived at supersession by the reference-data owner, not by this run.
     - `decision_log_entry` and `retention_rule`: not P1's (BR5, X6).

     The validated table list becomes these eight ARCHIVE and REVIEW tables: interaction, case_list_row, party_ext, account_ext, contact_point_ext, valuation_ext, dp_treatment, dp_guarantee_claim. This replaces the story's list, which contained reconciliation_result and data_product_load.
4. **REVIEW.** The rows are selected and counted as LISTED in `countsPerTable.listed`, with the keys in the run's list for Compliance (MSG-P1-020). There is no archive and no delete. The LOV-RETENTION-ACTION value REVIEW maps to this behaviour.
5. **Holds and partial runs.**
   - **Unit.** A delete unit is one table, one rule and one page of `rwb.source-data.retention.batch-size` = 5000.
   - **Hold re-check.** Before each unit's delete, the exclusion set is read again and rows of a newly held or reopened case are dropped from the unit before deletion. Their already-archived files stay in the WORM container, and the hold report lists them.
   - **Commits.** Each unit commits on its own. A failure on unit N leaves units 1 to N-1 deleted and recorded, and the run ends FAILED (MSG-GEN-006).
   - **Rerun.** A rerun with the same run date and version selects only rows still present (X4). A manifest mismatch or a delete failure is an exception path with its own AC.
6. **Ledger integrity** (`interaction`).
   - **Selection.** It filters `retention_class = recordClass`.
   - **Corrections.** An entry is archived and deleted together with every entry that corrects it, as one unit (by `corrects_entry_id`). An entry whose correction is not yet past its rule is kept.
   - **Sequence gaps.** `case_seq` gaps after archive are accepted for closed cases. The ledger check (E1068) verifies sequence continuity only for live rows of open cases.
   - **Idempotency keys.** `idempotency_key` rows are not reused after delete.

**Rationale.** The mechanism can be built and tested now without choosing a regulatory period. Holds are applied by exact keys from the owner of the cases. Tables with no safe join are never deleted. Destruction waits for Compliance, as RRA v4 s3 requires.

**Affected.**
- Services: rwb-source-data, rwb-document, rwb-case.
- Stories: RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P5-E1017-APP, RWB-P3-E1021-CON, RWB-ITG-E1017-ITG.
- Documents: RRA v4 (s1.1 note: P1 table list), ASM v2 (ASM-1972, ASM-4041), DL v12 (DL26 unchanged).

**Findings and themes settled.** TH-72: RWB-P1-E1017-APP#3, RWB-P1-E1017-APP#4, RWB-P1-E1017-APP#5, RWB-P1-E1017-APP#6, RWB-P1-E1017-APP#10, RWB-P1-E1017-APP#17.

**GAP and ASM.**
- GAP-1029 stays open (DL26, Compliance).
- ASM-1972 is changed: the interim values are the RRA v4 proposals, not 24 months on `occurred_at`. ASM-4041 is confirmed (DP05 kept).
- GAP-3158 is closed for the P1 table list.
- Opens NEW-GAP-C3 (join key for contact_point_ext and valuation_ext).

**Status.** Proposed – Claude Opus 5.5 (applied); retention periods Pending, owner Compliance (GAP-1029, DL26).

**Reuse note.** Every schema owner's retention action:
- supports ARCHIVE and REVIEW only until DL26 is answered;
- measures age from P3 `closedAt` for case-bound tables;
- joins holds by case, account or person key from the P3 retention-exclusions read;
- marks tables without an exact join REVIEW only;
- re-reads holds before each delete unit;
- lists every table of its schema as in scope or excluded, with a reason.
