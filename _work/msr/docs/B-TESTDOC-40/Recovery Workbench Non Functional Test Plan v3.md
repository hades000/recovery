SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Recovery Workbench

Non-functional test plan

| Item | Detail |
|---|---|
| Document | Recovery Workbench non-functional test plan |
| Version | 3 |
| Date | 22 November 2026 |
| Prepared by | Henka Group |
| Structure | ISO/IEC/IEEE 29119 |
| Supersedes | Non-functional test plan v2, dated 28 October 2026, whose title block reads: SCB Collections and Recovery. Henka Group, 28 October 2026; its own document control states Version 1 (CG-B-TESTDOC-40-1; ASM-B-TESTDOC-40-2) |
| Decision | D-RCV-60 microservice realignment |
| Tool | T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Status | Draft. No approval is recorded for this run (ASM-B-TESTDOC-40-1) |
| Tests | The 8 tests of the source, 82 per-service tests, 12 journey tests and 8 platform tests |
| Owners | Service codes P1 to P10 and S1 to S9 of the Microservice Ownership Map v1, and the platform epics RWB-PLT-EDGE, RWB-PLT-EVT, RWB-PLT-WF, RWB-PLT-DB, RWB-PLT-OBS, RWB-PLT-TPL and RWB-PLT-LIB |
| Dates | 28 October 2026 kept as the source date; this plan states no release date, and any release date written later is marked (tentative) (U7; DL48) |

## Change log

| Version | Date | Change | Tool |
|---|---|---|---|
| 2 | 28 October 2026 | Source version, read only and superseded by version 3; its document control states Version 1 | Not recorded in the source document |
| 3 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |

Change-log row: 3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash

# 1. Tests and pass marks

| Test | How | Pass mark | When |
|---|---|---|---|
| Load | 410 simulated users at three requests a minute for one hour against the release in SIT | 95th percentile under 2 seconds; error rate under 0.5 percent | Before each release |
| Stress | Increase to twice the busiest hour | No data loss; recovers within 10 minutes when load drops | Before E2 and E8 |
| Volume | Database loaded to the end-2027 size | Case history read under 2 seconds | Before E2 |
| Batch window | Full COLLINS load and the morning chain at 2027 volume | Allocation complete by 07:00 | Before E1 and E2 |
| Resilience | Kill a service instance; fail the database over; stop the agent platform | No lost actions; agent steps fall back to rules | Before E1 and E5 |
| Restore | Restore the database and documents to a point in time | Within the ACE recovery objectives (DL11) | Before E1 |
| Security | Container and dependency scans; access tests per role; penetration test | No finding above the bank threshold | Each release; penetration before the partner portal opens |
| Accessibility | Automated scan and keyboard checks | No level A or AA failure | Each screen |

These 8 tests are kept word for word, with their pass marks and their gates. Sections 6 to 8 add the per-service and journey tests the 19-service target needs. They change none of these pass marks and none of these gates. The accessibility test stays at "each screen"; with no screen inventory per service, section 9 keeps it as a gate on every screen of every service (CG-B-TESTDOC-40-6; ASM-B-TESTDOC-40-9).

# 2. Environment and data

SIT at production sizing where the ACE team provides it; masked data scaled to the target volume. Results are recorded against the release.

In the target, SIT holds the 19 schemas rwb_<name> in the ACE PostgreSQL database with one login per service, the shared Temporal cluster with its own persistence database, the Kafka topics rwb.<short>.events.v1 with their retry and .dlt topics, and gateway-bff with its Redis session store (Architecture v5 slides 2, 11 and 14; Ownership Map v1, Services). Each service runs an API deployment of 2 pods and a worker deployment scaled by KEDA on task-queue backlog or consumer lag (Architecture v5 slide 33). The pod sizes, the per-service connection caps and the test tools are Not specified in the source documents (CG-B-TESTDOC-40-4; ASM-B-TESTDOC-40-7).

The volume used by every test in this plan is the source volume: about 1,234 named users, about 410 users online in the busiest hour at about 21 requests a second, about 23,600 open cases at go-live and 26,500 at the end of 2027, 3,110 new accounts a month, and about 5.8 million documents and 2.8 TB by the end of 2031 (Non-functional specification v3, section 2). The 410 of the source is kept as the test load; the other readings of the same figure are 370 staff users and 50 partner users (NFR-002 and NFR-003), 48 concurrent partner users and about 420 concurrent users in total (Architecture v5 slides 33 and 48), and the difference is recorded rather than resolved (CG-B-TESTDOC-40-3; ASM-B-TESTDOC-40-6).

# 3. Who runs them

| Test | Who |
|---|---|
| Load, stress, volume, batch | QA engineers with the ACE team |
| Resilience and restore | SCB IT with the ACE team |
| Security | SCB IT security |
| Accessibility | QA engineers |
| Per-service tests, section 6.1 to 6.5 | QA team with the owning service team (suggested owner per Template and Rules R5.3) |
| Rule and agent tests, section 6.2 | QA team with the rule owners in rwb-decision |
| Data and schema isolation, section 6.4 | ACE team with the database administrator role |
| Journey tests, section 7 | QA team with the analyst of the epic and the ACE team |
| Platform tests, section 8 | DevOps team with SCB IT and the ACE team |
| Partner load and penetration, NFT-S9-01 and NFT-J-10 | SCB IT security with QA engineers |

# 4. Open targets

Recovery point and time objectives come from SCB IT under DL11.

