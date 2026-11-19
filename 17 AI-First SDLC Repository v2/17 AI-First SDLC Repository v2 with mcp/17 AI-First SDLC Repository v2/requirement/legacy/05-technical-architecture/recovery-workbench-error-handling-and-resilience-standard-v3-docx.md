<!-- source: 05 Technical architecture/Recovery Workbench Error Handling and Resilience Standard v3.docx -->
<!-- converted: 2026-11-16 from DOCX -->

> **Source:** `05 Technical architecture/Recovery Workbench Error Handling and Resilience Standard v3.docx`  
> **Converted from:** DOCX

Recovery Workbench

Error handling and resilience standard

SCB Collections and Recovery. Henka Group, 16 November 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench error handling and resilience standard |
| Version | 3 |
| Date | 16 November 2026 |
| Change | v3, 16 November 2026, D-RCV-36: Temporal retry policy and activity idempotency, the failed decision log rule, the outbox for Epics 1 and 2, and Drools failure handling (ADR-011, ADR-012) |
| Prepared by | Henka Group |
| Structure | arc42 crosscutting concepts |

# 1. Rules

- Every failure is caught at the boundary where it happens and is given a category and a message code.

- No failure is silent: it reaches a person, a queue or an alert with a named owner.

- A decision that cannot be recorded is not taken: a failed decision log write stops the chain and the state is not applied (REQ-DRI-005, consistent with E2-043).

- Outbound work is never lost: it waits in the outbox and retries. The outbox stays for outbound work in Epics 1 and 2, and the reference workflow uses it when Temporal is unavailable.

- Temporal activities retry on their own policy, and Drools failures are refused with a message; neither falls back silently.

- A user sees what happened and what to do, in Thai and English, from the error and message standard.

- An agent or model failure never stops a case: the rule result is used.

# 2. Failure categories

| Category | Example | Caught where | What happens | User sees | Owner |
|---|---|---|---|---|---|
| Validation | A required field is empty | Request validation | Request refused with 422 | MSG-GEN-001 next to the field | The user |
| Access | Role lacks the right | Permission check | 403 or 404 | MSG-P4-002 or MSG-P4-003 | The user's manager |
| State conflict | Move not allowed from the current state | Workflow | 409 | MSG-P3-005 | The user |
| Concurrent change | Record changed by someone else | Version check | 409 | MSG-GEN-004 | The user |
| Decision log | Log write fails | Decision log writer | Action stopped; state not applied; incident (REQ-DRI-005) | MSG-P7-003 | Platform administrator |
| Load | Control total fails | Load checks | Load refused; previous load kept; product marked stale | MSG-P1-001 on affected screens | Data steward |
| Outbound | WIN file transfer fails | Outbox sender | Retry, then exception queue | Task to the owner | Platform administrator |
| Agent | No answer in 60 seconds | Agent runtime client | Rule result used; fallback recorded | Nothing changes for the user | Risk and model risk officer |
| Platform | Database unavailable | Service | 503; health check fails | Service unavailable page | SCB IT |
| Workflow | Temporal frontend is unavailable | WorkflowGateway | Start or signal refused; the event stays in the outbox for retry | MSG-P3-036 | Platform administrator |
| Workflow failed | A workflow execution fails or stops moving | Temporal server and worker | Workflow is failed or flagged stuck; the case keeps its last applied state | MSG-P3-037 | Platform administrator |
| Rule package | Compile fails at load, no version is in force, or the checksum does not match | RuleEvaluator and rule package service | Load refused, or action held; a checksum mismatch raises an incident | MSG-P3-027 with check compile, package in force or checksum | Center of excellence analyst |
| Workflow change | A workflow change fails replay | Replay test gate in the pipeline | Build fails; nothing is deployed | MSG-P3-038 | Developer, platform administrator |

# 3. Retry

