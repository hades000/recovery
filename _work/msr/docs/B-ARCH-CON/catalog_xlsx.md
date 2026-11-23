## Read me

| SCB Collections and Recovery. Henka Group, 22 November 2026. | (C) Siam Commercial Bank and Henka Pte Ltd |
| Item | Value |
| Document | Recovery Workbench Service Contract Catalog v1 |
| Version | 1 |
| Date | 22 November 2026 |
| Decision | D-RCV-60 microservice realignment |
| Tool | T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Status | Draft |
| Owner role | Solution architect |
| Purpose | The contract register of the 19 Recovery services: what each service provides and consumes, in which call type, under which artefact, with which dependency class and which test |
| Source of record | Architecture v5 Text Extract v1 slides 13 to 20 and 41 to 44; Temporal and Drools Design Text Extract v1 slides 11 to 14; Microservice Ownership Map v1 |
| Sheets | Services; Call type matrix; Contract pairs; REST operations; Events; Temporal contracts; Jobs; Resources owned; Conformance; Open points; Change log |
| How to read | Contract pairs is the flat list behind section 5 of the document; one row per provider and consumer pair, class C for a service pair, X for an edge, H for the one self-subscription |
| Ownership | Every owner in this workbook comes from the Microservice Ownership Map v1 |

## Services

| Code | Service | Name | Wave | Schema and login | REST base | Kafka topic | Task queue | Java package | Service epic | Owns (Arch v5 slide 41) |
| P1 | rwb-source-data | Source data | 1 | rwb_source_data | /api/recovery/source-data/v1 | rwb.source-data.events.v1 | rwb-source-data | th.co.scb.ace.workbench.recovery.sourcedata | RWB-SVC-P1 | ACE view contract, extension tables, freshness, reconciliation |
| P2 | rwb-integration | Integration | 1 | rwb_integration | /api/recovery/integration/v1 | rwb.integration.events.v1 | rwb-integration | th.co.scb.ace.workbench.recovery.integration | RWB-SVC-P2 | interface config, file runs, outbound items, ACE integration paths |
| P3 | rwb-case | Case and workflow | 1 | rwb_case | /api/recovery/case/v1 | rwb.case.events.v1 | rwb-case | th.co.scb.ace.workbench.recovery.case | RWB-SVC-P3 | case, CMMN state, queues, tasks, allocation, timers |
| P4 | rwb-access | Access and authority | 1 | rwb_access | /api/recovery/access/v1 | rwb.access.events.v1 | rwb-access | th.co.scb.ace.workbench.recovery.access | RWB-SVC-P4 | Recovery roles as data, scope, masking policy, DoA table, access log |
| P5 | rwb-document | Document | 1 | rwb_document | /api/recovery/document/v1 | rwb.document.events.v1 | rwb-document | th.co.scb.ace.workbench.recovery.document | RWB-SVC-P5 | metadata, custody, OCR text and fields, signatures, retention |
| P6 | rwb-comms | Communications | 1 | rwb_comms | /api/recovery/comms/v1 | rwb.comms.events.v1 | rwb-comms | th.co.scb.ace.workbench.recovery.comms | RWB-SVC-P6 | notices, templates, merge fields, proof of delivery |
| P7 | rwb-decision | Decision and rules | 1 | rwb_decision | /api/recovery/decision/v1 | rwb.decision.events.v1 | rwb-decision | th.co.scb.ace.workbench.recovery.decision | RWB-SVC-P7 | approvals, central decision ledger, DMN model registry |
| P8 | rwb-payment | Payment | 2 | rwb_payment | /api/recovery/payment/v1 | rwb.payment.events.v1 | rwb-payment | th.co.scb.ace.workbench.recovery.payment | RWB-SVC-P8 | payment and proceeds matching, fees, bookings, posting files |
| P9 | rwb-reporting | Reporting | 1 | rwb_reporting | /api/recovery/reporting/v1 | rwb.reporting.events.v1 | rwb-reporting | th.co.scb.ace.workbench.recovery.reporting | RWB-SVC-P9 | measures, snapshots, steering dashboard, regulatory reports |
| P10 | rwb-agent | Agent | 1 | rwb_agent | /api/recovery/agent/v1 | rwb.agent.events.v1 | rwb-agent | th.co.scb.ace.workbench.recovery.agent | RWB-SVC-P10 | agent policies, prompts, runs, guardrails, evaluations |
| S1 | rwb-valuation | Valuation and route | 3 | rwb_valuation | /api/recovery/valuation/v1 | rwb.valuation.events.v1 | rwb-valuation | th.co.scb.ace.workbench.recovery.valuation | RWB-SVC-S1 | valuations, D6 route decision, route agent output |
| S2 | rwb-treatment | Treatment and offer | 2 | rwb_treatment | /api/recovery/treatment/v1 | rwb.treatment.events.v1 | rwb-treatment | th.co.scb.ace.workbench.recovery.treatment | RWB-SVC-S2 | treatments, contracts, settlement and deed-in-lieu agreements, plan timers |
| S3 | rwb-guarantee | Guarantee | 3 | rwb_guarantee | /api/recovery/guarantee/v1 | rwb.guarantee.events.v1 | rwb-guarantee | th.co.scb.ace.workbench.recovery.guarantee | RWB-SVC-S3 | TCG and insurance claims, guarantor notices and pursuit |
| S4 | rwb-litigation | Litigation | 3 | rwb_litigation | /api/recovery/litigation/v1 | rwb.litigation.events.v1 | rwb-litigation | th.co.scb.ace.workbench.recovery.litigation | RWB-SVC-S4 | legal actions, hearings, judgments, enforcement, LED auction ladder |
| S5 | rwb-asset | Asset | 2 | rwb_asset | /api/recovery/asset/v1 | rwb.asset.events.v1 | rwb-asset | th.co.scb.ace.workbench.recovery.asset | RWB-SVC-S5 | assets taken on, holding, floor price, listings, auction rounds |
| S6 | rwb-debtsale | Debt sale | 3 | rwb_debtsale | /api/recovery/debtsale/v1 | rwb.debtsale.events.v1 | rwb-debtsale | th.co.scb.ace.workbench.recovery.debtsale | RWB-SVC-S6 | lots, data room, buyer terms, bids, award, transfer |
| S7 | rwb-writeoff | Write-off | 4 | rwb_writeoff | /api/recovery/writeoff/v1 | rwb.writeoff.events.v1 | rwb-writeoff | th.co.scb.ace.workbench.recovery.writeoff | RWB-SVC-S7 | eligibility, committee, posting, recovery after charge-off |
| S8 | rwb-deviation | Deviation | 2 | rwb_deviation | /api/recovery/deviation/v1 | rwb.deviation.events.v1 | rwb-deviation | th.co.scb.ace.workbench.recovery.deviation | RWB-SVC-S8 | X1-X7 screening, pause, handling, return |
| S9 | rwb-partner | Partner | 4 | rwb_partner | /api/recovery/partner/v1 | rwb.partner.events.v1 | rwb-partner | th.co.scb.ace.workbench.recovery.partner | RWB-SVC-S9 | panel, partner users, instructions, results, fees, scorecards |

## Call type matrix

| starts / target | P3 | P7 | P4 | S8 | S1 | S2 | S3 | S4 | S5 | S6 | S7 | P5 | P6 | P8 | S9 | P2 | P1 | P9 | P10 | ACE Cmn | ACE DB | Outside |
| P3 rwb-case |  | E | R | T E | T E | T E | T E | T E | T E | T E | T E | E | E | E | E |  | T E |  |  |  |  |  |
| P7 rwb-decision |  |  | R |  |  |  |  |  |  |  |  |  | E |  |  |  |  |  | E |  |  | F |
| P4 rwb-access |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | R |  |  |
| S8 rwb-deviation | E |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | R E |  | T E |  |  |  |
| S1 rwb-valuation |  | T E |  |  |  |  |  |  |  |  |  |  |  |  |  |  | R |  | T |  |  |  |
| S2 rwb-treatment |  | T E |  | E |  |  |  |  |  |  |  | T |  | T E |  |  |  |  |  | N |  |  |
| S3 rwb-guarantee |  | T |  |  |  |  |  |  |  |  |  |  | T E | E |  |  |  |  |  |  |  |  |
| S4 rwb-litigation |  | T |  |  |  |  |  |  |  |  |  |  | T E |  | T E |  |  |  |  |  |  |  |
| S5 rwb-asset |  | T |  |  |  |  |  | E |  |  |  |  | T | T E | T E |  |  |  |  |  |  |  |
| S6 rwb-debtsale |  | T |  |  |  |  |  |  |  |  |  | T |  | T E |  | T |  |  |  |  |  |  |
| S7 rwb-writeoff |  | T |  |  |  |  |  |  |  |  |  |  |  | T E |  |  | R E |  |  |  |  |  |
| P5 rwb-document |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | T E |  |  | F |
| P6 rwb-comms | E | T |  | E |  | E |  |  |  |  |  | T |  | E |  | T |  |  |  | R |  |  |
| P8 rwb-payment |  | E |  |  |  | E |  |  | E | E | E |  |  |  |  | T | T E |  |  |  |  |  |
| S9 rwb-partner |  |  |  |  |  |  |  |  |  |  |  | R |  |  |  |  |  |  |  |  |  | R |
| P2 rwb-integration |  |  |  |  |  |  |  |  |  |  |  | R |  |  |  |  |  |  |  |  |  | F |
| P1 rwb-source-data |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | S |  |
| P9 rwb-reporting | E |  |  |  |  | E | E |  |  | E | E |  | E |  |  | T | T |  |  |  |  |  |
| P10 rwb-agent | E |  |  |  |  |  |  |  |  |  |  | R E |  |  |  |  | R |  |  |  |  | R |

## Contract pairs

