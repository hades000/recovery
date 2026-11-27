SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench Service Catalog v2

| Item | Value |
|---|---|
| Document | Recovery Workbench Service Catalog |
| Version | 2 |
| Date | 27 November 2026 |
| Decision | D-RCV-60 microservice realignment |
| Tool | T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Status | Draft |
| Owner role | Solution architect |
| Services in scope | 19: P1 to P10 and S1 to S9, plus the shared platform (PLT) |
| Source of record | Recovery Workbench Architecture v5 Text Extract v1 (slides 13 to 20 and 41 to 44); Recovery Workbench Microservice Ownership Map v3; Recovery Workbench Temporal and Drools Design Text Extract v1 |
| Change log | below |

| Version | Date | Change | Detail |
|---|---|---|---|
| 1 | 22 November 2026 | D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash | First Service Catalog. The 19 services, the resources each one owns, the provider and consumer contracts, the waves and the conformance rules are taken from Architecture v5 and the Ownership Map v1. No earlier version of this family exists (GAP-0140; ASM-0218). |
| 2 | 27 November 2026 | D-RCV-60 P1 developer readiness (RD-P1 register) | Targeted P1 ownership and dependency updates; case-list artifacts removed from P1, data_product_source added, account-page path remains GAP-3274. |

# 1. Purpose and scope

This catalogue is the single list of the 19 Recovery services. For each service it states the code, the name, the wave, the service epic, the schema and login, the REST base, the Kafka topic with its retry and dead-letter topics, the Temporal task queue, the Java package, the resources the service owns, and what it provides to and consumes from the other services.

It is the reference for four groups of readers:

- architects, who check that a call crosses exactly one boundary and in the right call type;
- the service teams, who build one service from the template in the Service Template Specification v1;
- ACE DB, who creates one schema, one login and one connection pool per service;
- the platform team, who creates the topics, the queues, the Helm releases and the dashboards.

What this catalogue does not contain: the request and response schemas (API Specification v5), the event payloads (Kafka Topic and Event Catalog v1), the workflow steps (Temporal Workflow and Activity Catalog v1), the table columns (Logical Data Model and Physical Schema) and the story-level build order (Build Sequence).

# 2. How this catalogue is built

## 2.1 Precedence

Where two sources disagree, the higher one wins and the loser is recorded as a gap and an assumption (Template and Rules §R3). The order used here is:

1. the Arch v5 catalogue slides 13 to 20 and 41 to 44, for services, resources, call types and jobs;
2. the Recovery Temporal and Drools Design v1, for the workflow split and the rules placement;
3. the Arch v5 narrative slides, for the standards that every service follows;
4. the Recovery Workbench Microservice Ownership Map v3, for the owner of every table, endpoint, event and workflow;
5. the current architecture documents (Decision Log, ADRs, TSDs, FSDs, LDM), which the realignment rewrites.

The Ownership Map is used for every owner in this catalogue. Its Services sheet is the source of the code, the service name, the wave, the schema, the REST base, the topic and the task queue; its Tables, Endpoints, Events, Workflows and activities and Jobs sheets are the source of the ownership of every resource named below.

## 2.2 What changed in this version

- The single recovery service and the single recovery schema of the earlier documents become 19 services with 19 schemas, 19 logins, 19 topics and 19 task queues (Arch v5 slide 41; ADR-013 and ADR-014).
- Every service is named and packaged by the rules in Template and Rules §R4, and is listed with the same field set so that the API, event, workflow, data and story documents can point at one row.
- The resources are the tables of the Ownership Map v3. The current recovery schema is split across the 19 schemas; the outbox, inbox and idempotency tables are library tables created in every service schema.
- No service and no call type is added or removed against Architecture v5. Two resource lists that Arch v5 names but the Ownership Map does not yet hold are recorded as gaps (GAP-0132 and GAP-0133).

# 3. The 19 services at a glance

Order is the Ownership Map order: platform services P1 to P10, then the route services S1 to S9.

| Code | Service | Name | Wave | Service epic | Schema and login | REST base | Kafka topic | Task queue | Java package |
|---|---|---|---|---|---|---|---|---|---|
| P1 | rwb-source-data | Source data | 1 | RWB-SVC-P1 | rwb_source_data | /api/recovery/source-data/v1 | rwb.source-data.events.v1 | rwb-source-data | th.co.scb.ace.workbench.recovery.sourcedata |
| P2 | rwb-integration | Integration | 1 | RWB-SVC-P2 | rwb_integration | /api/recovery/integration/v1 | rwb.integration.events.v1 | rwb-integration | th.co.scb.ace.workbench.recovery.integration |
| P3 | rwb-case | Case and workflow | 1 | RWB-SVC-P3 | rwb_case | /api/recovery/case/v1 | rwb.case.events.v1 | rwb-case | th.co.scb.ace.workbench.recovery.case |
| P4 | rwb-access | Access and authority | 1 | RWB-SVC-P4 | rwb_access | /api/recovery/access/v1 | rwb.access.events.v1 | rwb-access | th.co.scb.ace.workbench.recovery.access |
| P5 | rwb-document | Document | 1 | RWB-SVC-P5 | rwb_document | /api/recovery/document/v1 | rwb.document.events.v1 | rwb-document | th.co.scb.ace.workbench.recovery.document |
| P6 | rwb-comms | Communications | 1 | RWB-SVC-P6 | rwb_comms | /api/recovery/comms/v1 | rwb.comms.events.v1 | rwb-comms | th.co.scb.ace.workbench.recovery.comms |
| P7 | rwb-decision | Decision and rules | 1 | RWB-SVC-P7 | rwb_decision | /api/recovery/decision/v1 | rwb.decision.events.v1 | rwb-decision | th.co.scb.ace.workbench.recovery.decision |
| P8 | rwb-payment | Payment | 2 | RWB-SVC-P8 | rwb_payment | /api/recovery/payment/v1 | rwb.payment.events.v1 | rwb-payment | th.co.scb.ace.workbench.recovery.payment |
| P9 | rwb-reporting | Reporting | 1 | RWB-SVC-P9 | rwb_reporting | /api/recovery/reporting/v1 | rwb.reporting.events.v1 | rwb-reporting | th.co.scb.ace.workbench.recovery.reporting |
| P10 | rwb-agent | Agent | 1 | RWB-SVC-P10 | rwb_agent | /api/recovery/agent/v1 | rwb.agent.events.v1 | rwb-agent | th.co.scb.ace.workbench.recovery.agent |
| S1 | rwb-valuation | Valuation and route | 3 | RWB-SVC-S1 | rwb_valuation | /api/recovery/valuation/v1 | rwb.valuation.events.v1 | rwb-valuation | th.co.scb.ace.workbench.recovery.valuation |
| S2 | rwb-treatment | Treatment and offer | 2 | RWB-SVC-S2 | rwb_treatment | /api/recovery/treatment/v1 | rwb.treatment.events.v1 | rwb-treatment | th.co.scb.ace.workbench.recovery.treatment |
| S3 | rwb-guarantee | Guarantee | 3 | RWB-SVC-S3 | rwb_guarantee | /api/recovery/guarantee/v1 | rwb.guarantee.events.v1 | rwb-guarantee | th.co.scb.ace.workbench.recovery.guarantee |
| S4 | rwb-litigation | Litigation | 3 | RWB-SVC-S4 | rwb_litigation | /api/recovery/litigation/v1 | rwb.litigation.events.v1 | rwb-litigation | th.co.scb.ace.workbench.recovery.litigation |
| S5 | rwb-asset | Asset | 2 | RWB-SVC-S5 | rwb_asset | /api/recovery/asset/v1 | rwb.asset.events.v1 | rwb-asset | th.co.scb.ace.workbench.recovery.asset |
| S6 | rwb-debtsale | Debt sale | 3 | RWB-SVC-S6 | rwb_debtsale | /api/recovery/debtsale/v1 | rwb.debtsale.events.v1 | rwb-debtsale | th.co.scb.ace.workbench.recovery.debtsale |
| S7 | rwb-writeoff | Write-off | 4 | RWB-SVC-S7 | rwb_writeoff | /api/recovery/writeoff/v1 | rwb.writeoff.events.v1 | rwb-writeoff | th.co.scb.ace.workbench.recovery.writeoff |
| S8 | rwb-deviation | Deviation | 2 | RWB-SVC-S8 | rwb_deviation | /api/recovery/deviation/v1 | rwb.deviation.events.v1 | rwb-deviation | th.co.scb.ace.workbench.recovery.deviation |
| S9 | rwb-partner | Partner | 4 | RWB-SVC-S9 | rwb_partner | /api/recovery/partner/v1 | rwb.partner.events.v1 | rwb-partner | th.co.scb.ace.workbench.recovery.partner |

