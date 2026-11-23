## Read me

| Item | Value |
|---|---|
| SCB Collections and Recovery. Henka Group, 22 November 2026. |  |
| (C) Siam Commercial Bank and Henka Pte Ltd |  |
| Document | Recovery Workbench Service Catalog v1 |
| Version | 1 |
| Date | 22 November 2026 |
| Decision | D-RCV-60 microservice realignment |
| Tool | T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Status | Draft |
| Change log | 1, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Sheets | Services; Resources; REST operations; Events published; Events consumed; Workflows and schedules; Naming; Waves; Call types |
| Source of record | Recovery Workbench Architecture v5 Text Extract v1 (slides 13 to 20 and 41 to 44); Recovery Workbench Microservice Ownership Map v1; Recovery Workbench Temporal and Drools Design Text Extract v1 |

## Services

| Code | Service | Name | Wave | Service epic | Schema | Login | REST base | Kafka topic | Retry and DLT topics | Task queue | Java package | First API path | Owns (Arch v5 slide 41) | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P1 | rwb-source-data | Source data | 1 | RWB-SVC-P1 | rwb_source_data | rwb_source_data | /api/recovery/source-data/v1 | rwb.source-data.events.v1 | rwb.source-data.events.v1.retry.1m, rwb.source-data.events.v1.retry.10m, rwb.source-data.events.v1.retry.1h, rwb.source-data.events.v1.dlt | rwb-source-data | th.co.scb.ace.workbench.recovery.sourcedata | /customers/{id} | ACE view contract, extension tables, freshness, reconciliation | Draft |
| P2 | rwb-integration | Integration | 1 | RWB-SVC-P2 | rwb_integration | rwb_integration | /api/recovery/integration/v1 | rwb.integration.events.v1 | rwb.integration.events.v1.retry.1m, rwb.integration.events.v1.retry.10m, rwb.integration.events.v1.retry.1h, rwb.integration.events.v1.dlt | rwb-integration | th.co.scb.ace.workbench.recovery.integration | /interface-runs | interface config, file runs, outbound items, ACE integration paths | Draft |
| P3 | rwb-case | Case and workflow | 1 | RWB-SVC-P3 | rwb_case | rwb_case | /api/recovery/case/v1 | rwb.case.events.v1 | rwb.case.events.v1.retry.1m, rwb.case.events.v1.retry.10m, rwb.case.events.v1.retry.1h, rwb.case.events.v1.dlt | rwb-case | th.co.scb.ace.workbench.recovery.case | /cases/{id} | case, CMMN state, queues, tasks, allocation, timers | Draft |
| P4 | rwb-access | Access and authority | 1 | RWB-SVC-P4 | rwb_access | rwb_access | /api/recovery/access/v1 | rwb.access.events.v1 | rwb.access.events.v1.retry.1m, rwb.access.events.v1.retry.10m, rwb.access.events.v1.retry.1h, rwb.access.events.v1.dlt | rwb-access | th.co.scb.ace.workbench.recovery.access | /authorise | Recovery roles as data, scope, masking policy, DoA table, access log | Draft |
| P5 | rwb-document | Document | 1 | RWB-SVC-P5 | rwb_document | rwb_document | /api/recovery/document/v1 | rwb.document.events.v1 | rwb.document.events.v1.retry.1m, rwb.document.events.v1.retry.10m, rwb.document.events.v1.retry.1h, rwb.document.events.v1.dlt | rwb-document | th.co.scb.ace.workbench.recovery.document | /documents | metadata, custody, OCR text and fields, signatures, retention | Draft |
| P6 | rwb-comms | Communications | 1 | RWB-SVC-P6 | rwb_comms | rwb_comms | /api/recovery/comms/v1 | rwb.comms.events.v1 | rwb.comms.events.v1.retry.1m, rwb.comms.events.v1.retry.10m, rwb.comms.events.v1.retry.1h, rwb.comms.events.v1.dlt | rwb-comms | th.co.scb.ace.workbench.recovery.comms | /notices | notices, templates, merge fields, proof of delivery | Draft |
| P7 | rwb-decision | Decision and rules | 1 | RWB-SVC-P7 | rwb_decision | rwb_decision | /api/recovery/decision/v1 | rwb.decision.events.v1 | rwb.decision.events.v1.retry.1m, rwb.decision.events.v1.retry.10m, rwb.decision.events.v1.retry.1h, rwb.decision.events.v1.dlt | rwb-decision | th.co.scb.ace.workbench.recovery.decision | /decisions | approvals, central decision ledger, DMN model registry | Draft |
| P8 | rwb-payment | Payment | 2 | RWB-SVC-P8 | rwb_payment | rwb_payment | /api/recovery/payment/v1 | rwb.payment.events.v1 | rwb.payment.events.v1.retry.1m, rwb.payment.events.v1.retry.10m, rwb.payment.events.v1.retry.1h, rwb.payment.events.v1.dlt | rwb-payment | th.co.scb.ace.workbench.recovery.payment | /cases/{id}/payments | payment and proceeds matching, fees, bookings, posting files | Draft |
| P9 | rwb-reporting | Reporting | 1 | RWB-SVC-P9 | rwb_reporting | rwb_reporting | /api/recovery/reporting/v1 | rwb.reporting.events.v1 | rwb.reporting.events.v1.retry.1m, rwb.reporting.events.v1.retry.10m, rwb.reporting.events.v1.retry.1h, rwb.reporting.events.v1.dlt | rwb-reporting | th.co.scb.ace.workbench.recovery.reporting | /dashboards/{id} | measures, snapshots, steering dashboard, regulatory reports | Draft |
| P10 | rwb-agent | Agent | 1 | RWB-SVC-P10 | rwb_agent | rwb_agent | /api/recovery/agent/v1 | rwb.agent.events.v1 | rwb.agent.events.v1.retry.1m, rwb.agent.events.v1.retry.10m, rwb.agent.events.v1.retry.1h, rwb.agent.events.v1.dlt | rwb-agent | th.co.scb.ace.workbench.recovery.agent | /agent-runs/{id} | agent policies, prompts, runs, guardrails, evaluations | Draft |
| S1 | rwb-valuation | Valuation and route | 3 | RWB-SVC-S1 | rwb_valuation | rwb_valuation | /api/recovery/valuation/v1 | rwb.valuation.events.v1 | rwb.valuation.events.v1.retry.1m, rwb.valuation.events.v1.retry.10m, rwb.valuation.events.v1.retry.1h, rwb.valuation.events.v1.dlt | rwb-valuation | th.co.scb.ace.workbench.recovery.valuation | /cases/{id}/valuation | valuations, D6 route decision, route agent output | Draft |
| S2 | rwb-treatment | Treatment and offer | 2 | RWB-SVC-S2 | rwb_treatment | rwb_treatment | /api/recovery/treatment/v1 | rwb.treatment.events.v1 | rwb.treatment.events.v1.retry.1m, rwb.treatment.events.v1.retry.10m, rwb.treatment.events.v1.retry.1h, rwb.treatment.events.v1.dlt | rwb-treatment | th.co.scb.ace.workbench.recovery.treatment | /treatments | treatments, contracts, settlement and deed-in-lieu agreements, plan timers | Draft |
| S3 | rwb-guarantee | Guarantee | 3 | RWB-SVC-S3 | rwb_guarantee | rwb_guarantee | /api/recovery/guarantee/v1 | rwb.guarantee.events.v1 | rwb.guarantee.events.v1.retry.1m, rwb.guarantee.events.v1.retry.10m, rwb.guarantee.events.v1.retry.1h, rwb.guarantee.events.v1.dlt | rwb-guarantee | th.co.scb.ace.workbench.recovery.guarantee | /guarantee-claims | TCG and insurance claims, guarantor notices and pursuit | Draft |
| S4 | rwb-litigation | Litigation | 3 | RWB-SVC-S4 | rwb_litigation | rwb_litigation | /api/recovery/litigation/v1 | rwb.litigation.events.v1 | rwb.litigation.events.v1.retry.1m, rwb.litigation.events.v1.retry.10m, rwb.litigation.events.v1.retry.1h, rwb.litigation.events.v1.dlt | rwb-litigation | th.co.scb.ace.workbench.recovery.litigation | /legal-actions | legal actions, hearings, judgments, enforcement, LED auction ladder | Draft |
| S5 | rwb-asset | Asset | 2 | RWB-SVC-S5 | rwb_asset | rwb_asset | /api/recovery/asset/v1 | rwb.asset.events.v1 | rwb.asset.events.v1.retry.1m, rwb.asset.events.v1.retry.10m, rwb.asset.events.v1.retry.1h, rwb.asset.events.v1.dlt | rwb-asset | th.co.scb.ace.workbench.recovery.asset | /assets | assets taken on, holding, floor price, listings, auction rounds | Draft |
| S6 | rwb-debtsale | Debt sale | 3 | RWB-SVC-S6 | rwb_debtsale | rwb_debtsale | /api/recovery/debtsale/v1 | rwb.debtsale.events.v1 | rwb.debtsale.events.v1.retry.1m, rwb.debtsale.events.v1.retry.10m, rwb.debtsale.events.v1.retry.1h, rwb.debtsale.events.v1.dlt | rwb-debtsale | th.co.scb.ace.workbench.recovery.debtsale | /lots | lots, data room, buyer terms, bids, award, transfer | Draft |
| S7 | rwb-writeoff | Write-off | 4 | RWB-SVC-S7 | rwb_writeoff | rwb_writeoff | /api/recovery/writeoff/v1 | rwb.writeoff.events.v1 | rwb.writeoff.events.v1.retry.1m, rwb.writeoff.events.v1.retry.10m, rwb.writeoff.events.v1.retry.1h, rwb.writeoff.events.v1.dlt | rwb-writeoff | th.co.scb.ace.workbench.recovery.writeoff | /write-offs | eligibility, committee, posting, recovery after charge-off | Draft |
| S8 | rwb-deviation | Deviation | 2 | RWB-SVC-S8 | rwb_deviation | rwb_deviation | /api/recovery/deviation/v1 | rwb.deviation.events.v1 | rwb.deviation.events.v1.retry.1m, rwb.deviation.events.v1.retry.10m, rwb.deviation.events.v1.retry.1h, rwb.deviation.events.v1.dlt | rwb-deviation | th.co.scb.ace.workbench.recovery.deviation | /deviations | X1-X7 screening, pause, handling, return | Draft |
| S9 | rwb-partner | Partner | 4 | RWB-SVC-S9 | rwb_partner | rwb_partner | /api/recovery/partner/v1 | rwb.partner.events.v1 | rwb.partner.events.v1.retry.1m, rwb.partner.events.v1.retry.10m, rwb.partner.events.v1.retry.1h, rwb.partner.events.v1.dlt | rwb-partner | th.co.scb.ace.workbench.recovery.partner | /partners | panel, partner users, instructions, results, fees, scorecards | Draft |

