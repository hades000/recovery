# Increment Card — INC-032-epic-1-RWB-E1-046

**RWB-E1-046 — Template and merge field catalog as data**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-032` |
| Title | Template and merge field catalog as data |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-046` |
| RUN_ID | `INC-032-epic-1-RWB-E1-046` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P6 Communications |
| Story type | User story |
| Priority | Must |
| Build order | 32 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-001, RWB-E1-069 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P6 Communications.

## Scope

**Story:** As a **litigation officer (RW-LITOFF)**, I want **letter and document templates and their merge fields held as versioned data with the Legal approval record on each version**, so that **a template change is a data release approved by Legal and never a code release**.

**Business outcome:** Letters and notices are prepared by hand today, so the wording and the facts on a notice depend on who typed it. This story holds every template version, the merge fields it draws from the case and the Legal approval as data rows, so the letter engine (RWB-E1-052) can only use a version Legal approved and can only fill fields the catalog knows. It serves REQ-OCC-001 and REQ-OCC-002 and the FSD P6 measure "notices with proof of delivery, 100 percent", which needs every notice to come from a known template version (CTL-14).

**Main flow:**
1. Reference data administrator: loads the merge field catalog file through POST /admin/reference-loads with table "merge_field" and a valid from date.
2. System: checks every row: merge code unique, BR Field ID present in sys_fields, source entity and field present, required flag set. A row that fails refuses the whole load (refdata change process, step 3).
3. Reference data administrator: loads a template version file through POST /admin/reference-loads with table "template", carrying template code, language, product group, channel, notice type, signature basis, the body file reference, the merge codes used and, where Legal has signed, the approver and approval date.
4. System: reads every merge code in the body and in the merge code list and checks each one against the catalog in force. An unknown code refuses the load and names the code (MSG-P6-006).
5. System: assigns the next version number for the template code and language, keeps every earlier version readable and sets state Approved only where the approver and approval date are present, otherwise Draft.
6. System: the published interface TemplateCatalog returns, for a template code, language and date, the current version: the Approved version with the highest version number whose valid from date is on or before that date.

**Acceptance criteria:**
- AC1: Template versioned
- AC2: Unapproved template blocked
- AC3: Merge fields checked
- AC4: Catalog row with an unknown field ID is refused
- AC5: Template row with a missing required field is refused
- AC6: Repeated load creates no new version
- AC7: Withdrawn current version leaves no current version
- AC8: Future valid from date keeps the earlier version current

**Out of scope:**
- The template screen with upload, approval and withdrawal (RWB-E1-034).
- Generating notices from the templates (RWB-E1-052).
- Contract, credit approval and mortgage document generation (RWB-E2-026).
- Adding a template through the Compliance approval path (FEAT-ADM-05, Epic 8).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-046-template-and-merge-field-catalog-as-data-v1.md` |
| Requirement IDs | REQ-OCC-001, REQ-OCC-002 |
| BRD section | Business Requirements Epic 1, sections 3.6 and 4 |
| Decision | D7.1 |
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
| RW-REFADM, reference data administrator | Loads the catalog and template files (Reference data C) |
| RW-LEGAL, Legal counsel | Approves a template version; the approver named in the load (Documents A) |
| RW-LITOFF, litigation officer | Reads templates and the catalog (Documents R) |
| RW-COE, center of excellence analyst | Reads the catalog (Reference data R) |
| SY-CASEWF, case workflow module | Calls TemplateCatalog for the current version |

No approval level from the delegation of authority applies.

## Contract extract

**POST /api/recovery/v1/admin/reference-loads** (exists, module P4) | Item | Value | |---|---| | Request | multipart/form-data: file, table ("template" or "merge_field"), validFrom | | Response | 201 ReferenceLoad: id, table, validFrom, status, rows | | Errors | 401 no session (MSG-P4-001); 403 role lacks Reference data C (MSG-P4-002); 409 a load for the same table and file hash already exists (MSG-P1-002); 422 a row fails a check (MSG-GEN-001, MSG-P6-006, MSG-P1-002); 503 store unavailable (MSG-GEN-006) | | Authorization | Reference data, right C | | Idempotency | SHA-256 hash of the file per table; a repeat is refused (AC6) | P4 owns the endpoint. This story adds two table handlers to it through the P4 published interface: ```java public interface ReferenceLoadHandler { String table(); // "template" or "merge_field" LoadValidation validate(LoadFile file, LocalDate validFrom); LoadResu…

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

- No business value in code: template codes, languages, merge codes, field mappings and dates are read from the template and merge_field tables. - No personal data in logs, tests or prompts. Template bodies in tests use synthetic wording; merge values never appear in logs. - No read of another module's tables. sys_fields is read through the P4 reference data interface; the load path is P4's. - Earlier template versions are never updated or deleted. - A merge field marked personal_data is resolved only at generation time through the masking rules (RWB-E1-052), never stored in the template.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-046-template-and-merge-field-catalog-as-data-v1.md` |
| Specification | `output/INC-032-epic-1-RWB-E1-046/specify/spec.md` |
| Compliance validation | `output/INC-032-epic-1-RWB-E1-046/specify/compliance-validation.md` |
| Agent run log | `output/INC-032-epic-1-RWB-E1-046/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-032-epic-1-RWB-E1-046/plan/` |
| Implementation evidence | `output/INC-032-epic-1-RWB-E1-046/implement/` |
| API / functional test reports | `output/INC-032-epic-1-RWB-E1-046/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-032-epic-1-RWB-E1-046/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 8 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-046-template-and-merge-field-catalog-as-data-v1.md` |
| Output run | `output/INC-032-epic-1-RWB-E1-046/` |