| Item | Value |
|---|---|
| Services | 19 |
| Platform services (P1 to P10) | 10 |
| Route services (S1 to S9) | 9 |
| Services in wave 1 | 9: P1, P2, P3, P4, P5, P6, P7, P9, P10 |
| Services in wave 2 | 4: P8, S2, S5, S8 |
| Services in wave 3 | 4: S1, S3, S4, S6 |
| Services in wave 4 | 2: S7, S9 |
| Shared topic | rwb.decision-record.v1 (producer: all 19; central ledger: rwb-decision) |
| Temporal namespace | rwb-recovery |
| Platform task queue | rwb-platform (platform jobs JOB-21 and JOB-22) |
| Shared platform tables per service | 6: feature_flag, feature_flag_change, idempotency_key, outbox_event, outbox_delivery, processed_event |

# 4. Waves and service epics

A service is created when its first epic starts, so nothing is built twice (Arch v5 slide 38). Wave 0 builds the template once: the service template with the outbox, the inbox, the Temporal worker, the codec and OpenTelemetry, one Helm chart, the golden pipeline, the contract libraries, the workflow kit, the 19 schemas and logins, the Kafka topics and ACLs, and Temporal 1.30 or later.

| Wave | Services | Service epics | Built in the wave | Gate |
|---|---|---|---|---|
| 0 | None (platform only) | RWB-PLT-TPL, RWB-PLT-LIB, RWB-PLT-WF, RWB-PLT-DB, RWB-PLT-EVT, RWB-PLT-EDGE, RWB-PLT-OBS | Service template, Helm chart, golden pipeline, contract libraries, workflow kit, 19 schemas and logins, topics and ACLs | Template accepted; 19 logins created; topics exist |
| 1 | P1, P2, P3, P4, P5, P6, P7, P9, P10 | RWB-SVC-P1 to RWB-SVC-P7, RWB-SVC-P9, RWB-SVC-P10 | 9 services, each an API deployment and a worker deployment | BOT approval before Wave 1 go-live, if required (FPG 19/2560 cl. 5.5; up to 30 business days) |
| 2 | P8, S2, S5, S8 | RWB-SVC-P8, RWB-SVC-S2, RWB-SVC-S5, RWB-SVC-S8 | 4 services | Wave 1 in production |
| 3 | S1, S3, S4, S6 | RWB-SVC-S1, RWB-SVC-S3, RWB-SVC-S4, RWB-SVC-S6 | 4 services | Wave 2 in production |
| 4 | S7, S9 | RWB-SVC-S7, RWB-SVC-S9 | 2 services | Wave 3 in production |

No service in this catalogue carries a release date. Release dates are held in the Release Plan and are tentative (Decision U7 and DL48).

# 5. Naming, packaging and identifiers

Every service follows one set of rules (Template and Rules §R4). Nothing in this table is optional; the conformance rules in section 9 test it.

| Element | Rule | Example (P3) | Example (S6) |
|---|---|---|---|
| Service code | P1 to P10, S1 to S9 | P3 | S6 |
| Service name | `rwb-<short>` | rwb-case | rwb-debtsale |
| Schema and login | `rwb_<short with _>`; one login per service, the same name as the schema | rwb_case | rwb_debtsale |
| REST base | `/api/recovery/<short>/v1` behind gateway-bff | /api/recovery/case/v1 | /api/recovery/debtsale/v1 |
| Kafka topic | `rwb.<short>.events.v1` | rwb.case.events.v1 | rwb.debtsale.events.v1 |
| Retry and dead-letter topics | `rwb.<short>.events.v1` plus `.retry.1m`, `.retry.10m`, `.retry.1h` and `.dlt` | rwb.case.events.v1.dlt | rwb.debtsale.events.v1.dlt |
| Event names | `rwb.<short>.<Event>.v1` | rwb.case.CaseCreated.v1 | rwb.debtsale.LotAwarded.v1 |
| Temporal task queue | `rwb-<short>` in namespace rwb-recovery | rwb-case | rwb-debtsale |
| Java package | `th.co.scb.ace.workbench.recovery.<short without hyphen>` | th.co.scb.ace.workbench.recovery.case | th.co.scb.ace.workbench.recovery.debtsale |
| Service epic | `RWB-SVC-<code>` | RWB-SVC-P3 | RWB-SVC-S6 |
| Story scope | The service code prefixes every story ID | RWB-P3-E1018-APP | RWB-S6-E4011-APP |
| Decision record | Local record in the service schema plus DecisionRecorded on rwb.decision-record.v1 | same | same |

The event name pattern in the table is the documented rule; the event catalogue continues to name events by short name (CaseCreated, LotAwarded) and the topic carries the version. Both forms appear in this catalogue, and the topic is always named.

# 6. Service detail

One section per service, in Ownership Map order. Each section has the identity table, the contract table by call type, and the resources the service owns in its own schema. A row marked Out under Temporal is a call the service makes to another service on that service's queue.

## 6.1 P1 rwb-source-data — Source data

| Item | Value |
|---|---|
| Service code | P1 |
| Service | rwb-source-data |
| Service name | Source data |
| Wave (Arch v5) | 1 |
| Service epic | RWB-SVC-P1 |
| Schema | rwb_source_data |
| Login | rwb_source_data |
| REST base | /api/recovery/source-data/v1 |
| Kafka topic | rwb.source-data.events.v1 |
| Retry and dead-letter topics | rwb.source-data.events.v1.retry.1m, rwb.source-data.events.v1.retry.10m, rwb.source-data.events.v1.retry.1h, rwb.source-data.events.v1.dlt |
| Temporal task queue | rwb-source-data |
| Java package | th.co.scb.ace.workbench.recovery.sourcedata |
| Owns (Arch v5 slide 41) | ACE view contract, extension tables, freshness, reconciliation, product-to-source map (RD-P1-021) |
| First API path | /customers/{personKey} |
| Status | Draft |

**Contract by call type**

| Call type | Provided | Consumed |
|---|---|---|
| REST | GET /cases/{caseId}/interactions; POST /cases/{caseId}/interactions; GET /admin/jobs; POST /admin/jobs/{jobId}/rerun; GET /data-products/freshness (query product); GET /data-products/{productCode}/records; GET /admin/data-products; GET /admin/data-dictionary/fields; PATCH /admin/data-dictionary/fields/{fieldCode}; GET /admin/data-contracts; PATCH /admin/data-contracts/{contractId}; POST /admin/data-contracts/{contractId}/publish; POST /business-days/{date}/ready; GET /business-days/{date}/status; GET /cases/{caseId}/interactions/{entryId}; GET /efs-history (DP01 and DP05 gate; rwb-integration only); POST /retention-runs; GET /retention-runs/{runId}; GET /admin/reconciliation/results; GET /admin/reconciliation/results/{resultId}; GET /proof-of-delivery (rwb-comms only); GET /booking-facts; GET /batch-status (rwb-integration and rwb-payment); GET /payments (query exactly one of businessDate and accountKey); GET /accounts/{accountKey}/installment-facts; GET /contact-points; POST /contact-points/{contactPointKey}/failed-contacts; PUT /extension-facts/parties/{personKey}; PUT /extension-facts/accounts/{accountKey}; GET /customers/{personKey}; GET /accounts/{accountKey}; GET /collateral/{assetKey}; Pending: account-page read path and maximum keys per call, owner Solution architect, tracked as GAP-3274. | rwb-case: GET /parameters/{key}, reference loads and lists (RWB-P3-E1043-CON), GET /cases/retention-exclusions, GET /cases/closure-dates and case account keys. Paged open-case key-list Pending, owner rwb-case service owner (GAP-3273). rwb-integration: GET /admin/scheduled-jobs. rwb-access: POST /authorise (RWB-P4-E1016-APP; shape Pending, owner rwb-access contract owner, GAP-3322). |
| Kafka | AceDataReady (rwb-case, rwb-payment, rwb-integration, rwb-deviation, rwb-writeoff); AceDataLate; rwb.decision.DecisionRecorded.v1 (rwb.decision-record.v1) | Ledger intake: CaseCreated, CaseAllocated, CaseTransferred, TimerBreached (rwb.case.events.v1); DocumentStored (rwb.document.events.v1); DecisionRecorded (rwb.decision-record.v1). The service does not consume its own topic. |
| Temporal | Workflow: AceIngestCheck, ReconciliationWorkflow (JOB-04, child after the ALS stamp), Stage2ProductWorkflow, RetentionRunWorkflow; Activity: listEligibleAccounts, snapshot(page); Query: FreshnessQuery; Trigger: readiness handler, 05:30 Schedule rwb-source-data-ace-late-check, fallback poll (RD-P1-022/040). Pending: whether GET /payments replaces the slide 17 payments activity, owner solution architect, tracked as GAP-3556. | None. |
| File | None. | None. |
| SQL view | None. | 30 recovery.v_ace_* views, SELECT only. |

