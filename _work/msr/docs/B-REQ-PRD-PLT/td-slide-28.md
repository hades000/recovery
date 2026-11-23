
When things go wrong: nothing is lost, the case waits or retries

What happens to a running case in each failure

Worker stops

Work waits on its queue; resumes from history

A call fails (ACE, partner, DB)

Retried: 1 s, doubling, up to 10 tries

No rule version in force

Stops at once (no retry); stuck-case alert

New rule version is faulty

Refused at load; current version keeps running

Decision record write fails

Same transaction: nothing moves (R-UNI-39)

AI assistant slow

After 60 s the rule answer is used (R-UNI-32)

Kafka is down

Events wait in the outbox; none lost

Central ledger late

Work carries on; points of no return wait

Temporal keeps every running journey, each service keeps its own data, and the outbox keeps every event.

28

Notes: Worker down: tasks stay on the task queue; workers come back; the workflow resumes from history.
Call fails: activity retry policy 1 s initial interval, back-off 2, 10 attempts.
NoPackageInForce: non-retryable; the activity fails and the stuck-workflow scan (JOB-21, a visibility query every 5 minutes, platform team) raises it.
Rule version fails to load: load checks (compile, schema, overlap, unreachable row, default row, at least 50 scenarios, dry run) refuse it (state REFUSED); the version in force keeps running.
Decision record write fails: the record, the state change and the outbox row are one transaction, so nothing moves (R-UNI-39).
Kafka down: events wait in each producer's outbox and are published when it returns; consumers' inboxes drop duplicates; failed messages go to retry topics (1 min, 10 min, 1 h) then the dead-letter topic with an alert (v5 slide 22).
Central ledger late or down: services carry on and the ledger catches up from rwb.decision-record.v1; only points of no return (debt transfer, write-off, auction sale, title transfer) wait for its confirmation (strict mode, v5 slide 28).
AI agent slow: after 60 s the rule result is used (R-UNI-32).

