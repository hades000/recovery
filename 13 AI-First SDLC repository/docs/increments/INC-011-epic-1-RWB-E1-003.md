# Increment Card — INC-011-epic-1-RWB-E1-003

**RWB-E1-003 — ALS daily extract load**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-011` |
| Title | ALS daily extract load |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-003` |
| RUN_ID | `INC-011-epic-1-RWB-E1-003` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | User story |
| Priority | Must |
| Window | Window 1 |
| Critical path | No |
| Depends on | RWB-E1-001 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P1 Recovery data engine. **Build group:** P1a.

## Scope

**Story:** As a **data steward and data product owner (RW-DATASTEW)**, I want **ALS balances, arrears, payments and classification loaded every working day from the COLLINS daily batch for accounts at 90 days past due or more**, so that **account and arrears data is current to the previous working day**.

**Main flow:**
1. Quartz: starts JOB-01 COLLINS load check and intake at 05:00 for the expected business date, the previous working day.
2. System: opens a load_run row for INT-01 with status RUNNING; the unique key (interface, business date) stops a second run.
3. System: runs DQ-001 business date, DQ-002 structure, DQ-003 control total and DQ-004 keys on the staging records; any failure refuses the load.
4. System: runs DQ-005 references and DQ-006 lists of values; records that fail are counted, and the load is refused if the count is above 0.50 percent.
5. System: maps each record through the mapping version in force and the code map, and writes loan_account in one transaction, with data_as_of set to the business date.
6. System: writes the held records to dq_exception with the check code and the account number.

**Out of scope:**
- Case creation from the loaded accounts (JOB-02, RWB-E1-018).
- Payment matching to plans and settlements (JOB-07, Epic 2 and later).
- The data quality rules on loaded rows (RWB-E1-006) and the daily reconciliation (RWB-E1-011).
- The freshness stamp, the stale flag on LoadRefused, the check at 08:00 and MSG-P1-001 (RWB-E1-015).
- The SCBPDM and UDP loads (INT-04, INT-05) and the EFS load (RWB-E1-004).
- The job monitor screen SCR-44 (Epic 2).

**Business outcome and value hypothesis:** Case owners today read balances and days past due from ALS screens and team files, so two people can see two different numbers for one account. This story loads INT-01 (accounts) and INT-02 (payments) from the COLLINS daily batch into the account and arrears data product DP01, after the seven load checks, so every case reads one checked balance with its business date. It meets REQ-RDF-002 and serves the measure "loads on time and complete on 99 percent of days" and the load target "job runs by 07:00" (NFR-013).

**Constraints and guardrails:**
- No business value in code: tolerances, window times, sample size, mappings and code maps are data.
- No personal data in logs, tests or prompts. dq_exception.record_key holds the account key only; test data is synthetic in DEV and masked in SIT.
- No read of another module's tables. Reference values come through the P4 published interface; case data is not read.
- No call to ALS or any system of record; the only input is the COLLINS staging records (ADR-005).
- No partial load is ever visible: the write is one transaction per interface.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 003 ALS daily extract load v1.md` |
| Requirement IDs | REQ-RDF-002 |
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
| SY-DATALOAD, data load from COLLINS | Runs JOB-01; writes loan_account, account_payment, load_run, dq_exception and the DP01 status |
| RW-PLATADM, platform administrator | Lists jobs (Platform administration R) and reruns a refused, late or failed load (Platform administration U) |
| RW-SECADM, security administrator | Lists and reruns (Platform administration CRUDA); used only under break-glass |
| RW-DATASTEW, RW-COE, RW-AUDIT, RW-COMPLY | List jobs and their checks (Platform administration R); no rerun |
| Data steward group, platform administrator group | Receive the load alerts |

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
- **Feature flag:** `rwb.p1.als-load`. Off: JOB-01 skips the INT-01 and INT-02 steps and records nothing.
- **Critical path:** No; **depends on:** RWB-E1-001.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: tolerances, window times, sample size, mappings and code maps are data.
  - No personal data in logs, tests or prompts. dq_exception.record_key holds the account key only; test data is synthetic in DEV and masked in SIT.
  - No read of another module's tables. Reference values come through the P4 published interface; case data is not read.
  - No call to ALS or any system of record; the only input is the COLLINS staging records (ADR-005).
  - No partial load is ever visible: the write is one transaction per interface.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 003 ALS daily extract load v1.md` |
| Specification | `output/INC-011-epic-1-RWB-E1-003/specify/spec.md` |
| Compliance validation | `output/INC-011-epic-1-RWB-E1-003/specify/compliance-validation.md` |
| Agent run log | `output/INC-011-epic-1-RWB-E1-003/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-011-epic-1-RWB-E1-003/plan/` (TBC) |
| Implementation evidence | `output/INC-011-epic-1-RWB-E1-003/implement/` (TBC) |
| API / functional test reports | `output/INC-011-epic-1-RWB-E1-003/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-011-epic-1-RWB-E1-003/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-011-epic-1-RWB-E1-003/specify/compliance-validation.md`) |
| Acceptance criteria | 14 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11, AC12, AC13, AC14) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 003 ALS daily extract load v1.md` |
| Output run | `output/INC-011-epic-1-RWB-E1-003/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
