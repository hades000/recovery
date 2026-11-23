SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench

# Workflow engine design

| Item | Detail |
|---|---|
| Document | Recovery Workbench workflow engine design |
| Version | 4 |
| Date | 22 November 2026 |
| Supersedes | Version 3, 16 November 2026 |
| Change | v3, 16 November 2026, D-RCV-36: case workflows run on Temporal from Epic 3 while case data stays in the ACE database, Quartz keeps Epics 1-2 and Drools runs only inside an activity (ADR-011) |
| Change | v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Decision | D-RCV-60, with ADR-011 as amended by ADR-016: one parent workflow per case with a child workflow per stage, the workflow kit for the shared parts, and Temporal Schedules in place of Quartz |
| Prepared by | Henka Group |
| Structure | CMMN 1.1, arc42 runtime view |
| Status | Draft. No approval of version 4 is recorded (ASM-B-TECH-06-1). |

# 1. The design on one page

The Workbench runs the case lifecycle on Temporal from Epic 3, and case data stays where it is today: in the ACE database, in the schema of the service that owns it. Temporal holds the workflow state, its history and its durable timers; it does not become a second case store. From this version the case is one parent workflow with a child workflow per stage in the service that owns the stage (DP-12), the parts that every stage needs are built once in the workflow kit (Arch v5 slide 23), and every scheduled job is a Temporal Schedule in its owning service instead of a Quartz job (ADR-016). ADR-011 records the decision; D-RCV-36 fixes the boundaries and D-RCV-60 realigns them to Architecture v5.

| Element | Design |
|---|---|
| Engine | Temporal, hybrid: one self-hosted cluster per environment on the ACE AKS clusters, in the ACE namespace, installed with the official Temporal Helm chart; server and Java SDK versions are pinned to the SCB IT approved release. The cluster is shared: namespace rwb-recovery, one task queue per service (19), plus rwb-platform for the platform workflows. |
| System of record | Case data remains in the ACE DB, in the schema of the service that owns it (ADR-014). Temporal holds workflow state, history and timers; no case field is copied into Temporal and no report reads Temporal as a case store. |
| Workflow per case | One parent CaseWorkflow per case, workflow ID case-{caseId} (for example case-RW-2026-000123) on task queue rwb-case, from entry to closure. Each stage runs as a child workflow on the queue of the service that owns it: RouteDecisionWorkflow (rwb-valuation), TreatmentWorkflow (rwb-treatment), GuaranteeClaimWorkflow (rwb-guarantee), LitigationWorkflow (rwb-litigation), AssetDisposalWorkflow (rwb-asset), DebtSaleWorkflow (rwb-debtsale), WriteOffWorkflow (rwb-writeoff) and DeviationWorkflow (rwb-deviation). The case workflows are the only writers of case state, and Continue-As-New runs at every stage end and at least every 28 days. Section 3.1 lists the parent, its children and their owners. |
| Workflow kit | One versioned library at L3, owned by the platform team: Approval (maker-checker, the DoA lookup as a parameter), Notify, Document intake, Agent run with rule fallback, Human task with SLA, Saga runner, Scheduled job, Partner instruction. No business term appears in its interfaces. Recovery writes only its own domain workflows at L5 and its activity contracts at L4 (section 5.2). |
| Epics 1-2 work | Quartz is retired: no job is left on Quartz, so there is no Epic 1-2 exception. Every scheduled job is a Temporal Schedule in the owning service, and where the trigger is an ACE batch-complete record the job is an event-started workflow instead (ADR-016; TE-007 keeps no new story; ASM-B-TECH-06-2). Section 5.1 lists the 20 jobs of the Architecture v5 job map. |
| Rules | Drools is embedded in the service that owns the decision and is called only inside an activity. The package version is chosen at evaluation time and written to the local decision record and to the decision log (ADR-017 amends ADR-012, T7). |
| Timers | All callers use the TimerScheduler port. Inside a workflow the stage and prescription clocks are durable timers of the owning service; the port is kept for callers outside a workflow, and its four methods do not change (section 4). |
| Decision | ADR-011 Run case workflows on Temporal, with case data in the ACE database, as amended by ADR-016: a parent workflow with a child per stage, the workflow kit, and Temporal Schedules in place of Quartz. It supersedes ADR-003. D-RCV-36 T1, T2 and T7 apply. |

