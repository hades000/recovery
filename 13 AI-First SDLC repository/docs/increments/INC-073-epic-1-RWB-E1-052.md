# Increment Card — INC-073-epic-1-RWB-E1-052

**RWB-E1-052 — Notice generation v1**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-073` |
| Title | Notice generation v1 |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-052` |
| RUN_ID | `INC-073-epic-1-RWB-E1-052` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P6 Communications |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-015, RWB-E1-027, RWB-E1-046 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P6 Communications. **Build group:** P6.

## Scope

**Story:** As a **litigation officer (RW-LITOFF)**, I want **demand, recall and guarantor notices generated from the Legal-approved template with the case data merged**, so that **letters are produced without re-keying**.

**Main flow:**
1. Caller: calls NoticeApi.generate with case ID, notice type, party ID and language.
2. System: reads the case summary (case number, product group, status) through the P3 interface and the party role through the case parties.
3. System: asks TemplateCatalog for the current LETTER template for the notice type, product group and language on the business date.
4. System: resolves each merge code of the template through the interface of the module that owns its source field, and detokenizes personal values through the ACE PII service, which writes the access to PII Kafka.
5. System: if a required merge value is empty, holds the notice, names the field and raises a task to the case owner; stops.
6. System: renders the DOCX template to PDF and adds the footer: case number, template code, template version and generation date.

**Out of scope:**
- Dispatch to WIN and proof of delivery (RWB-E1-055, RWB-E2-021).
- Approval of demand and recall notices before dispatch (RWB-E2-014).
- The endpoint for a person to request a notice (RWB-E2-021).
- The litigation route rules that call generation in production (R-LIT-01 to R-LIT-03, Epic 5, DL24).
- Contract, credit approval and mortgage documents (RWB-E2-026).

**Business outcome and value hypothesis:** Notices are typed by hand from the core bank screens, so a wrong amount or address on a notice can void the notice period and delay litigation. This story merges the case facts into the current approved template, stores the PDF write-once on the case with the template version in the footer and records the decision. It serves REQ-OCC-001 and control CTL-14, and is the input to dispatch and proof of delivery (RWB-E1-055), which the FSD P6 measure "notices with proof of delivery, 100 percent" depends on.

**Constraints and guardrails:**
- No business value in code: notice types, templates, merge codes, task codes and the sent type mapping are data.
- No personal data in logs, tests or prompts. Names and addresses are detokenized only into the PDF; the decision log holds a reference to the merge snapshot, and the snapshot stores tokens, never clear values.
- No read of another module's tables. Case, party, account, task, document and decision log are reached through their published interfaces.
- The generated PDF is never overwritten; a correction is a new notice.
- PII Kafka receives one access event per detokenized field, through the ACE PII service.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 052 Notice generation v1 v1.md` |
| Requirement IDs | REQ-OCC-001 |
| BRD section | Business Requirements Epic 1, sections 3.6 and 4 |
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
| SY-CASEWF, case workflow module | Calls NoticeApi.generate (Litigation R, Documents R) |
| SY-DECLOG, decision log writer | Writes the D7.1 entry |
| RW-LITOFF, litigation officer | Reads the notice and the document (Litigation CRUA, Documents CRU); receives the task on a withdrawn template |
| RW-CASEOWN, case owner | Reads the notice (Litigation R) and receives the task on missing data |
| RW-LEGAL, Legal counsel | Reads the notice (Litigation RA) |

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
- **Feature flag:** `rwb.comms.notice-generation`.
- **Critical path:** No; **depends on:** RWB-E1-015, RWB-E1-027, RWB-E1-046.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: notice types, templates, merge codes, task codes and the sent type mapping are data.
  - No personal data in logs, tests or prompts. Names and addresses are detokenized only into the PDF; the decision log holds a reference to the merge snapshot, and the snapshot stores tokens, never clear values.
  - No read of another module's tables. Case, party, account, task, document and decision log are reached through their published interfaces.
  - The generated PDF is never overwritten; a correction is a new notice.
  - PII Kafka receives one access event per detokenized field, through the ACE PII service.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 052 Notice generation v1 v1.md` |
| Specification | `output/INC-073-epic-1-RWB-E1-052/specify/spec.md` |
| Compliance validation | `output/INC-073-epic-1-RWB-E1-052/specify/compliance-validation.md` |
| Agent run log | `output/INC-073-epic-1-RWB-E1-052/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-073-epic-1-RWB-E1-052/plan/` (TBC) |
| Implementation evidence | `output/INC-073-epic-1-RWB-E1-052/implement/` (TBC) |
| API / functional test reports | `output/INC-073-epic-1-RWB-E1-052/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-073-epic-1-RWB-E1-052/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-073-epic-1-RWB-E1-052/specify/compliance-validation.md`) |
| Acceptance criteria | 8 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 052 Notice generation v1 v1.md` |
| Output run | `output/INC-073-epic-1-RWB-E1-052/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
