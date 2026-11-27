SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench P2 Integration

Technical specification. SCB Collections and Recovery. Henka Group, 22 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD P2 Integration |
| Document ID | P2-RWB-TSD-v4 |
| Version | 4 |
| Status | Draft |
| Date | 22 November 2026 |
| Supersedes | Version 3, 15 November 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads (GAP-1999; ASM-3225: no squad is named per service) |
| Decision | D-RCV-60 microservice realignment; D-RCV-35 (U1 to U5), ADR-010 |
| Status note | Draft: no approval of version 4 is recorded (GAP-1998; ASM-3217) |
| Change | 4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |

| Version | Date | Change |
|---|---|---|
| 2 | 28 October 2026 | Module specification with inbound file adapters, outbound files and the outbox |
| 3 | 15 November 2026 | D-RCV-35: the Workbench loads no source data (U1). P2 becomes outbound only. Inbound interfaces INT-01 to INT-16 are re-owned by ACE ingestion (ACE team) and the Workbench reads them through `recovery.v_ace_*` views. The inbound file adapter, `interface_run` and `interface_signoff` are removed; `interface_config` is kept for outbound interfaces only; `party_product` is replaced by the ACE Tier 2 view `v_ace_party_product`; `efs_ledger_outcome` stays as in Physical Schema v5. API-P2-013 and API-P2-014 are retired |
| 4 | 22 November 2026 | D-RCV-60 microservice realignment: T0 Service, T5.2 as contracts, Ownership Map v1 owners |

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench FSD P2 Integration | FSD | Pair |
| Recovery Workbench Target Architecture | Architecture | Parent |
| Recovery Workbench Interface Specifications v3 | Architecture | Source of T5.1 and the outbound file checks |
| Recovery Workbench System Disposition and Integration Inventory v3 | Architecture | Source of the interface owners in T5.1 |
| Recovery Workbench Logical Data Model and Data Dictionary v7 | Data | Source of T3 |
| Recovery Workbench Physical Schema v5 | Data | Source of the T3 physical types and the views |
| Recovery Workbench ACE Data Tier Map v1 | Data | Frozen read-path and tier map |
| Recovery Workbench ACE DB Alignment Change Register v1 | Governance | Decision record for this version |
| Recovery Workbench API Specification | API | Source of appendix T-A |
| Recovery Workbench Microservice Ownership Map v1 | Ownership | Owner of every table, endpoint, event, workflow and job in T0 and T5.2 |

## Existing capability check

| Capability | Verdict | Owning document | Note |
|---|---|---|---|
| Inbound source data (ALS, SCBPDM, UDP, AAL, EFS, COLLINS models, LIT, CCMS, SVAF, AMIS, RPS, WIN proof of delivery, GL, NLEADS, EasyApp) | REUSE | ACE ingestion, RWB-ACE-001 (ACE team) | ACE lands the data; the Workbench runs no inbound load, file check, run record or sign-off |
| Read path into ACE data | REUSE | RWB-E1-069, TSD P1 | SELECT-only `recovery.v_ace_*` views; P2 reads them and never a `public` table |
| Sign-in, access check, audit, PII and SOC logging | REUSE | ACE common module | Called through the published interface |
| Notification path for SMS and LINE | REUSE | ACE common module | INT-17 and INT-18 |
| Scheduler and batch | REUSE | ACE pattern: Quartz and Spring Batch | Jobs in the Batch and Scheduling Design; no new `qrtz_` or `batch_` table |
| Outbound file adapter | NEW | This document, RWB-E1-007 | Outbound files only |
| Outbox and retry | NEW | Error Handling and Resilience Standard | Built in P2 for the recovery module |
| Rules evaluation | REUSE | Rules Engine Design | Through the rules component |

Under D-RCV-60 the scheduler and batch row is delivered by the Temporal layer (ADR-016): Temporal Schedules and event-started workflows in the owning service replace the Quartz and Spring Batch jobs (DP-10). The outbox and retry row is delivered by the Kafka outbox, inbox and retry topics (ADR-015; DP-09).

## T0. Service

P2 Integration is one of the 19 services of Architecture v5: `rwb-integration` (service name Integration, module P2, wave 1, service epic `RWB-SVC-P2`). Version 4 adds this section so that the specification is read as the specification of one service: its identity, what it owns, and the decoupling patterns that replace the monolith's in-process calls. Every owner is taken from Microservice Ownership Map v1 and every identifier from Template and Rules R4 (ADR-013, ADR-014).

P2 is the only holder of the outbound file adapters and the ACE integration paths; it owns no inbound interface since D-RCV-35.

### T0.1 Service identity

| Item | Value |
|---|---|
| Module | P2 Integration |
| Service | `rwb-integration` (Integration) |
| Service epic | `RWB-SVC-P2` |
| Wave | 1 |
| Schema | `rwb_integration` |
| Database login | `rwb_integration`: one login per service, with its own connection pool cap |
| REST base | `/api/recovery/integration/v1` |
| Kafka topic | `rwb.integration.events.v1`, with `.retry` and `.dlt` topics |
| Event names | `rwb.integration.<Event>.v1`, CloudEvents 1.0 in binary mode, key `caseId` |
| Temporal | namespace `rwb-recovery`; task queue `rwb-integration` |
| Java package | `th.co.scb.ace.workbench.recovery.integration` |
| Edge | gateway-bff for the operations screens; no partner traffic |
| Contract artefacts | `05 Technical architecture/Recovery Workbench API Specification v5/rwb-integration.yaml`; `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-integration.asyncapi.yaml` |
| Suggested owner, app development | TechX (suggested; any team may pick up this story) |
| Suggested owner, ACE DB | ACE team (suggested; any team may pick up this story) |

### T0.2 What this service owns

Architecture v5 slide 41 gives this service: interface config, file runs, outbound items, ACE integration paths. Table T0.2 states the same ownership in the form the Ownership Map uses, with the counts this specification carries. A table that the map assigns to another service is not built here, whatever T3 says (see the note under T3).

| Area | Owner and artefact | Count |
|---|---|---|
| Business tables in `rwb_integration` | `interface_config`, `job_catalog`, `outbound_item` | 3 |
| REST operations | appendix T-A and `rwb-integration.yaml` | 9 |
| Events published | FileDelivered, FileFailed | 2 |
| Workflows and schedules | none in the Ownership Map sheet; T5.2.1 names deliverFile(manifest), receiveFile | 2 |
| Jobs | none | 0 |