**Resources owned in rwb_source_data**

The platform library supplies local rwb_source_data.decision_record separately from the P1 business-table count (RD-P1-068).

| Table | Ownership basis |
|---|---|
| account_ext | Ownership Map v3, Tables sheet |
| business_day_readiness | Ownership Map v3, Tables sheet; RD-P1-021 |
| contact_point_ext | Ownership Map v3, Tables sheet |
| data_contract | Ownership Map v3, Tables sheet |
| data_product | Ownership Map v3, Tables sheet |
| data_product_access | Ownership Map v3, Tables sheet |
| data_product_load | Ownership Map v3, Tables sheet |
| dp_guarantee_claim | Ownership Map ruling dp_guarantee_claim |
| dp_treatment | Ownership Map ruling dp_treatment |
| efs_ledger_outcome | Ownership Map ruling efs_ledger_outcome |
| interaction | Ownership Map ruling interaction |
| job_run | Ownership Map v3, Tables sheet; RD-P1-021 |
| job_run_check | Ownership Map v3, Tables sheet; RD-P1-021 |
| party_ext | Ownership Map v3, Tables sheet |
| reconciliation_result | Ownership Map v3, Tables sheet |
| sys_field_version | Ownership Map v3, Tables sheet |
| sys_fields | Ownership Map v3, Tables sheet |
| sys_objects | Ownership Map v3, Tables sheet |
| valuation_ext | Ownership Map ruling valuation_ext |

**Notes**

- Reader of the 30 recovery.v_ace_* views, SELECT only (ADR-010). Cell of the interaction ledger (DP-18).

## 6.2 P2 rwb-integration — Integration

| Item | Value |
|---|---|
| Service code | P2 |
| Service | rwb-integration |
| Service name | Integration |
| Wave (Arch v5) | 1 |
| Service epic | RWB-SVC-P2 |
| Schema | rwb_integration |
| Login | rwb_integration |
| REST base | /api/recovery/integration/v1 |
| Kafka topic | rwb.integration.events.v1 |
| Retry and dead-letter topics | rwb.integration.events.v1.retry.1m, rwb.integration.events.v1.retry.10m, rwb.integration.events.v1.retry.1h, rwb.integration.events.v1.dlt |
| Temporal task queue | rwb-integration |
| Java package | th.co.scb.ace.workbench.recovery.integration |
| Owns (Arch v5 slide 41) | interface config, file runs, outbound items, ACE integration paths |
| First API path (Arch v5 slide 41) | /interface-runs |
| Status | Draft |

**Contract by call type**

| Call type | Provided | Consumed |
|---|---|---|
| REST | GET /interface-runs; POST /interface-runs/{id}/retry | REST: rwb-document: fetch file by ID (SAS link) |
| Kafka | FileDelivered; FileFailed; DecisionRecorded (rwb.decision-record.v1) | AceDataReady on rwb.source-data.events.v1 for JOB-08. |
| Temporal | Workflow: JOB-08 booking confirmation: own rwb-integration queue, ALS/COMPLETED AceDataReady; no Schedule; Activity: deliverFile(manifest), receiveFile; Window: Airflow file window: WIN file 16:00, buyer files per lot | None. |
| File | WIN (registered mail): daily outbound file (INT-14); debt buyers: per lot, encrypted (INT-25). | None. |
| SQL view | None. | None. |

**Resources owned in rwb_integration**

| Table | Ownership basis |
|---|---|
| interface_config | Ownership Map v3, Tables sheet |
| job_catalog | Ownership Map ruling job_catalog |
| outbound_item | Ownership Map v3, Tables sheet |

**Notes**

- Airflow never reads or writes rwb_* schemas; it calls service APIs only.

## 6.3 P3 rwb-case — Case and workflow

| Item | Value |
|---|---|
| Service code | P3 |
| Service | rwb-case |
| Service name | Case and workflow |
| Wave (Arch v5) | 1 |
| Service epic | RWB-SVC-P3 |
| Schema | rwb_case |
| Login | rwb_case |
| REST base | /api/recovery/case/v1 |
| Kafka topic | rwb.case.events.v1 |
| Retry and dead-letter topics | rwb.case.events.v1.retry.1m, rwb.case.events.v1.retry.10m, rwb.case.events.v1.retry.1h, rwb.case.events.v1.dlt |
| Temporal task queue | rwb-case |
| Java package | th.co.scb.ace.workbench.recovery.case |
| Owns (Arch v5 slide 41) | case, CMMN state, queues, tasks, allocation, timers |
| First API path (Arch v5 slide 41) | /cases/{id} |
| Status | Draft |

**Contract by call type**

| Call type | Provided | Consumed |
|---|---|---|
| REST | GET /cases/{id}; GET /cases?queue=; POST /cases/{id}/actions; GET /tasks; POST /tasks/{id}/complete; GET /case-summary/{id} (for the ACE shared case view); GET /parameters/{key} (RD-P1-063; service workload identities only) | REST: rwb-access: authorise (cached) |
| Kafka | CaseCreated; CaseAllocated; CaseAllocationFailed; CaseTransferred; CaseStateChanged; TimerBreached; DecisionRecorded (rwb.decision-record.v1) | CaseAllocationFailed; DeviationRaised; DeviationCleared; TreatmentBooked; PaymentMissed; NoticeDelivered; PartnerResultSubmitted; DocumentStored; DocumentFieldsExtracted; RouteDecided; AssetTakenOn; AssetSold; LotAwarded; WriteOffApproved; ProceedsMatched; JudgmentRecorded; AuctionResult; AccountsTransferred; TreatmentClosed; GuaranteeClaimFiled; GuaranteeClaimSettled; AceDataReady; RulePackageInForce |
| Temporal | Workflow: CaseWorkflow (parent, one per case); Workflow: DailyCaseRun: ALS/COMPLETED AceDataReady (JOB-02); no configured Schedule; Activity: allocate, transfer, rebalance; Schedule: Rebalancing 06:30 (JOB-06) | Source data: listEligibleAccounts(businessDate); Valuation: RouteDecisionWorkflow child; Treatment, guarantee, litigation, asset, debt sale and write-off stage workflows; Deviation: DeviationWorkflow child; Decision: ApprovalWorkflow child |
| File | None. | None. |
| SQL view | None. | None. |

**Resources owned in rwb_case**

| Table | Ownership basis |
|---|---|
| assignment | Ownership Map v3, Tables sheet |
| case_account | Ownership Map v3, Tables sheet |
| case_entry_exclusion | Ownership Map v3, Tables sheet |
| case_party | Ownership Map v3, Tables sheet |
| lov_value | Ownership Map ruling lov_value |
| parameter_catalog | Ownership Map v3, Tables sheet |
| parameter_value | Ownership Map v3, Tables sheet |
| queue | Ownership Map v3, Tables sheet |
| queue_measure | Ownership Map v3, Tables sheet |
| queue_member | Ownership Map v3, Tables sheet |
| recovery_case | Ownership Map v3, Tables sheet |
| reference_row | Ownership Map v3, Tables sheet |
| reference_version | Ownership Map v3, Tables sheet |
| task | Ownership Map v3, Tables sheet |
| timer | Ownership Map ruling timer |

