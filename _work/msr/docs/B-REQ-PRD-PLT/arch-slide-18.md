
Service contracts 5/7 · Routes 1: valuation, treatment, guarantee

IN = what the service accepts; OUT = what it writes and sends; the tag is the call type

IN

OUT

REST  GET /cases/{id}/valuation · POST /cases/{id}/route-proposals
EVT  RulePackageInForce
TMP  RouteDecisionWorkflow (child of case)

DB  writes schema rwb_valuation: valuations, D6 route decision, route agent output
EVT  rwb.valuation.events.v1: RouteDecided
TMP  Agent: child: route agent · Decision: child: approval
REST  Source data: collateral, appraisals

S1 · rwb-valuation
Valuation & route
queue rwb-valuation
rwb.valuation.events.v1

IN

OUT

REST  GET/POST /treatments · POST /treatments/{id}/offer
EVT  TreatmentBooked, PaymentMissed · DeviationRaised
TMP  TreatmentWorkflow · settlement and DIL sagas

DB  writes schema rwb_treatment: treatments, contracts, settlement and deed-in-lieu agreements, plan timers
EVT  rwb.treatment.events.v1: TreatmentApproved, TreatmentClosed
TMP  Decision: child: approval · Document: contract, e-sign · Payment: postProceeds
NEXUS  ACE Common: restructure calculator (Nexus)

S2 · rwb-treatment
TDR, settlement, DIL
queue rwb-treatment
rwb.treatment.events.v1

IN

OUT

REST  GET/POST /guarantee-claims
EVT  NoticeDelivered · ProceedsMatched
TMP  GuaranteeClaimWorkflow

DB  writes schema rwb_guarantee: TCG and insurance claims, guarantor notices and pursuit
EVT  rwb.guarantee.events.v1: GuaranteeClaimFiled, GuaranteeClaimSettled
TMP  Comms: child: guarantor notice · Decision: child: approval

S3 · rwb-guarantee
Guarantees
queue rwb-guarantee
rwb.guarantee.events.v1

18

Notes: Contracts in full (also in the service catalogue in the appendix):

rwb-valuation (S1, Valuation & route)
IN: REST GET /cases/{id}/valuation; POST /cases/{id}/route-proposals | events RulePackageInForce | Temporal RouteDecisionWorkflow (child of case)
OUT: schema rwb_valuation (valuations, D6 route decision, route agent output) | topic rwb.valuation.events.v1: RouteDecided | TMP Agent: child: route agent · Decision: child: approval | REST Source data: collateral, appraisals

rwb-treatment (S2, TDR, settlement, DIL)
IN: REST GET/POST /treatments; POST /treatments/{id}/offer | events TreatmentBooked, PaymentMissed; DeviationRaised | Temporal TreatmentWorkflow · settlement and DIL sagas
OUT: schema rwb_treatment (treatments, contracts, settlement and deed-in-lieu agreements, plan timers) | topic rwb.treatment.events.v1: TreatmentApproved, TreatmentClosed | TMP Decision: child: approval · Document: contract, e-sign · Payment: postProceeds | NEXUS ACE Common: restructure calculator (Nexus)

rwb-guarantee (S3, Guarantees)
IN: REST GET/POST /guarantee-claims | events NoticeDelivered; ProceedsMatched | Temporal GuaranteeClaimWorkflow
OUT: schema rwb_guarantee (TCG and insurance claims, guarantor notices and pursuit) | topic rwb.guarantee.events.v1: GuaranteeClaimFiled, GuaranteeClaimSettled | TMP Comms: child: guarantor notice · Decision: child: approval

Tags: REST = synchronous HTTPS (OpenAPI 3.1); EVT = Kafka topic (CloudEvents, AsyncAPI); TMP = Temporal activity or child workflow on the owner's task queue; NEXUS = Temporal Nexus operation into another namespace; SQL = read-only view; FILE = claim-check file; DB = the service's own schema in the ACE database.

