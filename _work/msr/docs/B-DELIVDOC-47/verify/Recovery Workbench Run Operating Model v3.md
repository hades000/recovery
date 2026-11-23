## Slide 1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

SCB

COLLECTIONS AND RECOVERY TRANSFORMATION
Recovery Workbench: run operating model

Henka Group, 28 October 2026
(C) Siam Commercial Bank and Henka Pte Ltd

3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash

## Slide 2

Who runs the Workbench after go-live

2

| Tier | What | Handles | Who |
|---|---|---|---|
| Tier 0 | Self-help | Help text, the content standard, the team start pack | Users |
| Tier 1 | Business support | How-to questions, access requests, data questions | Super users in each team; service desk |
| Tier 2 | Application support | Defects, failed jobs, exception queues, reference data loads | Platform administrator; reference data administrator; data steward |
| Tier 3 | Engineering | Code defects, performance, releases | TechX recovery squads; ACE team |
| Vendors and platforms | Platform support | Azure, Entra ID, COLLINS, model endpoint | SCB IT; data and analytics; Enterprise AI |


## Slide 3

Service levels

3

| Severity | Meaning | Respond | Restore | Owner |
|---|---|---|---|---|
| Severity 1 | Service down or decisions wrong | 15 minutes | 4 hours | Application owner |
| Severity 2 | A main path down with no workaround | 1 hour | 1 working day | Platform administrator |
| Severity 3 | A path with a workaround | 4 hours | Agreed date | Platform administrator |
| Severity 4 | Question or cosmetic | 1 working day | Backlog | Tier 1 |


## Slide 4

Hours and shifts

4

| Item | Design |
|---|---|
| Business hours | 08:00 to 20:00 on business days; tier 1 and tier 2 on duty |
| Early shift | 05:00 to 08:00 on business days: data steward on call for the loads and the morning chain |
| Outside hours | SCB IT on call for severity 1; platform administrator on call by rota |
| Release weekends | ACE team and the squads on call for the change window |


## Slide 5

Escalation

5

| Issue | Goes to | When |
|---|---|---|
| Severity 1 | Application owner and SCB IT incident manager | At once |
| Missed restore time | Head of the Chief Debt Recovery Management Office | At the restore time |
| Data load late | Data steward, then the data lead | 07:00, then 09:00 |
| Agent behaving wrongly | Risk and model risk officer; autonomy level lowered | At once |


## Slide 6

Decision needed

6

|  | Decision | Answer used until decided |
|---|---|---|
| DL02 | Who the application owner is | The Tribe lead, with the ACE team as technical custodian |


## Slide 7

What changed in version 3

7

| Version | Date | Decision | Tool | What changed |
|---|---|---|---|---|
| 3 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash | One run book page per service for the 19 services (slides 8 to 17); every owner from the Ownership Map v1; decisions DL44 to DL49 added; the five version 2 slides of tiers, service levels, hours, escalation and DL02 kept word for word; release dates unchanged and tentative (DL48). |
| 2 | 28 October 2026 (the date on the source cover) | Not stated in the source documents (CG-B-DELIVDOC-47-5; ASM-B-DELIVDOC-47-5) | Not stated in the source documents (CG-B-DELIVDOC-47-5; ASM-B-DELIVDOC-47-5) | The source deck: tiers, service levels, hours and shifts, escalation and the DL02 decision, kept on slides 2 to 6. |


The source has no change log, so no row before version 2 is reconstructed (CG-B-DELIVDOC-47-5; ASM-B-DELIVDOC-47-5). Status: Draft; no approval is recorded in this run (U8; CG-B-DELIVDOC-47-7; ASM-B-DELIVDOC-47-7).

## Slide 8

The service shape: what a run book covers

8

