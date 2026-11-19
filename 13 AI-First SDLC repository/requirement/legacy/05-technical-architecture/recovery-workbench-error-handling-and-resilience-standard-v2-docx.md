<!-- source: 05 Technical architecture/Recovery Workbench Error Handling and Resilience Standard v2.docx -->
<!-- converted: 2026-11-04 from DOCX -->

> **Source:** `05 Technical architecture/Recovery Workbench Error Handling and Resilience Standard v2.docx`  
> **Converted from:** DOCX

Recovery Workbench

Error handling and resilience standard

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench error handling and resilience standard |
| Version | 1 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Structure | arc42 crosscutting concepts |

# 1. Rules

- Every failure is caught at the boundary where it happens and is given a category and a message code.

- No failure is silent: it reaches a person, a queue or an alert with a named owner.

- A decision that cannot be recorded is not taken.

- Outbound work is never lost: it waits in the outbox and retries.

- A user sees what happened and what to do, in Thai and English, from the error and message standard.

- An agent or model failure never stops a case: the rule result is used.

# 2. Failure categories

| Category | Example | Caught where | What happens | User sees | Owner |
|---|---|---|---|---|---|
| Validation | A required field is empty | Request validation | Request refused with 422 | MSG-GEN-001 next to the field | The user |
| Access | Role lacks the right | Permission check | 403 or 404 | MSG-P4-002 or MSG-P4-003 | The user's manager |
| State conflict | Move not allowed from the current state | Workflow | 409 | MSG-P3-005 | The user |
| Concurrent change | Record changed by someone else | Version check | 409 | MSG-GEN-004 | The user |
| Decision log | Log write fails | Decision log writer | Action stopped; incident | MSG-P7-003 | Platform administrator |
| Load | Control total fails | Load checks | Load refused; previous load kept; product marked stale | MSG-P1-001 on affected screens | Data steward |
| Outbound | WIN file transfer fails | Outbox sender | Retry, then exception queue | Task to the owner | Platform administrator |
| Agent | No answer in 60 seconds | Agent runtime client | Rule result used; fallback recorded | Nothing changes for the user | Risk and model risk officer |
| Platform | Database unavailable | Service | 503; health check fails | Service unavailable page | SCB IT |

# 3. Retry

| Item | Policy |
|---|---|
| Outbound files and messages | Retry at 1, 5 and 15 minutes, then the exception queue (three retries, NFR-026 proposed) |
| Inbound loads | Check each hour until the load window closes; then the previous load stays in use |
| Agent calls | No retry inside the step; the rule result is used |
| Idempotency | Every retried action carries its idempotency key so a repeat has no effect |

# 4. What the user sees meanwhile

- A stale data product shows its business date and a warning on every screen that uses it.

- An outbound action waiting in the outbox shows as pending on the case timeline.

- A case in the exception queue shows the reason and the owner of the fix.

- During an outage the front end shows the service unavailable page and keeps unsent form input in the browser.

# 5. Recovery

| Event | Recovery |
|---|---|
| Failed load | Rerun from the job monitor after the source is fixed |
| Exception queue item | Fixed by its owner and resent; the resend is logged |
| Decision log chain break | Compliance and internal audit investigate; no entry is changed |
| Bad rule version | Previous version reloaded with an immediate date |
| Bad release | Feature flag off; previous tag redeployed if a flag does not cover it |
