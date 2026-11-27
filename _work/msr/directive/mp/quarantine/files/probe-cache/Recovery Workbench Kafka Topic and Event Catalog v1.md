## Sheet: Read me

| SCB Collections and Recovery. Henka Group, 22 November 2026. |
|---|
| (C) Siam Commercial Bank and Henka Pte Ltd |
| Recovery Workbench Kafka Topic and Event Catalog v1. Decision D-RCV-60. A new document of the realignment; it has no earlier version. |
| The one place where a service finds the name of its topic, of its event types and of its dead-letter topic, the services that read them, and the envelope and delivery rules that every event follows. |
| Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. |
| Status: Draft. This document is issued with no approval recorded (ASM-0196). |
| Change log |
| v1, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |
| No earlier version exists. The event table it replaces as the contract is Recovery Workbench Event and Messaging Design v4, 16 November 2026, D-RCV-36, which is carried forward in Event and Messaging Design v5. |
| What this version holds |
| Topics: 20 event topics, one per service plus the shared rwb.decision-record.v1, with owner, wave, settings, the event types carried and the consumer services. |
| Retry topics: three per event topic, one per window of 1 min, 10 min and 1 h, 60 in the set, with the window, the owner and the order of the ladder. |
| Dead-letter topics: 20, one per event topic, with the alert and the replay path. |
| Events: 43 event types, with the EV row of the event table where one exists, the event type name, the topic, the owner, the payload and the consumers. |
| Not on Kafka: the entries that are not plain topic events (the retired TimerDue, the CaseEvent signal and the two ACE batch events that are exempt from the transaction rule), and why. |
| Envelope, Outbox and inbox, Delivery rules: the message format and the delivery behaviour every producer and consumer implements. |
| ACLs: the write and read list of every service principal, derived from the producer and consumer columns of the event catalogue. |
| Traceability: the decision, the pattern and the slide each part of the catalogue implements. |
| Counts |
| 100 topics: 20 event topics, 60 retry topics and 20 dead-letter topics. |
| 43 event types: 28 carry an EV row of the v4 event table and 15 exist only in the Architecture v5 service catalogue. |
| 19 service principals plus gateway-bff; every service writes its own topic and the shared rwb.decision-record.v1. |
| 12 partitions, replication factor 3, 7-day retention and record key caseId on every event topic. |
| Sources |
| Recovery Workbench Architecture v5 Text Extract v1, slides 9, 11, 20, 21, 22, 35, 41, 42, 43 and 44. |
| Recovery Workbench Event and Messaging Design v4 (16 November 2026, D-RCV-36) and its next version, Event and Messaging Design v5 (22 November 2026, D-RCV-60). |
| Recovery Workbench Microservice Ownership Map v1, sheets Services and Events. |
| Recovery Workbench Temporal and Drools Design Text Extract v1, slides 14 and 15. |
| RWB-PLT-N002-INF (Kafka topics, retry and dead-letter topics and ACLs) and RWB-PLT-N008-INF (schema registry with BACKWARD compatibility). |
| Template and Rules §R4 (naming), §R5.5 DP-09, DP-14 and DP-03 (patterns), §R8.1 and §R8.2 (header and versioning), §R9 (placeholder). |
| Candidate gap rows GAP-0120 to GAP-0131 and candidate assumption rows ASM-0196 to ASM-0209 are written by this work package; step D1 renumbers them. |

## Sheet: Topics