• 19 services: P1 to P10 platform, S1 to S9 route. Each one has its own schema and login, the REST base /api/recovery/<short>/v1, the topic rwb.<short>.events.v1 with its retry and .dlt topics, and the task queue rwb-<short> (Template and Rules R4).
• Waves: 1 for P1 to P7, P9 and P10; 2 for P8, S2, S5 and S8; 3 for S1, S3, S4 and S6; 4 for S7 and S9 (Ownership Map v1, Services sheet).
• Every service comes from the service template: own schema and login, outbox and inbox, a Temporal worker, a local decision record and DecisionRecorded, OpenTelemetry (Architecture v5 slide 20).
• Shared platform pieces are not counted in the 19: gateway-bff with the Redis session, the partner gateway in the DMZ, Kafka, Temporal in namespace rwb-recovery, Airflow and observability (Architecture v5 slide 20 note).
• A run book page is one page per service: what it runs, what to look at first, who owns it and where it escalates. The source deck has none, so version 3 adds the pages on slides 10 to 13 (CG-B-DELIVDOC-47-6; ASM-B-DELIVDOC-47-6).
• Owner: the service code in the Ownership Map v1; the team is a suggestion only, TechX unless a DB, INF, OPS or ITG story names another owner (U3; Template and Rules R5.3; DL46).

## Slide 9

Run book per service: the eight steps

9

| Step | Do | Look at | Stop when |
|---|---|---|---|
| 1 | Open the service's page and confirm health | GET /health and GET /metrics on the service; the service dashboard | health green and the error rate back to its normal band |
| 2 | Confirm the worker polls its own queue | Temporal UI, namespace rwb-recovery, queue rwb-<short>; the KEDA backlog | the backlog falls and the workers scale |
| 3 | Clear the topic | the retry topics at 1 min, 10 min and 1 h, then the .dlt topic with an alert; the replay tool | no message in the .dlt topic and the alert closed |
| 4 | Confirm events left the outbox | the outbox table in the service's schema; DecisionRecorded on rwb.decision-record.v1 | the outbox empty and the 5-minute ledger target met |
| 5 | Check the service's Schedules | the service's Schedules in Temporal; the times are on its run book page | each Schedule ran at its time |
| 6 | Check the decision record | the local decision record, hash-linked, in the service's schema; the central ledger in P7 rwb-decision | the chain check passes and no gap alert is open |
| 7 | Check the calls it depends on | contract dependencies (C) never block; integration dependencies (I) only on ITG stories (Template and Rules R5.4) | the caller's circuit breaker is closed |
| 8 | Record and escalate | severity from slide 3; escalation from slide 5 and slide 17; owner from slide 15 | the ticket closes with the restore time met |


The alert thresholds and the per-service dashboard: Not specified in the source documents (CG-B-DELIVDOC-47-3; ASM-B-DELIVDOC-47-3). The desk uses the four severity bands on slide 3 until they are stated.

## Slide 10

Run book per service: platform P1 to P5

10

| Service | Wave and owner | Schema, queue and topic | What runs | First check |
|---|---|---|---|---|
| P1 rwb-source-data Source data | Wave 1 P1; TechX suggested | rwb_source_data queue rwb-source-data rwb.source-data.events.v1 | AceIngestCheck, reconciliation; listEligibleAccounts, snapshot(page); the 30 v_ace_* views | GET /freshness; the 05:30 AceDataLate alarm; the Airflow DAG's last task; the fallback poll of the ACE batch record |
| P2 rwb-integration Integration and files | Wave 1 P2; TechX suggested | rwb_integration queue rwb-integration rwb.integration.events.v1 | deliverFile(manifest), receiveFile; the WIN file at 16:00; the buyer files per lot | GET /interface-runs; POST /interface-runs/{id}/retry; FileFailed and the 16:00 window |
| P3 rwb-case Case and workflow | Wave 1 P3; TechX suggested | rwb_case queue rwb-case rwb.case.events.v1 | CaseWorkflow, one per case; DailyCaseRun (Schedule and AceDataReady); allocate, transfer, rebalance | DailyCaseRun finished; CaseAllocationFailed; the CaseWorkflow count in Temporal UI |
| P4 rwb-access Access and authority | Wave 1 P4; TechX suggested | rwb_access queue rwb-access rwb.access.events.v1 | POST /authorise with the cached answer; the six-monthly access review Schedule | POST /authorise answers; the cache refresh on AccessPolicyChanged and DoaLimitChanged |
| P5 rwb-document Document hub | Wave 1 P5; TechX suggested | rwb_document queue rwb-document rwb.document.events.v1 | DocumentIntakeWorkflow (OCR, classify, extract); the retention Schedule; Azure Blob WORM | DocumentStored without DocumentFieldsExtracted; Blob write errors; the retention run |


