# Recovery Workbench P1 Decision Register v3

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Run | D-RCV-60 P1 developer readiness (RD-P1 register) |
| Service epic | RWB-SVC-P1 rwb-source-data (Source data) |
| Version | v3, 27 November 2026 (v1 and v2 stay unchanged beside it) |
| Status | Proposed – Claude Opus 5.5 (applied) |
| Prepared by | Chief architect (design sub-agent), Claude Opus 5.5 (claude-opus-5-5) |
| Inputs | Recovery Workbench P1 Decision Register v2 (.md, .csv: RD-P1-001 to RD-P1-074, 45 decisions with amendments and final rulings); `decisions\batch-E.md` and `.csv` (RD-P1-060 to RD-P1-074 were batch D; batch E is RD-P1-075 to RD-P1-100) from the re-review packets (`SET\_work\p1-ready\packets\rereview ruling items.csv`, Blocker rows of `rereview story items.csv` and `rereview document items.csv`) and the blocking gaps of staged Gap Register v3. Earlier inputs as in v2: Recovery Workbench P1 Decision Register v1 (.md, .csv: RD-P1-001 to RD-P1-048, 30 decisions with amendments and final rulings); `decisions\batch-D.md` and `.csv` (RD-P1-060 to RD-P1-074); orchestrator amendments from the edit logs in `SET\_work\p1-ready\editlog\` (W3-messages-0078; S12-stories-0340; W5-runtime-0359, -0362, -0365, -0368 and FD3-runtime-0143); story keys found in Service Story Files v2 and the staged Service Story Files v3 |
| Precedence | D-RCV-60 and Architecture v5 (SET\22 Microservice Realignment) > RD-P1 decisions > 16 Temporal and Drools Adoption (D-RCV-36) > 15 ACE DB Alignment (D-RCV-35, ADR-010) > 14 Story Updates > all other documents |

## Purpose

This register holds every design decision taken in the D-RCV-60 P1 developer-readiness run: the three batches merged in v1 (A, B, C), batch D (v2) and batch E (v3), with the conflicts between them resolved. It is the single place a developer, a reviewer or a later service fix looks to find how an open point of rwb-source-data, or of a neighbour that calls it, was settled, from which sources, and what changed in which stories and documents.

## How later service fixes use it

1. **Look it up before ruling.** Search in this order and stop at the first hit:
   - **By theme ID (TH-nn).** The Themes column of the index and the theme lookup table below give every decision of a theme. Batch D decisions (RD-P1-060 to RD-P1-074) carry no TH theme: they settle the escalation items 1 to 63 of `SET\_work\p1-ready\ESCALATIONS.md`, given in the Escalation items column. Batch E decisions (RD-P1-075 to RD-P1-100) carry no TH theme either: they settle the re-review items and the blocking gaps given in the Escalation items column (re-review row as `<story>#<gap_no>`, and GAP numbers).
   - **By artefact name.** Search this file for the exact name as written in the contract or catalog: operation path with its braces (`GET /customers/{personKey}`), operationId, event type, topic, consumer group, workflow, activity or Schedule name, table, column, parameter key, message code, GAP, ASM or temporary ID. The artefact lookup table below points to the decisions of the most reused artefacts.
   - **By story key.** Search the `affected_stories` column of `Recovery Workbench P1 Decision Register v2.csv` for the full key (for example `RWB-P6-E2022-APP`); every decision that names the story is a row. Keys that batch D left as descriptions are filled in the "Story keys listed by the register" block of the decision and in the CSV.
2. **Apply the final ruling, not the original text.** The original text of each batch is kept word for word for audit. The amendment lines ("Amended by RD-P1-0xx (batch D): …", "Amended by RD-P1-0xx (batch E), register resolution XE-nn: …", "Amended by register (orchestrator; source …): …", "Amended by register resolution X-nn / XD-nn: …") and the **Final ruling (register)** paragraph say what applies; then take the **Reuse note**.
3. **Do not edit a ruling in place.** A later decision that changes a ruling here gets a new RD ID (next free: RD-P1-101) and an amendment line in the decision it changes; it never edits the original text.
4. **Values chosen without a source** were chosen by the model that made the decision. They stand until an owner confirms or replaces them. Temporary IDs (NEW-GAP-…, NEW-ASM-…) are mapped to register numbers in `Temp ID to register ID v1.csv` and by the orchestrator; batch D's NEW-GAP-D1 to NEW-GAP-D5 (mapped to GAP-3283 to GAP-3287 in `Temp ID to register ID v2.csv`) and batch E's NEW-GAP-E1 to NEW-GAP-E5 (next free GAP numbers after GAP-3580) are listed at the end of this file.

### Theme lookup

| Theme | Decisions |
|---|---|
| TH-11 | RD-P1-027 |
| TH-13 | RD-P1-001, RD-P1-006, RD-P1-009 |
| TH-16 | RD-P1-002, RD-P1-003, RD-P1-008 |
| TH-19 | RD-P1-020 |
| TH-20 | RD-P1-021, RD-P1-028 |
| TH-21 | RD-P1-040 |
| TH-22 | RD-P1-007 |
| TH-24 | RD-P1-041 |
| TH-27 | RD-P1-022, RD-P1-028 |
| TH-28 | RD-P1-023 |
| TH-29 | RD-P1-010 |
| TH-31 | RD-P1-008, RD-P1-009 |
| TH-42 | RD-P1-042 |
| TH-48 | RD-P1-044 |
| TH-49 | RD-P1-045 |
| TH-55 | RD-P1-025 |
| TH-59 | RD-P1-046 |
| TH-62 | RD-P1-004 |
| TH-63 | RD-P1-005, RD-P1-006, RD-P1-012 |
| TH-68 | RD-P1-012 |
| TH-69 | RD-P1-024 |
| TH-70 | RD-P1-026 |
| TH-71 | RD-P1-047 |
| TH-72 | RD-P1-048 |
| TH-78 | RD-P1-043 |

### Artefact lookup

| Artefact | Decisions |
|---|---|
| `Idempotency-Key` header, `idempotency_key` table, replay and 409 MSG-PLT-N009-05 | RD-P1-001 |
| `processed_event` (ledger-intake redeliveries; failed-contacts count-once keys) | RD-P1-001, RD-P1-009, RD-P1-070 |
| `Problem` envelope, `messageCode` pattern, status to message code table | RD-P1-004 |
| Wire names, enums, required flags of `rwb-source-data.yaml` 5.1.0; `DataProductFreshness` | RD-P1-005, RD-P1-041 |
| `ETag` / `If-Match`, 428 | RD-P1-006 |
| `InteractionLedgerWriter`, `POST /cases/{caseId}/interactions`, `InteractionRequest`, ledger business key | RD-P1-007, RD-P1-064 |
| LETTER entries, `externalRef`, `GET /proof-of-delivery`, PARTNER_RESULT, ASM-5391 | RD-P1-064, RD-P1-007 |
| `rwb.decision.DecisionRecorded.v1`; decision record versus read | RD-P1-008, RD-P1-072 |
| Ledger intake (consumed-event map, `ce_idempotencykey`, `.dlt`) | RD-P1-009 |
| `listEligibleAccounts`, `GET /efs-history`, `handover.hold_until` | RD-P1-010, RD-P1-067 |
| Contract fakes `fakes/rwb-source-data/5.1.0/` | RD-P1-011 |
| `GET /admin/jobs`, `POST /admin/jobs/{jobId}/rerun`, rerun standard of every service | RD-P1-012, RD-P1-065 |
| `job_run`, `business_day_readiness`, load-state records; local `decision_record` table | RD-P1-020, RD-P1-068 |
| Table, product, seed and write owners | RD-P1-021 |
| Owners of reconciliation, freshness stamps, events, gate, readiness; REC-04, REC-06 | RD-P1-022, RD-P1-069 |
| Case identifier in paths and payloads | RD-P1-023 |
| `case_list_row`, `rwb-case-caselist-daily`, `CaseListDayOpen`, account-page read | RD-P1-024 |
| Data dictionary baseline; dictionary gate MSG-P1-005 | RD-P1-025, RD-P1-071 |
| DP02 read by RW-COMPLY, DPA-2026.11 | RD-P1-026 |
| Migration packages sheet, CARRY / KEY / ACE_READ / EXCLUDE, act-time snapshot fields | RD-P1-027, RD-P1-068 |
| Parameter catalog, `recon.tolerance.pct`, `GET /parameters/{key}` | RD-P1-028, RD-P1-042, RD-P1-063 |
| `AceIngestCheck`, `POST /business-days/{date}/ready`, `GET /business-days/{date}/status`, `ReconciliationWorkflow` | RD-P1-040, RD-P1-065 |
| `rwb.source-data.AceDataReady.v1`, `AceDataLate`, consumer groups, retry and `.dlt` ACLs, JOB-08 owner | RD-P1-003, RD-P1-040, RD-P1-066 |
| Freshness stamp states, STALE, never-stamped product, freshness fixtures | RD-P1-041, RD-P1-062 |
| `DailyCompletenessGate` | RD-P1-041, RD-P1-010, RD-P1-067 |
| Section B views, DL43 flag | RD-P1-043 |
| Shared deployment objects | RD-P1-044 |
| Rollback, forward-only migrations | RD-P1-045 |
| `rwb_sandbox`, seed fixtures, ledger rows in tests | RD-P1-046, RD-P1-073 |
| `POST /retention-runs`, `retention-run-{runDate}`, retention scope | RD-P1-047, RD-P1-048 |
| `GET /customers/{personKey}`, `GET /accounts/{accountKey}`, `GET /collateral/{assetKey}`, `FieldMasker`, recipient name and address | RD-P1-060 |
| `GET /payments` (`businessDate` or `accountKey`) | RD-P1-061 |
| `POST /authorise` (rwb-access), gateway-bff error codes | RD-P1-063 |
| `GET /batch-status`, `BatchStatusAnswer.checksum`, break detail | RD-P1-066, RD-P1-069 |
| JOB-15, JOB-20, DailyCaseRun start, ACE boundary of rwb-payment | RD-P1-066 |
| `POST /contact-points/{contactPointKey}/failed-contacts`, `failed_count` | RD-P1-070 |
| Build chains deeper than 4; E1066-OPS / E1067-APP cycle | RD-P1-074 |
| `ChildWorkflowOptions` reuse policy, `WORKFLOW_ALREADY_EXISTS`, `AceLateCheckStart`, Schedule starts | RD-P1-078, RD-P1-040 |
| `ReadinessRecorder`, repeated ready call after close (XD-11), restart before wave 4 | RD-P1-079 |
| Flag-off answers, 404 MSG-P4-003 for flagged operations, first-release rollback | RD-P1-080, RD-P1-043, RD-P1-045 |
| `FreshnessStampWriter`, `stampDp04`, ON_CHANGE products, DP04 active count and record selection | RD-P1-081, RD-P1-041, RD-P1-068 |
| Page base, `FieldValue.value` formats, DP04 rerun deletes | RD-P1-082 |
| AceDataLate `status` null, in-place re-completion, weekly-only sources, gate value | RD-P1-083 |
| `getProofOfDelivery` publisher, incomplete WIN date | RD-P1-084 |
| REC-05 aggregate row, `ReconciliationResultPage`, reconciliation alerts | RD-P1-086, RD-P1-069 |
| Ledger refusals (`decisionLogId`, `correctsEntryId`, future `occurredAt`, actor check) | RD-P1-087 |
| `rwb-dlt-reason` CASE_NOT_FOUND, VALIDATION_REFUSED, DECISION_REF_REFUSED | RD-P1-088 |
| Ledger series `rwb_source_data_ledger_*`, `rwb-source-data-ledger-check`, `tr_interaction_no_truncate` | RD-P1-089 |
| `appendMigrated`, migrated ledger entries | RD-P1-090 |
| Access-log record AC-READ / AC-DENY, `AccessClient` | RD-P1-091, RD-P1-072 |
| `retention_run`, `retention_review_item`, `GET /retention-runs/{runId}/review-items`, `ageBasis`, archive container | RD-P1-092, RD-P1-047, RD-P1-048 |
| Cutover pipeline stage, sign-off, `manifest.json` / `acceptance.json`, ten clean days, `migration_source` | RD-P1-093, RD-P1-027 |
| `If-None-Match: *`, `GET /extension-facts/...` | RD-P1-094, RD-P1-006 |
| `data_product_access` date (`resolvedOn`), service rows, records field list | RD-P1-095 |
| `sys_objects` writer, DC-ACE seed, `ReferenceLoadApplyHandler`, `applied_reference_version` | RD-P1-096, RD-P1-020 |
| `GET /accounts` (account page, `missingKeys`) | RD-P1-097, RD-P1-024 |
| `is_personal`, Data Classification v6, mask-by-default (Restricted), recipient phone | RD-P1-076, RD-P1-077, RD-P1-060 |
| Dictionary baseline seed (Physical Schema v9) | RD-P1-075, RD-P1-025 |
| Sandbox files and bootstrap interims | RD-P1-098, RD-P1-046 |
| ACE additions foreign keys | RD-P1-099 |
| `GET /batch-status` 404 MSG-P1-001 | RD-P1-085, RD-P1-004 |

## Numbering

- Decision IDs are RD-P1-nnn (Readiness Decision for P1). `R-P1-nnn` was avoided because Assumptions Register v2 already uses it.
- Used: RD-P1-001 to RD-P1-012 (batch A), RD-P1-020 to RD-P1-028 (batch B), RD-P1-040 to RD-P1-048 (batch C), RD-P1-060 to RD-P1-074 (batch D), RD-P1-075 to RD-P1-100 (batch E): 71 decisions.
- Unused: RD-P1-013 to RD-P1-019, RD-P1-029 to RD-P1-039 and RD-P1-049 to RD-P1-059. They are not reserved for anything and are never back-filled. The next new decision is RD-P1-101.
- Conflict references X-nn (v1), XD-nn (v2) and XE-nn (v3) are register-internal labels used only in this file.

## Sources checked for the case-list conflict

- Architecture v5 Text Extract v1 (SET\22): slide 15 P1 card (lines 1073-1079 and 1113-1115) – P1 serves `/customers/{id}`, `/accounts/{id}`, `/collateral/{id}`, `/payments?accountId=`, freshness and `POST /business-days/{date}/ready`; workflows "AceIngestCheck, reconciliation"; schema "ACE view contract, extension tables, freshness, reconciliation"; events in "(none: Airflow call; fallback polls ACE batch record)". Slide 14 rwb-case (lines 980, 1034) – `GET /cases?queue=`. Slide 44 job table (line 2980) – JOB-04 Reconciliation in rwb-source-data. Lines 37 and 503 – no data lake connection. Line 2364 – Airflow sensor polls status until DONE; SLA alerts at 05:30 and 07:00.
- Microservice Ownership Map v2 (SET\22, extract in REVIEW\_reference\22): Tables R17 and Rulings R2 (`case_list_row` P1, basis TSD P1 v3, ASM-A6-tables-2) and Rulings R79 ("Confirmed by the programme directive of 26 November 2026 (D-RCV-60; GAP-0048) ... Confirm in the verification loop").
- Gap Register v2 (SET\23): GAP-2228 "Resolved (directive)" – "drop case_list_row, its key, the extract file, the lake path and the data set under DP-17; and leave REC-01 and REC-05 with RWB-P1-E1011"; also "have rwb-case read the account and freshness answers of RWB-P1-E1015-CON for one page". GAP-0048 "Resolved (directive)" – row table with P1. Both statuses come from the same change-log line (D-RCV-60, 26 November 2026: "the recommended resolution of every gap is accepted").
- Story files (SET\04 Service Story Files v2): the P1 E1002 APP, CON and OPS stories and RWB-P3-E1002-APP (list built in rwb-case).
- Physical Schema v8 `rwb_source_data.sql` lines 823 and 825 (`sys_objects` rows for `case_list_row` and `lake_copy_watermark`); API Specification v6 `rwb-source-data.yaml` lines 900-930 (`DataProductFreshness`); Error and Message Standard v5 rows MSG-P1-002, MSG-P1-011, MSG-P2-006; Batch and Scheduling Design v5 line 33 (COMPLETED).

**Ruling on the known conflict.** RD-P1-024 prevails. The two directive rows contradict each other and carry equal standing; Architecture v5, which sits at the top of the precedence and is the primary design, places no case list, case-list table or case-list workflow in rwb-source-data and gives JOB-04 as reconciliation only. GAP-2228 is the specific, later analysis of the target case list and follows Architecture v5; GAP-0048 adopts a table owner from TSD P1 v3 (lowest tier) pending verification. Every case-list part of RD-P1-002, RD-P1-003, RD-P1-011, RD-P1-012, RD-P1-020, RD-P1-022, RD-P1-040, RD-P1-042, RD-P1-043, RD-P1-044, RD-P1-045 and RD-P1-048 lapses (resolution X-01). Where GAP-2228 names the contract home of the account read (RWB-P1-E1015-CON), the directive is followed over RD-P1-024 item 3 (resolution X-27).

**Note (v2).** XD-09 adds the catalog rows of the rwb-case Schedule named in RD-P1-024 item 2; the ruling on the case-list conflict is unchanged.

## Index

| ID | Title | Themes | Escalation items | Services | Status |
|---|---|---|---|---|---|
| RD-P1-001 | One idempotency standard for every REST POST of rwb-source-data | TH-13 | – | rwb-source-data; PLT library (RWB-PLT-N009, RWB-PLT-TE006); gateway-bff; rwb-case; rwb-comms; rwb-integration; rwb-document | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-002 | Temporal catalog and P1 story names for workflows and activities | TH-16 | – | rwb-source-data; rwb-case; rwb-reporting; rwb-document | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-003 | Kafka catalog: AceDataReady and AceDataLate grain, key and outbox; P1 consumer registrations and ACLs | TH-16 | – | rwb-source-data; rwb-case; rwb-payment; rwb-deviation; rwb-writeoff; gateway-bff; rwb-document; rwb-decision | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-004 | The error envelope is the published Problem schema, extended once | TH-62 | – | All 19 services (shared Problem); rwb-source-data; gateway-bff | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-005 | One contract file per service; wire names, enums and required flags of rwb-source-data 5.1.0 | TH-63 | – | rwb-source-data; gateway-bff; rwb-case; rwb-reporting; rwb-agent; rwb-document; rwb-integration | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-006 | Optimistic concurrency on PUT and PATCH | TH-13; TH-63 | – | rwb-source-data; gateway-bff | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-007 | Interaction ledger: one writer, one append contract | TH-22 | – | rwb-source-data; rwb-case; rwb-comms; rwb-integration; rwb-document; rwb-payment; rwb-treatment; rwb-partner | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-008 | Event type name of DecisionRecorded | TH-31; TH-16 | – | All 19 producers; rwb-decision; rwb-reporting; rwb-source-data | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-009 | Ledger intake: consumed-event map, identity, filtering, retry and parking, ordering | TH-31; TH-13 | – | rwb-source-data; rwb-case; rwb-document; decision-record library producers | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-010 | Case-entry read contract: listEligibleAccounts (not entry-candidates) and the hand-over reads | TH-29 | – | rwb-source-data; rwb-case; rwb-integration; rwb-decision | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-011 | What counts as a published contract fake for DoR item 22, and version pinning | – | – | rwb-source-data; every class C consumer of P1; platform contract fake library | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-012 | Job monitor and rerun: owner, job set, list shape and rerun request | TH-68; TH-63 | – | rwb-source-data; gateway-bff; rwb-integration; rwb-decision; platform | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-020 | Run, readiness and load-state records of rwb-source-data | TH-19 | – | P1 rwb-source-data; P3 rwb-case; P2 rwb-integration; PLT | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-021 | One owner per table, product, seed and write across P1 and its neighbours | TH-20 | – | P1; P2; P3; P4; P5; P6; P7; S5; S6; S9; gateway-bff | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-022 | One owner each for reconciliation, freshness stamps, events, gate and readiness | TH-27 | – | P1; P3; P9 | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-023 | Case identifier in paths, queries and payloads | TH-28 | – | P1; P3; gateway-bff | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-024 | Case list: P3 rwb-case holds the list, P1 drops `case_list_row` | TH-69 | – | P1; P3; P9; gateway-bff | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-025 | Data dictionary baseline: counts, data product seed text and release checks | TH-55 | – | P1 | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-026 | RW-COMPLY read of DP02 in access version DPA-2026.11 | TH-70 | – | P1; P4 | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-027 | Migration package field mapping, allow-list and provenance columns | TH-11 | – | P1; P3; P5; P7; S2; S4; S5; S6; S9 and the other owners of migrated tables | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-028 | Parameter catalog for P1: where parameters live, their owner route, and what replaces the empty file | TH-20; TH-27 | – | P1; P3 | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-040 | Daily ingest, case list and reconciliation triggers, hand-offs and workflow IDs | TH-21 | – | rwb-source-data; rwb-case; rwb-payment; rwb-deviation; rwb-writeoff; gateway-bff | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-041 | Freshness stamp state model: expected date, multiple sources, repeats, late batches, STALE and the single writer | TH-24 | – | rwb-source-data | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-042 | Reconciliation tolerance (DL25) | TH-42 | – | rwb-source-data; rwb-case | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-043 | Section B views dependency (DL43): what builds, deploys and alerts while Section B is absent | TH-78 | – | rwb-source-data | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-044 | One owner per shared rwb-source-data deployment object; no consumer of the service's own AceDataReady | TH-48 | – | rwb-source-data; platform (RWB-PLT-N002) | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-045 | Rollback standard with forward-only migrations | TH-49 | – | rwb-source-data | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-046 | Sandbox scope (shared) and the published seed fixtures | TH-59 | – | rwb-source-data; rwb-case; rwb-access; rwb-document; rwb-deviation; platform (TE004) | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-047 | Retention run interface between P5 JOB-17 and P1, and the held-cases read from P3 | TH-71 | – | rwb-source-data; rwb-document; rwb-case | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-048 | Retention scope, age basis, hold join, REVIEW and delete rules for rwb_source_data | TH-72 | – | rwb-source-data; rwb-document; rwb-case | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-060 | Entity reads of rwb-source-data: customer, account and collateral; recipient name and postal address | – | 10; 16; 23; 51; 59; 61; S8 extra stories; E4045 account read | rwb-source-data; gateway-bff; rwb-comms; rwb-integration; rwb-deviation; rwb-case; rwb-payment; rwb-asset; rwb-access | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-061 | `GET /payments`: one operation, two query forms, one builder | – | 4 | rwb-source-data; rwb-payment; gateway-bff | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-062 | Never-stamped data product: what every reader shows and does; freshness fixtures | – | 17; 18; 22; 62 (first part) | rwb-case; rwb-comms; rwb-decision; rwb-reporting; rwb-agent; rwb-access; gateway-bff | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-063 | Contract operations reported missing: verified state and the remaining additions | – | 25; 29; 34; 46; 47; 49; 51 (gateway codes); 54 | rwb-case; rwb-access; gateway-bff; rwb-partner; rwb-writeoff; rwb-source-data | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-064 | Interaction ledger callers: letter dispatch and delivery entries, hand-recorded proof, permissions and entry types | – | 1; 26; 32; 37; 39; 40; 41; 50; 59 (second part); 60; 62 (second part); 63; extra stories RWB-P3-E2021-APP, RWB-P3-E2016-CON, RWB-P10-E1062-APP, RWB-P6-E2021-CON | rwb-source-data; rwb-comms; rwb-integration; rwb-case; rwb-partner; rwb-asset; rwb-agent; rwb-access | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-065 | Job reads and reruns across services; readiness repeats | – | 12; 24; 27; 31 (rerun part); 48; 57 (first part) | rwb-source-data; rwb-case; rwb-decision; rwb-integration; all services with jobs | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-066 | Event subscriptions, start rules and job owners; ACE boundary of rwb-payment | – | 5; 11 (start part); 13; 14; 15; 19; 20; 21; 30; 45; 53; ACE boundary E4044/E4045 | rwb-payment; rwb-integration; rwb-writeoff; rwb-case; rwb-decision; rwb-reporting; rwb-deviation; gateway-bff; rwb-source-data | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-067 | EFS history: gate products, late EFS batch and the single appender | – | 2; 11; 26 | rwb-integration; rwb-case; rwb-source-data | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-068 | Migration packages: decision chain, act-time snapshot fields, DM002, DM007 key, orphan checks, DP04, loader identity, local decision record table | – | 6; 7; 8; 9; 35; 36; 52; 57 (second part) | rwb-source-data; rwb-decision; rwb-case; rwb-asset; platform | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-069 | Reconciliation breaks, orphan keys, REC-04/REC-06 and date-wide reads | – | 31 (break list); 33; 38 (held proof rows, REC-09); 42; 43; 44 | rwb-source-data; rwb-payment; rwb-case; rwb-asset | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-070 | Count-once store for failed contacts | – | 3 | rwb-source-data; rwb-comms | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-071 | Data dictionary gate and new fields | – | 55 | rwb-access; rwb-source-data | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-072 | Decision records versus reads in the ledger intake; personal data seen by agents | – | 38 (call notes); 56 | rwb-access; rwb-source-data; rwb-agent; rwb-decision | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-073 | Test isolation for append-only rows and the shared sandbox | – | 28; 38 (sandbox) | rwb-source-data; rwb-case; rwb-access; rwb-deviation; platform | Proposed – Claude Opus 5.5 (applied) – amended |
| RD-P1-074 | Build-chain depth and the E1066-OPS / E1067-APP cycle | – | 58 | rwb-source-data | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-075 | Data dictionary baseline: values copied from Physical Schema v9 | – | E1001-APP#1 (ruling); amends RD-P1-025 | rwb-source-data | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-076 | Personal-data flag: Data Classification v6 governs; default masking by classification | – | E1001-APP#2 (document); E1068-APP#4; E2010-CON#13; GAP-3529; amends RD-P1-060 rule 2 | rwb-source-data; rwb-access (masking rules, FieldMasker fake); every service that uses FieldMasker | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-077 | Recipient phone number for SMS and LINE notices | – | Orchestrator question; narrows GAP-3283 | rwb-source-data; rwb-comms; rwb-access | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-078 | Temporal start mechanisms: client starts, child starts and Schedule starts | – | Orchestrator question; amends RD-P1-040, RD-P1-002 | rwb-source-data; every service that starts child workflows or Schedule-started per-date work (reuse) | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-079 | Readiness after the run closes, the readiness recorder and restarts before wave 4 | – | XD-11; E1013-APP#1 (story), E1013-APP#8; GAP-3390 | rwb-source-data | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-080 | Flag-off answers: freshness never 404; 404 MSG-P4-003 for other flagged operations | – | E1015-OPS#1; GAP-3506; amends RD-P1-043, RD-P1-045 | rwb-source-data; consumers of freshness (no change) | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-081 | ON_CHANGE products and the DP04 stamp; active-count check; DP04 record selection | – | E2010-APP#3, #4, #6; E2010-CON#2, #7; E2010-OPS#2; E2010-APP#1 and E2010-CON#1 (story); GAP-3525, GAP-3524; amends RD-P1-041, RD-P1-068 | rwb-source-data; rwb-treatment (parameter row) | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-082 | DP04 build reads, rerun and the records read value formats | – | E2010-CON#3, #6; GAP-3523, GAP-3528, GAP-3571, GAP-0512 | rwb-source-data; rwb-treatment; rwb-guarantee | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-083 | Freshness stamp edge cases: missing batch row, re-completion, restatement detection, weekly-only sources, gate value | – | E1015-APP#1, #2; E1015-CON#1; GAP-3430, GAP-3429, GAP-3288, GAP-3434 | rwb-source-data; AceDataLate consumers (alerts, gateway-bff banner) | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-084 | Proof-of-delivery: incomplete WIN date and the contract publisher | – | E1055-APP#1, #14 | rwb-source-data; rwb-comms | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-085 | `GET /batch-status` with no batch row: 404 MSG-P1-001 (directive exception) | – | E2007-APP#2; amends RD-P1-004 | rwb-source-data; rwb-integration; rwb-payment | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-086 | Reconciliation results: REC-05 aggregate row, result page, alert values, rwb-case inputs | – | E1011-CON#3; AD019-APP#1 (document); E1011-OPS#5; GAP-3412, GAP-3418, GAP-3421, GAP-3422, GAP-3411 | rwb-source-data; rwb-payment, rwb-case (readers) | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-087 | Ledger writer refusals and the actor check | – | E1066-APP#1; E1066-CON#1; GAP-3487, GAP-3489, GAP-3492 | rwb-source-data; rwb-case; every REST caller of the ledger | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-088 | Ledger intake: refusals that are not transient | – | E1067-APP#1; E1067-CON#1; GAP-3496 | rwb-source-data | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-089 | Ledger series, integrity check, protection of append-only objects and the sandbox reload | – | E1066-OPS#1; E1065-APP#1; GAP-3494, GAP-3493 | rwb-source-data; platform (NF06, N011) | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-090 | Migrated ledger entries: the cutover entry point of the writer | – | DM005-APP#1 (story) | rwb-source-data | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-091 | Access-log entries are written through the rwb-access access-log contract, never as decision records | – | RD-P1-072 vs RWB-P4-E1023-APP and RWB-P4-E1039; E1068-APP#2 (document); GAP-3395, GAP-3322 | rwb-access; rwb-source-data; rwb-case; gateway-bff; every service that reads personal data | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-092 | Retention run record, review list, age bases, record classes and the archive container | – | E1017-APP#1, #4, #5; E1017-OPS#1; GAP-3457, GAP-3454, GAP-0490 | rwb-source-data; rwb-document (JOB-17 caller); rwb-case (closure and exclusion reads) | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-093 | Migration cutover: provenance columns, pipeline authorisation, handover package and acceptance, clean days | – | DM003-APP#1, DM004-APP#1, DM007-APP#1 (document); DM006-APP#1, DM007-APP#2 (story); orchestrator questions | rwb-source-data; rwb-case, rwb-treatment, rwb-asset, rwb-litigation, rwb-comms, rwb-partner, rwb-decision, rwb-payment (owner loads) | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-094 | Extension facts: first write, the read of the row and its ETag, access rule | – | E1018#3; GAP-3555, GAP-3409, GAP-3407 | rwb-source-data; gateway-bff; rwb-access | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-095 | Data-product access: date of the access check, workload identities, field lists, catalog reconciliations | – | E1016-APP#11; E1016-CON#8; GAP-3443, GAP-3445, GAP-3446 | rwb-source-data; rwb-access; rwb-comms; rwb-integration; gateway-bff | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-096 | Dictionary and contract rows: object rows, DC-ACE seed, smoke records, reference-load handler, applied version | – | E1064-APP#3; E1064-APP#1, E1064-OPS#1 (story); E1064-APP#2, E1064-CON#2 (document); GAP-3338, GAP-3403; amends RD-P1-020 | rwb-source-data; rwb-case | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-097 | Account-page read used by rwb-case for the case list | – | GAP-3274, GAP-3438 | rwb-source-data; rwb-case | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-098 | Sandbox contract files and bootstrap: interim build | – | E1065-CON#1 (story); GAP-3481 to GAP-3486 | rwb-source-data; platform DB; rwb-case | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-099 | ACE additions: foreign-key delete rules, orphan rows and load order (interim) | – | ACE001-DB#4; GAP-3576 | ACE (RWB-ACE-001); rwb-source-data | Proposed – Claude Opus 5.5 (applied) |
| RD-P1-100 | Smaller rulings: snapshot(page), SCR-44 route, holder pair, delivery status name, EFS rows, complaints, DM012 to DM014 | – | E1013-APP#2; AD018-OPS#1 (document); E2034-APP#1 (story); E1068-APP#1 (document); E2001-APP#1 (document); DM012-APP#1, DM013-APP#1, #2, DM014-APP#1, #2 (story); GAP-3375, GAP-3327, GAP-3425, GAP-3384 | rwb-source-data; rwb-reporting; gateway-bff; rwb-case; rwb-integration; rwb-agent; rwb-writeoff | Proposed – Claude Opus 5.5 (applied) |

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

## Batch D and orchestrator amendments (v2)

Each resolution is written as an amendment line in the decision it changes and in its final ruling. XD-nn are register-internal labels used only in this file.