| Recovery event topics |  |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Settings of an event topic: 12 partitions, replication factor 3, 7-day retention, cleanup policy delete, record key caseId and CloudEvents 1.0 in binary mode (Arch v5 slide 9). The shared topic carries no settings of its own in any source (GAP-0125; ASM-0202). |  |  |  |  |  |  |  |  |  |  |  |
| Topic | Kind | Owner code | Owner service | Wave | Partitions | Replication | Retention | Key | Event types carried | Consumers | Basis |
| rwb.source-data.events.v1 | Event topic | P1 | rwb-source-data | 1 | 12 | 3 | 7 days | caseId | AceDataReady, AceDataLate | rwb-case, rwb-payment, rwb-deviation, rwb-writeoff, alerts, gateway-bff | Arch v5 slides 9 and 41; Ownership Map sheet Services |
| rwb.integration.events.v1 | Event topic | P2 | rwb-integration | 1 | 12 | 3 | 7 days | caseId | FileDelivered, FileFailed | requesting service | Arch v5 slides 9 and 41; Ownership Map sheet Services |
| rwb.case.events.v1 | Event topic | P3 | rwb-case | 1 | 12 | 3 | 7 days | caseId | CaseCreated, CaseAllocated, CaseAllocationFailed, CaseTransferred, CaseStateChanged, TimerBreached | rwb-agent, rwb-deviation, rwb-reporting, rwb-case, rwb-comms, gateway-bff | Arch v5 slides 9 and 41; Ownership Map sheet Services |
| rwb.access.events.v1 | Event topic | P4 | rwb-access | 1 | 12 | 3 | 7 days | caseId | AccessPolicyChanged, DoaLimitChanged | all (cache refresh) | Arch v5 slides 9 and 41; Ownership Map sheet Services |
| rwb.document.events.v1 | Event topic | P5 | rwb-document | 1 | 12 | 3 | 7 days | caseId | DocumentStored, DocumentFieldsExtracted | rwb-agent, rwb-case | Arch v5 slides 9 and 41; Ownership Map sheet Services |
| rwb.comms.events.v1 | Event topic | P6 | rwb-comms | 1 | 12 | 3 | 7 days | caseId | NoticeGenerated, NoticeDispatched, NoticeDelivered | rwb-decision, rwb-reporting, rwb-litigation, rwb-guarantee, rwb-case | Arch v5 slides 9 and 41; Ownership Map sheet Services |
| rwb.decision.events.v1 | Event topic | P7 | rwb-decision | 1 | 12 | 3 | 7 days | caseId | ApprovalRequested, RulePackageInForce, ApprovalDecided | gateway-bff, rwb-case, rwb-valuation, rwb-treatment, rwb-payment, open (ApprovalDecided; GAP-0128; ASM-0205) | Arch v5 slides 9 and 41; Ownership Map sheet Services |
| rwb.payment.events.v1 | Event topic | P8 | rwb-payment | 2 | 12 | 3 | 7 days | caseId | TreatmentBooked, PaymentMissed, ProceedsMatched | rwb-case, rwb-treatment, rwb-comms, rwb-asset, rwb-debtsale, rwb-writeoff, rwb-guarantee | Arch v5 slides 9 and 41; Ownership Map sheet Services |
| rwb.reporting.events.v1 | Event topic | P9 | rwb-reporting | 1 | 12 | 3 | 7 days | caseId | ReportPublished | open (ReportPublished; GAP-0128; ASM-0205) | Arch v5 slides 9 and 41; Ownership Map sheet Services |
| rwb.agent.events.v1 | Event topic | P10 | rwb-agent | 1 | 12 | 3 | 7 days | caseId | AgentRunCompleted | rwb-decision, rwb-document, rwb-deviation | Arch v5 slides 9 and 41; Ownership Map sheet Services |
| rwb.valuation.events.v1 | Event topic | S1 | rwb-valuation | 3 | 12 | 3 | 7 days | caseId | RouteDecided | rwb-case | Arch v5 slides 9 and 41; Ownership Map sheet Services |
| rwb.treatment.events.v1 | Event topic | S2 | rwb-treatment | 2 | 12 | 3 | 7 days | caseId | TreatmentApproved, TreatmentClosed | rwb-comms, rwb-payment, rwb-case, rwb-reporting | Arch v5 slides 9 and 41; Ownership Map sheet Services |
| rwb.guarantee.events.v1 | Event topic | S3 | rwb-guarantee | 3 | 12 | 3 | 7 days | caseId | GuaranteeClaimFiled, GuaranteeClaimSettled | rwb-case, rwb-reporting | Arch v5 slides 9 and 41; Ownership Map sheet Services |
| rwb.litigation.events.v1 | Event topic | S4 | rwb-litigation | 3 | 12 | 3 | 7 days | caseId | LawsuitFiled, JudgmentRecorded, AuctionResult | open (LawsuitFiled; GAP-0128; ASM-0205), rwb-asset, rwb-case | Arch v5 slides 9 and 41; Ownership Map sheet Services |
| rwb.asset.events.v1 | Event topic | S5 | rwb-asset | 2 | 12 | 3 | 7 days | caseId | AssetTakenOn, AssetSold | rwb-case, rwb-payment | Arch v5 slides 9 and 41; Ownership Map sheet Services |
| rwb.debtsale.events.v1 | Event topic | S6 | rwb-debtsale | 3 | 12 | 3 | 7 days | caseId | LotAwarded, AccountsTransferred | rwb-case, rwb-payment, rwb-reporting | Arch v5 slides 9 and 41; Ownership Map sheet Services |
| rwb.writeoff.events.v1 | Event topic | S7 | rwb-writeoff | 4 | 12 | 3 | 7 days | caseId | WriteOffApproved | rwb-case, rwb-payment, rwb-reporting | Arch v5 slides 9 and 41; Ownership Map sheet Services |
| rwb.deviation.events.v1 | Event topic | S8 | rwb-deviation | 2 | 12 | 3 | 7 days | caseId | DeviationRaised, DeviationCleared | rwb-case, rwb-comms, rwb-treatment | Arch v5 slides 9 and 41; Ownership Map sheet Services |
| rwb.partner.events.v1 | Event topic | S9 | rwb-partner | 4 | 12 | 3 | 7 days | caseId | InstructionIssued, PartnerResultSubmitted | partner portal, rwb-litigation, rwb-asset, rwb-case | Arch v5 slides 9 and 41; Ownership Map sheet Services |
| rwb.decision-record.v1 | Shared event topic | P7 | shared by the 19 services | 0 | Not specified in the source documents (GAP-0125; ASM-0202) | Not specified in the source documents (GAP-0125; ASM-0202) | Not specified in the source documents (GAP-0125; ASM-0202) | Not specified in the source documents (GAP-0125; ASM-0202) | DecisionRecorded | rwb-decision, rwb-reporting | Arch v5 slides 20 and 42 row 08; Ownership Map sheet Events row EV-08 |

## Sheet: Retry topics

| Retry topics: three per event topic, 60 in the set |  |  |  |  |  |
|---|---|---|---|---|---|
| Architecture v5 fixes three retry windows, 1 min, 10 min and 1 h, and RWB-PLT-N002-INF counts three retry topics per event topic. No source names a retry topic, so the name is left to the platform story and is not written here (GAP-0123; ASM-0200); a consumer binds to the retry topics through the outbox and inbox library and never by name. |  |  |  |  |  |
| Window | Topics in the set | When the record moves | Partitions | Owner | What it is for |
| 1 min | 20 | 1 min after the first failure | Same as its event topic | Owner of the event topic | First retry window of a record that a consumer failed. |
| 10 min | 20 | 10 min after the first failure | Same as its event topic | Owner of the event topic | Second retry window. |
| 1 h | 20 | 1 h after the first failure | Same as its event topic | Owner of the event topic | Third and last retry window; after it the record goes to the dead-letter topic. |
| Total topics in the set: 20 event topics + 60 retry topics + 20 dead-letter topics = 100 (RWB-PLT-N002-INF section 12.9). |  |  |  |  |  |

## Sheet: Dead-letter topics

