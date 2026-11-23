SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench — realignment v5 context (19 services in ACE)

**Context ID:** `CTX-REALIGN-RWB-V5`
**Version:** 3.0 (realignment v5), 22 November 2026
**Owner:** Context Updater (this file). Business truth: `project-context.md`; backend technical truth:
`backend-context.md`; frontend/UI/design truth: `frontend-context.md`; test and verification truth:
`testing-standards.md`; coding standards: `backend-standards.md`, `frontend-standards.md`.
**Source of truth:** `Recovery Workbench Architecture v5 Text Extract v1` (51 slides),
`Recovery Workbench Temporal and Drools Design Text Extract v1` (32 slides),
`Recovery Workbench Microservice Story Template and Rules v1` (§R1–§R9),
`Recovery Workbench Microservice Ownership Map v1` and `_work/msr/plan/ownership.json`,
`_work/msr/plan/split_plan.json`, `_work/msr/plan/ids.json`, and the 16 November 2026 context package
(`CONTEXT-20261116`).
**Status:** `READY` as a Draft context (`ASM-5682`: every AI-drafted artefact stays Draft until the
later verification loop). Arch v5 is the target architecture for this run; the six
decisions still open on Arch v5 slide 39 and the "for discussion" items are recorded in §14 and in
the assumption register. Evidence labels: `IMPLEMENTED`, `DOCUMENTED/REQUIRED`, `USER-PROVIDED`,
`RECOMMENDED`, `N/A`.

## 1. Purpose, precedence and what this file replaces

This file is the v5 context of the D-RCV-60 microservice realignment. It records the business,
architectural and delivery facts that change when the Workbench moves from one deployable module
inside ACE to **19 services inside ACE**, one per BA module, with a schema and login each, Kafka
business events, a shared Temporal layer and rules governed in `rwb-decision`.

**What it is not.** It does not replace the five canonical context files. It states the v5 delta,
fixes the owner of every service, table, endpoint, event, job and workflow, and lists the conflicts
that the v2 files still carry. The v2 files remain the long-form context for business rules,
front-end design and test levels; where they contradict this file and the v5 sources, this file and
the v5 sources win (gap `GAP-0019`).

### 1.1 Source precedence (R-PREC, Template and Rules §R3)

| Order | Source |
|---|---|
| 1 | Arch v5 catalogue slides (services, resources, call types: slides 13–20 and 41–44) |
| 2 | Recovery Temporal and Drools Detailed Design v1 |
| 3 | Arch v5 narrative slides |
| 4 | Decision Log (latest version) |
| 5 | Architecture Decision Records (latest version) |
| 6 | Technical Specifications by Module (latest version) |
| 7 | Functional Specifications by Module (latest version) |
| 8 | Physical Schema and Logical Data Model (latest version) |
| 9 | The story masters |

When two sources disagree, the higher one wins; the loser becomes a Conflict gap row and an
assumption row.

### 1.2 Default rulings (Template and Rules §R3)

| Item | Owner | Assumption |
|---|---|---|
| Parameters and reference data (E1-042, E1-043) | P3 `rwb-case` | `ASM-5675` |
| Case list API | P3 `rwb-case` | `ASM-5676` |
| Rule package registry | P7 `rwb-decision` | `ASM-5677` |
| Interaction ledger | P1 `rwb-source-data` | `ASM-5678`, `ASM-0067` |
| Feature flags | Platform library (PLT) | `ASM-5679`, `ASM-0073` |

### 1.3 Realignment decisions and IDs

| Item | Value | Note |
|---|---|---|
| Run decision | `D-RCV-60` | D-RCV-53 is already used in folder 21; `_work/msr/plan/ids.json` records the collision |
| Architecture decisions | `ADR-013` to `ADR-023` | 11 ADRs; each supersedes or amends the decision named in §13.4 |
| Decision Log rows | `DL44` to `DL49` | Adopt Arch v5; service epics with business-epic tags; soft ownership; Epic 1 preservation; dates unchanged and tentative; gap and assumption registers |
| Highest ID before this run | `D-RCV-59` | `ids.json` `max_used.drcv` |

## 2. Business overview in the v5 model

The Workbench is the recovery module of SCB's ACE collections service. It runs one case from
90 days past due to close. Recovery stays part of ACE: same AKS cluster, same Azure App Gateway,
same ACE Common shared services and the same ACE PostgreSQL server. Recovery has **no connection to
the data lake**; INT-19 and INT-20 are removed.

| Item | Value | Evidence |
|---|---|---|
| Product | Recovery Workbench, 19 services inside ACE | Arch v5 slides 1–2 |
| Business owner | SCB Collections and Recovery | Arch v5 slide 1 |
| Delivery partner | Henka Group with TechX squads | Arch v5 slide 1; Template and Rules §R1 |
| Case entry | Loan 90+ days past due, unless excluded | Arch v5 slide 3; package ENTRY/EXCLUSION |
| Case exit | Paid, settled, sold or written off | Arch v5 slide 3 |
| Routes | 8 routes, some run together | Arch v5 slide 3 |
| Service count | 19 services, 4 reading groups | Arch v5 slides 4 and 41 |
| Delivery model | Wave 0 platform, then waves 1–4 with the epics | Arch v5 slide 38 |
| Programme duration | Within 8 months, dates unchanged and tentative | Template and Rules §R1 U7 |

**The journey (Arch v5 slide 3).** 1 Enter (`rwb-source-data`) → 2 Take over (`rwb-case`: case
created overnight, allocated by 07:00) → 3 Choose route (`rwb-valuation`: valuation and rules
propose, an approver signs off) → 4 Work the route (route services) → 5 Collect (`rwb-payment`:
money matched and posted) → 6 Close (`rwb-case`).

**The eight routes.** Restructure, Settlement and Deed in lieu (`rwb-treatment`, S2); Guarantee
claim (`rwb-guarantee`, S3); Litigation (`rwb-litigation`, S4); Asset sale (`rwb-asset`, S5); Debt
sale (`rwb-debtsale`, S6); Write-off (`rwb-writeoff`, S7).

**Always on.** Special situations X1–X7 (`rwb-deviation`, S8) pause the stage clock but never the
legal prescription clock (R-DEV-01); approvals, the 50 bank-wide universal rules and the decision
log (`rwb-decision`, P7) apply at every step.

### 2.1 Volumes and service targets (Arch v5 slides 33, 48)

| Measure | Value |
|---|---|
| Open cases | 23,570 today (23,600 on slide 33); 26,479 by end 2027; 47,389 by 2031 |
| New cases | ~3,110 a month |
| Concurrent internal users | 414 at peak; ~21 requests a second |
| Partner users | 320 total; 48 concurrent |
| Documents | 64–74k a month; 2.8 TB by 2031; OCR target 500 pages an hour |
| Rule evaluations | 283–318k a month |
| Decision-log entries | 55–62k a month |
| Route work a month | 1,909 registered letters; 667 lawsuits filed; 720 repossessions; ~315 debt-sale accounts; 29 property sales |
| Screen response | < 2 s at the 95th percentile; the case screen is budgeted at about 1.2 s |
| Rule evaluation | < 300 ms |
| AI agent | 60 s, then the rule result (R-UNI-32) |
| Availability | 99.9% in business hours |
| RPO / RTO | Not set in NFR Spec v3 (gap `GAP-0015`; `ASM-5666` keeps the plan default until resolved) |

### 2.2 What changed since Arch v4 (Arch v5 slide 1 notes)

Recovery stays in ACE; `recovery-core` is split into 19 services (one per business module) so each
can be repurposed later; no database per service — one ACE database with one schema per service; no
data lake; Kafka is the event broker; the Temporal layer is redrawn in five layers so other
workbenches can reuse it.

## 3. Scope

**In scope:** the 19 services and their contracts, schemas, topics, task queues and workflows; the
shared platform pieces they use (gateway-bff, Temporal, Kafka, the bank Airflow, observability,
Key Vault codec server, Blob WORM); the ACE Common connections; the realignment of the documents,
BRDs, PRDs, story files, ADRs and Decision Log.

**Out of scope / removed:** the data lake and the Power BI feed (INT-19, INT-20 removed); a database
per service (a schema per service is used instead); 19 Temporal clusters (one shared cluster with a
namespace per workbench); a shared rules server on the hot path (rules are evaluated inside the
owning service); the shared Quartz tables for Recovery jobs.

## 4. Service catalogue (19 services)

Owner of every service row is the service itself (the Ownership Map "Services" sheet). REST base is
`/api/recovery/<short>/v1` behind gateway-bff (Template and Rules §R4); the Java package is
`th.co.scb.ace.workbench.recovery.<short without hyphen>`; the epic is `RWB-SVC-<code>`.

