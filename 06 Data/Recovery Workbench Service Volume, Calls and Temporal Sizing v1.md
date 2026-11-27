# Recovery Workbench Service Volume, Calls and Temporal Sizing v1

| Item | Value |
|---|---|
| Decision | D-RCV-60 (Architecture v5: 19 services inside ACE) |
| Status | Draft. Every figure marked EST is a proposal for confirmation by the owner named in section 11 |
| Date | 24 November 2026 |
| Reads with | Volume and Scale Forecast v4 (sheets Inputs, Five years, Users and load, Read path, Service volumes, Topics and queues); Architecture v5 Text Extract v1 (slides 2, 14 to 24, 34, 48); Temporal and Drools Design Text Extract v1; Business Requirements Program v5 section 6 (NFR-001 to NFR-007); PRD PLT NFR-PLT-016; RWB-PLT-E1070 and RWB-PLT-NF08 |
| Scope | The 19 services P1 to P10 and S1 to S9, gateway-bff, the partner gateway, Kafka and the shared Temporal layer (namespace `rwb-recovery`) |

## 1. Purpose

The sources state the business volume (cases, documents, users, route work) and size Kafka, but they set no figure for:

- the calls each service takes and makes,
- the Temporal load (workflow starts, open workflows, actions a second, history shards, persistence size, worker counts),
- the services whose driver has no source count: rwb-payment (P8), rwb-guarantee (S3), rwb-partner (S9), the SMS and LINE notices of rwb-comms (P6), the debt-sale lots (S6) and the dashboard reads of rwb-reporting (P9) (GAP-0281, GAP-1603, GAP-1643, GAP-0280).

This document puts all of it in one place. A sourced figure carries its source. A derived figure is labelled **EST-nn**, with its basis and its reason in section 8.

## 2. Summary

| Measure | 2027 | 2031 | Kind |
|---|---|---|---|
| Open cases | ~23,600 at go-live; 27,095 steady state | 47,389 | Source (NFR-001; Forecast v4) |
| New cases a month | 2,980 (from 3,110 new accounts) | 5,213 | Source formula (Five years!C5 / 12) |
| Concurrent users at peak | 414 (366 staff, 48 partner) | Same; named users are not forecast to grow | Source (Users and load) |
| Browser and partner requests at peak | ~21 a second | Same | Source (Users and load!E8) |
| Internal REST calls at peak, after composite-screen fan-out | ~35 a second; design 105 a second | Same | EST-01 |
| Kafka events | ~563k a month, ~26k a business day | ~0.9M a month | EST-02 (source says "tens of thousands a day") |
| Temporal new workflows | ~261k a month | ~420k a month | EST-03 |
| Temporal runs, including Continue-As-New | ~376k a month (base); ~550k (high) | ~650k to ~800k | EST-03 |
| Temporal open workflows | ~118k (base); ~292k (high) | ~205k (base); ~380k (high) | EST-04 |
| Temporal actions | 7 to 10 a second in business hours; design 100 sustained, 200 burst | Design unchanged | EST-05 |
| Temporal history shards | 512, fixed at cluster creation | 512 | EST-06 |
| Temporal persistence (PostgreSQL) | ~20 to 32 GB; provision 100 GB | ~45 GB | EST-07 |

**Conclusion.** The load is small for every component. Architecture v5 slide 48 says so ("a single well-built service could carry this load"). The design splits for ownership, release independence and isolation, not for throughput. Sizing therefore follows three rules:

1. Two small API pods per service, for availability rather than load.
2. Scale only the worker pools on the hot paths: rwb-case, rwb-payment, rwb-document, rwb-comms and rwb-agent.
3. Size the shared Temporal cluster for burst and for idle long-running workflows, not for average throughput.

## 3. Base figures from the sources

