
Workflow model: a parent per case, a child per stage, the same four steps for every event

CaseWorkflow on rwb-case tracks the case; each stage runs as a child workflow in the service that owns it

Any stage workflow
on its owner's queue

1  Event arrives
Kafka → case router → signal

2  EvaluateRules
Drools: package, version, rule

3  RecordAndApply
record + state + outbox, one transaction

4  Wait
durable timer or next signal

repeat

PARENT AND CHILDREN  (one queue per owning service)

CaseWorkflow · rwb-case
one per case, entry to closure

starts one child workflow per stage  ↓

Route decision
rwb-valuation  ·  S1

Treatment
rwb-treatment  ·  RES 37 · SET 27 · DIL 37

Guarantee claim
rwb-guarantee  ·  GUA 32

Litigation
rwb-litigation  ·  LIT 79

Asset disposal
rwb-asset  ·  DIS 72

Debt sale
rwb-debtsale  ·  DS 41

Write-off
rwb-writeoff  ·  WO 51

Deviation (any time)
rwb-deviation  ·  DEV 22

Continue-As-New at each stage end, at least every 28 days

The parent tracks the case; each stage runs where its rules and data live, always as receive, ask, record and apply, wait.

13

Notes: Aligned to Recovery Microservice Architecture v5 (slides 23 to 25). CaseWorkflow (workflow ID = case ID; ADR-011 writes it as case-{caseId}) runs on task queue rwb-case in namespace rwb-recovery from entry to closure. Each stage is a child workflow started on the owner's queue: RouteDecisionWorkflow (rwb-valuation, with ApprovalWorkflow from the kit on rwb-decision), TreatmentWorkflow (rwb-treatment: restructure, settlement, deed in lieu), GuaranteeClaimWorkflow (rwb-guarantee), LitigationWorkflow (rwb-litigation), AssetDisposalWorkflow (rwb-asset), DebtSaleWorkflow (rwb-debtsale), WriteOffWorkflow (rwb-writeoff), DeviationWorkflow (rwb-deviation, can start at any time and pauses the stage clock).

Each route set's rules run in the service that owns the stage; UNIVERSAL rules (R-UNI) apply in every service.

Events from other services reach the case through the case router in rwb-case (Kafka consumer, signalWithStart), never by direct calls; the parent forwards them to the running child. Inside every workflow the same four steps repeat: receive, ask Drools (EvaluateRules activity), record and apply in one transaction (RecordAndApply activity), wait.

History: Continue-As-New at every stage end and at least every 28 days keeps each run far below Temporal's limit of 51,200 events or 50 MB. Children use parent close policy ABANDON so they survive the parent's Continue-As-New. Search attributes: CaseId, Stage, ProductGroup, QueueCode.

This replaces the one-long-workflow model of Workflow Engine Design v3 / ADR-011 (route sets as states inside one workflow); ADR-011 needs updating.