| Dead-letter topics: 20, one per event topic |  |  |  |  |  |  |
|---|---|---|---|---|---|---|
| A record that fails the three retry windows goes to the dead-letter topic of its event topic, one alert is raised and the replay tool puts it back after the cause is fixed (Arch v5 slide 22). The .dlt suffix is the one the source gives and the name is derived from it (ASM-0201); replication and retention are not stated by any source (GAP-0124). |  |  |  |  |  |  |
| Dead-letter topic | Event topic it serves | Owner code | Partitions | Replication and retention | Alert and replay | Basis |
| rwb.source-data.events.v1.dlt | rwb.source-data.events.v1 | P1 | Same as its event topic (12) | Not specified in the source documents (GAP-0124; ASM-0201) | One alert per record; the replay tool is the recovery path | Arch v5 slides 9 and 22 ('.dlt'); RWB-PLT-N002-INF AC2 |
| rwb.integration.events.v1.dlt | rwb.integration.events.v1 | P2 | Same as its event topic (12) | Not specified in the source documents (GAP-0124; ASM-0201) | One alert per record; the replay tool is the recovery path | Arch v5 slides 9 and 22 ('.dlt'); RWB-PLT-N002-INF AC2 |
| rwb.case.events.v1.dlt | rwb.case.events.v1 | P3 | Same as its event topic (12) | Not specified in the source documents (GAP-0124; ASM-0201) | One alert per record; the replay tool is the recovery path | Arch v5 slides 9 and 22 ('.dlt'); RWB-PLT-N002-INF AC2 |
| rwb.access.events.v1.dlt | rwb.access.events.v1 | P4 | Same as its event topic (12) | Not specified in the source documents (GAP-0124; ASM-0201) | One alert per record; the replay tool is the recovery path | Arch v5 slides 9 and 22 ('.dlt'); RWB-PLT-N002-INF AC2 |
| rwb.document.events.v1.dlt | rwb.document.events.v1 | P5 | Same as its event topic (12) | Not specified in the source documents (GAP-0124; ASM-0201) | One alert per record; the replay tool is the recovery path | Arch v5 slides 9 and 22 ('.dlt'); RWB-PLT-N002-INF AC2 |
| rwb.comms.events.v1.dlt | rwb.comms.events.v1 | P6 | Same as its event topic (12) | Not specified in the source documents (GAP-0124; ASM-0201) | One alert per record; the replay tool is the recovery path | Arch v5 slides 9 and 22 ('.dlt'); RWB-PLT-N002-INF AC2 |
| rwb.decision.events.v1.dlt | rwb.decision.events.v1 | P7 | Same as its event topic (12) | Not specified in the source documents (GAP-0124; ASM-0201) | One alert per record; the replay tool is the recovery path | Arch v5 slides 9 and 22 ('.dlt'); RWB-PLT-N002-INF AC2 |
| rwb.payment.events.v1.dlt | rwb.payment.events.v1 | P8 | Same as its event topic (12) | Not specified in the source documents (GAP-0124; ASM-0201) | One alert per record; the replay tool is the recovery path | Arch v5 slides 9 and 22 ('.dlt'); RWB-PLT-N002-INF AC2 |
| rwb.reporting.events.v1.dlt | rwb.reporting.events.v1 | P9 | Same as its event topic (12) | Not specified in the source documents (GAP-0124; ASM-0201) | One alert per record; the replay tool is the recovery path | Arch v5 slides 9 and 22 ('.dlt'); RWB-PLT-N002-INF AC2 |
| rwb.agent.events.v1.dlt | rwb.agent.events.v1 | P10 | Same as its event topic (12) | Not specified in the source documents (GAP-0124; ASM-0201) | One alert per record; the replay tool is the recovery path | Arch v5 slides 9 and 22 ('.dlt'); RWB-PLT-N002-INF AC2 |
| rwb.valuation.events.v1.dlt | rwb.valuation.events.v1 | S1 | Same as its event topic (12) | Not specified in the source documents (GAP-0124; ASM-0201) | One alert per record; the replay tool is the recovery path | Arch v5 slides 9 and 22 ('.dlt'); RWB-PLT-N002-INF AC2 |
| rwb.treatment.events.v1.dlt | rwb.treatment.events.v1 | S2 | Same as its event topic (12) | Not specified in the source documents (GAP-0124; ASM-0201) | One alert per record; the replay tool is the recovery path | Arch v5 slides 9 and 22 ('.dlt'); RWB-PLT-N002-INF AC2 |
| rwb.guarantee.events.v1.dlt | rwb.guarantee.events.v1 | S3 | Same as its event topic (12) | Not specified in the source documents (GAP-0124; ASM-0201) | One alert per record; the replay tool is the recovery path | Arch v5 slides 9 and 22 ('.dlt'); RWB-PLT-N002-INF AC2 |
| rwb.litigation.events.v1.dlt | rwb.litigation.events.v1 | S4 | Same as its event topic (12) | Not specified in the source documents (GAP-0124; ASM-0201) | One alert per record; the replay tool is the recovery path | Arch v5 slides 9 and 22 ('.dlt'); RWB-PLT-N002-INF AC2 |
| rwb.asset.events.v1.dlt | rwb.asset.events.v1 | S5 | Same as its event topic (12) | Not specified in the source documents (GAP-0124; ASM-0201) | One alert per record; the replay tool is the recovery path | Arch v5 slides 9 and 22 ('.dlt'); RWB-PLT-N002-INF AC2 |
| rwb.debtsale.events.v1.dlt | rwb.debtsale.events.v1 | S6 | Same as its event topic (12) | Not specified in the source documents (GAP-0124; ASM-0201) | One alert per record; the replay tool is the recovery path | Arch v5 slides 9 and 22 ('.dlt'); RWB-PLT-N002-INF AC2 |
| rwb.writeoff.events.v1.dlt | rwb.writeoff.events.v1 | S7 | Same as its event topic (12) | Not specified in the source documents (GAP-0124; ASM-0201) | One alert per record; the replay tool is the recovery path | Arch v5 slides 9 and 22 ('.dlt'); RWB-PLT-N002-INF AC2 |
| rwb.deviation.events.v1.dlt | rwb.deviation.events.v1 | S8 | Same as its event topic (12) | Not specified in the source documents (GAP-0124; ASM-0201) | One alert per record; the replay tool is the recovery path | Arch v5 slides 9 and 22 ('.dlt'); RWB-PLT-N002-INF AC2 |
| rwb.partner.events.v1.dlt | rwb.partner.events.v1 | S9 | Same as its event topic (12) | Not specified in the source documents (GAP-0124; ASM-0201) | One alert per record; the replay tool is the recovery path | Arch v5 slides 9 and 22 ('.dlt'); RWB-PLT-N002-INF AC2 |
| rwb.decision-record.v1.dlt | rwb.decision-record.v1 | P7 | Same as its event topic | Not specified in the source documents (GAP-0124; ASM-0201) | One alert per record; the replay tool is the recovery path | Arch v5 slides 9 and 22 ('.dlt'); shared topic at GAP-0125 |