| Ref | Artefact | Decisions | Resolution | Source | Prevails |
|---|---|---|---|---|---|
| XD-01 | Consumers of `rwb.source-data.events.v1`; consumer groups; retry and `.dlt` ACLs | RD-P1-003 rule 1, rule 6 and Affected services vs RD-P1-066 rules 2, 3, 4, 11 | rwb-integration added as consumer (JOB-08); one group per consumer service with one listener; retry and `.dlt` ACLs for every consumer service; GL monthly branch of rwb-writeoff is a clarification of rule 1. | Batch D, register amendments list | RD-P1-066 |
| XD-02 | Owner of JOB-08; start rules of downstream daily jobs | RD-P1-040 item 2 vs RD-P1-066 rules 2-4, 6 | JOB-08 is rwb-integration's (GAP-0657 directive supersedes the Arch v5 slide 44 owner row for this job); rwb-payment keeps JOB-07; DailyCaseRun event-started. | Batch D, register amendments list | RD-P1-066 |
| XD-03 | Delivery entry `externalRef` and business key; dispatch entry; REST callers' permissions; rwb-partner append | RD-P1-007 rule 7 (`externalRef` = pod_key) vs RD-P1-064 rules 2-5, 9, 13 | `externalRef` = WIN barcode, else noticeRef; key with UUID v5 of `podKey`; dispatch entry pairs on the barcode; service rows "Case record C"; rwb-partner appends PARTNER_RESULT over REST (ASM-5391 changed). | Batch D, register amendments list | RD-P1-064 |
| XD-04 | Gate of `GET /efs-history` | RD-P1-010 rule 8 (DP01, as amended in v1) vs RD-P1-067 rule 1 | DP01 and DP05; `listEligibleAccounts` keeps DP01. | Batch D, register amendments list | RD-P1-067 |
| XD-05 | Local `decision_record` table of `rwb_source_data` | RD-P1-020 H ("no P1 decision-record table") vs RD-P1-068 rule 8 | The library table exists (Arch v5 line 1477); DDL Pending NEW-GAP-F08-7. | Batch D, register amendments list | RD-P1-068 |
| XD-06 | Migration allow-list: act-time snapshot fields, DM007 key, DM002 clause, orphan checks, loader identity | RD-P1-027 rule 2 and its DM002 and DM007 bullets vs RD-P1-068 rules 2-5, 7 | CARRY "value at act time" for DF-DEC-006, DF-FIN-006, DF-FIN-007; DF-LEG-005 KEY; DM002 clause moves to DM005; orphan checks per DM story; target-service loader. | Batch D, register amendments list | RD-P1-068 |
| XD-07 | `Problem.messageCode` pattern | RD-P1-004 rule 2 (`-\d{3}$`) vs RD-P1-001 and RD-P1-004 rule 3 (MSG-PLT-N009-03, -05, -06) | Pattern `^MSG-[A-Z0-9]+(-[A-Z0-9]+)*-\d{2,3}$`. | Orchestrator; REQUEST W3-messages-0078 | Register |
| XD-08 | In-process callers of `InteractionLedgerWriter` | RD-P1-007 rule 1 (as amended in v1) and RD-P1-064 rule 1 vs staged RWB-P1-DM005-APP v3 | RWB-P1-DM005-APP added (cutover write of migrated notes and promises, same transaction as `contact_point_ext`). Batch D does not contradict it (RD-P1-064 rule 1 restates the v1 list; RD-P1-068 rule 7 loads each package in its target service). | Orchestrator; REQUEST S12-stories-0340 | Register |
| XD-09 | Schedule `rwb-case-caselist-daily` and workflow `CaseListDayOpen` | RD-P1-024 item 2 (Schedule owned by rwb-case, no catalog row) | Entered in Temporal Workflow and Activity Catalog v3 and Batch and Scheduling Design v7 by the runtime writers; no P1 object. The workflow ID form `case-list-{businessDate}` against the RD-P1-022 reuse note is left open for the rwb-case owner. | Orchestrator; W5-runtime-0359, -0362, -0365, -0368; FD3-runtime-0143 | Register |
| XD-10 | What `processed_event` may hold | RD-P1-001 final rule 7 and X-19 ("ledger-intake redeliveries only") vs RD-P1-070 (failed-contacts count-once keys) | RD-P1-070 stands: it uses the in-process work-key form of the original rule 7 (R-UNI-40, `event_id` null) for this one operation; EFS and proof-of-delivery keys stay out. | Register (found while merging batch D) | RD-P1-070 |
| XD-11 | Repeated readiness call after AceIngestCheck has closed | RD-P1-040 item 1 Closing and X-18 (a late batch after the run closed is picked up by a repeated ready call, ALLOW_DUPLICATE) vs RD-P1-065 rule 3 ("once the row is DONE or LATE it starts nothing") | Merged: the call starts nothing when every due source is stamped; when a due source is still unstamped after the run closed (24 h), it opens a new run that stamps only the missing sources. Never a second AceDataReady for a stamped source or a second ReconciliationWorkflow. Confirmation by the P1 owner is recommended. | Register (found while merging batch D) | Merged |

## Batch E amendments (v3)

Each resolution is written as an amendment line in the decision it changes and in its final ruling. XE-nn are register-internal labels used only in this file.

| Ref | Artefact | Decisions | Resolution | Source | Prevails |
|---|---|---|---|---|---|
| XE-01 | Child workflow and Schedule starts | RD-P1-040 item 1 ID policy and reuse note; RD-P1-002 rows vs RD-P1-078 | Client starts keep USE_EXISTING + ALLOW_DUPLICATE; child starts use a deterministic ID, ALLOW_DUPLICATE_FAILED_ONLY and already-started = started; the 05:30 Schedule starts AceLateCheckStart. | Batch E (orchestrator question; Temporal behaviour, TWAC v3) | RD-P1-078 |
| XE-02 | `GET /batch-status` no row | RD-P1-004 status table vs GAP-0597 directive | 404 MSG-P1-001 as the one exception. | Batch E | RD-P1-085 |
| XE-03 | First write of extension facts | RD-P1-006 (If-Match required) | `If-None-Match: *` for the first write; GETs return the ETag. | Batch E | RD-P1-094 |
| XE-04 | Cutover writes to the ledger | RD-P1-007 server-set fields vs RWB-P1-DM005-APP | `appendMigrated` entry point. | Batch E | RD-P1-090 |
| XE-05 | Ledger writer refusals | RD-P1-007 (pending answers GAP-3487, GAP-3489, GAP-3492) | Statuses and codes ruled. | Batch E | RD-P1-087 |
| XE-06 | Intake non-transient refusals | RD-P1-009 (GAP-3496) | Park at once with three reason values. | Batch E | RD-P1-088 |
| XE-07 | Dictionary rows of new tables; applied reference version | RD-P1-020 D (governed load) and G | Rows come with the table's migration; new column. | Batch E | RD-P1-096 |
| XE-08 | Retention run record | RD-P1-020, RD-P1-047 (no run table, GAP-3457) | `retention_run`, `retention_review_item`, review-items read. | Batch E | RD-P1-092 |
| XE-09 | Readiness transitions | RD-P1-020 F (writer of business_day_readiness for non-HTTP starts) | ReadinessRecorder. | Batch E | RD-P1-079 |
| XE-10 | Account-page read | RD-P1-024 item 3 and X-27 (GAP-3274, GAP-3438) | `GET /accounts`. | Batch E | RD-P1-097 |
| XE-11 | Dictionary baseline seed version | RD-P1-025 (Physical Schema v8) vs staged Physical Schema v9 | Copy from v9. | Batch E (orchestrator question) | RD-P1-075 |
| XE-12 | Repeated readiness call after the run closes | XD-11; RD-P1-040 item 1; RD-P1-065 rule 3; TWAC v3 R18 | XD-11 confirmed with its mechanism; R18 text replaced. | Batch E (orchestrator question) | RD-P1-079 |
| XE-13 | DP04 STALE and DP04 stamp writer | RD-P1-041 items 4 and 7 and GAP-0511 line vs RD-P1-068 rule 6; RD-P1-002 stampDp04 | ON_CHANGE never STALE by time; stampDp04 the only DP04 writer through the single stamp component. | Batch E (orchestrator question; GAP-3525) | RD-P1-081 |
| XE-14 | Freshness edge cases | RD-P1-041 items 3 and 6, RD-P1-003 payload (GAP-3430, GAP-3429, GAP-3288) | In-place re-completion; nullable AceDataLate status; weekly-only source run. | Batch E | RD-P1-083 |
| XE-15 | Clean-day counting | RD-P1-042 clean day | REC-05 row included; a date with no row resets. | Batch E (orchestrator question) | RD-P1-093 |
| XE-16 | Flag-off answer of freshness | RD-P1-043 item 3 vs RD-P1-045 item 4 | Freshness and readiness never 404; other flagged operations 404 MSG-P4-003. | Batch E (orchestrator question) | RD-P1-080 |
| XE-17 | Retention age bases and record classes | RD-P1-048 item 2 (GAP-3454) | Values per table. | Batch E | RD-P1-092 |
| XE-18 | Personal-data flag and masking default | RD-P1-060 rule 2; RD-P1-025 seed vs DCPI v6 | DCPI v6 governs; mask by default only Restricted fields. | Batch E (orchestrator question) | RD-P1-076 |
| XE-19 | Recipient phone | RD-P1-060 rule 3 | PHONE and EMAIL clear for the rwb-comms notice identity. | Batch E (orchestrator question) | RD-P1-077 |
| XE-20 | Delivery status name | RD-P1-064 (`latestDeliveryStatus`) vs YAML `barcodeStatus` | `latestDeliveryStatus` with its derivation. | Batch E | RD-P1-100 |
| XE-21 | REC-05 served | RD-P1-069 / RD-P1-022 vs RWB-P1-E1011-CON s11 | Aggregate row. | Batch E | RD-P1-086 |
| XE-22 | Access-log entries | RD-P1-072 vs RWB-P4-E1023-APP (decision-record library) | Access-log contract of rwb-access. | Batch E (orchestrator question) | RD-P1-091 |
| XE-23 | Ledger protection and sandbox rebuild | RD-P1-073 rule 1 vs RWB-P1-E1066-OPS AC11 | Grants, TRUNCATE trigger, rebuild by schema drop. | Batch E | RD-P1-089 |

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
- Amended by register resolution XD-10 (batch D, RD-P1-070): Rule 7 and the X-19 sentence "`processed_event` holds ledger-intake redeliveries (ce_id) only": `processed_event` also holds the count-once keys of `POST /contact-points/{contactPointKey}/failed-contacts` – `consumer` `rwb-source-data.failed-contacts`, `idempotency_key` `FC:` followed by the lowercase hex SHA-256 of `<contactPointKey>|<reference>`, `event_id` null; a repeat adds 1 to `hit_count` and leaves `failed_count` unchanged (RD-P1-070). This is the in-process work-key form of the original rule 7 (R-UNI-40), kept for this one operation; EFS history and proof-of-delivery keys stay out (X-19).

**Final ruling (register).** Rules 1-5, 8 and 9 apply unchanged. Rule 6 retention bullet: ID `retention-run-{runDate}`, FAIL + ALLOW_DUPLICATE_FAILED_ONLY, 409 MSG-P2-006 while RUNNING or after COMPLETED, 202 after FAILED. Rule 7: `processed_event` holds two kinds of row only: ledger-intake event redeliveries (by ce_id, counted in `hit_count`) and the failed-contacts count-once keys of RD-P1-070 (consumer `rwb-source-data.failed-contacts`, key `FC:` + SHA-256 hex, `event_id` null); EFS repeats are counted by the P2 run, DP07 delivery repeats by metric `rwb_source_data_win_delivery_repeat_total`.

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
- Amended by RD-P1-078 (batch E), register resolution XE-01: Child starts of `ReconciliationWorkflow` (`recon-{businessDate}`) and `Stage2ProductWorkflow` (`stage2-dp04-{businessDate}`) use the deterministic workflow ID, ParentClosePolicy ABANDON and WorkflowIdReusePolicy ALLOW_DUPLICATE_FAILED_ONLY, with no conflict policy (a child start has none); the parent waits for the child start promise; a start that fails because the ID exists (`WORKFLOW_ALREADY_EXISTS`) is treated as started. The 05:30 Schedule starts `AceLateCheckStart`, whose activity `startIngestForExpectedDate` client-starts `ace-ingest-check-{businessDate}`.

**Final ruling (register).** Registered P1 workflows: `AceIngestCheck` (`ace-ingest-check-{businessDate}`; built by RWB-P1-E1015-APP; started by the readiness handler of RWB-P1-E1013-APP, the 05:30 Schedule `rwb-source-data-ace-late-check` and the fallback poll; activities `readBatchStatus`, `stampProducts`, `markStale`, `checkDailyCompleteness`), `ReconciliationWorkflow` (`recon-{businessDate}`; child of AceIngestCheck after the ALS stamp, and admin rerun; one activity `reconciliation`), `Stage2ProductWorkflow` (`stage2-dp04-{businessDate}`; child of AceIngestCheck after the ALS stamp; activities `readDp04SourcePage`, `writeDp04Page`, `checkActiveCount`, `stampDp04`), `RetentionRunWorkflow` (`retention-run-{runDate}`; eight activities). Shared activities `listEligibleAccounts` (RWB-P1-E1018-APP) and `snapshot(page)` (RWB-P1-E1013-APP) keep their Architecture v5 meaning. No case-list workflow, activity or Schedule exists in P1. Batch E (v3): child starts use a deterministic ID with ALLOW_DUPLICATE_FAILED_ONLY and already-started = started; the 05:30 Schedule starts AceLateCheckStart (RD-P1-078).

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
- Amended by RD-P1-066 (batch D), register resolution XD-01: Consumers of `rwb.source-data.events.v1` (rule 1 and Affected services) add rwb-integration for JOB-08 (GAP-0657 directive; RD-P1-066 rule 3), with consumer group `rwb-integration.rwb.source-data.events.v1` and a READ ACL in Kafka Topic and Event Catalog v3; rwb-payment keeps JOB-07. Rule 6 applies to every consumer service: one group per service per topic (working ID `<service>.<topic>`, for example `rwb-payment.rwb.source-data.events.v1`) with one listener that starts the service's runs by signal-with-start on their own workflow IDs; per-story groups are withdrawn (RD-P1-066 rule 2). Each consumer service holds WRITE and READ on the retry topics and WRITE on the `.dlt` topic of every topic it consumes (names per RWB-PLT-E1047-CON; RD-P1-066 rule 11). Rule 1 "start on sourceSystem ALS" governs daily work; a non-daily consumer may act on another source: rwb-writeoff's monthly GL write-off reconciliation starts on AceDataReady with `sourceSystem` GL and `status` COMPLETED (RD-P1-066 rule 4, clarification).

**Final ruling (register).** Rules 2-4 and 6 apply. EV-26 is published once per source system and business date (status COMPLETED); downstream daily work starts only on sourceSystem ALS, and a non-daily consumer may act on another source (rwb-writeoff monthly GL branch, RD-P1-066 rule 4). rwb-source-data reads `rwb.case.events.v1`, `rwb.document.events.v1`, `rwb.decision-record.v1` (ledger intake) and their retry topics, writes `rwb.source-data.events.v1` and `rwb.decision-record.v1`, and does not consume its own topic. Consumers of `rwb.source-data.events.v1` include rwb-integration (JOB-08, group `rwb-integration.rwb.source-data.events.v1`, READ ACL) and rwb-payment (JOB-07 with E4044, E4047 and E4050, one group `rwb-payment.rwb.source-data.events.v1`); every consumer service has one group per topic with one listener fanning out by signal-with-start, and WRITE and READ on the retry topics and WRITE on the `.dlt` topic of each topic it consumes.

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
- Amended by register (orchestrator; source REQUEST W3-messages-0078 in `SET\_work\p1-ready\editlog\W3-messages.csv`), register resolution XD-07: Rule 2: the `messageCode` pattern is widened from `^MSG-[A-Z0-9]+(-[A-Z0-9]+)*-\d{3}$` to `^MSG-[A-Z0-9]+(-[A-Z0-9]+)*-\d{2,3}$` (two or three final digits), so that MSG-PLT-N009-03, MSG-PLT-N009-05 and MSG-PLT-N009-06, which RD-P1-001 and the table of rule 3 require, validate; three-digit codes such as MSG-GEN-001 and MSG-P1-022 validate as before. The staged `rwb-source-data.yaml` 5.1.0 (`Problem`, lines 2148 and 2165) still carries the three-digit pattern and is changed by its owner.
- Amended by RD-P1-085 (batch E), register resolution XE-02: One exception to the status table: `GET /batch-status` with no `v_ace_batch_status` row for the source and date answers 404 MSG-P1-001 (GAP-0597, D-RCV-60 directive); 404 MSG-P4-003 keeps its meaning everywhere else.

**Final ruling (register).** Rules 1-4 apply; the `messageCode` pattern of rule 2 is `^MSG-[A-Z0-9]+(-[A-Z0-9]+)*-\d{2,3}$`; the state-conflict row takes the code the Error and Message Standard v5 assigns (MSG-P1-011 load or rerun already complete or running; MSG-P2-006 retention run of the same date running or complete). Batch E (v3): exception: `GET /batch-status` with no batch row answers 404 MSG-P1-001 (RD-P1-085).

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

- Amended by RD-P1-094 (batch E), register resolution XE-03: Clarification: the first write of an extension-facts key sends `If-None-Match: *` and is answered 201 with `ETag: "1"`; `If-None-Match: *` on an existing row, or If-Match on a key with no row, answers 409 MSG-GEN-004; neither header answers 428 MSG-GEN-004. `GET /extension-facts/parties/{personKey}` and `GET /extension-facts/accounts/{accountKey}` return the row and its ETag.

**Final ruling (register).** As ruled above, amended by batch E (v3): first write with `If-None-Match: *` (201); the two extension-facts GETs return the ETag (RD-P1-094).

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
- Amended by RD-P1-064 (batch D), register resolution XD-03: Rule 7: the delivery entry's `externalRef` is the WIN `barcode` of the row, else its `noticeRef` when `barcode` is null; a row with neither is not matched (no entry; rwb-comms logs it as unmatched); `occurredAt` = `callbackDate` at 00:00 Asia/Bangkok; business key `LETTER-<caseNo>-<yyyyMMdd of callbackDate>-<u>`, where `<u>` is the UUID version 5 of `podKey` in the RFC 9562 URL namespace. `externalRef` = pod_key and the raw pod_key in the key are withdrawn (`podKey` 255 exceeds `externalRef` 60 and `idempotencyKey` 120). The dispatch entry rwb-comms appends when the WIN file is sent carries `externalRef` = the same barcode, `deliveryStatus` SENT, `conductCheck` PASSED, `sourceRef` `INT-14 WIN` and key `LETTER-<caseNo>-<yyyyMMdd of sent date>-<noticeId>`, so dispatch and delivery pair on `externalRef`; a hand-recorded proof is appended by rwb-comms only (`actorType` USER). The mapping of WIN `delivery_status` values is Pending (NEW-GAP-D3).
- Amended by RD-P1-064 (batch D): REST callers. Each REST caller appends under its own workload identity with a service-identity row "Case record C on rwb-source-data" in Users Roles and Permissions v6 and Role to System Access Matrix v4 (RD-P1-064 rule 2); rwb-partner appends partner results over REST (`eventCode` PARTNER_RESULT, `actorType` PARTNER, `actorRef` the partner code; ASM-5391 changed from "through the published event"); on 503 MSG-P1-022 a caller does not commit its action, or retries with the same header and business keys (RD-P1-064 rule 13).
- Amended by register (orchestrator; source REQUEST S12-stories-0340 in `SET\_work\p1-ready\editlog\S12-stories.csv`), register resolution XD-08: Rule 1: RWB-P1-DM005-APP is an in-process caller of `InteractionLedgerWriter`: at cutover it writes one `interaction` row per migrated note or promise through the writer (which allocates `case_seq`; INSERT only, no UPDATE or DELETE), in the same transaction as its `contact_point_ext` rows, idempotent on the legacy record key (staged RWB-P1-DM005-APP v3 sections 4, 12 and 13). Batch D does not contradict it: RD-P1-064 rule 1 restates the v1 final list, and RD-P1-068 rule 7 has each package loaded by its target service, here rwb-source-data.
- Amended by RD-P1-090 (batch E), register resolution XE-04: Clarification: RWB-P1-DM005-APP calls `InteractionLedgerWriter.appendMigrated(MigratedInteraction)` (in process, behind the DM005 cutover switch), which keeps the legacy `occurredAt` and actor and sets `id`, `caseSeq`, `sourceSystem` WORKBENCH, `migration_source` and `migrated_at`.
- Amended by RD-P1-087 (batch E), register resolution XE-05: Clarification: writer refusals – DECISION_TAKEN without `decisionLogId` 422 MSG-GEN-001; an unknown or other-case `decisionLogId` or `correctsEntryId` 422 MSG-GEN-007 naming the field; decision-log read unanswered 503 MSG-P1-022; `occurredAt` beyond receipt plus 300 s 422 MSG-GEN-003; another service identity whose case read answers 404 gets 404 MSG-P4-003; a delegated user token must carry actorType USER and `actorRef` = its user identifier (else 403 MSG-P4-002).

**Final ruling (register).** Rules 2-6 and 8 apply; rule 7 as amended by RD-P1-064. In-process callers of InteractionLedgerWriter: RWB-P1-E1067-APP, RWB-P1-E2034-APP and RWB-P1-DM005-APP (cutover only). Every other service appends over REST under its own workload identity with a "Case record C on rwb-source-data" service row (rwb-case, rwb-comms, rwb-integration, rwb-document, rwb-payment, rwb-treatment, rwb-partner; rwb-partner with PARTNER_RESULT, ASM-5391 changed). Delivery entries are appended only by rwb-comms: dispatch and delivery pair on `externalRef` = WIN barcode (else noticeRef); delivery key `LETTER-<caseNo>-<yyyyMMdd of callbackDate>-<uuid5(podKey)>`; DP07 delivery repeats are a metric. EFS history is appended only by the P2 hand-over run (rule 8; RD-P1-067). Batch E (v3): DM005 writes through `appendMigrated` (RD-P1-090); writer refusals and actor check per RD-P1-087.

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

- Amended by RD-P1-088 (batch E), register resolution XE-06: A writer refusal that a retry cannot cure is parked at once on `<topic>.dlt` with `rwb-dlt-reason` CASE_NOT_FOUND, VALIDATION_REFUSED (plus `rwb-dlt-field`) or DECISION_REF_REFUSED; the offset is committed after the `.dlt` write; no LEDGER_WRITE_FAILED (kept for RETRIES_EXHAUSTED).

**Final ruling (register).** As ruled above, amended by batch E (v3): non-transient refusals park at once with CASE_NOT_FOUND, VALIDATION_REFUSED or DECISION_REF_REFUSED (RD-P1-088).

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
- Amended by RD-P1-067 (batch D), register resolution XD-04: Rule 8: `GET /efs-history` is gated on DP01 and DP05 – it refuses with 409 MSG-P1-001 unless both are complete for the business date (DailyCompletenessGate over both products; YAML 5.1.0 text "The DP01 and DP05 freshness gate must pass" kept), not on DP01 alone as the previous amendment line read; this aligns rule 8 with RD-P1-041 item 8 (JOB-02 reads DP05). `listEligibleAccounts` keeps the DP01 gate of rule 4. A late EFS batch is handled by the P2 hand-over run (durable-timer retry every 5 minutes up to `handover.hold_until`, Pending NEW-GAP-D4; RD-P1-067 rule 2). A never-stamped product refuses with `lastCompleteBusinessDate` null (RD-P1-062 rule 2, no change).

**Final ruling (register).** Rules 1-3 and 5-8 apply; the gate of rule 4 (`listEligibleAccounts`) is DailyCompletenessGate for DP01 (ALS row, status COMPLETED, with the RD-P1-021 seed); the gate of rule 8 (`GET /efs-history`) is DailyCompletenessGate for DP01 and DP05 (RD-P1-067).

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
- Amended by RD-P1-068 (batch D), register resolution XD-05: H: the sentence "there is no P1 decision-record table" is replaced. `rwb_source_data` has the local `decision_record` table that every service owns (Arch v5 line 1477: "Own schema: business tables + outbox + inbox + decision_record"), created by the shared library migration of RWB-PLT-E1027-CON; the sandbox smoke check and RWB-P1-DM012-APP write their decision records through that library. Its DDL is in no schema file of Physical Schema v9: Pending, owner platform lead (library owner), NEW-GAP-F08-7; interim the library's own migration runs in the Testcontainers build. `ce_idempotencykey` = the RD-P1-007 rule 4 business key. P1 still never writes `rwb_decision.decision_log_entry`; the rest of H (relay off in the sandbox; the acceptance criterion counts `outbox_event` rows) is unchanged.
- Amended by RD-P1-096 (batch E), register resolution XE-07: D: the `sys_objects` and `sys_fields` rows of `job_run`, `job_run_check`, `business_day_readiness` and of every later P1 table are written by the migration that creates the table, not by the governed load of RWB-P1-E1064-APP. G: `data_product`, `data_product_access` and `data_product_source` gain nullable `applied_reference_version integer`; the apply handler skips a version that is not greater.
- Amended by RD-P1-092 (batch E), register resolution XE-08: `rwb_source_data` adds `retention_run` and `retention_review_item` (RWB-P1-E1017-APP migrations).
- Amended by RD-P1-079 (batch E), register resolution XE-09: F: `business_day_readiness` is written only through `ReadinessRecorder` of RWB-P1-E1013-APP: `recordReceived` by the ready handler and by the first activity of a non-HTTP start; `recordState` DONE or LATE by RWB-P1-E1015-APP in the ALS stamp and ALS AceDataLate transactions; LATE may become DONE, DONE is final.

**Final ruling (register).** Tables A, B, D, G apply. H applies with the local `decision_record` table of `rwb_source_data` (library DDL of RWB-PLT-E1027-CON, Pending NEW-GAP-F08-7; P1 never writes `rwb_decision.decision_log_entry`). C: job set AceIngestCheck (`job_type` `AceIngestCheck`), ReconciliationWorkflow (JOB-04), Stage2ProductWorkflow, RetentionRunWorkflow. E: sources COMPLETED. F: DONE once ALS is stamped; LATE once AceDataLate is out with ALS not COMPLETED; `idempotency_key` = UUID header of the first call. Batch E (v3): dictionary rows come with each table's migration; `applied_reference_version` added (RD-P1-096); retention_run and retention_review_item added (RD-P1-092); readiness transitions through ReadinessRecorder (RD-P1-079).

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
- Amended by register (orchestrator; sources `SET\_work\p1-ready\editlog\W5-runtime.csv` rows W5-runtime-0359, -0362, -0365 and -0368 and `FD3-runtime.csv` row FD3-runtime-0143, the runtime writers), register resolution XD-09: Item 2's Schedule `rwb-case-caselist-daily` is entered in the catalogs: Temporal Workflow and Activity Catalog v3 sheet Schedules row 13 (P3 rwb-case, queue `rwb-case`, daily cron `0 15 7 * * ?` from the parameter `caselist.allocation.wait.until`, Asia/Bangkok, starts `CaseListDayOpen` with workflow ID `case-list-{businessDate}`, overlap SKIP, catch-up window length Pending GAP-2022 / ASM-3251), sheet Workflows row 24 (`CaseListDayOpen`, scheduled workflow of rwb-case: reads the DP01 freshness answer once, raises MSG-P1-001 to the team manager group when the date is stale, writes no row, publishes no event) and Read me A17 (13 Schedules, including the paused JOB-15, per FD3-runtime-0143); Batch and Scheduling Design v7 sheet Schedule and event map row 26 (job ID Pending NEW-GAP-W5-004). No P1 object is added. It is not the DailyCaseRun fallback Schedule, which stays unconfigured (RD-P1-066 rule 6). Open, not ruled here: the workflow ID `case-list-{businessDate}` does not follow the `<kebab-name>-{businessDate}` form of the RD-P1-022 reuse note (that form gives `case-list-day-open-{businessDate}`); left to the rwb-case owner.
- Amended by RD-P1-097 (batch E), register resolution XE-10: Item 3 and X-27: the account-page read is `GET /accounts` with repeated `accountKey` (1 to 200), answer `AccountPage` {items, missingKeys, freshness DP01}, Case record R, rwb-case workload identity; published in RWB-P1-E1015-CON, built by RWB-P1-E1002-APP (GAP-3274, GAP-3438 closed).

**Final ruling (register).** Items 2, 4, 5, 6 apply. Item 1: no `case_list_row` table, Schedule, case-list operations, publish status or case-list checks in P1; dictionary rows stay in the baseline marked retired. Item 2: rwb-case owns the Schedule `rwb-case-caselist-daily` (daily at `caselist.allocation.wait.until`, 07:15 Asia/Bangkok, overlap SKIP), which starts `CaseListDayOpen` (DP01 freshness read and stale alert, no row written), as entered in Temporal Workflow and Activity Catalog v3 and Batch and Scheduling Design v7; it is not DailyCaseRun's fallback. Item 3: RWB-P1-E1002-APP builds the account-page read; RWB-P1-E1015-CON publishes it (path and keys per call pending, NEW-GAP-B3); RWB-P1-E1002-CON is retired with a pointer; RWB-P1-E1002-OPS is a delta. Reconciliation: child of AceIngestCheck after the ALS stamp, REC-01 waits for rwb-case allocation until `caselist.allocation.wait.until`. Batch E (v3): account-page read is `GET /accounts` (RD-P1-097).

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

- Amended by RD-P1-075 (batch E), register resolution XE-11: The baseline is copied from the Physical Schema **v9** seed (not v8), with its v9 values (DF-REF-074 `varchar(200)`, the corrected DF-ACE types); counts unchanged; the rows PS v9 marks as added by later story migrations are not baseline. `is_personal` follows Data Classification v6 (RD-P1-076).

**Final ruling (register).** As ruled above, amended by batch E (v3): baseline copied from Physical Schema v9; is_personal per DCPI v6 (RD-P1-075, RD-P1-076).

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

- Amended by RD-P1-068 (batch D), register resolution XD-06: Rule 2 gains an act-time snapshot class: a field that records a value as it was at a past act, which ACE cannot answer later, is CARRY with reason "value at act time", with `migration_source` and `migrated_at`: DF-DEC-006 `model_version` (RWB-P1-DM012-APP) and DF-FIN-006 `amount`, DF-FIN-007 `received_date` of the legacy proceeds (RWB-P1-DM013-APP; GAP-2533 directive). Source to Target Mapping v7 sheet Migration packages changes those rows from ACE_READ to CARRY with that reason.
- Amended by RD-P1-068 (batch D): RWB-P1-DM007-APP bullet: DF-LEG-005 `lawsuit_no` is KEY (the linking ACE business key to `v_ace_lawsuit`, DF-ACE-233); ACE_READ covers DF-LEG-006 to DF-LEG-013 (not DF-LEG-005 to DF-LEG-013). The KEY list of rule 2 (b) gains `lawsuit_no`.
- Amended by RD-P1-068 (batch D): RWB-P1-DM002-APP bullet: RWB-P1-DM002-APP migrates nothing (Data Migration Approach v4 lines 132, 173); it is a verification story that reads `GET /customers/{personKey}` (RD-P1-060) and writes no row. The `contact_point_ext` clause (zero or one row per `contact_key`, any number per `person_key`, defaults of an absent row) belongs to RWB-P1-DM005-APP.
- Amended by RD-P1-068 (batch D): orphans and loader. The `plan_ref` (DM004) and `asset_key` (DM006) orphan checks are each DM story's own cutover check, counted in its evidence, reading the keys through rwb-source-data (`GET /accounts/{accountKey}`, `GET /collateral/{assetKey}`); REC-05 scope is unchanged. With SY-DATALOAD retired, each package is loaded by its target service under that service's workload identity and migration owner (RD-P1-021).

**Final ruling (register).** Rule 1 (one mapping, sheet Migration packages) applies. Rule 2: a package carries only Workbench system-of-record fields (CARRY), the linking ACE business keys (KEY: `account_key`, `person_key`, `contact_key`, `valuation_key`, `asset_key`, `plan_ref`, `lawsuit_no`) and act-time snapshot fields (CARRY, reason "value at act time": DF-DEC-006, DF-FIN-006, DF-FIN-007); every other ACE-sourced field is ACE_READ. DM007: CARRY DF-LEG-001 to DF-LEG-004 and DF-LEG-014, KEY DF-LEG-005, ACE_READ DF-LEG-006 to DF-LEG-013. DM002 migrates nothing (verification read of `GET /customers/{personKey}`); the `contact_point_ext` cardinality clause is RWB-P1-DM005-APP's. The `plan_ref` and `asset_key` orphan checks are DM004's and DM006's own cutover checks; each package is loaded by its target service under its workload identity. All other rules apply as ruled above.

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
- Amended by RD-P1-066 (batch D), register resolution XD-02: Item 2 "What starts downstream work": JOB-08 is rwb-integration's, not rwb-payment's (GAP-0657 "Accepted (directive)" supersedes the Arch v5 slide 44 owner row for this job); rwb-payment keeps JOB-07. The consumer list (Affected services) adds rwb-integration (P2). Each consumer service has one consumer group on `rwb.source-data.events.v1` with one listener that starts its runs by signal-with-start (RD-P1-066 rule 2). The ALS-only rule governs daily jobs; rwb-writeoff's monthly GL branch, started on AceDataReady with `sourceSystem` GL, does not breach it (RD-P1-066 rule 4, clarification). DailyCaseRun is event-started by rwb-case's AceDataReady (ALS, COMPLETED) consumer; the slide-14 Schedule is a fallback that is not configured (RD-P1-066 rule 6; GAP-0146).
- Amended by register resolution XD-11 (RD-P1-065 rule 3): Item 1 Closing, "a repeated ready call": after the run has closed, a repeated `POST /business-days/{date}/ready` opens a new AceIngestCheck run (ALLOW_DUPLICATE) only when a due source of the date is still unstamped (run closed at 24 h); the new run stamps only the missing sources. When every due source is stamped it starts nothing and answers 202 with the stored state. No second AceDataReady is published for a stamped source (RD-P1-041), and no second ReconciliationWorkflow starts: it is started only in the workflow task that commits the ALS stamp, and a second run of a date exists only through the rerun of a FAILED run (RD-P1-012).
- Amended by RD-P1-078 (batch E), register resolution XE-01: ID policy: USE_EXISTING + ALLOW_DUPLICATE applies to client starts of AceIngestCheck only; the in-service child starts use a deterministic ID, reuse ALLOW_DUPLICATE_FAILED_ONLY and already-started = started (no conflict policy exists for a child start); starter (b), the 05:30 Schedule, starts `AceLateCheckStart`, which client-starts the per-date run. The reuse note is read the same way.
- Amended by RD-P1-079 (batch E), register resolution XE-12: Register resolution XD-11 is confirmed with its mechanism: attach while open; start nothing when every due source of the date is stamped; otherwise open a new run that stamps only the missing sources. TWAC v3 R18 replaces "DONE or LATE starts nothing". Before wave 4 a FAILED child is restarted by the platform administrator with the Temporal CLI (same ID, ALLOW_DUPLICATE_FAILED_ONLY, startedBy ADMIN).