**Notes**

- Case list API, parameters and reference data are P3 by the R-PREC default ruling (E1-042, E1-043).

## 6.4 P4 rwb-access — Access and authority

| Item | Value |
|---|---|
| Service code | P4 |
| Service | rwb-access |
| Service name | Access and authority |
| Wave (Arch v5) | 1 |
| Service epic | RWB-SVC-P4 |
| Schema | rwb_access |
| Login | rwb_access |
| REST base | /api/recovery/access/v1 |
| Kafka topic | rwb.access.events.v1 |
| Retry and dead-letter topics | rwb.access.events.v1.retry.1m, rwb.access.events.v1.retry.10m, rwb.access.events.v1.retry.1h, rwb.access.events.v1.dlt |
| Temporal task queue | rwb-access |
| Java package | th.co.scb.ace.workbench.recovery.access |
| Owns (Arch v5 slide 41) | Recovery roles as data, scope, masking policy, DoA table, access log |
| First API path (Arch v5 slide 41) | /authorise |
| Status | Draft |

**Contract by call type**

| Call type | Provided | Consumed |
|---|---|---|
| REST | POST /authorise (role, scope, DoA); GET /me/permissions; GET /doa-limits; GET /masking-policies | REST: ACE Common: sign-in, group-to-role (Entra) |
| Kafka | AccessPolicyChanged; DoaLimitChanged; DecisionRecorded (rwb.decision-record.v1) | None. |
| Temporal | Schedule: Access review list (six-monthly, JOB-18) | None. |
| File | None. | None. |
| SQL view | None. | None. |

**Resources owned in rwb_access**

| Table | Ownership basis |
|---|---|
| delegation_limit | Ownership Map ruling delegation_limit |
| masking_rule | Ownership Map v3, Tables sheet |
| permission | Ownership Map v3, Tables sheet |
| role | Ownership Map v3, Tables sheet |
| role_conflict | Ownership Map v3, Tables sheet |

**Notes**

- Reference-data owner: no events consumed.

## 6.5 P5 rwb-document — Document

| Item | Value |
|---|---|
| Service code | P5 |
| Service | rwb-document |
| Service name | Document |
| Wave (Arch v5) | 1 |
| Service epic | RWB-SVC-P5 |
| Schema | rwb_document |
| Login | rwb_document |
| REST base | /api/recovery/document/v1 |
| Kafka topic | rwb.document.events.v1 |
| Retry and dead-letter topics | rwb.document.events.v1.retry.1m, rwb.document.events.v1.retry.10m, rwb.document.events.v1.retry.1h, rwb.document.events.v1.dlt |
| Temporal task queue | rwb-document |
| Java package | th.co.scb.ace.workbench.recovery.document |
| Owns (Arch v5 slide 41) | metadata, custody, OCR text and fields, signatures, retention |
| First API path (Arch v5 slide 41) | /documents |
| Status | Draft |

**Contract by call type**

| Call type | Provided | Consumed |
|---|---|---|
| REST | POST /documents (returns upload link); GET /documents/{id}; GET /cases/{id}/documents; POST /documents/generate | None. |
| Kafka | DocumentStored; DocumentFieldsExtracted; DecisionRecorded (rwb.decision-record.v1) | AgentRunCompleted |
| Temporal | Workflow: DocumentIntakeWorkflow: OCR, classify, extract (JOB-12); Activity: generate, seal; Schedule: Retention monthly, first Sunday (JOB-17) | Agent: classify and extract child |
| File | Azure Blob (WORM): files, 2.8 TB by 2031. | None. |
| SQL view | None. | None. |

**Resources owned in rwb_document**

| Table | Ownership basis |
|---|---|
| case_document_check | Ownership Map v3, Tables sheet |
| document | Ownership Map v3, Tables sheet |
| document_checklist_item | Ownership Map v3, Tables sheet |
| document_custody | Ownership Map v3, Tables sheet |
| document_field | Ownership Map v3, Tables sheet |
| document_hub_parameter | Ownership Map v3, Tables sheet |
| document_intake | Ownership Map v3, Tables sheet |
| document_text | Ownership Map v3, Tables sheet |
| document_type | Ownership Map v3, Tables sheet |
| retention_action | Ownership Map v3, Tables sheet |
| retention_rule | Ownership Map ruling retention_rule |
| signature_request | Ownership Map ruling signature_request |

**Notes**

- The only service that holds document custody.

## 6.6 P6 rwb-comms — Communications

| Item | Value |
|---|---|
| Service code | P6 |
| Service | rwb-comms |
| Service name | Communications |
| Wave (Arch v5) | 1 |
| Service epic | RWB-SVC-P6 |
| Schema | rwb_comms |
| Login | rwb_comms |
| REST base | /api/recovery/comms/v1 |
| Kafka topic | rwb.comms.events.v1 |
| Retry and dead-letter topics | rwb.comms.events.v1.retry.1m, rwb.comms.events.v1.retry.10m, rwb.comms.events.v1.retry.1h, rwb.comms.events.v1.dlt |
| Temporal task queue | rwb-comms |
| Java package | th.co.scb.ace.workbench.recovery.comms |
| Owns (Arch v5 slide 41) | notices, templates, merge fields, proof of delivery |
| First API path (Arch v5 slide 41) | /notices |
| Status | Draft |

**Contract by call type**

| Call type | Provided | Consumed |
|---|---|---|
| REST | POST /notices (request); GET /cases/{id}/notices | REST: ACE Common: notification path (SMS, LINE) |
| Kafka | NoticeGenerated; NoticeDispatched; NoticeDelivered; DecisionRecorded (rwb.decision-record.v1) | DeviationRaised; DeviationCleared; TreatmentApproved; PaymentMissed; CaseStateChanged |
| Temporal | Workflow: NoticeDispatchWorkflow (kit template); Schedule: WIN notices 16:00 (JOB-10) | Document: generate letter; Decision: approval child; Integration: deliverFile (WIN letters) |
| File | WIN letters handed to rwb-integration (INT-14). | None. |
| SQL view | None. | None. |

**Resources owned in rwb_comms**

| Table | Ownership basis |
|---|---|
| merge_field | Ownership Map v3, Tables sheet |
| notice | Ownership Map v3, Tables sheet |
| template | Ownership Map v3, Tables sheet |

**Notes**

- Contact stop on DeviationRaised and DeviationCleared.

## 6.7 P7 rwb-decision — Decision and rules

| Item | Value |
|---|---|
| Service code | P7 |
| Service | rwb-decision |
| Service name | Decision and rules |
| Wave (Arch v5) | 1 |
| Service epic | RWB-SVC-P7 |
| Schema | rwb_decision |
| Login | rwb_decision |
| REST base | /api/recovery/decision/v1 |
| Kafka topic | rwb.decision.events.v1 |
| Retry and dead-letter topics | rwb.decision.events.v1.retry.1m, rwb.decision.events.v1.retry.10m, rwb.decision.events.v1.retry.1h, rwb.decision.events.v1.dlt |
| Temporal task queue | rwb-decision |
| Java package | th.co.scb.ace.workbench.recovery.decision |
| Owns (Arch v5 slide 41) | approvals, central decision ledger, DMN model registry |
| First API path (Arch v5 slide 41) | /decisions |
| Status | Draft |

**Contract by call type**

| Call type | Provided | Consumed |
|---|---|---|
| REST | GET /decisions?caseId=; POST /approvals/{id}/decide; POST /rule-models; GET /rule-models/{n}/{v} | REST: rwb-access: DoA limits |
| Kafka | ApprovalRequested; ApprovalDecided; RulePackageInForce; DecisionRecorded (rwb.decision-record.v1) | DecisionRecorded; NoticeGenerated; AgentRunCompleted |
| Temporal | Workflow: ApprovalWorkflow (kit template); Schedule: Rule promote 00:01 (JOB-20, Temporal Schedule; no AceDataReady trigger); chain check 02:00 (JOB-14); Ingest: Continuous DecisionRecorded ingest from Kafka (JOB-13) | None. |
| File | Immutable storage: daily ledger seal (WORM). | None. |
| SQL view | None. | None. |

