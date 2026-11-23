SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Recovery Workbench

Error handling and resilience standard

| Item | Detail |
|---|---|
| Document | Recovery Workbench error handling and resilience standard |
| Version | 4 |
| Date | 22 November 2026 |
| Change | v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Prepared by | Henka Group |
| Structure | arc42 crosscutting concepts |
| Status | Draft. No approval is recorded for this version (ASM-B-TECH-10-1) |
| Source version | 3, 16 November 2026 |
| Tool | T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60 |

# Change log

| Version | Date | Change |
|---|---|---|
| v4 | 22 November 2026 | v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash. 2 s REST timeout, one REST hop, retry and .dlt rules per service: sections 1, 2, 3, 4, 5, 6, 7 and the new section 8; the change table sits at the end of the document |
| v3 | 16 November 2026 | v3, 16 November 2026, D-RCV-36: Temporal retry policy and activity idempotency, the failed decision log rule, the outbox for Epics 1 and 2, and Drools failure handling (ADR-011, ADR-012) |

# 1. Rules

- Every failure is caught at the boundary where it happens and is given a category and a message code.

- No failure is silent: it reaches a person, a queue or an alert with a named owner.

- A decision that cannot be recorded is not taken: a failed decision log write stops the chain and the state is not applied (REQ-DRI-005, consistent with E2-043).

- Outbound work is never lost: it waits in the outbox and retries. The outbox stays for outbound work in Epics 1 and 2, and the reference workflow uses it when Temporal is unavailable.

- Temporal activities retry on their own policy, and Drools failures are refused with a message; neither falls back silently.

- A user sees what happened and what to do, in Thai and English, from the error and message standard.

- An agent or model failure never stops a case: the rule result is used.

- A REST call is one hop and has a 2 s timeout. gateway-bff calls each owner directly and in parallel; a service never calls another service to answer a screen, and anything longer is a workflow (Architecture v5 slides 10 and 11; ADR-020).

- A GET retries once with jitter inside the 2 s budget, with a circuit breaker and a bulkhead per downstream. A POST is not retried automatically and carries its Idempotency-Key (Architecture v5 slide 11).

- An event that a consumer cannot handle is retried at 1 minute, 10 minutes and 1 hour on the retry topics of the owner's topic rwb.<short>.events.v1 and then goes to its .dlt topic with an alert. The inbox records ce_id, so a retry or a redelivery acts once (Architecture v5 slides 11 and 22; ADR-015; DP-09).

- Version 4 reads the outbox rule above for every service: the transactional outbox and the inbox are library objects in all 19 schemas, one copy in each owner's schema (Architecture v5 slides 20 and 22; DP-09). The Epic 1 and Epic 2 wording is kept as the as-built position, not as the target scope (CG-B-TECH-10-2; ASM-B-TECH-10-2).

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
| REST timeout | A hop does not answer within 2 s | REST client at the caller (gateway-bff, or the calling service) | The call ends at 2 s; the breaker opens for that downstream; a GET is retried once with jitter; a command is refused | RFC 9457 problem detail on that panel; the rest of the screen stays usable (ASM-B-TECH-10-4) | Platform administrator |
| Call chain | A service calls another service to answer a screen | Trace analysis and the contract test | The call is refused at design and build time; a trace with call depth above one is flagged | Nothing changes for the user | Developer |
| Event retry | A consumer fails to handle an event | Inbox and retry topics of the owner's topic | Retried at 1 minute, 10 minutes and 1 hour, then moved to the .dlt topic with an alert | Nothing changes for the user | Platform administrator |
| Duplicate event | The same ce_id is delivered twice | Inbox (processed_event) in the consumer's own schema | The second copy writes nothing; one row and one decision record | Nothing changes for the user | Platform administrator |
| Dead letter | An event exhausts the three retries | .dlt topic of the owner's topic | The event is parked with its ce_id and its case key; an alert is raised; the replay tool resends it after the fix | Nothing changes for the user until the replay | Platform administrator (ASM-B-TECH-10-5) |