| ID | Figure | Value | Source |
|---|---|---|---|
| B1 | Active inventory at 90 or more days past due | 28,119 accounts (12,256 Mortgage, 12,960 HP, 2,903 SSME) | Inputs I01, I02, I04 |
| B2 | New accounts at 90 days past due | 3,110 a month (808, 1,816, 486); +15% a year | Inputs I05 to I07, I09 |
| B3 | Accounts per case | 1.2 | Inputs I08 (DL17) |
| B4 | New cases 2027 / 2031 | 2,980 / 5,213 a month | Five years!C5, C9 (calculated) |
| B5 | Open cases | 23,570 today; 27,095 steady state 2027; 47,389 by 2031 | NFR-001; Five years!D5, D9 |
| B6 | Documents | 71,801 a month in 2027 (15 per new case + 1 per open case a month); 125,580 in 2031; 0.5 MB each | Five years!E5; Inputs I11 to I13 |
| B7 | Decision-log entries | 63,131 a month in 2027; 110,416 in 2031 | Five years!H5 |
| B8 | Rule evaluations | 12 per open case a month: ~325k a month in 2027 (slides quote 283k to 318k) | Inputs I17 |
| B9 | Interactions | 4 per open case a month: ~108k a month | Inputs I14 |
| B10 | Users | 466 recovery staff, 448 collections staff, 320 partner users; 40% / 15% online in the busiest hour; 3 requests a minute each | Inputs I27 to I32 |
| B11 | Peak load | 413.6 concurrent; 20.7 requests a second (18.3 staff, 2.4 partner) | Users and load (calculated) |
| B12 | ACE view reads | 60% of actions read a view, 2 reads each: 24.8 a second, 74 a second with a 3x burst | Inputs I33, I34; Read path |
| B13 | Route work | 667 lawsuits, 720 vehicles repossessed, 1,909 registered letters, 29 NPA properties sold a month; 4,736 NPA held; 3,783 debt-sale accounts a year | Inputs I20 to I25 |
| B14 | Restructure and deed in lieu | 173,807 accounts under restructure (stock); ~3,000 restructures a month; 1,000 deeds in lieu a month in 2027 | Inputs I26; NFR-005; NFR-006 |
| B15 | Service targets | Screen < 2 s p95; rule evaluation < 300 ms; agent 60 s then rule result; 99.9% in business hours | NFR v3; Arch v5 slide 48 |
| B16 | Kafka settings | 20 topics, 12 partitions, RF 3, 7 days, key caseId, retry 1 min / 10 min / 1 h then .dlt | Arch v5 slide 34; Forecast v4 Topics and queues |
| B17 | Temporal settings | One cluster per environment with its own PostgreSQL; namespace `rwb-recovery`; 19 task queues; 30-day retention then Blob archive; Continue-As-New at stage end and at least every 28 days; KEDA on backlog; server 1.30 or later | RWB-PLT-NF08; RWB-PLT-E1070; Temporal and Drools Design slides 13, 27 |
| B18 | Peak windows | 05:00 to 07:00 chain (data ready, case creation, payment matching, allocation, rebalance 06:30); OCR 500 pages an hour; notices 16:00; measures 01:30; rule promote 00:01 | Arch v5 slide 48; Forecast v4 Topics and queues |

## 4. Call types and why each is used

| Tag | Call type | Used for | Why this type |
|---|---|---|---|
| REST | Synchronous HTTPS, OpenAPI 3.1 | Screens, through gateway-bff, one hop to the owner service; partner portal through the partner gateway (FAPI 2.0) | A person is waiting (< 2 s p95). One hop with a 2 s timeout and a breaker per service keeps latency and failure from chaining. gateway-bff "never calls a service that then calls another" (Arch v5 slide 20) |
| EVT | Kafka topic, CloudEvents 1.0, outbox and inbox | Facts that have happened (CaseCreated, PaymentMissed). One topic per service plus the shared `rwb.decision-record.v1` | Many independent listeners. Order per case (key caseId). Replay for a new or reused service. Exactly-once effect from at-least-once delivery. Already run by ACE (slide 21) |
| TMP | Temporal activity or child workflow on the owner's task queue | Commands and steps in another service (approval, generate letter, postProceeds); long processes (litigation for years) | Durable retries, durable timers for months or years, saga compensation and full history. No command queue is needed (slide 21) |
| NEXUS | Temporal Nexus operation into another namespace | rwb-treatment to the ACE restructure calculator in `ace-collection` | Crosses a namespace owned by ACE with the same durability, without a shared queue or a REST chain |
| SQL | Read-only view SELECT | Only rwb-source-data reading the 30 `recovery.v_ace_*` views | One grant for the whole Workbench. ACE keeps ownership of its data |
| FILE | Claim-check file, MFT SFTP or Blob | WIN letters (INT-14), debt-buyer files (INT-25), posting files, regulatory extract, document storage | Outside parties take files. Large payloads stay out of events and workflow history |
| DB | Own schema in the ACE database | Each service writes only its own schema, outbox, inbox and decision_record | Isolation, with no data lake (D-RCV-60) |

## 5. Per-service volume, calls and Temporal load

### 5.1 Business volume per service (2027)

"Source" means the Forecast v4 Service volumes formula, calculated. "EST" means section 8.