**Resources owned in rwb_decision**

| Table | Ownership basis |
|---|---|
| approval | Ownership Map v3, Tables sheet |
| decision_log_entry | Ownership Map v3, Tables sheet |
| rule_package | Ownership Map ruling rule registry |
| rule_package_version | Ownership Map ruling rule registry |
| rule_row | Ownership Map ruling rule registry |
| rule_test_case | Ownership Map ruling rule registry |

**Notes**

- Owner of the shared topic rwb.decision-record.v1 and of the rule package registry (default ruling).
- `ApprovalDecided` is published on rwb.decision.events.v1; the Architecture v5 event catalogue names no consumer for it. Not specified in the source documents (GAP-0137; ASM-0215).

## 6.8 P8 rwb-payment — Payment

| Item | Value |
|---|---|
| Service code | P8 |
| Service | rwb-payment |
| Service name | Payment |
| Wave (Arch v5) | 2 |
| Service epic | RWB-SVC-P8 |
| Schema | rwb_payment |
| Login | rwb_payment |
| REST base | /api/recovery/payment/v1 |
| Kafka topic | rwb.payment.events.v1 |
| Retry and dead-letter topics | rwb.payment.events.v1.retry.1m, rwb.payment.events.v1.retry.10m, rwb.payment.events.v1.retry.1h, rwb.payment.events.v1.dlt |
| Temporal task queue | rwb-payment |
| Java package | th.co.scb.ace.workbench.recovery.payment |
| Owns (Arch v5 slide 41) | payment and proceeds matching, fees, bookings, posting files |
| First API path (Arch v5 slide 41) | /cases/{id}/payments |
| Status | Draft |

**Contract by call type**

| Call type | Provided | Consumed |
|---|---|---|
| REST | GET /cases/{id}/payments; POST /proceeds/{id}/allocate (manual) | None. |
| Kafka | TreatmentBooked; PaymentMissed; ProceedsMatched; DecisionRecorded (rwb.decision-record.v1) | AceDataReady; TreatmentApproved; LotAwarded; AssetSold; WriteOffApproved |
| Temporal | Workflow: Event-started workflows from AceDataReady; Activity: matchPayments (JOB-07); Activity: postProceeds (saga step) | Source data: payments for the business date; Integration: deliverFile (posting file) |
| File | Posting file through rwb-integration. | None. |
| SQL view | None. | None. |

**Resources owned in rwb_payment**

| Table | Ownership basis |
|---|---|
| payment_match_rule | Ownership Map v3, Tables sheet (GAP-0133) |
| proceeds | Ownership Map v3, Tables sheet |

The Ownership Map v3 holds `proceeds` and `payment_match_rule` for P8 (D-RCV-60, GAP-0133). Architecture v5 slide 41 also names fees, bookings and posting files, for which no table is named.

**Notes**

- Source data supplies the payments for the business date.

## 6.9 P9 rwb-reporting — Reporting

| Item | Value |
|---|---|
| Service code | P9 |
| Service | rwb-reporting |
| Service name | Reporting |
| Wave (Arch v5) | 1 |
| Service epic | RWB-SVC-P9 |
| Schema | rwb_reporting |
| Login | rwb_reporting |
| REST base | /api/recovery/reporting/v1 |
| Kafka topic | rwb.reporting.events.v1 |
| Retry and dead-letter topics | rwb.reporting.events.v1.retry.1m, rwb.reporting.events.v1.retry.10m, rwb.reporting.events.v1.retry.1h, rwb.reporting.events.v1.dlt |
| Temporal task queue | rwb-reporting |
| Java package | th.co.scb.ace.workbench.recovery.reporting |
| Owns (Arch v5 slide 41) | measures, snapshots, steering dashboard, regulatory reports |
| First API path (Arch v5 slide 41) | /dashboards/{id} |
| Status | Draft |

**Contract by call type**

| Call type | Provided | Consumed |
|---|---|---|
| REST | GET /dashboards/{id}; GET /reports/{id}; POST /reports/{id}/run (Airflow) | None. |
| Kafka | ReportPublished; DecisionRecorded (rwb.decision-record.v1) | All business events (projections); DecisionRecorded |
| Temporal | Activity: buildRegulatoryExtract; JOB-15: 01:30 Airflow POST /reports/{id}/run is live; the 01:30 Temporal Schedule is paused. Pending: final trigger, owner solution architect with the rwb-reporting owner (GAP-3573). | Source data: snapshot(page) for measures; Integration: deliverFile (regulatory extract) |
| File | Regulatory extract through rwb-integration. | None. |
| SQL view | None. | None. |

**Resources owned in rwb_reporting**

| Table | Ownership basis |
|---|---|
| measure_definition | Ownership Map v3, Tables sheet |
| measure_publish | Ownership Map v3, Tables sheet |
| measure_snapshot | Ownership Map v3, Tables sheet |

**Notes**

- No data lake: projections are built from events (DP-17).
- `ReportPublished` is published on rwb.reporting.events.v1; the Architecture v5 event catalogue names no consumer for it. Not specified in the source documents (GAP-0137; ASM-0215).

## 6.10 P10 rwb-agent — Agent

| Item | Value |
|---|---|
| Service code | P10 |
| Service | rwb-agent |
| Service name | Agent |
| Wave (Arch v5) | 1 |
| Service epic | RWB-SVC-P10 |
| Schema | rwb_agent |
| Login | rwb_agent |
| REST base | /api/recovery/agent/v1 |
| Kafka topic | rwb.agent.events.v1 |
| Retry and dead-letter topics | rwb.agent.events.v1.retry.1m, rwb.agent.events.v1.retry.10m, rwb.agent.events.v1.retry.1h, rwb.agent.events.v1.dlt |
| Temporal task queue | rwb-agent |
| Java package | th.co.scb.ace.workbench.recovery.agent |
| Owns (Arch v5 slide 41) | agent policies, prompts, runs, guardrails, evaluations |
| First API path (Arch v5 slide 41) | /agent-runs/{id} |
| Status | Draft |

**Contract by call type**

| Call type | Provided | Consumed |
|---|---|---|
| REST | GET /agent-runs/{id}; GET /agent-policies (admin); POST /agent-policies (admin) | REST: rwb-source-data: tool, read case facts; REST: rwb-document: tool, read extracted fields; REST: Enterprise AI endpoint: HTTPS private endpoint |
| Kafka | AgentRunCompleted; DecisionRecorded (rwb.decision-record.v1) | DocumentStored; CaseCreated |
| Temporal | Workflow: AgentRunWorkflow: 60 s, then the rule result | Tool gateway: Source data (case facts), Document (extracted fields), Enterprise AI endpoint |
| File | None. | None. |
| SQL view | None. | None. |

**Resources owned in rwb_agent**

| Table | Ownership basis |
|---|---|
| agent_alert | Ownership Map v3, Tables sheet |
| agent_evaluation | Ownership Map v3, Tables sheet |
| agent_evaluation_run | Ownership Map v3, Tables sheet |
| agent_feedback | Ownership Map v3, Tables sheet |
| agent_policy | Ownership Map v3, Tables sheet |
| agent_prompt | Ownership Map v3, Tables sheet |
| agent_run | Ownership Map v3, Tables sheet |
| agent_sample | Ownership Map v3, Tables sheet |

**Notes**

- Falls back to the rule result when the agent does not answer within 60 s.

## 6.11 S1 rwb-valuation — Valuation and route

| Item | Value |
|---|---|
| Service code | S1 |
| Service | rwb-valuation |
| Service name | Valuation and route |
| Wave (Arch v5) | 3 |
| Service epic | RWB-SVC-S1 |
| Schema | rwb_valuation |
| Login | rwb_valuation |
| REST base | /api/recovery/valuation/v1 |
| Kafka topic | rwb.valuation.events.v1 |
| Retry and dead-letter topics | rwb.valuation.events.v1.retry.1m, rwb.valuation.events.v1.retry.10m, rwb.valuation.events.v1.retry.1h, rwb.valuation.events.v1.dlt |
| Temporal task queue | rwb-valuation |
| Java package | th.co.scb.ace.workbench.recovery.valuation |
| Owns (Arch v5 slide 41) | valuations, D6 route decision, route agent output |
| First API path (Arch v5 slide 41) | /cases/{id}/valuation |
| Status | Draft |

