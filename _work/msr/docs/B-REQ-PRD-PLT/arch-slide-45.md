
A5 · Questions architects ask 1/2

Short answers; the detail is in the main slides

| Question | Answer |
|---|---|
| Why 19 services and not fewer? | One service per BA module gives each capability its own release, owner and contract, so it can be reused or replaced later (for example Document hub or Communications by ACE Collection) without untangling a shared core. |
| Isn't 19 too many for a team of nine? | They arrive in waves with the epics (9 at Epic 1, 19 by Epic 7). One service template, one Helm chart, one pipeline and shared libraries keep the cost per service low. |
| Why share the ACE database? | It is already run, backed up and approved; ACE data is there. A schema and login per service keeps ownership clear, and any schema can move to its own server later by changing a connection string. |
| Doesn't a shared database couple the services? | Only if they share tables. Rules: write only your own schema, no cross-schema joins or foreign keys, IDs across services, contracts for everything else. A boundary test fails the build on any violation. |
| Who reads ACE's data? | Only rwb-source-data reads the 30 recovery.v_ace_* views (ADR-010). Everyone else asks it through REST or a Temporal activity, so a change in ACE is absorbed in one place. |
| Why Kafka rather than Azure Service Bus? | ACE already runs Kafka, so no new platform or outsourcing review; replay lets a new or repurposed service rebuild its view from history; per-case ordering by key; many independent listeners. |
| What if the Kafka platform cannot host us in time? | Azure Event Hubs Premium speaks the Kafka protocol, so the same client code works. Until then the outbox keeps events safe in each service. |
| Why one Temporal cluster for ACE and Recovery? | Temporal isolates tenants with namespaces and task queues. One cluster per service would be 19 x 4 environments. Workers stay inside each service. |
| The bank is moving to Airflow: why not run everything there? | Airflow suits timed, cross-system batches. It is not built for millions of long-lived case workflows, approvals and timers. So Airflow says the data is ready, opens file windows and runs extracts; Temporal runs each case. For discussion. |


45

Notes: Q: Why 19 services and not fewer?
A: One service per BA module gives each capability its own release, owner and contract, so it can be reused or replaced later (for example Document hub or Communications by ACE Collection) without untangling a shared core.

Q: Isn't 19 too many for a team of nine?
A: They arrive in waves with the epics (9 at Epic 1, 19 by Epic 7). One service template, one Helm chart, one pipeline and shared libraries keep the cost per service low.

Q: Why share the ACE database?
A: It is already run, backed up and approved; ACE data is there. A schema and login per service keeps ownership clear, and any schema can move to its own server later by changing a connection string.

Q: Doesn't a shared database couple the services?
A: Only if they share tables. Rules: write only your own schema, no cross-schema joins or foreign keys, IDs across services, contracts for everything else. A boundary test fails the build on any violation.

Q: Who reads ACE's data?
A: Only rwb-source-data reads the 30 recovery.v_ace_* views (ADR-010). Everyone else asks it through REST or a Temporal activity, so a change in ACE is absorbed in one place.

Q: Why Kafka rather than Azure Service Bus?
A: ACE already runs Kafka, so no new platform or outsourcing review; replay lets a new or repurposed service rebuild its view from history; per-case ordering by key; many independent listeners.

Q: What if the Kafka platform cannot host us in time?
A: Azure Event Hubs Premium speaks the Kafka protocol, so the same client code works. Until then the outbox keeps events safe in each service.

Q: Why one Temporal cluster for ACE and Recovery?
A: Temporal isolates tenants with namespaces and task queues. One cluster per service would be 19 x 4 environments. Workers stay inside each service.

Q: The bank is moving to Airflow: why not run everything there?
A: Airflow suits timed, cross-system batches. It is not built for millions of long-lived case workflows, approvals and timers. So Airflow says the data is ready, opens file windows and runs extracts; Temporal runs each case. For discussion.