| Service | Driver | 2027 volume | 2031 | Kind |
|---|---|---|---|---|
| P1 rwb-source-data | Eligible accounts per business day; view reads | 28,119 accounts a day; 24.8 view reads a second at peak (74 with burst) | Stock-driven | Source |
| P2 rwb-integration | Outbound and inbound files | 1 WIN file a day (1,909 letters a month); 1 posting file a day; 1 buyer file per lot; ~70 files a month | Same | Source + EST-14 |
| P3 rwb-case | New cases; open CaseWorkflows | 2,980 a month; 27,095 open | 5,213; 47,389 | Source |
| P4 rwb-access | Authorisation behind each action | 20.7 logical checks a second; ~1 network call a second after the cache | Same | Source + EST-01 |
| P5 rwb-document | Documents stored, OCR'd, classified | 71,801 a month (~3,260 a business day) | 125,580 | Source |
| P6 rwb-comms | Notices | 1,909 registered letters (source) + ~25,200 other letters + ~54,200 SMS/LINE = **~81,300 notices a month** | ~142k | Source + **EST-08** |
| P7 rwb-decision | Ledger entries; approvals | 63,131 entries a month; **~11,600 approvals a month** | 110,416 | Source + **EST-09** |
| P8 rwb-payment | Receipts matched | **Base 13,000; high 187,000 receipts a month** (~8,500 a business day, high) | Base ×1.75 | **EST-10** |
| P9 rwb-reporting | Measures and reads | 1 publish a day; **~0.9 dashboard reads a second at peak** | Same | Source + **EST-11** |
| P10 rwb-agent | Agent runs | 74,781 (screening + classification) + 1,490 route-agent runs = ~76,300 a month | ~133k | Source + EST-03 |
| S1 rwb-valuation | Route decisions; appraisals | 2,980 route decisions; 1,490 appraisals a month | 5,213; 2,606 | Source |
| S2 rwb-treatment | Treatments | ~3,000 restructures + 1,000 deeds in lieu = ~4,000 a month; 173,807 restructured accounts monitored | ~7,000 | Source |
| S3 rwb-guarantee | Guarantee and insurance claims | **~360 claims a month** | ~630 | **EST-12** |
| S4 rwb-litigation | Lawsuits; hearings | 667 a month; ~1,334 hearings | Fact today, held flat | Source |
| S5 rwb-asset | Assets taken on and sold | 720 vehicles + 29 property sales a month; 4,736 held | Same | Source |
| S6 rwb-debtsale | Accounts sold; lots | ~315 accounts a month; **~1 lot a month (~12 a year)** | Same | Source + **EST-13** |
| S7 rwb-writeoff | Write-offs | 894 a month | 1,564 | Source |
| S8 rwb-deviation | Screenings; deviations raised | 2,980 screenings; **~300 raised a month** | 5,213 | Source + **EST-15** |
| S9 rwb-partner | Instructions to partners | 320 users, 48 concurrent; **~4,520 instructions and ~9,040 results a month** | ~7,900 | Source + **EST-14** |

### 5.2 REST calls per service (peak hour)

Browser traffic is 18.3 requests a second from staff through gateway-bff and 2.4 from partners through the partner gateway (B11). The split by screen family is EST-01. The design rate is 3x peak, the same burst factor the forecast uses for view reads.

| Service | REST in (main endpoints) | Peak req/s | Design req/s | Service-to-service REST out (per month) |
|---|---|---|---|---|
| gateway-bff | `/api/recovery/**`, session cookie | 18.3 in, ~35 out (fan-out) | 105 out | All owner services, one hop, in parallel, 2 s timeout |
| P1 rwb-source-data | `GET /customers`, `/accounts`, `/collateral`, `/payments`, `/freshness` | ~11 (composite screens) + ~1 (tools and services) | 36 | SQL views: 24.8 reads a second, 74 burst |
| P2 rwb-integration | `GET /interface-runs`, `POST /retry` (operations) | < 0.1 | 2 pods, no target | Document: fetch file, ~70 |
| P3 rwb-case | `GET /cases`, `/tasks`, `POST /actions`, `/case-summary` | 6.4 | 19 | Access: authorise (cached) |
| P4 rwb-access | `POST /authorise`, `GET /me/permissions`, `/doa-limits` | 20.7 logical; ~1 network (cache misses, 08:30 sign-in burst ~0.5) | 5 | ACE Common sign-in |
| P5 rwb-document | `POST /documents`, `GET /cases/{id}/documents`, `POST /generate` | 2.2 | 7 | None |
| P6 rwb-comms | `POST /notices`, `GET /cases/{id}/notices` | 0.9 | 3 | ACE Common notification path: ~54,200 SMS/LINE (EST-08) |
| P7 rwb-decision | `GET /decisions`, `POST /approvals/{id}/decide`, `/rule-models` | 1.5 | 5 | Access: DoA limits, ~11,600 (cached) |
| P8 rwb-payment | `GET /cases/{id}/payments`, `POST /proceeds/{id}/allocate` | 0.7 | 2 | None |
| P9 rwb-reporting | `GET /dashboards`, `/reports`, `POST /reports/{id}/run` | 0.9 | 3 | None |
| P10 rwb-agent | `GET /agent-runs`, `/agent-policies` | 0.2 | 1 | Tool calls to source-data and document: ~229k a month (3 per run, EST-03); Enterprise AI endpoint ~76,300 runs |
| S1 rwb-valuation | `GET /valuation`, `POST /route-proposals` | 0.5 | 2 | Source data: collateral, ~2,980 |
| S2 rwb-treatment | `GET/POST /treatments`, `POST /offer` | 1.5 | 5 | None (Nexus in 5.4) |
| S3 rwb-guarantee | `GET/POST /guarantee-claims` | 0.2 | 1 | None |
| S4 rwb-litigation | `GET/POST /legal-actions`, `/hearings` | 1.1 | 3 | None |
| S5 rwb-asset | `GET/POST /assets`, `/listings`, `/auction-rounds` | 0.7 | 2 | None |
| S6 rwb-debtsale | `GET/POST /lots`, `/bids`, `/award` | 0.2 | 1 | None |
| S7 rwb-writeoff | `GET/POST /write-offs`, `/submit` | 0.2 | 1 | Source data: GL outcome, ~894 |
| S8 rwb-deviation | `GET/POST /deviations`, `/clear` | 0.4 | 1 | Source data: party flags, ~2,980 |
| S9 rwb-partner | Staff `/partners`, `/instructions` (0.4); partner portal `/partner/v1/*` (2.4) | 2.8 | 9 | Document: partner uploads, ~9,040 |
| **Total** | | **~21 in; ~35 internal** | | **~335k browser requests a business day (EST-01)** |