**Final ruling (register).** Items 1-3 apply with: admin rerun only of FAILED runs; poll intervals in the values file; after the run has closed, a repeated ready call opens a new run only for due sources still unstamped, otherwise it starts nothing (XD-11). Item 2: daily downstream work starts only on ALS/COMPLETED; JOB-07 is rwb-payment's, JOB-08 rwb-integration's (GAP-0657), DailyCaseRun is event-started by rwb-case; one consumer group per consumer service. Item 5: ReconciliationWorkflow is a child of AceIngestCheck after the ALS stamp, waits for rwb-case allocation (poll `recon.allocation.poll.minutes` 5, limit `caselist.allocation.wait.until` 07:15), input `{businessDate, startedBy}`, USE_EXISTING + ALLOW_DUPLICATE. Items 4 and 6 withdrawn; item 7 without the case-list rows. rwb-source-data does not consume its own topic. Batch E (v3): client starts USE_EXISTING + ALLOW_DUPLICATE; child starts per RD-P1-078; Schedule through AceLateCheckStart; XD-11 confirmed (RD-P1-079).

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
- Amended by RD-P1-081 (batch E), register resolution XE-13: Item 4: the `expected_by` STALE trigger applies to DAILY and WEEKLY products only; an ON_CHANGE product (DP03, DP04) is never set STALE by time. Item 7: only the stamp component of RWB-P1-E1015-APP (`FreshnessStampWriter`) writes `data_product_load`; `stampProducts` calls it for DAILY and WEEKLY products with mapped sources, and `stampDp04` of Stage2ProductWorkflow is the only caller for DP04. GAP lines: "Closes GAP-0511 (DP04: STALE at expected_by 08:00, no 07:00 stale)" reads "GAP-0511 closed by RD-P1-068: DP04 is ON_CHANGE and never STALE by time".
- Amended by RD-P1-083 (batch E), register resolution XE-14: Item 3: a STALE row of (P, D) whose sources complete again is updated in place (LOADED, `stale_flagged_at` null, new times, `duplicate_count` + 1), no second AceDataReady. AceDataLate `status` is null when the source has no batch row. Item 6: a restatement is detected only while the run is open, on the latest `completed_at`. Weekly-only sources are due in the run whose start day is the cycle weekday.

**Final ruling (register).** Items 1, 2, 4-8 apply; item 3 times: `source_extracted_at` = latest source `completed_at`, `loaded_at` = write instant. ASM-0684 changed. Batch E (v3): STALE by time for DAILY/WEEKLY only; DP04 stamped only by stampDp04 through the one stamp component (RD-P1-081); in-place re-completion, nullable AceDataLate status, weekly-only source run (RD-P1-083).

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
- Amended by RD-P1-093 (batch E), register resolution XE-15: Clean day: every REC-01, REC-02 and REC-05 row of the date PASS (REC-05 is an aggregate row, RD-P1-086); a bank business date with a BREAK or with no row resets the count to zero; non-business days are skipped; counting starts after the last owner's ACCEPTED acceptance.

**Final ruling (register).** Items 1, 4, 5 apply; a BREAK raises MSG-P1-012 and the alert, no publish status; NOT_RUN does not exist; a run that cannot proceed (gate HOLD, allocation contract unreadable, parameter unreadable) writes no row. Batch E (v3): clean day includes the REC-05 row; a date with no row resets (RD-P1-093).

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
- Amended by RD-P1-080 (batch E), register resolution XE-16: Item 3(a): while the flag is off the ready call answers 202 and records the readiness row but starts no AceIngestCheck; status answers LATE; freshness answers 200 STALE with null date and never 404. AceIngestCheck keeps its own flag guard.

**Final ruling (register).** Items 1, 4, 5 apply; with the Section B flag off AceIngestCheck writes no stamp, publishes nothing, starts no child, status LATE, freshness STALE with null date. Batch E (v3): ready call starts no run while the flag is off; freshness never 404 (RD-P1-080).

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
- Amended by RD-P1-080 (batch E), register resolution XE-16: Item 4: on a first-release rollback the readiness and freshness operations answer as RD-P1-043 item 3 (never 404); every other flagged operation without a ruled flag-off answer answers 404 MSG-P4-003. The ledger-writer flag gates the REST append only.

**Final ruling (register).** Items 1-5 apply; item 6 ends: a FAILED P1 run is re-run after the fix through `POST /admin/jobs/{jobId}/rerun`. Batch E (v3): first-release rollback: freshness and readiness as RD-P1-043, other flagged operations 404 MSG-P4-003 (RD-P1-080).

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
- Amended by RD-P1-092 (batch E), register resolution XE-08: Item 1: `GET /retention-runs/{runId}` reads table `retention_run`; the listed REVIEW keys are rows of `retention_review_item`, read by Compliance through `GET /retention-runs/{runId}/review-items` (Platform administration R).

**Final ruling (register).** Items 2-4 apply. Item 1: `POST /retention-runs`, UUID Idempotency-Key, body `{ruleVersion, runDate, rules[]}`, 202 `{runId, status: ACCEPTED}`, 409 MSG-P2-006 (run of the date running or complete), 409 MSG-PLT-N009-05 (key reuse), 422 MSG-GEN-002 / MSG-P1-002 (rules refused); workflow `RetentionRunWorkflow`, ID `retention-run-{runDate}`, FAIL + ALLOW_DUPLICATE_FAILED_ONLY. Batch E (v3): run record table and review-items read (RD-P1-092).

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
- Amended by RD-P1-092 (batch E), register resolution XE-17: Item 2: accepted `ageBasis` values are `case.closedAt` (interaction, dp_treatment, dp_guarantee_claim), `account.lastClosedAt` (account_ext) and `person.lastClosedAt` (party_ext, contact_point_ext); valuation_ext selects nothing until GAP-3279; the REVIEW tables accept `recordClass` ALL only. Archive: path and manifest per GAP-0490; container and role pending NEW-GAP-E2; no delete without a write-once container.

**Final ruling (register).** Items 2, 4-6 apply with seven tables in scope (ARCHIVE: interaction; REVIEW: party_ext, account_ext, contact_point_ext, valuation_ext, dp_treatment, dp_guarantee_claim); `case_list_row` excluded as not created; periods pending GAP-1029. Batch E (v3): age bases and record classes per table; archive container pending NEW-GAP-E2 (RD-P1-092).

**Values chosen without a source.** Interim periods as data from RRA v4 proposals (pending DL26)

---

## RD-P1-060 · Entity reads of rwb-source-data: customer, account and collateral; recipient name and postal address

_Original text of batch D kept for audit. Amendments and the final ruling follow it._

**Question.** No published operation gives rwb-comms, rwb-integration or gateway-bff the recipient name and postal address (items 23, 51, 59, 61), nor gives RWB-P3-E2006-APP the account and collateral (item 16), rwb-payment the account fee facts (E4045), or rwb-deviation the party flags that AceDataReady no longer carries (item 10). YAML says DP02 contact rows carry no value, name or address; RWB-P1-E1016-APP v3 AC returns `contact_value` clear to an unmasked role; `GET /customers/{id}` is cited by eight stories and published nowhere.

**Options considered.** (1) Widen `GET /data-products/DP02/records` to answer clear values. (2) Publish the three per-entity reads Architecture v5 names and keep the records read masked. (3) Leave Pending. Option 2 chosen: it is what Arch v5 states, and it keeps one read path per consumer need.

**Sources.** Arch v5 lines 736, 776 (case screen: gateway-bff calls rwb-source-data `GET /v1/customers/{id}` and `/v1/accounts/{id}`, "masked by policy"), 1075 and 1114 (P1 card: `GET /customers/{id}, /accounts/{id} · GET /collateral/{id}, /payments?accountId=`), 2884. PCMD v4 sheet Read paths R4 (gateway-bff, masked values only), R7 (rwb-deviation, deceased and bankruptcy flags, `GET /customers/{id}`), R8 (rwb-comms contact points for notices: GAP-0244, ASM-0334), R9 (`/accounts/{id}` with `v_ace_ca_relation`); PCMD v4 field rows R13-R22 ("Served by GET /api/recovery/source-data/v1/customers/{id}"); PCMD v3 line 74 (`contact_value` "in full, for notices and calls; contact_value_masked for display. Every read is audited"). DCPI v5 R1073 (DF-ACE-057 first_name) and R1094 (DF-ACE-078 contact_value): "Masked unless the role may see it", basis "legal obligation for statutory notices". PS v9 `recovery_views.sql` lines 191-260 (`v_ace_customer`, `v_ace_contact` columns). YAML lines 338-395 (records read, DP02 contact rule), 1764-1795 (`PartyExtFacts`, `AccountExtFacts`), 18 (GAP-3274). RWB-P1-E1016-APP v3 AC (line 282, FieldMasker unmasks `contact_value`), line 411 (`FieldMasker` of RWB-P4-E1037-CON), line 713 (out of scope: `/customers/{id}`, `/accounts/{id}`, `/collateral/{id}`, NEW-GAP-S4b-4). RWB-P1-DM002-APP v3 lines 299, 485 (the operation belongs to RWB-P1-E1069-APP; GAP-0566). RWB-PLT-N001-CON v3 lines 32, 267, 282 (composite route, NEW-GAP-F08-4).

**Precedence applied.** Arch v5 (top) fixes the three operations and the masking-by-policy rule. RD-P1-005 (wire names camelCase) and RD-P1-004 (Problem) apply. The YAML DP02 rule is kept; the E1016-APP AC that contradicts it moves to the new read.

**Ruling.**
1. **Operations added to `rwb-source-data.yaml` 5.1.0** (the staged, unreleased version of this run; `x-service.operations` 29 → 32; owner `P1`; builder **RWB-P1-E1069-APP**; contract fake `fakes/rwb-source-data/5.1.0/` gets examples per RD-P1-011):
   - `GET /customers/{personKey}` – operationId `getCustomer`; x-capability Case record R. `personKey` = ACE `person_key` (string, maxLength 255). Answer `Customer`: the `v_ace_customer` Section A columns in camelCase – `personKey`, `cifNo`, `firstName`, `lastName`, `dateOfBirth`, `deceasedDate`, `deceasedFlag`, `gender`, `nationality`, `maritalStatus`, `occupation`, `customerStatus`, `category`, `countryOfResidence`, `isStaff`, `branchCode`, `idNoMasked`, `idNoLast4` (`spouseName` and `vatNumber` likewise, personal); the Section B columns (`partyType`, `idType`, `segment`) are added when RWB-ACE-001 deploys, behind the DL43 flag (RD-P1-043); `partyFacts` = the four `PartyExtFacts` booleans of `party_ext` (`vulnerable`, `deceasedOverride`, `bankruptcy`, `fraudFlag`), null when the person has no `party_ext` row; `contacts[]` = the `v_ace_contact` rows of the person: `contactKey`, `contactType` (PHONE, EMAIL, ADDRESS), `usageCode`, `contactValue`, `contactValueMasked`, `city`, `postCode`, `country`, with `consentStatus` and `verifiedAt` of `contact_point_ext` as in `ContactPointRow`; `freshness` = `DataProductFreshness` of DP02. No freshness refusal: the answer carries the DP02 record and the caller applies its own stale rule.
   - `GET /accounts/{accountKey}` – operationId `getAccount`; Case record R. Answer `Account`: the `v_ace_account` Section A columns in camelCase, `relations[]` from `v_ace_ca_relation` (PCMD v4 R9), `accountFacts` = the `AccountExtFacts` of `account_ext` (null when no row), `freshness` = DP01. The multi-key account-page read for the case list stays Pending under GAP-3274; this is the single-account form GAP-3274 names.
   - `GET /collateral/{assetKey}` – operationId `getCollateral`; Case record R. Answer `Collateral`: the `v_ace_collateral` rows of the asset key in camelCase, plus the `v_ace_collateral_detail` columns once Section B is live (DL43 flag), `freshness` = DP06.
   - Errors (RD-P1-004): 400 MSG-GEN-001; 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003 for a key with no row or outside scope; 503 MSG-GEN-006. GET only: no Idempotency-Key. Every read is written to the access log (YAML records rule; PCMD v3 line 74).