Non-functional specification v3 leaves these targets open: NFR-022 and NFR-023 (recovery point and recovery time) under DL11; NFR-071 (document backup and restore) under DL27; NFR-028, NFR-030, NFR-031, NFR-043, NFR-047, NFR-073 and NFR-075 under DL26 (its section 5). Until they close, the restore test in section 6.4 and NFT-PLT-08 run against the ACE objectives recorded under DL11 and are re-run when a target is set (CG-B-TESTDOC-40-8; ASM-B-TESTDOC-40-12).

# 5. How to read this version

• The target is 19 services, one per module, each with its own schema rwb_<name>, login, REST base /api/recovery/<short>/v1, topic rwb.<short>.events.v1 and Temporal task queue rwb-<short> (Template and Rules R4; Ownership Map v1, Services).
• Each service has five tests: 6.1 response time and load, 6.2 rules and agents where the service evaluates a rule or calls an agent, 6.3 events, workflows and schedules, 6.4 data, isolation and restore, 6.5 security, masking and audit.
• Test IDs are new under D-RCV-60 and carry no legacy ID: NFT-<service code>-<nn> for a service test, NFT-J-<nn> for a journey test and NFT-PLT-<nn> for a shared platform test. The source names no test ID (CG-B-TESTDOC-40-2; ASM-B-TESTDOC-40-4).
• Every pass mark is a value that already exists in section 1 of this plan or in Non-functional specification v3, cited by its ID. No target is new and no business value is invented.
• Where a value does not exist in any source, the Template and Rules R9 placeholder is written and a gap row and an assumption row are raised; section 11 lists them.
• Release names E1 to E8 are kept as the source writes them and are read as the eight business epics EP01 to EP08 (U1; ASM-B-TESTDOC-40-10). Any date is tentative (U7; DL48).
• An owner is a service code of the Microservice Ownership Map v1 or a platform epic of Template and Rules R5.1. A team type is written as a role only (U3).

# 6. Non-functional tests per service

## 6.1 Response time and load per service

The load is the source load of section 1: 410 simulated users at three requests a minute for one hour. Where a service has no screen of its own, the row tests its own endpoint or its own batch path at the same load and the same data volume.

| Test ID | Service | Load and data | Pass mark | When |
|---|---|---|---|---|
| NFT-P1-01 | P1 rwb-source-data, wave 1 | 410 users on GET /api/recovery/source-data/v1 for customers, accounts, collateral, payments and freshness, at the end-2027 volume, with the 30 recovery.v_ace_* views joined to ACE | 95th percentile under 2 seconds; error rate under 0.5 percent; every view read inside its 5 second statement timeout | Before E1 and before each release |
| NFT-P2-01 | P2 rwb-integration, wave 1 | The daily WIN letters file (INT-14) and the encrypted debt-buyer files (INT-25) at 2027 volume, each as a claim-check link and a manifest of fileId, batchId, sha256 and record count | No data loss; checksum on receipt; a failed file raises FileFailed and an operator retry; recovers within 10 minutes when load drops | Before E1 and before each release |
| NFT-P3-01 | P3 rwb-case, wave 1 | 410 users on GET /api/recovery/case/v1 for cases, queues and tasks, including a case record with 50 documents, at about 26,500 open cases | 95th percentile under 2 seconds; error rate under 0.5 percent; the case record view with 50 documents loads under 2 seconds | Before E1 and before each release |
| NFT-P4-01 | P4 rwb-access, wave 1 | Authorise and me-permissions calls on every screen through gateway-bff, with the cached permission data, at 410 users | 95th percentile under 2 seconds inside the gateway budget of 0.15 s session, 0.6 s slowest call and 0.3 s merge; every service authorises the object itself | Before E1 and before each release |
| NFT-P5-01 | P5 rwb-document, wave 1 | Document intake bursts at 500 pages an hour and the 2027 volume of about 860,000 documents; the case record with 50 documents | 500 pages per hour processed; 90 percent classification correct and the rest to the review queue; the case record loads under 2 seconds | Before E1 and before each release |
| NFT-P6-01 | P6 rwb-comms, wave 1 | The 16:00 letters and notices run with the WIN file window, and 1,909 registered letters a month | 95th percentile under 2 seconds on the notice screens; every outbound contact carries a conduct check result; no notice lost when the file path is stopped | Before E1 and before each release |
| NFT-P7-01 | P7 rwb-decision, wave 1 | 283 to 318 thousand rule evaluations a month and 55 to 62 thousand decision-log entries a month, with the log at its 36 GB 2031 size | A case history reads under 2 seconds; a rule evaluation completes under 300 milliseconds at the 95th percentile; the 00:01 promote and the 02:00 chain check complete | Before E1 and before each release |
| NFT-P8-01 | P8 rwb-payment, wave 2 | Payment matching and posting in the 05:00 to 07:00 chain at 2027 volume, with the same payment posted twice | No lost actions; a duplicate posting is rejected by its idempotency key; a failed saga step is undone; recovers within 10 minutes when load drops | Before E2 and before each release |
| NFT-P9-01 | P9 rwb-reporting, wave 1 | The 01:30 measures schedule and the regulatory extract over about 26,500 open cases and 5.8 million documents by 2031, built from events and not from a data lake | Dashboard screens under 2 seconds at the 95th percentile; measures and the regulatory extract complete from the event projections; no report reads another service's tables | Before E1 and before each release |
| NFT-P10-01 | P10 rwb-agent, wave 1 | Agent runs at the busiest hour, then the same runs with the agent platform stopped | An agent answers within 60 seconds, after which the rule result is used and the case still routes; the stopped platform loses no action and falls back to rules | Before E1 and before each release |
| NFT-S1-01 | S1 rwb-valuation, wave 3 | Route decision child workflows for 3,110 new cases a month, with facts from P1 and rules from P7 | A rule evaluation completes under 300 milliseconds at the 95th percentile; the route decision and its approval are recorded before the case moves on | Before E4 and before each release |
| NFT-S2-01 | S2 rwb-treatment, wave 2 | 3,000 restructure accounts a month and 1,000 deed-in-lieu cases a month in 2027, through the saga runner | Recovers within 10 minutes when load drops; a failed saga step is undone and no action is lost; stage timers pause on a deviation | Before E2 and before each release |
| NFT-S3-01 | S3 rwb-guarantee, wave 3 | Guarantee claim child workflows at the busiest hour, with notices through P6 and documents through P5 | 95th percentile under 2 seconds on the claim screens; no action lost when a downstream is stopped; the claim route stays available | Before E4 and before each release |
| NFT-S4-01 | S4 rwb-litigation, wave 3 | 667 lawsuits filed and 720 repossessions a month, with court-date timers across a stage pause | The legal deadline never pauses; no timer is lost when a worker is stopped and restarted; the workflow resumes from history | Before E5 and before each release |
| NFT-S5-01 | S5 rwb-asset, wave 2 | 29 property sales a month, the re-appraisal schedule and the auction rounds, with asset disposal sagas | The schedule runs on the owner task queue; a failed saga step is undone; no action lost when a downstream is stopped | Before E2 and before each release |
| NFT-S6-01 | S6 rwb-debtsale, wave 3 | About 315 debt-sale accounts a month and lot awards, with the data tape masked before the data room | The tape is masked; no personal data in events; the saga is undone on failure | Before E5 and before each release |
| NFT-S7-01 | S7 rwb-writeoff, wave 4 | The monthly write-off scan on the third working day, with posting waiting for the central ledger | The scan completes on its schedule; posting retries and is never lost; the ledger confirmation is present before the balance moves | Before E6 and before each release |
| NFT-S8-01 | S8 rwb-deviation, wave 2 | Deviation screening at case creation for the seven situations X1 to X7, then the same screening with the agent platform stopped | The stage clock pauses and the legal clock does not; screening falls back to rules within 60 seconds; no case is left unscreened | Before E2 and before each release |
| NFT-S9-01 | S9 rwb-partner, wave 4 | 50 partner users online in the busiest hour, with instructions for 73 agencies, 11 to 12 law firms, 4 auction vendors and 35 buyers | 95th percentile under 2 seconds; each partner user sees only the instructions placed with their firm; penetration test with no finding above the bank threshold before the portal opens | Before E8 and before the partner portal opens |

