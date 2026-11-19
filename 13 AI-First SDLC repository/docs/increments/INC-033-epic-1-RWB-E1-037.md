# Increment Card — INC-033-epic-1-RWB-E1-037

**RWB-E1-037 — Role to permission matrix as data and PDPA field masking by role**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-033` |
| Title | Role to permission matrix as data and PDPA field masking by role |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-037` |
| RUN_ID | `INC-033-epic-1-RWB-E1-037` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P4 Access and administration |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | Yes |
| Depends on | RWB-E1-022, RWB-E1-043, RWB-E1-027 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P4 Access and administration. **Build group:** P4.

## Scope

**Story:** As a **product owner**, I want **the mapping of roles to capability areas, the scope of each role and the masking of each personal data field held as versioned tables that every screen and API applies**, so that **a change of rights is a data load with an approver, a person sees only the cases in their scope, and personal data shows unmasked only to roles that need it**.

**Main flow:**
1. Reference data administrator (RW-REFADM): prepares the matrix file from the approved workbook, with the application owner's approval reference in the file header, and calls POST /admin/reference-loads with table "permission" and validFrom.
2. Workbench (PermissionMatrixLoader): validates the file whole: every active role once against all 14 capability areas, letters only from C, R, U, D, A in that order or "-", known role codes; stores the rows with status Loaded and the new matrix_version.
3. Security administrator (RW-SECADM): reviews the difference report against the version in force and calls POST /admin/reference-loads/{loadId}/approve.
4. Workbench: checks that the approver holds the role the parameter names for the table and is not the person who loaded it; writes one decision log entry for the approval with decision code AC-VERS and no case; marks the version Approved with its valid from date.
5. Workbench: from the valid from date, every new session resolves the new version (RWB-E1-022 keeps open sessions on their version), and the screens and endpoints of the new letters open with no deployment.
6. Person: requests a list or a record; ScopeService builds the filter from the role's default scope (own, team, region, all) and the person's teams and regions; the owning module applies it in its query.

**Out of scope:**
- Reallocation of a leaver's or mover's open cases (RWB-E1-030 daily rebalancing; R-UNI-18 and R-UNI-19 in Epic 2).
- Administration screens SCR-43 and SCR-47 (Epic 8, FEAT-ADM-01 and FEAT-ADM-14).
- Masking values for each role and field (Compliance, DL26).
- Access per data product in the data lake copy (RWB-E1-016).
- The six-monthly access review list (JOB-18, Epic 2 control CTL-10).

**Business outcome and value hypothesis:** Audit findings record unsuitable user access to EFS and staff sending debtor data outside the bank. Today rights are set inside each system and cannot be shown for a past date. This story holds the permission matrix (54 roles against 14 capability areas), the masking rules and the scope rule as versioned data, applies scope before permission on every request, and ends access at the next request when a person leaves. It meets REQ-ACA-003, REQ-ACA-005, REQ-ACA-007, REQ-ACA-009 and REQ-ACA-011 and puts controls CTL-09, CTL-10 and CTL-11 in place. The measure is rule and limit changes made without a code release: target 100 percent (FSD P4 A2.4).

**Constraints and guardrails:**
- No business value in code: letters, scopes, masking positions, approver roles and the refresh interval are data or parameters.
- No personal data in logs, tests or prompts. Tests use tokenized synthetic values; the access event lists field IDs, never values.
- No read of another module's tables: the scope filter is applied by the owning module's repository; masking works on DTOs.
- An unmasked value is fetched only through the ACE PII service, which logs every read.
- A field with no masking rule is masked.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 037 Role to permission matrix as data and PDPA field masking by role v1.md` |
| Requirement IDs | REQ-ACA-003, REQ-ACA-005, REQ-ACA-007, REQ-ACA-009, REQ-ACA-011 |
| BRD section | Business Requirements Epic 1, section 3.4; Business Requirements Epic 2, section 3.4 (REQ-ACA-011); Business Requirements Program, section 5.4 |
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
| Application owner (level 1, assumed DL02) | Approves each permission matrix version outside the Workbench; the approval reference is carried in the load file |
| Role owners (level 2) | Request matrix changes for the roles they own |
| RW-REFADM Reference data administrator | Loads a matrix or masking version (Reference data C). Approves none |
| RW-COE Center of excellence analyst | Holds Reference data C and may load; may not approve |
| RW-SECADM Security administrator | Approves a permission or role conflict version (approver role for the table, parameter) |
| RW-COMPLY Compliance and PDPA officer | Sets the masking rules and approves each masking version (approver role for the table, parameter) |
| RW-AUDIT Internal audit | Reads every version and the approval entries; changes nothing |
| Access administrator (level 3, bank IAM) | Removes leavers and movers from Entra ID groups |
| Line manager (level 4, bank IAM) | Starts mover and leaver changes |
| Every bank role | Sees cases inside the default scope of its roles, with fields masked per the masking rules |

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
- **Feature flag:** `rwb.access.permission-matrix`.
- **Critical path:** Yes; **depends on:** RWB-E1-022, RWB-E1-043, RWB-E1-027.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: letters, scopes, masking positions, approver roles and the refresh interval are data or parameters.
  - No personal data in logs, tests or prompts. Tests use tokenized synthetic values; the access event lists field IDs, never values.
  - No read of another module's tables: the scope filter is applied by the owning module's repository; masking works on DTOs.
  - An unmasked value is fetched only through the ACE PII service, which logs every read.
  - A field with no masking rule is masked.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 037 Role to permission matrix as data and PDPA field masking by role v1.md` |
| Specification | `output/INC-033-epic-1-RWB-E1-037/specify/spec.md` |
| Compliance validation | `output/INC-033-epic-1-RWB-E1-037/specify/compliance-validation.md` |
| Agent run log | `output/INC-033-epic-1-RWB-E1-037/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-033-epic-1-RWB-E1-037/plan/` (TBC) |
| Implementation evidence | `output/INC-033-epic-1-RWB-E1-037/implement/` (TBC) |
| API / functional test reports | `output/INC-033-epic-1-RWB-E1-037/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-033-epic-1-RWB-E1-037/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-033-epic-1-RWB-E1-037/specify/compliance-validation.md`) |
| Acceptance criteria | 10 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 037 Role to permission matrix as data and PDPA field masking by role v1.md` |
| Output run | `output/INC-033-epic-1-RWB-E1-037/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
