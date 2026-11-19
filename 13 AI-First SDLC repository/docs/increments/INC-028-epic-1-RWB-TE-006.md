# Increment Card — INC-028-epic-1-RWB-TE-006

**RWB-TE-006 — Outbox and retry for outbound work**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-028` |
| Title | Outbox and retry for outbound work |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-TE-006` |
| RUN_ID | `INC-028-epic-1-RWB-TE-006` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P2 Integration |
| Story type | Enabler |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-044, RWB-E1-027, RWB-E1-007 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P2 Integration. **Build group:** P2.

## Scope

**Story:** As a **squad member (RW-TRIBE)**, I want **every application event and every outbound work request written to an outbox in the same transaction as the change, and delivered to each consumer in order with retry**, so that **no outbound action is lost when a system or a consumer is down, and nothing is sent for a change that did not commit**.

**Main flow:**
1. Business service (for example notice approval): calls OutboxWriter.publish inside its own transaction with the event type (an event from EV-01 to EV-28, or an outbound work request type such as WIN_DISPATCH), schema version, case ID, payload references, actor and idempotency key.
2. OutboxWriter: writes one outbox_event row with the next case sequence, and one outbox_delivery row per consumer listed for the event type.
3. Database: commits the change, the event and its deliveries together, or none of them.
4. JOB-11 Outbox sender (event step): every minute selects due deliveries with a row lock that skips rows another instance holds, oldest case sequence first, taking only the lowest open sequence per case and consumer.
5. OutboxSender: calls the consumer with the event header (event ID, idempotency key, schema version, occurred time, actor) and payload; each consumer checks the key through IdempotencyGuard (RWB-E1-007) before it acts.
6. OutboxSender: on success marks the delivery DELIVERED; when the delivery had failed before and the consumer holds a case step, raises RETRY_SUCCEEDED for the case (R-UNI-35).

**Out of scope:**
- Outbound files, their SFTP transfer, retry and resend, and the duplicate check by key: RWB-E1-007.
- The consumers themselves, for example the ledger listener: RWB-E1-067 and RWB-E2-034.
- The interface and job monitor screen: SCR-44 in Epic 2 and Epic 8.
- Retry values: DL11.

**Business outcome and value hypothesis:** The Workbench modules talk to each other through application events, and outbound work such as a notice for WIN starts from an event in the module that approved it. If the event is sent before the change commits, or is lost when a consumer fails, a notice is never dispatched or a ledger entry is missing, and nobody sees it. The outbox stores each event with the change, a sender delivers it to every consumer at least once in case order, retries on a schedule held as data, and moves a delivery that keeps failing to the exception queue with a task. It meets REQ-DRI-007 (retry on a defined schedule; exception queue with a task for a named owner) and NFR-025 and NFR-026. The measure is the count of outbox deliveries in the exception queue over one day, with a target of zero (FSD P2 A2.1.1).

**Constraints and guardrails:**
- No business value in code: consumers, owners, retry counts, delays and batch size are configuration.
- No personal data in logs, tests or prompts; payloads hold references and codes only, and the admin endpoint does not return the payload.
- No read of another module's tables: case events and tasks go through the P3 interfaces; the decision log through P7.
- No event or delivery is deleted; a delivery leaves the exception queue only by being sent again.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 006 Outbox and retry for outbound work v1.md` |
| Requirement IDs | REQ-DRI-007 |
| BRD section | Business Requirements Program, section 5.2 and section 6.4 |
| Epic card | `epics/EPIC-001-foundation-1.md` |
| Lifecycle tailoring | `epics/EPIC-001-tailoring.md` |
| Module FSD / PRD | `docs/prds/` |
| Module TSD | `requirement/legacy/05-technical-architecture/` |
| Logical data model and data dictionary | `requirement/legacy/06-data/` |
| API specification | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v2.yaml` |
| Business rules and routing logic | `requirement/legacy/02-business-architecture-and-process/` |
| Error and message standard | `requirement/legacy/07-screens-and-experience/` |
| Engineering practices | `AGENTS.md` |

## Lifecycle tailoring

Shared record: `epics/EPIC-001-tailoring.md`. The phase classification is epic-level; this card records the story-specific agents and evidence.

## Story authority