Owner: the service code in the Ownership Map v1; the team is a suggestion only, any team may pick up this story (U3; DL46). Service owner for the run: Not specified in the source documents (CG-B-DELIVDOC-47-1; ASM-B-DELIVDOC-47-1).

## Slide 11

Run book per service: platform P6 to P10

11

| Service | Wave and owner | Schema, queue and topic | What runs | First check |
|---|---|---|---|---|
| P6 rwb-comms Communications | Wave 1 P6; TechX suggested | rwb_comms queue rwb-comms rwb.comms.events.v1 | NoticeDispatchWorkflow; the letter generated in P5; WIN letters through P2; ACE Common SMS and LINE | NoticeDispatched without NoticeDelivered; the ACE Common notification path; the WIN letter file |
| P7 rwb-decision Decision centre and log | Wave 1 P7; TechX suggested | rwb_decision queue rwb-decision rwb.decision.events.v1 | ApprovalWorkflow; rule promote 00:01; chain check 02:00; the daily ledger seal to WORM | ledger completeness against the 5-minute target; the 02:00 chain check; RulePackageInForce after 00:01 |
| P8 rwb-payment Payments and posting | Wave 2 P8; TechX suggested | rwb_payment queue rwb-payment rwb.payment.events.v1 | matchPayments, confirmBookings, postProceeds (saga step); the posting file to P2 | payments matched for the business date; PaymentMissed; the posting file delivered |
| P9 rwb-reporting Reporting | Wave 1 P9; TechX suggested | rwb_reporting queue rwb-reporting rwb.reporting.events.v1 | measures at 01:30 (Schedule); buildRegulatoryExtract; snapshot(page) from P1 | measures finished at 01:30 and ReportPublished; the regulatory extract file; projection lag on Kafka |
| P10 rwb-agent Agent runtime | Wave 1 P10; TechX suggested | rwb_agent queue rwb-agent rwb.agent.events.v1 | AgentRunWorkflow, 60 s and then the rule result; the tool gateway read-only calls; the Enterprise AI endpoint | AgentRunCompleted rate and the 60 s fallback; the Enterprise AI endpoint; switch rwb-agent off if it misbehaves |


Owner: the service code in the Ownership Map v1; the team is a suggestion only, any team may pick up this story (U3; DL46). Service owner for the run: Not specified in the source documents (CG-B-DELIVDOC-47-1; ASM-B-DELIVDOC-47-1).

## Slide 12

Run book per service: route S1 to S5

12

| Service | Wave and owner | Schema, queue and topic | What runs | First check |
|---|---|---|---|---|
| S1 rwb-valuation Valuation and route | Wave 3 S1; TechX suggested | rwb_valuation queue rwb-valuation rwb.valuation.events.v1 | RouteDecisionWorkflow, a child of the case; the route agent; the approval child | RouteDecided for the day's cases; RulePackageInForce picked up; collateral and appraisal reads from P1 |
| S2 rwb-treatment TDR, settlement, DIL | Wave 2 S2; TechX suggested | rwb_treatment queue rwb-treatment rwb.treatment.events.v1 | TreatmentWorkflow; the settlement and DIL sagas; the restructure calculator through Nexus | TreatmentApproved and TreatmentClosed; the plan timers; the Nexus call into ace-collection |
| S3 rwb-guarantee Guarantees | Wave 3 S3; TechX suggested | rwb_guarantee queue rwb-guarantee rwb.guarantee.events.v1 | GuaranteeClaimWorkflow; the guarantor notice child; the approval child | GuaranteeClaimFiled without GuaranteeClaimSettled; NoticeDelivered missing; the workflow age |
| S4 rwb-litigation Litigation and enforcement | Wave 3 S4; TechX suggested | rwb_litigation queue rwb-litigation rwb.litigation.events.v1 | LitigationWorkflow, years and continues-as-new; the law firm instruction; the demand notice child | instruction SLAs on rwb-partner; hearings without PartnerResultSubmitted; the continue-as-new run |
| S5 rwb-asset Assets and auction | Wave 2 S5; TechX suggested | rwb_asset queue rwb-asset rwb.asset.events.v1 | AssetDisposalWorkflow; the monthly re-appraisal (Schedule); the auction vendor instruction | the monthly re-appraisal Schedule; AuctionResult; AssetSold without ProceedsMatched |


