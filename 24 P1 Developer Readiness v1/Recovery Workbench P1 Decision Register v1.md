# Recovery Workbench P1 Decision Register v1

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Run | D-RCV-60 P1 developer readiness (RD-P1 register) |
| Service epic | RWB-SVC-P1 rwb-source-data (Source data) |
| Version | v1, 27 November 2026 |
| Status | Proposed – Claude Opus 5.5 (applied) |
| Prepared by | Chief architect (design sub-agent), Claude Opus 5.5 (claude-opus-5-5) |
| Inputs | `decisions\batch-A.md` and `.csv` (RD-P1-001 to RD-P1-012), `decisions\batch-B.md` and `.csv` (RD-P1-020 to RD-P1-028), `decisions\batch-C.md` (RD-P1-040 to RD-P1-048) |
| Precedence | D-RCV-60 and Architecture v5 (SET\22 Microservice Realignment) > RD-P1 decisions > 16 Temporal and Drools Adoption (D-RCV-36) > 15 ACE DB Alignment (D-RCV-35, ADR-010) > 14 Story Updates > all other documents |

## Purpose

This register holds every design decision taken in the D-RCV-60 P1 developer-readiness run, merged from the three decision batches, with the conflicts between batches resolved. It is the single place a developer, a reviewer or a later service fix looks to find how an open point of rwb-source-data was settled, from which sources, and what changed in which stories and documents.

## How later service fixes use it

1. Before ruling on anything, look it up here first: by theme ID (TH-nn), by artefact name (operation path, event type, workflow or activity name, table, column, parameter key, message code) or by story key. If a decision covers it, apply its **Final ruling (register)** and its **Reuse note**; do not rule again.
2. Read the final ruling, not only the original text. The original text of each batch is kept word for word for audit; where another decision prevailed, the amendment lines and the final ruling say what applies.
3. A later decision that changes a ruling here gets a new RD ID and an amendment line in the decision it changes; it never edits the original text.
4. Values listed under "Values chosen without a source" were chosen by the model that made the decision. They stand until an owner confirms or replaces them; the ones awaiting an owner are rows of `New gaps and assumptions from decisions v1.csv`.

## Numbering

- Decision IDs are RD-P1-nnn (Readiness Decision for P1). `R-P1-nnn` was avoided because Assumptions Register v2 already uses it.
- Used: RD-P1-001 to RD-P1-012 (batch A), RD-P1-020 to RD-P1-028 (batch B), RD-P1-040 to RD-P1-048 (batch C), 30 decisions.
- Unused: RD-P1-013 to RD-P1-019, RD-P1-029 to RD-P1-039 and RD-P1-049 to RD-P1-059. They are not reserved for anything and are never back-filled.
- Conflict references X-nn are register-internal labels used only in this file.

## Sources checked for the case-list conflict

- Architecture v5 Text Extract v1 (SET\22): slide 15 P1 card (lines 1073-1079 and 1113-1115) – P1 serves `/customers/{id}`, `/accounts/{id}`, `/collateral/{id}`, `/payments?accountId=`, freshness and `POST /business-days/{date}/ready`; workflows "AceIngestCheck, reconciliation"; schema "ACE view contract, extension tables, freshness, reconciliation"; events in "(none: Airflow call; fallback polls ACE batch record)". Slide 14 rwb-case (lines 980, 1034) – `GET /cases?queue=`. Slide 44 job table (line 2980) – JOB-04 Reconciliation in rwb-source-data. Lines 37 and 503 – no data lake connection. Line 2364 – Airflow sensor polls status until DONE; SLA alerts at 05:30 and 07:00.
- Microservice Ownership Map v2 (SET\22, extract in REVIEW\_reference\22): Tables R17 and Rulings R2 (`case_list_row` P1, basis TSD P1 v3, ASM-A6-tables-2) and Rulings R79 ("Confirmed by the programme directive of 26 November 2026 (D-RCV-60; GAP-0048) ... Confirm in the verification loop").
- Gap Register v2 (SET\23): GAP-2228 "Resolved (directive)" – "drop case_list_row, its key, the extract file, the lake path and the data set under DP-17; and leave REC-01 and REC-05 with RWB-P1-E1011"; also "have rwb-case read the account and freshness answers of RWB-P1-E1015-CON for one page". GAP-0048 "Resolved (directive)" – row table with P1. Both statuses come from the same change-log line (D-RCV-60, 26 November 2026: "the recommended resolution of every gap is accepted").
- Story files (SET\04 Service Story Files v2): the P1 E1002 APP, CON and OPS stories and RWB-P3-E1002-APP (list built in rwb-case).
- Physical Schema v8 `rwb_source_data.sql` lines 823 and 825 (`sys_objects` rows for `case_list_row` and `lake_copy_watermark`); API Specification v6 `rwb-source-data.yaml` lines 900-930 (`DataProductFreshness`); Error and Message Standard v5 rows MSG-P1-002, MSG-P1-011, MSG-P2-006; Batch and Scheduling Design v5 line 33 (COMPLETED).

**Ruling on the known conflict.** RD-P1-024 prevails. The two directive rows contradict each other and carry equal standing; Architecture v5, which sits at the top of the precedence and is the primary design, places no case list, case-list table or case-list workflow in rwb-source-data and gives JOB-04 as reconciliation only. GAP-2228 is the specific, later analysis of the target case list and follows Architecture v5; GAP-0048 adopts a table owner from TSD P1 v3 (lowest tier) pending verification. Every case-list part of RD-P1-002, RD-P1-003, RD-P1-011, RD-P1-012, RD-P1-020, RD-P1-022, RD-P1-040, RD-P1-042, RD-P1-043, RD-P1-044, RD-P1-045 and RD-P1-048 lapses (resolution X-01). Where GAP-2228 names the contract home of the account read (RWB-P1-E1015-CON), the directive is followed over RD-P1-024 item 3 (resolution X-27).


## Index

| ID | Title | Themes | Services | Status |
|---|---|---|---|---|
| RD-P1-001 | One idempotency standard for every REST POST of rwb-source-data | TH-13 | rwb-source-data; PLT library (RWB-PLT-N009, RWB-PLT-TE006); gateway-bff; rwb-case; rwb-comms; rwb-integration; rwb-document | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-002 | Temporal catalog and P1 story names for workflows and activities | TH-16 | rwb-source-data; rwb-case; rwb-reporting; rwb-document | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-003 | Kafka catalog: AceDataReady and AceDataLate grain, key and outbox; P1 consumer registrations and ACLs | TH-16 | rwb-source-data; rwb-case; rwb-payment; rwb-deviation; rwb-writeoff; gateway-bff; rwb-document; rwb-decision | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-004 | The error envelope is the published Problem schema, extended once | TH-62 | All 19 services (shared Problem); rwb-source-data; gateway-bff | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-005 | One contract file per service; wire names, enums and required flags of rwb-source-data 5.1.0 | TH-63 | rwb-source-data; gateway-bff; rwb-case; rwb-reporting; rwb-agent; rwb-document; rwb-integration | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-006 | Optimistic concurrency on PUT and PATCH | TH-13; TH-63 | rwb-source-data; gateway-bff | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-007 | Interaction ledger: one writer, one append contract | TH-22 | rwb-source-data; rwb-case; rwb-comms; rwb-integration; rwb-document; rwb-payment; rwb-treatment; rwb-partner | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-008 | Event type name of DecisionRecorded | TH-31; TH-16 | All 19 producers; rwb-decision; rwb-reporting; rwb-source-data | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-009 | Ledger intake: consumed-event map, identity, filtering, retry and parking, ordering | TH-31; TH-13 | rwb-source-data; rwb-case; rwb-document; decision-record library producers | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-010 | Case-entry read contract: listEligibleAccounts (not entry-candidates) and the hand-over reads | TH-29 | rwb-source-data; rwb-case; rwb-integration; rwb-decision | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-011 | What counts as a published contract fake for DoR item 22, and version pinning | – | rwb-source-data; every class C consumer of P1; platform contract fake library | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-012 | Job monitor and rerun: owner, job set, list shape and rerun request | TH-68; TH-63 | rwb-source-data; gateway-bff; rwb-integration; rwb-decision; platform | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-020 | Run, readiness and load-state records of rwb-source-data | TH-19 | P1 rwb-source-data; P3 rwb-case; P2 rwb-integration; PLT | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-021 | One owner per table, product, seed and write across P1 and its neighbours | TH-20 | P1; P2; P3; P4; P5; P6; P7; S5; S6; S9; gateway-bff | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-022 | One owner each for reconciliation, freshness stamps, events, gate and readiness | TH-27 | P1; P3; P9 | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-023 | Case identifier in paths, queries and payloads | TH-28 | P1; P3; gateway-bff | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-024 | Case list: P3 rwb-case holds the list, P1 drops `case_list_row` | TH-69 | P1; P3; P9; gateway-bff | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-025 | Data dictionary baseline: counts, data product seed text and release checks | TH-55 | P1 | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-026 | RW-COMPLY read of DP02 in access version DPA-2026.11 | TH-70 | P1; P4 | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-027 | Migration package field mapping, allow-list and provenance columns | TH-11 | P1; P3; P5; P7; S2; S4; S5; S6; S9 and the other owners of migrated tables | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-028 | Parameter catalog for P1: where parameters live, their owner route, and what replaces the empty file | TH-20; TH-27 | P1; P3 | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-040 | Daily ingest, case list and reconciliation triggers, hand-offs and workflow IDs | TH-21 | rwb-source-data; rwb-case; rwb-payment; rwb-deviation; rwb-writeoff; gateway-bff | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-041 | Freshness stamp state model: expected date, multiple sources, repeats, late batches, STALE and the single writer | TH-24 | rwb-source-data | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-042 | Reconciliation tolerance (DL25) | TH-42 | rwb-source-data; rwb-case | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-043 | Section B views dependency (DL43): what builds, deploys and alerts while Section B is absent | TH-78 | rwb-source-data | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-044 | One owner per shared rwb-source-data deployment object; no consumer of the service's own AceDataReady | TH-48 | rwb-source-data; platform (RWB-PLT-N002) | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-045 | Rollback standard with forward-only migrations | TH-49 | rwb-source-data | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-046 | Sandbox scope (shared) and the published seed fixtures | TH-59 | rwb-source-data; rwb-case; rwb-access; rwb-document; rwb-deviation; platform (TE004) | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-047 | Retention run interface between P5 JOB-17 and P1, and the held-cases read from P3 | TH-71 | rwb-source-data; rwb-document; rwb-case | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-048 | Retention scope, age basis, hold join, REVIEW and delete rules for rwb_source_data | TH-72 | rwb-source-data; rwb-document; rwb-case | Proposed – Claude Opus 5.5 (applied) – amended |

## Cross-batch conflicts and resolutions

Each resolution is written as an amendment line in the losing decision and its final ruling. X-05 was merged into X-04.

