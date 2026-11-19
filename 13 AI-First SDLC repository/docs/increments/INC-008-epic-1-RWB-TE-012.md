# Increment Card — INC-008-epic-1-RWB-TE-012

**RWB-TE-012 — Document storage containers**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-008` |
| Title | Document storage containers |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-TE-012` |
| RUN_ID | `INC-008-epic-1-RWB-TE-012` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P5 Document hub |
| Story type | Enabler |
| Priority | Must |
| Window | Window 1 |
| Critical path | No |
| Depends on | RWB-TE-001 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P5 Document hub. **Build group:** P5a.

## Scope

**Story:** As a **platform administrator**, I want **blob containers for documents, with a write-once container for legal types, reached by managed identity**, so that **legal documents cannot be overwritten**.

**Main flow:**
1. Platform administrator: applies the infrastructure template for the environment, which sets the storage account (shared key access off, public network access off, TLS 1.2 minimum, private endpoint) and creates the containers rwb-intake, rwb-docs, rwb-docs-legal and rwb-quarantine.
2. Template: turns on blob versioning and soft delete for rwb-docs, sets the time-based immutability policy on rwb-docs-legal (locked in PROD, unlocked in DEV, SIT and UAT), and assigns roles: the ACE service identity on rwb-intake, rwb-docs and rwb-docs-legal; SY-OCR on rwb-intake, rwb-docs and rwb-quarantine.
3. System: on start, StorageReadinessIndicator checks that the four containers exist and that rwb-docs-legal has its immutability policy; the document hub reports ready only if both hold.
4. Document store (RWB-E1-024): writes each file through BlobStorageAdapter with the managed identity, to rwb-docs-legal for a write-once type and to rwb-docs for any other type, at the name {caseId}/{documentId}/v{docVersion}.
5. Any client: an overwrite or delete of a blob in rwb-docs-legal is refused by the storage service; StorageErrorMapper turns the refusal into WriteOnceViolationException, which the store maps to 409 MSG-P5-002, and the attempt is written to the ACE audit log.
6. Document store: a new version is a new blob at v{n+1}; the earlier blob stays readable.

**Out of scope:**
- Choosing the container per document type and writing the document row (RWB-E1-024).
- Retention classes, archive and the retention job (RWB-E1-041, JOB-17).
- Legal hold on a case or a document (REQ-DCM-016; DL27).
- Backup and restore test of the document store (REQ-DCM-015; DL27).
- Sizing and cost of the storage (REQ-DCM-014; NFR-069).

**Business outcome and value hypothesis:** Audit findings record that evidence for decisions was incomplete or unreliable, and a notice or contract held in a shared folder can be replaced without trace. This story sets up the storage that the document store (RWB-E1-024), the intake (RWB-E1-057) and the malware scan (RWB-E1-041) write to: an intake container, a standard container with version history, a write-once container whose immutability policy refuses any overwrite or delete inside its retention period, and a quarantine container, all reached only by managed identity. It meets REQ-DCM-003 and REQ-DCM-002 and is the storage behind control CTL-12 and the storage pattern recommended under DL27.

**Constraints and guardrails:**
- No business value in code: the retention period, soft delete days and container names come from template parameters and properties.
- No personal data in logs, tests or prompts: blob names carry case and document IDs only, never a customer name or ID number; test files are synthetic.
- No read of another module's tables.
- No account key, connection string or shared access signature in code, configuration or the pipeline.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 012 Document storage containers v1.md` |
| Requirement IDs | REQ-DCM-003, REQ-DCM-002 |
| BRD section | Business Requirements Program, section 5.5 |
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
| RW-PLATADM, platform administrator | Applies the infrastructure template and reads the readiness check (Platform administration CRUD) |
| RW-SECADM, security administrator | Reviews the role assignments on the containers (Platform administration CRUDA) |
| SY-OCR, OCR and extraction pipeline | Writes to rwb-intake, rwb-docs and rwb-quarantine with its managed identity |
| RW-CASEOWN, case owner | Uploads documents through the store, which uses the ACE service identity (Documents CRU) |
| Solution architect with Compliance | Owns DL27 |

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
- **Feature flag:** None.
- **Critical path:** No; **depends on:** RWB-TE-001.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: the retention period, soft delete days and container names come from template parameters and properties.
  - No personal data in logs, tests or prompts: blob names carry case and document IDs only, never a customer name or ID number; test files are synthetic.
  - No read of another module's tables.
  - No account key, connection string or shared access signature in code, configuration or the pipeline.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 012 Document storage containers v1.md` |
| Specification | `output/INC-008-epic-1-RWB-TE-012/specify/spec.md` |
| Compliance validation | `output/INC-008-epic-1-RWB-TE-012/specify/compliance-validation.md` |
| Agent run log | `output/INC-008-epic-1-RWB-TE-012/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-008-epic-1-RWB-TE-012/plan/` (TBC) |
| Implementation evidence | `output/INC-008-epic-1-RWB-TE-012/implement/` (TBC) |
| API / functional test reports | `output/INC-008-epic-1-RWB-TE-012/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-008-epic-1-RWB-TE-012/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-008-epic-1-RWB-TE-012/specify/compliance-validation.md`) |
| Acceptance criteria | 12 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11, AC12) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 012 Document storage containers v1.md` |
| Output run | `output/INC-008-epic-1-RWB-TE-012/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