Two API pods per service carry several times these rates. No API tier needs autoscaling; HPA on CPU is a safety net only.

### 5.3 Kafka events per topic (2027)

| Topic | Events | Per month | Per business day | Kind |
|---|---|---|---|---|
| rwb.source-data.events.v1 | AceDataReady, AceDataLate | ~30 | 1 | Source |
| rwb.integration.events.v1 | FileDelivered, FileFailed | ~70 | 3 | EST-14 |
| rwb.case.events.v1 | CaseCreated 2,980; CaseAllocated 2,980; CaseTransferred ~2,710; CaseStateChanged ~54,190; TimerBreached ~1,355 | ~64,200 | ~2,900 | Source + EST-02 |
| rwb.access.events.v1 | AccessPolicyChanged, DoaLimitChanged | < 50 | ~0 | EST-02 |
| rwb.document.events.v1 | DocumentStored 71,801; DocumentFieldsExtracted ~44,700 | ~116,500 | ~5,300 | Source + EST-02 |
| rwb.comms.events.v1 | NoticeGenerated, NoticeDispatched (all); NoticeDelivered (registered) | ~164,500 (low case ~60,000) | ~7,500 | EST-08 |
| rwb.decision.events.v1 | ApprovalRequested, ApprovalDecided, RulePackageInForce | ~23,200 | ~1,050 | EST-09 |
| rwb.decision-record.v1 (shared) | DecisionRecorded from all 19 | 63,131 | ~2,870 | Source |
| rwb.payment.events.v1 | PaymentMissed ~18,700; TreatmentBooked ~4,000; ProceedsMatched ~2,100 | ~24,800 (base ~7,400) | ~1,130 | EST-10 |
| rwb.reporting.events.v1 | ReportPublished | ~22 | 1 | Source |
| rwb.agent.events.v1 | AgentRunCompleted | ~76,300 | ~3,470 | Source |
| rwb.valuation.events.v1 | RouteDecided | 2,980 | ~135 | Source |
| rwb.treatment.events.v1 | TreatmentApproved, TreatmentClosed | ~8,000 | ~360 | Source + EST-02 |
| rwb.guarantee.events.v1 | GuaranteeClaimFiled, GuaranteeClaimSettled | ~720 | ~33 | EST-12 |
| rwb.litigation.events.v1 | LawsuitFiled 667; JudgmentRecorded ~667; AuctionResult ~334 | ~1,670 | ~76 | Source + EST-02 |
| rwb.asset.events.v1 | AssetTakenOn ~750; AssetSold ~749 | ~1,500 | ~68 | Source |
| rwb.debtsale.events.v1 | LotAwarded, AccountsTransferred | ~2 | ~0 | EST-13 |
| rwb.writeoff.events.v1 | WriteOffApproved | 894 | ~41 | Source |
| rwb.deviation.events.v1 | DeviationRaised, DeviationCleared | ~600 | ~27 | EST-15 |
| rwb.partner.events.v1 | InstructionIssued ~4,520; PartnerResultSubmitted ~9,040 | ~13,560 | ~616 | EST-14 |
| **Total** | | **~563,000** | **~25,600** | Matches "tens of thousands of events a day" (slide 21) |

**Kafka sizing check.**
- Peak rate is under 10 events a second (the 16:00 notice batch and the 05:00 to 07:00 chain).
- Consumer deliveries are ~1.7M a month (about 3 consumer groups per event).
- Storage held at 7 days and RF 3 is ~131k events × ~2 KB × 3, so under 1 GB.
- 12 partitions per topic is far more than the load needs. It is kept for ordering spread and consumer parallelism, not throughput.
- This is the figure to give the ACE platform team for the quota (GAP-0280).

### 5.4 Temporal load per task queue (2027, base)

"Runs" counts new workflows plus Continue-As-New runs. Every open long-running workflow starts a new run at least every 28 days (B17).

