# Increment Card — INC-015-epic-1-RWB-E1-064

**RWB-E1-064 — Data dictionary for the 14 data products**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-015` |
| Title | Data dictionary for the 14 data products |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-064` |
| RUN_ID | `INC-015-epic-1-RWB-E1-064` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | Enabler |
| Priority | Must |
| Window | Window 1 |
| Critical path | No |
| Depends on | RWB-E1-001 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P1 Recovery data engine. **Build group:** P1a.

## Scope

**Story:** As a **data steward and data product owner (RW-DATASTEW)**, I want **every field in the 14 data products typed, sourced and owned, with a data contract per source system that its owner confirms**, so that **a data contract can be agreed with the system that owns it**.

**Main flow:**
1. Reference data administrator: loads the dictionary attributes (owner role, refresh cycle, behavior when late, interface) for all 1,256 fields through POST /admin/reference-loads with table sys_fields.
2. DataDictionaryLoader: refuses the whole load if any field lacks an attribute; otherwise writes the attributes and version 1 of each field to sys_field_version.
3. DataDictionaryLoader: creates or updates one data_contract per source system in status DRAFT, naming its interfaces, listing its mapped fields.
4. Developer or analyst: calls GET /admin/data-dictionary/fields and reads a field's type, source system, source field, refresh, owner and behavior when late.
5. Data steward: sends the contract to the system owner outside the Workbench and records the owner's confirmation with PATCH /admin/data-contracts/{contractId}: confirming role, date and the stored confirmation document.
6. Data steward: publishes the contract with POST /admin/data-contracts/{contractId}/publish; the service refuses a contract without a confirmation.

**Out of scope:**
- The catalog endpoint, access by product and PDPA masking (RWB-E1-016).
- Freshness stamps per load (RWB-E1-015).
- Retention per product and table (RWB-E1-017).
- The reference data screen SCR-40 (Epic 8).
- Contracts for stage 2 data products (RWB-E2-010).

**Business outcome and value hypothesis:** The 1,256 fields of the recovery tables come from 13 source systems or from the Workbench itself, and 108 source mappings still read "To confirm with the system owner" (s2t.txt). Without a confirmed contract a source can change a field and the load breaks or loads the wrong value. This story holds the dictionary as versioned data with type, source, source field, refresh, owner and behavior when late, groups the mapped fields into one contract per source system, and lets a contract be published only after its system owner confirms it. Serves REQ-RDF-001 (one system of record and one owner per product) and REQ-RDF-011 (catalog entry content).

**Constraints and guardrails:**
- No business value in code: owners, cycles, late behavior and contract content are data rows.
- No personal data in logs, tests or prompts: the dictionary holds definitions, not values; the confirmation names a role, not a person.
- No read of another module's tables: other modules use DataDictionaryQuery.
- A published contract is never edited in place; a change makes a new version.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 064 Data dictionary for the 14 data products v1.md` |
| Requirement IDs | REQ-RDF-001, REQ-RDF-011 |
| BRD section | Business Requirements Epic 1, section 3.1 (story), section 4 (REQ-RDF-001, REQ-RDF-011) and section 5 (data dictionary sources and owners) |
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
| RW-DATASTEW, data steward | Changes field definitions, records confirmations, publishes contracts (Reference data U) |
| RW-REFADM, reference data administrator | Submits the dictionary load (Reference data C) |
| RW-COE, center of excellence analyst | Reads and changes field definitions (Reference data CRUD) |
| RW-TRIBE, RW-AUDIT and other roles with Reference data R | Read the dictionary and the contracts |
| SY-DATALOAD, data load | Applies an approved dictionary load |

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
- **Feature flag:** `rwb.dataengine.data-dictionary`.
- **Critical path:** No; **depends on:** RWB-E1-001.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: owners, cycles, late behavior and contract content are data rows.
  - No personal data in logs, tests or prompts: the dictionary holds definitions, not values; the confirmation names a role, not a person.
  - No read of another module's tables: other modules use DataDictionaryQuery.
  - A published contract is never edited in place; a change makes a new version.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 064 Data dictionary for the 14 data products v1.md` |
| Specification | `output/INC-015-epic-1-RWB-E1-064/specify/spec.md` |
| Compliance validation | `output/INC-015-epic-1-RWB-E1-064/specify/compliance-validation.md` |
| Agent run log | `output/INC-015-epic-1-RWB-E1-064/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-015-epic-1-RWB-E1-064/plan/` (TBC) |
| Implementation evidence | `output/INC-015-epic-1-RWB-E1-064/implement/` (TBC) |
| API / functional test reports | `output/INC-015-epic-1-RWB-E1-064/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-015-epic-1-RWB-E1-064/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-015-epic-1-RWB-E1-064/specify/compliance-validation.md`) |
| Acceptance criteria | 8 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 064 Data dictionary for the 14 data products v1.md` |
| Output run | `output/INC-015-epic-1-RWB-E1-064/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