Owner: the service code in the Ownership Map v1; the team is a suggestion only, any team may pick up this story (U3; DL46). Service owner for the run: Not specified in the source documents (CG-B-DELIVDOC-47-1; ASM-B-DELIVDOC-47-1).

## Slide 13

Run book per service: route S6 to S9

13

| Service | Wave and owner | Schema, queue and topic | What runs | First check |
|---|---|---|---|---|
| S6 rwb-debtsale Debt sale | Wave 3 S6; TechX suggested | rwb_debtsale queue rwb-debtsale rwb.debtsale.events.v1 | DebtSaleWorkflow, a saga with the transfer as pivot; the data room pack; the buyer file through P2 | LotAwarded without AccountsTransferred; the buyer file delivery; the saga's pivot step |
| S7 rwb-writeoff Write-off and recovery | Wave 4 S7; TechX suggested | rwb_writeoff queue rwb-writeoff rwb.writeoff.events.v1 | WriteOffWorkflow; the scan on the 3rd working day (Schedule); the committee approval child | the 3rd-working-day scan ran; WriteOffApproved; posting held until the central ledger confirms |
| S8 rwb-deviation Deviation handling | Wave 2 S8; TechX suggested | rwb_deviation queue rwb-deviation rwb.deviation.events.v1 | DeviationWorkflow, a child of the case; X1 to X7 screening; the screening agent run | DeviationRaised without DeviationCleared; the paused stage timer; the screening agent run |
| S9 rwb-partner Partner management | Wave 4 S9; TechX suggested | rwb_partner queue rwb-partner rwb.partner.events.v1 | InstructionWorkflow with SLA timers; issueInstruction, recordResult; the partner portal on FAPI 2.0 | instruction SLA timers; PartnerResultSubmitted; the partner gateway and MFA |


Owner: the service code in the Ownership Map v1; the team is a suggestion only, any team may pick up this story (U3; DL46). Service owner for the run: Not specified in the source documents (CG-B-DELIVDOC-47-1; ASM-B-DELIVDOC-47-1).

## Slide 14

Run book for the shared platform

14

| Piece | Who runs it | What to check | Escalate to |
|---|---|---|---|
| gateway-bff with the Redis session | platform (PLT); SCB IT | one hop and the 2 s timeout per service; the session store; a breaker per service | SCB IT incident manager |
| Partner gateway (DMZ) | platform (PLT); SCB IT | FAPI 2.0; the partner client certificates; MFA | SCB IT incident manager |
| Kafka | the bank and ACE platform team | consumer lag per group; the retry topics; the .dlt alerts; the replay tool | ACE team |
| Temporal | platform (PLT) | namespace rwb-recovery; the queue backlog; JOB-21, the stuck workflow scan every 5 min | platform team |
| ACE PostgreSQL | ACE DBA | one login per schema; the capped pools per service; per-schema monitoring | ACE team |
| Airflow | the bank platform; SCB IT | the ACE ingestion DAG; POST /business-days/{date}/ready; the SLA alerts at 05:30 and 07:00 | data lead |
| Observability | platform (PLT); SCB IT | one trace across the services; ACE PII logs to the SOC; per-service metrics | SCB IT |


Escalation follows slide 5. The rota for the shared pieces: Not specified in the source documents (CG-B-DELIVDOC-47-4; ASM-B-DELIVDOC-47-4).

## Slide 15

Who owns what: the Ownership Map owners

15

