# Increment Card — INC-067-epic-1-RWB-E1-009

**RWB-E1-009 — CCMS and SVAF loads**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-067` |
| Title | CCMS and SVAF loads |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-009` |
| RUN_ID | `INC-067-epic-1-RWB-E1-009` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-003, RWB-E1-015, RWB-E1-007 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P1 Recovery data engine. **Build group:** P1b.

## Scope

**Story:** As a **data steward and data product owner (RW-DATASTEW)**, I want **collateral records from CCMS and appraisals from SVAF loaded from their weekly files and linked to the loan accounts**, so that **the collateral and asset data product DP06 is current without anyone looking the values up in CCMS or SVAF**.

**Main flow:**
1. File adapter (P2): JOB-09 receives the CCMS file for the week, passes its file checks, and calls `CcmsCollateralLoader.load("INT-10", businessDate, records)`.
2. System: opens a load_run for INT-10 with the interface_run reference.
3. System: runs DQ-061 references (each account link matches loan_account) and DQ-062 lists of values; above 0.50 percent the file is refused.
4. System: upserts collateral by collateral_no and replaces the account_collateral links of each loaded collateral, in one transaction.
5. System: runs DQ-063 movement, calls `FreshnessStampService.recordLoad` for DP06, sets COMPLETED, publishes LoadCompleted and returns the LoadOutcome to the adapter.
6. File adapter (P2): after INT-10, calls `SvafAppraisalLoader.load("INT-11", businessDate, records)` for the SVAF file.

**Out of scope:**
- Receiving the files and the file checks (RWB-E1-007).
- Ordering a new appraisal when the last one is stale (FEAT-VAL-01, Epic 4).
- Valuer identity from the partner panel (S9, Epic 2).
- AMIS and RPS asset loads (INT-12, INT-13, Epic 3).
- Same-day collateral or appraisal data (DL06).
- Encumbrance and occupancy updates by the Workbench (S5).

**Business outcome and value hypothesis:** Case owners and sale officers look up collateral and appraisal values in CCMS and SVAF by hand today, and the appraisal used for a decision is often more than a year old without anyone seeing it. This story loads the weekly CCMS (INT-10) and SVAF (INT-11) files that the file adapters receive and check, links each collateral to its accounts, and flags every appraisal older than the age limit at load. It meets REQ-RDF-004 and supports control CTL-27 (an asset is priced only on an appraisal inside its age limit).

**Constraints and guardrails:**
- No business value in code: the age limit and tolerances are parameters; mappings and code maps are data.
- No personal data in logs, tests or prompts. Title deed and plot numbers appear only in synthetic test files.
- No read of another module's tables. valuation is written only through ValuationRecordApi; the adapter's tables are not read.
- The load never overwrites occupancy or encumbrance_status, which the Workbench owns.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 009 CCMS and SVAF loads v1.md` |
| Requirement IDs | REQ-RDF-004 |
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
| SY-DATALOAD, data load from COLLINS | Runs the loaders; writes collateral, account_collateral, load_run and dq_exception; calls ValuationRecordApi (Asset and disposal CU) |
| RW-PLATADM, platform administrator | Lists runs (Platform administration R); reruns a refused or failed load (Platform administration U) |
| RW-DATASTEW, RW-COE, RW-AUDIT, RW-COMPLY, RW-SECADM | List runs (Platform administration R) |

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
- **Feature flag:** `rwb.p1.collateral-load`. Off: the loaders return status SKIPPED and write nothing.
- **Critical path:** No; **depends on:** RWB-E1-003, RWB-E1-015, RWB-E1-007.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: the age limit and tolerances are parameters; mappings and code maps are data.
  - No personal data in logs, tests or prompts. Title deed and plot numbers appear only in synthetic test files.
  - No read of another module's tables. valuation is written only through ValuationRecordApi; the adapter's tables are not read.
  - The load never overwrites occupancy or encumbrance_status, which the Workbench owns.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 009 CCMS and SVAF loads v1.md` |
| Specification | `output/INC-067-epic-1-RWB-E1-009/specify/spec.md` |
| Compliance validation | `output/INC-067-epic-1-RWB-E1-009/specify/compliance-validation.md` |
| Agent run log | `output/INC-067-epic-1-RWB-E1-009/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-067-epic-1-RWB-E1-009/plan/` (TBC) |
| Implementation evidence | `output/INC-067-epic-1-RWB-E1-009/implement/` (TBC) |
| API / functional test reports | `output/INC-067-epic-1-RWB-E1-009/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-067-epic-1-RWB-E1-009/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-067-epic-1-RWB-E1-009/specify/compliance-validation.md`) |
| Acceptance criteria | 11 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 009 CCMS and SVAF loads v1.md` |
| Output run | `output/INC-067-epic-1-RWB-E1-009/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
