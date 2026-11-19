# Increment Card — INC-001-epic-1-RWB-E1-044

**RWB-E1-044 — Database migrations versioned with parameterized schema names**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-001` |
| Title | Database migrations versioned with parameterized schema names |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-044` |
| RUN_ID | `INC-001-epic-1-RWB-E1-044` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | Enabler |
| Priority | Must |
| Build order | 1 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | None |
| Blocks | See the build sequence |
| Status | Planned — plan carried from the 10 Nov 2026 run; schema basis reverted to `recovery` by D-RCV-35; re-plan before build |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P3 Case and workflow.

## Scope

**Story:** As a **platform administrator (RW-PLATADM)**, I want **every schema change applied by a versioned Flyway migration, one migration per story, forward-only in PROD, with the schema name taken from a parameter**, so that **the database in every environment is the sum of known migrations and nothing else**.

**Business outcome:** The recovery tables share the ACE database with the collection module, and two squads change it from one repository (DT07, DT08). A column added by hand in one environment makes SIT and UAT test a database that PROD does not have. This story makes every change a numbered, checksummed migration with no schema name written in the file, and fails the pipeline on drift. It supports REQ-RDF-001 (the 14 data products held in the ACE database) and REQ-RDF-014 (stage 2 tables exist before the first treatment goes live). The measure is zero schema differences between a clean build and each environment at every release.

**Main flow:**
1. Developer: adds one migration file for the story under `recovery/src/main/resources/db/migration/recovery/`, named `V<number>__<description>.sql`, with the header line `-- Story: <story key>`.
2. Pipeline: runs the migration lint: no literal schema name, no foreign key into `public`, exactly one story key per file, no story key in two files, no undo file.
3. Pipeline: starts a clean PostgreSQL container and applies all migrations with `RWB_SCHEMA` set.
4. Pipeline: runs the drift check: dumps the schema object list of the clean database and of the target environment, and compares them.
5. Deployment: on service start, Flyway applies each pending migration once, in version order, and writes its checksum to the history table.
6. Deployment: Flyway validates the checksums of applied migrations; a changed file stops the start.

**Acceptance criteria:**
- AC1: Migration applied
- AC2: Drift detected
- AC3: Schema name as parameter
- AC4: Applied migration edited
- AC5: Literal schema name
- AC6: One migration per story
- AC7: Forward only in PROD
- AC8: Migration fails part way
- AC9: Two instances start together

**Out of scope:**
- The table definitions themselves (RWB-E1-001 and each story that adds a table).
- Seed reference data (RWB-E1-043).
- Code owners and the browser test runner in the pipeline (DL37, RWB-TE-002).
- Deployment slots and release windows (DL34, DL35).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-044-database-migrations-versioned-with-parameterized-schema-names-v1.md` |
| Requirement IDs | REQ-RDF-001, REQ-RDF-014 |
| BRD section | Business Requirements Epic 1, sections 3.3 and 4; Business Requirements Epic 2, section 4; Business Requirements Program, section 5.1 |
| Decision | None |
| Epic card | `epics/EPIC-001-foundation-1.md` |
| Lifecycle tailoring | `epics/EPIC-001-tailoring.md` |
| Module FSD / PRD | `docs/prds/` |
| Module TSD | `requirement/legacy/05-technical-architecture/` |
| API specification | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v4.yaml` |
| Physical schema | `requirement/legacy/06-data/recovery-workbench-physical-schema-v6.sql` |
| Engineering practices | `AGENTS.md` |

## Lifecycle tailoring

Shared record: `epics/EPIC-001-tailoring.md`. The phase classification is epic-level; this card records the story-specific agents and evidence.

## Story authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM, platform administrator | Runs deployments and reruns a failed migration job (Platform administration CRUD); reads migration runs on SCR-44 |
| RW-DATASTEW, data steward | Reads migration runs (Platform administration R) |
| RW-AUDIT, internal audit | Reads migration runs (Platform administration R) |
| Pipeline migration account | Applies migrations with the migration database account from the key store; not a Workbench role |

## Contract extract