## 6.2 Rules and agents per service

A rule evaluation is under 300 milliseconds at the 95th percentile and an agent answers within 60 seconds, after which the rule result is used (NFR-011, NFR-010, NFR-024). The rule package version is chosen at evaluation time and recorded (Temporal and Drools design).

| Test ID | Service | What is tested | Pass mark | When |
|---|---|---|---|---|
| NFT-P7-02 | P7 rwb-decision, wave 1 | Rule package load, checksum verify and swap; promotion at 00:01; chain check at 02:00; rollback in one call | A package that fails compile, schema, overlap, the default row or the 50-scenario check is refused; the version in force is recorded on every evaluation | Before E1 and at each rule version |
| NFT-P10-02 | P10 rwb-agent, wave 1 | Agent output schema check against the allowed-action list with the confidence threshold, and the fallback | A failing output falls back to the rule result; every agent write is logged with the model or agent version | Before E1 and before each release |
| NFT-S8-02 | S8 rwb-deviation, wave 2 | The screening agent inside DeviationWorkflow, with the 60 second limit | After 60 seconds the rule result is used and the case still routes | Before E2 |
| NFT-S1-02 | S1 rwb-valuation, wave 3 | The route agent and the rule evaluation inside RouteDecisionWorkflow | Rule evaluation under 300 milliseconds at the 95th percentile; the agent answers within 60 seconds or the rule result is used | Before E4 |
| NFT-S2-02 | S2 rwb-treatment, wave 2 | Rule evaluation for treatment and settlement offers in the embedded engine, under load | 300 milliseconds at the 95th percentile per evaluation; the rule version is recorded on the decision | Before E2 |
| NFT-S6-02 | S6 rwb-debtsale, wave 3 | Pricing rules for the lot and the tape, under load | 300 milliseconds at the 95th percentile; the rule version is recorded on the decision | Before E5 |

## 6.3 Events, workflows and schedules per service

Every event test uses the same pass marks: CloudEvents 1.0 in binary mode; a transactional outbox in the producer's schema; an inbox table in every consumer; an idempotent producer with acks=all; retry topics at 1 minute, 10 minutes and 1 hour, then .dlt with an alert; key = caseId and order per case (Architecture v5 slide 11).

Every workflow and schedule test uses the same pass marks: start-to-close per activity with backoff and heartbeats; the workflow ID is the business key; activities are idempotent; Continue-As-New at every stage end and at least every 28 days; the history stays far below 51,200 events or 50 MB; a worker that stops and restarts resumes from history (Temporal and Drools design). The source plan carries no pass mark for the outbox, the inbox, the retry topics or these history limits; the values above are taken from Architecture v5 slide 11 and the Temporal and Drools design (CG-B-TESTDOC-40-7; ASM-B-TESTDOC-40-5).

