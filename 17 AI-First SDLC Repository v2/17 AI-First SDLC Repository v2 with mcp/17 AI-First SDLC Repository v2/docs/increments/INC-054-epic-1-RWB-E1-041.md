# Increment Card — INC-054-epic-1-RWB-E1-041

**RWB-E1-041 — Retention classes and virus scan on intake**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-054` |
| Title | Retention classes and virus scan on intake |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-041` |
| RUN_ID | `INC-054-epic-1-RWB-E1-041` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P5 Document hub |
| Story type | User story |
| Priority | Must |
| Build order | 54 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-024, RWB-E1-049 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P5 Document hub.

## Scope

**Story:** As a **compliance and PDPA officer (RW-COMPLY)**, I want **every uploaded or scanned file checked for malware before it is stored, and a retention class per document type that the store applies and a monthly job acts on**, so that **the store holds only safe files and keeps each document for the time the policy sets, never removing one silently or while a legal hold is in place**.

**Business outcome:** Files reach the bank from branches, partners and email; one infected file in the store reaches every user who opens it. Documents also have no retention rule today, so nothing shows when a document may be archived (FSD P5 A2.17, A2.18). This story scans every file before storage and quarantines a failed file, holds the retention classes as data, and runs JOB-17 to archive documents past their class or list them for the Compliance review. It meets REQ-DCM-010 and REQ-DCM-016 (legal hold overrides retention), with NFR-028, NFR-072 and NFR-074.

**Main flow:**
1. JOB-12 Document intake: runs scanStep first, before ocrStep.
2. ScanStep: selects intake items with no scan_result and sends each file to MalwareScanClient.
3. ScanStep: on CLEAN, sets scan_result CLEAN and scanned_at, so ocrStep may read the item; on INFECTED, moves the file to the quarantine container, sets scan_result INFECTED, writes the audit event MALWARE_BLOCKED and alerts the platform administrator; the file is never stored.
4. Upload (RWB-E1-026): calls MalwareScanService.scanNow before DocumentStore.store; INFECTED returns 422 MSG-P5-016; if the scanning service does not answer, the call returns 503 MSG-P5-022 and nothing is kept.
5. DocumentStore (RWB-E1-024): stores clean files with the retention class of the type; legal types go to the write-once container.
6. JOB-17 Retention job: runs on the first Sunday of each month; for each active document computes expiry date = stored date plus period_months of its class.

**Acceptance criteria:**
- AC1: Malware blocked
- AC2: Retention class
- AC3: Expiry with end action archive
- AC4: Expiry with end action review
- AC5: Legal hold overrides the class
- AC6: Scanning service unavailable
- AC7: Class not in the retention table
- AC8: Second run in the same month
- AC9: Invalid retention class load
- AC10: Expiry on the run date

**Out of scope:**
- Disposal or extension of a document at the end of its class by a recorded decision (Epic 2, REQ-DCM-019).
- Applying retention on case closure (FEAT-COM-08, Epic 4).
- Placing or lifting a legal hold (P3, POST /api/recovery/v1/cases/{caseId}/legal-hold).
- The retention and personal data screen SCR-47 (Epic 8).
- Retention of the decision log and the interaction ledger (RWB-E1-014, RWB-E2-034).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-041-retention-classes-and-virus-scan-on-intake-v1.md` |
| Requirement IDs | REQ-DCM-010, REQ-DCM-016 |
| BRD section | Business Requirements Epic 1, section 3.5; Business Requirements Program, section 5.5 |
| Decision | None |
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
| SY-OCR, OCR and extraction pipeline | Runs the scan step (Documents CRU) |
| RW-COMPLY, compliance and PDPA officer | Owns the retention classes; reads the review list and the job counts |
| RW-REFADM, reference data administrator | Loads the retention class table (Reference data C) |
| Approver with Reference data A | Approves the load; no role holds Reference data A in the permission matrix today; assumed granted to the compliance and PDPA officer as table owner (DL01) |
| RW-PLATADM, platform administrator | Receives scan alerts; reruns JOB-12 and JOB-17 |
| SY-DECLOG, decision log writer | Writes the DOCRET entry |

## Contract extract

**Job: scan step** | Item | Value | |---|---| | Trigger | JOB-12 Document intake, step scanStep, first step | | Job name | JOB-12 Document intake | | Schedule | Every 15 minutes in business hours | | Input | Intake items with no scan_result | | Output | scan_result per item; quarantined files; audit events; alert after two failed runs | | Events published | None | | Idempotency key | Intake item ID; an item with a scan_result is not scanned again | | Restart behavior | Unscanned items are taken by the next run | **Job: retention** | Item | Value | |---|---| | Trigger | Quartz schedule of JOB-17 | | Job name | JOB-17 Retention job | | Schedule | Monthly, first Sunday, Asia/Bangkok | | Input | Active documents with their class; retention class version in force; legal hold per case | | Output | Archived documents; review list file; job counts | | Events published | None | | Idempotency key…

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

- No business value in code: periods, end actions and the scan timeout are data or properties. - No personal data in logs, tests or prompts: audit events carry the intake ID and the source, never the file name or content; test files are synthetic. - No read of another module's tables: legal hold comes through CaseDirectory. - The retention job never deletes a blob and never changes a write-once blob's content.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-041-retention-classes-and-virus-scan-on-intake-v1.md` |
| Specification | `output/INC-054-epic-1-RWB-E1-041/specify/spec.md` |
| Compliance validation | `output/INC-054-epic-1-RWB-E1-041/specify/compliance-validation.md` |
| Agent run log | `output/INC-054-epic-1-RWB-E1-041/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-054-epic-1-RWB-E1-041/plan/` |
| Implementation evidence | `output/INC-054-epic-1-RWB-E1-041/implement/` |
| API / functional test reports | `output/INC-054-epic-1-RWB-E1-041/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-054-epic-1-RWB-E1-041/review/` |
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
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-041-retention-classes-and-virus-scan-on-intake-v1.md` |
| Output run | `output/INC-054-epic-1-RWB-E1-041/` |