**GET /api/recovery/v1/admin/jobs** (P1 endpoint) lists migration runs with `type=MIGRATION`. | Item | Value | |---|---| | Request | Query `type` = MIGRATION, `status`, `from`, `to` | | Response | 200 `Job[]`: `id`, `type`, `businessDate`, `status` (APPLIED, FAILED), `startedAt`, `endedAt`, `checks` (version, checksum, drift result) | | Errors | 401 (MSG-P4-001); 403 no Platform administration R (MSG-P4-002); 503 | | Authorization | Platform administration, right R | | Idempotency | Not applicable | **Migration job** | Item | Value | |---|---| | Trigger | Service start in each environment, and the pipeline step `migrate` | | Job name | Not a scheduled job in batch.txt; it runs at deployment | | Input | The files in `db/migration/recovery`, `RWB_SCHEMA`, the migration account | | Output | Applied objects in schema `RWB_SCHEMA`; rows in `flyway_schema_history_recovery`; one `Job` record p…

## Owners and approvals

| Gate | Accountable role | Name | Decision / date |
|---|---|---|---|
| Requirements approval | Product Owner | Chitchaya Muanchonchana | Source story set v7/v6, 16 Nov 2026 |
| Context readiness | Forward Deployed Engineer | Jesniphat Pukkham | CONTEXT-20261116 |
| Plan approval | Forward Deployed Architect | Jesniphat Pukkham | Per-story plan gate |
| Pull request approval | Forward Deployed Engineer | Recovery tech lead | Per MR |

## Agents selected

| Lifecycle group | Agent | Applicable / Optional / Not used | Reason |
|---|---|---|---|
| Requirements and discovery | Context Builder / Updater | Applicable | Context package CONTEXT-20261116. |
| Design, backlog and spec | Technical Specifier | Applicable | Produces the implementation-ready spec. |
| Plan and build | Implementation Planner | Applicable | Produces `plan.md` and `tasks.md`. |
| Plan and build | Implementation Builder | Applicable | Builds the approved plan in ACE. |
| Quality and release | Compliance Reviewer | Applicable | Spec, plan and code gates. |
| Quality and release | API Tester | Per API scope | Driven by the spec. |
| Quality and release | Functional Automation Test | Per UI scope | Driven by the spec. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Stop signals:** any guardrail in story §17; a migration that is not `V<seq>__<story>_<name>.sql`; a direct read of an ACE table outside `recovery.v_ace_*`.

**Guardrails:**

- No business value in code or in a migration. Seed values are reference loads (RWB-E1-043), not migration inserts. - No personal data in migrations, tests or logs. No migration copies production rows. - No read of another module's tables. Each module owns its migrations; the recovery history table holds recovery versions only. - No literal schema name in any migration or repository query. - No migration declares a foreign key into `public`; the recovery schema holds ACE business keys and the views read ACE. - No manual change in any environment; a hotfix is a new migration through the pipeline.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-044-database-migrations-versioned-with-parameterized-schema-names-v1.md` |
| Specification | `output/INC-001-epic-1-RWB-E1-044/specify/spec.md` |
| Compliance validation | `output/INC-001-epic-1-RWB-E1-044/specify/compliance-validation.md` |
| Agent run log | `output/INC-001-epic-1-RWB-E1-044/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-001-epic-1-RWB-E1-044/plan/` |
| Implementation evidence | `output/INC-001-epic-1-RWB-E1-044/implement/` |
| API / functional test reports | `output/INC-001-epic-1-RWB-E1-044/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-001-epic-1-RWB-E1-044/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Planned — plan carried from the 10 Nov 2026 run; schema basis reverted to `recovery` by D-RCV-35; re-plan before build |
| Specification | SUCCESS — 10 Nov 2026, needs re-baseline for D-RCV-35 |
| Compliance review | PASS (2026-11-10) |
| Acceptance criteria | 9 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation | Spec and plan carried from `INC-001 (10 November 2026 run)`; not built. |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-044-database-migrations-versioned-with-parameterized-schema-names-v1.md` |
| Output run | `output/INC-001-epic-1-RWB-E1-044/` |