### T0.3 Decoupling patterns applied

The left column is the pattern of Template and Rules R5.5; the middle column quotes the line of this specification that carries the legacy marker, where one is present; the right column is what replaces it in this service.

| DP | Legacy marker in this specification | How the service lands it |
|---|---|---|
| DP-01 | `…recovery service identity holds SELECT on the 'recovery.v_ace_*' views only and no right on any 'public'…` | Owns its tables in `rwb_integration`; no other service reads them (ADR-014). |
| DP-02 | — | One login, `rwb_integration`, with its own connection pool cap. |
| DP-03 | `…on events from P3 and writes through the decision log. Its two record lifecycles:` | Local decision record plus DecisionRecorded (EV-08) on `rwb.decision-record.v1`. |
| DP-05 | `…postings and the Workbench reads them through 'v_ace_write_off'.` | Reads ACE through the `rwb-source-data` contract or its own `v_ace_*` views (ADR-010). |
| DP-07 | `DF-OPS-138 / direction / LOV / varchar(8) / Yes / LOV-DIRECTION / Workbench` | Reference data and lists of values from the `rwb-case` contract (H RWB-PLT-E1043-CON). |
| DP-08 | `RW-COE Center of excellence analyst / R` | Authorisation through the `rwb-access` authorise contract and the guard library (H RWB-PLT-E1037-CON). |
| DP-09 | `- the application event outbox, its deliveries and retries, and…` | Outbox and inbox library; CloudEvents on `rwb.integration.events.v1` with retry topics and `.dlt`. |
| DP-10 | `Scheduler and batch / REUSE / ACE pattern: Quartz and Spring Batch / Jobs in the Batch and…` | Temporal Schedules and event-started workflows through the workflow kit (ADR-016). |
| DP-11 | `…reaches other modules only through their published interfaces and other systems only through the outbound…` | One REST hop, 2 s timeout, breaker; the consumer builds against the provider's fake (ADR-020). |
| DP-13 | `API-P2-001 / GET / /api/recovery/v1/admin/outbound-items / Platform administration…` | REST base `/api/recovery/integration/v1`. |
| DP-14 | — | Topic `rwb.integration.events.v1`, retry topics and `.dlt`; naming library (H RWB-PLT-E1047-CON). |
| DP-15 | `Two migrations / Tier 1 views ship with RWB-E1-069 (V0002).…` | Per-service Flyway sequence in `rwb_integration`. |
| DP-16 | `- the outbound file adapter for WIN notices (INT-14), the data…` | Files through the `rwb-integration` contract (C RWB-P2-E1007-CON). |
| DP-17 | `…file adapter for WIN notices (INT-14), the data lake and Power BI copy (INT-19), the COLLINS…` | No data lake: reporting reads events; the lake copy is removed (ADR-018). |
| DP-18 | `- the EFS ledger outcome reference list.` | Interaction ledger owned by `rwb-source-data` (default ruling; DP-18). |
| DP-19 | `'v_ace_batch_status' / 2 / Job catalog screen / Last complete ACE business date per source,…` | Screens composed by gateway-bff; one composite route per screen (H RWB-PLT-N001-CON). |

### T0.4 What this service is not

- It holds no other service's table and no ACE table beyond the read-only `recovery.v_ace_*` views (DP-01, DP-05).
- It runs no shared Quartz job and touches no ACE batch table (DP-10; ADR-016).
- It receives no inbound file: every inbound interface lands in ACE and is read through the views (D-RCV-35).
- It is not a monolith module: the published Java interface of T2 is replaced by the contract set of T5.2 (DP-11; ADR-020).

## T1. Architecture overview

P2 Integration is delivered as the service `rwb-integration` (module P2, wave 1, service epic `RWB-SVC-P2`): one repository, one pipeline, one schema `rwb_integration` with one login, behind gateway-bff (ADR-013, ADR-014). Since D-RCV-35 it is outbound only. It covers:

- the outbound file adapter for WIN notices (INT-14), the data lake and Power BI copy (INT-19), the COLLINS model-learning feed through the data lake (INT-20) and the debt buyer data tape (INT-25);
- the application event outbox, its deliveries and retries, and the outbound exception queue;
- use of the paths ACE already runs: the notification path for NSS and LINE OA (INT-17, INT-18), PII Kafka, audit and SOC logging (INT-22) and the ACE common module (INT-34);
- the platform tables the module shares: idempotency keys, feature flags and the job catalog;
- the EFS ledger outcome reference list.

P2 takes no source data in. Every inbound interface lands in the ACE database through ACE's own ingestion and is owned by the ACE team. P2 reaches other modules only through the contracts of T5.2 and other systems only through the outbound adapter and the ACE paths.

The outbound interfaces in P2 scope are exactly INT-14, INT-19, INT-20 and INT-25, plus the ACE paths INT-17, INT-18, INT-22 and INT-34 (Interface Specifications v3). Two related interfaces are not P2 outbound work:

- INT-16 GL write-off is inbound: ACE ingestion (ACE team) lands the monthly write-off postings and the Workbench reads them through `v_ace_write_off`.
- INT-03 core bank bookings are manual: the officer books the restructure, settlement or write-off in the core bank, and the booking is confirmed on the next ACE batch through `v_ace_account`.

### T1.1 The ACE read path

P2 does not own the read path, but it reads through it and must keep to its rules (Tier Map section 1):

| Rule | What it means for P2 |
|---|---|
| One read surface | P2 reads source data only through `recovery.v_ace_*` views. A direct `public.*` read in P2 code or SQL is a defect and fails the TE-001 boundary test |
| No write | The recovery service identity holds SELECT on the views and nothing else in `public`; P2 never writes to an ACE table |
| No foreign key into ACE | P2 links to source records by business key (`person_key`, `account_key`), never by a UUID foreign key, because ACE cascades deletes on `account` |
| Freshness | The business date of each source comes from `v_ace_batch_status`. The recovery data engine (P1) stamps `data_product_load` and publishes EV-27 AceDataLate; P2 does not check inbound files |
| Two migrations | Tier 1 views ship with RWB-E1-069 (V0002). Tier 2 views, including `v_ace_party_product` and `v_ace_credit_decision`, ship with V0003 once RWB-ACE-001 lands; the P2 features that read them stay behind their flags until then |