## Sheet: Events

| Event types: 43 on 20 topics |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|
| The 28 types that carry an EV row keep the ID, the payload words and the meaning of the v4 event table; the 15 types with 'new' in the ID column exist only in the Architecture v5 service catalogue and are not renumbered (ASM-0209). Owner code and owner service are those of the Microservice Ownership Map v1. |  |  |  |  |  |  |  |  |  |  |
| EV row | Event | Event type (ce_type) | Topic | Owner code | Owner service | Direction | Payload | Consumers | Family | Basis |
| EV-01 | CaseCreated | rwb.case.CaseCreated.v1 | rwb.case.events.v1 | P3 | Case and workflow | Published | caseId, caseNo, productGroup, accounts, businessDate | rwb-agent, rwb-deviation, rwb-reporting | Domain event | Unchanged; event type named (D-RCV-60) |
| EV-02 | CaseAllocated | rwb.case.CaseAllocated.v1 | rwb.case.events.v1 | P3 | Case and workflow | Published | caseId, queueId, ownerId, ruleId, ruleVersion | rwb-reporting | Domain event | Unchanged; event type named (D-RCV-60) |
| EV-03 | CaseAllocationFailed | rwb.case.CaseAllocationFailed.v1 | rwb.case.events.v1 | P3 | Case and workflow | Published | caseId, reason, ruleGap | rwb-case | Domain event | Unchanged; event type named (D-RCV-60) |
| EV-04 | CaseTransferred | rwb.case.CaseTransferred.v1 | rwb.case.events.v1 | P3 | Case and workflow | Published | caseId, fromOwner, toOwner, reasonCode | rwb-reporting | Domain event | Unchanged; event type named (D-RCV-60) |
| EV-05 | CaseStateChanged | rwb.case.CaseStateChanged.v1 | rwb.case.events.v1 | P3 | Case and workflow | Published | caseId, fromState, toState, ruleId, decisionLogEntryId | rwb-comms, rwb-reporting | Domain event | Unchanged; event type named (D-RCV-60) |
| EV-06 | DeviationRaised | rwb.deviation.DeviationRaised.v1 | rwb.deviation.events.v1 | S8 | Deviation | Published | caseId, deviationCode, raisedBy | rwb-case, rwb-comms, rwb-treatment | Domain event | Unchanged; event type named (D-RCV-60) |
| EV-07 | DeviationCleared | rwb.deviation.DeviationCleared.v1 | rwb.deviation.events.v1 | S8 | Deviation | Published | caseId, deviationCode, outcome | rwb-case, rwb-comms | Domain event | Unchanged; event type named (D-RCV-60) |
| EV-08 | DecisionRecorded | rwb.decision.DecisionRecorded.v1 | rwb.decision-record.v1 | P7 | Decision and rules | Published (all 19 producers) | entryId, caseId, decisionCode, approver | rwb-decision, rwb-reporting | Domain event (shared topic) | Topic set: rwb.decision-record.v1 (Arch v5 slide 42 row 08) |
| EV-09 | ApprovalRequested | rwb.decision.ApprovalRequested.v1 | rwb.decision.events.v1 | P7 | Decision and rules | Published | approvalId, caseId, level, amount | gateway-bff | Domain event | Unchanged; event type named (D-RCV-60) |
| EV-10 | TreatmentApproved | rwb.treatment.TreatmentApproved.v1 | rwb.treatment.events.v1 | S2 | Treatment and offer | Published | treatmentId, caseId, terms | rwb-comms, rwb-payment | Domain event | Unchanged; event type named (D-RCV-60) |
| EV-11 | TreatmentBooked | rwb.payment.TreatmentBooked.v1 | rwb.payment.events.v1 | P8 | Payment | Published | treatmentId, bookingRef, businessDate | rwb-case, rwb-treatment | Domain event | Unchanged; event type named (D-RCV-60) |
| EV-12 | PaymentMissed | rwb.payment.PaymentMissed.v1 | rwb.payment.events.v1 | P8 | Payment | Published | treatmentId, dueDate, amountDue | rwb-case, rwb-treatment, rwb-comms | Domain event | Unchanged; event type named (D-RCV-60) |
| EV-13 | NoticeGenerated | rwb.comms.NoticeGenerated.v1 | rwb.comms.events.v1 | P6 | Communications | Published | noticeId, caseId, type, templateVersion | rwb-decision | Domain event | Unchanged; event type named (D-RCV-60) |
| EV-14 | NoticeDispatched | rwb.comms.NoticeDispatched.v1 | rwb.comms.events.v1 | P6 | Communications | Published | noticeId, barcode, sentDate | rwb-reporting | Domain event | Unchanged; event type named (D-RCV-60) |
| EV-15 | NoticeDelivered | rwb.comms.NoticeDelivered.v1 | rwb.comms.events.v1 | P6 | Communications | Published | noticeId, deliveredAt, status | rwb-litigation, rwb-guarantee, rwb-case | Domain event | Unchanged; event type named (D-RCV-60) |
| EV-16 | DocumentStored | rwb.document.DocumentStored.v1 | rwb.document.events.v1 | P5 | Document | Published | documentId, caseId, type, source | rwb-agent, rwb-case | Domain event | Unchanged; event type named (D-RCV-60) |
| EV-17 | DocumentFieldsExtracted | rwb.document.DocumentFieldsExtracted.v1 | rwb.document.events.v1 | P5 | Document | Published | documentId, fields, confidence | rwb-case | Domain event | Unchanged; event type named (D-RCV-60) |
| EV-18 | TimerDue | None (retired) | None (not on Kafka) | PLT | Platform library | Retired | timerId, caseId, timerType | None (retired) | Retired (durable timer) | Retired in v5: no event type and no topic (GAP-0120; ASM-0197) |
| EV-19 | TimerBreached | rwb.case.TimerBreached.v1 | rwb.case.events.v1 | P3 | Case and workflow | Published | timerId, caseId, escalateTo | gateway-bff | Domain event | Unchanged; event type named (D-RCV-60) |
| EV-20 | InstructionIssued | rwb.partner.InstructionIssued.v1 | rwb.partner.events.v1 | S9 | Partner | Published | instructionId, partnerId, type, dueOn | partner portal | Domain event | Unchanged; event type named (D-RCV-60) |
| EV-21 | PartnerResultSubmitted | rwb.partner.PartnerResultSubmitted.v1 | rwb.partner.events.v1 | S9 | Partner | Published | instructionId, result, documents | rwb-litigation, rwb-asset, rwb-case | Domain event | Direction and owner changed: v4 Consumed, Partner portal (GAP-0121; ASM-0198) |
| EV-22 | AssetTakenOn | rwb.asset.AssetTakenOn.v1 | rwb.asset.events.v1 | S5 | Asset | Published | assetId, caseId, source | rwb-case, rwb-payment | Domain event | Unchanged; event type named (D-RCV-60) |
| EV-23 | LotAwarded | rwb.debtsale.LotAwarded.v1 | rwb.debtsale.events.v1 | S6 | Debt sale | Published | lotId, buyerId, price | rwb-case, rwb-payment | Domain event | Unchanged; event type named (D-RCV-60) |
| EV-24 | WriteOffApproved | rwb.writeoff.WriteOffApproved.v1 | rwb.writeoff.events.v1 | S7 | Write-off | Published | writeOffId, caseId, amount | rwb-case, rwb-payment, rwb-reporting | Domain event | Unchanged; event type named (D-RCV-60) |
| EV-25 | ProceedsMatched | rwb.payment.ProceedsMatched.v1 | rwb.payment.events.v1 | P8 | Payment | Published | proceedsId, caseId, amount | rwb-case, rwb-asset, rwb-debtsale, rwb-writeoff, rwb-guarantee | Domain event | Unchanged; event type named (D-RCV-60) |
| EV-26 | AceDataReady | rwb.source-data.AceDataReady.v1 | rwb.source-data.events.v1 | P1 | Source data | Published | sourceSystem (source_system), businessDate (business_date), status, completedAt (completed_at) | rwb-case, rwb-payment, rwb-deviation, rwb-writeoff | Domain event | Direction and owner changed: v4 Consumed, ACE ingestion (GAP-0122; ASM-0199) |
| EV-27 | AceDataLate | rwb.source-data.AceDataLate.v1 | rwb.source-data.events.v1 | P1 | Source data | Published | sourceSystem (source_system), businessDate (business_date), status, completedAt (completed_at) | alerts, gateway-bff | Domain event | Owner set (P1, Arch v5 slide 43 row 27) |
| EV-28 | AgentRunCompleted | rwb.agent.AgentRunCompleted.v1 | rwb.agent.events.v1 | P10 | Agent | Published | runId, agent, caseId, outcome, fallback | rwb-decision, rwb-document, rwb-deviation | Domain event | Unchanged; event type named (D-RCV-60) |
| EV-29 | CaseEvent | None (Temporal signal) | None (not on Kafka) | P3 | Case and workflow | Signal | caseId, eventType, sourceEventId, businessDate | CaseWorkflow (Temporal signal) | Temporal signal | Not on Kafka: signal on the workflow ID case-{caseId} (Arch v5 slide 43 row 29) |
| EV-30 | RulePackageInForce | rwb.decision.RulePackageInForce.v1 | rwb.decision.events.v1 | P7 | Decision and rules | Application event | packageCode, packageVersion, versionId, validFrom, approvedBy | rwb-case, rwb-valuation, rwb-treatment, rwb-payment | Application event | Transport set: published on rwb.decision.events.v1 (Arch v5 slide 41) |
| new | ApprovalDecided | rwb.decision.ApprovalDecided.v1 | rwb.decision.events.v1 | P7 | Decision and rules | Published | Not specified in the source documents (GAP-0127; ASM-0204) | Not specified in the source documents (GAP-0128; ASM-0205) | Domain event (v5 catalogue) | New in v5 (Arch v5 slide 41, rwb-decision topic line) |
| new | ReportPublished | rwb.reporting.ReportPublished.v1 | rwb.reporting.events.v1 | P9 | Reporting | Published | Not specified in the source documents (GAP-0127; ASM-0204) | Not specified in the source documents (GAP-0128; ASM-0205) | Domain event (v5 catalogue) | New in v5 (Arch v5 slide 41, rwb-reporting topic line) |
| new | FileDelivered | rwb.integration.FileDelivered.v1 | rwb.integration.events.v1 | P2 | Integration | Published | Not specified in the source documents (GAP-0127; ASM-0204) | requesting service | Domain event (v5 catalogue) | New in v5 (Arch v5 slide 43, + row) |
| new | FileFailed | rwb.integration.FileFailed.v1 | rwb.integration.events.v1 | P2 | Integration | Published | Not specified in the source documents (GAP-0127; ASM-0204) | requesting service | Domain event (v5 catalogue) | New in v5 (Arch v5 slide 43, + row) |
| new | RouteDecided | rwb.valuation.RouteDecided.v1 | rwb.valuation.events.v1 | S1 | Valuation and route | Published | Not specified in the source documents (GAP-0127; ASM-0204) | rwb-case | Domain event (v5 catalogue) | New in v5 (Arch v5 slide 43, + row) |
| new | TreatmentClosed | rwb.treatment.TreatmentClosed.v1 | rwb.treatment.events.v1 | S2 | Treatment and offer | Published | Not specified in the source documents (GAP-0127; ASM-0204) | rwb-case, rwb-reporting | Domain event (v5 catalogue) | New in v5 (Arch v5 slide 43, + row) |
| new | GuaranteeClaimFiled | rwb.guarantee.GuaranteeClaimFiled.v1 | rwb.guarantee.events.v1 | S3 | Guarantee | Published | Not specified in the source documents (GAP-0127; ASM-0204) | rwb-case, rwb-reporting | Domain event (v5 catalogue) | New in v5 (Arch v5 slide 41; slide 43 GuaranteeClaim*) |
| new | GuaranteeClaimSettled | rwb.guarantee.GuaranteeClaimSettled.v1 | rwb.guarantee.events.v1 | S3 | Guarantee | Published | Not specified in the source documents (GAP-0127; ASM-0204) | rwb-case, rwb-reporting | Domain event (v5 catalogue) | New in v5 (Arch v5 slide 41; slide 43 GuaranteeClaim*) |
| new | LawsuitFiled | rwb.litigation.LawsuitFiled.v1 | rwb.litigation.events.v1 | S4 | Litigation | Published | Not specified in the source documents (GAP-0127; ASM-0204) | Not specified in the source documents (GAP-0128; ASM-0205) | Domain event (v5 catalogue) | New in v5 (Arch v5 slide 41, rwb-litigation topic line) |
| new | JudgmentRecorded | rwb.litigation.JudgmentRecorded.v1 | rwb.litigation.events.v1 | S4 | Litigation | Published | Not specified in the source documents (GAP-0127; ASM-0204) | rwb-asset, rwb-case | Domain event (v5 catalogue) | New in v5 (Arch v5 slide 43, + row) |
| new | AuctionResult | rwb.litigation.AuctionResult.v1 | rwb.litigation.events.v1 | S4 | Litigation | Published | Not specified in the source documents (GAP-0127; ASM-0204) | rwb-asset, rwb-case | Domain event (v5 catalogue) | New in v5 (Arch v5 slide 43, + row) |
| new | AssetSold | rwb.asset.AssetSold.v1 | rwb.asset.events.v1 | S5 | Asset | Published | Not specified in the source documents (GAP-0127; ASM-0204) | rwb-payment, rwb-case | Domain event (v5 catalogue) | New in v5 (Arch v5 slide 43, + row) |
| new | AccountsTransferred | rwb.debtsale.AccountsTransferred.v1 | rwb.debtsale.events.v1 | S6 | Debt sale | Published | Not specified in the source documents (GAP-0127; ASM-0204) | rwb-case, rwb-reporting | Domain event (v5 catalogue) | New in v5 (Arch v5 slide 43, + row) |
| new | AccessPolicyChanged | rwb.access.AccessPolicyChanged.v1 | rwb.access.events.v1 | P4 | Access and authority | Published | Not specified in the source documents (GAP-0127; ASM-0204) | all (cache refresh) | Domain event (v5 catalogue) | New in v5 (Arch v5 slide 41, rwb-access topic line) |
| new | DoaLimitChanged | rwb.access.DoaLimitChanged.v1 | rwb.access.events.v1 | P4 | Access and authority | Published | Not specified in the source documents (GAP-0127; ASM-0204) | all (cache refresh) | Domain event (v5 catalogue) | New in v5 (Arch v5 slide 41, rwb-access topic line) |

