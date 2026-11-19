# Increment Card — INC-072-epic-1-RWB-E1-048

**RWB-E1-048 — Rule change audit report**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-072` |
| Title | Rule change audit report |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-048` |
| RUN_ID | `INC-072-epic-1-RWB-E1-048` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | Enabler |
| Priority | Should |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-037, RWB-E1-011, RWB-E1-043 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P3 Case and workflow. **Build group:** P3b.

## Scope

**Story:** As a **center of excellence analyst (RW-COE)**, I want **the parameter change and rule change checklist (request, impact, test result, approver, load, verify, rollback plan) recorded on every change and reported for audit**, so that **a configuration change is as controlled as a code change**.

**Main flow:**
1. Center of excellence analyst: raises the change request in the bank's request tool and receives its reference, for example CR-2026-0042.
2. Reference data administrator: loads the new version through `POST /admin/reference-loads` (or `POST /admin/rule-versions`) with the request reference, the impact summary and the rollback plan as form fields.
3. Reference data service: stores the checklist fields on the version and records the test result from the load checks or the harness (PASSED or FAILED).
4. Approver: approves through `POST /admin/reference-loads/{loadId}/approve`.
5. Reference data service: refuses the approval unless the request reference, impact summary, rollback plan and a PASSED test result are present and the approver is not the author.
6. Reference data administrator: after the valid from date, records the verification through `POST /admin/reference-loads/{loadId}/verify`.

**Out of scope:**
- The load, validation and rollback of rule versions (RWB-E1-029).
- The rule table test harness that produces the rule test result (RWB-TE-005).
- The rules and parameters screen (SCR-39, Epic 8).
- The QA sample against the rule version applied (FEAT-ADM-08, Epic 8).

**Business outcome and value hypothesis:** Audit found the collection procedure was not followed because rules lived in documents (CTL-08). When rules and limits are data, a wrong row changes every case it touches, so each change needs the same evidence as a code change: who asked, what it affects, the test result, who approved, when it took effect and how to undo it. This story makes the checklist fields required before a version can be approved and gives audit one report of every change. It meets REQ-CWC-013 and REQ-DRI-011. The measure is that every version in force has a complete checklist in the report.

**Constraints and guardrails:**
- No business value in code. The checklist items are the fields; the report computes from rows.
- No personal data in logs, tests, the report or prompts. The report carries user IDs of staff and no customer or case data.
- No read of another module's tables. Rule versions reach the registry through the P4 handler calling the published interface.
- The report reads the registry; it never recomputes a version from the live tables.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 048 Rule change audit report v1.md` |
| Requirement IDs | REQ-CWC-013, REQ-DRI-011 |
| BRD section | Business Requirements Epic 1, sections 3.3 and 4; Business Requirements Program, sections 5.3 and 5.7 |
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
| RW-REFADM, reference data administrator | Loads a version with its checklist fields; records verification (Reference data C, U) |
| RW-COE, center of excellence analyst | Loads rule and reference versions; reads the report (Rules and parameters R) |
| RW-RISK, risk and model risk officer | Approves versions (Rules and parameters A; Reference data approve right assumed as in RWB-E1-043); reads the report |
| RW-AUDIT, internal audit | Reads and exports the report (Rules and parameters R). Changes nothing |
| RW-PLATADM, platform administrator | Reads the report (Rules and parameters R) |

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
| Quality and release | Functional Automation Test | Not used | UI is not in scope. |
| Quality and release | Azure Deploy pipeline | Not used | ACE uses its own pipeline. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Feature flag:** `rwb.p3.change-log`. Off: approval runs the RWB-E1-043 checks only and the report endpoint returns 404.
- **Critical path:** No; **depends on:** RWB-E1-037, RWB-E1-011, RWB-E1-043.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code. The checklist items are the fields; the report computes from rows.
  - No personal data in logs, tests, the report or prompts. The report carries user IDs of staff and no customer or case data.
  - No read of another module's tables. Rule versions reach the registry through the P4 handler calling the published interface.
  - The report reads the registry; it never recomputes a version from the live tables.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 048 Rule change audit report v1.md` |
| Specification | `output/INC-072-epic-1-RWB-E1-048/specify/spec.md` |
| Compliance validation | `output/INC-072-epic-1-RWB-E1-048/specify/compliance-validation.md` |
| Agent run log | `output/INC-072-epic-1-RWB-E1-048/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-072-epic-1-RWB-E1-048/plan/` (TBC) |
| Implementation evidence | `output/INC-072-epic-1-RWB-E1-048/implement/` (TBC) |
| API / functional test reports | `output/INC-072-epic-1-RWB-E1-048/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-072-epic-1-RWB-E1-048/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-072-epic-1-RWB-E1-048/specify/compliance-validation.md`) |
| Acceptance criteria | 9 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 048 Rule change audit report v1.md` |
| Output run | `output/INC-072-epic-1-RWB-E1-048/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