| Code | Service | Arch v5 name | Group | Wave | Schema | REST base | Topic | Task queue | First API path | Reuse class |
|---|---|---|---|---|---|---|---|---|---|---|
| P1 | `rwb-source-data` | Source data | Data & AI | 1 | `rwb_source_data` | `/api/recovery/source-data/v1` | `rwb.source-data.events.v1` | `rwb-source-data` | `/customers/{id}` | With configuration (as the pattern for reading ACE) |
| P2 | `rwb-integration` | Integration & files | Shared capabilities | 1 | `rwb_integration` | `/api/recovery/integration/v1` | `rwb.integration.events.v1` | `rwb-integration` | `/interface-runs` | Ready as is |
| P3 | `rwb-case` | Case & workflow | Case & control | 1 | `rwb_case` | `/api/recovery/case/v1` | `rwb.case.events.v1` | `rwb-case` | `/cases/{id}` | Recovery-specific (pattern reusable) |
| P4 | `rwb-access` | Access & administration | Case & control | 1 | `rwb_access` | `/api/recovery/access/v1` | `rwb.access.events.v1` | `rwb-access` | `/authorise` | Ready as is |
| P5 | `rwb-document` | Document hub | Shared capabilities | 1 | `rwb_document` | `/api/recovery/document/v1` | `rwb.document.events.v1` | `rwb-document` | `/documents` | Ready as is |
| P6 | `rwb-comms` | Communications | Shared capabilities | 1 | `rwb_comms` | `/api/recovery/comms/v1` | `rwb.comms.events.v1` | `rwb-comms` | `/notices` | Ready as is |
| P7 | `rwb-decision` | Decision center & log | Case & control | 1 | `rwb_decision` | `/api/recovery/decision/v1` | `rwb.decision.events.v1` | `rwb-decision` | `/decisions` | Ready as is |
| P8 | `rwb-payment` | Payments & posting | Shared capabilities | 2 | `rwb_payment` | `/api/recovery/payment/v1` | `rwb.payment.events.v1` | `rwb-payment` | `/cases/{id}/payments` | With configuration |
| P9 | `rwb-reporting` | Reporting | Data & AI | 1 | `rwb_reporting` | `/api/recovery/reporting/v1` | `rwb.reporting.events.v1` | `rwb-reporting` | `/dashboards/{id}` | Ready as is |
| P10 | `rwb-agent` | Agent runtime | Data & AI | 1 | `rwb_agent` | `/api/recovery/agent/v1` | `rwb.agent.events.v1` | `rwb-agent` | `/agent-runs/{id}` | Ready as is |
| S1 | `rwb-valuation` | Valuation & route | Recovery routes | 3 | `rwb_valuation` | `/api/recovery/valuation/v1` | `rwb.valuation.events.v1` | `rwb-valuation` | `/cases/{id}/valuation` | With configuration |
| S2 | `rwb-treatment` | TDR, settlement, DIL | Recovery routes | 2 | `rwb_treatment` | `/api/recovery/treatment/v1` | `rwb.treatment.events.v1` | `rwb-treatment` | `/treatments` | Recovery-specific |
| S3 | `rwb-guarantee` | Guarantees | Recovery routes | 3 | `rwb_guarantee` | `/api/recovery/guarantee/v1` | `rwb.guarantee.events.v1` | `rwb-guarantee` | `/guarantee-claims` | Recovery-specific |
| S4 | `rwb-litigation` | Litigation & enforcement | Recovery routes | 3 | `rwb_litigation` | `/api/recovery/litigation/v1` | `rwb.litigation.events.v1` | `rwb-litigation` | `/legal-actions` | Recovery-specific |
| S5 | `rwb-asset` | Assets & auction | Recovery routes | 2 | `rwb_asset` | `/api/recovery/asset/v1` | `rwb.asset.events.v1` | `rwb-asset` | `/assets` | With configuration |
| S6 | `rwb-debtsale` | Debt sale | Recovery routes | 3 | `rwb_debtsale` | `/api/recovery/debtsale/v1` | `rwb.debtsale.events.v1` | `rwb-debtsale` | `/lots` | With configuration |
| S7 | `rwb-writeoff` | Write-off & recovery | Recovery routes | 4 | `rwb_writeoff` | `/api/recovery/writeoff/v1` | `rwb.writeoff.events.v1` | `rwb-writeoff` | `/write-offs` | Recovery-specific |
| S8 | `rwb-deviation` | Deviation handling | Case & control | 2 | `rwb_deviation` | `/api/recovery/deviation/v1` | `rwb.deviation.events.v1` | `rwb-deviation` | `/deviations` | With configuration |
| S9 | `rwb-partner` | Partner management | Shared capabilities | 4 | `rwb_partner` | `/api/recovery/partner/v1` | `rwb.partner.events.v1` | `rwb-partner` | `/partners` | With configuration |

Note: the Ownership Map "Services" sheet records the short names "Source data", "Integration",
"Case and workflow", "Access and authority", "Document", "Communications", "Decision and rules",
"Payment", "Reporting", "Agent", "Valuation and route", "Treatment and offer", "Guarantee",
"Litigation", "Asset", "Debt sale", "Write-off", "Deviation", "Partner"; the names above are the
Arch v5 slide 4 and slide 41 labels. Both sources agree on code, service, wave, schema and queue.

**Shared platform (not one of the 19, Arch v5 slides 4 and 8):** gateway-bff with a Redis session
store and a codec server (Key Vault, AES-GCM); the partner gateway in the DMZ (FAPI 2.0); the shared
Temporal cluster; the Kafka business-event topics on the bank platform; the bank Airflow scheduler
(to discuss); observability on OpenTelemetry; Blob storage with WORM for documents.

**Groups are for reading only**; they are not deployment units.

## 5. Ownership (Ownership Map v1)

Source: `_work/msr/plan/ownership.json` and `Recovery Workbench Microservice Ownership Map v1`
(sheets Services, Tables 93 rows, Endpoints 156 rows, Events 30 rows, Workflows and activities 15
rows, Jobs 22 rows, Parameters, Rulings 71 rows). Every owner below is an Ownership Map value; the
map, not this file, is the authoritative register.

### 5.1 Counts by owner

| Owner | Tables | Endpoints | Events | Jobs | Workflows |
|---|---:|---:|---:|---:|---:|
| P1 | 18 | 18 | 2 | 3 | 0 |
| P2 | 3 | 11 | 0 | 0 | 0 |
| P3 | 15 | 22 | 7 | 3 | 1 |
| P4 | 5 | 4 | 0 | 1 | 0 |
| P5 | 12 | 17 | 2 | 2 | 1 |
| P6 | 3 | 11 | 3 | 1 | 1 |
| P7 | 6 | 19 | 3 | 3 | 1 |
| P8 | 1 | 2 | 3 | 2 | 0 |
| P9 | 3 | 1 | 0 | 1 | 0 |
| P10 | 8 | 11 | 1 | 0 | 1 |
| S1 | 0 | 3 | 0 | 0 | 1 |
| S2 | 1 | 4 | 1 | 0 | 1 |
| S3 | 1 | 2 | 0 | 0 | 1 |
| S4 | 2 | 5 | 0 | 0 | 1 |
| S5 | 2 | 6 | 1 | 1 | 1 |
| S6 | 2 | 5 | 1 | 0 | 1 |
| S7 | 1 | 2 | 1 | 1 | 1 |
| S8 | 1 | 2 | 2 | 0 | 1 |
| S9 | 3 | 6 | 2 | 0 | 1 |
| PLT | 6 | 5 | 1 | 4 | 1 |
| **Total** | **93** | **156** | **30** | **22** | **15** |

### 5.2 Tables per owner (93 tables)

| Owner | Count | Tables |
|---|---:|---|
| P1 | 18 | `account_ext`, `case_list_row`, `contact_point_ext`, `data_contract`, `data_product`, `data_product_access`, `data_product_load`, `dp_guarantee_claim`, `dp_treatment`, `efs_ledger_outcome`, `interaction`, `lake_copy_watermark`, `party_ext`, `reconciliation_result`, `sys_field_version`, `sys_fields`, `sys_objects`, `valuation_ext` |
| P2 | 3 | `interface_config`, `job_catalog`, `outbound_item` |
| P3 | 15 | `assignment`, `case_account`, `case_entry_exclusion`, `case_party`, `lov_value`, `parameter_catalog`, `parameter_value`, `queue`, `queue_measure`, `queue_member`, `recovery_case`, `reference_row`, `reference_version`, `task`, `timer` |
| P4 | 5 | `delegation_limit`, `masking_rule`, `permission`, `role`, `role_conflict` |
| P5 | 12 | `case_document_check`, `document`, `document_checklist_item`, `document_custody`, `document_field`, `document_hub_parameter`, `document_intake`, `document_text`, `document_type`, `retention_action`, `retention_rule`, `signature_request` |
| P6 | 3 | `merge_field`, `notice`, `template` |
| P7 | 6 | `approval`, `decision_log_entry`, `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` |
| P8 | 1 | `proceeds` |
| P9 | 3 | `measure_definition`, `measure_publish`, `measure_snapshot` |
| P10 | 8 | `agent_alert`, `agent_evaluation`, `agent_evaluation_run`, `agent_feedback`, `agent_policy`, `agent_prompt`, `agent_run`, `agent_sample` |
| S1 | 0 | None in the map; Arch v5 slide 18 gives `rwb_valuation` valuations, the D6 route decision and route-agent output (`GAP-0014`) |
| S2 | 1 | `treatment` |
| S3 | 1 | `guarantee_claim` |
| S4 | 2 | `hearing`, `legal_action` |
| S5 | 2 | `asset_sale`, `listing` |
| S6 | 2 | `debt_sale_account`, `debt_sale_lot` |
| S7 | 1 | `write_off` |
| S8 | 1 | `deviation` |
| S9 | 3 | `partner`, `partner_instruction`, `partner_user` |
| PLT | 6 | `feature_flag`, `feature_flag_change`, `idempotency_key`, `outbox_delivery`, `outbox_event`, `processed_event` |

