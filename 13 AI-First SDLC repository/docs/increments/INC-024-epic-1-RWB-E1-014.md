# Increment Card — INC-024-epic-1-RWB-E1-014

**RWB-E1-014 — Decision log copy to the data lake**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-024` |
| Title | Decision log copy to the data lake |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-014` |
| RUN_ID | `INC-024-epic-1-RWB-E1-014` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | User story |
| Priority | Should |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-056, RWB-E1-017 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P1 Recovery data engine. **Build group:** P1a.

## Scope

**Story:** As a **center of excellence analyst (RW-COE)**, I want **the decision log copied to the data lake each night, with a retention rule applied to the copy**, so that **reporting reads the log without touching the live log and nothing in the copy is kept longer than its rule**.

**Main flow:**
1. Quartz: starts JOB-13 Decision log copy at 01:00 for business date D (the previous calendar day).
2. DecisionLogLakeCopyService: reads the watermark (last copied entry hash and cumulative count) from lake_copy_watermark.
3. DecisionLogLakeCopyService: calls DecisionLogExport.head() and fixes the cut-off: the live count and last entry hash at start.
4. DecisionLogLakeCopyService: calls DecisionLogExport.entriesAfter(watermarkHash, 5000) in chain order until it reaches the cut-off hash.
5. LakeFileWriter: writes the entries to `decision-log/business_date=D/` as Parquet files and writes `_manifest.json` with the row count, first hash, last hash and cumulative count.
6. LakeCopyReconciler: reads the manifest back from the lake and compares the cumulative count and last hash with the cut-off (REC-08, tolerance zero).

**Out of scope:**
- Retention of the live decision log (NFR-030, DL26) and the hash chain check (JOB-14, RWB-TE-008).
- Operations reports built on the copy (FEAT-RPT-04, Epic 2).
- Logging each read of the lake copy to the access log (REQ-ACA-006, RWB-E1-039).
- The retention rule table and the data store retention job (RWB-E1-017).

**Business outcome and value hypothesis:** Reporting, audit sampling and model feedback need the full decision history, and queries against the live log slow the write path that every action depends on (ADR-009). A nightly copy that matches the live log on row count and last hash gives Power BI and audit one checked source (REC-08). The copy carries its own retention rule, so the lake does not keep decisions longer than the bank schedule allows. Serves REQ-DRI-009 and REQ-RDF-013; measure: copy matched on count and last hash on 99 percent of days (FSD P1 A2.20.1).

**Constraints and guardrails:**
- No business value in code: the retention period, page size, file size and lake path are data rows or properties.
- No personal data in logs, tests or prompts. Test entries use synthetic case IDs and synthetic hashes; inputs_ref holds references only.
- No read of another module's tables: decision_log_entry is read only through DecisionLogExport.
- The job never writes, updates or deletes a live decision log entry.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 014 Decision log copy to the data lake v1.md` |
| Requirement IDs | REQ-DRI-009, REQ-RDF-013 |
| BRD section | Business Requirements Epic 1, section 3.1 (story) and section 4 (REQ-DRI-009, REQ-RDF-013) |
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
| SY-DATALOAD, data load | Runs JOB-13, reads through DecisionLogExport, writes the lake files and the watermark |
| SY-DECLOG, decision log writer | Owns the live log; not called for writes in this story |
| RW-PLATADM, platform administrator | Reruns JOB-13 (Platform administration U) |
| RW-DATASTEW, data steward | Reads the job result and the break (Platform administration R) |
| RW-COE, RW-AUDIT, RW-COMPLY | Read the job monitor (Platform administration R); read the lake copy in Power BI |
| RW-BIANAL, reporting and BI analyst | Reads the lake copy for reporting |

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
- **Feature flag:** `rwb.dataengine.lake-copy`.
- **Critical path:** No; **depends on:** RWB-E1-056, RWB-E1-017.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: the retention period, page size, file size and lake path are data rows or properties.
  - No personal data in logs, tests or prompts. Test entries use synthetic case IDs and synthetic hashes; inputs_ref holds references only.
  - No read of another module's tables: decision_log_entry is read only through DecisionLogExport.
  - The job never writes, updates or deletes a live decision log entry.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 014 Decision log copy to the data lake v1.md` |
| Specification | `output/INC-024-epic-1-RWB-E1-014/specify/spec.md` |
| Compliance validation | `output/INC-024-epic-1-RWB-E1-014/specify/compliance-validation.md` |
| Agent run log | `output/INC-024-epic-1-RWB-E1-014/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-024-epic-1-RWB-E1-014/plan/` (TBC) |
| Implementation evidence | `output/INC-024-epic-1-RWB-E1-014/implement/` (TBC) |
| API / functional test reports | `output/INC-024-epic-1-RWB-E1-014/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-024-epic-1-RWB-E1-014/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — regated 2026-11-06: clarifications resolved by the D-RCV rulings; gate-002 compliance PASS |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-024-epic-1-RWB-E1-014/specify/compliance-validation.md`) |
| Acceptance criteria | 8 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 014 Decision log copy to the data lake v1.md` |
| Output run | `output/INC-024-epic-1-RWB-E1-014/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
