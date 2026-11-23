
Where we change today's design, and why

Ten changes; each becomes a new ADR (ADR-013 onward)

Today

Proposed

recovery-core: one deployable (ADR-001)

19 services, one per BA module

One schema for everything (ADR-002)

ACE database, one schema and login per service

30 views read by any module (ADR-010)

Views read only by rwb-source-data

Outbox without a broker

Outbox + Kafka business-event topics

Central log inside every call (ADR-009)

Local record, then central ledger in rwb-decision

Rules in Excel tables (ADR-012)

DMN decision models, registry in rwb-decision

One endless case workflow (ADR-011)

Workflow kit + stage children + Continue-As-New

ACE's Quartz tables; ADF / Control-M (BRD)

Temporal Schedules in services; bank Airflow runs the chain

Data lake and Power BI feed (INT-19/20)

Removed: reports from rwb-reporting

No circuit breakers

Timeouts, circuit breakers, bulkheads

Kept: same AKS cluster and App Gateway, ACE Common services, gateway-bff, shared Temporal, Blob with WORM, payload codec.

37

Notes: ADR-001/002: one deployable and one schema become 19 services with a schema and login each in the same ACE database. ADR-010: the 30 views stay, but only rwb-source-data reads them. Event and Messaging Design v4: outbox without a broker becomes outbox plus Kafka topics. ADR-009: the central log written inside every call becomes a local record plus central ledger. ADR-012: XLS decision tables become DMN models (same Drools runtime, converted table by table). ADR-011: one long CaseWorkflow becomes workflow kit plus stage children plus Continue-As-New. Batch and Scheduling Design v4: ACE's shared Quartz tables become Temporal Schedules, and the BRD's ADF/Control-M jobs move to the bank's Airflow for the cross-system chain only (for discussion). Interface Specifications v3: INT-19/20 (data lake, Power BI) are removed. Resilience: timeouts, circuit breakers and bulkheads become a standard.

