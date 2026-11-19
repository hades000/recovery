# Increment Card — INC-047-epic-1-RWB-E1-002

**RWB-E1-002 — Case list v1 with case ID, owner and queue**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-047` |
| Title | Case list v1 with case ID, owner and queue |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-002` |
| RUN_ID | `INC-047-epic-1-RWB-E1-002` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-018, RWB-E1-003, RWB-E1-007, RWB-E1-020 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P1 Recovery data engine. **Build group:** P1b.

## Scope

**Story:** As a **team manager (RW-TEAMMGR)**, I want **one case list with case number, account, product, stage, status, owner, queue, route, total balance and days past due for every account at 90 days past due or more, refreshed each working day and available in Power BI**, so that **every recovery team works from one list**.

**Main flow:**
1. Quartz: JOB-04 Daily reconciliation reaches its case list step after JOB-03 completes for the business date.
2. System: checks through `LoadRunQuery.completedLoad("INT-01", businessDate)` that the account load for the business date is COMPLETED.
3. System: opens a load_run row with job code JOB-04 and product DP03.
4. System: reads the open case accounts from `CaseQueryApi.openCaseAccounts(businessDate)`.
5. System: joins each account to loan_account for account number, total balance and days past due.
6. System: replaces the case_list_row rows for the business date in one transaction, each with the refresh time.

**Out of scope:**
- The reconciliation by product, the balance reconciliation, the red and green report and the hold of the publish (RWB-E1-011).
- The latest contact per case on the list (RWB-E1-004).
- The Workbench case list screen with queue and owner filters and export (RWB-E1-031).
- Row-level security by team in Power BI (RWB-E1-016).
- Queue measures and ageing (RWB-E1-030).

**Business outcome and value hypothesis:** Each recovery team keeps its own list of accounts today, and the lists do not agree with each other or with ALS. This story builds one case list each working day from the open cases and the account and arrears data product, checks its count against the ALS count of accounts at 90 days past due or more, and publishes it to Power BI. It meets REQ-RDF-007 (the case list reconciles daily to the ALS count, DL25) and serves the measure "loads on time and complete on 99 percent of days".

**Constraints and guardrails:**
- No business value in code: the threshold, the tolerance and the wait time are parameters.
- No personal data in logs, tests or prompts. The list holds no customer name, ID number or contact value.
- No read of another module's tables. recovery_case, case_account and queue are read only through `CaseQueryApi`.
- The extract file goes to the data lake only through the outbound file adapter.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 002 Case list v1 with case ID owner and queue v1.md` |
| Requirement IDs | REQ-RDF-007 |
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
| SY-DATALOAD, data load from COLLINS | Runs the case list step; writes case_list_row, load_run and dq_exception |
| SY-CASEWF, case workflow module | Serves `CaseQueryApi` |
| RW-PLATADM, platform administrator | Lists the runs (Platform administration R) and reruns the step (Platform administration U) |
| RW-DATASTEW, RW-COE, RW-AUDIT, RW-COMPLY, RW-SECADM | List the runs (Platform administration R) |
| RW-BIANAL, reporting and BI analyst | Builds and schedules the Power BI data set (Reporting CRUD) |
| RW-TEAMMGR, RW-CASEOWN, RW-PHONECOL | Read the case list report in Power BI (Reporting R); row-level security by team follows RWB-E1-016 |

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
- **Feature flag:** `rwb.p1.case-list`. Off: JOB-04 skips the case list step.
- **Critical path:** No; **depends on:** RWB-E1-018, RWB-E1-003, RWB-E1-007, RWB-E1-020.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: the threshold, the tolerance and the wait time are parameters.
  - No personal data in logs, tests or prompts. The list holds no customer name, ID number or contact value.
  - No read of another module's tables. recovery_case, case_account and queue are read only through `CaseQueryApi`.
  - The extract file goes to the data lake only through the outbound file adapter.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 002 Case list v1 with case ID owner and queue v1.md` |
| Specification | `output/INC-047-epic-1-RWB-E1-002/specify/spec.md` |
| Compliance validation | `output/INC-047-epic-1-RWB-E1-002/specify/compliance-validation.md` |
| Agent run log | `output/INC-047-epic-1-RWB-E1-002/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-047-epic-1-RWB-E1-002/plan/` (TBC) |
| Implementation evidence | `output/INC-047-epic-1-RWB-E1-002/implement/` (TBC) |
| API / functional test reports | `output/INC-047-epic-1-RWB-E1-002/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-047-epic-1-RWB-E1-002/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-047-epic-1-RWB-E1-002/specify/compliance-validation.md`) |
| Acceptance criteria | 10 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 002 Case list v1 with case ID owner and queue v1.md` |
| Output run | `output/INC-047-epic-1-RWB-E1-002/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
