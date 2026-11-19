# Increment Card — INC-003-epic-1-RWB-E1-042

**RWB-E1-042 — Central configuration service and parameter catalog**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-003` |
| Title | Central configuration service and parameter catalog |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-042` |
| RUN_ID | `INC-003-epic-1-RWB-E1-042` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | Enabler |
| Priority | Must |
| Build order | 3 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-044 |
| Blocks | See the build sequence |
| Status | Implemented — migration applied and tested; spec and plan rebaselined 16 Nov 2026 |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P3 Case and workflow.

## Scope

**Story:** As a **squad member (RW-TRIBE)**, I want **every environment setting and business parameter read from one configuration service and listed in a parameter catalog with name, type, default, owner, environment and where it is used**, so that **no value is hard-coded and every parameter has an owner**.

**Business outcome:** Thresholds such as the 90-day entry point are written into code and spreadsheets today, so a change needs a release and nobody can say who owns a value. This story holds every parameter definition in a catalog with an owner and a default, holds business values as approved, dated versions per environment, serves them to every engine at run time, and fails the build when code carries a literal business value or reads a parameter the catalog does not list. It meets REQ-DRI-010 and puts Principle 1 (DT02) into the build pipeline.

**Main flow:**
1. Squad member: adds a parameter to `config/parameter-catalog.csv` with key, kind, type, unit, range, default, scope, required, owner role, environments and used by; the pull request is reviewed by the owner.
2. Build: generates the `ParameterKeys` class from the catalog file; code reads a value only through ParameterService with a generated key.
3. Build: runs the magic number check over the recovery packages and the catalog completeness check.
4. Flyway: loads the catalog rows and the default values into parameter_catalog and parameter_value at deployment.
5. RW-COE: loads a new value version through POST /admin/reference-loads with table "PARAMETER", for example `case.entry.dpd` = 91 in PROD valid from 2026-12-10.
6. ParameterLoadChecks: checks key in catalog, type, range, environment and required values; refuses the load whole on any failure.

**Acceptance criteria:**
- AC1: Parameter read at run time
- AC2: Hard-coded value caught
- AC3: Catalog complete
- AC4: Required value missing at start-up
- AC5: Value outside its range
- AC6: Wrong type
- AC7: Author cannot approve
- AC8: Values per environment
- AC9: Secrets are listed, never served
- AC10: Rollback of a value version
- AC11: A new value takes effect on its valid from date

**Out of scope:**
- The reference data service for the other tables (RWB-E1-043).
- Product-specific parameters and service levels (RWB-E1-045).
- Dated feature flags (FEAT-CWC-26).
- The administration screen for parameters (Epic 8, FEAT-ADM-01).
- The change checklist and audit report (RWB-E2-041).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-042-central-configuration-service-and-parameter-catalog-v1.md` |
| Requirement IDs | REQ-DRI-010 |
| BRD section | Business Requirements Epic 1, section 3.3; Business Requirements Program, sections 5.3 and 5.7 |
| Decision | D6 entry |
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
| RW-COE | Owns the catalog; loads value versions (Reference data C; Rules and parameters CRUD) |
| RW-RISK | Approves a value version where a threshold or a limit moves (Reference data A, assumed grant; DL01) |
| RW-PLATADM | Owns environment settings; reads the catalog (Rules and parameters R) |
| RW-TRIBE | Adds catalog entries through reviewed pull requests |
| Every role with Rules and parameters R | Reads the catalog |
| RW-PHONECOL | No Rules and parameters right; refused |
| No delegation of authority level applies | A parameter is not a credit decision |

## Contract extract

**GET /admin/parameters** (new endpoint, see additions) | Item | Value | |---|---| | Request | Query key (prefix), kind, owner, environment | | Response | 200 array of { key, kind, type, unit, min, max, default, scope, required, owner, environments, usedBy, secret, valueInForce (absent when secret), versionNo, validFrom } | | Errors | 401 (MSG-P4-001); 403 no Rules and parameters R (MSG-P4-002); 503 | | Authorization | Rules and parameters, right R | | Idempotency | Not applicable | **POST /api/recovery/v1/admin/reference-loads** with table "PARAMETER" (P4 endpoint; this story builds the PARAMETER handler) | Item | Value | |---|---| | Request | multipart/form-data: file (rows of key, environment, value), table = "PARAMETER", validFrom | | Response | 201 ReferenceLoad: id, table, validFrom, status, rows | | Errors | 401; 403 no Reference data C (MSG-P4-002); 422 range (MSG-GEN-002), type…

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

- No business value in code: every limit, threshold, name and timer is a catalog entry with a value row; the build check enforces it. - No personal data in parameters, logs, tests or prompts; no secret value in the tables, the logs or any response. - No read of another module's tables: other modules read values only through ParameterService. - A value change never needs a deployment; a new parameter needs a reviewed catalog entry.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-042-central-configuration-service-and-parameter-catalog-v1.md` |
| Specification | `output/INC-003-epic-1-RWB-E1-042/specify/spec.md` |
| Compliance validation | `output/INC-003-epic-1-RWB-E1-042/specify/compliance-validation.md` |
| Agent run log | `output/INC-003-epic-1-RWB-E1-042/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-003-epic-1-RWB-E1-042/plan/` |
| Implementation evidence | `output/INC-003-epic-1-RWB-E1-042/implement/` |
| API / functional test reports | `output/INC-003-epic-1-RWB-E1-042/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-003-epic-1-RWB-E1-042/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Implemented — migration applied and tested; spec and plan rebaselined 16 Nov 2026 |
| Specification | SUCCESS — new v2 spec 16 Nov 2026 |
| Compliance review | PASS |
| Acceptance criteria | 11 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation | IMPLEMENTED. Migration pack `E1-042 Migration and Clarifications`; evidence `output/INC-003-epic-1-RWB-E1-042/implement/`. |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-042-central-configuration-service-and-parameter-catalog-v1.md` |
| Output run | `output/INC-003-epic-1-RWB-E1-042/` |