| Area | Owner | Stated in |
|---|---|---|
| Services, tables, endpoints, events, workflows and jobs | the service code P1 to P10 and S1 to S9 | Ownership Map v1, Services and Tables sheets |
| Parameters and reference data (E1-042, E1-043) | P3 rwb-case | R3 default ruling |
| Case list API | P3 rwb-case | R3 default ruling |
| Rule package registry | P7 rwb-decision | R3 default ruling |
| Interaction ledger | P1 rwb-source-data | R3 default ruling |
| Feature flags | the platform library (PLT); the admin paths served by P2 rwb-integration | R3 default ruling; Ownership Map v1 Rulings |
| Outbox, inbox and idempotency tables | the platform library, created in every service schema | Ownership Map v1 Rulings |
| Service owner for the run | Not specified in the source documents (CG-B-DELIVDOC-47-1; ASM-B-DELIVDOC-47-1) | gap in this version |
| Tier 1, tier 2 and tier 3 roles per service | Not specified in the source documents (CG-B-DELIVDOC-47-2; ASM-B-DELIVDOC-47-2) | gap in this version |


Each owner above is the owner recorded in the Ownership Map v1 or in the R3 default rulings; no owner is invented in this deck.

## Slide 16

Hours, rota and on call, per service

16

| Item | Design kept from version 2 | Per service in version 3 |
|---|---|---|
| Business hours | 08:00 to 20:00 on business days; tier 1 and tier 2 on duty | the service's suggested owner is on duty for its own page, slides 10 to 13 |
| Early shift | 05:00 to 08:00 on business days: data steward on call for the loads and the morning chain | P1 rwb-source-data first, then P3 rwb-case (DailyCaseRun), then the route services in play |
| Outside hours | SCB IT on call for severity 1; platform administrator on call by rota | one rota page per service: Not specified in the source documents (CG-B-DELIVDOC-47-4; ASM-B-DELIVDOC-47-4) |
| Release weekends | ACE team and the squads on call for the change window | the service's wave, 1 to 4, as printed on its page |


The four rows of version 2 are kept; the right-hand column is the only change, so that a page exists for each of the 19 services.

## Slide 17

Escalation, per service

17

| Issue | Goes to | When |
|---|---|---|
| Severity 1 | the service's suggested owner, then the application owner and the SCB IT incident manager | at once |
| Missed restore time | Head of the Chief Debt Recovery Management Office | at the restore time |
| Data load late | the P1 rwb-source-data owner, then the data steward, then the data lead | 07:00, then 09:00 |
| Agent behaving wrongly | the P10 rwb-agent owner, then the risk and model risk officer; the autonomy level is lowered | at once |
| Decision record gap | the P7 rwb-decision owner; the 5-minute completeness alert and the chain check | at once |
| Stuck workflow | the platform team; JOB-21, the visibility query every 5 minutes | at once |


The first four rows are those of version 2, with the service owner inserted for the 19 services; the last two rows are new for the target architecture.

## Slide 18

Decisions added in version 3

18

| ID | Decision | Answer used until decided |
|---|---|---|
| D-RCV-60 | Adopt Architecture v5 and realign the documents and stories | 19 services inside ACE, one schema and login per service; applied in this version |
| DL44 | Adopt Architecture v5 | Architecture v5 is the top source on the R3 precedence list |
| DL45 | Service epics plus business-epic tags | one epic per service (19), plus 7 platform and 5 integration epics |
| DL46 | Soft ownership by team type | the owner is a suggestion only; any team may pick up this story |
| DL47 | Epic 1 preservation rule | a built or in-build Epic 1 story keeps its base ID; the change is a delta story |
| DL48 | Dates unchanged and tentative | every release date is unchanged and marked (tentative) |
| DL49 | Gap and assumption registers | gaps and assumptions are recorded per document in folder 23 |


DL02 of slide 6 is unchanged and still open. D-RCV-60 and DL44 to DL49 are the new decisions of this realignment.

## Slide 19

Change log

19

| Version | Date | Change | Tool |
|---|---|---|---|
| 3 | 22 November 2026 | D-RCV-60 microservice realignment: one run book page per service (slides 8 to 17), every owner from the Ownership Map v1, decisions DL44 to DL49; every version 2 slide kept | T3 Code / OpenCode / DeepSeek v4.1 Flash |
| 2 | 28 October 2026 | the source deck; it records no change log and no tool line | Not stated in the source documents (CG-B-DELIVDOC-47-5; ASM-B-DELIVDOC-47-5) |


Change-log row: "3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash". Status: Draft.
