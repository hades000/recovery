# Increment Card — INC-025-epic-1-RWB-E1-027

**RWB-E1-027 — Decision log writer v1**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-025` |
| Title | Decision log writer v1 |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-027` |
| RUN_ID | `INC-025-epic-1-RWB-E1-027` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P7 Decision center and log |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | Yes |
| Depends on | RWB-E1-008, RWB-E1-056 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P7 Decision center and log. **Build group:** P7.

## Scope

**Story:** As the **case workflow module (SY-CASEWF)**, I want **one writer that validates and records case created, owner assigned, case transferred and document attached, with the rule ID and version used, in the same transaction as the action**, so that **the first decision records exist in Epic 1 and no action proceeds without its record**.

**Main flow:**
1. Calling module (for example SY-CASEWF in the morning allocation): builds a DecisionLogRecord with the case, the event, the rule ID and version, the inputs reference, the actor and an idempotency key, inside its own transaction.
2. Calling module: calls DecisionLogWriter.write as the last step before commit.
3. Writer (DecisionLogWriterService): checks that a transaction is open; refuses the call if not.
4. Writer: checks the idempotency key; for a key already written, returns the first entry reference and counts the repeat.
5. Writer (DecisionLogRecordValidator): checks the required fields and the version group; refuses an incomplete record with the missing field named.
6. Writer: calls DecisionLogStore.append (RWB-E1-008).

**Out of scope:**
- The store, the hash chain and the verifier (RWB-E1-008).
- Approval records with the limit applied (RWB-E2-013).
- Access events (RWB-E1-039).
- The copy to the data lake (RWB-E1-014).
- The recommendation service with reasons for the route decision (Epic 4, API-P7-001).

**Business outcome and value hypothesis:** Without one writer, each module would build its own record and some actions would go unrecorded. This story gives every module one published interface that checks each record against the seven field groups, refuses an incomplete record, writes it in the caller's transaction so that a failed write stops the action, ignores a repeated event and publishes DecisionRecorded. It meets REQ-DRI-004 and REQ-DRI-005 and is the automated part of control CTL-06. The measure is decisions with a log entry: target 100 percent, and no action without one (NFR-034).

**Constraints and guardrails:**
- No business value in code: decision codes per event are parameters and list values.
- No personal data in logs, tests or prompts; a refused record is logged with its case ID and field name only.
- No read of another module's tables; callers pass the values in the record.
- No write path to decision_log_entry other than this interface, checked by an architecture test.
- No retry inside the writer; the caller's job or request retries.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 027 Decision log writer v1 v1.md` |
| Requirement IDs | REQ-DRI-004, REQ-DRI-005 |
| BRD section | Business Requirements Epic 1, section 3.7; Business Requirements Program, section 5.7 |
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
| SY-DECLOG Decision log writer | Writes entries (Decision log C) |
| SY-CASEWF Case workflow module | Calls the writer for case created, owner assigned and case transferred (Decision log C) |
| SY-OCR OCR and extraction pipeline | Calls the writer for document attached (Decision log C) |
| SY-RULES, SY-DATALOAD, SY-AGENT | Call the writer for their own decisions (Decision log C) |
| RW-AUDIT, RW-COE and every role holding Decision log R | Read the entries |
| RW-PLATADM Platform administrator | Receives the incident when a write fails |

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
- **Feature flag:** `rwb.decision.log-writer`.
- **Critical path:** Yes; **depends on:** RWB-E1-008, RWB-E1-056.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: decision codes per event are parameters and list values.
  - No personal data in logs, tests or prompts; a refused record is logged with its case ID and field name only.
  - No read of another module's tables; callers pass the values in the record.
  - No write path to decision_log_entry other than this interface, checked by an architecture test.
  - No retry inside the writer; the caller's job or request retries.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 027 Decision log writer v1 v1.md` |
| Specification | `output/INC-025-epic-1-RWB-E1-027/specify/spec.md` |
| Compliance validation | `output/INC-025-epic-1-RWB-E1-027/specify/compliance-validation.md` |
| Agent run log | `output/INC-025-epic-1-RWB-E1-027/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-025-epic-1-RWB-E1-027/plan/` (TBC) |
| Implementation evidence | `output/INC-025-epic-1-RWB-E1-027/implement/` (TBC) |
| API / functional test reports | `output/INC-025-epic-1-RWB-E1-027/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-025-epic-1-RWB-E1-027/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-025-epic-1-RWB-E1-027/specify/compliance-validation.md`) |
| Acceptance criteria | 7 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 027 Decision log writer v1 v1.md` |
| Output run | `output/INC-025-epic-1-RWB-E1-027/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