# 2. CMMN elements on Temporal

CMMN 1.1 remains the design language the business reads. The model is not run by a CMMN engine: each element maps to one Temporal construct and one place where its state is held, and the mapping is complete. The counts of the v2 model are unchanged: 10 stages, 30 milestones, 150 tasks, 53 event listeners and 448 sentries.

| CMMN element | Temporal construct | Where the state is held |
|---|---|---|
| Case | Parent workflow case-{caseId} | The Temporal execution; recovery_case.id is the business key and the workflow ID is derived from it. |
| Stage | Child workflow on the owner's queue plus recovery_case.stage_code | recovery_case.stage_code, from LOV-STAGE. The workflow state names the same code, and the child runs in the service that owns the stage. |
| Milestone | Timeline row | One row on the case timeline, written by ApplyStateActivity when the milestone is reached. |
| Task | task row plus a completion signal | The task row holds the assignment, due date and status; completion arrives as a signal, never by polling. |
| Event listener | Signal handler (@SignalMethod) | The workflow signal method; the outbox keeps the event until the signal is delivered. |
| Sentry | Drools rule in an activity of the owning service | rule_row and the package version in force; the local decision record and the decision log record the rule ID and that version. |
| Case file item | Data read by activities through the service's own tables and the recovery.v_ace_* views | The ACE database. The activity builds facts, returns codes and writes nothing into workflow history. |

A case file item is never copied into workflow history. An activity reads it through the tables of its own rwb_<name> schema or a recovery.v_ace_* view (owned by rwb-source-data, DP-05), uses it to build the facts object, and returns only codes and identifiers. This keeps personal data out of Temporal and keeps the ACE database as the system of record.

# 3. How a case moves

An event is the only thing that moves a case. It arrives as a signal through the case router, is evaluated by one rule package, is recorded in the decision log, and only then changes the case. The order is fixed by REQ-DRI-005 and R-UNI-39.

| Step | What happens | If it fails |
|---|---|---|
| Case router | The inbox of rwb-case consumes the event and calls WorkflowGateway.signalWithStart(workflowId, "CaseEvent", payload) for case-{caseId}. A running CaseWorkflow takes the signal and forwards the event to the running stage child on the owner's queue; no service calls another service's workflow directly (Arch v5 slides 22 and 25). | MSG-P3-036 is returned. The outbox event stays and its delivery is retried; no state is written. |
| Signal CaseEvent | The stage child receives the signal. It carries the event ID, the event type, the business date and the idempotency key. | MSG-P3-036 is returned. The outbox event stays and its delivery is retried; no state is written. |
| EvaluateRulesActivity | Calls RuleEvaluator.evaluate(packageCode, facts, businessDate). The package version in force on the business date is chosen here and pinned in RuleResult with packageCode, packageVersion, ruleId and outputs. | NoPackageInForce is not retried. The workflow fails, nothing is written and the case does not move. |
| WriteDecisionLogActivity | Writes one decision_log_entry with the rule ID and the package version in its own transaction, in the schema of the owning service. This is the gate for the rest of the chain. | The chain stops. ApplyStateActivity is not called, the case does not move and an incident is raised (MSG-P7-003). |
| ApplyStateActivity | Applies the stage or route state, the task and the timer through the P3 case state service, using the event idempotency key. | The activity is retried with the same key; a retry after a commit returns the first result and writes no second row. |
| Timer | The next due date is stored as a timer row through TimerScheduler and as a durable timer of the owning service (section 4). | The timer is not set; the workflow fails and the E2-037 alert names the workflow and its case. |
| Outbox | Outbound work is written to outbox_event in the same transaction as the state and sent by the JOB-11 sender with retry. | The delivery stays RETRYING; after the limit it moves to the exception queue (R-UNI-33, R-UNI-36). |