| Test ID | Service | Topic and queue | Workflow, schedule or job | Pass mark |
|---|---|---|---|---|
| NFT-P1-03 | P1 rwb-source-data, wave 1 | rwb.source-data.events.v1; rwb-source-data | AceIngestCheck and reconciliation; AceDataReady; AceDataLate at 05:30; JOB-04 | The shared event and workflow marks; a missing or late batch raises AceDataLate and alerts the data steward |
| NFT-P2-03 | P2 rwb-integration, wave 1 | rwb.integration.events.v1; rwb-integration | File delivery through the claim-check activity, one file per SAS link | The shared event and workflow marks; a re-delivered file is safe because fileId is unique |
| NFT-P3-03 | P3 rwb-case, wave 1 | rwb.case.events.v1; rwb-case | CaseWorkflow parent; DailyCaseRun; JOB-02 and JOB-03; JOB-06 rebalancing | The shared event and workflow marks; the parent survives a child Continue-As-New through the ABANDON close policy |
| NFT-P4-03 | P4 rwb-access, wave 1 | rwb.access.events.v1; rwb-access | JOB-18 access review list, six-monthly | The shared event and workflow marks; the schedule produces the review list on its queue |
| NFT-P5-03 | P5 rwb-document, wave 1 | rwb.document.events.v1; rwb-document | DocumentIntakeWorkflow; JOB-12; JOB-17 retention | The shared event and workflow marks; an OCR burst is absorbed by the KEDA worker pool |
| NFT-P6-03 | P6 rwb-comms, wave 1 | rwb.comms.events.v1; rwb-comms | NoticeDispatchWorkflow; JOB-10 WIN notices | The shared event and workflow marks; a stopped file path loses no notice |
| NFT-P7-03 | P7 rwb-decision, wave 1 | rwb.decision.events.v1; rwb-decision | ApprovalWorkflow; JOB-14 chain check; JOB-20 rule promote; daily ledger seal to WORM | The shared event and workflow marks; the 02:00 chain check reports a break the same day |
| NFT-P8-03 | P8 rwb-payment, wave 2 | rwb.payment.events.v1; rwb-payment | JOB-07 matchPayments; JOB-08 confirmBookings; the payment saga | The shared event and workflow marks; a stop mid-saga returns the case to its prior state |
| NFT-P9-03 | P9 rwb-reporting, wave 1 | rwb.reporting.events.v1; rwb-reporting | The 01:30 measures schedule; JOB-15 regulatory extract; snapshot pages | The shared event and workflow marks; a projection is rebuilt from the topic with no gap |
| NFT-P10-03 | P10 rwb-agent, wave 1 | rwb.agent.events.v1; rwb-agent | AgentRunWorkflow with the 60 second limit and the rule fallback | The shared event and workflow marks; a model outage falls back to rules and the run is recorded |
| NFT-S1-03 | S1 rwb-valuation, wave 3 | rwb.valuation.events.v1; rwb-valuation | RouteDecisionWorkflow as a child of the case | The shared event and workflow marks; the decision is recorded before the case moves on |
| NFT-S2-03 | S2 rwb-treatment, wave 2 | rwb.treatment.events.v1; rwb-treatment | TreatmentWorkflow; settlement and deed-in-lieu sagas; stage timers | The shared event and workflow marks; a deviation signal pauses the stage timer only |
| NFT-S3-03 | S3 rwb-guarantee, wave 3 | rwb.guarantee.events.v1; rwb-guarantee | GuaranteeClaimWorkflow | The shared event and workflow marks; the claim resumes after a downstream stop |
| NFT-S4-03 | S4 rwb-litigation, wave 3 | rwb.litigation.events.v1; rwb-litigation | LitigationWorkflow; court-date timers; enforcement steps | The shared event and workflow marks; the prescription clock is never paused by a stage pause |
| NFT-S5-03 | S5 rwb-asset, wave 2 | rwb.asset.events.v1; rwb-asset | AssetDisposalWorkflow; JOB-19 re-appraisal; auction rounds | The shared event and workflow marks; the re-appraisal schedule runs on its queue |
| NFT-S6-03 | S6 rwb-debtsale, wave 3 | rwb.debtsale.events.v1; rwb-debtsale | DebtSaleWorkflow, a saga with transfer as the pivot | The shared event and workflow marks; a failed transfer is undone by the saga |
| NFT-S7-03 | S7 rwb-writeoff, wave 4 | rwb.writeoff.events.v1; rwb-writeoff | WriteOffWorkflow; JOB-16 monthly scan on the third working day; posting | The shared event and workflow marks; posting waits for the ledger confirmation in strict mode |
| NFT-S8-03 | S8 rwb-deviation, wave 2 | rwb.deviation.events.v1; rwb-deviation | DeviationWorkflow as a child of the case; return to the stage | The shared event and workflow marks; the stage clock pauses and the legal clock does not |
| NFT-S9-03 | S9 rwb-partner, wave 4 | rwb.partner.events.v1; rwb-partner | InstructionWorkflow for law firms, auction vendors and agencies | The shared event and workflow marks; an instruction is delivered once and recorded |

## 6.4 Data, isolation and restore per service

Each service has schema rwb_<name>, its own login and its own PgBouncer pool with a connection cap and a statement timeout of 5 seconds; no service reads another service's tables (DP-01, DP-02, DP-15; Architecture v5 slides 11 and 30; Ownership Map v1, Services).

The restore pass mark for every row is the one of section 1: restore within the ACE recovery objectives under DL11, tested before the first production release and at each release after it; the documents in WORM storage and the daily ledger seal are restored with the schema (NFR-071, open under DL27). The recovery point and time targets are Not specified in the source documents (CG-B-TESTDOC-40-8; ASM-B-TESTDOC-40-12).

