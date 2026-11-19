# Increment Card — INC-001-epic-1-RWB-E1-044

**RWB-E1-044 — Database migrations versioned with parameterized schema names**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-001` |
| Title | Database migrations versioned with parameterized schema names |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-044` |
| RUN_ID | `INC-001-epic-1-RWB-E1-044` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | Enabler |
| Priority | Must |
| Window | Window 1 |
| Critical path | Yes |
| Depends on | None |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P3 Case and workflow. **Build group:** P3a.

## Scope

**Story:** As a **platform administrator (RW-PLATADM)**, I want **every schema change applied by a versioned Flyway migration, one migration per story, forward-only in PROD, with the schema name taken from a parameter**, so that **the database in every environment is the sum of known migrations and nothing else**.

**Main flow:**
1. Developer: adds one migration file for the story under `recovery/src/main/resources/db/migration/recovery/`, named `V<number>__<description>.sql`, with the header line `-- Story: <story key>`.
2. Pipeline: runs the migration lint: no literal schema name, exactly one story key per file, no story key in two files, no undo file.
3. Pipeline: starts a clean PostgreSQL container and applies all migrations with `RWB_SCHEMA` set.
4. Pipeline: runs the drift check: dumps the schema object list of the clean database and of the target environment, and compares them.
5. Deployment: on service start, Flyway applies each pending migration once, in version order, and writes its checksum to the history table.
6. Deployment: Flyway validates the checksums of applied migrations; a changed file stops the start.

**Out of scope:**
- The table definitions themselves (RWB-E1-001 and each story that adds a table).
- Seed reference data (RWB-E1-043).
- Code owners and the browser test runner in the pipeline (DL37, RWB-TE-002).
- Deployment slots and release windows (DL34, DL35).

**Business outcome and value hypothesis:** The recovery tables share the ACE database with the collection module, and two squads change it from one repository (DT07, DT08). A column added by hand in one environment makes SIT and UAT test a database that PROD does not have. This story makes every change a numbered, checksummed migration with no schema name written in the file, and fails the pipeline on drift. It supports REQ-RDF-001 (the 14 data products held in the ACE database) and REQ-RDF-014 (stage 2 tables exist before the first treatment goes live). The measure is zero schema differences between a clean build and each environment at every release.

**Constraints and guardrails:**
- No business value in code or in a migration. Seed values are reference loads (RWB-E1-043), not migration inserts.
- No personal data in migrations, tests or logs. No migration copies production rows.
- No read of another module's tables. Each module owns its migrations; the recovery history table holds recovery versions only.
- No literal schema name in any migration or repository query.
- No manual change in any environment; a hotfix is a new migration through the pipeline.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 044 Database migrations versioned with parameterized schema names v1.md` |
| Requirement IDs | REQ-RDF-001, REQ-RDF-014 |
| BRD section | Business Requirements Epic 1, sections 3.3 and 4; Business Requirements Epic 2, section 4; Business Requirements Program, section 5.1 |
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
| RW-PLATADM, platform administrator | Runs deployments and reruns a failed migration job (Platform administration CRUD); reads migration runs on SCR-44 |
| RW-DATASTEW, data steward | Reads migration runs (Platform administration R) |
| RW-AUDIT, internal audit | Reads migration runs (Platform administration R) |
| Pipeline migration account | Applies migrations with the migration database account from the key store; not a Workbench role |

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
- **Feature flag:** `rwb.p3.migration-drift-gate`. On in SIT, UAT and PROD: drift fails the deployment. Off in DEV: drift is reported and the deployment continues.
- **Critical path:** Yes; **depends on:** None.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code or in a migration. Seed values are reference loads (RWB-E1-043), not migration inserts.
  - No personal data in migrations, tests or logs. No migration copies production rows.
  - No read of another module's tables. Each module owns its migrations; the recovery history table holds recovery versions only.
  - No literal schema name in any migration or repository query.
  - No manual change in any environment; a hotfix is a new migration through the pipeline.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 044 Database migrations versioned with parameterized schema names v1.md` |
| Specification | `output/INC-001-epic-1-RWB-E1-044/specify/spec.md` |
| Compliance validation | `output/INC-001-epic-1-RWB-E1-044/specify/compliance-validation.md` |
| Agent run log | `output/INC-001-epic-1-RWB-E1-044/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-001-epic-1-RWB-E1-044/plan/` (TBC) |
| Implementation evidence | `output/INC-001-epic-1-RWB-E1-044/implement/` (TBC) |
| API / functional test reports | `output/INC-001-epic-1-RWB-E1-044/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-001-epic-1-RWB-E1-044/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — cleaned against the current story on 2026-11-05; no removed ACs are mapped |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-001-epic-1-RWB-E1-044/specify/compliance-validation.md`) |
| Acceptance criteria | 0 — engineering enabler; no business ACs (see §7 note) |
| AC numbering | Not applicable — no ACs |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 044 Database migrations versioned with parameterized schema names v1.md` |
| Output run | `output/INC-001-epic-1-RWB-E1-044/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
