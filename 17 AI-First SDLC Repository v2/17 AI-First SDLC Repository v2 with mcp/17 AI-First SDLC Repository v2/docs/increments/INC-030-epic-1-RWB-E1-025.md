# Increment Card — INC-030-epic-1-RWB-E1-025

**RWB-E1-025 — Document types and fields agreed**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-030` |
| Title | Document types and fields agreed |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-025` |
| RUN_ID | `INC-030-epic-1-RWB-E1-025` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P5 Document hub |
| Story type | User story |
| Priority | Must |
| Build order | 30 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-069 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P5 Document hub.

## Scope

**Story:** As a **center of excellence analyst (RW-COE)**, I want **the first six document types (demand letter, court notice, appraisal report, title deed, settlement agreement, guarantor notice) with their key fields agreed with Legal and NPA and held as versioned reference data**, so that **the OCR pipeline, classification and extraction have one signed target list**.

**Business outcome:** Classification and extraction cannot be built or measured until the bank fixes which types are read and which fields come out of each (REQ-DCM-004, DL19). Today no signed list exists, so the model would train on a list that may change. This story turns the agreed list into a versioned table that the store (RWB-E1-024), classification (RWB-E1-050) and extraction (RWB-E1-053) read, and that changes by a data load without a code release (DT02). The measure it serves is fields extracted without review (FSD P5 A2.3.1).

**Main flow:**
1. Center of excellence analyst: prepares the list of six types and 26 fields; legal counsel and the Head of NPA review it and sign with a date.
2. Reference data administrator: uploads the file with POST /admin/reference-loads, table DOCUMENT_TYPE, validFrom 2026-11-30.
3. P4 reference load service: passes the rows to DocumentTypeLoader through the ReferenceTableLoader interface.
4. DocumentTypeLoader: validates every row: type code unique, label present, write-once flag present, retention class in LOV-RETENTION, at least one field, both sign-offs with a user ID and a date.
5. DocumentTypeLoader: on any failure refuses the load whole and returns the row errors; the version in force is unchanged.
6. DocumentTypeLoader: on success writes the rows as table version DOCTYPE-2026.11 with status LOADED, not yet in force.

**Acceptance criteria:**
- AC1: Field list signed
- AC2: Reference data
- AC3: Load without both sign-offs is refused
- AC4: Invalid values are refused in full
- AC5: The same version loaded twice
- AC6: A future version takes effect on its date
- AC7: The loader cannot approve their own load

**Out of scope:**
- The retention periods behind each class (RWB-E1-041; DL26).
- The checklist of required types per case type (RWB-E1-040).
- Stage 2 and 3 document types (RWB-E2-025).
- The reference data screen SCR-40 (Epic 8).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-025-document-types-and-fields-agreed-v1.md` |
| Requirement IDs | REQ-DCM-004 |
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
| RW-COE, center of excellence analyst | Prepares the list and reads the table |
| RW-LEGAL, legal counsel | Signs the list for Legal |
| RW-HEADNPA, Head of NPA | Signs the list for NPA |
| RW-REFADM, reference data administrator | Loads the file (Reference data C) |
| Approver with Reference data A | Approves the load. The permission matrix gives Reference data A to no role today; assumed granted to the legal counsel who owns the table (DL01) |
| SY-OCR, SY-RULES | Read the version in force |

## Contract extract

**POST /admin/reference-loads** (P4 endpoint; this story adds the table code DOCUMENT_TYPE) | Item | Value | |---|---| | Request | multipart/form-data: file (binary, the load file in the Excel template), table = "DOCUMENT_TYPE", validFrom (date) | | Response | 201 ReferenceLoad: id, table, validFrom, status (LOADED or REFUSED), rows | | Errors | 401; 403 no Reference data C (MSG-P4-002); 409 version already loaded (MSG-P3-027); 422 a row fails validation (MSG-P3-027 with row and error); 503 store unavailable (MSG-GEN-006) | | Authorization | Reference data, right C | | Idempotency | The table code and the table version; a second load of the same version is refused with 409 | **POST /api/recovery/v1/admin/reference-loads/{loadId}/approve** | Item | Value | |---|---| | Request | Path loadId (uuid) | | Response | 200 ReferenceLoad with status APPROVED | | Errors | 401; 403 no Reference dat…

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

- No business value in code: type codes, fields, write-once flags and retention classes are rows in document_type. - No personal data in logs, tests or prompts. Sign-off users in tests are synthetic IDs. - No read of another module's tables: LOV-RETENTION is read through the P4 list service. - A refused load writes no row.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-025-document-types-and-fields-agreed-v1.md` |
| Specification | `output/INC-030-epic-1-RWB-E1-025/specify/spec.md` |
| Compliance validation | `output/INC-030-epic-1-RWB-E1-025/specify/compliance-validation.md` |
| Agent run log | `output/INC-030-epic-1-RWB-E1-025/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-030-epic-1-RWB-E1-025/plan/` |
| Implementation evidence | `output/INC-030-epic-1-RWB-E1-025/implement/` |
| API / functional test reports | `output/INC-030-epic-1-RWB-E1-025/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-030-epic-1-RWB-E1-025/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 7 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-025-document-types-and-fields-agreed-v1.md` |
| Output run | `output/INC-030-epic-1-RWB-E1-025/` |