| Queue | Workflows | New workflows a month | Open at steady state | Actions per run (EST-05) | Cross-service calls it makes (TMP / NEXUS, per month) | Peak window |
|---|---|---|---|---|---|---|
| rwb-source-data | AceIngestCheck, reconciliation | ~45 | ~0 | 20 | None (it is called: listEligibleAccounts daily, snapshot pages daily) | 05:00 to 07:00 |
| rwb-integration | none (activities only) | 0 | 0 | — | Activities deliverFile / receiveFile, ~70 | 16:00 |
| rwb-case | CaseWorkflow (parent), DailyCaseRun | 2,980 + 30 | 27,095 (CAN ~27,100 runs) | 40 per 28-day run | Children: valuation 2,980, deviation 2,980, treatment ~4,000, litigation 667, asset ~750, write-off 894, guarantee ~360, debt sale ~1 | **05:00 to 07:00 (hot)** |
| rwb-access | none (Schedule six-monthly) | ~0 | 0 | — | None | — |
| rwb-document | DocumentIntakeWorkflow | 71,801 | ~200 in flight | 15 | Agent child: classify / extract, 71,801 | **OCR bursts (hot)** |
| rwb-comms | NoticeDispatchWorkflow | ~81,300 (EST-08) | ~500 | 10 | Document generate ~27,100; decision approval ~1,909; integration deliverFile daily | **16:00 burst (hot)** |
| rwb-decision | ApprovalWorkflow; Schedules 00:01, 02:00 | ~11,600 (EST-09) | ~800 | 12 | None (it is called) | Steady |
| rwb-payment | none (activities only) | 0 | 0 | — | Activities matchPayments over ~8,500 receipts a business day in pages; postProceeds ~2,100; integration posting file daily | **05:00 to 07:00 (hot)** |
| rwb-reporting | Schedule 01:30 | ~30 | 0 | 20 | Source-data snapshot pages; integration deliverFile | 01:30 |
| rwb-agent | AgentRunWorkflow (60 s cap) | ~76,300 | ~10 in flight | 8 | Tool calls (REST, 5.2); Enterprise AI endpoint | **Bursts (hot)** |
| rwb-valuation | RouteDecisionWorkflow | 2,980 | ~700 | 25 | Agent route child 1,490; decision approval 2,980 | With new cases |
| rwb-treatment | TreatmentWorkflow; settlement and DIL sagas | ~4,000 | ~48,000 (EST-04) | 12 per monthly run | Decision approval ~4,000; document contract ~4,000; payment postProceeds ~1,000; **NEXUS restructure calculator ~6,000** | Plan due dates |
| rwb-guarantee | GuaranteeClaimWorkflow | ~360 (EST-12) | ~1,000 | 25 | Comms guarantor notice ~360; decision approval ~360 | Low |
| rwb-litigation | LitigationWorkflow (years) | 667 | ~24,000 (EST-04) | 20 per run | Partner instruction 667; comms demand notice 667; decision approval 667 | Longest-running |
| rwb-asset | AssetDisposalWorkflow; re-appraisal monthly | ~750 | ~6,200 | 25 | Partner instruction ~749; decision approval ~749; payment postProceeds ~749 | Monthly |
| rwb-debtsale | DebtSaleWorkflow (saga) | ~1 (EST-13) | ~3 | 40 | Document data room; decision; integration buyer file; payment, ~1 each | Per lot |
| rwb-writeoff | WriteOffWorkflow; scan 3rd working day | ~894 | ~300 | 25 | Decision committee approval 894; payment postProceeds 894 | Monthly peak |
| rwb-deviation | DeviationWorkflow | 2,980 | ~600 | 25 | Agent screening child 2,980 | Any time |
| rwb-partner | InstructionWorkflow (SLA timers) | ~4,520 (EST-14) | ~10,000 | 25 | None (it is called) | SLA timers |
| **Total (base)** | | **~261,000** | **~118,000** | | | |

**High scenario (EST-04).** If rwb-treatment holds one monitoring workflow with a durable due-date timer for each of the 173,807 restructured accounts, open workflows rise to ~292,000 and runs to ~550,000 a month. Temporal carries this easily: an idle workflow costs storage only. It does, however, create the largest single burst (EST-05). **The platform is sized for the high scenario.**

## 6. Temporal platform sizing

