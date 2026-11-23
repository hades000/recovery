## What the realignment changes in the information flow
Version 5 is kept word for word; this table is the reading key. Every row is a flow of the source deck and every owner is a row of the Ownership Map v1. Slide 22 lists the nine points the source does not close.
| Version 5 says (source slide) | Version 6 | Owner | Decision |
|---|---|---|---|
| Reads the 30 views; writes in the ACE database (2, 3) | P1 alone reads the views; 19 rwb_* schemas, one login each, no cross-schema read | P1; 19 services | ADR-010, ADR-014, DP-01, DP-02 |
| One module holds case, rules, log, documents, partners (2) | P3 case · P7 decision · P5 document · S9 partner | P3, P7, P5, S9 | ADR-013 |
| Kafka only for personal data access logging (3) | Plus 19 topics rwb.<short>.events.v1 and the shared rwb.decision-record.v1 | each service | ADR-015, DP-09 |
| O04, O05: daily batch to the data lake (6) | No data lake: P9 projects from events; the O05 model-learning path stays open | P9 | ADR-018, DP-17 |
| O02: registered mail, file from the Workbench (6) | P6 writes the notice; P2 delivers the daily file (JOB-10, INT-14) | P6, P2 | DP-16 |
| O03: SMS and LINE through the ACE notification path (6) | Same path, one caller | P6 | ADR-019 |
| I13, O06: partner results and instructions (5, 6) | Partner portal and partner gateway, one owner | S9 | ADR-019 |
| I14: documents arrive at the document hub (5) | Blob with WORM, one owner | P5 | ADR-014 |
| I15: the guarantee officer enters quota and deadlines (5) | Entered on the claim that owns them | S3 | ADR-013 |
| I16: users and roles, group-to-role, iam_group (5) | P4 holds roles, scope, masking and DoA; P1 reads the view; sign-in stays ACE Common | P4, P1 | DP-08, DP-05 |
| O08: audit, PII and SOC events (6) | Unchanged: every service writes through ACE Common | each service | ADR-023 |
| The Workbench is the only system carrying the case identifier (11) | P3 owns caseId: the key of every event and the workflow ID | P3 | ADR-011, DP-12 |

## The ten platform services and the information they own
In and out per service, transcribed from the Architecture v5 service contracts (slides 14 to 20); the topic is the service's own, rwb.<short>.events.v1 (ASM-B-TECH-15-16). Wave: Rules R4 and Architecture v5 slide 38 (ASM-B-TECH-15-15).
| Code | Service and topic | Wave | Information it takes in | Information it sends out |
|---|---|---|---|---|
| P1 | rwb-source-data rwb.source-data.events.v1 | 1 | The 30 recovery.v_ace_* views, read only; the ACE batch record; the business date from Airflow | GET /customers/{id}, /accounts/{id}, /freshness; AceDataReady, AceDataLate; the ledger |
| P2 | rwb-integration rwb.integration.events.v1 | 1 | deliverFile and receiveFile tasks; the Airflow windows for WIN (16:00) and the buyer files | FileDelivered, FileFailed; the WIN file (INT-14); the encrypted buyer file (INT-25) |
| P3 | rwb-case rwb.case.events.v1 | 1 | Every case event; AceDataReady; RulePackageInForce; the CaseWorkflow parent | CaseCreated, CaseAllocated, CaseAllocationFailed, CaseTransferred, CaseStateChanged, TimerBreached |
| P4 | rwb-access rwb.access.events.v1 | 1 | POST /authorise from every service; ACE Common sign-in and group-to-role | AccessPolicyChanged, DoaLimitChanged; the DoA table and masking policies, cached |
| P5 | rwb-document rwb.document.events.v1 | 1 | POST /documents; AgentRunCompleted for classification; DocumentIntakeWorkflow | DocumentStored, DocumentFieldsExtracted; the file in Blob with WORM |
| P6 | rwb-comms rwb.comms.events.v1 | 1 | POST /notices; DeviationRaised/Cleared, TreatmentApproved, PaymentMissed, CaseStateChanged | NoticeGenerated, NoticeDispatched, NoticeDelivered; SMS and LINE through ACE Common |
| P7 | rwb-decision rwb.decision.events.v1 | 1 | DecisionRecorded from all 19; NoticeGenerated; AgentRunCompleted; ApprovalWorkflow | ApprovalRequested, ApprovalDecided, RulePackageInForce; the central ledger and its WORM seal |
| P8 | rwb-payment rwb.payment.events.v1 | 2 | AceDataReady; TreatmentApproved, LotAwarded, AssetSold, WriteOffApproved | TreatmentBooked, PaymentMissed, ProceedsMatched; the posting file through P2 |
| P9 | rwb-reporting rwb.reporting.events.v1 | 1 | Every business event as a projection; DecisionRecorded; the measures Schedule at 01:30 | ReportPublished; the regulatory extract through P2; the read model that replaces the lake |
| P10 | rwb-agent rwb.agent.events.v1 | 1 | DocumentStored and CaseCreated; AgentRunWorkflow: 60 s, then a rule result | AgentRunCompleted; case facts through P1, extracted fields through P5 |