## Sheet: Not on Kafka

| The entries that are not plain topic events |  |  |  |  |
|---|---|---|---|---|
| Three entries need a note because a reader of the event table would otherwise expect a topic and a producer for them. |  |  |  |  |
| Entry | Event | Why it is not a topic event | What happens instead | Basis |
| EV-18 | TimerDue | Retired (Arch v5 slide 42 row 18): the clock is a durable Temporal timer inside CaseWorkflow and PLT owns the capability | No producer and no consumer; the rules component of v4 is reached inside the workflow | GAP-0120; ASM-0197 |
| EV-29 | CaseEvent | A Temporal signal, not a domain event (Arch v5 slide 43 row 29) | The case router in rwb-case signals the workflow with ID case-{caseId}; the signal is not written to the outbox and no consumer subscribes to it | Arch v5 slide 43 row 29; Temporal and Drools design slide 14 |
| EV-26 and EV-27 | AceDataReady, AceDataLate | Both are topic events, but neither is written from a Workbench change: rwb-source-data raises them from the ACE batch record it reads through recovery.v_ace_batch_status | They stay exempt from the Transactions rule; the read is not a change and writes no outbox row | v4 rule Transactions; Arch v5 slide 43 rows 26 and 27 |

## Sheet: Envelope

| CloudEvents 1.0 envelope of every event |  |  |
|---|---|---|
| Architecture v5 fixes the mode, the headers, the trace header and the key; it does not give a value form for ce_source or ce_subject. |  |  |
| Item | Value | Basis |
| Mode | CloudEvents 1.0, Kafka binding in binary mode: ce_* attributes as headers, JSON body | Arch v5 slides 9 and 22 |
| ce_specversion | 1.0 | Arch v5 slide 22 |
| ce_id | The event identity and the inbox key; a redelivery is recognised and ignored | Arch v5 slide 22; GAP-0131; ASM-0208 |
| ce_type | rwb.<short>.<Event>.v1 of the owning service; rwb.decision.DecisionRecorded.v1 on the shared topic | Template and Rules §R4; ASM-0209 |
| ce_source | Not specified in the source documents (GAP-0130; ASM-0207) | Arch v5 slide 22 names the header only |
| ce_subject | Not specified in the source documents (GAP-0130; ASM-0207) | Arch v5 slide 22 names the header only |
| traceparent | W3C Trace Context header carried from producer through the relay to every consumer | Arch v5 slides 9 and 22 |
| Body | JSON validated against the registry; IDs, codes and facts only, no personal data | Arch v5 slide 22; v4 rule Payload |
| Kafka record key | caseId; order is per case | Arch v5 slide 9 |
| Schema version | In ce_type (.v1) and in the registry subject; the current and the previous version are accepted (GAP-0129; ASM-0206) | Arch v5 slide 22; v4 rule Versioning |
| Idempotency key | ce_id (GAP-0131; ASM-0208) | Arch v5 slide 22 |