### 5.3 Ownership rulings carried into this context

Fifteen table rulings and the API and flow rulings are recorded in the map with one assumption and
one Conflict gap row each. The rulings a downstream story is most likely to hit:

| Item | Owner | Ruling (abridged) | Assumption |
|---|---|---|---|
| `interaction`, `efs_ledger_outcome` | P1 | Ledger and intake rule stay with P1; case timeline API stays P3; P2 reads the ledger through P1's contract | `ASM-0067` |
| `case_list_row` | P1 | P1 builds the daily row projection; the case list API and screen stay P3 | `ASM-0068` |
| `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` | P7 | Registry, rows and test cases stay with P7; services hold a local evaluated copy only | `ASM-0069` |
| `delegation_limit` | P4 | DoA table is P4; P3 keeps only non-DoA parameters and reference data | `ASM-0070` |
| `lov_value` | P3 | Reference data | `ASM-0071` |
| `partner_user` | S9 | Partner users stay with S9; P4 keeps the internal role model | `ASM-0072` |
| `feature_flag`, `feature_flag_change` | PLT | Platform library; P2 serves the admin API | `ASM-0073` |
| `outbox_event`, `outbox_delivery`, `processed_event`, `idempotency_key` | PLT | Library objects, one copy per service schema | `ASM-0074` |
| `job_catalog` | P2 | Register stays with P2; Schedules are not rows in it | `ASM-0075` |
| `retention_rule` | P5 | Retention is P5; P1 drops its copy | `ASM-0076` |
| `signature_request` | P5 | P6 requests through P5's contract | `ASM-0077` |
| `timer` | P3 | Screen projection behind the timers endpoint; the clock is a durable Temporal timer | `ASM-0078` |
| `lake_copy_watermark` | P1 | Legacy table with no target; data lake removed | `ASM-0079` |
| `dp_treatment`, `dp_guarantee_claim` | P1 | Dated DP04 copies with P1; live records with S2 and S3 | `ASM-0080` |
| `valuation_ext` | P1 | One of the four extension tables; OQ-P1-05 stays open | `ASM-0081` |
| Asset valuation endpoints | S1 | `POST /assets/{assetId}/valuations`, `POST /assets/{assetKey}/valuations` | `ASM-0043` |
| Case interaction endpoints | P1 | Ledger owner; rwb-case reads through the contract | `ASM-0038` |
| Rule package and rule-version paths | P7 | Rule registry owner | `ASM-0040` |
| List and reference-load paths | P3 | Parameters and reference data owner | `ASM-0041` |
| Feature-flag paths | PLT | Platform library; P2 serves the API | `ASM-0039` |
| Workflow smoke path | PLT | Platform smoke on the platform queue | `ASM-0042` |
| `DecisionRecorded` (EV-08) | P7 | Event type and central ledger P7; every service writes its local record | `ASM-0055` |
| `TimerDue` (EV-18) | PLT | Retired; durable timers are platform | `ASM-0056` |
| `PartnerResultSubmitted` (EV-21) | S9 | Producer and owner S9 | `ASM-0057` |
| `AceDataReady` (EV-26) | P1 | Producer and owner P1 | `ASM-0058` |
| JOB-01 / JOB-09 | P1 | Retired under D-RCV-35; the read path replaces them | `ASM-0059`, `ASM-0045`, `ASM-0047` |
| JOB-05 | PLT | No Temporal Schedule; durable timers in each workflow | `ASM-0060`, `ASM-0046` |
| JOB-10 | P6 | P6 owns the notice and the 16:00 window; P2 performs `deliverFile` | `ASM-0062`, `ASM-0048` |
| JOB-13 | P7 | Continuous Kafka ingest; daily ledger seal | `ASM-0064` |
| JOB-15 | P9 | Airflow trigger; no data lake | `ASM-0065` |
| JOB-16 | S7 | Temporal Schedule, 3rd working day | `ASM-0066` |

## 6. Call types and contracts (Arch v5 slides 11–13)

Five call types, each with a fixed contract. Every service publishes its contracts (OpenAPI,
AsyncAPI, activity jar) before code; contract tests run in every build.

| | REST | Event (Kafka) | Temporal | File | SQL view |
|---|---|---|---|---|---|
| Use when | A person waits for the answer | A fact others may react to | A step in another service, or a long process | Bulk data, or a party outside the bank | Reading ACE data (rwb-source-data only) |
| Transport | HTTPS/JSON, mesh mTLS | Kafka over TLS; CloudEvents 1.0, binary mode | Temporal gRPC over mTLS; queue `rwb-<svc>` | Blob + MFT/SFTP; PGP for outside parties | PostgreSQL TLS; read-only login |
| Contract | OpenAPI 3.1; `/v1` in the path | AsyncAPI 3.0; JSON Schema registry, backward compatible | Typed activity/workflow interface in a contract jar | Manifest: fileId, batchId, sha256, record count | 30 `recovery.v_ace_*` views (ADR-010) |
| Identity | User JWT from the BFF + workload identity | OAUTHBEARER (Entra) or mTLS; topic ACLs | Namespace mTLS; worker identity per service | SAS link, one file, 15 minutes | One login: `rwb_source_data` |
| Timeout, retry | 2 s; retry GET only (once, jitter); breaker + bulkhead | Retry topics 1 min / 10 min / 1 h, then `.dlt` + alert | Start-to-close per activity; backoff; heartbeats | Retried by the workflow; checksum on receipt | 5 s statement timeout |
| Duplicates, order | `Idempotency-Key` on every POST | Key = `caseId` (order per case); inbox dedupe | Workflow ID = business key; activities idempotent | `fileId` unique; re-delivery safe | Read only |
| Errors | RFC 9457 problem details | Dead-letter topic; replay tool | Typed failures; non-retryable list; saga undo | `FileFailed` event; operator retry | Mapped to domain errors by P1 |
| Never | Call chains (depth > 1) | Personal data in events | I/O or PII in workflow code or payloads | Data inside the message | Any other service reading the views |

**Choosing a call type:** is a person waiting (REST) → did something happen that others care about
(event) → must another service do a step and return a result (Temporal activity, child workflow or
Nexus) → bulk data or an outside party (file). Events announce, Temporal commands, REST answers
people; the three are never mixed.

### 6.1 Who calls whom (Arch v5 slide 13, outbound view)

| Service | REST calls | Temporal / Nexus | Listens to events from | SQL | File | Outside |
|---|---|---|---|---|---|---|
| P3 Case | P4 | Children on S8, S1, S2, S3, S4, S5, S6, S7; activity on P1 | P7, S8, S1–S7, P5, P6, P8, S9, P1 | — | — | — |
| P7 Decision | P4 | — (runs `ApprovalWorkflow` on its own queue) | P6, P10 | — | WORM ledger seal | — |
| P4 Access | ACE Common | — | — | — | — | — |
| S8 Deviation | P1 | Child on P10 | P3, P1 | — | — | — |
| S1 Valuation | P1 | Activity on P7 and P10 | P7 | — | — | — |
| S2 Treatment | — | Activity on P7, P5, P8; Nexus to ACE Common | P7, S8, P8 | — | — | — |
| S3 Guarantee | — | Activity on P7 | P6, P8 | — | — | — |
| S4 Litigation | — | Activity on P7, P6, S9 | P6 | — | — | — |
| S5 Asset | — | Activity on P7, P8, S9 | S4 | — | — | — |
| S6 Debt sale | — | Activity on P7, P5, P8, P2 | — | — | — | — |
| S7 Write-off | P1 | Activity on P7, P8 | P1, P8 | — | — | — |
| P5 Document | — | Child on P10 | P3, P10 | — | Blob WORM | — |
| P6 Comms | ACE Common | Activity on P7, P5, P2 | P3, S8, S2, P8 | — | — | — |
| P8 Payment | — | Activity on P2, P1 | P7, S2, S5, S6, S7 | — | — | — |
| S9 Partner | P5 | — | — | — | — | Partner gateway |
| P2 Integration | P5 | — | — | — | MFT/SFTP | WIN, debt buyers |
| P1 Source data | — | — | — | `recovery.v_ace_*` | — | — |
| P9 Reporting | — | Activity on P2, P1 | P3, S2, S3, S6, S7, P6 | — | — | — |
| P10 Agent | P5, P1 | — | P3 | — | — | Enterprise AI endpoint |

Every service also: sends audit and PII logs to ACE Common over Kafka, publishes `DecisionRecorded`
to `rwb.decision-record.v1`, caches permission data from P4, and emits OpenTelemetry traces.
Route services reach shared capabilities through Temporal, never REST; only `rwb-source-data` reads
ACE's tables.

## 7. Event catalogue (30 entries, Arch v5 slides 42–43)