The retry topics and the .dlt topic belong to the service that owns the topic, one set per service; the owner of every topic is the service recorded in the Microservice Ownership Map v1, Services sheet. The exact names of the three retry topics and of the dead-letter topic are Not specified in the source documents (CG-B-TECH-10-1; ASM-B-TECH-10-3).

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
| REST calls | A hop answers within 2 s or the call ends. A GET retries once with jitter inside the budget; a POST is not retried automatically and carries its Idempotency-Key (Architecture v5 slides 10 and 11; ADR-020). |
| REST call depth | One hop. gateway-bff calls the owner, or reads a cached reference from rwb-access or rwb-source-data; a second service call on the same request is refused and the work becomes a workflow (Architecture v5 slide 11). |
| Event consumers | Retry topics at 1 minute, 10 minutes and 1 hour, then the .dlt topic with an alert and the replay tool. One consumer group per service, and one inbox row per ce_id (Architecture v5 slides 11 and 22). |
| Kafka broker unavailable | The producer's outbox keeps the event and the relay publishes it when Kafka returns; nothing is lost from the outbox (Architecture v5 slide 22). |
| REST calls inside an activity | The same 2 s timeout applies; the activity policy of section 6 is what repeats the call, not the REST client (Architecture v5 slide 11). |

# 4. What the user sees meanwhile

- A stale data product shows its business date and a warning on every screen that uses it.

- An outbound action waiting in the outbox shows as pending on the case timeline.

- A case in the exception queue shows the reason and the owner of the fix.

- During an outage the front end shows the service unavailable page and keeps unsent form input in the browser.

- When no rule package version is in force, the action is held and the case shows MSG-P3-027; the rest of the case stays usable.

- When the workflow service is unavailable, the case shows MSG-P3-036 and the outbound action shows as pending.

- When a REST hop times out, only the panel that needed it shows the RFC 9457 problem detail; the other panels of the case screen still load, because the gateway calls each owner in parallel and does not chain the calls (Architecture v5 slide 10; ASM-B-TECH-10-4).

- An event on a retry topic changes nothing on the screen until the consumer applies it. An event on a .dlt topic appears in the alert path and in the replay log, not as a case state (ASM-B-TECH-10-4).

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
| REST hop timeout | Reload the panel, or retry the GET once with jitter; the breaker closes when the downstream recovers; no case state is changed |
| Event on a retry topic | The consumer retries at 1 minute, 10 minutes and 1 hour; nothing is lost, because the event stays on the topic and its ce_id stays in the inbox |
| Event on a .dlt topic | The platform administrator replays it with the replay tool after the fix; the inbox drops any duplicate (ASM-B-TECH-10-5) |
| Call chain found in a trace | Cut the chain: the caller reads the owner's published contract, or the step moves into a workflow (ADR-020) |

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

- An activity that calls another service uses the 2 s REST timeout of section 3; the activity's own retry policy is what repeats the call, with the idempotency key above (Architecture v5 slide 11).

- A Kafka failure never fails a workflow: the event waits in the producer's outbox and the consumer retries on its retry topics. A workflow is not used to retry an event (Architecture v5 slide 22).

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
| REST hop timeout | RFC 9457 problem detail at the caller; no message ID is added by this standard (CG-B-TECH-10-3; ASM-B-TECH-10-4) |
| Event on a retry topic | No message; the consumer retries and the failure shows in the trace and the alert only |
| Event on a .dlt topic | Alert to the platform administrator; no case message until the replay |

- These are the only messages used for the Temporal and Drools failures in this standard. No message ID is added by this standard.

# 8. Calls between services in version 4

The realignment replaces the single deployable with 19 services (ADR-013). Every call between them follows one of four call types, and each call type has one failure rule: a REST hop has a 2 s timeout and is never chained, an event is retried and then dead-lettered, a Temporal activity retries on its own policy, and a file is retried by the workflow that started it (Architecture v5 slide 11; ADR-015, ADR-016, ADR-020).

