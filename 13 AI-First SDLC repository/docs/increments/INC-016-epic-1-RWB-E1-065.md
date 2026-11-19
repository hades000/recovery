# Increment Card — INC-016-epic-1-RWB-E1-065

**RWB-E1-065 — Sandbox database with synthetic recovery data**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-016` |
| Title | Sandbox database with synthetic recovery data |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-065` |
| RUN_ID | `INC-016-epic-1-RWB-E1-065` |
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

**Story:** As a **Tribe lead and squad member (RW-TRIBE)**, I want **a sandbox database holding synthetic recovery data**, so that **I can build and test before the real interfaces are available**.

**Main flow:**
1. Pipeline: on a merge to main that changes a recovery Flyway migration, or on a manual start, runs the sandbox build stage in DEV.
2. Pipeline: drops and recreates schema `recovery` in `rwb_sandbox` and applies every Flyway migration.
3. SandboxGenerator: reads sys_objects, sys_fields and lov_value from the sandbox to learn every table, column, type and list.
4. SandboxGenerator: creates synthetic cases with seed 20261128: 1,226 Mortgage, 1,296 Hire purchase and 290 SSME (10 percent of the 30 June 2026 inventory; DL15), with their accounts, parties, contact points, collateral, valuations, payments and interactions.
5. SandboxGenerator: adds 10 cases for each exception shape in section 8, BR4.
6. SandboxGenerator: loads the 54 roles, the permission matrix and one named test user per role.

**Out of scope:**
- Masked copies of production data in SIT and UAT (RWB-TE-004).
- The rule table test harness (RWB-TE-005) and the performance test harness (RWB-TE-009).
- The PDPA lint for code, tests and logs (RWB-TE-011).
- Real loads from COLLINS and the file interfaces (RWB-E1-003, RWB-E1-004, RWB-E1-007).

**Business outcome and value hypothesis:** The COLLINS loads, the file loads and the masked SIT copy are not available when the squads start on 2 November, and NFR-045 forbids production data in development. A sandbox in DEV built from the same Flyway migrations as the recovery schema, filled by a seeded generator with synthetic cases across Mortgage, Hire Purchase and SSME and the exception shapes the rules must handle, lets every squad build and test from the first day. The generator reads the data dictionary, so a schema change reaches the sandbox with no manual rebuild. Serves REQ-RDF-001 (the 14 data products in one schema) and REQ-RDF-010 (no personal data outside its permitted use).

**Constraints and guardrails:**
- No business value in code: volumes, seed and shape counts are properties; values come from the dictionary and the lists.
- No personal data in logs, tests or prompts: every name, identifier and contact value is synthetic, and the verifier blocks values that look real.
- No read of another module's tables at runtime: the generator is a build tool outside the ACE service and is never deployed to SIT, UAT or production.
- The sandbox is in DEV only; no copy goes to another environment.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 065 Sandbox database with synthetic recovery data v1.md` |
| Requirement IDs | REQ-RDF-001, REQ-RDF-010 |
| BRD section | Business Requirements Epic 1, section 3.1 (story) and section 4 (REQ-RDF-001, REQ-RDF-010); Business Requirements Program, section 6.7 (NFR-045) |
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
| RW-TRIBE, Tribe lead and squad members | Read and extract the sandbox through role `rwb_sandbox_read`; start a manual build |
| RW-PLATADM, platform administrator | Owns the sandbox database and the pipeline stage |
| Test users per role | Call the DEV service against the sandbox with their role's rights |

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
- **Feature flag:** `rwb.dataengine.sandbox` (enables the DEV profile that points the service at `rwb_sandbox`).
- **Critical path:** No; **depends on:** RWB-E1-001.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: volumes, seed and shape counts are properties; values come from the dictionary and the lists.
  - No personal data in logs, tests or prompts: every name, identifier and contact value is synthetic, and the verifier blocks values that look real.
  - No read of another module's tables at runtime: the generator is a build tool outside the ACE service and is never deployed to SIT, UAT or production.
  - The sandbox is in DEV only; no copy goes to another environment.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 065 Sandbox database with synthetic recovery data v1.md` |
| Specification | `output/INC-016-epic-1-RWB-E1-065/specify/spec.md` |
| Compliance validation | `output/INC-016-epic-1-RWB-E1-065/specify/compliance-validation.md` |
| Agent run log | `output/INC-016-epic-1-RWB-E1-065/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-016-epic-1-RWB-E1-065/plan/` (TBC) |
| Implementation evidence | `output/INC-016-epic-1-RWB-E1-065/implement/` (TBC) |
| API / functional test reports | `output/INC-016-epic-1-RWB-E1-065/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-016-epic-1-RWB-E1-065/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — cleaned against the current story on 2026-11-05; no removed ACs are mapped |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-016-epic-1-RWB-E1-065/specify/compliance-validation.md`) |
| Acceptance criteria | 0 — engineering enabler; no business ACs (see §7 note) |
| AC numbering | Not applicable — no ACs |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 065 Sandbox database with synthetic recovery data v1.md` |
| Output run | `output/INC-016-epic-1-RWB-E1-065/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