| Test ID | Service | Schema | What is tested | Pass mark |
|---|---|---|---|---|
| NFT-P1-04 | P1 rwb-source-data, wave 1 | rwb_source_data | The 30 recovery.v_ace_* views through one read-only login; freshness; reconciliation to the ACE account view | Only rwb-source-data reads the views; a read over 5 seconds is stopped; no unexplained variance in the daily reconciliation |
| NFT-P2-04 | P2 rwb-integration, wave 1 | rwb_integration | File manifests, checksum, re-delivery and the SAS link life of 15 minutes | A re-delivered file is safe; a bad checksum raises FileFailed and no data is moved |
| NFT-P3-04 | P3 rwb-case, wave 1 | rwb_case | Case, stage, task and timer rows; a point-in-time restore; the case history at 26,500 cases | The case history reads under 2 seconds; the restore meets the section 1 target; no other schema reads rwb_case |
| NFT-P4-04 | P4 rwb-access, wave 1 | rwb_access | Roles as data, scope, masking policy, DoA table and access log; the access review list | The access log holds every authorisation; the review list is produced six-monthly |
| NFT-P5-04 | P5 rwb-document, wave 1 | rwb_document | WORM storage, version and hold, retention schedule JOB-17, and the restore of documents | A legal type cannot be altered or deleted inside its retention period; the restore meets the section 1 target |
| NFT-P6-04 | P6 rwb-comms, wave 1 | rwb_comms | Notice records, conduct check results and the retention of notices | Every sent notice has its conduct check result; a contact without one is held |
| NFT-P7-04 | P7 rwb-decision, wave 1 | rwb_decision | Approvals, central ledger, DMN registry; the daily seal; the hash chain | A case history reads under 2 seconds at the 36 GB size; a break in the chain is reported the same day |
| NFT-P8-04 | P8 rwb-payment, wave 2 | rwb_payment | Payments, postings, idempotency keys and the replay of a posting | A duplicate is rejected; a replay leaves one posting per payment |
| NFT-P9-04 | P9 rwb-reporting, wave 1 | rwb_reporting | Measures, snapshots, steering dashboard and regulatory reports, built from events | No report reads another service's tables or a data lake copy; a snapshot is reproducible from the topic |
| NFT-P10-04 | P10 rwb-agent, wave 1 | rwb_agent | Policies, prompts, runs, guardrails and evaluations; the model and prompt version on every run | Every run is reproducible with its model and prompt version; no personal data in a workflow payload |
| NFT-S1-04 | S1 rwb-valuation, wave 3 | rwb_valuation | Valuation records and route decisions; the restore of a decision | The decision is reproducible with its rule and model version |
| NFT-S2-04 | S2 rwb-treatment, wave 2 | rwb_treatment | Treatment, offers and deed-in-lieu records; stage timers | A stage timer survives a worker restart; the record is restored with the case |
| NFT-S3-04 | S3 rwb-guarantee, wave 3 | rwb_guarantee | Claims and guarantors; the claim history | The claim history is restored with its documents and notices |
| NFT-S4-04 | S4 rwb-litigation, wave 3 | rwb_litigation | Court dates, judgments, enforcement and the prescription clock | The prescription clock is restored exactly; no date moves on a restore |
| NFT-S5-04 | S5 rwb-asset, wave 2 | rwb_asset | Assets taken on, holding, floor price, listings and auction rounds | The floor price history is kept per round; the appraisal is restored with the asset |
| NFT-S6-04 | S6 rwb-debtsale, wave 3 | rwb_debtsale | Lots, buyers and the tape; masking before the data room | The tape leaves masked; the buyer file is encrypted and re-delivery safe |
| NFT-S7-04 | S7 rwb-writeoff, wave 4 | rwb_writeoff | Write-off records, recoveries and the posting gate | Posting waits for the ledger confirmation; a recovery is posted once |
| NFT-S8-04 | S8 rwb-deviation, wave 2 | rwb_deviation | X1 to X7 screening, pause, handling and return records | The stage clock pause and resume are recorded; the legal clock is untouched |
| NFT-S9-04 | S9 rwb-partner, wave 4 | rwb_partner | Partners, firms and instructions; scope per firm | A partner reads only the instructions of their firm; the instruction history is restored |

## 6.5 Security, masking and audit per service

Every service authorises the object itself (OWASP API1 object-level authorisation) with cached permission data from rwb-access; there are no personal data in events, workflow inputs, logs or prompts; ACE data is read only through the owner's contract or the recovery.v_ace_* views; secrets live in the key store (Template and Rules R7 s17; NFR-039, NFR-040, NFR-052, NFR-053).

