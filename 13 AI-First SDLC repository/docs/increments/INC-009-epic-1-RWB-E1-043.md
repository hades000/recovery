# Increment Card — INC-009-epic-1-RWB-E1-043

**RWB-E1-043 — Reference data service with versioned tables**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-009` |
| Title | Reference data service with versioned tables |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-043` |
| RUN_ID | `INC-009-epic-1-RWB-E1-043` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | Enabler |
| Priority | Must |
| Window | Window 1 |
| Critical path | Yes |
| Depends on | RWB-E1-042, RWB-E1-044 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P3 Case and workflow. **Build group:** P3a.

## Scope

**Story:** As a **reference data administrator (RW-REFADM)**, I want **products, regions, exposure bands, roles, teams, queues, service levels, document types, templates, delegation of authority, legal periods and holidays held as versioned reference data with valid from, valid to, author and approver**, so that **business values change by a data release and not by code, and every engine can say which version it used**.

**Main flow:**
1. Reference data administrator: uploads a load file for one table code with a valid from date through `POST /admin/reference-loads`.
2. P4 load handler: passes the file rows, the table code, the valid from date and the caller's user ID to `ReferenceVersionRegistry.recordVersion(...)`.
3. Reference data service: checks the table code, the row schema for that table, the row keys, the valid from date and the author; computes the content hash and the next version number.
4. Reference data service: writes one `reference_version` row with status VALIDATED and one `reference_row` row per file row, in one transaction.
5. Approver: approves the load through `POST /admin/reference-loads/{loadId}/approve`.
6. Reference data service: checks that the approver is present, is not the author and holds the approve right; sets status APPROVED, `approver_user_id` and `approved_at`.

**Out of scope:**
- The rule table load, validation and rollback for the five rule tables (RWB-E1-029).
- The permission matrix and masking tables (RWB-E1-037) and the delegation of authority content (RWB-E1-038).
- The checklist fields and the rule change audit report (RWB-E1-048).
- Product parameter completeness checks (RWB-E1-045).
- Reference data screens SCR-39, SCR-40 and SCR-42 (Epic 8).

**Business outcome and value hypothesis:** Today the values that drive allocation, timers and approval limits live in team spreadsheets and in procedure documents, so nobody can say which value applied to a case on a given day. This story gives every reference table a version with a valid from date, an author and a different approver, and serves the version in force to the engines. It meets REQ-DRI-011 and REQ-CWC-006 and supports control CTL-08 (a rule, limit or list changes only through a validated load approved by its owner). The measure is that every value an engine reads carries a table code and a version number in its log line.

**Constraints and guardrails:**
- No business value in code. Table codes, columns, bands, periods and limits are rows; the code holds only the versioning behavior.
- No personal data in logs, tests or prompts. Log lines carry table codes and version numbers only. Test files use synthetic codes.
- No read of another module's tables. `lov_value` is read through the P4 published interface; P4 reaches the registry only through `ReferenceVersionRegistry`.
- A version row is never updated in place except for its status, approver and valid to; a correction is a new version.
- The cache never serves a version that is not APPROVED.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 043 Reference data service with versioned tables v1.md` |
| Requirement IDs | REQ-DRI-011, REQ-CWC-006 |
| BRD section | Business Requirements Epic 1, sections 3.3 and 4; Business Requirements Program, sections 5.3 and 5.7 |
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
| RW-REFADM, reference data administrator | Loads a version (Reference data C). Reads versions (R) |
| RW-COE, center of excellence analyst | Loads a version of the tables it owns (Reference data C) |
| RW-RISK, risk and model risk officer | Approves a version. Assumed: RW-RISK holds the approve right in Reference data, because no role holds it in the permission matrix today. The permission matrix change is loaded through RWB-E1-037; holders by name follow DL18 |
| SY-CASEWF, case workflow module | Reads the version in force (Reference data R) |
| SY-RULES, rules component | Reads the version in force (Reference data R) |
| RW-AUDIT, internal audit | Reads versions and their author and approver (Reference data R) |

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
| Quality and release | Functional Automation Test | Not used | UI is not in scope. |
| Quality and release | Azure Deploy pipeline | Not used | ACE uses its own pipeline. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Feature flag:** `rwb.p3.refdata-versions`. Off: the engines read the reference values loaded before this story.
- **Critical path:** Yes; **depends on:** RWB-E1-042, RWB-E1-044.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code. Table codes, columns, bands, periods and limits are rows; the code holds only the versioning behavior.
  - No personal data in logs, tests or prompts. Log lines carry table codes and version numbers only. Test files use synthetic codes.
  - No read of another module's tables. `lov_value` is read through the P4 published interface; P4 reaches the registry only through `ReferenceVersionRegistry`.
  - A version row is never updated in place except for its status, approver and valid to; a correction is a new version.
  - The cache never serves a version that is not APPROVED.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 043 Reference data service with versioned tables v1.md` |
| Specification | `output/INC-009-epic-1-RWB-E1-043/specify/spec.md` |
| Compliance validation | `output/INC-009-epic-1-RWB-E1-043/specify/compliance-validation.md` |
| Agent run log | `output/INC-009-epic-1-RWB-E1-043/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-009-epic-1-RWB-E1-043/plan/` (TBC) |
| Implementation evidence | `output/INC-009-epic-1-RWB-E1-043/implement/` (TBC) |
| API / functional test reports | `output/INC-009-epic-1-RWB-E1-043/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-009-epic-1-RWB-E1-043/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-009-epic-1-RWB-E1-043/specify/compliance-validation.md`) |
| Acceptance criteria | 10 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 043 Reference data service with versioned tables v1.md` |
| Output run | `output/INC-009-epic-1-RWB-E1-043/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