| Setting | Proposal | Reason |
|---|---|---|
| Throughput target | 100 actions a second sustained, 200 burst, at namespace level | The business-hour average is 7 to 10 a second (EST-05). The largest bursts are 16:00 notices (~12 a second) and the restructure due-date timers (~70 a second when spread over 4 hours, high scenario). A 10x margin over the average covers the 2031 growth without a change |
| History shards (`numHistoryShards`) | 512 | It **cannot be changed** after the cluster is created, so it is set once with headroom. 512 is the usual small-production value. 128 would carry today's load, but a re-shard means a new cluster and a migration |
| Server pods | frontend 2, history 2 (3 in PROD), matching 2, internal-worker 2, web 1 | Two of each for availability across nodes; RWB-PLT-E1070 AC checks 2 of 2 ready. Load needs about one pod each. History gets a third pod in PROD because it holds the shards and the timers |
| Server resources (starting point) | frontend 0.5 to 1 vCPU / 1 GB; history 1 to 2 vCPU / 2 to 4 GB; matching 0.5 to 1 vCPU / 1 GB | Small, because the load is small. These are Helm values per environment (E1070 BR8), tuned from the SIT volume test |
| Persistence | PostgreSQL, 100 GB provisioned, IOPS sized for writes; visibility in its own database | Estimated size is 20 to 32 GB in 2027 and ~45 GB in 2031 (EST-07). Temporal writes on every state change, so IOPS matter more than size. The separate visibility store follows E1070 |
| Namespace rate limit (`rwb-recovery`) | ~400 requests a second at the frontend | The cluster is shared with ACE, so a cap stops a runaway Recovery loop from starving ACE's namespace. It is 2x the burst target so normal peaks are never throttled |
| Retention | 30 days for closed workflows, then archive to Blob | Source (NF08). It keeps closed history small: ~10 to 17 GB at most |
| Continue-As-New | At stage end and at least every 28 days | Source. It keeps each history far under 51,200 events / 50 MB and keeps replay fast. It adds ~115k to 290k runs a month, which is included in EST-07 |
| Search attributes | CaseId, Stage, ProductGroup, QueueCode only | Source. Visibility rows stay small at ~1 KB each |
| Task queue partitions | Default (4) for every queue | 19 queues at under 10 tasks a second each do not need more |
| Payload size | Keep payloads to IDs and small facts (target < 10 KB); documents by reference (claim check) | The codec encrypts and enlarges payloads. Large payloads drive persistence size and replay time |
| Timer bursts | Add jitter to bulk due-date timers (spread over 2 to 4 hours, outside 05:00 to 07:00) | Without it, 87k timers on one due date fire at once and collide with the morning chain |

### Workers per service (KEDA on task-queue backlog)

| Queue | Min | Max | Activity slots per pod | Reason |
|---|---|---|---|---|
| rwb-case | 2 | 6 | 50 | The 05:00 to 07:00 chain must finish by 07:00 (NFR-013). Allocation and rebalance run over the whole open book |
| rwb-payment | 1 | 4 | 20 | Matches ~8,500 receipts a business day (high) inside the morning window, in pages |
| rwb-document | 2 | 8 | 10 (OCR is CPU-bound) | OCR target 500 pages an hour, with bursts when a hand-over pack of ~15 documents arrives |
| rwb-comms | 1 | 4 | 50 | The 16:00 batch is ~3,700 notices a business day |
| rwb-agent | 1 | 6 | 10 | Runs are capped at 60 s. Concurrency is bounded by the Enterprise AI endpoint quota, not by CPU |
| rwb-decision | 1 | 3 | 50 | Steady flow; ledger collection within 5 minutes |
| The other 13 queues | 1 (0 where scale-to-zero is allowed, NFR-PLT-016) | 2 | 20 | Hundreds to a few thousand runs a month. Scale-to-zero suits only queues with no timer-sensitive SLA (for example rwb-access, rwb-reporting, rwb-debtsale) |

## 7. Other shared components

| Component | Load | Proposal | Reason |
|---|---|---|---|
| gateway-bff | 18.3 req/s in, ~35 out | 2 pods; 2 s timeout and breaker per service (source) | Light; the pods are for availability |
| Redis session store | ~414 concurrent sessions; ~1,234 named users | Smallest HA tier | Holds sessions only, no business data (slide 20) |
| Partner gateway | 2.4 req/s; 48 concurrent | 2 pods in the DMZ | Isolation (FAPI 2.0), not load |
| ACE database connections | 19 services × (API + worker) × pods | Cap each login at 5 connections per pod (API) and 5 (worker): ~380 at minimum replicas, ~600 at maximum | 19 logins share one ACE PostgreSQL. A per-login cap protects ACE screens (risk register, slide 47) |
| Drools (in process) | ~325k evaluations a month; ~15 a second at peak | In process in each owner service; < 300 ms target | Too small to justify a separate rules service |
| Blob (WORM) | ~35 GB a month in 2027; 2.8 TB by 2031 | Hot tier for 12 months, then cool | Source volume; legal documents are write-once |

## 8. Estimates and their basis

Each estimate states its basis and its reason. Any input can be changed and the estimate recalculated.

