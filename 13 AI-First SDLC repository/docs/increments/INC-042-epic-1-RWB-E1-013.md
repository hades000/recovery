# Increment Card — INC-042-epic-1-RWB-E1-013

**RWB-E1-013 — Baseline measures**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-042` |
| Title | Baseline measures |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-013` |
| RUN_ID | `INC-042-epic-1-RWB-E1-013` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P9 Reporting |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-029, RWB-E1-018 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P9 Reporting. **Build group:** P9.

## Scope

**Story:** As the **Tribe lead (RW-TRIBE)**, I want **cases by route, age and queue, realized recovery, time in stage and turnaround per route published as the baseline, with definitions agreed by the Tribe**, so that **every later epic is measured against the same baseline**.

**Main flow:**
1. Reference data administrator: loads the measure definition file through POST /admin/reference-loads with table "measure_definition".
2. System: checks each row has a measure code, name, formula, data product, unit, approver and approval date; any failure refuses the whole load.
3. JOB-15 Reporting extract, nightly 01:30: reads the case facts of the previous business date through the P3 reporting interface and the payments since entry through the P1 interface.
4. System: computes each measure in force by its definition: counts by route, age band and queue; realized recovery; median time in stage; median turnaround per route.
5. System: writes one measure_snapshot row per measure, product and dimension value, with the definition version and business date.
6. System: on the baseline business date, marks the rows as baseline and frozen; frozen rows are never changed.

**Out of scope:**
- The steering dashboard data set, SCR-37 and the measures endpoint (RWB-E2-009).
- Queue and ageing measures for team managers (FEAT-RPT-02, RWB-E1-030).
- Benefit realisation tracking against the baseline (FEAT-RPT-06, Epic 6).
- The decision log copy to the data lake (RWB-E1-014).

**Business outcome and value hypothesis:** Measures are counted by hand from spreadsheets at month end today, and each team counts a case differently. This story holds each measure's definition, data product and formula as an approved data row, publishes the values for business date 27 November 2026 as a frozen baseline, and sends the nightly extract to the data lake for the Power BI data set. It serves REQ-RDF-012 and NFR-065 (measures from Workbench records, not a separate count), and the FSD P9 measure "measures read from the decision log and Workbench records, 100 percent".

**Constraints and guardrails:**
- No business value in code: measures, formulas, age bands and the baseline date are data or configuration.
- No personal data in logs, tests or prompts. The extract carries case IDs, codes, counts and amounts only; a field marked personal in sys_fields is never written.
- No read of another module's tables. Case and payment facts come through the P3 and P1 reporting interfaces.
- Frozen baseline rows are protected by a database trigger as well as by the service.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 013 Baseline measures v1.md` |
| Requirement IDs | REQ-RDF-012 |
| BRD section | Business Requirements Epic 1, sections 3.8 and 4 |
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
| RW-TRIBE, Tribe lead and squad members | Agrees the definitions; named as approver on each row; reads the report (Reporting R) |
| RW-REFADM, reference data administrator | Loads the definition file (Reference data C) |
| RW-BIANAL, Reporting and BI analyst | Builds the Power BI data set; reads the snapshot (Reporting CRUD) |
| RW-DATASTEW, data steward | Reads the run record and the freshness stamp (Reporting CRU) |
| RW-FINANCE, Finance and CFO delegate | Reads the baseline (Reporting R) |
| RW-PLATADM, platform administrator | Reruns JOB-15 from SCR-44 |

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
- **Feature flag:** `rwb.reporting.baseline`.
- **Critical path:** No; **depends on:** RWB-E1-029, RWB-E1-018.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: measures, formulas, age bands and the baseline date are data or configuration.
  - No personal data in logs, tests or prompts. The extract carries case IDs, codes, counts and amounts only; a field marked personal in sys_fields is never written.
  - No read of another module's tables. Case and payment facts come through the P3 and P1 reporting interfaces.
  - Frozen baseline rows are protected by a database trigger as well as by the service.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 013 Baseline measures v1.md` |
| Specification | `output/INC-042-epic-1-RWB-E1-013/specify/spec.md` |
| Compliance validation | `output/INC-042-epic-1-RWB-E1-013/specify/compliance-validation.md` |
| Agent run log | `output/INC-042-epic-1-RWB-E1-013/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-042-epic-1-RWB-E1-013/plan/` (TBC) |
| Implementation evidence | `output/INC-042-epic-1-RWB-E1-013/implement/` (TBC) |
| API / functional test reports | `output/INC-042-epic-1-RWB-E1-013/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-042-epic-1-RWB-E1-013/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — regated 2026-11-06: clarifications resolved by the D-RCV rulings; gate-002 compliance PASS |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-042-epic-1-RWB-E1-013/specify/compliance-validation.md`) |
| Acceptance criteria | 8 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 013 Baseline measures v1.md` |
| Output run | `output/INC-042-epic-1-RWB-E1-013/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
