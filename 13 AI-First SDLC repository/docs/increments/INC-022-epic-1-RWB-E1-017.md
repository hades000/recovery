# Increment Card — INC-022-epic-1-RWB-E1-017

**RWB-E1-017 — Retention and archive rule for the data store**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-022` |
| Title | Retention and archive rule for the data store |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-017` |
| RUN_ID | `INC-022-epic-1-RWB-E1-017` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | User story |
| Priority | Should |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-001, RWB-E1-043, RWB-TE-012, RWB-E1-064 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P1 Recovery data engine. **Build group:** P1a.

## Scope

**Story:** As a **Compliance and PDPA officer (RW-COMPLY)**, I want **a retention rule per data product and table, held as reference data, applied by a job that archives rows past their rule and logs the action**, so that **the store holds what the policy allows and nothing older**.

**Main flow:**
1. Reference data administrator: loads a retention rule version through POST /admin/reference-loads with table retention_rule; the owner approves it.
2. RetentionRuleLoader: validates the rows (known product, known table in sys_objects, months between 1 and 600, table not decision_log_entry) and stores the version.
3. Quartz: starts JOB-17 Retention job on the first Sunday of the month.
4. RetentionService: reads the rules in force on the run date.
5. RetentionService: calls CaseHoldQuery.casesOnLegalHold() and excludes every row of those cases.
6. RetentionService: selects, per rule, the rows whose age-basis field is older than the run date minus the retention months.

**Out of scope:**
- Retention classes for documents and the document legal hold (RWB-E1-041).
- The retention class for ledger entries as its own reference row (FEAT-ILG-10, RWB-E2-034).
- The decision log retention period (NFR-030, DL26) and the lake copy (RWB-E1-014).
- Closing a case after its retention period (REQ-S7-008, Epic 6).
- The personal data screen SCR-47 (Epic 8).

**Business outcome and value hypothesis:** PDPA and the bank retention schedule limit how long personal data is kept, and today recovery records stay in spreadsheets and systems with no end date. A retention rule per data product and table, loaded as versioned data, lets Compliance set and change periods without a release. A monthly job archives rows past their period to a write-once archive container and removes them from the live store, keeps every row of a case under legal hold, and records what it did. Serves REQ-RDF-013 and the retention requirements NFR-031 and NFR-072.

**Constraints and guardrails:**
- No business value in code: periods, tables, age-basis fields and the archive location are data rows or properties.
- No personal data in logs, tests or prompts: the job run and the hold report carry counts and case numbers only; test rows are synthetic.
- No read of another module's tables: legal hold comes from CaseHoldQuery.
- The decision log is never archived or deleted by this job, and no row is deleted before its archive copy is checked.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 017 Retention and archive rule for the data store v1.md` |
| Requirement IDs | REQ-RDF-013 |
| BRD section | Business Requirements Epic 1, section 3.1 (story) and section 4 (REQ-RDF-013) |
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
| RW-COMPLY, Compliance and PDPA officer | Owns the retention periods; reads the run result (Platform administration R) |
| RW-REFADM, reference data administrator | Submits the retention load (Reference data C) |
| Holder of Reference data A | Approves the retention load |
| RW-DATASTEW, data steward | Reads the run result for their products |
| RW-PLATADM, platform administrator | Reruns JOB-17 (Platform administration U) |
| SY-DATALOAD, data load | Runs JOB-17, writes the archive, deletes archived rows |
| SY-CASEWF, case workflow module | Answers CaseHoldQuery |

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
- **Feature flag:** `rwb.dataengine.retention`.
- **Critical path:** No; **depends on:** RWB-E1-001, RWB-E1-043, RWB-TE-012, RWB-E1-064.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: periods, tables, age-basis fields and the archive location are data rows or properties.
  - No personal data in logs, tests or prompts: the job run and the hold report carry counts and case numbers only; test rows are synthetic.
  - No read of another module's tables: legal hold comes from CaseHoldQuery.
  - The decision log is never archived or deleted by this job, and no row is deleted before its archive copy is checked.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 017 Retention and archive rule for the data store v1.md` |
| Specification | `output/INC-022-epic-1-RWB-E1-017/specify/spec.md` |
| Compliance validation | `output/INC-022-epic-1-RWB-E1-017/specify/compliance-validation.md` |
| Agent run log | `output/INC-022-epic-1-RWB-E1-017/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-022-epic-1-RWB-E1-017/plan/` (TBC) |
| Implementation evidence | `output/INC-022-epic-1-RWB-E1-017/implement/` (TBC) |
| API / functional test reports | `output/INC-022-epic-1-RWB-E1-017/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-022-epic-1-RWB-E1-017/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-022-epic-1-RWB-E1-017/specify/compliance-validation.md`) |
| Acceptance criteria | 9 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 017 Retention and archive rule for the data store v1.md` |
| Output run | `output/INC-022-epic-1-RWB-E1-017/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
