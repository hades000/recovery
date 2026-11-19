# Increment Card — INC-006-epic-1-RWB-TE-005

**RWB-TE-005 — Rule table test harness**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-006` |
| Title | Rule table test harness |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-TE-005` |
| RUN_ID | `INC-006-epic-1-RWB-TE-005` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | Enabler |
| Priority | Must |
| Window | Window 1 |
| Critical path | No |
| Depends on | RWB-E1-044 |
| Status | Cancelled (story retired by D-RCV-36, 16 November 2026) |

The work moves to RWB-E1-073.

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P3 Case and workflow. **Build group:** P3a.

## Scope

**Story:** As a **center of excellence analyst (RW-COE)**, I want **a harness that runs each rule row against its test case (the state, the event, the case facts and the expected result)**, so that **a rule change is tested the same way as code before it takes effect**.

**Main flow:**
1. Center of excellence analyst: loads a rule version through `POST /admin/rule-versions` with the rules and the Tests sheet.
2. P4 load handler: stores the rule rows and calls `RuleTableHarness.run(routeSet, ruleVersion)`.
3. Harness: reads the rule rows of the version and their test cases.
4. Harness: for each test case, builds a synthetic case file from the facts, evaluates the route set for the from state and the event, and gets the rows that hit.
5. Harness: passes the test when exactly one row hits, it is the row named by the test, and its to state, owner role and timer equal the expected values.
6. Harness: returns one result per rule ID; the load handler sets the version state to VALIDATED when every test passes, or FAILED otherwise, and writes the test result for the change log (RWB-E1-048).

**Out of scope:**
- The rule template, schema, overlap and unreachable row checks, load and rollback (RWB-E1-029).
- The change log and approval checklist (RWB-E1-048).
- The QA sample of closed decisions against the rule version applied (FEAT-ADM-08, Epic 8).

**Business outcome and value hypothesis:** The routing logic is 448 rules in ten route sets, held as data (ADR-004). A wrong condition or owner in one row moves every case that reaches it, and the bank has no test that proves a row does what its owner expects. Every rule row already names a test case (`rule_row.test_case_id`). This story runs those test cases on every rule load and in every build, and marks a version failed when any test fails. It meets REQ-CWC-014 and REQ-CWC-013. The measure is that every rule row in force has a passing test with its rule ID.

**Constraints and guardrails:**
- No business value in code. The expected results are data in the Tests sheet; the harness holds only the pass rule.
- No personal data in test facts, results, logs or prompts. Facts are codes and numbers.
- No read of another module's tables. Rule rows are read through the P4 interface.
- A failing harness never lets a version take effect, in any environment above DEV.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 005 Rule table test harness v1.md` |
| Requirement IDs | REQ-CWC-014, REQ-CWC-013 |
| BRD section | Business Requirements Epic 1, sections 3.3 and 4; Business Requirements Program, section 5.3 |
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
| RW-COE, center of excellence analyst | Loads a rule version, which runs the harness (Rules and parameters C); reads the results |
| RW-RISK, risk and model risk officer | Reads the results before approving (Rules and parameters R, A) |
| SY-RULES, Drools evaluator | Evaluates the rows inside the harness |
| RW-AUDIT, internal audit | Reads the results (Rules and parameters R) |

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
- **Feature flag:** `rwb.p3.rule-harness`. The flag cannot be off in SIT, UAT or PROD; off in DEV only, where a failed harness warns and the load continues.
- **Critical path:** No; **depends on:** RWB-E1-044.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code. The expected results are data in the Tests sheet; the harness holds only the pass rule.
  - No personal data in test facts, results, logs or prompts. Facts are codes and numbers.
  - No read of another module's tables. Rule rows are read through the P4 interface.
  - A failing harness never lets a version take effect, in any environment above DEV.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 005 Rule table test harness v1.md` |
| Specification | `output/INC-006-epic-1-RWB-TE-005/specify/spec.md` |
| Compliance validation | `output/INC-006-epic-1-RWB-TE-005/specify/compliance-validation.md` |
| Agent run log | `output/INC-006-epic-1-RWB-TE-005/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-006-epic-1-RWB-TE-005/plan/` (TBC) |
| Implementation evidence | `output/INC-006-epic-1-RWB-TE-005/implement/` (TBC) |
| API / functional test reports | `output/INC-006-epic-1-RWB-TE-005/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-006-epic-1-RWB-TE-005/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Cancelled (story retired by D-RCV-36, 16 November 2026) |
| Specification | SUCCESS — cleaned against the current story on 2026-11-05; no removed ACs are mapped |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-006-epic-1-RWB-TE-005/specify/compliance-validation.md`) |
| Acceptance criteria | 7 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 005 Rule table test harness v1.md` |
| Output run | `output/INC-006-epic-1-RWB-TE-005/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
