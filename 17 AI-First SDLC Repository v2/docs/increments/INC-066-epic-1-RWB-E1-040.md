# Increment Card — INC-066-epic-1-RWB-E1-040

**RWB-E1-040 — Document checklist per case type as reference data**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-066` |
| Title | Document checklist per case type as reference data |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-040` |
| RUN_ID | `INC-066-epic-1-RWB-E1-040` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P5 Document hub |
| Story type | User story |
| Priority | Should |
| Build order | 66 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-024, RWB-E1-043, RWB-E1-025, RWB-E1-026 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P5 Document hub.

## Scope

**Story:** As a **litigation officer (RW-LITOFF)**, I want **the required documents per case type and route held as a versioned reference table that the case documents screen, the case list and the review queue read**, so that **a missing document shows on the case without a person checking a list**.

**Business outcome:** Litigation packs and guarantee claims fail when a required document is missing, and today the gap is found by a person reading a paper list, often at filing (CTL-19, R-LIT-17). This story holds the checklist per case stage and route as data and keeps a completeness flag per case, recomputed whenever a document is stored or the case changes stage. It meets REQ-DCM-011 and gives the pack checks of Epic 4 and Epic 5 (R-LIT-16, R-GUA-07) one checklist source. The measure is fields extracted without review (FSD P5 A2.16.1).

**Main flow:**
1. Reference data administrator: loads the checklist file with POST /api/recovery/v1/admin/reference-loads, table DOCUMENT_CHECKLIST; the owner approves it.
2. ChecklistLoader: validates every row: stage in LOV-STAGE, route in LOV-ROUTE or empty, document type in the type table in force, no duplicate row; refuses the load whole on any error.
3. ChecklistEvaluator: on DocumentStored (EV-16), on CaseStateChanged (EV-05) and when a checklist version takes effect, takes the case's stage and route through CaseDirectory.
4. ChecklistEvaluator: picks the rows of the version in force for that stage, using the rows for the route where they exist and the rows with no route otherwise.
5. ChecklistEvaluator: counts the active documents of each required type on the case and writes case_document_check: checklist version, required count, present count, missing types and complete.
6. Litigation officer: opens the Documents tab (SCR-30); GET /cases/{caseId}/document-checklist returns each required item marked present or missing.

**Acceptance criteria:**
- AC1: Checklist by type
- AC2: Change as data
- AC3: Completeness flag
- AC4: The missing document arrives
- AC5: Stage change
- AC6: No checklist for the stage
- AC7: Load with an unknown type
- AC8: The same event twice
- AC9: Earlier version of a document

**Out of scope:**
- The litigation pack check against the defect list and the block at filing (FEAT-LIT-05, Epic 5; CTL-19).
- The guarantee claim checklist (FEAT-GUA-01, Epic 4).
- Retrieval requests for missing documents (R-LIT-17, Epic 5).
- The review queue screen that shows the case checklist (RWB-E1-054).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-040-document-checklist-per-case-type-as-reference-data-v1.md` |
| Requirement IDs | REQ-DCM-011 |
| BRD section | Business Requirements Epic 1, section 3.5; Business Requirements Program, section 5.5 |
| Decision | D7.2 |
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
| RW-REFADM, reference data administrator | Loads the checklist (Reference data C) |
| Approver with Reference data A | Approves the load; no role holds Reference data A in the permission matrix today; assumed granted to the legal counsel as co-owner of the checklist (DL01) |
| RW-LITOFF, RW-CASEOWN and roles with Documents R | Read the checklist and the flag for cases in their scope |
| RW-LEGAL, legal counsel | Agrees the items per stage (DL19) |
| SY-CASEWF | Publishes CaseStateChanged that triggers the recompute |

## Contract extract

**GET /api/recovery/v1/cases/{caseId}/document-checklist** (new, see additions; this story fills the required items) | Item | Value | |---|---| | Request | Path caseId | | Response | 200 DocumentChecklist: caseId, checklistVersion, stageCode, items [documentType, label, required, presentCount], missingCount, complete | | Errors | 401; 403 no Documents R (MSG-P4-002) or out of scope (MSG-P4-003); 404; 503 | | Authorization | Documents, right R, scope applied | | Idempotency | Not applicable | **POST /api/recovery/v1/admin/reference-loads** (table DOCUMENT_CHECKLIST) | Item | Value | |---|---| | Request | multipart/form-data: file, table = "DOCUMENT_CHECKLIST", validFrom | | Response | 201 ReferenceLoad | | Errors | 401; 403 (MSG-P4-002); 409 version already loaded (MSG-P3-027); 422 row errors (MSG-P3-027); 503 | | Authorization | Reference data, right C; approval with right A | | Idempot…

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

- No business value in code: stages, routes and required types are rows in document_checklist_item. - No personal data in logs, tests or prompts: the flag holds type codes and counts only. - No read of another module's tables: stage, route and owner come through CaseDirectory; P3 reads the flag through DocumentChecklistService. - The evaluator never blocks a case move; it reports only.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-040-document-checklist-per-case-type-as-reference-data-v1.md` |
| Specification | `output/INC-066-epic-1-RWB-E1-040/specify/spec.md` |
| Compliance validation | `output/INC-066-epic-1-RWB-E1-040/specify/compliance-validation.md` |
| Agent run log | `output/INC-066-epic-1-RWB-E1-040/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-066-epic-1-RWB-E1-040/plan/` |
| Implementation evidence | `output/INC-066-epic-1-RWB-E1-040/implement/` |
| API / functional test reports | `output/INC-066-epic-1-RWB-E1-040/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-066-epic-1-RWB-E1-040/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 9 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-040-document-checklist-per-case-type-as-reference-data-v1.md` |
| Output run | `output/INC-066-epic-1-RWB-E1-040/` |

