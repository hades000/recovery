# Increment Card — INC-050-epic-1-RWB-E1-067

**RWB-E1-067 — Every Workbench action into the interaction ledger**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-050` |
| Title | Every Workbench action into the interaction ledger |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-067` |
| RUN_ID | `INC-050-epic-1-RWB-E1-067` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | User story |
| Priority | Must |
| Build order | 50 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-066 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P1 Recovery data engine.

## Scope

**Story:** As a **case owner (RW-CASEOWN)**, I want **every action the Workbench takes on my case written to the ledger when it is taken**, so that **I can read the history without assembling it from four systems**.

**Business outcome:** The Workbench creates, allocates, transfers and escalates cases, attaches documents and records decisions by rule, often with no person involved. If these actions are not in the ledger, the case owner sees the customer contacts but not what the Workbench did between them. Each action already publishes an application event to the outbox in the same transaction as the change (events.txt); a ledger listener turns each event into one entry with its source and actor. Events are delivered at least once, so the listener rejects a repeat by its idempotency key and counts it. Serves REQ-ILG-005, REQ-ILG-002 and REQ-ILG-007.

**Main flow:**
1. Publishing module: commits its change and writes the event to the outbox in the same transaction.
2. Outbox: delivers the event to LedgerEventListener, in order per case.
3. LedgerEventListener: checks the schema version is the current or the previous version for the event.
4. LedgerEventMapper: maps the event to a LedgerEntryCommand: EV-01 to CASE_CREATED, EV-02 to CASE_ALLOCATED, EV-04 to CASE_TRANSFERRED, EV-19 to CASE_ESCALATED, EV-16 to DOCUMENT_ATTACHED, EV-08 to DECISION_TAKEN with the decision log entry ID.
5. LedgerEventMapper: sets actor from the event header (user ID or service identity), source system WORKBENCH, source reference as the owning module and event ID, and the event's idempotency key.
6. InteractionLedgerWriter: appends the entry with the next case_seq.

**Acceptance criteria:**
- AC1: Workbench events are captured
- AC2: The entry names its source
- AC3: Nothing is written twice
- AC4: An event with an unknown schema version
- AC5: The ledger write fails for an event
- AC6: Entries follow the order the events were written
- AC7: The same event on two threads at once
- AC8: An event for a case that does not exist

**Out of scope:**
- The ledger store and writer (RWB-E1-066) and the read interface (RWB-E1-068).
- Contact outcomes from EFS, dispatch outcomes from WIN, SMS and LINE, and partner hand-overs (RWB-E2-034).
- Escalation events other than a timer breach (Epic 2 workflow screens).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-067-every-workbench-action-into-the-interaction-ledger-v1.md` |
| Requirement IDs | REQ-ILG-005, REQ-ILG-002, REQ-ILG-007 |
| BRD section | Business Requirements Epic 1, section 3.1 (story) and section 4 (REQ-ILG-002, REQ-ILG-005, REQ-ILG-007) |
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
| SY-CASEWF, case workflow module | Runs the ledger listener and appends entries (Case record C) |
| SY-RULES, SY-OCR, SY-DECLOG | Appear as actors on entries; do not call the writer |
| SY-AGENT, agent platform | May not append (Case record R) |
| RW-PLATADM, platform administrator | Owns exception queue items from the listener; receives the incident |
| RW-CASEOWN, case owner | Reads the entries through RWB-E1-068 |

## Contract extract

**Listener** | Item | Value | |---|---| | Trigger | Outbox delivery of EV-01 CaseCreated, EV-02 CaseAllocated, EV-04 CaseTransferred, EV-08 DecisionRecorded, EV-16 DocumentStored, EV-19 TimerBreached | | Job name | None in batch.txt; the outbox consumer runs in the service, not as a scheduled job | | Input | Event header (event ID, idempotency key, schema version, occurred time, actor) and payload as in events.txt | | Output | One interaction row per event, or one hit on processed_event | | Events published | None | | Idempotency key | The event's idempotency key, unique on interaction.idempotency_key | | Restart behavior | At-least-once delivery; an unprocessed event is delivered again after a restart; three retries, then the exception queue (NFR-026) | **Published interface used (P1, from RWB-E1-066)** ```java LedgerEntryRef InteractionLedgerWriter.append(LedgerEntryCommand command);…

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

- No business value in code: the event map and the retry limit are configuration. - No personal data in logs, tests or prompts: entries from events carry codes and references only (events rule "Payload"); test events are synthetic. - No read of another module's tables: everything the entry needs comes from the event; no query on assignment, document or decision_log_entry. - The listener never acknowledges an event it has not written or moved to the exception queue.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-067-every-workbench-action-into-the-interaction-ledger-v1.md` |
| Specification | `output/INC-050-epic-1-RWB-E1-067/specify/spec.md` |
| Compliance validation | `output/INC-050-epic-1-RWB-E1-067/specify/compliance-validation.md` |
| Agent run log | `output/INC-050-epic-1-RWB-E1-067/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-050-epic-1-RWB-E1-067/plan/` |
| Implementation evidence | `output/INC-050-epic-1-RWB-E1-067/implement/` |
| API / functional test reports | `output/INC-050-epic-1-RWB-E1-067/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-050-epic-1-RWB-E1-067/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 8 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-067-every-workbench-action-into-the-interaction-ledger-v1.md` |
| Output run | `output/INC-050-epic-1-RWB-E1-067/` |

