
A1 · Service catalogue: the 19 services

One row per service: module, what it owns, its schema, API, topic, task queue and wave

| Module | Service | Owns | Schema | First API path | Kafka topic | Task queue | Wave |
|---|---|---|---|---|---|---|---|
| P3 | rwb-case | case, CMMN state, queues, tasks, allocation, timers | rwb_case | /cases/{id} | rwb.case.events.v1 | rwb-case | 1 |
| P7 | rwb-decision | approvals, central decision ledger, DMN model registry | rwb_decision | /decisions | rwb.decision.events.v1 | rwb-decision | 1 |
| P4 | rwb-access | Recovery roles as data, scope, masking policy, DoA table, access log | rwb_access | /authorise | rwb.access.events.v1 | rwb-access | 1 |
| S8 | rwb-deviation | X1-X7 screening, pause, handling, return | rwb_deviation | /deviations | rwb.deviation.events.v1 | rwb-deviation | 2 |
| P1 | rwb-source-data | ACE view contract, extension tables, freshness, reconciliation | rwb_source_data | /customers/{id} | rwb.source-data.events.v1 | rwb-source-data | 1 |
| P9 | rwb-reporting | measures, snapshots, steering dashboard, regulatory reports | rwb_reporting | /dashboards/{id} | rwb.reporting.events.v1 | rwb-reporting | 1 |
| P10 | rwb-agent | agent policies, prompts, runs, guardrails, evaluations | rwb_agent | /agent-runs/{id} | rwb.agent.events.v1 | rwb-agent | 1 |
| P2 | rwb-integration | interface config, file runs, outbound items, ACE integration paths | rwb_integration | /interface-runs | rwb.integration.events.v1 | rwb-integration | 1 |
| P5 | rwb-document | metadata, custody, OCR text and fields, signatures, retention | rwb_document | /documents | rwb.document.events.v1 | rwb-document | 1 |
| P6 | rwb-comms | notices, templates, merge fields, proof of delivery | rwb_comms | /notices | rwb.comms.events.v1 | rwb-comms | 1 |
| P8 | rwb-payment | payment and proceeds matching, fees, bookings, posting files | rwb_payment | /cases/{id}/payments | rwb.payment.events.v1 | rwb-payment | 2 |
| S9 | rwb-partner | panel, partner users, instructions, results, fees, scorecards | rwb_partner | /partners | rwb.partner.events.v1 | rwb-partner | 4 |
| S1 | rwb-valuation | valuations, D6 route decision, route agent output | rwb_valuation | /cases/{id}/valuation | rwb.valuation.events.v1 | rwb-valuation | 3 |
| S2 | rwb-treatment | treatments, contracts, settlement and deed-in-lieu agreements, plan timers | rwb_treatment | /treatments | rwb.treatment.events.v1 | rwb-treatment | 2 |
| S3 | rwb-guarantee | TCG and insurance claims, guarantor notices and pursuit | rwb_guarantee | /guarantee-claims | rwb.guarantee.events.v1 | rwb-guarantee | 3 |
| S4 | rwb-litigation | legal actions, hearings, judgments, enforcement, LED auction ladder | rwb_litigation | /legal-actions | rwb.litigation.events.v1 | rwb-litigation | 3 |
| S5 | rwb-asset | assets taken on, holding, floor price, listings, auction rounds | rwb_asset | /assets | rwb.asset.events.v1 | rwb-asset | 2 |
| S6 | rwb-debtsale | lots, data room, buyer terms, bids, award, transfer | rwb_debtsale | /lots | rwb.debtsale.events.v1 | rwb-debtsale | 3 |
| S7 | rwb-writeoff | eligibility, committee, posting, recovery after charge-off | rwb_writeoff | /write-offs | rwb.writeoff.events.v1 | rwb-writeoff | 4 |


41

Notes: Every service follows the same naming: schema rwb_<name> in the ACE database with its own login; REST under /api/recovery/<name>/v1 behind gateway-bff; Kafka topic rwb.<name>.events.v1; Temporal task queue rwb-<name> in namespace rwb-recovery. Wave = the delivery wave in which the service is created (Wave 1 = Epic 1).