| Test ID | Service | Access and masking test | Pass mark |
|---|---|---|---|
| NFT-P1-05 | P1 rwb-source-data, wave 1 | One read-only login on the views; masking of party identifiers on the response | Masked at rest and in use; no write is possible through the view login |
| NFT-P2-05 | P2 rwb-integration, wave 1 | File content outside the message; PGP for outside parties; SAS link life | No data inside the message; an expired link is refused |
| NFT-P3-05 | P3 rwb-case, wave 1 | Object-level authorisation on every case, queue and task call; masking by role | A caller without the object scope is refused; masked fields stay masked |
| NFT-P4-05 | P4 rwb-access, wave 1 | Role, scope, DoA and masking policy tests per role; SSO with multi-factor | Each role sees only its scope; no policy change without the access log |
| NFT-P5-05 | P5 rwb-document, wave 1 | Document access per role; WORM for legal types; every read logged | Every read of the document store is logged; a legal document cannot be altered |
| NFT-P6-05 | P6 rwb-comms, wave 1 | Consent state per channel; the conduct check; Thai and English output | A send without consent or without a conduct check is held |
| NFT-P7-05 | P7 rwb-decision, wave 1 | Decisions, approvals and the ledger; the approver outside their DoA | No approval above the DoA limit; every action carries the rule version and the approver |
| NFT-P8-05 | P8 rwb-payment, wave 2 | Payment screens and posting; object scope on a payment | A payment outside the caller's scope is refused; posting is idempotent |
| NFT-P9-05 | P9 rwb-reporting, wave 1 | Dashboard and report access by role; masking in the extract | A report shows only the caller's scope; the regulatory extract is masked |
| NFT-P10-05 | P10 rwb-agent, wave 1 | Agent service identity; the allowed-action list; no personal data in prompts or logs | An action outside the list is refused; the prompt and the log carry no personal data |
| NFT-S1-05 | S1 rwb-valuation, wave 3 | Valuation and route data by role; the DoA check before approval | A route decision without a valid approver is not recorded |
| NFT-S2-05 | S2 rwb-treatment, wave 2 | Offer and settlement data by role; settlement authority | An offer above authority is refused |
| NFT-S3-05 | S3 rwb-guarantee, wave 3 | Claim data and guarantor data by role | A guarantor's identifiers are masked unless the role allows them |
| NFT-S4-05 | S4 rwb-litigation, wave 3 | Court and law-firm data by role; partner scoping through S9 | A law firm sees only its own instructions |
| NFT-S5-05 | S5 rwb-asset, wave 2 | Asset, appraisal and auction data by role | A bidder sees no other bid |
| NFT-S6-05 | S6 rwb-debtsale, wave 3 | The tape before the data room; buyer file encryption | The tape is masked; the key is held in the key store |
| NFT-S7-05 | S7 rwb-writeoff, wave 4 | Write-off authority and the posting gate | A write-off above authority is refused; posting needs the ledger confirmation |
| NFT-S8-05 | S8 rwb-deviation, wave 2 | Deviation reasons and evidence by role | A deviation record is visible only to the roles that need it |
| NFT-S9-05 | S9 rwb-partner, wave 4 | Partner identity, multi-factor and scope; the DMZ route | A partner account is separate from a bank account and scoped to its firm |

# 7. Journey non-functional tests

A journey test runs the six steps of the recovery journey end to end, from a missed loan to a closed case, across the services that take part (Architecture v5 slide 3). The pass marks are the source pass marks and the NFR targets named in each row.

| Test ID | Journey | Services and steps | What it proves | Pass mark | When |
|---|---|---|---|---|---|
| NFT-J-01 | Enter and take over | P1 reads the ACE batch and raises AceDataReady; P3 starts DailyCaseRun, allocates and rebalances | NFR-013, NFR-015, NFR-019 | Case list available by 07:00 on the latest completed ACE batch; allocation complete by 07:00; a late batch delays the case list and alerts, and starts no workbench load | Before E1 |
| NFT-J-02 | Choose route | P3 starts RouteDecisionWorkflow on S1; P7 records the decision; P4 checks the DoA | NFR-010, NFR-011, NFR-024, NFR-033 | Rule evaluation under 300 milliseconds; the agent answers within 60 seconds or the rule result is used; every decision is reproducible with its rule, model and prompt version | Before E4 |
| NFT-J-03 | Restructure, settlement and deed in lieu | P3 child workflow on S2; documents through P5; notices through P6; money through P8 | NFR-005, NFR-006, NFR-025 | 3,000 restructure accounts and 1,000 deed-in-lieu cases a month; a failed step is undone; no outbound action is lost | Before E2 |
| NFT-J-04 | Guarantee claim | P3 child workflow on S3; notices through P6 | NFR-024, NFR-025 | The route stays available when a downstream is stopped; every notice carries a conduct check result | Before E5 |
| NFT-J-05 | Litigation and enforcement | P3 child workflow on S4; documents through P5; instructions through S9 | NFR-025, NFR-072 | The legal deadline never pauses; court-date timers survive a worker restart; no instruction is lost | Before E5 |
| NFT-J-06 | Asset sale and auction | P3 child workflow on S5; instructions through S9; money through P8 | NFR-025, NFR-026 | The schedule runs on its queue; a failed saga step is undone; an interface failure after three retries goes to the exception queue | Before E2 |
| NFT-J-07 | Debt sale | P3 child workflow on S6; files through P2; reporting through P9 | NFR-041, NFR-025 | The tape is masked before the data room; the buyer file is encrypted; a failed transfer is undone | Before E5 |
| NFT-J-08 | Write-off and recovery | P3 child workflow on S7; the decision in P7; posting in P8 | NFR-025, NFR-026, NFR-033 | The monthly scan completes; posting waits for the ledger confirmation and is never lost; a recovery is posted once | Before E6 |
| NFT-J-09 | Collect and post | P8 matches and posts; P3 records; P7 holds the record | NFR-025, NFR-026 | Money is matched to the case and posted once; a duplicate is rejected; no action is lost when a system of record is down | Before E1 |
| NFT-J-10 | Partner exchange from outside the bank | S9 through the partner gateway in the DMZ; S2, S4 and S5 issue instructions | NFR-050, NFR-063 | 50 partner users online at the 2 second target; a penetration test before the portal opens; each user sees only their own firm's instructions | Before E8 |
| NFT-J-11 | Deviation pause and return | P3 signals S8; S8 screens with P10 and P1; the stage clock pauses | NFR-024, NFR-072 | Screening within 60 seconds or by the rule; the stage clock pauses and the legal clock does not; the case returns to its stage | Before E2 |
| NFT-J-12 | Close and report | P3 closes; P7 seals the ledger; P9 builds the measures and the regulatory extract; P2 delivers the file | NFR-033, NFR-035, NFR-069 | Every decision is reproducible; the chain check runs daily; the extract and the measures come from events with no data lake | Before E1 |

# 8. Platform and shared non-functional tests