One parent workflow per case serialises the signals for that case: a second CaseEvent waits until the first path completes, and the workflow processes events in arrival order rather than in parallel. The parent forwards one event at a time and keeps no case field of its own (ASM-B-TECH-06-8). The decision log write is the gate: a failure there leaves the case unchanged, raises an incident and stops the chain before any state row. The package version pinned in step 3 is written in step 4 and is never recomputed on replay. Each service writes its own decision record in its own schema; rwb-decision collects it into the central ledger within 5 minutes and seals the ledger daily (ADR-022). At a point of no return the step waits for the ledger to confirm the record (strict mode, Arch v5 slide 28; CG-B-TECH-06-3; ASM-B-TECH-06-7).

## 3.1 The parent and its children

The parent tracks the case; each stage runs where its rules and its data live, on the queue of the service that owns it (Arch v5 slide 25; DP-12).

| Workflow | Kind | Owner and task queue |
|---|---|---|
| CaseWorkflow | Parent, one per case, entry to closure | P3 rwb-case, queue rwb-case |
| RouteDecisionWorkflow | Stage child, S1 valuation and route | S1 rwb-valuation, queue rwb-valuation |
| TreatmentWorkflow | Stage child, S2 restructure, settlement and deed in lieu | S2 rwb-treatment, queue rwb-treatment |
| GuaranteeClaimWorkflow | Stage child, S3 guarantees and guarantors | S3 rwb-guarantee, queue rwb-guarantee |
| LitigationWorkflow | Stage child, S4 litigation and enforcement | S4 rwb-litigation, queue rwb-litigation |
| AssetDisposalWorkflow | Stage child, S5 assets and auction | S5 rwb-asset, queue rwb-asset |
| DebtSaleWorkflow | Stage child, S6 debt sale | S6 rwb-debtsale, queue rwb-debtsale |
| WriteOffWorkflow | Stage child, S7 write-off and recovery | S7 rwb-writeoff, queue rwb-writeoff |
| DeviationWorkflow | Stage child, S8 deviations X1-X7, can start at any time | S8 rwb-deviation, queue rwb-deviation |
| ApprovalWorkflow | Kit template, started by the stage that needs an approval | P7 rwb-decision, queue rwb-decision |

The owner of each workflow and of each task queue is the owner in the Microservice Ownership Map v1 (Workflows and activities, Services). The parent workflow ID is case-{caseId}, for example case-RW-2026-000123. The child and kit workflow IDs are Not specified in the source documents (CG-B-TECH-06-6; ASM-B-TECH-06-6): the parent generates them and only its own ID is fixed. A child uses parent close policy ABANDON, so it survives the Continue-As-New of its parent. A stage that is still running when another route is approved stays where it is: routes can run together, and each child owns its own clock.

# 4. Timers

Timers stay rows in the timer table (E1-028) in rwb_case. Every caller schedules, pauses, resumes and cancels through the TimerScheduler port. JOB-05, the five-minute check, is retired: the port is now backed by the durable timer of the workflow that owns the clock, with no change to a caller (ADR-016; ASM-B-TECH-06-2).

| Timer | Set by | What happens when it ends | Durable timer |
|---|---|---|---|
| Stage clock | Entry to a state, from the service level table (DL22) | Warning at the warning point; escalation at the end (R-UNI-30) | Schedule, pause, resume |
| Prescription clock | Case entry, from the claim type | Warning forces a litigation review (R-UNI-31). Never paused by a deviation | Schedule; never paused |
| Notice period | Delivery date on the proof of delivery | Pack assembly opens (R-LIT-15) | Schedule |
| Offer validity | Offer sent | The offer lapses and the case returns to the owner | Schedule, cancel |
| Partner service level | Instruction issued | Breach raised and re-selection (R-LIT-28) | Schedule |
| Claim deadline | Default conditions met for a guarantee | Warning to the guarantee officer (R-GUA-01) | Schedule |
| Holding age | Asset take-on | Provision steps and re-appraisal (R-DIS-06, R-DIS-09) | Schedule |

