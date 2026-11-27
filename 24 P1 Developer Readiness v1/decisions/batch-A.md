# P1 developer readiness – decision register, batch A

Decisions RD-P1-001 to RD-P1-012 of the D-RCV-60 P1 developer-readiness run for service epic RWB-SVC-P1 (rwb-source-data). Batch A covers the contract rulings: idempotency, the Temporal and Kafka catalogs, the error envelope, the published OpenAPI and AsyncAPI, update concurrency, the interaction ledger append and intake, the case-entry read, contract fakes and the job monitor. IDs RD-P1-013 to RD-P1-019 of this batch's range are not used.

Precedence applied throughout (RUN_BRIEF hard rule 6): D-RCV-60 and Architecture v5 (SET\22 Microservice Realignment) > RD-P1 decisions > 16 Temporal and Drools Adoption (D-RCV-36) > 15 ACE DB Alignment (D-RCV-35, ADR-010) > 14 Story Updates > all other documents. Where two documents of the last tier conflict, the ruling names the stale one.

Abbreviations used in the source lists: Arch v5 = Recovery Workbench Architecture v5 Text Extract v1; T&R = Recovery Workbench Microservice Story Template and Rules v1; LDM v10 = Logical Data Model and Data Dictionary v10 (extract in REVIEW\_reference\06 Data); Kafka catalog = Kafka Topic and Event Catalog v2; Temporal catalog = Temporal Workflow and Activity Catalog v2; SCC v2 = Service Contract Catalog v2; API v6 = API Specification v6 folder; GR v2 / AR v2 = Gap Register v2 / Assumptions Register v2.

---

## RD-P1-001 · One idempotency standard for every REST POST of rwb-source-data

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

---

## RD-P1-002 · Temporal catalog and P1 story names for workflows and activities

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

---

## RD-P1-003 · Kafka catalog: AceDataReady and AceDataLate grain, key and outbox; P1 consumer registrations and ACLs

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

---

## RD-P1-004 · The error envelope is the published Problem schema, extended once

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

---

## RD-P1-005 · One contract file per service; wire names, enums and required flags of rwb-source-data 5.1.0

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

---

## RD-P1-006 · Optimistic concurrency on PUT and PATCH

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

---

## RD-P1-007 · Interaction ledger: one writer, one append contract

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

---

## RD-P1-008 · Event type name of DecisionRecorded

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

---

## RD-P1-009 · Ledger intake: consumed-event map, identity, filtering, retry and parking, ordering

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

---

## RD-P1-010 · Case-entry read contract: listEligibleAccounts (not entry-candidates) and the hand-over reads

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

---

## RD-P1-011 · What counts as a published contract fake for DoR item 22, and version pinning

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

---

## RD-P1-012 · Job monitor and rerun: owner, job set, list shape and rerun request

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
