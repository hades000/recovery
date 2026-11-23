
Open design points to settle before build

Six items, each with an owner

1

ADR-011: child workflow per stage

v5 design; ADR-011 has one workflow

Suggested owner  Recovery tech lead

2

ADR-009: record locally, seal centrally

Merges log + apply into one step

Suggested owner  RW-RISK + Internal Audit

3

Packages for S1, S3–S9

448 rules exist; codes are Phase 2

Suggested owner  RW-COE + architect

4

Route numbering R4 / R5

Documents disagree

Suggested owner  Business analyst

5

XLS tables or DMN 1.6

Same Drools runtime runs both

Suggested owner  RW-COE + RW-RISK

6

Temporal 1.30+, jobs as Schedules

Nexus, Worker Versioning; no Quartz

Suggested owner  Platform team

None of these blocks the demo; settle items 1, 2 and 3 before Epic 3 starts.

32

Notes: These follow from aligning the Temporal and Drools design to Recovery Microservice Architecture v5 (19 services).
1. ADR-011 update: v5 runs a parent CaseWorkflow with a child workflow per stage on the owning service's queue, with Continue-As-New at every stage end and at least every 28 days; ADR-011 and Workflow Engine Design v3 still describe one long CaseWorkflow with route sets as states.
2. ADR-009 change: v5 writes each decision record locally in the same transaction as the state change and seals it centrally in rwb-decision (strict mode at points of no return). This merges WriteDecisionLog and ApplyState into one RecordAndApply activity. Needs Risk and Internal Audit sign-off.
3. Drools packages for S1 and S3 to S9: the route sets exist (448 rules) but package codes are Phase 2; each needs one owning service (rwb-valuation, rwb-guarantee, rwb-litigation, rwb-asset, rwb-debtsale, rwb-writeoff, rwb-deviation).
4. Route numbering: R-LIT-01 starts litigation on route = R4; Case Journeys v3 calls R4 the guarantee claim and R5 litigation.
5. Rule format: Drools XLS decision tables today (ADR-012); v5 proposes OMG DMN 1.6, converted table by table on the same runtime.
6. Platform: Temporal 1.30+ for Nexus and Worker Versioning (local stack 1.29.7, ADR-011 1.28.1), and Quartz jobs such as JOB-16 become Temporal Schedules in the owning service (Phase 1 note T2 keeps Quartz).