| Ref | Artefact | Decisions in conflict | Resolution | Prevails |
|---|---|---|---|---|
| X-01 | Case list in P1: `case_list_row`, `CaseListBuildWorkflow`, Schedule `DailyCaseList`, checks ROWS_BELOW_ENTRY / ALLOCATION_COMPLETE / PUBLISHED, publish status | RD-P1-024 vs RD-P1-002, RD-P1-003, RD-P1-011, RD-P1-012, RD-P1-020 C, RD-P1-022, RD-P1-040 items 4-7, RD-P1-042, RD-P1-043, RD-P1-044, RD-P1-045, RD-P1-048 | RD-P1-024 stands. Verified: Architecture v5 slide 15 (lines 1073-1079, 1113-1115) gives P1 the workflows `AceIngestCheck` and reconciliation only and a schema of "ACE view contract, extension tables, freshness, reconciliation" (no case list); slide 44 (line 2980) gives JOB-04 as Reconciliation only; slide 10/14 put `GET /cases?queue=` in rwb-case and merge in gateway-bff; data lake removed (lines 37, 503). Gap Register v2 GAP-2228 is "Resolved (directive)" with "drop case_list_row ... leave REC-01 and REC-05 with RWB-P1-E1011". The opposite reading (Ownership Map v2 Tables R17, Rulings R2 and R79, GAP-0048) was accepted under the same blanket D-RCV-60 status change of 26 November 2026, rests on TSD P1 v3 only and says "confirm in the verification loop"; with two directive rows in conflict, Architecture v5 (same top tier, primary design) decides. RWB-P3-E1002-APP v2 already builds the list in rwb-case. ReconciliationWorkflow becomes a child of AceIngestCheck (batch B cross-batch note). The tie between the two directive rows is registered as a new gap for confirmation (NEW-GAP-X1). | RD-P1-024 |
| X-02 | Who starts ReconciliationWorkflow and Stage2ProductWorkflow; does rwb-source-data consume its own `rwb.source-data.events.v1` | RD-P1-002 (started by AceDataReady), RD-P1-003 rule 5 bullet 4 and ACL list vs RD-P1-040 (child workflows; no self-consumption) and RD-P1-044 | RD-P1-040 stands: Architecture v5 slide 15 lists P1's event input as "(none: Airflow call; fallback polls ACE batch record)"; KTEC v2 ACLs R4 grants no self read; CDC-02650 and CDC-02790 stay rejected. Downstream P1 workflows are child workflows of AceIngestCheck started in the workflow task that commits the ALS stamp (the moment AceDataReady for ALS is written). | RD-P1-040 |
| X-03 | P1 as Kafka consumer of the ledger-intake topics vs "rwb-source-data consumes nothing" | RD-P1-003 rule 5 bullets 1-3 and RD-P1-009 vs RD-P1-040 (precedence sentence) and RD-P1-044 (KEDA row: "the service consumes no topic") | RD-P1-003 and RD-P1-009 stand for the three ledger-intake topics (DP-18 makes P1 the ledger owner; RWB-P1-E1067-APP is in the P1 epic). The "consumes nothing" statements of RD-P1-040 and RD-P1-044 are limited to `rwb.source-data.events.v1`. The intake consumer groups are deployed by RWB-P1-E1066-OPS (ledger writer row of RD-P1-044; there is no E1067-OPS story). The remaining tension with Architecture v5 slide 15 (no event input listed for P1) is registered as NEW-ASM-X1. | RD-P1-003 |
| X-04 | Retention run: workflow ID, Idempotency-Key format, answer to a key reused with another body, 409 message, reuse policy, 202 body | RD-P1-001 rule 6, RD-P1-002 row, RD-P1-004 state row, RD-P1-005 rule 7 vs RD-P1-047 item 1 | Merged: workflow ID `retention-run-{runDate}` (RD-P1-047; follows the `<kebab-type>-{date}` rule of RD-P1-040); conflict policy FAIL plus reuse policy ALLOW_DUPLICATE_FAILED_ONLY (RD-P1-001); Idempotency-Key is a UUID and a reuse with another body answers 409 MSG-PLT-N009-05 (RD-P1-001, platform rule backed by LDM v10 DF-OPS-185, wins over RD-P1-047's `{runDate}:{ruleVersion}` key and 422 MSG-GEN-001); a run of the same run date RUNNING or COMPLETED answers 409 MSG-P2-006 (RD-P1-047; Error and Message Standard v5 lists RWB-E1-017 under MSG-P2-006); 202 body `{runId, status: ACCEPTED}` (RD-P1-047, additive to RD-P1-005). | RD-P1-047 / RD-P1-001 |
| X-06 | Owner story of activity `listEligibleAccounts` | RD-P1-022 (RWB-P1-E1013-APP) vs RD-P1-002 and RD-P1-010 (RWB-P1-E1018-APP) | RD-P1-010 stands (the decision that defines the activity's input, output and gate; EntryCandidateService of RWB-P1-E1018-APP implements it). RWB-P1-E1013-APP keeps `snapshot(page)`. | RD-P1-010 |
| X-07 | AceIngestCheck activities `publishAceDataReady`, `publishAceDataLate` | RD-P1-022 (lists them) vs RD-P1-002, RD-P1-003 rule 4, RD-P1-041 (outbox rows in the stamp transaction) | RD-P1-003 stands: the events are outbox rows written in the transaction of the freshness stamp; no publish activity exists. | RD-P1-003 |
| X-08 | Activities of ReconciliationWorkflow | RD-P1-002 (registers runRec01, runRec02, resolveRec05, writeReconciliationResult from AD019-APP) vs RD-P1-022, RD-P1-040, RD-P1-044 (one activity `reconciliation`, ASM-0689 confirmed; AD019 is a delta) | RD-P1-040 / RD-P1-022 stand: one registered activity `reconciliation`; the four AD019 names are not catalog activities (at most internal steps); AD019-OPS adds no reconciliation activity. | RD-P1-040 |
| X-09 | Owner story of workflow AceIngestCheck | RD-P1-002 (RWB-P1-E1013-APP and RWB-P1-E1015-APP) vs RD-P1-022 (E1015-APP builds; E1013-APP builds the readiness handler that starts it) | RD-P1-022 stands. | RD-P1-022 |
| X-10 | When `GET /business-days/{date}/status` answers DONE | RD-P1-020 F (every mapped source stamped and JOB-04 reconciliation finished, from RWB-P1-E1013-APP s9) vs RD-P1-040 item 1 (DONE once ALS is stamped) | RD-P1-040 stands: Architecture v5 line 2364 has the Airflow sensor poll until DONE with Airflow SLA alerts at 05:30 and 07:00; reconciliation now waits for rwb-case allocation (up to 07:15), so a DONE tied to reconciliation would breach the 07:00 SLA every day. | RD-P1-040 |
| X-11 | Readiness record: idempotency column and status answer fields | RD-P1-020 F (`idempotency_key` = the date; answer holds time of last change) vs RD-P1-001 rule 1 (UUID header) and RD-P1-005 rule 3 (`BusinessDayStatus {businessDate, status}`) | RD-P1-001 stands for the key (UUID of the first call; the date is deduplicated by `uk_business_day_readiness` and the workflow ID). RD-P1-020 stands for the answer: `BusinessDayStatus` adds `changedAt` and 404 for an unknown date (additive to RD-P1-005). | RD-P1-001 / RD-P1-020 |
| X-12 | Freshness stamp times: `source_extracted_at` / `sourceExtractedAt` and `loaded_at` / `loadedAt` | RD-P1-041 item 3 (earliest started_at; latest completed_at; confirms ASM-0684) vs RD-P1-005 rule 2 (sourceExtractedAt = ace_batch_run.completed_at; loadedAt = when the Workbench recorded the stamp) | RD-P1-005 stands. Verified in API Specification v6 rwb-source-data.yaml lines 916-923: sourceExtractedAt "When ACE completed the source batch (ace_batch_run.completed_at)", loadedAt "When the Workbench recorded the freshness stamp". RD-P1-041 item 3 becomes: source_extracted_at = latest completed_at among the product's sources; loaded_at = instant the row is written. ASM-0684 is changed, not confirmed. | RD-P1-005 |
| X-13 | `DataProductFreshness.businessDate` required vs null for a never-stamped product | RD-P1-005 rule 2 (required) vs RD-P1-041 item 4 and RD-P1-043 item 3(c) (null with status STALE) | RD-P1-041 stands: `businessDate` nullable; required = productCode, status. | RD-P1-041 |
| X-14 | Literal of a complete ACE batch in `v_ace_batch_status` | "COMPLETE" in RD-P1-003 rule 1, RD-P1-010 rule 4, RD-P1-012 rule 5, RD-P1-020 E vs "COMPLETED" in RD-P1-040, RD-P1-041 | COMPLETED (Batch and Scheduling Design v5 line 33: "when the record for the business date shows COMPLETED"; RD-P1-040/041). The gate answer COMPLETE / HOLD of DailyCompletenessGate is a different value and is unchanged. | RD-P1-040 |
| X-15 | Gate of `listEligibleAccounts` and `efs-history` | RD-P1-010 rule 4 (the ALS row) vs RD-P1-041 item 8 (DailyCompletenessGate over the product-to-source map) | RD-P1-041 mechanism stands: the activity calls DailyCompletenessGate for DP01, which with the RD-P1-021 seed (DP01 = ALS) is the ALS row; failure type and details of RD-P1-010 unchanged. | RD-P1-041 |
| X-16 | `job_type` of AceIngestCheck and ReconciliationWorkflow runs | RD-P1-012 rule 2 and RD-P1-020 C give both workflows type JOB-04, which collides on `uk_job_run (job_type, business_date, run_no)` | Register resolution: JOB-04 is ReconciliationWorkflow only (Architecture v5 slide 44: JOB-04 = Reconciliation); AceIngestCheck runs carry `job_type` = `AceIngestCheck` (workflow type string rule of RD-P1-012 rule 2). | RD-P1-020 (as amended) |
| X-17 | Publisher of `GET /admin/jobs` and `POST /admin/jobs/{jobId}/rerun` once the case list leaves P1 | RD-P1-012 rule 1 (RWB-P1-E1002-CON baseline, AD018-CON additive) vs RD-P1-024 item 3 (E1002 re-scoped to the account read) and RD-P1-020 D (RWB-P1-AD018-APP creates `job_run`) | RWB-P1-AD018-CON publishes both operations as the single baseline; no E1002 story carries them. Until RWB-P1-AD018 is released (wave 4) a P1 run is restarted by a repeated readiness call or the poll (RD-P1-040 item 1); registered as NEW-ASM-X4. | RD-P1-024 / RD-P1-020 |
| X-18 | Admin rerun of a closed run | RD-P1-040 item 1 Closing and item 4 (rerun of a closed run starts a new run) vs RD-P1-012 rule 5 (rerun only of a FAILED run; reuse ALLOW_DUPLICATE_FAILED_ONLY) | RD-P1-012 stands; RD-P1-040's conflict policy FAIL for reruns is merged into it. A late batch after a COMPLETED AceIngestCheck is picked up by a repeated ready call or the poll (ALLOW_DUPLICATE). | RD-P1-012 |
| X-19 | Counting of repeats: ASM-0822 (DP07 delivery) and ASM-0832 (EFS history) | RD-P1-001 rule 7 (EFS and proof-of-delivery keys in `processed_event`) and RD-P1-007 rule 7 (ASM-0822 to processed_event) vs RD-P1-007 rules 7-8 (P1 read writes nothing; EFS appended over REST by P2) and RD-P1-041 item 7 (metric) | RD-P1-007 rules 7-8 stand for the writes and RD-P1-041 item 7 for the DP07 count: `rwb_source_data_win_delivery_repeat_total`; EFS repeats are counted by the P2 run from 200 answers; `processed_event` keeps ledger-intake redeliveries only. | RD-P1-041 / RD-P1-007 |
| X-20 | Does RWB-P1-E1055-APP call InteractionLedgerWriter in process | RD-P1-007 rule 1 (yes) and RD-P1-021 E1066 note (E1055-APP owns proof-of-delivery writes) vs RD-P1-007 rule 7 (the P1 read writes nothing; rwb-comms appends over REST) | RD-P1-007 rule 7 stands: rwb-comms (RWB-P6-E1055-APP) is the only writer-caller for delivery entries; RWB-P1-E1055-APP is a read. | RD-P1-007 |
| X-21 | Dictionary rows of `case_list_row` after the case list leaves P1 | RD-P1-024 item 1 (DF-RPT-001 to DF-RPT-019 retired; P1 count drops) vs RD-P1-025 (baseline 123 / 1,379 copied from Physical Schema v8) | RD-P1-025 stands for the dictionary: Physical Schema v8 seeds `case_list_row` (line 823) and the already-retired `lake_copy_watermark` (line 825) in `sys_objects`; retired objects stay in the baseline marked retired. RD-P1-024's count drop applies to tables created, not to dictionary rows. | RD-P1-025 |
| X-22 | Classification of the new poll intervals and the allocation wait | RD-P1-040 (`ingest.poll.interval.minutes`, `caselist.allocation.poll.minutes` as named settings) vs RD-P1-028 item 2 (operational values go to the values file); RD-P1-028 item 4 (`caselist.allocation.wait.until` not used by P1) | RD-P1-028 stands: poll intervals are per-environment values-file entries of rwb-source-data; the allocation poll of reconciliation is `recon.allocation.poll.minutes` (renamed, case list gone). `caselist.allocation.wait.until` stays a rwb-case parameter and its `used_by` adds `rwb-source-data.reconciliation`. | RD-P1-028 |
| X-23 | Data product DP14 and the holiday calendar | RD-P1-021 (DP14 Workbench-only, not served by the records operation, never STALE) vs RD-P1-041 item 1 (expected date from DP14 `v_ace_holiday`, an ACE view only P1 may read) | Both stand within limits: P1 reads `v_ace_holiday` internally for the expected business date; the records operation keeps answering 400 for DP14; the composition of DP14 (P1 reference tables plus an ACE view) is registered as NEW-GAP-X2. | RD-P1-021 / RD-P1-041 |
| X-24 | What a reconciliation BREAK holds | RD-P1-042 item 2 (BREAK holds the publish: publish_status HELD) vs RD-P1-024 (no publish in P1) | RD-P1-024 stands: a BREAK raises MSG-P1-012 and the Reconciliation break alert and is shown in the run record; the effect of DL25's "holds the publish" on the rwb-case list is NEW-GAP-X3. | RD-P1-024 |
| X-25 | Case number inside the ledger business key | RD-P1-023 (case number is never a P1 key) vs RD-P1-007 rule 4 (`<code>-<caseNo>-<yyyyMMdd>-<actionId>`) | No conflict: the business key is an opaque producer string (ASM-3716 form); P1 never looks a case up by number. Clarifying note added to RD-P1-023. | none |
| X-26 | Workflow ID of CaseListBuildWorkflow (`case-list-{date}` vs `case-list-build-{date}`) | RD-P1-002 vs RD-P1-040 item 4 | Moot: the workflow is withdrawn by X-01. | RD-P1-024 |
| X-27 | Contract home of the account-page read used by rwb-case for the list | RD-P1-024 item 3 (published in RWB-P1-E1002-CON; RWB-P3-E1002-APP repoints) vs GAP-2228 directive resolution ("have rwb-case read the account and freshness answers of RWB-P1-E1015-CON") | GAP-2228 (D-RCV-60) stands: the account-page read is published in RWB-P1-E1015-CON, the single freshness-and-read surface, and built by RWB-P1-E1002-APP (same pattern as the readiness pair in RD-P1-022). RWB-P3-E1002-APP keeps its pointer to RWB-P1-E1015-CON (no repoint). RWB-P1-E1002-CON then publishes nothing (jobs moved by X-17) and is retired with a pointer; RWB-P1-E1002-OPS deploys the operation as a delta. | GAP-2228 directive |
| X-28 | Workflow ID uniqueness of `retention-run-{runDate}` in namespace `rwb-recovery` | RD-P1-047 (P1 RetentionRunWorkflow) vs the rwb-document RetentionRunWorkflow of JOB-17 in the same namespace | No ruling on P5's ID here; registered as NEW-ASM-X3 (rwb-document must not use the same workflow ID). | none |

## Decisions

## RD-P1-001 · One idempotency standard for every REST POST of rwb-source-data

_Original text of batch A kept for audit. Amendments and the final ruling follow it._

**Question.** Where does the idempotency key come from, what is its format and lifetime, what does a replay answer (200 or 201), what does the same key with a different body answer (409 or 422), how are body-less POSTs and business-level repeats handled, and what is counted?

**Options considered.**
1. Each story keeps its own rule (status quo): replay 200 in RWB-P1-E1066-APP, stored 201 in RWB-P1-E1066-CON, 422 in RWB-P1-E1002-CON X3, refusal MSG-P1-011 in RWB-P1-E1001-APP X7. Rejected: the platform library applies one rule in front of every handler.
2. Adopt the platform helper of RWB-PLT-N009 as is and fill its two open values (format, expiry) from the data dictionary. Chosen.
3. A free-text business key in the header (e.g. `2026-12-06-RET-2026.11`). Rejected: LDM v10 types the stored header as uuid.

**Sources.** Arch v5 slide 11 ("Idempotency-Key on every POST"; "Commands carry Idempotency-Key"); Error Handling and Resilience Standard v4 §3 (a POST is not retried automatically and carries its Idempotency-Key) and §6 (activity key = workflow ID + activity type + step); Service Template Specification v2 rows 3, 168, 199; RWB-PLT-N009-CON BR1–BR6, §11 rows Scope, Stored response, Expiry; RWB-PLT-N009-APP X3–X6 (MSG-PLT-N009-03, -04, -05, -06); LDM v10 entity row R54 `idempotency_key` ("kept 24 hours"), DF-OPS-184 to DF-OPS-188 (`idempotency_key` uuid UK, `endpoint` varchar(100), `request_hash` char(64) SHA-256 of the body, `response` jsonb); Kafka catalog sheet Outbox and inbox R6–R7; DF-OPS-180 to DF-OPS-183 (`processed_event.idempotency_key` varchar(120) UK, `hit_count` default 1, `last_seen_at`); AR v2 ASM-2437, ASM-2439, ASM-0208; GR v2 GAP-1400, GAP-1401, GAP-0131.

**Precedence applied.** Arch v5 fixes the header on every POST and RFC 9457 errors. The platform contract (N009) and LDM v10 are the same tier; they do not conflict – N009 leaves format and expiry open and LDM v10 gives both. Story texts that differ are stale.

**Ruling.**
1. **Header.** Every POST of rwb-source-data requires the header `Idempotency-Key` (name case-insensitive, ASM-2439). Value: a UUID in canonical 8-4-4-4-12 lower-case hex form, 36 characters (LDM v10 DF-OPS-185 type uuid). PUT, PATCH, GET and DELETE carry no Idempotency-Key (Arch v5 slide 11 names POST only); PUT and PATCH use RD-P1-006.
2. **Store and scope.** The helper of RWB-PLT-N009 stores the first response in `rwb_source_data.idempotency_key` (PLT library table, ASM-2437): `idempotency_key` = header value, `endpoint` = method plus the resolved path (e.g. `POST /admin/jobs/6f1c…/rerun`), `request_hash` = SHA-256 of the raw request body (of the empty string when there is no body), `response` = status, headers and body. Scope = service schema + key; the key is unique on its own inside the schema (DF-OPS-185 UK), so one key can never be used on two endpoints.
3. **Answers.**
   - Header missing, blank or not a UUID → **400**, problem `messageCode` `MSG-PLT-N009-03`; handler not invoked, nothing written.
   - Same key, same `endpoint`, same `request_hash`, inside the window → the **stored response replayed with its stored status and body** (a 201 stays 201, a 202 stays 202, a 200 stays 200); no second effect, no second event (`MSG-PLT-N009-04` is a log code only, never in a body).
   - Same key with a different `endpoint` or a different `request_hash` → **409**, `messageCode` `MSG-PLT-N009-05`; stored response unchanged. 422 is never used for a key conflict.
   - A second request with the same key while the first is still in flight (row locked, no response stored) → **409**, `MSG-PLT-N009-05`; the caller retries after the first completes and then receives the replay.
   - Store unreachable → **503**, `MSG-PLT-N009-06`, caller's transaction rolled back.
4. **Expiry.** A stored response is kept **24 hours** from its first write (LDM v10 entity `idempotency_key`); a purge removes older rows; after expiry the same key is a first request. The chart value is the platform's (RWB-PLT-N009-CON §11 Expiry) with default 24 h.
5. **Body-less POSTs** (rerun, publish, retention start): the body hash is that of the empty body, and "a different request" means a different resolved path (e.g. another `jobId`). Stories must not describe a "same key, different body" case for them.
6. **Business-level repeats are not key replays.** A request with a new key that repeats a business fact is answered by the operation's own rule, not by the helper:
   - rerun of a run that is not FAILED, or a second start for a business date already running → 409 (RD-P1-012);
   - retention run (RWB-P1-E1017): Temporal workflow ID `retention-<runDate>-<ruleVersion>` with reuse policy ALLOW_DUPLICATE_FAILED_ONLY; a new key after FAILED starts a new execution (202), a new key while RUNNING or after COMPLETED answers 409 with the stored `runId` in `detail`;
   - load repeat of the same table, validFrom and content hash (RWB-P1-E1001-APP X7, RWB-P3-E1043-CON BR5): **200** with the first load's body, nothing written (the contract text "returns the first load and writes nothing" wins over the story's refusal; MSG-P1-011 is not raised for it);
   - ledger append with a new header key but an `idempotencyKey` (business key) already in the ledger → RD-P1-007 rule 4 (200 with the existing entry).
7. **Counting (R-UNI-40).** Event redeliveries are counted in `processed_event.hit_count` (1 on first, +1 per repeat, `last_seen_at` set), keyed by ce_id (ASM-0208). In-process work keys (EFS history `EFS:<efs_record_key>`, proof-of-delivery keys, ledger business keys from the intake) use the same table with the work key in `processed_event.idempotency_key` and `event_id` null (DF-OPS-181 "where the key came from an event"). A REST key replay is not counted. `idempotency_key` has no hit count and none is added.
8. **Temporal.** Activity idempotency stays the Error Handling Standard v4 §6 rule (workflow ID + activity type + step); a Temporal start is deduplicated by its workflow ID (Arch v5 slide 11 "Workflow ID = business key").
9. **Yaml.** Every POST in `rwb-source-data.yaml` (API Specification v7) declares a reusable header parameter `IdempotencyKey` (`in: header`, `name: Idempotency-Key`, `required: true`, `schema: {type: string, format: uuid}`) and the responses 400, 409 and 503 (RD-P1-005).

**Rationale.** One rule lives in one library (Arch v5 slide 20, N009); the two values N009 left open are already in LDM v10, so nothing is invented. Separating key replay from business repeats removes the false "same key, different date" cases.

**Affected services.** rwb-source-data (provider of every POST); PLT library (RWB-PLT-N009, RWB-PLT-TE006); every caller of a P1 POST (gateway-bff, rwb-case, rwb-comms, rwb-integration, rwb-document).

**Affected stories.** RWB-P1-AD018-APP, RWB-P1-AD018-CON, RWB-P1-DM003-APP, RWB-P1-DM004-APP, RWB-P1-E1001-APP, RWB-P1-E1002-CON, RWB-P1-E1011-CON, RWB-P1-E1011-OPS, RWB-P1-E1013-APP, RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1055-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E1066-APP, RWB-P1-E1066-CON, RWB-P1-E1067-APP; consumers to align: RWB-P3-E1043-CON (status of the repeat stated as 200), RWB-PLT-N009-CON and RWB-PLT-N009-APP (format and expiry filled).

**Affected documents.** API Specification v6 → v7 `rwb-source-data.yaml`; Service Contract Catalog v2 → v3 (P1 rows: idempotency column); RWB-PLT-N009-CON/APP (§11 header format and expiry); Gap Register v2, Assumptions Register v2.

**Findings and themes settled.** TH-13: RWB-P1-E1013-APP#26, RWB-P1-E1066-APP#8, RWB-P1-E1067-APP#5, RWB-P1-DM003-APP#5, RWB-P1-DM004-APP#4, RWB-P1-AD018-APP#11, RWB-P1-E1055-APP#16, RWB-P1-E1067-APP#6 (key part, see RD-P1-009), RWB-P1-E1001-APP#G8, RWB-P1-E1064-APP#9, RWB-P1-AD018-CON#9, RWB-P1-E1002-CON#6, RWB-P1-E1017-CON#6, RWB-P1-E1064-CON#15, RWB-P1-E1066-CON#12. RWB-P1-E1018#13 is settled by RD-P1-006.

**GAP/ASM.** Closes GAP-1401 items (b) expiry and scope and GAP-1400 item (b) header format; changes ASM-2439 (working read replaced: UUID, 24 h, scope = schema + endpoint + key); confirms ASM-2437 and ASM-0208; changes ASM-0832 (the hit count of a repeated history key is `processed_event.hit_count`, not a writer idempotency store).

**Status.** Proposed – Claude Opus 5.5 (applied). Values 1–4 are taken from sources; the in-flight answer (rule 3, fourth bullet) and the retention reuse policy (rule 6) are Claude Opus 5.5 choices.

**Reuse note.** Every later service fix copies rules 1–5 verbatim (they are platform rules, not P1 rules) and rewrites its own "replay"/"same key" criteria as: missing key 400 MSG-PLT-N009-03; replay = stored status and body; mismatch or in-flight 409 MSG-PLT-N009-05; store down 503 MSG-PLT-N009-06; 24 h. Business-level repeats are stated per operation, never as key behaviour.

#### Register amendments

- Amended by RD-P1-047 (X-04): Rule 6, retention bullet: workflow ID `retention-run-{runDate}` (not `retention-<runDate>-<ruleVersion>`); conflict policy FAIL with reuse policy ALLOW_DUPLICATE_FAILED_ONLY; a new key while a run of the run date is RUNNING, or after it COMPLETED, answers 409 MSG-P2-006 with the stored `runId` in `detail`; a new key after FAILED starts a new execution (202). The header stays a UUID (rules 1-3 prevail over RD-P1-047's `{runDate}:{ruleVersion}`).
- Amended by RD-P1-007 and RD-P1-041 (X-19): Rule 7: EFS history keys and proof-of-delivery keys are removed from the in-process work keys. EFS history is appended over REST by the P2 hand-over run, which counts written/skipped from 201/200 (RD-P1-007 rule 8); the P1 proof-of-delivery read writes nothing (RD-P1-007 rule 7) and DP07 delivery repeats are counted by metric `rwb_source_data_win_delivery_repeat_total` (RD-P1-041 item 7). `processed_event` holds ledger-intake redeliveries (ce_id) only. This decision's change to ASM-0832 is replaced by RD-P1-007's.

**Final ruling (register).** Rules 1-5, 8 and 9 apply unchanged. Rule 6 retention bullet: ID `retention-run-{runDate}`, FAIL + ALLOW_DUPLICATE_FAILED_ONLY, 409 MSG-P2-006 while RUNNING or after COMPLETED, 202 after FAILED. Rule 7: `processed_event.hit_count` counts ledger-intake event redeliveries by ce_id only; EFS repeats are counted by the P2 run, DP07 delivery repeats by metric `rwb_source_data_win_delivery_repeat_total`.

**Values chosen without a source.** In-flight 409 answer; retention reuse policy ALLOW_DUPLICATE_FAILED_ONLY

---

## RD-P1-002 · Temporal catalog and P1 story names for workflows and activities

_Original text of batch A kept for audit. Amendments and the final ruling follow it._

**Question.** Which workflow type names, activity names, workflow IDs and schedules does rwb-source-data register, given that stories reuse the catalogued `listEligibleAccounts` and `snapshot(page)` for other purposes, use two names for the reconciliation workflow, and add workflows the catalog does not hold?

**Options considered.** (1) Change the catalog to the story meanings; (2) keep the Architecture v5 and catalog meanings and give the story-specific activities their own names, then add every uncatalogued P1 workflow to the catalog. Option 2 chosen: Arch v5 slides 14 and 15 fix the two activities and their callers.

**Sources.** Arch v5 slide 14 (rwb-case: "TMP Source data: listEligibleAccounts(businessDate)") and slide 15 (P1: "TMP Act: listEligibleAccounts, snapshot(page) · Workflow: AceIngestCheck, reconciliation"; rwb-reporting "snapshot(page) for measures"); Temporal catalog Workflows R18 (AceIngestCheck, one run per business date), R19 (reconciliation, JOB-04), Activities R4, R5; SCC v2 rows 185 and 188; Batch and Scheduling Design v6 Jobs R8 and Schedule map R5 (JOB-04 = "AceIngestCheck then reconciliation"); RWB-P1-E1002-APP/CON §12.5–12.6 (CaseListBuildWorkflow, DailyCaseList at 07:15); RWB-P1-E1011-APP/CON (ReconciliationWorkflow, `recon-{businessDate}`), RWB-P1-E1011-OPS (`reconciliation`); RWB-P1-E1015-CON §12.5; RWB-P1-E1017-APP/CON/OPS §12.5 (RetentionRunWorkflow, eight activities); RWB-P1-E2010-CON §12.5 and ASM-0702 (Stage2ProductWorkflow); AR v2 ASM-0702, GR v2 GAP-0145, GAP-0510, GAP-0497.

**Precedence applied.** Arch v5 fixes the meaning and caller of `listEligibleAccounts` and `snapshot(page)` and the proper name `AceIngestCheck`; Arch v5 uses `<Name>Workflow` type names elsewhere (RouteDecisionWorkflow, DeviationWorkflow) and writes "reconciliation" as a step label, so it does not fix that type name. Stories that reuse catalogued names for another meaning are stale.

**Ruling.** All P1 workflows and activities run on task queue `rwb-source-data`, namespace `rwb-recovery`, and are published in the rwb-source-data contract jar (major version 1).

| Kind | Name (exact type string) | Workflow ID | Started by | Owner story |
|---|---|---|---|---|
| Workflow | `AceIngestCheck` | `ace-ingest-check-{businessDate}` (yyyy-MM-dd) | `POST /business-days/{date}/ready` (Airflow), one run per business date | RWB-P1-E1013-APP, RWB-P1-E1015-APP |
| Workflow | `ReconciliationWorkflow` (JOB-04 step "reconciliation") | `recon-{businessDate}` | `rwb.source-data.AceDataReady.v1` for source ALS, and `POST /admin/jobs/{jobId}/rerun` | RWB-P1-E1011-APP |
| Workflow | `CaseListBuildWorkflow` (JOB-04 case-list step) | `case-list-{businessDate}` | `rwb.source-data.AceDataReady.v1` for ALS, fallback Schedule `DailyCaseList` | RWB-P1-E1002-APP |
| Workflow | `Stage2ProductWorkflow` | `stage2-dp04-{businessDate}` | `rwb.source-data.AceDataReady.v1` (ASM-0702) | RWB-P1-E2010-APP |
| Workflow | `RetentionRunWorkflow` | `retention-{runDate}-{ruleVersion}` | `POST /retention-runs` called by rwb-document JOB-17 | RWB-P1-E1017-APP |
| Activity | `listEligibleAccounts` | – | `DailyCaseRun` of rwb-case (JOB-02), see RD-P1-010 | RWB-P1-E1018-APP |
| Activity | `snapshot(page)` | – | rwb-reporting measures (SCC v2 row 188); RWB-P1-E1013-APP | RWB-P1-E1013-APP |
| Activity | `listCaseListAccounts(businessDate)` (renamed from the E1002 use of `listEligibleAccounts`) | – | `CaseListBuildWorkflow` | RWB-P1-E1002-APP |
| Activity | `caseListPage(businessDate, page)` (renamed from the E1002 use of `snapshot(page)`) | – | rwb-case SCR-02 and rwb-reporting | RWB-P1-E1002-APP |
| Activity | `readDp04SourcePage(businessDate, page)` (renamed from the E2010 use of `snapshot(page)`); `writeDp04Page`, `checkActiveCount`, `stampDp04` unchanged | – | `Stage2ProductWorkflow` | RWB-P1-E2010-APP |
| Activities | `stampProducts`, `markStale`, `checkDailyCompleteness` (RWB-P1-E1015-CON); `publishAceDataReady` and `publishAceDataLate` are **removed** (the outbox publishes, RD-P1-003) | – | `AceIngestCheck` | RWB-P1-E1015-APP |
| Activities | `validateRules`, `casesOnLegalHold`, `caseNumbers`, `selectRows(page)`, `archiveTable`, `verifyManifest`, `deleteArchivedRows`, `recordRun` (eight) | – | `RetentionRunWorkflow` | RWB-P1-E1017-APP |
| Schedule | `DailyCaseList` – cron from the rwb-case parameters contract (DP-06), default 07:15 Asia/Bangkok, overlap SKIP, catch-up one business date; it starts `CaseListBuildWorkflow` only if no execution with the same workflow ID exists | – | Temporal Schedule | RWB-P1-E1002-APP |

`AceIngestCheckWorkflow` (RWB-P1-E1015-CON) and `reconciliation` as a type name (RWB-P1-E1011-OPS) are stale. The reconciliation activities named in RWB-P1-AD019-APP (`runRec01`, `runRec02`, `resolveRec05`, `writeReconciliationResult`) are the activities of `ReconciliationWorkflow` and are added to the catalog with it. RWB-P1-E1002-CON AC6 is restated as "the cron is bound to the parameter with default 07:15", which satisfies AC11. RWB-P1-E1011-CON §12.9 states `recon-{businessDate}` on `rwb-source-data`.

**Rationale.** Keeps the Arch v5 contract of the two shared activities intact for their real callers (rwb-case, rwb-reporting), removes the same-name collision on one task queue, and gives every P1 workflow one catalogued type string so a start by type name cannot fail.

**Affected services.** rwb-source-data; rwb-case (caller of `listEligibleAccounts`, `caseListPage`); rwb-reporting (`snapshot(page)`, `caseListPage`); rwb-document (starts retention runs).

**Affected stories.** RWB-P1-E1001-APP, RWB-P1-E1002-APP, RWB-P1-E1002-CON, RWB-P1-E1002-OPS, RWB-P1-E1011-APP, RWB-P1-E1011-CON, RWB-P1-E1011-OPS, RWB-P1-E1013-APP, RWB-P1-E1015-APP, RWB-P1-E1015-CON, RWB-P1-E1015-OPS, RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P1-E2010-APP, RWB-P1-E2010-CON, RWB-P1-E2010-OPS, RWB-P1-AD018-CON, RWB-P1-AD019-APP; ITG to align: RWB-ITG-E1002-ITG.

**Affected documents.** Temporal Workflow and Activity Catalog v2 → v3 (sheets Workflows, Activities, Schedules); Batch and Scheduling Design v6 → v7 (JOB-04 row: workflows `AceIngestCheck`, `CaseListBuildWorkflow`, `ReconciliationWorkflow`; Schedule `DailyCaseList`); Service Contract Catalog v2 → v3 (P1 Temporal rows).

**Findings and themes settled.** TH-16 (Temporal part): RWB-P1-E1002-APP#6, RWB-P1-E1002-CON#10, RWB-P1-E1002-CON#21, RWB-P1-E1002-OPS#7, RWB-P1-E1011-APP#12, RWB-P1-E1011-CON#13, RWB-P1-E1011-OPS#4, RWB-P1-E1015-APP#27, RWB-P1-E1017-APP#23, RWB-P1-E2010-OPS#4.

**GAP/ASM.** Closes GAP-0145 for P1 (activities named); changes ASM-0702 (activity `snapshot(page)` of the stage 2 step renamed `readDp04SourcePage`); closes the workflow-name part of GAP-0497.

**Status.** Proposed – Claude Opus 5.5 (applied). `AceIngestCheck`, `listEligibleAccounts`, `snapshot(page)`, JOB-04 and the stories' own names are sourced; the three new activity names, the workflow IDs `ace-ingest-check-`, `case-list-`, `stage2-dp04-` and the type string `ReconciliationWorkflow` are Claude Opus 5.5 choices.

**Reuse note.** A later service never reuses a catalogued activity or workflow name for another meaning on its own task queue; a new name is added to the Temporal catalog in the same change as the story. Workflow type strings are `<Name>Workflow` unless Arch v5 gives a proper name (AceIngestCheck, DailyCaseRun).

#### Register amendments

- Amended by RD-P1-024 (X-01): Rows `CaseListBuildWorkflow`, `listCaseListAccounts`, `caseListPage` and Schedule `DailyCaseList` are withdrawn; the RWB-P1-E1002-CON AC6/AC11 cron sentence lapses.
- Amended by RD-P1-040 (X-02): No P1 workflow is started by consuming `rwb.source-data.AceDataReady.v1`. `ReconciliationWorkflow` (`recon-{businessDate}`) is started by `AceIngestCheck` as a child workflow (ParentClosePolicy ABANDON) in the workflow task that commits the ALS stamp, and by the admin rerun; `Stage2ProductWorkflow` (`stage2-dp04-{businessDate}`) is started the same way (the ALS-stamp moment that ASM-0702 ties to AceDataReady).
- Amended by RD-P1-022 (X-09): `AceIngestCheck` is built by RWB-P1-E1015-APP; RWB-P1-E1013-APP builds only the readiness handler that starts it. Starters add the 05:30 Schedule `rwb-source-data-ace-late-check` and the fallback poll; activity `readBatchStatus(businessDate)` is added (RD-P1-040 item 1).
- Amended by RD-P1-040 (X-08): `ReconciliationWorkflow` registers one activity, `reconciliation` (ASM-0689). `runRec01`, `runRec02`, `resolveRec05`, `writeReconciliationResult` are not added to the catalog.
- Amended by RD-P1-047 (X-04): `RetentionRunWorkflow` workflow ID is `retention-run-{runDate}`.

**Final ruling (register).** Registered P1 workflows: `AceIngestCheck` (`ace-ingest-check-{businessDate}`; built by RWB-P1-E1015-APP; started by the readiness handler of RWB-P1-E1013-APP, the 05:30 Schedule `rwb-source-data-ace-late-check` and the fallback poll; activities `readBatchStatus`, `stampProducts`, `markStale`, `checkDailyCompleteness`), `ReconciliationWorkflow` (`recon-{businessDate}`; child of AceIngestCheck after the ALS stamp, and admin rerun; one activity `reconciliation`), `Stage2ProductWorkflow` (`stage2-dp04-{businessDate}`; child of AceIngestCheck after the ALS stamp; activities `readDp04SourcePage`, `writeDp04Page`, `checkActiveCount`, `stampDp04`), `RetentionRunWorkflow` (`retention-run-{runDate}`; eight activities). Shared activities `listEligibleAccounts` (RWB-P1-E1018-APP) and `snapshot(page)` (RWB-P1-E1013-APP) keep their Architecture v5 meaning. No case-list workflow, activity or Schedule exists in P1.

**Values chosen without a source.** Activity name readDp04SourcePage; workflow IDs ace-ingest-check-{businessDate}, stage2-dp04-{businessDate}; type string ReconciliationWorkflow (listCaseListAccounts, caseListPage, case-list-{businessDate} withdrawn)

---

## RD-P1-003 · Kafka catalog: AceDataReady and AceDataLate grain, key and outbox; P1 consumer registrations and ACLs

_Original text of batch A kept for audit. Amendments and the final ruling follow it._

**Question.** What is the grain, record key and payload of EV-26 AceDataReady and EV-27 AceDataLate (catalog key caseId, stories key business date or source + date), are they published through the outbox or directly, and which topics does rwb-source-data consume (catalog lists it as consumer of none)?

**Options considered.** Key: caseId (catalog; the events carry none) / businessDate / sourceSystem + businessDate (ASM-0685). Publish: direct (catalog Not on Kafka R6) / outbox. Consumers: leave catalog / register every topic a P1 story consumes. Chosen: sourceSystem + businessDate, outbox, register.

**Sources.** Kafka catalog sheets Topics R4, Events R29–R30, Not on Kafka R6, Envelope R7–R14, Outbox and inbox R9, ACLs R2 and R4, Delivery rules R4–R13; asyncapi/rwb-source-data.asyncapi.yaml (x-topic key caseId; data untyped); AR v2 ASM-0685 (key sourceSystem and businessDate; subject = source system), ASM-0540, ASM-0206, ASM-0208; Arch v5 slides 11, 22, 32 and line 2294 (AceDataReady starts DailyCaseRun, payment runs, reconciliation, deviation screening); RWB-P1-E1013-APP AC3 and §12.3; RWB-P1-E1015-APP §12.3, AC15; RWB-P1-E1015-CON BR3; RWB-P1-E1067-APP §3.

**Precedence applied.** Arch v5 fixes CloudEvents binary mode, the outbox in the producer's transaction (slide 22) and the per-case key for case events; it says nothing about a key for events without a case. Catalog R6 ("EV-26 and EV-27 write no outbox row") conflicts with the stories, which write the freshness stamp – a Workbench change – before publishing; the catalog row is stale.

**Ruling.**
1. **Grain.** `rwb.source-data.AceDataReady.v1` is published once per **source system and business date** when the batch of that source is COMPLETE and its products are stamped; `rwb.source-data.AceDataLate.v1` once per source system and business date still not COMPLETE at the cut-off (05:30, Arch v5 slide 32). RWB-P1-E1013-APP AC3 reads "exactly one per source system and business date". Consumers that need one start per date (DailyCaseRun, ReconciliationWorkflow, CaseListBuildWorkflow, Stage2ProductWorkflow) start on sourceSystem `ALS` and deduplicate by their workflow ID.
2. **Record key and subject.** Kafka key = `{sourceSystem}:{businessDate}` (e.g. `ALS:2026-12-01`); `ce_subject` = sourceSystem (ASM-0685). `x-topic.key` of rwb.source-data.events.v1 becomes "sourceSystem:businessDate (no case)"; the catalog Topics R4 key column likewise.
3. **Payload** (`data`, JSON, all required unless stated): `sourceSystem` string ≤10 (ace_batch_run.source_system); `businessDate` string format date; `status` string – the `v_ace_batch_status` status value copied unchanged; `completedAt` string format date-time, **nullable** (null on AceDataLate when no batch completed). `eventId`, `occurredAt` and `schemaVersion` of ASM-0685 are not payload fields: they are `ce_id`, `ce_time` and the `.v1` of `ce_type` (catalog Envelope R6, R13). Field names are camelCase everywhere; snake_case in RWB-P1-E1015-APP §12.3 is stale.
4. **Outbox.** Both events are written to `rwb_source_data.outbox_event` in the transaction that writes the freshness stamp (`data_product_load`) and are published by the relay (JOB-11 of the service). Catalog Not on Kafka R6, Outbox and inbox R9 and Delivery rules R7 ("EV-26 and EV-27 are exempt") are changed to "EV-26 and EV-27 are written in the transaction of the freshness stamp". The publish activities are removed (RD-P1-002).
5. **Consumers registered for rwb-source-data** (Events consumer column and ACLs R4 read list):
   - `rwb.case.events.v1`: EV-01 CaseCreated, EV-02 CaseAllocated, EV-04 CaseTransferred, EV-19 TimerBreached (ledger intake, RD-P1-009);
   - `rwb.document.events.v1`: EV-16 DocumentStored (ledger intake);
   - `rwb.decision-record.v1`: EV-08 DecisionRecorded (ledger intake);
   - `rwb.source-data.events.v1` (own topic): EV-26 AceDataReady (reconciliation, case list, stage 2 starts).
   ACLs R4 for rwb-source-data: write `rwb.source-data.events.v1`, `rwb.decision-record.v1`; read the four topics above and their retry topics.
6. **Inbox.** One consumer group per service per topic (Delivery rules R13); ASM-0540's single group across three topics is changed. Group IDs follow RWB-PLT-E1047-CON; working value `rwb-source-data.<topic>`.

**Rationale.** The events have no case, so a caseId key cannot be filled; source + date is the only fact they carry and gives per-source order. The outbox keeps "no event without the change" (Arch v5 slide 22) and removes the double-publish path. Registering the consumers is what lets the P1 principal read in DEV and SIT.

**Affected services.** rwb-source-data; consumers of EV-26/27: rwb-case, rwb-payment, rwb-deviation, rwb-writeoff, gateway-bff, alerts; producers whose topics P1 now reads: rwb-case, rwb-document, every DecisionRecorded producer.

**Affected stories.** RWB-P1-E1011-CON, RWB-P1-E1013-APP, RWB-P1-E1015-APP, RWB-P1-E1015-CON, RWB-P1-E1015-OPS, RWB-P1-E1067-APP, RWB-P1-E1067-CON, RWB-P1-E1001-APP, RWB-P1-E2010-OPS, RWB-P1-E2021-APP; consumers to align: RWB-P2-E1007-CON (key wording).

**Affected documents.** Kafka Topic and Event Catalog v2 → v3 (Topics R4, Events R4–R7, R11, R19, R22, R29, R30 consumer columns, Not on Kafka R6, Outbox and inbox R9, ACLs R4, Delivery rules R7); API v6 → v7 asyncapi/rwb-source-data.asyncapi.yaml (key, typed data, consumers); Event and Messaging Design v6 → v7 (same rows if twinned).

**Findings and themes settled.** TH-16 (Kafka part): RWB-P1-E1011-CON#9, RWB-P1-E1013-APP#11, RWB-P1-E1015-APP#5, RWB-P1-E1015-APP#12, RWB-P1-E1015-CON#4, RWB-P1-E1015-CON#13, RWB-P1-E1015-OPS#3, RWB-P1-E1015-OPS#11, RWB-P1-E1067-APP#9, RWB-P1-E2021-APP#5 (event contract part).

**GAP/ASM.** Changes ASM-0685 (payload is four fields; the other three are envelope attributes) and ASM-0540 (consumer group per topic); closes GAP-0493 key part; changes the catalog exemption recorded against v4 rule Transactions.

**Status.** Proposed – Claude Opus 5.5 (applied). Grain per source and the key come from ASM-0685; the key literal form `{sourceSystem}:{businessDate}`, nullability of completedAt and the group ID working value are Claude Opus 5.5 choices.

**Reuse note.** Any event without a case uses the business key it carries as record key and ce_subject, never caseId, and is written through the outbox in the transaction of the change that caused it. A service that consumes a topic is added to the catalog consumer column and ACL read list in the same change as its consuming story.

#### Register amendments

- Amended by RD-P1-040 (X-02): Rule 5 fourth bullet (own topic, EV-26) is withdrawn; the ACLs R4 read list for rwb-source-data is the three ledger-intake topics and their retry topics. Rule 1: consumers that need one start per date start on the event with sourceSystem ALS and status COMPLETED; inside rwb-source-data the starts are child workflows of AceIngestCheck. CDC-02650 and CDC-02790 stay rejected.
- Amended by RD-P1-024 (X-01): `CaseListBuildWorkflow` is removed from the rule 1 list.
- Amended by RD-P1-040 (X-14): "COMPLETE" as a batch status reads COMPLETED.

**Final ruling (register).** Rules 2-4 and 6 apply. EV-26 is published once per source system and business date (status COMPLETED); downstream daily work starts only on sourceSystem ALS. rwb-source-data reads `rwb.case.events.v1`, `rwb.document.events.v1`, `rwb.decision-record.v1` (ledger intake) and their retry topics, writes `rwb.source-data.events.v1` and `rwb.decision-record.v1`, and does not consume its own topic.

**Values chosen without a source.** Key literal {sourceSystem}:{businessDate}; completedAt nullable; consumer group ID working value rwb-source-data.<topic>

---

## RD-P1-004 · The error envelope is the published Problem schema, extended once

_Original text of batch A kept for audit. Amendments and the final ruling follow it._

**Question.** Stories state the envelope as `code, message, messageId, traceId, field list` (or `type, title, status, detail, instance`); the published `Problem` has `type, title, status, detail, messageCode, messageTh, field, traceId`; RWB-PLT-N009 has `type, title, status, detail, instance, code, traceId`. Which one is built, and which message code goes with which status?

**Options considered.** (1) Story shape – rejected, not RFC 9457. (2) N009 member set – would change 19 published service yamls. (3) Published `Problem` as the base, add the two RFC 9457 members it lacks and the multi-field list, and align N009 (`code` = `messageCode`). Chosen.

**Sources.** Arch v5 slide 11 (RFC 9457 problem details); API v6 rwb-source-data.yaml components.responses E400–E503 and schemas.Problem; RWB-PLT-N009-CON BR1 and §11; RWB-PLT-N009-APP X3–X6; Error and Message Standard v5 rows MSG-GEN-001 to MSG-GEN-007, MSG-P4-001 to MSG-P4-003, MSG-P1-001, MSG-P1-022; Error Handling and Resilience Standard v4 lines 37, 166; Test Cases v8 TC-PLT-N009-APP-01; GR v2 GAP-1401 (a).

**Precedence applied.** Arch v5 fixes RFC 9457 and nothing more. The published yaml and N009 are the same tier; the published yaml is copied in all 19 services and wins on member names; N009's `code` is renamed. Story envelopes are stale. The Error and Message Standard v5 owns message meanings: RWB-P1-E1066-CON's use of MSG-GEN-004 ("Record changed by someone else") for a malformed request, and its text "The request could not be read: {detail}", are wrong and removed.

**Ruling.**
1. **Media type** `application/problem+json` on every 4xx and 5xx.
2. **Problem schema** (component `Problem` in every service yaml, identical): `type` string (URI of the error-map row, required); `title` string (required); `status` integer (required); `detail` string; `instance` string (request path + trace ID; stamped by the owning service, N009); `messageCode` string pattern `^MSG-[A-Z0-9]+(-[A-Z0-9]+)*-\d{3}$` (required on every problem the service writes); `messageTh` string (Thai text of the code, DL10); `field` string (JSON Pointer or parameter/header name of the first failing input); `errors` array of `{field: string, messageCode: string, detail: string}` (only on 400/422 with more than one failing input; Error and Message Standard v5 line 18 "a summary at the top lists them"); `traceId` string, the 32-hex W3C trace ID of the request (required). No other member; no stack trace, SQL, path or personal value.
3. **Status → message code table for rwb-source-data** (each CON story restates its rows against this table only):

| Condition | Status | messageCode |
|---|---|---|
| Body or query fails schema: required value missing | 400 (malformed) / 422 (well-formed but invalid) | MSG-GEN-001 |
| Value out of range | 422 | MSG-GEN-002 |
| Dates in wrong order | 422 | MSG-GEN-003 |
| Value not in its list of values | 400 (query) / 422 (body) | MSG-GEN-007 |
| Idempotency-Key missing, blank or not a UUID | 400 | MSG-PLT-N009-03 |
| Idempotency-Key reused with another request, or in flight | 409 | MSG-PLT-N009-05 |
| Idempotency store unavailable | 503 | MSG-PLT-N009-06 |
| No session or no Workbench role | 401 | MSG-P4-001 |
| Role lacks the right | 403 | MSG-P4-002 |
| Record missing or outside scope | 404 | MSG-P4-003 |
| Stale version / If-Match mismatch (RD-P1-006) | 409 | MSG-GEN-004 |
| If-Match missing on PUT/PATCH (RD-P1-006) | 428 | MSG-GEN-004 |
| State does not allow the action (e.g. rerun of a non-FAILED run) | 409 | the operation's own MSG-P1-nnn (MSG-P1-011 for a run already complete or running) |
| ACE data for the date not complete / product stale | 409 | MSG-P1-001 |
| Ledger cannot be written | 503 | MSG-P1-022 |
| ACE database or other system of record down | 503 | MSG-GEN-006 |

   An unsupported major version (`/v2` not served) answers 404 with `type` `…/unknown-version` and `messageCode` MSG-GEN-007 naming the version as the value; MSG-P4-003 is not used for it. The yaml E400 description is corrected from "MSG-GEN-001" alone to "MSG-GEN-001, MSG-GEN-007, MSG-PLT-N009-03".
4. RWB-PLT-N009-CON/APP BR1 and §11 are changed to this member set (`code` → `messageCode`; `messageTh`, `field`, `errors` added).

**Rationale.** One body, already published in every service file, with the two RFC 9457 standard members and a list for multi-field forms; message meanings stay with the message standard.

**Affected services.** All 19 services (shared Problem); rwb-source-data first; gateway-bff (passes `messageCode` and `detail` through, RWB-PLT-N001-CON).

**Affected stories.** RWB-P1-E1002-CON, RWB-P1-E1011-CON, RWB-P1-E1015-CON, RWB-P1-E1016-CON, RWB-P1-E1017-CON, RWB-P1-E1064-CON, RWB-P1-E1065-CON, RWB-P1-E1066-CON, RWB-P1-E1067-CON, RWB-P1-E2010-CON, RWB-P1-AD018-CON and their APP/OPS twins where they restate errors; RWB-PLT-N009-CON, RWB-PLT-N009-APP.

**Affected documents.** API v6 → v7 `rwb-source-data.yaml` (Problem, E400, new E428); the other 18 service yamls when their services are fixed (reuse note); Error Handling and Resilience Standard v4 → v5 (one line: envelope members); Service Contract Catalog v2 → v3 (§3.3 error envelope line).

**Findings and themes settled.** TH-62: RWB-P1-E1002-CON#5, RWB-P1-E1011-CON#4, RWB-P1-E1016-CON#3, RWB-P1-E1064-CON#3, RWB-P1-E1066-CON#3, RWB-P1-E2010-CON#5.

**GAP/ASM.** Closes GAP-1401 item (a) (published problem-detail schema). No ASM row needed.

**Status.** Proposed – Claude Opus 5.5 (applied). Base members from the published yaml; `instance` from RFC 9457/N009; the `errors` member, the `messageCode` pattern, 428 and the unknown-version answer are Claude Opus 5.5 choices.

**Reuse note.** Every service yaml carries this exact `Problem`; every CON story states errors only as rows of the table above (status, condition, messageCode) and never lists its own envelope members.

#### Register amendments

- Amended by RD-P1-047 (X-04): Table row "State does not allow the action": the messageCode is the one the Error and Message Standard v5 assigns to the operation: MSG-P1-011 for a load or rerun already complete or running, MSG-P2-006 for a retention run of the same run date already running or complete.

**Final ruling (register).** Rules 1-4 apply; the state-conflict row takes the code the Error and Message Standard v5 assigns (MSG-P1-011 load or rerun already complete or running; MSG-P2-006 retention run of the same date running or complete).

**Values chosen without a source.** errors member; messageCode pattern; 428 status; unknown-version answer

---

## RD-P1-005 · One contract file per service; wire names, enums and required flags of rwb-source-data 5.1.0

_Original text of batch A kept for audit. Amendments and the final ruling follow it._

**Question.** Stories and the published yaml/AsyncAPI disagree on property names, enums, required flags and paths; some stories create their own OpenAPI files. Which wins, and what are the corrected values?

**Options considered.** (1) Story wins everywhere; (2) yaml wins everywhere; (3) the published file is the single contract; it wins on names that exist in both, D-RCV-35 descriptions win on meaning, and story-only additions needed by an acceptance criterion are added additively. Option 3 chosen.

**Sources.** API v6 rwb-source-data.yaml (info.version 5.0.0, 12 operations; DataProductFreshness description "D-RCV-35 …"; records op; DataDictionaryField; DataContract; Interaction; InteractionPage); SCC v2 §3.4 (additive change inside v1); Arch v5 slide 32 (`POST /v1/business-days/{date}/ready` 202 idempotent; `GET /v1/business-days/{date}/status` RUNNING, DONE or LATE); AR v2 ASM-0681 (retention-run surface), ASM-0804, ASM-3528, ASM-3542; RWB-P1-E1015-CON §11, RWB-P1-E1016-CON §12.1, RWB-P1-E1017-CON §13, RWB-P1-E1064-CON §11, RWB-P1-E1068-APP §12.1, RWB-P1-E2010-CON §11.

**Precedence applied.** Arch v5 gives the readiness paths and codes. The yaml descriptions marked D-RCV-35 (15 ACE DB Alignment) beat GAP-0492's mapping and the story texts. Otherwise the published yaml beats story text on names.

**Ruling.**
1. **Single file.** `05 Technical architecture/Recovery Workbench API Specification v7/rwb-source-data.yaml` is the only REST contract of rwb-source-data and `asyncapi/rwb-source-data.asyncapi.yaml` the only event contract. Story-local files (`openapi/rwb-source-data-v1.yaml`, `contract/retention-run.yaml`) are not created; a story adds its fragment to the service file. Version **5.1.0** (additive inside `/v1`); `x-service.operations` updated to the new count; the change-log line names this register.
2. **Freshness** (`DataProductFreshness`, owner RWB-P1-E1015-CON): properties `productCode`, `productName`, `sourceSystem`, `businessDate` (date), `sourceExtractedAt` (date-time, = ace_batch_run.completed_at), `loadedAt` (date-time, when the Workbench recorded the stamp), `status` enum `LOADED`, `STALE` (replaces "Current or stale"), `staleSince` (date, first business date with no completed ACE batch; null when LOADED); required `productCode`, `businessDate`, `status`. `staleFlaggedAt` (RWB-P1-AD018-CON) and the started_at/completed_at swap of GAP-0492 are stale. RWB-P1-AD018-CON §11 references this schema and restates no field.
3. **Readiness** (owner RWB-P1-E1015-CON; Arch v5 slide 32): add `POST /business-days/{date}/ready` → 202 with `BusinessDayStatus {businessDate: date, status: enum RUNNING|DONE|LATE}` (Idempotency-Key per RD-P1-001; a repeat for the date replays 202) and `GET /business-days/{date}/status` → 200 `BusinessDayStatus`. The gate value COMPLETE/HOLD is returned by `GET /data-products/freshness` (RWB-P1-E1013-APP §12.1), not by the POST.
4. **Records** (`GET /data-products/{productCode}/records`): `caseId` query `required: true`, format uuid (missing → 400 MSG-GEN-001); `productCode` pattern `^DP(0[1-9]|1[0-4])$`; `page` integer minimum 0 default 0; `size` integer minimum 1 default 50 maximum 200. The row shape stays the published `fields: FieldValue[]` (`fieldName`, `value`, `masked`); the "field map" of RWB-P1-E1016-APP/CON is stale.
5. **Catalog entry** (`DataProductCatalogEntry`): the published properties stay (incl. `sourceViews`); RWB-P1-E1016-CON adds `reconciliations` (array of REC codes, string) and `access` (object: `capabilityArea` string, `right` string) only if its acceptance criteria assert them; any other story-only property is removed from the story.
6. **Data dictionary and contracts:** `sourceSystem` wire enum `ACE`, `WORKBENCH` on `DataDictionaryField` and as the filter value; stored `Workbench` seeds are mapped to `WORKBENCH` on read. `confirmationDocumentId` and `contractId` stay format uuid; fixtures use UUIDs (DOC-SYN-0640 and DC-ACE are display codes, not IDs). The remaining E1064 shape points (interfaceIds, fieldCount) are settled by the E1064 packet against this file under this rule.
7. **Retention runs** (ASM-0681): add `POST /retention-runs` (Idempotency-Key; 202 `{runId}`; 409 active run date; 422 refused rule set) and `GET /retention-runs/{runId}`.
8. **Ledger** (owner RWB-P1-E1066-CON; RD-P1-007): add `GET /cases/{caseId}/interactions/{entryId}` (operationId `getCasesCaseidInteractionsEntryid`; 404 MSG-P4-003 when the entry is not on that case) and query parameter `actor` (string ≤64, matches `actorRef`) on `GET /cases/{caseId}/interactions`.
9. **Every operation** declares 400, 401, 403, 503 and, as applicable, 404, 409, 422, 428 with the RD-P1-004 Problem; every POST declares the `IdempotencyKey` header parameter (RD-P1-001).
10. Stories cite "rwb-source-data.yaml 5.1.0 (API Specification v7)" as their build contract.

**Rationale.** One file per service is what consumers pin and contract tests compare (DoR item 23); the D-RCV-35 meanings are the ACE-aligned ones; additive changes keep `/v1`.

**Affected services.** rwb-source-data; consumers of its reads: gateway-bff, rwb-case, rwb-reporting, rwb-agent, rwb-document, rwb-integration.

**Affected stories.** RWB-P1-AD018-CON, RWB-P1-E1002-CON, RWB-P1-E1015-APP, RWB-P1-E1015-CON, RWB-P1-E1016-APP, RWB-P1-E1016-CON, RWB-P1-E1017-CON, RWB-P1-E1064-CON, RWB-P1-E1066-CON, RWB-P1-E1068-APP, RWB-P1-E2010-CON.

**Affected documents.** API v6 → v7 `rwb-source-data.yaml` and `asyncapi/rwb-source-data.asyncapi.yaml`; Service Contract Catalog v2 → v3 (§6.1 P1 operation list and §7 register entry 5.1.0); Document Index (v7 folder listed).

**Findings and themes settled.** TH-63: RWB-P1-E1015-APP#4, RWB-P1-E1016-APP#8, RWB-P1-E1068-APP#23, RWB-P1-AD018-CON#4, RWB-P1-E1015-CON#2, RWB-P1-E1015-CON#6, RWB-P1-E1016-CON#4, RWB-P1-E1017-CON#7, RWB-P1-E1064-CON#5, RWB-P1-E1064-CON#6, RWB-P1-E1066-CON#14, RWB-P1-E2010-CON#7, RWB-P1-E2010-CON#9. Job shape findings RWB-P1-AD018-CON#2, RWB-P1-E1002-CON#4 → RD-P1-012; RWB-P1-E1064-CON#4 → RD-P1-006; RWB-P1-E1017-CON#7 also by rule 7.

**GAP/ASM.** Confirms ASM-0681 and ASM-3542; supersedes the started/completed mapping recorded under GAP-0492; closes GAP-0563 (readiness shapes).

**Status.** Proposed – Claude Opus 5.5 (applied). Paths and meanings are sourced; enum LOADED/STALE follows the stories; paging bounds (default 50, max 200), the productCode pattern, the `access` object shape and version 5.1.0 are Claude Opus 5.5 choices.

**Reuse note.** For every later service: the published service yaml is the only contract file; a name present in both yaml and story is the yaml's; meaning written under a D-RCV-35 description wins; additive changes bump the minor version of the file and are listed in the catalog register.

#### Register amendments

- Amended by RD-P1-041 (X-13): Rule 2: `businessDate` is nullable (null only for a never-stamped product, or while the Section B flag is off, RD-P1-043 item 3c); required = `productCode`, `status`.
- Amended by RD-P1-020 (X-11): Rule 3: `BusinessDayStatus` adds `changedAt` (date-time, last state change); `GET /business-days/{date}/status` answers 404 MSG-P4-003 for a date with no readiness row.
- Amended by RD-P1-047 (X-04): Rule 7: `POST /retention-runs` answers 202 `{runId, status: ACCEPTED}`, 409 MSG-P2-006 (run of the date running or complete), 409 MSG-PLT-N009-05 (key reuse), 422 MSG-GEN-002 / MSG-P1-002 (rules refused); `GET /retention-runs/{runId}` returns `status`, `countsPerTable[]`, `archiveLocation`, `holdReport`.
- Amended by GAP-2228 directive (X-27): Rule 10 / operation list: the account-page read used by rwb-case is added to `rwb-source-data.yaml` under RWB-P1-E1015-CON once its path is fixed (NEW-GAP-B3).

**Final ruling (register).** Rules 1-10 apply with: `DataProductFreshness.businessDate` nullable (required productCode, status); `sourceExtractedAt` = ace_batch_run.completed_at and `loadedAt` = when the Workbench wrote the stamp (this mapping prevails, X-12); `BusinessDayStatus {businessDate, status, changedAt}` and 404 for an unknown date; retention answers per RD-P1-047 as amended; the account-page read is added under RWB-P1-E1015-CON when its path is fixed.

**Values chosen without a source.** Paging default 50 max 200; productCode pattern; access object shape; version 5.1.0; businessDate nullable (from RD-P1-041); BusinessDayStatus.changedAt (from RD-P1-020)

---

## RD-P1-006 · Optimistic concurrency on PUT and PATCH

_Original text of batch A kept for audit. Amendments and the final ruling follow it._

**Question.** Updates (data-dictionary and data-contract PATCH, flag replacement PUT in RWB-P1-E1018) have no version check, so two users can overwrite each other; RWB-P1-E1064-CON requires If-Match and 428 which the yaml lacks.

**Options considered.** (1) Last write wins; (2) `version` in the body; (3) `ETag`/`If-Match` carrying the row version. Option 3 chosen (HTTP standard, no body change).

**Sources.** Error Handling and Resilience Standard v4 (concurrent update); Error and Message Standard v5 MSG-GEN-004 ("Record changed by someone else"); API v6 rwb-source-data.yaml E409 description ("the record changed … MSG-GEN-004"), `DataDictionaryField.version`, `DataContract.version`; RWB-P1-E1064-CON §4 step 2, AC3; RWB-P1-E1018-APP §12.1 and AC10.

**Precedence applied.** No higher-tier source; the published E409 text and the message standard already name the condition.

**Ruling.** Every GET of an updatable resource returns header `ETag: "<version>"` (the row's version integer). Every PUT and PATCH of rwb-source-data requires `If-Match: "<version>"`: missing → **428**, MSG-GEN-004; not equal to the current version → **409**, MSG-GEN-004, nothing written. A successful write increments `version` by 1 and returns the new `ETag`. A PUT whose body equals the stored values writes no column, does not increment `version` and answers 200 with the stored row. Applies to `PATCH /admin/data-dictionary/fields/{fieldCode}`, `PATCH /admin/data-contracts/{contractId}`, `PUT /extension-facts/parties/{personKey}`, `PUT /extension-facts/accounts/{accountKey}`. PUT/PATCH carry no Idempotency-Key (RD-P1-001 rule 1); RWB-P1-E1064-APP AC11 is limited to `POST /admin/data-contracts/{contractId}/publish`.

**Rationale.** Uses the message and status already published for "the record changed"; makes RWB-P1-E1018 AC10 ("writes nothing new") testable.

**Affected services.** rwb-source-data; gateway-bff (passes ETag/If-Match).

**Affected stories.** RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E1064-OPS, RWB-P1-E1018 (RWB-P1-E1018-APP), RWB-P1-E1016-DB (version column if absent).

**Affected documents.** API v6 → v7 `rwb-source-data.yaml` (headers, E428); Physical schema (a `version` column on `party_ext` and `account_ext` if absent – the E1018 packet checks and raises a REQUEST row).

**Findings and themes settled.** RWB-P1-E1018#13 (TH-13), RWB-P1-E1064-CON#4 (TH-63), RWB-P1-E1064-APP#9 (scope of AC11).

**GAP/ASM.** None closed; no new ASM.

**Status.** Proposed – Claude Opus 5.5 (applied).

**Reuse note.** Every later service uses ETag/If-Match with 428/409 MSG-GEN-004 for PUT and PATCH, and Idempotency-Key only for POST.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

**Values chosen without a source.** ETag/If-Match mechanism and 428 for a missing If-Match

---

## RD-P1-007 · Interaction ledger: one writer, one append contract

_Original text of batch A kept for audit. Amendments and the final ruling follow it._

**Question.** Who writes the interaction ledger, through which path (flat `/interactions` or case-scoped), with which request properties, and how do P1's own producers (proof of delivery, ledger intake, EFS history) and other services append?

**Options considered.** (1) Every producer, including P1 stories, uses REST; (2) P1 stories call the writer component in process and other services use REST on the case-scoped path. Option 2 chosen: a REST call cannot join the read's database transaction (RWB-P1-E1055-APP#4).

**Sources.** T&R DP-18 (ledger owned by rwb-source-data); API v6 rwb-source-data.yaml `POST /cases/{caseId}/interactions` (owner P1, Case record C), `Interaction`, `InteractionRequest`; LDM v10 DF-INT-018 (`interaction.idempotency_key` varchar(120) UK), DF-INT-019 (`case_seq`); AR v2 ASM-3528 and ASM-3542 (case-scoped form), ASM-0538, ASM-0539, ASM-0696, ASM-0697, ASM-0820, ASM-0832; GR v2 GAP-0375, GAP-0504, GAP-2182, GAP-2185, GAP-2255; RWB-P1-E1066-CON §5, §12.1; RWB-P3-E1066-APP §4; RWB-P6-E1055-APP §12.2; RWB-P2-E2001-APP/CON §12.2.

**Precedence applied.** DP-18 (D-RCV-60) fixes the owner. ASM-3528/ASM-3542 (confirmed) fix the case-scoped path; ASM-0696/ASM-0697 (flat path) are superseded.

**Ruling.**
1. **One writer.** Only rwb-source-data writes `rwb_source_data.interaction`, through one component `InteractionLedgerWriter` (append only; no update or delete operation). Inside rwb-source-data, stories call it **in process in their own transaction**: RWB-P1-E1055-APP (proof of delivery), RWB-P1-E1067-APP (ledger intake), RWB-P1-E2034-APP. Every other service appends through REST.
2. **Paths** (base `/api/recovery/source-data/v1`): `POST /cases/{caseId}/interactions` (201 `Interaction`), `GET /cases/{caseId}/interactions` (`InteractionPage`), `GET /cases/{caseId}/interactions/{entryId}`. The flat `/interactions` family is withdrawn from every story, fake and OPS smoke test.
3. **InteractionRequest 5.1.0** (types and lengths from `Interaction`): required `eventCode` (enum of `Interaction.eventCode`), `occurredAt` (date-time), `actorType` (USER|SERVICE|PARTNER), `actorRef` (≤64), `sourceRef` (≤60), `idempotencyKey` (≤120, business key, rule 4); optional `channel`, `direction`, `contactResult` (replaces `result`), `actionCode`, `summary` (≤2000, personal data), `promiseAmount`, `promiseDate`, `contactKey`, `conductCheck`, `decisionLogId`, `correctsEntryId`, `fromHolderRef`, `toHolderRef`, `treatmentId`, `proceedsId`, `documentId` (uuid, new on both schemas, for DOCUMENT_ATTACHED), `deliveryStatus`, `externalRef`. Server-set, never sent: `id`, `caseId` (from the path), `caseSeq`, `sourceSystem` (`WORKBENCH` for REST and intake; `EFS` only for history entries), `retentionClass`. Missing required → 422 MSG-GEN-001 with `field`.
4. **Keys.** The header `Idempotency-Key` (UUID) governs HTTP replay (RD-P1-001). The body `idempotencyKey` is the ledger business key, unique permanently (DF-INT-018). Form: `<code>-<caseNo>-<yyyyMMdd>-<actionId>` where `<code>` is the EV number of the action's event (e.g. `EV-02`) or the ledger eventCode when the action has no event, and `<actionId>` the UUID of the producer's action record (the case-side link row of GAP-2255 for rwb-case); EFS history keeps `EFS:<efs_record_key>` (ASM-0832). A producer that both appends and publishes an event for one action uses the same value in the body and in `ce_idempotencykey` (RD-P1-009). A new header key with an existing business key → **200** with the existing entry (no new entry, no new caseSeq); with a different body → 409 MSG-PLT-N009-05.
5. **Scope check and CASE_CREATED.** The writer checks Case record C of the caller's token and the case through `GET /api/recovery/case/v1/cases/{caseId}` (2 s, one hop). A call made under the rwb-case workload identity (service token, `actorType` SERVICE) skips the case-exists read, because rwb-case appends before its own commit (ASM-0539, GAP-2255); 404 MSG-P4-003 is answered only to user tokens.
6. **Decision records.** An append writes no decision record (ASM-0538 changed): the acting service records its own decision. This also removes the intake loop of RD-P1-009.
7. **Proof of delivery** (RWB-P1-E1055-APP): the date-wide `GET /proof-of-delivery?businessDate=` writes nothing. rwb-comms matches rows to cases and calls `POST /cases/{caseId}/interactions` once per matched `pod_key` with `eventCode` LETTER, `deliveryStatus`, `externalRef` = pod_key, business key `LETTER-<caseNo>-<yyyyMMdd>-<pod_key>`; rwb-comms is the one writer-caller for delivery entries (RWB-P6-E1055-APP §12.2 line 393 kept, line 315 "the P1 read writes it" removed). The repeat count of ASM-0822 moves to the RD-P1-001 rule 7 counter.
8. **EFS history** (RWB-P1-E2001-APP/RWB-P2-E2001-APP): no batch append. The P2 hand-over run reads `GET /efs-history?accountKey=&businessDate=` and calls `POST /cases/{caseId}/interactions` once per row with the mapping: `eventCode` CONTACT (PROMISE when `isPtp`), `occurredAt` = `contactAt`, `actionCode`, `contactResult` RIGHT_PARTY when `isRpc` else empty, `promiseAmount`, `promiseDate`, `actorType` SERVICE, `actorRef` `rwb-integration`, `sourceRef` `EFS v_ace_efs_action`, `idempotencyKey` `EFS:<efsRecordKey>`; `sourceSystem` EFS is set by the writer when the key starts `EFS:`. Written/skipped counts are counted by the P2 run from 201 versus 200 answers.

**Rationale.** Keeps one owner and one table (DP-18), one path family (ASM-3542), and makes every append property explicit so DECISION_TAKEN, CORRECTION, OFFER and PAYMENT can be sent and tested.

**Affected services.** rwb-source-data (writer); rwb-case, rwb-comms, rwb-integration, rwb-document, rwb-payment, rwb-treatment, rwb-partner (REST callers).

**Affected stories.** RWB-P1-E1055-APP, RWB-P1-E1066-APP, RWB-P1-E1066-CON, RWB-P1-E1066-OPS, RWB-P1-E1067-APP, RWB-P1-E1068-APP, RWB-P1-E2001-APP, RWB-P1-E2021-APP, RWB-P1-E2022-APP, RWB-P1-E2034-APP; consumers to align: RWB-P3-E1066-APP, RWB-P6-E1055-APP, RWB-P6-E2021-CON, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2034-CON.

**Affected documents.** API v6 → v7 `rwb-source-data.yaml` (InteractionRequest, Interaction.documentId, entry read); Service Contract Catalog v2 → v3 (three ledger operations); Service Story Catalog v2 R194 (path).

**Findings and themes settled.** TH-22: RWB-P1-E1066-APP#1, RWB-P1-E1067-APP#4, RWB-P1-E1066-APP#2, RWB-P1-E2034-APP#4, RWB-P1-E2001-APP#6, RWB-P1-E1055-APP#4, RWB-P1-E1066-APP#4, RWB-P1-E1055-APP#2, RWB-P1-E1055-APP#1, RWB-P1-E1066-CON#2, RWB-P1-E1066-OPS#1.

**GAP/ASM.** Closes GAP-0375, GAP-0504, GAP-2182, GAP-2185; supersedes ASM-0696 and ASM-0697; confirms ASM-3528 and ASM-3542; changes ASM-0538 (no decision record per append), ASM-0820 and ASM-0822 (writer-caller is rwb-comms; counter), ASM-0832 (counter).

**Status.** Proposed – Claude Opus 5.5 (applied). Owner, path and property types are sourced; the in-process rule, the business-key form, the 200 business repeat, the SERVICE-token scope rule, `documentId`, and the EFS and delivery mappings are Claude Opus 5.5 choices.

**Reuse note.** Every later service that records a case action appends through `POST /cases/{caseId}/interactions` with the full InteractionRequest and the business key form of rule 4, never writes its own copy of the ledger, and records its own decision record for the action.

#### Register amendments

- Amended by RD-P1-007 rule 7 (X-20): Rule 1: the in-process callers are RWB-P1-E1067-APP and RWB-P1-E2034-APP; RWB-P1-E1055-APP does not call the writer.
- Amended by RD-P1-041 (X-19): Rule 7 last sentence: DP07 delivery repeats (ASM-0822) are counted by metric `rwb_source_data_win_delivery_repeat_total`, not by `processed_event`.

**Final ruling (register).** Rules 2-6 and 8 apply. In-process callers of InteractionLedgerWriter: RWB-P1-E1067-APP, RWB-P1-E2034-APP. Delivery entries are appended only by rwb-comms over REST; DP07 delivery repeats are a metric.

**Values chosen without a source.** In-process rule; business-key form; 200 business repeat; SERVICE-token scope rule; documentId; EFS and delivery mappings

---

## RD-P1-008 · Event type name of DecisionRecorded

_Original text of batch A kept for audit. Amendments and the final ruling follow it._

**Question.** `rwb.decision-record.DecisionRecorded.v1` (shared AsyncAPI, RWB-P1-E1067-APP/CON, Service Story Catalog v2) or `rwb.decision.DecisionRecorded.v1` (Kafka catalog, rwb-decision AsyncAPI, RWB-PLT-E1027-CON)?

**Options considered.** The two names above. Chosen: `rwb.decision.DecisionRecorded.v1`.

**Sources.** T&R §R4 and ASM-0209 (type = `rwb.<short>.<Event>.v1` of the owning service; "DecisionRecorded is therefore rwb.decision.DecisionRecorded.v1 on the shared topic"); Kafka catalog Events R11 and Envelope R7; API v6 asyncapi/rwb-decision.asyncapi.yaml (message name and const `rwb.decision.DecisionRecorded.v1`); asyncapi/rwb.decision-record.v1.asyncapi.yaml (stale name); RWB-PLT-E1027-CON.

**Precedence applied.** T&R rule plus confirmed ASM-0209 and two published artefacts against one; the shared AsyncAPI document is stale.

**Ruling.** `ce_type` = `rwb.decision.DecisionRecorded.v1` for every producer; topic stays `rwb.decision-record.v1`; owner P7 rwb-decision (`decision` is the owning short name, `decision-record` is a topic name, not a service). The shared document `asyncapi/rwb.decision-record.v1.asyncapi.yaml` changes its message name and `const` to `rwb.decision.DecisionRecorded.v1` and its description "Produced by rwb-decision" to "Produced by every service through the decision-record library (DP-03); type owner rwb-decision"; `x-consumers` adds `rwb-source-data`. Every story, fixture, fake and ITG that uses `rwb.decision-record.DecisionRecorded.v1` is corrected.

**Rationale.** The naming rule derives the name; two of three published sources already carry it.

**Affected services.** All 19 producers; rwb-decision, rwb-reporting, rwb-source-data (consumers).

**Affected stories.** RWB-P1-E1001-APP, RWB-P1-E1067-APP, RWB-P1-E1067-CON; ITG: RWB-ITG-E1067-ITG.

**Affected documents.** API v6 → v7 `asyncapi/rwb.decision-record.v1.asyncapi.yaml`; Service Story Catalog v2 (event name cell).

**Findings and themes settled.** TH-31: RWB-P1-E1067-APP#1; TH-16: RWB-P1-E1067-CON#8, RWB-P1-E1001-APP#G20.

**GAP/ASM.** Confirms ASM-0209.

**Status.** Proposed – Claude Opus 5.5 (applied) (the answer is in the sources; this register records the pick).

**Reuse note.** The type short name is the owning service's short name even on a shared topic; every consumer filters on `rwb.decision.DecisionRecorded.v1`.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

**Values chosen without a source.** None beyond the cited sources.

---

## RD-P1-009 · Ledger intake: consumed-event map, identity, filtering, retry and parking, ordering

_Original text of batch A kept for audit. Amendments and the final ruling follow it._

**Question.** For the six events the ledger intake consumes: which payload fields map to which ledger properties, where actor and business key come from, which DecisionRecorded events are ledgered (loop), how versions are accepted, what is retried or parked and with what record, how unlisted types and ordering are handled.

**Options considered.** Park in a P2 exception queue vs the topic's `.dlt`; one key (ce_id) vs a business key in an extension attribute; wait-behind-failure ordering vs read-time ordering. Chosen: `.dlt` (ASM-0542), business key in `ce_idempotencykey` (ASM-3716 attributes), read-time ordering.

**Sources.** Kafka catalog Events R4–R7, R11, R19, R22 (payloads), Envelope R6–R14, Delivery rules R4–R13; asyncapi/rwb-case.asyncapi.yaml (`ce_idempotencykey`, `ce_actor`); AR v2 ASM-3716, ASM-0540, ASM-0542, ASM-0207 (consumers never route on ce_source), ASM-0206; GR v2 GAP-0376, GAP-2257; API v6 `Interaction` (sourceRef example "EV-02 CaseAllocated"; holder refs "USER:<user id> or PARTNER:<partner code>"); RWB-P1-E1067-CON §12.4; Test Cases v8 TC-E1-067-03.

**Precedence applied.** Arch v5 slides 11 and 22 (CloudEvents binary, inbox, retry topics then `.dlt` and alert). ASM-0542 and ASM-3716 are confirmed. The "exception queue" wording of RWB-P1-E1067-APP/CON is stale.

**Ruling.**
1. **Envelope attributes required on all six types.** `ce_idempotencykey` (business key, RD-P1-007 rule 4 form, ≤120) and `ce_actor` (`USER:<userId>` | `SERVICE:<service name>` | `PARTNER:<partnerCode>`, ≤74). rwb-document (EV-16) and the decision-record library (EV-08, RWB-PLT-E1027) add both attributes to their AsyncAPI headers, as rwb-case already publishes. `actorType` = the prefix before the first colon; `actorRef` = the rest (≤64).
2. **Map** (`sourceSystem` = WORKBENCH, `occurredAt` = `ce_time`, `caseId` = `data.caseId`, `idempotencyKey` = `ce_idempotencykey`, actor per rule 1 on every row):

| Row | ce_type | Topic | eventCode | sourceRef (literal) | Extra mapping |
|---|---|---|---|---|---|
| 01 | `rwb.case.CaseCreated.v1` | rwb.case.events.v1 | CASE_CREATED | `EV-01 CaseCreated` | – |
| 02 | `rwb.case.CaseAllocated.v1` | rwb.case.events.v1 | CASE_ALLOCATED | `EV-02 CaseAllocated` | `toHolderRef` = `USER:` + `data.ownerId` |
| 03 | `rwb.case.CaseTransferred.v1` | rwb.case.events.v1 | CASE_TRANSFERRED | `EV-04 CaseTransferred` | `fromHolderRef` = `USER:` + `data.fromOwner`; `toHolderRef` = `USER:` + `data.toOwner` |
| 04 | `rwb.case.TimerBreached.v1` | rwb.case.events.v1 | CASE_ESCALATED | `EV-19 TimerBreached` | – |
| 05 | `rwb.document.DocumentStored.v1` | rwb.document.events.v1 | DOCUMENT_ATTACHED | `EV-16 DocumentStored` | `documentId` = `data.documentId` |
| 06 | `rwb.decision.DecisionRecorded.v1` | rwb.decision-record.v1 | DECISION_TAKEN | `EV-08 DecisionRecorded` | `decisionLogId` = `data.entryId`; `approver` not read |

   No personal field is read; `summary`, `channel`, `direction` stay empty.
3. **Filtering.** Any other `ce_type` on these topics is committed and ignored (no inbox row, no entry). A row-06 event with no `data.caseId` is committed and ignored. The loop is removed at source: a ledger append writes no decision record (RD-P1-007 rule 6); no routing on `ce_source` (ASM-0207).
4. **Versions.** The version is the `.vN` suffix of `ce_type` and the registry subject; the intake accepts the current and the previous registered version (catalog Envelope R13). All six are currently `.v1` only; fixtures use `.v1`; the refusal fixture uses an unregistered synthetic version (`rwb.case.CaseTransferred.v9`). "Version 3 accepting 2 and 1" is stale.
5. **Dedupe sequence** (one transaction in `rwb_source_data`): read `processed_event` by `ce_id` → if present, `hit_count + 1`, `last_seen_at`, commit, no entry; else insert `processed_event` (`hit_count` 1) and call `InteractionLedgerWriter` in process; if the business key already exists in `interaction`, no new entry (the inbox row still commits). AC7 expects one entry and `hit_count` 2 after one redelivery (DF-OPS-182).
6. **Retry and park.** Transient failures (database, case read timeout) → retry topics 1 min, 10 min, 1 h, then `<topic>.dlt`. Non-retryable → straight to `<topic>.dlt`: missing `ce_actor` or `ce_idempotencykey`, unsupported version, missing `data.caseId` on rows 01–05, payload failing the registry schema. Every `.dlt` record keeps the original record and `ce_*` headers and adds headers `rwb-dlt-reason` (`MISSING_ATTRIBUTE` | `UNSUPPORTED_VERSION` | `SCHEMA_INVALID` | `RETRIES_EXHAUSTED`), `rwb-dlt-consumer` (`rwb-source-data`) and `rwb-dlt-owner` (`P1 squad`). One alert per record (catalog Dead-letter sheet); incident `LEDGER_WRITE_FAILED` with MSG-P1-022 in its detail is raised only by the intake for `RETRIES_EXHAUSTED` (ASM-0542); the REST writer never raises it for intake calls. Replay through the platform replay tool adds one entry and leaves earlier entries intact.
7. **Ordering.** The intake does not wait behind a failed event (non-blocking retry). `caseSeq` is arrival order. The ledger is read ordered by `occurredAt`, then `caseSeq` (RWB-P1-E1068-APP); RWB-P1-E1067-APP AC6 is restated on read order; "one partition per case across three topics" and the cross-topic inversion report are removed.
8. **Runtime.** Consumer groups per RD-P1-003 rule 6; first start `auto.offset.reset=earliest`; when the intake feature flag is off the consumers are paused and resume from the committed offset; events older than the topic retention (7 days) are recovered only from `.dlt` through the replay tool.

**Rationale.** Uses the attributes rwb-case already publishes, removes the decision loop at source, and keeps the platform's retry and dead-letter path instead of a private queue.

**Affected services.** rwb-source-data; rwb-case, rwb-document, the decision-record library (all producers of EV-08).

**Affected stories.** RWB-P1-E1067-APP, RWB-P1-E1067-CON, RWB-P1-E1066-APP (LEDGER_WRITE_FAILED raiser), RWB-P1-E1068-APP (read order); producers to align: RWB-P5 DocumentStored producer story, RWB-PLT-E1027-CON; ITG: RWB-ITG-E1067-ITG.

**Affected documents.** API v6 → v7 asyncapi/rwb-document.asyncapi.yaml and rwb.decision-record.v1.asyncapi.yaml (headers `ce_idempotencykey`, `ce_actor`); Kafka catalog v3 Envelope (two extension attribute rows; dead-letter header rows); Test Cases v8 TC-E1-067-03 (key example in rule 4 form).

**Findings and themes settled.** TH-31: RWB-P1-E1067-APP#2, #7, #10, #11, #12, #19; RWB-P1-E1067-CON#1, #2, #3, #4, #5, #6, #7, #9, #11, #15; TH-13: RWB-P1-E1067-APP#5, RWB-P1-E1067-APP#6.

**GAP/ASM.** Closes GAP-0376 and GAP-2257; confirms ASM-0542 and the attribute names of ASM-3716; changes ASM-3716 (key shape gains `-<actionId>`) and ASM-0540 (groups per topic; order by occurredAt then caseSeq).

**Status.** Proposed – Claude Opus 5.5 (applied). Payload names, attributes, retry windows and `.dlt` come from sources; the holder prefixes, the `.dlt` header names and values, the v9 fixture, offset policy and the `documentId` mapping are Claude Opus 5.5 choices.

**Reuse note.** Any consumer that turns events into its own records: dedupe on ce_id in `processed_event` in the same transaction, business key from `ce_idempotencykey`, actor from `ce_actor`, non-retryable failures straight to `.dlt` with the three `rwb-dlt-*` headers, never route on `ce_source`.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

**Values chosen without a source.** Holder prefixes; rwb-dlt-* header names and values; v9 refusal fixture; offset policy; documentId mapping

---

## RD-P1-010 · Case-entry read contract: listEligibleAccounts (not entry-candidates) and the hand-over reads

_Original text of batch A kept for audit. Amendments and the final ruling follow it._

**Question.** Does rwb-case get its daily candidates through REST `GET /entry-candidates` (RWB-P1-E1018-APP) or the Temporal activity `listEligibleAccounts` (rwb-case story, catalogs)? Who supplies caller identity, inputs, the date predicate, paging, product group and borrower key, and what happens to `/entry-candidate-facts` (RWB-P1-E2001-APP)?

**Options considered.** REST entry-candidates; Temporal activity. Chosen: the activity (Arch v5 Q1 – no person waits; Arch v5 slide 14 names it).

**Sources.** Arch v5 slide 14 and lines 986, 1035 ("TMP Source data: listEligibleAccounts(businessDate)") and slide 12 (choosing the call type); SCC v2 row 185 (P1 → P3 Temporal activity, class C); Temporal catalog Activities R4; RWB-P1-E1018-APP §4 steps 4–10, §12.1, BR1, BR7, X4; RWB-P1-E2001-APP §1, §12.1; RWB-P3-E1018-APP §4, §12.2; LDM v10 DF-ACE-010 (`product_category`), DF-CAS-012 (`recovery_case.region_code`, Workbench-owned); GR v2 GAP-0571, GAP-0575, GAP-0592.

**Precedence applied.** Arch v5 and the two catalogs name the activity; RWB-P1-E1018-APP's REST read is stale.

**Ruling.**
1. **Contract.** Activity `listEligibleAccounts` on task queue `rwb-source-data`, namespace `rwb-recovery`, published in the rwb-source-data contract jar; called only by `DailyCaseRun` of rwb-case under the rwb-case worker identity (namespace mTLS). `GET /entry-candidates` is not published; `EntryCandidateService` of RWB-P1-E1018-APP implements the activity.
2. **Input** `EligibleAccountsRequest {businessDate: LocalDate (required), threshold: int 0–999 (required; the 90 is a rwb-case parameter, DP-06), pageToken: String (null for the first page), pageSize: int default 500, max 1000}`.
3. **Output** `EligibleAccountsPage {businessDate, threshold, asOf (completed_at of the COMPLETED ALS row), candidates[], breaks[], nextPageToken (null on the last page)}`; a candidate carries the RWB-P1-E1018-APP §12.1 fields (`accountKey`, `accountCode`, `productGroup`, `daysPastDue`, `totalBalance`, `contractNo`, `dataAsOf`, `tdrFlag`, `deceasedFlag`, `disputeOpen`, `deceasedOverride`, `bankruptcy`, `fraudFlag`, `personKey`); a break carries `keyType` (ACCOUNT|PERSON), `businessKey`, `viewName`, `businessDate`. Payloads pass the codec (AES-GCM).
4. **Date predicate.** `v_ace_account.days_past_due >= threshold AND v_ace_account.data_as_of = businessDate`, after the gate: the ALS row of `v_ace_batch_status` for the date is COMPLETE. Otherwise the activity fails **non-retryable** with type `AceBatchNotComplete`, details `{productCode: "DP01", messageCode: "MSG-P1-001", lastCompleteBusinessDate}`; `lastCompleteBusinessDate` is null when the view is absent or holds no complete row. A `businessDate` older than the current `data_as_of` fails non-retryable with type `BusinessDateNotCurrent` (the views hold current state only).
5. **Product group** = ACE `product_category` (DF-ACE-010; E1018 BR7), unvalidated. The product-code map of RWB-P1-E2001-APP is stale.
6. **Borrower key and breaks.** `personKey` and the REC-05 breaks are owned by this activity (RWB-P1-E1018-APP). `region_code` is a rwb-case attribute (DF-CAS-012) and is not served by P1.
7. **Filters.** Exclusion evaluation, the open-case filter and grouping belong to the caller (rwb-case / the P2 hand-over run); P1 returns the exclusion facts only. RWB-P2-E2001-APP/CON text that places them in this read is stale (GAP-0592).
8. **Hand-over reads.** `GET /entry-candidate-facts` is withdrawn: its facts are in the activity output, which DailyCaseRun passes to the hand-over step. `GET /efs-history?accountKey={accountKey}&businessDate={date}` stays (one account per call; Idempotent; caller the rwb-integration workload identity), gated as rule 4 with 409 MSG-P1-001, and rows are cut at `contact_at <= businessDate 23:59:59 Asia/Bangkok`.

**Rationale.** Matches the architecture's call type and the catalogs, removes a second entry path, and puts parameters and filters with their owner (DP-06).

**Affected services.** rwb-source-data; rwb-case (DailyCaseRun); rwb-integration (hand-over run); rwb-decision (RWB-P7-E1018 409 wording).

**Affected stories.** RWB-P1-E1018 (RWB-P1-E1018-APP), RWB-P1-E2001-APP; consumers to align: RWB-P3-E1018-APP, RWB-P3-E1018-CON, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P7-E1018-APP.

**Affected documents.** Temporal catalog v3 Activities R4 (signature); SCC v2 → v3 row 185; API v6 → v7 (no entry-candidates path; efs-history added); Cross-document Change Register (CDC-05378, CDC-05423 resolved).

**Findings and themes settled.** TH-29: RWB-P1-E2001-APP#2, RWB-P1-E2001-APP#16, RWB-P1-E2001-APP#3, RWB-P1-E1018#17, RWB-P1-E1018#1, RWB-P1-E1018#8.

**GAP/ASM.** Closes GAP-0571 (call type and shapes), GAP-0575 (break row), GAP-0592; changes the ASM-0813 and ASM-0817 working reads from REST to the activity.

**Status.** Proposed – Claude Opus 5.5 (applied). Call type, caller and fields are sourced; the request/page type names, page size, failure type names and the history cut-off are Claude Opus 5.5 choices.

**Reuse note.** A machine caller in another service reads P1 through the catalogued activity, never through a parallel REST read; failures of a Temporal contract are typed non-retryable failures carrying the message code in details.

#### Register amendments

- Amended by RD-P1-041 (X-14, X-15): Rule 4: the gate is `DailyCompletenessGate.check(businessDate, [DP01])` (RD-P1-041 item 8); with the RD-P1-021 seed it is the ALS row of `v_ace_batch_status` with status COMPLETED. Failure type `AceBatchNotComplete`, `BusinessDateNotCurrent` and details unchanged; rule 8 uses the same gate.

**Final ruling (register).** Rules 1-3 and 5-8 apply; the gate of rule 4 and rule 8 is DailyCompletenessGate for DP01 (ALS row, status COMPLETED, with the RD-P1-021 seed).

**Values chosen without a source.** EligibleAccountsRequest/EligibleAccountsPage names; page size 500 max 1000; failure types AceBatchNotComplete, BusinessDateNotCurrent; efs-history cut-off

---

## RD-P1-011 · What counts as a published contract fake for DoR item 22, and version pinning

_Original text of batch A kept for audit. Amendments and the final ruling follow it._

**Question.** P1 CON stories list only fakes of contracts they consume; consumers have no provider fake of P1's own operations, events or activities, and no fake version. What must a P1 CON story publish to meet DoR item 22?

**Options considered.** (1) Consumers write their own fakes; (2) the provider CON story publishes a provider fake per artefact, pinned to the contract version. Option 2 chosen.

**Sources.** Definition of Ready and Done v4 §2 items 12, 21, 22, 23 ("A contract fake of that version is in the contract fake library, and every consumer story on class C depends on the contract and builds against the fake (R5.4; R5.5 DP-11)"); T&R §R5.4 class C, §R7 section 12.8; SCC v2 §3.4 and the class C rows ("The provider's published contract and its fake"); Arch v5 slide 11 ("contract tests run in every build").

**Precedence applied.** DoR v4 and T&R; no conflict, only an omission in the stories.

**Ruling.**
1. **A fake is "published"** when the provider's CON story lists it in §12.8 under "Provider fakes" with: the artefact it fakes (OpenAPI operation IDs, AsyncAPI message names, or activity interface and methods); the contract version it is generated from (`rwb-source-data.yaml 5.1.0`, `rwb-source-data.asyncapi.yaml 5.1.0`, contract jar `rwb-source-data-contract 1.x`); the fake artefact and its version equal to the contract version; and the fixture set below. Consumed-contract fakes stay in §12.8 under "Consumed fakes".
2. **Form.** REST: WireMock mappings generated from the yaml, one mapping per documented status of each operation (200/201/202 plus every 4xx/5xx the operation declares, bodies in the RD-P1-004 Problem). Events: one sample record per message (headers and body) validating against the AsyncAPI and the registry subject. Temporal: a fake implementation of the activity interface in the contract jar's `testFixtures`, returning the fixture pages and the typed failures.
3. **Location.** The contract fake library of the platform (RWB-PLT-LIB), path `fakes/rwb-source-data/<contract version>/`; the fake is released with the contract and never edited by a consumer.
4. **Pinning.** Every consumer story states the contract version and the fake version it builds against in §12.2 or §12.4 (DoR item 23); an additive minor version publishes a new fake folder and keeps the previous one.
5. **Contract test.** The provider build runs every fake fixture against the implementation (provider verification); the consumer build runs against the fake; a drift between fake and document fails both builds.
6. **Minimum fixtures** for the four stories named by the checkers: RWB-P1-E1002-CON – the four case-list/job operations (RELEASED, HELD, PENDING rows, 404, paging), `caseListPage` and `listCaseListAccounts` fakes, an AceDataReady sample; RWB-P1-E1011-CON – the two reconciliation result reads (page and single with break rows; 400, 401, 403, 404, 503); RWB-P1-E1015-CON – `GET /data-products/freshness` (LOADED, STALE, not stamped), `POST /business-days/{date}/ready` (202, replay), `GET /business-days/{date}/status` (RUNNING, DONE, LATE), AceDataReady and AceDataLate samples; RWB-P1-E1016-CON – the six reads with 200, 400, 401, 403, 404, 503.

**Rationale.** DoR item 22 speaks of a fake "of that version"; only the provider can publish one that matches its contract, and generating it from the file keeps it from drifting.

**Affected services.** rwb-source-data; every class C consumer of P1.

**Affected stories.** RWB-P1-E1002-CON, RWB-P1-E1011-CON, RWB-P1-E1015-CON, RWB-P1-E1016-CON, and every other P1 CON story (RWB-P1-AD018-CON, RWB-P1-E1017-CON, RWB-P1-E1064-CON, RWB-P1-E1065-CON, RWB-P1-E1066-CON, RWB-P1-E1067-CON, RWB-P1-E2010-CON).

**Affected documents.** Service Contract Catalog v2 → v3 (§3.4 one line: fake per contract version); Definition of Ready and Done v4 (no change; this ruling is its reading).

**Findings and themes settled.** Checker-downgraded DoR 22 findings: RWB-P1-E1002-CON#7, RWB-P1-E1011-CON#1, RWB-P1-E1015-CON#9, RWB-P1-E1016-CON#2.

**GAP/ASM.** None closed; the fake library path is a working value until RWB-PLT-LIB publishes its layout.

**Status.** Proposed – Claude Opus 5.5 (applied).

**Reuse note.** Every service's CON story carries a "Provider fakes" table in §12.8 with artefact, contract version, fake version and fixtures; a CON story with only consumed fakes does not meet DoR item 22.

#### Register amendments

- Amended by RD-P1-024 and RD-P1-020 (X-01, X-17, X-27): Rule 6: the RWB-P1-E1002-CON fixture set is withdrawn (E1002-CON retired). RWB-P1-E1015-CON adds the account-page read fixtures (200, 400, 401, 403, 503) once its path is fixed; RWB-P1-AD018-CON carries the job-operation fixtures (one item per run; statuses PENDING, RUNNING, COMPLETE, FAILED, WAITING; rerun 202, 400, 404, 409, 503). `caseListPage` and `listCaseListAccounts` fakes and RELEASED/HELD/PENDING rows are withdrawn. RWB-P1-AD018-CON is added to the minimum-fixture list.

**Final ruling (register).** Rules 1-5 apply. Minimum fixtures: RWB-P1-AD018-CON (job operations), RWB-P1-E1011-CON, RWB-P1-E1015-CON (freshness, readiness pair, EV-26/27 samples, account-page read once its path is fixed), RWB-P1-E1016-CON. No E1002-CON fixture set.

**Values chosen without a source.** Fake form; fake library path fakes/rwb-source-data/<contract version>/ (working value); minimum fixture sets

---

## RD-P1-012 · Job monitor and rerun: owner, job set, list shape and rerun request

_Original text of batch A kept for audit. Amendments and the final ruling follow it._

**Question.** Two CON stories (RWB-P1-E1002-CON, RWB-P1-AD018-CON) publish `GET /admin/jobs` and `POST /admin/jobs/{jobId}/rerun` with different Job fields, filters, checks and errors; the job set includes other services' jobs; the list returns latest run per job while tests expect every run; the rerun has no body or key yet a 409 depends on a business date.

**Options considered.** Owner: E1002-CON (wave 1 baseline) or AD018-CON. Job set: all Workbench jobs or P1 jobs only. List: latest per job or one row per run. Chosen: E1002-CON owns the v1 baseline and AD018-CON extends it additively; P1 jobs only; one row per run.

**Sources.** API v6 rwb-source-data.yaml `/admin/jobs`, `/admin/jobs/{jobId}/rerun`, `Job`; Batch and Scheduling Design v6 Read me R16 (owners: P1 JOB-01, JOB-04, JOB-09), Jobs R5, R8, R13 (JOB-01 and JOB-09 retired under D-RCV-35); T&R DP-19 (screens through gateway-bff composite routes), DP-15 (Flyway per service); Arch v5 slide 11 (depth one); LDM v10 DF-OPS-224 (run uuid), DF-OPS-225 (JOB-nn); RWB-P1-AD018-CON §4.1–4.3, §12.1 (statuses PENDING, RUNNING, COMPLETE, FAILED, WAITING; two 409 conditions); RWB-P1-E1002-CON §11, §12.1 API-P1-002, checks ROWS_BELOW_ENTRY, ALLOCATION_COMPLETE, PUBLISHED; RWB-ITG-AD018-ITG AC2, TC-AD-018-02 (both runs logged); AR v2 ASM-0632; GR v2 GAP-0440.

**Precedence applied.** D-RCV-35 (yaml description, Batch v6) removes source loads; Arch v5 depth-one and DP-19 rule out P1 operating other services' jobs. The yaml description listing "case intake, outbound files, timers" as P1-served jobs is stale for jobs owned by P3, P2/P6 and the retired JOB-05.

**Ruling.**
1. **Owner.** rwb-source-data provides both operations. RWB-P1-E1002-CON publishes the v1 baseline; RWB-P1-AD018-CON is an additive change to it and lists RWB-P1-E1002-CON as its contract dependency; RWB-P1-E1011-CON references the rerun and restates none of it (its X4, X5 and the rerun clauses of AC6 are removed).
2. **Job set.** Only rwb-source-data runs: `AceIngestCheck`, `CaseListBuildWorkflow` and `ReconciliationWorkflow` (type `JOB-04`), `Stage2ProductWorkflow` and `RetentionRunWorkflow` (type = workflow type string, as they carry no JOB number), per RD-P1-002. Other services' jobs (JOB-02, -03, -06, -07, -08, -10, -12 to -22) are served by their owners; the cross-service monitor screen is a gateway-bff composite route (DP-19) calling each owner – "Pending: per-service job read operations of the other 18 services, owner Solution architect, to be registered as a GAP by the gap agent". Migration runs (`type=MIGRATION`, RWB-PLT-E1044) are not jobs of this operation; those stories read their own Flyway history (DP-15).
3. **List.** `GET /admin/jobs` returns `JobPage {items: Job[], page, size, total}`, **one item per run**, ordered `startedAt` descending. Query: `type` (string, a JOB-nn or a workflow type string; `jobCode` is stale), `status` (enum below), `from`, `to` (format date, on `businessDate`; default `from` = today − 7 days, `to` = today, Asia/Bangkok), `page` (min 0, default 0), `size` (min 1, default 50, max 200).
4. **Job** (names from the yaml; AD018 additions additive): `id` (uuid, run ID, DF-OPS-224; required), `type` (JOB-nn or workflow type; required), `jobName` (string), `workflowId` (string), `runNo` (integer, 1 for the first run of a type and business date), `businessDate` (date; required), `status` enum `PENDING`, `RUNNING`, `COMPLETE`, `FAILED`, `WAITING` (required), `startedAt` (date-time), `endedAt` (date-time; `finishedAt` is stale), `durationMinutes` (integer, null while running), `lastAceBusinessDate` (date), `checks` object whose keys are check codes – for JOB-04 `ROWS_BELOW_ENTRY`, `ALLOCATION_COMPLETE`, `PUBLISHED` – each `{expected: number, actual: number, passed: boolean}`.
5. **Rerun.** `POST /admin/jobs/{jobId}/rerun`: `{jobId}` is the **run ID** (uuid) of a FAILED run; no request body; header `Idempotency-Key` required (RD-P1-001). The business date and type are those of the failed run. Answers: **202** with the new `Job` (status PENDING, `runNo` + 1) – replaced from 200 because the run is started asynchronously; 400 MSG-PLT-N009-03; 404 MSG-P4-003 for an unknown run or a run that is not a P1 run; 409 MSG-P1-011 when the run is not FAILED or a run of the same type and business date is PENDING or RUNNING; 409 MSG-P1-001 when the ACE batch for the business date is not COMPLETE; 409 MSG-PLT-N009-05 for a key reuse; 503 MSG-GEN-006. A rerun starts the workflow of the run's type under its workflow ID (RD-P1-002), Temporal reuse policy ALLOW_DUPLICATE_FAILED_ONLY.
6. **Freshness** in the monitor is `GET /data-products/freshness` of RWB-P1-E1015-CON (RD-P1-005 rule 2); RWB-P1-AD018-CON restates no field.

**Rationale.** One owner, P1's own jobs only (depth one, no cross-service orchestration from P1), a history list that satisfies "both runs are logged", and a rerun whose date comes from the failed run so it needs no body.

**Affected services.** rwb-source-data; gateway-bff (composite monitor route); rwb-integration, rwb-decision, platform (their own job reads, outside P1).

**Affected stories.** RWB-P1-AD018-APP, RWB-P1-AD018-CON, RWB-P1-AD018-OPS, RWB-P1-E1002-APP, RWB-P1-E1002-CON, RWB-P1-E1011-CON, RWB-P1-E1011-OPS; consumers to align: RWB-ITG-AD018-ITG, RWB-PLT-E1044-APP, RWB-PLT-E1044-OPS, RWB-P7-E1008-OPS, RWB-P7-E2013-OPS, RWB-PLT-E1056-OPS, RWB-P2-E2001-APP/CON (no P1 rerun of a JOB-02 step).

**Affected documents.** API v6 → v7 `rwb-source-data.yaml` (`/admin/jobs` params and `JobPage`, `Job`, rerun 202/400/409, description corrected to P1 runs); Batch and Scheduling Design v6 → v7 (JOB-04 workflows); Service Contract Catalog v2 → v3.

**Findings and themes settled.** TH-68: RWB-P1-AD018-APP#7, RWB-P1-E1002-APP#14, RWB-P1-AD018-CON#3, RWB-P1-AD018-CON#8, RWB-P1-AD018-CON#11, RWB-P1-AD018-CON#14, RWB-P1-E1011-CON#5, RWB-P1-E1011-OPS#2; TH-63: RWB-P1-AD018-CON#2, RWB-P1-E1002-CON#4.

**GAP/ASM.** Closes GAP-0440 (job read, rerun answer, job-log fields); changes ASM-0632 (rerun answers 202; job list per run); a new GAP is needed for the other services' job reads (rule 2).

**Status.** Proposed – Claude Opus 5.5 (applied). Operations, statuses, checks and the D-RCV-35 job boundary are sourced; 202, the default window, paging, the `checks` value shape and the `workflowId`/`durationMinutes` semantics are Claude Opus 5.5 choices.

**Reuse note.** A service's job operations list and rerun only its own runs; a rerun is keyed by run ID, takes its business date from the failed run, answers 202 and refuses a non-FAILED run with 409; cross-service monitoring is a gateway-bff composite, never a call chain.

#### Register amendments

- Amended by RD-P1-024 and RD-P1-020 (X-17): Rule 1: RWB-P1-AD018-CON publishes both job operations as the single baseline (no E1002-CON baseline, no additive split); RWB-P1-E1011-CON and RWB-P1-E1015-CON reference the rerun and restate none of it.
- Amended by RD-P1-024 (X-01): Rule 2: `CaseListBuildWorkflow` is removed from the job set. Rule 4: `checks` keys are the codes of RD-P1-020 B (REC-01, REC-02, REC-05); ROWS_BELOW_ENTRY, ALLOCATION_COMPLETE and PUBLISHED are withdrawn.
- Amended by RD-P1-020 (X-16): Rule 2: type JOB-04 is `ReconciliationWorkflow` only; `AceIngestCheck` runs carry type `AceIngestCheck`.
- Amended by RD-P1-040 (X-14, X-18): Rule 5: MSG-P1-001 when the ACE batch is not COMPLETED; the rerun start uses conflict policy FAIL with reuse policy ALLOW_DUPLICATE_FAILED_ONLY.

**Final ruling (register).** Owner RWB-P1-AD018-CON (single publisher). Job set: `AceIngestCheck` (type `AceIngestCheck`), `ReconciliationWorkflow` (type JOB-04), `Stage2ProductWorkflow`, `RetentionRunWorkflow`. List, Job fields and rerun as rules 3-6, with `checks` keyed REC-01, REC-02, REC-05, MSG-P1-001 on a batch not COMPLETED, and rerun start FAIL + ALLOW_DUPLICATE_FAILED_ONLY.

**Values chosen without a source.** 202 rerun answer; default window 7 days; paging; checks value shape; workflowId and durationMinutes semantics; single AD018-CON owner (X-17)

---

## RD-P1-020 · Run, readiness and load-state records of rwb-source-data

_Original text of batch B kept for audit. Amendments and the final ruling follow it._

**Question.** Where are the job run log (RWB-P1-AD018), the run checks behind `GET /admin/jobs` and `POST /admin/jobs/{jobId}/rerun` (RWB-P1-E1002, RWB-P1-AD018), the business-date readiness state (RWB-P1-E1013), the load states of governed loads (RWB-P1-E1016, RWB-P1-E1064) and the sandbox decision records (RWB-P1-E1065) held, and with which table names, columns and types?

**Options considered.**
1. No run table: the log is the Temporal visibility record (ASM-0722).
2. A run table and a run-check child table in `rwb_source_data` (ASM-3464; RWB-P1-AD018-APP section 13).
3. One generic "state" table for runs, readiness and loads.

**Sources.**
- Assumptions Register v2 ASM-0722 (no job-run table) and ASM-3464 (run log rows of `rwb_source_data`, one row per attempt keyed by `job_id`, `business_date`, `run_no`); Gap Register v2 GAP-2162.
- API Specification v6 `rwb-source-data.yaml`: `/admin/jobs/{jobId}/rerun` with `jobId` `format: uuid`; schema `Job` = "A run of a Workbench job from the job catalog" with `id` uuid, `type`, `businessDate`, `status`, `startedAt`, `endedAt`, `checks` ("control totals of the run").
- RWB-P1-AD018-APP sections 4, 9, 11 and 13 (statuses PENDING, RUNNING, COMPLETE, FAILED, WAITING; `run_no` + 1 on a rerun; columns `job_id`, `business_date`, `run_no`, `status`, `started_at`, `finished_at`, `duration_minutes`, check columns, `message_id`).
- Architecture v5 Text Extract v1 slides 15, 31, 32 and 44 (P1 DB "ACE view contract, extension tables, freshness, reconciliation"; `POST /v1/business-days/{date}/ready` answered 202; Airflow sensor polls `GET /v1/business-days/{date}/status` until DONE; JOB-04 in rwb-source-data; JOB-21 uses visibility only for stuck-workflow scans).
- RWB-P1-E1013-APP sections 9 and 12.1 (status values RUNNING, DONE, LATE of the Airflow interface contract; status answer holds date, state and time of last change; 404 for an unknown date).
- Physical Schema v8 `rwb_source_data.sql` (18 tables; no run, readiness or load-state table); LDM v10 (no such entity; `job_catalog` DF-OPS-224 to DF-OPS-232 is P2's).
- Ownership Map v2 sheet Tables R47 and sheet Rulings R11 (`job_catalog` is P2 rwb-integration).
- Microservice Ownership Map v2 sheet Parameters and sheet Rulings R53 to R56; RWB-P1-E1013-APP section 3 (local decision-record library, `rwb.decision-record.v1`, DP-03).

**Precedence applied.** Architecture v5 does not forbid a run table and requires an addressable run (`jobId` uuid in API Specification v6, which follows it); Temporal visibility has no field for per-check control totals and is subject to namespace retention, so ASM-0722 cannot satisfy the published `Job.checks` element. ASM-0722 is superseded by this RD-P1 decision; ASM-3464 is confirmed and completed.

**Ruling.**

A. Table `job_run`, schema `rwb_source_data`, owner P1 rwb-source-data, subject area OPS, data product none (operational record). One row per attempt of a job that runs inside rwb-source-data.

| Field ID | Column | Type | Null | Default / rule |
|---|---|---|---|---|
| DF-OPS-233 | id | uuid | No | gen_random_uuid(); this is `Job.id` and the `jobId` of `POST /admin/jobs/{jobId}/rerun` |
| DF-OPS-234 | job_type | varchar(60) | No | `Job.type`: the job ID `JOB-nn` of the P2 job catalog (format of DF-OPS-225) where the workflow has one, otherwise the Temporal workflow type string (RD-P1-012 rule 2) |
| DF-OPS-235 | business_date | date | No | ACE business date of the run |
| DF-OPS-236 | run_no | integer | No | 1; a rerun writes a new row with `run_no` + 1 and never updates the earlier row |
| DF-OPS-237 | status | varchar(10) | No | 'PENDING'; list LOV-JOB-RUN = PENDING, RUNNING, COMPLETE, FAILED, WAITING (values from RWB-P1-AD018-APP section 9) |
| DF-OPS-238 | workflow_id | varchar(200) | Yes | Temporal workflow ID of the execution (Proposed length) |
| DF-OPS-239 | started_at | timestamptz | Yes | Set on RUNNING |
| DF-OPS-240 | finished_at | timestamptz | Yes | Set on COMPLETE or FAILED; `Job.endedAt` |
| DF-OPS-241 | duration_minutes | integer | Yes | Whole minutes from `started_at` to `finished_at` |
| DF-OPS-242 | message_id | varchar(20) | Yes | Message ID raised by the run, for example MSG-P1-012 (Proposed length) |
| DF-OPS-243 | requested_by | uuid | Yes | User who requested a rerun; null for an event-started run |
| DF-OPS-244 | idempotency_key | varchar(120) | Yes | Idempotency-Key of the rerun request (same type as `interaction.idempotency_key`) |
| DF-OPS-245 | rerun_of_id | uuid | Yes | `job_run.id` of the FAILED run this rerun follows; foreign key kept (same owner) |

Constraints and indexes: `uk_job_run UNIQUE (job_type, business_date, run_no)`; `uk_job_run_idempotency UNIQUE (idempotency_key)`; `ix_job_run_latest ON (job_type, business_date, status)`; `fk_job_run_rerun_of FOREIGN KEY (rerun_of_id) REFERENCES job_run(id)`. These names replace `ux_jobrun` and `ix_jobrun_latest` of RWB-P1-AD018-APP section 13 (Physical Schema naming rule).

B. Table `job_run_check`, schema `rwb_source_data`, owner P1, subject area OPS. One row per check of one run; it carries `Job.checks`.

| Field ID | Column | Type | Null | Default / rule |
|---|---|---|---|---|
| DF-OPS-246 | id | uuid | No | gen_random_uuid() |
| DF-OPS-247 | job_run_id | uuid | No | Foreign key to `job_run(id)`, same owner, `ON DELETE` not allowed (append only) |
| DF-OPS-248 | check_code | varchar(30) | No | List LOV-JOB-CHECK; first values are the JOB-04 reconciliation codes REC-01, REC-02 and REC-05 (the codes `reconciliation_result.rec_code` already carries) |
| DF-OPS-249 | check_result | varchar(8) | No | List LOV-REC-RESULT (PASS, BREAK) |
| DF-OPS-250 | check_count | integer | Yes | Control total counted by the run |
| DF-OPS-251 | expected_count | integer | Yes | Control total it is compared with |

Constraint `uk_job_run_check UNIQUE (job_run_id, check_code)`. The checks ROWS_BELOW_ENTRY, ALLOCATION_COMPLETE and PUBLISHED of RWB-P1-E1002 leave P1 with the case list (RD-P1-024) and are not P1 check codes.

C. Scope of the run log. `job_run` holds runs of the workflows that execute in rwb-source-data only, the job set of RD-P1-012 rule 2: `AceIngestCheck` and `ReconciliationWorkflow` (JOB-04, Ownership Map v2 sheet Jobs R5), `Stage2ProductWorkflow` and `RetentionRunWorkflow` (workflow type strings); `CaseListBuildWorkflow` only if RD-P1-024 is overturned. JOB-01 and JOB-09 are retired (ACE ingestion) and have no rows. Runs of jobs owned by other services stay in their owners (Architecture v5 slide 44: "each job runs in its owning service"); the job catalogue itself is read from P2 (RD-P1-021). A cross-service monitor view is not part of P1.

D. Writer and migration. RWB-P1-AD018-APP writes the one Flyway step `V<seq>__rwb_p1_ad018_job_run.sql` in the `rwb_source_data` sequence (DP-15) creating both tables, the indexes and their dictionary rows (`sys_objects` 2 rows, `sys_fields` 19 rows through the governed dictionary load of RWB-P1-E1064-APP); RWB-P1-AD018-OPS only runs it and does not claim it. The run rows are written by the job runner of RWB-P1-AD018-APP (a workflow-kit interceptor on the JOB-04 workflows); RWB-P1-E1011-APP writes the REC-nn results into `reconciliation_result` and the runner copies the per-check result into `job_run_check` in the same activity transaction.

E. AD018 start rule (RWB-P1-AD018-APP#6). A job starts only when every source system mapped (table `data_product_source`, RD-P1-021) to every data product the job reads is COMPLETE in `v_ace_batch_status` for the business date; otherwise the run is WAITING. The products a job reads are the `productCodes` its workflow passes to `DailyCompletenessGate.check(businessDate, productCodes)` (RWB-P1-E1015-CON); for JOB-04 they are the products named in RWB-P1-E1011-APP section 4.

F. Table `business_day_readiness`, schema `rwb_source_data`, owner P1, subject area OPS. One row per business date for which the readiness call or the fallback poll arrived.

| Field ID | Column | Type | Null | Default / rule |
|---|---|---|---|---|
| DF-OPS-252 | id | uuid | No | gen_random_uuid() |
| DF-OPS-253 | business_date | date | No | The `{date}` of `POST /business-days/{date}/ready` |
| DF-OPS-254 | state | varchar(10) | No | 'RUNNING'; list LOV-READINESS = RUNNING, DONE, LATE (Airflow interface contract, Architecture v5 slide 32; RWB-P1-E1013-APP section 9) |
| DF-OPS-255 | received_at | timestamptz | No | First arrival of the readiness call or fallback poll for the date |
| DF-OPS-256 | changed_at | timestamptz | No | Time of the last state change; returned by `GET /business-days/{date}/status` |
| DF-OPS-257 | idempotency_key | varchar(120) | Yes | Idempotency-Key of the readiness call (the date) |

Constraint `uk_business_day_readiness UNIQUE (business_date)`. `GET /business-days/{date}/status` answers 404 when no row exists for the date. Writer: RWB-P1-E1013-APP, in its own Flyway step `V<seq>__rwb_p1_e1013_business_day_readiness.sql`; state moves are those of RWB-P1-E1013-APP section 9 (DONE requires every mapped source stamped LOADED in `data_product_load` and the JOB-04 reconciliation of the date finished).

G. Load states of governed loads (RWB-P1-E1016-APP#17, RWB-P1-E1064-APP#7). rwb-source-data holds **no load-state table**. A load of `data_product_access`, `data_product`, `data_product_source` or a dictionary change arrives as a reference load of rwb-case (`POST /admin/reference-loads`, `/verify`, `/approve`, `/rollback`, owner P3, Ownership Map v2 sheet Rulings R33, R34, R39, R40) and its states, approver and rollback live in `rwb_case.reference_version` (P3). P1 implements the apply handler of RWB-P3-E1043-CON for its table codes: the handler is idempotent on (table code, version), applies the whole version in one transaction, and records the applied version on its own rows (`data_product_access.access_version`, `sys_field_version.field_version`). For `data_product_access`: at most one row is in force per (`product_code`, `role_code`) on any date; applying version V with `valid_from` D sets `valid_to` = D − 1 (inclusive last day) on the rows of the version it replaces; a re-delivered version is a no-op; a back-dated version (D earlier than the version in force) is refused by the handler with MSG-P1-002 (Proposed). The `data_product_load` table remains only the freshness stamp (DF-OPS-001 to DF-OPS-009) and is not a load-state table.

H. Sandbox decision records (RWB-P1-E1065-APP#8). The smoke check writes its decision records through the platform local decision-record library (RWB-PLT-E1027-CON, DP-03) as rows of `outbox_event` in `rwb_source_data` addressed to `rwb.decision-record.v1`; there is no P1 decision-record table and P1 never writes `rwb_decision.decision_log_entry`. In the sandbox the relay is off (ASM-3710), so the acceptance criterion counts `outbox_event` rows (one per evaluation) and asserts their type and key; case-creation codes are removed from the P1 smoke check.

**Rationale.** The API already publishes a run as a uuid resource with per-check totals; only a table can serve that durably. Readiness needs a durable per-date record for status, change time and 404 on an unknown date. Load approval belongs to the reference-load owner (P3), so a second P1 load-state machine would duplicate it. Decision records are a platform library concern (DP-03).

**Affected services.** P1 rwb-source-data; P3 rwb-case (reference-load states, two new lists); P2 rwb-integration (job catalogue read only); PLT (decision-record library).

**Affected stories.** RWB-P1-AD018-APP, RWB-P1-AD018-OPS, RWB-P1-AD018-CON, RWB-P1-E1002-APP, RWB-P1-E1013-APP, RWB-P1-E1016-APP, RWB-P1-E1064-APP, RWB-P1-E1065-APP, RWB-P1-E1011-APP.

**Affected documents.** Logical Data Model and Data Dictionary v10 → v11 (3 entities, 25 fields, lists LOV-JOB-RUN, LOV-JOB-CHECK, LOV-READINESS); Physical Schema v8 → v9 `rwb_source_data.sql` (3 tables); Reference Data and Lists of Values v5 → v6 (3 lists, starter rows for P1); API Specification v6 → v7 `rwb-source-data.yaml` (`Job.checks` items = `job_run_check`; `POST /business-days/{date}/ready` and `GET /business-days/{date}/status` are not yet in v6 and are added); Assumptions Register v2 (ASM-0722, ASM-3464); Gap Register v2 (GAP-2162).

**Findings and themes settled.** TH-19: RWB-P1-AD018-APP#4, RWB-P1-AD018-APP#5, RWB-P1-AD018-APP#6, RWB-P1-AD018-OPS#5, RWB-P1-E1002-APP#8, RWB-P1-E1013-APP#7, RWB-P1-E1016-APP#17, RWB-P1-E1064-APP#7, RWB-P1-E1065-APP#8.

**GAP/ASM rows closed or changed.** ASM-0722 → Superseded by RD-P1-020. ASM-3464 → Confirmed, completed by RD-P1-020 (table names `job_run`, `job_run_check`). GAP-2162 → run-record part closed by RD-P1-020 (the outbound-action operation of rwb-integration and the enforcement path stay open in GAP-2162). ASM-1614, ASM-3830 (E1064 apply order) → read with ruling G. ASM-3710 → unchanged (relay off in DEV).

**Status.** Proposed – Claude Opus 5.5 (applied).

**Reuse note.** Any service whose story asserts a run, a check or a readiness state copies this pattern: a per-attempt `<owner>` run table with `uk (job_type, business_date, run_no)` (the `job_id` of ASM-3464 and RWB-P1-AD018-APP is renamed `job_type` because the job set includes workflows without a JOB number, RD-P1-012), a child check table keyed by check code, and no load-state table where the load is a rwb-case reference load (P3 owns load states; the owner implements only an idempotent apply handler). Decision records go through the DP-03 library, never a local table.

#### Register amendments

- Amended by register resolution X-16: C: `job_type` JOB-04 is used for `ReconciliationWorkflow` only; `AceIngestCheck` rows carry `job_type` `AceIngestCheck`. The conditional `CaseListBuildWorkflow` clause lapses (RD-P1-024 stands).
- Amended by RD-P1-040 (X-10): F: DONE is set once ALS is stamped; LATE once AceDataLate is published for the date with ALS not COMPLETED (not "every mapped source stamped and JOB-04 reconciliation finished").
- Amended by RD-P1-001 (X-11): F: `business_day_readiness.idempotency_key` holds the UUID Idempotency-Key of the first readiness call, not the date; a repeat for the date is deduplicated by `uk_business_day_readiness` and the workflow ID.
- Amended by RD-P1-040 (X-14): E: "COMPLETE in v_ace_batch_status" reads COMPLETED.

**Final ruling (register).** Tables A, B, D, G, H apply. C: job set AceIngestCheck (`job_type` `AceIngestCheck`), ReconciliationWorkflow (JOB-04), Stage2ProductWorkflow, RetentionRunWorkflow. E: sources COMPLETED. F: DONE once ALS is stamped; LATE once AceDataLate is out with ALS not COMPLETED; `idempotency_key` = UUID header of the first call.

**Values chosen without a source.** Table and column names; DF-OPS-233 to DF-OPS-257; workflow_id varchar(200); message_id varchar(20); LOV-JOB-RUN, LOV-JOB-CHECK, LOV-READINESS codes; MSG-P1-002 for a back-dated access version; job_type AceIngestCheck (X-16)

---

## RD-P1-021 · One owner per table, product, seed and write across P1 and its neighbours

_Original text of batch B kept for audit. Amendments and the final ruling follow it._

**Question.** For each table, data product, seed and write that the P1 stories claim, which service owns it, in which schema, and by which read path do the other services reach it?

**Options considered.** (1) Keep the story readings. (2) Apply Microservice Ownership Map v2 sheet Tables row by row and Architecture v5 slide 41, and give every remaining item one owner by the same rule.

**Sources.** Microservice Ownership Map v2 sheets Tables (R2, R15, R17, R19 to R23, R29 to R36, R37, R38, R39, R45, R47, R51, R61 to R67, R73, R77 to R79, R86 to R88, R93), Parameters and Rulings; Architecture v5 Text Extract v1 slides 10, 15, 41 and 44; LDM v10 sheet Entities (R17, R18, R23, R93, R94); Reference Data and Lists of Values v5 sheets Reference tables and Reference data starter; RWB-P1-E1015-APP sections 3, 4 and 12.7; RWB-P1-E1015-OPS section 3; RWB-P1-E1016-APP sections 4 and 12.7; RWB-P1-E1065-APP sections 4, 11, 12.7; RWB-P1-AD018-APP sections 4.5, 12.2, 12.7; Assumptions Register v2 ASM-1967, ASM-0707, ASM-3476, ASM-0727, ASM-3479; Gap Register v2 GAP-2166, GAP-2172; Definition of Ready and Done v4 item 20.

**Precedence applied.** Architecture v5 slide 41 and the Ownership Map v2 (D-RCV-60) over FSD P1 v3 A2.2/A2.2.2 and TSD P1 v3 T3.5/T3.6 (other documents). Where the Ownership Map is silent (product-to-source map, cut-off), the owner of the table the value describes owns it.

**Ruling.**

| Item | Owner | Schema | How others reach it | What P1 stories do |
|---|---|---|---|---|
| `job_catalog` | P2 rwb-integration | rwb_integration | `GET /api/recovery/integration/v1/admin/scheduled-jobs` (x-module P2), one hop, 2 s, GET retried once with jitter; fake from the P2 contract | RWB-P1-AD018-APP removes `job_catalog` from 12.7, adds the call to 12.2, a fake to 12.8 and RWB-P2 contract dependency; the DP-06/DP-07 claim for `job_catalog` is deleted |
| `job_run`, `job_run_check`, `business_day_readiness` | P1 | rwb_source_data | P1 operations only | RD-P1-020 |
| Product-to-source map | P1 | rwb_source_data | P1 operations; the gate | New table `data_product_source` below |
| Cut-off time per product | P1 | rwb_source_data | `data_product.expected_by` (DF-REF column of `data_product`) | RWB-P1-E1015-APP/OPS read `expected_by` from `data_product` only; the "loaded through the rwb-case reference-data contract" reading is the **change route**, not the owner (ruling below) |
| `data_product`, `data_product_access`, `data_product_load`, `data_contract`, `sys_objects`, `sys_fields`, `sys_field_version`, `reconciliation_result`, `interaction`, `efs_ledger_outcome`, `dp_treatment`, `dp_guarantee_claim`, `party_ext`, `contact_point_ext`, `account_ext`, `valuation_ext` | P1 | rwb_source_data | P1 contracts | unchanged |
| `case_list_row` | none (dropped) | – | – | RD-P1-024 |
| `lake_copy_watermark` | none (dropped, Ownership Map v2 Rulings R12) | – | – | not created |
| `retention_rule`, `retention_action` | P5 rwb-document | rwb_document | rwb-document contract | not created in P1 (Ownership Map v2 Rulings R18) |
| `role`, `permission`, `masking_rule`, `delegation_limit` | P4 rwb-access | rwb_access | RWB-P4-E1037-CON (DP-08) | never seeded or held by P1 |
| `parameter_catalog`, `parameter_value` | P3 rwb-case | rwb_case | RWB-P3-E1042-CON (DP-06) | RD-P1-028 |
| `lov_value`, `reference_row`, `reference_version` | P3 rwb-case | rwb_case | RWB-P3-E1043-CON (DP-07) | read only |
| `partner`, `partner_instruction`, `partner_user` | S9 rwb-partner | rwb_partner | rwb-partner contract | DP08 catalog row stays a P1 row with system of record "Recovery Workbench"; its records are S9's |
| `document`, `document_field` and the other DP10 tables | P5 rwb-document | rwb_document | rwb-document contract | not read by P1 (ASM-1967) |
| `decision_log_entry` | P7 rwb-decision | rwb_decision | P7 contract; P7 calls P1's `FreshnessQuery` | P1 never reaches it |
| `recovery_case`, `case_account`, `case_party`, case status history | P3 rwb-case | rwb_case | rwb-case contracts | not seeded or read by table in P1 |

**New table `data_product_source`** (schema `rwb_source_data`, owner P1, subject area REF, data product DP14): one row per data product and ACE source system that feeds it.

| Field ID | Column | Type | Null | Rule |
|---|---|---|---|---|
| DF-REF-300 | id | uuid | No | gen_random_uuid() |
| DF-REF-301 | product_code | varchar(25) | No | LOV-DATA-PRODUCT; foreign key to `data_product(product_code)` (same owner) |
| DF-REF-302 | source_system | varchar(20) | No | The `source_system` value of `recovery.v_ace_batch_status` (varchar(20) in ACE Source Views v1) |

Constraint `uk_data_product_source UNIQUE (product_code, source_system)`. Seed (Proposed, from the system-of-record text of RD-P1-025; codes to be confirmed against the ACE `ace_batch_run.source_system` code list, owner ACE team, OQ-P1-01/OQ-P1-02): DP01 ALS; DP02 SCBPDM and the core bank; DP04 the core bank; DP05 EFS; DP06 CCMS, SVAF, AMIS, RPS; DP07 LIT, WIN; DP11 COLLINS; DP13 ALS, GL. Workbench-only products (DP03, DP08, DP09, DP10, DP12, DP14) have no row and are never STALE. Created and seeded by RWB-P1-E1001-APP in its baseline step; its later changes, and changes to `data_product.expected_by` and `data_product_access`, arrive as reference loads through the apply handler of RWB-P3-E1043-CON (RD-P1-020 G) and are stored only in `rwb_source_data`. This settles the two readings of RWB-P1-E1015-APP/OPS: owner P1, change route rwb-case reference load, runtime read local.

**Products served by `GET /data-products/{productCode}/records`** (RWB-P1-E1016-APP step 5): P1 serves DP01, DP02, DP04, DP05, DP06, DP07, DP11 and DP13 only, from the `recovery.v_ace_*` views and its own tables (`party_ext`, `contact_point_ext`, `account_ext`, `valuation_ext`, `interaction`, `dp_treatment`, `dp_guarantee_claim`). DP03, DP08, DP09, DP10, DP12 and DP14 are held by P3, S9, S6, P5, P7 and the DP14 owners; for them the operation answers 400 E400 with a problem detail naming the owning service, and gateway-bff routes the panel to the owner's contract (Architecture v5 slide 10). The message ID of that 400 is Pending: new MSG-P1 entry, owner product owner with the Error and Message Standard owner, to be registered as a GAP by the orchestrator. The case's account keys come from the rwb-case case contract (RD-P1-024), not from `case_list_row`.

**Data product and cutover writer of consent and contact quality.** `contact_point_ext` is P1's table in data product DP02 (LDM v10 Entities R94). The cutover rows are written by RWB-P1-DM005-APP in the same transaction as its interaction rows (ASM-3476, ASM-0727; RWB-P1-DM002-APP section 8); RWB-P1-DM002-APP writes `party_ext` only. FSD P1 v3 A2.2 (DP05 allocation) is stale. The interaction rows carry `person_key` (DF-INT-003) and `contact_key` (DF-INT-022), which exist in Physical Schema v8 `interaction` (closes the "no column" reading of RWB-P1-DM005-APP#1, see RD-P1-027).

**DM006.** S5 rwb-asset writes the asset rows; P1 holds only `valuation_ext` (Ownership Map v2 R93); the "owner not specified" and "excluded" lines of RWB-P1-DM006-APP sections 11 and 19 are replaced by this split.

**RWB-P1-E1065-APP.** The P1 sandbox seeds only P1 tables and ACE synthetic rows. Role and permission rows and test users (AC10, BR6) move to RWB-P4-E1065-APP; the case status change of AC12 moves to RWB-P3-E1065-APP. RWB-P1-E1065-APP keeps a note naming both.

**RWB-P1-E1066-APP.** Proof-of-delivery writes, the DP07 `duplicate_count`, the rwb_case link table and EFS key folding are removed from section 7 Target reading and listed in a note naming their owning stories (RWB-P1-E1055-APP for proof of delivery, RWB-P1-E1015-APP for `duplicate_count`, RWB-P3 for the case link); the story keeps the ledger writer's duties only.

**RWB-P1-E1015-CON.** P7 calls `FreshnessQuery` (provided by rwb-source-data) and writes its own snapshot in `rwb_decision`; the sentence "reaches this capability only through FreshnessQuery" is removed from 12.7.

**RWB-P1-E1064-CON consumers.** Section 18 lists RWB-P4-E1064-APP, RWB-P5-E1016-APP, RWB-P6-E1046-APP and the ITG stories E1016, E1025 and E1037 as consumers. The dictionary field reads (`GET /admin/data-dictionary/fields`, `/fields/{fieldCode}`) are owned by RWB-P1-E1064-CON; RWB-P5-E1016-APP's citation of RWB-P1-E1016-CON for them is corrected (REQUEST to the P5 owner).

**Rationale.** One owner per table is the Ownership Map's purpose; the remaining items follow "the owner of the table owns the value". Splitting owner from change route lets P1 keep its catalog local (no runtime hop for the gate) while the approval workflow stays P3's (DP-07, DoR item 20).

**Affected services.** P1, P2, P3, P4, P5, P6, P7, S5, S6, S9, gateway-bff.

**Affected stories.** RWB-P1-AD018-APP, RWB-P1-AD019-APP, RWB-P1-DM002-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM008-APP, RWB-P1-E1001-APP, RWB-P1-E1015-APP, RWB-P1-E1015-CON, RWB-P1-E1015-OPS, RWB-P1-E1016-APP, RWB-P1-E1064-CON, RWB-P1-E1065-APP, RWB-P1-E1066-APP, RWB-P4-E1065-APP, RWB-P3-E1065-APP, RWB-P5-E1016-APP, RWB-P6-E1046-APP.

**Affected documents.** LDM v10 → v11 (`data_product_source`, DF-REF-300 to DF-REF-302); Physical Schema v8 → v9 `rwb_source_data.sql`; Microservice Ownership Map v2 → v3 (add `job_run`, `job_run_check`, `business_day_readiness`, `data_product_source` as P1; retire `case_list_row`); Service Contract Catalog v2 → v3 (P1 consumes P2 scheduled-jobs; P7 consumes FreshnessQuery; P1-E1064-CON consumers); FSD P1 v3 A2.2/A2.2.2 (stale, named); API Specification v6 → v7 (`productCode` values of the records operation).

**Findings and themes settled.** TH-20: RWB-P1-E1015-APP#18, RWB-P1-DM002-APP#4, RWB-P1-DM008-APP#4, RWB-P1-AD018-APP#1, RWB-P1-E1016-APP#5, RWB-P1-E1065-APP#6, RWB-P1-E1065-APP#14, RWB-P1-AD018-APP#24, RWB-P1-AD019-APP#2 (key scope, with RD-P1-022), RWB-P1-DM005-APP#2, RWB-P1-DM006-APP#1, RWB-P1-E1066-APP#19, RWB-P1-E1015-CON#20, RWB-P1-E1015-OPS#12, RWB-P1-E1064-CON#20.

**GAP/ASM rows closed or changed.** GAP-2172 → Closed by RD-P1-021 (partner tables S9). GAP-2166 → owning data product of `contact_point_ext` closed (DP02) and key placement closed (DF-INT-003, DF-INT-022); the cutover extract layout part moves to RD-P1-027. ASM-1967, ASM-0707, ASM-3476, ASM-0727 → Confirmed. ASM-3479 → read with the DM006 split above.

**Status.** Proposed – Claude Opus 5.5 (applied).

**Reuse note.** Later service fixes take the owner from Ownership Map v2 (to be v3) and never from an FSD/TSD table list; a catalog or configuration table can be owned by the service that reads it at run time while its approved changes arrive through the rwb-case reference-load handler. A records or read operation serves only the owner's data and answers 400 with the owning service for anything else; gateway-bff composes.

#### Register amendments

- Amended by RD-P1-007 (X-20): RWB-P1-E1066-APP note: proof-of-delivery appends belong to RWB-P6-E1055-APP (rwb-comms, over REST); RWB-P1-E1055-APP owns only the read.
- Amended by RD-P1-041 (X-23): DP14: P1 reads `v_ace_holiday` internally for the expected business date (RD-P1-041 item 1); the records operation still answers 400 for DP14 until NEW-GAP-X2 is closed.

**Final ruling (register).** The ownership table applies. Proof-of-delivery appends: RWB-P6-E1055-APP over REST. DP14: `v_ace_holiday` read internally by P1; records operation answers 400 for DP14 pending NEW-GAP-X2.

**Values chosen without a source.** data_product_source and DF-REF-300 to DF-REF-302; seed source codes (to be confirmed by ACE team)

---

## RD-P1-022 · One owner each for reconciliation, freshness stamps, events, gate and readiness

_Original text of batch B kept for audit. Amendments and the final ruling follow it._

**Question.** RWB-P1-E1011-APP, RWB-P1-E1013-APP, RWB-P1-E1015-APP and RWB-P1-AD019-APP each build parts of the same reconciliation workflow, freshness stamps, events, completeness gate and readiness surface. Which story owns which part?

**Options considered.** (1) Merge into one story. (2) Keep four stories, each owning one disjoint part, with explicit build dependencies. (3) Let E1013 own the whole readiness chain.

**Sources.** RWB-P1-E1011-APP sections 1, 4, 12.2, 12.5, 13 (`ReconciliationWorkflow`, REC-01, REC-02, REC-05, `ix_reconciliation_date`, three rwb-case reads); RWB-P1-E1013-APP sections 1, 4 step 8, 7 AC7 and AC9, 8 BR1 to BR13, 9, 12.1, 12.5, 13 (`V1013_1__reconciliation_result_index`; AceIngestCheck workflow ID "Not specified" CG-ALL-2092); RWB-P1-E1015-APP sections 4, 12.5, 12.7 (`AceIngestCheckWorkflow`, one run per source system and business date, listener on `v_ace_batch_status`, cut-off Schedules at `expected_by`); RWB-P1-E1015-CON sections 1, 12; RWB-P1-AD019-APP sections 1, 4, 11, 17; RWB-ITG-AD019-ITG v2 AC2; Architecture v5 Text Extract v1 slides 15, 31, 32, 44 (readiness call is the main path, the ACE batch-record poll the fallback; AceDataLate at 05:30; JOB-04 in rwb-source-data); Data Quality and Reconciliation Rules v4 (per-service reconciliation); RWB-P3-E1002-APP v2 section 7 (REC-05 of RWB-P1-E1011 lists `case_account.account_key` orphans); Gap Register v2 GAP-2228 resolution ("leave REC-01 and REC-05 with RWB-P1-E1011").

**Precedence applied.** Architecture v5 (readiness call main, poll fallback; one service) and GAP-2228 resolution (D-RCV-60 directive) over the duplicated story texts.

**Ruling.**

| Part | Owning story (builds) | Contract story (publishes) | Others |
|---|---|---|---|
| `ReconciliationWorkflow` (JOB-04 reconciliation), activity `reconciliation`, REC-01, REC-02, REC-05, writes to `reconciliation_result`, index `ix_reconciliation_date`, `GET /admin/reconciliation/results`, feature flag `rwb.source-data.daily-gate` | RWB-P1-E1011-APP | RWB-P1-E1011-CON | RWB-P1-E1013-APP removes step 8, AC7 and `V1013_1__reconciliation_result_index`; RWB-P1-AD019-APP becomes a delta on E1011 |
| Workflow type `AceIngestCheck` (Java interface may be `AceIngestCheckWorkflow`), activities `stampProducts`, `markStale`, `checkDailyCompleteness`, `publishAceDataReady`, `publishAceDataLate`; writes to `data_product_load`; the two events `rwb.source-data.AceDataReady.v1` and `rwb.source-data.AceDataLate.v1`; `GET /data-products/freshness`; `FreshnessQuery`, `DailyCompletenessGate`; the 05:30 Schedule `rwb-source-data-ace-late-check` and the durable timers that replace the per-product cut-off Schedules (RD-P1-040 item 3); the fallback poll of `v_ace_batch_status` | RWB-P1-E1015-APP | RWB-P1-E1015-CON | RWB-P1-E1013-APP removes these from 4 steps 3 to 6 and 10, 12.3, 12.5 |
| `POST /business-days/{date}/ready`, `GET /business-days/{date}/status`, table `business_day_readiness` (RD-P1-020 F), `GET /payments?accountId=`, activities `listEligibleAccounts` and `snapshot(page)` | RWB-P1-E1013-APP | RWB-P1-E1015-CON (readiness pair, as the single freshness-and-readiness surface); RWB-P9-E1013-CON stays the consumer contract | – |
| Data quality console screen reads and data-steward actions over `reconciliation_result` | RWB-P1-AD019-APP | RWB-P1-E1011-CON | – |

Workflow identity (closes CG-ALL-2092; taken from RD-P1-002 and RD-P1-040, which carry TWAC v2 sheet Workflows R18 and R19 and ASM-0689): `AceIngestCheck` runs once per business date with workflow ID `ace-ingest-check-{businessDate}` (ISO yyyy-MM-dd), and stamps each source system of `data_product_source` (RD-P1-021) inside that one run. Its starters are those of RD-P1-040 item 1: (a) the readiness handler of RWB-P1-E1013-APP behind `POST /business-days/{date}/ready`; (b) the 05:30 Schedule; (c) the Control-M fallback poll; all with conflict policy USE_EXISTING, so a repeat never starts a second open run. The per-source-and-date grain of RWB-P1-E1015-APP section 12.5 is stale. `ReconciliationWorkflow` runs once per business date with workflow ID `recon-{businessDate}`; its parent is set by RD-P1-040 item 5, or by the cross-batch note above if RD-P1-024 stands.

Build dependencies: RWB-P1-E1013-APP depends on RWB-P1-E1015-APP and RWB-P1-E1011-APP (build); RWB-P1-AD019-APP depends on RWB-P1-E1011-APP (build, "H" dependency) and lists only its delta; RWB-P1-E1015-CON depends on nothing in E1013.

REC-05 key scope (RWB-P1-AD019-APP#2, with RD-P1-021): REC-05 resolves (a) the business keys held on P1's own tables (`account_ext.account_key`, `party_ext.person_key`, `contact_point_ext.contact_key`, `valuation_ext.valuation_key`, `interaction.person_key`, `interaction.contact_key`) against their `recovery.v_ace_*` views, and (b) `case_account.account_key` and `case_party.person_key` of open cases, read from a paged key-list read of the rwb-case case contract for the business date (operation in RWB-P3 case contract; path Pending, owner rwb-case service owner, to be registered as a GAP). `asset_key` and `payment_code` are removed from the REC-05 scope (no P1 table holds them; their owners S5 and P8 reconcile their own keys under Data Quality and Reconciliation Rules v4). The ITG orphan of RWB-ITG-AD019-ITG AC2 (`case_party` person_key P0099881) is produced through (b).

E1013 scope cut (RWB-P1-E1013-APP#22, #23): with the reconciliation removed, 12.2 stays "None at run time" except the readiness chain's own reads; BR1, BR2, BR5 and BR7 (P9 measure rules) leave section 8 and are referenced as RWB-P9-E1013-APP's; AC9 is split into component tests of the activities this story keeps; an Open decisions row lists DL25 and DL43.

"Events belong to" statements: RWB-P1-E1017-CON, RWB-P1-E1065-CON, RWB-P1-E1066-CON and RWB-P1-E1067-CON are corrected to "the events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1015-APP (published in RWB-P1-E1015-CON)", matching RWB-P1-E2010-CON.

**Rationale.** Architecture v5 names one AceIngestCheck and one reconciliation workflow for P1; the main start is the readiness call and the fallback is the poll, so both starters must hit the same workflow identity. Giving each part one story removes the duplicate migrations and duplicate events.

**Affected services.** P1; P3 (key-list read); P9 (measures contract unchanged).

**Affected stories.** RWB-P1-E1011-APP, RWB-P1-E1011-CON, RWB-P1-E1013-APP, RWB-P1-E1015-APP, RWB-P1-E1015-CON, RWB-P1-AD019-APP, RWB-P1-AD019-OPS, RWB-P1-E1017-CON, RWB-P1-E1065-CON, RWB-P1-E1066-CON, RWB-P1-E1067-CON, RWB-P1-E2010-CON, RWB-ITG-AD019-ITG, RWB-ITG-E1013-ITG.

**Affected documents.** Service Contract Catalog v2 → v3 (readiness pair under RWB-P1-E1015-CON; P1 consumes the rwb-case key list); API Specification v6 → v7 (readiness pair); Microservice Realignment Tracker (workflow IDs).

**Findings and themes settled.** TH-27: RWB-P1-E1013-APP#1, RWB-P1-E1013-APP#2, RWB-P1-E1013-APP#22, RWB-P1-E1013-APP#23, RWB-P1-E1011-APP#10, RWB-P1-AD019-APP#1, RWB-P1-E1015-CON#1; with RD-P1-021, RWB-P1-AD019-APP#2.

**GAP/ASM rows closed or changed.** CG-ALL-2092 (workflow ID form) → closed by RD-P1-022 with the ID of RD-P1-002 and RD-P1-040. GAP-2228 (reconciliation ownership part) → confirmed: REC-01 and REC-05 stay with RWB-P1-E1011.

**Status.** Proposed – Claude Opus 5.5 (applied).

**Reuse note.** When two stories of one service build the same workflow, the rule is: one APP story builds the workflow and its tables, one CON story publishes its surface, every other story consumes it with a build dependency; workflow IDs follow the TWAC catalog (`<kebab-name>-{businessDate}` for daily runs) and every starter uses conflict policy USE_EXISTING on that ID.

#### Register amendments

- Amended by RD-P1-010 (X-06): `listEligibleAccounts` is built by RWB-P1-E1018-APP; RWB-P1-E1013-APP keeps `snapshot(page)`, the readiness pair, `business_day_readiness` and `GET /payments?accountId=`.
- Amended by RD-P1-003 (X-07): `publishAceDataReady` and `publishAceDataLate` are not activities; the outbox rows are written in the stamp transaction.
- Amended by RD-P1-024 (X-01): Workflow identity: the parent of `ReconciliationWorkflow` is `AceIngestCheck` (child, ABANDON, after the ALS stamp).
- Amended by GAP-2228 directive (X-27): RWB-P1-E1015-CON also publishes the account-page read built by RWB-P1-E1002-APP.

**Final ruling (register).** Part ownership: ReconciliationWorkflow (child of AceIngestCheck) - RWB-P1-E1011-APP / RWB-P1-E1011-CON; AceIngestCheck, stamps, outbox events, freshness, gate, 05:30 Schedule, poll - RWB-P1-E1015-APP / RWB-P1-E1015-CON; readiness pair, `business_day_readiness`, `GET /payments`, `snapshot(page)` - RWB-P1-E1013-APP / RWB-P1-E1015-CON; `listEligibleAccounts` - RWB-P1-E1018-APP; account-page read - RWB-P1-E1002-APP / RWB-P1-E1015-CON; console - RWB-P1-AD019-APP / RWB-P1-E1011-CON.

**Values chosen without a source.** Removal of asset_key and payment_code from REC-05 scope

---

## RD-P1-023 · Case identifier in paths, queries and payloads

_Original text of batch B kept for audit. Amendments and the final ruling follow it._

**Question.** Do P1 operations take the case uuid or the case number as `caseId`?

**Options considered.** (1) uuid `recovery_case.id`. (2) Case number `case_no`. (3) Accept both with a lookup.

**Sources.** API Specification v6 `rwb-source-data.yaml` (`/cases/{caseId}/interactions` GET and POST: `caseId` `format: uuid`; E400 "Bad request. The request is malformed. Messages MSG-GEN-001"); Data Dictionary v10 DF-INT-002 `interaction.case_id` uuid; LDM v10 DF-RPT-003 `case_id` uuid; Physical Schema v8 `interaction.case_id uuid` and `case_list_row.case_no varchar(18)`; Screen Specifications v1 SCR-03 `recovery_case.case_no` 'RW-YYYY-NNNNNN'.

**Precedence applied.** The published API contract and the dictionary (uuid) over story criteria that pass a case number.

**Ruling.** Every P1 path, query and payload element named `caseId` (and every column `case_id`) is the uuid `rwb_case.recovery_case.id`. The case number (`case_no`, format `RW-YYYY-NNNNNN`, varchar(18)) is a display value only, is never a P1 key, and P1 offers no case-number lookup. A `caseId` that is not a uuid answers **400** (E400, MSG-GEN-001) before any read. Fixtures give each case a synthetic uuid and keep the case number beside it as display data, for example case `RW-2026-000102` ↔ a fixed synthetic uuid declared once in the story's section 16 fixture table. RWB-P1-E1055-APP replaces `RC-2026-000123` (not a case-number format) with a fixture uuid; RWB-P1-E1068-APP, RWB-P1-E2007-APP and RWB-P1-E1016-APP state `caseId` as the case uuid and pass fixture uuids in their criteria. A case that rwb-case does not return answers 404 (E404). RWB-P1-E2007-APP's "the case reference" becomes "the case uuid"; its read of `case_list_row` follows RD-P1-024.

**Rationale.** The contract and every key column are uuid; a second identifier would need a lookup that only rwb-case can serve and would add a hop.

**Affected services.** P1; P3 and gateway-bff as callers (pass the uuid they already hold).

**Affected stories.** RWB-P1-E1016-APP, RWB-P1-E1016-CON, RWB-P1-E1055-APP, RWB-P1-E1068-APP, RWB-P1-E2007-APP, RWB-P1-E1066-APP, RWB-P1-E1067-APP.

**Affected documents.** API Specification v6 → v7 (add the 400 for a non-uuid `caseId` on every P1 operation that takes it); Test Cases (fixture uuids).

**Findings and themes settled.** TH-28: RWB-P1-E1055-APP#20, RWB-P1-E1068-APP#6, RWB-P1-E2007-APP#2, RWB-P1-E1016-APP#15.

**GAP/ASM rows closed or changed.** None registered for this theme; the applying agent records the closure against the four findings.

**Status.** Proposed – Claude Opus 5.5 (applied).

**Reuse note.** Every service uses the owner's uuid as the path key of a cross-service resource; display numbers (case, lot, notice numbers) never key an API; a non-uuid key answers 400 MSG-GEN-001.

#### Register amendments

- Amended by register note X-25 (clarification, no change): The ledger business key of RD-P1-007 rule 4 may contain the case number as text; it is an opaque producer key, never a P1 lookup key.

**Final ruling (register).** As ruled; the ledger business key may carry the case number as opaque text.

**Values chosen without a source.** None beyond the cited sources.

---

## RD-P1-024 · Case list: P3 rwb-case holds the list, P1 drops `case_list_row`

_Original text of batch B kept for audit. Amendments and the final ruling follow it._

**Question.** Does P1 keep the daily projection `case_list_row` and serve the case list (GAP-0485, GAP-0486, ASM-0677, ASM-0678, Ownership Map v2 Rulings R2), or does rwb-case serve the list from its own rows plus P1 account reads (GAP-2228, ASM-3680, RWB-P3-E1002-APP)?

**Options considered.** (1) P1 keeps the projection; fix the P3 story. (2) P3 holds the list; P1 E1002 is re-scoped to the account read and retires the projection.

**Sources.** Architecture v5 Text Extract v1 slides 10, 14, 15, 41 (P1 DB "ACE view contract, extension tables, freshness, reconciliation"; rwb-case `GET /cases?queue=`; gateway-bff calls rwb-case and rwb-source-data in parallel and merges) and slide 37 / DP-17 (data lake removed); Gap Register v2 GAP-2228 (Status "Resolved (directive)": "drop case_list_row, its key, the extract file, the lake path and the data set under DP-17; and leave REC-01 and REC-05 with RWB-P1-E1011"); Assumptions Register v2 ASM-3676, ASM-3680, ASM-3682 (Confirmed); RWB-P3-E1002-APP v2 sections 1, 3, 4 step 5, 7, 8; Microservice Ownership Map v2 Tables R17 and Rulings R2 (ASM-A6-tables-2, basis TSD P1 v3 only); Data Migration Approach v4 section 7; Gap Register v2 GAP-0485, GAP-0486; ASM-0677, ASM-0678.

**Precedence applied.** Architecture v5 places no case list in P1's schema and gives the list operation to rwb-case; the GAP-2228 directive resolution (D-RCV-60) follows it. The Ownership Map v2 row for `case_list_row` rests only on TSD P1 v3 (an "other document") and is stale; Data Migration Approach v4 section 7, GAP-0485/GAP-0486 and ASM-0677/ASM-0678 are stale.

**Ruling.**
1. `case_list_row`, `uk_case_list_row`, the `DailyCaseList` Schedule at 07:15, `GET /case-list/dates/{businessDate}`, `GET /case-list/rows`, the publish status (PENDING, HELD, RELEASED) and the checks ROWS_BELOW_ENTRY, ALLOCATION_COMPLETE and PUBLISHED are removed from P1. The table is not created by RWB-P1-E1001-APP (its count of P1 tables drops by one; the applying agent restates the count from Physical Schema v9); its DDL stays in Physical Schema v9 as a retirement note, like `lake_copy_watermark`.
2. rwb-case serves the list (`GET /cases`, RWB-P3-E1002-APP), owns the morning Schedule `rwb-case-caselist-daily`, the flag `rwb.p1.case-list` (ASM-3682), MSG-P1-001 raising for the list, and the parameter `caselist.allocation.wait.until`.
3. RWB-P1-E1002-APP, -CON and -OPS are re-scoped (not retired) to the P1 contribution: one account read for a page of account keys of a business date, answering per account the account number, product, total balance, days past due, last contact time, last action code and `dataAsOf`, from `v_ace_account` and `v_ace_efs_action`, one hop with a 2 s budget (DP-05, DP-11). The operation is published in RWB-P1-E1002-CON on `/api/recovery/source-data/v1`; its path and maximum keys per call are Pending (owner solution architect; register a GAP), and Architecture v5's `GET /accounts/{id}` is the single-account form. RWB-P3-E1002-APP repoints its account read from RWB-P1-E1015-CON to RWB-P1-E1002-CON (REQUEST to the P3 owner); the freshness read stays RWB-P1-E1015-CON. RWB-P1-E1002-OPS deploys only that operation (no Schedule, no case-list alerts).
4. REC-01 compares the ACE count of accounts at or above `case.entry.dpd` with the open case accounts that rwb-case returns (RWB-P1-E1011-APP), and REC-05 uses the rwb-case key list (RD-P1-022). The cutover gate of Data Migration Approach v4 section 7 is restated on the same basis (REQUEST to the migration document owner).
5. RWB-P1-E1016-APP step 4 resolves the case's account keys through the rwb-case case contract (one hop), not from `case_list_row`; RWB-P1-E2007-APP and RWB-P1-E1011-APP drop every read or write of `case_list_row` and `publish_status`.
6. The P9 reporting read model is built in rwb-reporting from `rwb.case.events.v1` (ASM-3680); P1 still provides `snapshot(page)` for measures (Architecture v5 slide 15).

**Rationale.** Architecture v5 has no stored case-list projection in P1 and composes the list at read time; keeping a nightly copy is the defect the target removes (RWB-P3-E1002-APP section 2). Re-scoping rather than retiring the P1 E1002 stories keeps a home for the account read rwb-case needs.

**Affected services.** P1, P3, P9, gateway-bff.

**Affected stories.** RWB-P1-E1002-APP, RWB-P1-E1002-CON, RWB-P1-E1002-OPS, RWB-P1-E1001-APP, RWB-P1-E1011-APP, RWB-P1-E1013-APP, RWB-P1-E1016-APP, RWB-P1-E2007-APP, RWB-P3-E1002-APP, RWB-ITG-E1002-ITG (where present).

**Affected documents.** Microservice Ownership Map v2 → v3 (Tables R17 and Rulings R2 retired); Physical Schema v8 → v9 (`case_list_row` retirement note); LDM v10 → v11 (`case_list_row` marked retired; DF-RPT-001 to DF-RPT-019 retired); Data Migration Approach v4 → v5 section 7; Gap Register v2 (GAP-0485, GAP-0486); Assumptions Register v2 (ASM-0677, ASM-0678); Decision Log (record the case-list target); API Specification v6 → v7 (remove the two case-list operations if present; add the account-page read once its path is fixed); Service Contract Catalog v2 → v3.

**Findings and themes settled.** TH-69: RWB-P1-E1002-APP#2, RWB-P1-E1002-CON#1, RWB-P1-E1002-OPS#2.

**GAP/ASM rows closed or changed.** GAP-2228 → Confirmed for P1 (resolution applied to the P1 stories). GAP-0485, GAP-0486 → Closed, superseded by RD-P1-024. ASM-0677, ASM-0678 → Superseded by RD-P1-024. ASM-3676, ASM-3680, ASM-3682 → Confirmed. ASM-A6-tables-2 (Ownership Map basis) → withdrawn.

**Status.** Proposed – Claude Opus 5.5 (applied).

**Reuse note.** No service stores a copy of another owner's data for a list screen; lists are composed at read time from the owner's rows plus P1 account reads by key, one hop each, merged by gateway-bff or the list owner. Where a legacy story's artefact was a lake or file output, the target has no table for it.

#### Register amendments

- Amended by RD-P1-025 (X-21): Item 1: the dictionary rows of `case_list_row` (one `sys_objects` row, DF-RPT-001 to DF-RPT-019) stay in the RWB-P1-E1001-APP baseline marked retired, as `lake_copy_watermark` already is (Physical Schema v8 lines 823, 825); the counts 123 / 1,379 of RD-P1-025 are unchanged; only the table is not created.
- Amended by GAP-2228 directive (X-27): Item 3: the account-page read is published in RWB-P1-E1015-CON (not RWB-P1-E1002-CON) and built by RWB-P1-E1002-APP; RWB-P3-E1002-APP keeps its pointer to RWB-P1-E1015-CON (no repoint REQUEST). RWB-P1-E1002-CON publishes nothing and is retired with a pointer to RWB-P1-E1015-CON and RWB-P1-AD018-CON; RWB-P1-E1002-OPS deploys only the account-page read as a delta on RWB-P1-E1015-OPS.

**Final ruling (register).** Items 2, 4, 5, 6 apply. Item 1: no `case_list_row` table, Schedule, case-list operations, publish status or case-list checks in P1; dictionary rows stay in the baseline marked retired. Item 3: RWB-P1-E1002-APP builds the account-page read; RWB-P1-E1015-CON publishes it (path and keys per call pending, NEW-GAP-B3); RWB-P1-E1002-CON is retired with a pointer; RWB-P1-E1002-OPS is a delta. Reconciliation: child of AceIngestCheck after the ALS stamp, REC-01 waits for rwb-case allocation until `caselist.allocation.wait.until`.

**Values chosen without a source.** Account-page read built by RWB-P1-E1002-APP; RWB-P1-E1002-CON retired (X-27)

---

## RD-P1-025 · Data dictionary baseline: counts, data product seed text and release checks

_Original text of batch B kept for audit. Amendments and the final ruling follow it._

**Question.** Which counts does the dictionary baseline of RWB-P1-E1001-APP deliver (122 / 1,366 in the stories versus 123 / 1,379 in Physical Schema v7/v8), which `data_product.system_of_record` text is seeded, how is the DP07 value that exceeds varchar(120) handled, and what do the release checks of RWB-P1-E1064-OPS and RWB-P1-E1016-DB assert?

**Options considered.** (1) 122 / 1,366 (stories; ACE Field Gap List v1 Counts R4, R5). (2) 123 / 1,379 (Physical Schema v6, v7, v8 seed). For the text: (a) Physical Schema seed text; (b) RWB-P1-E1001-APP section 13 text under BR3. For DP07: shorten the text, or widen the column.

**Sources.** Physical Schema v5.sql (122 `sys_objects`, 1,366 `sys_fields` INSERT lines); Physical Schema v6.sql, v7 and v8 `rwb_source_data.sql` (123 and 1,379; 304 DF-ACE fields; v7 and v8 files identical); comparison v5 → v6: `payment_match_rule` removed (13 fields), `rule_package` (5) and `rule_package_version` (17) added, `rule_row` 18 → 21, `rule_test_case` 13 → 14, net +1 object and +13 fields, the D-RCV-36 changes; LDM v10 Read me R14 (123 entities: 89 Workbench tables, 4 extension tables, 30 views; 1,392 fields) and Fields DF-REF-261 to DF-REF-273 ("Retired by D-RCV-36", `payment_match_rule`, not seeded); ACE Field Gap List v1 sheet Counts R4 (122), R5 (1,366), R6, R12 (81 ACE-new fields over 79 distinct columns); Physical Schema v8 README (93 distinct tables); RWB-P1-E1001-APP sections 1, 8 BR3, 11 ("Target count: 93 tables" beside 92), 13 (14-row data product table); Physical Schema v8 `rwb_source_data.sql` lines 767 to 781 (seed text, e.g. DP01 'ACE (from ALS via COLLINS)'); LDM v10 DF-REF-074 `data_product.system_of_record` varchar(120); RWB-P1-E1064-APP AC4, BR9 (governed load adds DF-ACE-204); Test Cases v8 R1038 (TC-E1-064-04).

**Precedence applied.** D-RCV-36 (16 Temporal and Drools Adoption) ranks above D-RCV-35 (15 ACE DB Alignment): the ACE Field Gap List v1 counts 122 / 1,366 and Physical Schema v5 predate the D-RCV-36 rule-table change, so 123 / 1,379 is authoritative. For the seed text, BR3 of RWB-P1-E1001-APP implements D-RCV-35 U1 and REQ-RDF-001, which rank above the Physical Schema seed (an other document); the Physical Schema text is stale.

**Ruling.**
1. Baseline of RWB-P1-E1001-APP (its Flyway step `V<seq>__rwb_p1_e1001_data_products.sql`): `data_product` 14 rows, `sys_objects` **123** rows, `sys_fields` **1,379** rows of which **304** are DF-ACE view fields, copied from Physical Schema v8 `rwb_source_data.sql`. The dictionary describes **93** tables (89 Workbench + 4 extension) and **30** views. The 13 fields DF-REF-261 to DF-REF-273 of LDM v10 are retired by D-RCV-36 and are not seeded (LDM 1,392 − 13 = 1,379). Stale and to be corrected: RWB-P1-E1001-APP (122, 1,366, "92 tables"), RWB-P1-E1016-DB (122/1,366 check and AC4), RWB-P1-E1064-APP AC10, RWB-P1-E1064-OPS, Test Cases v8 rows asserting 122/1,366, ACE Field Gap List v1 sheet Counts R4 and R5 (pre-D-RCV-36).
2. Release and conformance checks never assert an exact count. RWB-P1-E1064-OPS and RWB-P1-E1016-DB assert: the E1001 baseline migration is applied (Flyway history row present); every baseline object name and every baseline field ID is present; counts are **at least** 123 and 1,379; and every field added after the baseline has a `sys_field_version` row from an approved governed load. A governed load (for example DF-ACE-204 in RWB-P1-E1064-APP AC4) therefore never blocks a later release. Tables added by later stories (RD-P1-020, RD-P1-021) enter the dictionary the same way.
3. RWB-P1-E1064-OPS applies no dictionary migration: RWB-P1-E1064-APP writes none (its sections 13 and 17); the OPS story verifies the E1001 baseline and lists RWB-P1-E1001-APP as a build dependency.
4. Seed text of `data_product.system_of_record`: the 14 values of RWB-P1-E1001-APP section 13 are the seed, with one correction: DP10 becomes `Recovery Workbench` (the story's "Recovery Workbench document hub" fits none of the BR3 forms). The Physical Schema v8 seed lines 767 to 781 are replaced by these values in Physical Schema v9.
5. DP07 length: the DP07 value (139 characters) is kept word for word and DF-REF-074 `data_product.system_of_record` is widened from varchar(120) to **varchar(200)** in LDM v11 and Physical Schema v9 (P1-owned column, no consumer impact). `sys_objects.system_of_record` (DF-REF-092) stays varchar(120).
6. Accepted grammar for BR3 and MSG-P1-003 (validator, case sensitive): a value is valid when it matches `^ACE \(ingested from [^)]+\)$`, or equals `Recovery Workbench`, or is one sentence of at most 200 characters that contains both `ACE (ingested from ` and `Recovery Workbench`, or starts with `Recovery Workbench, with ` and contains `ACE`. With the DP10 correction all 14 seed values pass (DP04, DP07 by form 3; DP14 by form 4).
7. ACE conformance contract of RWB-P1-ACE001-DB AC8: ACE Field Gap List v1 sheet Fields is the contract (81 ACE-new field rows over 79 distinct ACE columns, Counts R12; DF-DEC-006 and DF-DEC-023 both served by `collins_score.model_version`, DF-INT-008 and DF-INT-036 both by `efs_action.contact_result`); the legacy appendix A (80 rows, 79 distinct columns) is stale. See RD-P1-027 for how the story names the file.

**Rationale.** The 13-field and one-object difference is exactly the D-RCV-36 rule-table change; the higher-ranked decision wins. "At least" checks keep governed loads from breaking releases while still catching a missing baseline row.

**Affected services.** P1.

**Affected stories.** RWB-P1-E1001-APP, RWB-P1-E1016-DB, RWB-P1-E1016-APP, RWB-P1-E1064-APP, RWB-P1-E1064-OPS, RWB-P1-ACE001-DB.

**Affected documents.** Physical Schema v8 → v9 (`rwb_source_data.sql` seed text lines 767 to 781, DF-REF-074 width); LDM v10 → v11 (DF-REF-074 varchar(200)); ACE Field Gap List v1 (Counts R4, R5 stale; note to the ACE DB Alignment owner); Test Cases v8 → v9 (count assertions).

**Findings and themes settled.** TH-55: RWB-P1-E1001-APP#G2, RWB-P1-E1001-APP#G21, RWB-P1-ACE001-DB#6, RWB-P1-E1016-DB#2, RWB-P1-E1016-DB#3, RWB-P1-E1064-OPS#1, RWB-P1-E1064-OPS#2.

**GAP/ASM rows closed or changed.** None registered for this theme; the applying agent records the closure against the seven findings.

**Status.** Proposed – Claude Opus 5.5 (applied).

**Reuse note.** Every dictionary or seed count is taken from the highest Physical Schema seed after the D-RCV-36 changes (123 / 1,379 / 304) and asserted as "at least, plus every baseline ID present"; a text that a business rule validates is fixed once in the owning story and the schema copies it, never the reverse.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

**Values chosen without a source.** DF-REF-074 widened to varchar(200); DP10 text Recovery Workbench; BR3 / MSG-P1-003 grammar; at-least release checks

---

## RD-P1-026 · RW-COMPLY read of DP02 in access version DPA-2026.11

_Original text of batch B kept for audit. Amendments and the final ruling follow it._

**Question.** RWB-P1-E1016-APP AC6 (a legacy criterion kept word for word) has user `u-comply-01` holding RW-COMPLY read DP02, but the DPA-2026.11 seed of RWB-P1-E1016-DB holds six rows and none for RW-COMPLY, so BR1 answers 403. Seed a row, or change the criterion?

**Options considered.** (1) Change AC6 to a seeded role (RW-AUDIT or RW-CASEOWN). (2) Add a sourced RW-COMPLY / DP02 row to the seed.

**Sources.** RWB-P1-E1016-APP section 1 ("Kept word for word: the ten acceptance criteria … AC6"), section 7 AC6 ("Given user "u-comply-01" holds RW-COMPLY, which reads DP02", legacy RWB-E1-016 AC6), section 10 (RW-COMPLY "Owns the masking rules in rwb-access (DL26); reads the catalog"), section 16 TC-E1-016-06; RWB-P1-E1016-CON sections 12.8 and 16; RWB-P1-E1016-DB seed (six rows); Assumptions Register v2 ASM-0674 (six rows "the sources give"; sources listed: legacy RWB-E1-016 section 3 and AC3 and AC5, FSD P1 v3 A2.15); Gap Register v2 GAP-0482.

**Precedence applied.** The legacy criterion RWB-E1-016 AC6 is itself a source statement that RW-COMPLY reads DP02; ASM-0674 enumerated only section 3, AC3 and AC5 and missed it. Changing a criterion that the story keeps word for word would drop a legacy test; adding the row the legacy text states does not invent access.

**Ruling.** Version DPA-2026.11 of `data_product_access` is seeded with **seven** rows: the six of ASM-0674 plus `('DP02', 'RW-COMPLY', can_read true, access_version 'DPA-2026.11', valid_from DATE '2026-11-20', valid_to NULL)`, source legacy RWB-E1-016 AC6. AC6 of RWB-P1-E1016-APP stays word for word; the rwb-access fake of RWB-P1-E1016-CON keeps its granted answer for RW-COMPLY; RWB-P1-E1016-DB AC3 and its seed list change from six to seven rows; the masking answer for RW-COMPLY on DP02 still comes from rwb-access (DL26, all personal fields masked while no rule is loaded). No DP06 row is added for RW-PHONECOL (ASM-0674 unchanged on that point).

**Rationale.** The row is stated by a legacy acceptance criterion, so it is sourced; the safe-direction argument of ASM-0674 applies only to rows no source states.

**Affected services.** P1; P4 (masking answer unchanged).

**Affected stories.** RWB-P1-E1016-APP, RWB-P1-E1016-CON, RWB-P1-E1016-DB.

**Affected documents.** Assumptions Register v2 (ASM-0674 text: seven rows, source list adds legacy RWB-E1-016 AC6); Physical Schema v9 only if the access seed is held there (it is not in v8; the seed is RWB-P1-E1016-DB's).

**Findings and themes settled.** TH-70: RWB-P1-E1016-APP#1, RWB-P1-E1016-CON#18, RWB-P1-E1016-DB#11.

**GAP/ASM rows closed or changed.** ASM-0674 → Changed (seven rows) by RD-P1-026. GAP-0482 → stays open for the rest of the access matrix.

**Status.** Proposed – Claude Opus 5.5 (applied).

**Reuse note.** Before calling a seed row "not sourced", read every legacy acceptance criterion of the story: a Given that states a role reads a product is a source for that row.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

**Values chosen without a source.** None beyond the cited sources.

---

## RD-P1-027 · Migration package field mapping, allow-list and provenance columns

_Original text of batch B kept for audit. Amendments and the final ruling follow it._

**Question.** How does each DM package (RWB-P1-DM002-APP to RWB-P1-DM010-APP) and RWB-P1-ACE001-DB name the fields it carries, which fields are allowed or excluded, and where are the migration source and migration date held?

**Options considered.** (1) Leave each DM story to list fields. (2) One field-by-field mapping keyed by LDM field IDs, one allow-list rule, one provenance column pair for every migrated table.

**Sources.** Data Migration Approach v4 sections 7, 9.1 ("Every migrated row keeps its source and migration date columns in the owner's schema"), 9.2 (50 tables across 15 schemas receive migrated rows), 9.3, 9.4, 10.1; Source to Target Mapping v6 sheets Mapping and Mapping rules R18 (no load-time transform; no row migrated by another service); LDM v10 sheet Fields (system of record per field; DF-LEG-001 to DF-LEG-014; DF-PRT-015 `result_code`, DF-PRT-016 `fee_amount`; DF-INT-003 `person_key`, DF-INT-022 `contact_key`) and sheet Standard columns; Data Classification and Personal Data Inventory v5; Cross-document Change Register v1 CDC-02512, CDC-02520, CDC-02521, CDC-02527, CDC-02532, CDC-02533, CDC-02538 (migrated_at not in the dictionary; Pending); Gap Register v2 GAP-0529, GAP-0553, GAP-2166, GAP-2172, GAP-2174; TSD P1 v3 T3.3 view 16 (key `plan_ref`, `account_key`); Physical Schema v8 `contact_point_ext` (PK `contact_key`, `contact_type` PHONE/EMAIL/ADDRESS); ACE Field Gap List v1; Recovery Workbench ACE Team Stories v1.md section 13 (legacy appendix A).

**Precedence applied.** Data Migration Approach v4 (provenance rule) and LDM v10 (field IDs and systems of record) over the legacy Data Migration Stories v3 ranges; D-RCV-35 (ACE read path) over any package that would copy ACE facts.

**Ruling.**
1. **One mapping.** Source to Target Mapping v7 adds sheet `Migration packages`, owner data architect, one row per package and target field: `package_story` (RWB-P1-DMnnn-APP), `legacy_source` (legacy table.column), `target_service`, `target_schema`, `target_table`, `field_id` (LDM v11 ID), `field_name`, `physical_type`, `mandatory`, `disposition` (CARRY, EXCLUDE, ACE_READ, KEY), `reason`, `approved_by_role`, `classification_row` (Data Classification v5 row). Each DM story's section 11 is replaced by its rows of that sheet (copied, not re-derived), and AC1 of each DM story asserts every CARRY field of its rows.
2. **Allow-list rule.** A package carries only (a) fields of the target owner's tables whose LDM system of record is `Workbench` (disposition CARRY), and (b) the ACE business keys that link a row (`account_key`, `person_key`, `contact_key`, `valuation_key`, `asset_key`, `plan_ref`; disposition KEY). A field whose LDM system of record is an ACE source system (ALS, LIT, WIN, EFS, COLLINS, GL, SCBPDM, CCMS, SVAF, AMIS, RPS, or "… via COLLINS") is ACE_READ: never carried, read through the `recovery.v_ace_*` views of P1 (DP-05). Any other exclusion is EXCLUDE with a reason and the approving role.
   - RWB-P1-DM007-APP: CARRY DF-LEG-001 to DF-LEG-004 and DF-LEG-014 (and the Workbench `notice` fields); ACE_READ DF-LEG-005 to DF-LEG-013 (LIT), so AC5 (no court facts in the package) holds and sections 4 and 11 are aligned to it; the DP07 response is the view-backed read of RWB-P1-E1016-APP, separate from the package.
   - RWB-P1-DM008-APP: target owner S9 (RD-P1-021); `result_code` DF-PRT-015 (not "result") and `fee_amount` DF-PRT-016 are CARRY (system of record Workbench).
   - RWB-P1-DM004-APP: the plan lookup key is (`plan_ref`, `account_key`) exactly as TSD P1 v3 T3.3 view 16; section 11 is corrected and a duplicate `plan_ref` across two accounts is a boundary test.
   - RWB-P1-DM002-APP: `contact_point_ext` holds zero or one row per `contact_key` and any number per `person_key` (one per PHONE, EMAIL or ADDRESS contact point); an absent row means the table defaults (`consent_given` false, `failed_count` 0, `source` 'WORKBENCH'); the answer is a list per person (closes GAP-0553 reading).
   - RWB-P1-DM005-APP: `person_key` and `contact_key` are DF-INT-003 and DF-INT-022 on `interaction` (they exist in Physical Schema v8).
   - RWB-P1-DM006-APP: P1 extracts; S5 writes the asset rows in `rwb_asset`; P1 writes only `valuation_ext`; AC1 asserts the S5 package fields and the `valuation_ext` insert, and no cross-schema write.
   - RWB-P1-DM009-APP: target owner S6; include the case key only where it is enough (data minimisation), per the mapping sheet.
   - RWB-P1-DM010-APP: target owner P5; field IDs are the current DF-DOC IDs of LDM v10 for `document` and `document_field`; the legacy overlapping ranges (GAP-2174) are replaced by a legacy-to-current crosswalk column in the mapping sheet; pass-through extracted fields follow the P5 contract's field set and Data Classification v5 rows R268 to R275.
3. **Provenance columns.** LDM v11 sheet Standard columns adds two conditional standard columns, carried by every table that receives migrated rows (Data Migration Approach v4 section 9.2 list) and by no other table: `migration_source varchar(20)` (null for rows created live; the legacy source of the row, from list LOV-MIGRATION-SOURCE whose values are Pending, owner data owner) and `migrated_at timestamptz` (UTC instant the owner's load step wrote the row; null for live rows). Each owner adds them in its own Flyway step (DP-15); classification "Internal, not personal". Where a table already has a source column (`interaction.source_system`, `contact_point_ext.source`) it keeps it for the business source and still gains `migrated_at`. This resolves CDC-02512, CDC-02520, CDC-02521, CDC-02527, CDC-02532, CDC-02533 and CDC-02538 with one dictionary change.
4. **RWB-P1-ACE001-DB AC8.** The conformance contract is ACE Field Gap List v1 sheet Fields, held in the repository as a fixture copied from that sheet; the story names the file and version instead of "legacy RWB-ACE-001 appendix A". A "mapped column" is an ACE column named in that sheet; an extra mapped column is one present in a new ACE table of RWB-ACE-001 and absent from the sheet (see RD-P1-025 item 7 for the counts).

**Rationale.** A single mapping keyed by dictionary IDs removes ten divergent field lists; the system-of-record test is mechanical and already in the dictionary; one standard column pair satisfies the Migration Approach rule without a per-table field-ID hunt.

**Affected services.** P1 (extract, mapping, reconciliation rows) and every owner of a migrated table: P3, P5, P7, S2, S4, S5, S6, S9 and the others of Data Migration Approach v4 section 9.2.

**Affected stories.** RWB-P1-ACE001-DB, RWB-P1-DM002-APP, RWB-P1-DM003-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP, RWB-P1-DM008-APP, RWB-P1-DM009-APP, RWB-P1-DM010-APP.

**Affected documents.** Source to Target Mapping v6 → v7 (sheet Migration packages); LDM v10 → v11 (sheet Standard columns; LOV-MIGRATION-SOURCE); Data Classification v5 → v6 (two standard columns); Physical Schema v8 → v9 (the two columns on the migrated tables); Data Migration Approach v4 → v5 (section 9.1 names the columns); Cross-document Change Register v1 (CDC rows above).

**Findings and themes settled.** TH-11: RWB-P1-DM010-APP#8, RWB-P1-DM003-APP#4, RWB-P1-DM004-APP#5, RWB-P1-DM010-APP#4, RWB-P1-DM007-APP#2, RWB-P1-DM008-APP#2, RWB-P1-DM008-APP#7, RWB-P1-DM009-APP#12, RWB-P1-DM009-APP#2, RWB-P1-DM010-APP#3, RWB-P1-DM002-APP#6, RWB-P1-DM004-APP#2, RWB-P1-DM005-APP#1, RWB-P1-DM006-APP#2, RWB-P1-ACE001-DB#8.

**GAP/ASM rows closed or changed.** CDC-02512, CDC-02520, CDC-02521, CDC-02527, CDC-02532, CDC-02533, CDC-02538 → resolved by RD-P1-027 item 3. GAP-2166 (cutover extract layout) → closed by the mapping sheet. GAP-2174 → owner P5 fixed; crosswalk column holds the legacy IDs. GAP-0553 → closed (cardinality item 2). GAP-0529 → closed (DM006 item 2). New GAP needed: values of LOV-MIGRATION-SOURCE, owner data owner.

**Status.** Proposed – Claude Opus 5.5 (applied).

**Reuse note.** Every migration story of any service takes its fields from the Migration packages sheet; ACE-sourced fields are never carried; every migrated table carries `migration_source` and `migrated_at`.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

**Values chosen without a source.** Migration packages sheet layout and disposition codes; migration_source varchar(20); migrated_at

---

## RD-P1-028 · Parameter catalog for P1: where parameters live, their owner route, and what replaces the empty file

_Original text of batch B kept for audit. Amendments and the final ruling follow it._

**Question.** `SET\parameter-catalog.csv` is empty (0 bytes). Where do the parameters P1 reads live, who owns them, how does P1 read them, how are parameters told apart from reference data, and what replaces the empty file?

**Options considered.** (1) Fill the root file. (2) Treat the root file as void and use the rwb-case catalog source of RWB-P3-E1042 as the one catalog, with a document-set copy.

**Sources.** `SET\parameter-catalog.csv` (0 bytes, 18 November 2026, no version, no owner); `E1-042 Migration and Clarifications/README.md` and `RWB-E1-042 Clarification Pack.md` (build-time catalog `config/parameter-catalog.csv`, 13 bootstrap rows, header `key,kind,value_type,unit,min_value,max_value,default_value,scope,required,owner_role,environments,used_by,secret,description`; "When the full Epic 1 catalog arrives, replace this bootstrap CSV"); `sql/V042_1__parameter_catalog.sql` (`parameter_catalog`, `parameter_value`); RWB-P3-E1042-APP v2 (the catalog seed file `config/parameter-catalog.csv` is in the repository, owned by RW-COE; a new key is added by pull request reviewed by the owner); Microservice Ownership Map v2 sheet Tables R61, R62 (`parameter_catalog`, `parameter_value` P3 rwb_case) and sheet Parameters (parameters P3 via RWB-P3-E1042-CON; reference data P3 via RWB-P3-E1043-CON); Service Contract Catalog v2 (`GET /admin/parameters` P3); Definition of Ready and Done v4 item 20; Reference Data and Lists of Values v5 sheets Reference tables and Reference data starter; RWB-P1-E1011-APP sections 3, 12.2, 12.8, 13 (`recon.tolerance.pct` 0.00 assumed DL25, `recon.treatment.days` 2, `recon.payment.days` 1, `case.entry.dpd` 90); RWB-P1-AD019-APP sections 3, 17; RWB-P1-E1002-APP section 3 (`recon.caselist.tolerance.pct`, `caselist.allocation.wait.until`); Gap Register v2 GAP-2164 and ASM-3468 (deployment values in the per-environment values file).

**Precedence applied.** Ownership Map v2 and DoR item 20 (D-RCV-60) fix the owner and route; the E1-042 pack is the only source that defines catalog columns and keys; the root file has no content and no standing.

**Ruling.**
1. **Owner and route.** Business parameters live in `rwb_case.parameter_catalog` and `rwb_case.parameter_value` (owner P3 rwb-case, owner role of each key as in the catalog). P1 reads them only through RWB-P3-E1042-CON with its client library (`GET /api/recovery/case/v1/parameters/{key}`, version in force on the business date), faked in P1 tests; P1 holds no parameter table and no parameter in its values file.
2. **What is a parameter, a list, a P1 catalog row, a deployment value, a flag.** A scalar business setting (threshold, tolerance, wait time, days) is a parameter (RWB-P3-E1042-CON, DP-06). A closed set of codes is a list of values (RWB-P3-E1043-CON, DP-07; the P1 lists are the 45 starter rows of Reference Data v5). Rows of P1-owned catalog tables (`data_product`, `data_product_source`, `data_product_access`, `efs_ledger_outcome`) stay in `rwb_source_data` and change only through the reference-load apply handler (RD-P1-020 G, RD-P1-021). Thresholds of alerts, channel names, replica counts, batch sizes and archive containers are per-environment values-file entries (GAP-2164, ASM-3468), not parameters. Feature flags are the PLT flag library.
3. **Catalog of record.** The rwb-case repository file `config/parameter-catalog.csv` (RWB-P3-E1042-APP) is the catalog of record; its document-set copy is a new file `06 Data/Recovery Workbench Parameter Catalog v1.csv` with the 14-column header of the E1-042 bootstrap, containing the 13 bootstrap rows and the P1 rows of item 4. `SET\parameter-catalog.csv` is void: it is not cited by any story or document, and its removal is a REQUEST to the developer (this run edits no existing SET file).
4. **P1 rows** (Proposed values where marked; each `owner_role` RW-COE as in the bootstrap; `environments` "DEV,SIT,UAT,PROD"; `secret` false):
   - `case.entry.dpd` – existing bootstrap row, unchanged (default 90, DL16); `used_by` adds `rwb-source-data.reconciliation`.
   - `recon.tolerance.pct` – BUSINESS, DECIMAL, PERCENT, min 0, max 100, default 0.00, GLOBAL, required true, `used_by` `rwb-source-data.reconciliation`, "Tolerance of the count reconciliations REC-01 and REC-02 (DL25, assumed)". It **replaces** the bootstrap key `recon.caselist.tolerance.pct` (same meaning; the case list has left P1, RD-P1-024; RWB-P1-E1011-APP is the owning story of REC-01 and REC-02, RD-P1-022). Proposed.
   - `recon.treatment.days` – BUSINESS, INTEGER, DAYS, default 2, GLOBAL, required true, `used_by` `rwb-source-data.reconciliation`, "Days allowed in the treatment reconciliation (DL25, assumed)". Proposed (value from the RWB-P1-E1011-APP fake).
   - `recon.payment.days` – BUSINESS, INTEGER, DAYS, default 1, GLOBAL, required true, `used_by` `rwb-source-data.reconciliation`, "Days allowed in the payment reconciliation (DL25, assumed)". Proposed (value from the RWB-P1-E1011-APP fake).
   - `caselist.allocation.wait.until` – bootstrap row kept; it is rwb-case's (`used_by` `recovery.casewf.caselist`), not a P1 parameter after RD-P1-024.
   The meaning and unit of `recon.treatment.days` and `recon.payment.days` (calendar or working days) is Pending DL25, owner data steward with the centre of excellence; the applying agent registers it as a GAP.
5. **Story rule.** Every P1 story names its parameters in section 3 with key, default and source decision, lists the RWB-P3-E1042-CON fake in 12.8, and never names `/api/recovery/case/v1/parameters/{key}` without that contract. The keys `recon.caselist.tolerance.pct` in RWB-P1-E1002 stories are removed with the case list.

**Rationale.** The owner and contract are already ruled (Ownership Map v2, DoR item 20); the only build-time catalog with a defined format is the E1-042 bootstrap that RWB-P3-E1042-APP names; an empty, unversioned root file cannot be a source of record. One tolerance key for both reconciliations matches the owning story.

**Affected services.** P1, P3.

**Affected stories.** RWB-P1-E1011-APP, RWB-P1-AD019-APP, RWB-P1-E1002-APP, RWB-P1-E1002-CON, RWB-P1-E1002-OPS, RWB-P3-E1042-APP, RWB-P3-E1042-CON.

**Affected documents.** New `06 Data/Recovery Workbench Parameter Catalog v1.csv`; `E1-042 Migration and Clarifications/config/parameter-catalog.csv` (key rename, as a REQUEST to the P3 owner); `SET\parameter-catalog.csv` (void, removal REQUEST); Reference Data and Lists of Values v5 → v6 (read me: the parameter / list / catalog / values-file split).

**Findings and themes settled.** Parameter-catalog item of this batch; supports TH-20 (RWB-P1-AD018-APP#24) and TH-27 (RWB-P1-E1013-APP#22 DL25 row).

**GAP/ASM rows closed or changed.** New GAP needed: unit and meaning of `recon.treatment.days` and `recon.payment.days` (DL25), owner data steward with the centre of excellence. GAP-2164, ASM-3468 → Confirmed as the home of deployment values.

**Status.** Proposed – Claude Opus 5.5 (applied).

**Reuse note.** Every service registers its business parameters as rows of the rwb-case catalog (`config/parameter-catalog.csv`, mirrored in `06 Data/Recovery Workbench Parameter Catalog v1.csv`), reads them through RWB-P3-E1042-CON, puts closed code sets in lists (RWB-P3-E1043-CON), and keeps operational values in the per-environment values file.

#### Register amendments

- Amended by RD-P1-024 chain (X-22): Item 4 last bullet: `caselist.allocation.wait.until` stays rwb-case's row; its `used_by` adds `rwb-source-data.reconciliation`, because REC-01 waits for allocation until that time (RD-P1-040 item 5 as amended).

**Final ruling (register).** Items 1-5 apply; `caselist.allocation.wait.until` stays rwb-case's and is also read by P1 reconciliation (`used_by` adds `rwb-source-data.reconciliation`).

**Values chosen without a source.** recon.tolerance.pct row values; recon.treatment.days 2 and recon.payment.days 1 (from the E1011 fake); file name Recovery Workbench Parameter Catalog v1.csv

---

## RD-P1-040 · Daily ingest, case list and reconciliation triggers, hand-offs and workflow IDs

_Original text of batch C kept for audit. Amendments and the final ruling follow it._

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

#### Register amendments

- Amended by RD-P1-024 (X-01): Item 4 is withdrawn (no `CaseListBuildWorkflow`, no `DailyCaseList`). Item 5: `ReconciliationWorkflow` is started by `AceIngestCheck` as a child (ABANDON) in the workflow task that commits the ALS stamp; input `{businessDate, startedBy}`; before REC-01 it polls the rwb-case allocation contract every `recon.allocation.poll.minutes` (values file, 5, Proposed) with durable timers and runs at ALLOCATION_COMPLETE YES or at `caselist.allocation.wait.until` (07:15, rwb-case parameter); no ALLOCATION_COMPLETE check is recorded in P1; the case-list gate and `caseListRunId` lapse. Item 6 is withdrawn (the list deadline is rwb-case's). Item 7: no `CaseListBuildWorkflow` row and no `DailyCaseList` Schedule; R19 reads "child of AceIngestCheck"; a row is added for `Stage2ProductWorkflow` as a child of AceIngestCheck.
- Amended by RD-P1-012 (X-18): Item 1 Closing: an ADMIN rerun applies only to a FAILED run (conflict policy FAIL, reuse ALLOW_DUPLICATE_FAILED_ONLY); a late batch after a COMPLETED run is picked up by a repeated ready call or the poll.
- Amended by RD-P1-003 and RD-P1-009 (X-03): Precedence sentence: "KTEC v2 ACL R4 (rwb-source-data consumes nothing) is kept" is limited to `rwb.source-data.events.v1`; rwb-source-data reads the three ledger-intake topics.
- Amended by RD-P1-028 (X-22): `ingest.poll.interval.minutes` (5) and the allocation poll are per-environment values-file entries of rwb-source-data, not rwb-case parameters.

**Final ruling (register).** Items 1-3 apply with: admin rerun only of FAILED runs; poll intervals in the values file. Item 5: ReconciliationWorkflow is a child of AceIngestCheck after the ALS stamp, waits for rwb-case allocation (poll `recon.allocation.poll.minutes` 5, limit `caselist.allocation.wait.until` 07:15), input `{businessDate, startedBy}`, USE_EXISTING + ALLOW_DUPLICATE. Items 4 and 6 withdrawn; item 7 without the case-list rows. rwb-source-data does not consume its own topic.

**Values chosen without a source.** ingest.poll.interval.minutes 5; recon.allocation.poll.minutes 5 (was caselist.allocation.poll.minutes); 24 h run close; catch-up window 1 h; metric rwb_source_data_duplicate_start_total; conflict and reuse policies

---

## RD-P1-041 · Freshness stamp state model: expected date, multiple sources, repeats, late batches, STALE and the single writer

_Original text of batch C kept for audit. Amendments and the final ruling follow it._

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

#### Register amendments

- Amended by RD-P1-005 (X-12): Item 3 column values: `source_extracted_at` = the latest `completed_at` among P's sources for D (ace_batch_run.completed_at, as published in rwb-source-data.yaml); `loaded_at` = the instant AceIngestCheck writes the row. ASM-0684 is changed (mapping superseded), not confirmed.

**Final ruling (register).** Items 1, 2, 4-8 apply; item 3 times: `source_extracted_at` = latest source `completed_at`, `loaded_at` = write instant. ASM-0684 changed.

**Values chosen without a source.** Rollup option B; missing-calendar fallback; metric rwb_source_data_win_delivery_repeat_total

---

## RD-P1-042 · Reconciliation tolerance (DL25)

_Original text of batch C kept for audit. Amendments and the final ruling follow it._

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

#### Register amendments

- Amended by RD-P1-024 (X-24): Item 2: a BREAK raises MSG-P1-012 and the Reconciliation break alert and is shown in the run record; there is no `publish_status` in P1. Item 3: "no case list" is replaced by "allocation contract unreadable" among the cannot-proceed causes. The effect on the rwb-case list is NEW-GAP-X3.

**Final ruling (register).** Items 1, 4, 5 apply; a BREAK raises MSG-P1-012 and the alert, no publish status; NOT_RUN does not exist; a run that cannot proceed (gate HOLD, allocation contract unreadable, parameter unreadable) writes no row.

**Values chosen without a source.** DL25 option A applied ahead of Data lead confirmation

---

## RD-P1-043 · Section B views dependency (DL43): what builds, deploys and alerts while Section B is absent

_Original text of batch C kept for audit. Amendments and the final ruling follow it._

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

#### Register amendments

- Amended by RD-P1-024 (X-01): Item 2: "the case list freshness line" is removed. Item 3(b): `ReconciliationWorkflow` and `Stage2ProductWorkflow` are registered but not started (AceIngestCheck writes no stamp, so starts no child); there is no 07:15 Schedule.

**Final ruling (register).** Items 1, 4, 5 apply; with the Section B flag off AceIngestCheck writes no stamp, publishes nothing, starts no child, status LATE, freshness STALE with null date.

**Values chosen without a source.** DL43 answer A as the planning basis ahead of ACE team lead decision

---

## RD-P1-044 · One owner per shared rwb-source-data deployment object; no consumer of the service's own AceDataReady

_Original text of batch C kept for audit. Amendments and the final ruling follow it._

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

#### Register amendments

- Amended by RD-P1-024 (X-01, X-27): Row "CaseListBuildWorkflow registration; Schedule DailyCaseList; case-list alerts" is withdrawn; RWB-P1-E1002-OPS is a delta deploying only the account-page read.
- Amended by RD-P1-003 and RD-P1-009 (X-03): First row: "no consumer-lag trigger, because the service consumes no topic" reads "no lag trigger for rwb.source-data.events.v1, which P1 does not consume". The ledger-intake consumer groups on `rwb.case.events.v1`, `rwb.document.events.v1` and `rwb.decision-record.v1` are declared by RWB-P1-E1066-OPS (ledger writer row).
- Amended by RD-P1-040 (X-08): AD019-OPS adds no reconciliation activity ("any added activities" lapses).

**Final ruling (register).** Ownership table applies without the case-list row; RWB-P1-E1066-OPS declares the ledger-intake consumer groups; no P1 consumer group on `rwb.source-data.events.v1`; RWB-P1-E1002-OPS deploys only the account-page read; AD019-OPS adds no reconciliation activity.

**Values chosen without a source.** None beyond the cited sources.

---

## RD-P1-045 · Rollback standard with forward-only migrations

_Original text of batch C kept for audit. Amendments and the final ruling follow it._

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

#### Register amendments

- Amended by RD-P1-024 (X-01): Item 6 last sentence reads: "A FAILED P1 run is re-run after the fix through POST /admin/jobs/{jobId}/rerun (RD-P1-012 rule 5)."

**Final ruling (register).** Items 1-5 apply; item 6 ends: a FAILED P1 run is re-run after the fix through `POST /admin/jobs/{jobId}/rerun`.

**Values chosen without a source.** None beyond the cited sources.

---

## RD-P1-046 · Sandbox scope (shared) and the published seed fixtures

_Original text of batch C kept for audit. Amendments and the final ruling follow it._

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

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

**Values chosen without a source.** Interim shape counts (remainder to the plain 90-days-past-due shape)

---

## RD-P1-047 · Retention run interface between P5 JOB-17 and P1, and the held-cases read from P3

_Original text of batch C kept for audit. Amendments and the final ruling follow it._

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

#### Register amendments

- Amended by RD-P1-001 (X-04): Item 1: Idempotency-Key is a UUID (not `{runDate}:{ruleVersion}`); a key reused with another body answers 409 MSG-PLT-N009-05 (not 422 MSG-GEN-001); the 409 MSG-P2-006 for a run of the date running or complete stays; reuse policy ALLOW_DUPLICATE_FAILED_ONLY is added to conflict policy FAIL.

**Final ruling (register).** Items 2-4 apply. Item 1: `POST /retention-runs`, UUID Idempotency-Key, body `{ruleVersion, runDate, rules[]}`, 202 `{runId, status: ACCEPTED}`, 409 MSG-P2-006 (run of the date running or complete), 409 MSG-PLT-N009-05 (key reuse), 422 MSG-GEN-002 / MSG-P1-002 (rules refused); workflow `RetentionRunWorkflow`, ID `retention-run-{runDate}`, FAIL + ALLOW_DUPLICATE_FAILED_ONLY.

**Values chosen without a source.** P5 poll every 5 minutes; P3 paths retention-exclusions and closure-dates; page size 1,000; workflow ID retention-run-{runDate}

---

## RD-P1-048 · Retention scope, age basis, hold join, REVIEW and delete rules for rwb_source_data

_Original text of batch C kept for audit. Amendments and the final ruling follow it._

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

#### Register amendments

- Amended by RD-P1-024 (X-01): `case_list_row` is not created: the DP01 interim row (item 1) and its ARCHIVE entry (item 3) are withdrawn and it joins the excluded list ("not created, RD-P1-024"). The validated table list is seven tables: interaction, party_ext, account_ext, contact_point_ext, valuation_ext, dp_treatment, dp_guarantee_claim. Item 2 case-bound tables = `interaction`.

**Final ruling (register).** Items 2, 4-6 apply with seven tables in scope (ARCHIVE: interaction; REVIEW: party_ext, account_ext, contact_point_ext, valuation_ext, dp_treatment, dp_guarantee_claim); `case_list_row` excluded as not created; periods pending GAP-1029.

**Values chosen without a source.** Interim periods as data from RRA v4 proposals (pending DL26)

---

## Companion files

- `Recovery Workbench P1 Decision Register v1.csv`: one row per decision (30 rows) with the final ruling, amended_by and the values chosen without a source.
- `Affected stories outside P1 v1.csv`: 289 story keys outside RWB-SVC-P1, each verified as a file in Service Story Files v2. By service: rwb-case 34, RWB-ITG-W1 Wave 1 integration 33, rwb-writeoff 27, RWB-ITG-W4 Wave 4 integration 24, rwb-comms 24, rwb-integration 21, rwb-access 20, rwb-decision 20, rwb-payment 20, RWB-ITG-W2 Wave 2 integration 13, rwb-agent 9, rwb-document 9, RWB-ITG-W3 Wave 3 integration 4, RWB-PLT-TPL Service template and repositories 4, RWB-PLT-LIB Shared libraries 3, rwb-asset 3, rwb-litigation 3, rwb-partner 3, rwb-reporting 3, RWB-PLT-EDGE Edge and gateway 2, RWB-PLT-EVT Kafka event platform 2, rwb-deviation 2, rwb-guarantee 2, rwb-treatment 2, RWB-ITG-NFR Non-functional integration 1, RWB-PLT-OBS Observability 1.
- Keys checked that have no story file and were dropped from that list (a guessed contract twin of the DocumentStored producer RWB-P5-E1024-APP): `RWB-P5-E1024-CON`.
- `New gaps and assumptions from decisions v1.csv`: 34 rows (12 GAP, 22 ASM) with temporary IDs; the orchestrator assigns GAP numbers after GAP-3270 and ASM numbers after the last ASM of Assumptions Register v2, and replaces the labels in the register.

## Change log

| Version | Date | Change | By |
|---|---|---|---|
| v1 | 27 November 2026 | Register created from batches A, B and C; 27 cross-batch resolutions (X-01 to X-28; X-05 merged into X-04) applied as amendments; D-RCV-60 P1 developer readiness (RD-P1 register) | Chief architect (design sub-agent), Claude Opus 5.5 |