The port has four methods: schedule(TimerSpec), cancel(UUID timerId), pause(UUID timerId) and resume(UUID timerId). A workflow sets the clock as a durable timer of its own service, so a caller never writes a due date directly. The timer row in rwb_case is the audit copy and ApplyStateActivity keeps it in step with the durable timer (CG-B-TECH-06-1; ASM-B-TECH-06-10). Timers count working days from the bank holiday calendar held as reference data. A deviation pauses the stage clock; the prescription clock keeps running. The stage clock of a stage that runs as a child is paused on the instruction of the case, from the stage child itself, so that a resume returns to the exact state (CG-B-TECH-06-9; ASM-B-TECH-06-9). A durable timer survives a worker restart and an upgrade; the timer row is recovered from its own due date when the workflow reopens.

# 5. The Temporal platform

One Temporal cluster runs per environment on the ACE AKS clusters, in the ACE namespace, deployed with the official Temporal Helm chart. The facts below are frozen in D-RCV-36 T1 and are the input to E1-070 and E1-071.

| Item | Value |
|---|---|
| Clusters | One Temporal cluster per environment (DEV, SIT, UAT, PROD), on the ACE AKS clusters, deployed with the official Temporal Helm chart. Server and Java SDK versions are pinned to the release SCB IT approves at build; the approved version is recorded in Environment and Deployment Design v4. |
| Persistence | Databases temporal and temporal_visibility on the zone-redundant PostgreSQL flexible server, owned by role temporal_svc. temporal_svc has no grant on the ACE database, and no service login has a grant on the Temporal databases. |
| Namespace | rwb-recovery in each cluster (ace-collection is reserved for the ACE team). |
| Task queues | One queue per service, in namespace rwb-recovery: rwb-case (the parent CaseWorkflow, P3), rwb-treatment, rwb-guarantee, rwb-litigation, rwb-asset, rwb-debtsale, rwb-writeoff, rwb-deviation, rwb-valuation (the stage children and their activities), rwb-payment, rwb-decision, rwb-partner, rwb-document, rwb-comms, rwb-integration, rwb-agent, rwb-source-data, rwb-reporting and rwb-access (the activities and kit workflows they own), and rwb-platform for the platform workflows and Schedules of the platform team. A worker polls only its own queue and KEDA scales it on backlog. |
| Workflow IDs | case-{caseId} for the parent (for example case-RW-2026-000123); platform-smoke-{yyyymmdd} for the smoke workflow; the child workflow IDs are generated by the parent (CG-B-TECH-06-6; ASM-B-TECH-06-6). |
| Search attributes | CaseId, Stage, ProductGroup, QueueCode (Keyword). No personal data. |
| Payloads | Encrypted by the PdpaPayloadCodec (AES-GCM, key in Azure Key Vault). History never holds clear personal data. |
| Retention | 30 days for closed workflows (assumed; confirmed with DL26). Archive to Blob in E2-039. |
| Access | Temporal Web UI behind Entra ID OIDC: RW-PLATADM operate, RW-AUDIT read, RW-SECADM decode through the codec server (break-glass, logged). mTLS between worker, frontend and internal services. |
| Worker identity | SY-CASEWF (case workflows), SY-RULES (Drools evaluator). The worker of each service runs under that service's own login (DP-02). |
| Feature flags | rwb.p3.temporal (worker on or off), rwb.p3.drools (rule package endpoints). With either flag off, the endpoints return 404 and nothing else changes. |
| Parameters (through RWB-E1-042) | temporal.target, temporal.namespace, temporal.taskqueue.platform, temporal.retention.days=30, drools.kiebase.cache.max=20, rules.testcases.min=50. |