## Sheet: Outbox and inbox

| Outbox, inbox and the transaction boundary |  |  |  |  |  |
|---|---|---|---|---|---|
| The four objects are library objects of the platform and each service creates its own copy in its own schema; the Ownership Map holds that ruling. |  |  |  |  |  |
| Object | Owner | Where it lives | What it is for | Rule | Basis |
| outbox_event | PLT; created in every service schema rwb_* | The event row written with the state change of the producer | Written in the same transaction as the change; the relay publishes it and marks it sent | Arch v5 slide 22; DP-09; RWB-PLT-TE006 |  |
| outbox_delivery | PLT; created in every service schema | Delivery attempt and retry state of an outbox row | One row per attempt; a broker failure leaves the event in the outbox | Arch v5 slide 22; RWB-PLT-TE006 |  |
| processed_event | PLT; created in the schema of every consumer | The inbox of a consumer | ce_id is unique and is written in the same transaction as the consumer's change; a repeat is ignored and counted (R-UNI-40) | Arch v5 slide 22; DP-09 |  |
| idempotency_key | PLT; created in every service schema | The stored response of a POST, keyed by Idempotency-Key | A repeat returns the stored response and does not run the change | Arch v5 slide 11 |  |
| Outbox relay (JOB-11) | every service | The relay inside each service | Every minute it publishes the unsent rows to the service topic and to rwb.decision-record.v1 | Arch v5 slide 44 |  |
| Transaction boundary | the producing service | One local transaction in the producer's schema | The change, the decision record and the outbox row commit together; EV-26 and EV-27 stay exempt | v4 rule Transactions; Arch v5 slide 22 |  |