## Resources

| Code | Service | Schema | Table | Ownership basis |
|---|---|---|---|---|
| P1 | rwb-source-data | rwb_source_data | account_ext | Ownership Map v1, Tables sheet |
| P1 | rwb-source-data | rwb_source_data | case_list_row | Ownership Map ruling case_list_row |
| P1 | rwb-source-data | rwb_source_data | contact_point_ext | Ownership Map v1, Tables sheet |
| P1 | rwb-source-data | rwb_source_data | data_contract | Ownership Map v1, Tables sheet |
| P1 | rwb-source-data | rwb_source_data | data_product | Ownership Map v1, Tables sheet |
| P1 | rwb-source-data | rwb_source_data | data_product_access | Ownership Map v1, Tables sheet |
| P1 | rwb-source-data | rwb_source_data | data_product_load | Ownership Map v1, Tables sheet |
| P1 | rwb-source-data | rwb_source_data | dp_guarantee_claim | Ownership Map ruling dp_guarantee_claim |
| P1 | rwb-source-data | rwb_source_data | dp_treatment | Ownership Map ruling dp_treatment |
| P1 | rwb-source-data | rwb_source_data | efs_ledger_outcome | Ownership Map ruling efs_ledger_outcome |
| P1 | rwb-source-data | rwb_source_data | interaction | Ownership Map ruling interaction |
| P1 | rwb-source-data | rwb_source_data | lake_copy_watermark | Ownership Map ruling lake_copy_watermark |
| P1 | rwb-source-data | rwb_source_data | party_ext | Ownership Map v1, Tables sheet |
| P1 | rwb-source-data | rwb_source_data | reconciliation_result | Ownership Map v1, Tables sheet |
| P1 | rwb-source-data | rwb_source_data | sys_field_version | Ownership Map v1, Tables sheet |
| P1 | rwb-source-data | rwb_source_data | sys_fields | Ownership Map v1, Tables sheet |
| P1 | rwb-source-data | rwb_source_data | sys_objects | Ownership Map v1, Tables sheet |
| P1 | rwb-source-data | rwb_source_data | valuation_ext | Ownership Map ruling valuation_ext |
| P2 | rwb-integration | rwb_integration | interface_config | Ownership Map v1, Tables sheet |
| P2 | rwb-integration | rwb_integration | job_catalog | Ownership Map ruling job_catalog |
| P2 | rwb-integration | rwb_integration | outbound_item | Ownership Map v1, Tables sheet |
| P3 | rwb-case | rwb_case | assignment | Ownership Map v1, Tables sheet |
| P3 | rwb-case | rwb_case | case_account | Ownership Map v1, Tables sheet |
| P3 | rwb-case | rwb_case | case_entry_exclusion | Ownership Map v1, Tables sheet |
| P3 | rwb-case | rwb_case | case_party | Ownership Map v1, Tables sheet |
| P3 | rwb-case | rwb_case | lov_value | Ownership Map ruling lov_value |
| P3 | rwb-case | rwb_case | parameter_catalog | Ownership Map v1, Tables sheet |
| P3 | rwb-case | rwb_case | parameter_value | Ownership Map v1, Tables sheet |
| P3 | rwb-case | rwb_case | queue | Ownership Map v1, Tables sheet |
| P3 | rwb-case | rwb_case | queue_measure | Ownership Map v1, Tables sheet |
| P3 | rwb-case | rwb_case | queue_member | Ownership Map v1, Tables sheet |
| P3 | rwb-case | rwb_case | recovery_case | Ownership Map v1, Tables sheet |
| P3 | rwb-case | rwb_case | reference_row | Ownership Map v1, Tables sheet |
| P3 | rwb-case | rwb_case | reference_version | Ownership Map v1, Tables sheet |
| P3 | rwb-case | rwb_case | task | Ownership Map v1, Tables sheet |
| P3 | rwb-case | rwb_case | timer | Ownership Map ruling timer |
| P4 | rwb-access | rwb_access | delegation_limit | Ownership Map ruling delegation_limit |
| P4 | rwb-access | rwb_access | masking_rule | Ownership Map v1, Tables sheet |
| P4 | rwb-access | rwb_access | permission | Ownership Map v1, Tables sheet |
| P4 | rwb-access | rwb_access | role | Ownership Map v1, Tables sheet |
| P4 | rwb-access | rwb_access | role_conflict | Ownership Map v1, Tables sheet |
| P5 | rwb-document | rwb_document | case_document_check | Ownership Map v1, Tables sheet |
| P5 | rwb-document | rwb_document | document | Ownership Map v1, Tables sheet |
| P5 | rwb-document | rwb_document | document_checklist_item | Ownership Map v1, Tables sheet |
| P5 | rwb-document | rwb_document | document_custody | Ownership Map v1, Tables sheet |
| P5 | rwb-document | rwb_document | document_field | Ownership Map v1, Tables sheet |
| P5 | rwb-document | rwb_document | document_hub_parameter | Ownership Map v1, Tables sheet |
| P5 | rwb-document | rwb_document | document_intake | Ownership Map v1, Tables sheet |
| P5 | rwb-document | rwb_document | document_text | Ownership Map v1, Tables sheet |
| P5 | rwb-document | rwb_document | document_type | Ownership Map v1, Tables sheet |
| P5 | rwb-document | rwb_document | retention_action | Ownership Map v1, Tables sheet |
| P5 | rwb-document | rwb_document | retention_rule | Ownership Map ruling retention_rule |
| P5 | rwb-document | rwb_document | signature_request | Ownership Map ruling signature_request |
| P6 | rwb-comms | rwb_comms | merge_field | Ownership Map v1, Tables sheet |
| P6 | rwb-comms | rwb_comms | notice | Ownership Map v1, Tables sheet |
| P6 | rwb-comms | rwb_comms | template | Ownership Map v1, Tables sheet |
| P7 | rwb-decision | rwb_decision | approval | Ownership Map v1, Tables sheet |
| P7 | rwb-decision | rwb_decision | decision_log_entry | Ownership Map v1, Tables sheet |
| P7 | rwb-decision | rwb_decision | rule_package | Ownership Map ruling rule registry |
| P7 | rwb-decision | rwb_decision | rule_package_version | Ownership Map ruling rule registry |
| P7 | rwb-decision | rwb_decision | rule_row | Ownership Map ruling rule registry |
| P7 | rwb-decision | rwb_decision | rule_test_case | Ownership Map ruling rule registry |
| P8 | rwb-payment | rwb_payment | proceeds | Ownership Map v1, Tables sheet |
| P9 | rwb-reporting | rwb_reporting | measure_definition | Ownership Map v1, Tables sheet |
| P9 | rwb-reporting | rwb_reporting | measure_publish | Ownership Map v1, Tables sheet |
| P9 | rwb-reporting | rwb_reporting | measure_snapshot | Ownership Map v1, Tables sheet |
| P10 | rwb-agent | rwb_agent | agent_alert | Ownership Map v1, Tables sheet |
| P10 | rwb-agent | rwb_agent | agent_evaluation | Ownership Map v1, Tables sheet |
| P10 | rwb-agent | rwb_agent | agent_evaluation_run | Ownership Map v1, Tables sheet |
| P10 | rwb-agent | rwb_agent | agent_feedback | Ownership Map v1, Tables sheet |
| P10 | rwb-agent | rwb_agent | agent_policy | Ownership Map v1, Tables sheet |
| P10 | rwb-agent | rwb_agent | agent_prompt | Ownership Map v1, Tables sheet |
| P10 | rwb-agent | rwb_agent | agent_run | Ownership Map v1, Tables sheet |
| P10 | rwb-agent | rwb_agent | agent_sample | Ownership Map v1, Tables sheet |
| S2 | rwb-treatment | rwb_treatment | treatment | Ownership Map v1, Tables sheet |
| S3 | rwb-guarantee | rwb_guarantee | guarantee_claim | Ownership Map v1, Tables sheet |
| S4 | rwb-litigation | rwb_litigation | hearing | Ownership Map v1, Tables sheet |
| S4 | rwb-litigation | rwb_litigation | legal_action | Ownership Map v1, Tables sheet |
| S5 | rwb-asset | rwb_asset | asset_sale | Ownership Map v1, Tables sheet |
| S5 | rwb-asset | rwb_asset | listing | Ownership Map v1, Tables sheet |
| S6 | rwb-debtsale | rwb_debtsale | debt_sale_account | Ownership Map v1, Tables sheet |
| S6 | rwb-debtsale | rwb_debtsale | debt_sale_lot | Ownership Map v1, Tables sheet |
| S7 | rwb-writeoff | rwb_writeoff | write_off | Ownership Map v1, Tables sheet |
| S8 | rwb-deviation | rwb_deviation | deviation | Ownership Map v1, Tables sheet |
| S9 | rwb-partner | rwb_partner | partner | Ownership Map v1, Tables sheet |
| S9 | rwb-partner | rwb_partner | partner_instruction | Ownership Map v1, Tables sheet |
| S9 | rwb-partner | rwb_partner | partner_user | Ownership Map ruling partner_user |
| S1 | rwb-valuation | rwb_valuation | Not specified in the source documents (CG-B-ARCH-SVC-1; ASM-B-ARCH-SVC-1) | Architecture v5 slide 41 names valuations, the D6 route decision and the route agent output; the Ownership Map v1 has no row and the Physical Schema v6 has no table |
| P8 | rwb-payment | rwb_payment | Not specified in the source documents (CG-B-ARCH-SVC-2; ASM-B-ARCH-SVC-2) | Architecture v5 slide 41 names fees, bookings and posting files; TSD P8 v2 names payment_match_rule; neither source has a row in the Ownership Map v1 |
| PLT | platform library | every rwb_* schema | feature_flag | Ownership Map ruling feature flags |
| PLT | platform library | every rwb_* schema | feature_flag_change | Ownership Map ruling feature flags |
| PLT | platform library | every rwb_* schema | idempotency_key | Ownership Map ruling library tables |
| PLT | platform library | every rwb_* schema | outbox_event | Ownership Map ruling library tables |
| PLT | platform library | every rwb_* schema | outbox_delivery | Ownership Map ruling library tables |
| PLT | platform library | every rwb_* schema | processed_event | Ownership Map ruling library tables |