Temporal persistence is outside the 19 rwb_* schemas: the Physical Schema v6 counts 93 tables and none of them is a Temporal table. The frontend gRPC port 7233 is internal only; no Workbench endpoint proxies a case workflow call. The only Phase 1 path that starts a workflow is the smoke endpoint of E1-071. The parameters and the reference data of the platform are read through the rwb-case contracts RWB-P3-E1042-CON and RWB-P3-E1043-CON (DP-06, DP-07); rwb-platform is not one of the 19 services, it is the queue of the platform team (CG-B-TECH-06-2; ASM-B-TECH-06-3).

## 5.1 Schedules

Quartz is retired. TE-007 (scheduled jobs on Quartz) keeps no new story, no shared qrtz_* table is used, and job timing moves into the service that owns the job: a Temporal Schedule where the clock decides the start, an event-started workflow where an ACE batch-complete record decides it (Arch v5 slide 44; ADR-016; DP-10). A Schedule starts a workflow and never an activity, so every run has a history and a workflow ID, and it is created, versioned, paused and deleted with the service that owns it. The Schedule stories depend on RWB-PLT-E1071-CON, the contract of the workflow platform and the kit (DP-10). Times are Asia/Bangkok. Nine of the 20 jobs are Temporal Schedules: JOB-06, JOB-14, JOB-16, JOB-17, JOB-18, JOB-19, JOB-20, JOB-21 and JOB-22.

| Job | Name | When | Owner | Mechanism in version 4 |
|---|---|---|---|---|
| JOB-02 | Case creation | Airflow: ACE data ready | P3 rwb-case | AceDataReady to DailyCaseRun (event-started workflow) |
| JOB-03 | Morning allocation | after 02, by 07:00 | P3 rwb-case | DailyCaseRun step (event-started workflow) |
| JOB-04 | Reconciliation | Airflow: ACE data ready | P1 rwb-source-data | event-triggered workflow |
| JOB-05 | Timer check | every 5 min | all services | durable timers (retired) |
| JOB-06 | Rebalancing | 06:30 | P3 rwb-case | Temporal Schedule |
| JOB-07 | Payment matching | Airflow: ACE data ready | P8 rwb-payment | event-triggered workflow |
| JOB-08 | Booking confirmation | Airflow: ACE data ready | P8 rwb-payment | event-triggered workflow |
| JOB-10 | WIN notices | 16:00 | P6 rwb-comms with P2 rwb-integration | Airflow file window and workers |
| JOB-11 | Outbox sender | every minute | every service | outbox relay to Kafka |
| JOB-12 | Document intake | every 15 min | P5 rwb-document | event and KEDA workers |
| JOB-13 | Decision log copy | 01:00 | P7 rwb-decision | ingest is continuous (Kafka) |
| JOB-14 | Hash-chain check | 02:00 | P7 rwb-decision | Temporal Schedule |
| JOB-15 | Reporting extract | 01:30 | P9 rwb-reporting | Airflow trigger (no data lake) |
| JOB-16 | Write-off scan | monthly, 3rd working day | S7 rwb-writeoff | Temporal Schedule |
| JOB-17 | Retention | monthly, 1st Sunday | P5 rwb-document | Temporal Schedule |
| JOB-18 | Access review list | six-monthly | P4 rwb-access | Temporal Schedule |
| JOB-19 | Re-appraisal | monthly | S5 rwb-asset | Temporal Schedule |
| JOB-20 | Rule promote | 00:01 | P7 rwb-decision | Temporal Schedule to RulePackageInForce |
| JOB-21 | Stuck workflow scan | every 5 min | PLT rwb-platform | Temporal Schedule, visibility query and alert |
| JOB-22 | Smoke workflow | 06:00 | PLT rwb-platform | Temporal Schedule, starts PlatformSmokeWorkflow |

The Schedule ID, the overlap policy, the catch-up window and the pause-on-failure behaviour are Not specified in the source documents (CG-B-TECH-06-7; ASM-B-TECH-06-4). Until they are fixed, a Schedule carries the job ID as its name, no overlap, and no catch-up after downtime, and a failed run is visible through the workflow history and the E2-037 alert. The time zone is Asia/Bangkok, from the Batch and Scheduling Design v4.