Views P2 reads:

| View | Tier | Read by | For |
|---|---|---|---|
| `v_ace_plan` | 1 | API-P2-010 | ACE restructure plan status |
| `v_ace_efs_action_code` | 1 | `efs_ledger_outcome` maintenance | Valid EFS action codes |
| `v_ace_efs_action` | 1 | Interaction ledger build (P6), filtered by `efs_ledger_outcome` | Which EFS actions enter the ledger and on which channel |
| `v_ace_party_product` | 2 | API-P2-011 | Other products the case's borrowers hold |
| `v_ace_credit_decision` | 2 | API-P2-012 | NLEADS credit result shown with the credit pack |
| `v_ace_batch_status` | 2 | Job catalog screen | Last complete ACE business date per source, for display only |

## T2. Component design

| Component | Responsibility |
|---|---|
| IntegrationController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| IntegrationService | Business logic; calls the rules component; writes the decision log entry before any change |
| OutboundFileAdapter | Builds each outbound file from its `interface_config` version, runs the outbound file checks (layout, control totals), sends it by SFTP, records the acknowledgement and holds the waiting case steps until it arrives |
| OutboxRelay | Reads `outbox_event` rows committed with the change, creates one `outbox_delivery` per consumer, delivers with the retry intervals and raises a RESOLVE_OUTBOX_DELIVERY task on the last failure |
| IntegrationRepository | Reads and writes the module's tables only |
| AceViewReader | Read-only access to the `v_ace_*` views listed in T1.1; no other ACE access |
| Jobs | Outbound file runs as Temporal workflows and the outbox relay of the platform library (DP-09, DP-10); the data lake publish is removed (DP-17) |
| Published interface | The contracts of T5.2: the outbound file activities and the operational operations; no table is read across modules (DP-11) |

The inbound FileLoadAdapter of version 2, with its file checks, run record and manual-retirement sign-off, is removed. Its checks are now the ingestion contract ACE passes (Interface Specifications v3, "Checks ACE ingestion passes").

The published interface of this table is the contract set of T5.2: the REST operations, the events and the workflows, not a Java interface in a shared classpath (DP-11; ADR-020). Components that the Ownership Map places in another service are stated in T0.2 and T5.2 and are built by that service.

## T3. Data model

Every object of T3 that Microservice Ownership Map v1 assigns to `rwb-integration` lives in schema `rwb_integration` with the standard columns of T3.0 (DP-01, DP-15; ADR-014). T3.1 mixes three kinds of object: the business tables `interface_config`, `outbound_item` and `job_catalog` (P2 in the Ownership Map); the platform tables `outbox_event`, `outbox_delivery`, `processed_event`, `idempotency_key`, `feature_flag` and `feature_flag_change`, which belong to the shared libraries and not to a service schema (DP-09, DP-15); and `efs_ledger_outcome`, which the Ownership Map places with P1 (GAP-1992; ASM-3219). `party_product` is read from ACE and is not a table of this service.

### T3.0 Standard record columns

| Column | Type | Meaning |
|---|---|---|
| is_active | boolean | The active or inactive status of the record |
| state | varchar(40) | Record lifecycle state |
| version | integer | Optimistic lock version |
| created_at | timestamptz | When the record was created |
| created_by | uuid | Who or which service identity created it |
| updated_at | timestamptz | When the record last changed |
| updated_by | uuid | Who or which service identity last changed it |

### T3.1 Object and field definitions

**interface_config** (KEPT, outbound only). The settings of one outbound file interface, by version. Rows exist only for Workbench-owned outbound interfaces (INT-14, INT-19, INT-20, INT-25), so `direction` is always OUTBOUND, `transport` is SFTP and `inbound_path` holds the outbound folder. The column names are as in Physical Schema v5.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-136 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-137 | interface_id | TEXT | varchar(10) | Yes | None | Workbench |
| DF-OPS-138 | direction | LOV | varchar(8) | Yes | LOV-DIRECTION | Workbench |
| DF-OPS-139 | transport | LOV | varchar(10) | Yes | LOV-TRANSPORT | Workbench |
| DF-OPS-140 | inbound_path | TEXT | varchar(200) | No | None | Workbench |
| DF-OPS-141 | file_pattern | TEXT | varchar(120) | No | None | Workbench |
| DF-OPS-142 | data_product | LOV | varchar(25) | No | LOV-DATA-PRODUCT | Workbench |
| DF-OPS-143 | max_attempts | NUMBER | integer | Yes | None | Workbench |
| DF-OPS-144 | retry_intervals_min | TEXT | varchar(60) | No | None | Workbench |
| DF-OPS-145 | owner_role | LOV | varchar(20) | Yes | LOV-ROLE | Workbench |
| DF-OPS-146 | alert_role | LOV | varchar(20) | No | LOV-ROLE | Workbench |
| DF-OPS-147 | valid_from | DATE | date | Yes | None | Workbench |
| DF-OPS-148 | valid_to | DATE | date | No | None | Workbench |

**interface_run** and **interface_signoff** (REMOVED). Removed from Physical Schema v5 by D-RCV-35. There is no inbound run in the Workbench; outbound runs are recorded on `outbound_item` and `outbox_delivery`, and inbound sign-off moves to the ACE team in RWB-ACE-001. Field IDs DF-OPS-149 to DF-OPS-167 are retired and not reused.

**outbound_item** (NEW). One outbound file waiting to be sent, sent or in the exception queue.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-168 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-169 | interface_id | TEXT | varchar(10) | Yes | None | Workbench |
| DF-OPS-170 | idempotency_key | TEXT | varchar(120) | Yes | None | Workbench |
| DF-OPS-171 | payload_ref | ATTACHMENT | varchar(400) | Yes | None | Workbench |
| DF-OPS-172 | case_ids | TEXT | jsonb | No | None | Workbench |
| DF-OPS-173 | attempt_count | NUMBER | integer | Yes | None | Workbench |
| DF-OPS-174 | next_attempt_at | DATE | timestamptz | No | None | Workbench |
| DF-OPS-175 | status | LOV | varchar(12) | Yes | LOV-OUTBOUND-STATUS | Workbench |
| DF-OPS-176 | last_error | TEXT | varchar(400) | No | None | Workbench |
| DF-OPS-177 | owner_role | LOV | varchar(20) | Yes | LOV-ROLE | Workbench |

