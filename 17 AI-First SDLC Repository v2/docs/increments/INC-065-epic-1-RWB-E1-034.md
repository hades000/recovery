# Increment Card — INC-065-epic-1-RWB-E1-034

**RWB-E1-034 — Letter template management**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-065` |
| Title | Letter template management |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-034` |
| RUN_ID | `INC-065-epic-1-RWB-E1-034` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P6 Communications |
| Story type | User story |
| Priority | Should |
| Build order | 65 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-046, RWB-E1-015 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P6 Communications.

## Scope

**Story:** As a **litigation officer (RW-LITOFF)**, I want **a screen to upload a template version, have Legal counsel record the approval and set it current**, so that **templates are managed without a developer**.

**Business outcome:** A template change today needs a person outside Legal to edit a file and send it round, and nothing records which wording was approved. This story gives the litigation officer an upload and Legal counsel an approve and withdraw action on SCR-33 Template approval, with the approver and date held on the version. It serves REQ-OCC-002 and control CTL-14 (every notice from the current Legal-approved version), and removes the developer from template changes.

**Main flow:**
1. Litigation officer: opens SCR-33 Template approval and chooses the template code and language, or a new code.
2. Litigation officer: uploads the DOCX body and enters product group, channel, notice type, signature basis and the merge codes used.
3. System: checks the role (Documents C), the required fields, the file type and size, and every merge code against the catalog (MergeCodeScanner from RWB-E1-046).
4. System: stores the body write-once, creates the next version number in state Draft and shows it in the list.
5. Legal counsel: opens the Draft version, reads the body and the merge codes, enters the valid from date and approves.
6. System: checks the role (Documents A), that the approver is not the uploader (CTL-05), that the version is Draft and that valid from is not before today; sets state Approved with approver and approval time.

**Acceptance criteria:**
- AC1: New version
- AC2: Approval required
- AC3: The uploader cannot approve the version
- AC4: Unknown merge code refused at upload
- AC5: Required field empty
- AC6: File type not allowed
- AC7: Valid from before today
- AC8: Withdraw the current version
- AC9: Two approvals at the same time
- AC10: Repeated approval request

**Out of scope:**
- The catalog tables, load checks and TemplateCatalog interface (RWB-E1-046).
- Generating notices from a template (RWB-E1-052) and resuming held notices when a new version is approved (R-LIT-06, RWB-E2-021).
- Adding a template through the Compliance approval path (FEAT-ADM-05, Epic 8).
- Thai labels on SCR-33 beyond the standard messages (DL10).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-034-letter-template-management-v1.md` |
| Requirement IDs | REQ-OCC-002 |
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
| RW-LITOFF, litigation officer | Uploads a version (Documents C), reads templates (Documents R) |
| RW-LEGAL, Legal counsel | Uploads, approves and withdraws a version (Documents CRUA); cannot approve own upload |
| RW-CASEOWN, RW-TEAMMGR and other roles with Documents R | Read templates on SCR-33 |
| RW-COMPLY, Compliance and PDPA officer | Reads templates (Documents R) |

No approval level from the delegation of authority applies; Legal approval of wording is a Documents A right.

## Contract extract

All five endpoints are new and recorded in the additions file. Base path /api/recovery/v1. Errors use the Problem schema. | Method and path | Request | Response | Errors | Authorization | Idempotency | |---|---|---|---|---|---| | GET /templates | Query: code, language, state, page, size | 200 TemplatePage (items of Template) | 401, 403, 503 | Documents R, scope applied | Not applicable | | POST /templates | multipart: file, templateCode, language, productGroup, channel, noticeType, signatureBasis, mergeCodes | 201 Template, state DRAFT | 401; 403 (MSG-P4-002); 413; 415 (MSG-P6-010); 422 (MSG-GEN-001, MSG-P6-006); 503 (MSG-GEN-006) | Documents C | Idempotency-Key header | | GET /templates/{templateId}/content | None | 200 application/octet-stream | 401, 403, 404, 503 | Documents R | Not applicable | | POST /templates/{templateId}/approve | TemplateApproval: validFrom | 200 Template, stat…

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

- No business value in code: file types, size limit, merge codes and the template list are data or configuration. - No personal data in logs, tests or prompts. Template bodies in tests carry synthetic wording; the audit entry holds user IDs, template code and version only. - No read of another module's tables. Roles come from the ACE access check; storage through the ACE storage pattern. - A stored body is never overwritten; a correction is a new version. - The screen hides actions the role does not hold, and the server checks the right on every call.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-034-letter-template-management-v1.md` |
| Specification | `output/INC-065-epic-1-RWB-E1-034/specify/spec.md` |
| Compliance validation | `output/INC-065-epic-1-RWB-E1-034/specify/compliance-validation.md` |
| Agent run log | `output/INC-065-epic-1-RWB-E1-034/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-065-epic-1-RWB-E1-034/plan/` |
| Implementation evidence | `output/INC-065-epic-1-RWB-E1-034/implement/` |
| API / functional test reports | `output/INC-065-epic-1-RWB-E1-034/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-065-epic-1-RWB-E1-034/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 10 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-034-letter-template-management-v1.md` |
| Output run | `output/INC-065-epic-1-RWB-E1-034/` |