## REST operations

Operations provided by each service, as named in Architecture v5 slides 14 to 20, with the per-service base of Template and Rules §R4. The paths in API Specification v4 are the monolith paths; the per-service operation list is rewritten in API Specification v5 (CG-B-ARCH-SVC-10).

| Code | Service | Method | Path (Arch v5) | Full path | Source |
|---|---|---|---|---|---|
| P1 | rwb-source-data | GET | /customers/{id} | /api/recovery/source-data/v1/customers/{id} | Architecture v5 slides 14 to 20 |
| P1 | rwb-source-data | GET | /accounts/{id} | /api/recovery/source-data/v1/accounts/{id} | Architecture v5 slides 14 to 20 |
| P1 | rwb-source-data | GET | /collateral/{id} | /api/recovery/source-data/v1/collateral/{id} | Architecture v5 slides 14 to 20 |
| P1 | rwb-source-data | GET | /payments?accountId= | /api/recovery/source-data/v1/payments?accountId= | Architecture v5 slides 14 to 20 |
| P1 | rwb-source-data | GET | /freshness | /api/recovery/source-data/v1/freshness | Architecture v5 slides 14 to 20 |
| P1 | rwb-source-data | POST | /business-days/{date}/ready | /api/recovery/source-data/v1/business-days/{date}/ready | Architecture v5 slides 14 to 20 |
| P2 | rwb-integration | GET | /interface-runs | /api/recovery/integration/v1/interface-runs | Architecture v5 slides 14 to 20 |
| P2 | rwb-integration | POST | /interface-runs/{id}/retry | /api/recovery/integration/v1/interface-runs/{id}/retry | Architecture v5 slides 14 to 20 |
| P3 | rwb-case | GET | /cases/{id} | /api/recovery/case/v1/cases/{id} | Architecture v5 slides 14 to 20 |
| P3 | rwb-case | GET | /cases?queue= | /api/recovery/case/v1/cases?queue= | Architecture v5 slides 14 to 20 |
| P3 | rwb-case | POST | /cases/{id}/actions | /api/recovery/case/v1/cases/{id}/actions | Architecture v5 slides 14 to 20 |
| P3 | rwb-case | GET | /tasks | /api/recovery/case/v1/tasks | Architecture v5 slides 14 to 20 |
| P3 | rwb-case | POST | /tasks/{id}/complete | /api/recovery/case/v1/tasks/{id}/complete | Architecture v5 slides 14 to 20 |
| P3 | rwb-case | GET | /case-summary/{id} (for the ACE shared case view) | /api/recovery/case/v1/case-summary/{id} | Architecture v5 slides 14 to 20 |
| P4 | rwb-access | POST | /authorise (role, scope, DoA) | /api/recovery/access/v1/authorise | Architecture v5 slides 14 to 20 |
| P4 | rwb-access | GET | /me/permissions | /api/recovery/access/v1/me/permissions | Architecture v5 slides 14 to 20 |
| P4 | rwb-access | GET | /doa-limits | /api/recovery/access/v1/doa-limits | Architecture v5 slides 14 to 20 |
| P4 | rwb-access | GET | /masking-policies | /api/recovery/access/v1/masking-policies | Architecture v5 slides 14 to 20 |
| P5 | rwb-document | POST | /documents (returns upload link) | /api/recovery/document/v1/documents | Architecture v5 slides 14 to 20 |
| P5 | rwb-document | GET | /documents/{id} | /api/recovery/document/v1/documents/{id} | Architecture v5 slides 14 to 20 |
| P5 | rwb-document | GET | /cases/{id}/documents | /api/recovery/document/v1/cases/{id}/documents | Architecture v5 slides 14 to 20 |
| P5 | rwb-document | POST | /documents/generate | /api/recovery/document/v1/documents/generate | Architecture v5 slides 14 to 20 |
| P6 | rwb-comms | POST | /notices (request) | /api/recovery/comms/v1/notices | Architecture v5 slides 14 to 20 |
| P6 | rwb-comms | GET | /cases/{id}/notices | /api/recovery/comms/v1/cases/{id}/notices | Architecture v5 slides 14 to 20 |
| P7 | rwb-decision | GET | /decisions?caseId= | /api/recovery/decision/v1/decisions?caseId= | Architecture v5 slides 14 to 20 |
| P7 | rwb-decision | POST | /approvals/{id}/decide | /api/recovery/decision/v1/approvals/{id}/decide | Architecture v5 slides 14 to 20 |
| P7 | rwb-decision | POST | /rule-models | /api/recovery/decision/v1/rule-models | Architecture v5 slides 14 to 20 |
| P7 | rwb-decision | GET | /rule-models/{n}/{v} | /api/recovery/decision/v1/rule-models/{n}/{v} | Architecture v5 slides 14 to 20 |
| P8 | rwb-payment | GET | /cases/{id}/payments | /api/recovery/payment/v1/cases/{id}/payments | Architecture v5 slides 14 to 20 |
| P8 | rwb-payment | POST | /proceeds/{id}/allocate (manual) | /api/recovery/payment/v1/proceeds/{id}/allocate | Architecture v5 slides 14 to 20 |
| P9 | rwb-reporting | GET | /dashboards/{id} | /api/recovery/reporting/v1/dashboards/{id} | Architecture v5 slides 14 to 20 |
| P9 | rwb-reporting | GET | /reports/{id} | /api/recovery/reporting/v1/reports/{id} | Architecture v5 slides 14 to 20 |
| P9 | rwb-reporting | POST | /reports/{id}/run (Airflow) | /api/recovery/reporting/v1/reports/{id}/run | Architecture v5 slides 14 to 20 |
| P10 | rwb-agent | GET | /agent-runs/{id} | /api/recovery/agent/v1/agent-runs/{id} | Architecture v5 slides 14 to 20 |
| P10 | rwb-agent | GET | /agent-policies (admin) | /api/recovery/agent/v1/agent-policies | Architecture v5 slides 14 to 20 |
| P10 | rwb-agent | POST | /agent-policies (admin) | /api/recovery/agent/v1/agent-policies | Architecture v5 slides 14 to 20 |
| S1 | rwb-valuation | GET | /cases/{id}/valuation | /api/recovery/valuation/v1/cases/{id}/valuation | Architecture v5 slides 14 to 20 |
| S1 | rwb-valuation | POST | /cases/{id}/route-proposals | /api/recovery/valuation/v1/cases/{id}/route-proposals | Architecture v5 slides 14 to 20 |
| S2 | rwb-treatment | GET | /treatments | /api/recovery/treatment/v1/treatments | Architecture v5 slides 14 to 20 |
| S2 | rwb-treatment | POST | /treatments | /api/recovery/treatment/v1/treatments | Architecture v5 slides 14 to 20 |
| S2 | rwb-treatment | POST | /treatments/{id}/offer | /api/recovery/treatment/v1/treatments/{id}/offer | Architecture v5 slides 14 to 20 |
| S3 | rwb-guarantee | GET | /guarantee-claims | /api/recovery/guarantee/v1/guarantee-claims | Architecture v5 slides 14 to 20 |
| S3 | rwb-guarantee | POST | /guarantee-claims | /api/recovery/guarantee/v1/guarantee-claims | Architecture v5 slides 14 to 20 |
| S4 | rwb-litigation | GET | /legal-actions | /api/recovery/litigation/v1/legal-actions | Architecture v5 slides 14 to 20 |
| S4 | rwb-litigation | POST | /legal-actions | /api/recovery/litigation/v1/legal-actions | Architecture v5 slides 14 to 20 |
| S4 | rwb-litigation | GET | /hearings | /api/recovery/litigation/v1/hearings | Architecture v5 slides 14 to 20 |
| S4 | rwb-litigation | POST | /hearings | /api/recovery/litigation/v1/hearings | Architecture v5 slides 14 to 20 |
| S5 | rwb-asset | GET | /assets | /api/recovery/asset/v1/assets | Architecture v5 slides 14 to 20 |
| S5 | rwb-asset | POST | /assets | /api/recovery/asset/v1/assets | Architecture v5 slides 14 to 20 |
| S5 | rwb-asset | GET | /listings | /api/recovery/asset/v1/listings | Architecture v5 slides 14 to 20 |
| S5 | rwb-asset | POST | /listings | /api/recovery/asset/v1/listings | Architecture v5 slides 14 to 20 |
| S5 | rwb-asset | POST | /auction-rounds | /api/recovery/asset/v1/auction-rounds | Architecture v5 slides 14 to 20 |
| S6 | rwb-debtsale | GET | /lots | /api/recovery/debtsale/v1/lots | Architecture v5 slides 14 to 20 |
| S6 | rwb-debtsale | POST | /lots | /api/recovery/debtsale/v1/lots | Architecture v5 slides 14 to 20 |
| S6 | rwb-debtsale | POST | /lots/{id}/bids | /api/recovery/debtsale/v1/lots/{id}/bids | Architecture v5 slides 14 to 20 |
| S6 | rwb-debtsale | POST | /lots/{id}/award | /api/recovery/debtsale/v1/lots/{id}/award | Architecture v5 slides 14 to 20 |
| S7 | rwb-writeoff | GET | /write-offs | /api/recovery/writeoff/v1/write-offs | Architecture v5 slides 14 to 20 |
| S7 | rwb-writeoff | POST | /write-offs | /api/recovery/writeoff/v1/write-offs | Architecture v5 slides 14 to 20 |
| S7 | rwb-writeoff | POST | /write-offs/{id}/submit | /api/recovery/writeoff/v1/write-offs/{id}/submit | Architecture v5 slides 14 to 20 |
| S8 | rwb-deviation | GET | /deviations | /api/recovery/deviation/v1/deviations | Architecture v5 slides 14 to 20 |
| S8 | rwb-deviation | POST | /deviations | /api/recovery/deviation/v1/deviations | Architecture v5 slides 14 to 20 |
| S8 | rwb-deviation | POST | /deviations/{id}/clear | /api/recovery/deviation/v1/deviations/{id}/clear | Architecture v5 slides 14 to 20 |
| S9 | rwb-partner | GET | /partners (staff) | /api/recovery/partner/v1/partners | Architecture v5 slides 14 to 20 |
| S9 | rwb-partner | POST | /partners (staff) | /api/recovery/partner/v1/partners | Architecture v5 slides 14 to 20 |
| S9 | rwb-partner | GET | /instructions | /api/recovery/partner/v1/instructions | Architecture v5 slides 14 to 20 |
| S9 | rwb-partner | POST | /instructions | /api/recovery/partner/v1/instructions | Architecture v5 slides 14 to 20 |
| S9 | rwb-partner | /partner/v1/* | (partner portal, FAPI 2.0, through the partner gateway) | (partner portal, FAPI 2.0, through the partner gateway) | Architecture v5 slides 14 to 20 |

## Events published

| Code | Service | Event | Topic | Consumers | Producer (catalogue) |
|---|---|---|---|---|---|
| P1 | rwb-source-data | AceDataReady | rwb.source-data.events.v1 | rwb-case, rwb-payment, rwb-deviation, rwb-writeoff | rwb-source-data |
| P1 | rwb-source-data | AceDataLate | rwb.source-data.events.v1 | alerts, gateway-bff banner | rwb-source-data |
| P1 | rwb-source-data | DecisionRecorded | rwb.decision-record.v1 | rwb-decision, rwb-reporting | all 19 |
| P2 | rwb-integration | FileDelivered | rwb.integration.events.v1 | requesting service | rwb-integration |
| P2 | rwb-integration | FileFailed | rwb.integration.events.v1 | requesting service | rwb-integration |
| P2 | rwb-integration | DecisionRecorded | rwb.decision-record.v1 | rwb-decision, rwb-reporting | all 19 |
| P3 | rwb-case | CaseCreated | rwb.case.events.v1 | rwb-agent, rwb-deviation, rwb-reporting | rwb-case |
| P3 | rwb-case | CaseAllocated | rwb.case.events.v1 | rwb-reporting | rwb-case |
| P3 | rwb-case | CaseAllocationFailed | rwb.case.events.v1 | rwb-case | rwb-case |
| P3 | rwb-case | CaseTransferred | rwb.case.events.v1 | rwb-reporting | rwb-case |
| P3 | rwb-case | CaseStateChanged | rwb.case.events.v1 | rwb-comms, rwb-reporting | rwb-case |
| P3 | rwb-case | TimerBreached | rwb.case.events.v1 | gateway-bff (inbox) | rwb-case |
| P3 | rwb-case | DecisionRecorded | rwb.decision-record.v1 | rwb-decision, rwb-reporting | all 19 |
| P4 | rwb-access | AccessPolicyChanged | rwb.access.events.v1 | all (cache refresh) | rwb-access |
| P4 | rwb-access | DoaLimitChanged | rwb.access.events.v1 | all (cache refresh) | rwb-access |
| P4 | rwb-access | DecisionRecorded | rwb.decision-record.v1 | rwb-decision, rwb-reporting | all 19 |
| P5 | rwb-document | DocumentStored | rwb.document.events.v1 | rwb-agent, rwb-case | rwb-document |
| P5 | rwb-document | DocumentFieldsExtracted | rwb.document.events.v1 | rwb-case | rwb-document |
| P5 | rwb-document | DecisionRecorded | rwb.decision-record.v1 | rwb-decision, rwb-reporting | all 19 |
| P6 | rwb-comms | NoticeGenerated | rwb.comms.events.v1 | rwb-decision | rwb-comms |
| P6 | rwb-comms | NoticeDispatched | rwb.comms.events.v1 | rwb-reporting | rwb-comms |
| P6 | rwb-comms | NoticeDelivered | rwb.comms.events.v1 | rwb-litigation, rwb-guarantee, rwb-case | rwb-comms |
| P6 | rwb-comms | DecisionRecorded | rwb.decision-record.v1 | rwb-decision, rwb-reporting | all 19 |
| P7 | rwb-decision | ApprovalRequested | rwb.decision.events.v1 | gateway-bff (inbox) | rwb-decision |
| P7 | rwb-decision | ApprovalDecided | rwb.decision.events.v1 | Not specified in the source documents (CG-B-ARCH-SVC-6; ASM-B-ARCH-SVC-6) | rwb-decision |
| P7 | rwb-decision | RulePackageInForce | rwb.decision.events.v1 | rwb-case, rwb-valuation, rwb-treatment, rwb-payment | rwb-decision |
| P7 | rwb-decision | DecisionRecorded | rwb.decision-record.v1 | rwb-decision, rwb-reporting | all 19 |
| P8 | rwb-payment | TreatmentBooked | rwb.payment.events.v1 | rwb-case, rwb-treatment | rwb-payment |
| P8 | rwb-payment | PaymentMissed | rwb.payment.events.v1 | rwb-case, rwb-treatment, rwb-comms | rwb-payment |
| P8 | rwb-payment | ProceedsMatched | rwb.payment.events.v1 | rwb-case, rwb-asset, rwb-debtsale, rwb-writeoff, rwb-guarantee | rwb-payment |
| P8 | rwb-payment | DecisionRecorded | rwb.decision-record.v1 | rwb-decision, rwb-reporting | all 19 |
| P9 | rwb-reporting | ReportPublished | rwb.reporting.events.v1 | Not specified in the source documents (CG-B-ARCH-SVC-6; ASM-B-ARCH-SVC-6) | rwb-reporting |
| P9 | rwb-reporting | DecisionRecorded | rwb.decision-record.v1 | rwb-decision, rwb-reporting | all 19 |
| P10 | rwb-agent | AgentRunCompleted | rwb.agent.events.v1 | rwb-decision, rwb-document, rwb-deviation | rwb-agent |
| P10 | rwb-agent | DecisionRecorded | rwb.decision-record.v1 | rwb-decision, rwb-reporting | all 19 |
| S1 | rwb-valuation | RouteDecided | rwb.valuation.events.v1 | rwb-case | rwb-valuation |
| S1 | rwb-valuation | DecisionRecorded | rwb.decision-record.v1 | rwb-decision, rwb-reporting | all 19 |
| S2 | rwb-treatment | TreatmentApproved | rwb.treatment.events.v1 | rwb-comms, rwb-payment | rwb-treatment |
| S2 | rwb-treatment | TreatmentClosed | rwb.treatment.events.v1 | rwb-case, rwb-reporting | rwb-treatment |
| S2 | rwb-treatment | DecisionRecorded | rwb.decision-record.v1 | rwb-decision, rwb-reporting | all 19 |
| S3 | rwb-guarantee | GuaranteeClaimFiled | rwb.guarantee.events.v1 | rwb-case, rwb-reporting | rwb-guarantee |
| S3 | rwb-guarantee | GuaranteeClaimSettled | rwb.guarantee.events.v1 | rwb-case, rwb-reporting | rwb-guarantee |
| S3 | rwb-guarantee | DecisionRecorded | rwb.decision-record.v1 | rwb-decision, rwb-reporting | all 19 |
| S4 | rwb-litigation | LawsuitFiled | rwb.litigation.events.v1 | Not specified in the source documents (CG-B-ARCH-SVC-6; ASM-B-ARCH-SVC-6) | rwb-litigation |
| S4 | rwb-litigation | JudgmentRecorded | rwb.litigation.events.v1 | rwb-asset, rwb-case | rwb-litigation |
| S4 | rwb-litigation | AuctionResult | rwb.litigation.events.v1 | rwb-asset, rwb-case | rwb-litigation |
| S4 | rwb-litigation | DecisionRecorded | rwb.decision-record.v1 | rwb-decision, rwb-reporting | all 19 |
| S5 | rwb-asset | AssetTakenOn | rwb.asset.events.v1 | rwb-case, rwb-payment | rwb-asset |
| S5 | rwb-asset | AssetSold | rwb.asset.events.v1 | rwb-payment, rwb-case | rwb-asset |
| S5 | rwb-asset | DecisionRecorded | rwb.decision-record.v1 | rwb-decision, rwb-reporting | all 19 |
| S6 | rwb-debtsale | LotAwarded | rwb.debtsale.events.v1 | rwb-case, rwb-payment | rwb-debtsale |
| S6 | rwb-debtsale | AccountsTransferred | rwb.debtsale.events.v1 | rwb-case, rwb-reporting | rwb-debtsale |
| S6 | rwb-debtsale | DecisionRecorded | rwb.decision-record.v1 | rwb-decision, rwb-reporting | all 19 |
| S7 | rwb-writeoff | WriteOffApproved | rwb.writeoff.events.v1 | rwb-case, rwb-payment, rwb-reporting | rwb-writeoff |
| S7 | rwb-writeoff | DecisionRecorded | rwb.decision-record.v1 | rwb-decision, rwb-reporting | all 19 |
| S8 | rwb-deviation | DeviationRaised | rwb.deviation.events.v1 | rwb-case, rwb-comms, rwb-treatment | rwb-deviation |
| S8 | rwb-deviation | DeviationCleared | rwb.deviation.events.v1 | rwb-case, rwb-comms | rwb-deviation |
| S8 | rwb-deviation | DecisionRecorded | rwb.decision-record.v1 | rwb-decision, rwb-reporting | all 19 |
| S9 | rwb-partner | InstructionIssued | rwb.partner.events.v1 | partner portal | rwb-partner |
| S9 | rwb-partner | PartnerResultSubmitted | rwb.partner.events.v1 | rwb-litigation, rwb-asset, rwb-case | rwb-partner |
| S9 | rwb-partner | DecisionRecorded | rwb.decision-record.v1 | rwb-decision, rwb-reporting | all 19 |

## Events consumed

| Code | Service | Event | Producer topic | Producer |
|---|---|---|---|---|
| P3 | rwb-case | CaseAllocationFailed | rwb.case.events.v1 | rwb-case |
| P3 | rwb-case | DeviationRaised | rwb.deviation.events.v1 | rwb-deviation |
| P3 | rwb-case | DeviationCleared | rwb.deviation.events.v1 | rwb-deviation |
| P3 | rwb-case | TreatmentBooked | rwb.payment.events.v1 | rwb-payment |
| P3 | rwb-case | PaymentMissed | rwb.payment.events.v1 | rwb-payment |
| P3 | rwb-case | NoticeDelivered | rwb.comms.events.v1 | rwb-comms |
| P3 | rwb-case | PartnerResultSubmitted | rwb.partner.events.v1 | rwb-partner |
| P3 | rwb-case | DocumentStored | rwb.document.events.v1 | rwb-document |
| P3 | rwb-case | DocumentFieldsExtracted | rwb.document.events.v1 | rwb-document |
| P3 | rwb-case | RouteDecided | rwb.valuation.events.v1 | rwb-valuation |
| P3 | rwb-case | AssetTakenOn | rwb.asset.events.v1 | rwb-asset |
| P3 | rwb-case | AssetSold | rwb.asset.events.v1 | rwb-asset |
| P3 | rwb-case | LotAwarded | rwb.debtsale.events.v1 | rwb-debtsale |
| P3 | rwb-case | WriteOffApproved | rwb.writeoff.events.v1 | rwb-writeoff |
| P3 | rwb-case | ProceedsMatched | rwb.payment.events.v1 | rwb-payment |
| P3 | rwb-case | JudgmentRecorded | rwb.litigation.events.v1 | rwb-litigation |
| P3 | rwb-case | AuctionResult | rwb.litigation.events.v1 | rwb-litigation |
| P3 | rwb-case | AccountsTransferred | rwb.debtsale.events.v1 | rwb-debtsale |
| P3 | rwb-case | TreatmentClosed | rwb.treatment.events.v1 | rwb-treatment |
| P3 | rwb-case | GuaranteeClaimFiled | rwb.guarantee.events.v1 | rwb-guarantee |
| P3 | rwb-case | GuaranteeClaimSettled | rwb.guarantee.events.v1 | rwb-guarantee |
| P3 | rwb-case | AceDataReady | rwb.source-data.events.v1 | rwb-source-data |
| P3 | rwb-case | RulePackageInForce | rwb.decision.events.v1 | rwb-decision |
| P5 | rwb-document | AgentRunCompleted | rwb.agent.events.v1 | rwb-agent |
| P6 | rwb-comms | DeviationRaised | rwb.deviation.events.v1 | rwb-deviation |
| P6 | rwb-comms | DeviationCleared | rwb.deviation.events.v1 | rwb-deviation |
| P6 | rwb-comms | TreatmentApproved | rwb.treatment.events.v1 | rwb-treatment |
| P6 | rwb-comms | PaymentMissed | rwb.payment.events.v1 | rwb-payment |
| P6 | rwb-comms | CaseStateChanged | rwb.case.events.v1 | rwb-case |
| P7 | rwb-decision | DecisionRecorded | rwb.decision-record.v1 | all 19 |
| P7 | rwb-decision | NoticeGenerated | rwb.comms.events.v1 | rwb-comms |
| P7 | rwb-decision | AgentRunCompleted | rwb.agent.events.v1 | rwb-agent |
| P8 | rwb-payment | AceDataReady | rwb.source-data.events.v1 | rwb-source-data |
| P8 | rwb-payment | TreatmentApproved | rwb.treatment.events.v1 | rwb-treatment |
| P8 | rwb-payment | LotAwarded | rwb.debtsale.events.v1 | rwb-debtsale |
| P8 | rwb-payment | AssetSold | rwb.asset.events.v1 | rwb-asset |
| P8 | rwb-payment | WriteOffApproved | rwb.writeoff.events.v1 | rwb-writeoff |
| P9 | rwb-reporting | All business events (projections) | all business-event topics | all 19 |
| P9 | rwb-reporting | DecisionRecorded | rwb.decision-record.v1 | all 19 |
| P10 | rwb-agent | DocumentStored | rwb.document.events.v1 | rwb-document |
| P10 | rwb-agent | CaseCreated | rwb.case.events.v1 | rwb-case |
| S1 | rwb-valuation | RulePackageInForce | rwb.decision.events.v1 | rwb-decision |
| S2 | rwb-treatment | TreatmentBooked | rwb.payment.events.v1 | rwb-payment |
| S2 | rwb-treatment | PaymentMissed | rwb.payment.events.v1 | rwb-payment |
| S2 | rwb-treatment | DeviationRaised | rwb.deviation.events.v1 | rwb-deviation |
| S3 | rwb-guarantee | NoticeDelivered | rwb.comms.events.v1 | rwb-comms |
| S3 | rwb-guarantee | ProceedsMatched | rwb.payment.events.v1 | rwb-payment |
| S4 | rwb-litigation | NoticeDelivered | rwb.comms.events.v1 | rwb-comms |
| S4 | rwb-litigation | PartnerResultSubmitted | rwb.partner.events.v1 | rwb-partner |
| S5 | rwb-asset | JudgmentRecorded | rwb.litigation.events.v1 | rwb-litigation |
| S5 | rwb-asset | AuctionResult | rwb.litigation.events.v1 | rwb-litigation |
| S5 | rwb-asset | ProceedsMatched | rwb.payment.events.v1 | rwb-payment |
| S6 | rwb-debtsale | ProceedsMatched | rwb.payment.events.v1 | rwb-payment |
| S7 | rwb-writeoff | AceDataReady | rwb.source-data.events.v1 | rwb-source-data |
| S7 | rwb-writeoff | ProceedsMatched | rwb.payment.events.v1 | rwb-payment |
| S8 | rwb-deviation | CaseCreated | rwb.case.events.v1 | rwb-case |
| S8 | rwb-deviation | AceDataReady | rwb.source-data.events.v1 | rwb-source-data |
| S8 | rwb-deviation | AgentRunCompleted | rwb.agent.events.v1 | rwb-agent |

## Workflows and schedules

| Code | Service | Type | Item | Task queue | Source |
|---|---|---|---|---|---|
| P1 | rwb-source-data | Workflow | AceIngestCheck, reconciliation (JOB-04) | rwb-source-data | Architecture v5 slides 14 to 20 and 44 |
| P1 | rwb-source-data | Activity | listEligibleAccounts, snapshot(page) | rwb-source-data | Architecture v5 slides 14 to 20 and 44 |
| P1 | rwb-source-data | Trigger | Started by AceDataReady (JOB-04) | rwb-source-data | Architecture v5 slides 14 to 20 and 44 |
| P2 | rwb-integration | Activity | deliverFile(manifest), receiveFile | rwb-integration | Architecture v5 slides 14 to 20 and 44 |
| P2 | rwb-integration | Window | Airflow file window: WIN file 16:00, buyer files per lot | rwb-integration | Architecture v5 slides 14 to 20 and 44 |
| P3 | rwb-case | Workflow | CaseWorkflow (parent, one per case) | rwb-case | Architecture v5 slides 14 to 20 and 44 |
| P3 | rwb-case | Workflow | DailyCaseRun (Schedule and AceDataReady) | rwb-case | Architecture v5 slides 14 to 20 and 44 |
| P3 | rwb-case | Activity | allocate, transfer, rebalance | rwb-case | Architecture v5 slides 14 to 20 and 44 |
| P3 | rwb-case | Schedule | Rebalancing 06:30 (JOB-06) | rwb-case | Architecture v5 slides 14 to 20 and 44 |
| P3 | rwb-case | Outward call | Source data: listEligibleAccounts(businessDate) | rwb-case | Architecture v5 slides 14 to 20 and 44 |
| P3 | rwb-case | Outward call | Valuation: RouteDecisionWorkflow child | rwb-case | Architecture v5 slides 14 to 20 and 44 |
| P3 | rwb-case | Outward call | Treatment, guarantee, litigation, asset, debt sale and write-off stage workflows | rwb-case | Architecture v5 slides 14 to 20 and 44 |
| P3 | rwb-case | Outward call | Deviation: DeviationWorkflow child | rwb-case | Architecture v5 slides 14 to 20 and 44 |
| P3 | rwb-case | Outward call | Decision: ApprovalWorkflow child | rwb-case | Architecture v5 slides 14 to 20 and 44 |
| P4 | rwb-access | Schedule | Access review list (six-monthly, JOB-18) | rwb-access | Architecture v5 slides 14 to 20 and 44 |
| P5 | rwb-document | Workflow | DocumentIntakeWorkflow: OCR, classify, extract (JOB-12) | rwb-document | Architecture v5 slides 14 to 20 and 44 |
| P5 | rwb-document | Activity | generate, seal | rwb-document | Architecture v5 slides 14 to 20 and 44 |
| P5 | rwb-document | Schedule | Retention monthly, first Sunday (JOB-17) | rwb-document | Architecture v5 slides 14 to 20 and 44 |
| P5 | rwb-document | Outward call | Agent: classify and extract child | rwb-document | Architecture v5 slides 14 to 20 and 44 |
| P6 | rwb-comms | Workflow | NoticeDispatchWorkflow (kit template) | rwb-comms | Architecture v5 slides 14 to 20 and 44 |
| P6 | rwb-comms | Schedule | WIN notices 16:00 (JOB-10) | rwb-comms | Architecture v5 slides 14 to 20 and 44 |
| P6 | rwb-comms | Outward call | Document: generate letter | rwb-comms | Architecture v5 slides 14 to 20 and 44 |
| P6 | rwb-comms | Outward call | Decision: approval child | rwb-comms | Architecture v5 slides 14 to 20 and 44 |
| P6 | rwb-comms | Outward call | Integration: deliverFile (WIN letters) | rwb-comms | Architecture v5 slides 14 to 20 and 44 |
| P7 | rwb-decision | Workflow | ApprovalWorkflow (kit template) | rwb-decision | Architecture v5 slides 14 to 20 and 44 |
| P7 | rwb-decision | Schedule | Rule promote 00:01 (JOB-20); chain check 02:00 (JOB-14) | rwb-decision | Architecture v5 slides 14 to 20 and 44 |
| P7 | rwb-decision | Ingest | Continuous DecisionRecorded ingest from Kafka (JOB-13) | rwb-decision | Architecture v5 slides 14 to 20 and 44 |
| P8 | rwb-payment | Workflow | Event-started workflows from AceDataReady | rwb-payment | Architecture v5 slides 14 to 20 and 44 |
| P8 | rwb-payment | Activity | matchPayments (JOB-07), confirmBookings (JOB-08) | rwb-payment | Architecture v5 slides 14 to 20 and 44 |
| P8 | rwb-payment | Activity | postProceeds (saga step) | rwb-payment | Architecture v5 slides 14 to 20 and 44 |
| P8 | rwb-payment | Outward call | Source data: payments for the business date | rwb-payment | Architecture v5 slides 14 to 20 and 44 |
| P8 | rwb-payment | Outward call | Integration: deliverFile (posting file) | rwb-payment | Architecture v5 slides 14 to 20 and 44 |
| P9 | rwb-reporting | Activity | buildRegulatoryExtract | rwb-reporting | Architecture v5 slides 14 to 20 and 44 |
| P9 | rwb-reporting | Schedule | Measures 01:30 (JOB-15, Airflow trigger) | rwb-reporting | Architecture v5 slides 14 to 20 and 44 |
| P9 | rwb-reporting | Outward call | Source data: snapshot(page) for measures | rwb-reporting | Architecture v5 slides 14 to 20 and 44 |
| P9 | rwb-reporting | Outward call | Integration: deliverFile (regulatory extract) | rwb-reporting | Architecture v5 slides 14 to 20 and 44 |
| P10 | rwb-agent | Workflow | AgentRunWorkflow: 60 s, then the rule result | rwb-agent | Architecture v5 slides 14 to 20 and 44 |
| P10 | rwb-agent | Outward call | Tool gateway: Source data (case facts), Document (extracted fields), Enterprise AI endpoint | rwb-agent | Architecture v5 slides 14 to 20 and 44 |
| S1 | rwb-valuation | Workflow | RouteDecisionWorkflow (stage workflow, started by rwb-case) | rwb-valuation | Architecture v5 slides 14 to 20 and 44 |
| S1 | rwb-valuation | Outward call | Agent: route agent child | rwb-valuation | Architecture v5 slides 14 to 20 and 44 |
| S1 | rwb-valuation | Outward call | Decision: approval child | rwb-valuation | Architecture v5 slides 14 to 20 and 44 |
| S2 | rwb-treatment | Workflow | TreatmentWorkflow: settlement and deed-in-lieu sagas | rwb-treatment | Architecture v5 slides 14 to 20 and 44 |
| S2 | rwb-treatment | Outward call | Decision: approval child | rwb-treatment | Architecture v5 slides 14 to 20 and 44 |
| S2 | rwb-treatment | Outward call | Document: contract and e-sign | rwb-treatment | Architecture v5 slides 14 to 20 and 44 |
| S2 | rwb-treatment | Outward call | Payment: postProceeds | rwb-treatment | Architecture v5 slides 14 to 20 and 44 |
| S3 | rwb-guarantee | Workflow | GuaranteeClaimWorkflow | rwb-guarantee | Architecture v5 slides 14 to 20 and 44 |
| S3 | rwb-guarantee | Outward call | Comms: guarantor notice child | rwb-guarantee | Architecture v5 slides 14 to 20 and 44 |
| S3 | rwb-guarantee | Outward call | Decision: approval child | rwb-guarantee | Architecture v5 slides 14 to 20 and 44 |
| S4 | rwb-litigation | Workflow | LitigationWorkflow (years; continues-as-new) | rwb-litigation | Architecture v5 slides 14 to 20 and 44 |
| S4 | rwb-litigation | Outward call | Partner: issueInstruction (law firm) | rwb-litigation | Architecture v5 slides 14 to 20 and 44 |
| S4 | rwb-litigation | Outward call | Comms: demand notice child | rwb-litigation | Architecture v5 slides 14 to 20 and 44 |
| S4 | rwb-litigation | Outward call | Decision: approval child | rwb-litigation | Architecture v5 slides 14 to 20 and 44 |
| S5 | rwb-asset | Workflow | AssetDisposalWorkflow | rwb-asset | Architecture v5 slides 14 to 20 and 44 |
| S5 | rwb-asset | Schedule | Re-appraisal monthly (JOB-19) | rwb-asset | Architecture v5 slides 14 to 20 and 44 |
| S5 | rwb-asset | Outward call | Partner: issueInstruction (auction vendor) | rwb-asset | Architecture v5 slides 14 to 20 and 44 |
| S5 | rwb-asset | Outward call | Decision: approval child | rwb-asset | Architecture v5 slides 14 to 20 and 44 |
| S5 | rwb-asset | Outward call | Payment: postProceeds | rwb-asset | Architecture v5 slides 14 to 20 and 44 |
| S6 | rwb-debtsale | Workflow | DebtSaleWorkflow (saga, pivot = transfer) | rwb-debtsale | Architecture v5 slides 14 to 20 and 44 |
| S6 | rwb-debtsale | Outward call | Document: data room pack | rwb-debtsale | Architecture v5 slides 14 to 20 and 44 |
| S6 | rwb-debtsale | Outward call | Decision: approval child | rwb-debtsale | Architecture v5 slides 14 to 20 and 44 |
| S6 | rwb-debtsale | Outward call | Integration: deliverFile (buyer file) | rwb-debtsale | Architecture v5 slides 14 to 20 and 44 |
| S6 | rwb-debtsale | Outward call | Payment: postProceeds | rwb-debtsale | Architecture v5 slides 14 to 20 and 44 |
| S7 | rwb-writeoff | Workflow | WriteOffWorkflow | rwb-writeoff | Architecture v5 slides 14 to 20 and 44 |
| S7 | rwb-writeoff | Schedule | Scan, third working day (JOB-16) | rwb-writeoff | Architecture v5 slides 14 to 20 and 44 |
| S7 | rwb-writeoff | Outward call | Decision: committee approval child | rwb-writeoff | Architecture v5 slides 14 to 20 and 44 |
| S7 | rwb-writeoff | Outward call | Payment: postProceeds | rwb-writeoff | Architecture v5 slides 14 to 20 and 44 |
| S8 | rwb-deviation | Workflow | DeviationWorkflow (child of case) | rwb-deviation | Architecture v5 slides 14 to 20 and 44 |
| S8 | rwb-deviation | Outward call | Agent: screening agent run | rwb-deviation | Architecture v5 slides 14 to 20 and 44 |
| S9 | rwb-partner | Workflow | InstructionWorkflow: SLA timers | rwb-partner | Architecture v5 slides 14 to 20 and 44 |
| S9 | rwb-partner | Activity | issueInstruction, recordResult | rwb-partner | Architecture v5 slides 14 to 20 and 44 |
| S9 | rwb-partner | Outward call | Document: partner uploads (REST) | rwb-partner | Architecture v5 slides 14 to 20 and 44 |
| PLT | platform | Schedule | Stuck workflow scan every 5 minutes (JOB-21); platform smoke 06:00 (JOB-22), starts PlatformSmokeWorkflow | rwb-platform | Architecture v5 slide 44 |
| PLT | platform | Library | Outbox relay every minute (JOB-11) in every service; durable timers replace the 5-minute timer check (JOB-05, retired) | every rwb-<svc> | Architecture v5 slide 44; Ownership Map v1, Jobs sheet |

## Naming

| Element | Rule | Example |
|---|---|---|
| Service code | P1 to P10, S1 to S9 | P3 |
| Service name | rwb-<short> | rwb-case |
| Schema and login | rwb_<short with _> | rwb_case |
| REST base | /api/recovery/<short>/v1 | /api/recovery/case/v1 |
| Kafka topic | rwb.<short>.events.v1 | rwb.case.events.v1 |
| Retry and dead-letter topics | rwb.<short>.events.v1.retry.1m, .retry.10m, .retry.1h, .dlt | rwb.case.events.v1.dlt |
| Event names | rwb.<short>.<Event>.v1 | rwb.case.CaseCreated.v1 |
| Temporal task queue | rwb-<short> | rwb-case |
| Java package | th.co.scb.ace.workbench.recovery.<short without hyphen> | th.co.scb.ace.workbench.recovery.case |
| Service epic | RWB-SVC-<code> | RWB-SVC-P3 |

## Waves

| Wave | Services | Service epics | Gate |
|---|---|---|---|
| 0 | None (platform only) | RWB-PLT-TPL, RWB-PLT-LIB, RWB-PLT-WF, RWB-PLT-DB, RWB-PLT-EVT, RWB-PLT-EDGE, RWB-PLT-OBS | Template accepted; 19 logins created; topics exist |
| 1 | P1, P2, P3, P4, P5, P6, P7, P9, P10 | RWB-SVC-P1 to RWB-SVC-P7, RWB-SVC-P9, RWB-SVC-P10 | BOT approval before Wave 1 go-live, if required (FPG 19/2560 cl. 5.5) |
| 2 | P8, S2, S5, S8 | RWB-SVC-P8, RWB-SVC-S2, RWB-SVC-S5, RWB-SVC-S8 | Wave 1 in production |
| 3 | S1, S3, S4, S6 | RWB-SVC-S1, RWB-SVC-S3, RWB-SVC-S4, RWB-SVC-S6 | Wave 2 in production |
| 4 | S7, S9 | RWB-SVC-S7, RWB-SVC-S9 | Wave 3 in production |

## Call types

| Call type | Use when | Contract | Failure handling | Source |
|---|---|---|---|---|
| REST | A person waits for the answer | OpenAPI 3.1, /v1 in the path | 2 s timeout, one GET retry with jitter, circuit breaker and bulkhead, RFC 9457 problem details | Architecture v5 slides 10, 11 |
| Kafka event | A fact others may react to | AsyncAPI 3.0, CloudEvents 1.0 binary mode, JSON Schema BACKWARD | Outbox, inbox dedupe, retry 1 min, 10 min, 1 h then .dlt, replay tool | Architecture v5 slides 11, 22 |
| Temporal | A step in another service, or a long process | Typed activity and workflow interface in a contract jar | Typed failures, non-retryable list, saga undo | Architecture v5 slides 11, 23 to 26 |
| File | Bulk data, or a party outside the bank | Manifest: fileId, batchId, sha256, record count | FileFailed event, operator retry, checksum | Architecture v5 slide 11 |
| SQL view | Reading ACE data, rwb-source-data only | 30 recovery.v_ace_* views (ADR-010) | 5 s statement timeout | Architecture v5 slides 11, 29 |

