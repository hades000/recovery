
How the journey runs: one case workflow, with a child for each stage

The parent tracks the whole case; each stage runs in the service that owns it

CaseWorkflow  one per case, entry to closure · queue rwb-case · signals from the case router

child

Route decision
rwb-valuation + approval on rwb-decision

Deviation
rwb-deviation (any time)

Treatment / guarantee
rwb-treatment · rwb-guarantee

Litigation
rwb-litigation (years)

Asset / debt sale
rwb-asset · rwb-debtsale

Write-off
rwb-writeoff

time

Continue-As-New at every stage end and at least every 28 days

Timers that last for years
Court dates and letter deadlines survive restarts and upgrades

Events become signals
PaymentMissed, NoticeDelivered and others reach the case through the case router

Approvals from the kit
ApprovalWorkflow on rwb-decision, routed by authority (DoA)

Each stage runs on the queue of the service that owns it, so it scales, releases and can be reused with that service.

25

Notes: CaseWorkflow (rwb-case, workflow ID = case ID) is the parent from entry to closure. Each stage is a child workflow started on the owner's task queue: RouteDecisionWorkflow (rwb-valuation, with ApprovalWorkflow from the kit on rwb-decision), DeviationWorkflow (rwb-deviation, can start at any time and pauses the stage clock), TreatmentWorkflow (rwb-treatment) and GuaranteeClaimWorkflow (rwb-guarantee), LitigationWorkflow (rwb-litigation, can run for years), AssetDisposalWorkflow (rwb-asset) and DebtSaleWorkflow (rwb-debtsale), WriteOffWorkflow (rwb-writeoff).

Events from other services reach the case as signals through the case router (signalWithStart), never by direct calls.

History: Continue-As-New at every stage end and at least every 28 days keeps each run far below Temporal's limit of 51,200 events or 50 MB. Children use parent close policy ABANDON so they survive the parent's Continue-As-New.

