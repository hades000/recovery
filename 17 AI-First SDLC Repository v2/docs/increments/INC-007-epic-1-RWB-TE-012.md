# Increment Card — INC-007-epic-1-RWB-TE-012

**RWB-TE-012 — Document storage containers**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-007` |
| Title | Document storage containers |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-TE-012` |
| RUN_ID | `INC-007-epic-1-RWB-TE-012` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P5 Document hub |
| Story type | Enabler |
| Priority | Must |
| Build order | 7 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-TE-001 |
| Blocks | See the build sequence |
| Status | Ready for specify |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P5 Document hub.

## Scope

**Story:** As a **platform administrator**, I want **blob containers for documents, with a write-once container for legal types, reached by managed identity**, so that **legal documents cannot be overwritten**.

**Business outcome:** Audit findings record that evidence for decisions was incomplete or unreliable, and a notice or contract held in a shared folder can be replaced without trace. This story sets up the storage that the document store (RWB-E1-024), the intake (RWB-E1-057) and the malware scan (RWB-E1-041) write to: an intake container, a standard container with version history, a write-once container whose immutability policy refuses any overwrite or delete inside its retention period, and a quarantine container, all reached only by managed identity. It meets REQ-DCM-003 and REQ-DCM-002 and is the storage behind control CTL-12 and the storage pattern recommended under DL27.

**Main flow:**
1. Platform administrator: applies the infrastructure template for the environment, which sets the storage account (shared key access off, public network access off, TLS 1.2 minimum, private endpoint) and creates the containers rwb-intake, rwb-docs, rwb-docs-legal and rwb-quarantine.
2. Template: turns on blob versioning and soft delete for rwb-docs, sets the time-based immutability policy on rwb-docs-legal (locked in PROD, unlocked in DEV, SIT and UAT), and assigns roles: the ACE service identity on rwb-intake, rwb-docs and rwb-docs-legal; SY-OCR on rwb-intake, rwb-docs and rwb-quarantine.
3. System: on start, StorageReadinessIndicator checks that the four containers exist and that rwb-docs-legal has its immutability policy; the document hub reports ready only if both hold.
4. Document store (RWB-E1-024): writes each file through BlobStorageAdapter with the managed identity, to rwb-docs-legal for a write-once type and to rwb-docs for any other type, at the name {caseId}/{documentId}/v{docVersion}.
5. Any client: an overwrite or delete of a blob in rwb-docs-legal is refused by the storage service; StorageErrorMapper turns the refusal into WriteOnceViolationException, which the store maps to 409 MSG-P5-002, and the attempt is written to the ACE audit log.
6. Document store: a new version is a new blob at v{n+1}; the earlier blob stays readable.

**Acceptance criteria:**
- AC1: Write-once
- AC2: Delete is refused
- AC3: A new blob in the write-once container is allowed
- AC4: The standard container keeps earlier versions
- AC5: The identities hold only their roles
- AC6: Key-based access is refused
- AC7: An identity with no role is refused
- AC8: Public network access is refused
- AC9: A missing immutability policy stops the document hub
- AC10: Storage does not answer
- AC11: The quarantine container is closed to user sessions
- AC12: A repeated write of the same file is not an overwrite

**Out of scope:**
- Choosing the container per document type and writing the document row (RWB-E1-024).
- Retention classes, archive and the retention job (RWB-E1-041, JOB-17).
- Legal hold on a case or a document (REQ-DCM-016; DL27).
- Backup and restore test of the document store (REQ-DCM-015; DL27).
- Sizing and cost of the storage (REQ-DCM-014; NFR-069).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-012-document-storage-containers-v1.md` |
| Requirement IDs | REQ-DCM-003, REQ-DCM-002 |
| BRD section | Business Requirements Program, section 5.5 |
| Decision | DL27 |
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
| RW-PLATADM, platform administrator | Applies the infrastructure template and reads the readiness check (Platform administration CRUD) |
| RW-SECADM, security administrator | Reviews the role assignments on the containers (Platform administration CRUDA) |
| SY-OCR, OCR and extraction pipeline | Writes to rwb-intake, rwb-docs and rwb-quarantine with its managed identity |
| RW-CASEOWN, case owner | Uploads documents through the store, which uses the ACE service identity (Documents CRU) |
| Solution architect with Compliance | Owns DL27 |

## Contract extract

No endpoint of its own. The upload endpoint POST /api/recovery/v1/cases/{caseId}/documents (RWB-E1-026, RWB-E1-024) uses these containers: Documents, right C, scope applied; 403 without the right (MSG-P4-002); 503 when storage is unavailable or the document hub is not ready (MSG-GEN-006). **Container configuration (P5, used by BlobStorageAdapter in RWB-E1-024, QuarantineMover in RWB-E1-041 and IntakeService in RWB-E1-057)** ```java package recovery.dochub.storage; public interface DocumentContainers { BlobContainerClient intake(); // rwb.dochub.container.intake BlobContainerClient standard(); // rwb.dochub.container.standard BlobContainerClient legal(); // rwb.dochub.container.legal BlobContainerClient quarantine(); // rwb.dochub.container.quarantine StorageReadiness readiness(); // containers present, legal policy present } // Exceptions raised to callers: WriteOnceViolationException,…

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

- No business value in code: the retention period, soft delete days and container names come from template parameters and properties. - No personal data in logs, tests or prompts: blob names carry case and document IDs only, never a customer name or ID number; test files are synthetic. - No read of another module's tables. - No account key, connection string or shared access signature in code, configuration or the pipeline.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-012-document-storage-containers-v1.md` |
| Specification | `output/INC-007-epic-1-RWB-TE-012/specify/spec.md` |
| Compliance validation | `output/INC-007-epic-1-RWB-TE-012/specify/compliance-validation.md` |
| Agent run log | `output/INC-007-epic-1-RWB-TE-012/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-007-epic-1-RWB-TE-012/plan/` |
| Implementation evidence | `output/INC-007-epic-1-RWB-TE-012/implement/` |
| API / functional test reports | `output/INC-007-epic-1-RWB-TE-012/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-007-epic-1-RWB-TE-012/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Ready for specify |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 12 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-012-document-storage-containers-v1.md` |
| Output run | `output/INC-007-epic-1-RWB-TE-012/` |

