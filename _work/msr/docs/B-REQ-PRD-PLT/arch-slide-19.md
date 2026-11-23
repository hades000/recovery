
Service contracts 6/7 · Routes 2: litigation, asset, debt sale

IN = what the service accepts; OUT = what it writes and sends; the tag is the call type

IN

OUT

REST  GET/POST /legal-actions · GET/POST /hearings
EVT  NoticeDelivered · PartnerResultSubmitted
TMP  LitigationWorkflow (years; continues-as-new)

DB  writes schema rwb_litigation: legal actions, hearings, judgments, enforcement, LED auction ladder
EVT  rwb.litigation.events.v1: LawsuitFiled, JudgmentRecorded, AuctionResult
TMP  Partner: issueInstruction (law firm) · Comms: child: demand notice · Decision: child: approval

S4 · rwb-litigation
Litigation & enforcement
queue rwb-litigation
rwb.litigation.events.v1

IN

OUT

REST  GET/POST /assets, /listings · POST /auction-rounds
EVT  JudgmentRecorded, AuctionResult · ProceedsMatched
TMP  AssetDisposalWorkflow · Schedule: re-appraisal monthly

DB  writes schema rwb_asset: assets taken on, holding, floor price, listings, auction rounds
EVT  rwb.asset.events.v1: AssetTakenOn, AssetSold
TMP  Partner: issueInstruction (auction vendor) · Decision: child: approval · Payment: postProceeds

S5 · rwb-asset
Assets & auction
queue rwb-asset
rwb.asset.events.v1

IN

OUT

REST  GET/POST /lots · POST /lots/{id}/bids · /award
EVT  ProceedsMatched
TMP  DebtSaleWorkflow (saga, pivot = transfer)

DB  writes schema rwb_debtsale: lots, data room, buyer terms, bids, award, transfer
EVT  rwb.debtsale.events.v1: LotAwarded, AccountsTransferred
TMP  Document: data room pack · Decision: child: approval · Integration: deliverFile (buyer file) · Payment: postProceeds

S6 · rwb-debtsale
Debt sale
queue rwb-debtsale
rwb.debtsale.events.v1

19

Notes: Contracts in full (also in the service catalogue in the appendix):

rwb-litigation (S4, Litigation & enforcement)
IN: REST GET/POST /legal-actions; GET/POST /hearings | events NoticeDelivered; PartnerResultSubmitted | Temporal LitigationWorkflow (years; continues-as-new)
OUT: schema rwb_litigation (legal actions, hearings, judgments, enforcement, LED auction ladder) | topic rwb.litigation.events.v1: LawsuitFiled, JudgmentRecorded, AuctionResult | TMP Partner: issueInstruction (law firm) · Comms: child: demand notice · Decision: child: approval

rwb-asset (S5, Assets & auction)
IN: REST GET/POST /assets, /listings; POST /auction-rounds | events JudgmentRecorded, AuctionResult; ProceedsMatched | Temporal AssetDisposalWorkflow; Schedule: re-appraisal monthly
OUT: schema rwb_asset (assets taken on, holding, floor price, listings, auction rounds) | topic rwb.asset.events.v1: AssetTakenOn, AssetSold | TMP Partner: issueInstruction (auction vendor) · Decision: child: approval · Payment: postProceeds

rwb-debtsale (S6, Debt sale)
IN: REST GET/POST /lots; POST /lots/{id}/bids · /award | events ProceedsMatched | Temporal DebtSaleWorkflow (saga, pivot = transfer)
OUT: schema rwb_debtsale (lots, data room, buyer terms, bids, award, transfer) | topic rwb.debtsale.events.v1: LotAwarded, AccountsTransferred | TMP Document: data room pack · Decision: child: approval · Integration: deliverFile (buyer file) · Payment: postProceeds

Tags: REST = synchronous HTTPS (OpenAPI 3.1); EVT = Kafka topic (CloudEvents, AsyncAPI); TMP = Temporal activity or child workflow on the owner's task queue; NEXUS = Temporal Nexus operation into another namespace; SQL = read-only view; FILE = claim-check file; DB = the service's own schema in the ACE database.