| Call | Failure rule in version 4 | Owner |
|---|---|---|
| REST from gateway-bff to an owner | One hop; 2 s timeout; circuit breaker and bulkhead per downstream; a GET retried once with jitter; a POST carries its Idempotency-Key | gateway-bff calls; each service publishes and honours its own contract (Architecture v5 slides 10 and 11) |
| REST from a service to another service | Not used to answer a screen. A cached reference read from rwb-access or rwb-source-data is the only second call; anything longer is a workflow (ADR-020) | The calling service, against the owner's published contract |
| Event (Kafka) | Topic rwb.<short>.events.v1, key caseId, CloudEvents 1.0 binary mode; retry topics at 1 minute, 10 minutes and 1 hour; then .dlt with an alert and the replay tool; the inbox drops a duplicate | The service that owns the topic (section 8.3) |
| Temporal activity | Start-to-close per activity; initial interval 1 second, backoff coefficient 2, 10 attempts; NoPackageInForce is non-retryable | The service whose task queue rwb-<short> runs the workflow (Microservice Ownership Map v1, Workflows and activities sheet) |
| File | Retried by the workflow that started it, with a checksum on receipt; the manifest carries fileId, batchId, sha256 and record count | rwb-integration (P2) performs the transfer (Architecture v5 slide 11) |

## 8.1 One REST hop

- The browser calls gateway-bff only. gateway-bff checks the session and the coarse permission, then calls each owner it needs, in parallel, and merges the answers into the screen model (Architecture v5 slide 10).

- Two services are asked at the same time on the case screen, one hop each: rwb-case for the case, stage, tasks and timers, and rwb-source-data for the customer and the accounts (Architecture v5 slide 10).

- Other tabs load when the user clicks them, each from its own owner, one hop (Architecture v5 slide 10).

- Any call that would need a third service becomes a Temporal activity or a child workflow, not a REST chain (Architecture v5 slide 11; ADR-016, ADR-020).

- Trace analysis flags any trace with a call depth above one, and the contract test of each service fails a client that chains (Architecture v5 slide 11).

## 8.2 The 2 s timeout and the screen budget

- The 2 s is the ceiling of one REST call: the call ends at 2 s, the breaker opens for that downstream, and the caller answers with RFC 9457 problem details (Architecture v5 slides 10 and 11).

- The screen target is a separate figure: 2 s at p95 for the whole screen, planned at about 1.2 s — gateway and session 0.15 s, the slowest of the two parallel calls 0.6 s, composition and transfer 0.3 s (Architecture v5 slide 10).

- A hop that runs to its 2 s ceiling therefore consumes the whole screen budget. The read used in version 4 is that 2 s is the per-call ceiling and 1.2 s is the planning figure (CG-B-TECH-10-5; ASM-B-TECH-10-6).

## 8.3 Retry and .dlt by service

Each service owns its own topic and the retry and dead-letter topics of that topic. The topic, the retry ladder and the service that owns them are below; the owner of every row is the service recorded in the Microservice Ownership Map v1, Services and Events sheets (ASM-B-TECH-10-3).

| Code | Service | Topic | Retry | Dead letter | Owner |
|---|---|---|---|---|---|
| P1 | rwb-source-data | rwb.source-data.events.v1 | 1 min, 10 min, 1 h | .dlt of the topic, with alert | rwb-source-data (P1) |
| P2 | rwb-integration | rwb.integration.events.v1 | 1 min, 10 min, 1 h | .dlt of the topic, with alert | rwb-integration (P2) |
| P3 | rwb-case | rwb.case.events.v1 | 1 min, 10 min, 1 h | .dlt of the topic, with alert | rwb-case (P3) |
| P4 | rwb-access | rwb.access.events.v1 | 1 min, 10 min, 1 h | .dlt of the topic, with alert | rwb-access (P4) |
| P5 | rwb-document | rwb.document.events.v1 | 1 min, 10 min, 1 h | .dlt of the topic, with alert | rwb-document (P5) |
| P6 | rwb-comms | rwb.comms.events.v1 | 1 min, 10 min, 1 h | .dlt of the topic, with alert | rwb-comms (P6) |
| P7 | rwb-decision | rwb.decision.events.v1 | 1 min, 10 min, 1 h | .dlt of the topic, with alert | rwb-decision (P7) |
| P8 | rwb-payment | rwb.payment.events.v1 | 1 min, 10 min, 1 h | .dlt of the topic, with alert | rwb-payment (P8) |
| P9 | rwb-reporting | rwb.reporting.events.v1 | 1 min, 10 min, 1 h | .dlt of the topic, with alert | rwb-reporting (P9) |
| P10 | rwb-agent | rwb.agent.events.v1 | 1 min, 10 min, 1 h | .dlt of the topic, with alert | rwb-agent (P10) |
| S1 | rwb-valuation | rwb.valuation.events.v1 | 1 min, 10 min, 1 h | .dlt of the topic, with alert | rwb-valuation (S1) |
| S2 | rwb-treatment | rwb.treatment.events.v1 | 1 min, 10 min, 1 h | .dlt of the topic, with alert | rwb-treatment (S2) |
| S3 | rwb-guarantee | rwb.guarantee.events.v1 | 1 min, 10 min, 1 h | .dlt of the topic, with alert | rwb-guarantee (S3) |
| S4 | rwb-litigation | rwb.litigation.events.v1 | 1 min, 10 min, 1 h | .dlt of the topic, with alert | rwb-litigation (S4) |
| S5 | rwb-asset | rwb.asset.events.v1 | 1 min, 10 min, 1 h | .dlt of the topic, with alert | rwb-asset (S5) |
| S6 | rwb-debtsale | rwb.debtsale.events.v1 | 1 min, 10 min, 1 h | .dlt of the topic, with alert | rwb-debtsale (S6) |
| S7 | rwb-writeoff | rwb.writeoff.events.v1 | 1 min, 10 min, 1 h | .dlt of the topic, with alert | rwb-writeoff (S7) |
| S8 | rwb-deviation | rwb.deviation.events.v1 | 1 min, 10 min, 1 h | .dlt of the topic, with alert | rwb-deviation (S8) |
| S9 | rwb-partner | rwb.partner.events.v1 | 1 min, 10 min, 1 h | .dlt of the topic, with alert | rwb-partner (S9) |