The shared platform is not one of the 19 services: gateway-bff with its Redis session store, the Kafka topics, the Temporal cluster, the 19 schemas and logins, observability, and the documents in WORM storage (Architecture v5 slides 2 and 4; Template and Rules R5.1).

| Test ID | Platform piece and owner | What is tested | Pass mark | When |
|---|---|---|---|---|
| NFT-PLT-01 | gateway-bff and the edge, RWB-PLT-EDGE | Session check, one hop to each owner in parallel, composition, timeouts and the breaker | Session and composition inside the 1.2 second budget against the 2 second screen target; a 2 second timeout with one GET retry with jitter; a 15 minute idle timeout | Before E1 and before each release |
| NFT-PLT-02 | Kafka event platform, RWB-PLT-EVT | Topics, ACLs, outbox and inbox, retry topics and the dead-letter topic | CloudEvents 1.0 in binary mode; retry at 1 minute, 10 minutes and 1 hour, then .dlt with an alert; backward-compatible schema; no personal data in events | Before E1 and before each release |
| NFT-PLT-03 | Temporal workflow platform, RWB-PLT-WF | Namespace rwb-recovery, one task queue per service, worker stop and restart, Continue-As-New, Nexus to ACE, Worker Versioning | A stopped worker resumes from history; Continue-As-New at each stage end and at least every 28 days; history below 51,200 events or 50 MB; a replay of recorded histories passes on every new build | Before E1 and before each release |
| NFT-PLT-04 | ACE DB schemas and logins, RWB-PLT-DB | The 19 schemas and 19 logins, the PgBouncer caps, the statement timeout and per-schema monitoring | No cross-schema access; a statement over 5 seconds is stopped; a busy schema does not starve ACE; per-schema monitoring is on | Before E1 and before each release |
| NFT-PLT-05 | Observability, RWB-PLT-OBS | Traces, metrics and logs across the workflow, the decision service and the agents | One trace across services, events and workflows with W3C trace context; an alert reaches the named owner within 15 minutes | Before E1 and before each release |
| NFT-PLT-06 | Service template, libraries and pipeline, RWB-PLT-TPL and RWB-PLT-LIB | Container and dependency scans; the secret and personal-data gates; contract tests | A change with a secret, personal data in code, tests or logs, or an unapproved dependency is blocked; contract tests run in every build | Each release |
| NFT-PLT-07 | Availability, shared by all 19 services | Failover of a service instance, of the database, of Kafka, of Temporal and of the agent platform | 99.9 percent in business hours and 99.5 percent outside; no lost actions; agent steps fall back to rules; journeys pause and resume | Before E1 and before each release |
| NFT-PLT-08 | Backup and restore of the shared stores | The ACE database with its 19 schemas, the documents in WORM storage, the daily ledger seal and the Temporal persistence database | The restore meets the ACE objectives under DL11; the documents and the seal restore with the schema; the restore is repeated at each release | Before E1 and before each release |

# 9. Order by wave and gate

The wave of a service is the wave in the Ownership Map v1, Services. It matches the four delivery waves of Architecture v5 slide 38 and the wave map of Template and Rules R5.6.

| Wave | Services and platform added | Tests that must pass | Gate kept from the source |
|---|---|---|---|
| Wave 0 | RWB-PLT-TPL, RWB-PLT-LIB, RWB-PLT-WF, RWB-PLT-DB, RWB-PLT-EVT, RWB-PLT-EDGE, RWB-PLT-OBS | NFT-PLT-01 to NFT-PLT-08 | Before E1: Restore and Resilience |
| Wave 1 | P1, P2, P3, P4, P5, P6, P7, P9, P10 | The test rows NFT-<code>-01 to -05 of each of these 9 services, plus NFT-J-01, NFT-J-09 and NFT-J-12 | Before E1: Batch window, Restore and Resilience |
| Wave 2 | P8, S2, S5, S8 | The test rows NFT-<code>-01 to -05 of each of these 4 services, plus NFT-J-03, NFT-J-06 and NFT-J-11 | Before E2: Volume, Batch window and Stress |
| Wave 3 | S1, S3, S4, S6 | The test rows NFT-<code>-01 to -05 of each of these 4 services, plus NFT-J-02, NFT-J-04, NFT-J-05 and NFT-J-07 | Before E4 and E5, with Resilience before E5 |
| Wave 4 | S7, S9 | The test rows NFT-<code>-01 to -05 of each of these 2 services, plus NFT-J-08 and NFT-J-10 | Before E6 to E8, with Stress before E8 |
| Every wave | Every service in the wave | Load test of section 1 and the security scans of section 1 | Before each release; penetration before the partner portal opens |
| Every screen | Every screen of every service | Accessibility scan and keyboard checks | Each screen |

A test row of a service is one of NFT-<code>-01 in 6.1, NFT-<code>-02 in 6.2, NFT-<code>-03 in 6.3, NFT-<code>-04 in 6.4 and NFT-<code>-05 in 6.5; a service that evaluates no rule and calls no agent has no 6.2 row.

# 10. Traceability

## 10.1 The non-functional legacy keys and their new stories

The family carries 8 non-functional legacy keys. All 8 are kept with the disposition Moved (no impact) and wave 0 in the split plan, and each one is carried by a new platform story (_work/msr/plan/split_plan.json, legacy and stats: 358 legacy keys and 1,034 story slices).

