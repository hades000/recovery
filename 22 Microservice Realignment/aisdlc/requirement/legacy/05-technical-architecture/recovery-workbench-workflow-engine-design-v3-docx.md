<!-- source: 05 Technical architecture/Recovery Workbench Workflow Engine Design v3.docx -->
<!-- converted: 2026-11-16 from DOCX -->

> **Source:** `05 Technical architecture/Recovery Workbench Workflow Engine Design v3.docx`  
> **Converted from:** DOCX

Recovery Workbench

Workflow engine design

SCB Collections and Recovery. Henka Group, 16 November 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench workflow engine design |
| Version | 3 |
| Date | 16 November 2026 |
| Change | v3, 16 November 2026, D-RCV-36: case workflows run on Temporal from Epic 3 while case data stays in the ACE database, Quartz keeps Epics 1-2 and Drools runs only inside an activity (ADR-011) |
| Prepared by | Henka Group |
| Structure | CMMN 1.1, arc42 runtime view |

# 1. The design on one page

The Workbench runs the case lifecycle on Temporal from Epic 3, and case data stays where it is today: in the recovery schema of the ACE database. Temporal holds the workflow state, its history and its durable timers; it does not become a second case store. Every Epic 1 and Epic 2 scheduled job stays on Quartz, and Drools is reached only from an activity. ADR-011 records the decision; D-RCV-36 fixes the boundaries.

| Element | Design |
|---|---|
| Engine | Temporal, hybrid: one self-hosted cluster per environment on the ACE AKS clusters, in the ACE namespace, installed with the official Temporal Helm chart; server and Java SDK versions are pinned to the SCB IT approved release. |
| System of record | Case data remains in the ACE DB recovery schema. Temporal holds workflow state, history and timers; no case field is copied into Temporal and no report reads Temporal as a case store. |
| Workflow per case | From Epic 3, one workflow per case, workflow ID case-{caseId} (for example case-RW-2026-000123) on task queue rwb-case. The workflow is the only writer of case state. |
| Epics 1-2 work | Quartz and Spring Batch keep every scheduled job: JOB-03 allocation, JOB-04 reconciliation, JOB-05 timer check, JOB-06 rebalance, JOB-07, JOB-08 and the rest. Temporal Schedules are not used in Epics 1 and 2. |
| Rules | Drools is embedded in the recovery module and is called only inside an activity. The package version is chosen at evaluation time and written to the decision log (ADR-012, T7). |
| Timers | All callers use the TimerScheduler port. JOB-05 is its Quartz implementation in Epics 1 and 2; Epic 3 supplies a Temporal durable timer behind the same port. |
| Decision | ADR-011 Run case workflows on Temporal, with case data in the ACE database. It supersedes ADR-003. D-RCV-36 T1, T2 and T7 apply. |

# 2. CMMN elements on Temporal

CMMN 1.1 remains the design language the business reads. The model is not run by a CMMN engine: each element maps to one Temporal construct and one place where its state is held, and the mapping is complete. The counts of the v2 model are unchanged: 10 stages, 30 milestones, 150 tasks, 53 event listeners and 448 sentries.

| CMMN element | Temporal construct | Where the state is held |
|---|---|---|
| Case | Workflow case-{caseId} | The Temporal execution; recovery_case.id is the business key and the workflow ID is derived from it. |
| Stage | Workflow state plus recovery_case.stage_code | recovery_case.stage_code, from LOV-STAGE. The workflow state names the same code. |
| Milestone | Timeline row | One row on the case timeline, written by ApplyStateActivity when the milestone is reached. |
| Task | task row plus a completion signal | The task row holds the assignment, due date and status; completion arrives as a signal, never by polling. |
| Event listener | Signal handler (@SignalMethod) | The workflow signal method; the outbox keeps the event until the signal is delivered. |
| Sentry | Drools rule in an activity | rule_row and the package version in force; the decision log records the rule ID and that version. |
| Case file item | Data read by activities through recovery.v_ace_* views and recovery tables | The ACE database. The activity builds facts, returns codes and writes nothing into workflow history. |

