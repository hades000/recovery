# P1 developer readiness: decision register, batch B (RD-P1-020 to RD-P1-028)

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Run | D-RCV-60 P1 developer readiness (RD-P1 register) |
| Batch | B: data model, ownership, identifiers, case list, dictionary baseline, access seed, migration mapping, parameter catalog |
| Decision IDs | RD-P1-020 to RD-P1-028 (RD-P1-029 to RD-P1-039 not used by this batch) |
| Role | Solution architect and data architect (design sub-agent) |
| Model | Claude Opus 5.5 (claude-opus-5-5) |
| Precedence | D-RCV-60 and Architecture v5 > RD-P1 decisions > 16 Temporal and Drools Adoption (D-RCV-36) > 15 ACE DB Alignment (D-RCV-35, ADR-010) > 14 Story Updates > all other documents |

Conventions used in every ruling below.

- "Story" means the story file `04 User stories/Recovery Workbench Service Story Files v2/<epic folder>/<file> v2.md`.
- Field IDs: the next free numbers in Logical Data Model and Data Dictionary v10 (LDM v10), sheet Fields, were checked before allocation: DF-OPS ends at DF-OPS-232 and DF-REF ends at DF-REF-299 (DF-REF-274 to DF-REF-299 are the D-RCV-36 rule tables). New IDs start at DF-OPS-233 and DF-REF-300.
- Every new table carries the seven standard columns of LDM v10 sheet Standard columns (`is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by`); they are not repeated in the column lists.
- New tables follow the Physical Schema v8 conventions: `id uuid PRIMARY KEY DEFAULT gen_random_uuid()`, constraint names `uk_<table>`, index names `ix_<table>_<purpose>`, a cross-service reference is a plain uuid or business key with no foreign key.
- A new list of values is a closed list owned by P3 rwb-case and read through RWB-P3-E1043-CON (DP-07), as every P1 list in Reference Data and Lists of Values v5, sheet Reference data starter.
- Where a value had to be chosen because no source gives it, the ruling says "Proposed" for that value.

**Cross-batch consistency (for the orchestrator).** Checked against batch A and batch C as written on 27 November 2026.
- Aligned: RD-P1-020 follows RD-P1-012 for the job set, `Job` fields (`runNo`, `workflowId`, `durationMinutes`, `checks` as `{expected, actual, passed}` = `expected_count`, `check_count`, `check_result = 'PASS'`) and the run-ID rerun; RD-P1-022 follows RD-P1-002 and RD-P1-040 for the workflow grain and IDs (`ace-ingest-check-{businessDate}`, `recon-{businessDate}`, one 05:30 Schedule); RD-P1-028 agrees with RD-P1-042 (`recon.tolerance.pct` 0.00).
- **Conflict to settle:** RD-P1-012 rule 2 and 4, RD-P1-040 items 4 and 5 and RD-P1-048 keep `CaseListBuildWorkflow`, `case_list_row`, `DailyCaseList` and the checks ROWS_BELOW_ENTRY, ALLOCATION_COMPLETE, PUBLISHED in P1. RD-P1-024 (theme TH-69, assigned to this batch) rules that the case list leaves P1 under Architecture v5 and the GAP-2228 directive resolution. If RD-P1-024 stands, those parts of RD-P1-012, RD-P1-040 and RD-P1-048 lapse and `ReconciliationWorkflow` (`recon-{businessDate}`) is started as a child of `AceIngestCheck` after the ALS stamp, its REC-01 step first waiting for rwb-case allocation with the poll and the 07:15 limit that RD-P1-040 item 4 gives the case-list build. If the orchestrator overturns RD-P1-024, RD-P1-020 C, RD-P1-021 (records operation step 4) and RD-P1-022 (REC-05 key source) keep working unchanged, and only RD-P1-024 and the "checks leave P1" sentences of RD-P1-020 B are withdrawn.

---

## RD-P1-020 · Run, readiness and load-state records of rwb-source-data

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

---

## RD-P1-021 · One owner per table, product, seed and write across P1 and its neighbours

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

---

## RD-P1-022 · One owner each for reconciliation, freshness stamps, events, gate and readiness

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

---

## RD-P1-023 · Case identifier in paths, queries and payloads

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

---

## RD-P1-024 · Case list: P3 rwb-case holds the list, P1 drops `case_list_row`

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

---

## RD-P1-025 · Data dictionary baseline: counts, data product seed text and release checks

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

---

## RD-P1-026 · RW-COMPLY read of DP02 in access version DPA-2026.11

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

---

## RD-P1-027 · Migration package field mapping, allow-list and provenance columns

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

---

## RD-P1-028 · Parameter catalog for P1: where parameters live, their owner route, and what replaces the empty file

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
