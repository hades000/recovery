
How an event travels: 'payment missed' from outbox to three listeners

Exactly-once effect from at-least-once delivery: outbox in the producer, inbox in each consumer

rwb-payment

matchPayments (activity)

rwb_payment: tables + outbox (one transaction)

outbox relay

nothing is lost if Kafka is down

rwb.payment.events.v1
key caseId · 12 partitions · RF 3 · 7 days

partitions (6 of 12 shown); red = PaymentMissed for RC-123

publish

rwb-case
group rwb-case · case router → signal to CaseWorkflow

rwb-treatment
group rwb-treatment · check plan breach

rwb-comms
group rwb-comms · send reminder notice

each consumer: inbox (processed_event) in its own schema, same transaction as its change

On failure

retry 1 min

retry 10 min

retry 1 h

.dlt + alert

ce_specversion: 1.0
ce_type: rwb.payment.PaymentMissed.v1
ce_source: /rwb-payment
ce_id: 01JD…7Q
ce_subject: case/RC-123
traceparent: 00-4bf9…-01
key: RC-123
{ "caseId": "RC-123",
  "treatmentId": "TR-9",
  "dueDate": "2026-11-15",
  "amountDue": 12500.00,
  "daysLate": 3 }

on the wire: headers, key, body (IDs and facts only)

Name
rwb.<service>.events.v1

Envelope
CloudEvents 1.0, binary mode

Schema
JSON Schema registry, backward compatible

Producer
outbox · idempotent · acks=all

Payload
IDs and business facts, no PII

The producer writes once and moves on; each listener reacts in its own time and a duplicate never acts twice.

22

Notes: Producer: rwb-payment's matchPayments activity updates its tables and inserts the event into its outbox table in the same database transaction (schema rwb_payment). The outbox relay publishes it with an idempotent producer (acks=all, min.insync.replicas=2) and marks it sent. If Kafka is down, events wait in the outbox.

Topic: rwb.payment.events.v1, 12 partitions, replication factor 3, 7-day retention, key caseId. CloudEvents 1.0 Kafka binding in binary mode: ce_id, ce_type, ce_source, ce_subject as headers, W3C traceparent header, JSON body validated against the registry (BACKWARD compatibility).

Consumers: one consumer group per service. Each records ce_id in its inbox table (processed_event) in the same transaction as its own change, so a redelivered event has no second effect. Failures go to retry topics (1 min, 10 min, 1 h) and then to the dead-letter topic with an alert and a replay tool.

rwb-case does not act itself: its case router turns the event into a Temporal signal (signalWithStart) on the CaseWorkflow.

