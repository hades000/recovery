# Increment Card — INC-037-epic-1-RWB-E1-073

**RWB-E1-073 — Rule authoring, validation, test scenarios, approval and rollback in Drools**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-037` |
| Title | Rule authoring, validation, test scenarios, approval and rollback in Drools |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-073` |
| RUN_ID | `INC-037-epic-1-RWB-E1-073` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | User story |
| Priority | Must |
| Build order | 37 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-072, RWB-E1-042 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P3 Case and workflow.

## Scope

**Story:** As a **center of excellence analyst (RW-COE)**, I want **an Excel template in Drools decision-table format for each rule package, checks and scenarios on upload, approval by Risk, a dated start and rollback by one call**, so that **a rule change goes from template to production without a code release**.

**Business outcome:** Collection and recovery rules live in procedure documents today, and audit found the procedure not followed because the rules were not in the system (CTL-08). RWB-E1-029 proved the pattern for a home-built table component; this story carries the same control to Drools, where the workbook is the source of the decision table and the engine compiles it. A bad row can move every case that reaches it, so a load must be refused whole, a scenario must fail the build, and a rollback must take one call.

**Main flow:**
1. RW-COE: fills the package workbook (Rows and Tests tabs) for package ALLOCATION, version "ALLOC-2026.12", valid from 2026-12-15.
2. RW-COE: calls POST /admin/rule-packages/ALLOCATION/versions with the file and valid from.
3. RuleWorkbookParser: reads the Rows and Tests tabs, keeps row numbers and the version label, and generates the DRL.
4. DroolsCompileCheck: compiles the generated DRL; a compile error refuses the load and names the row and cell.
5. RuleLoadValidator: runs the schema check against the lists, then overlap, unreachable rows and the default row for ALLOCATION.
6. RuleScenarioRunner: runs at least rules.testcases.min scenarios (50) from the Tests tab through RuleEvaluator and compares each result with the expected queue or outcome.

**Acceptance criteria:**
- AC1: Valid load
- AC2: Overlap refused
- AC3: Scenarios
- AC4: Rollback
- AC5: Schema error
- AC6: Unreachable row
- AC7: Missing default
- AC8: Author cannot approve
- AC9: Rollback with no earlier version
- AC10: Same version loaded twice
- AC11: Valid from in the past
- AC12: Empty file
- AC13: Compile error
- AC14: Build gate fails on a scenario
- AC15: Change log records the checksum

**Out of scope:**
- The change checklist and the rule change audit report (RWB-E2-041).
- The Epic 2 packages RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH (RWB-E2-042).
- The Drools runtime, the KieBase cache and the rule catalog read (RWB-E1-072).
- Reference data loads for queues and lists (RWB-E1-019, RWB-E1-043).
- The administration screen for rule packages (Epic 8, FEAT-ADM-02).
- Loading the other 448 routing rules (later epics; DL24).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-073-rule-authoring-validation-test-scenarios-approval-and-rollback-in-drools-v1.md` |
| Requirement IDs | REQ-CWC-013, REQ-CWC-014, REQ-DRI-004, REQ-CWC-008 |
| BRD section | Business Requirements Epic 1, section 3.3; Business Requirements Program, sections 5.3 and 5.7 |
| Decision | D-RCV-36 (T3, T4, T5, T8, T10); ADR-012 |
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
| RW-COE | Loads a package version and calls rollback (Rules and parameters CRUD) |
| RW-RISK | Approves a version (Rules and parameters A); may not hold RW-COE |
| RW-AUDIT | Reads versions, scenarios, dry run counts and the change log (Rules and parameters R) |
| RW-REFADM | Prepares load files; may not approve |
| SY-RULES | Evaluates the draft and the version in force for scenarios and the dry run |
| SY-CASEWF | Applies the approved decision; no endpoint right |
| RW-TRIBE | Builds and runs RuleScenarioBuildGate; no PROD data in the build |
| No delegation of authority level applies | A rule package version is not a credit decision |

## Contract extract

**POST /api/recovery/v1/admin/rule-packages/{packageCode}/versions** (P4 endpoint) | Item | Value | |---|---| | Request | multipart/form-data: file (xlsx workbook with Rows and Tests), validFrom (date). The version label is a cell in the workbook | | Response | 201 RulePackageVersion: versionId, packageCode, versionLabel, status LOADED, validFrom, validTo, author, checksum, testResult {total, passed, failed, failedScenarioIds}, dryRunCounts {openCases, changedCases, byProduct, byQueue} | | Errors | 401 (MSG-P4-001); 403 no Rules and parameters C (MSG-P4-002); 404 unknown package code; 409 version label exists (MSG-GEN-004); 422 a check failed (MSG-P3-027, with the check, rows, cells and scenario IDs in Problem.detail), empty file (MSG-GEN-001), date order (MSG-GEN-003); 503 | | Authorization | Rules and parameters, right C | | Idempotency | Package code and version label; a repeat is re…

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

- No business value in code: rows, conditions, target queues, scenarios and the test count are data. - No personal data in logs, tests, workflow history or prompts: scenarios use synthetic case facts and the dry run reports counts only. - No read of another module's tables; ACE data only through recovery.v_ace_* views: the dry run reads case fields through the P3 repository. - One evaluator for the load checks, the scenarios, the dry run and production; no check uses a second engine. - The approver is never the author; the service checks it, not only the screen. - An in-force package version is never edited; rollback moves the pointer and writes the reason. - The build gate reads a release manifest and a Testcontainers database; it never connects to SIT, UAT or PROD and never writes a live database.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-073-rule-authoring-validation-test-scenarios-approval-and-rollback-in-drools-v1.md` |
| Specification | `output/INC-037-epic-1-RWB-E1-073/specify/spec.md` |
| Compliance validation | `output/INC-037-epic-1-RWB-E1-073/specify/compliance-validation.md` |
| Agent run log | `output/INC-037-epic-1-RWB-E1-073/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-037-epic-1-RWB-E1-073/plan/` |
| Implementation evidence | `output/INC-037-epic-1-RWB-E1-073/implement/` |
| API / functional test reports | `output/INC-037-epic-1-RWB-E1-073/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-037-epic-1-RWB-E1-073/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 15 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-073-rule-authoring-validation-test-scenarios-approval-and-rollback-in-drools-v1.md` |
| Output run | `output/INC-037-epic-1-RWB-E1-073/` |

