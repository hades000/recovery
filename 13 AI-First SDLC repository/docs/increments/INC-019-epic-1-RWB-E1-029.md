# Increment Card — INC-019-epic-1-RWB-E1-029

**RWB-E1-029 — Rule load, validation and rollback**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-019` |
| Title | Rule load, validation and rollback |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-029` |
| RUN_ID | `INC-019-epic-1-RWB-E1-029` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | None |
| Status | Cancelled (story retired by D-RCV-36, 16 November 2026) |

The work moves to RWB-E1-073.

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P3 Case and workflow. **Build group:** P3a.

## Scope

**Story:** As a **center of excellence analyst (RW-COE)**, I want **an Excel template for the five rule tables, validation on load (schema, overlaps, unreachable rows, missing default, 50 test cases and a dry run), a load with a version, approval, rollback by one call and a change log**, so that **a rule change goes from template to production without a code release**.

**Main flow:**
1. RW-COE: fills the Rules template (tabs Rows and Tests) for table ALLOCATION, version "ALLOC-2026.12", valid from 2026-12-15.
2. RW-COE: calls POST /admin/rule-versions with the file, route set UNIVERSAL_RULES and valid from.
3. RuleLoadValidator: runs the schema check (columns, types, lists), then overlap, unreachable rows and missing default.
4. RuleTestRunner: runs the 50 test cases against the new rows and compares each result with the expected queue or outcome.
5. RuleDryRun: evaluates the new rows against every open case and counts the cases whose result would change, by product and queue.
6. RuleVersionService: on any failed check, refuses the load whole and names every failed row or test case; on success stores the rows with status LOADED and writes the change log entry with author, time, check result and dry run counts.

**Out of scope:**
- The rule change audit report and the change checklist (RWB-E1-048).
- Loading the other 448 routing rules (later epics; DL24).
- The administration screen for rules (Epic 8, FEAT-ADM-02).
- Reference data loads for queues and lists (RWB-E1-019, RWB-E1-043).

**Business outcome and value hypothesis:** Collection and recovery rules live in procedure documents today, and audit found the procedure not followed because the rules were not in the system (CTL-08). This story takes a rule version from one template through checks that refuse a bad table whole, an approval by Risk, a dated start and a one-call rollback, with each step in the change log. It meets REQ-CWC-013, REQ-CWC-014 and REQ-DRI-004, and covers the Epic 1 rule tables named in DL24: entry, exclusion, allocation, assignment and transfer.

**Constraints and guardrails:**
- No business value in code: rows, conditions, target queues, test cases and the test count are data.
- No personal data in logs, tests, the dry run report or prompts; the dry run reports counts only.
- No read of another module's tables: P3 validation receives rows as drafts; rule_row is written only by P4 code.
- The engines and the test runner use the same evaluator, so a passed test means the same result in production.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 029 Rule load validation and rollback v1.md` |
| Requirement IDs | REQ-CWC-013, REQ-CWC-014, REQ-DRI-004 |
| BRD section | Business Requirements Epic 1, section 3.3; Business Requirements Program, sections 5.3 and 5.7 |
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
| RW-COE | Loads versions and calls rollback (Rules and parameters CRUD) |
| RW-RISK | Approves a version (Rules and parameters A); may not hold RW-COE |
| RW-AUDIT | Reads versions and the change log (Rules and parameters R) |
| RW-REFADM | Prepares load files; may not approve |
| SY-RULES | Reads the version in force for evaluation |
| No delegation of authority level applies | A rule version is not a credit decision |

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
- **Feature flag:** `rwb.p3.ruleload`. Off: the load and rollback endpoints return 404; the version in force stays.
- **Critical path:** No; **depends on:** None.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: rows, conditions, target queues, test cases and the test count are data.
  - No personal data in logs, tests, the dry run report or prompts; the dry run reports counts only.
  - No read of another module's tables: P3 validation receives rows as drafts; rule_row is written only by P4 code.
  - The engines and the test runner use the same evaluator, so a passed test means the same result in production.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 029 Rule load validation and rollback v1.md` |
| Specification | `output/INC-019-epic-1-RWB-E1-029/specify/spec.md` |
| Compliance validation | `output/INC-019-epic-1-RWB-E1-029/specify/compliance-validation.md` |
| Agent run log | `output/INC-019-epic-1-RWB-E1-029/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-019-epic-1-RWB-E1-029/plan/` (TBC) |
| Implementation evidence | `output/INC-019-epic-1-RWB-E1-029/implement/` (TBC) |
| API / functional test reports | `output/INC-019-epic-1-RWB-E1-029/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-019-epic-1-RWB-E1-029/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Cancelled (story retired by D-RCV-36, 16 November 2026) |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-019-epic-1-RWB-E1-029/specify/compliance-validation.md`) |
| Acceptance criteria | 12 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11, AC12) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 029 Rule load validation and rollback v1.md` |
| Output run | `output/INC-019-epic-1-RWB-E1-029/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
