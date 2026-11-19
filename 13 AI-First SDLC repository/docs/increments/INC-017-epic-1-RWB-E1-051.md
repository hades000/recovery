# Increment Card — INC-017-epic-1-RWB-E1-051

**RWB-E1-051 — Legacy feed jobs on ADF and Control-M**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-017` |
| Title | Legacy feed jobs on ADF and Control-M |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-051` |
| RUN_ID | `INC-017-epic-1-RWB-E1-051` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P2 Integration |
| Story type | User story |
| Priority | Must |
| Window | Window 1 |
| Critical path | No |
| Depends on | RWB-E1-001, RWB-E1-007 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P2 Integration. **Build group:** P2.

## Scope

**Story:** As a **data steward and data product owner (RW-DATASTEW)**, I want **the ALS, EFS, CCMS and SVAF feed jobs scheduled on Control-M and ADF, each writing a run record and alerting on failure**, so that **the squad loads run every day or week without a manual step**.

**Main flow:**
1. Platform administrator: commits the Control-M job definitions for the ALS and EFS extracts into COLLINS and the ADF pipelines for the CCMS and SVAF file moves to the `ops/` folder.
2. Pipeline: validates the definitions and deploys them to the environment through the bank's deployment path.
3. Control-M: runs the ALS and EFS extracts after COLLINS end of day; COLLINS completes its load before 05:00.
4. ADF: moves the weekly CCMS and SVAF files from the source drop folder to the Workbench SFTP inbound folder by Sunday 23:00 (assumed; DL12).
5. Scheduler: JOB-01 starts at 05:00 and reads the COLLINS load; JOB-09 starts Monday 04:00 and reads the CCMS and SVAF files through FileLoadAdapter.
6. SY-DATALOAD: each run writes an interface_run row with interface, business date, status, record count, start and end time.

**Out of scope:**
- The loaders and record checks for each data product: RWB-E1-003, RWB-E1-004 and RWB-E1-009.
- AMIS, RPS and GL feeds: Epic 3 and Epic 6.
- Run books for every other Epic 1 job: RWB-E1-056.
- The SCR-44 monitor screen: Epic 2.

**Business outcome and value hypothesis:** ALS and EFS data reach the Workbench through the COLLINS daily batch, and CCMS and SVAF through weekly files (ADR-005). Today the extracts and file moves are started by hand. This story puts the four feeds on the bank schedulers, records each run in the Workbench and tests each file layout in the pipeline, so a changed source field is found before it reaches production. It meets REQ-DRI-008, REQ-RDF-002, REQ-RDF-003 and REQ-RDF-004.

**Constraints and guardrails:**
- No business value in code: times, folders and retry windows are configuration rows or properties.
- No personal data in logs, tests or prompts; sample files are synthetic and run rows hold counts only.
- No read of another module's tables; records reach P1 only through its loaders.
- No direct call from the Workbench to ALS, EFS, CCMS or SVAF; the bank schedulers deliver to COLLINS and to the inbound folder.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 051 Legacy feed jobs on ADF and Control M v1.md` |
| Requirement IDs | REQ-DRI-008, REQ-RDF-002, REQ-RDF-003, REQ-RDF-004 |
| BRD section | Business Requirements Epic 1, section 3.2; Business Requirements Program, sections 5.1 and 5.2 |
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
| RW-PLATADM, platform administrator | Maintains the Control-M and ADF definitions; reruns a feed job (Platform administration, U) |
| RW-DATASTEW, data steward | Receives the alerts; reads run rows (Platform administration, R) |
| SY-DATALOAD, data load | Runs JOB-01 and JOB-09 and writes the run rows |
| RW-AUDIT, RW-COMPLY, RW-COE, RW-SECADM | Read run rows (Platform administration, R) |

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
- **Feature flag:** None.
- **Critical path:** No; **depends on:** RWB-E1-001, RWB-E1-007.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: times, folders and retry windows are configuration rows or properties.
  - No personal data in logs, tests or prompts; sample files are synthetic and run rows hold counts only.
  - No read of another module's tables; records reach P1 only through its loaders.
  - No direct call from the Workbench to ALS, EFS, CCMS or SVAF; the bank schedulers deliver to COLLINS and to the inbound folder.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 051 Legacy feed jobs on ADF and Control M v1.md` |
| Specification | `output/INC-017-epic-1-RWB-E1-051/specify/spec.md` |
| Compliance validation | `output/INC-017-epic-1-RWB-E1-051/specify/compliance-validation.md` |
| Agent run log | `output/INC-017-epic-1-RWB-E1-051/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-017-epic-1-RWB-E1-051/plan/` (TBC) |
| Implementation evidence | `output/INC-017-epic-1-RWB-E1-051/implement/` (TBC) |
| API / functional test reports | `output/INC-017-epic-1-RWB-E1-051/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-017-epic-1-RWB-E1-051/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — cleaned against the current story on 2026-11-05; no removed ACs are mapped |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-017-epic-1-RWB-E1-051/specify/compliance-validation.md`) |
| Acceptance criteria | 4 ACs in the current story (AC1, AC4, AC5, AC6) |
| AC numbering | Intentional gaps: AC2, AC3 (removed by the 4 November 2026 cleanup) |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 051 Legacy feed jobs on ADF and Control M v1.md` |
| Output run | `output/INC-017-epic-1-RWB-E1-051/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
