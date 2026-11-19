# Increment Card — INC-023-epic-1-RWB-TE-006

**RWB-TE-006 — Outbox and retry for outbound work**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-023` |
| Title | Outbox and retry for outbound work |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-TE-006` |
| RUN_ID | `INC-023-epic-1-RWB-TE-006` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P2 Integration |
| Story type | Enabler |
| Priority | Must |
| Build order | 23 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-044, RWB-E1-027, RWB-E1-007 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P2 Integration.

## Scope

**Story:** As a **squad member (RW-TRIBE)**, I want **every application event and every outbound work request written to an outbox in the same transaction as the change, and delivered to each consumer in order with retry**, so that **no outbound action is lost when a system or a consumer is down, and nothing is sent for a change that did not commit**.

**Business outcome:** The Workbench modules talk to each other through application events, and outbound work such as a notice for WIN starts from an event in the module that approved it. If the event is sent before the change commits, or is lost when a consumer fails, a notice is never dispatched or a ledger entry is missing, and nobody sees it. The outbox stores each event with the change, a sender delivers it to every consumer at least once in case order, retries on a schedule held as data, and moves a delivery that keeps failing to the exception queue with a task. It meets REQ-DRI-007 (retry on a defined schedule; exception queue with a task for a named owner) and NFR-025 and NFR-026. The measure is the count of outbox deliveries in the exception queue over one day, with a target of zero (FSD P2 A2.1.1).

**Main flow:**
1. Business service (for example notice approval): calls OutboxWriter.publish inside its own transaction with the event type (an event from EV-01 to EV-28, or an outbound work request type such as WIN_DISPATCH), schema version, case ID, payload references, actor and idempotency key.
2. OutboxWriter: writes one outbox_event row with the next case sequence, and one outbox_delivery row per consumer listed for the event type.
3. Database: commits the change, the event and its deliveries together, or none of them.
4. JOB-11 Outbox sender (event step): every minute selects due deliveries with a row lock that skips rows another instance holds, oldest case sequence first, taking only the lowest open sequence per case and consumer.
5. OutboxSender: calls the consumer with the event header (event ID, idempotency key, schema version, occurred time, actor) and payload; each consumer checks the key through IdempotencyGuard (RWB-E1-007) before it acts.
6. OutboxSender: on success marks the delivery DELIVERED; when the delivery had failed before and the consumer holds a case step, raises RETRY_SUCCEEDED for the case (R-UNI-35).

**Acceptance criteria:**
- AC1: Sent after commit
- AC2: Retry limit
- AC3: Nothing is sent for a change that did not commit
- AC4: A retry that succeeds
- AC5: The same event is written once
- AC6: Two sender instances
- AC7: Order per case and consumer
- AC8: Consumers are independent
- AC9: Sending an exception delivery again
- AC10: An event with no case
- AC11: Retry settings come from configuration

**Out of scope:**
- Outbound files, their SFTP transfer, retry and resend, and the duplicate check by key: RWB-E1-007.
- The consumers themselves, for example the ledger listener: RWB-E1-067 and RWB-E2-034.
- The interface and job monitor screen: SCR-44 in Epic 2 and Epic 8.
- Retry values: DL11.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-006-outbox-and-retry-for-outbound-work-v1.md` |
| Requirement IDs | REQ-DRI-007 |
| BRD section | Business Requirements Program, section 5.2 and section 6.4 |
| Decision | None |
| Epic card | `epics/EPIC-001-foundation-1.md` |
| Lifecycle tailoring | `epics/EPIC-001-tailoring.md` |
| Module FSD / PRD | `docs/prds/` |
| Module TSD | `requirement/legacy/05-technical-architecture/` |
| API specification | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v4.yaml` |
| Physical schema | `requirement/legacy/06-data/recovery-workbench-physical-schema-v6.sql` |
| Engineering practices | `AGENTS.md` |

## Lifecycle tailoring

Shared record: `epics/EPIC-001-tailoring.md`. The phase classification is epic-level; this card records the story-specific agents and evidence.

## Story authority

