# Technical Specification — RWB-TE-006 Outbox and retry for outbound work

| Field | Value |
|---|---|
| Story | RWB-TE-006 — Outbox and retry for outbound work |
| Epic / module | E1 / P2 Integration (technical enabler) |
| RUN_ID | `INC-028-epic-1-RWB-TE-006` |
| Source requirement | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 006 Outbox and retry for outbound work v1.md`; REQ-DRI-007; BRD Program §5.2, §6.4 |
| Upstream IDs | REQ-DRI-007; NFR-025; NFR-026; R-UNI-33, 35, 36, 39, 40; RWB-E1-007; RWB-E1-027; RWB-E1-044; RWB-E1-042; DL11 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Platform administrator; TechX tech lead; see `compliance-validation.md` |
## Change Scope Declaration
| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen of its own. The `RESOLVE_OUTBOX_DELIVERY` task appears on SCR-09, which exists from RWB-E1-007; the platform administrator uses the two admin endpoints. |
| Logic In Scope | `YES` — transactional outbox write, per-consumer delivery, ordering, retry, exception move, case events, decision-log guard and resend. |
| API In Scope | `YES` — two new E1 endpoints: `GET /admin/outbox/deliveries` and `POST /admin/outbox/deliveries/{deliveryId}/resend`. |
| API Impact Type | `NEW_API_REQUIRED` |
| Impacted Existing Nodes | `outbox_event` (new); `outbox_delivery` (new); `processed_event` (RWB-E1-007); JOB-11 event step; P3 case events and tasks; P7 decision log; SCR-09 task list. |
| New Nodes Required | `YES` — `OutboxWriter`; `OutboxEventEntity`; `OutboxDeliveryEntity`; `OutboxRepository`; `OutboxSender`; `ConsumerCatalog`; `OutboxSenderEventStep`; `OutboxAdminController`. |
| Inherited Existing Behavior | Idempotency guard (RWB-E1-007); outbound file sender (RWB-E1-007); decision log writer (RWB-E1-027); migrations (RWB-E1-044); configuration service (RWB-E1-042); case events and tasks (P3). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |
## Requirement-to-SPEC Logic Coverage
| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | An event and its deliveries are written in the same transaction as the change. | SPEC-RWB-TE-006-002 | DIRECT | `OutboxWriter.publish` joins the caller's transaction. | COVERED |
| BR2 | Each event carries an event ID and an idempotency key unique in the outbox; consumers drop a repeat. | SPEC-RWB-TE-006-004, SPEC-RWB-TE-006-007 | DIRECT | Unique key; `IdempotencyGuard` in each consumer. | COVERED |
| BR3 | Delivery is at least once; each consumer has its own delivery state. | SPEC-RWB-TE-006-003, SPEC-RWB-TE-006-007 | DIRECT | One `outbox_delivery` per event and consumer. | COVERED |
| BR4 | Events for one case reach each consumer in the order they were written. | SPEC-RWB-TE-006-005, SPEC-RWB-TE-006-006 | DIRECT | `case_seq`; lowest open sequence per case and consumer. | COVERED |
| BR5 | A failed delivery is retried on the schedule; after the last retry it moves to the exception queue with a task. | SPEC-RWB-TE-006-008, SPEC-RWB-TE-006-009 | DIRECT | Retry settings from configuration; task `RESOLVE_OUTBOX_DELIVERY`. | COVERED |
| BR6 | For a consumer that holds a case step, the first failure raises `SYSTEM_UNAVAILABLE`, a later success `RETRY_SUCCEEDED`, and the limit `RETRY_LIMIT_REACHED`. | SPEC-RWB-TE-006-010 | DIRECT | Case events through P3. | COVERED |
| BR7 | Payloads hold references and codes, never personal data; the event carries its schema version. | SPEC-RWB-TE-006-016 | DIRECT | Payload JSON with IDs and codes; `schema_version` required. | COVERED |
| BR8 | The move to the exception queue for a case does not happen unless its decision log entry is written. | SPEC-RWB-TE-006-011 | DIRECT | Decision log write in the same transaction; rollback to RETRYING. | COVERED |
| BR9 | Consumers, owners, retry counts and delays are read from configuration. | SPEC-RWB-TE-006-008, SPEC-RWB-TE-006-009 | DIRECT | `ConsumerCatalog`; no literal in the sender. | COVERED |
| AC1 | A notice approved at 10:00 writes one `WIN_DISPATCH` request and one delivery; the header holds event ID, key, schema version 1, time and actor; payload holds references only; the 10:01 run delivers and the consumer enqueues the WIN file; DELIVERED. | SPEC-RWB-TE-006-002, SPEC-RWB-TE-006-003, SPEC-RWB-TE-006-007, SPEC-RWB-TE-006-016 | DIRECT | One transaction; payload references only. | COVERED |
| AC2 | A target down through 10:01, 10:02, 10:07 and 10:22: no fifth attempt; delivery EXCEPTION with attempt count 4; task; `RETRY_LIMIT_REACHED` with one decision log entry. | SPEC-RWB-TE-006-008..011 | DIRECT | Initial attempt + 3 retries. | COVERED |
| AC3 | A rollback after publish leaves no event and no delivery. | SPEC-RWB-TE-006-002 | DIRECT | Same transaction; rollback removes both. | COVERED |
| AC4 | A failure at 10:01 moves the case to RETRY_QUEUE; the 10:02 attempt succeeds; delivery DELIVERED with attempt count 2; `RETRY_SUCCEEDED` resumes the case. | SPEC-RWB-TE-006-007, SPEC-RWB-TE-006-010 | DIRECT | Case event on success after a failure. | COVERED |
| AC5 | Two approvals with the same key: one event; the second gets `DuplicateOutboxKeyException` and changes nothing. | SPEC-RWB-TE-006-004 | DIRECT | Unique `idempotency_key`. | COVERED |
| AC6 | 200 due deliveries and two instances: each delivery made once; 200 calls. | SPEC-RWB-TE-006-006 | DIRECT | `FOR UPDATE SKIP LOCKED`. | COVERED |
| AC7 | Sequence 11 fails for `ledger`; sequence 12 waits until 11 is DELIVERED. | SPEC-RWB-TE-006-005, SPEC-RWB-TE-006-006 | DIRECT | Lowest open sequence per case and consumer. | COVERED |
| AC8 | `ledger` fails and `reporting-feed` succeeds on one event: independent states; the case route does not change because `ledger` does not hold the case step. | SPEC-RWB-TE-006-003, SPEC-RWB-TE-006-010 | DIRECT | Per-consumer state; case-step flag in configuration. | COVERED |
| AC9 | Resend an EXCEPTION delivery: 200, MSG-GEN-005, PENDING, attempt 0; resend a DELIVERED delivery: 409 MSG-P2-022. | SPEC-RWB-TE-006-013 | DIRECT | Status check before reset. | COVERED |
| AC10 | An event with no case whose only consumer fails four times: EXCEPTION; alert within 15 minutes; no task and no case event. | SPEC-RWB-TE-006-012 | DIRECT | Null case branch. | COVERED |
| AC11 | Retry delays changed to 2, 10 and 30 at 09:00; a failure at 10:01 is due at 10:03. | SPEC-RWB-TE-006-008 | DIRECT | Settings read per attempt. | COVERED |
| X1–X3 | Rollback after publish; a consumer fails once then succeeds; the same key is published twice. | SPEC-RWB-TE-006-002, 004, 007, 010 | DIRECT | No event/delivery; DELIVERED with case resume; one event and a duplicate exception. | COVERED |
| X4–X6 | Two sender instances; an earlier event failing for the same case/consumer; one consumer fails and another succeeds. | SPEC-RWB-TE-006-003, 006 | DIRECT | Each delivery once; later events wait; independent delivery states. | COVERED |
| X7–X9 | Resend a non-EXCEPTION delivery; an event with no case fails past its limit; retry settings change. | SPEC-RWB-TE-006-008, 012, 013 | DIRECT | 409 MSG-P2-022; EXCEPTION with alert; next attempt uses new delays. | COVERED |
| X10–X11 | Decision log write fails at the limit; a role without Platform administration U resends. | SPEC-RWB-TE-006-011, 015 | DIRECT | RETRYING with MSG-P7-003 and incident; 403 MSG-P4-002. | COVERED |
## User story intent interpretation
As a **squad member (RW-TRIBE)**, I want **every application event and every outbound work request written to an outbox in the same transaction as the change, and delivered to each consumer in order with retry**, so that **no outbound action is lost when a system or a consumer is down, and nothing is sent for a change that did not commit**.

The story builds the transactional outbox: the writer joins the caller's transaction, writes one event and one delivery per configured consumer, and the sender delivers each delivery at least once in case order. A failed delivery is retried on a data-held schedule; after the last retry it moves to EXCEPTION with a task for the consumer's owner role, and for a consumer that holds a case step the case moves to RETRY_QUEUE, resumes, or moves to EXCEPTION_QUEUE through P3. A decision-log failure blocks the exception move. The platform administrator lists deliveries and resends an exception one.
## Entry trigger and preconditions
| Item | Value |
|---|---|
| Trigger | `OutboxWriter.publish` inside a business transaction; JOB-11 event step every minute; administrator resend. |
| Preconditions | RWB-E1-044, RWB-E1-027 and RWB-E1-007 done; consumer list in `rwb.integration.outbox.consumers`; retry settings in `rwb.integration.outbox.retry`; Quartz clustered; JOB-11 runs every minute; flag `rwb.integration.outbox` on. |
| Input | `OutboxEvent` from a business service; consumer configuration; retry settings; due `outbox_delivery` rows. |
| Output | `outbox_event` and `outbox_delivery` rows; delivered/retrying/exception states; case events; tasks; alerts; admin list/resend. |
| Feature flag | `rwb.integration.outbox`. Off: the event step does not run and deliveries stay PENDING; the writer still records events so nothing is lost when it is switched on. |
## Field-level behaviour matrix
| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `outbox_event` | `event_type`, `schema_version`, `case_id`, `case_seq`, `idempotency_key`, `payload`, `actor_ref`, `occurred_at` | Caller | Append only | Unique `idempotency_key`; unique `(case_id, case_seq)` |
| `outbox_delivery` | `event_id`, `consumer`, `status`, `attempt_count`, `next_attempt_at`, `last_error_code`, `delivered_at`, `task_id` | Writer + sender | System writes | Unique `(event_id, consumer)`; status PENDING/RETRYING/DELIVERED/EXCEPTION |
| `recovery_case` | `route_state` | Current | P3 writes on the event | RETRY_QUEUE, RESUME_STATE, EXCEPTION_QUEUE |
| `task` | `task_code`, `owner_role`, `status` | P3 | P3 writes | `RESOLVE_OUTBOX_DELIVERY`; owner role from configuration |
| `decision_log_entry` | decision, rule, version | P7 | Append only | Written before the exception move commits |
## Status-transition matrix
| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| — | Publish | Business transaction commits | Delivery PENDING | One row per consumer; next attempt now |
| PENDING | Consumer succeeds | — | DELIVERED | `delivered_at`; case `RETRY_SUCCEEDED` if it had failed |
| PENDING | Consumer fails | Retries left | RETRYING | Attempt +1; next attempt from settings; case `SYSTEM_UNAVAILABLE` on the first failure if it holds the step |
| RETRYING | Consumer succeeds | — | DELIVERED | Case resumes |
| RETRYING | Consumer fails | No retries left | EXCEPTION | Task; case `RETRY_LIMIT_REACHED`; decision log |
| EXCEPTION | Resend | Version/status valid | PENDING | Attempt 0; audit |
| Delivery PENDING/RETRYING | Feature flag off | — | Unchanged | No send |
| No case status change | — | — | — | The case status is not changed; route state is P3 |
## Exceptional-case behaviour
| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Business transaction rolls back | No event, no delivery | None |
| X2 | Consumer fails once, then succeeds | DELIVERED; case resumes | None |
| X3 | Same key published twice | One event; duplicate exception | None |
| X4 | Two sender instances | Each delivery once | None |
| X5 | Earlier event failing for the same case/consumer | Later events wait | None |
| X6 | One consumer fails, another succeeds | Independent states | None |
| X7 | Resend a non-EXCEPTION delivery | Refused | 409 MSG-P2-022 |
| X8 | Event with no case fails past its limit | EXCEPTION; alert; no task/case event | MSG-P2-001 |
| X9 | Retry settings change | Next attempt uses new delays | None |
| X10 | Decision log write fails at the limit | Nothing changes; delivery RETRYING; next run retries the delivery and the move | MSG-P7-003 |
| X11 | Role without Platform administration U resends | 403; nothing changes | MSG-P4-002 |
## API change assessment
| Item | Value |
|---|---|
| API Impact Type | `NEW_API_REQUIRED` |
| New endpoints | `GET /api/recovery/v1/admin/outbox/deliveries` (Platform administration R); `POST /api/recovery/v1/admin/outbox/deliveries/{deliveryId}/resend` (U). |
| Contract delta | List query `status`, `consumer`, `eventType`, `from`, `to`, `page`, `size`; `OutboxDeliveryPage` with items and paging; resend returns `OutboxDelivery` PENDING, attempt 0. The payload is never returned. |
| Backward compatibility | New endpoints; no existing operation changes. |
| Authorization | Platform administration R/U; resend written to the ACE audit log with user and time; 403 MSG-P4-002. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 409 MSG-P2-022 (not EXCEPTION); 503. |
| Versioning | No version change; both operations are first in E1. |
## Unit Test Applicability
| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label change. The task appears on the existing SCR-09 list; the admin endpoints are used directly. | Existing front-end tests stay green; no new front-end test is required. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | BR1–BR9; SPEC-RWB-TE-006-001..020 | New writer, entities, repository, sender, consumer catalog, event step and controller. | Unit tests cover commit/rollback, duplicate key, per-consumer state, ordering, skip-locked, retry boundary 3/4, exception move, decision-log failure, null case, resend and access. |
## Detailed design
### Components
| Component | Type | Responsibility |
|---|---|---|
| `OutboxWriter` | Published interface | Writes the event and one delivery per listed consumer in the caller's transaction. |
| `OutboxEventEntity`, `OutboxDeliveryEntity` | Entity | The two rows. |
| `OutboxRepository` | Repository | Skip-locked selection of due deliveries in case order per consumer. |
| `OutboxSender` | Service | Delivery, retry scheduling, case events and exception move. |
| `ConsumerCatalog` | Service | Reads the consumer list and retry settings. |
| `OutboxSenderEventStep` | Job | The event step of JOB-11. |
| `OutboxAdminController` | Controller | The list and resend endpoints. |

### Data and migration
Flyway `V<next>__create_outbox_event.sql` creates `outbox_event` (id, event_type, schema_version, case_id, case_seq, idempotency_key unique, payload jsonb, actor_ref, occurred_at, standard columns) and `outbox_delivery` (id, event_id FK, consumer, status, attempt_count, next_attempt_at, last_error_code, delivered_at, task_id, standard columns) with `UNIQUE (event_id, consumer)`, a status check and `ix_outbox_delivery_due` on `(next_attempt_at) WHERE status IN ('PENDING','RETRYING')`. `case_seq` is the case's highest sequence + 1 under a lock on the case's latest outbox row.

### Rules
1. `publish` writes the event and its deliveries in the caller's transaction; a rollback leaves neither.
2. A duplicate `idempotency_key` throws `DuplicateOutboxKeyException`; nothing changes.
3. The sender selects due deliveries with `FOR UPDATE SKIP LOCKED`, oldest `case_seq` first, taking only the lowest open sequence per case and consumer.
4. On success, mark DELIVERED; if the delivery had failed and the consumer holds the case step, raise `RETRY_SUCCEEDED`.
5. On failure, increment the attempt count and set the next attempt from the retry settings; on the first failure of a case-step consumer, raise `SYSTEM_UNAVAILABLE`.
6. When the retries are used, set EXCEPTION, raise `RESOLVE_OUTBOX_DELIVERY` for the consumer's owner role, and for a case-step consumer raise `RETRY_LIMIT_REACHED`; write the decision log entry in the same transaction. A failed log write rolls back to RETRYING; the next run retries the delivery and the move.
7. An event with no case that reaches the limit becomes EXCEPTION with an alert and no task or case event.
8. The admin list excludes the payload; resend only accepts EXCEPTION and resets to PENDING with attempt 0.

### Transaction and events
The writer joins the caller's transaction. The exception move, task, case event and decision log entry are one transaction. Delivery is at least once; each consumer drops a repeat through `IdempotencyGuard`. The sender publishes no event of its own; it delivers EV-01..EV-28.

### Security and authority
| Actor | Right | Scope |
|---|---|---|
| SY-CASEWF | Run the sender; apply R-UNI-33/35/36; raise the task | All |
| SY-DECLOG | Write the exception-move entry | All |
| RW-PLATADM | Platform administration CRUD; list and resend | All |
| RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY | Platform administration R | All |
| RW-SECADM | Platform administration CRUDA | All |

### Observability and operations
- Metrics: deliveries pending/retrying/delivered/exception; attempt counts; sender duration; decision-log failures.
- Alerts: delivery in EXCEPTION, event with no case, sender late, decision-log failure.
- Task `RESOLVE_OUTBOX_DELIVERY` on SCR-09 with MSG-P2-001.
- Run book: JOB-11 event step follows the RWB-E1-056 format.

### Performance
- Batch size 200 per run (assumed; DL11); index on due deliveries; `SKIP LOCKED` keeps instances apart.
- The sender runs every minute; a delivery is attempted at most once per run.
- No numeric throughput target is stated; record SIT duration.

### Feature flag and rollback
`rwb.integration.outbox`. Off: the event step does not run and deliveries stay PENDING; the writer still records events. Rollback: turn the flag off; the migration is additive.

### No UI change
No screen of its own. The task appears on SCR-09 (RWB-E1-007); SCR-44 shows deliveries from Epic 2.
## Test scenarios
| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-TE-006-01 | AC1, BR1, BR3, BR7 | System | Notice approved at 10:00; stub succeeds | One event, one delivery, header fields, references-only payload, DELIVERED |
| TC-TE-006-02 | AC2, BR5, BR6, BR8 | System | Stub fails four times | No fifth attempt; EXCEPTION; task; RETRY_LIMIT_REACHED; one log entry |
| TC-TE-006-03 | AC3, BR1 | System | Approval rolled back after publish | No event, no delivery |
| TC-TE-006-04 | AC4, BR6 | System | Stub fails once, then succeeds | DELIVERED, attempt 2; RETRY_SUCCEEDED |
| TC-TE-006-05 | AC5, BR2 | System | Two approvals, same key | One event; second duplicate exception |
| TC-TE-006-06 | AC6 | System | 200 due deliveries, two instances | Each delivered once; 200 calls |
| TC-TE-006-07 | AC7, BR4 | System | Sequences 11 and 12; ledger fails on 11 | 12 waits for 11 |
| TC-TE-006-08 | AC8, BR3 | System | ledger fails, reporting-feed succeeds | Independent states; no case route change |
| TC-TE-006-09 | AC9 | System | OBD-SYN-0001 EXCEPTION; OBD-SYN-0002 DELIVERED | 200 MSG-GEN-005; 409 MSG-P2-022 |
| TC-TE-006-10 | AC10 | System | No-case event, consumer fails four times | EXCEPTION; alert; no task/case event |
| TC-TE-006-11 | AC11, BR9 | System | Delays changed to 2/10/30 before the run | Next attempt at 10:03 |
| TC-TE-006-12 | X11 | Security | RW-DATASTEW resends | 403; MSG-P4-002 |
| TC-TE-006-13 | X10 | Resilience | Decision log forced to fail at the move | RETRYING; MSG-P7-003; incident |
| TC-TE-006-14 | BR1–BR9 | Unit | Commit/rollback; duplicate key; order; lock; retry 3/4 | Pass/fail as specified |
## Guardrails
- No business value in code: consumers, owners, retry counts, delays and batch size are configuration.
- No personal data in logs, tests or prompts; payloads hold references and codes only, and the admin endpoint does not return the payload.
- No read of another module's tables: case events and tasks go through P3; the decision log through P7.
## Out of scope
- Outbound files, SFTP transfer, retry and resend, and the duplicate check by key: RWB-E1-007.
- The consumers themselves, for example the ledger listener: RWB-E1-067 and RWB-E2-034.
- The interface and job monitor screen: SCR-44 in Epic 2 and Epic 8; retry values: DL11.
## Traceability
| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-007 | Retry on a defined schedule; exception queue with a task for a named owner | Program §5.2, §6.4 | None | All recovery processes | R-UNI-33, 35, 36, 39, 40 | TC-TE-006-01..14 |
## Clarification Log
| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | §3; SPEC-008 | The retry settings (3 retries at 1, 5 and 15 minutes) are assumed. | Determines attempt times. | Use the assumed values under DL11; they are configuration. | RESOLVED | SPEC-008 |
| CLAR-002 | §3; SPEC-003 | The consumer list and the case-step flag are assumed. | Determines deliveries and case events. | `win-dispatch` holds the case step; `ledger` and `reporting-feed` do not; load them in configuration. | RESOLVED | SPEC-003 |
| CLAR-003 | §13; SPEC-006 | The batch size 200 is assumed. | Affects the run duration. | 200 per run (DL11); configuration. | RESOLVED | SPEC-006 |
| CLAR-004 | AC4; SPEC-007 | AC4 says "delivers the delivery status with attempt count 2". | Ambiguous wording. | The delivery is DELIVERED with attempt count 2. | RESOLVED | SPEC-007 |
| CLAR-005 | X10; SPEC-011 | What exactly is retried when the decision log fails at the limit? | The consumer may still be down. | The delivery stays RETRYING and is tried at the next run; if it fails again, the exception move is attempted again. Nothing moves until the decision log entry is written. | RESOLVED | SPEC-011 |
| CLAR-006 | AC10; SPEC-012 | An event with no case has no task and no case event. | Determines the null-case branch. | EXCEPTION plus an alert to the platform administrator; no task and no case event. | RESOLVED | SPEC-012 |
| CLAR-007 | §14; SPEC-009 | `MSG-P2-001` uses `{interface}` and `{item}` for a consumer and an event. | Message wording. | `{interface}` is the consumer name; `{item}` is the event type and case number. | RESOLVED | SPEC-009 |
| CLAR-008 | BR7; SPEC-016 | The schema version is 1 for all E1 events. | Payload compatibility. | `schema_version = 1` for E1; a later change increments it. | RESOLVED | SPEC-016 |

`CLARIFICATION_STATUS: RESOLVED` — all eight items are answered from the story, the configuration or DL11.
## Status reporting
```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend outbox story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New transactional outbox, per-consumer delivery, retry, exception move and two admin endpoints; existing SCR-09 task list reused.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: new outbox capability and two endpoints]
REQUIREMENT_COVERAGE_SUMMARY: All 9 business rules, 11 acceptance criteria, 11 exception paths and 8 state transitions are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 9] [COVERED_RULES: 9] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