## 5.2 The workflow kit

The kit is the L3 library that every stage and every other workbench composes; it holds no business term in its interfaces and it is versioned with semantic versioning, with workers pinned by Worker Versioning (Arch v5 slide 23). It is owned by the platform team and delivered with RWB-PLT-E1071, the workflow platform (RWB-PLT-WF; DP-10).

| Kit template | What it does | Used by |
|---|---|---|
| Approval | maker-checker with the DoA lookup passed as a parameter | RouteDecisionWorkflow (S1) and every DoA approval of S2, S3, S5, S6 and S7, started on rwb-decision |
| Notify | sends a notice through the rwb-comms contract | LitigationWorkflow (S4), GuaranteeClaimWorkflow (S3), TreatmentWorkflow (S2) |
| Document intake | intake, OCR, classification and field extraction through rwb-document | LitigationWorkflow (S4), AssetDisposalWorkflow (S5), DeviationWorkflow (S8) |
| Agent run with rule fallback | runs an agent and takes the rule answer after 60 s (R-UNI-32) | RouteDecisionWorkflow (S1), AssetDisposalWorkflow (S5), DeviationWorkflow (S8) |
| Human task with SLA | officer task with the warning and breach timers of R-UNI-30 | every stage workflow |
| Saga runner | local steps with a compensating action before the pivot and retries after it | TreatmentWorkflow (S2), AssetDisposalWorkflow (S5), DebtSaleWorkflow (S6), WriteOffWorkflow (S7) |
| Scheduled job | starts a workflow from a Temporal Schedule | the nine Schedules of 5.1 |
| Partner instruction | instruction, service-level timer, chase and recall through rwb-partner | LitigationWorkflow (S4), AssetDisposalWorkflow (S5), InstructionWorkflow (S9) |

The kit version, its artefact coordinates and the compatibility rule between a kit version and a worker build are Not specified in the source documents (CG-B-TECH-06-8; ASM-B-TECH-06-5). A kit change is treated like a workflow change: it needs a version guard and a replay pass before it is released, because it changes the shape of a history (section 6).

# 6. Determinism and versioning

A Temporal workflow must replay its history and reach the same result. That constraint shapes the code: the workflow decides, and every activity does the I/O.

- Workflow code is deterministic. It reads no clock, no random source, no database and no Drools package. The business date and the event ID come from the signal; the current time comes from the workflow context.

- Every side effect is an activity: EvaluateRulesActivity, WriteDecisionLogActivity, ApplyStateActivity, the outbox write and each outbound call. A child workflow is started by the parent; its own steps are activities on the owner's queue.

- A code change that alters the path is guarded by Workflow.getVersion(changeId, DEFAULT_VERSION, 1). A history recorded before the change takes the old branch; a new workflow takes the new branch.

- The replay test gate E2-040 replays recorded SIT histories on every build. A non-deterministic change fails the gate with MSG-P3-038 and blocks the merge; time-skipping tests run a 30-day timer in under a minute.

- Workers carry a build ID. A new build takes new workflows while a workflow already running finishes on the build that started it.

- The rule package version is chosen inside the activity, on the caller's business date, and pinned in RuleResult. The workflow writes that version to the decision log; replay reads the recorded activity result and never evaluates the package again.

- Continue-As-New runs at every stage end and at least every 28 days, so a run stays far below the limit of 51,200 events or 50 MB; a child uses parent close policy ABANDON, so it survives the Continue-As-New of its parent. A signal that arrives while a workflow continues as new is Not specified in the source documents (CG-B-TECH-06-5; ASM-B-TECH-06-11).

The separation means a rule change needs no workflow version: a new package version is data, and the activity picks it on the next event. A workflow code change needs a version guard and a replay pass, because it changes the shape of the history. Neither path edits a workflow history or a package version in place.

# 7. Failure handling

Failure is handled at three levels: the activity retry, the workflow and the outbox. Each level has one owner, one message and one run book entry.