| # | Provider | Consumer | Call type | Interface | Contract artefact | Class | ITG harness | Source |
| 1 | ACE Common | gateway-bff | REST | Sign-in through ACE Common; session to short-lived user JWT | ACE Common API (sign-in, notification path) | X | RWB-ITG-W1 harness | slide 20 |
| 2 | ACE Common | P4 rwb-access | REST | Sign-in, group-to-role (Entra ID) | ACE Common API (sign-in, notification path) | X | RWB-ITG-W1 harness | slide 13, slide 14 |
| 3 | ACE Common | P6 rwb-comms | REST | Notification path (SMS, LINE OA) | ACE Common API (sign-in, notification path) | X | RWB-ITG-W1 harness | slide 13, slide 17 |
| 4 | ACE Common | S2 rwb-treatment | Nexus | restructure.calculate (Nexus operation, namespace ace-collection) | Nexus operation, ace-collection | X | RWB-ITG-W2 harness | slide 13, slide 18 |
| 5 | ACE database | P1 rwb-source-data | SQL view | SELECT on the 30 recovery.v_ace_* views, read only (ADR-010) | View contract, SELECT only | X | RWB-ITG-W1 harness | slide 13, slide 15 |
| 6 | All 19 services | ACE Common | Kafka | Audit and PII logs | AsyncAPI 3.0, ACE Common logging topics | X | RWB-ITG-W1 harness | slide 13 note |
| 7 | All 19 services | P7 rwb-decision | Kafka | DecisionRecorded | AsyncAPI 3.0, rwb.decision-record.v1 | C | RWB-ITG-W1 harness | slide 42, slide 43 (EV-08) |
| 8 | All 19 services | P9 rwb-reporting | Kafka | DecisionRecorded | AsyncAPI 3.0, rwb.decision-record.v1 | C | RWB-ITG-W1 harness | slide 42, slide 43 (EV-08) |
| 9 | Outside the cluster | P10 rwb-agent | REST | Enterprise AI private endpoint (INT-23), HTTPS | The external API or interface of that party | X | RWB-ITG-W1 harness | slide 13, slide 16 |
| 10 | Outside the cluster | S9 rwb-partner | REST | Partners (law firms, agencies, buyers) through the partner gateway, FAPI 2.0, MFA | The external API or interface of that party | X | RWB-ITG-W4 harness | slide 13, slide 17 |
| 11 | P1 rwb-source-data | gateway-bff | Kafka | AceDataLate | AsyncAPI 3.0, rwb.source-data.events.v1 | X | RWB-ITG-W1 harness | slide 42, slide 43 (EV-27) |
| 12 | P1 rwb-source-data | gateway-bff | REST | GET /customers/{id}; GET /accounts/{id}; GET /freshness (composite case screen, one hop each in parallel) | OpenAPI 3.1, /api/recovery/source-data/v1 | X | RWB-ITG-W1 harness | slide 15, slide 20 |
| 13 | P1 rwb-source-data | P10 rwb-agent | REST | Tool: read case facts (read-only tool-gateway call) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RWB-ITG-W1 harness | slide 13, slide 16 |
| 14 | P1 rwb-source-data | P3 rwb-case | Kafka | AceDataReady | AsyncAPI 3.0, rwb.source-data.events.v1 | C | RWB-ITG-W1 harness | slide 42, slide 43 (EV-26) |
| 15 | P1 rwb-source-data | P3 rwb-case | Temporal | Activity: listEligibleAccounts(businessDate) | Activity contract jar on task queue rwb-source-data | C | RWB-ITG-W1 harness | slide 14 |
| 16 | P1 rwb-source-data | P8 rwb-payment | Kafka | AceDataReady | AsyncAPI 3.0, rwb.source-data.events.v1 | C | RWB-ITG-W2 harness | slide 42, slide 43 (EV-26) |
| 17 | P1 rwb-source-data | P8 rwb-payment | Temporal | Activity: payments for business date | Activity contract jar on task queue rwb-source-data | C | RWB-ITG-W2 harness | slide 13, slide 17 |
| 18 | P1 rwb-source-data | P9 rwb-reporting | Temporal | Activity: snapshot(page) for measures | Activity contract jar on task queue rwb-source-data | C | RWB-ITG-W1 harness | slide 13, slide 15 |
| 19 | P1 rwb-source-data | S1 rwb-valuation | REST | Collateral and appraisals (GET /collateral/{id}) | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RWB-ITG-W3 harness | slide 13, slide 18 |
| 20 | P1 rwb-source-data | S7 rwb-writeoff | Kafka | AceDataReady | AsyncAPI 3.0, rwb.source-data.events.v1 | C | RWB-ITG-W4 harness | slide 42, slide 43 (EV-26) |
| 21 | P1 rwb-source-data | S7 rwb-writeoff | REST | GL outcome | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RWB-ITG-W4 harness | slide 13, slide 20 |
| 22 | P1 rwb-source-data | S8 rwb-deviation | Kafka | AceDataReady | AsyncAPI 3.0, rwb.source-data.events.v1 | C | RWB-ITG-W2 harness | slide 42, slide 43 (EV-26) |
| 23 | P1 rwb-source-data | S8 rwb-deviation | REST | Party flags | OpenAPI 3.1, /api/recovery/source-data/v1 | C | RWB-ITG-W2 harness | slide 13, slide 15 |
| 24 | P10 rwb-agent | P5 rwb-document | Kafka | AgentRunCompleted | AsyncAPI 3.0, rwb.agent.events.v1 | C | RWB-ITG-W1 harness | slide 42, slide 43 (EV-28) |
| 25 | P10 rwb-agent | P5 rwb-document | Temporal | Child workflow: classify / extract run | Activity contract jar on task queue rwb-agent | C | RWB-ITG-W1 harness | slide 13, slide 16 |
| 26 | P10 rwb-agent | P7 rwb-decision | Kafka | AgentRunCompleted | AsyncAPI 3.0, rwb.agent.events.v1 | C | RWB-ITG-W1 harness | slide 42, slide 43 (EV-28) |
| 27 | P10 rwb-agent | S1 rwb-valuation | Temporal | Child workflow: route agent run | Activity contract jar on task queue rwb-agent | C | RWB-ITG-W3 harness | slide 13, slide 18 |
| 28 | P10 rwb-agent | S8 rwb-deviation | Kafka | AgentRunCompleted | AsyncAPI 3.0, rwb.agent.events.v1 | C | RWB-ITG-W2 harness | slide 42, slide 43 (EV-28) |
| 29 | P10 rwb-agent | S8 rwb-deviation | Temporal | Child workflow: screening agent run | Activity contract jar on task queue rwb-agent | C | RWB-ITG-W2 harness | slide 13, slide 15 |
| 30 | P2 rwb-integration | Outside the cluster | File | WIN registered mail, daily outbound file (INT-14); debt buyers, per lot, encrypted (INT-25) | File manifest (fileId, batchId, sha256, record count) | X | RWB-ITG-W1 harness | slide 13, slide 16 |
| 31 | P2 rwb-integration | P6 rwb-comms | Temporal | Activity: deliverFile (WIN letters) | Activity contract jar on task queue rwb-integration | C | RWB-ITG-W1 harness | slide 13, slide 17 |
| 32 | P2 rwb-integration | P8 rwb-payment | Temporal | Activity: deliverFile (posting file) | Activity contract jar on task queue rwb-integration | C | RWB-ITG-W2 harness | slide 13, slide 17 |
| 33 | P2 rwb-integration | P9 rwb-reporting | Temporal | Activity: deliverFile (regulatory extract) | Activity contract jar on task queue rwb-integration | C | RWB-ITG-W1 harness | slide 13, slide 15 |
| 34 | P2 rwb-integration | The requesting service | Kafka | FileDelivered | AsyncAPI 3.0, rwb.integration.events.v1 | X | RWB-ITG-W1 harness | slide 43 (event catalogue, not numbered) |
| 35 | P2 rwb-integration | The requesting service | Kafka | FileFailed | AsyncAPI 3.0, rwb.integration.events.v1 | X | RWB-ITG-W1 harness | slide 43 (event catalogue, not numbered) |
| 36 | P2 rwb-integration | S6 rwb-debtsale | Temporal | Activity: deliverFile (buyer file) | Activity contract jar on task queue rwb-integration | C | RWB-ITG-W3 harness | slide 13, slide 19 |
| 37 | P3 rwb-case | gateway-bff | Kafka | TimerBreached | AsyncAPI 3.0, rwb.case.events.v1 | X | RWB-ITG-W1 harness | slide 42, slide 43 (EV-19) |
| 38 | P3 rwb-case | gateway-bff | REST | GET /cases/{id}; GET /cases?queue=; POST /cases/{id}/actions; GET /tasks; POST /tasks/{id}/complete; GET /case-summary/{id} | OpenAPI 3.1, /api/recovery/case/v1 | X | RWB-ITG-W1 harness | slide 14, slide 20 |
| 39 | P3 rwb-case | P10 rwb-agent | Kafka | CaseCreated | AsyncAPI 3.0, rwb.case.events.v1 | C | RWB-ITG-W1 harness | slide 42, slide 43 (EV-01) |
| 40 | P3 rwb-case | P3 rwb-case | Kafka | CaseAllocationFailed | AsyncAPI 3.0, rwb.case.events.v1 | H | RWB-ITG-W1 harness | slide 42, slide 43 (EV-03) |
| 41 | P3 rwb-case | P6 rwb-comms | Kafka | CaseStateChanged | AsyncAPI 3.0, rwb.case.events.v1 | C | RWB-ITG-W1 harness | slide 42, slide 43 (EV-05) |
| 42 | P3 rwb-case | P9 rwb-reporting | Kafka | CaseAllocated | AsyncAPI 3.0, rwb.case.events.v1 | C | RWB-ITG-W1 harness | slide 42, slide 43 (EV-02) |
| 43 | P3 rwb-case | P9 rwb-reporting | Kafka | CaseCreated | AsyncAPI 3.0, rwb.case.events.v1 | C | RWB-ITG-W1 harness | slide 42, slide 43 (EV-01) |
| 44 | P3 rwb-case | P9 rwb-reporting | Kafka | CaseStateChanged | AsyncAPI 3.0, rwb.case.events.v1 | C | RWB-ITG-W1 harness | slide 42, slide 43 (EV-05) |
| 45 | P3 rwb-case | P9 rwb-reporting | Kafka | CaseTransferred | AsyncAPI 3.0, rwb.case.events.v1 | C | RWB-ITG-W1 harness | slide 42, slide 43 (EV-04) |
| 46 | P3 rwb-case | S8 rwb-deviation | Kafka | CaseCreated | AsyncAPI 3.0, rwb.case.events.v1 | C | RWB-ITG-W2 harness | slide 42, slide 43 (EV-01) |
| 47 | P4 rwb-access | All 19 services | Kafka | AccessPolicyChanged | AsyncAPI 3.0, rwb.access.events.v1 | C | RWB-ITG-W1 harness | slide 43 (event catalogue, not numbered) |
| 48 | P4 rwb-access | All 19 services | Kafka | DoaLimitChanged | AsyncAPI 3.0, rwb.access.events.v1 | C | RWB-ITG-W1 harness | slide 43 (event catalogue, not numbered) |
| 49 | P4 rwb-access | P3 rwb-case | REST | POST /authorise (role, scope, DoA), cached in rwb-case | OpenAPI 3.1, /api/recovery/access/v1 | C | RWB-ITG-W1 harness | slide 13, slide 14 |
| 50 | P4 rwb-access | P7 rwb-decision | REST | GET /doa-limits (DoA limits) | OpenAPI 3.1, /api/recovery/access/v1 | C | RWB-ITG-W1 harness | slide 13, slide 14 |
| 51 | P5 rwb-document | Outside the cluster | File | Azure Blob (WORM): files, 2.8 TB by 2031 | File manifest (fileId, batchId, sha256, record count) | X | RWB-ITG-W1 harness | slide 13, slide 16 |
| 52 | P5 rwb-document | P10 rwb-agent | Kafka | DocumentStored | AsyncAPI 3.0, rwb.document.events.v1 | C | RWB-ITG-W1 harness | slide 42, slide 43 (EV-16) |
| 53 | P5 rwb-document | P10 rwb-agent | REST | Tool: read extracted fields (read-only tool-gateway call) | OpenAPI 3.1, /api/recovery/document/v1 | C | RWB-ITG-W1 harness | slide 13, slide 16 |
| 54 | P5 rwb-document | P2 rwb-integration | REST | Fetch file by ID (SAS link) | OpenAPI 3.1, /api/recovery/document/v1 | C | RWB-ITG-W1 harness | slide 13, slide 16 |
| 55 | P5 rwb-document | P3 rwb-case | Kafka | DocumentFieldsExtracted | AsyncAPI 3.0, rwb.document.events.v1 | C | RWB-ITG-W1 harness | slide 42, slide 43 (EV-17) |
| 56 | P5 rwb-document | P3 rwb-case | Kafka | DocumentStored | AsyncAPI 3.0, rwb.document.events.v1 | C | RWB-ITG-W1 harness | slide 42, slide 43 (EV-16) |
| 57 | P5 rwb-document | P6 rwb-comms | Temporal | Document: generate letter | Activity contract jar on task queue rwb-document | C | RWB-ITG-W1 harness | slide 13, slide 17 |
| 58 | P5 rwb-document | S2 rwb-treatment | Temporal | Contract document generation and e-sign | Activity contract jar on task queue rwb-document | C | RWB-ITG-W2 harness | slide 13, slide 18 |
| 59 | P5 rwb-document | S6 rwb-debtsale | Temporal | Document: data room pack | Activity contract jar on task queue rwb-document | C | RWB-ITG-W3 harness | slide 13, slide 19 |
| 60 | P5 rwb-document | S9 rwb-partner | REST | Partner uploads (SAS link) | OpenAPI 3.1, /api/recovery/document/v1 | C | RWB-ITG-W4 harness | slide 13, slide 17 |
| 61 | P6 rwb-comms | P3 rwb-case | Kafka | NoticeDelivered | AsyncAPI 3.0, rwb.comms.events.v1 | C | RWB-ITG-W1 harness | slide 42, slide 43 (EV-15) |
| 62 | P6 rwb-comms | P7 rwb-decision | Kafka | NoticeGenerated | AsyncAPI 3.0, rwb.comms.events.v1 | C | RWB-ITG-W1 harness | slide 42, slide 43 (EV-13) |
| 63 | P6 rwb-comms | P9 rwb-reporting | Kafka | NoticeDispatched | AsyncAPI 3.0, rwb.comms.events.v1 | C | RWB-ITG-W1 harness | slide 42, slide 43 (EV-14) |
| 64 | P6 rwb-comms | S3 rwb-guarantee | Kafka | NoticeDelivered | AsyncAPI 3.0, rwb.comms.events.v1 | C | RWB-ITG-W3 harness | slide 42, slide 43 (EV-15) |
| 65 | P6 rwb-comms | S3 rwb-guarantee | Temporal | Child workflow: guarantor notice | Activity contract jar on task queue rwb-comms | C | RWB-ITG-W3 harness | slide 13, slide 18 |
| 66 | P6 rwb-comms | S4 rwb-litigation | Kafka | NoticeDelivered | AsyncAPI 3.0, rwb.comms.events.v1 | C | RWB-ITG-W3 harness | slide 42, slide 43 (EV-15) |
| 67 | P6 rwb-comms | S4 rwb-litigation | Temporal | Child workflow: demand notice | Activity contract jar on task queue rwb-comms | C | RWB-ITG-W3 harness | slide 13, slide 19 |
| 68 | P6 rwb-comms | S5 rwb-asset | Temporal | Not specified in the source documents (CG-B-ARCH-CON-8; ASM-B-ARCH-CON-8) | Activity contract jar on task queue rwb-comms | C | RWB-ITG-W2 harness | slide 13 |
| 69 | P7 rwb-decision | gateway-bff | Kafka | ApprovalRequested | AsyncAPI 3.0, rwb.decision.events.v1 | X | RWB-ITG-W1 harness | slide 42, slide 43 (EV-09) |
| 70 | P7 rwb-decision | Outside the cluster | File | Immutable storage: daily ledger seal (WORM) | File manifest (fileId, batchId, sha256, record count) | X | RWB-ITG-W1 harness | slide 13, slide 14 |
| 71 | P7 rwb-decision | Not specified in the source documents (CG-B-ARCH-CON-4; ASM-B-ARCH-CON-4) | Kafka | ApprovalDecided | AsyncAPI 3.0, rwb.decision.events.v1 | C | RWB-ITG-W1 harness | slide 43 (event catalogue, not numbered) |
| 72 | P7 rwb-decision | P3 rwb-case | Kafka | RulePackageInForce | AsyncAPI 3.0, rwb.decision.events.v1 | C | RWB-ITG-W1 harness | slide 42, slide 43 (EV-30) |
| 73 | P7 rwb-decision | P6 rwb-comms | Temporal | Child workflow: approval | Activity contract jar on task queue rwb-decision | C | RWB-ITG-W1 harness | slide 13, slide 17 |
| 74 | P7 rwb-decision | P8 rwb-payment | Kafka | RulePackageInForce | AsyncAPI 3.0, rwb.decision.events.v1 | C | RWB-ITG-W2 harness | slide 42, slide 43 (EV-30) |
| 75 | P7 rwb-decision | S1 rwb-valuation | Kafka | RulePackageInForce | AsyncAPI 3.0, rwb.decision.events.v1 | C | RWB-ITG-W3 harness | slide 42, slide 43 (EV-30) |
| 76 | P7 rwb-decision | S1 rwb-valuation | Temporal | Child workflow: ApprovalWorkflow (kit template) | Activity contract jar on task queue rwb-decision | C | RWB-ITG-W3 harness | slide 13, slide 18 |
| 77 | P7 rwb-decision | S2 rwb-treatment | Kafka | RulePackageInForce | AsyncAPI 3.0, rwb.decision.events.v1 | C | RWB-ITG-W2 harness | slide 42, slide 43 (EV-30) |
| 78 | P7 rwb-decision | S2 rwb-treatment | Temporal | Child workflow: ApprovalWorkflow (DoA) | Activity contract jar on task queue rwb-decision | C | RWB-ITG-W2 harness | slide 13, slide 18 |
| 79 | P7 rwb-decision | S3 rwb-guarantee | Temporal | Child workflow: ApprovalWorkflow | Activity contract jar on task queue rwb-decision | C | RWB-ITG-W3 harness | slide 13, slide 18 |
| 80 | P7 rwb-decision | S4 rwb-litigation | Temporal | Child workflow: ApprovalWorkflow | Activity contract jar on task queue rwb-decision | C | RWB-ITG-W3 harness | slide 13, slide 19 |
| 81 | P7 rwb-decision | S5 rwb-asset | Temporal | Child workflow: ApprovalWorkflow | Activity contract jar on task queue rwb-decision | C | RWB-ITG-W2 harness | slide 13, slide 19 |
| 82 | P7 rwb-decision | S6 rwb-debtsale | Temporal | Child workflow: ApprovalWorkflow | Activity contract jar on task queue rwb-decision | C | RWB-ITG-W3 harness | slide 13, slide 19 |
| 83 | P7 rwb-decision | S7 rwb-writeoff | Temporal | Child workflow: committee approval | Activity contract jar on task queue rwb-decision | C | RWB-ITG-W4 harness | slide 13, slide 20 |
| 84 | P8 rwb-payment | P3 rwb-case | Kafka | PaymentMissed | AsyncAPI 3.0, rwb.payment.events.v1 | C | RWB-ITG-W2 harness | slide 42, slide 43 (EV-12) |
| 85 | P8 rwb-payment | P3 rwb-case | Kafka | ProceedsMatched | AsyncAPI 3.0, rwb.payment.events.v1 | C | RWB-ITG-W2 harness | slide 42, slide 43 (EV-25) |
| 86 | P8 rwb-payment | P3 rwb-case | Kafka | TreatmentBooked | AsyncAPI 3.0, rwb.payment.events.v1 | C | RWB-ITG-W2 harness | slide 42, slide 43 (EV-11) |
| 87 | P8 rwb-payment | P6 rwb-comms | Kafka | PaymentMissed | AsyncAPI 3.0, rwb.payment.events.v1 | C | RWB-ITG-W2 harness | slide 42, slide 43 (EV-12) |
| 88 | P8 rwb-payment | S2 rwb-treatment | Kafka | PaymentMissed | AsyncAPI 3.0, rwb.payment.events.v1 | C | RWB-ITG-W2 harness | slide 42, slide 43 (EV-12) |
| 89 | P8 rwb-payment | S2 rwb-treatment | Kafka | TreatmentBooked | AsyncAPI 3.0, rwb.payment.events.v1 | C | RWB-ITG-W2 harness | slide 42, slide 43 (EV-11) |
| 90 | P8 rwb-payment | S2 rwb-treatment | Temporal | Activity: postProceeds (saga step) | Activity contract jar on task queue rwb-payment | C | RWB-ITG-W2 harness | slide 13, slide 18 |
| 91 | P8 rwb-payment | S3 rwb-guarantee | Kafka | ProceedsMatched | AsyncAPI 3.0, rwb.payment.events.v1 | C | RWB-ITG-W3 harness | slide 42, slide 43 (EV-25) |
| 92 | P8 rwb-payment | S5 rwb-asset | Kafka | ProceedsMatched | AsyncAPI 3.0, rwb.payment.events.v1 | C | RWB-ITG-W2 harness | slide 42, slide 43 (EV-25) |
| 93 | P8 rwb-payment | S5 rwb-asset | Temporal | Activity: postProceeds | Activity contract jar on task queue rwb-payment | C | RWB-ITG-W2 harness | slide 13, slide 19 |
| 94 | P8 rwb-payment | S6 rwb-debtsale | Kafka | ProceedsMatched | AsyncAPI 3.0, rwb.payment.events.v1 | C | RWB-ITG-W3 harness | slide 42, slide 43 (EV-25) |
| 95 | P8 rwb-payment | S6 rwb-debtsale | Temporal | Activity: postProceeds | Activity contract jar on task queue rwb-payment | C | RWB-ITG-W3 harness | slide 13, slide 19 |
| 96 | P8 rwb-payment | S7 rwb-writeoff | Kafka | ProceedsMatched | AsyncAPI 3.0, rwb.payment.events.v1 | C | RWB-ITG-W4 harness | slide 42, slide 43 (EV-25) |
| 97 | P8 rwb-payment | S7 rwb-writeoff | Temporal | Activity: postProceeds | Activity contract jar on task queue rwb-payment | C | RWB-ITG-W4 harness | slide 13, slide 20 |
| 98 | P9 rwb-reporting | Not specified in the source documents (CG-B-ARCH-CON-4; ASM-B-ARCH-CON-4) | Kafka | ReportPublished | AsyncAPI 3.0, rwb.reporting.events.v1 | C | RWB-ITG-W1 harness | slide 43 (event catalogue, not numbered) |
| 99 | S1 rwb-valuation | P3 rwb-case | Kafka | RouteDecided | AsyncAPI 3.0, rwb.valuation.events.v1 | C | RWB-ITG-W3 harness | slide 43 (event catalogue, not numbered) |
| 100 | S1 rwb-valuation | P3 rwb-case | Temporal | Child workflow: RouteDecisionWorkflow | Activity contract jar on task queue rwb-valuation | C | RWB-ITG-W3 harness | slide 14, slide 18 |
| 101 | S2 rwb-treatment | P3 rwb-case | Kafka | TreatmentClosed | AsyncAPI 3.0, rwb.treatment.events.v1 | C | RWB-ITG-W2 harness | slide 43 (event catalogue, not numbered) |
| 102 | S2 rwb-treatment | P3 rwb-case | Temporal | Child workflow: the treatment stage workflows (TreatmentWorkflow) | Activity contract jar on task queue rwb-treatment | C | RWB-ITG-W2 harness | slide 14, slide 18 |
| 103 | S2 rwb-treatment | P6 rwb-comms | Kafka | TreatmentApproved | AsyncAPI 3.0, rwb.treatment.events.v1 | C | RWB-ITG-W2 harness | slide 42, slide 43 (EV-10) |
| 104 | S2 rwb-treatment | P8 rwb-payment | Kafka | TreatmentApproved | AsyncAPI 3.0, rwb.treatment.events.v1 | C | RWB-ITG-W2 harness | slide 42, slide 43 (EV-10) |
| 105 | S2 rwb-treatment | P9 rwb-reporting | Kafka | TreatmentClosed | AsyncAPI 3.0, rwb.treatment.events.v1 | C | RWB-ITG-W2 harness | slide 43 (event catalogue, not numbered) |
| 106 | S3 rwb-guarantee | P3 rwb-case | Kafka | GuaranteeClaimFiled | AsyncAPI 3.0, rwb.guarantee.events.v1 | C | RWB-ITG-W3 harness | slide 43 (event catalogue, not numbered) |
| 107 | S3 rwb-guarantee | P3 rwb-case | Kafka | GuaranteeClaimSettled | AsyncAPI 3.0, rwb.guarantee.events.v1 | C | RWB-ITG-W3 harness | slide 43 (event catalogue, not numbered) |
| 108 | S3 rwb-guarantee | P3 rwb-case | Temporal | Child workflow: GuaranteeClaimWorkflow | Activity contract jar on task queue rwb-guarantee | C | RWB-ITG-W3 harness | slide 14, slide 18 |
| 109 | S3 rwb-guarantee | P9 rwb-reporting | Kafka | GuaranteeClaimFiled | AsyncAPI 3.0, rwb.guarantee.events.v1 | C | RWB-ITG-W3 harness | slide 43 (event catalogue, not numbered) |
| 110 | S3 rwb-guarantee | P9 rwb-reporting | Kafka | GuaranteeClaimSettled | AsyncAPI 3.0, rwb.guarantee.events.v1 | C | RWB-ITG-W3 harness | slide 43 (event catalogue, not numbered) |
| 111 | S4 rwb-litigation | P3 rwb-case | Kafka | AuctionResult | AsyncAPI 3.0, rwb.litigation.events.v1 | C | RWB-ITG-W3 harness | slide 43 (event catalogue, not numbered) |
| 112 | S4 rwb-litigation | P3 rwb-case | Kafka | JudgmentRecorded | AsyncAPI 3.0, rwb.litigation.events.v1 | C | RWB-ITG-W3 harness | slide 43 (event catalogue, not numbered) |
| 113 | S4 rwb-litigation | P3 rwb-case | Temporal | Child workflow: LitigationWorkflow | Activity contract jar on task queue rwb-litigation | C | RWB-ITG-W3 harness | slide 14, slide 19 |
| 114 | S4 rwb-litigation | S5 rwb-asset | Kafka | AuctionResult | AsyncAPI 3.0, rwb.litigation.events.v1 | C | RWB-ITG-W3 harness | slide 43 (event catalogue, not numbered) |
| 115 | S4 rwb-litigation | S5 rwb-asset | Kafka | JudgmentRecorded | AsyncAPI 3.0, rwb.litigation.events.v1 | C | RWB-ITG-W3 harness | slide 43 (event catalogue, not numbered) |
| 116 | S5 rwb-asset | P3 rwb-case | Kafka | AssetSold | AsyncAPI 3.0, rwb.asset.events.v1 | C | RWB-ITG-W2 harness | slide 43 (event catalogue, not numbered) |
| 117 | S5 rwb-asset | P3 rwb-case | Kafka | AssetTakenOn | AsyncAPI 3.0, rwb.asset.events.v1 | C | RWB-ITG-W2 harness | slide 42, slide 43 (EV-22) |
| 118 | S5 rwb-asset | P3 rwb-case | Temporal | Child workflow: AssetDisposalWorkflow | Activity contract jar on task queue rwb-asset | C | RWB-ITG-W2 harness | slide 14, slide 19 |
| 119 | S5 rwb-asset | P8 rwb-payment | Kafka | AssetSold | AsyncAPI 3.0, rwb.asset.events.v1 | C | RWB-ITG-W2 harness | slide 43 (event catalogue, not numbered) |
| 120 | S5 rwb-asset | P8 rwb-payment | Kafka | AssetTakenOn | AsyncAPI 3.0, rwb.asset.events.v1 | C | RWB-ITG-W2 harness | slide 42, slide 43 (EV-22) |
| 121 | S6 rwb-debtsale | P3 rwb-case | Kafka | AccountsTransferred | AsyncAPI 3.0, rwb.debtsale.events.v1 | C | RWB-ITG-W3 harness | slide 43 (event catalogue, not numbered) |
| 122 | S6 rwb-debtsale | P3 rwb-case | Kafka | LotAwarded | AsyncAPI 3.0, rwb.debtsale.events.v1 | C | RWB-ITG-W3 harness | slide 42, slide 43 (EV-23) |
| 123 | S6 rwb-debtsale | P3 rwb-case | Temporal | Child workflow: DebtSaleWorkflow | Activity contract jar on task queue rwb-debtsale | C | RWB-ITG-W3 harness | slide 14, slide 19 |
| 124 | S6 rwb-debtsale | P8 rwb-payment | Kafka | LotAwarded | AsyncAPI 3.0, rwb.debtsale.events.v1 | C | RWB-ITG-W3 harness | slide 42, slide 43 (EV-23) |
| 125 | S6 rwb-debtsale | P9 rwb-reporting | Kafka | AccountsTransferred | AsyncAPI 3.0, rwb.debtsale.events.v1 | C | RWB-ITG-W3 harness | slide 43 (event catalogue, not numbered) |
| 126 | S7 rwb-writeoff | P3 rwb-case | Kafka | WriteOffApproved | AsyncAPI 3.0, rwb.writeoff.events.v1 | C | RWB-ITG-W4 harness | slide 42, slide 43 (EV-24) |
| 127 | S7 rwb-writeoff | P3 rwb-case | Temporal | Child workflow: WriteOffWorkflow | Activity contract jar on task queue rwb-writeoff | C | RWB-ITG-W4 harness | slide 14, slide 20 |
| 128 | S7 rwb-writeoff | P8 rwb-payment | Kafka | WriteOffApproved | AsyncAPI 3.0, rwb.writeoff.events.v1 | C | RWB-ITG-W4 harness | slide 42, slide 43 (EV-24) |
| 129 | S7 rwb-writeoff | P9 rwb-reporting | Kafka | WriteOffApproved | AsyncAPI 3.0, rwb.writeoff.events.v1 | C | RWB-ITG-W4 harness | slide 42, slide 43 (EV-24) |
| 130 | S8 rwb-deviation | P3 rwb-case | Kafka | DeviationCleared | AsyncAPI 3.0, rwb.deviation.events.v1 | C | RWB-ITG-W2 harness | slide 42, slide 43 (EV-07) |
| 131 | S8 rwb-deviation | P3 rwb-case | Kafka | DeviationRaised | AsyncAPI 3.0, rwb.deviation.events.v1 | C | RWB-ITG-W2 harness | slide 42, slide 43 (EV-06) |
| 132 | S8 rwb-deviation | P3 rwb-case | Temporal | Child workflow: DeviationWorkflow | Activity contract jar on task queue rwb-deviation | C | RWB-ITG-W2 harness | slide 14, slide 15 |
| 133 | S8 rwb-deviation | P6 rwb-comms | Kafka | DeviationCleared | AsyncAPI 3.0, rwb.deviation.events.v1 | C | RWB-ITG-W2 harness | slide 42, slide 43 (EV-07) |
| 134 | S8 rwb-deviation | P6 rwb-comms | Kafka | DeviationRaised | AsyncAPI 3.0, rwb.deviation.events.v1 | C | RWB-ITG-W2 harness | slide 42, slide 43 (EV-06) |
| 135 | S8 rwb-deviation | S2 rwb-treatment | Kafka | DeviationRaised | AsyncAPI 3.0, rwb.deviation.events.v1 | C | RWB-ITG-W2 harness | slide 42, slide 43 (EV-06) |
| 136 | S9 rwb-partner | P3 rwb-case | Kafka | PartnerResultSubmitted | AsyncAPI 3.0, rwb.partner.events.v1 | C | RWB-ITG-W4 harness | slide 42, slide 43 (EV-21) |
| 137 | S9 rwb-partner | Partner portal | Kafka | InstructionIssued | AsyncAPI 3.0, rwb.partner.events.v1 | X | RWB-ITG-W4 harness | slide 42, slide 43 (EV-20) |
| 138 | S9 rwb-partner | S4 rwb-litigation | Kafka | PartnerResultSubmitted | AsyncAPI 3.0, rwb.partner.events.v1 | C | RWB-ITG-W4 harness | slide 42, slide 43 (EV-21) |
| 139 | S9 rwb-partner | S4 rwb-litigation | Temporal | Activity: issueInstruction (law firm) | Activity contract jar on task queue rwb-partner | C | RWB-ITG-W4 harness | slide 13, slide 19 |
| 140 | S9 rwb-partner | S5 rwb-asset | Kafka | PartnerResultSubmitted | AsyncAPI 3.0, rwb.partner.events.v1 | C | RWB-ITG-W4 harness | slide 42, slide 43 (EV-21) |
| 141 | S9 rwb-partner | S5 rwb-asset | Temporal | Activity: issueInstruction (auction vendor) | Activity contract jar on task queue rwb-partner | C | RWB-ITG-W4 harness | slide 13, slide 19 |

