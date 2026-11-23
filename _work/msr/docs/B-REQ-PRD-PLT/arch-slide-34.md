
When one part fails, the rest keeps working

Example: the litigation service is down

Case

Decision

Access

Deviation

Valuation

Treatment

Guarantee

Litigation

Asset

Debt sale

Write-off

Document

Comms

Payment

Partner

Integration

Source data

Reporting

Agent

Litigation pauses. Its work waits on its queue and topic offset and resumes when it is back. The other 18 keep running.

Kafka down

Events wait in each service's outbox and are sent when it returns. Nothing is lost.

Temporal down

Running journeys pause and resume where they stopped. Screens keep working.

ACE database busy

Each service's pool is capped, so Recovery cannot starve ACE; reports use projections.

AI slow or down

After 60 seconds the rule-based answer is used; officers are never blocked.

Failures are contained by design (queues, outboxes, timeouts, circuit breakers, capped pools), not by luck.

34

Notes: Contained by design: each service has its own schema and login, task queue, consumer group and workers; REST calls have timeouts and circuit breakers; events wait in outboxes and topics; Temporal keeps every running journey.

Litigation down: litigation tabs show 'temporarily unavailable'; LitigationWorkflow tasks wait on queue rwb-litigation and resume when it is back; Kafka keeps its consumer offset; every other route, the case list and payments continue.

Other cases: Kafka down (outboxes hold events), Temporal down (journeys pause and resume; screens still work), ACE database busy (capped pools keep Recovery from starving ACE), AI slow (rule result after 60 s). Full table in the appendix.