**processed_event** (NEW). An event or work key a consumer has already processed, so a repeat is ignored and counted.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-178 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-179 | consumer | TEXT | varchar(60) | Yes | None | Workbench |
| DF-OPS-180 | idempotency_key | TEXT | varchar(120) | Yes | None | Workbench |
| DF-OPS-181 | event_id | CROSS_REF | uuid | No | None | Workbench |
| DF-OPS-182 | hit_count | NUMBER | integer | Yes | None | Workbench |
| DF-OPS-183 | last_seen_at | DATE | timestamptz | No | None | Workbench |

**idempotency_key** (NEW). The stored response of an API request sent with an Idempotency-Key header, kept 24 hours.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-184 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-185 | idempotency_key | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-186 | endpoint | TEXT | varchar(100) | Yes | None | Workbench |
| DF-OPS-187 | request_hash | TEXT | char(64) | Yes | None | Workbench |
| DF-OPS-188 | response | TEXT | jsonb | Yes | None | Workbench |

**outbox_event** (NEW). An application event or outbound work request written in the same transaction as the change.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-189 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-190 | event_type | TEXT | varchar(40) | Yes | None | Workbench |
| DF-OPS-191 | schema_version | NUMBER | integer | Yes | None | Workbench |
| DF-OPS-192 | case_id | CROSS_REF | uuid | No | None | Workbench |
| DF-OPS-193 | case_seq | NUMBER | bigint | No | None | Workbench |
| DF-OPS-194 | idempotency_key | TEXT | varchar(120) | Yes | None | Workbench |
| DF-OPS-195 | payload | TEXT | jsonb | Yes | None | Workbench |
| DF-OPS-196 | actor_ref | TEXT | varchar(64) | No | None | Workbench |
| DF-OPS-197 | occurred_at | DATE | timestamptz | Yes | None | Workbench |

**outbox_delivery** (NEW). The delivery of one outbox event to one consumer, with its retries.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-198 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-199 | event_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-OPS-200 | consumer | TEXT | varchar(60) | Yes | None | Workbench |
| DF-OPS-201 | status | LOV | varchar(12) | Yes | LOV-OUTBOX-DELIVERY | Workbench |
| DF-OPS-202 | attempt_count | NUMBER | integer | Yes | None | Workbench |
| DF-OPS-203 | next_attempt_at | DATE | timestamptz | Yes | None | Workbench |
| DF-OPS-204 | last_error_code | TEXT | varchar(40) | No | None | Workbench |
| DF-OPS-205 | delivered_at | DATE | timestamptz | No | None | Workbench |
| DF-OPS-206 | task_id | CROSS_REF | uuid | No | None | Workbench |

**feature_flag** (NEW). A feature flag with its value per environment, owner and removal date.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-207 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-208 | flag_key | TEXT | varchar(80) | Yes | None | Workbench |
| DF-OPS-209 | description | TEXT | varchar(400) | Yes | None | Workbench |
| DF-OPS-210 | owner_user_id | USER_REF | uuid | Yes | None | Workbench |
| DF-OPS-211 | owner_team | TEXT | varchar(60) | No | None | Workbench |
| DF-OPS-212 | default_on | BOOLEAN | boolean | Yes | None | Workbench |
| DF-OPS-213 | dev_on | BOOLEAN | boolean | Yes | None | Workbench |
| DF-OPS-214 | sit_on | BOOLEAN | boolean | Yes | None | Workbench |
| DF-OPS-215 | uat_on | BOOLEAN | boolean | Yes | None | Workbench |
| DF-OPS-216 | prod_on | BOOLEAN | boolean | Yes | None | Workbench |
| DF-OPS-217 | removal_date | DATE | date | Yes | None | Workbench |

**feature_flag_change** (NEW). One change of a feature flag value in one environment.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-218 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-219 | flag_key | TEXT | varchar(80) | Yes | None | Workbench |
| DF-OPS-220 | environment | LOV | varchar(4) | Yes | LOV-ENVIRONMENT | Workbench |
| DF-OPS-221 | old_value | BOOLEAN | boolean | Yes | None | Workbench |
| DF-OPS-222 | new_value | BOOLEAN | boolean | Yes | None | Workbench |
| DF-OPS-223 | reason | TEXT | varchar(400) | Yes | None | Workbench |

**job_catalog** (NEW). A scheduled job with its owner, run book and expected duration. The inbound load jobs leave the catalog with D-RCV-35; ACE ingestion jobs are ACE's and are not catalogued here.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-224 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-225 | job_id | TEXT | varchar(6) | Yes | None | Workbench |
| DF-OPS-226 | job_name | TEXT | varchar(80) | Yes | None | Workbench |
| DF-OPS-227 | owner_role | LOV | varchar(20) | Yes | LOV-ROLE | Workbench |
| DF-OPS-228 | schedule_text | TEXT | varchar(120) | Yes | None | Workbench |
| DF-OPS-229 | runbook_path | TEXT | varchar(200) | No | None | Workbench |
| DF-OPS-230 | expected_minutes | NUMBER | integer | No | None | Workbench |
| DF-OPS-231 | alert_after_minutes | NUMBER | integer | No | None | Workbench |
| DF-OPS-232 | first_release | TEXT | varchar(3) | No | None | Workbench |

**party_product** (REMOVED; read from ACE). The Workbench copy of the customer product holding (DF-PTY-022 to DF-PTY-027) leaves Physical Schema v5. The holding is a Tier 2 ACE table, `public.party_product` (SCBPDM, raised in RWB-ACE-001), read through **`v_ace_party_product`** (Section B, view B11). API-P2-011 reads the view below, joined to the case's borrowers on `person_key`, with no foreign key.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-ACE-280 | person_key | TEXT | varchar(255) | No | None | ACE `party_product.person_key` |
| DF-ACE-281 | account_no | TEXT | varchar(255) | No | None | ACE `party_product.account_key` |
| DF-ACE-282 | account_key | TEXT | varchar(255) | No | None | ACE `party_product.account_key` |
| DF-ACE-283 | product_type | TEXT | varchar(20) | No | None | ACE `party_product.product_type` |
| DF-ACE-284 | product_status | TEXT | varchar(15) | No | None | ACE `party_product.product_status` |
| DF-ACE-285 | data_as_of | DATE | date | No | None | ACE `party_product.business_date` |