**Contract by call type**

| Call type | Provided | Consumed |
|---|---|---|
| REST | GET /cases/{id}/valuation; POST /cases/{id}/route-proposals | REST: rwb-source-data: collateral, appraisals |
| Kafka | RouteDecided; DecisionRecorded (rwb.decision-record.v1) | RulePackageInForce |
| Temporal | Workflow: RouteDecisionWorkflow (stage workflow, started by rwb-case) | Agent: route agent child; Decision: approval child |
| File | None. | None. |
| SQL view | None. | None. |

**Resources owned in rwb_valuation**

| Table | Ownership basis |
|---|---|
| valuation | Ownership Map v3, Tables sheet (GAP-0132) |

**Notes**

- Route decision under D6; the rule package version is written to the decision record.

## 6.12 S2 rwb-treatment — Treatment and offer

| Item | Value |
|---|---|
| Service code | S2 |
| Service | rwb-treatment |
| Service name | Treatment and offer |
| Wave (Arch v5) | 2 |
| Service epic | RWB-SVC-S2 |
| Schema | rwb_treatment |
| Login | rwb_treatment |
| REST base | /api/recovery/treatment/v1 |
| Kafka topic | rwb.treatment.events.v1 |
| Retry and dead-letter topics | rwb.treatment.events.v1.retry.1m, rwb.treatment.events.v1.retry.10m, rwb.treatment.events.v1.retry.1h, rwb.treatment.events.v1.dlt |
| Temporal task queue | rwb-treatment |
| Java package | th.co.scb.ace.workbench.recovery.treatment |
| Owns (Arch v5 slide 41) | treatments, contracts, settlement and deed-in-lieu agreements, plan timers |
| First API path (Arch v5 slide 41) | /treatments |
| Status | Draft |

**Contract by call type**

| Call type | Provided | Consumed |
|---|---|---|
| REST | GET /treatments; POST /treatments; POST /treatments/{id}/offer | NEXUS: ACE Common: restructure calculator (Nexus) |
| Kafka | TreatmentApproved; TreatmentClosed; DecisionRecorded (rwb.decision-record.v1) | TreatmentBooked; PaymentMissed; DeviationRaised |
| Temporal | Workflow: TreatmentWorkflow: settlement and deed-in-lieu sagas | Decision: approval child; Document: contract and e-sign; Payment: postProceeds |
| File | None. | None. |
| SQL view | None. | None. |

**Resources owned in rwb_treatment**

| Table | Ownership basis |
|---|---|
| treatment | Ownership Map v3, Tables sheet |

**Notes**

- Pivots: debt released once the customer pays; title transfer registered.

## 6.13 S3 rwb-guarantee — Guarantee

| Item | Value |
|---|---|
| Service code | S3 |
| Service | rwb-guarantee |
| Service name | Guarantee |
| Wave (Arch v5) | 3 |
| Service epic | RWB-SVC-S3 |
| Schema | rwb_guarantee |
| Login | rwb_guarantee |
| REST base | /api/recovery/guarantee/v1 |
| Kafka topic | rwb.guarantee.events.v1 |
| Retry and dead-letter topics | rwb.guarantee.events.v1.retry.1m, rwb.guarantee.events.v1.retry.10m, rwb.guarantee.events.v1.retry.1h, rwb.guarantee.events.v1.dlt |
| Temporal task queue | rwb-guarantee |
| Java package | th.co.scb.ace.workbench.recovery.guarantee |
| Owns (Arch v5 slide 41) | TCG and insurance claims, guarantor notices and pursuit |
| First API path (Arch v5 slide 41) | /guarantee-claims |
| Status | Draft |

**Contract by call type**

| Call type | Provided | Consumed |
|---|---|---|
| REST | GET /guarantee-claims; POST /guarantee-claims | None. |
| Kafka | GuaranteeClaimFiled; GuaranteeClaimSettled; DecisionRecorded (rwb.decision-record.v1) | NoticeDelivered; ProceedsMatched |
| Temporal | Workflow: GuaranteeClaimWorkflow | Comms: guarantor notice child; Decision: approval child |
| File | None. | None. |
| SQL view | None. | None. |

**Resources owned in rwb_guarantee**

| Table | Ownership basis |
|---|---|
| guarantee_claim | Ownership Map v3, Tables sheet |

**Notes**

- TCG and insurer claims sit on the same claim record.

## 6.14 S4 rwb-litigation — Litigation

| Item | Value |
|---|---|
| Service code | S4 |
| Service | rwb-litigation |
| Service name | Litigation |
| Wave (Arch v5) | 3 |
| Service epic | RWB-SVC-S4 |
| Schema | rwb_litigation |
| Login | rwb_litigation |
| REST base | /api/recovery/litigation/v1 |
| Kafka topic | rwb.litigation.events.v1 |
| Retry and dead-letter topics | rwb.litigation.events.v1.retry.1m, rwb.litigation.events.v1.retry.10m, rwb.litigation.events.v1.retry.1h, rwb.litigation.events.v1.dlt |
| Temporal task queue | rwb-litigation |
| Java package | th.co.scb.ace.workbench.recovery.litigation |
| Owns (Arch v5 slide 41) | legal actions, hearings, judgments, enforcement, LED auction ladder |
| First API path (Arch v5 slide 41) | /legal-actions |
| Status | Draft |

**Contract by call type**

| Call type | Provided | Consumed |
|---|---|---|
| REST | GET /legal-actions; POST /legal-actions; GET /hearings; POST /hearings | None. |
| Kafka | LawsuitFiled; JudgmentRecorded; AuctionResult; DecisionRecorded (rwb.decision-record.v1) | NoticeDelivered; PartnerResultSubmitted |
| Temporal | Workflow: LitigationWorkflow (years; continues-as-new) | Partner: issueInstruction (law firm); Comms: demand notice child; Decision: approval child |
| File | None. | None. |
| SQL view | None. | None. |

**Resources owned in rwb_litigation**

| Table | Ownership basis |
|---|---|
| hearing | Ownership Map v3, Tables sheet |
| legal_action | Ownership Map v3, Tables sheet |

**Notes**

- The longest-running stage; Continue-As-New at every stage end and at least every 28 days.

## 6.15 S5 rwb-asset — Asset

| Item | Value |
|---|---|
| Service code | S5 |
| Service | rwb-asset |
| Service name | Asset |
| Wave (Arch v5) | 2 |
| Service epic | RWB-SVC-S5 |
| Schema | rwb_asset |
| Login | rwb_asset |
| REST base | /api/recovery/asset/v1 |
| Kafka topic | rwb.asset.events.v1 |
| Retry and dead-letter topics | rwb.asset.events.v1.retry.1m, rwb.asset.events.v1.retry.10m, rwb.asset.events.v1.retry.1h, rwb.asset.events.v1.dlt |
| Temporal task queue | rwb-asset |
| Java package | th.co.scb.ace.workbench.recovery.asset |
| Owns (Arch v5 slide 41) | assets taken on, holding, floor price, listings, auction rounds |
| First API path (Arch v5 slide 41) | /assets |
| Status | Draft |

**Contract by call type**

| Call type | Provided | Consumed |
|---|---|---|
| REST | GET /assets; POST /assets; GET /listings; POST /listings; POST /auction-rounds | None. |
| Kafka | AssetTakenOn; AssetSold; DecisionRecorded (rwb.decision-record.v1) | JudgmentRecorded; AuctionResult; ProceedsMatched |
| Temporal | Workflow: AssetDisposalWorkflow; Schedule: Re-appraisal monthly (JOB-19) | Partner: issueInstruction (auction vendor); Decision: approval child; Payment: postProceeds |
| File | None. | None. |
| SQL view | None. | None. |

**Resources owned in rwb_asset**

| Table | Ownership basis |
|---|---|
| asset_sale | Ownership Map v3, Tables sheet |
| listing | Ownership Map v3, Tables sheet |

**Notes**

- The LED auction ladder is shared with rwb-litigation through events.