| Role | Rights in this story |
|---|---|
| SY-CASEWF, case workflow module | Runs the sender step, applies R-UNI-33, R-UNI-35 and R-UNI-36 and raises the task |
| SY-DECLOG, decision log writer | Writes the entry for the move to the exception queue |
| RW-PLATADM, platform administrator | Reads deliveries and sends an exception delivery again (Platform administration CRUD) |
| RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY | Read deliveries (Platform administration R) |
| RW-SECADM, security administrator | Reads deliveries (Platform administration CRUDA) |
| No approval level from the delegation of authority applies | The story takes no business decision |

## Owners and approvals

| Gate | Accountable role | Name | Decision / date |
|---|---|---|---|
| Intake approval | Product Owner | TBC | |
| Context readiness | Forward Deployed Engineer | TBC | |
| Requirements approval (BRD / PRD) | Product Owner, FDA | TBC | |
| Design and architecture approval | Forward Deployed Architect | TBC | |
| Backlog and specification approval | Product Owner | TBC | |
| Plan approval | Forward Deployed Architect | TBC | |
| Task approval | Forward Deployed Engineer | TBC | |
| Pull request approval (code review) | Forward Deployed Engineer | TBC | |
| Quality and security gate | FDA, Quality Engineer, Security | TBC | |
| Release readiness | Forward Deployed Engineer | TBC | |
| Deployment approval | Product Owner / PM | TBC | |
| Operate and learn review | Ops / System Manager | TBC | |

`TBC` is not an approval (`GAP-006`). The story is in delivery at the specification stage; the human gates remain open until named.

## Agents selected

| Lifecycle group | Agent | Applicable / Optional / Not used | Reason |
|---|---|---|---|
| Requirements and discovery | Context Builder | Not used | The context package exists; reuse `.github/contexts/` and `EPIC-001`. |
| Requirements and discovery | BRD Builder | Not used | The BRD is approved; reuse it. |
| Requirements and discovery | PRD Builder | Not used | The FSD/PRD is approved; reuse it. |
| Design, backlog and spec | Jira Backlog Manager | Optional | The local story file is the backlog; Jira import is TBC. |
| Design, backlog and spec | Technical Specifier | Applicable | Produces the implementation-ready spec. |
| Plan and build | Implementation Planner | Applicable | Produces `plan.md` and `tasks.md`. |
| Plan and build | Implementation Builder | Applicable | Builds the approved plan in the ACE repository. |
| Quality and release | Compliance Reviewer | Applicable | Spec, plan and code gates. |
| Quality and release | API Tester | Applicable | Required by the spec's API scope. |
| Quality and release | Functional Automation Test | Not used | UI is not in scope. |
| Quality and release | Azure Deploy pipeline | Not used | ACE uses its own pipeline. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Feature flag:** `rwb.integration.outbox`. Off: the event step does not run and deliveries stay PENDING; the writer still records events so nothing is lost when it is switched on.
- **Critical path:** No; **depends on:** RWB-E1-044, RWB-E1-027, RWB-E1-007.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: consumers, owners, retry counts, delays and batch size are configuration.
  - No personal data in logs, tests or prompts; payloads hold references and codes only, and the admin endpoint does not return the payload.
  - No read of another module's tables: case events and tasks go through the P3 interfaces; the decision log through P7.
  - No event or delivery is deleted; a delivery leaves the exception queue only by being sent again.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 006 Outbox and retry for outbound work v1.md` |
| Specification | `output/INC-028-epic-1-RWB-TE-006/specify/spec.md` |
| Compliance validation | `output/INC-028-epic-1-RWB-TE-006/specify/compliance-validation.md` |
| Agent run log | `output/INC-028-epic-1-RWB-TE-006/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-028-epic-1-RWB-TE-006/plan/` (TBC) |
| Implementation evidence | `output/INC-028-epic-1-RWB-TE-006/implement/` (TBC) |
| API / functional test reports | `output/INC-028-epic-1-RWB-TE-006/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-028-epic-1-RWB-TE-006/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-028-epic-1-RWB-TE-006/specify/compliance-validation.md`) |
| Acceptance criteria | 11 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 006 Outbox and retry for outbound work v1.md` |
| Output run | `output/INC-028-epic-1-RWB-TE-006/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
