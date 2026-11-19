# Increment Card — INC-044-epic-1-RWB-E1-066

**RWB-E1-066 — Interaction ledger store and writer**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-044` |
| Title | Interaction ledger store and writer |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-066` |
| RUN_ID | `INC-044-epic-1-RWB-E1-066` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | User story |
| Priority | Must |
| Build order | 44 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-018, RWB-E1-027 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P1 Recovery data engine.

## Scope

**Story:** As a **case owner (RW-CASEOWN)**, I want **every contact, letter, promise, payment and hand-over on the case written to one ledger when it is recorded**, so that **the history of the case is never assembled after the fact**.

**Business outcome:** Today the history of a recovery case is spread across EFS, LIT, letters and team spreadsheets, and an officer rebuilds it by hand before each decision. One append-only ledger per case, written in the same transaction as the action it records, gives one ordered history with no gap. The ledger records what happened with the customer; the decision log records why the system acted; each ledger entry for a decision points to its decision log entry. A ledger write that fails stops the action and raises an incident, so the history never has a silent gap. Serves REQ-ILG-001, REQ-ILG-002, REQ-ILG-004 and REQ-ILG-008; NFR-070 and NFR-077.

**Main flow:**
1. Case owner: records a call with POST /cases/{caseId}/interactions (channel CALL, direction OUTBOUND, result RIGHT_PARTY, summary, promise amount and date).
2. P3 interactions handler: checks Case record C and the case scope, opens a transaction and calls InteractionLedgerWriter.append().
3. InteractionLedgerWriter: validates the command (case, event code in LOV-LEDGER-EVENT, occurred time, actor, source, idempotency key).
4. InteractionLedgerWriter: takes a transaction-level advisory lock on the case ID and assigns case_seq as the case's highest case_seq plus 1.
5. InteractionLedgerWriter: inserts the entry with event code, actor type and reference, source system and source reference, channel and direction where they apply, and the decision log entry ID for a decision.
6. P3 handler: commits the action and the entry in one transaction and returns 201 with the Interaction.

**Acceptance criteria:**
- AC1: The ledger exists and is written to
- AC2: It is ordered and complete
- AC3: It is distinct from the decision log
- AC4: A write failure is visible
- AC5: A required value is missing
- AC6: Two entries for one case at the same moment
- AC7: A case that does not exist
- AC8: An entry cannot be changed

**Out of scope:**
- Writing the Workbench events from the outbox to the ledger and duplicate rejection (RWB-E1-067).
- The ledger read interface and its filters (RWB-E1-068).
- Contact and dispatch outcomes from EFS, WIN, SMS and LINE, partner hand-overs and the timeline view (RWB-E2-034).
- The retention class for ledger entries (FEAT-ILG-10, RWB-E2-034).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-066-interaction-ledger-store-and-writer-v1.md` |
| Requirement IDs | REQ-ILG-001, REQ-ILG-002, REQ-ILG-004, REQ-ILG-008 |
| BRD section | Business Requirements Epic 1, section 3.1 (story) and section 4 (REQ-ILG-001, REQ-ILG-002, REQ-ILG-004, REQ-ILG-008) |
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
| RW-CASEOWN, case owner | Records contacts and promises on own cases (Case record C, scope Own) |
| RW-TEAMMGR, RW-PHONECOL and other case roles | Read entries only in this story (Case record R) |
| SY-CASEWF, case workflow module | Appends entries for case actions (Case record C) |
| SY-DATALOAD, data load | Appends entries from the EFS and ALS loads (Case record C) |
| RW-AUDIT, internal audit | Reads only; may not record (Case record R) |
| RW-PLATADM, platform administrator | Receives the LEDGER_WRITE_FAILED incident |

## Contract extract

**Endpoint used (P3, API-P3-015)** | Item | Value | |---|---| | Method and path | POST /api/recovery/v1/cases/{caseId}/interactions | | Request | InteractionRequest: channel, direction, result, summary | | Response | 201 Interaction: id, caseId, partyId, occurredAt, channel, direction, actionCode, contactResult, promiseAmount, promiseDate, summary, conductCheck, sourceSystem | | Errors | 401 no session (MSG-P4-001); 403 no Case record C (MSG-P4-002); 404 case missing or out of scope (MSG-P4-003); 422 field invalid (MSG-GEN-001); 503 ledger write failed (MSG-P1-022) | | Authorization | Case record, C, scope applied | | Idempotency | The handler builds the idempotency key from the request ID header; a repeat returns the first entry (RWB-E1-067) | **Published interface (P1)** ```java package recovery.dataengine.ledger.api; public interface InteractionLedgerWriter { /** Must run inside the…

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

- No business value in code: event codes are list values; channels, directions and results come from their lists. - No personal data in logs, tests or prompts: the incident detail names the case ID and the error class only; the summary is never logged; test summaries are synthetic. - No read of another module's tables: decision details come through the P7 interface; the interaction table is written only through InteractionLedgerWriter and read only through RWB-E1-068. - No entry is ever updated or deleted by application code.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-066-interaction-ledger-store-and-writer-v1.md` |
| Specification | `output/INC-044-epic-1-RWB-E1-066/specify/spec.md` |
| Compliance validation | `output/INC-044-epic-1-RWB-E1-066/specify/compliance-validation.md` |
| Agent run log | `output/INC-044-epic-1-RWB-E1-066/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-044-epic-1-RWB-E1-066/plan/` |
| Implementation evidence | `output/INC-044-epic-1-RWB-E1-066/implement/` |
| API / functional test reports | `output/INC-044-epic-1-RWB-E1-066/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-044-epic-1-RWB-E1-066/review/` |
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
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-066-interaction-ledger-store-and-writer-v1.md` |
| Output run | `output/INC-044-epic-1-RWB-E1-066/` |

