
Event broker: Kafka, on the platform ACE already runs

Recovery gets its own business-event topics and access rules, separate from ACE's PII logging topics

Recommended: Apache Kafka on the bank / ACE platform
dedicated Recovery topics and ACLs · fallback: Event Hubs Premium (Kafka API)

Already part of ACE
ACE runs Kafka today (PII logging): no new platform or outsourcing review

Order per case
Record key = caseId, so one case's events arrive in order

Replay from history
A new or repurposed service rebuilds its view from the topic

Many independent listeners
One consumer group per service; the producer never changes

Same code on Azure if needed
Event Hubs Premium speaks the Kafka protocol

|  | Kafka (bank platform) | Event Hubs Premium | Service Bus Premium |
|---|---|---|---|
| Already used by ACE | Yes (PII logging) | No | No |
| Replay history | Yes, retention per topic | Yes, up to 90 days | No: removed when consumed |
| Order per case | Partition key = caseId | Partition key | Sessions |
| Many listeners | Consumer groups | Consumer groups | Topic subscriptions |
| Client code | Kafka client | Same Kafka client | Own SDK |
| Run by | Bank / ACE platform team | Azure (managed) | Azure (managed) |
| Role in this design | Recommended | Fallback | Not chosen |


Kafka: ACE already runs it, it keeps history for replay and reuse, and the same code moves to Event Hubs if ever needed.

21

Notes: Recommendation: host Recovery's business events on the bank Kafka platform that ACE already uses for PII logging, as dedicated topics with their own ACLs, quotas and schema subjects. Fallback: Azure Event Hubs Premium through its Kafka endpoint; the same producer and consumer code works.

Why Kafka for this design: (1) already operated for ACE, so no new platform and no new outsourcing assessment under FPG 19/2559; (2) ordering per case by using caseId as the record key; (3) retention and replay, so a new or repurposed service can rebuild its own view from history, which matters for the reuse goal; (4) independent consumer groups per service; (5) CloudEvents has a standard Kafka binding.

Why not Azure Service Bus: good for command queues with sessions and dead-lettering, but messages are removed once consumed (no replay), it is a new platform for ACE, and it needs its own SDK. Commands between services already go through Temporal, so we do not need a command queue.

To confirm with the ACE platform team: capacity (Recovery volume is small: tens of thousands of events a day), topic naming, ACL model, schema registry, environments.

