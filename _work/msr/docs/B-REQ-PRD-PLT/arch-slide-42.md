
A2 · Event catalogue 1/2

Every business event: producer topic and consuming services (CloudEvents on Kafka, key caseId)

| # | Event | Producer | Topic | Consumers |
|---|---|---|---|---|
| 01 | CaseCreated | rwb-case | rwb.case.events.v1 | rwb-agent, rwb-deviation, rwb-reporting |
| 02 | CaseAllocated | rwb-case | rwb.case.events.v1 | rwb-reporting |
| 03 | CaseAllocationFailed | rwb-case | rwb.case.events.v1 | rwb-case |
| 04 | CaseTransferred | rwb-case | rwb.case.events.v1 | rwb-reporting |
| 05 | CaseStateChanged | rwb-case | rwb.case.events.v1 | rwb-comms, rwb-reporting |
| 06 | DeviationRaised | rwb-deviation | rwb.deviation.events.v1 | rwb-case, rwb-comms, rwb-treatment |
| 07 | DeviationCleared | rwb-deviation | rwb.deviation.events.v1 | rwb-case, rwb-comms |
| 08 | DecisionRecorded | all 19 | rwb.decision-record.v1 | rwb-decision, rwb-reporting |
| 09 | ApprovalRequested | rwb-decision | rwb.decision.events.v1 | gateway-bff (inbox) |
| 10 | TreatmentApproved | rwb-treatment | rwb.treatment.events.v1 | rwb-comms, rwb-payment |
| 11 | TreatmentBooked | rwb-payment | rwb.payment.events.v1 | rwb-case, rwb-treatment |
| 12 | PaymentMissed | rwb-payment | rwb.payment.events.v1 | rwb-case, rwb-treatment, rwb-comms |
| 13 | NoticeGenerated | rwb-comms | rwb.comms.events.v1 | rwb-decision |
| 14 | NoticeDispatched | rwb-comms | rwb.comms.events.v1 | rwb-reporting |
| 15 | NoticeDelivered | rwb-comms | rwb.comms.events.v1 | rwb-litigation, rwb-guarantee, rwb-case |
| 16 | DocumentStored | rwb-document | rwb.document.events.v1 | rwb-agent, rwb-case |
| 17 | DocumentFieldsExtracted | rwb-document | rwb.document.events.v1 | rwb-case |
| 18 | TimerDue | durable timer | — | (retired: timer inside the workflow) |
| 19 | TimerBreached | rwb-case | rwb.case.events.v1 | gateway-bff (inbox) |


42

Notes: Events carry IDs and facts, never personal data. Each producer writes to its outbox in the same transaction as its state change; a relay publishes to its topic. Consumers dedupe through their inbox table. Schemas are versioned in the registry with BACKWARD compatibility; the AsyncAPI document per service is the contract.

