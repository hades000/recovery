# Technical Specification — RWB-TE-005 Rule table test harness

| Field | Value |
|---|---|
| Story | RWB-TE-005 — Rule table test harness |
| Epic / module | E1 / P3 Case and workflow |
| RUN_ID | `INC-006-epic-1-RWB-TE-005` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-008); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 005 Rule table test harness v1.md` |
| Upstream IDs | BRD-RWB-003, BRD-RWB-020; FR-RWB-008; REQ-CWC-013, REQ-CWC-014; US-RWB-TE-005; CTX-FEATURE-003; ADR-004; DF-REF-015, DF-REF-185..197 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. The analyst reads the load response and the version list; SCR-39 is Epic 8. |
| Logic In Scope | `YES` — test-case extraction, synthetic case build, evaluation, pass rule, version state and build gate. |
| API In Scope | `NO` — no new or changed contract. The story is called by `POST /admin/rule-versions` and listed by `GET /admin/rule-versions` (P4, delivered by RWB-E1-029). |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | P4 rule-version load handler; rule evaluator (SY-RULES); rule version state; build pipeline. |
| New Nodes Required | `YES` — `RuleTableHarnessImpl`, `CaseFileFixtureBuilder`, `RuleTestCaseRepository`, `TestsSheetReader`, `RuleTableHarnessTest`, `rule_test_case` table. |
| Inherited Existing Behavior | RWB-E1-029 rule template, load and version state; RWB-E1-044 migrations; ADR-004 decision-table evaluator with hit policy Unique; RWB-E1-048 change log. |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Every rule row has one test case, named by its `test_case_id`. | SPEC-RWB-TE-005-001, SPEC-RWB-TE-005-002 | DIRECT | Tests sheet read into `rule_test_case`; a row without a test fails the version. | COVERED |
| BR2 | A test passes when exactly one row hits, it is the named row, and its to state, owner role and timer equal the expected values. | SPEC-RWB-TE-005-004 | DIRECT | Hit policy Unique; zero hits, two hits and any field difference fail. | COVERED |
| BR3 | A version with any failing test is FAILED and cannot be approved or take effect. | SPEC-RWB-TE-005-005 | DIRECT | Version state written before approval is possible. | COVERED |
| BR4 | The harness runs on every rule load and in every build. | SPEC-RWB-TE-005-006, SPEC-RWB-TE-005-011 | DIRECT | P4 load handler call plus the `ruleTests` Gradle task. | COVERED |
| BR5 | Tests use synthetic case facts only. | SPEC-RWB-TE-005-003 | DIRECT | `CaseFileFixtureBuilder` accepts codes and numbers only; no customer or account data. | COVERED |
| BR6 | The completeness checks of the rule set run before the tests. | SPEC-RWB-TE-005-008 | DIRECT | `rules.txt` Checks run first; a completeness failure stops the harness. | COVERED |
| AC1 | 37 tests run on RES-2026.11; each names its rule and test case; all pass and the version is VALIDATED. | SPEC-RWB-TE-005-001, SPEC-RWB-TE-005-002, SPEC-RWB-TE-005-005 | DIRECT | One result per rule row. | COVERED |
| AC2 | A changed to state fails R-RES-04 with expected and actual named; version FAILED and not approvable. | SPEC-RWB-TE-005-004, SPEC-RWB-TE-005-005 | DIRECT | R-RES-04 expects WITH_FCR_OFFICER, row has IN_FCR_QUEUE. | COVERED |
| AC3 | A row naming a missing test case marks the version FAILED naming row and test case. | SPEC-RWB-TE-005-002, SPEC-RWB-TE-005-005 | DIRECT | R-RES-12 / RT-RES-012. | COVERED |
| AC4 | Two rows hitting one input fails naming both rule IDs. | SPEC-RWB-TE-005-004 | DIRECT | R-RES-09 and R-RES-10. | COVERED |
| AC5 | No row hitting a test input fails naming the expected rule. | SPEC-RWB-TE-005-004 | DIRECT | R-RES-28. | COVERED |
| AC6 | A missing fact fails naming the fact. | SPEC-RWB-TE-005-003 | DIRECT | `break_count` for R-RES-30. | COVERED |
| AC7 | A repeated run returns the same 37 passes and stores one result set. | SPEC-RWB-TE-005-007 | DIRECT | Unique (route set, version, test case); result rows updated, not duplicated. | COVERED |
| X1..X6 | Exceptional paths in the table below map to SPEC-002..007. | SPEC-RWB-TE-005-002..007 | DIRECT | Wrong action, missing test, two hits, no hit, missing fact, repeated run. | COVERED |

> **AC cleanup (4 November 2026):** the development-process criteria removed from story §7 are not mapped here. The remaining acceptance criteria are those in the current story.

## User story intent interpretation

As a **center of excellence analyst (RW-COE)**, I want **a harness that runs each rule row against its test case (the state, the event, the case facts and the expected result)**, so that **a rule change is tested the same way as code before it takes effect**.

The story is a technical enabler for the rules component. It turns the Tests sheet that already accompanies every rule template into an executable gate: the load handler calls it, the build calls it, and a version with any failing row cannot be approved. It adds no screen and no business rule; the expected results are data.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | Every rule-version load through `POST /admin/rule-versions`; every build through the `ruleTests` task. |
| Preconditions | RWB-E1-044 done; the rules component evaluates a route set as a decision table with hit policy Unique (ADR-004); the rule template carries a Tests sheet with one case per row; every rule row has `test_case_id`; the Restructure route set is loaded in SIT with 37 rows; the loader holds RW-COE. |
| Input | Rule rows of the version, the Tests sheet, the route set and rule version identifiers. |
| Output | `HarnessResult` with one `RuleTestResult` per rule ID; `rule_test_case` rows; version state VALIDATED or FAILED; build report. |
| Feature flag | `rwb.p3.rule-harness`. Cannot be off in SIT, UAT or PROD; off in DEV only, where a failed harness warns and the load continues but the version stays FAILED. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `rule_test_case` | `test_case_id`, `route_set`, `rule_version`, `rule_id` | Tests sheet | New row per load | Unique (route_set, rule_version, test_case_id); rule ID must exist in the version. |
| `rule_test_case` | `from_state`, `event_code` | Tests sheet | New row per load | Must match the row's from state and event. |
| `rule_test_case` | `facts` | Tests sheet | New row per load | JSON object of synthetic codes and numbers; no personal data. |
| `rule_test_case` | `expected_to_state`, `expected_owner_role`, `expected_timer_spec` | Tests sheet | New row per load | Compared exactly with the hit row. |
| `rule_test_case` | `result`, `result_detail` | Harness | System-written | PASSED or FAILED; detail names expected, actual and hit rule IDs. |
| `rule_row` | `test_case_id` | Rule template | Read-only in this story | Required; a missing or unknown ID fails the version. |
| Rule version | `state` | Load handler | System-written | VALIDATED only when every test passes; FAILED otherwise. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | Load with Tests sheet | Every test passes | VALIDATED | One result per rule ID; version may be approved. |
| None | Load with Tests sheet | Any test fails | FAILED | Failing rule IDs and test case IDs in the response; approval refused. |
| FAILED | Approve | — | FAILED | Approval refused; no effect. |
| VALIDATED | Approve | Approver is not the author | APPROVED | Normal RWB-E1-029 flow. |

This story changes no case status.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | To state, owner or timer differs from the test | Test fails; version FAILED | MSG-P3-014 |
| X2 | Rule row has no test case in the Tests sheet | Version FAILED naming the rule | MSG-P3-014 |
| X3 | Two rows hit the same input | Test fails naming both rule IDs | MSG-P3-014 |
| X4 | No row hits a test input | Test fails naming the expected rule | MSG-P3-014 |
| X5 | A fact is missing or unused by the condition | Test fails naming the fact | MSG-P3-014 |
| X6 | The same version is run twice | Same results; one result set | None |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `POST /api/recovery/v1/admin/rule-versions` (runs the harness); `GET /api/recovery/v1/admin/rule-versions?routeSet=&status=` (lists VALIDATED/FAILED). |
| Contract delta | None. The 422 `Problem.detail` listing failing rule IDs is already described in API Specification v2 for this endpoint (MSG-P3-014, RWB-TE-005). |
| Backward compatibility | Unchanged. |
| Authorization | Rules and parameters C to load; R to read results. 401 MSG-P4-001; 403 MSG-P4-002; 409 MSG-GEN-004; 422 MSG-P3-014; 503. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label change. | Existing frontend tests remain green. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | FR-RWB-008; SPEC-RWB-TE-005-001..011 | New harness, fixture builder, sheet reader, repository and build test factory. | Positive, negative, boundary and error-path tests: 37 passes, wrong state, missing test, two hits, zero hits, missing fact, repeat, 448 build tests. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `RuleTableHarnessImpl` | Service | Runs every test of a version through the evaluator and builds the result. |
| `CaseFileFixtureBuilder` | Service | Builds a synthetic case file from the test facts; refuses a missing fact. |
| `RuleTestCaseRepository` | Repository | Reads and writes `rule_test_case`. |
| `TestsSheetReader` | Service | Reads the Tests sheet of the rule template into test cases. |
| `RuleTableHarnessTest` | Build job | JUnit 5 dynamic test factory, one test per rule ID. |
| `RuleTableHarness` | Published interface | `run(routeSet, ruleVersion)` returning `HarnessResult`. |

### Package and boundaries

`recovery.casewf.rules.harness` in the recovery module; tests in
`recovery/src/test/java/recovery/casewf/rules/harness`. Rule rows are read through the P4
`RuleTableReader`; the harness never queries `rule_row` directly. The P4 load handler calls the
published interface; it does not depend on the implementation.

### Data and migration

`V<next>__rwb_te_005_rule_test_case.sql` creates `rule_test_case` (`id uuid PK`, `test_case_id
varchar(20)`, `route_set varchar(15)`, `rule_version varchar(20)`, `rule_id varchar(20)`,
`from_state varchar(60)`, `event_code varchar(60)`, `facts jsonb`, `expected_to_state varchar(60)`,
`expected_owner_role varchar(20)`, `expected_timer_spec varchar(60)`, `result varchar(10)`,
`result_detail varchar(1000)`, standard columns) with `UNIQUE (route_set, rule_version,
test_case_id)`. The schema comes from `${schema}`.

### Pass rule and hit policy

1. Read the rows of the version and their test cases.
2. Build a synthetic case file from `facts`; a missing fact fails the test.
3. Evaluate the route set for the from state and event with hit policy Unique.
4. The test passes only when exactly one row hits, that row is the named row, and its to state, owner
   role and timer equal the expected values.
5. A zero-hit, multi-hit or field difference fails with expected and actual in the detail.

### Build integration

The Gradle task `ruleTests` runs `RuleTableHarnessTest` as a JUnit 5 dynamic test factory over
`recovery/src/test/resources/rules/*.xlsx`, one test per rule ID. The build runs 448 tests across the
ten route sets and fails on any failing rule test.

### Transaction and events

The load handler runs the harness before storing a version as VALIDATED. The harness writes its result
rows in the same transaction as the version state. A repeated run updates the same result set; it does
not insert a second one. No event is published.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-COE | Rules and parameters C; loads a version and reads results | All |
| RW-RISK | Rules and parameters R/A; reads results before approval | All |
| SY-RULES | Evaluates the rows inside the harness | All |
| RW-AUDIT | Rules and parameters R; reads results | All |

The harness runs under the caller's identity; it does not elevate. A role without Rules and parameters
C receives 403 MSG-P4-002 at the load endpoint.

### Observability and operations

- Load response: total, passed, failed and each `RuleTestResult`.
- Build report: one named test per rule ID; a failing test fails the build.
- Metrics: tests run, pass rate, harness duration, versions refused.
- No personal data in facts, results or logs; facts are codes and numbers.

### Performance

- 448 rule evaluations per build; each is an in-memory decision-table evaluation.
- A load evaluates one route set at a time; the 37-row Restructure set is the SIT baseline.
- Results are written in one batch per version.

### Feature flag and rollback

- `rwb.p3.rule-harness`: off in DEV only, where a failed harness warns and the load continues but the
  version remains FAILED and cannot be approved. It cannot be off in SIT, UAT or PROD.
- Rollback: turn the flag off in DEV; redeploy the previous tag. No data rollback is needed.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-TE-005-01 | AC1, BR1, BR2 | System | Restructure 37 rows and 37 tests | 37 pass; version VALIDATED |
| TC-TE-005-02 | AC2, BR2, BR3 | System | R-RES-04 changed to IN_FCR_QUEUE | Fails; expected/actual named; version FAILED |
| TC-TE-005-03 | AC3, BR1 | System | R-RES-12 names missing RT-RES-012 | FAILED; both IDs named |
| TC-TE-005-04 | AC4, BR2 | System | R-RES-09 and R-RES-10 both hold | Fails; both rule IDs named |
| TC-TE-005-05 | AC5, BR2 | System | R-RES-28 condition matches nothing | Fails; R-RES-28 named |
| TC-TE-005-06 | AC6, BR5 | System | R-RES-30 without `break_count` | Fails; fact named |
| TC-TE-005-07 | AC7 | System | Same version twice | Same 37 results; one result set |
| TC-TE-005-08 | BR4 | System | 448 rows in repository rule files | 448 named tests; a failure fails the build |
| TC-TE-005-09 | Authority | Security | RW-CASEOWN loads a version | 403; MSG-P4-002 |
| TC-TE-005-10 | BR6 | Unit | Completeness failure before tests | Harness does not run; version FAILED |

## Guardrails and out of scope

- No business value in code; expected results are data in the Tests sheet. The harness holds only the
  pass rule.
- No personal data in test facts, results, logs or prompts. Facts are codes and numbers.
- Rule rows are read through the P4 interface; no cross-module table read.
- Out of scope: the rule template, schema, overlap, unreachable-row and default checks, load and
  rollback (RWB-E1-029); the change log and approval checklist (RWB-E1-048); the QA sample of closed
  decisions (FEAT-ADM-08, Epic 8).

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | AC1, SPEC-006 | Is the harness run over 37 rows or 448? | Determines the SIT and build fixtures. | Both: 37 Restructure rows in SIT, 448 rows across the ten route sets in the build. | RESOLVED | SPEC-006 |
| CLAR-002 | BR1; SPEC-001 | Is the Tests sheet or `rule_test_case` the source of truth? | Determines what is reviewed. | The Tests sheet is the reviewed source; `rule_test_case` stores the parsed case and result. | RESOLVED | SPEC-001 |
| CLAR-003 | BR3, feature flag; SPEC-005 | What happens in DEV when the flag is off and a test fails? | Load may continue in DEV. | The load continues with a warning, but the version is FAILED and cannot be approved or take effect. | RESOLVED | SPEC-005 |
| CLAR-004 | AC4; SPEC-004 | Which row wins when two rows hit? | Hit policy. | No row wins: hit policy Unique, so a two-hit result is a test failure naming both rows. | RESOLVED | SPEC-004 |
| CLAR-005 | BR5; SPEC-003 | May test facts contain customer data? | PDPA. | No. Facts are synthetic codes and numbers only. | RESOLVED | SPEC-003 |
| CLAR-006 | Flow 4; SPEC-004 | Does the harness use the same evaluator as production? | A different evaluator would make the test meaningless. | Yes; the shared decision-table evaluator is called with a synthetic case file. | RESOLVED | SPEC-004 |
| CLAR-007 | Contract; SPEC-009 | Does the harness need a new endpoint? | Contract delta. | No; it is called inside `POST /admin/rule-versions` and read through the existing GET. | RESOLVED | SPEC-009 |

`CLARIFICATION_STATUS: RESOLVED` — all 7 items are answered from the story, ADR-004 or the API
specification. No item changes a business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend test-enabler story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New rule-table test harness; no screen and no contract change; the existing rule-version load endpoint calls it.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: test harness inside the existing rule-version load with no contract delta]
REQUIREMENT_COVERAGE_SUMMARY: All 6 business rules, 7 acceptance criteria, 6 exception paths and 3 version states are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 6] [COVERED_RULES: 6] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