## REST operations

| Operation | Owner | Contract path | Base path |
| GET /admin/access-log | P4 | /api/recovery/access/v1/admin/access-log | /api/recovery/access/v1 |
| GET /admin/agent-configs | P10 | /api/recovery/agent/v1/admin/agent-configs | /api/recovery/agent/v1 |
| GET /admin/agent-evaluations | P10 | /api/recovery/agent/v1/admin/agent-evaluations | /api/recovery/agent/v1 |
| GET /admin/agent-evaluations/{evaluationId}/report | P10 | /api/recovery/agent/v1/admin/agent-evaluations/{evaluationId}/report | /api/recovery/agent/v1 |
| GET /admin/agent-metrics | P10 | /api/recovery/agent/v1/admin/agent-metrics | /api/recovery/agent/v1 |
| GET /admin/agent-runs | P10 | /api/recovery/agent/v1/admin/agent-runs | /api/recovery/agent/v1 |
| GET /admin/change-log | P3 | /api/recovery/case/v1/admin/change-log | /api/recovery/case/v1 |
| GET /admin/data-contracts | P1 | /api/recovery/source-data/v1/admin/data-contracts | /api/recovery/source-data/v1 |
| GET /admin/data-dictionary/fields | P1 | /api/recovery/source-data/v1/admin/data-dictionary/fields | /api/recovery/source-data/v1 |
| GET /admin/data-products | P1 | /api/recovery/source-data/v1/admin/data-products | /api/recovery/source-data/v1 |
| GET /admin/data-quality/exceptions | P1 | /api/recovery/source-data/v1/admin/data-quality/exceptions | /api/recovery/source-data/v1 |
| GET /admin/feature-flags | PLT | GET /admin/feature-flags | PLT |
| GET /admin/jobs | P1 | /api/recovery/source-data/v1/admin/jobs | /api/recovery/source-data/v1 |
| GET /admin/lists/{listCode} | P3 | /api/recovery/case/v1/admin/lists/{listCode} | /api/recovery/case/v1 |
| GET /admin/outbound-items | P2 | /api/recovery/integration/v1/admin/outbound-items | /api/recovery/integration/v1 |
| GET /admin/outbox/deliveries | P2 | /api/recovery/integration/v1/admin/outbox/deliveries | /api/recovery/integration/v1 |
| GET /admin/parameters | P3 | /api/recovery/case/v1/admin/parameters | /api/recovery/case/v1 |
| GET /admin/roles | P4 | /api/recovery/access/v1/admin/roles | /api/recovery/access/v1 |
| GET /admin/rule-package-versions/{versionId}/dry-run | P7 | /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/dry-run | /api/recovery/decision/v1 |
| GET /admin/rule-packages | P7 | /api/recovery/decision/v1/admin/rule-packages | /api/recovery/decision/v1 |
| GET /admin/rule-packages/change-report | P7 | /api/recovery/decision/v1/admin/rule-packages/change-report | /api/recovery/decision/v1 |
| GET /admin/rule-packages/{packageCode}/versions | P7 | /api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions | /api/recovery/decision/v1 |
| GET /admin/rule-versions | P7 | /api/recovery/decision/v1/admin/rule-versions | /api/recovery/decision/v1 |
| GET /admin/scheduled-jobs | P2 | /api/recovery/integration/v1/admin/scheduled-jobs | /api/recovery/integration/v1 |
| GET /admin/templates | P6 | /api/recovery/comms/v1/admin/templates | /api/recovery/comms/v1 |
| GET /admin/templates/{templateId}/content | P6 | /api/recovery/comms/v1/admin/templates/{templateId}/content | /api/recovery/comms/v1 |
| GET /admin/trackers | P1 | /api/recovery/source-data/v1/admin/trackers | /api/recovery/source-data/v1 |
| GET /admin/trackers/retirement-report | P1 | /api/recovery/source-data/v1/admin/trackers/retirement-report | /api/recovery/source-data/v1 |
| GET /approvals | P7 | /api/recovery/decision/v1/approvals | /api/recovery/decision/v1 |
| GET /approvals/{approvalId} | P7 | /api/recovery/decision/v1/approvals/{approvalId} | /api/recovery/decision/v1 |
| GET /assets | S5 | /api/recovery/asset/v1/assets | /api/recovery/asset/v1 |
| GET /assets/{assetId} | S5 | /api/recovery/asset/v1/assets/{assetId} | /api/recovery/asset/v1 |
| GET /assets/{assetKey} | S5 | /api/recovery/asset/v1/assets/{assetKey} | /api/recovery/asset/v1 |
| GET /cases | P3 | /api/recovery/case/v1/cases | /api/recovery/case/v1 |
| GET /cases/export | P3 | /api/recovery/case/v1/cases/export | /api/recovery/case/v1 |
| GET /cases/{caseId} | P3 | /api/recovery/case/v1/cases/{caseId} | /api/recovery/case/v1 |
| GET /cases/{caseId}/accounts | P3 | /api/recovery/case/v1/cases/{caseId}/accounts | /api/recovery/case/v1 |
| GET /cases/{caseId}/agent-outputs | P10 | /api/recovery/agent/v1/cases/{caseId}/agent-outputs | /api/recovery/agent/v1 |
| GET /cases/{caseId}/customer-products | P2 | /api/recovery/integration/v1/cases/{caseId}/customer-products | /api/recovery/integration/v1 |
| GET /cases/{caseId}/document-checklist | P5 | /api/recovery/document/v1/cases/{caseId}/document-checklist | /api/recovery/document/v1 |
| GET /cases/{caseId}/documents | P5 | /api/recovery/document/v1/cases/{caseId}/documents | /api/recovery/document/v1 |
| GET /cases/{caseId}/interactions | P1 | /api/recovery/source-data/v1/cases/{caseId}/interactions | /api/recovery/source-data/v1 |
| GET /cases/{caseId}/next-action | P3 | /api/recovery/case/v1/cases/{caseId}/next-action | /api/recovery/case/v1 |
| GET /cases/{caseId}/parties | P3 | /api/recovery/case/v1/cases/{caseId}/parties | /api/recovery/case/v1 |
| GET /cases/{caseId}/plan-status | P2 | /api/recovery/integration/v1/cases/{caseId}/plan-status | /api/recovery/integration/v1 |
| GET /cases/{caseId}/recommendation | P7 | /api/recovery/decision/v1/cases/{caseId}/recommendation | /api/recovery/decision/v1 |
| GET /cases/{caseId}/timeline | P3 | /api/recovery/case/v1/cases/{caseId}/timeline | /api/recovery/case/v1 |
| GET /cases/{caseId}/timers | P3 | /api/recovery/case/v1/cases/{caseId}/timers | /api/recovery/case/v1 |
| GET /data-products/freshness | P1 | /api/recovery/source-data/v1/data-products/freshness | /api/recovery/source-data/v1 |
| GET /data-products/{productCode}/records | P1 | /api/recovery/source-data/v1/data-products/{productCode}/records | /api/recovery/source-data/v1 |
| GET /debt-sale-lots/{lotId} | S6 | /api/recovery/debtsale/v1/debt-sale-lots/{lotId} | /api/recovery/debtsale/v1 |
| GET /decision-log | P7 | /api/recovery/decision/v1/decision-log | /api/recovery/decision/v1 |
| GET /decision-log/{entryId} | P7 | /api/recovery/decision/v1/decision-log/{entryId} | /api/recovery/decision/v1 |
| GET /documents | P5 | /api/recovery/document/v1/documents | /api/recovery/document/v1 |
| GET /documents/{documentId} | P5 | /api/recovery/document/v1/documents/{documentId} | /api/recovery/document/v1 |
| GET /documents/{documentId}/content | P5 | /api/recovery/document/v1/documents/{documentId}/content | /api/recovery/document/v1 |
| GET /feature-flags | PLT | GET /feature-flags | PLT |
| GET /intake-items/{intakeItemId} | P5 | /api/recovery/document/v1/intake-items/{intakeItemId} | /api/recovery/document/v1 |
| GET /intake-items/{intakeItemId}/content | P5 | /api/recovery/document/v1/intake-items/{intakeItemId}/content | /api/recovery/document/v1 |
| GET /legal-actions/{legalActionId} | S4 | /api/recovery/litigation/v1/legal-actions/{legalActionId} | /api/recovery/litigation/v1 |
| GET /me/session | P4 | /api/recovery/access/v1/me/session | /api/recovery/access/v1 |
| GET /me/tasks | P3 | /api/recovery/case/v1/me/tasks | /api/recovery/case/v1 |
| GET /notices/{noticeId} | P6 | /api/recovery/comms/v1/notices/{noticeId} | /api/recovery/comms/v1 |
| GET /partner/data-room/{lotId} | S6 | /api/recovery/debtsale/v1/partner/data-room/{lotId} | /api/recovery/debtsale/v1 |
| GET /partner/instructions | S9 | /api/recovery/partner/v1/partner/instructions | /api/recovery/partner/v1 |
| GET /partners | S9 | /api/recovery/partner/v1/partners | /api/recovery/partner/v1 |
| GET /proceeds | P8 | /api/recovery/payment/v1/proceeds | /api/recovery/payment/v1 |
| GET /queues | P3 | /api/recovery/case/v1/queues | /api/recovery/case/v1 |
| GET /queues/{queueId}/cases | P3 | /api/recovery/case/v1/queues/{queueId}/cases | /api/recovery/case/v1 |
| GET /reports/measures | P9 | /api/recovery/reporting/v1/reports/measures | /api/recovery/reporting/v1 |
| GET /review-items | P5 | /api/recovery/document/v1/review-items | /api/recovery/document/v1 |
| GET /treatments/{treatmentId} | S2 | /api/recovery/treatment/v1/treatments/{treatmentId} | /api/recovery/treatment/v1 |
| GET /treatments/{treatmentId}/credit-pack | P2 | /api/recovery/integration/v1/treatments/{treatmentId}/credit-pack | /api/recovery/integration/v1 |
| GET /treatments/{treatmentId}/credit-result | P2 | /api/recovery/integration/v1/treatments/{treatmentId}/credit-result | /api/recovery/integration/v1 |
| GET /treatments/{treatmentId}/signature-requests | P6 | /api/recovery/comms/v1/treatments/{treatmentId}/signature-requests | /api/recovery/comms/v1 |
| PATCH /admin/data-contracts/{contractId} | P1 | /api/recovery/source-data/v1/admin/data-contracts/{contractId} | /api/recovery/source-data/v1 |
| PATCH /admin/data-dictionary/fields/{fieldCode} | P1 | /api/recovery/source-data/v1/admin/data-dictionary/fields/{fieldCode} | /api/recovery/source-data/v1 |
| PATCH /admin/feature-flags/{flagKey} | PLT | PATCH /admin/feature-flags/{flagKey} | PLT |
| PATCH /deviations/{deviationId} | S8 | /api/recovery/deviation/v1/deviations/{deviationId} | /api/recovery/deviation/v1 |
| PATCH /documents/{documentId}/fields/{fieldId} | P5 | /api/recovery/document/v1/documents/{documentId}/fields/{fieldId} | /api/recovery/document/v1 |
| PATCH /guarantee-claims/{claimId} | S3 | /api/recovery/guarantee/v1/guarantee-claims/{claimId} | /api/recovery/guarantee/v1 |
| PATCH /legal-actions/{legalActionId} | S4 | /api/recovery/litigation/v1/legal-actions/{legalActionId} | /api/recovery/litigation/v1 |
| PATCH /tasks/{taskId} | P3 | /api/recovery/case/v1/tasks/{taskId} | /api/recovery/case/v1 |
| PATCH /treatments/{treatmentId} | S2 | /api/recovery/treatment/v1/treatments/{treatmentId} | /api/recovery/treatment/v1 |
| POST /admin/agent-configs | P10 | /api/recovery/agent/v1/admin/agent-configs | /api/recovery/agent/v1 |
| POST /admin/agent-configs/{versionId}/approve | P10 | /api/recovery/agent/v1/admin/agent-configs/{versionId}/approve | /api/recovery/agent/v1 |
| POST /admin/agent-evaluations | P10 | /api/recovery/agent/v1/admin/agent-evaluations | /api/recovery/agent/v1 |
| POST /admin/agent-samples | P10 | /api/recovery/agent/v1/admin/agent-samples | /api/recovery/agent/v1 |
| POST /admin/break-glass-grants | P4 | /api/recovery/access/v1/admin/break-glass-grants | /api/recovery/access/v1 |
| POST /admin/data-contracts/{contractId}/publish | P1 | /api/recovery/source-data/v1/admin/data-contracts/{contractId}/publish | /api/recovery/source-data/v1 |
| POST /admin/feature-flags | PLT | POST /admin/feature-flags | PLT |
| POST /admin/interfaces/{interfaceCode}/manual-retirement | P2 | /api/recovery/integration/v1/admin/interfaces/{interfaceCode}/manual-retirement | /api/recovery/integration/v1 |
| POST /admin/jobs/{jobId}/rerun | P1 | /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun | /api/recovery/source-data/v1 |
| POST /admin/outbound-items/{itemId}/resend | P2 | /api/recovery/integration/v1/admin/outbound-items/{itemId}/resend | /api/recovery/integration/v1 |
| POST /admin/outbox/deliveries/{deliveryId}/resend | P2 | /api/recovery/integration/v1/admin/outbox/deliveries/{deliveryId}/resend | /api/recovery/integration/v1 |
| POST /admin/reference-loads | P3 | /api/recovery/case/v1/admin/reference-loads | /api/recovery/case/v1 |
| POST /admin/reference-loads/{loadId}/approve | P3 | /api/recovery/case/v1/admin/reference-loads/{loadId}/approve | /api/recovery/case/v1 |
| POST /admin/reference-loads/{loadId}/rollback | P3 | /api/recovery/case/v1/admin/reference-loads/{loadId}/rollback | /api/recovery/case/v1 |
| POST /admin/reference-loads/{loadId}/verify | P3 | /api/recovery/case/v1/admin/reference-loads/{loadId}/verify | /api/recovery/case/v1 |
| POST /admin/rule-package-versions/{versionId}/approve | P7 | /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/approve | /api/recovery/decision/v1 |
| POST /admin/rule-package-versions/{versionId}/rollback | P7 | /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/rollback | /api/recovery/decision/v1 |
| POST /admin/rule-packages/{packageCode}/versions | P7 | /api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions | /api/recovery/decision/v1 |
| POST /admin/rule-versions | P7 | /api/recovery/decision/v1/admin/rule-versions | /api/recovery/decision/v1 |
| POST /admin/rule-versions/{versionId}/approve | P7 | /api/recovery/decision/v1/admin/rule-versions/{versionId}/approve | /api/recovery/decision/v1 |
| POST /admin/rule-versions/{versionId}/rollback | P7 | /api/recovery/decision/v1/admin/rule-versions/{versionId}/rollback | /api/recovery/decision/v1 |
| POST /admin/templates | P6 | /api/recovery/comms/v1/admin/templates | /api/recovery/comms/v1 |
| POST /admin/templates/{templateId}/approve | P6 | /api/recovery/comms/v1/admin/templates/{templateId}/approve | /api/recovery/comms/v1 |
| POST /admin/templates/{templateId}/withdraw | P6 | /api/recovery/comms/v1/admin/templates/{templateId}/withdraw | /api/recovery/comms/v1 |
| POST /admin/trackers/{trackerId}/loads | P1 | /api/recovery/source-data/v1/admin/trackers/{trackerId}/loads | /api/recovery/source-data/v1 |
| POST /admin/trackers/{trackerId}/retire | P1 | /api/recovery/source-data/v1/admin/trackers/{trackerId}/retire | /api/recovery/source-data/v1 |
| POST /admin/trackers/{trackerId}/sign-off | P1 | /api/recovery/source-data/v1/admin/trackers/{trackerId}/sign-off | /api/recovery/source-data/v1 |
| POST /admin/workflows/smoke | PLT | POST /admin/workflows/smoke | PLT |
| POST /agent-runs/{runId}/feedback | P10 | /api/recovery/agent/v1/agent-runs/{runId}/feedback | /api/recovery/agent/v1 |
| POST /approvals/{approvalId}/approve | P7 | /api/recovery/decision/v1/approvals/{approvalId}/approve | /api/recovery/decision/v1 |
| POST /approvals/{approvalId}/refuse | P7 | /api/recovery/decision/v1/approvals/{approvalId}/refuse | /api/recovery/decision/v1 |
| POST /approvals/{approvalId}/return | P7 | /api/recovery/decision/v1/approvals/{approvalId}/return | /api/recovery/decision/v1 |
| POST /assets/{assetId}/listings | S5 | /api/recovery/asset/v1/assets/{assetId}/listings | /api/recovery/asset/v1 |
| POST /assets/{assetId}/valuations | S1 | /api/recovery/valuation/v1/assets/{assetId}/valuations | /api/recovery/valuation/v1 |
| POST /assets/{assetKey}/listings | S5 | /api/recovery/asset/v1/assets/{assetKey}/listings | /api/recovery/asset/v1 |
| POST /assets/{assetKey}/valuations | S1 | /api/recovery/valuation/v1/assets/{assetKey}/valuations | /api/recovery/valuation/v1 |
| POST /cases/{caseId}/deviations | S8 | /api/recovery/deviation/v1/cases/{caseId}/deviations | /api/recovery/deviation/v1 |
| POST /cases/{caseId}/documents | P5 | /api/recovery/document/v1/cases/{caseId}/documents | /api/recovery/document/v1 |
| POST /cases/{caseId}/field-captures | P5 | /api/recovery/document/v1/cases/{caseId}/field-captures | /api/recovery/document/v1 |
| POST /cases/{caseId}/generated-documents | P5 | /api/recovery/document/v1/cases/{caseId}/generated-documents | /api/recovery/document/v1 |
| POST /cases/{caseId}/guarantee-claims | S3 | /api/recovery/guarantee/v1/cases/{caseId}/guarantee-claims | /api/recovery/guarantee/v1 |
| POST /cases/{caseId}/instructions | S9 | /api/recovery/partner/v1/cases/{caseId}/instructions | /api/recovery/partner/v1 |
| POST /cases/{caseId}/interactions | P1 | /api/recovery/source-data/v1/cases/{caseId}/interactions | /api/recovery/source-data/v1 |
| POST /cases/{caseId}/legal-actions | S4 | /api/recovery/litigation/v1/cases/{caseId}/legal-actions | /api/recovery/litigation/v1 |
| POST /cases/{caseId}/legal-hold | P3 | /api/recovery/case/v1/cases/{caseId}/legal-hold | /api/recovery/case/v1 |
| POST /cases/{caseId}/messages | P6 | /api/recovery/comms/v1/cases/{caseId}/messages | /api/recovery/comms/v1 |
| POST /cases/{caseId}/notices | P6 | /api/recovery/comms/v1/cases/{caseId}/notices | /api/recovery/comms/v1 |
| POST /cases/{caseId}/route | S1 | /api/recovery/valuation/v1/cases/{caseId}/route | /api/recovery/valuation/v1 |
| POST /cases/{caseId}/transfer | P3 | /api/recovery/case/v1/cases/{caseId}/transfer | /api/recovery/case/v1 |
| POST /cases/{caseId}/treatments | S2 | /api/recovery/treatment/v1/cases/{caseId}/treatments | /api/recovery/treatment/v1 |
| POST /debt-sale-lots | S6 | /api/recovery/debtsale/v1/debt-sale-lots | /api/recovery/debtsale/v1 |
| POST /debt-sale-lots/{lotId}/award | S6 | /api/recovery/debtsale/v1/debt-sale-lots/{lotId}/award | /api/recovery/debtsale/v1 |
| POST /documents/{documentId}/custody | P5 | /api/recovery/document/v1/documents/{documentId}/custody | /api/recovery/document/v1 |
| POST /documents/{documentId}/regenerate | P5 | /api/recovery/document/v1/documents/{documentId}/regenerate | /api/recovery/document/v1 |
| POST /documents/{documentId}/review | P5 | /api/recovery/document/v1/documents/{documentId}/review | /api/recovery/document/v1 |
| POST /documents/{documentId}/versions | P5 | /api/recovery/document/v1/documents/{documentId}/versions | /api/recovery/document/v1 |
| POST /intake-items/{intakeItemId}/resolve | P5 | /api/recovery/document/v1/intake-items/{intakeItemId}/resolve | /api/recovery/document/v1 |
| POST /legal-actions/{legalActionId}/hearings | S4 | /api/recovery/litigation/v1/legal-actions/{legalActionId}/hearings | /api/recovery/litigation/v1 |
| POST /listings/{listingId}/rounds | S5 | /api/recovery/asset/v1/listings/{listingId}/rounds | /api/recovery/asset/v1 |
| POST /notices/{noticeId}/approve | S4 | /api/recovery/litigation/v1/notices/{noticeId}/approve | /api/recovery/litigation/v1 |
| POST /partner/data-room/{lotId}/bids | S6 | /api/recovery/debtsale/v1/partner/data-room/{lotId}/bids | /api/recovery/debtsale/v1 |
| POST /partner/instructions/{instructionId}/accept | S9 | /api/recovery/partner/v1/partner/instructions/{instructionId}/accept | /api/recovery/partner/v1 |
| POST /partner/instructions/{instructionId}/invoices | S9 | /api/recovery/partner/v1/partner/instructions/{instructionId}/invoices | /api/recovery/partner/v1 |
| POST /partner/instructions/{instructionId}/results | S9 | /api/recovery/partner/v1/partner/instructions/{instructionId}/results | /api/recovery/partner/v1 |
| POST /proceeds/{proceedsId}/match | P8 | /api/recovery/payment/v1/proceeds/{proceedsId}/match | /api/recovery/payment/v1 |
| POST /queues/{queueId}/placements | P3 | /api/recovery/case/v1/queues/{queueId}/placements | /api/recovery/case/v1 |
| POST /signature-requests/{requestId}/result | P6 | /api/recovery/comms/v1/signature-requests/{requestId}/result | /api/recovery/comms/v1 |
| POST /treatments/{treatmentId}/credit-result | P2 | /api/recovery/integration/v1/treatments/{treatmentId}/credit-result | /api/recovery/integration/v1 |
| POST /treatments/{treatmentId}/signature-requests | P6 | /api/recovery/comms/v1/treatments/{treatmentId}/signature-requests | /api/recovery/comms/v1 |
| POST /treatments/{treatmentId}/submit | S2 | /api/recovery/treatment/v1/treatments/{treatmentId}/submit | /api/recovery/treatment/v1 |
| POST /write-off-scans | S7 | /api/recovery/writeoff/v1/write-off-scans | /api/recovery/writeoff/v1 |
| POST /write-offs/{writeOffId}/committee-decision | S7 | /api/recovery/writeoff/v1/write-offs/{writeOffId}/committee-decision | /api/recovery/writeoff/v1 |

