# Increment Card — INC-059-epic-1-RWB-E1-011

**RWB-E1-011 — Reconciliation and data quality report**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-059` |
| Title | Reconciliation and data quality report |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-011` |
| RUN_ID | `INC-059-epic-1-RWB-E1-011` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-002, RWB-E1-006 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P1 Recovery data engine. **Build group:** P1b.

## Scope

**Story:** As a **team manager (RW-TEAMMGR)**, I want **a daily reconciliation of the case list to ALS, with the variance by product and the data quality results in one Power BI report**, so that **everyone sees whether today's case list can be trusted**.

**Main flow:**
1. System: JOB-04 Daily reconciliation runs its reconciliation step after the case list step for the business date.
2. System: checks through `LoadRunQuery` that the INT-01 load for the business date is COMPLETED.
3. System: for each product group, counts the ALS accounts at or above 90 days past due less the accounts excluded at entry, and the case list rows at or above 90 days past due (REC-01).
4. System: for each product group, sums total_balance on both sides (REC-02).
5. System: computes the variance and the variance percent and compares it with the tolerance; writes one reconciliation_result per reconciliation and product.
6. System: writes one dq_exception per account that breaks, with check code REC-01 and the account number: in ALS and not on the case list, or on the case list and not in ALS.

**Out of scope:**
- Working a break to closure with an owner and a date, and releasing a held publish by hand (FEAT-RPT-09 full scope, Epic 2).
- Reconciliation of treatments, payments, notices, write-offs and assets (REC-03 to REC-07, later epics).
- The decision log copy check (REC-08, RWB-E1-014).
- Cross-source case count reconciliation in the reporting module (FEAT-RPT-05 full scope, Epic 2).

**Business outcome and value hypothesis:** No one can say today whether the recovery teams' lists cover every account at 90 days past due, so missing accounts are found late or not at all. This story runs the reconciliations REC-01 (account count by product) and REC-02 (balance by product) every working day, lists every account that breaks, holds the publish of the case list when a product is outside the tolerance, and publishes the result with the data quality results in one report. It meets REQ-RDF-007 and REQ-RDF-008, applies control CTL-01, and serves the accuracy measure "reconciliation breaks cleared within one day, 100 percent".

**Constraints and guardrails:**
- No business value in code: the tolerance and the threshold are parameters.
- No personal data in logs, tests or prompts. Break rows carry account numbers only.
- No read of another module's tables. Exclusions come through `CaseQueryApi`; open case accounts come from case_list_row.
- A held case list is never published by hand from this story.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 011 Reconciliation and data quality report v1.md` |
| Requirement IDs | REQ-RDF-007, REQ-RDF-008 |
| BRD section | Business Requirements Epic 1, sections 3.1 and 3.8; Business Requirements Program, section 5.1 |
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
| SY-DATALOAD, data load from COLLINS | Runs the reconciliation; writes reconciliation_result, dq_exception and the publish status |
| RW-DATASTEW, data steward and data product owner | Reads results and break rows (Platform administration R); signs the daily reconciliation to ALS |
| RW-PLATADM, platform administrator | Reads results; reruns the step (Platform administration U) |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-SECADM | Read results and break rows (Platform administration R) |
| RW-TEAMMGR, RW-BIANAL and other report readers | Read the Power BI report (Reporting R); RW-BIANAL builds it (Reporting CRUD) |

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
- **Feature flag:** `rwb.p1.reconciliation`. Off: the case list publishes as in RWB-E1-002 with its count check.
- **Critical path:** No; **depends on:** RWB-E1-002, RWB-E1-006.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: the tolerance and the threshold are parameters.
  - No personal data in logs, tests or prompts. Break rows carry account numbers only.
  - No read of another module's tables. Exclusions come through `CaseQueryApi`; open case accounts come from case_list_row.
  - A held case list is never published by hand from this story.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 011 Reconciliation and data quality report v1.md` |
| Specification | `output/INC-059-epic-1-RWB-E1-011/specify/spec.md` |
| Compliance validation | `output/INC-059-epic-1-RWB-E1-011/specify/compliance-validation.md` |
| Agent run log | `output/INC-059-epic-1-RWB-E1-011/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-059-epic-1-RWB-E1-011/plan/` (TBC) |
| Implementation evidence | `output/INC-059-epic-1-RWB-E1-011/implement/` (TBC) |
| API / functional test reports | `output/INC-059-epic-1-RWB-E1-011/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-059-epic-1-RWB-E1-011/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-059-epic-1-RWB-E1-011/specify/compliance-validation.md`) |
| Acceptance criteria | 6 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 011 Reconciliation and data quality report v1.md` |
| Output run | `output/INC-059-epic-1-RWB-E1-011/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