A case file item is never copied into workflow history. An activity reads it through the recovery tables or a recovery.v_ace_* view, uses it to build the facts object, and returns only codes and identifiers. This keeps personal data out of Temporal and keeps the ACE database as the system of record.

# 3. How a case moves

An event is the only thing that moves a case. It arrives as a signal, is evaluated by one rule package, is recorded in the decision log, and only then changes the case. The order is fixed by REQ-DRI-005 and R-UNI-39.

| Step | What happens | If it fails |
|---|---|---|
| Signal CaseEvent | The outbox relay calls WorkflowGateway.signal(workflowId, "CaseEvent", payload) for case-{caseId}. The signal carries the event ID, the event type, the business date and the idempotency key. | MSG-P3-036 is returned. The outbox event stays and its delivery is retried; no state is written. |
| EvaluateRulesActivity | Calls RuleEvaluator.evaluate(packageCode, facts, businessDate). The package version in force on the business date is chosen here and pinned in RuleResult with packageCode, packageVersion, ruleId and outputs. | NoPackageInForce is not retried. The workflow fails, nothing is written and the case does not move. |
| WriteDecisionLogActivity | Writes one decision_log_entry with the rule ID and the package version in its own transaction. This is the gate for the rest of the chain. | The chain stops. ApplyStateActivity is not called, the case does not move and an incident is raised (MSG-P7-003). |
| ApplyStateActivity | Applies the stage or route state, the task and the timer through the P3 case state service, using the event idempotency key. | The activity is retried with the same key; a retry after a commit returns the first result and writes no second row. |
| Timer | The next due date is stored as a timer row through TimerScheduler, or as a durable Temporal timer from Epic 3. | The timer is not set; the workflow fails and the E2-037 alert names the workflow and its case. |
| Outbox | Outbound work is written to outbox_event in the same transaction as the state and sent by the JOB-11 sender with retry. | The delivery stays RETRYING; after the limit it moves to the exception queue (R-UNI-33, R-UNI-36). |

One workflow per case serialises the signals for that case: a second CaseEvent waits until the first path completes, and the workflow processes events in arrival order rather than in parallel. The decision log write is the gate: a failure there leaves the case unchanged, raises an incident and stops the chain before any state row. The package version pinned in step 2 is written in step 3 and is never recomputed on replay.

# 4. Timers

Timers stay rows in the timer table (E1-028). Every caller schedules, pauses, resumes and cancels through the TimerScheduler port, and JOB-05 is its Quartz implementation in Epics 1 and 2. The same port takes a Temporal durable timer in Epic 3, with no change to a caller.

| Timer | Set by | What happens when it ends | Epics 1-2 | Epic 3+ |
|---|---|---|---|---|
| Stage clock | Entry to a state, from the service level table (DL22) | Warning at the warning point; escalation at the end (R-UNI-30) | JOB-05; schedule, pause, resume | Durable timer; pause, resume |
| Prescription clock | Case entry, from the claim type | Warning forces a litigation review (R-UNI-31). Never paused by a deviation | JOB-05; schedule, cancel (never paused) | Durable timer; never paused |
| Notice period | Delivery date on the proof of delivery | Pack assembly opens (R-LIT-15) | JOB-05; schedule | Durable timer |
| Offer validity | Offer sent | The offer lapses and the case returns to the owner | JOB-05; schedule, cancel | Durable timer; cancel |
| Partner service level | Instruction issued | Breach raised and re-selection (R-LIT-28) | JOB-05; schedule | Durable timer |
| Claim deadline | Default conditions met for a guarantee | Warning to the guarantee officer (R-GUA-01) | JOB-05; schedule | Durable timer |
| Holding age | Asset take-on | Provision steps and re-appraisal (R-DIS-06, R-DIS-09) | JOB-05; schedule | Durable timer |

