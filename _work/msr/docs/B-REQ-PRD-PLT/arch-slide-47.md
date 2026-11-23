
A7 · Risks and how we handle them

Each risk has a mitigation and an owner

| Risk | Impact | Mitigation | Owner |
|---|---|---|---|
| Too many deployables for the team | Slow delivery, on-call load | Waves by epic; service template, one Helm chart, golden pipeline; platform team runs Kafka and Temporal | Delivery lead |
| ACE database capacity | Slow ACE screens or jobs | Connection pools and caps per login; heavy reports from projections; monitor per schema; move a schema out if needed | ACE DBA |
| Schema rules broken over time | Hidden coupling between services | Database grants per schema; boundary test in every build; review of every new grant | Architecture |
| Kafka platform not ready | Events stay in outboxes | Outbox port; Event Hubs Kafka endpoint as fallback | Enterprise Architecture |
| Temporal upgrade from 1.28.1 | No Nexus, no Worker Versioning | Upgrade to 1.30+ in Wave 0 | Platform team |
| Ledger model not accepted by Audit | Back to synchronous central log | Strict mode for irreversible steps; early walkthrough with Audit | Architecture, Audit |
| BOT approval lead time | Wave 1 date slips | Confirm route early; plan up to 30 business days | Compliance |
| ACE Common contracts change | Recovery features break | Versioned contracts and contract tests with the ACE team | ACE team |


47

Notes: Too many deployables for the team: Slow delivery, on-call load. Mitigation: Waves by epic; service template, one Helm chart, golden pipeline; platform team runs Kafka and Temporal (Delivery lead)
ACE database capacity: Slow ACE screens or jobs. Mitigation: Connection pools and caps per login; heavy reports from projections; monitor per schema; move a schema out if needed (ACE DBA)
Schema rules broken over time: Hidden coupling between services. Mitigation: Database grants per schema; boundary test in every build; review of every new grant (Architecture)
Kafka platform not ready: Events stay in outboxes. Mitigation: Outbox port; Event Hubs Kafka endpoint as fallback (Enterprise Architecture)
Temporal upgrade from 1.28.1: No Nexus, no Worker Versioning. Mitigation: Upgrade to 1.30+ in Wave 0 (Platform team)
Ledger model not accepted by Audit: Back to synchronous central log. Mitigation: Strict mode for irreversible steps; early walkthrough with Audit (Architecture, Audit)
BOT approval lead time: Wave 1 date slips. Mitigation: Confirm route early; plan up to 30 business days (Compliance)
ACE Common contracts change: Recovery features break. Mitigation: Versioned contracts and contract tests with the ACE team (ACE team)