## Events

| ID | Event | Producer | Topic | Consumers | Numbered in the event catalogue | Source |
| EV-01 | CaseCreated | P3 rwb-case | rwb.case.events.v1 | P10 rwb-agent; S8 rwb-deviation; P9 rwb-reporting | Yes | Arch v5 slide 42, slide 43 |
| EV-02 | CaseAllocated | P3 rwb-case | rwb.case.events.v1 | P9 rwb-reporting | Yes | Arch v5 slide 42, slide 43 |
| EV-03 | CaseAllocationFailed | P3 rwb-case | rwb.case.events.v1 | P3 rwb-case | Yes | Arch v5 slide 42, slide 43 |
| EV-04 | CaseTransferred | P3 rwb-case | rwb.case.events.v1 | P9 rwb-reporting | Yes | Arch v5 slide 42, slide 43 |
| EV-05 | CaseStateChanged | P3 rwb-case | rwb.case.events.v1 | P6 rwb-comms; P9 rwb-reporting | Yes | Arch v5 slide 42, slide 43 |
| EV-06 | DeviationRaised | S8 rwb-deviation | rwb.deviation.events.v1 | P3 rwb-case; P6 rwb-comms; S2 rwb-treatment | Yes | Arch v5 slide 42, slide 43 |
| EV-07 | DeviationCleared | S8 rwb-deviation | rwb.deviation.events.v1 | P3 rwb-case; P6 rwb-comms | Yes | Arch v5 slide 42, slide 43 |
| EV-08 | DecisionRecorded | All 19 services | rwb.decision-record.v1 | P7 rwb-decision; P9 rwb-reporting | Yes | Arch v5 slide 42, slide 43 |
| EV-09 | ApprovalRequested | P7 rwb-decision | rwb.decision.events.v1 | gateway-bff | Yes | Arch v5 slide 42, slide 43 |
| EV-10 | TreatmentApproved | S2 rwb-treatment | rwb.treatment.events.v1 | P6 rwb-comms; P8 rwb-payment | Yes | Arch v5 slide 42, slide 43 |
| EV-11 | TreatmentBooked | P8 rwb-payment | rwb.payment.events.v1 | P3 rwb-case; S2 rwb-treatment | Yes | Arch v5 slide 42, slide 43 |
| EV-12 | PaymentMissed | P8 rwb-payment | rwb.payment.events.v1 | P3 rwb-case; S2 rwb-treatment; P6 rwb-comms | Yes | Arch v5 slide 42, slide 43 |
| EV-13 | NoticeGenerated | P6 rwb-comms | rwb.comms.events.v1 | P7 rwb-decision | Yes | Arch v5 slide 42, slide 43 |
| EV-14 | NoticeDispatched | P6 rwb-comms | rwb.comms.events.v1 | P9 rwb-reporting | Yes | Arch v5 slide 42, slide 43 |
| EV-15 | NoticeDelivered | P6 rwb-comms | rwb.comms.events.v1 | S4 rwb-litigation; S3 rwb-guarantee; P3 rwb-case | Yes | Arch v5 slide 42, slide 43 |
| EV-16 | DocumentStored | P5 rwb-document | rwb.document.events.v1 | P10 rwb-agent; P3 rwb-case | Yes | Arch v5 slide 42, slide 43 |
| EV-17 | DocumentFieldsExtracted | P5 rwb-document | rwb.document.events.v1 | P3 rwb-case | Yes | Arch v5 slide 42, slide 43 |
| EV-18 | TimerDue | PLT platform library | - | NONE | Yes | Arch v5 slide 42, slide 43 |
| EV-19 | TimerBreached | P3 rwb-case | rwb.case.events.v1 | gateway-bff | Yes | Arch v5 slide 42, slide 43 |
| EV-20 | InstructionIssued | S9 rwb-partner | rwb.partner.events.v1 | Partner portal | Yes | Arch v5 slide 42, slide 43 |
| EV-21 | PartnerResultSubmitted | S9 rwb-partner | rwb.partner.events.v1 | S4 rwb-litigation; S5 rwb-asset; P3 rwb-case | Yes | Arch v5 slide 42, slide 43 |
| EV-22 | AssetTakenOn | S5 rwb-asset | rwb.asset.events.v1 | P3 rwb-case; P8 rwb-payment | Yes | Arch v5 slide 42, slide 43 |
| EV-23 | LotAwarded | S6 rwb-debtsale | rwb.debtsale.events.v1 | P3 rwb-case; P8 rwb-payment | Yes | Arch v5 slide 42, slide 43 |
| EV-24 | WriteOffApproved | S7 rwb-writeoff | rwb.writeoff.events.v1 | P3 rwb-case; P8 rwb-payment; P9 rwb-reporting | Yes | Arch v5 slide 42, slide 43 |
| EV-25 | ProceedsMatched | P8 rwb-payment | rwb.payment.events.v1 | P3 rwb-case; S5 rwb-asset; S6 rwb-debtsale; S7 rwb-writeoff; S3 rwb-guarantee | Yes | Arch v5 slide 42, slide 43 |
| EV-26 | AceDataReady | P1 rwb-source-data | rwb.source-data.events.v1 | P3 rwb-case; P8 rwb-payment; S8 rwb-deviation; S7 rwb-writeoff | Yes | Arch v5 slide 42, slide 43 |
| EV-27 | AceDataLate | P1 rwb-source-data | rwb.source-data.events.v1 | gateway-bff | Yes | Arch v5 slide 42, slide 43 |
| EV-28 | AgentRunCompleted | P10 rwb-agent | rwb.agent.events.v1 | P7 rwb-decision; P5 rwb-document; S8 rwb-deviation | Yes | Arch v5 slide 42, slide 43 |
| EV-29 | CaseEvent | P3 rwb-case | rwb.case.events.v1 | NONE | Yes | Arch v5 slide 42, slide 43 |
| EV-30 | RulePackageInForce | P7 rwb-decision | rwb.decision.events.v1 | P3 rwb-case; S1 rwb-valuation; S2 rwb-treatment; P8 rwb-payment | Yes | Arch v5 slide 42, slide 43 |
| - | RouteDecided | S1 rwb-valuation | rwb.valuation.events.v1 | P3 rwb-case | No | Arch v5 slide 43 (not numbered) |
| - | AssetSold | S5 rwb-asset | rwb.asset.events.v1 | P8 rwb-payment; P3 rwb-case | No | Arch v5 slide 43 (not numbered) |
| - | JudgmentRecorded | S4 rwb-litigation | rwb.litigation.events.v1 | S5 rwb-asset; P3 rwb-case | No | Arch v5 slide 43 (not numbered) |
| - | AuctionResult | S4 rwb-litigation | rwb.litigation.events.v1 | S5 rwb-asset; P3 rwb-case | No | Arch v5 slide 43 (not numbered) |
| - | TreatmentClosed | S2 rwb-treatment | rwb.treatment.events.v1 | P3 rwb-case; P9 rwb-reporting | No | Arch v5 slide 43 (not numbered) |
| - | GuaranteeClaimFiled | S3 rwb-guarantee | rwb.guarantee.events.v1 | P3 rwb-case; P9 rwb-reporting | No | Arch v5 slide 43 (not numbered) |
| - | GuaranteeClaimSettled | S3 rwb-guarantee | rwb.guarantee.events.v1 | P3 rwb-case; P9 rwb-reporting | No | Arch v5 slide 43 (not numbered) |
| - | AccountsTransferred | S6 rwb-debtsale | rwb.debtsale.events.v1 | P3 rwb-case; P9 rwb-reporting | No | Arch v5 slide 43 (not numbered) |
| - | AccessPolicyChanged | P4 rwb-access | rwb.access.events.v1 | All 19 services | No | Arch v5 slide 43 (not numbered) |
| - | DoaLimitChanged | P4 rwb-access | rwb.access.events.v1 | All 19 services | No | Arch v5 slide 43 (not numbered) |
| - | FileDelivered | P2 rwb-integration | rwb.integration.events.v1 | The requesting service | No | Arch v5 slide 43 (not numbered) |
| - | FileFailed | P2 rwb-integration | rwb.integration.events.v1 | The requesting service | No | Arch v5 slide 43 (not numbered) |
| - | ApprovalDecided | P7 rwb-decision | rwb.decision.events.v1 | Not specified in the source documents (CG-B-ARCH-CON-4; ASM-B-ARCH-CON-4) | No | Arch v5 slide 43 (not numbered) |
| - | ReportPublished | P9 rwb-reporting | rwb.reporting.events.v1 | Not specified in the source documents (CG-B-ARCH-CON-4; ASM-B-ARCH-CON-4) | No | Arch v5 slide 43 (not numbered) |