The port has four methods: schedule(TimerSpec), cancel(UUID timerId), pause(UUID timerId) and resume(UUID timerId). JOB-05 checks due timers every five minutes and calls the port, so a caller never writes a due date directly. Timers count working days from the bank holiday calendar held as reference data. A deviation pauses the stage clock; the prescription clock keeps running. A Temporal durable timer survives a worker restart; a Quartz timer is recovered from the timer row on start.

# 5. The Temporal platform

One Temporal cluster runs per environment on the ACE AKS clusters, in the ACE namespace, deployed with the official Temporal Helm chart. The facts below are frozen in D-RCV-36 T1 and are the input to E1-070 and E1-071.

| Item | Value |
|---|---|
| Clusters | One Temporal cluster per environment (DEV, SIT, UAT, PROD), on the ACE AKS clusters, deployed with the official Temporal Helm chart. Server and Java SDK versions are pinned to the release SCB IT approves at build; the approved version is recorded in Environment and Deployment Design v4. |
| Persistence | Databases temporal and temporal_visibility on the zone-redundant PostgreSQL flexible server, owned by role temporal_svc. temporal_svc has no grant on the ACE database, and recovery_svc has no grant on the Temporal databases. |
| Namespace | rwb-recovery in each cluster (ace-collection is reserved for the ACE team). |
| Task queues | rwb-case (case workflows, Epic 3+), rwb-integration (multi-step outbound chains, Epic 3+), rwb-platform (smoke and health workflows, Epic 1). |
| Workflow IDs | case-{caseId} (for example case-RW-2026-000123); platform-smoke-{yyyymmdd}. |
| Search attributes | CaseId, Stage, ProductGroup, QueueCode (Keyword). No personal data. |
| Payloads | Encrypted by the PdpaPayloadCodec (AES-GCM, key in Azure Key Vault). History never holds clear personal data. |
| Retention | 30 days for closed workflows (assumed; confirmed with DL26). Archive to Blob in E2-039. |
| Access | Temporal Web UI behind Entra ID OIDC: RW-PLATADM operate, RW-AUDIT read, RW-SECADM decode through the codec server (break-glass, logged). mTLS between worker, frontend and internal services. |
| Worker identity | SY-CASEWF (case workflows), SY-RULES (Drools evaluator). |
| Feature flags | rwb.p3.temporal (worker on or off), rwb.p3.drools (rule package endpoints). With either flag off, the endpoints return 404 and nothing else changes. |
| Parameters (through RWB-E1-042) | temporal.target, temporal.namespace, temporal.taskqueue.platform, temporal.retention.days=30, drools.kiebase.cache.max=20, rules.testcases.min=50. |

Temporal persistence is outside the recovery schema: the Physical Schema v6 counts 93 tables and none of them is a Temporal table. The frontend gRPC port 7233 is internal only; no Workbench endpoint proxies a case workflow call. The only Phase 1 path that starts a workflow is the smoke endpoint of E1-071.

# 6. Determinism and versioning

A Temporal workflow must replay its history and reach the same result. That constraint shapes the code: the workflow decides, and every activity does the I/O.

- Workflow code is deterministic. It reads no clock, no random source, no database and no Drools package. The business date and the event ID come from the signal; the current time comes from the workflow context.

- Every side effect is an activity: EvaluateRulesActivity, WriteDecisionLogActivity, ApplyStateActivity, the outbox write and each outbound call.

- A code change that alters the path is guarded by Workflow.getVersion(changeId, DEFAULT_VERSION, 1). A history recorded before the change takes the old branch; a new workflow takes the new branch.

- The replay test gate E2-040 replays recorded SIT histories on every build. A non-deterministic change fails the gate with MSG-P3-038 and blocks the merge; time-skipping tests run a 30-day timer in under a minute.

- Workers carry a build ID. A new build takes new workflows while a workflow already running finishes on the build that started it.

- The rule package version is chosen inside the activity, on the caller's business date, and pinned in RuleResult. The workflow writes that version to the decision log; replay reads the recorded activity result and never evaluates the package again.

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