| Item | Value |
|---|---|
| Initial interval | 1 second |
| Backoff coefficient | 2 |
| Maximum attempts | 10 |
| Non-retryable | NoPackageInForce |
| Applies to | EvaluateRulesActivity, WriteDecisionLogActivity, ApplyStateActivity |
| Source | E2-043 ActivityRetryPolicies |

- NoPackageInForce is a refusal, not a transient fault: the activity fails at once, the workflow fails, no decision log entry is written and no case row changes (MSG-P3-027).

- A failed decision log write stops the chain. The state activity is not called; after the retries the workflow fails, an incident is raised and the case stays where it was (MSG-P7-003).

- Every activity uses the event idempotency key. A retry after a commit finds the first row and returns it, so one event gives one decision entry and one state row (R-UNI-40).

- When Temporal is unreachable at signal time, WorkflowGateway.signalWithStart fails with MSG-P3-036. The outbox event and its delivery stay for the next attempt; nothing is lost and no case is left half-moved.

- A failed or stuck workflow is seen before a case waits: E2-037 alerts within five minutes with MSG-P3-037, and the stuck scanner uses temporal.stuck.hours = 24 (JOB-21, a Schedule on rwb-platform).

- An outbound call that keeps failing follows the outbox: retry, then the exception queue after the limit (R-UNI-33, R-UNI-36). The workflow is not held open by a partner.

- A stage child that fails after its retries leaves the parent waiting with no step that moves the case; the child start policy, its timeouts and the parent's action are Not specified in the source documents (CG-B-TECH-06-4; ASM-B-TECH-06-12).

A workflow that fails after its retries stays visible in the Temporal Web UI with its full history. RW-PLATADM may reset or terminate it, and E2-038 writes that action to the decision log; a reset reuses the recorded history and does not repeat a completed activity. The run books of E2-037 name the alert, the check and the escalation for each failure, per service, because each child runs on the queue and the run book of its owner.

# 8. Delivery by epic

Phase 1 delivers the platform, the worker and the operating model, with no live case workflow. Epic 2 proves the pattern on a reference workflow and adds the gates that make a change safe. Epic 3 builds the case workflows on that base.

| Story | Scope | Release | New stories |
|---|---|---|---|
| E1-070 | Temporal platform on the ACE AKS clusters: Helm release, temporal and temporal_visibility, rwb-recovery namespace, mTLS, OIDC Web UI, dashboard and run book. | 30 November 2026 (tentative) | RWB-PLT-E1070-CON, RWB-PLT-E1070-APP, RWB-ITG-E1070-ITG |
| E1-071 | Temporal worker and SDK in the recovery module: worker on rwb-platform, PdpaPayloadCodec, WorkflowGateway, PlatformSmokeWorkflow and the boundary test. | 30 November 2026 (tentative) | RWB-PLT-E1071-CON, RWB-PLT-E1071-APP |
| E2-037 | Observability and run books: metrics, failed and stuck workflow alerts (MSG-P3-037), schedule-to-start latency and the workflow dashboard. | 31 December 2026 (tentative) | RWB-PLT-E2037-CON, RWB-PLT-E2037-APP |
| E2-038 | Security, codec server and admin audit: break-glass decode for RW-SECADM and a decision log entry for every terminate, reset and signal. | 31 December 2026 (tentative) | RWB-PLT-E2038-CON, RWB-PLT-E2038-APP, RWB-ITG-E2038-ITG |
| E2-039 | Resilience: backup and point-in-time restore, zone failover, one-minor upgrade and the archive of closed histories to Blob. | 31 December 2026 (tentative) | RWB-PLT-E2039-CON, RWB-PLT-E2039-APP |
| E2-040 | Workflow versioning and replay gate: ReplayTestGate, encrypted history export from SIT, time-skipping base class and build ID rollout (MSG-P3-038). | 31 December 2026 (tentative) | RWB-PLT-E2040-CON, RWB-PLT-E2040-APP |
| E2-043 | Reference case workflow: signal, evaluate, decision log, state and outbox; three activities and ActivityRetryPolicies. | 31 December 2026 (tentative) | RWB-P3-E2043-CON, RWB-P3-E2043-APP, RWB-P7-E2043-APP, RWB-P3-E2043-OPS, RWB-ITG-E2043-ITG |
| Epic 3+ | One workflow per case on rwb-case, durable timers, multi-step outbound chains and the full CMMN state model. | Phase 2 | The stage stories of S1 rwb-valuation to S8 rwb-deviation, one story set per service |