## Temporal contracts

| Type | Name | Owner | Task queue | Contract artefact | Consumers | Source |
| Workflow | AgentRunWorkflow | P10 rwb-agent | rwb-agent | Activity contract jar | None named in the sources | Ownership Map v1, Workflows and activities |
| Workflow | CaseWorkflow | P3 rwb-case | rwb-case | Activity contract jar | None named in the sources | Ownership Map v1, Workflows and activities |
| Workflow | DocumentIntakeWorkflow | P5 rwb-document | rwb-document | Activity contract jar | None named in the sources | Ownership Map v1, Workflows and activities |
| Workflow | NoticeDispatchWorkflow | P6 rwb-comms | rwb-comms | Activity contract jar | None named in the sources | Ownership Map v1, Workflows and activities |
| Workflow | ApprovalWorkflow | P7 rwb-decision | rwb-decision | Activity contract jar | S3 rwb-guarantee; S4 rwb-litigation; S5 rwb-asset; S6 rwb-debtsale | Ownership Map v1, Workflows and activities |
| Workflow | PlatformSmokeWorkflow | PLT platform library | - | Activity contract jar | None named in the sources | Ownership Map v1, Workflows and activities |
| Workflow | RouteDecisionWorkflow | S1 rwb-valuation | rwb-valuation | Activity contract jar | P3 rwb-case | Ownership Map v1, Workflows and activities |
| Workflow | TreatmentWorkflow | S2 rwb-treatment | rwb-treatment | Activity contract jar | None named in the sources | Ownership Map v1, Workflows and activities |
| Workflow | GuaranteeClaimWorkflow | S3 rwb-guarantee | rwb-guarantee | Activity contract jar | P3 rwb-case | Ownership Map v1, Workflows and activities |
| Workflow | LitigationWorkflow | S4 rwb-litigation | rwb-litigation | Activity contract jar | P3 rwb-case | Ownership Map v1, Workflows and activities |
| Workflow | AssetDisposalWorkflow | S5 rwb-asset | rwb-asset | Activity contract jar | P3 rwb-case | Ownership Map v1, Workflows and activities |
| Workflow | DebtSaleWorkflow | S6 rwb-debtsale | rwb-debtsale | Activity contract jar | P3 rwb-case | Ownership Map v1, Workflows and activities |
| Workflow | WriteOffWorkflow | S7 rwb-writeoff | rwb-writeoff | Activity contract jar | P3 rwb-case | Ownership Map v1, Workflows and activities |
| Workflow | DeviationWorkflow | S8 rwb-deviation | rwb-deviation | Activity contract jar | P3 rwb-case | Ownership Map v1, Workflows and activities |
| Workflow | InstructionWorkflow | S9 rwb-partner | rwb-partner | Activity contract jar | None named in the sources | Ownership Map v1, Workflows and activities |