CloudEvents 1.0 on Kafka, key `caseId`, IDs and facts only; outbox in the producer, inbox in each
consumer. "Owner" is the Ownership Map owner code.

| # | Event | Producer | Topic | Consumers | Owner |
|---|---|---|---|---|---|
| EV-01 | CaseCreated | `rwb-case` | `rwb.case.events.v1` | `rwb-agent`, `rwb-deviation`, `rwb-reporting` | P3 |
| EV-02 | CaseAllocated | `rwb-case` | `rwb.case.events.v1` | `rwb-reporting` | P3 |
| EV-03 | CaseAllocationFailed | `rwb-case` | `rwb.case.events.v1` | `rwb-case` | P3 |
| EV-04 | CaseTransferred | `rwb-case` | `rwb.case.events.v1` | `rwb-reporting` | P3 |
| EV-05 | CaseStateChanged | `rwb-case` | `rwb.case.events.v1` | `rwb-comms`, `rwb-reporting` | P3 |
| EV-06 | DeviationRaised | `rwb-deviation` | `rwb.deviation.events.v1` | `rwb-case`, `rwb-comms`, `rwb-treatment` | S8 |
| EV-07 | DeviationCleared | `rwb-deviation` | `rwb.deviation.events.v1` | `rwb-case`, `rwb-comms` | S8 |
| EV-08 | DecisionRecorded | all 19 services | `rwb.decision-record.v1` | `rwb-decision`, `rwb-reporting` | P7 |
| EV-09 | ApprovalRequested | `rwb-decision` | `rwb.decision.events.v1` | gateway-bff (inbox) | P7 |
| EV-10 | TreatmentApproved | `rwb-treatment` | `rwb.treatment.events.v1` | `rwb-comms`, `rwb-payment` | S2 |
| EV-11 | TreatmentBooked | `rwb-payment` | `rwb.payment.events.v1` | `rwb-case`, `rwb-treatment` | P8 |
| EV-12 | PaymentMissed | `rwb-payment` | `rwb.payment.events.v1` | `rwb-case`, `rwb-treatment`, `rwb-comms` | P8 |
| EV-13 | NoticeGenerated | `rwb-comms` | `rwb.comms.events.v1` | `rwb-decision` | P6 |
| EV-14 | NoticeDispatched | `rwb-comms` | `rwb.comms.events.v1` | `rwb-reporting` | P6 |
| EV-15 | NoticeDelivered | `rwb-comms` | `rwb.comms.events.v1` | `rwb-litigation`, `rwb-guarantee`, `rwb-case` | P6 |
| EV-16 | DocumentStored | `rwb-document` | `rwb.document.events.v1` | `rwb-agent`, `rwb-case` | P5 |
| EV-17 | DocumentFieldsExtracted | `rwb-document` | `rwb.document.events.v1` | `rwb-case` | P5 |
| EV-18 | TimerDue | durable timer | — | none | PLT (retired) |
| EV-19 | TimerBreached | `rwb-case` | `rwb.case.events.v1` | gateway-bff (inbox) | P3 |
| EV-20 | InstructionIssued | `rwb-partner` | `rwb.partner.events.v1` | partner portal | S9 |
| EV-21 | PartnerResultSubmitted | `rwb-partner` | `rwb.partner.events.v1` | `rwb-litigation`, `rwb-asset`, `rwb-case` | S9 |
| EV-22 | AssetTakenOn | `rwb-asset` | `rwb.asset.events.v1` | `rwb-case`, `rwb-payment` | S5 |
| EV-23 | LotAwarded | `rwb-debtsale` | `rwb.debtsale.events.v1` | `rwb-case`, `rwb-payment` | S6 |
| EV-24 | WriteOffApproved | `rwb-writeoff` | `rwb.writeoff.events.v1` | `rwb-case`, `rwb-payment`, `rwb-reporting` | S7 |
| EV-25 | ProceedsMatched | `rwb-payment` | `rwb.payment.events.v1` | `rwb-case`, `rwb-asset`, `rwb-debtsale`, `rwb-writeoff`, `rwb-guarantee` | P8 |
| EV-26 | AceDataReady | `rwb-source-data` | `rwb.source-data.events.v1` | `rwb-case`, `rwb-payment`, `rwb-deviation`, `rwb-writeoff` | P1 |
| EV-27 | AceDataLate | `rwb-source-data` | `rwb.source-data.events.v1` | alerts, gateway-bff banner | P1 |
| EV-28 | AgentRunCompleted | `rwb-agent` | `rwb.agent.events.v1` | `rwb-decision`, `rwb-document`, `rwb-deviation` | P10 |
| EV-29 | CaseEvent (signal) | case router | — | CaseWorkflow (Temporal signal) | P3 |
| EV-30 | RulePackageInForce | `rwb-decision` | `rwb.decision.events.v1` | `rwb-case`, `rwb-valuation`, `rwb-treatment`, `rwb-payment` | P7 |

Further event types named in the contract slides (no separate EV number): `RouteDecided`
(`rwb.valuation.events.v1`, consumers `rwb-case`, owner S1); `AssetSold`
(`rwb.asset.events.v1`, consumers `rwb-payment`, `rwb-case`, owner S5); `JudgmentRecorded`,
`AuctionResult` (`rwb.litigation.events.v1`, consumers `rwb-asset`, `rwb-case`, owner S4);
`TreatmentClosed`, `GuaranteeClaimFiled`, `GuaranteeClaimSettled` (owners S2 and S3);
`AccountsTransferred` (`rwb.debtsale.events.v1`, consumers `rwb-case`, `rwb-reporting`, owner S6);
`AccessPolicyChanged`, `DoaLimitChanged` (`rwb.access.events.v1`, all services for cache refresh,
owner P4); `FileDelivered`, `FileFailed` (`rwb.integration.events.v1`, the requesting service,
owner P2).

**Kafka settings:** topic per service `rwb.<name>.events.v1`; 12 partitions; replication factor 3;
7-day retention; key `caseId`; CloudEvents binary mode; outbox and inbox; retry 1 min, 10 min, 1 h,
then `.dlt`; Event Hubs Premium is the fallback.

## 8. Jobs, schedules and the overnight chain

| Job | Name | When | Owner | Mechanism |
|---|---|---|---|---|
| JOB-01 | ACE ingestion read path | retired | P1 | none (retired under D-RCV-35; read through the views) |
| JOB-02 | Case creation | Airflow: ACE data ready | P3 | `AceDataReady` → `DailyCaseRun` |
| JOB-03 | Morning allocation | after 02:00, by 07:00 | P3 | `DailyCaseRun` step |
| JOB-04 | Reconciliation | Airflow: ACE data ready | P1 | event-started workflow |
| JOB-05 | Timer check | every 5 min | PLT | durable timers (retired) |
| JOB-06 | Rebalancing | 06:30 | P3 | Temporal Schedule |
| JOB-07 | Payment matching | Airflow: ACE data ready | P8 | event-started workflow |
| JOB-08 | Booking confirmation | Airflow: ACE data ready | P8 | event-started workflow |
| JOB-09 | Source load | retired | P1 | none (retired under D-RCV-35) |
| JOB-10 | WIN notices | 16:00 | P6 (P2 delivers the file) | Airflow file window + workers |
| JOB-11 | Outbox sender | every minute | PLT | outbox relay to Kafka |
| JOB-12 | Document intake | every 15 min | P5 | event + KEDA workers |
| JOB-13 | Decision log ingest | continuous (was 01:00) | P7 | Kafka ingest + daily ledger seal |
| JOB-14 | Hash-chain check | 02:00 | P7 | Temporal Schedule |
| JOB-15 | Reporting extract | 01:30 | P9 | Airflow trigger (no data lake) |
| JOB-16 | Write-off scan | monthly, 3rd working day | S7 | Temporal Schedule |
| JOB-17 | Retention | monthly, 1st Sunday | P5 | Temporal Schedule |
| JOB-18 | Access review list | six-monthly | P4 | Temporal Schedule |
| JOB-19 | Re-appraisal | monthly | S5 | Temporal Schedule |
| JOB-20 | Rule promote | 00:01 | P7 | Temporal Schedule → `RulePackageInForce` |
| JOB-21 | Stuck workflow scan | every 5 min | PLT | visibility query + alert |
| JOB-22 | Smoke workflow | 06:00 | PLT | Temporal Schedule (`PlatformSmokeWorkflow`) |

**The overnight chain (Arch v5 slide 31).** 00:00 ACE ingestion (bank Airflow DAG) → 02:00 rules,
ledger, measures (`rwb-decision`, `rwb-reporting`) → 04:00 create and allocate cases (`rwb-case`);
ACE ready ~04:30 → `AceDataReady`; `AceDataLate` alarm 05:30 → payment matching (`rwb-payment`) →
06:30 rebalance (`rwb-case`) → 07:00 officers working → 16:00 customer letters
(`rwb-comms` → `rwb-integration`).

