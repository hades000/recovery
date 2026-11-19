# Increment Card — INC-046-epic-1-RWB-E1-066

**RWB-E1-066 — Interaction ledger store and writer**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-046` |
| Title | Interaction ledger store and writer |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-066` |
| RUN_ID | `INC-046-epic-1-RWB-E1-066` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-018, RWB-E1-027 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P1 Recovery data engine. **Build group:** P1b.

## Scope

**Story:** As a **case owner (RW-CASEOWN)**, I want **every contact, letter, promise, payment and hand-over on the case written to one ledger when it is recorded**, so that **the history of the case is never assembled after the fact**.

**Main flow:**
1. Case owner: records a call with POST /cases/{caseId}/interactions (channel CALL, direction OUTBOUND, result RIGHT_PARTY, summary, promise amount and date).
2. P3 interactions handler: checks Case record C and the case scope, opens a transaction and calls InteractionLedgerWriter.append().
3. InteractionLedgerWriter: validates the command (case, event code in LOV-LEDGER-EVENT, occurred time, actor, source, idempotency key).
4. InteractionLedgerWriter: takes a transaction-level advisory lock on the case ID and assigns case_seq as the case's highest case_seq plus 1.
5. InteractionLedgerWriter: inserts the entry with event code, actor type and reference, source system and source reference, channel and direction where they apply, and the decision log entry ID for a decision.
6. P3 handler: commits the action and the entry in one transaction and returns 201 with the Interaction.

**Out of scope:**
- Writing the Workbench events from the outbox to the ledger and duplicate rejection (RWB-E1-067).
- The ledger read interface and its filters (RWB-E1-068).
- Contact and dispatch outcomes from EFS, WIN, SMS and LINE, partner hand-overs and the timeline view (RWB-E2-034).
- The retention class for ledger entries (FEAT-ILG-10, RWB-E2-034).

**Business outcome and value hypothesis:** Today the history of a recovery case is spread across EFS, LIT, letters and team spreadsheets, and an officer rebuilds it by hand before each decision. One append-only ledger per case, written in the same transaction as the action it records, gives one ordered history with no gap. The ledger records what happened with the customer; the decision log records why the system acted; each ledger entry for a decision points to its decision log entry. A ledger write that fails stops the action and raises an incident, so the history never has a silent gap. Serves REQ-ILG-001, REQ-ILG-002, REQ-ILG-004 and REQ-ILG-008; NFR-070 and NFR-077.

**Constraints and guardrails:**
- No business value in code: event codes are list values; channels, directions and results come from their lists.
- No personal data in logs, tests or prompts: the incident detail names the case ID and the error class only; the summary is never logged; test summaries are synthetic.
- No read of another module's tables: decision details come through the P7 interface; the interaction table is written only through InteractionLedgerWriter and read only through RWB-E1-068.
- No entry is ever updated or deleted by application code.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 066 Interaction ledger store and writer v1.md` |
| Requirement IDs | REQ-ILG-001, REQ-ILG-002, REQ-ILG-004, REQ-ILG-008 |
| BRD section | Business Requirements Epic 1, section 3.1 (story) and section 4 (REQ-ILG-001, REQ-ILG-002, REQ-ILG-004, REQ-ILG-008) |
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
| RW-CASEOWN, case owner | Records contacts and promises on own cases (Case record C, scope Own) |
| RW-TEAMMGR, RW-PHONECOL and other case roles | Read entries only in this story (Case record R) |
| SY-CASEWF, case workflow module | Appends entries for case actions (Case record C) |
| SY-DATALOAD, data load | Appends entries from the EFS and ALS loads (Case record C) |
| RW-AUDIT, internal audit | Reads only; may not record (Case record R) |
| RW-PLATADM, platform administrator | Receives the LEDGER_WRITE_FAILED incident |

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
- **Feature flag:** `rwb.dataengine.ledger-writer`.
- **Critical path:** No; **depends on:** RWB-E1-018, RWB-E1-027.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: event codes are list values; channels, directions and results come from their lists.
  - No personal data in logs, tests or prompts: the incident detail names the case ID and the error class only; the summary is never logged; test summaries are synthetic.
  - No read of another module's tables: decision details come through the P7 interface; the interaction table is written only through InteractionLedgerWriter and read only through RWB-E1-068.
  - No entry is ever updated or deleted by application code.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 066 Interaction ledger store and writer v1.md` |
| Specification | `output/INC-046-epic-1-RWB-E1-066/specify/spec.md` |
| Compliance validation | `output/INC-046-epic-1-RWB-E1-066/specify/compliance-validation.md` |
| Agent run log | `output/INC-046-epic-1-RWB-E1-066/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-046-epic-1-RWB-E1-066/plan/` (TBC) |
| Implementation evidence | `output/INC-046-epic-1-RWB-E1-066/implement/` (TBC) |
| API / functional test reports | `output/INC-046-epic-1-RWB-E1-066/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-046-epic-1-RWB-E1-066/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-046-epic-1-RWB-E1-066/specify/compliance-validation.md`) |
| Acceptance criteria | 8 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 066 Interaction ledger store and writer v1.md` |
| Output run | `output/INC-046-epic-1-RWB-E1-066/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