## Sheet: ACLs

| Principals and ACLs: who writes and who reads |  |  |  |  |  |
|---|---|---|---|---|---|
| One principal per service, least privilege, separate from the ACE PII logging topics (Arch v5 slides 21 and 35). The write list is the service's own topic plus the shared rwb.decision-record.v1, because every service publishes DecisionRecorded. The read list is the consumer column of the event catalogue and nothing else. rwb.integration.events.v1 is read by the requesting service of a file run, which the catalogue does not name, and the two access events are read by all services for their cache; both are granted per use and not per service here. |  |  |  |  |  |
| Service | Code | Principal | Write topics | Read topics | Basis |
| rwb-source-data | P1 | Workload identity of the service, one principal per service | rwb.source-data.events.v1 and rwb.decision-record.v1 | None | Arch v5 slides 21 and 35; consumers from slides 42 and 43 |
| rwb-integration | P2 | Workload identity of the service, one principal per service | rwb.integration.events.v1 and rwb.decision-record.v1 | None | Arch v5 slides 21 and 35; consumers from slides 42 and 43 |
| rwb-case | P3 | Workload identity of the service, one principal per service | rwb.case.events.v1 and rwb.decision-record.v1 | rwb.case.events.v1, rwb.deviation.events.v1, rwb.decision.events.v1, rwb.treatment.events.v1, rwb.payment.events.v1, rwb.comms.events.v1, rwb.document.events.v1, rwb.partner.events.v1, rwb.asset.events.v1, rwb.debtsale.events.v1, rwb.writeoff.events.v1, rwb.source-data.events.v1, rwb.valuation.events.v1, rwb.guarantee.events.v1, rwb.litigation.events.v1 | Arch v5 slides 21 and 35; consumers from slides 42 and 43 |
| rwb-access | P4 | Workload identity of the service, one principal per service | rwb.access.events.v1 and rwb.decision-record.v1 | None | Arch v5 slides 21 and 35; consumers from slides 42 and 43 |
| rwb-document | P5 | Workload identity of the service, one principal per service | rwb.document.events.v1 and rwb.decision-record.v1 | rwb.agent.events.v1 | Arch v5 slides 21 and 35; consumers from slides 42 and 43 |
| rwb-comms | P6 | Workload identity of the service, one principal per service | rwb.comms.events.v1 and rwb.decision-record.v1 | rwb.case.events.v1, rwb.deviation.events.v1, rwb.treatment.events.v1, rwb.payment.events.v1 | Arch v5 slides 21 and 35; consumers from slides 42 and 43 |
| rwb-decision | P7 | Workload identity of the service, one principal per service | rwb.decision.events.v1 and rwb.decision-record.v1 | rwb.decision-record.v1, rwb.comms.events.v1, rwb.agent.events.v1 | Arch v5 slides 21 and 35; consumers from slides 42 and 43 |
| rwb-payment | P8 | Workload identity of the service, one principal per service | rwb.payment.events.v1 and rwb.decision-record.v1 | rwb.decision.events.v1, rwb.treatment.events.v1, rwb.asset.events.v1, rwb.debtsale.events.v1, rwb.writeoff.events.v1, rwb.source-data.events.v1 | Arch v5 slides 21 and 35; consumers from slides 42 and 43 |
| rwb-reporting | P9 | Workload identity of the service, one principal per service | rwb.reporting.events.v1 and rwb.decision-record.v1 | rwb.case.events.v1, rwb.decision-record.v1, rwb.treatment.events.v1, rwb.comms.events.v1, rwb.debtsale.events.v1, rwb.writeoff.events.v1, rwb.guarantee.events.v1 | Arch v5 slides 21 and 35; consumers from slides 42 and 43 |
| rwb-agent | P10 | Workload identity of the service, one principal per service | rwb.agent.events.v1 and rwb.decision-record.v1 | rwb.case.events.v1, rwb.document.events.v1 | Arch v5 slides 21 and 35; consumers from slides 42 and 43 |
| rwb-valuation | S1 | Workload identity of the service, one principal per service | rwb.valuation.events.v1 and rwb.decision-record.v1 | rwb.decision.events.v1 | Arch v5 slides 21 and 35; consumers from slides 42 and 43 |
| rwb-treatment | S2 | Workload identity of the service, one principal per service | rwb.treatment.events.v1 and rwb.decision-record.v1 | rwb.deviation.events.v1, rwb.decision.events.v1, rwb.payment.events.v1 | Arch v5 slides 21 and 35; consumers from slides 42 and 43 |
| rwb-guarantee | S3 | Workload identity of the service, one principal per service | rwb.guarantee.events.v1 and rwb.decision-record.v1 | rwb.payment.events.v1, rwb.comms.events.v1 | Arch v5 slides 21 and 35; consumers from slides 42 and 43 |
| rwb-litigation | S4 | Workload identity of the service, one principal per service | rwb.litigation.events.v1 and rwb.decision-record.v1 | rwb.comms.events.v1, rwb.partner.events.v1 | Arch v5 slides 21 and 35; consumers from slides 42 and 43 |
| rwb-asset | S5 | Workload identity of the service, one principal per service | rwb.asset.events.v1 and rwb.decision-record.v1 | rwb.payment.events.v1, rwb.partner.events.v1, rwb.litigation.events.v1 | Arch v5 slides 21 and 35; consumers from slides 42 and 43 |
| rwb-debtsale | S6 | Workload identity of the service, one principal per service | rwb.debtsale.events.v1 and rwb.decision-record.v1 | rwb.payment.events.v1 | Arch v5 slides 21 and 35; consumers from slides 42 and 43 |
| rwb-writeoff | S7 | Workload identity of the service, one principal per service | rwb.writeoff.events.v1 and rwb.decision-record.v1 | rwb.payment.events.v1, rwb.source-data.events.v1 | Arch v5 slides 21 and 35; consumers from slides 42 and 43 |
| rwb-deviation | S8 | Workload identity of the service, one principal per service | rwb.deviation.events.v1 and rwb.decision-record.v1 | rwb.case.events.v1, rwb.source-data.events.v1, rwb.agent.events.v1 | Arch v5 slides 21 and 35; consumers from slides 42 and 43 |
| rwb-partner | S9 | Workload identity of the service, one principal per service | rwb.partner.events.v1 and rwb.decision-record.v1 | None | Arch v5 slides 21 and 35; consumers from slides 42 and 43 |
| gateway-bff | PLT (edge) | Workload identity of the edge service | None (the edge publishes no business event) | rwb.case.events.v1, rwb.decision.events.v1, rwb.source-data.events.v1 | Arch v5 slides 42 and 43 (gateway-bff inbox and banner) |