- When Temporal is unreachable at signal time, WorkflowGateway.signal fails with MSG-P3-036. The outbox event and its delivery stay for the next attempt; nothing is lost and no case is left half-moved.

- A failed or stuck workflow is seen before a case waits: E2-037 alerts within five minutes with MSG-P3-037, and the stuck scanner uses temporal.stuck.hours = 24.

- An outbound call that keeps failing follows the outbox: retry, then the exception queue after the limit (R-UNI-33, R-UNI-36). The workflow is not held open by a partner.

A workflow that fails after its retries stays visible in the Temporal Web UI with its full history. RW-PLATADM may reset or terminate it, and E2-038 writes that action to the decision log; a reset reuses the recorded history and does not repeat a completed activity. The run books of E2-037 name the alert, the check and the escalation for each failure.

# 8. Delivery by epic

Phase 1 delivers the platform, the worker and the operating model, with no live case workflow. Epic 2 proves the pattern on a reference workflow and adds the gates that make a change safe. Epic 3 builds the case workflows on that base.

| Story | Scope | Release |
|---|---|---|
| E1-070 | Temporal platform on the ACE AKS clusters: Helm release, temporal and temporal_visibility, rwb-recovery namespace, mTLS, OIDC Web UI, dashboard and run book. | 30 November 2026 |
| E1-071 | Temporal worker and SDK in the recovery module: worker on rwb-platform, PdpaPayloadCodec, WorkflowGateway, PlatformSmokeWorkflow and the boundary test. | 30 November 2026 |
| E2-037 | Observability and run books: metrics, failed and stuck workflow alerts (MSG-P3-037), schedule-to-start latency and the workflow dashboard. | 31 December 2026 |
| E2-038 | Security, codec server and admin audit: break-glass decode for RW-SECADM and a decision log entry for every terminate, reset and signal. | 31 December 2026 |
| E2-039 | Resilience: backup and point-in-time restore, zone failover, one-minor upgrade and the archive of closed histories to Blob. | 31 December 2026 |
| E2-040 | Workflow versioning and replay gate: ReplayTestGate, encrypted history export from SIT, time-skipping base class and build ID rollout (MSG-P3-038). | 31 December 2026 |
| E2-043 | Reference case workflow: signal, evaluate, decision log, state and outbox; three activities and ActivityRetryPolicies. | 31 December 2026 |
| Epic 3+ | One workflow per case on rwb-case, durable timers, multi-step outbound chains and the full CMMN state model. | Phase 2 |

The order is deliberate. E1-070 and E1-071 give Epic 3 a running, secure and observable worker before the first case workflow exists. E2-043 fixes the step order in a test-only skeleton, E2-040 makes a change to it safe, and E2-037, E2-038 and E2-039 make it operable. Epic 3 then copies one proven pattern instead of inventing one per squad.

# 9. References

- ADR-011 Run case workflows on Temporal, with case data in the ACE database. It supersedes ADR-003 (DT09, DT10: no workflow engine).

- D-RCV-36, decisions T1 (Temporal hybrid), T2 (Quartz for Epics 1-2), T7 (Drools only in an activity) and the platform facts in section 5.

- RWB-E1-070 Temporal platform on the ACE AKS clusters.

- RWB-E1-071 Temporal worker and SDK in the recovery module.

- RWB-E2-037 Temporal observability and run books.

- RWB-E2-038 Temporal security, codec server and admin audit.

- RWB-E2-039 Temporal resilience: backup, failover, upgrade and archive.

- RWB-E2-040 Workflow versioning and replay test gate.

- RWB-E2-043 Temporal and Drools integration pattern and reference case workflow.

- Recovery Workbench Rules Engine Design v3 (embedded Drools, rule packages and the decision log).

- Recovery Workbench Environment and Deployment Design v4 (pinned Temporal version and environment values).

- Recovery Workbench Error and Message Standard v4 (MSG-P3-027, MSG-P3-036, MSG-P3-037, MSG-P3-038).
