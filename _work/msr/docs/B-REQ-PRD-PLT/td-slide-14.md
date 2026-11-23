
How the workflow asks the rules: one event, step by step

Example: a restructure customer misses a payment (EV-12) → rule R-RES-27 starts a cure period

rwb-payment

Case router

CaseWorkflow

Treatment (child)

EvaluateRules

Drools

RecordAndApply

PaymentMissed · Kafka

1

signalWithStart

2

forward to stage

3

evaluate RESTRUCTURE

4

evaluate(pkg, facts)

5

R-RES-27 · version · start cure period

6

record + state + task + outbox: one transaction

7

durable timer: wait 30 days

8

payment arrives the same way → wait ends early

9

The answer and the move are saved together, or not at all; if a worker dies, the workflow replays and reuses the answer.

14

Notes: The pattern every case event follows, aligned to Recovery Microservice Architecture v5 (slides 22, 24, 25, 27, 28):
1. rwb-payment's matchPayments activity (JOB-07, started by AceDataReady) finds no payment. In one transaction it updates schema rwb_payment and writes PaymentMissed (EV-12) to its outbox; the relay publishes it to Kafka topic rwb.payment.events.v1 (CloudEvents 1.0, key caseId).
2. The case router in rwb-case consumes it (inbox, so a duplicate never acts twice) and calls signalWithStart on the CaseWorkflow (workflow ID = case ID).
3. CaseWorkflow forwards the event to the running stage child, TreatmentWorkflow on queue rwb-treatment.
4-6. EvaluateRules runs as an activity on rwb-treatment: RuleEvaluator.evaluate(packageCode, facts, onDate) returns RuleResult(packageCode, packageVersion, ruleId, outputs). Drools is only called inside an activity, so replays reuse the recorded result.
7. RecordAndApply writes, in one transaction in schema rwb_treatment: the decision record (rule ID, version, inputs, answer; hash-linked to the previous record), the new state and task, and the outbox rows (DecisionRecorded to rwb.decision-record.v1). If it fails, nothing moves (R-UNI-39). rwb-decision collects the record into the central ledger within 5 minutes.
8. The workflow waits on a durable timer (the 30-day cure period).
9. A later payment arrives the same way and ends the wait early.

Compared with Workflow Engine Design v3: the separate WriteDecisionLog and ApplyState activities become one RecordAndApply activity, because v5 writes the record and the change in one transaction (proposed change to ADR-009). Retry policy: 1 s initial interval, back-off 2, 10 attempts; NoPackageInForce is non-retryable.