## Jobs

| Job | Owner | Contract form | Source |
| JOB-01 | P1 rwb-source-data | none (retired under D-RCV-35; ACE ingestion, read through the rwb-source-data ACE view contract) | Arch v5 slide 44; Ownership Map v1, Jobs |
| JOB-02 | P3 rwb-case | event-started workflow (DailyCaseRun in rwb-case) | Arch v5 slide 44; Ownership Map v1, Jobs |
| JOB-03 | P3 rwb-case | event-started workflow (DailyCaseRun step in rwb-case) | Arch v5 slide 44; Ownership Map v1, Jobs |
| JOB-04 | P1 rwb-source-data | event-started workflow (AceIngestCheck and reconciliation in rwb-source-data) | Arch v5 slide 44; Ownership Map v1, Jobs |
| JOB-05 | PLT platform library | no Temporal Schedule (durable timers inside each workflow; the 5-minute timer check is retired) | Arch v5 slide 44; Ownership Map v1, Jobs |
| JOB-06 | P3 rwb-case | Temporal Schedule rebalancing in rwb-case | Arch v5 slide 44; Ownership Map v1, Jobs |
| JOB-07 | P8 rwb-payment | event-started workflow (matchPayments in rwb-payment) | Arch v5 slide 44; Ownership Map v1, Jobs |
| JOB-08 | P8 rwb-payment | event-started workflow (confirmBookings in rwb-payment) | Arch v5 slide 44; Ownership Map v1, Jobs |
| JOB-09 | P1 rwb-source-data | none (retired under D-RCV-35; ACE ingestion, read through the rwb-source-data ACE view contract) | Arch v5 slide 44; Ownership Map v1, Jobs |
| JOB-10 | P6 rwb-comms | Temporal Schedule WIN notices in rwb-comms (Airflow file window; rwb-integration delivers the file) | Arch v5 slide 44; Ownership Map v1, Jobs |
| JOB-11 | PLT platform library | no Temporal Schedule (outbox relay to Kafka in every service) | Arch v5 slide 44; Ownership Map v1, Jobs |
| JOB-12 | P5 rwb-document | event-started workflow (DocumentIntakeWorkflow in rwb-document, KEDA workers) | Arch v5 slide 44; Ownership Map v1, Jobs |
| JOB-13 | P7 rwb-decision | no Temporal Schedule (continuous DecisionRecorded ingest from Kafka in rwb-decision) | Arch v5 slide 44; Ownership Map v1, Jobs |
| JOB-14 | P7 rwb-decision | Temporal Schedule chain check in rwb-decision | Arch v5 slide 44; Ownership Map v1, Jobs |
| JOB-15 | P9 rwb-reporting | Airflow trigger (buildRegulatoryExtract in rwb-reporting; no data lake) | Arch v5 slide 44; Ownership Map v1, Jobs |
| JOB-16 | S7 rwb-writeoff | Temporal Schedule write-off scan in rwb-writeoff | Arch v5 slide 44; Ownership Map v1, Jobs |
| JOB-17 | P5 rwb-document | Temporal Schedule retention in rwb-document | Arch v5 slide 44; Ownership Map v1, Jobs |
| JOB-18 | P4 rwb-access | Temporal Schedule access review list in rwb-access | Arch v5 slide 44; Ownership Map v1, Jobs |
| JOB-19 | S5 rwb-asset | Temporal Schedule re-appraisal in rwb-asset | Arch v5 slide 44; Ownership Map v1, Jobs |
| JOB-20 | P7 rwb-decision | Temporal Schedule rule promote in rwb-decision | Arch v5 slide 44; Ownership Map v1, Jobs |
| JOB-21 | PLT platform library | Temporal Schedule stuck workflow scan in rwb-platform (PLT) | Arch v5 slide 44; Ownership Map v1, Jobs |
| JOB-22 | PLT platform library | Temporal Schedule platform smoke in rwb-platform (PLT), starts PlatformSmokeWorkflow | Arch v5 slide 44; Ownership Map v1, Jobs |