2. **Masking.** Every field tagged `is_personal` passes through `FieldMasker.mask(dto, session)` of RWB-P4-E1037-CON for the caller's user session or workload identity; a field with no rule is masked (E1016-APP line 411). `contactValue` is answered clear only when `isUnmasked(contactValue, session)` is true; otherwise it carries the `contact_value_masked` value. The same holds for `firstName`, `lastName` and the address columns.
3. **Recipient name and postal address (item 61).** The clear name and postal address (`firstName`, `lastName`, and the ADDRESS row's `contactValue`, `city`, `postCode`, `country`, chosen by `contactKey`) are read only through `GET /customers/{personKey}`, by the rwb-comms notice workload identity (RWB-P6-E1007-APP, RWB-P6-E1032-APP, RWB-P6-E1052-APP/CON) and the rwb-integration outbound-file workload identity (RWB-P2-E1007-APP/CON, INT-14 WIN file). The masking rule rows that unmask those fields for those two identities are **Pending, owner data protection officer with the rwb-access (P4) owner**, tracked as NEW-GAP-D1 (narrows GAP-0244 / ASM-0334). **Interim build:** the FieldMasker fake carries rules unmasking `firstName`, `lastName` and `contactValue` for those two identities only; gateway-bff and every user role get masked values (PCMD v4 R4); tests assert both branches.
4. **DP02 records read keeps its rule.** `GET /data-products/DP02/records` answers contact rows with `contactKey`, `contactType`, `consentStatus`, `verifiedAt` only (YAML line 381). RWB-P1-E1016-APP's scenario "contact_value is returned clear with masked false" is re-targeted to `GET /customers/{personKey}`.
5. **Party flags (item 10).** AceDataReady carries the four fields of RD-P1-003 only. rwb-deviation reads `deceasedFlag`, `deceasedDate` and `partyFacts.deceasedOverride` / `partyFacts.bankruptcy` through `GET /customers/{personKey}` (PCMD v4 R7), one hop, 2 s; RWB-ITG-E7003-ITG and RWB-S8-E1020-APP (the one S8 story in Story Files v2 that takes the flags off AceDataReady) align.
6. **Callers named in the YAML `description` of each operation:** `getCustomer` – gateway-bff (case screen composite, RWB-PLT-N001-CON; closes NEW-GAP-F08-4), rwb-comms, rwb-integration, rwb-deviation, rwb-case (portal offer view facts through gateway-bff, item 59; RWB-P6-E4036-APP/CON), RWB-P1-DM002-APP verification; `getAccount` – gateway-bff, rwb-case, rwb-payment (RWB-P8-E4045-APP fee facts `collections_fee` DF-ACE-024), RWB-P3-E2006-APP; `getCollateral` – RWB-P3-E2006-APP, rwb-asset.

**Rationale.** Arch v5 already names the operations and their masking; publishing them removes the largest single cross-cutting blocker (five services) without widening the records read, and keeps the clear name and address behind one audited, rule-driven read.

**Affected services.** rwb-source-data (provider); gateway-bff, rwb-comms, rwb-integration, rwb-deviation, rwb-case, rwb-payment, rwb-asset, rwb-access (masking rules).

**Affected stories.** RWB-P1-E1069-APP (builds the three operations), RWB-P1-E1016-APP (AC re-target, out-of-scope line), RWB-P1-E1016-CON, RWB-P1-DM002-APP, RWB-P6-E1007-APP, RWB-P6-E1032-APP, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-ITG-E1052-ITG, RWB-P2-E1007-APP, RWB-P2-E1007-CON, RWB-ITG-E1007-ITG, RWB-ITG-E1065-ITG, RWB-PLT-N001-CON, RWB-P3-E2006-APP, RWB-P3-E2014-APP, RWB-P7-E2014-APP, RWB-P8-E4045-APP, RWB-ITG-E7003-ITG, RWB-S8-E1020-APP, RWB-P6-E4036-APP, RWB-P6-E4036-CON, RWB-P10-E8003-APP.

**Affected documents.** API Specification v7 `rwb-source-data.yaml` (three paths, schemas `Customer`, `Account`, `Collateral`, operation count, records description unchanged) and `index.yaml` count; Service Contract Catalog v3 (.md and .xlsx: three rows); Party and Customer Master Data Design (next version: Read paths R8 → `GET /customers/{personKey}`); Users Roles and Permissions v6 / Role to System Access Matrix v4 (masking rows Pending, NEW-GAP-D1); Gap Register v3 (GAP-0566, GAP-0549 closed; GAP-0244 narrowed; NEW-GAP-D1).

**Escalation items settled.** 10, 16, 23, 51 (first part), 59 (customer facts), 61; S8 extra story; ACE boundary of E4045 (account part). Temp gaps closed: NEW-GAP-F13-1, NEW-GAP-F02-1, NEW-GAP-F08-4, NEW-GAP-F15-4 (read published; masking rows remain as NEW-GAP-D1), NEW-GAP-S4b-4.

**GAP/ASM.** Closes GAP-0566 and GAP-0549 (response schemas); narrows GAP-0244 / ASM-0334 to NEW-GAP-D1; GAP-3274 unchanged (page form).

**Status.** Proposed – Claude Opus 5.5 (applied). Paths, callers and masking-by-policy are sourced (Arch v5, PCMD, DCPI); the path parameter names, operationIds, answer grouping (`partyFacts`, `contacts`, `relations`, `accountFacts`) and the null-when-no-row rule are Claude Opus 5.5 choices.

**Reuse note.** Any service that needs ACE party, contact, account or collateral facts of one key calls these three reads; it never asks for clear personal values elsewhere, and it never reads the DP02 records read for a contact value.

**Values chosen without a source.** operationIds `getCustomer`, `getAccount`, `getCollateral`; path parameter names `personKey`, `accountKey`, `assetKey`; group names `partyFacts`, `contacts`, `relations`, `accountFacts`; `partyFacts` / `accountFacts` null when no extension row.

#### Register amendments

- Amended by RD-P1-076 (batch E), register resolution XE-18: Rule 2: the mask-by-default rule applies to fields of DCPI v6 classification Restricted; a personal field of classification Confidential or Internal is returned within the caller's scope unless a masking rule masks it (confirmation NEW-GAP-E5). `is_personal` mirrors DCPI v6.
- Amended by RD-P1-077 (batch E), register resolution XE-19: Rule 3: the PHONE and EMAIL `contactValue` are also unmasked, for the rwb-comms notice workload identity only (SMS, LINE); GAP-3283 widened.

**Final ruling (register).** As ruled above, amended by batch E (v3): mask by default only Restricted fields (RD-P1-076); PHONE and EMAIL clear for the rwb-comms notice identity (RD-P1-077).

---

## RD-P1-061 · `GET /payments`: one operation, two query forms, one builder

_Original text of batch D kept for audit. Amendments and the final ruling follow it._

**Question (item 4).** `/payments` is used by RWB-P1-E2008-APP (`businessDate`) and RWB-P1-E1013-APP (`accountId`) with different query parameters; YAML publishes only the date form and records NEW-GAP-S10-14.

**Sources.** Arch v5 lines 1075, 1114 (`/payments?accountId=`); YAML lines 1129-1163 (`getPayments`, businessDate, PaymentsAnswer, NEW-GAP-S10-14, GAP-0601); register RD-P1-022 final ("readiness pair, `business_day_readiness`, `GET /payments`, `snapshot(page)` – RWB-P1-E1013-APP / RWB-P1-E1015-CON"); `/accounts/{accountKey}/installment-facts` (YAML line 1164) for the wire name of the ACE account key.

**Precedence applied.** Arch v5 fixes one path with an account query; RD-P1-022 fixes the builder; RD-P1-005 fixes the wire name (`accountKey`, the ACE key name used across YAML 5.1.0; Arch v5 `accountId` is the same key).

**Ruling.**
1. One operation `GET /payments` (operationId `getPayments`), builder **RWB-P1-E1013-APP** (RD-P1-022, not amended); contract published in RWB-P1-E1015-CON.
2. Query: exactly one of `businessDate` (date) or `accountKey` (string, maxLength 255). Both or neither → 400 MSG-GEN-001 with `field`.
3. `businessDate` form: unchanged from YAML 5.1.0 (one row per `paymentCode` from `v_ace_payment` for the date, ordered by `paymentCode`, `batchStatus` and `productStatus`, 409 MSG-P1-001). Its rules are those written in RWB-P1-E2008-APP, which keeps them as the acceptance criteria of that form and gains an H dependency on RWB-P1-E1013-APP; RWB-P1-E2008-APP keeps building `GET /accounts/{accountKey}/installment-facts`.
4. `accountKey` form: the `v_ace_payment` rows of the account, ordered by `paymentDate` then `paymentCode`, in the same `PaymentsAnswer` shape with `businessDate` = the DP01 stamp in use; same 409 rule.
5. Paging and row cap stay Pending (GAP-0601, NEW-GAP-S10-04, owner data architect); interim unpaged for both forms.
6. Callers: rwb-payment JOB-07 (RWB-P8-E2008-APP), RWB-P8-E4044-APP, RWB-P8-E4045-APP, RWB-P8-E4050-APP (date form); E1013 baseline measures and gateway-bff (account form). YAML `description` names both stories and the builder.

**Affected services.** rwb-source-data; rwb-payment; gateway-bff.
**Affected stories.** RWB-P1-E1013-APP, RWB-P1-E2008-APP, RWB-P1-E1015-CON, RWB-P8-E2008-APP, RWB-P8-E2008-CON, RWB-P8-E4044-APP, RWB-P8-E4045-APP, RWB-P8-E4050-APP, RWB-ITG-E2008-ITG.
**Affected documents.** `rwb-source-data.yaml` (parameter, oneOf rule, description); Service Contract Catalog v3 (row of `getPayments`); Gap Register v3 (NEW-GAP-S10-14 closed).
**Escalation items settled.** 4. **GAP/ASM.** Closes NEW-GAP-S10-14; GAP-0601 unchanged.
**Status.** Proposed – Claude Opus 5.5 (applied). **Reuse note.** One path, one handler, one builder per resource: a second caller adds a query form to the owner's operation, never a second operation.
**Values chosen without a source.** Exactly-one rule; account-form ordering.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-062 · Never-stamped data product: what every reader shows and does; freshness fixtures

_Original text of batch D kept for audit. Amendments and the final ruling follow it._

**Question (items 17, 22, 62 first part, 18).** RD-P1-041 makes a never-stamped product `businessDate` null and `status` STALE. Stories ask what the data-date header, stale banner, input age, `data_as_of`, MSG-P1-001 `{date}`, notice generation and "last complete day" do then; and fixtures in five stories use dates that do not match the RD-P1-041 expected business date.

**Sources.** Register RD-P1-041 final (never stamped = businessDate null, STALE; expected date = latest bank business day before T); RD-P1-010 final (`AceBatchNotComplete` with `lastCompleteBusinessDate` null when none); YAML `DataProductFreshness` (lines 2174-2206: "null only for a never-stamped product or while the Section B flag is off", `staleSince` "null when LOADED"); EMS v5 MSG-P1-001 "{product} is from {date}. Today's load has not arrived."; RWB-P6-E1052-APP X6 and X12 (STALE with a date: generation proceeds with that date shown); RWB-P3-E2011-APP BR12 (header omitted when the answer is absent); BSD v7 JOB-02 ("No cases from a stale business date").

**Precedence applied.** RD-P1-041 (register) fixes the answer; this decision only fixes reader behaviour and does not amend it.

**Ruling.**
1. **Answer.** `businessDate` null, `status` STALE, `staleSince` null, `sourceExtractedAt` and `loadedAt` absent.
2. **Gated reads refuse.** Every gated operation and activity (`listEligibleAccounts`, `GET /efs-history`, `/booking-facts`, `/payments`, `/accounts/{accountKey}/installment-facts`, DailyCompletenessGate) refuses with 409 MSG-P1-001 (activity: non-retryable `AceBatchNotComplete`, `lastCompleteBusinessDate` null).
3. **No date, fail closed.** A reader that needs a data date treats a never-stamped product as having none: the `X-Data-As-Of` header is omitted (as for an absent answer, E2011 BR12); the stale banner shows (status STALE); `data_as_of` on a decision record, notice or report row is null; an input age is not computed (null) and every age check that uses it fails as too old.
4. **Notices (items 22, 62).** A notice whose merged products include a never-stamped product is **held** (not generated), with MSG-P1-001, and is retried in the next window after AceDataReady (the RWB-P2-E1007-APP X1 mechanism). This is the fail-closed reading of point 3; the product owner confirms it under NEW-GAP-F13-5 (kept as a confirmation, not a build blocker). A STALE product that has a `businessDate` keeps the existing rule (proceed with the date shown).
5. **"Last complete day" (RWB-P9-E2009-APP).** The `businessDate` of the stamp in use; for a never-stamped product there is none: the data set excludes the product and shows no data date for it.
6. **MSG-P1-001 `{date}`.** EMS v5 has no wording for a product with no stamp: **Pending, owner Error and Message Standard owner (UX content lead)**, NEW-GAP-D2. Interim build: Problem `messageCode` MSG-P1-001 with `{product}` filled and `{date}` left empty; tests assert the code and the product only.
7. **Fixtures (item 18).** Every freshness fixture uses the RD-P1-041 expected date: for a test day T, the expected date D is the latest bank business day before T on the sandbox calendar. Each consumer fake serves three rows: LOADED for D; STALE with `businessDate` = the business day before D and `staleSince` = D; never stamped (`businessDate` null). RWB-P3-E2011-APP, RWB-P3-E2011-CON, RWB-P3-E2014-APP, RWB-P7-E2014-APP and RWB-P7-E2014-CON change their dates accordingly.

**Affected services.** All freshness readers: rwb-case, rwb-comms, rwb-decision, rwb-reporting, rwb-agent, rwb-access, gateway-bff.
**Affected stories.** RWB-P1-DM001-APP, RWB-P1-DM002-APP, RWB-P3-E2011-APP, RWB-P3-E2011-CON, RWB-P3-E2014-APP, RWB-P7-E2014-APP, RWB-P7-E2014-CON, RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P6-E1007-APP, RWB-P6-E1011-APP, RWB-P6-E1032-APP, RWB-P10-E1059-APP, RWB-P10-E1059-CON, RWB-P4-E8018-APP, RWB-P9-E2009-APP.
**Affected documents.** Error and Message Standard (next version: wording Pending, NEW-GAP-D2); Gap Register v3 (NEW-GAP-L03-1, NEW-GAP-L04-01, NEW-GAP-L04-02, NEW-GAP-L04-03, NEW-GAP-S12-1, NEW-GAP-F13-2 closed; NEW-GAP-F13-5 kept as confirmation; NEW-GAP-D2 new).
**Escalation items settled.** 17, 18, 22, 62 (first part).
**Status.** Proposed – Claude Opus 5.5 (applied). **Reuse note.** A product without a stamp is treated as having no data date: refuse gated reads, omit the date, fail age checks, hold dependent outbound work.
**Values chosen without a source.** Fail-closed reading; notice held; three-row fixture.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-063 · Contract operations reported missing: verified state and the remaining additions

_Original text of batch D kept for audit. Amendments and the final ruling follow it._

**Question (items 25, 29, 34, 46, 47, 49, 51 gateway codes, 54).** Editors report operations missing from published contracts.

**Sources (verified).** YAML 5.1.0 `paths` (lines 295-1376) holds `GET /proof-of-delivery`, `GET /admin/reconciliation/results` and `/{resultId}`, `GET /booking-facts`, `GET /batch-status`, `GET /payments`, `GET /accounts/{accountKey}/installment-facts`, `PUT /extension-facts/parties/{personKey}`, `PUT /extension-facts/accounts/{accountKey}`; freshness query parameter is `product` (line 307). Staged `asyncapi/rwb-source-data.asyncapi.yaml` is 5.1.0 with key "sourceSystem:businessDate (no case)" (lines 10, 24, 159). Staged `asyncapi/rwb.decision-record.v1.asyncapi.yaml` names `rwb.decision.DecisionRecorded.v1` (lines 51, 98). Staged `rwb-case.yaml` 5.1.0 has `/admin/parameters` and no `/parameters/{key}`; register RD-P1-028 (P1 reads parameters only through RWB-P3-E1042-CON `GET /api/recovery/case/v1/parameters/{key}`); Parameter Catalog v1.csv header (14 columns). Staged `rwb-access.yaml` 5.1.0 has no `/authorise`; Service Contract Catalog v3 rows at lines 225, 609, 681 (`POST /authorise (role, scope, DoA), cached in rwb-case`, `/api/recovery/access/v1`, Arch v5 slides 13-14). Staged `rwb-partner.yaml` and `rwb-writeoff.yaml` path lists. Register RD-P1-010 (region_code belongs to rwb-case), RD-P1-001, RD-P1-004.

**Ruling.**
1. **Already published (items 25, 29, P1 half of 46, 34; DecisionRecorded check).** No story drops those operations; stories cite them by path and operationId from YAML 5.1.0. The asyncapi files already carry RD-P1-003 and RD-P1-008. Editors who saw them missing worked on an earlier copy.
2. **Freshness query name (item 46).** The query parameter is `product`; RWB-P1-E1015-CON v3 text that says `productCode` for the query is corrected. `productCode` stays the path parameter of the records read and the answer field.
3. **`rwb-case.yaml`: add `GET /parameters/{key}`** (operationId `getParameter`, owner P3, builder RWB-P3-E1042-CON, RD-P1-028). Answer: the catalog row (the 14 columns of `config/parameter-catalog.csv`) and the value in force from `parameter_value` with the column names RWB-P3-E1042-CON uses. Service workload identities only. A parameter with `secret` true answers 404 MSG-P4-003. 401, 403, 503 per RD-P1-004. This closes NEW-GAP-F11-8.
4. **`recon.tolerance.pct` `used_by` (item 46).** Not extended: only the P1 reconciliation uses it, because RD-P1-069 rule 6 removes the duplicate open-case check from RWB-P3-E1011-APP; rwb-case reads reconciliation results from `GET /admin/reconciliation/results`.
5. **`rwb-access.yaml`: add `POST /authorise`** (Service Contract Catalog v3 rows 225, 609, 681; owner P4, builder RWB-P4-E1016-APP). Request and answer fields are **Pending, owner rwb-access contract owner**, NEW-GAP-F09-3 kept. Interim build for the callers (RWB-P1-E1016-APP, -CON, -DB): they send `Idempotency-Key` (UUID per call; the platform filter RWB-PLT-N009 applies to every POST), they assert only allow or deny and the Problem `messageCode` (401 MSG-P4-001, 403 MSG-P4-002, 404 MSG-P4-003), never role or scope values the provider has not published, and they test against the P4 fake.
6. **Other contracts outside P1 (item 49).** Staff read of an instruction in `rwb-partner.yaml` and read of a write-off decision in `rwb-writeoff.yaml`: Pending, owners S9 and S7 contract owners (NEW-GAP-F07-02). Whether `identity_ref` holds a person key: Pending, owner data architect (NEW-GAP-F07-01).
7. **gateway-bff codes (item 51).** RD-P1-004 applies to gateway-bff: a downstream Problem is passed through unchanged (status, `messageCode`, `traceId`); the gateway's own errors use the same envelope; the code of the edge 500 stays Pending (NEW-GAP-F08-2, owner platform edge owner).
8. **Case region and branch (item 47).** `region_code` belongs to rwb-case (RD-P1-010). The source of `branch_code` on the case record is **Pending, owner rwb-case owner with the data architect**, NEW-GAP-F11-6 kept; interim: rwb-case stores the `branchCode` of `GET /accounts/{accountKey}` (RD-P1-060) when the account view carries one, else null.
9. **Service Contract Catalog section 6.1** is aligned to Service Catalog v2 (finishing-pass item).

**Affected services.** rwb-case, rwb-access, gateway-bff, rwb-partner, rwb-writeoff, rwb-source-data.
**Affected stories.** RWB-P1-E1015-CON, RWB-P3-E1042-CON, RWB-P3-E1011-APP, RWB-P4-E1016-APP, RWB-P1-E1016-APP, RWB-P1-E1016-CON, RWB-P1-E1016-DB, RWB-PLT-N001-CON, RWB-P1-E2007-APP, RWB-P1-E2008-APP, RWB-ITG-E2007-ITG, RWB-ITG-E2008-ITG, RWB-ITG-E1055-ITG, RWB-ITG-E1011-ITG.
**Affected documents.** `rwb-case.yaml` (`/parameters/{key}`), `rwb-access.yaml` (`/authorise`), `index.yaml` counts; Service Contract Catalog v3 (.md/.xlsx; section 6.1); Parameter Catalog v1.csv (no change to `used_by`); Gap Register v3 (NEW-GAP-F11-8 closed; NEW-GAP-F09-3, NEW-GAP-F07-01, NEW-GAP-F07-02, NEW-GAP-F08-2, NEW-GAP-F11-6 kept).
**Escalation items settled.** 25, 29, 34, 46, 47, 49, 51 (second part), 54; checks "DecisionRecorded event type" and "Service Contract Catalog 6.1".
**Status.** Proposed – Claude Opus 5.5 (applied). **Reuse note.** Before reporting an operation as missing, read the staged YAML `paths`; a caller of an unpublished shape asserts only the envelope and the code.
**Values chosen without a source.** operationId `getParameter`; secret parameter answers 404; interim `branchCode` source.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-064 · Interaction ledger callers: letter dispatch and delivery entries, hand-recorded proof, permissions and entry types

_Original text of batch D kept for audit. Amendments and the final ruling follow it._

**Question (items 1, 26, 32, 37, 39, 40, 41, 50, 59 failed append, 60, 62 second part, 63; extra stories).** RD-P1-007 rule 7 sets `externalRef` = `pod_key`, but the dispatch entry carries the WIN barcode, so proof and letter never pair; `podKey` is 255 characters against `externalRef` 60 and `idempotencyKey` 120; the dispatch append needs `conductCheck`; no permission lets rwb-comms append; rwb-partner's route conflicts with ASM-5391; complaints, customer answers and notice entries have no settled form.

**Sources.** Register RD-P1-007 (rules 1-8 and final), RD-P1-009 (consumed map has no partner type), RD-P1-001. YAML `InteractionRequest` (lines 1986-2064: eventCode enum without COMPLAINT; `actorType` USER, SERVICE, PARTNER; `channel` enum incl. LETTER, PORTAL; `conductCheck` PASSED, BLOCKED, NOT_APPLICABLE; `externalRef` maxLength 60; LETTER rule "conductCheck is required when deliveryStatus is SENT or absent; externalRef is required when deliveryStatus is present"); `Interaction.latestDeliveryStatus` (derived per `externalRef`); `ProofOfDeliveryRow` (`podKey` 255, `noticeRef` 60, `barcode` 40, `callbackDate`, `deliveryStatus` 15). PS v9 `v_ace_pod` (lines 615-631). AR v3 ASM-5391. EMS v5 MSG-P1-022. RWB-P2-E1007-APP (INT-14 WIN notice file).

**Precedence applied.** RD-P1-007 stands; rule 7 is amended for the reference and key only, because the published schema lengths (YAML, same run) make `pod_key` unusable as `externalRef` and the derivation of `latestDeliveryStatus` needs the dispatch and delivery entries to share a reference. **Amends RD-P1-007 rule 7** and **changes ASM-5391**.

**Ruling.**
1. **Callers.** In-process: RWB-P1-E1067-APP, RWB-P1-E2034-APP (RD-P1-007 final). REST, each under its own workload identity: rwb-case, rwb-comms, rwb-integration, rwb-document, rwb-payment, rwb-treatment, rwb-partner.
2. **Permission (item 40).** Users Roles and Permissions v6 and Role to System Access Matrix v4 add, for each REST caller of rule 1 that lacks it, a service-identity row "Case record C on rwb-source-data" (the x-capability of `POST /cases/{caseId}/interactions`). rwb-comms is the first row (NEW-GAP-F10-01 closed).
3. **Dispatch entry (rwb-comms, when the WIN file is sent; items 1, 63).** `eventCode` LETTER, `channel` LETTER, `direction` OUTBOUND, `deliveryStatus` SENT, `externalRef` = the WIN `barcode` of the notice, `conductCheck` PASSED (a letter is dispatched only after the conduct check passed), `actorType` SERVICE, `actorRef` `rwb-comms`, `sourceRef` `INT-14 WIN`, `idempotencyKey` `LETTER-<caseNo>-<yyyyMMdd of sent date>-<noticeId>`. A letter refused by the conduct check appends `conductCheck` BLOCKED with no `deliveryStatus` and no `externalRef`.
4. **Delivery entry (rwb-comms, after `GET /proof-of-delivery`; amends rule 7).** One entry per matched row: `eventCode` LETTER, `deliveryStatus` from the row, `externalRef` = `barcode`, else `noticeRef` when `barcode` is null; a row with neither is not matched (no entry; rwb-comms logs the row as unmatched). `occurredAt` = `callbackDate` at 00:00 Asia/Bangkok. `idempotencyKey` `LETTER-<caseNo>-<yyyyMMdd of callbackDate>-<u>` where `<u>` is the UUID version 5 of `podKey` in the RFC 9562 URL namespace (36 characters, so the key stays within 120 and stays the same on every re-read). The mapping of WIN `delivery_status` values to SENT, DELIVERED, READ, FAILED is **Pending, owner rwb-comms owner with the WIN interface owner**, NEW-GAP-D3; interim: the values of the RWB-P6-E1055-APP fixture.
5. **Hand-recorded proof (items 37, 60).** Yes, it writes an entry, through rwb-comms only: `eventCode` LETTER, `actorType` USER, `actorRef` the user ID, `deliveryStatus` as recorded, `externalRef` = the notice's barcode, `idempotencyKey` `LETTER-<caseNo>-<yyyyMMdd>-<id of the rwb-comms record of the hand entry>`. `<caseNo>` is read from rwb-case `GET /cases/{caseId}` (one hop) – the case number source of item 60.
6. **Single appender of delivery entries (items 32, 39).** rwb-comms only (RD-P1-007 final). RWB-P1-E2021-APP and RWB-P3-E2021-APP write no delivery entry. `GET /proof-of-delivery` stays readable by the rwb-comms workload identity only; rwb-asset (RWB-S5-E3022-APP/CON) reads delivery state from `GET /cases/{caseId}/interactions` (`latestDeliveryStatus` of the LETTER entry) or from rwb-comms `GET /notices/{noticeId}`, and RWB-P1-E1055-APP keeps rwb-comms as its one caller.
7. **EFS history appender (item 26).** The P2 rwb-integration hand-over run (RD-P1-007 rule 8; RD-P1-067). RWB-P3-E2001-APP removes its append step.
8. **Promise rows (item 32).** PROMISE when the entry records a promise to pay (EFS `isPtp`, or a Workbench contact with `promiseAmount` and `promiseDate`); CONTACT otherwise.
9. **rwb-partner (item 50).** Appends partner results over REST: `eventCode` PARTNER_RESULT, `actorType` PARTNER, `actorRef` the partner code, business key per RD-P1-007 rule 4. ASM-5391 is changed from "through the published event" to this REST append (RD-P1-009 has no partner event in its map). NEW-GAP-F08-1 closed.
10. **Customer answers (item 60).** Appended by the receiving service: `eventCode` CONTACT, `direction` INBOUND, `channel` PORTAL for an answer given on HOME.SCB, `actorType` SERVICE, `actorRef` the receiving service (`rwb-comms`); on events `ce_actor` = `SERVICE:rwb-comms`. There is no customer actor type. That HOME.SCB maps to PORTAL is **Pending confirmation, owner product owner**, NEW-GAP-F16-1 (interim PORTAL).
11. **Notices on the timeline (item 62).** Postal notices are LETTER entries (rules 3-5); SMS and LINE messages are CONTACT entries with `channel` SMS or LINE, `direction` OUTBOUND and `deliveryStatus`. Repeats: same header key with another body → 409 MSG-PLT-N009-05; new header key with an existing business key → 200 with the existing entry (RD-P1-001, RD-P1-007 rule 4).
12. **Complaints (item 41).** No ledger eventCode identifies a complaint. **Pending, owner product owner with compliance**, NEW-GAP-F10-02 kept. Interim: RWB-P10-E1062 X1 checks run without a complaint signal from the ledger; the complaint condition is marked Pending in the story.
13. **Failed append (item 59).** On 503 MSG-P1-022 the caller does not commit its action, or retries with the same header key and business key; no caller keeps an action whose entry was not written.
14. **Extra stories.** RWB-P3-E2021-APP (drop the delivery write), RWB-P3-E2016-CON (cite RD-P1-007 instead of GAP-0716), RWB-P10-E1062-APP (ledger read through `GET /cases/{caseId}/interactions`, as its CON), RWB-P6-E2021-CON (proof of delivery is the P1 `GET /proof-of-delivery` read by rwb-comms, not an INT-15 result from rwb-integration, as RWB-P6-E2021-OPS).

**Affected services.** rwb-source-data, rwb-comms, rwb-integration, rwb-case, rwb-partner, rwb-asset, rwb-agent, rwb-access (permissions).
**Affected stories.** RWB-P1-E1055-APP, RWB-P1-E2021-APP, RWB-P1-E2034-APP, RWB-P1-E1066-APP, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, RWB-P6-E1052-APP, RWB-P3-E2021-APP, RWB-P3-E2016-CON, RWB-P3-E2001-APP, RWB-P2-E2001-APP, RWB-ITG-E2021-ITG, RWB-ITG-E2034-ITG, RWB-ITG-E1055-ITG, RWB-S5-E3022-APP, RWB-S5-E3022-CON, RWB-S9 result stories (RWB-S9 stories cited under ASM-5391), RWB-P10-E1062-APP, RWB-P10-E1062-CON, RWB-ITG-E1062-ITG, RWB-P6-E4036-APP.
**Affected documents.** `rwb-source-data.yaml` (LETTER description: externalRef rule); Users Roles and Permissions v6 (.xlsx), Role to System Access Matrix v4 (.xlsx); Assumptions Register v3 (ASM-5391 changed); Gap Register v3 (NEW-GAP-S10-16, NEW-GAP-F06-1, NEW-GAP-F10-01, NEW-GAP-F08-1, NEW-GAP-F14-1, NEW-GAP-F14-2, NEW-GAP-F13-6, NEW-GAP-F13-7, NEW-GAP-F15-2, NEW-GAP-F16-2, NEW-GAP-F16-3, NEW-GAP-F16-4 closed; NEW-GAP-F10-02 and NEW-GAP-F16-1 kept; NEW-GAP-D3 new); register RD-P1-007 (amendment line).
**Escalation items settled.** 1, 26, 32, 37, 39, 40, 41, 50, 59 (second part), 60, 62 (second part), 63; extra stories RWB-P3-E2021-APP, RWB-P3-E2016-CON, RWB-P10-E1062-APP, RWB-P6-E2021-CON.
**Status.** Proposed – Claude Opus 5.5 (applied). **Reuse note.** Pair outbound and delivery entries on the external reference the channel returns (barcode for WIN); derive bounded business keys with UUID v5 of long source keys; customer-originated entries carry the receiving service as actor.
**Values chosen without a source.** `externalRef` barcode-then-noticeRef; UUID v5 URL namespace; `sourceRef` `INT-14 WIN`; dispatch `conductCheck` PASSED; HOME.SCB → PORTAL interim; actor of customer answers.

#### Story keys listed by the register

Batch D wrote "RWB-S9 result stories (RWB-S9 stories cited under ASM-5391)". Found in Service Story Files v2 (no S9 story of this set is staged in v3):

- RWB-S9-E6033-APP – the one S9 story that cites ASM-5391 (section 11, the DF-INT-001 to DF-INT-013 row "Not written here"); it now appends the PARTNER_RESULT entry over REST (rule 9).
- RWB-S9-E6033-CON – the contract of the partner result intake and of `rwb.partner.PartnerResultSubmitted.v1`.
- RWB-S9-E2034-APP – the partner half of the ledger: PARTNER_RESULT, INBOUND, PORTAL carried as event attributes (AC2).
- RWB-S9-E7018-APP – the field-visit result: an `InteractionLedgerClient` entry and EV-21 PartnerResultSubmitted (flow steps 9 and 11).
- RWB-S9-E7018-CON – the contract of the same result (EV-21; the ledger entry declared as consumed).
- Integration twin: RWB-ITG-E6033-ITG (staged Service Story Files v3).

#### Register amendments

- Amended by register (orchestrator; source REQUEST S12-stories-0340), register resolution XD-08: Rule 1: the in-process callers of `InteractionLedgerWriter` are RWB-P1-E1067-APP, RWB-P1-E2034-APP and RWB-P1-DM005-APP (cutover write of migrated notes and promises; RD-P1-007 final as amended). Rule 1 restated the v1 list and did not rule DM005 out.
- Amended by RD-P1-100 (batch E), register resolution XE-20: Clarification: the read property is `latestDeliveryStatus`, derived per `externalRef` from the entry with the latest `occurredAt`, ties broken by the highest `caseSeq`; `barcodeStatus` is removed.

**Final ruling (register).** Rules 2-14 apply. Rule 1: in-process callers RWB-P1-E1067-APP, RWB-P1-E2034-APP and RWB-P1-DM005-APP (cutover); REST callers as listed. The S9 partner-result stories of rule 9 are RWB-S9-E6033-APP, RWB-S9-E6033-CON, RWB-S9-E2034-APP, RWB-S9-E7018-APP and RWB-S9-E7018-CON (integration twin RWB-ITG-E6033-ITG). Batch E (v3): `latestDeliveryStatus` derivation (RD-P1-100).

---

## RD-P1-065 · Job reads and reruns across services; readiness repeats

_Original text of batch D kept for audit. Amendments and the final ruling follow it._

**Question (items 12, 24, 27, 31 rerun part, 48, 57 first part).**

**Sources.** Register RD-P1-012 final (rerun of a FAILED run only, ALLOW_DUPLICATE_FAILED_ONLY, 409 MSG-P1-011; other services' jobs served by their owners, gateway-bff composes; MIGRATION runs not served), RD-P1-040 final (readiness 202 idempotent; admin rerun only of FAILED runs), RD-P1-041 (no second AceDataReady for a stamped date), RD-P1-020 (`business_day_readiness`, business date unique). GR v3 GAP-3271 (per-service job reads, owner solution architect), GAP-0657 resolution ("serve the rerun on the integration base for the jobs of this service's catalogue"). BSD v7 Jobs rows JOB-03, JOB-06, JOB-14.

**Ruling.**
1. **One rerun standard (items 27, 31).** The RD-P1-012 rule is the platform standard for every service's job monitor: only a FAILED run is rerun (new run, same business date, reuse policy ALLOW_DUPLICATE_FAILED_ONLY); a COMPLETE or running run answers 409 with the owner's "already complete or running" code. TE008 of JOB-14 (rwb-decision) becomes the rerun of a FAILED chain check; a completed check is re-verified by the next 02:00 run. RWB-ITG-E2010-ITG and RWB-ITG-E4050-ITG drop "rerun of a completed run". An owner who needs another rule asks for a new RD decision.
2. **Job reads of other services (item 24).** GAP-3271 is widened to name rwb-case: the job read and rerun of DailyCaseRun (JOB-02 and its JOB-03 step) and of JOB-06 are served by rwb-case. Owner solution architect with the rwb-case owner. Interim: RWB-ITG-E1020-ITG and RWB-ITG-E1030-ITG assert outcomes through rwb-case's published reads (`/queues/{queueId}/cases`, `/cases/{caseId}`) and mark their rerun steps Pending.
3. **Readiness repeat (item 48).** `POST /business-days/{date}/ready` for a date that already has a `business_day_readiness` row answers 202 with the stored state; while AceIngestCheck runs it attaches (USE_EXISTING); once the row is DONE or LATE it starts nothing. A second ReconciliationWorkflow run of a date exists only through the rerun of a FAILED run. The ITG DM stories' assumption (no second reconciliation run) is confirmed; RWB-P1-E1011-APP and RWB-P1-E1013-APP state it.
4. **Booking confirmation retry (item 12).** No second AceDataReady is published for a stamped date. A RWB-P2-E2007-APP run that the gate refuses ends FAILED with MSG-P1-001 and is rerun from the rwb-integration job monitor (rule 1; GAP-0657); there is no wait-for-a-second-event path.
5. **RWB-PLT-E1044-CON (item 57).** Removes the migration-run record and the job-view fake (RD-P1-012: MIGRATION runs are not served).

**Affected services.** All services with jobs; rwb-case, rwb-decision, rwb-integration, rwb-source-data.
**Affected stories.** RWB-P1-E1011-APP, RWB-P1-E1013-APP, RWB-P1-AD018-APP, RWB-P2-E2007-APP, RWB-P2-E2007-CON, RWB-ITG-E2007-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E2010-ITG, RWB-ITG-E4050-ITG, RWB-ITG-E1011-ITG, RWB-PLT-E1044-CON, the rwb-decision JOB-14 story that holds TE008, and the ITG DM stories (RWB-ITG-DM0nn-ITG) that test readiness repeats.
**Affected documents.** Gap Register v3 (GAP-3271 widened; NEW-GAP-F04-1, NEW-GAP-F05-2 (rerun part) closed); Test Cases (TE008 row); Batch and Scheduling Design v7 (Jobs notes: rerun standard).
**Escalation items settled.** 12, 24, 27, 31 (rerun part), 48, 57 (first part); extra story RWB-PLT-E1044-CON.
**Status.** Proposed – Claude Opus 5.5 (applied). **Reuse note.** Reruns are of failed runs only, in every service; a repeated readiness call never restarts closed work.
**Values chosen without a source.** None beyond the reuse of RD-P1-012.

#### Story keys listed by the register

Batch D wrote "the rwb-decision JOB-14 story that holds TE008, and the ITG DM stories (RWB-ITG-DM0nn-ITG) that test readiness repeats". Found:

- RWB-PLT-TE008-APP (Service Story Files v2) – TE008, the JOB-14 chain check built as the `ChainCheckSchedule` instance in rwb-decision (02:00, queue `rwb-decision`).
- RWB-ITG-TE008-ITG (staged v3) – holds the rerun of a completed JOB-14 run (X3 and AC4, through the rwb-decision rerun operation, NEW-GAP-A1); under rule 1 it becomes the rerun of a FAILED chain check.
- ITG DM readiness stories (staged v3; each repeats `POST /business-days/{date}/ready` for the same business date with a new UUID Idempotency-Key and asserts that no second set of reconciliation result rows appears): RWB-ITG-DM003-ITG, RWB-ITG-DM004-ITG, RWB-ITG-DM005-ITG, RWB-ITG-DM006-ITG, RWB-ITG-DM007-ITG, RWB-ITG-DM008-ITG, RWB-ITG-DM009-ITG, RWB-ITG-DM010-ITG, RWB-ITG-DM011-ITG, RWB-ITG-DM012-ITG, RWB-ITG-DM013-ITG.
- Related, not listed by batch D: RWB-P7-E1008-APP owns `DecisionChainCheckWorkflow` and the Schedule `decision-log-chain-check` (JOB-14) and follows the same rerun standard.

#### Register amendments

- Amended by register resolution XD-11 (RD-P1-040 item 1): Rule 3 "once the row is DONE or LATE it starts nothing" holds when every due source of the date is stamped. When the closed run left a due source unstamped (closed at 24 h), the repeated call opens a new AceIngestCheck run (ALLOW_DUPLICATE, RD-P1-040 item 1 Closing) that stamps only the missing sources. Either way no second AceDataReady is published for a stamped source and no second ReconciliationWorkflow starts, so the ITG DM assumption stands.
- Amended by RD-P1-079 (batch E), register resolution XE-12: Rule 3 is read with RD-P1-079 rule 1 (XD-11 confirmed); before wave 4 the restart of a FAILED child is the runbook step of RD-P1-079 rule 4.

**Final ruling (register).** Rules 1, 2, 4 and 5 apply; rule 3 is read with RD-P1-040 item 1 (XD-11): a repeated ready call attaches while the run is open, starts nothing once every due source is stamped, and opens a new run only for due sources still unstamped after the run closed; never a second AceDataReady for a stamped source or a second ReconciliationWorkflow. Stories: RWB-PLT-TE008-APP and RWB-ITG-TE008-ITG (TE008 of JOB-14) and RWB-ITG-DM003-ITG, RWB-ITG-DM004-ITG, RWB-ITG-DM005-ITG, RWB-ITG-DM006-ITG, RWB-ITG-DM007-ITG, RWB-ITG-DM008-ITG, RWB-ITG-DM009-ITG, RWB-ITG-DM010-ITG, RWB-ITG-DM011-ITG, RWB-ITG-DM012-ITG, RWB-ITG-DM013-ITG (readiness repeats). Batch E (v3): rule 3 per RD-P1-079.

---

## RD-P1-066 · Event subscriptions, start rules and job owners; ACE boundary of rwb-payment

_Original text of batch D kept for audit. Amendments and the final ruling follow it._

**Question (items 5, 11 start, 13, 14, 15, 19, 20, 21, 30, 45, 53; ACE boundary of RWB-P8-E4044-APP/-CON and RWB-P8-E4045-APP).**

**Sources.** Run brief rule 6 (only rwb-source-data reads `recovery.v_ace_*`). RWB-P8-E4044-APP v3 lines 9, 48, 66, 74-75; RWB-P8-E4045-APP v3 lines 9, 50, 66, 77, 153; RWB-P8-E4047-APP line 337; YAML `/batch-status` (access rwb-integration only), `/payments`. Register RD-P1-003 (one consumer group per service per topic; KTEC v2 R13), RD-P1-040 (downstream daily work starts only on ALS/COMPLETED). BSD v7 Read me rows 19-20 (JOB-08 owner P8; JOB-02 event-started), Jobs rows JOB-02, JOB-08, JOB-15, JOB-20; Schedule and event map row JOB-15 (NEW-GAP-W5-003). GR v3 GAP-0657 (Accepted (directive): "Keep JOB-08 and its activities with rwb-integration … record the rwb-payment owner row of Architecture v5 slide 44 as superseded for this job"), GAP-0146 (DailyCaseRun: event-started; slide-14 Schedule a fallback not configured), GAP-3037. RWB-S7-E6023-APP lines 8, 28, 77, 89, 109. RWB-P2-E1007-APP lines 96, 378. Parameter Catalog v1 `caselist.allocation.wait.until` 07:15. PS v9 `data_product.expected_by` 08:00 for DP01.

**Precedence applied.** The ACE rule (D-RCV-60) overrides the P8 stories. For JOB-08 the GAP-0657 directive is a D-RCV-60 acceptance that explicitly supersedes the Arch v5 slide 44 owner row; it wins over RD-P1-040's consumer list and BSD v7. **Amends RD-P1-040 and RD-P1-003 (consumer list)**.

**Ruling.**
1. **ACE boundary.** RWB-P8-E4044-APP, RWB-P8-E4044-CON and RWB-P8-E4045-APP read no `recovery.v_ace_*` view. E4044 starts on AceDataReady (`sourceSystem` ALS, `status` COMPLETED) consumed from `rwb.source-data.events.v1` and reads the receipts with `GET /payments?businessDate=` (RD-P1-061); E4045 reads `GET /accounts/{accountKey}` (RD-P1-060) and `GET /payments`; either reads `GET /batch-status` when it needs the batch row. The YAML access line of `/batch-status` adds the rwb-payment workload identity. The "Open" lines of both stories are closed.
2. **Delivery of the events (items 20, 21).** AceDataReady and AceDataLate are delivered on the topic; "through the contract" means the asyncapi contract of rwb-source-data. rwb-payment has one consumer group, working ID `rwb-payment.rwb.source-data.events.v1`, with one listener that starts the JOB-07 run (RWB-P8-E2008-APP), E4044, E4047 and E4050 by signal-with-start on their own workflow IDs. Per-story groups are withdrawn. The same rule applies to every consumer service.
3. **JOB-08 owner (item 5).** rwb-integration (GAP-0657). BSD v7 Jobs and Schedule-map rows JOB-08 and Read me row 20 change owner to P2 rwb-integration; Kafka Topic and Event Catalog v3 adds consumer group `rwb-integration.rwb.source-data.events.v1` with READ ACL; rwb-payment keeps JOB-07. RD-P1-040 and RD-P1-003 consumer lists gain rwb-integration.
4. **Monthly GL write-off reconciliation (item 19).** No new event: the starter is AceDataReady with `sourceSystem` GL and `status` COMPLETED, consumed by rwb-writeoff's one group; the branch acts when `businessDate` is on or after the audit period's cut-off date. RD-P1-040's ALS-only rule governs daily jobs and is not breached by this monthly branch (clarification, not amendment). The posting-row read stays **Pending, owner P1 contract owner with the rwb-writeoff owner**, GAP-3037; interim the S7 stories build against a fake.
5. **Held-file release (item 13).** Confirmed: AceDataReady ALS/COMPLETED triggers the release; the held request re-reads freshness before building and stays held while its products are STALE.
6. **DailyCaseRun (item 14).** An event-started workflow started by rwb-case's AceDataReady (ALS, COMPLETED) consumer, not a Temporal Schedule; the slide-14 Schedule is a fallback not configured in the target (GAP-0146; BSD v7). RWB-PLT-NF07-INF is reworded.
7. **JOB-20 (item 15).** A Temporal Schedule in rwb-decision at 00:01 (BSD v7); AceDataReady does not start it. RWB-P7-E1020-APP preconditions are corrected.
8. **JOB-15 (item 30).** **Pending, owner solution architect with the rwb-reporting owner** (NEW-GAP-W5-003). Interim: the Airflow trigger `POST /reports/{id}/run` at 01:30 is the live entry (BSD v7 Jobs row JOB-15); the 01:30 Temporal Schedule is created paused. RWB-ITG-E2009-ITG and RWB-P9-E2009-APP follow.
9. **Lateness signals (item 45).** 07:15 is `caselist.allocation.wait.until`, the allocation wait limit, not a lateness alert. The staleness signal is STALE at `data_product.expected_by` (08:00 for DP01, RD-P1-041); AceDataLate goes out at 05:30. rwb-case derives no expected date: it reads `GET /data-products/freshness`.
10. **Case entry (item 11, start part).** JOB-02 starts on ALS alone (RD-P1-040); EFS completeness is handled in RD-P1-067.
11. **Retry and dead-letter topics (item 53).** Each consumer service gets WRITE and READ on the retry topics and WRITE on the `.dlt` topic of every topic it consumes (names per RWB-PLT-E1047-CON; RD-P1-009 non-blocking retry). Kafka Topic and Event Catalog v3 adds the ACL rows. Observability and Monitoring Design v6 adds catalog rows for AceIngestCheck (workflow metrics and alerts).

**Affected services.** rwb-payment, rwb-integration, rwb-writeoff, rwb-case, rwb-decision, rwb-reporting, rwb-deviation, gateway-bff, rwb-source-data.
**Affected stories.** RWB-P8-E4044-APP, RWB-P8-E4044-CON, RWB-P8-E4045-APP, RWB-P8-E4047-APP, RWB-P8-E4050-APP, RWB-P8-E2008-APP, RWB-P8-E2008-OPS, RWB-P2-E2007-APP, RWB-P2-E2007-OPS, RWB-P7-E2007-APP, RWB-S7-E6023-APP, RWB-S7-E6023-CON, RWB-P2-E1007-APP, RWB-PLT-NF07-INF, RWB-P7-E1020-APP, RWB-P9-E2009-APP, RWB-ITG-E2009-ITG, RWB-P3-E1011-APP, RWB-P3-E2001-APP, RWB-PLT-E1047-CON.
**Affected documents.** `rwb-source-data.yaml` (`/batch-status` access); Batch and Scheduling Design v7 (.xlsx; v6 .docx twin) JOB-08 owner, JOB-15 interim; Kafka Topic and Event Catalog v3 (consumer groups, retry/DLT ACLs); Event and Messaging Design v7; Temporal Workflow and Activity Catalog v3 (JOB-08 worker queue rwb-integration); Observability and Monitoring Design v6; Microservice Ownership Map v3 (JOB-08); Gap Register v3 (GAP-0146 resolved; NEW-GAP-F08-5, NEW-GAP-F08-10, NEW-GAP-F11-2 closed; GAP-3037, NEW-GAP-W5-003 kept); register RD-P1-040 and RD-P1-003 (amendment lines).
**Escalation items settled.** 5, 11 (start), 13, 14, 15, 19, 20, 21, 30, 45, 53; ACE boundary E4044/E4045.
**Status.** Proposed – Claude Opus 5.5 (applied). **Reuse note.** One group per service per topic, one listener fanning out; non-daily consumers may filter AceDataReady on another source; no service but rwb-source-data reads an ACE view.
**Values chosen without a source.** Group working IDs (pattern of RD-P1-003); JOB-15 Schedule paused interim; GL cut-off rule.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-067 · EFS history: gate products, late EFS batch and the single appender

_Original text of batch D kept for audit. Amendments and the final ruling follow it._

**Question (items 2, 11, 26).** RD-P1-010 final names DP01 as the gate of rule 8 (`GET /efs-history`), so a stale EFS (DP05) load no longer refuses and history can be partial; case entry starts on ALS alone while EFS may arrive late; the appender differs between RD-P1-007 rule 8 and staged RWB-P3-E2001-APP.

**Sources.** Register RD-P1-010 final; RD-P1-041 item 8 (gate source set = every source mapped to a DAILY product read by JOB-02, JOB-04, JOB-07 or JOB-08); BSD v7 JOB-02 ("Creates cases …; attaches history"); PS v9 seed DP05 DAILY 08:00 (EFS); YAML `/efs-history` description ("The DP01 and DP05 freshness gate must pass"); RD-P1-007 rule 8; Parameter Catalog v1 (no `handover.hold_until` row); RD-P1-040 (poll every 5 minutes).

**Precedence applied.** Within the register, RD-P1-041 item 8 already puts EFS in the gate set because JOB-02 reads DP05; this decision reconciles RD-P1-010 with it (clarification of RD-P1-010 rule 8, recorded as an amendment line).

**Ruling.**
1. **Gate (item 2).** `GET /efs-history` refuses with 409 MSG-P1-001 unless DP01 and DP05 are both complete for the business date (YAML text kept). `listEligibleAccounts` keeps the DP01 gate.
2. **Late EFS (item 11).** Case creation proceeds on ALS. The P2 hand-over run, on 409 MSG-P1-001 from `/efs-history`, waits on a durable timer and retries every 5 minutes until DP05 is stamped for the date or until `handover.hold_until`; at that limit it hands over without history and the rows are appended when DP05 arrives (the `EFS:<efsRecordKey>` business key makes the late append idempotent). The key `handover.hold_until` is not in Parameter Catalog v1: **Pending, owner rwb-integration owner with RW-COE**, NEW-GAP-D4; interim default 09:00 as in RWB-P3-E2001-APP. No separate completeness check is built.
3. **Appender (item 26).** The P2 rwb-integration hand-over run only (RD-P1-007 rule 8). RWB-P3-E2001-APP removes the append and keeps the case-side hand-over state.

**Affected stories.** RWB-P1-E2001-APP, RWB-P2-E2001-APP, RWB-P2-E2001-CON, RWB-P2-E2001-OPS, RWB-P3-E2001-APP, RWB-ITG-E2001-ITG.
**Affected documents.** Parameter Catalog v1.csv (row Pending, NEW-GAP-D4); Gap Register v3 (NEW-GAP-L03-2 closed; NEW-GAP-D4 new); register RD-P1-010 (amendment line).
**Escalation items settled.** 2, 11, 26.
**Status.** Proposed – Claude Opus 5.5 (applied). **Reuse note.** A read is gated on every product it serves; a late secondary product delays only the step that needs it, bounded by a parameter, and is caught up idempotently.
**Values chosen without a source.** Hand over without history at the limit; 5-minute retry.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-068 · Migration packages: decision chain, act-time snapshot fields, DM002, DM007 key, orphan checks, DP04, loader identity, local decision record table

_Original text of batch D kept for audit. Amendments and the final ruling follow it._

**Question (items 6, 7, 8, 9, 35, 36, 52, 57 second part).**

**Sources.** Staged `asyncapi/rwb.decision-record.v1.asyncapi.yaml` (ingest-rule line 31: "chain_seq and prev_hash assigned by rwb-decision under the chain lock"; payload lines 96-113: no rule, version, model or hash fields). RWB-P1-DM012-APP v3 lines 42-60. Register RD-P1-027 (allow-list: carry only Workbench system-of-record fields plus linking ACE business keys; DM007 carries DF-LEG-001..004 and DF-LEG-014), RD-P1-020 ("no P1 table" for decision records), RD-P1-021 (contact_point_ext cutover writer RWB-P1-DM005-APP), RD-P1-022 (REC-05 scope). LDM v10 DF-DEC-006 `model_version` (COLLINS; "Read at decision time"), DF-FIN-006 `amount` and DF-FIN-007 `received_date` (core bank via COLLINS), DF-LEG-005 `lawsuit_no` (LIT; DF-ACE-233 `v_ace_lawsuit.lawsuit_no`). GR v3 GAP-2533 (Accepted (directive): "keep the recorded legacy amount and received date with their provenance and copy no ACE row"). DMA v4 lines 132, 173 (RWB-DM-002: "Nothing: out of scope"). PS v9 seed DP04 ON_CHANGE, "ACE (ingested from the core bank) for the plan". Arch v5 line 1477 ("DB Own schema: business tables + outbox + inbox + decision_record") and line 1495. PS v9: no schema file holds a `decision_record` table.

**Precedence applied.** GAP-2533 (D-RCV-60 directive) and Arch v5 line 1477 outrank RD-P1-027 and RD-P1-020. **Amends RD-P1-027** (act-time snapshot class; DM007 key; DM002 clause) and **RD-P1-020** (decision_record table).

**Ruling.**
1. **Decision chain (item 6).** rwb-decision owns `chain_seq` and `prev_hash`; RWB-P1-DM012-APP sets no chain field and drops "the first record written in this service after cutover takes the entry_hash of the last migrated entry". Carrying the legacy `prev_hash`/`entry_hash`, rule ID and rule version on DecisionRecorded is **Pending, owner rwb-decision contract owner with compliance**, NEW-GAP-S13-4 kept (blocks the publish step only). Interim: DM012 builds the extract and the local decision records; publication of migrated entries stays behind the DM012 feature switch (off) until the schema carries the fields; the cutover evidence file lists every legacy `entry_hash` and the last legacy hash.
2. **Act-time snapshot fields (item 7).** A field that records a value as it was at a past act, which ACE cannot answer later, is CARRY with reason "value at act time": DF-DEC-006 `model_version` (DM012) and DF-FIN-006 `amount`, DF-FIN-007 `received_date` of the legacy proceeds (DM013, GAP-2533), each with `migration_source` and `migrated_at`. Source to Target Mapping v7 sheet Migration packages rows change from ACE_READ to CARRY with that reason.
3. **DM002 (item 8).** Migrates nothing (DMA v4). RWB-P1-DM002-APP is a verification story that reads `GET /customers/{personKey}` (RD-P1-060) and writes no row; the RD-P1-027 clause "DM002 contact_point_ext has zero or one row per contact_key …" belongs to RWB-P1-DM005-APP.
4. **DM007 key (item 9).** DF-LEG-005 `lawsuit_no` is KEY (the linking ACE business key to `v_ace_lawsuit`); DF-LEG-006 to DF-LEG-013 stay EXCLUDE (ACE_READ).
5. **Orphans (item 35).** REC-05 scope is unchanged. The `plan_ref` (DM004) and `asset_key` (DM006) orphan checks are each DM story's own cutover check, counted in its evidence; they read the keys through rwb-source-data (`GET /accounts/{accountKey}`, `GET /collateral/{assetKey}`).
6. **DP04 (item 36).** DP04 is ON_CHANGE (seed). Its plan part has a mapped source (the core bank, RD-P1-021 `data_product_source`): a stamp row is written when that source completes, it is never set STALE by time and DP04 is not in the DAILY gate set. RWB-P1-DM004-APP corrects "no ACE source".
7. **Loader identity (item 57).** With SY-DATALOAD retired, each package is loaded by its target service under that service's workload identity and migration owner (RD-P1-021: one owner per table).
8. **Local decision record table (item 52).** `rwb_source_data` has the local `decision_record` table that every service owns (Arch v5 line 1477), created by the shared library migration of RWB-PLT-E1027-CON; DM012 and the sandbox write through it. Its DDL is in no schema file of PS v9: **Pending, owner platform lead (library owner)**, NEW-GAP-F08-7 kept; interim the library's own migration runs in the Testcontainers build. `ce_idempotencykey` = the RD-P1-007 rule 4 business key (RD-P1-009); NEW-GAP-F08-6 closed.

**Affected stories.** RWB-P1-DM002-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P1-E1065-APP, RWB-PLT-E1027-CON, the ITG DM stories of DM004, DM006, DM007, DM012, DM013.
**Affected documents.** Source to Target Mapping v7 (.xlsx, sheet Migration packages); Data Migration Approach v5 (.docx); Physical Schema v9 README (decision_record Pending note); Microservice Ownership Map v3 (DM002 row); Gap Register v3 (NEW-GAP-S12-2, NEW-GAP-S12-6, NEW-GAP-F06-4, NEW-GAP-F06-6, NEW-GAP-F08-6 closed; NEW-GAP-S13-4, NEW-GAP-F08-7 kept); register RD-P1-027 and RD-P1-020 (amendment lines).
**Escalation items settled.** 6, 7, 8, 9, 35, 36, 52, 57 (second part).
**Status.** Proposed – Claude Opus 5.5 (applied). **Reuse note.** Carry a value ACE cannot answer later; never carry a value ACE answers; one chain owner; every service has its local decision record table.
**Values chosen without a source.** "Act-time snapshot" class name and reason text; DM012 publish switch interim.

#### Story keys listed by the register

Batch D wrote "the ITG DM stories of DM004, DM006, DM007, DM012, DM013" (orchestrator: packages DM004 to DM013). Found (staged v3): RWB-ITG-DM004-ITG, RWB-ITG-DM006-ITG, RWB-ITG-DM007-ITG, RWB-ITG-DM012-ITG, RWB-ITG-DM013-ITG. The other ITG DM stories in that range (RWB-ITG-DM005-ITG, RWB-ITG-DM008-ITG to RWB-ITG-DM011-ITG) name none of the fields or checks of rules 1-5 and 8 (`plan_ref`, `asset_key`, `lawsuit_no`, `model_version`, `chain_seq`, `prev_hash`, `received_date`, `decision_record`) and no SY-DATALOAD loader (rule 7), so they are not affected.

#### Register amendments

- Amended by RD-P1-081 (batch E), register resolution XE-13: Rule 6: the DP04 row of D is written by `stampDp04` of Stage2ProductWorkflow after every DP04 page of D is committed (source_system WORKBENCH, `source_extracted_at` = ALS `completed_at` of D); once a core-bank `data_product_source` row for DP04 is seeded (ASM-5695), Stage2ProductWorkflow first waits for that source. DP04 stays ON_CHANGE, never STALE by time, not in the DAILY gate.

**Final ruling (register).** As ruled above; the ITG DM stories are RWB-ITG-DM004-ITG, RWB-ITG-DM006-ITG, RWB-ITG-DM007-ITG, RWB-ITG-DM012-ITG, RWB-ITG-DM013-ITG. Batch E (v3): DP04 stamped by stampDp04 after the build (RD-P1-081).

---

## RD-P1-069 · Reconciliation breaks, orphan keys, REC-04/REC-06 and date-wide reads

_Original text of batch D kept for audit. Amendments and the final ruling follow it._

**Question (items 31 break list, 33, 38 held proof rows and REC-09, 42, 43, 44).**

**Sources.** YAML `/admin/reconciliation/results/{resultId}` (break detail store and locator Pending, GAP-1508, NEW-GAP-S2B-03), `/proof-of-delivery` (paging GAP-0577), `BatchStatusAnswer` (no checksum); PS v9 `v_ace_batch_status.checksum` varchar(64). Register RD-P1-012 (P1 checks REC-01, REC-02, REC-05), RD-P1-022 (REC-05 owner P1; key-list read GAP-3273). RWB-P8-E4050-APP lines 64-66, 88 (REC-04 is part of the rwb-payment daily reconciliation).

**Ruling.**
1. **Break and orphan detail (items 31, 43).** Store and read stay **Pending, owner P1 data architect with the P1 contract owner** (GAP-1508, NEW-GAP-S2B-03). Interim: result reads answer aggregates; RWB-P1-AD019-APP, RWB-ITG-E2010-ITG, RWB-ITG-E4050-ITG and the P3 console assert counts.
2. **REC-04 and REC-06 (item 33).** Computed by rwb-payment's daily reconciliation (RWB-P8-E4050-APP) into `rwb_payment`; P1 computes REC-01, REC-02 and REC-05 only. `BatchStatusAnswer` adds `checksum` (string, maxLength 64, nullable; `v_ace_batch_status.checksum`) for E4050.
3. **Held proof rows and REC-09 (item 38).** No published read in P1 v1; Pending under GAP-0577 and GAP-1508.
4. **Date-wide DP06 (item 42).** **Pending, owner P1 contract owner with the rwb-asset owner**, NEW-GAP-F10-03 kept. Interim (not blocking): the S5 reconciliation reads each asset of its own list through `GET /collateral/{assetKey}` (RD-P1-060).
5. **Open-case key check (item 44).** One owner: P1 REC-05 (RD-P1-022). RWB-P3-E1011-APP drops its own check and serves only the key-list read (GAP-3273).

**Affected stories.** RWB-P1-E1011-APP, RWB-P1-E1011-CON, RWB-P1-AD019-APP, RWB-P1-E2010-APP, RWB-P3-E1011-APP, RWB-S5-E1011-APP, RWB-P8-E4050-APP, RWB-ITG-E2010-ITG, RWB-ITG-E4050-ITG, RWB-ITG-E1011-ITG.
**Affected documents.** `rwb-source-data.yaml` (`BatchStatusAnswer.checksum`); Data Quality and Reconciliation Rules v5 (owner of REC-04, REC-06); Gap Register v3 (NEW-GAP-F11-4 closed; GAP-1508, NEW-GAP-S2B-03, NEW-GAP-F10-03, GAP-0577 kept).
**Escalation items settled.** 31 (break list), 33, 38 (proof rows, REC-09), 42, 43, 44.
**Status.** Proposed – Claude Opus 5.5 (applied). **Reuse note.** One owner per reconciliation check; consumers of break detail build on counts until GAP-1508 closes.
**Values chosen without a source.** None (checksum from the view).

#### Register amendments

- Amended by RD-P1-086 (batch E), register resolution XE-21: REC-05 is written as one aggregate `reconciliation_result` row per business date (`product_group` ALL, PASS when no orphan) and served by `GET /admin/reconciliation/results` (`recCode` REC-01, REC-02, REC-05); the result page envelope is {items, page, size, total}. Orphan detail stays Pending (GAP-1508, GAP-3413).

**Final ruling (register).** As ruled above, amended by batch E (v3): REC-05 aggregate row; result page envelope (RD-P1-086).

---

## RD-P1-070 · Count-once store for failed contacts

_Original text of batch D kept for audit. Amendments and the final ruling follow it._

**Question (item 3).** `POST /contact-points/{contactPointKey}/failed-contacts` must raise `failed_count` once per contact point and reference, but no store of counted references exists (NEW-GAP-S10-17).

**Sources.** YAML lines 1241-1282; PS v9 `processed_event` (consumer varchar(60), idempotency_key varchar(120), event_id uuid nullable, hit_count, uk_processed_event (consumer, idempotency_key)); register RD-P1-001 (R-UNI-40: "work key with event_id null for in-process keys").

**Ruling.** The counted references are rows of `rwb_source_data.processed_event` with `consumer` `rwb-source-data.failed-contacts`, `idempotency_key` `FC:` followed by the lowercase hex SHA-256 of `<contactPointKey>|<reference>` (67 characters), `event_id` null. The row and the `failed_count` increase are written in one transaction. A repeat finds the row: `hit_count` + 1, `failed_count` unchanged, answer 201 with `counted` false. No new table.

**Affected stories.** RWB-P1-E2022-APP, RWB-P6 SMS/LINE caller stories, RWB-ITG-E2022 stories. **Affected documents.** `rwb-source-data.yaml` (description: Pending removed); Gap Register v3 (NEW-GAP-S10-17 closed).
**Escalation items settled.** 3. **Status.** Proposed – Claude Opus 5.5 (applied). **Reuse note.** In-process count-once keys use `processed_event` with a hashed key when the natural key can exceed 120 characters.
**Values chosen without a source.** Consumer name; `FC:` prefix and hash form.

#### Story keys listed by the register

Batch D wrote "RWB-P6 SMS/LINE caller stories, RWB-ITG-E2022 stories". Callers of `POST /contact-points/{contactPointKey}/failed-contacts` found (staged v3): RWB-P6-E2022-APP (posts the failed reference with a UUID Idempotency-Key), RWB-P6-E2022-CON (the consumed-operation row and its acceptance criterion), RWB-P6-E2022-OPS (the rwb-source-data client under the rwb-comms workload identity) and RWB-ITG-E2022-ITG (the WireMock of the operation; it is the only ITG E2022 story). RWB-P6-E4039-APP and RWB-P6-E4039-CON (v2) name `failed_count` as a field written through the P1 contract but do not call this operation; they are not listed.

#### Register amendments

- Register resolution XD-10: this decision prevails over the reading "`processed_event` holds ledger-intake redeliveries (ce_id) only" of RD-P1-001 rule 7 (X-19); the amendment line is in RD-P1-001.

**Final ruling (register).** As ruled above (prevails over the ledger-intake-only reading of RD-P1-001 rule 7, XD-10); the callers are RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2022-OPS, RWB-ITG-E2022-ITG.

---

## RD-P1-071 · Data dictionary gate and new fields

_Original text of batch D kept for audit. Amendments and the final ruling follow it._

**Question (item 55).** RWB-P4-E1064-APP refuses loads naming unknown fields, while RD-P1-025 adds fields only through a load – a deadlock.

**Sources.** EMS v5 MSG-P1-005 ("A rule version names a field not in the data dictionary"); register RD-P1-025 (later fields carry `sys_field_version` rows).

**Ruling.** The unknown-field check (MSG-P1-005) applies to rule versions, mappings and access loads that name fields. A data dictionary load is how a field becomes known: it validates its own rows (field code unique, entity present in `sys_objects`, type valid) and writes `sys_fields` and `sys_field_version` rows. When one release brings both, the dictionary load is applied first. RWB-P4-E1064-APP and RWB-P1-E1064-APP state the scope.

**Affected stories.** RWB-P4-E1064-APP, RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E1064-OPS. **Affected documents.** Gap Register v3 (NEW-GAP-F09-5 closed).
**Escalation items settled.** 55. **Status.** Proposed – Claude Opus 5.5 (applied). **Reuse note.** Gates that check names against a catalog never apply to the load that maintains the catalog.
**Values chosen without a source.** Order dictionary first.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-072 · Decision records versus reads in the ledger intake; personal data seen by agents

_Original text of batch D kept for audit. Amendments and the final ruling follow it._

**Question (items 56, 38 call notes).** RD-P1-009 row 06 turns every DecisionRecorded with a `caseId` into a DECISION_TAKEN entry; if reads were recorded as decisions, each case-record read would add a timeline entry. A screening agent may read unmasked call-note text.

**Sources.** Register RD-P1-009 row 06; DP-03 (decision records for decisions); YAML records read ("every read is written to the access log"); YAML `Interaction.summary` ("Masked unless the caller's role may see it").

**Ruling.**
1. A read is not a decision. Reads (case record, data product, customer, authorise checks) are written to the access log only and publish no DecisionRecorded. Only decisions under DP-03 (for example a delegation-of-authority approval) are decision records, and those with a `caseId` correctly become DECISION_TAKEN entries. Stories that record a read as a decision are corrected; RD-P1-009 is unchanged.
2. The screening agent reads `summary` masked; an unmasking rule for an agent identity is **Pending, owner data protection officer**, NEW-GAP-F03-2 kept; interim masked.

**Affected stories.** RWB-P4-E1016-APP, RWB-P1-E1016-APP, RWB-P1-E1067-APP, RWB-P10-E1062-APP, RWB-P10-E1062-CON, RWB-ITG-E1062-ITG. **Affected documents.** Gap Register v3 (NEW-GAP-F09-4 closed; NEW-GAP-F03-2 kept).
**Escalation items settled.** 38 (call notes), 56. **Status.** Proposed – Claude Opus 5.5 (applied). **Reuse note.** Access is logged, decisions are recorded; never both for a read.
**Values chosen without a source.** None.

#### Register amendments

- Amended by RD-P1-091 (batch E), register resolution XE-22: Clarification: access records (AC-READ, AC-DENY) go through the rwb-access access-log contract of RWB-P4-E1039-CON via `AccessClient`, never through the decision-record library or a topic; a read whose access record cannot be written returns no data (503 MSG-GEN-006); transport pending GAP-3322 with an in-process interim port.

**Final ruling (register).** As ruled above, amended by batch E (v3): access-log path per RD-P1-091.

---

## RD-P1-073 · Test isolation for append-only rows and the shared sandbox

_Original text of batch D kept for audit. Amendments and the final ruling follow it._

**Question (items 28, 38 sandbox).** The ITG harness wants to reset append-only ledger rows (NEW-GAP-F04-2, W1J01); a failed sandbox build and the seeding of other schemas are unclear (NEW-GAP-F03-4, NEW-GAP-F03-5).

**Sources.** Register RD-P1-007 rule 1 (append only; no update or delete), RD-P1-046 (sandbox `rwb_sandbox`, shared), RD-P1-021 (role and permission seeding to RWB-P4-E1065-APP, AC12 to RWB-P3-E1065-APP).

**Ruling.**
1. No environment deletes or resets ledger rows. The ITG harness isolates by run: every test creates its own cases and uses a fresh UUID per run as `<actionId>` in business keys; assertions filter by `caseId`. The only reset is the rebuild of the sandbox from DDL between suites (RD-P1-046).
2. A failed sandbox build leaves the previous sandbox in place and fails the pipeline; each schema is seeded by its owner's E1065 story (RD-P1-021).

**Affected stories.** RWB-ITG-E2034-ITG, RWB-ITG-E1065-ITG, RWB-ITG-W1 journey stories using W1J01, RWB-P1-E1065-APP, RWB-P1-E1065-CON, RWB-P1-E1065-DB, RWB-P3-E1065-APP, RWB-P4-E1065-APP, RWB-S8-E1065-APP. **Affected documents.** Gap Register v3 (NEW-GAP-F04-2, NEW-GAP-F03-4, NEW-GAP-F03-5 closed).
**Escalation items settled.** 28, 38 (sandbox). **Status.** Proposed – Claude Opus 5.5 (applied). **Reuse note.** Isolate tests by data, never by deleting append-only rows.
**Values chosen without a source.** Keep-old-sandbox rule.

#### Story keys listed by the register

Batch D wrote "RWB-ITG W1 journey stories using W1J01". Found (staged v3): RWB-ITG-W1J01-ITG (the contract-test harness; it carries the ledger-reset Pending NEW-GAP-F04-2, closed by rule 1) and RWB-ITG-W1J02-ITG (the wave 1 journey on the W1J01 synthetic set; its step 13 returns to the seeded state and runs the journey again, which now isolates by run instead of resetting ledger rows).

#### Register amendments

- Amended by RD-P1-089 (batch E), register resolution XE-23: Clarification: the runtime login holds SELECT and INSERT on `interaction` only and a BEFORE TRUNCATE trigger refuses TRUNCATE; the sandbox in-place reload excludes `interaction`; the rebuild from DDL is DROP SCHEMA `rwb_source_data` CASCADE in `rwb_sandbox` and the Flyway sequence plus seed, never a database drop.

**Final ruling (register).** As ruled above; the W1 journey stories are RWB-ITG-W1J01-ITG and RWB-ITG-W1J02-ITG. Batch E (v3): protection and rebuild mechanism per RD-P1-089.

---

## RD-P1-074 · Build-chain depth and the E1066-OPS / E1067-APP cycle

_Original text of batch D kept for audit. Amendments and the final ruling follow it._

**Question (item 58).** Seven rwb-source-data stories sit in build chains up to 6 deep against a limit of 4; E1066-OPS and E1067-APP depend on each other.

**Ruling.**
1. The cut of the deep chains is **Pending, owner solution architect**, NEW-GAP-D5; interim the Story Build Order v5 and Dependency Map v7 keep the chains, flagged, and the stories are READY WITH MINOR GAPS.
2. The cycle is broken: RWB-P1-E1067-APP depends on RWB-P1-E1066-APP (the writer) only; RWB-P1-E1066-OPS depends on RWB-P1-E1066-APP and not on RWB-P1-E1067-APP; the intake's deployment step is a later step with no build dependency back.
3. The W9 graph (`SET\_work\p1-ready\qa\w9-governance\graph.py`, then `apply.py` and `fix_bo.py`) is re-run after story editing ends.

**Affected stories.** RWB-P1-E1066-OPS, RWB-P1-E1067-APP, RWB-P1-E1067-CON and the seven chain stories named by W9. **Affected documents.** Story Build Order v5 (.docx), Dependency Map v7 (.xlsx); Gap Register v3 (NEW-GAP-D5).
**Escalation items settled.** 58; finishing-pass step "re-run W9". **Status.** Proposed – Claude Opus 5.5 (applied). **Reuse note.** OPS stories depend on their APP stories, never the reverse.
**Values chosen without a source.** Direction of the cycle cut.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-075 · Data dictionary baseline: values copied from Physical Schema v9

_Original text of batch E kept for audit. Amendments and the final ruling follow it._

**Question.** RD-P1-025 tells RWB-P1-E1001-APP to copy the 123 objects and 1,379 baseline fields from the Physical Schema v8 seed. The v8 seed has DF-REF-074 as `varchar(120)`; PS v9 (staged, line 1457) has `varchar(200)` and corrected DF-ACE types. Which seed is the baseline (RR ruling item RWB-P1-E1001-APP#1)?

**Options considered.** (1) Keep v8 and apply the v9 corrections by a later migration. (2) Copy the baseline from PS v9. Option 2: PS v9 is the staged next version that already carries the RD-P1-025 widening and the RD-P1-024 retirements; copying v8 would ship values the register already corrected.

**Sources.** REG v2 RD-P1-025 (baseline "Physical Schema v8 rwb_source_data.sql seed … DF-REF-074 widened to varchar(200)"); PS v9 `rwb_source_data.sql` line 1457 (DF-REF-074 `varchar(200)`), lines 2432-2434 (retired rows marked `RETIRED`), 2436 onwards (rows "added by later story migrations … not part of the RWB-P1-E1001-APP baseline"); PS v9 README line 235 (127 object rows and 1,409 field rows = the 123 / 1,379 baseline plus `data_product_source` and later story rows).

**Precedence applied.** RD-P1-025 is a register decision; this decision amends its source version only. Counts are unchanged.

**Ruling.**
1. The RWB-P1-E1001-APP baseline is the `rwb_source_data.sql` seed of **Physical Schema v9**: the 123 `sys_objects` and 1,379 `sys_fields` baseline rows with their v9 values (DF-REF-074 `varchar(200)`, the corrected DF-ACE physical types), the `data_product` seed (14 rows), `case_list_row` and `lake_copy_watermark` kept and marked `RETIRED`. Counts stay "at least 123 / 1,379".
2. The rows PS v9 lists after the comment "Dictionary rows added by later story migrations" (`job_run`, `job_run_check`, `business_day_readiness`, DF-OPS-233 to DF-OPS-257, DF-EXT-050, DF-INT-030) and the `data_product_source` rows (DF-REF-300 to DF-REF-302) are not baseline rows; they are written by the migration of the story that creates the table (RD-P1-096 rule 1).
3. RWB-P1-E1001-APP section 4 step 3, section 13 build step 8, AC1 and AC5 say "copied with their Physical Schema v9 values"; every "Physical Schema v8" citation in P1 stories that names the seed becomes v9.
4. The `is_personal` values of the seed follow RD-P1-076 (Data Classification v6), not the v9 seed as it stands.

**Rationale.** One baseline that already includes the corrections the register made, so no story ships a value that a later migration must undo.

**Affected services.** rwb-source-data.
**Affected stories.** RWB-P1-E1001-APP, RWB-P1-E1064-APP, RWB-P1-E1064-OPS, RWB-P1-E1016-DB, RWB-P1-ACE001-DB, RWB-P1-E1016-CON.
**Affected documents.** Register RD-P1-025 (amendment line); Test Cases v9 (TC-P1-E1001-APP rows citing v8); Logical Data Model and Data Dictionary v11 (no change; already v9 values).
**Findings settled.** RWB-P1-E1001-APP#1 (re-review).
**GAP/ASM.** None.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** A dictionary baseline is always copied from the highest staged Physical Schema version.
**Values chosen without a source.** None.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-076 · Personal-data flag: Data Classification v6 governs; default masking by classification

_Original text of batch E kept for audit. Amendments and the final ruling follow it._

**Question.** RWB-P1-E1001-APP AC13 (CTL-11) compares `sys_fields.is_personal` with the personal-data inventory, but the PS v9 seed and DCPI v6 disagree. Which source governs, what does AC13 compare, and what does "a field with no rule is masked" (RD-P1-060 rule 2) apply to? Related: RWB-P1-E1068-APP guardrail "A personal field with no unmasking rule is never returned" against BR4 returning promise fields (RR E1068-APP#4); DP04 personal data and an access-log write failure (GAP-3529; RR E2010-CON#13).

**Options considered.** (1) PS v9 seed governs. (2) DCPI v6 governs and `is_personal` mirrors its "Personal data" column; masking by default keyed on `is_personal`. (3) DCPI v6 governs; `is_personal` mirrors "Personal data"; the mask-by-default rule keys on the DCPI classification Restricted. Option 3.

**Sources.** DCPI v6 sheet Fields (1,395 fields; columns BR Field ID, Personal data category, Classification, Personal data, On screen); sheet Key ("Restricted: masked or never exposed in clear"; "Confidential: customer data shown within scope, encrypted"; "Internal: shown by permission"; "Masking policy: the P4 rwb-access masking_rule rows, enforced in each service and applied by rwb-source-data on every ACE field it serves"); sheet Handling; Read me v6 ("Personal-field flags remain keyed by field ID; P4 rwb-access owns masking_rule"). PS v9 `rwb_source_data.sql` sys_fields seed (1,409 rows). Comparison made for this ruling: 500 field IDs differ (seed false where DCPI says Yes: 361 Customer data, 76 Indirect identifier, 50 Staff identifier, 5 Sensitive, 4 Direct identifier; seed true where DCPI says No: DF-DOC-049, DF-DOC-052, DF-DOC-077, DF-DOC-089); 27 seed rows have no DCPI row (DF-INT-030, DF-REF-274 to DF-REF-299). DCPI v6 DF-TRT-050 `contract_no`: Not personal, Internal. REG v2 RD-P1-060 rule 2. RWB-P3-E1023-APP BR4 ("a read whose record cannot be written returns no data").

**Precedence applied.** No higher tier rules the flag. DCPI is the inventory owned by the data protection officer and the document the bank's PDPA controls cite; the dictionary column is a copy. **Amends RD-P1-060 rule 2** (scope of the mask-by-default rule).

**Ruling.**
1. **Source of truth.** DCPI v6 sheet Fields governs whether a field is personal, its category and its classification. `sys_fields.is_personal` = true exactly when the DCPI v6 row of the same field ID has Personal data = "Yes".
2. **Seed correction.** The data architect corrects the `is_personal` values of the PS v9 seed (staged, not yet released) to rule 1 before RWB-P1-E1001-APP is Done: 496 rows false → true and the four DF-DOC rows above true → false. LDM v11 sheet Fields follows the same flags.
3. **AC13.** RWB-P1-E1001-APP AC13 compares every baseline field ID present in DCPI v6: `is_personal` must equal (Personal data = "Yes"); any difference fails with the list of field IDs. A field ID absent from DCPI v6 is listed as "unclassified" and does not fail AC13; the 27 absent rows (DF-INT-030, DF-REF-274 to DF-REF-299) are **Pending, owner data protection officer**, NEW-GAP-E1; interim they are treated as not personal and the list is attached to the release evidence.
4. **Masking default (amends RD-P1-060 rule 2).** `FieldMasker.mask(dto, session)` (RWB-P4-E1037-CON) applies to every personal field. A field of classification **Restricted** (Direct identifier or Sensitive) with no unmasking rule for the caller is masked. A personal field of classification Confidential or Internal (Customer data, Indirect identifier, Staff identifier) is returned within the caller's case scope unless a masking rule masks it (DCPI v6 Handling and Key). Confirmation of this default by the data protection officer is **Pending**, NEW-GAP-E5; interim the FieldMasker fake applies rule 4 as written.
5. **RWB-P1-E1068-APP.** The guardrail reads "A Restricted field with no unmasking rule is never returned in clear". `personKey` and `contactKey` (Indirect identifier), `actorRef` (Staff identifier) and the promise fields `promiseAmount`, `promiseDate` (Customer data, Confidential; DF-INT-010) are returned within scope; `summary` keeps its own rule (masked unless the role may see it; RD-P1-072 rule 2).
6. **DP04 (GAP-3529).** No DP04 property is Restricted in DCPI v6; `contract_no` (DF-TRT-050) is Not personal, Internal, and is returned by permission. When the access-log entry of a records read cannot be written (RD-P1-091), the read answers **503 MSG-GEN-006** and returns no row (fail closed; RWB-P3-E1023-APP BR4 pattern). GAP-3529 is closed.

**Rationale.** One owner for classification; the dictionary flag becomes checkable; masking by default lands on the 17 Restricted fields instead of silently masking 500 customer-data fields that the screens must show within scope.

**Affected services.** rwb-source-data; rwb-access (masking rules, FieldMasker fake); every service that uses FieldMasker.
**Affected stories.** RWB-P1-E1001-APP, RWB-P1-E1068-APP, RWB-P1-E1016-APP, RWB-P1-E1016-CON, RWB-P1-E1069-APP, RWB-P1-E2010-CON, RWB-P1-E2010-APP, RWB-P4-E1037-CON, RWB-P4-E1037-APP, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON.
**Affected documents.** Physical Schema v9 `rwb_source_data.sql` (is_personal values; owner data architect); Logical Data Model and Data Dictionary v11 (same); Data Classification and Personal Data Inventory v6 (27 rows Pending); register RD-P1-060 (amendment line); Gap Register v3 (GAP-3529 closed; NEW-GAP-E1, NEW-GAP-E5); Test Cases v9 (TC rows of E1001-APP AC13, E1068-APP guardrail).
**Findings settled.** RWB-P1-E1001-APP#2, RWB-P1-E1068-APP#4, RWB-P1-E2010-CON#13 (re-review).
**GAP/ASM.** Closes GAP-3529. Narrows GAP-3475 (NEW-GAP-S6-13) to the confirmation in NEW-GAP-E5. New NEW-GAP-E1, NEW-GAP-E5.
**Status.** Proposed – Claude Opus 5.5 (applied); NEW-GAP-E1 and NEW-GAP-E5 pending with the data protection officer.
**Reuse note.** Ask DCPI whether a field is personal; mask by default only what DCPI classes Restricted.
**Values chosen without a source.** Classification-keyed masking default; "unclassified" handling of fields absent from DCPI.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-077 · Recipient phone number for SMS and LINE notices

_Original text of batch E kept for audit. Amendments and the final ruling follow it._

**Question.** RD-P1-060 rule 3 unmasks the clear name and the postal address for the rwb-comms notice and rwb-integration outbound-file identities (masking rows Pending GAP-3283, NEW-GAP-D1). SMS notices (RWB-P1-E2022-APP, RWB-P6-E2022-APP) need the clear phone number. Who may read it, and through which read?

**Sources.** REG v2 RD-P1-060 rules 2-4; DCPI v6 DF-ACE-078 `contact_value` (Direct identifier, Restricted, "Masked unless the role may see it", lawful basis "legal obligation for statutory notices"); DCPI v6 sheet Key ("ACE contact value: full value where a notice or a call needs it; masked for display"); YAML `ContactPointRow` and DP02 records rule (no contact value).

**Ruling.**
1. The clear phone number is the `contactValue` of a `contacts[]` row with `contactType` PHONE, read only through `GET /customers/{personKey}` (RD-P1-060), chosen by `contactKey`.
2. It is unmasked only for the **rwb-comms notice workload identity** (SMS and LINE dispatch through NSS and LINE OA; RWB-P1-E2022-APP, RWB-P6-E2022-APP, RWB-P6-E2021-APP). rwb-integration, gateway-bff and every user role get `contactValueMasked`. EMAIL rows follow the same rule.
3. The masking rule rows are part of GAP-3283 (NEW-GAP-D1), widened to "PHONE and EMAIL `contactValue` for the rwb-comms notice identity"; owner data protection officer with the rwb-access owner. Interim: the FieldMasker fake unmasks PHONE and EMAIL `contactValue` for the rwb-comms notice identity only; tests assert the masked branch for every other caller.
4. The phone number never enters an event, a workflow input, a ledger `summary`, a log or a metric (DCPI v6 PII controls); the ledger CONTACT entry carries `contactKey` only.

**Affected services.** rwb-source-data; rwb-comms; rwb-access.
**Affected stories.** RWB-P1-E2022-APP, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2021-APP, RWB-P1-E1069-APP, RWB-P4-E1037-CON.
**Affected documents.** Gap Register v3 (GAP-3283 subject widened); Users Roles and Permissions v6 / Role to System Access Matrix v4 (masking rows Pending).
**GAP/ASM.** GAP-3283 widened.
**Status.** Proposed – Claude Opus 5.5 (applied); masking rows pending under GAP-3283.
**Reuse note.** Any channel that needs a clear contact point reads it from `GET /customers/{personKey}` under its own notice identity and stores only `contactKey`.
**Values chosen without a source.** EMAIL included with PHONE.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-078 · Temporal start mechanisms: client starts, child starts and Schedule starts

_Original text of batch E kept for audit. Amendments and the final ruling follow it._

**Question.** RD-P1-040 and TWAC v3 rows R19 and R22 give the child starts of `ReconciliationWorkflow` and `Stage2ProductWorkflow` "conflict USE_EXISTING and reuse ALLOW_DUPLICATE". A Temporal child workflow start has no workflow-ID conflict policy: only client starts do. What is the correct mechanism, and does the 05:30 Schedule start the per-date run?

**Options considered.** (1) Keep the text. (2) Client starts keep USE_EXISTING; child starts use a deterministic workflow ID, a reuse policy and explicit handling of the already-started failure; Schedule starts go through a starter that issues a client start. Option 2.

**Sources.** TWAC v3 sheet Workflows R18 (AceIngestCheck: ID `ace-ingest-check-{businessDate}`, USE_EXISTING, ALLOW_DUPLICATE), R19 (`recon-{businessDate}`, "conflict USE_EXISTING and reuse ALLOW_DUPLICATE for the original child start"), R22 (`stage2-dp04-{businessDate}`, same), R23; sheet Schedules R12 (`rwb-source-data-ace-late-check`, 05:30, SKIP, catch-up 1 h, "Starts AceIngestCheck for the expected business date if no run is open"); sheet Platform rules R8 (ABANDON), R12 (Worker Versioning), R16 (SKIP), R18 (Temporal 1.30 or later), R22 (reruns FAIL + ALLOW_DUPLICATE_FAILED_ONLY). REG v2 RD-P1-040 item 1, item 5 as amended, XD-11. Temporal behaviour (platform facts, Temporal 1.30): `WorkflowIdConflictPolicy` is an option of a client start (and of signal-with-start) only; a child start takes a workflow ID and a `WorkflowIdReusePolicy`; when the ID is already running, or closed and the reuse policy refuses it, the child start fails (history event `StartChildWorkflowExecutionFailed` with cause `WORKFLOW_ALREADY_EXISTS`; the SDK raises its workflow-execution-already-started failure through the child's start promise); a Schedule action starts its workflow with the action's workflow ID suffixed by the scheduled time.

**Precedence applied.** RD-P1-040 (register) is amended; TWAC v3 rows follow. No higher-tier source sets a policy.

**Ruling.**
1. **Client starts of AceIngestCheck** (readiness handler, fallback poll, admin): workflow ID `ace-ingest-check-{businessDate}`, `WorkflowIdConflictPolicy` USE_EXISTING, `WorkflowIdReusePolicy` ALLOW_DUPLICATE, unchanged. The admin rerun of a FAILED run keeps FAIL + ALLOW_DUPLICATE_FAILED_ONLY (Platform rules R22).
2. **Child starts** (`ReconciliationWorkflow` `recon-{businessDate}`, `Stage2ProductWorkflow` `stage2-dp04-{businessDate}`), issued by AceIngestCheck in the workflow task that commits the ALS stamp:
   - `ChildWorkflowOptions`: the deterministic workflow ID, `ParentClosePolicy` ABANDON, `WorkflowIdReusePolicy` **ALLOW_DUPLICATE_FAILED_ONLY**, task queue `rwb-source-data`. No conflict policy is set (none exists for a child).
   - The parent waits for the child's start promise (`Workflow.getWorkflowExecution(child)` in the Java SDK) before it completes or continues, so an ABANDONed child is never lost when the parent closes.
   - When the start fails because the ID already exists (open run, or a closed COMPLETED run refused by the reuse policy), AceIngestCheck treats the child as started: it records nothing new, raises no failure and increments `rwb_source_data_duplicate_start_total` with label `workflow` = the child type. Any other start failure fails the workflow task and is retried by Temporal.
   - A closed FAILED child is never restarted by the parent; it is rerun only through `POST /admin/jobs/{jobId}/rerun` (a client start with FAIL + ALLOW_DUPLICATE_FAILED_ONLY), or before wave 4 as in RD-P1-079 rule 4.
3. **Schedule starts.** Because a Schedule suffixes its workflow ID with the scheduled time, the Schedule `rwb-source-data-ace-late-check` does not start AceIngestCheck itself. Its action starts the short workflow **`AceLateCheckStart`** (task queue `rwb-source-data`, ID `ace-late-check-start` plus the Schedule suffix), whose one activity `startIngestForExpectedDate` computes the expected business date (RD-P1-041 item 1) and issues the client start of rule 1 with `startedBy` SCHEDULE. The fallback poll, when built (GAP-3277), uses the same starter with `startedBy` POLL.
4. **Catalog rows.** TWAC v3 R19 and R22 read "child start: deterministic ID, reuse ALLOW_DUPLICATE_FAILED_ONLY, already-started treated as started; no conflict policy (child starts have none); admin rerun FAIL + ALLOW_DUPLICATE_FAILED_ONLY". R18 keeps its policies. A new Workflows row `AceLateCheckStart` (P1, kind "Schedule starter", activity `startIngestForExpectedDate`) and a new Activities row are added; Schedules R12 reads "starts AceLateCheckStart, which starts or attaches to AceIngestCheck for the expected business date".
5. **Reuse rule (amends the RD-P1-040 reuse note).** "Every system-started workflow uses USE_EXISTING + ALLOW_DUPLICATE" applies to client starts only. In-service child starts use a deterministic ID, ALLOW_DUPLICATE_FAILED_ONLY and the already-started handling of rule 2. Schedule-started per-date work goes through a starter activity.

**Rationale.** Uses only options Temporal offers for each start kind; keeps one run per date even when the Schedule fires; keeps XD-11's "never a second ReconciliationWorkflow" true by the reuse policy, not by convention.

**Affected services.** rwb-source-data; every service that starts child workflows or Schedule-started per-date work (reuse).
**Affected stories.** RWB-P1-E1015-APP, RWB-P1-E1015-OPS, RWB-P1-E1011-APP, RWB-P1-E2010-APP, RWB-P1-E2010-OPS, RWB-P1-AD019-APP, RWB-P1-E1013-APP, RWB-P1-AD018-APP, RWB-ITG-E1015-ITG.
**Affected documents.** Temporal Workflow and Activity Catalog v3 (R18 note, R19, R22, Schedules R12, two new rows); Batch and Scheduling Design v7 (JOB-04 and the 05:30 row); register RD-P1-040 and RD-P1-002 (amendment lines); Test Cases v9 (child start duplicate case).
**GAP/ASM.** None closed; GAP-3277 unchanged.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** Client start: USE_EXISTING + ALLOW_DUPLICATE. Child start: deterministic ID + ALLOW_DUPLICATE_FAILED_ONLY + already-started = started. Schedule: start a starter, never the per-date workflow.
**Values chosen without a source.** Workflow type `AceLateCheckStart`, activity `startIngestForExpectedDate`, ID prefix `ace-late-check-start`, label `workflow` on the duplicate metric.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-079 · Readiness after the run closes, the readiness recorder and restarts before wave 4

_Original text of batch E kept for audit. Amendments and the final ruling follow it._

**Question.** XD-11 (register v2) merged RD-P1-040 item 1 and RD-P1-065 rule 3 and asked for confirmation; TWAC v3 R18 still says "DONE or LATE starts nothing". Who writes `business_day_readiness` transitions for starts that are not HTTP (RR E1013-APP#1)? How is a date recovered when its ingest run failed or closed before the ALS batch arrived, before the AD018 rerun exists (RR E1013-APP#8; GAP-3390)?

**Sources.** REG v2 XD-11, RD-P1-040 item 1 (24 h close), RD-P1-065 rule 3, RD-P1-020 F (`business_day_readiness`, DF-OPS-252 to DF-OPS-257, state LOV-READINESS RUNNING/DONE/LATE, written by RWB-P1-E1013-APP), RD-P1-022 (readiness pair E1013-APP; AceIngestCheck E1015-APP), X-17 and NEW-ASM-X4 (restart before wave 4 by a repeated ready call or the poll); TWAC v3 R18; PS v9 `business_day_readiness` seed rows.

**Ruling.**
1. **XD-11 confirmed, with the mechanism.** On `POST /business-days/{date}/ready`:
   - (a) a run `ace-ingest-check-{date}` is open → the client start (USE_EXISTING) attaches; answer 202 with the stored state;
   - (b) no run is open and every due source of the date has its stamp row (`data_product_load` for the products it feeds) → nothing is started; answer 202 with the stored state;
   - (c) no run is open and a due source is not stamped (never started, the run FAILED, or the run closed at 24 h) → a new run opens (ALLOW_DUPLICATE) and stamps only the missing sources; `job_run.run_no` + 1 when AD018 is live.
   The check of (b) is the in-process `DailyCompletenessGate` source set of the date read by the handler. No second AceDataReady for a stamped source; no second ReconciliationWorkflow (RD-P1-078 rule 2).
2. **TWAC v3 R18** replaces "DONE or LATE starts nothing" with rule 1 (a)-(c). RD-P1-065 rule 3 reads with this rule.
3. **Readiness recorder (E1013-APP#1).** RWB-P1-E1013-APP builds the in-process component `ReadinessRecorder` with two methods, each idempotent and run inside the caller's transaction:
   - `recordReceived(businessDate, startedBy)` – upsert on `uk_business_day_readiness`; first insert state RUNNING, `received_at` now. Called by the ready handler (HTTP) and by the first activity of every AceIngestCheck run started otherwise (SCHEDULE, POLL, ADMIN).
   - `recordState(businessDate, DONE | LATE)` – called by RWB-P1-E1015-APP inside the `stampProducts` transaction that commits the ALS stamp (DONE) and inside the transaction that writes the ALS AceDataLate outbox row (LATE); sets `changed_at`. LATE may become DONE when ALS is stamped later; DONE never changes back.
   RWB-P1-E1015-APP adds both calls to section 4 and its workflow contract; the E1015-CON workflow note names them.
4. **Restart before wave 4 (GAP-3390).** Until RWB-P1-AD018 is released:
   - AceIngestCheck: rule 1 (c) is the restart: a repeated ready call (or the fallback poll where enabled) opens a new run for a date with an unstamped due source. The readiness row keeps its state until the new run writes DONE.
   - A FAILED `ReconciliationWorkflow` or `Stage2ProductWorkflow`: the platform administrator (RW-PLATADM) starts the same workflow ID with the Temporal CLI under runbook entry "P1 run failed before wave 4", reuse policy ALLOW_DUPLICATE_FAILED_ONLY, input `{businessDate, startedBy: ADMIN}`, and records the action in the release record. A COMPLETED run is never restarted. From wave 4 the admin rerun of RD-P1-012 replaces the runbook step.
   GAP-3390 is closed by this rule.

**Affected services.** rwb-source-data.
**Affected stories.** RWB-P1-E1013-APP, RWB-P1-E1015-APP, RWB-P1-E1015-CON, RWB-P1-E1015-OPS, RWB-P1-E1011-APP, RWB-P1-E2010-APP, RWB-P1-E2010-OPS, RWB-P1-AD018-APP, RWB-ITG-E1013-ITG, RWB-ITG-E1015-ITG.
**Affected documents.** Temporal Workflow and Activity Catalog v3 (R18 text); Observability and Monitoring Design v6 (runbook entry); register RD-P1-040, RD-P1-065 (amendment lines; XD-11 confirmed); Gap Register v3 (GAP-3390 closed); Assumptions Register v3 (ASM-5707 unchanged; NEW-ASM-X4 confirmed with rule 4).
**Findings settled.** RWB-P1-E1013-APP#1, RWB-P1-E1013-APP#8 (re-review).
**GAP/ASM.** Closes GAP-3390.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** A repeated start opens a new run only for work not yet done; never re-run done work by a start call.
**Values chosen without a source.** Component and method names; runbook step for wave 3 and earlier.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-080 · Flag-off answers: freshness never 404; 404 MSG-P4-003 for other flagged operations

_Original text of batch E kept for audit. Amendments and the final ruling follow it._

**Question.** RD-P1-043 (Section B flag `rwb.dataengine.freshness-stamp` off: ready 202, status LATE, freshness STALE with null date) and RD-P1-045 item 4 (first-release rollback: "the api answers 404 on the flagged operations") give two answers for the same flag; RWB-P1-E1015-OPS AC5 and AC21 disagree and the YAML freshness read has no 404 (RR E1015-OPS#1). Which message does a flagged-off 404 carry, and does the ledger-writer flag gate the in-process writer (GAP-3506)?

**Sources.** REG v2 RD-P1-043 item 3, RD-P1-045 item 4, RD-P1-062 (never-stamped answer); YAML `/data-products/freshness` (no 404), `/admin/jobs` ("While the flag rwb.p1.jobmonitor is off both job operations answer 404 MSG-P4-003 (RD-P1-045)"), `/admin/reconciliation/results` (same), `/proof-of-delivery` (flag off: 200 with no row and DP07 STALE); RWB-P1-E1015-OPS lines 85, 101, 150-155, 216-221; RWB-P1-E1015-APP AC40; EMS v6 MSG-P4-003.

**Ruling.**
1. **Freshness and readiness never answer 404 because of a flag.** For `rwb.dataengine.freshness-stamp` off – before the ACE dependency gate and after a first-release rollback alike – `GET /data-products/freshness` answers 200 with every product `businessDate` null, status STALE (RD-P1-043 item 3(c), RD-P1-062); `GET /business-days/{date}/status` answers LATE for a date with a readiness row (404 MSG-P4-003 only for a date with no row, RD-P1-020 F); `POST /business-days/{date}/ready` answers 202 and records the readiness row (RD-P1-079 rule 3) but **starts no AceIngestCheck** while the flag is off, so no run queues while the worker is at zero. AceIngestCheck keeps its own guard (RWB-P1-E1015-APP AC40: a run that starts with the flag off writes no stamp, event or child).
2. **Other flagged operations.** An operation behind a flag with no flag-off answer ruled in an RD-P1 decision answers **404 MSG-P4-003** while its flag is off (the YAML form already used for the job monitor and the reconciliation results). Reads whose flag-off answer is ruled keep it: `GET /proof-of-delivery` (200, no row, DP07 STALE).
3. **First-release rollback (amends RD-P1-045 item 4).** Flag off; worker scaled to zero; the release's Schedules paused; operations answer as in rules 1 and 2. RWB-P1-E1015-OPS AC21 reads "the readiness and freshness operations answer as in AC5 and every other flagged operation of the release answers 404 MSG-P4-003".
4. **Ledger-writer flag (GAP-3506).** `rwb.dataengine.ledger-writer` gates the REST append path only (404 MSG-P4-003). In-process callers are gated by their own flags: `rwb.dataengine.ledger-events` (intake consumers paused, RWB-P1-E1067-APP), the DM005 cutover switch (RWB-P1-DM005-APP), RWB-P1-E2034-APP's own flag. GAP-3506 is closed.

**Affected services.** rwb-source-data; consumers of freshness (no change).
**Affected stories.** RWB-P1-E1015-OPS, RWB-P1-E1015-APP, RWB-P1-E1015-CON, RWB-P1-E1013-APP, RWB-P1-E1066-APP, RWB-P1-E1066-OPS, RWB-P1-E2001-APP, RWB-P1-E2007-APP, RWB-P1-E1011-OPS, RWB-P1-E1017-OPS, RWB-P1-E2010-OPS, RWB-P1-AD019-OPS.
**Affected documents.** API Specification v7 `rwb-source-data.yaml` (descriptions of the flagged operations: "404 MSG-P4-003 while <flag> is off"); register RD-P1-043 and RD-P1-045 (amendment lines); Gap Register v3 (GAP-3506 closed); Test Cases v9 (TC-P1-E1015-OPS-19 and the AC21 row).
**Findings settled.** RWB-P1-E1015-OPS#1 (re-review).
**GAP/ASM.** Closes GAP-3506.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** A read that gates other services' work answers "no data" when flagged off, never 404; every other flagged-off operation answers 404 MSG-P4-003.
**Values chosen without a source.** Ready call starts no run while the flag is off.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-081 · ON_CHANGE products and the DP04 stamp; active-count check; DP04 record selection

_Original text of batch E kept for audit. Amendments and the final ruling follow it._

**Question.** RD-P1-041 item 4 sets the stamp in use STALE at `expected_by` and its GAP lines close GAP-0511 as "DP04: STALE at expected_by 08:00"; RD-P1-068 rule 6 says DP04 is ON_CHANGE, stamped when its core-bank source completes, never STALE by time. `stampProducts` of AceIngestCheck and `stampDp04` of Stage2ProductWorkflow both claim the DP04 row (GAP-3525). The active-count check compares a window of changed rows with an unwindowed count (GAP-3524). Which row per treatment does the DP04 records read answer (RR E2010-APP#6, E2010-CON#7)?

**Sources.** REG v2 RD-P1-041 items 3, 4, 7 and GAP lines, RD-P1-068 rule 6, RD-P1-002 (Stage2ProductWorkflow activities); PS v9 `data_product` seed line 904 (DP04 ON_CHANGE, "As it changes"; DP03 line 903 ON_CHANGE), `data_product_source` seed lines 2429-2431 (no DP04 row; core-bank code Pending ASM-5695), `dp_treatment` (`uk_dp_treatment (business_date, treatment_id)`), `dp_guarantee_claim`; CASE-YAML / PS v9 `rwb_case.case_account.is_primary`, `linked_to`; TWAC v3 R22; RWB-P1-E2010-APP s4 steps 1-6; GR v3 GAP-2696 (Accepted (directive): active states held as a parameter row).

**Precedence applied.** RD-P1-068 (later, specific) prevails over RD-P1-041 for ON_CHANGE products. **Amends RD-P1-041** (item 4 scope; item 7 writer; GAP-0511 line) and **RD-P1-068 rule 6** (when the DP04 row is written).

**Ruling.**
1. **STALE by time applies to DAILY and WEEKLY products only.** RD-P1-041 item 4's `expected_by` trigger never runs for a product whose `refresh_cycle` is ON_CHANGE (DP03, DP04). The FAILED trigger still applies to an ON_CHANGE product that has a mapped source. The "Closes GAP-0511 (DP04: STALE at expected_by 08:00 …)" line of RD-P1-041 now reads "GAP-0511 closed by RD-P1-068: DP04 is ON_CHANGE and never STALE by time".
2. **One stamp component.** `data_product_load` is written only by the stamp component of RWB-P1-E1015-APP (`FreshnessStampWriter`, in process). `stampProducts` (AceIngestCheck) calls it for products whose `refresh_cycle` is DAILY or WEEKLY and that have at least one `data_product_source` row; it never stamps an ON_CHANGE product. `stampDp04` (Stage2ProductWorkflow, RWB-P1-E2010-APP) is the only caller that stamps DP04. GAP-3525 is closed.
3. **When DP04 is stamped (amends RD-P1-068 rule 6).** Stage2ProductWorkflow for D starts as a child in the workflow task that commits the ALS stamp (TWAC v3 R22). `stampDp04` writes the DP04 row for D (status LOADED, `source_system` `WORKBENCH`, `source_extracted_at` = the ALS `completed_at` of D, `loaded_at` = write instant) after every DP04 page of D is committed. When the core-bank code of ASM-5695 is confirmed and a DP04 `data_product_source` row is seeded, Stage2ProductWorkflow waits (durable timer, `ingest.poll.interval.minutes`) for that source to be COMPLETED for D before `stampDp04`; until then it does not wait.
4. **Active-count check (GAP-3524).** The comparable population is: for each `treatment_id`, the `dp_treatment` row with the greatest `business_date` ≤ D, counted when its state is active. Active states are the parameter row GAP-2696 names, **Pending, owner rwb-treatment owner with RW-COE** (GAP-3524 narrowed to the states). Interim: `checkActiveCount` runs in report mode – on a difference it lists the break with MSG-P1-002 and the count in the run result, but it does not hold `stampDp04`. The hold is switched on by the story change that closes GAP-3524.
5. **DP04 records read selection (E2010-APP#6, E2010-CON#7).** `GET /data-products/DP04/records?caseId=` answers, per `treatment_id` and per `guarantee_claim_id` of the case, the row with the greatest `business_date` ≤ the business date of the DP04 stamp in use. `recordId` = `treatment_id` or `guarantee_claim_id` (not the row `id`); `entity` = `dp_treatment` or `dp_guarantee_claim`. The contract number, contract date and plan terms are joined at request time from `v_ace_account` / `v_ace_plan` on the case's primary account: the `case_account` row with `is_primary` true and `linked_to` null, read through the rwb-case contract. Rows of a date later than the stamp in use (an unfinished or failed build) are never answered.
6. **Stories.** RWB-P1-E2010-APP, -CON and -OPS remove every "08:00 / expected_by / STALE from the expected-by time" statement for DP04 (s3, X3, s13, s19, AC4, AC5, BR4, s14; TC-P1-E2010-APP-08, TC-P1-E2010-CON-04, -12) and cite this decision; the E2010-OPS smoke asserts only that the DP04 row is written by `stampDp04` after the ALS stamp.

**Affected services.** rwb-source-data; rwb-treatment (parameter row).
**Affected stories.** RWB-P1-E2010-APP, RWB-P1-E2010-CON, RWB-P1-E2010-OPS, RWB-P1-E1015-APP, RWB-P1-E1015-CON, RWB-P1-DM004-APP, RWB-S2-E2010-APP, RWB-ITG-E2010-ITG.
**Affected documents.** Temporal Workflow and Activity Catalog v3 (R22 steps; Activities R22 `stampProducts` scope); register RD-P1-041, RD-P1-068, RD-P1-002 (amendment lines); API Specification v7 `rwb-source-data.yaml` (records read description for DP04); Gap Register v3 (GAP-3525 closed, GAP-3524 narrowed, GAP-0511 closure text); Test Cases v9.
**Findings settled.** RWB-P1-E2010-APP#1, #3, #4, #6; RWB-P1-E2010-CON#1, #2, #7; RWB-P1-E2010-OPS#2 (re-review).
**GAP/ASM.** Closes GAP-3525; narrows GAP-3524 (blocks build: No with the interim).
**Status.** Proposed – Claude Opus 5.5 (applied); active states pending under GAP-3524.
**Reuse note.** A derived product is stamped by its build, through the single stamp component, and only ACE-fed DAILY/WEEKLY products go STALE by time.
**Values chosen without a source.** `FreshnessStampWriter` name; `source_system` WORKBENCH and the time columns of the DP04 row; report-mode interim; latest-row-per-ID population.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-082 · DP04 build reads, rerun and the records read value formats

_Original text of batch E kept for audit. Amendments and the final ruling follow it._

**Question.** RWB-P1-E2010-CON uses `page=0&size=1000` for the treatment and claim reads while RWB-S2-E2010-APP and RWB-S3-E2010-APP refuse "a page below one" (RR E2010-CON#3). What happens on a rerun to rows absent from the new answer and to pages committed before a failure (GAP-3523)? What are the string forms of `FieldValue.value`, the order and the `total` of the records read (RR E2010-CON#6; GAP-0512, GAP-3528, GAP-3571)?

**Sources.** YAML (every page parameter `minimum: 0, default: 0`; `JobPage`, `InteractionPage`, `DataProductRecordPage` {items, page, size, total}; `FieldValue.value` string, non-null); CASE-YAML (page `minimum: 0`); GR v3 GAP-2696 and GAP-2738 (Accepted (directive): window reads with page, size, total, maximum 1000, 400 on an empty or inverted window, order `updated_at` then `id`); PS v9 `dp_treatment` (numeric(18,2), timestamptz, date columns, `updated_at`).

**Ruling.**
1. **Page base.** Every page of the Recovery Workbench REST contracts is zero-based (`page` minimum 0, default 0), as every published page in API Specification v7. The rwb-treatment read `GET /treatments?changedFrom=&changedTo=&page=&size=` and the rwb-guarantee read `GET /guarantee-claims?changedFrom=&changedTo=&page=&size=` take `page` from 0, `size` 1 to 1000 (default 1000 for the DP04 build), answer {items, window, page, size, total}, order `updated_at` then `id`, and answer 400 MSG-GEN-003 on an inverted window and 400 MSG-GEN-001 on a missing bound; an empty window [D, D+1) with no row answers 200 with `items` empty. RWB-S2-E2010-APP and RWB-S3-E2010-APP change "a page below one" to "a page below zero".
2. **Rerun and visibility (GAP-3523).** A FAILED run's committed pages stay; they are invisible because the records read answers only rows dated ≤ the DP04 stamp in use (RD-P1-081 rule 5) and a failed run writes no stamp. The rerun upserts by (`business_date`, record ID), then, before `stampDp04`, deletes the rows of business date D (both tables) whose `updated_at` is earlier than the rerun's start instant – the rows its answer no longer contains. GAP-3523 is closed.
3. **Value formats of `FieldValue.value` (records read, every product).** Timestamp: ISO 8601 with offset `+07:00` (Asia/Bangkok), seconds precision. Date: `yyyy-MM-dd`. Numeric: plain decimal string with the scale of the physical type (`numeric(18,2)` → `300000.50`), no grouping, `.` as separator. Boolean: `true` / `false`. Integer: decimal digits. A null column: the `FieldValue` is omitted. A masked field: `value` = the masked form, `masked` true. GAP-0512 and GAP-3528 are closed; GAP-3571 (physical types of uncast view columns) stays open for the ACE data owner but no longer blocks: the format follows the type the view returns.
4. **Order and total (GAP-3528).** Items ordered by `entity`, then `recordId`, ascending; `total` = number of `DataProductRecord` items over all pages (not field values).

**Affected services.** rwb-source-data; rwb-treatment; rwb-guarantee.
**Affected stories.** RWB-P1-E2010-CON, RWB-P1-E2010-APP, RWB-S2-E2010-APP, RWB-S3-E2010-APP, RWB-P1-E1016-APP, RWB-P1-E1016-CON, RWB-ITG-E2010-ITG.
**Affected documents.** API Specification v7 `rwb-source-data.yaml` (`FieldValue.value` description; records read order and total), `rwb-treatment.yaml` and `rwb-guarantee.yaml` (when the two reads are published, CDC-03577 and GAP-2738); Gap Register v3 (GAP-3523, GAP-0512, GAP-3528 closed; GAP-3571 non-blocking).
**Findings settled.** RWB-P1-E2010-CON#3, RWB-P1-E2010-CON#6 (re-review).
**GAP/ASM.** Closes GAP-3523, GAP-0512, GAP-3528.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** Zero-based pages everywhere; dated snapshot rows are made invisible by the stamp, not by transactions spanning pages.
**Values chosen without a source.** Claim-read maximum 1000; delete-by-`updated_at` rule; string formats; order key.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-083 · Freshness stamp edge cases: missing batch row, re-completion, restatement detection, weekly-only sources, gate value

_Original text of batch E kept for audit. Amendments and the final ruling follow it._

**Question.** (a) AceDataLate `status` is required and "copied unchanged" from `v_ace_batch_status`, but a source may have no row (GAP-3430; RR E1015-APP#1, E1015-CON#1). (b) A date D whose row went STALE after a failure completes again, but `uk_data_product_load (product_code, business_date)` forbids a second row (RR E1015-APP#2). (c) How is a changed `completed_at` detected for a multi-source product (GAP-3429)? (d) Which run holds the timer and late event of a weekly-only source (GAP-3288)? (e) Where is the gate value COMPLETE/HOLD over REST (GAP-3434)?

**Sources.** ASYNC lines 186-222 (AceDataReady and AceDataLate payloads); PS v9 `recovery_views.sql` lines 498-510 (`v_ace_batch_status`), `data_product_load` (lines 185-203); PS v9 `data_product_source` seed (DP06: CCMS, SVAF, AMIS, RPS – weekly only); REG v2 RD-P1-040 item 1 ("a source is due on a date when it feeds a DAILY product, or a WEEKLY product whose cycle day that is") and item 3, RD-P1-041 items 1, 4-6; YAML `/data-products/freshness` (array of `DataProductFreshness`).

**Ruling.**
1. **No batch row (GAP-3430).** In ASYNC 5.1.0 AceDataLate `data.status` becomes `type: [string, "null"]`, still required: the `v_ace_batch_status` value copied unchanged, **null when the source has no batch row for the date**; `completedAt` stays null. AceDataReady is unchanged (always a row). RWB-P1-E1015-APP AC41 and RWB-P1-E1015-CON AC17 and the sample assert `status: null`. GAP-3430 is closed.
2. **Re-completion of a STALE date (E1015-APP#2).** When (P, D) already has a row that went STALE (failed after completed) and every mapped source is COMPLETED again for D, the existing row is **updated in place**: status LOADED, `stale_flagged_at` null, `source_extracted_at` = the new latest `completed_at`, `loaded_at` = update instant, `duplicate_count` + 1, `version` + 1. No second AceDataReady, no child start (RD-P1-079 rule 1); the operations duplicate alert fires (restated batch runbook entry). RWB-P1-E1015-APP s4 step 7 and a new state row and AC state this.
3. **Restatement detection (GAP-3429).** While the run of D is open, a restatement is detected when the latest `completed_at` among P's sources differs from `source_extracted_at` of P's row for D (RD-P1-041 item 6 then applies). A restatement of a source whose new time stays below the product's latest time, and any restatement after the run has closed, is not detected by P1 in version 1. AC35 asserts the open-run case on the latest source. GAP-3429 stays open for the per-source store, **blocks build: No**.
4. **Weekly-only sources (GAP-3288).** A source that feeds only a WEEKLY product is due in the AceIngestCheck run whose start day in Asia/Bangkok is the product's cycle weekday (DP06: Monday, from `expected_by` MON 08:00), i.e. the run of the latest bank business day before that day. That run raises AceDataLate for the source at 05:30 of the cycle day with that business date and holds DP06's `expected_by` timer (MON 08:00). Other runs neither poll nor raise anything for the source. GAP-3288 is closed; confirmation of the cycle-day rule by the ACE team lead is recommended.
5. **Gate value over REST (GAP-3434).** No gate member is added to `GET /data-products/freshness`. `DailyCompletenessGate` is in-process only (`listEligibleAccounts`, `/efs-history`, reconciliation, AD019); a REST caller uses the per-product `status` and `GET /business-days/{date}/status`. RWB-P1-E1015-CON removes the REST gate assertion. GAP-3434 is closed.

**Affected services.** rwb-source-data; AceDataLate consumers (alerts, gateway-bff banner).
**Affected stories.** RWB-P1-E1015-APP, RWB-P1-E1015-CON, RWB-P1-E1015-OPS, RWB-P1-E1013-APP, RWB-ITG-E1015-ITG.
**Affected documents.** `asyncapi/rwb-source-data.asyncapi.yaml` (AceDataLate status nullable); Event and Messaging Design v7 / Kafka Topic and Event Catalog v3 (EV-27 status note); Gap Register v3 (GAP-3430, GAP-3288, GAP-3434 closed; GAP-3429 non-blocking); Test Cases v9.
**Findings settled.** RWB-P1-E1015-APP#1, #2; RWB-P1-E1015-CON#1 (re-review).
**GAP/ASM.** Closes GAP-3430, GAP-3288, GAP-3434.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** Null, never an invented code, for a value the source does not have; one row per key, updated in place on re-completion.
**Values chosen without a source.** Nullable status; in-place update; cycle-day run rule; version 1 detection limit.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-084 · Proof-of-delivery: incomplete WIN date and the contract publisher

_Original text of batch E kept for audit. Amendments and the final ruling follow it._

**Question.** How does `GET /proof-of-delivery` show a date whose WIN batch is incomplete, with no answer member for it (RR E1055-APP#1)? Which story publishes `getProofOfDelivery` and its fake (RR E1055-APP#14)?

**Sources.** YAML `/proof-of-delivery` ("RWB-P1-E1055-APP … only when the WIN batch of the date is COMPLETED … the answer has no member for the reason (Pending: GAP-0579)"), `ProofOfDeliveryAnswer` {businessDate, productCode DP07, freshness, rows}; PS v9 `data_product_source` (DP07: LIT, WIN); RWB-P6-E1055-APP X2; REG v2 RD-P1-011 (fakes), RD-P1-022 (contract homes).

**Ruling.**
1. **Incomplete date.** No member is added. The answer carries `freshness` = DP07 stamp in use. rwb-comms treats the requested `businessDate` as incomplete when `freshness.businessDate` is null or earlier than the requested date, or `freshness.status` is STALE; it then appends no delivery entry and reads again on its next poll. `rows` is empty in that case. RWB-P1-E1055-APP adds the AC; RWB-P6-E1055-APP X2 reads the same rule.
2. **Publisher.** `getProofOfDelivery` is published in **RWB-P1-E1015-CON** (the freshness-and-read surface, as for the other P1 reads, X-27) and built by RWB-P1-E1055-APP; the fake (RD-P1-011) has three examples: complete date with rows, incomplete date (businessDate earlier, rows empty), flag off. RWB-P1-E1055-APP s20 "CON Done" points to RWB-P1-E1015-CON; RWB-P6-E1055-APP's contract dependency changes from RWB-P1-E1055-APP to RWB-P1-E1015-CON.

**Affected stories.** RWB-P1-E1055-APP, RWB-P1-E1015-CON, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-ITG-E1055-ITG.
**Affected documents.** API Specification v7 `rwb-source-data.yaml` (description: publisher and incomplete-date rule); Service Contract Catalog v3 (row of `getProofOfDelivery`); Story Build Order v5 / Dependency Map v7 (dependency edge).
**Findings settled.** RWB-P1-E1055-APP#1, #14 (re-review).
**GAP/ASM.** GAP-0579 closed by rule 1 (the reason member is not needed).
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** A consumer decides completeness from the freshness stamp it is given; consumers depend on CON stories, never on APP stories.
**Values chosen without a source.** None beyond rule 2's choice of contract home.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-085 · `GET /batch-status` with no batch row: 404 MSG-P1-001 (directive exception)

_Original text of batch E kept for audit. Amendments and the final ruling follow it._

**Question.** RD-P1-004's status table maps "record missing or outside scope" to 404 MSG-P4-003; the YAML and GAP-0597 answer 404 MSG-P1-001 for a source and date with no batch row; RWB-P2-E2007-APP and -CON say MSG-P4-003 (RR E2007-APP#2).

**Sources.** GR v3 GAP-0597 (Resolved (directive), D-RCV-60: "answer 404 with MSG-P1-001 when no batch row exists for the source and date"); YAML `/batch-status` 404; REG v2 RD-P1-004 status table; EMS v6 MSG-P1-001 ("Data product stale after a late or failed batch").

**Precedence applied.** D-RCV-60 directive resolution (top tier, as X-27) over RD-P1-004. **Amends RD-P1-004** (one recorded exception).

**Ruling.** `GET /batch-status` answers **404 MSG-P1-001** when `v_ace_batch_status` has no row for the source and date: the batch has not arrived, which is a freshness state, not a missing record. This is the one exception to the RD-P1-004 status table; 404 MSG-P4-003 keeps its meaning everywhere else. RWB-P2-E2007-APP and RWB-P2-E2007-CON (line 266) change to MSG-P1-001; RWB-P1-E2007-APP AC13 and X12 keep it.

**Affected stories.** RWB-P1-E2007-APP, RWB-P2-E2007-APP, RWB-P2-E2007-CON, RWB-ITG-E2007-ITG, RWB-P8-E4050-APP (caller of `getBatchStatus`).
**Affected documents.** Register RD-P1-004 (amendment line); API Specification v7 (no change).
**Findings settled.** RWB-P1-E2007-APP#2 (re-review).
**GAP/ASM.** GAP-0597 confirmed.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** A source batch not yet arrived is MSG-P1-001 in every answer, whatever the status code.
**Values chosen without a source.** None.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-086 · Reconciliation results: REC-05 aggregate row, result page, alert values, rwb-case inputs

_Original text of batch E kept for audit. Amendments and the final ruling follow it._

**Question.** Consumers read a "REC-05 aggregate for the date" (RWB-P8-E4050-APP s12, RWB-P3-AD019-APP, RWB-P1-DM009-APP s12.8), and the DM clean-day rule needs "no new REC-05 orphan", while RWB-P1-E1011-CON s11 says REC-05 is not inserted and the YAML `recCode` enum is REC-01, REC-02 (RR E1011-CON#3). The result page envelope is Pending (GAP-3412; RR AD019-APP#1). Alert selectors, ticket channel and thresholds are Pending (GAP-3418, GAP-3421, GAP-3422; RR E1011-OPS#5). The rwb-case allocation and exclusion paths are unpublished (GAP-3411).

**Sources.** PS v9 `reconciliation_result` (lines 326-347; `uk_reconciliation_result (rec_code, business_date, product_group)`); YAML `/admin/reconciliation/results` and `ReconciliationResultPage` (Pending), `/admin/jobs` (page 0-based, size default 50 max 200, from default today minus 7 days, `JobPage`); REG v2 RD-P1-022 (P1 computes REC-01, REC-02, REC-05), RD-P1-042 (tolerance 0.00, clean day), RD-P1-069 (aggregates only); BSD v7 JOB-04; data_product `expected_by` 08:00 (DL11).

**Ruling.**
1. **REC-05 is served as one aggregate row per business date** in `reconciliation_result`: `rec_code` REC-05, `product_group` `ALL`, `source_count` = keys checked, `workbench_count` = keys resolved, `variance_count` = orphan keys, `variance_pct` = orphans / keys checked × 100 (0 when none checked), `tolerance_pct` 0.0000, `result` PASS when `variance_count` = 0, else BREAK. The YAML `recCode` enum becomes [REC-01, REC-02, REC-05]; the LOV of `product_group` for results adds `ALL` (Reference Data and Lists of Values v6). RWB-P1-E1011-CON s11 drops "Do not … insert REC-05". Orphan key detail stays Pending (GAP-1508, GAP-3413). The DM clean day reads "every REC-01, REC-02 and REC-05 row of the date PASS" (RD-P1-093 rule 5).
2. **Result page (GAP-3412).** `ReconciliationResultPage` = {items: ReconciliationResult[], page, size, total}, required all four; `page` minimum 0 default 0, `size` 1 to 200 default 50; `from` default today minus 7 days, `to` default today (Asia/Bangkok, inclusive, on `business_date`); order `business_date` descending, then `rec_code`, then `product_group`; 422 MSG-GEN-002 for size out of range, 422 MSG-GEN-003 for `from` after `to`. The fake and AD019-APP AC1, AC9 use it. GAP-3412 is closed.
3. **Alerts (GAP-3418, GAP-3421, GAP-3422).** Interim values-file entries of rwb-source-data, armed only while the reconciliation flag is on: break alert on any REC-01, REC-02 or REC-05 BREAK row of the date (consistent with tolerance 0.00); JOB-04 not-completed alert when no ReconciliationWorkflow of D is COMPLETED by 08:00 Asia/Bangkok; route to the P1 squad channel of the values file; ticket channel blank (no ticket) until the owner fills it. The three gaps stay open for the operational owner, **blocks build: No**.
4. **rwb-case inputs (GAP-3411).** Until rwb-case publishes the allocation and exclusion paths and the dated REC-02 open-case input, the reconciliation is built and tested against the rwb-case contract fake with the shapes named in RWB-P1-E1011-CON; the reconciliation flag stays off outside DEV and SIT. GAP-3411 stays open, owner rwb-case service owner, **blocks build: No**.

**Affected services.** rwb-source-data; rwb-payment, rwb-case (readers).
**Affected stories.** RWB-P1-E1011-APP, RWB-P1-E1011-CON, RWB-P1-E1011-OPS, RWB-P1-AD019-APP, RWB-P1-AD019-OPS, RWB-P1-DM003-APP to RWB-P1-DM010-APP (clean day), RWB-P8-E4050-APP, RWB-P3-AD019-APP, RWB-ITG-E1011-ITG, RWB-ITG-AD019-ITG.
**Affected documents.** API Specification v7 `rwb-source-data.yaml` (`recCode` enum, `ReconciliationResultPage`, parameters); Reference Data and Lists of Values v6 (`ALL`); Observability and Monitoring Design v6 (reconciliation break and JOB-04 rows); Gap Register v3 (GAP-3412 closed; GAP-3418, GAP-3421, GAP-3422, GAP-3411 non-blocking).
**Findings settled.** RWB-P1-E1011-CON#3, RWB-P1-AD019-APP#1, RWB-P1-E1011-OPS#5 (re-review).
**GAP/ASM.** Closes GAP-3412.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** Every P1 page is {items, page, size, total}, 0-based, 50/200; a check without detail is still an aggregate row.
**Values chosen without a source.** `product_group` ALL; REC-05 column mapping; 08:00 not-completed boundary; sort order.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-087 · Ledger writer refusals and the actor check

_Original text of batch E kept for audit. Amendments and the final ruling follow it._

**Question.** What status and messageCode does the writer answer for a DECISION_TAKEN append without `decisionLogId`, with an unknown entry, or when the decision-log read does not answer (GAP-3487)? For a future `occurredAt` and a `correctsEntryId` that names an unknown entry or one of another case (GAP-3489)? For a service identity other than rwb-case whose case read answers 404, and must a user token's `actorRef` equal its subject (GAP-3492)? (RR E1066-APP#1, E1066-CON#1.)

**Sources.** RWB-P1-E1066-APP v3 s4 steps 3, 5, 6, X4, X6, X9, AC16, AC17, s12.2; EMS v6 MSG-GEN-001, MSG-GEN-003, MSG-GEN-007, MSG-P4-002, MSG-P4-003, MSG-P1-022; REG v2 RD-P1-004 (status table), RD-P1-007 rule 5, RD-P1-009 (actor form `USER:` / `SERVICE:` / `PARTNER:`).

**Ruling.** Nothing is written in any refusal.
1. **DECISION_TAKEN (GAP-3487).** No `decisionLogId` → 422 MSG-GEN-001, `field` decisionLogId. The decision-log read answers 404, or the entry's `caseId` is not the path case → 422 MSG-GEN-007, `field` decisionLogId. The read does not answer in 2 s or answers 503 → 503 MSG-P1-022 (as X6). GAP-3487 is closed.
2. **CORRECTION (GAP-3489).** `correctsEntryId` unknown or of another case → 422 MSG-GEN-007, `field` correctsEntryId.
3. **Future occurredAt (GAP-3489).** `occurredAt` later than the server receipt instant plus `ledger.occurred-at.future-tolerance.seconds` (values file, 300) → 422 MSG-GEN-003, `field` occurredAt. GAP-3489 is closed.
4. **Other service identities (GAP-3492).** A service identity other than rwb-case whose case read answers 404 or 403 gets 404 MSG-P4-003, as a user caller (X4).
5. **Actor check (GAP-3492).** For a delegated user token (a token with a user subject), `actorType` must be USER and `actorRef` must equal the token's Workbench user identifier; otherwise 403 MSG-P4-002. For a workload token, `actorType` and `actorRef` are stored as sent (the calling service vouches; RD-P1-009). GAP-3492 is closed; confirmation by compliance is recommended.
6. The provider fake of RWB-P1-E1066-CON s12.8 maps each of these refusals.

**Affected stories.** RWB-P1-E1066-APP, RWB-P1-E1066-CON, RWB-P1-E1067-APP (in-process mapping, RD-P1-088), RWB-P3-E1066-APP, RWB-ITG-E1066-ITG.
**Affected documents.** API Specification v7 `rwb-source-data.yaml` (`POST /cases/{caseId}/interactions` description and 422 rows); Gap Register v3 (GAP-3487, GAP-3489, GAP-3492 closed); Test Cases v9 (AC16, AC17 rows).
**Findings settled.** RWB-P1-E1066-APP#1, RWB-P1-E1066-CON#1 (re-review).
**GAP/ASM.** Closes GAP-3487, GAP-3489, GAP-3492.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** A body reference that does not resolve is 422 MSG-GEN-007 naming the field; a downstream that does not answer is 503 with the owner's write-failed code.
**Values chosen without a source.** MSG-GEN-007 and MSG-GEN-003 for these cases; 300 s tolerance and its key; actor equality rule.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-088 · Ledger intake: refusals that are not transient

_Original text of batch E kept for audit. Amendments and the final ruling follow it._

**Question.** The intake (RWB-P1-E1067-APP) retries transient failures and parks malformed events; what does it do when the in-process writer refuses for a reason a retry cannot cure – case not found, validation refusal, decision-log reference refused – and with which `rwb-dlt-reason` (GAP-3496; RR E1067-APP#1, E1067-CON#1)?

**Sources.** REG v2 RD-P1-009 (retry 1 min, 10 min, 1 h, then `<topic>.dlt`; headers `rwb-dlt-reason`, `rwb-dlt-consumer`, `rwb-dlt-owner`; LEDGER_WRITE_FAILED only on RETRIES_EXHAUSTED); RWB-P1-E1067-APP lines 92, 102, 145, 170, 198, 324 (reasons UNSUPPORTED_VERSION, RETRIES_EXHAUSTED, MISSING_ATTRIBUTE, SCHEMA_INVALID); RD-P1-087.

**Ruling.**
1. Such a refusal is parked **at once** on `<topic>.dlt` (no retry topic), with `rwb-dlt-consumer=rwb-source-data`, `rwb-dlt-owner=P1 squad` and `rwb-dlt-reason`:
   - `CASE_NOT_FOUND` – the case read answers 404 or 403;
   - `VALIDATION_REFUSED` – the writer answers 422 (any field), the field name in header `rwb-dlt-field`;
   - `DECISION_REF_REFUSED` – the DECISION_TAKEN reference is missing or refused (RD-P1-087 rule 1).
2. The offset is committed after the `.dlt` write; `processed_event` records the `ce_id` with no entry; no LEDGER_WRITE_FAILED is raised (it stays for RETRIES_EXHAUSTED). A decision-log or case read that does not answer stays transient (retry path).
3. Replay after correction uses the platform replay tool; the business key prevents a duplicate entry.
4. RWB-P1-E1067-APP X6 and AC8 read: "no entry; parked at once with `CASE_NOT_FOUND`; the consumer log shows the case ID and no payload value". RWB-P1-E1067-CON AC5, AC11 and the writer stub follow.

**Affected stories.** RWB-P1-E1067-APP, RWB-P1-E1067-CON, RWB-P1-E1066-OPS (dlt alert), RWB-ITG-E1067-ITG.
**Affected documents.** Event and Messaging Design v7 / Kafka Topic and Event Catalog v3 (reason values of the ledger-intake `.dlt`); Gap Register v3 (GAP-3496 closed).
**Findings settled.** RWB-P1-E1067-APP#1, RWB-P1-E1067-CON#1 (re-review).
**GAP/ASM.** Closes GAP-3496.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** A consumer parks at once what a retry cannot fix and names why in `rwb-dlt-reason`.
**Values chosen without a source.** The three reason values; header `rwb-dlt-field`.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-089 · Ledger series, integrity check, protection of append-only objects and the sandbox reload

_Original text of batch E kept for audit. Amendments and the final ruling follow it._

**Question.** RWB-P1-E1066-OPS names five ledger series and three alerts without metric names, types or the emitting component; the case_seq gap check, the periodic trigger check and an incident signal that survives a database outage are open (GAP-3494; RR E1066-OPS#1). How are TRUNCATE and trigger changes refused (E1066-OPS AC11), and how does the sandbox reload `interaction` while TRUNCATE is refused (GAP-3493; RR E1065-APP#1)?

**Sources.** RWB-P1-E1066-OPS v3 lines 58, 82, 95, 153-159, 198-202, 298 (series: append rate, failures by class, duplicate hits, p95 latency, case_seq gaps; dimensions environment, release, build ID; no case ID label); PS v9 `rwb_source_data.sql` lines 599-608 (`refuse_change()`, `tr_interaction_append_only BEFORE UPDATE OR DELETE`), README line 179 (logins by RWB-PLT-NF06-DB, privileges by RWB-PLT-N011-DB); existing metric form `rwb_source_data_duplicate_start_total`, `rwb_source_data_win_delivery_repeat_total`; TWAC v3 Platform rules R19 (no Quartz; a job is a Temporal Schedule); REG v2 RD-P1-073 rule 1, RD-P1-046.

**Ruling.**
1. **Series (GAP-3494)**, emitted by `InteractionLedgerWriter` (RWB-P1-E1066-APP) through the service's metrics registry, labels `environment`, `release`, `build_id` only (plus the label named):
   - `rwb_source_data_ledger_append_total` – counter, label `caller` (REST, INTAKE, E2034, CUTOVER);
   - `rwb_source_data_ledger_append_failure_total` – counter, label `error_class` (DB, SEQ_CLASH, CASE_READ, DECISION_READ, VALIDATION);
   - `rwb_source_data_ledger_duplicate_total` – counter, label `kind` (HEADER_REPLAY, BUSINESS_KEY);
   - `rwb_source_data_ledger_append_duration_seconds` – histogram; the dashboard shows p95;
   - `rwb_source_data_ledger_case_seq_gap_total` – counter, written by the integrity check of rule 2.
   The series live in process memory and are scraped from the metrics endpoint, so a database outage still raises the failure-rate alert on `error_class="DB"` (the incident signal). RWB-P1-E1066-APP adds the emitting code and an AC; RWB-P1-E1066-OPS AC4 and AC5 assert names and labels. Thresholds stay values-file entries of E1066-OPS.
2. **Integrity check.** Temporal Schedule `rwb-source-data-ledger-check`, hourly, overlap SKIP, starts workflow `LedgerIntegrityCheck` (activity `checkLedgerIntegrity`, RWB-P1-E1066-APP). It counts case_seq gaps on cases not closed (gaps of closed cases are accepted, RD-P1-048) into `rwb_source_data_ledger_case_seq_gap_total`, and sets gauge `rwb_source_data_ledger_guard_present` to 1 when `tr_interaction_append_only` and `tr_interaction_no_truncate` exist and are enabled, else 0 (alert on 0). TWAC v3 gains the Schedule and workflow rows.
3. **Protection of append-only objects (GAP-3493).** Both mechanisms apply:
   - the tables of `rwb_source_data` are owned by the migration owner role that runs Flyway for the schema (created by RWB-PLT-NF06-DB, privileges by RWB-PLT-N011-DB); the runtime login `rwb_source_data` holds SELECT and INSERT on `interaction` only (no UPDATE, DELETE, TRUNCATE or TRIGGER), so it cannot TRUNCATE or `ALTER TABLE … DISABLE TRIGGER`;
   - a forward migration of RWB-P1-E1066-APP adds `CREATE TRIGGER tr_interaction_no_truncate BEFORE TRUNCATE ON interaction FOR EACH STATEMENT EXECUTE FUNCTION refuse_change();`, so even the owner role cannot truncate.
4. **Sandbox reload (E1065-APP#1).** The in-place reload of RWB-P1-E1065-APP truncates and reloads the ACE-shaped tables of `public` and the generator-seeded P1 tables **except `interaction`**; generator `interaction` rows are inserted only when the table is empty. The "rebuild from DDL between suites" of RD-P1-073 is `DROP SCHEMA rwb_source_data CASCADE` in `rwb_sandbox` by the migration owner role under the sandbox build identity (RD-P1-098 rule 4), then the Flyway sequence and the seed; the database is never dropped (RD-P1-046). Never done outside `rwb_sandbox`. AC5 of RWB-P1-E1065-APP is aligned; GAP-3493 is closed.

**Affected stories.** RWB-P1-E1066-APP, RWB-P1-E1066-OPS, RWB-P1-E1067-APP, RWB-P1-E2034-APP, RWB-P1-E1065-APP, RWB-P1-E1065-DB, RWB-PLT-NF06-DB, RWB-PLT-N011-DB, RWB-ITG-E1066-ITG.
**Affected documents.** Physical Schema v9 `rwb_source_data.sql` (TRUNCATE trigger as the next forward version; ownership note in the README); Temporal Workflow and Activity Catalog v3 (Schedule and workflow rows); Observability and Monitoring Design v6 (ledger series and alerts); register RD-P1-073 (clarification line); Gap Register v3 (GAP-3494, GAP-3493 closed).
**Findings settled.** RWB-P1-E1066-OPS#1, RWB-P1-E1065-APP#1 (re-review).
**GAP/ASM.** Closes GAP-3494, GAP-3493.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** Append-only tables: runtime login INSERT/SELECT only, BEFORE UPDATE/DELETE and BEFORE TRUNCATE triggers, an hourly integrity check; reset only by a schema rebuild in the sandbox.
**Values chosen without a source.** Metric and label names; hourly Schedule, workflow and activity names; the gauge.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-090 · Migrated ledger entries: the cutover entry point of the writer

_Original text of batch E kept for audit. Amendments and the final ruling follow it._

**Question.** RWB-P1-DM005-APP writes migrated notes and promises through `InteractionLedgerWriter` in process (XD-08), but the writer sets `id`, `caseSeq` and `sourceSystem` itself, and `migration_source` and `migrated_at` are not in `InteractionRequest` (RR DM005-APP#1).

**Sources.** REG v2 XD-08, RD-P1-007 (server-set fields), RD-P1-027 (standard columns `migration_source varchar(20)`, `migrated_at timestamptz`), RD-P1-064 rule 1; PS v9 `interaction`; GR v3 GAP-3275 (LOV-MIGRATION-SOURCE values).

**Ruling.**
1. RWB-P1-E1066-APP builds the in-process method `InteractionLedgerWriter.appendMigrated(MigratedInteraction)`, callable only by RWB-P1-DM005-APP and only while the DM005 cutover switch is on; no REST path.
2. It takes the legacy `occurredAt`, `eventCode`, `actorType`, `actorRef`, `channel`, `direction`, `contactResult`, `summary`, `promiseAmount`, `promiseDate`, `contactKey`, `idempotencyKey` (the legacy business key) and `migrationSource`. It sets `id`, `caseSeq` (per case, in legacy `occurredAt` order, under the same advisory lock as `append`), `sourceSystem` WORKBENCH, `migration_source`, and `migrated_at` = commit instant (UTC), and keeps the append-only rules. An existing business key adds nothing.
3. `migration_source` takes the LOV-MIGRATION-SOURCE value (Pending, owner data owner, GAP-3275); interim the fixture value is a test constant, never a LOV row.
4. The legacy-to-writer field mapping is RWB-P1-DM005-APP's (section 11, from Source to Target Mapping v7 sheet Migration packages). RWB-P1-E1066-APP becomes a build dependency of RWB-P1-DM005-APP.

**Affected stories.** RWB-P1-DM005-APP, RWB-P1-E1066-APP, RWB-ITG-DM005-ITG.
**Affected documents.** Story Build Order v5 / Dependency Map v7 (edge E1066-APP → DM005-APP); register RD-P1-007 (clarification line).
**Findings settled.** RWB-P1-DM005-APP#1 (re-review).
**GAP/ASM.** GAP-3275 unchanged.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** A migration writes through the owner's own component, never by a raw insert, and that component sets the provenance columns.
**Values chosen without a source.** Method and type names.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-091 · Access-log entries are written through the rwb-access access-log contract, never as decision records

_Original text of batch E kept for audit. Amendments and the final ruling follow it._

**Question.** RD-P1-072 says reads go to the access log only and publish no DecisionRecorded, but RWB-P4-E1023-APP (BR6, BR7, BR12, AC24) writes AC-READ and AC-DENY through the decision-record library (GAP-3395, NEW-GAP-G6-1). How are access-log entries written? ACCESS-YAML publishes only `GET /admin/access-log`; the write is unpublished (GAP-3322; RR E1068-APP#2).

**Sources.** REG v2 RD-P1-072; RWB-P3-E1023-APP v3 lines 53, 67, 169, 227 (BR4), 341, 346, 410; RWB-PLT-E1037-CON v3 lines 235, 279, 287, 396, 406 (the access-log operation belongs to P4 through RWB-P4-E1039-CON; the audit fake records the case id, field id and flag and refuses a record that carries a value); DCPI v6 sheet Key ("Read audit … through PII Kafka"; "PII logging: the ACE Common audit and personal-data access log path (INT-34) to the SOC, separate from the rwb.<service>.events.v1 topics"); ACCESS-YAML `/admin/access-log`.

**Ruling.**
1. **One path.** Every read of personal data, and every refused access check, writes one access record through the **rwb-access access-log contract of RWB-P4-E1039-CON**, called by the reading service's `AccessClient` (platform library, RWB-PLT-E1037). Record: event `AC-READ` or `AC-DENY`, the caller's user or workload identity, `caseId` where there is one, the operation, the field IDs read and their `masked` flags, the instant; never a value. rwb-access stores it in its access log (read by `GET /admin/access-log`) and forwards the PII access record to the ACE Common PII path (INT-34) to the SOC.
2. **Not a decision record.** No access record is written through the decision-record library, published as `rwb.decision.DecisionRecorded.v1`, sent on any `rwb.<service>.events.v1` topic or appended to the interaction ledger. RWB-P4-E1023-APP BR6, BR7, BR12 and AC24, and RWB-P4-E1039-APP, -CON and -DB, are restated accordingly. AC-DENY is an access check, not a DP-03 decision.
3. **Failure.** A read whose access record cannot be written returns no data: 503 MSG-GEN-006 (RWB-P3-E1023-APP BR4; RD-P1-076 rule 6).
4. **Pending transport (GAP-3322).** The write operation, its payload and its transport are **Pending, owner rwb-access contract owner with the solution architect**. Interim: `AccessClient.record(accessRecord)` is an in-process port of the platform library; in tests and DEV it is backed by the audit fake of RWB-PLT-E1037-CON s12.8, which records the fields and refuses a record with a value; P1 and P3 stories assert the record through the fake. GAP-3395 is closed; GAP-3322 stays open, **blocks build: No** with this interim.

**Affected services.** rwb-access; rwb-source-data; rwb-case; gateway-bff; every service that reads personal data.
**Affected stories.** RWB-P4-E1023-APP, RWB-P4-E1039-APP, RWB-P4-E1039-CON, RWB-P4-E1039-DB, RWB-P3-E1023-APP, RWB-ITG-E1023-ITG, RWB-P4-E1037-CON, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P1-E1068-APP, RWB-P1-E1016-APP, RWB-P1-E1069-APP, RWB-P1-E2010-CON.
**Affected documents.** API Specification v7 `rwb-access.yaml` (description of the access-log write as Pending GAP-3322); register RD-P1-072 (clarification line); Gap Register v3 (GAP-3395 closed; GAP-3322 non-blocking).
**Findings settled.** RWB-P1-E1068-APP#2 (document); RWB-P4-E1023-APP#3 residual.
**GAP/ASM.** Closes GAP-3395.
**Status.** Proposed – Claude Opus 5.5 (applied); transport pending under GAP-3322.
**Reuse note.** Access is logged through rwb-access; decisions are recorded through the decision-record library; never both for one read.
**Values chosen without a source.** Record field list (taken from the audit fake and the E1023 AC wording).

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-092 · Retention run record, review list, age bases, record classes and the archive container

_Original text of batch E kept for audit. Amendments and the final ruling follow it._

**Question.** No table stores the retention run record (GAP-3457, NEW-GAP-S5-8; RR E1017-APP#1). Where are the listed REVIEW keys held, and how does Compliance read them (RR E1017-APP#4)? Which `ageBasis` and `recordClass` values are accepted per REVIEW table (GAP-3454; RR E1017-APP#5)? Which archive container, identity and prefix (GAP-0490; RR E1017-OPS#1)?

**Sources.** YAML `RetentionRun` {status RUNNING/COMPLETED/FAILED, countsPerTable, archiveLocation, holdReport (GAP-3450)}, `RetentionTableCount`, `RetentionRule` (`ageBasis` "for interaction the only allowed value is case.closedAt"), `/retention-runs/{runId}` (Platform administration R); CASE-YAML `ClosureDate` {caseId, closedAt, accountKeys, personKeys}, `RetentionExclusion` {caseId, reason LEGAL_HOLD/OPEN, accountKeys, personKeys}; PS v9 `interaction.retention_class`; DCPI v6 Read me v6 (DF-EXT-050 `contact_point_ext.person_key`); REG v2 RD-P1-047, RD-P1-048; GR v3 GAP-0490 (Resolved (directive): path `retention/YYYY-MM-DD/<table>/`, manifest of row count and SHA-256 per file, the service's own credential, read back before any delete; container contract with RWB-PLT-TE012-APP), GAP-3279.

**Ruling.**
1. **Run record (GAP-3457).** RWB-P1-E1017-APP creates, in its own forward migration, table `retention_run` in `rwb_source_data`: `id uuid` (= runId), `run_date date`, `run_no integer`, `rule_version varchar(20)`, `status varchar(10)` (RUNNING, COMPLETED, FAILED), `started_at timestamptz`, `completed_at timestamptz` null, `archive_location varchar(400)` null, `counts_per_table jsonb` (array of `RetentionTableCount`), `hold_report jsonb`, and the standard columns; `uk_retention_run (run_date, run_no)`. The stored HTTP answer stays in the platform idempotency store (RD-P1-001). Dictionary rows come with the migration (next free DF-OPS IDs; RD-P1-071, RD-P1-096 rule 1). `recordRun` writes it; `GET /retention-runs/{runId}` reads it. From wave 4 `job_run` also carries the run for the job monitor; `retention_run` stays.
2. **Listed keys (E1017-APP#4).** Table `retention_review_item`: `id uuid`, `retention_run_id uuid` (FK to `retention_run`), `table_name varchar(30)`, `record_key varchar(255)`, `age_basis_at timestamptz`, and the standard columns; `uk_retention_review_item (retention_run_id, table_name, record_key)`. Compliance reads it through the new `GET /retention-runs/{runId}/review-items` (operationId `getRetentionRunReviewItems`; Platform administration R; `page` 0-based; `size` 1 to 200, default 50; answer {items[{tableName, recordKey, ageBasisAt}], page, size, total}; 404 MSG-P4-003 for an unknown run). Platform administration R is the read-only right that Compliance (RW-COMPLY) and audit hold.
3. **Age bases (GAP-3454).** Accepted `ageBasis` per table, each measured with the boundary-kept rule of RD-P1-048:
   - `interaction`, `dp_treatment`, `dp_guarantee_claim`: `case.closedAt` (join by `case_id` to `ClosureDate`);
   - `account_ext`: `account.lastClosedAt` – the latest `closedAt` of the `ClosureDate` items whose `accountKeys` hold the key, when no `RetentionExclusion` holds it;
   - `party_ext`, `contact_point_ext`: `person.lastClosedAt` – the same by `personKeys` (`contact_point_ext.person_key`, DF-EXT-050);
   - `valuation_ext`: no join key yet (GAP-3279, owner data architect); interim its rule is accepted, nothing is selected (`selected` 0, `listed` 0) and the run log names the reason.
   Any other value answers 422 MSG-GEN-007. GAP-3454 is closed except for valuation_ext (GAP-3279).
4. **Record classes.** For `interaction`, `recordClass` filters `retention_class`. The six REVIEW tables have no class column: their only accepted `recordClass` is `ALL`; any other value answers 422 MSG-GEN-007.
5. **Archive container (GAP-0490; E1017-OPS#1).** Path and manifest as GAP-0490: `retention/{runDate}/{tableName}/`, a manifest with the row count and SHA-256 per file, read back before any delete, written under the rwb-source-data workload identity. The container name per environment and a prefix-scoped write-once role for that identity are **Pending, owner solution architect with platform security**, NEW-GAP-E2 (container contract with RWB-PLT-TE012-APP). Interim: DEV and the pipeline test write to a local blob emulator container `rwb-source-data-retention` behind the `ArchiveStore` port; in SIT and later the ARCHIVE delete step stays behind the retention flag off (the REVIEW listing may run) until NEW-GAP-E2 is closed. No row is deleted without a write-once container.

**Affected services.** rwb-source-data; rwb-document (JOB-17 caller); rwb-case (closure and exclusion reads).
**Affected stories.** RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P5-E1017-APP, RWB-PLT-TE012-APP, RWB-ITG-E1017-ITG.
**Affected documents.** Physical Schema v9 (two tables as the next forward versions); API Specification v7 `rwb-source-data.yaml` (`/retention-runs/{runId}/review-items`; `ageBasis` and `recordClass` descriptions; operation count, see RD-P1-094 and RD-P1-097); Service Contract Catalog v3; Temporal Workflow and Activity Catalog v3 (R23 `recordRun` target); Logical Data Model and Data Dictionary v11; Gap Register v3 (GAP-3457, GAP-3454 closed; NEW-GAP-E2).
**Findings settled.** RWB-P1-E1017-APP#1, #4, #5; RWB-P1-E1017-OPS#1 (re-review).
**GAP/ASM.** Closes GAP-3457 and GAP-3454 (valuation_ext stays with GAP-3279). New NEW-GAP-E2. GAP-0490 confirmed.
**Status.** Proposed – Claude Opus 5.5 (applied); container pending under NEW-GAP-E2.
**Reuse note.** A run with per-table counts has its own run table; REVIEW lists are rows, read through a paged read under the read-only admin right.
**Values chosen without a source.** Table and column names; operation path and id; `ageBasis` literals other than `case.closedAt`; `ALL`; emulator container name.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-093 · Migration cutover: provenance columns, pipeline authorisation, handover package and acceptance, clean days

_Original text of batch E kept for audit. Amendments and the final ruling follow it._

**Question.** (a) DM stories read back `migration_source` and `migrated_at` through owner contracts that do not expose them (RR DM003-APP#1, DM004-APP#1, DM007-APP#1). (b) How is a cutover run started, with which rights, and who signs off? DM006 and DM007 check "Platform administration R", which is a read-only right. (c) The handover package layout and the owner's acceptance signal (RR DM006-APP#1, DM007-APP#2; GAP-2170, GAP-0529, GAP-3541). (d) How are ten clean days counted when a date has no reconciliation row?

**Sources.** REG v2 RD-P1-027 (standard columns on every migrated table), RD-P1-042 (clean day; MSG-P1-023), RD-P1-068 rule 7 (each package loaded by its target service identity), RD-P1-086 rule 1; RWB-P1-DM003-APP v3 lines 55, 58, 85, 93, 98, 103-108 (release-pipeline command; the handover is a file; sign-off in the cutover record; ASM-0717); RWB-P1-DM007-APP v3 lines 54, 77, 80, 83, 98-99 (ASM-3485); RWB-P1-DM006-APP v3 lines 77, 85, 102-105; EMS v6 MSG-P1-023.

**Ruling.**
1. **Provenance (one rule).** Owner contracts do not expose `migration_source` or `migrated_at`, and no DM story asserts them through an owner read. A DM story asserts them (i) on the rows it writes itself (`valuation_ext` for DM006; `contact_point_ext` and `interaction` for DM005) and (ii) on every row of its handover package files. The owner load and the RWB-ITG-DM0nn-ITG story assert them in the owner schema. DM003-APP AC3, BR6 and TC-DM-003-03, DM004-APP AC3 and BR4, DM007-APP AC1 and the owner-mock lines change accordingly.
2. **Entry mechanism and rights.** A cutover step is a **release-pipeline stage**, never a REST call or a Workbench screen action, so no Workbench capability is checked to start it. The stage runs under the workload identity of the service that reads or writes (P1 extract: `rwb_source_data`; owner load: the target service, RD-P1-068 rule 7), with one Idempotency-Key (UUID) per run recorded in the cutover record. Starting the stage needs the pipeline's protected-environment approval by the **release owner**; squad members (RW-TRIBE) build it and trigger it in DEV and the pipeline test only. The exception rows "a caller without Platform administration R … 403 MSG-P4-002 / 401 MSG-P4-001" (DM006 exception 6, DM007 X8, and AC3 and AC8 where they test it) become "a stage without the environment approval does not start; nothing is read".
3. **Sign-off.** The data steward (RW-DATASTEW) signs off through the pipeline's manual-approval step on the cutover record. The step first recomputes the clean-day count and, when it is below ten, fails with the MSG-P1-023 text and records no sign-off. Platform administration R (RW-AUDIT, RW-COMPLY and the other holders) only reads the cutover record and its evidence; it never starts a stage or signs off.
4. **Handover package and acceptance.** Each package is a folder of the cutover record, `<packageStory>/<cutoverBusinessDate>/<targetService>/`, holding one UTF-8 CSV per entity (header row; one column per section 11 field by `field_name`, plus `migration_source` and `migrated_at`) and `manifest.json` {packageStory, cutoverBusinessDate, targetService, idempotencyKey, files[{entity, rowCount, sha256}]}. The owner's load stage writes `acceptance.json` beside it: {packageStory, cutoverBusinessDate, targetService, status ACCEPTED | REFUSED, acceptedRowCount, refusedKeys[], loadedAt, loaderIdentity}. A package counts as handed over only with an ACCEPTED acceptance whose `acceptedRowCount` equals the manifest. There is no timeout: the cutover record stays open, and sign-off is impossible, until every owner of the story has ACCEPTED. DM003, DM004, DM006 (AC9, AC10, exception 8) and DM007 (AC10, AC12, X7) use this layout; the CSV column order is the section 11 order.
5. **Ten clean days.** Counting starts on the first bank business date after the last owner's ACCEPTED acceptance. A date is clean when it has REC-01 and REC-02 rows for every product group and the REC-05 row (RD-P1-086 rule 1), all PASS. A bank business date with any BREAK row, or with no row at all (run not finished, gate HOLD or allocation unreadable – RD-P1-042 writes no row then), is not clean and resets the count to zero; the date is listed with reason `BREAK` or `NO_RESULT`. Non-business days (DP14 holiday calendar) are skipped. The count is derived from the rows each time it is read, so a FAILED run that is rerun later and writes PASS rows makes that date clean on the next read.

**Affected services.** rwb-source-data; rwb-case, rwb-treatment, rwb-asset, rwb-litigation, rwb-comms, rwb-partner, rwb-decision, rwb-payment (owner loads).
**Affected stories.** RWB-P1-DM001-APP, RWB-P1-DM002-APP, RWB-P1-DM003-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP, RWB-P1-DM008-APP, RWB-P1-DM009-APP, RWB-P1-DM010-APP, RWB-P1-DM011-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P1-DM014-APP (rules 2 and 3 for every cutover story; rule 4 for the packaged ones DM003, DM004, DM006, DM007, DM008, DM009, DM010, DM013), RWB-ITG-DM003-ITG to RWB-ITG-DM013-ITG, RWB-P8-DM013-APP.
**Affected documents.** Data Migration Approach v5 (cutover stage, rights, package layout, clean-day rule); Users Roles and Permissions v6 (Platform administration R read-only note); Gap Register v3 (GAP-2170, GAP-0529, GAP-3541 closed; GAP-3275 unchanged).
**Findings settled.** RWB-P1-DM003-APP#1, RWB-P1-DM004-APP#1, RWB-P1-DM007-APP#1 (document); RWB-P1-DM006-APP#1, RWB-P1-DM007-APP#2 (story).
**GAP/ASM.** Closes GAP-2170, GAP-0529, GAP-3541. ASM-0717 and ASM-3485 confirmed.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** A cutover runs in the pipeline under service identities, signs off in the pipeline, hands over by manifest and acceptance files, and counts clean days from result rows only.
**Values chosen without a source.** Folder and file names; manifest and acceptance members; reset on a missing row; reason codes.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-094 · Extension facts: first write, the read of the row and its ETag, access rule

_Original text of batch E kept for audit. Amendments and the final ruling follow it._

**Question.** `PUT /extension-facts/parties/{personKey}` and `/accounts/{accountKey}` require If-Match (RD-P1-006), but the first write has no version (GAP-3555; RR E1018#3) and no GET returns a row or its ETag (GAP-3409). The roles and masking of the writes are open (GAP-3407).

**Sources.** REG v2 RD-P1-006 (`ETag: "<version>"`; 428 and 409 MSG-GEN-004); YAML lines 1318-1411 (the two PUT operations, `PartyExtFactsRecord`, `AccountExtFactsRecord`); DCPI v6 (DF-EXT-002 to DF-EXT-004 Sensitive, Restricted).

**Ruling.**
1. **First write (GAP-3555).** A write for a key with no row sends `If-None-Match: *` and no If-Match; the row is created and the answer is **201** with `ETag: "1"`. `If-None-Match: *` when a row exists → 409 MSG-GEN-004. Neither header → 428 MSG-GEN-004. An If-Match for a key with no row → 409 MSG-GEN-004. GAP-3555 is closed.
2. **Read (GAP-3409).** `GET /extension-facts/parties/{personKey}` (operationId `getExtensionFactsPartiesPersonkey`) and `GET /extension-facts/accounts/{accountKey}` (`getExtensionFactsAccountsAccountkey`) answer the record with its `ETag`; 404 MSG-P4-003 when no row exists; x-capability Case record R; built by RWB-P1-E1018-APP. A test obtains the ETag from this read or from the write answer. GAP-3409 is closed.
3. **Access rule (GAP-3407), interim.** The PUTs carry x-capability **Case record C**, checked from the token (no authorise call). The change is written to the access log (RD-P1-091) with the field IDs. Answers pass through FieldMasker (RD-P1-076: the three Sensitive booleans are masked unless a rule unmasks them). The permission letter, the owning screen story and the unmasking rule for the exclusion screen stay **Pending, owner product owner with compliance** (GAP-3407, **blocks build: No**); the FieldMasker fake carries an unmasking rule for the test role so that both branches are tested.

**Affected stories.** RWB-P1-E1018-APP, RWB-P1-E1069-APP, RWB-P4-E1037-CON.
**Affected documents.** API Specification v7 `rwb-source-data.yaml` (If-None-Match parameter, 201, two GET operations); Service Contract Catalog v3; Gap Register v3 (GAP-3555, GAP-3409 closed; GAP-3407 non-blocking); register RD-P1-006 (clarification line).
**Findings settled.** RWB-P1-E1018#3 (re-review).
**GAP/ASM.** Closes GAP-3555, GAP-3409.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** Create with `If-None-Match: *`, update with `If-Match`; every updatable resource has a GET that returns its ETag.
**Values chosen without a source.** operationIds; 201 for the first write; the Case record C interim.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-095 · Data-product access: date of the access check, workload identities, field lists, catalog reconciliations

_Original text of batch E kept for audit. Amendments and the final ruling follow it._

**Question.** RWB-P1-E1016-APP resolves `data_product_access` rows on "the business date in Asia/Bangkok", while RWB-P4-E1016-APP tests valid-from against "the case's business date" (GAP-3443; RR E1016-APP#11). How is a workload identity (the rwb-comms dispatch loop of RWB-P1-E2021-APP) authorised for the records read, which has role rows only (RR E1016-CON#8)? Which fields does each product serve, and how is an object without `account_key` or `person_key` restricted to the case (GAP-3445)? Where are the REC codes per product of the catalog stored (GAP-3446)?

**Sources.** PS v9 `data_product_access` (`uk_data_product_access (product_code, role_code, access_version)`, `valid_from`, `valid_to`), `sys_objects.data_product`, `sys_fields`; RWB-P1-E1016-APP line 106; RWB-P4-E1016-APP lines 84, 102, 116; YAML records read description; REG v2 RD-P1-064 (service rows "Case record C on rwb-source-data" for workload identities).

**Ruling.**
1. **One date (GAP-3443).** Access rows are in force on the **calendar date of the request instant in Asia/Bangkok** (`valid_from` ≤ that date, and `valid_to` null or ≥ that date): access is about now, not about the data date. P1 puts the date in the access resolution it presents with the authorise request (`resolvedOn`; the rest of the field set stays Pending under GAP-0983), and RWB-P4-E1016-APP step 9 and X5 test valid-from against `resolvedOn`. GAP-3443 is closed.
2. **Workload identities (E1016-CON#8).** A workload identity is authorised by its **service row**, the same row form RD-P1-064 uses for the ledger: Case record R on rwb-source-data for the service, plus one `data_product_access` row per product with `role_code` = the service row code. The service row codes are **Pending, owner rwb-access owner with the data steward**, NEW-GAP-E3; interim fixture codes sit in the rwb-access fake and the P1 seed of DEV only. The section 12.1 access column of RWB-P1-E1016-CON names the consumers: gateway-bff (users), rwb-comms (RWB-P1-E2021-APP dispatch loop, DP02), rwb-integration (RWB-P2-E1007-APP), and the readers of RWB-P1-E2010-APP through gateway-bff.
3. **Field list per product (GAP-3445).** The records read of product P serves the active `sys_fields` of the objects whose `sys_objects.data_product` = P and that the read path holds (the v_ace_* view or the P1 table). An object is restricted to the case by `account_key` or `person_key` (ACE views) or by `case_id` (Workbench tables); an object with none of them is not served by the records read. GAP-3445 is closed.
4. **Catalog reconciliations (GAP-3446).** No table holds REC codes per product. Interim: the catalog entry answers `reconciliations` as an empty list and AC15 asserts the empty list. Pending, owner data steward (GAP-3446, **blocks build: No**).

**Affected stories.** RWB-P1-E1016-APP, RWB-P1-E1016-CON, RWB-P4-E1016-APP, RWB-P1-E2021-APP, RWB-P2-E1007-APP, RWB-ITG-E1016-ITG.
**Affected documents.** API Specification v7 `rwb-source-data.yaml` (records read access note); Gap Register v3 (GAP-3443, GAP-3445 closed; GAP-3446 non-blocking; NEW-GAP-E3).
**Findings settled.** RWB-P1-E1016-APP#11, RWB-P1-E1016-CON#8 (re-review).
**GAP/ASM.** Closes GAP-3443, GAP-3445. New NEW-GAP-E3.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** Validity dates of access rows are calendar dates of the request; services are authorised by service rows, never by borrowing a user role.
**Values chosen without a source.** Calendar-date rule; `resolvedOn`; the empty-list interim.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-096 · Dictionary and contract rows: object rows, DC-ACE seed, smoke records, reference-load handler, applied version

_Original text of batch E kept for audit. Amendments and the final ruling follow it._

**Question.** Who writes new `sys_objects` rows when the E1064 governed load refuses a field of an unknown object (RD-P1-071; RR E1064-APP#3)? Who writes the DC-ACE version 1 DRAFT row (RR E1064-APP#1)? Which synthetic records does the E1064 smoke run use (RR E1064-OPS#1; GAP-3471)? How is the P3 reference-load handler built while its contract is unpublished (GAP-3338; RR E1064-APP#2, E1064-CON#2)? Which column holds the applied reference version (GAP-3403)?

**Sources.** PS v9 `rwb_source_data.sql` (lines 2436 onwards, "Dictionary rows added by later story migrations", for example `job_run`), `data_contract` (lines 205-218: `contract_code`, `source_system`, `interface_id` NOT NULL varchar(40), `contract_version`, `status` default DRAFT); RWB-P1-E1064-APP lines 58, 96-101, 139-140; RWB-P1-E1064-OPS lines 70, 310; REG v2 RD-P1-020 D and G, RD-P1-071, RD-P1-045 (a seed fails on an existing key); EMS v6 MSG-P1-021.

**Ruling.**
1. **Object rows (amends RD-P1-020 D).** The `sys_objects` and `sys_fields` rows of a new table are written by the same forward migration that creates the table (the PS v9 pattern), not by the E1064 governed load. The governed load changes field rows and adds fields of existing objects only; a field of an object absent from `sys_objects` is refused with MSG-P1-005 (RD-P1-071). RWB-P1-E1064-APP adds that AC; RWB-P1-AD018-APP's "through the governed load of RWB-P1-E1064-APP" reads "in its own migration".
2. **DC-ACE seed.** A forward data migration of RWB-P1-E1064-APP inserts the `data_contract` row (`contract_code` DC-ACE, `source_system` ACE, `interface_id` per GAP-3469 – interim `ACE-VIEW-CONTRACT`, `contract_version` 1, `status` DRAFT, no confirmation) in every environment; it fails on an existing key. Its AC asserts the row.
3. **Smoke records (GAP-3471).** In SIT and UAT the smoke run writes nothing: it reads the dictionary and the contracts, sends a PATCH with a stale If-Match (expects 409 MSG-GEN-004, nothing written) and publishes the unconfirmed DC-ACE (expects the MSG-P1-021 refusal, nothing written). The write smoke with a synthetic field and contract runs in DEV only. The smoke identity with Reference data U stays Pending, owner QA lead (GAP-3471, **blocks build: No**).
4. **Reference-load handler (GAP-3338).** Interim: P1 builds `ReferenceLoadApplyHandler` in process (RWB-P1-E1001-APP for `data_product`, `data_product_access` and `data_product_source`; RWB-P1-E1064-APP for dictionary rows), with table code = the table name, idempotent on (table code, version). Its tests drive it with the payload of the RWB-P3-E1043-CON fake; it is not integrated with rwb-case until the transport is published. The 12.8 handler stubs of E1064-APP and E1064-CON are taken from that fake. GAP-3338 stays open, owner solution architect with the rwb-case service owner, **blocks build: No**.
5. **Applied version (GAP-3403).** A forward migration of RWB-P1-E1001-APP adds the nullable column `applied_reference_version integer` to `data_product`, `data_product_access` and `data_product_source` (next free DF-REF IDs after DF-REF-302); the handler skips a load whose version is not greater. GAP-3403 is closed.

**Affected stories.** RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E1064-OPS, RWB-P1-E1001-APP, RWB-P1-AD018-APP, RWB-P3-E1043-CON, RWB-ITG-E1064-ITG.
**Affected documents.** Physical Schema v9 (the new column as a forward version); register RD-P1-020 (amendment line); Gap Register v3 (GAP-3403 closed; GAP-3338, GAP-3471 and GAP-3469 non-blocking).
**Findings settled.** RWB-P1-E1064-APP#1, #2, #3; RWB-P1-E1064-CON#2; RWB-P1-E1064-OPS#1 (re-review).
**GAP/ASM.** Closes GAP-3403.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** A table and its dictionary rows ship in one migration; smoke runs in shared environments prove refusals, not writes.
**Values chosen without a source.** Interim `interface_id`; column name; handler name.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-097 · Account-page read used by rwb-case for the case list

_Original text of batch E kept for audit. Amendments and the final ruling follow it._

**Question.** X-27 put the account-page read of rwb-case in RWB-P1-E1015-CON, built by RWB-P1-E1002-APP; its path, page limit, wire names, right and errors are open (GAP-3274, GAP-3438).

**Sources.** REG v2 X-27, RD-P1-024 item 3, RD-P1-060 (single-account `GET /accounts/{accountKey}`, `Account` schema); YAML (`size` maximum 200 on P1 pages); DCPI v6 Read me v6 ("Redact query-string keys").

**Ruling.** `GET /accounts` with the repeated query parameter `accountKey` (1 to 200 values; more → 422 MSG-GEN-002; none → 400 MSG-GEN-001); operationId `getAccounts`; x-capability Case record R; caller the rwb-case workload identity only. Answer `AccountPage` {items: `Account`[] in the order of the request, missingKeys: string[], freshness: the DP01 `DataProductFreshness`}; a key with no row is listed in `missingKeys`, never answered 404. Errors 400 MSG-GEN-001, 401 MSG-P4-001, 403 MSG-P4-002, 422 MSG-GEN-002, 503 MSG-GEN-006. Query-string keys are redacted in logs. Published in RWB-P1-E1015-CON, built by RWB-P1-E1002-APP, deployed by RWB-P1-E1002-OPS; the YAML line "Pending: account-page read path …" is removed. GAP-3274 and GAP-3438 are closed.

**Affected stories.** RWB-P1-E1002-APP, RWB-P1-E1002-OPS, RWB-P1-E1015-CON, RWB-P3-E1002-APP.
**Affected documents.** API Specification v7 `rwb-source-data.yaml` (path and schema); Service Contract Catalog v3; Gap Register v3.
**GAP/ASM.** Closes GAP-3274, GAP-3438.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** A multi-key read is a GET with repeated keys, the page maximum as the key limit, and the missing keys listed.
**Values chosen without a source.** Path form, operationId, `missingKeys`, the 200-key limit.

**Operation count after batch E.** `rwb-source-data.yaml` `x-service.operations` goes from 32 to 36: `GET /retention-runs/{runId}/review-items` (RD-P1-092), the two extension-facts GETs (RD-P1-094) and `GET /accounts` (RD-P1-097).

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-098 · Sandbox contract files and bootstrap: interim build

_Original text of batch E kept for audit. Amendments and the final ruling follow it._

**Question.** The sandbox contract files and build identities are open (GAP-3481 to GAP-3486; RR E1065-CON#1).

**Sources.** REG v2 RD-P1-046, RD-P1-073; RWB-P1-E1065-APP s7-s8 (shape table); RWB-P1-E1065-CON s11, s12.8.

**Ruling (interims; each gap stays open with its owner, blocks build: No).**
1. **GAP-3481 (files).** RWB-P1-E1065-CON s11 publishes, for `seed-profile.json`, `case-seed-list.csv` and `shape-table.csv`, a column and key table generated from the files the build produces now: every key present is required; its type is the generated JSON or CSV type; the `shape_id` values are the 11 rows of RWB-P1-E1065-APP s7-s8 and the `product_group` codes are those used there. Build report: JSON. Checksum: SHA-256 over the file bytes as written (UTF-8, LF), every column included. The contract test of AC2 compares a build with this table.
2. **GAP-3482 (list read).** The build reads `GET /admin/lists/{listCode}` from the rwb-case contract fake (RD-P1-011) in DEV and the pipeline test; the real read waits for the build identity.
3. **GAP-3483 (target gate).** Pipeline parameter `sandboxTarget`; the allow-list of hosts is the pipeline variable group of DEV and the pipeline test; any other host fails the build before a connection is opened.
4. **GAP-3484 (bootstrap).** In DEV and the pipeline test one bootstrap principal of the environment (the pipeline's DEV database administrator login) runs CREATE DATABASE `rwb_sandbox`, the `recovery` views, the grants on `public` and `recovery`, the role creation and ALTER VIEW OWNER as a step before Flyway, and acts as the sandbox build identity of RD-P1-089 rule 4. Outside those two environments the principal is the ACE DBA's (Pending).
5. **GAP-3485.** Unchanged (already blocks build: No).
6. **GAP-3486.** `rwb_sandbox_read` is a NOLOGIN group role with SELECT on the sandbox schemas; individual DEV logins are granted membership; the Entra group mapping waits, and the human extraction test is out of Done until it is mapped.

**Affected stories.** RWB-P1-E1065-CON, RWB-P1-E1065-APP, RWB-P1-E1065-DB, RWB-P1-E1069-DB, RWB-ITG-E1065-ITG.
**Affected documents.** Gap Register v3 (GAP-3481, GAP-3482, GAP-3483, GAP-3484 and GAP-3486 set to blocks build: No with these interims).
**Findings settled.** RWB-P1-E1065-CON#1 (re-review).
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** A sandbox interim never reaches beyond DEV and the pipeline test.
**Values chosen without a source.** Parameter name; the bootstrap step; the NOLOGIN role.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-099 · ACE additions: foreign-key delete rules, orphan rows and load order (interim)

_Original text of batch E kept for audit. Amendments and the final ruling follow it._

**Question.** RWB-P1-ACE001-DB AC15 states the D-RCV-35 account cascade; the ON DELETE of the other foreign keys (hearing to lawsuit, npa_sale to npa_asset, three tables to asset, party_product to customer), the orphan rejection and the load order are Pending (GAP-3576; RR ACE001-DB#4).

**Sources.** RWB-P1-ACE001-DB v3 lines 220-229, 452; ACE Field Gap List v2 sheet ACE additions (Key column); D-RCV-35 (account cascade); PS v9 (own foreign keys use ON DELETE RESTRICT).

**Ruling (interim; GAP-3576 stays open for confirmation by the ACE team lead, blocks build: No).**
1. `hearing` → `lawsuit`: ON DELETE CASCADE, so that the D-RCV-35 account delete that cascades to `lawsuit` completes; the Given of AC15 adds hearing rows and its Then asserts that they are deleted.
2. Every other new foreign key (`npa_sale` → `npa_asset`, the three tables → `asset`, `party_product` → `customer`): ON DELETE RESTRICT.
3. An ingested row whose parent key is absent is rejected alone (not the whole file) and written to the ingestion job's reject log with its key; AC14 asserts that the row is not stored and the rest of the file is.
4. Load order of the ingestion jobs: parents before children – `customer`, `account`, `asset`, `npa_asset`, `lawsuit`, then their children.

**Affected stories.** RWB-P1-ACE001-DB, RWB-P1-E1069-DB.
**Affected documents.** ACE Field Gap List v2 (note); Gap Register v3 (GAP-3576 interim).
**Findings settled.** RWB-P1-ACE001-DB#4 (re-review).
**Status.** Proposed – Claude Opus 5.5 (applied); confirmation by the ACE team lead pending.
**Reuse note.** New ACE keys restrict deletes, except where an existing cascade must keep working.
**Values chosen without a source.** All four rules (interim).

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## RD-P1-100 · Smaller rulings: snapshot(page), SCR-44 route, holder pair, delivery status name, EFS rows, complaints, DM012 to DM014

_Original text of batch E kept for audit. Amendments and the final ruling follow it._

**Ruling.**
1. **`snapshot(page)` (RR E1013-APP#2; GAP-3425, GAP-3384).** P9 has not published the activity, its dated fields, sort, cursor or page size. RWB-P1-E1013-APP takes `snapshot(page)` and AC6 out of its Done; the activity is added by a later change of the story once RWB-P9-E1013-CON publishes it. Pending, owner P1 contract owner with the rwb-reporting owner (GAP-3425, blocks build: No).
2. **SCR-44 route (RR AD018-OPS#1; GAP-0516, ASM-0708).** The gateway-bff composite route is not published; route registration and AC13 leave the RWB-P1-AD018-OPS release and are not a release stop. Pending, owner gateway-bff contract owner (RWB-PLT-N001-CON), GAP-0516.
3. **Holder pair (RR E2034-APP#1).** `toHolderRef` is required on CASE_ALLOCATED (`fromHolderRef` optional); both are required on CASE_TRANSFERRED; both are optional on HANDOVER; on any other event code a holder field answers 422 MSG-GEN-007 naming the field (RD-P1-009 rows 02 and 03). RWB-P1-E2034-APP X4, BR2, step 4 and the ACs, the YAML description and the append of RWB-P3-E2034-APP align.
4. **Delivery status name (RR E1068-APP#1, document; GAP-3477).** The property is `latestDeliveryStatus` (RD-P1-064). Derivation per `externalRef`: the `deliveryStatus` of the entry with the latest `occurredAt`, ties broken by the highest `caseSeq`. `barcodeStatus` is removed from the YAML; RWB-P1-E1068-APP adds the AC.
5. **EfsHistoryRow (RR E2001-APP#1, document).** Every `EfsHistoryRow` property except `efsRecordKey`, `idempotencyKey` and `contactAt` is nullable in the YAML, and the fake is re-published (follows the story; no new rule).
6. **EFS ledger filter (GAP-3375).** P1 owns `efs_ledger_outcome` (DL29), so `GET /efs-history` applies the filter and answers only the rows that are to be appended; the P2 hand-over run appends every row it is given (RD-P1-067). The filter content stays with DL29, owner data architect with the solution architect (GAP-3375, blocks build: No).
7. **Complaints (GAP-3327).** RD-P1-064 keeps complaints Pending; X1 and AC5 of RWB-P10-E1062-APP leave its Done until GAP-3327 is closed.
8. **DM012 (RR DM012-APP#1).** The legacy hash, rule and version fields travel only in the extract file and the cutover evidence until GAP-3547 (NEW-GAP-S13-4) is closed (RD-P1-068 rule 1); AC1, BR2 and s11 say so.
9. **DM013 (RR DM013-APP#1, #2).** No source names the column that matches a Workbench write-off decision to a GL write-off: **Pending, owner rwb-writeoff owner with the data owner**, NEW-GAP-E4. Interim: RWB-P1-DM013-APP migrates the decisions without the write-off resolution and stamp, and its fixture drops them. The selection per part is the story's: the open matches of proceeds, the cases closed in the migration window and the write-off decisions of those cases.
10. **DM014 (RR DM014-APP#1, #2).** The comparison uses only what `GET /admin/lists/{listCode}` answers (version number, valid-from, rows), with the count and hash computed by P1. The scope is the seven rows of section 9.4 of RWB-DM-014; the rows rwb-case does not answer stay Pending under GAP-0238.

**Affected stories.** RWB-P1-E1013-APP, RWB-P9-E1013-CON, RWB-P1-AD018-OPS, RWB-PLT-N001-CON, RWB-P1-E2034-APP, RWB-P3-E2034-APP, RWB-P1-E1068-APP, RWB-P1-E2001-APP, RWB-P2-E2001-APP, RWB-P10-E1062-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P8-DM013-APP, RWB-P1-DM014-APP.
**Affected documents.** API Specification v7 `rwb-source-data.yaml` (`latestDeliveryStatus`, `EfsHistoryRow` nullability, holder description); Gap Register v3 (NEW-GAP-E4).
**GAP/ASM.** New NEW-GAP-E4. GAP-3425, GAP-0516, GAP-3375, GAP-3327 and GAP-0238 stay open, non-blocking with these interims.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** Out of Done with a pending item is better than a guessed contract.
**Values chosen without a source.** The derivation tie-break; the DM013 interim.

#### Register amendments

- None. No other decision contradicts this ruling.

**Final ruling (register).** As ruled above, unchanged.

---

## Batch D verdicts, amendment list and new gap rows

The sections below are batch D's own text, kept word for word. The amendments it lists are applied in this register (XD-01 to XD-06).

### Verdicts on "Extra stories to edit"

| Entry | Verdict |
|---|---|
| RWB-PLT-E1044-CON | Agree: remove the migration-run record and the job-view fake (RD-P1-065 rule 5, RD-P1-012). |
| RWB-P3-E2021-APP | Agree: it writes no delivery entry; rwb-comms is the one appender (RD-P1-064 rule 6). |
| RWB-P3-E2016-CON | Agree: replace the GAP-0716 citation with RD-P1-007 (and RD-P1-064). |
| RWB-P10-E1062-APP | Agree: same ledger-read alignment as its CON (`GET /cases/{caseId}/interactions`); complaint signal Pending (RD-P1-064 rule 12). |
| rwb-deviation (S8) stories taking deceased/bankrupt flags off AceDataReady | Agree: the one such story in Story Files v2 is RWB-S8-E1020-APP; flags come from `GET /customers/{personKey}` (RD-P1-060 rule 5). |
| RWB-P6-E2021-CON | Agree: proof of delivery is the P1 read used by rwb-comms, not an INT-15 result from rwb-integration (RD-P1-064 rule 14). |
| RWB-P6-E4036-CON | Agree: match E4036-APP; customer facts through `GET /customers/{personKey}` masked (RD-P1-060). |
| RWB-P8-E4044-APP, -CON, RWB-P8-E4045-APP (full review) | Agree: ACE boundary fix per RD-P1-066 rule 1. |
| RWB-P3-E2006-APP (full review) | Agree: reads `GET /data-products/freshness?product=`, `GET /accounts/{accountKey}`, `GET /collateral/{assetKey}` (RD-P1-060, RD-P1-063 rule 2). |
| S2 shallow edits (E1011 APP/CON/OPS, E1013 APP) re-run as S2b | Agree (process step; apply RD-P1-061 and RD-P1-065 in the re-run). |

### Verdicts on the check lists

| Check | Verdict |
|---|---|
| Wrong GAP numbers in AD018-APP v3 and AD019-APP v3 (GAP-3280, -3272, -3276, -3275) | Agree to check; verified now: no GAP-327x or GAP-328x citation remains in staged AD018-APP, AD019-APP, E1001-APP, E2010-APP or E1017-CON (AD018-APP line 10 records the replacement). Keep in the finishing pass for other v3 stories. |
| E1065 APP/CON/DB must not rename the sandbox database | Agree; verified: the three staged stories use `rwb_sandbox` (RD-P1-046). No edit needed. |
| E1066-APP AC15 missing key → MSG-PLT-N009-03 | Agree; verified: X8 row and AC15 cite MSG-PLT-N009-03 and -05. No edit needed. |
| Decision-record asyncapi carries `rwb.decision.DecisionRecorded.v1` | Agree; verified (lines 51, 98). Done. |
| GAP-3283 cited by E1001-APP and E2010-APP | Agree; verified: no staged story cites GAP-3283 now. The E1001 subject (NEW-GAP-F12-1) still needs a register row from the orchestrator. |
| E1066-APP event code outside the list → MSG-GEN-007 | Agree; verified: line 219 answers 422 MSG-GEN-007. No edit needed. |
| E1017-CON cites GAP-3271 for holdReport | Agree; verified: the staged E1017-CON no longer cites GAP-3271. The holdReport point belongs to RD-P1-047. |
| Staged source-data AsyncAPI still 5.0.0 with key caseId (item 34) | Disagree with the premise: staged file is 5.1.0 with key `{sourceSystem}:{businessDate}` (RD-P1-063 rule 1). |
| Re-run W9 graph after story editing | Agree (RD-P1-074 rule 3). |
| Service Contract Catalog section 6.1 to match Service Catalog v2 | Agree (RD-P1-063 rule 9). |

### Register amendments to add (for the orchestrator)

- RD-P1-003: consumer list adds rwb-integration (JOB-08) – RD-P1-066 rule 3.
- RD-P1-007 rule 7: `externalRef` = barcode (else noticeRef), key `LETTER-<caseNo>-<yyyyMMdd>-<uuid5(podKey)>` – RD-P1-064 rule 4.
- RD-P1-010 rule 8: `/efs-history` gate is DP01 and DP05 – RD-P1-067 rule 1.
- RD-P1-020: `rwb_source_data` has the library `decision_record` table – RD-P1-068 rule 8.
- RD-P1-027: act-time snapshot CARRY class; DF-LEG-005 KEY; DM002 clause moves to DM005 – RD-P1-068 rules 2-4.
- RD-P1-040: JOB-08 is rwb-integration's – RD-P1-066 rule 3.

### New gap rows (temporary IDs, next free GAP numbers after GAP-3282)

| Temp ID | Subject | Owner | Decision |
|---|---|---|---|
| NEW-GAP-D1 | Masking rule rows unmasking `firstName`, `lastName`, `contactValue` (ADDRESS) for the rwb-comms notice and rwb-integration outbound-file workload identities | Data protection officer with the rwb-access owner | RD-P1-060 |
| NEW-GAP-D2 | MSG-P1-001 wording for a product never stamped | Error and Message Standard owner | RD-P1-062 |
| NEW-GAP-D3 | Mapping of WIN `delivery_status` to SENT, DELIVERED, READ, FAILED | rwb-comms owner with the WIN interface owner | RD-P1-064 |
| NEW-GAP-D4 | Parameter `handover.hold_until` (catalog row, value) | rwb-integration owner with RW-COE | RD-P1-067 |
| NEW-GAP-D5 | Cut of build chains deeper than 4 | Solution architect | RD-P1-074 |

## Batch E verdicts, amendment list and new gap rows

The sections below are batch E's own text, kept word for word. The amendments it lists are applied in this register (XE-01 to XE-23).

### Verdicts on the re-review Blocker rows owned by a story or document (no ruling needed)

| Row | Verdict |
|---|---|
| RWB-P1-ACE001-DB#1 | Story: take the extra-column rule, type and length from sheet ACE additions. |
| RWB-P1-DM001-APP#1, #2 | Story: rewrite on the published `Account` schema (RD-P1-060); no gate; 200 with DP01 freshness STALE (RD-P1-062). |
| RWB-P1-DM009-APP#1 | Story: add `case_account` to the dump read (read, not carried); the account's case is its `case_account` row with `linked_to` null, the primary row first. |
| RWB-P1-E1016-CON#1 | Story: regenerate section 11 from the Physical Schema v9 seed (RD-P1-075) and add an automated comparison. |
| RWB-P1-E1018#1 | Story: `totalBalance` BigDecimal scale 2, nullable; the currency unit stays with GAP-3405. |
| RWB-P1-E2010-APP#2, RWB-P1-E2010-OPS#1 | Story: the DP04 tables are created by RWB-P1-E1001-APP (PS v9); E2010 only writes them; add the dependency. |
| RWB-P1-E1064-CON#1 (document) | Document owner (API contract): add enums, maxLength, required flags, ETag headers and the 422 to the YAML. |

### Register amendments to add (applied in register v3)

- RD-P1-002: child start policies of `ReconciliationWorkflow` and `Stage2ProductWorkflow`; `AceLateCheckStart` – RD-P1-078.
- RD-P1-004: one exception, `GET /batch-status` with no row → 404 MSG-P1-001 – RD-P1-085.
- RD-P1-006: first write with `If-None-Match: *`; GET of the extension facts – RD-P1-094 (clarification).
- RD-P1-007: `appendMigrated` cutover entry point – RD-P1-090 (clarification).
- RD-P1-020 D: dictionary rows of a new table come with its migration – RD-P1-096 rule 1.
- RD-P1-025: baseline copied from Physical Schema v9; `is_personal` per RD-P1-076 – RD-P1-075.
- RD-P1-040: child starts and Schedule starts (RD-P1-078); XD-11 confirmed with its mechanism and the TWAC R18 text (RD-P1-079).
- RD-P1-041: item 4 time trigger for DAILY and WEEKLY only; item 7 single stamp component with `stampDp04` for DP04; GAP-0511 line (RD-P1-081); AceDataLate status null and in-place re-completion (RD-P1-083).
- RD-P1-043: the ready call starts no run while the flag is off – RD-P1-080.
- RD-P1-045: item 4 first-release rollback answers – RD-P1-080.
- RD-P1-060: rule 2 masking default by classification – RD-P1-076; rule 3 phone and email for rwb-comms – RD-P1-077.
- RD-P1-065: rule 3 read with RD-P1-079.
- RD-P1-068: rule 6 DP04 stamped by `stampDp04` after the build – RD-P1-081.
- RD-P1-072: access-log path – RD-P1-091 (clarification).
- RD-P1-073: protection and rebuild mechanism – RD-P1-089 (clarification).

### New gap rows (temporary IDs, next free GAP numbers after GAP-3580)

| Temp ID | Subject | Owner | Decision |
|---|---|---|---|
| NEW-GAP-E1 | Data Classification rows for the 27 dictionary fields absent from DCPI v6 (DF-INT-030, DF-REF-274 to DF-REF-299) | Data protection officer | RD-P1-076 |
| NEW-GAP-E2 | Retention archive container per environment and the prefix-scoped write-once role of the rwb-source-data workload identity | Solution architect with platform security | RD-P1-092 |
| NEW-GAP-E3 | Service row codes of workload identities used as `role_code` in `data_product_access` | rwb-access owner with the data steward | RD-P1-095 |
| NEW-GAP-E4 | Column that matches a Workbench write-off decision to a GL write-off in the DM013 migration | rwb-writeoff owner with the data owner | RD-P1-100 |
| NEW-GAP-E5 | Confirmation of the classification-keyed masking default (Restricted masked without a rule; Confidential and Internal returned within scope) | Data protection officer | RD-P1-076 |

### Gap register dispositions

- **Closed:** GAP-0512, GAP-0529, GAP-0579, GAP-2170, GAP-3274, GAP-3288, GAP-3390, GAP-3395, GAP-3403, GAP-3409, GAP-3412, GAP-3430, GAP-3434, GAP-3438, GAP-3443, GAP-3445, GAP-3454 (valuation_ext stays with GAP-3279), GAP-3457, GAP-3487, GAP-3489, GAP-3492, GAP-3493, GAP-3494, GAP-3496, GAP-3506, GAP-3523, GAP-3525, GAP-3528, GAP-3529, GAP-3541, GAP-3555.
- **Kept open, blocks build changed to No with the stated interim:** GAP-3322, GAP-3327, GAP-3338, GAP-3375, GAP-3407, GAP-3411, GAP-3418, GAP-3421, GAP-3422, GAP-3429, GAP-3446, GAP-3471, GAP-3481, GAP-3482, GAP-3483, GAP-3484, GAP-3486, GAP-3524 (narrowed to the active states), GAP-3571, GAP-3576.
- **Widened:** GAP-3283 (PHONE and EMAIL for rwb-comms). **Confirmed:** GAP-0490, GAP-0597.

## Companion files

- `Recovery Workbench P1 Decision Register v3.csv`: one row per decision (71 rows) with the final ruling, amended_by, the values chosen without a source and the escalation items; the header of v2.
- `Recovery Workbench P1 Decision Register v2.md` and `.csv`: the v2 register, unchanged.
- `decisions\batch-E.md` and `.csv`: batch E as written (RD-P1-075 to RD-P1-100).
- `Recovery Workbench P1 Decision Register v1.md` and `.csv`: the v1 register, unchanged.
- Batch E new temporary gaps NEW-GAP-E1 to NEW-GAP-E5 are in the batch E section above; the orchestrator assigns GAP numbers after GAP-3580.
- `Affected stories outside P1 v1.csv`: the 289 story keys outside RWB-SVC-P1 of v1, unchanged. The stories outside P1 that batch D adds are in the `affected_stories` column of the v2 CSV.
- `New gaps and assumptions from decisions v1.csv`: the 34 temporary rows of v1, unchanged. Batch D's new temporary gaps NEW-GAP-D1 to NEW-GAP-D5 are in the table above; the orchestrator assigns GAP numbers after GAP-3282.

## Change log

| Version | Date | Change | By |
|---|---|---|---|
| v1 | 27 November 2026 | Register created from batches A, B and C; 27 cross-batch resolutions (X-01 to X-28; X-05 merged into X-04) applied as amendments; D-RCV-60 P1 developer readiness (RD-P1 register) | Chief architect (design sub-agent), Claude Opus 5.5 |
| v2 | 27 November 2026 | Batch D (RD-P1-060 to RD-P1-074) added in full; its amendments applied to RD-P1-003, RD-P1-007, RD-P1-010, RD-P1-020, RD-P1-027 and RD-P1-040; orchestrator amendments to RD-P1-004 (messageCode pattern), RD-P1-007 and RD-P1-064 (DM005 in-process caller) and RD-P1-024 (rwb-case-caselist-daily in the catalogs); two further resolutions found while merging (XD-10 RD-P1-001 / RD-P1-070, XD-11 RD-P1-040 / RD-P1-065); story keys filled for RD-P1-064, RD-P1-065, RD-P1-068, RD-P1-070 and RD-P1-073; index, lookup header and CSV (escalation_items) updated; D-RCV-60 P1 developer readiness (RD-P1 register) | Chief architect (design sub-agent), Claude Opus 5.5 |
| v3 | 27 November 2026 | Batch E (RD-P1-075 to RD-P1-100) added in full; 23 register resolutions XE-01 to XE-23 applied as amendment lines and final-ruling additions to RD-P1-002, RD-P1-004, RD-P1-006, RD-P1-007, RD-P1-009, RD-P1-020, RD-P1-024, RD-P1-025, RD-P1-040, RD-P1-041, RD-P1-042, RD-P1-043, RD-P1-045, RD-P1-047, RD-P1-048, RD-P1-060, RD-P1-064, RD-P1-065, RD-P1-068, RD-P1-069, RD-P1-072 and RD-P1-073; XD-11 confirmed with its mechanism (RD-P1-079); index, lookup tables, numbering and CSV updated; D-RCV-60 P1 developer readiness (RD-P1 register) | Chief architect (design sub-agent), Claude Opus 5.5 |
