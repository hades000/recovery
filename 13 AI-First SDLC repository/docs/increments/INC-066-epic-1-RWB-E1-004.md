# Increment Card — INC-066-epic-1-RWB-E1-004

**RWB-E1-004 — EFS extract load**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-066` |
| Title | EFS extract load |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-004` |
| RUN_ID | `INC-066-epic-1-RWB-E1-004` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-003, RWB-E1-015, RWB-E1-002 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P1 Recovery data engine. **Build group:** P1b.

## Scope

**Story:** As a **data steward and data product owner (RW-DATASTEW)**, I want **the EFS contacts and promises for accounts at 90 days past due loaded each working day from the COLLINS daily batch**, so that **the contact history is on the case from its first day**.

**Main flow:**
1. Quartz: JOB-01 attempt reaches the INT-07 step after the INT-01 step has completed for the business date.
2. System: opens a load_run for INT-07 and checks that the mapping version in force is approved.
3. System: runs DQ-036 business date, DQ-037 structure, DQ-038 control total and DQ-039 keys; any failure refuses the load.
4. System: runs DQ-040 references (the account key matches loan_account) and DQ-041 lists of values; above 0.50 percent the load is refused.
5. System: skips records whose action code is not in the named list and counts them.
6. System: maps the remaining records and inserts collections_history rows by their EFS record key in one transaction; a key already held is not inserted again.

**Out of scope:**
- Copying the history into the interaction ledger at case entry (RWB-E1-018, RWB-E1-066).
- The contact history on the case record view (RWB-E1-023, RWB-E1-035).
- The automated EFS file load that replaces the manual file handling (FEAT-CHO-10, Epic 2).
- Contact repository and consent per channel (FEAT-COM-05, Epic 4).
- X6 lost contact and skip trace (FEAT-DVF-06, Epic 7).

**Business outcome and value hypothesis:** When an account moves from collections to recovery today, the case owner does not see what the phone team agreed with the customer, and the customer can be called twice or asked again for a promise already made. This story loads the EFS contact and promise records (INT-07) into the collections history held by the Workbench, checked like every other load, and puts the latest contact on the case list. It meets REQ-RDF-003 and serves NFR-014 (collections data ingested at start of day).

**Constraints and guardrails:**
- No business value in code: the window end, the named list of action codes and the mapping are data.
- No personal data in logs, tests or prompts. Free-text notes are not loaded; dq_exception holds the account key only.
- No read of another module's tables. P3 reads the history through CollectionsHistoryApi; this story never writes interaction.
- No call to EFS; the only input is the COLLINS staging records.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 004 EFS extract load v1.md` |
| Requirement IDs | REQ-RDF-003 |
| BRD section | Business Requirements Epic 1, section 3.1; Business Requirements Program, section 5.1 |
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
| SY-DATALOAD, data load from COLLINS | Runs the INT-07 step; writes collections_history, load_run, dq_exception and the case list columns; records the DP05 load through FreshnessStampService |
| RW-PLATADM, platform administrator | Lists runs (Platform administration R); reruns a refused or late load (Platform administration U) |
| RW-DATASTEW, data steward and data product owner | Lists runs (Platform administration R); records the EFS owner's sign-off on the mapping version through the reference data change process |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-SECADM | List runs (Platform administration R) |

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
- **Feature flag:** `rwb.p1.efs-load`. Off: JOB-01 skips the INT-07 step and the window check.
- **Critical path:** No; **depends on:** RWB-E1-003, RWB-E1-015, RWB-E1-002.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: the window end, the named list of action codes and the mapping are data.
  - No personal data in logs, tests or prompts. Free-text notes are not loaded; dq_exception holds the account key only.
  - No read of another module's tables. P3 reads the history through CollectionsHistoryApi; this story never writes interaction.
  - No call to EFS; the only input is the COLLINS staging records.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 004 EFS extract load v1.md` |
| Specification | `output/INC-066-epic-1-RWB-E1-004/specify/spec.md` |
| Compliance validation | `output/INC-066-epic-1-RWB-E1-004/specify/compliance-validation.md` |
| Agent run log | `output/INC-066-epic-1-RWB-E1-004/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-066-epic-1-RWB-E1-004/plan/` (TBC) |
| Implementation evidence | `output/INC-066-epic-1-RWB-E1-004/implement/` (TBC) |
| API / functional test reports | `output/INC-066-epic-1-RWB-E1-004/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-066-epic-1-RWB-E1-004/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-066-epic-1-RWB-E1-004/specify/compliance-validation.md`) |
| Acceptance criteria | 10 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 004 EFS extract load v1.md` |
| Output run | `output/INC-066-epic-1-RWB-E1-004/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