| Item | Policy |
|---|---|
| Outbound files and messages | Retry at 1, 5 and 15 minutes, then the exception queue (three retries, NFR-026 proposed) |
| Inbound loads | Check each hour until the load window closes; then the previous load stays in use |
| Agent calls | No retry inside the step; the rule result is used |
| Idempotency | Every retried action carries its idempotency key so a repeat has no effect |
| Temporal activities | Default policy: initial interval 1 second, backoff coefficient 2, maximum attempts 10. NoPackageInForce is non-retryable. |
| Temporal activity idempotency | Every activity carries an idempotency key built from the workflow ID, the activity type and the step; a retry writes one row and one decision log entry. |
| Temporal workflow tasks | A workflow task failure retries on the same workflow execution; a workflow that cannot progress is failed and raises MSG-P3-037. |
| Workflow service unavailable | Start and signal return MSG-P3-036; the event stays in the outbox and the caller retries. |

# 4. What the user sees meanwhile

- A stale data product shows its business date and a warning on every screen that uses it.

- An outbound action waiting in the outbox shows as pending on the case timeline.

- A case in the exception queue shows the reason and the owner of the fix.

- During an outage the front end shows the service unavailable page and keeps unsent form input in the browser.

- When no rule package version is in force, the action is held and the case shows MSG-P3-027; the rest of the case stays usable.

- When the workflow service is unavailable, the case shows MSG-P3-036 and the outbound action shows as pending.

# 5. Recovery

| Event | Recovery |
|---|---|
| Failed load | Rerun from the job monitor after the source is fixed |
| Exception queue item | Fixed by its owner and resent; the resend is logged |
| Decision log chain break | Compliance and internal audit investigate; no entry is changed |
| Bad rule version | Previous version reloaded with an immediate date |
| Bad release | Feature flag off; previous tag redeployed if a flag does not cover it |
| Failed workflow | Retry the activity or reset the workflow after the fix; the case state is unchanged until the decision log write succeeds |
| Rule package compile failure | The load is refused; fix the workbook and load a new version; the version in force keeps serving |
| No rule package in force | Load and approve a version with today's valid-from, or hold the action; there is no silent fallback |
| Rule package checksum mismatch | The version is refused and an incident is raised; the previous version keeps serving |

# 6. Temporal and Drools

- Temporal activities retry by default with an initial interval of 1 second, a backoff coefficient of 2 and a maximum of 10 attempts. NoPackageInForce is non-retryable, so a missing rule package fails the activity at once and the action is held.

- Every activity carries an idempotency key built from the workflow ID, the activity type and the step. A retry after a timeout writes one row, one decision log entry and one outbox item.

- A workflow task failure retries the task on the same workflow execution. A workflow that cannot progress is failed, the case keeps its last applied state, and MSG-P3-037 goes to the platform administrator.

- When the workflow service is unavailable, WorkflowGateway.start and signal return MSG-P3-036. The event stays in the outbox for retry, and no case state is changed.

- A failed decision log write stops the chain and the state is not applied (REQ-DRI-005). E2-043 uses the same order: EvaluateRulesActivity, WriteDecisionLogActivity, then ApplyStateActivity.

- The outbox stays for outbound work in Epics 1 and 2. The reference workflow in E2-043 writes through the outbox before the external call, so outbound work is kept when Temporal is unavailable.

- Drools compile failure at load is refused with MSG-P3-027 and check compile; no version is written. When no version is in force, RuleEvaluator raises NoPackageInForce, the action is held, and MSG-P3-027 names the package and check package in force.

- A checksum mismatch between the stored DRL and the recorded checksum refuses the version at load into the KieBase cache and raises an incident to RW-PLATADM. The previous version keeps serving.

- A workflow change that fails the replay test fails the build with MSG-P3-038; nothing is deployed. A role without the right gets MSG-P4-002.

# 7. Message map

| Failure | Message |
|---|---|
| Rule package compile failure at load | MSG-P3-027 with check compile |
| No rule package version in force | MSG-P3-027 with check package in force; the action is held |
| Rule package checksum mismatch | MSG-P3-027 with check checksum; an incident is raised |
| Workflow service unavailable | MSG-P3-036 |
| Workflow failed or stuck | MSG-P3-037 |
| Workflow change fails replay | MSG-P3-038 |
| Role lacks the right | MSG-P4-002 |
| Decision log write failure | MSG-P7-003 |

- These are the only messages used for the Temporal and Drools failures in this standard. No message ID is added by this standard.
