# Increment Card — INC-048-epic-1-RWB-E1-023

**RWB-E1-023 — Case record view v1, read only**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-048` |
| Title | Case record view v1, read only |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-023` |
| RUN_ID | `INC-048-epic-1-RWB-E1-023` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-018, RWB-E1-024, RWB-E1-037, RWB-E1-039 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P3 Case and workflow. **Build group:** P3b.

## Scope

**Story:** As a **case owner (RW-CASEOWN)**, I want **one read-only screen per case with the case ID, accounts, arrears, owner, queue, stage, status, contact history and documents, read from the data products with the business date of each**, so that **I stop searching files and systems to understand a case**.

**Main flow:**
1. Case owner: opens a case from SCR-02 Case list; SCR-03 shows the Loading state.
2. CaseRecordPage: calls GET /cases/{caseId}, GET /cases/{caseId}/accounts, GET /cases/{caseId}/parties, GET /cases/{caseId}/interactions and GET /cases/{caseId}/documents in parallel.
3. CaseAndWorkflowController: checks Case record R and the scope; out of scope returns 404.
4. CaseRecordQueryService: reads the case from P3 tables, and the account balances, arrears and party facts through the P1 interface with their data_as_of dates.
5. CaseRecordQueryService: applies the masking rules for the caller's role through FieldMasker and publishes one AC-READ access event with the field IDs read and their masked flags.
6. DocumentHub (P5): returns the document list for the case through its endpoint.

**Out of scope:**
- The history timeline on the case view (RWB-E1-035).
- The full editable case view with collateral, decisions and timers (RWB-E2-016).
- Document upload and search (RWB-E1-026).
- Collateral and valuation sections (Epic 2, after the CCMS and SVAF loads).

**Business outcome and value hypothesis:** A case owner opens EFS, ALS, shared drives and team spreadsheets today to answer one question about a case. This story puts the case, its accounts and arrears, its parties, its contact history and its documents on SCR-03, each section showing the business date of the data product it comes from, with personal fields masked by role and every view of personal data written to the access log. It meets REQ-OCC-007, REQ-RDF-009, REQ-ACA-005 and REQ-ACA-006.

**Constraints and guardrails:**
- No business value in code: masking rules, labels and timeouts are data.
- No personal data in logs, tests or prompts; test parties are synthetic and the application log holds case numbers only.
- No read of another module's tables: account and party data through RecoveryDataQuery (P1), documents through the P5 endpoint.
- Personal fields are never shown unmasked when the access log write fails.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 023 Case record view v1 read only v1.md` |
| Requirement IDs | REQ-OCC-007, REQ-RDF-009, REQ-ACA-005, REQ-ACA-006 |
| BRD section | Business Requirements Epic 1, sections 3.3, 3.4 and 3.6; Business Requirements Program, sections 5.1, 5.4 and 5.6 |
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
| RW-CASEOWN | Opens cases in scope Own (Case record R) |
| RW-TEAMMGR | Opens cases in scope Team |
| RW-PHONECOL | Opens cases in scope Own, read only, with masking |
| RW-CONDUCT, RW-AUDIT | Open every case (scope All) |
| RW-REFADM, RW-SECADM | No Case record right; refused |
| SY-CASEWF | Reads P1 data through the published interface |

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
| Quality and release | API Tester | Applicable | Required by the spec's API scope. |
| Quality and release | Functional Automation Test | Applicable | Required by the spec's UI scope. |
| Quality and release | Azure Deploy pipeline | Not used | ACE uses its own pipeline. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Feature flag:** `rwb.p3.caserecordview`. Off: SCR-03 shows the case header only.
- **Critical path:** No; **depends on:** RWB-E1-018, RWB-E1-024, RWB-E1-037, RWB-E1-039.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: masking rules, labels and timeouts are data.
  - No personal data in logs, tests or prompts; test parties are synthetic and the application log holds case numbers only.
  - No read of another module's tables: account and party data through RecoveryDataQuery (P1), documents through the P5 endpoint.
  - Personal fields are never shown unmasked when the access log write fails.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 023 Case record view v1 read only v1.md` |
| Specification | `output/INC-048-epic-1-RWB-E1-023/specify/spec.md` |
| Compliance validation | `output/INC-048-epic-1-RWB-E1-023/specify/compliance-validation.md` |
| Agent run log | `output/INC-048-epic-1-RWB-E1-023/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-048-epic-1-RWB-E1-023/plan/` (TBC) |
| Implementation evidence | `output/INC-048-epic-1-RWB-E1-023/implement/` (TBC) |
| API / functional test reports | `output/INC-048-epic-1-RWB-E1-023/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-048-epic-1-RWB-E1-023/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-048-epic-1-RWB-E1-023/specify/compliance-validation.md`) |
| Acceptance criteria | 10 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 023 Case record view v1 read only v1.md` |
| Output run | `output/INC-048-epic-1-RWB-E1-023/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