**Airflow (for discussion, Arch v5 slide 32).** Four uses: the overnight chain; fixed-window file
transfers (WIN 16:00 INT-14, debt-buyer files INT-25); report and regulatory extracts (JOB-15);
one-off bulk work (cutover loads, backfills, data quality, GL reconciliation). Interface:
`POST /v1/business-days/{date}/ready` → 202, idempotent on the date; `GET /v1/business-days/{date}/status`
→ `RUNNING | DONE | LATE`; service APIs only, mTLS with client credentials; Airflow never reads or
writes `rwb_*` schemas. Per-case work, approvals, multi-day timers, sagas and event reactions stay in
Temporal and Kafka.

## 9. Temporal design

### 9.1 Five layers (Arch v5 slides 23–24; Temporal design slides 11–12)

| Layer | Content | Owner |
|---|---|---|
| L5 | Domain workflows: `CaseWorkflow` and the stage children | Each service team |
| L4 | Service activity contracts on queue `rwb-<svc>` (for example `Payment.postProceeds`, `Partner.issueInstruction`, `EvaluateRules`, `RecordAndApply`) and Nexus endpoints | Each service team |
| L3 | Workflow kit (versioned library): Approval (maker-checker, DoA), Notify, Document intake, Agent run + fallback, Human task with SLA, Saga runner, Scheduled job, Partner instruction | Platform team |
| L2 | Namespaces: `ace-collection`, `rwb-recovery` (and the next workbench) with own quotas, certificates and codec keys | Platform team |
| L1 | Temporal cluster: one per environment on ACE AKS, own persistence database, UI, metrics, codec server; version 1.30+ | Platform team |

Rules that keep it reusable: no business terms in L1–L3 interfaces; the kit is versioned and workers
are pinned (Worker Versioning); all I/O in activities; Continue-As-New at stage ends and at least
every 28 days; payloads encrypted by the codec (AES-GCM, keys in Key Vault per namespace).

### 9.2 Workflows (15 in the Ownership Map)

| Workflow | Owner | Queue | Source |
|---|---|---|---|
| `CaseWorkflow` | P3 | `rwb-case` | Arch v5 slide 14; parent, one per case |
| `ApprovalWorkflow` | P7 | `rwb-decision` | Arch v5 slide 14; kit template |
| `RouteDecisionWorkflow` | S1 | `rwb-valuation` | Arch v5 slide 18 |
| `TreatmentWorkflow` | S2 | `rwb-treatment` | Arch v5 slide 18; settlement and DIL sagas |
| `GuaranteeClaimWorkflow` | S3 | `rwb-guarantee` | Arch v5 slide 18 |
| `LitigationWorkflow` | S4 | `rwb-litigation` | Arch v5 slide 19; years, continues-as-new |
| `AssetDisposalWorkflow` | S5 | `rwb-asset` | Arch v5 slide 19 |
| `DebtSaleWorkflow` | S6 | `rwb-debtsale` | Arch v5 slide 19; saga, pivot = transfer |
| `WriteOffWorkflow` | S7 | `rwb-writeoff` | Arch v5 slide 20 |
| `DeviationWorkflow` | S8 | `rwb-deviation` | Arch v5 slide 15; child of the case |
| `InstructionWorkflow` | S9 | `rwb-partner` | Arch v5 slide 17; SLA timers |
| `NoticeDispatchWorkflow` | P6 | `rwb-comms` | Arch v5 slide 17; kit template |
| `DocumentIntakeWorkflow` | P5 | `rwb-document` | Arch v5 slide 16; OCR, classify, extract |
| `AgentRunWorkflow` | P10 | `rwb-agent` | Arch v5 slide 16; 60 s, then the rule result |
| `PlatformSmokeWorkflow` | PLT | platform queue | Arch v5 slide 44 JOB-22 |

### 9.3 The runtime pattern (Temporal design slides 13–14, 27–28)

`CaseWorkflow` (workflow ID = case ID; ADR-011 writes it `case-{caseId}`) runs from entry to closure
on queue `rwb-case`. Each stage is a child workflow on the owner's queue; children use parent close
policy ABANDON so they survive Continue-As-New. Events reach the case through the case router in
`rwb-case` (`signalWithStart`), never by direct calls. Every event follows four steps: receive →
`EvaluateRules` (Drools, inside an activity) → `RecordAndApply` (decision record, state change and
outbox in one transaction) → wait on a durable timer or the next signal.

- Retry: 1 s initial interval, back-off 2, 10 attempts; `NoPackageInForce` is non-retryable.
- History: Continue-As-New at every stage end and at least every 28 days (limit 51,200 events or
  50 MB).
- Search attributes: `CaseId`, `Stage`, `ProductGroup`, `QueueCode` only.
- Retention: 30 days for closed workflows, archived to Blob (E2-039).
- Workers run in each service's worker deployment and poll only their own queue; KEDA scales them
  on backlog, down to zero for bursty work.
- Versioning: Worker Versioning, `Workflow.getVersion`, and the replay gate (E2-040) on every build.
- Failure behaviour: worker down → work waits and resumes from history; call failure → retried;
  no rule version → stops at once with a stuck-case alert; faulty rule version → refused at load,
  current version keeps running; decision-record write fails → nothing moves; AI slow → rule answer
  after 60 s; Kafka down → events wait in the outbox; central ledger late → work carries on except at
  points of no return.

## 10. Rules and the decision log

### 10.1 Rule governance (Arch v5 slides 27–28; Temporal design slides 15–16)

- **Governed centrally in `rwb-decision` (P7):** authoring, test scenarios, four-eyes approval,
  effective dating and version audit.
- **Run in the owning service:** the service loads the model (`GET /rule-models/{n}/{v}`), verifies
  the checksum, swaps it in atomically, keeps the last good model on failure (cache max 20) and
  evaluates inside an activity in under 300 ms.
- **Author:** business writes the decision table; **test:** at least 50 scenarios
  (`rules.testcases.min=50`); **approve:** four-eyes, the author cannot approve; **publish:**
  `RulePackageInForce` (EV-30); **promote:** JOB-20 at 00:01; **rollback:** one call.
- **Stored per version:** workbook (Blob), generated DRL, SHA-256, valid-from date, approver.
  Version states: `LOADED`, `APPROVED`, `IN_FORCE`, `SUPERSEDED`, `ROLLED_BACK`, `REFUSED`.
- **Load checks:** compile, schema, overlap, unreachable row, default row, at least 50 scenarios,
  dry run.
- **First match wins:** RuleSet = package code; one row per rule; rows share one activation group;
  salience from row order; default row last; the rule name is the rule ID written to the record.
- **Format:** XLS decision tables today (ADR-012); the target is OMG DMN 1.6, converted table by
  table on the same Drools runtime (gap `GAP-0006`).

**Rule sets (448 rules in 10 route sets):** RES 37, SET 27, DIL 37, GUA 32, LIT 79, DIS 72, DS 41,
WO 51, DEV 22, UNI 50. Phase 1 packages: ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT, TRANSFER,
RESTRUCTURE, PAYMENT_MATCH, BOOKING_MATCH. UNIVERSAL (R-UNI-01 to 50) arrives in Epic 3. Packages
for S1 and S3–S9 are Phase 2 (gap `GAP-0004`). `rule_row` stays as the parsed, queryable
catalog.

### 10.2 Decision record and ledger

1. The owning service writes the decision record, the state change and the outbox row in one
   transaction; the record is hash-linked to the previous one.
2. It publishes `DecisionRecorded` (EV-08) to `rwb.decision-record.v1`.
3. `rwb-decision` consumes it idempotently into the central ledger within 5 minutes, with gap
   alerts; JOB-14 checks the chain at 02:00.
4. A daily ledger fingerprint is sealed to write-once (WORM) storage.
5. **Strict mode at points of no return:** debt transfer, write-off posting, auction sale and title
   transfer wait for the central ledger to confirm. Everything else carries on.

Record fields: `chain_seq`, `inputsRef`, `ruleId`, `ruleVersion`, `recommendation`,
`approverUserId`, `approvalLevel`, `finalCall`, `actions`, `outcome`, `decidedAt`, `prev_hash`,
`entry_hash`. This model changes ADR-009 and needs Risk and Internal Audit sign-off
(gap `GAP-0003`).

Delegation of authority is versioned reference data (`delegation_limit`) owned by P4, approved and
dated like a rule package; every answer records the version used.

## 11. Data

| Item | Value | Evidence |
|---|---|---|
| Server | ACE PostgreSQL (Azure Database for PostgreSQL), PgBouncer | Arch v5 slide 29 |
| Recovery schemas | 19, one login each: `rwb_case` … `rwb_agent` | Arch v5 slide 29 |
| ACE schema | `recovery` holds the 30 read-only `v_ace_*` views (ADR-010) | Arch v5 slides 7, 29 |
| Read rule | Only `rwb_source_data` has SELECT on the views | Arch v5 slides 11, 29 |
| No cross-schema | No joins, views or foreign keys across schemas; IDs only; ask the owner through its contract | Arch v5 slide 29 |
| Migrations | Flyway per service, in its own pipeline and schema | Arch v5 slide 29 |
| Boundary test | A build failure on any cross-schema reference | Arch v5 slide 29 |
| Connection budget | One PgBouncer pool per login with a cap and a statement timeout (5 s) | Arch v5 slides 11, 29 |
| Temporal | Its own persistence database, no grant on the ACE database | Arch v5 slides 8, 23 |
| Documents | Azure Blob with WORM, `rwb-document` only; 2.8 TB by 2031 | Arch v5 slides 16, 29 |
| Movability | Any schema can move to its own server by changing the connection string | Arch v5 slide 29 |
| Tables | 93 in the Ownership Map, distributed as in §5.2 | Ownership Map |