The shared topic rwb.decision-record.v1 is owned by rwb-decision (P7); its retry topics and its .dlt topic follow the same rule, and each service writes only its own local decision record and publishes it (Architecture v5 slide 20; DP-03, DP-09). The exact names of the retry topics and of the .dlt topics are Not specified in the source documents (CG-B-TECH-10-1; ASM-B-TECH-10-3). Who is alerted and who replays is the platform administrator role (CG-B-TECH-10-4; ASM-B-TECH-10-5).

# 9. Realignment changes in version 4 (D-RCV-60)

| # | Section | Version 3 | Version 4 | Decision |
|---|---|---|---|---|
| 1 | 1 Rules | No REST rule; no per-service retry or dead-letter rule | A REST call is one hop with a 2 s timeout; an event is retried and then dead-lettered; the outbox and inbox rule is read for all 19 services | D-RCV-60; ADR-020, ADR-015; DP-09 |
| 2 | 2 Failure categories | 13 categories, none for a REST timeout, a call chain or a dead-letter event | 18 categories; 5 added: REST timeout, call chain, event retry, duplicate event, dead letter | D-RCV-60 |
| 3 | 3 Retry | Temporal, outbound, load, agent and idempotency policy | 5 rows added: REST calls, REST call depth, event consumers, Kafka broker unavailable, REST calls inside an activity | D-RCV-60; ADR-015, ADR-020 |
| 4 | 4 What the user sees | Outage, stale product, exception queue, rule package, workflow | 2 bullets added: a timed-out panel and its usable neighbours; an event on a retry or .dlt topic | D-RCV-60 |
| 5 | 5 Recovery | 9 recovery paths | 4 rows added: REST hop timeout, event on a retry topic, event on a .dlt topic, call chain in a trace | D-RCV-60 |
| 6 | 6 Temporal and Drools | Activity retry, idempotency, workflow tasks, workflow unavailable, decision log, outbox, Drools | 2 bullets added: the 2 s timeout inside an activity; a Kafka failure never fails a workflow | D-RCV-60 |
| 7 | 7 Message map | 8 messages; no message ID added | 3 rows added; the closing rule is unchanged and still adds no message ID | D-RCV-60 |
| 8 | 8 Calls between services | Not in version 3 | New: the four call types with their failure rule, one REST hop, the 2 s ceiling against the 1.2 s screen budget, and the retry and .dlt owner of all 19 topics | D-RCV-60; ADR-013, ADR-015, ADR-016, ADR-020 |

Everything else in version 3 is kept character for character: the seven opening rules, the thirteen failure categories, the eight retry rows, the six user-facing statements, the nine recovery paths, the nine Temporal and Drools bullets, the eight message rows, and the closing sentence of section 7. No message code, requirement ID, decision reference or date of version 3 is changed, and no release date is added.
