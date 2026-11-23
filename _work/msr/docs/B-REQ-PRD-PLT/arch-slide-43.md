
A3 · Event catalogue 2/2

Every business event: producer topic and consuming services (CloudEvents on Kafka, key caseId)

| # | Event | Producer | Topic | Consumers |
|---|---|---|---|---|
| 20 | InstructionIssued | rwb-partner | rwb.partner.events.v1 | partner portal |
| 21 | PartnerResultSubmitted | rwb-partner | rwb.partner.events.v1 | rwb-litigation, rwb-asset, rwb-case |
| 22 | AssetTakenOn | rwb-asset | rwb.asset.events.v1 | rwb-case, rwb-payment |
| 23 | LotAwarded | rwb-debtsale | rwb.debtsale.events.v1 | rwb-case, rwb-payment |
| 24 | WriteOffApproved | rwb-writeoff | rwb.writeoff.events.v1 | rwb-case, rwb-payment, rwb-reporting |
| 25 | ProceedsMatched | rwb-payment | rwb.payment.events.v1 | rwb-case, rwb-asset, rwb-debtsale, rwb-writeoff, rwb-guarantee |
| 26 | AceDataReady | rwb-source-data | rwb.source-data.events.v1 | rwb-case, rwb-payment, rwb-deviation, rwb-writeoff |
| 27 | AceDataLate | rwb-source-data | rwb.source-data.events.v1 | alerts, gateway-bff banner |
| 28 | AgentRunCompleted | rwb-agent | rwb.agent.events.v1 | rwb-decision, rwb-document, rwb-deviation |
| 29 | CaseEvent (signal) | case router | — | CaseWorkflow (Temporal signal) |
| 30 | RulePackageInForce | rwb-decision | rwb.decision.events.v1 | rwb-case, rwb-valuation, rwb-treatment, rwb-payment |
| + | RouteDecided | rwb-valuation | rwb.valuation.events.v1 | rwb-case |
| + | AssetSold | rwb-asset | rwb.asset.events.v1 | rwb-payment, rwb-case |
| + | JudgmentRecorded, AuctionResult | rwb-litigation | rwb.litigation.events.v1 | rwb-asset, rwb-case |
| + | TreatmentClosed, GuaranteeClaim* | rwb-treatment / guarantee | — | rwb-case, rwb-reporting |
| + | AccountsTransferred | rwb-debtsale | rwb.debtsale.events.v1 | rwb-case, rwb-reporting |
| + | AccessPolicyChanged, DoaLimitChanged | rwb-access | rwb.access.events.v1 | all (cache refresh) |
| + | FileDelivered, FileFailed | rwb-integration | rwb.integration.events.v1 | requesting service |


43

Notes: Events carry IDs and facts, never personal data. Each producer writes to its outbox in the same transaction as its state change; a relay publishes to its topic. Consumers dedupe through their inbox table. Schemas are versioned in the registry with BACKWARD compatibility; the AsyncAPI document per service is the contract.