**efs_ledger_outcome** (KEPT, per Physical Schema v5). Which EFS action codes enter the interaction ledger and on which channel. A Workbench reference table (subject area REF, data product DP14), unique on `action_code`. It is a Workbench decision about ACE data, not a copy: `action_code` takes values from `v_ace_efs_action_code`, and the interaction ledger build applies it to `v_ace_efs_action` rows. `channel` defaults to CALL and `in_ledger` to true.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-128 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-129 | action_code | LOV | varchar(10) | Yes | LOV-ACTION-CODE | Workbench |
| DF-REF-130 | channel | LOV | varchar(15) | Yes | LOV-CHANNEL | Workbench |
| DF-REF-131 | in_ledger | BOOLEAN | boolean | Yes | None | Workbench |

### T3.2 Lists of values

| List | Values | Note |
|---|---|---|
| LOV-CHANNEL | MOBILE, HOME_PHONE, WORK_PHONE, LINE, EMAIL, POSTAL_ADDRESS, CALL, VISIT, SMS, LETTER, PORTAL, BRANCH | |
| LOV-DATA-PRODUCT | DP01, DP02, DP03, DP04, DP05, DP06, DP07, DP08, DP09, DP10, DP11, DP12, DP13, DP14 | |
| LOV-DIRECTION | INBOUND, OUTBOUND | `interface_config` uses OUTBOUND only; INBOUND stays for `interaction.direction` |
| LOV-ENVIRONMENT | DEV, SIT, UAT, PROD | |
| LOV-OUTBOUND-STATUS | PENDING, SENT, RETRY, EXCEPTION, ACKNOWLEDGED | |
| LOV-OUTBOX-DELIVERY | PENDING, RETRYING, DELIVERED, EXCEPTION | |
| LOV-TRANSPORT | SFTP, COLLINS | `interface_config` uses SFTP only; COLLINS was the inbound route |
| LOV-INTERFACE-RUN | Retired with `interface_run` | |
| LOV-PRODUCT-STATUS | ACTIVE, DELINQUENT, CLOSED, WRITTEN_OFF | Display list for `v_ace_party_product.product_status`; the ACE value is not constrained by the Workbench |

### T3.3 Relationships

| From | Field | To | Cardinality |
|---|---|---|---|
| processed_event | event_id | outbox_event | Many to 0 or 1 |
| outbox_event | case_id | recovery_case | Many to 0 or 1 |
| outbox_delivery | event_id | outbox_event | Many to 1 |
| outbox_delivery | task_id | task | Many to 0 or 1 |
| notice | dispatch_file_id | outbound_item | Many to 0 or 1 |
| v_ace_party_product | person_key | case_party.person_key | Business key, no foreign key |
| efs_ledger_outcome | action_code | v_ace_efs_action_code.action_code | Business key, no foreign key |

The version 2 relationship `party_product.party_id` to `party` is removed with both tables.

## T4. State machines and workflow

No case state machine of its own; the module acts on events from P3 and writes through the decision log. Its two record lifecycles:

| Record | States | Rule |
|---|---|---|
| outbound_item | PENDING, SENT, RETRY, EXCEPTION, ACKNOWLEDGED | Sent on the next run; a failed send or failed outbound check moves to RETRY at the `retry_intervals_min` of its `interface_config` version; after `max_attempts` (three for INT-14 and INT-25) it moves to EXCEPTION and a task goes to `owner_role`; the waiting case steps resume on ACKNOWLEDGED |
| outbox_delivery | PENDING, RETRYING, DELIVERED, EXCEPTION | One delivery per event and consumer; a repeat is dropped through `processed_event`; the last failure raises a RESOLVE_OUTBOX_DELIVERY task |

A resend from the exception queue (API-P2-002, API-P2-004) sets PENDING and attempt count 0.

## T5. Integration and interfaces

### T5.1 External system interfaces

Owners and approaches follow Interface Specifications v3 and the Integration Inventory v3. Every inbound row is owned by ACE ingestion; P2 builds only the Workbench-owned outbound rows.