| ID | Estimate | Basis | Reason for the choice |
|---|---|---|---|
| EST-01 | Staff REST split: case 35%, document 12%, decision 8%, treatment 8%, litigation 6%, comms 5%, reporting 5%, asset 4%, payment 4%, valuation 3%, deviation 2%, access 2%, partner (staff) 2%, write-off, debt sale, guarantee and agent 1% each. Source-data takes ~11 req/s from composite screens (18.3 × 60%). Daily: 74.5k requests at the peak hour × 9 hours × 50% load = ~335k a business day | Forecast I33 (60% of actions read account and party facts); Arch v5 slide 20 (composite screens call owners in parallel); work queues dominate officer time | The case list, case record and tasks are the officers' main screens. Every other module is opened from the case. Even a split twice as uneven leaves every service under 20 req/s |
| EST-02 | Case events: transfers 10% of open cases a month; state changes 2 per open case a month; timer breaches 5% of open cases a month. Fields extracted only for the 15-document hand-over pack per new case. Judgments match lawsuits at steady state; auctions follow half of the judgments | Inputs I16 (2 route steps a month per open case); I11 | State changes follow route steps. Generated documents need no extraction |
| EST-03 | Agent tool calls: 3 per run. Route-agent run on every second new case (1,490) | Slide 16 (screening per case, classification per document); Service volumes S1 basis (one appraisal for every second case) | An agent reads case facts and extracted fields, and the run is capped at 60 s |
| EST-04 | Open workflows: litigation 667 a month × 36 months average = ~24,000; treatment ~4,000 a month × 12 months = ~48,000; assets = 4,736 held + 2 months of vehicles; partner instructions ~10,000 (agency placements 6 months, others 1 month). High scenario adds 173,807 restructure monitors | Inputs I20, I23, I26; NFR-005, NFR-006; litigation "years" (Topics and queues) | Long-running workflows, not new starts, drive the open count and the storage |
| EST-05 | Actions per run: intake 15, agent 8, notice 10, approval 12, case 40 per 28-day run, litigation 20, treatment 12, others 25. Total ~5.7M a month (base), ~7.8M (high). Averaged over 220 business hours: 7.2 to 9.8 a second | Workflow shapes in the Temporal and Drools Design (activities per step) | Even with each figure doubled, the load stays under 20 a second on average |
| EST-06 | 512 history shards | Temporal production practice; immutable setting | Section 6 |
| EST-07 | Persistence: open workflows × 50 KB + 30 days of closed runs × 30 KB + visibility 1 KB per workflow. Base ~20 GB, high ~32 GB, 2031 ~45 GB | EST-03, EST-04; codec overhead; Continue-As-New | Section 6 |
| EST-08 | **Notices (P6):** 1 letter per open case a month = 27,095 (includes the 1,909 registered); SMS/LINE 2 per open case a month (pre-due reminder, missed-payment notice) = 54,190; total ~81,300. Low case, if SMS/LINE are recorded only by ACE Common: ~27,100 | Inputs I12 (1 document per open case a month: letters, proofs, partner reports); B13 | No source counts SMS/LINE (GAP-1603). A reminder before the due date and a notice after a miss is the usual collections pattern |
| EST-09 | **Approvals (P7):** route decisions 2,980 + treatments ~4,000 + write-offs 894 + lawsuits 667 + asset sales ~749 + registered and legal notices 1,909 + guarantee claims ~360 + lots ~1 = ~11,600 a month | Each service's contract names "Decision: child: approval" (slides 14 to 20) | Counts one approval per material action that the contracts route through rwb-decision |
| EST-10 | **Payments (P8):** base = open-case accounts 27,095 × 1.2 = 32,500 accounts, 40% paying each month = ~13,000 receipts. High = base + one installment for each of the 173,807 restructured accounts = ~187,000 receipts a month, ~8,500 a business day. Misses at 10% of expected installments = ~18,700 PaymentMissed. TreatmentBooked ~4,000. ProceedsMatched ~2,100 (assets ~749, debt-sale accounts ~315, settlements ~1,000) | Inputs I08, I26; S2 driver ("accounts under restructure monitored"); P8 consumes TreatmentApproved, AssetSold, LotAwarded, WriteOffApproved | No receipt count exists (GAP-0281, GAP-1643). PaymentMissed for restructured accounts needs every installment matched, so the high scenario sets the size. The batch runs in pages, so even the high case is minutes of work |
| EST-11 | **Dashboard reads (P9):** 5% of staff requests = ~0.9 a second at peak | EST-01 | Managers and team leads open dashboards. Officers work queues |
| EST-12 | **Guarantee claims (S3):** SSME new cases ~466 a month × 50% with a TCG guarantee claim = ~233; plus 5% of Mortgage and HP new cases (~2,515) with an insurance claim = ~126; total ~360 a month | Inputs I05 to I09 split by product | SSME lending is the main user of TCG guarantees. Insurance claims (death, disability) are a small share of secured retail lending |
| EST-13 | **Debt-sale lots (S6):** 3,783 accounts a year ÷ ~300 accounts a lot = ~12 lots a year | Inputs I25 | Volume per lot does not affect sizing. Per-lot files and sagas are tiny |
| EST-14 | **Partner instructions (S9):** law firms 667 (lawsuits) + repossession agents 720 + auction vendors ~749 + valuers 1,490 + collection agency placements 30% of new cases ~894 = ~4,520 a month; 2 results per instruction = ~9,040. Files (P2): WIN 22 + posting 22 + regulatory ~1 + buyer ~1 + inbound ~24 = ~70 a month | Inputs I20, I21, I24; S1 basis; 73 agencies (NFR-003) | Every outsourced route step becomes an instruction to a partner, and partners report progress and outcome |
| EST-15 | **Deviations raised (S8):** 10% of screenings = ~300 a month, open 2 months on average | Screening X1 to X7 on each new case | A small share of cases carry a deceased, bankrupt or similar flag |