| Legacy key | Legacy title | Disposition | New story | Wave | Where this plan tests it |
|---|---|---|---|---|---|
| NF-01 | Repository and pipeline baseline | Moved (no impact) | RWB-PLT-NF01-OPS | 0 | NFT-PLT-06 |
| NF-02 | Shared library baseline | Moved (no impact) | RWB-PLT-NF02-APP | 0 | NFT-PLT-06 |
| NF-03 | Environment baseline | Moved (no impact) | RWB-PLT-NF03-OPS | 0 | NFT-PLT-01 and the environment paragraph of section 2 |
| NF-04 | Secrets and configuration baseline | Moved (no impact) | RWB-PLT-NF04-OPS | 0 | NFT-PLT-06 |
| NF-05 | Quality gates baseline | Moved (no impact) | RWB-PLT-NF05-OPS | 0 | NFT-PLT-06 |
| NF-06 | Create the 19 rwb_* schemas and logins | Moved (no impact) | RWB-PLT-NF06-DB | 0 | NFT-PLT-04 and section 6.4 |
| NF-07 | Airflow edge integration | Moved (no impact) | RWB-PLT-NF07-INF | 0 | NFT-PLT-01 and NFT-J-01 |
| NF-08 | Temporal platform baseline | Moved (no impact) | RWB-PLT-NF08-INF | 0 | NFT-PLT-03 and section 6.3 |

## 10.2 The NFR IDs this plan proves

| Test group | NFR IDs proved |
|---|---|
| Section 1 and 6.1 | NFR-001, NFR-002, NFR-003, NFR-007, NFR-008, NFR-009, NFR-012, NFR-070 |
| 6.2 | NFR-010, NFR-011, NFR-024, NFR-033, NFR-055, NFR-066 |
| 6.3 | NFR-025, NFR-026, NFR-067, NFR-077 |
| 6.4 | NFR-022, NFR-023, NFR-069, NFR-071 |
| 6.5 | NFR-039, NFR-040, NFR-042, NFR-045, NFR-049, NFR-050, NFR-051, NFR-052, NFR-053, NFR-054 |
| 7 | NFR-004, NFR-005, NFR-006, NFR-013, NFR-014, NFR-015, NFR-016, NFR-017, NFR-018, NFR-019, NFR-038, NFR-041, NFR-072 |
| 8 | NFR-020, NFR-021, NFR-048, NFR-064, NFR-065, NFR-068 |
| Section 1, Accessibility | NFR-060, NFR-061, NFR-063 |

Every other requirement of Non-functional specification v3 keeps its owner and the test that document names; this plan does not change it.

# 11. Gaps and assumptions raised by this version

The rows below are candidate rows. Step D1 numbers them as GAP-nnnn and ASM-nnnn and rewrites every citation, as Template and Rules R9 requires.

| Candidate gap | Type | What is missing or in conflict | Owner role | Paired assumption |
|---|---|---|---|---|
| CG-B-TESTDOC-40-1 | Outdated | The document control states Version 1 while the file is the second version; the version and date rows cannot both be kept word for word in a next version | Document owner | ASM-B-TESTDOC-40-2 |
| CG-B-TESTDOC-40-2 | Missing | The plan names no test ID and no per-service test, so the realignment has nothing to attach a service to | QA lead | ASM-B-TESTDOC-40-4 |
| CG-B-TESTDOC-40-3 | Conflict | The user concurrency is written as about 410 in section 1 and NFR-002 and NFR-003 give 370 staff and 50 partner users, while Architecture v5 slides 33 and 48 note about 420 concurrent users and 48 concurrent partner users | Solution architect | ASM-B-TESTDOC-40-6 |
| CG-B-TESTDOC-40-4 | Missing | SIT sizing is "production sizing where the ACE team provides it" with no pod size, connection cap or test tool for any of the 19 services | ACE team with SCB IT | ASM-B-TESTDOC-40-7 |
| CG-B-TESTDOC-40-5 | Ambiguous | The When column names E1, E2, E5 and E8 and no source maps these names to the waves or to the eight business epics | Delivery lead | ASM-B-TESTDOC-40-10 |
| CG-B-TESTDOC-40-6 | Missing | Accessibility is "each screen" and no screen inventory exists per service in the plan or the architecture | Business lead | ASM-B-TESTDOC-40-9 |
| CG-B-TESTDOC-40-7 | Missing | The plan has no pass mark for the outbox and inbox, the retry topics to .dlt, or the workflow history limits that the 19-service target introduces | Solution architect | ASM-B-TESTDOC-40-5 |
| CG-B-TESTDOC-40-8 | Missing | The restore pass mark depends on the ACE recovery objectives and NFR-022 and NFR-023 are Open under DL11, so the restore test has no target of its own | IT lead with Operational Risk | ASM-B-TESTDOC-40-12 |

# 12. What this version keeps and what it changes

Kept word for word from version 2: the title and subtitle, the four sections 1 to 4 with their tables, all 8 tests with their pass marks and their When values, the environment paragraph, the who-runs table, and the open-target sentence on DL11. Every number of the source is kept: 410 users, three requests a minute, one hour, 2 seconds, 0.5 percent, twice the busiest hour, 10 minutes, end-2027, 07:00, each release, each screen, level A and AA. The date 28 October 2026 is kept as the source date; this version states no release date, and any release date written later is marked (tentative) (U7; DL48).

Changed by the realignment: the two header lines and the change-log row (Template and Rules R8.1); the document control block with the version, the decision, the tool, the status and the owner convention; the added environment paragraph for 19 schemas, one topic and one task queue per service; the new sections 5 to 12 with 82 per-service tests, 12 journey tests, 8 platform tests, the wave order, the legacy trace, the NFR coverage and the register. Every pass mark added is a value of section 1 or of Non-functional specification v3 cited by ID. No business value is invented and no date is added.

Out of scope for this version: the test data plan, the test cases, the regression suite and the user acceptance scripts, which are their own families; the rule package contents; the model choice; and the issue-tracker impact, which is written to its own file only (U6).