The order is deliberate. E1-070 and E1-071 give Epic 3 a running, secure and observable worker before the first case workflow exists. E2-043 fixes the step order in a test-only skeleton, E2-040 makes a change to it safe, and E2-037, E2-038 and E2-039 make it operable. Epic 3 then copies one proven pattern instead of inventing one per squad.

D-RCV-60 adds three things to that sequence and moves no date. The workflow kit is part of RWB-PLT-E1071-CON, so the first stage that needs an approval or a saga composes it instead of writing it (section 5.2). The child workflow per stage is a change to E2-043 and to the stage stories of S1 to S8, each on its owner's queue (section 3.1). The Schedules replace Quartz in the owning service, and TE-007 is retired with no story, its work carried by RWB-PLT-E1071-CON and the nine Schedules of 5.1 (DP-10).

# 9. References

- ADR-011 Run case workflows on Temporal, with case data in the ACE database. It supersedes ADR-003 (DT09, DT10: no workflow engine). It is amended by ADR-016 for the child workflow per stage and for Schedules in place of Quartz.

- ADR-014 one schema and one login per service in the ACE PostgreSQL database; ADR-017 embedded Drools per service with the rule registry in rwb-decision; ADR-022 a local decision record plus a central ledger.

- D-RCV-36, decisions T1 (Temporal hybrid), T2 (Quartz for Epics 1-2), T7 (Drools only in an activity) and the platform facts in section 5. Where T2 keeps Quartz, D-RCV-60 and ADR-016 retire it: TE-007 keeps no new story.

- D-RCV-60 and DL44: adopt Architecture v5 and realign the documents and stories.

- Recovery Microservice Architecture v5: slides 22 to 25 (event travel, the five Temporal layers, the runtime, and the parent with a child per stage) and slide 44 (the job map).

- Recovery Workbench Temporal and Drools Design v1: the workflow kit, the parent and its children, and the Schedules.

- Recovery Workbench Microservice Ownership Map v1: the service, workflow, event, job and parameter owners used in sections 3.1, 5 and 5.1.

- Template and Rules v1, R5.5: DP-01 (schema per service), DP-02 (one login per service), DP-05 (ACE data through rwb-source-data), DP-06 and DP-07 (parameters and reference data), DP-10 (Schedules through the workflow kit) and DP-12 (CaseWorkflow parent with a child per stage).

- RWB-E1-070 Temporal platform on the ACE AKS clusters.

- RWB-E1-071 Temporal worker and SDK in the recovery module.

- RWB-E2-037 Temporal observability and run books.

- RWB-E2-038 Temporal security, codec server and admin audit.

- RWB-E2-039 Temporal resilience: backup, failover, upgrade and archive.

- RWB-E2-040 Workflow versioning and replay test gate.

- RWB-E2-043 Temporal and Drools integration pattern and reference case workflow.

- RWB-TE-007 Scheduled jobs on Quartz: retired under D-RCV-60, no new story.

- Recovery Workbench Rules Engine Design v3 (embedded Drools, rule packages and the decision log).

- Recovery Workbench Environment and Deployment Design v4 (pinned Temporal version and environment values).

- Recovery Workbench Batch and Scheduling Design v4 (the jobs of JOB-01 to JOB-22, their times and their Asia/Bangkok zone).

- Recovery Workbench Error and Message Standard v4 (MSG-P3-027, MSG-P3-036, MSG-P3-037, MSG-P3-038).