| ID | System | Direction | Owner and approach | Frequency |
|---|---|---|---|---|
| INT-01 | Core bank (ALS) | In, into ACE | ACE ingestion (ACE team), Workbench reads `v_ace_account` | Daily, end of day |
| INT-02 | Core bank (ALS) | In, into ACE | ACE ingestion (ACE team), Workbench reads `v_ace_payment` | Daily, end of day |
| INT-03 | Core bank (ALS) | Out | Workbench: no interface; booked by the officer, confirmed on the next ACE batch through `v_ace_account` | As approved |
| INT-04 | SCBPDM | In, into ACE | ACE ingestion (ACE team), Workbench reads `v_ace_customer` and `v_ace_contact` | Daily, end of day |
| INT-05 | UDP | In, into ACE | ACE ingestion (ACE team), Workbench reads `v_ace_account` and `v_ace_customer` | Daily, end of day |
| INT-06 | AAL | In, into ACE | ACE ingestion (ACE team), Workbench reads `v_ace_account` and `v_ace_customer` | Daily, end of day |
| INT-07 | EFS | In, into ACE | ACE ingestion (ACE team), Workbench reads `v_ace_efs_action` | Daily, end of day |
| INT-08 | COLLINS models | In, into ACE | ACE ingestion (ACE team), Workbench reads `v_ace_score` | Daily; monthly for some models |
| INT-09 | LIT | In, into ACE | ACE ingestion (ACE team), Workbench reads `v_ace_lawsuit` and `v_ace_hearing` | Daily, end of day |
| INT-10 | CCMS | In, into ACE | ACE ingestion (ACE team), Workbench reads `v_ace_collateral` and `v_ace_collateral_detail` | Weekly |
| INT-11 | SVAF | In, into ACE | ACE ingestion (ACE team), Workbench reads `v_ace_valuation` | Weekly |
| INT-12 | AMIS | In, into ACE | ACE ingestion (ACE team), Workbench reads `v_ace_npa_asset` and `v_ace_npa_sale` | Monthly |
| INT-13 | RPS | In, into ACE | ACE ingestion (ACE team), Workbench reads `v_ace_npa_asset` | Weekly |
| INT-14 | WIN | Out | Workbench (P2): outbound file through the OutboundFileAdapter | Daily |
| INT-15 | WIN | In, into ACE | ACE ingestion (ACE team), Workbench reads `v_ace_pod` | Weekly |
| INT-16 | GL | In, into ACE | ACE ingestion (ACE team), Workbench reads `v_ace_write_off` | Monthly |
| INT-17 | NSS | Out | ACE team: ACE notification path, queued by P6 | As sent |
| INT-18 | LINE OA | Out | ACE team: ACE notification path, queued by P6 | As sent |
| INT-19 | Data lake and Power BI | Out | Workbench (P2): daily batch copy | Daily |
| INT-20 | COLLINS | Out | Workbench (P2): daily batch to the data lake | Daily |
| INT-21 | Entra ID and the bank IAM | In | ACE team: ACE sign-in | At each sign-in |
| INT-22 | PII Kafka, audit and SOC logs | Out | ACE team: ACE logging, called through the common module | As they happen |
| INT-23 | Enterprise AI model endpoint | Both | Bank platform: private endpoint in the SCB tenant | Per request |
| INT-24 | Partner portal | Both | Workbench: screens through the external gateway | As entered |
| INT-25 | Debt buyers | Out | Workbench (P2): outbound file through the data room | Per lot |
| INT-26 | NLEADS | Out | Workbench: submitted by the officer in NLEADS; the decision returns through the new ACE interface | As needed |
| INT-27 | HOME.SCB | Out | Workbench: not available today; published by the sale officer | As listed |
| INT-28 | SCIS | Out | Workbench: not available today; prepared by the officer | As needed |
| INT-29 | Thai Credit Guarantee Corporation | Both | Workbench: not available today; entered and filed by the guarantee officer | As needed |
| INT-30 | NCB | In | Workbench: not available today; by the officer | As needed |
| INT-31 | Aric | Out | Workbench: not available today; by the fraud investigator | As needed |
| INT-32 | Salesforce | In | Workbench: not available today | None |
| INT-33 | Legal Execution Department and courts | In | Workbench: through the law firms in the partner portal | As entered |
| INT-34 | ACE common module | Both | ACE team: published module interface | Per request |
| New ACE interface | NLEADS | In, into ACE | ACE ingestion (ACE team), Workbench reads `v_ace_credit_decision` | As decisions are made |
| New ACE interface | EasyApp | In, into ACE | ACE ingestion (ACE team), Workbench reads `v_ace_esign` | As signatures are requested |

The two new ACE interfaces carry no INT number yet (Interface Specifications v3).

Every outbound file P2 sends passes the outbound file checks in Interface Specifications v3: layout against the agreed specification and template version, control totals against the rows, and acknowledgement by the receiver. A failed layout or totals check does not send and raises the item to the platform administrator.

### T5.2 Contracts

Version 4 states every cross-module dependency of this module as a contract, so that the service is built against a published artefact and its fake (ADR-020; DP-11). The artefact per call type is: OpenAPI 3.1 for REST, AsyncAPI 3.0 for Kafka, the Temporal interface named here for a workflow or activity, the Interface Specifications manifest for a file, the Nexus operation for the ACE restructure calculator, and a grant on the view for SQL. No row of this section reads another service's table (DP-01). Every consumed contract is class C (Template and Rules R5.4): it never blocks the build, because the consumer builds against the fake, and the real cross-service behaviour is class I work on an integration story. Architecture v5 slides 13 to 20 name a few operations differently from the published files of 22 November 2026; the published file is the artefact the fake is generated from and is the one cited here (GAP-1997; ASM-3224).

#### T5.2.1 Contracts provided