**2031.** Case-driven figures grow ×1.75 (5,213 ÷ 2,980). User counts and the route facts (lawsuits, repossessions, letters) are held at today's value because the forecast does not grow them. The Temporal design target (100 sustained, 200 burst) and the 512 shards still hold in 2031. Only persistence grows (~45 GB).

## 9. Peak windows

| Window | What runs | Services | Load | Design response |
|---|---|---|---|---|
| 00:01 to 02:00 | Rule promote, ledger chain check | rwb-decision | Tiny | None |
| 01:30 | Measures publish | rwb-reporting, rwb-source-data snapshot | 1 run | None |
| Overnight (high scenario) | Restructure due-date timers | rwb-treatment, rwb-payment | Up to ~87k timers on a due date | Jitter over 2 to 4 hours, finished before 05:00 |
| **05:00 to 07:00** | AceDataReady → case creation, payment matching, allocation, rebalance 06:30 | rwb-source-data, rwb-case, rwb-payment, rwb-deviation, rwb-valuation | ~135 new cases, ~8,500 receipts (high), ~850 PaymentMissed | KEDA scales the case and payment workers; must finish by 07:00 |
| 08:30 to 10:00 | Sign-in, queue load | gateway-bff, rwb-access, rwb-case, rwb-source-data | 21 req/s, 74 view reads a second in a burst | Two API pods; permission cache |
| Business hours | Screens, document intake, agent runs | All | 7 to 10 Temporal actions a second | KEDA on document and agent |
| **16:00** | Notice generation, WIN file | rwb-comms, rwb-document, rwb-integration | ~3,700 notices | KEDA on the comms worker |
| Month start / 3rd working day | Re-appraisal, write-off scan | rwb-asset, rwb-writeoff | Hundreds | None |

## 10. What changes the answer

| If this moves | Effect |
|---|---|
| Growth runs at 35% instead of 15% (I09 note) | 2031 inflow is ~2.5x the base. Temporal and Kafka targets still hold. Persistence reaches ~70 GB; Blob ~4.5 TB |
| Every restructured account gets a workflow (high scenario) | Open workflows ~292k. Needs timer jitter; no change to shards |
| SMS/LINE handled only by ACE Common | rwb-comms falls to ~27,100 notices and ~60k events a month |
| Agent use extends to every interaction | Agent runs could reach ~180k a month. The limit is the Enterprise AI endpoint quota, not Temporal |
| A second workbench joins the shared Temporal cluster | Add its namespace and rate limit. 512 shards leave room |

## 11. To confirm

| Item | Estimates | Owner (role) | Needed by |
|---|---|---|---|
| Screen mix and peak usage | EST-01, EST-11 | Business lead | SIT performance test |
| Receipt count and installment pattern | EST-10 | Payments and posting owner | Wave 2 |
| SMS/LINE volume and where it is recorded | EST-08 | Communications owner with the ACE Common team | Wave 1 |
| Approval counts by type | EST-09 | Risk with the decision center owner | Wave 1 |
| Guarantee and insurance claim volume | EST-12 | Guarantee owner | Wave 3 |
| Partner instruction and result volume | EST-14 | Partner and agency manager | Wave 4 |
| Temporal shards, persistence, namespace rate limit, server resources | Section 6 | ACE platform team | Before the cluster is created (shards cannot change) |
| Kafka quota at ~563k events a month | 5.3 | ACE platform team (GAP-0280) | Wave 1 |
| Connection caps per login | Section 7 | ACE DBA | Wave 1 |
| Agent concurrency quota | Section 6 workers | Enterprise AI endpoint owner | Wave 1 |

## 12. Notes on the sources

- Architecture v5 slide 48 states "3,110 new cases a month". That is the new-account count. The forecast formula gives 2,980 cases a month for 2027 (÷1.2 accounts per case, +15% growth).
- Concurrent users appear as 414 (slide 48), ~420 (NFR-PLT-016) and 370 staff + 50 partner (NFR-002, NFR-003). The forecast formula gives 413.6.
- Rule evaluations appear as 283k to 318k a month (slides). The 2027 steady-state formula gives ~325k.
- Forecast v3 and v4 store formulas with no cached values. The figures here were calculated from the formulas; the 2031 open-case result reproduces the stated 47,389.