## Resources owned

| Table | Owner | Schema | Basis |
| account_ext | P1 | rwb_source_data | Ownership Map v1, Tables sheet |
| agent_alert | P10 | rwb_agent | Ownership Map v1, Tables sheet |
| agent_evaluation | P10 | rwb_agent | Ownership Map v1, Tables sheet |
| agent_evaluation_run | P10 | rwb_agent | Ownership Map v1, Tables sheet |
| agent_feedback | P10 | rwb_agent | Ownership Map v1, Tables sheet |
| agent_policy | P10 | rwb_agent | Ownership Map v1, Tables sheet |
| agent_prompt | P10 | rwb_agent | Ownership Map v1, Tables sheet |
| agent_run | P10 | rwb_agent | Ownership Map v1, Tables sheet |
| agent_sample | P10 | rwb_agent | Ownership Map v1, Tables sheet |
| approval | P7 | rwb_decision | Ownership Map v1, Tables sheet |
| asset_sale | S5 | rwb_asset | Ownership Map v1, Tables sheet |
| assignment | P3 | rwb_case | Ownership Map v1, Tables sheet |
| case_account | P3 | rwb_case | Ownership Map v1, Tables sheet |
| case_document_check | P5 | rwb_document | Ownership Map v1, Tables sheet |
| case_entry_exclusion | P3 | rwb_case | Ownership Map v1, Tables sheet |
| case_list_row | P1 | rwb_source_data | Ownership Map ruling; ASM-A6-tables-2 |
| case_party | P3 | rwb_case | Ownership Map v1, Tables sheet |
| contact_point_ext | P1 | rwb_source_data | Ownership Map v1, Tables sheet |
| data_contract | P1 | rwb_source_data | Ownership Map v1, Tables sheet |
| data_product | P1 | rwb_source_data | Ownership Map v1, Tables sheet |
| data_product_access | P1 | rwb_source_data | Ownership Map v1, Tables sheet |
| data_product_load | P1 | rwb_source_data | Ownership Map v1, Tables sheet |
| debt_sale_account | S6 | rwb_debtsale | Ownership Map v1, Tables sheet |
| debt_sale_lot | S6 | rwb_debtsale | Ownership Map v1, Tables sheet |
| decision_log_entry | P7 | rwb_decision | Ownership Map v1, Tables sheet |
| delegation_limit | P4 | rwb_access | Ownership Map ruling; ASM-A6-tables-4 |
| deviation | S8 | rwb_deviation | Ownership Map v1, Tables sheet |
| document | P5 | rwb_document | Ownership Map v1, Tables sheet |
| document_checklist_item | P5 | rwb_document | Ownership Map v1, Tables sheet |
| document_custody | P5 | rwb_document | Ownership Map v1, Tables sheet |
| document_field | P5 | rwb_document | Ownership Map v1, Tables sheet |
| document_hub_parameter | P5 | rwb_document | Ownership Map v1, Tables sheet |
| document_intake | P5 | rwb_document | Ownership Map v1, Tables sheet |
| document_text | P5 | rwb_document | Ownership Map v1, Tables sheet |
| document_type | P5 | rwb_document | Ownership Map v1, Tables sheet |
| dp_guarantee_claim | P1 | rwb_source_data | Ownership Map ruling; ASM-A6-tables-14 |
| dp_treatment | P1 | rwb_source_data | Ownership Map ruling; ASM-A6-tables-14 |
| efs_ledger_outcome | P1 | rwb_source_data | Ownership Map ruling; ASM-A6-tables-1 |
| feature_flag | PLT | every rwb_* schema | Ownership Map ruling; ASM-A6-tables-7 |
| feature_flag_change | PLT | every rwb_* schema | Ownership Map ruling; ASM-A6-tables-7 |
| guarantee_claim | S3 | rwb_guarantee | Ownership Map v1, Tables sheet |
| hearing | S4 | rwb_litigation | Ownership Map v1, Tables sheet |
| idempotency_key | PLT | every rwb_* schema | Ownership Map ruling; ASM-A6-tables-8 |
| interaction | P1 | rwb_source_data | Ownership Map ruling; ASM-A6-tables-1 |
| interface_config | P2 | rwb_integration | Ownership Map v1, Tables sheet |
| job_catalog | P2 | rwb_integration | Ownership Map ruling; ASM-A6-tables-9 |
| lake_copy_watermark | P1 | rwb_source_data | Ownership Map ruling; ASM-A6-tables-13 |
| legal_action | S4 | rwb_litigation | Ownership Map v1, Tables sheet |
| listing | S5 | rwb_asset | Ownership Map v1, Tables sheet |
| lov_value | P3 | rwb_case | Ownership Map ruling; ASM-A6-tables-5 |
| masking_rule | P4 | rwb_access | Ownership Map v1, Tables sheet |
| measure_definition | P9 | rwb_reporting | Ownership Map v1, Tables sheet |
| measure_publish | P9 | rwb_reporting | Ownership Map v1, Tables sheet |
| measure_snapshot | P9 | rwb_reporting | Ownership Map v1, Tables sheet |
| merge_field | P6 | rwb_comms | Ownership Map v1, Tables sheet |
| notice | P6 | rwb_comms | Ownership Map v1, Tables sheet |
| outbound_item | P2 | rwb_integration | Ownership Map v1, Tables sheet |
| outbox_delivery | PLT | every rwb_* schema | Ownership Map ruling; ASM-A6-tables-8 |
| outbox_event | PLT | every rwb_* schema | Ownership Map ruling; ASM-A6-tables-8 |
| parameter_catalog | P3 | rwb_case | Ownership Map v1, Tables sheet |
| parameter_value | P3 | rwb_case | Ownership Map v1, Tables sheet |
| partner | S9 | rwb_partner | Ownership Map v1, Tables sheet |
| partner_instruction | S9 | rwb_partner | Ownership Map v1, Tables sheet |
| partner_user | S9 | rwb_partner | Ownership Map ruling; ASM-A6-tables-6 |
| party_ext | P1 | rwb_source_data | Ownership Map v1, Tables sheet |
| permission | P4 | rwb_access | Ownership Map v1, Tables sheet |
| proceeds | P8 | rwb_payment | Ownership Map v1, Tables sheet |
| processed_event | PLT | every rwb_* schema | Ownership Map ruling; ASM-A6-tables-8 |
| queue | P3 | rwb_case | Ownership Map v1, Tables sheet |
| queue_measure | P3 | rwb_case | Ownership Map v1, Tables sheet |
| queue_member | P3 | rwb_case | Ownership Map v1, Tables sheet |
| reconciliation_result | P1 | rwb_source_data | Ownership Map v1, Tables sheet |
| recovery_case | P3 | rwb_case | Ownership Map v1, Tables sheet |
| reference_row | P3 | rwb_case | Ownership Map v1, Tables sheet |
| reference_version | P3 | rwb_case | Ownership Map v1, Tables sheet |
| retention_action | P5 | rwb_document | Ownership Map v1, Tables sheet |
| retention_rule | P5 | rwb_document | Ownership Map ruling; ASM-A6-tables-10 |
| role | P4 | rwb_access | Ownership Map v1, Tables sheet |
| role_conflict | P4 | rwb_access | Ownership Map v1, Tables sheet |
| rule_package | P7 | rwb_decision | Ownership Map ruling; ASM-A6-tables-3 |
| rule_package_version | P7 | rwb_decision | Ownership Map ruling; ASM-A6-tables-3 |
| rule_row | P7 | rwb_decision | Ownership Map ruling; ASM-A6-tables-3 |
| rule_test_case | P7 | rwb_decision | Ownership Map ruling; ASM-A6-tables-3 |
| signature_request | P5 | rwb_document | Ownership Map ruling; ASM-A6-tables-11 |
| sys_field_version | P1 | rwb_source_data | Ownership Map v1, Tables sheet |
| sys_fields | P1 | rwb_source_data | Ownership Map v1, Tables sheet |
| sys_objects | P1 | rwb_source_data | Ownership Map v1, Tables sheet |
| task | P3 | rwb_case | Ownership Map v1, Tables sheet |
| template | P6 | rwb_comms | Ownership Map v1, Tables sheet |
| timer | P3 | rwb_case | Ownership Map ruling; ASM-A6-tables-12 |
| treatment | S2 | rwb_treatment | Ownership Map v1, Tables sheet |
| valuation_ext | P1 | rwb_source_data | Ownership Map ruling; ASM-A6-tables-15 |
| write_off | S7 | rwb_writeoff | Ownership Map v1, Tables sheet |