Carried forward from the v2 baseline and still true in v5: four 1:1 extension tables keyed by ACE
business keys (`party_ext`, `contact_point_ext`, `account_ext`, `valuation_ext`, all P1); the
Workbench loads no source data (D-RCV-35 U1); ACE's own tables are never altered.

## 12. Edge, security, AI and compliance

### 12.1 Edge (Arch v5 slides 7–8, 20)

Staff reach the shared Azure App Gateway with WAF: `/` and `/api/*` go to ACE, `/recovery/*` and
`/api/recovery/*` go to the Recovery `gateway-bff` (Spring Cloud Gateway, session in Redis, opaque
session cookie, 15-minute idle timeout, sign-in through ACE Common with Entra ID and MFA). The BFF
makes one hop per owner service, in parallel for composite screens, with a 2 s timeout and a circuit
breaker per service; it never calls a service that then calls another. Partners use the separate
partner gateway (FAPI 2.0) in the DMZ that fronts `rwb-partner` (`/partner/v1/*`).

### 12.2 Security layers (Arch v5 slide 35)

| Layer | Control |
|---|---|
| Edge | Shared App Gateway with WAF; partners only through the partner gateway (FAPI 2.0) |
| Sign-in | ACE Common sign-in (Entra ID, MFA) at the shared gateway-bff; 15-minute idle timeout |
| Service to service | Every call encrypted and identified both ways (mTLS); Kafka ACLs per service |
| Inside each service | Role, scope and DoA checked on every action from P4 data (OWASP API1 object-level authorisation) |
| Data | One login per schema; personal data masked and encrypted; never in events or workflow payloads |
| Audit and monitoring | Hash-chained decision log; ACE PII logging to SOC; one trace across services |

Standards applied: NIST SP 800-204/204A/204B/204C/204D, OWASP API Top 10 (2023), FAPI 2.0,
OpenAPI 3.1, AsyncAPI 3, CloudEvents 1.0, OMG DMN 1.6, OpenTelemetry and W3C Trace Context,
BIAN v14, microservices.io patterns, Azure Well-Architected, Temporal durable execution.

### 12.3 AI controls (Arch v5 slides 35, 50)

AI suggests, never decides; a person approves. Model and prompt versions are recorded; personal data
is masked before it leaves; 60-second limit then the rules decide (R-UNI-32); AI runs only in
`rwb-agent` and is easy to switch off. This follows the BOT AI Risk Management Guidelines of
12 September 2025 (date from a secondary source; gap `GAP-0020`).

### 12.4 ACE Common connections (Arch v5 slide 30, INT-34)

| # | Caller | Contract | Call type |
|---|---|---|---|
| 1 | gateway-bff, `rwb-access` | Sign-in, user JWT, group-to-role (Entra ID) | REST / OIDC |
| 2 | All 19 services | Audit and PII access logs to SOC | Kafka (PII path) |
| 3 | `rwb-case` | Shared case view: `GET /case-summary/{id}` | REST |
| 4 | `rwb-treatment` | Restructure calculator `restructure.calculate` (REST fallback) | Nexus |
| 5 | `rwb-comms` | SMS and LINE message, delivery status (NSS, LINE OA) | REST |
| 6 | `rwb-source-data` | 30 `recovery.v_ace_*` views, read-only | SQL views |

External interfaces: WIN registered mail file (INT-14), debt-buyer encrypted files (INT-25),
Enterprise AI private endpoint (INT-23). Removed: INT-19 and INT-20 (data lake, Power BI).

### 12.5 Compliance (Arch v5 slide 50)

| Regulation | What it asks | How the design responds |
|---|---|---|
| BOT FPG 19/2560 (IT risk management) | Board-approved plan and prior BOT approval before first use of a technology or a change that may pose significant risk (cl. 5.5); report significant incidents | Treat the move to microservices as a significant change; submit before Wave 1; incident reporting through SIEM and runbooks |
| BOT FPG 19/2559 (IT outsourcing) | Board-approved outsourcing policy; notify or seek approval before use | All services stay on the bank's Azure tenant and AKS; any new managed service is checked against the outsourcing register |
| BOT Cyber Resilience Assessment Framework | Governance, identify, protect, detect, respond, recover, third-party risk | Zero trust, mesh mTLS, WAF, SIEM, tested recovery tiers |
| BOT AI Risk Management Guidelines (12 Sep 2025) | Board accountability, lifecycle risk, accuracy and explainability, customer disclosure, human option | AI isolated in `rwb-agent`; autonomy levels; human decision on material actions; prompts, outputs and model versions logged |
| Thailand PDPA | Lawful purpose, minimisation, security, retention, data-subject rights | Personal data only in the owning service; IDs in events and workflows; Temporal payload encryption; retention jobs |

Programme dependency: under FPG 19/2560 cl. 5.5 the change may need a board-approved plan and BOT
approval before Wave 1 (up to 30 business days); the route is still open (gap `GAP-0010`).

## 13. Delivery model

### 13.1 Epics (31) and waves

| Group | Epics |
|---|---|
| Platform (7) | `RWB-PLT-TPL`, `RWB-PLT-LIB`, `RWB-PLT-WF`, `RWB-PLT-DB`, `RWB-PLT-EVT`, `RWB-PLT-EDGE`, `RWB-PLT-OBS` |
| Service (19) | `RWB-SVC-P1` … `RWB-SVC-S9` |
| Integration (5) | `RWB-ITG-W1` … `RWB-ITG-W4`, `RWB-ITG-NFR` |

Every story also carries its business epic `EP01`–`EP08` as a tag. One epic per service; the owner
is a suggestion only ("any team may pick up this story"); no names of people anywhere.

| Wave | Content |
|---|---|
| 0 · platform once | Service template + Helm, contract libraries, workflow kit (L3), 19 schemas + logins, Kafka topics + ACLs, Temporal 1.30+ |
| 1 · Epic 1 (9 services) | P1, P2, P3, P4, P5, P6, P7, P9, P10 |
| 2 · Epics 2–3 (+4) | P8, S2, S5, S8 |
| 3 · Epics 4–5 (+4) | S1, S3, S4, S6 |
| 4 · Epics 6–7 (+2) | S7, S9 |

Business-epic wave map (W-MAP): EP01 = 1; EP02, EP03 = 2; EP04, EP05 = 3; EP06, EP07, EP08 = 4;
platform and NF = 0. A story whose W-MAP wave is earlier than its service's Arch v5 wave keeps the
W-MAP wave, and one conflict gap is raised per service and business epic.

Release dates are carried unchanged and marked **(tentative)** (`ASM-5680`): Release 1 (Epic 1
Foundation 1) 30 November 2026 (tentative); Release 2 (Epic 2 Foundation 2) 31 December 2026
(tentative); Epic 3–8 monthly releases to June 2027 (tentative). Arch v5 does not map its waves to
these dates (gap `GAP-0001`).

### 13.2 Work types and suggested owners

| Work type | Name | Suggested owner (fixed phrase) |
|---|---|---|
| CON | Contract | TechX (suggested; any team may pick up this story) |
| APP | App development | TechX (suggested; any team may pick up this story) |
| DB | ACE DB | ACE team (suggested; any team may pick up this story) |
| INF | Infrastructure | SCB IT infrastructure (suggested; any team may pick up this story) |
| OPS | DevOps | DevOps team (suggested; any team may pick up this story) |
| ITG | Integration | TechX (suggested; any team may pick up this story); harness and NFR stories: QA team (suggested; any team may pick up this story) |

**Dependency classes.** H = same service or a platform CON story (the only class that blocks a
non-CON story, and only in the same lane); C = another service's CON story (build against the
published contract and its fake; never blocks); I = real cross-service behaviour (ITG stories only);
X = external or team-type work (tracked, does not block).

**Story IDs.** `RWB-<scope>-<legacy compact>-<work type>[-n]`; scope P1–P10, S1–S9, PLT or ITG;
legacy compact E1018, TE001, AD003, DM002, ACE001, NF06, N001 (new) or W1J01 (new integration); `-2`
is the delta copy of a preserved story that keeps its base ID. Example: `RWB-P3-E1018-APP`.

**Lane and Day-1 rules.** A CON story is always Day 1 in contract group `CG-W<wave>`; APP stories
build against CON and fakes; H dependencies point only to the same service or a platform CON; I
dependencies only on ITG stories; a lane is a connected group of non-CON stories linked by H, depth
at most 4 (a deeper chain is cut and an assumption recorded); every team type has Day-1 work (N001–
N012 and W1J01); every service has at least one CON story; ready to start is "Day 1" or
"After <the in-lane story IDs it waits for>".

