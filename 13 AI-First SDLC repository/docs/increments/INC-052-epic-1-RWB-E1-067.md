# Increment Card — INC-052-epic-1-RWB-E1-067

**RWB-E1-067 — Every Workbench action into the interaction ledger**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-052` |
| Title | Every Workbench action into the interaction ledger |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-067` |
| RUN_ID | `INC-052-epic-1-RWB-E1-067` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-066 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P1 Recovery data engine. **Build group:** P1b.

## Scope

**Story:** As a **case owner (RW-CASEOWN)**, I want **every action the Workbench takes on my case written to the ledger when it is taken**, so that **I can read the history without assembling it from four systems**.

**Main flow:**
1. Publishing module: commits its change and writes the event to the outbox in the same transaction.
2. Outbox: delivers the event to LedgerEventListener, in order per case.
3. LedgerEventListener: checks the schema version is the current or the previous version for the event.
4. LedgerEventMapper: maps the event to a LedgerEntryCommand: EV-01 to CASE_CREATED, EV-02 to CASE_ALLOCATED, EV-04 to CASE_TRANSFERRED, EV-19 to CASE_ESCALATED, EV-16 to DOCUMENT_ATTACHED, EV-08 to DECISION_TAKEN with the decision log entry ID.
5. LedgerEventMapper: sets actor from the event header (user ID or service identity), source system WORKBENCH, source reference as the owning module and event ID, and the event's idempotency key.
6. InteractionLedgerWriter: appends the entry with the next case_seq.

**Out of scope:**
- The ledger store and writer (RWB-E1-066) and the read interface (RWB-E1-068).
- Contact outcomes from EFS, dispatch outcomes from WIN, SMS and LINE, and partner hand-overs (RWB-E2-034).
- Escalation events other than a timer breach (Epic 2 workflow screens).

**Business outcome and value hypothesis:** The Workbench creates, allocates, transfers and escalates cases, attaches documents and records decisions by rule, often with no person involved. If these actions are not in the ledger, the case owner sees the customer contacts but not what the Workbench did between them. Each action already publishes an application event to the outbox in the same transaction as the change (events.txt); a ledger listener turns each event into one entry with its source and actor. Events are delivered at least once, so the listener rejects a repeat by its idempotency key and counts it. Serves REQ-ILG-005, REQ-ILG-002 and REQ-ILG-007.

**Constraints and guardrails:**
- No business value in code: the event map and the retry limit are configuration.
- No personal data in logs, tests or prompts: entries from events carry codes and references only (events rule "Payload"); test events are synthetic.
- No read of another module's tables: everything the entry needs comes from the event; no query on assignment, document or decision_log_entry.
- The listener never acknowledges an event it has not written or moved to the exception queue.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 067 Every Workbench action into the interaction ledger v1.md` |
| Requirement IDs | REQ-ILG-005, REQ-ILG-002, REQ-ILG-007 |
| BRD section | Business Requirements Epic 1, section 3.1 (story) and section 4 (REQ-ILG-002, REQ-ILG-005, REQ-ILG-007) |
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
| SY-CASEWF, case workflow module | Runs the ledger listener and appends entries (Case record C) |
| SY-RULES, SY-OCR, SY-DECLOG | Appear as actors on entries; do not call the writer |
| SY-AGENT, agent platform | May not append (Case record R) |
| RW-PLATADM, platform administrator | Owns exception queue items from the listener; receives the incident |
| RW-CASEOWN, case owner | Reads the entries through RWB-E1-068 |

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
| Quality and release | API Tester | Not used | API is not in scope. |
| Quality and release | Functional Automation Test | Not used | UI is not in scope. |
| Quality and release | Azure Deploy pipeline | Not used | ACE uses its own pipeline. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Feature flag:** `rwb.dataengine.ledger-events`.
- **Critical path:** No; **depends on:** RWB-E1-066.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: the event map and the retry limit are configuration.
  - No personal data in logs, tests or prompts: entries from events carry codes and references only (events rule "Payload"); test events are synthetic.
  - No read of another module's tables: everything the entry needs comes from the event; no query on assignment, document or decision_log_entry.
  - The listener never acknowledges an event it has not written or moved to the exception queue.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 067 Every Workbench action into the interaction ledger v1.md` |
| Specification | `output/INC-052-epic-1-RWB-E1-067/specify/spec.md` |
| Compliance validation | `output/INC-052-epic-1-RWB-E1-067/specify/compliance-validation.md` |
| Agent run log | `output/INC-052-epic-1-RWB-E1-067/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-052-epic-1-RWB-E1-067/plan/` (TBC) |
| Implementation evidence | `output/INC-052-epic-1-RWB-E1-067/implement/` (TBC) |
| API / functional test reports | `output/INC-052-epic-1-RWB-E1-067/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-052-epic-1-RWB-E1-067/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-052-epic-1-RWB-E1-067/specify/compliance-validation.md`) |
| Acceptance criteria | 8 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 067 Every Workbench action into the interaction ledger v1.md` |
| Output run | `output/INC-052-epic-1-RWB-E1-067/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