## The nine stage services and the information they own
The stage services run as children of the CaseWorkflow on their own queue, rwb-<short>. No service reads another service's tables (DP-01); ACE data comes through P1's contract or the service's own ACE views (DP-05).
| Code | Service and topic | Wave | Information it takes in | Information it sends out |
|---|---|---|---|---|
| S1 | rwb-valuation rwb.valuation.events.v1 | 3 | RulePackageInForce; the RouteDecisionWorkflow child; collateral and appraisals through P1 | RouteDecided |
| S2 | rwb-treatment rwb.treatment.events.v1 | 2 | TreatmentBooked, PaymentMissed, DeviationRaised; the TreatmentWorkflow sagas | TreatmentApproved, TreatmentClosed; the restructure calculation through Nexus to ACE Common |
| S3 | rwb-guarantee rwb.guarantee.events.v1 | 3 | NoticeDelivered, ProceedsMatched; the quota and claim deadlines entered on the claim (I15) | GuaranteeClaimFiled, GuaranteeClaimSettled; the guarantor notice through P6 |
| S4 | rwb-litigation rwb.litigation.events.v1 | 3 | NoticeDelivered, PartnerResultSubmitted; LitigationWorkflow with Continue-As-New | LawsuitFiled, JudgmentRecorded, AuctionResult; instructions to law firms through S9 |
| S5 | rwb-asset rwb.asset.events.v1 | 2 | JudgmentRecorded, AuctionResult, ProceedsMatched; the monthly re-appraisal | AssetTakenOn, AssetSold; instructions to auction vendors through S9 |
| S6 | rwb-debtsale rwb.debtsale.events.v1 | 3 | ProceedsMatched; the data room pack from P5; the DebtSaleWorkflow saga | LotAwarded, AccountsTransferred; the buyer file through P2 (INT-25) |
| S7 | rwb-writeoff rwb.writeoff.events.v1 | 4 | AceDataReady for the GL posting (I12 through P1); ProceedsMatched; WriteOffWorkflow | WriteOffApproved |
| S8 | rwb-deviation rwb.deviation.events.v1 | 2 | CaseCreated, AceDataReady (deceased and bankrupt flags), AgentRunCompleted | DeviationRaised, DeviationCleared; party flags through P1 |
| S9 | rwb-partner rwb.partner.events.v1 | 4 | The partner portal /partner/v1/* through the partner gateway (FAPI 2.0); instruction tasks | InstructionIssued, PartnerResultSubmitted; partner uploads into P5 |

## The events that carry the information, and their owners 1/2
Every event carries IDs and facts, never personal data; the key is caseId; the producer writes its outbox in the same transaction (DP-09, ADR-015). These ten are the facts of the data, the case and the platforms.
| Event | Producer | Consumers | Topic |
|---|---|---|---|
| AceDataReady | P1 | P3, P8, S8, S7 | rwb.source-data.events.v1 |
| AceDataLate | P1 | alerts, gateway-bff banner | rwb.source-data.events.v1 |
| CaseCreated | P3 | P10, S8, P9 | rwb.case.events.v1 |
| CaseStateChanged | P3 | P6, P9 | rwb.case.events.v1 |
| DeviationRaised | S8 | P3, P6, S2 | rwb.deviation.events.v1 |
| DeviationCleared | S8 | P3, P6 | rwb.deviation.events.v1 |
| DocumentStored | P5 | P10, P3 | rwb.document.events.v1 |
| DocumentFieldsExtracted | P5 | P3 | rwb.document.events.v1 |
| PartnerResultSubmitted | S9 | S4, S5, P3 | rwb.partner.events.v1 |
| RulePackageInForce | P7 | P3, S1, S2, P8 | rwb.decision.events.v1 |

## The events that carry the information, and their owners 2/2
These nine are the working facts of a case. Architecture v5 slides 42 and 43 carry the full catalogue of 30 events; the source slides of this deck use only the rows on slides 16 and 17.
| Event | Producer | Consumers | Topic |
|---|---|---|---|
| TreatmentApproved | S2 | P6, P8 | rwb.treatment.events.v1 |
| TreatmentBooked | P8 | P3, S2 | rwb.payment.events.v1 |
| PaymentMissed | P8 | P3, S2, P6 | rwb.payment.events.v1 |
| ProceedsMatched | P8 | P3, S5, S6, S7, S3 | rwb.payment.events.v1 |
| NoticeGenerated | P6 | P7 | rwb.comms.events.v1 |
| NoticeDispatched | P6 | P9 | rwb.comms.events.v1 |
| NoticeDelivered | P6 | S4, S3, P3 | rwb.comms.events.v1 |
| WriteOffApproved | S7 | P3, P8, P9 | rwb.writeoff.events.v1 |
| DecisionRecorded | all 19 | P7 (the ledger), P9 | rwb.decision-record.v1 |

## One payment's path: from ACE to the ledger, service by service
Architecture v5 slide 22 and the Temporal and Drools design slide 14 carry the same path for PaymentMissed; every other fact in this deck travels the same way, and only the owner and the event change (ASM-B-TECH-15-1).
| Step | Where | What happens | Call type |
|---|---|---|---|
| 1 | ACE ingestion | Posts the day's payments and closes the business date (I02); outside the 19 services | Batch |
| 2 | P1 rwb-source-data | Reads v_ace_payment and v_ace_batch_status and publishes AceDataReady | Event |
| 3 | P3 rwb-case | DailyCaseRun starts on AceDataReady (JOB-02) and allocates by 07:00 (JOB-03) | Workflow |
| 4 | P8 rwb-payment | matchPayments finds no payment for the case (JOB-07) | Activity |
| 5 | P8 rwb-payment | Writes PaymentMissed to its outbox in the same transaction as the state change | Event |
| 6 | P3 rwb-case | The case router dedupes in its inbox and signals the CaseWorkflow | Signal |
| 7 | S2 rwb-treatment | The running TreatmentWorkflow evaluates R-RES-27 and starts the 30-day cure period | Activity, timer |
| 8 | S2 rwb-treatment | RecordAndApply writes the decision record, the state and the outbox in one transaction | Activity |
| 9 | P7 rwb-decision | Collects DecisionRecorded into the ledger within 5 minutes; P9 projects it | Event |

## Five call types, and the owner of each path
The five call types and their limits are Architecture v5 slides 11 and 12; the owner of each path is a row of the Ownership Map v1. Events announce, Temporal commands, REST answers people.
| Call type | What travels | Who owns the path | Contract and limit | Never |
|---|---|---|---|---|
| REST | A person waits: a screen read, or one command | gateway-bff asks the owner, one hop | OpenAPI 3.1, /v1 in the path; 2 s; GET retried once; a breaker per downstream | A call chain deeper than one hop |
| Kafka event | A fact others may react to; IDs and facts, no personal data | The producer, on its own topic | AsyncAPI 3.0, CloudEvents 1.0 binary; retry 1 min, 10 min, 1 h, then .dlt | Personal data in an event; an event used as a command |
| Temporal | A step in another service, or a long process | The service that owns the workflow or activity, queue rwb-<short> | A typed interface in a contract jar; workflow ID = the business key | I/O or personal data in workflow code |
| File | Bulk data, or a party outside the bank | P2 rwb-integration | A manifest with fileId, sha256 and record count; a SAS link, one file, 15 minutes | Data inside the message |
| SQL view | ACE source data, read only | P1 rwb-source-data, the only reader | The 30 recovery.v_ace_* views; 5 s statement timeout; read-only login | Another service reading the views or the tables |

## The shared platform: what is not one of the 19 services
These parts are named by the source slides but are not rows of the 19-service table; each flow that crosses them is named on the source slide that uses it.
| Part | Owner | What it holds | Where this deck uses it |
|---|---|---|---|
| gateway-bff and Redis | Shared platform, not a row of the Ownership Map (CG-B-TECH-15-1; ASM-B-TECH-15-4) | The session, the short-lived user JWT, at most a few parallel calls per screen | Every screen read (source slide 10) |
| Kafka | The bank's Kafka platform; one topic and ACL per service | 19 topics rwb.<short>.events.v1 and the shared rwb.decision-record.v1 | Every event on slides 16 and 17 |
| Temporal | The platform workflow kit; one queue per service | Namespace rwb-recovery, queue rwb-<short>, the CaseWorkflow and the stage children | The workflows and timers of slides 8, 9 and 18 |
| Airflow | The bank's scheduler (replaces Control-M) | The ACE ingestion DAG, the business-date hand-off, the WIN and buyer file windows, the extract | JOB-02, 04, 07, 08, 10, 15 |
| Blob with WORM | P5 rwb-document | Every file and its retention, 2.8 TB by 2031 | I14, O07 |
| The 30 recovery.v_ace_* views | P1 rwb-source-data | The only read path out of ACE source data; read-only login | I01 to I12, I16 |
| ACE Common | The ACE team, outside the 19 services | Sign-in, audit and PII logging, the shared case view, the restructure calculator, notifications | I16, O03, O08, and the DoA limits of P4 |

## The owner of each fallback when a flow does not arrive
The seven rows are source slide 8; only the owner is added. The decision to raise a task, a timer or a state change stays in the service that owns the case stage.
| When (source slide 8) | Owner | What it sends | What the user sees |
|---|---|---|---|
| An ACE source is late | P1 | AceDataLate at the cut-off; the data product marked stale | The age of the data on every screen that uses it |
| ACE refuses a feed | P1 | The last complete business date, read through v_ace_batch_status | The same, with the product marked stale |
| A weekly or monthly source is late | P1 | AceDataLate one business day after the ACE batch was due | The age of the data on the case |
| A decision input is older than its age limit | S1, S2, S4, S5, S7 | A held task naming the input and its age | Which input is out of date and how to refresh it |
| A score is missing for an account | S1 | A route decision without the score; P7 records the missing input | No score, and the reason |
| A booking is not seen on the next ACE business date | P8 | A task to the officer who recorded the booking; the case stays waiting | The booking marked as not confirmed |
| An outbound file is not acknowledged | P2 | A retry; after the third failure FileFailed and a task to the owning team | The notice marked as not sent |

## What this version leaves open
These nine points are the ones this version cannot close from the source documents; each is a row of the Gap Register and the Assumptions Register. The open decision-log rows of source slide 11 (DL06, DL30, DL43) stay open and are not repeated here.
| What is open | Placeholder and assumption | Owner role |
|---|---|---|
| The owner of gateway-bff, the Redis session and the App Gateway route; the Map has no row | CG-B-TECH-15-1; ASM-B-TECH-15-4 | Platform team, RWB-PLT-EDGE |
| The model-learning batch (O05) has no path now that the data lake is removed | CG-B-TECH-15-2; ASM-B-TECH-15-5 | Reporting and the model owner |
| Source slide 8 reads ace_batch_run, a table; ADR-010 allows the 30 views only | CG-B-TECH-15-3; ASM-B-TECH-15-6 | P1 rwb-source-data |
| Which services read the interaction ledger, and how | CG-B-TECH-15-4; ASM-B-TECH-15-7 | P1 rwb-source-data |
| Which service records a partner result, S9 or the dated data product of P1 | CG-B-TECH-15-5; ASM-B-TECH-15-8 | S9 rwb-partner |
| Users and roles: sign-in, group-to-role and the iam_group view | CG-B-TECH-15-6; ASM-B-TECH-15-9 | P4 rwb-access |
| Who builds SMS and LINE dispatch (DL30 stays open) | CG-B-TECH-15-7; ASM-B-TECH-15-10 | P6 rwb-comms |
| The WIN file window JOB-10 is written by two services | CG-B-TECH-15-8; ASM-B-TECH-15-11 | P6 and P2 |
| Two Kafka roles: PII logging and the 19 business topics | CG-B-TECH-15-9; ASM-B-TECH-15-12 | Solution architect |