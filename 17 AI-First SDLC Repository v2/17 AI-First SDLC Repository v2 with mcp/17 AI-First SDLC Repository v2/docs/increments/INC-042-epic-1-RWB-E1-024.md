# Increment Card — INC-042-epic-1-RWB-E1-024

**RWB-E1-024 — Document store and index**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-042` |
| Title | Document store and index |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-024` |
| RUN_ID | `INC-042-epic-1-RWB-E1-024` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P5 Document hub |
| Story type | User story |
| Priority | Must |
| Build order | 42 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-027, RWB-E1-018, RWB-E1-025, RWB-TE-012, RWB-E1-001 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P5 Document hub.

## Scope

**Story:** As a **litigation officer (RW-LITOFF)**, I want **every document stored against its case with its type, date, source and extracted fields, legal types held in a write-once container, and every version kept**, so that **I find a document by case ID, type and date, and a legal document cannot be changed after it is stored**.

**Business outcome:** Recovery documents are held today in folders, shared drives and with couriers; originals go missing and evidence is rebuilt for each audit (FSD P5 A1.3). This story builds the store and the index that every other document story writes to: one document record in the Workbench document hub per file, the file in blob storage, legal types write-once (DT06, ADR-007, control CTL-12). It meets REQ-DCM-001, REQ-DCM-002, REQ-DCM-003 and REQ-DCM-008. The module measure is fields extracted without review (FSD P5 A2.1.1), which can only be counted once every document is indexed against its case.

**Main flow:**
1. Caller: calls DocumentStore.store with the case ID, the document type, the source, the file in the intake container, its SHA-256 hash and any extracted fields.
2. DocumentStoreService: gets the case through CaseDirectory.findById and refuses the call if the case does not exist.
3. DocumentStoreService: reads the type row from the document type table version in force: write_once and retention_class.
4. DocumentStoreService: checks the file type by its content signature and the file size against INTAKE_ALLOWED_TYPES and INTAKE_MAX_FILE_MB.
5. DocumentStoreService: looks for an active document on the case with the same type and hash; if one exists, returns it and stops.
6. DocumentStoreService: in one transaction, writes the decision log entry (decision code DOCATT, final call STORED) through DecisionLogWriter, inserts the document row with doc_version 1 and state COPY_PENDING, inserts the document_field rows and writes DocumentStored (EV-16) to the outbox.

**Acceptance criteria:**
- AC1: Stored against case
- AC2: Write once
- AC3: Retention class
- AC4: A new version keeps the history
- AC5: Unknown document type is refused
- AC6: File type not allowed
- AC7: Size limit boundary
- AC8: The same file stored twice
- AC9: Two versions added at the same time
- AC10: Version on a superseded document
- AC11: The storage copy fails
- AC12: Case outside the reader's scope

**Out of scope:**
- The upload form, the case document list and the search within a case (RWB-E1-026).
- Classification, field extraction and automatic attach from the OCR intake (RWB-E1-050, RWB-E1-053, RWB-E1-032).
- Confirming or correcting an extracted field with PATCH /documents/{documentId}/fields/{fieldId} (RWB-E1-054).
- Retention periods, the retention job and the virus scan (RWB-E1-041).
- Container creation, backup and restore tests (RWB-TE-012; REQ-DCM-015).
- Custody of originals (Epic 2, SCR-32) and electronic discovery (Epic 2, REQ-DCM-017).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-024-document-store-and-index-v1.md` |
| Requirement IDs | REQ-DCM-001, REQ-DCM-002, REQ-DCM-003, REQ-DCM-008 |
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
| SY-OCR, OCR and extraction pipeline | Stores documents through DocumentStore (Documents C) |
| RW-CASEOWN, RW-LITOFF, RW-RESTRUCT and the other roles with Documents C | Store through the upload in RWB-E1-026 |
| Roles with Documents U (for example RW-CASEOWN, RW-LITOFF, RW-LEGAL, RW-COMPLY) | Add a new version |
| Roles with Documents R (for example RW-TEAMMGR, RW-AUDIT, RW-PHONECOL) | Read metadata and content inside their scope |
| SY-DECLOG, decision log writer | Writes the DOCATT entry |
| Nobody | Deletes or changes a write-once document |

## Contract extract

**GET /documents/{documentId}** | Item | Value | |---|---| | Request | Path documentId (uuid) | | Response | 200 Document: id, caseId, partyId, documentType, source, storageRef, classificationConfidence, reviewStatus, retentionClass, writeOnce, docVersion. Extended with storedAt, previousVersionId, versions and fields (see additions) | | Errors | 401 not signed in; 403 no Documents R (MSG-P4-002) or case out of scope (MSG-P4-003); 404 no such document; 503 store unavailable (MSG-GEN-006) | | Authorization | Documents, right R, scope applied | | Idempotency | Not applicable | **GET /api/recovery/v1/documents/{documentId}/content** | Item | Value | |---|---| | Request | Path documentId (uuid) | | Response | 200 application/octet-stream, the file of that version | | Errors | 401; 403 as above; 404; 503 while state is COPY_PENDING (MSG-GEN-006) | | Authorization | Documents, right R, scope…

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

- No business value in code: file types, size limit, write-once flag, retention class and container names are data rows or properties. - No personal data in logs, tests or prompts. Test files are synthetic; extracted field values in logs are replaced by the field name. - No read of another module's tables: the case is read through CaseDirectory, the decision log is written through DecisionLogWriter. - The service never overwrites a blob; every version is a new blob path. - The PII access log entry for each read is written by the ACE common module, never by this package.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-024-document-store-and-index-v1.md` |
| Specification | `output/INC-042-epic-1-RWB-E1-024/specify/spec.md` |
| Compliance validation | `output/INC-042-epic-1-RWB-E1-024/specify/compliance-validation.md` |
| Agent run log | `output/INC-042-epic-1-RWB-E1-024/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-042-epic-1-RWB-E1-024/plan/` |
| Implementation evidence | `output/INC-042-epic-1-RWB-E1-024/implement/` |
| API / functional test reports | `output/INC-042-epic-1-RWB-E1-024/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-042-epic-1-RWB-E1-024/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 12 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-024-document-store-and-index-v1.md` |
| Output run | `output/INC-042-epic-1-RWB-E1-024/` |

