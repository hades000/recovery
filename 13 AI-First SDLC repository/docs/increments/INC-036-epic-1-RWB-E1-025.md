# Increment Card — INC-036-epic-1-RWB-E1-025

**RWB-E1-025 — Document types and fields agreed**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-036` |
| Title | Document types and fields agreed |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-025` |
| RUN_ID | `INC-036-epic-1-RWB-E1-025` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P5 Document hub |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-012 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P5 Document hub. **Build group:** P5a.

## Scope

**Story:** As a **center of excellence analyst (RW-COE)**, I want **the first six document types (demand letter, court notice, appraisal report, title deed, settlement agreement, guarantor notice) with their key fields agreed with Legal and NPA and held as versioned reference data**, so that **the OCR pipeline, classification and extraction have one signed target list**.

**Main flow:**
1. Center of excellence analyst: prepares the list of six types and 26 fields; legal counsel and the Head of NPA review it and sign with a date.
2. Reference data administrator: uploads the file with POST /admin/reference-loads, table DOCUMENT_TYPE, validFrom 2026-11-30.
3. P4 reference load service: passes the rows to DocumentTypeLoader through the ReferenceTableLoader interface.
4. DocumentTypeLoader: validates every row: type code unique, label present, write-once flag present, retention class in LOV-RETENTION, at least one field, both sign-offs with a user ID and a date.
5. DocumentTypeLoader: on any failure refuses the load whole and returns the row errors; the version in force is unchanged.
6. DocumentTypeLoader: on success writes the rows as table version DOCTYPE-2026.11 with status LOADED, not yet in force.

**Out of scope:**
- The retention periods behind each class (RWB-E1-041; DL26).
- The checklist of required types per case type (RWB-E1-040).
- Stage 2 and 3 document types (RWB-E2-025).
- The reference data screen SCR-40 (Epic 8).

**Business outcome and value hypothesis:** Classification and extraction cannot be built or measured until the bank fixes which types are read and which fields come out of each (REQ-DCM-004, DL19). Today no signed list exists, so the model would train on a list that may change. This story turns the agreed list into a versioned table that the store (RWB-E1-024), classification (RWB-E1-050) and extraction (RWB-E1-053) read, and that changes by a data load without a code release (DT02). The measure it serves is fields extracted without review (FSD P5 A2.3.1).

**Constraints and guardrails:**
- No business value in code: type codes, fields, write-once flags and retention classes are rows in document_type.
- No personal data in logs, tests or prompts. Sign-off users in tests are synthetic IDs.
- No read of another module's tables: LOV-RETENTION is read through the P4 list service.
- A refused load writes no row.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 025 Document types and fields agreed v1.md` |
| Requirement IDs | REQ-DCM-004 |
| BRD section | Business Requirements Epic 1, section 3.5; Business Requirements Program, section 5.5 |
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
| RW-COE, center of excellence analyst | Prepares the list and reads the table |
| RW-LEGAL, legal counsel | Signs the list for Legal |
| RW-HEADNPA, Head of NPA | Signs the list for NPA |
| RW-REFADM, reference data administrator | Loads the file (Reference data C) |
| Approver with Reference data A | Approves the load. The permission matrix gives Reference data A to no role today; assumed granted to the legal counsel who owns the table (DL01) |
| SY-OCR, SY-RULES | Read the version in force |

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
- **Feature flag:** `rwb.dochub.doctypes`. Off: the table code DOCUMENT_TYPE is refused by the reference load endpoint.
- **Critical path:** No; **depends on:** RWB-E1-012.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: type codes, fields, write-once flags and retention classes are rows in document_type.
  - No personal data in logs, tests or prompts. Sign-off users in tests are synthetic IDs.
  - No read of another module's tables: LOV-RETENTION is read through the P4 list service.
  - A refused load writes no row.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 025 Document types and fields agreed v1.md` |
| Specification | `output/INC-036-epic-1-RWB-E1-025/specify/spec.md` |
| Compliance validation | `output/INC-036-epic-1-RWB-E1-025/specify/compliance-validation.md` |
| Agent run log | `output/INC-036-epic-1-RWB-E1-025/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-036-epic-1-RWB-E1-025/plan/` (TBC) |
| Implementation evidence | `output/INC-036-epic-1-RWB-E1-025/implement/` (TBC) |
| API / functional test reports | `output/INC-036-epic-1-RWB-E1-025/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-036-epic-1-RWB-E1-025/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-036-epic-1-RWB-E1-025/specify/compliance-validation.md`) |
| Acceptance criteria | 7 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 025 Document types and fields agreed v1.md` |
| Output run | `output/INC-036-epic-1-RWB-E1-025/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
