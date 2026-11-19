# Increment Card — INC-008-epic-1-RWB-E1-043

**RWB-E1-043 — Reference data service with versioned tables**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-008` |
| Title | Reference data service with versioned tables |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-043` |
| RUN_ID | `INC-008-epic-1-RWB-E1-043` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | Enabler |
| Priority | Must |
| Build order | 8 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-042, RWB-E1-044 |
| Blocks | See the build sequence |
| Status | Planned — plan carried from the 10 Nov 2026 run; re-baseline for D-RCV-35 |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P3 Case and workflow.

## Scope

**Story:** As a **reference data administrator (RW-REFADM)**, I want **products, regions, exposure bands, roles, teams, queues, service levels, document types, templates, delegation of authority and legal periods held as versioned reference data with valid from, valid to, author and approver**, so that **business values change by a data release and not by code, and every engine can say which version it used**.

**Business outcome:** Today the values that drive allocation, timers and approval limits live in team spreadsheets and in procedure documents, so nobody can say which value applied to a case on a given day. This story gives every reference table a version with a valid from date, an author and a different approver, and serves the version in force to the engines. The holiday calendar is not one of them: ACE holds the Bank of Thailand calendar in `bot_holiday`, and the timer engine reads it through `v_ace_holiday`, so no Workbench list holds holidays and no holiday load is needed. It meets REQ-DRI-011 and REQ-CWC-006 and supports control CTL-08 (a rule, limit or list changes only through a validated load approved by its owner). The measure is that every value an engine reads carries a table code and a version number in its log line.

**Main flow:**
1. Reference data administrator: uploads a load file for one table code with a valid from date through `POST /admin/reference-loads`.
2. P4 load handler: passes the file rows, the table code, the valid from date and the caller's user ID to `ReferenceVersionRegistry.recordVersion(...)`.
3. Reference data service: checks the table code, the row schema for that table, the row keys, the valid from date and the author; computes the content hash and the next version number.
4. Reference data service: writes one `reference_version` row with status VALIDATED and one `reference_row` row per file row, in one transaction.
5. Approver: approves the load through `POST /admin/reference-loads/{loadId}/approve`.
6. Reference data service: checks that the approver is present, is not the author and holds the approve right; sets status APPROVED, `approver_user_id` and `approved_at`.

**Acceptance criteria:**
- AC1: Versioned row
- AC2: Approver recorded
- AC3: Read by services
- AC4: Row fails the schema check
- AC5: Approval with no approver
- AC6: Valid from in the past
- AC7: Same file loaded twice
- AC8: Two approvals at once
- AC9: No version in force
- AC10: Empty load file

**Out of scope:**
- Rule packages and their load, validation, approval and rollback (RWB-E1-072, RWB-E1-073). Rule tables are not reference tables.
- The permission matrix and masking tables (RWB-E1-037) and the delegation of authority content (RWB-E1-038).
- The checklist fields and the rule change audit report (RWB-E2-041).
- Product parameter completeness checks (RWB-E1-045).
- Reference data screens SCR-39, SCR-40 and SCR-42 (Epic 8).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-043-reference-data-service-with-versioned-tables-v2.md` |
| Requirement IDs | REQ-DRI-011, REQ-CWC-006 |
| BRD section | Business Requirements Epic 1, sections 3.3 and 4; Business Requirements Program, sections 5.3 and 5.7 |
| Decision | D-RCV-36 (T3, T4, T8); ADR-012 |
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
| RW-REFADM, reference data administrator | Loads a version (Reference data C). Reads versions (R) |
| RW-COE, center of excellence analyst | Loads a version of the tables it owns (Reference data C) |
| RW-RISK, risk and model risk officer | Approves a version. Assumed: RW-RISK holds the approve right in Reference data, because no role holds it in the permission matrix today. The permission matrix change is loaded through RWB-E1-037; holders by name follow DL18 |
| SY-CASEWF, case workflow module | Reads the version in force (Reference data R) |
| SY-RULES, Drools evaluator | Reads reference values as Drools facts during an evaluation (Reference data R) |
| RW-AUDIT, internal audit | Reads versions and their author and approver (Reference data R) |

The same person may not hold RW-REFADM and RW-RISK (separation of duty table). Approval of DELEGATION_LIMIT follows doa.txt How it applies, rule 11: a change is a data load approved by Risk.

## Contract extract

**POST /api/recovery/v1/admin/reference-loads** (P4 endpoint; calls this story's interface) | Item | Value | |---|---| | Request | multipart/form-data: `file` (CSV or XLSX, one sheet), `table` (a LOV-REF-TABLE code), `validFrom` (date) | | Response | 201 `ReferenceLoad`: `id`, `table`, `validFrom`, `status` (VALIDATED), `rows` | | Errors | 401 no session (MSG-P4-001); 403 no Reference data C (MSG-P4-002); 409 an approved version of the table already has this valid from (MSG-P3-027); 422 a check failed (MSG-P3-027) or the file has no rows (MSG-GEN-001); 503 the store is unavailable | | Authorization | Reference data, right C | | Idempotency | Table code, valid from and content hash. A repeat returns the existing load and writes nothing | **POST /api/recovery/v1/admin/reference-loads/{loadId}/approve** (P4 endpoint) | Item | Value | |---|---| | Request | Path `loadId` (uuid). No body | |…

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

- No business value in code: table codes, columns, bands, periods and limits are rows; the code holds only the versioning behavior. - No personal data in logs, tests, workflow history or prompts: log lines carry table codes and version numbers only, and test files use synthetic codes. - No read of another module's tables; ACE data only through recovery.v_ace_* views: `lov_value` is read through the P4 published interface, and P4 reaches the registry only through `ReferenceVersionRegistry`. - A version row is never updated in place except for its status, approver and valid to; a correction is a new version. - The cache never serves a version that is not APPROVED. - No rule table is held, loaded or versioned here: rule packages are Drools packages of RWB-E1-072 and RWB-E1-073, and LOV-REF-TABLE carries no rule table code.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-043-reference-data-service-with-versioned-tables-v2.md` |
| Specification | `output/INC-008-epic-1-RWB-E1-043/specify/spec.md` |
| Compliance validation | `output/INC-008-epic-1-RWB-E1-043/specify/compliance-validation.md` |
| Agent run log | `output/INC-008-epic-1-RWB-E1-043/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-008-epic-1-RWB-E1-043/plan/` |
| Implementation evidence | `output/INC-008-epic-1-RWB-E1-043/implement/` |
| API / functional test reports | `output/INC-008-epic-1-RWB-E1-043/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-008-epic-1-RWB-E1-043/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Planned — plan carried from the 10 Nov 2026 run; re-baseline for D-RCV-35 |
| Specification | SUCCESS — 10 Nov 2026, needs re-baseline for D-RCV-35 |
| Compliance review | PASS (2026-11-10) |
| Acceptance criteria | 10 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation | Spec and plan carried from `INC-009 (10 November 2026 run)`; not built. |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-043-reference-data-service-with-versioned-tables-v2.md` |
| Output run | `output/INC-008-epic-1-RWB-E1-043/` |

