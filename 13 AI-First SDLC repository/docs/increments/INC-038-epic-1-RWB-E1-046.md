# Increment Card — INC-038-epic-1-RWB-E1-046

**RWB-E1-046 — Template and merge field catalog as data**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-038` |
| Title | Template and merge field catalog as data |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-046` |
| RUN_ID | `INC-038-epic-1-RWB-E1-046` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P6 Communications |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-012 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P6 Communications. **Build group:** P6.

## Scope

**Story:** As a **litigation officer (RW-LITOFF)**, I want **letter and document templates and their merge fields held as versioned data with the Legal approval record on each version**, so that **a template change is a data release approved by Legal and never a code release**.

**Main flow:**
1. Reference data administrator: loads the merge field catalog file through POST /admin/reference-loads with table "merge_field" and a valid from date.
2. System: checks every row: merge code unique, BR Field ID present in sys_fields, source entity and field present, required flag set. A row that fails refuses the whole load (refdata change process, step 3).
3. Reference data administrator: loads a template version file through POST /admin/reference-loads with table "template", carrying template code, language, product group, channel, notice type, signature basis, the body file reference, the merge codes used and, where Legal has signed, the approver and approval date.
4. System: reads every merge code in the body and in the merge code list and checks each one against the catalog in force. An unknown code refuses the load and names the code (MSG-P6-006).
5. System: assigns the next version number for the template code and language, keeps every earlier version readable and sets state Approved only where the approver and approval date are present, otherwise Draft.
6. System: the published interface TemplateCatalog returns, for a template code, language and date, the current version: the Approved version with the highest version number whose valid from date is on or before that date.

**Out of scope:**
- The template screen with upload, approval and withdrawal (RWB-E1-034).
- Generating notices from the templates (RWB-E1-052).
- Contract, credit approval and mortgage document generation (RWB-E2-026).
- Adding a template through the Compliance approval path (FEAT-ADM-05, Epic 8).

**Business outcome and value hypothesis:** Letters and notices are prepared by hand today, so the wording and the facts on a notice depend on who typed it. This story holds every template version, the merge fields it draws from the case and the Legal approval as data rows, so the letter engine (RWB-E1-052) can only use a version Legal approved and can only fill fields the catalog knows. It serves REQ-OCC-001 and REQ-OCC-002 and the FSD P6 measure "notices with proof of delivery, 100 percent", which needs every notice to come from a known template version (CTL-14).

**Constraints and guardrails:**
- No business value in code: template codes, languages, merge codes, field mappings and dates are read from the template and merge_field tables.
- No personal data in logs, tests or prompts. Template bodies in tests use synthetic wording; merge values never appear in logs.
- No read of another module's tables. sys_fields is read through the P4 reference data interface; the load path is P4's.
- Earlier template versions are never updated or deleted.
- A merge field marked personal_data is resolved only at generation time through the masking rules (RWB-E1-052), never stored in the template.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 046 Template and merge field catalog as data v1.md` |
| Requirement IDs | REQ-OCC-001, REQ-OCC-002 |
| BRD section | Business Requirements Epic 1, sections 3.6 and 4 |
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
| RW-REFADM, reference data administrator | Loads the catalog and template files (Reference data C) |
| RW-LEGAL, Legal counsel | Approves a template version; the approver named in the load (Documents A) |
| RW-LITOFF, litigation officer | Reads templates and the catalog (Documents R) |
| RW-COE, center of excellence analyst | Reads the catalog (Reference data R) |
| SY-CASEWF, case workflow module | Calls TemplateCatalog for the current version |

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
- **Feature flag:** `rwb.comms.template-catalog`.
- **Critical path:** No; **depends on:** RWB-E1-012.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: template codes, languages, merge codes, field mappings and dates are read from the template and merge_field tables.
  - No personal data in logs, tests or prompts. Template bodies in tests use synthetic wording; merge values never appear in logs.
  - No read of another module's tables. sys_fields is read through the P4 reference data interface; the load path is P4's.
  - Earlier template versions are never updated or deleted.
  - A merge field marked personal_data is resolved only at generation time through the masking rules (RWB-E1-052), never stored in the template.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 046 Template and merge field catalog as data v1.md` |
| Specification | `output/INC-038-epic-1-RWB-E1-046/specify/spec.md` |
| Compliance validation | `output/INC-038-epic-1-RWB-E1-046/specify/compliance-validation.md` |
| Agent run log | `output/INC-038-epic-1-RWB-E1-046/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-038-epic-1-RWB-E1-046/plan/` (TBC) |
| Implementation evidence | `output/INC-038-epic-1-RWB-E1-046/implement/` (TBC) |
| API / functional test reports | `output/INC-038-epic-1-RWB-E1-046/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-038-epic-1-RWB-E1-046/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-038-epic-1-RWB-E1-046/specify/compliance-validation.md`) |
| Acceptance criteria | 8 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 046 Template and merge field catalog as data v1.md` |
| Output run | `output/INC-038-epic-1-RWB-E1-046/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