The REST operations of this service are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-integration.yaml` (5.0.0, 22 November 2026) under the base `/api/recovery/integration/v1`. Appendix T-A holds the endpoint IDs, the access right and the first release of each one.

| # | Method | Path | operationId |
|---|---|---|---|
| 1 | GET | `/admin/outbound-items` | `getAdminOutboundItems` |
| 2 | POST | `/admin/outbound-items/{itemId}/resend` | `postAdminOutboundItemsItemidResend` |
| 3 | GET | `/admin/outbox/deliveries` | `getAdminOutboxDeliveries` |
| 4 | POST | `/admin/outbox/deliveries/{deliveryId}/resend` | `postAdminOutboxDeliveriesDeliveryidResend` |
| 5 | GET | `/admin/scheduled-jobs` | `getAdminScheduledJobs` |
| 6 | GET | `/cases/{caseId}/plan-status` | `getCasesCaseidPlanStatus` |
| 7 | GET | `/cases/{caseId}/customer-products` | `getCasesCaseidCustomerProducts` |
| 8 | GET | `/treatments/{treatmentId}/credit-pack` | `getTreatmentsTreatmentidCreditPack` |
| 9 | GET | `/treatments/{treatmentId}/credit-result` | `getTreatmentsTreatmentidCreditResult` |

Workflows, schedules, files and views this service provides:

| Contract | Type | Called by or target | Note |
|---|---|---|---|
| deliverFile(manifest) | Temporal activity | P6 rwb-comms, P8 rwb-payment, P9 rwb-reporting, S6 rwb-debtsale | Contract of T5.2.1; runs on rwb-integration |
| receiveFile | Temporal activity | P2 rwb-integration | Contract of T5.2.1; runs on rwb-integration |
| WIN registered mail, daily (INT-14) | Outbound file | WIN | 16:00 file window, opened by Airflow (JOB-10) |
| Debt buyer data tape per lot, encrypted (INT-25) | Outbound file | Debt buyers | Per awarded lot, encrypted and masked (NFR-041) |

Events this service publishes (AsyncAPI 3.0, CloudEvents 1.0):

| Event | EV | Topic | Consumers |
|---|---|---|---|
| FileDelivered | — | `rwb.integration.events.v1` | requesting service |
| FileFailed | — | `rwb.integration.events.v1` | requesting service |

#### T5.2.2 Contracts consumed

| Contract | Type | Provider | Class | Failure path |
|---|---|---|---|---|
| Fetch an outbound file by ID through a time-limited SAS link | REST | P5 rwb-document | C | 2 s timeout, breaker; built against the fake (ADR-020) |

Events this service consumes:

None.

#### T5.2.3 Call-type summary

| Call type | Provided | Consumed | Artefact |
|---|---|---|---|
| REST | 9 | 1 | OpenAPI 3.1, one file per service |
| Kafka (events) | 2 | 0 | AsyncAPI 3.0, one file per service |
| Temporal | 2 | 0 | Workflow and activity interfaces, queue `rwb-integration` |
| File | 2 | 0 | Interface Specifications manifest and the SAS link |
| Nexus | 0 | 0 | Nexus operation into ACE |
| SQL | 0 | 0 | Read-only grant on the view |

A contract change is a new version of the artefact, never a code change in the consumer (ADR-020). The provider named in T5.2.2 is the owner in Microservice Ownership Map v1, and the consumer list of each event is the Arch v5 event catalogue on slides 42 and 43.

### T5.3 Events

The event contract of this service is `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-integration.asyncapi.yaml`; the shared decision-record contract is `asyncapi/rwb.decision-record.v1.asyncapi.yaml`. Every service publishes DecisionRecorded (EV-08) to `rwb.decision-record.v1` from its outbox in the same transaction as its state change (DP-03, DP-09; ADR-015, ADR-022); consuming services dedupe through their inbox table. Events carry identifiers and facts, never personal data (Event and Messaging Design v4, sheet Rules).

| Event | EV | Direction | Topic |
|---|---|---|---|
| FileDelivered | — | Published | `rwb.integration.events.v1` |
| FileFailed | — | Published | `rwb.integration.events.v1` |

An event shown with `—` has no number in the numbered catalogue: the Arch v5 catalogue calls these rows `+`, so the number is not specified in the source documents (GAP-1996; ASM-3223).

## T6. Security and access control

### T6.1 RBAC matrix

| Role | Platform administration |
|---|---|
| RW-COE Center of excellence analyst | R |
| RW-DATASTEW Data steward and data product owner | R |
| RW-AUDIT Internal audit | R |
| RW-COMPLY Compliance and PDPA officer | R |
| RW-PLATADM Platform administrator | CRUD |
| RW-SECADM Security administrator | CRUDA |

### T6.2 Authentication and authorization

Entra ID single sign-on through the ACE front end; each endpoint declares its capability area and right; scope filters every query; masking applies to personal fields; service identities for jobs and agents. The recovery service identity holds SELECT on the `recovery.v_ace_*` views only and no right on any `public` table. The SY-DATALOAD actor is removed; there is no inbound load identity. Outbound files carry personal data only as the receiving interface allows (WIN addresses, debt buyer tape per the sale terms), and every read of personal data through a view is logged to PII Kafka (INT-22).

Every operation of T5.2.1 is authorised through the `rwb-access` authorise contract with the role, the scope and the delegation limit of T6.1 (DP-08; C RWB-P4-E1037-CON); the caller caches the answer and refreshes it on AccessPolicyChanged and DoaLimitChanged.

## T7. Non-functional requirements

| ID | Requirement | Target | Status |
|---|---|---|---|
| NFR-049 | Staff authenticate with single sign-on and multi-factor authentication. | Entra ID single sign-on with multi-factor | Proposed |
| NFR-050 | Partner accounts authenticate with multi-factor and are scoped to their own cases. | Multi-factor, scoped | Proposed |
| NFR-051 | Agents run under service identities and are subject to the same role checks as people. | Service identities | Proposed |
| NFR-052 | Secrets are held in the key store and never in code, configuration files or prompts. | No secrets in code or prompts | Proposed |
| NFR-053 | Data is encrypted at rest and in transit. | Encrypted | Proposed |
| NFR-054 | The build pipeline blocks a change that carries a secret, personal data in code, tests or logs, or an unapproved dependency. | Pipeline checks pass | Proposed |
| NFR-055 | Agent outputs are schema checked against an allowed-action list with a confidence threshold, and fall back to rules when the check fails. | Schema check on every output | Proposed |
| NFR-056 | Penetration testing and a security review are completed before the first production release. | Before the first production release and before the partner portal opens to users outside the bank | Proposed, DL11 |

## T8. Requirement traceability

| Requirement | Feature | Story | Test |
|---|---|---|---|
| REQ-DRI-006 | FEAT-RDF-21 | RWB-E1-007 (rewritten: outbound files only) | TC-E1-007-01 |
| REQ-DRI-007 | FEAT-RDF-21 | RWB-E1-007 (rewritten: outbound files only) | TC-E1-007-01 |
| REQ-DRI-008 | FEAT-RDF-21 | RWB-E1-007 (rewritten: outbound files only) | TC-E1-007-01 |
| REQ-DRI-013 | None | Written one epic ahead | With the story |
| D-RCV-35 read path | None | RWB-E1-069 (views and boundary rule); RWB-ACE-001 (ACE additions) | With the story |

## Appendix T-A. API specification

### T-A.1 Endpoint inventory

| ID | Method | Path | Access | First in |
|---|---|---|---|---|
| API-P2-001 | GET | /api/recovery/integration/v1/admin/outbound-items | Platform administration R | E1 |
| API-P2-002 | POST | /api/recovery/integration/v1/admin/outbound-items/{itemId}/resend | Platform administration U | E1 |
| API-P2-003 | GET | /api/recovery/integration/v1/admin/outbox/deliveries | Platform administration R | E1 |
| API-P2-004 | POST | /api/recovery/integration/v1/admin/outbox/deliveries/{deliveryId}/resend | Platform administration U | E1 |
| API-P2-005 | GET | /api/recovery/integration/v1/feature-flags | None R | E1 |
| API-P2-006 | GET | /api/recovery/integration/v1/admin/feature-flags | Platform administration R | E1 |
| API-P2-007 | POST | /api/recovery/integration/v1/admin/feature-flags | Platform administration C | E1 |
| API-P2-008 | PATCH | /api/recovery/integration/v1/admin/feature-flags/{flagKey} | Platform administration U | E1 |
| API-P2-009 | GET | /api/recovery/integration/v1/admin/scheduled-jobs | Platform administration R | E1 |
| API-P2-010 | GET | /api/recovery/integration/v1/cases/{caseId}/plan-status | Case record R | E2 |
| API-P2-011 | GET | /api/recovery/integration/v1/cases/{caseId}/customer-products | Case record R | E2 |
| API-P2-012 | GET | /api/recovery/integration/v1/treatments/{treatmentId}/credit-pack | Treatment and offer R | E2 |
| API-P2-013 | - | Retired in v3 | - | - |
| API-P2-014 | - | Retired in v3 | - | - |

The operation IDs, paths and operationIds of these endpoints are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-integration.yaml`; where an appendix row and the published operation differ, the published operation is the contract of T5.2.1 and the row keeps its ID for traceability (GAP-1997; ASM-3224).

