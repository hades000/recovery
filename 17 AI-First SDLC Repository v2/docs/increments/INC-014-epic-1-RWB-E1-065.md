# Increment Card — INC-014-epic-1-RWB-E1-065

**RWB-E1-065 — Sandbox database with synthetic recovery data**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-014` |
| Title | Sandbox database with synthetic recovery data |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-065` |
| RUN_ID | `INC-014-epic-1-RWB-E1-065` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | Enabler |
| Priority | Must |
| Build order | 14 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-001, RWB-E1-069 |
| Blocks | See the build sequence |
| Status | Ready for specify |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P1 Recovery data engine.

## Scope

**Story:** As a **Tribe lead and squad member (RW-TRIBE)**, I want **a sandbox database that stands up the ACE schema and the recovery schema from the same DDL as SIT, with synthetic ACE-shaped source rows and synthetic Workbench rows**, so that **I can build and test every view read before the ACE interfaces are available and without production data**.

**Business outcome:** SIT reads the real ACE database; DEV has none. Without a local ACE schema the 30 `recovery.v_ace_*` views cannot compile, so no squad can test a source read, the case list, a notice or a report before SIT is connected. The sandbox applies the ACE schema for the 22 Tier 1 tables, the RWB-ACE-001 DDL for the 14 Tier 2 tables, Physical Schema v6 for the 92 recovery tables and the four extension tables, and V0002 and V0003 for the 30 views. It fills the source tables with synthetic rows and the Workbench tables with synthetic cases across Mortgage, Hire Purchase and SSME, and the exception shapes the rules must handle.

**Main flow:**
1. Pipeline: on a merge to main that changes the ACE schema DDL, a recovery Flyway migration or the dictionary, or on a manual start, runs the sandbox build stage in DEV.
2. Pipeline: creates database `rwb_sandbox_next` and two empty schemas, `public` and `recovery`.
3. Pipeline: applies `ACE Schema PostgreSQL v1.sql` (22 Tier 1 tables), then the RWB-ACE-001 DDL (14 Tier 2 tables), then V0001 (92 tables and the dictionary), V0002 (16 Section A views) and V0003 (14 Section B views).
4. SandboxGenerator: reads `sys_objects`, `sys_fields` and `lov_value` to learn every table, column, type and list.
5. SandboxGenerator: seeds the 22 Tier 1 tables and the 14 Tier 2 tables with synthetic rows, including one `ace_batch_run` row per source and business date.
6. SandboxGenerator: creates synthetic cases with seed 20261128: 1,226 Mortgage, 1,296 Hire purchase and 290 SSME (10 percent of the 30 June 2026 inventory; DL15), with their accounts, parties, contact points, collateral, valuations, payments and interactions, linked by business key to the ACE-shaped rows.

**Acceptance criteria:**
- AC1: The sandbox exists
- AC2: It is readable and extractable
- AC3: It scales with the schema
- AC4: A column with no dictionary entry
- AC5: The reset is idempotent
- AC6: A generated value breaks a constraint
- AC7: No clear personal value outside the ACE tables
- AC8: Accounts at the entry boundary
- AC9: Two builds at once

**Out of scope:**
- Masked copies of production data in SIT and UAT (RWB-TE-004).
- The rule scenario build gate (RWB-E1-073) and the performance test harness (RWB-TE-009).
- The PDPA lint for code, tests and logs (RWB-TE-011).
- The ACE ingestion itself and the 14 Tier 2 tables: the ACE team owns them in RWB-ACE-001.
- The 30 views, their grants and the view conformance test: RWB-E1-069.
- The dictionary content and its change process: RWB-E1-064.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-065-sandbox-database-with-synthetic-recovery-data-v1.md` |
| Requirement IDs | REQ-RDF-001, REQ-RDF-010 |
| BRD section | Business Requirements Epic 1, section 3.1 (story) and section 4 (REQ-RDF-001, REQ-RDF-010); Business Requirements Program, section 6.7 (NFR-045) |
| Decision | D-RCV-35 (U1, U4); ADR-010; DL43 |
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
| RW-TRIBE, Tribe lead and squad members | Read and extract the sandbox through role `rwb_sandbox_read`; start a manual build |
| RW-PLATADM, platform administrator | Owns the sandbox database and the pipeline stage |
| Test users per role | Call the DEV service against the sandbox with their role's rights |
| ACE team lead and ACE DBA | Own the ACE schema DDL used as the test double and the Tier 2 DDL of RWB-ACE-001; approve a change to either |

## Contract extract

**Pipeline stage** | Item | Value | |---|---| | Trigger | Merge to main that changes the ACE schema DDL, a file under the recovery Flyway migration folder or the dictionary; manual start by RW-TRIBE or RW-PLATADM | | Job name | Sandbox build, a DEV pipeline stage; not a scheduled job and not in `job_catalog` | | Schedule | On trigger only | | Input | `ACE Schema PostgreSQL v1.sql`; the RWB-ACE-001 Tier 2 DDL; V0001, V0002 and V0003; `sys_objects`, `sys_fields` and `lov_value` after migration; the role and permission seed file; properties in section 13 | | Output | Database `rwb_sandbox` with schema `public` (the ACE schema, including the 22 Tier 1 and 14 Tier 2 tables) and schema `recovery` (92 tables and 30 views) holding synthetic rows; build report with row count per table and the verifier result | | Events published | None | | Idempotency key | Commit hash and seed. The same pair pr…

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

- No business value in code: volumes, seed and shape counts are properties; values come from the dictionary and the lists. - No personal data in logs, tests or prompts: every name, identifier and contact value is synthetic, and the verifier blocks a value that looks real in schema recovery. - No read of another module's tables at runtime: the generator is a build tool outside the ACE service and is never deployed to SIT, UAT or production. - The sandbox is in DEV only; no copy goes to another environment. The ACE-shaped tables are a test double, not a data copy. - No copy and no load table is created: the Workbench reads source data only through `recovery.v_ace_*`.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-065-sandbox-database-with-synthetic-recovery-data-v1.md` |
| Specification | `output/INC-014-epic-1-RWB-E1-065/specify/spec.md` |
| Compliance validation | `output/INC-014-epic-1-RWB-E1-065/specify/compliance-validation.md` |
| Agent run log | `output/INC-014-epic-1-RWB-E1-065/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-014-epic-1-RWB-E1-065/plan/` |
| Implementation evidence | `output/INC-014-epic-1-RWB-E1-065/implement/` |
| API / functional test reports | `output/INC-014-epic-1-RWB-E1-065/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-014-epic-1-RWB-E1-065/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Ready for specify |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 9 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-065-sandbox-database-with-synthetic-recovery-data-v1.md` |
| Output run | `output/INC-014-epic-1-RWB-E1-065/` |