## Conformance

| # | Contract rule | Tested by |
| 1 | The provider publishes its OpenAPI 3.1, AsyncAPI 3.0 and activity contract jar before the implementation story starts | Contract publication gate in the pipeline |
| 2 | Every operation in section 6 exists in the published contract, under the service's own base path | OpenAPI diff against the Ownership Map Endpoints sheet |
| 3 | Every event the service publishes is in its AsyncAPI document, on its own topic, with CloudEvents 1.0 binary mode and key caseId | AsyncAPI validation plus a schema registry check |
| 4 | Every event the service consumes is deduplicated in processed_event, in the same transaction as the change | Inbox test |
| 5 | Every activity and child workflow the service calls is declared in the provider's contract jar; no service imports another service's code | Activity contract test |
| 6 | No REST chain longer than one hop; route services reach shared capabilities through Temporal | Contract test plus trace-depth check |
| 7 | No cross-schema read, join, view or foreign key; the boundary test fails the build on any violation | Architecture test |
| 8 | Every POST and PATCH is idempotent through Idempotency-Key, and every consumer of the same key returns the first result | Idempotency test |
| 9 | Error responses follow RFC 9457 for REST and the error code form for events | Contract example test |
| 10 | The provider's fake serves every operation and every event of its contract | Fake conformance test in the consumer build |
| 11 | The pair is proved end to end in the integration story of the later wave | RWB-ITG-W<n> harness |
| 12 | The contract document is registered in section 6 with its version | Registration check on the CON story |

## Open points

| ID | Point | Effect in this catalogue | Owner role |
| CG-B-ARCH-CON-1 | No earlier Service Contract Catalog exists, so v1 carries no inherited sections, IDs, numbers or dates | Version 1, status Draft; the change-log row is the first | Delivery lead |
| CG-B-ARCH-CON-2 | The Ownership Map Endpoints sheet holds the monolith operations of API Specification v4, while Architecture v5 slide 41 states a per-service base path; the per-service paths and payloads are written in API Specification v5 | Section 6 lists the operation per owning service under its base path and leaves the final path to API Specification v5 | Solution architect |
| CG-B-ARCH-CON-3 | The coordinates of the activity contract jars (groupId, artifactId, version) are not specified | Section 7.1 states the artefact and the package root, and leaves the coordinates open | Tech lead |
| CG-B-ARCH-CON-4 | The event catalogue does not name the consumers of ApprovalDecided or ReportPublished | The two rows state Not specified in the source documents | Solution architect |
| CG-B-ARCH-CON-5 | The schema registry product and its deployment are not specified; only the BACKWARD compatibility rule is stated | Section 7.2 states the compatibility rule and not the product | Platform architect |
| CG-B-ARCH-CON-6 | The slide 13 rule that route services reach shared capabilities through Temporal sits beside REST cells from S1, S7 and S8 to rwb-source-data | Section 8.3 reads the rule as covering the five shared capabilities named in the slide note; the rwb-source-data reads stay REST | Solution architect |
| CG-B-ARCH-CON-7 | The request and response content of the Enterprise AI private endpoint (INT-23) is not specified | Section 8.4 names the edge and the stub, not a payload | Solution architect |
| CG-B-ARCH-CON-8 | The call-type matrix marks S5 to P6 as Temporal, but the asset contract on Architecture v5 slide 19 names no communications interface and no other slide supplies one | Section 6.15 carries the placeholder in its Temporal row and no interface is invented | Solution architect |

## Change log

| Version | Date | Change | Detail |
| 1 | 22 November 2026 | D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash | First Service Contract Catalog: contract model, call-type matrix, contract inventory, contract by service, shared platform contracts, dependency classes, contract tests and change control |