## 6.16 S6 rwb-debtsale — Debt sale

| Item | Value |
|---|---|
| Service code | S6 |
| Service | rwb-debtsale |
| Service name | Debt sale |
| Wave (Arch v5) | 3 |
| Service epic | RWB-SVC-S6 |
| Schema | rwb_debtsale |
| Login | rwb_debtsale |
| REST base | /api/recovery/debtsale/v1 |
| Kafka topic | rwb.debtsale.events.v1 |
| Retry and dead-letter topics | rwb.debtsale.events.v1.retry.1m, rwb.debtsale.events.v1.retry.10m, rwb.debtsale.events.v1.retry.1h, rwb.debtsale.events.v1.dlt |
| Temporal task queue | rwb-debtsale |
| Java package | th.co.scb.ace.workbench.recovery.debtsale |
| Owns (Arch v5 slide 41) | lots, data room, buyer terms, bids, award, transfer |
| First API path (Arch v5 slide 41) | /lots |
| Status | Draft |

**Contract by call type**

| Call type | Provided | Consumed |
|---|---|---|
| REST | GET /lots; POST /lots; POST /lots/{id}/bids; POST /lots/{id}/award | None. |
| Kafka | LotAwarded; AccountsTransferred; DecisionRecorded (rwb.decision-record.v1) | ProceedsMatched |
| Temporal | Workflow: DebtSaleWorkflow (saga, pivot = transfer) | Document: data room pack; Decision: approval child; Integration: deliverFile (buyer file); Payment: postProceeds |
| File | Buyer file per lot through rwb-integration (INT-25). | None. |
| SQL view | None. | None. |

**Resources owned in rwb_debtsale**

| Table | Ownership basis |
|---|---|
| debt_sale_account | Ownership Map v3, Tables sheet |
| debt_sale_lot | Ownership Map v3, Tables sheet |

**Notes**

- Seven-step saga across five services; the point of no return is the transfer.

## 6.17 S7 rwb-writeoff — Write-off

| Item | Value |
|---|---|
| Service code | S7 |
| Service | rwb-writeoff |
| Service name | Write-off |
| Wave (Arch v5) | 4 |
| Service epic | RWB-SVC-S7 |
| Schema | rwb_writeoff |
| Login | rwb_writeoff |
| REST base | /api/recovery/writeoff/v1 |
| Kafka topic | rwb.writeoff.events.v1 |
| Retry and dead-letter topics | rwb.writeoff.events.v1.retry.1m, rwb.writeoff.events.v1.retry.10m, rwb.writeoff.events.v1.retry.1h, rwb.writeoff.events.v1.dlt |
| Temporal task queue | rwb-writeoff |
| Java package | th.co.scb.ace.workbench.recovery.writeoff |
| Owns (Arch v5 slide 41) | eligibility, committee, posting, recovery after charge-off |
| First API path (Arch v5 slide 41) | /write-offs |
| Status | Draft |

**Contract by call type**

| Call type | Provided | Consumed |
|---|---|---|
| REST | GET /write-offs; POST /write-offs; POST /write-offs/{id}/submit | REST: rwb-source-data: GL outcome |
| Kafka | WriteOffApproved; DecisionRecorded (rwb.decision-record.v1) | AceDataReady; ProceedsMatched |
| Temporal | Workflow: WriteOffWorkflow; Schedule: Scan, third working day (JOB-16) | Decision: committee approval child; Payment: postProceeds |
| File | None. | None. |
| SQL view | None. | None. |

**Resources owned in rwb_writeoff**

| Table | Ownership basis |
|---|---|
| write_off | Ownership Map v3, Tables sheet |

**Notes**

- Recovery after charge-off continues on the same case.

## 6.18 S8 rwb-deviation — Deviation

| Item | Value |
|---|---|
| Service code | S8 |
| Service | rwb-deviation |
| Service name | Deviation |
| Wave (Arch v5) | 2 |
| Service epic | RWB-SVC-S8 |
| Schema | rwb_deviation |
| Login | rwb_deviation |
| REST base | /api/recovery/deviation/v1 |
| Kafka topic | rwb.deviation.events.v1 |
| Retry and dead-letter topics | rwb.deviation.events.v1.retry.1m, rwb.deviation.events.v1.retry.10m, rwb.deviation.events.v1.retry.1h, rwb.deviation.events.v1.dlt |
| Temporal task queue | rwb-deviation |
| Java package | th.co.scb.ace.workbench.recovery.deviation |
| Owns (Arch v5 slide 41) | X1-X7 screening, pause, handling, return |
| First API path (Arch v5 slide 41) | /deviations |
| Status | Draft |

**Contract by call type**

| Call type | Provided | Consumed |
|---|---|---|
| REST | GET /deviations; POST /deviations; POST /deviations/{id}/clear | REST: rwb-source-data: party flags |
| Kafka | DeviationRaised; DeviationCleared; DecisionRecorded (rwb.decision-record.v1) | CaseCreated; AceDataReady; AgentRunCompleted |
| Temporal | Workflow: DeviationWorkflow (child of case) | Agent: screening agent run |
| File | None. | None. |
| SQL view | None. | None. |

**Resources owned in rwb_deviation**

| Table | Ownership basis |
|---|---|
| deviation | Ownership Map v3, Tables sheet |

**Notes**

- Can start at any time and pauses the stage clock.

## 6.19 S9 rwb-partner — Partner

| Item | Value |
|---|---|
| Service code | S9 |
| Service | rwb-partner |
| Service name | Partner |
| Wave (Arch v5) | 4 |
| Service epic | RWB-SVC-S9 |
| Schema | rwb_partner |
| Login | rwb_partner |
| REST base | /api/recovery/partner/v1 |
| Kafka topic | rwb.partner.events.v1 |
| Retry and dead-letter topics | rwb.partner.events.v1.retry.1m, rwb.partner.events.v1.retry.10m, rwb.partner.events.v1.retry.1h, rwb.partner.events.v1.dlt |
| Temporal task queue | rwb-partner |
| Java package | th.co.scb.ace.workbench.recovery.partner |
| Owns (Arch v5 slide 41) | panel, partner users, instructions, results, fees, scorecards |
| First API path (Arch v5 slide 41) | /partners |
| Status | Draft |

**Contract by call type**