## Sheet: Delivery rules

| Delivery rules every producer and consumer implements |  |
|---|---|
| The first ten rules are the rules of the v4 event table, carried forward; the last three are the platform rules of Architecture v5. Where a rule is changed, the row names the gap. |  |
| Rule | Detail |
| Ordering | Events of one case are processed in the order they were written, by one sequence per case in the outbox; the record key caseId keeps them in one partition. |
| Delivery | At least once; consumers are idempotent. |
| Duplicates | Each consumer records ce_id in processed_event in the same transaction as its own change; a repeat is ignored and counted (R-UNI-40). |
| Transactions | The event is written in the same transaction as the change; no event without the change and no change without the event. EV-26 and EV-27 are exempt. |
| Payload | References and codes; no personal data. |
| Versioning | An event carries its schema version; consumers accept the current and the previous version; the registry is BACKWARD compatible. |
| Failure | Three retry windows (1 min, 10 min, 1 h), then the dead-letter topic of the event topic, one alert and the replay tool. |
| Signals | A Temporal signal goes to one workflow ID; it is not a broadcast, not a domain event and not written to the outbox. |
| Outbox | The transaction boundary of the producer; the relay publishes every minute and marks the row sent. |
| Inbox | One consumer group per service per topic; the inbox row and the consumer's change commit together. |
| History | Temporal history is the workflow's own record; it is not an event bus and no consumer subscribes to it. |
| Schema registry | JSON Schema with BACKWARD compatibility; the AsyncAPI 3.0 document of the topic is the contract; no subject is named in this version (GAP-0129; ASM-0206). |
| Platform | Bank Kafka platform ACE already uses, separate topics and ACLs from PII logging; Azure Event Hubs Premium through its Kafka endpoint is the fallback. |

## Sheet: Traceability

| What each part of the catalogue implements |  |  |
|---|---|---|
| Requirement, contract element and the sheets that carry it; the gap and assumption rows are those of this work package. |  |  |
| Requirement | What it fixes | Where it is carried |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | Topics, Envelope, Outbox and inbox, Delivery rules |
| DP-09 | Outbox and inbox library; CloudEvents | Topics, Envelope, Outbox and inbox |
| DP-14 | rwb.<short>.events.v1 replaces the legacy topic names | Topics, events column of every row |
| DP-03 | Local decision record and the shared topic rwb.decision-record.v1 | Topics (shared row), Events (EV-08) |
| Arch v5 slide 9 | Kafka settings, key caseId, retry then .dlt | Topics, Retry topics, Dead-letter topics |
| Arch v5 slide 21 | Bank Kafka platform, separate from PII logging, Event Hubs fallback | ACLs, Delivery rules |
| Arch v5 slide 22 | CloudEvents binary mode, outbox, inbox, retry and dead letter | Envelope, Outbox and inbox, Delivery rules |
| Arch v5 slide 41 | One topic per service and the event types of each service | Topics, Events |
| Arch v5 slides 42 and 43 | Producer and consumers of every event | Events, ACLs |
| Arch v5 slide 44 | JOB-11 outbox sender, every minute, every service | Outbox and inbox |
| RWB-PLT-N002-INF | The 100 topics, the settings, the ACL model | Topics, Retry topics, Dead-letter topics, ACLs |
| RWB-PLT-N008-INF | Schema registry with BACKWARD compatibility | Envelope, Delivery rules |
| Template and Rules §R4 | Event name rwb.<short>.<Event>.v1 | Events, Envelope |