### T-A.2 Endpoint detail

#### API-P2-001 GET /admin/outbound-items

| Item | Value |
|---|---|
| Purpose | List outbound file items by status and interface for the exception queue |
| Request | Query: status, interfaceId, from, to |
| Response | OutboundItem[] |
| Errors | 401, 403, 503 |
| Authorization | Platform administration, right R, scope applied |
| Idempotency | Not applicable |

#### API-P2-002 POST /admin/outbound-items/{itemId}/resend

| Item | Value |
|---|---|
| Purpose | Send an outbound item in the exception queue again: status PENDING, attempt count 0 |
| Request | None |
| Response | OutboundItem |
| Errors | 401, 403, 404, 409, 503 |
| Authorization | Platform administration, right U, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P2-003 GET /admin/outbox/deliveries

| Item | Value |
|---|---|
| Purpose | List application event outbox deliveries by status and consumer |
| Request | Query: status, consumer, eventType, from, to, page, size |
| Response | OutboxDeliveryPage |
| Errors | 401, 403, 503 |
| Authorization | Platform administration, right R, scope applied |
| Idempotency | Not applicable |

#### API-P2-004 POST /admin/outbox/deliveries/{deliveryId}/resend

| Item | Value |
|---|---|
| Purpose | Send an outbox delivery in the exception queue again: status PENDING, attempt count 0 |
| Request | None |
| Response | OutboxDelivery |
| Errors | 401, 403, 404, 409, 503 |
| Authorization | Platform administration, right U, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P2-005 GET /feature-flags

| Item | Value |
|---|---|
| Purpose | Read the effective feature flag values for the caller's environment |
| Request | None |
| Response | FeatureFlagValue[] |
| Errors | 401, 503 |
| Authorization | None, right R, scope applied |
| Idempotency | Not applicable |

#### API-P2-006 GET /admin/feature-flags

| Item | Value |
|---|---|
| Purpose | List feature flags with values per environment, owner and removal date |
| Request | Query: overdue, owner |
| Response | FeatureFlag[] |
| Errors | 401, 403, 503 |
| Authorization | Platform administration, right R, scope applied |
| Idempotency | Not applicable |

#### API-P2-007 POST /admin/feature-flags

| Item | Value |
|---|---|
| Purpose | Create a feature flag |
| Request | FeatureFlagRequest |
| Response | FeatureFlag |
| Errors | 401, 403, 409, 422, 503 |
| Authorization | Platform administration, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P2-008 PATCH /admin/feature-flags/{flagKey}

| Item | Value |
|---|---|
| Purpose | Change a feature flag value for one environment with a reason |
| Request | FeatureFlagChange |
| Response | FeatureFlag |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Platform administration, right U, scope applied |
| Idempotency | Not applicable |

#### API-P2-009 GET /admin/scheduled-jobs

| Item | Value |
|---|---|
| Purpose | List the job catalog with owner, schedule, run book and alert threshold; shows the last complete ACE business date per source from `v_ace_batch_status` for reference |
| Request | None |
| Response | JobCatalogEntry[] |
| Errors | 401, 403, 503 |
| Authorization | Platform administration, right R, scope applied |
| Idempotency | Not applicable |

#### API-P2-010 GET /cases/{caseId}/plan-status

| Item | Value |
|---|---|
| Purpose | Read the ACE restructure plan status of the case from `v_ace_plan`, with fallback to the status stored on the case (`plan_status`, `plan_status_as_of`) |
| Request | None |
| Response | PlanStatus |
| Errors | 401, 403, 404, 503 |
| Authorization | Case record, right R, scope applied |
| Idempotency | Not applicable |

#### API-P2-011 GET /cases/{caseId}/customer-products

| Item | Value |
|---|---|
| Purpose | Read the other products of the case's borrowers from `v_ace_party_product`, joined on `case_party.person_key`, masked by role; returns `data_as_of` with each row |
| Request | None |
| Response | CustomerProducts |
| Errors | 401, 403, 404, 503 (also when the Tier 2 view is not yet deployed and the flag is off) |
| Authorization | Case record, right R, scope applied |
| Idempotency | Not applicable |

#### API-P2-012 GET /treatments/{treatmentId}/credit-pack

| Item | Value |
|---|---|
| Purpose | Assemble the credit approval pack for submission in NLEADS; includes the NLEADS reference, result, reason and decision date from `v_ace_credit_decision` once a decision has been ingested |
| Request | None |
| Response | CreditPack |
| Errors | 401, 403, 404, 503 |
| Authorization | Treatment and offer, right R, scope applied |
| Idempotency | Not applicable |

#### API-P2-013 (retired)

Version 2 recorded the NLEADS reference, result, approval level and reason on the treatment by hand. D-RCV-35 routes the NLEADS decision through ACE (`credit_decision`, read through `v_ace_credit_decision`) and removes the four `treatment` columns, so the Workbench no longer writes the result. The decision is read with API-P2-012.

#### API-P2-014 (retired)

Version 2 signed off the end of manual file handling for an inbound interface into `interface_signoff`. Both the table and the inbound interfaces leave the Workbench; inbound sign-off is the ACE team's in RWB-ACE-001, and spreadsheet retirement moves to the Cutover plan (U5).

## Appendix T-B. Open technical decisions

| Decision | What is needed |
|---|---|
| DL06 | Option A (daily batch through COLLINS) is superseded by D-RCV-35. Still open: which outbound interfaces need same-day sending |
| DL11 | Non-functional target values |
| DL35 | Deployment slots |
| DL43 | ACE team acceptance of the RWB-ACE-001 scope and dates; blocks the Tier 2 views `v_ace_party_product`, `v_ace_credit_decision` and `v_ace_batch_status` that API-P2-009, API-P2-011 and API-P2-012 read |

## Document sign-off

| Role | Name | Signature | Date |
|---|---|---|---|
| Solution architect | | | |
| Tech lead | | | |
| ACE team | | | |
| QA lead | | | |