| Call type | Provided | Consumed |
|---|---|---|
| REST | GET /partners (staff); POST /partners (staff); GET /instructions; POST /instructions; /partner/v1/* (partner portal, FAPI 2.0, through the partner gateway) | rwb-source-data: POST /cases/{caseId}/interactions (Case record C, PARTNER_RESULT, partner code as actorRef). REST: rwb-document: partner uploads (link); REST: Partners (law firms, agencies, buyers): via the partner gateway, MFA |
| Kafka | InstructionIssued; PartnerResultSubmitted; DecisionRecorded (rwb.decision-record.v1) | None. |
| Temporal | Workflow: InstructionWorkflow: SLA timers; Activity: issueInstruction, recordResult | Document: partner uploads (REST) |
| File | None. | None. |
| SQL view | None. | None. |

**Resources owned in rwb_partner**

| Table | Ownership basis |
|---|---|
| partner | Ownership Map v3, Tables sheet |
| partner_instruction | Ownership Map v3, Tables sheet |
| partner_user | Ownership Map ruling partner_user |

**Notes**

- Work arrives as Temporal tasks; the partner portal is the only partner surface, behind the partner gateway.

# 7. Resource ownership

The tables of the current recovery schema are split across the 19 service schemas. The Ownership Map v3 assigns every table, and the counts below are the rows of its Tables sheet. Seven further tables are library objects that the template creates in every service schema, so they are owned once by the platform library (PLT) and instantiated 19 times.

| Code | Service | Schema | Tables | Tables owned |
|---|---|---|---|---|
| P1 | rwb-source-data | rwb_source_data | 20 | account_ext, business_day_readiness, contact_point_ext, data_contract, data_product, data_product_access, data_product_load, data_product_source, dp_guarantee_claim, dp_treatment, efs_ledger_outcome, interaction, job_run, job_run_check, party_ext, reconciliation_result, sys_field_version, sys_fields, sys_objects, valuation_ext |
| P2 | rwb-integration | rwb_integration | 3 | interface_config, job_catalog, outbound_item |
| P3 | rwb-case | rwb_case | 15 | assignment, case_account, case_entry_exclusion, case_party, lov_value, parameter_catalog, parameter_value, queue, queue_measure, queue_member, recovery_case, reference_row, reference_version, task, timer |
| P4 | rwb-access | rwb_access | 5 | delegation_limit, masking_rule, permission, role, role_conflict |
| P5 | rwb-document | rwb_document | 12 | case_document_check, document, document_checklist_item, document_custody, document_field, document_hub_parameter, document_intake, document_text, document_type, retention_action, retention_rule, signature_request |
| P6 | rwb-comms | rwb_comms | 3 | merge_field, notice, template |
| P7 | rwb-decision | rwb_decision | 6 | approval, decision_log_entry, rule_package, rule_package_version, rule_row, rule_test_case |
| P8 | rwb-payment | rwb_payment | 2 | payment_match_rule, proceeds |
| P9 | rwb-reporting | rwb_reporting | 3 | measure_definition, measure_publish, measure_snapshot |
| P10 | rwb-agent | rwb_agent | 8 | agent_alert, agent_evaluation, agent_evaluation_run, agent_feedback, agent_policy, agent_prompt, agent_run, agent_sample |
| S1 | rwb-valuation | rwb_valuation | 1 | valuation |
| S2 | rwb-treatment | rwb_treatment | 1 | treatment |
| S3 | rwb-guarantee | rwb_guarantee | 1 | guarantee_claim |
| S4 | rwb-litigation | rwb_litigation | 2 | hearing, legal_action |
| S5 | rwb-asset | rwb_asset | 2 | asset_sale, listing |
| S6 | rwb-debtsale | rwb_debtsale | 2 | debt_sale_account, debt_sale_lot |
| S7 | rwb-writeoff | rwb_writeoff | 1 | write_off |
| S8 | rwb-deviation | rwb_deviation | 1 | deviation |
| S9 | rwb-partner | rwb_partner | 3 | partner, partner_instruction, partner_user |
| PLT | platform library | every rwb_* schema | 7 | decision_record, feature_flag, feature_flag_change, idempotency_key, outbox_event, outbox_delivery, processed_event |

Totals: 91 business tables across the 19 services, 7 library tables instantiated in every schema, and one schema and login per service.

Rules that hold for every table (Arch v5 slide 29):

- A service writes only its own schema and has no grant on any other schema.
- No cross-schema joins, views or foreign keys. Services hold each other's IDs and use contracts for everything else.
- Each service runs its own Flyway migrations in its own pipeline; a boundary test in every build fails on any cross-schema reference.
- Each login goes through its own PgBouncer pool with a connection cap and a statement timeout.
- Only rwb_source_data has SELECT on the 30 recovery.v_ace_* views.

# 8. Service-to-service call summary

The call types below are the engineering standards of Architecture v5 slides 10 to 12, applied to every service in section 6. A service never mixes them: a REST call answers a person, an event announces a fact, a Temporal call commands a step, a file moves bulk data, and only rwb-source-data reads the ACE views.

| Call type | Where it is used | Contract | Failure handling | Source |
|---|---|---|---|---|
| REST | A person waits for the answer: gateway-bff to the owner, one hop, in parallel for composite screens | OpenAPI 3.1, /v1 in the path | 2 s timeout, one GET retry with jitter, circuit breaker and bulkhead per downstream, RFC 9457 problem details | Arch v5 slides 10, 11, 13 |
| Kafka event | A fact others may react to; never a command | AsyncAPI 3.0, CloudEvents 1.0 binary mode, JSON Schema registry BACKWARD | Outbox, inbox dedupe, retry 1 min, 10 min, 1 h then .dlt with an alert and a replay tool | Arch v5 slides 11, 22, 42, 43 |
| Temporal | A step in another service or a long process; a child workflow per stage | Typed activity and workflow interface in a contract jar on queue `rwb-<svc>` | Typed failures, non-retryable list, start-to-close per activity, saga undo before the pivot | Arch v5 slides 11, 23, 24, 25, 26 |
| File | Bulk data or a party outside the bank | Manifest: fileId, batchId, sha256, record count; SAS link open for 15 minutes | FileFailed event, operator retry, checksum on receipt | Arch v5 slide 11 |
| SQL view | Reading ACE data, rwb-source-data only | 30 recovery.v_ace_* views (ADR-010) | 5 s statement timeout; mapped to domain errors by P1 | Arch v5 slides 11 and 29 |

Rules that the call types enforce (Arch v5 slide 13): route services reach the shared capabilities through Temporal, never REST; only rwb-source-data touches ACE's tables; rwb-decision and rwb-reporting listen widely and call almost nobody; the case router in rwb-case turns events into signals and never calls another service directly for a business step.

# 9. What every service must provide

A service is conformant when all of the following are true. The same list is the Definition of Done in the Service Template Specification v1.

| # | Conformance rule | Tested by |
|---|---|---|
| 1 | Code, name, schema, login, REST base, topic, retry and dead-letter topics, task queue and Java package follow section 5 exactly | Template conformance test in the build |
| 2 | The service is built from the service template and the shared libraries: Spring Boot, outbox relay, inbox, Temporal worker, payload codec, OpenTelemetry, contract tests | Pipeline gate |
| 3 | The OpenAPI 3.1 contract, the AsyncAPI 3.0 contract and the activity contract jar are published before the code | Contract test in every build |
| 4 | Every write and the event it produces are one local transaction in the service's own schema | Outbox test |
| 5 | Every consumed event is deduplicated through processed_event in the same transaction as the change | Inbox test |
| 6 | The boundary test fails on any cross-schema reference | Architecture test |
| 7 | Every decision writes a local, hash-linked decision record and publishes DecisionRecorded | Decision record test |
| 8 | Rules are evaluated in an activity, under 300 ms, with the package version in the record | Rules test |
| 9 | Traces, metrics and logs go to OpenTelemetry; /health and /metrics exist | Platform check |
| 10 | The service owns a contract story (CON) in its service epic before any build story starts | Story set check |

# 10. Open points

| ID | Point | Effect in this catalogue | Owner role |
|---|---|---|---|
| GAP-0132 | The Ownership Map v1 held no table for rwb-valuation; the Ownership Map v3 holds `valuation` (D-RCV-60) | Section 6.11 lists the table | Solution architect |
| GAP-0133 | The Ownership Map v1 held only proceeds for rwb-payment; the Ownership Map v3 also holds `payment_match_rule` (D-RCV-60) | Section 6.8 lists the table | Solution architect |
| GAP-0137 | The event catalogue does not name the consumers of ApprovalDecided or ReportPublished | Section 6.6 and 6.9 carry the placeholder | Solution architect |
| GAP-0140 | No earlier Service Catalog exists, so v1 carries no inherited IDs, numbers or dates | Version 1, status Draft; the change log row is the first | Delivery lead |
| GAP-0141 | The API Specification v4 paths are the monolith paths, while this catalogue states the per-service base; the per-service operations are rewritten in API Specification v5 | Section 6 states the Architecture v5 contract and the map's ownership; the operation list is left to API Specification v5 | Solution architect |

The five open points on the template side are in the Service Template Specification v1 §21: GAP-0134 (stack versions), GAP-0135 (repository name and location), GAP-0136 (chart, release and registry), GAP-0138 (decision_record in every schema) and GAP-0139 (pipeline tool).

The full text of every gap and assumption is in the Gap Register and the Assumptions Register (folder 23). Candidate rows are in `_work/msr/gaps/B-ARCH-SVC.jsonl` and `_work/msr/assumptions/B-ARCH-SVC.jsonl`.

# 11. Change log

| Version | Date | Change | Detail |
|---|---|---|---|
| 1 | 22 November 2026 | D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash | First Service Catalog: 19 services, 19 schemas and logins, 19 topics with retry and dead-letter topics, 19 task queues, the resources of the Ownership Map v1, and the per-service contract by call type. |
| 2 | 27 November 2026 | D-RCV-60 P1 developer readiness (RD-P1 register) | Targeted edits: rwb-source-data resources, contracts, events and workflows; resource counts read from the Ownership Map v3. |
