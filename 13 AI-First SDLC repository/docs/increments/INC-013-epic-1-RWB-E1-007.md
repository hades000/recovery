# Increment Card — INC-013-epic-1-RWB-E1-007

**RWB-E1-007 — Integration adapters for file loads and outbound files**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-013` |
| Title | Integration adapters for file loads and outbound files |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-007` |
| RUN_ID | `INC-013-epic-1-RWB-E1-007` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P2 Integration |
| Story type | User story |
| Priority | Must |
| Window | Window 1 |
| Critical path | Yes |
| Depends on | RWB-E1-001 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P2 Integration. **Build group:** P2.

## Scope

**Story:** As a **platform administrator (RW-PLATADM)**, I want **one adapter pattern for every file load and outbound file, with file checks, a run log, retry and an exception queue**, so that **every later interface follows one pattern and a failed file is found on the day it fails**.

**Main flow:**
1. Scheduler: JOB-09 starts the file load for an inbound interface, for example INT-10 CCMS, at its time.
2. SY-DATALOAD: the FileLoadAdapter reads the interface configuration row in force and lists the inbound folder for the file pattern and business date.
3. SY-DATALOAD: the adapter writes an interface_run row with status RECEIVED, the file name, the file hash and the business date.
4. SY-DATALOAD: the adapter runs the file checks held as data (business date, structure, control total, keys) against the header and trailer.
5. SY-DATALOAD: when every file check passes, the adapter hands the records to the owning module's loader through its published interface and sets the run to LOADED with the record count.
6. Owning module: writes an outbound file request through OutboundFiles.enqueue, for example JOB-10 for the daily WIN notice file (INT-14).

**Out of scope:**
- The record-level checks (references, lists of values, movement) and the stale marker: P1 loaders, RWB-E1-015 and RWB-E1-016.
- The run books and job monitoring: RWB-E1-056.
- The Control-M and ADF schedules of the source extracts: RWB-E1-051.
- The full SCR-44 interface and job monitor: Epic 2 and Epic 8.
- The WIN notice content and template: RWB-E2-021.

**Business outcome and value hypothesis:** Each source outside COLLINS is reached today by hand or by a one-off file, and failures are found late. This story builds the one path every file takes in and out: checked, logged, retried on a schedule held as data, and moved to the exception queue with a task for a named owner after the retry limit. It meets REQ-DRI-006, REQ-DRI-007 and REQ-DRI-008 and serves the FSD P2 measure "outbound items in the exception queue over one day: zero".

**Constraints and guardrails:**
- No business value in code: retry counts, intervals, folders, patterns, owners and check tolerances are read from tables.
- No personal data in logs, tests or prompts; file contents are never logged, only names, counts, hashes and check results.
- No read of another module's tables; records reach the owning module only through its RecordLoader.
- Only SftpTransport opens a connection to another system; the boundary test fails the build on any other call.
- Outbound items carry case IDs, never addresses or names.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 007 Integration adapters for file loads and outbound files v1.md` |
| Requirement IDs | REQ-DRI-006, REQ-DRI-007, REQ-DRI-008 |
| BRD section | Business Requirements Epic 1, section 3.2; Business Requirements Program, section 5.2 |
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
| SY-DATALOAD, data load | Reads files, runs the file checks, writes run rows and outbound items, sends files |
| SY-CASEWF, case workflow module | Moves the route state on SYSTEM_UNAVAILABLE, RETRY_SUCCEEDED, RETRY_LIMIT_REACHED and OUTBOUND_FAILED and raises the task |
| RW-PLATADM, platform administrator | Lists exception items and resends one (Platform administration, U) |
| RW-DATASTEW, data steward | Receives the refused load alert; reads run rows (Platform administration, R) |
| RW-REFADM, reference data administrator | Loads a new interface configuration version |
| RW-AUDIT, RW-COMPLY, RW-COE, RW-SECADM | Read run rows and exception items (Platform administration, R) |

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
| Quality and release | Functional Automation Test | Applicable | Required by the spec's UI scope. |
| Quality and release | Azure Deploy pipeline | Not used | ACE uses its own pipeline. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Feature flag:** None.
- **Critical path:** Yes; **depends on:** RWB-E1-001.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: retry counts, intervals, folders, patterns, owners and check tolerances are read from tables.
  - No personal data in logs, tests or prompts; file contents are never logged, only names, counts, hashes and check results.
  - No read of another module's tables; records reach the owning module only through its RecordLoader.
  - Only SftpTransport opens a connection to another system; the boundary test fails the build on any other call.
  - Outbound items carry case IDs, never addresses or names.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 007 Integration adapters for file loads and outbound files v1.md` |
| Specification | `output/INC-013-epic-1-RWB-E1-007/specify/spec.md` |
| Compliance validation | `output/INC-013-epic-1-RWB-E1-007/specify/compliance-validation.md` |
| Agent run log | `output/INC-013-epic-1-RWB-E1-007/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-013-epic-1-RWB-E1-007/plan/` (TBC) |
| Implementation evidence | `output/INC-013-epic-1-RWB-E1-007/implement/` (TBC) |
| API / functional test reports | `output/INC-013-epic-1-RWB-E1-007/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-013-epic-1-RWB-E1-007/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — cleaned against the current story on 2026-11-05; no removed ACs are mapped |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-013-epic-1-RWB-E1-007/specify/compliance-validation.md`) |
| Acceptance criteria | 8 ACs in the current story (AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9) |
| AC numbering | Intentional gaps: AC1 (removed by the 4 November 2026 cleanup) |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 007 Integration adapters for file loads and outbound files v1.md` |
| Output run | `output/INC-013-epic-1-RWB-E1-007/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