### 13.3 Decoupling patterns (DP-01 to DP-20)

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H `RWB-PLT-E1027-CON` |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from `rwb-decision` | H `RWB-PLT-E1072-CON`; C `RWB-P7-E1073-CON` |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through `rwb-source-data`'s contract or the service's own ACE views | none |
| DP-06 | Parameters, `casewf.config` | Parameters contract of `rwb-case` and the client library | H `RWB-PLT-E1042-CON`; C `RWB-P3-E1042-CON` |
| DP-07 | Reference data, LOV | Reference-data contract of `rwb-case` | H `RWB-PLT-E1043-CON`; C `RWB-P3-E1043-CON` |
| DP-08 | RecoveryAccessGuard | Authorise contract of `rwb-access` and the guard library | H `RWB-PLT-E1037-CON`; C `RWB-P4-E1037-CON` |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H `RWB-PLT-TE006-CON` |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H `RWB-PLT-E1071-CON` |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-12 | One workflow per case | `CaseWorkflow` parent with a child workflow per stage | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H `RWB-PLT-E1047-CON` |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H `RWB-PLT-E1044-CON` |
| DP-16 | `recovery.integration.adapter` | `rwb-integration` contract | C `RWB-P2-E1007-CON` |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into `rwb-reporting` | none; gap if the story needs lake data |
| DP-18 | Interaction ledger | Ledger owned by `rwb-source-data` (default ruling) | none |
| DP-19 | Screen, `ace-web` | gateway-bff composite route | H `RWB-PLT-N001-CON` |
| DP-20 | Agent client | `rwb-agent` contract | C `RWB-P10-TE013-CON` |

### 13.4 New architecture decisions

| ADR | Decision |
|---|---|
| ADR-013 | 19 services inside ACE — supersedes the single-service decision ADR-002 |
| ADR-014 | Schema and login per service in ACE PostgreSQL |
| ADR-015 | Kafka with outbox, inbox and CloudEvents |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz |
| ADR-017 | Embedded Drools per service; rule registry in `rwb-decision` — amends D-RCV-36 T1 and T2 |
| ADR-018 | No data lake; `rwb-reporting` read model from events |
| ADR-019 | Edge: gateway-bff and partner gateway |
| ADR-020 | Contract-first REST, one hop, 2 s timeout |
| ADR-021 | Per-service Flyway and migration ownership |
| ADR-022 | Local decision record plus central ledger |
| ADR-023 | Observability per service |

Note: Template and Rules §R8.4 describes ADR-013 as superseding the single-service decision ADR-002,
while Arch v5 slide 37 records ADR-001 as the one-deployable decision and ADR-002 as the one-schema
decision. Both numbers are kept as written in their sources.

Decision Log: `D-RCV-60` (adopt Arch v5 and realign the documents and stories), plus `DL44` adopt
Arch v5, `DL45` service epics plus business-epic tags, `DL46` soft ownership by team type, `DL47`
Epic 1 preservation, `DL48` dates unchanged and tentative, `DL49` gap and assumption registers.

### 13.5 Epic 1 preservation and legacy dispositions

| Group | Stories | Rule |
|---|---|---|
| Built or in build, preserved | `RWB-TE-001`, `TE-002`, `TE-003`, `E1-042`, `E1-043`, `E1-044` | The as-built story keeps its base ID with `preserved=true`; sections 1–11, 14–16, 18 and 19 are copied word for word; sections 12 and 13 sit under "As built (monolith)"; the microservice change is a separate delta story (`-2` copy, or CON/OPS stories); no change to built code until a delta story is picked up |
| Must change | `RWB-E1-001` | The single recovery schema (92 tables, 14 data products, dictionary; R6 gives 92, Physical Schema v6 and the Ownership Map record 93) is in build; the built migration is kept; the split into `rwb_*` schemas is new work (`RWB-PLT-NF06-DB` and the per-service DB stories) |
| Retired | `RWB-E1-014` (decision-log copy to the data lake), `RWB-TE-007` (Quartz scheduler) | No new story; dependencies on E1-014 are dropped; dependencies on TE-007 point to `RWB-PLT-E1071-CON` |
| Already cancelled | `E1-003`, `004`, `005`, `006`, `009`, `010`, `012`, `029`, `048`, `051`; `TE-005` | No new story |
| No impact | `E1-024`, `025`, `026`, `033`, `034`, `038`, `040`, `041`, `045`, `053`, `060`, `061`, `068`; `TE-010`, `TE-012` | Moved to their epic with content unchanged |

Split plan (`split_plan.json`): 358 legacy keys → **1,034 story slices**, **939 Day-1** stories
across the five team types (ACE, DEVOPS, INFRA, QA, TechX), **510 lanes**. Dispositions: 308 Split
(rework), 24 Moved (no impact), 17 New, 6 Preserved + delta, 2 Retired (D-RCV-60), 1 Must change.

### 13.6 Story template obligations

Every story carries the 20-row metadata table in the Template and Rules §R7.1 order and the 19
sections of §R7.2. Each `Scenario: ACn` line ends with an origin tag, either
"(legacy RWB-…-nnn ACn)" or "(new, D-RCV-60)". Section 12 uses tables 12.1–12.9 (REST provided,
REST consumed, events published, events consumed, workflows and activities, schedules, tables owned,
contract fakes, call-type summary), written "None" where empty. Section 16 columns are TC ID,
Covers, Level (Unit, Component, Contract, Integration, End to end, NFR) and Data; ITG copies end in
`-ITG`. Section 17 guardrails: no business values in code, no PII in events, workflow inputs or logs,
ACE data only through the owner's contract or `v_ace_*` views.

### 13.7 Open architecture decisions and risks

Six decisions the architecture team still owes (Arch v5 slide 39); the first three are needed before
Wave 0 starts:

| # | Decision | Owner |
|---|---|---|
| 1 | Kafka for business events: dedicated Recovery topics on the bank Kafka platform, fallback the Azure Event Hubs Kafka endpoint | Enterprise Architecture, ACE platform team |
| 2 | A schema per service in the ACE database: 19 schemas and 19 logins, a connection budget per service, no cross-schema access | ACE team, DBA |
| 3 | Shared Temporal layer: the platform team owns the cluster and the workflow kit, upgrade to 1.30+, namespaces per workbench | Platform team, ACE team |
| 4 | ACE Common contracts: sign-in, notification path, shared case view adapter, restructure calculator Nexus, audit and PII logging | ACE team |
| 5 | Decision ledger model: local record plus central ledger in `rwb-decision`, strict mode for irreversible steps, changes ADR-009 | Risk, Internal Audit |
| 6 | BOT approval route: is this a significant change under FPG 19/2560 cl. 5.5? Lead time up to 30 business days | Compliance, IT risk |

Eight risks and their mitigations (Arch v5 slide 47):

| Risk | Impact | Mitigation | Owner |
|---|---|---|---|
| Too many deployables for the team | Slow delivery, on-call load | Waves by epic; service template, one Helm chart, golden pipeline; platform team runs Kafka and Temporal | Delivery lead |
| ACE database capacity | Slow ACE screens or jobs | Connection pools and caps per login; heavy reports from projections; monitor per schema; move a schema out if needed | ACE DBA |
| Schema rules broken over time | Hidden coupling between services | Grants per schema; boundary test in every build; review of every new grant | Architecture |
| Kafka platform not ready | Events stay in outboxes | Outbox port; Event Hubs Kafka endpoint as fallback | Enterprise Architecture |
| Temporal upgrade from 1.28.1 | No Nexus, no Worker Versioning | Upgrade to 1.30+ in Wave 0 | Platform team |
| Ledger model not accepted by Audit | Back to a synchronous central log | Strict mode for irreversible steps; early walkthrough with Audit | Architecture, Audit |
| BOT approval lead time | Wave 1 date slips | Confirm the route early; plan up to 30 business days | Compliance |
| ACE Common contracts change | Recovery features break | Versioned contracts and contract tests with the ACE team | ACE team |

## 14. Conflicts, gaps and assumptions

Each row has a candidate gap `CG-A10-CTX-n` and a candidate assumption `ASM-A10-CTX-n` in
`_work/msr/gaps/A10-CTX.jsonl` and `_work/msr/assumptions/A10-CTX.jsonl`; step D1 numbers them
`GAP-nnnn` and `ASM-nnnn`. Arch v5 is treated as the target in this run (`ASM-0033`).