| Who | What they may do in this story |
|---|---|
| SY-CASEWF, case workflow module | Runs the sender step, applies R-UNI-33, R-UNI-35 and R-UNI-36 and raises the task |
| SY-DECLOG, decision log writer | Writes the entry for the move to the exception queue |
| RW-PLATADM, platform administrator | Reads deliveries and sends an exception delivery again (Platform administration CRUD) |
| RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY | Read deliveries (Platform administration R) |
| RW-SECADM, security administrator | Reads deliveries (Platform administration CRUDA) |
| No approval level from the delegation of authority applies | The story takes no business decision |

## Contract extract

**Published interfaces** ```java // recovery.integration.api; joins the caller's transaction UUID OutboxWriter.publish(OutboxEvent event); // OutboxEvent: eventType (EV-01 to EV-28 names, or a work request type such as WIN_DISPATCH), schemaVersion, caseId (nullable), payload (references only), actorRef, idempotencyKey // throws DuplicateOutboxKeyException when the key exists // Implemented by each consumer and listed under its consumer name ConsumeResult OutboxConsumer.consume(EventHeader header, JsonNode payload); // OK or FAILED(code) // P3 interfaces used on failure and recovery void CaseEvents.raise(UUID caseId, String eventCode, String reference); // SYSTEM_UNAVAILABLE, RETRY_SUCCEEDED, RETRY_LIMIT_REACHED UUID TaskApi.raiseTask(UUID caseId, String taskCode, String ownerRole); // RWB-E1-007, called by each consumer before it acts boolean IdempotencyGuard.firstTime(String consumer,…

## Owners and approvals

| Gate | Accountable role | Name | Decision / date |
|---|---|---|---|
| Requirements approval | Product Owner | Chitchaya Muanchonchana | Source story set v7/v6, 16 Nov 2026 |
| Context readiness | Forward Deployed Engineer | Jesniphat Pukkham | CONTEXT-20261116 |
| Plan approval | Forward Deployed Architect | Jesniphat Pukkham | Per-story plan gate |
| Pull request approval | Forward Deployed Engineer | Recovery tech lead | Per MR |

## Agents selected

| Lifecycle group | Agent | Applicable / Optional / Not used | Reason |
|---|---|---|---|
| Requirements and discovery | Context Builder / Updater | Applicable | Context package CONTEXT-20261116. |
| Design, backlog and spec | Technical Specifier | Applicable | Produces the implementation-ready spec. |
| Plan and build | Implementation Planner | Applicable | Produces `plan.md` and `tasks.md`. |
| Plan and build | Implementation Builder | Applicable | Builds the approved plan in ACE. |
| Quality and release | Compliance Reviewer | Applicable | Spec, plan and code gates. |
| Quality and release | API Tester | Per API scope | Driven by the spec. |
| Quality and release | Functional Automation Test | Per UI scope | Driven by the spec. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Stop signals:** any guardrail in story §17; a migration that is not `V<seq>__<story>_<name>.sql`; a direct read of an ACE table outside `recovery.v_ace_*`.

**Guardrails:**

- No business value in code: consumers, owners, retry counts, delays and batch size are configuration. - No personal data in logs, tests or prompts; payloads hold references and codes only, and the admin endpoint does not return the payload. - No read of another module's tables: case events and tasks go through the P3 interfaces; the decision log through P7. - No event or delivery is deleted; a delivery leaves the exception queue only by being sent again.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-006-outbox-and-retry-for-outbound-work-v1.md` |
| Specification | `output/INC-023-epic-1-RWB-TE-006/specify/spec.md` |
| Compliance validation | `output/INC-023-epic-1-RWB-TE-006/specify/compliance-validation.md` |
| Agent run log | `output/INC-023-epic-1-RWB-TE-006/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-023-epic-1-RWB-TE-006/plan/` |
| Implementation evidence | `output/INC-023-epic-1-RWB-TE-006/implement/` |
| API / functional test reports | `output/INC-023-epic-1-RWB-TE-006/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-023-epic-1-RWB-TE-006/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 11 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-006-outbox-and-retry-for-outbound-work-v1.md` |
| Output run | `output/INC-023-epic-1-RWB-TE-006/` |