| ID | Item | Type | Resolution used here |
|---|---|---|---|
| `GAP-0001` | The Arch v5 waves 0–4 are not mapped to the release dates carried from the v2 baseline | Outdated | Dates copied unchanged and marked (tentative); the wave-to-release mapping is left open (`ASM-0011`) |
| `GAP-0002` | ADR-011 and Workflow Engine Design v3 describe one long `CaseWorkflow`; v5 runs a child workflow per stage | Conflict | The v5 child-per-stage model is recorded; ADR-011 needs an update (`ASM-0012`) |
| `GAP-0003` | ADR-009 writes the central log inside every call; v5 writes the record locally and seals it centrally | Conflict | `RecordAndApply` in one transaction plus the central ledger; Risk and Internal Audit sign-off is still needed (`ASM-0013`) |
| `GAP-0004` | Only RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH exist as Phase 1 packages; S1 and S3–S9 have 448 rules but no package codes | Missing | Rules stay with their route set; the package codes are Phase 2 (`ASM-0014`) |
| `GAP-0005` | Route numbering: R-LIT-01 starts litigation on R4, while Case Journeys v3 calls R4 the guarantee claim and R5 litigation | Conflict | The rule text keeps its numbering; the route name follows Case Journeys v3 (`ASM-0015`) |
| `GAP-0006` | Rule format: XLS decision tables today (ADR-012) vs OMG DMN 1.6 in v5 | Ambiguous | Both run on the same Drools runtime; the conversion is table by table (`ASM-0016`) |
| `GAP-0007` | Temporal version: v5 requires 1.30+, ADR-011 pins 1.28.1, the local stack runs 1.29.7 | Conflict | Wave 0 upgrades to 1.30+ (`ASM-0017`) |
| `GAP-0008` | JOB-16 starts from a Temporal Schedule (slides 23/44), from the ACE batch record (Batch and Scheduling v4) and stays on Quartz under T2 | Conflict | Temporal Schedule in S7 on the 3rd working day (`ASM-0018`) |
| `GAP-0009` | Airflow is "for discussion": DAG ownership, Control-M cutover, hosting and the ADR that replaces the BRD's ADF/Control-M wording are open | Ambiguous | Airflow is recorded as the bank scheduler at Recovery's edges only (`ASM-0019`) |
| `GAP-0010` | BOT approval route under FPG 19/2560 cl. 5.5 is undecided (up to 30 business days) | Missing | Treated as a significant change; the submission date is a programme dependency (`ASM-0020`) |
| `GAP-0011` | Kafka hosting is not confirmed: capacity, topic naming, ACL model, schema registry and environments are to agree; Event Hubs Premium is the fallback | Missing | Kafka on the bank platform with the fallback kept (`ASM-0021`; `ASM-5669` holds the cluster ownership and sizing default until resolved) |
| `GAP-0012` | The 19 schemas and logins and the per-login connection budget are not created or quantified | Missing | Wave 0 creates them; the budget is set by the ACE DBA (`ASM-0022`) |
| `GAP-0013` | The ACE Common contracts (sign-in, PII logging, case-view adapter, calculator Nexus, notification path) are not versioned or scheduled | Missing | Consumed as versioned contracts (INT-34) with contract tests on both sides (`ASM-0023`) |
| `GAP-0014` | The 93-table inventory comes from Physical Schema v6: S1 has no table although slide 18 gives three objects, P8 has one table although slide 17 gives matching, fees, bookings and posting files, and the Ownership Map FK-cut sheet is empty | Missing | The map is used as-is for owners; the missing `rwb_*` tables and the FK cuts are gap work (`ASM-0024`) |
| `GAP-0015` | RPO/RTO are not set in NFR Spec v3; the v2 context assumed 15 minutes and 4 hours | Conflict | RPO/RTO stay unset; no target is claimed (`ASM-0025`) |
| `GAP-0016` | Volumes differ: v2 says ~45,000 cases a year and 180 users; v5 says 23,570 open cases (47,389 by 2031), 3,110 new cases a month and 414 concurrent staff | Conflict | The v5 Volume and Scale Forecast v3 figures are used (`ASM-0026`) |
| `GAP-0017` | Arch v5 has no screen inventory, screen-to-service map or design system; the 53 screens in `frontend-context.md` are not restated in v5 | Missing | Front-end detail stays in `frontend-context.md` v2; the v5 screen map is gap work (`ASM-0027`) |
| `GAP-0018` | JOB-21 and JOB-22 are recorded on a platform task queue `rwb-platform`, which is not one of the 19 service queues named in Arch v5 | Ambiguous | The platform queue is recorded as a shared platform queue (`ASM-0028`) |
| `GAP-0019` | The five canonical context files remain at v2: one service, schema `recovery`, 93 tables, Quartz, ~45,000 cases a year, RPO 15 minutes | Outdated | This file carries the v5 delta; the v2 files need re-basing in a later context run (`ASM-0029`) |
| `GAP-0020` | Regulatory sourcing: the AI guidelines date is from a secondary source, FPG 19/2559 may be superseded, and CRAF has no standalone BOT document | Ambiguous | Recorded as verified 19 November 2026 by the architecture source; Compliance confirms (`ASM-0030`) |
| `GAP-0021` | `testing-standards.md` v2 lacks the v5 test obligations: Kafka contract and event tests, Temporal replay gate E2-040, JOB-22 smoke, 50-scenario rule load checks, the per-build boundary test | Outdated | The v5 test obligations are recorded in §9 and §10; the standards file needs the delta (`ASM-0031`) |
| `GAP-0022` | `TimerDue` (EV-18) has two owners in the map: an API ruling names P3, the flow ruling and the events sheet name PLT | Conflict | PLT, and the event stays retired (`ASM-0032`) |

## 15. Registers and inherited open items

- Candidate gaps and assumptions for this work package: `_work/msr/gaps/A10-CTX.jsonl` (22 rows)
  and `_work/msr/assumptions/A10-CTX.jsonl` (24 rows). Only step D1 numbers them.
- The gap and assumption registers (folder 23) are the single register for the run; this file cites
  candidates only.
- Inherited open items from the v2 package (`context-manifest.json`): GAP-005 Thai messages,
  GAP-006 per-story approver names, GAP-007 ACE Tier 2 ingestion assumption, GAP-008 Temporal
  version and retention. GAP-008 is partly answered by this run (Temporal 1.30+); retention stays
  30 days for closed workflows.

## 16. Source register

| ID | Source | Version | Used for |
|---|---|---|---|
| `SRC-30` | Recovery Workbench Architecture v5 Text Extract v1 | v1, 22 November 2026 | Services, contracts, events, jobs, data, edge, security, compliance, delivery |
| `SRC-31` | Recovery Workbench Temporal and Drools Design Text Extract v1 | v1, 22 November 2026 | Workflow model, rule governance, scenarios S1–S9, open design points |
| `SRC-32` | Recovery Workbench Microservice Story Template and Rules v1 | v1, 22 November 2026 | R-PREC, default rulings, naming, epics, work types, DP table, waves, template, outputs, gaps |
| `SRC-33` | Recovery Workbench Microservice Ownership Map v1 / `ownership.json` | v1, 22 November 2026 | Owner of every service, table, endpoint, event, job, workflow |
| `SRC-34` | `_work/msr/plan/split_plan.json` | run artefact | Story slices, legacy dispositions, Day-1 counts, lanes |
| `SRC-35` | `_work/msr/plan/ids.json` | run artefact | ADR-013–023, DL44–49, D-RCV-60 |
| `SRC-36` | Context package `CONTEXT-20261116` (`project-context.md`, `backend-context.md`, `frontend-context.md`, `testing-standards.md`, `domain-context.md`, standards) | v2, 16 November 2026 | Carried-forward business and technical baseline; flagged where stale |

## 17. Guidance for downstream agents

1. This file is the v5 delta. Read it before any story, then the owning long-form context:
   `project-context.md` for business truth, `backend-context.md` for server detail,
   `frontend-context.md` for UI detail, `testing-standards.md` for test levels.
2. Where this file and a v2 context disagree, this file and the v5 sources win; record the conflict
   in the story's clarification log.
3. Use the Ownership Map for every owner. Do not assign a table, endpoint, event, job or workflow to
   a service the map does not name.
4. One service writes only its own schema; only `rwb-source-data` reads the 30 `recovery.v_ace_*`
   views; no cross-schema joins, views or foreign keys.
5. REST is one hop with a 2 s timeout, `Idempotency-Key` on POST and RFC 9457 errors. Use a Temporal
   activity or child workflow for any step in another service; use Kafka only for facts.
6. Events carry IDs and business facts only; no personal data; key `caseId`; outbox and inbox in the
   same transaction as the state change.
7. Rules are governed in `rwb-decision` and evaluated in the owning service inside an activity; every
   answer records the rule ID and version in the decision record.
8. No business value, threshold, template, queue, role or route in code: use the parameter and
   reference-data contracts of `rwb-case`, the `delegation_limit` table of `rwb-access` and the rule
   packages of `rwb-decision`.
9. Mark every release date "(tentative)" and copy it unchanged; never raise a date as a gap.
10. Record an open item; do not ask the user a question during an automated stage. The only exception
    is a safety, credential or production-data issue, which stops the run.
11. Cite the context ID `CTX-REALIGN-RWB-V5` plus the source ID in the spec, plan and traceability
    matrix.

## 18. Change log and version history

| Version | Date | Change |
|---|---|---|
| 3.0 | 22 November 2026 | New realignment context for Arch v5: 19 services, schema and login per service, Kafka events, the five-layer Temporal design, rules governed in `rwb-decision`, no data lake, ownership from the Ownership Map, 22 candidate gaps and 24 candidate assumptions |

3.0, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash

| Version | Date | Breaking for an approved spec or plan? |
|---|---|---|
| 3.0 | 22 November 2026 | Yes: the single-service constraint (ADR-001/ADR-002), schema `recovery`, the 93-table single schema, Quartz scheduling and the v2 volume and NFR figures are replaced for the v5 baseline. Approved specs and plans built on v2 must be re-validated (gap `GAP-0019`). |
